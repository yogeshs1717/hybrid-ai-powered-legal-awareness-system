import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  PencilLine,
  ScanSearch,
  ScrollText,
  Compass,
  ShieldCheck,
  CircleAlert,
  ArrowRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

/*
  Product-level explanation only. Deliberately no ML internals (no classifiers,
  similarity, model architecture) — focuses on what LegalLens does, its scope,
  how it earns trust, its limits, and awareness-vs-advice.
*/

function fade(delay = 0) {
  return {
    initial: { opacity: 0, y: 18 },
    whileInView: { opacity: 1, y: 0 },
    viewport: { once: true, margin: "-70px" },
    transition: { duration: 0.55, delay, ease: [0.22, 1, 0.36, 1] as const },
  };
}

const STEPS = [
  {
    icon: PencilLine,
    title: "You describe what happened",
    body: "Write your situation in plain, everyday language — no legal terms needed. Just tell LegalLens what happened to you.",
  },
  {
    icon: ScanSearch,
    title: "LegalLens reads it carefully",
    body: "It works out which area of law your situation relates to and the specific kind of issue it looks like.",
  },
  {
    icon: ScrollText,
    title: "It shows relevant provisions",
    body: "You see legal provisions that may relate to your situation, explained simply — each linked to an official source you can check.",
  },
  {
    icon: Compass,
    title: "It points you to what's next",
    body: "Practical next steps and the official government portals that handle your kind of issue, so you know where to go.",
  },
];

const SCOPE_IN = [
  "Cyber fraud (online scams, impersonation, unauthorised account access)",
  "Consumer issues (defective products, refund denial, service problems)",
  "Traffic enforcement situations",
  "Workplace & wage concerns",
  "Contractual disputes",
];

const SCOPE_OUT = [
  "Criminal matters, FIRs, arrest or bail guidance",
  "Predicting the outcome of a case",
  "Telling you whether you will win or have a case",
  "Replacing a qualified advocate",
  "Legal areas outside its five focus areas",
];

const FAQ = [
  {
    q: "Is this legal advice?",
    a: "No. LegalLens provides legal awareness — general information to help you understand your situation and where to turn. For advice specific to your circumstances, consult a qualified legal professional.",
  },
  {
    q: "Where does the legal information come from?",
    a: "Every provision shown has been checked by a person against an official Indian government source, and each one links back to that source so you can verify it yourself.",
  },
  {
    q: "What if there's nothing verified to show?",
    a: "LegalLens will tell you plainly. Rather than guess or invent an answer, it's honest when there isn't a verified provision available — and still offers practical next steps and official portals where it can.",
  },
  {
    q: "Does LegalLens store what I write?",
    a: "Your description is used only to produce your analysis. It isn't shown in your browser's address bar and isn't part of any shareable link.",
  },
  {
    q: "Which language should I write in?",
    a: "English works best right now, including everyday, informal phrasing and small spelling mistakes — you don't need perfect grammar.",
  },
];

