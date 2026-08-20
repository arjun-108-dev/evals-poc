"""Aggregate multi-trial (pass^k) reliability results into metrics and a report.

Reads every CSV in results/raw_passk/, computes pass^k consistency metrics,
and writes:
    results/summary_passk/passk_curves.csv   - long format (model, k, passk)
    results/summary_passk/model_summary.csv  - per-model pass^1/pass^8 + failure modes
    results/summary_passk/per_item.csv       - per-item consistency for charting
    results/summary_passk/failures.md        - human-readable reliability report
It also synchronizes the results into frontend/public/data.

Usage:
    uv run python evaluator/analyze_passk.py
    uv run python evaluator/analyze_passk.py --no-sync
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
RAW = os.path.join(ROOT, "results", "raw_passk")
SUMMARY = os.path.join(ROOT, "results", "summary_passk")
FRONTEND_DATA = os.path.join(ROOT, "frontend", "public", "data")


def _b(v: str) -> bool:
    return str(v).strip().lower() == "true"


def read_rows(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_passk(model_id: str, meta: dict, rows: list[dict]) -> dict:
    """Group rows by example id + trial, compute pass^k and failure modes."""
    if not rows:
        raise SystemExit(f"  [warn] {model_id} has no rows in {RAW}")

    # (example_id) -> [(trial, tool_correct, category, difficulty, tool)]
    by_ex: dict[str, dict] = {}
    for r in rows:
        ex = by_ex.setdefault(r["id"], {
            "trials": [], "category": r.get("category", ""),
            "difficulty": r.get("difficulty", ""),
            "tool": r.get("expected_tool", ""),
        })
        ex["trials"].append((int(r["trial"]), _b(r["tool_correct"])))

    n = len(by_ex)
    K = max(t for ex in by_ex.values() for t, _ in ex["trials"])

    def _sorted_corrects(ex):
        return [ok for _, ok in sorted(ex["trials"])]

    # pass^k: fraction of examples correct on ALL of the first k trials.
    passk: list[float] = []
    for k in range(1, K + 1):
        ok = sum(1 for ex in by_ex.values()
                 if all(_sorted_corrects(ex)[:k]))
        passk.append(ok / n if n else 0.0)

    # Failure modes over all K trials.
    always_right = [exid for exid, ex in by_ex.items() if sum(_sorted_corrects(ex)) == K]
    always_wrong = [exid for exid, ex in by_ex.items() if sum(_sorted_corrects(ex)) == 0]
    inconsistent = [exid for exid, ex in by_ex.items()
                    if 0 < sum(_sorted_corrects(ex)) < K]

    # Single-trial accuracy averaged across all trials (robust pass^1 estimate).
    all_oks = [ok for ex in by_ex.values() for ok in _sorted_corrects(ex)]
    avg_single = sum(all_oks) / len(all_oks) if all_oks else 0.0

    lats = [float(r["latency_ms"]) for r in rows if r.get("latency_ms")]
    avg_lat = sum(lats) / len(lats) if lats else 0.0

    return {
        "model_id": model_id,
        "name": meta["name"],
        "size": meta["size"],
        "color": meta["color"],
        "n_examples": n,
        "K": K,
        "pass1": passk[0],
        "pass8": passk[-1] if passk else 0.0,
        "passk": passk,
        "avg_single_trial": avg_single,
        "n_always_right": len(always_right),
        "n_inconsistent": len(inconsistent),
        "n_always_wrong": len(always_wrong),
        "avg_latency_ms": round(avg_lat, 1),
        "always_right": always_right,
        "inconsistent": inconsistent,
        "always_wrong": always_wrong,
        "by_ex": by_ex,
    }


def write_curves_csv(results: list[dict], path: str):
    fields = ["model_id", "name", "size", "color", "k", "passk"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for m in results:
            for k, p in enumerate(m["passk"], 1):
                w.writerow({"model_id": m["model_id"], "name": m["name"],
                            "size": m["size"], "color": m["color"],
                            "k": k, "passk": round(p, 4)})


def write_model_summary(results: list[dict], path: str):
    fields = ["model_id", "name", "size", "color",
              "n_examples", "K",
              "pass1", "pass8", "drop",
              "avg_single_trial",
              "n_always_right", "n_inconsistent", "n_always_wrong",
              "avg_latency_ms"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for m in results:
            w.writerow({
                "model_id": m["model_id"], "name": m["name"], "size": m["size"],
                "color": m["color"], "n_examples": m["n_examples"], "K": m["K"],
                "pass1": round(m["pass1"], 4), "pass8": round(m["pass8"], 4),
                "drop": round(m["pass1"] - m["pass8"], 4),
                "avg_single_trial": round(m["avg_single_trial"], 4),
                "n_always_right": m["n_always_right"],
                "n_inconsistent": m["n_inconsistent"],
                "n_always_wrong": m["n_always_wrong"],
                "avg_latency_ms": m["avg_latency_ms"],
            })


def write_per_item(results: list[dict], path: str):
    fields = ["model_id", "id", "expected_tool", "category", "difficulty",
              "trials_correct", "failure_mode"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for m in results:
            for exid in sorted(m["by_ex"].keys()):
                ex = m["by_ex"][exid]
                corrects = sorted(ex["trials"])
                n_ok = sum(ok for _, ok in corrects)
                mode = ("always_right" if n_ok == m["K"]
                        else "always_wrong" if n_ok == 0 else "inconsistent")
                w.writerow({
                    "model_id": m["model_id"], "id": exid,
                    "expected_tool": ex["tool"], "category": ex["category"],
                    "difficulty": ex["difficulty"],
                    "trials_correct": n_ok, "failure_mode": mode,
                })


def write_failures_md(results: list[dict], path: str):
    lines = ["# Pass^k Reliability Failures", ""]
    lines.append("Generated automatically by `evaluator/analyze_passk.py`. All results below are "
                 "from **real** model runs via Ollama (no synthetic data).")
    lines.append("")

    ranked = sorted(results, key=lambda m: m["pass8"], reverse=True)
    lines.append("## Model ranking (by pass^K)")
    lines.append("")
    lines.append("| Model | Size | pass^1 | pass^K | drop | always right | inconsistent | always wrong |")
    lines.append("|-------|------|-------:|------:|-----:|-------------:|-------------:|-------------:|")
    for m in ranked:
        lines.append(f"| {m['name']} | {m['size']} | "
                     f"{m['pass1']*100:.0f}% | {m['pass8']*100:.0f}% | "
                     f"{(m['pass1']-m['pass8'])*100:.0f}pp | "
                     f"{m['n_always_right']} | {m['n_inconsistent']} | {m['n_always_wrong']} |")
    lines.append("")

    for m in ranked:
        lines.append(f"## {m['name']} ({m['size']})")
        lines.append("")
        lines.append(f"- **pass^1**: {m['pass1']*100:.1f}%   "
                     f"**pass^K** (K={m['K']}): {m['pass8']*100:.1f}%   "
                     f"drop: {(m['pass1']-m['pass8'])*100:.1f}pp")
        lines.append(f"- Consistent (always right): **{m['n_always_right']}/{m['n_examples']}** "
                     f"({m['n_always_right']/m['n_examples']*100:.0f}%)")
        lines.append(f"- Inconsistent (right on some trials): **{m['n_inconsistent']}/{m['n_examples']}**")
        lines.append(f"- Incapable / always wrong: **{m['n_always_wrong']}/{m['n_examples']}** "
                     f"({m['n_always_wrong']/m['n_examples']*100:.0f}%)")
        lines.append("")

        if m["always_wrong"]:
            rows_aw = sorted(m["always_wrong"])
            lines.append(f"### Always wrong ({len(rows_aw)}) - failed all {m['K']} trials")
            for exid in rows_aw:
                ex = m["by_ex"][exid]
                lines.append(f"- **{exid}** `{ex['tool']}` ({ex['category']}/{ex['difficulty']})")
            lines.append("")

        if m["inconsistent"]:
            rows_in = sorted(m["inconsistent"])
            lines.append(f"### Inconsistent ({len(rows_in)}) - right on some, wrong on some trials")
            for exid in rows_in:
                ex = m["by_ex"][exid]
                n_ok = sum(ok for _, ok in sorted(ex["trials"]))
                lines.append(f"- **{exid}** `{ex['tool']}` ({ex['category']}/{ex['difficulty']}): "
                             f"{n_ok}/{m['K']} trials correct")
            lines.append("")

        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def sync_frontend():
    os.makedirs(FRONTEND_DATA, exist_ok=True)
    dst_raw = os.path.join(FRONTEND_DATA, "results", "raw_passk")
    dst_sum = os.path.join(FRONTEND_DATA, "results", "summary_passk")
    os.makedirs(dst_raw, exist_ok=True)
    os.makedirs(dst_sum, exist_ok=True)
    if os.path.isdir(RAW):
        for fn in os.listdir(RAW):
            if fn.endswith(".csv"):
                shutil.copy2(os.path.join(RAW, fn), os.path.join(dst_raw, fn))
    for fn in ["passk_curves.csv", "model_summary.csv", "per_item.csv", "failures.md"]:
        src = os.path.join(SUMMARY, fn)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dst_sum, fn))
    print(f"[sync] copied pass^k results -> {FRONTEND_DATA}")


def main():
    ap = argparse.ArgumentParser(description="Aggregate pass^k reliability results.")
    ap.add_argument("--no-sync", action="store_true", help="Skip copying to frontend")
    args = ap.parse_args()

    models = json.load(open(os.path.join(DATA, "models.json"), encoding="utf-8"))["models"]
    meta = {m["id"]: m for m in models}

    if not os.path.isdir(RAW):
        raise SystemExit(f"No results dir {RAW}. Run run_eval.py --samples N first.")

    csv_files = [f for f in os.listdir(RAW) if f.endswith(".csv")]
    if not csv_files:
        raise SystemExit(f"No result CSVs found in {RAW}.")

    results = []
    for fn in sorted(csv_files):
        mid = fn[:-4]
        if mid not in meta:
            print(f"[warn] {fn} has no entry in models.json; skipping")
            continue
        rows = read_rows(os.path.join(RAW, fn))
        print(f"[passk] {mid}: {len(rows)} rows, trials=1..{max(int(r['trial']) for r in rows)}")
        results.append(compute_passk(mid, meta[mid], rows))

    results.sort(key=lambda x: [m["id"] for m in models].index(x["model_id"]))

    os.makedirs(SUMMARY, exist_ok=True)
    write_curves_csv(results, os.path.join(SUMMARY, "passk_curves.csv"))
    write_model_summary(results, os.path.join(SUMMARY, "model_summary.csv"))
    write_per_item(results, os.path.join(SUMMARY, "per_item.csv"))
    write_failures_md(results, os.path.join(SUMMARY, "failures.md"))

    print(f"[analyze] wrote pass^k metrics for {len(results)} models")
    for m in results:
        print(f"  {m['name']:<18} pass^1={m['pass1']*100:.1f}%  "
              f"pass^{m['K']}={m['pass8']*100:.1f}%  "
              f"drop={(m['pass1']-m['pass8'])*100:.1f}pp")

    if not args.no_sync:
        sync_frontend()


if __name__ == "__main__":
    main()