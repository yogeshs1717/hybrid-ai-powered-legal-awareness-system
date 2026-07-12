# PROJECT_CONTEXT_HANDOFF.md
# Smart Legal Intelligence System for Indian Law Awareness using NLP
# Complete Context Transfer Document — For New Claude Session

---

> **PURPOSE OF THIS DOCUMENT**
> This document transfers the complete, corrected project context to a new Claude
> conversation that has zero access to the previous chat history. It is the
> authoritative record of every architectural decision, correction, and pending task.
> The new Claude session must read this document in its entirety before taking any action.
>
> When earlier decisions conflict with later corrections, the LATER CORRECTION is the
> source of truth. Deprecated ideas are documented here only to prevent them from
> being accidentally revived.

---

## PART 1 — PROJECT IDENTITY

**Full Project Title:** Smart Legal Intelligence System for Indian Law Awareness using NLP

**Short Name:** Legal Intelligence System

**Domain:** Legal Tech / Civic Technology — India

**Intended Users:** Indian citizens who face common real-life legal situations and lack
awareness of their legal rights and applicable laws.

**Core Problem Being Solved:**
Many Indian citizens encounter situations involving cyber fraud, consumer exploitation,
workplace wage theft, traffic authority misconduct, and contractual disputes, but have
no accessible way to understand which laws apply to their situation or what practical
steps to take. Existing tools either provide generic answers or require the user to
already know which law to look for. This system bridges that gap.

**Phase 1 Purpose:**
Build a controlled, functional MVP that can analyze a user's natural language scenario,
classify it into one of five legal domains, identify the specific issue type within
that domain, retrieve verified curated legal provisions from a curated knowledge base,
and present simplified explanations, practical action steps, and official complaint portals.

**Legal Awareness Disclaimer Philosophy:**
The system provides legal awareness, not legal advice. Every response carries a mandatory
disclaimer. The system never claims that a specific law "definitely applies" or that a user
"definitely has a case." The system retrieves potentially relevant provisions and explains
why they may be relevant. All legal content must be verified from official sources.

---

## PART 2 — PROJECT MOTTO (NON-NEGOTIABLE)

This project is:
- **NOT** a legal chatbot
- **NOT** an LLM wrapper
- **NOT** an AI lawyer
- **NOT** a legal judgment engine
- **NOT** a replacement for a qualified advocate
- **NOT** a full Indian law coverage system

**The intended conceptual flow:**

```
Citizen describes a real-life scenario in natural language
                    ↓
System validates and understands the scenario
                    ↓
System determines the broad legal domain
(e.g., Cyber Fraud, Consumer Issues, Workplace/Wage)
                    ↓
System determines the specific issue within that domain
(e.g., OTP Fraud, Refund Denial, Delayed Wages)
                    ↓
System retrieves verified, curated legal provisions
relevant to that specific issue from the knowledge base
                    ↓
System explains in plain language why those provisions
may be relevant to the described situation
                    ↓
System suggests practical issue-specific next steps
                    ↓
System provides relevant official government portals
                    ↓
System states clearly this is legal awareness, not legal advice
```

**Why this architecture stands apart from generic LLM legal tools:**
A generic LLM generates legal answers from its training knowledge. It may be wrong.
It cannot cite an auditable official source. Its output can change between requests.
This system retrieves pre-verified, curated legal information from a controlled data store.
Legal content is determined by human curation and review, not by model generation.
The ML layer only classifies and matches. It never decides what the law says.

---

## PART 3 — FINAL PHASE 1 SCOPE

### Five Approved Legal Domains

| Domain ID             | Display Name           | Primary Legal Framework         |
|-----------------------|------------------------|---------------------------------|
| `cyber_fraud`         | Cyber Fraud            | Information Technology Act 2000 |
| `consumer_issues`     | Consumer Issues        | Consumer Protection Act 2019    |
| `traffic_enforcement` | Traffic Enforcement    | Motor Vehicles Act 1988         |
| `workplace_wage`      | Workplace / Wage       | To be confirmed (see note)      |
| `contractual_disputes`| Contractual Disputes   | Indian Contract Act 1872        |

**Wage Law Note (CRITICAL):**
The previous prototype used Payment of Wages Act 1936 and Minimum Wages Act 1948
without verifying their current status under the Code on Wages 2019. This must NOT
be blindly reused. Before populating any workplace_wage KB entries, the project team
must research the current applicability of the Code on Wages 2019 using official
Government of India sources and document the decision in `docs/wage_law_research.md`.

### Controlled Coverage Philosophy
- Five legal domains
- Curated Acts (approximately 5–6 major statutory areas)
- Approximately 20–30 curated legal provisions total across all domains
- A controlled issue taxonomy (approximately 25 issues across the five domains)
- Every provision manually verified against India Code before being marked verified

### Explicitly Out of Scope (Phase 1)

The following must NOT enter Phase 1 unless the project scope is explicitly changed:
- Criminal law analysis (IPC / Bharatiya Nyaya Sanhita provisions)
- CrPC / Bharatiya Nagarik Suraksha Sanhita court procedures
- FIR filing procedures as primary guidance
- Arrest and bail procedures
- Constitutional law and fundamental rights Articles
- Prevention of Corruption Act provisions
- Case outcome prediction
- Automated legal judgment
- Court procedure under CPC
- Full Indian law coverage
- Lawyer replacement functionality

**Specific removals from an earlier prototype that must NOT be re-added:**
- IPC Section 420 under cyber_fraud (criminal law — out of scope)
- Prevention of Corruption Act under traffic_enforcement (criminal law — out of scope)

---

## PART 4 — FINAL ARCHITECTURE

### The Rejected Architecture (DO NOT REVIVE)

An earlier prototype used this pattern:
```
Scenario → ML Category Classification → Category → Fixed Acts and Sections → Response
```

This was rejected because:
- A broad category like "consumer_issues" contains five different issue types
  (defective product, refund denial, misleading advertisement, service deficiency,
  unfair trade practice), each of which may involve different legal provisions
- Returning ALL sections for a domain regardless of the specific scenario is
  inaccurate and misleading to citizens
- The architecture provides no way to explain WHY specific provisions are relevant

### The Correct Architecture

```
SCENARIO → DOMAIN → ISSUE → RELEVANT CURATED LEGAL PROVISIONS
```

