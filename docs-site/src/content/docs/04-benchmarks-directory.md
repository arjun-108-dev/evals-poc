---
title: "Benchmarks Directory"
description: "Index of verified evaluation benchmarks, with the metric and size of each."
---

All benchmarks listed here are verified against primary sources cited on each page. Each entry gives the metric, the size, and where the benchmark is discussed in this guide.

## Capability and Knowledge

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [ARC](https://arxiv.org/abs/1803.05457) | Accuracy | 7,787 grade-school science items, 1,172 Challenge test | [09](/09-capability-knowledge/) |
| [ARC-AGI-2](https://arxiv.org/abs/2505.11831) | pass@2 task-solve rate | 100 private tasks | [09](/09-capability-knowledge/) |
| [GPQA](https://arxiv.org/abs/2311.12022) | Accuracy | 448 expert PhD questions | [09](/09-capability-knowledge/) |
| [HLE](https://arxiv.org/abs/2501.14249) | Accuracy | 2,500 questions, 58 subjects | [09](/09-capability-knowledge/) |
| [HellaSwag](https://arxiv.org/abs/1905.07830) | Accuracy | 10,042 validation items | [09](/09-capability-knowledge/) |
| [MEGA-Bench](https://arxiv.org/abs/2410.10563) | 45 metric types | 505 multimodal tasks | [09](/09-capability-knowledge/) |
| [MMLU](https://arxiv.org/abs/2009.03300) | 5-shot accuracy | 57 subjects, ~14k items | [09](/09-capability-knowledge/) |
| [MMLU-Pro](https://arxiv.org/abs/2406.01574) | CoT accuracy | ~12k items, 10 options | [09](/09-capability-knowledge/) |
| [MMLU-Redux](https://arxiv.org/abs/2406.04127) | Accuracy | Re-annotated MMLU subsets | [09](/09-capability-knowledge/) |

## Reasoning and Math

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [AIME 2024](https://arxiv.org/abs/2412.16720) | Exact match | 15 integer-answer problems per exam | [10](/10-reasoning-math/) |
| [AIME 2025](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/aime2025) | Exact match | 30 items (AIME I+II) | [10](/10-reasoning-math/) |
| [BABILong](https://arxiv.org/abs/2406.10149) | Exact match | 20 bAbI tasks, up to 10M tokens | [10](/10-reasoning-math/), [12](/12-long-context/) |
| [BBH](https://arxiv.org/abs/2210.09261) | 3-shot CoT accuracy | 23 tasks, 6,511 items | [10](/10-reasoning-math/) |
| [FrontierMath](https://arxiv.org/abs/2411.04872) | Automated verify | Research-level problems | [10](/10-reasoning-math/) |
| [GSM8K](https://arxiv.org/abs/2110.14168) | Exact match | 8.5K word problems | [10](/10-reasoning-math/) |
| [HARP](https://arxiv.org/abs/2412.08819) | Zero-shot CoT accuracy | 5,409 competition problems | [10](/10-reasoning-math/) |
| [MATH](https://arxiv.org/abs/2103.03874) | Normalized exact match | 12.5K problems | [10](/10-reasoning-math/) |
| [MATH-500](https://arxiv.org/abs/2305.20050) | Normalized accuracy | 500 problems | [10](/10-reasoning-math/) |
| [MGSM](https://arxiv.org/abs/2210.03057) | Exact-match solve rate | 250 items x 10 languages | [10](/10-reasoning-math/), [18](/18-multilingual/) |

## Code Generation

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [BigCodeBench](https://arxiv.org/abs/2406.15877) | Pass@1 | 1,140 library-aware tasks | [11](/11-code-generation/) |
| [CodeContests](https://arxiv.org/abs/2203.07814) | n@k solve rate | 13,328 train / 165 test | [11](/11-code-generation/) |
| [HumanEval](https://arxiv.org/abs/2107.03374) | pass@1/pass@k | 164 problems | [11](/11-code-generation/) |
| [LiveCodeBench](https://arxiv.org/abs/2403.07974) | Pass@1 | 511 problems, date-capped | [11](/11-code-generation/) |
| [MBPP](https://arxiv.org/abs/2108.07732) | pass@k | 974 tasks, 500 eval | [11](/11-code-generation/) |
| [SWE-bench](https://arxiv.org/abs/2310.06770) | % resolved | 2,294 GitHub issues | [11](/11-code-generation/) |
| [SWE-bench Pro](https://arxiv.org/abs/2509.16941) | % resolved | 1,865 long-horizon issues | [11](/11-code-generation/) |
| [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) | % resolved | 500 validated issues | [11](/11-code-generation/) |

## Long Context

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [HELMET](https://arxiv.org/abs/2410.02694) | LLM-judge or auto | 7 categories, 8K-128K | [12](/12-long-context/), [17](/17-llm-as-judge/) |
| [InfiniteBench](https://arxiv.org/abs/2402.13718) | Per-task | 12 tasks, ~200K avg tokens | [12](/12-long-context/) |
| [LongBench](https://arxiv.org/abs/2308.14508) | ROUGE/F1/Edit Sim | 21 bilingual tasks | [12](/12-long-context/) |
| [LongBench v2](https://arxiv.org/abs/2412.15204) | Zero-shot accuracy | 503 MCQs, 8k-2M words | [12](/12-long-context/) |
| [LongCite](https://arxiv.org/abs/2409.02897) | Citation F1, GPT-4o judge | Up to 128K tokens | [12](/12-long-context/), [17](/17-llm-as-judge/) |
| [MMLongBench](https://arxiv.org/abs/2505.10610) | Accuracy | 13,331 examples, 8K-128K | [12](/12-long-context/) |
| [NeedleBench](https://arxiv.org/abs/2407.11963) | Accuracy | 4k-1000k tokens | [12](/12-long-context/) |
| [NIAH](https://github.com/gkamradt/LLMTest_NeedleInAHaystack) | Retrieval heatmap | Length x depth sweep | [12](/12-long-context/) |

## RAG Faithfulness

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [ARES](https://arxiv.org/abs/2311.09476) | Judge accuracy | 3 RAG dimensions | [13](/13-rag-faithfulness/), [17](/17-llm-as-judge/) |
| [Finetune-RAG](https://arxiv.org/abs/2505.10792) | Bench-RAG judge | Anti-hallucination dataset | [13](/13-rag-faithfulness/) |
| [HaluEval](https://arxiv.org/abs/2305.11747) | Accuracy/F1 | ~35k generated + 5k human | [13](/13-rag-faithfulness/) |
| [RAGAS](https://arxiv.org/abs/2309.15217) | Faithfulness | Reference-free | [13](/13-rag-faithfulness/) |
| [RAGTruth](https://arxiv.org/abs/2401.00396) | Detector F1 | ~18k responses | [13](/13-rag-faithfulness/) |
| [SummaC](https://arxiv.org/abs/2111.09525) | Balanced acc | NLI-based | [13](/13-rag-faithfulness/) |
| [TruthfulQA](https://arxiv.org/abs/2109.07958) | GPT-judge | 817 questions | [13](/13-rag-faithfulness/) |

## Safety and Refusal

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [XSTest](https://arxiv.org/abs/2308.01263) | Refusal rate | 250 safe + 200 unsafe | [14](/14-safety-refusal/) |
| [HarmBench](https://arxiv.org/abs/2402.04249) | Attack success rate | 510 harmful behaviors | [14](/14-safety-refusal/) |
| [JailbreakBench JBB](https://arxiv.org/abs/2404.01318) | Attack success rate + cost | 100 misuse behaviors (+ over-refusal set) | [14](/14-safety-refusal/) |
| [WildGuard](https://arxiv.org/abs/2406.18495) | F1 | 92K train / 5,299 test | [14](/14-safety-refusal/) |
| [AdvBench](https://arxiv.org/abs/2307.15043) | Attack success rate | 500 behaviors + 500 strings | [14](/14-safety-refusal/) |
| [TrustLLM](https://arxiv.org/abs/2401.05561) | Per-dimension scores | 16 LLMs, 30+ datasets | [14](/14-safety-refusal/) |
| [RealToxicityPrompts](https://arxiv.org/abs/2009.11462) | Expected-max toxicity | 100K prompts | [14](/14-safety-refusal/) |

## Preference and Alignment

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [AlpacaEval](https://github.com/tatsu-lab/alpaca_eval) | Win rate | 805 instructions | [15](/15-preference-alignment/), [17](/17-llm-as-judge/) |
| [AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475) | Length-controlled win rate | 805 instructions | [15](/15-preference-alignment/), [17](/17-llm-as-judge/) |
| [Arena-Hard](https://arxiv.org/abs/2406.11939) | Win rate | 500 hard prompts | [15](/15-preference-alignment/), [17](/17-llm-as-judge/) |
| [Chatbot Arena](https://arxiv.org/abs/2403.04132) | Bradley-Terry Elo | 240K+ votes | [15](/15-preference-alignment/) |
| [MT-Bench](https://arxiv.org/abs/2306.05685) | Judge score | 80 two-turn questions | [15](/15-preference-alignment/), [17](/17-llm-as-judge/) |
| [RewardBench](https://arxiv.org/abs/2403.13787) | Pairwise accuracy | 2,985 trios | [15](/15-preference-alignment/), [17](/17-llm-as-judge/) |

## Instruction Following

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [IFEval](https://arxiv.org/abs/2311.07911) | Strict/loose accuracy | 541 prompts, 25 types | [16](/16-instruction-following/) |
| [FollowBench](https://arxiv.org/abs/2310.20410) | HSR/SSR/CSL | 820 instructions, up to 5 constraint levels | [16](/16-instruction-following/) |
| [InfoBench](https://arxiv.org/abs/2401.03601) | Decomposed requirements following ratio | 500 instructions, 2,250 sub-questions | [16](/16-instruction-following/) |
| [The Instruction Hierarchy](https://arxiv.org/abs/2404.13208) | Robustness % | In-domain + held-out attack suites | [16](/16-instruction-following/), [14](/14-safety-refusal/) |

## Language Model as Judge

| Method | Metric | Grader | Detail page |
| --- | --- | --- | --- |
| [G-Eval](https://arxiv.org/abs/2303.16634) | Reference-free NLG score | Prompted CoT judge | [17](/17-llm-as-judge/) |
| [JudgeLM](https://arxiv.org/abs/2310.17631) | Parity with GPT-4 judgments | Fine-tuned 7B/13B/33B | [17](/17-llm-as-judge/) |
| [Prometheus / Prometheus 2](https://arxiv.org/abs/2405.01535) | Rubric-grounded score, agreement | Fine-tuned 7B/13B/8x7B | [17](/17-llm-as-judge/) |
| [PandaLM](https://arxiv.org/abs/2306.05087) | Swap-consistency filtered preference | Fine-tuned 7B judge | [17](/17-llm-as-judge/) |
| [Self-Recognition / Self-Preference](https://arxiv.org/abs/2404.13076) | Self-preference magnitude | Diagnostic study | [17](/17-llm-as-judge/) |

## Multilingual

| Benchmark | Metric | Size | Detail page |
| --- | --- | --- | --- |
| [Belebele](https://arxiv.org/abs/2308.16884) | Accuracy | 122 language variants | [18](/18-multilingual/) |
| [CulturaX](https://arxiv.org/abs/2309.09400) | n/a (corpus) | 6.3T tokens, 167 languages | [18](/18-multilingual/) |
| [Global-MMLU](https://arxiv.org/abs/2412.03304) | Accuracy | 42 languages | [18](/18-multilingual/) |
| [IndicXTREME](https://arxiv.org/abs/2212.05409) | Accuracy/F1 | 9 tasks, 20 languages | [18](/18-multilingual/) |
| [MMMLU](https://huggingface.co/datasets/openai/MMMLU) | Accuracy | ~197k items, 14 locales | [09](/09-capability-knowledge/), [18](/18-multilingual/) |
| [SeaExam and SeaBench](https://arxiv.org/abs/2502.06298) | Accuracy / judge-based | Southeast Asian local questions | [18](/18-multilingual/) |
| [TyDi QA](https://arxiv.org/abs/2003.05002) | F1 | 204K QA pairs, 11 languages | [18](/18-multilingual/) |
| [XCOPA](https://arxiv.org/abs/2005.00333) | Accuracy | 11 languages | [18](/18-multilingual/) |
| [XL-Sum](https://arxiv.org/abs/2106.13822) | ROUGE | 1M pairs, 44 languages | [18](/18-multilingual/) |
| [XQuAD](https://arxiv.org/abs/1910.11856) | F1/EM | 1,190 QA pairs, 10 languages | [18](/18-multilingual/) |

## References

Every entry in this directory maps to a verified primary source, fetched and confirmed on 2026-08-19. Benchmarks without a verified URL are not listed here. Entry counts and metrics follow the cited abstracts; where an abstract does not state a size, the entry lists only what is sourced.