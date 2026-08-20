"""Evaluate a single tiny model on basic math reasoning.

Usage:
    uv run python evaluator/run_math_eval.py --model gemma3:1b
    uv run python evaluator/run_math_eval.py --model qwen3:0.6b --limit 10

Outputs one detailed CSV per model at results/raw_math/<model_id>.csv.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

import utils  # noqa: E402
from math_graders import extract_answer, grade  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
RESULTS_RAW = os.path.join(ROOT, "results", "raw_math")

CSV_FIELDS = [
    "id", "question", "category", "difficulty", "expected_answer",
    "model_output", "extracted_answer",
    "answer_parsed", "answer_correct",
    "latency_ms", "error",
]

SYSTEM_PROMPT = (
    "You are a careful math assistant. Solve the problem step by step, then "
    "finish your response with a single line containing ONLY the numeric "
    "answer, like: Answer: 42\n"
    "If the answer is a fraction, give it as a decimal (e.g. 0.5 not 1/2)."
)


def _is_pulled(tag: str) -> bool:
    try:
        import urllib.request
        with urllib.request.urlopen(f"{utils.OLLAMA_HOST}/api/tags", timeout=5) as r:
            models = json.loads(r.read()).get("models", [])
        return any(m.get("name") == tag or m.get("name", "").startswith(tag + ":") for m in models)
    except Exception:
        return False


def run(model_id: str, limit: int | None) -> str:
    models = utils.load_json(os.path.join(DATA, "models.json"))["models"]
    cfg = next((m for m in models if m["id"] == model_id), None)
    if cfg is None:
        raise SystemExit(f"Unknown model id '{model_id}'. Available: {[m['id'] for m in models]}")

    tag = cfg["ollama"]
    dataset = utils.load_dataset(os.path.join(DATA, "math_dataset.jsonl"))
    if limit:
        dataset = dataset[:limit]

    exe = utils.find_ollama()
    if not utils.ensure_server():
        raise SystemExit("Ollama server is not reachable. Start Ollama and try again.")
    if not _is_pulled(tag):
        if not utils.pull_model(tag, exe):
            raise SystemExit(f"Could not pull model '{tag}'. Skipping.")

    out_csv = os.path.join(ROOT, f"results/raw_math/{cfg['id']}.csv")
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    print(f"\n=== Math eval: {cfg['name']} ({tag}) on {len(dataset)} examples ===")
    rows = []
    for i, ex in enumerate(dataset, 1):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": ex["question"]},
        ]
        resp = utils.call_ollama(tag, messages, tools=[])
        extracted = extract_answer(resp["content"])
        g = grade(ex, extracted)
        row = {
            "id": ex["id"],
            "question": ex["question"],
            "category": ex.get("category", ""),
            "difficulty": ex.get("difficulty", ""),
            "expected_answer": ex["answer"],
            "model_output": resp["content"],
            "extracted_answer": g["extracted_answer"] if g["answer_parsed"] else "",
            "answer_parsed": g["answer_parsed"],
            "answer_correct": g["answer_correct"],
            "latency_ms": resp["latency_ms"],
            "error": resp["error"],
        }
        rows.append(row)
        status = "OK" if g["answer_correct"] else ("PARSED" if g["answer_parsed"] else "NOPARSE")
        print(f"  [{i:2d}/{len(dataset)}] {ex['id']} exp={ex['answer']:<6} got={g['extracted_answer']} [{status}] {resp['latency_ms']:.0f}ms")
        sys.stdout.flush()

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {out_csv}")
    return out_csv


def main():
    ap = argparse.ArgumentParser(description="Run math eval for one tiny model.")
    ap.add_argument("--model", required=True, help="Model id from data/models.json")
    ap.add_argument("--limit", type=int, default=None, help="Evaluate only the first N examples")
    args = ap.parse_args()
    run(args.model, args.limit)


if __name__ == "__main__":
    main()
