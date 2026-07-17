import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowUpRight, Landmark } from "lucide-react";
import type { Portal, PortalPriority } from "@/types/contract";

const PRIORITY_LABEL: Record<PortalPriority, string> = {
  immediate: "Start here",
  primary: "Primary",
  secondary: "If applicable",
};

const PRIORITY_VARIANT: Record<PortalPriority, "default" | "accent" | "muted"> = {
  immediate: "default",
  primary: "accent",
  secondary: "muted",
};

/** Official government / regulator portals (CLAUDE.md Section 8, max 3). */
export function PortalList({ portals }: { portals: Portal[] }) {
  if (!portals?.length) return null;
  return (
    <Card className="p-5 sm:p-6">
      <div className="mb-4 flex items-center gap-2.5">
        <Landmark className="h-5 w-5 text-accent" aria-hidden />
        <h3 className="font-display text-lg font-semibold text-foreground">
          Official portals
        </h3>
      </div>
      <ul className="space-y-3">
        {portals.map((portal, i) => (
          <li key={`${portal.official_url}-${i}`}>
            <a
              href={portal.official_url}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-start justify-between gap-3 rounded-xl border border-white/10 bg-white/[0.02] p-4 transition-colors hover:border-primary/30 hover:bg-white/[0.04]"
            >
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-medium text-foreground">{portal.name}</span>
                  <Badge variant={PRIORITY_VARIANT[portal.priority]}>
                    {PRIORITY_LABEL[portal.priority]}
                  </Badge>
                </div>
                <p className="mt-1 text-sm text-muted-foreground text-pretty">
                  {portal.purpose}
                </p>
              </div>
              <ArrowUpRight
                className="mt-0.5 h-5 w-5 shrink-0 text-muted-foreground transition-colors group-hover:text-primary"
                aria-hidden
              />
            </a>
          </li>
        ))}
      </ul>
    </Card>
  );
}
