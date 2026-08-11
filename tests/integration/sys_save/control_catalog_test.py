import unittest
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.control_catalog import (  # noqa: E402
    CATALOG_GENERATION_ID,
    CHECKPOINT_KINDS,
    CatalogValidationError,
    build_control_catalog,
    make_choice_restore_checkpoint_record,
    make_restore_control_location_record,
    make_save_restore_fixture_record,
)


SOURCE_HASHES = {
    "stmt.before_choice": "a" * 64,
    "stmt.after_reaction": "b" * 64,
    "stmt.before_payoff": "c" * 64,
    "stmt.after_payoff": "d" * 64,
}


def _records():
    locations = tuple(
        make_restore_control_location_record(
            control_location_id="location." + kind,
            checkpoint_kind=kind,
            engine_statement_id="stmt." + kind,
            source_artifact_hash=SOURCE_HASHES["stmt." + kind],
            catalog_generation_id=CATALOG_GENERATION_ID,
            action_gate_profile_id="gate." + kind,
            owner_system="SYS-SAVE",
        )
        for kind in CHECKPOINT_KINDS
    )
    fixtures = tuple(
        make_save_restore_fixture_record(
            fixture_id="fixture." + kind,
            choice_checkpoint_record=make_choice_restore_checkpoint_record(
                checkpoint_id="checkpoint." + kind,
                checkpoint_kind=kind,
                control_location_id="location." + kind,
                state_sentinel="semantic_state:v2",
                expected_history=("choice." + kind,),
                expected_axes=(0, 0, 0, 0, 0),
                target_choice_id="choice." + kind,
                target_reaction_id="reaction." + kind,
                target_payoff_id_or_none=None,
                observation_horizon_id="horizon." + kind,
                owner_system="SYS-CHOICE",
            ),
            expected_save_contract_sentinel="save_contract:v1",
            expected_catalog_generation_id=CATALOG_GENERATION_ID,
            expected_ending_sentinel="ending_flow:v1",
            expected_ending_state={"lifecycle": "Active"},
            expected_pending_ending_id=None,
            owner_system="SYS-SAVE",
        )
        for kind in CHECKPOINT_KINDS
    )
    gates = tuple("gate." + kind for kind in CHECKPOINT_KINDS)
    return locations, fixtures, gates


def _build(locations=None, fixtures=None, gates=None):
    default_locations, default_fixtures, default_gates = _records()
    return build_control_catalog(
        tuple(default_locations if locations is None else locations),
        tuple(default_fixtures if fixtures is None else fixtures),
        catalog_generation_id=CATALOG_GENERATION_ID,
        canonical_source_hashes=SOURCE_HASHES,
        action_gate_profile_ids=tuple(default_gates if gates is None else gates),
    )


