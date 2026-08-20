---
title: Multi-pass reliability (pass^k)
description: Why a single successful attempt doesn't mean a model is reliable, and how pass^k exposes the gap.
---

Most reported eval numbers answer "can the model do this at all." Multi-pass reliability answers a different, more production-relevant question: "can the model do this **every time**." The two questions produce very different numbers for the same model, and conflating them is one of the most common ways a tool-calling eval overstates how deployable a model is.

## The Problem With Single-Shot Numbers

A model that solves a task once has demonstrated it is *capable* of solving it. It has not demonstrated it will solve it *reliably* — the same task, asked again under identical conditions, can produce a different (wrong) tool call due to sampling variance, ambiguity the model resolves differently on different runs, or brittleness that only shows up some fraction of the time. A single-shot pass rate cannot distinguish a model that is consistently right 80% of the time from one that is right 100% of the time on 80% of tasks and unreliable on the rest — but those are very different systems to put into production.

## pass@k vs. pass^k

These two metrics sound similar and are frequently confused, but they measure close to opposite things:

- **pass@k** (common in code-generation evals like HumanEval) asks: out of *k* independent attempts, did **at least one** succeed? This is an *optimistic* metric — it rewards a model that can occasionally get lucky, and it's a reasonable metric when a human or system can pick the best of several generated candidates.
- **pass^k** (introduced by τ-bench) asks: out of *k* independent attempts at the identical task, did the model succeed on **every single one**? This is a *pessimistic*, consistency-focused metric — it directly penalizes flakiness, and it maps much more closely to a real deployment where an agent typically gets one shot per user request and can't retry until something works.

For a tool-calling agent, pass^k is the more honest metric, because production users don't get to silently retry a failed booking or a failed refund five times and keep only the attempt that worked.

## What the Degradation Looks Like

In the original τ-bench paper, GPT-4o's success rate on the retail domain fell substantially as the required number of consecutive successful trials increased from 1 to 8 — a model that looked reasonably capable at a single attempt revealed clear inconsistency once required to repeat that success ([τ-bench paper](https://arxiv.org/abs/2406.12045)). The size of that drop, not the single-shot number alone, is the more informative signal about whether the model is ready for unattended production use.

