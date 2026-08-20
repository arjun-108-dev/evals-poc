import { useEffect, useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { EvalTable } from "./EvalTable";
import { loadModelRows } from "@/lib/data";
import type { DatasetExample, ExampleRow, ModelMeta } from "@/lib/types";

type StatusFilter = "all" | "correct" | "wrong_tool" | "false_positive" | "arg_mismatch";

const STATUS_LABEL: Record<StatusFilter, string> = {
  all: "All statuses",
  correct: "Correct",
  wrong_tool: "Wrong tool",
  false_positive: "False positive",
  arg_mismatch: "Arg mismatch",
};

export function ModelDetail({
  models,
  dataset,
}: {
  models: ModelMeta[];
  dataset: DatasetExample[];
}) {
  const [selected, setSelected] = useState<ModelMeta>(models[0]);
  const [rows, setRows] = useState<ExampleRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [status, setStatus] = useState<StatusFilter>("all");

  useEffect(() => {
    let alive = true;
    setLoading(true);
    loadModelRows(selected.id, dataset)
      .then((r) => alive && setRows(r))
      .catch(() => alive && setRows([]))
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, [selected, dataset]);

  const categories = useMemo(
    () => ["all", ...Array.from(new Set(dataset.map((d) => d.category)))],
    [dataset],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return rows.filter((r) => {
      if (status !== "all") {
        const st: StatusFilter = r.false_positive
          ? "false_positive"
          : !r.tool_correct
            ? "wrong_tool"
            : !r.args_correct
              ? "arg_mismatch"
              : "correct";
        if (st !== status) return false;
      }
      if (category !== "all" && r.category !== category) return false;
      if (q && !r.prompt.toLowerCase().includes(q) && !r.id.includes(q))
        return false;
      return true;
    });
  }, [rows, query, category, status]);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {models.map((m) => (
          <Button
            key={m.id}
            size="sm"
            variant={selected.id === m.id ? "default" : "outline"}
            onClick={() => setSelected(m)}
          >
            {m.name}
          </Button>
        ))}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search prompts…"
          className="h-8 w-full max-w-xs"
        />
        <Select value={category} onValueChange={(v) => setCategory(v as string)}>
          <SelectTrigger size="sm" className="w-full sm:w-44">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            {categories.map((c) => (
              <SelectItem key={c} value={c}>
                {c === "all" ? "All categories" : c}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select
          value={status}
          onValueChange={(v) => setStatus(v as StatusFilter)}
        >
          <SelectTrigger size="sm" className="w-full sm:w-44">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            {(Object.keys(STATUS_LABEL) as StatusFilter[]).map((s) => (
              <SelectItem key={s} value={s}>
                {STATUS_LABEL[s]}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <span className="ml-auto text-xs text-muted-foreground">
          {filtered.length} / {rows.length} examples
        </span>
      </div>

      {loading ? (
        <div className="rounded-lg border border-border p-8 text-center text-sm text-muted-foreground">
          Loading {selected.name} results…
        </div>
      ) : (
        <EvalTable rows={filtered} />
      )}
    </div>
  );
}
