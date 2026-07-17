import { Scale } from "lucide-react";
import { Card } from "@/components/ui/card";
import { ConfidenceMeter } from "./ConfidenceMeter";
import type { DomainAnalysis } from "@/types/contract";

/** The general area of law the situation appears to relate to. */
export function DomainResultCard({ domain }: { domain: DomainAnalysis }) {
  return (
    <Card className="p-5 sm:p-6">
      <div className="flex items-start gap-4">
        <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-primary/12 text-primary">
          <Scale className="h-5 w-5" aria-hidden />
        </span>
        <div className="min-w-0 flex-1">
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground/80">
            Area of law
          </p>
          <h3 className="mt-0.5 font-display text-xl font-semibold tracking-tight text-foreground">
            {domain.display_name}
          </h3>
          <div className="mt-4">
            <ConfidenceMeter value={domain.confidence} label={domain.confidence_label} />
          </div>
        </div>
      </div>
    </Card>
  );
}
