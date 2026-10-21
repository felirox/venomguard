"""
VenomGuard - Conversational AI and Emergency Medical Triage Companion
Plain-English, verified medical triage assistance for snakebite emergencies.
Supports modern OpenAI models with an intelligent, offline WHO-compliant
emergency fallback engine when API keys or network are unavailable.
"""

import logging
import os
from typing import List, Optional

from dotenv import load_dotenv

try:
    import streamlit as st
except ImportError:
    st = None

load_dotenv()
logger = logging.getLogger("venomguard.chat")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def get_offline_medical_response(user_query: str, snake_type: str = "Unknown Snake") -> str:
    """
    Intelligent offline emergency response engine based on WHO snakebite management protocols.
    Provides immediate, verified answers to common emergency queries without needing an API key.
    """
    q = user_query.lower()

    if any(k in q for k in ["tourniquet", "tie", "rope", "tight", "band"]):
        return (
            "DO NOT APPLY A TOURNIQUET under any circumstances.\n\n"
            "Arterial tourniquets cut off arterial blood supply, rapidly causing tissue ischemia, gangrene, and limb amputation. "
            "Furthermore, when a tourniquet is subsequently loosened at a medical facility, the sudden bolus of accumulated "
            "venom and metabolic toxins released into the circulation can trigger cardiovascular collapse and shock.\n\n"
            "What to do instead: Apply a broad crepe bandage over the entire limb (firm and snug, as for a sprained ankle, "
            "without impeding arterial pulses), immobilize the limb with a rigid splint to prevent joint flexion, "
            "and keep the limb resting at or slightly below heart level."
        )

    if any(k in q for k in ["suck", "mouth", "cut", "razor", "blade", "incision"]):
        return (
            "NEVER CUT THE WOUND OR ATTEMPT TO SUCK out venom.\n\n"
            "Clinical evaluations show that suction extracts less than 1% of injected venom. Incising the bite wound lacerates "
            "nerves, tendons, and blood vessels, accelerating bleeding. Oral suction introduces oral bacteria deep into the wound, "
            "causing severe secondary infections and tissue destruction. Commercial suction devices are similarly ineffective."
        )

    if any(k in q for k in ["ice", "cold", "freeze", "pack"]):
        return (
            "DO NOT APPLY ICE or cold packs.\n\n"
            "Freezing temperatures accelerate local tissue necrosis, compound microvascular spasm, and produce cold-induced "
            "frostbite in already compromised tissue. Keep the affected area at ambient temperature."
        )

    if any(k in q for k in ["antivenom", "antidote", "medicine", "pill", "injection"]):
        return (
            "Antivenom Information:\n\n"
            "1. Prescription Only: Real antivenom is administered exclusively in equipped hospitals intravenously under direct "
            "physician supervision. Because antivenom can provoke anaphylactic shock, clinicians must have resuscitation medications ready.\n"
            "2. Specificity: Antivenoms are chosen based on the indigenous snake fauna of the incident area.\n"
            "3. Do not rely on oral remedies or unverified preparations: There are no effective oral antivenoms or over-the-counter snakebite pills."
        )

    if any(k in q for k in ["symptom", "sign", "feel", "look like", "effect"]):
        return (
            f"Clinical Signs to Monitor for {snake_type}:\n\n"
            "- Neurotoxic indicators: Bilateral ptosis (drooping eyelids), diplopia (double vision), dysphagia (difficulty swallowing), slurred speech, or shortness of breath.\n"
            "- Hemotoxic indicators: Persistent bleeding from bite punctures, spontaneous gingival bleeding, epistaxis, or abnormal bruising.\n"
            "- Local tissue effects: Rapidly expanding swelling, severe pain, or blister formation.\n\n"
            "Mark the border of expanding swelling on the skin with a pen every 15 minutes to help attending clinicians monitor progression."
        )

    if any(k in q for k in ["calm", "slow", "spread", "running", "walk"]):
        return (
            "How to Minimize Venom Absorption:\n\n"
            "- Absolute Physical Rest: The patient must remain recumbent and stationary. Do not permit walking or physical exertion.\n"
            "- Calm Reassurance: Anxiety elevates heart rate, accelerating lymphatic flow of venom into the systemic circulation.\n"
            "- Rigid Splinting: Immobilize the limb to prevent muscular contractions. Keep it positioned below the level of the heart."
        )

    return (
        f"Emergency Guidance for {snake_type} Encounter:\n\n"
        f"1. Immobilize: Keep the patient completely still. Splint the bitten limb below heart level.\n"
        f"2. Remove constriction: Take off rings, watches, and restrictive clothing immediately.\n"
        f"3. Avoid harmful actions: Do not cut, suck, apply ice, or use tourniquets.\n"
        f"4. Seek hospital evaluation: Transport the patient recumbent to an equipped medical center immediately. Dial 112 if dispatch is available."
    )


