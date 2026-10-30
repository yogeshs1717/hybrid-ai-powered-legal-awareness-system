import { AlertTriangle, ArrowRight, RotateCcw, ShieldAlert, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

interface UnknownScenarioFallbackCardProps {
  fallbackMessage?: string | null;
  onReset?: () => void;
  onSelectExample?: (scenarioText: string) => void;
}

const SAMPLE_SCENARIOS = [
  {
    domain: "Cyber Fraud",
    act: "Information Technology Act, 2000",
    color: "border-sky-500/40 bg-sky-500/5 hover:border-sky-500",
    badgeBg: "bg-sky-500/15 text-sky-700 dark:text-sky-300",
    scenario:
      "Someone called pretending to be bank manager and asked for OTP, then 40000 was debited from my account",
  },
  {
    domain: "Consumer Issues",
    act: "Consumer Protection Act, 2019",
    color: "border-emerald-500/40 bg-emerald-500/5 hover:border-emerald-500",
    badgeBg: "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300",
    scenario:
      "I bought a new washing machine from an appliance store but it does not spin and company refuses replacement or refund",
  },
  {
    domain: "Traffic Enforcement",
    act: "Motor Vehicles Act, 1988",
    color: "border-amber-500/40 bg-amber-500/5 hover:border-amber-500",
    badgeBg: "bg-amber-500/15 text-amber-700 dark:text-amber-300",
    scenario:
      "Traffic police seized my bike key and took my bike without giving any seizure memo or official receipt",
  },
  {
    domain: "Workplace & Wage",
    act: "Code on Wages, 2019",
    color: "border-purple-500/40 bg-purple-500/5 hover:border-purple-500",
    badgeBg: "bg-purple-500/15 text-purple-700 dark:text-purple-300",
    scenario:
      "My employer has withheld my salary for past 3 months despite several reminders and full work attendance",
  },
  {
    domain: "Contractual Disputes",
    act: "Indian Contract Act, 1872",
    color: "border-rose-500/40 bg-rose-500/5 hover:border-rose-500",
    badgeBg: "bg-rose-500/15 text-rose-700 dark:text-rose-300",
    scenario:
      "I paid an advance of 50000 to an interior contractor with a signed agreement but he stopped work midway and ran away",
  },
];

export function UnknownScenarioFallbackCard({
  fallbackMessage,
  onReset,
  onSelectExample,
}: UnknownScenarioFallbackCardProps) {
  const defaultMsg =
    "We could not identify a valid legal scenario or dispute from your description. " +
    "Please enter a specific legal situation (such as cyber fraud, unauthorized debits, " +
    "defective products, consumer complaints, traffic challans, unpaid salary, or breach of contract) " +
    "with clear details about what happened so we can identify the applicable laws and action steps.";

  return (
    <div className="flex flex-col gap-5 select-none">
      {/* Fallback Alert Banner */}
      <div className="relative rounded-xl border-2 border-amber-500 bg-amber-500/10 p-5 sm:p-6 shadow-sm overflow-hidden">
        <span className="canvas-handle -top-1.5 -left-1.5" />
        <span className="canvas-handle -top-1.5 -right-1.5" />
        <span className="canvas-handle -bottom-1.5 -left-1.5" />
        <span className="canvas-handle -bottom-1.5 -right-1.5" />

        <div className="flex items-center gap-2 mb-3">
          <span className="p-1 rounded bg-amber-500 text-black">
            <ShieldAlert className="h-4 w-4 stroke-[2.5]" />
          </span>
          <span className="font-mono text-xs font-black uppercase text-amber-950 dark:text-amber-200 tracking-wider">
            LEGAL SCENARIO NOT RECOGNIZED
          </span>
        </div>

        <h3 className="font-mono text-base sm:text-lg font-bold text-foreground">
          Please enter a valid legal scenario or dispute
        </h3>

        <p className="mt-2 text-xs sm:text-sm leading-relaxed text-foreground font-medium">
          {fallbackMessage || defaultMsg}
        </p>

        <div className="mt-4 flex flex-wrap items-center gap-3 pt-3 border-t border-amber-500/30">
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground font-medium">
            <AlertTriangle className="h-3.5 w-3.5 text-amber-600 dark:text-amber-400 shrink-0" />
            <span>
              LegalLens provides awareness for real legal grievances. Random sentences, greetings, or non-legal questions cannot be matched to laws.
            </span>
          </div>

          {onReset && (
            <button
              type="button"
              onClick={onReset}
              className="mt-1 inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg border border-amber-600/50 bg-amber-500/20 hover:bg-amber-500/30 text-amber-950 dark:text-amber-100 font-mono text-xs font-bold transition-colors"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              <span>Enter a Different Scenario</span>
            </button>
          )}
        </div>
      </div>

      {/* Suggested Examples Container */}
      <div className="rounded-xl border-2 border-border bg-card p-5 sm:p-6 shadow-sm">
        <div className="flex items-center justify-between gap-2 mb-3 pb-2 border-b border-border/60">
          <div className="flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-primary" />
            <h4 className="font-mono text-xs font-black uppercase tracking-wider text-foreground">
              SUPPORTED LEGAL AREAS & SAMPLE SCENARIOS
            </h4>
          </div>
          <span className="font-mono text-[10px] font-bold text-muted-foreground uppercase px-2 py-0.5 rounded bg-muted/60">
            5 DOMAINS SUPPORTED
          </span>
        </div>

        <p className="text-xs text-muted-foreground font-medium mb-4">
          Click any sample below to see how LegalLens identifies applicable statutes, sections, and grievance portals:
        </p>

        <div className="grid gap-3 sm:grid-cols-1">
          {SAMPLE_SCENARIOS.map((item) => (
            <motion.div
              key={item.domain}
              whileHover={{ scale: 1.01 }}
              transition={{ duration: 0.15 }}
              onClick={() => onSelectExample && onSelectExample(item.scenario)}
              className={`group cursor-pointer rounded-lg border-2 p-3 sm:p-4 transition-all duration-150 ${item.color}`}
            >
              <div className="flex items-center justify-between gap-2 mb-1.5">
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded font-mono text-[10px] font-black uppercase tracking-wider ${item.badgeBg}`}>
                    {item.domain}
                  </span>
                  <span className="font-mono text-[11px] text-muted-foreground hidden sm:inline">
                    ({item.act})
                  </span>
                </div>
                <span className="inline-flex items-center gap-1 text-[11px] font-mono font-bold text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                  <span>Try this scenario</span>
                  <ArrowRight className="h-3 w-3" />
                </span>
              </div>
              <p className="text-xs sm:text-sm font-medium text-foreground leading-relaxed italic">
                "{item.scenario}"
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
