# LegalLens – Pipeline Module Failure Analysis

**Auditor:** Senior AI Evaluation Engineer & Legal System Architect  
**Evaluation Scope:** Baseline Audit of the Four-Module Processing Pipeline  
**Benchmark:** 150 Ground-Truth Indian Legal Scenarios  
**Date:** October 30, 2026  

---

## 1. Architectural Overview & Failure Pipeline

The LegalLens system processes citizen legal queries through a sequential four-module pipeline:

```
[Citizen Scenario] 
        │
        ▼
┌─────────────────────────────────┐
│ Module 1: Domain Classifier     │ ──> Failure Mode A (Domain Misclassification)
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│ Module 2: Issue Detector        │ ──> Failure Mode B (Issue Prototype Mismatch)
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│ Module 3: Legal Intelligence    │ ──> Failure Mode C (Missing KB Data)
│           Engine                │ ──> Failure Mode D (Incomplete Provision Mapping)
└─────────────────────────────────┘ ──> Failure Mode E (Legal Inapplicability)
        │
        ▼
┌─────────────────────────────────┐
│ Module 4: Response Builder      │ ──> Failure Mode H (Uncertainty & Fallback Errors)
└─────────────────────────────────┘ ──> Failure Mode G (Inadequate Action Guidance)
        │
        ▼
[Structured Response (JSON)]
```

Because the pipeline is strictly feed-forward, an error in an upstream module unconditionally constrains all downstream modules. This analysis provides an exhaustive breakdown of failure modes observed at each module stage during the 150-scenario benchmark.

---

## 2. Module 1: Domain Classifier Failure Analysis

### 2.1 Performance Summary
- **Domain Accuracy:** 94.67% (evaluated) | 84.00% (raw exact-match diagonal)
- **Macro F1:** 0.8756
- **Total Classification Failures (Category A):** 8 cases (5.33%)

### 2.2 Primary Misclassification Patterns

#### Pattern 1: Consumer Protection vs Commercial Contract (B2B Exclusion)
- **Observed in:** CD17 (MSME supplier auto components), CD11 (Partnership fund dispute)
- **Root Cause:** The classifier relies on TF-IDF unigram and bigram features (`vendor`, `supplied`, `invoice`, `defective parts`). When a commercial vendor supplies defective machinery to another company, the classifier predicts `consumer_issues`.
- **Legal Reality:** Under Section 2(7) of the Consumer Protection Act, 2019, a "consumer" explicitly excludes any entity obtaining goods for resale or for any commercial purpose (*Lilavati Kirtilal Mehta Medical Trust v. Unique Shanti Developers, (2020) 2 SCC 265*). Such disputes belong strictly to `contractual_disputes` under the Commercial Courts Act, 2015 and the Indian Contract Act, 1872.

#### Pattern 2: Service Deficiency vs Contractual Breach
- **Observed in:** CI07 (Air conditioner technician Rs 4,500 repair), CI30 (2016 builder apartment delayed possession)
- **Root Cause:** Both scenarios contain language common to breach of agreement (`contracted`, `advance payment`, `breach`, `agreed timeline`). The classifier routes these to `contractual_disputes`.
- **Legal Reality:** An individual consumer hiring an AC technician or buying a residential flat from a real estate builder is legally a consumer under Section 2(7)(ii) of CPA 2019. The failure to perform constitutes "deficiency in service" under Section 2(11).

#### Pattern 3: Financial Dispute vs Cyber Crime Keyword Bias
- **Observed in:** CI09 (Bank deducting unauthorized non-maintenance and SMS charges), CD11 (Partner siphoning firm money to crypto wallet)
- **Root Cause:** Heavy weight on tokens `bank`, `deducted`, `account`, `crypto wallet` pulls the classifier toward `cyber_fraud`.
- **Legal Reality:** CI09 is a banking consumer service deficiency governed by the Consumer Protection Act and the RBI Integrated Ombudsman Scheme, not an unauthorized cyber hack under Section 66 of the IT Act.

#### Pattern 4: Adversarial Prompt Injection / Cross-Domain Distraction
- **Observed in:** CF28 (*"An online scammer hacked my account so traffic police must suspend his driving license"*)
- **Root Cause:** The TF-IDF model gave decisive weight to `traffic police` and `driving license` over `online scammer hacked`, misrouting a cyber fraud complaint to `traffic_enforcement`.

---

## 3. Module 2: Issue Detector Failure Analysis

### 3.1 Performance Summary
- **Issue Detection Accuracy:** 76.33%
- **Total Issue Detection Failures (Category B):** 43 cases (28.67%)
- **Average Prototype Cosine Similarity on True Positives:** 0.584

### 3.2 Primary Failure Modes in Issue Detection

#### 1. Hyper-Specific Prototype Latching
- **Description:** When multiple related issues share high semantic similarity, the cosine similarity argmax often picks a hyper-specific sub-issue instead of the canonical issue.
- **Examples:**
  - `CF01`: User reported phone call OTP extraction. Matched `credit_card_reward_points_expiry_link` (score: 0.512) instead of `otp_fraud`.
  - `CF03`: Fake recruitment firm scam. Matched `overseas_cyber_slave_job_trafficking` (score: 0.498) instead of general `recruitment_job_offer_fraud`.
  - `CF04`: Fake HDFC netbanking link phishing. Matched `fastag_recharge_wallet_phishing` (score: 0.531) instead of `phishing`.
- **Impact:** While the broad domain was correct, the user is presented with slightly misaligned prototype reasoning ("Layer A reasoning").

