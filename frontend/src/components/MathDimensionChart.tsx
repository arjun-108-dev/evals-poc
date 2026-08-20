import { useId, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  XAxis,
  YAxis,
} from "recharts";

import type { ChartConfig } from "@/components/ui/chart";
import {
  ChartContainer,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  bucketAccuracy,
  dimensionOrder,
  type DimensionKey,
} from "@/lib/mathStats";
import { pct } from "@/lib/series";
import type { MathExampleRow, MathMetric } from "@/lib/types";

const DIFF_PREFERRED = ["easy", "medium", "hard"];

interface Props {
  rowsByModel: Record<string, MathExampleRow[]>;
  models: MathMetric[];
  className?: string;
  showToggle?: boolean;
}

export function MathDimensionChart({
  rowsByModel,
  models,
  className,
  showToggle = true,
}: Props) {
  const [groupKey, setGroupKey] = useState<DimensionKey>("difficulty");

  const buckets = useMemo(
    () => bucketAccuracy(rowsByModel, groupKey),
    [rowsByModel, groupKey],
  );
  const dims = useMemo(
    () =>
      dimensionOrder(
        rowsByModel,
        groupKey,
        groupKey === "difficulty" ? DIFF_PREFERRED : [],
      ),
    [rowsByModel, groupKey],
  );

  const data = useMemo(
    () =>
      dims.map((d) => {
        const row: Record<string, string | number> = { bucket: d };
        for (const m of models) {
          const cell = buckets[m.model_id]?.[d];
          row[m.model_id] = cell?.accuracy ?? 0;
          row[`${m.model_id}__n`] = cell?.total ?? 0;
        }
        return row;
      }),
    [dims, buckets, models],
  );

  const config: ChartConfig = {};
  for (const m of models) {
    config[m.model_id] = { label: m.name, color: m.color };
  }

  const id = useId().replace(/:/g, "");

  return (
    <div className={className}>
      {showToggle && (
        <div className="mb-3 flex items-center justify-between">
          <p className="text-xs text-muted-foreground">
            Accuracy by{" "}
            {groupKey === "difficulty" ? "difficulty level" : "category"}
          </p>
          <Select
            value={groupKey}
            onValueChange={(v) => setGroupKey(v as DimensionKey)}
          >
            <SelectTrigger size="sm" className="w-36">
              <SelectValue placeholder="Group by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="difficulty">Difficulty</SelectItem>
              <SelectItem value="category">Category</SelectItem>
            </SelectContent>
          </Select>
        </div>
      )}
      <ChartContainer config={config} id={id}>
        <BarChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 4 }}>
          <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
          <XAxis
            dataKey="bucket"
            tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
            stroke="var(--border)"
          />
          <YAxis
            domain={[0, 1]}
            tickFormatter={pct}
            tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
            stroke="var(--border)"
          />
          <ChartTooltip
            content={
              <ChartTooltipContent
                formatter={(value, _name, item) => {
                  const payload = item?.payload as
                    | Record<string, unknown>
                    | undefined;
                  const n = payload
                    ? Number(payload[`${item?.dataKey}__n`])
                    : NaN;
                  return Number.isNaN(n)
                    ? pct(Number(value))
                    : `${pct(Number(value))} · ${n} q`;
                }}
              />
            }
          />
          <Legend content={<ChartLegendContent />} />
          {models.map((m) => (
            <Bar
              key={m.model_id}
              dataKey={m.model_id}
              fill={m.color}
              radius={[4, 4, 0, 0]}
              maxBarSize={40}
            />
          ))}
        </BarChart>
      </ChartContainer>
    </div>
  );
}
