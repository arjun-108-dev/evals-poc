import { ArrowLeftIcon } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { MetricRadarChart } from "./MetricRadarChart";
import { TradeoffScatterChart } from "./TradeoffScatterChart";
import { MATH_METRIC_INFO } from "@/lib/metricsInfo";
import { MATH_SUB_SCORES, pct } from "@/lib/series";
import type { MathMetric, MathMetricKey } from "@/lib/types";

const ms = (v: number) => `${Math.round(v)}ms`;
const fmtFor = (k: MathMetricKey) => (k === "avg_latency_ms" ? ms : pct);

export function MathMetricDetailPage({
  metricKey,
  metrics,
  onBack,
}: {
  metricKey: MathMetricKey;
  metrics: MathMetric[];
  onBack: () => void;
}) {
  const info = MATH_METRIC_INFO[metricKey];
  const format = fmtFor(metricKey);

  const sorted = [...metrics].sort((a, b) =>
    info.goodDirection === "high"
      ? (b[metricKey] as number) - (a[metricKey] as number)
      : (a[metricKey] as number) - (b[metricKey] as number),
  );
  const best = sorted[0];
  const worst = sorted[sorted.length - 1];

  return (
    <div className="space-y-6">
      <Button variant="ghost" size="sm" onClick={onBack}>
        <ArrowLeftIcon data-icon="inline-start" />
        Back to overview
      </Button>

      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-semibold tracking-tight text-foreground">
            {info.title}
          </h2>
          <Badge variant={info.goodDirection === "high" ? "secondary" : "outline"}>
            {info.goodDirection === "high" ? "higher is better" : "lower is better"}
          </Badge>
        </div>
        <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
          {info.hint}
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">{info.title}</CardTitle>
          <CardDescription>All 5 models on this metric</CardDescription>
        </CardHeader>
        <CardContent>
          {metricKey === "avg_latency_ms" ? (
            <TradeoffScatterChart
              metrics={metrics}
              xKey="avg_latency_ms"
              yKey="overall_score"
              xLabel="Avg Latency (ms)"
              yLabel="Overall Score"
              xFormat={ms}
              yFormat={(v) => v.toFixed(2)}
              xGuide={6000}
              yGuide={0.8}
              xDomain={[0, 18000]}
              yDomain={[0, 1]}
              className="aspect-[16/9] w-full"
            />
          ) : (
            <MetricRadarChart
              metrics={metrics}
              subScores={MATH_SUB_SCORES}
              className="aspect-square mx-auto w-full max-w-md"
            />
          )}
        </CardContent>
      </Card>

      <div className="space-y-4">
        <Section title="What it measures">{info.description}</Section>
        <Separator />
        <Section title="How to read it">{info.howToRead}</Section>
        <Separator />
        <div>
          <h3 className="mb-2 text-sm font-semibold text-foreground">
            Watch for
          </h3>
          <ul className="list-disc space-y-1.5 pl-5 text-sm leading-relaxed text-muted-foreground">
            {info.watchFor.map((w, i) => (
              <li key={i}>{w}</li>
            ))}
          </ul>
        </div>
      </div>

      <div>
        <h3 className="mb-2 text-sm font-semibold text-foreground">
          Per-model values
        </h3>
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent">
              <TableHead className="px-2 py-1.5 text-xs font-medium">Model</TableHead>
              <TableHead className="hidden px-2 py-1.5 text-xs font-medium sm:table-cell">
                Size
              </TableHead>
              <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
                Value
              </TableHead>
              <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
                Rank
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {sorted.map((m, i) => (
              <TableRow key={m.model_id}>
                <TableCell className="px-2 py-1.5">
                  <span className="text-sm font-medium text-foreground">
                    {m.name}
                  </span>
                  {m.model_id === best.model_id && (
                    <Badge variant="secondary" className="ml-2">
                      best
                    </Badge>
                  )}
                </TableCell>
                <TableCell className="hidden px-2 py-1.5 text-sm text-muted-foreground sm:table-cell">
                  {m.size}
                </TableCell>
                <TableCell className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-foreground">
                  {format(m[metricKey] as number)}
                </TableCell>
                <TableCell className="px-2 py-1.5 text-right font-mono text-xs tabular-nums text-muted-foreground">
                  #{i + 1}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <p className="mt-2 text-xs text-muted-foreground">
          Best: <span className="text-foreground">{best.name}</span> (
          {format(best[metricKey] as number)})
          {"  ·  "}Weakest:{" "}
          <span className="text-foreground">{worst.name}</span> (
          {format(worst[metricKey] as number)})
        </p>
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="mb-2 text-sm font-semibold text-foreground">{title}</h3>
      <p className="text-sm leading-relaxed text-muted-foreground">{children}</p>
    </div>
  );
}