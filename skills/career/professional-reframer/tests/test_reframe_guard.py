import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("reframe_guard", ROOT / "scripts" / "reframe_guard.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class GuardTests(unittest.TestCase):
    def test_detects_corporate_sludge(self):
        result = MOD.lint("Dynamic leader with a proven track record of world-class results.")
        phrases = {x["phrase"] for x in result["flags"]}
        self.assertIn("dynamic leader", phrases)
        self.assertIn("proven track record", phrases)
        self.assertIn("world-class", phrases)

    def test_claim_delta_flags_leadership_upgrade(self):
        result = MOD.compare(
            "I helped the project team organize weekly updates.",
            "Led the project team and managed weekly delivery updates.",
        )
        cats = {x["category"] for x in result["introduced_claim_risks"]}
        self.assertIn("leadership", cats)
        self.assertIn("management", cats)

    def test_claim_delta_flags_new_metric(self):
        result = MOD.compare(
            "I automated a weekly report.",
            "Automated a weekly report, reducing processing time by 40%.",
        )
        self.assertTrue(any(x["category"] == "new quantified claim" for x in result["introduced_claim_risks"]))

    def test_supported_plain_reframe_not_flagged_as_scope_upgrade(self):
        result = MOD.compare(
            "I showed new employees how to use the database and fixed their issues.",
            "Trained new employees on database use and resolved user issues.",
        )
        self.assertEqual(result["introduced_claim_risks"], [])

    def test_responsible_for_style_flag(self):
        result = MOD.lint("Responsible for creating weekly reports.")
        self.assertTrue(any(x["phrase"] == "responsible for" for x in result["flags"]))


if __name__ == "__main__":
    unittest.main()
