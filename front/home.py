"""
VenomGuard - Home Page
Landing page with emergency quick actions, global health announcement,
and educational insights on the world's deadliest snakes.
"""

from pathlib import Path
from PIL import Image
import streamlit as st

SNAKE_DIR = Path(__file__).resolve().parent.parent / "snake"


def home_page():
    # Emergency & Website Status Banner
    st.info(
        "⚡ **Notice**: The public cloud website is temporarily undergoing infrastructure and model "
        "upgrades and **will be back online soon!** You can run the entire platform locally or explore "
        "all features in the live interactive app below."
    )

    # Hero Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1f1c2c 0%, #928DAB 100%); padding: 30px; border-radius: 12px; margin-bottom: 24px; text-align: center;">
        <h1 style='color: #ffffff; font-size: 42px; margin-bottom: 8px;'>🛡️ VenomGuard</h1>
        <h3 style='color: #f0f0f0; font-size: 22px; font-weight: normal; margin-top: 0;'>
            Know About the Snake • Prevent Fatalities • Stay Safe
        </h3>
        <p style='color: #dcdcdc; max-width: 720px; margin: 12px auto 0 auto; font-size: 15px;'>
            An open-source AI platform combining computer vision for species identification,
            WHO-standard emergency first aid guidance, and real-time hospital locator routing.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Action Buttons
    col_a1, col_a2, col_a3 = st.columns(3)

    with col_a1:
        st.markdown("#### 📸 Snake Identification")
        st.write("Upload or photograph a snake to immediately identify species and venom danger level.")
        if st.button("🚀 Identify a Snake", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    with col_a2:
        st.markdown("#### 🤖 Emergency AI Chat")
        st.write("Chat with the interactive medical companion for emergency triage and first-aid steps.")
        if st.button("💬 Start VenomChat", use_container_width=True):
            st.session_state["new_state"] = "chat_c1"
            rerun_app()

    with col_a3:
        st.markdown("#### 🤝 Global Mission")
        st.write("Explore our mission to cut global snakebite mortality in half under the WHO 2030 roadmap.")
        if st.button("📖 Learn More & Partner", use_container_width=True):
            st.session_state["new_state"] = "about"
            rerun_app()

    st.write("---")

    # Top 3 Deadliest Snakes in the World
    st.markdown("### 🐍 Top 3 Deadliest Venomous Snakes in the World")
    st.caption("Recognizing these highly venomous species can save lives in field encounters.")

    col1, col2, col3 = st.columns(3)

    with col1:
        it_path = SNAKE_DIR / "Inland-Taipan.jpeg"
        if it_path.exists():
            st.image(Image.open(it_path), use_container_width=True)
        st.markdown("#### 🥇 1. Inland Taipan")
        st.caption("*Oxyuranus microlepidotus* (Australia)")
        st.write(
            "Possesses the most toxic venom of any land snake. A single bite yields enough "
            "lethal neurotoxin and myotoxin to kill 100 adult humans. Rarely encountered due to remote habitats."
        )

    with col2:
        ct_path = SNAKE_DIR / "Coastal-Taipan.jpeg"
        if ct_path.exists():
            st.image(Image.open(ct_path), use_container_width=True)
        st.markdown("#### 🥈 2. Coastal Taipan")
        st.caption("*Oxyuranus scutellatus* (Australia / New Guinea)")
        st.write(
            "Extremely fast and aggressive when cornered, striking repeatedly. Its potent venom "
            "contains presynaptic neurotoxins causing respiratory paralysis, accompanied by coagulopathy."
        )

    with col3:
        kc_path = SNAKE_DIR / "King-Cobra.jpeg"
        if kc_path.exists():
            st.image(Image.open(kc_path), use_container_width=True)
        st.markdown("#### 🥉 3. King Cobra")
        st.caption("*Ophiophagus hannah* (South & Southeast Asia)")
        st.write(
            "The longest venomous snake on Earth (up to 5.5 meters). Injects massive volumes of "
            "neurotoxic venom in a single bite, capable of killing a full-grown Asian elephant or human within 30 minutes."
        )


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
