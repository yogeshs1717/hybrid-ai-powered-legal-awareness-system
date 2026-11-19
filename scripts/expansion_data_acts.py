"""Expansion data for Acts and Sections across the five LegalLens domains.
Authoritative statutory texts from India Code (https://www.indiacode.nic.in).
Every section contains all 15 required legal attributes.
"""

NEW_ACTS = {
    "bharatiya_sakshya_adhiniyam_2023": {
        "official_act_name": "Bharatiya Sakshya Adhiniyam, 2023",
        "act_year": 2023,
        "short_name": "BSA 2023",
        "official_source_name": "India Code",
        "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/20061/1/a2023-47.pdf",
        "sections": {
            "57": {
                "section_number": "57",
                "official_section_title": "Primary evidence",
                "official_text": "Primary evidence means the document itself produced for the inspection of the Court. Explanation 1.—Where a document is executed in several parts, each part is primary evidence of the document... Explanation 5.—Where an electronic or digital record is created or stored, and such storage occurs simultaneously or sequentially in multiple files, each such file is primary evidence.",
                "simplified_explanation": "Establishes that electronic or digital files stored across computer hard drives, cloud backups, or smartphones constitute primary evidence that courts must accept without secondary certification if the file itself is produced directly.",
                "legal_ingredients": [
                    "Document or digital record produced directly for inspection of Court",
                    "Electronic or digital record created or stored in digital medium",
                    "Simultaneous or sequential storage occurring across multiple files or devices"
                ],
                "domain": "cyber_fraud",
                "relevant_issues": [
                    "cyber_digital_evidence_admissibility",
                    "otp_fraud",
                    "online_impersonation",
                    "unauthorized_account_access"
                ],
                "punishment_or_remedy": "Admissibility as primary proof in criminal trials and civil proceedings.",
                "related_provisions": [
                    "BSA 2023 Section 61",
                    "BSA 2023 Section 63",
                    "IT Act 2000 Section 4"
                ],
                "exceptions_and_limitations": [
                    "Where the primary digital file is inaccessible or destroyed, secondary electronic evidence may be led subject to Section 63 certificate."
                ],
                "amendment_status": "In force; commenced on 1st July 2024 via Gazette Notification S.O. 2790(E).",
                "jurisdiction": "Central (Applies to all courts and judicial proceedings in India).",
                "applicability_notes": "Essential evidentiary section for all cyber fraud prosecutions and electronic transaction disputes.",
                "keywords": [
                    "primary evidence",
                    "electronic record",
                    "digital record",
                    "cloud storage",
                    "digital proof",
                    "smartphone export"
                ],
                "citation": "Section 57, Bharatiya Sakshya Adhiniyam, 2023",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "61": {
                "section_number": "61",
                "official_section_title": "Admissibility of electronic or digital record",
                "official_text": "Nothing in this Adhiniyam shall apply to deny the admissibility of an electronic or digital record in evidence on the ground that it is an electronic or digital record and such record shall have the same legal effect, validity and enforceability as other document.",
                "simplified_explanation": "Provides statutory guarantee that electronic or digital records cannot be rejected by courts merely because they are in electronic format, giving digital evidence identical legal force as paper documents.",
                "legal_ingredients": [
                    "Record generated or stored in electronic or digital format",
                    "Compliance with procedural conditions set out under Section 63"
                ],
                "domain": "cyber_fraud",
                "relevant_issues": [
                    "cyber_digital_evidence_admissibility",
                    "phishing",
                    "data_breach_victimization",
                    "ransomware_data_hijacking"
                ],
                "punishment_or_remedy": "Statutory admissibility of electronic records as legal evidence.",
                "related_provisions": [
                    "BSA 2023 Section 63",
                    "IT Act 2000 Section 4",
                    "IT Act 2000 Section 65"
                ],
                "exceptions_and_limitations": [
                    "Electronic records remain subject to proof of genuineness and integrity of computer source."
                ],
                "amendment_status": "In force; commenced on 1st July 2024 via Gazette Notification S.O. 2790(E).",
                "jurisdiction": "Central (Applies across all judicial and quasi-judicial proceedings in India).",
                "applicability_notes": "Replaces foundational common-law presumptions regarding physical papers, equating digital logs, SMS, and WhatsApp chats to physical letters.",
                "keywords": [
                    "admissibility of electronic record",
                    "digital validity",
                    "enforceability",
                    "electronic document",
                    "digital proof"
                ],
                "citation": "Section 61, Bharatiya Sakshya Adhiniyam, 2023",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "63": {
                "section_number": "63",
                "official_section_title": "Admissibility of electronic records and certificate requirement",
                "official_text": "(1) Notwithstanding anything contained in this Adhiniyam, any information contained in an electronic record which is printed on paper, stored, recorded or copied in optical or magnetic media or cloud or database... shall be deemed to be also a document... (4) In any proceedings where it is desired to give a statement in evidence by virtue of this section, a certificate doing any of the following things, that is to say,— (a) identifying the electronic record containing the statement and describing the manner in which it was produced; (b) giving such particulars of any device involved in the production of that electronic record as may be appropriate for the purpose of showing that the electronic record was produced by a computer... signed by a person in charge of the computer or device, or the management of the relevant activities... shall be evidence of any matter stated in the certificate.",
                "simplified_explanation": "Mandates that printouts, screenshots, or secondary copies of digital records must be accompanied by an electronic evidence certificate signed by the device custodian or owner to be admissible in court. Replaces former Section 65B of Indian Evidence Act.",
                "legal_ingredients": [
                    "Information contained in an electronic record produced by a computer or digital device",
                    "Device was operating properly during relevant period or malfunction did not affect accuracy",
                    "Statutory electronic certificate signed by person in lawful control or management of device"
                ],
                "domain": "cyber_fraud",
                "relevant_issues": [
                    "cyber_digital_evidence_admissibility",
                    "otp_fraud",
                    "identity_theft",
                    "digital_arrest_extortion",
                    "online_impersonation"
                ],
                "punishment_or_remedy": "Legal admissibility of secondary electronic evidence; without certificate, secondary digital evidence is inadmissible (Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal).",
                "related_provisions": [
                    "BSA 2023 Section 61",
                    "IT Act 2000 Section 65",
                    "BNSS 2023 Section 94"
                ],
                "exceptions_and_limitations": [
                    "Certificate is not required when the original physical electronic device (original mobile phone/laptop) is produced directly under Section 57."
                ],
                "amendment_status": "In force; commenced on 1st July 2024 via Gazette Notification S.O. 2790(E).",
                "jurisdiction": "Central (Applies across all courts in India).",
                "applicability_notes": "Critical statutory procedural requirement for admitting digital logs, transaction SMS, call records, and WhatsApp chats in cyber fraud prosecutions.",
                "keywords": [
                    "section 63 certificate",
                    "electronic certificate",
                    "secondary electronic evidence",
                    "section 65b replacement",
                    "call detail records",
                    "whatsapp chat proof"
                ],
                "citation": "Section 63, Bharatiya Sakshya Adhiniyam, 2023",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            }
        }
    },
    "payment_of_bonus_act_1965": {
        "official_act_name": "Payment of Bonus Act, 1965",
        "act_year": 1965,
        "short_name": "Payment of Bonus Act 1965",
        "official_source_name": "India Code",
        "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/1572/1/196521.pdf",
        "sections": {
            "8": {
                "section_number": "8",
                "official_section_title": "Eligibility for bonus",
                "official_text": "Every employee shall be entitled to be paid by his employer in an accounting year, bonus, in accordance with the provisions of this Act, provided he has worked in the establishment for not less than thirty working days in that year.",
                "simplified_explanation": "Every employee who has worked in an establishment for at least 30 working days in an accounting year has a statutory entitlement to receive annual bonus from the employer.",
                "legal_ingredients": [
                    "Employee employed on salary or wage up to statutory ceiling",
                    "Worked in establishment for not less than 30 working days in that accounting year",
                    "Establishment employs 20 or more persons (or factory under Factories Act)"
                ],
                "domain": "workplace_wage",
                "relevant_issues": [
                    "statutory_annual_bonus_non_payment_profitable_unit",
                    "statutory_annual_bonus_denial",
                    "final_settlement_withheld"
                ],
                "punishment_or_remedy": "Statutory right to bonus recovery with interest; recovery through Labour Commissioner under Section 21.",
                "related_provisions": [
                    "Payment of Bonus Act 1965 Section 10",
                    "Payment of Bonus Act 1965 Section 19",
                    "Code on Wages 2019 Section 26"
                ],
                "exceptions_and_limitations": [
                    "Employee must not be disqualified under Section 9 for fraud, theft, or violent misconduct."
                ],
                "amendment_status": "In force; wage ceiling amended by Act 6 of 2016.",
                "jurisdiction": "Central (Enforced by Central and State Labour Departments).",
                "applicability_notes": "Mandatory statutory right of workmen; cannot be contracted out via appointment letters or company policies.",
                "keywords": [
                    "eligibility for bonus",
                    "30 working days",
                    "statutory bonus",
                    "annual bonus",
                    "workplace wage"
                ],
                "citation": "Section 8, Payment of Bonus Act, 1965",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "9": {
                "section_number": "9",
                "official_section_title": "Disqualification for bonus",
                "official_text": "Notwithstanding anything contained in this Act, an employee shall be disqualified from receiving bonus under this Act, if he is dismissed from service for— (a) fraud; or (b) riotous or violent behaviour while on the premises of the establishment; or (c) theft, misappropriation or sabotage of any property of the establishment.",
                "simplified_explanation": "An employee loses right to bonus only if formally dismissed after domestic inquiry specifically for fraud, violence on premises, or theft/sabotage. Employer cannot forfeit bonus arbitrarily without formal dismissal on these statutory grounds.",
                "legal_ingredients": [
                    "Formal order of dismissal from service",
                    "Dismissal order expressly based on proved fraud, riotous/violent behaviour, or theft/sabotage"
                ],
                "domain": "workplace_wage",
                "relevant_issues": [
                    "statutory_annual_bonus_non_payment_profitable_unit",
                    "unlawful_termination_without_due_process",
                    "final_settlement_withheld"
                ],
                "punishment_or_remedy": "Forfeiture of bonus applies strictly to the accounting year of dismissal.",
                "related_provisions": [
                    "Payment of Bonus Act 1965 Section 8",
                    "Industrial Disputes Act 1947 Section 11A"
                ],
                "exceptions_and_limitations": [
                    "Resignation, ordinary termination, or performance issues do not disqualify an employee from receiving statutory bonus."
                ],
                "amendment_status": "In force.",
                "jurisdiction": "Central.",
                "applicability_notes": "Employers often falsely cite resignation to deny bonus; this section strictly limits forfeiture to proved dismissals for grave misconduct.",
                "keywords": [
                    "disqualification for bonus",
                    "forfeiture of bonus",
                    "dismissal for fraud",
                    "theft sabotage",
                    "violent conduct"
                ],
                "citation": "Section 9, Payment of Bonus Act, 1965",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "10": {
                "section_number": "10",
                "official_section_title": "Payment of minimum bonus",
                "official_text": "Subject to the other provisions of this Act, every employer shall be bound to pay to every employee in respect of the accounting year... a minimum bonus which shall be 8.33 per cent. of the salary or wage earned by the employee during the accounting year or one hundred rupees, whichever is higher, whether or not the employer has any allocable surplus in the accounting year.",
                "simplified_explanation": "Mandates that employers must pay a minimum statutory bonus of 8.33% of wages (or Rs 100), regardless of whether the establishment made a profit or suffered a loss in that accounting year.",
                "legal_ingredients": [
                    "Covered establishment",
                    "Eligible employee who worked 30+ days",
                    "Payment mandatory regardless of profit, loss, or allocable surplus"
                ],
                "domain": "workplace_wage",
                "relevant_issues": [
                    "statutory_annual_bonus_non_payment_profitable_unit",
                    "delayed_wages",
                    "unpaid_wages"
                ],
                "punishment_or_remedy": "Right to claim 8.33% minimum wage bonus plus interest; penal prosecution of employer under Section 28.",
                "related_provisions": [
                    "Payment of Bonus Act 1965 Section 8",
                    "Payment of Bonus Act 1965 Section 19",
                    "Code on Wages 2019 Section 26"
                ],
                "exceptions_and_limitations": [
                    "New establishments are exempt from paying minimum bonus during first 5 accounting years only if they have not derived any profit."
                ],
                "amendment_status": "In force; minimum percentage frozen at 8.33%.",
                "jurisdiction": "Central.",
                "applicability_notes": "Commonly violated when employers claim company suffered losses to deny annual Diwali or financial year-end bonus.",
                "keywords": [
                    "minimum bonus",
                    "8.33 percent",
                    "loss making company bonus",
                    "mandatory bonus",
                    "statutory entitlement"
                ],
                "citation": "Section 10, Payment of Bonus Act, 1965",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "19": {
                "section_number": "19",
                "official_section_title": "Time-limit for payment of bonus",
                "official_text": "All amounts payable to an employee by way of bonus under this Act shall be paid in cash by his employer— (a) where there is a dispute regarding payment of bonus... within a month from the date on which the award comes into operation; (b) in any other case, within a period of eight months from the close of the accounting year.",
                "simplified_explanation": "Requires employers to pay all bonus amounts in cash within 8 months from the close of the accounting year (by 30th November for March financial years).",
                "legal_ingredients": [
                    "Bonus payable under the Act",
                    "Payment must be made in cash/bank transfer within 8 months from financial year end"
                ],
                "domain": "workplace_wage",
                "relevant_issues": [
                    "statutory_annual_bonus_non_payment_profitable_unit",
                    "delayed_wages",
                    "final_settlement_withheld"
                ],
                "punishment_or_remedy": "Statutory recovery application before Labour Officer; penal action under Section 28.",
                "related_provisions": [
                    "Payment of Bonus Act 1965 Section 21",
                    "Payment of Bonus Act 1965 Section 28"
                ],
                "exceptions_and_limitations": [
                    "Appropriate Government may extend the 8-month period on application by employer, but total period cannot exceed 2 years."
                ],
                "amendment_status": "In force.",
                "jurisdiction": "Central.",
                "applicability_notes": "Enforces strict deadline on corporate bonus disbursement; employers cannot postpone bonus indefinitely.",
                "keywords": [
                    "time limit for bonus",
                    "eight months",
                    "bonus deadline",
                    "november 30 deadline",
                    "cash bonus"
                ],
                "citation": "Section 19, Payment of Bonus Act, 1965",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "28": {
                "section_number": "28",
                "official_section_title": "Penalty for contravention of Act or rules",
                "official_text": "If any person— (a) contravenes any of the provisions of this Act or any rule made thereunder; or (b) to whom a direction is given or a requisition is made under this Act fails to comply... he shall be punishable with imprisonment for a term which may extend to six months, or with fine which may extend to one thousand rupees, or with both.",
                "simplified_explanation": "Imposes criminal punishment of imprisonment up to 6 months, fine up to Rs 1,000, or both on employers who fail to pay statutory bonus or violate the rules.",
                "legal_ingredients": [
                    "Willful failure to pay bonus or comply with statutory directions",
                    "Complaint filed by or under authority of appropriate Government"
                ],
                "domain": "workplace_wage",
                "relevant_issues": [
                    "statutory_annual_bonus_non_payment_profitable_unit",
                    "delayed_wages"
                ],
                "punishment_or_remedy": "Imprisonment up to six months, or fine up to one thousand rupees, or both.",
                "related_provisions": [
                    "Payment of Bonus Act 1965 Section 10",
                    "Payment of Bonus Act 1965 Section 19"
                ],
                "exceptions_and_limitations": [
                    "Cognizance taken only on complaint by or with sanction of Labour Department."
                ],
                "amendment_status": "In force.",
                "jurisdiction": "Central.",
                "applicability_notes": "Criminal deterrence against employers withholding statutory employee bonuses.",
                "keywords": [
                    "bonus penalty",
                    "employer imprisonment",
                    "bonus prosecution",
                    "six months jail",
                    "labour inspector complaint"
                ],
                "citation": "Section 28, Payment of Bonus Act, 1965",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            }
        }
    },
    "registration_act_1908": {
        "official_act_name": "Registration Act, 1908",
        "act_year": 1908,
        "short_name": "Registration Act 1908",
        "official_source_name": "India Code",
        "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/2187/1/190816.pdf",
        "sections": {
            "17": {
                "section_number": "17",
                "official_section_title": "Documents of which registration is compulsory",
                "official_text": "(1) The following documents shall be registered... (a) instruments of gift of immovable property; (b) other non-testamentary instruments which purport or operate to create, declare, assign, limit or extinguish... any right, title or interest... of the value of one hundred rupees and upwards, to or in immovable property; (d) leases of immovable property from year to year, or for any term exceeding one year, or reserving a yearly rent.",
                "simplified_explanation": "Specifies documents that legally must be registered with the Sub-Registrar: property gifts, sales/transfers of immovable property worth Rs 100 or more, and tenancy leases exceeding 11 months (one year or more).",
                "legal_ingredients": [
                    "Document purporting to create, declare, assign, limit or extinguish right/title/interest in immovable property",
                    "Value of property rights Rs 100 or upwards, or lease term exceeding one year"
                ],
                "domain": "contractual_disputes",
                "relevant_issues": [
                    "unregistered_lease_immovable_property_dispute",
                    "commercial_lease_security_deposit_withholding",
                    "breach_of_contract"
                ],
                "punishment_or_remedy": "Mandatory requirement of law; failure invokes evidentiary bar under Section 49.",
                "related_provisions": [
                    "Registration Act 1908 Section 49",
                    "Transfer of Property Act 1882 Section 107",
                    "Transfer of Property Act 1882 Section 54"
                ],
                "exceptions_and_limitations": [
                    "Residential rental agreements for 11 months or less are not compulsorily registrable under Central Section 17(1)(d), though state stamp laws apply."
                ],
                "amendment_status": "In force; state amendments in Maharashtra, Karnataka, Tamil Nadu require registration of leave and license.",
                "jurisdiction": "Central & State (State amendments apply).",
                "applicability_notes": "Foundation of all immovable property and tenancy disputes in India; unregistered long-term leases create severe legal infirmities.",
                "keywords": [
                    "compulsory registration",
                    "section 17 registration",
                    "lease registration",
                    "immovable property",
                    "sub registrar",
                    "11 month lease"
                ],
                "citation": "Section 17, Registration Act, 1908",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "49": {
                "section_number": "49",
                "official_section_title": "Effect of non-registration of documents required to be registered",
                "official_text": "No document required by section 17 or by any provision of the Transfer of Property Act, 1882, to be registered shall— (a) affect any immovable property comprised therein, or (b) confer any power to adopt, or (c) be received as evidence of any transaction affecting such property... Provided that an unregistered document affecting immovable property and required by this Act or the Transfer of Property Act, 1882, to be registered may be received as evidence of a contract in a suit for specific performance under Chapter II of the Specific Relief Act, 1877, or as evidence of any collateral transaction not required to be effected by registered instrument.",
                "simplified_explanation": "An unregistered document that required compulsory registration cannot transfer title or be received as evidence of property transfer in court, but may be admitted to prove a contract in a specific performance suit or for collateral purposes.",
                "legal_ingredients": [
                    "Document required by Section 17 to be registered",
                    "Failure to register with Sub-Registrar",
                    "Inadmissibility to affect property or prove transfer"
                ],
                "domain": "contractual_disputes",
                "relevant_issues": [
                    "unregistered_lease_immovable_property_dispute",
                    "part_performance_possession_protection",
                    "specific_performance_readiness_willingness_dispute"
                ],
                "punishment_or_remedy": "Inadmissibility in evidence; limited exception for specific performance suits or collateral facts.",
                "related_provisions": [
                    "Registration Act 1908 Section 17",
                    "Transfer of Property Act 1882 Section 53A",
                    "Specific Relief Act 1963 Section 10"
                ],
                "exceptions_and_limitations": [
                    "Unregistered agreement to sell can be received as evidence of contract in suit for specific performance under proviso to S. 49."
                ],
                "amendment_status": "In force.",
                "jurisdiction": "Central.",
                "applicability_notes": "Crucial statutory barrier in property litigation; protects buyers under specific performance while penalizing unregistered transfers.",
                "keywords": [
                    "effect of non registration",
                    "inadmissible evidence",
                    "collateral purpose",
                    "proviso section 49",
                    "unregistered agreement to sell"
                ],
                "citation": "Section 49, Registration Act, 1908",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            }
        }
    },
    "competition_act_2002": {
        "official_act_name": "Competition Act, 2002",
        "act_year": 2002,
        "short_name": "Competition Act 2002",
        "official_source_name": "India Code",
        "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/2010/1/200312.pdf",
        "sections": {
            "3": {
                "section_number": "3",
                "official_section_title": "Anti-competitive agreements",
                "official_text": "(1) No enterprise or association of enterprises or person or association of persons shall enter into any agreement in respect of production, supply, distribution, storage, acquisition or control of goods or provision of services, which causes or is likely to cause an appreciable adverse effect on competition within India. (2) Any agreement entered into in contravention of the provisions contained in sub-section (1) shall be void. (3) Any agreement entered into between enterprises... including cartels, engaged in identical or similar trade of goods or provision of services, which— (a) directly or indirectly determines purchase or sale prices; (b) limits or controls production, supply, markets; (c) shares the market... shall be presumed to have an appreciable adverse effect on competition.",
                "simplified_explanation": "Declares agreements between businesses that harm fair competition—such as price fixing cartels, bid rigging, artificial market allocation, and forced tie-in sales (e.g. schools forcing books/uniforms from single vendor)—illegal and void.",
                "legal_ingredients": [
                    "Agreement between enterprises or persons",
                    "Appreciable adverse effect on competition (AAEC) in India",
                    "Price fixing, market allocation, bid rigging, or tie-in arrangement"
                ],
                "domain": "consumer_issues",
                "relevant_issues": [
                    "anti_competitive_cartel_price_fixing",
                    "school_mandatory_uniform_book_tie_in",
                    "unfair_trade_practice"
                ],
                "punishment_or_remedy": "Agreement void ab initio; penalty up to 10% of average turnover or 3 times profit for cartel members under Section 27.",
                "related_provisions": [
                    "Competition Act 2002 Section 4",
                    "Competition Act 2002 Section 19",
                    "CPA 2019 Section 2(47)"
                ],
                "exceptions_and_limitations": [
                    "Reasonable conditions necessary for protecting intellectual property rights (patents, trademarks, copyrights) are exempt under S. 3(5)."
                ],
                "amendment_status": "In force; amended by Competition (Amendment) Act, 2023.",
                "jurisdiction": "Central (Applies across all commercial enterprises in India).",
                "applicability_notes": "Directly empowers consumers to challenge collusive price hikes, airline ticket cartels, and school vendor tie-in exploitation.",
                "keywords": [
                    "anti competitive agreement",
                    "cartel",
                    "price fixing",
                    "bid rigging",
                    "tie in sales",
                    "market allocation",
                    "void agreement"
                ],
                "citation": "Section 3, Competition Act, 2002",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "4": {
                "section_number": "4",
                "official_section_title": "Abuse of dominant position",
                "official_text": "(1) No enterprise or group shall abuse its dominant position. (2) There shall be an abuse of dominant position under sub-section (1), if an enterprise or a group.— (a) directly or indirectly, imposes unfair or discriminatory— (i) condition in purchase or sale of goods or service; or (ii) price in purchase or sale (including predatory price) of goods or service... (b) limits or restricts— (i) production of goods or provision of services; (c) indulges in practice or practices resulting in denial of market access in any manner.",
                "simplified_explanation": "Prohibits powerful market leaders and dominant digital platforms from exploiting consumers through unfair prices, predatory pricing below cost to wipe out competition, or blocking market access.",
                "legal_ingredients": [
                    "Dominant position held by enterprise in relevant geographic and product market",
                    "Abusive conduct: unfair conditions, predatory pricing, denial of market access, or leveraging dominance"
                ],
                "domain": "consumer_issues",
                "relevant_issues": [
                    "anti_competitive_cartel_price_fixing",
                    "dark_patterns_drip_pricing_sneaked_charges",
                    "unfair_contract_terms_consumer"
                ],
                "punishment_or_remedy": "Cease and desist order, division of dominant enterprise, penalty up to 10% of average turnover under Section 27.",
                "related_provisions": [
                    "Competition Act 2002 Section 3",
                    "Competition Act 2002 Section 19",
                    "CPA 2019 Section 2(46)"
                ],
                "exceptions_and_limitations": [
                    "Mere possession of dominant market share is not illegal; the statutory violation requires proof of abusive conduct."
                ],
                "amendment_status": "In force; global turnover penalty standard introduced by Act 9 of 2023.",
                "jurisdiction": "Central.",
                "applicability_notes": "Primary weapon against Big Tech and monopolistic entities imposing unfair terms on Indian consumers.",
                "keywords": [
                    "abuse of dominant position",
                    "predatory pricing",
                    "unfair condition",
                    "denial of market access",
                    "dominant enterprise",
                    "competition commission"
                ],
                "citation": "Section 4, Competition Act, 2002",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "19": {
                "section_number": "19",
                "official_section_title": "Inquiry into certain agreements and dominant position",
                "official_text": "(1) The Commission may inquire into any alleged contravention of the provisions contained in sub-section (1) of section 3 or sub-section (1) of section 4 either on its own motion or on— (a) receipt of any information, in such manner and accompanied by such fee as may be determined by regulations, from any person, consumer or their association or trade association; or (b) a reference made to it by the Central Government or a State Government or a statutory authority.",
                "simplified_explanation": "Empowers any individual consumer, citizen, trade association, or government body to file an information complaint before the Competition Commission of India (CCI) to investigate cartels or anti-competitive practices.",
                "legal_ingredients": [
                    "Information petition submitted by consumer, person, or association",
                    "Prima facie contravention of Section 3 (anti-competitive agreement) or Section 4 (abuse of dominance)"
                ],
                "domain": "consumer_issues",
                "relevant_issues": [
                    "anti_competitive_cartel_price_fixing",
                    "school_mandatory_uniform_book_tie_in"
                ],
                "punishment_or_remedy": "Director General (DG) investigation; interim relief under Section 33; final penalty and restitution orders under Section 27.",
                "related_provisions": [
                    "Competition Act 2002 Section 26",
                    "Competition Act 2002 Section 27",
                    "Competition Act 2002 Section 33"
                ],
                "exceptions_and_limitations": [
                    "CCI will close information at Section 26(2) stage if no prima facie competition concern is disclosed."
                ],
                "amendment_status": "In force.",
                "jurisdiction": "Central (CCI Delhi has nationwide jurisdiction).",
                "applicability_notes": "Key procedural gateway enabling citizens to trigger antitrust investigations against corporate cartels.",
                "keywords": [
                    "cci complaint",
                    "information under section 19",
                    "competition inquiry",
                    "director general investigation",
                    "consumer antitrust filing"
                ],
                "citation": "Section 19, Competition Act, 2002",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            }
        }
    },
    "industrial_employment_standing_orders_act_1946": {
        "official_act_name": "Industrial Employment (Standing Orders) Act, 1946",
        "act_year": 1946,
        "short_name": "Standing Orders Act 1946",
        "official_source_name": "India Code",
        "official_source_url": "https://www.indiacode.nic.in/bitstream/123456789/1987/1/194620.pdf",
        "sections": {
            "3": {
                "section_number": "3",
                "official_section_title": "Submission of draft standing orders",
                "official_text": "(1) Within six months from the date on which this Act becomes applicable to an industrial establishment, the employer shall submit to the Certifying Officer five copies of the draft standing orders proposed by him for adoption in his industrial establishment. (2) Provision shall be made in such draft for every matter set out in the Schedule which may be applicable to the industrial establishment.",
                "simplified_explanation": "Mandates employers in industrial establishments with 100 or more workmen to draft and formally certify standing orders defining transparent rules for employment classification, shift work, attendance, and misconduct inquiries.",
                "legal_ingredients": [
                    "Industrial establishment with 100+ workmen (or state lower threshold)",
                    "Submission of draft standing orders covering all Schedule matters within 6 months"
                ],
                "domain": "workplace_wage",
                "relevant_issues": [
                    "unilateral_change_in_service_conditions_without_notice",
                    "unlawful_termination_without_due_process"
                ],
                "punishment_or_remedy": "Certifying Officer certification; fine up to Rs 5,000 for employer failure to submit draft under Section 13.",
                "related_provisions": [
                    "Standing Orders Act 1946 Section 10A",
                    "Industrial Disputes Act 1947 Section 9A"
                ],
                "exceptions_and_limitations": [
                    "Establishments with less than the statutory threshold (unless notified by State) are governed by model standing orders."
                ],
                "amendment_status": "In force.",
                "jurisdiction": "Central & State.",
                "applicability_notes": "Statutory safeguard against arbitrary management rules; standing orders have statutory force of contract.",
                "keywords": [
                    "draft standing orders",
                    "certification of standing orders",
                    "terms of employment",
                    "workplace rules",
                    "misconduct inquiry"
                ],
                "citation": "Section 3, Industrial Employment (Standing Orders) Act, 1946",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            },
            "10A": {
                "section_number": "10A",
                "official_section_title": "Payment of subsistence allowance",
                "official_text": "(1) Where any workman is suspended by the employer pending investigation or inquiry into complaints or charges of misconduct against him, the employer shall pay to such workman a subsistence allowance— (a) at the rate of fifty per centum of the wages which the workman was entitled to immediately preceding the date of such suspension, for the first ninety days of suspension; and (b) at the rate of seventy-five per centum of such wages for the remaining period of suspension if the delay in the completion of disciplinary proceedings against such workman is not directly attributable to the conduct of such workman.",
                "simplified_explanation": "Establishes a mandatory statutory right that any employee suspended pending domestic inquiry must be paid subsistence allowance: 50% salary for first 90 days, and 75% thereafter if delay is not caused by the employee.",
                "legal_ingredients": [
                    "Workman suspended by employer pending inquiry into misconduct",
                    "Statutory entitlement to 50% wages for first 90 days of suspension",
                    "Rate increases to 75% wages after 90 days if delay is not employee fault"
                ],
                "domain": "workplace_wage",
                "relevant_issues": [
                    "statutory_subsistence_allowance_suspension",
                    "unlawful_termination_without_due_process",
                    "delayed_wages"
                ],
                "punishment_or_remedy": "Recovery of unpaid subsistence allowance with interest; inquiry proceedings vitiated and termination void if subsistence allowance is withheld (Supreme Court in State of Maharashtra v. Chandrabhan).",
                "related_provisions": [
                    "Industrial Disputes Act 1947 Section 33C",
                    "Payment of Wages Act 1936 Section 15"
                ],
                "exceptions_and_limitations": [
                    "Subsistence allowance is not reduced if the employee obtains an adjournment with valid medical reason."
                ],
                "amendment_status": "In force; inserted by Act 18 of 1982.",
                "jurisdiction": "Central & State.",
                "applicability_notes": "High-impact protection against employer starvation tactics during prolonged suspension and disciplinary inquiries.",
                "keywords": [
                    "subsistence allowance",
                    "suspended employee salary",
                    "50 percent salary",
                    "75 percent salary",
                    "suspension pending inquiry",
                    "disciplinary proceedings"
                ],
                "citation": "Section 10A, Industrial Employment (Standing Orders) Act, 1946",
                "provision_status": "in_force",
                "verification": {
                    "status": "pending_manual_verification"
                }
            }
        }
    }
}

