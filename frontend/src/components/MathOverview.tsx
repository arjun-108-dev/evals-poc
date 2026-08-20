import { ArrowRightIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MetricRadarChart } from "./MetricRadarChart";
import { TradeoffScatterChart } from "./TradeoffScatterChart";
import { MathMetricsTable } from "./MathMetricsTable";
import { MATH_SUB_SCORES, pct } from "@/lib/series";
import type { MathMetric, MathMetricKey } from "@/lib/types";

const ms = (v: number) => `${Math.round(v)}ms`;

export function MathOverview({
  metrics,
  onSelectMetric,
}: {
  metrics: MathMetric[];
  onSelectMetric: (k: MathMetricKey) => void;
}) {
  const best = [...metrics].sort((a, b) => b.overall_score - a.overall_score)[0];
  const worst = [...metrics].sort((a, b) => a.overall_score - b.overall_score)[0];
  const fastest = [...metrics].sort(
    (a, b) => a.avg_latency_ms - b.avg_latency_ms,
  )[0];

  return (
    <div className="space-y-6">
      <section className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Model comparison</CardTitle>
            <CardDescription>
              One polygon per model across the two sub-scores that make up the
              Overall Score. The best model is highlighted; all others are
              neutral.
            </CardDescription>
            <CardAction>
              <Button
                variant="link"
                size="sm"
                className="h-auto p-0"
                onClick={() => onSelectMetric("overall_score")}
              >
                Explain score
                <ArrowRightIcon data-icon="inline-end" />
              </Button>
            </CardAction>
          </CardHeader>
          <CardContent>
            <MetricRadarChart
              metrics={metrics}
              subScores={MATH_SUB_SCORES}
              className="mx-auto aspect-square w-full max-w-2xl"
            />
            <p className="mt-2 text-center text-xs text-muted-foreground">
              Best: <span className="text-foreground">{best.name}</span> (
              {best.overall_score.toFixed(2)}){"  ·  "}Weakest:{" "}
              <span className="text-foreground">{worst.name}</span> (
              {worst.overall_score.toFixed(2)})
            </p>
          </CardContent>
        </Card>

        <div className="grid gap-4 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">
                Accuracy vs extraction
              </CardTitle>
              <CardDescription>
                Being right matters less if no answer is ever extracted. Top-right
                is the goal zone.
              </CardDescription>
              <CardAction>
                <Button
                  variant="link"
                  size="sm"
                  className="h-auto p-0"
                  onClick={() => onSelectMetric("parse_rate")}
                >
                  Explain parse rate
                  <ArrowRightIcon data-icon="inline-end" />
                </Button>
              </CardAction>
            </CardHeader>
            <CardContent>
              <TradeoffScatterChart
                metrics={metrics}
                xKey="accuracy"
                yKey="parse_rate"
                xLabel="Accuracy"
                yLabel="Parse Rate"
                xFormat={pct}
                yFormat={pct}
                xGuide={0.85}
                yGuide={0.95}
                xDomain={[0, 1]}
                yDomain={[0, 1]}
                goodZone="top-right"
                className="aspect-square w-full"
              />
              <p className="mt-2 text-xs text-muted-foreground">
                Worst extractor:{" "}
                <span className="text-foreground">{best.name}</span> actually all
                models parsed every answer this run.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Speed vs quality</CardTitle>
              <CardDescription>
                Overall score against average latency (dot size = params).
              </CardDescription>
              <CardAction>
                <Button
                  variant="link"
                  size="sm"
                  className="h-auto p-0"
                  onClick={() => onSelectMetric("avg_latency_ms")}
                >
                  Explain latency
                  <ArrowRightIcon data-icon="inline-end" />
                </Button>
              </CardAction>
            </CardHeader>
            <CardContent>
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
                className="aspect-square w-full"
              />
              <p className="mt-2 text-xs text-muted-foreground">
                Fastest: <span className="text-foreground">{fastest.name}</span> (
                {ms(fastest.avg_latency_ms)})
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold tracking-tight text-foreground">
          All metrics
        </h2>
        <MathMetricsTable metrics={metrics} />
      </section>
    </div>
  );
}