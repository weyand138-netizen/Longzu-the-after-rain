"""S7-02 integration checks for the owned Ren'Py terminal boundary."""

import ast
import sys
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GAME = ROOT / "game"
sys.path.insert(0, str(GAME))

from modules.ending_completion_projection import EndingCompletionEvent  # noqa: E402
from modules.ending_completion_restore import (  # noqa: E402
    ENDING_COMPLETION_EVENT_FIELDS,
)
from modules.ending_rules import ENDING_PRIORITY  # noqa: E402


STATE_SOURCE = ROOT / "game" / "10_state.rpy"


class TerminalLifecycleSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = STATE_SOURCE.read_text(encoding="utf-8")
        cls.python_source = cls.source.split("label day7_resolve_ending:", 1)[0]
        init_block = cls.python_source.split("init python:\n", 1)[1].split(
            "default persistent.sys_persist_state", 1
        )[0]
        cls.tree = ast.parse(textwrap.dedent(init_block))

    def _assigned_literal(self, name):
        for node in self.tree.body:
            if (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == name
            ):
                return ast.literal_eval(node.value)
        self.fail("missing literal assignment: {}".format(name))

    def test_schema2_is_the_only_authoritative_rollback_state(self):
        for legacy_default in (
            "default understanding =",
            "default autonomy =",
            "default truth =",
            "default preparation =",
            "default sacrifice =",
            "default choice_history =",
        ):
            self.assertNotIn(legacy_default, self.source)
        self.assertIn("default semantic_state = None", self.source)
        self.assertIn('"schema_version": 2', self.source)
        self.assertIn('"axes": {axis: 0 for axis in AXES}', self.source)
        self.assertIn('"choice_history": []', self.source)
        self.assertIn('state_schema_sentinel = STATE_SCHEMA_SENTINEL', self.source)
        self.assertIn('ending_flow_sentinel = ENDING_FLOW_SENTINEL', self.source)
        self.assertIn('ending_flow_state = ACTIVE_ENDING_LIFECYCLE', self.source)

    def test_state_adapter_has_the_single_private_snapshot_builder_call(self):
        calls = [
            node
            for node in ast.walk(self.tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "_build_detached_ending_snapshot"
        ]
        self.assertEqual(1, len(calls))
        owner = next(
            node.name
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and any(candidate is calls[0] for candidate in ast.walk(node))
        )
        self.assertEqual("current_ending_snapshot", owner)
        self.assertIn("state = _active_semantic_state()", self.source)
        self.assertIn("axis_values = tuple(state[\"axes\"][axis] for axis in AXES)", self.source)
        self.assertIn("history_ids = tuple(state[\"choice_history\"])", self.source)

    def test_exact_frozen_map_and_single_canonical_resolution_handoff(self):
        expected_pairs = tuple(
            (ending_id, "ending_" + ending_id)
            for ending_id in ENDING_PRIORITY
        )
        self.assertEqual(
            expected_pairs,
            self._assigned_literal("_ENDING_LABEL_MAP_ITEMS"),
        )
        self.assertIn("ENDING_LABEL_MAP = dict(_ENDING_LABEL_MAP_ITEMS)", self.source)
        handoff = self.source.split("def prepare_day7_ending_jump():", 1)[1].split(
            "def commit_ending_entry", 1
        )[0]
        self.assertEqual(1, handoff.count("resolve_ending_record(snapshot)"))
        self.assertIn("pending_ending_id = _pending_id_for(ending_id)", handoff)
        self.assertIn("return ending_labels[ending_id]", handoff)
        self.assertIn("label day7_resolve_ending:", self.source)
        self.assertIn("jump expression _day7_target_label", self.source)
        self.assertIn("label after_load:", self.source)
        self.assertIn("jump ending_resolution_safe_boundary", self.source)
        self.assertIn("$ renpy.full_restart()", self.source)

    def test_completion_event_validation_is_part_of_the_load_safe_boundary(self):
        validator = self.source.split(
            "def validate_ending_completion_state(lifecycle, pending_id, event, root):",
            1,
        )[1].split("def _validate_existing_completion_event", 1)[0]
        self.assertIn("validate_persist_root(root)", validator)
        self.assertIn("Active lifecycle cannot have a completion event", validator)
        self.assertIn("A resolver handoff legitimately stages one of the six pending IDs", validator)
        self.assertIn("completion event requires an Ended lifecycle", validator)
        self.assertIn("completion event does not match the pending ending", validator)
        self.assertIn("completion event lacks durable ending membership", validator)
        after_load = self.source.split("label after_load:", 1)[1].split(
            "label ending_resolution_safe_boundary:", 1
        )[0]
        self.assertIn("validate_ending_completion_state(", after_load)
        self.assertIn("jump ending_resolution_safe_boundary", after_load)

    def test_entry_and_completion_are_the_only_owned_lifecycle_boundaries(self):
        entry = self.source.split("def commit_ending_entry(expected_ending_id):", 1)[1].split(
            "def _replace_persistent_root", 1
        )[0]
        self.assertIn("_active_ending_lifecycle()", entry)
        self.assertIn("ending_flow_state = ENDED_ENDING_LIFECYCLE", entry)
        self.assertNotIn("persistent.", entry)
        completion = self.source.split("def commit_ending_completion(ending_id, completion_checkpoint):", 1)[1].split(
            "def apply_accessibility_settings", 1
        )[0]
        self.assertEqual(1, completion.count("_project_ending_completion("))
        self.assertIn("ending_completion_event_record = event", completion)
        self.assertIn('return "DUPLICATE_NOOP"', completion)
        self.assertEqual(
            tuple(EndingCompletionEvent.__dataclass_fields__),
            ENDING_COMPLETION_EVENT_FIELDS,
        )

    def test_no_legacy_axes_only_resolver_path_remains(self):
        self.assertNotIn("preview_current_ending", self.source)
        self.assertNotIn("resolve_ending(current_axis_snapshot())", self.source)
        self.assertIn("_active_ending_lifecycle()", self.source)
        self.assertIn("axis_deltas do not match the frozen choice projection", self.source)


if __name__ == "__main__":
    unittest.main()
