# Issue Support Review — 22 Working Issues
# Smart Legal Intelligence System — Taxonomy Governance Gate
# Per CLAUDE.md §6.8 (Issue Admission Test) and §6.10 (Issue-to-Provision Support Gate)

---

> **Status of this document: REVIEW APPROVED BY USER (2026-07-10), with the status
> terminology corrected from `approved` to `taxonomy_supported`.**
> Per-issue `status` values below are the review's findings. The taxonomy as a whole
> remains **WORKING** until explicit user sign-off. No taxonomy change is applied by
> this document — recommendations are recorded only. This document is frozen; modify
> only if a genuine contradiction is discovered.

## 0. Scope and Hard Limits of This Review

**This is a taxonomy-support review, not provision verification.**

- Candidate Acts, sections, and sources named below are **research leads and evidence
  of issue support only**. They are **not** citizen-facing verified legal provisions.
- Nothing in this review sets `verification.status = manually_verified` or finalizes
  `provision_status = in_force`. Those are human-only actions taken later, against
  approved official sources (`CLAUDE.md` §7.5, §7.6).
- **Source caveat:** candidate citations in this review originate from assistant
  knowledge of well-established Indian statutes. Under `CLAUDE.md` §7.6, AI memory is
  a prohibited *source for KB provisions*; here it is used only to name leads that a
  human must confirm against India Code / the named official body before any KB
  population. Every lead is therefore implicitly "pending confirmation."
- The two governance stages are kept separate per `CLAUDE.md` §11:
  - **Issue Support Review** (this document): "Does this issue appear legally
    supportable and useful enough to exist in our controlled taxonomy?"
  - **Manual Provision Verification** (later, human-only): "Has this exact
    Act/section/source/status/text been checked against an approved official source?"

**Status vocabulary (only these):** `working` / `provision_research_required` /
`taxonomy_supported` / `rejected` / `merged`.
- `taxonomy_supported` means: passes the five-point admission test with reasonable
  official-source leads for provision support. **It is a review finding, not final
  approval** — the taxonomy as a whole remains WORKING until explicit user sign-off,
  and every provision lead still requires later human manual verification.
- `provision_research_required` means: the issue is admissible as a scenario type, but
  its provision support cannot be responsibly pinned down without targeted
  official-source research; it must not be used for KB population until that research
  completes.

**Admission test applied to every issue (`CLAUDE.md` §6.8):**
1. Distinct real-life scenario type?
2. Module 2 can distinguish it from siblings via prototype similarity matching?
3. Reasonable official-source evidence of relevant provision support?
4. Meaningfully different action guidance or portal conditions?
5. Inside the non-criminal Phase 1 scope?

**Scope note applying to the whole `cyber_fraud` domain:** IT Act 2000 provisions such
as 66C/66D are penal in character. `CLAUDE.md` §3.1 names the IT Act 2000 as the
approved Phase 1 framework for `cyber_fraud`; the Phase 1 criminal-law exclusion (§3.3)
targets IPC/BNS, CrPC/BNSS, and the Prevention of Corruption Act specifically. This
review follows §3.1. Awareness framing (not prosecution guidance) keeps these issues
inside the project motto.

---

## 1. Domain: `cyber_fraud` (6 issues)

### 1.1 `otp_fraud`

- **issue_id:** `otp_fraud` | **domain_id:** `cyber_fraud`
- **scenario_definition:** Citizen is manipulated — typically by a caller or message
  impersonating a bank, wallet, or official — into revealing an OTP, PIN, or banking
  credential, followed by (or aimed at) an unauthorized financial transaction.
- **sibling_boundary:** vs `online_impersonation` — impersonation used *as the means to
  extract an OTP/credential toward a financial transaction* belongs here; impersonation
  without the credential-extraction/transaction core belongs there. vs `phishing` —
  phishing's instrument is a fake link/page; OTP fraud's instrument is direct social
  engineering over call/SMS.
- **candidate_official_legal_source:** India Code — Information Technology Act 2000,
  §66C (identity theft: fraudulent use of password/electronic signature/unique
  identification), §66D (cheating by personation using computer resource). Regulator:
  RBI circular on Limited Liability of Customers in Unauthorised Electronic Banking
  Transactions (customer-liability protection).
- **candidate_provision_support:** Strong — §66C/§66D map directly; the RBI circular
  grounds bank-liability awareness. All pending human confirmation.
- **expected_action_difference:** Highly time-critical and unique: contact bank
  immediately to block card/account, request chargeback/reversal, report via national
  cybercrime channels. Distinct from all siblings.
- **admission_test:** 1 ✅ distinct; 2 ✅ OTP/bank/transaction vocabulary is
  prototype-separable; 3 ✅ strong leads; 4 ✅ unique urgency profile; 5 ✅ per §3.1
  framework note above.
- **status:** **taxonomy_supported**

### 1.2 `online_impersonation`

