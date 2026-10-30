# How to Run the Project

This project consists of four services that run concurrently:
1. **ML Service** (Python / FastAPI) on port `8000`
2. **Speech Service** (Python / faster-whisper FastAPI) on port `8001`
3. **API Gateway** (Node.js / Express) on port `5000`
4. **Frontend** (React / Vite) on port `3000`

---

## 1. One-Time Setup

Open your terminal in the project root:

### Step A: Setup ML Service (Python)
```bash
cd ml-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

### Step B: Setup Speech Service (Python / faster-whisper)
```bash
# Uses the pre-created virtual environment in speech-service/.venv
source speech-service/.venv/bin/activate
pip install -r speech-service/requirements.txt
```

### Step C: Setup API Gateway (Node.js)
```bash
cd backend
npm install
cd ..
```

### Step D: Setup Frontend (React)
```bash
cd frontend
npm install
cd ..
```

---

## 2. Start Commands

### Recommended: Start Both AI Services with One Command
From the project root, run:
```bash
npm run dev
# or
npm start
# or
./start-services.sh
```
This concurrently starts **both** `ml-service` (port 8000) and `speech-service` (port 8001) with live hot-reloading and colored prefixed logs. Press `Ctrl+C` to cleanly stop both.

*(Optional: Run `npm run dev:all` to launch all 4 services concurrently — ML service, speech service, API gateway, and frontend).*

---

### Alternative: Manual Start (Separate Terminals)
Open separate terminal tabs from the project root and run:

### Terminal 1: ML Service
```bash
cd ml-service
source venv/bin/activate
uvicorn app.main:app --port 8000 --reload --reload-dir app --reload-dir ../knowledge_base
```
*Health check URL:* `http://localhost:8000/health`

### Terminal 2: Speech Service (Voice Input)
```bash
speech-service/.venv/bin/uvicorn app.main:app --app-dir speech-service --host 127.0.0.1 --port 8001 --reload
```
*Health check URL:* `http://localhost:8001/health`

### Terminal 3: API Gateway
```bash
cd backend
npm run dev
```
*Health check URL:* `http://localhost:5000/api/health`

### Terminal 4: Frontend
```bash
cd frontend
npm run dev
```
*App URL:* **`http://localhost:3000`**

---

## 3. Quick Verification

Open your browser and navigate to:
👉 **[http://localhost:3000](http://localhost:3000)**

1. **Typed input:** Type a scenario (e.g., *"Someone called pretending to be bank staff and asked for OTP, then money was deducted"*) and click **Run Legal Analysis**.
2. **Voice input:** Click the **Voice Input (Record)** button, speak in English, Hindi, or Kannada, click **Done Recording**, review the transcribed text and detected language, and click **Run Legal Analysis**.

---

## Optional: Run Tests

- **Speech Service Tests:**
  ```bash
  speech-service/.venv/bin/python -m unittest speech-service/tests/test_api.py
  speech-service/.venv/bin/python -m unittest speech-service/tests/test_live.py
  ```
- **ML Service Tests:**
  ```bash
  cd ml-service && pytest
  ```
- **Backend Tests (including Voice Workflow Integration):**
  ```bash
  cd backend && npm test
  ```
- **Frontend Type Check & Build:**
  ```bash
  cd frontend && npm run build
  ```

