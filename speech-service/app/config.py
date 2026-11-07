"""Configuration for the LegalLens Speech Service.

Centralizes runtime options, model parameters, upload constraints,
and security settings (CORS, loopback binding).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Set

# Base directory of the speech-service
BASE_DIR = Path(__file__).resolve().parents[1]

# Service network binding (Security: default to 127.0.0.1 loopback)
HOST = os.environ.get("SPEECH_SERVICE_HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT") or os.environ.get("SPEECH_SERVICE_PORT") or "8001")

# Faster-Whisper Model Settings
MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "small")
DEVICE = os.environ.get("WHISPER_DEVICE", "cpu")
COMPUTE_TYPE = os.environ.get("WHISPER_COMPUTE_TYPE", "int8")

# Upload and Security Constraints
# Max upload size: 25 MB (sufficient for up to ~10-15 minutes of compressed speech)
MAX_FILE_SIZE_BYTES = int(os.environ.get("MAX_FILE_SIZE_BYTES", str(25 * 1024 * 1024)))

# Supported audio extensions for upload validation
ALLOWED_EXTENSIONS: Set[str] = {
    "webm",
    "ogg",
    "wav",
    "mp3",
    "m4a",
    "mp4",
    "flac",
    "aac",
    "opus",
    "wma",
}

# Supported audio MIME types
ALLOWED_MIME_TYPES: Set[str] = {
    "audio/webm",
    "audio/webm;codecs=opus",
    "audio/x-webm",
    "video/webm",
    "audio/ogg",
    "audio/ogg;codecs=opus",
    "audio/wav",
    "audio/wave",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp3",
    "audio/mp4",
    "audio/m4a",
    "audio/x-m4a",
    "audio/flac",
    "audio/x-flac",
    "audio/aac",
    "audio/opus",
    "application/octet-stream",  # Often sent by browsers when recording blobs
}

# CORS origins: restrict to local development frontend and backend gateway
_DEFAULT_CORS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
]

cors_env = os.environ.get("SPEECH_CORS_ORIGINS")
if cors_env:
    CORS_ORIGINS: List[str] = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
else:
    CORS_ORIGINS: List[str] = _DEFAULT_CORS
