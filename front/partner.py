"""
VenomGuard - Partner With Us
Clear, grounded partnership avenues for clinics, health departments, and sponsors.
"""

import streamlit as st


def partner_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 24px; border-radius: 12px; margin-bottom: 24px; text-align: center;">
        <h2 style='color: white; margin: 0; font-weight: 800;'>🤝 Partner with VenomGuard</h2>
        <p style='color: #f1f8f5; margin-top: 6px; font-size: 16px;'>
            Let's work together to get better snakebite triage tools to the communities that need them most.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    Preventing snakebite fatalities isn't just a software problem—it requires cold-chain logistics, 
    antivenom supplies, and well-trained health workers. We collaborate with partners across three main areas:
    """)

    tab_gov, tab_corp, tab_ngo = st.tabs([
        "🏛️ Health Departments & Rural Clinics",
        "🏢 Healthcare Industry & CSR Sponsors",
        "🌍 Researchers & Field Non-Profits"
    ])

    with tab_gov:
        st.markdown("### 🏛️ For Regional Health Authorities & Public Clinics")
        st.markdown("""
        If you run or support rural healthcare facilities in snakebite-endemic regions, we want to help you deploy VenomGuard locally:
        
        - **Emergency Dispatch Integration**: Link VenomGuard directly into your local ambulance lines (e.g., 108 in India or 112 in GSM networks).
        - **Antivenom Stock Audits**: Help us keep an up-to-date registry of which hospitals currently stock monovalent and polyvalent antivenom.
        - **Field Worker Toolkits**: Put lightweight offline snake identification in the hands of community health extensionists and rural clinic nurses.
        - **Incident Mapping**: Aggregate anonymized, community-level encounter data to predict seasonal snakebite spikes.
        """)

    with tab_corp:
        st.markdown("### 🏢 For CSR Programs & Tech Sponsors")
        st.markdown("""
        We are proud to partner with tech companies, medical device makers, and philanthropic foundations:
        
        - **Subsidizing Antivenom Access**: Direct financial grants to cover antivenom vials for low-income agricultural families who cannot afford treatment.
        - **Model Training & Cloud Infrastructure**: Cloud compute credits that allow us to expand our computer vision models to hundreds of rare species.
        - **Cold-Chain Logistics Support**: Helping rural clinics maintain the refrigeration required to keep antivenom potent.
        """)

    with tab_ngo:
        st.markdown("### 🌍 For Herpetologists, Doctors & Field NGOs")
        st.markdown("""
        If you work on the front lines of global health, wilderness safety, or herpetology, we'd love your expertise:
        
        - **Data Donations**: Share verified field photos to improve our detection accuracy for underrepresented species.
        - **Clinical Review**: Help verify first-aid guidelines for specialized regional venom profiles (e.g. sea snakes, rear-fanged colubrids).
        - **Language Localization**: Help translate first-aid advice into local dialects so anyone can read it during an emergency.
        """)

    st.write("---")
    st.markdown("### 📬 Get in Touch")
    st.markdown("Interested in working together or running a pilot? Drop a message to **partners@venomguard.org** or connect via [niran.dev](https://niran.dev/).")
