import { Card } from "@/components/ui/card";
import { FileSearch } from "lucide-react";

/*
  The explicit safe state (CLAUDE.md Section 8 & 14): when no manually-verified,
  in-force provision exists for the detected situation, LegalLens says so plainly
  — it never invents a legal answer and never renders an empty section. Action
  steps and portals may still be shown alongside this state by the caller.
*/
export function NoVerifiedProvisionState() {
  return (
    <Card className="p-6 sm:p-8">
      <div className="flex flex-col items-start gap-4 sm:flex-row">
        <span className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-accent/12 text-accent">
          <FileSearch className="h-6 w-6" aria-hidden />
        </span>
        <div>
          <h3 className="font-display text-xl font-semibold text-foreground">
            No verified legal provision to show yet
          </h3>
          <p className="mt-2 text-sm leading-relaxed text-muted-foreground text-pretty">
            LegalLens only shows legal provisions that a person has checked against an
            official government source. For this situation, there isn't a verified
            provision available to display right now — so rather than guess, we're
            being upfront about it. The steps and official portals below can still help
            you move forward.
          </p>
        </div>
      </div>
    </Card>
  );
}
