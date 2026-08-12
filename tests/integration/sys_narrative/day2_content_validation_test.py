import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DAY2_SOURCE = ROOT / "game" / "chapters" / "day2.rpy"
DAY1_PARTIAL_MANIFEST = ROOT / "game" / "modules" / "narrative_partial_manifest.py"
SCREENS = ROOT / "game" / "screens.rpy"
TESTCASES = ROOT / "game" / "testcases.rpy"
EVIDENCE = (
    ROOT
    / "production"
    / "qa"
    / "evidence"
    / "day2-content-validation-2026-08-11"
    / "record.md"
)
EVIDENCE_RUN = EVIDENCE.parent / "run"


EXPECTED_ROUTE_CASES = (
    "day2_accept_alias_save_token_route_contract",
    "day2_assign_alias_spend_tokens_route_contract",
    "day2_repair_alias_route_contract",
    "day2_keyboard_default_focus_and_traversal_contract",
    "day2_accessibility_visual_baselines",
)
EXPECTED_CHOICE_IDS = (
    "day2_accept_alias",
    "day2_assign_alias",
    "day2_admit_alias_unknown",
    "day2_save_second_token",
    "day2_spend_both_tokens",
)
EXPECTED_BINDINGS = (
    ("day2_accept_alias", "reaction_day2_accept_alias", "payoff_day2_alias_day4"),
    ("day2_assign_alias", "reaction_day2_assign_alias", "payoff_day2_assigned_alias_day6"),
    ("day2_admit_alias_unknown", "reaction_day2_admit_alias_unknown", "payoff_day2_admit_day5"),
    ("day2_save_second_token", "reaction_day2_save_second_token", "payoff_day2_token_day6"),
    ("day2_spend_both_tokens", "reaction_day2_spend_both_tokens", "payoff_day2_spend_day4"),
)
EXPECTED_VISIBLE_REACTIONS = {
    "day2_accept_alias_save_token_route_contract": (
        "\u5979\u628a\u624b\u7559\u5728\u6309\u952e\u4e0a\uff0c\u770b\u7740\u6635\u79f0\u5728\u5f00\u573a\u753b\u9762\u91cc\u4eae\u8d77\u6765\u3002",
        "\u5979\u628a\u7b2c\u4e8c\u679a\u5e01\u4ea4\u7ed9\u4ed6\u4fdd\u7ba1\uff0c\u7136\u540e\u7528\u7559\u4e0b\u7684\u4e00\u679a\u5e01\u5f00\u59cb\u6e38\u620f\u3002",
    ),
    "day2_assign_alias_spend_tokens_route_contract": (
        "\u5979\u7167\u7740\u65b0\u7684\u540d\u5b57\u6309\u5b8c\u6700\u540e\u4e00\u4e2a\u952e\uff0c\u5374\u628a\u624b\u4ece\u9762\u677f\u4e0a\u79fb\u5f00\u3002",
        "\u6700\u540e\u4e00\u679a\u5e01\u843d\u8fdb\u673a\u5668\u3002\u5979\u628a\u624b\u653e\u56de\u64cd\u7eb5\u6746\u4e0a\uff0c\u76f4\u5230\u8fd9\u4e00\u5c40\u7684\u97f3\u4e50\u505c\u4e0b\u3002",
    ),
    "day2_repair_alias_route_contract": (
        "\u8def\u660e\u975e\u628a\u8bdd\u6536\u56de\u6765\u3002\u7ed8\u68a8\u8863\u91cd\u65b0\u6572\u4e0b\u81ea\u5df1\u7684\u6635\u79f0\uff0c\u518d\u628a\u5c4f\u5e55\u63a8\u5230\u4ed6\u9762\u524d\u3002",
        "\u5979\u628a\u7b2c\u4e8c\u679a\u5e01\u4ea4\u7ed9\u4ed6\u4fdd\u7ba1\uff0c\u7136\u540e\u7528\u7559\u4e0b\u7684\u4e00\u679a\u5e01\u5f00\u59cb\u6e38\u620f\u3002",
    ),
}
EXPECTED_CAPTURES = (
    "day2_alias_1280x720_keyboard_silent_reduced_motion.png",
    "day2_tokens_1280x720_keyboard_silent_reduced_motion.png",
    "day2_alias_1280x720_font_1_5_high_contrast.png",
    "day2_tokens_1280x720_font_1_5_high_contrast.png",
)
EXPECTED_CAPTURE_HASHES = {
    "day2_alias_1280x720_keyboard_silent_reduced_motion.png": "47de8ee60c02666d4834f517bebba7c183a7580cc9988f4fcbb7932057a9b8b3",
    "day2_tokens_1280x720_keyboard_silent_reduced_motion.png": "b4b8f058d2507ea0c2fb11146def3bf5e9d87bc36fa6eb53ef266310ca8617cf",
    "day2_alias_1280x720_font_1_5_high_contrast.png": "ccdbc09d6848d46939bf6e3d3f8aa42e815bb4c589ae5537ef6a570943d2fb30",
    "day2_tokens_1280x720_font_1_5_high_contrast.png": "7228a209df1b8c20fddd8fc19e729e639d3d0813b1eacc2e8eecca1a146f726f",
}


