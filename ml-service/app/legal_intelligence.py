"""Module 3 — Legal Intelligence Engine (CLAUDE.md Section 8).

What this is: the trust anchor of the system. Given a detected issue_id it
performs PURE KB LOOKUP — zero ML, zero generation, zero external calls.

The eligibility gate (CLAUDE.md 7.5) is enforced HERE, at the last moment
before legal content can reach a citizen. A provision is returnable only if
BOTH:

    verification.status == "manually_verified"
    AND provision_status == "in_force"

Everything else — unverified, pending, omitted, repealed, amended — is
silently discarded from the result (and the discard is what triggers the
explicit safe state if nothing survives).

Must NOT (CLAUDE.md Section 8): use any ML model, generate content, infer
from model memory, invent Act names/penalties/procedures, make external API
calls, substitute AI-generated law for an unverified provision, ask an LLM to
invent a missing section, expose pending candidate provisions, or treat issue
similarity as legal certainty.

Explicit safe state: if no eligible provision exists for the issue (or no
issue was detected at all), the result says so via
legal_information_status = "no_verified_provision_available" — never an
unexplained empty list, never a fabricated answer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.knowledge_base_loader import MAX_ACTION_STEPS, KnowledgeBase

# The gate (CLAUDE.md 7.5). Both must hold; neither alone is sufficient.
ELIGIBLE_VERIFICATION_STATUS = "manually_verified"
ELIGIBLE_PROVISION_STATUSES = frozenset({"in_force"})  # Phase 1

# Portal rules (CLAUDE.md Section 8). MAX_ACTION_STEPS is imported from the
# loader, which owns the limit at validation time; the slice in
# _action_steps() is defense-in-depth against a KB edited after startup.
_PRIORITY_ORDER = {"immediate": 0, "primary": 1, "secondary": 2}
MAX_PORTALS = 3

LEGAL_INFO_PROVISIONS_AVAILABLE = "provisions_available"
LEGAL_INFO_NO_VERIFIED_PROVISION = "no_verified_provision_available"


@dataclass(frozen=True)
class LegalIntelligenceResult:
    """Module 3 output contract. Plain data — Module 4 shapes the API response."""

    legal_information_status: str
    legal_provisions: List[Dict[str, Any]] = field(default_factory=list)
    action_steps: List[str] = field(default_factory=list)
    portals: List[Dict[str, Any]] = field(default_factory=list)


class LegalIntelligenceEngine:
    """Deterministic KB retrieval with the citizen-facing eligibility gate."""

    def __init__(self, kb: KnowledgeBase):
        self._kb = kb

    def retrieve(self, issue_id: Optional[str]) -> LegalIntelligenceResult:
        """Retrieve eligible provisions, action steps, and portals for an issue.

        ``issue_id=None`` (Module 2 detected nothing) is a legitimate input
        and yields the explicit safe state.
        """
        if issue_id is None or issue_id not in self._kb.issues:
            return LegalIntelligenceResult(
                legal_information_status=LEGAL_INFO_NO_VERIFIED_PROVISION
            )

        provisions = self._eligible_provisions(issue_id)
        status = (
            LEGAL_INFO_PROVISIONS_AVAILABLE
            if provisions
            else LEGAL_INFO_NO_VERIFIED_PROVISION
        )
        return LegalIntelligenceResult(
            legal_information_status=status,
            legal_provisions=provisions,
            action_steps=self._action_steps(issue_id),
            portals=self._portals(issue_id),
        )

    # ------------------------------------------------------------------
    # Provisions
    # ------------------------------------------------------------------

    @staticmethod
    def _is_citizen_facing_eligible(section: Dict[str, Any]) -> bool:
        """The hard gate (CLAUDE.md 7.5): manual verification AND in-force
        status. This function is the single place the check lives."""
        verification_ok = (
            section.get("verification", {}).get("status") == ELIGIBLE_VERIFICATION_STATUS
        )
        status_ok = section.get("provision_status") in ELIGIBLE_PROVISION_STATUSES
        return verification_ok and status_ok

    def _eligible_provisions(self, issue_id: str) -> List[Dict[str, Any]]:
        issue = self._kb.issues[issue_id]
        results: List[Dict[str, Any]] = []
        for ref in issue.get("provision_references", []) or []:
            act_id, section_id = ref.get("act_id"), ref.get("section_id")
            section = self._kb.resolve_provision(act_id, section_id)
            if section is None:
                continue  # loader guarantees this at startup; defensive anyway
            if not self._is_citizen_facing_eligible(section):
                # Discard. No substitution, no generation, no LLM fallback —
                # the absence itself becomes the explicit safe state.
                continue
            act = self._kb.acts[act_id]
            results.append(
                {
                    "act_id": act_id,
                    "act": act.get("official_act_name") or act.get("short_name") or act_id,
                    "section": f"Section {section.get('section_number', section_id)}",
                    "title": section.get("official_section_title"),
                    # Only the simplified explanation is citizen-facing by
                    # default — full statutory text never appears (8.1).
                    "simplified_explanation": section.get("simplified_explanation"),
                    # Layer B — human-curated, carried from the issue mapping.
                    "provision_relevance_rationale": ref.get(
                        "provision_relevance_rationale"
                    ),
                    "official_source": {
                        "name": act.get("official_source_name"),
                        "url": act.get("official_source_url"),
                    },
                }
            )
        return results

    # ------------------------------------------------------------------
    # Practical guidance
    # ------------------------------------------------------------------

    def _action_steps(self, issue_id: str) -> List[str]:
        guidance = self._kb.issue_guidance.get(issue_id, {})
        return list(guidance.get("action_steps", []) or [])[:MAX_ACTION_STEPS]

    def _portals(self, issue_id: str) -> List[Dict[str, Any]]:
        """Filter to portals supporting this issue, sort immediate -> primary
        -> secondary, return at most MAX_PORTALS."""
        portal_ids = self._kb.portals_by_issue.get(issue_id, [])
        portals = [self._kb.portals[pid] for pid in portal_ids]
        portals.sort(key=lambda p: _PRIORITY_ORDER.get(p.get("priority"), 99))
        return [
            {
                "name": portal.get("name"),
                "official_url": portal.get("official_url"),
                "purpose": portal.get("purpose"),
                "priority": portal.get("priority"),
            }
            for portal in portals[:MAX_PORTALS]
        ]