class ControlCatalogTests(unittest.TestCase):
    def test_four_kinds_and_many_to_one_fixture_coverage_are_valid(self):
        locations, fixtures, gates = _records()
        second = make_save_restore_fixture_record(
            fixture_id="fixture.before_payoff.alt",
            choice_checkpoint_record=make_choice_restore_checkpoint_record(
                checkpoint_id="checkpoint.before_payoff.alt",
                checkpoint_kind="before_payoff",
                control_location_id="location.before_payoff",
                state_sentinel="semantic_state:v2",
                expected_history=("different.prehistory",),
                expected_axes=(1, 0, 0, 0, 0),
                target_choice_id="choice.before_payoff.alt",
                target_reaction_id="reaction.before_payoff.alt",
                target_payoff_id_or_none="payoff.before_payoff.alt",
                observation_horizon_id="horizon.before_payoff.alt",
                owner_system="SYS-CHOICE",
            ),
            expected_save_contract_sentinel="save_contract:v1",
            expected_catalog_generation_id=CATALOG_GENERATION_ID,
            expected_ending_sentinel="ending_flow:v1",
            expected_ending_state={"lifecycle": "Active"},
            expected_pending_ending_id=None,
            owner_system="SYS-SAVE",
        )
        catalog = _build(locations, fixtures + (second,), gates)
        self.assertEqual(set(catalog.production_by_key), {
            ("location." + kind, kind) for kind in CHECKPOINT_KINDS
        })
        self.assertEqual(len(catalog.fixture_records), 5)

    def test_exact_record_factories_reject_missing_extra_and_wrong_types(self):
        with self.assertRaises(CatalogValidationError):
            make_restore_control_location_record(control_location_id="only")
        with self.assertRaises(CatalogValidationError):
            make_choice_restore_checkpoint_record(**{
                "checkpoint_id": "id",
                "checkpoint_kind": "before_choice",
                "control_location_id": "location",
                "state_sentinel": "semantic_state:v2",
                "expected_history": [],
                "expected_axes": (0, 0, 0, 0, 0),
                "target_choice_id": "choice",
                "target_reaction_id": "reaction",
                "target_payoff_id_or_none": None,
                "observation_horizon_id": "horizon",
                "owner_system": "SYS-CHOICE",
                "extra": "forbidden",
            })
        with self.assertRaises(CatalogValidationError):
            make_save_restore_fixture_record(**{
                "fixture_id": "fixture",
                "choice_checkpoint_record": object(),
                "expected_save_contract_sentinel": "save_contract:v1",
                "expected_catalog_generation_id": CATALOG_GENERATION_ID,
                "expected_ending_sentinel": "ending_flow:v1",
                "expected_ending_state": {},
                "expected_pending_ending_id": None,
                "owner_system": "SYS-SAVE",
            })

    def test_orphans_duplicates_and_unresolved_mappings_fail_freeze(self):
        locations, fixtures, gates = _records()
        with self.assertRaises(CatalogValidationError):
            _build(locations, fixtures[:-1], gates)
        with self.assertRaises(CatalogValidationError):
            _build(locations + (locations[0],), fixtures, gates)
        duplicate_statement = make_restore_control_location_record(
            control_location_id="location.other",
            checkpoint_kind="after_reaction",
            engine_statement_id=locations[0].engine_statement_id,
            source_artifact_hash=locations[0].source_artifact_hash,
            catalog_generation_id=CATALOG_GENERATION_ID,
            action_gate_profile_id="gate.after_reaction",
            owner_system="SYS-SAVE",
        )
        with self.assertRaises(CatalogValidationError):
            _build(locations + (duplicate_statement,), fixtures, gates)
        with self.assertRaises(CatalogValidationError):
            _build(locations, fixtures + (fixtures[0],), gates)
        with self.assertRaises(CatalogValidationError):
            _build(locations, fixtures[:-1] + (make_save_restore_fixture_record(
                fixture_id="fixture.orphan",
                choice_checkpoint_record=make_choice_restore_checkpoint_record(
                    checkpoint_id="checkpoint.orphan",
                    checkpoint_kind="before_choice",
                    control_location_id="location.missing",
                    state_sentinel="semantic_state:v2",
                    expected_history=(),
                    expected_axes=(0, 0, 0, 0, 0),
                    target_choice_id="choice.orphan",
                    target_reaction_id="reaction.orphan",
                    target_payoff_id_or_none=None,
                    observation_horizon_id="horizon.orphan",
                    owner_system="SYS-CHOICE",
                ),
                expected_save_contract_sentinel="save_contract:v1",
                expected_catalog_generation_id=CATALOG_GENERATION_ID,
                expected_ending_sentinel="ending_flow:v1",
                expected_ending_state={},
                expected_pending_ending_id=None,
                owner_system="SYS-SAVE",
            ),), gates)

    def test_source_identity_generation_and_file_line_drift_fail(self):
        locations, fixtures, gates = _records()
        with self.assertRaises(CatalogValidationError):
            _build(locations, fixtures, gates[:-1])
        drifted = dict(SOURCE_HASHES)
        drifted["stmt.before_choice"] = "f" * 64
        with self.assertRaises(CatalogValidationError):
            build_control_catalog(
                locations,
                fixtures,
                catalog_generation_id=CATALOG_GENERATION_ID,
                canonical_source_hashes=drifted,
                action_gate_profile_ids=gates,
            )
        with self.assertRaises(CatalogValidationError):
            make_restore_control_location_record(
                control_location_id="location.before_choice",
                checkpoint_kind="before_choice",
                engine_statement_id="script.rpy:42",
                source_artifact_hash=SOURCE_HASHES["stmt.before_choice"],
                catalog_generation_id=CATALOG_GENERATION_ID,
                action_gate_profile_id="gate.before_choice",
                owner_system="SYS-SAVE",
            )

    def test_generation_is_authoritative_and_all_records_match_it(self):
        locations, fixtures, gates = _records()
        catalog = _build(locations, fixtures, gates)
        self.assertEqual(catalog.generation_id, CATALOG_GENERATION_ID)
        bad = list(locations)
        bad[0] = make_restore_control_location_record(
            control_location_id=bad[0].control_location_id,
            checkpoint_kind=bad[0].checkpoint_kind,
            engine_statement_id=bad[0].engine_statement_id,
            source_artifact_hash=bad[0].source_artifact_hash,
            catalog_generation_id="catalog:other",
            action_gate_profile_id=bad[0].action_gate_profile_id,
            owner_system=bad[0].owner_system,
        )
        with self.assertRaises(CatalogValidationError):
            _build(tuple(bad), fixtures, gates)


if __name__ == "__main__":
    unittest.main()
