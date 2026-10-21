"""
VenomGuard - Photo Upload and Identification Form
Interface for camera capture, file upload, and incident location.
"""

from pathlib import Path
import random
from typing import Optional

import numpy as np
from PIL import Image
import streamlit as st

from AI_Code.detect_snake_existence import DetectSnakeExistence
from function.location import address_to_latlng, get_address_from_coordinates_geopy, get_latitude_longitude

ai_snake = DetectSnakeExistence()
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "AI_Code" / "Dataset" / "examples"


def upload_image():
    st.markdown("## Snake Identification")
    st.markdown(
        "Upload a photo or capture one using your camera. "
        "Keep at least 2 meters away from any live snake. Do not attempt to trap or corner it."
    )

    with st.form(key="snake_detection_form"):
        mode = st.selectbox(
            "Select input method:",
            [
                "Upload a photo or use camera",
                "Use a pre-loaded sample photo (Demo Mode)"
            ]
        )

        image: Optional[Image.Image] = None

        if mode == "Upload a photo or use camera":
            col_cam, col_file = st.columns(2)
            with col_cam:
                camera_file = st.camera_input("Take a photo")
            with col_file:
                uploaded_file = st.file_uploader("Or upload an image file", type=["jpeg", "jpg", "png", "webp"])

            if camera_file is not None:
                image = Image.open(camera_file)
            elif uploaded_file is not None:
                image = Image.open(uploaded_file)
        else:
            sample_files = list(EXAMPLES_DIR.glob("*.*")) if EXAMPLES_DIR.exists() else []
            if sample_files:
                chosen = random.choice(sample_files)
                image = Image.open(chosen)
                st.info(f"Loaded test sample: {chosen.name}")
            else:
                st.warning("No sample files found in Dataset/examples. Please upload a photo.")

        if image is not None:
            st.image(image, caption="Photo for analysis", use_container_width=True)

        st.markdown("---")
        st.markdown("### Location")
        st.markdown("Used to identify nearby healthcare facilities stocking antivenom.")

        lat, lng = get_latitude_longitude()
        initial_address = get_address_from_coordinates_geopy(lat, lng)

        user_address = st.text_area(
            "Confirm or adjust your city / region:",
            value=initial_address,
            key="location_address_input",
            help="Enter your city or area if the automatic detection is inaccurate."
        )

        submit_button = st.form_submit_button(
            label="Analyze Photo and Get First Aid",
            use_container_width=True
        )

    if submit_button:
        if image is None:
            st.warning("Please provide a photo or select Demo Mode first.")
            return None

        with st.spinner("Analyzing photo for species markings and venom classification..."):
            img_array = np.array(image)
            is_present = ai_snake.get_snake_existence(img_array)

            latlng = address_to_latlng(user_address) or (lat, lng)

            if not is_present:
                st.error("No snake was detected in this photo. Please try a clearer shot.")
                return "error", image, user_address, latlng, False

            snake_type = ai_snake.get_snake_type()
            op = ai_snake.get_snake_detailed_info(snake_type)

            st.success(f"Identified: {op[0]} ({op[1]})")
            return "show_result", image, user_address, latlng, op

    return None
