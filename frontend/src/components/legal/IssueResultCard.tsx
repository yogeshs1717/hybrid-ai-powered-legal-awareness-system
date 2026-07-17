import { Sparkles } from "lucide-react";
import { Card } from "@/components/ui/card";
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
    <Card className="p-5 sm:p-6">
      <div className="flex items-start gap-4">
        <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-accent/12 text-accent">
          <Sparkles className="h-5 w-5" aria-hidden />
        </span>
        <div className="min-w-0 flex-1">
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground/80">
            Detected situation
          </p>
          <h3 className="mt-0.5 font-display text-xl font-semibold tracking-tight text-foreground">
            {issue.display_name}
          </h3>

          {issue.issue_match_reason && (
            <div className="mt-4 rounded-xl border border-white/10 bg-white/[0.02] p-3.5">
              <p className="text-xs font-medium text-muted-foreground/80">
                Why your situation matched this
              </p>
              <p className="mt-1 text-sm leading-relaxed text-foreground/90 text-pretty">
                {issue.issue_match_reason}
              </p>
            </div>
          )}

          {signals?.length > 0 && (
            <div className="mt-4">
              <p className="mb-2 text-xs font-medium text-muted-foreground/80">
                Signals we noticed
              </p>
              <ScenarioSignals signals={signals} />
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}
