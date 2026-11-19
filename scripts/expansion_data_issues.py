"""Expansion data for Issues, Guidance, and Portals across the five LegalLens domains.
Every issue mapping contains structured provision references, legal elements,
factual conditions, exceptions, and multilingual prototypes (EN, HI, KN).
Every guidance contains <= 5 concrete action steps.
"""

NEW_PORTALS = {
    "cci_portal": {
        "portal_id": "cci_portal",
        "name": "Competition Commission of India (CCI)",
        "official_url": "https://www.cci.gov.in",
        "purpose": "Statutory body to eliminate anti-competitive cartels, prohibit abuse of dominant market power, and investigate corporate price-fixing under Competition Act, 2002.",
        "priority": "primary",
        "usage_condition": "Use when filing information against corporate cartels, predatory pricing, or tie-in practices affecting consumers.",
        "official_source": "Competition Commission of India, Government of India",
        "supported_issue_ids": [
            "anti_competitive_cartel_price_fixing",
            "school_mandatory_uniform_book_tie_in"
        ]
    },
    "tdsat_portal": {
        "portal_id": "tdsat_portal",
        "name": "Telecom Disputes Settlement and Appellate Tribunal (TDSAT)",
        "official_url": "https://tdsat.gov.in",
        "purpose": "Statutory appellate tribunal adjudicating cyber appeals under IT Act Section 48 and telecom/broadcasting consumer disputes under TRAI Act, 1997.",
        "priority": "primary",
        "usage_condition": "Use for statutory appeals against State IT Adjudicating Officer orders or major telecom service disputes.",
        "official_source": "Ministry of Communications / TDSAT, Government of India",
        "supported_issue_ids": [
            "cyber_adjudicating_officer_compensation",
            "telemarketing_spoofing_trai_violation",
            "telecom_vas_billing_dispute"
        ]
    },
    "cio_bima_portal": {
        "portal_id": "cio_bima_portal",
        "name": "Council for Insurance Ombudsmen (CIO)",
        "official_url": "https://www.cioins.co.in",
        "purpose": "Statutory ombudsman forum for cost-free, binding, independent resolution of personal insurance claim disputes, delays, and repudiations up to Rs 50 Lakhs.",
        "priority": "primary",
        "usage_condition": "Use when private or public insurers reject or delay settlement of life, health, or motor insurance claims.",
        "official_source": "Council for Insurance Ombudsmen, Government of India",
        "supported_issue_ids": [
            "insurance_ombudsman_claim_repudiation_dispute",
            "insurance_claim_arbitrary_rejection",
            "health_insurance_claim_arbitrary_rejection"
        ]
    }
}

