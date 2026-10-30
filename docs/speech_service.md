# Speech Service & Multilingual Voice Input Documentation

**LegalLens — Hybrid AI-Powered Legal Awareness System**

This document covers the implementation, operations, testing, and multilingual considerations for the **Speech Service** (`speech-service/`).

---

## 1. Overview & Architecture

The Speech Service enables Indian citizens to dictate their legal complaints in **English**, **हिन्दी (Hindi)**, or **ಕನ್ನಡ (Kannada)** using a local automatic speech recognition (ASR) engine.

### Architectural Principles

1. **Local & Private:** Runs entirely on-device (laptop CPU) using `faster-whisper` (`small` model with `int8` quantization). Audio is processed locally and never transmitted to external APIs or third parties.
2. **Strict Separation of Concerns:** The speech service **only transcribes audio and detects language**. It does not classify legal domains, retrieve statutes, or generate legal advice.
3. **Preservation of Original Wording:** Spoken Hindi is transcribed in Devanagari script, Kannada in Kannada script, and English in Latin script. The service **does not perform silent translation**.
4. **Editable Transcript:** The transcribed text is populated directly into the complaint form, allowing the citizen to review, correct names/dates/details, and submit it to the existing LegalLens legal analysis pipeline.
5. **Privacy by Design:** Temporary audio files are deleted immediately after transcription via `try...finally` blocks. Neither user audio recordings nor transcribed complaint text are written to server log files.

---

## 2. Port & Service Topology

| Service | Technology | Port | Binding | Purpose |
|---|---|---|---|---|
| **Speech Service** | FastAPI / `faster-whisper` | `8001` | `127.0.0.1` | Local voice recording transcription & language detection |
| **ML Service** | FastAPI / Scikit-learn | `8000` | `127.0.0.1` | Legal domain classification & issue prototype matching |
| **API Gateway** | Node.js / Express | `5000` | `127.0.0.1` | Validation, rate-limiting, script bridging, anonymized logging |
| **Frontend** | React / Vite | `3000` | `localhost` | Citizen-facing interface with microphone & text input |

---

## 3. Setup & Activation

### Step 1: Environment Activation
The dedicated Python virtual environment is located at `speech-service/.venv`.

```bash
# From project root
source speech-service/.venv/bin/activate
```

### Step 2: Install or Verify Dependencies
The dependencies are defined in `speech-service/requirements.txt`:
- `faster-whisper` (1.2.1+)
- `fastapi` (0.115.0+)
- `uvicorn[standard]` (0.30.0+)
- `python-multipart` (0.0.12+)
- `pydantic` (2.8.0+)

```bash
pip install -r speech-service/requirements.txt
```

*Note:* System FFmpeg (version 9.0+) is already installed on Omarchy Linux.

---

## 4. Running the Speech Service

Run the service bound to loopback (`127.0.0.1`) on port `8001`:

```bash
# Option A: From speech-service directory
cd speech-service
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload

# Option B: From project root
speech-service/.venv/bin/uvicorn app.main:app --app-dir speech-service --host 127.0.0.1 --port 8001
```

### Health Check Verification

```bash
curl http://127.0.0.1:8001/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "speech-service",
  "model_size": "small",
  "device": "cpu",
  "compute_type": "int8",
  "model_loaded": true,
  "supported_languages": ["en", "hi", "kn"]
}
```

---

## 5. API Reference

### `GET /health`
Returns service status, model configuration, and memory loaded state.

### `POST /transcribe`
Accepts a multipart audio upload and returns the transcript, language code, and language confidence.

**Request:**
- `file`: Audio file (`audio/webm`, `audio/ogg`, `audio/wav`, `audio/mp4`, `audio/mp3`, `audio/flac`)
- `language` *(optional)*: Language hint (`en`, `hi`, `kn`, or omitted for auto-detection)

**Response (`200 OK`):**
```json
{
  "transcript": "Someone called pretending to be a bank manager and asked for OTP",
  "language": "en",
  "language_probability": 0.985,
  "duration": 4.25
}
```

**Error Codes:**
- `400 Bad Request`: Empty recording, unsupported file format, or corrupted audio stream.
- `413 Content Too Large`: Audio upload exceeds 25 MB limit.
- `503 Service Unavailable`: Whisper model not loaded into memory.

---

## 6. Testing

### Automated Unit Tests (Mocked Whisper)
Runs in < 0.1s without downloading or executing the neural network:

```bash
speech-service/.venv/bin/python -m unittest speech-service/tests/test_api.py
```

Tests cover:
- Health check loaded and degraded modes
- English, Hindi, and Kannada transcription responses
- Empty upload validation (400)
- Unsupported format rejection (400)
- Oversized upload rejection (413)
- Corrupted audio decoding handling (400)
- Unloaded model rejection (503)

### Automated Live Integration Tests (Real Whisper Model)
Tests actual inference using the local Whisper `small` model on CPU with int8:

```bash
speech-service/.venv/bin/python -m unittest speech-service/tests/test_live.py
```

### Backend Voice Integration & Regression Tests
Validates the gateway's acceptance of transcribed complaints, script detection, and typed complaint regression:

```bash
cd backend && npm test
```

### Frontend Build & Typecheck
Ensures TypeScript contracts, hooks, and build bundles are strictly verified:

```bash
cd frontend && npm run build
```

