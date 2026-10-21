"""
VenomGuard - Home Page
Clean, natural introduction with emergency quick-actions and insights into deadly snakes.
"""

from pathlib import Path
from PIL import Image
import streamlit as st

SNAKE_DIR = Path(__file__).resolve().parent.parent / "snake"


def home_page():
    # Website status notice
    st.info(
        "⚡ **Heads up**: The live website is down for a quick infrastructure refresh right now, "
        "but it'll be back up very soon! In the meantime, you can test everything right here locally "
        "or flip on Demo Mode to explore all features."
    )

    # Hero Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1f1c2c 0%, #928DAB 100%); padding: 32px 24px; border-radius: 12px; margin-bottom: 24px; text-align: center;">
        <h1 style='color: #ffffff; font-size: 40px; margin-bottom: 8px; font-weight: 800;'>🛡️ VenomGuard</h1>
        <h3 style='color: #f0f0f0; font-size: 20px; font-weight: 400; margin-top: 0;'>
            Identify the snake. Get verified first aid. Find antivenom fast.
        </h3>
        <p style='color: #e0e0e0; max-width: 720px; margin: 12px auto 0 auto; font-size: 15px; line-height: 1.6;'>
            When someone gets bitten, panic and bad advice can be just as dangerous as the venom itself. 
            VenomGuard gives you clear, verified first aid, identifies snake species from a photo, 
            and points you straight to the nearest hospital equipped with antivenom.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Action Cards
    col_a1, col_a2, col_a3 = st.columns(3)

    with col_a1:
        st.markdown("#### 📸 Check a Snake Photo")
        st.write("Upload or take a picture from a safe distance to see if it's venomous and identify the species.")
        if st.button("Identify Snake", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    with col_a2:
        st.markdown("#### 💬 Ask the First-Aid AI")
        st.write("Have a quick question about symptoms, what to do, or what NOT to do? Chat with our triage assistant.")
        if st.button("Start VenomChat", use_container_width=True):
            st.session_state["new_state"] = "chat_c1"
            rerun_app()

    with col_a3:
        st.markdown("#### 🌍 Why We Built This")
        st.write("Read about the global snakebite crisis and how open-source software helps save lives.")
        if st.button("About & Partnerships", use_container_width=True):
            st.session_state["new_state"] = "about"
            rerun_app()

    st.write("---")

    # Top 3 Deadliest Snakes
    st.markdown("### 🐍 Three of the World's Deadliest Snakes")
    st.caption("Knowing what lives in your region and how to spot them can keep you safe.")

    col1, col2, col3 = st.columns(3)

    with col1:
        it_path = SNAKE_DIR / "Inland-Taipan.jpeg"
        if it_path.exists():
            st.image(Image.open(it_path), use_container_width=True)
        st.markdown("#### 🥇 Inland Taipan")
        st.caption("*Oxyuranus microlepidotus* • Central Australia")
        st.write(
            "Hands down the most toxic venom of any land snake—a single bite has enough venom to kill "
            "100 full-grown humans. Luckily, it's shy, calm, and lives out in remote clay plains, so people "
            "rarely run into one in the wild."
        )

    with col2:
        ct_path = SNAKE_DIR / "Coastal-Taipan.jpeg"
        if ct_path.exists():
            st.image(Image.open(ct_path), use_container_width=True)
        st.markdown("#### 🥈 Coastal Taipan")
        st.caption("*Oxyuranus scutellatus* • Northern & Eastern Australia")
        st.write(
            "Unlike its inland cousin, the coastal taipan is lightning-fast and nervous. If cornered, "
            "it strikes repeatedly. Its venom shuts down your nervous system and stops blood from clotting, "
            "making urgent hospital care essential."
        )

    with col3:
        kc_path = SNAKE_DIR / "King-Cobra.jpeg"
        if kc_path.exists():
            st.image(Image.open(kc_path), use_container_width=True)
        st.markdown("#### 🥉 King Cobra")
        st.caption("*Ophiophagus hannah* • South & Southeast Asia")
        st.write(
            "The longest venomous snake on Earth, reaching up to 18 feet (5.5m). When threatened, it can lift "
            "a third of its body straight up and hiss like a growling dog. It delivers a massive dose of "
            "neurotoxin that can stop human breathing in under 30 minutes."
        )


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
