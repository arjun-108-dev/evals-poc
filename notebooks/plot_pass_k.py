"""Generate pass^k reliability charts for the docs site.

Reads results/summary_passk/*.csv (and results/raw_passk/*.csv for the per-tool
breakdown), renders 4 charts into docs-site/public/images/:

    1. passk-degradation.png  - pass^k vs k, one line per model (temp 0.7, k=1..8)
    2. passk-gap.png          - pass^1 vs pass^8 grouped bars, annotated drop
    3. passk-failure-modes.png- 100% stacked bar: always right / inconsistent / always wrong
    4. passk-by-tool.png      - pass^1 vs pass^8 per expected tool, one panel per model

Usage:
    uv run python notebooks/plot_pass_k.py
"""
from __future__ import annotations

import os
import sys

# notebooks/inspect.py shadows the stdlib `inspect` module that matplotlib
# needs at import time. Drop the script dir from sys.path so stdlib wins.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path
            if os.path.abspath(p) != os.path.abspath(_SCRIPT_DIR)]

import csv
import json
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMMARY = os.path.join(ROOT, "results", "summary_passk")
RAW = os.path.join(ROOT, "results", "raw_passk")
DATA = os.path.join(ROOT, "data")
OUT_DIR = os.path.join(ROOT, "docs-site", "public", "images")

K = 8
DPI = 160
MODEL_ORDER = ["qwen3-0.6b", "qwen2.5-0.5b"]


