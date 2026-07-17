import { cn } from "@/lib/utils";

/*
  The LegalLens mark: a magnifying glass whose lens frames three tapering
  "clarity lines" — a document being read and made clearer ("See the law more
  clearly"). Minimal, legal, and integrated into the brand rather than a generic
  floating icon. Rendered with the jade→brass brand gradient.
*/

let uid = 0;

export function LensMark({
  className,
  title = "LegalLens",
}: {
  className?: string;
  title?: string;
}) {
  // Unique gradient ids so multiple marks on one page don't collide.
  const id = `lens-${(uid += 1)}`;
  // An empty title marks the render as purely decorative.
  const decorative = title === "";
  return (
    <svg
      viewBox="0 0 40 40"
      role={decorative ? undefined : "img"}
      aria-label={decorative ? undefined : title}
      aria-hidden={decorative || undefined}
      className={cn("h-9 w-9", className)}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id={`ring-${id}`} x1="6" y1="5" x2="30" y2="31" gradientUnits="userSpaceOnUse">
          <stop stopColor="hsl(var(--primary))" />
          <stop offset="1" stopColor="hsl(var(--accent))" />
        </linearGradient>
        <radialGradient id={`glass-${id}`} cx="0.4" cy="0.35" r="0.8">
          <stop stopColor="hsl(var(--primary) / 0.16)" />
          <stop offset="1" stopColor="hsl(var(--primary) / 0.02)" />
        </radialGradient>
      </defs>

      {/* lens glass */}
      <circle cx="17" cy="17" r="11.5" fill={`url(#glass-${id})`} />
      {/* lens ring */}
      <circle
        cx="17"
        cy="17"
        r="11.5"
        fill="none"
        stroke={`url(#ring-${id})`}
        strokeWidth="2.4"
      />
      {/* clarity lines — a document read clearly through the lens */}
      <g stroke="hsl(var(--accent))" strokeWidth="1.7" strokeLinecap="round" opacity="0.95">
        <line x1="12" y1="14" x2="22" y2="14" />
        <line x1="12" y1="17.5" x2="20.5" y2="17.5" />
        <line x1="12" y1="21" x2="18" y2="21" />
      </g>
      {/* handle */}
      <path
        d="M25.4 25.4 L33 33"
        stroke={`url(#ring-${id})`}
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  );
}
