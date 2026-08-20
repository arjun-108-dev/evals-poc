---
title: "Long Context Evaluation"
description: "How to measure whether a model uses information anywhere in a long input."
---

## What It Measures

Long context evaluation measures whether a model can find and use information that is not near the ask, across windows from 4K tokens to well past 1M. Formats include synthetic retrieval (needle-in-a-haystack, RULER), document-grounded QA (LongBench, InfiniteBench), citation-grounded QA (LongCite), and long-horizon application tasks (HELMET). Effective context is what matters: a model may accept a large nominal window while attending reliably only to a much shorter neighborhood. Success is task-specific accuracy or F1 at the stated window length ([LongBench](https://arxiv.org/abs/2308.14508); [HELMET](https://arxiv.org/abs/2410.02694)).

## What It Is Used For

- Build one when the product ingests documents, transcripts, codebases, or logs beyond a few thousand tokens.
- LongBench and LongBench v2 give solid bilingual document tasks ([LongBench](https://arxiv.org/abs/2308.14508); [LongBench v2](https://arxiv.org/abs/2412.15204)).
- InfiniteBench stresses very long (~200K tokens) inputs across five domains ([InfiniteBench](https://arxiv.org/abs/2402.13718)).
- LongCite measures citation-grounded question answering up to 128K tokens ([LongCite](https://arxiv.org/abs/2409.02897)).
- HELMET evaluates seven application-centric categories such as code and long-document usage ([HELMET](https://arxiv.org/abs/2410.02694)).
- BABILong pushes reasoning over synthetic text at up to 10M tokens ([BABILong](https://arxiv.org/abs/2406.10149)).
- NIAH is the community-standard visual sweep of retrieval across length and depth ([NIAH](https://github.com/gkamradt/LLMTest_NeedleInAHaystack)) in [Benchmarks directory](/04-benchmarks-directory/).

## Typical Grader / Metric

- Retrieval accuracy or exact match for needle-style tests.
- Per-task metrics for document tasks: ROUGE-L, F1, similarity, or exact match ([LongBench](https://arxiv.org/abs/2308.14508)).
- Citation F1 under a judge model for grounded QA ([LongCite](https://arxiv.org/abs/2409.02897)).
- HELMET uses LLM-as-judge for open-ended categories and automatic metrics where possible ([HELMET](https://arxiv.org/abs/2410.02694)).
- Most benchmarks mix automatic scoring with a judge model for open-ended answers.

## Build Complexity

**Medium / High**. Reason: the data is expensive because inputs must be much longer than typical examples, and evaluation must control where the target information sits. Judge models are needed for some open-ended tasks, and very-long inputs require significant inference compute.

## What You Would Build

- Pick a task type: synthetic retrieval, long-document QA, citation QA, or full-application.
- Curate or concatenate documents to reach the target window.
- Plant the answer at controlled positions (start, middle, end).
- Prompt with generation or retrieval directives.
- Score per task: exact match for retrieval, F1 or ROUGE-L for QA, citation F1 for grounded answers.

## Related Benchmarks

- [LongBench](https://arxiv.org/abs/2308.14508), [LongBench v2](https://arxiv.org/abs/2412.15204), [InfiniteBench](https://arxiv.org/abs/2402.13718), [LongCite](https://arxiv.org/abs/2409.02897).
- Arc stress tests: [BABILong](https://arxiv.org/abs/2406.10149), [NeedleBench](https://arxiv.org/abs/2407.11963), [NIAH](https://github.com/gkamradt/LLMTest_NeedleInAHaystack).
- Application-centric: [HELMET](https://arxiv.org/abs/2410.02694).
- Multimodal long context: [MMLongBench](https://arxiv.org/abs/2505.10610).

## Related Tools

- [HELM Long Context leaderboard](https://crfm.stanford.edu/helm/long-context/latest/) runs RULER SQuAD, RULER HotPotQA, and InfiniteBench scenarios.
- lm-evaluation-harness implements longbench, babilong, and ruler tasks ([lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md)).

## Contamination and Bias Notes

- RULER-style synthetic retrieval is contamination-resistant but measures only one dimension (information location).
- Document tasks inherited from public corpora can overlap with training data; prefer fresh or licensed corpora.
- English and Chinese dominate long-context benchmarks; other languages are sparse.

## References

- [LongBench](https://arxiv.org/abs/2308.14508) | 21 bilingual tasks across six categories. Verified 2026-08-19.
- [LongBench v2](https://arxiv.org/abs/2412.15204) | 503 English MCQs, up to 2M words. Verified 2026-08-19.
- [InfiniteBench](https://arxiv.org/abs/2402.13718) | ~200K average tokens. Verified 2026-08-19.
- [LongCite](https://arxiv.org/abs/2409.02897) | Citation-grounded QA. Verified 2026-08-19.
- [HELMET](https://arxiv.org/abs/2410.02694) | Application-centric categories. Verified 2026-08-19.
- [BABILong](https://arxiv.org/abs/2406.10149) | Up to 10M tokens. Verified 2026-08-19.
- [NeedleBench](https://arxiv.org/abs/2407.11963) | Bilingual synthetic retrieval. Verified 2026-08-19.
- [MMLongBench](https://arxiv.org/abs/2505.10610) | Multimodal long context. Verified 2026-08-19.
- [HELM Long Context leaderboard](https://crfm.stanford.edu/helm/long-context/latest/) | RULER and InfiniteBench scenarios. Verified 2026-08-19.
- [lm-evaluation-harness tasks README](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/README.md) | Task catalog. Verified 2026-08-19.
- [NIAH](https://github.com/gkamradt/LLMTest_NeedleInAHaystack) | Community retrieval sweep. Verified 2026-08-19.