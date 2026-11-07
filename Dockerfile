# ==============================================================================
# LegalLens Unified Backend Service (API Gateway + ML Service)
# ==============================================================================
FROM python:3.11-slim

# Install Node.js 20, curl, and certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1. Install ML Service dependencies
COPY ml-service/requirements.txt ./ml-service/
RUN pip install --no-cache-dir -r ./ml-service/requirements.txt

# 2. Install Node Gateway dependencies
COPY backend/package*.json ./backend/
RUN cd backend && npm ci --omit=dev

# 3. Copy application code & knowledge base
COPY knowledge_base ./knowledge_base
COPY ml-service ./ml-service
COPY backend ./backend

# Environment configuration
ENV PORT=5000
ENV ML_SERVICE_URL=http://127.0.0.1:8000
ENV KB_DIR=/app/knowledge_base
ENV MODELS_DIR=/app/ml-service/models
ENV NODE_ENV=production

# Startup script: launches ML service internally, then hands off to Node Gateway
RUN echo '#!/bin/sh\n\
set -e\n\
echo "Starting LegalLens ML Service on port 8000..."\n\
python3 -m uvicorn app.main:app --app-dir ml-service --host 127.0.0.1 --port 8000 &\n\
\n\
echo "Waiting for ML Service to become healthy..."\n\
for i in $(seq 1 30); do\n\
  if curl -sf http://127.0.0.1:8000/health > /dev/null 2>&1; then\n\
    echo "ML Service is healthy and ready!"\n\
    break\n\
  fi\n\
  sleep 1\n\
done\n\
\n\
echo "Starting Express API Gateway on port ${PORT}..."\n\
cd /app/backend\n\
exec node src/server.js\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 5000

CMD ["/app/start.sh"]
