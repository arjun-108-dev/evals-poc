# Evals POC

A proof-of-concept for **LLM evaluation**. This repo ships a full evaluation loop — dataset generation, a deterministic Python harness that runs evals on **small open-weight models** via Ollama, an analysis pipeline that computes scores, and two deployed sites to present the work.

## Live Sites

| Site | What it is | URL |
|------|-----------|-----|
| **Eval Dashboard** | React dashboard showing the models, the math + tool-calling eval scores, and the per-run data | https://evals.arjun-90c.workers.dev/ |
| **Docs Site** | A sourced field guide to model evaluation ("A Field Guide to LLM Evaluation") | https://evals-poc.arjun-90c.workers.dev/ |

## What's Here

```
.
├── data/          # Datasets (JSONL) + model metadata & tool schemas
├── evaluator/     # Python harness: run evals, grade deterministically, aggregate metrics
├── notebooks/     # Dataset generators + run inspection & plotting scripts
├── results/       # Raw per-model CSVs + aggregated metrics/failure reports
├── frontend/      # React + Vite + shadcn dashboard that visualizes the results
└── docs-site/     # Astro + Starlight docs site (the LLM eval field guide)
```

## The Evaluations

Two eval suites were run against five tiny open-weight models served locally with Ollama:

**Tool-calling** — given a prompt like *"Set a timer for 10 minutes to take the pizza out of the oven"*, can the model pick the right tool (`get_weather`, `set_timer`, `send_message`, `search_contacts`), supply the right arguments, and — just as important — abstain when no tool is needed? Graded **deterministically** (parsing + strict-but-fair comparison, no LLM-as-judge). A classic pass@k variant repeats runs across trials to measure reliability.

**Math reasoning** — arithmetic, word problems, fractions/percent, and simple algebra across easy/medium/hard difficulty, with answers extracted from free-form responses and compared numerically with a small tolerance.

**Models evaluated:** FunctionGemma 270M, Gemma 3 1B, Qwen3 0.6B, Qwen2.5 0.5B, Qwen2.5 1.5B.

Every number on the dashboard comes from real model runs — no synthetic results, and no LLM grading. The full methodology is captured in the [docs site](https://evals-poc.arjun-90c.workers.dev/).

## Running the Pipeline

Requires [uv](https://docs.astral.sh/uv/) and a running [Ollama](https://ollama.dev) server.

```bash
# 1. Generate datasets (optional — checked in)
uv run python notebooks/gen_dataset.py
uv run python notebooks/gen_math_dataset.py

# 2. Run an eval for a model (see data/models.json for ids)
uv run python evaluator/run_eval.py --model qwen3-0.6b
uv run python evaluator/run_math_eval.py --model qwen2.5-1.5b

# 3. Multi-trial reliability (pass^k)
uv run python evaluator/run_eval.py --model qwen3-0.6b --samples 8 --temperature 0.7

# 4. Aggregate metrics + sync data into the frontend
uv run python evaluator/analyze.py
uv run python evaluator/analyze_math.py
uv run python evaluator/analyze_passk.py
```

Analyzed outputs land in `results/summary/`, `results/summary_math/`, and `results/summary_passk/` and are copied into `frontend/public/data/` so the dashboard can render them statically (no backend).

### Running the sites locally

```bash
# Dashboard (Vite)
cd frontend && pnpm install && pnpm dev

# Docs site (Astro)
cd docs-site && pnpm install && pnpm dev
```

## Project Layout

| Path | Purpose |
|------|---------|
| `data/models.json` | The five evaluated models, their Ollama tags, colors, and notes |
| `data/tools.json` | The OpenAPI-style tool schemas used in the tool-calling eval |
| `data/*.jsonl` | The eval datasets (curated + large tool-calling sets, math set) |
| `evaluator/run_eval.py` | Runs one tool-calling eval for one model → `results/raw/` |
| `evaluator/run_math_eval.py` | Runs the math eval → `results/raw_math/` |
| `evaluator/graders.py` | Deterministic tool-calling parser + grader |
| `evaluator/math_graders.py` | Answer extractor + numeric grader |
| `evaluator/analyze*.py` | Aggregates raw CSVs into metrics + failure markdown reports |
| `notebooks/gen_*.py` | Dataset generators; `plot_pass_k.py` for reliability charts |
| `results/` | Raw CSVs and aggregated metrics/failure reports |
| `frontend/` | React dashboard for browsing scores, models, and run data |
| `docs-site/` | Astro/Starlight docs site — the LLM eval field guide |

## Why This Exists

This is a lightweight proof-of-concept that end-to-end evals don't require a heavy stack: a tiny locally-served model, a handful of hand-written probes, deterministic grading, and a static dashboard are enough to surface real differences in model behavior — useful signal for anyone starting to think about evaluating their own LLM apps.