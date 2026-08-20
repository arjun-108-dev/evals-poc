import Papa from "papaparse";
import type {
  DatasetExample,
  ExampleRow,
  MathDatasetExample,
  MathExampleRow,
  MathMetric,
  Metric,
  ModelMeta,
} from "./types";

const BASE = "/data";

async function getText(path: string): Promise<string> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    throw new Error(`Failed to load ${path} (${res.status})`);
  }
  return res.text();
}

async function getJson<T>(path: string): Promise<T> {
  return JSON.parse(await getText(path)) as T;
}

export async function loadModels(): Promise<ModelMeta[]> {
  const data = await getJson<{ models: ModelMeta[] }>("/models.json");
  return data.models;
}

export async function loadMetrics(): Promise<Metric[]> {
  const text = await getText("/results/summary/metrics.csv");
  const rows = Papa.parse<Record<string, string>>(text, {
    header: true,
    skipEmptyLines: true,
  }).data;
  return rows.map((r) => ({
    model_id: r.model_id,
    name: r.name,
    size: r.size,
    color: r.color,
    n_examples: Number(r.n_examples) || 0,
    n_should_call: Number(r.n_should_call) || 0,
    n_should_not_call: Number(r.n_should_not_call) || 0,
    tool_accuracy: Number(r.tool_accuracy) || 0,
    call_accuracy: Number(r.call_accuracy) || 0,
    arg_accuracy: Number(r.arg_accuracy) || 0,
    abstain_accuracy: Number(r.abstain_accuracy) || 0,
    format_validity: Number(r.format_validity) || 0,
    false_positive_rate: Number(r.false_positive_rate) || 0,
    overall_score: Number(r.overall_score) || 0,
    avg_latency_ms: Number(r.avg_latency_ms) || 0,
    n_tool_correct: Number(r.n_tool_correct) || 0,
    n_call_correct: Number(r.n_call_correct) || 0,
    n_arg_correct: Number(r.n_arg_correct) || 0,
    n_false_positive: Number(r.n_false_positive) || 0,
  }));
}

export async function loadDataset(): Promise<DatasetExample[]> {
  const text = await getText("/eval_dataset.jsonl");
  return text
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l) as DatasetExample);
}

export async function loadModelRows(
  modelId: string,
  dataset: DatasetExample[],
): Promise<ExampleRow[]> {
  const text = await getText(`/results/raw/${modelId}.csv`);
  const rows = Papa.parse<Record<string, string>>(text, {
    header: true,
    skipEmptyLines: true,
  }).data;
  const catById = new Map(dataset.map((d) => [d.id, d]));
  return rows.map((r) => {
    const meta = catById.get(r.id);
    return {
      id: r.id,
      prompt: r.prompt,
      expected_tool: r.expected_tool,
      expected_args: r.expected_args,
      model_output: r.model_output,
      parsed_tool: r.parsed_tool,
      parsed_args: r.parsed_args,
      tool_correct: r.tool_correct === "True",
      args_correct: r.args_correct === "True",
      format_valid: r.format_valid === "True",
      false_positive: r.false_positive === "True",
      latency_ms: Number(r.latency_ms) || 0,
      error: r.error,
      category: meta?.category,
      difficulty: meta?.difficulty,
    };
  });
}

export async function loadMathMetrics(): Promise<MathMetric[]> {
  const text = await getText("/results/summary_math/metrics.csv");
  const rows = Papa.parse<Record<string, string>>(text, {
    header: true,
    skipEmptyLines: true,
  }).data;
  return rows.map((r) => ({
    model_id: r.model_id,
    name: r.name,
    size: r.size,
    color: r.color,
    n_examples: Number(r.n_examples) || 0,
    n_parsed: Number(r.n_parsed) || 0,
    n_correct: Number(r.n_correct) || 0,
    accuracy: Number(r.accuracy) || 0,
    parse_rate: Number(r.parse_rate) || 0,
    overall_score: Number(r.overall_score) || 0,
    avg_latency_ms: Number(r.avg_latency_ms) || 0,
  }));
}

export async function loadMathDataset(): Promise<MathDatasetExample[]> {
  const text = await getText("/math_dataset.jsonl");
  return text
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l) as MathDatasetExample);
}

export async function loadMathModelRows(
  modelId: string,
  dataset: MathDatasetExample[],
): Promise<MathExampleRow[]> {
  const text = await getText(`/results/raw_math/${modelId}.csv`);
  const rows = Papa.parse<Record<string, string>>(text, {
    header: true,
    skipEmptyLines: true,
  }).data;
  const metaById = new Map(dataset.map((d) => [d.id, d]));
  return rows.map((r) => {
    const meta = metaById.get(r.id);
    return {
      id: r.id,
      question: r.question,
      expected_answer: r.expected_answer,
      model_output: r.model_output,
      extracted_answer: r.extracted_answer,
      answer_parsed: r.answer_parsed === "True",
      answer_correct: r.answer_correct === "True",
      latency_ms: Number(r.latency_ms) || 0,
      error: r.error,
      category: meta?.category ?? r.category,
      difficulty: meta?.difficulty ?? r.difficulty,
    };
  });
}