export function HowItWorksPage() {
  return (
    <div className="container max-w-4xl py-14 sm:py-20">
      {/* Intro */}
      <motion.header {...fade()} className="mx-auto max-w-2xl text-center">
        <span className="eyebrow justify-center">The product</span>
        <h1 className="mt-4 font-display text-4xl font-semibold tracking-tight text-balance sm:text-5xl">
          How LegalLens works
        </h1>
        <p className="mt-4 text-muted-foreground text-pretty sm:text-lg">
          A calm, trustworthy way to understand which laws may relate to a real-life
          situation — and what you can do next.
        </p>
      </motion.header>

      {/* Steps */}
      <section className="mt-16">
        <div className="grid gap-4 sm:grid-cols-2 sm:gap-5">
          {STEPS.map((s, i) => (
            <motion.div key={s.title} {...fade(i * 0.05)}>
              <Card className="glass-hover h-full p-6">
                <div className="flex items-center gap-3">
                  <span className="grid h-10 w-10 place-items-center rounded-xl bg-primary/12 text-primary">
                    <s.icon className="h-5 w-5" aria-hidden />
                  </span>
                  <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground/70">
                    Step {i + 1}
                  </span>
                </div>
                <h3 className="mt-4 font-semibold text-foreground">{s.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground text-pretty">
                  {s.body}
                </p>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Scope */}
      <section id="scope" className="mt-20 scroll-mt-24">
        <motion.h2
          {...fade()}
          className="font-display text-2xl font-semibold tracking-tight sm:text-3xl"
        >
          What LegalLens covers
        </motion.h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-2 sm:gap-5">
          <motion.div {...fade()}>
            <Card className="h-full p-6">
              <h3 className="flex items-center gap-2 font-semibold text-primary">
                <ShieldCheck className="h-5 w-5" /> In scope
              </h3>
              <ul className="mt-4 space-y-2.5">
                {SCOPE_IN.map((s) => (
                  <li key={s} className="flex items-start gap-2.5 text-sm text-foreground/90">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                    {s}
                  </li>
                ))}
              </ul>
            </Card>
          </motion.div>
          <motion.div {...fade(0.06)}>
            <Card className="h-full p-6">
              <h3 className="flex items-center gap-2 font-semibold text-muted-foreground">
                <CircleAlert className="h-5 w-5" /> Not in scope
              </h3>
              <ul className="mt-4 space-y-2.5">
                {SCOPE_OUT.map((s) => (
                  <li
                    key={s}
                    className="flex items-start gap-2.5 text-sm text-muted-foreground"
                  >
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-muted-foreground/50" />
                    {s}
                  </li>
                ))}
              </ul>
            </Card>
          </motion.div>
        </div>
      </section>

      {/* Trust */}
      <section id="trust" className="mt-20 scroll-mt-24">
        <motion.div
          {...fade()}
          className="rounded-3xl border border-primary/15 bg-primary/[0.05] p-8 sm:p-10"
        >
          <h2 className="font-display text-2xl font-semibold tracking-tight sm:text-3xl">
            Why you can trust what you see
          </h2>
          <div className="mt-6 grid gap-6 sm:grid-cols-3">
            {[
              {
                t: "Human-checked",
                d: "Provisions are verified by a person against official sources before they're ever shown.",
              },
              {
                t: "Always sourced",
                d: "Each provision links to its official government source so you can confirm it yourself.",
              },
              {
                t: "Honest by design",
                d: "When there's nothing verified to show, LegalLens says so — it never fabricates the law.",
              },
            ].map((c) => (
              <div key={c.t}>
                <h3 className="font-semibold text-foreground">{c.t}</h3>
                <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground text-pretty">
                  {c.d}
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* FAQ */}
      <section className="mt-20">
        <motion.h2
          {...fade()}
          className="font-display text-2xl font-semibold tracking-tight sm:text-3xl"
        >
          Common questions
        </motion.h2>
        <motion.div {...fade(0.05)} className="mt-4">
          <Accordion type="single" collapsible className="w-full">
            {FAQ.map((f, i) => (
              <AccordionItem key={i} value={`item-${i}`}>
                <AccordionTrigger>{f.q}</AccordionTrigger>
                <AccordionContent>{f.a}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </motion.div>
      </section>

      {/* Awareness vs advice + CTA */}
      <section className="mt-16">
        <motion.div
          {...fade()}
          className="rounded-3xl border border-accent/20 bg-accent/[0.05] p-8 text-center sm:p-10"
        >
          <h2 className="font-display text-2xl font-semibold tracking-tight text-balance">
            Awareness, not legal advice
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground text-pretty">
            This information is for legal awareness only and does not constitute legal
            advice. Please consult a qualified legal professional for advice specific to
            your situation.
          </p>
          <div className="mt-7">
            <Button asChild size="lg">
              <Link to="/analyze">
                Analyze a situation <ArrowRight />
              </Link>
            </Button>
          </div>
        </motion.div>
      </section>
    </div>
  );
}
