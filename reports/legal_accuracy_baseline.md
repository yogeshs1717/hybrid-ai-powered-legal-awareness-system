# LegalLens – Legal Accuracy Baseline & Mapping Gap Audit Report

**Auditor Role:** Senior Indian Legal Researcher, Legal AI Architect & Software Testing Specialist  
**System Evaluated:** LegalLens – Hybrid AI-Powered Legal Awareness System  
**Report Type:** Phase One & Phase Two Baseline Reproduction & Mapping Gap Diagnosis  
**Date of Audit:** October 30, 2026  
**Status:** Baseline Reproduction Verified Across 150 Benchmark Scenarios  

---

## 1. Executive Summary & Baseline Reproduction

An independent reproduction of the legal accuracy and reliability evaluation of LegalLens was conducted directly against the FastAPI `/analyze` endpoint using the 150 benchmark scenarios across the five locked project domains:

- **Cyber Fraud:** 30 scenarios
- **Consumer Issues:** 30 scenarios
- **Traffic Enforcement:** 30 scenarios
- **Workplace / Wage:** 30 scenarios
- **Contractual Disputes:** 30 scenarios

### 1.1 Verified Baseline Evaluation Metrics

| Metric / Evaluation Dimension | Evaluated Baseline Score | Evaluation Weight | Weighted Contribution |
|:---|:---:|:---:|:---:|
| **1. Domain Classification Accuracy** | **94.67%** | 10% | 9.47% |
| **2. Issue Detection Accuracy** | **76.33%** | 15% | 11.45% |
| **3. Correct Act Identification** | **55.57%** | 15% | 8.34% |
| **4. Section Retrieval Precision & Recall** | **53.38%** | 20% | 10.68% |
| **5. Legal Applicability & Reasoning** | **79.97%** | 15% | 11.99% |
| **6. Official Citation Verification Rate** | **100.00%** | 10% | 10.00% |
| **7. Action-Step Accuracy** | **98.00%** | 5% | 4.90% |
| **8. Government Portal Accuracy** | **98.00%** | 5% | 4.90% |
| **9. Clarification & Uncertainty Handling** | **87.20%** | 5% | 4.36% |
| **OVERALL WEIGHTED ACCURACY SCORE** | **76.08%** | **100%** | **76.08%** |

**Performance Band:** *Acceptable legal assistance with minor supervision (75% - 89%)*  
**Operational Metrics:** 100% uptime, zero HTTP 500 errors, **2.66 ms** average latency per query.

---

## 2. Root Cause Analysis of Low Section Retrieval (53.38%)

The lowest-performing dimension in the baseline system is **Section Retrieval Precision & Recall (53.38%)**, followed by **Act Identification (55.57%)**. Detailed diagnostic tracing revealed four structural causes:

### 2.1 Cause 1: Under-Mapped Single Provisions in `issue_mappings.json`
The curated knowledge base historically mapped many real-world citizen issues to only a single statutory section. Under Indian statutory law, however, disputes almost always invoke compound statutory provisions:
- **Criminal Cyber Scams:** In practice, online financial cheating cannot be charged under Section 66D of the Information Technology Act, 2000 alone. A valid police complaint/FIR requires **Section 318(4) of Bharatiya Nyaya Sanhita, 2023** (Cheating and dishonestly inducing delivery of property) alongside IT Act Section 66C (Identity theft) and 66D.
- **Consumer Defect Claims:** A complaint under Section 35 of the Consumer Protection Act, 2019 requires establishing the statutory definition of **Defect (Section 2(10))** or **Deficiency in Service (Section 2(11))**, and often **Product Liability (Section 84)**.
- **Traffic Offenses:** The Motor Vehicles Act, 1988 separates the substantive duty/violation section (e.g. Section 129 for helmet) from the penalizing section (Section 194D). Mapping only one leaves the citizen without knowledge of either the rule or the statutory penalty.

### 2.2 Cause 2: Conflating Textual Similarity with Legal Applicability
Module 2 uses TF-IDF cosine similarity against prototype sentences. If a user scenario mentions a prominent keyword like "phone", "card", or "bank", the prototype argmax frequently latches onto a hyper-specific sibling issue (e.g., `fastag_recharge_wallet_phishing` instead of `phishing`, or `credit_card_reward_points_expiry_link` instead of `otp_fraud`). While in the same domain, this misdirection causes Module 3 to retrieve narrow statutory provisions that do not match the complete factual matrix.

### 2.3 Cause 3: Absence of Relevance Classification
The baseline system returns a flat list of legal provisions with no tiering. It does not distinguish whether a section is:
- `DIRECTLY_APPLICABLE` (all core elements satisfied)
- `CONDITIONALLY_APPLICABLE` (applies if specific factual predicates are established)
- `PROCEDURAL_PROVISION` (mechanisms like notice periods, limitation, complaint filing procedures)
- `SUPPORTING_PROVISION` (statutory definitions and evidentiary presumptions)

