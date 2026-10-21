"""
VenomGuard - Detection Result Presentation
Presents verified taxonomic classification, venomous danger status, and emergency triage routing.
"""

from typing import Optional
import streamlit as st


def show_result(image=None, op=None):
    """
    Renders classification details and provides immediate routing to first aid.
    """
    if op is None:
        op = st.session_state.get("op", ["Unknown Snake", "Species unconfirmed", "venomous (Uncertain)", "Length: Variable"])

    if image is None:
        image = st.session_state.get("image")

    snake_name = op[0]
    scientific_name = op[1]
    toxicity_str = str(op[2])
    size_str = str(op[3])

    is_venomous = "venomous" in toxicity_str.lower() and "non-venomous" not in toxicity_str.lower()

    st.markdown("## 🔬 Snake Identification Result")

    col_img, col_info = st.columns([1, 1.2])

    with col_img:
        if image is not None:
            st.image(image, caption="Analyzed Photograph", use_container_width=True)
        else:
            st.info("No preview image available.")

    with col_info:
        st.markdown(f"### **{snake_name}**")
        st.markdown(f"*Scientific Name:* **_{scientific_name}_**")

        # Toxicity badge
        if is_venomous:
            st.error(f"⚠️ **DANGER LEVEL**: {toxicity_str.upper()}")
            st.markdown(
                "🚨 **CRITICAL WARNING**: This species possesses medically significant venom. "
                "Any bite must be treated as a medical emergency. Do NOT wait for symptoms to appear."
            )
        else:
            st.success(f"🟢 **STATUS**: {toxicity_str}")
            st.markdown(
                "ℹ️ This species is classified as non-venomous. While antivenom is not required, "
                "clean puncture wounds thoroughly with soap and water to prevent bacterial infection and check tetanus status."
            )

        st.markdown(f"📏 **Morphology & Dimensions**: {size_str}")

    st.write("---")

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("🚨 Emergency First Aid & Hospitals", use_container_width=True):
            st.session_state["new_state"] = "first_aid"
            st.session_state["snake_type"] = snake_name
            rerun_app()

    with col_btn2:
        if st.button("💬 Chat with AI Medical Companion", use_container_width=True):
            st.session_state["new_state"] = "chat_c2"
            st.session_state["snake_type"] = snake_name
            rerun_app()

    with col_btn3:
        if st.button("🔄 Analyze Another Image", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    return "first_aid", True, is_venomous, snake_name


def rerun_app():
    """Cross-version Streamlit rerun helper."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
