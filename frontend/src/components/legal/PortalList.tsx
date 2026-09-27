import { ArrowUpRight, Landmark } from "lucide-react";
import type { Portal, PortalPriority } from "@/types/contract";

const PRIORITY_BADGES: Record<PortalPriority, { label: string; className: string }> = {
  immediate: {
    label: "START HERE",
    className: "bg-[#10b981] text-black font-mono text-[10px] font-black uppercase px-2 py-0.5 rounded",
  },
  primary: {
    label: "PRIMARY",
    className: "bg-[#00c5ff] text-black font-mono text-[10px] font-black uppercase px-2 py-0.5 rounded",
  },
  secondary: {
    label: "IF APPLICABLE",
    className: "bg-muted text-foreground font-mono text-[10px] font-bold uppercase px-2 py-0.5 rounded border border-border",
  },
};

/** Official government / regulator portals (CLAUDE.md Section 8, max 3). */
export function PortalList({ portals }: { portals: Portal[] }) {
  if (!portals?.length) return null;
  return (
    <div className="rounded-xl border-2 border-black dark:border-white/30 bg-card p-5 sm:p-6 shadow-sm select-none">
      <div className="flex items-center justify-between mb-4">
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#00c5ff] text-black font-mono text-xs font-black uppercase">
          <Landmark className="h-3.5 w-3.5 stroke-[2.5]" />
          <span>OFFICIAL GRIEVANCE PORTALS</span>
        </span>
        <span className="font-mono text-[11px] text-muted-foreground uppercase font-bold">
          GOVERNMENT BACKED
        </span>
      </div>

      <ul className="space-y-3 mt-2">
        {portals.map((portal, i) => {
          const badge = PRIORITY_BADGES[portal.priority];
          return (
            <li key={`${portal.official_url}-${i}`}>
              <a
                href={portal.official_url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-start justify-between gap-3 rounded-xl border-2 border-border bg-background p-4 hover:border-black dark:hover:border-[#00c5ff] hover:bg-muted/30 transition-all duration-200"
              >
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="font-mono text-sm font-bold text-foreground group-hover:text-[#00c5ff] transition-colors">
                      {portal.name}
                    </span>
                    <span className={badge.className}>
                      {badge.label}
                    </span>
                  </div>
                  <p className="mt-1 text-xs sm:text-sm text-muted-foreground font-medium">
                    {portal.purpose}
                  </p>
                </div>
                <div className="h-8 w-8 rounded-lg border border-border flex items-center justify-center text-muted-foreground group-hover:bg-foreground group-hover:text-background transition-colors shrink-0">
                  <ArrowUpRight className="h-4 w-4" />
                </div>
              </a>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
