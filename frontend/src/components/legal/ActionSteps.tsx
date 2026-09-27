import { ListChecks } from "lucide-react";

/*
  Issue-specific next steps (CLAUDE.md Section 8). Rendered in the order the API
  returns them — most time-sensitive first. The UI adds no steps of its own.
*/
export function ActionSteps({ steps }: { steps: string[] }) {
  if (!steps?.length) return null;
  return (
    <div className="rounded-xl border-2 border-black dark:border-white/30 bg-card p-5 sm:p-6 shadow-sm select-none">
      <div className="flex items-center justify-between mb-4">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#e11d48] text-white font-mono text-xs font-black uppercase">
          <ListChecks className="h-3.5 w-3.5 stroke-[2.5]" />
          <span>SUGGESTED NEXT STEPS</span>
        </span>
        <span className="font-mono text-[11px] text-muted-foreground uppercase font-bold">
          ORDERED BY PRIORITY
        </span>
      </div>

      <ol className="space-y-3.5 mt-2">
        {steps.map((step, i) => (
          <li key={i} className="flex items-start gap-3.5 p-3 rounded-lg border border-border/80 bg-muted/20">
            <span className="h-7 w-7 rounded border border-border bg-foreground text-background font-mono text-xs font-black flex items-center justify-center shrink-0">
              {String(i + 1).padStart(2, "0")}
            </span>
            <p className="pt-0.5 text-xs sm:text-sm leading-relaxed text-foreground font-medium">
              {step}
            </p>
          </li>
        ))}
      </ol>
    </div>
  );
}
