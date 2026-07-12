"""FastAPI entry point for the ML service (port 8000).

What this is: the composition root. At startup it loads and validates the
knowledge base, constructs the four modules, injects them into the pipeline,
and exposes exactly two routes:

    POST /analyze  — full four-module analysis of a scenario
    GET  /health   — operational status (which classifier mode is live,
                     KB counts) with zero legal content

HTTP semantics (CLAUDE.md 8.2, permanent):
- Model uncertainty on VALID input is HTTP 200 with warning flags — by
  construction, because the ResponseBuilder always yields a normal response.
- HTTP 400 is reserved for actual input validation failures (empty/too
  short/too long/malformed). FastAPI's default would be 422; a handler
  converts request-validation failures to 400 to match the contract.
  (The Node.js gateway will additionally validate upstream in Phase 1D.)

Honesty with no data: with a skeleton KB and no trained model the service
still runs — the mock classifier reports LOW confidence, Module 2 detects
nothing, Module 3 returns the explicit safe state, and /health openly says
classifier_mode="mock". Nothing pretends to be a real legal result.

Run from the ml-service directory:  uvicorn app.main:app --port 8000
Environment overrides: KB_DIR (default: <repo>/knowledge_base),
MODELS_DIR (default: <ml-service>/models).
"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.classifier import create_domain_classifier
from app.issue_detector import IssueDetector
from app.knowledge_base_loader import load_knowledge_base
from app.legal_intelligence import LegalIntelligenceEngine
from app.pipeline import AnalysisPipeline
from app.response_builder import ResponseBuilder
from app.schemas import AnalyzeRequest, AnalyzeResponse, HealthResponse

_ML_SERVICE_ROOT = Path(__file__).resolve().parents[1]
_REPO_ROOT = _ML_SERVICE_ROOT.parent

KB_DIR = Path(os.environ.get("KB_DIR", _REPO_ROOT / "knowledge_base"))
MODELS_DIR = Path(os.environ.get("MODELS_DIR", _ML_SERVICE_ROOT / "models"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Composition root: everything is built once, here, and injected.
    A KB that fails validation aborts startup — loud failure over silently
    serving corrupted legal data."""
    kb = load_knowledge_base(KB_DIR)
    classifier = create_domain_classifier(MODELS_DIR)
    issue_detector = IssueDetector(kb)

    app.state.kb = kb
    app.state.classifier_mode = classifier.mode
    app.state.issue_detector_mode = issue_detector.mode
    app.state.pipeline = AnalysisPipeline(
        classifier=classifier,
        issue_detector=issue_detector,
        legal_engine=LegalIntelligenceEngine(kb),
        response_builder=ResponseBuilder(),
    )
    yield


app = FastAPI(
    title="Smart Legal Intelligence System — ML Service",
    description=(
        "Legal awareness analysis: domain classification, issue detection "
        "using prototype similarity matching, and retrieval of manually "
        "verified legal provisions. Provides legal awareness, not legal advice."
    ),
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def validation_to_400(request: Request, exc: RequestValidationError):
    """Input validation failures are client errors: HTTP 400 (CLAUDE.md 8.2).
    Distinct from low model confidence, which is always HTTP 200."""
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": "invalid_input", "detail": exc.errors()},
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request_body: AnalyzeRequest, request: Request) -> AnalyzeResponse:
    request_id = request_body.request_id or str(uuid.uuid4())
    return request.app.state.pipeline.analyze(request_body.scenario, request_id)


@app.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    counts = request.app.state.kb.counts()
    return HealthResponse(
        status="ok",
        classifier_mode=request.app.state.classifier_mode,
        issue_detector_mode=request.app.state.issue_detector_mode,
        kb_acts=counts["acts"],
        kb_sections=counts["sections"],
        kb_issues=counts["issues"],
        kb_portals=counts["portals"],
    )