Not:

```
SCENARIO → DOMAIN → ALL SECTIONS FOR THAT DOMAIN
```

### Full System Architecture

```
React Frontend (Port 3000)
        ↓ HTTPS REST
Node.js / Express API Gateway (Port 5000)
        ↓ HTTP
Python FastAPI ML Service (Port 8000)
        ├── Module 1: Domain Classifier
        ├── Module 2: Issue Detector
        ├── Module 3: Legal Intelligence Engine
        ├── Module 4: Response Builder
        └── reads from: Legal Knowledge Base (JSON files)
```

### Component Responsibilities

**React Frontend:**
Accepts user scenario text. Displays structured results: domain, issue, legal provisions,
why relevant, action steps, portals, disclaimer. Shows clarification prompt when confidence
is low. Never contains legal logic. Renders only what the API returns.

**Node.js API Gateway:**
Receives scenario from browser. Validates input (length, type, sanitization).
Applies rate limiting (10 req/min per IP). Generates UUID request_id.
Proxies to Python service. Logs anonymized data (no raw scenario text).
Returns response to browser. Handles HTTP error codes for validation failures.

**Python FastAPI ML Service:**
The intelligence layer. Contains all four modules. Loads knowledge base and ML models
at startup. Wires all four modules in sequence. Returns structured JSON.

**Domain Classifier (Module 1):**
TF-IDF vectorization + Logistic Regression. Classifies raw scenario into one of five
legal domains. Returns domain_id and classification confidence. Does NOT select sections,
generate explanations, or determine whether a user has a legal case.

**Issue Detector (Module 2):**
Identifies the specific issue type within the predicted domain. Phase 1 approach:
cosine similarity against curated prototype texts stored in issue_mappings.json.
Returns issue_id, similarity score, and scenario_signals (key overlapping terms).
Does NOT use a separately trained ML model in Phase 1 (prototype similarity only).

**Legal Intelligence Engine (Module 3):**
Contains NO machine learning. Pure dictionary lookup from the knowledge base.
Given issue_id: retrieves provision references from issue_mappings.json, loads
provision details from acts_and_sections.json, retrieves action steps and portals
from issue_actions_portals.json. Returns provisions, action steps, portals.
Never generates content. Never invents laws or sections.

**Response Builder (Module 4):**
Assembles all module outputs into the final structured JSON. Assigns confidence labels.
Sets low_confidence_warning and needs_clarification flags. Selects clarification
question if needed. Adds mandatory disclaimer. Enforces response schema.

**Legal Knowledge Base:**
Three separate JSON files (explained in Part 7). Stores verified legal truth,
scenario taxonomy, and practical guidance. Read-only at runtime. Modified only
by human curation and verification.

**Database / Logging Layer:**
MySQL tables for anonymized query logs and user feedback. Raw scenario text is never
stored. Stores: request_id, domain_id, issue_id, confidence scores, language, timestamp.
Feedback table stores ratings and sanitized comments.

**Modularity Requirement:**
These are logical responsibilities. Modules 1-4 and the knowledge base loader all run
inside the same Python service in Phase 1. They must remain logically separate
(separate files, clear interfaces) so that Module 1 and Module 2 can be replaced by
BERT in Phase 2 without changing Modules 3, 4, the KB files, or the response schema.

---

## PART 5 — DOMAIN CLASSIFIER

**Phase 1 Approach:** TF-IDF Vectorization + Logistic Regression

**Input:** Raw user scenario text (string)

**Output:**
```
{ "domain_id": "cyber_fraud", "confidence": 0.91 }
```

**Processing pipeline:**
1. Lowercase the text
2. Remove punctuation
3. Remove NLTK English stopwords
4. Lemmatize tokens (WordNetLemmatizer)
5. TF-IDF transform (using trained vectorizer: max_features=8000, ngram_range=(1,2), sublinear_tf=True)
6. Logistic Regression predict_proba()
7. Return class with highest probability and that probability as confidence

**What the Domain Classifier must NOT do:**
- Select legal sections
- Generate legal explanations
- Determine whether a user has a legal case
- Generate action steps
- Provide legal conclusions of any kind

**Critical naming rule:**
The confidence score is classification confidence from the ML model.
It is NOT a measure of legal certainty or correctness.
Label it in the UI and API as "Classification confidence" or "Model confidence."
Never display "91% legally correct" or "High legal certainty."

**Training artifacts:**
- `models/tfidf_domain_vectorizer.pkl` (trained TF-IDF vectorizer)
- `models/domain_classifier.pkl` (trained Logistic Regression classifier)

**Phase 2 replacement:** This module is replaced by a fine-tuned BERT classifier.
The output contract (domain_id + confidence) must remain stable.

---

## PART 6 — ISSUE DETECTOR

### Why the Issue Layer Exists

Domain classification alone is insufficient for legal provision retrieval.
"Consumer issues" is too broad. A user with a defective product and a user who
received a misleading advertisement both fall under consumer_issues, but they
may need different legal provisions. The issue layer identifies which specific
problem type the scenario represents within the predicted domain.

### Phase 1 Issue Taxonomy (Working — Must Be Reviewed Before Finalization)

```
cyber_fraud
├── otp_fraud                   OTP theft / banking impersonation
├── online_impersonation        Fake officials or fake identity
├── phishing                    Fake links, fake login pages
├── identity_theft              Aadhaar/PAN misuse, credential theft
├── online_financial_fraud      Investment scams, advance fee fraud
└── unauthorized_account_access Hacked email, social media, accounts

consumer_issues
├── defective_product           Broken or faulty goods received
├── refund_denial               Refused refund within policy window
├── misleading_advertisement    False product claims, fake discounts
├── service_deficiency          Paid service not delivered as promised
└── unfair_trade_practice       Deceptive commercial practices

traffic_enforcement
├── bribe_demand                Officer demands cash payment
├── wrongful_challan            Incorrect or false fine issued
├── document_dispute            Document seizure or verification issue
└── vehicle_detention           Unlawful detention of vehicle

workplace_wage
├── delayed_wages               Salary not paid on time
├── unpaid_wages                Salary withheld entirely
├── unauthorized_deduction      Illegal deductions from salary
├── minimum_wage_violation      Paid below statutory minimum
└── wage_complaint_process      How to formally complain

contractual_disputes
├── breach_of_contract          Other party broke the agreement
├── non_performance             Party failed to deliver as agreed
├── security_deposit_dispute    Deposit not returned after agreement
└── compensation_for_breach     Seeking damages for breach
```

