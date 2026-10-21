"""
VenomGuard - Partner With Us
Collaboration avenues for clinics, health departments, and research institutions.
"""

import streamlit as st


def partner_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 22px; border-radius: 8px; margin-bottom: 24px; text-align: center;">
        <h2 style='color: white; margin: 0; font-weight: 800;'>Partner with VenomGuard</h2>
        <p style='color: #f1f8f5; margin-top: 6px; font-size: 15px;'>
            Collaborative avenues to improve snakebite triage and antivenom routing in vulnerable regions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    Mitigating snakebite mortality requires coordination across cold-chain logistics, 
    antivenom supplies, and clinical education. We collaborate across three main sectors:
    """)

    tab_gov, tab_corp, tab_ngo = st.tabs([
        "Public Health and Rural Clinics",
        "Healthcare Industry and Corporate Support",
        "Field NGOs and Clinical Researchers"
    ])

    with tab_gov:
        st.markdown("### Public Health Authorities and Regional Clinics")
        st.markdown("""
        For health departments and district medical centers in snakebite-endemic regions:
        
        - Emergency dispatch integration: Connecting VenomGuard triage data with ambulance dispatch lines.
        - Antivenom inventory tracking: Maintaining current registries of facilities stocking specific antivenoms.
        - Community health extension: Equipping rural primary healthcare workers with offline identification tools.
        - Surveillance mapping: Analyzing anonymized incidence data to forecast seasonal surge periods.
        """)

    with tab_corp:
        st.markdown("### Corporate Social Responsibility and Industry Partnerships")
        st.markdown("""
        For organizations providing technical infrastructure or philanthropic support:
        
        - Antivenom access funding: Grants directed to subsidize antivenom vials for low-income patients.
        - Computational resources: Cloud compute support for retraining models across underrepresented species.
        - Distribution and cold-chain support: Initiatives maintaining required refrigeration at remote health posts.
        """)

    with tab_ngo:
        st.markdown("### Herpetologists and Humanitarian Researchers")
        st.markdown("""
        For field clinicians, toxicologists, and herpetologists:
        
        - Image data contributions: Sharing verified field photography to expand classification coverage.
        - Protocol review: Refining first-aid advice for atypical or regional venom profiles.
        - Localization: Translating emergency guidance into regional languages and dialects.
        """)

    st.write("---")
    st.markdown("### Contact")
    st.markdown("To discuss pilot deployments or research collaboration, contact **partners@venomguard.org** or connect via [niran.dev](https://niran.dev/).")
