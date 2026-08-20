---
title: "Types of Evaluations"
description: "Index of evaluation categories, with a page for each type and when to build it."
---

Evaluation is not one benchmark. This guide splits LLM evaluation into ten categories, each with its own metrics, graders, build complexity, and failure modes. Use this page as an index; each entry links to a dedicated page.

## The Ten Types

| Type | Page | What it measures | Typical metric |
| --- | --- | --- | --- |
| Capability and knowledge | [Capability and knowledge](/09-capability-knowledge/) | Factual recall across domains | Accuracy on MCQ |
| Reasoning and math | [Reasoning and math](/10-reasoning-math/) | Multi-step symbolic and numeric reasoning | Exact match, usually with CoT |
| Code generation | [Code generation](/11-code-generation/) | Producing correct programs | Pass@k on unit tests |
| Long context | [Long context](/12-long-context/) | Using information anywhere in long inputs | Retrieval accuracy, per-task metrics |
| RAG faithfulness | [RAG faithfulness](/13-rag-faithfulness/) | Staying grounded in retrieved context | Faithfulness, citation F1 |
| Safety and refusal | [Safety and refusal](/14-safety-refusal/) | Refusing harmful requests, accepting safe ones | Refusal rate, harmfulness |
| Preference alignment | [Preference alignment](/15-preference-alignment/) | Matching human preferences | Win rate, reward model accuracy |
| Instruction following | [Instruction following](/16-instruction-following/) | Honoring formatting and content constraints | Constraint satisfaction |
| LLM as judge | [LLM-as-a-judge](/17-llm-as-judge/) | Using a model to grade or compare outputs | Judge agreement, win rate |
| Multilingual | [Multilingual](/18-multilingual/) | Performance outside English | Accuracy or F1 per language |

## How the Categories Relate

The categories overlap by design. Reasoning evals often rely on knowledge; RAG faithfulness evaluation frequently uses an LLM judge; multilingual tests reuse MMLU's item pool in translation. When you choose an eval, pick the category that names the failure mode you care about, then use the cross-references to find overlapping tools.

## Choosing an Eval Type

- Build a **capability or knowledge** eval when you need a broad baseline or procurement comparison ([MMLU](https://arxiv.org/abs/2009.03300)).
- Build a **reasoning or math** eval when the model must think, not just recall ([MATH](https://arxiv.org/abs/2103.03874)).
- Build a **code** eval when correctness is testable at runtime ([HumanEval](https://arxiv.org/abs/2107.03374)).
- Build a **long-context** eval when real usage exceeds a few thousand tokens ([LongBench](https://arxiv.org/abs/2308.14508)).
- Build a **RAG faithfulness** eval when the model has access to external context it might contradict ([RAGAS paper](https://arxiv.org/abs/2309.15217)).
- Build a **safety or refusal** eval before releasing anything user-facing. XSTest tests the balance between helpfulness and harmlessness ([XSTest](https://arxiv.org/abs/2308.01263)).
- Build a **preference** eval after fine-tuning with human feedback.
- Build an **instruction-following** eval for agents and structured output products.
- Build an **LLM-as-judge** setup when open-ended outputs cannot be scored by rules.
- Build a **multilingual** eval when users are not English-only ([MGSM](https://arxiv.org/abs/2210.03057)).

## Common Assembly Pattern

Almost every eval can be assembled from four parts:

1. A dataset of items, either curated or translated.
2. A prompt format, fixed across models.
3. A solver or generation step.
4. A scorer, whether exact match, rule-based, or judge model.

Frameworks in [Tools and frameworks](/05-tools/) such as [OpenCompass](https://opencompass.readthedocs.io/en/stable/) and [Inspect AI](https://inspect.aisi.org.uk/) provide all four parts ready to configure.

## References

- [HELM](https://arxiv.org/abs/2211.09110) | Taxonomy of scenarios and metrics that motivates this index. Verified 2026-08-19.
- [MMLU](https://arxiv.org/abs/2009.03300) | Knowledge benchmark. Verified 2026-08-19.
- [MATH](https://arxiv.org/abs/2103.03874) | Reasoning benchmark. Verified 2026-08-19.
- [HumanEval](https://arxiv.org/abs/2107.03374) | Code benchmark. Verified 2026-08-19.
- [LongBench](https://arxiv.org/abs/2308.14508) | Long-context benchmark. Verified 2026-08-19.
- [RAGAS paper](https://arxiv.org/abs/2309.15217) | RAG evaluation framework. Verified 2026-08-19.
- [MGSM](https://arxiv.org/abs/2210.03057) | Multilingual reasoning. Verified 2026-08-19.
- [XSTest](https://arxiv.org/abs/2308.01263) | Safety and refusal balance. Verified 2026-08-19.
- [Inspect AI](https://inspect.aisi.org.uk/) | Configurable eval framework. Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Benchmark platform. Verified 2026-08-19.