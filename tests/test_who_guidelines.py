"""
Unit tests for WHO snakebite emergency triage and guidelines engine.
"""

import unittest
from function.who_guidelines import classify_venom_syndrome, get_who_protocol


class TestWHOGuidelines(unittest.TestCase):

    def test_neurotoxic_syndrome_classification(self):
        syndrome = classify_venom_syndrome("Indian Cobra", "venomous")
        self.assertEqual(syndrome["syndrome"], "Neurotoxic Envenomation")
        self.assertTrue(any("ptosis" in s.lower() for s in syndrome["symptoms"]))

    def test_hemotoxic_syndrome_classification(self):
        syndrome = classify_venom_syndrome("Russell's Viper", "venomous")
        self.assertIn("Hemotoxic", syndrome["syndrome"])
        self.assertTrue(any("bleeding" in s.lower() for s in syndrome["symptoms"]))

    def test_non_venomous_classification(self):
        syndrome = classify_venom_syndrome("Corn Snake", "non-venomous ---")
        self.assertIn("Non-Venomous", syndrome["syndrome"])

    def test_protocol_contains_critical_donts(self):
        protocol = get_who_protocol("Black Mamba", "venomous")
        donts_text = " ".join(protocol.critical_donts).lower()
        self.assertIn("tourniquet", donts_text)
        self.assertIn("suck", donts_text)
        self.assertIn("cut", donts_text)
        self.assertIn("ice", donts_text)

    def test_protocol_contains_essential_dos(self):
        protocol = get_who_protocol("Saw-scaled Viper", "venomous")
        dos_text = " ".join(protocol.immediate_dos).lower()
        self.assertIn("calm", dos_text)
        self.assertIn("immobilize", dos_text)
        self.assertIn("constricting", dos_text)

    def test_emergency_dispatch_numbers(self):
        protocol = get_who_protocol("Common Krait", "venomous")
        self.assertEqual(protocol.emergency_numbers.get("Global / GSM Standard"), "112")
        self.assertIn("108", protocol.emergency_numbers.get("India", ""))


if __name__ == "__main__":
    unittest.main()