#### 2. Fine-Grained Traffic Offense Distinction
- **Description:** Traffic scenarios frequently involve multiple concurrent violations (e.g., TE01: speeding + jumping red light + refusing breath test). Module 2 can only emit a single issue ID, leading to the suppression of secondary offenses.

---

## 4. Module 3: Legal Intelligence Engine Failure Analysis

### 4.1 Performance Summary
- **Correct Act Identification:** 55.57%
- **Section Retrieval Precision & Recall:** 53.38%
- **Knowledge Base Gaps (Category C):** 62 cases
- **Incomplete Provision Mappings (Category D):** 58 cases
- **Legal Applicability Accuracy:** 79.97%

### 4.2 Architectural Limitation: Single-Provision / Under-Mapped Determinism

Module 3 uses a deterministic lookup: `issue_id -> [statutory_provisions]`. If the knowledge base maps an issue to only one Act/Section, the engine cannot retrieve other jointly applicable statutes, causing low recall:

#### Case Study 1: Cyber Financial Fraud (Under-Citation of BNS 2023)
- In Indian legal practice, an online financial scam is never prosecuted under the Information Technology Act alone. Police register an FIR invoking:
  - **Section 66C / 66D IT Act, 2000** (Identity theft and cheating by personation via computer); **AND**
  - **Section 318(4) Bharatiya Nyaya Sanhita, 2023** (Cheating and dishonestly inducing delivery of property).
- In the baseline KB, many cyber issues mapped solely to IT Act Section 66D, causing a 50% drop in expected section recall.

#### Case Study 2: Consumer Disputes (Omission of Definitional & Liability Sections)
- For defective consumer goods (e.g., CI01 smartphone defect), filing a complaint under Section 35 of CPA 2019 requires establishing the statutory definition of "defect" under Section 2(10) or "deficiency in service" under Section 2(11), and "product liability" under Section 84.
- In the baseline KB, only Section 35 was returned for numerous issues, missing the substantive rights sections.

#### Case Study 3: Traffic Offenses (Separation of Substantive Section and Penalty Section)
- Under the Motor Vehicles Act, 1988, driving without a helmet is a violation of **Section 129**, punishable under **Section 194D** (fine of Rs 1,000 and 3-month license disqualification).
- If only Section 129 is retrieved, the citizen is informed of the rule but not the statutory penalty.

---

## 5. Module 4: Response Builder & Uncertainty Handling Failure Analysis

### 5.1 Performance Summary
- **Uncertainty & Clarification Accuracy:** 87.20%
- **Official Portal Accuracy:** 98.00%
- **Action Steps Practical Accuracy:** 98.00%
- **Official Citation Verification Rate:** 100.00%
- **Backend / Schema Stability:** 100.00% (Zero HTTP 500 errors)

### 5.2 Failure Modes in Uncertainty Handling (Category H)

#### 1. Incomplete Scenario Over-Confidence
- **Observed in:** 19 cases (e.g., CF23, WW26, CD26)
- **Root Cause:** When an incomplete input contains high-frequency legal terms (e.g., `account`, `overtime`, `invoice`), the classifier confidence exceeds the `0.60` threshold. Consequently, `low_confidence_warning` is False and `needs_clarification` is False, returning full legal provisions on an incomplete scenario.
- **Remedy:** The `scenario_validator.py` must verify minimum entity completeness (e.g., presence of party relationship, temporal anchor, or specific dispute quantum).

#### 2. Historical Law Advisory Absence (Category I)
- **Observed in:** 3 cases (CI30, CD29, CF29)
- **Root Cause:** The pipeline does not inspect incident timestamps to alert the citizen that offenses prior to July 1, 2024 must be filed under the Indian Penal Code, 1860 rather than Bharatiya Nyaya Sanhita, 2023.

---

## 6. Cascading Failure Matrix

The table below illustrates how failures in one module propagate through subsequent modules:

| Root Module Failure | Downstream Consequence in Module 2 | Downstream Consequence in Module 3 | Downstream Consequence in Module 4 | Total Impact |
|:---|:---|:---|:---|:---|
| **Module 1 Error** (e.g. CD17: Commercial dispute predicted as Consumer) | Module 2 searches only `consumer_issues` prototypes | Module 3 retrieves CPA 2019 Section 35 instead of Commercial Courts Act | Response recommends consumer forum (e-Daakhil) which will dismiss with costs | Critical Legal Risk |
| **Module 2 Error** (e.g. CF01: OTP fraud matched as Reward link) | Retrieves narrow prototype rationale | Module 3 still retrieves IT Act 66C/66D | Response provides valid IT Act sections and 1930 portal | Minor Issue Mismatch (High Applicability) |
| **Module 3 Incomplete Mapping** | None (upstream) | Retrieves only 1 of 3 relevant statutory sections | Citizen receives accurate but incomplete legal citations | Moderate Under-Citation |

---

## 7. Actionable Architectural Roadmap (For Stage B)

1. **Module 1 Enhancement:**
   - Incorporate domain boundary rejection rules for B2B commercial transactions and independent contractor consumer service disputes.
2. **Module 2 Clustered Matching:**
   - Implement a two-tiered prototype index: Tier 1 (Parent Issue Cluster) -> Tier 2 (Specific Variant).
3. **Module 3 Multi-Section Expansion:**
   - Enrich `knowledge_base/issue_mappings.json` with compound statutory tuples (e.g., Rule + Penalty, Substantive Right + Enforcement Section).
4. **Module 4 Temporal & Uncertainty Guardrails:**
   - Add regex date detection for pre-July 2024 incidents to append IPC transitional notes automatically.
