import { useId } from "react";
import {
  CartesianGrid,
  ReferenceArea,
  ReferenceLine,
  Scatter,
  ScatterChart,
  XAxis,
  YAxis,
  ZAxis,
} from "recharts";

import type { ChartConfig } from "@/components/ui/chart";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { modelColors, paramCount, type MetricLike } from "@/lib/series";

interface Props<T extends MetricLike> {
  metrics: T[];
  xKey: keyof T;
  yKey: keyof T;
  xLabel: string;
  yLabel: string;
  xFormat?: (v: number) => string;
  yFormat?: (v: number) => string;
  /** vertical guide line value (marks good/bad boundary on x) */
  xGuide: number;
  /** horizontal guide line value (marks good/bad boundary on y) */
  yGuide: number;
  xDomain: [number, number];
  yDomain: [number, number];
  className?: string;
  goodZone?: "top-left" | "top-right";
}

export function TradeoffScatterChart<T extends MetricLike>({
  metrics,
  xKey,
  yKey,
  xLabel,
  yLabel,
  xFormat = (v) => `${v}`,
  yFormat = (v) => `${v}`,
  xGuide,
  yGuide,
  xDomain,
  yDomain,
  className,
  goodZone = "top-left",
}: Props<T>) {
  const colors = modelColors(metrics);
  const maxParams = Math.max(...metrics.map((m) => paramCount(m.size)));
  const zone =
    goodZone === "top-left"
      ? { x1: xDomain[0], x2: xGuide, labelPos: "insideTopLeft" as const }
      : { x1: xGuide, x2: xDomain[1], labelPos: "insideTopRight" as const };

  const data = metrics.map((m) => ({
    name: m.name,
    x: m[xKey] as number,
    y: m[yKey] as number,
    params: paramCount(m.size),
    fill: colors[m.model_id],
  }));

  const config = metrics.reduce<ChartConfig>((acc, m) => {
    acc[m.model_id] = { label: m.name, color: colors[m.model_id] };
    return acc;
  }, {});

  const id = useId().replace(/:/g, "");

  return (
    <ChartContainer config={config} className={className} id={id}>
      <ScatterChart margin={{ top: 12, right: 16, bottom: 8, left: 4 }}>
        <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
        <ReferenceArea
          x1={zone.x1}
          x2={zone.x2}
          y1={yGuide}
          y2={yDomain[1]}
          fill="var(--muted-foreground)"
          fillOpacity={0.07}
          stroke="none"
          label={{
            value: "good zone",
            position: zone.labelPos,
            fill: "var(--muted-foreground)",
            fontSize: 10,
          }}
        />
        <XAxis
          type="number"
          dataKey="x"
          domain={xDomain}
          tickFormatter={xFormat}
          tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
          stroke="var(--border)"
          label={{
            value: xLabel,
            position: "insideBottom",
            offset: -2,
            fill: "var(--muted-foreground)",
            fontSize: 11,
          }}
        />
        <YAxis
          type="number"
          dataKey="y"
          domain={yDomain}
          tickFormatter={yFormat}
          tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
          stroke="var(--border)"
          label={{
            value: yLabel,
            angle: -90,
            position: "insideLeft",
            fill: "var(--muted-foreground)",
            fontSize: 11,
          }}
        />
        <ZAxis
          type="number"
          dataKey="params"
          range={[80, 520]}
          domain={[0, maxParams]}
        />
        <ReferenceLine
          x={xGuide}
          stroke="var(--muted-foreground)"
          strokeDasharray="4 4"
          strokeOpacity={0.5}
        />
        <ReferenceLine
          y={yGuide}
          stroke="var(--muted-foreground)"
          strokeDasharray="4 4"
          strokeOpacity={0.5}
        />
        <ChartTooltip
          cursor={{ strokeDasharray: "3 3", stroke: "var(--muted-foreground)" }}
          content={
            <ChartTooltipContent
              labelFormatter={(_label, payload) =>
                (payload?.[0]?.payload?.name as string) ?? ""
              }
              formatter={(value, _name, item) =>
                (item?.dataKey === "x"
                  ? xFormat(Number(value))
                  : yFormat(Number(value)))
              }
            />
          }
        />
        <Scatter
          data={data}
          fill="var(--muted-foreground)"
          stroke="var(--border)"
          strokeWidth={1}
          label={(props: any) => {
            if (props.cx == null || props.cy == null || !props.payload?.name)
              return null;
            return (
              <text
                x={props.cx + 8}
                y={props.cy - 8}
                className="fill-current"
                style={{
                  fontSize: 10,
                  fontWeight: 600,
                  fill: props.payload.fill,
                }}
              >
                {props.payload.name}
              </text>
            );
          }}
        />
      </ScatterChart>
    </ChartContainer>
  );
}
