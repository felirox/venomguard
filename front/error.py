import streamlit as st


def error_page(error_message="That's unfortunate"):
    """
    Display an error message and offer an option to return to the detection page.
    """
    st.markdown(error_message)

    st.error("There is no snake detected in the picture uploaded by you")  # Display the custom error message
    # Optionally, add a button or link to guide the user back to the upload page
    if st.button("Try again"):
        st.session_state['new_state'] = "detect"
        st.experimental_rerun()
