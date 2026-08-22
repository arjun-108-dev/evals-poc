"""Evaluate a single tiny model on tool-calling.

Usage:
    uv run python evaluator/run_eval.py --model gemma3-1b
    uv run python evaluator/run_eval.py --model qwen3-0.6b --limit 10
    uv run python evaluator/run_eval.py --model qwen3-0.6b --dataset data/eval_dataset_large.jsonl \
        --samples 8 --temperature 0.7
    uv run python evaluator/run_eval.py --model qwen3-0.6b --dataset data/eval_dataset_large.jsonl \
        --limit 10 --no-file   # print only, no CSV written

Outputs one detailed CSV per model. Single-shot runs write to
results/raw/<model_id>.csv; multi-trial (pass^k) runs write to
results/raw_passk/<model_id>.csv by default. Use --no-file to skip
writing any files and only print the per-case results to the terminal.
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
    "trial", "id", "prompt", "category", "difficulty",
    "expected_tool", "expected_args",
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


def run(model_id: str, limit: int | None, samples: int = 1,
        dataset_path: str | None = None, temperature: float = 0.0,
        out_dir: str | None = None, offset: int = 0,
        no_file: bool = False) -> str:
    # Resolve model config.
    models = utils.load_json(os.path.join(DATA, "models.json"))["models"]
    cfg = next((m for m in models if m["id"] == model_id), None)
    if cfg is None:
        raise SystemExit(f"Unknown model id '{model_id}'. Available: {[m['id'] for m in models]}")

    tag = cfg["ollama"]
    tools = utils.load_json(os.path.join(DATA, "tools.json"))["tools"]
    ds_path = dataset_path or os.path.join(DATA, "eval_dataset.jsonl")
    dataset = utils.load_dataset(ds_path)
    if limit:
        dataset = dataset[offset:offset + limit]
    elif offset:
        dataset = dataset[offset:]

    exe = utils.find_ollama()
    if not utils.ensure_server():
        raise SystemExit("Ollama server is not reachable. Start Ollama and try again.")
    if not _is_pulled(tag):
        if not utils.pull_model(tag, exe):
            raise SystemExit(f"Could not pull model '{tag}'. Skipping.")

    if out_dir:
        out_csv = os.path.join(out_dir, f"{cfg['id']}.csv")
    elif samples > 1:
        out_dir = os.path.join(ROOT, "results", "raw_passk")
        out_csv = os.path.join(out_dir, f"{cfg['id']}.csv")
    else:
        out_csv = os.path.join(ROOT, cfg["csv"])

    if not no_file:
        os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    n_calls = len(dataset) * samples
    print(f"\n=== Evaluating {cfg['name']} ({tag}) on {len(dataset)} examples x {samples} trial(s) "
          f"(temperature={temperature}) ===")
    print(f"    dataset: {ds_path}")
    print(f"    output : {out_csv if not no_file else '(none - no file written)'}")
    tool_names = [t["function"]["name"] for t in tools]
    rows = []
    for i, ex in enumerate(dataset, 1):
        messages = utils.build_messages(ex["prompt"], tool_names)
        for trial in range(1, samples + 1):
            seed = trial if samples > 1 else None
            resp = utils.call_ollama(tag, messages, tools,
                                     temperature=temperature, seed=seed)
            parsed_tool, parsed_args, found_call = parse_tool_call(resp["content"], resp["tool_calls"])
            g = grade(ex, parsed_tool, parsed_args, found_call)
            row = {
                "trial": trial,
                "id": ex["id"],
                "prompt": ex["prompt"],
                "category": ex.get("category", ""),
                "difficulty": ex.get("difficulty", ""),
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

            if ex["expected_tool"] == "none":
                expected_disp = "none (no tool needed)"
            elif ex["expected_args"]:
                expected_disp = (f"{ex['expected_tool']}("
                                 f"{json.dumps(ex['expected_args'], ensure_ascii=False)})")
            else:
                expected_disp = ex["expected_tool"]
            parsed_disp = g["parsed_tool"] or "(no tool call)"
            if g["parsed_args"]:
                parsed_disp = f"{g['parsed_tool']}({g['parsed_args']})"

            trial_tag = f" t{trial}/{samples}" if samples > 1 else ""
            print(f"\n  [{i:>3}/{len(dataset)}]{trial_tag} {ex['id']}  [{status}] "
                  f"{resp['latency_ms']:.0f}ms")
            print(f"    prompt  : {ex['prompt']}")
            print(f"    expected: {expected_disp}")
            print(f"    got     : {parsed_disp}")
            if resp["error"]:
                print(f"    error   : {resp['error']}")
            if g["tool_correct"] and not g["args_correct"]:
                print(f"    note    : right tool, wrong args")
            if g["false_positive"]:
                print(f"    note    : called a tool when none was needed")
            if not g["format_valid"]:
                print(f"    note    : malformed tool-call format")
            sys.stdout.flush()

    if not no_file:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            w.writeheader()
            w.writerows(rows)
        print(f"\nWrote {len(rows)} rows ({n_calls} API calls) -> {out_csv}")
    else:
        print(f"\nEvaluated {len(rows)} rows ({n_calls} API calls); no file written")
    return out_csv


def main():
    ap = argparse.ArgumentParser(description="Run tool-calling eval for one tiny model.")
    ap.add_argument("--model", required=True, help="Model id from data/models.json")
    ap.add_argument("--limit", type=int, default=None, help="Evaluate only the first N examples")
    ap.add_argument("--offset", type=int, default=0, help="Start evaluating at this example index")
    ap.add_argument("--samples", type=int, default=1,
                    help="Run each example this many times (pass^k). Requires temperature > 0.")
    ap.add_argument("--dataset", default=None,
                    help="Dataset JSONL path (default: data/eval_dataset.jsonl)")
    ap.add_argument("--temperature", type=float, default=0.0,
                    help="Sampling temperature. Use e.g. 0.7 for multi-trial reliability runs.")
    ap.add_argument("--out", default=None,
                    help="Output CSV directory. Defaults to results/raw_passk when --samples > 1.")
    ap.add_argument("--no-file", action="store_true",
                    help="Do not write any CSV; only print results to the terminal.")
    args = ap.parse_args()
    run(args.model, args.limit, args.samples, args.dataset, args.temperature, args.out,
        args.offset, args.no_file)


if __name__ == "__main__":
    main()
