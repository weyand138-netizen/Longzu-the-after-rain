"""S7-04 traceability checks for the completed SYS-ENDING contract batch."""

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EPIC = ROOT / "production" / "epics" / "sys-ending" / "EPIC.md"
SPRINT = ROOT / "production" / "sprints" / "sprint-007.md"
STATUS = ROOT / "production" / "sprint-status.yaml"
TR_REGISTRY = ROOT / "docs" / "architecture" / "tr-registry.yaml"
TRACEABILITY = ROOT / "production" / "qa" / "evidence" / "sprint-007-terminal-traceability-2026-08-13.md"
STORY = ROOT / "production" / "epics" / "sys-ending" / "story-004-terminal-validation-and-traceability.md"
READINESS = ROOT / "production" / "qa" / "evidence" / "story-readiness-s7-04-2026-08-13.md"

SOURCES = (
    ROOT / "game" / "modules" / "ending_rules.py",
    ROOT / "game" / "10_state.rpy",
    ROOT / "game" / "chapters" / "endings.rpy",
    ROOT / "tests" / "test_ending_rules.py",
    ROOT / "tests" / "integration" / "sys_ending" / "terminal_lifecycle_source_test.py",
    ROOT / "tests" / "integration" / "sys_ending" / "ending_closure_source_test.py",
    Path(__file__),
)


class TerminalTraceabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.epic = EPIC.read_text(encoding="utf-8")
        cls.sprint = SPRINT.read_text(encoding="utf-8")
        cls.status = STATUS.read_text(encoding="utf-8")
        cls.registry = TR_REGISTRY.read_text(encoding="utf-8")
        cls.traceability = TRACEABILITY.read_text(encoding="utf-8")
        cls.story = STORY.read_text(encoding="utf-8")
        cls.readiness = READINESS.read_text(encoding="utf-8")

    def test_sources_and_exact_hashes_bind_one_terminal_generation(self):
        for source in SOURCES:
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            with self.subTest(source=source.name):
                self.assertIn(digest, self.traceability)

    def test_story_epic_and_sprint_records_agree(self):
        for story_id in ("001", "002", "003"):
            self.assertIn("story-{}".format(story_id), self.epic)
        self.assertRegex(self.epic, r"Story 001.*?\| Complete \|")
        self.assertRegex(self.epic, r"Story 002.*?\| Complete \|")
        self.assertRegex(self.epic, r"Story 003.*?\| Complete \|")
        for sprint_id in ("S7-01", "S7-02", "S7-03"):
            self.assertIsNotNone(
                re.search(r'id: "{}".*?status: complete'.format(sprint_id), self.status, re.DOTALL)
            )
        self.assertIsNotNone(
            re.search(r'id: "S7-04".*?status: (ready|in_progress|complete)', self.status, re.DOTALL)
        )
        self.assertIn("**Status**: Complete", self.story)
        self.assertIn("**Verdict**: READY", self.readiness)

    def test_all_terminal_requirements_have_truthful_evidence_links(self):
        for requirement in (
            "TR-END-001",
            "TR-END-002",
            "TR-END-003",
            "TR-END-004",
            "TR-END-005",
            "TR-END-006",
        ):
            self.assertIn(requirement, self.traceability)
            self.assertIn(requirement, self.registry)
        for evidence in (
            "sprint-007-s7-01-code-review-2026-08-13.md",
            "sprint-007-s7-02-code-review-2026-08-13.md",
            "sprint-007-s7-03-code-review-2026-08-13.md",
            "sprint-007-s7-04-code-review-2026-08-13.md",
            "smoke-sprint-007-2026-08-13.md",
            "qa-signoff-sprint-007-2026-08-13.md",
        ):
            self.assertIn(evidence, self.traceability)

    def test_runtime_root_and_unclaimed_scope_are_explicit(self):
        self.assertFalse((ROOT / "src").exists())
        normalized = " ".join(self.traceability.split())
        self.assertIn("runtime implementation root is `game/`", normalized)
        self.assertIn("no empty `src/` directory", normalized)
        for excluded in (
            "Day 7 authored-content QA",
            "full terminal equivalence-class enumeration",
            "release/package work",
            "project-stage promotion",
        ):
            self.assertIn(excluded, self.traceability)


if __name__ == "__main__":
    unittest.main()
