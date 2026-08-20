import { useEffect, useState } from "react";

import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { loadDataset, loadMetrics, loadModels } from "./lib/data";
import type { DatasetExample, Metric, MetricKey, ModelMeta } from "./lib/types";
import { Overview } from "./components/Overview";
import { ModelDetail } from "./components/ModelDetail";
import { MetricDetailPage } from "./components/MetricDetailPage";

type View = "overview" | "detail" | "chart";

export default function App() {
  const [models, setModels] = useState<ModelMeta[]>([]);
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [dataset, setDataset] = useState<DatasetExample[]>([]);
  const [view, setView] = useState<View>("overview");
  const [chartMetric, setChartMetric] = useState<MetricKey | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([loadModels(), loadMetrics(), loadDataset()])
      .then(([m, met, d]) => {
        setModels(m);
        setMetrics(met);
        setDataset(d);
      })
      .catch((e) => setError(String(e?.message ?? e)));
  }, []);

  const ready = models.length > 0 && metrics.length > 0;
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
              Tiny Model Tool-Calling Eval
            </h1>
            <p className="text-[11px] text-muted-foreground">
              Real Ollama runs · {models.length} models · {dataset.length} prompts
            </p>
          </div>
          <TabsList className="ml-auto w-full sm:w-fit">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="detail">Per-model</TabsTrigger>
          </TabsList>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">
        {error && (
          <div className="rounded-lg border border-destructive/40 bg-destructive/10 p-4 text-sm text-destructive">
            Could not load evaluation data. Run{" "}
            <code>uv run python evaluator/analyze.py</code> to generate{" "}
            <code>/data</code> files, then restart the dev server.
            <div className="mt-1 text-xs text-destructive/80">{error}</div>
          </div>
        )}

        {!error && !ready && (
          <div className="rounded-lg border border-border bg-muted/40 p-8 text-center text-sm text-muted-foreground">
            Loading evaluation data…
          </div>
        )}

        {ready && (
          <>
            <TabsContent value="overview">
              {view === "chart" && chartMetric ? (
                <MetricDetailPage
                  metricKey={chartMetric}
                  metrics={metrics}
                  onBack={() => setView("overview")}
                />
              ) : (
                <Overview
                  metrics={metrics}
                  onSelectMetric={(k) => {
                    setChartMetric(k);
                    setView("chart");
                  }}
                />
              )}
            </TabsContent>
            <TabsContent value="detail">
              <ModelDetail models={models} dataset={dataset} />
            </TabsContent>
          </>
        )}

        <footer className="mt-10 border-t border-border pt-4 text-xs text-muted-foreground">
          All metrics are computed deterministically from real model outputs (no
          LLM judge, no synthetic data). See{" "}
          <code className="text-foreground">README.md</code> for methodology.
        </footer>
      </main>
    </Tabs>
  );
}
