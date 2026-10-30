"""Runner script for LegalLens 250-Scenario Multilingual Benchmark.

Evaluates performance across English, Kannada, Hindi, Romanized Kannada (Kanglish),
Romanized Hindi (Hinglish), and Code-mixed inputs.
Outputs language-wise comparison tables and cross-language consistency metrics.
"""

from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

BENCHMARK_CASES = Path("docs/multilingual_benchmark_cases.json")
RESULTS_OUT = Path("docs/multilingual_benchmark_results.json")


def normalize_sec(s: str) -> str:
    s = s.lower().replace("section", "").replace("sec", "").replace("rule", "").strip()
    return s.replace("_", "(").replace(")", "")


def evaluate_benchmark():
    with open(BENCHMARK_CASES, encoding="utf-8") as f:
        cases = json.load(f)

    print(f"[*] Starting Multilingual Benchmark across {len(cases)} cases...")

    results_by_case = []
    lang_stats = defaultdict(lambda: {
        "total": 0,
        "lang_detect_correct": 0,
        "domain_correct": 0,
        "issue_correct": 0,
        "valid_scenario_count": 0,
        "sec_recall_sum": 0.0,
        "sec_prec_sum": 0.0,
        "act_recall_sum": 0.0,
        "total_latency_ms": 0.0,
        "domain_preds": Counter(),
        "domain_truths": Counter()
    })

    parallel_groups = defaultdict(dict)

    with TestClient(app) as client:
        for idx, c in enumerate(cases, 1):
            t0 = time.perf_counter()
            resp = client.post("/analyze", json={"scenario": c["scenario"]})
            latency_ms = (time.perf_counter() - t0) * 1000.0

            data = resp.json()
            domain_pred = data.get("analysis", {}).get("domain", {}).get("id")
            issue_pred = data.get("analysis", {}).get("issue", {}).get("id")
            det_lang = data.get("detected_language")
            is_valid = data.get("is_valid_scenario", False)
            retrieved_provisions = data.get("legal_provisions", [])

            # Metrics
            lang_key = c["language"]
            # Script check
            lang_match = False
            if lang_key in ("kn", "kn-en") and det_lang in ("kn", "kn-en", "kn-Latn"):
                lang_match = True
            elif lang_key in ("hi", "hi-en") and det_lang in ("hi", "hi-en", "hi-Latn"):
                lang_match = True
            elif lang_key == "kn-Latn" and det_lang in ("kn-Latn", "kn", "kn-en"):
                lang_match = True
            elif lang_key == "hi-Latn" and det_lang in ("hi-Latn", "hi", "hi-en"):
                lang_match = True
            elif lang_key == "en" and det_lang == "en":
                lang_match = True

            domain_match = (domain_pred == c["domain"])
            issue_match = (issue_pred == c["expected_issue"])

            # Sections
            exp_secs = {normalize_sec(s) for s in c["expected_sections"]}
            ret_secs = {normalize_sec(p["section"]) for p in retrieved_provisions}
            overlap = exp_secs & ret_secs
            sec_recall = len(overlap) / len(exp_secs) if exp_secs else 1.0
            sec_prec = len(overlap) / len(ret_secs) if ret_secs else 0.0

            # Acts
            exp_acts = {a.lower() for a in c["expected_acts"]}
            ret_acts = {p["act"].lower() for p in retrieved_provisions}
            act_overlap = exp_acts & ret_acts
            act_recall = len(act_overlap) / len(exp_acts) if exp_acts else 1.0

            # Update stats
            s = lang_stats[lang_key]
            s["total"] += 1
            if lang_match:
                s["lang_detect_correct"] += 1
            if domain_match:
                s["domain_correct"] += 1
            if issue_match:
                s["issue_correct"] += 1
            if is_valid:
                s["valid_scenario_count"] += 1
            s["sec_recall_sum"] += sec_recall
            s["sec_prec_sum"] += sec_prec
            s["act_recall_sum"] += act_recall
            s["total_latency_ms"] += latency_ms
            s["domain_truths"][c["domain"]] += 1
            s["domain_preds"][domain_pred] += 1

            # Parallel group record
            grp = c.get("parallel_group_id")
            if grp:
                parallel_groups[grp][lang_key] = {
                    "domain": domain_pred,
                    "issue": issue_pred,
                    "sections": list(ret_secs)
                }

            results_by_case.append({
                "test_id": c["test_id"],
                "language": lang_key,
                "domain": c["domain"],
                "predicted_domain": domain_pred,
                "expected_issue": c["expected_issue"],
                "predicted_issue": issue_pred,
                "detected_language": det_lang,
                "domain_correct": domain_match,
                "issue_correct": issue_match,
                "section_recall": sec_recall,
                "section_precision": sec_prec,
                "latency_ms": latency_ms
            })

            if idx % 50 == 0 or idx == len(cases):
                print(f"[{idx:03d}/{len(cases)}] Processed...")

    # Cross-language consistency calculation
    consistent_groups = 0
    total_groups = len(parallel_groups)
    for grp, lang_map in parallel_groups.items():
        # Check if predictions across all available languages in the group agree on domain
        domains_in_grp = {v["domain"] for v in lang_map.values()}
        issues_in_grp = {v["issue"] for v in lang_map.values()}
        if len(domains_in_grp) == 1 and len(issues_in_grp) == 1:
            consistent_groups += 1

    group_consistency_pct = (consistent_groups / total_groups) * 100.0 if total_groups else 0.0

    print("\n" + "=" * 95)
    print(f"{'Language':12s} | {'Cases':5s} | {'LangDet%':9s} | {'Domain%':8s} | {'Issue%':7s} | {'SecRec%':8s} | {'SecPrec%':8s} | {'Latency':7s}")
    print("=" * 95)

    summary_by_lang = {}
    for lk, st in sorted(lang_stats.items()):
        tot = st["total"]
        ld_pct = (st["lang_detect_correct"] / tot) * 100.0
        dom_pct = (st["domain_correct"] / tot) * 100.0
        iss_pct = (st["issue_correct"] / tot) * 100.0
        sec_rec = (st["sec_recall_sum"] / tot) * 100.0
        sec_prec = (st["sec_prec_sum"] / tot) * 100.0
        lat_avg = st["total_latency_ms"] / tot
        summary_by_lang[lk] = {
            "total_cases": tot,
            "language_detection_accuracy": round(ld_pct, 2),
            "domain_classification_accuracy": round(dom_pct, 2),
            "issue_detection_accuracy": round(iss_pct, 2),
            "section_recall": round(sec_rec, 2),
            "section_precision": round(sec_prec, 2),
            "average_latency_ms": round(lat_avg, 2)
        }
        print(f"{lk:12s} | {tot:5d} | {ld_pct:8.1f}% | {dom_pct:7.1f}% | {iss_pct:6.1f}% | {sec_rec:7.1f}% | {sec_prec:7.1f}% | {lat_avg:6.2f}ms")

    print("-" * 95)
    print(f"Overall Cross-Language Group Consistency: {group_consistency_pct:.2f}% ({consistent_groups}/{total_groups} parallel scenario groups agree)")
    print("=" * 95)

    out_payload = {
        "benchmark_summary": {
            "total_cases": len(cases),
            "cross_language_group_consistency_percent": round(group_consistency_pct, 2),
            "parallel_scenario_groups": total_groups,
            "consistent_parallel_groups": consistent_groups
        },
        "language_wise_performance": summary_by_lang,
        "case_level_results": results_by_case
    }

    with open(RESULTS_OUT, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)

    print(f"[+] Multilingual benchmark results written to {RESULTS_OUT}")


if __name__ == "__main__":
    evaluate_benchmark()
