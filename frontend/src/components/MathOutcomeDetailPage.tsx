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
import { MathOutcomeChart } from "./MathOutcomeChart";
import { outcomeComposition } from "@/lib/mathStats";
import { pct } from "@/lib/series";
import type { MathMetric } from "@/lib/types";

export function MathOutcomeDetailPage({
  metrics,
  onBack,
}: {
  metrics: MathMetric[];
  onBack: () => void;
}) {
  const outcome = outcomeComposition(metrics);

  return (
    <div className="space-y-6">
      <Button variant="ghost" size="sm" onClick={onBack}>
        <ArrowLeftIcon data-icon="inline-start" />
        Back to overview
      </Button>

      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-semibold tracking-tight text-foreground">
            Outcome composition
          </h2>
        </div>
        <p className="mt-1 max-w-3xl text-sm text-muted-foreground">
          Each model's results split into correct, wrong, and unparsed counts.
          The overall score formula blends accuracy and parse rate, but this
          chart shows the raw volumes behind each.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Stacked outcome</CardTitle>
          <CardDescription>
            Green = correct, red = wrong, gray = unparsed
          </CardDescription>
        </CardHeader>
        <CardContent>
          <MathOutcomeChart metrics={metrics} className="w-full" />
        </CardContent>
      </Card>

      <div className="space-y-4">
        <Section title="What it shows">
          A stacked bar per model where the total height equals the number of
          questions (37). The green segment is correct answers, red is wrong
          answers, and gray is questions where no numeric answer could be
          extracted at all.
        </Section>
        <Separator />
        <Section title="How to read it">
          Compare segment heights across models. A tall green segment means the
          model is doing well. A tall red segment means the model attempted but
          was wrong. Any visible gray segment means the model failed to produce
          a parsable numeric answer — a different failure mode from being
          wrong.
        </Section>
        <Separator />
        <Section title="What to look for">
          The overall score formula (0.75&middot;accuracy + 0.25&middot;parse
          rate) blends two failure modes together. This chart splits them
          apart: a model with a low overall score because it cannot format
          output (high unparsed) needs a different fix than one that is
          confidently wrong (low correct, low unparsed). In this run every
          model parsed all 37 answers, so all non-correct answers are wrong
          rather than unparsed.
        </Section>
      </div>

      <div>
        <h3 className="mb-2 text-sm font-semibold text-foreground">
          Per-model composition
        </h3>
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent">
              <TableHead className="px-2 py-1.5 text-xs font-medium">
                Model
              </TableHead>
              <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
                Correct
              </TableHead>
              <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
                Wrong
              </TableHead>
              <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
                Unparsed
              </TableHead>
              <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
                Accuracy
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {outcome.map((o) => (
              <TableRow key={o.model_id}>
                <TableCell className="px-2 py-1.5 text-sm text-foreground">
                  {o.name}
                </TableCell>
                <TableCell className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-foreground">
                  {o.correct}
                </TableCell>
                <TableCell className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-destructive">
                  {o.wrong}
                </TableCell>
                <TableCell className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-muted-foreground">
                  {o.unparsed}
                </TableCell>
                <TableCell className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-foreground">
                  {pct(o.accuracy)}
                </TableCell>
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
