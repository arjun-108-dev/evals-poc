import { useId } from "react";
import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
} from "recharts";

import type { ChartConfig } from "@/components/ui/chart";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { modelColors, pct, SUB_SCORES, type MetricLike } from "@/lib/series";

interface Props<T extends MetricLike> {
  metrics: T[];
  className?: string;
  showLabels?: boolean;
  subScores?: { key: keyof T; label: string }[];
}

export function MetricRadarChart<T extends MetricLike>({
  metrics,
  className,
  showLabels = true,
  subScores = SUB_SCORES as unknown as { key: keyof T; label: string }[],
}: Props<T>) {
  const colors = modelColors(metrics);
  const bestId = [...metrics].sort(
    (a, b) => b.overall_score - a.overall_score,
  )[0].model_id;

  const data = subScores.map((s) => {
    const row: Record<string, number | string> = { metric: s.label };
    for (const m of metrics) row[m.model_id] = m[s.key] as number;
    return row;
  });

  const config = metrics.reduce<ChartConfig>((acc, m) => {
    acc[m.model_id] = { label: m.name, color: colors[m.model_id] };
    return acc;
  }, {});

  const id = useId().replace(/:/g, "");

  return (
    <ChartContainer
      config={config}
      className={className}
      id={id}
    >
      <RadarChart data={data} outerRadius="72%">
        <PolarGrid stroke="var(--border)" />
        <PolarAngleAxis
          dataKey="metric"
          tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
        />
        <PolarRadiusAxis
          domain={[0, 1]}
          tickCount={5}
          tickFormatter={pct}
          tick={{ fill: "var(--muted-foreground)", fontSize: 10 }}
          axisLine={false}
        />
        {metrics.map((m) => {
          const isBest = m.model_id === bestId;
          const color = colors[m.model_id];
          return (
            <Radar
              key={m.model_id}
              name={m.name}
              dataKey={m.model_id}
              stroke={color}
              fill={color}
              fillOpacity={isBest ? 0.28 : 0.05}
              strokeWidth={isBest ? 2.5 : 1.25}
              dot={(props: any) => {
                if (!showLabels || props.index !== 0) return null;
                return (
                  <text
                    x={(props.cx ?? 0) + (isBest ? 6 : 4)}
                    y={(props.cy ?? 0) - (isBest ? 4 : 2)}
                    textAnchor={isBest ? "start" : "start"}
                    className="fill-current"
                    style={{
                      fontSize: isBest ? 11 : 9,
                      fontWeight: isBest ? 700 : 500,
                      fill: color,
                    }}
                  >
                    {m.name}
                  </text>
                );
              }}
            />
          );
        })}
        <ChartTooltip
          content={
            <ChartTooltipContent
              formatter={(value) => pct(Number(value))}
            />
          }
        />
      </RadarChart>
    </ChartContainer>
  );
}