NEW_ISSUES = {
    # -------------------------------------------------------------------------
    # DOMAIN 1: CYBER FRAUD
    # -------------------------------------------------------------------------
    "cyber_digital_evidence_admissibility": {
        "issue_id": "cyber_digital_evidence_admissibility",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "cyber_fraud",
        "display_name": "Digital Evidence Admissibility & Section 63 BSA Certificate",
        "issue_definition": "Police or trial court requiring statutory electronic certificate or proof of authenticity to admit WhatsApp chats, emails, banking screenshots, or server logs in a cyber fraud prosecution.",
        "prototype_texts": [
            "Police or court is asking for an electronic certificate to admit my WhatsApp screenshots and cyber fraud bank statement as legal evidence.",
            "How do I prove my digital chats and call records in court under the new evidence act BSA 2023 without my phone being seized?",
            "The cyber cell is asking for Section 63 certificate for email and digital screenshots of the transaction.",
            "ಸೈಬರ್ ಅಪರಾಧದ ಸಾಕ್ಷ್ಯವಾಗಿ ವಾಟ್ಸಾಪ್ ಚಾಟ್ ಮತ್ತು ಬ್ಯಾಂಕ್ ಸ್ಟೇಟ್‌ಮೆಂಟ್‌ಗಳನ್ನು ನ್ಯಾಯಾಲಯದಲ್ಲಿ ಹಾಜರುಪಡಿಸಲು ಸೆಕ್ಷನ್ 63 ಪ್ರಮಾಣಪತ್ರ ಕೇಳುತ್ತಿದ್ದಾರೆ.",
            "कोर्ट में साइबर फ्रॉड के व्हाट्सएप चैट और ऑनलाइन ट्रांजैक्शन का स्क्रीनशॉट साबित करने के लिए इलेक्ट्रॉनिक सर्टिफिकेट मांगा गया है।"
        ],
        "provision_references": [
            {
                "act_id": "bharatiya_sakshya_adhiniyam_2023",
                "section_id": "61",
                "provision_relevance_rationale": "Confers statutory recognition that electronic records carry identical legal validity and enforceability as physical paper documents.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Admissibility of electronic record", "Statutory equivalence to physical documents"],
                "applicability_conditions": ["Record produced in electronic or digital format"],
                "missing_facts": ["Whether the original device or a printout is being tendered in court"],
                "exceptions": ["Subject to verification of device integrity under Section 63"]
            },
            {
                "act_id": "bharatiya_sakshya_adhiniyam_2023",
                "section_id": "63",
                "provision_relevance_rationale": "Mandates statutory electronic certificate signed by custodian/device owner to admit secondary digital evidence like printouts and exports.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Device lawful management", "Proper operation during period", "Statutory schedule certificate"],
                "applicability_conditions": ["Secondary copy, screenshot, or printout tendered in evidence"],
                "missing_facts": ["Whether certificate signed by device owner or system administrator is attached"],
                "exceptions": ["Not required if original mobile device itself produced under Section 57"]
            },
            {
                "act_id": "it_act_2000",
                "section_id": "4",
                "provision_relevance_rationale": "Substantive IT Act provision granting legal recognition to electronic records.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Legal recognition of electronic records"],
                "applicability_conditions": ["Electronic record accessible for subsequent reference"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "cyber_ransomware_data_kidnapping": {
        "issue_id": "cyber_ransomware_data_kidnapping",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "cyber_fraud",
        "display_name": "Ransomware System Hijacking & Cyber Extortion",
        "issue_definition": "Cybercriminals deployed ransomware encrypting computers, servers, or personal databases, demanding extortion money or cryptocurrency to unlock data.",
        "prototype_texts": [
            "Our office computers and customer database were locked by ransomware and hackers are demanding 2 Bitcoins to give decryption key.",
            "A malicious script encrypted all files on my computer, changed file extensions, and a text file says pay money in crypto or all data will be leaked.",
            "Ransomware attack locked down hospital management servers and hackers are threatening to publish confidential medical records.",
            "ನನ್ನ ಲ್ಯಾಪ್‌ಟಾಪ್ ಮತ್ತು ಸರ್ವರ್ ಡೇಟಾವನ್ನು ರಾನ್‌ಸಮ್‌ವೇರ್ ಲಾಕ್ ಮಾಡಿದೆ ಮತ್ತು ಡಿಕ್ರಿಪ್ಷನ್‌ಗಾಗಿ ಕ್ರಿಪ್ಟೋಕರೆನ್ಸಿ ಹಣ ಕೇಳುತ್ತಿದ್ದಾರೆ.",
            "कंप्यूटर में रैंसमवेयर वायरस आ गया है और सारे फाइल्स लॉक करके हैकर पैसे की मांग कर रहे हैं।"
        ],
        "provision_references": [
            {
                "act_id": "it_act_2000",
                "section_id": "43",
                "provision_relevance_rationale": "Civil liability and penalty for introducing computer contaminants, encrypting data, and denying access.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Unauthorised access", "Introducing virus or contaminant", "Denial of access to authorised user"],
                "applicability_conditions": ["Data encrypted or destroyed without owner permission"],
                "missing_facts": ["Whether security logs and incident hashes were preserved"],
                "exceptions": []
            },
            {
                "act_id": "it_act_2000",
                "section_id": "66",
                "provision_relevance_rationale": "Substantive penal provision for computer related offences punishable with imprisonment up to 3 years.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Dishonest or fraudulent commission of Section 43 acts"],
                "applicability_conditions": ["Accused acted dishonestly or fraudulently"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "bns_2023",
                "section_id": "308",
                "provision_relevance_rationale": "Substantive criminal extortion provision for putting person in fear of injury/data leak to extort money.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Putting person in fear of harm/leak", "Dishonestly inducing delivery of money or valuable security"],
                "applicability_conditions": ["Demand of ransom or extortion money made"],
                "missing_facts": ["Proof of extortion communication or ransom note"],
                "exceptions": []
            },
            {
                "act_id": "it_act_2000",
                "section_id": "70B",
                "provision_relevance_rationale": "Mandatory 6-hour cybersecurity incident reporting obligation to CERT-In for ransomware attacks.",
                "relevance_classification": "PROCEDURAL_PROVISION",
                "applicable_legal_elements": ["Statutory reporting of ransomware incident to CERT-In"],
                "applicability_conditions": ["Organisational or critical system breach"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "telemarketing_spoofing_trai_violation": {
        "issue_id": "telemarketing_spoofing_trai_violation",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "cyber_fraud",
        "display_name": "Unsolicited Telemarketing, Robocalls & SMS Header Spoofing",
        "issue_definition": "Citizen bombarded by aggressive unregistered telemarketing calls, auto-dialers, or fraudulent SMS with spoofed banking sender headers despite DND registration.",
        "prototype_texts": [
            "I keep getting 20 spam calls and scam loan SMS daily from fake 140 numbers and unregistered mobile numbers even though DND is active.",
            "Someone is spoofing my bank SMS header sending fake lottery and phishing links to my phone.",
            "Telemarketing company calling multiple times a day from automated robotic dialers refusing to remove my phone number.",
            "ಡಿಎನ್‌ಡಿ ಆಕ್ಟಿವ್ ಇದ್ದರೂ ಪ್ರತಿದಿನ ನಕಲಿ ಬ್ಯಾಂಕ್ ಲೋನ್ ಮತ್ತು ಸ್ಪ್ಯಾಮ್ ಕಾಲ್‌ಗಳು ಕಿರುಕುಳ ನೀಡುತ್ತಿವೆ.",
            "डीएनडी चालू होने के बाद भी रोज 15-20 स्पैम कॉल्स और फर्जी बैंक लोन के मैसेज आ रहे हैं।"
        ],
        "provision_references": [
            {
                "act_id": "trai_act_1997",
                "section_id": "14",
                "provision_relevance_rationale": "Governs dispute resolution regarding telecom service provider defaults and consumer grievances before TDSAT.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Dispute between service provider and group of consumers", "Non-enforcement of TCCCPR DND regulations"],
                "applicability_conditions": ["Telecom consumer aggrieved by persistent commercial communications"],
                "missing_facts": ["Whether complaint lodged via telecom operator DND app or 1909"],
                "exceptions": []
            },
            {
                "act_id": "it_act_2000",
                "section_id": "66d",
                "provision_relevance_rationale": "Penalizes cheating by personation through telecommunication devices and spoofed sender IDs.",
                "relevance_classification": "CONDITIONALLY_APPLICABLE",
                "applicable_legal_elements": ["Cheating by personation", "Using computer or telecom resource"],
                "applicability_conditions": ["Caller impersonated bank, government agency, or reputable entity"],
                "missing_facts": ["Whether caller attempted fraudulent financial inducement"],
                "exceptions": ["Ordinary commercial marketing without fraud is governed purely under TRAI regulations"]
            }
        ]
    },
    "cyber_adjudicating_officer_compensation": {
        "issue_id": "cyber_adjudicating_officer_compensation",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "cyber_fraud",
        "display_name": "IT Act Section 46 Adjudicating Officer Compensation Claim",
        "issue_definition": "Victim seeking statutory monetary compensation up to Rs 5 Crore before State IT Secretary against negligent bank or hacker for unauthorized account debits or data theft.",
        "prototype_texts": [
            "I want to file a compensation claim before the State IT Secretary under Section 46 of IT Act because my bank allowed unauthorized net banking transfers.",
            "How do I claim money back from negligent bank under IT Act Adjudicating Officer up to 5 crore rupees?",
            "Bank failed to implement 2FA security and fraudster transferred 15 lakhs, seeking compensation under Section 43 and 46 of Information Technology Act.",
            "ಬ್ಯಾಂಕ್ ನಿರ್ಲಕ್ಷ್ಯದಿಂದ ಸೈಬರ್ ವಂಚನೆಯಲ್ಲಿ ಕಳೆದುಹೋದ ಹಣವನ್ನು ಐಟಿ ಆಕ್ಟ್ ಸೆಕ್ಷನ್ 46 ರ ಪ್ರಕಾರ ಪರಿಹಾರವಾಗಿ ಪಡೆಯುವುದು ಹೇಗೆ?",
            "साइबर फ्रॉड में बैंक की लापरवाही से कटे पैसों का हर्जाना पाने के लिए आईटी सेक्रेटरी एडजुडिकेटिंग ऑफिसर के पास केस कैसे करें।"
        ],
        "provision_references": [
            {
                "act_id": "it_act_2000",
                "section_id": "46",
                "provision_relevance_rationale": "Empowers State IT Secretary to adjudicate compensation claims up to Rs 5 Crore for Section 43/43A contraventions.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Contravention of Chapter IX of IT Act", "Claim for injury or damage not exceeding Rs 5 Crore", "Inquiry held by Adjudicating Officer"],
                "applicability_conditions": ["Claim amount <= Rs 5,00,00,000", "Incident involves unauthorised computer access or failure of data security"],
                "missing_facts": ["Whether petition filed in prescribed form before State IT Secretary"],
                "exceptions": ["Claims above Rs 5 Crore must be filed in regular Civil Court"]
            },
            {
                "act_id": "it_act_2000",
                "section_id": "43",
                "provision_relevance_rationale": "Statutory ground of liability for damages: unauthorised extraction of data or access to computer network.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Unauthorised access", "Downloading or extracting data", "Denial of access"],
                "applicability_conditions": ["Absence of user permission"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "it_act_2000",
                "section_id": "48",
                "provision_relevance_rationale": "Statutory appellate avenue before TDSAT against Adjudicating Officer orders within 45 days.",
                "relevance_classification": "PROCEDURAL_PROVISION",
                "applicable_legal_elements": ["Statutory appeal to TDSAT"],
                "applicability_conditions": ["Aggrieved by order of Adjudicating Officer"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "cyber_mule_account_money_laundering": {
        "issue_id": "cyber_mule_account_money_laundering",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "cyber_fraud",
        "display_name": "Cyber Mule Account Syndicate & Bank Account Freezing",
        "issue_definition": "Citizen's bank account frozen by police after being used or compromised as a money mule account to funnel cybercrime proceeds, or citizen trapped by commission agents.",
        "prototype_texts": [
            "My bank account was frozen by cyber police because someone transferred scam money through my UPI without my knowledge.",
            "A Telegram group offered 5% commission for renting my savings account, now police froze all my accounts under cyber fraud FIR.",
            "My legitimate salary account is on debit freeze due to a 10000 rupees lien placed by Gujarat cyber crime cell for mule money trail.",
            "ಯಾರೋ ವಂಚನೆಯ ಹಣವನ್ನು ನನ್ನ ಖಾತೆಗೆ ವರ್ಗಾಯಿಸಿದ್ದರಿಂದ ಸೈಬರ್ ಪೊಲೀಸರು ನನ್ನ ಬ್ಯಾಂಕ್ ಖಾತೆಯನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ಫ್ರೀಜ್ ಮಾಡಿದ್ದಾರೆ.",
            "टेलीग्राम पर कमीशन के चक्कर में बैंक डिटेल दिया था, अब पुलिस ने साइबर फ्रॉड म्यूल अकाउंट बताकर खाता सीज कर दिया है।"
        ],
        "provision_references": [
            {
                "act_id": "bns_2023",
                "section_id": "317",
                "provision_relevance_rationale": "Substantive offence for receiving or retaining stolen property and fraud funds.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Property transferred by theft, extortion, or cheating", "Dishonestly receiving or retaining stolen property"],
                "applicability_conditions": ["Funds transferred were proceeds of crime"],
                "missing_facts": ["Whether account holder had knowledge of fraudulent origin or acted innocently"],
                "exceptions": ["Innocent account holders without criminal knowledge are protected against prosecution"]
            },
            {
                "act_id": "bnss_2023",
                "section_id": "107",
                "provision_relevance_rationale": "Empowers Magistrate Court to attach mule accounts and distribute recovered money back to original victims.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Property derived from criminal activity", "Police application to Court for attachment", "Order for distribution to victim"],
                "applicability_conditions": ["Funds currently frozen in mule account"],
                "missing_facts": ["Whether victim has applied to Magistrate for refund of attached money"],
                "exceptions": []
            },
            {
                "act_id": "prevention_of_money_laundering_act_2002",
                "section_id": "3",
                "provision_relevance_rationale": "Offence of money-laundering for knowingly assisting in laundering proceeds of crime.",
                "relevance_classification": "CONDITIONALLY_APPLICABLE",
                "applicable_legal_elements": ["Involvement in process or activity connected with proceeds of crime"],
                "applicability_conditions": ["Commercial mule syndicate laundering funds exceeding threshold"],
                "missing_facts": [],
                "exceptions": ["Ordinary small unauthorized transfers do not attract PMLA"]
            }
        ]
    },

    # -------------------------------------------------------------------------
    # DOMAIN 2: CONSUMER ISSUES
    # -------------------------------------------------------------------------
    "product_liability_defective_good_injury": {
        "issue_id": "product_liability_defective_good_injury",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "consumer_issues",
        "display_name": "Product Liability Claim for Personal Injury or Property Damage",
        "issue_definition": "Consumer or bystander suffered physical injury, burn, illness, or property damage caused by a defective electronic appliance, exploding battery, or toxic product.",
        "prototype_texts": [
            "A pressure cooker exploded due to defective safety valve causing severe burns and kitchen damage, seeking product liability compensation.",
            "An electric scooter battery caught fire while charging inside my garage, burning my two-wheeler and injuring my hand.",
            "A newly purchased water heater leaked electric current giving an electric shock to family member, claiming compensation from manufacturer.",
            "ದೋಷಪೂರಿತ ಪ್ರೆಶರ್ ಕುಕ್ಕರ್ ಅಥವಾ ಗೀಸರ್ ಸ್ಫೋಟಗೊಂಡು ಗಾಯವಾಗಿದ್ದು ಕಂಪನಿಯಿಂದ ಪರಿಹಾರ ಪಡೆಯಲು ಪ್ರಾಡಕ್ಟ್ ಲಯಾಬಿಲಿಟಿ ಕೇಸ್ ಹಾಕುವುದು ಹೇಗೆ?",
            "नया खरीदा हुआ इलेक्ट्रॉनिक सामान फटने से आग लग गई और शरीर में चोट आई, मैन्युफैक्चरर पर प्रोडक्ट लायबिलिटी का केस करना है।"
        ],
        "provision_references": [
            {
                "act_id": "cpa_2019",
                "section_id": "82",
                "provision_relevance_rationale": "Governs statutory applicability of product liability actions against manufacturers, service providers, and sellers.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Harm caused by defective product", "Manufactured, serviced, or sold by opposite party"],
                "applicability_conditions": ["Harm includes personal injury, property damage, mental agony"],
                "missing_facts": ["Medical treatment records and photographs of damaged product"],
                "exceptions": ["Subject to Section 87 statutory defenses"]
            },
            {
                "act_id": "cpa_2019",
                "section_id": "83",
                "provision_relevance_rationale": "Statutory entitlement of consumer to bring product liability action before Consumer Commission.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Complainant suffered harm", "Brought before District/State Consumer Commission"],
                "applicability_conditions": ["Causal connection between product defect and injury"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "84",
                "provision_relevance_rationale": "Specifies manufacturer liability for manufacturing defect, design defect, or failure to conform to express warranty.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Manufacturing defect", "Defective design", "Inadequate warning of danger"],
                "applicability_conditions": ["Product left manufacturer custody in defective condition"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "87",
                "provision_relevance_rationale": "Statutory defense exceptions: product was modified or misused contrary to warning labels.",
                "relevance_classification": "CONDITIONALLY_APPLICABLE",
                "applicable_legal_elements": ["Statutory defenses available to seller/manufacturer"],
                "applicability_conditions": ["Opposite party raises plea of consumer tampering or misuse"],
                "missing_facts": ["Whether product was serviced by unauthorized local mechanics"],
                "exceptions": ["Manufacturer must prove adequate warning was provided"]
            }
        ]
    },
    "anti_competitive_cartel_price_fixing": {
        "issue_id": "anti_competitive_cartel_price_fixing",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "consumer_issues",
        "display_name": "Anti-Competitive Cartel, Price-Fixing & Monopolistic Abuse",
        "issue_definition": "Consumers exploited by corporate cartels colluding on airfares, cement prices, or schools forcing tie-in purchases of uniforms from a single monopolistic vendor.",
        "prototype_texts": [
            "Private school is forcing all parents to buy textbooks and uniforms exclusively from one vendor at triple the market price.",
            "Airlines operating on the same route suddenly doubled ticket prices simultaneously showing cartel price-fixing behavior.",
            "Exclusive dealer syndicate in our city refusing to sell spare parts to independent repair shops to maintain monopoly.",
            "ಶಾಲೆಯವರು ಯೂನಿಫಾರ್ಮ್ ಮತ್ತು ಪುಸ್ತಕಗಳನ್ನು ತಮ್ಮ ನಿರ್ದಿಷ್ಟ ಅಂಗಡಿಯಲ್ಲೇ ದುಪ್ಪಟ್ಟು ಬೆಲೆಗೆ ಖರೀದಿಸುವಂತೆ ಬಲವಂತ ಮಾಡುತ್ತಿದ್ದಾರೆ.",
            "स्कूल वाले किताबें और ड्रेस अपनी ही चुनिंदा दुकान से तीन गुना कीमत पर खरीदने का दबाव बना रहे हैं, क्या यह गैरकानूनी है?"
        ],
        "provision_references": [
            {
                "act_id": "competition_act_2002",
                "section_id": "3",
                "provision_relevance_rationale": "Declares anti-competitive agreements, cartels, price-fixing, and tie-in sales void ab initio.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Agreement causing appreciable adverse effect on competition", "Price-fixing, market allocation, or tie-in arrangement"],
                "applicability_conditions": ["Tie-in purchase forced upon consumers or collusive price manipulation"],
                "missing_facts": ["Proof of circular or mandate forcing exclusive vendor purchase"],
                "exceptions": ["Reasonable conditions protecting IPR under Section 3(5)"]
            },
            {
                "act_id": "competition_act_2002",
                "section_id": "4",
                "provision_relevance_rationale": "Prohibits abuse of dominant position through unfair conditions or denial of market access.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Dominant enterprise", "Imposing unfair condition or price", "Denial of market access"],
                "applicability_conditions": ["Enterprise occupies position of economic strength in relevant market"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "competition_act_2002",
                "section_id": "19",
                "provision_relevance_rationale": "Procedural right of any consumer or association to file information before CCI to initiate investigation.",
                "relevance_classification": "PROCEDURAL_PROVISION",
                "applicable_legal_elements": ["Information filed by consumer under Section 19(1)(a)"],
                "applicability_conditions": ["Prima facie case of Section 3 or Section 4 violation"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "2_47",
                "provision_relevance_rationale": "Categorizes forced tie-in sales and deceptive commercial tactics as an Unfair Trade Practice.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Unfair trade practice", "Misleading representation"],
                "applicability_conditions": ["Consumer forced into tied transaction"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "packaged_commodity_mrp_tampering_overcharging": {
        "issue_id": "packaged_commodity_mrp_tampering_overcharging",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "consumer_issues",
        "display_name": "MRP Tampering, Dual Pricing & Above-MRP Overcharging",
        "issue_definition": "Retailer, airport shop, or multiplex cinema charging prices higher than the printed Maximum Retail Price (MRP), or sticking altered price labels over original MRP.",
        "prototype_texts": [
            "Railway station stall charged 30 rupees for a water bottle with printed MRP of 20 rupees claiming cooling charges.",
            "Airport retail outlet pasted a sticker of 150 rupees over the manufacturer printed MRP of 80 rupees on potato chips.",
            "Cinema hall selling popcorn and cold drinks with a dual MRP sticker higher than identical products sold outside.",
            "ಎಂಆರ್‌ಪಿ ೨೦ ರೂಪಾಯಿ ಇರುವ ನೀರಿನ ಬಾಟಲಿಗೆ ರೈಲ್ವೇ ಸ್ಟೇಷನ್‌ನಲ್ಲಿ ೩೦ ರೂಪಾಯಿ ವಸೂಲಿ ಮಾಡಿದ್ದಾರೆ ಮತ್ತು ಎಂಆರ್‌ಪಿ ಮೇಲೆ ಸ್ಟಿಕ್ಕರ್ ಹಾಕಿದ್ದಾರೆ.",
            "एमआरपी 50 रुपये थी लेकिन दुकानदार ने स्टिकर लगाकर 80 रुपये लिए और फ्रिज में रखने का एक्स्ट्रा चार्ज जोड़ा।"
        ],
        "provision_references": [
            {
                "act_id": "legal_metrology_act_2009",
                "section_id": "18",
                "provision_relevance_rationale": "Mandates that no person shall sell or distribute any pre-packaged commodity unless it bears statutory declarations including MRP.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Pre-packaged commodity", "Compliance with mandatory retail declarations", "Prohibition of sale without declarations"],
                "applicability_conditions": ["Goods sold in pre-packaged retail condition"],
                "missing_facts": ["Photograph of package showing printed MRP and bill showing extra amount charged"],
                "exceptions": []
            },
            {
                "act_id": "legal_metrology_act_2009",
                "section_id": "36",
                "provision_relevance_rationale": "Imposes statutory penalty—fine up to Rs 25,000 to Rs 1 Lakh—for selling pre-packaged goods at price higher than MRP.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Selling packaged commodity at price exceeding printed Maximum Retail Price (MRP)"],
                "applicability_conditions": ["Price charged exceeds printed retail price inclusive of all taxes"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "2_47",
                "provision_relevance_rationale": "Classifies charging above MRP as a statutory Unfair Trade Practice actionable before Consumer Commission.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Unfair trade practice", "Charging price in excess of price fixed by law"],
                "applicability_conditions": ["Consumer overcharged beyond statutory ceiling"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "substandard_adulterated_food_toxic_illness": {
        "issue_id": "substandard_adulterated_food_toxic_illness",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "consumer_issues",
        "display_name": "Adulterated, Unsafe or Substandard Food Causing Illness",
        "issue_definition": "Consumer suffered food poisoning or severe infection from contaminated, adulterated, or insect-infested restaurant food or packaged provisions.",
        "prototype_texts": [
            "We ordered biryani from online delivery app and found dead cockroach inside, family fell sick with severe food poisoning.",
            "Packaged milk had chemical detergent adulteration and foul smell, causing stomach infection in toddler.",
            "Restaurant served contaminated food resulting in hospitalization with acute gastroenteritis, hotel refusing responsibility.",
            "ರೆಸ್ಟೋರೆಂಟ್‌ನಿಂದ ತರಿಸಿದ ಊಟದಲ್ಲಿ ಹುಳು ಇತ್ತು ಮತ್ತು ಅದನ್ನು ಸೇವಿಸಿ ಫುಡ್ ಪಾಯಿಸನ್ ಆಗಿ ಆಸ್ಪತ್ರೆಗೆ ದಾಖಲಾಗಿದ್ದೇವೆ.",
            "ऑनलाइन खाने में मरा हुआ कीड़ा निकला और खाना खाने के बाद फूड पॉइजनिंग होकर हॉस्पिटल में भर्ती होना पड़ा।"
        ],
        "provision_references": [
            {
                "act_id": "food_safety_act_2006",
                "section_id": "26",
                "provision_relevance_rationale": "General responsibility of food business operators to ensure food satisfies safety requirements.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Food business operator duty", "Safe food standard", "Prohibition of unsafe, misbranded, or sub-standard food"],
                "applicability_conditions": ["Food sold or delivered by food business operator"],
                "missing_facts": ["Food sample preserved and food inspector inspection report"],
                "exceptions": []
            },
            {
                "act_id": "food_safety_act_2006",
                "section_id": "54",
                "provision_relevance_rationale": "Imposes penalty up to Rs 1 Lakh for food containing extraneous matter such as insects, plastic, or foreign particles.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Presence of extraneous foreign matter in food"],
                "applicability_conditions": ["Foreign object or insect discovered in food"],
                "missing_facts": ["Photographic proof and restaurant bill"],
                "exceptions": []
            },
            {
                "act_id": "food_safety_act_2006",
                "section_id": "59",
                "provision_relevance_rationale": "Criminal punishment—imprisonment up to life and fine up to Rs 10 Lakh—for manufacturing or selling unsafe food causing injury or illness.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Manufacturing, selling, or storing unsafe food", "Resulting in non-grievous injury, grievous hurt, or death"],
                "applicability_conditions": ["Victim suffered medical illness or hospitalization"],
                "missing_facts": ["Hospital discharge summary and medical test reports"],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "84",
                "provision_relevance_rationale": "Product liability compensation action against restaurant and delivery platform for medical costs and mental agony.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Product liability of food manufacturer/provider", "Compensation for harm"],
                "applicability_conditions": ["Personal injury or medical expense sustained"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "insurance_ombudsman_claim_repudiation_dispute": {
        "issue_id": "insurance_ombudsman_claim_repudiation_dispute",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "consumer_issues",
        "display_name": "Insurance Ombudsman Redressal for Arbitrary Claim Rejection",
        "issue_definition": "Insurance company arbitrarily rejected or delayed a genuine health, life, or motor insurance claim exceeding 30 days without valid statutory justification.",
        "prototype_texts": [
            "My father's cashless health insurance claim of 4 lakhs was rejected by TPA citing non-disclosure of pre-existing hypertension after 4 years of policy.",
            "Motor insurance company deducted 60% depreciation on accident car repair claim without justification.",
            "Health insurance claim pending for 45 days with endless repetitive document queries, want to file complaint with Insurance Ombudsman.",
            "ನಾಲ್ಕು ವರ್ಷಗಳಿಂದ ಪ್ರೀಮಿಯಂ ಪಾವತಿಸುತ್ತಿದ್ದರೂ ಹೆಲ್ತ್ ಇನ್ಶೂರೆನ್ಸ್ ಕ್ಲೈಮ್ ಅನ್ನು ನೆಪ ಹೇಳಿ ತಿರಸ್ಕರಿಸಿದ್ದಾರೆ, ಇನ್ಶೂರೆನ್ಸ್ ಒಂಬುಡ್ಸ್‌ಮನ್‌ಗೆ ದೂರು ನೀಡುವುದು ಹೇಗೆ?",
            "बीमा कंपनी ने 4 साल पुरानी स्वास्थ्य बीमा पॉलिसी का क्लेम पुरानी बीमारी का बहाना बनाकर खारिज कर दिया है, ओम्बड्समैन में कैसे जाएं।"
        ],
        "provision_references": [
            {
                "act_id": "insurance_act_1938",
                "section_id": "45",
                "provision_relevance_rationale": "Statutory three-year incontestability rule: policy cannot be questioned or repudiated on grounds of misstatement after expiry of 3 years.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Three years expired since policy issuance", "Absolute statutory bar on repudiation for pre-existing non-disclosure"],
                "applicability_conditions": ["Policy continuously in force for 3 years or more"],
                "missing_facts": ["Date of policy inception and date of claim rejection"],
                "exceptions": ["Insurer must prove deliberate fraud, which is subject to high statutory burden"]
            },
            {
                "act_id": "cpa_2019",
                "section_id": "2_11",
                "provision_relevance_rationale": "Arbitrary repudiation of valid insurance claim constitutes statutory service deficiency.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Deficiency of service by insurer"],
                "applicability_conditions": ["Valid premium paid and claim covered under policy terms"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "35",
                "provision_relevance_rationale": "Jurisdiction to file consumer complaint before District Commission for claim amount plus compensation.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Filing complaint before District Commission"],
                "applicability_conditions": ["Claim value up to Rs 50 Lakhs"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "spurious_cosmetics_adulterated_drugs": {
        "issue_id": "spurious_cosmetics_adulterated_drugs",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "consumer_issues",
        "display_name": "Sale of Spurious Drugs, Adulterated Cosmetics & Counterfeits",
        "issue_definition": "Consumer supplied fake, adulterated, or hazardous counterfeit cosmetics or substandard medicines without batch numbers or valid licenses.",
        "prototype_texts": [
            "I ordered branded sunscreen online but received fake counterfeit bottle with no batch number which caused severe skin burns and allergy.",
            "Local chemist sold expired antibiotics with tampered expiry date sticker, seeking legal action against medical store.",
            "Counterfeit luxury perfume purchased online turned out to be chemical solvent causing severe respiratory irritation.",
            "ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಖರೀದಿಸಿದ ಕಾಸ್ಮೆಟಿಕ್ಸ್ ನಕಲಿಯಾಗಿದ್ದು ಮುಖದಲ್ಲಿ ಸುಟ್ಟ ಗಾಯ ಮತ್ತು ಅಲರ್ಜಿ ಉಂಟಾಗಿದೆ.",
            "दवा की दुकान से नकली और एक्सपायर्ड दवा बेची गई जिसकी एक्सपायरी डेट खुरची हुई थी।"
        ],
        "provision_references": [
            {
                "act_id": "drugs_and_cosmetics_act_1940",
                "section_id": "18",
                "provision_relevance_rationale": "Strict prohibition on manufacturing, storing, or selling spurious, adulterated, or misbranded drugs and cosmetics.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Prohibition of manufacture and sale of spurious/adulterated drugs or cosmetics", "Failure to conform to standards"],
                "applicability_conditions": ["Goods fall under definition of drug or cosmetic"],
                "missing_facts": ["Purchase bill, packaging showing batch number, dermatologist report"],
                "exceptions": []
            },
            {
                "act_id": "drugs_and_cosmetics_act_1940",
                "section_id": "27",
                "provision_relevance_rationale": "Criminal penalties—imprisonment up to 10 years or life for selling adulterated or spurious drugs causing grievous hurt.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Sale of spurious drug likely to cause death or grievous hurt", "Punishment with imprisonment not less than 10 years extending to life"],
                "applicability_conditions": ["Drug spurious or contaminated"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "84",
                "provision_relevance_rationale": "Product liability action against seller and e-commerce platform for compensation of medical treatment.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Harm caused by adulterated cosmetic/drug", "Product seller liability"],
                "applicability_conditions": ["Harm sustained by consumer"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "unlawful_electricity_disconnection_meter_dispute": {
        "issue_id": "unlawful_electricity_disconnection_meter_dispute",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "consumer_issues",
        "display_name": "Unlawful Electricity Disconnection & Arbitrary Meter Billing",
        "issue_definition": "Power utility disconnected electricity connection without mandatory 15-day statutory notice or slapped an arbitrary assessment bill for a faulty meter.",
        "prototype_texts": [
            "Electricity board disconnected our home power supply without giving any prior written 15 days notice over disputed bill.",
            "BESCOM/DISCOM issued arbitrary inflated assessment of 1 lakh rupees claiming meter was running slow, threatening disconnection.",
            "Power company cut off power connection immediately when bill was challenged in grievance cell.",
            "೧೫ ದಿನಗಳ ಲಿಖಿತ ನೋಟಿಸ್ ನೀಡದೆ ವಿದ್ಯುತ್ ಮಂಡಳಿಯವರು ಏಕಾಏಕಿ ನಮ್ಮ ಮನೆಯ ವಿದ್ಯುತ್ ಸಂಪರ್ಕ ಕಡಿತಗೊಳಿಸಿದ್ದಾರೆ.",
            "बिजली विभाग ने बिना 15 दिन का कानूनी नोटिस दिए मीटर का बिल विवाद होने पर सीधे बिजली काट दी है।"
        ],
        "provision_references": [
            {
                "act_id": "electricity_act_2003",
                "section_id": "56",
                "provision_relevance_rationale": "Mandates compulsory 15 clear days written notice before electricity can be disconnected for unpaid dues; no disconnection if disputed amount is deposited.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Default in payment of electricity charge", "Mandatory requirement: not less than 15 clear days notice in writing", "Bar on disconnection if consumer deposits under protest"],
                "applicability_conditions": ["Electricity disconnection effected or threatened without 15-day notice"],
                "missing_facts": ["Proof of lack of 15 days written notice before disconnection"],
                "exceptions": ["Does not apply to cases of direct power theft under Section 135"]
            },
            {
                "act_id": "electricity_act_2003",
                "section_id": "42",
                "provision_relevance_rationale": "Statutory grievance redressal: Consumer Grievance Redressal Forum (CGRF) and Electricity Ombudsman.",
                "relevance_classification": "PROCEDURAL_PROVISION",
                "applicable_legal_elements": ["Establishment of CGRF", "Right of appeal to Electricity Ombudsman"],
                "applicability_conditions": ["Grievance against electricity distribution licensee"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "2_11",
                "provision_relevance_rationale": "Unlawful disconnection of essential electricity supply constitutes gross service deficiency.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Deficiency in electricity supply service"],
                "applicability_conditions": ["Consumer suffered disruption of essential utility"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },

    # -------------------------------------------------------------------------
    # DOMAIN 3: TRAFFIC ENFORCEMENT
    # -------------------------------------------------------------------------
    "traffic_enforcing_officer_violation_double_penalty": {
        "issue_id": "traffic_enforcing_officer_violation_double_penalty",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "traffic_enforcement",
        "display_name": "Traffic Police Violation (Section 210B Double Penalty) & Bribery",
        "issue_definition": "Traffic police officer or transport enforcement personnel riding without helmet, driving wrong side, or demanding bribes/extortion under threat of fake challan.",
        "prototype_texts": [
            "A traffic police constable was riding a two-wheeler on wrong side without helmet and when questioned he threatened to impound my bike.",
            "Traffic cop demanded 1000 rupees cash bribe to let me go without issuing challan, how do I report under Section 210B and Prevention of Corruption Act?",
            "Traffic police vehicle jumped red light and officers were not wearing seatbelts, can I report them for double fine under MV Act?",
            "ಟ್ರಾಫಿಕ್ ಪೊಲೀಸರೇ ಹೆಲ್ಮೆಟ್ ಇಲ್ಲದೆ ರಾಂಗ್ ಸೈಡ್ ಗಾಡಿ ಓಡಿಸುತ್ತಿದ್ದಾರೆ ಮತ್ತು ಲಂಚ ಕೇಳುತ್ತಿದ್ದಾರೆ, ಸೆಕ್ಷನ್ ೨೧೦ಬಿ ಅಡಿಯಲ್ಲಿ ದ್ವಿಗುಣ ದಂಡ ಹೇಗೆ?",
            "ट्रैफिक पुलिस वाला खुद बिना हेलमेट के गलत दिशा में गाड़ी चला रहा था और रिश्वत मांग रहा था, 210B में डबल जुर्माने की शिकायत कैसे करें।"
        ],
        "provision_references": [
            {
                "act_id": "mv_act_1988",
                "section_id": "210B",
                "provision_relevance_rationale": "Mandates that any enforcing authority committing a traffic violation shall be liable for TWICE (double) the statutory penalty.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Authority empowered to enforce MV Act", "Committed traffic offence under the Act", "Statutory double (2x) penalty"],
                "applicability_conditions": ["Offender is police or transport enforcement officer"],
                "missing_facts": ["Dashcam footage, video, or photograph showing officer uniform/badge and vehicle number"],
                "exceptions": ["Bona fide emergency pursuit or life-saving dispatch exempt"]
            },
            {
                "act_id": "prevention_of_corruption_act_1988",
                "section_id": "7",
                "provision_relevance_rationale": "Substantive offence for public servant obtaining undue advantage or bribe to forgo issuing traffic challan.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Public servant", "Demanding or accepting undue financial advantage", "Improper performance of public duty"],
                "applicability_conditions": ["Cash or UPI bribe demanded by traffic officer"],
                "missing_facts": ["Audio/video recording of bribe demand or UPI transaction record"],
                "exceptions": []
            },
            {
                "act_id": "bns_2023",
                "section_id": "217",
                "provision_relevance_rationale": "Penalizes public servant disobeying direction of law with intent to save person from punishment or property from forfeiture.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Public servant knowingly disobeying direction of law"],
                "applicability_conditions": ["Officer acted unlawfully"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "driving_while_disqualified_revoked_licence": {
        "issue_id": "driving_while_disqualified_revoked_licence",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "traffic_enforcement",
        "display_name": "Driving While Disqualified or Operating with Suspended Licence",
        "issue_definition": "Driver operating a motor vehicle or applying for a fresh licence while their driving licence has been formally suspended or disqualified by RTO or Court.",
        "prototype_texts": [
            "My licence was suspended for 3 months due to overspeeding and police caught me driving again, what is the fine under Section 182?",
            "Someone whose driving licence was cancelled for drunk driving applied for a new licence from another RTO state.",
            "Caught driving commercial vehicle while driving licence was disqualified by magistrate court.",
            "ಆರ್‌ಟಿಒ ಅಮಾನತು ಮಾಡಿರುವ ಚಾಲನಾ ಪರವಾನಗಿ ಅವಧಿಯಲ್ಲಿ ವಾಹನ ಚಾಲನೆ ಮಾಡಿದ್ದಕ್ಕೆ ಪೊಲೀಸರು ಪ್ರಕರಣ ದಾಖಲಿಸಿದ್ದಾರೆ.",
            "ड्राइविंग लाइसेंस सस्पेंड होने के बाद भी गाड़ी चलाते हुए पकड़े जाने पर धारा 182 में क्या सजा और जुर्माना है।"
        ],
        "provision_references": [
            {
                "act_id": "mv_act_1988",
                "section_id": "182",
                "provision_relevance_rationale": "Imposes criminal punishment—fine up to Rs 10,000, imprisonment up to 3 months, or both—for driving or obtaining licence while disqualified.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Person disqualified from holding or obtaining driving licence", "Drives in public place or applies for new licence without disclosing endorsement"],
                "applicability_conditions": ["Existing valid disqualification order from RTO or Court"],
                "missing_facts": ["Details of previous suspension/disqualification order"],
                "exceptions": ["Does not apply if disqualification was stayed by appellate court"]
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "180",
                "provision_relevance_rationale": "Penalizes vehicle owner with fine up to Rs 5,000 or 3 months jail for allowing an unauthorized or disqualified person to drive.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Owner of motor vehicle", "Allowing unauthorized or disqualified person to drive"],
                "applicability_conditions": ["Owner permitted disqualified person to drive"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "mentally_physically_unfit_driving": {
        "issue_id": "mentally_physically_unfit_driving",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "traffic_enforcement",
        "display_name": "Driving When Mentally or Physically Incapacitated",
        "issue_definition": "Operating a motor vehicle on public roads when suffering from an acute medical disability, seizure disorder, or severe physical incapacitation causing danger to public.",
        "prototype_texts": [
            "Driver suffered an epileptic seizure while driving a bus causing multiple collisions, was driving despite doctor prohibiting driving.",
            "Person with uncorrected severe visual impairment driving at night causing public safety hazard.",
            "Police booked driver under Section 186 for driving while mentally or physically unfit after erratic driving on highway.",
            "ದೈಹಿಕ ಅಥವಾ ಮಾನಸಿಕ ಅಸ್ವಸ್ಥತೆಯಿಂದ ಸಾರ್ವಜನಿಕರಿಗೆ ಅಪಾಯವಾಗುವಂತೆ ವಾಹನ ಚಾಲನೆ ಮಾಡಿದ್ದಕ್ಕಾಗಿ ಕೇಸ್ ದಾಖಲಾಗಿದೆ.",
            "गंभीर बीमारी या अस्वस्थता की हालत में गाड़ी चलाने पर धारा 186 मोटर वाहन अधिनियम के तहत क्या कार्रवाई होती है।"
        ],
        "provision_references": [
            {
                "act_id": "mv_act_1988",
                "section_id": "186",
                "provision_relevance_rationale": "Penalizes driving in public place when to knowledge suffering from disease or disability calculated to cause danger to public.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Driving in public place", "Knowledge of suffering from disease or disability causing danger"],
                "applicability_conditions": ["Medical condition rendered driving dangerous to public"],
                "missing_facts": ["Medical certificate and RTO fitness records"],
                "exceptions": ["Specially adapted invalid carriages with medical clearance exempt"]
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "184",
                "provision_relevance_rationale": "Substantive dangerous driving section punishable with imprisonment up to 1 year or fine up to Rs 5,000.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Driving dangerously having regard to all circumstances"],
                "applicability_conditions": ["Erratic driving observed in public"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "mandatory_vehicle_safety_recall_defect": {
        "issue_id": "mandatory_vehicle_safety_recall_defect",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "traffic_enforcement",
        "display_name": "Statutory Vehicle Safety Recall & Manufacturing Defect",
        "issue_definition": "Automobile or EV manufacturer refusing to recall or fix vehicles possessing critical systemic defects in braking, steering, airbags, or battery thermal management.",
        "prototype_texts": [
            "My new car model has a known steering lock failure affecting hundreds of buyers, but the car manufacturer is refusing a statutory recall.",
            "EV two-wheeler caught fire due to known battery thermal runaway defect, demanding full replacement under Section 110A MV Act.",
            "Automobile company refusing to replace defective engine that stalls suddenly on highways.",
            "ಹೊಸ ಕಾರಿನಲ್ಲಿ ಸ್ಟೀರಿಂಗ್ ಮತ್ತು ಬ್ರೇಕ್ ವೈಫಲ್ಯದ ಗಂಭೀರ ದೋಷವಿದ್ದು ಕಂಪನಿಯು ವಾಹನವನ್ನು ಮರಳಿ ಪಡೆಯಲು (ರಿಕಲ್) ನಿರಾಕರಿಸುತ್ತಿದೆ.",
            "कार में ब्रेक फेलियर और इंजन की गंभीर तकनीकी खराबी है लेकिन कंपनी गाड़ी वापस लेने और पूरा पैसा लौटाने से मना कर रही है।"
        ],
        "provision_references": [
            {
                "act_id": "mv_act_1988",
                "section_id": "110A",
                "provision_relevance_rationale": "Empowers Central Government to order mandatory vehicle recall; obligates manufacturer to reimburse 100% price or replace vehicle.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Defect in motor vehicle causing harm to occupants, environment, or road users", "Statutory obligation on manufacturer to reimburse or replace vehicle"],
                "applicability_conditions": ["Systemic manufacturing or design defect in vehicle model"],
                "missing_facts": ["Service history, job cards, and manufacturer technical bulletins"],
                "exceptions": ["Damage resulting from accidents or unauthorized third party modifications excluded"]
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "182A",
                "provision_relevance_rationale": "Imposes fine up to Rs 1 Crore on manufacturers for non-compliance with motor vehicle standards or recall orders.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Offences by manufacturer of motor vehicles", "Penalty up to Rs 1 Crore"],
                "applicability_conditions": ["Manufacturer failed to comply with statutory recall or safety standards"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "84",
                "provision_relevance_rationale": "Product liability action before Consumer Commission for full refund of vehicle purchase price plus compensation.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Manufacturing defect in motor vehicle", "Product liability action against manufacturer"],
                "applicability_conditions": ["Defect manifests within warranty/usable life"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "hit_and_run_statutory_solatium_compensation": {
        "issue_id": "hit_and_run_statutory_solatium_compensation",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "traffic_enforcement",
        "display_name": "Hit-and-Run Solatium Fund & No-Fault Accident Compensation",
        "issue_definition": "Victim or bereaved family of a hit-and-run motor accident seeking statutory no-fault compensation (Rs 2 Lakhs for death, Rs 50,000 for grievous hurt) from the Government Solatium Scheme.",
        "prototype_texts": [
            "Pedestrian was killed by an unidentified speeding truck that fled the scene, how to claim statutory hit and run compensation under Section 161?",
            "Brother suffered grievous head injury in hit-and-run bike accident where offending vehicle could not be traced.",
            "Seeking immediate 2 lakh rupees compensation from Government Solatium Fund for fatal hit and run accident.",
            "ಹಿಟ್ ಆಂಡ್ ರನ್ ಅಪಘಾತದಲ್ಲಿ ಅಪರಿಚಿತ ವಾಹನ ಡಿಕ್ಕಿ ಹೊಡೆದು ವ್ಯಕ್ತಿ ಸಾವನ್ನಪ್ಪಿದ್ದು ಸರ್ಕಾರದ ಸೊಲೇಷಿಯಂ ಫಂಡ್‌ನಿಂದ ಪರಿಹಾರ ಪಡೆಯುವುದು ಹೇಗೆ?",
            "हिट एंड रन सड़क हादसे में अज्ञात गाड़ी टक्कर मारकर भाग गई, सरकार से 2 लाख रुपये का मुआवजा कैसे मिलेगा।"
        ],
        "provision_references": [
            {
                "act_id": "mv_act_1988",
                "section_id": "161",
                "provision_relevance_rationale": "Special scheme for compensation to victims of hit and run motor accidents: fixed Rs 2 Lakhs for death, Rs 50,000 for grievous hurt.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Hit and run motor accident where identity of vehicle cannot be ascertained", "Statutory payment: Rs 2,00,000 in case of death, Rs 50,000 in case of grievous hurt"],
                "applicability_conditions": ["Offending vehicle untraceable despite police investigation"],
                "missing_facts": ["Police FIR and Final Report certifying untraceable offending vehicle"],
                "exceptions": ["Does not bar claimant from higher MACT compensation if vehicle is later identified"]
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "164",
                "provision_relevance_rationale": "Guaranteed no-fault statutory compensation of Rs 5 Lakhs for death and Rs 2.5 Lakhs for grievous hurt without proving negligence.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Death or grievous hurt from motor accident", "No requirement to prove negligence of owner/driver"],
                "applicability_conditions": ["Vehicle identified and insured"],
                "missing_facts": ["Insurance details of vehicle"],
                "exceptions": ["Mutually exclusive with fault-based claim under Section 166"]
            },
            {
                "act_id": "bns_2023",
                "section_id": "106",
                "provision_relevance_rationale": "Criminal punishment for causing death by rash and negligent driving and fleeing without reporting.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Causing death by rash and negligent act", "Duty to report to police"],
                "applicability_conditions": ["Fatal road accident"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "traffic_obstruction_unreasonable_towing_charges": {
        "issue_id": "traffic_obstruction_unreasonable_towing_charges",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "traffic_enforcement",
        "display_name": "Traffic Obstruction, Breakdown & Unreasonable Towing Fees",
        "issue_definition": "Vehicle towed unlawfully while driver was arranging mechanic, or private towing agency extorted exorbitant unregulated towing and clamping fees.",
        "prototype_texts": [
            "My car broke down with flat tire with hazard lights on, and within 10 minutes private towing contractor towed it away demanding 3000 rupees cash.",
            "Traffic police towed my bike while parked legally without any no-parking signage, charging exorbitant towing fee without receipt.",
            "Car was wheel clamped while I was seated inside waiting for passenger, officer demanding 1500 fine under obstruction Section 201.",
            "ಕಾರು ಕೆಟ್ಟು ನಿಂತಿದ್ದಾಗ ಮೆಕ್ಯಾನಿಕ್ ಕರೆಯಲು ಹೋಗಿದ್ದೆ, ಆದರೆ ಅಷ್ಟರಲ್ಲೇ ಟ್ರ್ಯಾಫಿಕ್ ಪೊಲೀಸರು ಅಕ್ರಮವಾಗಿ ಟೋಯಿಂಗ್ ಮಾಡಿ ೨೫೦೦ ರೂ ಕೇಳುತ್ತಿದ್ದಾರೆ.",
            "गाड़ी पंचर होने पर रोड साइड में खड़ी थी, 10 मिनट में ट्रैफिक पुलिस क्रेन से उठाकर ले गई और 2000 रुपये की अवैध वसूली कर रहे हैं।"
        ],
        "provision_references": [
            {
                "act_id": "mv_act_1988",
                "section_id": "201",
                "provision_relevance_rationale": "Statutory rules on traffic obstruction, abandonment beyond 10 hours, and prescribed statutory towing charges.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Vehicle causing impediment to free flow of traffic", "Prescribed statutory towing fee", "Prohibition of arbitrary private extortion"],
                "applicability_conditions": ["Towing or wheel clamping executed by traffic enforcement"],
                "missing_facts": ["Towing payment receipt and photo of parking location"],
                "exceptions": ["Towing is prohibited when driver or passenger is seated inside vehicle"]
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "127",
                "provision_relevance_rationale": "Governs removal of motor vehicles abandoned or left unattended on public roads.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Vehicle abandoned for 10 hours or in prohibited zone", "Authorised removal by uniform police officer"],
                "applicability_conditions": ["Vehicle left unattended"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "198",
                "provision_relevance_rationale": "Penalizes unauthorized tampering with vehicle mechanism or brakes.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Unauthorised tampering with stationary vehicle"],
                "applicability_conditions": ["Towing caused physical damage to vehicle"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "statutory_14_day_traffic_prosecution_notice_defense": {
        "issue_id": "statutory_14_day_traffic_prosecution_notice_defense",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "traffic_enforcement",
        "display_name": "Section 209 MV Act Statutory 14-Day Notice Defense to Challans",
        "issue_definition": "Citizen contesting delayed automated speed camera or dangerous driving challans issued months after alleged violation without mandatory 14-day statutory notice.",
        "prototype_texts": [
            "I received an automated speeding challan on SMS 4 months after the date of alleged driving, how to contest under Section 209 14-day notice bar?",
            "Traffic police sent dangerous driving summons after 60 days without any on-the-spot warning or notice within fourteen days.",
            "Can I get automated camera challan dismissed because police failed to serve notice within 14 days of the offence?",
            "ಅಪರಾಧ ನಡೆದ ೪ ತಿಂಗಳ ನಂತರ ಆನ್‌ಲೈನ್ ಕ್ಯಾಮೆರಾ ಚಲನ್ ಬಂದಿದ್ದು, ಸೆಕ್ಷನ್ ೨೦೯ ರ ಪ್ರಕಾರ ೧೪ ದಿನದೊಳಗೆ ನೋಟಿಸ್ ನೀಡದಿದ್ದರೆ ಚಲನ್ ರದ್ದುಪಡಿಸಬಹುದೇ?",
            "स्पीडिंग का चालान 3 महीने बाद मैसेज से भेजा गया है, धारा 209 के तहत 14 दिन में नोटिस न मिलने पर क्या चालान खारिज हो सकता है।"
        ],
        "provision_references": [
            {
                "act_id": "mv_act_1988",
                "section_id": "209",
                "provision_relevance_rationale": "Absolute statutory bar: no conviction for speeding (S. 183) or dangerous driving (S. 184) unless warned at spot or notice served within 14 days.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Prosecution under Section 183 or Section 184", "Failure to warn at spot AND failure to serve notice within 14 days", "Statutory bar on conviction"],
                "applicability_conditions": ["Challan relates to speeding (183) or dangerous driving (184)", "Notice dispatched/served after 14 days from date of offence"],
                "missing_facts": ["Date of alleged violation vs date of dispatch/SMS of challan"],
                "exceptions": ["Bar does not apply if delay was caused by driver failure to keep registered address updated on Vahan"]
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "183",
                "provision_relevance_rationale": "Substantive speeding offence governed by Section 209 restriction.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Driving at excess speed"],
                "applicability_conditions": ["Allegation of exceeding speed limit"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "184",
                "provision_relevance_rationale": "Substantive dangerous driving offence governed by Section 209 restriction.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Driving dangerously"],
                "applicability_conditions": ["Allegation of dangerous driving"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "national_highway_toll_obstruction_dispute": {
        "issue_id": "national_highway_toll_obstruction_dispute",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "traffic_enforcement",
        "display_name": "FASTag Toll Plaza Overcharging, Delay & Highway Obstruction",
        "issue_definition": "Toll plaza operator charged double toll, experienced scanner failure refusing valid FASTag, or created traffic gridlock beyond 100 meters on National Highway.",
        "prototype_texts": [
            "Toll plaza scanner failed to read active FASTag with balance and plaza staff forced me to pay double cash toll.",
            "Toll gate queue stretched for 500 meters and operator refused to lift boom barrier despite NHAI 100-meter yellow line rule.",
            "FASTag was debited twice at same toll booth within 2 minutes for single passage.",
            "ಫಾಸ್ಟ್‌ಟ್ಯಾಗ್‌ನಲ್ಲಿ ಬ್ಯಾಲೆನ್ಸ್ ಇದ್ದರೂ ಟೋಲ್ ಪ್ಲಾಜಾದಲ್ಲಿ ಸ್ಕ್ಯಾನರ್ ಕೆಲಸ ಮಾಡದೆ ಡಬಲ್ ಹಣ ವಸೂಲಿ ಮಾಡಿದ್ದಾರೆ.",
            "फास्टैग में पर्याप्त बैलेंस होने पर भी टोल गेट पर डबल कैश लिया गया और बैरियर खोलने से मना कर दिया।"
        ],
        "provision_references": [
            {
                "act_id": "national_highways_act_1956",
                "section_id": "8B",
                "provision_relevance_rationale": "Criminal punishment for mischief by injury or obstruction to National Highway.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Mischief or unauthorized obstruction to National Highway traffic"],
                "applicability_conditions": ["Unlawful obstruction on National Highway"],
                "missing_facts": ["Toll plaza receipt, FASTag deduction SMS, dashcam footage"],
                "exceptions": []
            },
            {
                "act_id": "mv_act_1988",
                "section_id": "177",
                "provision_relevance_rationale": "General penalty for contravention of rules and regulations made under MV Act.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Contravention of highway and traffic rules"],
                "applicability_conditions": ["Violation of National Highway fee rules"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "2_11",
                "provision_relevance_rationale": "Double deduction or refusal of valid digital payment at toll plaza is actionable service deficiency.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Deficiency of service by toll concessionaire"],
                "applicability_conditions": ["Consumer paid toll or experienced wrongful double deduction"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },

    # -------------------------------------------------------------------------
    # DOMAIN 4: WORKPLACE & WAGE
    # -------------------------------------------------------------------------
    "statutory_subsistence_allowance_suspension": {
        "issue_id": "statutory_subsistence_allowance_suspension",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "workplace_wage",
        "display_name": "Suspension Without Subsistence Allowance (Section 10A Standing Orders)",
        "issue_definition": "Employee suspended by management pending domestic inquiry or disciplinary proceedings without payment of mandatory 50% / 75% subsistence allowance.",
        "prototype_texts": [
            "Company placed me under suspension pending inquiry 4 months ago and has not paid a single rupee of salary or subsistence allowance.",
            "Employer suspended me over false allegations and refuses to pay 50% subsistence allowance during the domestic inquiry.",
            "Suspended from job for 6 months, can management withhold 100% of my wages during departmental inquiry?",
            "ಆಡಳಿತ ಮಂಡಳಿಯು ನನ್ನನ್ನು ಕೆಲಸದಿಂದ ಅಮಾನತುಗೊಳಿಸಿದ್ದು, ವಿಚಾರಣೆ ನಡೆಯುವಾಗ ನೀಡಬೇಕಾದ ಶೇಕಡಾ ೫೦ ರಷ್ಟು ಜೀವನಾಧಾರ ಭತ್ಯೆಯನ್ನು ನಿರಾಕರಿಸಿದೆ.",
            "कंपनी ने जांच के नाम पर मुझे 3 महीने से सस्पेंड कर रखा है और कोई गुजारा भत्ता (सब्सिस्टेंस अलाउंस) नहीं दे रहे हैं।"
        ],
        "provision_references": [
            {
                "act_id": "industrial_employment_standing_orders_act_1946",
                "section_id": "10A",
                "provision_relevance_rationale": "Mandates non-negotiable statutory subsistence allowance: 50% wages for first 90 days, and 75% thereafter if delay is not employee fault.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Workman suspended pending inquiry", "Statutory entitlement to 50% wages for first 90 days", "Rate increases to 75% wages thereafter"],
                "applicability_conditions": ["Workman suspended pending domestic inquiry"],
                "missing_facts": ["Suspension letter and date of commencement of suspension"],
                "exceptions": ["Non-payment of subsistence allowance vitiates the inquiry and renders termination void (Supreme Court in Chandrabhan)"]
            },
            {
                "act_id": "industrial_disputes_act_1947",
                "section_id": "33C",
                "provision_relevance_rationale": "Statutory recovery of money due from an employer via application to Labour Court.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Recovery of money due from employer under settlement or statutory provision"],
                "applicability_conditions": ["Arrears of subsistence allowance computed and unpaid"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "payment_of_wages_act_1936",
                "section_id": "15",
                "provision_relevance_rationale": "Claims arising out of deductions from wages or delay in payment of wages before Authority.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Unauthorized withholding of statutory wage entitlement"],
                "applicability_conditions": ["Employee wage falls within Act ceiling"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "unilateral_change_in_service_conditions_without_notice": {
        "issue_id": "unilateral_change_in_service_conditions_without_notice",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "workplace_wage",
        "display_name": "Unilateral Change in Service Conditions Without Section 9A Notice",
        "issue_definition": "Management arbitrarily increased daily working hours, changed shift schedules, cancelled allowances, or altered leave benefits without mandatory 21 days written notice.",
        "prototype_texts": [
            "Company suddenly increased daily working hours from 8 to 11 hours and cut shift allowance without any prior 21 days notice.",
            "Management unilaterally changed my job grade, withdrew transport allowance, and changed working days from 5 to 6 days a week.",
            "Employer arbitrarily altered our shift timings and cancelled Saturday off without giving Section 9A notice of change.",
            "೨೧ ದಿನಗಳ ಮುಂಚಿತ ನೋಟಿಸ್ ನೀಡದೆ ಕಂಪನಿಯು ನಮ್ಮ ಕೆಲಸದ ಸಮಯ ಮತ್ತು ವೇತನ ಭತ್ಯೆಯನ್ನು ಏಕಾಏಕಿ ಬದಲಾವಣೆ ಮಾಡಿದೆ.",
            "कंपनी ने बिना 21 दिन का कानूनी नोटिस दिए काम के घंटे 8 से बढ़ाकर 11 कर दिए और शनिवार की छुट्टी खत्म कर दी।"
        ],
        "provision_references": [
            {
                "act_id": "industrial_disputes_act_1947",
                "section_id": "9A",
                "provision_relevance_rationale": "Mandates mandatory 21 days written notice before effecting any change in Fourth Schedule matters (wages, hours, shifts, allowances).",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Proposed change in conditions of service", "Mandatory written notice to affected workmen", "21-day statutory notice period"],
                "applicability_conditions": ["Change affects wages, hours of work, rest intervals, leave, or shift working"],
                "missing_facts": ["Written memo or email announcing unilateral change"],
                "exceptions": ["Changes made pursuant to valid settlement or tribunal award exempt"]
            },
            {
                "act_id": "industrial_employment_standing_orders_act_1946",
                "section_id": "3",
                "provision_relevance_rationale": "Terms of employment must strictly conform to certified standing orders.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Compliance with certified standing orders"],
                "applicability_conditions": ["Establishment has certified standing orders"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "code_on_wages_2019",
                "section_id": "13",
                "provision_relevance_rationale": "Fixes maximum daily and weekly working hours and mandatory weekly day of rest.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Maximum daily working hours limit", "Mandatory day of rest in seven days"],
                "applicability_conditions": ["Hours of work exceed statutory daily ceiling"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "statutory_annual_bonus_non_payment_profitable_unit": {
        "issue_id": "statutory_annual_bonus_non_payment_profitable_unit",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "workplace_wage",
        "display_name": "Denial or Non-Payment of Statutory Annual Minimum Bonus",
        "issue_definition": "Employer refused or defaulted in paying statutory annual bonus (minimum 8.33% of wages) within 8 months of financial year close, citing false loss claims or resignation.",
        "prototype_texts": [
            "Company did not pay our annual Diwali bonus of 8.33% claiming company had a bad quarter even though we worked all 12 months.",
            "I resigned after working for 2 years and company withheld my statutory annual bonus in full and final settlement.",
            "Establishment employing 40 workers has never paid statutory minimum bonus under Payment of Bonus Act.",
            "ವರ್ಷಪೂರ್ತಿ ಕೆಲಸ ಮಾಡಿದರೂ ಕಂಪನಿಯು ೮.೩೩% ಶಾಸನಬದ್ಧ ಬೋನಸ್ ನೀಡಲು ನಿರಾಕರಿಸಿದೆ ಮತ್ತು ರಾಜೀನಾಮೆ ನೀಡಿದ ಕಾರಣಕ್ಕೆ ಬೋನಸ್ ಕಡಿತಗೊಳಿಸಿದೆ.",
            "कंपनी ने पूरे साल काम करने के बाद भी कानूनी 8.33% बोनस देने से मना कर दिया है और इस्तीफे के बाद बोनस रोक लिया है।"
        ],
        "provision_references": [
            {
                "act_id": "payment_of_bonus_act_1965",
                "section_id": "8",
                "provision_relevance_rationale": "Every employee working not less than 30 working days in an accounting year is entitled to receive annual bonus.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Employee worked not less than 30 working days in accounting year", "Establishment employs 20 or more persons"],
                "applicability_conditions": ["Worked at least 30 working days in relevant accounting year"],
                "missing_facts": ["Salary slips and attendance records for the financial year"],
                "exceptions": ["Disqualified only if formally dismissed for fraud, violence, or theft under Section 9"]
            },
            {
                "act_id": "payment_of_bonus_act_1965",
                "section_id": "10",
                "provision_relevance_rationale": "Mandates payment of minimum bonus of 8.33% of wages regardless of profit, loss, or surplus.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Mandatory minimum bonus of 8.33% of salary or Rs 100", "Payable whether or not employer has allocable surplus"],
                "applicability_conditions": ["Establishment not in exempt infancy period"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "payment_of_bonus_act_1965",
                "section_id": "19",
                "provision_relevance_rationale": "Strict deadline: all bonus amounts must be paid in cash within 8 months from close of accounting year.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Mandatory payment in cash within 8 months from accounting year close"],
                "applicability_conditions": ["More than 8 months elapsed since financial year end"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "payment_of_bonus_act_1965",
                "section_id": "28",
                "provision_relevance_rationale": "Criminal prosecution—imprisonment up to 6 months, fine up to Rs 1,000, or both for non-payment.",
                "relevance_classification": "PROCEDURAL_PROVISION",
                "applicable_legal_elements": ["Criminal penalty for contravention of Bonus Act"],
                "applicability_conditions": ["Willful non-payment by employer"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "individual_workman_termination_industrial_dispute": {
        "issue_id": "individual_workman_termination_industrial_dispute",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "workplace_wage",
        "display_name": "Direct Labour Court Dispute for Individual Termination (Section 2A)",
        "issue_definition": "Individual employee illegally terminated, fired, or discharged without due inquiry, seeking direct access to Labour Court for reinstatement with back wages.",
        "prototype_texts": [
            "I was fired verbally on WhatsApp without any inquiry or termination notice after working 3 years, want to approach Labour Court directly.",
            "Company illegally terminated me without notice pay or retrenchment compensation, can I file a case without a trade union under Section 2A?",
            "Constructive termination after asking for maternity benefits, seeking reinstatement and full back wages through Labour Court.",
            "ಯಾವುದೇ ನೋಟಿಸ್ ಅಥವಾ ತನಿಖೆ ಇಲ್ಲದೆ ನನ್ನನ್ನು ಕೆಲಸದಿಂದ ವಜಾಗೊಳಿಸಿದ್ದು, ಸೆಕ್ಷನ್ ೨ಎ ಅಡಿಯಲ್ಲಿ ನೇರವಾಗಿ ಲೇಬರ್ ಕೋರ್ಟ್‌ಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು ಹೇಗೆ?",
            "कंपनी ने बिना किसी कारण और नोटिस के मुझे नौकरी से निकाल दिया, बिना यूनियन के लेबर कोर्ट में केस कैसे दर्ज करें।"
        ],
        "provision_references": [
            {
                "act_id": "industrial_disputes_act_1947",
                "section_id": "2A",
                "provision_relevance_rationale": "Individual discharge, dismissal, retrenchment, or termination is deemed an industrial dispute, granting direct access to Labour Court after 3 months.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Individual workman discharged, dismissed, or retrenched", "Deemed industrial dispute without trade union sponsorship", "Direct application to Labour Court after 3 months conciliation"],
                "applicability_conditions": ["Termination occurred within 3 years", "Applicant qualifies as 'workman' under Section 2(s)"],
                "missing_facts": ["Termination email/letter and conciliation application date"],
                "exceptions": ["Managerial and administrative personnel earning above statutory threshold excluded"]
            },
            {
                "act_id": "industrial_disputes_act_1947",
                "section_id": "25F",
                "provision_relevance_rationale": "Conditions precedent to retrenchment: one month written notice (or pay in lieu) and 15 days average pay per year of service.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Continuous service of not less than one year", "One month notice or pay in lieu", "Retrenchment compensation of 15 days pay per year"],
                "applicability_conditions": ["Workman completed 240 days continuous service in preceding 12 months"],
                "missing_facts": ["Proof of service duration and non-payment of retrenchment compensation"],
                "exceptions": []
            },
            {
                "act_id": "industrial_disputes_act_1947",
                "section_id": "33C",
                "provision_relevance_rationale": "Recovery application for unpaid retrenchment compensation and back wages before Labour Court.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Recovery of money due from employer"],
                "applicability_conditions": ["Monetary dues crystallized"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "retaliatory_action_posh_complainant": {
        "issue_id": "retaliatory_action_posh_complainant",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "workplace_wage",
        "display_name": "Workplace Retaliation & Victimization of POSH Complainant",
        "issue_definition": "Woman employee subjected to retaliation, forced transfer, salary cut, or bad performance appraisal by employer or Internal Committee after filing a POSH sexual harassment complaint.",
        "prototype_texts": [
            "After I filed a sexual harassment complaint against my manager, HR gave me a poor appraisal and transferred me to another city.",
            "Management is retaliating against me for speaking out in a POSH case by withholding my variable pay and excluding me from meetings.",
            "The Internal Committee whitewashed my complaint because the respondent is a director, how to appeal under Section 18 within 90 days?",
            "ಲೈಂಗಿಕ ಕಿರುಕುಳದ (ಪಾಶ್) ದೂರು ದಾಖಲಿಸಿದ ನಂತರ ಕಂಪನಿಯು ನನ್ನ ಮೇಲೆ ಪ್ರತೀಕಾರ ತೀರಿಸಿಕೊಳ್ಳಲು ವರ್ಗಾವಣೆ ಮತ್ತು ವೇತನ ಕಡಿತ ಮಾಡಿದೆ.",
            "पॉश (POSH) कमेटी में शिकायत करने के बाद कंपनी ने मेरा प्रमोशन रोक दिया और दूसरी जगह ट्रांसफर कर दिया, 90 दिन में अपील कैसे करें।"
        ],
        "provision_references": [
            {
                "act_id": "posh_act_2013",
                "section_id": "3",
                "provision_relevance_rationale": "Expressly prohibits hostile work environments, threats of detrimental treatment, or retaliation connected to sexual harassment complaints.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Threat of detrimental treatment in employment", "Hostile work environment", "Connected to sexual harassment complaint"],
                "applicability_conditions": ["Adverse employment action taken after complaint"],
                "missing_facts": ["Timeline showing complaint date vs adverse action date"],
                "exceptions": []
            },
            {
                "act_id": "posh_act_2013",
                "section_id": "18",
                "provision_relevance_rationale": "Statutory right of appeal within 90 days to Court or appellate authority against IC recommendations or employer retaliation.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Appeal against IC findings or non-implementation", "90-day limitation period"],
                "applicability_conditions": ["Appeal filed within 90 days of IC report"],
                "missing_facts": ["Copy of IC inquiry report and recommendations"],
                "exceptions": []
            },
            {
                "act_id": "posh_act_2013",
                "section_id": "12",
                "provision_relevance_rationale": "Statutory interim relief: transfer of respondent, grant of paid leave up to 3 months, or restraining respondent from reporting on work.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Statutory interim relief during inquiry", "Restraining respondent from supervising complainant"],
                "applicability_conditions": ["Inquiry pending or completed"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "posh_act_2013",
                "section_id": "26",
                "provision_relevance_rationale": "Penal action against employer: fine up to Rs 50,000 and cancellation of business licence for repeated non-compliance.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Penalty for non-compliance by employer"],
                "applicability_conditions": ["Employer failed to act on recommendations"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "unlawful_alteration_of_service_conditions_during_conciliation": {
        "issue_id": "unlawful_alteration_of_service_conditions_during_conciliation",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "workplace_wage",
        "display_name": "Alteration of Service Conditions During Pendency of Conciliation (Section 33)",
        "issue_definition": "Employer suspended, terminated, or reduced wages of workmen while dispute is actively pending conciliation before Labour Officer without prior permission.",
        "prototype_texts": [
            "While our wage dispute was being heard by Labour Conciliation Officer, management fired 3 active worker representatives without permission.",
            "Employer terminated my service during ongoing conciliation proceedings before the Labour Commissioner, violating Section 33.",
            "Management stopped paying salary to workers during conciliation meeting, seeking Section 33A complaint for automatic reinstatement.",
            "ಕಾರ್ಮಿಕ ಅಧಿಕಾರಿಯ ಮುಂದೆ ಸಂಧಾನ ಸಭೆ ನಡೆಯುತ್ತಿರುವಾಗಲೇ ಕಂಪನಿಯು ನಮ್ಮನ್ನು ಕೆಲಸದಿಂದ ತೆಗೆದುಹಾಕಿದೆ.",
            "लेबर कमिश्नर के सामने विवाद की सुनवाई के दौरान ही कंपनी ने बिना अनुमति नौकरी से निकाल दिया, धारा 33 का उल्लंघन।"
        ],
        "provision_references": [
            {
                "act_id": "industrial_disputes_act_1947",
                "section_id": "33",
                "provision_relevance_rationale": "Absolute statutory prohibition on altering service conditions or dismissing workmen during pendency of conciliation without express written permission.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Pendency of conciliation or Labour Court proceedings", "Alteration of conditions of service or dismissal of workman", "Absence of express prior written permission"],
                "applicability_conditions": ["Proceedings actively pending before conciliation officer/tribunal"],
                "missing_facts": ["Proof of active conciliation notices and subsequent termination order"],
                "exceptions": ["Action taken in violation of Section 33 is void ab initio (Jaipur Zila Sahakari Bank case)"]
            },
            {
                "act_id": "industrial_disputes_act_1947",
                "section_id": "33C",
                "provision_relevance_rationale": "Direct recovery of salary and wages for the entire duration of illegal dismissal.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Recovery of wages due from employer"],
                "applicability_conditions": ["Termination void under Section 33"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },

    # -------------------------------------------------------------------------
    # DOMAIN 5: CONTRACTUAL DISPUTES
    # -------------------------------------------------------------------------
    "commercial_dispute_mandatory_pre_institution_mediation": {
        "issue_id": "commercial_dispute_mandatory_pre_institution_mediation",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Mandatory Pre-Institution Mediation (Section 12A Commercial Courts Act)",
        "issue_definition": "Party filing or defending a commercial suit exceeding specified pecuniary value where pre-institution mediation is mandatory unless urgent interim relief is sought.",
        "prototype_texts": [
            "We have a commercial supply contract dispute of 50 lakhs, is pre-institution mediation mandatory under Section 12A before filing a civil suit?",
            "Opposite party filed a commercial suit directly in court without going to Legal Services Authority for mediation, seeking rejection of plaint under Patil Automation.",
            "How to initiate pre-institution mediation for unpaid B2B software development invoices before filing commercial court suit?",
            "ವಾಣಿಜ್ಯ ವಿವಾದದಲ್ಲಿ ಕೋರ್ಟ್‌ಗೆ ಹೋಗುವ ಮುನ್ನ ಸೆಕ್ಷನ್ ೧೨ಎ ಅಡಿಯಲ್ಲಿ ಮಧ್ಯಸ್ಥಿಕೆ (ಮೆಡಿಯೇಶನ್) ಕಡ್ಡಾಯವೇ?",
            "कमर्शियल कोर्ट में मुकदमा करने से पहले धारा 12A के तहत लीगल सर्विसेज अथॉरिटी में मध्यस्थता (मीडिएशन) अनिवार्य है क्या।"
        ],
        "provision_references": [
            {
                "act_id": "commercial_courts_act_2015",
                "section_id": "12A",
                "provision_relevance_rationale": "Mandates that a commercial suit not contemplating urgent interim relief shall not be instituted unless plaintiff exhausts pre-institution mediation.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Commercial dispute of specified value", "Mandatory pre-institution mediation through District Legal Services Authority", "Suit filed without mediation is liable to rejection under Order VII Rule 11 CPC (Patil Automation v. Rakheja)"],
                "applicability_conditions": ["Commercial suit filed without prayer for urgent interim relief"],
                "missing_facts": ["Whether urgent interim injunction is sought in the plaint"],
                "exceptions": ["Suits contemplating urgent interim relief (e.g. freezing bank accounts or urgent injunction) are exempt"]
            },
            {
                "act_id": "contract_act_1872",
                "section_id": "73",
                "provision_relevance_rationale": "Substantive ground of compensation for loss or damage caused by breach of commercial contract.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Breach of contract", "Naturally arising loss or damage"],
                "applicability_conditions": ["Actual commercial loss sustained"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "unregistered_lease_immovable_property_dispute": {
        "issue_id": "unregistered_lease_immovable_property_dispute",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Unregistered Long-Term Lease & Tenancy Dispute",
        "issue_definition": "Landlord-tenant dispute arising out of an unregistered lease deed for a duration exceeding 11 months (one year or more), triggering evidentiary bar under Section 49 Registration Act.",
        "prototype_texts": [
            "We signed a 3-year commercial rental agreement on 100 rupees stamp paper without registering it at Sub-Registrar, can landlord evict me abruptly?",
            "Tenant refusing to vacate claiming 5-year unregistered lease agreement is valid, seeking eviction under Transfer of Property Act.",
            "Landlord withheld 5 lakhs commercial deposit claiming unregistered 2-year lease agreement cannot be produced in court.",
            "ಸಬ್-ರಿಜಿಸ್ಟ್ರಾರ್ ಕಚೇರಿಯಲ್ಲಿ ನೋಂದಣಿ ಮಾಡಿಸದ ೩ ವರ್ಷದ ಬಾಡಿಗೆ ಕರಾರು ಪತ್ರದ ಮಾನ್ಯತೆ ಮತ್ತು ಖಾಲಿ ಮಾಡುವ ವಿವಾದ.",
            "3 साल का किराए का एग्रीमेंट बिना रजिस्ट्री कराए 100 रुपये के स्टांप पेपर पर किया था, अब मकान मालिक अचानक खाली करने को कह रहा है।"
        ],
        "provision_references": [
            {
                "act_id": "registration_act_1908",
                "section_id": "17",
                "provision_relevance_rationale": "Mandates compulsory registration of leases of immovable property from year to year or exceeding one year.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Lease of immovable property exceeding one year", "Compulsory registration with Sub-Registrar"],
                "applicability_conditions": ["Lease duration exceeds 11 months"],
                "missing_facts": ["Original lease document and proof of tenure"],
                "exceptions": ["11-month rental agreements exempt from compulsory central registration"]
            },
            {
                "act_id": "registration_act_1908",
                "section_id": "49",
                "provision_relevance_rationale": "Unregistered document required to be registered cannot affect immovable property or be received as evidence of property transfer.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Document inadmissible to prove leasehold rights", "Admissible only for collateral purpose or to prove contract in specific performance"],
                "applicability_conditions": ["Failure to register document under Section 17"],
                "missing_facts": [],
                "exceptions": ["Admissible to prove nature of possession (collateral purpose)"]
            },
            {
                "act_id": "tp_act_1882",
                "section_id": "106",
                "provision_relevance_rationale": "In absence of registered lease, tenancy is treated as month-to-month terminable by 15 days notice (residential) or 6 months (manufacturing).",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Month-to-month tenancy", "15 days notice to quit in writing"],
                "applicability_conditions": ["Unregistered lease exceeding one year creates monthly tenancy by operation of law"],
                "missing_facts": ["Proof of service of Section 106 notice to quit"],
                "exceptions": []
            },
            {
                "act_id": "tp_act_1882",
                "section_id": "107",
                "provision_relevance_rationale": "Substantive rule: leases exceeding one year can be made only by registered instrument.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Leases exceeding one year must be registered"],
                "applicability_conditions": ["Tenure exceeding 12 months"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "part_performance_possession_protection": {
        "issue_id": "part_performance_possession_protection",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Protection of Possession Under Doctrine of Part Performance (Section 53A TPA)",
        "issue_definition": "Purchaser who paid consideration and took physical possession under written sale agreement seeking statutory protection against eviction by dishonest seller.",
        "prototype_texts": [
            "I paid 90% advance money and took physical possession of house under written agreement to sell, now seller is threatening to evict me and sell to someone else.",
            "Can seller throw me out of property after handing over possession and taking money under Section 53A part performance?",
            "Builder handed over flat keys and possession under sale agreement, but delaying sale deed and threatening to cancel allotment.",
            "ಬರೆದುಕೊಟ್ಟ ಕರಾರು ಪತ್ರದಂತೆ ಹಣ ಪಾವತಿಸಿ ಸ್ವಾಧೀನ ಪಡೆದ ನಂತರ ಮಾಲೀಕರು ಅಕ್ರಮವಾಗಿ ಹೊರಹಾಕಲು ಯತ್ನಿಸುತ್ತಿದ್ದಾರೆ.",
            "एग्रीमेंट टू सेल पर 90% पैसा देकर मकान का कब्जा ले लिया था, अब विक्रेता मुकर रहा है और कब्जा खाली कराने की धमकी दे रहा है।"
        ],
        "provision_references": [
            {
                "act_id": "tp_act_1882",
                "section_id": "53A",
                "provision_relevance_rationale": "Statutory doctrine of part performance: debars transferor from evicting or enforcing rights against transferee who took possession and is ready to perform.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Written signed agreement to transfer immovable property", "Transferee took possession in part performance", "Transferee performed or willing to perform balance terms", "Statutory shield against eviction"],
                "applicability_conditions": ["Transferee in continuous lawful possession", "Transferee ready and willing to pay balance consideration"],
                "missing_facts": ["Proof of physical possession and payment receipts"],
                "exceptions": ["Post-2001, agreement must be registered to defend possession against subsequent registered buyers"]
            },
            {
                "act_id": "specific_relief_act_1963",
                "section_id": "10",
                "provision_relevance_rationale": "Mandatory specific performance: court must enforce contract of sale of immovable property.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Specific performance of contract enforced by court"],
                "applicability_conditions": ["Valid agreement to sell"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "registration_act_1908",
                "section_id": "49",
                "provision_relevance_rationale": "Proviso to Section 49 allows unregistered agreement to be received as evidence of contract in suit for specific performance.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Unregistered agreement admissible in specific performance suit"],
                "applicability_conditions": ["Suit filed under Specific Relief Act"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "specific_performance_readiness_willingness_dispute": {
        "issue_id": "specific_performance_readiness_willingness_dispute",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Specific Performance & Proving Readiness and Willingness (Section 16c)",
        "issue_definition": "Purchaser filing civil suit for specific performance of property agreement, contesting seller's defense that buyer was unready or lacked funds to pay balance consideration.",
        "prototype_texts": [
            "Seller refused to execute sale deed after taking 20 lakhs advance claiming I did not arrange balance money on time, how to prove readiness and willingness in court?",
            "Filing suit for specific performance of plot sale agreement, what documents are needed to satisfy Section 16(c) of Specific Relief Act?",
            "Seller backing out of registered sale agreement due to increase in land market prices, claiming contract expired.",
            "ಜಮೀನು ಮಾರಾಟದ ಕರಾರು ಪತ್ರದಂತೆ ಬಾಕಿ ಹಣ ಪಾವತಿಸಲು ಸಿದ್ಧರಿದ್ದರೂ ಮಾಲೀಕರು ರಿಜಿಸ್ಟ್ರೇಷನ್ ಮಾಡಿಸದೆ ಸತಾಯಿಸುತ್ತಿದ್ದಾರೆ.",
            "जमीन का बयाना लेने के बाद रेट बढ़ जाने पर सेलर रजिस्ट्री कराने से मना कर रहा है, स्पेसिफिक परफॉर्मेंस का केस कैसे करें।"
        ],
        "provision_references": [
            {
                "act_id": "specific_relief_act_1963",
                "section_id": "10",
                "provision_relevance_rationale": "Mandatory specific performance of contracts by civil courts (post-2018 amendment removed court discretion).",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Specific performance mandatory unless barred under Section 11(2), 14, or 16"],
                "applicability_conditions": ["Valid contract of sale of immovable property"],
                "missing_facts": ["Original agreement to sell and legal notice issued calling upon seller to execute deed"],
                "exceptions": []
            },
            {
                "act_id": "specific_relief_act_1963",
                "section_id": "16",
                "provision_relevance_rationale": "Personal bar: plaintiff MUST plead and prove continuous readiness (financial capacity) and willingness (intent) to perform essential terms.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Proof of readiness and willingness throughout from agreement date to decree", "Financial capacity proved through bank balance, loan sanction, or liquid assets"],
                "applicability_conditions": ["Plaintiff seeking specific performance decree"],
                "missing_facts": ["Bank account statements or loan sanction letters proving balance funds were available"],
                "exceptions": ["Failure to prove readiness is fatal to specific performance suit"]
            },
            {
                "act_id": "contract_act_1872",
                "section_id": "51",
                "provision_relevance_rationale": "Reciprocal promises: seller not bound to execute deed unless buyer ready to pay balance consideration.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Promisor not bound to perform unless reciprocal promisee ready and willing"],
                "applicability_conditions": ["Concurrent conditions in agreement"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "limitation_act_1963",
                "section_id": "art_55",
                "provision_relevance_rationale": "Article 54/55: 3-year limitation period from date fixed for performance or notice of refusal.",
                "relevance_classification": "PROCEDURAL_PROVISION",
                "applicable_legal_elements": ["Three years limitation period"],
                "applicability_conditions": ["Suit filed within 3 years of refusal"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "condition_vs_warranty_breach_sale_of_goods": {
        "issue_id": "condition_vs_warranty_breach_sale_of_goods",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Breach of Core Condition vs Collateral Warranty in Supply Contracts",
        "issue_definition": "Commercial buyer supplied with industrial goods or raw materials failing core specifications, seeking complete contract repudiation and refund vs claiming price reduction.",
        "prototype_texts": [
            "We ordered industrial steel of grade SS316 but supplier delivered inferior SS304 grade, can we repudiate contract and reject goods under Section 12?",
            "Factory machinery delivered lacks specified production capacity, seeking full refund for breach of essential condition.",
            "Wholesale textile consignment delivered does not match the approved sample in quality or shade.",
            "ಖರೀದಿಸಿದ ಕೈಗಾರಿಕಾ ಯಂತ್ರೋಪಕರಣ ಅಥವಾ ಕಚ್ಚಾ ವಸ್ತು ಒಪ್ಪಂದದ ಗುಣಮಟ್ಟಕ್ಕೆ ಹೊಂದಿಕೆಯಾಗದಿದ್ದಾಗ ಸಂಪೂರ್ಣ ಆರ್ಡರ್ ರದ್ದುಪಡಿಸಿ ಹಣ ವಾಪಸ್ ಪಡೆಯುವುದು ಹೇಗೆ?",
            "सप्लायर ने तयशुदा क्वालिटी और ग्रेड का माल न भेजकर घटिया माल भेजा है, सेल ऑफ गुड्स एक्ट में पूरा माल रिजेक्ट करके पैसा कैसे वापस लें।"
        ],
        "provision_references": [
            {
                "act_id": "sale_of_goods_act_1930",
                "section_id": "12",
                "provision_relevance_rationale": "Core distinction: breach of condition gives right to treat contract as repudiated and reject goods; breach of warranty gives claim for damages only.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Condition essential to main purpose -> right to repudiate contract", "Warranty collateral -> damages only"],
                "applicability_conditions": ["Stipulation breached goes to root of contract"],
                "missing_facts": ["Purchase order specifications vs lab test report of delivered goods"],
                "exceptions": []
            },
            {
                "act_id": "sale_of_goods_act_1930",
                "section_id": "15",
                "provision_relevance_rationale": "Implied condition that goods must correspond strictly with description.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Sale by description", "Implied condition of correspondence with description"],
                "applicability_conditions": ["Goods sold by description or technical specification"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "sale_of_goods_act_1930",
                "section_id": "17",
                "provision_relevance_rationale": "Sale by sample: bulk must correspond with sample in quality, and goods free from unapparent unmerchantable defects.",
                "relevance_classification": "CONDITIONALLY_APPLICABLE",
                "applicable_legal_elements": ["Bulk must correspond with sample", "Reasonable opportunity to compare"],
                "applicability_conditions": ["Sale was made based on approved sample"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "contract_act_1872",
                "section_id": "73",
                "provision_relevance_rationale": "Damages for breach of contract including transportation and storage losses.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Compensation for direct loss naturally arising from breach"],
                "applicability_conditions": ["Financial loss sustained"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "unpaid_seller_lien_and_resale": {
        "issue_id": "unpaid_seller_lien_and_resale",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Unpaid Seller's Statutory Lien, Stoppage in Transit & Resale",
        "issue_definition": "Manufacturer, distributor, or supplier exercising statutory lien to withhold delivery, stop goods in transit, or resell goods after buyer defaulted on payment.",
        "prototype_texts": [
            "Buyer failed to pay balance 10 lakhs for manufactured goods, can I exercise unpaid seller lien and resell goods to another customer?",
            "Buyer became insolvent while goods were with transport logistics carrier, how to exercise stoppage in transit under Sale of Goods Act?",
            "Supplier suing buyer for full contract price under Section 55 after buyer refused delivery of customized machinery.",
            "ಖರೀದಿದಾರನು ಹಣ ಪಾವತಿಸದಿದ್ದಾಗ ತಯಾರಕರು ಸರಕುಗಳ ಮೇಲೆ ಲಿಯನ್ ಹಕ್ಕು ಚಲಾಯಿಸಿ ಬೇರೆಯವರಿಗೆ ಮರುಮಾರಾಟ ಮಾಡಬಹುದೇ?",
            "खरीदार ने माल तैयार होने के बाद पेमेंट रोक दिया, क्या विक्रेता माल रोककर किसी और को बेच सकता है और नुकसान की भरपाई मांग सकता है।"
        ],
        "provision_references": [
            {
                "act_id": "sale_of_goods_act_1930",
                "section_id": "46",
                "provision_relevance_rationale": "Statutory rights of unpaid seller: lien on goods for price while in possession, stoppage in transit upon buyer insolvency, and right of resale.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Whole of price has not been paid or tendered", "Statutory lien while in possession", "Right of stoppage in transit", "Right of resale"],
                "applicability_conditions": ["Seller is unpaid and retains possession or goods in transit"],
                "missing_facts": ["Payment terms, invoices, and notice of resale issued to buyer"],
                "exceptions": ["Lien lost once buyer lawfully obtains physical possession"]
            },
            {
                "act_id": "sale_of_goods_act_1930",
                "section_id": "55",
                "provision_relevance_rationale": "Statutory right of seller to sue buyer for full contract price where property in goods has passed.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Property in goods passed to buyer", "Buyer wrongfully neglects or refuses to pay"],
                "applicability_conditions": ["Ownership passed to buyer"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "sale_of_goods_act_1930",
                "section_id": "56",
                "provision_relevance_rationale": "Suit for damages for wrongful non-acceptance representing difference between contract price and market price.",
                "relevance_classification": "CONDITIONALLY_APPLICABLE",
                "applicable_legal_elements": ["Buyer wrongfully refuses to accept goods", "Damages for non-acceptance"],
                "applicability_conditions": ["Goods not accepted by buyer"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "pawn_pledge_collateral_default_dispute": {
        "issue_id": "pawn_pledge_collateral_default_dispute",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Pledged Collateral, Gold Loan Auction & Section 176 Notice",
        "issue_definition": "Bank, NBFC, or pawnbroker auctioning pledged gold jewelry, vehicles, or shares without giving mandatory reasonable written notice under Section 176 Contract Act.",
        "prototype_texts": [
            "Gold loan company auctioned family jewelry without giving me reasonable notice of sale after I delayed interest payment by one month.",
            "NBFC sold pledged commercial vehicle without serving statutory auction notice and refusing to refund surplus money.",
            "Can a gold loan lender secretly sell pledged ornaments without sending a registered notice of sale under Section 176?",
            "ಚಿನ್ನದ ಸಾಲದ ಬಡ್ಡಿಯನ್ನು ಒಂದು ತಿಂಗಳು ತಡವಾಗಿ ಕಟ್ಟಿದ್ದಕ್ಕೆ ಬ್ಯಾಂಕಿನವರು ಯಾವುದೇ ಮುನ್ಸೂಚನೆ ನೋಟಿಸ್ ನೀಡದೆ ಚಿನ್ನವನ್ನು ಹರಾಜು ಹಾಕಿದ್ದಾರೆ.",
            "गोल्ड लोन कंपनी ने बिना कोई कानूनी नोटिस दिए गिरवी रखे सोने के गहने नीलाम कर दिए और सरप्लस पैसा भी नहीं लौटा रहे हैं।"
        ],
        "provision_references": [
            {
                "act_id": "contract_act_1872",
                "section_id": "176",
                "provision_relevance_rationale": "Mandates that pawnee can only sell pledged goods upon giving reasonable notice of sale to pawnor; sale without notice is illegal conversion and surplus must be returned.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Default in payment of pledged debt", "Mandatory requirement: pawnee MUST give reasonable notice of sale to pawnor", "Surplus sale proceeds must be paid over to borrower"],
                "applicability_conditions": ["Goods pledged as collateral security", "Lender conducted auction or sale"],
                "missing_facts": ["Proof of lack of prior written auction notice"],
                "exceptions": ["Statutory requirement of reasonable notice cannot be contracted out (PTC India case)"]
            },
            {
                "act_id": "contract_act_1872",
                "section_id": "172",
                "provision_relevance_rationale": "Defines pledge: bailment of goods as security for payment of debt.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Bailment of goods as security for debt"],
                "applicability_conditions": ["Pledge relationship established"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "cpa_2019",
                "section_id": "2_11",
                "provision_relevance_rationale": "Auction of gold without statutory notice constitutes gross deficiency in financial service and unfair trade practice.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Deficiency of banking/NBFC service", "Compensation for sentimental value and gold price appreciation"],
                "applicability_conditions": ["Consumer relationship with lending institution"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "unstamped_commercial_agreement_impoundment": {
        "issue_id": "unstamped_commercial_agreement_impoundment",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Unstamped Commercial Contract & Section 33/35 Impounding",
        "issue_definition": "Commercial contract, indemnity bond, or lease executed on deficient or zero stamp paper, rendering it inadmissible in court and liable to impounding with 10x penalty.",
        "prototype_texts": [
            "We executed a commercial consultancy agreement on plain paper without stamp duty, can it be admitted in court if opposite party disputes payment?",
            "Court impounded our partnership agreement for insufficient stamp duty demanding 10 times penalty under Section 35 of Stamp Act.",
            "Can an agreement executed on 100 rupees stamp paper instead of required 0.5% ad valorem stamp duty be enforced in arbitration?",
            "ಸಾಕಷ್ಟು ಸ್ಟಾಂಪ್ ಶುಲ್ಕ ಪಾವತಿಸದ ಕರಾರು ಪತ್ರವನ್ನು ನ್ಯಾಯಾಲಯದಲ್ಲಿ ಸಾಕ್ಷ್ಯವಾಗಿ ಹಾಜರುಪಡಿಸಬಹುದೇ ಮತ್ತು ಹತ್ತು ಪಟ್ಟು ದಂಡ ಹೇಗೆ?",
            "बिना स्टांप ड्यूटी या कम स्टांप पेपर पर किए गए कमर्शियल एग्रीमेंट को कोर्ट ने अमान्य घोषित कर 10 गुना पेनल्टी लगा दी है।"
        ],
        "provision_references": [
            {
                "act_id": "indian_stamp_act_1899",
                "section_id": "33",
                "provision_relevance_rationale": "Mandates that every court or public authority before whom an insufficiently stamped instrument is produced MUST impound it.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Instrument chargeable with stamp duty", "Produced before public officer or court", "Mandatory statutory impoundment for deficient duty"],
                "applicability_conditions": ["Stamp duty paid is less than prescribed Schedule rate"],
                "missing_facts": ["Original document and stamp duty paid vs applicable state tariff"],
                "exceptions": []
            },
            {
                "act_id": "indian_stamp_act_1899",
                "section_id": "35",
                "provision_relevance_rationale": "Inadmissibility: no instrument chargeable with duty shall be admitted in evidence unless deficient duty plus 10x penalty is paid.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Instrument inadmissible in evidence for any purpose", "Admissible only on payment of deficient duty plus penalty up to ten times"],
                "applicability_conditions": ["Party seeks to tender document in evidence"],
                "missing_facts": [],
                "exceptions": ["Curable defect: document becomes fully admissible once deficit stamp duty and penalty are paid"]
            },
            {
                "act_id": "karnataka_stamp_act_1957",
                "section_id": "33",
                "provision_relevance_rationale": "State stamp law parallel: mandatory impounding of insufficiently stamped instruments in Karnataka.",
                "relevance_classification": "CONDITIONALLY_APPLICABLE",
                "applicable_legal_elements": ["Impounding under Karnataka Stamp Act"],
                "applicability_conditions": ["Document executed in or relating to property in Karnataka"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    },
    "partnership_firm_unregistered_suit_bar": {
        "issue_id": "partnership_firm_unregistered_suit_bar",
        "taxonomy_status": "taxonomy_supported",
        "domain_id": "contractual_disputes",
        "display_name": "Unregistered Partnership Firm Statutory Bar on Suits (Section 69)",
        "issue_definition": "Unregistered partnership firm or partner barred from filing a civil suit to enforce contractual rights against third parties or between co-partners under Section 69 Partnership Act.",
        "prototype_texts": [
            "Our partnership firm is not registered with Registrar of Firms, can we file a recovery suit against a defaulting client for 20 lakhs?",
            "Defendant filed application to dismiss our commercial suit on ground that plaintiff partnership firm is unregistered under Section 69.",
            "Can an unregistered partner sue co-partners for accounts and dissolution of business?",
            "ರಿಜಿಸ್ಟ್ರಾರ್ ಆಫ್ ಫರ್ಮ್ಸ್‌ನಲ್ಲಿ ನೋಂದಣಿ ಮಾಡಿಸದ ಪಾಲುದಾರಿಕೆ ಸಂಸ್ಥೆಯು ಗ್ರಾಹಕರ ವಿರುದ್ಧ ಬಾಕಿ ಹಣ ವಸೂಲಿಗಾಗಿ ಕೋರ್ಟ್‌ನಲ್ಲಿ ಕೇಸ್ ಹಾಕಬಹುದೇ?",
            "रजिस्ट्रार के पास फर्म का रजिस्ट्रेशन न होने पर क्लाइंट से पेमेंट वसूली का केस धारा 69 पार्टनरशिप एक्ट में खारिज हो गया है।"
        ],
        "provision_references": [
            {
                "act_id": "partnership_act_1932",
                "section_id": "69",
                "provision_relevance_rationale": "Absolute statutory bar: no suit to enforce a right arising from a contract shall be instituted in any court by or on behalf of an unregistered firm against any third party.",
                "relevance_classification": "DIRECTLY_APPLICABLE",
                "applicable_legal_elements": ["Suit to enforce contractual right", "Plaintiff firm is not registered with Registrar of Firms", "Or persons suing are not shown in Register of Firms as partners", "Absolute statutory bar on filing suit"],
                "applicability_conditions": ["Suit arises out of contract against third party or between partners"],
                "missing_facts": ["Form A acknowledgment from Registrar of Firms"],
                "exceptions": ["Does not bar suit for dissolution of firm or for accounts of dissolved firm under Section 69(3)(a)"]
            },
            {
                "act_id": "partnership_act_1932",
                "section_id": "48",
                "provision_relevance_rationale": "Mode of settlement of accounts between partners upon dissolution.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Settlement of partnership accounts upon dissolution"],
                "applicability_conditions": ["Partnership dissolution proceedings"],
                "missing_facts": [],
                "exceptions": []
            },
            {
                "act_id": "commercial_courts_act_2015",
                "section_id": "12A",
                "provision_relevance_rationale": "Unregistered firm can still explore pre-institution mediation since mediation is not a formal suit barred by Section 69.",
                "relevance_classification": "SUPPORTING_PROVISION",
                "applicable_legal_elements": ["Pre-institution mediation avenue"],
                "applicability_conditions": ["Commercial dispute mediation"],
                "missing_facts": [],
                "exceptions": []
            }
        ]
    }
}

NEW_GUIDANCE = {
    "cyber_digital_evidence_admissibility": {
        "action_steps": [
            "Preserve original mobile phones, hard drives, and cloud backups without altering metadata or deleting messages.",
            "Export raw chat archives, email headers, and bank account statement PDFs containing transaction reference numbers.",
            "Draft and execute a statutory Electronic Certificate under Section 63 of Bharatiya Sakshya Adhiniyam, 2023 detailing device serial number and operating integrity.",
            "Obtain signed bank transaction certificates with official bank seal confirming unauthorized debit details.",
            "Submit the Section 63 certificate along with printouts to the Cyber Crime Police Station or Trial Court."
        ],
        "portal_ids": ["cybercrime_gov_in", "ecourts_services"]
    },
    "cyber_ransomware_data_kidnapping": {
        "action_steps": [
            "Immediately isolate affected computers and disconnect network cables and Wi-Fi to stop lateral spread.",
            "Preserve ransomware note, encrypted sample files, attacker Bitcoin wallet address, and firewall logs as forensic evidence.",
            "File a high-priority incident report immediately on the National Cyber Crime Reporting Portal under extortion/ransomware.",
            "Submit mandatory 6-hour cybersecurity incident reporting to CERT-In (incident@cert-in.org.in) under IT Act Section 70B.",
            "Do NOT pay ransom; engage professional cybersecurity recovery specialists and restore clean data from offline backups."
        ],
        "portal_ids": ["cybercrime_gov_in", "cert_in"]
    },
    "telemarketing_spoofing_trai_violation": {
        "action_steps": [
            "Activate full Do Not Disturb (DND) by sending SMS 'START 0' to 1909 or via your telecom operator app.",
            "Report the spam call or SMS within 3 days by SMSing 'COMPLAINT <call/sms text>, <number>, <dd/mm/yy>' to 1909.",
            "Report fraudulent header spoofing and suspicious numbers on Sanchar Saathi (Chakshu facility) of DoT.",
            "File a formal grievance on TRAI DND 3.0 mobile application or portal against telecom operator non-compliance.",
            "If financial phishing was attempted, report immediately on National Cyber Crime Portal or call 1930."
        ],
        "portal_ids": ["sanchar_saathi_chakshu", "trai_dnd", "tdsat_portal"]
    },
    "cyber_adjudicating_officer_compensation": {
        "action_steps": [
            "Gather all bank statements, police FIR, transaction logs, and written bank dispute rejection letters.",
            "Compute the exact financial loss and interest sustained, ensuring the total claim is within Rs 5 Crore.",
            "Draft a formal Petition under Section 46 of Information Technology Act, 2000 in prescribed format with fee.",
            "File the petition before the designated Adjudicating Officer (Secretary, Information Technology Department of your State).",
            "Serve notice upon the opposite party (bank or fraudster) and appear before the Adjudicating Officer for summary inquiry."
        ],
        "portal_ids": ["cybercrime_gov_in", "tdsat_portal", "rbi_cms"]
    },
    "cyber_mule_account_money_laundering": {
        "action_steps": [
            "Obtain written reason from your home branch specifying which police cyber cell placed the debit freeze or lien.",
            "Contact the Investigating Officer of the concerned Cyber Crime Cell with bank statements proving your legitimate source of income.",
            "Provide all communication, advertisements, or scam messages showing you were an innocent victim without criminal intent.",
            "Apply before the jurisdictional Judicial Magistrate under BNSS Section 107 / CrPC 457 for defreezing or releasing lien.",
            "File an official complaint on the National Cyber Crime Reporting Portal detailing how your credentials were misused."
        ],
        "portal_ids": ["cybercrime_gov_in", "ecourts_services", "cctns_citizen"]
    },
    "product_liability_defective_good_injury": {
        "action_steps": [
            "Preserve the defective product, broken parts, packaging, invoice, and warranty card in safe custody without altering them.",
            "Obtain comprehensive medical records, doctor treatment certificates, hospital bills, and photographic proof of injury/damage.",
            "Send a formal Legal Notice to the product manufacturer and seller demanding product liability compensation under CPA 2019.",
            "Lodge a consumer grievance on the National Consumer Helpline (NCH INGRAM portal) seeking manufacturer response.",
            "File a Product Liability Complaint before the District Consumer Commission via e-Daakhil for compensation and medical damages."
        ],
        "portal_ids": ["edaakhil", "consumer_helpline_ingram", "bis_manakonline"]
    },
    "anti_competitive_cartel_price_fixing": {
        "action_steps": [
            "Collect documentary evidence: school circulars, vendor invoices, price comparison lists, or identical cartel pricing quotes.",
            "Draft a formal Information Petition under Section 19(1)(a) of the Competition Act, 2002 detailing anti-competitive practices.",
            "Pay the prescribed statutory filing fee as specified by Competition Commission of India (General) Regulations.",
            "File the information petition before the Competition Commission of India (CCI) in New Delhi or via its online portal.",
            "Also lodge an Unfair Trade Practice complaint on the National Consumer Helpline or District Consumer Commission."
        ],
        "portal_ids": ["cci_portal", "consumer_helpline_ingram", "edaakhil"]
    },
    "packaged_commodity_mrp_tampering_overcharging": {
        "action_steps": [
            "Retain the pre-packaged item and take clear photographs of the printed Maximum Retail Price (MRP) and tampered stickers.",
            "Demand a printed tax invoice or cash receipt explicitly showing the price charged above MRP.",
            "Lodge an immediate complaint with the Controller of Legal Metrology (Weights and Measures Department) of your State.",
            "Register an online consumer grievance on the National Consumer Helpline (NCH - INGRAM) with attached photos and receipt.",
            "File an Unfair Trade Practice claim before the District Consumer Commission via e-Daakhil seeking refund, penalty, and costs."
        ],
        "portal_ids": ["consumer_helpline_ingram", "edaakhil"]
    },
    "substandard_adulterated_food_toxic_illness": {
        "action_steps": [
            "Preserve the contaminated food sample in a clean container, photograph the foreign matter/insect, and keep the restaurant bill.",
            "Seek immediate medical attention and obtain medical test reports and hospital discharge summary confirming food poisoning.",
            "File an urgent complaint on the FSSAI FoSCoS portal to trigger an immediate food safety inspection of the restaurant premises.",
            "Lodge an official grievance on the food delivery app and National Consumer Helpline (NCH) demanding full refund.",
            "File a Product Liability and deficiency complaint before District Consumer Commission on e-Daakhil claiming medical compensation."
        ],
        "portal_ids": ["fssai_foscos", "edaakhil", "consumer_helpline_ingram"]
    },
    "insurance_ombudsman_claim_repudiation_dispute": {
        "action_steps": [
            "Submit a formal written representation to the Grievance Redressal Officer (GRO) of the insurance company detailing policy history.",
            "If insurer rejects representation or fails to resolve within 30 days, draft a complaint for the Insurance Ombudsman.",
            "File complaint before the Insurance Ombudsman under Insurance Ombudsman Rules 2017 via the Council for Insurance Ombudsmen portal.",
            "Attach policy copy, claim rejection letter, medical discharge summary, and doctor prescription proofs.",
            "Attend Ombudsman summary hearing; awards up to Rs 50 Lakhs are binding on the insurer without any court fees."
        ],
        "portal_ids": ["cio_bima_portal", "irdai_bima_bharosa", "edaakhil"]
    },
    "spurious_cosmetics_adulterated_drugs": {
        "action_steps": [
            "Retain the medicine/cosmetic packaging, bottle, batch number details, and official chemist purchase invoice.",
            "Consult a medical specialist/dermatologist and secure a clinical certificate detailing allergic burn or adverse reaction.",
            "Lodge a formal complaint with the State Drugs Controller / Food & Drug Administration (FDA) for statutory laboratory testing.",
            "Register a complaint on the National Consumer Helpline (NCH) and e-Daakhil for seller/manufacturer product liability.",
            "If medicine caused serious harm, file a police complaint under Drugs and Cosmetics Act Section 27 and BNS Section 318."
        ],
        "portal_ids": ["consumer_helpline_ingram", "edaakhil", "cctns_citizen"]
    },
    "unlawful_electricity_disconnection_meter_dispute": {
        "action_steps": [
            "Check whether electricity distribution company (DISCOM) served mandatory 15 clear days written notice before disconnection.",
            "Deposit disputed electricity charge 'under protest' if necessary to compel immediate statutory power restoration under Section 56.",
            "File an urgent complaint before the Consumer Grievance Redressal Forum (CGRF) of your power utility for interim reconnection.",
            "If CGRF fails to resolve or rejects complaint within 60 days, appeal before the State Electricity Ombudsman.",
            "File a Consumer Commission complaint on e-Daakhil claiming compensation for wrongful disconnection of essential service."
        ],
        "portal_ids": ["edaakhil", "consumer_helpline_ingram", "cpgrams"]
    },
    "traffic_enforcing_officer_violation_double_penalty": {
        "action_steps": [
            "Capture clear, non-confrontational video, dashcam, or photographic evidence showing officer uniform, name badge, and vehicle registration number.",
            "Note exact location, time, and traffic police jurisdiction where the violation occurred.",
            "Lodge a formal complaint on the State Police / Traffic Police Citizen Vigilance portal citing MV Act Section 210B (double fine).",
            "If illegal gratification or cash bribe was demanded, call Anti-Corruption Bureau / CBI helpline 1064 or report on CVC portal.",
            "File a public grievance on CPGRAMS or State Lokayukta attaching video evidence for departmental disciplinary action."
        ],
        "portal_ids": ["central_vigilance_commission", "cbi_anti_corruption", "karnataka_lokayukta", "cpgrams"]
    },
    "driving_while_disqualified_revoked_licence": {
        "action_steps": [
            "Cease driving immediately; driving while disqualified attracts mandatory Section 182 criminal prosecution and fine up to Rs 10,000.",
            "Check Parivahan Sarathi portal to verify the exact period and grounds of suspension recorded by the licensing authority.",
            "If suspension was issued without show-cause notice, file a statutory appeal before the Appellate Authority under Section 19(3) MV Act.",
            "If disqualification period has elapsed, apply formally on Parivahan portal for restoration of driving licence.",
            "Attend the Judicial Magistrate Court on summons date with legal counsel to contest or compound the Section 182 charge."
        ],
        "portal_ids": ["parivahan", "vcourts", "ecourts_services"]
    },
    "mentally_physically_unfit_driving": {
        "action_steps": [
            "Obtain a comprehensive medical fitness assessment from a government registered medical practitioner (Form 1-A).",
            "If medical condition is temporary, surrender driving licence voluntarily to RTO until full medical recovery.",
            "If disability is permanent, apply for an 'adapted vehicle' endorsement or invalid carriage licence under CMVR rules.",
            "If booked under Section 186, present medical specialist certificates before the Traffic Court to prove lack of dangerous intent.",
            "Ensure that private insurance company is notified of medical modifications to keep third-party insurance coverage intact."
        ],
        "portal_ids": ["parivahan", "vcourts"]
    },
    "mandatory_vehicle_safety_recall_defect": {
        "action_steps": [
            "Obtain authorized service center job cards and diagnostic reports documenting recurring steering, brake, or battery failure.",
            "Check Ministry of Road Transport and Highways (MoRTH) vehicle recall portal to see if similar defects are reported for your model.",
            "Lodge a formal defect and safety complaint on the MoRTH portal under Section 110A MV Act demanding mandatory recall.",
            "Send a statutory Legal Notice to manufacturer and dealer demanding full vehicle replacement or 100% price refund.",
            "File a Product Liability Complaint before State or National Consumer Commission via e-Daakhil claiming vehicle replacement."
        ],
        "portal_ids": ["parivahan", "edaakhil", "consumer_helpline_ingram"]
    },
    "hit_and_run_statutory_solatium_compensation": {
        "action_steps": [
            "Register an immediate police FIR at the local police station certifying that the accident was caused by an unknown/untraced vehicle.",
            "Obtain certified copies of FIR, post-mortem report (in case of death), or medical injury certificate from government hospital.",
            "Submit Form I Application for Compensation under Hit and Run Motor Accidents Scheme to the Claim Enquiry Officer (Sub-Divisional Magistrate).",
            "The Claim Enquiry Officer sanctions Rs 2 Lakhs (death) or Rs 50,000 (grievous injury) payable directly from the Solatium Fund.",
            "If offending vehicle is subsequently identified by police, file a comprehensive claim before MACT under Section 166 for full damages."
        ],
        "portal_ids": ["solatium_fund_morth", "parivahan", "ecourts_services"]
    },
    "traffic_obstruction_unreasonable_towing_charges": {
        "action_steps": [
            "Take photographs of vehicle location showing breakdown condition, hazard lights, or absence of mandatory No-Parking signboards.",
            "Demand a printed government receipt with vehicle number, towing agency name, and breakdown of fine vs actual towing charge.",
            "If vehicle was damaged during towing, document dents/scratches immediately at the traffic police yard with video.",
            "Lodge a formal complaint on the Parivahan NextGen eChallan Grievance System challenging unlawful towing fee.",
            "If towing occurred while driver/passenger was seated inside, file complaint before City Traffic Commissioner citing violation of towing rules."
        ],
        "portal_ids": ["echallan_grievance", "parivahan", "cpgrams"]
    },
    "statutory_14_day_traffic_prosecution_notice_defense": {
        "action_steps": [
            "Check the timestamp of the alleged traffic violation vs the exact date and time the challan was generated and SMS/notice delivered.",
            "Download certified digital challan copy from Parivahan eChallan portal showing date of dispatch.",
            "If more than 14 days elapsed without on-spot warning or notice, raise a formal dispute on the eChallan Grievance Portal citing Section 209.",
            "If matter is referred to Virtual Court or Regular Traffic Court, submit written application pleading Section 209 statutory bar.",
            "The Magistrate Court is statutorily bound to dismiss the speeding/dangerous driving prosecution where notice was served after 14 days."
        ],
        "portal_ids": ["echallan_grievance", "vcourts", "parivahan"]
    },
    "national_highway_toll_obstruction_dispute": {
        "action_steps": [
            "Retain toll receipt and screenshot of active FASTag balance at the exact time of crossing toll plaza.",
            "If toll scanner was non-functional and double cash was charged, call NHAI National Highway Helpline 1033 immediately.",
            "Lodge an online complaint on National Highways Authority of India (NHAI) grievance portal detailing toll plaza name and lane.",
            "If FASTag was debited twice, raise a chargeback dispute through your issuing bank or FASTag wallet app within 15 days.",
            "File consumer service deficiency claim on National Consumer Helpline (NCH) seeking refund of excess toll and compensation."
        ],
        "portal_ids": ["cpgrams", "consumer_helpline_ingram", "parivahan"]
    },
    "statutory_subsistence_allowance_suspension": {
        "action_steps": [
            "Send a formal written demand letter to management requesting immediate payment of statutory subsistence allowance under Section 10A.",
            "Ensure that you do not take up any alternate employment during suspension and submit a formal non-employment certificate to employer.",
            "If employer refuses to pay within 30 days, file an application before the Labour Commissioner / Authority under Payment of Wages Act.",
            "File a recovery application under Section 33C(2) of Industrial Disputes Act before the Labour Court for computation of unpaid arrears.",
            "Remind the inquiry officer that domestic inquiry proceedings are legally void and termination invalid if subsistence allowance is withheld."
        ],
        "portal_ids": ["samadhan", "shram_suvidha", "ecourts_services"]
    },
    "unilateral_change_in_service_conditions_without_notice": {
        "action_steps": [
            "Submit a formal written protest letter to management stating that the change violates Section 9A of Industrial Disputes Act 1947.",
            "Gather employment contracts, appointment letters, past pay slips, and shift rosters proving existing service conditions.",
            "File an industrial dispute complaint before the local Conciliation Officer / Assistant Labour Commissioner on the Samadhan portal.",
            "Request the Conciliation Officer to issue an interim direction to employer to maintain status quo on shift timings and wages.",
            "If conciliation fails, request reference of dispute to Labour Court under Section 10 for adjudication and quashing of unilateral change."
        ],
        "portal_ids": ["samadhan", "shram_suvidha"]
    },
    "statutory_annual_bonus_non_payment_profitable_unit": {
        "action_steps": [
            "Calculate your statutory bonus entitlement (minimum 8.33% of basic wage + DA earned during the accounting year).",
            "Send a written demand to the employer citing Section 8 and Section 10 of Payment of Bonus Act 1965.",
            "If payment is not disbursed within 8 months of financial year close, file a complaint before the Labour Inspector / Labour Commissioner.",
            "File a formal recovery application on the Ministry of Labour Samadhan Portal under Section 21 of Payment of Bonus Act.",
            "Labour Officer can issue recovery certificate to District Collector to recover unpaid bonus as arrears of land revenue."
        ],
        "portal_ids": ["samadhan", "shram_suvidha"]
    },
    "individual_workman_termination_industrial_dispute": {
        "action_steps": [
            "Gather appointment letter, payslips, attendance records, and termination letter/email.",
            "Send a legal demand notice for reinstatement with back wages to employer within 30 days of termination.",
            "File an individual industrial dispute under Section 2A before the Conciliation Officer on the Samadhan portal.",
            "If conciliation fails or after expiry of 3 months from application date, apply directly to the Labour Court for adjudication.",
            "Labour Court conducts judicial trial and can award full reinstatement with continuous service, back wages, or heavy compensation."
        ],
        "portal_ids": ["samadhan", "shram_suvidha", "ecourts_services"]
    },
    "retaliatory_action_posh_complainant": {
        "action_steps": [
            "Document every retaliatory action in writing: adverse appraisals, sudden transfers, exclusion from meetings, and abusive messages.",
            "Submit a formal complaint of retaliation and hostile work environment to the Internal Committee (IC) and senior leadership.",
            "Request interim relief under Section 12 POSH Act: transfer of respondent, grant of up to 3 months paid leave, or reporting reassignment.",
            "If IC report is biased or employer retaliates, file a statutory appeal under Section 18 within 90 days before the Appellate Authority.",
            "Register a complaint on the Ministry of Women & Child Development SHe-Box portal for government monitoring of the workplace inquiry."
        ],
        "portal_ids": ["shebox_portal", "samadhan", "ecourts_services"]
    },
    "unlawful_alteration_of_service_conditions_during_conciliation": {
        "action_steps": [
            "Notify the Conciliation Officer immediately in writing that employer altered service conditions or terminated worker during conciliation.",
            "Submit copy of the conciliation notice showing the dispute was actively sub-judice when the employer took punitive action.",
            "File a formal complaint under Section 33A of Industrial Disputes Act before the Conciliation Officer / Labour Court.",
            "Section 33A complaint is adjudicated as a regular dispute, and the illegal termination or wage cut is treated as void ab initio.",
            "Seek immediate interim order for status quo and restoration of salary payment pending final conciliation report."
        ],
        "portal_ids": ["samadhan", "shram_suvidha"]
    },
    "commercial_dispute_mandatory_pre_institution_mediation": {
        "action_steps": [
            "Compile all commercial contracts, purchase orders, invoices, delivery challans, and demand notices.",
            "Ensure that total commercial claim exceeds specified pecuniary value under Commercial Courts Act.",
            "Submit an application for Pre-Institution Mediation before the District Legal Services Authority (DLSA) in prescribed Form 1.",
            "DLSA issues notice to opposite party and conducts mediation sessions to explore mutually agreeable monetary settlement.",
            "If settlement is arrived, it carries status of arbitral award; if mediation fails (Non-Starter Report), file commercial court suit."
        ],
        "portal_ids": ["nalsa", "ecourts_services"]
    },
    "unregistered_lease_immovable_property_dispute": {
        "action_steps": [
            "Review lease agreement terms; if duration exceeds 11 months and is unregistered, it is legally deemed a month-to-month tenancy.",
            "Serve a formal 15-day statutory Notice to Quit in writing under Section 106 of Transfer of Property Act 1882.",
            "Preserve bank statements showing monthly rent transfers to establish tenancy relationship and collateral possession.",
            "If tenant refuses to vacate after notice period, file a civil suit for eviction and recovery of mesne profits/arrears.",
            "If security deposit was wrongfully withheld by landlord, file civil recovery suit under Contract Act Section 73 within 3 years."
        ],
        "portal_ids": ["ecourts_services"]
    },
    "part_performance_possession_protection": {
        "action_steps": [
            "Gather written agreement to sell, full or partial payment receipts, bank statement debits, and physical possession handover letter.",
            "Preserve utility bills (electricity, water), property tax receipts, or municipal voter ID showing your physical possession.",
            "Send a legal notice to seller affirming continuous readiness and willingness to pay balance consideration and execute sale deed.",
            "If seller threatens illegal dispossession, file a civil suit for Permanent Injunction restraining eviction under Section 53A TPA.",
            "Simultaneously file a suit for Specific Performance of Contract under Section 10 of Specific Relief Act within 3 years."
        ],
        "portal_ids": ["ecourts_services"]
    },
    "specific_performance_readiness_willingness_dispute": {
        "action_steps": [
            "Issue a formal legal notice to seller before agreement expiry date expressing unconditional readiness to pay balance sale price.",
            "Compile documentary proof of financial readiness: bank account balance, fixed deposit receipts, or sanctioned home loan letters.",
            "Attend the Sub-Registrar office on the agreed date, mark your presence with an attendance receipt, and notify the seller.",
            "File a suit for Specific Performance of Agreement to Sell before the Civil Court within 3 years limitation period under Article 54.",
            "Seek interim temporary injunction under Order XXXIX CPC restraining the seller from creating third-party rights or selling land."
        ],
        "portal_ids": ["ecourts_services"]
    },
    "condition_vs_warranty_breach_sale_of_goods": {
        "action_steps": [
            "Inspect delivered goods immediately upon arrival and document deviations from purchase order specifications with photographs.",
            "Issue a formal Rejection Notice in writing to the seller within reasonable time explicitly repudiating the contract under Section 12.",
            "Store rejected goods safely at seller risk and expense without using them commercially (commercial use waives rejection right).",
            "Obtain an independent government/NABL accredited laboratory test certificate proving failure to meet core technical standards.",
            "File a commercial suit for refund of advance payment, freight charges, and damages under Sale of Goods Act Section 57."
        ],
        "portal_ids": ["ecourts_services", "msme_samadhaan"]
    },
    "unpaid_seller_lien_and_resale": {
        "action_steps": [
            "Check that goods are still in your physical custody or in transit with third-party logistics/transporter.",
            "Serve a formal written Notice of Unpaid Seller Lien to the buyer demanding payment of balance invoice price within 7 days.",
            "If goods are in transit and buyer is insolvent, send written stoppage-in-transit notice to the carrier under Section 50.",
            "If buyer fails to tender payment, send notice of intention to resell under Section 54 and resell goods in open market.",
            "File suit against buyer for balance deficit between contract price and resale proceeds under Section 55/56."
        ],
        "portal_ids": ["msme_samadhaan", "ecourts_services"]
    },
    "pawn_pledge_collateral_default_dispute": {
        "action_steps": [
            "Check the gold loan pawn ticket, loan agreement, and interest payment receipts.",
            "Verify whether the lender issued a formal written Notice of Sale specifying date, time, and reserve price of auction under Section 176.",
            "If auction was conducted without statutory reasonable notice, send legal notice alleging unlawful conversion and deficiency.",
            "Demand complete accounting statement of auction proceeds, sale price realized, and immediate refund of surplus balance.",
            "File a consumer complaint on e-Daakhil or RBI Banking Ombudsman portal claiming return of gold or market compensation."
        ],
        "portal_ids": ["rbi_cms", "edaakhil", "consumer_helpline_ingram"]
    },
    "unstamped_commercial_agreement_impoundment": {
        "action_steps": [
            "Examine whether agreement was executed on required ad valorem stamp paper according to relevant State Stamp Act Schedule.",
            "If agreement is unstamped, it cannot be produced in court or arbitration without paying deficit duty plus penalty up to 10x.",
            "Submit the document voluntarily to the District Collector / Sub-Registrar of Stamps under Section 31 for adjudication of duty.",
            "Pay the deficit stamp duty and mitigated penalty as assessed by the Collector of Stamps to obtain valid endorsement under Section 42.",
            "Once stamped and certified by the Collector, the agreement becomes fully admissible in court and enforceable in arbitration."
        ],
        "portal_ids": ["ecourts_services"]
    },
    "partnership_firm_unregistered_suit_bar": {
        "action_steps": [
            "Check whether partnership deed was registered with the Registrar of Firms (ROF) in your State and Form A was issued.",
            "If firm is unregistered, it is barred from filing a regular civil recovery suit against third parties under Section 69(2).",
            "Apply immediately for registration of the partnership firm with the Registrar of Firms before initiating court proceedings.",
            "Explore Pre-Institution Mediation under Section 12A Commercial Courts Act, as mediation is not barred by Section 69.",
            "If partners have an internal dispute, file a suit for formal Dissolution and Accounts under Section 69(3)(a) which is statutorily exempt from the bar."
        ],
        "portal_ids": ["mca_portal", "nalsa", "ecourts_services"]
    }
}

