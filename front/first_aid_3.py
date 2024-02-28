import streamlit as st
from function.first_aid import tell_first_aid
from function.llm_chat import first_aid_chat

def first_aid_page(snake_type, location, op):
    st.markdown("## Snake Information")


    st.markdown(f"- Snake Name: {op[0]}")
    st.markdown(f"- Species Name: {op[1]}")
    
    # Apply conditional coloring
    danger_level = op[2].lower()
    if 'non-venomous' in danger_level:
        dcolor = "green"
    elif 'venomous' in danger_level and 'danger' in danger_level:
        dcolor = "red; -webkit-text-stroke: 1px red"
    elif 'venomous' in danger_level:
        dcolor = "red"
    else:  # Unclear dangerousness
        dcolor = "yellow"

    st.markdown(f"- <span style='color: {dcolor};'>Danger Level: {op[2]}</span>", unsafe_allow_html=True)
    
    # st.markdown(f"- Danger Level: <span style='color: red;'>{op[2]}</span>", unsafe_allow_html=True)

    st.markdown(f"- {op[3]}")
    st.session_state["snake_type"] = op[0]

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
    
    if st.button('Call Emergency Number (112)'):
        # Create a link that opens the phone dialer with number 112 pre-filled
        st.markdown('<a href="tel:112" target="_blank">Click to call 112</a>', unsafe_allow_html=True)
