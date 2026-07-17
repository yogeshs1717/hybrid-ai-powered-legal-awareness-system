import { useEffect, useState } from "react";
import { motion, useReducedMotion } from "framer-motion";
import { Check, Loader2 } from "lucide-react";
import { LensMark } from "@/components/brand/LensMark";
import { cn } from "@/lib/utils";

/*
  Calm, honest loading state. The labels are user-facing and non-technical — they
  never expose classifiers or similarity internals — but they do reflect the real
  order of work, so the wait feels intentional rather than theatrical.
*/
const STAGES = [
  "Reading your situation",
  "Identifying the area of law",
  "Finding relevant provisions",
  "Preparing your next steps",
];

export function AnalysisStages() {
  const reduce = useReducedMotion();
  const [active, setActive] = useState(0);

  useEffect(() => {
    if (reduce) return;
    const id = setInterval(() => {
      setActive((a) => (a < STAGES.length - 1 ? a + 1 : a));
    }, 900);
    return () => clearInterval(id);
  }, [reduce]);

  return (
    <div
      className="glass mx-auto max-w-md rounded-3xl p-6 sm:p-8"
      role="status"
      aria-live="polite"
      aria-label="Analyzing your situation"
    >
      {/* Brand pulse — the lens at work. */}
      <div className="mb-6 flex justify-center">
        <span className="relative grid place-items-center">
          <span
            aria-hidden
            className="absolute h-14 w-14 animate-pulse-ring rounded-full border border-primary/40 motion-reduce:hidden"
          />
          <LensMark className="h-10 w-10" title="" />
        </span>
      </div>

      <div className="flex flex-col gap-0.5">
        {STAGES.map((label, i) => {
          const done = i < active;
          const current = i === active;
          return (
            <motion.div
              key={label}
              initial={reduce ? false : { opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: reduce ? 0 : i * 0.08 }}
              className="flex items-center gap-3.5 py-2"
            >
              <span
                className={cn(
                  "grid h-7 w-7 shrink-0 place-items-center rounded-full border transition-colors duration-300",
                  done && "border-primary/40 bg-primary/15 text-primary",
                  current && "border-primary/50 bg-primary/10 text-primary",
                  !done && !current && "border-white/10 text-muted-foreground/50",
                )}
              >
                {done ? (
                  <Check className="h-4 w-4" />
                ) : current ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <span className="h-1.5 w-1.5 rounded-full bg-current" />
                )}
              </span>
              <span
                className={cn(
                  "text-sm transition-colors duration-300",
                  (done || current) ? "text-foreground" : "text-muted-foreground/60",
                )}
              >
                {label}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
