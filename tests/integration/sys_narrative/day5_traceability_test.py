import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "game" / "chapters" / "day5.rpy"
GENERATION = ROOT / "game" / "modules" / "day5_source_generation.py"
EPIC = ROOT / "production" / "epics" / "sys-narrative" / "EPIC.md"
SPRINT_STATUS = ROOT / "production" / "sprint-status.yaml"
SPRINT = ROOT / "production" / "sprints" / "sprint-004.md"
TRACEABILITY = ROOT / "production" / "qa" / "evidence" / "day5-traceability-2026-08-13.md"
STORY = ROOT / "production" / "epics" / "sys-narrative" / "story-015-day5-traceability.md"
SMOKE = ROOT / "production" / "qa" / "smoke-sprint-004-2026-08-13.md"
QA_SIGNOFF = ROOT / "production" / "qa" / "qa-signoff-sprint-004-2026-08-13.md"


class Day5TraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        cls.generation = GENERATION.read_text(encoding="utf-8")
        cls.epic = EPIC.read_text(encoding="utf-8")
        cls.sprint_status = SPRINT_STATUS.read_text(encoding="utf-8")
        cls.sprint = SPRINT.read_text(encoding="utf-8")
        cls.traceability = TRACEABILITY.read_text(encoding="utf-8")
        cls.story = STORY.read_text(encoding="utf-8")
        cls.smoke = SMOKE.read_text(encoding="utf-8")
        cls.qa_signoff = QA_SIGNOFF.read_text(encoding="utf-8")

    def test_matrix_binds_all_day5_story_source_asset_test_and_qa_paths(self):
        self.assertIn(self.source_hash, self.traceability)
        self.assertIn('DAY5_SOURCE_SHA256 = "{}"'.format(self.source_hash), self.generation)
        for requirement in ("TR-NAR-012", "TR-NAR-013", "TR-NAR-014", "TR-NAR-015"):
            self.assertIn(requirement, self.traceability)
        for path in (
            "story-012-day5-authored-source.md",
            "story-013-day5-asset-admission.md",
            "story-014-day5-content-validation.md",
            "story-015-day5-traceability.md",
            "day5-authored-source-evidence.md",
            "day5-content-validation-2026-08-13-reviewed-verified/record.md",
            "day5_asset_admission_test.py",
            "day5_authored_source_test.py",
            "day5_route_derivation_test.py",
            "day5_content_validation_test.py",
            "day5_traceability_test.py",
            "qa-plan-sprint-004-2026-08-12.md",
            "day5-code-review-2026-08-13.md",
            "smoke-sprint-004-2026-08-13.md",
            "qa-signoff-sprint-004-2026-08-13.md",
        ):
            self.assertIn(path, self.traceability)

    def test_story_and_historical_qa_statuses_agree_after_qa_approval(self):
        for story_id in ("012", "013", "014", "015"):
            self.assertRegex(
                self.epic,
                r"\| {} \| .*? \| .*? \| Complete \|".format(story_id),
            )
        self.assertIn("**Status**: Complete", self.story)
        self.assertIn("## Verdict: APPROVED", self.qa_signoff)
        self.assertIn("# Sprint 4", self.sprint)
        self.assertIn("Day 5", self.sprint)
        self.assertIn("Stories 012-015 are Complete and Sprint", self.traceability)
        self.assertIn("4 is `complete`", self.traceability)

    def test_objective_smoke_and_human_review_close_the_qa_hand_off(self):
        self.assertIn("**Verdict**: PASS", self.smoke)
        self.assertIn("Python 222/222 PASS", self.smoke)
        self.assertIn("37/37 testcases, 345/345 assertions", self.smoke)
        self.assertIn("**Result**: PASS", self.qa_signoff)
        self.assertIn("## Verdict: APPROVED", self.qa_signoff)
        self.assertIn("Sprint 4 is approved for local close-out", self.qa_signoff)

    def test_runtime_root_and_scope_boundary_are_explicit(self):
        normalized = " ".join(self.traceability.split())
        self.assertIn("implementation root is `game/`", normalized)
        self.assertIn("no empty `src/` directory", normalized)
        self.assertIn("does not claim Day 6+", normalized)
        self.assertIn("terminal-witness, ending, epilogue, release, or partial-manifest delivery", normalized)
        self.assertFalse((ROOT / "src").exists(), "The project convention forbids a manufactured empty src root.")


if __name__ == "__main__":
    unittest.main()
