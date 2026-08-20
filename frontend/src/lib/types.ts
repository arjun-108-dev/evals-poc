export interface ModelMeta {
  id: string;
  ollama: string;
  name: string;
  size: string;
  csv: string;
  color: string;
  notes?: string;
}

export interface Metric {
  model_id: string;
  name: string;
  size: string;
  color: string;
  n_examples: number;
  n_should_call: number;
  n_should_not_call: number;
  tool_accuracy: number;
  call_accuracy: number;
  arg_accuracy: number;
  abstain_accuracy: number;
  format_validity: number;
  false_positive_rate: number;
  overall_score: number;
  avg_latency_ms: number;
  n_tool_correct: number;
  n_call_correct: number;
  n_arg_correct: number;
  n_false_positive: number;
}

export interface ExampleRow {
  id: string;
  prompt: string;
  expected_tool: string;
  expected_args: string;
  model_output: string;
  parsed_tool: string;
  parsed_args: string;
  tool_correct: boolean;
  args_correct: boolean;
  format_valid: boolean;
  false_positive: boolean;
  latency_ms: number;
  error: string;
  category?: string;
  difficulty?: string;
}

export interface DatasetExample {
  id: string;
  prompt: string;
  expected_tool: string;
  expected_args: Record<string, unknown> | null;
  category: string;
  difficulty: string;
}

export type MetricKey =
  | "overall_score"
  | "call_accuracy"
  | "arg_accuracy"
  | "abstain_accuracy"
  | "false_positive_rate"
  | "avg_latency_ms";
