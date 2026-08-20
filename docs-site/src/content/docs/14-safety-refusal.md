---
title: "Safety and Refusal Evaluation"
description: "How to measure whether a model refuses harmful requests without refusing safe ones."
---

## What It Measures

Safety and refusal evaluation measures the model's decision boundary between compliance and refusal across a calibrated set of prompts. Two quantities matter together: refusal on unsafe prompts (harmlessness) and compliance on safe prompts that merely resemble unsafe ones (helpfulness, the absence of exaggerated safety). XSTest is the canonical instrument: 250 safe prompts across ten categories (homonyms, figurative language, safe contexts, privacy) and 200 contrastive unsafe prompts ([XSTest](https://arxiv.org/abs/2308.01263)). Success means refusing the unsafe set while answering most of the safe set.

## What It Is Used For

- Build one before any user-facing release, especially chatbots, coding assistants, and agentic tools that can take actions.
- XSTest is small (450 prompts) and is the cheapest systematic red team you can run ([XSTest](https://arxiv.org/abs/2308.01263)).
- HarmBench and JailbreakBench standardize the attack side: 510 and 100 curated harmful behaviors respectively, scored as attack success rate ([HarmBench](https://arxiv.org/abs/2402.04249); [JailbreakBench JBB](https://arxiv.org/abs/2404.01318)).
- WildGuard gives a fine-tuned moderation classifier with a labeled refusal/harmfulness test set ([WildGuard](https://arxiv.org/abs/2406.18495)).
- TrustLLM bundles truthfulness, safety, fairness, robustness, privacy, and ethics into one reportable scorecard ([TrustLLM](https://arxiv.org/abs/2401.05561)).

## Typical Grader / Metric

- Refusal rate, the fraction of prompts fully or partially refused, scored per prompt.
- Attack success rate (ASR) for adversarial evaluation, usually graded by a semantic policy judge or a fine-tuned classifier ([HarmBench](https://arxiv.org/abs/2402.04249)).
- Manual annotation is the reference method; string matching and GPT-4 classification approximate it, though string matching both over- and under-counts ([XSTest](https://arxiv.org/abs/2308.01263)).
- Needs "good output" generation from the model, then a classifier (rule-based, fine-tuned, or a judge model).

## Build Complexity

**Medium**. Reason: the prompt sets exist and are cheap to run, but the scoring taxonomy (full compliance, partial refusal, full refusal) is subtle enough that you need either careful manual annotation or a validated judge classifier.

## What You Would Build

- Download the XSTest prompt set.
- Generate responses to the full 450-prompts.
- Classify each response as compliant, partial refusal, or full refusal, manually or via a judge model.
- Report safe-prompt refusal rate (lower is better) and unsafe-prompt refusal rate (higher is better).
- Use rollback- or guardrail-specific subsets when testing deployed systems.

## Related Benchmarks

- [XSTest](https://arxiv.org/abs/2308.01263), [HarmBench](https://arxiv.org/abs/2402.04249), [JailbreakBench JBB](https://arxiv.org/abs/2404.01318), [WildGuard](https://arxiv.org/abs/2406.18495), [AdvBench](https://arxiv.org/abs/2307.15043), [TrustLLM](https://arxiv.org/abs/2401.05561), plus [HELM](https://arxiv.org/abs/2211.09110) (bias and toxicity metrics) and [TruthfulQA](https://arxiv.org/abs/2109.07958) in [Benchmarks directory](/04-benchmarks-directory/).

## Related Tools

- [Inspect AI](https://inspect.aisi.org.uk/) supports refusal scoring; XSTest implementations exist in inspect_evals. See [Tools and frameworks](/05-tools/).

## Contamination and Bias Notes

- XSTest has shaped safety fine-tuning and prompt patterns, so model eval-awareness may have shifted behavior.
- AdvBench behaviors are now widely reused in training and later evals; treat them as a format rather than a freshness signal ([AdvBench](https://arxiv.org/abs/2307.15043)).
- Classifier judges (string matching, fine-tuned moderators) trade off false refusals against missed attacks; calibrate on a labeled slice.
- Models overfit lexically to refusal phrases; test adversarial reformulations.
- Most safety sets are English-only by construction.

## References

- [XSTest](https://arxiv.org/abs/2308.01263) | 250 safe + 200 unsafe prompts. Verified 2026-08-19.
- [HarmBench](https://arxiv.org/abs/2402.04249) | 510 harmful behaviors, ASR grading. Verified 2026-08-19.
- [JailbreakBench JBB](https://arxiv.org/abs/2404.01318) | 100 misuse behaviors + over-refusal set. Verified 2026-08-19.
- [WildGuard](https://arxiv.org/abs/2406.18495) | Moderation model and test set. Verified 2026-08-19.
- [AdvBench](https://arxiv.org/abs/2307.15043) | 500 harmful behaviors, GCG paper. Verified 2026-08-19.
- [TrustLLM](https://arxiv.org/abs/2401.05561) | Multi-dimension trustworthiness. Verified 2026-08-19.
- [HELM](https://arxiv.org/abs/2211.09110) | Toxicity and bias categories. Verified 2026-08-19.
- [TruthfulQA](https://arxiv.org/abs/2109.07958) | Truthfulness failures. Verified 2026-08-19.
- [Inspect AI](https://inspect.aisi.org.uk/) | Refusal scoring support. Verified 2026-08-19.