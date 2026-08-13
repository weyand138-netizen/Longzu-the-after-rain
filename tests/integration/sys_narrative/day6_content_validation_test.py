import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DAY6_SOURCE = ROOT / "game" / "chapters" / "day6.rpy"
SCREENS = ROOT / "game" / "screens.rpy"
TESTCASES = ROOT / "game" / "testcases.rpy"
PARTIAL_MANIFEST = ROOT / "game" / "modules" / "narrative_partial_manifest.py"
EVIDENCE = ROOT / "production" / "qa" / "evidence" / "day6-content-validation-2026-08-13-final-verified"
RUN = EVIDENCE / "run-passed"

EXPECTED_CASES = (
    "day6_backup_truth_fallback_contract",
    "day6_shared_commitment_contract",
    "day6_independent_commitment_contract",
    "day6_solo_commitment_contract",
    "day6_shift_takeback_old_order_contract",
    "day6_invalid_facts_hide_commitment_contract",
    "day6_keyboard_default_focus_and_traversal_contract",
    "day6_accessibility_visual_baselines",
)
EXPECTED_CAPTURE_HASHES = {
    "day6_cost_1280x720_keyboard_silent_reduced_motion.png": "926fe9bf63e7ce935d70cf1537b6a34c0f10d38ad0584857d9971f5c02322bb0",
    "day6_commitment_1280x720_keyboard_silent_reduced_motion.png": "85a5bf2a276783db07ff739c454423f062c2fe209a39f4fd6d6b64fadf31a645",
    "day6_cost_1280x720_font_1_5_high_contrast.png": "426b749e4d7e3ec8fce15577cc8a09002faff2711e93c0a71f9248b5fe940844",
    "day6_commitment_1280x720_font_1_5_high_contrast.png": "739b2aab55494e87993db3b7e8b3ac5f7e905d85ab26185d742e0ed054fee5cd",
}


def testcase_block(source, testcase_name):
    return source.split("testcase {}:".format(testcase_name), 1)[1].split("testcase ", 1)[0]


class Day6ContentValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DAY6_SOURCE.read_text(encoding="utf-8")
        cls.screens = SCREENS.read_text(encoding="utf-8")
        cls.testcases = TESTCASES.read_text(encoding="utf-8")
        cls.evidence = (EVIDENCE / "record.md").read_text(encoding="utf-8")

    def test_engine_routes_cover_frozen_nodes_commitment_partitions_and_fail_closed_case(self):
        for testcase_name in EXPECTED_CASES:
            self.assertIn("testcase {}:".format(testcase_name), self.testcases)
        for testcase_name in EXPECTED_CASES[:6]:
            case = testcase_block(self.testcases, testcase_name)
            self.assertIn('run Jump("chapter_day6_no_safe_house")', case)
            self.assertIn('keysym "K_RETURN"', case)

        backup = testcase_block(self.testcases, EXPECTED_CASES[0])
        for choice_id in ("day6_reopen_service_exit", "day6_disclose_withheld_archive", "day6_burn_old_identity", "day6_no_executable_route"):
            self.assertIn(choice_id, backup)
        self.assertIn('"day6_reopen_service_exit"', backup)
        self.assertIn('"day6_disclose_withheld_archive"', backup)

        for testcase_name, commitment in zip(EXPECTED_CASES[1:5], ("shared_escape", "independent_contact", "solo_departure", "old_order_return")):
            self.assertIn('agency_day6_commitment_state == "{}"'.format(commitment), testcase_block(self.testcases, testcase_name))
        shifted = testcase_block(self.testcases, EXPECTED_CASES[4])
        self.assertIn("event_shifted_cost_consequence_visible is True", shifted)
        self.assertIn("event_erii_rejects_shifted_cost_again is True", shifted)
        self.assertIn('"day6_take_cost_back"', shifted)
        invalid = testcase_block(self.testcases, EXPECTED_CASES[5])
        self.assertIn('agency_day6_commitment_state == "undetermined"', invalid)
        self.assertIn('"day5_answer_outcome_mismatch"', invalid)

    def test_accessibility_cases_cover_both_surfaces_without_test_assigned_focus(self):
        focus_case = testcase_block(self.testcases, EXPECTED_CASES[6])
        visual_case = testcase_block(self.testcases, EXPECTED_CASES[7])
        self.assertNotIn("renpy.set_focus", focus_case)
        self.assertIn('_focused_day6_choice_id() == "day1_choice_0"', focus_case)
        self.assertIn('_focused_day6_choice_id() == "day1_choice_1"', focus_case)
        self.assertIn("renpy.set_physical_size, (1280, 720)", visual_case)
        self.assertIn('setattr, renpy.game.preferences, "self_voicing", False', visual_case)
        self.assertIn("apply_accessibility_settings, 1.5, True, True, False, False", visual_case)
        for capture_name in EXPECTED_CAPTURE_HASHES:
            self.assertIn(capture_name, visual_case)
        self.assertIn('text_hover_underline (current_chapter in ("day3", "day4", "day5", "day6"))', self.screens)

    def test_evidence_binds_current_source_testcase_output_and_capture_bytes(self):
        result = json.loads((RUN / "result.json").read_text(encoding="utf-8-sig"))
        stdout = (RUN / "stdout.txt").read_bytes()
        stderr = (RUN / "stderr.txt").read_bytes()
        self.assertEqual(hashlib.sha256(DAY6_SOURCE.read_bytes()).hexdigest(), result["day6_source_sha256"])
        self.assertEqual(hashlib.sha256(TESTCASES.read_bytes()).hexdigest(), result["testcases_sha256"])
        self.assertEqual(hashlib.sha256(stdout).hexdigest(), result["stdout_sha256"])
        self.assertEqual(hashlib.sha256(stderr).hexdigest(), result["stderr_sha256"])
        self.assertEqual(-1, result["exit_code"])
        self.assertEqual("[rpytest] Status: PASSED ", result["status_line"])
        self.assertIn(b"Test cases :    45 |    45 passed", stdout)
        self.assertIn(b"Assertions :   386 |   386 passed", stdout)
        for capture_name, expected_hash in EXPECTED_CAPTURE_HASHES.items():
            payload = (RUN / "screenshots" / "visual" / capture_name).read_bytes()
            self.assertEqual(b"\x89PNG\r\n\x1a\n", payload[:8])
            self.assertEqual((1280, 720), tuple(int.from_bytes(value, "big") for value in (payload[16:20], payload[20:24])))
            self.assertEqual(expected_hash, hashlib.sha256(payload).hexdigest())
            self.assertIn(expected_hash, self.evidence)

    def test_scope_stays_day6_and_the_day1_partial_manifest_remains_unchanged(self):
        self.assertIn('PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"', PARTIAL_MANIFEST.read_text(encoding="utf-8"))
        self.assertNotIn("day6_", PARTIAL_MANIFEST.read_text(encoding="utf-8"))
        normalized = " ".join(self.evidence.split())
        self.assertIn("does not claim Day 7, a terminal witness, route qualification, ending, epilogue, partial-manifest expansion, release", normalized)
        self.assertNotRegex(self.source.lower(), r"\b(audio|sound|hover|timed|timer|animation|motion)\b")


if __name__ == "__main__":
    unittest.main()