- **issue_id:** `online_impersonation` | **domain_id:** `cyber_fraud`
- **scenario_definition:** Someone poses online (or via phone/digital channel) as a
  real person, official, or organization — fake profile, fake officer call, spoofed
  business identity — to deceive, intimidate, or defraud, where the scenario does not
  center on OTP extraction or a fake login page.
- **sibling_boundary:** vs `otp_fraud` — see 1.1. vs `phishing` — no fake
  site/link; the *identity itself* is the instrument. vs `identity_theft` — there,
  the citizen's *own* identity is misused by someone else; here, someone pretends to
  be *another party or authority* toward the citizen.
- **candidate_official_legal_source:** India Code — IT Act 2000 §66D; §66C where
  credentials are also misused.
- **candidate_provision_support:** Strong — §66D is squarely about cheating by
  personation using a computer resource. Pending confirmation.
- **expected_action_difference:** Evidence preservation (profiles, numbers,
  screenshots), platform-level reporting, cybercrime portal; banking urgency only if
  money moved (then routes toward `otp_fraud`-style steps).
- **admission_test:** 1 ✅; 2 ✅ (fake-identity vocabulary vs OTP/link vocabulary);
  3 ✅; 4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 1.3 `phishing`

- **issue_id:** `phishing` | **domain_id:** `cyber_fraud`
- **scenario_definition:** Citizen receives fake links, websites, login pages, emails,
  or SMS engineered to harvest credentials or payments (fake bank page, fake KYC-update
  link, fake delivery-fee page).
- **sibling_boundary:** Instrument test — a fabricated digital artifact (link/page/
  email) defines phishing. If the artifact leads to OTP capture plus a transaction,
  prototype wording decides: fake-link/page vocabulary → `phishing`; call-based OTP
  extraction → `otp_fraud`. vs `online_impersonation` — a fake page is not a personal
  identity performance.
- **candidate_official_legal_source:** India Code — IT Act 2000 §66C, §66D. Statutory
  authority: CERT-In (constituted under IT Act §70B) advisories as official technical
  guidance.
- **candidate_provision_support:** Strong. Pending confirmation.
- **expected_action_difference:** Do-not-click/credential-reset guidance, bank
  notification if credentials entered, reporting including CERT-In/cybercrime channels.
- **admission_test:** 1 ✅; 2 ✅; 3 ✅; 4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 1.4 `identity_theft`

- **issue_id:** `identity_theft` | **domain_id:** `cyber_fraud`
- **scenario_definition:** The citizen's identity documents or identifiers (Aadhaar,
  PAN, photographs, credentials) are misused by another person — e.g. loans, SIM cards,
  or accounts opened in the citizen's name.
- **sibling_boundary:** vs `otp_fraud` — no tricked transaction; the harm is identity
  replication/misuse. vs `unauthorized_account_access` — takeover of an *existing*
  account vs misuse of identity to create/obtain *new* instruments.
- **candidate_official_legal_source:** India Code — IT Act 2000 §66C. Statutory
  authority: UIDAI grievance/biometric-lock mechanisms; DoT's TAFCOP portal
  (SIM-connections check) as official portals.
- **candidate_provision_support:** Strong — §66C is the direct anchor. Pending
  confirmation.
- **expected_action_difference:** Issuer-side actions (UIDAI biometric lock, credit
  bureau report check, SIM audit via TAFCOP) — a portal set unlike any sibling.
- **admission_test:** 1 ✅; 2 ✅; 3 ✅; 4 ✅ strongly; 5 ✅.
- **status:** **taxonomy_supported**

### 1.5 `other_online_financial_fraud`

- **issue_id:** `other_online_financial_fraud` | **domain_id:** `cyber_fraud`
- **scenario_definition (positive definition, not a fallback):** An online scheme
  soliciting payments or investments through deception — fake investment/trading
  platforms, advance-fee or "processing fee" frauds, fraudulent work-from-home/task
  schemes — where the deception is the scheme itself rather than OTP capture, a fake
  login page, personation of a known entity, identity replication, or account takeover.
- **catch-all check (explicit):** The issue is bounded by its **positive** definition
  above. Prototypes must describe concrete scheme patterns (investment app that blocks
  withdrawal, fee demanded to "release" winnings/job). A scenario with low similarity
  to *all* issues must take the clarification/uncertain path (`CLAUDE.md` §8.2) — it
  must **never** default into this issue. With that guardrail recorded, the issue is
  currently **controlled, not a catch-all**. This guardrail must be re-checked at
  prototype curation and at every evaluation cycle.
- **sibling_boundary:** Defined by exclusion *plus* positive scheme vocabulary
  (investment, returns, fee, task, withdrawal blocked) — separable from OTP/link/
  identity vocabulary of siblings.
- **candidate_official_legal_source:** India Code — IT Act 2000 §66D (lead); Banning of
  Unregulated Deposit Schemes Act 2019 (for deposit-taking schemes); RBI/SEBI investor
  cautions and registered-entity lists (regulator sources).
