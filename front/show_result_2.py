"""
VenomGuard - Detection Result Presentation
Displays species classification, danger rating, and routing options.
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

    st.markdown("## Identification Results")

    col_img, col_info = st.columns([1, 1.2])

    with col_img:
        if image is not None:
            st.image(image, caption="Analyzed Photo", use_container_width=True)
        else:
            st.info("No preview image available.")

    with col_info:
        st.markdown(f"### {snake_name}")
        st.markdown(f"Scientific name: *{scientific_name}*")

        if is_venomous:
            st.error(f"Danger Rating: {toxicity_str}")
            st.markdown(
                "Medical Emergency: This species possesses medically significant venom. "
                "Treat any bite as an immediate emergency and proceed to a hospital without waiting for symptoms."
            )
        else:
            st.success(f"Status: {toxicity_str}")
            st.markdown(
                "This species is non-venomous. However, bite wounds can introduce bacteria. "
                "Wash the bite thoroughly with soap and clean water, and verify tetanus vaccination status."
            )

        if size_str:
            st.markdown(f"Typical Size: {size_str}")

    st.write("---")

    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("See First Aid and Hospitals", use_container_width=True):
            st.session_state["new_state"] = "first_aid"
            st.session_state["snake_type"] = snake_name
            rerun_app()

    with col_btn2:
        if st.button("Ask First-Aid Assistant", use_container_width=True):
            st.session_state["new_state"] = "chat_c2"
            st.session_state["snake_type"] = snake_name
            rerun_app()

    with col_btn3:
        if st.button("Check Another Photo", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    return "first_aid", True, is_venomous, snake_name


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
