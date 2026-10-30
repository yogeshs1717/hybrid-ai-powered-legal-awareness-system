"""Multilingual Pipeline Tests for LegalLens.

Verifies:
1. Script and language identification for English, Kannada, Hindi, Romanized, and Code-mixed inputs.
2. Unicode normalization (NFKC, zero-width stripping).
3. Indic-to-canonical legal representation for deterministic retrieval.
4. Multilingual scenario validation (distinguishing genuine legal queries from conversational chit-chat).
5. Cross-language domain and statutory retrieval consistency across parallel scenarios.
6. End-to-end POST /analyze API responses in native Indic scripts.
"""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.multilingual import (
    detect_language_and_script,
    normalize_unicode,
    INDIC_TO_CANONICAL_LEGAL,
)
from app.schemas import AnalyzeResponse


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# -----------------------------------------------------------------------------
# 1. Script and Language Identification Tests
# -----------------------------------------------------------------------------
def test_language_detection_english():
    text = "Someone called me posing as a bank executive and asked for the OTP sent to my phone."
    info = detect_language_and_script(text)
    assert info.detected_language == "en"
    assert info.detected_script == "Latin"
    assert not info.is_code_mixed
    assert info.language_confidence > 0.80


def test_language_detection_kannada():
    text = "ಯಾರೋ ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿ ಎಂದು ಕರೆ ಮಾಡಿ ನನ್ನ ಮೊಬೈಲ್‌ಗೆ ಬಂದ ಒಟಿಪಿ ಪಡೆದುಕೊಂಡರು ಮತ್ತು ಹಣ ಕಡಿತವಾಯಿತು."
    info = detect_language_and_script(text)
    assert info.detected_language == "kn"
    assert info.detected_script == "Kannada"
    assert info.language_confidence > 0.80


def test_language_detection_hindi():
    text = "किसी ने बैंक अधिकारी बनकर फोन किया और फोन पर आया ओटीपी पूछा और तुरंत खाते से पैसे कट गए।"
    info = detect_language_and_script(text)
    assert info.detected_language == "hi"
    assert info.detected_script == "Devanagari"
    assert info.language_confidence > 0.80


def test_language_detection_kanglish():
    text = "Yaaro bank manager antha call madi OTP kedi nan account inda 50000 duddu cut madiddare."
    info = detect_language_and_script(text)
    assert info.detected_language in ("kn-Latn", "kn-en")
    assert info.detected_script == "Latin"
    assert info.is_code_mixed


def test_language_detection_hinglish():
    text = "Kisi ne bank manager ban kar call kiya aur OTP manga fir account se 50000 kat gaye."
    info = detect_language_and_script(text)
    assert info.detected_language in ("hi-Latn", "hi-en")
    assert info.detected_script == "Latin"
    assert info.is_code_mixed


def test_language_detection_code_mixed():
    text = "Delivered brand new washing machine with defective motor, showroom replacement kooda kodalla refund kooda illa."
    info = detect_language_and_script(text)
    assert info.is_code_mixed
    assert info.detected_language in ("kn-en", "kn-Latn")


# -----------------------------------------------------------------------------
# 2. Unicode Normalization Tests
# -----------------------------------------------------------------------------
def test_unicode_normalization_zero_width():
    raw = "ಖಾತೆಯಿಂದ\u200C ಹಣ\u200D ಕಡಿತವಾಯಿತು\uFEFF."
    normalized = normalize_unicode(raw)
    assert "\u200C" not in normalized
    assert "\u200D" not in normalized
    assert "\uFEFF" not in normalized
    assert "ಖಾತೆಯಿಂದ ಹಣ ಕಡಿತವಾಯಿತು." == normalized


def test_unicode_normalization_whitespace():
    raw = "  ಬ್ಯಾಂಕ್     ಖಾತೆಯಿಂದ    ಹಣ   "
    normalized = normalize_unicode(raw)
    assert normalized == "ಬ್ಯಾಂಕ್ ಖಾತೆಯಿಂದ ಹಣ"


# -----------------------------------------------------------------------------
# 3. Indic-to-Canonical Legal Concept Alignment
# -----------------------------------------------------------------------------
def test_canonical_alignment_cyber_fraud():
    text = "ನನ್ನ ಬ್ಯಾಂಕ್ ಖಾತೆಯಿಂದ ಹಣ ಕಡಿತವಾಗಿದೆ."
    info = detect_language_and_script(text)
    assert "[CANONICAL:" in info.canonical_text
    canonical_lower = info.canonical_text.lower()
    assert "bank" in canonical_lower
    assert "account" in canonical_lower


