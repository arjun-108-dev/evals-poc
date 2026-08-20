"""Utilities for the tiny-model tool-calling evaluator.

Handles locating the Ollama binary, ensuring the server is reachable, and
calling the Ollama chat API with tools. Pure standard library so the project
has no hard third-party dependencies at evaluation time.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from typing import Any, Optional

# A few well-known places Ollama installs itself on Windows.
_OLLAMA_CANDIDATE_PATHS = [
    r"C:\Users\techs\AppData\Local\Programs\Ollama\ollama.exe",
    r"C:\Program Files\Ollama\ollama.exe",
    os.path.expanduser(r"~\.ollama\ollama.exe"),
]

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def find_ollama() -> Optional[str]:
    """Return the path to the ollama executable, or None if not found."""
    on_path = shutil.which("ollama")
    if on_path:
        return on_path
    for p in _OLLAMA_CANDIDATE_PATHS:
        if os.path.isfile(p):
            return p
    return None


def ensure_server(timeout: float = 30.0) -> bool:
    """Return True if the Ollama server is reachable within `timeout` seconds."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=2):
                return True
        except Exception:
            time.sleep(0.5)
    return False


def pull_model(tag: str, exe: Optional[str] = None) -> bool:
    """Pull a model via the Ollama CLI. Returns True on success."""
    exe = exe or find_ollama()
    if not exe:
        print("[pull] ollama executable not found; cannot pull", file=sys.stderr)
        return False
    print(f"[pull] pulling {tag} (this may take a while)...")
    try:
        proc = subprocess.run([exe, "pull", tag], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              encoding="utf-8", errors="replace")
        # Print progress (pull uses \r carriage returns); keep last lines.
        out = proc.stdout or ""
        for line in out.splitlines()[-15:]:
            print("   ", line)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[pull] failed for {tag}:\n{e.stdout}", file=sys.stderr)
        return False


def _normalize_tool_calls(raw: Any) -> list[dict]:
    """Normalize Ollama's tool_calls field into a list of
    {name: str, arguments: dict} dicts regardless of wire format version."""
    calls = []
    if not isinstance(raw, list):
        return calls
    for c in raw:
        if not isinstance(c, dict):
            continue
        # Ollama emits either {function: {name, arguments}} or {name, arguments}
        fn = c.get("function") if isinstance(c.get("function"), dict) else c
        name = fn.get("name") if isinstance(fn, dict) else None
        arguments = fn.get("arguments") if isinstance(fn, dict) else None
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except Exception:
                arguments = None
        if name and isinstance(arguments, dict):
            calls.append({"name": name, "arguments": arguments})
    return calls


def call_ollama(model: str, messages: list[dict], tools: list[dict],
                timeout: float = 120.0) -> dict:
    """Call the Ollama chat API with `tools`.

    Many tiny models do not support Ollama's structured `tools` parameter and
    reply with HTTP 400. In that case we transparently retry WITHOUT tools and
    rely on the system prompt to coax a JSON tool call from the model text
    output. This keeps the evaluation fair across tool-native and non-native
    models and surfaces the real tool-calling behavior of small models.

    Returns a dict with keys:
        content     - model text output (may be empty when a tool call is made)
        tool_calls  - list of {name, arguments} parsed from the API response
        latency_ms  - wall-clock time for the (successful) request
        error       - error string or "" on success
    """
    result = {"content": "", "tool_calls": [], "latency_ms": 0.0, "error": ""}

    def _post(use_tools: bool) -> dict:
        payload: dict = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.0},
        }
        if use_tools:
            payload["tools"] = tools
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return {"ok": True, "body": body, "ms": round((time.time() - t0) * 1000, 1), "err": ""}
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            return {"ok": False, "body": None, "ms": round((time.time() - t0) * 1000, 1),
                    "err": f"HTTP {e.code}: {detail[:300]}"}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "body": None, "ms": round((time.time() - t0) * 1000, 1),
                    "err": f"{type(e).__name__}: {e}"}

    r = _post(use_tools=True)
    # Detect "does not support tools" and retry without the tools parameter.
    if not r["ok"] and "does not support tools" in r["err"]:
        r = _post(use_tools=False)

    if not r["ok"]:
        result["latency_ms"] = r["ms"]
        result["error"] = r["err"]
        return result

    result["latency_ms"] = r["ms"]
    body = r["body"] or {}
    msg = body.get("message", {}) or {}
    result["content"] = msg.get("content", "") or ""
    result["tool_calls"] = _normalize_tool_calls(msg.get("tool_calls"))
    return result


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_dataset(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_messages(prompt: str, tool_names: list[str] | None = None) -> list[dict]:
    """Construct the chat messages for a single evaluation example.

    The system prompt instructs the model to emit a tool call as a single JSON
    object when a tool is required, and plain text otherwise. This works for
    both tool-native models and models that only produce free text.
    """
    names = ", ".join(tool_names) if tool_names else "the available tools"
    system = (
        "You are a helpful assistant. You have access to these tools: "
        f"{names}.\n"
        "If the user's request requires a tool, respond with EXACTLY ONE JSON "
        "object of the form {\"name\": <tool_name>, \"arguments\": {<args>}} and "
        "nothing else. If no tool is needed, reply in plain text and do NOT call "
        "any tool. Be concise and use the exact argument names from the tool "
        "definitions."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
