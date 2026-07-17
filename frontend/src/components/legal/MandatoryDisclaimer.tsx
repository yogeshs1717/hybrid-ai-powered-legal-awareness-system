import { Info } from "lucide-react";

/*
  Renders the disclaimer text supplied by the API (CLAUDE.md Section 10 — every
  response, no exceptions). The text is taken from the payload, not hardcoded, so
  the UI never drifts from the backend's approved wording.
*/
export function MandatoryDisclaimer({ text }: { text: string }) {
  return (
    <div
      role="note"
      className="flex gap-3 rounded-2xl border border-accent/20 bg-accent/[0.06] p-4 sm:p-5"
    >
      <Info className="mt-0.5 h-5 w-5 shrink-0 text-accent" aria-hidden />
      <p className="text-sm leading-relaxed text-muted-foreground text-pretty">
        {text}
      </p>
    </div>
  );
}
