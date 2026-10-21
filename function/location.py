"""
VenomGuard - Geolocation & Hospital Locator Module
Provides resilient geolocation, geocoding, reverse geocoding, and emergency
hospital routing with graceful fallbacks for offline or open-source deployments.
"""

import logging
import os
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
import requests

load_dotenv()
logger = logging.getLogger("venomguard.location")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")


def get_latitude_longitude(timeout: int = 5) -> Tuple[float, float]:
    """
    Retrieves approximate geographic coordinates based on client IP.
    Uses geojs.io with a fallback to ip-api.com and safe default on network failure.
    """
    providers = [
        ("https://get.geojs.io/v1/ip/geo.json", lambda d: (float(d["latitude"]), float(d["longitude"]))),
        ("http://ip-api.com/json/", lambda d: (float(d["lat"]), float(d["lon"]))),
    ]

    for url, extractor in providers:
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                lat, lng = extractor(data)
                logger.info("IP Geolocation successful: (%s, %s)", lat, lng)
                return lat, lng
        except Exception as exc:
            logger.debug("Provider %s failed: %s", url, exc)

    logger.warning("All IP geolocation providers failed or network is offline. Defaulting to (0.0, 0.0).")
    return 0.0, 0.0


def get_address_from_coordinates_geopy(latitude: float, longitude: float, timeout: int = 5) -> str:
    """
    Converts latitude and longitude to a human-readable street address via Nominatim.
    Safe against timeouts, network errors, or invalid coordinates.
    """
    if latitude == 0.0 and longitude == 0.0:
        return "Unknown location - Please enter your current city or address manually"

    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="VenomGuard_Global_Emergency_App/2.0", timeout=timeout)
        location = geolocator.reverse((latitude, longitude), language="en")
        if location and location.address:
            return str(location.address)
    except Exception as exc:
        logger.warning("Reverse geocoding via geopy failed: %s", exc)

    return f"Coordinates: {latitude:.4f}, {longitude:.4f}"


def address_to_latlng(address: str, timeout: int = 5) -> Optional[Tuple[float, float]]:
    """
    Converts an address string to (latitude, longitude).
    Tries Google Maps API if configured, otherwise falls back to free OpenStreetMap Nominatim.
    """
    if not address or not address.strip():
        return None

    clean_address = address.strip()

    # 1. Try Google Maps API if configured
    if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "ENTER_YOUR_API_KEY":
        try:
            import googlemaps
            gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY, timeout=timeout)
            geocode_result = gmaps.geocode(clean_address)
            if geocode_result and len(geocode_result) > 0:
                loc = geocode_result[0]["geometry"]["location"]
                return float(loc["lat"]), float(loc["lng"])
        except Exception as exc:
            logger.warning("Google Maps geocoding failed: %s. Falling back to Nominatim.", exc)

    # 2. Free OpenStreetMap Nominatim fallback
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="VenomGuard_Global_Emergency_App/2.0", timeout=timeout)
        location = geolocator.geocode(clean_address)
        if location:
            return float(location.latitude), float(location.longitude)
    except Exception as exc:
        logger.warning("Nominatim geocoding failed: %s", exc)

    return None


def get_nearby_hospitals(location: Optional[Tuple[float, float]], radius_meters: int = 15000) -> List[Dict[str, str]]:
    """
    Finds nearby emergency healthcare facilities equipped for snakebite emergencies.
    Supports Google Places API with fallback to direct Google Maps search URLs.
    """
    results: List[Dict[str, str]] = []

    if not location or (location[0] == 0.0 and location[1] == 0.0):
        return [
            {
                "name": "Local District / Government Hospital",
                "address": "Seek immediate care at the nearest regional emergency hospital.",
                "url": "https://www.google.com/maps/search/emergency+hospital"
            }
        ]

    lat, lng = location

    # 1. Try Google Maps Places API if configured
    if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "ENTER_YOUR_API_KEY":
        try:
            import googlemaps
            gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
            places_result = gmaps.places_nearby(
                location=location,
                keyword="emergency hospital",
                radius=radius_meters,
                type="hospital"
            )

            for place in places_result.get("results", [])[:8]:
                name = place.get("name", "Hospital")
                vicinity = place.get("vicinity", "Nearby Emergency Center")
                place_id = place.get("place_id")
                url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}&query_place_id={place_id}" if place_id else f"https://www.google.com/maps/search/{requests.utils.quote(name)}/@{lat},{lng},14z"
                results.append({"name": name, "address": vicinity, "url": url})

            if results:
                return results
        except Exception as exc:
            logger.warning("Google Places query failed: %s", exc)

    # 2. Resilient Open Web direct map links
    maps_search_url = f"https://www.google.com/maps/search/emergency+hospital/@{lat},{lng},14z"
    osm_search_url = f"https://www.openstreetmap.org/search?query=hospital#map=14/{lat}/{lng}"

    return [
        {
            "name": "Nearest Emergency Hospital (Google Maps)",
            "address": f"Search radius ~{radius_meters // 1000}km from coordinates ({lat:.3f}, {lng:.3f})",
            "url": maps_search_url
        },
        {
            "name": "Emergency Healthcare on OpenStreetMap",
            "address": "Community open-source medical locator",
            "url": osm_search_url
        },
        {
            "name": "Government District Hospital / Poison Control",
            "address": "Contact emergency dispatcher (112 / local ambulance) for nearest antivenom facility.",
            "url": maps_search_url
        }
    ]
