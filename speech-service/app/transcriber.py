"""Transcriber wrapper using faster-whisper.

Handles model loading, audio decoding, and language detection.
Runs locally on CPU with int8 quantization.
Preserves original spoken language and wording (no silent translation).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Tuple

# Compatibility patch: PyAV 14+ removed the 'metadata_errors' parameter from av.open.
# faster-whisper 1.2.x still passes metadata_errors='ignore', which raises a TypeError in av 19+.
try:
    import av

    _orig_av_open = av.open

    def _safe_av_open(*args, **kwargs):
        kwargs.pop("metadata_errors", None)
        return _orig_av_open(*args, **kwargs)

    av.open = _safe_av_open
except ImportError:
    pass

logger = logging.getLogger("speech_service.transcriber")


class SpeechTranscriber:
    """Wrapper around faster-whisper WhisperModel."""

    def __init__(
        self,
        model_size: str = "small",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model = None

    @property
    def is_loaded(self) -> bool:
        """Returns True if the Whisper model is loaded in memory."""
        return self._model is not None

    def load_model(self) -> None:
        """Loads the Whisper model into memory.

        Should be called once during application startup.
        """
        from faster_whisper import WhisperModel

        logger.info(
            "Loading faster-whisper model '%s' (device=%s, compute_type=%s)...",
            self.model_size,
            self.device,
            self.compute_type,
        )
        self._model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
        )
        logger.info("faster-whisper model '%s' successfully loaded into memory.", self.model_size)

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
    ) -> Tuple[str, str, float, float]:
        """Transcribes the given audio file using faster-whisper.

        Args:
            audio_path: Path to the audio file on disk.
            language: Optional explicit language code (e.g. 'en', 'hi', 'kn').
                      If None or empty, auto-detects language.

        Returns:
            Tuple of:
            - transcript: Transcribed text string
            - language: Detected/used language code
            - language_probability: Confidence score (0.0 to 1.0)
            - duration: Audio duration in seconds

        Raises:
            RuntimeError: If model is not loaded.
            Exception: If audio decoding or transcription fails.
        """
        if not self.is_loaded or self._model is None:
            raise RuntimeError("Whisper model is not loaded in memory.")

        # Ensure task is strictly 'transcribe' so no translation occurs
        segments_gen, info = self._model.transcribe(
            audio_path,
            language=language if language and language != "auto" else None,
            task="transcribe",
            beam_size=5,
            temperature=0.0,
            vad_filter=False,
        )

        # Iterate segments to materialize transcript
        segment_texts = []
        for segment in segments_gen:
            text = segment.text.strip()
            if text:
                segment_texts.append(text)

        transcript = " ".join(segment_texts).strip()

        detected_language = info.language or "unknown"
        language_probability = float(info.language_probability) if info.language_probability is not None else 0.0
        duration = float(info.duration) if info.duration is not None else 0.0

        return transcript, detected_language, language_probability, duration
