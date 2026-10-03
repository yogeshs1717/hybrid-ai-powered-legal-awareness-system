import { Link } from "react-router-dom";
import {
  PencilLine,
  ScanSearch,
  ScrollText,
  Compass,
  ArrowRight,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Sparkles,
} from "lucide-react";

const PIPELINE_STEPS = [
  {
    step: "01",
    label: "INPUT",
    tagColor: "bg-[#f59e0b] text-black",
    handwritten: "in your own words",
    icon: PencilLine,
    title: "You Describe What Happened",
    body: "Write naturally in everyday English, हिन्दी, or ಕನ್ನಡ. No legal terminology, IPC sections, or formal jargon required.",
  },
  {
    step: "02",
    label: "NLP ENGINE",
    tagColor: "bg-[#10b981] text-black",
    handwritten: "AI domain match",
    icon: ScanSearch,
    title: "LegalLens Identifies The Issue",
    body: "The model extracts key factual signals and classifies the situation into specific Indian legal domains with strict confidence scoring.",
  },
  {
    step: "03",
    label: "STATUTE MAP",
    tagColor: "bg-[#e11d48] text-white",
    handwritten: "verified laws only",
    icon: ScrollText,
    title: "Matches Verified Statutes",
    body: "We map your situation to checked provisions from Bharatiya Nyaya Sanhita 2024, Motor Vehicles Act 1988, IT Act, and Consumer Protection Act.",
  },
  {
    step: "04",
    label: "ACTION PLAN",
    tagColor: "bg-[#00c5ff] text-black",
    handwritten: "official next steps",
    icon: Compass,
    title: "Grievance Channels & Next Steps",
    body: "You receive ordered practical steps and direct links to official government reporting portals (cybercrime.gov.in, e-daakhil).",
  },
];

const SCOPE_IN = [
  { title: "Cyber Fraud & Online Scams", desc: "OTP theft, UPI fraud, unauthorized banking, impersonation" },
  { title: "Consumer Rights & Deficiencies", desc: "Defective goods, refund denials, misleading ads, unfair trade" },
  { title: "Traffic & Motor Violations", desc: "Fine disputes, e-challans, license & vehicle documentation" },
  { title: "Workplace & Wage Issues", desc: "Unpaid salary, wrongful termination, employment agreement breaches" },
  { title: "Contractual & Tenancy Disputes", desc: "Security deposits, tenancy agreements, service agreement disputes" },
];

const SCOPE_OUT = [
  { title: "Criminal Trial Defense & Bail", desc: "Arrests, criminal trials, bail applications require an advocate" },
  { title: "Predicting Case Outcomes", desc: "We never speculate on whether you will 'win' or 'lose' a case" },
  { title: "Court Filing & Petitions", desc: "Filing formal petitions in high courts or district courts" },
  { title: "Replacing a Licensed Lawyer", desc: "Educational awareness only — not personalized advocate representation" },
];

const FAQS = [
  {
    q: "Is LegalLens a replacement for a lawyer?",
    a: "No. LegalLens is a public legal awareness system. It helps you understand which Indian statutes may apply and directs you to official grievance mechanisms. For representation in court or formal legal documents, consult a licensed advocate.",
  },
  {
    q: "Where does the legal information come from?",
    a: "All provisions are grounded in official Indian statutory texts (Bharatiya Nyaya Sanhita, Information Technology Act, Consumer Protection Act, etc.) and checked by legal researchers. We never fabricate statutes.",
  },
  {
    q: "What languages can I write in?",
    a: "You can write in English, हिन्दी (Hindi), or ಕನ್ನಡ (Kannada). Our system detects the language and matches provisions accordingly.",
  },
  {
    q: "Is my scenario kept private?",
    a: "Yes. Your description is processed only to perform the legal analysis. It is never logged in plaintext or shared with third parties.",
  },
];