def test_canonical_alignment_cheque_bounce():
    text = "ಖಾತೆಯಲ್ಲಿ ಸಾಕಷ್ಟು ಹಣವಿಲ್ಲದೆ ಚೆಕ್ ಬೌನ್ಸ್ ಆಗಿದೆ."
    info = detect_language_and_script(text)
    canonical_lower = info.canonical_text.lower()
    assert "cheque bounce" in canonical_lower
    assert "section 138" in canonical_lower


def test_canonical_alignment_traffic():
    text = "ಸಂಚಾರ ಪೊಲೀಸರು ಕುಡಿದು ವಾಹನ ಚಾಲನೆ ಎಂದು ಬ್ರೀತ್‌ಅನಲೈಜರ್ ಪರೀಕ್ಷೆ ಇಲ್ಲದೆ ಚಲನ್ ಹಾಕಿದ್ದಾರೆ."
    info = detect_language_and_script(text)
    canonical_lower = info.canonical_text.lower()
    assert "traffic police" in canonical_lower
    assert "drunk driving" in canonical_lower
    assert "breathalyzer" in canonical_lower


# -----------------------------------------------------------------------------
# 4. Multilingual Scenario Validation Tests
# -----------------------------------------------------------------------------
def test_scenario_validator_accepts_kannada_legal_query(client):
    payload = {
        "scenario": "ನನ್ನ ಅನುಮತಿ ಅಥವಾ ಯಾವುದೇ ಒಟಿಪಿ ಹಂಚಿಕೊಳ್ಳದೆ ನನ್ನ ಬ್ಯಾಂಕ್ ಖಾತೆಯಿಂದ ಅನಧಿಕೃತವಾಗಿ 50000 ಹಣ ಕಡಿತವಾಗಿದೆ."
    }
    resp = client.post("/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_valid_scenario"] is True
    assert data["analysis"]["domain"]["id"] == "cyber_fraud"
    assert len(data["legal_provisions"]) > 0


def test_scenario_validator_accepts_hindi_legal_query(client):
    payload = {
        "scenario": "मेरी अनुमति या कोई ओटीपी साझा किए बिना मेरे बैंक खाते से अनधिकृत तरीके से 50000 रुपये काट लिए गए।"
    }
    resp = client.post("/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_valid_scenario"] is True
    assert data["analysis"]["domain"]["id"] == "cyber_fraud"
    assert len(data["legal_provisions"]) > 0


def test_scenario_validator_rejects_conversational_indic(client):
    payload = {
        "scenario": "ನಮಸ್ಕಾರ ನೀವು ಹೇಗಿದ್ದೀರಿ ನನಗೆ ಇಂದು ಒಂದು ಒಳ್ಳೆಯ ಜೋಕ್ ಹೇಳಿ ಕವಿತೆ ಬರೆಯಿರಿ."
    }
    resp = client.post("/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_valid_scenario"] is False
    assert data["analysis"]["domain"]["id"] == "unknown"
    assert data["fallback_message"] is not None