def load_summary(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_raw(model: str) -> list[dict]:
    with open(os.path.join(RAW, f"{model}.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _b(v: str) -> bool:
    return str(v).strip().lower() == "true"


def tool_pass1_pass8(model: str) -> dict[str, tuple[float, float]]:
    """pass^1 (trial 1) and pass^8 (all trials) per expected tool from raw rows."""
    rows = read_raw(model)
    by_ex: dict[str, list[tuple[int, bool, str]]] = defaultdict(list)
    for r in rows:
        by_ex[r["id"]].append((int(r["trial"]), _b(r["tool_correct"]), r["expected_tool"]))
    per_tool: dict[str, list[bool]] = defaultdict(list)  # tool -> list of trial1 outcomes
    all8: dict[str, list[bool]] = defaultdict(list)      # tool -> all-8-correct outcomes
    for exid, trials in by_ex.items():
        trials.sort()
        tool = trials[0][2]
        okay = [ok for _, ok, _ in trials]
        per_tool[tool].append(okay[0])
        all8[tool].append(all(okay))
    out = {}
    for tool in set(list(per_tool) + list(all8)):
        p1 = sum(per_tool[tool]) / len(per_tool[tool])
        p8 = sum(all8[tool]) / len(all8[tool])
        out[tool] = (p1, p8)
    return out


def chart_degradation(curves: list[dict], out_path: str):
    plt.figure(figsize=(8, 4.8))
    for m in load_summary(os.path.join(SUMMARY, "model_summary.csv")):
        color = m["color"]
        name = m["name"]
        pts = [float(r["passk"]) for r in curves if r["model_id"] == m["model_id"]]
        if not pts:
            continue
        label = f"{name}: pass^1 {pts[0]*100:.0f}% -> pass^8 {pts[-1]*100:.0f}%"
        plt.plot(range(1, len(pts) + 1), [p * 100 for p in pts],
                 marker="o", label=label, color=color, linewidth=2.2, markersize=5)
        plt.text(len(pts), pts[-1] * 100, f"  pass^8\n  {pts[-1]*100:.0f}%",
                 ha="left", va="center", color=color, fontsize=9, fontweight="bold")
    plt.xlabel("k (consecutive successful trials required)")
    plt.ylabel("pass^k (all k trials correct, %)")
    plt.title("Tool-calling reliability degrades as k increases\n"
              "(150 examples, temperature 0.7, seeds 1-8)", fontsize=11)
    plt.ylim(55, 100)
    plt.yticks(range(55, 101, 5))
    plt.xticks(range(1, K + 1))
    plt.grid(axis="y", linestyle=":", alpha=0.5)
    plt.legend(loc="lower left", fontsize=9, framealpha=0.9)
    plt.tight_layout()
    plt.savefig(out_path, dpi=DPI)
    plt.close()
    print("wrote", out_path)


def chart_gap(model_summary: list[dict], out_path: str):
    plt.figure(figsize=(8, 4.8))
    names = [m["name"] for m in model_summary]
    p1 = [float(m["pass1"]) * 100 for m in model_summary]
    p8 = [float(m["pass8"]) * 100 for m in model_summary]
    cols = [m["color"] for m in model_summary]
    x = range(len(names))
    w = 0.36
    b1 = plt.bar([i - w / 2 for i in x], p1, width=w, color=[c for c in cols],
                 label="pass^1  (a single attempt)", alpha=0.95, edgecolor="white")
    b8 = plt.bar([i + w / 2 for i in x], p8, width=w, color=[c for c in cols],
                 hatch="//", alpha=0.45, label="pass^8  (all 8 attempts)", edgecolor="white")
    for r in list(b1) + list(b8):
        plt.text(r.get_x() + r.get_width() / 2, r.get_height() + 1,
                 f"{r.get_height():.0f}%", ha="center", va="bottom", fontsize=9)
    for i, m in enumerate(model_summary):
        drop = float(m["pass1"]) * 100 - float(m["pass8"]) * 100
        plt.text(i, max(p1[i], p8[i]) + 8, f"-{drop:.0f}pp", ha="center", fontsize=10,
                 fontweight="bold", color="#B91C1C")
    plt.ylim(0, 112)
    plt.ylabel("success rate (%)")
    plt.xticks(list(x), names)
    plt.title("The pass^1-to-pass^8 gap: one-shot looks fine, reliability drops",
              fontsize=11)
    plt.grid(axis="y", linestyle=":", alpha=0.5)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(out_path, dpi=DPI)
    plt.close()
    print("wrote", out_path)


def chart_failure_modes(model_summary: list[dict], out_path: str):
    plt.figure(figsize=(8, 4.4))
    names = [m["name"] for m in model_summary]
    ar = [int(m["n_always_right"]) for m in model_summary]
    inc = [int(m["n_inconsistent"]) for m in model_summary]
    aw = [int(m["n_always_wrong"]) for m in model_summary]
    cols = [m["color"] for m in model_summary]
    x = range(len(names))
    bottom = [0] * len(names)
    b = plt.bar(x, ar, bottom=bottom, color=cols, alpha=0.9, edgecolor="white",
                label="always right (8/8)")
    bottom = ar
    plt.bar(x, inc, bottom=bottom, color="#F59E0B", alpha=0.9, edgecolor="white",
            label="inconsistent (1-7/8)")
    bottom = [a + i for a, i in zip(ar, inc)]
    plt.bar(x, aw, bottom=bottom, color="#DC2626", alpha=0.9, edgecolor="white",
            label="always wrong (0/8)")
    for i, m in enumerate(model_summary):
        n = float(m["n_examples"])
        plt.text(i, int(m["n_always_right"]) / 2,
                 f"{int(m['n_always_right'])/n*100:.0f}%",
                 ha="center", va="center", color="white", fontsize=10, fontweight="bold")
        plt.text(i, int(m["n_always_right"]) + int(m["n_inconsistent"]) / 2,
                 f"{int(m['n_inconsistent'])/n*100:.0f}%", ha="center", va="center",
                 color="white", fontsize=10, fontweight="bold")
        plt.text(i, n - int(m["n_always_wrong"]) / 2,
                 f"{int(m['n_always_wrong'])/n*100:.0f}%",
                 ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    plt.ylabel("examples of 150")
    plt.xticks(list(x), names)
    plt.ylim(0, 160)
    plt.title("Reliability taxonomy: consistent vs flaky vs incapable", fontsize=11)
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(out_path, dpi=DPI)
    plt.close()
    print("wrote", out_path)


def chart_by_tool(out_path: str):
    models = [m for m in load_summary(os.path.join(SUMMARY, "model_summary.csv"))
              if m["model_id"] in MODEL_ORDER]
    tools = ["get_weather", "set_timer", "send_message", "search_contacts"]
    short = {"get_weather": "get_weather", "set_timer": "set_timer",
             "send_message": "send_message", "search_contacts": "search_contacts"}
    n = len(models)
    fig, axes = plt.subplots(1, n, figsize=(11, 4.2), sharey=True)
    if n == 1:
        axes = [axes]
    w = 0.36
    for ax, m in zip(axes, models):
        data = tool_pass1_pass8(m["model_id"])
        p1 = [data[t][0] * 100 for t in tools]
        p8 = [data[t][1] * 100 for t in tools]
        x = range(len(tools))
        ax.bar([i - w / 2 for i in x], p1, width=w, color=m["color"], alpha=0.9,
               edgecolor="white", label="pass^1")
        ax.bar([i + w / 2 for i in x], p8, width=w, color=m["color"], alpha=0.35,
               hatch="//", edgecolor="white", label="pass^8")
        ax.set_title(f"{m['name']}", fontsize=11)
        ax.set_xticks(list(x))
        ax.set_xticklabels([short[t] for t in tools], rotation=20, ha="right", fontsize=8)
        ax.set_ylim(0, 110)
        ax.grid(axis="y", linestyle=":", alpha=0.5)
        ax.legend(fontsize=8)
    fig.suptitle("Flakiness varies by tool: pass^1 vs pass^8 per expected tool", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out_path, dpi=DPI)
    plt.close(fig)
    print("wrote", out_path)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    curves = load_summary(os.path.join(SUMMARY, "passk_curves.csv"))
    model_summary = load_summary(os.path.join(SUMMARY, "model_summary.csv"))

    chart_degradation(curves, os.path.join(OUT_DIR, "passk-degradation.png"))
    chart_gap(model_summary, os.path.join(OUT_DIR, "passk-gap.png"))
    chart_failure_modes(model_summary, os.path.join(OUT_DIR, "passk-failure-modes.png"))
    chart_by_tool(os.path.join(OUT_DIR, "passk-by-tool.png"))
    print("done. charts in", OUT_DIR)


if __name__ == "__main__":
    main()