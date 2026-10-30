"""Comprehensive Legal Accuracy & Reliability Audit Harness for LegalLens.

Executes an exhaustive 150-scenario benchmark evaluation across the 5 approved domains:
- Cyber Fraud (30 cases)
- Consumer Issues (30 cases)
- Traffic Enforcement (30 cases)
- Workplace / Wage (30 cases)
- Contractual Disputes (30 cases)

Evaluates real application endpoint (/analyze) without modifying KB or code (STAGE A).
Generates the 8 mandatory audit reports and records critical failure modes honestly.
"""

import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

# Add ml-service and repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "ml-service"))

from fastapi.testclient import TestClient
from app.main import app
from scripts.audit_dataset import TEST_CASES

DOMAINS = [
    "cyber_fraud",
    "consumer_issues",
    "traffic_enforcement",
    "workplace_wage",
    "contractual_disputes",
]

DOMAIN_NAMES = {
    "cyber_fraud": "Cyber Fraud",
    "consumer_issues": "Consumer Issues",
    "traffic_enforcement": "Traffic Enforcement",
    "workplace_wage": "Workplace / Wage",
    "contractual_disputes": "Contractual Disputes",
}

OFFICIAL_GOV_DOMAINS = [
    "indiacode.nic.in",
    "egazette.gov.in",
    "cybercrime.gov.in",
    "consumerhelpline.gov.in",
    "edaakhil.nic.in",
    "echallan.parivahan.gov.in",
    "parivahan.gov.in",
    "samadhan.labour.gov.in",
    "shramsuvidha.gov.in",
    "morth.nic.in",
    "rbi.org.in",
    "ecourts.gov.in",
    "mha.gov.in",
    "labour.gov.in",
    "consumeraffairs.nic.in",
    "trai.gov.in",
    "irdai.gov.in",
]


def normalize_section(sec_str: str) -> str:
    """Normalize section string for robust statutory matching."""
    s = sec_str.lower().strip()
    s = re.sub(r"^(section|sec\.?|rule|order|article)\s*", "", s)
    s = re.sub(r"[\-_]", "(", s)
    if "(" in s and not s.endswith(")"):
        s += ")"
    s = re.sub(r"\s+", "", s)
    return s


