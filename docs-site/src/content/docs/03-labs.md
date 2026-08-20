---
title: "Labs and Toolmakers"
description: "The research labs, government institutes, and teams that produce evaluation frameworks."
---

This page identifies the organizations behind the frameworks and benchmarks used throughout this guide. Every entity is verified against a primary source.

## Central Framework Makers

| Lab | Affiliation | Contribution | Verified source |
| --- | --- | --- | --- |
| Stanford CRFM | Stanford HAI | HELM, HELM Long Context leaderboard | [HELM](https://arxiv.org/abs/2211.09110); [HELM Long Context](https://crfm.stanford.edu/helm/long-context/latest/) |
| EleutherAI | Open research collective | lm-evaluation-harness, Open LLM Leaderboard backend | [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) |
| Shanghai AI Laboratory | Chinese national lab | OpenCompass, CompassRank leaderboard | [OpenCompass](https://opencompass.readthedocs.io/en/stable/); [Shanghai AI Lab announcement](https://www.shlab.org.cn/news/5443498) |
| UK AI Security Institute (AISI) | UK government | Inspect framework, inspect_evals | [Inspect AI](https://inspect.aisi.org.uk/) |

## Labs by Evaluation Focus

### Generation Labs

- **OpenAI** publishes MMMLU and documents it in the o1 System Card ([AIME 2024 (o1 System Card)](https://arxiv.org/abs/2412.16720)); maintains [MMMLU](https://huggingface.co/datasets/openai/MMMLU).
- **Anthropic** and other frontier labs release system cards that standardize accuracy reporting on MMLU-style benchmarks.

### Academic Evaluators

- **EPOCH AI** maintains FrontierMath for testing frontier math capability ([FrontierMath](https://arxiv.org/abs/2411.04872)).
- **Stanford CRFM** runs the HELM framework and leaderboards ([HELM](https://arxiv.org/abs/2211.09110)).

### Regional Labs

- **Shanghai AI Laboratory** leads OpenCompass and the Compass leaderboards ([OpenCompass](https://opencompass.readthedocs.io/en/stable/); [Shanghai AI Lab announcement](https://www.shlab.org.cn/news/5443498)).
- **Academic groups** contribute regional benchmarks such as SeaExam and SeaBench for Southeast Asian languages ([SeaExam and SeaBench](https://arxiv.org/abs/2502.06298)) and IndicXTREME for Indic languages ([IndicXTREME](https://arxiv.org/abs/2212.05409)).

## Coordination and Standards

- Hugging Face's Open LLM Leaderboard uses EleutherAI's lm-evaluation-harness as its evaluation backend ([lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)).
- Government bodies increasingly operate their own eval tooling, notably the UK AISI's Inspect ([Inspect AI](https://inspect.aisi.org.uk/)) and its community eval collection ([inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals)).

## References

- [HELM](https://arxiv.org/abs/2211.09110) | Stanford CRFM. Verified 2026-08-19.
- [HELM Long Context leaderboard](https://crfm.stanford.edu/helm/long-context/latest/) | Stanford CRFM. Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Shanghai AI Laboratory. Verified 2026-08-19.
- [Shanghai AI Lab announcement](https://www.shlab.org.cn/news/5443498) | OpenCompass launch announcement, Shanghai AI Laboratory. Verified 2026-08-20.
- [Inspect AI](https://inspect.aisi.org.uk/) | UK AI Security Institute. Verified 2026-08-19.
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | EleutherAI. Verified 2026-08-19.
- [FrontierMath](https://arxiv.org/abs/2411.04872) | EPOCH AI. Verified 2026-08-19.
- [SeaExam and SeaBench](https://arxiv.org/abs/2502.06298) | Southeast Asian local evaluation. Verified 2026-08-19.
- [IndicXTREME](https://arxiv.org/abs/2212.05409) | AI4Bharat. Verified 2026-08-19.
- [MMMLU](https://huggingface.co/datasets/openai/MMMLU) | OpenAI. Verified 2026-08-19.
- [AIME 2024 (o1 System Card)](https://arxiv.org/abs/2412.16720) | OpenAI benchmark release. Verified 2026-08-19.
- [inspect_evals](https://github.com/UKGovernmentBEIS/inspect_evals) | Community eval collection. Verified 2026-08-19.