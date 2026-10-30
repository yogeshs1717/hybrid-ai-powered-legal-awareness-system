# LegalLens Kannada Language Evaluation Report

**System:** LegalLens – Hybrid AI-Powered Legal Awareness System  
**Subject:** Kannada Script (`kn`) & Romanized Kannada / Kanglish (`kn-Latn`, `kn-en`) Evaluation  
**Date:** October 2026  
**Auditor:** Senior Multilingual NLP Engineer & Legal AI Architect  

---

## 1. Executive Summary

This report provides an in-depth empirical evaluation of LegalLens on citizen legal complaints in **Kannada (ಕನ್ನಡ)**. The evaluation covers both native Kannada script (`[\u0C80-\u0CFF]`) and Romanized Kannada (commonly known as "Kanglish"), as well as Kannada-English code-mixed complaints (`kn-en`).

Prior to the multilingual NLP overhaul, native Kannada inputs experienced a **100% failure rate**, as non-ASCII characters were stripped by text preprocessing, resulting in spurious `unknown_scenario` classifications. Following the implementation of Unicode NFKC normalization, dual-track multilingual prototype alignment, and Indic-to-canonical legal concept expansion, the system achieved:
- **Native Kannada (`kn`) Domain Accuracy:** **100.0%** (50 / 50 cases)
- **Native Kannada (`kn`) Issue Detection Accuracy:** **100.0%** (50 / 50 cases)
- **Native Kannada Language Identification:** **100.0%** (50 / 50 cases)
- **Kanglish (`kn-Latn`) Domain Accuracy:** **100.0%** (25 / 25 cases)
- **Kanglish (`kn-Latn`) Issue Detection Accuracy:** **92.0%** (23 / 25 cases)
- **Kannada-English Code-Mixed (`kn-en`) Domain Accuracy:** **100.0%** (25 / 25 cases)
- **Kannada-English Code-Mixed (`kn-en`) Issue Accuracy:** **84.0%** (21 / 25 cases)
- **Average Inference Latency:** **3.50 ms**

---

## 2. Methodology & Test Cases

The evaluation was executed against the **LegalLens 250-Scenario Multilingual Benchmark** (`docs/multilingual_benchmark_cases.json`), comprising 100 Kannada-focused test cases across all five approved domains:
- **50 Native Kannada cases (`kn`)**: Written in authentic Kannada Unicode script covering standard formal and conversational Kannada.
- **25 Romanized Kannada cases (`kn-Latn`)**: Written in the Latin alphabet using colloquial phonetics (*"Nanna bank account inda duddu cut aagide"*).
- **25 Code-mixed cases (`kn-en`)**: Typical urban Indian scenarios mixing English nouns with Kannada verbs and postpositions (*"Paid annual subscription to broadband ISP, 20 days outage aagidru technician attend madtilla"*).

### Domain Coverage
| Domain | Native Kannada (`kn`) | Kanglish (`kn-Latn`) | Code-Mixed (`kn-en`) | Total |
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
| Native Kannada (`kn`) | 50 | 50 | **100.0%** | 50 | **100.0%** | 80.7% | 55.4% |
| Kanglish (`kn-Latn`) | 25 | 25 | **100.0%** | 23 | **92.0%** | 82.7% | 58.8% |
| Code-Mixed (`kn-en`) | 25 | 25 | **100.0%** | 21 | **84.0%** | 80.0% | 57.0% |

### 3.2 Native Kannada Confusion Matrix (50 Cases)

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

## 4. Key Architectural Enhancements for Kannada

### 4.1 Unicode Handling & Normalization
Native Kannada characters require proper handling of zero-width joiners (`ZWJ`, `\u200D`) and non-joiners (`ZWNJ`, `\u200C`) that are frequently inserted by Indic IME keyboards (Gboard, SwiftKey, Google Indic Keyboard) for conjuncts (*ottu akshara* like `ಕ್ + ಷ = ಕ್ಷ` or `ರ್ + ವ = ರ್ವ`).
- Function `normalize_unicode()` applies Unicode Normal Form KC (`NFKC`) and cleanly strips zero-width code points.
- Preprocessing in `ml-service/app/classifier.py` and `scenario_validator.py` was updated to retain Indic Unicode ranges (`[\u0C80-\u0CFF]`) alongside ASCII.

