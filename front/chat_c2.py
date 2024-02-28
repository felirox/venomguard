import streamlit as st
from function.only_chat import only_chat
from function.first_aid import tell_first_aid
from function.llm_chat import first_aid_chat


def chatting_page(snake_type, location):
    st.markdown("## What to do?")
    
    # Initialize hospitals to an empty list or suitable default
    hospitals = ["City Government Hospital","Your area has no information on hospitals. Please check with local authorities."]

    if "last" not in st.session_state:
        st.session_state["last"] = False
        
    if not st.session_state["last"]:
        print("tell user the first aid.")
        st.markdown("**Thinking...**")
        # llm searches the first aid
        first_aid, hospitals = tell_first_aid(snake_type=snake_type, location=location)
        st.session_state["first_aid"] = first_aid
        st.session_state["hospitals"] = hospitals
        st.session_state["last"] = True
    else:
        # Ensure that hospitals is retrieved from session state if already set
        hospitals = st.session_state.get("hospitals", [])
        
    first_aid_chat(snake_type, st.session_state["first_aid"], hospitals)



