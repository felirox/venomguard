import streamlit as st 

# 蛇があるかどうか、

def show_result(image):

    with st.form(key="show_result"):
        st.markdown("# Type of the snake")
        st.markdown("### Is it venomous?")
        submit_button = st.form_submit_button(label='Proceed to next step')
        print(1)
        print(submit_button)

    if submit_button is not None:
        state = "first_aid"
        snake = True
        venom = True
        snake_type = "Viper" #Miyuki, can you change this to pass the snake type from the results?
#  

        return state, snake, venom, snake_type

    