### 2.4 Cause 4: Lack of Statutory Element Validation
The baseline system does not verify whether the factual ingredients of an offense are present. For example:
- It cannot distinguish an intentional fraudulent inducement at inception (BNS Section 318 Cheating) from a subsequent civil failure to deliver (Indian Contract Act Section 73).
- It cannot distinguish between an authorized traffic diversion ordered by a police officer (Section 119/179 MV Act) and voluntary wrong-side driving (Section 184 MV Act).

---

## 3. Comprehensive Audit of the 83 Reported Mapping Gaps

The 83 mapping gaps identified in `knowledge_base_gaps.json` were audited and grouped into statutory categories across the five domains.

### 3.1 Domain 1: Cyber Fraud (13 Gaps)

| Gap ID | User Scenario Summary | Predicted Issue | Retrieved Provisions | Legally Expected Provisions | Legal Reason & Official Authority |
|:---|:---|:---|:---|:---|:---|
| **CF01** | Phone call OTP debit fraud (Rs 48,000) | `credit_card_reward_points_expiry_link` | IT Act S. 66C, 66D | IT Act S. 66C, 66D **AND** BNS S. 318(4) | Deceptive inducement to part with OTP is both cyber personation (IT Act 66D) and criminal cheating (BNS 318(4)). FIRs require both. (Gazette of India, India Code). |
| **CF04** | SMS phishing link mimicking HDFC net banking | `fastag_recharge_wallet_phishing` | IT Act S. 66D | IT Act S. 66C, 66D **AND** BNS S. 318 | Electronic phishing creates fake computer resource to cheat. Requires BNS 318 for cheating and IT Act 66C/66D. |
| **CF07** | SIM swap fraud with duplicate SIM | `sim_swap_fraud` | IT Act S. 66C | IT Act S. 66C, 66D **AND** BNS S. 318, 336 | Fraudulent issuance of duplicate SIM involves identity theft (66C), forgery (BNS 336), and cheating (BNS 318). |
| **CF09** | Unauthorized POS transaction while abroad | `card_cloning_skimming` | IT Act S. 66C, 66D | IT Act S. 66C, 66D, BNS S. 318, **RBI Zero Liability Circular** | Skimming/cloning requires BNS 318 for property loss, plus RBI Master Direction DBR.No.Leg.BC.78/09.07.005/2017-18 for customer zero liability. |
| **CF11** | Stalking & vulgar messages via fake handles | `online_impersonation` | IT Act S. 66D | IT Act S. 66E, 67 **AND** BNS S. 78, 79, 351 | Repeated non-consensual electronic harassment constitutes cyber stalking under BNS Section 78 and privacy violation under IT Act Section 66E. |
| **CF12** | Video call recording & morphed sextortion | `sextortion_fraud` | IT Act S. 66E, 67 | IT Act S. 66E, 67, 67A **AND** BNS S. 308, 351 | Morphing explicit material is an offense under IT Act 67A; extorting money under threat of disclosure is extortion under BNS Section 308. |
| **CF13** | Instagram seller received UPI and vanished | `None` (Safe Fallback) | None | IT Act S. 66D, BNS S. 318, **CPA S. 2(11) / E-Commerce Rules** | Fake seller inducing UPI transfer without intent to supply is cheating under BNS 318 and unfair trade practice under Consumer Protection (E-Commerce) Rules 2020. |
| **CF14** | UPI transfer debited but landlord did not receive | `remote_access_app_fraud` | IT Act S. 66D | **RBI Circular DPSS.CO.PD.No.629/02.01.014/2019-20** (Harmonisation of TAT) | Transaction failure is not cyber fraud; it is a technical failure governed by RBI TAT circular for auto-reversal and Rs 100/day compensation. |
| **CF15** | Electricity bill disconnection APK scam | `electricity_bill_sms_apk_scam` | IT Act S. 66D, 43 | IT Act S. 43, 66, 66D **AND** BNS S. 318 | Installing malicious APK to compromise mobile device is unauthorized access under S. 43/66 and cheating under BNS 318. |
| **CF16** | AI voice clone virtual kidnapping ransom | `ai_voice_clone_virtual_kidnapping` | IT Act S. 66D | IT Act S. 66D **AND** BNS S. 308, 318, 319, 351 | Impersonating a kidnapped family member with AI audio to demand money is extortion (BNS 308), cheating by personation (BNS 319), and criminal intimidation (BNS 351). |
| **CF17** | AePS biometric fingerprint cloning theft | `aeps_biometric_aadhaar_money_theft` | IT Act S. 66C, 66 | IT Act S. 66C, 66 **AND** BNS S. 318, Aadhaar Act S. 42 | Biometric cloning involves identity theft (66C), unauthorized access (66), Aadhaar Act Section 42 violation, and BNS 318 cheating. |
| **CF18** | Customs drug parcel digital arrest scam | `courier_customs_fraud` | IT Act S. 66D | IT Act S. 66D **AND** BNS S. 204, 308, 318 | Impersonating police/customs officers via video call to extort money is impersonation of public servant (BNS 204), extortion (BNS 308), and cheating (BNS 318). |
| **CF20** | Telegram task review investment scam | `fake_crypto_arbitrage_telegram_ponzi` | IT Act S. 66D | IT Act S. 66D **AND** BNS S. 318, Banning of Unregulated Deposit Schemes Act 2019 S. 3 | Inducing public deposits into fake task/crypto schemes violates BUDS Act 2019 and constitutes cheating under BNS 318. |

