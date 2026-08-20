"""Evaluate a single tiny model on tool-calling.

Usage:
    uv run python evaluator/run_eval.py --model gemma3-1b
    uv run python evaluator/run_eval.py --model qwen3-0.6b --limit 10

Outputs one detailed CSV per model at results/raw/<model_id>.csv.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys

# Make the evaluator package importable when run as a script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Windows consoles default to cp1252, which cannot encode Ollama's progress
# spinners / unicode model output. Force UTF-8 for all printed output.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

import utils  # noqa: E402
from graders import parse_tool_call, grade  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
RESULTS_RAW = os.path.join(ROOT, "results", "raw")

CSV_FIELDS = [
    "id", "prompt", "expected_tool", "expected_args",
    "model_output", "parsed_tool", "parsed_args",
    "tool_correct", "args_correct", "format_valid",
    "false_positive", "latency_ms", "error",
]


def _is_pulled(tag: str) -> bool:
    try:
        import json
        import urllib.request
        with urllib.request.urlopen(f"{utils.OLLAMA_HOST}/api/tags", timeout=5) as r:
            models = json.loads(r.read()).get("models", [])
        return any(m.get("name") == tag or m.get("name", "").startswith(tag + ":") for m in models)
    except Exception:
        return False


def run(model_id: str, limit: int | None) -> str:
    # Resolve model config.
    models = utils.load_json(os.path.join(DATA, "models.json"))["models"]
    cfg = next((m for m in models if m["id"] == model_id), None)
    if cfg is None:
        raise SystemExit(f"Unknown model id '{model_id}'. Available: {[m['id'] for m in models]}")

    tag = cfg["ollama"]
    tools = utils.load_json(os.path.join(DATA, "tools.json"))["tools"]
    dataset = utils.load_dataset(os.path.join(DATA, "eval_dataset.jsonl"))
    if limit:
        dataset = dataset[:limit]

    exe = utils.find_ollama()
    if not utils.ensure_server():
        raise SystemExit("Ollama server is not reachable. Start Ollama and try again.")
    if not _is_pulled(tag):
        if not utils.pull_model(tag, exe):
            raise SystemExit(f"Could not pull model '{tag}'. Skipping.")

    out_csv = os.path.join(ROOT, cfg["csv"])
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    print(f"\n=== Evaluating {cfg['name']} ({tag}) on {len(dataset)} examples ===")
    tool_names = [t["function"]["name"] for t in tools]
    rows = []
    for i, ex in enumerate(dataset, 1):
        messages = utils.build_messages(ex["prompt"], tool_names)
        resp = utils.call_ollama(tag, messages, tools)
        parsed_tool, parsed_args, found_call = parse_tool_call(resp["content"], resp["tool_calls"])
        g = grade(ex, parsed_tool, parsed_args, found_call)
        row = {
            "id": ex["id"],
            "prompt": ex["prompt"],
            "expected_tool": ex["expected_tool"],
            "expected_args": json.dumps(ex["expected_args"], ensure_ascii=False) if ex["expected_args"] is not None else "",
            "model_output": resp["content"],
            "parsed_tool": g["parsed_tool"],
            "parsed_args": g["parsed_args"],
            "tool_correct": g["tool_correct"],
            "args_correct": g["args_correct"],
            "format_valid": g["format_valid"],
            "false_positive": g["false_positive"],
            "latency_ms": resp["latency_ms"],
            "error": resp["error"],
        }
        rows.append(row)
        status = "OK" if g["tool_correct"] else ("FP" if g["false_positive"] else "MISS")
        print(f"  [{i:2d}/{len(dataset)}] {ex['id']} -> {g['parsed_tool'] or '(none)':<14} [{status}] {resp['latency_ms']:.0f}ms")
        # Flush incrementally so long runs show progress.
        sys.stdout.flush()

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {out_csv}")
    return out_csv


def main():
    ap = argparse.ArgumentParser(description="Run tool-calling eval for one tiny model.")
    ap.add_argument("--model", required=True, help="Model id from data/models.json")
    ap.add_argument("--limit", type=int, default=None, help="Evaluate only the first N examples")
    args = ap.parse_args()
    run(args.model, args.limit)


if __name__ == "__main__":
    main()
