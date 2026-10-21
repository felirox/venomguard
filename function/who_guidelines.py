"""
VenomGuard - WHO Snakebite Emergency First Aid & Clinical Triage Engine
Compliant with World Health Organization (WHO) Guidelines for the Clinical Management
of Snakebite in Africa, Asia, and Latin America.

Provides verified, life-saving first-aid instructions, dispels lethal folk myths,
and supplies syndromic triage recommendations that function completely offline.
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

#### 🟢 Immediate Actions to Take (DO):
{dos_md}

---

#### 🔴 Dangerous Practices to Avoid (DO NOT):
{donts_md}

---

#### 🩺 Expected Symptoms & Warning Signs:
{symptoms_md}

---

#### 🚑 Urgent Transport & Hospital Advice:
{self.evacuation_advice}
"""


# Standard WHO DOs and DONTs
WHO_UNIVERSAL_DOS = [
    "**Keep the victim calm and still**: Movement accelerates venom absorption into the bloodstream and lymphatic system.",
    "**Immobilize the bitten limb**: Splint the affected leg or arm and apply a broad crepe bandage at comfortable tension (like for a sprained ankle). Keep the limb at or slightly below heart level.",
    "**Remove constricting items immediately**: Take off rings, bracelets, watches, tight shoes, and restrictive garments before swelling develops.",
    "**Clean the wound gently**: If clean water is available, rinse the bite site very gently. Do not scrub or manipulate the puncture holes.",
    "**Record time and track symptoms**: Note the exact time of the bite. Mark the leading edge of swelling on the skin with a pen every 15 minutes.",
    "**Safely note snake characteristics**: If possible, photograph the snake from a safe distance (minimum 2 meters) or remember color patterns. NEVER attempt to catch, corner, or kill the snake.",
    "**Arrange immediate transport**: Transport the victim lying down on a stretcher or vehicle to a hospital capable of administering antivenom and supportive airway care."
]

WHO_UNIVERSAL_DONTS = [
    "**DO NOT apply a tight arterial tourniquet**: Arterial tourniquets cut off blood supply, leading to ischemia, gangrene, and amputation, while causing a fatal venom surge when released.",
    "**DO NOT cut or incise the bite wound**: Cutting lacerates nerves, tendons, and arteries, and introduces catastrophic secondary infection.",
    "**DO NOT attempt to suck out venom**: Mouth or mechanical suction devices are completely ineffective and expose the rescuer to venom while infecting the wound.",
    "**DO NOT apply ice, cold packs, or chemicals**: Extreme cold accelerates local tissue necrosis and causes frostbite over compromised tissue.",
    "**DO NOT administer traditional herbs, electrical shocks, or folk remedies**: These delay genuine hospital treatment and frequently cause fatal sepsis or kidney failure.",
    "**DO NOT give alcohol, aspirin, or stimulants**: Aspirin exacerbates hemotoxic bleeding, and alcohol impairs medical neurological assessment."
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
                "Bilateral ptosis (drooping eyelids) - earliest hallmark sign",
                "Diplopia (double vision) and difficulty swallowing or speaking",
                "Progressive descending muscle weakness and limb flaccidity",
                "Respiratory muscle paralysis leading to asphyxiation if untreated",
                "Excessive salivation and sweating"
            ],
            "priority": "CRITICAL EMERGENCY - Risk of rapid respiratory arrest within 30-180 minutes."
        }

    # Hemotoxic / Cytotoxic syndrome (Vipers, Adders, Pit Vipers)
    if any(k in name for k in ["viper", "adder", "rattlesnake", "copperhead", "cottonmouth", "lancehead", "bushmaster"]):
        return {
            "syndrome": "Hemotoxic / Cytotoxic (Vasculotoxic) Envenomation",
            "symptoms": [
                "Rapid severe local pain and expanding swelling around the bite site",
                "Spontaneous systemic bleeding (gums, nose, puncture sites, urine)",
                "Extensive bruising (ecchymosis) and blood-filled blistering (bullae)",
                "Coagulopathy and internal hemorrhage risk",
                "Tissue necrosis requiring wound debridement or surgical monitoring"
            ],
            "priority": "HIGH EMERGENCY - Risk of hypovolemic shock, massive tissue necrosis, and renal failure."
        }

    # Default / Unknown venomous
    if "venomous" in tox and "non-venomous" not in tox:
        return {
            "syndrome": "Potentially Severe Envenomation",
            "symptoms": [
                "Local pain, swelling, and redness progressing along the limb",
                "Nausea, dizziness, abdominal pain, or abnormal sweating",
                "Bleeding from bite punctures or systemic bleeding points",
                "Muscle weakness, numbness, or breathing difficulty"
            ],
            "priority": "HIGH EMERGENCY - Requires urgent medical triage and 24-hour observation."
        }

    # Non-venomous
    return {
        "syndrome": "Non-Venomous Bite (Low Systemic Risk)",
        "symptoms": [
            "Minor localized scratches or superficial puncture wounds",
            "Mild localized discomfort and erythema",
            "Minimal swelling without progressive spread",
            "Tetanus infection risk if wound care is neglected"
        ],
        "priority": "STANDARD MEDICAL CARE - Clean wound thoroughly, verify tetanus prophylaxis, monitor for bacterial infection."
    }


def get_who_protocol(snake_name: str, toxicity_text: str = "") -> FirstAidProtocol:
    """Generates an evidence-based WHO first-aid protocol."""
    syndrome_info = classify_venom_syndrome(snake_name, toxicity_text)
    is_non_venomous = "non-venomous" in (toxicity_text or "").lower() or syndrome_info["syndrome"].startswith("Non-Venomous")

    danger_cat = "Harmless / Mild" if is_non_venomous else "Hazardous - Antivenom Evaluation Mandatory"

    evac_advice = (
        "While non-venomous bites do not require antivenom, the patient should visit a local clinic "
        "for antiseptic wound cleaning and a tetanus vaccination booster."
        if is_non_venomous
        else (
            f"**URGENT**: {syndrome_info['priority']} Immediately dispatch or transport the patient to an emergency "
            "hospital equipped with intensive care support (ventilators) and antivenom stock. Keep patient horizontal and stationary during transit."
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
