"""Script to expand training data for LegalLens to improve classification accuracy.

Ensures every one of the 214 legal issues has at least 11-12 authentic, diverse
citizen scenario rows in ml-service/data/training_data_v2.csv.
"""

from __future__ import annotations

import csv
import json
import random
from collections import Counter
from pathlib import Path

random.seed(42)

KB_PATH = Path("knowledge_base/issue_mappings.json")
TRAIN_PATH = Path("ml-service/data/training_data_v2.csv")

# Scenario templates and contextual variation builders per domain
LOCATIONS = [
    "in Bengaluru", "in Mumbai", "in Delhi NCR", "in Hyderabad", "in Chennai",
    "in Pune", "in Kolkata", "in Ahmedabad", "in Jaipur", "in Lucknow",
    "in Chandigarh", "in Indore", "in Kochi", "in Surat", "in Nagpur"
]

AMOUNTS = [
    "Rs 12,000", "Rs 25,000", "Rs 45,000", "Rs 80,000", "Rs 1.5 lakhs",
    "Rs 2.8 lakhs", "Rs 50,000", "Rs 35,000", "Rs 90,000", "Rs 4 lakhs"
]

PLATFORMS = {
    "cyber_fraud": ["Google Pay", "PhonePe", "Paytm", "BHIM UPI", "NetBanking portal", "credit card", "mobile banking app", "YONO app"],
    "consumer_issues": ["Amazon India", "Flipkart", "e-commerce marketplace", "local retail outlet", "authorized dealership", "electronics store"],
    "traffic_enforcement": ["traffic junction", "outer ring road", "highway toll plaza", "signal crossing", "metro construction zone"],
    "workplace_wage": ["IT services firm", "manufacturing unit", "private company", "startup", "commercial establishment", "consulting agency"],
    "contractual_disputes": ["commercial partnership", "registered vendor contract", "tenancy lease", "service level agreement", "supply agreement"]
}


def load_existing():
    rows = []
    with open(TRAIN_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def generate_variations_for_issue(issue: dict, needed: int) -> list[str]:
    """Generate realistic, domain-specific citizen scenarios for an issue."""
    iid = issue["issue_id"]
    did = issue["domain_id"]
    dname = issue.get("display_name") or issue.get("canonical_name") or iid.replace("_", " ").title()
    idef = issue.get("issue_definition") or dname
    protos = issue.get("prototype_texts", [])
    
    variations = []
    
    # Prefix structures
    starters = [
        "I need immediate legal guidance regarding an incident where",
        "Citizen complaint:",
        "Last week,",
        "Yesterday morning,",
        "A few days ago,",
        "We are facing a serious dispute because",
        "My problem is that",
        "I was recently subjected to an issue where",
        "Filing a formal grievance regarding",
        "How do I take legal action after",
        "Please help me understand my legal rights because",
        "I am a victim of an incident where",
        "An incident occurred recently where",
        "Urgent assistance needed:",
        "Reporting an unlawful practice where"
    ]
    
    for i in range(needed):
        starter = starters[i % len(starters)]
        loc = LOCATIONS[i % len(LOCATIONS)]
        amt = AMOUNTS[i % len(AMOUNTS)]
        plat = PLATFORMS[did][i % len(PLATFORMS[did])]
        base_proto = protos[i % len(protos)] if protos else idef
        
        # Style variation 1: First-person narrative focusing on the factual harm
        if i % 4 == 0:
            sc = f"{starter} {base_proto.lower().rstrip('.')} {loc}, causing a direct loss of {amt}."
        # Style variation 2: Transactional narrative with platform/institution context
        elif i % 4 == 1:
            sc = f"While using {plat} {loc}, {idef.lower().rstrip('.')}. The other party took {amt} and refuses to respond or rectify the situation."
        # Style variation 3: Formal grievance describing the specific violation
        elif i % 4 == 2:
            sc = f"{starter} {dname.lower()} occurred involving {amt}. Specifically, {base_proto.rstrip('.')} despite repeated written reminders."
        # Style variation 4: Direct, conversational citizen voice
        else:
            sc = f"{base_proto.rstrip('.')} {loc} involving a disputed sum of {amt} via {plat}, and I want to know the legal sections and procedure to file a complaint."
        
        # Clean up double periods or duplicate spaces
        sc = " ".join(sc.split()).replace("..", ".").strip()
        variations.append(sc)
        
    return variations


def main():
    with open(KB_PATH, encoding="utf-8") as f:
        kb_data = json.load(f)
    issues = kb_data["issues"]
    
    existing_rows = load_existing()
    existing_counts = Counter(r["issue_id"] for r in existing_rows)
    existing_scenarios = set(r["scenario"].strip().lower() for r in existing_rows)
    
    print(f"Loaded {len(existing_rows)} existing rows across {len(existing_counts)} issues.")
    
    TARGET_PER_ISSUE = 11
    new_rows = []
    
    for iid, issue in issues.items():
        did = issue["domain_id"]
        cur_count = existing_counts.get(iid, 0)
        needed = max(0, TARGET_PER_ISSUE - cur_count)
        
        if needed > 0:
            generated = generate_variations_for_issue(issue, needed)
            for sc in generated:
                if sc.strip().lower() not in existing_scenarios:
                    existing_scenarios.add(sc.strip().lower())
                    new_rows.append({
                        "scenario": sc,
                        "domain": did,
                        "issue_id": iid
                    })
    
    print(f"Generated {len(new_rows)} new high-quality training rows.")
    all_rows = existing_rows + new_rows
    print(f"Total dataset will have {len(all_rows)} rows.")
    
    # Write back to training_data_v2.csv
    fieldnames = ["scenario", "domain", "issue_id"]
    with open(TRAIN_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
        
    print(f"Successfully saved expanded dataset to {TRAIN_PATH}")
    
    # Check new domain distribution
    final_domain_counts = Counter(r["domain"] for r in all_rows)
    print("New domain distribution:", dict(final_domain_counts))


if __name__ == "__main__":
    main()
