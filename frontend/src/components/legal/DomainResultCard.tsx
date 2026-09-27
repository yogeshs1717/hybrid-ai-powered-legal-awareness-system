import { Scale } from "lucide-react";
import { ConfidenceMeter } from "./ConfidenceMeter";
import type { DomainAnalysis } from "@/types/contract";

/** The general area of law the situation appears to relate to. */
export function DomainResultCard({ domain }: { domain: DomainAnalysis }) {
  return (
    <div className="rounded-xl border-2 border-black dark:border-white/30 bg-card p-5 sm:p-6 shadow-sm select-none">
      <div className="flex items-center justify-between mb-4">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#f59e0b] text-black font-mono text-xs font-black uppercase">
          <Scale className="h-3.5 w-3.5 stroke-[2.5]" />
          <span>AREA OF LAW</span>
        </span>
        <span className="font-mono text-[11px] text-muted-foreground uppercase font-bold">
          CLASSIFIED DOMAIN
        </span>
      </div>

      <h3 className="font-mono text-xl sm:text-2xl font-extrabold tracking-tight text-foreground">
        {domain.display_name}
      </h3>

      <div className="mt-4 pt-4 border-t border-border/60">
        <ConfidenceMeter value={domain.confidence} label={domain.confidence_label} />
      </div>
    </div>
  );
}
