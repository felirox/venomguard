"""
Unit tests for offline emergency medical conversational triage.
"""

import unittest
from function.llm_chat import get_offline_medical_response


class TestChat(unittest.TestCase):

    def test_tourniquet_warning(self):
        resp = get_offline_medical_response("Can I put a tight tourniquet around my leg?")
        self.assertIn("DO NOT APPLY A TOURNIQUET", resp)
        self.assertIn("amputation", resp.lower())

    def test_suction_warning(self):
        resp = get_offline_medical_response("Should I suck the venom with my mouth?")
        self.assertIn("NEVER CUT THE WOUND OR ATTEMPT TO SUCK", resp)

    def test_ice_warning(self):
        resp = get_offline_medical_response("Should I put ice on the bite?")
        self.assertIn("DO NOT APPLY ICE", resp)

    def test_antivenom_guidance(self):
        resp = get_offline_medical_response("Where can I buy antivenom pills?")
        self.assertIn("Prescription Only", resp)

    def test_symptom_explanation(self):
        resp = get_offline_medical_response("What are the symptoms of this bite?", snake_type="King Cobra")
        self.assertIn("King Cobra", resp)
        self.assertIn("ptosis", resp.lower())


if __name__ == "__main__":
    unittest.main()
