import { Sparkles } from "lucide-react";
import { ScenarioSignals } from "./ScenarioSignals";
import type { IssueAnalysis } from "@/types/contract";

/*
  The specific situation type detected within the area of law, plus the Layer A
  "why this matched" explanation (issue_match_reason, CLAUDE.md Section 6.7).
  The raw similarity_score is intentionally NOT rendered (Section 6.2 / approved
  design) — only the human-readable match reason is shown.
*/
export function IssueResultCard({
  issue,
  signals,
}: {
  issue: IssueAnalysis;
  signals: string[];
}) {
  return (
    <div className="rounded-xl border-2 border-black dark:border-white/30 bg-card p-5 sm:p-6 shadow-sm select-none">
      <div className="flex items-center justify-between mb-4">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#00c5ff] text-black font-mono text-xs font-black uppercase">
          <Sparkles className="h-3.5 w-3.5 stroke-[2.5]" />
          <span>DETECTED SITUATION</span>
        </span>
        <span className="font-mono text-[11px] text-muted-foreground uppercase font-bold">
          ISSUE PROFILE
        </span>
      </div>

      <h3 className="font-mono text-xl sm:text-2xl font-extrabold tracking-tight text-foreground">
        {issue.display_name}
      </h3>

      {issue.issue_match_reason && (
        <div className="mt-4 rounded-lg border-2 border-border bg-muted/40 p-3.5">
          <p className="font-mono text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
            Why your situation matched this
          </p>
          <p className="mt-1 text-xs sm:text-sm leading-relaxed text-foreground/90 font-medium">
            {issue.issue_match_reason}
          </p>
        </div>
      )}

      {signals?.length > 0 && (
        <div className="mt-4 pt-3 border-t border-border/60">
          <p className="mb-2 font-mono text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
            Key Signals Identified
          </p>
          <ScenarioSignals signals={signals} />
        </div>
      )}
    </div>
  );
}