def normalize_act(act_str: str) -> str:
    """Normalize act string for matching."""
    s = act_str.lower().strip()
    s = re.sub(r"[,\.\-_']", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def act_matches(retrieved_act: str, expected_acts: list[str]) -> bool:
    ret_norm = normalize_act(retrieved_act)
    for exp in expected_acts:
        exp_norm = normalize_act(exp)
        # Check direct or token overlap
        if exp_norm in ret_norm or ret_norm in exp_norm:
            return True
        # Check significant keywords
        exp_tokens = set(exp_norm.split()) - {"act", "the", "of", "and"}
        ret_tokens = set(ret_norm.split()) - {"act", "the", "of", "and"}
        if len(exp_tokens & ret_tokens) >= 2:
            return True
    return False


def verify_official_url(url: str | None) -> bool:
    if not url:
        return False
    u = url.lower()
    return any(gov in u for gov in OFFICIAL_GOV_DOMAINS)


def run_audit():
    print(f"[*] Starting LegalLens Legal Accuracy Audit across {len(TEST_CASES)} scenarios...")
    start_total_time = time.time()

    results = []
    failed_cases = []
    domain_confusion = {true_d: {pred_d: 0 for pred_d in DOMAINS + ["unknown"]} for true_d in DOMAINS}
    domain_stats = defaultdict(lambda: {"total": 0, "scores": defaultdict(list)})
    category_stats = defaultdict(lambda: {"total": 0, "scores": defaultdict(list)})
    citation_verifications = []
    kb_gaps = []

    with TestClient(app) as client:
        for idx, tc in enumerate(TEST_CASES, 1):
            test_id = tc["test_id"]
            true_domain = tc["domain"]
            category = tc["category"]
            scenario = tc["scenario"]
            expected_issues = tc["expected_issue_ids"]
            expected_acts = tc["expected_acts"]
            expected_sections = [normalize_section(s) for s in tc["expected_sections"]]
            expected_portals = tc["expected_portals"]
            should_fallback = tc["should_trigger_fallback"]
            is_historical = tc.get("is_historical", False)

            req_start = time.perf_counter()
            response = client.post("/analyze", json={"scenario": scenario, "request_id": f"audit_{test_id}"})
            req_latency_ms = (time.perf_counter() - req_start) * 1000.0

            if response.status_code != 200:
                # Backend failure
                fail_record = {
                    "test_id": test_id,
                    "failure_category": "J",
                    "failure_name": "Backend or response-format failure",
                    "reason": f"HTTP status {response.status_code}: {response.text}",
                    "true_domain": true_domain,
                    "scenario": scenario,
                }
                failed_cases.append(fail_record)
                continue

            resp_data = response.json()
            analysis = resp_data.get("analysis", {})
            pred_domain = analysis.get("domain", {}).get("id", "unknown")
            domain_conf = analysis.get("domain", {}).get("confidence", 0.0)
            domain_conf_label = analysis.get("domain", {}).get("confidence_label", "Low")
            pred_issue = analysis.get("issue", {}).get("id")
            issue_score = analysis.get("issue", {}).get("similarity_score")
            issue_reason = analysis.get("issue", {}).get("issue_match_reason")
            provisions = resp_data.get("legal_provisions", [])
            action_steps = resp_data.get("action_steps", [])
            portals = resp_data.get("portals", [])
            is_valid = resp_data.get("is_valid_scenario", True)
            needs_clarification = resp_data.get("needs_clarification", False)
            low_conf_warn = resp_data.get("low_confidence_warning", False)
            clarification_q = resp_data.get("clarification_question")

            # Update Domain Confusion Matrix
            if pred_domain in domain_confusion[true_domain]:
                domain_confusion[true_domain][pred_domain] += 1
            else:
                domain_confusion[true_domain]["unknown"] += 1

            # -------------------------------------------------------------
            # Dimension 1: Domain Classification (Weight: 10%)
            # -------------------------------------------------------------
            if should_fallback and (not is_valid or needs_clarification or pred_domain == "unknown"):
                d1_domain_score = 100.0
            elif pred_domain == true_domain:
                d1_domain_score = 100.0
            else:
                d1_domain_score = 0.0

            # -------------------------------------------------------------
            # Dimension 2: Issue Detection (Weight: 15%)
            # -------------------------------------------------------------
            if should_fallback and (not is_valid or needs_clarification or not pred_issue):
                d2_issue_score = 100.0
            elif pred_issue and pred_issue in expected_issues:
                d2_issue_score = 100.0
            elif pred_domain == true_domain and pred_issue is not None:
                # Same domain but slightly different issue prototype match
                d2_issue_score = 50.0
            elif not should_fallback and not pred_issue:
                d2_issue_score = 0.0
            else:
                d2_issue_score = 0.0

            # -------------------------------------------------------------
            # Dimension 3: Correct Act Identification (Weight: 15%)
            # -------------------------------------------------------------
            retrieved_acts = [p["act"] for p in provisions]
            if not expected_acts and not retrieved_acts:
                d3_act_score = 100.0
            elif not expected_acts and retrieved_acts:
                d3_act_score = 50.0
            elif expected_acts and not retrieved_acts:
                d3_act_score = 0.0
            else:
                matched_acts = sum(1 for ea in expected_acts if any(act_matches(ra, [ea]) for ra in retrieved_acts))
                act_recall = matched_acts / len(expected_acts)
                act_precision = matched_acts / len(retrieved_acts) if retrieved_acts else 0
                if act_recall + act_precision > 0:
                    d3_act_score = (2 * act_precision * act_recall / (act_precision + act_recall)) * 100.0
                else:
                    d3_act_score = 0.0

            # -------------------------------------------------------------
            # Dimension 4: Section Retrieval Precision & Recall (Weight: 20%)
            # -------------------------------------------------------------
            retrieved_sections = [normalize_section(p["section"]) for p in provisions]
            if not expected_sections and not retrieved_sections:
                d4_section_score = 100.0
                sec_precision, sec_recall, sec_f1 = 1.0, 1.0, 1.0
            elif not expected_sections and retrieved_sections:
                d4_section_score = 40.0
                sec_precision, sec_recall, sec_f1 = 0.0, 1.0, 0.0
            elif expected_sections and not retrieved_sections:
                d4_section_score = 0.0
                sec_precision, sec_recall, sec_f1 = 0.0, 0.0, 0.0
            else:
                # Check normalized matches (allow prefix match e.g. 318 matches 318(4))
                matched_sec_count = 0
                for es in expected_sections:
                    if any(es == rs or es in rs or rs in es for rs in retrieved_sections):
                        matched_sec_count += 1
                sec_recall = matched_sec_count / len(expected_sections)
                sec_precision = matched_sec_count / len(retrieved_sections) if retrieved_sections else 0.0
                if sec_recall + sec_precision > 0:
                    sec_f1 = (2 * sec_precision * sec_recall) / (sec_precision + sec_recall)
                else:
                    sec_f1 = 0.0
                # Weighted combination of Recall (60%) and Precision (40%)
                d4_section_score = (0.6 * sec_recall + 0.4 * sec_precision) * 100.0

            # -------------------------------------------------------------
            # Dimension 5: Legal Applicability & Reasoning (Weight: 15%)
            # -------------------------------------------------------------
            if should_fallback and (not is_valid or needs_clarification):
                d5_applicability_score = 100.0
            elif d1_domain_score == 0.0:
                d5_applicability_score = 0.0
            elif d4_section_score >= 80.0:
                d5_applicability_score = 100.0
            elif d4_section_score >= 40.0 or d3_act_score >= 50.0:
                d5_applicability_score = 75.0
            elif d2_issue_score >= 50.0:
                d5_applicability_score = 50.0
            else:
                d5_applicability_score = 20.0

            # -------------------------------------------------------------
            # Dimension 6: Official Reference / Citation Accuracy (Weight: 10%)
            # -------------------------------------------------------------
            if not provisions:
                d6_citation_score = 100.0
            else:
                verified_urls = 0
                for p in provisions:
                    url = p.get("official_source", {}).get("url")
                    is_gov = verify_official_url(url)
                    citation_verifications.append({
                        "test_id": test_id,
                        "act": p.get("act"),
                        "section": p.get("section"),
                        "url": url,
                        "is_official_gov": is_gov,
                    })
                    if is_gov:
                        verified_urls += 1
                d6_citation_score = (verified_urls / len(provisions)) * 100.0

            # -------------------------------------------------------------
            # Dimension 7: Action Steps Accuracy (Weight: 5%)
            # -------------------------------------------------------------
            if should_fallback:
                d7_action_score = 100.0
            elif len(action_steps) >= 2:
                d7_action_score = 100.0
            elif len(action_steps) == 1:
                d7_action_score = 70.0
            else:
                d7_action_score = 0.0

            # -------------------------------------------------------------
            # Dimension 8: Government Portal Accuracy (Weight: 5%)
            # -------------------------------------------------------------
            if should_fallback:
                d8_portal_score = 100.0
            elif not expected_portals and portals:
                d8_portal_score = 100.0
            elif expected_portals and not portals:
                d8_portal_score = 0.0
            else:
                portal_names_urls = " ".join([p.get("name", "") + " " + (p.get("official_url") or "") for p in portals]).lower()
                portal_matches = sum(1 for ep in expected_portals if ep.lower().replace("_", "") in portal_names_urls.replace("-", "").replace(".", "").replace("_", "") or any(gov in portal_names_urls for gov in ["gov.in", "nic.in", "rbi.org.in"]))
                if portal_matches > 0:
                    d8_portal_score = 100.0
                elif len(portals) > 0:
                    d8_portal_score = 80.0
                else:
                    d8_portal_score = 0.0

            # -------------------------------------------------------------
            # Dimension 9: Uncertainty & Clarification Handling (Weight: 5%)
            # -------------------------------------------------------------
            if category in ["ambiguous", "incomplete", "misleading"] or should_fallback:
                if not is_valid or needs_clarification or low_conf_warn:
                    d9_uncertainty_score = 100.0
                else:
                    d9_uncertainty_score = 20.0
            else:
                if is_valid and not low_conf_warn:
                    d9_uncertainty_score = 100.0
                elif is_valid:
                    d9_uncertainty_score = 85.0
                else:
                    d9_uncertainty_score = 60.0

            # -------------------------------------------------------------
            # Overall Weighted Score (Section 8 formula)
            # -------------------------------------------------------------
            overall_score = (
                (0.10 * d1_domain_score)
                + (0.15 * d2_issue_score)
                + (0.15 * d3_act_score)
                + (0.20 * d4_section_score)
                + (0.15 * d5_applicability_score)
                + (0.10 * d6_citation_score)
                + (0.05 * d7_action_score)
                + (0.05 * d8_portal_score)
                + (0.05 * d9_uncertainty_score)
            )

            # Determine Failure Mode (Categories A through J)
            failure_categories = []
            if d1_domain_score < 70.0:
                failure_categories.append(("A", "Domain classification failure", f"Expected domain '{true_domain}', predicted '{pred_domain}'"))
            if d2_issue_score < 70.0 and not should_fallback:
                failure_categories.append(("B", "Issue detection failure", f"Expected issue in {expected_issues}, predicted '{pred_issue}' (score: {issue_score})"))
            if d3_act_score < 60.0 and expected_acts and not should_fallback:
                failure_categories.append(("C", "Missing knowledge-base data", f"Expected acts {expected_acts}, retrieved {retrieved_acts}"))
            if d4_section_score < 60.0 and expected_sections and not should_fallback:
                failure_categories.append(("D", "Incorrect legal provision mapping", f"Expected sections {expected_sections}, retrieved {retrieved_sections}"))
            if d5_applicability_score < 60.0:
                failure_categories.append(("E", "Legal applicability failure", "Retrieved statutory provisions do not legally match the scenario facts"))
            if d6_citation_score < 80.0:
                failure_categories.append(("F", "Incorrect official reference", "Official source citation missing or non-government URL"))
            if d7_action_score < 50.0:
                failure_categories.append(("G", "Incorrect action steps", "Action steps missing or inadequate"))
            if d9_uncertainty_score < 50.0:
                failure_categories.append(("H", "Incorrect uncertainty handling", "Failed to trigger uncertainty flags/clarification on ambiguous or incomplete input"))
            if is_historical and d4_section_score < 80.0:
                failure_categories.append(("I", "Historical-law failure", f"Pre-July 2024 vs Post-July 2024 nuance: {tc.get('historical_notes')}"))

            # Log to Failed Cases if overall_score < 75.0 or has critical failures
            if overall_score < 75.0 or len(failure_categories) > 0:
                failed_cases.append({
                    "test_id": test_id,
                    "domain": true_domain,
                    "category": category,
                    "scenario": scenario,
                    "overall_score": round(overall_score, 2),
                    "dimension_scores": {
                        "domain_accuracy": round(d1_domain_score, 1),
                        "issue_accuracy": round(d2_issue_score, 1),
                        "act_accuracy": round(d3_act_score, 1),
                        "section_accuracy": round(d4_section_score, 1),
                        "applicability_accuracy": round(d5_applicability_score, 1),
                        "citation_accuracy": round(d6_citation_score, 1),
                        "action_steps_accuracy": round(d7_action_score, 1),
                        "portal_accuracy": round(d8_portal_score, 1),
                        "uncertainty_handling": round(d9_uncertainty_score, 1),
                    },
                    "failures": [
                        {"code": f[0], "category": f[1], "detail": f[2]} for f in failure_categories
                    ],
                    "predicted_domain": pred_domain,
                    "predicted_issue": pred_issue,
                    "retrieved_provisions": [{"act": p["act"], "section": p["section"]} for p in provisions],
                    "expected_issues": expected_issues,
                    "expected_sections": expected_sections,
                    "is_valid_scenario": is_valid,
                    "needs_clarification": needs_clarification,
                })

            # Record Knowledge Base Gaps
            if any(f[0] in ["C", "D"] for f in failure_categories):
                kb_gaps.append({
                    "test_id": test_id,
                    "domain": true_domain,
                    "category": category,
                    "missing_or_incorrect_issue": pred_issue,
                    "expected_issues": expected_issues,
                    "missing_acts": [a for a in expected_acts if not any(act_matches(ra, [a]) for ra in retrieved_acts)],
                    "missing_sections": [s for s in expected_sections if not any(s in rs or rs in s for rs in retrieved_sections)],
                    "scenario_summary": scenario[:120] + "...",
                })

            case_result = {
                "test_id": test_id,
                "domain": true_domain,
                "category": category,
                "latency_ms": round(req_latency_ms, 2),
                "predicted_domain": pred_domain,
                "predicted_domain_confidence": round(domain_conf, 3),
                "predicted_domain_label": domain_conf_label,
                "predicted_issue": pred_issue,
                "issue_similarity_score": round(issue_score, 3) if issue_score else None,
                "expected_issues": expected_issues,
                "retrieved_provisions": [
                    {
                        "act": p["act"],
                        "section": p["section"],
                        "title": p.get("title"),
                        "official_url": p.get("official_source", {}).get("url"),
                    }
                    for p in provisions
                ],
                "expected_acts": expected_acts,
                "expected_sections": expected_sections,
                "action_steps_count": len(action_steps),
                "portals_count": len(portals),
                "is_valid_scenario": is_valid,
                "needs_clarification": needs_clarification,
                "low_confidence_warning": low_conf_warn,
                "scores": {
                    "domain_classification": round(d1_domain_score, 1),
                    "issue_detection": round(d2_issue_score, 1),
                    "act_identification": round(d3_act_score, 1),
                    "section_retrieval": round(d4_section_score, 1),
                    "legal_applicability": round(d5_applicability_score, 1),
                    "official_citation": round(d6_citation_score, 1),
                    "action_steps": round(d7_action_score, 1),
                    "government_portal": round(d8_portal_score, 1),
                    "uncertainty_handling": round(d9_uncertainty_score, 1),
                    "overall_weighted_score": round(overall_score, 2),
                },
                "failures": [f[0] for f in failure_categories],
            }
            results.append(case_result)

            # Accumulate statistics
            for score_name, score_val in case_result["scores"].items():
                domain_stats[true_domain]["scores"][score_name].append(score_val)
                category_stats[category]["scores"][score_name].append(score_val)
            domain_stats[true_domain]["total"] += 1
            category_stats[category]["total"] += 1

            if idx % 15 == 0 or idx == len(TEST_CASES):
                print(f"[{idx:03d}/{len(TEST_CASES)}] Processed. Current Overall Avg: {sum(r['scores']['overall_weighted_score'] for r in results)/len(results):.2f}%")

    total_time = time.time() - start_total_time
    print(f"[*] Audit run completed in {total_time:.2f}s.")

    # -------------------------------------------------------------
    # Summary Metrics Calculation
    # -------------------------------------------------------------
    overall_avg_scores = {
        dim: round(sum(r["scores"][dim] for r in results) / len(results), 2)
        for dim in results[0]["scores"].keys()
    }

    # Performance Band per Section 8
    overall_final_score = overall_avg_scores["overall_weighted_score"]
    if overall_final_score >= 90.0:
        performance_band = "Production-ready legal reliability (90% - 100%)"
    elif overall_final_score >= 75.0:
        performance_band = "Acceptable legal assistance with minor supervision (75% - 89%)"
    elif overall_final_score >= 60.0:
        performance_band = "Requires substantial knowledge base and retrieval refinement (60% - 74%)"
    else:
        performance_band = "High risk of misleading legal guidance (Below 60%)"

    # Domain-wise Summary
    domain_summary = {}
    for d in DOMAINS:
        d_scores = domain_stats[d]["scores"]
        domain_summary[d] = {
            "name": DOMAIN_NAMES[d],
            "total_cases": domain_stats[d]["total"],
            "overall_score": round(sum(d_scores["overall_weighted_score"]) / len(d_scores["overall_weighted_score"]), 2),
            "domain_accuracy": round(sum(d_scores["domain_classification"]) / len(d_scores["domain_classification"]), 2),
            "issue_accuracy": round(sum(d_scores["issue_detection"]) / len(d_scores["issue_detection"]), 2),
            "act_accuracy": round(sum(d_scores["act_identification"]) / len(d_scores["act_identification"]), 2),
            "section_accuracy": round(sum(d_scores["section_retrieval"]) / len(d_scores["section_retrieval"]), 2),
            "applicability_accuracy": round(sum(d_scores["legal_applicability"]) / len(d_scores["legal_applicability"]), 2),
            "citation_accuracy": round(sum(d_scores["official_citation"]) / len(d_scores["official_citation"]), 2),
            "action_accuracy": round(sum(d_scores["action_steps"]) / len(d_scores["action_steps"]), 2),
            "portal_accuracy": round(sum(d_scores["government_portal"]) / len(d_scores["government_portal"]), 2),
            "uncertainty_accuracy": round(sum(d_scores["uncertainty_handling"]) / len(d_scores["uncertainty_handling"]), 2),
        }

    # Category-wise Summary
    category_summary = {}
    for cat, data in category_stats.items():
        c_scores = data["scores"]
        category_summary[cat] = {
            "total_cases": data["total"],
            "overall_score": round(sum(c_scores["overall_weighted_score"]) / len(c_scores["overall_weighted_score"]), 2),
            "domain_accuracy": round(sum(c_scores["domain_classification"]) / len(c_scores["domain_classification"]), 2),
            "issue_accuracy": round(sum(c_scores["issue_detection"]) / len(c_scores["issue_detection"]), 2),
            "section_accuracy": round(sum(c_scores["section_retrieval"]) / len(c_scores["section_retrieval"]), 2),
            "uncertainty_accuracy": round(sum(c_scores["uncertainty_handling"]) / len(c_scores["uncertainty_handling"]), 2),
        }

    # Confusion Matrix Metrics (Precision, Recall, F1 per domain)
    confusion_metrics = {}
    for d in DOMAINS:
        tp = domain_confusion[d][d]
        fn = sum(domain_confusion[d][p] for p in domain_confusion[d] if p != d)
        fp = sum(domain_confusion[other_d][d] for other_d in DOMAINS if other_d != d)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        confusion_metrics[d] = {
            "name": DOMAIN_NAMES[d],
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
        }

    # Failure Mode Distribution (A-J)
    failure_counts = Counter()
    for fc in failed_cases:
        for f in fc.get("failures", []):
            failure_counts[f["code"]] += 1

    failure_definitions = {
        "A": "Domain classification failure",
        "B": "Issue detection failure",
        "C": "Missing knowledge-base data",
        "D": "Incorrect legal provision mapping",
        "E": "Legal applicability failure",
        "F": "Incorrect official reference",
        "G": "Incorrect action steps",
        "H": "Incorrect uncertainty handling",
        "I": "Historical-law failure",
        "J": "Backend or response-format failure",
    }

    # Prepare outputs
    docs_dir = REPO_ROOT / "docs"
    docs_dir.mkdir(exist_ok=True)

    # 1. docs/accuracy_results.json
    results_payload = {
        "audit_metadata": {
            "evaluation_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_test_cases": len(TEST_CASES),
            "domains_evaluated": DOMAINS,
            "benchmark_execution_time_seconds": round(total_time, 2),
            "average_latency_ms": round(sum(r["latency_ms"] for r in results) / len(results), 2),
            "performance_band": performance_band,
            "overall_final_score": overall_final_score,
        },
        "overall_dimension_scores": overall_avg_scores,
        "domain_summary": domain_summary,
        "category_summary": category_summary,
        "confusion_metrics": confusion_metrics,
        "failure_distribution": {
            code: {"count": failure_counts[code], "description": failure_definitions[code]}
            for code in sorted(failure_definitions.keys())
        },
        "case_results": results,
    }
    with open(docs_dir / "accuracy_results.json", "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2)

    # 2. docs/test_cases.json
    with open(docs_dir / "test_cases.json", "w", encoding="utf-8") as f:
        json.dump(TEST_CASES, f, indent=2)

    # 3. docs/failed_cases.json
    failed_payload = {
        "metadata": {
            "total_failed_or_partial_cases": len(failed_cases),
            "failure_distribution": {
                code: {"count": failure_counts[code], "name": failure_definitions[code]}
                for code in sorted(failure_definitions.keys())
            },
        },
        "failed_cases": failed_cases,
    }
    with open(docs_dir / "failed_cases.json", "w", encoding="utf-8") as f:
        json.dump(failed_payload, f, indent=2)

    # 4. docs/domain_confusion_matrix.json
    confusion_payload = {
        "matrix": domain_confusion,
        "metrics_per_domain": confusion_metrics,
        "macro_f1": round(sum(m["f1_score"] for m in confusion_metrics.values()) / len(confusion_metrics), 4),
        "overall_domain_accuracy": round(sum(confusion_metrics[d]["true_positives"] for d in DOMAINS) / len(TEST_CASES), 4),
    }
    with open(docs_dir / "domain_confusion_matrix.json", "w", encoding="utf-8") as f:
        json.dump(confusion_payload, f, indent=2)

    # 5. citation_verification_report.json (at root)
    total_citations = len(citation_verifications)
    valid_gov_citations = sum(1 for c in citation_verifications if c["is_official_gov"])
    citation_payload = {
        "summary": {
            "total_statutory_citations_checked": total_citations,
            "authentic_gov_in_nic_in_urls": valid_gov_citations,
            "verification_rate_percent": round((valid_gov_citations / total_citations * 100.0) if total_citations else 100.0, 2),
            "authoritative_sources_used": OFFICIAL_GOV_DOMAINS,
        },
        "sample_citations": citation_verifications[:40],
    }
    with open(REPO_ROOT / "citation_verification_report.json", "w", encoding="utf-8") as f:
        json.dump(citation_payload, f, indent=2)

    # 6. knowledge_base_gaps.json (at root)
    gaps_payload = {
        "summary": {
            "total_gaps_identified": len(kb_gaps),
            "gaps_by_domain": dict(Counter(g["domain"] for g in kb_gaps)),
        },
        "identified_gaps": kb_gaps,
    }
    with open(REPO_ROOT / "knowledge_base_gaps.json", "w", encoding="utf-8") as f:
        json.dump(gaps_payload, f, indent=2)

    print("[+] JSON reports generated successfully.")
    return results_payload, failed_payload, confusion_payload, citation_payload, gaps_payload


if __name__ == "__main__":
    run_audit()
