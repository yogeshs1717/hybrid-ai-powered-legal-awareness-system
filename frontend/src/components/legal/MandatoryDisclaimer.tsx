import { ShieldAlert } from "lucide-react";

/*
  Renders the disclaimer text supplied by the API (CLAUDE.md Section 10 — every
  response, no exceptions). The text is taken from the payload, not hardcoded, so
  the UI never drifts from the backend's approved wording.
*/
export function MandatoryDisclaimer({ text }: { text: string }) {
  return (
    <div
      role="note"
      className="rounded-xl border-2 border-border bg-card p-4 sm:p-5 select-none shadow-sm"
    >
      <div className="flex items-center gap-2 mb-2">
        <span className="p-1 rounded bg-amber-500/20 text-amber-600 dark:text-amber-400">
          <ShieldAlert className="h-4 w-4" />
        </span>
        <span className="font-mono text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
          LEGAL AWARENESS NOTICE (NON-ADVICE)
        </span>
      </div>
      <p className="text-xs sm:text-sm leading-relaxed text-muted-foreground font-medium pl-7">
        {text}
      </p>
    </div>
  );
}
