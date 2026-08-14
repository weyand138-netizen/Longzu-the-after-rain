import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DAY5_SOURCE = ROOT / "game" / "chapters" / "day5.rpy"
DAY1_PARTIAL_MANIFEST = ROOT / "game" / "modules" / "narrative_partial_manifest.py"
SCREENS = ROOT / "game" / "screens.rpy"
TESTCASES = ROOT / "game" / "testcases.rpy"
REVALIDATION = ROOT / "production" / "qa" / "evidence" / "s7-02-runtime-state-revalidation-2026-08-13.md"
HISTORICAL_DAY5_SOURCE_SHA256 = "9ec6fd98498902c8bfe1bc0a72c9f497d0be8a584ce5d289853e532f4168e432"
EVIDENCE = (
    ROOT
    / "production"
    / "qa"
    / "evidence"
    / "day5-content-validation-2026-08-13-reviewed-verified"
    / "record.md"
)
EVIDENCE_RUN = EVIDENCE.parent / "run-passed"

EXPECTED_ROUTE_CASES = (
    "day5_shared_honor_and_repair_route_contract",
    "day5_contact_replace_route_contract",
    "day5_solo_route_answer_contract",
    "day5_continue_without_route_answer_contract",
    "day5_invalid_route_facts_hide_response_contract",
    "day5_keyboard_default_focus_and_traversal_contract",
    "day5_accessibility_visual_baselines",
)
EXPECTED_CAPTURE_HASHES = {
    "day5_truth_1280x720_keyboard_silent_reduced_motion.png": "b10511edcf42c70f21506d0c3c1e05668b5d845f1f04c6312125758a3d5ba077",
    "day5_response_1280x720_keyboard_silent_reduced_motion.png": "3d66b92ed645d071dbf4a9130a7a1936c15c4346ce14d6e3f79e6c7276566b62",
    "day5_truth_1280x720_font_1_5_high_contrast.png": "0b1447ca7e69505cbba46f0ca704641084cdb93f52461245cd7f76daea1c5a91",
    "day5_response_1280x720_font_1_5_high_contrast.png": "aab19a6be0bf22160bd8233583a7a1ae44ef017aa3a1fe61c4a96f1d7a089161",
}


def testcase_block(source, testcase_name):
    """Return one required testcase body and fail naturally if it is absent."""

    marker = "testcase {}:".format(testcase_name)
    return source.split(marker, 1)[1].split("testcase ", 1)[0]


