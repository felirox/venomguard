"""
VenomGuard - About Page
Comprehensive information on snakebite envenoming, the global health challenge,
system architecture, and open-source contribution guidelines.
"""

import streamlit as st


def about_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 24px; border-radius: 12px; margin-bottom: 24px;">
        <h2 style='text-align: center; color: #ffffff; margin-bottom: 8px;'>🛡️ About VenomGuard</h2>
        <p style='text-align: center; color: #e0e0e0; font-size: 16px; margin: 0;'>
            Next-Gen Open-Source Snakebite Management System with Computer Vision, Geolocation Triage, and AI First-Aid
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "🚀 **Cloud Deployment Notice**: The public deployment demo is temporarily undergoing infrastructure "
        "and model upgrades and will be back online shortly! In the meantime, all features can be run locally "
        "or explored in Demo Mode."
    )

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("### 🌍 The Global Snakebite Crisis")
        st.markdown("""
        Snakebite envenoming is officially designated by the **World Health Organization (WHO)** as a highest-priority **Neglected Tropical Disease (NTD)**:
        
        - **5.4 Million** snakebites occur globally each year.
        - **81,000 to 138,000 Deaths** annually, disproportionately claiming agricultural workers, children, and rural inhabitants.
        - **400,000+ Permanent Disabilities**, including limb amputations, kidney damage, chronic ulcerations, and psychological trauma.
        - **The Golden Hour**: Antivenom efficacy degrades rapidly with delay. When panic ensues, victims often resort to harmful practices (tourniquets, cutting, sucking) that exacerbate injury.
        """)

    with col2:
        st.markdown("### 🎯 Project Origins")
        st.markdown("""
        VenomGuard was originally conceived and engineered for the **UGIP Hackathon by SoftBank & The University of Tokyo**, created by:
        
        - **Niran N** ([niran.dev](https://niran.dev/))
        - **Miyuki**
        - **Yuki**
        
        VenomGuard bridges the critical gap between emergency encounter and hospital antivenom administration using open-source artificial intelligence.
        """)

    st.write("---")

    st.markdown("### 🔬 System Architecture & Technologies")

    col_t1, col_t2, col_t3 = st.columns(3)

    with col_t1:
        st.markdown("#### 🐍 Computer Vision & ML")
        st.markdown("""
        - **Dual YOLO & FastAI Models**: Multi-classifier ensemble for presence verification and fine-grained species identification.
        - **3,600+ Curated Taxa**: Curated database mapping scientific and common names to verified clinical toxicity levels and morphology.
        - **Offline / Resilient Fallbacks**: Deterministic local heuristics ensure zero downtime even during total network failure.
        """)

    with col_t2:
        st.markdown("#### 🏥 Geolocation & Routing")
        st.markdown("""
        - **IP & GPS Geocoding**: Automatic incident location detection with reverse geocoding via OpenStreetMap and Google Maps API.
        - **Antivenom Center Locator**: Direct navigation links to regional emergency care centers and poison control facilities.
        - **Universal Emergency Contacts**: Immediate one-click dialing for local emergency dispatchers (112, 911, 108, 999).
        """)

    with col_t3:
        st.markdown("#### 🤖 LLM Medical Companion")
        st.markdown("""
        - **WHO Clinical Triage**: Strict compliance with WHO Guidelines for the Clinical Management of Snakebite.
        - **Myth Dispelling Engine**: Immediate intervention preventing lethal practices (tourniquets, wound incisions, ice).
        - **Hybrid AI Pipeline**: Real-time OpenAI GPT-4o conversational guidance backed by a fully offline rule-based medical responder.
        """)

    st.write("---")

    st.markdown("### 🤝 Open Source & Contributing")
    st.markdown("""
    VenomGuard is dedicated to remaining free, open, and transparent to maximize humanitarian impact:
    
    1. **Code Contributions**: Extend AI classifier weights, improve mobile responsiveness, or optimize offline caching.
    2. **Clinical & Taxa Data**: Contribute regional snake distribution datasets and antivenom inventory mappings.
    3. **Localization**: Help translate emergency instructions into vernacular languages across Africa, South Asia, and Latin America.
    """)

    if st.button("⬅️ Return to Home Page", use_container_width=True):
        st.session_state["new_state"] = "home"
        if hasattr(st, "rerun"):
            st.rerun()
        elif hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
