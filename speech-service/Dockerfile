# ==============================================================================
# LegalLens Speech Service (FastAPI + Faster-Whisper)
# ==============================================================================
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PORT=8001
ENV SPEECH_SERVICE_HOST=0.0.0.0
ENV SPEECH_SERVICE_PORT=8001
ENV WHISPER_MODEL_SIZE=tiny
ENV WHISPER_DEVICE=cpu
ENV WHISPER_COMPUTE_TYPE=int8

EXPOSE 8001

CMD ["sh", "-c", "python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8001}"]
