# Plan: In-Depth LLM Evaluation Documentation

## Goal
Build a polished, well-sourced knowledge base on **model evaluation** — what evals are,
the types, how public labs actually evaluate, what each benchmark/tool reveals, and
concrete example eval projects (featuring the existing tiny tool-calling POC plus
blueprints for more). Delivered as a multi-page `docs/` knowledge base **and** an
Astro documentation website that renders it.

## Deliverables
1. `PLAN.md` (this file) — the approved plan.
2. `docs/` — the canonical markdown documentation (8 pages).
3. `docs-site/` — an Astro website that renders `docs/*.md` as a navigable, dark,
   professional docs site (sidebar + per-page TOC + Mermaid diagrams).

## Documentation structure (`docs/`)
```
docs/
├── README.md                 # Landing: TOC, navigation, exec summary, how to use
├── 01-what-is-evaluation.md  # Definition, why it matters, terminology, eval lifecycle diagram
├── 02-types-of-evals.md      # Taxonomy + what each type highlights (table + mermaid)
├── 03-labs.md                # How public labs evaluate (OpenAI, Anthropic, Google DeepMind,
│                             #   Meta, Moonshot AI/Kimi, DeepSeek, Mistral)
├── 04-benchmarks-directory.md # Catalog of benchmarks → what each highlights (table)
├── 05-tools.md               # Tools companies use (capability harnesses, app-eval, observability)
├── 06-how-to-build-evals.md  # Practical playbook + pitfalls
├── 07-case-studies.md        # Example eval projects (tiny tool-calling POC flagship + blueprints)
└── 08-glossary.md            # Terms
```

## Astro website (`docs-site/`)
- Built with **Astro 5** (manually scaffolded, no interactive prompts).
- Reads the canonical markdown from `../docs` via an Astro **content collection**
  (`glob` loader from `astro/loaders`), so the website and `docs/` never drift.
- Styling: Tailwind v4 (`@tailwindcss/vite`), dark mode by default, responsive.
- Navigation: auto-generated left sidebar from frontmatter `order`/`title`; right-hand
  on-page table of contents.
- Diagrams: Mermaid via CDN + a small client script (graceful fallback to a code block
  if Mermaid is unavailable).
- Pages: `/` (README) and `/<slug>/` for each doc.
- Verification: `pnpm install` + `pnpm build` must succeed; `pnpm dev` serves locally.

## Key content (grounded in public sources)
- **Labs (`03-labs.md`)**:
  - *OpenAI*: `openai/evals` + `simple-evals` (zero-shot CoT), external **red teaming**
    (mixed manual/automated, threat modeling → automated evals), and **production
    evaluations** from de-identified ChatGPT traffic + CoT monitors to defeat evaluation
    awareness (alignment.openai.com/prod-evals).
  - *Moonshot AI / Kimi*: K2 tech report — large-scale **agentic data synthesis**
    (ACEBench-inspired, thousands of tools/MCP), general RL with self-judging; benchmarks
    τ²-Bench / AceBench / SWE-bench; plus the **K2 Vendor Verifier** (`tool_call_f1`,
    `schema_accuracy`) — a real tool-calling eval.
  - *Anthropic, Google DeepMind, Meta, DeepSeek, Mistral*: publicly documented practices
    (constitutional/RLHF evals, internal capability suites, technical reports,
    OpenCompass/HELM numbers) and what each emphasizes.
- **Benchmarks (`04`)**: MMLU/MMLU-Pro, GPQA, MATH/AIME, HumanEval, SWE-bench,
  τ²-Bench/AceBench (tool use), IFEval, SimpleQA, TruthfulQA, ToxiGen/BBQ,
  Chatbot Arena/LMArena, HELM — each with "measures / highlights / blind spots".
- **Tools (`05`)**: capability harnesses (`lm-evaluation-harness`, HELM, OpenCompass,
  UK AISI **Inspect AI**); app-eval (Ragas, DeepEval, Promptfoo, Giskard);
  observability+evals (LangSmith, W&B Weave, Braintrust, Phoenix, Langfuse, Helicone);
  lab-specific (OpenAI Evals, Kimi K2 Vendor Verifier). Comparison table: layer / license
  / shape / when to use.
- **Case studies (`07`)**: the existing POC (`data/`, `evaluator/run_eval.py`,
  `graders.py`, `analyze.py`) as the flagship worked example of deterministic
  tool-calling grading; plus blueprints for RAG faithfulness, safety red-team, IFEval,
  and coding eval projects.

## Execution order
1. `PLAN.md` (root).
2. `docs/` pages 01–08 (with frontmatter for the site).
3. `docs-site/` Astro scaffold (package.json, astro.config, content config, layout, pages).
4. Style (dark, sidebar, TOC, Mermaid).
5. `pnpm install` + `pnpm build`; fix errors; confirm `pnpm dev` works.

## Constraints
- Documentation only touches markdown + the Astro site; the existing POC code is
  referenced, not modified.
- All claims cite the public sources gathered (OpenAI papers/blog, Kimi K2 report +
  K2 Vendor Verifier, HELM/OpenCompass/lm-eval-harness docs, LangSmith/Inspect/
  Promptfoo/Ragas pages).
