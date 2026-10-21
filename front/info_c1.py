"""
VenomGuard - Manual Snake Info and Incident Input
Form for users who do not have a photograph but know the species or have descriptive details.
"""

from typing import Optional, Tuple
import streamlit as st

from function.location import (
    address_to_latlng,
    get_address_from_coordinates_geopy,
    get_latitude_longitude,
)


def tell_snake_info() -> Optional[Tuple[str, str, str, Optional[Tuple[float, float]]]]:
    st.markdown("## Direct Emergency Consultation")
    st.markdown(
        "If you do not have a photo, enter the common or scientific name of the snake, "
        "or describe visible features such as coloration, head shape, and approximate length."
    )

    with st.form(key="tell_snake_info_form"):
        snake_type = st.text_input(
            "Snake name or description:",
            placeholder="e.g. King Cobra, Saw-scaled Viper, green snake with triangular head",
            help="Provide any available details regarding appearance."
        )

        st.markdown("---")
        st.markdown("### Location")

        lat, lng = get_latitude_longitude()
        default_address = get_address_from_coordinates_geopy(lat, lng)

        user_address = st.text_area(
            "Confirm or adjust your current location:",
            value=default_address,
            key="chat_location_address",
            help="Used to identify nearby emergency hospitals."
        )

        submitted = st.form_submit_button("Start First-Aid Consultation", use_container_width=True)

    if submitted:
        chosen_snake = snake_type.strip() if snake_type and snake_type.strip() else "Unknown Snake"
        latlng = address_to_latlng(user_address) or (lat, lng)
        return "chat_c2", chosen_snake, user_address, latlng

    return None
