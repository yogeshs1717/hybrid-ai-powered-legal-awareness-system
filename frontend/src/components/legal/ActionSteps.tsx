import { Card } from "@/components/ui/card";
import { ListChecks } from "lucide-react";

/*
  Issue-specific next steps (CLAUDE.md Section 8). Rendered in the order the API
  returns them — most time-sensitive first. The UI adds no steps of its own.
*/
export function ActionSteps({ steps }: { steps: string[] }) {
  if (!steps?.length) return null;
  return (
    <Card className="p-5 sm:p-6">
      <div className="mb-4 flex items-center gap-2.5">
        <ListChecks className="h-5 w-5 text-primary" aria-hidden />
        <h3 className="font-display text-lg font-semibold text-foreground">
          Suggested next steps
        </h3>
      </div>
      <ol className="space-y-3">
        {steps.map((step, i) => (
          <li key={i} className="flex gap-3.5">
            <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-primary/12 text-sm font-semibold text-primary">
              {i + 1}
            </span>
            <p className="pt-0.5 text-sm leading-relaxed text-foreground/90 text-pretty">
              {step}
            </p>
          </li>
        ))}
      </ol>
    </Card>
  );
}
