---
title: "Glossary"
description: "Canonical terms used across the evaluation guide, defined consistently."
---

## Accuracy

The fraction of items where the model output matches a gold answer, either by exact match or by a fixed extraction rule. The default metric for multiple-choice benchmarks such as MMLU and Belebele ([MMLU](https://arxiv.org/abs/2009.03300); [Belebele](https://arxiv.org/abs/2308.16884)).

## Benchmark

A fixed dataset, prompt format, and scoring rule used to compare models. Benchmarks differ from evaluation frameworks in that they ship a curated item set rather than tooling ([HELM](https://arxiv.org/abs/2211.09110)).

## Calibration

Whether predicted confidence matches observed correctness. HELM measures calibration across 16 core scenarios by comparing confidence to accuracy ([HELM](https://arxiv.org/abs/2211.09110)).

## Chain-of-thought (CoT)

A prompting technique that asks the model to reason step by step before answering. Used by MGSM and many math benchmarks to elicit reasoning ([MGSM](https://arxiv.org/abs/2210.03057)).

## Contamination

Occurrence of evaluation items, or close paraphrases of them, in a model's training data, which inflates scores. MMLU is widely suspected to be in pretraining corpora ([MathArena contamination](https://arxiv.org/abs/2505.23281)).

## Discriminative evaluation

Scoring a model by comparing its perplexity across candidate answers in a multiple-choice setting, without generating free text. OpenCompass supports this scoring mode alongside generative outputs ([OpenCompass](https://opencompass.readthedocs.io/en/stable/)).

## Evaluation framework

Software tooling for running evaluations, handling datasets, prompting, scoring, and logging. Examples are HELM, OpenCompass, Inspect, and lm-evaluation-harness.

## Exact match (EM)

A binary metric that passes only when the normalized output equals the normalized reference answer. Distinct from F1, which tolerates partial overlap. Used in XQuAD and math evaluation ([XQuAD](https://arxiv.org/abs/1910.11856)).

## F1

Harmonic mean of precision and recall over token overlap between model output and reference answer. Standard for extractive reading comprehension and span-based tasks such as TyDi QA and XQuAD ([TyDi QA](https://arxiv.org/abs/2003.05002)).

## Few-shot evaluation

Evaluation where the prompt includes a small number of solved examples before the test item, typically 0 to 5. MMLU is conventionally reported at 5-shot ([MMLU](https://arxiv.org/abs/2009.03300)).

## Generative evaluation

Evaluation where the model writes free text that is later scored, either by extraction, a judge model, or a downstream tool. OpenCompass supports this style of scoring for open-ended outputs ([OpenCompass](https://opencompass.readthedocs.io/en/stable/)).

## Grading rubric

A rule set used to score open-ended outputs, often applied by a judge model. Contrast with closed-form benchmarks that use exact match ([MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)).

## Hallucination

Model output that invents facts or contradicts provided context. Measured by faithfulness metrics in RAG evaluation ([RAGAS paper](https://arxiv.org/abs/2309.15217)).

## Judge model

A language model used to score or prefer outputs in place of a human annotator. Risks include bias toward longer or more fluent outputs ([MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)).

## LLM-as-a-judge

The practice of using a judge model for evaluation, typically as a reference-free grader or a pairwise comparator. See [LLM-as-a-judge](/17-llm-as-judge/).

## Multiple-choice

An answer format with a fixed set of options and one correct choice. The default for knowledge benchmarks, for example MMLU (4 options) and Belebele (4 options).

## Pass@k

Probability that at least one of k generated samples passes a correctness check, typically hidden unit tests. Used by code benchmarks such as HumanEval ([HumanEval](https://arxiv.org/abs/2107.03374)).

## Preference pair

A pair of model outputs plus a scalar preference or chosen-rejected label, used to train and judge alignment. See [RewardBench](https://arxiv.org/abs/2403.13787).

## ROUGE

A family of n-gram overlap metrics for summarization and generation. ROUGE-L uses the longest common subsequence. Reported for XL-Sum ([XL-Sum](https://arxiv.org/abs/2106.13822)).

## Scenario

In HELM terminology, a triple of task, domain, and language that defines one use case under evaluation ([HELM](https://arxiv.org/abs/2211.09110)).

## Task

A single evaluation setting defined by a prompt format and an expected output type, for example extractive QA or code completion.

## Win rate

Fraction of comparisons where a candidate model is judged better than a baseline. Used by AlpacaEval and Arena-Hard ([AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475)).

## Zero-shot evaluation

Evaluation with no solved examples in the prompt. Common for reasoning and instruction-following tests.

## References

The definitions above reflect the cited benchmarks and frameworks. Every benchmark and tool named here has a verified entry in [Benchmarks directory](/04-benchmarks-directory/) or [Tools and frameworks](/05-tools/).

- [HELM](https://arxiv.org/abs/2211.09110) | Scenarios, multi-metric evaluation. Verified 2026-08-19.
- [MMLU](https://arxiv.org/abs/2009.03300) | Knowledge benchmark, 5-shot accuracy. Verified 2026-08-19.
- [Belebele](https://arxiv.org/abs/2308.16884) | Multiple-choice reading comprehension. Verified 2026-08-19.
- [MGSM](https://arxiv.org/abs/2210.03057) | Multilingual math with CoT. Verified 2026-08-19.
- [MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) | Judge model evaluation. Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Discriminative and generative modes. Verified 2026-08-19.
- [HumanEval](https://arxiv.org/abs/2107.03374) | Pass@k for code. Verified 2026-08-19.
- [RAGAS paper](https://arxiv.org/abs/2309.15217) | Faithfulness and relevance. Verified 2026-08-19.
- [RewardBench](https://arxiv.org/abs/2403.13787) | Preference pairs. Verified 2026-08-19.
- [TyDi QA](https://arxiv.org/abs/2003.05002) | F1 for extractive QA. Verified 2026-08-19.
- [XQuAD](https://arxiv.org/abs/1910.11856) | F1 and EM. Verified 2026-08-19.
- [XL-Sum](https://arxiv.org/abs/2106.13822) | ROUGE for summarization. Verified 2026-08-19.
- [AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475) | Length-controlled win rate. Verified 2026-08-19.
- [MathArena contamination](https://arxiv.org/abs/2505.23281) | Contamination evidence. Verified 2026-08-19.