**This taxonomy is a working proposal, not legally final.** It must be reviewed
before dataset finalization and legal KB population.

### Phase 1 Approach

**Recommended approach: TF-IDF cosine similarity against curated issue prototypes**

Each issue has 3-5 prototype texts written in the knowledge base (issue_mappings.json).
These prototypes describe what that issue typically sounds like when a citizen describes it.
The issue detector vectorizes the user's scenario and computes cosine similarity against
each prototype. The issue with the highest similarity score is selected.

### UNRESOLVED ARCHITECTURAL QUESTION (Must Be Addressed in New Session)

**Should the Issue Detector reuse the Domain Classifier's TF-IDF vectorizer, or use a separate vectorizer?**

**Option A — Reuse the domain TF-IDF vectorizer:**
- Pros: Simpler — one vectorizer, one .pkl file, fewer moving parts
- Cons: The domain vectorizer was trained to distinguish between 5 broad legal areas.
  Its IDF weights reflect what is distinctive at the domain level. Issue detection
  requires distinguishing fine-grained sub-types within one domain — a different
  vocabulary problem. A word that is common across domain examples gets a low IDF
  weight even if it is critical for issue discrimination within that domain.
- BERT migration: When BERT replaces the domain classifier, the issue detector would
  need to be re-evaluated because it was sharing the domain vectorizer.

**Option B — Separate issue-specific TF-IDF vectorizer:**
- Pros: The vocabulary and IDF weights are derived from issue prototype texts,
  making them optimized for issue-level discrimination. The vectorizer is fit
  in-memory at service startup from the prototype texts in issue_mappings.json.
  No separate training script needed. No .pkl file needed. When BERT replaces
  Module 1, Module 2 is completely unaffected — clean separation.
  Adding a new issue only requires adding prototype texts to the KB, no retraining.
- Cons: One additional in-memory vectorizer (small, not a real performance concern).
  Prototype corpus is small, so IDF weights may be less statistically robust.
- BERT migration: Completely independent of Module 1 — cleaner Phase 2 migration.

**The previous architecture review leaned toward Option B** but required the new session
to explicitly compare both options and recommend the better long-term architecture before
implementing. Do not implement blindly — explain the trade-off and confirm the choice.

### Keyword Matching Rule
Keywords may be used as supporting signals (for debugging, explanation, prototype support).
Keywords must NOT be the primary legal decision engine.
"if scenario contains 'scam' → cyber_fraud" is unacceptable because "The shopkeeper
scammed me with fake shoes" is not automatically cyber fraud.

---

## PART 7 — LEGAL KNOWLEDGE BASE

### Core Principle
Legal truth and ML taxonomy are separate concepts and must be stored separately.
Legal knowledge is organized by Act and Section (how law is organized).
Scenario taxonomy is organized by Domain and Issue (how problems are categorized).
The mapping between them (Issue → Provision IDs) is the bridge.

### Three-File Structure (Final Decision)

**File 1: `acts_and_sections.json` — Legal Truth Store**
Answers: "What does Section 66D of the IT Act say?"
Organized by: Act → Section
Contains: Official text, simplified explanation, source metadata, verification block
Modified by: Human curation and verification only
Change rate: Very rare (laws change infrequently)

**File 2: `issue_mappings.json` — Bridge File**
Answers: "For issue 'otp_fraud', which provisions are relevant? What do prototype scenarios look like?"
Contains two things:
1. Prototype texts for each issue (3-5 per issue) — used by Issue Detector
2. Provision references for each issue (act_id + section_id + why_relevant) — used by Legal Intelligence Engine
Change rate: Occasional (as new issues or provisions are added)

**File 3: `issue_actions_portals.json` — Practical Guidance Store**
Answers: "For issue 'otp_fraud', what should the citizen do?"
Contains: Issue-specific action steps, portal definitions with priority and usage conditions
Change rate: More frequent (portal URLs change; steps get refined)

### Why Three Files (Not One)
Updating action steps (lower risk) should not require editing the same file as
verified legal text (highest risk). Each file has a different change rate and
a different risk profile. Keeping them separate isolates changes and reduces
the risk of accidentally corrupting verified legal data.

### Legal Hierarchy (Act-Centric)
```
Acts
  └── Sections
        └── Optional subsection / clause metadata
```
Never organize the legal truth store by ML category. That coupling was the core
problem with the rejected architecture.

### ID and Reference System
Every Act has a stable ID (e.g., `it_act_2000`).
Every section within an Act has a stable ID (e.g., `66d`).
Issue mappings reference these IDs. Legal text is never duplicated across issues.
Reference integrity must be validated: every act_id + section_id pair in
issue_mappings.json must resolve to a real entry in acts_and_sections.json.

---

## PART 8 — LEGAL PROVISION RECORD FORMAT

Every provision stored in acts_and_sections.json must contain:

```json
{
  "section_number": "66D",
  "official_section_title": "Punishment for cheating by personation by using computer resource",
  "official_text": "Full statutory text from India Code...",
  "simplified_explanation": "Plain language explanation for citizens using approved wording only...",
  "applicability_notes": "When does this provision apply — conditions and context",
  "status": "active",
  "verification": {
    "status": "pending_manual_verification",
    "verified_by": null,
    "verified_on": null
  }
}
```

The Act-level record contains:
```json
{
  "official_act_name": "Information Technology Act, 2000",
  "act_year": 2000,
  "short_name": "IT Act 2000",
  "official_source_name": "India Code",
  "official_source_url": "https://indiacode.nic.in/...",
  "sections": { ... }
}
```

### HARD RULE ON VERIFICATION

**Every new provision begins with:**
```json
"verification": {
  "status": "pending_manual_verification",
  "verified_by": null,
  "verified_on": null
}
```

**NO AI ASSISTANT (INCLUDING CLAUDE) MAY CHANGE `verification.status` TO `manually_verified`.**

This is a human-only action. Only a human team member who has physically checked
the provision text against the official India Code publication may change the status:
```json
"verification": {
  "status": "manually_verified",
  "verified_by": "Team member name",
  "verified_on": "YYYY-MM-DD"
}
```

