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
      className="relative rounded-2xl border-2 border-black dark:border-white/30 bg-card p-6 sm:p-8 max-w-md mx-auto shadow-sm select-none"
      role="status"
      aria-live="polite"
      aria-label="Analyzing your situation"
    >
      {/* 4 Corner Handles */}
      <span className="canvas-handle -top-1.5 -left-1.5" />
      <span className="canvas-handle -top-1.5 -right-1.5" />
      <span className="canvas-handle -bottom-1.5 -left-1.5" />
      <span className="canvas-handle -bottom-1.5 -right-1.5" />

      {/* Brand Icon & Status Pill */}
      <div className="mb-6 flex flex-col items-center">
        <LensMark className="h-10 w-10 text-foreground animate-pulse" title="LegalLens" />
        <div className="mt-3 inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#00c5ff]/20 text-[#00c5ff] font-mono text-xs font-bold uppercase tracking-wider">
          <span className="h-2 w-2 rounded-full bg-[#00c5ff] animate-ping" />
          <span>STATUTORY ANALYSIS RUNNING</span>
        </div>
      </div>

      <div className="space-y-3">
        {STAGES.map((label, i) => {
          const done = i < active;
          const current = i === active;
          return (
            <motion.div
              key={label}
              initial={reduce ? false : { opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: reduce ? 0 : i * 0.08 }}
              className={cn(
                "flex items-center justify-between p-2.5 rounded-lg border transition-all duration-200",
                done
                  ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-950 dark:text-emerald-200"
                  : current
                  ? "border-[#00c5ff] bg-[#00c5ff]/10 text-foreground shadow-sm"
                  : "border-border/60 bg-muted/20 text-muted-foreground opacity-60"
              )}
            >
              <div className="flex items-center gap-3">
                <span className="font-mono text-xs font-bold">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span className="text-xs sm:text-sm font-medium">
                  {label}
                </span>
              </div>

              <div>
                {done ? (
                  <Check className="h-4 w-4 text-emerald-600 dark:text-emerald-400 stroke-[3]" />
                ) : current ? (
                  <Loader2 className="h-4 w-4 text-[#00c5ff] animate-spin" />
                ) : (
                  <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground" />
                )}
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
