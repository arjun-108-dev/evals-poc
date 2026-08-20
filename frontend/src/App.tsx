import { useEffect, useState } from "react";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import {
  loadDataset,
  loadMathDataset,
  loadMathMetrics,
  loadMetrics,
  loadModels,
} from "./lib/data";
import type {
  DatasetExample,
  MathDatasetExample,
  MathMetric,
  MathMetricKey,
  Metric,
  MetricKey,
  ModelMeta,
} from "./lib/types";
import { Overview } from "./components/Overview";
import { ModelDetail } from "./components/ModelDetail";
import { MetricDetailPage } from "./components/MetricDetailPage";
import { MathOverview } from "./components/MathOverview";
import { MathModelDetail } from "./components/MathModelDetail";
import { MathMetricDetailPage } from "./components/MathMetricDetailPage";

type View = "overview" | "detail" | "chart";
type EvalKind = "tool" | "math";

export default function App() {
  const [models, setModels] = useState<ModelMeta[]>([]);
  const [toolMetrics, setToolMetrics] = useState<Metric[]>([]);
  const [toolDataset, setToolDataset] = useState<DatasetExample[]>([]);
  const [mathMetrics, setMathMetrics] = useState<MathMetric[]>([]);
  const [mathDataset, setMathDataset] = useState<MathDatasetExample[]>([]);
  const [evalKind, setEvalKind] = useState<EvalKind>("tool");
  const [view, setView] = useState<View>("overview");
  const [chartMetric, setChartMetric] = useState<
    MetricKey | MathMetricKey | null
  >(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      loadModels(),
      loadMetrics(),
      loadDataset(),
      loadMathMetrics(),
      loadMathDataset(),
    ])
      .then(([m, met, d, mmet, md]) => {
        setModels(m);
        setToolMetrics(met);
        setToolDataset(d);
        setMathMetrics(mmet);
        setMathDataset(md);
      })
      .catch((e) => setError(String(e?.message ?? e)));
  }, []);

  const switchEval = (kind: EvalKind) => {
    setEvalKind(kind);
    setView("overview");
    setChartMetric(null);
  };

  const dataset = evalKind === "tool" ? toolDataset : mathDataset;
  const ready =
    models.length > 0 &&
    (evalKind === "tool" ? toolMetrics.length > 0 : mathMetrics.length > 0);
  const tabValue: "overview" | "detail" = view === "detail" ? "detail" : "overview";

  return (
    <Tabs
      value={tabValue}
      onValueChange={(v) => setView(v as "overview" | "detail")}
      className="min-h-full"
    >
      <header className="sticky top-0 z-10 border-b border-border bg-background/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-3 sm:flex-row sm:items-center sm:gap-4">
          <div>
            <h1 className="text-base font-semibold tracking-tight text-foreground">
              Tiny Model {evalKind === "math" ? "Math" : "Tool-Calling"} Eval
            </h1>
            <p className="text-[11px] text-muted-foreground">
              Real Ollama runs · {models.length} models · {dataset.length}{" "}
              {evalKind === "math" ? "questions" : "prompts"}
            </p>
          </div>
          <div className="ml-auto flex w-full items-center justify-end gap-2 sm:w-fit">
            <Select value={evalKind} onValueChange={(v) => switchEval(v as EvalKind)}>
              <SelectTrigger size="sm" className="w-full sm:w-36">
                <SelectValue placeholder="Evaluation" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="tool">Tool Calling</SelectItem>
                <SelectItem value="math">Math</SelectItem>
              </SelectContent>
            </Select>
            <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="detail">Per-model</TabsTrigger>
            </TabsList>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        {error && (
          <div className="rounded-lg border border-destructive/40 bg-destructive/10 p-4 text-sm text-destructive">
            Could not load evaluation data. Run{" "}
            <code>uv run python evaluator/analyze.py</code> and{" "}
            <code>uv run python evaluator/analyze_math.py</code> to generate{" "}
            <code>/data</code> files, then restart the dev server.
            <div className="mt-1 text-xs text-destructive/80">{error}</div>
          </div>
        )}

        {!error && !ready && (
          <div className="rounded-lg border border-border bg-muted/40 p-8 text-center text-sm text-muted-foreground">
            Loading evaluation data…
          </div>
        )}

        {ready &&
          (evalKind === "tool" ? (
            <>
              <TabsContent value="overview">
                {view === "chart" && chartMetric ? (
                  <MetricDetailPage
                    metricKey={chartMetric as MetricKey}
                    metrics={toolMetrics}
                    onBack={() => setView("overview")}
                  />
                ) : (
                  <Overview
                    metrics={toolMetrics}
                    onSelectMetric={(k) => {
                      setChartMetric(k);
                      setView("chart");
                    }}
                  />
                )}
              </TabsContent>
              <TabsContent value="detail">
                <ModelDetail models={models} dataset={toolDataset} />
              </TabsContent>
            </>
          ) : (
            <>
              <TabsContent value="overview">
                {view === "chart" && chartMetric ? (
                  <MathMetricDetailPage
                    metricKey={chartMetric as MathMetricKey}
                    metrics={mathMetrics}
                    onBack={() => setView("overview")}
                  />
                ) : (
                  <MathOverview
                    metrics={mathMetrics}
                    onSelectMetric={(k) => {
                      setChartMetric(k);
                      setView("chart");
                    }}
                  />
                )}
              </TabsContent>
              <TabsContent value="detail">
                <MathModelDetail models={models} dataset={mathDataset} />
              </TabsContent>
            </>
          ))}

        <footer className="mt-10 border-t border-border pt-4 text-xs text-muted-foreground">
          All metrics are computed deterministically from real model outputs (no
          LLM judge, no synthetic data). See{" "}
          <code className="text-foreground">README.md</code> for methodology.
        </footer>
      </main>
    </Tabs>
  );
}