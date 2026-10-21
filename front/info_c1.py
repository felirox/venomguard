"""
VenomGuard - Manual Snake Info & Incident Input
Natural form for users who don't have a photo but know the snake or have a description.
"""

from typing import Optional, Tuple
import streamlit as st

from function.location import (
    address_to_latlng,
    get_address_from_coordinates_geopy,
    get_latitude_longitude,
)


def tell_snake_info() -> Optional[Tuple[str, str, str, Optional[Tuple[float, float]]]]:
    st.markdown("## 💬 Emergency VenomChat")
    st.markdown(
        "Don't have a photo? No problem. Type in the snake's name, or describe what you remember "
        "(color, patterns, head shape, size)."
    )

    with st.form(key="tell_snake_info_form"):
        snake_type = st.text_input(
            "Snake name or description:",
            placeholder="e.g. King Cobra, Saw-scaled Viper, Green snake with triangular head...",
            help="Any detail helps—even just 'small brown snake with diamond marks'."
        )

        st.markdown("---")
        st.markdown("### 📍 Where are you?")

        lat, lng = get_latitude_longitude()
        default_address = get_address_from_coordinates_geopy(lat, lng)

        user_address = st.text_area(
            "Confirm or adjust your location:",
            value=default_address,
            key="chat_location_address",
            help="Used to find nearby emergency hospitals."
        )

        submitted = st.form_submit_button("🚀 Start First-Aid Chat", use_container_width=True)

    if submitted:
        chosen_snake = snake_type.strip() if snake_type and snake_type.strip() else "Unknown Snake"
        latlng = address_to_latlng(user_address) or (lat, lng)
        return "chat_c2", chosen_snake, user_address, latlng

    return None