# -----------------------------------------------------------------------------
# 5. Cross-Language Consistency Tests
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "en_text, kn_text, hi_text, expected_domain",
    [
        (
            "Someone called me posing as a bank executive and asked for the OTP sent to my phone, and 50000 was debited immediately.",
            "ಯಾರೋ ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿ ಎಂದು ಕರೆ ಮಾಡಿ ನನ್ನ ಮೊಬೈಲ್‌ಗೆ ಬಂದ ಒಟಿಪಿ ಪಡೆದುಕೊಂಡರು ಮತ್ತು ತಕ್ಷಣವೇ 50000 ಹಣ ಕಡಿತವಾಯಿತು.",
            "किसी ने बैंक अधिकारी बनकर फोन किया और फोन पर आया ओटीपी पूछा, और तुरंत खाते से 50000 रुपये कट गए।",
            "cyber_fraud",
        ),
        (
            "The brand new refrigerator I purchased was delivered with a broken compressor, and the company refuses refund or replacement.",
            "ನಾನು ಖರೀದಿಸಿದ ಹೊಸ ರೆಫ್ರಿಜರೇಟರ್ ಮುರಿದ ಕಂಪ್ರೆಸರ್‌ನೊಂದಿಗೆ ಬಂದಿದ್ದು, ಕಂಪನಿಯು ಮರುಪಾವತಿ ಅಥವಾ ಬದಲಾವಣೆಯನ್ನು ನಿರಾಕರಿಸಿದೆ.",
            "मेरे द्वारा खरीदा गया नया फ्रिज खराब कंप्रेसर के साथ आया, और कंपनी पैसे वापस करने या बदलने से इनकार कर रही है।",
            "consumer_issues",
        ),
        (
            "Traffic police demanded Rs 10000 fine for drunk driving without administering any breathalyzer test or medical blood exam.",
            "ಸಂಚಾರ ಪೊಲೀಸರು ಯಾವುದೇ ಬ್ರೀತ್‌ಅನಲೈಜರ್ ಅಥವಾ ವೈದ್ಯಕೀಯ ರಕ್ತ ಪರೀಕ್ಷೆ ಮಾಡದೆ ಕುಡಿದು ವಾಹನ ಚಾಲನೆ ಎಂದು 10000 ದಂಡ ವಿಧಿಸಿದ್ದಾರೆ.",
            "ट्रैफिक पुलिस ने बिना कोई ब्रेथ एनालाइजर या मेडिकल टेस्ट किए शराब पीकर गाड़ी चलाने का 10000 रुपये का चालान काट दिया।",
            "traffic_enforcement",
        ),
        (
            "My employer has delayed paying my monthly salary for the past three months without any explanation or notice.",
            "ನನ್ನ ಉದ್ಯೋಗದಾತರು ಯಾವುದೇ ವಿವರಣೆ ಅಥವಾ ಸೂಚನೆಯಿಲ್ಲದೆ ಕಳೆದ ಮೂರು ತಿಂಗಳಿಂದ ನನ್ನ ಮಾಸಿಕ ವೇತನವನ್ನು ನೀಡಿಲ್ಲ.",
            "मेरे नियोक्ता ने बिना किसी स्पष्टीकरण या सूचना के पिछले तीन महीनों से मेरा मासिक वेतन रोक रखा है।",
            "workplace_wage",
        ),
        (
            "A business client issued a cheque of Rs 3 lakhs for goods delivered, but the bank returned it dishonoured with memo funds insufficient.",
            "ಸರಕು ಸರಬರಾಜಿಗಾಗಿ ವ್ಯಾಪಾರ ಗ್ರಾಹಕರು 3 ಲಕ್ಷದ ಚೆಕ್ ನೀಡಿದ್ದು, ಖಾತೆಯಲ್ಲಿ ಹಣವಿಲ್ಲ ಎಂದು ಬ್ಯಾಂಕ್ ಚೆಕ್ ಬೌನ್ಸ್ ಮಾಡಿ ವಾಪಸ್ ನೀಡಿದೆ.",
            "सप्लाई किए गए माल के लिए ग्राहक ने 3 लाख का चेक दिया था, लेकिन बैंक ने खाते में अपर्याप्त राशि का मेमो देकर चेक बाउंस कर दिया।",
            "contractual_disputes",
        ),
    ],
)
def test_cross_language_domain_agreement(client, en_text, kn_text, hi_text, expected_domain):
    resp_en = client.post("/analyze", json={"scenario": en_text}).json()
    resp_kn = client.post("/analyze", json={"scenario": kn_text}).json()
    resp_hi = client.post("/analyze", json={"scenario": hi_text}).json()

    # All three must match expected domain identically
    assert resp_en["analysis"]["domain"]["id"] == expected_domain
    assert resp_kn["analysis"]["domain"]["id"] == expected_domain
    assert resp_hi["analysis"]["domain"]["id"] == expected_domain

    # All three must agree on the same issue
    issue_en = resp_en["analysis"]["issue"]["id"]
    issue_kn = resp_kn["analysis"]["issue"]["id"]
    issue_hi = resp_hi["analysis"]["issue"]["id"]
    assert issue_en == issue_kn == issue_hi

    # All three must retrieve at least one statutory provision
    assert len(resp_en["legal_provisions"]) > 0
    assert len(resp_kn["legal_provisions"]) > 0
    assert len(resp_hi["legal_provisions"]) > 0


# -----------------------------------------------------------------------------
# 6. Response Schema Multilingual Fields
# -----------------------------------------------------------------------------
def test_response_multilingual_metadata_fields(client):
    payload = {"scenario": "ನನ್ನ ಬ್ಯಾಂಕ್ ಖಾತೆಯಿಂದ ಅನಧಿಕೃತವಾಗಿ ಹಣ ಕಡಿತವಾಗಿದೆ."}
    resp = client.post("/analyze", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    assert data["detected_language"] == "kn"
    assert data["detected_script"] == "Kannada"
    assert isinstance(data["language_confidence"], float)
    assert isinstance(data["is_code_mixed"], bool)
