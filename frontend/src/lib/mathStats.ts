import type { MathExampleRow, MathMetric } from "./types";

export type DimensionKey = "category" | "difficulty";

export interface BucketCell {
  total: number;
  correct: number;
  accuracy: number;
}

/** Accuracy per (model, dimension value) bucket, derived from per-example rows. */
export function bucketAccuracy(
  rowsByModel: Record<string, MathExampleRow[]>,
  groupKey: DimensionKey,
): Record<string, Record<string, BucketCell>> {
  const out: Record<string, Record<string, BucketCell>> = {};
  for (const [modelId, rows] of Object.entries(rowsByModel)) {
    const buckets: Record<string, BucketCell> = {};
    for (const r of rows) {
      const key = r[groupKey] ?? "unknown";
      const cell = (buckets[key] ??= { total: 0, correct: 0, accuracy: 0 });
      cell.total += 1;
      if (r.answer_correct) cell.correct += 1;
    }
    for (const key of Object.keys(buckets)) {
      buckets[key].accuracy = buckets[key].total
        ? buckets[key].correct / buckets[key].total
        : 0;
    }
    out[modelId] = buckets;
  }
  return out;
}

/** Ordered list of dimension values present in the rows, preferred order first. */
export function dimensionOrder(
  rowsByModel: Record<string, MathExampleRow[]>,
  groupKey: DimensionKey,
  preferred: string[],
): string[] {
  const seen = new Set<string>();
  for (const rows of Object.values(rowsByModel)) {
    for (const r of rows) {
      const k = r[groupKey];
      if (k) seen.add(k);
    }
  }
  return [
    ...preferred.filter((v) => seen.has(v)),
    ...[...seen].filter((v) => !preferred.includes(v)),
  ];
}

export interface OutcomeRow {
  model_id: string;
  name: string;
  color: string;
  size: string;
  correct: number;
  wrong: number;
  unparsed: number;
  accuracy: number;
}

/** Split each model's aggregate counts into correct / wrong / unparsed. */
export function outcomeComposition(metrics: MathMetric[]): OutcomeRow[] {
  return metrics.map((m) => {
    const wrong = m.n_parsed - m.n_correct;
    const unparsed = m.n_examples - m.n_parsed;
    return {
      model_id: m.model_id,
      name: m.name,
      color: m.color,
      size: m.size,
      correct: m.n_correct,
      wrong,
      unparsed,
      accuracy: m.n_examples ? m.n_correct / m.n_examples : 0,
    };
  });
}
