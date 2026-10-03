import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Scale,
  ShoppingBag,
  Briefcase,
  FileText,
  ArrowRight,
  Sparkles,
  Search,
  Car,
  RotateCcw,
} from "lucide-react";
import { ScenarioInput } from "@/features/analyze/ScenarioInput";
import { useAnalyze } from "@/hooks/useAnalyze";
import { AnalysisStages } from "@/features/analyze/AnalysisStages";
import { ResultView } from "@/features/analyze/ResultView";
import { AnalyzeErrorCard } from "@/features/analyze/AnalyzeError";

export function LandingPage() {
  const analyze = useAnalyze();
  const { data, error, isPending, isSuccess, isError, reset } = analyze;
  const [submittedScenario, setSubmittedScenario] = useState<string>("");

  useEffect(() => {
    if (isSuccess) {
      const el = document.getElementById("analyze-section");
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
  }, [isSuccess]);
  return (
    <div className="relative min-h-[calc(100vh-5rem)] flex flex-col justify-between overflow-x-hidden px-4 sm:px-6 py-10 sm:py-16 select-none">
      {/* ---------- Canvas Sticky Notes / Tags (Like Reference Image 2) ---------- */}
      <div className="max-w-5xl mx-auto w-full relative">
        {/* Left Sticky Note (Mint Green, tilted -6deg) */}
        <div className="hidden lg:block absolute -top-4 left-12 z-20 -rotate-6 transition-transform hover:rotate-0 duration-200">
          <div className="bg-[#a7f3d0] dark:bg-[#065f46] text-emerald-950 dark:text-emerald-100 font-mono text-xs px-3.5 py-1.5 rounded shadow-sm border border-emerald-300 dark:border-emerald-700">
            Updated for BNS 2024
          </div>
        </div>

        {/* Right Sticky Note (Warm Amber, tilted +6deg) */}
        <div className="hidden lg:block absolute -top-4 right-16 z-20 rotate-6 transition-transform hover:rotate-0 duration-200">
          <div className="bg-[#fef08a] dark:bg-[#854d0e] text-amber-950 dark:text-amber-100 font-mono text-xs px-3.5 py-1.5 rounded shadow-sm border border-amber-300 dark:border-amber-700">
            Official Indian Law Data
          </div>
        </div>

        {/* Floating Speech Bubble (Magenta, right side) */}
        <div className="hidden md:block absolute top-36 right-0 sm:-right-4 z-20 rotate-3">
          <div className="speech-bubble bg-[#e11d48] text-white text-[11px] font-mono font-bold px-3 py-1 rounded shadow-md">
            All 28 States &amp; UTs 🇮🇳
          </div>
        </div>

        {/* Floating User Cursor Sticker (Like Reference Image 2 "YOU") */}
        <div className="hidden md:flex absolute top-24 -right-12 z-20 items-center gap-1.5">
          <div className="h-7 w-7 rounded-full bg-black text-white dark:bg-white dark:text-black flex items-center justify-center text-[10px] font-mono font-bold shadow-md">
            YOU
          </div>
          <svg className="w-4 h-4 -rotate-45 text-black dark:text-white" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3 3l7 18 3-7 7-3L3 3z" />
          </svg>
        </div>

        {/* ---------- Left Polaroid Photo Card (Like Reference Image 1) ---------- */}
        <motion.div
          initial={{ opacity: 0, x: -20, rotate: -8 }}
          animate={{ opacity: 1, x: 0, rotate: -8 }}
          transition={{ duration: 0.6 }}
          className="hidden xl:block absolute top-16 -left-16 z-10 hover:rotate-0 transition-transform duration-300"
        >
          <div className="polaroid-card w-44">
            <div className="h-32 bg-slate-100 dark:bg-slate-800 rounded-sm flex flex-col items-center justify-center p-3 text-center border border-border/40">
              <Scale className="h-10 w-10 text-primary mb-1 stroke-[1.75]" />
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-muted-foreground">
                Bharatiya Nyaya
              </span>
            </div>
            <p className="font-handwriting text-center text-lg text-slate-800 dark:text-slate-200 mt-2 font-bold">
              legal rights 2026
            </p>
          </div>
        </motion.div>

        {/* ---------- Right Polaroid Photo Card (Like Reference Image 1) ---------- */}
        <motion.div
          initial={{ opacity: 0, x: 20, rotate: 8 }}
          animate={{ opacity: 1, x: 0, rotate: 8 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="hidden xl:block absolute top-20 -right-20 z-10 hover:rotate-0 transition-transform duration-300"
        >
          <div className="polaroid-card w-44">
            <div className="h-32 bg-slate-100 dark:bg-slate-800 rounded-sm flex flex-col items-center justify-center p-3 text-center border border-border/40">
              <Sparkles className="h-10 w-10 text-[#00c5ff] mb-1 stroke-[1.75]" />
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-muted-foreground">
                Grievance Portals
              </span>
            </div>
            <p className="font-handwriting text-center text-lg text-slate-800 dark:text-slate-200 mt-2 font-bold">
              official sources
            </p>
          </div>
        </motion.div>

        {/* ---------- Hero Center: Figma Selection Box (Like Reference Image 1 & 2) ---------- */}
        <div className="flex flex-col items-center text-center">
          {/* Handwritten Annotation above the selection box */}
          <div className="mb-2 flex flex-col items-center">
            <span className="font-handwriting text-2xl sm:text-3xl text-foreground/80 font-bold -rotate-2">
              what's up
            </span>
            <div className="w-12 h-1 bg-foreground/20 rounded-full mt-0.5" />
          </div>

          {/* Interactive Bounding Selection Box */}
          <div className="relative inline-block px-8 py-3 my-2 border-2 border-black dark:border-[#00c5ff] bg-background/80 backdrop-blur-sm shadow-sm select-none">
            {/* 8 Transform Handles */}
            <span className="canvas-handle -top-1.5 -left-1.5" />
            <span className="canvas-handle -top-1.5 left-1/2 -translate-x-1/2" />
            <span className="canvas-handle -top-1.5 -right-1.5" />
            <span className="canvas-handle top-1/2 -translate-y-1/2 -left-1.5" />
            <span className="canvas-handle top-1/2 -translate-y-1/2 -right-1.5" />
            <span className="canvas-handle -bottom-1.5 -left-1.5" />
            <span className="canvas-handle -bottom-1.5 left-1/2 -translate-x-1/2" />
            <span className="canvas-handle -bottom-1.5 -right-1.5" />

            <h1 className="font-mono text-2xl sm:text-4xl font-extrabold uppercase tracking-tight text-foreground">
              LEGAL LENS
            </h1>
          </div>

          {/* Tagline Pill */}
          <div className="flex items-center gap-2 mt-3 text-xs font-mono font-bold text-muted-foreground tracking-wider uppercase">
            <span className="h-2 w-2 rounded-full bg-[#00c5ff] animate-pulse" />
            <span>100% Free Public Legal Awareness</span>
          </div>

          {/* Short, Minimal Subtitle (No bulky headings) */}
          <p className="mt-3 font-mono text-sm sm:text-base font-semibold text-foreground/80 tracking-tight">
            Indian Laws &amp; Legal Rights, Simplified.
          </p>

          {/* Main Action Buttons */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="#analyze-section"
              className="inline-flex items-center gap-3 px-7 py-3.5 bg-black text-white dark:bg-white dark:text-black font-mono text-sm font-bold tracking-wider rounded-lg shadow-lg hover:bg-neutral-800 dark:hover:bg-neutral-200 transition-transform active:scale-95"
            >
              <div className="h-5 w-5 rounded bg-[#00c5ff] flex items-center justify-center text-black">
                <Search className="h-3 w-3 stroke-[3]" />
              </div>
              <span>ANALYZE YOUR SITUATION</span>
              <ArrowRight className="h-4 w-4" />
            </a>

            <a
              href="#how-it-works-section"
              className="inline-flex items-center gap-2 px-6 py-3.5 border-2 border-border bg-card/80 hover:bg-muted font-mono text-xs font-bold tracking-wider rounded-lg transition-colors"
            >
              <span>HOW IT WORKS</span>
            </a>
          </div>
        </div>
      </div>

      {/* ---------- Capability Tiles ---------- */}
      <div className="max-w-5xl mx-auto w-full mt-14 sm:mt-16">
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5">
          {/* Tile 1: Yellow (Cyber Fraud) */}
          <div className="flex items-center justify-between bg-[#f59e0b] text-black px-4 py-3 rounded-lg shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all font-bold text-sm select-none">
            <span>Cyber Fraud</span>
            <span className="grid grid-cols-2 gap-0.5 p-1 bg-black/10 rounded">
              <span className="w-1.5 h-1.5 bg-black rounded-[1px]" />
              <span className="w-1.5 h-1.5 bg-black rounded-[1px]" />
              <span className="w-1.5 h-1.5 bg-black rounded-[1px]" />
              <span className="w-1.5 h-1.5 bg-black rounded-[1px]" />
            </span>
          </div>

          {/* Tile 2: Green (Consumer Rights) */}
          <div className="flex items-center justify-between bg-[#10b981] text-black px-4 py-3 rounded-lg shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all font-bold text-sm select-none">
            <span>Consumer Rights</span>
            <span className="p-1 bg-black/10 rounded">
              <ShoppingBag className="w-4 h-4 text-black stroke-[2.5]" />
            </span>
          </div>

          {/* Tile 3: Purple (Traffic Enforcement) */}
          <div className="flex items-center justify-between bg-[#8b5cf6] text-white px-4 py-3 rounded-lg shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all font-bold text-sm select-none">
            <span>Traffic Enforcement</span>
            <span className="p-1 bg-white/20 rounded">
              <Car className="w-4 h-4 text-white stroke-[2.5]" />
            </span>
          </div>

          {/* Tile 4: Magenta (Labor & Wages) */}
          <div className="flex items-center justify-between bg-[#e11d48] text-white px-4 py-3 rounded-lg shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all font-bold text-sm select-none">
            <span>Labor &amp; Wages</span>
            <span className="p-1 bg-white/20 rounded">
              <Briefcase className="w-4 h-4 text-white stroke-[2.5]" />
            </span>
          </div>

          {/* Tile 5: Cyan (Contract Law) */}
          <div className="flex items-center justify-between bg-[#00c5ff] text-black px-4 py-3 rounded-lg shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all font-bold text-sm select-none col-span-2 sm:col-span-1">
            <span>Contract Law</span>
            <span className="p-1 bg-black/10 rounded">
              <FileText className="w-4 h-4 text-black stroke-[2.5]" />
            </span>
          </div>
        </div>
      </div>

      {/* ---------- Dedicated Section 02: ANALYZE YOUR SITUATION ---------- */}
      <section id="analyze-section" className="max-w-3xl mx-auto w-full mt-24 sm:mt-32 pt-8 scroll-mt-20">
        <div className="flex flex-col items-center text-center mb-8">
          <span className="font-handwriting text-2xl sm:text-3xl text-foreground/80 font-bold -rotate-2">
            try it right here
          </span>
          <div className="w-12 h-1 bg-foreground/20 rounded-full mt-0.5 mb-2" />

          <div className="relative inline-block px-7 py-2.5 my-2 border-2 border-black dark:border-[#00c5ff] bg-background/80 backdrop-blur-sm">
            <span className="canvas-handle -top-1.5 -left-1.5" />
            <span className="canvas-handle -top-1.5 -right-1.5" />
            <span className="canvas-handle -bottom-1.5 -left-1.5" />
            <span className="canvas-handle -bottom-1.5 -right-1.5" />
            <h2 className="font-mono text-xl sm:text-2xl font-extrabold uppercase tracking-tight text-foreground">
              02 / LEGAL ANALYZER
            </h2>
          </div>

          <p className="mt-2 text-xs sm:text-sm font-medium text-muted-foreground max-w-md">
            Type what happened in plain language. We'll find relevant Indian statutory provisions and verified portals.
          </p>
        </div>

        {/* Embedded Scenario Input & Results */}
        {!isPending && !isSuccess && !isError && (
          <div className="bg-card/70 backdrop-blur-sm rounded-2xl border-2 border-border p-4 sm:p-6 shadow-sm">
            <ScenarioInput
              onSubmit={(scenario) => {
                setSubmittedScenario(scenario);
                analyze.mutate(scenario);
              }}
              loading={isPending}
            />
          </div>
        )}

        {isPending && (
          <div className="py-8">
            <AnalysisStages />
          </div>
        )}

        {isError && error && (
          <div className="py-6">
            <AnalyzeErrorCard error={error} onRetry={reset} />
          </div>
        )}

        {isSuccess && data && (
          <div className="space-y-6">
            <div className="flex items-center justify-between gap-4 border-b-2 border-border pb-4">
              <div>
                <span className="font-mono text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                  LEGAL INTELLIGENCE OUTPUT
                </span>
                <h3 className="font-mono text-xl sm:text-2xl font-black text-foreground">
                  ANALYSIS RESULTS
                </h3>
              </div>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => {
                    reset();
                    setSubmittedScenario("");
                  }}
                  className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full border-2 border-foreground hover:bg-foreground hover:text-background font-mono text-xs font-bold transition-colors shadow-sm"
                >
                  <RotateCcw className="h-3.5 w-3.5" />
                  <span>ANALYZE NEW SITUATION</span>
                </button>
              </div>
            </div>

            <ResultView data={data} scenario={submittedScenario} />
          </div>
        )}
      </section>

      {/* ---------- Dedicated Section 03: HOW IT WORKS ---------- */}
      <section id="how-it-works-section" className="max-w-4xl mx-auto w-full mt-24 sm:mt-32 pt-8 scroll-mt-20">
        <div className="flex flex-col items-center text-center mb-12">
          <span className="font-handwriting text-2xl sm:text-3xl text-foreground/80 font-bold rotate-2">
            4 simple steps
          </span>
          <div className="w-12 h-1 bg-foreground/20 rounded-full mt-0.5 mb-2" />

          <div className="relative inline-block px-7 py-2.5 my-2 border-2 border-black dark:border-[#00c5ff] bg-background/80 backdrop-blur-sm">
            <span className="canvas-handle -top-1.5 -left-1.5" />
            <span className="canvas-handle -top-1.5 -right-1.5" />
            <span className="canvas-handle -bottom-1.5 -left-1.5" />
            <span className="canvas-handle -bottom-1.5 -right-1.5" />
            <h2 className="font-mono text-xl sm:text-2xl font-extrabold uppercase tracking-tight text-foreground">
              03 / HOW IT WORKS
            </h2>
          </div>

          <p className="mt-2 text-xs sm:text-sm font-medium text-muted-foreground max-w-md">
            A transparent pipeline from your real-life scenario to verified Indian legal protections.
          </p>
        </div>

        {/* 4 Interactive Step Cards */}
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="rounded-xl border-2 border-border bg-card p-5 shadow-sm hover:-translate-y-1 transition-transform">
            <div className="flex items-center justify-between mb-3">
              <span className="px-2.5 py-1 rounded bg-[#f59e0b] text-black font-mono text-xs font-black">
                STEP 01
              </span>
              <span className="font-mono text-[11px] text-muted-foreground">INPUT</span>
            </div>
            <h3 className="font-mono text-base font-bold text-foreground">Describe your situation</h3>
            <p className="mt-1.5 text-xs sm:text-sm text-muted-foreground leading-relaxed">
              Write in plain English, Hindi, or Kannada. No legal jargon or section numbers needed.
            </p>
          </div>

          <div className="rounded-xl border-2 border-border bg-card p-5 shadow-sm hover:-translate-y-1 transition-transform">
            <div className="flex items-center justify-between mb-3">
              <span className="px-2.5 py-1 rounded bg-[#10b981] text-black font-mono text-xs font-black">
                STEP 02
              </span>
              <span className="font-mono text-[11px] text-muted-foreground">AI NLP</span>
            </div>
            <h3 className="font-mono text-base font-bold text-foreground">LegalLens analyzes the issue</h3>
            <p className="mt-1.5 text-xs sm:text-sm text-muted-foreground leading-relaxed">
              Extracts factual indicators and classifies the legal domain with strict confidence scoring.
            </p>
          </div>

          <div className="rounded-xl border-2 border-border bg-card p-5 shadow-sm hover:-translate-y-1 transition-transform">
            <div className="flex items-center justify-between mb-3">
              <span className="px-2.5 py-1 rounded bg-[#e11d48] text-white font-mono text-xs font-black">
                STEP 03
              </span>
              <span className="font-mono text-[11px] text-muted-foreground">STATUTES</span>
            </div>
            <h3 className="font-mono text-base font-bold text-foreground">Matches verified statutes</h3>
            <p className="mt-1.5 text-xs sm:text-sm text-muted-foreground leading-relaxed">
              Displays relevant sections from Bharatiya Nyaya Sanhita, Motor Vehicles Act, IT Act, and Consumer Act.
            </p>
          </div>

          <div className="rounded-xl border-2 border-border bg-card p-5 shadow-sm hover:-translate-y-1 transition-transform">
            <div className="flex items-center justify-between mb-3">
              <span className="px-2.5 py-1 rounded bg-[#00c5ff] text-black font-mono text-xs font-black">
                STEP 04
              </span>
              <span className="font-mono text-[11px] text-muted-foreground">ACTION</span>
            </div>
            <h3 className="font-mono text-base font-bold text-foreground">Action steps &amp; portals</h3>
            <p className="mt-1.5 text-xs sm:text-sm text-muted-foreground leading-relaxed">
              Direct access to official grievance portals (e.g. cybercrime.gov.in, National Consumer Helpline).
            </p>
          </div>
        </div>

        <div className="mt-6 text-center">
          <Link
            to="/how-it-works"
            className="inline-flex items-center gap-2 font-mono text-xs font-bold text-foreground hover:text-[#00c5ff] transition-colors underline underline-offset-4"
          >
            <span>VIEW FULL COVERAGE &amp; LIMITS GUIDE</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </section>

      {/* Minimal Legal Awareness Notice */}
      <div className="max-w-4xl mx-auto w-full mt-16 text-center">
        <p className="text-[11px] font-mono text-muted-foreground/80">
          LegalLens provides public legal awareness only and does not constitute formal legal advice.
        </p>
      </div>
    </div>
  );
}
