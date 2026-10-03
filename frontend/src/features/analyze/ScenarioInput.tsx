import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Loader2, Scale } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";

const MIN = 20;
const MAX = 2000;

export function ScenarioInput({
  onSubmit,
  loading,
  initialValue = "",
}: {
  onSubmit: (scenario: string) => void;
  loading: boolean;
  initialValue?: string;
}) {
  const [value, setValue] = useState(initialValue);
  const trimmed = value.trim();
  const len = trimmed.length;
  const tooShort = len > 0 && len < MIN;
  const tooLong = len > MAX;
  const canSubmit = len >= MIN && len <= MAX && !loading;

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (canSubmit) onSubmit(trimmed);
      }}
      className="w-full"
    >
      <div className="relative rounded-xl border-2 border-border bg-card p-2 shadow-sm transition-colors focus-within:border-black dark:focus-within:border-[#00c5ff]">
        <span className="canvas-handle -top-1.5 -left-1.5" />
        <span className="canvas-handle -top-1.5 -right-1.5" />
        <span className="canvas-handle -bottom-1.5 -left-1.5" />
        <span className="canvas-handle -bottom-1.5 -right-1.5" />
        <Textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          maxLength={MAX + 200}
          placeholder="Describe your situation in plain words (English, हिन्दी, or ಕನ್ನಡ)..."
          aria-label="Describe your situation"
          aria-invalid={tooShort || tooLong}
          className="min-h-[200px] sm:min-h-[220px] bg-transparent border-0 text-base focus-visible:ring-0 focus-visible:outline-none resize-y pb-10"
          onKeyDown={(e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && canSubmit) {
              onSubmit(trimmed);
            }
          }}
        />

        {/* Bottom Bar inside the box */}
        <div className="absolute bottom-3 left-4 right-4 flex items-center justify-between text-xs font-mono text-muted-foreground select-none">
          <span
            className={cn(
              "tabular-nums transition-colors font-medium",
              tooShort && "text-amber-500",
              tooLong && "text-destructive",
            )}
          >
            {tooShort
              ? `${MIN - len} more characters needed`
              : tooLong
                ? `${len - MAX} over limit`
                : `${len} / ${MAX}`}
          </span>
          <span className="hidden sm:inline opacity-70">
            Press Ctrl + Enter to submit
          </span>
        </div>
      </div>

      {/* Action Footer */}
      <div className="mt-5 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-xs font-mono text-muted-foreground flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-full bg-[#10b981]" />
          <span>Supports English, हिन्दी, &amp; ಕನ್ನಡ</span>
        </div>

        <motion.div whileTap={{ scale: 0.98 }} className="w-full sm:w-auto">
          <button
            type="submit"
            disabled={!canSubmit}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-lg bg-black text-white dark:bg-white dark:text-black font-mono text-xs font-bold tracking-wider uppercase shadow-md hover:bg-neutral-800 dark:hover:bg-neutral-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          >
            {loading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin text-[#00c5ff]" />
                <span>ANALYZING STATUTES…</span>
              </>
            ) : (
              <>
                <Scale className="h-4 w-4 text-[#00c5ff]" />
                <span>RUN LEGAL ANALYSIS</span>
                <ArrowRight className="h-4 w-4 ml-1" />
              </>
            )}
          </button>
        </motion.div>
      </div>
    </form>
  );
}
