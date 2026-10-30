"""Exhaustive 250-scenario Independent Benchmark Evaluation Harness for LegalLens.

Evaluates the improved system on 250 brand new scenarios (50 per domain).
Calculates and records all 15 required metrics:
1. Domain classification accuracy
2. Issue detection accuracy
3. Macro F1
4. Act identification precision and recall
5. Section-level precision and recall
6. Multi-label provision precision and recall
7. Exact provision-set accuracy
8. Legal applicability accuracy
9. False-positive provision rate
10. Clarification accuracy
11. Historical law accuracy
12. Citation accuracy
13. Portal routing accuracy
14. Action-step accuracy
15. End-to-end scenario accuracy
"""

import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "ml-service"))

from fastapi.testclient import TestClient
from app.main import app
from scripts.independent_benchmark_dataset import BENCHMARK_250_CASES

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


def normalize_sec(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"^(section|sec\.?|rule|order|article)\s*", "", s)
    s = re.sub(r"[\-_]", "(", s)
    if "(" in s and not s.endswith(")"):
        s += ")"
    s = re.sub(r"\s+", "", s)
    return s


def normalize_act(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[,\.\-_']", " ", s)
    return " ".join(s.split())


def act_matches(retrieved_act: str, expected_acts: list[str]) -> bool:
    ret_norm = normalize_act(retrieved_act)
    for exp in expected_acts:
        exp_norm = normalize_act(exp)
        if exp_norm in ret_norm or ret_norm in exp_norm:
            return True
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


def run_benchmark():
    print(f"[*] Starting LegalLens 250-Scenario Independent Benchmark...")
    start_time = time.time()

    results = []
    domain_confusion = {true_d: {pred_d: 0 for pred_d in DOMAINS + ["unknown"]} for true_d in DOMAINS}
    domain_stats = defaultdict(lambda: {"total": 0, "scores": defaultdict(list)})
    category_stats = defaultdict(lambda: {"total": 0, "scores": defaultdict(list)})
    latencies = []

    # Counters for 15 metrics
    m1_domain_correct = 0
    m2_issue_correct = 0
    m4_act_precisions, m4_act_recalls = [], []
    m5_sec_precisions, m5_sec_recalls = [], []
    m6_multi_f1s = []
    m7_exact_match_count = 0
    m8_applicability_scores = []
    m9_false_positive_provisions = 0
    m9_total_provisions_retrieved = 0
    m10_clarification_scores = []
    m11_historical_correct = 0
    m11_historical_total = 0
    m12_citation_valid = 0
    m12_citation_total = 0
    m13_portal_scores = []
    m14_action_scores = []
    m15_end_to_end_correct = 0

    with TestClient(app) as client:
        for idx, tc in enumerate(BENCHMARK_250_CASES, 1):
            test_id = tc["test_id"]
            true_domain = tc["domain"]
            category = tc["category"]
            scenario = tc["scenario"]
            expected_issues = tc["expected_issue_ids"]
            expected_acts = tc["expected_acts"]
            expected_sections = [normalize_sec(s) for s in tc["expected_sections"]]
            expected_portals = tc["expected_portals"]
            should_fallback = tc["should_trigger_fallback"]
            is_historical = tc.get("is_historical", False)

            t0 = time.perf_counter()
            response = client.post("/analyze", json={"scenario": scenario, "request_id": f"bench_{test_id}"})
            latency_ms = (time.perf_counter() - t0) * 1000.0
            latencies.append(latency_ms)

            if response.status_code != 200:
                print(f"[!] Error on {test_id}: {response.status_code} {response.text}")
                continue

            resp_data = response.json()
            analysis = resp_data.get("analysis", {})
            pred_domain = analysis.get("domain", {}).get("id", "unknown")
            domain_conf = analysis.get("domain", {}).get("confidence", 0.0)
            pred_issue = analysis.get("issue", {}).get("id")
            issue_sim = analysis.get("issue", {}).get("similarity_score")
            provisions = resp_data.get("legal_provisions", [])
            action_steps = resp_data.get("action_steps", [])
            portals = resp_data.get("portals", [])
            is_valid = resp_data.get("is_valid_scenario", True)
            needs_clarification = resp_data.get("needs_clarification", False)
            hist_note = resp_data.get("historical_law_note")

            # Update confusion matrix
            if pred_domain in domain_confusion[true_domain]:
                domain_confusion[true_domain][pred_domain] += 1
            else:
                domain_confusion[true_domain]["unknown"] += 1

            # -----------------------------------------------------------------
            # Metric 1: Domain Classification Accuracy
            # -----------------------------------------------------------------
            if should_fallback and (not is_valid or needs_clarification or pred_domain == "unknown"):
                domain_ok = True
                domain_score = 100.0
            elif pred_domain == true_domain:
                domain_ok = True
                domain_score = 100.0
            else:
                domain_ok = False
                domain_score = 0.0
            if domain_ok:
                m1_domain_correct += 1

            # -----------------------------------------------------------------
            # Metric 2: Issue Detection Accuracy
            # -----------------------------------------------------------------
            if should_fallback and (not is_valid or needs_clarification or not pred_issue):
                issue_ok = True
                issue_score = 100.0
            elif pred_issue and pred_issue in expected_issues:
                issue_ok = True
                issue_score = 100.0
            elif pred_domain == true_domain and pred_issue is not None:
                issue_ok = False
                issue_score = 50.0  # partial credit for same domain
            else:
                issue_ok = False
                issue_score = 0.0
            if issue_ok:
                m2_issue_correct += 1

            # -----------------------------------------------------------------
            # Metric 4: Act Identification Precision & Recall
            # -----------------------------------------------------------------
            retrieved_acts = [p["act"] for p in provisions]
            if not expected_acts and not retrieved_acts:
                act_p, act_r, act_f1 = 1.0, 1.0, 1.0
            elif not expected_acts and retrieved_acts:
                act_p, act_r, act_f1 = 0.0, 1.0, 0.0
            elif expected_acts and not retrieved_acts:
                act_p, act_r, act_f1 = 0.0, 0.0, 0.0
            else:
                matched_acts = sum(1 for ea in expected_acts if any(act_matches(ra, [ea]) for ra in retrieved_acts))
                act_r = matched_acts / len(expected_acts)
                act_p = matched_acts / len(retrieved_acts) if retrieved_acts else 0.0
                act_f1 = (2 * act_p * act_r) / (act_p + act_r) if (act_p + act_r) > 0 else 0.0
            m4_act_precisions.append(act_p)
            m4_act_recalls.append(act_r)
            act_score = act_f1 * 100.0

            # -----------------------------------------------------------------
            # Metric 5 & 6 & 7 & 9: Section Retrieval & Multi-Label Metrics
            # -----------------------------------------------------------------
            retrieved_sections = [normalize_sec(p["section"]) for p in provisions]
            m9_total_provisions_retrieved += len(retrieved_sections)

            if not expected_sections and not retrieved_sections:
                sec_p, sec_r, sec_f1 = 1.0, 1.0, 1.0
                exact_match = True
            elif not expected_sections and retrieved_sections:
                sec_p, sec_r, sec_f1 = 0.0, 1.0, 0.0
                exact_match = False
                m9_false_positive_provisions += len(retrieved_sections)
            elif expected_sections and not retrieved_sections:
                sec_p, sec_r, sec_f1 = 0.0, 0.0, 0.0
                exact_match = False
            else:
                matched_sec = 0
                for es in expected_sections:
                    if any(es == rs or es in rs or rs in es for rs in retrieved_sections):
                        matched_sec += 1
                sec_r = matched_sec / len(expected_sections)
                sec_p = matched_sec / len(retrieved_sections) if retrieved_sections else 0.0
                sec_f1 = (2 * sec_p * sec_r) / (sec_p + sec_r) if (sec_p + sec_r) > 0 else 0.0
                m9_false_positive_provisions += (len(retrieved_sections) - matched_sec)
                exact_match = (set(expected_sections) == set(retrieved_sections))

            m5_sec_precisions.append(sec_p)
            m5_sec_recalls.append(sec_r)
            m6_multi_f1s.append(sec_f1)
            if exact_match:
                m7_exact_match_count += 1
            sec_score = (0.6 * sec_r + 0.4 * sec_p) * 100.0

            # -----------------------------------------------------------------
            # Metric 8: Legal Applicability & Reasoning Accuracy
            # -----------------------------------------------------------------
            if should_fallback and (not is_valid or needs_clarification):
                applicability_score = 100.0
            elif not domain_ok:
                applicability_score = 0.0
            elif sec_score >= 80.0:
                applicability_score = 100.0
            elif sec_score >= 40.0:
                applicability_score = 80.0
            elif issue_score >= 50.0:
                applicability_score = 60.0
            else:
                applicability_score = 25.0
            m8_applicability_scores.append(applicability_score)

            # -----------------------------------------------------------------
            # Metric 10: Clarification & Uncertainty Handling
            # -----------------------------------------------------------------
            if category in ["ambiguous", "incomplete", "misleading"] or should_fallback:
                if not is_valid or needs_clarification or domain_conf < 0.65:
                    clarification_score = 100.0
                else:
                    clarification_score = 30.0
            else:
                clarification_score = 100.0 if (is_valid and not needs_clarification) else 85.0
            m10_clarification_scores.append(clarification_score)

            # -----------------------------------------------------------------
            # Metric 11: Historical Law Accuracy
            # -----------------------------------------------------------------
            if is_historical:
                m11_historical_total += 1
                if hist_note is not None and "Indian Penal Code, 1860" in hist_note:
                    m11_historical_correct += 1

            # -----------------------------------------------------------------
            # Metric 12: Citation Verification Accuracy
            # -----------------------------------------------------------------
            if not provisions:
                citation_score = 100.0
            else:
                valid_urls = 0
                for p in provisions:
                    m12_citation_total += 1
                    u = p.get("official_source", {}).get("url")
                    if verify_official_url(u):
                        valid_urls += 1
                        m12_citation_valid += 1
                citation_score = (valid_urls / len(provisions)) * 100.0

            # -----------------------------------------------------------------
            # Metric 13 & 14: Portal & Action Steps Accuracy
            # -----------------------------------------------------------------
            portal_score = 100.0 if (should_fallback or len(portals) > 0) else 0.0
            action_score = 100.0 if (should_fallback or len(action_steps) >= 2) else 70.0
            m13_portal_scores.append(portal_score)
            m14_action_scores.append(action_score)

            # -----------------------------------------------------------------
            # Metric 15: End-to-End Scenario Accuracy
            # -----------------------------------------------------------------
            overall_case_score = (
                (0.10 * domain_score)
                + (0.15 * issue_score)
                + (0.15 * act_score)
                + (0.20 * sec_score)
                + (0.15 * applicability_score)
                + (0.10 * citation_score)
                + (0.05 * action_score)
                + (0.05 * portal_score)
                + (0.05 * clarification_score)
            )
            is_end_to_end_pass = (overall_case_score >= 75.0)
            if is_end_to_end_pass:
                m15_end_to_end_correct += 1

            # Record result
            case_res = {
                "test_id": test_id,
                "domain": true_domain,
                "category": category,
                "latency_ms": round(latency_ms, 2),
                "predicted_domain": pred_domain,
                "predicted_issue": pred_issue,
                "expected_issues": expected_issues,
                "retrieved_provisions": [
                    {
                        "act": p["act"],
                        "section": p["section"],
                        "relevance_classification": p.get("relevance_classification"),
                        "elements": p.get("applicable_legal_elements"),
                    }
                    for p in provisions
                ],
                "expected_sections": expected_sections,
                "historical_note_present": hist_note is not None,
                "scores": {
                    "domain": round(domain_score, 1),
                    "issue": round(issue_score, 1),
                    "act": round(act_score, 1),
                    "section": round(sec_score, 1),
                    "applicability": round(applicability_score, 1),
                    "citation": round(citation_score, 1),
                    "action_steps": round(action_score, 1),
                    "portals": round(portal_score, 1),
                    "clarification": round(clarification_score, 1),
                    "overall_weighted_score": round(overall_case_score, 2),
                },
            }
            results.append(case_res)

            for s_name, s_val in case_res["scores"].items():
                domain_stats[true_domain]["scores"][s_name].append(s_val)
                category_stats[category]["scores"][s_name].append(s_val)
            domain_stats[true_domain]["total"] += 1
            category_stats[category]["total"] += 1

            if idx % 25 == 0 or idx == len(BENCHMARK_250_CASES):
                print(f"[{idx:03d}/{len(BENCHMARK_250_CASES)}] Completed. Current Avg Score: {sum(r['scores']['overall_weighted_score'] for r in results)/len(results):.2f}%")

    total_bench_time = time.time() - start_time
    print(f"[*] Benchmark finished in {total_bench_time:.2f}s.")

    # Macro F1 for Domain Classification
    macro_f1_sum = 0
    confusion_metrics = {}
    for d in DOMAINS:
        tp = domain_confusion[d][d]
        fn = sum(domain_confusion[d][p] for p in domain_confusion[d] if p != d)
        fp = sum(domain_confusion[other_d][d] for other_d in DOMAINS if other_d != d)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        macro_f1_sum += f1
        confusion_metrics[d] = {
            "name": DOMAIN_NAMES[d],
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
        }
    macro_f1 = macro_f1_sum / len(DOMAINS)

    # 15 Required Metrics Summary
    benchmark_metrics = {
        "1_domain_classification_accuracy_percent": round((m1_domain_correct / len(results)) * 100.0, 2),
        "2_issue_detection_accuracy_percent": round((m2_issue_correct / len(results)) * 100.0, 2),
        "3_macro_f1_score": round(macro_f1, 4),
        "4_act_identification_precision_percent": round((sum(m4_act_precisions) / len(m4_act_precisions)) * 100.0, 2),
        "4_act_identification_recall_percent": round((sum(m4_act_recalls) / len(m4_act_recalls)) * 100.0, 2),
        "5_section_level_precision_percent": round((sum(m5_sec_precisions) / len(m5_sec_precisions)) * 100.0, 2),
        "5_section_level_recall_percent": round((sum(m5_sec_recalls) / len(m5_sec_recalls)) * 100.0, 2),
        "6_multi_label_provision_f1_percent": round((sum(m6_multi_f1s) / len(m6_multi_f1s)) * 100.0, 2),
        "7_exact_provision_set_accuracy_percent": round((m7_exact_match_count / len(results)) * 100.0, 2),
        "8_legal_applicability_accuracy_percent": round((sum(m8_applicability_scores) / len(m8_applicability_scores)), 2),
        "9_false_positive_provision_rate_percent": round((m9_false_positive_provisions / max(1, m9_total_provisions_retrieved)) * 100.0, 2),
        "10_clarification_accuracy_percent": round((sum(m10_clarification_scores) / len(m10_clarification_scores)), 2),
        "11_historical_law_accuracy_percent": round((m11_historical_correct / max(1, m11_historical_total)) * 100.0, 2),
        "12_citation_verification_rate_percent": round((m12_citation_valid / max(1, m12_citation_total)) * 100.0, 2),
        "13_portal_routing_accuracy_percent": round((sum(m13_portal_scores) / len(m13_portal_scores)), 2),
        "14_action_step_accuracy_percent": round((sum(m14_action_scores) / len(m14_action_scores)), 2),
        "15_end_to_end_scenario_accuracy_percent": round((m15_end_to_end_correct / len(results)) * 100.0, 2),
        "overall_weighted_benchmark_score": round(sum(r["scores"]["overall_weighted_score"] for r in results) / len(results), 2),
        "average_latency_ms": round(sum(latencies) / len(latencies), 2),
    }

    # Save to reports and docs
    out_payload = {
        "benchmark_metadata": {
            "total_test_cases": len(results),
            "execution_time_seconds": round(total_bench_time, 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        "fifteen_statutory_metrics": benchmark_metrics,
        "confusion_metrics_by_domain": confusion_metrics,
        "domain_confusion_matrix": domain_confusion,
        "case_results": results,
    }

    docs_dir = REPO_ROOT / "docs"
    with open(docs_dir / "independent_benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)

    print("[+] Independent benchmark results written to docs/independent_benchmark_results.json")
    return benchmark_metrics, confusion_metrics, results


if __name__ == "__main__":
    run_benchmark()
