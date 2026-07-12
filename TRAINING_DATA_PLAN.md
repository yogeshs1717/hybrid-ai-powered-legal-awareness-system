# TRAINING_DATA_PLAN.md
# Dataset Blueprint — Smart Legal Intelligence System
# Governance Gate — Must Be Approved Before Any Training CSV Is Generated

---

> This is a blueprint, not a dataset. No scenarios are generated here. Per
> `CLAUDE.md` Section 11, `training_data_v1.csv` may not be created until this plan
> is approved by the user **and** the Issue Support Review (Section 3) has cleared.
>
> **Status: DRAFT — PENDING TAXONOMY SUPPORT REVIEW AND USER APPROVAL.**

---

## 1. Domain Labels (Final — 5)

| Domain ID | Display Name |
|---|---|
| `cyber_fraud` | Cyber Fraud |
| `consumer_issues` | Consumer Issues |
| `traffic_enforcement` | Traffic Enforcement |
| `workplace_wage` | Workplace / Wage |
| `contractual_disputes` | Contractual Disputes |

`domain` is the **only supervised target** for the Module 1 Domain Classifier.

## 2. Working Issue Taxonomy (22 working issues)

This taxonomy is a **working proposal**, not legally final. It stays WORKING until the
Issue Support Review (Section 3) clears and the user signs it off. It must not be used
to populate the legal KB (`acts_and_sections.json` / `issue_mappings.json`) or to label
Dataset V1 before that.

```
cyber_fraud (6)
├── otp_fraud                          OTP theft / banking impersonation
├── online_impersonation               Fake officials or fake identity
├── phishing                           Fake links, fake login pages
├── identity_theft                     Aadhaar/PAN misuse, credential theft
├── other_online_financial_fraud       Online financial deception not fitting the
│                                       above (see scope note below — NOT a catch-all)
└── unauthorized_account_access        Hacked email, social media, accounts

consumer_issues (5)
├── defective_product                  Broken or faulty goods received
├── refund_denial                      Refused refund within policy window
├── misleading_advertisement           False product claims, fake discounts
├── service_deficiency                 Paid service not delivered as promised
└── unfair_trade_practice              Deceptive commercial practices

traffic_enforcement (5)
├── bribe_demand                       Officer demands cash payment
├── wrongful_challan                   Incorrect or false fine issued
├── document_acceptance_or_verification  Dispute over whether a licence / RC /
│                                         insurance / DigiLocker / mParivahan record
│                                         is accepted or considered valid during
│                                         enforcement or verification
├── document_seizure_or_retention      Authority takes / seizes / retains a licence,
│                                         RC, or other traffic document and the citizen
│                                         questions the authority, basis, or procedure
└── vehicle_detention                  Unlawful detention of vehicle

workplace_wage (4)
├── delayed_wages                      Salary not paid on time
├── unpaid_wages                       Salary withheld entirely
├── unauthorized_deduction             Illegal deductions from salary
└── minimum_wage_violation             Paid below statutory minimum

contractual_disputes (2)
├── breach_of_contract                 Failure to perform, or violation of, an agreed
│                                         contractual obligation (broad Phase 1 issue —
│                                         see note below)
└── security_deposit_dispute           Deposit not returned after agreement
```

**Count:** 6 + 5 + 5 + 4 + 2 = **22 working issues.** This is within the
"approximately 20–25 controlled issues" Phase 1 scope (`CLAUDE.md` Section 3.2). The
count is a scope description, not a quota — issues are not added to reach a round
number.

### 2.1 Taxonomy Change Log (from the prior 24-issue draft)

