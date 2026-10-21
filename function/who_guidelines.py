"""
VenomGuard - WHO Snakebite Emergency First Aid and Clinical Triage Engine
Compliant with World Health Organization (WHO) Guidelines for the Clinical Management
of Snakebite in Africa, Asia, and Latin America.

Provides verified first-aid guidance and syndromic triage rules.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class FirstAidProtocol:
    snake_name: str
    danger_category: str
    immediate_dos: List[str]
    critical_donts: List[str]
    syndromic_effects: List[str]
    evacuation_advice: str
    emergency_numbers: Dict[str, str] = field(default_factory=lambda: {
        "Global / GSM Standard": "112",
        "India": "112 / 108",
        "United States & Canada": "911",
        "United Kingdom": "999",
        "Australia": "000",
        "Japan": "119",
        "South Africa": "112 / 10177",
        "Kenya": "999 / 112",
        "Brazil": "192 (SAMU)",
    })

    def to_markdown(self) -> str:
        dos_md = "\n".join([f"- **DO:** {item}" for item in self.immediate_dos])
        donts_md = "\n".join([f"- **DO NOT:** {item}" for item in self.critical_donts])
        symptoms_md = "\n".join([f"- {item}" for item in self.syndromic_effects])

        return f"""
### Emergency First Aid (WHO Protocol)

**Target Snake:** {self.snake_name}  
**Classification:** {self.danger_category}

---

#### Actions to take immediately (DO):
{dos_md}

---

#### Practices to avoid (DO NOT):
{donts_md}

---

#### Clinical signs to monitor:
{symptoms_md}

---

