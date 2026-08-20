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
import { MathDimensionChart } from "./MathDimensionChart";
import { MathHeatmap } from "./MathHeatmap";
import { MathOutcomeChart } from "./MathOutcomeChart";
import { MathMetricsTable } from "./MathMetricsTable";
import type { MathChartKey, MathExampleRow, MathMetric } from "@/lib/types";

export function MathOverview({
  models,
  rowsByModel,
  onSelectChart,
}: {
  models: MathMetric[];
  rowsByModel: Record<string, MathExampleRow[]>;
  onSelectChart: (k: MathChartKey) => void;
}) {
  return (
    <div className="space-y-6">
      <section className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Accuracy by category &amp; difficulty</CardTitle>
            <CardDescription>
              Per-model accuracy sliced by difficulty level or category. Toggle
              between the two views to find where models fall apart.
            </CardDescription>
            <CardAction>
              <Button
                variant="link"
                size="sm"
                className="h-auto p-0"
                onClick={() => onSelectChart("dimension")}
              >
                Details
                <ArrowRightIcon data-icon="inline-end" />
              </Button>
            </CardAction>
          </CardHeader>
          <CardContent>
            <MathDimensionChart
              rowsByModel={rowsByModel}
              models={models}
              className="w-full"
            />
          </CardContent>
        </Card>

        <div className="grid gap-4 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">
                Category &times; model heatmap
              </CardTitle>
              <CardDescription>
                Accuracy per (model, category) pair &mdash; darker = better
              </CardDescription>
              <CardAction>
                <Button
                  variant="link"
                  size="sm"
                  className="h-auto p-0"
                  onClick={() => onSelectChart("heatmap")}
                >
                  Details
                  <ArrowRightIcon data-icon="inline-end" />
                </Button>
              </CardAction>
            </CardHeader>
            <CardContent>
              <MathHeatmap
                rowsByModel={rowsByModel}
                models={models}
                className="w-full"
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">
                Outcome composition
              </CardTitle>
              <CardDescription>
                Correct / wrong / unparsed breakdown per model
              </CardDescription>
              <CardAction>
                <Button
                  variant="link"
                  size="sm"
                  className="h-auto p-0"
                  onClick={() => onSelectChart("outcome")}
                >
                  Details
                  <ArrowRightIcon data-icon="inline-end" />
                </Button>
              </CardAction>
            </CardHeader>
            <CardContent>
              <MathOutcomeChart metrics={models} className="w-full" />
            </CardContent>
          </Card>
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold tracking-tight text-foreground">
          All metrics
        </h2>
        <MathMetricsTable metrics={models} />
      </section>
    </div>
  );
}