This isn't unique to frontier models or to τ-bench's domains. Subsequent log-analysis work examining τ-bench Airline runs found that a meaningful share of apparent agent failures on the original task set were actually caused by flawed or ambiguous task annotations rather than genuine model error — after correcting for that, average pass^5 across sampled models roughly doubled ([log analysis paper](https://arxiv.org/abs/2605.08545)). That's a useful caution in the other direction: before concluding a model is unreliable, check whether the eval's own task definitions are unambiguous and correctly graded — a "flaky model" result can sometimes be a flaky benchmark.

## Results From Our POC

We measured pass^k directly on our own tool-calling eval, using a 150-example dataset (hand-authored; harder than our original 34-example set, with 35 abstention cases and 35 adversarial edge cases) and two of our tiny Ollama models: **Qwen3 0.6B** (the strongest tool-caller in our suite) and **Qwen2.5 0.5B** (the weakest). Every example was run 8 times at temperature 0.7 with fixed seeds 1–8.

![pass^k degrades with k for both models](/images/passk-degradation.png)

| Model | pass^1 | pass^8 | drop | always right (8/8) | inconsistent (1–7/8) | always wrong (0/8) |
|-------|-------:|-------:|-----:|-------------------:|----------------------:|-------------------:|
| Qwen3 0.6B | 94% | 86% | **8pp** | 129 / 150 (86%) | 18 / 150 (12%) | 3 / 150 (2%) |
| Qwen2.5 0.5B | 81% | 69% | **12pp** | 104 / 150 (69%) | 24 / 150 (16%) | 22 / 150 (15%) |

![pass^1 vs pass^8, and the drop between them](/images/passk-gap.png)

Both models clear a single-shot bar that looks defensible, yet a meaningful share of tasks simply never work, and another share works only sometimes. The two models fail differently, and that difference is exactly what pass^k exists to expose:

- **Qwen3 0.6B is rarely wrong, occasionally flaky.** 86% of tasks are correct on all 8 attempts and only 2% fail every single time; its 8pp drop is almost entirely "inconsistent" tasks that it gets right most of the time but not reliably.
- **Qwen2.5 0.5B is both flaky *and* habitually wrong.** A fifth as many tasks (15%) are wrong on all 8 attempts, and its pass^8 collapse is driven by a single failure mode: **it calls a tool when it shouldn't**. On the 36 abstention examples (no tool needed), its accuracy is 44% on a single attempt and just **11% at pass^8** — only 4 of 36 questions were answered correctly all 8 times, because the model keeps confidently firing off irrelevant tool calls.

![Consistency taxonomy: always right vs inconsistent vs always wrong](/images/passk-failure-modes.png)

The per-tool breakdown reinforces that flakiness is not uniform. `set_timer` and `search_contacts` are near-perfect across both models at all k; `get_weather` and `send_message` both degrade, and `send_message` (two required args, `recipient` and `message`) is the flakiest single call Qwen3 0.6B makes: 90% → 72%.

![per-tool pass^1 vs pass^8](/images/passk-by-tool.png)

Three things stand out from this run. First, both models' single-shot numbers *look* production-ready ("94%!", "81%!") while pass^8 tells a different story, exactly the conflation this page warns about. Second, the gap between "always wrong" and "inconsistent" is actionable: Qwen3 0.6B's failures are mostly sampling brittleness (prompt or schema clarity work), while more than a third of Qwen2.5 0.5B's failures are a repeatable capability deficiency (it over-triggers tools — a refusal/abstain training gap, not a lucky sampling miss). Third, reporting by tool and by task type surfaces which specific calls belong in a deployment's retry path.

_Data & reproducibility: dataset and generator are `data/eval_dataset_large.jsonl` and `notebooks/gen_dataset_large.py`; raw multi-trial runs are in `results/raw_passk/`; pass^k computation lives in `evaluator/analyze_passk.py` and its outputs in `results/summary_passk/`; charts are generated by `notebooks/plot_pass_k.py`._

## Why This Matters More For Small Models

Small, on-device models are more likely to show meaningful pass^k degradation than frontier models, for a structural reason: constrained parameter counts make formatting, argument-typing, and tool-selection decisions more sensitive to small variations in phrasing or sampling. A tiny model might report a respectable pass^1 tool-selection accuracy while its pass^4 or pass^8 number tells a much less flattering story — and that gap is exactly the information a deployment decision needs. Reporting only a single-run number for a small model risks making it look more production-ready than it is.

## How To Add This To An Eval

- Run each test case *k* times (k=3 to k=8 is typical, budget permitting) with independent sampling — not the same seed repeated.
- Report pass^1 (single-shot), and at least one higher-k value, side by side, not just the higher one in isolation — the gap between them is the point.
- Keep temperature and other sampling settings fixed and documented, since pass^k results are only comparable across models run under matching sampling conditions.
- Where feasible, distinguish "model got it wrong every time" from "model got it wrong inconsistently" in your reporting — the two failure modes call for different follow-up (one suggests a capability gap, the other suggests a prompt or schema clarity problem).

On our POC run specifically: **k = 8, temperature 0.7, seeds 1–8**, 150 hand-authored examples, two models, all results in `results/`. One comparability trap worth flagging: our single-shot dashboard numbers are measured at temperature 0.0 (greedy), while pass^k *requires* nonzero sampling temperature to have any variance at all. So the pass^1 quoted in this section is the *temperature 0.7* pass^1, not the greedy baseline — mix those two sampling conditions up and you're no longer measuring the same system.

## References

- [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | Sierra Research & Princeton. Introduces pass^k. Verified 2026-08-20.
- [Log analysis is necessary for credible evaluation of AI agents](https://arxiv.org/abs/2605.08545) | τ-bench Airline log-analysis case study. Verified 2026-08-20.
