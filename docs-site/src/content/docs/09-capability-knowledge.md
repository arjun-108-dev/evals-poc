---
title: "Capability and Knowledge Evaluation"
description: "What knowledge evals measure and when to build one."
---

## What It Measures

Capability and knowledge evaluation measures whether a model can recall facts across domains and infer from them at a benchmark-defined difficulty level. The standard format is multiple-choice with 4 to 10 options (MMLU uses 4, MMLU-Pro uses 10) covering subjects from elementary math to US history, law, and computer science ([MMLU](https://arxiv.org/abs/2009.03300); [MMLU-Pro](https://arxiv.org/abs/2406.01574)). Success means accuracy at or above the target threshold on a fixed, static item set. This is the cheapest test of "does the model know what it should know" and the least diagnostic of how a model behaves in an open-ended product.

## What It Is Used For

- Build one when you need a broad cross-model baseline, for procurement comparison, or for model-selection gates.
- MMLU and MMLU-Pro are the workhorses of nearly every model tech report, which makes them the lingua franca of capability claims.
- GPQA raises the difficulty to expert-written, PhD-level questions ([GPQA](https://arxiv.org/abs/2311.12022)), and HLE pushes to frontier expert level ([HLE](https://arxiv.org/abs/2501.14249)).
- HELM's original 16 core scenarios are the reference framework for doing this multi-metric instead of accuracy-only ([HELM](https://arxiv.org/abs/2211.09110)).
- See the case studies in [Case studies](/07-case-studies/) for procurement-style comparisons.

## Typical Grader / Metric

- Accuracy, scored by exact match on the selected option letter.
- Optionally with chain-of-thought to reach later MMLU-Pro questions ([MMLU-Pro](https://arxiv.org/abs/2406.01574)).
- Automatic and rule-based; no judge model required.
- MMLU-Redux and MMLU-Pro were introduced partly because ~6.49% of MMLU items contain errors, so metric quality depends on dataset hygiene ([MMLU-Redux](https://arxiv.org/abs/2406.04127)).

## Build Complexity

**Low / Medium**. Reason: the dataset is a static CSV of questions and options per language, and the scorer is exact match on an extracted option. Verified translation of items into new languages is the main cost if you go multilingual.

## What You Would Build

- Curate or buy a question set with one correct answer recorded per item.
- Fix a prompt template (for example `[question]\nA\nB\nC\nD\nAnswer:`).
- Run generations or, for open models, score by option likelihood.
- Extract the letter and compare to the gold answer.
- Optionally add few-shot exemplars; MMLU is conventionally 5-shot ([MMLU](https://arxiv.org/abs/2009.03300)).

## Related Benchmarks

- [MMLU](https://arxiv.org/abs/2009.03300), [MMLU-Pro](https://arxiv.org/abs/2406.01574), [MMLU-Redux](https://arxiv.org/abs/2406.04127) in [Benchmarks directory](/04-benchmarks-directory/).
- Hard and frontier tiers: [GPQA](https://arxiv.org/abs/2311.12022), [HLE](https://arxiv.org/abs/2501.14249).
- Broad and multimodal: [MEGA-Bench](https://arxiv.org/abs/2410.10563), [ARC](https://arxiv.org/abs/1803.05457).
- Multilingual variants: [MMMLU](https://huggingface.co/datasets/openai/MMMLU), [Global-MMLU](https://arxiv.org/abs/2412.03304).

## Related Tools

- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) ships preconfigured MMLU and MMLU-Pro configs.
- [Inspect AI](https://inspect.aisi.org.uk/) has solver/scorer primitives for MCQ tasks.
- lm-evaluation-harness implements MMLU and HellaSwag task groups ([lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md)).

## Contamination and Bias Notes

- MMLU and its variants are widely suspected to be in pretraining corpora; treat high MMLU numbers as a lower bound on true capability ([MathArena contamination](https://arxiv.org/abs/2505.23281)).
- MMLU content is US-centric by construction, which carries over to MMMLU and Global-MMLU, both translations of the same English item pool.
- HellaSwag was designed to counter trivial repetition but remains sensitive to length and style artifacts ([HellaSwag](https://arxiv.org/abs/1905.07830)).

## References

- [MMLU](https://arxiv.org/abs/2009.03300) | 57 subjects, 4-choice, 5-shot accuracy. Verified 2026-08-19.
- [MMLU-Pro](https://arxiv.org/abs/2406.01574) | 10-option reasoning upgrade. Verified 2026-08-19.
- [MMLU-Redux](https://arxiv.org/abs/2406.04127) | Error-rate audit of MMLU. Verified 2026-08-19.
- [GPQA](https://arxiv.org/abs/2311.12022) | Expert PhD-level questions. Verified 2026-08-19.
- [HLE](https://arxiv.org/abs/2501.14249) | Frontier expert questions. Verified 2026-08-19.
- [ARC](https://arxiv.org/abs/1803.05457) | Grade-school science. Verified 2026-08-19.
- [HELM](https://arxiv.org/abs/2211.09110) | Multi-metric framework. Verified 2026-08-19.
- [HellaSwag](https://arxiv.org/abs/1905.07830) | Commonsense sentence completion. Verified 2026-08-19.
- [MEGA-Bench](https://arxiv.org/abs/2410.10563) | Multimodal real-world tasks. Verified 2026-08-19.
- [MMMLU](https://huggingface.co/datasets/openai/MMMLU) | 14-language MMLU. Verified 2026-08-19.
- [Global-MMLU](https://arxiv.org/abs/2412.03304) | Culture-sensitive 42-language MMLU. Verified 2026-08-19.
- [MathArena contamination](https://arxiv.org/abs/2505.23281) | Contamination evidence. Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Benchmark platform. Verified 2026-08-19.
- [Inspect AI](https://inspect.aisi.org.uk/) | Configurable eval framework. Verified 2026-08-19.
- [lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md) | Task catalog. Verified 2026-08-19.