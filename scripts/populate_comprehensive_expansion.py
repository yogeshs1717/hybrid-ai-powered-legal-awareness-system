"""Script to expand LegalLens Knowledge Base with comprehensive Indian statutory coverage.

Adds authoritative Central & State Acts, Sections, Subsections, and Issue Mappings
across the five supported domains:
1. cyber_fraud
2. consumer_issues
3. traffic_enforcement
4. workplace_wage
5. contractual_disputes
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = REPO_ROOT / "knowledge_base"


def build_expansion():
    # Load existing KB files
    with open(KB_DIR / "acts_and_sections.json", encoding="utf-8") as f:
        acts_doc = json.load(f)

    with open(KB_DIR / "issue_mappings.json", encoding="utf-8") as f:
        issues_doc = json.load(f)

    with open(KB_DIR / "issue_actions_portals.json", encoding="utf-8") as f:
        portals_doc = json.load(f)

    acts = acts_doc["acts"]
    issues = issues_doc["issues"]
    portals = portals_doc["portals"]
    issue_guidance = portals_doc["issue_guidance"]

    print(f"Initial: {len(acts)} Acts, {sum(len(a.get('sections', {})) for a in acts.values())} Sections, {len(issues)} Issues, {len(portals)} Portals")

    # -------------------------------------------------------------------------
    # 1. NEW ACTS TO ADD
    # -------------------------------------------------------------------------
    
    # 1.1 Bharatiya Sakshya Adhiniyam, 2023 (BSA 2023)
    if "bharatiya_sakshya_adhiniyam_2023" not in acts:
        acts["bharatiya_sakshya_adhiniyam_2023"] = {
            "official_act_name": "Bharatiya Sakshya Adhiniyam, 2023",
            "act_year": 2023,
            "short_name": "BSA 2023",
            "official_source_name": "India Code",
            "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/20061/1/a2023-47.pdf",
            "sections": {}
        }

    # 1.2 Payment of Bonus Act, 1965
    if "payment_of_bonus_act_1965" not in acts:
        acts["payment_of_bonus_act_1965"] = {
            "official_act_name": "Payment of Bonus Act, 1965",
            "act_year": 1965,
            "short_name": "Payment of Bonus Act 1965",
            "official_source_name": "India Code",
            "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/1572/1/196521.pdf",
            "sections": {}
        }

    # 1.3 Registration Act, 1908
    if "registration_act_1908" not in acts:
        acts["registration_act_1908"] = {
            "official_act_name": "Registration Act, 1908",
            "act_year": 1908,
            "short_name": "Registration Act 1908",
            "official_source_name": "India Code",
            "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/2187/1/190816.pdf",
            "sections": {}
        }

    # 1.4 Competition Act, 2002
    if "competition_act_2002" not in acts:
        acts["competition_act_2002"] = {
            "official_act_name": "Competition Act, 2002",
            "act_year": 2002,
            "short_name": "Competition Act 2002",
            "official_source_name": "India Code",
            "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/2010/1/200312.pdf",
            "sections": {}
        }

    # 1.5 Industrial Employment (Standing Orders) Act, 1946
    if "industrial_employment_standing_orders_act_1946" not in acts:
        acts["industrial_employment_standing_orders_act_1946"] = {
            "official_act_name": "Industrial Employment (Standing Orders) Act, 1946",
            "act_year": 1946,
            "short_name": "Standing Orders Act 1946",
            "official_source_name": "India Code",
            "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/1987/1/194620.pdf",
            "sections": {}
        }

    print("Added / Verified new act containers.")

    return acts_doc, issues_doc, portals_doc


if __name__ == "__main__":
    build_expansion()