---

### 3.2 Domain 2: Consumer Issues (21 Gaps)

| Gap ID | User Scenario Summary | Predicted Issue | Retrieved Provisions | Legally Expected Provisions | Legal Reason & Official Authority |
|:---|:---|:---|:---|:---|:---|
| **CI01** | Defective smartphone motherboard dead in 7 days | `defective_product_replacement_denial` | CPA 2019 S. 35 | CPA 2019 S. 2(10), S. 2(11), S. 35, S. 84 | Defective product requires establishing statutory definition of "defect" (S. 2(10)) and product liability of manufacturer/dealer (S. 84). |
| **CI02** | Airline canceled flight and refuses refund | `flight_delay_cancellation_refund_dispute` | CPA 2019 S. 35 | CPA 2019 S. 2(11), S. 35, **DGCA CAR Section 3, Series M, Part IV** | Airline refund denial is deficiency in service under CPA S. 2(11) and a direct violation of DGCA Civil Aviation Requirements on cancellations. |
| **CI03** | Coaching institute refuses refund upon withdrawal | `education_coaching_fee_refund_dispute` | CPA 2019 S. 35 | CPA 2019 S. 2(11), S. 2(47), S. 35, **CCPA Guidelines on Coaching Institutes 2024** | Withholding fees for unavailed quarters is an unfair trade practice under S. 2(47) and specifically prohibited under Central Consumer Protection Authority Guidelines. |
| **CI04** | Misleading dark-pattern subscription auto-debit | `misleading_advertisement_claim` | CPA 2019 S. 2(28) | CPA 2019 S. 2(28), S. 89, **CCPA Guidelines for Prevention of Dark Patterns 2023** | Deceptive auto-renewals constitute dark patterns under CCPA Dark Patterns Guidelines and attract penalties under CPA S. 89. |
| **CI07** | AC technician took Rs 4,500 and damaged unit | `breach_of_contract` (Domain error) | Contract Act S. 73 | CPA 2019 S. 2(11), S. 35 | Individual hiring service technician is a consumer; damage during service constitutes deficiency in service under CPA Section 2(11). |
| **CI09** | Bank deducted unauthorized SMS alert charges | `credit_card_reward_points_expiry_link` (Domain error) | IT Act S. 66C | CPA 2019 S. 2(11), S. 35, **RBI Integrated Ombudsman Scheme 2021** | Bank deducting fees without consent is a deficiency in banking service under CPA S. 2(11) and governed by RBI Ombudsman. |
| **CI10** | Pressure cooker exploded causing burn injury | `defective_product_replacement_denial` | CPA 2019 S. 35 | CPA 2019 S. 2(10), S. 84, S. 85, S. 86 | Personal injury from defective product triggers Chapter VI Product Liability under Sections 84-86 of CPA 2019. |
| **CI11** | Health insurance claim rejected for unproven pre-existing condition | `health_insurance_claim_rejection_dispute` | CPA 2019 S. 35 | CPA 2019 S. 2(11), S. 35, **Insurance Ombudsman Rules 2017 (Rule 17)** | Insurer cannot repudiate claim without medical proof after 8-year moratorium; deficiency under S. 2(11) and Insurance Ombudsman jurisdiction. |
| **CI12** | Telecom SIM deactivated without notice | `telecom_unsolicited_commercial_communication_spam` | TRAI Reg. 2018 | CPA 2019 S. 2(11), S. 35, **TRAI Telecom Consumers Protection Regulations** | Arbitrary disconnection without statutory notice violates TRAI Regulations and constitutes deficiency in service under CPA S. 2(11). |
| **CI14** | Hospital refused emergency admission over advance deposit | `hospital_overbilling_cashless_insurance_denial` | CPA 2019 S. 35 | CPA 2019 S. 2(11), S. 35, **Clinical Establishments Act 2010 S. 12** | Emergency treatment denial violates Section 12(2) of Clinical Establishments Act and Supreme Court rulings (*Parmanand Katara*). |
| **CI15** | Food delivery delivered spoiled food with fungus | `expired_packaged_food_sale` | FSS Act S. 26 | FSS Act S. 26, S. 59, CPA 2019 S. 2(10), S. 84 | Contaminated food involves FSS Act 2006 S. 59 (unsafe food penalty) and product liability of food business operator under CPA S. 84. |
| **CI16** | Car delivered with altered odometer | `unfair_contract_terms_unilateral_clause` | CPA 2019 S. 2(46) | CPA 2019 S. 2(47), S. 35, BNS S. 318 | Tampering with odometer to deceive buyer is unfair trade practice under S. 2(47) and criminal cheating under BNS S. 318. |
| **CI17** | Real estate developer delayed possession by 4 years | `real_estate_delayed_possession_interest` | RERA S. 18 | RERA 2016 S. 18, CPA 2019 S. 2(11), S. 35 | Homebuyer has concurrent remedy before RERA (Section 18 interest/refund) and Consumer Commission (Supreme Court in *Imperia Structures*). |
| **CI18** | Hotel refused refund citing 100% cancellation penalty | `unfair_contract_terms_unilateral_clause` | CPA 2019 S. 2(46) | CPA 2019 S. 2(46), S. 2(47), S. 35 | Unilateral 100% cancellation penalty is an "unfair contract" under Section 2(46) of CPA 2019 and voidable before State/National Commission. |
| **CI19** | Packaged goods sold at Rs 250 with Rs 180 MRP | `packaged_goods_dual_mrp_overcharging` | Legal Metrology S. 18 | Legal Metrology Act 2009 S. 18, S. 36, CPA 2019 S. 2(47) | Selling above MRP violates Section 18 of Legal Metrology Act (penalty S. 36) and constitutes unfair trade practice under CPA S. 2(47). |
| **CI20** | E-commerce seller refused return of wrong product delivered | `ecommerce_fake_seller_fraud` | CPA E-Commerce Rules | CPA 2019 S. 2(11), S. 35, **Consumer Protection (E-Commerce) Rules 2020 Rule 6** | E-commerce entity cannot refuse return of misdescribed or wrong goods under Rule 6 of E-Commerce Rules 2020. |
| **CI27** | Microwave stopped working, user claimed shopkeeper committed criminal breach | `credit_card_reward_points_expiry_link` (Domain error) | IT Act S. 66C | CPA 2019 S. 2(10), S. 35 (Civil consumer defect) | Adversarial attempt to criminalize appliance breakdown; system must recognize consumer defect (S. 2(10)) and reject false criminal claims. |
| **CI29** | In 2021 doctor left surgical sponge inside patient | `hospital_overbilling_cashless_insurance_denial` | CPA 2019 S. 35 | CPA 2019 S. 2(11), S. 35, S. 84, S. 86 (*Res Ipsa Loquitur*) | Medical negligence with retained foreign body is gross deficiency in service under CPA S. 2(11) and product/service liability under S. 86. |
| **CI30** | In 2016 builder took 50% advance for unapproved project | `commercial_lease_lock_in_penalty_dispute` (Domain error) | TP Act S. 106 | CPA 1986 S. 14 / CPA 2019 S. 35, BNS S. 318 | Pre-2019 delayed possession claim must acknowledge CPA 1986 provisions and criminal cheating where approvals were falsified. |

