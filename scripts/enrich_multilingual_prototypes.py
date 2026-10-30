"""Enrich knowledge base issues with authentic multilingual prototype texts.

Adds native Kannada, native Hindi, Romanized Kannada (Kanglish), and
Romanized Hindi (Hinglish) prototype texts to legal issues in
knowledge_base/issue_mappings.json.
"""

from __future__ import annotations

import json
from pathlib import Path

KB_MAPPINGS = Path("knowledge_base/issue_mappings.json")

# High-frequency multilingual prototype templates and expressions per domain
MULTILINGUAL_EXPANSIONS = {
    # --- CYBER FRAUD ---
    "otp_fraud": [
        "ಯಾರೋ ಬ್ಯಾಂಕ್ ಮ್ಯಾನೇಜರ್ ಅಂತ ಕರೆ ಮಾಡಿ ಒಟಿಪಿ ಪಡೆದುಕೊಂಡರು ಮತ್ತು ಖಾತೆಯಿಂದ ಹಣ ಕಡಿತವಾಯಿತು.",
        "किसी ने बैंक से फोन किया और ओटीपी मांगा, ओटीपी बताते ही खाते से पैसे कट गए।",
        "Phone call madi bank KYC ge OTP kedi nanna account inda duddu transfer madiddare.",
        "Kisi ne fake bank call karke OTP manga aur phone par aate hi account se paise nikal liye."
    ],
    "upi_payment_fraud": [
        "ಯುಪಿಐ ಮೂಲಕ ಹಣ ಸ್ವೀಕರಿಸಲು ಕ್ಯೂಆರ್ ಕೋಡ್ ಸ್ಕ್ಯಾನ್ ಮಾಡಲು ಹೇಳಿ ನನ್ನ ಖಾತೆಯಿಂದ ಹಣ ಕದ್ದಿದ್ದಾರೆ.",
        "यूपीआई पर पैसे भेजने के बहाने क्यूआर कोड स्कैन करवाया और मेरे खाते से पैसे कट गए।",
        "UPI payment madbeku antha helidru QR scan madi nan account inda duddu transfer aagide.",
        "UPI se payment receive karne ke liye QR scan kiya aur account se paise kat gaye."
    ],
    "phishing": [
        "ಬ್ಯಾಂಕ್ ಕೆವೈಸಿ ಅಪ್‌ಡೇಟ್ ಮಾಡಲು ಎಸ್‌ಎಂಎಸ್ ಲಿಂಕ್ ಕಳುಹಿಸಿ ವಂಚನೆ ಮಾಡಲಾಗಿದೆ.",
        "बैंक केवाईसी अपडेट करने के नाम पर मैसेज में फर्जी लिंक भेजकर धोखाधड़ी की गई।",
        "Bank KYC update antha fake link kalisi account hack madi duddu kaddidare.",
        "Bank SMS me fake link aaya KYC ke liye aur click karte hi account hack ho gaya."
    ],
    "identity_theft": [
        "ನನ್ನ ಆಧಾರ್ ಮತ್ತು ಪಾನ್ ವಿವರಗಳನ್ನು ಬಳಸಿ ಯಾರೋ ನನ್ನ ಹೆಸರಿನಲ್ಲಿ ನಕಲಿ ಸಾಲ ಅಥವಾ ಸಿಮ್ ಪಡೆದಿದ್ದಾರೆ.",
        "मेरे आधार और पैन कार्ड का गलत इस्तेमाल करके किसी ने मेरे नाम पर फर्जी लोन ले लिया।",
        "Nanna aadhaar pan card use madi nan hesaralli fake loan thagondiddare identity theft.",
        "Mera aadhaar aur pan use karke kisi ne mere naam se fake SIM ya loan nikal liya."
    ],
    "sim_swap_fraud": [
        "ನನ್ನ ಸಿಮ್ ಕಾರ್ಡ್ ದಿಢೀರನೆ ನಿಷ್ಕ್ರಿಯಗೊಂಡಿತು ಮತ್ತು ಹೊಸ ಸಿಮ್ ಪಡೆದು ಬ್ಯಾಂಕ್ ಖಾತೆಯಿಂದ ಹಣ ವರ್ಗಾಯಿಸಿದ್ದಾರೆ.",
        "मेरा सिम कार्ड अचानक बंद हो गया और जालसाजों ने नया सिम लेकर बैंक से पैसे निकाल लिए।",
        "Nan SIM block aagi fraudster bere SIM issue madsi bank account inda duddu withdraw madidare.",
        "SIM swap fraud hua mera network band ho gaya aur duplicate SIM se bank paise uda liye."
    ],
    "part_time_job_fraud": [
        "ಟೆಲಿಗ್ರಾಮ್‌ನಲ್ಲಿ ದಿನಕ್ಕೆ 3000 ಗಳಿಸಿ ಎಂದು ಸುಳ್ಳು ಪಾರ್ಟ್ ಟೈಮ್ ಕೆಲಸದ ಆಮಿಷವೊಡ್ಡಿ ಹಣ ವಂಚಿಸಿದ್ದಾರೆ.",
        "टेलीग्राम पर पार्ट टाइम जॉब का लालच देकर टास्क पूरा करने के नाम पर लाखों रुपये ठग लिए।",
        "Telegram task job antha helidru review madi daily earning antha duddu cheat madidare.",
        "Telegram par fake review task job me invest karwake lakhon rupaye fraud kar liye."
    ],
    "digital_arrest_extortion": [
        "ಸಿಬಿಐ ಅಥವಾ ಮುಂಬೈ ಪೊಲೀಸರು ಎಂದು ವಿಡಿಯೋ ಕಾಲ್ ಮಾಡಿ ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್ ಹೆಸರಿನಲ್ಲಿ ಬೆದರಿಸಿ ಹಣ ಪಡೆದಿದ್ದಾರೆ.",
        "सीबीआई या पुलिस अधिकारी बनकर वीडियो कॉल किया और डिजिटल अरेस्ट की धमकी देकर पैसे ट्रांसफर करवाए।",
        "Police athava CBI officer antha video call madi digital arrest antha hedrisi duddu transfer madskondru.",
        "CBI ya customs officer bankar fake digital arrest warrant dikha kar account se paise loot liye."
    ],
    "rbi_zero_liability_unauthorized_transaction": [
        "ನನ್ನ ಅನುಮತಿ ಅಥವಾ ಒಟಿಪಿ ಇಲ್ಲದೆ ನನ್ನ ಬ್ಯಾಂಕ್ ಖಾತೆಯಿಂದ ಹಣ ಕಡಿತವಾಗಿದೆ ಮತ್ತು ಅನಧಿಕೃತ ವಹಿವಾಟು ನಡೆದಿದೆ.",
        "मेरे बैंक खाते से मेरी अनुमति या ओटीपी के बिना पैसे कट गए और अनधिकृत लेनदेन हुआ।",
        "Nanna bank account inda permission illade unauthorized aagi duddu cut aagide.",
        "Mere bank account se bina meri permission ya OTP ke paise kat gaye aur unauthorized debit ho gaya."
    ],

    # --- CONSUMER ISSUES ---
    "defective_product": [
        "ನಾನು ಖರೀದಿಸಿದ ಹೊಸ ಉತ್ಪನ್ನದಲ್ಲಿ ದೋಷವಿದೆ ಮತ್ತು ಕಂಪನಿ ಮರುಪಾವತಿ ಅಥವಾ ಬದಲಾವಣೆ ನಿರಾಕರಿಸಿದೆ.",
        "दुकान से खरीदा गया नया उत्पाद खराब निकला और विक्रेता ने पैसे वापस करने या बदलने से मना कर दिया।",
        "Khareedi madida hosha item defect aagide replacement athava refund kodalla anthare.",
        "Dukaan se khareeda hua product defective nikla aur seller na refund de raha hai na replace."
    ],
    "service_deficiency": [
        "ನಾನು ಪಾವತಿಸಿದ ಸೇವೆ ಅತ್ಯಂತ ಕಳಪೆಯಾಗಿದೆ ಮತ್ತು ಒಪ್ಪಂದದಂತೆ ಕೆಲಸ ಪೂರ್ಣಗೊಳಿಸಿಲ್ಲ.",
        "कंपनी की सेवा में भारी कमी है, पैसे लेने के बाद भी उचित सेवा प्रदान नहीं की गई।",
        "Full amount pay madidru service kottilla deficiency of service consumer complaint madbeku.",
        "Puri payment lene ke baad bhi company ne service theek se nahi di aur deficiency of service ki."
    ],
    "refund_denial": [
        "ಆನ್‌ಲೈನ್ ಪಾವತಿ ಪೂರ್ಣಗೊಂಡಿದ್ದರೂ ಇ-ಕಾಮರ್ಸ್ ಸಂಸ್ಥೆ ಆದೇಶಿಸಿದ ವಸ್ತುಗಳನ್ನು ವಿತರಿಸಿಲ್ಲ ಮತ್ತು ಹಣ ವಾಪಸ್ ನೀಡಿಲ್ಲ.",
        "भुगतान करने के बाद भी विक्रेता ने सामान नहीं भेजा और रिफंड देने से साफ इनकार कर दिया।",
        "Online payment aagide order deliver aagilla refund kodalla antha company reject madide.",
        "Payment hone ke bawjud na product deliver hua na refund diya consumer rights violation."
    ],
    "misleading_advertisement": [
        "ಜಾಹೀರಾತಿನಲ್ಲಿ ಸುಳ್ಳು ಭರವಸೆ ನೀಡಿ ಕಳಪೆ ಉತ್ಪನ್ನವನ್ನು ಮಾರಾಟ ಮಾಡಲಾಗಿದೆ.",
        "विज्ञापन में बड़े-बड़े झूठे दावे करके घटिया सामान बेच दिया भ्रामक विज्ञापन।",
        "TV advertisement nalli fake claims madi bad product kottidare misleading ad complaint.",
        "Misleading advertisement dekh kar course ya product liya par reality me sab jhooth tha."
    ],

    # --- TRAFFIC ENFORCEMENT ---
    "seatbelt_helmet_camera_dispute": [
        "ಸಂಚಾರ ಪೊಲೀಸರು ಹೆಲ್ಮೆಟ್ ಧರಿಸಿಲ್ಲ ಎಂದು ತಪ್ಪು ಚಲನ್ ಅಥವಾ ಕ್ಯಾಮೆರಾ ನೋಟಿಸ್ ನೀಡಿದ್ದಾರೆ.",
        "हेलमेट पहनने के बावजूद ट्रैफिक पुलिस या कैमरे ने बिना हेलमेट का गलत चालान काट दिया।",
        "Helmet dharisidru traffic camera invalid challan issue madide grievance file madbeku.",
        "Helmet pehna hua tha fir bhi automated traffic camera ne 1000 ka galat challan bhej diya."
    ],
    "two_wheeler_pillion_helmet_challan_dispute": [
        "ಹಿಂಬದಿ ಸವಾರರು ಹೆಲ್ಮೆಟ್ ಧರಿಸಿದ್ದರೂ ಸಂಚಾರ ಕ್ಯಾಮೆರಾ ತಪ್ಪು ನೋಟಿಸ್ ನೀಡಿದೆ.",
        "पीछे बैठे व्यक्ति ने भी हेलमेट लगाया था फिर भी पिलियन राइडर का गलत चालान काट दिया।",
        "Pillion rider helmet haakidru false e-challan issue madiddare grievance upload madbeku.",
        "Pillion rider helmet pehne hue tha fir bhi camera ne wrong challan generate kar diya."
    ],
    "wrong_side_police_diversion_defense": [
        "ಪೊಲೀಸರ ನಿರ್ದೇಶನದಂತೆ ತಿರುವು ಪಡೆದಿದ್ದರೂ ವಿರುದ್ಧ ದಿಕ್ಕಿನಲ್ಲಿ ಚಲಿಸಿದ ಆರೋಪದ ಮೇಲೆ ಚಲನ್ ಹಾಕಿದ್ದಾರೆ.",
        "ट्रैफिक पुलिस के कहने पर डायवर्जन लिया था, फिर भी गलत साइड गाड़ी चलाने का चालान भेज दिया।",
        "Traffic cop instructions prakara one way hogidde aadre camera section 184 challan kottide.",
        "Police officer ke diversion batane par gaadi mod li thi par wrong side challan aa gaya."
    ],
    "drunk_driving_breathalyzer_dispute": [
        "ಮದ್ಯ ಸೇವಿಸದಿದ್ದರೂ ಪೊಲೀಸರು ಬ್ರೀತ್‌ಅನಲೈಜರ್ ಪರೀಕ್ಷೆ ಮಾಡದೆ ಸುಳ್ಳು ದಂಡ ವಿಧಿಸಿದ್ದಾರೆ.",
        "शराब नहीं पी थी फिर भी पुलिस ने ब्रेथ एनालाइजर टेस्ट में हेरफेर करके गलत केस बना दिया।",
        "Alcohol consume madilla aadre traffic police drink and drive challan section 185 apply madiddare.",
        "Sharab nahi pi thi fir bhi traffic cop ne breathalyzer bina check kiye section 185 laga diya."
    ],

    # --- WORKPLACE / WAGE ---
    "delayed_wages": [
        "ಕಳೆದ ಮೂರು ತಿಂಗಳಿಂದ ಮಾಲೀಕರು ಯಾವುದೇ ಕಾರಣವಿಲ್ಲದೆ ನನ್ನ ಮಾಸಿಕ ವೇತನವನ್ನು ನೀಡಿಲ್ಲ.",
        "कंपनी पिछले तीन महीनों से बिना किसी कारण के मेरा वेतन और बकाया तनख्वाह रोक कर बैठी है।",
        "Last 3 months inda company sambala kottilla unpaid salary legal notice kalisbeku.",
        "Employer pichle 3 mahine se salary nahi de raha hai Payment of Wages Act me complaint karni hai."
    ],
    "unpaid_wages": [
        "ಕೆಲಸ ಮಾಡಿದ ಪೂರ್ಣ ಅವಧಿಯ ವೇತನವನ್ನು ಸಂಸ್ಥೆಯು ನೀಡದೆ ಬಾಕಿ ಉಳಿಸಿಕೊಂಡಿದೆ.",
        "काम करने के बाद भी कंपनी ने पूरी तनख्वाह नहीं दी और पैसे देने से मना कर दिया।",
        "Kelasa madida full salary kottilla company labour commissioner ge complaint madbeku.",
        "Full month kaam kiya par company ne salary nahi di unpaid wages recovery under section 15."
    ],
    "unauthorized_deduction": [
        "ಉದ್ಯೋಗದಾತರು ನನ್ನ ಪೂರ್ವಾನುಮತಿಯಿಲ್ಲದೆ ವೇತನದಿಂದ ಅಕ್ರಮವಾಗಿ ಕಡಿತ ಮಾಡಿದ್ದಾರೆ.",
        "कंपनी ने बिना किसी वैध कारण के मेरे वेतन से गैरकानूनी कटौती कर ली है।",
        "Consent illade salary inda illegal deductions madiddare Payment of Wages Act Section 7.",
        "Bina permission salary se galat deduction kiya company ne labour court me claim karna hai."
    ],
    "pf_deduction_non_deposit": [
        "ಪ್ರತಿ ತಿಂಗಳು ವೇತನದಿಂದ ಪಿಎಫ್ ಕಡಿತಗೊಳಿಸಿದ್ದರೂ ಇಪಿಎಫ್‌ಒ ಖಾತೆಗೆ ಜಮಾ ಮಾಡಿಲ್ಲ.",
        "वेतन से हर महीने पीएफ काटा गया लेकिन कंपनी ने भविष्य निधि खाते में जमा नहीं किया।",
        "Monthly payslip nalli PF deduct aagide aadre EPFO passbook ge deposit aagilla.",
        "Salary se PF cut hota hai par EPFO portal par passbook me deposit nahi dikha raha."
    ],
    "gratuity_withholding_dispute": [
        "ಐದು ವರ್ಷಗಳ ಸೇವೆ ಪೂರ್ಣಗೊಳಿಸಿ ರಾಜೀನಾಮೆ ನೀಡಿದ ನಂತರವೂ ಗ್ರ್ಯಾಚ್ಯುಟಿ ಪಾವತಿಸಿಲ್ಲ.",
        "पांच साल लगातार काम करके इस्तीफा देने के बाद भी कंपनी ने ग्रेच्युटी का भुगतान नहीं किया।",
        "5 years continuous service complete aagidru company gratuity payment release madilla.",
        "5 saal service ke baad resign kiya par company gratuity ka paisa nahi de rahi hai."
    ],
    "posh_workplace_sexual_harassment_complaint": [
        "ಕೆಲಸದ ಸ್ಥಳದಲ್ಲಿ ಮಹಿಳಾ ಉದ್ಯೋಗಿಗೆ ಲೈಂಗಿಕ ಅಥವಾ ಮಾನಸಿಕ ಕಿರುಕುಳ ನೀಡಲಾಗಿದೆ.",
        "कार्यस्थल पर महिला कर्मचारी के साथ यौन उत्पीड़न और अनुचित व्यवहार किया गया।",
        "Office nalli female employee ge POSH sexual harassment aagide internal committee complaint.",
        "Workplace par female staff ke sath sexual harassment hua aur Internal Committee sunwai nahi kar rahi."
    ],

    # --- CONTRACTUAL DISPUTES ---
    "security_deposit_dispute": [
        "ಬಾಡಿಗೆ ಮನೆ ಖಾಲಿ ಮಾಡಿದ ನಂತರವೂ ಮನೆ ಮಾಲೀಕರು ಭದ್ರತಾ ಠೇವಣಿಯನ್ನು ವಾಪಸ್ ನೀಡಲು ನಿರಾಕರಿಸಿದ್ದಾರೆ.",
        "फ्लैट खाली करने के बाद भी मकान मालिक सिक्योरिटी डिपॉजिट की रकम वापस नहीं कर रहा है।",
        "House vacate madi keys hand over madidru landlord security deposit thevani refund madilla.",
        "Makan khali kar diya par landlord security deposit wapas nahi kar raha bekar ke charges laga raha hai."
    ],
    "cheque_bounce_statutory_notice_138": [
        "ವ್ಯಾಪಾರ ಬಾಕಿಗಾಗಿ ನೀಡಿದ ಚೆಕ್ ಬ್ಯಾಂಕಿನಲ್ಲಿ ಹಣದ ಕೊರತೆಯಿಂದ ಬೌನ್ಸ್ ಆಗಿದೆ.",
        "बकाया राशि के भुगतान के लिए दिया गया चेक खाते में अपर्याप्त राशि के कारण बाउंस हो गया।",
        "Business client kottidda cheque funds insufficient antha bank memo bounce aagide.",
        "Business debt ke liye client ne cheque diya tha jo insufficient balance se bounce ho gaya Section 138."
    ],
    "breach_of_contract": [
        "ಒಪ್ಪಂದದ ಷರತ್ತುಗಳನ್ನು ಉಲ್ಲಂಘಿಸಿ ಸರಕು ಸರಬರಾಜು ಮಾಡದೆ ವ್ಯಾಪಾರ ನಷ್ಟ ಉಂಟುಮಾಡಿದ್ದಾರೆ.",
        "व्यापारिक अनुबंध की शर्तों का उल्लंघन करके सप्लाई रोक दी जिससे भारी आर्थिक नुकसान हुआ।",
        "Commercial contract breach aagide terms follow madilla compensation damages claim madbeku.",
        "Commercial contract ke terms violate kiye supplier ne aur supply rok di damages Section 73."
    ],
    "non_compete_clause_dispute": [
        "ರಾಜೀನಾಮೆ ನೀಡಿದ ನಂತರ ಎರಡು ವರ್ಷ ಯಾವುದೇ ಕಂಪನಿಯಲ್ಲಿ ಕೆಲಸ ಮಾಡಬಾರದು ಎಂದು ಬೆದರಿಸುತ್ತಿದ್ದಾರೆ.",
        "इस्तीफे के बाद कंपनी गैर-कानूनी नॉन-कम्पीट क्लॉज लगाकर दूसरी जगह नौकरी करने से रोक रही है।",
        "Resign madidmele bere company ge hogbardu antha non-compete clause inda threaten madiddare.",
        "Company non-compete clause ka bahana banakar relieving letter nahi de rahi Contract Act Section 27."
    ],
}


def main():
    with open(KB_MAPPINGS, encoding="utf-8") as f:
        data = json.load(f)

    issues = data["issues"]
    enriched_count = 0
    added_protos = 0

    for issue_id, new_protos in MULTILINGUAL_EXPANSIONS.items():
        if issue_id in issues:
            cur_protos = issues[issue_id].setdefault("prototype_texts", [])
            for p in new_protos:
                if p not in cur_protos:
                    cur_protos.append(p)
                    added_protos += 1
            enriched_count += 1

    with open(KB_MAPPINGS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully enriched {enriched_count} issues with {added_protos} multilingual prototypes.")


if __name__ == "__main__":
    main()
