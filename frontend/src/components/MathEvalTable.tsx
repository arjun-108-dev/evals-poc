import { Fragment, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";
import type { MathExampleRow } from "@/lib/types";

type MathStatus = "correct" | "wrong" | "unparsed";

function rowStatus(r: MathExampleRow): MathStatus {
  if (!r.answer_parsed) return "unparsed";
  if (!r.answer_correct) return "wrong";
  return "correct";
}

const STATUS_LABEL: Record<MathStatus, string> = {
  correct: "Correct",
  wrong: "Wrong",
  unparsed: "Unparsed",
};

const STATUS_VARIANT: Record<MathStatus, "secondary" | "outline" | "destructive"> = {
  correct: "secondary",
  wrong: "outline",
  unparsed: "destructive",
};

function latencyTone(ms: number) {
  if (ms >= 10000)
    return { text: "text-destructive", bar: "var(--destructive)" };
  if (ms >= 6000) return { text: "text-foreground", bar: "var(--foreground)" };
  return { text: "text-muted-foreground", bar: "var(--muted-foreground)" };
}

export function MathEvalTable({ rows }: { rows: MathExampleRow[] }) {
  const [expanded, setExpanded] = useState<string | null>(null);
  const maxLatency = Math.max(1, ...rows.map((r) => r.latency_ms));

  return (
    <Table>
      <TableHeader>
        <TableRow className="hover:bg-transparent">
          <TableHead className="hidden w-24 px-2 py-1.5 text-xs font-medium sm:table-cell">
            ID
          </TableHead>
          <TableHead className="px-2 py-1.5 text-xs font-medium">
            Question
          </TableHead>
          <TableHead className="px-2 py-1.5 text-xs font-medium">Status</TableHead>
          <TableHead className="w-36 px-2 py-1.5 text-right text-xs font-medium">
            Latency
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map((r) => {
          const status = rowStatus(r);
          const tone = latencyTone(r.latency_ms);
          const isOpen = expanded === r.id;
          return (
            <Fragment key={r.id}>
              <TableRow
                onClick={() => setExpanded(isOpen ? null : r.id)}
                className="cursor-pointer"
              >
                <TableCell className="hidden px-2 py-1.5 font-mono text-xs text-muted-foreground sm:table-cell">
                  {r.id}
                </TableCell>
                <TableCell className="max-w-md px-2 py-1.5 text-sm text-foreground">
                  <span className="line-clamp-1">{r.question}</span>
                </TableCell>
                <TableCell className="px-2 py-1.5">
                  <Badge variant={STATUS_VARIANT[status]}>
                    {STATUS_LABEL[status]}
                  </Badge>
                </TableCell>
                <TableCell className="px-2 py-1.5">
                  <div className="flex items-center justify-end gap-2">
                    <div className="h-1 w-10 overflow-hidden rounded-full bg-muted">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${Math.min(100, (r.latency_ms / maxLatency) * 100)}%`,
                          background: tone.bar,
                        }}
                      />
                    </div>
                    <span
                      className={cn(
                        "w-14 text-right font-mono text-xs tabular-nums",
                        tone.text,
                      )}
                    >
                      {Math.round(r.latency_ms)}
                    </span>
                  </div>
                </TableCell>
              </TableRow>
              {isOpen && (
                <TableRow className="hover:bg-transparent">
                  <TableCell colSpan={4} className="bg-muted/30 px-3 py-3">
                    <MathRowDetail r={r} />
                  </TableCell>
                </TableRow>
              )}
            </Fragment>
          );
        })}
      </TableBody>
    </Table>
  );
}

function MathRowDetail({ r }: { r: MathExampleRow }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="space-y-3">
        <Field label="Question">
          <p className="text-sm text-foreground">{r.question}</p>
        </Field>
        <Field label="Expected answer">
          <p className="text-sm font-mono text-foreground">{r.expected_answer}</p>
        </Field>
        <Field label="Extracted answer">
          <p className="text-sm font-mono text-foreground">
            {r.extracted_answer || "(none)"}
          </p>
        </Field>
      </div>
      <div className="space-y-3">
        <Field label="Raw model output">
          <ScrollArea className="h-40 rounded-lg border border-border bg-muted/30">
            <pre className="whitespace-pre-wrap p-2 text-xs text-muted-foreground">
              {r.model_output || "(empty)"}
            </pre>
          </ScrollArea>
        </Field>
        <Field label="Grading">
          <div className="flex flex-wrap gap-1.5">
            <Flag ok={r.answer_parsed} label="parsed" />
            <Flag ok={r.answer_correct} label="correct" />
            {r.error && (
              <span className="text-xs text-destructive">error: {r.error}</span>
            )}
          </div>
        </Field>
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="mb-1 text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
        {label}
      </div>
      {children}
    </div>
  );
}

function Flag({ ok, label }: { ok: boolean; label: string }) {
  return (
    <Badge variant={ok ? "secondary" : "destructive"}>
      {label}: {ok ? "✓" : "✗"}
    </Badge>
  );
}