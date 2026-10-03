import { useState, useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { RotateCcw } from "lucide-react";
import { useAnalyze } from "@/hooks/useAnalyze";
import { ScenarioInput } from "@/features/analyze/ScenarioInput";
import { AnalysisStages } from "@/features/analyze/AnalysisStages";
import { ResultView } from "@/features/analyze/ResultView";
import { AnalyzeErrorCard } from "@/features/analyze/AnalyzeError";

export function AnalyzePage() {
  const location = useLocation();
  const navigate = useNavigate();
  const initialTriggered = useRef(false);
  const analyze = useAnalyze();
  const { data, error, isPending, isSuccess, isError, reset } = analyze;

  const initialScenario = (location.state as { scenario?: string })?.scenario;
  const [submittedScenario, setSubmittedScenario] = useState<string>(initialScenario || "");

  useEffect(() => {
    if (initialScenario && !initialTriggered.current && !isPending && !isSuccess && !data) {
      initialTriggered.current = true;
      setSubmittedScenario(initialScenario);
      analyze.mutate(initialScenario);
    }
  }, [initialScenario, isPending, isSuccess, data, analyze]);

  useEffect(() => {
    if (isSuccess) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }, [isSuccess]);

  const handleReset = () => {
    reset();
    setSubmittedScenario("");
    initialTriggered.current = false;
    if (location.state) {
      navigate(location.pathname, { replace: true, state: {} });
    }
  };

  const showInput = !isPending && !isSuccess;

  return (
    <div className="container max-w-4xl py-10 sm:py-16 select-none">
      <AnimatePresence>
        {showInput && !isError && (
          <motion.section
            key="input"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            {/* Header with Canvas Selection Box */}
            <header className="mx-auto mb-10 max-w-2xl text-center flex flex-col items-center">
              <span className="font-handwriting text-2xl sm:text-3xl text-foreground/80 font-bold -rotate-2">
                your situation
              </span>
              <div className="w-12 h-1 bg-foreground/20 rounded-full mt-0.5 mb-2" />

              <div className="relative inline-block px-7 py-2.5 my-2 border-2 border-black dark:border-[#00c5ff] bg-background/80 backdrop-blur-sm">
                <span className="canvas-handle -top-1.5 -left-1.5" />
                <span className="canvas-handle -top-1.5 -right-1.5" />
                <span className="canvas-handle -bottom-1.5 -left-1.5" />
                <span className="canvas-handle -bottom-1.5 -right-1.5" />
                <h1 className="font-mono text-2xl sm:text-3xl font-extrabold uppercase tracking-tight text-foreground">
                  LEGAL ANALYZER
                </h1>
              </div>

              <p className="mt-3 max-w-lg text-sm font-medium text-muted-foreground text-pretty">
                Describe what happened in plain language. We'll identify the applicable Indian laws,
                provisions, and verified reporting channels.
              </p>
            </header>

            <div className="mx-auto max-w-2xl">
              <ScenarioInput
                onSubmit={(s) => {
                  setSubmittedScenario(s);
                  analyze.mutate(s);
                }}
                loading={isPending}
                initialValue={initialScenario || ""}
              />
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
            <AnalyzeErrorCard error={error} onRetry={handleReset} />
          </motion.section>
        )}

        {isSuccess && data && (
          <motion.section
            key="result"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            <div className="mx-auto mb-8 flex max-w-3xl items-center justify-between gap-4 border-b-2 border-border pb-4">
              <div>
                <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                  LEGAL INTELLIGENCE OUTPUT
                </span>
                <h2 className="font-mono text-xl sm:text-2xl font-black text-foreground">
                  ANALYSIS RESULTS
                </h2>
              </div>
              <button
                type="button"
                onClick={handleReset}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full border-2 border-foreground hover:bg-foreground hover:text-background font-mono text-xs font-bold transition-colors shadow-sm"
              >
                <RotateCcw className="h-3.5 w-3.5" />
                <span>ANALYZE NEW SITUATION</span>
              </button>
            </div>
            <ResultView data={data} scenario={submittedScenario} />
          </motion.section>
        )}
      </AnimatePresence>
    </div>
  );
}
