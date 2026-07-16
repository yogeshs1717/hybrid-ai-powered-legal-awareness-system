# CLAUDE.md
# Smart Legal Intelligence System for Indian Law Awareness using NLP
# Permanent Project Constitution — Architecture, Scope, and Rules

---

> **STATUS:** Locked (Revision 4 — Cross-Document Consistency and Governance Precision,
> applied on top of Revision 3's taxonomy + dataset governance and Revision 2's
> architectural/legal-safety corrections; see `PROJECT_STATE.md` for the correction
> record). Revision 4 is a consistency and precision correction, **not** a redesign —
> no architectural decision changed. This file is the permanent source of truth for
> architecture, scope, and rules. Decisions recorded here are final unless the user
> explicitly reopens them. Do not revive anything listed under "Rejected / Deprecated."
>
> **READ ORDER FOR ANY NEW SESSION:** This file → `PROJECT_STATE.md` → inspect the
> actual repository files. Never trust a status claim in `PROJECT_STATE.md` without
> verifying the file physically exists and has been read.

---

## 1. Project Identity

**Title:** Smart Legal Intelligence System for Indian Law Awareness using NLP

**Domain:** Legal Tech / Civic Technology — India

**Users:** Indian citizens facing common legal situations (cyber fraud, consumer
disputes, traffic enforcement issues, wage problems, contractual disputes) who lack
awareness of applicable laws and practical next steps.

**Problem solved:** Citizens have no accessible way to learn which laws apply to a
real-life situation or what to do about it. Generic LLM tools generate legal-sounding
answers with no auditable source and no guarantee of correctness. This system instead
classifies the scenario and retrieves legal information from a **human-curated legal
knowledge base with citizen-facing retrieval restricted to manually verified
provisions** — it never generates legal content, and it never surfaces a provision
that a human has not yet checked against an official source.

**Disclaimer philosophy:** The system provides legal *awareness*, not legal *advice*.
It never claims a law "definitely applies" or that a user "has a case." Every response
carries a mandatory disclaimer (Section 10).

## 2. Project Motto (Non-Negotiable)

This project is **not**: a legal chatbot, an LLM wrapper, an AI lawyer, a legal
judgment engine, a replacement for a qualified advocate, or a full Indian law coverage
system.

**Conceptual flow:**
```
Scenario (natural language)
   → Domain Classification (1 of 5 legal domains)
   → Issue Detection using Prototype Similarity Matching
     (restricted to issues within the predicted domain)
   → Legal provision retrieval — restricted to manually verified provisions
     (KB lookup, zero ML/generation)
   → Two-layer plain-language rationale:
       issue match reason (why the scenario matched this issue)
       + curated provision relevance rationale (why this provision maps to the issue)
   → Issue-specific action steps
   → Official government complaint portals
   → Mandatory disclaimer
```

**Why this differs from a generic LLM legal tool:** An LLM generates answers from
training memory — unverifiable, inconsistent between calls. This system retrieves
content from a human-curated legal knowledge base, and only the subset of that
knowledge base a human has manually verified is ever shown to a citizen. The ML layer
only classifies and matches; it never decides what the law says, and it never fills a
gap left by missing verification.

## 3. Phase 1 Scope

### 3.1 Five Approved Domains

| Domain ID | Display Name | Primary Legal Framework |
|---|---|---|
| `cyber_fraud` | Cyber Fraud | Information Technology Act 2000 |
| `consumer_issues` | Consumer Issues | Consumer Protection Act 2019 |
| `traffic_enforcement` | Traffic Enforcement | Motor Vehicles Act 1988 |
| `workplace_wage` | Workplace / Wage | TBD — gated on `docs/wage_law_research.md` |
| `contractual_disputes` | Contractual Disputes | Indian Contract Act 1872 |

**Wage law rule:** Do not populate any `workplace_wage` KB entries based on Payment of
Wages Act 1936 / Minimum Wages Act 1948 assumptions. The Code on Wages 2019 may have
superseded them. `docs/wage_law_research.md` must exist and document current
applicability, from official government sources, before any wage provision is added.

### 3.2 Controlled Coverage

- 5 domains, ~5–6 curated Acts, ~20–30 total curated candidate provisions
- A controlled issue taxonomy of **approximately 20–25 controlled issues** across the
  5 domains (currently **22 working issues** after taxonomy cleanup — see
  `TRAINING_DATA_PLAN.md` for the authoritative working list). The issue count is an
  approximate scope description, **not a quota** — do not invent issues to reach a
  round number, and do not keep an issue that fails the admission test (Section 6.8).
- Every candidate provision starts with `verification.status =
  pending_manual_verification` **and** `provision_status = unverified` (Section 7).
  Neither field alone makes a provision citizen-facing — see Section 7.5.

### 3.3 Explicitly Out of Scope (Phase 1)

Criminal law (IPC / BNS), CrPC/BNSS procedures, FIR filing as primary guidance, arrest
and bail procedures, constitutional law, Prevention of Corruption Act, case-outcome
prediction, automated legal judgment, CPC court procedure, full Indian law coverage,
lawyer-replacement functionality.

**Specifically banned re-additions:** IPC Section 420 under `cyber_fraud`; Prevention
of Corruption Act under `traffic_enforcement`.

## 4. Architecture

### 4.1 Rejected Architecture (do not revive)

