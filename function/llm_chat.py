"""
VenomGuard - Conversational AI & Emergency Medical Triage Companion
Provides real-time interactive medical triage support for snakebite victims.
Supports OpenAI API (v1.x and v0.x) with an intelligent, offline WHO-compliant
emergency fallback engine when API keys or network are unavailable.
"""

import logging
import os
import re
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
            "Arterial tourniquets cut off blood supply to the limb, causing tissue necrosis, "
            "gangrene, and often requiring surgical amputation. In addition, when an arterial "
            "tourniquet is eventually removed at a clinic, a sudden massive surge of trapped venom "
            "and toxins floods the heart and lungs, frequently causing fatal shock.\n\n"
            "**What to do instead:** Apply a broad, firm crepe bandage (like for a sprained ankle) "
            "over the entire limb and immobilize it with a splint. Keep the limb below heart level."
        )

    if any(k in q for k in ["suck", "mouth", "cut", "razor", "blade", "incision"]):
        return (
            "❌ **NEVER CUT THE WOUND OR ATTEMPT TO SUCK THE VENOM!**\n\n"
            "Scientific studies show that cutting and sucking removes less than 1% of injected venom. "
            "Cutting severs nerves, muscles, and arteries, aggravating uncontrolled bleeding. "
            "Mouth suction introduces virulent oral bacteria into deep wound tissues, precipitating severe "
            "gangrene and systemic sepsis. Suction devices are equally ineffective and cause further tissue damage."
        )

    if any(k in q for k in ["ice", "cold", "freeze", "pack"]):
        return (
            "❌ **DO NOT APPLY ICE OR FREEZING PACKS!**\n\n"
            "Applying ice to a snakebite site accelerates local tissue injury, compounds vasoconstriction, "
            "and induces frostbite over already vulnerable cellular structures. Keep the bite site at ambient temperature."
        )

    if any(k in q for k in ["antivenom", "antidote", "medicine", "pill", "injection"]):
        return (
            "💊 **Antivenom Administration Guidance:**\n\n"
            "1. **Prescription Only**: Antivenom can ONLY be safely administered in an equipped medical facility "
            "under direct physician supervision, due to the risk of severe anaphylaxis (allergic shock).\n"
            "2. **Species Specificity**: Polyvalent or monovalent antivenoms are chosen based on regional snake species.\n"
            "3. **Do not buy unverified internet remedies or black-market antivenoms**: Counterfeit antivenoms "
            "are common and ineffective. Please transport the patient immediately to the nearest hospital."
        )

    if any(k in q for k in ["symptom", "sign", "feel", "look like", "effect"]):
        return (
            f"🩺 **Clinical Symptoms to Monitor for {snake_type}:**\n\n"
            "- **Neurotoxic Signs**: Drooping eyelids (ptosis), blurred/double vision, difficulty swallowing, slurred speech, respiratory distress.\n"
            "- **Hemotoxic Signs**: Uncontrolled oozing from bite punctures, gum bleeding, spontaneous bruising, hematuria (blood in urine).\n"
            "- **Cytotoxic Signs**: Rapidly expanding severe swelling, blistering, darkening skin (necrosis), extreme burning pain.\n\n"
            "⚠️ **Mark the swelling boundary with a pen every 15 minutes** to help attending physicians track venom progression."
        )

    if any(k in q for k in ["calm", "slow", "spread", "running", "walk"]):
        return (
            "⏱️ **How to Slow Venom Spread:**\n\n"
            "- **Complete Physical Rest**: Keep the victim strictly seated or lying down. Do not let them walk or run.\n"
            "- **Reassurance**: Extreme anxiety and elevated heart rate accelerate lymphatic pumping of venom into the central circulation.\n"
            "- **Immobilization**: Splint the affected limb so joints cannot flex. Keep the bite at or slightly below the level of the heart."
        )

    # General emergency response
    return (
        f"🚨 **Emergency Guidance for {snake_type} Encounter:**\n\n"
        f"1. **Immobilize**: Keep the victim calm and still. Splint the bitten limb.\n"
        f"2. **Remove constriction**: Take off rings, watches, and tight footwear immediately.\n"
        f"3. **Do NOT cut, suck, ice, or apply tourniquets.**\n"
        f"4. **Emergency Transport**: Proceed directly to an equipped emergency medical facility. "
        f"If emergency dispatch is available, call 112 (or local emergency line) immediately."
    )


def query_llm_assistant(messages: List[dict], snake_type: str) -> str:
    """Queries OpenAI or falls back to the offline clinical triage engine."""
    if OPENAI_API_KEY and OPENAI_API_KEY.strip() not in ("", "ENTER_YOUR_API_KEY"):
        # Modern OpenAI client
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

        # Legacy OpenAI fallback
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
    """
    Renders the nearby hospital routing cards and conversational triage companion.
    """
    st.markdown("### 🏥 Nearby Emergency Hospitals & Antivenom Centers")

    if hospitals:
        display_limit = 4
        for i, h in enumerate(hospitals[:display_limit]):
            st.markdown(f"**{i+1}.** {h}")

        if len(hospitals) > display_limit:
            with st.expander(f"View {len(hospitals) - display_limit} more facilities"):
                for i, h in enumerate(hospitals[display_limit:], start=display_limit + 1):
                    st.markdown(f"**{i}.** {h}")
    else:
        st.info("No nearby facilities found. Please contact local emergency services immediately.")

    st.write("---")
    st.markdown("### 💬 Interactive First-Aid Companion & Triage Chat")

    # Initialize session state chat history
    chat_key = "venomguard_chat_history"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {"role": "assistant", "content": first_aid}
        ]

    # Render prior messages
    for msg in st.session_state[chat_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if user_input := st.chat_input("Ask a question about first aid, symptoms, or what to do..."):
        st.session_state[chat_key].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Build prompt messages for LLM
        system_prompt = (
            f"You are VenomGuard's emergency medical assistant for a patient who encountered a {snake_type}. "
            "Follow official WHO Snakebite Guidelines strictly. Be calm, highly urgent, and emphasize "
            "calm immobilization and immediate hospital transport. Forbid tourniquets, incisions, and sucking."
        )

        llm_messages = [{"role": "system", "content": system_prompt}]
        for m in st.session_state[chat_key][-6:]:  # Keep recent context window
            llm_messages.append({"role": m["role"], "content": m["content"]})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing emergency triage guidance..."):
                response_text = query_llm_assistant(llm_messages, snake_type=snake_type)
                st.markdown(response_text)

        st.session_state[chat_key].append({"role": "assistant", "content": response_text})


def only_chat(snake_type: str = "Unknown Snake"):
    """Standalone VenomChat entry point."""
    first_aid_chat(
        snake_type=snake_type,
        first_aid=(
            f"👋 Hello! I am your **VenomGuard Emergency Companion**. "
            f"If you or someone nearby has been bitten or encountered a snake ({snake_type}), "
            "I can guide you through verified WHO first-aid steps, dangerous myths to avoid, "
            "and hospital preparation. What is your current situation?"
        ),
        hospitals=[
            "[Search Emergency Hospitals Near Me](https://www.google.com/maps/search/emergency+hospital)"
        ]
    )
