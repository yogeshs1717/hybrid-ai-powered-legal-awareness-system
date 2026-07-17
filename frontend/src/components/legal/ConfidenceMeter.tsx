import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { HelpCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ConfidenceLabel } from "@/types/contract";

/*
  Shows the domain classifier's "model confidence" (CLAUDE.md Section 5, 8.1).
  Explicitly labelled model confidence — never "legal certainty" (Section 10).
  Note: this is ONLY used for the domain. The issue similarity_score is never
  shown to citizens (Section 6.2, per approved design).
*/

const LABEL_STYLES: Record<ConfidenceLabel, string> = {
  High: "text-primary",
  Medium: "text-accent",
  Low: "text-muted-foreground",
};

export function ConfidenceMeter({
  value,
  label,
}: {
  value: number;
  label: ConfidenceLabel;
}) {
  const pct = Math.round(Math.max(0, Math.min(1, value)) * 100);
  return (
    <div className="w-full">
      <div className="mb-1.5 flex items-center justify-between text-xs">
        <span className="inline-flex items-center gap-1.5 text-muted-foreground">
          Model confidence
          <Tooltip>
            <TooltipTrigger aria-label="What is model confidence?">
              <HelpCircle className="h-3.5 w-3.5 opacity-70" />
            </TooltipTrigger>
            <TooltipContent>
              How sure the classifier is about the general area of law — not a
              statement that any law applies to your situation.
            </TooltipContent>
          </Tooltip>
        </span>
        <span className={cn("font-semibold", LABEL_STYLES[label])}>{label}</span>
      </div>
      <div
        className="h-1.5 w-full overflow-hidden rounded-full bg-white/[0.07]"
        role="meter"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Model confidence"
      >
        <div
          className="h-full rounded-full bg-gradient-to-r from-primary to-accent transition-[width] duration-700 ease-out"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
