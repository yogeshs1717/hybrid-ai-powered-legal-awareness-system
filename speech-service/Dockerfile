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

COPY speech-service/requirements.txt ./speech-service/
RUN pip install --no-cache-dir -r ./speech-service/requirements.txt

COPY speech-service ./speech-service

ENV SPEECH_SERVICE_HOST=0.0.0.0
ENV SPEECH_SERVICE_PORT=8001
ENV WHISPER_MODEL_SIZE=small
ENV WHISPER_DEVICE=cpu
ENV WHISPER_COMPUTE_TYPE=int8

EXPOSE 8001

CMD ["python3", "-m", "uvicorn", "app.main:app", "--app-dir", "speech-service", "--host", "0.0.0.0", "--port", "8001"]
