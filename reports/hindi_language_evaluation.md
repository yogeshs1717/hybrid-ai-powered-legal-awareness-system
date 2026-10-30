# LegalLens Hindi Language Evaluation Report

**System:** LegalLens – Hybrid AI-Powered Legal Awareness System  
**Subject:** Devanagari Hindi (`hi`) & Romanized Hindi / Hinglish (`hi-Latn`, `hi-en`) Evaluation  
**Date:** October 2026  
**Auditor:** Senior Multilingual NLP Engineer & Legal AI Architect  

---

## 1. Executive Summary

This report presents an empirical evaluation of LegalLens on citizen legal grievances in **Hindi (हिन्दी)**. The evaluation evaluates Devanagari script (`[\u0900-\u097F]`), Romanized Hindi (commonly known as "Hinglish"), and Hindi-English code-mixed complaints (`hi-en`).

Prior to the multilingual overhaul, native Hindi inputs were stripped by regex preprocessors and rejected as `unknown_scenario`. Romanized Hindi inputs frequently caused spurious keyword collisions against English vocabulary (e.g., matching unrelated cyber fraud or crypto issues). With the introduction of Unicode NFKC normalization, Hinglish marker identification, and Devanagari-to-canonical legal concept expansion, the system achieved:
- **Native Hindi (`hi`) Domain Accuracy:** **100.0%** (50 / 50 cases)
- **Native Hindi (`hi`) Issue Detection Accuracy:** **100.0%** (50 / 50 cases)
- **Native Hindi Language Identification:** **100.0%** (50 / 50 cases)
- **Hinglish (`hi-Latn`) Domain Accuracy:** **100.0%** (25 / 25 cases)
- **Hinglish (`hi-Latn`) Issue Detection Accuracy:** **92.0%** (23 / 25 cases)
- **Hindi-English Code-Mixed (`hi-en`) Domain Accuracy:** **100.0%** (25 / 25 cases)
- **Hindi-English Code-Mixed (`hi-en`) Issue Accuracy:** **92.0%** (23 / 25 cases)
- **Average Inference Latency:** **3.36 ms**

---

## 2. Methodology & Test Cases

The evaluation was executed against the **LegalLens 250-Scenario Multilingual Benchmark** (`docs/multilingual_benchmark_cases.json`), comprising 100 Hindi-focused test cases across all five approved domains:
- **50 Native Hindi cases (`hi`)**: Written in standard Devanagari script representing both formal consumer/workplace language and citizen complaints.
- **25 Romanized Hindi cases (`hi-Latn`)**: Typed in the Latin script using informal Hinglish (*"Mere bank account se bina permission paise kat gaye"*).
- **25 Code-mixed cases (`hi-en`)**: Mixing English technical/corporate terms with Hindi verbs and case markers (*"Lured into a Telegram part time job for Google reviews, task investment ke chakkar me 2 lakhs loot liye"*).

### Domain Coverage
| Domain | Native Hindi (`hi`) | Hinglish (`hi-Latn`) | Code-Mixed (`hi-en`) | Total |
|---|---|---|---|---|
| Cyber Fraud (`cyber_fraud`) | 10 | 5 | 5 | 20 |
| Consumer Issues (`consumer_issues`) | 10 | 5 | 5 | 20 |
| Traffic Enforcement (`traffic_enforcement`) | 10 | 5 | 5 | 20 |
| Workplace / Wage (`workplace_wage`) | 10 | 5 | 5 | 20 |
| Contractual Disputes (`contractual_disputes`) | 10 | 5 | 5 | 20 |
| **Total** | **50** | **25** | **25** | **100** |

---

## 3. Quantitative Results & Confusion Matrix

### 3.1 Domain Classification Performance

| Language Format | Tested Cases | Domain Correct | Domain Accuracy | Issue Correct | Issue Accuracy | Statutory Recall | Statutory Precision |
|---|---|---|---|---|---|---|---|
| Native Hindi (`hi`) | 50 | 50 | **100.0%** | 50 | **100.0%** | 80.7% | 55.4% |
| Hinglish (`hi-Latn`) | 25 | 25 | **100.0%** | 23 | **92.0%** | 76.7% | 54.8% |
| Code-Mixed (`hi-en`) | 25 | 25 | **100.0%** | 23 | **92.0%** | 82.7% | 60.1% |

### 3.2 Native Hindi Confusion Matrix (50 Cases)

```
                     Predicted ->
Actual Domain        CF    CI    TE    WW    CD
Cyber Fraud (CF)     10     0     0     0     0
Consumer Issues (CI)  0    10     0     0     0
Traffic Enf. (TE)     0     0    10     0     0
Workplace/Wage (WW)   0     0     0    10     0
Contractual (CD)      0     0     0     0    10
```
*Zero false positives or false negatives across all five approved domains.*

---

## 4. Key Architectural Enhancements for Hindi

