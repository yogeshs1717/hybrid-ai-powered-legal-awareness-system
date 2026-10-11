"""FastAPI application entrypoint for LegalLens Speech Service (port 8001).

Provides local multilingual speech-to-text transcription using faster-whisper.
Complies with LegalLens architecture:
- Transcribes only; does not generate legal reasoning or advice.
- Preserves original spoken language and wording without silent translation.
- Never logs raw user complaint audio or transcript text (privacy by design).
- Automatically cleans up temporary audio files.
"""

from __future__ import annotations

import logging
import os
import tempfile
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import config
from app.schemas import ErrorDetail, HealthResponse, TranscribeResponse
from app.transcriber import SpeechTranscriber

# Logging setup (Privacy: operational metadata only, never audio/transcript data)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("speech_service.api")

# Global transcriber instance
transcriber = SpeechTranscriber(
    model_size=config.MODEL_SIZE,
    device=config.DEVICE,
    compute_type=config.COMPUTE_TYPE,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Composition root: load Whisper model once during startup."""
    logger.info("Starting up LegalLens Speech Service...")
    try:
        transcriber.load_model()
    except Exception as exc:
        logger.error(
            "Failed to load Whisper model on startup: %s. Service will start in degraded mode.",
            exc,
        )
    app.state.transcriber = transcriber
    yield
    logger.info("Shutting down LegalLens Speech Service...")


app = FastAPI(
    title="LegalLens Speech Service",
    description=(
        "Local speech-to-text service powered by faster-whisper. "
        "Supports English, Hindi, and Kannada for citizen legal complaints."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# CORS Middleware configured strictly for local frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health and model status",
)
async def health():
    """Returns operational status, model configuration, and memory state."""
    model_loaded = transcriber.is_loaded
    return HealthResponse(
        status="ok" if model_loaded else "degraded",
        service="speech-service",
        model_size=config.MODEL_SIZE,
        device=config.DEVICE,
        compute_type=config.COMPUTE_TYPE,
        model_loaded=model_loaded,
        supported_languages=["en", "hi", "kn"],
    )


@app.post(
    "/transcribe",
    response_model=TranscribeResponse,
    responses={
        400: {"model": ErrorDetail, "description": "Invalid, corrupted, or unsupported audio"},
        413: {"model": ErrorDetail, "description": "Upload exceeds size limit"},
        503: {"model": ErrorDetail, "description": "Speech model unavailable"},
    },
    summary="Transcribe uploaded audio file",
)
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file recorded by user"),
    language: Optional[str] = Form(
        None,
        description="Optional language code ('en', 'hi', 'kn') or None for auto-detection",
    ),
):
    """Transcribes an uploaded audio file and detects the spoken language.

    Preserves original language and wording. Does not translate.
    """
    if not transcriber.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Speech recognition model is not loaded or unavailable.",
        )

    filename = file.filename or "recording.webm"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "webm"
    content_type = (file.content_type or "").lower().split(";")[0].strip()

    # Validate audio file extension / mime type
    is_extension_allowed = ext in config.ALLOWED_EXTENSIONS
    is_mime_allowed = any(
        content_type == allowed.split(";")[0].strip() for allowed in config.ALLOWED_MIME_TYPES
    )

    if not is_extension_allowed and not is_mime_allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported audio format '{ext}'. "
                f"Supported formats: {', '.join(sorted(config.ALLOWED_EXTENSIONS))}."
            ),
        )

    # Read audio content with size limit enforcement
    temp_file_path = None
    total_bytes = 0

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp_audio:
            temp_file_path = temp_audio.name
            chunk_size = 64 * 1024  # 64 KB chunks
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > config.MAX_FILE_SIZE_BYTES:
                    max_mb = config.MAX_FILE_SIZE_BYTES // (1024 * 1024)
                    http_413 = getattr(status, "HTTP_413_CONTENT_TOO_LARGE", 413)
                    raise HTTPException(
                        status_code=http_413,
                        detail=f"Audio file exceeds maximum allowed size of {max_mb} MB.",
                    )
                temp_audio.write(chunk)

        if total_bytes == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty audio file received. Please record your complaint before submitting.",
            )

        # Transcribe audio file
        try:
            transcript, detected_lang, lang_prob, duration = transcriber.transcribe(
                audio_path=temp_file_path,
                language=language if language and language != "auto" else None,
            )
        except Exception as exc:
            # Check for audio decoding / corruption issues
            exc_str = str(exc).lower()
            if (
                "invalid data" in exc_str
                or "could not find audio" in exc_str
                or "header missing" in exc_str
                or "corrupt" in exc_str
                or "demuxer" in exc_str
            ):
                logger.warning("Failed to decode audio file (size=%d bytes): %s", total_bytes, exc)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or corrupted audio file. Unable to decode audio stream.",
                )
            logger.error("Transcription error: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Audio transcription failed. Please try speaking again.",
            )

        # Operational log (CLAUDE.md privacy rule: no scenario text, no user speech logged)
        logger.info(
            "Transcription completed: duration=%.2fs, lang=%s, prob=%.4f, size=%d bytes",
            duration,
            detected_lang,
            lang_prob,
            total_bytes,
        )

        return TranscribeResponse(
            transcript=transcript,
            language=detected_lang,
            language_probability=round(lang_prob, 4),
            duration=round(duration, 2),
        )

    finally:
        # Guarantee temporary audio file is deleted
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError as exc:
                logger.warning("Failed to delete temporary audio file %s: %s", temp_file_path, exc)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=False,
    )