export function HowItWorksPage() {
  return (
    <div className="relative py-12 sm:py-16 px-4 sm:px-6 select-none max-w-5xl mx-auto">
      {/* ---------- Sticky Notes on Top ---------- */}
      <div className="relative w-full">
        <div className="hidden lg:block absolute -top-6 left-4 z-10 -rotate-6">
          <div className="bg-[#a7f3d0] dark:bg-[#065f46] text-emerald-950 dark:text-emerald-100 font-mono text-xs px-3.5 py-1.5 rounded shadow-sm border border-emerald-300 dark:border-emerald-700">
            BNS 2024 · MV Act · IT Act
          </div>
        </div>
        <div className="hidden lg:block absolute -top-6 right-8 z-10 rotate-6">
          <div className="bg-[#fef08a] dark:bg-[#854d0e] text-amber-950 dark:text-amber-100 font-mono text-xs px-3.5 py-1.5 rounded shadow-sm border border-amber-300 dark:border-amber-700">
            100% Deterministic Grounding
          </div>
        </div>
      </div>

      {/* ---------- Header with Canvas Selection Box ---------- */}
      <div className="flex flex-col items-center text-center mb-16">
        <span className="font-handwriting text-2xl sm:text-3xl text-foreground/80 font-bold -rotate-2">
          how it actually works
        </span>
        <div className="w-12 h-1 bg-foreground/20 rounded-full mt-0.5 mb-2" />

        <div className="relative inline-block px-8 py-2.5 my-2 border-2 border-black dark:border-[#00c5ff] bg-background/80 backdrop-blur-sm">
          <span className="canvas-handle -top-1.5 -left-1.5" />
          <span className="canvas-handle -top-1.5 left-1/2 -translate-x-1/2" />
          <span className="canvas-handle -top-1.5 -right-1.5" />
          <span className="canvas-handle -bottom-1.5 -left-1.5" />
          <span className="canvas-handle -bottom-1.5 left-1/2 -translate-x-1/2" />
          <span className="canvas-handle -bottom-1.5 -right-1.5" />
          <h1 className="font-mono text-2xl sm:text-4xl font-extrabold uppercase tracking-tight text-foreground">
            HOW IT WORKS
          </h1>
        </div>

        <p className="mt-3 font-mono text-xs sm:text-sm font-semibold text-muted-foreground uppercase tracking-wider">
          Plain language in · Verified Indian laws out
        </p>
      </div>

      {/* ---------- 4 Studio Step Pipeline Cards ---------- */}
      <section className="mb-20">
        <div className="flex items-center gap-2 mb-6">
          <span className="font-mono text-xs font-black uppercase tracking-wider text-muted-foreground">
            01 / 4-STAGE PIPELINE
          </span>
          <span className="h-px flex-1 bg-border" />
        </div>

        <div className="grid gap-5 sm:grid-cols-2">
          {PIPELINE_STEPS.map((s) => (
            <div
              key={s.step}
              className="relative rounded-xl border-2 border-black dark:border-white/30 bg-card p-6 shadow-sm hover:-translate-y-1 transition-transform duration-200 select-none"
            >
              {/* Corner Handles */}
              <span className="canvas-handle -top-1.5 -left-1.5" />
              <span className="canvas-handle -top-1.5 -right-1.5" />
              <span className="canvas-handle -bottom-1.5 -left-1.5" />
              <span className="canvas-handle -bottom-1.5 -right-1.5" />

              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className={`px-2.5 py-1 rounded font-mono text-xs font-black uppercase ${s.tagColor}`}>
                    STEP {s.step}
                  </span>
                  <span className="font-mono text-[11px] font-bold text-muted-foreground">
                    [{s.label}]
                  </span>
                </div>
                <span className="font-handwriting text-base font-bold text-foreground/70 -rotate-3">
                  {s.handwritten}
                </span>
              </div>

              <div className="flex items-start gap-3.5">
                <div className="h-10 w-10 rounded-lg border-2 border-border bg-muted flex items-center justify-center text-foreground shrink-0 mt-0.5">
                  <s.icon className="h-5 w-5 stroke-[2]" />
                </div>
                <div>
                  <h3 className="font-mono text-base sm:text-lg font-bold text-foreground">
                    {s.title}
                  </h3>
                  <p className="mt-2 text-xs sm:text-sm text-muted-foreground leading-relaxed font-medium">
                    {s.body}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ---------- Transparent Scope Matrix ---------- */}
      <section className="mb-20">
        <div className="flex items-center gap-2 mb-6">
          <span className="font-mono text-xs font-black uppercase tracking-wider text-muted-foreground">
            02 / SYSTEM BOUNDARIES &amp; SCOPE
          </span>
          <span className="h-px flex-1 bg-border" />
        </div>

        <div className="grid gap-6 sm:grid-cols-2">
          {/* Covered (In Scope) */}
          <div className="rounded-xl border-2 border-emerald-500 bg-emerald-500/[0.04] p-6 shadow-sm select-none">
            <div className="flex items-center justify-between mb-5">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-[#10b981] text-black font-mono text-xs font-black uppercase">
                <CheckCircle2 className="h-3.5 w-3.5 stroke-[2.5]" />
                <span>WHAT WE COVER</span>
              </span>
              <span className="font-mono text-[11px] font-bold text-emerald-600 dark:text-emerald-400">
                5 CORE DOMAINS
              </span>
            </div>

            <ul className="space-y-4">
              {SCOPE_IN.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2.5">
                  <span className="text-[#10b981] font-black text-sm">✓</span>
                  <div>
                    <h4 className="font-mono text-xs sm:text-sm font-bold text-foreground">
                      {item.title}
                    </h4>
                    <p className="text-[11px] sm:text-xs text-muted-foreground font-medium mt-0.5">
                      {item.desc}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          {/* Not Covered (Out of Scope) */}
          <div className="rounded-xl border-2 border-rose-500 bg-rose-500/[0.04] p-6 shadow-sm select-none">
            <div className="flex items-center justify-between mb-5">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-[#e11d48] text-white font-mono text-xs font-black uppercase">
                <XCircle className="h-3.5 w-3.5 stroke-[2.5]" />
                <span>WHAT WE DO NOT DO</span>
              </span>
              <span className="font-mono text-[11px] font-bold text-rose-600 dark:text-rose-400">
                SAFETY LIMITS
              </span>
            </div>

            <ul className="space-y-4">
              {SCOPE_OUT.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2.5">
                  <span className="text-[#e11d48] font-black text-sm">✕</span>
                  <div>
                    <h4 className="font-mono text-xs sm:text-sm font-bold text-foreground">
                      {item.title}
                    </h4>
                    <p className="text-[11px] sm:text-xs text-muted-foreground font-medium mt-0.5">
                      {item.desc}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>

      {/* ---------- Frequently Asked Questions ---------- */}
      <section className="mb-20">
        <div className="flex items-center gap-2 mb-6">
          <span className="font-mono text-xs font-black uppercase tracking-wider text-muted-foreground">
            03 / FREQUENTLY ASKED QUESTIONS
          </span>
          <span className="h-px flex-1 bg-border" />
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          {FAQS.map((faq, idx) => (
            <div
              key={idx}
              className="rounded-xl border-2 border-border bg-card p-5 shadow-sm select-none"
            >
              <div className="flex items-center gap-2 mb-2 text-[#00c5ff]">
                <HelpCircle className="h-4 w-4 shrink-0" />
                <h3 className="font-mono text-xs sm:text-sm font-bold text-foreground">
                  {faq.q}
                </h3>
              </div>
              <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed font-medium pl-6">
                {faq.a}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ---------- Bottom Studio Action Box ---------- */}
      <div className="relative rounded-2xl border-2 border-black dark:border-white bg-foreground text-background p-8 text-center flex flex-col items-center select-none shadow-lg">
        <span className="canvas-handle -top-1.5 -left-1.5" />
        <span className="canvas-handle -top-1.5 -right-1.5" />
        <span className="canvas-handle -bottom-1.5 -left-1.5" />
        <span className="canvas-handle -bottom-1.5 -right-1.5" />

        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#00c5ff] text-black font-mono text-xs font-black uppercase mb-3">
          <Sparkles className="h-3.5 w-3.5" />
          <span>TRY IT NOW</span>
        </div>

        <h3 className="font-mono text-xl sm:text-3xl font-black uppercase tracking-tight">
          Ready to understand your rights?
        </h3>
        <p className="mt-2 text-xs sm:text-sm opacity-80 max-w-md font-medium">
          Describe any situation in plain words to get verified Indian legal provisions and official next steps.
        </p>

        <Link
          to="/analyze"
          className="mt-6 inline-flex items-center gap-2 px-7 py-3.5 rounded-lg bg-[#00c5ff] text-black font-mono text-xs font-black uppercase tracking-wider shadow hover:scale-105 transition-transform"
        >
          <span>RUN LEGAL ANALYSIS</span>
          <ArrowRight className="h-4 w-4 stroke-[2.5]" />
        </Link>
      </div>
    </div>
  );
}
