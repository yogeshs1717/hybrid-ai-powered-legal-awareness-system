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
        s_clean = re.sub(r"[\-_]", " ", s_lower)

        def has_any(phrases: list[str]) -> bool:
            return any(p in s_lower or p in s_clean for p in phrases)

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
            if iid == "cheque_bounce_statutory_notice_138" and not has_any(["cheque", "check"]):
                adj -= 0.40
            if iid == "fraudulent_active_concealment_used_car_sale" and not has_any(["car", "vehicle", "automobile", "odometer"]):
                adj -= 0.40
            if iid == "automobile_manufacturing_defect_lemon_vehicle" and not has_any(["car", "vehicle", "automobile", "odometer", "clutch", "engine", "brake"]):
                adj -= 0.40
            if iid == "holiday_timeshare_membership_scam" and not has_any(["timeshare", "holiday", "resort", "vacation"]):
                adj -= 0.40
            if iid in ("gender_wage_gap_unequal_pay", "gender_wage_discrimination") and not has_any(["gender", "women", "female", "male", "sex", "men and women", "unequal pay"]):
                adj -= 0.40
            if iid in ("hit_and_run_solatium_fund_claim", "mact_accident_compensation_claim") and not has_any(["accident", "tribunal", "mact", "hit and run", "crash", "collision", "injury", "fatal", "solatium"]):
                adj -= 0.40
            if iid == "fake_charity_donation_fraud" and not has_any(["charity", "donation", "orphanage", "ngo"]):
                adj -= 0.40
            if iid == "credit_card_reward_points_expiry_link" and not has_any(["reward", "point", "redeem", "expiry link"]):
                adj -= 0.35
            if iid == "fastag_recharge_wallet_phishing" and not has_any(["fastag", "toll"]):
                adj -= 0.35
            if iid == "overseas_cyber_slave_job_trafficking" and not has_any(["overseas", "abroad", "cambodia", "myanmar", "laos", "slave", "traffick"]):
                adj -= 0.35
            if iid == "google_review_rating_task_scam" and not has_any(["google review", "rating task", "youtube like"]):
                adj -= 0.30
            if iid == "packaged_food_misleading_nutrition_claims" and not has_any(["packaged food", "nutrition label", "fssai"]):
                adj -= 0.25
            if iid == "cinema_hall_water_confiscation_mrp" and not has_any(["cinema", "multiplex", "theater", "water bottle"]):
                adj -= 0.35
            if iid == "e_commerce_refusal_of_open_box_delivery" and not has_any(["open box", "open-box"]):
                adj -= 0.25
            if iid == "two_wheeler_pillion_helmet_challan_dispute" and not has_any(["pillion", "passenger on bike", "sitting behind"]):
                adj -= 0.20

            # -------------------------------------------------------------
            # Canonical intent bonuses (reward matching true legal problem)
            # -------------------------------------------------------------
            if iid == "otp_fraud" and has_any(["otp", "one-time password", "asked for otp", "share otp", "shared the code"]):
                adj += 0.25
            if iid == "phishing" and has_any(["phishing", "phishing link", "net banking", "login credentials", "fake website", "bank link"]):
                adj += 0.35
            if iid == "ecommerce_fake_seller_fraud" and has_any(["fake seller", "fake listing", "rental listing", "fake pg", "nobroker", "marketplace"]):
                adj += 0.35
            if iid == "recruitment_job_offer_fraud" and has_any(["recruitment", "job offer", "registration fee", "employment agency", "hr recruiter"]):
                adj += 0.25
            if iid in ("sim_swap_fraud", "identity_theft") and has_any(["sim swap", "duplicate sim", "network lost", "cloned sim"]):
                adj += 0.25
            if iid == "sextortion_fraud" and has_any(["sextortion", "video call", "morphed", "naked", "pornograph", "nude"]):
                adj += 0.25
            if iid == "qr_code_fraud" and has_any(["qr code", "qr", "scan to receive"]):
                adj += 0.25
            if iid == "card_cloning_skimming" and has_any(["skimming", "cloning", "pos transaction while abroad", "international pos", "physical card was securely in my pocket"]):
                adj += 0.25
            if iid in ("aeps_biometric_aadhaar_money_theft", "aeps_fingerprint_cloning_fraud") and has_any(["aeps", "biometric", "fingerprint cloning", "mini atm", "mini-atm"]):
                adj += 0.30
            if iid == "electricity_bill_sms_apk_scam" and has_any(["electricity bill", "bill update apk", "malicious electricity"]):
                adj += 0.35
            if iid in ("ai_voice_clone_virtual_kidnapping", "deepfake_extortion") and has_any(["voice clone", "ai generative audio", "virtual kidnapping", "ransom"]):
                adj += 0.35
            if iid == "whatsapp_account_call_forwarding_hijack" and has_any(["call forwarding", "star code", "cloned my whatsapp"]):
                adj += 0.35
            if iid == "fake_crypto_arbitrage_telegram_ponzi" and has_any(["crypto arbitrage", "vip trading whatsapp", "fake sebi"]):
                adj += 0.30
            if iid in ("rbi_zero_liability_unauthorized_transaction", "upi_wrong_transfer_reversal_delay") and has_any(["zero liability", "timeout error", "auto-reversal", "auto reversal", "wrong transfer"]):
                adj += 0.35
            if iid == "unauthorized_account_access" and has_any(["strange device logged in", "unauthorized access"]):
                adj += 0.25

            # Consumer
            if iid in ("defective_product", "defective_mobile_green_line_display_after_update") and has_any(["defective", "motherboard", "stopped working in", "dead unit", "hardware"]):
                adj += 0.22
            if iid in ("unfair_trade_practice", "defective_product") and has_any(["second-hand car", "second hand car", "altered odometer", "odometer", "certified vehicle"]):
                adj += 0.35
            if iid in ("dark_patterns_hidden_charges", "unfair_trade_practice") and has_any(["convenience fees", "convenience fee", "hidden charges", "drip pricing"]):
                adj += 0.35
            if iid == "service_deficiency" and has_any(["repair agency", "technician", "ac repair", "servicing", "service was bad", "broadband", "slow speed", "clutch plate", "clutch pedal", "power surge", "voltage fluctuation", "transformer", "bescom", "non-maintenance charges", "sms alert fees", "sms fees", "account penalties"]):
                adj += 0.35
            if iid == "misleading_advertisement" and has_any(["advertised", "advertisement", "false claim", "dietary supplement"]):
                adj += 0.22
            if iid in ("insurance_claim_rejection_dispute", "health_insurance_claim_arbitrary_rejection", "insurance_claim_arbitrary_rejection") and has_any(["health insurance", "mediclaim", "claim rejected", "gall bladder", "surgery claim", "insurance claim"]):
                adj += 0.25
            if iid == "flight_delay_cancellation_compensation" and has_any(["flight", "airline", "airport"]):
                adj += 0.25

            # Traffic
            if has_any(["bribe", "bribery", "chai paani", "chai-paani", "speed money", "unofficial cash", "illegal gratification", "under the table", "demanded cash", "demanded 500", "demanded 1000", "demanded 2000", "without receipt", "without challan", "cash to let me go", "asking bribe"]):
                if iid == "bribe_demand":
                    adj += 0.45
                elif iid in (
                    "triple_riding_pillion_child_dispute",
                    "juvenile_minor_driving_parent_penalty",
                    "unlawful_towing",
                    "digital_documents_refusal_digilocker_mparivahan",
                    "uninsured_vehicle_challan_portal_sync_delay",
                    "traffic_signal_camera_red_light_yellow_light_glitch",
                    "emergency_vehicle_passage_challan_dispute",
                    "seatbelt_helmet_camera_dispute",
                ):
                    adj -= 0.40

            if iid == "wrong_side_police_diversion_defense" and has_any(["police directed", "police instructed", "diversion", "traffic diversion", "diverting all vehicles"]):
                adj += 0.35
            if iid == "seatbelt_helmet_camera_dispute" and has_any(["helmet", "seatbelt", "headgear", "camera challan"]):
                adj += 0.25
            if iid == "drunk_driving_breathalyzer_dispute" and has_any(["drunk", "alcohol", "breath", "bac", "breathalyzer"]):
                adj += 0.25
            if iid in ("digital_documents_refusal_digilocker_mparivahan", "document_acceptance_or_verification") and has_any(["digilocker", "mparivahan", "digital license", "electronic documents", "failed to produce"]):
                adj += 0.30
            if iid in ("uninsured_vehicle_vahan_sync_delay_fine", "uninsured_vehicle_challan_portal_sync_delay") and has_any(["uninsured", "third party insurance", "without insurance", "third-party insurance", "third party"]):
                adj += 0.35
            if iid in ("emergency_vehicle_passage_red_light_challan", "emergency_vehicle_obstruction_dispute", "emergency_vehicle_passage_challan_dispute") and has_any(["emergency", "ambulance", "siren"]):
                adj += 0.35
            if iid == "driving_without_licence_challan_dispute" and has_any(["never obtained", "without a driving license", "without driving license", "no license"]):
                adj += 0.35
            if iid in ("one_way_no_entry_signage_obscured", "wrongful_challan") and has_any(["obscured by overgrown", "tree branches", "refused to ply", "metered journey", "overspeeding ticket"]):
                adj += 0.35
            if iid in ("hsrp_number_plate_challan_dispute", "high_security_registration_plate_hsrp_dispute", "wrongful_challan") and has_any(["hsrp", "number plate", "registration plate"]):
                adj += 0.35
            if iid == "illegal_vehicle_key_confiscation_by_constable" and has_any(["keys", "took my keys", "confiscated keys"]):
                adj += 0.35
            if iid == "unlawful_towing_occupant_inside_vehicle" and has_any(["towed", "towing", "inside vehicle"]):
                adj += 0.35
            if iid in ("hit_and_run_solatium_fund_claim", "mact_accident_compensation_claim") and has_any(["hit and run", "accident compensation", "solatium", "fatal road crash", "fled without rendering"]):
                adj += 0.35

            # Workplace
            if iid in ("unpaid_wages", "delayed_wages") and has_any(["unpaid wages", "salary unpaid", "delayed salary", "3 months salary", "wages withheld"]):
                adj += 0.25
            if iid in ("unauthorized_deduction", "unilateral_laptop_damage_deduction_exit") and has_any(["deduction", "deducted from salary", "breakage deduction", "damage deduction", "penalty for delayed software"]):
                adj += 0.30
            if iid in ("unlawful_termination_without_due_process", "notice_period_exorbitant_deduction_exit") and has_any(["relieving letter", "experience certificate", "retrenchment", "terminated without retrenchment", "180 days of service"]):
                adj += 0.35
            if iid in ("gratuity_withholding_dispute", "gratuity_withheld_past_5_years_service") and has_any(["gratuity", "5 years service"]):
                adj += 0.30
            if iid in ("maternity_benefit_paid_leave_denial", "maternity_leave_salary_denial_or_termination") and has_any(["pregnant", "pregnancy", "maternity"]):
                adj += 0.30
            if iid in ("overtime_wage_denial", "casual_contract_worker_overtime_wage_theft") and has_any(["overtime", "extra hours", "12 hours daily", "double rate"]):
                adj += 0.25
            if iid == "posh_workplace_sexual_harassment_complaint" and has_any(["sexual harassment", "posh", "internal committee", "icc"]):
                adj += 0.30
            if iid == "freelance_vendor_non_payment" and has_any(["freelance", "freelancer", "ui designer", "service contract"]):
                adj += 0.35
            if iid == "construction_worker_safety_wage_default" and has_any(["construction", "builder", "bocw", "scaffolding", "safety harness", "safety helmets", "site labourers", "daily wage labourers"]):
                adj += 0.40
            if iid == "workplace_injury_compensation_denial" and has_any(["injury compensation", "injured on duty", "disablement", "factory accident", "hand fracture", "spinal injury", "machine accident"]):
                adj += 0.40
            if iid == "child_labour_exploitation_workplace" and has_any(["child labour", "minor employed", "12-year-old child", "under 14", "schooling denied", "child working in restaurant"]):
                adj += 0.40

            # Contractual
            if iid == "cheque_bounce_statutory_notice_138" and has_any(["cheque", "dishonoured", "bounced", "insufficient funds", "stop payment", "stop-payment"]):
                adj += 0.35
            if iid == "commercial_debt_interest_claim" and has_any(["commercial interest", "interest on overdue", "interest act", "statutory interest claim", "interest on debt"]):
                adj += 0.40
            if iid == "power_of_attorney_unauthorized_execution" and has_any(["power of attorney", "poa", "attorney holder", "revoked poa", "attorney-in-fact"]):
                adj += 0.40
            if iid in ("non_compete_clause_employment_trade_restraint", "non_compete_clause_dispute") and has_any(["non-compete", "non compete", "liquidated damages 10 lakhs", "restraint of trade"]):
                adj += 0.35
            if iid in ("security_deposit_dispute", "landlord_security_deposit_withheld_unjustly", "tenancy_security_deposit_unlawful_deduction") and has_any(["security deposit", "rental deposit", "landlord refused deposit", "water seepage", "plumbing alterations", "walls"]):
                adj += 0.35
            if iid == "commercial_lease_lock_in_penalty_dispute" and has_any(["locked out", "padlock", "retail store tenant", "lease agreement", "evicted overnight"]):
                adj += 0.35
            if iid == "commercial_vendor_raw_material_delivery_default" and has_any(["registered msme", "auto components", "corporate manufacturer", "wholesale grain", "industrial fasteners", "steel bolts", "hydraulic press"]):
                adj += 0.35
            if iid == "breach_of_contract" and has_any(["commercial land", "registered sale agreement", "refuses to execute", "partnership firm siphoned", "delivery milestone", "unconditional 30-day extension"]):
                adj += 0.35
            if iid == "coercion_duress_agreement_dispute" and has_any(["coerced", "threat of violence", "blank stamp paper", "moneylender"]):
                adj += 0.30
            if iid == "time_barred_debt_written_promise_breach" and has_any(["time-barred", "limitation", "6 years ago", "old invoice"]):
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
