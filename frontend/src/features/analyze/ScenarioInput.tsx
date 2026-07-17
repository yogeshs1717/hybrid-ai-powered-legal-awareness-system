import { useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Loader2, ShieldAlert, PackageX, Wallet } from "lucide-react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const MIN = 20;
const MAX = 2000;

const EXAMPLES = [
  {
    icon: ShieldAlert,
    label: "Bank OTP scam",
    text: "Someone called pretending to be my bank and asked for an OTP, then money left my account.",
  },
  {
    icon: PackageX,
    label: "Refund refused",
    text: "I bought a phone online but received a damaged product and the seller refuses a refund.",
  },
  {
    icon: Wallet,
    label: "Unpaid salary",
    text: "My employer has not paid my salary for the last two months despite repeated reminders.",
  },
];

/*
  Scenario capture. Mirrors the gateway's 20–2000 char bound (backend remains the
  authority). The scenario is only ever sent in the POST body — never persisted,
  never placed in a URL (CLAUDE.md Section 9).
*/
export function ScenarioInput({
  onSubmit,
  loading,
}: {
  onSubmit: (scenario: string) => void;
  loading: boolean;
}) {
  const [value, setValue] = useState("");
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
      {/* Soft halo behind the textarea when focused — calm, not flashy. */}
      <div className="group relative rounded-2xl">
        <div
          aria-hidden
          className="pointer-events-none absolute -inset-px rounded-2xl bg-gradient-to-br from-primary/25 via-transparent to-accent/20 opacity-0 blur-sm transition-opacity duration-500 group-focus-within:opacity-100"
        />
        <Textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          maxLength={MAX + 200}
          placeholder="Describe what happened, in your own words. For example: “A shopkeeper sold me fake branded shoes and won't take them back.”"
          aria-label="Describe your situation"
          aria-invalid={tooShort || tooLong}
          className="relative min-h-[190px] bg-white/[0.035] pb-12 text-base backdrop-blur-sm sm:min-h-[200px]"
          onKeyDown={(e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && canSubmit) {
              onSubmit(trimmed);
            }
          }}
        />
        <div className="pointer-events-none absolute bottom-3.5 left-4 right-4 flex items-center justify-between text-xs">
          <span
            aria-live="polite"
            className={cn(
              "tabular-nums text-muted-foreground/70 transition-colors",
              tooShort && "text-accent",
              tooLong && "text-destructive",
            )}
          >
            {tooShort
              ? `${MIN - len} more characters needed`
              : tooLong
                ? `${len - MAX} over the limit`
                : `${len} / ${MAX}`}
          </span>
          <span className="hidden text-muted-foreground/50 sm:inline">
            Ctrl / ⌘ + Enter to analyze
          </span>
        </div>
      </div>

      <div className="mt-5 flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <p className="mb-2 text-[0.7rem] font-medium uppercase tracking-[0.14em] text-muted-foreground/60">
            Try an example
          </p>
          <div className="flex flex-wrap gap-2">
            {EXAMPLES.map((ex) => (
              <button
                key={ex.label}
                type="button"
                disabled={loading}
                onClick={() => setValue(ex.text)}
                className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.03] px-3.5 py-2 text-xs text-muted-foreground transition-all duration-200 hover:border-primary/35 hover:bg-primary/[0.07] hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background active:scale-[0.97] disabled:opacity-50 motion-reduce:active:scale-100"
              >
                <ex.icon className="h-3.5 w-3.5 text-primary/80" aria-hidden />
                {ex.label}
              </button>
            ))}
          </div>
        </div>

        <motion.div whileTap={{ scale: 0.98 }} className="sm:shrink-0">
          <Button type="submit" size="lg" disabled={!canSubmit} className="w-full sm:w-auto">
            {loading ? (
              <>
                <Loader2 className="animate-spin" /> Analyzing…
              </>
            ) : (
              <>
                See the law more clearly <ArrowRight />
              </>
            )}
          </Button>
        </motion.div>
      </div>
    </form>
  );
}
