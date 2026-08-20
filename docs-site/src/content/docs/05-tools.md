---
title: "Tools and Frameworks"
description: "The evaluation frameworks, tooling, and libraries you build with."
---

This page covers the software you run evals with, distinct from the datasets in [Benchmarks directory](/04-benchmarks-directory/). Every tool is verified against its official docs or repository.

## Full Frameworks

| Tool | Maintainer | What it does | Verified source |
| --- | --- | --- | --- |
| [HELM](https://arxiv.org/abs/2211.09110) | Stanford CRFM | Holistic multi-metric eval, scenarios x metrics | [Leaderboard](https://crfm.stanford.edu/helm/long-context/latest/) |
| [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Shanghai AI Lab | 100+ datasets, objective + subjective, distributed | [Docs](https://opencompass.readthedocs.io/en/stable/) |
| [Inspect AI](https://inspect.aisi.org.uk/) | UK AI Security Institute | Composable tasks, agents, tools, sandboxes, 200+ prebuilt evals | [Docs](https://inspect.aisi.org.uk/) |
| [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | EleutherAI | 60+ benchmarks, HuggingFace/vLLM backends | [Repo](https://github.com/EleutherAI/lm-evaluation-harness) |

## Choosing a Framework

- Pick **HELM** when you want standardized multi-metric comparison across scenarios, or its long-context leaderboard specifically ([HELM Long Context leaderboard](https://crfm.stanford.edu/helm/long-context/latest/)).
- Pick **OpenCompass** when you want many preconfigured Chinese and English benchmarks plus dedicated LLM-as-judge, code, and math verification tutorials ([OpenCompass](https://opencompass.readthedocs.io/en/stable/)).
- Pick **Inspect AI** when you build agent, tool-use, or sandboxed code evals and want its built-in agents, MCP tools, and Inspect View ([Inspect AI](https://inspect.aisi.org.uk/)).
- Pick **lm-evaluation-harness** when you run standard academic benchmarks on HuggingFace models quickly. It backs the Open LLM Leaderboard ([lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)).

## Framework Feature Notes

- OpenCompass splits evaluation into Configure, Inference, Evaluation, and Visualization stages; task partitioners and runners handle parallel execution ([OpenCompass docs](https://opencompass.readthedocs.io/en/stable/get_started/quick_start.html)).
- Inspect models an eval as a Task combining a Dataset, a Solver, and a Scorer, with support for model-graded scoring and sandboxing ([Inspect AI](https://inspect.aisi.org.uk/)).
- lm-evaluation-harness decodes the task catalog and supports API, HuggingFace, vLLM, and GGUF backends ([lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md)).

## Specialized Tooling

| Tool | Purpose | Verified source |
| --- | --- | --- |
| [RAGAS](https://arxiv.org/abs/2309.15217) | Reference-free RAG metrics (faithfulness, relevance) | [Docs](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) |
| [TruLens RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/) | RAG hallucination checks: context relevance, groundedness, answer relevance | [Docs](https://www.trulens.org/getting_started/core_concepts/rag_triad/) |
| [HelpSteer](https://arxiv.org/abs/2311.09528) | Multi-attribute reward labels | [Paper](https://arxiv.org/abs/2311.09528) |
| [HelpSteer2](https://arxiv.org/abs/2406.08673) | Preference pairs for reward training | [Paper](https://arxiv.org/abs/2406.08673) |
| [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/aime2025) | Community eval collection for Inspect | [Repo](https://github.com/UKGovernmentBEIS/inspect_evals) |

## References

- [HELM](https://arxiv.org/abs/2211.09110) | Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Verified 2026-08-19.
- [Inspect AI](https://inspect.aisi.org.uk/) | Verified 2026-08-19.
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | Verified 2026-08-19.
- [RAGAS Faithfulness docs](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) | Verified 2026-08-19.
- [TruLens RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/) | Verified 2026-08-19.
- [RAGAS paper](https://arxiv.org/abs/2309.15217) | Reference-free RAG metrics. Verified 2026-08-19.
- [HelpSteer](https://arxiv.org/abs/2311.09528) | Reward labels. Verified 2026-08-19.
- [HelpSteer2](https://arxiv.org/abs/2406.08673) | Preference pairs. Verified 2026-08-19.
- [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) | Community eval collection. Verified 2026-08-19.
- [HELM Long Context leaderboard](https://crfm.stanford.edu/helm/long-context/latest/) | Verified 2026-08-19.
- [lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md) | Task catalog. Verified 2026-08-19.