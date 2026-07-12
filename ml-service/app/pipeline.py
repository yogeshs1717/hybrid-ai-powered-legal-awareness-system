"""Analysis pipeline — pure orchestration of Modules 1-4.

What this is: the wiring, and only the wiring. It calls Module 1, hands its
output to Module 2, hands that to Module 3, and hands everything to Module 4.
It contains NO business logic: no thresholds, no eligibility checks, no
similarity math, no wording. If a decision needs making, it belongs inside
the module that owns it — never here.

NOT the deprecated prototype ``pipeline.py``: that file was a monolith that
embedded all four modules' logic in one place and was explicitly rejected
(PROJECT_STATE.md, deprecated items). This class exists precisely so the four
modules stay separate — which is what makes the Phase 2 BERT swap of
Modules 1-2 a constructor-argument change and nothing more.

Dependency injection: every module arrives as a constructor argument. The
pipeline never constructs its own dependencies, so any module can be replaced
(mock classifier today, trained tomorrow, BERT in Phase 2) without touching
this file.
"""

from __future__ import annotations

from app.classifier import DomainClassifier
from app.issue_detector import IssueDetector
from app.legal_intelligence import LegalIntelligenceEngine
from app.response_builder import ResponseBuilder
from app.schemas import AnalyzeResponse


class AnalysisPipeline:
    """Module 1 -> Module 2 -> Module 3 -> Module 4, nothing else."""

    def __init__(
        self,
        classifier: DomainClassifier,
        issue_detector: IssueDetector,
        legal_engine: LegalIntelligenceEngine,
        response_builder: ResponseBuilder,
    ):
        self._classifier = classifier
        self._issue_detector = issue_detector
        self._legal_engine = legal_engine
        self._response_builder = response_builder

    def analyze(self, scenario_text: str, request_id: str) -> AnalyzeResponse:
        # Module 1 — Domain Classification (trained model or honest mock).
        domain_prediction = self._classifier.predict(scenario_text)

        # Module 2 — Issue Detection using Prototype Similarity Matching,
        # scoped to the predicted domain. May be None (legitimate state).
        issue_detection = self._issue_detector.detect(
            scenario_text, domain_prediction.domain_id
        )

        # Module 3 — Legal Intelligence Engine (KB lookup + eligibility gate).
        intelligence = self._legal_engine.retrieve(
            issue_detection.issue_id if issue_detection else None
        )

        # Module 4 — Response Builder (assembly of the locked contract).
        return self._response_builder.build(
            request_id=request_id,
            domain_prediction=domain_prediction,
            issue_detection=issue_detection,
            intelligence=intelligence,
        )
