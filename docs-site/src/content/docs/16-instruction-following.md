---
title: "Instruction-Following Evaluation"
description: "How to measure whether a model honors formatting and content constraints."
---

## What It Measures

Instruction-following evaluation measures whether a model obeys explicit, objectively verifiable constraints in a prompt: word counts, JSON formatting, keyword repetition, section structure, and similar rules. The benchmark prompt embeds one or more verifiable instructions, and a deterministic program checks compliance. Success is the fraction of instructions followed, computed strictly (all constraints in the prompt must hold) and loosely (partial credit per instruction) ([IFEval](https://arxiv.org/abs/2311.07911)).

## What It Is Used For

- Build one when the product depends on structured output: JSON-only responses, agents that must follow workflow steps, formatting rules, or content constraints.
- IFEval is the standard benchmark: 541 prompts with 25 verifiable instruction types ([IFEval](https://arxiv.org/abs/2311.07911)).
- FollowBench scales the constraint count from 1 to 5 levels per instruction and scores satisfaction rate ([FollowBench](https://arxiv.org/abs/2310.20410)).
- InfoBench decomposes each instruction into yes/no sub-requirements and scores the fraction met ([InfoBench](https://arxiv.org/abs/2401.03601)).
- It is one of the core benchmarks in the [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) and is fully deterministic, so no judge bias.

## Typical Grader / Metric

- Instruction-level strict accuracy and loose accuracy, computed by rule-based verification.
- Prompt-level accuracy: all instructions in a prompt must hold.
- FollowBench adds hard satisfaction rate (HSR), soft satisfaction rate (SSR), and consistent satisfaction levels (CSL) ([FollowBench](https://arxiv.org/abs/2310.20410)).
- InfoBench reports the decomposed requirements following ratio (DRFR), judged by a GPT-4-0314 model answering yes/no questions ([InfoBench](https://arxiv.org/abs/2401.03601)).
- IFEval is automatic and deterministic; no judge model. FollowBench and InfoBench need a judge model for open-ended instructions.

## Build Complexity

**Low**. Reason: the prompt set is public, scoring is a deterministic verifier, and there is no judge model dependency. The main work is writing the verification functions.

## What You Would Build

- Load the IFEval prompt set.
- Run generation per prompt.
- Verify each instruction with a deterministic checker (word count, regex, keyword match, JSON parse).
- Report strict and loose accuracy at instruction and prompt level.

## Related Benchmarks

- [IFEval](https://arxiv.org/abs/2311.07911), [FollowBench](https://arxiv.org/abs/2310.20410), [InfoBench](https://arxiv.org/abs/2401.03601), [The Instruction Hierarchy](https://arxiv.org/abs/2404.13208) in [Benchmarks directory](/04-benchmarks-directory/).

## Related Tools

- [lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md) implements the IFEval task.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) ships IFEval configurations.

## Contamination and Bias Notes

- IFEval is English-only; multilingual instructions and script-specific rules are still under-served, and translated versions remain a research area.
- IFEval is now a well-known public benchmark, so models may be trained to pass its verifier directly (eval-awareness).
- Verifiable instructions can be gamed; verify the checker rather than the output when scores are surprisingly high.
- Judge-based variants (FollowBench, InfoBench) inherit the length and position biases of LLM judges.

## References

- [IFEval](https://arxiv.org/abs/2311.07911) | 541 prompts, 25 verifiable instruction types. Verified 2026-08-19.
- [FollowBench](https://arxiv.org/abs/2310.20410) | Multi-level constraints, HSR/SSR/CSL. Verified 2026-08-19.
- [InfoBench](https://arxiv.org/abs/2401.03601) | Decomposed requirement tracking, DRFR. Verified 2026-08-19.
- [The Instruction Hierarchy](https://arxiv.org/abs/2404.13208) | Privilege ordering and robustness suite. Verified 2026-08-19.
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) | Runs IFEval among its six benchmarks. Verified 2026-08-20.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Benchmark platform. Verified 2026-08-19.
- [lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md) | Task catalog. Verified 2026-08-19.