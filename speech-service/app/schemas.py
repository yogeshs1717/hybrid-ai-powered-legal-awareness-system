"""Pydantic schemas for the Speech Service API."""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Operational status of the speech service."""

    status: str = Field(..., description="Service status, e.g. 'ok'")
    service: str = Field("speech-service", description="Service identifier")
    model_size: str = Field(..., description="Whisper model size, e.g. 'small'")
    device: str = Field(..., description="Compute device, e.g. 'cpu'")
    compute_type: str = Field(..., description="Quantization compute type, e.g. 'int8'")
    model_loaded: bool = Field(..., description="Whether the Whisper model is loaded in memory")
    supported_languages: List[str] = Field(
        default=["en", "hi", "kn"],
        description="Key supported languages (English, Hindi, Kannada)",
    )


class TranscribeResponse(BaseModel):
    """Result of speech transcription."""

    transcript: str = Field(..., description="Transcribed text in original spoken language")
    language: str = Field(..., description="Detected language code, e.g. 'en', 'hi', 'kn'")
    language_probability: float = Field(
        ...,
        description="Confidence score for the detected language (0.0 to 1.0)",
    )
    duration: Optional[float] = Field(
        None,
        description="Duration of the audio recording in seconds",
    )


class ErrorDetail(BaseModel):
    """Standardized error response."""

    detail: str = Field(..., description="Descriptive error explanation")
