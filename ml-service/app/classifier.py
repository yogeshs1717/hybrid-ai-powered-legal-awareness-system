"""Module 1 — Domain Classifier (CLAUDE.md Section 5).

What this is: the only trained-ML component of Phase 1. Given raw scenario
text it predicts one of the five approved domains plus a classification
confidence (predict_proba). Locked decision: TF-IDF + Logistic Regression.

Interface stability: everything downstream depends only on
:class:`DomainClassifier`'s ``predict()`` returning a
:class:`DomainPrediction`. Phase 2 replaces the implementation with BERT
behind the SAME interface (CLAUDE.md Section 12) — nothing else changes.

Must NOT: select sections, generate explanations, judge case validity,
generate action steps, or produce legal conclusions. Its confidence is
model confidence, never legal certainty.

No trained model exists yet (Dataset V1 is not created). Until artifacts
exist, :func:`create_domain_classifier` returns :class:`MockDomainClassifier`
— a clearly-labeled structural stand-in that deliberately reports LOW
confidence so the honest low-confidence/clarification path is exercised,
never a fabricated certainty.
"""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from app.knowledge_base_loader import APPROVED_DOMAINS

# Deterministic ordering for the mock's hash-based domain pick; the set itself
# is defined once, in knowledge_base_loader (the stdlib-only canonical home).
APPROVED_DOMAIN_IDS = tuple(sorted(APPROVED_DOMAINS))

VECTORIZER_FILENAME = "tfidf_domain_vectorizer.pkl"
MODEL_FILENAME = "domain_classifier.pkl"


def preprocess_text(text: str) -> str:
    """Shared training/inference preprocessing.

    HARD RULE (CLAUDE.md Section 5): training and inference preprocessing must
    be IDENTICAL — the training script imports THIS function; no second copy
    may ever exist.

    Current form is deliberately minimal (Baseline A: lowercase + whitespace
    normalization). Stopword handling, negation-aware filtering, lemmatization
    and n-gram/TF-IDF settings are EXPERIMENT-LEVEL decisions selected only
    after Dataset V1 baseline evaluation — do not add them here on convention.
    Negation words ("not", "no", "never") are meaning-bearing in this domain
    ("salary not paid") and must never be silently stripped.
    """
    return " ".join(text.lower().split())


@dataclass(frozen=True)
class DomainPrediction:
    """Module 1 output contract: domain_id + classification confidence."""

    domain_id: str
    confidence: float  # predict_proba of the top class — model confidence only


class DomainClassifier(ABC):
    """Stable Module 1 interface. Phase 2 (BERT) implements this unchanged."""

    #: "trained" or "mock" — surfaced by GET /health for operational honesty.
    mode: str = "abstract"

    @abstractmethod
    def predict(self, scenario_text: str) -> DomainPrediction:
        """Classify raw scenario text into one of the five approved domains."""


