// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'LLM Evaluation — A Field Guide',
			description:
				'A complete, sourced guide to evaluating language models: types, how labs evaluate, what benchmarks reveal, the tools companies use, and example eval projects.',
			customCss: ['./src/styles/custom.css'],
			sidebar: [
				{
					label: 'Introduction',
					items: [
						{ label: 'Overview', link: '/' },
						{ label: 'What is evaluation?', slug: '01-what-is-evaluation' },
						{ label: 'Types of evals', slug: '02-types-of-evals' },
					],
				},
				{
					label: 'Landscape',
					items: [
						{ label: 'How labs evaluate', slug: '03-labs' },
						{ label: 'Benchmarks directory', slug: '04-benchmarks-directory' },
						{ label: 'Tools', slug: '05-tools' },
					],
				},
				{
					label: 'Practice',
					items: [
						{ label: 'How to build evals', slug: '06-how-to-build-evals' },
						{ label: 'Case studies', slug: '07-case-studies' },
						{ label: 'Glossary', slug: '08-glossary' },
					],
				},
				{
					label: 'The Ten Evaluation Types',
					items: [
						{ label: 'Capability & knowledge', slug: '09-capability-knowledge' },
						{ label: 'Reasoning & math', slug: '10-reasoning-math' },
						{ label: 'Code generation', slug: '11-code-generation' },
						{ label: 'Long context', slug: '12-long-context' },
						{ label: 'RAG faithfulness', slug: '13-rag-faithfulness' },
						{ label: 'Safety & refusal', slug: '14-safety-refusal' },
						{ label: 'Preference alignment', slug: '15-preference-alignment' },
						{ label: 'Instruction following', slug: '16-instruction-following' },
						{ label: 'LLM-as-a-judge', slug: '17-llm-as-judge' },
						{ label: 'Multilingual', slug: '18-multilingual' },
            { label: 'Tools and Agents', slug: '19-tools-and-agents' },
						{ label: 'Pass K Reliability', slug: '20-pass-k-reliability' },
					],
				},
			],
		}),
	],
});
