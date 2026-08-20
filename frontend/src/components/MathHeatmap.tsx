import { useMemo } from "react";

import { bucketAccuracy } from "@/lib/mathStats";
import { pct } from "@/lib/series";
import type { MathExampleRow, MathMetric } from "@/lib/types";

const HEAT_ACCENT = "var(--eval-accent)";
const HEAT_BG = "var(--background)";

function heatStyle(acc: number, n: number) {
  if (n === 0) {
    return { background: "transparent", color: "var(--muted-foreground)" };
  }
  return {
    background: `color-mix(in oklch, ${HEAT_ACCENT} ${Math.round(10 + acc * 80)}%, ${HEAT_BG})`,
    color: acc >= 0.55 ? "oklch(0.16 0.03 165)" : "var(--muted-foreground)",
  };
}

function titleCase(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

interface Props {
  rowsByModel: Record<string, MathExampleRow[]>;
  models: MathMetric[];
  className?: string;
}

export function MathHeatmap({ rowsByModel, models, className }: Props) {
  const buckets = useMemo(
    () => bucketAccuracy(rowsByModel, "category"),
    [rowsByModel],
  );
  const cats = useMemo(
    () => [
      ...new Set(
        Object.values(rowsByModel)
          .flat()
          .map((r) => r.category)
          .filter((c): c is string => !!c),
      ),
    ],
    [rowsByModel],
  );

  return (
    <div className={className}>
      <div
        className="grid"
        style={{ gridTemplateColumns: `160px repeat(${cats.length}, 1fr)` }}
      >
        <div className="p-2 text-xs font-medium text-muted-foreground" />
        {cats.map((c) => (
          <div
            key={c}
            className="truncate p-2 text-center text-xs font-medium text-muted-foreground"
          >
            {titleCase(c)}
          </div>
        ))}
        {models.map((m) => (
          <div key={m.model_id} className="contents">
            <div className="flex items-center gap-2 p-2 text-xs text-foreground">
              <span
                className="inline-block h-2 w-2 shrink-0 rounded-full"
                style={{ background: m.color }}
              />
              {m.name}
            </div>
            {cats.map((c) => {
              const cell = buckets[m.model_id]?.[c];
              const acc = cell?.accuracy ?? 0;
              const n = cell?.total ?? 0;
              const style = heatStyle(acc, n);
              return (
                <div
                  key={c}
                  className="flex items-center justify-center gap-1 rounded p-2 text-xs"
                  style={style}
                >
                  <span className="tabular-nums">{pct(acc)}</span>
                  <span className="opacity-60">·{n}</span>
                </div>
              );
            })}
          </div>
        ))}
      </div>
      <div className="mt-3 flex items-center gap-2 text-[10px] text-muted-foreground">
        <span>Low</span>
        <div
          className="h-2 flex-1 rounded"
          style={{
            background: `linear-gradient(to right, color-mix(in oklch, ${HEAT_ACCENT} 10%, ${HEAT_BG}), color-mix(in oklch, ${HEAT_ACCENT} 90%, ${HEAT_BG}))`,
          }}
        />
        <span>High</span>
      </div>
    </div>
  );
}
