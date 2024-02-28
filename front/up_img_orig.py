import streamlit as st 
from PIL import Image
import numpy as np
from function.location import get_latitude_longitude
from function.location import get_address_from_coordinates_geopy
from function.location import address_to_latlng
from AI_Code.detect_snake_existence import DetectSnakeExistence
import random, os

ai_snake = DetectSnakeExistence()


def upload_image():
    hackathon_mode = st.button('[Hackathon Mode] Use a random snake image to test the app')
    image = None
    address = None
    with st.form(key='Snake Image'):
        st.markdown("## How does a snake look?")
        image_input = st.camera_input("Take a picture")
        uploaded_file = st.file_uploader("Or upload the snake image.", type=["jpeg","jpg", "png"])
        hackathon_mode = st.button('[Hackathon Mode] Use a random snake image to test the app')

        image = None
        if image_input is not None:
            # Handle camera input
            image = Image.open(image_input)
        elif uploaded_file is not None:
            # Handle file upload
            image = Image.open(uploaded_file)
        elif hackathon_mode:
            # Select a random image from the sample_images directory
            sample_images_dir = 'AI_Code/Dataset/examples'
            random_image_name = random.choice(os.listdir(sample_images_dir))
            random_image_path = os.path.join(sample_images_dir, random_image_name)
            image = Image.open(random_image_path)
        else:
            st.error("Please upload a valid image or use the camera to take a picture of a snake.")
            st.session_state["new_state"] = "error"
            st.session_state["error_message"] = "No Snake Found in the Image. Please retry"  # Assuming the second element is the error message
            st.experimental_rerun()
            
        
        if image is not None:
            img_array = np.array(image)
            st.image(img_array, caption="Image of snake", use_column_width=True)
        
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
        
    if submit_button and image is not None:
        print("Debug:",image)
        # TODO!!!!
        img_array = np.array(image)  # Ensure we have the image in numpy array format
        detection_result = ai_snake.get_snake_existence(img_array)
        state = "show_result"
        latlng = address_to_latlng(address)
            
        # Display the detection result
        if detection_result:
            st.success("Snake detected in the image.")
            snake_type = ai_snake.get_snake_type()
            op = ai_snake.get_snake_detailed_info(snake_type)
            if  "venomous" in op[2]:
                state = "show_result"
                
                st.success("It's venomous")
            else:
                state = "error"
                st.error("It's not venomous")
                
            return state, image, address, latlng, op
            # Proceed to next step
        else:
            state = "error"
            st.markdown("No snake detected in the image.")
            st.error("No snake detected in the image.")
            #Raise a warning to user to tell them to upload a valid image
            # state = "upload_image"
            return state, image, address, latlng, False