class Day5ContentValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DAY5_SOURCE.read_text(encoding="utf-8")
        cls.screens = SCREENS.read_text(encoding="utf-8")
        cls.testcases = TESTCASES.read_text(encoding="utf-8")
        cls.partial_manifest = DAY1_PARTIAL_MANIFEST.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_engine_routes_cover_every_frozen_answer_and_fail_closed_partition(self):
        for testcase_name in EXPECTED_ROUTE_CASES:
            self.assertIn("testcase {}:".format(testcase_name), self.testcases)

        for testcase_name in EXPECTED_ROUTE_CASES[:5]:
            case = testcase_block(self.testcases, testcase_name)
            self.assertIn('run Jump("chapter_day5_family_lie")', case)
            self.assertIn('keysym "K_RETURN"', case)
            self.assertIn('renpy.get_displayable("quick_menu", "quick_menu_root") is None', case)

        shared = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[0])
        self.assertIn('"shared_escape"', shared)
        self.assertIn('"outcome_route_preference_honored_shared_escape"', shared)
        self.assertIn('"day5_repair_school_evidence"', shared)
        self.assertIn('"day5_repair_daily_choice"', shared)

        contact = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[1])
        self.assertIn('"independent_contact"', contact)
        self.assertIn('"outcome_route_preference_overridden_to_old_order"', contact)
        self.assertIn('event_external_blame_only is True', contact)
        self.assertIn('has_unresolved_token("token_override_daily_choice") is True', contact)
        self.assertIn('has_unresolved_token("token_hide_school_evidence") is True', contact)

        solo = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[2])
        self.assertIn('"solo_departure"', solo)
        self.assertIn('"outcome_route_preference_honored_solo_departure"', solo)

        fallback = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[3])
        self.assertIn('"continue_without_executable_route"', fallback)
        self.assertIn('"outcome_route_preference_honored_continue_without_executable_route"', fallback)

        invalid = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[4])
        self.assertIn('agency_day5_response_answer == "undetermined"', invalid)
        self.assertIn('event_family_response_requested is False', invalid)
        self.assertIn('event_erii_selects_route_response is False', invalid)
        self.assertIn('cp_day5_route_answer_expressed is False', invalid)

    def test_accessibility_cases_observe_native_focus_and_capture_both_surfaces(self):
        focus_case = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[5])
        self.assertNotIn("renpy.set_focus", focus_case)
        self.assertIn('_focused_day5_choice_id() == "day1_choice_0"', focus_case)
        self.assertIn('_focused_day5_choice_id() == "day1_choice_1"', focus_case)
        self.assertIn('renpy.get_displayable("quick_menu", "quick_menu_root") is None', focus_case)

        visual_case = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[6])
        self.assertNotIn("renpy.set_focus", visual_case)
        self.assertIn("renpy.set_physical_size, (1280, 720)", visual_case)
        self.assertIn('setattr, renpy.game.preferences, "self_voicing", False', visual_case)
        self.assertIn("apply_accessibility_settings, 1.0, False, True, False, False", visual_case)
        self.assertIn("apply_accessibility_settings, 1.5, True, True, False, False", visual_case)
        for capture_name in EXPECTED_CAPTURE_HASHES:
            self.assertIn(capture_name, visual_case)
        self.assertIn('text_hover_underline (current_chapter in ("day3", "day4", "day5", "day6"))', self.screens)
        self.assertIn("default_focus (index == 0)", self.screens)

    def test_current_evidence_binds_source_output_and_capture_bytes(self):
        recorded = re.search(
            r"^\*\*Day 5 source SHA-256\*\*: `([0-9a-f]{64})`\s*$",
            self.evidence,
            re.MULTILINE,
        )
        self.assertIsNotNone(recorded)
        self.assertEqual(HISTORICAL_DAY5_SOURCE_SHA256, recorded.group(1))

        stdout = (EVIDENCE_RUN / "stdout.txt").read_bytes()
        stderr = (EVIDENCE_RUN / "stderr.txt").read_bytes()
        result = json.loads((EVIDENCE_RUN / "result.json").read_text(encoding="utf-8-sig"))
        self.assertIn(b"[rpytest] Status: PASSED", stdout)
        self.assertEqual(-1, result["exit_code"])
        self.assertEqual("[rpytest] Status: PASSED ", result["status_line"])
        self.assertEqual(HISTORICAL_DAY5_SOURCE_SHA256, result["day5_source_sha256"])
        self.assertIn(hashlib.sha256(DAY5_SOURCE.read_bytes()).hexdigest(), REVALIDATION.read_text(encoding="utf-8"))
        recorded_testcases = re.search(
            r"^\*\*Testcase source SHA-256\*\*: `([0-9a-f]{64})`$",
            self.evidence,
            re.MULTILINE,
        )
        self.assertIsNotNone(recorded_testcases)
        self.assertEqual(recorded_testcases.group(1), result["testcases_sha256"])
        self.assertEqual(hashlib.sha256(stdout).hexdigest(), result["stdout_sha256"])
        self.assertEqual(hashlib.sha256(stderr).hexdigest(), result["stderr_sha256"])
        self.assertIn(b"Test cases :    37 |    37 passed", stdout)
        self.assertIn(b"Assertions :   345 |   345 passed", stdout)

        for capture_name, expected_hash in EXPECTED_CAPTURE_HASHES.items():
            payload = (EVIDENCE_RUN / "screenshots" / "visual" / capture_name).read_bytes()
            self.assertEqual(b"\x89PNG\r\n\x1a\n", payload[:8])
            self.assertEqual(
                (1280, 720),
                tuple(int.from_bytes(value, "big") for value in (payload[16:20], payload[20:24])),
            )
            self.assertEqual(expected_hash, hashlib.sha256(payload).hexdigest())
            self.assertIn(expected_hash, self.evidence)

    def test_scope_stays_day5_and_the_partial_manifest_remains_day1_only(self):
        self.assertIn('PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"', self.partial_manifest)
        self.assertNotIn("day5_", self.partial_manifest)
        normalized_evidence = " ".join(self.evidence.split())
        self.assertIn("no Day 5 partial manifest", normalized_evidence)
        self.assertIn(
            "does not claim full-manifest, terminal-witness, ending, epilogue, or release validation",
            normalized_evidence,
        )
        self.assertNotRegex(self.source.lower(), r"\b(audio|sound|hover|timed|timer|animation|motion)\b")


if __name__ == "__main__":
    unittest.main()
