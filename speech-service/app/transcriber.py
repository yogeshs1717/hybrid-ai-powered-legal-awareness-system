"""Transcriber wrapper using faster-whisper.

Handles model loading, audio decoding, repetition suppression, and script normalization.
Runs locally on CPU with int8 quantization.
Preserves original spoken language and wording (no silent translation).
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
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


def convert_to_wav_16k(audio_path: str) -> Tuple[str, bool]:
    """Convert any incoming audio file to standard 16kHz mono 16-bit PCM WAV using ffmpeg.

    This ensures complete compatibility with browser MediaRecorder WebM/Opus, OGG, and MP4 formats,
    repairing missing metadata headers and demuxing reliably.

    Returns:
        Tuple of (effective_audio_path, is_temporary_file).
    """
    out_path = f"{audio_path}.16k.wav"
    try:
        cmd = [
            "ffmpeg",
            "-y",
            "-nostdin",
            "-threads",
            "1",
            "-i",
            audio_path,
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            out_path,
        ]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=20,
        )
        if result.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return out_path, True
        logger.warning(
            "ffmpeg audio conversion exited with code %d: %s. Using original audio file.",
            result.returncode,
            result.stderr.decode("utf-8", errors="replace"),
        )
    except Exception as exc:
        logger.warning("ffmpeg audio conversion encountered error: %s. Using original audio file.", exc)

    return audio_path, False

# Unicode mapping from Devanagari (0x0900-0x097F) to Kannada (0x0C80-0x0CFF)
# Used when Whisper outputs Kannada phonetics in Devanagari script.
DEV_TO_KN_MAP = {
    # Independent vowels
    "\u0905": "\u0C85",  # A
    "\u0906": "\u0C86",  # AA
    "\u0907": "\u0C87",  # I
    "\u0908": "\u0C88",  # II
    "\u0909": "\u0C89",  # U
    "\u090A": "\u0C8A",  # UU
    "\u090B": "\u0C8B",  # Vocalic R
    "\u090E": "\u0C8E",  # Short E
    "\u090F": "\u0C8F",  # E -> Long E
    "\u0910": "\u0C90",  # AI
    "\u0912": "\u0C92",  # Short O
    "\u0913": "\u0C93",  # O -> Long O
    "\u0914": "\u0C94",  # AU
    # Signs
    "\u0901": "\u0C81",  # Candrabindu
    "\u0902": "\u0C82",  # Anusvara
    "\u0903": "\u0C83",  # Visarga
    # Consonants
    "\u0915": "\u0C95",  # KA
    "\u0916": "\u0C96",  # KHA
    "\u0917": "\u0C97",  # GA
    "\u0918": "\u0C98",  # GHA
    "\u0919": "\u0C99",  # NGA
    "\u091A": "\u0C9A",  # CA
    "\u091B": "\u0C9B",  # CHA
    "\u091C": "\u0C9C",  # JA
    "\u091D": "\u0C9D",  # JHA
    "\u091E": "\u0C9E",  # NYA
    "\u091F": "\u0C9F",  # TTA
    "\u0920": "\u0CA0",  # TTHA
    "\u0921": "\u0CA1",  # DDA
    "\u0922": "\u0CA2",  # DDHA
    "\u0923": "\u0CA3",  # NNA
    "\u0924": "\u0CA4",  # TA
    "\u0925": "\u0CA5",  # THA
    "\u0926": "\u0CA6",  # DA
    "\u0927": "\u0CA7",  # DHA
    "\u0928": "\u0CA8",  # NA
    "\u092A": "\u0CAA",  # PA
    "\u092B": "\u0CAB",  # PHA
    "\u092C": "\u0CAC",  # BA
    "\u092D": "\u0CAD",  # BHA
    "\u092E": "\u0CAE",  # MA
    "\u092F": "\u0CAF",  # YA
    "\u0930": "\u0CB0",  # RA
    "\u0932": "\u0CB2",  # LA
    "\u0933": "\u0CB3",  # LLA
    "\u0935": "\u0CB5",  # VA
    "\u0936": "\u0CB6",  # SHA
    "\u0937": "\u0CB7",  # SSA
    "\u0938": "\u0CB8",  # SA
    "\u0939": "\u0CB9",  # HA
    # Dependent vowel signs (Matras)
    "\u093E": "\u0CBE",  # AA sign
    "\u093F": "\u0CBF",  # I sign
    "\u0940": "\u0CC0",  # II sign
    "\u0941": "\u0CC1",  # U sign
    "\u0942": "\u0CC2",  # UU sign
    "\u0943": "\u0CC3",  # Vocalic R sign
    "\u0944": "\u0CC4",  # Vocalic RR sign
    "\u0946": "\u0CC6",  # Short E sign
    "\u0947": "\u0CC7",  # E sign -> Long E sign
    "\u0948": "\u0CC8",  # AI sign
    "\u094A": "\u0CCA",  # Short O sign
    "\u094B": "\u0CCB",  # O sign -> Long O sign
    "\u094C": "\u0CCC",  # AU sign
    "\u094D": "\u0CCD",  # Virama (halant)
    # Nukhtas & Urdu/Persian sounds mapped to Kannada bases
    "\u0958": "\u0C95",  # QA -> KA
    "\u0959": "\u0C96",  # KHHA -> KHA
    "\u095A": "\u0C97",  # GHHA -> GA
    "\u095B": "\u0C9C",  # ZA -> JA
    "\u095C": "\u0CA1",  # DDDHA -> DDA
    "\u095D": "\u0CA2",  # RHA -> DDHA
    "\u095E": "\u0CAB",  # FA -> PHA
    # Digits
    "\u0966": "\u0CE6",  # 0
    "\u0967": "\u0CE7",  # 1
    "\u0968": "\u0CE8",  # 2
    "\u0969": "\u0CE9",  # 3
    "\u096A": "\u0CEA",  # 4
    "\u096B": "\u0CEB",  # 5
    "\u096C": "\u0CEC",  # 6
    "\u096D": "\u0CED",  # 7
    "\u096E": "\u0CEE",  # 8
    "\u096F": "\u0CEF",  # 9
    # Punctuation
    "\u0964": ".",       # Danda
    "\u0965": ".",       # Double danda
}


def devanagari_to_kannada(text: str) -> str:
    """Converts text containing Devanagari script into native Kannada script."""
    text = text.replace("\u093C", "")  # strip nukhta
    res = []
    for ch in text:
        if ch in DEV_TO_KN_MAP:
            res.append(DEV_TO_KN_MAP[ch])
        elif 0x0900 <= ord(ch) <= 0x097F:
            kn_cp = ord(ch) + 0x0380
            res.append(chr(kn_cp))
        else:
            res.append(ch)
    return "".join(res)


def clean_repetitions(text: str) -> str:
    """Removes pathological repeating loops from Whisper hallucinations."""
    if not text:
        return text
    # Clean excessive repeating single characters (e.g. 'ಸಾರಿಲಿಲಿಲಿಲಿಲಿಲಿ')
    cleaned = re.sub(r"([^\s])\1{3,}", r"\1", text)
    # Clean repeating phrases
    for n in range(6, 1, -1):
        cleaned = re.sub(rf"((?:\S+\s*){{{n}}})\1{{2,}}", r"\1", cleaned)
    return cleaned.strip()


def normalize_acronyms(text: str, lang: str) -> str:
    """Normalizes spoken acronyms in Hindi and Kannada so downstream analysis recognizes them."""
    if not text:
        return text

    if lang == "kn":
        # Kannada acronyms
        text = re.sub(r"(?<![^\s])(ಒ\s*ಟಿ\s*ಪಿ|ಒಟಿಪಿ|ಒಟೀಪೀ|ಓಟಿಪಿ)(?![^\s.,!?])", "ಒಟಿಪಿ (OTP)", text)
        text = re.sub(r"(?<![^\s])(ಎಫ್\s*ಐ\s*ಆರ್|ಎಫ್ಐಆರ್)(?![^\s.,!?])", "ಎಫ್ಐಆರ್ (FIR)", text)
        text = re.sub(r"(?<![^\s])(ಎ\s*ಟಿ\s*ಎಂ|ಎಟಿಎಂ)(?![^\s.,!?])", "ಎಟಿಎಂ (ATM)", text)
    elif lang == "hi":
        # Hindi acronyms
        text = re.sub(r"(?<![^\s])(ओ\s*टी\s*पी|ओटीपी|उटीपी)(?![^\s.,!?])", "ओटीपी (OTP)", text)
        text = re.sub(r"(?<![^\s])(एफ\s*आई\s*आर|एफआईआर|एफ़आईआर)(?![^\s.,!?])", "एफआईआर (FIR)", text)
        text = re.sub(r"(?<![^\s])(ए\s*टी\s*एम|एटीएम)(?![^\s.,!?])", "एटीएम (ATM)", text)

    return text



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

        norm_lang = language.strip().lower() if language and language != "auto" else None

        # Priming prompt: do NOT pass Kannada script prompt to Whisper because it poisons the decoder
        # Whisper decodes Kannada acoustically into phonetic Devanagari, which is then mapped to Kannada script
        initial_prompt = None
        if norm_lang == "hi":
            initial_prompt = "हिन्दी भाषा. बैंक, खाता, पैसे, धोखाधड़ी, शिकायत, ओटीपी, उपभोक्ता, वेतन, पुलिस."
        elif norm_lang == "en":
            initial_prompt = "Legal awareness complaint. Bank, fraud, scam, consumer, police, salary, agreement."

        # Configure anti-hallucination and transcription parameters
        # Convert audio to clean 16kHz mono WAV if possible for maximum format compatibility
        effective_path, is_temp = convert_to_wav_16k(audio_path)

        try:
            # vad_filter with min_silence_duration_ms=1000 and speech_pad_ms=400 ensures
            # non-speech / silence does not cause hallucination loops while preserving speech boundaries.
            segments_gen, info = self._model.transcribe(
                effective_path,
                language=norm_lang,
                task="transcribe",
                beam_size=5,
                temperature=0.0,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=1000, speech_pad_ms=400),
                condition_on_previous_text=False,
                repetition_penalty=1.05,
                initial_prompt=initial_prompt,
            )

            # Iterate segments to materialize transcript
            segment_texts = []
            for segment in segments_gen:
                text = segment.text.strip()
                if text:
                    segment_texts.append(text)

            raw_transcript = " ".join(segment_texts).strip()
        finally:
            if is_temp and os.path.exists(effective_path):
                try:
                    os.unlink(effective_path)
                except OSError:
                    pass

        # Clean repeating token loops
        transcript = clean_repetitions(raw_transcript)

        detected_language = norm_lang or (info.language or "unknown").lower()
        language_probability = float(info.language_probability) if info.language_probability is not None else 0.0
        duration = float(info.duration) if info.duration is not None else 0.0

        # Script normalization: If Kannada was spoken, ensure Devanagari is converted to native Kannada
        if detected_language == "kn":
            if re.search(r"[\u0900-\u097F]", transcript):
                transcript = devanagari_to_kannada(transcript)
            transcript = normalize_acronyms(transcript, "kn")
        elif detected_language == "hi":
            transcript = normalize_acronyms(transcript, "hi")

        return transcript, detected_language, language_probability, duration
