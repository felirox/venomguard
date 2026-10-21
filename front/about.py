"""
VenomGuard - About Page
Background on snakebite envenoming, system design, and open-source contribution.
"""

import streamlit as st


def about_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 24px; border-radius: 8px; margin-bottom: 24px;">
        <h2 style='text-align: center; color: #ffffff; margin-bottom: 6px; font-weight: 800;'>The Background of VenomGuard</h2>
        <p style='text-align: center; color: #e0e0e0; font-size: 15px; margin: 0;'>
            An open-source initiative addressing emergency snakebite triage and antivenom access.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "The public demo deployment is undergoing scheduled infrastructure maintenance and will be "
        "back online shortly. You can run all features locally or via Demo Mode."
    )

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("### The Global Impact of Snakebites")
        st.markdown("""
        Annually, roughly 5.4 million individuals sustain snakebites worldwide, resulting in 81,000 to 138,000 fatalities 
        and over 400,000 permanent disabilities, including limb amputations and chronic renal complications.

        The burden falls predominantly on agricultural workers and rural communities in tropical regions of Asia, Africa, 
        and Latin America. High mortality frequently stems from delay, lack of antivenom at local dispensaries, and 
        widespread reliance on harmful traditional practices such as razor cuts and tight tourniquets.
        """)

    with col2:
        st.markdown("### Project Origins")
        st.markdown("""
        VenomGuard was initiated during the UGIP Hackathon organized by SoftBank and The University of Tokyo:
        
        - Niran N ([niran.dev](https://niran.dev/))
        - Miyuki
        - Yuki

        The objective is to equip individuals and health extension workers with immediate, offline-capable 
        triage and hospital routing on mobile devices.
        """)

    st.write("---")

    st.markdown("### Technical Design")

    col_t1, col_t2, col_t3 = st.columns(3)

    with col_t1:
        st.markdown("#### Computer Vision")
        st.markdown("""
        - Dual-stage classification: initial presence verification followed by species differentiation.
        - Reference dataset covering 3,600+ snake taxa with verified venom profiles.
        - Resilient fallback to pure-Python matching when offline.
        """)

    with col_t2:
        st.markdown("#### Hospital Geolocation")
        st.markdown("""
        - Automated IP geolocation and address resolution via OpenStreetMap and Google Maps.
        - Routing to regional medical centers equipped for snakebite emergencies.
        - Direct calling interface for universal emergency dispatch (112).
        """)

    with col_t3:
        st.markdown("#### Clinical Triage Engine")
        st.markdown("""
        - Implementation of official World Health Organization snakebite management protocols.
        - Direct prohibition of dangerous practices (tourniquets, suction, incisions).
        - Conversational assistant with deterministic offline rule-based fallback.
        """)

    st.write("---")

    st.markdown("### Open Source Development")
    st.markdown("""
    VenomGuard is published under the MIT license to facilitate community adaptation, regional database 
    expansion, and translation into vernacular languages. Contributions from developers, clinicians, and 
    herpetologists are welcome via our GitHub repository.
    """)

    if st.button("Return to Home", use_container_width=True):
        st.session_state["new_state"] = "home"
        if hasattr(st, "rerun"):
            st.rerun()
        elif hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
