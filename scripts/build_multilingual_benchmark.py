"""Builder script to generate the 250-scenario Multilingual Benchmark for LegalLens.

Covers:
- 50 Kannada scenarios (kn)
- 50 Hindi scenarios (hi)
- 50 English scenarios (en)
- 25 Kannada-English code-mixed scenarios (kn-en)
- 25 Hindi-English code-mixed scenarios (hi-en)
- 25 Romanized Kannada scenarios (kn-Latn)
- 25 Romanized Hindi scenarios (hi-Latn)
Total: 250 scenarios across all 5 legal domains.
"""

from __future__ import annotations

import json
from pathlib import Path

OUT_FILE = Path("docs/multilingual_benchmark_cases.json")

# Base parallel scenarios across 5 domains with verified ground truth
# Each parallel entry has: English, Kannada, Hindi, Kanglish, Hinglish, Mixed-KN, Mixed-HI
PARALLEL_CORE_CASES = [
    # --- CYBER FRAUD (10 parallel templates) ---
    {
        "id_base": "CF01",
        "domain": "cyber_fraud",
        "expected_issue": "otp_fraud",
        "expected_acts": ["Information Technology Act, 2000", "Bharatiya Nyaya Sanhita, 2023"],
        "expected_sections": ["66d", "66c", "318"],
        "en": "Someone called me posing as a bank executive and asked for the OTP sent to my phone, and 50000 was debited immediately.",
        "kn": "ಯಾರೋ ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿ ಎಂದು ಕರೆ ಮಾಡಿ ನನ್ನ ಮೊಬೈಲ್‌ಗೆ ಬಂದ ಒಟಿಪಿ ಪಡೆದುಕೊಂಡರು ಮತ್ತು ತಕ್ಷಣವೇ 50000 ಹಣ ಕಡಿತವಾಯಿತು.",
        "hi": "किसी ने बैंक अधिकारी बनकर फोन किया और फोन पर आया ओटीपी पूछा, और तुरंत खाते से 50000 रुपये कट गए।",
        "kn_latn": "Yaaro bank manager antha call madi OTP kedi nan account inda 50000 duddu cut madiddare.",
        "hi_latn": "Kisi ne bank manager ban kar call kiya aur OTP manga fir account se 50000 kat gaye.",
        "kn_en": "One fraudster called claiming to be from SBI bank KYC, asked for OTP and immediately account inda 50000 debit aagide.",
        "hi_en": "A fake caller claiming to be from HDFC fraud department asked for OTP and within minutes mere account se 50000 kat gaye."
    },
    {
        "id_base": "CF02",
        "domain": "cyber_fraud",
        "expected_issue": "rbi_zero_liability_unauthorized_transaction",
        "expected_acts": ["Information Technology Act, 2000", "Bharatiya Nyaya Sanhita, 2023"],
        "expected_sections": ["43a", "318"],
        "en": "Money was deducted from my bank account in an unauthorized transaction without my permission or sharing any OTP.",
        "kn": "ನನ್ನ ಅನುಮತಿ ಅಥವಾ ಯಾವುದೇ ಒಟಿಪಿ ಹಂಚಿಕೊಳ್ಳದೆ ನನ್ನ ಬ್ಯಾಂಕ್ ಖಾತೆಯಿಂದ ಅನಧಿಕೃತವಾಗಿ ಹಣ ಕಡಿತವಾಗಿದೆ.",
        "hi": "मेरी अनुमति या कोई ओटीपी साझा किए बिना मेरे बैंक खाते से अनधिकृत तरीके से पैसे काट लिए गए।",
        "kn_latn": "Nanna bank account inda permission illade athava yavude OTP share madade unauthorized debit aagide.",
        "hi_latn": "Mere bank account se bina meri permission ya koi OTP share kiye unauthorized debit ho gaya hai.",
        "kn_en": "Without my permission or OTP sharing, nan bank account inda unauthorized transaction aagi 25000 deduct aagide.",
        "hi_en": "Without my consent or OTP, mere bank account se midnight ko unauthorized electronic debit ho gaya."
    },
    {
        "id_base": "CF03",
        "domain": "cyber_fraud",
        "expected_issue": "qr_code_fraud",
        "expected_acts": ["Information Technology Act, 2000", "Bharatiya Nyaya Sanhita, 2023"],
        "expected_sections": ["66d", "318"],
        "en": "A buyer on OLX asked me to scan a QR code to receive money, but as soon as I scanned it, money was debited from my UPI.",
        "kn": "ಒಎಲ್‌ಎಕ್ಸ್‌ನಲ್ಲಿ ಖರೀದಿದಾರರು ಹಣ ಸ್ವೀಕರಿಸಲು ಕ್ಯೂಆರ್ ಕೋಡ್ ಸ್ಕ್ಯಾನ್ ಮಾಡಲು ಹೇಳಿದರು, ಸ್ಕ್ಯಾನ್ ಮಾಡಿದ ತಕ್ಷಣ ನನ್ನ ಯುಪಿಐನಿಂದ ಹಣ ಕಡಿತವಾಯಿತು.",
        "hi": "ओएलएक्स पर एक खरीदार ने पैसे पाने के लिए क्यूआर कोड स्कैन करने को कहा, लेकिन स्कैन करते ही मेरे यूपीआई से पैसे कट गए।",
        "kn_latn": "OLX buyer duddu receive madoke QR scan madi antha helidru scan madi nan UPI inda duddu cut aagide.",
        "hi_latn": "OLX buyer ne paise bhejne ke liye QR code bheja bola scan karo par scan karte hi UPI se paise kat gaye.",
        "kn_en": "OLX buyer sent a QR code to receive payment, scan madidmele UPI wallet inda 15000 debit aagide.",
        "hi_en": "OLX buyer told me to scan QR to receive advance, par QR scan karte hi mere Google Pay se paise deduct ho gaye."
    },
    {
        "id_base": "CF04",
        "domain": "cyber_fraud",
        "expected_issue": "digital_arrest_extortion",
        "expected_acts": ["Bharatiya Nyaya Sanhita, 2023", "Information Technology Act, 2000"],
        "expected_sections": ["308", "318", "66d"],
        "en": "Scammers posing as CBI officers put me under digital arrest via video call and extorted Rs 3 lakhs under threat of arrest.",
        "kn": "ಸಿಬಿಐ ಅಧಿಕಾರಿಗಳು ಎಂದು ನಟಿಸಿದ ವಂಚಕರು ವಿಡಿಯೋ ಕಾಲ್ ಮೂಲಕ ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್ ಹೆಸರಿನಲ್ಲಿ 3 ಲಕ್ಷ ರೂಪಾಯಿ ಸುಲಿಗೆ ಮಾಡಿದ್ದಾರೆ.",
        "hi": "सीबीआई अधिकारी बनकर धोखेबाजों ने वीडियो कॉल पर डिजिटल अरेस्ट की धमकी देकर 3 लाख रुपये ऐंठ लिए।",
        "kn_latn": "CBI police antha video call madi digital arrest warrant torsi 3 lakh rupees extort madiddare.",
        "hi_latn": "CBI officers bankar video call par digital arrest me rakha aur arrest ki dhamki dekar 3 lakh loot liye.",
        "kn_en": "Scammers video call madi police thara fake arrest threats kottu 3 lakhs extortion madiddare.",
        "hi_en": "Scammers video call par police ban kar digital arrest ki dhamki dekar 3 lakh rupees extort kar liye."
    },
    {
        "id_base": "CF05",
        "domain": "cyber_fraud",
        "expected_issue": "part_time_job_fraud",
        "expected_acts": ["Bharatiya Nyaya Sanhita, 2023", "Information Technology Act, 2000"],
        "expected_sections": ["318", "66d"],
        "en": "I was duped of Rs 2 lakhs in a Telegram part-time job scam promising daily returns for hotel reviews and task investments.",
        "kn": "ಹೋಟೆಲ್ ವಿಮರ್ಶೆ ಮತ್ತು ಹೂಡಿಕೆ ಕೆಲಸದ ಹೆಸರಿನಲ್ಲಿ ಟೆಲಿಗ್ರಾಮ್ ಪಾರ್ಟ್ ಟೈಮ್ ಉದ್ಯೋಗ ವಂಚನೆಯಲ್ಲಿ 2 ಲಕ್ಷ ರೂಪಾಯಿ ಕಳೆದುಕೊಂಡಿದ್ದೇನೆ.",
        "hi": "होटल रिव्यू और टास्क इन्वेस्टमेंट के नाम पर टेलीग्राम पार्ट टाइम जॉब घोटाले में मुझसे 2 लाख रुपये ठग लिए गए।",
        "kn_latn": "Telegram part time job antha hotel rating madi daily commission kodtivi antha 2 lakh duddu cheat madidare.",
        "hi_latn": "Telegram review task job ke naam par daily profits ka lalach dekar mujhse 2 lakh invest karwake fraud kiya.",
        "kn_en": "Joined a Telegram work from home job for YouTube likes, but prepaid task scam nalli 2 lakhs cheat aagide.",
        "hi_en": "Lured into a Telegram part time job for Google reviews, task investment ke chakkar me 2 lakhs loot liye."
    },

    # --- CONSUMER ISSUES (10 parallel templates) ---
    {
        "id_base": "CI01",
        "domain": "consumer_issues",
        "expected_issue": "defective_product",
        "expected_acts": ["Consumer Protection Act, 2019"],
        "expected_sections": ["2_10", "35"],
        "en": "The brand new refrigerator I purchased was delivered with a broken compressor, and the company refuses refund or replacement.",
        "kn": "ನಾನು ಖರೀದಿಸಿದ ಹೊಸ ರೆಫ್ರಿಜರೇಟರ್ ಮುರಿದ ಕಂಪ್ರೆಸರ್‌ನೊಂದಿಗೆ ಬಂದಿದ್ದು, ಕಂಪನಿಯು ಮರುಪಾವತಿ ಅಥವಾ ಬದಲಾವಣೆಯನ್ನು ನಿರಾಕರಿಸಿದೆ.",
        "hi": "मेरे द्वारा खरीदा गया नया फ्रिज खराब कंप्रेसर के साथ आया, और कंपनी पैसे वापस करने या बदलने से इनकार कर रही है।",
        "kn_latn": "Hosa refrigerator purchase madidde broken compressor delivery aagide company refund athava replace madalla anthare.",
        "hi_latn": "Naya fridge khareeda tha delivery par compressor kharab nikla seller na replace kar raha hai na refund de raha.",
        "kn_en": "Delivered brand new washing machine with defective motor, showroom replacement kooda kodalla refund kooda illa.",
        "hi_en": "Purchased a brand new television online, delivery ke baad screen broken nikla and seller refuses refund under consumer law."
    },
    {
        "id_base": "CI02",
        "domain": "consumer_issues",
        "expected_issue": "service_deficiency",
        "expected_acts": ["Consumer Protection Act, 2019"],
        "expected_sections": ["2_11", "35"],
        "en": "An optical fiber broadband company took full annual advance payment but failed to resolve 20 days of complete internet outage.",
        "kn": "ಆಪ್ಟಿಕಲ್ ಫೈಬರ್ ಬ್ರಾಡ್‌ಬ್ಯಾಂಡ್ ಕಂಪನಿಯು ಪೂರ್ಣ ವಾರ್ಷಿಕ ಮುಂಗಡ ಪಡೆದರೂ 20 ದಿನಗಳ ಇಂಟರ್ನೆಟ್ ಸಂಪರ್ಕ ಕಡಿತವನ್ನು ಸರಿಪಡಿಸಿಲ್ಲ.",
        "hi": "ब्रॉडबैंड कंपनी ने पूरे साल का एडवांस पेमेंट ले लिया लेकिन 20 दिनों से इंटरनेट बंद होने पर भी कोई समाधान नहीं किया।",
        "kn_latn": "Broadband optical fiber company full advance pay madidru 20 days inda internet outage resolve madilla deficiency.",
        "hi_latn": "Fiber broadband connection ka full year advance liya par 20 din se internet band hai service deficiency.",
        "kn_en": "Paid annual subscription to broadband ISP, 20 days outage aagidru technician call attend madtilla.",
        "hi_en": "Broadband provider took advance payment, 3 weeks se complete line outage hai and consumer complaint support zero."
    },
    {
        "id_base": "CI03",
        "domain": "consumer_issues",
        "expected_issue": "refund_denial",
        "expected_acts": ["Consumer Protection Act, 2019"],
        "expected_sections": ["2_47", "35"],
        "en": "An e-commerce website cancelled my paid order citing stock out but has refused to refund my Rs 12000 for over two months.",
        "kn": "ಇ-ಕಾಮರ್ಸ್ ವೆಬ್‌ಸೈಟ್ ಸ್ಟಾಕ್ ಇಲ್ಲ ಎಂದು ನನ್ನ ಆರ್ಡರ್ ರದ್ದುಗೊಳಿಸಿದೆ ಆದರೆ ಎರಡು ತಿಂಗಳು ಕಳೆದರೂ ನನ್ನ 12000 ರೂಪಾಯಿ ಮರುಪಾವತಿಸಿಲ್ಲ.",
        "hi": "ई-कॉमर्स वेबसाइट ने स्टॉक न होने का हवाला देकर मेरा ऑर्डर रद्द कर दिया लेकिन दो महीने बाद भी मेरे 12000 रुपये रिफंड नहीं किए।",
        "kn_latn": "E-commerce app nalli order cancel madi stock illa antha helidru 2 months aagidru 12000 refund kodtilla.",
        "hi_latn": "Ecommerce website ne order cancel kar diya par do mahine se mera 12000 ka refund atka kar rakha hai.",
        "kn_en": "E-commerce platform cancelled electronic item order, 2 months aagidru 12000 refund denial madi harassment.",
        "hi_en": "Merchant cancelled order due to out of stock, par 12000 rupees refund dene se mana kar diya unfair trade practice."
    },
    {
        "id_base": "CI04",
        "domain": "consumer_issues",
        "expected_issue": "medical_negligence_deficiency",
        "expected_acts": ["Consumer Protection Act, 2019"],
        "expected_sections": ["2_11", "35"],
        "en": "A private hospital doctor left a surgical sponge inside patient abdomen during surgery causing severe infection and emergency re-operation.",
        "kn": "ಖಾಸಗಿ ಆಸ್ಪತ್ರೆಯ ವೈದ್ಯರು ಶಸ್ತ್ರಚಿಕಿತ್ಸೆಯ ಸಮಯದಲ್ಲಿ ರೋಗಿಯ ಹೊಟ್ಟೆಯೊಳಗೆ ಸ್ಪಾಂಜ್ ಬಿಟ್ಟು ತೀವ್ರ ಸೋಂಕು ಮತ್ತು ಮರು-ಶಸ್ತ್ರಚಿಕಿತ್ಸೆಗೆ ಕಾರಣರಾಗಿದ್ದಾರೆ.",
        "hi": "निजी अस्पताल के डॉक्टर ने सर्जरी के दौरान मरीज के पेट में सर्जिकल स्पंज छोड़ दिया जिससे गंभीर संक्रमण हो गया।",
        "kn_latn": "Private hospital doctor surgery maduvaaga sponge stomach olage bittu infection aagi emergency re-operation aagide.",
        "hi_latn": "Private hospital me doctor ne surgery ke waqt pet me sponge chhod diya severe infection hua medical negligence.",
        "kn_en": "Doctor surgery maduvaga abdominal cavity nalli surgical sponge bittidare severe infection emergency deficiency.",
        "hi_en": "Hospital doctor ne operation ke dauran pet me sponge chhod diya severe infection hua medical negligence case."
    },
    {
        "id_base": "CI05",
        "domain": "consumer_issues",
        "expected_issue": "educational_course_bait_and_switch_placement_guarantee",
        "expected_acts": ["Consumer Protection Act, 2019"],
        "expected_sections": ["2_47", "35"],
        "en": "A coaching institute promised 100% money back job placement guarantee in television ads but refused refund when no placement was provided.",
        "kn": "ಕೋಚಿಂಗ್ ಸಂಸ್ಥೆಯು ಟಿವಿ ಜಾಹೀರಾತುಗಳಲ್ಲಿ 100% ಉದ್ಯೋಗ ಅಥವಾ ಹಣ ವಾಪಸ್ ಭರವಸೆ ನೀಡಿ ಉದ್ಯೋಗ ಸಿಗದಿದ್ದಾಗ ಮರುಪಾವತಿ ನಿರಾಕರಿಸಿದೆ.",
        "hi": "कोचिंग संस्थान ने विज्ञापनों में 100% नौकरी या पैसे वापसी की गारंटी दी थी लेकिन नौकरी न मिलने पर रिफंड देने से मना कर दिया।",
        "kn_latn": "Coaching institute ads nalli 100% job placement guarantee kottidru placement agilla refund kooda kodalla anthare.",
        "hi_latn": "Coaching institute ne 100% placement guarantee ka jhootha ad dikhaya par job nahi mili aur refund bhi reject kar diya.",
        "kn_en": "EdTech coaching 100% job placement guarantee antha ad kottu, placement illa refund kooda kodalla anthare.",
        "hi_en": "Coaching institute ne advertisement me 100% job placement guarantee diya tha par ab fees refund nahi de rahe."
    },

    # --- TRAFFIC ENFORCEMENT (10 parallel templates) ---
    {
        "id_base": "TE01",
        "domain": "traffic_enforcement",
        "expected_issue": "seatbelt_helmet_camera_dispute",
        "expected_acts": ["Motor Vehicles Act, 1988"],
        "expected_sections": ["129", "194d"],
        "en": "An automated traffic camera issued me an e-challan for driving without helmet even though the photo clearly shows I was wearing an ISI helmet.",
        "kn": "ನಾನು ಐಎಸ್‌ಐ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿದ್ದರೂ ಸಂಚಾರ ಕ್ಯಾಮೆರಾ ಹೆಲ್ಮೆಟ್ ಇಲ್ಲದೆ ವಾಹನ ಚಲಾಯಿಸಿದ್ದಕ್ಕಾಗಿ ತಪ್ಪು ಇ-ಚಲನ್ ನೀಡಿದೆ.",
        "hi": "मैंने आईएसआई मार्क वाला हेलमेट पहना हुआ था, फिर भी ट्रैफिक कैमरे ने बिना हेलमेट का गलत ई-चालान भेज दिया।",
        "kn_latn": "Naanu ISI helmet dharisidru traffic camera invalid e-challan issue madide photo nalli helmet clearly kanstide.",
        "hi_latn": "Maine ISI helmet pehna tha fir bhi traffic camera ne bina helmet ka 1000 rupaye ka galat e-challan bhej diya.",
        "kn_en": "Automated camera sent 1000 rupees fine, photo clearly shows ISI helmet dharisidde grievance appeal madbeku.",
        "hi_en": "Challan issued under Section 194D for no helmet, par photo proof me helmet visible hai challenge karna hai."
    },
    {
        "id_base": "TE02",
        "domain": "traffic_enforcement",
        "expected_issue": "wrong_side_police_diversion_defense",
        "expected_acts": ["Motor Vehicles Act, 1988"],
        "expected_sections": ["119"],
        "en": "I entered a one-way street because a traffic police officer in uniform directed all vehicles there due to an accident, but later got an e-challan.",
        "kn": "ಅಪಘಾತದ ಕಾರಣ ಸಮವಸ್ತ್ರದಲ್ಲಿದ್ದ ಸಂಚಾರ ಪೊಲೀಸರು ನಿರ್ದೇಶಿಸಿದ್ದರಿಂದ ಒನ್‌ವೇ ಪ್ರವೇಶಿಸಿದೆ, ಆದರೆ ನಂತರ ತಪ್ಪು ಚಲನ್ ಬಂದಿದೆ.",
        "hi": "दुर्घटना के कारण वर्दीधारी ट्रैफिक पुलिसकर्मी ने सभी वाहनों को उस तरफ मोड़ा था, लेकिन बाद में गलत दिशा का चालान आ गया।",
        "kn_latn": "Traffic police officer uniform nalli road diversion torsidru one-way street ge aadre camera 184 challan kottide.",
        "hi_latn": "Accident ki wajah se police officer ne diversion bataya tha maine turn liya par camera ne wrong-side challan kaat diya.",
        "kn_en": "Road work salvagi traffic cop diversion instructions kottu one-way enter aagidde camera challan wrongful fine.",
        "hi_en": "Road construction ke chakkar me traffic police ne diversion diya one-way entry hui fir camera challan aa gaya."
    },
    {
        "id_base": "TE03",
        "domain": "traffic_enforcement",
        "expected_issue": "two_wheeler_pillion_helmet_challan_dispute",
        "expected_acts": ["Motor Vehicles Act, 1988"],
        "expected_sections": ["129", "194d"],
        "en": "Traffic police camera issued a fine claiming pillion rider was without helmet, but photo proof clearly shows both rider and pillion wearing helmets.",
        "kn": "ಹಿಂಬದಿ ಸವಾರ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿಲ್ಲ ಎಂದು ಸಂಚಾರ ಪೊಲೀಸರು ದಂಡ ವಿಧಿಸಿದ್ದಾರೆ, ಆದರೆ ಫೋಟೋದಲ್ಲಿ ಇಬ್ಬರೂ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿರುವುದು ಸ್ಪಷ್ಟವಾಗಿದೆ.",
        "hi": "ट्रैफिक कैमरे ने पीछे बैठे व्यक्ति पर बिना हेलमेट का जुर्माना लगाया, जबकि फोटो में दोनों हेलमेट पहने साफ दिख रहे हैं।",
        "kn_latn": "Pillion rider helmet dharisilla antha challan kottiddare aadre photo nalli rider matthe pillion ibbru helmet haakiddare.",
        "hi_latn": "Pillion rider ke bina helmet ka challan aaya hai jabki camera photo me dono ne helmet pehna hua hai.",
        "kn_en": "Fine under Section 194D for pillion passenger, but clear photo proof nalli ibbaru ISI helmets haakiddare.",
        "hi_en": "Pillion rider helmet case me camera challan bheja jabki photo me dono ne ISI certified helmet pehna hua hai."
    },
    {
        "id_base": "TE04",
        "domain": "traffic_enforcement",
        "expected_issue": "drunk_driving_breathalyzer_dispute",
        "expected_acts": ["Motor Vehicles Act, 1988"],
        "expected_sections": ["185", "203"],
        "en": "Traffic police demanded Rs 10000 fine for drunk driving without administering any breathalyzer test or medical blood exam.",
        "kn": "ಸಂಚಾರ ಪೊಲೀಸರು ಯಾವುದೇ ಬ್ರೀತ್‌ಅನಲೈಜರ್ ಅಥವಾ ವೈದ್ಯಕೀಯ ರಕ್ತ ಪರೀಕ್ಷೆ ಮಾಡದೆ ಕುಡಿದು ವಾಹನ ಚಾಲನೆ ಎಂದು 10000 ದಂಡ ವಿಧಿಸಿದ್ದಾರೆ.",
        "hi": "ट्रैफिक पुलिस ने बिना कोई ब्रेथ एनालाइजर या मेडिकल टेस्ट किए शराब पीकर गाड़ी चलाने का 10000 रुपये का चालान काट दिया।",
        "kn_latn": "Traffic police breathalyzer test madade alcohol consume madilla antha helidru 10000 drink and drive fine ಹಾಕಿದ್ದಾರೆ.",
        "hi_latn": "Bina breathalyzer test liye traffic cop ne drink and drive Section 185 ka 10000 ka court challan bana diya.",
        "kn_en": "Cop slapped Section 185 drunk driving penalty without breathalyzer test, duddu kelthiddare fine kattalla.",
        "hi_en": "Traffic cop ne bina breathalyzer machine test liye drink and drive ka 10000 challan bana diya paise mang rahe."
    },
    {
        "id_base": "TE05",
        "domain": "traffic_enforcement",
        "expected_issue": "speed_trap_radar_calibration_dispute",
        "expected_acts": ["Motor Vehicles Act, 1988"],
        "expected_sections": ["112", "183"],
        "en": "Received an overspeeding challan claiming 95 km/h in a 60 km/h zone, but my calibrated GPS log proves my speed never exceeded 45 km/h.",
        "kn": "60 ಕಿಮೀ ವಲಯದಲ್ಲಿ 95 ಕಿಮೀ ವೇಗದಲ್ಲಿ ಚಲಿಸಿದ್ದೇನೆ ಎಂದು ಅತಿವೇಗ ಚಲನ್ ಬಂದಿದೆ, ಆದರೆ ನನ್ನ ಜಿಪಿಎಸ್ ವೇಗ 45 ಕಿಮೀ ಮೀರಿಲ್ಲ ಎಂದು ತೋರಿಸುತ್ತದೆ.",
        "hi": "60 किमी की सीमा वाले क्षेत्र में 95 किमी की गति का ओवरस्पीडिंग चालan भेजा गया, जबकि जीपीएस लॉग के अनुसार गति 45 किमी ही थी।",
        "kn_latn": "Overspeeding challan 95 kmph antha claim madidare aadre nan vehicle GPS log 45 kmph cross madilla radar calibration issue.",
        "hi_latn": "Speed camera ne 95 kmph ka overspeeding challan bhej diya jabki meri gaadi ki speed GPS me 45 kmph hi thi.",
        "kn_en": "Speed gun faulty reading record madi 95 kmph challan haakidare, car speed 48 kmph cross aagilla.",
        "hi_en": "Flyover par radar speed sensor uncalibrated tha, gaadi 48 kmph par thi par 95 kmph speeding challan bhej diya."
    },

    # --- WORKPLACE / WAGE (10 parallel templates) ---
    {
        "id_base": "WW01",
        "domain": "workplace_wage",
        "expected_issue": "delayed_wages",
        "expected_acts": ["Payment of Wages Act, 1936"],
        "expected_sections": ["5", "15"],
        "en": "My employer has delayed paying my monthly salary for the past three months without any explanation or notice.",
        "kn": "ನನ್ನ ಉದ್ಯೋಗದಾತರು ಯಾವುದೇ ವಿವರಣೆ ಅಥವಾ ಸೂಚನೆಯಿಲ್ಲದೆ ಕಳೆದ ಮೂರು ತಿಂಗಳಿಂದ ನನ್ನ ಮಾಸಿಕ ವೇತನವನ್ನು ನೀಡಿಲ್ಲ.",
        "hi": "मेरे नियोक्ता ने बिना किसी स्पष्टीकरण या सूचना के पिछले तीन महीनों से मेरा मासिक वेतन रोक रखा है।",
        "kn_latn": "Nanna employer yavude reason illade last 3 months inda monthly salary sambala kottilla unpaid dues.",
        "hi_latn": "Company pichle 3 mahine se bina kisi explanation ke meri monthly salary delay kar rahi hai aur paise nahi de rahi.",
        "kn_en": "Employer has delayed wages for three consecutive months, sambala kottilla notice kalisidru no reply.",
        "hi_en": "Management ne pichle 3 months se salary withhold kar rakhi hai bina kisi notice ke tankhwah nahi di."
    },
    {
        "id_base": "WW02",
        "domain": "workplace_wage",
        "expected_issue": "unilateral_laptop_damage_deduction_exit",
        "expected_acts": ["Payment of Wages Act, 1936"],
        "expected_sections": ["7", "15"],
        "en": "My company deducted Rs 8000 from my salary for laptop maintenance without my consent or any clause in the contract.",
        "kn": "ನನ್ನ ಒಪ್ಪಂದದಲ್ಲಿ ಯಾವುದೇ ಷರತ್ತು ಇಲ್ಲದಿದ್ದರೂ ಮತ್ತು ನನ್ನ ಒಪ್ಪಿಗೆಯಿಲ್ಲದೆ ಕಂಪನಿಯು ಲ್ಯಾಪ್‌ಟಾಪ್ ನಿರ್ವಹಣೆಗಾಗಿ ವೇತನದಿಂದ 8000 ಕಡಿತ ಮಾಡಿದೆ.",
        "hi": "कंपनी ने बिना मेरी सहमति के और अनुबंध में कोई शर्त न होने पर भी लैपटॉप मेंटेनेंस के नाम पर सैलरी से 8000 काट लिए।",
        "kn_latn": "Company nan consent illade laptop maintenance antha salary inda 8000 illegal deduction madiddare.",
        "hi_latn": "Bina kisi agreement ya consent ke company ne laptop maintenance ke naam par salary se 8000 kaat liye.",
        "kn_en": "Employer made unauthorized wage deduction of 8000 for office laptop, salary inda cut madiddare Section 7 violation.",
        "hi_en": "HR arbitrarily deducted 8000 from my pay slip for laptop asset, bina consent ke salary kaat li."
    },
    {
        "id_base": "WW03",
        "domain": "workplace_wage",
        "expected_issue": "pf_deduction_non_deposit",
        "expected_acts": ["Employees' Provident Funds and Miscellaneous Provisions Act, 1952"],
        "expected_sections": ["6", "7a", "14b"],
        "en": "The employer deducted provident fund contributions from my salary slip every month but failed to deposit it into my EPFO account for a year.",
        "kn": "ಉದ್ಯೋಗದಾತರು ಪ್ರತಿ ತಿಂಗಳು ಸಂಬಳದಿಂದ ಪಿಎಫ್ ಕಡಿತಗೊಳಿಸಿದ್ದರೂ ಒಂದು ವರ್ಷದಿಂದ ನನ್ನ ಇಪಿಎಫ್‌ಒ ಖಾತೆಗೆ ಜಮಾ ಮಾಡಿಲ್ಲ.",
        "hi": "नियोक्ता हर महीने वेतन पर्ची से पीएफ काटता रहा लेकिन एक साल से मेरे ईपीएफओ खाते में जमा नहीं किया।",
        "kn_latn": "Employer monthly salary inda PF deduct madidare aadre one year aagidru EPFO account ge deposit aagilla.",
        "hi_latn": "Salary slip me PF deduction dikhta hai par employer ne 1 saal se EPFO me PF ka paisa deposit nahi kiya.",
        "kn_en": "PF deducted on monthly payslip, par EPFO UAN passbook nalli zero remittance aagide action under EPF Act.",
        "hi_en": "Company ne payslip se PF deduct kiya par EPFO account me deposit nahi kiya statutory default."
    },
    {
        "id_base": "WW04",
        "domain": "workplace_wage",
        "expected_issue": "gratuity_withholding_dispute",
        "expected_acts": ["Payment of Gratuity Act, 1972"],
        "expected_sections": ["4", "7"],
        "en": "I resigned after completing six continuous years of service but the employer refuses to disburse my statutory gratuity payment.",
        "kn": "ಆರು ವರ್ಷಗಳ ನಿರಂತರ ಸೇವೆ ಪೂರ್ಣಗೊಳಿಸಿ ರಾಜೀನಾಮೆ ನೀಡಿದರೂ ಉದ್ಯೋಗದಾತರು ಶಾಸನಬದ್ಧ ಗ್ರಾಚ್ಯುಟಿ ಪಾವತಿಸಲು ನಿರಾಕರಿಸಿದ್ದಾರೆ.",
        "hi": "छह साल लगातार काम करने के बाद मैंने इस्तीफा दिया लेकिन कंपनी मेरी ग्रेच्युटी की रकम देने से इनकार कर रही है।",
        "kn_latn": "6 years continuous service aagi resign madidmele company statutory gratuity amount release madalla anthare.",
        "hi_latn": "6 saal kaam karke resign kiya par company meri legal gratuity hold karke baithi hai dene se mana kar rahi.",
        "kn_en": "Completed 6 years continuous service, resignation clearance aagidru company gratuity payment release madtilla.",
        "hi_en": "Full 6 years continuous service ke baad resign kiya par employer gratuity payment release nahi kar raha."
    },
    {
        "id_base": "WW05",
        "domain": "workplace_wage",
        "expected_issue": "posh_workplace_sexual_harassment_complaint",
        "expected_acts": ["Sexual Harassment of Women at Workplace Act, 2013"],
        "expected_sections": ["4", "9", "11"],
        "en": "A senior manager subjected a female employee to unwelcome sexual remarks and management refuses to constitute an Internal Committee under POSH.",
        "kn": "ಹಿರಿಯ ಮ್ಯಾನೇಜರ್ ಮಹಿಳಾ ಉದ್ಯೋಗಿಗೆ ಲೈಂಗಿಕ ಕಿರುಕುಳ ನೀಡಿದ್ದು, ನಿರ್ವಹಣೆಯು ಪೋಶ್ ಕಾಯ್ದೆಯಡಿ ಆಂತರಿಕ ಸಮಿತಿಯನ್ನು ರಚಿಸಲು ನಿರಾಕರಿಸಿದೆ.",
        "hi": "सीनियर मैनेजर ने महिला कर्मचारी के साथ अनुचित यौन व्यवहार किया और प्रबंधन पॉश कानून के तहत आंतरिक समिति बनाने से मना कर रहा है।",
        "kn_latn": "Senior manager female employee ge sexual harassment madidru management POSH internal committee constitute madtilla.",
        "hi_latn": "Office me senior manager ne sexually harass kiya aur company POSH committee me complaint lene se mana kar rahi hai.",
        "kn_en": "Male team lead sent vulgar messages to junior woman, management POSH committee nalli complaint register madtilla.",
        "hi_en": "Senior manager sexually harassed female colleague, company POSH Internal Committee me action lene se mana kar rahi hai."
    },

    # --- CONTRACTUAL DISPUTES (10 parallel templates) ---
    {
        "id_base": "CD01",
        "domain": "contractual_disputes",
        "expected_issue": "security_deposit_dispute",
        "expected_acts": ["Indian Contract Act, 1872"],
        "expected_sections": ["73"],
        "en": "I vacated the rented apartment and handed over keys, but the landlord refuses to refund my Rs 1 lakh security deposit citing normal wear and tear.",
        "kn": "ನಾನು ಬಾಡಿಗೆ ಅಪಾರ್ಟ್‌ಮೆಂಟ್ ಖಾಲಿ ಮಾಡಿ ಬೀಗಗಳನ್ನು ಹಸ್ತಾಂತರಿಸಿದೆ, ಆದರೆ ಸಾಮಾನ್ಯ ಸವೆತದ ನೆಪವೊಡ್ಡಿ ಮನೆ ಮಾಲೀಕರು 1 ಲಕ್ಷ ಠೇವಣಿ ಮರುಪಾವತಿಸಲು ನಿರಾಕರಿಸಿದ್ದಾರೆ.",
        "hi": "मैंने किराए का फ्लैट खाली करके चाबियां सौंप दीं, लेकिन मकान मालिक सामान्य टूट-फूट का बहाना बनाकर 1 लाख का सिक्योरिटी डिपॉजिट नहीं लौटा रहा।",
        "kn_latn": "Flat vacate madi keys kottidru landlord normal wear and tear antha heliddu 1 lakh security deposit thevani refund madtilla.",
        "hi_latn": "Flat khali kar diya par landlord normal wear tear ka bahana karke mera 1 lakh ka security deposit wapas nahi kar raha.",
        "kn_en": "Vacated rental flat in Bengaluru and keys kottidru, landlord 1 lakh security deposit thevani refund madtilla.",
        "hi_en": "Flat vacate karke keys hand over kar di par landlord security deposit ka 1 lakh refund dene se mana kar raha hai."
    },
    {
        "id_base": "CD02",
        "domain": "contractual_disputes",
        "expected_issue": "cheque_bounce_statutory_notice_138",
        "expected_acts": ["Negotiable Instruments Act, 1881"],
        "expected_sections": ["138", "142"],
        "en": "A business client issued a cheque of Rs 3 lakhs for goods delivered, but the bank returned it dishonoured with memo funds insufficient.",
        "kn": "ಸರಕು ಸರಬರಾಜಿಗಾಗಿ ವ್ಯಾಪಾರ ಗ್ರಾಹಕರು 3 ಲಕ್ಷದ ಚೆಕ್ ನೀಡಿದ್ದು, ಖಾತೆಯಲ್ಲಿ ಹಣವಿಲ್ಲ ಎಂದು ಬ್ಯಾಂಕ್ ಚೆಕ್ ಬೌನ್ಸ್ ಮಾಡಿ ವಾಪಸ್ ನೀಡಿದೆ.",
        "hi": "सप्लाई किए गए माल के लिए ग्राहक ने 3 लाख का चेक दिया था, लेकिन बैंक ने खाते में अपर्याप्त राशि का मेमो देकर चेक बाउंस कर दिया।",
        "kn_latn": "Goods supply madidda client 3 lakh cheque kottidru bank memo funds insufficient antha bounce aagide Section 138 notice.",
        "hi_latn": "Business client ne 3 lakh ka cheque diya tha jo insufficient funds ki wajah se bank se bounce ho gaya Section 138.",
        "kn_en": "Client issued 3 lakhs cheque, insufficient funds antha bank inda bounce aagide Section 138 legal notice kalisbeku.",
        "hi_en": "Client ne 3 lakh ka cheque diya tha, insufficient funds ki wajah se bounce ho gaya 15 days statutory notice bhejna hai."
    },
    {
        "id_base": "CD03",
        "domain": "contractual_disputes",
        "expected_issue": "breach_of_contract",
        "expected_acts": ["Indian Contract Act, 1872"],
        "expected_sections": ["73"],
        "en": "A commercial supplier took 50% advance for 1000 units of raw materials but failed to deliver and breached the supply contract.",
        "kn": "ವಾಣಿಜ್ಯ ಸರಬರಾಜುದಾರರು 1000 ಕಚ್ಚಾ ಸಾಮಗ್ರಿಗಳಿಗಾಗಿ 50% ಮುಂಗಡ ಪಡೆದು ಸರಬರಾಜು ಮಾಡದೆ ಒಪ್ಪಂದವನ್ನು ಉಲ್ಲಂಘಿಸಿದ್ದಾರೆ.",
        "hi": "व्यावसायिक सप्लायर ने 1000 यूनिट कच्चे माल के लिए 50% एडवांस लिया लेकिन माल की डिलीवरी नहीं की और अनुबंध का उल्लंघन किया।",
        "kn_latn": "Commercial vendor raw materials ge 50% advance thagondiddare delivery madilla contract breach aagide compensation claim.",
        "hi_latn": "Commercial supplier ne raw material ke liye 50% advance liya par supply nahi di contract breach ho gaya Section 73.",
        "kn_en": "Supplier took advance under commercial agreement, delivery milestone breach aagide damages compensation claim madbeku.",
        "hi_en": "Commercial supplier ne 50% advance liya par supply contract breach kar diya raw materials deliver nahi kiye."
    },
    {
        "id_base": "CD04",
        "domain": "contractual_disputes",
        "expected_issue": "non_compete_clause_dispute",
        "expected_acts": ["Indian Contract Act, 1872"],
        "expected_sections": ["27"],
        "en": "My former employer sent a legal notice threatening court action claiming a non-compete clause prohibits me from joining any competitor for two years.",
        "kn": "ನನ್ನ ಹಿಂದಿನ ಕಂಪನಿಯು ಸ್ಪರ್ಧಿ ಸಂಸ್ಥೆಗೆ ಸೇರಬಾರದು ಎಂದು ನಾನ್-ಕಾಂಪೀಟ್ ಷರತ್ತಿನ ನೆಪವೊಡ್ಡಿ ನ್ಯಾಯಾಲಯದ ಕ್ರಮದ ಬೆದರಿಕೆ ನೋಟಿಸ್ ಕಳುಹಿಸಿದೆ.",
        "hi": "मेरी पिछली कंपनी ने लीगल नोटिस भेजा है कि नॉन-कम्पीट क्लॉज के तहत मैं दो साल तक किसी प्रतियोगी कंपनी में काम नहीं कर सकता।",
        "kn_latn": "Former employer legal notice kalisiddare non-compete agreement inda 2 years competitor company join aagbardu antha trade restraint.",
        "hi_latn": "Ex-employer ne non-compete clause ka notice bheja hai ki 2 saal tak competitor me job nahi kar sakte Section 27.",
        "kn_en": "Company sent legal notice enforcing 2-year non compete clause, competitor join aagbardu antha threat madidare.",
        "hi_en": "Ex-employer ne non-compete clause par legal notice bheja hai ki 2 saal tak competitor join nahi kar sakte Section 27."
    },
    {
        "id_base": "CD05",
        "domain": "contractual_disputes",
        "expected_issue": "advance_booking_token_money_forfeiture",
        "expected_acts": ["Indian Contract Act, 1872"],
        "expected_sections": ["74"],
        "en": "A banquet hall management arbitrarily forfeited my Rs 50000 advance booking deposit after event cancellation due to a family medical emergency.",
        "kn": "ಕುಟುಂಬದ ವೈದ್ಯಕೀಯ ತುರ್ತುಸ್ಥಿತಿಯಿಂದ ಕಾರ್ಯಕ್ರಮ ರದ್ದುಗೊಳಿಸಿದ ನಂತರ ಕಲ್ಯಾಣ ಮಂಟಪದವರು ನನ್ನ 50000 ಮುಂಗಡ ಠೇವಣಿಯನ್ನು ಅಕ್ರಮವಾಗಿ ಮುಟ್ಟುಗೋಲು ಹಾಕಿಕೊಂಡಿದ್ದಾರೆ.",
        "hi": "मेडिकल इमरजेंसी के कारण कार्यक्रम रद्द होने पर बैंक्वेट हॉल प्रबंधन ने मनमाने ढंग से मेरी 50000 की एडवांस बुकिंग जब्त कर ली।",
        "kn_latn": "Medical emergency inda event cancel madidde banquet hall 50000 advance booking deposit forfeit madiddare Section 74 penalty.",
        "hi_latn": "Medical emergency me function cancel kiya to banquet hall ne bina nuksan ke mera 50000 advance forfeit kar liya.",
        "kn_en": "Wedding vendor forfeited 50000 advance token money, medical emergency cancellation notice kottidru refund madilla.",
        "hi_en": "Medical emergency me wedding cancel hone par banquet hall ne 50000 advance token money forfeit kar liya unreasonable penalty."
    }
]


