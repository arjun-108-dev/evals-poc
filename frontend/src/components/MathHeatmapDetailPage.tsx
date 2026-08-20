import { ArrowLeftIcon } from "lucide-react";

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
import { MathHeatmap } from "./MathHeatmap";
import { bucketAccuracy } from "@/lib/mathStats";
import { pct } from "@/lib/series";
import type { MathExampleRow, MathMetric } from "@/lib/types";

export function MathHeatmapDetailPage({
  rowsByModel,
  models,
  onBack,
}: {
  rowsByModel: Record<string, MathExampleRow[]>;
  models: MathMetric[];
  onBack: () => void;
}) {
  const buckets = bucketAccuracy(rowsByModel, "category");
  const cats = [
    ...new Set(
      Object.values(rowsByModel)
        .flat()
        .map((r) => r.category)
        .filter((c): c is string => !!c),
    ),
  ];

  return (
    <div className="space-y-6">
      <Button variant="ghost" size="sm" onClick={onBack}>
        <ArrowLeftIcon data-icon="inline-start" />
        Back to overview
      </Button>

      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-semibold tracking-tight text-foreground">
            Category &times; model heatmap
          </h2>
        </div>
        <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
          Accuracy per (model, category) pair — the darker the cell, the
          better the model performed on that category.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Heatmap</CardTitle>
          <CardDescription>
            Cell color encodes accuracy; the number shows questions per cell
          </CardDescription>
        </CardHeader>
        <CardContent>
          <MathHeatmap
            rowsByModel={rowsByModel}
            models={models}
            className="w-full"
          />
        </CardContent>
      </Card>

      <div className="space-y-4">
        <Section title="What it shows">
          A grid where rows are models, columns are categories (arithmetic,
          word problem, fraction/percent, algebra), and each cell shows the
          model's accuracy on that category. Cell intensity scales with
          accuracy, and the small number is the question count behind the
          percentage.
        </Section>
        <Separator />
        <Section title="How to read it">
          Scan across a row to see whether a model is uniformly strong or has
          category-specific gaps. Scan down a column to compare models on the
          same category. Darker teal = higher accuracy; light or empty cells
          = lower or no data.
        </Section>
        <Separator />
        <Section title="What to look for">
          A model that is strong on arithmetic but weak on word problems
          reveals a reading-comprehension bottleneck, not a math one. A row
          that is uniformly dark means the model handles every category well.
          Be careful with per-category counts: at ~8 questions per category, a
          single question moves the percentage by 12.5 points.
        </Section>
      </div>

      <div>
        <h3 className="mb-2 text-sm font-semibold text-foreground">
          Exact numbers
        </h3>
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent">
              <TableHead className="px-2 py-1.5 text-xs font-medium">
                Model
              </TableHead>
              {cats.map((c) => (
                <TableHead
                  key={c}
                  className="px-2 py-1.5 text-right text-xs font-medium"
                >
                  {c.replace("_", " ")}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {models.map((m) => (
              <TableRow key={m.model_id}>
                <TableCell className="px-2 py-1.5 text-sm text-foreground">
                  {m.name}
                </TableCell>
                {cats.map((c) => {
                  const cell = buckets[m.model_id]?.[c];
                  const acc = cell?.accuracy ?? 0;
                  const n = cell?.total ?? 0;
                  return (
                    <TableCell
                      key={c}
                      className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-foreground"
                    >
                      {pct(acc)}
                      <span className="text-muted-foreground"> · {n}</span>
                    </TableCell>
                  );
                })}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <h3 className="mb-2 text-sm font-semibold text-foreground">{title}</h3>
      <p className="text-sm leading-relaxed text-muted-foreground">{children}</p>
    </div>
  );
}
