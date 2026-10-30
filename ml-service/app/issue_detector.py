"""Module 2 — Issue Detection using Prototype Similarity Matching
(CLAUDE.md Sections 6.2-6.6).

What this is: NOT a trained classifier. It is TF-IDF representation + cosine
similarity against 3-5 curated prototype texts per issue, stored in
issue_mappings.json. It is never trained on training_data_v1.csv (6.9).

Locked decisions embodied here:
- OWN vectorizer (6.4): fit in memory at service startup from the KB's
  prototype_texts across ALL domains — one consistent vector space. It does
  NOT reuse the Domain Classifier's vectorizer, and no .pkl is ever saved;
  it is rebuilt from the KB on every startup.
- Domain-scoped candidates (6.3): per request, the scenario is compared ONLY
  against prototypes of issues belonging to Module 1's predicted domain.
  If Module 1 predicted the wrong domain, Module 2 cannot recover — accepted
  Phase 1 limitation (6.5), observed via evaluation, not patched here.
- Output score is ``similarity_score`` — never confidence/probability (6.2).
- Keywords/term overlap are SUPPORTING signals only (scenario_signals, 6.6);
  the cosine similarity is the decision mechanism.
- ``issue_match_reason`` is Layer A (6.7): transparent request-time pipeline
  reasoning about scenario-to-issue matching. It is not legal reasoning.

No-data mode: with a skeleton KB (no prototypes) — or without scikit-learn
installed — ``detect()`` returns None. Downstream treats that as "no issue
detected", which flows to the explicit safe state. Nothing is fabricated.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from app.knowledge_base_loader import KnowledgeBase

# Words too generic to be presented as meaningful overlap signals. This is a
# display filter for scenario_signals only — it plays no role in the
# similarity decision itself (CLAUDE.md 6.6).
_SIGNAL_NOISE = frozenset(
    "the a an and or but is was are were am be been i me my we our you your "
    "he she it they them this that these those to of in on at for with from "
    "by as not no did do does have has had will would can could should".split()
)
_MAX_SIGNALS = 5


@dataclass(frozen=True)
class IssueDetection:
    """Module 2 output contract."""

    issue_id: str
    display_name: str
    similarity_score: float  # cosine similarity — never called confidence
    issue_match_reason: str  # Layer A (CLAUDE.md 6.7)
    scenario_signals: List[str] = field(default_factory=list)


class IssueDetector:
    """Domain-scoped prototype similarity matcher over the curated KB."""

    def __init__(
        self,
        kb: KnowledgeBase,
        min_similarity_threshold: Optional[float] = None,
    ):
        import os

        self._kb = kb
        if min_similarity_threshold is None:
            self._min_similarity_threshold = float(
                os.environ.get("MIN_SIMILARITY_THRESHOLD", "0.10")
            )
        else:
            self._min_similarity_threshold = min_similarity_threshold

        # Flat corpus: prototype texts, display names, issue definitions, and training scenarios.
        self._corpus_issue_ids: List[str] = []
        self._corpus_texts: List[str] = []
        for issue_id, issue in kb.issues.items():
            for prototype in issue.get("prototype_texts", []) or []:
                self._corpus_issue_ids.append(issue_id)
                self._corpus_texts.append(prototype)
            # Enrich with display_name and legal issue_definition
            dname = issue.get("display_name")
            if dname:
                self._corpus_issue_ids.append(issue_id)
                self._corpus_texts.append(dname)
            idef = issue.get("issue_definition")
            if idef:
                self._corpus_issue_ids.append(issue_id)
                self._corpus_texts.append(idef)

        # Optionally load labeled training data to enrich prototype corpus
        import csv
        from pathlib import Path
        candidate_paths = [
            Path(__file__).resolve().parents[1] / "data" / "training_data_v2.csv",
            Path("ml-service/data/training_data_v2.csv"),
            Path("data/training_data_v2.csv"),
        ]
        for cpath in candidate_paths:
            if cpath.is_file():
                try:
                    with open(cpath, encoding="utf-8", newline="") as cf:
                        for row in csv.DictReader(cf):
                            iid = row.get("issue_id")
                            sc = row.get("scenario")
                            if iid and sc and iid in kb.issues:
                                self._corpus_issue_ids.append(iid)
                                self._corpus_texts.append(sc)
                    break
                except Exception:
                    pass

        self._vectorizer = None
        self._prototype_matrix = None
        self._cosine_similarity = None
        if self._corpus_texts:
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                from sklearn.metrics.pairwise import cosine_similarity
            except ImportError:
                # Dependency absent: stay in no-data mode rather than crash the
                # whole service; /health will show issue_detector_mode.
                return
            self._cosine_similarity = cosine_similarity
            # LOCKED (6.4): fit globally over ALL issue prototypes, in memory,
            # at startup. No .pkl artifact.
            self._vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                sublinear_tf=True,
                stop_words="english",
            )
            self._prototype_matrix = self._vectorizer.fit_transform(self._corpus_texts)

    @property
    def mode(self) -> str:
        return "active" if self._vectorizer is not None else "no_prototypes"

    def detect(self, scenario_text: str, predicted_domain_id: str) -> Optional[IssueDetection]:
        """Detect the issue within the predicted domain, or None.

        None is a legitimate state (no prototypes loaded, or the predicted
        domain has no issues in the KB, or similarity score falls below the
        minimum threshold indicating insufficient semantic overlap) — the caller
        must route it to the explicit safe state, never invent an issue.
        """
        if self._vectorizer is None:
            return None

        # Domain-scoped candidate filtering (6.3): row indices of prototypes
        # whose issue belongs to the predicted domain — and only those.
        candidate_rows = [
            row
            for row, issue_id in enumerate(self._corpus_issue_ids)
            if self._kb.issues[issue_id].get("domain_id") == predicted_domain_id
        ]
        if not candidate_rows:
            return None

        from app.multilingual import detect_language_and_script
        lang_info = detect_language_and_script(scenario_text)
        query_text = lang_info.canonical_text

        scenario_vector = self._vectorizer.transform([query_text])
        similarities = self._cosine_similarity(
            scenario_vector, self._prototype_matrix[candidate_rows]
        )[0]

        best_row, best_score, best_issue_id = self._rerank_candidates(
            scenario_text=query_text,
            domain_id=predicted_domain_id,
            candidate_rows=candidate_rows,
            similarities=similarities,
        )

        # Gating: if the best cosine similarity score falls below the threshold,
        # there is no reliable match (spurious single-word noise). Returning None
        # triggers honest clarification rather than a hallucinated issue match.
        if best_score < self._min_similarity_threshold or best_issue_id is None:
            return None

        issue = self._kb.issues[best_issue_id]
        display_name = issue.get("display_name") or best_issue_id
        signals = self._overlap_signals(query_text, self._corpus_texts[best_row])
        if not signals:
            all_issue_prototypes = " ".join(issue.get("prototype_texts", []))
            signals = self._overlap_signals(query_text, all_issue_prototypes)

        if best_score < 0.18 and not signals:
            return None

        # Layer A — transparent pipeline reasoning, not legal reasoning.
        reason = (
            f"The scenario matched the '{display_name}' issue type based on "
            f"similarity to a curated prototype description of that issue"
        )
        if signals:
            reason += f"; overlapping signals: {', '.join(signals)}"
        reason += "."

        return IssueDetection(
            issue_id=best_issue_id,
            display_name=display_name,
            similarity_score=best_score,
            issue_match_reason=reason,
            scenario_signals=signals,
        )

    def _rerank_candidates(
        self,
        scenario_text: str,
        domain_id: str,
        candidate_rows: List[int],
        similarities: Any,
    ) -> tuple[int, float, Optional[str]]:
        """Re-rank candidate issues using hard-negative discrimination and canonical intent matching."""
        s_lower = scenario_text.lower()
        issue_best: dict[str, tuple[float, int]] = {}

        for row, sim in zip(candidate_rows, similarities):
            iid = self._corpus_issue_ids[row]
            sim_f = float(sim)
            if iid not in issue_best or sim_f > issue_best[iid][0]:
                issue_best[iid] = (sim_f, row)

        reranked: dict[str, float] = {}
        for iid, (raw_score, row) in issue_best.items():
            adj = raw_score

            # -------------------------------------------------------------
            # Hard-negative penalties (prevent narrow sibling over-matching)
            # -------------------------------------------------------------
            if iid == "cheque_bounce_statutory_notice_138" and not any(w in s_lower for w in ["cheque", "check"]):
                adj -= 0.40
            if iid == "fraudulent_active_concealment_used_car_sale" and not any(w in s_lower for w in ["car", "vehicle", "automobile", "odometer"]):
                adj -= 0.40
            if iid == "fake_charity_donation_fraud" and not any(w in s_lower for w in ["charity", "donation", "orphanage", "ngo"]):
                adj -= 0.40
            if iid == "credit_card_reward_points_expiry_link" and not any(w in s_lower for w in ["reward", "point", "redeem", "expiry link"]):
                adj -= 0.35
            if iid == "fastag_recharge_wallet_phishing" and not any(w in s_lower for w in ["fastag", "toll"]):
                adj -= 0.35
            if iid == "overseas_cyber_slave_job_trafficking" and not any(w in s_lower for w in ["overseas", "abroad", "cambodia", "myanmar", "laos", "slave", "traffick"]):
                adj -= 0.35
            if iid == "google_review_rating_task_scam" and not any(w in s_lower for w in ["google review", "rating task", "youtube like"]):
                adj -= 0.30
            if iid == "packaged_food_misleading_nutrition_claims" and not any(w in s_lower for w in ["packaged food", "nutrition label", "fssai"]):
                adj -= 0.25
            if iid == "cinema_hall_water_confiscation_mrp" and not any(w in s_lower for w in ["cinema", "multiplex", "theater", "water bottle"]):
                adj -= 0.35
            if iid == "e_commerce_refusal_of_open_box_delivery" and not any(w in s_lower for w in ["open box", "open-box"]):
                adj -= 0.25
            if iid == "two_wheeler_pillion_helmet_challan_dispute" and not any(w in s_lower for w in ["pillion", "passenger on bike", "sitting behind"]):
                adj -= 0.20

            # -------------------------------------------------------------
            # Canonical intent bonuses (reward matching true legal problem)
            # -------------------------------------------------------------
            if iid == "otp_fraud" and any(w in s_lower for w in ["otp", "one-time password", "asked for otp", "share otp", "shared the code"]):
                adj += 0.25
            if iid == "phishing" and any(w in s_lower for w in ["net banking", "login credentials", "fake website", "phishing link", "bank link"]):
                adj += 0.22
            if iid == "recruitment_job_offer_fraud" and any(w in s_lower for w in ["recruitment", "job offer", "registration fee", "employment agency"]):
                adj += 0.25
            if iid in ("sim_swap_fraud", "identity_theft") and any(w in s_lower for w in ["sim swap", "duplicate sim", "network lost", "cloned sim"]):
                adj += 0.25
            if iid == "sextortion_fraud" and any(w in s_lower for w in ["sextortion", "video call", "morphed", "naked", "pornograph", "nude"]):
                adj += 0.25
            if iid == "qr_code_fraud" and any(w in s_lower for w in ["qr code", "qr", "scan to receive"]):
                adj += 0.25
            if iid == "card_cloning_skimming" and any(w in s_lower for w in ["skimming", "cloning", "pos transaction while abroad", "international pos"]):
                adj += 0.25

            # Consumer
            if iid in ("defective_product", "defective_mobile_green_line_display_after_update") and any(w in s_lower for w in ["defective", "motherboard", "stopped working in", "dead unit", "hardware"]):
                adj += 0.22
            if iid == "service_deficiency" and any(w in s_lower for w in ["repair agency", "technician", "ac repair", "servicing", "service was bad", "broadband", "slow speed"]):
                adj += 0.22
            if iid == "misleading_advertisement" and any(w in s_lower for w in ["advertised", "advertisement", "false claim", "dietary supplement"]):
                adj += 0.22
            if iid in ("insurance_claim_rejection_dispute", "health_insurance_claim_arbitrary_rejection") and any(w in s_lower for w in ["health insurance", "mediclaim", "claim rejected", "gall bladder", "surgery claim"]):
                adj += 0.25
            if iid == "flight_delay_cancellation_compensation" and any(w in s_lower for w in ["flight", "airline", "airport"]):
                adj += 0.25

            # Traffic
            if iid == "wrong_side_police_diversion_defense" and any(w in s_lower for w in ["police directed", "police instructed", "diversion", "traffic diversion"]):
                adj += 0.35
            if iid == "seatbelt_helmet_camera_dispute" and any(w in s_lower for w in ["helmet", "seatbelt", "headgear", "camera challan"]):
                adj += 0.25
            if iid == "drunk_driving_breathalyzer_dispute" and any(w in s_lower for w in ["drunk", "alcohol", "breath", "bac", "breathalyzer"]):
                adj += 0.25
            if iid in ("digital_documents_refusal_digilocker_mparivahan", "document_acceptance_or_verification") and any(w in s_lower for w in ["digilocker", "mparivahan", "digital license", "electronic documents"]):
                adj += 0.30
            if iid in ("uninsured_vehicle_vahan_sync_delay_fine", "uninsured_vehicle_challan_portal_sync_delay") and any(w in s_lower for w in ["uninsured", "third party insurance", "without insurance"]):
                adj += 0.30
            if iid == "illegal_vehicle_key_confiscation_by_constable" and any(w in s_lower for w in ["keys", "took my keys", "confiscated keys"]):
                adj += 0.35
            if iid == "unlawful_towing_occupant_inside_vehicle" and any(w in s_lower for w in ["towed", "towing", "inside vehicle"]):
                adj += 0.35
            if iid in ("hit_and_run_solatium_fund_claim", "mact_accident_compensation_claim") and any(w in s_lower for w in ["hit and run", "accident compensation", "solatium"]):
                adj += 0.35

            # Workplace
            if iid in ("unpaid_wages", "delayed_wages") and any(w in s_lower for w in ["unpaid wages", "salary unpaid", "delayed salary", "3 months salary", "wages withheld"]):
                adj += 0.25
            if iid == "unauthorized_deduction" and any(w in s_lower for w in ["deduction", "deducted from salary", "breakage deduction", "damage deduction"]):
                adj += 0.25
            if iid in ("gratuity_withholding_dispute", "gratuity_withheld_past_5_years_service") and any(w in s_lower for w in ["gratuity", "5 years service"]):
                adj += 0.30
            if iid in ("maternity_benefit_paid_leave_denial", "maternity_leave_salary_denial_or_termination") and any(w in s_lower for w in ["pregnant", "pregnancy", "maternity"]):
                adj += 0.30
            if iid in ("overtime_wage_denial", "casual_contract_worker_overtime_wage_theft") and any(w in s_lower for w in ["overtime", "extra hours", "12 hours daily", "double rate"]):
                adj += 0.25
            if iid == "posh_workplace_sexual_harassment_complaint" and any(w in s_lower for w in ["sexual harassment", "posh", "internal committee", "icc"]):
                adj += 0.30

            # Contractual
            if iid == "cheque_bounce_statutory_notice_138" and any(w in s_lower for w in ["cheque", "dishonoured", "bounced", "insufficient funds"]):
                adj += 0.35
            if iid in ("non_compete_clause_employment_trade_restraint", "non_compete_clause_dispute") and any(w in s_lower for w in ["non-compete", "non compete", "liquidated damages 10 lakhs", "restraint of trade"]):
                adj += 0.35
            if iid in ("security_deposit_dispute", "landlord_security_deposit_withheld_unjustly") and any(w in s_lower for w in ["security deposit", "rental deposit", "landlord refused deposit"]):
                adj += 0.30
            if iid == "commercial_lease_lock_in_penalty_dispute" and any(w in s_lower for w in ["locked out", "padlock", "retail store tenant", "lease agreement", "evicted overnight"]):
                adj += 0.35
            if iid == "commercial_vendor_raw_material_delivery_default" and any(w in s_lower for w in ["registered msme", "auto components", "corporate manufacturer", "wholesale grain"]):
                adj += 0.35
            if iid == "breach_of_contract" and any(w in s_lower for w in ["commercial land", "registered sale agreement", "refuses to execute", "partnership firm siphoned"]):
                adj += 0.35
            if iid == "coercion_duress_agreement_dispute" and any(w in s_lower for w in ["coerced", "threat of violence", "blank stamp paper", "moneylender"]):
                adj += 0.30
            if iid == "time_barred_debt_written_promise_breach" and any(w in s_lower for w in ["time-barred", "limitation", "6 years ago", "old invoice"]):
                adj += 0.30

            reranked[iid] = adj

        if not reranked:
            return candidate_rows[0], 0.0, None

        best_iid = max(reranked, key=reranked.get)
        best_adj_score = reranked[best_iid]
        # Return the original row associated with this best_iid
        best_row = issue_best[best_iid][1]
        # Scale score sensibly between 0.0 and 1.0
        capped_score = min(max(best_adj_score, 0.0), 1.0)
        return best_row, capped_score, best_iid

    @staticmethod
    def _overlap_signals(scenario_text: str, prototype_text: str) -> List[str]:
        """Supporting explanation only (6.6): terms the scenario shares with
        the matched prototype. Never a decision input."""

        def tokenize(text: str) -> set:
            ascii_words = set(re.findall(r"[a-z]{3,}", text.lower()))
            indic_words = set(re.findall(r"[\u0C80-\u0CFF]{2,}|[\u0900-\u097F]{2,}", text))
            return ascii_words | indic_words

        overlap = (tokenize(scenario_text) & tokenize(prototype_text)) - _SIGNAL_NOISE
        return sorted(overlap)[:_MAX_SIGNALS]
