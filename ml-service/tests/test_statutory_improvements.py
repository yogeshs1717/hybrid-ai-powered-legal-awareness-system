"""Unit and regression tests for statutory accuracy improvements.

Tests:
1. Multi-provision compound retrieval for cyber fraud (IT Act 66C, 66D, BNS 318).
2. B2B Commercial exclusion under Consumer Protection Act 2019 Section 2(7).
3. Statutory defense under Motor Vehicles Act Section 119(2) (lawful police diversion).
4. Historical law transition detection for pre-July 1, 2024 incidents (IPC/CrPC note).
5. Non-commencement of Code on Wages 2019 (operative Payment of Wages / Minimum Wages Acts).
6. Cheque bounce compound provisions (NI Act Section 138 & Section 142).
7. MSME delayed payments statutory interest (MSMED Act Sections 15, 16, 18).
8. Contractual restraint of trade (Indian Contract Act Section 27).
9. Enriched statutory schema fields (relevance_classification, applicable_legal_elements, etc.).
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
    with TestClient(app) as c:
        yield c


def test_compound_provision_retrieval_cyber_fraud(client):
    """UPI/OTP fraud must retrieve compound provisions across IT Act and BNS."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "A caller posing as my bank manager asked for my OTP to update KYC, and Rs 50,000 was debited via UPI immediately."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["analysis"]["domain"]["id"] == "cyber_fraud"
    
    sections = [p["section"].lower() for p in data["legal_provisions"]]
    acts = [p["act"].lower() for p in data["legal_provisions"]]
    
    # Must retrieve both IT Act and BNS 318
    assert any("66d" in s or "66c" in s for s in sections)
    assert any("318" in s for s in sections)
    assert any("information technology" in a for a in acts)
    assert any("bharatiya nyaya" in a for a in acts)


def test_b2b_commercial_exclusion_routes_to_contractual(client):
    """B2B commercial wholesale purchases are excluded from CPA Section 2(7) and must route to contractual disputes."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "Our textile trading company purchased 500 bolts of fabric from a wholesale vendor for commercial resale, but the supplier delivered damaged stock and refused to refund the commercial invoice."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["analysis"]["domain"]["id"] == "contractual_disputes"


def test_police_diversion_statutory_defense(client):
    """Diversion by traffic police officer in uniform provides statutory defense under MV Act Section 119(2)."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "Traffic police officer in uniform directed all vehicles into a one-way street due to an accident ahead. Later I received an e-challan for Section 184 dangerous driving for entering that street."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["analysis"]["domain"]["id"] == "traffic_enforcement"
    # Section 184 should be filtered out or excluded due to statutory defense under Section 119(2)
    sections = [p["section"] for p in data["legal_provisions"]]
    assert not any("184" in s for s in sections)


def test_historical_law_transition_pre_july_2024(client):
    """Scenarios with dates prior to July 1, 2024 must include a historical law note referencing IPC 1860."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "In March 2024, a company defrauded me of Rs 2 lakhs through a fraudulent online investment scheme."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["historical_law_note"] is not None
    assert "July 1, 2024" in data["historical_law_note"]
    assert "Indian Penal Code, 1860" in data["historical_law_note"]


def test_wage_law_prioritizes_operative_acts(client):
    """Unpaid wages must retrieve the operative Payment of Wages Act, 1936 or Minimum Wages Act, 1948."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "My employer has delayed paying my monthly salary for the past three months without any explanation."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["analysis"]["domain"]["id"] == "workplace_wage"
    acts = [p["act"] for p in data["legal_provisions"]]
    assert any("Payment of Wages Act, 1936" in a for a in acts)


def test_cheque_bounce_retrieves_ni_act(client):
    """Dishonour of cheque must retrieve Negotiable Instruments Act Section 138."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "A business client issued a cheque of Rs 3 lakhs for goods delivered, but the cheque was dishonoured by the bank with the memo funds insufficient."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["analysis"]["domain"]["id"] == "contractual_disputes"
    sections = [p["section"] for p in data["legal_provisions"]]
    assert any("138" in s for s in sections)


def test_msme_delayed_payment_retrieval(client):
    """MSME delayed payment claims must retrieve MSMED Act 2006 provisions."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "Our registered MSME manufacturing unit supplied auto components to a large buyer on invoice 70 days ago, but the payment is delayed and not released."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["analysis"]["domain"]["id"] == "contractual_disputes"
    acts = [p["act"] for p in data["legal_provisions"]]
    assert any("Micro, Small and Medium Enterprises Development Act, 2006" in a for a in acts)


def test_restraint_of_trade_non_compete(client):
    """Non-compete clause in employment agreement must retrieve Contract Act Section 27."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "My employment agreement has a non-compete clause prohibiting me from working in the entire IT sector for two years after resigning."
        },
    )
    assert r.status_code == 200
    data = r.json()
    sections = [p["section"] for p in data["legal_provisions"]]
    assert any("27" in s for s in sections)


def test_enriched_statutory_element_fields(client):
    """Responses must contain enriched statutory elements and relevance classifications."""
    r = client.post(
        "/analyze",
        json={
            "scenario": "I bought a refrigerator from an online platform which was delivered with a broken compressor, and the company refuses refund or replacement."
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data["legal_provisions"]) > 0
    prov = data["legal_provisions"][0]
    
    # Check enriched statutory fields
    assert "relevance_classification" in prov
    assert prov["relevance_classification"] in (
        "DIRECTLY_APPLICABLE",
        "CONDITIONALLY_APPLICABLE",
        "PROCEDURAL_PROVISION",
        "SUPPORTING_PROVISION",
        "NOT_APPLICABLE",
    )
    assert "applicable_legal_elements" in prov
    assert isinstance(prov["applicable_legal_elements"], list)
    assert "applicability_conditions" in prov
    assert isinstance(prov["applicability_conditions"], list)