class Day2ContentValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DAY2_SOURCE.read_text(encoding="utf-8")
        cls.screens = SCREENS.read_text(encoding="utf-8")
        cls.testcases = TESTCASES.read_text(encoding="utf-8")
        cls.partial_manifest = DAY1_PARTIAL_MANIFEST.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_source_hash_is_current_in_the_day2_evidence_record(self):
        recorded = re.search(
            r"^\*\*Day 2 source SHA-256\*\*: `([0-9a-f]{64})`$",
            self.evidence,
            re.MULTILINE,
        )
        self.assertIsNotNone(recorded)
        self.assertEqual(
            hashlib.sha256(DAY2_SOURCE.read_bytes()).hexdigest(), recorded.group(1)
        )

    def test_engine_routes_cover_every_canonical_day2_response_by_keyboard(self):
        for testcase in EXPECTED_ROUTE_CASES:
            self.assertIn("testcase {}:".format(testcase), self.testcases)
        for choice_id in EXPECTED_CHOICE_IDS:
            self.assertIn(choice_id, self.testcases)
        day2_cases = self.testcases[
            self.testcases.index("testcase day2_accept_alias_save_token_route_contract:") : self.testcases.index(
                "testcase day3_share_honor_route_contract:"
            )
        ]
        self.assertEqual(12, day2_cases.count('keysym "K_RETURN"'))
        self.assertIn('run Function(renpy.set_focus, "choice", "day1_choice_2")', self.testcases)
        self.assertIn('has_unresolved_token("token_silence_as_consent") is True', self.testcases)
        self.assertIn('has_unresolved_token("token_silence_as_consent") is False', self.testcases)
        normal_route = self.testcases.split(
            "testcase day2_accept_alias_save_token_route_contract:", 1
        )[1].split("testcase ", 1)[0]
        self.assertIn(
            'renpy.get_displayable("choice", "day1_choice_2") is None',
            normal_route,
        )
        repair_route = self.testcases.split(
            "testcase day2_repair_alias_route_contract:", 1
        )[1].split("testcase ", 1)[0]
        self.assertIn(
            'renpy.get_displayable("choice", "day1_choice_2") is not None',
            repair_route,
        )
        for testcase, reactions in EXPECTED_VISIBLE_REACTIONS.items():
            route_case = self.testcases.split("testcase {}:".format(testcase), 1)[1]
            route_case = route_case.split("testcase ", 1)[0]
            for reaction in reactions:
                encoded_reaction = reaction.encode("unicode_escape").decode("ascii")
                self.assertIn(
                    'keysym "K_RETURN"\n    assert "{}"'.format(encoded_reaction),
                    route_case,
                )

    def test_engine_proves_day2_default_focus_and_keyboard_traversal_without_test_focus_assignment(self):
        focus_case = self.testcases.split(
            "testcase day2_keyboard_default_focus_and_traversal_contract:", 1
        )[1].split("testcase ", 1)[0]
        self.assertNotIn("renpy.set_focus", focus_case)
        self.assertIn('assert eval _focused_day2_choice_id() == "day1_choice_0"', focus_case)
        self.assertIn('keysym "K_DOWN"', focus_case)
        self.assertIn('assert eval _focused_day2_choice_id() == "day1_choice_1"', focus_case)
        self.assertIn('keysym "K_DOWN" repeat 2', focus_case)
        self.assertIn('assert eval _focused_day2_choice_id() == "day1_choice_2"', focus_case)
        self.assertIn('keysym "K_RETURN"', focus_case)
        self.assertIn('choice_history == ["day2_assign_alias", "day2_spend_both_tokens"]', focus_case)
        self.assertIn(
            'choice_history == ["day1_assume_food_consent", "day2_admit_alias_unknown", "day2_save_second_token"]',
            focus_case,
        )

    def test_source_exactly_declares_the_five_approved_day2_joins(self):
        records = tuple(
            re.findall(
                r'\(\s*"(day2_[a-z_]+)"\s*,\s*"(reaction_day2_[a-z_]+)"\s*,\s*"(payoff_[a-z0-9_]+)"',
                self.source.split("DAY2_CHOICE_RECORDS = (", 1)[1].split(
                    "DAY2_CHOICE_EFFECTS", 1
                )[0],
            )
        )
        self.assertEqual(EXPECTED_BINDINGS, records)

    def test_day2_choice_surfaces_are_keyboard_safe_and_do_not_expose_internal_semantics(self):
        self.assertIn("if not critical_choice_interaction:", self.screens)
        self.assertIn('id "quick_menu_root"', self.screens)
        self.assertIn("default_focus (index == 0)", self.screens)
        self.assertIn("text_size int(32 * accessibility_scale)", self.screens)
        self.assertIn('background Solid(("#000000" if accessibility_high_contrast', self.screens)
        for forbidden in ("hidden score", "route semantics", "token/resource", "ending condition"):
            self.assertNotIn(forbidden, self.source.lower())

    def test_visual_baseline_testcase_captures_both_day2_choice_surfaces_in_both_variants(self):
        visual_case = self.testcases.split("testcase day2_accessibility_visual_baselines:", 1)[1].split(
            "testcase accessibility_settings_batch_contract:", 1
        )[0]
        self.assertIn("renpy.set_physical_size, (1280, 720)", visual_case)
        self.assertIn('setattr, renpy.game.preferences, "self_voicing", False', visual_case)
        self.assertIn("apply_accessibility_settings, 1.0, False, True, False, False", visual_case)
        self.assertIn("apply_accessibility_settings, 1.5, True, True, False, False", visual_case)
        for capture in EXPECTED_CAPTURES:
            self.assertIn(capture, visual_case)

    def test_day2_source_keeps_the_textual_tradeoff_and_has_no_audio_or_motion_gate(self):
        self.assertIn("scene_day2_alias_answer", self.source)
        self.assertIn("scene_day2_two_tokens", self.source)
        self.assertIn("scene_day2_last_machine", self.source)
        self.assertIn('if has_unresolved_token("token_silence_as_consent"):', self.source)
        self.assertNotRegex(self.source.lower(), r"\b(audio|sound|hover|timed|timer|animation|motion)\b")

    def test_day1_only_partial_manifest_has_not_been_extended_or_promoted_for_day2(self):
        self.assertIn('PARTIAL_MANIFEST_SCHEMA = "narrative_partial_day1_manifest:v1"', self.partial_manifest)
        self.assertIn('DAY1_SOURCE_UNIT_ID = "chapter_day1_her_own_name"', self.partial_manifest)
        self.assertNotIn("day2_", self.partial_manifest)
        self.assertIn("full_production_manifest=False", self.partial_manifest)
        self.assertIn("terminal_witness_coverage=TERMINAL_WITNESS_NOT_APPLICABLE", self.partial_manifest)
        self.assertIn("cannot satisfy a full production gate", self.partial_manifest)

    def test_evidence_records_runner_captures_and_boundary_review(self):
        self.assertIn("## Preserved Engine Run", self.evidence)
        self.assertIn("## Visual and Accessibility Results", self.evidence)
        self.assertIn("## Content Review", self.evidence)
        self.assertIn("ADR-0009", self.evidence)
        self.assertRegex(self.evidence, r"no\s+Day 2 partial manifest")
        for capture in EXPECTED_CAPTURES:
            self.assertIn(capture, self.evidence)

    def test_preserved_evidence_files_match_the_recorded_capture_hashes_and_dimensions(self):
        stdout_bytes = (EVIDENCE_RUN / "stdout.txt").read_bytes()
        stdout = stdout_bytes.decode("utf-8")
        self.assertIn("[rpytest] Status: PASSED", stdout)
        result = json.loads((EVIDENCE_RUN / "result.json").read_text(encoding="utf-8"))
        stderr = (EVIDENCE_RUN / "stderr.txt").read_bytes()
        self.assertEqual("[rpytest] Status: PASSED", result["status_line"])
        self.assertEqual(
            hashlib.sha256(stdout_bytes).hexdigest(), result["stdout_sha256"]
        )
        self.assertEqual(hashlib.sha256(stderr).hexdigest(), result["stderr_sha256"])
        self.assertIn("Test cases :    18 |    18 passed", stdout)
        self.assertIn("Assertions :   102 |   102 passed", stdout)
        for capture, expected_hash in EXPECTED_CAPTURE_HASHES.items():
            capture_path = EVIDENCE_RUN / "screenshots" / "visual" / capture
            payload = capture_path.read_bytes()
            self.assertEqual(b"\x89PNG\r\n\x1a\n", payload[:8])
            self.assertEqual((1280, 720), tuple(int.from_bytes(value, "big") for value in (payload[16:20], payload[20:24])))
            self.assertEqual(expected_hash, hashlib.sha256(payload).hexdigest())
            self.assertIn(expected_hash, self.evidence)


if __name__ == "__main__":
    unittest.main()
