---
title: Tool use & agentic evaluation
description: How to evaluate whether a model can select, call, and sequence external tools correctly.
---

Tool use (also called function calling) is a model's ability to turn a natural-language request into a valid call to an external function, API, or tool. It is the capability this guide's companion POC dashboard measures directly, so treat this page as the bridge between the general concepts above and that dashboard.

Unlike most of the ten types on this site, correctness here is structural, not semantic: an answer is either a syntactically and semantically valid call against a known schema or it is not. That makes tool-use eval closer to program correctness checking than to open-ended judgment, which is also why it typically needs its own metrics rather than reusing accuracy or a judge score.

## Why It's a Distinct Eval Type

A model can be fluent and well-aligned and still fail at tool use in ways that don't show up on knowledge or reasoning benchmarks: picking the wrong function among several similar ones, hallucinating a parameter name, passing a string where the schema wants an integer, calling a tool when it should have asked a clarifying question instead, or forgetting a tool call it made two turns ago. None of this is captured by MMLU-style accuracy or by a chat-quality judge, which is why dedicated tool-use benchmarks emerged as their own category once agentic products moved past single-turn chat.

## What These Evals Measure

Most tool-use benchmarks decompose the problem into a few checks, usually applied per call:

- **Function selection** — did the model choose the correct tool from the set offered (or correctly decline to call any tool)?
- **Argument correctness** — are the parameter names, types, and values right, including required vs. optional fields?
- **Executability** — does the generated call actually run and, where checked, produce the correct output when executed against a real or simulated backend?
- **Ordering and parallelism** — for tasks needing more than one call, are calls sequenced or parallelized correctly, including dependencies where one call's output feeds another's input?
- **Multi-turn state tracking** — across a longer conversation, does the model keep track of what has already been called, what the environment now looks like, and what still needs to happen?
- **Policy adherence** — in agentic customer-service style tasks, does the model follow written business rules (e.g. refund limits) while completing the user's goal, not just complete the goal?

## Benchmarks

| Benchmark | What it tests | Verified source |
|---|---|---|
| Berkeley Function-Calling Leaderboard (BFCL) | Single, multiple, and parallel function calls across Python/Java/JavaScript/REST, using Abstract Syntax Tree (AST) matching plus an executable track; later versions add multi-turn, multi-step, and agentic settings | [BFCL paper](https://openreview.net/forum?id=2GmDdhBdDk); [Gorilla project](https://gorilla.cs.berkeley.edu/leaderboard.html) |
| τ-bench / τ²-bench | Multi-turn, tool-using agents against simulated users in retail, airline, and (in τ²) telecom domains, graded on final database state against an annotated goal, not the transcript | [τ-bench paper](https://arxiv.org/abs/2406.12045); [tau2-bench repo](https://github.com/sierra-research/tau2-bench) |
| API-Bank | Runnable evaluation across 73 APIs and 314 annotated tool-use dialogues, scoring planning, retrieval, and calling ability separately | [API-Bank paper](https://arxiv.org/abs/2304.08244) |
| ToolBench / StableToolBench | Large-scale (16k+ real APIs) tool-use benchmark; StableToolBench adds a cached virtual API layer so scores don't drift as real third-party APIs change or go offline | [StableToolBench paper](https://arxiv.org/abs/2403.07714) |
| AgentBench | Broader agentic evaluation across multiple environments (not tool-calling-only), useful as a comparison point for how tool use fits into general agent capability | [AgentBench paper](https://arxiv.org/abs/2308.03688) |

## Key Methodology Notes

**AST matching vs. execution.** BFCL's core method parses the generated call into an abstract syntax tree and compares it against the reference call's structure, which scales to thousands of functions without needing to actually run anything; its executable track additionally runs a subset of calls for ground truth. Know which mode a reported number comes from — AST-only scores can look stronger than a model's real-world executable success rate.

**pass^k, not pass@k.** τ-bench's headline metric requires a model to succeed on every one of *k* independent trials of the same task, not just the best of *k* attempts. The gap between the two is large: in the original paper, GPT-4o's retail score fell from roughly 60% at a single trial to close to 25% once required to succeed on all 8 trials, which best-of-k scoring would have hidden entirely. For any tool-calling eval you build, report a repeat-trial number, not just a single-shot pass rate — one lucky call sequence is not the same as a reliable one.

**Outcome grading over transcript grading.** τ-bench and its successors score success by diffing the final environment/database state against an annotated goal state, rather than pattern-matching the conversation. This avoids over-rewarding a model that "talks" like it solved the task without actually calling the tools that would have changed the state.

**Live and adversarial splits matter.** BFCL's live category uses user-contributed, less curated functions rather than only expert-written ones, and later analysis found that small paraphrases of otherwise-identical queries can drop top-model accuracy by double digits. A benchmark built only from clean, hand-written examples will systematically overstate real-world reliability — mirror this by including some deliberately messy or ambiguous tool schemas in your own eval set.

**Cost is part of the result.** Because tool-calling agents often run many turns per task, published leaderboards increasingly report cost alongside accuracy (dollars per task, or tokens per successful completion) and flag which models are Pareto-optimal on the accuracy/cost frontier rather than just accuracy-best. For small on-device models specifically, latency and memory footprint deserve the same treatment cost gets here — a model that's 5 points behind but runs 10x faster and fits in memory the larger one can't is a different kind of "win" that a single leaderboard number won't show.

## Applying This to Small / On-Device Models

Most of the benchmarks above were built and are reported against frontier, API-hosted models. A few adjustments matter when evaluating something like a 0.3–1.5B parameter model run locally via Ollama:

- Expect much lower absolute pass rates — tool selection and strict argument-schema formatting are exactly the skills that degrade fastest as parameter count shrinks, so a low score is informative, not necessarily a bug in the eval.
- Report AST/structural correctness and executable correctness separately; small models frequently produce a call that is close in structure but fails on a type-cast or an enum value, which the two metrics distinguish.
- Track output-format compliance as its own row (did the model even emit a parseable tool call vs. plain text) — smaller models fail this more often than larger ones, and it's a distinct failure mode from picking the wrong tool.
- Pair accuracy with the practical numbers that actually matter for the on-device use case: latency per call and memory footprint, so the eval answers "is this fast/small enough to be worth its lower accuracy," not just "how accurate is it."

## References

- [The Berkeley Function Calling Leaderboard (BFCL)](https://openreview.net/forum?id=2GmDdhBdDk) | UC Berkeley Gorilla project. Verified 2026-08-20.
- [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | Sierra Research & Princeton. Verified 2026-08-20.
- [tau2-bench](https://github.com/sierra-research/tau2-bench) | Sierra Research. Verified 2026-08-20.
- [API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs](https://arxiv.org/abs/2304.08244) | Verified 2026-08-20.
- [StableToolBench: Towards Stable Large-Scale Benchmarking on Tool Learning of Large Language Models](https://arxiv.org/abs/2403.07714) | Verified 2026-08-20.
- [AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688) | Verified 2026-08-20.