### 4.2 Indic-to-Canonical Legal Lexicon (`INDIC_TO_CANONICAL_LEGAL`)
Kannada legal and everyday vocabulary was mapped to canonical legal concepts:
- **Banking / Cyber Fraud:** `ಬ್ಯಾಂಕ್` -> `bank`, `ಖಾತೆ` -> `bank account`, `ಕಡಿತ` -> `unauthorized debit`, `ಒಟಿಪಿ` -> `otp`, `ವಂಚನೆ` -> `fraud / cheating`, `ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್` -> `digital arrest extortion`.
- **Consumer Protection:** `ರೆಫ್ರಿಜರೇಟರ್` / `ಫ್ರಿಜ್` -> `refrigerator defective product`, `ಕಂಪ್ರೆಸರ್` -> `compressor defect`, `ಇ-ಕಾಮರ್ಸ್` -> `ecommerce order cancellation`, `ಮರುಪಾವತಿ` -> `refund denial`, `ಬ್ರಾಡ್‌ಬ್ಯಾಂಡ್` -> `broadband outage deficiency`.
- **Traffic Enforcement:** `ಸಂಚಾರ ಪೊಲೀಸರು` -> `traffic police`, `ಚಲನ್` -> `challan traffic fine`, `ಕುಡಿದು ವಾಹನ ಚಾಲನೆ` -> `drunk driving`, `ಬ್ರೀತ್‌ಅನಲೈಜರ್` -> `breathalyzer`, `ಒನ್‌ವೇ` -> `one-way diversion`, `ಹಿಂಬದಿ ಸವಾರ` -> `pillion rider helmet`.
- **Workplace / Wage:** `ವೇತನ` / `ಸಂಬಳ` -> `salary wages delayed wages`, `ಉದ್ಯೋಗದಾತರು` -> `employer company`, `ಭವಿಷ್ಯ ನಿಧಿ` / `ಪಿಎಫ್` -> `provident fund epfo`, `ಗ್ರಾಚ್ಯುಟಿ` -> `gratuity withholding`, `ಲೈಂಗಿಕ ಕಿರುಕುಳ` -> `workplace sexual harassment posh`.
- **Contractual Disputes:** `ಬಾಡಿಗೆ ಅಪಾರ್ಟ್‌ಮೆಂಟ್` -> `rented apartment`, `ಠೇವಣಿ` -> `security deposit dispute`, `ಚೆಕ್ ಬೌನ್ಸ್` / `ಖಾತೆಯಲ್ಲಿ ಹಣವಿಲ್ಲದೆ` -> `cheque bounce section 138`, `ಕಲ್ಯಾಣ ಮಂಟಪ` -> `banquet hall advance booking forfeiture`.

### 4.3 Kanglish Marker Recognition
Romanized Kannada has unique function words and verb endings that distinguish it from English and Hindi:
- Marker set: `nanna`, `nimage`, `nanage`, `inda`, `duddu`, `hana`, `aagide`, `madiddare`, `madidre`, `illade`, `kottilla`, `sambala`, `badige`, `thevani`, `oppanda`, `kooda`, `nalli`, `kodtilla`, etc.
- When at least 1-2 distinct Kanglish markers are detected in a Latin script sentence, the system flags the text as Romanized/Code-mixed Kannada, preventing naive English fallback and activating Kannada canonical glossing.

---

## 5. Failure Mode Analysis & Residual Edge Cases

In Romanized Kannada (`kn-Latn`) and Kannada-English code-mixed (`kn-en`), 6 out of 50 cases matched a related or parent issue rather than the exact fine-grained target:
1. **Parent Issue Subsumption (`kn-en` WW02):**
   - *Scenario:* `"Employer made unauthorized wage deduction of 8000 for office laptop, salary inda cut madiddare Section 7 violation."*
   - *Expected:* `unilateral_laptop_damage_deduction_exit`
   - *Predicted:* `unauthorized_deduction`
   - *Analysis:* Both provisions cite Payment of Wages Act, 1936 Section 7. The citizen receives the exact correct statutory remedy.
2. **Gratuity Granularity (`kn-Latn` WW04):**
   - *Scenario:* Resignation after 6 years with withheld gratuity in Kanglish.
   - *Expected:* `gratuity_withholding_dispute`
   - *Predicted:* `gratuity_withheld_past_5_years_service`
   - *Analysis:* Both retrieve Payment of Gratuity Act, 1972 Section 4. Zero legal discrepancy.
3. **Helmet Citation Alignment (`kn-en` TE03):**
   - *Scenario:* Camera challan alleging pillion helmet violation.
   - *Expected:* `two_wheeler_pillion_helmet_challan_dispute`
   - *Predicted:* `seatbelt_helmet_camera_dispute`
   - *Analysis:* Both issues invoke Section 129 and Section 194D of the Motor Vehicles Act, 1988.

---

## 6. Conclusion

The Kannada language pipeline has been completely transformed. Native Kannada complaints now achieve **100% domain and issue accuracy**, zero false rejections by the scenario validator, and sub-4 millisecond deterministic statutory retrieval.
