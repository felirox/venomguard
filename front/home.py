"""
VenomGuard - Home Page
Introduction with quick actions and reference species details.
"""

from pathlib import Path
from PIL import Image
import streamlit as st

SNAKE_DIR = Path(__file__).resolve().parent.parent / "snake"


def home_page():
    st.info(
        "The live website is temporarily down for an infrastructure update and will be back online shortly. "
        "You can run the app locally or use Demo Mode to test all features."
    )

    st.markdown("""
    <div style="background: linear-gradient(135deg, #1f1c2c 0%, #4a5568 100%); padding: 32px 24px; border-radius: 8px; margin-bottom: 24px; text-align: center;">
        <h1 style='color: #ffffff; font-size: 38px; margin-bottom: 8px; font-weight: 800;'>VenomGuard</h1>
        <h3 style='color: #edf2f7; font-size: 19px; font-weight: 400; margin-top: 0;'>
            Snake identification, verified first aid, and antivenom hospital routing
        </h3>
        <p style='color: #cbd5e0; max-width: 680px; margin: 12px auto 0 auto; font-size: 15px; line-height: 1.6;'>
            After a snakebite, bad advice and delay cause serious injury.
            VenomGuard provides verified WHO first-aid guidance, identifies snake species from a photo,
            and routes you to the nearest hospital carrying antivenom.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_a1, col_a2, col_a3 = st.columns(3)

    with col_a1:
        st.markdown("#### Check a Snake Photo")
        st.write("Upload or take a photo from a safe distance to identify the species and check its venom profile.")
        if st.button("Identify Snake", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    with col_a2:
        st.markdown("#### First-Aid Assistant")
        st.write("Ask questions about symptoms, immediate steps to take, and dangerous practices to avoid.")
        if st.button("Start First-Aid Chat", use_container_width=True):
            st.session_state["new_state"] = "chat_c1"
            rerun_app()

    with col_a3:
        st.markdown("#### Background and Mission")
        st.write("Read about the global burden of snakebites and why open-source tools matter.")
        if st.button("About the Project", use_container_width=True):
            st.session_state["new_state"] = "about"
            rerun_app()

    st.write("---")

    st.markdown("### Reference Species")
    st.caption("Commonly encountered venomous snakes with high medical significance.")

    col1, col2, col3 = st.columns(3)

    with col1:
        it_path = SNAKE_DIR / "Inland-Taipan.jpeg"
        if it_path.exists():
            st.image(Image.open(it_path), use_container_width=True)
        st.markdown("#### Inland Taipan")
        st.caption("*Oxyuranus microlepidotus* • Central Australia")
        st.write(
            "Possesses the highest venom yield per toxicity ratio of any land snake. "
            "A single bite contains enough neurotoxin to kill multiple adult humans. "
            "It lives in remote clay plains and is rarely encountered by people in the wild."
        )

    with col2:
        ct_path = SNAKE_DIR / "Coastal-Taipan.jpeg"
        if ct_path.exists():
            st.image(Image.open(ct_path), use_container_width=True)
        st.markdown("#### Coastal Taipan")
        st.caption("*Oxyuranus scutellatus* • Northern and Eastern Australia")
        st.write(
            "Fast and defensive when cornered. It inhabits coastal grasslands and agricultural areas. "
            "Its venom causes rapid presynaptic neurotoxicity and prevents blood from clotting, "
            "requiring immediate antivenom therapy."
        )

    with col3:
        kc_path = SNAKE_DIR / "King-Cobra.jpeg"
        if kc_path.exists():
            st.image(Image.open(kc_path), use_container_width=True)
        st.markdown("#### King Cobra")
        st.caption("*Ophiophagus hannah* • South and Southeast Asia")
        st.write(
            "The longest venomous snake in the world, growing up to 5.5 meters. "
            "When threatened, it raises the anterior part of its body and hisses loudly. "
            "It injects high volumes of venom per strike, which can impair breathing within 30 minutes."
        )


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
