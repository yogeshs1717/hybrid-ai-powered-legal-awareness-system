import { BookOpen, ExternalLink, ShieldCheck } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
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
    <Card className="overflow-hidden transition-colors duration-300 hover:border-white/[0.15]">
      <div className="border-b border-white/10 bg-white/[0.02] p-5 sm:p-6">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="default">
            <ShieldCheck className="h-3.5 w-3.5" aria-hidden />
            Verified provision
          </Badge>
          <span className="text-xs text-muted-foreground/70">#{index + 1}</span>
        </div>
        <div className="mt-3 flex items-start gap-3">
          <span className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-primary/12 text-primary">
            <BookOpen className="h-5 w-5" aria-hidden />
          </span>
          <div className="min-w-0">
            <h4 className="font-display text-lg font-semibold leading-tight text-foreground">
              {provision.act} · {provision.section}
            </h4>
            {provision.title && (
              <p className="mt-0.5 text-sm text-muted-foreground text-pretty">
                {provision.title}
              </p>
            )}
          </div>
        </div>
      </div>

      <div className="space-y-4 p-5 sm:p-6">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground/70">
            In plain language
          </p>
          <p className="mt-1.5 text-sm leading-relaxed text-foreground/90 text-pretty">
            {provision.simplified_explanation}
          </p>
        </div>

        <div className="rounded-xl border border-primary/15 bg-primary/[0.05] p-3.5">
          <p className="text-xs font-medium uppercase tracking-wider text-primary/90">
            Why this may be relevant
          </p>
          <p className="mt-1.5 text-sm leading-relaxed text-foreground/90 text-pretty">
            {provision.provision_relevance_rationale}
          </p>
        </div>

        {official_source?.url ? (
          <a
            href={official_source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-primary hover:underline"
          >
            <ExternalLink className="h-4 w-4" aria-hidden />
            View on {official_source.name}
          </a>
        ) : (
          <p className="text-xs text-muted-foreground/70">
            Source: {official_source?.name ?? "Official source"}
          </p>
        )}
      </div>
    </Card>
  );
}
