"""
VenomGuard - Detection Result Presentation
Natural, human-centered summary of species classification and danger rating.
"""

from typing import Optional
import streamlit as st


def show_result(image=None, op=None):
    if op is None:
        op = st.session_state.get("op", ["Unknown Snake", "Species unconfirmed", "venomous (Uncertain)", "Length: Variable"])

    if image is None:
        image = st.session_state.get("image")

    snake_name = op[0]
    scientific_name = op[1]
    toxicity_str = str(op[2])
    size_str = str(op[3])

    is_venomous = "venomous" in toxicity_str.lower() and "non-venomous" not in toxicity_str.lower()

    st.markdown("## 🔬 Identification Results")

    col_img, col_info = st.columns([1, 1.2])

    with col_img:
        if image is not None:
            st.image(image, caption="Analyzed Photo", use_container_width=True)
        else:
            st.info("No preview image available.")

    with col_info:
        st.markdown(f"### **{snake_name}**")
        st.markdown(f"*Scientific name:* **_{scientific_name}_**")

        if is_venomous:
            st.error(f"⚠️ **Danger Rating**: {toxicity_str}")
            st.markdown(
                "🚨 **Medical Emergency**: This snake is venomous. Treat any bite as an immediate emergency. "
                "Do NOT wait around for symptoms to show up—get to a hospital now."
            )
        else:
            st.success(f"🟢 **Status**: {toxicity_str}")
            st.markdown(
                "ℹ️ This species is non-venomous. However, puncture wounds can still get infected easily. "
                "Wash the wound thoroughly with clean water and soap, and check if you need a tetanus booster."
            )

        if size_str:
            st.markdown(f"📏 **Typical Size**: {size_str}")

    st.write("---")

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("🚑 See First Aid & Find Hospitals", use_container_width=True):
            st.session_state["new_state"] = "first_aid"
            st.session_state["snake_type"] = snake_name
            rerun_app()

    with col_btn2:
        if st.button("💬 Ask First-Aid Assistant", use_container_width=True):
            st.session_state["new_state"] = "chat_c2"
            st.session_state["snake_type"] = snake_name
            rerun_app()

    with col_btn3:
        if st.button("🔄 Try Another Photo", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    return "first_aid", True, is_venomous, snake_name


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
