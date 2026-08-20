---
title: "How to Build Evaluations"
description: "A step-by-step procedure for building a trustworthy eval."
---

This page is the practitioner playbook. It compresses the per-type pages (09 to 18) into a repeatable procedure. Before building anything, [Types of evaluations](/02-types-of-evals/) tells you which eval to build, and [Glossary](/08-glossary/) defines the terms.

## Step 1. Decide What Failure Mode You Care About

Evaluation only pays off when it names a risk you must control. Choose the type that names your risk:

- Unsure if the model knows the domain facts: capability and knowledge.
- Needs to think or compute: reasoning and math.
- Writes programs: code generation.
- Ingests long documents: long context.
- Answers over retrieved sources: RAG faithfulness.
- Faces user harm: safety and refusal.
- Should sound pleasant and on-policy: preference alignment and instruction following.
- Deployed outside English: multilingual.

## Step 2. Pick the Dataset and Metric

Use the verified catalog in [Benchmarks directory](/04-benchmarks-directory/). Match the metric to the output type:

| Output type | Metric |
| --- | --- |
| Multiple choice | Accuracy |
| Numeric / symbolic | Exact match after normalization |
| Code | pass@k under hidden tests |
| Open-ended | Judge model, validated against humans |

Reuse an existing dataset where possible. Building a new dataset is justified only when the existing ones are contaminated or off-domain ([MathArena contamination](https://arxiv.org/abs/2505.23281)).

## Step 3. Pick the Framework

Match the framework to the eval shape:

- Standard academic suite on local models: lm-evaluation-harness ([repo](https://github.com/EleutherAI/lm-evaluation-harness)).
- Many configured benchmarks, Chinese plus English, distributed: OpenCompass ([docs](https://opencompass.readthedocs.io/en/stable/)).
- Agents, tools, sandboxes, custom scorers: Inspect ([docs](https://inspect.aisi.org.uk/)).
- Multi-metric transparency across scenarios: HELM ([paper](https://arxiv.org/abs/2211.09110)).

## Step 4. Fix the Protocol Before Running

Publish the protocol alongside the results. It must fix:

1. The prompt template and number of shots.
2. Sampling temperature and count.
3. The extraction or scoring rule.
4. The judge model and its rubric.

HELM exists because fixing the adaptation protocol makes cross-model numbers comparable ([HELM](https://arxiv.org/abs/2211.09110)).

## Step 5. Validate the Grader

For any judge-based metric:

- Sample a labeled subset of model outputs.
- Score with the judge and with humans.
- Report agreement and disagreement patterns.
- Look for the four judge biases: position, verbosity, self-enhancement, and grading capability ([MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)).
- Enable length control where the judge compares responses ([AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475)).

For rule-based metrics (accuracy, exact match, pass@k), validate the extraction on a sample before trusting the number.

## Step 6. Guard Against Contamination

- Prefer dated, live, or private evals for frontier claims ([LiveCodeBench](https://arxiv.org/abs/2403.07974)).
- Treat old benchmarks (MMLU, GSM8K, HumanEval) as upper bounds, since they are plausibly in training data.
- Record the eval date in your results, because benchmark membership changes over time.

## Step 7. Report the Whole Picture

- Report per-type metrics, not one aggregate score.
- Include failure analysis, not just the average.
- Link every number to its dataset, prompt, and grader.
- Flag English-only coverage if you claim multilingual readiness ([Global-MMLU](https://arxiv.org/abs/2412.03304)).

## References

- [HELM](https://arxiv.org/abs/2211.09110) | Protocol standardization. Verified 2026-08-19.
- [MathArena contamination](https://arxiv.org/abs/2505.23281) | Contamination as a reason to build fresh evals. Verified 2026-08-19.
- [LiveCodeBench](https://arxiv.org/abs/2403.07974) | Date-capping as a contamination defense. Verified 2026-08-19.
- [MT-Bench / LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) | Judge bias taxonomy. Verified 2026-08-19.
- [AlpacaEval 2.0 (LC)](https://arxiv.org/abs/2404.04475) | Length control. Verified 2026-08-19.
- [Global-MMLU](https://arxiv.org/abs/2412.03304) | Multilingual coverage audits. Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Configurable platform. Verified 2026-08-19.
- [Inspect AI](https://inspect.aisi.org.uk/) | Agent and sandbox evals. Verified 2026-08-19.
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | Academic benchmarks. Verified 2026-08-19.