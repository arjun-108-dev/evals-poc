---
title: "LLM-as-a-Judge Evaluation"
description: "How to use a model to grade or compare outputs, and the biases to watch for."
---

## What It Measures

LLM-as-a-judge evaluation uses a second model to score or compare the outputs of the model under test. It is not a benchmark; it is an evaluation method for open-ended answers that elude rule-based scoring. Two modes dominate: single-answer grading, where a judge rates an output against a rubric, and pairwise comparison, where a judge prefers one of two outputs. The concern that motivates this page is judge validity, whether the judge agrees with humans and stays unbiased ([MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)).

## What It Is Used For

- Build one when outputs are free-form and cannot be scored by exact match, for example conversational quality, summarization, or preference.
- MT-Bench established the reference pattern for judge-based chat evaluation ([MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)).
- G-Eval scores open-ended text against a rubric with a chain-of-thought judge, reference-free ([G-Eval](https://arxiv.org/abs/2303.16634)).
- JudgeLM, Prometheus, and Prometheus 2 fine-tune open judge models to reduce API dependence ([JudgeLM](https://arxiv.org/abs/2310.17631); [Prometheus 2](https://arxiv.org/abs/2405.01535)).
- AlpacaEval 2.0 and Arena-Hard use a judge model for pairwise win rate ([AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475), [Arena-Hard](https://arxiv.org/abs/2406.11939)).
- ARES uses fine-tuned judges with calibration for RAG evaluation ([ARES](https://arxiv.org/abs/2311.09476)).
- LongCite uses a judge to score citation fidelity ([LongCite](https://arxiv.org/abs/2409.02897)).

## Typical Grader / Metric

- Pairwise win rate, with length-controlled variants that remove length bias.
- Single-answer judgment against a grading rubric (G-Eval, Prometheus).
- Judge agreement, computed against human labels, is the validity check you must report.
- Automatic by definition, but only trustworthy after human validation.

## Build Complexity

**Medium**. Reason: the judge is an API or open model you already have, but you must build a rubric, validate judge-human agreement on a labeled slice, and watch for the four known biases below.

## What You Would Build

- Choose a judging mode: single-answer or pairwise.
- Write a grading rubric with explicit criteria.
- Sample outputs and have the judge score them.
- Validate the judge against human labels; measure agreement.
- Report win rate or rubric score with confidence intervals.
- When relevant, enable length control to neutralize length bias.

## Related Benchmarks

- [MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685), [AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475), [LongCite](https://arxiv.org/abs/2409.02897), [ARES](https://arxiv.org/abs/2311.09476) in [Benchmarks directory](/04-benchmarks-directory/).
- Open judge methods: [G-Eval](https://arxiv.org/abs/2303.16634), [JudgeLM](https://arxiv.org/abs/2310.17631), [Prometheus 2](https://arxiv.org/abs/2405.01535), [PandaLM](https://arxiv.org/abs/2306.05087).

## Related Tools

- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) and [Inspect AI](https://inspect.aisi.org.uk/) ship model-graded evaluation primitives. See [Tools and frameworks](/05-tools/).

## Contamination and Bias Notes

- Flags from the reference study: judges bias toward position, verbosity, self-enhancement, and limited grading capability ([MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)).
- Length-controlled win rate is the standard corrective in pairwise setups ([AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475)).
- Most open judges inherit training-data dependence; even fine-tuned judges score answers from their own family higher.
- Studies confirm judges are lenient, prompt-sensitive, and can be fooled by placeholder answers; always audit judge-human agreement ([Judging the Judges](https://arxiv.org/abs/2406.12624)).
- Self-preference is documented for GPT-3.5, GPT-4, and Llama 2 and is a causal, reproducible effect ([Self-Recognition / Self-Preference](https://arxiv.org/abs/2404.13076)).

## References

- [MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) | Reference judge protocol and bias taxonomy. Verified 2026-08-19.
- [AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475) | Length-controlled judge. Verified 2026-08-19.
- [Arena-Hard](https://arxiv.org/abs/2406.11939) | Hard-prompt pairwise judge. Verified 2026-08-19.
- [G-Eval](https://arxiv.org/abs/2303.16634) | Reference-free rubric scoring. Verified 2026-08-19.
- [JudgeLM](https://arxiv.org/abs/2310.17631) | Fine-tuned open judge. Verified 2026-08-19.
- [Prometheus 2](https://arxiv.org/abs/2405.01535) | Open judge, merged modes. Verified 2026-08-19.
- [PandaLM](https://arxiv.org/abs/2306.05087) | Distilled pairwise judge. Verified 2026-08-19.
- [ARES](https://arxiv.org/abs/2311.09476) | Calibrated fine-tuned judges. Verified 2026-08-19.
- [LongCite](https://arxiv.org/abs/2409.02897) | Citation judge. Verified 2026-08-19.
- [Judging the Judges](https://arxiv.org/abs/2406.12624) | 13 judges vs human alignment. Verified 2026-08-19.
- [Self-Recognition / Self-Preference](https://arxiv.org/abs/2404.13076) | Judge self-preference study. Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Model-graded scoring. Verified 2026-08-19.
- [Inspect AI](https://inspect.aisi.org.uk/) | Model-graded scoring. Verified 2026-08-19.