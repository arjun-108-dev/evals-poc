---
title: "Multilingual Evaluation"
description: "How to evaluate LLM performance outside English."
---

## What It Measures

Multilingual evaluation measures a model's accuracy and fluency in languages other than English, usually by reusing an English benchmark task and translating or natively collecting items. The dominant pattern is translation of English benchmarks (MGSM, XQuAD, Belebele passages, MMMLU) which risks "translationese" and Anglo-American content. The corrective pattern is native collection (TyDi QA, IndicXTREME, SeaBench) which avoids both. Success is accuracy or F1 per language, and the headline number is usually the cross-language average ([MGSM](https://arxiv.org/abs/2210.03057); [TyDi QA](https://arxiv.org/abs/2003.05002)).

## What It Is Used For

- Build one when users are not English-only or when you must document non-English gaps before launch.
- MMMLU and Global-MMLU give knowledge retrieval across 14 and 42 languages respectively ([MMMLU](https://huggingface.co/datasets/openai/MMMLU); [Global-MMLU](https://arxiv.org/abs/2412.03304)).
- MGSM and XQuAD cover reasoning and reading comprehension in 10 to 11 languages ([MGSM](https://arxiv.org/abs/2210.03057); [XQuAD](https://arxiv.org/abs/1910.11856)).
- Belebele spans 122 language variants, the widest net currently available ([Belebele](https://arxiv.org/abs/2308.16884)).
- TyDi QA is the reference for native, non-translated multilingual QA ([TyDi QA](https://arxiv.org/abs/2003.05002)).
- IndicXTREME covers 20 Indic languages across retrieval, QA, and classification ([IndicXTREME](https://arxiv.org/abs/2212.05409)).
- SeaExam and SeaBench measure local, real-world questions in Southeast Asia ([SeaExam and SeaBench](https://arxiv.org/abs/2502.06298)).

## Typical Grader / Metric

- Accuracy for multiple-choice (MMMLU, Global-MMLU, Belebele).
- Exact-match solve rate for MGSM under chain-of-thought ([MGSM](https://arxiv.org/abs/2210.03057)).
- F1 and EM for extractive QA (XQuAD, TyDi QA) ([XQuAD](https://arxiv.org/abs/1910.11856)).
- XL-Sum reports ROUGE for abstractive summarization ([XL-Sum](https://arxiv.org/abs/2106.13822)).
- Mix of rule-based and judge-based scoring depending on the task.

## Build Complexity

**Medium / High**. Reason: the translated-corpus route requires professional translators for quality, and the native-collection route requires in-country annotators. A judge model is only needed for open-ended tasks.

## What You Would Build

- Choose a route: translated or native.
- Translated route: pick an English task, obtain professional or high-quality translations per target language, retain the metric.
- Native route: hire native annotators to write items in context, as TyDi QA did ([TyDi QA](https://arxiv.org/abs/2003.05002)).
- Report per-language and cross-language average, and flag the English-to-other-language gap.

## Related Benchmarks

- [MMMLU](https://huggingface.co/datasets/openai/MMMLU), [Global-MMLU](https://arxiv.org/abs/2412.03304), [MGSM](https://arxiv.org/abs/2210.03057), [XQuAD](https://arxiv.org/abs/1910.11856), [Belebele](https://arxiv.org/abs/2308.16884), [TyDi QA](https://arxiv.org/abs/2003.05002), [IndicXTREME](https://arxiv.org/abs/2212.05409), [SeaExam and SeaBench](https://arxiv.org/abs/2502.06298), [XCOPA](https://arxiv.org/abs/2005.00333), [XL-Sum](https://arxiv.org/abs/2106.13822) in [Benchmarks directory](/04-benchmarks-directory/).

## Related Tools

- [CulturaX](https://arxiv.org/abs/2309.09400) is a 167-language pretraining corpus for building plurilingual models.
- lm-evaluation-harness ships Belebele and MMLU variants ([lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md)).

## Contamination and Bias Notes

- Translated benchmarks inherit English content and Anglo-American facts; Global-MMLU shows most culturally sensitive items favor the Americas and Europe, and 28% of MMLU items require culturally sensitive knowledge ([Global-MMLU](https://arxiv.org/abs/2412.03304)).
- MMLU-based items potentially sit in pretraining data, raising contamination risk for every MMLU translation.
- Translation-sourced passages, including Belebele's parallel reading-comprehension items, carry English framing even at low-resource coverage.
- Native-collection benchmarks reduce translationese but cost far more to build.

## References

- [MMMLU](https://huggingface.co/datasets/openai/MMMLU) | 14-locale professional translation of MMLU. Verified 2026-08-19.
- [Global-MMLU](https://arxiv.org/abs/2412.03304) | Cultural and linguistic bias analysis. Verified 2026-08-19.
- [MGSM](https://arxiv.org/abs/2210.03057) | 10-language grade-school math. Verified 2026-08-19.
- [XQuAD](https://arxiv.org/abs/1910.11856) | 10-language extractive QA. Verified 2026-08-19.
- [Belebele](https://arxiv.org/abs/2308.16884) | 122-language reading comprehension. Verified 2026-08-19.
- [TyDi QA](https://arxiv.org/abs/2003.05002) | Native QA in 11 languages. Verified 2026-08-19.
- [IndicXTREME](https://arxiv.org/abs/2212.05409) | 9 tasks in 20 Indic languages. Verified 2026-08-19.
- [SeaExam and SeaBench](https://arxiv.org/abs/2502.06298) | SEA local questions. Verified 2026-08-19.
- [XCOPA](https://arxiv.org/abs/2005.00333) | Causal commonsense in 11 languages. Verified 2026-08-19.
- [XL-Sum](https://arxiv.org/abs/2106.13822) | 44-language summarization. Verified 2026-08-19.
- [CulturaX](https://arxiv.org/abs/2309.09400) | 167-language corpus. Verified 2026-08-19.
- [lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md) | Task catalog. Verified 2026-08-19.