# How to Run the Project

This project consists of three services that run concurrently:
1. **ML Service** (Python / FastAPI) on port `8000`
2. **API Gateway** (Node.js / Express) on port `5000`
3. **Frontend** (React / Vite) on port `3000`

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

### Step B: Setup API Gateway (Node.js)
```bash
cd backend
npm install
cd ..
```

### Step C: Setup Frontend (React)
```bash
cd frontend
npm install
cd ..
```

---

## 2. Start Commands

Open **3 separate terminal tabs** from the project root and run:

### Terminal 1: ML Service
```bash
cd ml-service
source venv/bin/activate
uvicorn app.main:app --port 8000 --reload --reload-dir app --reload-dir ../knowledge_base
```
*Health check URL:* `http://localhost:8000/health`

### Terminal 2: API Gateway
```bash
cd backend
npm run dev
```
*Health check URL:* `http://localhost:5000/api/health`

### Terminal 3: Frontend
```bash
cd frontend
npm run dev
```
*App URL:* **`http://localhost:3000`**

---

## 3. Quick Verification

Open your browser and navigate to:
👉 **[http://localhost:3000](http://localhost:3000)**

Type a scenario (e.g., *"Someone called pretending to be bank staff and asked for OTP, then money was deducted"*) and click **Analyze**.

---

## Optional: Run Tests

- **ML Service Tests:**
  ```bash
  cd ml-service && pytest
  ```
- **Backend Tests:**
  ```bash
  cd backend && npm test
  ```
- **Frontend Type Check & Build:**
  ```bash
  cd frontend && npm run build
  ```
