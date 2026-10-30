"""Structured Legal Element Validation Engine for LegalLens.

Enforces authentic Indian statutory element matching, distinguishing:
- Textual similarity vs. genuine statutory applicability
- Civil breach of contract (ICA 73) vs. Criminal cheating (BNS 318)
- Consumer deficiency (CPA 2(11)) vs. Excluded B2B commercial purchases (CPA 2(7))
- Voluntary transactions vs. Unauthorized electronic debits
- Lawful police instructions (MVA 119(2)) vs. Dangerous driving (MVA 184)
- Pre-July 1, 2024 IPC/CrPC offenses vs. Post-July 1, 2024 BNS/BNSS offenses

Assigns relevance classifications:
- DIRECTLY_APPLICABLE
- CONDITIONALLY_APPLICABLE
- PROCEDURAL_PROVISION
- SUPPORTING_PROVISION
- NOT_APPLICABLE
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ValidationResult:
    relevance_classification: str
    applicable_legal_elements: List[str] = field(default_factory=list)
    applicability_conditions: List[str] = field(default_factory=list)
    missing_facts: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    clarification_question: Optional[str] = None
    is_excluded: bool = False
    exclusion_reason: Optional[str] = None


HISTORICAL_TRANSITION_NOTE = (
    "Statutory Transition Notice: For offenses and transactions occurring prior to "
    "July 1, 2024, the Indian Penal Code, 1860 (IPC) and Code of Criminal Procedure, "
    "1973 (CrPC) apply pursuant to Article 20(1) of the Constitution of India and "
    "Section 358 of Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS), rather than "
    "Bharatiya Nyaya Sanhita, 2023 (BNS)."
)


def detect_historical_incident(text: str) -> Optional[str]:
    """Detect if scenario refers to an incident prior to July 1, 2024."""
    lower = text.lower()
    # Check years 19xx or 2000-2023
    year_match = re.search(r"\b(19\d{2}|20[01]\d|202[0-3])\b", lower)
    if year_match:
        return HISTORICAL_TRANSITION_NOTE
    # Check explicit phrases
    if "before july 2024" in lower or "in 2016" in lower or "in 2017" in lower or "in 2021" in lower:
        return HISTORICAL_TRANSITION_NOTE
    if re.search(r"\b(january|february|march|april|may|june)\s+2024\b", lower):
        return HISTORICAL_TRANSITION_NOTE
    return None


def evaluate_statutory_provision(
    scenario_text: str,
    domain_id: str,
    issue_id: str,
    act_id: str,
    section_id: str,
) -> ValidationResult:
    """Evaluate essential statutory ingredients for a specific provision against scenario facts."""
    s_lower = scenario_text.lower()
    act = act_id.lower()
    sec = str(section_id).lower()

    # -------------------------------------------------------------------------
    # 1. BNS 2023 Section 318 / 319 (Cheating & Personation)
    # -------------------------------------------------------------------------
    if act == "bns_2023" and sec in ("318", "319"):
        has_deception = any(w in s_lower for w in ["fraud", "scam", "cheat", "deceive", "fake", "phish", "impersonat", "tricked", "stolen", "induced", "unauthorized"])
        has_delivery = any(w in s_lower for w in ["transferred", "paid", "sent", "debited", "withdrawn", "money", "rupees", "rs", "lakhs", "amount", "otp"])
        has_commercial_breach_only = any(w in s_lower for w in ["delayed delivery", "minor delay", "invoice delayed", "contract payment late by"])

        if has_commercial_breach_only and not has_deception:
            return ValidationResult(
                relevance_classification="NOT_APPLICABLE",
                is_excluded=True,
                exclusion_reason="Mere delayed performance or contractual breach without fraudulent inducement at inception is civil, not criminal (Hridaya Ranjan Prasad Verma v. State of Bihar).",
                missing_facts=["Evidence of fraudulent intent at the time agreement was entered into"],
            )

        if has_deception and has_delivery:
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE",
                applicable_legal_elements=[
                    "Fraudulent or dishonest inducement by accused",
                    "Deception practiced upon the victim",
                    "Delivery of property or valuable security by victim",
                ],
                applicability_conditions=[
                    "Accused possessed dishonest intention at the time of making the promise",
                ],
                exceptions=[
                    "Ordinary contractual breach without inception dishonest intention does not constitute criminal cheating",
                ],
            )
        else:
            return ValidationResult(
                relevance_classification="CONDITIONALLY_APPLICABLE",
                applicable_legal_elements=["Deception", "Dishonest inducement to deliver property"],
                missing_facts=["Whether the person made false representations before money was transferred"],
                clarification_question="Did the other party make false promises or fake representations before you transferred the funds?",
            )

    # -------------------------------------------------------------------------
    # 2. BNS 2023 Section 308 / 351 (Extortion & Criminal Intimidation)
    # -------------------------------------------------------------------------
    if act == "bns_2023" and sec in ("308", "351", "352"):
        has_fear = any(w in s_lower for w in ["threat", "threatened", "blackmail", "extort", "fear", "arrest", "harm", "violence", "police custody", "video call"])
        has_demand = any(w in s_lower for w in ["pay", "money", "demand", "ransom", "transfer", "extort"])
        if has_fear and has_demand:
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE",
                applicable_legal_elements=[
                    "Intentionally putting complainant in fear of injury/reputational harm",
                    "Dishonestly inducing delivery of money under threat",
                ],
                applicability_conditions=["Threat must be intentional and induce victim into parting with money"],
            )
        elif has_fear:
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE",
                applicable_legal_elements=["Threat to cause injury to person or reputation"],
                applicability_conditions=["Section 351 applies for criminal intimidation without extortion demand"],
            )

    # -------------------------------------------------------------------------
    # 3. IT Act 2000 Section 66C & 66D (Identity Theft & Computer Personation)
    # -------------------------------------------------------------------------
    if act == "it_act_2000" and sec in ("66c", "66d"):
        has_computer = any(w in s_lower for w in ["online", "upi", "website", "link", "sms", "email", "phone", "app", "apk", "internet", "whatsapp", "telegram", "net banking", "qr", "otp"])
        has_impersonation = any(w in s_lower for w in ["fake", "caller claimed", "impersonat", "bank manager", "police", "customs", "officer", "otp", "phish"])
        if has_computer and (has_impersonation or "otp" in s_lower):
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE",
                applicable_legal_elements=[
                    "Use of communication device or computer resource",
                    "Cheating by personating another person (S. 66D)",
                    "Fraudulent use of password, OTP, or identity credential (S. 66C)",
                ],
            )
        return ValidationResult(
            relevance_classification="CONDITIONALLY_APPLICABLE",
            applicable_legal_elements=["Electronic device or computer resource involvement"],
            missing_facts=["Whether communication occurred via computer or telecom network"],
        )

    # -------------------------------------------------------------------------
    # 4. Consumer Protection Act 2019 Section 2(7) Exclusion (B2B Commercial)
    # -------------------------------------------------------------------------
    if act == "cpa_2019":
        # Check B2B commercial exclusion
        is_b2b = any(w in s_lower for w in ["registered msme", "resale", "commercial purpose", "industrial supplier", "auto components", "wholesale", "corporate manufacturer", "raw materials"])
        is_personal_livelihood = "self-employment" in s_lower or "personal livelihood" in s_lower
        if is_b2b and not is_personal_livelihood:
            return ValidationResult(
                relevance_classification="NOT_APPLICABLE",
                is_excluded=True,
                exclusion_reason="Under Section 2(7) of Consumer Protection Act 2019, goods or services purchased for resale or commercial purpose are excluded from consumer forums (Lilavati Kirtilal Mehta Medical Trust).",
                missing_facts=["Whether goods were purchased exclusively for earning livelihood through self-employment"],
            )

        # Defect vs Deficiency vs Product Liability
        if sec in ("2_10", "2_11"):
            return ValidationResult(
                relevance_classification="SUPPORTING_PROVISION",
                applicable_legal_elements=[
                    "Statutory definition of defect in goods (S. 2(10)) or deficiency in service (S. 2(11))",
                ],
            )
        if sec == "35":
            return ValidationResult(
                relevance_classification="PROCEDURAL_PROVISION",
                applicable_legal_elements=["Statutory right to institute complaint before District Consumer Commission"],
                applicability_conditions=[
                    "Complainant must be a consumer under S. 2(7)",
                    "Complaint filed within 2-year limitation period (S. 69)",
                ],
            )
        if sec in ("84", "85", "86"):
            has_injury_damage = any(w in s_lower for w in ["injury", "hurt", "harm", "exploded", "fire", "burned", "death", "damage to property"])
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE" if has_injury_damage else "CONDITIONALLY_APPLICABLE",
                applicable_legal_elements=["Product liability action against manufacturer/seller for harm caused by defective product"],
                applicability_conditions=["Harm or injury resulted directly from defect in product"],
            )

    # -------------------------------------------------------------------------
    # 5. Motor Vehicles Act 1988: Statutory Defense for Traffic Diversion
    # -------------------------------------------------------------------------
    if act == "mv_act_1988":
        # Police diversion defense to wrong-side / dangerous driving
        has_police_instruction = (
            any(w in s_lower for w in ["police directed", "police instructed", "police diversion", "constable told me", "official diversion", "traffic diversion", "cop directed"])
            or (("police" in s_lower or "constable" in s_lower or "cop" in s_lower) and any(d in s_lower for d in ["directed", "instructed", "divert", "diversion", "told me", "told us", "signaled"]))
        )
        if sec == "184" and has_police_instruction:
            return ValidationResult(
                relevance_classification="NOT_APPLICABLE",
                is_excluded=True,
                exclusion_reason="Following lawful instructions of a police officer in uniform during temporary diversion is a complete statutory defense under Section 119(2) of Motor Vehicles Act, 1988.",
                exceptions=["Section 119(2) MV Act: Driver is required to obey directions given by a police officer in uniform."],
            )
        if sec in ("119", "119_2"):
            if has_police_instruction:
                return ValidationResult(
                    relevance_classification="DIRECTLY_APPLICABLE",
                    applicable_legal_elements=["Duty to obey traffic signs subject to direction by police officer in uniform"],
                )
        if sec in ("194d", "194b", "185", "196"):
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE",
                applicable_legal_elements=["Statutory fine and disqualification penalty"],
            )
        if sec in ("129", "138", "146"):
            return ValidationResult(
                relevance_classification="SUPPORTING_PROVISION",
                applicable_legal_elements=["Substantive statutory safety mandate"],
            )
        if sec in ("139_cmvr", "130", "206"):
            return ValidationResult(
                relevance_classification="PROCEDURAL_PROVISION",
                applicable_legal_elements=["Production and seizure procedure for driving license and registration certificate"],
            )

    # -------------------------------------------------------------------------
    # 6. Workplace & Wage: Payment of Wages Act vs Code on Wages
    # -------------------------------------------------------------------------
    if act in ("payment_of_wages_act_1936", "minimum_wages_act_1948"):
        if sec in ("15", "20"):
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE",
                applicable_legal_elements=[
                    "Statutory claim for withheld wages or unauthorized deductions before Authority",
                ],
                applicability_conditions=["Claim filed within 12 months (or reasonable cause shown)"],
            )
        if sec in ("5", "7", "12"):
            return ValidationResult(
                relevance_classification="SUPPORTING_PROVISION",
                applicable_legal_elements=["Statutory wage payment timeline and permissible deduction rules"],
            )

    # -------------------------------------------------------------------------
    # 7. Contract Act 1872: Section 27 (Non-Compete Restraint of Trade Void)
    # -------------------------------------------------------------------------
    if act == "contract_act_1872" and sec == "27":
        has_non_compete = any(w in s_lower for w in ["non-compete", "non compete", "liquidated damages", "leaving job", "competitor", "restraint of trade"])
        if has_non_compete:
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE",
                applicable_legal_elements=[
                    "Agreement in restraint of lawful profession, trade, or business is void ab initio",
                    "Post-employment non-compete covenants are completely unenforceable in India (Percept D'Mark v. Zaheer Khan)",
                ],
                exceptions=["Sale of goodwill of a business (sole statutory exception)"],
            )

    # -------------------------------------------------------------------------
    # 8. NI Act 1881: Section 138 (Cheque Bounce)
    # -------------------------------------------------------------------------
    if act == "ni_act_1881" and sec == "138":
        has_cheque = "cheque" in s_lower or "check" in s_lower
        has_bounce = any(w in s_lower for w in ["bounced", "dishonoured", "insufficient funds", "returned unpaid"])
        if has_cheque and has_bounce:
            return ValidationResult(
                relevance_classification="DIRECTLY_APPLICABLE",
                applicable_legal_elements=[
                    "Cheque drawn for discharge of legally enforceable debt or liability",
                    "Dishonour by bank for insufficiency of funds or exceeds arrangement",
                ],
                applicability_conditions=[
                    "Cheque presented within 3 months of date of issuance",
                    "Statutory demand notice sent in writing within 30 days of receipt of return memo (S. 142)",
                    "Drawer failed to pay within 15 days of receipt of notice",
                ],
                missing_facts=["Whether written demand notice was served within 30 days of the bank return memo"],
            )

    # Default fallback
    return ValidationResult(
        relevance_classification="DIRECTLY_APPLICABLE",
        applicable_legal_elements=["Statutory compliance with relevant legal rule"],
    )
