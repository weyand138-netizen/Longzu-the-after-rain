import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DAY4_SOURCE = ROOT / "game" / "chapters" / "day4.rpy"
DAY1_PARTIAL_MANIFEST = ROOT / "game" / "modules" / "narrative_partial_manifest.py"
SCREENS = ROOT / "game" / "screens.rpy"
TESTCASES = ROOT / "game" / "testcases.rpy"
EVIDENCE = ROOT / "production" / "qa" / "evidence" / "day4-content-validation-2026-08-11" / "record.md"
EVIDENCE_RUN = EVIDENCE.parent / "run"


EXPECTED_ROUTE_CASES = (
    "day4_two_ticket_contact_register_route_contract",
    "day4_single_ticket_contact_decline_route_contract",
    "day4_no_backup_contact_register_route_contract",
    "day4_contact_requires_approved_alias_and_retained_token_contract",
    "day4_keyboard_default_focus_and_traversal_contract",
    "day4_accessibility_visual_baselines",
)
EXPECTED_CAPTURE_NAMES = (
    "day4_route_1280x720_keyboard_silent_reduced_motion.png",
    "day4_contact_1280x720_keyboard_silent_reduced_motion.png",
    "day4_route_1280x720_font_1_5_high_contrast.png",
    "day4_contact_1280x720_font_1_5_high_contrast.png",
)


def testcase_block(source, testcase_name):
    """Return one testcase body without accepting an absent testcase as coverage."""

    marker = "testcase {}:".format(testcase_name)
    return source.split(marker, 1)[1].split("testcase ", 1)[0]


