"""New statutory sections to be added to existing Acts in LegalLens.
Every section has all 15 required legal attributes from India Code statutory text.
"""

EXISTING_ACTS_EXPANSIONS = {
    "it_act_2000": {
        "46": {
            "section_number": "46",
            "official_section_title": "Power to adjudicate",
            "official_text": "(1) For the purpose of adjudging under this Chapter, whether any person has committed a contravention of any of the provisions of this Act or of any rule, regulation, direction or order made thereunder... the Central Government shall appoint any officer not below the rank of a Director to the Government of India or an equivalent officer of a State Government to be an adjudicating officer for holding an inquiry in the manner prescribed by the Central Government... (1A) The adjudicating officer appointed under sub-section (1) shall exercise jurisdiction to adjudicate matters in which the claim for injury or damage does not exceed five crore rupees.",
            "simplified_explanation": "Empowers citizens to file a statutory compensation petition before the State IT Secretary (acting as Adjudicating Officer) to recover financial compensation up to Rs 5 Crore for cyber hacking, unauthorised data access, or bank fraud under Chapter IX of the IT Act.",
            "legal_ingredients": [
                "Contravention of Chapter IX (Section 43 unauthorised access, 43A data privacy breach)",
                "Claim for damage or injury up to Rs 5 Crore",
                "Petition filed before designated Adjudicating Officer of State Government"
            ],
            "domain": "cyber_fraud",
            "relevant_issues": [
                "cyber_adjudicating_officer_compensation",
                "unauthorized_account_access",
                "data_breach_victimization"
            ],
            "punishment_or_remedy": "Adjudicating Officer can award monetary compensation up to Rs 5 Crore against the wrongdoer or negligent bank/institution.",
            "related_provisions": [
                "IT Act 2000 Section 43",
                "IT Act 2000 Section 43A",
                "IT Act 2000 Section 48"
            ],
            "exceptions_and_limitations": [
                "Claims exceeding Rs 5 Crore must be filed before the competent Civil Court."
            ],
            "amendment_status": "In force; jurisdiction limit of Rs 5 Crore inserted by Act 10 of 2009.",
            "jurisdiction": "State-level Adjudicating Officer (Information Technology Department of relevant State/UT).",
            "applicability_notes": "A powerful, underutilized quasi-judicial forum for cyber victims to recover lost money without the delays of regular civil courts.",
            "keywords": [
                "adjudicating officer",
                "compensation up to 5 crore",
                "it secretary adjudication",
                "cyber fraud compensation",
                "section 46 inquiry"
            ],
            "citation": "Section 46, Information Technology Act, 2000",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "48": {
            "section_number": "48",
            "official_section_title": "Establishment of Cyber Appellate Tribunal / Appellate Tribunal",
            "official_text": "(1) The Telecom Disputes Settlement and Appellate Tribunal established under section 14 of the Telecom Regulatory Authority of India Act, 1997, shall, on and from the commencement of Part XIV of Chapter VI of the Finance Act, 2017, be the Appellate Tribunal for the purposes of this Act and the said Appellate Tribunal shall exercise the jurisdiction, powers and authority conferred on it by or under this Act.",
            "simplified_explanation": "Establishes that appeals against orders passed by the State Adjudicating Officer under Section 46 lie before the Telecom Disputes Settlement and Appellate Tribunal (TDSAT) in New Delhi.",
            "legal_ingredients": [
                "Aggrieved by an order of the Adjudicating Officer under Section 46",
                "Appeal filed before TDSAT within 45 days from date of receipt of order"
            ],
            "domain": "cyber_fraud",
            "relevant_issues": [
                "cyber_adjudicating_officer_compensation"
            ],
            "punishment_or_remedy": "Statutory appellate remedy to confirm, set aside, or modify compensation awards.",
            "related_provisions": [
                "IT Act 2000 Section 46",
                "TRAI Act 1997 Section 14"
            ],
            "exceptions_and_limitations": [
                "Limitation period of 45 days to file appeal; delay can be condoned on sufficient cause."
            ],
            "amendment_status": "In force; powers merged with TDSAT via Finance Act, 2017.",
            "jurisdiction": "Central (TDSAT New Delhi).",
            "applicability_notes": "Statutory appellate avenue for cyber fraud victims or corporate entities appealing IT Adjudicating Officer verdicts.",
            "keywords": [
                "cyber appellate tribunal",
                "tdsat appeal",
                "it act appeal",
                "45 days limitation",
                "adjudicating officer appeal"
            ],
            "citation": "Section 48, Information Technology Act, 2000",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "70": {
            "section_number": "70",
            "official_section_title": "Protected system",
            "official_text": "(1) The appropriate Government may, by notification in the Official Gazette, declare any computer resource which directly or indirectly affects the facility of Critical Information Infrastructure, to be a protected system... (3) Any person who secures access or attempts to secure access to a protected system in contravention of the provisions of this section shall be punished with imprisonment of either description for a term which may extend to ten years and shall also be liable to fine.",
            "simplified_explanation": "Imposes severe criminal penalties—imprisonment up to 10 years and fine—for unauthorized access or hacking attempts targeting critical information infrastructure (such as banking networks, power grids, defense, or telecom infrastructure).",
            "legal_ingredients": [
                "Computer system declared as 'protected system' by Government notification",
                "Securing access or attempting to secure access without authorization"
            ],
            "domain": "cyber_fraud",
            "relevant_issues": [
                "cyber_ransomware_data_kidnapping",
                "ransomware_data_hijacking"
            ],
            "punishment_or_remedy": "Imprisonment of either description up to ten years and fine.",
            "related_provisions": [
                "IT Act 2000 Section 66F",
                "IT Act 2000 Section 70B",
                "BNS 2023 Section 318"
            ],
            "exceptions_and_limitations": [
                "Authorized personnel acting in the performance of official statutory duties are exempt."
            ],
            "amendment_status": "In force; amended by Act 10 of 2009.",
            "jurisdiction": "Central.",
            "applicability_notes": "Applies to high-level cyber sabotage, ransomware attacks on government/banking servers, and critical infrastructure attacks.",
            "keywords": [
                "protected system",
                "critical information infrastructure",
                "ten years imprisonment",
                "national cyber security",
                "ransomware attack"
            ],
            "citation": "Section 70, Information Technology Act, 2000",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "70B": {
            "section_number": "70B",
            "official_section_title": "Indian Computer Emergency Response Team to serve as national agency for incident response",
            "official_text": "(1) The Central Government shall, by notification in the Official Gazette, appoint an agency of the Government to be called the Indian Computer Emergency Response Team... (4) The agency referred to in sub-section (1) shall perform the following functions... (a) collection, analysis and dissemination of information on cyber incidents; (b) forecast and alerts of cyber security incidents; (c) emergency measures for handling cyber security incidents; (d) coordination of cyber incidents response activities... (6) Any service provider, intermediaries, data centres, body corporate and any other person who fails to provide the information called for or comply with the direction... shall be punishable with imprisonment for a term which may extend to one year or with fine which may extend to one lakh rupees or with both.",
            "simplified_explanation": "Establishes CERT-In as the national nodal agency for cyber incident response, requiring corporations, VPN providers, and intermediaries to report cyber incidents within 6 hours and cooperate with investigations.",
            "legal_ingredients": [
                "Occurrence of cybersecurity incident, data breach, or ransomware event",
                "Statutory obligation to report incident and comply with CERT-In directions"
            ],
            "domain": "cyber_fraud",
            "relevant_issues": [
                "cyber_ransomware_data_kidnapping",
                "data_breach_victimization",
                "ransomware_data_hijacking"
            ],
            "punishment_or_remedy": "Imprisonment up to one year, or fine up to one lakh rupees, or both for non-compliance with directions under Section 70B(6).",
            "related_provisions": [
                "IT Act 2000 Section 43A",
                "IT Act 2000 Section 70",
                "DPDP Act 2023 Section 8"
            ],
            "exceptions_and_limitations": [
                "Reporting directions apply to service providers, intermediaries, data centres, and bodies corporate."
            ],
            "amendment_status": "In force; inserted by Act 10 of 2009, reinforced by CERT-In Directions 2022.",
            "jurisdiction": "Central (CERT-In New Delhi).",
            "applicability_notes": "Statutory foundation for mandatory corporate incident reporting and forensic cyber investigation in India.",
            "keywords": [
                "cert in",
                "cyber incident reporting",
                "6 hour breach notification",
                "ransomware reporting",
                "section 70b"
            ],
            "citation": "Section 70B, Information Technology Act, 2000",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "cpa_2019": {
        "38": {
            "section_number": "38",
            "official_section_title": "Procedure on admission of complaint",
            "official_text": "(1) The District Commission shall, on admission of a complaint... refer a copy of the admitted complaint within twenty-one days from the date of its admission to the opposite party mentioning therein or directing him to give his version of the case within a period of thirty days or such extended period not exceeding fifteen days... (2) Where the complaint alleges a defect in goods which cannot be determined without proper analysis or test... the District Commission shall obtain a sample of the goods... and refer it to the appropriate laboratory... (9) The District Commission shall have the same powers as are vested in a civil court under the Code of Civil Procedure, 1908.",
            "simplified_explanation": "Outlines the statutory trial procedure in the Consumer Forum: notice issued within 21 days, opposite party must respond within 30 days, lab testing for defective goods, and ex-parte orders if the seller fails to appear.",
            "legal_ingredients": [
                "Admitted consumer complaint",
                "Statutory 21-day notice to opposite party",
                "30-day response window (extendable by 15 days max)",
                "Referral to government testing laboratory for defective goods"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "defective_product",
                "automobile_manufacturing_defect_lemon_vehicle",
                "food_delivery_adulterated_contaminated_meal"
            ],
            "punishment_or_remedy": "Ex-parte adjudication against defaulting company; statutory laboratory test report binding.",
            "related_provisions": [
                "CPA 2019 Section 35",
                "CPA 2019 Section 39",
                "CPA 2019 Section 83"
            ],
            "exceptions_and_limitations": [
                "Opposite party cannot exceed 45 days total to file written version (Constitution Bench in New India Assurance v. Hilli Multipurpose Cold Storage).",
            ],
            "amendment_status": "In force.",
            "jurisdiction": "District Consumer Disputes Redressal Commission.",
            "applicability_notes": "Core procedural protection ensuring speedy justice for consumers without technical civil court formalities.",
            "keywords": [
                "procedure on admission",
                "30 day written version",
                "laboratory sample test",
                "ex parte consumer order",
                "civil court powers"
            ],
            "citation": "Section 38, Consumer Protection Act, 2019",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "40": {
            "section_number": "40",
            "official_section_title": "Review by District Commission in certain cases",
            "official_text": "The District Commission shall have the power to review any of the order passed by it if there is an error apparent on the face of the record, either of its own motion or on an application made by any of the parties within thirty days of such order.",
            "simplified_explanation": "Grants the District Consumer Commission statutory power to review and correct its own orders within 30 days if there is an obvious mistake or error apparent on the record.",
            "legal_ingredients": [
                "Order passed by District Commission",
                "Error apparent on the face of the record",
                "Application filed within 30 days from date of order"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "service_deficiency",
                "refund_denial"
            ],
            "punishment_or_remedy": "Rectification and modification of erroneous consumer forum orders without needing an expensive appeal.",
            "related_provisions": [
                "CPA 2019 Section 41",
                "CPA 2019 Section 38"
            ],
            "exceptions_and_limitations": [
                "Review cannot re-hear the entire merits of the case; it is strictly limited to patent errors apparent on the face of record."
            ],
            "amendment_status": "In force; novel power introduced in CPA 2019 (not available under 1986 Act).",
            "jurisdiction": "District Consumer Commission.",
            "applicability_notes": "Provides swift local correction of typographical, calculation, or clear factual oversights in consumer orders.",
            "keywords": [
                "review power",
                "error apparent on record",
                "30 days review application",
                "district commission review",
                "rectification"
            ],
            "citation": "Section 40, Consumer Protection Act, 2019",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "41": {
            "section_number": "41",
            "official_section_title": "Appeal against order of District Commission",
            "official_text": "Any person aggrieved by an order made by the District Commission may prefer an appeal against such order to the State Commission on the grounds of facts or law within a period of forty-five days from the date of the order... Provided that no appeal by a person, who is required to pay any amount in terms of an order of the District Commission, shall be entertained by the State Commission unless the appellant has deposited fifty per cent. of that amount in the manner prescribed.",
            "simplified_explanation": "Provides a statutory right of appeal to the State Consumer Commission within 45 days. Crucially, a corporate appellant must pre-deposit 50% of the awarded amount before their appeal can even be heard, protecting the consumer.",
            "legal_ingredients": [
                "Aggrieved by order of District Commission",
                "Appeal filed within 45 days to State Commission",
                "Mandatory pre-deposit of 50% of ordered compensation amount by appealing company"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "service_deficiency",
                "automobile_manufacturing_defect_lemon_vehicle",
                "insurance_claim_rejection_dispute"
            ],
            "punishment_or_remedy": "Appellate scrutiny by State Commission; 50% deposit secures consumer compensation against corporate delay tactics.",
            "related_provisions": [
                "CPA 2019 Section 38",
                "CPA 2019 Section 71"
            ],
            "exceptions_and_limitations": [
                "State Commission may entertain an appeal after 45 days if satisfied there was sufficient cause for delay."
            ],
            "amendment_status": "In force; 50% mandatory pre-deposit standard introduced under 2019 Act.",
            "jurisdiction": "State Consumer Disputes Redressal Commission.",
            "applicability_notes": "Prevents large corporations from filing frivolous appeals to drag out consumer compensation payouts.",
            "keywords": [
                "appeal to state commission",
                "45 days limitation",
                "50 percent pre deposit",
                "stay on consumer order",
                "consumer appeal"
            ],
            "citation": "Section 41, Consumer Protection Act, 2019",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "71": {
            "section_number": "71",
            "official_section_title": "Enforcement of orders of District Commission, State Commission or National Commission",
            "official_text": "Every order made by a District Commission, State Commission or the National Commission shall be enforced by it in the same manner as if it were a decree of a civil court made by a court in a suit being executed under the provisions of the Code of Civil Procedure, 1908.",
            "simplified_explanation": "Grants Consumer Commissions full execution powers identical to a Civil Court, allowing attachment of bank accounts, seizure of corporate property, and recovery warrants if a company disobeys an order.",
            "legal_ingredients": [
                "Final or interim order passed by Consumer Commission",
                "Failure of opposite party to comply with order within stipulated period",
                "Execution petition filed under Order XXI CPC"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "service_deficiency",
                "defective_product",
                "refund_denial"
            ],
            "punishment_or_remedy": "Attachment of company bank accounts, property distress warrants, civil recovery decree.",
            "related_provisions": [
                "CPA 2019 Section 72",
                "CPA 2019 Section 39"
            ],
            "exceptions_and_limitations": [
                "Execution proceedings can be stayed only by a formal stay order from a higher appellate commission."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "District, State, or National Consumer Commission.",
            "applicability_notes": "Ensures that consumer awards are not mere paper orders, but enforceable decrees backed by bank attachment powers.",
            "keywords": [
                "enforcement of order",
                "execution petition",
                "bank attachment",
                "decree of civil court",
                "recovery of consumer award"
            ],
            "citation": "Section 71, Consumer Protection Act, 2019",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "72": {
            "section_number": "72",
            "official_section_title": "Penalty for non-compliance of order",
            "official_text": "(1) Whoever fails to comply with any order made by the District Commission or the State Commission or the National Commission, as the case may be, shall be punishable with imprisonment for a term which shall not be less than one month, but which may extend to three years, or with fine, which shall not be less than twenty-five thousand rupees, but which may extend to one lakh rupees, or with both... (2) The District Commission, the State Commission or the National Commission, as the case may be, shall have the power of a Judicial Magistrate of the first class for the trial of offences under sub-section (1).",
            "simplified_explanation": "Imposes criminal penalties on company directors and sellers who fail to comply with consumer court orders: mandatory imprisonment from 1 month up to 3 years, fine from Rs 25,000 to Rs 1,00,000, or both, with commissions acting as Judicial Magistrates.",
            "legal_ingredients": [
                "Lawful order passed by Consumer Commission",
                "Willful non-compliance by trader, manufacturer, or corporate director",
                "Application under Section 72 filed by aggrieved consumer"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "service_deficiency",
                "refund_denial",
                "automobile_manufacturing_defect_lemon_vehicle"
            ],
            "punishment_or_remedy": "Non-bailable arrest warrants against company directors; imprisonment from 1 month up to 3 years, and fine up to Rs 1 Lakh.",
            "related_provisions": [
                "CPA 2019 Section 71",
                "BNSS 2023 Section 173"
            ],
            "exceptions_and_limitations": [
                "Summary trial procedure under BNSS/CrPC applies."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "District, State, or National Consumer Commission exercising First Class Judicial Magistrate powers.",
            "applicability_notes": "The strongest coercive statutory tool to force corporate compliance with refund and compensation orders.",
            "keywords": [
                "penalty for non compliance",
                "imprisonment up to 3 years",
                "judicial magistrate powers",
                "arrest warrant corporate director",
                "fine up to 1 lakh"
            ],
            "citation": "Section 72, Consumer Protection Act, 2019",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "82": {
            "section_number": "82",
            "official_section_title": "Application of Chapter VI (Product Liability)",
            "official_text": "This Chapter shall apply to every action for product liability for harm caused by or resulting from any product manufactured by a product manufacturer or serviced by a product service provider or sold by a product seller.",
            "simplified_explanation": "Introduces statutory Product Liability across India, holding manufacturers, service providers, and sellers legally liable for any harm, physical injury, mental agony, or property damage caused by defective products.",
            "legal_ingredients": [
                "Harm, personal injury, illness, or property damage caused to consumer",
                "Harm caused by defective product or deficient service",
                "Applicable to product manufacturer, service provider, and seller"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "product_liability_defective_good_injury",
                "defective_product",
                "ev_battery_thermal_range_defect"
            ],
            "punishment_or_remedy": "Statutory compensation for harm, medical expenses, property loss, and damages.",
            "related_provisions": [
                "CPA 2019 Section 83",
                "CPA 2019 Section 84",
                "CPA 2019 Section 85",
                "CPA 2019 Section 86"
            ],
            "exceptions_and_limitations": [
                "Harm does not include commercial damage to product itself unless covered under warranty; governed by Section 87 exceptions."
            ],
            "amendment_status": "In force; landmark regime introduced under CPA 2019.",
            "jurisdiction": "Central (Consumer Commissions across India).",
            "applicability_notes": "Landmark statutory reform replacing caveat emptor with strict product liability for manufacturers and distributors in India.",
            "keywords": [
                "product liability",
                "chapter vi cpa",
                "harm caused by product",
                "manufacturer liability",
                "strict liability consumer"
            ],
            "citation": "Section 82, Consumer Protection Act, 2019",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "83": {
            "section_number": "83",
            "official_section_title": "Product liability action",
            "official_text": "A product liability action may be brought by a complainant before a District Commission or State Commission or National Commission, as the case may be, for harm caused to him on account of a defective product made by a manufacturer or serviced by a service provider or sold by a product seller.",
            "simplified_explanation": "Empowers an injured consumer or their legal heirs to file a formal product liability suit before the Consumer Commission claiming compensation for injuries or loss caused by a defective product.",
            "legal_ingredients": [
                "Complainant suffered harm or injury",
                "Direct causal nexus between harm and product defect or service deficiency",
                "Action brought before competent Consumer Commission"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "product_liability_defective_good_injury",
                "defective_product",
                "automobile_manufacturing_defect_lemon_vehicle"
            ],
            "punishment_or_remedy": "Full compensation for injury, medical costs, disability, and replacement/refund of defective product.",
            "related_provisions": [
                "CPA 2019 Section 82",
                "CPA 2019 Section 84",
                "CPA 2019 Section 87"
            ],
            "exceptions_and_limitations": [
                "Subject to proof of defect and exclusion defenses under Section 87."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Consumer Commissions.",
            "applicability_notes": "Foundation section for all personal injury and property damage compensation claims arising from defective goods.",
            "keywords": [
                "product liability action",
                "claim for harm",
                "defective product compensation",
                "injury compensation",
                "strict liability claim"
            ],
            "citation": "Section 83, Consumer Protection Act, 2019",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "87": {
            "section_number": "87",
            "official_section_title": "Exceptions to product liability action",
            "official_text": "(1) A product liability action shall not lie against the product seller, if at the time of harm, the product was misused, altered, or modified... (2) In any product liability action, a product manufacturer shall not be liable, where— (a) the product was purchased by an employer for use at the workplace and the product manufacturer had provided warnings or instructions to such employer; (b) the product was sold as a component or material to be used in another product; (c) the product was one which was legally meant to be used only by or under the supervision of an expert.",
            "simplified_explanation": "Sets out statutory defenses where manufacturer or seller is not liable: product was unauthorizedly modified, misused against clear warnings, or used without mandatory expert supervision.",
            "legal_ingredients": [
                "Evidence of unauthorized modification or misuse by consumer",
                "Failure to observe clear statutory warnings",
                "Employer workplace use defense"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "product_liability_defective_good_injury",
                "warranty_guarantee_denial"
            ],
            "punishment_or_remedy": "Statutory dismissal of product liability claim if exclusion grounds are established.",
            "related_provisions": [
                "CPA 2019 Section 82",
                "CPA 2019 Section 83"
            ],
            "exceptions_and_limitations": [
                "Defense fails if manufacturer failed to provide adequate warning or instruction manual in simple language."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Consumer Commissions.",
            "applicability_notes": "Critical for legal balance; prevents frivolous claims where consumers self-modified or dangerously misused products.",
            "keywords": [
                "exceptions to product liability",
                "product misuse defense",
                "alteration modification",
                "warning instruction defense",
                "statutory exclusions"
            ],
            "citation": "Section 87, Consumer Protection Act, 2019",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "rera_act_2016": {
        "11": {
            "section_number": "11",
            "official_section_title": "Functions and duties of promoter",
            "official_text": "(1) The promoter shall, upon receiving his Login Id and password... create his web page on the website of the Authority and enter all details of the proposed project... (3) The promoter at the time of the booking and issue of allotment letter shall be responsible to make available to the allottee... sanctioned plans, layout plans... (4) The promoter shall— (a) be responsible for all obligations, responsibilities and functions under the provisions of this Act... till the conveyance of all the apartments, plots or buildings... (b) be responsible to obtain the completion certificate or the occupancy certificate, or both.",
            "simplified_explanation": "Mandates that real estate builders and promoters must disclose all project sanctions on the RERA website, provide sanctioned layouts at booking, and obtain official completion/occupancy certificates before handover.",
            "legal_ingredients": [
                "Promoter developing real estate project exceeding 500 sq meters or 8 apartments",
                "Statutory duty to upload quarterly project progress",
                "Obligation to secure Occupancy Certificate (OC) prior to physical possession"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "builder_delay_possession_dispute",
                "real_estate_delayed_possession_interest"
            ],
            "punishment_or_remedy": "RERA Authority directions, penalty up to 5% of estimated project cost under Section 61.",
            "related_provisions": [
                "RERA 2016 Section 12",
                "RERA 2016 Section 18",
                "RERA 2016 Section 19"
            ],
            "exceptions_and_limitations": [
                "Applies strictly to projects registered or registrable under RERA."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "State Real Estate Regulatory Authority (RERA).",
            "applicability_notes": "Builders cannot offer possession on mere 'fit-out' basis without obtaining official completion/occupancy certificate.",
            "keywords": [
                "duties of promoter",
                "occupancy certificate mandatory",
                "completion certificate",
                "quarterly project update",
                "sanctioned layout disclosure"
            ],
            "citation": "Section 11, Real Estate (Regulation and Development) Act, 2016",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "12": {
            "section_number": "12",
            "official_section_title": "Obligations of promoter regarding veracity of advertisement or prospectus",
            "official_text": "Where any person makes an advance or a deposit on the basis of the information contained in the notice, advertisement or prospectus, or on the basis of any model apartment, plot or building... and sustains any loss or damage by reason of any incorrect, false statement included therein, he shall be compensated by the promoter in the manner as provided under this Act: Provided that if the person affected by such incorrect, false statement contained in the notice, advertisement or prospectus, or the model apartment, plot or building, as the case may be, intends to withdraw from the proposed project, he shall be returned his entire investment along with interest at such rate as may be prescribed and the compensation in the manner provided under this Act.",
            "simplified_explanation": "Grants home buyers the statutory right to withdraw from a project and demand a 100% refund of their entire investment with interest and compensation if the builder lured them with false advertisements, fake amenities, or deceptive model apartments.",
            "legal_ingredients": [
                "Deposit or advance made relying on builder's brochure, advertisement, or model flat",
                "False, misleading, or incorrect statement in marketing materials",
                "Allottee intention to withdraw from project or claim damages"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "builder_delay_possession_dispute",
                "misleading_advertisement",
                "advance_booking_token_money_forfeiture"
            ],
            "punishment_or_remedy": "Immediate full refund of all amounts paid plus statutory interest (MCLR + 2%) and compensation from promoter.",
            "related_provisions": [
                "RERA 2016 Section 18",
                "CPA 2019 Section 21"
            ],
            "exceptions_and_limitations": [
                "Allottee must produce copy of advertisement, brochure, or email representations relied upon."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "State RERA Authority & Adjudicating Officer.",
            "applicability_notes": "Potent statutory protection against real estate 'flyer deception', phantom amenities, and bait-and-switch layout changes.",
            "keywords": [
                "false builder advertisement",
                "model flat deception",
                "full refund with interest",
                "withdrawal from project",
                "section 12 rera"
            ],
            "citation": "Section 12, Real Estate (Regulation and Development) Act, 2016",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "19": {
            "section_number": "19",
            "official_section_title": "Rights and duties of allottees",
            "official_text": "(1) The allottee shall be entitled to obtain the information relating to sanctioned plans, layout plans... (3) The allottee shall be entitled to claim the possession of apartment, plot or building... (4) The allottee shall be entitled to claim the refund of amount paid along with interest at such rate as may be prescribed and compensation in the manner as provided under this Act, from the promoter, if the promoter fails to comply or is unable to give possession of the apartment, plot or building in accordance with the terms of agreement for sale... (6) Every allottee, who has entered into an agreement for sale... shall be responsible to make necessary payments in the manner and within the time as specified in the said agreement for sale.",
            "simplified_explanation": "Defines mutual rights and duties: home buyers have the statutory right to timely possession, project information, and full refund with interest if possession is delayed, while having a duty to pay construction-linked installments on time.",
            "legal_ingredients": [
                "Allottee under registered agreement for sale",
                "Right to timely possession as per agreed date",
                "Promoter default triggers statutory right to refund with interest or monthly delay interest"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "builder_delay_possession_dispute",
                "real_estate_delayed_possession_interest"
            ],
            "punishment_or_remedy": "Statutory refund or monthly interest until actual delivery of physical possession.",
            "related_provisions": [
                "RERA 2016 Section 18",
                "RERA 2016 Section 31"
            ],
            "exceptions_and_limitations": [
                "Allottee who defaults in timely milestone payments may be liable to pay delay interest to the promoter."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "State RERA Authority.",
            "applicability_notes": "Statutory benchmark balancing buyer rights with installment payment obligations.",
            "keywords": [
                "rights of allottee",
                "possession timeline",
                "refund with interest",
                "builder default",
                "construction linked payment"
            ],
            "citation": "Section 19, Real Estate (Regulation and Development) Act, 2016",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "43": {
            "section_number": "43",
            "official_section_title": "Establishment of Real Estate Appellate Tribunal",
            "official_text": "(1) The appropriate Government shall, by notification, establish an Appellate Tribunal to be known as the — (name of the State/Union territory) Real Estate Appellate Tribunal... (5) Any person aggrieved by any direction or decision or order made by the Authority or by an adjudicating officer under this Act may prefer an appeal before the Appellate Tribunal having jurisdiction... Provided that where a promoter files an appeal with the Appellate Tribunal, it shall not be entertained, without the promoter first having deposited with the Appellate Tribunal at least thirty per cent. of the penalty, or such higher percentage as may be determined... or the total amount to be paid to the allottee including interest and compensation.",
            "simplified_explanation": "Establishes the Real Estate Appellate Tribunal (REAT) to hear appeals within 60 days. Builders appealing a refund order must pre-deposit 100% of the amount awarded to the allottee (or 30% of penalty), preventing delay tactics.",
            "legal_ingredients": [
                "Appeal preferred within 60 days of RERA Authority order",
                "Promoter appellant must pre-deposit 100% of awarded allottee refund/compensation (Newtech Promoters v. State of UP)"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "builder_delay_possession_dispute",
                "real_estate_delayed_possession_interest"
            ],
            "punishment_or_remedy": "Statutory appeal; mandatory 100% pre-deposit locks builder money for consumer benefit.",
            "related_provisions": [
                "RERA 2016 Section 31",
                "RERA 2016 Section 18"
            ],
            "exceptions_and_limitations": [
                "Delay beyond 60 days can be condoned only on proving sufficient cause."
            ],
            "amendment_status": "In force; 100% pre-deposit upheld by Supreme Court in Newtech Promoters (2021).",
            "jurisdiction": "State Real Estate Appellate Tribunal.",
            "applicability_notes": "High Court level appellate oversight; strict pre-deposit requirement protects home buyers from endless builder litigation.",
            "keywords": [
                "real estate appellate tribunal",
                "reat appeal",
                "mandatory pre deposit",
                "60 days appeal",
                "newtech promoters"
            ],
            "citation": "Section 43, Real Estate (Regulation and Development) Act, 2016",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "food_safety_act_2006": {
        "51": {
            "section_number": "51",
            "official_section_title": "Penalty for sub-standard food",
            "official_text": "Any person who whether by himself or by any other person on his behalf manufactures for sale or stores or sells or distributes or imports any article of food for human consumption which is sub-standard, shall be liable to a penalty which may extend to five lakh rupees.",
            "simplified_explanation": "Imposes a heavy statutory financial penalty of up to Rs 5 Lakh on food manufacturers, cloud kitchens, and restaurants that sell or deliver substandard food that fails statutory nutritional and purity standards.",
            "legal_ingredients": [
                "Article of food intended for human consumption",
                "Failure to meet prescribed quality standards or specifications",
                "Penalty up to Rs 5,00,000 imposed by Adjudicating Officer"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "substandard_adulterated_food_toxic_illness",
                "food_delivery_adulterated_contaminated_meal",
                "defective_product"
            ],
            "punishment_or_remedy": "Penalty up to five lakh rupees.",
            "related_provisions": [
                "Food Safety Act 2006 Section 26",
                "Food Safety Act 2006 Section 59",
                "CPA 2019 Section 84"
            ],
            "exceptions_and_limitations": [
                "Penalty adjudicated by District Additional District Magistrate (ADM/Adjudicating Officer)."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central & State Food Safety Authorities.",
            "applicability_notes": "Directly targets substandard commercial food, cloud kitchen meals, and adulterated food items.",
            "keywords": [
                "sub standard food",
                "penalty up to 5 lakh",
                "food safety penalty",
                "fssai violation",
                "cloud kitchen food defect"
            ],
            "citation": "Section 51, Food Safety and Standards Act, 2006",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "52": {
            "section_number": "52",
            "official_section_title": "Penalty for misbranded food",
            "official_text": "(1) Any person who whether by himself or by any other person on his behalf manufactures for sale or stores or sells or distributes or imports any article of food for human consumption which is misbranded, shall be liable to a penalty which may extend to three lakh rupees... (2) The Adjudicating Officer may issue a direction to the person found guilty of an offence under this section, for taking corrective action.",
            "simplified_explanation": "Imposes a fine of up to Rs 3 Lakh on companies selling misbranded food items that carry misleading labels, false nutritional claims, or conceal artificial additives and preservatives.",
            "legal_ingredients": [
                "Misbranded food with deceptive labels or false claims",
                "Failure to disclose ingredients, allergens, or genuine nutritional values",
                "Penalty up to Rs 3,00,000"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "substandard_adulterated_food_toxic_illness",
                "packaged_food_misleading_nutrition_claims",
                "misleading_advertisement"
            ],
            "punishment_or_remedy": "Penalty up to three lakh rupees, plus recall of misbranded batches.",
            "related_provisions": [
                "Food Safety Act 2006 Section 51",
                "CPA 2019 Section 89",
                "Legal Metrology Act 2009 Section 36"
            ],
            "exceptions_and_limitations": [
                "Excludes minor typographical errors that do not mislead the consumer as to nature or quality."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central & State Food Safety Authorities.",
            "applicability_notes": "Protects consumers against 'health washing', fake organic claims, and hidden chemicals in packaged foods.",
            "keywords": [
                "misbranded food",
                "false nutritional label",
                "penalty up to 3 lakh",
                "fssai misbranding",
                "deceptive food packaging"
            ],
            "citation": "Section 52, Food Safety and Standards Act, 2006",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "54": {
            "section_number": "54",
            "official_section_title": "Penalty for food containing extraneous matter",
            "official_text": "Any person whether by himself or by any other person on his behalf manufactures for sale or stores or sells or distributes or imports any article of food for human consumption containing extraneous matter, shall be liable to a penalty which may extend to one lakh rupees.",
            "simplified_explanation": "Imposes a penalty of up to Rs 1 Lakh on any restaurant, cloud kitchen, or packaged food brand for serving or selling food containing foreign objects, insects, glass, plastic, or dead matter.",
            "legal_ingredients": [
                "Presence of extraneous foreign matter (insects, glass, plastic, hair, stones) in food",
                "Food intended for human consumption",
                "Penalty up to Rs 1,00,000"
            ],
            "domain": "consumer_issues",
            "relevant_issues": [
                "substandard_adulterated_food_toxic_illness",
                "food_delivery_adulterated_contaminated_meal"
            ],
            "punishment_or_remedy": "Penalty up to one lakh rupees, food safety inspection, and consumer damages.",
            "related_provisions": [
                "Food Safety Act 2006 Section 50",
                "Food Safety Act 2006 Section 59",
                "CPA 2019 Section 84"
            ],
            "exceptions_and_limitations": [
                "Extraneous matter must not be inherent to the natural raw product (e.g., fruit seed)."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central & State Food Safety Authorities.",
            "applicability_notes": "Frequently invoked when delivery meals or restaurant food contains insects, dead pests, or sharp objects.",
            "keywords": [
                "extraneous matter in food",
                "insect in food",
                "foreign object in restaurant meal",
                "food contamination penalty",
                "fssai section 54"
            ],
            "citation": "Section 54, Food Safety and Standards Act, 2006",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "mv_act_1988": {
        "110A": {
            "section_number": "110A",
            "official_section_title": "Recall of motor vehicles",
            "official_text": "(1) The Central Government may, by order, direct a manufacturer to recall motor vehicles of a particular type or its variant, if— (a) a defect in that particular type of motor vehicle, or a component of that motor vehicle, may cause harm to the environment or to the driver or occupants of such motor vehicle or to other road users; or (b) a defect in that particular type of motor vehicle has been reported to the Central Government by— (i) such percentage of owners... (2) Where the manufacturer... undertakes to recall... the manufacturer shall— (a) reimburse the buyers... or (b) replace the defective motor vehicle with another motor vehicle of similar or better specifications.",
            "simplified_explanation": "Empowers the Central Government to order mandatory vehicle recalls for critical manufacturing, brake, or steering defects, legally obligating automobile manufacturers to either give buyers a 100% full refund or replace the vehicle with a brand new one.",
            "legal_ingredients": [
                "Systemic defect in vehicle type or component causing safety or environmental hazard",
                "Mandatory order of recall or voluntary recall by manufacturer",
                "Statutory obligation to reimburse full price or replace defective vehicle"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "mandatory_vehicle_safety_recall_defect",
                "automobile_manufacturing_defect_lemon_vehicle",
                "ev_battery_thermal_range_defect"
            ],
            "punishment_or_remedy": "Full vehicle replacement or 100% financial reimbursement to buyer; fine up to Rs 1 Crore on non-compliant manufacturer under Section 182A.",
            "related_provisions": [
                "MV Act 1988 Section 182A",
                "CPA 2019 Section 84"
            ],
            "exceptions_and_limitations": [
                "Defect must be a manufacturing or design defect, not damage caused by post-purchase accidents or unauthorized third-party modifications."
            ],
            "amendment_status": "In force; inserted by Motor Vehicles (Amendment) Act, 2019.",
            "jurisdiction": "Central (Ministry of Road Transport and Highways - MoRTH).",
            "applicability_notes": "Statutory lemon law protection for Indian motor vehicle and EV owners against dangerous manufacturing faults.",
            "keywords": [
                "mandatory vehicle recall",
                "lemon car law india",
                "automobile manufacturing defect",
                "full refund vehicle defect",
                "replacement of defective car"
            ],
            "citation": "Section 110A, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "115": {
            "section_number": "115",
            "official_section_title": "Power to restrict the use of vehicles",
            "official_text": "The State Government or any authority authorised in this behalf by the State Government, if satisfied that it is necessary in the interest of public safety or convenience, or because of the nature of any road or bridge, may, by notification in the Official Gazette, prohibit or restrict, subject to such exceptions and conditions as may be specified in the notification, the driving of motor vehicles or of any specified class or description of motor vehicles or the use of trailers either generally in a specified area or on a specified road.",
            "simplified_explanation": "Authorizes State Governments and traffic commissioners to restrict certain classes of vehicles (e.g. heavy goods trucks in city limits during peak hours) on specific roads or bridges for public safety.",
            "legal_ingredients": [
                "Gazette notification by State Government or authorized traffic authority",
                "Restriction justified by public safety, convenience, or road/bridge condition"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "wrong_side_police_diversion_defense",
                "wrongful_challan"
            ],
            "punishment_or_remedy": "Violation punishable under Section 177 / 179; however, un-notified or arbitrary curbs can be challenged in High Court.",
            "related_provisions": [
                "MV Act 1988 Section 116",
                "MV Act 1988 Section 177"
            ],
            "exceptions_and_limitations": [
                "Emergency vehicles (ambulances, fire engines) are universally exempt."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "State Governments & City Police Commissioners.",
            "applicability_notes": "Legal basis for peak-hour heavy vehicle bans, pedestrian zones, and one-way traffic restrictions.",
            "keywords": [
                "restriction on vehicles",
                "truck peak hour ban",
                "gazette notification traffic",
                "prohibition of driving",
                "section 115 mva"
            ],
            "citation": "Section 115, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "133": {
            "section_number": "133",
            "official_section_title": "Duty of owner of motor vehicle to give information",
            "official_text": "The owner of a motor vehicle the driver or conductor of which is accused of any offence under this Act shall, on the demand of any police officer authorised in this behalf by the State Government, give all information regarding the name and address of, and the licence held by, the driver or conductor which is in his possession or could by reasonable diligence be ascertained by him.",
            "simplified_explanation": "Requires the registered owner of a motor vehicle to provide the true name, address, and driving licence details of the person who was driving the vehicle when an offence or accident occurred.",
            "legal_ingredients": [
                "Accusation of motor vehicle offence involving vehicle",
                "Demand by authorized police officer",
                "Owner obligation to disclose driver identity and licence details"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "document_acceptance_or_verification",
                "mact_accident_compensation_claim",
                "wrongful_challan"
            ],
            "punishment_or_remedy": "Failure by owner punishable under Section 187 with fine up to Rs 500 or imprisonment up to 3 months.",
            "related_provisions": [
                "MV Act 1988 Section 180",
                "MV Act 1988 Section 187"
            ],
            "exceptions_and_limitations": [
                "Owner is not liable if vehicle was stolen and theft was promptly reported to police."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central & State.",
            "applicability_notes": "Prevents vehicle owners from hiding reckless drivers, hit-and-run perpetrators, or unauthorized minors.",
            "keywords": [
                "owner duty to disclose driver",
                "driver identity information",
                "section 133 mva notice",
                "police demand driver name",
                "hit and run driver identification"
            ],
            "citation": "Section 133, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "147": {
            "section_number": "147",
            "official_section_title": "Requirements of policies and limits of liability",
            "official_text": "(1) In order to comply with the requirements of this Chapter, a policy of insurance must be a policy which— (a) is issued by a person who is an authorised insurer; and (b) insures the person or classes of persons specified in the policy to the extent specified in sub-section (2)— (i) against any liability which may be incurred by him in respect of the death of or bodily injury to any person, including owner of the goods or his authorised representative carried in the motor vehicle or damage to any property of a third party caused by or arising out of the use of the motor vehicle in a public place.",
            "simplified_explanation": "Mandates compulsory Third Party Insurance coverage for every motor vehicle in India, guaranteeing compensation for death, bodily injury, or third-party property damage arising from road accidents.",
            "legal_ingredients": [
                "Policy issued by IRDAI-authorized insurer",
                "Compulsory coverage for third-party death, bodily injury, and property damage",
                "Motor vehicle used in public place"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "mact_accident_compensation_claim",
                "insurance_claim_rejection_dispute"
            ],
            "punishment_or_remedy": "Driving without third-party insurance punishable under Section 196 (fine up to Rs 2,000 / Rs 4,000 or imprisonment up to 3 months).",
            "related_provisions": [
                "MV Act 1988 Section 146",
                "MV Act 1988 Section 149",
                "MV Act 1988 Section 166"
            ],
            "exceptions_and_limitations": [
                "Policy does not cover contractual liability unless specifically endorsed."
            ],
            "amendment_status": "In force; Chapter XI substituted by Act 32 of 2019.",
            "jurisdiction": "Central (Applies across all motor vehicles in India).",
            "applicability_notes": "Statutory bedrock of road accident compensation and Motor Accidents Claims Tribunal (MACT) litigation.",
            "keywords": [
                "third party insurance mandatory",
                "limits of liability",
                "accident bodily injury coverage",
                "mact third party claim",
                "section 147 mva"
            ],
            "citation": "Section 147, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "149": {
            "section_number": "149",
            "official_section_title": "Duty of insurers to satisfy judgments and awards against persons insured",
            "official_text": "(1) If, after a certificate of insurance has been issued... judgment or award in respect of any such liability as is required to be covered by a policy... is obtained against any person insured by the policy, then... the insurer shall, subject to the provisions of this section, pay to the person entitled to the benefit of the decree any sum not exceeding the sum assured payable thereunder.",
            "simplified_explanation": "Imposes an absolute statutory duty on insurance companies to pay accident compensation awards decreed by the MACT Court directly to the victim or their family, preventing insurers from evading payments.",
            "legal_ingredients": [
                "Valid certificate of insurance issued",
                "MACT judgment or court decree obtained against insured driver/owner",
                "Statutory obligation on insurer to satisfy award amount"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "mact_accident_compensation_claim",
                "hit_and_run_statutory_solatium_compensation"
            ],
            "punishment_or_remedy": "Direct execution and recovery of award from insurer assets.",
            "related_provisions": [
                "MV Act 1988 Section 147",
                "MV Act 1988 Section 166"
            ],
            "exceptions_and_limitations": [
                "Insurer can defend only on limited statutory grounds (fake driving licence, unauthorized vehicle use) under Section 149(2), and even then must 'pay and recover'."
            ],
            "amendment_status": "In force; 'pay and recover' principle affirmed by Supreme Court.",
            "jurisdiction": "Motor Accidents Claims Tribunal (MACT).",
            "applicability_notes": "Protects road accident victims from driver insolvency; insurer must pay victim first and recover from owner later.",
            "keywords": [
                "insurer duty to pay award",
                "pay and recover",
                "satisfy mact decree",
                "insurance compensation payout",
                "section 149 mva"
            ],
            "citation": "Section 149, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "164": {
            "section_number": "164",
            "official_section_title": "Payment of compensation in case of death or grievous hurt",
            "official_text": "(1) Notwithstanding anything contained in this Act or in any other law for the time being in force or instrument having the force of law, the owner of the motor vehicle or the authorised insurer shall be liable to pay in the case of death or grievous hurt due to any accident arising out of the use of motor vehicle, a compensation, of a sum of five lakh rupees in case of death or of two and a half lakh rupees in case of grievous hurt to the legal heirs or the victim, as the case may be. (2) In any claim for compensation under sub-section (1), the claimant shall not be required to plead or establish that the death or grievous hurt... was due to any wrongful act or neglect or default of the owner of the vehicle.",
            "simplified_explanation": "Provides guaranteed, fast no-fault compensation: Rs 5 Lakh for death and Rs 2.5 Lakh for grievous injury, without the victim needing to prove whose fault or negligence caused the accident.",
            "legal_ingredients": [
                "Death or grievous hurt arising out of motor vehicle accident",
                "Claimant NOT required to plead or prove wrongful act, negligence, or fault",
                "Fixed statutory compensation: Rs 5,00,000 for death, Rs 2,50,000 for grievous hurt"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "hit_and_run_statutory_solatium_compensation",
                "mact_accident_compensation_claim"
            ],
            "punishment_or_remedy": "Immediate no-fault statutory compensation of Rs 5 Lakh (death) or Rs 2.5 Lakh (grievous hurt) paid by owner/insurer within 30 days.",
            "related_provisions": [
                "MV Act 1988 Section 161",
                "MV Act 1988 Section 166"
            ],
            "exceptions_and_limitations": [
                "If claimant receives Section 164 compensation, they cannot pursue a fault-based claim under Section 166."
            ],
            "amendment_status": "In force; inserted by 2019 Amendment Act replacing former Section 163A.",
            "jurisdiction": "MACT & MoRTH Claims Settlement.",
            "applicability_notes": "Lifesaver for poor accident victims; eliminates lengthy multi-year negligence trials.",
            "keywords": [
                "no fault liability",
                "5 lakh death compensation",
                "2.5 lakh grievous hurt",
                "no negligence proof required",
                "section 164 mva"
            ],
            "citation": "Section 164, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "182": {
            "section_number": "182",
            "official_section_title": "Offences relating to licences",
            "official_text": "(1) Whoever, being disqualified under this Act for holding or obtaining a driving licence, drives a motor vehicle in a public place or applies for or obtains a driving licence or, not being entitled to have a driving licence issued to him free of endorsement, applies for or obtains a driving licence without giving particulars of such endorsement shall be punishable with imprisonment for a term which may extend to three months, or with fine to the extent of ten thousand rupees, or with both.",
            "simplified_explanation": "Imposes criminal punishment—fine up to Rs 10,000, imprisonment up to 3 months, or both—on anyone who drives a vehicle or secretly applies for a new driving licence while disqualified or suspended by RTO/Court.",
            "legal_ingredients": [
                "Person disqualified or licence suspended under MV Act",
                "Driving motor vehicle in public place or applying for new licence while disqualified"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "driving_while_disqualified_revoked_licence",
                "driving_without_licence_challan"
            ],
            "punishment_or_remedy": "Imprisonment up to three months, or fine up to ten thousand rupees, or both; revocation of newly obtained fraudulent licence.",
            "related_provisions": [
                "MV Act 1988 Section 180",
                "MV Act 1988 Section 181",
                "MV Act 1988 Section 206"
            ],
            "exceptions_and_limitations": [
                "Does not apply if disqualification order was formally stayed by appellate transport authority or court."
            ],
            "amendment_status": "In force; fine increased from Rs 500 to Rs 10,000 by 2019 Amendment Act.",
            "jurisdiction": "Central & State.",
            "applicability_notes": "Severely punishes suspended drunk drivers or disqualified road offenders who continue driving illegally.",
            "keywords": [
                "driving while disqualified",
                "revoked licence driving",
                "10000 rupees fine",
                "three months imprisonment",
                "suspended driving licence"
            ],
            "citation": "Section 182, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "186": {
            "section_number": "186",
            "official_section_title": "Driving when mentally or physically unfit to drive",
            "official_text": "Whoever drives a motor vehicle in any public place when he is to his knowledge suffering from any disease or disability calculated to cause his driving of the vehicle to be a source of danger to the public, shall be punishable for the first offence with fine which may extend to one thousand rupees and for a second or subsequent offence with fine which may extend to two thousand rupees.",
            "simplified_explanation": "Penalizes driving a motor vehicle in public when suffering from a severe physical or mental condition (e.g. epileptic seizures, uncorrected vision loss, acute impairment) that endangers road safety.",
            "legal_ingredients": [
                "Driving motor vehicle in a public place",
                "Knowledge of suffering from disease or disability calculated to cause danger to public"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "mentally_physically_unfit_driving",
                "dangerous_driving_challan"
            ],
            "punishment_or_remedy": "Fine up to Rs 1,000 for first offence, Rs 2,000 for subsequent offence; suspension of driving licence under Section 19.",
            "related_provisions": [
                "MV Act 1988 Section 184",
                "MV Act 1988 Section 185",
                "MV Act 1988 Section 19"
            ],
            "exceptions_and_limitations": [
                "Persons driving specially adapted invalid carriages or vehicles modified for persons with disabilities with RTO medical clearance are exempt."
            ],
            "amendment_status": "In force; fines updated by Act 32 of 2019.",
            "jurisdiction": "Central & State.",
            "applicability_notes": "Statutory ground for revoking driving licences of individuals who develop incapacitating medical conditions.",
            "keywords": [
                "physically unfit driving",
                "medical disability driving",
                "epilepsy driving risk",
                "danger to public",
                "licence revocation medical grounds"
            ],
            "citation": "Section 186, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "197": {
            "section_number": "197",
            "official_section_title": "Taking vehicle without authority",
            "official_text": "(1) Whoever takes and drives away any motor vehicle without having either the consent of the owner thereof or other lawful authority shall be punishable with imprisonment which may extend to three months, or with fine which may extend to five thousand rupees, or with both... (2) Any person who, knowing that a motor vehicle has been so taken, drives it or allows himself to be carried in it without such consent or authority shall be punishable with imprisonment which may extend to three months, or with fine which may extend to five thousand rupees, or with both.",
            "simplified_explanation": "Penalizes joyriding or taking away someone's motor vehicle without owner consent (even without intent to permanently steal it) with imprisonment up to 3 months, fine up to Rs 5,000, or both, covering both driver and passengers.",
            "legal_ingredients": [
                "Taking and driving away motor vehicle without owner consent or lawful authority",
                "Or traveling as passenger knowing vehicle was taken without consent"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "unlawful_towing",
                "vehicle_detention"
            ],
            "punishment_or_remedy": "Imprisonment up to three months, or fine up to five thousand rupees, or both.",
            "related_provisions": [
                "BNS 2023 Section 303",
                "MV Act 1988 Section 198"
            ],
            "exceptions_and_limitations": [
                "Accused had reasonable belief that he had lawful authority or that owner would have consented under circumstances."
            ],
            "amendment_status": "In force; fine raised from Rs 500 to Rs 5,000 by 2019 Amendment Act.",
            "jurisdiction": "Central & State.",
            "applicability_notes": "Applies to unauthorized joyriding, mechanics taking customer cars for unauthorized personal trips, or valet misuse.",
            "keywords": [
                "joyriding",
                "taking vehicle without consent",
                "mechanic unauthorized car drive",
                "valet misuse vehicle",
                "section 197 mva"
            ],
            "citation": "Section 197, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "198": {
            "section_number": "198",
            "official_section_title": "Unauthorized interference with vehicle",
            "official_text": "Whoever otherwise than with lawful authority or reasonable excuse enters or mounts any stationary motor vehicle or tampers with the brake or any part of the mechanism of a motor vehicle shall be punishable with fine which may extend to one thousand rupees.",
            "simplified_explanation": "Makes it an offence to enter, mount, or tamper with the brakes or mechanical parts of a stationary motor vehicle without lawful authority or reasonable excuse, punishable with fine up to Rs 1,000.",
            "legal_ingredients": [
                "Stationary motor vehicle",
                "Entering, mounting, or tampering with brakes or mechanism without lawful authority or reasonable excuse"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "unlawful_towing_occupant_inside_vehicle",
                "unlawful_towing"
            ],
            "punishment_or_remedy": "Fine up to one thousand rupees.",
            "related_provisions": [
                "MV Act 1988 Section 197",
                "MV Act 1988 Section 201"
            ],
            "exceptions_and_limitations": [
                "Authorized police officers executing lawful seizure or towing with reasonable excuse."
            ],
            "amendment_status": "In force; fine raised from Rs 100 to Rs 1,000 by 2019 Amendment Act.",
            "jurisdiction": "Central & State.",
            "applicability_notes": "Protects private parked vehicles from vandalism, unauthorized entry, or private recovery agents tampering with brakes.",
            "keywords": [
                "tampering with vehicle",
                "brake tampering",
                "unauthorized mounting",
                "entering stationary car",
                "section 198 mva"
            ],
            "citation": "Section 198, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "201": {
            "section_number": "201",
            "official_section_title": "Penalty for causing obstruction to free flow of traffic",
            "official_text": "(1) Whoever keeps a disabled vehicle on any public place, in such a manner, so as to cause impediment to the free flow of traffic, shall be liable for penalty up to fifty rupees per hour, so long as it remains situated... (2) Where any vehicle is abandoned or left unattended in a public place for more than ten hours by its owner or driver or is parked in a place where parking is legally prohibited, its removal by a towing service or its immobilisation by the use of wheel clamps may be authorised by a police officer in uniform... Provided that the owner of the motor vehicle shall be liable to pay the towing charges and the penalty as prescribed.",
            "simplified_explanation": "Governs traffic obstruction, vehicle breakdown, and towing: police may authorize towing or wheel clamping only for vehicles parked illegally or left unattended for over 10 hours, with prescribed statutory towing fees.",
            "legal_ingredients": [
                "Disabled vehicle left causing impediment to traffic flow",
                "Or vehicle left unattended for over 10 hours or in strictly prohibited no-parking zone",
                "Authorization by police officer in uniform for towing or wheel clamping"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "traffic_obstruction_unreasonable_towing_charges",
                "unlawful_towing",
                "unlawful_towing_occupant_inside_vehicle"
            ],
            "punishment_or_remedy": "Prescribed statutory towing fee and obstruction penalty; illegal private towing charges can be refunded.",
            "related_provisions": [
                "MV Act 1988 Section 127",
                "MV Act 1988 Section 200"
            ],
            "exceptions_and_limitations": [
                "Towing is unlawful if driver or occupant is seated inside vehicle, or if breakdown warning lights were displayed and driver was arranging repair."
            ],
            "amendment_status": "In force; towing rules updated by 2019 Amendment Act.",
            "jurisdiction": "Central & State Police Regulations.",
            "applicability_notes": "Essential statutory check against arbitrary private towing contractors and exorbitant towing fines.",
            "keywords": [
                "traffic obstruction penalty",
                "towing charges",
                "wheel clamping",
                "illegal towing dispute",
                "10 hours unattended vehicle"
            ],
            "citation": "Section 201, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "209": {
            "section_number": "209",
            "official_section_title": "Restriction on conviction",
            "official_text": "No person prosecuted for an offence punishable under section 183 or section 184 shall be convicted unless— (a) he was warned at the time the offence was committed that the question of prosecuting him would be taken into consideration, or (b) within fourteen days from the commission of the offence, a notice specifying the nature of the alleged offence and the time and place where it is alleged to have been committed was served on or sent by registered post to him or the person registered as the owner of the vehicle.",
            "simplified_explanation": "Provides a powerful statutory protection for drivers: no person can be legally convicted or fined for speeding (Section 183) or dangerous driving (Section 184) unless warned at the time of the offence or served with a formal notice within 14 days.",
            "legal_ingredients": [
                "Prosecution for speeding (S. 183) or dangerous driving (S. 184)",
                "Statutory requirement: driver was warned at the spot, OR formal notice served/dispatched within 14 days",
                "Failure of police to notify within 14 days completely bars lawful conviction"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "statutory_14_day_traffic_prosecution_notice_defense",
                "wrongful_challan",
                "speed_camera_calibration_challan"
            ],
            "punishment_or_remedy": "Absolute statutory bar on conviction; delayed traffic challans served months later are legally void.",
            "related_provisions": [
                "MV Act 1988 Section 183",
                "MV Act 1988 Section 184",
                "CMVR 1989 Rule 167A"
            ],
            "exceptions_and_limitations": [
                "Bar does not apply if delay was caused by driver failing to provide correct registered address on Vahan portal."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central (Applies to all traffic courts across India).",
            "applicability_notes": "Key legal defense against delayed automated camera challans sent months after the alleged incident.",
            "keywords": [
                "14 day notice requirement",
                "restriction on conviction",
                "delayed challan void",
                "speeding notice deadline",
                "section 209 mva"
            ],
            "citation": "Section 209, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "210B": {
            "section_number": "210B",
            "official_section_title": "Penalty for offence committed by an authority for enforcing this Act",
            "official_text": "Any authority that is empowered to enforce the provisions of this Act shall, if such authority commits an offence under this Act, be liable for twice the penalty corresponding to that offence under this Act.",
            "simplified_explanation": "Mandates that if a traffic police officer, transport inspector, or enforcement official commits a traffic violation (e.g. driving without helmet, jumping signal, using mobile while driving), they must pay TWICE (double) the normal fine.",
            "legal_ingredients": [
                "Individual is an authority empowered to enforce the Motor Vehicles Act (traffic police, RTO officer)",
                "Commission of traffic violation or offence under MV Act",
                "Statutory mandate: double (2x) the penalty prescribed for ordinary citizens"
            ],
            "domain": "traffic_enforcement",
            "relevant_issues": [
                "traffic_enforcing_officer_violation_double_penalty",
                "wrongful_challan"
            ],
            "punishment_or_remedy": "Twice (200%) the standard statutory penalty, plus departmental disciplinary inquiry.",
            "related_provisions": [
                "MV Act 1988 Section 129",
                "MV Act 1988 Section 194D",
                "Prevention of Corruption Act 1988 Section 7"
            ],
            "exceptions_and_limitations": [
                "Police officers acting under bona fide emergency dispatch (pursuit of fleeing criminal) are protected."
            ],
            "amendment_status": "In force; landmark accountability provision inserted by Act 32 of 2019.",
            "jurisdiction": "Central & State Police / Transport Departments.",
            "applicability_notes": "Crucial provision for citizen dignity; ensures traffic police are held to higher statutory standards than the public.",
            "keywords": [
                "double penalty for police",
                "enforcing authority violation",
                "twice the fine",
                "police traffic violation",
                "section 210b mva"
            ],
            "citation": "Section 210B, Motor Vehicles Act, 1988",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "industrial_disputes_act_1947": {
        "2A": {
            "section_number": "2A",
            "official_section_title": "Dismissal, etc., of an individual workman to be deemed to be an industrial dispute",
            "official_text": "(1) Where any employer discharges, dismisses, retrenches or otherwise terminates the services of an individual workman, any dispute or difference between that workman and his employer connected with, or arising out of, such discharge, dismissal, retrenchment or termination shall be deemed to be an industrial dispute notwithstanding that no other workman nor any union of workmen is a party to the dispute... (2) The workman may make an application direct to the Labour Court or Tribunal for adjudication of the dispute after the expiry of three months from the date he made the application to the Conciliation Officer.",
            "simplified_explanation": "Guarantees that an individual employee who is fired, dismissed, or terminated can file an industrial dispute directly before the Labour Court after 3 months of conciliation, without needing a trade union or other workers to back them.",
            "legal_ingredients": [
                "Individual workman discharged, dismissed, retrenched, or terminated",
                "Dispute deemed an industrial dispute by operation of law",
                "Right to apply directly to Labour Court after 3 months of conciliation application"
            ],
            "domain": "workplace_wage",
            "relevant_issues": [
                "individual_workman_termination_industrial_dispute",
                "unlawful_termination_without_due_process",
                "forced_resignation_notice_pay_deduction"
            ],
            "punishment_or_remedy": "Reinstatement with full back wages, continuity of service, and compensation.",
            "related_provisions": [
                "Industrial Disputes Act 1947 Section 10",
                "Industrial Disputes Act 1947 Section 25F",
                "Industrial Disputes Act 1947 Section 33C"
            ],
            "exceptions_and_limitations": [
                "Application must be filed before the Labour Court within three years from the date of discharge or termination."
            ],
            "amendment_status": "In force; Section 2A(2) inserted by Act 24 of 2010 granting direct access to Labour Court.",
            "jurisdiction": "Central & State Labour Courts / Industrial Tribunals.",
            "applicability_notes": "Eliminates the historical barrier where individual non-union employees could not access Labour Courts.",
            "keywords": [
                "individual termination dispute",
                "direct application to labour court",
                "deemed industrial dispute",
                "3 months conciliation window",
                "reinstatement back wages"
            ],
            "citation": "Section 2A, Industrial Disputes Act, 1947",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "9A": {
            "section_number": "9A",
            "official_section_title": "Notice of change",
            "official_text": "No employer, who proposes to effect any change in the conditions of service applicable to any workman in respect of any matter specified in the Fourth Schedule, shall effect such change,— (a) without giving to the workmen likely to be affected by such change a notice in the prescribed manner of the nature of the change proposed to be effected; or (b) within twenty-one days of giving such notice.",
            "simplified_explanation": "Prohibits employers from unilaterally altering working hours, shift timings, rest intervals, pay allowances, or leave rules without giving affected employees a mandatory 21 days written statutory notice.",
            "legal_ingredients": [
                "Proposed change in Fourth Schedule matters (wages, hours, shifts, leave, allowances)",
                "Statutory requirement: mandatory written notice to affected employees",
                "Mandatory 21-day cooling period before change can take effect"
            ],
            "domain": "workplace_wage",
            "relevant_issues": [
                "unilateral_change_in_service_conditions_without_notice",
                "split_shift_excessive_spreadover_hospitality",
                "variable_pay_retrospective_target_shifting"
            ],
            "punishment_or_remedy": "Unilateral change void ab initio; penal action against employer under Section 31.",
            "related_provisions": [
                "Industrial Disputes Act 1947 Section 33",
                "Standing Orders Act 1946 Section 3"
            ],
            "exceptions_and_limitations": [
                "Notice not required where change is effected pursuant to any settlement or award of an Industrial Tribunal."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central & State Labour Departments.",
            "applicability_notes": "Essential defense against sudden employer pay cuts, forced overtime shifts, or arbitrary schedule changes.",
            "keywords": [
                "notice of change",
                "21 days notice",
                "fourth schedule",
                "unilateral shift change",
                "alteration of service conditions"
            ],
            "citation": "Section 9A, Industrial Disputes Act, 1947",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "10": {
            "section_number": "10",
            "official_section_title": "Reference of disputes to Boards, Courts or Tribunals",
            "official_text": "(1) Where the appropriate Government is of opinion that any industrial dispute exists or is apprehended, it may at any time, by order in writing— (c) refer the dispute or any matter appearing to be connected with, or relevant to, the dispute... to a Labour Court for adjudication; (d) refer the dispute or any matter appearing to be connected with, or relevant to, the dispute... to a Tribunal for adjudication.",
            "simplified_explanation": "Statutory mechanism by which the Government or conciliation officer refers an unresolved employer-employee dispute to the Labour Court or Industrial Tribunal for binding judicial adjudication.",
            "legal_ingredients": [
                "Existence or apprehension of industrial dispute",
                "Failure of conciliation proceedings (Failure of Conciliation - FOC report)",
                "Formal order of reference by appropriate Government to Labour Court/Tribunal"
            ],
            "domain": "workplace_wage",
            "relevant_issues": [
                "individual_workman_termination_industrial_dispute",
                "delayed_wages",
                "unpaid_wages"
            ],
            "punishment_or_remedy": "Binding judicial award enforceable as decree of court; back wages, reinstatement, or financial settlement.",
            "related_provisions": [
                "Industrial Disputes Act 1947 Section 2A",
                "Industrial Disputes Act 1947 Section 11",
                "Industrial Disputes Act 1947 Section 33C"
            ],
            "exceptions_and_limitations": [
                "Disputes relating to managerial/administrative personnel earning above statutory threshold are excluded from 'workman' definition."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Labour Court / Industrial Tribunal.",
            "applicability_notes": "Core dispute resolution path for all collective and referred individual labour disputes in India.",
            "keywords": [
                "reference of dispute",
                "labour court adjudication",
                "industrial tribunal award",
                "foc report",
                "section 10 reference"
            ],
            "citation": "Section 10, Industrial Disputes Act, 1947",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "33": {
            "section_number": "33",
            "official_section_title": "Conditions of service, etc., to remain unchanged during pendency of proceedings",
            "official_text": "(1) During the pendency of any conciliation proceeding before a conciliation officer or a Board or of any proceeding before an arbitrator or a Labour Court or Tribunal or National Tribunal in respect of an industrial dispute, no employer shall— (a) in regard to any matter connected with the dispute, alter to the prejudice of the workmen concerned in such dispute, the conditions of service applicable to them immediately before the commencement of such proceeding; or (b) for any misconduct connected with the dispute, discharge or punish, whether by dismissal or otherwise, any workmen concerned in such dispute, save with the express permission in writing of the authority before which the proceeding is pending.",
            "simplified_explanation": "Prohibits employers from firing, suspending, transferring, or cutting the pay of employees while a labour dispute is pending before a Conciliation Officer or Labour Court, unless express prior written permission is obtained.",
            "legal_ingredients": [
                "Pendency of conciliation or Labour Court proceedings",
                "Alteration of service conditions or dismissal of workman during proceedings",
                "Absence of express prior written permission from conciliation authority/tribunal"
            ],
            "domain": "workplace_wage",
            "relevant_issues": [
                "unlawful_alteration_of_service_conditions_during_conciliation",
                "unlawful_termination_without_due_process",
                "forced_resignation_notice_pay_deduction"
            ],
            "punishment_or_remedy": "Action taken in violation of Section 33 is void ab initio (Jaipur Zila Sahakari Bhoomi Vikas Bank v. Ram Gopal Sharma); complaint under Section 33A.",
            "related_provisions": [
                "Industrial Disputes Act 1947 Section 33A",
                "Industrial Disputes Act 1947 Section 9A"
            ],
            "exceptions_and_limitations": [
                "For misconduct not connected with the dispute, employer may discharge on paying one month wages and applying for approval under S. 33(2)(b)."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Labour Conciliation Officers and Labour Courts.",
            "applicability_notes": "Vital shield protecting employees against management retaliation as soon as they approach the Labour Department.",
            "keywords": [
                "conditions of service unchanged",
                "pendency of conciliation",
                "section 33 protection",
                "employer retaliation ban",
                "approval application"
            ],
            "citation": "Section 33, Industrial Disputes Act, 1947",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "posh_act_2013": {
        "2_n": {
            "section_number": "2(n)",
            "official_section_title": "Definition of sexual harassment",
            "official_text": "\"sexual harassment\" includes any one or more of the following unwelcome acts or behaviour (whether directly or by implication) namely:— (i) physical contact and advances; or (ii) a demand or request for sexual favours; or (iii) making sexually coloured remarks; or (iv) showing pornography; or (v) any other unwelcome physical, verbal or non-verbal conduct of sexual nature.",
            "simplified_explanation": "Defines sexual harassment at the workplace comprehensively: covers unwanted physical touch, sexual advances, demands for sexual favours, sexually coloured remarks, sharing explicit media, and any unwelcome verbal or non-verbal sexual conduct.",
            "legal_ingredients": [
                "Unwelcome physical, verbal, or non-verbal conduct of a sexual nature",
                "Direct or implied advances, demands, or sexually coloured remarks",
                "Workplace context or work-related interaction"
            ],
            "domain": "workplace_wage",
            "relevant_issues": [
                "posh_workplace_sexual_harassment_complaint",
                "retaliatory_action_posh_complainant"
            ],
            "punishment_or_remedy": "Triggers mandatory Internal Committee (IC) inquiry; disciplinary action, wage deduction, or termination of respondent.",
            "related_provisions": [
                "POSH Act 2013 Section 3",
                "POSH Act 2013 Section 9",
                "BNS 2023 Section 78"
            ],
            "exceptions_and_limitations": [
                "Subjective perception of victim is primary standard; intention of respondent is secondary."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central (Applies across all private and public workplaces in India).",
            "applicability_notes": "Statutory baseline for determining actionable workplace harassment in corporate, industrial, and remote work environments.",
            "keywords": [
                "definition of sexual harassment",
                "unwelcome physical contact",
                "sexually coloured remarks",
                "demand for sexual favours",
                "posh section 2n"
            ],
            "citation": "Section 2(n), Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "3": {
            "section_number": "3",
            "official_section_title": "Prevention of sexual harassment",
            "official_text": "(1) No woman shall be subjected to sexual harassment at any workplace. (2) The following circumstances, among other circumstances, if it occurs, or is present in relation to or connected with any act or behavior of sexual harassment may amount to sexual harassment:— (i) implied or explicit promise of preferential treatment in her employment; or (ii) implied or explicit threat of detrimental treatment in her employment; or (iii) implied or explicit threat about her present or future employment status; or (iv) interference with her work or creating an intimidating or offensive or hostile work environment for her; or (v) humiliating treatment likely to affect her health or safety.",
            "simplified_explanation": "Expressly prohibits hostile work environments, quid pro quo harassment, preferential treatment promises, threats to job security, and humiliating conduct affecting a woman's health or psychological safety at work.",
            "legal_ingredients": [
                "Workplace conduct creating hostile or intimidating environment",
                "Implied or explicit promise of promotion or threat of demotion/termination connected to sexual conduct",
                "Humiliating treatment affecting health or psychological safety"
            ],
            "domain": "workplace_wage",
            "relevant_issues": [
                "posh_workplace_sexual_harassment_complaint",
                "retaliatory_action_posh_complainant"
            ],
            "punishment_or_remedy": "Disciplinary action, interim transfer of respondent, paid leave to complainant, and financial compensation.",
            "related_provisions": [
                "POSH Act 2013 Section 12",
                "POSH Act 2013 Section 13"
            ],
            "exceptions_and_limitations": [
                "Applies to all workplaces including virtual platforms, off-site client meetings, and office parties."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Prohibits corporate environments that silently tolerate toxicity or retaliate against women speaking up.",
            "keywords": [
                "hostile work environment",
                "quid pro quo harassment",
                "threat to employment status",
                "humiliating treatment",
                "section 3 posh"
            ],
            "citation": "Section 3, Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "18": {
            "section_number": "18",
            "official_section_title": "Appeal",
            "official_text": "(1) Any person aggrieved from the recommendations made under sub-section (2) of section 13 or under clause (i) or clause (ii) of sub-section (3) of section 13 or sub-section (1) or sub-section (2) of section 14 or section 17 or non-implementation of such recommendations may prefer an appeal to the court or tribunal in accordance with the provisions of the service rules applicable to the said person or where no such service rules exist... to an appellate authority notified under clause (a) of section 2 of the Industrial Employment (Standing Orders) Act, 1946... (2) The appeal shall be preferred within a period of ninety days of the recommendations.",
            "simplified_explanation": "Provides a statutory right of appeal within 90 days to a court, tribunal, or appellate authority if the Internal Committee (IC) report is biased, procedural guidelines were flouted, or the employer refuses to implement recommendations.",
            "legal_ingredients": [
                "Aggrieved by IC recommendations, finding, or employer non-implementation",
                "Appeal filed within 90 days from date of recommendation",
                "Appellate forum: service tribunal, Labour Court, or notified appellate authority"
            ],
            "domain": "workplace_wage",
            "relevant_issues": [
                "retaliatory_action_posh_complainant",
                "posh_workplace_sexual_harassment_complaint"
            ],
            "punishment_or_remedy": "Appellate authority can set aside flawed IC report, order fresh independent inquiry, or enforce compensation.",
            "related_provisions": [
                "POSH Act 2013 Section 13",
                "POSH Act 2013 Section 26"
            ],
            "exceptions_and_limitations": [
                "Appeal must be filed within 90 days."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central & State (Appellate Authorities and High Courts).",
            "applicability_notes": "Vital legal remedy when company management influences the Internal Committee to whitewash executive misconduct.",
            "keywords": [
                "posh appeal",
                "90 days appeal deadline",
                "biased ic report appeal",
                "non implementation of posh recommendations",
                "section 18 posh"
            ],
            "citation": "Section 18, Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "19": {
            "section_number": "19",
            "official_section_title": "Duties of employer",
            "official_text": "Every employer shall— (a) provide a safe working environment at the workplace which shall include safety from the persons coming into contact at the workplace; (b) display at any conspicuous place in the workplace, the penal consequences of sexual harassments; and the order constituting, the Internal Committee; (c) organise workshops and awareness programmes at regular intervals for sensitising the employees... (h) cause to initiate action, under the Indian Penal Code or any other law for the time being in force, against the perpetrator.",
            "simplified_explanation": "Mandates that employers must provide a safe working environment, display the constitution of the Internal Committee and penal consequences publicly, conduct regular employee sensitization, and assist the victim in filing a police complaint.",
            "legal_ingredients": [
                "Employer in private or public sector",
                "Statutory duty to maintain safe working environment, display IC notices, and assist victim in police complaint",
                "Non-compliance punishable under Section 26 with fine up to Rs 50,000 and cancellation of business licence"
            ],
            "domain": "workplace_wage",
            "relevant_issues": [
                "posh_workplace_sexual_harassment_complaint",
                "retaliatory_action_posh_complainant"
            ],
            "punishment_or_remedy": "Penalty up to Rs 50,000 under Section 26; repeated violation leads to cancellation of business licence or registration.",
            "related_provisions": [
                "POSH Act 2013 Section 4",
                "POSH Act 2013 Section 26"
            ],
            "exceptions_and_limitations": [
                "Applies to all employers having 10 or more employees."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central & State District Officers.",
            "applicability_notes": "Employers cannot plead ignorance; failure to constitute IC or conduct sensitization triggers heavy statutory penalties.",
            "keywords": [
                "duties of employer posh",
                "safe working environment",
                "ic notice display",
                "penalty for not constituting ic",
                "section 19 posh"
            ],
            "citation": "Section 19, Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "contract_act_1872": {
        "14": {
            "section_number": "14",
            "official_section_title": "Free consent defined",
            "official_text": "Consent is said to be free when it is not caused by— (1) coercion, as defined in section 15, or (2) undue influence, as defined in section 16, or (3) fraud, as defined in section 17, or (4) misrepresentation, as defined in section 18, or (5) mistake, subject to the provisions of sections 20, 21 and 22. Consent is said to be so caused when it would not have been given but for the existence of such coercion, undue influence, fraud, misrepresentation or mistake.",
            "simplified_explanation": "Establishes that a valid contract requires genuine free consent. If consent was obtained through coercion, pressure, fraud, false representations, or factual mistake, the contract is legally flawed and voidable.",
            "legal_ingredients": [
                "Agreement entered into between parties",
                "Absence of coercion, undue influence, fraud, misrepresentation, or bilateral mistake of fact"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "breach_of_contract",
                "employment_bond_original_certificate_retention",
                "advance_booking_token_money_forfeiture"
            ],
            "punishment_or_remedy": "Contract voidable at the option of the party whose consent was vitiated under Section 19.",
            "related_provisions": [
                "Contract Act 1872 Section 15",
                "Contract Act 1872 Section 16",
                "Contract Act 1872 Section 17",
                "Contract Act 1872 Section 19"
            ],
            "exceptions_and_limitations": [
                "If party had the means of discovering the truth with ordinary diligence in cases of misrepresentation."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central (Civil Courts).",
            "applicability_notes": "The foundation stone of Indian contract law; protects citizens coerced into signing one-sided indemnity bonds or unfair agreements.",
            "keywords": [
                "free consent",
                "coercion",
                "undue influence",
                "vitiated consent",
                "section 14 contract act"
            ],
            "citation": "Section 14, Indian Contract Act, 1872",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "20": {
            "section_number": "20",
            "official_section_title": "Agreement void where both parties are under mistake as to matter of fact",
            "official_text": "Where both the parties to an agreement are under a mistake as to a matter of fact essential to the agreement, the agreement is void. Explanation.—An erroneous opinion as to the value of the thing which forms the subject-matter of the agreement is not to be deemed a mistake as to a matter of fact.",
            "simplified_explanation": "Renders an agreement completely void from the beginning if both parties entered into it under a mutual mistake regarding a fundamental factual matter essential to the contract (e.g. goods already destroyed unknown to both).",
            "legal_ingredients": [
                "Bilateral mistake common to both parties",
                "Mistake relates to an essential matter of fact, not mere opinion of value"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "breach_of_contract",
                "advance_deposit_forfeiture_dispute"
            ],
            "punishment_or_remedy": "Agreement void ab initio; restoration of advantages or money under Section 65.",
            "related_provisions": [
                "Contract Act 1872 Section 21",
                "Contract Act 1872 Section 65"
            ],
            "exceptions_and_limitations": [
                "A mistake as to market price or commercial profitability does not void the agreement."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Enables citizens to escape accidental or impossible contracts and recover advance deposits.",
            "keywords": [
                "mutual mistake of fact",
                "bilateral mistake",
                "void agreement",
                "essential fact mistake",
                "section 20 contract act"
            ],
            "citation": "Section 20, Indian Contract Act, 1872",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "21": {
            "section_number": "21",
            "official_section_title": "Effect of mistakes as to law",
            "official_text": "A contract is not voidable because it was caused by a mistake as to any law in force in India; but a mistake as to a law not in force in India has the same effect as a mistake of fact.",
            "simplified_explanation": "Reaffirms the universal legal maxim that ignorance or mistake of Indian domestic law does not excuse non-performance or void a contract (ignorantia juris non excusat).",
            "legal_ingredients": [
                "Mistake relating to a law in force in India",
                "Contract remains fully valid and binding despite party's misconception of law"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "breach_of_contract",
                "commercial_dispute_mandatory_pre_institution_mediation"
            ],
            "punishment_or_remedy": "Contract remains enforceable; party cannot escape contractual performance on plea of ignorance of law.",
            "related_provisions": [
                "Contract Act 1872 Section 20",
                "Contract Act 1872 Section 14"
            ],
            "exceptions_and_limitations": [
                "A mistake regarding foreign law is treated as a mistake of fact under the proviso."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Parties cannot evade commercial contracts by claiming they were unaware of Indian statutory regulations.",
            "keywords": [
                "mistake of law",
                "ignorantia juris non excusat",
                "enforceable contract",
                "mistake of indian law",
                "section 21 contract act"
            ],
            "citation": "Section 21, Indian Contract Act, 1872",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "32": {
            "section_number": "32",
            "official_section_title": "Enforcement of contracts contingent on an event happening",
            "official_text": "Contingent contracts to do or not to do anything if an uncertain future event happens cannot be enforced by law unless and until that event has happened. If the event becomes impossible, such contracts become void.",
            "simplified_explanation": "Governs contingent contracts: an agreement conditional on an uncertain future event (e.g. obtaining bank loan approval or municipal building sanction) cannot be legally enforced until that condition occurs, and becomes void if the condition becomes impossible.",
            "legal_ingredients": [
                "Contract expressly dependent on collateral uncertain future event",
                "Condition precedent must occur before performance can be demanded",
                "Contract becomes void if the event becomes impossible"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "breach_of_contract",
                "advance_deposit_forfeiture_dispute"
            ],
            "punishment_or_remedy": "Contract becomes void upon impossibility; refund of advance deposits under Section 65.",
            "related_provisions": [
                "Contract Act 1872 Section 56",
                "Contract Act 1872 Section 65"
            ],
            "exceptions_and_limitations": [
                "If the promisor himself wrongfully prevented the contingent event from happening, he cannot benefit from non-occurrence."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Protects buyers who paid token advances subject to bank loan approval or legal clearance.",
            "keywords": [
                "contingent contract",
                "condition precedent",
                "uncertain event",
                "impossible contingency void",
                "section 32 contract act"
            ],
            "citation": "Section 32, Indian Contract Act, 1872",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "51": {
            "section_number": "51",
            "official_section_title": "Promisor not bound to perform, unless reciprocal promisee ready and willing to perform",
            "official_text": "When a contract consists of reciprocal promises to be simultaneously performed, no promisor need perform his promise unless the promisee is ready and willing to perform his reciprocal promise.",
            "simplified_explanation": "Establishes the doctrine of concurrent conditions: in contracts with simultaneous promises (e.g. cash on delivery, or deed execution upon balance payment), neither party is bound to perform unless the other party is genuinely ready and willing to perform their part.",
            "legal_ingredients": [
                "Reciprocal promises intended to be performed simultaneously",
                "Promisor excused from performing if reciprocal promisee is unready or unwilling"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "breach_of_contract",
                "specific_performance_readiness_willingness_dispute",
                "freelance_software_developer_invoice_nonpayment"
            ],
            "punishment_or_remedy": "Lawful withholding of performance; defense against breach of contract claim.",
            "related_provisions": [
                "Contract Act 1872 Section 52",
                "Specific Relief Act 1963 Section 16(c)"
            ],
            "exceptions_and_limitations": [
                "Where contract expressly specifies an agreed order of performance."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Allows software freelancers, suppliers, and service providers to withhold delivery if client refuses milestone payment.",
            "keywords": [
                "reciprocal promises",
                "ready and willing to perform",
                "concurrent conditions",
                "withholding performance",
                "section 51 contract act"
            ],
            "citation": "Section 51, Indian Contract Act, 1872",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "67": {
            "section_number": "67",
            "official_section_title": "Effect of neglect of promisee to afford promisor reasonable facilities for performance",
            "official_text": "If any promisee neglects or refuses to afford the promisor reasonable facilities for the performance of his promise, the promisor is excused by such neglect or refusal as to any non-performance caused thereby.",
            "simplified_explanation": "Excuses a contractor, vendor, or freelancer from liability for delay or non-performance if the client failed to provide necessary approvals, server access, raw materials, or site clearance needed to do the job.",
            "legal_ingredients": [
                "Contract requires cooperation or facility from promisee (access, designs, inputs)",
                "Promisee neglects or refuses to provide reasonable facilities",
                "Promisor excused from non-performance or delay caused by promisee default"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "breach_of_contract",
                "freelance_software_developer_invoice_nonpayment",
                "freelance_vendor_non_payment"
            ],
            "punishment_or_remedy": "Promisor excused from contractual breach; right to claim compensation for expenses incurred.",
            "related_provisions": [
                "Contract Act 1872 Section 53",
                "Contract Act 1872 Section 73"
            ],
            "exceptions_and_limitations": [
                "Promisor must prove that written requests for facilities or access were made and ignored."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Protects IT agencies and independent contractors from liquidated damages when client ghosted or delayed approvals.",
            "keywords": [
                "neglect to afford facilities",
                "client delay defense",
                "excused non performance",
                "lack of access",
                "section 67 contract act"
            ],
            "citation": "Section 67, Indian Contract Act, 1872",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "172": {
            "section_number": "172",
            "official_section_title": "Pledge, Pawnor and Pawnee defined",
            "official_text": "The bailment of goods as security for payment of a debt or performance of a promise is called \"pledge\". The bailor is in this case called the \"pawnor\". The bailee is called the \"pawnee\".",
            "simplified_explanation": "Defines a pledge: the bailment of gold, physical goods, or securities to a lender as collateral security for a loan or debt. The borrower is the pawnor, and the lender/bank is the pawnee.",
            "legal_ingredients": [
                "Bailment and transfer of possession of movable goods",
                "Goods transferred as security for payment of debt or performance of promise"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "pawn_pledge_collateral_default_dispute",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Governs statutory rights and obligations between gold loan borrowers and NBFCs/pawnbrokers.",
            "related_provisions": [
                "Contract Act 1872 Section 176",
                "Contract Act 1872 Section 151"
            ],
            "exceptions_and_limitations": [
                "Pledge requires actual or constructive delivery of possession of goods to pawnee."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Applies to gold loans, share pledges, vehicle pawn loans, and banking collateral disputes.",
            "keywords": [
                "pledge defined",
                "pawnor pawnee",
                "gold loan security",
                "bailment as security",
                "section 172 contract act"
            ],
            "citation": "Section 172, Indian Contract Act, 1872",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "176": {
            "section_number": "176",
            "official_section_title": "Pawnee's right where pawnor makes default",
            "official_text": "If the pawnor makes default in payment of the debt, or performance, at the stipulated time or the promise, in respect of which the goods were pledged, the pawnee may bring a suit against the pawnor upon the debt or promise, and retain the goods pledged as a collateral security; or he may sell the thing pledged, on giving the pawnor reasonable notice of the sale. If the proceeds of such sale are less than the amount due in respect of the debt or promise, the pawnor is still liable to pay the balance. If the proceeds of the sale are greater than the amount so due, the pawnee shall pay over the surplus to the pawnor.",
            "simplified_explanation": "Mandates that if a borrower defaults on a gold loan or pledged collateral, the lender CANNOT secretly sell the pledged goods. The lender MUST give reasonable written notice of auction to the borrower and must immediately refund any surplus proceeds.",
            "legal_ingredients": [
                "Borrower default in repayment of pledged debt",
                "Mandatory statutory requirement: pawnee MUST give reasonable written notice of sale to pawnor",
                "Obligation to return surplus sale proceeds to borrower"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "pawn_pledge_collateral_default_dispute",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Sale conducted without reasonable notice is illegal conversion; borrower entitled to return of gold or damages.",
            "related_provisions": [
                "Contract Act 1872 Section 172",
                "Contract Act 1872 Section 73"
            ],
            "exceptions_and_limitations": [
                "Notice of sale cannot be waived even by express contractual clause (Apex Court in PTC India Financial Services v. Venkateswarlu)."
            ],
            "amendment_status": "In force; non-waivability of notice affirmed by Supreme Court.",
            "jurisdiction": "Central.",
            "applicability_notes": "Vital protection against aggressive NBFCs and gold loan companies secretly auctioning family gold without statutory notice.",
            "keywords": [
                "pawnee right to sell",
                "reasonable notice of auction",
                "gold loan illegal auction",
                "surplus proceeds refund",
                "section 176 contract act"
            ],
            "citation": "Section 176, Indian Contract Act, 1872",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "specific_relief_act_1963": {
        "14": {
            "section_number": "14",
            "official_section_title": "Contracts not specifically enforceable",
            "official_text": "The following contracts cannot be specifically enforced, namely:— (a) where a party to the contract has obtained substituted performance of contract in accordance with the provisions of section 20; (b) a contract, the performance of which involves the performance of a continuous duty which the court cannot supervise; (c) a contract which is so dependent on the personal qualifications of the parties that the court cannot enforce specific performance of its material terms; and (d) a contract which is in its nature determinable.",
            "simplified_explanation": "Specifies contracts that courts cannot order specific performance for: contracts where substituted performance was taken, personal service/employment contracts, contracts requiring continuous court supervision, and contracts that can be terminated by either party (determinable).",
            "legal_ingredients": [
                "Contract falls into statutory exclusion categories",
                "Remedy restricted to monetary compensation/damages rather than specific performance"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "breach_of_contract",
                "specific_performance_readiness_willingness_dispute"
            ],
            "punishment_or_remedy": "Dismissal of specific performance suit; court awards monetary damages under Section 73 Contract Act.",
            "related_provisions": [
                "Specific Relief Act 1963 Section 10",
                "Specific Relief Act 1963 Section 20",
                "Contract Act 1872 Section 73"
            ],
            "exceptions_and_limitations": [
                "Contracts for transfer of immovable property are generally enforceable under Section 10."
            ],
            "amendment_status": "In force; substituted by Specific Relief (Amendment) Act, 2018.",
            "jurisdiction": "Central (Civil Courts).",
            "applicability_notes": "Employers cannot force employees to work, nor can agency partners force personal services under this section.",
            "keywords": [
                "contracts not specifically enforceable",
                "personal service contract",
                "determinable contract",
                "substituted performance",
                "section 14 specific relief act"
            ],
            "citation": "Section 14, Specific Relief Act, 1963",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "16": {
            "section_number": "16",
            "official_section_title": "Personal bars to relief",
            "official_text": "Specific performance of a contract cannot be enforced in favour of a person— (a) who has obtained substituted performance of contract under section 20; or (b) who has become incapable of performing, or violates any essential term of, the contract... or acts in fraud of the contract... or (c) who fails to prove that he has performed or has always been ready and willing to perform the essential terms of the contract which are to be performed by him.",
            "simplified_explanation": "Mandates that a buyer seeking specific performance of a property sale agreement MUST prove continuous 'readiness and willingness' (financial capacity and intent to pay) from the date of the agreement until the trial.",
            "legal_ingredients": [
                "Plaintiff in specific performance suit",
                "Mandatory statutory requirement: proof of continuous readiness (financial capacity) and willingness (mental intent) to perform essential terms",
                "Failure to prove continuous readiness is an absolute statutory bar"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "specific_performance_readiness_willingness_dispute",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Statutory dismissal of specific performance suit if readiness and willingness is not proved.",
            "related_provisions": [
                "Specific Relief Act 1963 Section 10",
                "Contract Act 1872 Section 51"
            ],
            "exceptions_and_limitations": [
                "Readiness does not require carrying physical cash at all times; proving genuine financial capability (bank funds, sanctioned loan) is sufficient."
            ],
            "amendment_status": "In force; 2018 amendment retained Section 16(c) readiness and willingness bar.",
            "jurisdiction": "Central (Civil Courts).",
            "applicability_notes": "Central battleground in all real estate and property sale agreement litigation in India.",
            "keywords": [
                "readiness and willingness",
                "section 16c specific relief",
                "personal bars to relief",
                "property sale agreement suit",
                "financial capacity proof"
            ],
            "citation": "Section 16, Specific Relief Act, 1963",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "41": {
            "section_number": "41",
            "official_section_title": "Injunction when refused",
            "official_text": "An injunction cannot be granted— (e) to prevent the breach of a contract the performance of which would not be specifically enforced; (h) when equally efficacious relief can certainly be obtained by any other usual mode of proceeding except in case of breach of trust; (i) when the conduct of the plaintiff or his agents has been such as to disentitle him to the assistance of the court; (j) when the plaintiff has no personal interest in the matter.",
            "simplified_explanation": "Sets out statutory bars where civil courts cannot grant injunctions: when money damages would be equally efficacious, when the contract itself is not specifically enforceable, or when the plaintiff has unclean hands.",
            "legal_ingredients": [
                "Suit for permanent or temporary injunction",
                "Equally efficacious alternative relief (e.g. monetary damages) available",
                "Or plaintiff's own inequitable conduct disentitles relief"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "breach_of_contract",
                "specific_performance_readiness_willingness_dispute"
            ],
            "punishment_or_remedy": "Refusal and dismissal of injunction application.",
            "related_provisions": [
                "Specific Relief Act 1963 Section 38",
                "Specific Relief Act 1963 Section 14"
            ],
            "exceptions_and_limitations": [
                "Does not apply to clear breaches of trust."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central (Civil Courts).",
            "applicability_notes": "Prevents parties from obtaining frivolous stay orders when their losses can easily be compensated in money.",
            "keywords": [
                "injunction when refused",
                "equally efficacious relief",
                "unclean hands doctrine",
                "stay order refused",
                "section 41 specific relief act"
            ],
            "citation": "Section 41, Specific Relief Act, 1963",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "sale_of_goods_act_1930": {
        "12": {
            "section_number": "12",
            "official_section_title": "Condition and warranty",
            "official_text": "(1) A stipulation in a contract of sale with reference to goods which are the subject thereof may be a condition or a warranty. (2) A condition is a stipulation essential to the main purpose of the contract, the breach of which gives rise to a right to treat the contract as repudiated. (3) A warranty is a stipulation collateral to the main purpose of the contract, the breach of which gives rise to a claim for damages but not to a right to reject the goods and treat the contract as repudiated. (4) Whether a stipulation in a contract of sale is a condition or a warranty depends in each case on the construction of the contract.",
            "simplified_explanation": "Distinguishes between a core Condition and a collateral Warranty: breach of a vital condition entitles the buyer to cancel the contract, reject the goods, and demand a full refund; breach of a warranty only entitles the buyer to claim financial damages.",
            "legal_ingredients": [
                "Contract of sale of goods",
                "Breach of condition: vital stipulation going to root of contract -> right to repudiate contract and reject goods",
                "Breach of warranty: collateral term -> right to monetary damages only"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "condition_vs_warranty_breach_sale_of_goods",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Repudiation of contract and full refund for condition breach; compensation for warranty breach.",
            "related_provisions": [
                "Sale of Goods Act 1930 Section 13",
                "Sale of Goods Act 1930 Section 15",
                "Contract Act 1872 Section 73"
            ],
            "exceptions_and_limitations": [
                "Parties' use of the word 'condition' or 'warranty' in text is not conclusive; courts look at the substance of the agreement."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central (Commercial & Civil Courts).",
            "applicability_notes": "Essential distinction in all commercial procurement, machinery supply, and commodity trading disputes.",
            "keywords": [
                "condition vs warranty",
                "right to repudiate contract",
                "rejection of goods",
                "collateral warranty damages",
                "section 12 sale of goods act"
            ],
            "citation": "Section 12, Sale of Goods Act, 1930",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "13": {
            "section_number": "13",
            "official_section_title": "When condition to be treated as warranty",
            "official_text": "(1) Where a contract of sale is subject to any condition to be fulfilled by the seller, the buyer may waive the condition or elect to treat the breach of the condition as a breach of warranty and not as a ground for treating the contract as repudiated. (2) Where a contract of sale is not severable and the buyer has accepted the goods or part thereof, the breach of any condition... can only be treated as a breach of warranty... unless there is a term of the contract, express or implied, to that effect.",
            "simplified_explanation": "Clarifies that if a buyer accepts goods or continues using them after discovering a defect, the law treats the breach of condition as a breach of warranty, restricting the buyer to claiming damages rather than rejecting the goods.",
            "legal_ingredients": [
                "Buyer accepted goods or part thereof in non-severable contract",
                "Buyer waiver of condition",
                "Remedy converted from rejection of goods to action for damages"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "condition_vs_warranty_breach_sale_of_goods",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Damages in diminution of price under Section 59.",
            "related_provisions": [
                "Sale of Goods Act 1930 Section 12",
                "Sale of Goods Act 1930 Section 59"
            ],
            "exceptions_and_limitations": [
                "Acceptance does not occur if buyer was not given a reasonable opportunity to examine goods under Section 41."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Warns commercial buyers that using defective goods for months prevents them from demanding a total return.",
            "keywords": [
                "condition treated as warranty",
                "waiver of condition",
                "accepted goods",
                "diminution of price",
                "section 13 sale of goods act"
            ],
            "citation": "Section 13, Sale of Goods Act, 1930",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "14": {
            "section_number": "14",
            "official_section_title": "Implied undertaking as to title, etc.",
            "official_text": "In a contract of sale, unless the circumstances of the contract are such as to show a different intention, there is— (a) an implied condition on the part of the seller that, in the case of a sale, he has a right to sell the goods... and (b) an implied warranty that the buyer shall have and enjoy quiet possession of the goods; (c) an implied warranty that the goods shall be free from any charge or encumbrance in favour of any third party not declared or known to the buyer.",
            "simplified_explanation": "Guarantees an automatic implied condition that the seller is the legal owner with the right to sell, and an implied warranty that the goods are free from undisclosed third-party loans, hypothecation, or legal claims.",
            "legal_ingredients": [
                "Contract of sale of goods",
                "Statutory implied condition that seller has lawful title to sell",
                "Implied warranty of quiet possession and freedom from third-party charges"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "condition_vs_warranty_breach_sale_of_goods",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Repudiation of sale and full refund if seller had no title (Rowland v. Divall); damages for third party encumbrance.",
            "related_provisions": [
                "Sale of Goods Act 1930 Section 12",
                "BNS 2023 Section 317"
            ],
            "exceptions_and_limitations": [
                "Excludes sales where seller purports to sell only such title as he or a third person may have."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Protects buyers who unwittingly buy stolen goods, hypothecated vehicles, or goods with bank liens.",
            "keywords": [
                "implied title condition",
                "right to sell",
                "quiet possession warranty",
                "freedom from encumbrance",
                "stolen goods sale void"
            ],
            "citation": "Section 14, Sale of Goods Act, 1930",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "15": {
            "section_number": "15",
            "official_section_title": "Sale by description",
            "official_text": "Where there is a contract for the sale of goods by description, there is an implied condition that the goods shall correspond with the description; and, if the sale is by sample as well as by description, it is not sufficient that the bulk of the goods corresponds with the sample if the goods do not also correspond with the description.",
            "simplified_explanation": "Mandates that when goods are sold by description (e.g. online catalog, technical specification, grade of steel/fabric), the delivered goods MUST correspond strictly with that description. If they differ, the buyer has the legal right to reject them.",
            "legal_ingredients": [
                "Sale of goods by description or specification",
                "Delivered goods fail to correspond with the agreed description",
                "Breach of statutory implied condition"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "condition_vs_warranty_breach_sale_of_goods",
                "breach_of_contract",
                "e_commerce_refusal_of_open_box_delivery"
            ],
            "punishment_or_remedy": "Right to reject delivered goods and claim complete refund of purchase price plus damages.",
            "related_provisions": [
                "Sale of Goods Act 1930 Section 12",
                "Sale of Goods Act 1930 Section 16"
            ],
            "exceptions_and_limitations": [
                "De minimis non curat lex: microscopic deviations that do not affect utility or commercial description are disregarded."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Foundation of commercial quality enforcement; seller cannot deliver a different brand, model, or grade than specified.",
            "keywords": [
                "sale by description",
                "goods must correspond with description",
                "catalog specification breach",
                "right to reject wrong goods",
                "section 15 sale of goods act"
            ],
            "citation": "Section 15, Sale of Goods Act, 1930",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "17": {
            "section_number": "17",
            "official_section_title": "Sale by sample",
            "official_text": "(1) A contract of sale is a contract for sale by sample where there is a term in the contract, express or implied, to that effect. (2) In the case of a contract for sale by sample there is an implied condition— (a) that the bulk shall correspond with the sample in quality; (b) that the buyer shall have a reasonable opportunity of comparing the bulk with the sample; (c) that the goods shall be free from any defect, rendering them unmerchantable, which would not be apparent on reasonable examination of the sample.",
            "simplified_explanation": "Requires that when goods are ordered based on a sample, the bulk shipment must match the sample's quality, the buyer must be allowed to inspect and compare, and goods must be free from latent defects that ordinary examination would not reveal.",
            "legal_ingredients": [
                "Contract of sale by sample",
                "Bulk shipment must correspond with sample in quality",
                "Mandatory reasonable opportunity to inspect bulk against sample",
                "Freedom from latent unmerchantable defects"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "condition_vs_warranty_breach_sale_of_goods",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Right to reject entire consignment and recover payment with damages.",
            "related_provisions": [
                "Sale of Goods Act 1930 Section 15",
                "Sale of Goods Act 1930 Section 41"
            ],
            "exceptions_and_limitations": [
                "Patent defects that were obvious on simple inspection of sample are not protected."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Vital in wholesale textile, agricultural grain, and manufacturing raw material supply contracts.",
            "keywords": [
                "sale by sample",
                "bulk correspond with sample",
                "opportunity to inspect",
                "latent defect in sample",
                "section 17 sale of goods act"
            ],
            "citation": "Section 17, Sale of Goods Act, 1930",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "46": {
            "section_number": "46",
            "official_section_title": "Unpaid seller's rights",
            "official_text": "(1) Subject to the provisions of this Act and of any law for the time being in force, the unpaid seller of goods, as such, has by implication of law— (a) a lien on the goods for the price while he is in possession of them; (b) in case of the insolvency of the buyer, a right of stopping the goods in transit after he has parted with the possession of them; (c) a right of re-sale as limited by this Act.",
            "simplified_explanation": "Grants an unpaid commercial seller three strong statutory remedies if the buyer defaults on payment: the right to keep possession of goods under lien, the right to stop goods in transit if buyer is insolvent, and the right to resell the goods.",
            "legal_ingredients": [
                "Seller to whom whole of price has not been paid or tendered",
                "Possession of goods retained (lien), or goods in transit with carrier, or right of resale"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "unpaid_seller_lien_and_resale",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Lien on goods, stoppage in transit, and right of resale under Section 54.",
            "related_provisions": [
                "Sale of Goods Act 1930 Section 47",
                "Sale of Goods Act 1930 Section 50",
                "Sale of Goods Act 1930 Section 55"
            ],
            "exceptions_and_limitations": [
                "Lien is lost once seller delivers goods to carrier without reserving disposal rights or buyer lawfully obtains possession."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Essential commercial protection for wholesalers and manufacturers against defaulting corporate buyers.",
            "keywords": [
                "unpaid seller rights",
                "seller lien",
                "stoppage in transit",
                "right of resale",
                "section 46 sale of goods act"
            ],
            "citation": "Section 46, Sale of Goods Act, 1930",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "55": {
            "section_number": "55",
            "official_section_title": "Suit for price",
            "official_text": "(1) Where under a contract of sale the property in the goods has passed to the buyer and the buyer wrongfully neglects or refuses to pay for the goods according to the terms of the contract, the seller may sue him for the price of the goods. (2) Where under a contract of sale the price is payable on a day certain irrespective of delivery and the buyer wrongfully neglects or refuses to pay such price, the seller may sue him for the price although the property in the goods has not passed and the goods have not been appropriated to the contract.",
            "simplified_explanation": "Authorizes a seller to file a civil suit directly for the recovery of the full agreed price (plus interest) when ownership has passed to the buyer and the buyer wrongfully refuses to pay.",
            "legal_ingredients": [
                "Property in goods has passed to buyer, or payment due on date certain irrespective of delivery",
                "Buyer wrongfully neglects or refuses to pay agreed price"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "unpaid_seller_lien_and_resale",
                "breach_of_contract",
                "freelance_vendor_non_payment"
            ],
            "punishment_or_remedy": "Decree for full contract price plus statutory interest under Interest Act 1978.",
            "related_provisions": [
                "Sale of Goods Act 1930 Section 46",
                "Commercial Courts Act 2015 Section 12A",
                "Interest Act 1978 Section 3"
            ],
            "exceptions_and_limitations": [
                "Subject to 3-year limitation period under Article 55 of Limitation Act 1963."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Commercial & Civil Courts.",
            "applicability_notes": "Standard statutory basis for recovery of commercial supply invoice arrears.",
            "keywords": [
                "suit for price",
                "recovery of invoice amount",
                "unpaid supplier suit",
                "commercial goods payment",
                "section 55 sale of goods act"
            ],
            "citation": "Section 55, Sale of Goods Act, 1930",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "56": {
            "section_number": "56",
            "official_section_title": "Damages for non-acceptance",
            "official_text": "Where the buyer wrongfully neglects or refuses to accept and pay for the goods, the seller may sue him for damages for non-acceptance.",
            "simplified_explanation": "Gives the seller the right to sue the buyer for damages (market price difference, storage, and transport losses) if the buyer wrongfully cancels an order or refuses to accept delivery.",
            "legal_ingredients": [
                "Valid contract of sale",
                "Buyer wrongfully neglects or refuses to accept delivery and pay",
                "Seller suffered loss (difference between contract price and market price at date of breach)"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "unpaid_seller_lien_and_resale",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Damages representing difference between contract price and market price on date of breach.",
            "related_provisions": [
                "Sale of Goods Act 1930 Section 55",
                "Contract Act 1872 Section 73"
            ],
            "exceptions_and_limitations": [
                "Seller has a legal duty to mitigate damages by attempting resale in the open market."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central (Commercial & Civil Courts).",
            "applicability_notes": "Protects manufacturers against sudden client order cancellations after raw materials have been committed.",
            "keywords": [
                "damages for non acceptance",
                "wrongful order cancellation",
                "market price difference",
                "buyer breach",
                "section 56 sale of goods act"
            ],
            "citation": "Section 56, Sale of Goods Act, 1930",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "ni_act_1881": {
        "143": {
            "section_number": "143",
            "official_section_title": "Power of Court to try cases summarily",
            "official_text": "(1) Notwithstanding anything contained in the Code of Criminal Procedure, 1973, all offences under this Chapter shall be tried by a Judicial Magistrate of the first class or by a Metropolitan Magistrate and the provisions of sections 262 to 265 (both inclusive) of the said Code shall, as far as may be, apply to such trials... (3) Every trial under this section shall be conducted as expeditiously as possible and an endeavour shall be made to conclude the trial within six months from the date of filing of the complaint.",
            "simplified_explanation": "Directs that cheque bounce trials under Section 138 must be tried summarily by Magistrates and must be concluded expeditiously within six months from the date of complaint filing.",
            "legal_ingredients": [
                "Complaint filed under Section 138 NI Act",
                "Summary trial procedure under CrPC/BNSS",
                "Statutory mandate to conclude trial within six months"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "cheque_bounce_statutory_notice_138"
            ],
            "punishment_or_remedy": "Magistrate can pass sentence of imprisonment up to one year and fine exceeding five thousand rupees in summary trial.",
            "related_provisions": [
                "NI Act 1881 Section 138",
                "NI Act 1881 Section 143A",
                "NI Act 1881 Section 148"
            ],
            "exceptions_and_limitations": [
                "Magistrate may recall summary procedure and conduct regular summons trial if sentence of over one year may be warranted."
            ],
            "amendment_status": "In force; inserted by Act 55 of 2002.",
            "jurisdiction": "Judicial Magistrate First Class / Metropolitan Magistrate.",
            "applicability_notes": "Statutory priority standard enacted to prevent cheque bounce litigation from dragging on for decades.",
            "keywords": [
                "summary trial cheque bounce",
                "six months trial conclusion",
                "section 143 ni act",
                "fast track cheque trial",
                "magistrate summary trial"
            ],
            "citation": "Section 143, Negotiable Instruments Act, 1881",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "148": {
            "section_number": "148",
            "official_section_title": "Power of Appellate Court to order deposit",
            "official_text": "(1) Notwithstanding anything contained in the Code of Criminal Procedure, 1973, in an appeal by the drawer against conviction under section 138, the Appellate Court may order the appellant to deposit such sum which shall be a minimum of twenty per cent. of the fine or compensation awarded by the trial Court... (2) The amount referred to in sub-section (1) shall be deposited within sixty days from the date of the order, or within such further period not exceeding thirty days as may be directed by the Court on sufficient cause being shown.",
            "simplified_explanation": "Empowers Sessions Courts and High Courts hearing an appeal by a convicted cheque defaulter to order mandatory deposit of a minimum of 20% of the compensation awarded by the trial court within 60 days, which can be released to the complainant.",
            "legal_ingredients": [
                "Appeal filed by drawer convicted under Section 138",
                "Appellate Court power to order deposit of minimum 20% of fine/compensation",
                "Deposit mandatory within 60 days (extendable by 30 days max)"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "cheque_bounce_statutory_notice_138"
            ],
            "punishment_or_remedy": "Mandatory 20% minimum pre-deposit secures interim recovery for complainant; stay vacated on non-deposit.",
            "related_provisions": [
                "NI Act 1881 Section 138",
                "NI Act 1881 Section 143A"
            ],
            "exceptions_and_limitations": [
                "Supreme Court in Surinder Singh Deswal v. Virender Gandhi held that the word 'may' is generally interpreted as mandatory unless exceptional circumstances exist."
            ],
            "amendment_status": "In force; inserted by Negotiable Instruments (Amendment) Act, 2018.",
            "jurisdiction": "Sessions Courts & High Courts.",
            "applicability_notes": "Stops convicted cheque defaulters from staying sentences without paying any compensation to the victim.",
            "keywords": [
                "20 percent deposit in appeal",
                "section 148 ni act",
                "cheque bounce appeal deposit",
                "surinder singh deswal",
                "interim compensation release"
            ],
            "citation": "Section 148, Negotiable Instruments Act, 1881",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "tp_act_1882": {
        "53A": {
            "section_number": "53A",
            "official_section_title": "Part performance",
            "official_text": "Where any person contracts to transfer for consideration any immoveable property by writing signed by him or on his behalf from which the terms necessary to constitute the transfer can be ascertained with reasonable certainty, and the transferee has, in part performance of the contract, taken possession of the property or any part thereof... and the transferee has performed or is willing to perform his part of the contract, then, notwithstanding that where there is an instrument of transfer, that the transfer has not been completed in the manner prescribed therefor by the law for the time being in force, the transferor or any person claiming under him shall be debarred from enforcing against the transferee and persons claiming under him any right in respect of the property of which the transferee has taken or continued in possession, other than a right expressly provided by the terms of the contract.",
            "simplified_explanation": "Protects a buyer who paid consideration and took physical possession under a written property agreement: the seller cannot arbitrarily evict the buyer or sell the property to someone else, even if the formal sale deed has not yet been executed.",
            "legal_ingredients": [
                "Contract to transfer immovable property for consideration in writing signed by transferor",
                "Transferee has taken physical possession in part performance of contract",
                "Transferee has performed or is ready and willing to perform his part",
                "Statutory debarment of transferor from evicting transferee"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "part_performance_possession_protection",
                "unregistered_lease_immovable_property_dispute",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Equitable defense debarring transferor from dispossessing or evicting transferee in possession.",
            "related_provisions": [
                "Transfer of Property Act 1882 Section 54",
                "Registration Act 1908 Section 17",
                "Registration Act 1908 Section 49"
            ],
            "exceptions_and_limitations": [
                "Following the 2001 Registration Amendment, Section 53A protection requires the agreement to be registered to defend possession against third parties."
            ],
            "amendment_status": "In force; amended by Act 48 of 2001.",
            "jurisdiction": "Central (Civil Courts).",
            "applicability_notes": "Fundamental doctrine of part performance protecting bona fide purchasers in possession.",
            "keywords": [
                "part performance",
                "section 53a tpa",
                "possession protection",
                "agreement to sell possession",
                "shield not a sword"
            ],
            "citation": "Section 53A, Transfer of Property Act, 1882",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "54": {
            "section_number": "54",
            "official_section_title": "Sale defined",
            "official_text": "\"Sale\" is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised. Sale how made.—Such transfer, in the case of tangible immoveable property of the value of one hundred rupees and upwards, or in the case of a reversion or other intangible thing, can be made only by a registered instrument... Contract for sale.—A contract for the sale of immoveable property is a contract that a sale of such property shall take place on terms settled between the parties. It does not, of itself, create any interest in or charge on such property.",
            "simplified_explanation": "Defines sale of immovable property and establishes that sale of property worth Rs 100 or more can ONLY be legally effected by a registered sale deed. A mere agreement to sell does not transfer title until formal registration.",
            "legal_ingredients": [
                "Transfer of ownership in immovable property in exchange for price",
                "Statutory requirement: mandatory registered instrument for property value >= Rs 100",
                "Contract for sale does not itself create proprietary title"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "unregistered_lease_immovable_property_dispute",
                "part_performance_possession_protection",
                "specific_performance_readiness_willingness_dispute"
            ],
            "punishment_or_remedy": "Unregistered transfer cannot convey legal title (Suraj Lamp & Industries v. State of Haryana).",
            "related_provisions": [
                "Transfer of Property Act 1882 Section 53A",
                "Registration Act 1908 Section 17",
                "Registration Act 1908 Section 49"
            ],
            "exceptions_and_limitations": [
                "GPA/SA/Will transfers do not convey title under Suraj Lamp ruling; registered conveyance deed mandatory."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central.",
            "applicability_notes": "Statutory foundation of Indian property conveyancing law.",
            "keywords": [
                "sale defined",
                "registered sale deed mandatory",
                "contract for sale",
                "suraj lamp ruling",
                "section 54 tpa"
            ],
            "citation": "Section 54, Transfer of Property Act, 1882",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "107": {
            "section_number": "107",
            "official_section_title": "Leases how made",
            "official_text": "A lease of immoveable property from year to year, or for any term exceeding one year or reserving a yearly rent, can be made only by a registered instrument. All other leases of immoveable property may be made either by a registered instrument or by oral agreement accompanied by delivery of possession.",
            "simplified_explanation": "Mandates that any lease or rental agreement for immovable property exceeding one year (exceeding 11 months) must be executed by a registered instrument, while leases of 11 months or less may be made without registration.",
            "legal_ingredients": [
                "Lease of immovable property exceeding one year or reserving yearly rent",
                "Statutory requirement: mandatory registered instrument",
                "Leases for 11 months or less exempt from compulsory central registration"
            ],
            "domain": "contractual_disputes",
            "relevant_issues": [
                "unregistered_lease_immovable_property_dispute",
                "commercial_lease_security_deposit_withholding",
                "breach_of_contract"
            ],
            "punishment_or_remedy": "Unregistered lease exceeding one year creates only a month-to-month tenancy terminable by 15-day notice under Section 106.",
            "related_provisions": [
                "Transfer of Property Act 1882 Section 105",
                "Transfer of Property Act 1882 Section 106",
                "Registration Act 1908 Section 17"
            ],
            "exceptions_and_limitations": [
                "Certain states (e.g. Maharashtra Rent Control Act) mandate registration of all leave and license agreements regardless of duration."
            ],
            "amendment_status": "In force.",
            "jurisdiction": "Central & State.",
            "applicability_notes": "Origin of the ubiquitous '11-month rental agreement' practice in Indian real estate.",
            "keywords": [
                "leases how made",
                "11 month rental agreement",
                "lease registration exceeding one year",
                "month to month tenancy",
                "section 107 tpa"
            ],
            "citation": "Section 107, Transfer of Property Act, 1882",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "bns_2023": {
        "317": {
            "section_number": "317",
            "official_section_title": "Stolen property",
            "official_text": "(1) Property, the possession whereof has been transferred by theft, or by extortion, or by robbery, and property which has been criminally misappropriated or in respect of which criminal breach of trust has been committed, is designated as \"stolen property\"... (2) Whoever dishonestly receives or retains any stolen property, knowing or having reason to believe the same to be stolen property, shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.",
            "simplified_explanation": "Penalizes anyone who knowingly receives or holds stolen funds or property—including 'cyber mule' bank account holders and UPI account renters who allow fraudulent money to pass through their accounts—with imprisonment up to 3 years, fine, or both.",
            "legal_ingredients": [
                "Property transferred through cyber fraud, cheating, theft, or extortion",
                "Dishonest receipt or retention of stolen funds/property",
                "Knowledge or reason to believe funds were illicitly obtained"
            ],
            "domain": "cyber_fraud",
            "relevant_issues": [
                "cyber_mule_account_money_laundering",
                "bank_account_freeze_mule_involvement",
                "otp_fraud"
            ],
            "punishment_or_remedy": "Imprisonment of either description up to three years, or fine, or both; freezing and attachment of bank account under BNSS Section 107.",
            "related_provisions": [
                "BNS 2023 Section 318",
                "BNSS 2023 Section 107",
                "PMLA 2002 Section 3"
            ],
            "exceptions_and_limitations": [
                "Innocent account holders whose credentials were hacked without their knowledge are not liable under Section 317 for lack of mens rea."
            ],
            "amendment_status": "In force; commenced on 1st July 2024 (replacing IPC Section 411).",
            "jurisdiction": "Central (Criminal Courts).",
            "applicability_notes": "Primary substantive penal provision applied by cyber police against mule account syndicates and commission agents.",
            "keywords": [
                "stolen property",
                "cyber mule account",
                "receiving fraudulent money",
                "three years imprisonment",
                "section 317 bns"
            ],
            "citation": "Section 317, Bharatiya Nyaya Sanhita, 2023",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "337": {
            "section_number": "337",
            "official_section_title": "Forgery of record of Court or of public register, etc.",
            "official_text": "Whoever forges a document or an electronic record, purporting to be a record or proceeding of or in a Court of Justice, or a register of birth, baptism, marriage or burial, or a register kept by a public servant in his official capacity, or a certificate or document purporting to be made by a public servant in his official capacity... shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
            "simplified_explanation": "Imposes severe punishment—imprisonment up to 7 years and fine—for forging government records, court orders, fake police notices, fake RTO driving licences, or fraudulent official challan slips.",
            "legal_ingredients": [
                "Forgery of document or electronic record",
                "Document purports to be court record, public register, police notice, or official certificate",
                "Intent to cause damage or defraud"
            ],
            "domain": "cyber_fraud",
            "relevant_issues": [
                "digital_arrest_extortion",
                "fake_traffic_challan_apk_scam",
                "wrongful_challan"
            ],
            "punishment_or_remedy": "Imprisonment of either description up to seven years, and fine.",
            "related_provisions": [
                "BNS 2023 Section 336",
                "BNS 2023 Section 318",
                "IT Act 2000 Section 66D"
            ],
            "exceptions_and_limitations": [
                "Cognizable and non-bailable offence."
            ],
            "amendment_status": "In force; commenced on 1st July 2024 (replacing IPC Section 466).",
            "jurisdiction": "Central.",
            "applicability_notes": "Applies directly to cyber extortionists sending fake CBI/Customs warrants and fake traffic challan APK links.",
            "keywords": [
                "forgery of public record",
                "fake police notice",
                "fake court warrant",
                "seven years jail",
                "section 337 bns"
            ],
            "citation": "Section 337, Bharatiya Nyaya Sanhita, 2023",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    },
    "bnss_2023": {
        "94": {
            "section_number": "94",
            "official_section_title": "Summons to produce document or other thing",
            "official_text": "(1) Whenever any Court or any officer in charge of a police station considers that the production of any document or other thing is necessary or desirable for the purposes of any investigation, inquiry, trial or other proceeding under this Sanhita by or before such Court or officer, such Court may issue a summons, or such officer a written order, to the person in whose possession or power such document or thing is believed to be, requiring him to attend and produce it, or to produce it, at the time and place stated in the summons or order.",
            "simplified_explanation": "Empowers investigating police officers and courts to issue formal statutory summons to banks, telecom operators, and crypto exchanges to immediately produce server logs, account statements, CCTV footage, and digital records.",
            "legal_ingredients": [
                "Necessity or desirability for investigation, inquiry, or trial",
                "Written summons issued by Court or order by Station House Officer (SHO)",
                "Document, server log, or electronic device in possession of recipient"
            ],
            "domain": "cyber_fraud",
            "relevant_issues": [
                "cyber_digital_evidence_admissibility",
                "otp_fraud",
                "cyber_mule_account_money_laundering"
            ],
            "punishment_or_remedy": "Failure to comply punishable under BNS Section 223 / IPC Section 175; search warrant under Section 96.",
            "related_provisions": [
                "BNSS 2023 Section 107",
                "BSA 2023 Section 63",
                "IT Act 2000 Section 69"
            ],
            "exceptions_and_limitations": [
                "Does not affect Sections 123 and 124 of Evidence Act / BSA provisions regarding state secrets."
            ],
            "amendment_status": "In force; commenced on 1st July 2024 (replacing CrPC Section 91).",
            "jurisdiction": "Central (Police Officers & Criminal Courts across India).",
            "applicability_notes": "The primary statutory tool used by Cyber Crime Cells to requisition IP logs, CDRs, and bank transfer trails.",
            "keywords": [
                "summons to produce document",
                "section 94 bnss",
                "police requisition bank logs",
                "call detail records summons",
                "crpc 91 replacement"
            ],
            "citation": "Section 94, Bharatiya Nagarik Suraksha Sanhita, 2023",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        },
        "107": {
            "section_number": "107",
            "official_section_title": "Attachment, forfeiture or restoration of property",
            "official_text": "(1) Where a police officer making an investigation has reason to believe that any property is derived or obtained, directly or indirectly, as a result of a criminal activity or from the commission of any offence, he may, with the prior approval in writing of the Superintendent of Police or Commissioner of Police, make an application to the Court having jurisdiction to take cognizance of the offence for attachment of such property... (6) Where the Court finds that the property attached is derived or obtained from criminal activity, the Court may pass an order to forfeit the property to the State Government or distribute it to the victim of the offence.",
            "simplified_explanation": "Authorizes police and Magistrate Courts to formally freeze, attach, and forfeit fraudulent bank accounts and cyber crime proceeds, with a landmark provision empowering the Court to distribute the seized funds directly back to the victim.",
            "legal_ingredients": [
                "Property derived or obtained as result of criminal activity or cyber offence",
                "Prior written approval of Superintendent of Police (SP) or Police Commissioner",
                "Court order of attachment and distribution to victim"
            ],
            "domain": "cyber_fraud",
            "relevant_issues": [
                "cyber_mule_account_money_laundering",
                "otp_fraud",
                "bank_account_freeze_mule_involvement"
            ],
            "punishment_or_remedy": "Judicial attachment and direct refund of frozen money to the victim.",
            "related_provisions": [
                "BNSS 2023 Section 94",
                "BNS 2023 Section 317",
                "PMLA 2002 Section 5"
            ],
            "exceptions_and_limitations": [
                "Court must issue show-cause notice of 14 days to the affected account holder before final forfeiture."
            ],
            "amendment_status": "In force; transformative victim-compensation power introduced in BNSS 2023 (replacing CrPC S. 102).",
            "jurisdiction": "Criminal Courts across India.",
            "applicability_notes": "Statutory game-changer for cyber victims; allows Magistrate to release frozen mule account funds directly back to the defrauded citizen.",
            "keywords": [
                "attachment of property",
                "refund to victim",
                "freezing cyber fraud account",
                "distribute money to victim",
                "section 107 bnss"
            ],
            "citation": "Section 107, Bharatiya Nagarik Suraksha Sanhita, 2023",
            "provision_status": "in_force",
            "verification": {"status": "pending_manual_verification"}
        }
    }
}

