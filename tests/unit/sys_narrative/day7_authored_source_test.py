import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = ROOT / "game" / "chapters" / "day7.rpy"
BASELINE_PATH = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
SOURCE_GENERATION_PATH = ROOT / "game" / "modules" / "day7_source_generation.py"
TESTCASES_PATH = ROOT / "game" / "testcases.rpy"
EVIDENCE_PATH = ROOT / "production" / "qa" / "evidence" / "day7-authored-source-evidence-2026-08-14.md"

EXPECTED_SCENES = (
    "scene_day7_red_well_approach",
    "scene_day7_causal_recall",
    "scene_day7_ending_entry",
)


class Day7AuthoredSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE_PATH.read_text(encoding="utf-8")
        cls.chapter = cls.source.split("label chapter_day7_before_red_well:", 1)[1]
        cls.baseline = BASELINE_PATH.read_text(encoding="utf-8")
        cls.generation = SOURCE_GENERATION_PATH.read_text(encoding="utf-8")
        cls.testcases = TESTCASES_PATH.read_text(encoding="utf-8")
        cls.evidence = EVIDENCE_PATH.read_text(encoding="utf-8")

    def test_source_declares_exactly_the_canonical_unit_and_three_scenes(self):
        self.assertEqual(1, self.source.count("label chapter_day7_before_red_well:"))
        self.assertEqual(
            ("chapter_day7_before_red_well",),
            tuple(re.findall(r"^label\s+([a-z0-9_]+):", self.source, re.MULTILINE)),
        )
        self.assertIn("DAY7_CHOICE_RECORDS = ()", self.source)
        for scene_id in EXPECTED_SCENES:
            self.assertIn(scene_id, self.source)
            self.assertIn("`{}`".format(scene_id), self.baseline)

    def test_chapter_acknowledges_only_prior_visible_facts_without_new_semantics(self):
        self.assertIn('current_chapter = "day7"', self.chapter)
        self.assertNotIn("default ", self.source)
        self.assertNotIn("menu:", self.chapter)
        self.assertNotIn("apply_choice(", self.chapter)
        for forbidden in (
            "semantic_state",
            "axis",
            "repair",
            "revoke",
            "qualification",
            "resource_",
            "persistent",
            "commit_ending_",
            "ENDING_LABEL_MAP",
        ):
            self.assertNotIn(forbidden, self.chapter)
        self.assertIn("前六日", self.chapter)
        self.assertIn("已经发生的事", self.chapter)
        self.assertNotIn("分数", self.chapter)
        self.assertNotIn("资格", self.chapter)
        self.assertNotIn("结局", self.chapter)

    def test_only_owned_terminal_handoff_occurs_once_after_all_scenes(self):
        self.assertEqual(1, self.chapter.count("jump day7_resolve_ending"))
        self.assertNotIn("call ", self.chapter)
        self.assertNotIn("return", self.chapter)
        handoff_index = self.chapter.index("jump day7_resolve_ending")
        for scene_id in EXPECTED_SCENES:
            self.assertLess(self.chapter.index(scene_id), handoff_index)
        self.assertNotIn("from modules.ending", self.source)
        self.assertNotIn("import ending", self.source)

    def test_player_safe_catalog_is_bound_to_the_current_source_generation(self):
        self.assertIn("DAY7_PLAYER_SAFE_CATALOG_INPUTS", self.source)
        self.assertIn('"catalog_id": "chapter_day7_before_red_well"', self.source)
        self.assertIn('"catalog_id": "memory_days1_to6_causal_recall"', self.source)
        self.assertIn('"fact_days1_to6_acknowledged"', self.source)
        self.assertIn("DAY7_SOURCE_SHA256", self.source)
        self.assertNotRegex(self.source, r'"(?:score|token|qualification|predicate|cause|ending_hint)')
        recorded = re.search(r'^DAY7_SOURCE_SHA256 = "([0-9a-f]{64})"$', self.generation, re.MULTILINE)
        self.assertIsNotNone(recorded)
        self.assertEqual(hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest(), recorded.group(1))
        self.assertIn(recorded.group(1), self.evidence)
        self.assertIn("game/", self.evidence)

    def test_engine_testcase_uses_the_owned_handoff_not_a_terminal_double(self):
        block = self.testcases.split("testcase day7_authored_handoff_rain_stops:", 1)[1]
        self.assertIn('run Jump("chapter_day7_before_red_well")', block)
        self.assertIn('advance until "雨停在窗外。"', block)
        self.assertIn('assert eval ending_flow_state == "Ended"', block)
        self.assertIn('assert eval pending_ending_id == "ending.rain_stops"', block)
        self.assertNotIn("_day7_terminal_double", block.split("testcase ", 1)[0])

    def test_engine_failure_case_calls_the_real_pre_entry_boundary(self):
        helper = self.testcases.split("def _capture_day7_failed_handoff(failure_kind):", 1)[1].split(
            "def _stage_s7_ending_label", 1
        )[0]
        self.assertIn("prepare_day7_ending_jump()", helper)
        self.assertIn("except (TypeError, ValueError):", helper)
        self.assertIn("ending_flow_state", helper)
        self.assertIn("pending_ending_id", helper)
        self.assertIn("ending_completion_event_record", helper)
        block = self.testcases.split("testcase day7_authored_handoff_failure_closure:", 1)[1]
        self.assertIn('run Function(_capture_day7_failed_handoff, "type")', block)
        self.assertIn('run Function(_capture_day7_failed_handoff, "value")', block)
        self.assertIn('("Active", None, None, (), (), (), ())', block)


if __name__ == "__main__":
    unittest.main()
