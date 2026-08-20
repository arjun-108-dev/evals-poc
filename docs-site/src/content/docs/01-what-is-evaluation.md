---
title: "What Is LLM Evaluation"
description: "Definitions, history, and the core concepts of LLM evaluation."
---

## What Evaluation Is

LLM evaluation is the systematic measurement of a model's capabilities, limitations, and risks under controlled conditions. It sits between training and deployment: you evaluate to decide whether a model is good enough, and the eval design determines whether your answer is trustworthy.

## Why Evaluation Needs Design

A model is a conditional text generator. It has no built-in notion of "correct." Every evaluation therefore chooses three things:

1. A **scenario**: the task, the domain of text, and the language.
2. A **metric**: accuracy, robustness, fairness, calibration, toxicity, or efficiency.
3. An **adaptation**: the prompting or fine-tuning strategy that turns the model into a system.

HELM makes this structure explicit, measuring 7 metric categories per scenario instead of a single accuracy number ([HELM](https://arxiv.org/abs/2211.09110)).

## The Two Failure Modes of Naive Evaluation

- **Benchmark gaming.** Models are compared on a single number from a public benchmark, so training data swallows the benchmark itself. The community response is contamination-aware eval (LiveCodeBench dates its problems, AIME 2024 is documented as contaminated) ([LiveCodeBench](https://arxiv.org/abs/2403.07974); [MathArena contamination](https://arxiv.org/abs/2505.23281)).
- **Dimensional collapse.** Reporting only accuracy hides robustness, fairness, and safety failures. HELM counters this by measuring 7 metrics per scenario, so metrics beyond accuracy stay visible and trade-offs surface ([HELM](https://arxiv.org/abs/2211.09110)).

## The Vocabulary of Evaluation

The comparison of a model to knowledge benchmarks uses accuracy; reasoning uses exact match; code uses pass@k; open-ended output uses judge models. Each concept is defined once in [Glossary](/08-glossary/) and reused across every page in this guide.

## Where Evaluation Is Actually Done

Three venues, three standards:

- **Model releases** report standard accuracy suites in system cards. The MMLU family anchors these: MMLU spans 57 subjects ([MMLU](https://arxiv.org/abs/2009.03300)), and MMMLU extends the test set to 14 locales with professional translations ([MMMLU](https://huggingface.co/datasets/openai/MMMLU)).
- **Leaderboards** standardize one harness across many models, for example the Open LLM Leaderboard backed by lm-evaluation-harness ([lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)).
- **Investigations** audit the evals themselves. MathArena reports strong signs of contamination in AIME 2024 ([MathArena contamination](https://arxiv.org/abs/2505.23281)). ARES reduces judge prediction errors in RAG evaluation through prediction-powered inference with human-annotated points ([ARES](https://arxiv.org/abs/2311.09476)).

## How to Read This Guide

- [Types of evaluations](/02-types-of-evals/) is the index of ten evaluation types.
- [Glossary](/08-glossary/) defines every term used.
- Pages 09 through 18 cover one evaluation type each, in the format defined in AGENTS.md.
- [Benchmarks directory](/04-benchmarks-directory/) and [Tools and frameworks](/05-tools/) index the verified data and software.

## References

- [HELM](https://arxiv.org/abs/2211.09110) | Scenario-metric taxonomy and multi-metric standards. Verified 2026-08-19.
- [MMLU](https://arxiv.org/abs/2009.03300) | Reference knowledge benchmark. Verified 2026-08-19.
- [LiveCodeBench](https://arxiv.org/abs/2403.07974) | Contamination-aware code eval. Verified 2026-08-19.
- [MathArena contamination](https://arxiv.org/abs/2505.23281) | AIME contamination evidence. Verified 2026-08-19.
- [MMMLU](https://huggingface.co/datasets/openai/MMMLU) | Multilingual MMLU release. Verified 2026-08-19.
- [ARES](https://arxiv.org/abs/2311.09476) | Calibrated fine-tuned judges. Verified 2026-08-19.
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | Leaderboard backend. Verified 2026-08-19.