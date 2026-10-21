"""
Unit tests for location, geocoding, and hospital navigation links.
"""

import unittest
from function.location import get_address_from_coordinates_geopy, get_nearby_hospitals


class TestLocation(unittest.TestCase):

    def test_default_coordinates_address(self):
        """Verifies (0.0, 0.0) yields user-friendly unknown location text."""
        addr = get_address_from_coordinates_geopy(0.0, 0.0)
        self.assertIn("Unknown location", addr)

    def test_nearby_hospitals_generation(self):
        """Verifies emergency hospital list returns valid map URLs."""
        hospitals = get_nearby_hospitals((28.6139, 77.2090))
        self.assertGreater(len(hospitals), 0)
        first = hospitals[0]
        self.assertIn("name", first)
        self.assertIn("url", first)
        self.assertTrue(first["url"].startswith("http"))


if __name__ == "__main__":
    unittest.main()