- **candidate_provision_support:** **Partial and heterogeneous** — the candidate set
  spans IT Act / BUDS Act / financial-regulator territory depending on scheme type.
  A small, stable provision set for Phase 1 has not been responsibly pinned down and
  needs targeted official-source research.
- **expected_action_difference:** Stop further payments, verify entity against RBI/SEBI
  registration lists, bank + cybercrime reporting.
- **admission_test:** 1 ✅ (real, common scheme types); 2 ✅ with the guardrail; 3 ⚠️
  leads exist but heterogeneous; 4 ✅; 5 ✅.
- **status:** **provision_research_required**

### 1.6 `unauthorized_account_access`

- **issue_id:** `unauthorized_account_access` | **domain_id:** `cyber_fraud`
- **scenario_definition:** The citizen's existing email, social media, or financial
  account is accessed/taken over without authorization — password changed, locked out,
  account misused.
- **sibling_boundary:** vs `identity_theft` — takeover of an existing account vs
  identity replication elsewhere. vs `phishing` — phishing is a *method*; this issue is
  the resulting-state scenario where access itself is the core harm reported.
- **candidate_official_legal_source:** India Code — IT Act 2000 §43 (penalty and
  **compensation** for unauthorized access — a civil-compensation provision, a notably
  good fit for awareness scope), §66 (computer-related offences).
- **candidate_provision_support:** Strong — §43's compensation framing is directly
  usable for non-criminal awareness. Pending confirmation.
- **expected_action_difference:** Account-recovery flows, platform reporting, evidence
  of takeover, cybercrime portal.
- **admission_test:** 1 ✅; 2 ✅; 3 ✅; 4 ✅; 5 ✅ (§43 is civil in nature).
- **status:** **taxonomy_supported**

---

## 2. Domain: `consumer_issues` (5 issues)

All five anchor on the Consumer Protection Act 2019 (India Code) — a single coherent
statute, which strengthens provision support but concentrates boundary risk inside the
domain (see 2.3/2.5 boundary flag).

### 2.1 `defective_product`

- **issue_id:** `defective_product` | **domain_id:** `consumer_issues`
- **scenario_definition:** Purchased goods are broken, faulty, or materially not as
  specified (dead-on-arrival phone, counterfeit shoes sold as genuine, appliance
  failing within days).
- **sibling_boundary:** vs `refund_denial` — here the *product's condition* is the
  core; there the *seller's refusal to honor a refund* is the core (a defective product
  followed by refund refusal can appear in either; prototype rule: dominant complaint
  wins). vs `misleading_advertisement` — product materially differs from *advertised
  claims* → there; product simply broken → here.
- **candidate_official_legal_source:** India Code — Consumer Protection Act 2019:
  §2(10) ("defect" definition), Chapter VI product liability (§82–§87), §35 (complaint
  to District Commission). Official portals: e-daakhil (online consumer complaint
  filing), National Consumer Helpline 1915 (DoCA).
- **candidate_provision_support:** Strong. Pending confirmation.
- **expected_action_difference:** Warranty/seller remedy first, documented demand, then
  e-daakhil/District Commission route.
- **admission_test:** 1 ✅; 2 ✅; 3 ✅; 4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 2.2 `refund_denial`

