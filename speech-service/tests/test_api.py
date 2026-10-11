"""Unit tests for LegalLens Speech Service API.

Mocks the heavier Whisper model so tests execute fast, deterministically,
and without requiring external network access.
"""

from __future__ import annotations

import io
import os
import unittest
from unittest.mock import MagicMock, patch

from starlette.testclient import TestClient

# Ensure speech-service root is on python path
import sys
from pathlib import Path

speech_dir = Path(__file__).resolve().parents[1]
if str(speech_dir) not in sys.path:
    sys.path.insert(0, str(speech_dir))

from app.main import app, transcriber


def create_dummy_wav_bytes() -> bytes:
    """Generate minimal valid PCM WAV bytes."""
    import wave

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes(b"\x00\x00" * 1600)  # 0.1s of silence
    return buf.getvalue()


class TestSpeechServiceHealth(unittest.TestCase):
    """Tests for GET /health endpoint."""

    def setUp(self):
        self.client = TestClient(app)

    def test_health_when_model_loaded(self):
        """GET /health should return ok and model_loaded: true."""
        with patch.object(transcriber, "_model", new=MagicMock()):
            response = self.client.get("/health")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "ok")
            self.assertEqual(data["service"], "speech-service")
            self.assertEqual(data["model_size"], "small")
            self.assertEqual(data["device"], "cpu")
            self.assertEqual(data["compute_type"], "int8")
            self.assertTrue(data["model_loaded"])
            self.assertIn("en", data["supported_languages"])
            self.assertIn("hi", data["supported_languages"])
            self.assertIn("kn", data["supported_languages"])

    def test_health_when_model_not_loaded(self):
        """GET /health should return degraded when model is None."""
        with patch.object(transcriber, "_model", new=None):
            response = self.client.get("/health")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "degraded")
            self.assertFalse(data["model_loaded"])


class TestSpeechServiceTranscribe(unittest.TestCase):
    """Tests for POST /transcribe endpoint."""

    def setUp(self):
        self.client = TestClient(app)
        self.wav_bytes = create_dummy_wav_bytes()

    def test_transcribe_valid_audio_english(self):
        """POST /transcribe returns expected transcript and detected language for English."""
        mock_result = (
            "Someone called pretending to be bank manager and asked for OTP",
            "en",
            0.985,
            3.2,
        )
        with patch.object(transcriber, "_model", new=MagicMock()), \
             patch.object(transcriber, "transcribe", return_value=mock_result):

            response = self.client.post(
                "/transcribe",
                files={"file": ("recording.wav", self.wav_bytes, "audio/wav")},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["transcript"], mock_result[0])
            self.assertEqual(data["language"], "en")
            self.assertAlmostEqual(data["language_probability"], 0.985, places=3)
            self.assertAlmostEqual(data["duration"], 3.2, places=1)

    def test_transcribe_valid_audio_hindi(self):
        """POST /transcribe returns Hindi transcript and language code 'hi'."""
        mock_result = (
            "किसी ने बैंक अधिकारी बनकर फोन किया और मुझसे ओटीपी मांगा",
            "hi",
            0.992,
            4.1,
        )
        with patch.object(transcriber, "_model", new=MagicMock()), \
             patch.object(transcriber, "transcribe", return_value=mock_result):

            response = self.client.post(
                "/transcribe",
                files={"file": ("recording.webm", self.wav_bytes, "audio/webm")},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["transcript"], mock_result[0])
            self.assertEqual(data["language"], "hi")
            self.assertAlmostEqual(data["language_probability"], 0.992, places=3)

    def test_transcribe_valid_audio_kannada(self):
        """POST /transcribe returns Kannada transcript and language code 'kn'."""
        mock_result = (
            "ಯಾರೋ ಬ್ಯಾಂಕ್ ಮ್ಯಾನೇಜರ್ ಎಂದು ಕರೆ ಮಾಡಿ ಒಟಿಪಿ ಕೇಳಿದರು",
            "kn",
            0.978,
            3.8,
        )
        with patch.object(transcriber, "_model", new=MagicMock()), \
             patch.object(transcriber, "transcribe", return_value=mock_result):

            response = self.client.post(
                "/transcribe",
                files={"file": ("recording.ogg", self.wav_bytes, "audio/ogg")},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["transcript"], mock_result[0])
            self.assertEqual(data["language"], "kn")
            self.assertAlmostEqual(data["language_probability"], 0.978, places=3)

    def test_transcribe_empty_upload_fails(self):
        """POST /transcribe rejects 0-byte audio upload with HTTP 400."""
        with patch.object(transcriber, "_model", new=MagicMock()):
            response = self.client.post(
                "/transcribe",
                files={"file": ("empty.wav", b"", "audio/wav")},
            )
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertIn("empty", data["detail"].lower())

    def test_transcribe_unsupported_format_fails(self):
        """POST /transcribe rejects non-audio file formats with HTTP 400."""
        with patch.object(transcriber, "_model", new=MagicMock()):
            response = self.client.post(
                "/transcribe",
                files={"file": ("document.pdf", b"%PDF-1.4 dummy", "application/pdf")},
            )
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertIn("unsupported audio format", data["detail"].lower())

    def test_transcribe_excessive_size_fails(self):
        """POST /transcribe rejects uploads exceeding size limit with HTTP 413."""
        with patch.object(transcriber, "_model", new=MagicMock()), \
             patch("app.config.MAX_FILE_SIZE_BYTES", 100):  # 100 bytes limit for test

            oversized_bytes = b"\x00" * 500
            response = self.client.post(
                "/transcribe",
                files={"file": ("big.wav", oversized_bytes, "audio/wav")},
            )
            self.assertEqual(response.status_code, 413)
            data = response.json()
            self.assertIn("exceeds maximum allowed size", data["detail"].lower())

    def test_transcribe_corrupted_audio_fails(self):
        """POST /transcribe handles corrupted audio decoding gracefully with HTTP 400."""
        with patch.object(transcriber, "_model", new=MagicMock()), \
             patch.object(
                 transcriber,
                 "transcribe",
                 side_effect=Exception("Invalid data found when processing input: demuxer error"),
             ):

            response = self.client.post(
                "/transcribe",
                files={"file": ("corrupt.wav", self.wav_bytes, "audio/wav")},
            )
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertIn("corrupted", data["detail"].lower())

    def test_transcribe_model_unavailable(self):
        """POST /transcribe returns HTTP 503 if model is not loaded."""
        with patch.object(transcriber, "_model", new=None):
            response = self.client.post(
                "/transcribe",
                files={"file": ("recording.wav", self.wav_bytes, "audio/wav")},
            )
            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertIn("not loaded", data["detail"].lower())


if __name__ == "__main__":
    unittest.main()
