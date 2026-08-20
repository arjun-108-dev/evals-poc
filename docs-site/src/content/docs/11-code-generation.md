---
title: "Code Generation Evaluation"
description: "How to measure whether a model writes correct programs."
---

## What It Measures

Code generation evaluation measures whether a model produces programs that satisfy a specification. The item is a natural-language prompt plus, optionally, function signatures and test cases; the model must emit code that passes hidden or held-out tests. Units range from single functions (HumanEval, MBPP) to complete library-aware tasks (BigCodeBench) to real GitHub issue resolutions across entire repositories (SWE-bench). Success is the pass rate over generated samples, reported as pass@k ([HumanEval](https://arxiv.org/abs/2107.03374); [BigCodeBench](https://arxiv.org/abs/2406.15877); [SWE-bench](https://arxiv.org/abs/2310.06770)).

## What It Is Used For

- Build one when the product generates or edits code, powers coding agents, or autocompletes.
- HumanEval and MBPP are the standard function-level baselines ([HumanEval](https://arxiv.org/abs/2107.03374); [MBPP](https://arxiv.org/abs/2108.07732)).
- BigCodeBench adds library-aware calls to 139 real Python libraries ([BigCodeBench](https://arxiv.org/abs/2406.15877)).
- LiveCodeBench samples competitive problems dated after the model release to stay contamination-free ([LiveCodeBench](https://arxiv.org/abs/2403.07974)).
- SWE-bench and SWE-bench Pro measure long-horizon repository tasks and drive agent development ([SWE-bench](https://arxiv.org/abs/2310.06770); [SWE-bench Pro](https://arxiv.org/abs/2509.16941)).
- SWE-bench Verified is the human-audited 500-task subset favored in model releases ([SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)).

## Typical Grader / Metric

- pass@k, computed from sampled completions checked against hidden unit tests.
- SWE-bench measures the percentage of GitHub issues resolved, verified by the patch test suite.
- CodeContests uses n@k solve rate on competitive problems ([CodeContests](https://arxiv.org/abs/2203.07814)).
- Fully automatic; requires a sandbox runtime, not a judge model.

## Build Complexity

**High**. Reason: you need a large curated problem set, hidden tests, and a sandboxed executor that can run untrusted code safely. Repository-level evals (SWE-bench) additionally require environment provisioning and patch application logic.

## What You Would Build

- Select or curate problems with gold tests.
- Sample k completions per problem under a fixed prompt template.
- Run each completion inside an isolated sandbox (Docker or similar).
- Evaluate with hidden unit tests.
- Report pass@1 and pass@k, computed over samples.

For a repository-level eval:

- Fetch a real issue, its base commit, and its test patch.
- Have the model produce a patch or full edit.
- Apply the patch, run the added tests, and record pass or fail ([SWE-bench](https://arxiv.org/abs/2310.06770)).

## Related Benchmarks

- Function level: [HumanEval](https://arxiv.org/abs/2107.03374), [MBPP](https://arxiv.org/abs/2108.07732), [BigCodeBench](https://arxiv.org/abs/2406.15877).
- Competitive and fresh: [LiveCodeBench](https://arxiv.org/abs/2403.07974), [CodeContests](https://arxiv.org/abs/2203.07814).
- Repository level: [SWE-bench](https://arxiv.org/abs/2310.06770), [SWE-bench Pro](https://arxiv.org/abs/2509.16941), [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) in [Benchmarks directory](/04-benchmarks-directory/).

## Related Tools

- [Inspect AI](https://inspect.aisi.org.uk/) has built-in bash and sandboxing primitives for code evals, plus a dedicated code evaluation tutorial.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) ships code evaluation configs and Docker-based evaluation services.
- lm-evaluation-harness supports generate_until tasks for code benchmarks ([lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md)).

## Contamination and Bias Notes

- HumanEval-style problems and their solutions are widely believed to be in substantial portions of training corpora; LiveCodeBench exists specifically because of this ([LiveCodeBench](https://arxiv.org/abs/2403.07974)).
- Evaluate on dated problems and prefer benchmarks that ship release-date guarantees.
- Code evals are overwhelmingly Python and English-only; coverage of other languages and natural-language specs is thin.

## References

- [HumanEval](https://arxiv.org/abs/2107.03374) | 164 handwritten Python problems. Verified 2026-08-19.
- [MBPP](https://arxiv.org/abs/2108.07732) | 974 crowd-sourced Python tasks. Verified 2026-08-19.
- [BigCodeBench](https://arxiv.org/abs/2406.15877) | 1,140 library-aware tasks. Verified 2026-08-19.
- [LiveCodeBench](https://arxiv.org/abs/2403.07974) | Contamination-free by date. Verified 2026-08-19.
- [CodeContests](https://arxiv.org/abs/2203.07814) | Competitive programming. Verified 2026-08-19.
- [SWE-bench](https://arxiv.org/abs/2310.06770) | 2,294 GitHub issues. Verified 2026-08-19.
- [SWE-bench Pro](https://arxiv.org/abs/2509.16941) | 1,865 long-horizon issues. Verified 2026-08-19.
- [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) | 500 human-validated issues. Verified 2026-08-19.
- [OpenCompass](https://opencompass.readthedocs.io/en/stable/) | Benchmark platform. Verified 2026-08-19.
- [Inspect AI](https://inspect.aisi.org.uk/) | Configurable eval framework. Verified 2026-08-19.
- [lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md) | Task catalog. Verified 2026-08-19.