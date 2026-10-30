# LegalLens Multilingual NLP Baseline Diagnosis Report

**System:** LegalLens – Hybrid AI-Powered Legal Awareness System  
**Subject:** Multilingual NLP Pipeline Inspection: Kannada, Hindi, English, and Romanized Code-Mixed Inputs  
**Date:** October 2026  
**Auditor:** Senior Multilingual NLP Engineer & Software Architect  

---

## 1. Executive Summary

A diagnostic audit of the LegalLens Natural Language Processing (NLP) pipeline was conducted to investigate critical failures when processing inputs in Indian languages—specifically **Kannada (ಕನ್ನಡ)**, **Hindi (हिन्दी)**, **Romanized Kannada (Kanglish)**, and **Romanized Hindi (Hinglish)**.

### Primary Diagnostic Findings:
1. **Total Failure on Native Script Inputs:** Native Kannada script (`[\u0C80-\u0CFF]`) and Devanagari Hindi script (`[\u0900-\u097F]`) were rejected as `unknown_scenario` with `is_valid_scenario=False`, returning 0 legal provisions.
2. **Misclassification of Romanized Indic Inputs:** Inputs typed in Latin script (e.g., *"Nanna bank account inda nanna permission illade duddu cut aagide"* or *"Mere bank account se bina permission paise kat gaye"*) bypassed script detection, produced spurious keyword matches against English vocabulary, and mapped to incorrect issues (`p2p_crypto_bank_freeze` and `qr_code_fraud` instead of unauthorized banking debit).
3. **Cross-Language Inconsistency:** The identical legal situation yielded conflicting results across languages:
   - **English:** Correctly identified as `cyber_fraud` -> `otp_fraud`.
   - **Kannada:** Rejected as `unknown_scenario`.
   - **Hindi:** Rejected as `unknown_scenario`.
   - **Romanized Kannada:** `cyber_fraud` -> `p2p_crypto_bank_freeze` (Wrong issue).
   - **Romanized Hindi:** `cyber_fraud` -> `qr_code_fraud` (Wrong issue).

---

## 2. Technical Root Cause Analysis

The failure of the multilingual pipeline is caused by five systemic architectural defects:

### Defect 1: ASCII-Only Text Sanitization in Preprocessing (`classifier.py`)
In `ml-service/app/classifier.py`, the core text preprocessor used by both training and inference is defined as:
```python
def preprocess_text(text: str) -> str:
    # ...
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    # ...
```
- **Consequence:** The regular expression `[^a-z0-9\s]` explicitly strips all non-ASCII characters. Every single Kannada glyph (e.g., `ನ`, `ನ್`, `ನ`, `ಬ್ಯಾಂ`, `ಕ್`) and Devanagari glyph (e.g., `म`, `े`, `र`, `े`, `ब`, `ैं`, `क`) is deleted.
- A 60-character Kannada grievance is reduced to an empty string `""` before it even reaches the TF-IDF vectorizer.

### Defect 2: Latin-Only Word Tokenization in `scenario_validator.py`
In `ml-service/app/scenario_validator.py`, legal concept presence is verified using:
```python
tokens = set(re.findall(r"[a-z]{3,}", text_lower))
```
- **Consequence:** The token extractor only matches sequences of Latin ASCII characters `[a-z]`. For native Indic scripts, `tokens` is completely empty (`set()`).
- Because `len(matched_legal) == 0`, the validator triggers:
  ```python
  if len(matched_legal) == 0:
      return ScenarioEvaluation(
          is_valid=False,
          fallback_message=FALLBACK_MESSAGE,
          reason="no_legal_concepts_detected",
          effective_issue=effective_issue,
      )
  ```
  Every valid Kannada and Hindi legal complaint is falsely flagged as non-legal chatter or gibberish.

