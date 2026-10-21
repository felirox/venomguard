"""
VenomGuard - Conversational AI & Emergency Medical Triage Companion
Real-time, calm, plain-English medical triage support for snakebite emergencies.
Supports modern OpenAI API (gpt-4o) with an intelligent, offline WHO-compliant
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
            "❌ **STRICTLY DO NOT APPLY A TOURNIQUET!**\n\n"
            "Tourniquets are one of the most dangerous snakebite myths out there. "
            "Cutting off blood flow traps venom in the limb, rapidly kills tissue, and often leads to surgical amputation. "
            "Worse yet, the moment doctors loosen that band at the hospital, all the trapped venom floods the heart and lungs at once, "
            "frequently causing sudden fatal shock.\n\n"
            "**What to do instead:** Wrap a broad, stretchy bandage firmly around the entire limb (snug like wrapping a sprained ankle—do NOT cut off blood flow), "
            "splint it so the joints can't bend, and keep the limb resting at or slightly below heart level."
        )

    if any(k in q for k in ["suck", "mouth", "cut", "razor", "blade", "incision"]):
        return (
            "❌ **NEVER CUT THE WOUND OR ATTEMPT TO SUCK OUT THE VENOM!**\n\n"
            "Sucking venom out only works in old movies—clinical studies prove it extracts less than 1% of injected venom. "
            "Slashing the bite wound with knives or razor blades slices tendons, nerves, and arteries, causing heavy bleeding. "
            "Even worse, human mouths are full of bacteria, which causes severe gangrene and wound infections when introduced into deep tissue."
        )

    if any(k in q for k in ["ice", "cold", "freeze", "pack"]):
        return (
            "❌ **DO NOT APPLY ICE OR COLD PACKS!**\n\n"
            "Freezing ice severely damages skin and muscle cells that are already under stress from venom, "
            "accelerating tissue death and causing frostbite. Keep the bite at normal room temperature."
        )

    if any(k in q for k in ["antivenom", "antidote", "medicine", "pill", "injection"]):
        return (
            "💊 **How Antivenom Actually Works:**\n\n"
            "1. **Prescription Only**: Real antivenom can ONLY be given at an equipped hospital through an IV drip under a doctor's care. "
            "Because antivenom can trigger severe allergic reactions, emergency doctors need to monitor the patient with epinephrine ready.\n"
            "2. **Species Matching**: Hospitals choose specific antivenoms based on which snake species live in the area.\n"
            "3. **Never buy online 'antidote pills' or folk powders**: They are counterfeit scams and completely useless against venom. Get to a hospital."
        )

    if any(k in q for k in ["symptom", "sign", "feel", "look like", "effect"]):
        return (
            f"🩺 **Symptoms to Watch For with a {snake_type} Bite:**\n\n"
            "- **Nerve & Breathing Signs**: Heavy, drooping eyelids (ptosis), double vision, trouble swallowing or slurred speech, shortness of breath.\n"
            "- **Blood & Clotting Signs**: Persistent oozing from the bite punctures, bleeding gums, nosebleeds, or unusual bruising.\n"
            "- **Local Tissue Signs**: Rapidly expanding swelling, blister formation, or severe burning pain.\n\n"
            "⚠️ **Mark the swelling border with a pen every 15 minutes**—this helps the emergency doctor see how quickly venom is traveling."
        )

    if any(k in q for k in ["calm", "slow", "spread", "running", "walk"]):
        return (
            "⏱️ **How to Slow Down Venom Spread:**\n\n"
            "- **Total Physical Stillness**: Have the person sit or lie down immediately. Do not let them walk or run.\n"
            "- **Take Slow Breaths**: High anxiety makes the heart pump faster, which pushes venom through the lymphatic system much quicker.\n"
            "- **Splint the Limb**: Immobilize the arm or leg so muscles don't contract and pump venom. Keep it resting below heart level."
        )

    # General emergency response
    return (
        f"🚨 **Emergency Guidance for {snake_type}:**\n\n"
        f"1. **Stay completely still**: Splint the bitten arm or leg and keep it resting below heart level.\n"
        f"2. **Take off rings & tight clothes**: Remove rings, watches, and shoes right now before swelling traps them.\n"
        f"3. **Never cut, suck, ice, or tie a tourniquet.**\n"
        f"4. **Get to a hospital**: Have someone drive or carry the patient immediately. Dial 112 (or local emergency line) if available."
    )


def query_llm_assistant(messages: List[dict], snake_type: str) -> str:
    """Queries OpenAI or falls back to the offline clinical triage engine."""
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

    # Offline Emergency Fallback
    last_user_query = messages[-1]["content"] if messages else ""
    return get_offline_medical_response(last_user_query, snake_type=snake_type)


def first_aid_chat(snake_type: str, first_aid: str, hospitals: List[str]):
    if st is None:
        raise RuntimeError("Streamlit is required to render first_aid_chat UI components.")

    st.markdown("### 🏥 Nearby Emergency Hospitals & Clinics")

    if hospitals:
        display_limit = 4
        for i, h in enumerate(hospitals[:display_limit]):
            st.markdown(f"**{i+1}.** {h}")

        if len(hospitals) > display_limit:
            with st.expander(f"See {len(hospitals) - display_limit} more hospitals nearby"):
                for i, h in enumerate(hospitals[display_limit:], start=display_limit + 1):
                    st.markdown(f"**{i}.** {h}")
    else:
        st.info("No nearby facilities found. Please contact local emergency services immediately.")

    st.write("---")
    st.markdown("### 💬 Ask the First-Aid Assistant")

    chat_key = "venomguard_chat_history"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {"role": "assistant", "content": first_aid}
        ]

    for msg in st.session_state[chat_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask a question about symptoms, what to do, or hospital prep..."):
        st.session_state[chat_key].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        system_prompt = (
            f"You are VenomGuard's emergency medical assistant for a patient who encountered a {snake_type}. "
            "Follow official WHO Snakebite Guidelines strictly. Speak calmly, clearly, and naturally without jargon. "
            "Emphasize calm immobilization and immediate hospital transport. Forbid tourniquets, incisions, and sucking."
        )

        llm_messages = [{"role": "system", "content": system_prompt}]
        for m in st.session_state[chat_key][-6:]:
            llm_messages.append({"role": m["role"], "content": m["content"]})

        with st.chat_message("assistant"):
            with st.spinner("Checking emergency guidance..."):
                response_text = query_llm_assistant(llm_messages, snake_type=snake_type)
                st.markdown(response_text)

        st.session_state[chat_key].append({"role": "assistant", "content": response_text})


def only_chat(snake_type: str = "Unknown Snake"):
    """Standalone VenomChat entry point."""
    first_aid_chat(
        snake_type=snake_type,
        first_aid=(
            f"👋 Hi there! I'm your **VenomGuard First-Aid Companion**. "
            f"If someone was bitten or you ran into a snake ({snake_type}), "
            "I'm here to give you verified steps, warn you about harmful myths, "
            "and help you get to the right hospital. What's happening right now?"
        ),
        hospitals=[
            "[Search Emergency Hospitals Near Me](https://www.google.com/maps/search/emergency+hospital)"
        ]
    )
