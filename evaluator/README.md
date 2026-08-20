# Evaluator

The Python harness at the heart of the [evals POC](../README.md). Runs evaluations against small open-weight models served locally by Ollama, grades every response **deterministically**, and aggregates the raw runs into metrics and failure reports. No LLM-as-judge, no synthetic results — every number comes from real model runs.

## Pipelines

There are three evaluation pipelines, each split into a *run* script and an *analyze* script:

| Pipeline | Run | Analyze | Outputs to |
|----------|-----|---------|------------|
| **Tool-calling** | `run_eval.py` | `analyze.py` | `results/raw/`, `results/summary/` |
| **Math reasoning** | `run_math_eval.py` | `analyze_math.py` | `results/raw_math/`, `results/summary_math/` |
| **Pass^k reliability** | `run_eval.py --samples N` | `analyze_passk.py` | `results/raw_passk/`, `results/summary_passk/` |

### Tool-calling

Given a prompt like *"Set a timer for 10 minutes to take the pizza out of the oven"*, the model must pick the right tool (`get_weather`, `set_timer`, `send_message`, `search_contacts`), supply the right arguments, and abstain when no tool is needed. Responses are parsed with layered heuristics (`graders.py`) and compared against the expected `(tool, args)` pair — strict-but-fair normalization for numbers (tolerance) and strings (case/whitespace), out-of-order keys tolerated, extra keys ignored. A multi-trial mode (`--samples N`, `--temperature 0.7`) measures **pass^k** reliability.

### Math

Arithmetic, word problems, fractions/percent, and simple algebra across easy/medium/hard difficulty. A final answer is extracted from free-form reasoning (`math_graders.py`) using layered patterns (`Answer: N`, "the answer is N", trailing numbers, fractions) and compared numerically with a small tolerance. Two failure modes are tracked separately: **could we parse a number?** (`answer_parsed`) and **was it correct?** (`answer_correct`).

## Usage

Requires [uv](https://docs.astral.sh/uv/) and a running [Ollama](https://ollama.dev) server. Pure standard library at eval time — no third-party hard dependencies.

```bash
# Single-shot tool-calling eval (default temperature 0.0)
uv run python evaluator/run_eval.py --model qwen3-0.6b
uv run python evaluator/run_eval.py --model qwen3-0.6b --dataset data/eval_dataset_large.jsonl --limit 10

# Math eval
uv run python evaluator/run_math_eval.py --model gemma3:1b

# Pass^k reliability (8 trials per example)
uv run python evaluator/run_eval.py --model qwen3-0.6b --samples 8 --temperature 0.7

# Aggregate everything + sync data into the frontend dashboard
uv run python evaluator/analyze.py
uv run python evaluator/analyze_math.py
uv run python evaluator/analyze_passk.py
```

Model ids come from `data/models.json` (e.g. `functiongemma-270m`, `gemma3-1b`, `qwen3-0.6b`, `qwen2.5-0.5b`, `qwen2.5-1.5b`).

## Outputs

Analyze scripts write:

- `metrics.csv` — one row per model with the headline metrics and overall score.
- `failures.md` — a ranked summary plus per-model failure modes (false positives, wrong tool, right tool/wrong args, malformed calls, unparsed/wrong answers).

Both are synced into `frontend/public/data/` so the dashboard can render everything statically. See the [root README](../README.md) for the full pipeline and the [docs site](https://evals-poc.arjun-90c.workers.dev/) for the methodology write-up.

## Scoring

- **Tool** overall = `0.45·call_acc + 0.25·arg_acc + 0.20·abstain_acc + 0.10·format_validity`.
- **Math** overall = `0.75·accuracy + 0.25·parse_rate`.
- **Pass^k** = fraction of examples correct on **all** of the first `k` trials (with `always_right` / `inconsistent` / `always_wrong` failure-mode buckets).