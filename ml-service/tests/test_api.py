"""End-to-end API tests for the FastAPI ML service (Modules 1-4 wired).

Exercises the live app via FastAPI's TestClient against the real trained model
(if present) and the populated KB. Skipped automatically if fastapi/httpx are
not installed, so tests/test_loader.py still runs standalone (stdlib-only).

Run from the ml-service directory:  python -m pytest tests/test_api.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import app  # noqa: E402


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # lifespan loads KB + classifier
        yield c


def test_health_reports_kb_and_modes(client):
    h = client.get("/health").json()
    assert h["status"] == "ok"
    assert h["classifier_mode"] in ("trained", "mock")
    assert h["issue_detector_mode"] in ("active", "no_prototypes")
    assert h["kb_acts"] >= 1 and h["kb_issues"] >= 1


def test_analyze_returns_contract_shape_and_disclaimer(client):
    r = client.post(
        "/analyze",
        json={
            "scenario": "Someone called pretending to be my bank and asked for the "
            "OTP that came on my phone, then money was debited from my account."
        },
    )
    assert r.status_code == 200
    body = r.json()
    # Locked response-contract fields (CLAUDE.md 8.1)
    for key in (
        "success", "request_id", "analysis", "legal_provisions",
        "legal_information_status", "action_steps", "portals", "disclaimer",
    ):
        assert key in body
    assert body["analysis"]["issue"].get("confidence") is None  # never 'confidence'
    assert "similarity_score" in body["analysis"]["issue"]
    assert body["disclaimer"]  # mandatory, every response


def test_analyze_serves_only_verified_provisions(client):
    """A strong OTP scenario should retrieve manually_verified + in_force
    provisions (IT Act 66C/66D). If the KB were unpopulated/unverified this
    would instead be the explicit safe state."""
    body = client.post(
        "/analyze",
        json={
            "scenario": "A fraudster posing as my bank's KYC team made me share the "
            "OTP and an unauthorised transaction happened immediately after."
        },
    ).json()
    if body["legal_provisions"]:
        assert body["legal_information_status"] == "provisions_available"
        assert all(p["provision_relevance_rationale"] for p in body["legal_provisions"])
    else:
        assert body["legal_information_status"] == "no_verified_provision_available"


def test_short_input_is_http_400(client):
    r = client.post("/analyze", json={"scenario": "help"})
    assert r.status_code == 400  # input validation, not model uncertainty


def test_low_confidence_is_http_200_not_error(client):
    """Model uncertainty on a valid-length but vague scenario must stay 200
    with warning flags, never an HTTP error (CLAUDE.md 8.2)."""
    r = client.post(
        "/analyze",
        json={"scenario": "something happened and i am not sure what to do about it"},
    )
    assert r.status_code == 200
    assert "low_confidence_warning" in r.json()


def test_unknown_scenario_returns_fallback_not_random_domain(client):
    """An unknown sentence or non-legal chatter must return a clear fallback message
    with is_valid_scenario=False, domain='unknown', and zero legal provisions."""
    r = client.post(
        "/analyze",
        json={"scenario": "The quick brown fox jumps over the lazy dog in the garden."},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["is_valid_scenario"] is False
    assert data["legal_information_status"] == "unknown_scenario"
    assert data["analysis"]["domain"]["id"] == "unknown"
    assert len(data["legal_provisions"]) == 0
    assert data["fallback_message"] is not None
    assert "legal scenario" in data["fallback_message"].lower()


def test_valid_legal_scenario_does_not_trigger_fallback(client):
    """A valid legal scenario must be recognized as valid and NOT trigger fallback."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "Someone called pretending to be bank manager and asked for OTP, then 40000 was debited from my account"
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["is_valid_scenario"] is True
    assert data["fallback_message"] is None
    assert data["analysis"]["domain"]["id"] == "cyber_fraud"
    assert data["legal_information_status"] == "provisions_available"
    assert len(data["legal_provisions"]) > 0

