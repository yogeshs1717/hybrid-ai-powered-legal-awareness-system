"""Domain Classifier training pipeline — Module 1 (CLAUDE.md Sections 5, 11).

Pipeline-before-data (CLAUDE.md 11): this script is complete and runnable
BEFORE Dataset V1 exists, and must run identically on a 10-row smoke-test
file and the full V1 file. It does not generate data; it refuses politely if
the CSV is absent.

What it does:
  1. Loads a CSV with the locked schema: scenario, domain, issue_id (11.1).
     - ``domain`` is the ONLY supervised target.
     - ``issue_id`` is human-annotated analysis metadata: validated for
       integrity, echoed in coverage stats, NEVER used as a feature/target.
  2. Evaluates with Stratified 5-Fold Cross-Validation by domain, fixed seed
     (11.3) — macro F1, per-class precision/recall/F1, aggregate confusion
     matrix. A 70/15/15 split is deliberately NOT used at this dataset size.
  3. Fits the final TF-IDF + Logistic Regression on the full dataset and
     saves the two locked artifacts (Section 5):
         models/tfidf_domain_vectorizer.pkl
         models/domain_classifier.pkl

Hard rule honored: preprocessing is IMPORTED from app.classifier
(preprocess_text) — the exact function inference uses. No second copy exists.

TF-IDF/LogisticRegression parameters below are experiment-level DEFAULTS
(Section 5) — they are command-line configurable and must be selected via the
baseline comparisons on Dataset V1, then documented in
docs/evaluation_notes.md. No fixed accuracy number ends iteration; read the
confusion matrix (Section 11).

Usage (from the ml-service directory):
    python training/train_domain_classifier.py data/training_data_v1.csv
    python training/train_domain_classifier.py smoke.csv --folds 2
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

# Make ``app`` importable when run as a script from ml-service/.
_ML_SERVICE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ML_SERVICE_ROOT))

from app.classifier import (  # noqa: E402  (path setup must precede import)
    APPROVED_DOMAIN_IDS,
    MODEL_FILENAME,
    VECTORIZER_FILENAME,
    preprocess_text,
)

REQUIRED_COLUMNS = ("scenario", "domain", "issue_id")
DEFAULT_SEED = 42
DEFAULT_FOLDS = 5


def load_dataset(csv_path: Path) -> tuple[list[str], list[str], list[str]]:
    """Load and validate the dataset. Returns (scenarios, domains, issue_ids).

    Validation is structural only — label CORRECTNESS is a human annotation
    responsibility (TRAINING_DATA_PLAN.md Section 12), not this script's.
    """
    if not csv_path.is_file():
        sys.exit(
            f"Dataset not found: {csv_path}\n"
            "This is expected until Dataset V1 is created (gated on taxonomy "
            "sign-off and TRAINING_DATA_PLAN.md approval). The pipeline is "
            "ready; the data is not — by design (pipeline-before-data)."
        )

    scenarios: list[str] = []
    domains: list[str] = []
    issue_ids: list[str] = []
    problems: list[str] = []

    with open(csv_path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(
                f"CSV schema error: missing column(s) {missing}. "
                f"Required schema: {','.join(REQUIRED_COLUMNS)} (CLAUDE.md 11.1)."
            )
        for row_number, row in enumerate(reader, start=2):  # 1-based + header
            scenario = (row.get("scenario") or "").strip()
            domain = (row.get("domain") or "").strip()
            issue_id = (row.get("issue_id") or "").strip()
            if not scenario:
                problems.append(f"row {row_number}: empty scenario")
                continue
            if domain not in APPROVED_DOMAIN_IDS:
                problems.append(f"row {row_number}: unknown domain '{domain}'")
                continue
            if not issue_id:
                problems.append(f"row {row_number}: missing issue_id metadata")
                continue
            scenarios.append(scenario)
            domains.append(domain)
            issue_ids.append(issue_id)

    if problems:
        sys.exit("Dataset validation failed:\n- " + "\n- ".join(problems))
    if not scenarios:
        sys.exit("Dataset is empty after validation.")
    return scenarios, domains, issue_ids


def build_model(seed: int, max_features: int | None, ngram_max: int):
    """One place constructs the (experiment-configurable) model pipeline, so
    CV folds and the final fit are guaranteed identical."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline

    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=preprocess_text,  # THE shared function
                    max_features=max_features,
                    ngram_range=(1, ngram_max),
                ),
            ),
            ("logreg", LogisticRegression(max_iter=1000, random_state=seed)),
        ]
    )


