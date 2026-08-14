import ast
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DAY7_SOURCE = ROOT / "game" / "chapters" / "day7.rpy"
STATE_SOURCE = ROOT / "game" / "10_state.rpy"
TESTCASES = ROOT / "game" / "testcases.rpy"
BASELINE = ROOT / "design" / "narrative" / "seven-day-content-baseline.md"
TRACEABILITY = ROOT / "production" / "qa" / "evidence" / "day7-traceability-2026-08-14.md"
EVIDENCE = ROOT / "production" / "qa" / "evidence" / "day7-content-validation-2026-08-14-verified"
RUN = EVIDENCE / "run-passed"
HISTORICAL_DAY7_SOURCE_SHA256 = "017e1582d1dfcb0b78d4c8f2545b41090f4b6bf24763fdcb59e0f58984f8f214"

WITNESS_IDS = (
    "rain_stops",
    "her_own_name",
    "see_the_sea",
    "one_person_train",
    "golden_cage",
    "unsent_postcard",
)
EXPECTED_CASES = (
    "day7_six_canonical_history_handoffs",
    "day7_authored_handoff_failure_closure",
    "day7_accessibility_visual_baselines",
)
EXPECTED_CAPTURE_HASHES = {
    "day7_causal_recall_1280x720_keyboard_silent_reduced_motion.png": "4a6d8c0726f2da70b4b52c1b1f59f8c7a70378d3c6c0e03bd4d8f23511830182",
    "day7_causal_recall_1280x720_font_1_5_high_contrast.png": "4a6d8c0726f2da70b4b52c1b1f59f8c7a70378d3c6c0e03bd4d8f23511830182",
}


def testcase_block(source, testcase_name):
    return source.split("testcase {}:".format(testcase_name), 1)[1].split("testcase ", 1)[0]


def baseline_witness_cells(source):
    rows = {}
    for line in source.splitlines():
        if not line.startswith("|") or "`witness_" not in line:
            continue
        cells = [cell.strip() for cell in line.split("|")]
        witness_id = cells[1].strip("`").removeprefix("witness_").removesuffix("_v1")
        rows[witness_id] = {
            "history": tuple(cells[2].strip("`").split(" → ")),
            "axes": cells[4].strip("`"),
        }
    return rows


