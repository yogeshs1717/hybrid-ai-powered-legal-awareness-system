import { FileSearch } from "lucide-react";

/*
  The explicit safe state (CLAUDE.md Section 8 & 14): when no manually-verified,
  in-force provision exists for the detected situation, LegalLens says so plainly
  — it never invents a legal answer and never renders an empty section. Action
  steps and portals may still be shown alongside this state by the caller.
*/
export function NoVerifiedProvisionState() {
  return (
    <div className="rounded-xl border-2 border-black dark:border-white/30 bg-card p-5 sm:p-6 shadow-sm select-none">
      <div className="flex items-center gap-2 mb-3">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#f59e0b] text-black font-mono text-xs font-black uppercase">
          <FileSearch className="h-3.5 w-3.5 stroke-[2.5]" />
          <span>STATUTE NOTICE</span>
        </span>
        <span className="font-mono text-[11px] text-muted-foreground uppercase font-bold">
          TRANSPARENCY STANDARD
        </span>
      </div>

      <h3 className="font-mono text-base sm:text-lg font-bold text-foreground">
        No verified legal provision to show yet
      </h3>
      <p className="mt-2 text-xs sm:text-sm leading-relaxed text-muted-foreground font-medium">
        LegalLens only displays legal provisions that have been human-verified against official government sources.
        For this situation, there isn't a verified provision mapped yet — so rather than guess or fabricate legal text,
        we are transparent about it. Please refer to the suggested next steps and official grievance portals below.
      </p>
    </div>
  );
}