---

## 7. Manual Testing Procedure for Hindi, Kannada, and English

To test voice input directly in the browser:

1. **Start all 4 services:**
   - ML Service on `8000`: `cd ml-service && source venv/bin/activate && uvicorn app.main:app --port 8000`
   - Speech Service on `8001`: `speech-service/.venv/bin/uvicorn app.main:app --app-dir speech-service --host 127.0.0.1 --port 8001`
   - Backend Gateway on `5000`: `cd backend && npm run dev`
   - Frontend on `3000`: `cd frontend && npm run dev`
2. **Open browser:** Navigate to `http://localhost:3000`.
3. **Test English Scenario:**
   - Click **Voice Input (Record)**.
   - Speak: *"Someone called pretending to be bank manager and asked for OTP, then money was debited from my account."*
   - Click **Done Recording**.
   - Verify transcript appears in English with `Transcribed in English` badge.
   - Click **RUN LEGAL ANALYSIS** and verify IT Act Section 66D is identified.
4. **Test Hindi (हिन्दी) Scenario:**
   - Click **Voice Input (Record)**.
   - Speak: *"किसी ने बैंक अधिकारी बनकर फोन किया और मुझसे ओटीपी मांगा, जिसके बाद मेरे खाते से पैसे कट गए।"*
   - Click **Done Recording**.
   - Verify transcript appears in Devanagari script with `Transcribed in हिन्दी (Hindi)` badge.
   - Click **RUN LEGAL ANALYSIS** and verify the result is correctly displayed.
5. **Test Kannada (ಕನ್ನಡ) Scenario:**
   - Click **Voice Input (Record)**.
   - Speak: *"ಯಾರೋ ಬ್ಯಾಂಕ್ ಮ್ಯಾನೇಜರ್ ಎಂದು ಕರೆ ಮಾಡಿ ಒಟಿಪಿ ಕೇಳಿದರು, ನಂತರ ನನ್ನ ಖಾತೆಯಿಂದ ಹಣ ಕಡಿತವಾಯಿತು."*
   - Click **Done Recording**.
   - Verify transcript appears in Kannada script with `Transcribed in ಕನ್ನಡ (Kannada)` badge.
   - Click **RUN LEGAL ANALYSIS** and verify legal guidance is retrieved.
6. **Test Transcript Editing:**
   - Record an audio clip.
   - In the textarea, change or add words (e.g., add date or bank name).
   - Verify the edited text is what gets submitted to analysis.
7. **Test Typed Input Regression:**
   - Directly type a scenario without using the microphone.
   - Verify typing works exactly as before.

---

## 8. Multilingual NLP Considerations & Downstream Limitations

### Whisper ASR Performance & Script Normalization
- **English (`en`):** Highly accurate transcription on Whisper `small`.
- **Hindi (`hi`):** Reliable transcription in Devanagari script for standard speech. Includes automatic acronym normalization (e.g. `ओटीपी` -> `ओटीपी (OTP)`) and anti-repetition token filtering (`repetition_penalty=1.2`, `no_repeat_ngram_size=3`) to prevent trailing stutter loops.
- **Kannada (`kn`):** Supported with language selection and prompt priming. When Whisper's BPE tokenizer decodes phonetic Kannada into Devanagari Unicode, the service automatically converts Devanagari characters (`0x0900-0x097F`) into native Kannada script (`0x0C80-0x0CFF`) and normalizes Kannada acronyms (`ಒಟಿಪಿ` -> `ಒಟಿಪಿ (OTP)`).

### Downstream ML Pipeline Support & Threshold Calibration
- **Current ML Architecture:** The existing LegalLens `DomainClassifier` (Logistic Regression with TF-IDF) and `IssueDetector` (cosine similarity over prototype texts in `issue_mappings.json`) are **strictly trained and curated on English text**.
- **Issue Similarity Threshold Calibration:** The `min_similarity_threshold` in `IssueDetector` is set to `0.12` (configurable via `MIN_SIMILARITY_THRESHOLD` environment variable). In high-dimensional TF-IDF space across 120 issues, natural translated complaints score between 0.14 and 0.22; calibrating the threshold from the legacy 0.22 to 0.12 ensures authentic complaints match verified statutory provisions while vague inputs (< 0.10) continue to trigger honest clarification warnings.
- **Indic Script Bridging:** To support typed or dictated Hindi and Kannada without replacing the verified legal knowledge base:
  1. The user can select their spoken language (`Auto`, `English`, `हिन्दी`, `ಕನ್ನಡ`) in the microphone interface.
  2. The speech service transcribes audio into the speaker's native script (Devanagari or Kannada) with script normalization.
  3. The user sees and edits the original transcript in their own language.
  4. The API Gateway detects Devanagari/Kannada Unicode code points (or uses explicit language hints) and bridges the text to English via a cached translation layer before passing it to the ML service.
  5. The result cards on the frontend are translated back dynamically to Hindi or Kannada using the result localization engine.
- **Recommended Future Enhancement (Phase 2):** For true end-to-end native Indic legal NLP without intermediate translation, fine-tune an **IndicBERT** or **multilingual embedding model** (such as `Indic-Sentence-BERT` or `multilingual-e5-small`) directly on multilingual legal prototype pairs, ensuring legal negation ("salary not paid" vs "salary paid") and statutory terminology are natively matched.

