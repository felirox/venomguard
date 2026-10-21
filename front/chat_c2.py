"""
VenomGuard - Conversational Emergency Chat View
Renders active chat stream with hospital routing and emergency calling options.
"""

from typing import Optional, Tuple
import streamlit as st

from function.first_aid import tell_first_aid
from function.llm_chat import first_aid_chat


def chatting_page(snake_type: str, location: Optional[Tuple[float, float]] = None):
    st.markdown("## 🤖 Emergency Triage & First-Aid Companion")

    # Emergency Call Header
    col_msg, col_call = st.columns([2.5, 1])
    with col_msg:
        st.markdown(f"**Discussing Incident for**: `{snake_type}`")
        st.caption("Ask questions about first aid, swelling, what NOT to do, or hospital arrival preparation.")
    with col_call:
        st.markdown(
            '<a href="tel:112" style="background-color: #c0392b; color: white; padding: 8px 14px; text-decoration: none; font-weight: bold; border-radius: 6px; display: inline-block;">📞 Call 112</a>',
            unsafe_allow_html=True
        )

    st.write("---")

    cache_key = f"chat_fa_initial_{snake_type}"
    hosp_key = f"chat_hosp_initial_{snake_type}"

    if cache_key not in st.session_state:
        with st.spinner("Preparing emergency first-aid recommendations..."):
            fa_text, hospitals = tell_first_aid(snake_type=snake_type, location=location)
            st.session_state[cache_key] = fa_text
            st.session_state[hosp_key] = hospitals
    else:
        fa_text = st.session_state[cache_key]
        hospitals = st.session_state[hosp_key]

    first_aid_chat(snake_type, fa_text, hospitals)
