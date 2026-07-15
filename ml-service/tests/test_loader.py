"""Unit tests for knowledge_base_loader.

Every KB record in this file is a TEST FIXTURE — NOT LEGAL DATA. Fixture act/
section/issue/portal IDs are deliberately fake (test_act_0000 etc.) so they
can never be mistaken for real provisions. Fixtures may set any status value,
including 'manually_verified': that is exercising the validator with mock
data, not verifying a legal provision (permitted per PROJECT_STATE.md
Section 8 — structural tests with clearly marked fixtures are not gated on
real verified provisions).

Run from the ml-service directory:  python -m pytest tests/test_loader.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.knowledge_base_loader import (  # noqa: E402
    KBValidationError,
    load_knowledge_base,
)

REPO_KB_DIR = Path(__file__).resolve().parents[2] / "knowledge_base"


# ---------------------------------------------------------------------------
# Fixture helpers — TEST DATA ONLY, NOT LEGAL DATA
# ---------------------------------------------------------------------------

def make_acts(sections: dict | None = None) -> dict:
    return {
        "acts": {
            "test_act_0000": {
                "official_act_name": "Test Act 0000 (TEST FIXTURE - NOT LEGAL DATA)",
                "act_year": 2000,
                "short_name": "Test Act",
                "official_source_name": "Test Source",
                "official_source_url": None,
                "sections": sections
                if sections is not None
                else {
                    "s1": {
                        "section_number": "1",
                        "official_section_title": "Test Section (FIXTURE)",
                        "official_text": None,
                        "simplified_explanation": "Fixture explanation.",
                        "applicability_notes": None,
                        "keywords": ["fixture"],
                        "citation": None,
                        "provision_status": "unverified",
                        "verification": {
                            "status": "pending_manual_verification",
                            "verified_by": None,
                            "verified_on": None,
                        },
                    }
                },
            }
        }
    }


def make_mappings(issue_overrides: dict | None = None) -> dict:
    issue = {
        "issue_id": "test_issue",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "cyber_fraud",
        "display_name": "Test Issue (FIXTURE)",
        "issue_definition": "A fixture scenario type.",
        "prototype_texts": ["fixture prototype text one", "fixture prototype text two"],
        "provision_references": [
            {
                "act_id": "test_act_0000",
                "section_id": "s1",
                "provision_relevance_rationale": "Fixture rationale (Layer B).",
            }
        ],
    }
    issue.update(issue_overrides or {})
    return {"issues": {"test_issue": issue}}


def make_guidance(portal_overrides: dict | None = None,
                  guidance_overrides: dict | None = None) -> dict:
    portal = {
        "portal_id": "test_portal",
        "name": "Test Portal (FIXTURE)",
        "official_url": None,
        "purpose": "Fixture purpose.",
        "priority": "primary",
        "usage_condition": None,
        "official_source": "Test Authority",
        "supported_issue_ids": ["test_issue"],
    }
    portal.update(portal_overrides or {})
    guidance = {"action_steps": ["Fixture step 1.", "Fixture step 2."],
                "portal_ids": ["test_portal"]}
    guidance.update(guidance_overrides or {})
    return {"issue_guidance": {"test_issue": guidance}, "portals": {"test_portal": portal}}


def write_kb(tmp_path: Path, acts: dict, mappings: dict, guidance: dict) -> Path:
    (tmp_path / "acts_and_sections.json").write_text(json.dumps(acts), encoding="utf-8")
    (tmp_path / "issue_mappings.json").write_text(json.dumps(mappings), encoding="utf-8")
    (tmp_path / "issue_actions_portals.json").write_text(
        json.dumps(guidance), encoding="utf-8"
    )
    return tmp_path


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_real_repo_kb_loads_and_validates():
    """The actual repository KB must always pass full structural validation.
    (Originally asserted emptiness; the KB is now being populated issue by
    issue, so the invariant is validity + index consistency, not emptiness.)"""
    kb = load_knowledge_base(REPO_KB_DIR)
    counts = kb.counts()
    # Every issue is indexed under exactly one approved domain.
    assert sum(len(v) for v in kb.issues_by_domain.values()) == counts["issues"]
    # Guidance entries can never exceed issues (validated 1:1 by issue_id).
    assert counts["guidance_entries"] <= counts["issues"]


def test_minimal_fixture_loads_and_builds_indexes(tmp_path):
    kb_dir = write_kb(tmp_path, make_acts(), make_mappings(), make_guidance())
    kb = load_knowledge_base(kb_dir)
    assert kb.counts() == {
        "acts": 1, "sections": 1, "issues": 1, "guidance_entries": 1, "portals": 1
    }
    # Runtime indexes:
    assert kb.issues_by_domain == {"cyber_fraud": ["test_issue"]}
    assert kb.portals_by_issue == {"test_issue": ["test_portal"]}
    # Provision resolution:
    assert kb.resolve_provision("test_act_0000", "s1") is not None
    assert kb.resolve_provision("test_act_0000", "missing") is None
    assert kb.resolve_provision("missing_act", "s1") is None


def test_duplicate_json_key_rejected(tmp_path):
    """A duplicated ID inside a JSON object is corruption, not a tie-break."""
    write_kb(tmp_path, make_acts(), make_mappings(), make_guidance())
    raw = (
        '{"acts": {"dup_act": {"sections": {}}, "dup_act": {"sections": {}}}}'
    )
    (tmp_path / "acts_and_sections.json").write_text(raw, encoding="utf-8")
    with pytest.raises(KBValidationError, match="duplicate key"):
        load_knowledge_base(tmp_path)


def test_embedded_issue_id_must_match_key(tmp_path):
    kb_dir = write_kb(
        tmp_path, make_acts(), make_mappings({"issue_id": "wrong_id"}), make_guidance()
    )
    with pytest.raises(KBValidationError, match="does not equal its object key"):
        load_knowledge_base(kb_dir)


def test_embedded_portal_id_must_match_key(tmp_path):
    kb_dir = write_kb(
        tmp_path, make_acts(), make_mappings(),
        make_guidance(portal_overrides={"portal_id": "wrong_portal"}),
    )
    with pytest.raises(KBValidationError, match="does not equal its object key"):
        load_knowledge_base(kb_dir)


def test_unresolved_provision_reference_rejected(tmp_path):
    kb_dir = write_kb(
        tmp_path,
        make_acts(),
        make_mappings(
            {
                "provision_references": [
                    {
                        "act_id": "ghost_act",
                        "section_id": "s1",
                        "provision_relevance_rationale": "Fixture.",
                    }
                ]
            }
        ),
        make_guidance(),
    )
    with pytest.raises(KBValidationError, match="does not resolve"):
        load_knowledge_base(kb_dir)


def test_unknown_domain_rejected(tmp_path):
    kb_dir = write_kb(
        tmp_path, make_acts(), make_mappings({"domain_id": "criminal_law"}),
        make_guidance(),
    )
    with pytest.raises(KBValidationError, match="not an approved domain"):
        load_knowledge_base(kb_dir)


def test_invalid_taxonomy_status_rejected(tmp_path):
    kb_dir = write_kb(
        tmp_path, make_acts(), make_mappings({"taxonomy_status": "approved"}),
        make_guidance(),
    )
    # 'approved' was renamed to 'taxonomy_supported'; the old value must fail.
    with pytest.raises(KBValidationError, match="taxonomy_status"):
        load_knowledge_base(kb_dir)


def test_unresolved_portal_id_in_guidance_rejected(tmp_path):
    kb_dir = write_kb(
        tmp_path, make_acts(), make_mappings(),
        make_guidance(guidance_overrides={"portal_ids": ["ghost_portal"]}),
    )
    with pytest.raises(KBValidationError, match="ghost_portal"):
        load_knowledge_base(kb_dir)


def test_action_steps_over_limit_rejected(tmp_path):
    kb_dir = write_kb(
        tmp_path, make_acts(), make_mappings(),
        make_guidance(guidance_overrides={"action_steps": [f"Step {i}" for i in range(6)]}),
    )
    with pytest.raises(KBValidationError, match="exceeds the maximum"):
        load_knowledge_base(kb_dir)


def test_invalid_verification_status_rejected(tmp_path):
    sections = {
        "s1": {
            "section_number": "1",
            "provision_status": "unverified",
            "verification": {"status": "ai_verified", "verified_by": None,
                             "verified_on": None},
        }
    }
    kb_dir = write_kb(
        tmp_path, make_acts(sections),
        make_mappings({"provision_references": []}), make_guidance(),
    )
    with pytest.raises(KBValidationError, match="verification.status"):
        load_knowledge_base(kb_dir)


def test_all_errors_collected_not_just_first(tmp_path):
    """The loader reports every finding, not only the first one."""
    kb_dir = write_kb(
        tmp_path,
        make_acts(),
        make_mappings({"issue_id": "wrong_id", "domain_id": "criminal_law"}),
        make_guidance(),
    )
    with pytest.raises(KBValidationError) as excinfo:
        load_knowledge_base(kb_dir)
    assert len(excinfo.value.errors) >= 2