```
Scenario → ML Category Classification → Fixed Acts/Sections for that Category → Response
```
Rejected because a broad domain contains multiple issue types needing different
provisions; returning all sections for a domain is inaccurate; there is no way to
explain *why* a specific provision applies.

### 4.2 Correct Architecture

```
SCENARIO
  → DOMAIN CLASSIFICATION
  → ISSUE DETECTION (prototype similarity, scoped to the predicted domain's issues)
  → MANUALLY VERIFIED LEGAL PROVISIONS ONLY (KB lookup, zero ML/generation)
```

### 4.3 System Components

```
React Frontend (3000)
   ↓ HTTPS REST
Node.js / Express API Gateway (5000)
   ↓ HTTP
Python FastAPI ML Service (8000)
   ├── Module 1: Domain Classifier (trained model — Logistic Regression)
   ├── Module 2: Issue Detector (Issue Detection using Prototype Similarity Matching — not a trained classifier)
   ├── Module 3: Legal Intelligence Engine
   ├── Module 4: Response Builder
   └── reads: Legal Knowledge Base (JSON, read-only at runtime)
```

**Modularity requirement:** Modules 1–4 run in one Python service in Phase 1 but must
stay logically separate (separate files, stable interfaces) so Modules 1–2 can be
replaced by BERT in Phase 2 without touching Modules 3–4, the KB, or the response
schema.

### 4.4 Component Responsibilities

**React Frontend:** Accepts scenario text; renders domain, issue, provisions (only
manually verified ones), the two-layer relevance rationale (`issue_match_reason` +
`provision_relevance_rationale`), action steps, portals, disclaimer, clarification
prompt, and the explicit "no verified provision available" state when it occurs.
Contains no legal logic — renders only what the API returns. Does not assume a raw
issue `similarity_score` must be shown to the citizen (see Section 8.1) — that is a
usability decision made later, not an architectural requirement.

**Node.js API Gateway:** Validates input (length/type/sanitization), rate limits
(10 req/min/IP), generates UUID `request_id`, proxies to the ML service, logs
anonymized data only (Section 9), returns the response, maps validation failures to
HTTP 400.

**Python FastAPI ML Service:** Loads KB and models at startup; wires the four modules
in sequence; returns structured JSON per the response contract (Section 8.1).

## 5. Module 1 — Domain Classifier

**Permanent architectural decision:** TF-IDF + Logistic Regression. Input: raw
scenario text. Output: `{ "domain_id": "cyber_fraud", "confidence": 0.91 }`.

**Supervised target:** Module 1 trains on `scenario → domain` **only**. `domain` is the
supervised target. `issue_id` (present in the dataset, Section 11) is **never** used as
a Module 1 training target, input feature, hidden feature, or a substitute for domain
classification. It is human-annotated analysis metadata only.

**Preprocessing and hyperparameters are experiment-level decisions, not constitutional
rules.** They must be selected and documented only after Dataset V1 exists and
baseline experiments have been run (see Section 11). This file does not lock:
lowercasing/punctuation handling specifics, stopword lists, lemmatization, exact
`ngram_range`, exact `max_features`, or `sublinear_tf`. Those live in the training
implementation/configuration, not here.

**Principles that do govern preprocessing (permanent):**
- Training and inference preprocessing **must be identical** — this is a hard rule,
  not an experiment variable.
