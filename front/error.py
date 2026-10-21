"""
VenomGuard - Detection Retry and Guidance
Practical assistance when an uploaded image cannot be classified.
"""

import streamlit as st


def error_page(error_message: str = "No snake could be detected in the provided image."):
    st.markdown("## Detection Notice")
    st.warning(st.session_state.get("error_message", error_message))

    st.markdown("""
    ### Potential factors:
    - Background camouflage: Snakes often match surrounding foliage, rocks, and soil.
    - Camera distance: Photos taken from a safe distance may leave the subject too small for reliable classification.
    - Image sharpness: Motion blur or low lighting can obscure diagnostic scale patterns.
    """)

    st.write("---")
    st.markdown("### Next Steps")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Upload Another Photo", use_container_width=True):
            st.session_state["new_state"] = "detect"
            rerun_app()

    with col2:
        if st.button("Describe the Snake in Chat", use_container_width=True):
            st.session_state["new_state"] = "chat_c1"
            rerun_app()

    st.markdown(
        """
        <div style="margin-top: 24px; padding: 14px; background-color: #2c3e50; border-radius: 6px; text-align: center;">
            <p style="color: #ecf0f1; margin-bottom: 8px;">If a bite has occurred, do not delay travel to capture more photos. Seek immediate medical evaluation.</p>
            <a href="tel:112" style="background-color: #e74c3c; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-weight: bold;">
                Call Emergency Dispatch (112)
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
