import { cn } from "@/lib/utils";
import { LensMark } from "./LensMark";

/*
  LegalLens wordmark lockup. The lens mark reads as the counter of the leading
  "L" — the magnifying glass is part of the name, not a badge beside it.
  "Legal" sits in the foreground; "Lens" carries the jade→brass gradient so the
  lens and the word it names share one identity.
*/

export function Logo({
  className,
  showWordmark = true,
  markClassName,
}: {
  className?: string;
  showWordmark?: boolean;
  markClassName?: string;
}) {
  return (
    <span className={cn("inline-flex items-center gap-2.5 select-none", className)}>
      <LensMark className={cn("h-8 w-8 shrink-0", markClassName)} />
      {showWordmark && (
        <span className="font-display text-xl font-semibold tracking-tight leading-none">
          <span className="text-foreground">Legal</span>
          <span className="text-jade-brass">Lens</span>
        </span>
      )}
    </span>
  );
}
