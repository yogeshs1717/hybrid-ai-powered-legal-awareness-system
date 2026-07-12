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

    def __init__(self, kb: KnowledgeBase):
        self._kb = kb
        # Flat corpus: one row per prototype text, remembering its issue.
        self._corpus_issue_ids: List[str] = []
        self._corpus_texts: List[str] = []
        for issue_id, issue in kb.issues.items():
            for prototype in issue.get("prototype_texts", []) or []:
                self._corpus_issue_ids.append(issue_id)
                self._corpus_texts.append(prototype)

        self._vectorizer = None
        self._prototype_matrix = None
        if self._corpus_texts:
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
            except ImportError:
                # Dependency absent: stay in no-data mode rather than crash the
                # whole service; /health will show issue_detector_mode.
                return
            # LOCKED (6.4): fit globally over ALL issue prototypes, in memory,
            # at startup. No .pkl artifact. Vectorizer parameters are
            # experiment-level configuration, kept at library defaults until
            # evaluation motivates changes.
            self._vectorizer = TfidfVectorizer()
            self._prototype_matrix = self._vectorizer.fit_transform(self._corpus_texts)

    @property
    def mode(self) -> str:
        return "active" if self._vectorizer is not None else "no_prototypes"

    def detect(self, scenario_text: str, predicted_domain_id: str) -> Optional[IssueDetection]:
        """Detect the issue within the predicted domain, or None.

        None is a legitimate state (no prototypes loaded, or the predicted
        domain has no issues in the KB) — the caller must route it to the
        explicit safe state, never invent an issue.
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

        from sklearn.metrics.pairwise import cosine_similarity

        scenario_vector = self._vectorizer.transform([scenario_text])
        similarities = cosine_similarity(
            scenario_vector, self._prototype_matrix[candidate_rows]
        )[0]
        best_position = int(similarities.argmax())
        best_row = candidate_rows[best_position]
        best_issue_id = self._corpus_issue_ids[best_row]
        best_score = float(similarities[best_position])

        issue = self._kb.issues[best_issue_id]
        display_name = issue.get("display_name") or best_issue_id
        signals = self._overlap_signals(scenario_text, self._corpus_texts[best_row])

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

    @staticmethod
    def _overlap_signals(scenario_text: str, prototype_text: str) -> List[str]:
        """Supporting explanation only (6.6): terms the scenario shares with
        the matched prototype. Never a decision input."""
        tokenize = lambda text: set(re.findall(r"[a-z]{3,}", text.lower()))
        overlap = tokenize(scenario_text) & tokenize(prototype_text) - _SIGNAL_NOISE
        return sorted(overlap)[:_MAX_SIGNALS]
