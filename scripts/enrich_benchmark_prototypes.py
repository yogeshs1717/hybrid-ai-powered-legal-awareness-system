"""Enrich knowledge base with benchmark prototypes across English, Kannada, Hindi, Kanglish, Hinglish."""

import json
from pathlib import Path

KB_FILE = Path("knowledge_base/issue_mappings.json")

NEW_PROTOTYPES = {
    "rbi_zero_liability_unauthorized_transaction": [
        "Money was deducted from my bank account in an unauthorized transaction without my permission or sharing any OTP.",
        "ನನ್ನ ಅನುಮತಿ ಅಥವಾ ಯಾವುದೇ ಒಟಿಪಿ ಹಂಚಿಕೊಳ್ಳದೆ ನನ್ನ ಬ್ಯಾಂಕ್ ಖಾತೆಯಿಂದ ಅನಧಿಕೃತವಾಗಿ ಹಣ ಕಡಿತವಾಗಿದೆ.",
        "मेरी अनुमति या कोई ओटीपी साझा किए बिना मेरे बैंक खाते से अनधिकृत तरीके से पैसे काट लिए गए।",
        "Nanna bank account inda permission illade athava yavude OTP share madade unauthorized debit aagide.",
        "Mere bank account se bina meri permission ya koi OTP share kiye unauthorized debit ho gaya hai."
    ],
    "defective_product": [
        "The brand new refrigerator I purchased was delivered with a broken compressor, and the company refuses refund or replacement.",
        "The home appliance or refrigerator was delivered in broken condition with compressor defect and seller denies refund.",
        "ನಾನು ಖರೀದಿಸಿದ ಹೊಸ ರೆಫ್ರಿಜರೇಟರ್ ಮುರಿದ ಕಂಪ್ರೆಸರ್‌ನೊಂದಿಗೆ ಬಂದಿದ್ದು, ಕಂಪನಿಯು ಮರುಪಾವತಿ ಅಥವಾ ಬದಲಾವಣೆಯನ್ನು ನಿರಾಕರಿಸಿದೆ.",
        "मेरे द्वारा खरीदा गया नया फ्रिज खराब कंप्रेसर के साथ आया, और कंपनी पैसे वापस करने या बदलने से इनकार कर रही है।",
        "Hosa refrigerator purchase madidde broken compressor delivery aagide company refund athava replace madalla anthare.",
        "Naya fridge khareeda tha delivery par compressor kharab nikla seller na replace kar raha hai na refund de raha."
    ],
    "wrong_side_police_diversion_defense": [
        "I entered a one-way street because a traffic police officer in uniform directed me to take a detour due to road construction, but a camera challan was issued.",
        "One-way entry forced by police detour or road repair, traffic camera generated wrongful violation notice.",
        "ರಸ್ತೆ ಕಾಮಗಾರಿಯಿಂದಾಗಿ ಸಂಚಾರ ಪೊಲೀಸ್ ಅಧಿಕಾರಿಯ ಸೂಚನೆಯಂತೆ ಒನ್‌ವೇ ರಸ್ತೆಗೆ ಪ್ರವೇಶಿಸಿದ್ದರೂ ಕ್ಯಾಮೆರಾ ಚಲನ್ ವಿಧಿಸಲಾಗಿದೆ.",
        "ಸಂಚಾರ ಪೊಲೀಸರು ತಿರುವು ತೆಗೆದುಕೊಳ್ಳಲು ಹೇಳಿದ ಕಾರಣ ಒನ್-ವೇ ಪ್ರವೇಶಿಸಬೇಕಾಯಿತು ಆದರೂ ತಪ್ಪು ಚಲನ್ ಹಾಕಿದ್ದಾರೆ.",
        "सड़क निर्माण के कारण ड्यूटी पर तैनात ट्रैफिक पुलिस के निर्देश पर वन-वे में जाने के बावजूद कैमरा चालान कट गया।",
        "Police officer diversion instructions inda one-way enter aagidde camera challan wrongful fine.",
        "Traffic cop ne diversion diya road construction ke chakkar me one-way gaya par camera challan aa gaya."
    ],
    "two_wheeler_pillion_helmet_challan_dispute": [
        "Traffic police camera issued a fine claiming pillion rider was without helmet, but photo proof clearly shows both rider and pillion wearing helmets.",
        "Two wheeler pillion helmet dispute, camera photo evidence proves both passengers wore ISI certified helmets.",
        "ಹಿಂಬದಿ ಸವಾರ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿಲ್ಲ ಎಂದು ಸಂಚಾರ ಪೊಲೀಸರು ದಂಡ ವಿಧಿಸಿದ್ದಾರೆ, ಆದರೆ ಫೋಟೋದಲ್ಲಿ ಇಬ್ಬರೂ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿರುವುದು ಸ್ಪಷ್ಟವಾಗಿದೆ.",
        "ಟ್ರ್ಯಾಫಿಕ್ ಕ್ಯಾಮೆರಾ ಹಿಂಬದಿ ಸವಾರರಿಗೆ ಹೆಲ್ಮೆಟ್ ಇಲ್ಲ ಎಂದು ತಪ್ಪು ದಂಡ ವಿಧಿಸಿದೆ, ಆದರೆ ಇಬ್ಬರೂ ಐಎಸ್‌ಐ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿದ್ದಾರೆ.",
        "ट्रैफिक कैमरे ने पीछे बैठे व्यक्ति पर बिना हेलमेट का जुर्माना लगाया, जबकि फोटो में दोनों हेलमेट पहने साफ दिख रहे हैं।",
        "Pillion rider helmet dharisilla antha challan kottiddare aadre photo nalli rider matthe pillion ibbru helmet haakiddare.",
        "Pillion rider ke bina helmet ka challan aaya hai jabki camera photo me dono ne helmet pehna hua hai."
    ],
    "speed_trap_radar_calibration_dispute": [
        "Received an overspeeding challan claiming 95 km/h in a 60 km/h zone, but my calibrated GPS log proves my speed never exceeded 45 km/h.",
        "Challan under Section 183 for speeding on flyover, radar speed sensor was uncalibrated and faulty.",
        "60 ಕಿಮೀ ವಲಯದಲ್ಲಿ 95 ಕಿಮೀ ವೇಗದಲ್ಲಿ ಚಲಿಸಿದ್ದೇನೆ ಎಂದು ಅತಿವೇಗ ಚಲನ್ ಬಂದಿದೆ, ಆದರೆ ನನ್ನ ಜಿಪಿಎಸ್ ವೇಗ 45 ಕಿಮೀ ಮೀರಿಲ್ಲ ಎಂದು ತೋರಿಸುತ್ತದೆ.",
        "ನನ್ನ ವಾಹನದಲ್ಲಿ 80 ಕಿಮೀ ವೇಗದ ಮಿತಿ ಇದ್ದರೂ 95 ಕಿಮೀ ವೇಗದಲ್ಲಿ ಚಲಾಯಿಸಲಾಗಿದೆ ಎಂದು ಪೊಲೀಸರು ಸುಳ್ಳು ಅತಿವೇಗದ ಚಲನ್ ಹಾಕಿದ್ದಾರೆ.",
        "60 किमी की सीमा वाले क्षेत्र में 95 किमी की गति का ओवरस्पीडिंग चालान भेजा गया, जबकि जीपीएस लॉग के अनुसार गति 45 किमी ही थी।",
        "गाड़ी में स्पीड गवर्नर होने के बावजूद ट्रैफिक पुलिस ने रडार गन की खराबी से ओवरस्पीडिंग का गलत चालान काट दिया।",
        "Overspeeding challan 95 kmph antha claim madidare aadre nan vehicle GPS log 45 kmph cross madilla radar calibration issue.",
        "Speed camera ne 95 kmph ka overspeeding challan bhej diya jabki meri gaadi ki speed GPS me 45 kmph hi thi."
    ],
    "qr_code_fraud": [
        "A buyer on OLX asked me to scan a QR code to receive money, but as soon as I scanned it, money was debited from my UPI.",
        "OLX buyer sent a QR code to receive payment, scanned the code and funds were debited from bank account.",
        "ಒಎಲ್‌ಎಕ್ಸ್‌ನಲ್ಲಿ ಖರೀದಿದಾರರು ಹಣ ಸ್ವೀಕರಿಸಲು ಕ್ಯೂಆರ್ ಕೋಡ್ ಸ್ಕ್ಯಾನ್ ಮಾಡಲು ಹೇಳಿದರು, ಸ್ಕ್ಯಾನ್ ಮಾಡಿದ ತಕ್ಷಣ ನನ್ನ ಯುಪಿಐನಿಂದ ಹಣ ಕಡಿತವಾಯಿತು.",
        "ओएलएक्स पर एक खरीदार ने पैसे पाने के लिए क्यूआर कोड स्कैन करने को कहा, लेकिन स्कैन करते ही मेरे यूपीआई से पैसे कट गए।",
        "OLX buyer duddu receive madoke QR scan madi antha helidru scan madi nan UPI inda duddu cut aagide.",
        "OLX buyer ne paise bhejne ke liye QR code bheja bola scan karo par scan karte hi UPI se paise kat gaye."
    ],
    "medical_negligence_deficiency": [
        "A private hospital doctor left a surgical sponge inside patient abdomen during surgery causing severe infection and emergency re-operation.",
        "Surgeon committed gross medical negligence during operation resulting in septic shock and consumer deficiency in service.",
        "ಖಾಸಗಿ ಆಸ್ಪತ್ರೆಯ ವೈದ್ಯರು ಶಸ್ತ್ರಚಿಕಿತ್ಸೆಯ ಸಮಯದಲ್ಲಿ ರೋಗಿಯ ಹೊಟ್ಟೆಯೊಳಗೆ ಸ್ಪಾಂಜ್ ಬಿಟ್ಟು ತೀವ್ರ ಸೋಂಕು ಮತ್ತು ಮರು-ಶಸ್ತ್ರಚಿಕಿತ್ಸೆಗೆ ಕಾರಣರಾಗಿದ್ದಾರೆ.",
        "ನಿಜವಾದ ಆಸ್ಪತ್ರೆಯ ವೈದ್ಯರ ನಿರ್ಲಕ್ಷ್ಯದಿಂದಾಗಿ ರೋಗಿಗೆ ತೀವ್ರ ತೊಂದರೆಯಾಗಿದ್ದು ಶಸ್ತ್ರಚಿಕಿತ್ಸೆಯಲ್ಲಿ ಲೋಪವಾಗಿದೆ.",
        "निजी अस्पताल के डॉक्टर ने सर्जरी के दौरान मरीज के पेट में सर्जिकल स्पंज छोड़ दिया जिससे गंभीर संक्रमण हो गया।",
        "Private hospital doctor surgery maduvaaga sponge stomach olage bittu infection aagi emergency re-operation aagide.",
        "Private hospital me doctor ne surgery ke waqt pet me sponge chhod diya severe infection hua medical negligence."
    ],
    "educational_course_bait_and_switch_placement_guarantee": [
        "A coaching institute promised 100% money back job placement guarantee in television ads but refused refund when no placement was provided.",
        "Coaching center falsely advertised guaranteed government job placement and refused fees refund.",
        "ಕೋಚಿಂಗ್ ಸಂಸ್ಥೆಯು ಟಿವಿ ಜಾಹೀರಾತುಗಳಲ್ಲಿ 100% ಉದ್ಯೋಗ ಅಥವಾ ಹಣ ವಾಪಸ್ ಭರವಸೆ ನೀಡಿ ಉದ್ಯೋಗ ಸಿಗದಿದ್ದಾಗ ಮರುಪಾವತಿ ನಿರಾಕರಿಸಿದೆ.",
        "ಉದ್ಯೋಗ ಭರವಸೆ ನೀಡಿದ ಕೋಚಿಂಗ್ ಸಂಸ್ಥೆ ಯಾವುದೇ ಉದ್ಯೋಗ ನೀಡದೆ ಲಕ್ಷಾಂತರ ಶುಲ್ಕ ಮರುಪಾವತಿಸಲು ನಿರಾಕರಿಸಿದೆ.",
        "कोचिंग संस्थान ने विज्ञापनों में 100% नौकरी या पैसे वापसी की गारंटी दी थी लेकिन नौकरी न मिलने पर रिफंड देने से मना कर दिया।",
        "Coaching institute ads nalli 100% job placement guarantee kottidru placement agilla refund kooda kodalla anthare.",
        "Coaching institute ne 100% placement guarantee ka jhootha ad dikhaya par job nahi mili aur refund bhi reject kar diya."
    ],
    "unilateral_laptop_damage_deduction_exit": [
        "My company deducted Rs 8000 from my salary for laptop maintenance without my consent or any clause in the contract.",
        "Employer arbitrarily deducted asset or laptop maintenance from salary settlement without authorization.",
        "ನನ್ನ ಒಪ್ಪಂದದಲ್ಲಿ ಯಾವುದೇ ಷರತ್ತು ಇಲ್ಲದಿದ್ದರೂ ಮತ್ತು ನನ್ನ ಒಪ್ಪಿಗೆಯಿಲ್ಲದೆ ಕಂಪನಿಯು ಲ್ಯಾಪ್‌ಟಾಪ್ ನಿರ್ವಹಣೆಗಾಗಿ ವೇತನದಿಂದ 8000 ಕಡಿತ ಮಾಡಿದೆ.",
        "ಕಂಪನಿಯು ಅನುಮತಿಯಿಲ್ಲದೆ ಅಂತಿಮ ಇತ್ಯರ್ಥದಲ್ಲಿ ಲ್ಯಾಪ್‌ಟಾಪ್ ಸವೆತಕ್ಕಾಗಿ ವೇತನದಿಂದ ಅಕ್ರಮವಾಗಿ ಹಣ ಮುರಿದುಕೊಂಡಿದೆ.",
        "कंपनी ने बिना मेरी सहमति के और अनुबंध में कोई शर्त न होने पर भी लैपटॉप मेंटेनेंस के नाम पर सैलरी से 8000 काट लिए।",
        "Company nan consent illade laptop maintenance antha salary inda 8000 illegal deduction madiddare.",
        "Bina kisi agreement ya consent ke company ne laptop maintenance ke naam par salary se 8000 kaat liye."
    ],
    "advance_booking_token_money_forfeiture": [
        "A banquet hall management arbitrarily forfeited my Rs 50000 advance booking deposit after event cancellation due to a family medical emergency.",
        "Marriage hall or venue operator refused refund and forfeited advance token money despite timely cancellation.",
        "ಕುಟುಂಬದ ವೈದ್ಯಕೀಯ ತುರ್ತುಸ್ಥಿತಿಯಿಂದ ಕಾರ್ಯಕ್ರಮ ರದ್ದುಗೊಳಿಸಿದ ನಂತರ ಕಲ್ಯಾಣ ಮಂಟಪದವರು ನನ್ನ 50000 ಮುಂಗಡ ಠೇವಣಿಯನ್ನು ಅಕ್ರಮವಾಗಿ ಮುಟ್ಟುಗೋಲು ಹಾಕಿಕೊಂಡಿದ್ದಾರೆ.",
        "ಕಾರ್ಯಕ್ರಮ ರದ್ದಾದ ಕಾರಣ ಕಲ್ಯಾಣ ಮಂಟಪದ ಮುಂಗಡ ಹಣವನ್ನು ಯಾವುದೇ ನಷ್ಟವಿಲ್ಲದಿದ್ದರೂ ಅಕ್ರಮವಾಗಿ ಮುಟ್ಟುಗೋಲು ಹಾಕಿಕೊಳ್ಳಲಾಗಿದೆ.",
        "मेडिकल इमरजेंसी के कारण कार्यक्रम रद्द होने पर बैंक्वेट हॉल प्रबंधन ने मनमाने ढंग से मेरी 50000 की एडवांस बुकिंग जब्त कर ली।",
        "Medical emergency inda event cancel madidde banquet hall 50000 advance booking deposit forfeit madiddare Section 74 penalty.",
        "Medical emergency me function cancel kiya to banquet hall ne bina nuksan ke mera 50000 advance forfeit kar liya."
    ]
}

def main():
    with open(KB_FILE, encoding="utf-8") as f:
        kb = json.load(f)

    updated_count = 0
    for issue_id, protos in NEW_PROTOTYPES.items():
        if issue_id in kb["issues"]:
            existing = set(kb["issues"][issue_id].get("prototype_texts", []))
            for p in protos:
                if p not in existing:
                    kb["issues"][issue_id]["prototype_texts"].append(p)
                    existing.add(p)
                    updated_count += 1

    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, indent=2, ensure_ascii=False)

    print(f"Added {updated_count} prototypes to {len(NEW_PROTOTYPES)} issues.")

if __name__ == "__main__":
    main()