class Day4ContentValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DAY4_SOURCE.read_text(encoding="utf-8")
        cls.screens = SCREENS.read_text(encoding="utf-8")
        cls.testcases = TESTCASES.read_text(encoding="utf-8")
        cls.partial_manifest = DAY1_PARTIAL_MANIFEST.read_text(encoding="utf-8")

    def test_engine_routes_cover_ticket_contact_and_guarded_no_backup_paths_by_keyboard(self):
        for testcase_name in EXPECTED_ROUTE_CASES:
            self.assertIn("testcase {}:".format(testcase_name), self.testcases)

        for testcase_name in EXPECTED_ROUTE_CASES[:4]:
            case = testcase_block(self.testcases, testcase_name)
            self.assertIn('run Jump("chapter_day4_seaside_train")', case)
            self.assertIn('keysym "K_RETURN"', case)
            self.assertIn('renpy.get_displayable("quick_menu", "quick_menu_root") is None', case)
            self.assertIn('advance until screen "choice"', case)

        two_ticket = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[0])
        self.assertIn('resource_two_tickets is True', two_ticket)
        self.assertIn('event_identity_exposed is True', two_ticket)
        self.assertIn('event_two_window_tickets_acquired is True', two_ticket)
        self.assertIn('resource_contact_card is True', two_ticket)
        self.assertIn('event_contact_risk_handover_complete is True', two_ticket)

        single_ticket = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[1])
        self.assertIn('resource_single_ticket is True', single_ticket)
        self.assertIn('event_contact_channel_declined is True', single_ticket)
        self.assertIn('has_unresolved_token("token_abandon_backup_plan") is True', single_ticket)

        no_backup = testcase_block(self.testcases, EXPECTED_ROUTE_CASES[2])
        self.assertIn('agency_day4_route_preparation_outcome == "outcome_self_controlled_option_not_prepared"', no_backup)
        self.assertIn('agency_day4_independent_contact_outcome == "outcome_independent_option_prepared"', no_backup)

    def test_route_preparation_answer_precedes_responses_and_contact_requires_alias_and_token(self):
        route_answer = 'agency_day4_route_preparation_answer = DAY4_ROUTE_PREPARATION_ANSWER_STATE'
        first_response = 'apply_choice("day4_buy_two_tickets_real_name"'
        self.assertLess(self.source.index(route_answer), self.source.index(first_response))

        contact_guard = re.search(
            r"if \(\s*(?P<guard>.*?)\s*\):\n\s+\$ agency_day4_independent_contact_request",
            self.source,
            re.DOTALL,
        )
        self.assertIsNotNone(contact_guard)
        self.assertIn('"day2_save_second_token" in choice_history', contact_guard.group("guard"))
        self.assertTrue(
            '"day2_accept_alias" in choice_history' in contact_guard.group("guard")
            or '"day2_admit_alias_unknown" in choice_history' in contact_guard.group("guard"),
            "Day 4 contact must require an approved alias outcome as well as the retained arcade token.",
        )

    def test_accessibility_baselines_use_physical_surface_keyboard_focus_and_non_colour_indicator(self):
        focus_case = testcase_block(self.testcases, "day4_keyboard_default_focus_and_traversal_contract")
        self.assertNotIn("renpy.set_focus", focus_case)
        for choice_id in ("day1_choice_0", "day1_choice_1", "day1_choice_2"):
            self.assertIn('_focused_day4_choice_id() == "{}"'.format(choice_id), focus_case)
        self.assertEqual(3, focus_case.count('keysym "K_DOWN"'))

        visual_case = testcase_block(self.testcases, "day4_accessibility_visual_baselines")
        self.assertNotIn("renpy.set_focus", visual_case)
        self.assertIn("renpy.set_physical_size, (1280, 720)", visual_case)
        self.assertIn('setattr, renpy.game.preferences, "self_voicing", False', visual_case)
        self.assertIn("apply_accessibility_settings, 1.0, False, True, False, False", visual_case)
        self.assertIn("apply_accessibility_settings, 1.5, True, True, False, False", visual_case)
        for capture_name in EXPECTED_CAPTURE_NAMES:
            self.assertIn(capture_name, visual_case)
        self.assertIn('text_hover_underline (current_chapter in ("day3", "day4", "day5", "day6"))', self.screens)

    def test_decision_facts_remain_textual_and_partial_manifest_scope_stays_day1_only(self):
        self.assertIn("scene_day4_route_answer", self.source)
        self.assertIn("scene_day4_contact_channel", self.source)
        self.assertNotRegex(self.source.lower(), r"\b(audio|sound|hover|timed|timer|animation|motion)\b")
        self.assertIn('PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"', self.partial_manifest)
        self.assertNotIn("day4_", self.partial_manifest)

    def test_evidence_bundle_binds_current_source_hash_and_required_artifacts(self):
        self.assertTrue(EVIDENCE.is_file(), "Day 4 evidence record is required before this integration validation can pass.")
        evidence = EVIDENCE.read_text(encoding="utf-8")
        recorded_hash = re.search(r"^\*\*Day 4 source SHA-256\*\*: `([0-9a-f]{64})`$", evidence, re.MULTILINE)
        self.assertIsNotNone(recorded_hash)
        self.assertEqual(hashlib.sha256(DAY4_SOURCE.read_bytes()).hexdigest(), recorded_hash.group(1))
        result = json.loads((EVIDENCE_RUN / "result.json").read_text(encoding="utf-8-sig"))
        self.assertEqual("[rpytest] Status: PASSED ", result["status_line"])
        self.assertEqual(
            hashlib.sha256((EVIDENCE_RUN / "stdout.txt").read_bytes()).hexdigest(),
            result["stdout_sha256"],
        )
        self.assertEqual(
            hashlib.sha256((EVIDENCE_RUN / "stderr.txt").read_bytes()).hexdigest(),
            result["stderr_sha256"],
        )
        normalized = " ".join(evidence.split())
        self.assertIn("no Day 4 partial manifest", normalized)
        self.assertIn("does not claim full-manifest, terminal-witness, ending, or release validation", normalized)
        for capture_name in EXPECTED_CAPTURE_NAMES:
            self.assertIn(capture_name, evidence)
            capture = EVIDENCE_RUN / "screenshots" / "visual" / capture_name
            payload = capture.read_bytes()
            self.assertEqual(b"\x89PNG\r\n\x1a\n", payload[:8])
            self.assertEqual(
                (1280, 720),
                tuple(int.from_bytes(value, "big") for value in (payload[16:20], payload[20:24])),
            )


if __name__ == "__main__":
    unittest.main()
