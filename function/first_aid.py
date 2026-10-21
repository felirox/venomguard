"""
VenomGuard - First Aid Guidance & Emergency Dispatch Orchestrator
Coordinates clinical triage protocols, nearby medical facility lookups,
and conversational AI guidance with complete offline resilience.
"""

import logging
import os
from typing import List, Optional, Tuple, Union

from dotenv import load_dotenv
from function.location import get_nearby_hospitals
from function.who_guidelines import get_who_protocol

load_dotenv()
logger = logging.getLogger("venomguard.firstaid")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def generate_llm_first_aid(snake_type: str, location_hint: str = "") -> Optional[str]:
    """
    Attempts to generate personalized first-aid guidance via OpenAI API.
    Compatible with both modern openai>=1.0.0 and legacy openai<1.0.0.
    """
    if not OPENAI_API_KEY or OPENAI_API_KEY.strip() in ("", "ENTER_YOUR_API_KEY"):
        return None

    sys_prompt = f"""You are VenomGuard's emergency medical assistant, adhering strictly to World Health Organization (WHO) snakebite envenoming protocols.
The user reports a bite from or encounter with: {snake_type}. Location context: {location_hint or 'Unknown'}.

Provide immediate, high-priority, calm emergency guidance:
1. Universal DOs: Keep victim still, calm, immobilize bitten limb with a broad bandage below heart level, remove constrictive jewelry/clothing.
2. Lethal DON'Ts: DO NOT apply tourniquets, DO NOT cut, DO NOT suck venom, DO NOT apply ice or folk herbs.
3. Specific symptoms to monitor for {snake_type}.
4. Direct urgent advice to proceed to the nearest emergency medical facility immediately."""

    # Try modern openai client (openai>=1.0.0)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a professional emergency medical first-aid AI."},
                {"role": "user", "content": sys_prompt}
            ],
            timeout=10
        )
        return response.choices[0].message.content
    except ImportError:
        pass
    except Exception as exc:
        logger.warning("Modern OpenAI API call failed: %s", exc)

    # Try legacy openai (openai<1.0.0)
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[{"role": "system", "content": sys_prompt}],
            request_timeout=10
        )
        return response["choices"][0]["message"]["content"]
    except Exception as exc:
        logger.warning("Legacy OpenAI API call failed: %s", exc)

    return None


def tell_first_aid(snake_type: str, location: Optional[Tuple[float, float]] = None) -> Tuple[str, List[str]]:
    """
    Generates emergency first aid advice and retrieves a list of nearby hospitals.
    Falls back reliably to verified offline WHO protocols when APIs are unavailable.
    """
    logger.info("Generating first aid guidance for '%s' at location %s", snake_type, location)

    # 1. Retrieve nearby hospitals
    raw_hospitals = get_nearby_hospitals(location)
    hospitals_formatted = []
    for h in raw_hospitals:
        name = h.get("name", "Hospital")
        addr = h.get("address", "")
        url = h.get("url", "")
        if url:
            hospitals_formatted.append(f"[{name}]({url}) - {addr}")
        else:
            hospitals_formatted.append(f"{name} - {addr}")

    if not hospitals_formatted:
        hospitals_formatted = [
            "Regional Government / Emergency Hospital",
            "Please dial 112 (or local emergency dispatcher) for antivenom center routing."
        ]

    # 2. Try online LLM guidance if key exists
    llm_content = generate_llm_first_aid(snake_type, location_hint=str(location) if location else "")
    if llm_content:
        return llm_content, hospitals_formatted

    # 3. Offline WHO protocol fallback (fully verified, instant, zero cost)
    protocol = get_who_protocol(snake_type)
    return protocol.to_markdown(), hospitals_formatted
