import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "game" / "chapters" / "day7.rpy"
GENERATION = ROOT / "game" / "modules" / "day7_source_generation.py"
EPIC = ROOT / "production" / "epics" / "sys-narrative" / "EPIC.md"
SPRINT_STATUS = ROOT / "production" / "sprint-status.yaml"
SPRINT = ROOT / "production" / "sprints" / "sprint-006.md"
TRACEABILITY = ROOT / "production" / "qa" / "evidence" / "day7-traceability-2026-08-14.md"
STORY = ROOT / "production" / "epics" / "sys-narrative" / "story-023-day7-traceability.md"
SMOKE = ROOT / "production" / "qa" / "smoke-sprint-006-2026-08-14.md"
QA_SIGNOFF = ROOT / "production" / "qa" / "qa-signoff-sprint-006-2026-08-14.md"
EVIDENCE_REVIEW = ROOT / "production" / "qa" / "evidence-review-sprint-006-2026-08-14.md"


class Day7TraceabilityTests(unittest.TestCase):
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
        cls.evidence_review = EVIDENCE_REVIEW.read_text(encoding="utf-8")

    def test_matrix_binds_all_day7_story_source_asset_test_and_qa_paths(self):
        self.assertEqual(
            "017e1582d1dfcb0b78d4c8f2545b41090f4b6bf24763fdcb59e0f58984f8f214",
            self.source_hash,
        )
        self.assertIn('DAY7_SOURCE_SHA256 = "{}"'.format(self.source_hash), self.generation)
        for requirement in ("TR-NAR-020", "TR-NAR-021", "TR-NAR-022", "TR-NAR-023"):
            self.assertIn(requirement, self.traceability)
        for path in (
            "story-020-day7-authored-source.md",
            "story-021-day7-asset-admission.md",
            "story-022-day7-content-validation.md",
            "story-023-day7-traceability.md",
            "day7-authored-source-evidence-2026-08-14.md",
            "day7-asset-admission-2026-08-14.md",
            "day7-content-validation-2026-08-14-verified/record.md",
            "day7_authored_source_test.py",
            "day7_asset_admission_test.py",
            "day7_content_validation_test.py",
            "day7_traceability_test.py",
            "game/testcases.rpy",
            "run-renpy-day7-evidence.ps1",
            "qa-plan-sprint-006-2026-08-13.md",
            "sprint-006-s6-01-code-review-2026-08-14.md",
            "sprint-006-s6-02-code-review-2026-08-14.md",
            "sprint-006-s6-03-code-review-2026-08-14.md",
            "sprint-006-s6-04-code-review-2026-08-14.md",
            "smoke-sprint-006-2026-08-14.md",
            "qa-signoff-sprint-006-2026-08-14.md",
            "evidence-review-sprint-006-2026-08-14.md",
        ):
            self.assertIn(path, self.traceability)

    def test_story_epic_and_sprint_records_agree_after_qa_approval(self):
        for story_id in ("020", "021", "022", "023"):
            self.assertRegex(self.epic, r"\| {} \| .*? \| .*? \| Complete \|".format(story_id))
        self.assertIn("**Status**: Complete", self.story)
        for story_id in ("S6-01", "S6-02", "S6-03", "S6-04"):
            self.assertIn(story_id, self.sprint)
        normalized = " ".join(self.traceability.split())
        self.assertIn("Stories 020-023 are Complete", normalized)
        self.assertIn("Sprint 6 is `complete`", normalized)
        self.assertIn("status: complete", self.sprint_status)

    def test_objective_smoke_evidence_review_and_approved_qa_close_the_hand_off(self):
        self.assertIn("**Verdict**: PASS", self.smoke)
        self.assertIn("Python 278/278 PASS", self.smoke)
        self.assertIn("56/56 testcases, 474/474 assertions", self.smoke)
        self.assertIn("## Verdict: ADEQUATE", self.evidence_review)
        self.assertIn("## Verdict: APPROVED", self.qa_signoff)
        self.assertIn("**Result**: PASS", self.qa_signoff)
        self.assertIn("Sprint 6 is approved for local close-out", self.qa_signoff)

    def test_runtime_root_and_scope_boundary_are_explicit(self):
        normalized = " ".join(self.traceability.split())
        self.assertIn("implementation root is `game/`", normalized)
        self.assertIn("no empty `src/` directory", normalized)
        self.assertIn(
            "does not claim six-ending prose, completion, epilogue, resolver semantics, qualification enumeration, full-manifest, release, or stage delivery",
            normalized,
        )
        self.assertFalse((ROOT / "src").exists(), "The project convention forbids a manufactured empty src root.")


if __name__ == "__main__":
    unittest.main()
