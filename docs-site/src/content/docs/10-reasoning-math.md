---
title: "Reasoning and Math Evaluation"
description: "How to measure multi-step reasoning and symbolic math."
---

## What It Measures

Reasoning and math evaluation measures whether a model can produce a correct final answer for problems that require several inferential steps, algorithmic manipulation, or graded difficulty levels, rather than recall of a fact. Formats include word problems (GSM8K), competition problems (MATH, HARP, AIME), and benchmarked BIG-Bench reasoning tasks (BBH). Success is defined by an exact numeric or symbolic match against a gold answer, and models are usually prompted with chain-of-thought to elicit the reasoning trace ([GSM8K](https://arxiv.org/abs/2110.14168); [MATH](https://arxiv.org/abs/2103.03874); [BBH](https://arxiv.org/abs/2210.09261)).

## What It Is Used For

- Build one when the product involves arithmetic, tutoring, agents that compute, or any claim of "reasoning" capability.
- GSM8K is the standard entry point for grade-school math ([GSM8K](https://arxiv.org/abs/2110.14168)).
- MATH and AIME push difficulty into competition territory ([MATH](https://arxiv.org/abs/2103.03874); [AIME 2024 (o1 System Card)](https://arxiv.org/abs/2412.16720)).
- FrontierMath is the research-grade ceiling with automated verification ([FrontierMath](https://arxiv.org/abs/2411.04872)).
- BBH covers non-math reasoning skills such as logic and temporal reasoning ([BBH](https://arxiv.org/abs/2210.09261)).
- See [Case studies](/07-case-studies/) for contamination-aware math timelines.

## Typical Grader / Metric

- Exact match on the normalized final answer, extracted after chain-of-thought.
- MATH uses answer extraction plus normalization; AIME requires exact integers.
- HARP uses SymPy for automated symbolic checking of competition answers ([HARP](https://arxiv.org/abs/2412.08819)).
- FrontierMath uses automated verification of programming-generated certificates ([FrontierMath](https://arxiv.org/abs/2411.04872)).
- All automatic and rule-based; no judge model.
- MATH-500 is the 500-problem subset used for rollout and policy evaluations ([MATH-500](https://arxiv.org/abs/2305.20050)).

## Build Complexity

**Medium**. Reason: curating problems with gold answers and a verifier is moderate work, and the harder tiers (AIME, FrontierMath) require expert-problem generation or licensing. Prompting and answer-extraction engineering dominate the effort.

## What You Would Build

- Select a difficulty tier: GSM8K, MATH-500, MATH, AIME, or FrontierMath.
- Prompt with chain-of-thought (`Let's think step by step`) and request a boxed or final answer.
- Extract the answer and normalize (strip units, canonical form).
- Compare exact match against gold.
- For symbolic answers, verify with an automated checker such as SymPy ([HARP](https://arxiv.org/abs/2412.08819)).

## Related Benchmarks

- [GSM8K](https://arxiv.org/abs/2110.14168), [MATH](https://arxiv.org/abs/2103.03874), [MATH-500](https://arxiv.org/abs/2305.20050), [BBH](https://arxiv.org/abs/2210.09261).
- Competition tier: [AIME 2024 (o1 System Card)](https://arxiv.org/abs/2412.16720), [AIME 2025 (inspect_evals)](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/aime2025), [HARP](https://arxiv.org/abs/2412.08819).
- Frontier: [FrontierMath](https://arxiv.org/abs/2411.04872).
- Multilingual: [MGSM](https://arxiv.org/abs/2210.03057) in [Benchmarks directory](/04-benchmarks-directory/).

## Related Tools

- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) has general math evaluation guidance and reasoning-model tutorials.
- [Inspect AI](https://inspect.aisi.org.uk/) and inspect_evals ship AIME and math evaluators ([AIME 2025 (inspect_evals)](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/aime2025)).
- lm-evaluation-harness implements GSM8K and CoT variants ([lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md)).

## Contamination and Bias Notes

- AIME 2024 is widely available online and shows strong signs of contamination, so MathArena evaluates models in real time on freshly released competition problems to avoid memorization ([MathArena contamination](https://arxiv.org/abs/2505.23281)).
- Old, static benchmarks like GSM8K and MATH are near-saturated on frontier models; prefer fresh problems or date-capped evals to measure current capability.
- English-only source content biases items toward Anglo-American school curricula.

## References

- [GSM8K](https://arxiv.org/abs/2110.14168) | Grade-school word problems. Verified 2026-08-19.
- [MATH](https://arxiv.org/abs/2103.03874) | Competition problems with normalization. Verified 2026-08-19.
- [MATH-500](https://arxiv.org/abs/2305.20050) | 500-problem subset. Verified 2026-08-19.
- [BBH](https://arxiv.org/abs/2210.09261) | BIG-Bench Hard suite. Verified 2026-08-19.
- [AIME 2024 (o1 System Card)](https://arxiv.org/abs/2412.16720) | Integer-answer competition. Verified 2026-08-19.
- [AIME 2025 (inspect_evals)](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/aime2025) | Integer-answer competition. Verified 2026-08-19.
- [HARP](https://arxiv.org/abs/2412.08819) | 5,409 US competition problems. Verified 2026-08-19.
- [FrontierMath](https://arxiv.org/abs/2411.04872) | Automated verification at research level. Verified 2026-08-19.
- [MGSM](https://arxiv.org/abs/2210.03057) | 10-language math word problems. Verified 2026-08-19.
- [MathArena contamination](https://arxiv.org/abs/2505.23281) | AIME contamination evidence. Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Benchmark platform. Verified 2026-08-19.
- [Inspect AI](https://inspect.aisi.org.uk/) | Configurable eval framework. Verified 2026-08-19.
- [lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md) | Task catalog. Verified 2026-08-19.