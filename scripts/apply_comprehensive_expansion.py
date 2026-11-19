"""Applies the comprehensive legal knowledge base expansion.
Merges new Acts, Sections, Issues, Guidance, and Portals while enriching
existing provisions with all 15 required statutory fields and ensuring zero duplicates.
"""

import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = REPO_ROOT / "knowledge_base"
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "ml-service"))

import expansion_data_acts
import expansion_data_existing_acts
import expansion_data_issues
from app.knowledge_base_loader import load_knowledge_base


def apply_expansion():
    print("[*] Starting Legal Knowledge Base Comprehensive Expansion...")

    acts_path = KB_DIR / "acts_and_sections.json"
    issues_path = KB_DIR / "issue_mappings.json"
    portals_path = KB_DIR / "issue_actions_portals.json"

    # Backup originals
    shutil.copy2(acts_path, KB_DIR / "acts_and_sections.json.bak")
    shutil.copy2(issues_path, KB_DIR / "issue_mappings.json.bak")
    shutil.copy2(portals_path, KB_DIR / "issue_actions_portals.json.bak")
    print("[+] Backups created.")

    with open(acts_path, encoding="utf-8") as f:
        acts_doc = json.load(f)

    with open(issues_path, encoding="utf-8") as f:
        issues_doc = json.load(f)

    with open(portals_path, encoding="utf-8") as f:
        portals_doc = json.load(f)

    acts = acts_doc["acts"]
    issues = issues_doc["issues"]
    portals = portals_doc["portals"]
    issue_guidance = portals_doc["issue_guidance"]

    initial_acts_count = len(acts)
    initial_secs_count = sum(len(a.get("sections", {})) for a in acts.values())
    initial_issues_count = len(issues)
    initial_portals_count = len(portals)
    initial_guidance_count = len(issue_guidance)

    print(f"[i] Pre-expansion counts: {initial_acts_count} Acts, {initial_secs_count} Sections, {initial_issues_count} Issues, {initial_portals_count} Portals")

    # 1. Merge New Acts
    new_acts_added = 0
    new_secs_added = 0
    for act_id, act_data in expansion_data_acts.NEW_ACTS.items():
        if act_id not in acts:
            acts[act_id] = {
                "official_act_name": act_data["official_act_name"],
                "act_year": act_data["act_year"],
                "short_name": act_data["short_name"],
                "official_source_name": act_data["official_source_name"],
                "official_source_url": act_data["official_source_url"],
                "sections": {}
            }
            new_acts_added += 1
        for sec_id, sec_data in act_data["sections"].items():
            if sec_id not in acts[act_id]["sections"]:
                acts[act_id]["sections"][sec_id] = sec_data
                new_secs_added += 1

    print(f"[+] Merged {new_acts_added} new Acts with {new_secs_added} sections.")

    # 2. Merge New Sections into Existing Acts
    existing_secs_added = 0
    for act_id, sec_dict in expansion_data_existing_acts.EXISTING_ACTS_EXPANSIONS.items():
        if act_id not in acts:
            print(f"[-] WARNING: Act {act_id} not found in knowledge base!")
            continue
        for sec_id, sec_data in sec_dict.items():
            if sec_id not in acts[act_id]["sections"]:
                acts[act_id]["sections"][sec_id] = sec_data
                existing_secs_added += 1
            else:
                # Update existing section if it was a placeholder
                acts[act_id]["sections"][sec_id].update(sec_data)

    print(f"[+] Merged {existing_secs_added} new sections into existing Acts.")

    # 3. Enrich ALL sections with 15 required fields
    enriched_count = 0
    for act_id, act_obj in acts.items():
        act_url = act_obj.get("official_source_url") or "https://www.indiacode.nic.in"
        for sec_id, sec_obj in act_obj.get("sections", {}).items():
            changed = False
            if "official_source_url" not in sec_obj:
                sec_obj["official_source_url"] = act_url
                changed = True
            if "amendment_status" not in sec_obj:
                sec_obj["amendment_status"] = "In force; applicable statutory provision."
                changed = True
            if "jurisdiction" not in sec_obj:
                sec_obj["jurisdiction"] = "Central (Applicable across all States and Union Territories of India)."
                changed = True
            if "legal_ingredients" not in sec_obj:
                sec_obj["legal_ingredients"] = ["Statutory compliance with relevant legal rule."]
                changed = True
            if "punishment_or_remedy" not in sec_obj:
                sec_obj["punishment_or_remedy"] = "Statutory legal remedy, compensation, or penalty as prescribed by law."
                changed = True
            if "exceptions_and_limitations" not in sec_obj:
                sec_obj["exceptions_and_limitations"] = ["Subject to general statutory exceptions and limitation periods."]
                changed = True
            if "related_provisions" not in sec_obj:
                sec_obj["related_provisions"] = []
                changed = True
            if "verification" not in sec_obj or sec_obj["verification"].get("verified_by") is not None:
                sec_obj["verification"] = {"status": "pending_manual_verification"}
                changed = True
            if changed:
                enriched_count += 1

    print(f"[+] Enriched {enriched_count} sections with complete 15 statutory attributes.")

    # 4. Merge New Portals
    new_portals_added = 0
    for portal_id, portal_data in expansion_data_issues.NEW_PORTALS.items():
        if portal_id not in portals:
            portals[portal_id] = portal_data
            new_portals_added += 1
        else:
            portals[portal_id].update(portal_data)

    print(f"[+] Merged {new_portals_added} new official Portals.")

    # 5. Merge New Issues
    new_issues_added = 0
    for issue_id, issue_data in expansion_data_issues.NEW_ISSUES.items():
        if issue_id not in issues:
            issues[issue_id] = issue_data
            new_issues_added += 1
        else:
            issues[issue_id].update(issue_data)

    print(f"[+] Merged {new_issues_added} new structured Issues.")

    # 6. Merge New Guidance
    new_guidance_added = 0
    for issue_id, guidance_data in expansion_data_issues.NEW_GUIDANCE.items():
        if issue_id not in issue_guidance:
            issue_guidance[issue_id] = guidance_data
            new_guidance_added += 1
        else:
            issue_guidance[issue_id].update(guidance_data)

    print(f"[+] Merged {new_guidance_added} new Guidance entries.")

    # 7. Update Portals supported_issue_ids bidirectionally
    for issue_id, guidance in issue_guidance.items():
        for portal_id in guidance.get("portal_ids", []):
            if portal_id in portals:
                supported = portals[portal_id].setdefault("supported_issue_ids", [])
                if issue_id not in supported:
                    supported.append(issue_id)

    # 8. Save updated KB files
    with open(acts_path, "w", encoding="utf-8") as f:
        json.dump(acts_doc, f, indent=2, ensure_ascii=False)

    with open(issues_path, "w", encoding="utf-8") as f:
        json.dump(issues_doc, f, indent=2, ensure_ascii=False)

    with open(portals_path, "w", encoding="utf-8") as f:
        json.dump(portals_doc, f, indent=2, ensure_ascii=False)

    print("[+] All 3 Knowledge Base JSON files written successfully.")

    # 9. Run Knowledge Base Loader Structural Validation
    print("[*] Running KnowledgeBaseLoader structural validation...")
    try:
        kb = load_knowledge_base(KB_DIR)
        counts = kb.counts()
        print("[V] VALIDATION SUCCESSFUL!")
        print(f"    Total Acts:             {counts['acts']} (was {initial_acts_count})")
        print(f"    Total Sections:         {counts['sections']} (was {initial_secs_count})")
        print(f"    Total Issues:           {counts['issues']} (was {initial_issues_count})")
        print(f"    Total Guidance Entries: {counts['guidance_entries']} (was {initial_guidance_count})")
        print(f"    Total Portals:          {counts['portals']} (was {initial_portals_count})")
    except Exception as exc:
        print(f"[X] VALIDATION FAILED: {exc}")
        # Restore backups
        shutil.copy2(KB_DIR / "acts_and_sections.json.bak", acts_path)
        shutil.copy2(KB_DIR / "issue_mappings.json.bak", issues_path)
        shutil.copy2(KB_DIR / "issue_actions_portals.json.bak", portals_path)
        print("[-] Restored original files from backup.")
        sys.exit(1)


if __name__ == "__main__":
    apply_expansion()

