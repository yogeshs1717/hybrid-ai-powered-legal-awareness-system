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
      className="rounded-xl border-2 border-amber-400 bg-amber-500/10 p-4 sm:p-5 select-none"
    >
      <div className="flex items-center gap-2 mb-1.5">
        <span className="p-1 rounded bg-amber-500 text-black">
          <AlertTriangle className="h-3.5 w-3.5 stroke-[2.5]" />
        </span>
        <span className="font-mono text-xs font-black uppercase text-amber-950 dark:text-amber-200">
          CLARIFICATION HELPFUL
        </span>
      </div>
      <div className="pl-6 text-xs sm:text-sm leading-relaxed text-foreground font-medium">
        <p className="font-bold text-foreground">
          This reading is less certain than usual.
        </p>
        <p className="mt-1 text-muted-foreground">
          {clarificationQuestion ??
            "Adding a little more detail about what happened can help LegalLens understand your situation more clearly."}
        </p>
        <p className="mt-2 text-xs font-mono font-bold text-amber-900 dark:text-amber-300">
          ↓ Preliminary legal provisions and guidance are available below.
        </p>
      </div>
    </div>
  );
}
