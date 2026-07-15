# PROJECT_STATE.md
# Smart Legal Intelligence System — Current Implementation State
# Living Document — Update After Every Meaningful Implementation Batch

---

> **HOW TO USE THIS FILE**
> Before starting any work in a new session:
> 1. Read `CLAUDE.md` (architecture, rules, contracts — permanent, changes rarely)
> 2. Read this file (current state)
> 3. Inspect the actual files in the repository — do NOT trust this document blindly
> 4. Compare actual state to what this file says; if stale, correct it before proceeding
> 5. State exactly what you are about to do before writing any code

---

## PERMANENT RULE — WHAT COUNTS AS COMPLETE

**A file may only be marked COMPLETE in this document when all three are true:**
1. It **physically exists** in the current repository (verified by directly listing
   or reading it in the current session — not assumed from a prior document).
2. Its **current contents have been inspected** (read, not recalled from memory or
   from another document's description of it).
3. Its **role is consistent with `CLAUDE.md`**.

**Historical generation in another Claude session, sandbox, or environment does not
count as COMPLETE.** If a document describes work as done that cannot be found in this
repository, that work is NOT COMPLETE here — it is, at best, a historical reference
that may inform recreation.

This rule exists because a prior version of this file marked eleven documents
COMPLETE that had been produced in a different sandbox session
(`/home/claude/legal-docs/`, `/mnt/user-data/outputs/...`) and never existed in this
Windows repository. That was a governance failure. It is corrected below.

---

## SECTION 1 — CURRENT PHASE

**Overall Status:** Phase 1B — ML Service Foundation (structural implementation
complete; verified; no data, no trained model).

**Current Focus:** Governance is complete and **FROZEN** (`CLAUDE.md` Rev 4,
`TRAINING_DATA_PLAN.md`, `docs/issue_support_review.md`, and the KB schemas after the
four user-directed enhancements) — modify only on a genuine discovered contradiction.
This file remains the living state tracker per its maintenance rule. The taxonomy
remains **WORKING until explicit user sign-off**.

**Dataset V1: FROZEN (2026-07-13)** — 133 rows, accepted by user as baseline after a
targeted quality pass (17 rows rewritten: typos/informal/style/boundary; distribution
unchanged). Do not modify unless explicitly instructed.

**Current milestone: incremental KB population** — one issue at a time,
taxonomy_supported issues only, stop for user review after each. Populated so far:
`otp_fraud`, `online_impersonation`, `phishing`, `identity_theft`,
`unauthorized_account_access`, `defective_product` (6/14 — cyber_fraud's supported
issues complete; consumer_issues started; `other_online_financial_fraud` stays
provision_research_required).

**Pending human verification:** IT Act sections **43**, **66**; CPA 2019 act record
(India Code URL null) and sections **2(10)**, **35**, **84** — all
`pending_manual_verification` / `unverified`, official_text null. Portal URLs pending
confirmation: `consumer_helpline_ingram` (candidate: consumerhelpline.gov.in) and
`edaakhil` (candidate: edaakhil.nic.in) — fetch confirmation failed this session, so
both stored as null per the no-placeholder rule.

**First human verification completed (2026-07-16):** IT Act 2000 sections 66C and 66D
were manually verified by **Shreeharsha N L** against India Code (official text +
source URL added by the verifier). `verification.status = manually_verified` and
`provision_status = in_force` — the verifier's edit initially saved an invalid literal
(`verification_done`) and missed `provision_status`; at the verifier's explicit
direction in chat, Claude applied the clerical correction to the stated values (a
loader-breaking enum error; disclosed here per §7.5). The eligibility gate now
**returns** 66C/66D for all three populated issues (`provisions_available`).

**Immediate Next Task:** User reviews the `defective_product` population (and
optionally verifies IT Act 43/66, CPA 2019 sections, and the two consumer portal
URLs), then instructs the next issue (suggested next: `refund_denial` — reuses CPA
2019; likely adds section 2(47) unfair trade practice definition as a candidate).

**Git:** repo re-rooted by user at `Demo/` (parent `PROGRAMS/.git` removed). Branch
renamed to `main`; `.gitignore` extended (IDE/OS/build/model artifacts); Phase 1B
foundation re-committed as `b0f887f` (the prior `70e6049` lived in the deleted parent
repo). No remotes configured.

---

## SECTION 2 — PHYSICAL REPOSITORY STATE (verified this session)

Verified by direct directory listing of `D:\PROGRAMS\Demo` in the current session.
Git: repository initialized, no commits yet, all files untracked.

```
D:\PROGRAMS\Demo\
├── CLAUDE.md                      ← permanent architecture doc (Revision 4)
├── PROJECT_CONTEXT_HANDOFF.md     ← pre-existing — historical context transfer doc
├── PROJECT_STATE.md               ← this file — living state tracker
├── TRAINING_DATA_PLAN.md          ← dataset blueprint, DRAFT pending approval (frozen)
├── docs\
│   └── issue_support_review.md    ← Issue Support Review (22/22) — APPROVED by user; taxonomy still WORKING (frozen)
├── knowledge_base\                ← SCHEMA SKELETONS ONLY (enhanced + FROZEN), no legal content
│   ├── acts_and_sections.json     ← Legal Truth Store schema (+ keywords, citation); acts = {}
│   ├── issue_mappings.json        ← Bridge File schema (+ issue_id, taxonomy_status); issues = {}
│   └── issue_actions_portals.json ← Practical Guidance schema (+ portal_id); issue_guidance/portals = {}
└── ml-service\                    ← Phase 1B — STRUCTURAL IMPLEMENTATION, no data/model
    ├── requirements.txt           ← dependency manifest with per-package reasons
    ├── app\
    │   ├── main.py                ← FastAPI composition root; POST /analyze, GET /health
    │   ├── pipeline.py            ← orchestration only (NOT the deprecated monolith)
    │   ├── classifier.py          ← Module 1 interface + trained/mock impls + preprocess_text
    │   ├── issue_detector.py      ← Module 2 — prototype similarity, own in-memory vectorizer
    │   ├── knowledge_base_loader.py ← KB load + validation + runtime indexes (stdlib-only)
    │   ├── legal_intelligence.py  ← Module 3 — KB lookup + eligibility gate + safe state
    │   ├── response_builder.py    ← Module 4 — contract assembly only
    │   └── schemas.py             ← response contract (pydantic) + shared constants
    ├── training\
    │   └── train_domain_classifier.py ← pipeline-before-data training tool (5-fold CV)
    └── tests\
        └── test_loader.py         ← 12 loader tests (all passing)
```

**Nothing else exists in this repository.** No `backend/`, `frontend/`, `database/`,
`models/` (no `.pkl` artifacts), or `data/` (no dataset CSV). `docs/wage_law_research.md`
does not exist yet.

---

## SECTION 3 — DOCUMENT STATUS (corrected)

| Document | Status | Basis |
|---|---|---|
| `CLAUDE.md` | **COMPLETE (Revision 4)** | Physically exists in repo root; created then revised across four correction batches (Rev 2: architectural/legal-safety; Rev 3: taxonomy + dataset governance; Rev 4: cross-document consistency + governance precision — see Section 4); consistent with `PROJECT_CONTEXT_HANDOFF.md` plus the corrections; Rev 4 pending user confirmation before treated as frozen |
| `PROJECT_CONTEXT_HANDOFF.md` | **PRESENT — historical reference** | Physically exists; pre-existing; treated as the historical source of truth for architecture decisions, now superseded operationally by `CLAUDE.md` |
| `PROJECT_STATE.md` | **COMPLETE (this revision)** | This file, updated this session against verified repo contents |
| `TRAINING_DATA_PLAN.md` | **DRAFT — accepted as current blueprint draft; PENDING USER APPROVAL** | Physically exists; 22-issue taxonomy + dataset governance; the Issue Support Review it required (its Section 3) has now been performed — user sign-off of the review findings and of this plan are the remaining open gates |
| `docs/issue_support_review.md` | **COMPLETE — APPROVED BY USER (2026-07-10); FROZEN** | Physically exists; all 22 working issues reviewed against the admission test (§6.8) and support gate (§6.10); 14 taxonomy_supported / 8 provision_research_required; status terminology corrected to `taxonomy_supported` at user instruction; taxonomy itself remains WORKING until explicit user sign-off |
| `knowledge_base/` (3 JSON files) | **COMPLETE — SCHEMA SKELETONS, ENHANCED + FROZEN** | Physically exist; four user-directed enhancements applied (explicit `issue_id` per issue, explicit `portal_id` per portal, `taxonomy_status` per issue, `keywords` + `citation` per provision); re-validated as parseable JSON; still zero legal content; frozen — modify only on genuine contradiction |
| `ml-service/` (10 files) | **COMPLETE — STRUCTURAL** | Phase 1B foundation: all files compile; loader validates the real skeletons; 12/12 unit tests pass; end-to-end pipeline smoke test produces an honest safe-state response (mock classifier, Low confidence, no fabricated content). No trained model, no dataset, no BERT/RAG |
| `docs/wage_law_research.md` | **PENDING** | Does not exist (parallel legal-data workstream — does not block KB skeletons; blocks all 4 `workplace_wage` issues per the support review) |

**Historical documents referenced in `PROJECT_CONTEXT_HANDOFF.md` Part 29 that are NOT
present in this repository** (generated in a prior sandbox session, never transferred
here — do not treat as available):
`ARCHITECTURE_DOCUMENT_v3.md`, `AUDIT_REPORT_v3.md`, `MIGRATION_PLAN_v3.md`,
`FILE_RESPONSIBILITY_DOCUMENT.md`, `FILE_STRUCTURE_v3.md`, `KB_DESIGN_DOCUMENT.md`,
`FINAL_IMPLEMENTATION_ORDER.md`, `DEPENDENCY_GRAPH.md`,
`ARCHITECTURE_REVIEW_RESPONSE.md`, and the earlier prototype implementation files
(`pipeline.py`, `main.py`, old `schemas.py`, `legal_knowledge_base.json`,
`training_data.csv`, `train_model.py`, backend `app.js`, frontend components).

**Disposition:** these are not being recreated as standalone documents. Their useful
content (architecture decisions, file responsibility reasoning, dependency structure)
has been folded into `CLAUDE.md` where it affects Phase 1 implementation. They will
not be tracked as pending deliverables unless the user asks for them specifically —
recreating narrative/audit documents that don't gate implementation is not required by
`CLAUDE.md`'s conventions (Section 17).

---

## SECTION 4 — ARCHITECTURE DECISIONS RECORDED

All recorded in full in `CLAUDE.md`. Summary for state-tracking purposes:

- Domain → Issue → curated legal provision architecture (not domain → all sections).
- Five Phase 1 domains locked (Section 3 of `CLAUDE.md`).
- Three-file KB separation locked (`acts_and_sections.json`, `issue_mappings.json`,
  `issue_actions_portals.json`).
- Manual legal verification is human-only; no AI may set `manually_verified`.
- Low ML confidence → HTTP 200 + warning flags, never HTTP 422.
- Dataset development is iterative (plan → V1 → train → evaluate → improve → repeat).

### Issue Detector Vectorizer — LOCKED

**Decision:** The Issue Detector (Module 2) uses its own issue-specific TF-IDF
vectorizer, fit in memory at service startup from curated issue prototype texts in
`issue_mappings.json`. It does **not** reuse the Domain Classifier's TF-IDF vectorizer.
No `.pkl` artifact is produced for it — it is rebuilt from the KB on every startup.

**Reason:** domain classification and issue-level similarity are different
representation problems; the domain vectorizer's IDF weights are tuned for
between-domain separation and would underweight terms that matter for
within-domain issue discrimination. A separate vectorizer keeps Module 2 fully
decoupled from Module 1, so a future BERT swap for Module 1 requires no change to
Module 2, and Module 2 remains independently evaluable/replaceable.

**Constraint carried forward:** keyword matching may only support explanation
(`scenario_signals`); it must never become the primary issue-decision mechanism.

Full rationale: `CLAUDE.md` Section 6.4.

### Revision 2 Correction Batch — LOCKED (2026-07-09)

Applied to `CLAUDE.md` at the user's request as architectural precision and
legal-safety corrections, before the document is treated as frozen. None of these
reopen prior locked decisions — they sharpen them. All ten are now permanent
`CLAUDE.md` content; this is a state-tracking summary only, `CLAUDE.md` is the
authoritative text.

1. **Pending legal provisions are not citizen-facing.** `verification.status =
   pending_manual_verification` alone was previously undefined with respect to
   runtime retrieval — now explicit: a pending provision must never reach a citizen.
   (`CLAUDE.md` §7.5)
2. **Citizen-facing provision eligibility requires manual verification *plus*
   eligible provision status** — both `verification.status == manually_verified` AND
   `provision_status == in_force` are required; neither alone is sufficient. A new
   controlled `provision_status` enum (`unverified` / `in_force` / `omitted` /
   `repealed` / `amended_review_required` / `applicability_uncertain`) replaces the
   prior vague `"status": "active"` field. Only a human may set an eligible
   `provision_status`, same human-only rule as `verification.status`. (§7.4, §7.5)
3. **Issue detection is scoped to issues within the predicted domain.** Module 2 no
   longer compares the scenario against every issue across all domains — only
   against issues belonging to the domain Module 1 predicted. The issue-specific
   vectorizer itself is still fit globally across all prototypes (locked decision,
   §6.4 below); only the per-request *candidate comparison set* is domain-filtered.
   (`CLAUDE.md` §6.3)
4. **Wrong-domain routing is an accepted Phase 1 limitation and must be evaluated.**
   If Module 1 mispredicts the domain, Module 2 cannot recover into the correct
   domain's issues. Tracked via the domain confusion matrix, low-confidence handling,
   and `docs/evaluation_notes.md` failure analysis. Future mitigations (top-2 domain
   routing, joint domain/issue classification, hierarchical BERT) are named as Phase
   2+ directions only — not implemented now. (§6.5)
5. **Exact preprocessing/hyperparameters are experiment-level decisions, not
   constitutional rules.** The permanent decision is only "TF-IDF + Logistic
   Regression" for Module 1. Specific stopword handling, lemmatization,
   `ngram_range`, `max_features`, `sublinear_tf` are no longer hardcoded in
   `CLAUDE.md` — they are selected via baseline experiments after Dataset V1 exists,
   evaluated with macro F1 / per-class metrics / confusion matrix, and documented in
   `docs/evaluation_notes.md`. Negation handling is flagged as important (stopword
   removal must not strip negation terms). The one rule that stays permanent: training
   and inference preprocessing must be identical. (§5)
6. **Module 2 terminology is "Issue Detection using Prototype Similarity Matching,"
   not "Issue Classification."** Cosine similarity against curated prototypes is not
   a trained classifier and must not be described as one in technical or viva-facing
   documentation. (§6.2)
7. **Issue match reasoning and provision relevance rationale are separate concepts.**
   Layer A — `issue_match_reason` (generated at request time from Module 2's
   similarity/prototype/signal data, explains scenario→issue matching) — is distinct
   from Layer B — `provision_relevance_rationale` (human-curated in
   `issue_mappings.json`, explains issue→provision mapping, replaces the prior
   `why_relevant` naming). They must never be merged into one field or one
   generation step. (§6.7)
8. **Provision status is human-governed.** Claude may identify candidate provisions,
   flag that official-source review is needed, and draft simplified explanations —
   Claude may never independently set `provision_status = in_force` or
   `verification.status = manually_verified` as a final fact, even if asked casually.
   (§7.5, §17)
9. **Issue cosine similarity is exposed as `similarity_score`, not `confidence`.**
   `domain.confidence` (Logistic Regression `predict_proba()`) and
   `issue.similarity_score` (cosine similarity) are named differently in the response
   contract because they are generated by fundamentally different mechanisms; the
   issue score must never be called confidence/probability/certainty. Raw
   `similarity_score` may still appear in the API for debugging/evaluation/threshold
   tuning — whether it's shown to citizens in the UI is deferred as a usability
   decision, not locked as architecture. (§6.2–6.3, §8.1)
10. **Numeric confidence/clarification thresholds are configurable and
    evaluation-driven.** The High/Medium/Low/Low+warning cutoffs (0.80/0.65/0.60) are
    documented as Phase 1 provisional defaults, to be re-tuned from Dataset V1
    evaluation results rather than treated as immutable. The permanent architectural
    rule that survives any retuning: low ML confidence on valid input returns HTTP
    200 with warning/clarification fields, never HTTP 422. (§8.1, §8.2)

**Additional response-contract changes from this batch** (see `CLAUDE.md` §8.1):
`legal_information_status` field added (`"provisions_available"` /
`"no_verified_provision_available"`) so Module 3 can report an explicit safe state
when no eligible manually verified provision exists, instead of silently returning an
empty list or fabricating an answer. Terminology in §1/§2/§10 corrected — the KB is no
longer described as "pre-verified" as a whole; it is a "human-curated legal knowledge
base with citizen-facing retrieval restricted to manually verified provisions."

### Revision 3 Correction Batch — Taxonomy + Dataset Governance — LOCKED (2026-07-10)

Applied to `CLAUDE.md` and `TRAINING_DATA_PLAN.md` at the user's request. None reopen a
locked decision — they sharpen taxonomy and dataset governance. `CLAUDE.md` and
`TRAINING_DATA_PLAN.md` are the authoritative texts; this is a state-tracking summary.

**Taxonomy changes (now 22 working issues, was 24):**
- **Removed** `wage_complaint_process` (procedural intent, not a scenario type),
  `compensation_for_breach` (desired remedy, not what happened), `non_performance`
  (overlapped `breach_of_contract` too heavily for prototype similarity).
- **Renamed** `online_financial_fraud` → `other_online_financial_fraud`, with an
  explicit anti-catch-all scope note (low similarity → clarification path, not
  force-fit).
- **Replaced** `document_dispute` (too vague) with `document_acceptance_or_verification`
  and `document_seizure_or_retention`.
- **Did not add** `bike_key_removal` — deferred until official-source research supports
  a non-criminal Phase 1 basis.

**Governance additions:**
- **Issue admission test** (`CLAUDE.md` §6.8): an issue must represent *what happened*,
  not a remedy/procedure/portal; must pass a 5-point distinctness / distinguishability
  / provision-support / action-difference / scope test. Count is scope, not quota.
- **Issue-to-provision support gate** (`CLAUDE.md` §6.10, `TRAINING_DATA_PLAN.md` §3):
  before an issue is approved for labeling/KB population, an Issue Support Review must
  show credible provision support (records `issue_id`, `domain_id`,
  `scenario_definition`, `sibling_boundary`, `candidate_official_legal_source`,
  `candidate_provision_support`, `expected_action_difference`, `status`). No review
  file created this batch — a candidate artifact is proposed in the summary.
- **`issue_id` role** (`CLAUDE.md` §5, §6.9, §11.1): dataset schema is
  `scenario, domain, issue_id`; `domain` is Module 1's only supervised target;
  `issue_id` is human-annotated analysis metadata (coverage/error-slicing), never a
  Module 1 target/feature and never Module 2 training data. Module 2 is not a trained
  classifier — it performs prototype similarity matching against the curated prototypes
  in `issue_mappings.json`.
- **Language scope** (`CLAUDE.md` §11.2): Phase 1 is English (incl. Indian/noisy
  English); Hinglish/code-mixed is out of official Phase 1 scope (deferred to a future
  experimental set, not created now).
- **Evaluation strategy** (`CLAUDE.md` §11.3, `TRAINING_DATA_PLAN.md` §13): Stratified
  5-Fold Cross-Validation (by `domain`, fixed seed) replaces 70/15/15 as the primary
  Dataset V1 model-development strategy; permanent no-leakage rule for paraphrase
  families; future untouched holdout / challenge set still required (CV does not
  replace it).
- **Coverage rule** (`TRAINING_DATA_PLAN.md` §4): ~25–30 scenarios per domain is the
  primary target; issue coverage is a diversity checklist (~4–7 per issue soft guide,
  not a balancing rule); ~125–150 total is a natural landing point, not a quota.
- **Cross-domain confusion** (`TRAINING_DATA_PLAN.md` §9): boundary examples must be
  human-labelable; scenarios genuinely unresolvable from text become clarification test
  cases, never arbitrarily-labeled training rows.

### Revision 4 Correction Batch — Cross-Document Consistency and Governance Precision — LOCKED (2026-07-10)

A consistency and precision pass — **not a redesign**; no architectural, legal-safety,
taxonomy, or dataset-governance decision from Revision 2/3 was reopened or changed.
`CLAUDE.md` is the authoritative text; this is a state-tracking summary.

1. **Human-verification source wording aligned with the approved source hierarchy**
   (`CLAUDE.md` §7.5): the human-only verification gate previously said "checked against
   the official India Code publication," which was narrower than the approved-source
   rule (§7.6: India Code *or* official central-government ministry / regulator /
   statutory-authority publications). §7.5 now references "an approved official source
   under Section 7.6." The human-only gate is unchanged and not weakened; sources are
   not broadened beyond §7.6; citizen-facing eligibility still requires
   `manually_verified` **and** `in_force`.
2. **Taxonomy/dataset lifecycle reordered** (`CLAUDE.md` §11): the old "lock issue
   taxonomy → confirm provision support" ordering was corrected to "draft WORKING
   taxonomy → admission test + Issue Support Review → revise/merge/reject → user
   sign-off → approve plan → Dataset V1 → train → evaluate (5-fold CV) → inspect
   confusion + issue_id slices → improve → retrain." The taxonomy is locked by sign-off
   *after* review, not before. Added an explicit statement that Issue Support Review
   (does this issue look legally supportable enough to exist?) and Manual Provision
   Verification (has a human checked this exact Act/section/source/status against an
   approved source?) are separate stages and must never be merged.
3. **Module 2 terminology corrected in this file** (§4 Revision 3 record): the phrase
   "Module 2 remains trained only on curated prototypes" was technically inaccurate —
   Module 2 is not a trained classifier. Corrected to "Module 2 is not a trained
   classifier — it performs prototype similarity matching against curated prototypes in
   `issue_mappings.json`." (`CLAUDE.md` and `TRAINING_DATA_PLAN.md` already used accurate
   wording; only this file's historical-summary line needed the fix.)
4. **Implementation gates clarified as step-specific** (this file, §8): replaced the
   overbroad "no implementation proceeds until these gates clear" with a rule that each
   gate blocks only the steps it governs, plus an explicit mapping (Issue Support Review
   + sign-off / plan approval / wage-law research / absence of verified provisions →
   what each does and does not block). This is not permission to start implementation;
   the stop-and-approve workflow and Section 10 order still govern.
5. **Future Module 2 score-contract safety rule** (`CLAUDE.md` §12): if a future phase
   replaces prototype similarity matching with a *trained* issue model, the Module 2
   score field, semantics, and API contract must be explicitly reviewed and versioned;
   Phase 1 `issue.similarity_score` must not be silently reused to mean classifier
   confidence/probability. Does not change the Phase 1 field, contract, or Issue
   Detector architecture.

`TRAINING_DATA_PLAN.md` required **no** modification this batch — it already used
accurate Module 2 wording, the correct lifecycle ordering, and CLAUDE.md cross-references
that remain valid (no section renumbering occurred). It was left unchanged rather than
touched cosmetically.

---

## SECTION 5 — DATASET STATUS

| Item | Status |
|---|---|
| `TRAINING_DATA_PLAN.md` | DRAFT — pending Issue Support Review + user approval (Section 8) |
| `ml-service/data/training_data_v1.csv` | **DRAFT CREATED (2026-07-13)** — 133 rows (28 cyber / 27 consumer / 26 traffic / 26 wage / 26 contractual), schema `scenario,domain,issue_id`, all 22 issues covered, quality-reviewed (no duplicates/near-duplicates, labels valid, lengths in bounds, accepted by the training script's validator). All rows are Claude-drafted candidates — **pending human annotation review (user is the final annotator, TRAINING_DATA_PLAN §12)** |
| `data/training_data_v2.csv`+ | **PENDING** — blocked on V1 evaluation |
| Issue taxonomy | **WORKING — 22 issues** (6 cyber / 5 consumer / 5 traffic / 4 wage / 2 contractual) — `TRAINING_DATA_PLAN.md` §2. Issue Support Review **approved by user** (`docs/issue_support_review.md`: 14 taxonomy_supported / 8 provision_research_required); taxonomy stays WORKING pending explicit user sign-off |
| Training pipeline (`train_domain_classifier.py`) | **COMPLETE — STRUCTURAL** — exists, runnable on any valid CSV (pipeline-before-data); refuses politely when the CSV is absent; Stratified 5-Fold CV; imports the same `preprocess_text` inference uses |
| Trained models (`.pkl` files) | **PENDING** — do not exist (blocked on Dataset V1) |

**Locked Dataset V1 decisions** (authoritative text in `CLAUDE.md` §11 and
`TRAINING_DATA_PLAN.md`):
- Schema `scenario, domain, issue_id`; `domain` is the Module 1 supervised target;
  `issue_id` is analysis metadata only; issue prototypes remain separate in
  `issue_mappings.json` (Module 2 not trained on the CSV).
- ~25–30 scenarios per domain (primary target); issue coverage is a diversity
  checklist; ~125–150 total is a natural landing point, not a quota.
- Indian/noisy English in scope; formal Hinglish out of Phase 1.
- Stratified 5-Fold Cross-Validation (by `domain`) is the primary model-development
  evaluation strategy; no fixed numeric accuracy stopping rule.

No dataset CSV, real or synthetic, has been generated in this repository.

---

## SECTION 6 — KNOWLEDGE BASE STATE

| File | Status |
|---|---|
| `knowledge_base/acts_and_sections.json` | **POPULATING** — `it_act_2000` with sections `66c`, `66d` (both `pending_manual_verification` + `unverified`; official_text/URL null awaiting human verification against India Code) |
| `knowledge_base/issue_mappings.json` | **POPULATING** — `otp_fraud` (4 prototypes, 2 provision references with Layer-B rationales) |
| `knowledge_base/issue_actions_portals.json` | **POPULATING** — `otp_fraud` guidance (5 steps) + portals `cybercrime_gov_in` (immediate, URL confirmed), `rbi_cms` (secondary, conditional, URL confirmed) |

**Populated: 1 of 14 taxonomy_supported issues (`otp_fraud`).** Zero provisions
manually verified; the eligibility gate is verified to return the safe state. Rules in
force: one issue at a time; never a whole domain at once; `provision_research_required`
issues (8) blocked until instructed; wage-law research still gates all
`workplace_wage` provisions (see Section 9).

---

## SECTION 7 — APPLICATION CODE STATE

**ML service (Phase 1B): STRUCTURALLY COMPLETE, verified this session.**
- All four modules exist as separate files with stable interfaces (Module 1
  `classifier.py`, Module 2 `issue_detector.py`, Module 3 `legal_intelligence.py`,
  Module 4 `response_builder.py`), wired by `pipeline.py` (orchestration only) behind
  `main.py` (POST /analyze, GET /health), with the response contract in `schemas.py`
  and startup validation in `knowledge_base_loader.py`.
- Verified: all files compile; loader self-check passes on the real frozen skeletons;
  12/12 unit tests pass (`tests/test_loader.py`); end-to-end smoke test on the empty
  KB returns the honest safe state (mock Low confidence → clarification →
  `no_verified_provision_available` → disclaimer). Dependencies for full service
  runtime (fastapi/uvicorn/scikit-learn/joblib/numpy) are listed in
  `requirements.txt` but not all installed locally yet (pytest + pydantic installed
  for verification).
- The classifier runs in **mock mode** (clearly labeled, always Low confidence) until
  a model is trained; the issue detector runs in **no_prototypes mode** until the KB
  is populated. Both modes are surfaced by GET /health.

Node.js backend, React frontend, database schema: **all PENDING** — later phases.

---

## SECTION 8 — OPEN APPROVAL GATES

| Gate | Status |
|---|---|
| `CLAUDE.md` architecture direction | Confirmed by user (Revision 1) |
| `CLAUDE.md` Revision 2 (architectural/legal-safety) | Applied; user acknowledged direction and requested Revision 3 |
| `CLAUDE.md` Revision 3 (taxonomy + dataset governance) | Applied; user reviewed and requested Revision 4 consistency corrections |
| `CLAUDE.md` Revision 4 (cross-document consistency + governance precision) approved / frozen | Awaiting user confirmation (this batch) |
| Issue Support Review for the 22 working issues | **APPROVED by user (2026-07-10)** with terminology change `approved` → `taxonomy_supported`; document frozen |
| Issue taxonomy formally signed off | **Still open** — taxonomy remains WORKING until explicit user sign-off; blocks KB *population* and Dataset V1 labeling, not schema skeletons |
| Governance freeze | **In effect** — `CLAUDE.md`, `TRAINING_DATA_PLAN.md`, `docs/issue_support_review.md`, and the KB schemas (post-enhancement) frozen; modify only on a genuine discovered contradiction |
| Phase 1A KB schemas | **Done** — enhanced per user instruction (issue_id, portal_id, taxonomy_status, keywords+citation), then frozen |
| Phase 1B ML service structure → Dataset V1 / training | ML structure complete — **awaiting user approval before any Dataset V1 or training work** |
| Research queue from the review (wage-law, bribe_demand, wrongful_challan, other_online_financial_fraud, security_deposit_dispute) | Open — blocks KB population / Dataset V1 labeling for the 8 provision_research_required issues only |
| `TRAINING_DATA_PLAN.md` approved | DRAFT accepted as current blueprint draft — awaiting user approval |
| `docs/wage_law_research.md` written | Not started (parallel workstream; does not block KB skeletons) |

**Gates are step-specific, not globally blocking.** Implementation proceeds only when
the specific approval gate and blueprint relevant to *that* step have cleared — an open
gate blocks the steps it governs, not every step. Current gate relationships:

- **Issue Support Review + taxonomy sign-off** block: issue-level KB population, Dataset
  V1 `issue_id` labeling against the approved taxonomy, final issue-prototype curation,
  and issue-specific action/portal mapping.
- **`TRAINING_DATA_PLAN.md` approval** blocks: creation of `training_data_v1.csv`.
- **Wage-law research** blocks: `workplace_wage` legal-provision population only. It does
  **not** block empty KB skeleton creation, the modular Domain Classifier pipeline
  structure, or Dataset V1 planning.
- **Absence of manually verified provisions** blocks: citizen-facing provision retrieval
  and meaningful end-to-end Legal Intelligence Engine output using those provisions. It
  does **not** inherently block structural Legal Intelligence Engine code, schema
  definitions, or unit tests using clearly-marked fixtures/mocks.

This is not permission to begin implementation now. The **current approved
implementation order (Section 10)** and the user's stop-and-approve workflow govern
sequencing; the immediate next task remains the Issue Support Review (Section 12).

---

## SECTION 9 — BLOCKERS

| Blocker | Blocks | Resolution |
|---|---|---|
| Taxonomy not yet signed off (review approved; sign-off still explicit and separate) | Taxonomy finalization; issue-level KB population; Dataset V1 labeling | User gives explicit taxonomy sign-off |
| 8 issues at `provision_research_required` | KB population + Dataset V1 labeling finalization **for those 8 issues only** (all 4 wage issues, `bribe_demand`, `wrongful_challan`, `other_online_financial_fraud`, `security_deposit_dispute`) | Targeted official-source research per the review's research queue (§7.3) |
| `TRAINING_DATA_PLAN.md` not yet approved | `data/training_data_v1.csv` | User approves after the support review |
| `docs/wage_law_research.md` not written | **`workplace_wage` legal-provision population only** (a parallel legal-data workstream) — does **not** block empty KB skeletons, the Module 1 pipeline structure, or Dataset V1 planning | Write before workplace/wage provision population, using only official Government of India sources |
| ~~No KB structures exist~~ **RESOLVED (2026-07-10)** | ~~Meaningful Legal Intelligence Engine integration against the real project KB~~ | Three KB skeleton structures created (`knowledge_base/`); structures exist, content does not |
| No manually verified legal provisions exist | Citizen-facing legal provision retrieval; meaningful end-to-end legal provision output using real legal provisions | Controlled legal provision population + human verification against approved official sources (Section 7.6 of `CLAUDE.md`) |
| No trained model exists | `domain_classifier.py` runtime use | Resolved when Dataset V1 is trained |

Structural code, schema definitions, and unit tests using clearly marked fixtures or
mocks are **not** inherently blocked by the absence of manually verified provisions
(see Section 8). The approved implementation order (Section 10) still governs
sequencing.

---

## SECTION 10 — CORRECTED IMPLEMENTATION ORDER

```
1.  Governance foundation — state recovery                        ← COMPLETE
2.  Dataset blueprint and issue taxonomy                          ← CURRENT (draft done, pending review/approval)
3.  Issue Support Review and taxonomy sign-off                    ← REVIEW APPROVED; TAXONOMY SIGN-OFF STILL PENDING
4.  Create the three legal KB skeleton structures only            ← DONE (schemas only, enhanced + frozen, 2026-07-10)
5.  Build the modular ML pipeline structure (code; no trained model required yet)  ← DONE (2026-07-10, verified)
6.  Create small Dataset V1
7.  Train and evaluate using Stratified 5-Fold Cross-Validation
8.  Inspect confusion matrix and issue_id error slices
9.  Improve Dataset V1 and retrain
10. Controlled legal provision population + human verification (parallel legal-data
    workstream; verification.status and eligible provision_status stay human-only)
11. Build Legal Intelligence Engine and Response Builder against the structured KB
12. Stabilize ML/API response contract
13. Build Node.js integration
14. Build frontend result flow
15. End-to-end testing
```

**Parallel legal-data requirement:** wage-law research → **before** workplace/wage KB
provision population (Step 10, wage subset only). Wage-law research is **not** a blocker
for empty KB skeleton creation (Step 4), the Domain Classifier pipeline structure
(Step 5), or Dataset V1 planning (Step 2). Do not bulk-populate 20–30 legal provisions
in one step (Step 10) — population is incremental and each provision starts
`pending_manual_verification` / `provision_status = unverified`.

---

## SECTION 11 — LAST COMPLETED TASK

**Most recent (batch 10 — dataset quality pass + freeze; KB population begins,
2026-07-13):** Rewrote 17 of 133 dataset rows in place (realistic typos: salry, accont,
instgram, whatsap, recived, reciept, cleand, becoz; fragmented/complaint/conversational
styles; more informal Indian English; 2 boundary rewrites — Instagram-seller
non-delivery kept `cyber_fraud`, advance-paid salon package kept `consumer_issues`).
Row count, schema, domain counts, and issue distribution unchanged; all validations
re-passed (no dupes/near-dupes, 22 issues, training-script validator OK). **Dataset V1
frozen.** Populated first KB issue `otp_fraud`: IT Act 2000 act record + sections
66c/66d (official_text and India Code URL left null — India Code blocks automated
fetch (HTTP 403), so URLs are unconfirmed per the null-not-placeholder rule;
candidate URLs handed to user for human verification), simplified explanations,
applicability notes, keywords, citations, 4 prototype texts, 2 Layer-B rationales,
5 action steps, 2 portals (cybercrime.gov.in confirmed official via fetch — MHA/I4C;
cms.rbi.org.in confirmed official — RBI, conditional usage). All provisions
`pending_manual_verification` + `unverified`. Verified: loader validation + reference
integrity pass; 12/12 tests (one test updated — it had hardcoded the KB being empty);
engine gate check confirms 0 provisions returned and explicit safe state while
unverified, with action steps and portals served.

**Batch 9 (Dataset V1 draft, 2026-07-13):** generated
`ml-service/data/training_data_v1.csv` — 133 scenarios (28/27/26/26/26 per domain),
locked schema `scenario,domain,issue_id` (issue_id = analysis metadata per CLAUDE.md
11.1; user asked for two columns but the frozen schema and the training script's
validator require three — noted as an assumption). Scenario mix per TRAINING_DATA_PLAN
§7: standard / informal-noisy Indian English / narrative / cross-domain boundary rows
(freelancer-vs-employee, online-fraud-vs-consumer, consumer-vs-contract), English only,
no Hinglish. Quality review passed: no exact or near duplicates (token-Jaccard check),
all labels valid and domain-consistent, all 22 issues covered, lengths 20–2000,
accepted by `load_dataset()`. Status: DRAFT pending human annotation review — Claude
drafted, user is the final annotator. issue_id values for the 8
provision_research_required issues are provisional metadata (does not affect Module 1
training). No training performed; no model artifacts exist.

**Batch 8 (Git re-configuration + Phase 1B implementation review):**
Git: repo now rooted at `Demo/`, branch `main`, improved `.gitignore`, foundation
committed as `b0f887f`, tree clean, no remotes. Code review of all 10 Phase 1B files —
quality fixes only, no new functionality, no contract changes: single-sourced the
approved-domain set in `knowledge_base_loader` (classifier + schemas now import it,
with an import-time display-name consistency guard); removed duplicate
`LEGAL_INFO_*` constants from `schemas.py` (owner: `legal_intelligence`); Module 3 now
imports `MAX_ACTION_STEPS` from the loader; classifier factory returns the classifier
only (mode read from the instance); issue_detector hoisted the cosine-similarity
import to startup and cleaned style; training script now exits cleanly when a domain
has <2 rows instead of crashing in StratifiedKFold. `response_builder.py`,
`pipeline.py`, `tests/test_loader.py` already satisfactory — unchanged. Re-verified:
compile OK, loader self-check OK, 12/12 tests pass, pipeline smoke test OK (mock mode,
safe state). Review changes are uncommitted, pending user approval.

**Batch 7 (KB schema enhancements + Phase 1B ML Service Foundation):**
applied the four user-directed schema enhancements (explicit `issue_id` per issue,
explicit `portal_id` per portal, `taxonomy_status` enum per issue, `keywords` +
`citation` per provision record), re-validated, and froze the schemas. Built the
Phase 1B structural implementation: `ml-service/app/` (main, pipeline, classifier,
issue_detector, knowledge_base_loader, legal_intelligence, response_builder, schemas),
`ml-service/training/train_domain_classifier.py`, `ml-service/tests/test_loader.py`,
plus `requirements.txt`. Dependency injection throughout; four-module separation
preserved; eligibility gate implemented in Module 3; Module 2 fits its own in-memory
vectorizer from prototype_texts only; mock classifier is honest (always Low
confidence). Verified: loader self-check on real skeletons, 12/12 tests pass,
end-to-end smoke test returns the safe state. **No Dataset V1, no trained model, no
BERT, no RAG, no legal provisions, no frontend, no backend gateway, no database.**

**Batch 6 (review approval + governance freeze + Phase 1A KB schemas):**
user approved the Issue Support Review with one terminology change — status value
`approved` renamed to `taxonomy_supported` throughout `docs/issue_support_review.md`,
with the enum definitions in `CLAUDE.md` §6.10 and `TRAINING_DATA_PLAN.md` §3.2 synced
(authorized contradiction fix); governance documents frozen. Created the Phase 1A KB
structural foundation: `knowledge_base/` with `acts_and_sections.json`,
`issue_mappings.json`, `issue_actions_portals.json` — complete `_meta` + `_schema`
contracts, empty data containers, validated JSON. **No legal provisions populated; no
verification status set; no Dataset V1; no model training; no BERT/RAG; no wage
provisions.** Taxonomy remains WORKING pending explicit user sign-off.

**Batch 5 (Issue Support Review):** corrected the Section 9 blocker model
(separated "no KB structures exist" from "no manually verified provisions exist," with
their distinct blocks/resolutions; structural code/schemas/fixture-based tests not
inherently blocked); created `docs/issue_support_review.md` and performed the Issue
Support Review for all 22 working issues against the admission test (`CLAUDE.md` §6.8)
and support gate (§6.10). Outcome: **14 taxonomy_supported (labeled "approved" at the
time; renamed in batch 6), 8 provision_research_required, 0 rejected/merged**. Key findings: `bribe_demand` has weak in-scope provision support
(PCA is banned — conditional reframe/reject recommendation recorded); all 4 wage issues
gated on the pending wage-law research; `other_online_financial_fraud` assessed as
controlled (not a catch-all) with an explicit guardrail; no `bike_key_removal` issue
added (no official-source support found); two weak sibling boundaries flagged
(`misleading_advertisement`/`unfair_trade_practice`, `delayed_wages`/`unpaid_wages`)
with designated merge fallbacks recorded, not applied. No taxonomy change applied; no
verification statuses set; no KB/dataset/ML/backend/frontend files created.

**Batch 4 (Revision 4, cross-document consistency + governance
precision):** aligned the human-verification source wording with the approved source
hierarchy (`CLAUDE.md` §7.5); reordered the taxonomy/dataset lifecycle so the Issue
Support Review precedes taxonomy sign-off and Dataset V1, and separated Issue Support
Review from Manual Provision Verification (§11); added the future Module 2
score-contract safety rule (§12); bumped the revision label to Revision 4; corrected the
inaccurate "Module 2 remains trained" phrase in this file's Revision 3 summary; and
replaced the overbroad implementation-gate wording with step-specific gates (§8).
`TRAINING_DATA_PLAN.md` needed no change. No code, KB, dataset CSV, wage-research, or
review-artifact files created.

**Batch 3 (Revision 3 — taxonomy + dataset governance):** applied the Revision 3
correction batch to `CLAUDE.md` (issue admission test §6.8, Module 2 not-trained note
§6.9, issue-to-provision support gate §6.10, `issue_id` role §5/§11.1, English-only
language scope §11.2, 5-fold CV + coverage strategy §11.3, quick-reference conventions
§17, count → 22 in §3.2); rewrote `TRAINING_DATA_PLAN.md` to the 22-issue taxonomy with
the taxonomy change log, admission test, support gate, revised coverage plan, `issue_id`
schema, English-only language scope, 5-fold CV strategy, and updated confusion/
annotation/versioning governance; recorded the batch here (Section 4). No code, KB,
dataset CSV, wage-research, or review-artifact files created.

**Prior session (batch 2):** ten architectural-precision/legal-safety corrections to
`CLAUDE.md` (Revision 2 — citizen-facing eligibility gate, domain-scoped issue
detection, unlocked hyperparameters, Module 2 terminology, two-layer reasoning,
human-governed `provision_status`, `similarity_score` naming, configurable thresholds).

**Prior session (batch 1):** repository audit; created `CLAUDE.md` and
`TRAINING_DATA_PLAN.md`; rewrote this file against verified repo contents; locked the
Issue Detector vectorizer decision; added the permanent COMPLETE-status rule.

---

## SECTION 12 — EXACT NEXT PENDING TASK

**Next task: user reviews the Phase 1B ML service structure and approves the next
step.** Per the approved implementation order, the natural next steps after approval
are (in whichever order the user gates them):
- **Dataset V1 creation** (Step 6) — requires explicit taxonomy sign-off AND
  `TRAINING_DATA_PLAN.md` approval first.
- **Training + evaluation** (Step 7) — requires Dataset V1.
- **Parallel legal-data workstream** — wage-law research (`docs/wage_law_research.md`),
  then controlled provision population + human verification for signed-off issues.

Still-open gates:
1. **Explicit taxonomy sign-off** — taxonomy remains WORKING; blocks KB population and
   Dataset V1 labeling. Sign-off should also decide the `bribe_demand` path and
   acknowledge the two evaluation-gated merge fallbacks.
2. **`TRAINING_DATA_PLAN.md` approval** — blocks `training_data_v1.csv`.
3. **Research queue** (review §7.3) — blocks KB population for the 8
   `provision_research_required` issues; wage-law research (parallel workstream) blocks
   all `workplace_wage` provisions.

No KB content, dataset CSV, or model training until the relevant gates clear.

---

## SECTION 13 — UPDATE LOG

| Date | Update Description | Updated By |
|---|---|---|
| 2025-07-08 | Initial `PROJECT_STATE.md` created at context handoff point (later found to contain unverified COMPLETE claims for files not in this repo) | Claude (auto) |
| 2026-07-09 | Repository audit; corrected all COMPLETE claims against verified physical repo state; created `CLAUDE.md` and `TRAINING_DATA_PLAN.md`; added permanent COMPLETE-status rule; locked Issue Detector vectorizer decision | Claude |
| 2026-07-09 | Correction batch (Revision 2): applied 10 architectural-precision/legal-safety corrections to `CLAUDE.md` (citizen-facing provision eligibility, domain-scoped issue detection, unlocked preprocessing hyperparameters, Module 2 terminology, two-layer relevance reasoning, human-governed `provision_status`, `similarity_score` naming, configurable thresholds); recorded batch here; no code/KB/dataset/wage-research changes made | Claude |
| 2026-07-10 | Correction batch (Revision 3 — taxonomy + dataset governance): taxonomy cut to 22 working issues (removed `wage_complaint_process` / `compensation_for_breach` / `non_performance`; renamed `online_financial_fraud` → `other_online_financial_fraud`; split `document_dispute` into acceptance/verification + seizure/retention); added issue admission test, issue-to-provision support gate, `issue_id`-as-metadata rule, English-only language scope, Stratified 5-Fold CV strategy; updated `CLAUDE.md` and `TRAINING_DATA_PLAN.md`; recorded batch here; no code/KB/dataset/wage-research/review-artifact files created | Claude |
| 2026-07-10 | Correction batch (Revision 4 — cross-document consistency + governance precision): aligned §7.5 verification source with the §7.6 approved-source hierarchy; reordered the §11 taxonomy/dataset lifecycle (support review before sign-off) and separated Issue Support Review from Manual Provision Verification; added the future Module 2 score-contract safety rule (§12); fixed the inaccurate "Module 2 remains trained" phrase in this file; made implementation gates step-specific (§8); bumped label to Revision 4. `TRAINING_DATA_PLAN.md` unchanged (already accurate). No code/KB/dataset/wage-research/review-artifact files created | Claude |
| 2026-07-10 | Batch 5 — blocker-model split (KB structures vs verified provisions) in §9; performed the Issue Support Review for all 22 working issues and created `docs/issue_support_review.md` (14 taxonomy_supported [originally labeled "approved"], 8 provision_research_required, 0 rejected/merged; conditional bribe_demand recommendation; wage issues gated on wage-law research; no bike_key_removal added; merge fallbacks recorded for misleading_ad/UTP and delayed/unpaid wages). Taxonomy unchanged, still WORKING pending user sign-off. No verification statuses set; no KB/dataset/ML/backend/frontend files created | Claude |
| 2026-07-10 | Batch 6 — user approved the Issue Support Review with status rename `approved` → `taxonomy_supported` (applied in the review; enum synced in `CLAUDE.md` §6.10 + `TRAINING_DATA_PLAN.md` §3.2 as an authorized contradiction fix); governance documents frozen. Phase 1A: created `knowledge_base/` with the three schema-only JSON files (validated; empty data containers; zero legal content; no verification statuses; no Dataset V1; no training; no BERT/RAG; no wage provisions) | Claude |
| 2026-07-10 | Batch 7 — four user-directed KB schema enhancements (issue_id, portal_id, taxonomy_status, keywords+citation) applied and schemas frozen. Phase 1B ML Service Foundation created: 8 app modules + training script + loader tests + requirements.txt. Verified: all compile, loader self-check on real skeletons passes, 12/12 tests pass, end-to-end smoke test returns honest safe state (mock classifier, Low confidence, no fabricated legal content). No Dataset V1 / trained model / BERT / RAG / provisions / frontend / backend / DB | Claude |
| 2026-07-12 | Batch 8 — Git re-configured (root = Demo, branch main, .gitignore extended, foundation re-committed as b0f887f after user removed parent repo; no remotes). Phase 1B implementation review: de-duplicated domain-set / status-constant / action-step-limit definitions, simplified classifier factory, cleaned issue_detector style, fixed training-script crash on <2-row domains. No new functionality; contracts unchanged. All verification re-passed (12/12 tests, smoke OK). Review changes uncommitted pending approval | Claude |
| 2026-07-13 | Batch 9 — Dataset V1 draft generated per user order: 133 rows across 5 domains (28/27/26/26/26), schema scenario,domain,issue_id, all 22 issues covered, quality review passed (no dupes/near-dupes, valid labels, training-script validator OK). DRAFT — pending human annotation review; no training run; no model artifacts | Claude |
| 2026-07-13 | Batch 10 — targeted dataset quality pass (17/133 rows: typos, style variation, informal Indian English, 2 boundary rewrites; counts/schema/distribution unchanged; all validations re-passed) → **Dataset V1 FROZEN**. KB population started: `otp_fraud` populated (IT Act 66C/66D pending verification, official_text/URL null per source rules; portals cybercrime.gov.in + rbi_cms confirmed official). Loader + 12/12 tests + eligibility-gate check pass. KB state: 1 act, 2 sections, 1 issue, 2 portals | Claude |
| 2026-07-14 | Batch 11 — populated `online_impersonation` (2/14): reused existing IT Act 66D (primary) + 66C references with new Layer-B rationales, 4 prototypes, 5 action steps, new portal `sanchar_saathi_chakshu` (DoT — fetch-confirmed official; conditional on call/SMS/WhatsApp impersonation); extended cybercrime_gov_in supported_issue_ids. No new act/section needed; previously completed issue untouched; verification fields untouched. Loader + 12/12 tests + gate check pass. KB state: 1 act, 2 sections, 2 issues, 3 portals | Claude |
| 2026-07-16 | Batch 15 — populated `defective_product` (6/14; consumer domain opened): new act `cpa_2019` (India Code URL null pending confirmation) with candidate sections 2(10) defect definition, 35 complaint filing, 84 product liability — all pending/unverified with null official_text; 4 prototypes, 3 Layer-B rationales, 5 action steps (evidence preservation first), 2 new portals `consumer_helpline_ingram` (primary) + `edaakhil` (secondary, conditional) with null URLs (fetch confirmation unavailable this session; candidates recorded for verifier). Gate withholds unverified CPA sections (safe state); 5 prior issues regression-checked; loader + 12/12 tests pass. KB state: 2 acts, 7 sections (2 verified), 6 issues, 7 portals | Claude |
| 2026-07-16 | Batch 14 — populated `unauthorized_account_access` (5/14; cyber_fraud supported issues complete): added new IT Act candidate sections 43 (compensation for unauthorized access — primary) and 66 (computer-related offences), both `pending_manual_verification`/`unverified` with null official_text awaiting human verification; 4 prototypes, 5 action steps (recovery+2FA first), reused cybercrime_gov_in. Gate correctly withholds unverified 43/66 (safe state) while still serving verified 66C/66D for prior issues; loader + 12/12 tests pass. KB state: 1 act, 4 sections (2 verified, 2 pending), 5 issues, 5 portals | Claude |
| 2026-07-16 | Batch 13 — populated `identity_theft` (4/14): reused verified IT Act 66C (single reference, per support review), 4 prototypes, 5 action steps, 2 new portals — `sanchar_saathi_tafcop` (DoT; SIMs in your name; parent portal fetch-confirmed) and `uidai` (fetch-confirmed official; Aadhaar biometric lock/grievance; conditional); extended cybercrime_gov_in. No new act/section needed. Gate returns 66C (`provisions_available`); portal sort immediate→primary→secondary verified; prior 3 issues regression-checked. Loader + 12/12 tests pass. KB state: 1 act, 2 sections, 4 issues, 5 portals | Claude |
| 2026-07-16 | Batch 12 — populated `phishing` (3/14): reused 66C (primary) + 66D, 4 prototypes, 5 action steps, extended cybercrime_gov_in + sanchar_saathi_chakshu (usage condition generalized to fraud communications). Human verification recorded: 66C/66D manually verified by Shreeharsha N L against India Code (official text + PDF URL added by verifier); Claude applied a disclosed clerical fix of the verifier's invalid enum literal (`verification_done` → `manually_verified`) and missing `provision_status = in_force` at the verifier's explicit direction — loader was rejecting the KB. Gate now returns both provisions for all 3 issues. Loader + 12/12 tests pass. KB state: 1 act, 2 sections (both in_force/verified), 3 issues, 3 portals | Claude |

---

**MAINTENANCE RULE:** Update this file after every meaningful implementation batch
(~3-5 related files, or one full component). Every status in this file must be
traceable to a file that was actually inspected in the session that set that status —
see the Permanent Rule at the top of this document.
