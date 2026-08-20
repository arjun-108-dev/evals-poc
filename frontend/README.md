# Eval Dashboard

The React frontend for the [evals POC](../README.md). A static, data-driven dashboard that visualizes the results of running tool-calling and math evals against small open-weight models — the models, every score, and the raw run data.

Live at **https://evals.arjun-90c.workers.dev/**

## What It Does

- **Tool-Calling tab** — per-model metrics (call accuracy, argument accuracy, abstention rate, false positives, format validity, overall score), a trade-off scatter (accuracy vs. latency), a metric comparison table/radar, and a per-model drill-down that shows every prompt, what tool the model chose, and whether it was graded correct.
- **Math tab** — accuracy, parse rate, and overall scores across categories (arithmetic, word problems, fractions/percent, algebra), heatmaps by category × difficulty, outcome breakdowns, and a per-model view of every question with the extracted answer.
- **Overview / Per-model** views for both evals, all selectable from the header.

Everything is computed **deterministically** from real model outputs and served as static JSON/CSV — there is no backend and no LLM-as-judge.

## Stack

React 19 · Vite 8 · TypeScript · Tailwind v4 · shadcn/ui (`@base-ui/react`) · Recharts

## Local Dev

The dashboard loads its data from `public/data/`, which is populated by the evaluator's analysis scripts. Make sure the data is up to date first:

```bash
cd .. && uv run python evaluator/analyze.py
cd .. && uv run python evaluator/analyze_math.py
cd .. && uv run python evaluator/analyze_passk.py
```

Then start the dev server:

```bash
pnpm install
pnpm dev        # Vite dev server (HMR)
```

| Command | Action |
|---------|--------|
| `pnpm dev` | Start local dev server |
| `pnpm build` | Type-check + production build to `dist/` |
| `pnpm preview` | Preview the production build |
| `pnpm lint` | Oxlint |

## Data Layout

`public/data/` mirrors the repo's `data/` and `results/` directories once the analysis scripts have run:

```
public/data/
├── models.json              # the evaluated models (name, size, color, notes)
├── tools.json               # tool schemas used in the tool-calling eval
├── eval_dataset.jsonl       # tool-calling prompt dataset
├── math_dataset.jsonl       # math question dataset
└── results/
    ├── raw/                 # per-model tool-calling runs (CSV)
    ├── raw_math/            # per-model math runs (CSV)
    ├── raw_passk/           # per-model pass^k trial runs (CSV)
    ├── summary/             # aggregated tool metrics + failures.md
    ├── summary_math/        # aggregated math metrics + failures.md
    └── summary_passk/       # pass^k curves, model + per-item summaries, failures.md
```