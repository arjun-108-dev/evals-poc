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

## Why This Matters More For Small Models

Small, on-device models are more likely to show meaningful pass^k degradation than frontier models, for a structural reason: constrained parameter counts make formatting, argument-typing, and tool-selection decisions more sensitive to small variations in phrasing or sampling. A tiny model might report a respectable pass^1 tool-selection accuracy while its pass^4 or pass^8 number tells a much less flattering story — and that gap is exactly the information a deployment decision needs. Reporting only a single-run number for a small model risks making it look more production-ready than it is.

## How To Add This To An Eval

- Run each test case *k* times (k=3 to k=8 is typical, budget permitting) with independent sampling — not the same seed repeated.
- Report pass^1 (single-shot), and at least one higher-k value, side by side, not just the higher one in isolation — the gap between them is the point.
- Keep temperature and other sampling settings fixed and documented, since pass^k results are only comparable across models run under matching sampling conditions.
- Where feasible, distinguish "model got it wrong every time" from "model got it wrong inconsistently" in your reporting — the two failure modes call for different follow-up (one suggests a capability gap, the other suggests a prompt or schema clarity problem).

## References

- [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | Sierra Research & Princeton. Introduces pass^k. Verified 2026-08-20.
- [Log analysis is necessary for credible evaluation of AI agents](https://arxiv.org/abs/2605.08545) | τ-bench Airline log-analysis case study. Verified 2026-08-20.