#### Hospital Transport Guidance:
{self.evacuation_advice}
"""


WHO_UNIVERSAL_DOS = [
    "**Keep the victim completely calm and still**: Physical movement and exertion accelerate venom absorption into the bloodstream and lymphatic vessels.",
    "**Immobilize the bitten limb**: Splint the affected arm or leg to prevent joint movement, and apply a broad crepe bandage at comfortable tension (snug, as for a sprained ankle, without cutting off arterial circulation). Keep the limb at or slightly below heart level.",
    "**Remove constricting jewelry and clothing immediately**: Take off rings, bracelets, watches, and tight footwear before localized swelling expands.",
    "**Clean the wound gently**: If clean water is available, gently rinse the bite site. Do not scrub, rub, or manipulate puncture holes.",
    "**Record time and track symptoms**: Record the exact time of the bite. Mark the advancing border of swelling on the skin with a pen every 15 minutes to assist attending clinicians.",
    "**Safely observe or photograph the snake**: If safe, photograph the snake from a distance of at least 2 meters. Never attempt to capture, corner, or kill the snake.",
    "**Arrange immediate hospital transport**: Transport the patient recumbent (lying down) on a stretcher or vehicle to a hospital equipped with antivenom and airway support."
]

WHO_UNIVERSAL_DONTS = [
    "**DO NOT apply a tight arterial tourniquet**: Arterial tourniquets cut off blood flow, causing tissue ischemia, gangrene, and limb amputation. Removing a tourniquet abruptly releases accumulated venom and toxins into the circulation, precipitating shock.",
    "**DO NOT cut or incise the bite wound**: Cutting with knives or razor blades severs nerves and tendons, aggravates bleeding, and introduces severe bacterial infections.",
    "**DO NOT attempt to suck out the venom**: Suction removes negligible venom and introduces oral bacteria deep into compromised tissue. Mechanical suction extractors are equally ineffective.",
    "**DO NOT apply ice or cold packs**: Ice exacerbates local tissue necrosis and causes frostbite injury.",
    "**DO NOT administer traditional remedies or electric shocks**: Herbal preparations, black stones, and shocks are ineffective and delay hospital evaluation.",
    "**DO NOT give alcohol, pain relievers like aspirin, or stimulants**: Aspirin exacerbates bleeding from hemotoxic venoms, and alcohol impairs neurological monitoring."
]


def classify_venom_syndrome(snake_name: str, toxicity_text: str = "") -> Dict[str, Any]:
    name = (snake_name or "").lower()
    tox = (toxicity_text or "").lower()

    # Neurotoxic syndrome
    if any(k in name for k in ["cobra", "krait", "mamba", "taipan", "coral snake", "sea snake"]):
        return {
            "syndrome": "Neurotoxic Envenomation",
            "symptoms": [
                "Bilateral ptosis (drooping eyelids): early indicator of neurotoxicity",
                "Diplopia (double vision) and difficulty swallowing or speaking",
                "Descending symmetrical limb weakness",
                "Respiratory muscle impairment and dyspnea (urgent clinical risk)",
                "Excessive salivation and perspiration"
            ],
            "priority": "CRITICAL EMERGENCY: Risk of rapid respiratory arrest within 30 to 180 minutes."
        }

    # Hemotoxic / Cytotoxic syndrome (Vipers, Adders, Pit Vipers)
    if any(k in name for k in ["viper", "adder", "rattlesnake", "copperhead", "cottonmouth", "lancehead", "bushmaster"]):
        return {
            "syndrome": "Hemotoxic / Cytotoxic (Vasculotoxic) Envenomation",
            "symptoms": [
                "Severe local pain and expanding edema around the bite site",
                "Spontaneous systemic bleeding from bite punctures, gums, or epistaxis",
                "Ecchymosis (bruising) and formation of blood blisters",
                "Hypotension, dizziness, or syncope",
                "Local tissue necrosis requiring wound care monitoring"
            ],
            "priority": "HIGH EMERGENCY: Risk of coagulopathy, extensive tissue necrosis, and acute kidney injury."
        }

    # Default / Unknown venomous
    if "venomous" in tox and "non-venomous" not in tox:
        return {
            "syndrome": "Potentially Severe Envenomation",
            "symptoms": [
                "Progressive pain, erythema, and swelling extending up the bitten limb",
                "Nausea, diaphoresis, or abdominal discomfort",
                "Persistent bleeding or oozing from puncture wounds",
                "Weakness, paresthesias, or breathing difficulty"
            ],
            "priority": "HIGH EMERGENCY: Hospital observation and serial coagulation monitoring required."
        }

    # Non-venomous
    return {
        "syndrome": "Non-Venomous Bite (Low Systemic Risk)",
        "symptoms": [
            "Superficial scratches or punctures without spreading edema",
            "Localized tenderness or erythema",
            "Absence of ptosis, abnormal bleeding, or systemic symptoms",
            "Risk of secondary bacterial wound infection or tetanus"
        ],
        "priority": "STANDARD MEDICAL CARE: Cleanse wound thoroughly with soap and water, apply antiseptic, and verify tetanus prophylaxis."
    }


def get_who_protocol(snake_name: str, toxicity_text: str = "") -> FirstAidProtocol:
    syndrome_info = classify_venom_syndrome(snake_name, toxicity_text)
    is_non_venomous = "non-venomous" in (toxicity_text or "").lower() or syndrome_info["syndrome"].startswith("Non-Venomous")

    danger_cat = "Harmless / Mild" if is_non_venomous else "Hazardous - Antivenom Evaluation Mandatory"

    evac_advice = (
        "Although antivenom is not indicated for non-venomous bites, visit a healthcare center "
        "for antiseptic wound cleaning and tetanus assessment."
        if is_non_venomous
        else (
            f"URGENT: {syndrome_info['priority']} Transport the patient recumbent and immobilized "
            "directly to an emergency facility equipped with antivenom and supportive mechanical ventilation."
        )
    )

    return FirstAidProtocol(
        snake_name=snake_name,
        danger_category=danger_cat,
        immediate_dos=WHO_UNIVERSAL_DOS,
        critical_donts=WHO_UNIVERSAL_DONTS,
        syndromic_effects=syndrome_info["symptoms"],
        evacuation_advice=evac_advice
    )
