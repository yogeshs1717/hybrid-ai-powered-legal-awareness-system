import { Badge } from "@/components/ui/badge";

/** Supporting signal chips (CLAUDE.md Section 6.6 — explanation only, not a decision). */
export function ScenarioSignals({ signals }: { signals: string[] }) {
  if (!signals?.length) return null;
  return (
    <div className="flex flex-wrap gap-2">
      {signals.map((s, i) => (
        <Badge key={`${s}-${i}`} variant="muted" className="capitalize">
          {s}
        </Badge>
      ))}
    </div>
  );
}