---

### 3.3 Domain 3: Traffic Enforcement (19 Gaps)

| Gap ID | User Scenario Summary | Predicted Issue | Retrieved Provisions | Legally Expected Provisions | Legal Reason & Official Authority |
|:---|:---|:---|:---|:---|:---|
| **TE01** | Driving two-wheeler without helmet | `driving_without_helmet_challan` | MV Act S. 129 | MV Act S. 129 **AND** S. 194D | S. 129 establishes duty to wear protective headgear; S. 194D prescribes the specific fine (Rs 1,000) and 3-month license disqualification. |
| **TE02** | Driving car without fastening seatbelt | `driving_without_seatbelt_challan` | MV Act S. 138 | MV Act S. 138(3) **AND** S. 194B | S. 138 empowers state rules for safety belts; S. 194B establishes the specific statutory penalty (Rs 1,000 fine). |
| **TE03** | Jumping red traffic light at intersection | `jumping_traffic_red_light_challan` | MV Act S. 119 | MV Act S. 119 **AND** S. 184 | Disobeying mandatory traffic sign/signal (S. 119) is prosecuted as dangerous driving under S. 184 (fine up to Rs 5,000 / imprisonment). |
| **TE04** | Driving vehicle without valid Third-Party Insurance | `driving_uninsured_vehicle_challan` | MV Act S. 146 | MV Act S. 146 **AND** S. 196 | S. 146 mandates compulsory third-party insurance; S. 196 imposes penalty (imprisonment up to 3 months or fine up to Rs 2,000/4,000). |
| **TE05** | Showing DigiLocker digital driving license, officer demands physical | `rule_139_digital_documents_digilocker_mparivahan` | CMVR Rule 139 | CMVR Rule 139, MV Act S. 130, S. 206(4), **MoRTH Notification RT-11036/64/2017-MVL** | Officer cannot insist on physical document under Rule 139; seizure of digital documents is governed strictly by Section 206(4). |
| **TE06** | Driver stopped for breathalyzer test, BAC 45mg/100ml | `drunken_driving_alcohol_breath_test` | MV Act S. 185 | MV Act S. 185, S. 203, S. 204 | Breath alcohol exceeding 30mg/100ml violates S. 185; S. 203 and S. 204 govern breath test procedure and mandatory medical laboratory test. |
| **TE07** | E-challan issued with blurry photo showing wrong vehicle | `fake_wrong_number_plate_traffic_challan` | MV Act S. 133 | MV Act S. 133, CMVR Rule 167A, Virtual Courts | Electronic enforcement challans must comply with Rule 167A electronic monitoring standards; challengeable before Virtual Court under S. 133. |
| **TE08** | Commercial truck overloaded by 4 tonnes | `overloading_goods_vehicle_challan` | MV Act S. 113 | MV Act S. 113, S. 114, S. 194(1) | S. 113 limits vehicle weight; S. 114 empowers offloading at driver's cost; S. 194(1) imposes Rs 20,000 base fine + Rs 2,000 per excess tonne. |
| **TE09** | 16-year-old minor driving father's car | `juvenile_minor_driving_parent_penalty` | MV Act S. 199A | MV Act S. 199A, S. 4 | S. 199A imposes Rs 25,000 fine and up to 3 years imprisonment on guardian, vehicle registration cancellation for 1 year, and minor debarred till age 25. |
| **TE10** | Vehicle using illegal high-decibel pressure horn | `pressure_horn_loud_exhaust_challan` | CMVR Rule 119 | CMVR Rule 119, MV Act S. 182A(4), S. 190(2) | Altering silencer or using prohibited horn violates Rule 119 CMVR and attracts S. 190(2) environmental pollution penalty and S. 182A(4). |
| **TE11** | Using mobile phone handheld while driving | `using_mobile_phone_while_driving_challan` | MV Act S. 184 | MV Act S. 184(c), CMVR Rule 138-A | Handheld mobile usage while driving is classified as dangerous driving under S. 184(c) and Rule 138-A of Central Motor Vehicles Rules. |
| **TE12** | Parking in designated 'No Parking' zone | `no_parking_zone_vehicle_towing_charges` | MV Act S. 122 | MV Act S. 122, S. 127, S. 177 | Leaving vehicle in dangerous position violates S. 122; S. 127 authorizes towing by police; S. 177/177A prescribes general penalty. |
| **TE13** | Drove wrong side due to official police diversion | `wrong_side_driving_one_way_violation` | MV Act S. 184 | MV Act S. 119(1), S. 119(2), S. 184 | Disobeying ordinary road flow pursuant to lawful direction of police officer under S. 119(2) is a statutory defense to S. 184 dangerous driving. |
| **TE14** | Vehicle documents seized without issuing receipt | `rule_139_digital_documents_digilocker_mparivahan` | CMVR Rule 139 | MV Act S. 206(2), S. 206(3), S. 206(4) | Police seizing documents must give temporary acknowledgment/receipt under Section 206(3) valid until documents returned or fine paid. |
| **TE15** | Commercial taxi permit expired 2 weeks ago | `driving_without_permit_commercial_vehicle` | MV Act S. 66 | MV Act S. 66, S. 192A | Driving transport vehicle without valid permit violates S. 66 and is punishable under S. 192A with imprisonment up to 6 months or fine up to Rs 10,000. |
| **TE16** | Black tinted sun film on side windows (VLT 20%) | `tinted_glass_sun_film_challan` | CMVR Rule 100 | CMVR Rule 100, MV Act S. 182A(4), Supreme Court in *Avishek Goenka* | Visual Light Transmission must be >= 70% for windscreen and >= 50% for side glasses; black film paste is completely prohibited by Supreme Court. |
| **TE17** | Refusing to stop when signaled by traffic constable | `disobeying_police_traffic_signal_challan` | MV Act S. 179 | MV Act S. 132(1), S. 179(1) | Duty to stop vehicle when required by police officer in uniform under S. 132(1); refusal punishable under S. 179(1) with fine up to Rs 2,000. |
| **TE18** | Driving vehicle with expired Pollution Under Control (PUC) | `driving_without_pucc_pollution_challan` | CMVR Rule 115 | CMVR Rule 115(7), MV Act S. 190(2) | Failure to possess valid PUCC violates Rule 115(7) CMVR and attracts S. 190(2) penalty (fine up to Rs 10,000 or imprisonment up to 3 months). |
| **TE20** | Ambulance obstructed by private car refusing to yield | `blocking_emergency_vehicle_ambulance_challan` | MV Act S. 194E | MV Act S. 194E | Failure to draw to the side of the road to yield right of way to emergency vehicles (ambulance/fire) is punishable under S. 194E with fine up to Rs 10,000. |

