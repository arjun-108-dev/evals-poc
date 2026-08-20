"""Deterministic graders for tool-calling evaluation.

The core metrics are computed without any LLM-as-judge: we parse the model
output into a (tool, arguments) pair and compare it against the expected
values with strict-but-fair normalization.
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional

# Numeric tolerance for argument comparison (helps with int vs float noise).
NUMERIC_TOLERANCE = 1e-6


def _norm_string(s: Any) -> str:
    """Normalize a string for lenient comparison."""
    if s is None:
        return ""
    return re.sub(r"\s+", " ", str(s).strip().lower())


def _looks_like_call_attempt(text: str) -> bool:
    """Heuristic: does the text look like the model *tried* to emit a tool call
    but in a broken format? Used to flag format_valid=False."""
    t = text or ""
    if re.search(r"\{[^{}]*\"(name|function)\"", t):
        return True
    if re.search(r"\w+\s*\(\s*[\"\']?\w+[\"\']?\s*[:=]", t):
        return True
    return False


def parse_tool_call(raw_text: str, api_tool_calls: list[dict]) -> tuple[str, Optional[dict], bool]:
    """Extract a (tool_name, arguments, found_call) triple from model output.

    Priority:
      1. Structured tool_calls returned by the Ollama API (most reliable).
      2. Free-text JSON / function syntax emitted inline by the model.

    `found_call` is True only when we recovered a tool name together with a
    dict of arguments.
    """
    # 1) API-provided structured calls.
    if api_tool_calls:
        c = api_tool_calls[0]
        return c.get("name", ""), c.get("arguments"), True

    text = (raw_text or "").strip()
    if not text:
        return "", None, False

    # Strip markdown code fences.
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    candidate = fenced.group(1).strip() if fenced else text

    # 2a) Try to parse the whole candidate as JSON.
    parsed = None
    try:
        parsed = json.loads(candidate)
    except Exception:
        # 2b) Extract the first {...} block and try again.
        m = re.search(r"\{.*\}", candidate, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(0))
            except Exception:
                parsed = None

    if isinstance(parsed, dict):
        name, args = _name_and_args_from_json(parsed)
        if name:
            return name, (args if isinstance(args, dict) else {}), True

    # 2b.5) FunctionGemma's own protocol, e.g.
    #   call:set_timer{duration_minutes:10,label: pizza}<end_function_call>
    #   model:get_weather{}<end_function_call>
    #   return: {"name": "get_weather", "arguments": {"location": "Tokyo"}}
    fg = _parse_functiongemma(candidate)
    if fg[0]:
        return fg

    # 2c) Function-call syntax: name({json}) or name(key="val", ...)
    m = re.search(r"(\w+)\s*\((?P<body>.*)\)\s*$", candidate, re.DOTALL)
    if m:
        name = m.group(1)
        body = m.group("body").strip()
        args: dict[str, Any] = {}
        # JSON object body?
        if body.startswith("{") or body.startswith('"'):
            try:
                inner = json.loads(body)
                if isinstance(inner, dict):
                    return name, inner, True
                if isinstance(inner, str):
                    # name("paris") -> assume first param
                    args = {"value": inner}
                    return name, args, True
            except Exception:
                pass
        # key=value pairs
        for kv in re.findall(r'(\w+)\s*=\s*("(?:[^"]*)"|\'(?:[^\']*)\'|[^,\)]+)', body):
            k = kv[0]
            v = kv[1].strip().strip('"').strip("'")
            args[k] = _coerce(v)
        if args:
            return name, args, True
        # name() with empty body -> still a call attempt
        return name, {}, True

    return "", None, False


def _parse_functiongemma(text: str) -> tuple[str, Optional[dict], bool]:
    """Parse FunctionGemma's custom tool-call protocol from free text.

    Supports:
      call:<name>{<body>}<end_function_call>
      model:<name>{<body>}<end_function_call>
      return: {"name": <name>, "arguments": {<args>}}
    where <body> may be JSON or simple key:value pairs (values unquoted).
    """
    # JSON return form first.
    m = re.search(r"return\s*:\s*(\{.*\})", text, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict):
                name, args = _name_and_args_from_json(obj)
                if name:
                    return name, (args if isinstance(args, dict) else {}), True
        except Exception:
            pass

    # call:/model: form.
    m = re.search(r"(?:call|model)\s*:\s*(\w+)\s*\{(.*?)\}<end_function_call>", text, re.DOTALL)
    if m:
        name = m.group(1)
        body = m.group(2).strip()
        args: dict[str, Any] = {}
        if body:
            try:
                parsed = json.loads(body)
                if isinstance(parsed, dict):
                    return name, parsed, True
            except Exception:
                pass
            # key:value pairs (values may be unquoted / contain spaces).
            for kv in re.findall(r"(\w+)\s*:\s*([^,}<]+)", body):
                args[kv[0]] = _coerce(kv[1].strip())
        return name, args, True
    return "", None, False


def _name_and_args_from_json(obj: dict) -> tuple[Optional[str], Any]:
    """Pull (name, arguments) out of common JSON shapes small models emit."""
    # {"name": "x", "arguments": {...}}
    if "name" in obj and ("arguments" in obj or "parameters" in obj):
        args = obj.get("arguments", obj.get("parameters"))
        return obj["name"], args
    # {"function": {"name": "x", "arguments": {...}}}
    fn = obj.get("function")
    if isinstance(fn, dict) and "name" in fn:
        return fn["name"], fn.get("arguments")
    # Bare {tool_name: {args}} or {tool_name: value}
    if len(obj) == 1:
        k, v = next(iter(obj.items()))
        if isinstance(v, dict):
            return k, v
    return None, None


def _coerce(v: str) -> Any:
    try:
        return int(v)
    except Exception:
        pass
    try:
        return float(v)
    except Exception:
        return v


def _args_match(parsed: Optional[dict], expected: Optional[dict]) -> bool:
    """Strict-but-fair argument comparison.

    - All expected keys must be present (case-insensitive).
    - Numeric values compared with tolerance.
    - String values compared after normalization (equality or containment).
    - Extra keys in `parsed` are ignored (fair to the model).
    """
    if expected is None:
        return True
    if not isinstance(parsed, dict):
        return False
    parsed_lower = {str(k).lower(): v for k, v in parsed.items()}
    for key, exp_val in expected.items():
        if key.lower() not in parsed_lower:
            return False
        got = parsed_lower[key.lower()]
        if isinstance(exp_val, (int, float)) and not isinstance(exp_val, bool):
            try:
                if abs(float(got) - float(exp_val)) > NUMERIC_TOLERANCE:
                    return False
            except Exception:
                return False
        else:
            g, e = _norm_string(got), _norm_string(exp_val)
            if not (g == e or e in g or g in e):
                return False
    return True


def grade(example: dict, parsed_tool: str, parsed_args: Optional[dict],
          found_call: bool) -> dict:
    """Grade a single example. Returns the grading flags for the CSV row."""
    expected_tool = example.get("expected_tool", "none")
    expected_args = example.get("expected_args")

    if expected_tool == "none":
        false_positive = found_call
        tool_correct = not found_call
        args_correct = not found_call
    else:
        false_positive = False
        tool_correct = found_call and parsed_tool == expected_tool
        args_correct = bool(tool_correct) and _args_match(parsed_args, expected_args)

    # format_valid: a tool call attempt must be well-formed; abstentions are fine.
    if found_call:
        format_valid = isinstance(parsed_args, dict)
    else:
        format_valid = True

    return {
        "parsed_tool": parsed_tool or "",
        "parsed_args": json.dumps(parsed_args, ensure_ascii=False) if isinstance(parsed_args, dict) else "",
        "tool_correct": tool_correct,
        "args_correct": args_correct,
        "format_valid": format_valid,
        "false_positive": false_positive,
    }
