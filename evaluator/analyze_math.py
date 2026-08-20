"""Aggregate math evaluation results into metrics and a report.

Reads every CSV in results/raw_math/, computes per-model metrics, writes:
    results/summary_math/metrics.csv
    results/summary_math/failures.md
It also synchronizes the data + results into frontend/public/data so the
React frontend can load everything statically (no backend).

Usage:
    uv run python evaluator/analyze_math.py
    uv run python evaluator/analyze_math.py --no-sync
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
RAW = os.path.join(ROOT, "results", "raw_math")
SUMMARY = os.path.join(ROOT, "results", "summary_math")
FRONTEND_DATA = os.path.join(ROOT, "frontend", "public", "data")


def sync_frontend():
    """Copy data + results into frontend/public/data for static serving."""
    os.makedirs(FRONTEND_DATA, exist_ok=True)
    # data files
    for fn in ["models.json", "math_dataset.jsonl"]:
        shutil.copy2(os.path.join(DATA, fn), os.path.join(FRONTEND_DATA, fn))
    # results tree
    dst_raw = os.path.join(FRONTEND_DATA, "results", "raw_math")
    dst_sum = os.path.join(FRONTEND_DATA, "results", "summary_math")
    os.makedirs(dst_raw, exist_ok=True)
    os.makedirs(dst_sum, exist_ok=True)
    for fn in os.listdir(RAW):
        if fn.endswith(".csv"):
            shutil.copy2(os.path.join(RAW, fn), os.path.join(dst_raw, fn))
    for fn in ["metrics.csv", "failures.md"]:
        src = os.path.join(SUMMARY, fn)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dst_sum, fn))
    print(f"[sync] copied math data + results -> {FRONTEND_DATA}")


def _b(v: str) -> bool:
    return str(v).strip().lower() == "true"


def read_rows(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_metrics(model_id: str, name: str, size: str, color: str,
                    rows: list[dict]) -> dict:
    n = len(rows)
    parsed = sum(1 for r in rows if _b(r["answer_parsed"]))
    correct = sum(1 for r in rows if _b(r["answer_correct"]))
    lats = [float(r["latency_ms"]) for r in rows if r["latency_ms"]]

    accuracy = correct / n if n else 0.0
    parse_rate = parsed / n if n else 0.0
    # Overall blends raw accuracy with extraction success so a model that
    # fails to emit any number can't hide behind a low-n subset.
    overall = 0.75 * accuracy + 0.25 * parse_rate
    avg_lat = sum(lats) / len(lats) if lats else 0.0

    return {
        "model_id": model_id,
        "name": name,
        "size": size,
        "color": color,
        "n_examples": n,
        "n_parsed": parsed,
        "n_correct": correct,
        "accuracy": round(accuracy, 4),
        "parse_rate": round(parse_rate, 4),
        "overall_score": round(overall, 4),
        "avg_latency_ms": round(avg_lat, 1),
    }


def category_breakdown(rows: list[dict]) -> dict[str, dict]:
    cats: dict[str, dict] = {}
    for r in rows:
        c = r.get("category", "unknown")
        d = cats.setdefault(c, {"n": 0, "correct": 0})
        d["n"] += 1
        if _b(r["answer_correct"]):
            d["correct"] += 1
    return {c: {"n": v["n"], "acc": round(v["correct"] / v["n"], 4) if v["n"] else 0.0}
            for c, v in cats.items()}


def write_metrics_csv(metrics: list[dict], path: str):
    fields = [
        "model_id", "name", "size", "color",
        "n_examples", "n_parsed", "n_correct",
        "accuracy", "parse_rate", "overall_score", "avg_latency_ms",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(metrics)


def write_failures_md(metrics: list[dict], per_model_rows: dict[str, list[dict]],
                      models_meta: dict[str, dict], path: str):
    lines = ["# Math Evaluation: Failures & Notable Cases", ""]
    lines.append("Generated automatically by `evaluator/analyze_math.py`. All results below are "
                 "from **real** model runs via Ollama (no synthetic data).")
    lines.append("")

    lines.append("## Model ranking (by overall score)")
    lines.append("")
    lines.append("| Rank | Model | Size | Accuracy | Parse Rate | Overall | Avg ms |")
    lines.append("|------|-------|------|---------:|-----------:|--------:|--------:|")
    ranked = sorted(metrics, key=lambda m: m["overall_score"], reverse=True)
    for i, m in enumerate(ranked, 1):
        lines.append(
            f"| {i} | {m['name']} | {m['size']} | "
            f"{m['accuracy']*100:.0f}% | {m['parse_rate']*100:.0f}% | "
            f"{m['overall_score']:.3f} | {m['avg_latency_ms']:.0f} |"
        )
    lines.append("")

    for m in ranked:
        mid = m["model_id"]
        rows = per_model_rows.get(mid, [])
        wrong = [r for r in rows if not _b(r["answer_correct"])]
        noparse = [r for r in rows if not _b(r["answer_parsed"])]
        cats = category_breakdown(rows)

        lines.append(f"## {m['name']} ({m['size']})")
        if models_meta.get(mid, {}).get("notes"):
            lines.append(f"_{models_meta[mid]['notes']}_")
        lines.append("")
        lines.append(f"- Accuracy: **{m['accuracy']*100:.0f}%** "
                     f"({m['n_correct']}/{m['n_examples']})")
        lines.append(f"- Parse rate: **{m['parse_rate']*100:.0f}%** "
                     f"({m['n_parsed']}/{m['n_examples']})")
        lines.append(f"- Accuracy by category: " +
                     ", ".join(f"{c}={v['acc']*100:.0f}% (n={v['n']})" for c, v in sorted(cats.items())))
        lines.append("")

        if noparse:
            lines.append(f"### No answer extracted ({len(noparse)})")
            for r in noparse[:12]:
                lines.append(f"- **{r['id']}** exp={r['expected_answer']}: {r['model_output'][:120]!r}")
            if len(noparse) > 12:
                lines.append(f"- ...and {len(noparse)-12} more.")
            lines.append("")

        if wrong:
            parsed_wrong = [r for r in wrong if _b(r["answer_parsed"])]
            lines.append(f"### Wrong answers ({len(parsed_wrong)})")
            for r in parsed_wrong[:12]:
                lines.append(f"- **{r['id']}** ({r['question'][:60]}) "
                             f"expected {r['expected_answer']} → got {r['extracted_answer']}")
            if len(parsed_wrong) > 12:
                lines.append(f"- ...and {len(parsed_wrong)-12} more.")
            lines.append("")

        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-sync", action="store_true", help="Skip copying files to frontend/public/data")
    args = ap.parse_args()

    models = json.load(open(os.path.join(DATA, "models.json"), encoding="utf-8"))["models"]
    meta = {m["id"]: m for m in models}

    csv_files = [f for f in os.listdir(RAW) if f.endswith(".csv")]
    if not csv_files:
        raise SystemExit(f"No result CSVs found in {RAW}. Run run_math_eval.py first.")

    metrics: list[dict] = []
    per_model_rows: dict[str, list[dict]] = {}
    for fn in sorted(csv_files):
        mid = fn[:-4]
        if mid not in meta:
            print(f"[warn] {fn} has no entry in models.json; skipping")
            continue
        rows = read_rows(os.path.join(RAW, fn))
        per_model_rows[mid] = rows
        m = meta[mid]
        metrics.append(compute_metrics(mid, m["name"], m["size"], m["color"], rows))

    metrics.sort(key=lambda x: [m["id"] for m in models].index(x["model_id"]))

    os.makedirs(SUMMARY, exist_ok=True)
    write_metrics_csv(metrics, os.path.join(SUMMARY, "metrics.csv"))
    write_failures_md(metrics, per_model_rows, meta, os.path.join(SUMMARY, "failures.md"))
    print(f"[analyze_math] wrote metrics.csv and failures.md for {len(metrics)} models")
    if not args.no_sync:
        sync_frontend()


if __name__ == "__main__":
    main()
