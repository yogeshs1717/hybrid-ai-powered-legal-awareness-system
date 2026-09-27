import { BookOpen, ExternalLink, ShieldCheck } from "lucide-react";
import type { LegalProvision } from "@/types/contract";

/*
  A single manually-verified legal provision (CLAUDE.md Section 8). The card
  shows the simplified explanation and the Layer B curated
  provision_relevance_rationale (Section 6.7) — kept visually separate from the
  Layer A issue match reason so the two reasoning layers never blur together.
  Full statutory text is never shown here; only the official-source link.
*/
export function ProvisionCard({
  provision,
  index,
}: {
  provision: LegalProvision;
  index: number;
}) {
  const { official_source } = provision;
  return (
    <div className="rounded-xl border-2 border-black dark:border-white/30 bg-card shadow-sm overflow-hidden select-none">
      {/* Header bar */}
      <div className="border-b-2 border-border bg-muted/40 p-4 sm:p-5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#10b981] text-black font-mono text-xs font-black uppercase">
            <ShieldCheck className="h-3.5 w-3.5 stroke-[2.5]" />
            <span>VERIFIED STATUTE</span>
          </span>
          <span className="font-mono text-xs font-bold text-muted-foreground">
            #{index + 1}
          </span>
        </div>
        <span className="font-mono text-[11px] text-muted-foreground uppercase font-bold hidden sm:inline">
          OFFICIAL LAW TEXT
        </span>
      </div>

      {/* Main Title Section */}
      <div className="p-5 sm:p-6 border-b border-border/60">
        <div className="flex items-start gap-3">
          <div className="h-10 w-10 shrink-0 rounded-lg border-2 border-border bg-muted flex items-center justify-center text-foreground">
            <BookOpen className="h-5 w-5 stroke-[2]" />
          </div>
          <div className="min-w-0">
            <h4 className="font-mono text-lg sm:text-xl font-black text-foreground">
              {provision.act} · {provision.section}
            </h4>
            {provision.title && (
              <p className="mt-1 text-xs sm:text-sm font-medium text-muted-foreground">
                {provision.title}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div className="space-y-4 p-5 sm:p-6">
        <div>
          <p className="font-mono text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
            IN PLAIN WORDS
          </p>
          <p className="mt-1 text-sm leading-relaxed text-foreground font-medium">
            {provision.simplified_explanation}
          </p>
        </div>

        <div className="rounded-lg border-2 border-[#f59e0b]/40 bg-[#f59e0b]/10 p-4">
          <p className="font-mono text-[11px] font-black uppercase tracking-wider text-amber-900 dark:text-amber-200">
            Why this may be relevant to your situation
          </p>
          <p className="mt-1 text-xs sm:text-sm leading-relaxed text-foreground font-medium">
            {provision.provision_relevance_rationale}
          </p>
        </div>

        {official_source?.url ? (
          <div className="pt-2">
            <a
              href={official_source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border-2 border-foreground bg-foreground text-background font-mono text-xs font-bold tracking-wider hover:bg-transparent hover:text-foreground transition-all"
            >
              <span>VIEW ON {official_source.name?.toUpperCase() ?? "OFFICIAL PORTAL"}</span>
              <ExternalLink className="h-3.5 w-3.5" />
            </a>
          </div>
        ) : (
          <p className="text-xs font-mono text-muted-foreground">
            Source: {official_source?.name ?? "Official Indian Law Gazette"}
          </p>
        )}
      </div>
    </div>
  );
}
