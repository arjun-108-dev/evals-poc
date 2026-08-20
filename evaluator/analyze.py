"""Aggregate evaluation results into metrics and an analysis report.

Reads every CSV in results/raw/, computes per-model metrics, writes:
    results/summary/metrics.csv
    results/summary/failures.md
It also synchronizes the data + results into frontend/public/data so the
React frontend can load everything statically (no backend).

Usage:
    uv run python evaluator/analyze.py
    uv run python evaluator/analyze.py --no-sync
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
RAW = os.path.join(ROOT, "results", "raw")
SUMMARY = os.path.join(ROOT, "results", "summary")
FRONTEND_DATA = os.path.join(ROOT, "frontend", "public", "data")


def _b(v: str) -> bool:
    return str(v).strip().lower() == "true"


def read_rows(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_metrics(model_id: str, name: str, size: str, color: str,
                    rows: list[dict]) -> dict:
    n = len(rows)
    should_call = [r for r in rows if r["expected_tool"] != "none"]
    should_not = [r for r in rows if r["expected_tool"] == "none"]

    tool_correct = sum(1 for r in rows if _b(r["tool_correct"]))
    call_correct = sum(1 for r in should_call if _b(r["tool_correct"]))
    arg_correct = sum(1 for r in should_call if _b(r["args_correct"]))
    format_valid = sum(1 for r in rows if _b(r["format_valid"]))
    false_pos = sum(1 for r in should_not if _b(r["false_positive"]))
    lats = [float(r["latency_ms"]) for r in rows if r["latency_ms"]]

    # Decision accuracy over ALL examples (correct call OR correct abstention).
    tool_acc = tool_correct / n if n else 0.0
    # Ability to pick the right tool WHEN one is needed.
    call_acc = call_correct / len(should_call) if should_call else 0.0
    # Argument extraction fidelity (only meaningful when a tool was needed).
    arg_acc = arg_correct / len(should_call) if should_call else 0.0
    # Ability to correctly abstain when no tool is needed (1 - FPR).
    abstain_acc = 1 - (false_pos / len(should_not)) if should_not else 1.0
    fmt = format_valid / n if n else 0.0
    fpr = false_pos / len(should_not) if should_not else 0.0
    # Overall: tool selection when needed (45%) + arg fidelity (25%) +
    # correct abstention (20%) + format validity (10%).
    overall = 0.45 * call_acc + 0.25 * arg_acc + 0.20 * abstain_acc + 0.10 * fmt
    avg_lat = sum(lats) / len(lats) if lats else 0.0

    return {
        "model_id": model_id,
        "name": name,
        "size": size,
        "color": color,
        "n_examples": n,
        "n_should_call": len(should_call),
        "n_should_not_call": len(should_not),
        "tool_accuracy": round(tool_acc, 4),
        "call_accuracy": round(call_acc, 4),
        "arg_accuracy": round(arg_acc, 4),
        "abstain_accuracy": round(abstain_acc, 4),
        "format_validity": round(fmt, 4),
        "false_positive_rate": round(fpr, 4),
        "overall_score": round(overall, 4),
        "avg_latency_ms": round(avg_lat, 1),
        "n_tool_correct": tool_correct,
        "n_call_correct": call_correct,
        "n_arg_correct": arg_correct,
        "n_false_positive": false_pos,
    }


def category_breakdown(rows: list[dict]) -> dict[str, dict]:
    cats: dict[str, dict] = {}
    for r in rows:
        c = r.get("category", "unknown")
        d = cats.setdefault(c, {"n": 0, "correct": 0})
        d["n"] += 1
        if _b(r["tool_correct"]):
            d["correct"] += 1
    return {c: {"n": v["n"], "acc": round(v["correct"] / v["n"], 4) if v["n"] else 0.0}
            for c, v in cats.items()}


def write_metrics_csv(metrics: list[dict], path: str):
    fields = [
        "model_id", "name", "size", "color",
        "n_examples", "n_should_call", "n_should_not_call",
        "tool_accuracy", "call_accuracy", "arg_accuracy",
        "abstain_accuracy", "format_validity", "false_positive_rate",
        "overall_score", "avg_latency_ms",
        "n_tool_correct", "n_call_correct", "n_arg_correct", "n_false_positive",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(metrics)


def write_failures_md(metrics: list[dict], per_model_rows: dict[str, list[dict]],
                      models_meta: dict[str, dict], path: str):
    lines = ["# Evaluation Failures & Notable Cases", ""]
    lines.append("Generated automatically by `evaluator/analyze.py`. All results below are "
                 "from **real** model runs via Ollama (no synthetic data).")
    lines.append("")

    # Ranked summary table.
    lines.append("## Model ranking (by overall score)")
    lines.append("")
    lines.append("| Rank | Model | Size | Call Acc | Arg Acc | Abstain | FPR | Overall | Avg ms |")
    lines.append("|------|-------|------|---------:|--------:|--------:|----:|--------:|--------:|")
    ranked = sorted(metrics, key=lambda m: m["overall_score"], reverse=True)
    for i, m in enumerate(ranked, 1):
        lines.append(
            f"| {i} | {m['name']} | {m['size']} | "
            f"{m['call_accuracy']*100:.0f}% | {m['arg_accuracy']*100:.0f}% | "
            f"{m['abstain_accuracy']*100:.0f}% | "
            f"{m['false_positive_rate']*100:.0f}% | {m['overall_score']:.3f} | "
            f"{m['avg_latency_ms']:.0f} |"
        )
    lines.append("")

    for m in ranked:
        mid = m["model_id"]
        rows = per_model_rows.get(mid, [])
        should_not = [r for r in rows if r["expected_tool"] == "none"]
        fps = [r for r in should_not if _b(r["false_positive"])]
        mism = [r for r in rows if r["expected_tool"] != "none"
                and not _b(r["tool_correct"]) and not _b(r["false_positive"])]
        argmiss = [r for r in rows if r["expected_tool"] != "none"
                   and _b(r["tool_correct"]) and not _b(r["args_correct"])]
        fmtbad = [r for r in rows if not _b(r["format_valid"])]
        cats = category_breakdown(rows)

        lines.append(f"## {m['name']} ({m['size']})")
        if models_meta.get(mid, {}).get("notes"):
            lines.append(f"_{models_meta[mid]['notes']}_")
        lines.append("")
        lines.append(f"- Tool accuracy: **{m['tool_accuracy']*100:.0f}%** "
                     f"({m['n_tool_correct']}/{m['n_should_call']+m['n_should_not_call']})")
        lines.append(f"- Argument accuracy: **{m['arg_accuracy']*100:.0f}%** "
                     f"({m['n_arg_correct']}/{m['n_should_call']})")
        lines.append(f"- False positive rate: **{m['false_positive_rate']*100:.0f}%** "
                     f"({m['n_false_positive']}/{m['n_should_not_call']})")
        lines.append(f"- Accuracy by category: " +
                     ", ".join(f"{c}={v['acc']*100:.0f}% (n={v['n']})" for c, v in sorted(cats.items())))
        lines.append("")

        if fps:
            lines.append(f"### False positives ({len(fps)}) - called a tool when none was needed")
            for r in fps:
                lines.append(f"- **{r['id']}** ({r['prompt'][:60]}) "
                             f"→ called `{r['parsed_tool'] or '(unknown)'}` "
                             f"args={r['parsed_args'] or '{}'}")
            lines.append("")

        if mism:
            lines.append(f"### Wrong / missing tool ({len(mism)})")
            for r in mism[:12]:
                lines.append(f"- **{r['id']}** expected `{r['expected_tool']}` "
                             f"→ got `{r['parsed_tool'] or '(none)'}` "
                             f"(prompt: {r['prompt'][:50]})")
            if len(mism) > 12:
                lines.append(f"- ...and {len(mism)-12} more.")
            lines.append("")

        if argmiss:
            lines.append(f"### Right tool, wrong args ({len(argmiss)})")
            for r in argmiss[:12]:
                lines.append(f"- **{r['id']}** `{r['expected_tool']}`: "
                             f"expected {r['expected_args']} → got {r['parsed_args'] or '{}'}")
            if len(argmiss) > 12:
                lines.append(f"- ...and {len(argmiss)-12} more.")
            lines.append("")

        if fmtbad:
            lines.append(f"### Malformed tool calls ({len(fmtbad)})")
            for r in fmtbad[:8]:
                lines.append(f"- **{r['id']}**: {r['model_output'][:120]!r}")
            lines.append("")

        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def sync_frontend():
    """Copy data + results into frontend/public/data for static serving."""
    os.makedirs(FRONTEND_DATA, exist_ok=True)
    # data files
    for fn in ["models.json", "tools.json", "eval_dataset.jsonl"]:
        shutil.copy2(os.path.join(DATA, fn), os.path.join(FRONTEND_DATA, fn))
    # results tree
    dst_raw = os.path.join(FRONTEND_DATA, "results", "raw")
    dst_sum = os.path.join(FRONTEND_DATA, "results", "summary")
    os.makedirs(dst_raw, exist_ok=True)
    os.makedirs(dst_sum, exist_ok=True)
    for fn in os.listdir(RAW):
        if fn.endswith(".csv"):
            shutil.copy2(os.path.join(RAW, fn), os.path.join(dst_raw, fn))
    for fn in ["metrics.csv", "failures.md"]:
        src = os.path.join(SUMMARY, fn)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dst_sum, fn))
    print(f"[sync] copied data + results -> {FRONTEND_DATA}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-sync", action="store_true", help="Skip copying files to frontend/public/data")
    args = ap.parse_args()

    models = json.load(open(os.path.join(DATA, "models.json"), encoding="utf-8"))["models"]
    meta = {m["id"]: m for m in models}

    csv_files = [f for f in os.listdir(RAW) if f.endswith(".csv")]
    if not csv_files:
        raise SystemExit(f"No result CSVs found in {RAW}. Run run_eval.py first.")

    metrics: list[dict] = []
    per_model_rows: dict[str, list[dict]] = {}
    for fn in sorted(csv_files):
        mid = fn[:-4]  # strip .csv
        if mid not in meta:
            print(f"[warn] {fn} has no entry in models.json; skipping")
            continue
        rows = read_rows(os.path.join(RAW, fn))
        per_model_rows[mid] = rows
        m = meta[mid]
        metrics.append(compute_metrics(mid, m["name"], m["size"], m["color"], rows))

    # Stable order: by model list order.
    metrics.sort(key=lambda x: [m["id"] for m in models].index(x["model_id"]))

    os.makedirs(SUMMARY, exist_ok=True)
    write_metrics_csv(metrics, os.path.join(SUMMARY, "metrics.csv"))
    write_failures_md(metrics, per_model_rows, meta, os.path.join(SUMMARY, "failures.md"))

    print(f"[analyze] wrote metrics.csv and failures.md for {len(metrics)} models")
    if not args.no_sync:
        sync_frontend()


if __name__ == "__main__":
    main()
