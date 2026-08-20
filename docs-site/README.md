# LLM Evaluation Field Guide — Docs Site

The documentation site for the [evals POC](../README.md). A sourced, navigable field guide to **model evaluation**: what evals are, the types, how public labs actually evaluate, what benchmarks and tools reveal, and concrete example eval projects (including the tool-calling + math POC in this repo).

Live at **https://evals-poc.arjun-90c.workers.dev/**

![Built with Starlight](https://astro.badg.es/v2/built-with-starlight/tiny.svg)

## Content

The site is organized into four sections:

| Section | Pages |
|---------|-------|
| **Introduction** | Overview, what is evaluation, types of evals |
| **Landscape** | How labs evaluate (OpenAI, Anthropic, Google DeepMind, Meta, Moonshot/Kimi, DeepSeek, Mistral), benchmarks directory, tools |
| **Practice** | How to build evals, case studies, glossary |
| **The Ten Evaluation Types** | Capability & knowledge, reasoning & math, code generation, long context, RAG faithfulness, safety & refusal, preference alignment, instruction following, LLM-as-judge, multilingual — plus tools & agents and pass^k reliability |

Each curated page acts as a deep dive on a real evaluation type — what it measures, how it's typically run, and what it highlights — grounded in public sources and cited throughout.

## Stack

Astro 7 · Starlight · Tailwind v4 (dark by default) · auto sidebar + on-page TOC

## Local Dev

```bash
pnpm install
pnpm dev        # dev server at localhost:4321
```

| Command | Action |
|---------|--------|
| `pnpm dev` | Start local dev server |
| `pnpm build` | Build the production site to `dist/` |
| `pnpm preview` | Preview the build locally |

The docs content lives in `src/content/docs/` as plain Markdown (with frontmatter for ordering/titles), configured via `src/content.config.ts` and the sidebar in `astro.config.mjs`.