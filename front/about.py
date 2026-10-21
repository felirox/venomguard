"""
VenomGuard - About Page
The story behind VenomGuard, the global snakebite crisis, and how open source saves lives.
"""

import streamlit as st


def about_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 26px; border-radius: 12px; margin-bottom: 24px;">
        <h2 style='text-align: center; color: #ffffff; margin-bottom: 6px; font-weight: 800;'>🛡️ The Story of VenomGuard</h2>
        <p style='text-align: center; color: #e0e0e0; font-size: 16px; margin: 0;'>
            How an open-source hackathon project is tackling one of the world's most neglected emergencies.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "⚡ **Heads up on the demo site**: Our public cloud deployment is getting an infrastructure upgrade "
        "and will be back up very soon! You can run the entire platform locally or explore in Demo Mode."
    )

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("### 💔 The Reality of Snakebites")
        st.markdown("""
        Every single year, roughly **5.4 million people** are bitten by snakes. Between **81,000 and 138,000 die**, 
        and another **400,000 people** survive with permanent amputations, kidney failure, or severe trauma.

        Most victims are agricultural workers, rural families, and kids in tropical regions of Asia, Africa, 
        and Latin America. The heartbreaking truth is that many of these deaths aren't just caused by venom—they're 
        caused by **panic, bad first aid (like razor incisions and tight tourniquets), and not knowing which clinic 
        actually has antivenom in stock.**
        """)

    with col2:
        st.markdown("### 🚀 Where VenomGuard Started")
        st.markdown("""
        VenomGuard was originally born during the **UGIP Hackathon by SoftBank & The University of Tokyo**, built by:
        
        - **Niran N** ([niran.dev](https://niran.dev/))
        - **Miyuki**
        - **Yuki**

        We wanted to build something practical that anyone with a basic phone could use in the middle of nowhere 
        to get calm, verified advice when seconds count.
        """)

    st.write("---")

    st.markdown("### 🛠️ How It Works Under the Hood")

    col_t1, col_t2, col_t3 = st.columns(3)

    with col_t1:
        st.markdown("#### 🐍 Computer Vision")
        st.markdown("""
        - **FastAI & YOLOv8 Ensemble**: Multi-stage detection checks whether an image actually contains a snake, then classifies the species.
        - **3,600+ Species Database**: Built from curated biological records detailing venom type, lethality, and typical size.
        - **Works Offline**: If you lose signal, the app falls back to pure-Python local matching without crashing.
        """)

    with col_t2:
        st.markdown("#### 🏥 Smart Hospital Routing")
        st.markdown("""
        - **Auto-Location**: Detects your rough coordinates or lets you type your area.
        - **Antivenom Center Links**: Generates instant turn-by-turn navigation to major hospitals equipped for emergencies.
        - **One-Tap Emergency Call**: Dial 112 with a single tap on your phone.
        """)

    with col_t3:
        st.markdown("#### 🤖 Emergency First-Aid AI")
        st.markdown("""
        - **WHO-Compliant**: Follows the World Health Organization's official clinical snakebite guidelines to the letter.
        - **Busts Deadly Myths**: Firmly stops users from applying dangerous tourniquets, ice, or mouth suction.
        - **Dual Pipeline**: Uses modern LLMs when connected, and an intelligent offline triage engine when you have no signal.
        """)

    st.write("---")

    st.markdown("### 🤝 Why We Kept It Open Source")
    st.markdown("""
    Proprietary health apps charge subscriptions that the people most affected by snakebites could never afford. 
    By keeping VenomGuard free and open-source under the MIT license, anyone—from wilderness clubs and park rangers 
    to rural health clinics and researchers—can fork it, translate it into local languages, or adapt it to their own region.

    Want to help? Check out our GitHub repository, add local snake data, or help translate first-aid advice!
    """)

    if st.button("⬅️ Back to Home", use_container_width=True):
        st.session_state["new_state"] = "home"
        if hasattr(st, "rerun"):
            st.rerun()
        elif hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
