---
title: "Case Studies"
description: "Real-world applications of evaluation, with the lessons they teach."
---

Each case study is grounded in the verified sources of this guide. Use them as precedent for your own eval design.

## Case Study 1: The Contaminated Benchmark Treadmill

**Context.** AIME 2024 was used to announce a major model release, then MathArena documented strong signs of contamination in AIME 2024, since its problems were widely available online before evaluation. The result: integer-answer AIME scores inflated, and the benchmark lost credibility for these models ([MathArena contamination](https://arxiv.org/abs/2505.23281)).

**Practice.** Treat any widely cited benchmark as plausibly contaminated. Report the eval date and prefer date-capped problems, following the design of LiveCodeBench ([LiveCodeBench](https://arxiv.org/abs/2403.07974)).

## Case Study 2: Judging Open-Ended Chat Quality

**Context.** MT-Bench established the LLM-as-a-judge pattern for grading two-turn conversations with GPT-4, and simultaneously audited judge bias: position, verbosity, self-enhancement, and limited grading ability were all measured ([MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)). AlpacaEval later added length control because the naive win rate favored longer outputs ([AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475)).

**Practice.** Never ship a judge eval without a human-labeled validation slice and a length-controlled variant.

## Case Study 3: Multilingual Evaluation Built on Translation

**Context.** MMMLU professional-translated MMLU into 14 locales, and Global-MMLU extended the analysis to 42 languages. The audit found that MMLU content is culturally biased: 28% of questions require culturally sensitive knowledge and 84.9% of geographic references target North America or Europe ([Global-MMLU](https://arxiv.org/abs/2412.03304)). Translation reproduces that bias.

**Practice.** For multilingual readiness, pair a translation-family benchmark with a native-collection one, such as TyDi QA or SeaBench, which avoids English transfer ([TyDi QA](https://arxiv.org/abs/2003.05002); [SeaExam and SeaBench](https://arxiv.org/abs/2502.06298)).

## Case Study 4: RAG Hallucination Surfaced by Faithfulness Scoring

**Context.** RAG products fail when the model ignores the source and answers from parametric memory. RAGAS defines faithfulness as the fraction of claims inferable from the retrieved context, and RAGTruth supplies ~18k human-annotated responses for training detectors ([RAGAS paper](https://arxiv.org/abs/2309.15217); [RAGTruth](https://arxiv.org/abs/2401.00396)).

**Practice.** Deploy a faithfulness check before release, and calibrate the judge against human labels using the ARES calibration method ([ARES](https://arxiv.org/abs/2311.09476)).

## Case Study 5: Safety Tension Between Helpful and Harmless

**Context.** XSTest showed that models calibrated for safety at ChatGPT scale can over-refuse safe prompts that merely resemble unsafe ones, while insufficiently aligned models comply with nearly all unsafe prompts. Both extremes are failures ([XSTest](https://arxiv.org/abs/2308.01263)).

**Practice.** Score safe and unsafe prompts together. A refusal rate on unsafe prompts is uninformative without the compliance rate on the safe set.

## Cross-Cutting Lessons

- Standardize the protocol or numbers are not comparable between teams ([HELM](https://arxiv.org/abs/2211.09110)).
- Audit the grader, whatever it is.
- Retire benchmarks once saturated or contaminated.
- Read the English default bias into every multilingual claim.

## References

- [MathArena contamination](https://arxiv.org/abs/2505.23281) | Verified 2026-08-19.
- [LiveCodeBench](https://arxiv.org/abs/2403.07974) | Verified 2026-08-19.
- [MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) | Verified 2026-08-19.
- [AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475) | Verified 2026-08-19.
- [Global-MMLU](https://arxiv.org/abs/2412.03304) | Verified 2026-08-19.
- [MMMLU](https://huggingface.co/datasets/openai/MMMLU) | Verified 2026-08-19.
- [TyDi QA](https://arxiv.org/abs/2003.05002) | Verified 2026-08-19.
- [SeaExam and SeaBench](https://arxiv.org/abs/2502.06298) | Verified 2026-08-19.
- [RAGAS paper](https://arxiv.org/abs/2309.15217) | Verified 2026-08-19.
- [RAGTruth](https://arxiv.org/abs/2401.00396) | Verified 2026-08-19.
- [ARES](https://arxiv.org/abs/2311.09476) | Verified 2026-08-19.
- [XSTest](https://arxiv.org/abs/2308.01263) | Verified 2026-08-19.
- [HELM](https://arxiv.org/abs/2211.09110) | Verified 2026-08-19.