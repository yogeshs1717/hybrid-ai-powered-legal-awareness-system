"""Scenario Validator — Evaluates whether user input describes a recognized legal scenario.

Distinguishes between genuine citizen legal queries (in the five approved domains:
Cyber Fraud, Consumer Issues, Traffic Enforcement, Workplace / Wage, Contractual Disputes)
and unknown, non-legal inputs (such as conversational chit-chat, random sentences,
everyday non-legal chatter, gibberish, or unsupported out-of-scope topics).

When an unknown or non-legal scenario is detected, the system safely routes to an
informative fallback state advising the user to enter a valid legal scenario, rather
than hallucinating a random legal domain and statutory provisions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Set, Tuple

from app.classifier import DomainPrediction
from app.issue_detector import IssueDetection

FALLBACK_MESSAGE = (
    "We could not identify a valid legal scenario or dispute from your description. "
    "Please enter a specific legal situation (such as cyber fraud, unauthorized debits, "
    "defective products, consumer complaints, traffic challans, unpaid salary, or breach of contract) "
    "with clear details about what happened so we can identify the applicable laws and action steps."
)

# Domain-specific legal tokens (stems and core keywords)
DOMAIN_SPECIFIC_KEYWORDS = {
    "cyber_fraud": {
        "bank", "account", "money", "upi", "otp", "pin", "debit", "debited", "credit", "card",
        "transfer", "transferred", "wallet", "scam", "scammer", "fraud", "fraudster", "hacked",
        "hacking", "phishing", "apk", "link", "malware", "caller", "ransom", "telegram", "investment",
        "crypto", "loan", "impersonat", "impersonation", "blackmail", "blackmailed", "extortion",
        "profile", "transaction", "withdrawn", "withdrawal", "stolen", "sim", "kyc", "biometric",
        "aadhaar", "pan", "identity", "cyber", "password", "app", "online", "device", "remotely",
        "unauthorized", "unauthorised", "digital", "arrest", "customs", "cbi", "fedex", "courier",
        "parcel", "fastag", "aeps", "clone", "cloned", "voice", "emergency", "wedding", "reward",
        "points", "redeem", "victim", "cheated", "trafficking", "stalkerware", "spyware", "nobroker",
        "rental", "pg", "hostel", "listing", "accommodation", "duped", "fake listing"
    },
    "consumer_issues": {
        "buy", "bought", "purchase", "purchased", "product", "item", "order", "ordered", "shop",
        "store", "seller", "amazon", "flipkart", "delivery", "delivered", "courier", "defective",
        "defect", "damaged", "broken", "refund", "refunded", "replacement", "replaced", "return",
        "returned", "warranty", "guarantee", "bill", "billing", "receipt", "invoice", "charged",
        "charge", "overcharged", "mrp", "food", "restaurant", "meal", "expired", "spurious",
        "fake", "counterfeit", "cinema", "airline", "flight", "cancelled", "cancellation", "ticket",
        "service", "technician", "goods", "dealer", "dealership", "e-commerce", "ecommerce",
        "appliance", "repair", "refrigerator", "phone", "laptop", "television", "tv", "washing",
        "coaching", "tuition", "fee", "fees", "institute", "admission", "display", "screen",
        "adulterated", "contamination", "poisoning", "boarding", "delay", "builder", "flat",
        "possession", "apartment", "real estate", "hospital", "medical", "doctor", "negligence",
        "dark pattern", "drip", "hidden charge", "service charge", "dishonored", "tpa",
        "repudiation", "repudiated", "pre-existing", "cashless", "airsewa", "passenger",
        "baggage", "voucher", "dgca", "insurance", "claim", "telecom", "operator", "prepaid",
        "postpaid", "connection", "broadband", "fiber", "fibre", "outage", "streaming", "ott",
        "subscription", "auto-debit", "geyser", "microwave", "oven", "odometer", "tampered",
        "second-hand", "used car", "exploded", "wiring", "burns"
    },
    "traffic_enforcement": {
        "traffic", "challan", "challans", "echallan", "fine", "fined", "fines", "fining", "penalty",
        "penalties", "penalized", "rto", "license", "licence", "dl", "rc", "vehicle", "car", "bike",
        "motorcycle", "scooter", "helmet", "signal", "red light", "amber", "camera", "radar",
        "speed", "speeding", "overspeeding", "parking", "towed", "towing", "impound", "impounded",
        "seized", "seizure", "drink", "drunk", "breathalyzer", "alcohol", "puc", "pucc", "pollution",
        "hsrp", "number plate", "plate", "tint", "tinted", "mparivahan", "digilocker", "seatbelt",
        "cop", "constable", "officer", "memo", "ambulance", "emergency vehicle", "insurance",
        "uninsured", "policy", "vahan", "exhaust", "silencer", "overloading", "weighbridge",
        "permit", "transport", "confiscate", "confiscated", "key", "keys", "snatched",
        "diversion", "diversions", "barricade", "barricades", "metro", "construction",
        "opposite", "wrong-side", "wrong side", "solatium", "mact", "accident", "crash",
        "collision", "hit-and-run", "hit and run", "runaway", "pedestrian", "rash", "triple",
        "pillion", "passengers", "two-wheeler", "rider", "adult"
    },
    "workplace_wage": {
        "salary", "salaries", "wage", "wages", "pay", "paid", "unpaid", "employer", "employee",
        "company", "boss", "office", "job", "work", "worked", "working", "hours", "shift",
        "overtime", "deduction", "deducted", "deductions", "pf", "provident", "epf", "epfo",
        "uan", "gratuity", "bonus", "notice", "notice period", "fired", "terminate", "terminated",
        "termination", "resign", "resigned", "resignation", "settlement", "clearance", "leave",
        "maternity", "pregnancy", "pregnant", "contractor", "worker", "allowance", "staff",
        "severance", "employment", "reminders", "payslip", "payslips", "muster", "arrears",
        "withheld", "withholding", "intern", "internship", "stipend", "trainee", "bond",
        "certificate", "relieving", "experience letter", "bench", "layoff", "retrenchment",
        "posh", "harassment", "sexual", "vulgar", "lewd", "committee", "clawback", "basic pay",
        "remittance", "non-deposit"
    },
    "contractual_disputes": {
        "contract", "contracts", "contractual", "agreement", "agreements", "agreed", "advance",
        "deposit", "security deposit", "tenant", "landlord", "rent", "rented", "lease", "leased",
        "deed", "sign", "signed", "signing", "breach", "breached", "default", "defaulted",
        "defaulter", "supplier", "vendor", "client", "buyer", "msme", "payment", "unpaid", "pending",
        "outstanding", "commercial", "wholesale", "supply", "builder", "possession", "flat", "property",
        "premises", "partnership", "terms", "abandoned", "abandoning", "renovation", "interior",
        "token", "invoice", "freelance", "freelancer", "non-compete", "nda", "duress", "coercion",
        "misrepresentation", "indemnity", "forfeited", "forfeiture", "bailment", "valet",
        "substituted performance", "specific performance", "injunction", "deliverables", "materials",
        "cheque", "cheques", "bounced", "bounce", "dishonoured", "dishonor", "dishonour",
        "memo", "funds insufficient", "insufficient funds", "vacating", "vacated", "painting",
        "wear and tear", "eviction", "milestone", "extension", "franchise", "franchisee",
        "franchisor", "partner", "stop payment", "stop-payment", "waived", "waiver", "sale deed",
        "conveyance"
    },
}

ALL_LEGAL_KEYWORDS: Set[str] = set().union(*DOMAIN_SPECIFIC_KEYWORDS.values()) | {
    "cheat", "cheated", "cheating", "illegal", "unlawful", "violate", "violated", "violation",
    "complain", "complaint", "dispute", "disputed", "refused", "refusal", "harassment",
    "compensation", "damages", "sue", "court", "unauthorized", "unauthorised", "withheld",
    "withholding", "harass", "extort", "extortion", "threaten", "threatened", "stole", "stolen",
    "theft", "loss", "police", "bribe", "investigate", "law", "rights", "legal", "notice",
    "reminders", "recovery", "fraud", "scam", "penalty", "due", "dues"
}

# Indic keywords and stems (Kannada & Hindi) for validating non-English legal queries
INDIC_LEGAL_KEYWORDS: Set[str] = {
    # Kannada legal core terms
    "ಬ್ಯಾಂಕ್", "ಖಾತೆ", "ಖಾತೆಯಿಂದ", "ಹಣ", "ದುಡ್ಡು", "ದೂರು", "ವಂಚನೆ", "ಸಂಬಳ", "ವೇತನ", "ಚಲನ್", "ಪೊಲೀಸ್",
    "ಗ್ರಾಹಕ", "ಬಾಡಿಗೆ", "ಕರಾರು", "ಒಪ್ಪಂದ", "ಚೆಕ್", "ದೋಷ", "ಖರೀದಿ", "ಖರೀದಿಸಿದೆ", "ಕೊಂಡುಕೊಂಡೆ", "ಉತ್ಪನ್ನ",
    "ವಸ್ತು", "ಅಡ್ವಾನ್ಸ್", "ಠೇವಣಿ", "ಲಂಚ", "ಕಿರುಕುಳ", "ಕೆಲಸ", "ಕಂಪನಿ", "ಪಾರ್ಸೆಲ್", "ಆಸ್ಪತ್ರೆ", "ವೈದ್ಯ",
    "ಇಂಜೆಕ್ಷನ್", "ಆನ್‌ಲೈನ್", "ಕೊಟ್ಟಿಲ್ಲ", "ತಡೆದು", "ಹಾಕಿದ್ದಾರೆ", "ವಂಚಿಸಿದ್ದಾರೆ", "ಕಡಿತ", "ಓಟಿಪಿ", "ಬೌನ್ಸ್",
    # Hindi legal core terms
    "बैंक", "खाता", "खाते", "पैसे", "रुपये", "शिकायत", "धोखाधड़ी", "धोखा", "वेतन", "तनख्वाह", "सैलरी",
    "चालान", "पुलिस", "उपभोक्ता", "ग्राहक", "किराया", "अनुबंध", "समझौता", "चेक", "खराबी", "खराब", "खरीद",
    "सामान", "उत्पाद", "सिक्योरिटी", "डिपॉजिट", "रिश्वत", "उत्पीड़न", "नौकरी", "कंपनी", "पार्सल", "अस्पताल",
    "डॉक्टर", "ऑनलाइन", "रिफंड", "वारंटी", "जुर्माना"
}

LEGAL_ROOT_STEMS = (
    "fine", "penalt", "challan", "insur", "polic", "vehicl", "licen", "wage", "salar",
    "deduct", "pay", "fraud", "scam", "cheat", "theft", "stolen", "breach", "contract",
    "agree", "refund", "defect", "terminat", "resign", "withheld", "deposit", "landlord",
    "tenant", "employ", "overtime", "gratuity", "provident", "matern", "extort", "blackmail",
    "hacked", "phish", "deliver", "purchas", "order", "warant", "guarant", "towed", "seiz",
    "bounc", "chequ", "divers", "accid", "posh", "harass", "mact", "claim"
)

CASUAL_PREFIXES = [
    r"^(hi|hello|hey|good morning|good evening|good afternoon)\b",
    r"^(how are you|what are you doing|tell me a joke|write a poem|sing a song)\b",
    r"^(what is the capital|recipe for|how to cook|weather in|how do i learn)\b",
    r"^(my favorite|i like|i love watching|i need a recipe|can you)\b",
]


@dataclass(frozen=True)
class ScenarioEvaluation:
    """Outcome of validating user scenario text."""
    is_valid: bool
    fallback_message: Optional[str]
    reason: str
    effective_issue: Optional[IssueDetection]


def evaluate_scenario(
    scenario_text: str,
    domain_prediction: DomainPrediction,
    issue_detection: Optional[IssueDetection],
) -> ScenarioEvaluation:
    """Evaluates whether scenario_text is a recognized legal scenario within scope.

    Returns ScenarioEvaluation with is_valid=True for valid legal scenarios,
    or is_valid=False with fallback_message for unknown/non-legal text.
    """
    from app.multilingual import detect_language_and_script
    lang_info = detect_language_and_script(scenario_text)
    eval_text = lang_info.canonical_text.lower().strip()

    text_lower = scenario_text.lower().strip()
    tokens = set(re.findall(r"[a-z]{3,}", eval_text))
    stemmed_matches = {t for t in tokens if any(t.startswith(s) for s in LEGAL_ROOT_STEMS)}
    indic_matches = {w for w in INDIC_LEGAL_KEYWORDS if w in text_lower}
    matched_legal = (tokens & ALL_LEGAL_KEYWORDS) | stemmed_matches | indic_matches

    sim = issue_detection.similarity_score if issue_detection else 0.0
    signals = issue_detection.scenario_signals if issue_detection else []

    # 1. Spurious single-token noise filtering:
    # If prototype similarity is low (< 0.25) and overlap is <= 1 signal, verify that
    # the signal is a genuine legal keyword. If not, treat issue as spurious.
    is_spurious_issue = False
    if issue_detection is not None:
        if sim < 0.25 and len(signals) <= 1:
            if not signals or not any(s in ALL_LEGAL_KEYWORDS for s in signals):
                is_spurious_issue = True

    effective_issue = None if is_spurious_issue else issue_detection
    effective_sim = effective_issue.similarity_score if effective_issue else 0.0

    # 2. Check casual conversational greetings / prompts
    is_casual_prefix = any(re.search(p, text_lower) for p in CASUAL_PREFIXES)
    if is_casual_prefix and len(matched_legal) < 2:
        return ScenarioEvaluation(
            is_valid=False,
            fallback_message=FALLBACK_MESSAGE,
            reason="conversational_or_general_query",
            effective_issue=effective_issue,
        )

    # 3. Complete absence of any legal concepts across all 5 domains
    if len(matched_legal) == 0:
        return ScenarioEvaluation(
            is_valid=False,
            fallback_message=FALLBACK_MESSAGE,
            reason="no_legal_concepts_detected",
            effective_issue=effective_issue,
        )

    # 4. Out-of-scope check when no issue was matched
    if effective_issue is None:
        dom_keywords = DOMAIN_SPECIFIC_KEYWORDS.get(domain_prediction.domain_id, set())
        has_dom_signal = any(t in dom_keywords for t in tokens)
        # If no keywords match the predicted domain, model picked it arbitrarily
        if not has_dom_signal:
            return ScenarioEvaluation(
                is_valid=False,
                fallback_message=FALLBACK_MESSAGE,
                reason="out_of_scope_unsupported_domain",
                effective_issue=effective_issue,
            )
        # If domain confidence is very low (< 0.42) and matched legal concepts < 2
        if domain_prediction.confidence < 0.42 and len(matched_legal) < 2:
            return ScenarioEvaluation(
                is_valid=False,
                fallback_message=FALLBACK_MESSAGE,
                reason="insufficient_legal_signals",
                effective_issue=effective_issue,
            )

    # 5. Low confidence and low issue similarity
    if (
        domain_prediction.confidence < 0.40
        and effective_sim < 0.22
        and len(matched_legal) < 2
    ):
        return ScenarioEvaluation(
            is_valid=False,
            fallback_message=FALLBACK_MESSAGE,
            reason="insufficient_confidence_and_similarity",
            effective_issue=effective_issue,
        )

    return ScenarioEvaluation(
        is_valid=True,
        fallback_message=None,
        reason="valid_legal_scenario",
        effective_issue=effective_issue,
    )
