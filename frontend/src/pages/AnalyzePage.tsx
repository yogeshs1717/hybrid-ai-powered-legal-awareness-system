import { AnimatePresence, motion } from "framer-motion";
import { RotateCcw } from "lucide-react";
import { useAnalyze } from "@/hooks/useAnalyze";
import { ScenarioInput } from "@/features/analyze/ScenarioInput";
import { AnalysisStages } from "@/features/analyze/AnalysisStages";
import { ResultView } from "@/features/analyze/ResultView";
import { AnalyzeErrorCard } from "@/features/analyze/AnalyzeError";
import { Button } from "@/components/ui/button";

/*
  The core product surface. A single staged view — input -> loading -> result /
  error — so transitions stay smooth and the scenario never round-trips through a
  URL. No Three.js here (approved design): results must be fast and accessible.
*/
export function AnalyzePage() {
  const analyze = useAnalyze();
  const { data, error, isPending, isSuccess, isError, reset } = analyze;

  const showInput = !isPending && !isSuccess;

  return (
    <div className="container max-w-4xl py-10 sm:py-14">
      <AnimatePresence mode="wait">
        {showInput && !isError && (
          <motion.section
            key="input"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.35 }}
          >
            <header className="mx-auto mb-9 max-w-2xl text-center sm:mb-10">
              <span className="eyebrow justify-center">Scenario analysis</span>
              <h1 className="mt-4 font-display text-3xl font-semibold tracking-tight text-foreground sm:text-4xl text-balance">
                Describe your situation
              </h1>
              <p className="mx-auto mt-4 max-w-xl text-muted-foreground text-pretty">
                Tell LegalLens what happened in plain words. You'll get the area of
                law it relates to, provisions that may apply, and practical next steps
                — with sources you can check yourself.
              </p>
            </header>
            <div className="mx-auto max-w-2xl">
              <ScenarioInput onSubmit={(s) => analyze.mutate(s)} loading={isPending} />
            </div>
          </motion.section>
        )}

        {isPending && (
          <motion.section
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="py-16"
          >
            <AnalysisStages />
          </motion.section>
        )}

        {isError && error && (
          <motion.section
            key="error"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="py-10"
          >
            <AnalyzeErrorCard error={error} onRetry={reset} />
          </motion.section>
        )}

        {isSuccess && data && (
          <motion.section
            key="result"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="mx-auto mb-7 flex max-w-3xl items-end justify-between gap-4">
              <div>
                <span className="eyebrow">Results</span>
                <h1 className="mt-2 font-display text-2xl font-semibold tracking-tight text-foreground sm:text-3xl">
                  Your analysis
                </h1>
              </div>
              <Button variant="outline" size="sm" onClick={reset}>
                <RotateCcw className="h-4 w-4" /> New situation
              </Button>
            </div>
            <ResultView data={data} />
          </motion.section>
        )}
      </AnimatePresence>
    </div>
  );
}
