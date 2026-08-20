import { useId } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
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
import { outcomeComposition } from "@/lib/mathStats";
import { pct } from "@/lib/series";
import type { MathMetric } from "@/lib/types";

interface Props {
  metrics: MathMetric[];
  className?: string;
}

const OUTCOME_COLORS = {
  correct: "var(--eval-accent)",
  wrong: "var(--destructive)",
  unparsed: "var(--muted-foreground)",
};

export function MathOutcomeChart({ metrics, className }: Props) {
  const data = outcomeComposition(metrics).map((o) => ({
    name: o.name,
    correct: o.correct,
    wrong: o.wrong,
    unparsed: o.unparsed,
    label: pct(o.accuracy),
  }));

  const config: ChartConfig = {
    correct: { label: "Correct", color: OUTCOME_COLORS.correct },
    wrong: { label: "Wrong", color: OUTCOME_COLORS.wrong },
    unparsed: { label: "Unparsed", color: OUTCOME_COLORS.unparsed },
  };

  const id = useId().replace(/:/g, "");

  const maxY = Math.max(...data.map((d) => d.correct + d.wrong + d.unparsed), 1);

  return (
    <ChartContainer config={config} className={className} id={id}>
      <BarChart data={data} margin={{ top: 20, right: 16, bottom: 8, left: 4 }}>
        <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
        <XAxis
          dataKey="name"
          tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
          stroke="var(--border)"
        />
        <YAxis
          domain={[0, maxY + 1]}
          allowDecimals={false}
          tick={{ fill: "var(--muted-foreground)", fontSize: 11 }}
          stroke="var(--border)"
        />
        <ChartTooltip
          content={
            <ChartTooltipContent
              formatter={(value, _name, item) => {
                const p = item?.payload as
                  | { correct: number; wrong: number; unparsed: number }
                  | undefined;
                if (!p) return String(value);
                const total = p.correct + p.wrong + p.unparsed;
                return `${value} (${pct(Number(value) / total)})`;
              }}
            />
          }
        />
        <Legend content={<ChartLegendContent />} />
        <Bar
          dataKey="correct"
          stackId="a"
          fill={OUTCOME_COLORS.correct}
          radius={[0, 0, 0, 0]}
        >
          <LabelList
            dataKey="label"
            position="top"
            fill="var(--muted-foreground)"
            fontSize={11}
          />
        </Bar>
        <Bar
          dataKey="wrong"
          stackId="a"
          fill={OUTCOME_COLORS.wrong}
          radius={[0, 0, 0, 0]}
        />
        <Bar
          dataKey="unparsed"
          stackId="a"
          fill={OUTCOME_COLORS.unparsed}
          radius={[0, 0, 4, 4]}
        />
      </BarChart>
    </ChartContainer>
  );
}