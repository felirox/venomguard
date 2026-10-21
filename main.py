"""
VenomGuard - Main Streamlit Application Controller
Entry point coordinating page routing, session state, and global UI components.
"""

from dotenv import load_dotenv
import streamlit as st
from streamlit_option_menu import option_menu

from front.about import about_page
from front.chat_c2 import chatting_page
from front.error import error_page
from front.first_aid_3 import first_aid_page
from front.home import home_page
from front.info_c1 import tell_snake_info
from front.partner import partner_page
from front.show_result_2 import show_result
from front.upload_image_1 import upload_image

# Load environment configuration
load_dotenv()


def rerun_app():
    """Cross-version Streamlit rerun helper."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


# Page configuration
st.set_page_config(
    page_title="VenomGuard - AI Snakebite Triage & Hospital Locator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header Branding
st.markdown(
    """
    <div style="text-align: center; padding: 10px 0 18px 0;">
        <h1 style='
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 44px;
            font-weight: 800;
            margin-bottom: 4px;
            letter-spacing: -0.5px;
        '>
            🛡️ VenomGuard
        </h1>
        <p style="color: #888888; font-size: 16px; margin: 0;">
            Open-source snakebite identification, verified first aid, and antivenom hospital locator
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")

# Initialize routing session state
if "new_state" not in st.session_state:
    st.session_state["new_state"] = "home"


# Sidebar Navigation
def on_menu_change(key):
    selection = st.session_state[key]
    state_map = {
        "Home": "home",
        "Identify Snake": "detect",
        "First-Aid Chat": "chat_c1",
        "About the Project": "about",
        "Partner with Us": "partner_page",
    }
    if selection in state_map:
        st.session_state["new_state"] = state_map[selection]


menu_items = ["Home", "Identify Snake", "First-Aid Chat", "About the Project", "Partner with Us"]
icons = ["house", "camera", "chat-dots", "info-circle", "briefcase"]

# Determine active index based on session state
current_state = st.session_state.get("new_state", "home")
default_idx = 0
if current_state == "detect":
    default_idx = 1
elif current_state in ("chat_c1", "chat_c2"):
    default_idx = 2
elif current_state == "about":
    default_idx = 3
elif current_state == "partner_page":
    default_idx = 4

with st.sidebar:
    st.markdown("### 🧭 Menu")
    option_menu(
        menu_title=None,
        options=menu_items,
        icons=icons,
        default_index=default_idx,
        on_change=on_menu_change,
        key="main_menu_nav"
    )

    st.write("---")
    st.markdown("### 🚨 Emergency Call")
    st.markdown(
        """
        <div style="text-align: center; margin-top: 6px;">
            <a href="tel:112" style="background-color: #e74c3c; color: white; padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: bold; display: block;">
                ⚡ Call 112 (Universal)
            </a>
            <p style="font-size: 11px; color: #888; margin-top: 6px; margin-bottom: 0;">
                Connects to local emergency medical dispatch.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("---")
    st.caption("VenomGuard • Built for SoftBank & UTokyo UGIP Hackathon • Open Source")


# Main Router
state = st.session_state.get("new_state", "home")

if state == "home":
    home_page()

elif state == "about":
    about_page()

elif state == "partner_page":
    partner_page()

elif state == "detect":
    result = upload_image()
    if result is not None:
        next_state, image, address, latlng, op = result
        if op is not False:
            st.session_state["new_state"] = next_state
            st.session_state["image"] = image
            st.session_state["address"] = address
            st.session_state["latlng"] = latlng
            st.session_state["op"] = op
            rerun_app()
        else:
            st.session_state["new_state"] = "error"
            st.session_state["error_message"] = "We couldn't spot a snake in that photo. Please try another shot."
            rerun_app()

elif state == "show_result":
    image = st.session_state.get("image")
    op = st.session_state.get("op")
    show_result(image, op)

elif state == "first_aid":
    op = st.session_state.get("op")
    snake_type = op[0] if (op and len(op) > 0) else st.session_state.get("snake_type", "Unknown Snake")
    location = st.session_state.get("latlng")
    first_aid_page(snake_type, location, op)

elif state == "chat_c1":
    result = tell_snake_info()
    if result is not None:
        next_state, snake_type, address, latlng = result
        st.session_state["new_state"] = next_state
        st.session_state["snake_type"] = snake_type
        st.session_state["address"] = address
        st.session_state["latlng"] = latlng
        rerun_app()

elif state == "chat_c2":
    snake_type = st.session_state.get("snake_type", "Unknown Snake")
    location = st.session_state.get("latlng")
    chatting_page(snake_type, location)

elif state == "error":
    error_page()