class Day7ContentValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = DAY7_SOURCE.read_text(encoding="utf-8")
        cls.state = STATE_SOURCE.read_text(encoding="utf-8")
        cls.testcases = TESTCASES.read_text(encoding="utf-8")
        cls.baseline = BASELINE.read_text(encoding="utf-8")
        cls.evidence = (EVIDENCE / "record.md").read_text(encoding="utf-8")

    def test_canonical_witnesses_match_the_frozen_baseline_including_golden_cage(self):
        marker = "DAY7_CANONICAL_WITNESSES = "
        literal = self.testcases.split(marker, 1)[1].split("\n    def _setup_day7_canonical_witness", 1)[0]
        witnesses = ast.literal_eval(literal)
        baseline = baseline_witness_cells(self.baseline)
        self.assertEqual(set(WITNESS_IDS), set(witnesses))
        self.assertTrue(set(WITNESS_IDS).issubset(baseline))
        for ending_id in WITNESS_IDS:
            self.assertEqual(baseline[ending_id]["history"], tuple(witnesses[ending_id][0]))
            self.assertEqual(
                baseline[ending_id]["axes"],
                "/".join(str(witnesses[ending_id][1][axis]) for axis in ("understanding", "autonomy", "truth", "preparation", "sacrifice")),
            )
        golden_history = witnesses["golden_cage"][0]
        self.assertIn("day5_replace_erii_response", golden_history)
        self.assertNotIn("day5_honor_erii_response", golden_history)
        self.assertEqual(
            "3/2/3/2/1",
            "/".join(str(witnesses["golden_cage"][1][axis]) for axis in ("understanding", "autonomy", "truth", "preparation", "sacrifice")),
        )

    def test_engine_handoff_covers_all_six_histories_and_fails_closed_without_side_effects(self):
        for testcase_name in EXPECTED_CASES:
            self.assertIn("testcase {}:".format(testcase_name), self.testcases)
        canonical = testcase_block(self.testcases, EXPECTED_CASES[0])
        self.assertEqual(6, canonical.count('run Jump("chapter_day7_before_red_well")'))
        for ending_id in WITNESS_IDS:
            self.assertIn('Function(_setup_day7_canonical_witness, "{}")'.format(ending_id), canonical)
            self.assertIn('pending_ending_id == "ending.{}"'.format(ending_id), canonical)
        failed = testcase_block(self.testcases, EXPECTED_CASES[1])
        failure_helper = self.testcases.split("    def _capture_day7_failed_handoff", 1)[1].split("\n\n    DAY7_CANONICAL_WITNESSES", 1)[0]
        self.assertIn("_capture_day7_failed_handoff", failed)
        self.assertIn("TypeError", failure_helper)
        self.assertIn("ValueError", failure_helper)
        self.assertIn('("Active", None, None, (), (), (), ())', failed)
        self.assertIn("except (TypeError, ValueError):", self.state)
        self.assertIn("jump ending_resolution_safe_boundary", self.state)
        self.assertIn("$ renpy.full_restart()", self.state)
        self.assertEqual(1, self.source.count("jump day7_resolve_ending"))

    def test_accessibility_baselines_and_evidence_bind_the_current_artifacts(self):
        visual = testcase_block(self.testcases, EXPECTED_CASES[2])
        self.assertIn("renpy.set_physical_size, (1280, 720)", visual)
        self.assertIn('setattr, renpy.game.preferences, "self_voicing", False', visual)
        self.assertIn("apply_accessibility_settings, 1.5, True, True, False, False", visual)
        self.assertNotIn("renpy.set_focus", visual)
        for capture_name in EXPECTED_CAPTURE_HASHES:
            self.assertIn(capture_name, visual)

        result = json.loads((RUN / "result.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(HISTORICAL_DAY7_SOURCE_SHA256, result["day7_source_sha256"])
        self.assertIn(hashlib.sha256(DAY7_SOURCE.read_bytes()).hexdigest(), TRACEABILITY.read_text(encoding="utf-8"))
        self.assertEqual(hashlib.sha256(TESTCASES.read_bytes()).hexdigest(), result["testcases_sha256"])
        self.assertEqual(hashlib.sha256((RUN / "stdout.txt").read_bytes()).hexdigest(), result["stdout_sha256"])
        self.assertEqual(hashlib.sha256((RUN / "stderr.txt").read_bytes()).hexdigest(), result["stderr_sha256"])
        self.assertEqual(-1, result["exit_code"])
        self.assertEqual("[rpytest] Status: PASSED ", result["status_line"])
        stdout = (RUN / "stdout.txt").read_bytes()
        self.assertIn(b"Test cases :    56 |    56 passed", stdout)
        self.assertIn(b"Assertions :   474 |   474 passed", stdout)
        for capture_name, expected_hash in EXPECTED_CAPTURE_HASHES.items():
            payload = (RUN / "screenshots" / "visual" / capture_name).read_bytes()
            self.assertEqual(b"\x89PNG\r\n\x1a\n", payload[:8])
            self.assertEqual((1280, 720), tuple(int.from_bytes(value, "big") for value in (payload[16:20], payload[20:24])))
            self.assertEqual(expected_hash, hashlib.sha256(payload).hexdigest())
            self.assertIn(expected_hash, self.evidence)

    def test_scope_is_day7_handoff_only_and_runtime_root_is_game(self):
        normalized = " ".join(self.evidence.split())
        self.assertIn("does not claim six-ending prose, completion, epilogue, resolver semantics, route qualification, release, or human narrative/readability approval", normalized)
        self.assertIn("`game/`; no empty `src/`", self.evidence)
        self.assertNotRegex(self.source.lower(), r"\b(audio|sound|hover|timed|timer|animation|motion)\b")


if __name__ == "__main__":
    unittest.main()