Claude may design the schema, help identify candidate provisions, and draft simplified
explanations. AI-generated content is not manual verification. The field must
intentionally remain `pending_manual_verification` until a human changes it.

---

## PART 9 — LEGAL SOURCE RULES

**Primary source:** India Code (indiacode.nic.in)

**Acceptable additional sources:** Official Central Government ministry, department,
regulator (e.g., Ministry of Labour, RBI, MCA), or statutory authority publications.

**Prohibited sources:**
- AI model memory or training knowledge (including Claude's knowledge)
- Blogs, news articles, or legal commentary websites
- Social media content
- Legal help forums
- Unverified secondary sources of any kind

Every provision in acts_and_sections.json must have `official_source_name` and
`official_source_url`. If the URL is not yet confirmed, set `official_source_url: null`
and keep `verification.status: pending_manual_verification`. Do not use a placeholder URL.

### Wage Law Specific Warning

An earlier prototype used Payment of Wages Act 1936 and Minimum Wages Act 1948
as if they were automatically the current primary wage-law framework for India.

**This must not be blindly reused.**

The Code on Wages 2019 was enacted to consolidate several wage-related Acts.
Before populating any workplace_wage entries:
1. Research the current implementation status of the Code on Wages 2019
2. Determine which provisions are currently in force
3. Determine whether the older Acts have been repealed or remain applicable
4. Document findings and sources in `docs/wage_law_research.md`
5. Only then populate workplace_wage KB entries based on confirmed current law

---

## PART 10 — LEGAL WORDING AND SAFETY RULES

### Prohibited Phrases (Never Use)
- "This law definitely applies to your situation"
- "You can definitely sue"
- "You have a strong case"
- "The employer has committed an offence"
- "The police acted illegally"
- "You will win"
- "You are legally protected"
- "Exact law applicable to your case"

### Approved Phrasing
- "Relevant curated legal provisions"
- "Potentially relevant provisions"
- "Provisions that may apply based on the described scenario"
- "Based on the information you have provided"
- "Why this provision may be relevant to your situation"
- "Legal awareness information"

### Mandatory Disclaimer (Every Single Response, No Exceptions)
```
"This information is for legal awareness only and does not constitute legal advice.
Please consult a qualified legal professional for advice specific to your situation."
```

### Explainability Honesty Rule
Do not claim the project uses SHAP, LIME, or XAI unless those techniques are
actually implemented. Phase 1 "why_relevant" text is curated human-authored rationale
stored in the knowledge base. Call it "curated rationale" or "system reasoning."
Never call it "explainable AI" or "XAI."

---

## PART 11 — LEGAL INTELLIGENCE ENGINE

**Module 3 in the four-module pipeline.**

**Input:** issue_id (string, after domain and issue classification)

**Responsibilities:**
1. Look up issue_id in issue_mappings.json → get list of provision references
2. For each reference: load act + section details from acts_and_sections.json
3. Add why_relevant text from the issue mapping record
4. Look up issue_id in issue_actions_portals.json → get curated action steps
5. Load portal data for portal_ids listed for this issue
6. Filter portals: only return portals where issue_id is in supported_issue_ids
7. Sort portals by priority (immediate → primary → secondary)
8. Return max 3 portals

**Output:** `{ legal_provisions: [...], action_steps: [...], portals: [...] }`

**What it must NOT do:**
- Use any ML model
- Generate any content
- Infer sections from model memory
- Invent Act names, penalties, or procedures
- Make external API calls

**This is what makes the system trustworthy:** Every provision returned was
pre-selected by a human, verified against official sources, and stored in the KB.
No AI generation is involved in the legal content layer.

---

## PART 12 — ACTION STEPS (Issue-Specific)

**Final rule:** Action steps must be issue-specific whenever possible.
Generic category-level steps ("contact the authorities", "save evidence") are insufficient.

**Example of rejected generic steps (cyber_fraud level):**
1. Contact authority
2. Save evidence
3. File complaint

**Example of correct issue-specific steps (otp_fraud):**
1. Contact your bank immediately and report the unauthorised transaction. Ask them to block your account or card.
2. Preserve all evidence: call records, SMS alerts, transaction IDs, screenshots.
3. Report the incident through the official cybercrime reporting portal as soon as possible.
4. Request your bank to initiate the chargeback process for any unauthorised transfer.

**Action steps are stored in `issue_actions_portals.json` mapped to issue IDs.**
The Legal Intelligence Engine retrieves them. An LLM must not freely generate
legally sensitive procedure steps.

**Action step rules:**
- Issue-specific, not domain boilerplate
- Start with the most time-sensitive step
- Maximum 5 steps per issue
- No FIR filing as primary advice (outside Phase 1 scope)
- No criminal procedure steps

---

## PART 13 — PORTAL MAPPING

**Improvement from the earlier architecture:**

Earlier: Issue → simple list of portal IDs

Final: Issue → structured portal mapping with priority and conditions

**Each portal entry must contain:**
```json
{
  "portal_id": "cybercrime_gov_in",
  "name": "National Cyber Crime Reporting Portal",
  "official_url": "https://cybercrime.gov.in",
  "purpose": "File complaints about cybercrime incidents",
  "priority": "immediate",
  "usage_condition": "Use when the incident involves online fraud, impersonation, OTP theft",
  "official_source": "Ministry of Home Affairs, Government of India",
  "supported_issue_ids": ["otp_fraud", "online_impersonation", "phishing", "identity_theft"]
}
```

**Priority values:**
- `immediate` — Contact within 24 hours; time-sensitive (e.g., freeze bank account)
- `primary` — Main formal complaint avenue
- `secondary` — Alternative or supplementary option

**Portal selection logic:** Filter by supported_issue_ids, sort by priority, return max 3.

**Important conditional portal example:**
The RBI Banking Ombudsman portal is relevant for OTP fraud scenarios where a regulated
financial entity is involved and an initial complaint has already been made to the bank.
It should NOT be automatically returned as the first portal for every financial fraud
scenario. It is conditional — add `usage_condition` to reflect this.

**Only official government or regulator portals for complaint filing recommendations.**

---

## PART 14 — RESPONSE CONTRACT

**Desired structured API response:**

```json
{
  "success": true,
  "request_id": "uuid-v4-string",
  "analysis": {
    "domain": {
      "id": "cyber_fraud",
      "display_name": "Cyber Fraud",
      "confidence": 0.91,
      "confidence_label": "High"
    },
    "issue": {
      "id": "otp_fraud",
      "display_name": "OTP / Financial Impersonation Fraud",
      "confidence": 0.88
    },
    "scenario_signals": ["pretending to be bank", "asked for OTP"]
  },
  "legal_provisions": [
    {
      "act_id": "it_act_2000",
      "act": "Information Technology Act, 2000",
      "section": "Section 66D",
      "title": "Punishment for cheating by personation by using computer resource",
      "simplified_explanation": "...",
      "why_relevant": "Your scenario describes a person allegedly pretending to represent a bank through a communication channel...",
      "official_source": {
        "name": "India Code",
        "url": "https://indiacode.nic.in/..."
      }
    }
  ],
  "action_steps": ["...", "...", "..."],
  "portals": [
    {
      "name": "National Cyber Crime Reporting Portal",
      "official_url": "https://cybercrime.gov.in",
      "purpose": "File cybercrime complaints online",
      "priority": "immediate"
    }
  ],
  "low_confidence_warning": false,
  "needs_clarification": false,
  "clarification_question": null,
  "disclaimer": "This information is for legal awareness only and does not constitute legal advice. Please consult a qualified legal professional for advice specific to your situation."
}
```

**Full statutory text must NOT appear in the default response.** Citizens see only the
simplified_explanation. The UI may provide a "View Official Provision" link to the source.

**Confidence label thresholds:**
- High: ≥ 0.80
- Medium: 0.65–0.79
- Low: 0.60–0.64
- Low + warning: < 0.60

---

## PART 15 — LOW CONFIDENCE HANDLING

### Corrected Decision (replaces earlier HTTP 422 behavior)

**WRONG (previous prototype):** Return HTTP 422 when domain confidence < 0.60

**CORRECT:** Return HTTP 200 with warning flags

Low ML confidence is not an HTTP client error. A valid scenario may simply be ambiguous.
Validation errors (empty input, too short, too long, malformed) still use HTTP 400.
Model uncertainty uses HTTP 200 with:

```json
{
  "success": true,
  "low_confidence_warning": true,
  "needs_clarification": true,
  "clarification_question": "Could you describe whether this involved an online transaction, a physical purchase, or a service you paid for?",
  "legal_provisions": [],
  "action_steps": [],
  "portals": [],
  "disclaimer": "..."
}
```

**Future Clarification Question Engine (design must not block this):**
Low confidence → identify source of ambiguity → ask targeted clarification question
→ user provides more context → re-analyze with combined input.
Phase 1 implementation of the question can be simple (domain-keyed static questions).
The API contract must not prevent this from being built later.

---

## PART 16 — DATASET PHILOSOPHY (CRITICAL)

### Rejected Approach (Do Not Revive)
- Generate hundreds of scenarios in bulk before defining the plan
- Treat dataset creation as a one-time task
- Generate near-duplicate examples to hit arbitrary sample count targets
- Evaluate using accuracy alone and declare success at 85%

### Correct Approach (Final Decision)

**Dataset development is iterative and driven by evaluation findings.**

```
Lock domain taxonomy
        ↓
Lock issue taxonomy
        ↓
Confirm in-scope legal provision support for issues
        ↓
Create training_data_plan.md (blueprint — must be approved before CSV generation)
        ↓
Create small Dataset V1 (≈25-30 per domain, ≈125-150 total)
        ↓
Build complete ML training pipeline
        ↓
Train Domain Classifier V1
        ↓
Evaluate: study confusion matrix, identify failure modes
        ↓
Document findings in evaluation_notes.md
        ↓
Improve dataset based on observed failures
        ↓
Create training_data_v2.csv (never overwrite v1)
        ↓
Retrain and compare
        ↓
Repeat until quality targets are met
```

**Dataset versioning rule:** Never overwrite. Use training_data_v1.csv, v2, v3.
This allows reproducing any past training run.

---

## PART 17 — training_data_plan.md (REQUIRED GATE)

This file must be created and approved BEFORE any training CSV is generated.
It is a project governance gate, not a nice-to-have.

**Contents:**
- Final domain taxonomy
- Final issue taxonomy (with all issue IDs)
- Planned sample coverage per issue
- Expected sample counts per domain
- Class balance strategy
- Coverage gap analysis
- Scenario type requirements:
  - Clear standard scenarios (40%)
  - Informal Indian English (20%) — may mix Hindi words, shorter sentences
  - Spelling and grammar variations (15%) — real user input is messy
  - Longer narrative scenarios (15%) — multi-sentence descriptions
  - Cross-domain boundary scenarios (10%) — labeled with correct domain
- Cross-domain confusion pairs to explicitly address:
  - consumer_issues vs contractual_disputes
  - cyber_fraud vs consumer_issues (online shopping fraud boundary)
  - workplace_wage vs contractual_disputes (freelancer vs employee)
- Train / validation / test split strategy (recommended: 70/15/15, stratified)
- Evaluation metrics and success criteria
- Instructions on what NOT to do (no near-duplicate bulk generation)

---

## PART 18 — DATASET V1

Start with approximately 25-30 scenarios per domain (≈125-150 total).
This is not a sacred target — follow the blueprint from training_data_plan.md.

**CSV format:**
```
scenario,domain,issue
"...",cyber_fraud,otp_fraud
```

**Columns:**
- `scenario`: natural language text (20-2000 chars)
- `domain`: one of the five approved domain IDs exactly
- `issue`: one of the approved issue IDs for that domain

**After V1 training, evaluate with:**
- Accuracy (not the only metric)
- Per-class Precision, Recall, F1
- Macro-averaged F1
- Full 5×5 confusion matrix

**Study these specific confusion pairs after every training run:**
- consumer_issues vs contractual_disputes (most expected)
- cyber_fraud vs consumer_issues
- workplace_wage vs contractual_disputes

**Do not add more data until you understand what the confusion matrix shows.**
More data is not always the solution. Better targeted data for observed failure modes is.

---

## PART 19 — EXTERNAL DATASET STRATEGY

A public dataset (e.g., from Kaggle) is not automatically trustworthy just because
it is public. Any external dataset used must go through this process:

1. Identify dataset as potentially relevant (consumer complaints, cyber fraud descriptions, etc.)
2. Extract text that may be relevant to Phase 1 scope
3. Filter to remove out-of-scope content
4. Normalize text format
5. Manually annotate each example to OUR domain taxonomy
6. Manually annotate each example to OUR issue taxonomy
7. Review annotated examples for ambiguity and correctness

A public dataset does NOT need to use our labels. The scenario text may be useful;
the original labels are not relevant to this project.

Controlled synthetic augmentation may be used where coverage remains weak
after real data is exhausted, but:
- Do NOT create hundreds of near-duplicate LLM-generated examples
- Every synthetic example must be reviewed by a human before inclusion
- Synthetic examples should cover specific gaps identified by the confusion matrix

---

## PART 20 — ML PIPELINE BEFORE FINAL DATASET

**Key decision:** The ML pipeline must be built as a complete, working tool
BEFORE the final dataset is ready.

The training script (`train_domain_classifier.py`) must be complete and runnable
on any valid CSV file (even a 10-row test file). This way:
- The pipeline is ready when Dataset V1 is complete
- The same pipeline runs on V2, V3, etc. without changes
- The pipeline and dataset evolve together through evaluation

The training script must implement:
- CSV loading (expects columns: scenario, domain, issue)
- Text preprocessing (identical to inference preprocessing — critical!)
- Stratified train/validation/test split
- TF-IDF vectorizer fitting (on training data only)
- Logistic Regression training
- Evaluation: per-class precision/recall/F1, macro F1, confusion matrix
- Model artifact saving (.pkl files)

**Preprocessing must be identical between training and inference.**
If they differ, the model receives unfamiliar input during inference and performance degrades.

---

## PART 21 — EVALUATION

**Never evaluate using accuracy alone.**

Required metrics after every training run:
- Accuracy
- Per-class Precision
- Per-class Recall
- Per-class F1
- Macro-averaged F1 (most important for balanced multi-class performance)
- Full confusion matrix

**Macro F1 matters** because it weights each class equally regardless of sample count.
If cyber_fraud has 50 examples and traffic_enforcement has 25, accuracy can look
good even if traffic_enforcement is classified poorly. Macro F1 catches this.

**Do not declare success when a hardcoded target like 85% is reached.**
Inspect dataset quality and confusion matrix first. A metric can be reached by
gaming the dataset. A reliable model is understood, not just measured.

**Document every evaluation run in `docs/evaluation_notes.md`** with:
- Which dataset version was used
- Confusion matrix findings
- Which pairs were most confused
- What the findings suggest about dataset improvements
- Decisions made based on findings

---

## PART 22 — PRIVACY AND LOGGING

**Raw scenario text must NOT be stored in query logs.**

Anonymized log record may contain:
- Request UUID
- domain_id (predicted)
- issue_id (predicted, if detected)
- domain_confidence (numeric)
- issue_confidence (numeric, if available)
- language code
- timestamp
- feedback_status (null / helpful / not_helpful)
- Optionally: SHA-256 hash of scenario (for deduplication only)

**Do NOT claim that SHA-256 hashing makes the system "fully anonymous."**
Hashing is a technical measure, not a legal privacy guarantee.
Use the narrower accurate statement: "Raw scenario text is not stored in query logs."

Feedback comments may contain personal information (users describe their situation
to give context with feedback). Store feedback separately. Sanitize before storage.
Do not overclaim legal compliance without proper legal review.

---

## PART 23 — BERT ROLE (PHASE 2)

**Phase 1:** TF-IDF + Logistic Regression for domain classification + prototype similarity for issues

**Phase 2:** Fine-tuned BERT-based classification

BERT replaces or improves the NLP understanding layer (Modules 1 and 2).
It improves classification accuracy, especially for:
- Short or ambiguous scenarios
- Informal Indian English
- Domain boundary cases

**BERT does NOT replace:**
- Legal Knowledge Base
- Issue mappings
- Action step mappings
- Portal mappings
- Legal Intelligence Engine (Module 3)
- Response Builder (Module 4)
- Response schema / API contract

**Why the module separation is essential for BERT migration:**
If Modules 1-2 (ML) and Modules 3-4 (Legal Intelligence) are cleanly separated
with a stable interface between them, swapping TF-IDF for BERT requires changing
only Modules 1 and 2. Everything downstream is unaffected.

**Stable ML output contract (must survive Phase 1 → Phase 2):**
```json
{
  "domain": { "id": "...", "confidence": 0.0, "confidence_label": "..." },
  "issue": { "id": "...", "confidence": 0.0 },
  "scenario_signals": ["..."]
}
```

**Recommended BERT model:** bert-base-uncased (Phase 2, English)
**Phase 3 multilingual:** bert-base-multilingual-cased or IndicBERT

---

## PART 24 — RAG ROLE (PHASE 3)

RAG (Retrieval-Augmented Generation) improves explanation quality.
It is an enhancement, not a dependency. Phase 1 works without RAG.

**RAG conceptual flow:**
```
scenario → domain/issue classification
        → Legal Intelligence Engine retrieves provision IDs
        → retrieve verified legal text chunks from vector store
        → provide retrieved chunks to LLM as grounding context
        → LLM generates simplified explanation based ONLY on retrieved content
        → explanation retains source references from retrieved chunks
```

**RAG must NOT:**
- Select Acts or sections independently
- Invent section numbers, penalties, or legal rights
- Generate action steps (still retrieved from KB)
- Override the Legal Intelligence Engine's provision selection
- Introduce legal content not in the retrieved chunks

Every RAG output must be traceable to retrieved source material.

---

## PART 25 — FRONTEND PHILOSOPHY

The primary UX is **scenario analysis**, not a chatbot.

**Conceptual UI flow:**
```
Scenario Input (text area + analyze button)
        ↓
Domain Result (badge + confidence bar)
        ↓
Detected Issue (issue type + scenario signals)
        ↓
Legal Provisions (1-3 cards, one per provision)
        ↓ (inside each card)
Why This May Be Relevant (curated rationale)
        ↓
Action Steps (issue-specific ordered list)
        ↓
Official Portals (relevant links with priority)
        ↓
Disclaimer (mandatory, always visible)
        ↓ (if low confidence)
Clarification Prompt (targeted question)
```

**Do not overbuild the frontend before the backend response schema is stable.**
Build display components once the API contract is confirmed working.

---

## PART 26 — BEGINNER-FRIENDLY DEVELOPMENT REQUIREMENT

The project owner is new to Machine Learning. For every implementation component,
the Claude assistant must explain:

1. What is being built (plain language)
2. Why this component exists (what problem it solves)
3. What goes in (inputs)
4. What comes out (outputs)
5. Where it sits in the overall architecture
6. What would break or be weaker without this component
7. Then the implementation
8. Explanation of important code decisions after implementation

**Do not hide complexity behind "this is standard boilerplate."**
If a file exists, it must have a documented reason.
If a library is installed, explain why it is required.
If an architectural decision is made, explain the trade-off.

---

## PART 27 — AVOID PREMATURE COMPLEXITY

Phase 1 must remain: **clean, modular, understandable, working, extensible.**

Do not introduce:
- Kafka or message queues
- Kubernetes or container orchestration
- Distributed databases
- Multi-agent AI systems
- Excessive microservice decomposition
- Enterprise-scale abstractions

**Sufficient stack for Phase 1:**
React + Node.js/Express + Python FastAPI + structured JSON knowledge base + MySQL logging

Docker Compose for local development is acceptable and useful.
Add complexity only when a real requirement justifies it.

---

## PART 28 — FINAL PHASE ROADMAP

### Phase 1 — Controlled NLP + Legal Intelligence MVP
- Final domain taxonomy (5 domains)
- Final issue taxonomy (~25 issues)
- Three-file knowledge base schema design
- Verified candidate legal provisions (pending_manual_verification by default)
- Issue-to-provision mappings with why_relevant text
- Issue-specific action step mappings
- Structured portal mappings with priority
- training_data_plan.md (blueprint, approved before data generation)
- Dataset V1 (~125-150 scenarios)
- TF-IDF + Logistic Regression domain classifier
- Issue detector (prototype cosine similarity, Phase 1)
- ML analysis FastAPI service (4 modules)
- Legal Intelligence Engine (KB-only, no ML)
- Response Builder
- Node.js API gateway
- React scenario analysis UI
- Low-confidence HTTP 200 handling
- Clarification-ready response contract
- User feedback mechanism
- Evaluation and confusion matrix iteration
- Complete documentation (all files listed in Part 29)
- Wage law research completed before wage KB populated

### Phase 2 — Transformer and Retrieval Upgrade
- Expand and annotate dataset
- Fine-tune BERT for domain classification
- Optionally fine-tune BERT for issue classification
- Compare TF-IDF + LR vs BERT results
- Preserve ML output contract (interface stability)
- Build verified legal document chunking pipeline
- Generate embeddings for curated legal corpus
- Implement vector retrieval
- Add controlled RAG for grounded explanation generation
- Preserve source references in all RAG outputs
- Evaluate retrieval relevance and explanation grounding

### Phase 3 — Accessibility and Scale
- Hindi language support
- Kannada language support
- Multilingual transformer models (IndicBERT or similar)
- Speech-to-text scenario input
- Accessibility improvements (WCAG 2.1 AA)
- Progressive Web App (offline capability)
- Expand to additional verified legal domains
- Additional curated legal provisions

---

## PART 29 — EXISTING DOCUMENT CONTEXT

### Documents Already Produced (In This Conversation)

**In `/home/claude/legal-docs/` (final session output):**
- `CLAUDE.md` — v3.0, comprehensive master context document
- `ARCHITECTURE_DOCUMENT_v3.md` — Full architecture with diagrams, module responsibilities, request flow, BERT/RAG paths
- `AUDIT_REPORT_v3.md` — Updated audit reflecting all three review rounds, component status table
- `MIGRATION_PLAN_v3.md` — Iterative dataset strategy, pipeline-before-data approach, all 10 phases
- `FILE_RESPONSIBILITY_DOCUMENT.md` — Every file explained: why it exists, inputs, outputs, dependencies
- `FILE_STRUCTURE_v3.md` — Complete directory tree with purpose and status for every file
- `TRAINING_DATA_PLAN.md` — Dataset blueprint document (ready for approval, not yet approved)
- `KB_DESIGN_DOCUMENT.md` — Three-file KB structure rationale, schema, population order, verification workflow
- `FINAL_IMPLEMENTATION_ORDER.md` — Phase 0 through Phase 1E, step-by-step with beginner explanations
- `DEPENDENCY_GRAPH.md` — Component-level and file-level dependency graphs, data flow, BERT migration map
- `ARCHITECTURE_REVIEW_RESPONSE.md` — Point-by-point evaluation of all 15 architectural corrections

**Earlier documents in `/mnt/user-data/outputs/` (earlier session — partially superseded):**
- `AUDIT_REPORT.md` — First audit (superseded by AUDIT_REPORT_v3.md)
- `ARCHITECTURE_PROPOSAL.md` — First architecture proposal (superseded by ARCHITECTURE_DOCUMENT_v3.md)
- `MIGRATION_PLAN.md` — First migration plan (superseded by MIGRATION_PLAN_v3.md)
- `CLAUDE_v2.md` — Second CLAUDE.md version (superseded by v3.0 in legal-docs/)

### Prototype Implementation Files (Earlier Session — NOT Final Architecture)

**In `/mnt/user-data/outputs/legal-awareness-system/ml-service/`:**
- `app/pipeline.py` — **DEPRECATED.** Monolithic pipeline combining all four modules.
  Must be replaced by four separate module files in Phase 1B.
- `app/main.py` — **DEPRECATED.** Uses old pipeline. Must be rewritten to wire four modules.
- `app/schemas.py` — **PARTIALLY REUSABLE.** Update for new response shape.
- `data/legal_knowledge_base.json` — **DEPRECATED.** Single-file KB, contains IPC Section 420
  and Prevention of Corruption Act (both out of scope). Replace with three-file structure.
- `data/training_data.csv` — **PARTIALLY REUSABLE.** Has domain labels only, no issue column.
  Old column name is "category" not "domain". Needs update and diversity improvements.
- `training/train_model.py` — **DEPRECATED.** Replace with train_domain_classifier.py.

**In `/mnt/user-data/outputs/legal-awareness-system/backend/src/`:**
- `app.js` — **PARTIALLY REUSABLE.** Has correct middleware structure. Fix broken
  `require("./knowledge_base_summary.json")` reference. Update logging to include issue_id.

**In `/mnt/user-data/outputs/legal-awareness-system/frontend/src/`:**
- Existing components (ScenarioInput, ResultCard, ActionSteps, etc.) — **PARTIALLY REUSABLE.**
  Update for new response schema (add issue, why_relevant, clarification fields).

---

## PART 30 — MIGRATION CONTEXT

**Migration thinking already established:**

1. Remove out-of-scope legal content (IPC 420, PCA) from any KB files
2. Fix low-confidence HTTP 422 → HTTP 200 with warning flags
3. Restructure the single-file KB into three separate files
4. Write wage_law_research.md before populating workplace_wage provisions
5. Write training_data_plan.md before generating any training CSV
6. Build complete ML pipeline (train script + all four modules) as reusable tools
7. Generate Dataset V1 (~125-150 scenarios) following the approved plan
8. Train Domain Classifier V1, evaluate, study confusion matrix
9. Iterate: improve dataset based on evaluation findings
10. Update backend logging to include issue_id
11. Update frontend only after response schema is stable
12. End-to-end integration testing

**Critical migration rule:** Dataset improvement is an iterative cycle, not one bulk step.
"Improve dataset" means: study confusion matrix → identify specific failure modes →
add targeted scenarios → retrain → compare. Not: add arbitrary numbers of examples.

---

## PART 31 — CURRENT STATE AT HANDOFF

The new Claude conversation should assume:

- Architecture discussion across three review rounds is **complete**
- All architectural decisions documented in this handoff are **final and locked**
- No new architectural review is needed — proceed to documentation finalization
- The ten documentation deliverables requested in the second review prompt are **COMPLETE**
  (all produced in `/home/claude/legal-docs/` during this session — see Part 29)
- Prototype implementation files exist but are **not final architecture** — see Part 29
- No production code should be generated immediately from this handoff
- The immediate task is to confirm the project context, then begin **Phase 0** of the
  implementation order (wage law research, training data plan approval, KB skeleton design)
- The **first actual implementation task** after Phase 0 approval is **Phase 1A.1**:
  creating the three KB file skeletons

**The Issue Detector vectorizer question (Option A vs Option B) was resolved in this session:**
Option B (separate prototype vectorizer) was selected. The new session should confirm
understanding of this decision and implement accordingly.

---

## PART 32 — ROLE OF PROJECT_STATE.md

Alongside this handoff document, a `PROJECT_STATE.md` file is provided.

**Different purposes:**

| Document                     | Purpose                                                         |
|------------------------------|-----------------------------------------------------------------|
| `CLAUDE.md`                  | Permanent architecture, rules, conventions, API contracts       |
| `PROJECT_CONTEXT_HANDOFF.md` | One-time context transfer for new Claude session/account        |
| `PROJECT_STATE.md`           | Living implementation state — updated after every work batch    |

**`PROJECT_STATE.md` must be updated after every meaningful implementation batch.**
A "meaningful batch" is approximately 3-5 related files or one complete component.
Examples: domain classifier implementation, KB restructuring, Legal Intelligence Engine.

**Before continuing in any new Claude conversation:**
1. Read CLAUDE.md
2. Read PROJECT_STATE.md
3. Inspect actual current file tree
4. Compare PROJECT_STATE.md to actual state (do not blindly trust the document)
5. Identify the exact next pending task
6. State what will be created/modified before writing any code

**Never assume a previous Claude session generated files correctly without inspecting them.**
Never regenerate an existing file from memory without first reading the current version.

---

## INSTRUCTIONS FOR THE NEXT CLAUDE SESSION

**Read this entire document before taking any action.**

1. **Treat all decisions in this handoff as final.** Do not re-open architectural questions
   that are documented as resolved. Do not revive deprecated ideas listed in the introduction.

2. **Do not start production implementation immediately.** The immediate task is:
   - Confirm understanding of this context document
   - Read PROJECT_STATE.md to understand current implementation state
   - Inspect any existing files in the repository before modifying or regenerating them
   - Proceed to Phase 0 work (wage law research and training data plan approval)

3. **Do not revive any deprecated architecture.** Specifically, never:
   - Map categories directly to fixed legal sections
   - Include IPC Section 420 under cyber_fraud
   - Include Prevention of Corruption Act under traffic_enforcement
   - Use HTTP 422 for low confidence responses
   - Allow an LLM or AI to mark provisions as `manually_verified`
   - Treat the dataset as a one-time bulk generation task
   - Return "exact laws" as if legal applicability is certain

4. **Handle the Issue Detector vectorizer:** Option B (separate prototype TF-IDF vectorizer
   fit in-memory on issue prototype texts) was selected. The in-memory vectorizer is fit
   at service startup from issue_mappings.json prototype texts. No .pkl file is saved.
   Implement Module 2 accordingly.

5. **Preserve manual legal verification as human-only.** Never change `verification.status`
   to `manually_verified` in any KB file. Always set `pending_manual_verification` as default.

6. **Create training_data_plan.md before any bulk dataset generation.** The plan file
   already exists in `/home/claude/legal-docs/TRAINING_DATA_PLAN.md` and must be
   presented for user approval before Dataset V1 (CSV) is generated.

7. **Use Dataset V1 iteratively.** Train → Evaluate → Study confusion matrix →
   Improve dataset → Retrain. Do not generate hundreds of examples before the first evaluation.

8. **Keep ML pipeline structure complete and independent of dataset size.** The training
   script must work on a 10-row test file or a 150-row V1 file identically.

9. **Wait for explicit user approval before beginning production implementation.**
   After confirming context and showing Phase 0 status, ask for approval to proceed.

10. **For every implementation component: explain before coding.** Why it exists, inputs,
    outputs, architecture role, what breaks without it — then code — then explain important decisions.

11. **Maintain PROJECT_STATE.md.** Update it after every meaningful implementation batch
    of approximately 3-5 related files or one complete component.

12. **Verify existing files before depending on or regenerating them.** Use view/read tools
    to inspect actual current file content before modifying or building on top of any file.
