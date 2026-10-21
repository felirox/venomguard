"""
VenomGuard - WHO Snakebite Emergency First Aid & Clinical Triage Engine
Compliant with World Health Organization (WHO) Guidelines for the Clinical Management
of Snakebite in Africa, Asia, and Latin America.

Written in natural, calm, plain-English emergency guidance that anyone can understand in seconds.
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
        donts_md = "\n".join([f"- ❌ **DO NOT:** {item}" for item in self.critical_donts])
        symptoms_md = "\n".join([f"- {item}" for item in self.syndromic_effects])

        return f"""
### 🚨 Immediate Life-Saving First Aid (WHO Protocol)

**Target Snake:** {self.snake_name}  
**Classification:** {self.danger_category}

---

#### 🟢 What to do right now (DO):
{dos_md}

---

#### 🔴 Dangerous myths to avoid (DO NOT):
{donts_md}

---

#### 🩺 Symptoms and warning signs to watch for:
{symptoms_md}

---

#### 🚑 Urgent Hospital Advice:
{self.evacuation_advice}
"""


# Standard WHO DOs and DONTs (in clear, natural, crisis-ready English)
WHO_UNIVERSAL_DOS = [
    "**Keep the victim completely calm and still**: Any physical movement or running makes the heart pump faster, which speeds up venom circulation.",
    "**Immobilize the bitten limb**: Splint the affected arm or leg so joints can't bend, and wrap a broad bandage firmly (snug like wrapping a sprained ankle, but not cutting off blood). Keep the limb at or slightly below heart level.",
    "**Remove constricting jewelry and clothing immediately**: Take off rings, bracelets, watches, and tight footwear before swelling begins—once swelling starts, rings can cut off circulation.",
    "**Clean the wound gently**: If clean water is available, gently rinse the bite area. Do not scrub or squeeze the puncture marks.",
    "**Track the time and watch symptoms**: Write down the exact time of the bite. Mark the border of any swelling on the skin with a pen every 15 minutes so doctors can see how fast it's spreading.",
    "**Safely remember or photograph the snake**: If safe, snap a photo from at least 2 meters away. NEVER try to catch, corner, or kill the snake.",
    "**Head straight to the hospital**: Carry the patient or drive them while keeping them lying down. Do not let them walk."
]

WHO_UNIVERSAL_DONTS = [
    "**DO NOT apply a tight arterial tourniquet**: Tourniquets cut off blood flow, causing gangrene and loss of the limb. When loosened, they cause a deadly rush of trapped venom straight to the heart and lungs.",
    "**DO NOT cut or slash the bite wound**: Cutting with knives or razor blades damages nerves, tendons, and arteries, causes severe bleeding, and leads to nasty infections.",
    "**DO NOT try to suck out the venom**: Sucking venom with your mouth or suction devices is a movie myth that doesn't work. It damages tissue and injects mouth bacteria directly into the wound.",
    "**DO NOT apply ice or cold packs**: Ice accelerates tissue death and causes frostbite over already damaged flesh.",
    "**DO NOT waste time on folk remedies or electric shocks**: Herbs, black stones, and shocks are ineffective and waste precious minutes needed for antivenom.",
    "**DO NOT give alcohol, pain relievers like aspirin, or caffeine**: Aspirin worsens bleeding from hemotoxic venoms, and alcohol clouds clinical evaluation."
]


def classify_venom_syndrome(snake_name: str, toxicity_text: str = "") -> Dict[str, Any]:
    """
    Identifies primary clinical syndromic profile based on snake nomenclature and database toxicity.
    """
    name = (snake_name or "").lower()
    tox = (toxicity_text or "").lower()

    # Neurotoxic syndrome
    if any(k in name for k in ["cobra", "krait", "mamba", "taipan", "coral snake", "sea snake"]):
        return {
            "syndrome": "Neurotoxic Envenomation",
            "symptoms": [
                "Heavy, drooping eyelids (ptosis) — often the very first sign",
                "Double vision and difficulty swallowing or speaking clearly",
                "Limb weakness and heavy feeling in arms or legs",
                "Shortness of breath and difficulty breathing (urgent danger)",
                "Excess saliva and sweating"
            ],
            "priority": "CRITICAL EMERGENCY — Risk of breathing paralysis within 30 to 180 minutes."
        }

    # Hemotoxic / Cytotoxic syndrome (Vipers, Adders, Pit Vipers)
    if any(k in name for k in ["viper", "adder", "rattlesnake", "copperhead", "cottonmouth", "lancehead", "bushmaster"]):
        return {
            "syndrome": "Hemotoxic / Cytotoxic (Vasculotoxic) Envenomation",
            "symptoms": [
                "Intense burning pain and rapidly spreading swelling around the bite",
                "Bleeding from bite marks, gums, nose, or urine that won't stop",
                "Dark purple bruising and blood blisters forming under the skin",
                "Feeling faint, dizzy, or light-headed",
                "Severe tissue swelling that can damage muscles if untreated"
            ],
            "priority": "HIGH EMERGENCY — Risk of internal bleeding, severe swelling, and kidney damage."
        }

    # Default / Unknown venomous
    if "venomous" in tox and "non-venomous" not in tox:
        return {
            "syndrome": "Potentially Severe Envenomation",
            "symptoms": [
                "Spreading pain, swelling, and redness moving up the limb",
                "Nausea, dizziness, cold sweat, or stomach cramps",
                "Persistent oozing of blood from the puncture marks",
                "Any numbness, tingling, or shortness of breath"
            ],
            "priority": "HIGH EMERGENCY — Requires hospital observation for at least 24 hours."
        }

    # Non-venomous
    return {
        "syndrome": "Non-Venomous Bite (Low Systemic Risk)",
        "symptoms": [
            "Shallow scratches or puncture marks without spreading swelling",
            "Mild localized stinging or redness",
            "No drooping eyes, no trouble breathing, no bleeding from gums",
            "Risk of ordinary bacterial wound infection or tetanus"
        ],
        "priority": "STANDARD MEDICAL CARE — Clean well with soap and water, apply antiseptic, and verify your tetanus booster."
    }


def get_who_protocol(snake_name: str, toxicity_text: str = "") -> FirstAidProtocol:
    """Generates an evidence-based WHO first-aid protocol."""
    syndrome_info = classify_venom_syndrome(snake_name, toxicity_text)
    is_non_venomous = "non-venomous" in (toxicity_text or "").lower() or syndrome_info["syndrome"].startswith("Non-Venomous")

    danger_cat = "Harmless / Mild" if is_non_venomous else "Hazardous - Antivenom Evaluation Mandatory"

    evac_advice = (
        "While this bite is non-venomous and doesn't require antivenom, please visit a local clinic "
        "to get the puncture wounds cleaned properly and check if you need a tetanus shot."
        if is_non_venomous
        else (
            f"**URGENT**: {syndrome_info['priority']} Head immediately to the nearest hospital equipped with "
            "antivenom and emergency airway support. Keep the patient completely still and lying down on the way."
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