### Defect 3: Naive Script Range Detection in the API Gateway (`backend/src/translator.js`)
The API gateway relied on a basic Unicode range check:
```javascript
function detectScript(text) {
  if (/[\u0C80-\u0CFF]/.test(text)) return "kn";
  if (/[\u0900-\u097F]/.test(text)) return "hi";
  return "en";
}
```
- **Consequence:** Romanized Kannada ("Kanglish") and Romanized Hindi ("Hinglish") contain zero Indic Unicode code points. They are strictly Latin alphabet strings.
- `detectScript` returned `"en"` for Romanized text.
- The gateway treated Romanized text as standard English, sent it untranslated to the ML service, and the English TF-IDF vectorizer failed to comprehend colloquial Indic words (*"duddu"*, *"kat gaye"*, *"illade"*, *"bina"*).

### Defect 4: Single-Language Knowledge Base Assumption
- In `knowledge_base/issue_mappings.json`, all 214 issues were curated with English-only prototype phrases (`prototype_texts`).
- In `ml-service/data/training_data_v2.csv`, all 2,383 training rows were exclusively written in English.
- Cosine similarity between an English TF-IDF space and Indic tokens is mathematically zero, creating a hard linguistic barrier.

### Defect 5: Gateway Translation Failure Vulnerability
- The gateway attempted to translate Indic text to English using an undocumented Google web endpoint (`https://translate.googleapis.com/translate_a/single?client=gtx`).
- This external network dependency is fragile: it fails under offline operation, network latency, or IP rate-limiting, silently falling back to the original text which then crashed the ML service.
- Direct API calls to `ml-service` (`POST /analyze`) completely bypass the gateway, rendering `ml-service` incapable of serving multilingual requests independently.

---

## 3. Baseline Metric Measurements (Pre-Fix)

A diagnostic evaluation was executed across 25 parallel legal scenarios in 5 language formats (English, Kannada, Hindi, Romanized Kannada, Romanized Hindi):

| Language / Format | Script Detected | Domain Accuracy | Issue Accuracy | Valid Scenario % | Provs Retrieved |
|---|:---:|:---:|:---:|:---:|:---:|
| **English** | Latin (100%) | **100.0%** | **84.0%** | 100.0% | 100.0% |
| **Kannada (ಕನ್ನಡ)** | Kannada (100%) | **0.0%** | **0.0%** | **0.0%** | **0.0%** |
| **Hindi (हिन्दी)** | Devanagari (100%) | **0.0%** | **0.0%** | **0.0%** | **0.0%** |
| **Romanized Kannada** | Misdetected as English | **40.0%** | **8.0%** | 44.0% | 40.0% |
| **Romanized Hindi** | Misdetected as English | **48.0%** | **12.0%** | 52.0% | 48.0% |
| **Cross-Language Consistency** | — | — | **4.0%** | — | — |

*Note: In 96% of cross-language comparisons, identical legal scenarios produced completely divergent outputs across languages.*

---

## 4. Architectural Fix Plan

To make LegalLens genuinely multilingual without breaking the 4-module architecture or relying on external generative LLMs, the following components must be implemented:

1. **Multilingual NLP Module (`ml-service/app/multilingual.py`):**
   - Unicode NFKC normalization and diacritic cleaner.
   - Script & language detection supporting `kn`, `hi`, `en`, `kn-Latn`, `hi-Latn`, and mixed code-switching.
   - High-precision Indic legal canonicalization (mapping native Kannada, Hindi, and Romanized terms to canonical legal concepts).
2. **Unicode-Preserving Preprocessor (`classifier.py` & `scenario_validator.py`):**
   - Replace ASCII-only regexes with Unicode-aware tokenizers (`\w+`).
   - Add multilingual legal keyword dictionaries for Kannada and Hindi.
3. **Multilingual Issue Retriever (`issue_detector.py`):**
   - Multi-representation cosine matching: matches against native prototypes and canonical legal concepts.
   - Enrich knowledge-base prototypes with verified Kannada, Hindi, Kanglish, and Hinglish phrases.
4. **Multilingual Training & Benchmark Expansion:**
   - Expand `training_data_v2.csv` with multilingual and code-mixed examples.
   - Build a 250-scenario multilingual test benchmark covering all 5 domains and language modes.
5. **Cross-Language Consistency Test Suite:**
   - Automated tests verifying that identical scenarios in English, Kannada, Hindi, Kanglish, and Hinglish retrieve the same domain and issue.
