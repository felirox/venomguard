"""
VenomGuard - Manual Snake Info & Incident Input View
Allows users without a photo to specify the snake species and incident location manually.
"""

from typing import Optional, Tuple
import streamlit as st

from function.location import (
    address_to_latlng,
    get_address_from_coordinates_geopy,
    get_latitude_longitude,
)


def tell_snake_info() -> Optional[Tuple[str, str, str, Optional[Tuple[float, float]]]]:
    st.markdown("## 💬 Direct Emergency VenomChat")
    st.markdown("If you don't have a photo of the snake, tell us its common or scientific name, or what it looked like.")

    with st.form(key="tell_snake_info_form"):
        snake_type = st.text_input(
            "Snake Name or Description:",
            placeholder="e.g. King Cobra, Saw-scaled Viper, Green snake with triangular head...",
            help="Enter any details you remember about the snake."
        )

        st.markdown("---")
        st.markdown("### 📍 Your Current Location")

        lat, lng = get_latitude_longitude()
        default_address = get_address_from_coordinates_geopy(lat, lng)

        user_address = st.text_area(
            "Verify or update your location for hospital routing:",
            value=default_address,
            key="chat_location_address"
        )

        submitted = st.form_submit_button("🚀 Start Emergency Guidance Chat", use_container_width=True)

    if submitted:
        chosen_snake = snake_type.strip() if snake_type and snake_type.strip() else "Unknown Snake"
        latlng = address_to_latlng(user_address) or (lat, lng)
        return "chat_c2", chosen_snake, user_address, latlng

    return None
