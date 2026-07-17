import { motion, useReducedMotion, type Variants } from "framer-motion";
import type { AnalyzeResponse } from "@/types/contract";
import { DomainResultCard } from "@/components/legal/DomainResultCard";
import { IssueResultCard } from "@/components/legal/IssueResultCard";
import { ProvisionCard } from "@/components/legal/ProvisionCard";
import { ActionSteps } from "@/components/legal/ActionSteps";
import { PortalList } from "@/components/legal/PortalList";
import { NoVerifiedProvisionState } from "@/components/legal/NoVerifiedProvisionState";
import { LowConfidenceBanner } from "@/components/legal/LowConfidenceBanner";
import { MandatoryDisclaimer } from "@/components/legal/MandatoryDisclaimer";

/*
  Progressive, calm reveal of the analysis. Content is staggered in a readable
  hierarchy: clarification (if any) -> area of law -> situation -> provisions (or
  the explicit safe state) -> steps -> portals -> mandatory disclaimer.
  The disclaimer always renders (CLAUDE.md Section 10).
*/
function useVariants() {
  const reduce = useReducedMotion();
  const container: Variants = {
    hidden: {},
    show: {
      transition: { staggerChildren: reduce ? 0 : 0.12, delayChildren: 0.05 },
    },
  };
  const item: Variants = {
    hidden: reduce ? { opacity: 0 } : { opacity: 0, y: 18 },
    show: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] },
    },
  };
  return { container, item };
}

export function ResultView({ data }: { data: AnalyzeResponse }) {
  const { container, item } = useVariants();
  const hasProvisions =
    data.legal_information_status === "provisions_available" &&
    data.legal_provisions.length > 0;
  // The ML service returns an all-null issue when no situation type could be
  // detected within the predicted domain — render the domain alone in that
  // case rather than an empty issue card.
  const issue = data.analysis.issue;
  const hasIssue = issue.id != null && issue.display_name != null;

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="mx-auto flex w-full max-w-3xl flex-col gap-4 sm:gap-5"
    >
      {(data.low_confidence_warning || data.needs_clarification) && (
        <motion.div variants={item}>
          <LowConfidenceBanner clarificationQuestion={data.clarification_question} />
        </motion.div>
      )}

      <div className={hasIssue ? "grid gap-4 sm:gap-5 md:grid-cols-2" : "grid gap-4 sm:gap-5"}>
        <motion.div variants={item}>
          <DomainResultCard domain={data.analysis.domain} />
        </motion.div>
        {hasIssue && (
          <motion.div variants={item}>
            <IssueResultCard
              issue={issue}
              signals={data.analysis.scenario_signals}
            />
          </motion.div>
        )}
      </div>

      <motion.div variants={item} className="flex items-center gap-3 px-1 pt-3">
        <h2 className="shrink-0 font-display text-lg font-semibold text-foreground">
          {hasProvisions ? "Provisions that may relate" : "Legal information"}
        </h2>
        <span aria-hidden className="h-px flex-1 bg-gradient-to-r from-white/15 to-transparent" />
      </motion.div>

      {hasProvisions ? (
        data.legal_provisions.map((p, i) => (
          <motion.div key={`${p.act_id}-${p.section}-${i}`} variants={item}>
            <ProvisionCard provision={p} index={i} />
          </motion.div>
        ))
      ) : (
        <motion.div variants={item}>
          <NoVerifiedProvisionState />
        </motion.div>
      )}

      {data.action_steps?.length > 0 && (
        <motion.div variants={item}>
          <ActionSteps steps={data.action_steps} />
        </motion.div>
      )}

      {data.portals?.length > 0 && (
        <motion.div variants={item}>
          <PortalList portals={data.portals} />
        </motion.div>
      )}

      <motion.div variants={item}>
        <MandatoryDisclaimer text={data.disclaimer} />
      </motion.div>
    </motion.div>
  );
}