---

### 3.4 Domain 4: Workplace / Wage (13 Gaps)

| Gap ID | User Scenario Summary | Predicted Issue | Retrieved Provisions | Legally Expected Provisions | Legal Reason & Official Authority |
|:---|:---|:---|:---|:---|:---|
| **WW01** | Factory worker unpaid wages for 3 months | `unpaid_wages_delay_in_salary` | Payment of Wages Act S. 15 | Payment of Wages Act 1936 S. 5, S. 15 **AND** Minimum Wages Act 1948 S. 12, S. 20 | S. 5 fixes wage period (within 7/10 days); S. 15 provides claim before Authority; non-payment below minimum wage invokes Minimum Wages Act S. 12/20. |
| **WW02** | Employer made arbitrary Rs 8,000 deduction for glass breakage | `illegal_wage_deduction` | Payment of Wages Act S. 7 | Payment of Wages Act 1936 S. 7, S. 9, S. 10, S. 15 | Deductions for damage or loss under S. 7(2)(c) must comply with procedural safeguards of S. 10 (giving show-cause opportunity) and cannot exceed actual damage. |
| **WW03** | Employee completed 6 years service, employer refuses gratuity | `gratuity_non_payment_dispute` | Payment of Gratuity Act S. 4 | Payment of Gratuity Act 1972 S. 4, S. 7, S. 8 | Gratuity is payable on completion of 5 years service under S. 4; S. 7 mandates employer to determine and pay within 30 days; S. 8 provides recovery with compound interest. |
| **WW04** | Pregnant employee terminated during 7th month of pregnancy | `maternity_benefit_denial_leave_pay` | Maternity Benefit Act S. 5 | Maternity Benefit Act 1961 S. 5, S. 12, S. 21 | S. 12 strictly prohibits discharge or dismissal of a woman during her pregnancy/maternity absence; violation punishable under S. 21 with imprisonment. |
| **WW05** | Factory worker forced to work 12 hours daily without overtime pay | `overtime_wage_denial_extra_hours` | Factories Act S. 59 | Factories Act 1948 S. 51, S. 54, S. 59 **AND** Minimum Wages Act S. 14 | Work exceeding 9 hours/day or 48 hours/week mandates overtime pay at double the ordinary rate of wages under Factories Act S. 59 and Minimum Wages Act S. 14. |
| **WW06** | Workman retrenched after 4 years without notice or retrenchment compensation | `unlawful_termination_without_due_process` | Industrial Disputes Act S. 2A | Industrial Disputes Act 1947 S. 25F, S. 25B, S. 33C | Retrenchment of continuous workman (S. 25B) without 1 month notice and 15 days average pay per year of service is void ab initio under S. 25F; recovery under S. 33C. |
| **WW07** | Employer deducted PF from salary but failed to deposit with EPFO | `pf_deduction_not_deposited_epfo` | EPF Act S. 14 | EPF Act 1952 S. 14, S. 14B, BNS S. 316 (Criminal breach of trust) | Failure to deposit employee PF contribution after deducting it constitutes criminal breach of trust under BNS Section 316 and damages under EPF Act Section 14B. |
| **WW08** | Female software engineer subjected to sexual harassment, company has no ICC | `posh_workplace_sexual_harassment_complaint` | POSH Act S. 9 | POSH Act 2013 S. 4, S. 9, S. 26 | Workplace with 10+ employees must constitute Internal Committee under S. 4; failure punishable under S. 26 with fine up to Rs 50,000; complaint under S. 9. |
| **WW09** | Security guard paid Rs 7,000 monthly against statutory minimum wage of Rs 14,500 | `minimum_wages_non_compliance` | Minimum Wages Act S. 12 | Minimum Wages Act 1948 S. 12, S. 20, S. 22 | Paying less than notified statutory minimum wage violates S. 12; S. 20 Authority can award up to 10x compensation; S. 22 provides penal imprisonment. |
| **WW10** | Factory worker lost two fingers in machine, employer refused compensation | `workplace_injury_workmen_compensation` | Employee's Compensation Act S. 3 | Employee's Compensation Act 1923 S. 3, S. 4, S. 4A | Employer is liable for personal injury by accident arising out of employment under S. 3; S. 4A mandates payment within 1 month plus 12% interest and 50% penalty. |
| **WW11** | Full-time IT employee fired on WhatsApp without severance or notice pay | `unlawful_termination_without_due_process` | Industrial Disputes Act S. 2A | State Shops & Commercial Establishments Act (e.g. Karnataka S. 39), Contract Act S. 73 | Non-workmen / IT employees are protected by State Shops and Commercial Establishments Acts requiring 1 month written notice or notice pay and statutory inquiry. |
| **WW12** | Contractual workers doing same job as permanent workers paid 50% wages | `minimum_wages_non_compliance` | Minimum Wages Act S. 12 | Contract Labour (R&A) Act 1970 S. 21, Rule 25(2)(v), Equal Remuneration principle | Contract labour performing same or similar work as regular workmen are entitled to identical wage rates under Rule 25(2)(v) of Contract Labour Central Rules. |
| **WW14** | Company closed factory without 60 days notice to Labour Department | `unlawful_termination_without_due_process` | Industrial Disputes Act S. 2A | Industrial Disputes Act 1947 S. 25FFA, S. 25-O | Employer intending to close undertaking must serve 60 days notice under S. 25FFA (or obtain prior government permission for 100+ workmen under S. 25-O). |

