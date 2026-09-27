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

const LABEL_COLORS: Record<ConfidenceLabel, string> = {
  High: "bg-[#10b981] text-black",
  Medium: "bg-[#f59e0b] text-black",
  Low: "bg-[#e11d48] text-white",
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
    <div className="w-full select-none">
      <div className="mb-2 flex items-center justify-between text-xs font-mono">
        <span className="inline-flex items-center gap-1.5 text-muted-foreground font-bold">
          <span>MODEL CONFIDENCE</span>
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
        <span className={cn("px-2 py-0.5 rounded text-[10px] font-black uppercase", LABEL_COLORS[label])}>
          {label} · {pct}%
        </span>
      </div>
      <div
        className="h-2.5 w-full overflow-hidden rounded-full border border-border bg-muted/50 p-0.5"
        role="meter"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Model confidence"
      >
        <div
          className={cn(
            "h-full rounded-full transition-[width] duration-500 ease-out",
            label === "High" ? "bg-[#10b981]" : label === "Medium" ? "bg-[#f59e0b]" : "bg-[#e11d48]"
          )}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
