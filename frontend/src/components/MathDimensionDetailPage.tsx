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
import { MathDimensionChart } from "./MathDimensionChart";
import { bucketAccuracy } from "@/lib/mathStats";
import { pct } from "@/lib/series";
import type { MathExampleRow, MathMetric } from "@/lib/types";

const DIFFS = ["easy", "medium", "hard"];

export function MathDimensionDetailPage({
  rowsByModel,
  models,
  onBack,
}: {
  rowsByModel: Record<string, MathExampleRow[]>;
  models: MathMetric[];
  onBack: () => void;
}) {
  const buckets = bucketAccuracy(rowsByModel, "difficulty");

  return (
    <div className="space-y-6">
      <Button variant="ghost" size="sm" onClick={onBack}>
        <ArrowLeftIcon data-icon="inline-start" />
        Back to overview
      </Button>

      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-semibold tracking-tight text-foreground">
            Accuracy by category &amp; difficulty
          </h2>
          <Badge variant="secondary">grouped bar chart</Badge>
        </div>
        <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
          Per-model accuracy sliced by difficulty level or category, with a
          toggle between the two views.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Accuracy by dimension</CardTitle>
          <CardDescription>
            Toggle between difficulty and category grouping
          </CardDescription>
        </CardHeader>
        <CardContent>
          <MathDimensionChart
            rowsByModel={rowsByModel}
            models={models}
            className="w-full"
          />
        </CardContent>
      </Card>

      <div className="space-y-4">
        <Section title="What it shows">
          For each difficulty level (easy / medium / hard) or category, the
          fraction of questions each model answered correctly. Toggle between
          grouping by difficulty or category to see both breakdowns.
        </Section>
        <Separator />
        <Section title="How to read it">
          Each bar group represents one slice (e.g. "hard" questions). Within
          each group there is one bar per model, colored by the model's legend
          color. A tall bar means the model excels at that slice; a short bar
          exposes a weakness.
        </Section>
        <Separator />
        <Section title="What to look for">
          Watch for models that degrade gracefully from easy to medium to hard
          versus those that cliff at "hard" — that gap is what aggregate
          accuracy hides. Category cliffs (great at arithmetic but weak on word
          problems) suggest a comprehension bottleneck rather than an
          arithmetic one. Note that each bucket holds only a handful of
          questions, so single-question swings move the percentage a lot.
        </Section>
      </div>

      <div>
        <h3 className="mb-2 text-sm font-semibold text-foreground">
          Per-difficulty accuracy
        </h3>
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent">
              <TableHead className="px-2 py-1.5 text-xs font-medium">
                Difficulty
              </TableHead>
              {models.map((m) => (
                <TableHead
                  key={m.model_id}
                  className="px-2 py-1.5 text-right text-xs font-medium"
                >
                  {m.name}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {DIFFS.map((d) => (
              <TableRow key={d}>
                <TableCell className="px-2 py-1.5 text-sm capitalize text-foreground">
                  {d}
                </TableCell>
                {models.map((m) => {
                  const cell = buckets[m.model_id]?.[d];
                  const acc = cell?.accuracy ?? 0;
                  const n = cell?.total ?? 0;
                  return (
                    <TableCell
                      key={m.model_id}
                      className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-foreground"
                    >
                      {pct(acc)}
                      <span className="text-muted-foreground"> · {n} q</span>
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
