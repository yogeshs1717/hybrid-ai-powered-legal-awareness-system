# Domain Classifier — Evaluation Notes

Per CLAUDE.md Sections 5, 11, 11.3. Never overwrite; append a new run section each time.

---

## Run 1 — Dataset V1 (baseline)

- **Date:** 2026-07-16
- **Dataset:** `data/training_data_v1.csv` — 133 rows, frozen. Domain distribution:
  cyber_fraud 28, consumer_issues 27, contractual_disputes 26, traffic_enforcement 26,
  workplace_wage 26. 22 distinct `issue_id` values (analysis metadata only — not a
  model feature/target).
- **Model:** TF-IDF + Logistic Regression (`max_iter=1000`, seed 42).
- **Preprocessing:** `preprocess_text` = lowercase + whitespace normalization
  (Baseline A). Shared identically by training and inference (imported from
  `app.classifier`).
- **TF-IDF config:** library defaults, `ngram_range=(1,1)`, `max_features=None`
  (experiment-level; not yet tuned).
- **Evaluation:** Stratified 5-Fold Cross-Validation, stratified by `domain`, seed 42.

### Metrics

| Metric | Value |
|---|---|
| Macro F1 (mean of folds) | **0.799** (std 0.051) |
| Accuracy (out-of-fold) | 0.80 |
| Macro precision | 0.81 |
| Macro recall | 0.80 |

Per-fold macro F1: 0.878, 0.737, 0.813, 0.748, 0.817.

Per-class (out-of-fold aggregate):

| Domain | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| consumer_issues | 0.65 | 0.56 | 0.60 | 27 |
| contractual_disputes | 0.72 | 0.88 | 0.79 | 26 |
| cyber_fraud | 0.84 | 0.93 | 0.88 | 28 |
| traffic_enforcement | 0.92 | 0.88 | 0.90 | 26 |
| workplace_wage | 0.91 | 0.77 | 0.83 | 26 |

### Confusion matrix (rows = true, cols = predicted)

```
labels: [consumer_issues, contractual_disputes, cyber_fraud, traffic_enforcement, workplace_wage]
[[15  6  4  1  1]
 [ 2 23  0  0  1]
 [ 1  0 26  1  0]
 [ 2  1  0 23  0]
 [ 3  2  1  0 20]]
```

### Findings (read the matrix, not just the number)

- **`consumer_issues` is the weakest class (recall 0.56)** and drives most of the
  error. Its confusions align with the two boundary pairs pre-registered in
  `TRAINING_DATA_PLAN.md` §9:
  - **consumer_issues → contractual_disputes (6):** the dominant confusion, exactly the
    pair the plan flagged. Both involve paid-for things not delivered; the
    service_deficiency vs breach_of_contract boundary is genuinely close in short text.
  - **consumer_issues → cyber_fraud (4):** online-shopping-fraud boundary, also
    pre-registered.
- **`issue_id` error slices** (analysis only, does not make Module 1 an issue
  classifier): most misclassified were `refund_denial` (4) and `service_deficiency`
  (4) — both consumer issues near the contractual boundary — plus `unpaid_wages` (3).
- **`workplace_wage` recall 0.77:** 3 wage rows → consumer_issues; wage-vs-consumer
  wording overlap ("not paid", "refund/salary") likely.
- Traffic and cyber are strong (F1 0.90, 0.88).

### Suspected causes (before adding data — CLAUDE.md §11, §15)

1. **Class-boundary ambiguity**, not raw scarcity, dominates: the errors cluster on the
   two documented hard boundaries, not randomly.
2. **Preprocessing loss / vocabulary:** unigram-only TF-IDF with no negation-aware
   handling may miss distinguishing cues ("agreement"/"contract" vs "seller"/"shop").
3. Not attributing to insufficient data alone.

### Proposed next steps for V2 (not applied yet)

- Add targeted consumer-vs-contract boundary examples that make the distinguishing
  signal explicit (formal agreement / business party → contractual; retail purchase or
  paid consumer service → consumer), rather than adding bulk rows.
- Try Baseline B/C: `ngram_range=(1,2)`, tuned `max_features`, negation-aware
  stopwords — compare macro F1 and the consumer/contract confusion cell specifically.
- Re-run 5-fold CV; a future untouched holdout / challenge set once V2 matures.
- No fixed accuracy target ends iteration; stop when the confusion matrix is understood
  and residual errors are reviewed as acceptable.

### Artifacts

`models/tfidf_domain_vectorizer.pkl`, `models/domain_classifier.pkl` — regenerable
from V1 + seed 42; gitignored (not committed). Service confirmed loading in
`classifier_mode = "trained"`.
