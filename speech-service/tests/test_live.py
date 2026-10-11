"""Integration tests for live faster-whisper transcription.

Runs actual inference with the local Whisper 'small' model on CPU with int8.
Validates end-to-end execution with real audio bytes.
"""

from __future__ import annotations

import io
import math
import os
import tempfile
import unittest
import wave

import sys
from pathlib import Path

speech_dir = Path(__file__).resolve().parents[1]
if str(speech_dir) not in sys.path:
    sys.path.insert(0, str(speech_dir))

from app.transcriber import SpeechTranscriber


def generate_tone_wav(duration_s: float = 1.0, freq_hz: float = 440.0) -> bytes:
    """Generate a valid PCM WAV audio file with a sine tone."""
    sample_rate = 16000
    num_samples = int(sample_rate * duration_s)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            sample_val = int(16000 * math.sin(2 * math.pi * freq_hz * (i / sample_rate)))
            frames.extend(sample_val.to_bytes(2, byteorder="little", signed=True))
        wav_file.writeframes(frames)
    return buf.getvalue()


class TestLiveWhisperTranscriber(unittest.TestCase):
    """Verifies actual WhisperModel 'small' loaded and executing locally."""

    @classmethod
    def setUpClass(cls):
        cls.transcriber = SpeechTranscriber(
            model_size="small",
            device="cpu",
            compute_type="int8",
        )
        cls.transcriber.load_model()

    def test_live_model_is_loaded(self):
        """Verifies model reports is_loaded True."""
        self.assertTrue(self.transcriber.is_loaded)

    def test_live_transcribe_audio_file(self):
        """Verifies transcribe executes without error on a real WAV file."""
        wav_data = generate_tone_wav(duration_s=1.5, freq_hz=300.0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(wav_data)
            temp_path = f.name

        try:
            transcript, lang, prob, duration = self.transcriber.transcribe(temp_path)
            # Duration should be close to 1.5s
            self.assertGreater(duration, 0.5)
            # Language code should be a string (e.g. 'en')
            self.assertIsInstance(lang, str)
            self.assertGreaterEqual(prob, 0.0)
            self.assertLessEqual(prob, 1.0)
            self.assertIsInstance(transcript, str)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_live_transcribe_with_language_hints(self):
        """Verifies passing language hints ('en', 'hi', 'kn') works cleanly."""
        wav_data = generate_tone_wav(duration_s=1.0, freq_hz=440.0)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(wav_data)
            temp_path = f.name

        try:
            for target_lang in ["en", "hi", "kn"]:
                transcript, lang, prob, duration = self.transcriber.transcribe(
                    temp_path,
                    language=target_lang,
                )
                self.assertEqual(lang, target_lang)
                self.assertIsInstance(transcript, str)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()
