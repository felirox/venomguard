"""
VenomGuard - Emergency First Aid & Hospital Navigation
Presents calm, life-saving steps, dispels myths, and provides direct hospital directions.
"""

from typing import Any, Optional, Tuple
import streamlit as st

from function.first_aid import tell_first_aid
from function.llm_chat import first_aid_chat
from function.who_guidelines import get_who_protocol


def first_aid_page(snake_type: str, location: Optional[Tuple[float, float]], op: Any):
    snake_name = op[0] if (op and len(op) > 0) else snake_type
    species_name = op[1] if (op and len(op) > 1) else "Species unconfirmed"
    danger_level = str(op[2]) if (op and len(op) > 2) else "Unknown"
    size_info = str(op[3]) if (op and len(op) > 3) else ""

    is_venomous = "venomous" in danger_level.lower() and "non-venomous" not in danger_level.lower()

    st.markdown("## 🚨 Emergency First Aid & Next Steps")

    # Quick Emergency Dial Box
    col_call, col_status = st.columns([1.1, 1.9])
    with col_call:
        st.markdown(
            """
            <div style="background-color: #c0392b; padding: 14px; border-radius: 8px; text-align: center;">
                <h4 style="color: white; margin: 0 0 6px 0;">📞 Call Emergency Services</h4>
                <a href="tel:112" style="background-color: white; color: #c0392b; padding: 10px 16px; text-decoration: none; font-weight: bold; border-radius: 6px; display: inline-block;">
                    ⚡ Tap to Call 112 (Universal)
                </a>
                <p style="color: #fadbd8; font-size: 11px; margin-top: 6px; margin-bottom: 0;">
                    Or call your local emergency number: 911 (Americas), 108 (India), 999 (UK/Africa)
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_status:
        st.markdown(f"**Snake**: **{snake_name}** (*{species_name}*)")
        if is_venomous:
            st.error(f"⚠️ **Danger Rating**: {danger_level}")
        else:
            st.success(f"🟢 **Danger Rating**: {danger_level}")
        if size_info:
            st.caption(f"Size: {size_info}")

    st.write("---")

    # Cache protocol generation
    cache_key_fa = f"fa_content_{snake_name}"
    cache_key_hosp = f"fa_hospitals_{snake_name}"

    if cache_key_fa not in st.session_state:
        with st.spinner("Loading verified medical advice and searching nearby hospitals..."):
            fa_text, hosp_list = tell_first_aid(snake_name, location=location)
            st.session_state[cache_key_fa] = fa_text
            st.session_state[cache_key_hosp] = hosp_list
    else:
        fa_text = st.session_state[cache_key_fa]
        hosp_list = st.session_state[cache_key_hosp]

    protocol = get_who_protocol(snake_name, danger_level)

    col_dos, col_donts = st.columns(2)
    with col_dos:
        st.markdown("### 🟢 What to do right now (DO)")
        for item in protocol.immediate_dos:
            st.markdown(f"- {item}")

    with col_donts:
        st.markdown("### 🔴 Dangerous myths to avoid (DO NOT)")
        for item in protocol.critical_donts:
            st.markdown(f"- ❌ {item}")

    st.write("---")

    first_aid_chat(snake_name, fa_text, hosp_list)
