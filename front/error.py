"""
VenomGuard - Detection Error & Retry Guidance View
Provides helpful recovery paths when an image cannot be processed or contains no snake.
"""

import streamlit as st


def error_page(error_message: str = "No snake could be clearly identified in the uploaded image."):
    st.markdown("## ⚠️ Detection Notice")
    st.warning(st.session_state.get("error_message", error_message))

    st.markdown("""
    ### Why did this happen?
    - **Occlusion or Distance**: The snake may be partially hidden under foliage or photographed from too far away.
    - **Image Quality**: Low resolution, motion blur, or poor night lighting can impede computer vision classifiers.
    - **Safe Framing**: For safety, users frequently photograph from distance; try cropping the image closer to the snake if safe.
    """)

    st.write("---")
    st.markdown("### Next Steps")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📸 Upload a Different Photograph", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    with col2:
        if st.button("💬 Describe Snake Manually in VenomChat", use_container_width=True):
            st.session_state["new_state"] = "chat_c1"
            rerun_app()

    st.markdown(
        """
        <div style="margin-top: 24px; padding: 14px; background-color: #2c3e50; border-radius: 8px; text-align: center;">
            <p style="color: #ecf0f1; margin-bottom: 8px;">In an urgent bite emergency, do NOT delay hospital transit for photography.</p>
            <a href="tel:112" style="background-color: #e74c3c; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: bold;">
                🚨 Call Emergency Dispatch (112)
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
