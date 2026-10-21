"""
VenomGuard - Image Upload & Detection Interface
Handles camera capture, image uploads, demo sample images, and initial geolocation.
"""

from pathlib import Path
import random
from typing import Optional, Tuple

import numpy as np
from PIL import Image
import streamlit as st

from AI_Code.detect_snake_existence import DetectSnakeExistence
from function.location import address_to_latlng, get_address_from_coordinates_geopy, get_latitude_longitude

ai_snake = DetectSnakeExistence()
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "AI_Code" / "Dataset" / "examples"


def upload_image():
    """
    Renders the image submission form and performs snake detection & classification.
    Returns: (state, image, address, latlng, op)
    """
    st.markdown("## 📸 Snake Presence & Species Identification")
    st.markdown(
        "Upload a clear photograph of the snake, or use your device camera. "
        "Keep a safe distance of at least 2 meters from any live snake."
    )

    with st.form(key="snake_detection_form"):
        mode = st.selectbox(
            "Select Input Source:",
            [
                "Upload from Device / Camera",
                "[Demo Mode] Use Pre-loaded Sample Snake Image"
            ]
        )

        image: Optional[Image.Image] = None

        if mode == "Upload from Device / Camera":
            col_cam, col_file = st.columns(2)
            with col_cam:
                camera_file = st.camera_input("Take a photo (stay at safe distance)")
            with col_file:
                uploaded_file = st.file_uploader("Or upload an image file", type=["jpeg", "jpg", "png", "webp"])

            if camera_file is not None:
                image = Image.open(camera_file)
            elif uploaded_file is not None:
                image = Image.open(uploaded_file)
        else:
            # Demo Mode
            sample_files = list(EXAMPLES_DIR.glob("*.*")) if EXAMPLES_DIR.exists() else []
            if sample_files:
                chosen = random.choice(sample_files)
                image = Image.open(chosen)
                st.info(f"Loaded sample image for testing: `{chosen.name}`")
            else:
                st.warning("No sample images found in Dataset/examples. Please upload an image.")

        if image is not None:
            st.image(image, caption="Image for Snake Analysis", use_container_width=True)

        st.markdown("---")
        st.markdown("### 📍 Incident Location")
        st.markdown("Accurate location ensures routing to the closest hospital equipped with appropriate antivenom.")

        # Geolocation lookup
        lat, lng = get_latitude_longitude()
        initial_address = get_address_from_coordinates_geopy(lat, lng)

        user_address = st.text_area(
            "Verify or correct your current address / city:",
            value=initial_address,
            key="location_address_input",
            help="Enter your current city, district, or landmark."
        )

        submit_button = st.form_submit_button(
            label="🔍 Analyze Image & Determine Danger Level",
            use_container_width=True
        )

    if submit_button:
        if image is None:
            st.warning("⚠️ Please provide an image (take a picture, upload a file, or select Demo Mode).")
            return None

        with st.spinner("Analyzing image for snake presence and taxonomic features..."):
            img_array = np.array(image)
            is_present = ai_snake.get_snake_existence(img_array)

            latlng = address_to_latlng(user_address) or (lat, lng)

            if not is_present:
                st.error("No snake was detected in the submitted image. Please retry with a clearer photo.")
                return "error", image, user_address, latlng, False

            # Identify species
            snake_type = ai_snake.get_snake_type()
            op = ai_snake.get_snake_detailed_info(snake_type)

            st.success(f"Snake detected: **{op[0]}** ({op[1]})")
            return "show_result", image, user_address, latlng, op

    return None
