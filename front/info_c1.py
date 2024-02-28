import streamlit as st 
from PIL import Image
import numpy as np
import os
from function.location import get_latitude_longitude
from function.location import get_address_from_coordinates_geopy
from function.location import address_to_latlng

def tell_snake_info():
    with st.form(key='tell snake info'):
        st.markdown("## What type of snake bit you?")
        snake_type = st.text_input("Please tell us the name of the snake.")
        # Tell us your current location
        latitude, longitude = get_latitude_longitude()
        address = get_address_from_coordinates_geopy(latitude, longitude)
        st.markdown("***")
        st.markdown("## Tell us your current location.")
        st.markdown("#### Your Location")
        # st.markdown(f"Latitude:{latitude}, Longitude:{longitude}")
        st.markdown(f"Address:{address}")
        address = st.text_area('Correct the address if there is any error.',
                                          value=address,
                                          key='address_w')
        
        print(f"latitude:{latitude}, longitude:{longitude}")
        
        submit_button = st.form_submit_button(label='Proceed to next step')
        
    if submit_button:
        
        state = "chat_c2"
        latlng = address_to_latlng(address)
        
                
        return state, snake_type, address, latlng
            # Proceed to next step
        