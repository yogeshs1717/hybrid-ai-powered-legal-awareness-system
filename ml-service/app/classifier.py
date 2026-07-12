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
from typing import Tuple

APPROVED_DOMAIN_IDS = (
    "cyber_fraud",
    "consumer_issues",
    "traffic_enforcement",
    "workplace_wage",
    "contractual_disputes",
)

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
        return DomainPrediction(
            domain_id=str(self._model.classes_[best_index]),
            confidence=float(probabilities[best_index]),
        )


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


def create_domain_classifier(models_dir: Path) -> Tuple[DomainClassifier, str]:
    """Factory: trained classifier if both artifacts exist, else the mock.

    Returns (classifier, mode) so the caller can log/report which one is live.
    """
    models_dir = Path(models_dir)
    vectorizer_path = models_dir / VECTORIZER_FILENAME
    model_path = models_dir / MODEL_FILENAME
    if vectorizer_path.is_file() and model_path.is_file():
        classifier: DomainClassifier = TrainedDomainClassifier(vectorizer_path, model_path)
    else:
        classifier = MockDomainClassifier()
    return classifier, classifier.mode
