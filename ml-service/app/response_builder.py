"""Module 4 — Response Builder (CLAUDE.md Section 8).

What this is: pure assembly. It takes the outputs of Modules 1-3 and shapes
them into the locked response contract (schemas.AnalyzeResponse). It NEVER
performs legal lookup, never touches the KB, never re-decides anything a
prior module decided — if it needs a fact, that fact must arrive as input.

Responsibilities:
- assign the domain confidence label,
- set low_confidence_warning / needs_clarification,
- select the (Phase 1: static, domain-keyed) clarification question,
- pass through legal_information_status from Module 3,
- attach the mandatory disclaimer — every response, no exceptions.

Thresholds are Phase 1 provisional defaults, configuration not constitution
(CLAUDE.md 8.1): they will be re-tuned from Dataset V1 evaluation. The
permanent rule is HTTP-level: model uncertainty on valid input is still a
200 with warning flags — never an HTTP error (8.2). That rule lives in
main.py by construction (this builder always returns a normal response).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.classifier import DomainPrediction
from app.issue_detector import IssueDetection
from app.legal_intelligence import LegalIntelligenceResult
from app.schemas import (
    Analysis,
    AnalyzeResponse,
    DISCLAIMER,
    DomainAnalysis,
    DOMAIN_DISPLAY_NAMES,
    IssueAnalysis,
    LegalProvision,
    OfficialSource,
    PortalOut,
)


@dataclass(frozen=True)
class ConfidenceThresholds:
    """Phase 1 provisional defaults (CLAUDE.md 8.1) — configuration, to be
    re-tuned from Dataset V1 evaluation, not constitutional values."""

    high: float = 0.80
    medium: float = 0.65
    low: float = 0.60  # below this: Low + warning + clarification


# Phase 1 clarification questions: simple domain-keyed static text (8.2).
# Wording is awareness-safe: it asks for context, claims nothing legal.
_CLARIFICATION_QUESTIONS = {
    "cyber_fraud": (
        "Could you describe what happened in more detail — for example, "
        "whether it involved a call or message, a link or website, an OTP, "
        "or access to one of your accounts?"
    ),
    "consumer_issues": (
        "Could you describe the purchase or service in more detail — what "
        "you paid for, what you received, and what the seller or provider "
        "said when you raised it?"
    ),
    "traffic_enforcement": (
        "Could you describe the situation in more detail — for example, "
        "whether it involved a fine, your documents, or your vehicle, and "
        "what the officer said or did?"
    ),
    "workplace_wage": (
        "Could you describe your work situation in more detail — for "
        "example, whether you are an employee, how much is unpaid or "
        "deducted, and since when?"
    ),
    "contractual_disputes": (
        "Could you describe the agreement in more detail — what was agreed, "
        "what the other party did or did not do, and whether anything was "
        "put in writing?"
    ),
}
_DEFAULT_CLARIFICATION = (
    "Could you describe your situation in a little more detail, including "
    "what happened, who was involved, and when?"
)


class ResponseBuilder:
    """Assembles the final AnalyzeResponse. Assembly only — no lookup."""

    def __init__(self, thresholds: ConfidenceThresholds | None = None):
        self._thresholds = thresholds or ConfidenceThresholds()

    def confidence_label(self, confidence: float) -> str:
        t = self._thresholds
        if confidence >= t.high:
            return "High"
        if confidence >= t.medium:
            return "Medium"
        return "Low"  # includes the below-low warning band

    def build(
        self,
        request_id: str,
        domain_prediction: DomainPrediction,
        issue_detection: Optional[IssueDetection],
        intelligence: LegalIntelligenceResult,
    ) -> AnalyzeResponse:
        confidence = domain_prediction.confidence
        low_confidence = confidence < self._thresholds.low
        # Clarify when the model is unsure OR nothing matched at issue level —
        # both are honest uncertainty, both are HTTP 200 states (8.2).
        needs_clarification = low_confidence or issue_detection is None

        analysis = Analysis(
            domain=DomainAnalysis(
                id=domain_prediction.domain_id,
                display_name=DOMAIN_DISPLAY_NAMES.get(
                    domain_prediction.domain_id, domain_prediction.domain_id
                ),
                confidence=confidence,
                confidence_label=self.confidence_label(confidence),
            ),
            issue=IssueAnalysis(
                id=issue_detection.issue_id if issue_detection else None,
                display_name=issue_detection.display_name if issue_detection else None,
                similarity_score=(
                    issue_detection.similarity_score if issue_detection else None
                ),
                issue_match_reason=(
                    issue_detection.issue_match_reason if issue_detection else None
                ),
            ),
            scenario_signals=(
                issue_detection.scenario_signals if issue_detection else []
            ),
        )

        return AnalyzeResponse(
            success=True,
            request_id=request_id,
            analysis=analysis,
            legal_provisions=[
                LegalProvision(
                    act_id=p["act_id"],
                    act=p["act"],
                    section=p["section"],
                    title=p.get("title"),
                    simplified_explanation=p.get("simplified_explanation"),
                    provision_relevance_rationale=p["provision_relevance_rationale"],
                    official_source=OfficialSource(**(p.get("official_source") or {})),
                )
                for p in intelligence.legal_provisions
            ],
            legal_information_status=intelligence.legal_information_status,
            action_steps=list(intelligence.action_steps),
            portals=[
                PortalOut(
                    name=portal["name"],
                    official_url=portal.get("official_url"),
                    purpose=portal["purpose"],
                    priority=portal["priority"],
                )
                for portal in intelligence.portals
            ],
            low_confidence_warning=low_confidence,
            needs_clarification=needs_clarification,
            clarification_question=(
                _CLARIFICATION_QUESTIONS.get(
                    domain_prediction.domain_id, _DEFAULT_CLARIFICATION
                )
                if needs_clarification
                else None
            ),
            disclaimer=DISCLAIMER,
        )