- Preprocessing must preserve scenario/legally-relevant meaning. Stopword removal must
  not blindly strip meaningful terms — **negation handling is important** (e.g. "did
  not receive," "not paid," "refused to") and must not be silently destroyed by a
  generic stopword list.
- Lemmatization is optional until evaluated — do not include it just because it is
  common in NLP tutorials.
- Unigram/bigram settings and `max_features` must be evaluated on Dataset V1, not
  assumed.

**Suggested baseline comparison (to run once Dataset V1 exists, not before):**
- Baseline A — minimal text normalization + TF-IDF + Logistic Regression
- Baseline B — normalization + selected preprocessing (stopwords/negation-aware/lemmatization)
- Baseline C — alternative n-gram / TF-IDF parameter settings

Evaluate each using macro F1, per-class precision/recall/F1, and the confusion matrix
(Section 11). Document the finally selected preprocessing in `docs/evaluation_notes.md`
after evaluation — do not choose it up front because it is conventional.

**Must not:** select sections, generate explanations, judge case validity, generate
action steps, produce legal conclusions.

**Naming rule:** the score is *classification confidence*, not legal certainty. Label
it "Classification confidence" / "Model confidence" everywhere — API and UI. Never
"legally correct" or "legal certainty."

**Artifacts:** `models/tfidf_domain_vectorizer.pkl`, `models/domain_classifier.pkl`.

**Phase 2:** replaced by fine-tuned BERT; the `domain_id` + `confidence` output
contract must remain stable.

## 6. Module 2 — Issue Detector

### 6.1 Why the Issue Layer Exists

Domain alone is too coarse for provision retrieval — e.g. `consumer_issues` covers
defective products, refund denial, misleading ads, service deficiency, and unfair
trade practice, which may need different provisions.

### 6.2 Terminology — Not a Trained Classifier

Module 2 is **Issue Detection using Prototype Similarity Matching**. It is TF-IDF
representation + cosine similarity against curated prototypes — it is not a
separately trained statistical classifier, and cosine similarity is not itself a
trained classifier. Do not call this "Issue Classification" in technical or
viva-facing documentation. Correct module naming:
- Module 1: **Domain Classification** (a trained classifier)
- Module 2: **Issue Detection using Prototype Similarity Matching** (not a trained
  classifier)

### 6.3 Approach (Phase 1) — Domain-Scoped Prototype Similarity Matching

After Module 1 predicts a domain, Module 2 detects the issue **only among the issues
belonging to that predicted domain.** It does not compare the scenario against issues
from unrelated domains.

```
predicted domain_id
  → filter the issue taxonomy to issues where issue.domain_id == predicted domain_id
  → load curated prototype texts (3–5 per issue) for those candidate issues only
  → vectorize the scenario and the candidate prototypes
  → cosine similarity between scenario vector and each candidate prototype
  → select the issue whose prototype(s) score highest
```

Example: if Module 1 predicts `consumer_issues`, Module 2's candidate set is limited to
`defective_product`, `refund_denial`, `misleading_advertisement`,
`service_deficiency`, `unfair_trade_practice` — it must never simultaneously score the
scenario against `otp_fraud`, `bribe_demand`, `unpaid_wages`, or any issue outside the
predicted domain.

Output: `issue_id`, `similarity_score` (see Section 6.2 naming — never called
"confidence"), and `scenario_signals` (overlapping terms, supporting explanation only).

### 6.4 LOCKED DECISION — Vectorizer Scope

**The Issue Detector uses its own issue-specific TF-IDF vectorizer, fit in memory at
service startup from the curated issue prototype texts in `issue_mappings.json` across
all domains. It does NOT reuse the Domain Classifier's TF-IDF vectorizer. No `.pkl`
file is produced for this vectorizer — it is rebuilt from the KB every time the
service starts.**

This is distinct from the domain-scoped *candidate filtering* in Section 6.3: the
vectorizer's vocabulary/IDF weights are fit once, globally, over all issue prototypes
(for a consistent vector space across the whole KB); what changes per-request is which
prototypes are compared against the scenario, which Section 6.3 restricts to the
predicted domain's issues.

**Reason:** domain classification and fine-grained issue similarity are different
representation problems. The domain vectorizer's IDF weights are tuned to separate 5
broad domains; terms that are common across a domain's examples but critical for
distinguishing issues *within* that domain would be underweighted if the domain
vectorizer were reused. A separate vectorizer, fit on issue-level prototype text,
optimizes for the discrimination Module 2 actually needs.

**Consequence for Phase 2:** this keeps Module 2 fully decoupled from Module 1, so
replacing Module 1 with BERT requires no change to Module 2. Module 2 remains
independently evaluable and independently replaceable later.

**Trade-off accepted:** the prototype corpus is small, so IDF weights are less
statistically robust than a large training set would give. Mitigate by keeping 3–5
well-differentiated prototypes per issue; do not compensate by adding keyword rules as
a decision mechanism (Section 6.6).

### 6.5 Domain-Scoped Candidate Filtering — Accepted Phase 1 Limitation

**If Module 1 predicts the wrong domain, Module 2 is restricted to the wrong issue
candidate set and may not recover** — it cannot select an issue belonging to a domain
Module 1 did not predict. This is an accepted Phase 1 limitation, not an oversight.

It must be observed and tracked through:
- the domain confusion matrix (Section 11)
- low-confidence / clarification handling (Section 8.2) — a low domain confidence
  should reduce trust in the downstream issue result, not just the domain result
- explicit failure analysis in `docs/evaluation_notes.md`

**Future improvements (not implemented in Phase 1):** top-2 domain routing (run issue
detection against the candidate issues of the top two predicted domains), joint
domain/issue classification, BERT-based hierarchical classification. These are Phase 2+
directions and must not be built now.

### 6.6 Keyword Matching Rule

Keywords may be used only as a supporting/debugging signal (e.g. populating
`scenario_signals`). Keywords must never be the primary issue-decision mechanism.
`"if scenario contains 'scam' → cyber_fraud"` is unacceptable — a shopkeeper "scamming"
someone with fake shoes is not cyber fraud.

### 6.7 Two-Layer Relevance Reasoning

The explanation shown to a citizen is made of two distinct reasoning layers that must
never be collapsed into one curated sentence.

**Layer A — Issue Match Reason** (`issue_match_reason`)
- **Owner:** Module 2 / analysis layer, generated at request time.
- **Explains:** why the scenario matched the detected issue.
- **Basis:** transparent Phase 1 signals only — matched prototype, similarity result,
  scenario/prototype term overlap (supporting, not decisive), `scenario_signals`.
- **Example:** "The scenario matched the OTP fraud issue type because it contains
  signals related to bank impersonation and an OTP request."
- This is scenario-to-issue matching explanation, **not legal reasoning.**

**Layer B — Provision Relevance Rationale** (`provision_relevance_rationale`)
- **Owner:** curated issue-to-provision mapping, stored in `issue_mappings.json`
  (Section 7.2), authored by a human, not generated at request time.
- **Explains:** why a manually verified provision is associated with the detected
  issue type.
- **Example:** "This provision is mapped to this issue type because the curated issue
  definition concerns alleged digital personation used to deceive a person."
- Not dynamically invented by an LLM at request time.

**Combined citizen-facing presentation (conceptual):**
```
Why this may be relevant:
1. Your scenario matched [issue type] based on [issue_match_reason].
2. The project's curated legal mapping associates this issue type with
   [provision] because [provision_relevance_rationale].
```

Neither layer may be called SHAP, LIME, XAI, or model explainability (Section 10). It
is transparent pipeline reasoning (Layer A) plus curated legal rationale (Layer B).

### 6.8 Issue Taxonomy Design Rule and Admission Test

**An issue must represent WHAT HAPPENED in the user's scenario** — a distinct
real-life situation type. An issue must **not** primarily represent: what action the
user wants to take, what remedy the user wants, which complaint procedure they are
asking about, or which portal they should use. Those belong in
`issue_actions_portals.json`, the provision mappings, or response construction — not in
the issue taxonomy itself.

**Admission test — before an issue is approved, all five must hold:**
1. Is this a distinct real-life scenario type?
2. Can the Issue Detector meaningfully distinguish it from sibling issues (given
   prototype-similarity matching over a small curated corpus)?
3. Does it map to meaningfully specific legal provision retrieval or applicability
   rationale?
4. Does it produce meaningfully different action guidance or portal conditions?
5. Is it inside the non-criminal Phase 1 scope?

An issue that fails these — e.g. it describes a desired remedy ("compensation"), a
procedural intent ("how to complain"), or overlaps a sibling too heavily for
prototype similarity to separate — must not be admitted or retained. The issue count
is an approximate scope description, not a quota (Section 3.2).

### 6.9 Module 2 Is Not Trained on the Training Dataset

Module 2's matching data is the curated issue prototype texts in `issue_mappings.json`
(Section 6.3–6.4). **The Issue Detector is not trained on `training_data_v1.csv` (or
any later dataset version) in Phase 1.** The training dataset supervises Module 1 only
(Section 5). `issue_id` in the dataset is human-annotated analysis metadata, never a
training signal for Module 2. See Section 11 for the dataset schema and the role of
`issue_id`.

### 6.10 Issue-to-Provision Support Gate (Governance)

Before an issue is **approved** for Dataset V1 labeling and KB population, it must pass
an **Issue Support Review** — the project must have reasonable evidence, from official
legal-source research, that the issue maps to relevant provision retrieval, before
committing to it. This prevents creating an issue first and searching for a law
afterward. This does **not** require every provision to already be manually verified
before the taxonomy is discussed — it requires a credible provision-support basis per
issue. The review records, per issue: `issue_id`, `domain_id`, `scenario_definition`,
`sibling_boundary`, `candidate_official_legal_source`, `candidate_provision_support`,
`expected_action_difference`, and `status` (one of `working` / `provision_research_required`
/ `taxonomy_supported` / `rejected` / `merged` — `taxonomy_supported` is a review
finding, not final approval; the taxonomy stays WORKING until user sign-off). The
detailed review procedure lives in
`TRAINING_DATA_PLAN.md`; the taxonomy stays WORKING until this review and user sign-off
complete.

## 7. Legal Knowledge Base

### 7.1 Core Principle

Legal truth (Act → Section) and ML taxonomy (Domain → Issue) are different concepts
and must be stored separately. The bridge is Issue → Provision references.

### 7.2 Three-File Structure

- **`acts_and_sections.json`** — Legal Truth Store. Act → Section. Official text,
  simplified explanation, source metadata, verification block, `provision_status`
  (Section 7.4). Modified only by human curation. Changes rarely.
- **`issue_mappings.json`** — Bridge File. Per issue: 3–5 prototype texts (used by
  Module 2's similarity matching, Section 6.3) + provision references (`act_id` +
  `section_id` + `provision_relevance_rationale`, used by Module 3, Section 6.7 Layer
  B). Changes occasionally.
- **`issue_actions_portals.json`** — Practical Guidance Store. Per issue: action steps
  and portal references (priority, usage condition). Changes most frequently (URLs,
  refined steps).

**Why separate:** each file has a different change rate and risk profile; editing
low-risk action steps must never risk corrupting verified legal text.

### 7.3 ID/Reference Integrity

Every Act has a stable ID (`it_act_2000`); every section a stable ID (`66d`). Issue
mappings reference these IDs — legal text is never duplicated. Every `act_id`+
`section_id` pair referenced in `issue_mappings.json` must resolve to a real entry in
`acts_and_sections.json`.

### 7.4 Provision Record Format

```json
{
  "section_number": "66D",
  "official_section_title": "...",
  "official_text": "...",
  "simplified_explanation": "...",
  "applicability_notes": "...",
  "provision_status": "unverified",
  "verification": {
    "status": "pending_manual_verification",
    "verified_by": null,
    "verified_on": null
  }
}
```

**`provision_status` is a controlled enum, not a free-text or AI-assumed value:**
`unverified` (default for every new candidate provision) | `in_force` | `omitted` |
`repealed` | `amended_review_required` | `applicability_uncertain`.

For Phase 1, `in_force` is the only status considered eligible for citizen-facing
retrieval, and only once combined with `verification.status == manually_verified`
(Section 7.5). `unverified`, `omitted`, `repealed`, `amended_review_required`, and
`applicability_uncertain` must never be surfaced to a citizen as an applicable legal
provision, unless the architecture is explicitly changed later for historical/
legal-reference display.

Act-level record additionally carries `official_act_name`, `act_year`, `short_name`,
`official_source_name`, `official_source_url`, `sections`.

### 7.5 HARD RULE — Manual Verification Is Human-Only, and Pending Provisions Are Never Citizen-Facing

**Lifecycle:**
```
Candidate provision identified
  → added to legal KB (provision_status = unverified, verification.status = pending_manual_verification)
  → human checks the official source
  → human confirms legal text, section identity, source, and provision status
  → human sets verification.status = manually_verified AND provision_status = in_force (if currently in force)
  → provision becomes eligible for citizen-facing retrieval
```

**A legal provision is NOT eligible for citizen-facing retrieval while
`verification.status` is `pending_manual_verification`.** Citizen-facing eligibility
requires **both**:
1. `verification.status == "manually_verified"`, **and**
2. `provision_status` is an eligible status (`in_force` in Phase 1).

**No AI assistant, including Claude, may ever change `verification.status` to
`manually_verified`, or independently set `provision_status` to `in_force` as a final
verified fact.** Only a human who has checked the provision against an **approved
official source under Section 7.6** (India Code, or an official central-government
ministry / regulator / statutory-authority publication) may set:
```json
"provision_status": "in_force",
"verification": { "status": "manually_verified", "verified_by": "<name>", "verified_on": "YYYY-MM-DD" }
```
During human verification, the project team verifies: Act identity, Section identity,
official section title, official source, legal text/verified extract, current
provision status, amendment/omission concerns, and applicability notes.

Claude may design schema, identify candidate provisions, flag that official-source
review is needed, and draft simplified explanations — none of that is manual
verification, and none of it may set an eligible `provision_status` or
`manually_verified`.

**If an issue mapping references a provision that is not both manually verified and
`in_force`, Module 3 (Section 8) must not return that provision, must not substitute
another AI-generated legal answer, and must not ask an LLM to invent a missing
section.** See Section 8 for the explicit safe-state response.

### 7.6 Legal Source Rules

**Primary source:** India Code (indiacode.nic.in). **Acceptable:** official central
government ministry/regulator/statutory authority publications. **Prohibited:** AI
model memory/training knowledge, blogs, news, social media, legal forums, any
unverified secondary source.

Every provision must have `official_source_name` and `official_source_url`. If a URL
is unconfirmed, set it to `null` and keep verification pending — never use a
placeholder URL.

## 8. Legal Intelligence Engine (Module 3) and Response Contract

**Input:** `issue_id`. **Steps:**
```
issue_id
  → retrieve issue-to-provision references from issue_mappings.json
  → resolve provision IDs against acts_and_sections.json
  → check verification.status == manually_verified
  → check provision_status is eligible (in_force)
  → discard any provision not eligible for citizen-facing retrieval (Section 7.5)
  → attach provision_relevance_rationale (Layer B, Section 6.7) for each eligible provision
  → retrieve issue-specific action steps from issue_actions_portals.json
  → evaluate portal mappings and usage conditions
  → filter portals to those supporting this issue_id, sort by priority
    (immediate → primary → secondary), return max 3
  → return structured legal intelligence result
```

**Must not:** use any ML model, generate content, infer from model memory, invent Act
names/penalties/procedures, make external API calls, replace an unverified provision
with AI-generated law, ask an LLM to invent a missing section, expose pending
candidate provisions to citizens, or treat issue similarity as legal certainty. This
is the component that makes the system trustworthy — every returned provision was
pre-selected by a human **and** manually verified before it can ever be returned.

**Explicit safe state:** if no eligible manually verified provision exists for the
detected issue, the Legal Intelligence Engine must report this explicitly rather than
returning nothing unexplained or fabricating an answer — see `legal_information_status`
in Section 8.1. The citizen-facing message must remain cautious and must not imply a
legal answer exists when it does not.

**Action steps:** issue-specific (never generic domain boilerplate), most
time-sensitive step first, max 5 steps, no FIR filing as primary advice, no criminal
procedure.

**Portals:** each entry has `portal_id`, `name`, `official_url`, `purpose`, `priority`
(`immediate`/`primary`/`secondary`), `usage_condition`, `official_source`,
`supported_issue_ids`. Only official government/regulator portals. Conditional portals
(e.g. RBI Banking Ombudsman) must carry a `usage_condition`, not be returned
unconditionally.

**Response Builder (Module 4):** assembles all module outputs, assigns the domain
confidence label, sets `low_confidence_warning`/`needs_clarification`, sets
`legal_information_status`, selects a clarification question if needed, attaches the
mandatory disclaimer, enforces the schema below.

### 8.1 Response Contract

```json
{
  "success": true,
  "request_id": "uuid-v4",
  "analysis": {
    "domain": { "id": "cyber_fraud", "display_name": "Cyber Fraud", "confidence": 0.91, "confidence_label": "High" },
    "issue": { "id": "otp_fraud", "display_name": "OTP / Financial Impersonation Fraud", "similarity_score": 0.88, "issue_match_reason": "..." },
    "scenario_signals": ["pretending to be bank", "asked for OTP"]
  },
  "legal_provisions": [
    {
      "act_id": "it_act_2000", "act": "Information Technology Act, 2000", "section": "Section 66D",
      "title": "...", "simplified_explanation": "...", "provision_relevance_rationale": "...",
      "official_source": { "name": "India Code", "url": "https://indiacode.nic.in/..." }
    }
  ],
  "legal_information_status": "provisions_available",
  "action_steps": ["...", "...", "..."],
  "portals": [{ "name": "...", "official_url": "...", "purpose": "...", "priority": "immediate" }],
  "low_confidence_warning": false,
  "needs_clarification": false,
  "clarification_question": null,
  "disclaimer": "This information is for legal awareness only and does not constitute legal advice. Please consult a qualified legal professional for advice specific to your situation."
}
```

**Field naming rules (locked):**
- `domain.confidence` — Logistic Regression `predict_proba()` output. May be called
  "confidence" / "classification confidence" / "model confidence."
- `issue.similarity_score` — cosine similarity output. **Never** called `confidence`,
  `probability`, `legal confidence`, or `certainty` (Section 6.2, 6.3).
- `issue.issue_match_reason` — Layer A (Section 6.7).
- `legal_provisions[].provision_relevance_rationale` — Layer B (Section 6.7),
  replaces any prior `why_relevant` naming.
- `legal_information_status` — `"provisions_available"` or
  `"no_verified_provision_available"` (Section 8). Exact field name may be refined
  during implementation, but the concept (an explicit safe state, not silent omission)
  is locked.

The raw `issue.similarity_score` may be retained in the API response for debugging,
evaluation, and threshold tuning. **Whether the frontend displays it to an ordinary
citizen is a usability decision made later, not an architectural requirement locked
here.**

Full statutory text never appears in the default response — only
`simplified_explanation`. The UI may link out to the official source.

**Confidence label thresholds (Phase 1 provisional defaults, not permanently
locked):** High ≥ 0.80, Medium 0.65–0.79, Low 0.60–0.64, Low+warning < 0.60. These
numeric thresholds — and any equivalent thresholds later introduced for issue
`similarity_score` — must be treated as configuration and re-tuned using Dataset V1
evaluation results (Section 11), not treated as immutable constitutional values. The
architectural rule that survives any retuning is Section 8.2.

### 8.2 Low-Confidence Handling

**Correct (permanent architecture):** HTTP 200 with `low_confidence_warning`/
`needs_clarification` flags. **Wrong (rejected):** HTTP 422 for low ML confidence —
model uncertainty on a valid scenario is not a client error. HTTP 400 remains reserved
for actual input validation failures (empty/too short/too long/malformed). Phase 1
clarification questions may be simple domain-keyed static text; the contract must not
block a future dynamic clarification engine. The exact numeric threshold that triggers
these flags is configuration/evaluation-driven (Section 8.1), not hardcoded here.

## 9. Privacy and Logging

Raw scenario text is **never** stored in query logs. Logged fields: request UUID,
predicted `domain_id`/`issue_id`, `domain.confidence`, `issue.similarity_score`,
language code, timestamp, feedback status, optionally a SHA-256 hash of the scenario
(dedup only — this is a technical measure, not a claim of anonymity; never state
hashing makes the system "fully anonymous"). Feedback comments may contain personal
context — store separately, sanitize before storage, do not overclaim legal
compliance.

## 10. Legal Wording Rules

**Never use:** "definitely applies," "you can definitely sue," "you have a strong
case," "has committed an offence," "acted illegally," "you will win," "you are legally
protected," "exact law applicable to your case." Also never describe the knowledge
base as a whole as "pre-verified legal information" — it contains unverified
candidates; only the manually verified subset is citizen-facing (Section 1, 7.5).

**Use instead:** "relevant curated legal provisions," "potentially relevant
provisions," "provisions that may apply based on the described scenario," "based on
the information you have provided," "human-curated legal knowledge base with
citizen-facing retrieval restricted to manually verified provisions."

**Mandatory disclaimer, every response, no exceptions:**
> "This information is for legal awareness only and does not constitute legal advice.
> Please consult a qualified legal professional for advice specific to your situation."

**Explainability honesty:** `issue_match_reason` (Layer A) is transparent pipeline
reasoning from Phase 1 signals; `provision_relevance_rationale` (Layer B) is curated,
human-authored rationale (Section 6.7). Call these "curated rationale" / "transparent
pipeline reasoning" — never "explainable AI" or "XAI," and never SHAP/LIME, unless
those techniques are actually implemented.

## 11. Dataset Lifecycle

Iterative, not a one-time bulk task. The governance lifecycle is:
```
Lock the five-domain taxonomy
→ draft the WORKING issue taxonomy
→ perform the Issue Admission Test (Section 6.8) and Issue Support Review (Section 6.10)
→ revise / merge / reject issues where required
→ user signs off the approved issue taxonomy
→ approve TRAINING_DATA_PLAN.md
→ create Dataset V1 (~25–30/domain, ~125–150 total)
→ build full training pipeline → train baseline(s)
→ evaluate using Stratified 5-Fold Cross-Validation
  (confusion matrix, per-class + macro F1; select preprocessing/hyperparameters, Section 5)
→ inspect confusion matrix and issue_id error slices
→ document findings → improve dataset for observed failures
→ v2 (never overwrite v1) → retrain → repeat until targets are understood, not just hit
```
The issue taxonomy is locked by **sign-off after review**, not before it — do not treat
the working taxonomy as final until the admission test + support review clear and the
user signs off.

**Issue Support Review vs. Manual Provision Verification are separate governance stages,
never merged:**
- **Issue Support Review** (Section 6.10) asks: "Does this issue appear legally
  supportable and useful enough to exist in our controlled taxonomy?" It needs
  reasonable official-source *evidence* of provision support — it does **not** require
  any provision to have completed manual verification.
- **Manual Provision Verification** (Section 7.5) asks: "Has this exact Act / section /
  source / status / legal text been checked by a human against an approved official
  source and approved for citizen-facing retrieval?" It is human-only and gates
  citizen-facing retrieval.

Never overwrite a dataset version. Never declare success on accuracy alone or on
hitting an arbitrary threshold without inspecting the confusion matrix. Never
bulk-generate near-duplicate examples to hit a sample-count target.

**Pipeline-before-data:** `train_domain_classifier.py` must run identically on a
10-row test file or the full V1 file. Preprocessing must be identical between training
and inference (Section 5) — this is the one preprocessing rule that is permanent; the
specific preprocessing steps themselves are not.

External datasets require: scope filtering, text normalization, manual re-annotation
to *our* taxonomy (their original labels are irrelevant), review for ambiguity.
Synthetic augmentation is allowed only to fill gaps the confusion matrix identifies,
must be human-reviewed per example, and must never be hundreds of near-duplicates.

### 11.1 Dataset Schema and the Role of `issue_id`

Dataset V1 (and later versions) have the schema: **`scenario, domain, issue_id`**.
- `scenario` — raw scenario text, the model input.
- `domain` — the **supervised target** for Module 1 (one of the 5 domain IDs).
- `issue_id` — **human-annotated analysis metadata only** (one of the approved issue
  IDs, belonging to the row's domain). Used for coverage analysis, error slicing
  (e.g. "which issue types inside `workplace_wage` are most often misclassified?"),
  dataset diversity inspection, and qualitative Module 2 sanity checking. It is **not**
  a Module 1 target/feature (Section 5) and **not** training data for Module 2
  (Section 6.9). Using `issue_id` for error slicing is analysis only — it does not turn
  Module 1 into an issue classifier.

### 11.2 Phase 1 Language Scope

**Phase 1 officially supports English.** In scope for Dataset V1: Indian English
phrasing, informal English, grammar mistakes, missing articles, short user-style text,
spelling mistakes, run-on sentences (e.g. "my salary not credited yet", "shop guy not
giving refund"). **Out of official Phase 1 scope:** code-mixed Hinglish (e.g. "paisa
nahi mila", "salary nahi diya"). Do not claim Hinglish support in Phase 1. Code-mixed
input may be evaluated later in a separate experimental dataset — do not fold it into
the official Dataset V1 coverage target.

### 11.3 Coverage Target and Evaluation Strategy

- **Coverage target:** approximately **25–30 distinct scenarios per domain** for
  Dataset V1 (domain-level balance is the primary class-balance objective, since
  `domain` is the only supervised target). Approved issue coverage is used as a
  **diversity checklist** (~4–7 scenarios per approved issue as a soft planning guide,
  not a hard balancing rule — issue-level counts need not be equal). Expected total
  ~125–150 if the coverage plan naturally supports it; do not manipulate counts to hit
  a fixed total.
- **Primary model-development evaluation: Stratified 5-Fold Cross-Validation**,
  stratified by `domain`, fixed seed. A 70/15/15 split is *not* the primary strategy —
  at ~125–150 rows it produces validation/test partitions too small to trust. CV is
  used to compare preprocessing/TF-IDF configurations and inspect macro F1, per-class
  precision/recall/F1, and cross-fold confusion behavior.
- **No-leakage rule:** near-duplicate or intentionally paraphrased variants derived
  from the same base scenario must not be split across folds in a way that creates
  leakage. If paraphrase families later exist, use `StratifiedGroupKFold` / explicit
  scenario-family IDs. Do not overengineer this before such families exist, but the
  no-leakage rule is permanent.
- **Future/final evaluation:** an untouched holdout or a manually curated challenge set
  once dataset maturity supports it. 5-fold CV does **not** replace the need for future
  unseen evaluation.

## 12. BERT Role (Phase 2)

Fine-tuned BERT may replace/improve Modules 1–2, particularly for short/ambiguous
scenarios, informal Indian English, and domain-boundary cases. BERT does **not**
replace the KB, issue mappings, action/portal mappings, Module 3, Module 4, or the
response schema. The stable ML output contract that must survive the swap:
```json
{ "domain": {"id":"...","confidence":0.0,"confidence_label":"..."}, "issue": {"id":"...","similarity_score":0.0,"issue_match_reason":"..."}, "scenario_signals": ["..."] }
```
Recommended: `bert-base-uncased` (Phase 2, English); `bert-base-multilingual-cased` or
IndicBERT (Phase 3, multilingual).

**Module 2 score-contract safety rule (future-proofing, does not change Phase 1):** In
Phase 1, `issue.similarity_score` means cosine similarity against curated issue
prototypes — not a probability, confidence, or certainty. If a future phase replaces
prototype similarity matching with a *trained* issue model, the Module 2 score field,
its semantics, and the API contract must be **explicitly reviewed and versioned** at
that time. Phase 1 `issue.similarity_score` must **not** be silently reused to
represent classifier confidence, classifier probability, or any other fundamentally
different score. This note does not decide the Phase 2 issue-model API, does not rename
the Phase 1 field, and does not change the current Issue Detector architecture — it only
prevents a future misuse of the existing field name.

## 13. RAG Role (Phase 3)

Enhancement only, not a dependency — Phase 1 works without it. RAG may only ground
*explanation* generation in retrieved, verified legal text chunks; it must never select
Acts/sections independently, invent section numbers/penalties/rights, generate action
steps, or override Module 3's provision selection. RAG is subject to the same
citizen-facing eligibility rule as Module 3 (Section 7.5) — it may only ground
explanations in manually verified, `in_force` provisions. Every RAG output must be
traceable to a retrieved source chunk.

## 14. Frontend Philosophy

Primary UX is scenario analysis, not a chatbot: input → domain result → issue result →
provision cards (with `provision_relevance_rationale`, not raw legal text) → action
steps → portals → disclaimer → clarification prompt if low confidence. The frontend
must also render the explicit "no verified provision available" state
(`legal_information_status`) when it occurs — this must not be hidden or silently
rendered as an empty section. Whether raw `issue.similarity_score` is shown to
citizens is a usability decision, not locked here (Section 8.1). Do not build display
components ahead of a stable API response schema.

## 15. Beginner-Friendly Development Requirement

The project owner is new to ML. For every implementation component, explain before
coding: what it is, why it exists, inputs, outputs, where it sits architecturally,
what breaks without it — then implement — then explain the important decisions made.
Do not hand-wave anything as "standard boilerplate" without a stated reason.

## 16. Avoid Premature Complexity

Sufficient Phase 1 stack: React + Node/Express + Python FastAPI + structured JSON KB +
MySQL logging. Do not introduce Kafka, Kubernetes, distributed databases, multi-agent
systems, excessive microservices, or enterprise abstractions. Docker Compose for local
dev is fine. Add complexity only when a real requirement justifies it.

## 17. Implementation Conventions

- Every provision record and file must trace to an official source (Section 7.6).
- Citizen-facing provision eligibility requires **both**
  `verification.status == manually_verified` **and** `provision_status == in_force`
  (Section 7.5). Neither field alone is sufficient.
- `verification.status` and an eligible `provision_status` are human-only fields;
  Claude must never set either, even if asked casually (Section 7.5).
- Preprocessing steps and TF-IDF hyperparameters (`ngram_range`, `max_features`,
  stopwords, lemmatization) are experiment-level configuration selected after Dataset
  V1 evaluation, not constitutional rules (Section 5).
- Confidence-label and clarification thresholds are configuration, tuned from
  evaluation results, not permanently hardcoded (Section 8.1).
- Module 2 output is `similarity_score`, never `confidence`/`probability`/`certainty`
  (Section 6.2–6.3, 8.1).
- Module 2 detects issues only within the domain Module 1 predicted (Section 6.3);
  this is an accepted Phase 1 limitation (Section 6.5), not a bug.
- `issue_match_reason` (Layer A, generated) and `provision_relevance_rationale`
  (Layer B, curated) are separate concepts and must never be merged into one field
  or one generation step (Section 6.7).
- Issues represent what happened in the scenario, not desired remedy/procedure/portal;
  every issue must pass the admission test (Section 6.8) and the issue-to-provision
  support gate (Section 6.10). Issue count is an approximate scope figure (~20–25,
  currently 22), never a quota (Section 3.2).
- Dataset schema is `scenario, domain, issue_id`; `domain` is Module 1's only
  supervised target; `issue_id` is analysis metadata, never a Module 1 feature/target
  and never Module 2 training data (Sections 5, 6.9, 11.1).
- Phase 1 language is English (incl. Indian/noisy English); Hinglish/code-mixed is out
  of official Phase 1 scope (Section 11.2).
- Dataset V1 model development uses Stratified 5-Fold Cross-Validation (by `domain`,
  fixed seed) as the primary evaluation strategy, with a permanent no-leakage rule
  (Section 11.3); no fixed accuracy number ends iteration (Section 11).
- Domain/issue IDs are stable snake_case strings referenced by ID everywhere, never
  duplicated as free text.
- ML output contract (Section 12) must remain stable across Phase 1 → Phase 2.
- No production code is written until the relevant governance/blueprint document for
  that phase exists in this repository and has been approved by the user.
- `PROJECT_STATE.md` is the living implementation tracker; see its own rule for what
  qualifies as COMPLETE. This file (`CLAUDE.md`) changes rarely and only on explicit
  architectural decisions.

## 18. Success Reporting

On **successful** task completion, report only:
- Files modified
- Manual verification required (if any)
- Commit hash
- Updated project progress

Do **not** print detailed validation logs, loader summaries, regression summaries,
gate summaries, or test summaries unless: a validation step fails, a repair is
performed, human intervention is required, or the user explicitly requests a detailed
report.

**All validation, loader, test, and repository-integrity steps must still be executed
in full — only the reporting is shortened.** Never skip a check because its output
will not be shown.

---

**This file supersedes all prior CLAUDE.md versions referenced in project history
(e.g. "v2," "v3") — none of those files exist in this repository. This is the only
CLAUDE.md that governs this project going forward.**
