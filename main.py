from front.upload_image_1 import upload_image
from front.show_result_2 import show_result
from front.first_aid_3 import first_aid_page
from streamlit_option_menu import option_menu
from front.home import home_page
from front.about import about_page
from front.partner import partner_page
from front.error import error_page
from front.info_c1 import tell_snake_info
from front.chat_c2 import chatting_page


import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(
    page_title="VenomGuard",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/d/d5/Snake_icon.svg"
)

# 🛡️VenomGuard🛡️
st.markdown("""
    <h1 style='
        font-style: normal; 
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; 
        font-size: 48px; 
        color: #ECF0F1;
        text-align: center; 
        margin-bottom: 20px;
        -webkit-text-stroke: 1px #2C3E50; 
        text-shadow: 2px 2px 4px #7F8C8D; 
    '>
        🛡️VenomGuard
    </h1>
    """, unsafe_allow_html=True)


st.write('---')
st.write("##")

if 'new_state' not in st.session_state:
    print("new_verを初期化")
    st.session_state['new_state'] = "home"
    
if st.session_state['new_state'] == "home":
    home_page()

if st.session_state['new_state'] == "about":
    about_page()

if st.session_state['new_state'] == "detect":
    result = upload_image()
    if result is not None:

        if result[4] is not False:
            st.session_state["new_state"],\
                st.session_state["image"],\
                st.session_state["address"],\
                st.session_state["latlng"],\
                st.session_state["op"] = result
            st.experimental_rerun()
        else:
            st.session_state["new_state"] = "error"
            st.session_state["error_message"] = "No Snake Found in the Image. Please retry"  # Assuming the second element is the error message
            st.experimental_rerun()
            # raise error that image does not contain snake and to reupload
            
if st.session_state['new_state'] == "partner_page":
    partner_page()
    
def on_change(key):
    selection = st.session_state[key]
    if selection == "Home":
        st.session_state['new_state'] = "home"
    elif selection == "About":
        st.session_state['new_state'] = "about"
    elif selection == "Detect":
        st.session_state['new_state'] = "detect"
    elif selection == "VenomChat":
        st.session_state['new_state'] = "chat_c1"
    elif selection == "Partner with Us":
        st.session_state['new_state'] = "partner_page"

    
with st.sidebar:
    selected = option_menu("Main Menu", ['Home', 'About', 'Detect', 'VenomChat',"Partner with Us"], menu_icon=None,
        icons=['house','lightbulb', 'card-image', 'chat-dots','bi-briefcase-fill'], default_index=0, on_change=on_change, key="main_menu")

if st.session_state["new_state"] == "error":
    error_page()

if st.session_state["new_state"] == "show_result":
    image = st.session_state["image"]
    result = show_result(image)
    if result is not None:
        st.session_state["new_state"],\
            st.session_state["snake"],\
            st.session_state["venom"],\
            st.session_state["snake_type"] = result
        st.experimental_rerun()
    
if st.session_state["new_state"] == "first_aid":
    snake_type = st.session_state["op"][1]
    location = st.session_state["latlng"]
    op = st.session_state["op"]
    first_aid_page(snake_type, location, op)

if st.session_state["new_state"] == "chat_c1":
    
    result = tell_snake_info()
    if result is not None:
        st.session_state["new_state"],\
            st.session_state["snake_type"],\
            st.session_state["address"],\
            st.session_state["latlng"] = result
        st.experimental_rerun()
    
if st.session_state["new_state"] == "chat_c2":
    snake_type = st.session_state["snake_type"]
    location = st.session_state["latlng"]
    chatting_page(snake_type, location)
    
print("LAST")