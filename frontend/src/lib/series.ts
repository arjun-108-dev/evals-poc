import type { MathMetric, Metric } from "./types";

/** Minimal shape shared by every metric row (tool + math evals). */
export interface MetricLike {
  model_id: string;
  name: string;
  size: string;
  color: string;
  overall_score: number;
}

/** Accent reserved for the single best-performing model (teal/green). */
export const ACCENT = "var(--eval-accent)";

/** Neutral gray ramp for every other model — theme-consistent, dark-mode safe. */
const GRAYS = [
  "color-mix(in oklch, var(--foreground) 72%, var(--background))",
  "color-mix(in oklch, var(--foreground) 56%, var(--background))",
  "color-mix(in oklch, var(--foreground) 42%, var(--background))",
  "color-mix(in oklch, var(--foreground) 30%, var(--background))",
];

export const pct = (v: number) => `${Math.round(v * 100)}%`;

export function bestModelId<T extends MetricLike>(metrics: T[]): string {
  return [...metrics].sort((a, b) => b.overall_score - a.overall_score)[0]
    .model_id;
}

export function worstModelId<T extends MetricLike>(metrics: T[]): string {
  return [...metrics].sort((a, b) => a.overall_score - b.overall_score)[0]
    .model_id;
}

/** Map of model_id -> series color (accent for best, gray otherwise). */
export function modelColors<T extends MetricLike>(
  metrics: T[],
): Record<string, string> {
  const best = bestModelId(metrics);
  let g = 0;
  const out: Record<string, string> = {};
  for (const m of metrics) {
    out[m.model_id] = m.model_id === best ? ACCENT : GRAYS[g++ % GRAYS.length];
  }
  return out;
}

/** Parse a size label like "1.5B" / "270M" into billions of params. */
export function paramCount(size: string): number {
  const n = parseFloat(size);
  if (Number.isNaN(n)) return 0;
  return size.toLowerCase().includes("b") ? n : n / 1000;
}

export const SUB_SCORES: { key: keyof Metric; label: string }[] = [
  { key: "call_accuracy", label: "Call" },
  { key: "arg_accuracy", label: "Arg" },
  { key: "abstain_accuracy", label: "Abstain" },
  { key: "format_validity", label: "Format" },
];

export const MATH_SUB_SCORES: { key: keyof MathMetric; label: string }[] = [
  { key: "accuracy", label: "Accuracy" },
  { key: "parse_rate", label: "Parse" },
];
