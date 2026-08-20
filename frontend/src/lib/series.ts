import type { Metric } from "./types";

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

export function bestModelId(metrics: Metric[]): string {
  return [...metrics].sort((a, b) => b.overall_score - a.overall_score)[0]
    .model_id;
}

export function worstModelId(metrics: Metric[]): string {
  return [...metrics].sort((a, b) => a.overall_score - b.overall_score)[0]
    .model_id;
}

/** Map of model_id -> series color (accent for best, gray otherwise). */
export function modelColors(metrics: Metric[]): Record<string, string> {
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
