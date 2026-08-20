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
import type { ExampleRow } from "@/lib/types";

type Status = "correct" | "wrong_tool" | "false_positive" | "arg_mismatch";

function rowStatus(r: ExampleRow): Status {
  if (r.false_positive) return "false_positive";
  if (!r.tool_correct) return "wrong_tool";
  if (!r.args_correct) return "arg_mismatch";
  return "correct";
}

const STATUS_LABEL: Record<Status, string> = {
  correct: "Correct",
  wrong_tool: "Wrong tool",
  false_positive: "False positive",
  arg_mismatch: "Arg mismatch",
};

// 3 genuinely distinct variants, ordered by severity (low -> high).
const STATUS_VARIANT: Record<Status, "secondary" | "outline" | "destructive"> =
  {
    correct: "secondary",
    arg_mismatch: "outline",
    wrong_tool: "outline",
    false_positive: "destructive",
  };

function latencyTone(ms: number) {
  if (ms >= 10000)
    return { text: "text-destructive", bar: "var(--destructive)" };
  if (ms >= 6000) return { text: "text-foreground", bar: "var(--foreground)" };
  return { text: "text-muted-foreground", bar: "var(--muted-foreground)" };
}

export function EvalTable({ rows }: { rows: ExampleRow[] }) {
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
            Prompt
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
                  <span className="line-clamp-1">{r.prompt}</span>
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
                    <RowDetail r={r} />
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

function RowDetail({ r }: { r: ExampleRow }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="space-y-3">
        <Field label="Prompt">
          <p className="text-sm text-foreground">{r.prompt}</p>
        </Field>
        <Field label="Expected">
          <p className="text-sm text-foreground">
            <span className="font-mono text-foreground">{r.expected_tool}</span>
            {r.expected_args ? (
              <code className="ml-2 text-xs text-muted-foreground">
                {r.expected_args}
              </code>
            ) : null}
          </p>
        </Field>
        <Field label="Predicted">
          <p className="text-sm text-foreground">
            <span className="font-mono text-foreground">
              {r.parsed_tool || "(none)"}
            </span>
            {r.parsed_args ? (
              <code className="ml-2 text-xs text-muted-foreground">
                {r.parsed_args}
              </code>
            ) : null}
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
            <Flag ok={r.tool_correct} label="tool" />
            <Flag ok={r.args_correct} label="args" />
            <Flag ok={r.format_valid} label="format" />
            <Flag ok={!r.false_positive} label="no FP" />
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
