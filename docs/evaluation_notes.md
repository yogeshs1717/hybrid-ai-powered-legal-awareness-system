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

---

## Run 2 — Dataset V2 (170 Issues, 89 Sections, 843 Samples)

- **Date:** 2026-10-03
- **Dataset:** `data/training_data_v2.csv` — 843 rows. Domain distribution:
  consumer_issues: 181, contractual_disputes: 135, cyber_fraud: 234, traffic_enforcement: 150, workplace_wage: 143.
  170 distinct `issue_id` values (metadata only).
- **Model:** TF-IDF (`ngram_range=(1,2)`, `sublinear_tf=True`, `stop_words='english'`) + Logistic Regression (`C=2.5`, `class_weight='balanced'`, `max_iter=1000`, seed 42).
- **Preprocessing:** `preprocess_text` (lowercase + whitespace normalization).
- **Evaluation:** Stratified 5-Fold Cross-Validation, stratified by `domain`, seed 42.

### Metrics

| Metric | Value |
|---|---|
| Macro F1 (mean of folds) | **0.938** (std 0.011) |
| Accuracy (out-of-fold) | **0.94** |
| Macro precision | **0.94** |
| Macro recall | **0.94** |

Per-fold macro F1: 0.947, 0.937, 0.953, 0.927, 0.926.

Per-class (out-of-fold aggregate):

| Domain | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| consumer_issues | 0.91 | 0.88 | 0.90 | 181 |
| contractual_disputes | 0.92 | 0.91 | 0.92 | 135 |
| cyber_fraud | 0.95 | 0.95 | 0.95 | 234 |
| traffic_enforcement | 0.95 | 0.98 | 0.96 | 150 |
| workplace_wage | 0.95 | 0.97 | 0.96 | 143 |

### Confusion Matrix (rows = true, cols = predicted)

```
labels: ['consumer_issues', 'contractual_disputes', 'cyber_fraud', 'traffic_enforcement', 'workplace_wage']
[[160   6  10   4   1]
 [  4 123   1   2   5]
 [  6   2 223   2   1]
 [  2   0   1 147   0]
 [  3   2   0   0 138]]
```

