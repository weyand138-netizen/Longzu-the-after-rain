import sys
import unittest
from dataclasses import replace
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.narrative_partial_manifest import (  # noqa: E402
    DAY1_HANDOFF_NODE_ID,
    DAY1_SOURCE_UNIT_ID,
    PARTIAL_ARTIFACT_KIND,
    PARTIAL_MANIFEST_SCHEMA,
    TERMINAL_WITNESS_NOT_APPLICABLE,
    Day1HandoffWitness,
    PartialManifestValidationError,
    build_partial_day1_manifest,
    reject_full_production_promotion,
    replay_day1_handoff_witness,
)


SOURCE_PATH = PROJECT_ROOT / "game" / "chapters" / "day1.rpy"


class Day1FlowManifestTests(unittest.TestCase):
    def build_manifest(self, **overrides):
        return build_partial_day1_manifest(SOURCE_PATH, **overrides)

    def test_builds_a_non_production_partial_day1_manifest(self):
        manifest = self.build_manifest()
        self.assertEqual(PARTIAL_MANIFEST_SCHEMA, manifest.schema)
        self.assertEqual(PARTIAL_ARTIFACT_KIND, manifest.artifact_kind)
        self.assertEqual(DAY1_SOURCE_UNIT_ID, manifest.source_unit_id)
        self.assertFalse(manifest.full_production_manifest)
        self.assertEqual(TERMINAL_WITNESS_NOT_APPLICABLE, manifest.terminal_witness_coverage)

    def test_manifest_binds_the_current_day1_source_hash(self):
        manifest = self.build_manifest()
        self.assertEqual(64, len(manifest.source_hash))
        self.assertEqual(manifest.source_hash, self.build_manifest().source_hash)

    def test_manifest_exact_covers_all_day1_choice_reaction_payoff_identities(self):
        manifest = self.build_manifest()
        self.assertEqual(6, len(manifest.bindings))
        self.assertEqual(
            {"day1_accept_clothing", "day1_choose_safe_clothing", "day1_repair_first_destination", "day1_keep_first_override", "day1_read_food_gesture", "day1_assume_food_consent"},
            {binding.canonical_choice_id for binding in manifest.bindings},
        )
        for binding in manifest.bindings:
            self.assertEqual("reaction_" + binding.canonical_choice_id, binding.immediate_reaction_id)
            self.assertTrue(binding.delayed_payoff_id.startswith("payoff_"))

    def test_manifest_has_only_the_controlled_handoff_successor(self):
        manifest = self.build_manifest()
        self.assertEqual((DAY1_HANDOFF_NODE_ID,), manifest.successor_node_ids)
        self.assertEqual(DAY1_HANDOFF_NODE_ID, manifest.day1_handoff_node_id)
        self.assertNotIn("terminal_entry_id", manifest.__dataclass_fields__)

    def test_stale_hash_fails_without_a_repaired_artifact(self):
        with self.assertRaisesRegex(PartialManifestValidationError, "stale source hash"):
            self.build_manifest(source_hash="0" * 64)

    def test_duplicate_binding_fails_closed(self):
        manifest = self.build_manifest()
        duplicated = tuple(
            (binding.canonical_choice_id, binding.immediate_reaction_id, binding.delayed_payoff_id)
            for binding in manifest.bindings
        ) + (("day1_accept_clothing", "reaction_day1_accept_clothing", "payoff_day1_clothing_day4"),)
        with self.assertRaisesRegex(PartialManifestValidationError, "duplicate"):
            self.build_manifest(records=duplicated)

    def test_unknown_or_generic_binding_fails_closed(self):
        manifest = self.build_manifest()
        altered = list(
            (binding.canonical_choice_id, binding.immediate_reaction_id, binding.delayed_payoff_id)
            for binding in manifest.bindings
        )
        altered[0] = ("day1_unknown", "reaction_day1_unknown", "payoff_generic")
        with self.assertRaisesRegex(PartialManifestValidationError, "exact-match"):
            self.build_manifest(records=tuple(altered))

    def test_future_placeholder_is_rejected(self):
        with self.assertRaisesRegex(PartialManifestValidationError, "forbidden"):
            self.build_manifest(successor_node_ids=("node_future_placeholder",))

    def test_ending_or_terminal_reference_is_rejected(self):
        for forbidden_successor in ("node_ending_rain_stops", "node_terminal_entry"):
            with self.subTest(forbidden_successor=forbidden_successor):
                with self.assertRaisesRegex(PartialManifestValidationError, "forbidden"):
                    self.build_manifest(successor_node_ids=(forbidden_successor,))

    def test_production_to_test_only_edge_is_rejected(self):
        with self.assertRaisesRegex(PartialManifestValidationError, "forbidden"):
            self.build_manifest(successor_node_ids=("node_test_only_handoff",))

    def test_canonical_handoff_witness_replays_to_one_controlled_node(self):
        manifest = self.build_manifest()
        witness = Day1HandoffWitness(
            witness_id="witness_day1_handoff_v1",
            starting_state_id="canonical_prologue_state",
            ordered_choice_history=("day1_accept_clothing", "day1_read_food_gesture"),
            handoff_node_id=DAY1_HANDOFF_NODE_ID,
        )
        self.assertEqual(DAY1_HANDOFF_NODE_ID, replay_day1_handoff_witness(manifest, witness))

    def test_invalid_guard_or_successor_witness_fails_closed(self):
        manifest = self.build_manifest()
        witness = Day1HandoffWitness(
            witness_id="witness_day1_handoff_v1",
            starting_state_id="canonical_prologue_state",
            ordered_choice_history=("day1_repair_first_destination", "day1_read_food_gesture"),
            handoff_node_id=DAY1_HANDOFF_NODE_ID,
        )
        with self.assertRaisesRegex(PartialManifestValidationError, "enabled Day 1"):
            replay_day1_handoff_witness(manifest, witness)

    def test_runtime_scan_and_cfg_enumeration_counts_are_zero(self):
        manifest = self.build_manifest()
        self.assertEqual(0, manifest.runtime_source_scan_count)
        self.assertEqual(0, manifest.runtime_cfg_enumeration_count)

    def test_full_production_or_release_promotion_is_rejected(self):
        with self.assertRaisesRegex(PartialManifestValidationError, "full production gate"):
            reject_full_production_promotion(self.build_manifest())

    def test_mutated_boundary_fields_cannot_claim_full_or_terminal_coverage(self):
        manifest = self.build_manifest()
        full = replace(manifest, full_production_manifest=True)
        terminal = replace(manifest, terminal_witness_coverage="covered")
        self.assertTrue(full.full_production_manifest)
        self.assertEqual("covered", terminal.terminal_witness_coverage)
        with self.assertRaisesRegex(PartialManifestValidationError, "full production gate"):
            reject_full_production_promotion(full)
        with self.assertRaisesRegex(PartialManifestValidationError, "full production gate"):
            reject_full_production_promotion(terminal)


if __name__ == "__main__":
    unittest.main()
