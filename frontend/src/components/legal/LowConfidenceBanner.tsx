import { AlertTriangle } from "lucide-react";

/*
  Low-confidence / clarification prompt (CLAUDE.md Section 8.2). This arrives on
  the HTTP 200 success path — it is NOT an error. Tone stays calm and cautious
  (Section 10): it never implies a wrong answer, only that more detail helps.
*/
export function LowConfidenceBanner({
  clarificationQuestion,
}: {
  clarificationQuestion: string | null;
}) {
  return (
    <div
      role="status"
      className="flex gap-3 rounded-2xl border border-accent/25 bg-accent/[0.07] p-4 sm:p-5"
    >
      <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-accent" aria-hidden />
      <div className="text-sm leading-relaxed text-pretty">
        <p className="font-medium text-foreground">
          This reading is less certain than usual.
        </p>
        <p className="mt-1 text-muted-foreground">
          {clarificationQuestion ??
            "Adding a little more detail about what happened can help LegalLens understand your situation more clearly."}
        </p>
      </div>
    </div>
  );
}