- **Removed `wage_complaint_process`** — it described a procedural intent ("how do I
  complain?"), not a scenario type. The underlying scenario is detected as
  `delayed_wages` / `unpaid_wages` / `unauthorized_deduction` /
  `minimum_wage_violation`; complaint steps, Labour Department routes, and grievance
  portals live in `issue_actions_portals.json`.
- **Removed `compensation_for_breach`** — it described a desired remedy, not what
  happened. Compensation/damages may later surface as a curated provision, a provision
  relevance rationale, applicability notes, or a remedy-awareness action step under a
  contractual issue.
- **Removed `non_performance`** — it overlapped `breach_of_contract` too heavily for a
  prototype-similarity Issue Detector ("failed to deliver as agreed" vs. "broke the
  agreement" would create artificial prototype overlap). `breach_of_contract` is the
  broad Phase 1 issue for failure to perform or violation of an agreed obligation.
- **Renamed `online_financial_fraud` → `other_online_financial_fraud`** — see scope
  note in Section 2.2.
- **Replaced `document_dispute`** (too vague — combined verification, digital-document
  acceptance, seizure, and retention) with two clearer issues:
  `document_acceptance_or_verification` and `document_seizure_or_retention`.
- **Did NOT add `bike_key_removal`** — the motivating bike-key example is retained as
  project context, but no issue is added until official-source legal research
  establishes a reliable non-criminal Phase 1 legal basis, an appropriate mapping, and
  distinct action guidance.

### 2.2 Scope Note — `other_online_financial_fraud` Is Not a Catch-All

It covers online financial-deception scenarios that do not primarily fit `otp_fraud`,
`phishing`, `online_impersonation`, `identity_theft`, or `unauthorized_account_access`
— conceptually fake investment platforms, advance-fee scams, fraudulent online
money-making schemes. It must **not** become "anything cyber that did not match another
issue." The Issue Detector still relies on curated prototypes and similarity
thresholds; a low-similarity scenario must take the clarification / uncertain path
(`CLAUDE.md` Section 8.2), never be force-fitted into this issue.

### 2.3 Note — `contractual_disputes` Has Only 2 Issues

Because domain-level scenario balance is the primary objective (Section 5), this domain
will carry more scenarios per issue than domains with more issues. That is acceptable
under the soft coverage guide (Section 4). It may also indicate the contractual
taxonomy could expand post-review — but only via the admission test (Section 3.1) and
the support gate (Section 3.2), never to pad the count.

## 3. Issue Support Review and Admission (Governance Gate)

The taxonomy in Section 2 is WORKING. Before any issue is **approved** for Dataset V1
labeling and KB population, it must pass both the admission test and the support gate.
No new file is created for this review yet — a candidate artifact is proposed in the
final summary; this section records the requirement.

### 3.1 Issue Admission Test (`CLAUDE.md` Section 6.8)

An issue must represent **what happened** in the user's scenario — not a desired
action, remedy, complaint procedure, or portal. Before approval, all five must hold:
1. Is this a distinct real-life scenario type?
2. Can the Issue Detector meaningfully distinguish it from sibling issues (given
   prototype-similarity matching over a small curated corpus)?
3. Does it map to meaningfully specific legal provision retrieval or applicability
   rationale?
4. Does it produce meaningfully different action guidance or portal conditions?
5. Is it inside the non-criminal Phase 1 scope?

### 3.2 Issue Support Review (`CLAUDE.md` Section 6.10)

For every issue, record: `issue_id`, `domain_id`, `scenario_definition`,
`sibling_boundary`, `candidate_official_legal_source`, `candidate_provision_support`,
`expected_action_difference`, and `status`. Status values: `working` /
`provision_research_required` / `taxonomy_supported` / `rejected` / `merged`
(`taxonomy_supported` is a review finding, not final approval — the taxonomy stays
WORKING until user sign-off).

Approval requires reasonable evidence — from official legal-source research — that the
scenario type is distinct, has a clear boundary, maps to relevant provision retrieval,
and fits Phase 1 scope. This avoids creating an issue first and hunting for a law
afterward. It does **not** require provisions to be manually verified before the
taxonomy is discussed — verification is a later, human-only step (`CLAUDE.md` Section
7.5).

## 4. Dataset V1 Coverage Plan

**Primary target: approximately 25–30 distinct scenarios per domain.** Domain-level
balance is the primary class-balance objective, because `domain` is the only supervised
target (Section 5). Approved-issue coverage is used as a **diversity checklist**, not a
balancing constraint.

| Domain | Approved issues (working) | Domain-level target rows |
|---|---|---|
| `cyber_fraud` | 6 | ~25–30 |
| `consumer_issues` | 5 | ~25–30 |
| `traffic_enforcement` | 5 | ~25–30 |
| `workplace_wage` | 4 | ~25–30 |
| `contractual_disputes` | 2 | ~25–30 |
| **Total** | **22** | **~125–150** |

- Soft per-issue planning guide: **~4–7 scenarios per approved issue**, used only to
  ensure a domain is not dominated by one easy scenario pattern. It is **not** a hard
  balancing rule; issue-level counts need not be equal (issue_id is not a supervised
  target). Domains with fewer issues (e.g. `contractual_disputes`) will exceed the
  per-issue guide — that is expected and acceptable.
- Do not manipulate counts merely to hit a fixed total. ~125–150 is where the plan
  naturally lands if per-domain coverage is met; it is not a quota.

## 5. Class Balance Strategy

- **Primary:** balance at the **domain** level (roughly even rows per domain) — this is
  what Module 1 is trained and evaluated on.
- Within a domain, spread rows across the domain's approved issues per the diversity
  checklist (Section 4), but do not force equal issue-level counts.
- `issue_id` is analysis metadata, not a training signal (Section 6), so issue-level
  imbalance does not bias the Module 1 model — it only affects how finely we can slice
  errors during analysis.

## 6. Dataset Schema and the Role of `issue_id`

**Schema: `scenario, domain, issue_id`.**

- `scenario` — raw scenario text used as the model input (20–2000 chars).
- `domain` — supervised target label for Module 1; exactly one of the 5 domain IDs.
- `issue_id` — **human-annotated analysis metadata only**; one of the approved issue
  IDs, and it must belong to the row's `domain`.

**`issue_id` is used for:** coverage analysis, error slicing, identifying which issue
types the Domain Classifier struggles with, dataset-diversity inspection, and
qualitative Module 2 sanity checking. Example: if `workplace_wage` shows poor recall,
`issue_id` lets us inspect whether errors concentrate in `delayed_wages`,
`unpaid_wages`, `unauthorized_deduction`, or `minimum_wage_violation`.

**`issue_id` is never:** a Module 1 training target, a Module 1 input feature, a hidden
feature, or a substitute for domain classification. **The Issue Detector (Module 2) is
not trained on this CSV** — its matching data is the curated prototype texts in
`issue_mappings.json` (`CLAUDE.md` Sections 6.3–6.4, 6.9). Prototype curation is a
separate task from writing these training rows, though the two must stay consistent.

## 7. Scenario Type Coverage

| Type | Target share | Description |
|---|---|---|
| Clear standard scenarios | 40% | Well-formed, unambiguous, single-issue |
| Informal / noisy Indian English | 20% | Shorter sentences, colloquial tone, English only |
| Spelling / grammar noise | 15% | Real user typing patterns — missing articles, typos, run-ons |
| Longer narrative scenarios | 15% | Multi-sentence, some irrelevant detail mixed with the real issue |
| Cross-domain boundary scenarios | 10% | Deliberately near a domain boundary, labeled with the *correct* domain (Section 9) |

### 7.1 Language Scope (English only in Phase 1)

Phase 1 officially supports **English**. In scope: Indian English, informal English,
grammar mistakes, missing articles, short user-style text, spelling mistakes, run-on
sentences — e.g. "my salary not credited yet", "shop guy not giving refund", "traffic
police took my documents", "company saying wait from 2 months".

**Out of official Phase 1 scope: code-mixed Hinglish** — e.g. "paisa nahi mila",
"salary nahi diya", "refund nahi de raha". These must **not** be included in the
official Dataset V1 coverage target, and Phase 1 must not claim Hinglish support.
Code-mixed input may be evaluated later in a separate experimental set (conceptually
`data/experimental_code_mixed_test.csv` — **not created now**).

## 8. Ambiguous Examples

A few scenarios per domain should be intentionally ambiguous — hard enough that a human
labeler had to think — for later testing of `low_confidence_warning` /
`needs_clarification` behavior. Ambiguity here is about how hard the *text* is to
classify, **while a correct single label is still recoverable from the text**. A
scenario whose correct domain is genuinely unknowable from the text is **not** an
ambiguous training example — see Section 9.

## 9. Cross-Domain Confusion Coverage

The three confusion pairs to address explicitly:
- `consumer_issues` vs `contractual_disputes` — paid service not delivered could read
  as `service_deficiency` (consumer) or `breach_of_contract` (contract), depending on
  whether there is a formal agreement.
- `cyber_fraud` vs `consumer_issues` — online-shopping fraud boundary (fake seller vs.
  legitimate seller with a defective product / misleading ad).
- `workplace_wage` vs `contractual_disputes` — freelancer/gig worker (contract) vs.
  employee (wage law), both unpaid.

For each pair, Dataset V1 includes intentionally difficult **but human-labelable**
boundary examples, labeled with the correct domain, so the confusion matrix can be read
against known hard cases.

**Hard rule:** do **not** include an example whose correct domain is genuinely
unknowable from the text. If essential context is missing, treat it as a
clarification / ambiguity **test** case — not a supervised training row — until an
explicit labeling rule is defined. The dataset must never teach the model an arbitrary
label for a scenario a human cannot resolve from the provided text.

## 10. External Dataset Adaptation Strategy

A public dataset is not usable as-is (`CLAUDE.md` Section 11):
1. Identify a dataset as potentially relevant to Phase 1 scope.
2. Extract only text plausibly relevant to our 5 domains.
3. Filter out anything out-of-scope (criminal law, unrelated categories).
4. Normalize text format (encoding, whitespace).
5. Manually annotate each kept example to *our* domain taxonomy.
6. Manually annotate each kept example to *our* issue taxonomy (`issue_id` metadata).
7. Review annotated examples for ambiguity/correctness before inclusion.

The source dataset's own labels are discarded — only scenario text may be reused, and
only after passing steps 1–7.

## 11. Controlled Synthetic Augmentation Rules

- Only to fill specific gaps the confusion matrix / error slices identify after a real
  training run — never to hit a raw sample-count target in V1.
- Every synthetic example is human-reviewed before inclusion.
- No bulk generation of near-duplicate examples.
- Each synthetic addition is traceable to the failure mode it addresses (recorded in
  `docs/evaluation_notes.md` once that file exists).
- Synthetic paraphrase families must respect the no-leakage rule (Section 13).

## 12. Annotation Governance

- **Every Dataset V1 row is human-reviewed.** Claude may draft candidate scenario text;
  Claude is **not** the final annotator.
- For each candidate row:
  1. Review whether the scenario fits Phase 1 scope.
  2. Assign the `domain` label manually.
  3. Assign `issue_id` metadata manually.
  4. Confirm the issue belongs to the assigned domain.
  5. Check whether the scenario is a near-duplicate of an existing row.
  6. Check whether the scenario is genuinely labelable from the text.
  7. Accept, revise, or reject the row.
- If a scenario does not fit an approved issue: **do not force it** into the nearest
  issue — flag it for taxonomy review (it may indicate a missing/mis-scoped issue).
- If a scenario lacks enough context to determine a domain: **do not arbitrarily assign
  a domain** for training — treat it as a clarification/ambiguity case outside the
  supervised set unless an explicit labeling rule is established.

## 13. Model-Development Evaluation Strategy

**Primary model-development evaluation: Stratified 5-Fold Cross-Validation.**

- Stratified by `domain`. Fixed random seed for reproducibility.
- Purpose: compare preprocessing choices, compare TF-IDF configurations, and inspect
  macro F1, per-class precision/recall/F1, and confusion behavior across folds.
- A 70/15/15 split is **not** the primary Dataset V1 strategy — at ~125–150 rows the
  validation/test partitions would be too small to trust.
- **No-leakage rule (permanent):** near-duplicate or intentionally paraphrased variants
  derived from the same base scenario must not be split across folds in a way that
  creates leakage. When paraphrase families exist, use `StratifiedGroupKFold` /
  explicit scenario-family IDs / another controlled grouping. Do not overengineer this
  before such families exist, but keep the rule.
- **Future/final evaluation:** an untouched holdout or a manually curated challenge set
  once dataset maturity supports it. 5-fold CV does **not** replace future unseen
  evaluation — do not claim that it does.

## 14. Evaluation Metrics

Never accuracy alone. After every meaningful training experiment, record: Accuracy;
per-class Precision, Recall, F1; **Macro-averaged F1 (primary summary metric)**; and
the full domain × domain confusion matrix, with specific attention to the three
confusion pairs (Section 9).

- No fixed numeric target (e.g. "85%") is a stopping condition by itself. Stop
  iterating when the confusion matrix is understood and remaining errors are reviewed
  as acceptable.
- Dataset changes are driven by confusion analysis, `issue_id` error slicing, coverage
  gaps, ambiguous scenarios, and known boundary cases — not by a raw count target.
  Using `issue_id` to answer "which scenario types inside `workplace_wage` are most
  often misclassified?" is **analysis only**; it does not make Module 1 an issue
  classifier.

## 15. Dataset Versioning and Evaluation Notes

- Files: `data/training_data_v1.csv`, `training_data_v2.csv`, … — **never overwritten**,
  never silently replaced. A version is superseded, not deleted, so any past run
  reproduces.
- Each evaluation record in `docs/evaluation_notes.md` contains: dataset version, model
  configuration, preprocessing configuration, TF-IDF configuration, cross-validation
  strategy, fold-level metrics or summary statistics, Macro F1, per-class findings,
  confusion-matrix findings, `issue_id` error slices where useful, identified failure
  modes, and dataset changes proposed for the next version.
- **Do not attribute every error to insufficient data.** Candidate causes to weigh
  first: overlapping domain definitions, poor scenario labeling, preprocessing loss,
  vocabulary limitations, class-boundary ambiguity, model limitations, data leakage,
  issue-coverage imbalance. Record the suspected cause before adding examples.

## 16. Explicit Non-Goals for This Plan

- Does not generate `training_data_v1.csv`.
- Does not generate scenarios.
- Does not finalize the issue taxonomy — Section 3 (support review + user sign-off) is
  a separate gate.
- Does not populate any legal KB content.
- Does not create the experimental code-mixed test file.

---

**Status: DRAFT — PENDING TAXONOMY SUPPORT REVIEW AND USER APPROVAL.** Once the Issue
Support Review clears and the user approves, the first executable steps are Phase 1A KB
skeletons and the Module 1 pipeline structure (per `PROJECT_STATE.md` implementation
order); `data/training_data_v1.csv` follows, built per Sections 4–13.
