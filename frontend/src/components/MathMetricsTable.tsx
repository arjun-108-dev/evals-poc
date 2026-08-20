import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";
import { ACCENT, pct } from "@/lib/series";
import type { MathMetric } from "@/lib/types";

export function MathMetricsTable({ metrics }: { metrics: MathMetric[] }) {
  const best = [...metrics].sort((a, b) => b.overall_score - a.overall_score)[0];

  return (
    <Table>
      <TableHeader>
        <TableRow className="hover:bg-transparent">
          <TableHead className="px-2 py-1.5 text-xs font-medium">Model</TableHead>
          <TableHead className="hidden px-2 py-1.5 text-xs font-medium sm:table-cell">
            Size
          </TableHead>
          <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
            Acc
          </TableHead>
          <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
            Parse
          </TableHead>
          <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
            Overall
          </TableHead>
          <TableHead className="px-2 py-1.5 text-right text-xs font-medium">
            Avg ms
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {metrics.map((m) => {
          const isBest = m.model_id === best.model_id;
          return (
            <TableRow key={m.model_id}>
              <TableCell className="px-2 py-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-foreground">
                    {m.name}
                  </span>
                  {isBest && <Badge variant="secondary">best</Badge>}
                </div>
              </TableCell>
              <TableCell className="hidden px-2 py-1.5 text-sm text-muted-foreground sm:table-cell">
                {m.size}
              </TableCell>
              <TableCell className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-foreground">
                {pct(m.accuracy)}
              </TableCell>
              <TableCell
                className={cn(
                  "px-2 py-1.5 text-right font-mono text-sm tabular-nums",
                  m.parse_rate < 0.9
                    ? "text-destructive"
                    : m.parse_rate < 1
                      ? "text-foreground"
                      : "text-muted-foreground",
                )}
              >
                {pct(m.parse_rate)}
              </TableCell>
              <TableCell className="px-2 py-1.5">
                <div className="flex items-center justify-end gap-2">
                  <div className="h-1.5 w-16 overflow-hidden rounded-full bg-muted">
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${Math.round(m.overall_score * 100)}%`,
                        background: isBest ? ACCENT : "var(--muted-foreground)",
                      }}
                    />
                  </div>
                  <span className="w-10 font-mono text-sm tabular-nums text-foreground">
                    {m.overall_score.toFixed(2)}
                  </span>
                </div>
              </TableCell>
              <TableCell className="px-2 py-1.5 text-right font-mono text-sm tabular-nums text-muted-foreground">
                {Math.round(m.avg_latency_ms)}
              </TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
}
