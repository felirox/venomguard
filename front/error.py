"""
VenomGuard - Detection Retry & Guidance View
Reassuring, practical assistance when an image cannot be processed.
"""

import streamlit as st


def error_page(error_message: str = "We couldn't clearly spot a snake in that photo."):
    st.markdown("## 🔍 No Snake Detected")
    st.warning(st.session_state.get("error_message", error_message))

    st.markdown("""
    ### Why did this happen?
    - **Natural Camouflage**: Snakes blend into leaves, rocks, and grass extraordinarily well.
    - **Camera Distance**: If the photo was taken from far away (which is smart for safety!), the snake might be too small for the model to detect reliably.
    - **Lighting or Blur**: Dark or shaky photos can obscure the scales and markings our classifier looks for.
    """)

    st.write("---")
    st.markdown("### What would you like to do?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📸 Try Another Photo", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    with col2:
        if st.button("💬 Describe It in VenomChat", use_container_width=True):
            st.session_state["new_state"] = "chat_c1"
            rerun_app()

    st.markdown(
        """
        <div style="margin-top: 24px; padding: 14px; background-color: #2c3e50; border-radius: 8px; text-align: center;">
            <p style="color: #ecf0f1; margin-bottom: 8px;">If someone was bitten, don't waste time taking more photos—get to a hospital right now.</p>
            <a href="tel:112" style="background-color: #e74c3c; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: bold;">
                🚨 Call Emergency Services (112)
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