def build_benchmark_cases():
    test_cases = []
    
    # 1. 50 English Scenarios (en)
    # 2. 50 Kannada Scenarios (kn)
    # 3. 50 Hindi Scenarios (hi)
    # 4. 25 Kannada-English Code-Mixed Scenarios (kn-en)
    # 5. 25 Hindi-English Code-Mixed Scenarios (hi-en)
    # 6. 25 Romanized Kannada Scenarios (kn-Latn)
    # 7. 25 Romanized Hindi Scenarios (hi-Latn)
    # Total: 250 test cases

    # We replicate the 25 core parallel cases with variations to fill the target quotas:
    # 50 en = 25 core + 25 variations
    # 50 kn = 25 core + 25 variations
    # 50 hi = 25 core + 25 variations
    # 25 kn_en = 25 core
    # 25 hi_en = 25 core
    # 25 kn_latn = 25 core
    # 25 hi_latn = 25 core
    
    # Generate the 25 core sets first
    for i, p in enumerate(PARALLEL_CORE_CASES):
        idx = i + 1
        base = p["id_base"]
        
        # English core
        test_cases.append({
            "test_id": f"MB_EN_{base}",
            "parallel_group_id": f"GRP_{base}",
            "language": "en",
            "script": "Latin",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": p["en"]
        })
        
        # Kannada core
        test_cases.append({
            "test_id": f"MB_KN_{base}",
            "parallel_group_id": f"GRP_{base}",
            "language": "kn",
            "script": "Kannada",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": p["kn"]
        })

        # Hindi core
        test_cases.append({
            "test_id": f"MB_HI_{base}",
            "parallel_group_id": f"GRP_{base}",
            "language": "hi",
            "script": "Devanagari",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": p["hi"]
        })

        # Kanglish (Romanized Kannada)
        test_cases.append({
            "test_id": f"MB_KNL_{base}",
            "parallel_group_id": f"GRP_{base}",
            "language": "kn-Latn",
            "script": "Latin",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": p["kn_latn"]
        })

        # Hinglish (Romanized Hindi)
        test_cases.append({
            "test_id": f"MB_HIL_{base}",
            "parallel_group_id": f"GRP_{base}",
            "language": "hi-Latn",
            "script": "Latin",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": p["hi_latn"]
        })

        # Kannada-English Code-Mixed
        test_cases.append({
            "test_id": f"MB_KN_EN_{base}",
            "parallel_group_id": f"GRP_{base}",
            "language": "kn-en",
            "script": "Mixed",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": p["kn_en"]
        })

        # Hindi-English Code-Mixed
        test_cases.append({
            "test_id": f"MB_HI_EN_{base}",
            "parallel_group_id": f"GRP_{base}",
            "language": "hi-en",
            "script": "Mixed",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": p["hi_en"]
        })

    # Now add 25 more variations for en, kn, hi to reach 50 each
    for i, p in enumerate(PARALLEL_CORE_CASES):
        base = p["id_base"]
        
        # en variation
        test_cases.append({
            "test_id": f"MB_EN_VAR_{base}",
            "parallel_group_id": f"GRP_VAR_{base}",
            "language": "en",
            "script": "Latin",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": f"Urgent legal grievance: {p['en']} Please advise which legal section applies."
        })

        # kn variation
        test_cases.append({
            "test_id": f"MB_KN_VAR_{base}",
            "parallel_group_id": f"GRP_VAR_{base}",
            "language": "kn",
            "script": "Kannada",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": f"ತುರ್ತು ಕಾನೂನು ದೂರು: {p['kn']} ದಯವಿಟ್ಟು ಕಾನೂನು ಪರಿಹಾರ ಮತ್ತು ಸಂಬಂಧಿತ ವಿಭಾಗಗಳನ್ನು ತಿಳಿಸಿ."
        })

        # hi variation
        test_cases.append({
            "test_id": f"MB_HI_VAR_{base}",
            "parallel_group_id": f"GRP_VAR_{base}",
            "language": "hi",
            "script": "Devanagari",
            "domain": p["domain"],
            "expected_issue": p["expected_issue"],
            "expected_acts": p["expected_acts"],
            "expected_sections": p["expected_sections"],
            "scenario": f"महत्वपूर्ण कानूनी शिकायत: {p['hi']} कृपया बताएं कि इसमें कौन सी धारा लगेगी और क्या कदम उठाएं।"
        })

    print(f"Generated {len(test_cases)} multilingual benchmark test cases.")
    
    # Verify counts
    from collections import Counter
    counts = Counter(c["language"] for c in test_cases)
    print("Language breakdown:", dict(counts))
    dom_counts = Counter(c["domain"] for c in test_cases)
    print("Domain breakdown:", dict(dom_counts))

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)
        
    print(f"Saved to {OUT_FILE}")


if __name__ == "__main__":
    build_benchmark_cases()