- **issue_id:** `refund_denial` | **domain_id:** `consumer_issues`
- **scenario_definition:** Seller/platform refuses a refund the citizen is entitled to
  under the stated policy, promise, or circumstances (return window ignored, "no
  refund" imposed after payment, cancelled service not refunded).
- **sibling_boundary:** See 2.1. vs `service_deficiency` — refusal to return money vs
  quality/non-delivery of the service itself.
- **candidate_official_legal_source:** India Code — CPA 2019 §2(47) (unfair trade
  practice — includes, per its clauses, failure to return consideration where required;
  exact clause to be confirmed during verification), §2(9) (consumer rights), §35.
- **candidate_provision_support:** Good — the UTP definition's refund-related clause is
  the direct lead; the exact sub-clause number must be confirmed against India Code.
- **expected_action_difference:** Written refund demand with deadline, platform
  grievance officer, NCH 1915, e-daakhil.
- **admission_test:** 1 ✅; 2 ✅ (refund/return vocabulary is distinctive); 3 ✅;
  4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 2.3 `misleading_advertisement`

- **issue_id:** `misleading_advertisement` | **domain_id:** `consumer_issues`
- **scenario_definition:** A purchase influenced by false product claims, fake
  discounts, or misrepresentation *in advertising or promotional claims*.
- **sibling_boundary (boundary flag — see 2.5):** Statutorily, misleading
  advertisement is closely intertwined with unfair trade practice in CPA 2019. The
  operational boundary is: deception located in the **advertisement/claim** itself →
  here; deceptive conduct **at or around the transaction** (fake billing, warranty
  denial tactics, bait-and-switch at sale) → `unfair_trade_practice`. This boundary is
  prototype-enforced, not statute-enforced.
- **candidate_official_legal_source:** India Code — CPA 2019 §2(28) ("misleading
  advertisement" definition), §21 (CCPA powers against false/misleading ads). CCPA
  Guidelines for Prevention of Misleading Advertisements 2022 (official DoCA source).
- **candidate_provision_support:** Strong — a dedicated statutory definition plus a
  dedicated regulator power. Pending confirmation.
- **expected_action_difference:** Evidence of the ad/claim, CCPA complaint route in
  addition to standard consumer remedies — a portal condition siblings don't share.
- **admission_test:** 1 ✅; 2 ⚠️ separable but only with carefully differentiated
  prototypes (see flag); 3 ✅; 4 ✅ (CCPA route); 5 ✅.
- **status:** **taxonomy_supported** (with recorded boundary caution against 2.5)

### 2.4 `service_deficiency`

- **issue_id:** `service_deficiency` | **domain_id:** `consumer_issues`
- **scenario_definition:** A paid service is not delivered, or delivered materially
  below the promised standard (coaching classes stopped mid-course, botched repair,
  event services not provided as agreed).
- **sibling_boundary:** vs `refund_denial` — see 2.2. Cross-domain vs
  `breach_of_contract`: consumer-context service for personal use → here; negotiated
  commercial/business agreement or non-consumer relationship → `contractual_disputes`.
  This is one of the three known cross-domain confusion pairs
  (`TRAINING_DATA_PLAN.md` §9) — boundary examples required in Dataset V1.
- **candidate_official_legal_source:** India Code — CPA 2019 §2(11) ("deficiency"
  definition), §2(42) ("service"), §35.
- **candidate_provision_support:** Strong. Pending confirmation.
- **expected_action_difference:** Service-provider grievance first, documented
  deficiency evidence, consumer forum route.
- **admission_test:** 1 ✅; 2 ✅; 3 ✅; 4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 2.5 `unfair_trade_practice`

- **issue_id:** `unfair_trade_practice` | **domain_id:** `consumer_issues`
- **scenario_definition:** Deceptive commercial practice at or around the sale that is
  not primarily an advertising claim and not a product defect — false warranty
  promises, bait-and-switch at the counter, charging above MRP, fake or inflated
  billing, refusal to issue a bill.
- **sibling_boundary (weak — flagged):** CPA 2019 §2(47) is broad, and misleading
  advertisement is effectively a subset of unfair trade practice in the statute. The
  taxonomy keeps them separate because the *scenario experiences* differ ("the ad lied
  to me" vs "the shop cheated me at the counter") and the action/portal routes differ
  (CCPA ad-complaint route vs standard consumer remedies). **Risk recorded:** if
  prototype curation or Dataset V1 evaluation shows Module 2 cannot separate 2.3 and
  2.5, the merge of `misleading_advertisement` into `unfair_trade_practice` is the
  designated fallback — decision deferred to evaluation, not applied now.
- **candidate_official_legal_source:** India Code — CPA 2019 §2(47), §35.
- **candidate_provision_support:** Strong (same statute). Pending confirmation.
- **expected_action_difference:** Bill/MRP evidence, Legal Metrology angle for
  MRP-overcharging (Legal Metrology Act 2009 as a research lead), consumer forum.
- **admission_test:** 1 ✅; 2 ⚠️ (see flag); 3 ✅; 4 ✅ (moderately); 5 ✅.
- **status:** **taxonomy_supported** (with recorded boundary caution against 2.3)

---

## 3. Domain: `traffic_enforcement` (5 issues)

### 3.1 `bribe_demand`

- **issue_id:** `bribe_demand` | **domain_id:** `traffic_enforcement`
- **scenario_definition:** An enforcement officer demands an informal cash payment in
  lieu of, or alongside, formal enforcement ("pay me here and no challan").
- **sibling_boundary:** vs `wrongful_challan` — no formal challan is at issue; the
  demand for unofficial payment is the scenario core.
- **candidate_official_legal_source (problem case):** The direct legal
  characterization of bribery is the **Prevention of Corruption Act — explicitly
  banned from Phase 1** (`CLAUDE.md` §3.3). Non-criminal candidate angle: Motor
  Vehicles Act 1988 §200 (compounding of offences — official payment routes), the
  e-challan system and receipt requirements (MoRTH/state rules), and official state
  transport / vigilance grievance channels as portals.
- **candidate_provision_support:** **Weak within Phase 1 scope.** Awareness can be
  framed as "you are entitled to an official challan/receipt and official payment
  channels" (MV Act §200 + e-challan procedure leads), but no in-scope provision
  directly addresses the bribe demand itself without entering PCA territory.
- **expected_action_difference:** Distinct — insist on official challan/receipt,
  decline unofficial payment, state transport/vigilance grievance routes.
- **admission_test:** 1 ✅ (very real scenario type); 2 ✅ (cash/no-receipt vocabulary
  separable); 3 ❌ not yet within scope constraints; 4 ✅; 5 ⚠️ only under the
  payment-procedure framing.
- **status:** **provision_research_required**
- **Recorded conditional recommendation (not applied):** if targeted research cannot
  establish adequate non-criminal provision support, either (a) reframe the issue as
  `on_spot_payment_without_official_challan` (a payment-procedure dispute anchored on
  MV Act §200 / e-challan procedure), or (b) reject it from Phase 1. Decision belongs
  to the user after research.

### 3.2 `wrongful_challan`

- **issue_id:** `wrongful_challan` | **domain_id:** `traffic_enforcement`
- **scenario_definition:** A fine/challan issued incorrectly — wrong vehicle or person,
  offence not committed, duplicate challan, grossly wrong amount.
- **sibling_boundary:** vs `vehicle_detention` — paper/electronic fine vs physical
  custody of the vehicle (clean boundary). vs `bribe_demand` — a formal (if wrong)
  challan exists here.
- **candidate_official_legal_source:** India Code — MV Act 1988 penalty/adjudication
  chapter (Chapter XIII), §200 (option to compound vs contest before court). Official
  portal: echallan.parivahan.gov.in grievance route (MoRTH/NIC).
- **candidate_provision_support:** **Moderate but diffuse** — the citizen's concrete
  "right to contest" pathway (grievance vs court appearance, timelines, consequences of
  non-payment) spans MV Act procedure and state e-challan rules; the specific section
  mapping needs targeted research before KB population.
- **expected_action_difference:** Verify challan details online, portal grievance,
  contest-vs-compound decision — unique guidance.
- **admission_test:** 1 ✅; 2 ✅; 3 ⚠️ leads exist, mapping diffuse; 4 ✅; 5 ✅.
- **status:** **provision_research_required**

### 3.3 `document_acceptance_or_verification`

- **issue_id:** `document_acceptance_or_verification` | **domain_id:** `traffic_enforcement`
- **scenario_definition:** A dispute over whether a licence, RC, insurance record,
  DigiLocker document, or mParivahan record is accepted or considered valid during
  enforcement/verification (officer refuses digital documents; disputes validity of a
  document the citizen holds).
- **sibling_boundary:** vs `document_seizure_or_retention` — here the document
  **remains with the citizen** and its *validity/acceptance* is disputed; there the
  authority **physically takes/retains** it (clean, prototype-separable boundary).
- **candidate_official_legal_source:** India Code — MV Act 1988 §130 (duty to produce
  licence and registration); Central Motor Vehicles Rules 1989 Rule 139 (time window to
  produce documents); IT Act 2000 §4 (legal recognition of electronic records); MoRTH
  advisory recognizing DigiLocker/mParivahan-held documents as valid (official ministry
  source).
- **candidate_provision_support:** Strong — statutory production duty + rules window +
  electronic-record recognition + ministry advisory. Pending confirmation.
- **expected_action_difference:** Cite digital-document validity, produce within the
  allowed window, state transport department grievance.
- **admission_test:** 1 ✅; 2 ✅; 3 ✅; 4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 3.4 `document_seizure_or_retention`

- **issue_id:** `document_seizure_or_retention` | **domain_id:** `traffic_enforcement`
- **scenario_definition:** An enforcement authority takes, seizes, or retains a
  licence, RC, or other traffic document, and the citizen questions the authority,
  basis, or procedure for the retention.
- **sibling_boundary:** See 3.3. vs `vehicle_detention` — document custody vs vehicle
  custody (clean).
- **candidate_official_legal_source:** India Code — MV Act 1988 §206 (power to impound
  documents; conditions; temporary acknowledgment/receipt in lieu of seized document).
- **candidate_provision_support:** Strong — §206 is a direct statutory anchor for
  exactly this scenario. Pending confirmation.
- **expected_action_difference:** Demand the seizure acknowledgment/receipt, understand
  the stated ground, return/retrieval procedure, transport authority grievance.
- **admission_test:** 1 ✅; 2 ✅; 3 ✅; 4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 3.5 `vehicle_detention`

- **issue_id:** `vehicle_detention` | **domain_id:** `traffic_enforcement`
- **scenario_definition:** The citizen's vehicle is detained/impounded and the citizen
  questions the basis or procedure (detention for alleged no-registration/permit/
  licence, prolonged retention, unclear release process).
- **sibling_boundary:** vs `wrongful_challan` and `document_seizure_or_retention` —
  clean boundaries (physical vehicle custody is the defining element).
- **candidate_official_legal_source:** India Code — MV Act 1988 §207 (power to detain
  vehicles used without registration/permit or by unlicensed drivers; release
  procedure).
- **candidate_provision_support:** Strong — §207 is the direct anchor. Pending
  confirmation.
- **expected_action_difference:** Ascertain the stated statutory ground, release
  procedure and applicable fees/receipts, grievance escalation.
- **admission_test:** 1 ✅; 2 ✅; 3 ✅; 4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 3.6 Research finding — physical vehicle control / key removal (no issue added)

The project's motivating bike-key example was assessed as instructed. Within the
approved official-source categories, **no MV Act 1988 provision was identified that
authorizes or specifically regulates removal of a vehicle's keys by enforcement
personnel.** The statutory powers located in this review are §206 (documents) and §207
(vehicle detention), both with defined procedure. Judicial observations on
key-snatching exist in case law and news reporting — **both outside this project's
approved source categories.** Conclusion: credible official-source support for a
distinct `bike_key_removal` issue is **not established**; the issue is **not added**
(consistent with `TRAINING_DATA_PLAN.md` §2.1). Scenarios describing key removal
alongside effective detention of the vehicle can route to `vehicle_detention`
prototypes. Revisit only through dedicated official-source research.

---

## 4. Domain: `workplace_wage` (4 issues)

### 4.0 Domain-level finding — wage-law transition (applies to all four issues)

The Code on Wages 2019 was enacted to consolidate the Payment of Wages Act 1936, the
Minimum Wages Act 1948, and related statutes. **The commencement status of its
substantive provisions, and therefore which statute currently governs each wage
scenario, is exactly the unresolved question that `docs/wage_law_research.md` exists to
answer — and that research has not been performed** (`CLAUDE.md` §3.1 wage rule).
Per instruction, this review does **not** perform that research and does **not** force
approval. All four issues therefore receive `provision_research_required`: they are
admissible as scenario types (findings below), but no wage provision may be pinned for
KB population until the wage-law research completes. Candidate sources below are
dual-tracked (older Act / Code on Wages) purely as research leads.

### 4.1 `delayed_wages`

- **issue_id:** `delayed_wages` | **domain_id:** `workplace_wage`
- **scenario_definition:** An employed citizen's wages are acknowledged but paid late
  or remain pending ("salary for last month still not credited," recurring late
  payment), employment relationship continuing.
- **sibling_boundary (weak-to-moderate — flagged):** vs `unpaid_wages` — the intended
  boundary is temporal/intent: *late or pending with an ongoing employer relationship*
  here, vs *withheld entirely / refusal / employer absconded / final dues after exit*
  there. Real user text is often indeterminate ("company saying wait from 2 months").
  **Recorded merge watch:** if the wage-law research shows the statutory remedy and
  authority are identical for both, and prototype evaluation cannot separate them, the
  designated fallback is merging both into a single `wage_nonpayment` issue. Decision
  deferred — not applied.
- **candidate_official_legal_source (leads only):** Payment of Wages Act 1936 §5 (time
  of payment) / Code on Wages 2019 §17 (time limit for payment of wages) — which
  governs is the research question. Ministry of Labour & Employment and Chief Labour
  Commissioner (Central) channels; Samadhan portal as an official grievance lead.
- **candidate_provision_support:** Cannot be responsibly established pre-research.
- **expected_action_difference:** Written demand to employer, labour authority
  complaint route (post-research specificity).
- **admission_test:** 1 ✅; 2 ⚠️ (boundary flag); 3 ⏳ pending research; 4 ⚠️ likely
  shared with 4.2; 5 ✅.
- **status:** **provision_research_required**

### 4.2 `unpaid_wages`

- **issue_id:** `unpaid_wages` | **domain_id:** `workplace_wage`
- **scenario_definition:** Wages withheld entirely — employer refuses to pay, has
  absconded, or final dues/settlement after leaving employment are denied.
- **sibling_boundary:** See 4.1 (flagged pair). vs `unauthorized_deduction` — nothing
  paid vs paid-but-cut (clean).
- **candidate_official_legal_source (leads only):** Payment of Wages Act 1936 §15
  (claims authority) / Code on Wages 2019 §45 (claims) — dual-tracked pending research.
- **candidate_provision_support:** Pending research.
- **expected_action_difference:** Claims-authority route, potentially different limits/
  timelines than delay cases (research to confirm whether genuinely different from 4.1).
- **admission_test:** 1 ✅; 2 ⚠️; 3 ⏳; 4 ⚠️; 5 ✅.
- **status:** **provision_research_required**

### 4.3 `unauthorized_deduction`

- **issue_id:** `unauthorized_deduction` | **domain_id:** `workplace_wage`
- **scenario_definition:** Employer deducts amounts from salary without legal basis or
  consent — arbitrary fines, "breakage" charges, unexplained cuts.
- **sibling_boundary:** Clean — payment happened but was reduced; distinct from both
  non-payment issues and from rate-level violation (4.4).
- **candidate_official_legal_source (leads only):** Payment of Wages Act 1936 §7
  (authorized deductions — exhaustive list) / Code on Wages 2019 §18 — dual-tracked.
- **candidate_provision_support:** Pending research (the lead is strong in either
  statute; which governs is the open question).
- **expected_action_difference:** Demand deduction breakdown/payslip, challenge
  specific deduction, labour authority route.
- **admission_test:** 1 ✅; 2 ✅ (deduction vocabulary distinctive); 3 ⏳; 4 ✅; 5 ✅.
- **status:** **provision_research_required**

### 4.4 `minimum_wage_violation`

- **issue_id:** `minimum_wage_violation` | **domain_id:** `workplace_wage`
- **scenario_definition:** Citizen paid below the statutory minimum wage for their
  region/category of work.
- **sibling_boundary:** Clean — a *rate-level* violation (how much per day/month is
  lawful) vs payment-timing/withholding issues.
- **candidate_official_legal_source (leads only):** Minimum Wages Act 1948 / Code on
  Wages 2019 §§5–9 (minimum wage fixation and obligation) — dual-tracked; state
  minimum-wage notifications (official state government sources) will matter.
- **candidate_provision_support:** Pending research.
- **expected_action_difference:** Identify applicable notified rate, labour
  inspector/claims route.
- **admission_test:** 1 ✅; 2 ✅ ("less than minimum wage" vocabulary distinctive);
  3 ⏳; 4 ✅; 5 ✅.
- **status:** **provision_research_required**

---

## 5. Domain: `contractual_disputes` (2 issues)

### 5.1 `breach_of_contract`

- **issue_id:** `breach_of_contract` | **domain_id:** `contractual_disputes`
- **scenario_definition:** A party fails to perform, or violates, an agreed contractual
  obligation — non-delivery under an agreement, abandonment of agreed work, refusal to
  perform, materially substandard performance of a negotiated (non-consumer-context)
  agreement.
- **breadth assessment (explicit, as instructed):** This is deliberately the broad
  Phase 1 bucket after `non_performance` was merged in. **Assessed as acceptably broad
  for Phase 1**, because across its subtypes (non-delivery, repudiation, defective
  performance) the candidate provision set is shared (ICA §37/§39/§73/§74) and the
  Phase 1 action guidance is shared (document the agreement and breach → formal written
  notice → negotiate/escalate → civil remedy awareness). Under `CLAUDE.md` §6.8, a
  subdivision is justified only when provision mappings or action guidance genuinely
  diverge — currently they do not. **Watch item:** if Dataset V1 shows this single
  issue absorbing highly heterogeneous scenarios with diverging guidance needs,
  subdivision candidates (e.g. money-owed-under-agreement vs work-not-done) should be
  proposed through the admission test — not applied now.
- **sibling_boundary:** vs `security_deposit_dispute` — deposit return after the
  agreement ends vs performance failure during the agreement (clean). Cross-domain vs
  `service_deficiency` and `workplace_wage` — the two known confusion pairs
  (`TRAINING_DATA_PLAN.md` §9): consumer-context service → consumer domain; employee
  wages → wage domain; freelancer/business agreement → here.
- **candidate_official_legal_source:** India Code — Indian Contract Act 1872: §37
  (obligation to perform), §39 (effect of refusal to perform), §73 (compensation for
  loss caused by breach), §74 (compensation for breach where penalty stipulated).
  Specific Relief Act 1963 §10 (specific performance) as a supplementary lead.
- **candidate_provision_support:** Strong — the ICA remedy core is stable and directly
  on-point. Pending confirmation.
- **expected_action_difference:** Notice-and-negotiate first, evidence of agreement and
  breach, civil remedy awareness (damages/specific performance) — distinct from
  consumer-forum routes.
- **admission_test:** 1 ✅; 2 ✅ (agreement/contract vocabulary anchors the domain
  boundary); 3 ✅; 4 ✅; 5 ✅.
- **status:** **taxonomy_supported**

### 5.2 `security_deposit_dispute`

- **issue_id:** `security_deposit_dispute` | **domain_id:** `contractual_disputes`
- **scenario_definition:** A security deposit — typically rental housing, also service
  or equipment deposits — is not returned after the agreement ends despite the citizen
  meeting the agreed conditions.
- **sibling_boundary:** See 5.1 (clean vs breach). The scenario type is highly
  recognizable in real life and its vocabulary (deposit, landlord, vacate, refund of
  deposit) is prototype-separable.
- **candidate_official_legal_source:** India Code — Indian Contract Act 1872 §73 (the
  general anchor). Tenancy-specific layer: Model Tenancy Act 2021 (deposit caps and
  return timelines; **adoption varies state-by-state**) and state Rent Acts / state
  rent authorities — official sources, but jurisdiction-dependent.
- **candidate_provision_support:** **Split finding.** The general ICA §73 anchor
  duplicates 5.1's provision set — on provisions alone this issue would not clearly
  pass admission test 3 (meaningfully *specific* retrieval). Its distinct value rests
  on the tenancy-specific layer (Model Tenancy Act / state rent authority routes),
  whose current applicability by state needs targeted research before the issue's
  provision mapping can be responsibly written.
- **expected_action_difference:** **Strongly distinct** — written demand referencing
  the agreement's deposit clause, rent-authority/tenancy routes where available,
  evidence of handover condition. This is the issue's strongest admission argument.
- **admission_test:** 1 ✅ strongly; 2 ✅; 3 ⚠️ generic anchor shared with 5.1,
  specific layer needs research; 4 ✅ strongly; 5 ✅.
- **status:** **provision_research_required**

---

## 6. Boundary-Pair Analysis (as instructed)

| Pair | Verdict | Basis |
|---|---|---|
| `otp_fraud` vs `online_impersonation` | Separable with rule | Impersonation-toward-OTP/transaction → otp_fraud; identity performance without credential/transaction core → impersonation. Prototypes must encode this. |
| `phishing` vs `online_impersonation` | Separable | Instrument test: fabricated link/page/site → phishing; personal/organizational identity performance → impersonation. |
| `misleading_advertisement` vs `unfair_trade_practice` | **Weak — flagged** | Statutory overlap (misleading ads sit inside §2(47) UTP). Boundary is prototype-enforced: deception in the ad/claim vs deception at/around the transaction. Merge is the designated fallback if evaluation fails. |
| `defective_product` vs `refund_denial` | Separable with rule | Product condition vs seller's refusal; dominant-complaint rule for combined scenarios. |
| `wrongful_challan` vs `vehicle_detention` | Clean | Paper/electronic fine vs physical vehicle custody. |
| `document_acceptance_or_verification` vs `document_seizure_or_retention` | Clean | Document stays with citizen (validity disputed) vs document physically taken. |
| `delayed_wages` vs `unpaid_wages` | **Weak-to-moderate — flagged** | Temporal/intent boundary; real user text often indeterminate. Merge watch (`wage_nonpayment`) pending wage-law research + prototype evaluation. |
| `breach_of_contract` vs `security_deposit_dispute` | Clean | Performance failure during agreement vs deposit return after agreement ends; distinctive deposit vocabulary. |

## 7. Review Summary

### 7.1 Status Tally (22 issues — 6 + 5 + 5 + 4 + 2)

| Domain | taxonomy_supported | provision_research_required | rejected | merged | working |
|---|---|---|---|---|---|
| `cyber_fraud` (6) | 5 | 1 (`other_online_financial_fraud`) | 0 | 0 | 0 |
| `consumer_issues` (5) | 5 | 0 | 0 | 0 | 0 |
| `traffic_enforcement` (5) | 3 | 2 (`bribe_demand`, `wrongful_challan`) | 0 | 0 | 0 |
| `workplace_wage` (4) | 0 | 4 (all — wage-law research gate) | 0 | 0 | 0 |
| `contractual_disputes` (2) | 1 | 1 (`security_deposit_dispute`) | 0 | 0 | 0 |
| **Total (22)** | **14** | **8** | **0** | **0** | **0** |

### 7.2 Recommendations Recorded (none applied)

1. **No immediate taxonomy change is recommended.** All 22 issues remain in the
   taxonomy; 8 carry `provision_research_required` and are blocked from KB population
   and Dataset V1 labeling finalization until their research completes.
2. **Conditional (bribe_demand):** if targeted research cannot establish non-criminal
   provision support, reframe as `on_spot_payment_without_official_challan` or reject.
3. **Merge watch (wage):** `delayed_wages` + `unpaid_wages` → `wage_nonpayment` if the
   wage-law research shows identical remedies AND prototypes cannot separate them.
4. **Merge fallback (consumer):** `misleading_advertisement` → `unfair_trade_practice`
   only if prototype/Dataset V1 evaluation shows Module 2 cannot separate them.
5. **No `bike_key_removal` issue** — official-source support not established (§3.6).
6. **No rename is recommended at this time** (the bribe_demand reframe in item 2 is
   conditional on research findings).

### 7.3 Research Queue Created by This Review

| Priority | Research item | Unblocks |
|---|---|---|
| 1 | Wage-law transition research (`docs/wage_law_research.md` — already a planned parallel workstream) | All 4 `workplace_wage` issues |
| 2 | Non-criminal provision support for `bribe_demand` (MV Act §200 / e-challan payment-procedure framing) | `bribe_demand` |
| 3 | Contest/grievance pathway mapping for challans (MV Act Ch. XIII + state e-challan rules) | `wrongful_challan` |
| 4 | Stable Phase 1 provision set for `other_online_financial_fraud` (IT Act §66D vs BUDS Act 2019 scope split) | `other_online_financial_fraud` |
| 5 | Model Tenancy Act 2021 state-adoption status + state rent authority routes | `security_deposit_dispute` |

---

**Next step after this review:** user reviews these findings and signs off (or amends)
the taxonomy. KB skeleton creation and ML pipeline structure follow per the approved
implementation order. No provision named in this document is verified; every future KB
entry derived from these leads starts at `provision_status = unverified`,
`verification.status = pending_manual_verification`.
