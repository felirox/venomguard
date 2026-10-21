"""
VenomGuard - Partnership & Institutional Collaboration View
Outlines collaboration opportunities for healthcare networks, corporate CSR,
government ministries of health, and international NGOs.
"""

import streamlit as st


def partner_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 22px; border-radius: 12px; margin-bottom: 24px; text-align: center;">
        <h2 style='color: white; margin: 0;'>🤝 Partner with VenomGuard</h2>
        <p style='color: #f1f8f5; margin-top: 6px; font-size: 16px;'>
            Join us in reducing snakebite fatalities and disabilities worldwide through open technology
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    At VenomGuard, we believe eradicating preventable snakebite deaths requires coordinated global action.
    We collaborate across three core sectors:
    """)

    tab_gov, tab_corp, tab_ngo = st.tabs([
        "🏛️ Government & Ministries of Health",
        "🏢 Healthcare Industry & Corporate CSR",
        "🌍 NGOs & Academic Researchers"
    ])

    with tab_gov:
        st.markdown("### 🏛️ Public Health & National Emergency Frameworks")
        st.markdown("""
        National health authorities in snakebite-endemic regions can integrate VenomGuard directly into their rural health infrastructure:
        
        1. **Emergency Dispatch Integration**: Connect VenomGuard's triage stream directly with national emergency dispatch numbers (e.g., 108 in India, 112 in GSM zones).
        2. **Antivenom Stockpile Tracking**: Real-time visibility into regional antivenom inventories at district hospital level to route patients only to stocked clinics.
        3. **Community Healthcare Worker Triage**: Equipping rural field workers (e.g. ASHA workers in India, community health extensionists) with offline detection tools.
        4. **Epidemiological Surveillance**: Anonymized incidence heatmaps informing national antivenom procurement and deployment.
        """)

    with tab_corp:
        st.markdown("### 🏢 Corporate Social Responsibility & Pharmaceutical Partnerships")
        st.markdown("""
        We partner with pharmaceutical companies, technology leaders, and medical device manufacturers to scale global life-saving access:
        
        - **Antivenom Subsidization**: Direct funding channel subsidizing costly antivenom vials for impoverished agricultural families.
        - **Compute & Model Training**: Cloud compute credits powering continuous model retraining on expansive field photography datasets.
        - **Cold-Chain Logistics**: Partnerships ensuring rapid distribution of temperature-sensitive antivenoms to remote rural health posts.
        - **Brand Visibility & CSR Impact**: Transparent impact reporting tracking verified lives saved and clinics equipped.
        """)

        st.markdown("#### Partnership Recognition Tiers")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("**Silver Partner**\n- Recognition in annual impact report\n- Community outreach alignment\n- Direct clinic subsidy tracking")
        with c2:
            st.success("**Gold Partner**\n- Priority feature in antivenom directory\n- Joint press releases & global health forum representation\n- Regional deployment sponsorship")
        with c3:
            st.warning("**Platinum Partner**\n- Strategic advisory board position\n- Co-developed regional AI models\n- High-impact national deployment programs")

    with tab_ngo:
        st.markdown("### 🌍 NGOs, MSF, and Academic Researchers")
        st.markdown("""
        VenomGuard welcomes active research collaboration with international organizations:
        
        - **Data Sharing**: Open exchange of anonymized bite records, clinical outcomes, and regional herpetological sightings.
        - **Field Clinical Trials**: Validating model accuracy in real-world clinical triage conditions across Africa and Southeast Asia.
        - **Educational Curriculum**: Co-authoring multilingual educational posters and mobile first-aid guides to dispel lethal snakebite folk myths.
        """)

    st.write("---")
    st.markdown("### 📬 Get in Touch with the VenomGuard Team")
    st.markdown("To explore a pilot deployment or institutional partnership, reach out to our team at **partners@venomguard.org** or connect via [niran.dev](https://niran.dev/).")