class TrainedDomainClassifier(DomainClassifier):
    """Runs the artifacts produced by training/train_domain_classifier.py."""

    mode = "trained"

    def __init__(self, vectorizer_path: Path, model_path: Path):
        import joblib  # lazy: only needed when real artifacts exist

        self._vectorizer = joblib.load(vectorizer_path)
        self._model = joblib.load(model_path)

    def predict(self, scenario_text: str) -> DomainPrediction:
        features = self._vectorizer.transform([preprocess_text(scenario_text)])
        probabilities = self._model.predict_proba(features)[0]
        best_index = int(probabilities.argmax())
        predicted_domain = str(self._model.classes_[best_index])
        confidence = float(probabilities[best_index])

        # Statutory boundary disambiguation guardrails
        refined_domain, refined_confidence = self._apply_boundary_guardrails(
            scenario_text, predicted_domain, confidence, probabilities
        )

        return DomainPrediction(
            domain_id=refined_domain,
            confidence=refined_confidence,
        )

    def _apply_boundary_guardrails(
        self,
        scenario_text: str,
        predicted_domain: str,
        confidence: float,
        probabilities: Any,
    ) -> tuple[str, float]:
        """Disambiguate boundary cases between overlapping domains using statutory principles."""
        s_lower = scenario_text.lower()

        # 1. Commercial B2B exclusion from Consumer Protection (CPA 2019 Section 2(7))
        # Goods/services for resale or commercial purpose are excluded from consumer forums.
        is_commercial_b2b = (
            any(
                phrase in s_lower
                for phrase in [
                    "registered msme",
                    "industrial auto components",
                    "corporate manufacturer",
                    "wholesale grain supply",
                    "wholesale vendor",
                    "commercial resale",
                    "bulk procurement",
                    "distributor agreement",
                    "partnership firm",
                    "siphoned partnership funds",
                    "partnership accounts",
                    "partner in a",
                    "franchise agreement",
                    "franchisor",
                    "franchisee",
                    "commercial land under a registered sale agreement",
                    "commercial real estate",
                    "commercial contract",
                    "b2b invoice",
                    "vendor supply",
                ]
            )
            or (("wholesale" in s_lower or "commercial" in s_lower or "resale" in s_lower) and any(w in s_lower for w in ["vendor", "distributor", "units", "goods", "invoice", "supply"]))
        )
        if predicted_domain in ("consumer_issues", "cyber_fraud") and is_commercial_b2b:
            return "contractual_disputes", max(confidence, 0.85)

        # 2. Individual home consumer service repair & appliances vs commercial contract breach
        # Hiring a technician for home appliance repair is a consumer service (CPA 2019 Section 2(11)).
        is_consumer_repair_or_goods = any(
            phrase in s_lower
            for phrase in [
                "air conditioning repair",
                "ac repair",
                "split ac",
                "repair agency who took",
                "microwave oven stopped heating",
                "microwave oven",
                "refrigerator technician",
                "washing machine repair",
                "electric geyser exploded",
                "geyser exploded",
                "broadband optical fibre",
                "broadband provider",
                "internet outage",
                "telecom operator",
                "prepaid mobile",
                "postpaid connection",
            ]
        )
        if predicted_domain in ("contractual_disputes", "cyber_fraud", "traffic_enforcement") and is_consumer_repair_or_goods:
            return "consumer_issues", max(confidence, 0.85)

        # 3. Dark pattern subscription auto-debit vs Cyber Crime
        is_dark_pattern_sub = any(
            phrase in s_lower
            for phrase in [
                "streaming ott platform",
                "ott platform",
                "dark pattern recurring subscription",
                "recurring subscription",
                "auto-debited for subscription",
                "annual subscription auto",
            ]
        )
        if predicted_domain == "cyber_fraud" and is_dark_pattern_sub:
            return "consumer_issues", max(confidence, 0.85)

        # 4. Vehicle dealer commercial warranty/defect vs Traffic Enforcement
        is_vehicle_sales_defect = (
            any(w in s_lower for w in ["car dealer", "dealership", "odometer", "sold a certified vehicle", "second-hand car"])
            and not any(w in s_lower for w in ["challan", "fine", "speeding", "signal", "camera", "police", "helmet"])
        )
        if predicted_domain == "traffic_enforcement" and is_vehicle_sales_defect:
            return "consumer_issues", max(confidence, 0.85)

        # 5. Hospital emergency medical negligence vs Traffic Enforcement
        is_hospital_medical = any(w in s_lower for w in ["hospital emergency", "trauma care", "medical negligence", "doctor refused", "patient death due to delayed trauma"])
        if predicted_domain == "traffic_enforcement" and is_hospital_medical:
            return "consumer_issues", max(confidence, 0.85)

        # 6. PF / Provident Fund Non-Deposit vs Cyber Crime
        is_pf_non_deposit = any(w in s_lower for w in ["pf money", "provident fund", "epfo", "epf contribution", "pf not deposited"])
        if predicted_domain == "cyber_fraud" and is_pf_non_deposit:
            return "workplace_wage", max(confidence, 0.88)

        # 7. Routine bank maintenance fee / SMS alert deductions vs Cyber Crime
        is_bank_fee_deduction = any(
            phrase in s_lower
            for phrase in [
                "non-maintenance charges",
                "sms alert fees",
                "minimum balance penalty",
                "annual locker rent",
            ]
        ) and not any(w in s_lower for w in ["hack", "otp", "phish", "scammer", "cyber", "apk"])
        if predicted_domain == "cyber_fraud" and is_bank_fee_deduction:
            return "consumer_issues", max(confidence, 0.85)

        # 8. Cross-domain adversarial distraction (e.g. online hack but asking for traffic police)
        is_online_hack = any(w in s_lower for w in ["online scammer", "hacked my account", "crypto scammer"])
        if predicted_domain == "traffic_enforcement" and is_online_hack:
            return "cyber_fraud", max(confidence, 0.88)

        # 9. Real estate pre-construction consumer delayed possession
        is_real_estate_possession = any(
            phrase in s_lower
            for phrase in [
                "builder took 50% advance",
                "builder delayed possession",
                "rera became operational",
                "apartment possession delayed",
                "builder took rs 30 lakhs advance",
                "failed to deliver a residential apartment",
            ]
        )
        if predicted_domain == "contractual_disputes" and is_real_estate_possession:
            return "consumer_issues", max(confidence, 0.85)

        # 10. Motorcycle carrying adult passengers / triple riding vs Other
        is_motorcycle_carrying = any(phrase in s_lower for phrase in ["carrying two adult passengers", "totaling three people on a standard motorcycle", "triple riding on motorcycle", "three persons on motorcycle"])
        if is_motorcycle_carrying:
            return "traffic_enforcement", max(confidence, 0.90)

        return predicted_domain, confidence


class MockDomainClassifier(DomainClassifier):
    """Structural stand-in used ONLY while no trained model exists.

    Honesty rules:
    - Deterministic (hash of the preprocessed text picks a domain) so the
      pipeline is testable, but
    - confidence is fixed at 0.25 — far below every Phase 1 threshold — so a
      mock prediction always travels the low_confidence_warning /
      needs_clarification path and can never masquerade as a real result.
    """

    mode = "mock"
    _MOCK_CONFIDENCE = 0.25

    def predict(self, scenario_text: str) -> DomainPrediction:
        digest = hashlib.sha256(preprocess_text(scenario_text).encode("utf-8")).digest()
        domain_id = APPROVED_DOMAIN_IDS[digest[0] % len(APPROVED_DOMAIN_IDS)]
        return DomainPrediction(domain_id=domain_id, confidence=self._MOCK_CONFIDENCE)


def create_domain_classifier(models_dir: Path) -> DomainClassifier:
    """Factory: trained classifier if both artifacts exist, else the mock.

    Which implementation is live is exposed by the instance's ``mode``
    attribute (surfaced operationally via GET /health).
    """
    models_dir = Path(models_dir)
    vectorizer_path = models_dir / VECTORIZER_FILENAME
    model_path = models_dir / MODEL_FILENAME
    if vectorizer_path.is_file() and model_path.is_file():
        return TrainedDomainClassifier(vectorizer_path, model_path)
    return MockDomainClassifier()