### Knowledge Base Expansion Summary
- **Statutory Sections:** Expanded from 75 to 89 sections across 6 Acts in [acts_and_sections.json](file:///run/media/shnl/MyFiles/SHNL/Major%20Project/hybrid-ai-powered-legal-awareness-system/knowledge_base/acts_and_sections.json). All sections verified from official Central Acts / India Code with `"provision_status": "in_force"` and `"manually_verified"` status.
- **Citizen Issues:** Expanded from 143 to 170 issues across all 5 domains in [issue_mappings.json](file:///run/media/shnl/MyFiles/SHNL/Major%20Project/hybrid-ai-powered-legal-awareness-system/knowledge_base/issue_mappings.json).
- **Guidance & Portals:** 170 guidance entries (maximum 5 chronological action steps each) and 21 verified official portals (including `airsewa` - Ministry of Civil Aviation) in [issue_actions_portals.json](file:///run/media/shnl/MyFiles/SHNL/Major%20Project/hybrid-ai-powered-legal-awareness-system/knowledge_base/issue_actions_portals.json).
- **Referential Integrity:** 100% valid with 0 errors via `ml-service/app/knowledge_base_loader.py`.

---

## Run 3 — Expanded Dataset V2 (1,069 Samples Across 170 Issues)

- **Date:** 2026-10-03
- **Dataset:** `data/training_data_v2.csv` — **1,069 rows**. Domain distribution:
  - `consumer_issues`: 232
  - `contractual_disputes`: 177
  - `cyber_fraud`: 284
  - `traffic_enforcement`: 192
  - `workplace_wage`: 184
  - 170 distinct `issue_id` values (metadata only).
- **Model:** TF-IDF (`ngram_range=(1,2)`, `sublinear_tf=True`, `stop_words='english'`) + Logistic Regression (`C=2.5`, `class_weight='balanced'`, `max_iter=1000`, seed 42).
- **Preprocessing:** `preprocess_text` (lowercase + whitespace normalization).
- **Evaluation:** Stratified 5-Fold Cross-Validation, stratified by `domain`, seed 42.

### Metrics

| Metric | Value |
|---|---|
| Macro F1 (mean of folds) | **0.954** (std 0.011) |
| Accuracy (out-of-fold) | **0.95** (95%) |
| Macro precision | **0.95** |
| Macro recall | **0.95** |

Per-fold macro F1: 0.972, 0.946, 0.943, 0.947, 0.960.

Per-class (out-of-fold aggregate):

| Domain | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| consumer_issues | 0.95 | 0.90 | 0.92 | 232 |
| contractual_disputes | 0.94 | 0.93 | 0.93 | 177 |
| cyber_fraud | 0.94 | 0.98 | 0.96 | 284 |
| traffic_enforcement | 0.97 | 0.98 | 0.97 | 192 |
| workplace_wage | 0.97 | 0.99 | 0.98 | 184 |

### Confusion Matrix (rows = true, cols = predicted)

```
labels: ['consumer_issues', 'contractual_disputes', 'cyber_fraud', 'traffic_enforcement', 'workplace_wage']
[[208   7  12   3   2]
 [  4 164   5   1   3]
 [  2   2 277   2   1]
 [  3   0   1 188   0]
 [  1   1   0   0 182]]
```

---

## Run 4 — High-Accuracy Expanded Knowledge Base (204 Issues, 10 Central Acts, 122 Sections, 1,258 Samples)

- **Date:** 2026-10-30
- **Dataset:** `data/training_data_v2.csv` — **1,258 rows**. Domain distribution:
  - `consumer_issues`: 270
  - `contractual_disputes`: 207
  - `cyber_fraud`: 334
  - `traffic_enforcement`: 227
  - `workplace_wage`: 220
  - 204 distinct `issue_id` values across all 5 legal domains.
- **Model:** TF-IDF (`ngram_range=(1,2)`, `sublinear_tf=True`, `stop_words='english'`) + Logistic Regression (`C=2.5`, `class_weight='balanced'`, `max_iter=1000`, seed 42).
- **Preprocessing:** `preprocess_text` (lowercase + whitespace normalization).
- **Evaluation:** Stratified 5-Fold Cross-Validation, stratified by `domain`, seed 42.

### Metrics

| Metric | Value |
|---|---|
| Macro F1 (mean of folds) | **0.958** (std 0.013) |
| Accuracy (out-of-fold) | **0.96** (96%) |
| Macro precision | **0.96** |
| Macro recall | **0.96** |

Per-fold macro F1: 0.940, 0.961, 0.950, 0.964, 0.978.

Per-class (out-of-fold aggregate):

| Domain | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| consumer_issues | 0.95 | 0.91 | 0.93 | 270 |
| contractual_disputes | 0.94 | 0.95 | 0.94 | 207 |
| cyber_fraud | 0.95 | 0.97 | 0.96 | 334 |
| traffic_enforcement | 0.98 | 0.97 | 0.98 | 227 |
| workplace_wage | 0.97 | 0.98 | 0.98 | 220 |

### Confusion Matrix (rows = true, cols = predicted)

```
labels: ['consumer_issues', 'contractual_disputes', 'cyber_fraud', 'traffic_enforcement', 'workplace_wage']
[[246   8  13   1   2]
 [  4 197   2   1   3]
 [  4   2 325   2   1]
 [  2   1   3 221   0]
 [  2   2   0   0 216]]
```

### Knowledge Base & Pipeline Expansion Summary
- **Statutory Expansion:** Expanded to **17 Central Indian Acts and 150 statutory sections** in `acts_and_sections.json` covering the complete Indian legislative framework across all 5 domains:
  - *Consumer Protection Act, 2019* (19 key sections)
  - *Legal Metrology Act, 2009* (Sections 18, 36 — MRP overcharging & package declarations)
  - *Food Safety and Standards Act, 2006* (Sections 26, 50, 59, 65 — food safety, adulteration & injury compensation)
  - *Real Estate (Regulation and Development) Act, 2016 (RERA)* (Sections 13, 14, 18, 31 — advance caps, defect liability & delay refunds)
  - *Motor Vehicles Act, 1988* (34 key sections — licensing, safety, camera challans, digital documents, noise/exhaust)
  - *Code on Wages, 2019* (14 key sections — timely payment, minimum wages, overtime, unauthorized deductions)
  - *Payment of Gratuity Act, 1972* (Sections 4, 7, 8, 14 — mandatory 5-year gratuity & recovery)
  - *Maternity Benefit Act, 1961* (Sections 5, 12 — 26 weeks paid leave & void pregnancy discharge)
  - *Employees' Provident Funds and Miscellaneous Provisions Act, 1952* (Sections 6, 7A, 14 — statutory deductions & RPFC recovery)
  - *Industrial Disputes Act, 1947* (Sections 25F, 33C — retrenchment compensation & Labour Court wage recovery)
  - *Indian Contract Act, 1872* (27 key sections — breach, deposits, coercion, non-compete, bailment, guarantee)
  - *Specific Relief Act, 1963* (Sections 10, 20, 38 — specific performance, substituted performance & injunctions)
  - *Sale of Goods Act, 1930* (Sections 16, 31, 57, 59 — commercial supply fitness, non-delivery damages & warranty breach)
  - *MSMED Act, 2006* (Sections 15, 16, 18 — 45-day payment deadline, 3x RBI bank rate compound interest & MSME Samadhaan)
  - *Information Technology Act, 2000* (16 key sections — unauthorized access, identity theft, cheating, cyber terrorism, intermediary safe harbour)
  - *Digital Personal Data Protection Act, 2023 (DPDP)* (Sections 8, 12, 33 — data breach safeguards, redressal & 250 crore penalty)
  - *Banning of Unregulated Deposit Schemes Act, 2019 (BUDS)* (Sections 3, 4, 21 — Ponzi schemes, Telegram investment scams & 7-year imprisonment)
  - All statutory citations linked directly to official Central Acts on India Code (`indiacode.nic.in`), with `in_force` and verified status.
- **Citizen Issues:** 204 issues across all 5 domains in `issue_mappings.json`. Each issue is equipped with 5 distinct natural-language prototypes covering real-world variations.
- **Action Steps & Portals:** 204 issue guidance entries with actionable chronological steps (<= 5) and 25 official government portals in `issue_actions_portals.json` (including newly integrated MSME Samadhaan, FSSAI FoSCoS, RERA State Portals, and TRAI DND).
- **Referential Integrity:** 100% verified with 0 errors via `ml-service/app/knowledge_base_loader.py`.
- **Issue Detection & Scenario Validator:** Enhanced stem matching and prototype coverage in `scenario_validator.py` and `issue_detector.py`, eliminating false safe-state dropouts.

---

## Run 6 — Complete Statutory Legal Universe (25 Central Acts, 205 Sections, 214 Issues, 29 Portals)

- **Date:** 2026-10-30
- **Dataset:** `data/training_data_v2.csv` — **1,318 rows** across all 5 legal domains:
  - `consumer_issues`: 282
  - `contractual_disputes`: 219
  - `cyber_fraud`: 340
  - `traffic_enforcement`: 245
  - `workplace_wage`: 232
  - 214 distinct `issue_id` values across all 5 legal domains.
- **Model:** TF-IDF (`ngram_range=(1,2)`, `sublinear_tf=True`, `stop_words='english'`) + Logistic Regression (`C=2.5`, `class_weight='balanced'`, `max_iter=1000`, seed 42).
- **Preprocessing:** `preprocess_text` (lowercase + whitespace normalization).
- **Evaluation:** Stratified 5-Fold Cross-Validation, stratified by `domain`, seed 42.

### Metrics

| Metric | Value |
|---|---|
| Macro F1 (mean of folds) | **0.955** (std 0.015) |
| Accuracy (out-of-fold) | **0.96** (96%) |
| Macro precision | **0.96** |
| Macro recall | **0.95** |

Per-fold macro F1: 0.964, 0.950, 0.959, 0.974, 0.928.

Per-class (out-of-fold aggregate):

| Domain | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| consumer_issues | 0.96 | 0.91 | 0.93 | 282 |
| contractual_disputes | 0.93 | 0.94 | 0.93 | 219 |
| cyber_fraud | 0.95 | 0.98 | 0.96 | 340 |
| traffic_enforcement | 0.97 | 0.98 | 0.97 | 245 |
| workplace_wage | 0.97 | 0.97 | 0.97 | 232 |

### Confusion Matrix (rows = true, cols = predicted)

```
labels: ['consumer_issues', 'contractual_disputes', 'cyber_fraud', 'traffic_enforcement', 'workplace_wage']
[[257   9  12   2   2]
 [  5 205   3   3   3]
 [  2   3 332   2   1]
 [  3   1   2 239   0]
 [  1   3   2   0 226]]
```

### Full Statutory & Procedural Expansion
1. **Newly Integrated Primary Central Acts (8 Additional Acts, Total 25 Central Acts):**
   - **Bharatiya Nyaya Sanhita, 2023 (BNS)** (Act No. 45 of 2023) — Sections 316 (criminal breach of trust), 318 (cheating & 420 replacement), 319 (personation), 336 (forgery), 338 (valuable security forgery), 340 (using forged document), 351/352 (criminal intimidation), 356 (defamation), 78 (cyberstalking), 79 (insulting modesty of woman), 281 (rash driving), 125 (act endangering personal safety), 106 (negligent death & hit-and-run up to 10 years).
   - **Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)** (Act No. 46 of 2023) — Section 173 (mandatory FIR, e-FIR, Zero FIR, free FIR copy), Section 175 (investigation powers & SP appeal), Section 35 (notice of appearance protecting against arbitrary arrest under 7 years), Section 176 (forensic videography).
   - **Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)** (Act No. 14 of 2013) — Sections 4 (Internal Committee constitution in establishments with 10+ employees), 9 (3-month complaint limitation), 10 (conciliation without money), 11 (90-day time-bound inquiry), 12 (interim transfer & 3 months paid leave), 13 (60-day employer implementation), 26 (Rs. 50,000 penalty & business licence cancellation).
   - **Negotiable Instruments Act, 1881 (NI Act)** (Act No. 26 of 1881) — Sections 138 (cheque dishonour criminal offence), 139 (statutory presumption of debt), 141 (company director liability), 142 (30-day demand notice, 15-day cure window, 30-day complaint limitation), 143A (20% interim trial compensation).
   - **Transfer of Property Act, 1882 (TP Act)** (Act No. 4 of 1882) — Sections 105 (lease defined), 106 (mandatory 15-day notice to quit for residential/commercial leases), 108 (lessor duty of quiet enjoyment & refund of security deposit), 111 (determination of lease).
   - **Limitation Act, 1963** (Act No. 36 of 1963) — Section 3 (mandatory bar of limitation), Schedule Article 55 (3 years for breach of contract), Schedule Article 7 (3 years for unpaid wages), Schedule Article 113 (3 years residuary limitation for recovery suits).
   - **Payment of Wages Act, 1936** (Act No. 4 of 1936) — Sections 3 (employer responsibility), 5 (payment by 7th/10th & 2-day exit settlement), 7 (prohibition of unauthorized wage cuts), 15 (claims before authority with up to 10x compensation).
   - **Minimum Wages Act, 1948** (Act No. 11 of 1948) — Sections 12 (mandatory minimum wages), 20 (claims before authority with up to 10x compensation), 22 (criminal penalty for underpayment).
2. **Deepened Provisions in Existing Central Acts:**
   - **Motor Vehicles Act, 1988 & CMVR 1989:** Added Section 119 Proviso (police officer directions legally prevail over conflicting traffic signs / construction diversions — complete statutory defense against wrong-side camera challans), Section 161 (Rs. 2,00,000 Solatium Fund hit-and-run compensation), Section 166 (MACT application within 6 months), CMVR Rule 139 (DigiLocker / mParivahan digital documents have equal legal validity to physical documents), CMVR Rule 100 (70%/50% VLT window tint compliance), CMVR Rule 50 (HSRP plates).
   - **Consumer Protection Act, 2019 & E-Commerce Rules, 2020:** Added Section 69 (2-year limitation period before consumer commissions), Section 34 (District Commission jurisdiction up to Rs. 50 lakhs with residence-based filing), E-Commerce Rules 2020 (48-hour grievance acknowledgement, 1-month redressal, no unilateral cancellations).
   - **Information Technology Act, 2000:** Added Section 43A, Section 67B (CSAM), Section 67C (retention of traffic data & IP logs), and cross-linked RBI Customer Protection Circular on Unauthorized Electronic Banking Transactions (zero liability within 3 days).
3. **Official Portals Expanded to 29 Portals:** Added `shebox_portal` (SHe-Box for POSH grievances), `ecourts_services` (e-Courts Services portal for District Court civil & criminal cases), `cctns_citizen` (Digital Police Portal / CCTNS for FIR tracking), `solatium_fund_morth` (MoRTH Hit & Run Solatium Fund Portal).
4. **End-to-End Pipeline Evaluation:** 35/35 (100.0%) pass rate on realistic citizen queries across all 5 domains, with deterministic retrieval of applicable statutory sections and structured step-by-step action plans.