def cross_validate(scenarios, domains, issue_ids, folds: int, seed: int,
                   max_features, ngram_max) -> None:
    """Stratified K-Fold CV by domain (CLAUDE.md 11.3). Prints macro F1,
    per-class report, and the fold-aggregated confusion matrix."""
    import numpy as np
    from sklearn.metrics import classification_report, confusion_matrix, f1_score
    from sklearn.model_selection import StratifiedKFold

    class_counts = Counter(domains)
    smallest = min(class_counts.values())
    if smallest < folds:
        print(
            f"NOTE: smallest domain has {smallest} row(s) < {folds} folds; "
            f"reducing folds to {smallest}."
        )
        folds = max(2, smallest)

    labels = sorted(class_counts)
    y = np.array(domains)
    x = np.array(scenarios)
    issue_meta = np.array(issue_ids)

    skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    macro_f1_scores: list[float] = []
    total_confusion = np.zeros((len(labels), len(labels)), dtype=int)
    all_true: list[str] = []
    all_pred: list[str] = []
    misclassified_issue_ids: Counter = Counter()

    for fold_number, (train_idx, val_idx) in enumerate(skf.split(x, y), start=1):
        model = build_model(seed, max_features, ngram_max)
        model.fit(x[train_idx], y[train_idx])
        predictions = model.predict(x[val_idx])

        fold_macro = f1_score(y[val_idx], predictions, average="macro")
        macro_f1_scores.append(fold_macro)
        total_confusion += confusion_matrix(y[val_idx], predictions, labels=labels)
        all_true.extend(y[val_idx])
        all_pred.extend(predictions)

        # issue_id error slicing (11.1): ANALYSIS ONLY — never a feature.
        for truth, pred, issue in zip(y[val_idx], predictions, issue_meta[val_idx]):
            if truth != pred:
                misclassified_issue_ids[issue] += 1
        print(f"fold {fold_number}/{folds}: macro F1 = {fold_macro:.3f}")

    print("\n=== Cross-validated results (aggregate over folds) ===")
    mean = float(np.mean(macro_f1_scores))
    std = float(np.std(macro_f1_scores))
    print(f"macro F1: mean {mean:.3f} (std {std:.3f})")
    print("\nPer-class report (all out-of-fold predictions):")
    print(classification_report(all_true, all_pred, labels=labels, zero_division=0))
    print("Confusion matrix (rows = true, cols = predicted):")
    print("labels:", labels)
    print(total_confusion)
    if misclassified_issue_ids:
        print("\nissue_id error slices (analysis metadata only — top 10):")
        for issue_id, count in misclassified_issue_ids.most_common(10):
            print(f"  {issue_id}: {count} misclassified")
    print(
        "\nREMINDER: record dataset version, configuration, these metrics, and "
        "confusion findings in docs/evaluation_notes.md. No fixed accuracy "
        "number ends iteration — understand the confusion matrix (CLAUDE.md 11)."
    )


def train_final_and_save(scenarios, domains, models_dir: Path, seed: int,
                         max_features, ngram_max) -> None:
    """Fit on ALL rows and save the two locked artifacts (CLAUDE.md 5)."""
    import joblib

    model = build_model(seed, max_features, ngram_max)
    model.fit(scenarios, domains)
    models_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model.named_steps["tfidf"], models_dir / VECTORIZER_FILENAME)
    joblib.dump(model.named_steps["logreg"], models_dir / MODEL_FILENAME)
    print(f"\nSaved: {models_dir / VECTORIZER_FILENAME}")
    print(f"Saved: {models_dir / MODEL_FILENAME}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="Dataset CSV (scenario,domain,issue_id)")
    parser.add_argument("--models-dir", type=Path,
                        default=_ML_SERVICE_ROOT / "models")
    parser.add_argument("--folds", type=int, default=DEFAULT_FOLDS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    # Experiment-level knobs (CLAUDE.md Section 5) — defaults are library
    # defaults, to be chosen via baseline comparison on Dataset V1:
    parser.add_argument("--max-features", type=int, default=None)
    parser.add_argument("--ngram-max", type=int, default=1)
    parser.add_argument("--no-save", action="store_true",
                        help="Evaluate only; do not write model artifacts.")
    args = parser.parse_args()

    scenarios, domains, issue_ids = load_dataset(args.csv_path)
    print(f"Loaded {len(scenarios)} rows from {args.csv_path}")
    print("Domain distribution:", dict(sorted(Counter(domains).items())))
    print("Distinct issue_ids (metadata only):", len(set(issue_ids)))

    cross_validate(scenarios, domains, issue_ids, args.folds, args.seed,
                   args.max_features, args.ngram_max)
    if not args.no_save:
        train_final_and_save(scenarios, domains, args.models_dir, args.seed,
                             args.max_features, args.ngram_max)


if __name__ == "__main__":
    main()
