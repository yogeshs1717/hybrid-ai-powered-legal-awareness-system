"""Multilingual NLP Module for LegalLens.

Provides comprehensive support for:
- English (Latin script)
- Kannada (Kannada script & Romanized Kanglish)
- Hindi (Devanagari script & Romanized Hinglish)
- Code-mixed Indian English / Kannada / Hindi (kn-en, hi-en)

Capabilities:
1. Script detection (Latin, Kannada, Devanagari, Mixed)
2. Language identification with confidence & code-mixing flag
3. Unicode text normalization (NFKC, zero-width stripping, Indic diacritics)
4. Domain-specific legal terminology canonicalization / glossing
5. Multilingual prototype alignment for deterministic semantic retrieval
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass(frozen=True)
class LanguageInfo:
    """Multilingual metadata for input scenarios."""
    detected_language: str        # 'en', 'kn', 'hi', 'kn-Latn', 'hi-Latn', 'kn-en', 'hi-en', 'unknown'
    language_confidence: float    # 0.0 to 1.0
    detected_script: str          # 'Latin', 'Kannada', 'Devanagari', 'Mixed'
    is_code_mixed: bool
    normalized_text: str
    canonical_text: str           # Original text enriched with canonical legal tokens for retrieval


# -----------------------------------------------------------------------------
# 1. Indic Script Ranges & Clean Markers (Strictly Indic Words Only)
# -----------------------------------------------------------------------------
KANNADA_RANGE = re.compile(r"[\u0C80-\u0CFF]")
DEVANAGARI_RANGE = re.compile(r"[\u0900-\u097F]")
LATIN_RANGE = re.compile(r"[a-zA-Z]")

# High-frequency Romanized Kannada (Kanglish) function words & markers (Strictly Kannada words)
KANGLISH_MARKERS: Set[str] = {
    "nanna", "namma", "nimage", "nanage", "inda", "duddu", "hana", "aagide", "agide",
    "aagidru", "agidru", "aagi", "agi", "madiddare", "madidare", "madidru", "madidre",
    "illade", "illa", "hathira", "kotidare", "kottidare", "agalla", "beku", "yaru", "yaaro",
    "hege", "anthara", "anthare", "kattidde", "sambala", "gadi", "khate", "vanchane",
    "badige", "thevani", "oppanda", "salaha", "danda", "apaghatha", "kelasa", "salvagi",
    "ondhu", "eradu", "idhe", "iro", "madodu", "kaddidare", "torsidru", "kanstide",
    "haakiddare", "haakidde", "madtilla", "kottilla", "tagondidde", "hogidde", "madbeku",
    "kodtilla", "kodalla", "madalla", "kooda", "nalli", "kedi", "helidru", "heli", "thago"
}

# High-frequency Romanized Hindi (Hinglish) function words & markers (Strictly Hindi words)
HINGLISH_MARKERS: Set[str] = {
    "mera", "mere", "meri", "mujhe", "mujhse", "humara", "apna", "apne", "bina", "paise",
    "rupaye", "kat", "gaye", "gaya", "gayi", "diya", "diye", "kiye", "kiya", "nahi", "nahin",
    "hua", "hui", "hue", "hai", "hain", "tha", "thi", "kisi", "usne", "unhone", "isko",
    "dhokha", "dhokhadhadi", "tankhwah", "vetan", "gaadi", "chori", "chalann", "jurmana",
    "apradh", "kiraya", "samjhauta", "anubandh", "grahak", "kharab", "shikayat", "karein",
    "toota", "loot", "chakkar", "raha", "rahe", "rahi", "chahiye", "karwake", "dene", "mana",
    "nikla", "atka", "paisa", "rakha", "khareeda", "bekhabar", "thaga", "khatam", "bheja",
    "karna", "khate", "unke", "iske", "wala", "wali", "bolkar", "bataya", "pehna", "nikal",
    "thop", "liya"
}


# -----------------------------------------------------------------------------
# 2. Curated Multilingual Legal Lexicon (Kannada & Hindi -> English Canonical)
# -----------------------------------------------------------------------------
INDIC_TO_CANONICAL_LEGAL: Dict[str, List[str]] = {
    # --- Cyber Fraud Concepts ---
    "ಬ್ಯಾಂಕ್": ["bank"],
    "ಖಾತೆ": ["account", "bank account"],
    "ಖಾತೆಯಿಂದ": ["account", "bank account"],
    "ಹಣ": ["money", "funds"],
    "ದುಡ್ಡು": ["money", "funds"],
    "ಕಡಿತ": ["debited", "deducted", "unauthorized transaction"],
    "ಕಡಿತವಾಗಿದೆ": ["debited", "unauthorized debit"],
    "ಕದ್ದಿದ್ದಾರೆ": ["stolen", "unauthorized debit"],
    "ಅನುಮತಿಯಿಲ್ಲದೆ": ["without permission", "unauthorized"],
    "ಅನುಮತಿ": ["permission", "consent"],
    "ವಂಚನೆ": ["fraud", "scam", "cheating"],
    "ವಂಚಿಸಿದ್ದಾರೆ": ["cheated", "fraud"],
    "ಓಟಿಪಿ": ["otp", "verification code"],
    "ವರ್ಗಾವಣೆ": ["transfer", "transaction"],
    "ಹ್ಯಾಕ್": ["hacked", "unauthorized access"],
    "ಲಿಂಕ್": ["phishing link", "malicious link"],
    "ಪಾಸ್‌ವರ್ಡ್": ["password", "credential"],
    "ಸೈಬರ್": ["cyber", "online fraud"],
    "ಸಿಬಿಐ": ["cbi", "police impersonation", "cyber fraud"],
    "ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್": ["digital arrest", "extortion", "cyber fraud"],
    "ಸುಲಿಗೆ": ["extortion", "cyber crime", "money"],
    "ವಿಡಿಯೋ ಕಾಲ್": ["video call", "digital arrest"],
    "ಕರೆ ಮಾಡಿ": ["phone call impersonation", "fake caller", "bank manager impersonation"],
    "ಲೋನ್ ಆಪ್": ["loan app fraud", "extortion", "harassment", "blackmail"],
    "ಸಾಲದ ಆ್ಯಪ್": ["loan app fraud", "extortion", "blackmail"],
    "ಕಿರುಕುಳ": ["harassment", "extortion", "blackmail"],
    "ಕದಿಯಲಾಗಿದೆ": ["stolen funds", "unauthorized debit"],

    "बैंक": ["bank"],
    "खाता": ["account", "bank account"],
    "खाते": ["account", "bank account"],
    "पैसे": ["money", "funds"],
    "रुपये": ["money", "rupees"],
    "कट": ["debited", "deducted"],
    "कट गए": ["debited", "unauthorized debit"],
    "काट लिए": ["debited", "deducted unauthorized"],
    "चुरा": ["stolen", "theft"],
    "चुरा लिए": ["stolen", "unauthorized debit"],
    "अनुमति के बिना": ["without permission", "unauthorized"],
    "अनुमति": ["permission", "consent"],
    "धोखाधड़ी": ["fraud", "cheating", "scam"],
    "धोखा": ["fraud", "cheating"],
    "ओटीपी": ["otp", "verification code"],
    "ट्रांसफर": ["transfer", "transaction"],
    "हैक": ["hacked", "unauthorized access"],
    "लिंक": ["phishing link", "malicious link"],
    "पासवर्ड": ["password", "credential"],
    "साइबर": ["cyber", "online fraud"],
    "सीबीआई": ["cbi", "police impersonation", "cyber fraud"],
    "डिजिटल अरेस्ट": ["digital arrest", "extortion", "cyber fraud"],
    "ऐंठ": ["extortion", "cyber crime"],
    "वीडियो कॉल": ["video call", "digital arrest"],
    "ಟೆಲಿಗ್ರಾಮ್": ["telegram", "telegram job scam", "task scam"],
    "ಪಾರ್ಟ್ ಟೈಮ್": ["part time job", "job scam", "task investment scam"],
    "ಹೂಡಿಕೆ": ["investment", "task investment"],
    "टेलीग्राम": ["telegram", "telegram job scam", "task scam"],
    "पार्ट टाइम": ["part time job", "job scam", "task investment scam"],
    "टास्क": ["task scam", "prepaid task investment"],
    "रिव्यू": ["hotel review", "task scam"],

    # Romanized Cyber Fraud
    "duddu": ["money", "funds"],
    "hana": ["money", "funds"],
    "paise": ["money", "funds"],
    "rupaye": ["money", "rupees"],
    "cut aagide": ["debited", "unauthorized debit"],
    "kat gaye": ["debited", "unauthorized debit"],
    "permission illade": ["without permission", "unauthorized"],
    "bina permission": ["without permission", "unauthorized"],
    "dhokhadhadi": ["fraud", "scam"],
    "vanchane": ["fraud", "scam"],
    "digital arrest": ["digital arrest", "extortion", "cyber fraud"],

    # --- Consumer Issues Concepts ---
    "ಗ್ರಾಹಕ": ["consumer", "customer"],
    "ಉತ್ಪನ್ನ": ["product", "goods"],
    "ವಸ್ತು": ["product", "item"],
    "ಖರೀದಿ": ["purchase", "bought"],
    "ಖರೀದಿಸಿದೆ": ["bought", "purchased", "defective product"],
    "ಖರೀದಿಸಿದ": ["bought", "purchased"],
    "ಕೊಂಡುಕೊಂಡೆ": ["bought", "purchased", "consumer product"],
    "ಕೊಂಡೆ": ["bought", "purchased"],
    "ದೋಷ": ["defect", "defective"],
    "ದೋಷಪೂರಿತ": ["defective", "damaged"],
    "ಮುರಿದ": ["broken", "damaged"],
    "ಕೆಲಸ ಮಾಡುತ್ತಿಲ್ಲ": ["not working", "defective product", "damaged"],
    "ಕೆಲಸ ಮಾಡ್ತಿಲ್ಲ": ["not working", "defective product"],
    "ಅಂಗಡಿಯವರು": ["shopkeeper", "store", "seller", "merchant"],
    "ಅಂಗಡಿ": ["shop", "store", "seller"],
    "ವಾಪಸ್ ತೆಗೆದುಕೊಳ್ಳುತ್ತಿಲ್ಲ": ["refusal to return", "refund denial", "return refused"],
    "ವಾಪಸ್ ಕೊಡ್ತಿಲ್ಲ": ["refund denial", "not returning money"],
    "ಹಿಂತಿರುಗಿಸಲು ನಿರಾಕರಣೆ": ["refund denial", "refusal to return"],
    "ಪಾರ್ಸೆಲ್": ["parcel", "courier", "delivery", "ecommerce"],
    "ಕಲ್ಲು": ["wrong item", "counterfeit", "delivery fraud", "fake parcel"],
    "ಆನ್‌ಲೈನ್": ["online shopping", "ecommerce"],
    "ಮೊಬೈಲ್": ["mobile phone", "appliance", "product"],
    "ಫೋನ್": ["phone", "appliance", "product"],
    "ರೆಫ್ರಿಜರೇಟರ್": ["refrigerator", "defective product", "appliance"],
    "ಫ್ರಿಜ್": ["refrigerator", "defective product", "appliance"],
    "ಕಂಪ್ರೆಸರ್": ["compressor", "defective product"],
    "ಇ-ಕಾಮರ್ಸ್": ["ecommerce order cancel", "refund denial", "consumer dispute"],
    "ಆರ್ಡರ್ ರದ್ದು": ["order cancelled", "refund denial", "stock out"],
    "ಮರುಪಾವತಿಸಿಲ್ಲ": ["refund denial", "unpaid refund"],
    "ಬ್ರಾಡ್‌ಬ್ಯಾಂಡ್": ["broadband provider", "internet outage", "service deficiency"],
    "ಇಂಟರ್ನೆಟ್ ಸಂಪರ್ಕ ಕಡಿತ": ["internet outage", "service deficiency"],
    "ಆಸ್ಪತ್ರೆ": ["hospital emergency", "hospital", "medical negligence"],
    "ವೈದ್ಯರು": ["doctor", "medical negligence"],
    "ವೈದ್ಯಕೀಯ ನಿರ್ಲಕ್ಷ್ಯ": ["medical negligence", "deficiency in service"],
    "ವೈದ್ಯಕೀಯ ರಕ್ತ ಪರೀಕ್ಷೆ": ["blood test", "breathalyzer defense", "medical test"],
    "ಶಸ್ತ್ರಚಿಕಿತ್ಸೆ": ["surgery", "medical negligence"],
    "ರೋಗಿ": ["patient", "medical negligence"],
    "ಕೋಚಿಂಗ್": ["coaching institute", "misleading advertisement", "consumer"],
    "ಜಾಹೀರಾತು": ["misleading advertisement", "consumer dispute"],
    "ಮರುಪಾವತಿ": ["refund", "money back"],
    "ಬದಲಾವಣೆ": ["replacement", "exchange"],
    "ವಾರಂಟಿ": ["warranty", "guarantee"],
    "ಸೇವೆ ಕೊರತೆ": ["deficiency of service"],
    "ಹೆಚ್ಚು ಬಿಲ್": ["overcharged", "excess billing"],
    "ಆಹಾರ ಕಲಬೆರಕೆ": ["food adulteration", "contaminated food"],
    "ಫ್ಲೈಟ್ ರದ್ದು": ["flight cancelled", "airline delay"],
    "ಬಿಲ್": ["bill", "invoice"],

    "उपभोक्ता": ["consumer", "customer"],
    "ग्राहक": ["consumer", "customer"],
    "उत्पाद": ["product", "item"],
    "सामान": ["product", "goods", "item"],
    "खरीद": ["purchase", "bought"],
    "खरीदा": ["bought", "purchased"],
    "खराबी": ["defect", "defective"],
    "खराब": ["defective", "damaged"],
    "फ्रिज": ["refrigerator", "defective product", "appliance"],
    "कंप्रेसर": ["compressor", "defective product"],
    "ब्रॉडबैंड": ["broadband provider", "internet outage", "service deficiency"],
    "इंटरनेट बंद": ["internet outage", "service deficiency"],
    "अस्पताल": ["hospital emergency", "hospital", "medical negligence"],
    "डॉक्टर": ["doctor", "medical negligence"],
    "सर्जरी": ["surgery", "medical negligence"],
    "मरीज": ["patient", "medical negligence"],
    "कोचिंग": ["coaching institute", "misleading advertisement", "consumer"],
    "विज्ञापन": ["misleading advertisement", "consumer dispute"],
    "टूटा": ["broken", "damaged"],
    "रिफंड": ["refund", "money back"],
    "वापसी": ["return", "refund"],
    "वारंटी": ["warranty", "guarantee"],
    "सेवा में कमी": ["deficiency of service"],
    "अधिक वसूली": ["overcharged", "excess price"],
    "खाने में मिलावट": ["food adulteration", "unsafe food"],
    "फ्लाइट रद्द": ["flight cancelled", "airline delay"],
    "बिल": ["bill", "invoice"],

    # Romanized Consumer
    "kharab": ["defective", "damaged"],
    "kelsa madtilla": ["not working", "defective"],
    "kaam nahi kar raha": ["not working", "defective"],
    "seva kami": ["deficiency of service"],
    "seve korathe": ["deficiency of service"],

    # --- Traffic Enforcement Concepts ---
    "ಸಂಚಾರ": ["traffic"],
    "ಸಂಚಾರ ಪೊಲೀಸ್": ["traffic police"],
    "ಸಂಚಾರ ಪೊಲೀಸರು": ["traffic police", "challan"],
    "ಚಲನ್": ["challan", "traffic fine"],
    "ಚಲನ್‌": ["challan", "traffic fine"],
    "ದಂಡ": ["fine", "penalty"],
    "ತಡೆದು": ["stopped vehicle", "traffic police", "interstate entry"],
    "ಅನಗತ್ಯವಾಗಿ": ["unlawfully", "wrongful challan", "harassment"],
    "ಹಾಕಿದ್ದಾರೆ": ["issued challan", "traffic fine"],
    "ಹಾಕಿದ್ರು": ["issued challan", "traffic fine"],
    "ಲಂಚ": ["bribe", "extortion", "corrupt traffic police"],
    "ದಾಖಲೆಗಳು": ["documents", "rc dl", "insurance"],
    "ಹೆಲ್ಮೆಟ್": ["helmet"],
    "ಐಎಸ್‌ಐ ಹೆಲ್ಮೆಟ್": ["isi helmet", "helmet dispute"],
    "ಹಿಂಬದಿ ಸವಾರ": ["pillion rider", "helmet dispute"],
    "ಒನ್‌ವೇ": ["one way street", "police diversion", "wrong side"],
    "ಒನ್-ವೇ": ["one way street", "police diversion", "wrong side"],
    "ತಿರುವು": ["traffic diversion", "police instruction", "police directed"],
    "ನಿರ್ದೇಶಿಸಿದ್ದರಿಂದ": ["police directed", "police instructed", "diversion"],
    "ರಸ್ತೆ ಕಾಮಗಾರಿ": ["road construction", "traffic diversion"],
    "ವೇಗದ ಮಿತಿ": ["speed limit", "overspeeding", "speed governor", "speed trap"],
    "ಸ್ಪೀಡ್ ಗವರ್ನರ್": ["speed governor", "speed trap", "radar"],
    "ಸಿಗ್ನಲ್": ["traffic signal", "red light"],
    "ವಾಹನ": ["vehicle", "motor vehicle"],
    "ಕಾರು": ["car"],
    "ಬೈಕ್": ["bike", "motorcycle"],
    "ಚಾಲನಾ ಪರವಾನಗಿ": ["driving licence", "license"],
    "ಅತಿವೇಗ": ["overspeeding", "speed trap", "radar"],
    "ಕುಡಿದು ವಾಹನ ಚಾಲನೆ": ["drunk driving", "breathalyzer"],
    "ಬ್ರೀತ್‌ಅನಲೈಜರ್": ["breathalyzer", "drunk driving"],
    "ಪಿಯುಸಿ": ["puc", "pollution certificate"],
    "ವಿಮೆ": ["vehicle insurance", "third party insurance"],
    "ಪಾರ್ಕಿಂಗ್": ["parking fine", "towed vehicle"],

    "यातायात": ["traffic"],
    "ट्रैफिक": ["traffic"],
    "ट्रैफिक पुलिस": ["traffic police"],
    "चालान": ["challan", "traffic fine"],
    "जुर्माना": ["penalty", "fine"],
    "हेलमेट": ["helmet"],
    "पिलियन": ["pillion rider", "helmet dispute"],
    "डायवर्जन": ["traffic diversion", "police instruction", "police directed"],
    "मोड़ा था": ["traffic diversion", "police directed", "diversion"],
    "गलत दिशा": ["wrong side", "one way street", "police diversion"],
    "वन-वे": ["wrong side", "one way street", "police diversion"],
    "सड़क निर्माण": ["road construction", "traffic diversion"],
    "आईएएसआई हेलमेट": ["isi helmet", "helmet dispute"],
    "स्पीड गवर्नर": ["speed governor", "speed trap", "radar"],
    "रडार": ["speed trap", "radar", "radar calibration"],
    "सिग्नल": ["traffic signal", "red light"],
    "गाड़ी": ["vehicle", "motor vehicle"],
    "कार": ["car"],
    "बाइक": ["bike", "motorcycle"],
    "ड्राइविंग लाइसेंस": ["driving licence", "license"],
    "तेज गति": ["overspeeding", "speed trap", "radar"],
    "ओवरस्पीडिंग": ["overspeeding", "speeding"],
    "शराब पीकर गाड़ी": ["drunk driving", "breathalyzer"],
    "ब्रेथ एनालाइजर": ["breathalyzer", "drunk driving"],
    "रक्त परीक्षण": ["blood test", "breathalyzer defense", "medical test"],
    "प्रदूषण": ["pollution certificate", "puc"],
    "बीमा": ["vehicle insurance", "third party insurance"],
    "पार्किंग": ["parking fine", "towed vehicle"],

    # Romanized Traffic
    "gaadi": ["vehicle", "motor vehicle"],
    "challann": ["challan", "traffic fine"],
    "danda": ["fine", "penalty"],
    "jurmana": ["fine", "penalty"],

    # --- Workplace / Wage Concepts ---
    "ವೇತನ": ["salary", "wages"],
    "ಸಂಬಳ": ["salary", "wages"],
    "ಸಂಬಳ ನೀಡಿಲ್ಲ": ["unpaid salary", "delayed wage"],
    "ಸಂಬಳ ಕೊಟ್ಟಿಲ್ಲ": ["unpaid salary", "delayed wage", "wages withheld"],
    "ಕೆಲಸ ಮಾಡುತ್ತಿರುವ": ["employed", "company", "worker"],
    "ತಿಂಗಳಿಂದ": ["months unpaid", "delayed wages"],
    "ಮಾಸಿಕ ವೇತನವನ್ನು ನೀಡಿಲ್ಲ": ["unpaid salary", "delayed wage"],
    "ಉದ್ಯೋಗದಾತರು": ["employer", "company"],
    "ಕಂಪನಿ": ["company"],
    "ಪಿಎಫ್": ["provident fund", "pf money", "epfo"],
    "ಭವಿಷ್ಯ ನಿಧಿ": ["provident fund", "epfo", "epf contribution"],
    "ಗ್ರಾಚ್ಯುಟಿ": ["gratuity", "gratuity withholding"],
    "ಲ್ಯಾಪ್‌ಟಾಪ್ ಕಡಿತ": ["unauthorized wage deduction", "salary deduction"],
    "ರಾಜೀನಾಮೆ": ["resignation", "notice period"],
    "ಪೋಶ್": ["posh", "workplace sexual harassment", "internal committee"],
    "ಆಂತರಿಕ ಸಮಿತಿ": ["internal committee", "posh workplace harassment"],
    "ಲೈಂಗಿಕ ಕಿರುಕುಳ": ["workplace sexual harassment", "posh"],
    "ಪ್ರಸೂತಿ ರಜೆ": ["maternity leave"],

    "वेतन": ["salary", "wages"],
    "तनख्वाह": ["salary", "wages"],
    "सैलरी": ["salary", "wages"],
    "वेतन रोक रखा": ["unpaid salary", "delayed wage"],
    "मासिक वेतन": ["monthly salary", "delayed wage"],
    "नियोक्ता": ["employer", "company"],
    "पीएफ": ["provident fund", "pf money", "epfo"],
    "भविष्य निधि": ["provident fund", "epfo", "epf contribution"],
    "ग्रेच्युटी": ["gratuity", "gratuity withholding"],
    "पॉश": ["posh", "workplace sexual harassment", "internal committee"],
    "यौन उत्पीड़न": ["workplace sexual harassment", "posh"],
    "आंतरिक समिति": ["internal committee", "posh"],
    "इस्तीफा": ["resignation", "notice period"],
    "मातृत्व अवकाश": ["maternity leave"],

    # Romanized Workplace
    "tankhwah": ["salary", "wages"],
    "sambala": ["salary", "wages"],
    "naukri": ["job", "employment"],
    "kelasa": ["job", "employment"],
    "sambala kottilla": ["unpaid salary", "delayed wage"],
    "tankhwah nahi di": ["unpaid salary", "delayed wage"],

    # --- Contractual Disputes Concepts ---
    "ಒಪ್ಪಂದ": ["contract", "agreement"],
    "ಕರಾರು": ["agreement", "deed"],
    "ಬಾಡಿಗೆ ಮನೆಯ ಮಾಲೀಕರು": ["landlord", "rented premises", "security deposit dispute"],
    "ಬಾಡಿಗೆ ಮನೆ": ["rented house", "tenancy", "premises"],
    "ಅಡ್ವಾನ್ಸ್ ಹಣ": ["advance deposit", "security deposit dispute"],
    "ಅಡ್ವಾನ್ಸ್": ["advance deposit", "security deposit"],
    "ಮುಂಗಡ ಹಣ": ["advance deposit", "security deposit dispute"],
    "ಠೇವಣಿ ಹಣ": ["security deposit dispute"],
    "ವಾಪಸ್ ಕೊಡುತ್ತಿಲ್ಲ": ["refusal to refund deposit", "breach of contract"],
    "ಬಾಡಿಗೆ ಅಪಾರ್ಟ್‌ಮೆಂಟ್": ["rented apartment", "security deposit dispute"],
    "ಬೀಗಗಳನ್ನು ಹಸ್ತಾಂತರಿಸಿದೆ": ["vacated apartment", "security deposit dispute"],
    "ಮನೆ ಮಾಲೀಕರು": ["landlord", "security deposit dispute"],
    "ಠೇವಣಿ": ["deposit", "security deposit dispute"],
    "ಖಾತೆಯಲ್ಲಿ ಹಣವಿಲ್ಲದೆ": ["insufficient funds", "cheque bounce", "section 138"],
    "ಖಾತೆಯಲ್ಲಿ ಸಾಕಷ್ಟು ಹಣವಿಲ್ಲ": ["insufficient funds", "cheque bounce", "section 138"],
    "ಹಣವಿಲ್ಲದೆ ಬೌನ್ಸ್": ["insufficient funds", "cheque bounce", "section 138"],
    "ಸ್ನೇಹಿತನಿಗೆ ಕೊಟ್ಟ ಚೆಕ್": ["cheque bounce", "section 138"],
    "ಚೆಕ್ ಬೌನ್ಸ್": ["cheque bounce", "cheque dishonour", "section 138"],
    "ಚೆಕ್": ["cheque", "cheque bounce"],
    "ಬೌನ್ಸ್": ["cheque bounce", "section 138"],
    "ಕಚ್ಚಾ ಸಾಮಗ್ರಿ": ["raw material", "commercial supply contract", "breach of contract"],
    "ವಾಣಿಜ್ಯ ಸರಬರಾಜುದಾರರು": ["commercial supplier", "breach of contract"],
    "ನಾನ್-ಕಾಂಪೀಟ್": ["non compete clause", "contract act section 27"],
    "ಸ್ಪರ್ಧಿ ಸಂಸ್ಥೆ": ["competitor company", "non compete clause", "section 27"],
    "ಕಲ್ಯಾಣ ಮಂಟಪ": ["banquet hall", "advance deposit forfeiture", "section 74"],
    "ಮುಟ್ಟುಗೋಲು": ["forfeiture", "advance deposit forfeiture", "section 74"],

    "अनुबंध": ["contract", "agreement"],
    "समझौता": ["agreement", "contract"],
    "किराए का फ्लैट": ["rented apartment", "security deposit dispute"],
    "चाबियां": ["vacated apartment", "security deposit dispute"],
    "मकान मालिक": ["landlord", "security deposit dispute"],
    "सिक्योरिटी डिपॉजिट": ["security deposit dispute"],
    "पर्याप्त राशि न होने": ["insufficient funds", "cheque bounce", "section 138"],
    "खाते में पर्याप्त राशि नहीं": ["insufficient funds", "cheque bounce", "section 138"],
    "चेक बाउंस": ["cheque bounce", "cheque dishonour", "section 138"],
    "चेक": ["cheque", "cheque bounce"],
    "बाउंस": ["cheque bounce", "section 138"],
    "कच्चे माल": ["raw material", "commercial supply", "breach of contract"],
    "सप्लायर": ["commercial supplier", "breach of contract"],
    "नॉन-कम्पीट": ["non compete clause", "contract act section 27"],
    "प्रतियोगी कंपनी": ["competitor company", "non compete clause", "section 27"],
    "बैंक्वेट हॉल": ["banquet hall", "advance deposit forfeiture", "section 74"],
    "जब्त": ["advance booking forfeiture", "section 74 penalty"],

    # Romanized Contractual
    "kiraya": ["rent", "tenancy"],
    "badige": ["rent", "tenancy"],
    "thevani": ["security deposit", "deposit"],
    "oppanda": ["contract", "agreement"],
    "samjhauta": ["contract", "agreement"],
    "cheque bounce": ["cheque bounce", "section 138"],
    "non-compete": ["non compete clause", "contract act section 27"],
}


# -----------------------------------------------------------------------------
# 3. Unicode Normalization & Cleaning
# -----------------------------------------------------------------------------
def normalize_unicode(text: str) -> str:
    """Applies NFKC normalization and strips non-printable / zero-width characters."""
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKC", text)
    normalized = re.sub(r"[\u200B\u200C\u200D\uFEFF]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


# -----------------------------------------------------------------------------
# 4. Script & Language Detection Engine
# -----------------------------------------------------------------------------
def detect_language_and_script(text: str) -> LanguageInfo:
    """Robustly identifies language, script, code-mixing status, and canonical text."""
    normalized = normalize_unicode(text)
    if not normalized:
        return LanguageInfo(
            detected_language="unknown",
            language_confidence=0.0,
            detected_script="Unknown",
            is_code_mixed=False,
            normalized_text="",
            canonical_text="",
        )

    # 1. Script Counts
    kn_chars = len(KANNADA_RANGE.findall(normalized))
    hi_chars = len(DEVANAGARI_RANGE.findall(normalized))
    lat_chars = len(LATIN_RANGE.findall(normalized))
    total_alpha = kn_chars + hi_chars + lat_chars

    if total_alpha == 0:
        return LanguageInfo(
            detected_language="unknown",
            language_confidence=0.0,
            detected_script="Punctuation/Numeric",
            is_code_mixed=False,
            normalized_text=normalized,
            canonical_text=normalized,
        )

    kn_ratio = kn_chars / total_alpha
    hi_ratio = hi_chars / total_alpha
    lat_ratio = lat_chars / total_alpha

    detected_script = "Latin"
    is_code_mixed = False

    # Check for code-mixing between Indic script and Latin
    if kn_chars >= 4 and lat_chars >= 8:
        detected_lang = "kn-en"
        detected_script = "Mixed"
        is_code_mixed = True
        confidence = 0.95
    elif hi_chars >= 4 and lat_chars >= 8:
        detected_lang = "hi-en"
        detected_script = "Mixed"
        is_code_mixed = True
        confidence = 0.95
    elif kn_ratio >= 0.20:
        detected_lang = "kn"
        detected_script = "Kannada" if kn_ratio >= 0.75 else "Mixed"
        is_code_mixed = (lat_chars > 0)
        confidence = round(min(1.0, kn_ratio + 0.3), 2)
    elif hi_ratio >= 0.20:
        detected_lang = "hi"
        detected_script = "Devanagari" if hi_ratio >= 0.75 else "Mixed"
        is_code_mixed = (lat_chars > 0)
        confidence = round(min(1.0, hi_ratio + 0.3), 2)
    else:
        # 3. Pure Latin Script — Distinguish English vs Romanized Kanglish / Hinglish vs Code-mixed
        tokens = [t.lower() for t in re.findall(r"[a-zA-Z]+", normalized)]
        kn_hits = sum(1 for t in tokens if t in KANGLISH_MARKERS)
        hi_hits = sum(1 for t in tokens if t in HINGLISH_MARKERS)

        if kn_hits >= 1 and kn_hits >= hi_hits:
            is_mixed = (len(tokens) >= 8 and kn_hits <= len(tokens) * 0.45)
            detected_lang = "kn-en" if is_mixed else "kn-Latn"
            detected_script = "Latin"
            is_code_mixed = True
            confidence = round(min(1.0, 0.70 + (kn_hits * 0.05)), 2)
        elif hi_hits >= 1 and hi_hits > kn_hits:
            is_mixed = (len(tokens) >= 8 and hi_hits <= len(tokens) * 0.45)
            detected_lang = "hi-en" if is_mixed else "hi-Latn"
            detected_script = "Latin"
            is_code_mixed = True
            confidence = round(min(1.0, 0.70 + (hi_hits * 0.05)), 2)
        else:
            detected_lang = "en"
            detected_script = "Latin"
            is_code_mixed = False
            confidence = round(lat_ratio, 2)

    # 4. Build Canonical Aligned Representation for Retrieval
    canonical_tokens: List[str] = []
    text_lower = normalized.lower()

    for indic_term, canonical_concepts in INDIC_TO_CANONICAL_LEGAL.items():
        if indic_term in text_lower:
            canonical_tokens.extend(canonical_concepts)

    if canonical_tokens:
        canonical_text = f"{normalized} [CANONICAL: {' '.join(set(canonical_tokens))}]"
    else:
        canonical_text = normalized

    return LanguageInfo(
        detected_language=detected_lang,
        language_confidence=confidence,
        detected_script=detected_script,
        is_code_mixed=is_code_mixed,
        normalized_text=normalized,
        canonical_text=canonical_text,
    )
