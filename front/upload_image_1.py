"""
VenomGuard - Photo Upload & Identification Form
Natural, user-friendly interface for camera capture, file upload, and incident location.
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
    st.markdown("## 📸 Snake Identification")
    st.markdown(
        "Upload a photo or snap one with your camera. "
        "**Safety first**: Always keep at least 6 feet (2 meters) away from any live snake. Never try to catch or corner it."
    )

    with st.form(key="snake_detection_form"):
        mode = st.selectbox(
            "How would you like to provide the picture?",
            [
                "Upload a photo or take one now",
                "Try with a pre-loaded sample photo (Demo Mode)"
            ]
        )

        image: Optional[Image.Image] = None

        if mode == "Upload a photo or take one now":
            col_cam, col_file = st.columns(2)
            with col_cam:
                camera_file = st.camera_input("Take a photo (stay back!)")
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
                st.info(f"Loaded test sample: `{chosen.name}`")
            else:
                st.warning("No sample files found in Dataset/examples. Please upload a photo.")

        if image is not None:
            st.image(image, caption="Photo to analyze", use_container_width=True)

        st.markdown("---")
        st.markdown("### 📍 Where are you located?")
        st.markdown("We use this to find the closest hospitals stocked with antivenom.")

        lat, lng = get_latitude_longitude()
        initial_address = get_address_from_coordinates_geopy(lat, lng)

        user_address = st.text_area(
            "Confirm or adjust your city / area:",
            value=initial_address,
            key="location_address_input",
            help="Type your city, district, or landmark if the detected location looks off."
        )

        submit_button = st.form_submit_button(
            label="🔍 Analyze Photo & Get First Aid",
            use_container_width=True
        )

    if submit_button:
        if image is None:
            st.warning("⚠️ Please snap a photo or upload an image first, or switch to Demo Mode.")
            return None

        with st.spinner("Analyzing image for snake species and venom profile..."):
            img_array = np.array(image)
            is_present = ai_snake.get_snake_existence(img_array)

            latlng = address_to_latlng(user_address) or (lat, lng)

            if not is_present:
                st.error("We couldn't clearly detect a snake in this photo. Please try another shot.")
                return "error", image, user_address, latlng, False

            snake_type = ai_snake.get_snake_type()
            op = ai_snake.get_snake_detailed_info(snake_type)

            st.success(f"Identified: **{op[0]}** (*{op[1]}*)")
            return "show_result", image, user_address, latlng, op

    return None
