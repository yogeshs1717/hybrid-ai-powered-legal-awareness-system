import { motion, useReducedMotion, type Variants } from "framer-motion";
import { FileText } from "lucide-react";
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
      transition: { staggerChildren: reduce ? 0 : 0.08, delayChildren: 0.02 },
    },
  };
  const item: Variants = {
    hidden: reduce ? { opacity: 1, y: 0 } : { opacity: 0, y: 14 },
    show: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] },
    },
  };
  return { container, item };
}

export function ResultView({
  data,
  scenario,
}: {
  data: AnalyzeResponse;
  scenario?: string;
}) {
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
      {scenario && (
        <motion.div
          variants={item}
          className="relative rounded-xl border-2 border-border bg-card/90 backdrop-blur-sm p-4 sm:p-5 shadow-sm overflow-hidden"
        >
          <span className="canvas-handle -top-1.5 -left-1.5" />
          <span className="canvas-handle -top-1.5 -right-1.5" />
          <span className="canvas-handle -bottom-1.5 -left-1.5" />
          <span className="canvas-handle -bottom-1.5 -right-1.5" />

          <div className="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-border/60">
            <div className="flex items-center gap-2">
              <span className="flex h-5 w-5 items-center justify-center rounded bg-primary/10 text-primary">
                <FileText className="h-3.5 w-3.5" />
              </span>
              <span className="font-mono text-xs font-black uppercase tracking-wider text-muted-foreground">
                YOUR REPORTED SITUATION
              </span>
            </div>
            <span className="font-mono text-[10px] font-bold text-muted-foreground uppercase px-2 py-0.5 rounded bg-muted/60">
              ANALYZED INPUT
            </span>
          </div>

          <p className="text-sm sm:text-base font-medium text-foreground leading-relaxed italic select-text whitespace-pre-wrap">
            "{scenario}"
          </p>
        </motion.div>
      )}

      {(data.low_confidence_warning || data.needs_clarification) && (
        <motion.div variants={item}>
          <LowConfidenceBanner clarificationQuestion={data.clarification_question} />
        </motion.div>
      )}

      <motion.div variants={item} className={hasIssue ? "grid gap-4 sm:gap-5 md:grid-cols-2" : "grid gap-4 sm:gap-5"}>
        <DomainResultCard domain={data.analysis.domain} />
        {hasIssue && (
          <IssueResultCard
            issue={issue}
            signals={data.analysis.scenario_signals}
          />
        )}
      </motion.div>

      <motion.div variants={item} className="flex items-center gap-3 px-1 pt-4">
        <span className="shrink-0 font-mono text-xs sm:text-sm font-black uppercase tracking-wider text-foreground">
          {hasProvisions ? "APPLICABLE STATUTORY PROVISIONS" : "LEGAL INFORMATION"}
        </span>
        <span aria-hidden className="h-0.5 flex-1 bg-border" />
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
