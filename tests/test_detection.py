"""
Unit tests for AI snake existence and species identification engine.
"""

import unittest
from AI_Code.detect_snake_existence import DetectSnakeExistence, SnakeInfo


class TestDetectSnakeExistence(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.detector = DetectSnakeExistence()
        cls.detector.load_csv_pandas()

    def test_snake_info_backwards_compatibility(self):
        """Ensures SnakeInfo supports list index unpacking and indexing."""
        info = SnakeInfo("King Cobra", "Ophiophagus hannah", "venomous 💀💀💀💀", "Length: 300 to 550 cm")
        
        # Test tuple/list unpacking
        name, sci, tox, size = info
        self.assertEqual(name, "King Cobra")
        self.assertEqual(sci, "Ophiophagus hannah")
        self.assertEqual(tox, "venomous 💀💀💀💀")
        self.assertEqual(size, "Length: 300 to 550 cm")

        # Test index access
        self.assertEqual(info[0], "King Cobra")
        self.assertEqual(info[1], "Ophiophagus hannah")
        self.assertEqual(info[2], "venomous 💀💀💀💀")
        self.assertEqual(info[3], "Length: 300 to 550 cm")

        # Test typed properties
        self.assertTrue(info.is_venomous)
        self.assertEqual(info.to_dict()["snake_name"], "King Cobra")

    def test_snake_info_non_venomous(self):
        info = SnakeInfo("Corn Snake", "Pantherophis guttatus", "non-venomous ---", "Length: 60 to 180 cm")
        self.assertFalse(info.is_venomous)

    def test_exact_common_name_lookup(self):
        info = self.detector.get_snake_detailed_info("King Cobra")
        self.assertEqual(info[0].lower(), "king cobra")
        self.assertTrue(info.is_venomous)

    def test_exact_scientific_name_lookup(self):
        info = self.detector.get_snake_detailed_info("Oxyuranus microlepidotus")
        self.assertEqual(info[0], "Inland Taipan")
        self.assertTrue(info.is_venomous)

    def test_fuzzy_matching(self):
        info = self.detector.get_snake_detailed_info("king cbra")
        self.assertEqual(info[0], "King Cobra")
        self.assertTrue(info.is_venomous)

    def test_safety_fallback_unknown_snake(self):
        """Unrecognized species should be treated as potentially venomous for clinical safety."""
        info = self.detector.get_snake_detailed_info("NonexistentAlienSnake12345")
        self.assertEqual(info[0], "NonexistentAlienSnake12345")
        self.assertTrue(info.is_venomous)
        self.assertEqual(info.source, "safety_fallback")

    def test_compare_c1_c2_selection(self):
        """Tests that compare_c1_c2 selects the higher-confidence classifier prediction."""
        self.detector.result_c1 = {"predictions": [{"confidence": 0.85, "class": "Saw-scaled Viper"}]}
        self.detector.result_c2 = {"predictions": [{"confidence": 0.60, "class": "Corn Snake"}]}
        
        # When C1 > C2, must return C1's prediction
        chosen = self.detector.compare_c1_c2()
        self.assertEqual(chosen, "Saw-scaled Viper")

        # When C2 > C1, must return C2's prediction
        self.detector.result_c1 = {"predictions": [{"confidence": 0.40, "class": "Saw-scaled Viper"}]}
        self.detector.result_c2 = {"predictions": [{"confidence": 0.92, "class": "Black Mamba"}]}
        chosen = self.detector.compare_c1_c2()
        self.assertEqual(chosen, "Black Mamba")


if __name__ == "__main__":
    unittest.main()