---

### 3.5 Domain 5: Contractual Disputes (17 Gaps)

| Gap ID | User Scenario Summary | Predicted Issue | Retrieved Provisions | Legally Expected Provisions | Legal Reason & Official Authority |
|:---|:---|:---|:---|:---|:---|
| **CD01** | Commercial vendor failed to deliver machinery, buyer suffered business loss | `breach_of_contract` | Contract Act S. 73 | Indian Contract Act 1872 S. 73, S. 74 **AND** Sale of Goods Act 1930 S. 57 | Compensation for breach under S. 73 covers ordinary damages arising naturally; buyer action for non-delivery of goods governed by S. 57 Sale of Goods Act. |
| **CD02** | Residential landlord refuses to refund Rs 1,50,000 security deposit | `security_deposit_refund_dispute` | Contract Act S. 73 | Indian Contract Act S. 73, Transfer of Property Act 1882 S. 108(q), State Rent Control Act | Withholding security deposit without lawful deduction violates lease covenants under TP Act S. 108 and unjust enrichment principles. |
| **CD03** | Client issued cheque for Rs 2,50,000 which bounced for insufficient funds | `cheque_bounce_statutory_notice_138` | NI Act S. 138 | NI Act 1881 S. 138, S. 141, S. 142 | Dishonour for funds insufficient triggers S. 138; S. 142 mandates statutory demand notice within 30 days and 15 days cure period before filing complaint. |
| **CD04** | Interior decorator took 70% advance and abandoned site half finished | `breach_of_contract` | Contract Act S. 73 | Indian Contract Act 1872 S. 39, S. 73 **AND** Specific Relief Act 1963 S. 20 | Refusal to perform contract in its entirety permits buyer to terminate under S. 39 and obtain "substituted performance" through third party under S. 20 Specific Relief Act. |
| **CD05** | Service agreement clause stipulates Rs 50 lakh penalty for minor breach | `liquidated_damages_penalty_clause_dispute` | Contract Act S. 74 | Indian Contract Act 1872 S. 74 (*Kailash Nath Associates v. DDA*) | Stipulated sum by way of penalty cannot be enforced in full; S. 74 limits recovery to reasonable compensation not exceeding the named amount. |
| **CD06** | Vendor supplied sub-standard industrial steel bolts causing machine breakdown | `breach_of_contract` | Contract Act S. 73 | Sale of Goods Act 1930 S. 15, S. 16, S. 59 **AND** Contract Act S. 73 | Implied condition as to fitness for purpose under S. 16 Sale of Goods Act; breach allows buyer to set up breach of warranty in diminution of price under S. 59. |
| **CD07** | Franchise agreement induced by falsified balance sheets and revenue figures | `None` (Domain/Validation failure) | None | Indian Contract Act 1872 S. 17 (Fraud), S. 18 (Misrepresentation), S. 19 (Voidability) **AND** BNS S. 318 | Agreement induced by fraudulent representation is voidable under S. 19 Contract Act and constitutes criminal cheating under BNS S. 318. |
| **CD08** | Client terminated 2-year AMC abruptly without 60-day notice | `commercial_lease_lock_in_penalty_dispute` | TP Act S. 106 | Indian Contract Act 1872 S. 73 | Termination of commercial service contract in breach of agreed notice period is a simple breach of contract under S. 73, not a lease dispute under TP Act. |
| **CD10** | Buyer paid 90% purchase price for land, seller refuses to execute deed | `fraudulent_active_concealment_used_car_sale` (Mismatch) | Contract Act S. 17 | Specific Relief Act 1963 S. 10, S. 16, S. 20 **AND** Transfer of Property Act S. 54 | Contract to transfer immovable property is enforceable by mandatory specific performance under Section 10 of Specific Relief Act (post-2018 amendment). |
| **CD11** | Commercial partner siphoned firm funds to personal crypto account | `fake_charity_donation_fraud` (Domain error) | IT Act S. 66D | Indian Partnership Act 1932 S. 9, S. 10, S. 13 **AND** BNS S. 316 (Criminal breach of trust) | Partner duty of utmost good faith (S. 9) and duty to indemnify for fraud (S. 10); siphoning firm property is criminal breach of trust under BNS S. 316. |
| **CD12** | Oral contract for wholesale grain supply witnessed by brokers with advance paid | `cheque_bounce_statutory_notice_138` (Mismatch) | NI Act S. 138 | Indian Contract Act 1872 S. 10, Sale of Goods Act 1930 S. 5, S. 57 | Under Indian law, oral agreements are valid contracts (S. 10 Contract Act); failure to deliver grain entitles buyer to sue for non-delivery under S. 57 Sale of Goods Act. |
| **CD13** | Borrower coerced into signing blank stamp papers under physical threat | `undue_influence_senior_citizen_property_agreement` | Contract Act S. 16 | Indian Contract Act 1872 S. 15 (Coercion), S. 19 **AND** BNS S. 351 (Criminal intimidation) | Coercion by threatening an unlawful act vitiates free consent under Section 15 of Contract Act and constitutes criminal intimidation under BNS Section 351. |
| **CD14** | Creditor trying to recover invoice dated 6 years ago with no written acknowledgment | `time_barred_debt_written_promise_breach` | Contract Act S. 25 | Limitation Act 1963 S. 3, Schedule Art. 55 **AND** Contract Act S. 25(3) | 3-year limitation period under Article 55 Limitation Act bars suit; debt only recoverable if debtor executes fresh written promise to pay under S. 25(3). |
| **CD15** | Commercial landlord locked out tenant overnight without statutory 15-day notice | `cheque_bounce_statutory_notice_138` (Mismatch) | NI Act S. 138 | Transfer of Property Act 1882 S. 106, S. 108, S. 111 **AND** Contract Act S. 73 | Termination of month-to-month lease requires 15 days written notice under S. 106 TP Act; extra-judicial lockout is illegal dispossession. |
| **CD17** | Registered MSME supplier supplied auto components, corporate buyer unpaid for 90 days | `None` (Domain/Validation failure) | None | MSMED Act 2006 S. 15, S. 16, S. 18 **AND** Contract Act S. 73 | Section 15 mandates payment within 45 days; Section 16 mandates compound interest at 3x RBI bank rate; Section 18 provides reference to MSEFC. |
| **CD18** | Employer filed suit for Rs 10 lakh liquidated damages on 2-year post-employment non-compete | `non_compete_clause_employment_trade_restraint` | Contract Act S. 27 | Indian Contract Act 1872 S. 27 **AND** S. 74 (*Percept D'Mark v. Zaheer Khan*) | Section 27 renders every agreement in restraint of lawful profession, trade, or business void ab initio; post-employment non-compete cannot be enforced via liquidated damages. |
| **CD29** | In 2017 business client issued cheque of Rs 2 lakh that bounced | `cheque_bounce_statutory_notice_138` | NI Act S. 138 | NI Act 1881 S. 138, S. 142, CrPC 1973 S. 190 (Historical) | Historical cheque bounce governed by Negotiable Instruments Act S. 138 and Code of Criminal Procedure, 1973 (not BNSS). |

---

## 4. Key Takeaways for Stage 3 & Stage 4 Implementation

1. **Multi-Provision Mappings are Non-Negotiable:**
   Every gap analysis confirms that real Indian legal problems cannot be accurately addressed by a single statutory section. Module 3 must support compound provisions structured into `DIRECTLY_APPLICABLE`, `CONDITIONALLY_APPLICABLE`, `PROCEDURAL_PROVISION`, and `SUPPORTING_PROVISION`.
2. **Issue Detection Must Distinguish Civil Breach from Criminal Cheat:**
   Module 2 must be strengthened with hard-negative discriminators to differentiate:
   - Initial fraudulent deception (BNS 318) vs. Subsequent commercial non-performance (Contract Act 73).
   - Defective consumer product (CPA 2(10)) vs. Industrial B2B breach (Sale of Goods Act 16).
3. **Structured Legal Element Validation is Mandatory:**
   Before marking a section as `DIRECTLY_APPLICABLE`, Module 3 must evaluate the presence of statutory ingredients (e.g. deceptive inducement, continuous workman status, 30-day notice limitation).