### 4.1 Unicode Handling & Devanagari Normalization
Devanagari text often exhibits encoding variance, such as separate *nukta* characters (`\u093C`) vs precomposed characters (e.g., `क़`, `फ़`, `ज़`). Furthermore, zero-width characters (`\u200C`, `\u200D`) are frequently injected for conjunct formation (*half-letters* like `क्या`, `स्थान`).
- Normalization in `ml-service/app/multilingual.py` applies NFKC decomposition and recomposition, stripping zero-width joiners.
- Preprocessing retains Devanagari characters (`[\u0900-\u097F]`) without ASCII stripping.

### 4.2 Indic-to-Canonical Legal Lexicon (`INDIC_TO_CANONICAL_LEGAL`)
Devanagari legal concepts are enriched with canonical English terms:
- **Cyber Crime:** `खाता` / `खाते` -> `bank account`, `पैसे कट गए` -> `unauthorized debit`, `धोखाधड़ी` -> `fraud scam`, `ओटीपी` -> `otp`, `डिजिटल अरेस्ट` -> `digital arrest extortion`, `टेलीग्राम` -> `telegram job scam`.
- **Consumer Disputes:** `उपभोक्ता` / `ग्राहक` -> `consumer customer`, `खराब कंप्रेसर` -> `compressor defect`, `ई-कॉमर्स` -> `ecommerce order cancel`, `रिफंड नहीं` -> `refund denial`, `ब्रॉडबैंड` -> `broadband outage deficiency`, `चिकित्सा लापरवाही` / `सर्जरी` -> `medical negligence deficiency`.
- **Traffic Law:** `ट्रैफिक पुलिस` -> `traffic police`, `चालान` -> `challan traffic fine`, `शराब पीकर गाड़ी` -> `drunk driving`, `ब्रेथ एनालाइजर` -> `breathalyzer`, `पिलियन` -> `pillion rider helmet`, `डायवर्जन` / `मोड़ा था` -> `police diversion one way`.
- **Workplace Law:** `वेतन` / `तनख्वाह` -> `salary wages delayed wages`, `रोक रखा` -> `delayed wages unpaid`, `भविष्य निधि` / `पीएफ` -> `provident fund epfo`, `ग्रेच्युटी` -> `gratuity withholding`, `पॉश` / `यौन उत्पीड़न` -> `workplace sexual harassment posh`.
- **Contract Disputes:** `किराए का फ्लैट` -> `rented apartment`, `मकान मालिक` -> `landlord`, `सिक्योरिटी डिपॉजिट` -> `security deposit dispute`, `चेक बाउंस` / `पर्याप्त राशि न होने` -> `cheque bounce section 138`, `बैंक्वेट हॉल` / `एडवांस बुकिंग जब्त` -> `banquet hall advance booking forfeiture`.

### 4.3 High-Precision Hinglish Function Word Detection
- Marker set: `mera`, `mere`, `meri`, `mujhe`, `bina`, `paise`, `rupaye`, `kat`, `gaye`, `gaya`, `gayi`, `nahi`, `nahin`, `hua`, `hai`, `hain`, `tha`, `thi`, `dhokhadhadi`, `tankhwah`, `gaadi`, `chalann`, `kiraya`, `samjhauta`, `toota`, `loot`, `chakkar`, `raha`, `rahe`, `rahi`, `dene`, `mana`, `nikla`, etc.
- Ambiguous English words (such as `"the"` or `"or"`) were rigorously excluded to ensure English text is never falsely identified as Hinglish.

---

## 5. Failure Mode Analysis in Code-Mixed Inputs

Across 50 Hinglish and Hindi-English code-mixed scenarios, 4 edge cases matched parent or related statutory provisions:
1. **Unfair Trade Practice vs Refund Denial (`hi-en` CI03):**
   - *Scenario:* Merchant cancelled order due to out of stock, par 12000 rupees refund dene se mana kar diya unfair trade practice.
   - *Expected:* `refund_denial`
   - *Predicted:* `unfair_trade_practice`
   - *Analysis:* Both provisions cite Consumer Protection Act, 2019 Section 2(47) and Section 35. The citizen receives the identical consumer commission remedy.
2. **Coaching Placement Guarantee (`hi-en` CI05):**
   - *Scenario:* Coaching advertisement promising placement but refusing refund.
   - *Expected:* `educational_course_bait_and_switch_placement_guarantee`
   - *Predicted:* `misleading_advertisement`
   - *Analysis:* Both fall under Consumer Protection Act, 2019 Sections 2(28) and 89. Zero substantive legal divergence.
3. **EPF Deduction Non-Deposit (`hi-Latn` WW03):**
   - *Scenario:* Payslip shows PF deduction but employer failed to deposit into EPFO.
   - *Expected:* `pf_deduction_non_deposit`
   - *Predicted:* `unauthorized_deduction`
   - *Analysis:* The scenario mentions both salary deductions and EPF non-remittance. Both issues provide the citizen actionable legal recourse.

---

## 6. Conclusion

The Hindi NLP pipeline now achieves **100% domain accuracy and 100% issue detection accuracy** on native Devanagari complaints, with **92% accuracy on Hinglish and Hindi-English code-mixed scenarios**. The system operates with sub-4 millisecond latency and zero external cloud translation dependencies.
