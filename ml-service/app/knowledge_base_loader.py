"""Knowledge Base loader and validator.

What this is: the only component that reads the three KB JSON files
(CLAUDE.md Section 7.2). It runs once at service startup, validates the files
against the schema contracts embedded in their ``_schema`` blocks, builds the
runtime indexes the modules need, and hands back an immutable-by-convention
:class:`KnowledgeBase` object. At runtime the KB is read-only.

Why it exists: Modules 2 and 3 must be able to trust the KB blindly. Every
structural guarantee (IDs match keys, references resolve, enums are legal)
is enforced HERE, once, at startup — so a corrupted KB fails the service
loudly instead of silently returning wrong legal information to a citizen.

What breaks without it: a dangling ``act_id`` reference would surface as a
KeyError mid-request, or worse, as a silently missing provision.

Validation performed:
  1. JSON well-formedness, including duplicate-key detection (a duplicated
     act/issue/portal ID would otherwise be silently swallowed by json.load).
  2. Schema shape: required containers and fields, enum membership.
  3. ID discipline: embedded ``issue_id``/``portal_id`` must equal the object key.
  4. Reference integrity: every (act_id, section_id) in issue_mappings resolves;
     every portal_id in issue_guidance resolves; every supported_issue_id and
     guidance key resolves to a known issue.
  5. Runtime indexes: issues_by_domain, portals_by_issue.

Deliberately stdlib-only so KB integrity can be checked (and unit-tested)
without installing the ML stack.

Self-check: ``python knowledge_base_loader.py [kb_dir]`` validates a KB
directory and prints a summary.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Controlled vocabularies (mirrors of the frozen KB schemas / CLAUDE.md)
# ---------------------------------------------------------------------------

# CANONICAL definition of the five approved Phase 1 domains (CLAUDE.md 3.1).
# Other modules import this rather than redefining it — this module is
# stdlib-only, so importing it never drags in heavy dependencies.
APPROVED_DOMAINS = frozenset(
    {
        "cyber_fraud",
        "consumer_issues",
        "traffic_enforcement",
        "workplace_wage",
        "contractual_disputes",
    }
)

TAXONOMY_STATUSES = frozenset(
    {"working", "provision_research_required", "taxonomy_supported", "rejected", "merged"}
)

PROVISION_STATUSES = frozenset(
    {
        "unverified",
        "in_force",
        "omitted",
        "repealed",
        "amended_review_required",
        "applicability_uncertain",
    }
)

VERIFICATION_STATUSES = frozenset({"pending_manual_verification", "manually_verified"})

PORTAL_PRIORITIES = frozenset({"immediate", "primary", "secondary"})

MAX_ACTION_STEPS = 5  # CLAUDE.md Section 8

KB_FILENAMES = (
    "acts_and_sections.json",
    "issue_mappings.json",
    "issue_actions_portals.json",
)

# Documentation-only keys inside the KB files; never treated as data.
_DOC_KEYS = {"_meta", "_schema"}


class KBValidationError(Exception):
    """Raised when the KB fails structural validation. Carries every finding."""

    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(
            "Knowledge base validation failed with "
            f"{len(errors)} error(s):\n- " + "\n- ".join(errors)
        )


@dataclass
class KnowledgeBase:
    """Validated, indexed, read-only-at-runtime view of the three KB files."""

    acts: Dict[str, Any]
    issues: Dict[str, Any]
    issue_guidance: Dict[str, Any]
    portals: Dict[str, Any]
    # Runtime indexes (built by the loader, never persisted):
    issues_by_domain: Dict[str, List[str]] = field(default_factory=dict)
    portals_by_issue: Dict[str, List[str]] = field(default_factory=dict)

    def resolve_provision(self, act_id: str, section_id: str) -> Optional[Dict[str, Any]]:
        """Return the section record for (act_id, section_id), or None."""
        act = self.acts.get(act_id)
        if not act:
            return None
        return act.get("sections", {}).get(section_id)

    def counts(self) -> Dict[str, int]:
        return {
            "acts": len(self.acts),
            "sections": sum(len(a.get("sections", {})) for a in self.acts.values()),
            "issues": len(self.issues),
            "guidance_entries": len(self.issue_guidance),
            "portals": len(self.portals),
        }


# ---------------------------------------------------------------------------
# JSON parsing with duplicate-key detection
# ---------------------------------------------------------------------------

def _duplicate_guard_hook(pairs: List[tuple]) -> Dict[str, Any]:
    """object_pairs_hook that rejects duplicate keys instead of silently
    keeping the last one — a duplicated act/issue/portal ID is data corruption,
    not a tie to be broken arbitrarily."""
    seen: Dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate key '{key}' in JSON object")
        seen[key] = value
    return seen


def _load_json(path: Path, errors: List[str]) -> Optional[Dict[str, Any]]:
    if not path.is_file():
        errors.append(f"{path.name}: file not found at {path}")
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh, object_pairs_hook=_duplicate_guard_hook)
    except ValueError as exc:  # includes JSONDecodeError and duplicate keys
        errors.append(f"{path.name}: invalid JSON — {exc}")
        return None


# ---------------------------------------------------------------------------
# Per-file validators (collect errors; never raise mid-walk)
# ---------------------------------------------------------------------------

def _validate_acts(acts: Dict[str, Any], errors: List[str]) -> None:
    for act_id, act in acts.items():
        where = f"acts_and_sections.json: act '{act_id}'"
        if not isinstance(act, dict):
            errors.append(f"{where}: record must be an object")
            continue
        sections = act.get("sections")
        if not isinstance(sections, dict):
            errors.append(f"{where}: missing/invalid 'sections' object")
            continue
        for section_id, section in sections.items():
            swhere = f"{where}, section '{section_id}'"
            if not isinstance(section, dict):
                errors.append(f"{swhere}: record must be an object")
                continue
            status = section.get("provision_status")
            if status not in PROVISION_STATUSES:
                errors.append(
                    f"{swhere}: provision_status '{status}' not in controlled enum"
                )
            verification = section.get("verification")
            if not isinstance(verification, dict):
                errors.append(f"{swhere}: missing 'verification' block")
            else:
                vstatus = verification.get("status")
                if vstatus not in VERIFICATION_STATUSES:
                    errors.append(
                        f"{swhere}: verification.status '{vstatus}' not in controlled enum"
                    )
            keywords = section.get("keywords", [])
            if keywords is not None and not isinstance(keywords, list):
                errors.append(f"{swhere}: 'keywords' must be a list when present")


def _validate_issues(issues: Dict[str, Any], acts: Dict[str, Any], errors: List[str]) -> None:
    for issue_id, issue in issues.items():
        where = f"issue_mappings.json: issue '{issue_id}'"
        if not isinstance(issue, dict):
            errors.append(f"{where}: record must be an object")
            continue
        embedded = issue.get("issue_id")
        if embedded != issue_id:
            errors.append(
                f"{where}: embedded issue_id '{embedded}' does not equal its object key"
            )
        tax_status = issue.get("taxonomy_status")
        if tax_status not in TAXONOMY_STATUSES:
            errors.append(
                f"{where}: taxonomy_status '{tax_status}' not in controlled enum"
            )
        domain_id = issue.get("domain_id")
        if domain_id not in APPROVED_DOMAINS:
            errors.append(f"{where}: domain_id '{domain_id}' is not an approved domain")
        prototypes = issue.get("prototype_texts")
        if not isinstance(prototypes, list) or not all(
            isinstance(p, str) and p.strip() for p in (prototypes or [])
        ):
            errors.append(f"{where}: prototype_texts must be a list of non-empty strings")
        for i, ref in enumerate(issue.get("provision_references", []) or []):
            rwhere = f"{where}, provision_references[{i}]"
            if not isinstance(ref, dict):
                errors.append(f"{rwhere}: must be an object")
                continue
            act_id, section_id = ref.get("act_id"), ref.get("section_id")
            act = acts.get(act_id)
            if act is None:
                errors.append(f"{rwhere}: act_id '{act_id}' does not resolve")
            elif section_id not in act.get("sections", {}):
                errors.append(
                    f"{rwhere}: section_id '{section_id}' does not resolve under act '{act_id}'"
                )
            if not ref.get("provision_relevance_rationale"):
                errors.append(f"{rwhere}: missing provision_relevance_rationale (Layer B)")


def _validate_guidance_and_portals(
    issue_guidance: Dict[str, Any],
    portals: Dict[str, Any],
    issues: Dict[str, Any],
    errors: List[str],
) -> None:
    for portal_id, portal in portals.items():
        where = f"issue_actions_portals.json: portal '{portal_id}'"
        if not isinstance(portal, dict):
            errors.append(f"{where}: record must be an object")
            continue
        embedded = portal.get("portal_id")
        if embedded != portal_id:
            errors.append(
                f"{where}: embedded portal_id '{embedded}' does not equal its object key"
            )
        if portal.get("priority") not in PORTAL_PRIORITIES:
            errors.append(f"{where}: priority '{portal.get('priority')}' invalid")
        for issue_id in portal.get("supported_issue_ids", []) or []:
            if issue_id not in issues:
                errors.append(
                    f"{where}: supported_issue_id '{issue_id}' is not a known issue"
                )

    for issue_id, guidance in issue_guidance.items():
        where = f"issue_actions_portals.json: issue_guidance '{issue_id}'"
        if issue_id not in issues:
            errors.append(f"{where}: not a known issue in issue_mappings.json")
        if not isinstance(guidance, dict):
            errors.append(f"{where}: record must be an object")
            continue
        steps = guidance.get("action_steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"{where}: action_steps must be a non-empty list")
        elif len(steps) > MAX_ACTION_STEPS:
            errors.append(
                f"{where}: {len(steps)} action_steps exceeds the maximum of {MAX_ACTION_STEPS}"
            )
        for portal_id in guidance.get("portal_ids", []) or []:
            if portal_id not in portals:
                errors.append(f"{where}: portal_id '{portal_id}' does not resolve")


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def load_knowledge_base(kb_dir: Path) -> KnowledgeBase:
    """Load, validate, and index the three-file KB. Raises KBValidationError
    with the complete error list if anything is structurally wrong."""
    kb_dir = Path(kb_dir)
    errors: List[str] = []

    acts_doc = _load_json(kb_dir / "acts_and_sections.json", errors)
    mappings_doc = _load_json(kb_dir / "issue_mappings.json", errors)
    guidance_doc = _load_json(kb_dir / "issue_actions_portals.json", errors)
    if errors:
        raise KBValidationError(errors)

    def container(doc: Dict[str, Any], fname: str, key: str) -> Dict[str, Any]:
        value = doc.get(key)
        if not isinstance(value, dict):
            errors.append(f"{fname}: missing/invalid top-level '{key}' object")
            return {}
        return {k: v for k, v in value.items() if k not in _DOC_KEYS}

    acts = container(acts_doc, "acts_and_sections.json", "acts")
    issues = container(mappings_doc, "issue_mappings.json", "issues")
    issue_guidance = container(guidance_doc, "issue_actions_portals.json", "issue_guidance")
    portals = container(guidance_doc, "issue_actions_portals.json", "portals")
    if errors:
        raise KBValidationError(errors)

    _validate_acts(acts, errors)
    _validate_issues(issues, acts, errors)
    _validate_guidance_and_portals(issue_guidance, portals, issues, errors)
    if errors:
        raise KBValidationError(errors)

    kb = KnowledgeBase(
        acts=acts, issues=issues, issue_guidance=issue_guidance, portals=portals
    )
    for issue_id, issue in issues.items():
        kb.issues_by_domain.setdefault(issue["domain_id"], []).append(issue_id)
    for portal_id, portal in portals.items():
        for issue_id in portal.get("supported_issue_ids", []) or []:
            kb.portals_by_issue.setdefault(issue_id, []).append(portal_id)
    return kb


if __name__ == "__main__":  # manual self-check, not a service path
    default_dir = Path(__file__).resolve().parents[2] / "knowledge_base"
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else default_dir
    try:
        loaded = load_knowledge_base(target)
    except KBValidationError as exc:
        print(f"INVALID: {exc}")
        raise SystemExit(1)
    print(f"VALID knowledge base at {target}")
    for name, count in loaded.counts().items():
        print(f"  {name}: {count}")
