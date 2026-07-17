import { Link } from "react-router-dom";
import { motion, useReducedMotion } from "framer-motion";
import {
  ArrowRight,
  BadgeCheck,
  ShieldCheck,
  Languages,
  Landmark,
  Scale,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { HeroCanvas } from "@/components/three/HeroCanvas";

/* Concise trust strip directly beneath the hero — trust before interaction. */
const TRUST_STRIP = [
  { icon: ShieldCheck, text: "Human-verified legal provisions" },
  { icon: Landmark, text: "Official Government portals" },
  { icon: Scale, text: "Legal awareness only — not legal advice" },
];

const TRUST = [
  {
    icon: ShieldCheck,
    title: "Grounded in official sources",
    body: "Every legal provision LegalLens shows is checked against official Indian government sources — with a link so you can verify it yourself.",
  },
  {
    icon: Languages,
    title: "Plain, human language",
    body: "No dense legalese. LegalLens explains what a provision means in words anyone can follow.",
  },
  {
    icon: Landmark,
    title: "The right next step",
    body: "Get practical steps and the official government portals that actually handle your kind of situation.",
  },
  {
    icon: BadgeCheck,
    title: "Awareness, not guesswork",
    body: "LegalLens helps you understand the law. It never claims you have a case — and it's honest when there's nothing verified to show.",
  },
];

function fade(delay = 0) {
  return {
    initial: { opacity: 0, y: 20 },
    whileInView: { opacity: 1, y: 0 },
    viewport: { once: true, margin: "-80px" },
    transition: { duration: 0.6, delay, ease: [0.22, 1, 0.36, 1] as const },
  };
}

export function LandingPage() {
  const reduce = useReducedMotion();

  const rise = (delay: number) => ({
    initial: reduce ? { opacity: 0 } : { opacity: 0, y: 18 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.7, delay, ease: [0.22, 1, 0.36, 1] as const },
  });

  return (
    <div className="overflow-x-clip">
      {/* ---------- Hero ---------- */}
      <section className="relative">
        <div className="absolute inset-0 -z-10">
          <HeroCanvas />
          {/* keeps the headline unmistakably the focal point over the scene */}
          <div className="hero-vignette absolute inset-0" aria-hidden />
        </div>

        <div className="container flex min-h-[calc(100svh-4rem)] flex-col items-center justify-center py-16 text-center sm:py-20">
          <motion.div
            {...rise(0)}
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-4 py-1.5 text-xs text-muted-foreground backdrop-blur"
          >
            <span className="relative flex h-1.5 w-1.5">
              <span className="absolute inline-flex h-full w-full animate-pulse-ring rounded-full bg-primary motion-reduce:hidden" />
              <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-primary" />
            </span>
            Legal awareness for Indian citizens
          </motion.div>

          <motion.h1
            {...rise(0.08)}
            className="mt-7 max-w-4xl font-display text-[2.75rem] font-semibold leading-[1.04] tracking-tight text-balance sm:text-6xl md:text-7xl"
          >
            See the law
            <br className="sm:hidden" />{" "}
            <span className="text-jade-brass">more clearly.</span>
          </motion.h1>

          <motion.p
            {...rise(0.16)}
            className="mt-6 max-w-xl text-base leading-relaxed text-muted-foreground text-pretty sm:mt-7 sm:text-lg"
          >
            Describe a real-life situation in your own words. LegalLens shows you the
            laws that may relate to it, in plain language — with official sources and
            practical next steps.
          </motion.p>

          <motion.div
            {...rise(0.24)}
            className="mt-9 flex w-full max-w-sm flex-col items-center gap-3 sm:mt-10 sm:w-auto sm:max-w-none sm:flex-row"
          >
            <Button asChild size="lg" className="w-full sm:w-auto">
              <Link to="/analyze">
                Analyze a situation <ArrowRight />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary" className="w-full sm:w-auto">
              <Link to="/how-it-works">How LegalLens works</Link>
            </Button>
          </motion.div>

          {/* Trust strip — concise, professional, beneath the CTAs */}
          <motion.ul
            {...rise(0.36)}
            className="mt-14 flex w-full max-w-3xl flex-col items-stretch gap-2.5 sm:mt-16 sm:flex-row sm:items-center sm:justify-center sm:gap-0 sm:divide-x sm:divide-white/10"
            aria-label="Why you can trust LegalLens"
          >
            {TRUST_STRIP.map(({ icon: Icon, text }) => (
              <li
                key={text}
                className="flex items-center justify-center gap-2.5 rounded-xl border border-white/[0.07] bg-white/[0.03] px-4 py-3 text-sm text-muted-foreground backdrop-blur sm:rounded-none sm:border-0 sm:bg-transparent sm:px-6 sm:py-0 sm:backdrop-blur-none"
              >
                <Icon className="h-4 w-4 shrink-0 text-primary" aria-hidden />
                <span className="text-pretty">{text}</span>
              </li>
            ))}
          </motion.ul>
        </div>
      </section>

      {/* ---------- Trust, expanded ---------- */}
      <section className="container py-20 sm:py-28">
        <motion.div {...fade()} className="mx-auto max-w-2xl text-center">
          <span className="eyebrow justify-center">Why LegalLens</span>
          <h2 className="mt-4 font-display text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
            Built to be trusted, not just clever
          </h2>
          <p className="mt-4 text-muted-foreground text-pretty">
            Legal information is only useful if you can rely on it. LegalLens is
            designed to be careful, transparent, and honest about its limits.
          </p>
        </motion.div>

        <div className="mt-12 grid gap-4 sm:mt-14 sm:grid-cols-2 sm:gap-5 lg:grid-cols-4">
          {TRUST.map((f, i) => (
            <motion.div key={f.title} {...fade(i * 0.06)}>
              <Card className="glass-hover h-full p-6">
                <span className="grid h-11 w-11 place-items-center rounded-xl bg-primary/12 text-primary">
                  <f.icon className="h-5 w-5" aria-hidden />
                </span>
                <h3 className="mt-4 font-semibold text-foreground">{f.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground text-pretty">
                  {f.body}
                </p>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ---------- Flow preview ---------- */}
      <section className="container py-6 sm:py-12">
        <div className="glass relative overflow-hidden rounded-3xl p-7 sm:p-12">
          <div className="absolute -right-16 -top-16 h-56 w-56 rounded-full bg-[radial-gradient(circle,hsl(var(--accent)/0.16),transparent_60%)] blur-2xl" />
          <div className="relative grid gap-10 lg:grid-cols-2 lg:items-center lg:gap-14">
            <motion.div {...fade()}>
              <span className="eyebrow">One simple step</span>
              <h2 className="mt-4 font-display text-3xl font-semibold tracking-tight text-balance sm:text-4xl">
                From confusion to clarity
              </h2>
              <p className="mt-4 text-muted-foreground text-pretty">
                You don't need to know any legal terms to start. Describe what happened
                — LegalLens does the rest and shows you a calm, readable summary you can
                act on.
              </p>
              <ul className="mt-7 space-y-3.5">
                {[
                  "The area of law your situation relates to",
                  "Relevant legal provisions, explained simply",
                  "Clear, practical steps you can take next",
                  "Official government portals for your issue",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-3">
                    <BadgeCheck className="mt-0.5 h-5 w-5 shrink-0 text-primary" />
                    <span className="text-sm text-foreground/90">{item}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-9">
                <Button asChild>
                  <Link to="/analyze">
                    Try it now <ArrowRight />
                  </Link>
                </Button>
              </div>
            </motion.div>

            <motion.div {...fade(0.1)} className="space-y-3">
              {[
                { k: "Area of law", v: "Cyber Fraud", tone: "primary" },
                { k: "Detected situation", v: "OTP / impersonation fraud", tone: "accent" },
                { k: "Next step", v: "Report on the official cybercrime portal", tone: "primary" },
              ].map((row) => (
                <div
                  key={row.k}
                  className="flex flex-col gap-1 rounded-2xl border border-white/10 bg-white/[0.03] p-4 transition-colors duration-300 hover:border-white/[0.16] sm:flex-row sm:items-center sm:justify-between sm:gap-4"
                >
                  <span className="text-[0.68rem] font-medium uppercase tracking-[0.14em] text-muted-foreground/70">
                    {row.k}
                  </span>
                  <span
                    className={
                      row.tone === "accent"
                        ? "text-sm font-medium text-accent"
                        : "text-sm font-medium text-primary"
                    }
                  >
                    {row.v}
                  </span>
                </div>
              ))}
              <p className="px-1 pt-2 text-xs text-muted-foreground/70">
                Illustrative preview. Your actual results depend on what you describe.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ---------- Awareness vs advice ---------- */}
      <section className="container py-20 sm:py-28">
        <motion.div
          {...fade()}
          className="mx-auto max-w-3xl rounded-3xl border border-accent/20 bg-accent/[0.05] p-8 text-center sm:p-12"
        >
          <h2 className="font-display text-2xl font-semibold tracking-tight text-balance sm:text-3xl">
            Awareness, not legal advice
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted-foreground text-pretty">
            LegalLens helps you understand which laws may relate to your situation and
            where to turn next. It doesn't tell you whether a law definitely applies or
            whether you have a case. For advice specific to your situation, always
            consult a qualified legal professional.
          </p>
          <div className="mt-8">
            <Button asChild variant="secondary">
              <Link to="/how-it-works">Understand our scope &amp; limits</Link>
            </Button>
          </div>
        </motion.div>
      </section>
    </div>
  );
}
