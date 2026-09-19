import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DAY3_SOURCE = ROOT / "game" / "chapters" / "day3.rpy"
DAY1_PARTIAL_MANIFEST = ROOT / "game" / "modules" / "narrative_partial_manifest.py"
SCREENS = ROOT / "game" / "screens.rpy"
TESTCASES = ROOT / "game" / "testcases.rpy"
EVIDENCE = ROOT / "production" / "qa" / "evidence" / "day3-content-validation-2026-08-11" / "record.md"
EVIDENCE_RUN = EVIDENCE.parent / "run"

EXPECTED_ROUTE_CASES = (
    "day3_share_honor_route_contract",
    "day3_share_force_route_contract",
    "day3_hide_honor_route_contract",
    "day3_hide_force_route_contract",
    "day3_keyboard_default_focus_and_traversal_contract",
    "day3_accessibility_visual_baselines",
)
EXPECTED_ROUTE_HISTORIES = {
    "day3_share_honor_route_contract": ("day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_honor_pause"),
    "day3_share_force_route_contract": ("day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_force_explanation"),
    "day3_hide_honor_route_contract": ("day2_assign_alias", "day2_spend_both_tokens", "day3_hide_school_evidence", "day3_honor_pause"),
    "day3_hide_force_route_contract": ("day2_assign_alias", "day2_spend_both_tokens", "day3_hide_school_evidence", "day3_force_explanation"),
}
EXPECTED_CAPTURES = (
    "day3_evidence_1280x720_keyboard_silent_reduced_motion.png",
    "day3_truth_pace_1280x720_keyboard_silent_reduced_motion.png",
    "day3_evidence_1280x720_font_1_5_high_contrast.png",
    "day3_truth_pace_1280x720_font_1_5_high_contrast.png",
)
EXPECTED_CAPTURE_HASHES = {
    "day3_evidence_1280x720_keyboard_silent_reduced_motion.png": "6aa757eb34ce0adf7a80c9cdc5057ca9f097c59fd635d2bb770a57e56053ba23",
    "day3_truth_pace_1280x720_keyboard_silent_reduced_motion.png": "0a2848d133da160190076896dd90cdd5b293feabe1d40cb45ce451ee9d961d59",
    "day3_evidence_1280x720_font_1_5_high_contrast.png": "0597043403e60c433f975f4b0963890c5264417dd39398208c4ec5bb33955c14",
    "day3_truth_pace_1280x720_font_1_5_high_contrast.png": "d976e15e0a4df0537f08eb80a018c82528b8f6787f7c57baa6ffdd3a7b3a4ecf",
}