def query_llm_assistant(messages: List[dict], snake_type: str) -> str:
    if OPENAI_API_KEY and OPENAI_API_KEY.strip() not in ("", "ENTER_YOUR_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                temperature=0.2,
                messages=messages,
                timeout=12
            )
            return response.choices[0].message.content
        except ImportError:
            pass
        except Exception as exc:
            logger.warning("Modern OpenAI chat call failed: %s", exc)

        try:
            import openai
            openai.api_key = OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.2,
                messages=messages,
                request_timeout=12
            )
            return response["choices"][0]["message"]["content"]
        except Exception as exc:
            logger.warning("Legacy OpenAI chat call failed: %s", exc)

    last_user_query = messages[-1]["content"] if messages else ""
    return get_offline_medical_response(last_user_query, snake_type=snake_type)


def first_aid_chat(snake_type: str, first_aid: str, hospitals: List[str]):
    if st is None:
        raise RuntimeError("Streamlit is required to render first_aid_chat UI components.")

    st.markdown("### Nearby Emergency Hospitals")

    if hospitals:
        display_limit = 4
        for i, h in enumerate(hospitals[:display_limit]):
            st.markdown(f"**{i+1}.** {h}")

        if len(hospitals) > display_limit:
            with st.expander(f"See {len(hospitals) - display_limit} more facilities nearby"):
                for i, h in enumerate(hospitals[display_limit:], start=display_limit + 1):
                    st.markdown(f"**{i}.** {h}")
    else:
        st.info("No nearby facilities found. Please contact local emergency services immediately.")

    st.write("---")
    st.markdown("### First-Aid Consultation")

    chat_key = "venomguard_chat_history"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {"role": "assistant", "content": first_aid}
        ]

    for msg in st.session_state[chat_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask a question about symptoms, immediate steps, or hospital arrival..."):
        st.session_state[chat_key].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        system_prompt = (
            f"You are VenomGuard's emergency medical assistant for a patient who encountered a {snake_type}. "
            "Adhere strictly to official WHO Snakebite Guidelines. Provide calm, direct, actionable advice without jargon. "
            "Emphasize immobilization and immediate hospital transport. Prohibit tourniquets, incisions, and suction."
        )

        llm_messages = [{"role": "system", "content": system_prompt}]
        for m in st.session_state[chat_key][-6:]:
            llm_messages.append({"role": m["role"], "content": m["content"]})

        with st.chat_message("assistant"):
            with st.spinner("Reviewing clinical guidance..."):
                response_text = query_llm_assistant(llm_messages, snake_type=snake_type)
                st.markdown(response_text)

        st.session_state[chat_key].append({"role": "assistant", "content": response_text})


def only_chat(snake_type: str = "Unknown Snake"):
    first_aid_chat(
        snake_type=snake_type,
        first_aid=(
            f"Hello. This is the VenomGuard First-Aid Companion. "
            f"If an individual was bitten or encountered a snake ({snake_type}), "
            "this interface provides verified WHO first-aid steps, identifies harmful myths, "
            "and assists in hospital navigation. Please describe the situation."
        ),
        hospitals=[
            "[Search Emergency Hospitals Near Me](https://www.google.com/maps/search/emergency+hospital)"
        ]
    )
