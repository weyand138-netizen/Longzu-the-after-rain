import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "game" / "chapters" / "day6.rpy"
GENERATION = ROOT / "game" / "modules" / "day6_source_generation.py"
EPIC = ROOT / "production" / "epics" / "sys-narrative" / "EPIC.md"
SPRINT_STATUS = ROOT / "production" / "sprint-status.yaml"
SPRINT = ROOT / "production" / "sprints" / "sprint-005.md"
TRACEABILITY = ROOT / "production" / "qa" / "evidence" / "day6-traceability-2026-08-13.md"
STORY = ROOT / "production" / "epics" / "sys-narrative" / "story-019-day6-traceability.md"
SMOKE = ROOT / "production" / "qa" / "smoke-sprint-005-2026-08-13.md"
QA_SIGNOFF = ROOT / "production" / "qa" / "qa-signoff-sprint-005-2026-08-13.md"
REVALIDATION = ROOT / "production" / "qa" / "evidence" / "s7-02-runtime-state-revalidation-2026-08-13.md"


class Day6TraceabilityTests(unittest.TestCase):
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
        cls.revalidation = REVALIDATION.read_text(encoding="utf-8")

    def test_matrix_binds_all_day6_story_source_asset_test_and_qa_paths(self):
        self.assertIn("4571b38e0ad718d7ee0b2c581f4257c98e3f31fc948004408b204c6d3915f99e", self.traceability)
        self.assertIn('DAY6_SOURCE_SHA256 = "{}"'.format(self.source_hash), self.generation)
        self.assertIn(self.source_hash, self.revalidation)
        for requirement in ("TR-NAR-016", "TR-NAR-017", "TR-NAR-018", "TR-NAR-019"):
            self.assertIn(requirement, self.traceability)
        for path in (
            "story-016-day6-authored-source.md",
            "story-017-day6-asset-admission.md",
            "story-018-day6-content-validation.md",
            "story-019-day6-traceability.md",
            "day6-authored-source-evidence.md",
            "day6-content-validation-2026-08-13-final-verified/record.md",
            "day6_asset_admission_test.py",
            "day6_authored_source_test.py",
            "day6_commitment_derivation_test.py",
            "day6_content_validation_test.py",
            "day6_traceability_test.py",
            "qa-plan-sprint-005-2026-08-13.md",
            "day6-code-review-2026-08-13.md",
            "smoke-sprint-005-2026-08-13.md",
            "qa-signoff-sprint-005-2026-08-13.md",
        ):
            self.assertIn(path, self.traceability)

    def test_story_and_sprint_statuses_agree_after_qa_approval(self):
        for story_id in ("016", "017", "018", "019"):
            self.assertRegex(self.epic, r"\| {} \| .*? \| .*? \| Complete \|".format(story_id))
        self.assertIn("**Status**: Complete", self.story)
        for story_id in ("S5-01", "S5-02", "S5-03", "S5-04"):
            self.assertIn(story_id, self.sprint)
        self.assertIn("Stories 016-019 are Complete and", self.traceability)
        self.assertIn("Sprint 5 is `complete`", self.traceability)

    def test_objective_smoke_and_human_review_close_the_qa_hand_off(self):
        self.assertIn("**Verdict**: PASS", self.smoke)
        self.assertIn("Python 242/242 PASS", self.smoke)
        self.assertIn("45/45 testcases, 386/386 assertions", self.smoke)
        self.assertIn("## Verdict: APPROVED", self.qa_signoff)
        self.assertIn("**Result**: PASS", self.qa_signoff)
        self.assertIn("Sprint 5 is approved for local close-out", self.qa_signoff)

    def test_runtime_root_and_scope_boundary_are_explicit(self):
        normalized = " ".join(self.traceability.split())
        self.assertIn("implementation root is `game/`", normalized)
        self.assertIn("no empty `src/` directory", normalized)
        self.assertIn("does not claim Day 7, terminal-witness, ending, epilogue, release, or partial-manifest delivery", normalized)
        self.assertFalse((ROOT / "src").exists(), "The project convention forbids a manufactured empty src root.")


if __name__ == "__main__":
    unittest.main()