class Day3ContentValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DAY3_SOURCE.read_text(encoding="utf-8")
        cls.screens = SCREENS.read_text(encoding="utf-8")
        cls.testcases = TESTCASES.read_text(encoding="utf-8")
        cls.partial_manifest = DAY1_PARTIAL_MANIFEST.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_source_hash_is_current_in_the_day3_evidence_record(self):
        recorded = re.search(r"^\*\*Day 3 source SHA-256\*\*: `([0-9a-f]{64})`$", self.evidence, re.MULTILINE)
        self.assertIsNotNone(recorded)
        self.assertEqual(hashlib.sha256(DAY3_SOURCE.read_bytes()).hexdigest(), recorded.group(1))

    def test_engine_routes_cover_all_day2_compatible_day3_combinations_by_keyboard(self):
        for testcase in EXPECTED_ROUTE_CASES:
            self.assertIn("testcase {}:".format(testcase), self.testcases)
        for testcase, history in EXPECTED_ROUTE_HISTORIES.items():
            route_case = self.testcases.split("testcase {}:".format(testcase), 1)[1].split("testcase ", 1)[0]
            self.assertEqual(2, route_case.count('keysym "K_RETURN"'))
            self.assertIn('run Jump("chapter_day3_empty_school")', route_case)
            self.assertIn('assert eval current_chapter == "day3"', route_case)
            expected_history = "[{}]".format(
                ", ".join('"{}"'.format(choice_id) for choice_id in history)
            )
            self.assertIn(
                "current_choice_history() == {}".format(expected_history),
                route_case,
            )
            self.assertIn('advance until screen "choice"', route_case)
            self.assertIn('assert eval current_chapter == "prologue"', route_case)
            self.assertIn('renpy.get_displayable("choice", "day1_choice_0") is not None', route_case)
            self.assertIn('renpy.get_displayable("choice", "day1_choice_1") is not None', route_case)
            self.assertIn('renpy.get_displayable("quick_menu", "quick_menu_root") is None', route_case)
        for assertion in (
            'event_empty_school_trace_confirmed is True',
            'cp_day3_empty_school_trace_complete is True',
            'agency_day3_truth_pace_request == "event_truth_pace_requested"',
            'agency_day3_truth_pace_answer == "event_erii_closes_archive"',
            'agency_day3_truth_pace_outcome == "outcome_pause_honored"',
            'agency_day3_truth_pace_outcome == "outcome_pause_overridden"',
        ):
            self.assertIn(assertion, self.testcases)

    def test_keyboard_focus_is_observed_without_assignment_and_quick_menu_is_absent(self):
        focus_case = self.testcases.split("testcase day3_keyboard_default_focus_and_traversal_contract:", 1)[1].split("testcase ", 1)[0]
        self.assertNotIn("renpy.set_focus", focus_case)
        self.assertEqual(2, focus_case.count('assert eval _focused_day3_choice_id() == "day1_choice_0"'))
        self.assertEqual(2, focus_case.count('assert eval _focused_day3_choice_id() == "day1_choice_1"'))
        self.assertEqual(2, focus_case.count('keysym "K_DOWN"'))
        self.assertEqual(2, focus_case.count('keysym "K_RETURN"'))
        self.assertIn('renpy.get_displayable("quick_menu", "quick_menu_root") is None', focus_case)

    def test_accessibility_baselines_capture_both_choice_surfaces_at_1280x720(self):
        visual_case = self.testcases.split("testcase day3_accessibility_visual_baselines:", 1)[1].split("testcase ", 1)[0]
        self.assertIn("renpy.set_physical_size, (1280, 720)", visual_case)
        self.assertIn('setattr, renpy.game.preferences, "self_voicing", False', visual_case)
        self.assertIn("apply_accessibility_settings, 1.0, False, True, False, False", visual_case)
        self.assertIn("apply_accessibility_settings, 1.5, True, True, False, False", visual_case)
        self.assertNotIn("renpy.set_focus", visual_case)
        self.assertEqual(4, visual_case.count('assert eval _focused_day3_choice_id() == "day1_choice_0"'))
        for capture in EXPECTED_CAPTURES:
            self.assertIn(capture, visual_case)
        self.assertIn("default_focus (index == 0)", self.screens)
        self.assertIn('text_hover_underline (current_chapter in ("day3", "day4", "day5", "day6"))', self.screens)
        self.assertIn("text_size int(32 * accessibility_scale)", self.screens)
        self.assertIn('background Solid(("#000000" if accessibility_high_contrast', self.screens)

    def test_decision_facts_have_text_and_keyboard_paths_not_sensory_only_gates(self):
        self.assertIn("scene_day3_evidence_choice", self.source)
        self.assertIn("scene_day3_truth_pace_answer", self.source)
        self.assertNotRegex(self.source.lower(), r"\b(audio|sound|hover|timed|timer|animation|motion)\b")
        self.assertEqual(2, self.source.count("$ critical_choice_interaction = True"))
        self.assertEqual(4, self.source.count("$ critical_choice_interaction = False"))
        self.assertIn('keysym "K_RETURN"', self.testcases)

    def test_evidence_run_and_scope_remain_current_and_fail_closed(self):
        stdout = (EVIDENCE_RUN / "stdout.txt").read_bytes()
        stderr = (EVIDENCE_RUN / "stderr.txt").read_bytes()
        result = json.loads((EVIDENCE_RUN / "result.json").read_text(encoding="utf-8-sig"))
        self.assertIn(b"[rpytest] Status: PASSED", stdout)
        self.assertEqual(-1, result["exit_code"])
        self.assertEqual("[rpytest] Status: PASSED ", result["status_line"])
        self.assertEqual(hashlib.sha256(stdout).hexdigest(), result["stdout_sha256"])
        self.assertEqual(hashlib.sha256(stderr).hexdigest(), result["stderr_sha256"])
        self.assertIn(b"Test cases :    24 |    24 passed", stdout)
        self.assertIn(b"Assertions :   172 |   172 passed", stdout)
        for capture, expected_hash in EXPECTED_CAPTURE_HASHES.items():
            payload = (EVIDENCE_RUN / "screenshots" / "visual" / capture).read_bytes()
            self.assertEqual(b"\x89PNG\r\n\x1a\n", payload[:8])
            self.assertEqual((1280, 720), tuple(int.from_bytes(value, "big") for value in (payload[16:20], payload[20:24])))
            self.assertEqual(expected_hash, hashlib.sha256(payload).hexdigest())
            self.assertIn(expected_hash, self.evidence)
        self.assertIn('PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"', self.partial_manifest)
        self.assertNotIn("day3_", self.partial_manifest)
        normalized_evidence = " ".join(self.evidence.split())
        self.assertIn("no Day 3 partial manifest", normalized_evidence)
        self.assertIn("does not claim full-manifest, terminal-witness, ending, or release validation", normalized_evidence)


if __name__ == "__main__":
    unittest.main()
