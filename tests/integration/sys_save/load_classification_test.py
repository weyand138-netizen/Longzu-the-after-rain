import unittest
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.load_classification import (  # noqa: E402
    CORRUPT_STATE,
    EMPTY_SLOT_NOOP,
    INTERNAL_LOAD_VALIDATION_FAILURE,
    LEGACY_INCOMPATIBLE,
    LoadClassificationError,
    SUPPORTED,
    SUPPORTED_ENDING_FLOW_SENTINEL,
    SUPPORTED_SAVE_CONTRACT_SENTINEL,
    SUPPORTED_SEMANTIC_STATE_SENTINEL,
    UNSUPPORTED_CONTROL_LOCATION,
    UNSUPPORTED_VERSION,
    UNREADABLE_SAVE,
    classify_load,
    make_load_preflight_input,
    preflight_load_slot,
)


class LoadClassificationTests(unittest.TestCase):
    def _record(self, **overrides):
        values = {
            "save_contract_sentinel": SUPPORTED_SAVE_CONTRACT_SENTINEL,
            "catalog_generation_id": "catalog:v1",
            "state_schema_sentinel": SUPPORTED_SEMANTIC_STATE_SENTINEL,
            "ending_flow_sentinel": SUPPORTED_ENDING_FLOW_SENTINEL,
            "semantic_state": {"axes": {"truth": 1}},
            "ending_state": {"lifecycle": "Active"},
            "control_location_id": "location.before_choice",
            "checkpoint_kind": "before_choice",
            "catalog_valid": True,
            "source_artifact_match": True,
            "location_match_count": 1,
            "checkpoint_state_coherent": True,
        }
        values.update(overrides)
        return make_load_preflight_input(**values)

    def _classify(self, record, **hooks):
        validators = {
            "semantic_validator": lambda value: True,
            "ending_validator": lambda value: True,
            "location_matcher": lambda value: record.location_match_count,
            "checkpoint_validator": lambda value: True,
        }
        validators.update(hooks)
        return classify_load(record, **validators)

    def test_empty_slot_returns_noop_without_inspection_classifier_or_native_load(self):
        calls = []

        def reader():
            calls.append("reader")
            return self._record()

        def classifier(_record):
            calls.append("classifier")
            raise AssertionError("empty slots must not reach the classifier")

        result = preflight_load_slot(
            "manual-1",
            False,
            detached_reader=reader,
            classifier=classifier,
        )

        self.assertEqual(result.classification, EMPTY_SLOT_NOOP)
        self.assertEqual(result.focus_slot, "manual-1")
        self.assertFalse(result.install_allowed)
        self.assertFalse(result.loaded_scene_allowed)
        self.assertEqual(result.detached_inspection_calls, 0)
        self.assertEqual(result.classifier_calls, 0)
        self.assertEqual(result.native_load_calls, 0)
        self.assertEqual(calls, [])

    def test_unreadable_occupied_container_blocks_before_install(self):
        def reader():
            raise OSError("truncated native save")

        result = preflight_load_slot(
            "manual-1",
            True,
            detached_reader=reader,
        )

        self.assertEqual(result.classification, UNREADABLE_SAVE)
        self.assertFalse(result.install_allowed)
        self.assertFalse(result.loaded_scene_allowed)
        self.assertEqual(result.detached_inspection_calls, 1)
        self.assertEqual(result.classifier_calls, 0)
        self.assertEqual(result.native_load_calls, 0)

    def test_missing_any_required_sentinel_wins_before_all_state_validators(self):
        for field in (
            "save_contract_sentinel",
            "catalog_generation_id",
            "state_schema_sentinel",
            "ending_flow_sentinel",
        ):
            with self.subTest(field=field):
                calls = []
                record = self._record(**{field: None})
                result = self._classify(
                    record,
                    semantic_validator=lambda value: calls.append(("semantic", value)) or False,
                    ending_validator=lambda value: calls.append(("ending", value)) or False,
                    location_matcher=lambda value: calls.append(("location", value)) or 0,
                    checkpoint_validator=lambda value: calls.append(("checkpoint", value)) or False,
                )
                self.assertEqual(result.classification, LEGACY_INCOMPATIBLE)
                self.assertEqual(calls, [])

    def test_unknown_or_wrong_type_version_wins_before_state_validation(self):
        for field, value in (
            ("save_contract_sentinel", "save_contract:v9"),
            ("catalog_generation_id", "catalog:v9"),
            ("state_schema_sentinel", "semantic_state:v9"),
            ("ending_flow_sentinel", "ending_flow:v9"),
            ("save_contract_sentinel", object()),
            ("catalog_generation_id", 1),
            ("state_schema_sentinel", []),
            ("ending_flow_sentinel", {"version": 1}),
        ):
            with self.subTest(field=field, value=repr(value)):
                calls = []
                result = self._classify(
                    self._record(**{field: value}),
                    semantic_validator=lambda value: calls.append("semantic") or True,
                    ending_validator=lambda value: calls.append("ending") or True,
                    location_matcher=lambda value: calls.append("location") or 1,
                )
                self.assertEqual(result.classification, UNSUPPORTED_VERSION)
                self.assertEqual(calls, [])

    def test_catalog_or_source_integrity_failure_precedes_state_validation(self):
        for field in ("catalog_valid", "source_artifact_match"):
            with self.subTest(field=field):
                calls = []
                result = self._classify(
                    self._record(**{field: False}),
                    semantic_validator=lambda value: calls.append("semantic") or True,
                    ending_validator=lambda value: calls.append("ending") or True,
                    location_matcher=lambda value: calls.append("location") or 1,
                )
                self.assertEqual(result.classification, INTERNAL_LOAD_VALIDATION_FAILURE)
                self.assertEqual(calls, [])

    def test_invalid_semantic_or_ending_state_is_corrupt(self):
        semantic_calls = []
        result = self._classify(
            self._record(),
            semantic_validator=lambda value: semantic_calls.append(value) or False,
            ending_validator=lambda value: self.fail("ending validator must not run") or True,
        )
        self.assertEqual(result.classification, CORRUPT_STATE)
        self.assertEqual(len(semantic_calls), 1)

        ending_calls = []
        result = self._classify(
            self._record(),
            semantic_validator=lambda value: True,
            ending_validator=lambda value: ending_calls.append(value) or False,
        )
        self.assertEqual(result.classification, CORRUPT_STATE)
        self.assertEqual(len(ending_calls), 1)

    def test_location_cardinality_has_unsupported_and_internal_outcomes(self):
        self.assertEqual(
            self._classify(self._record(location_match_count=0)).classification,
            UNSUPPORTED_CONTROL_LOCATION,
        )
        self.assertEqual(
            self._classify(self._record(location_match_count=2)).classification,
            INTERNAL_LOAD_VALIDATION_FAILURE,
        )
        self.assertEqual(
            self._classify(self._record(location_match_count=True)).classification,
            INTERNAL_LOAD_VALIDATION_FAILURE,
        )

    def test_checkpoint_incoherence_is_corrupt_and_uses_runtime_validator(self):
        calls = []

        def checkpoint_validator(record):
            calls.append(record.semantic_state)
            return False

        result = self._classify(
            self._record(
                semantic_state={"runtime": "state"},
                checkpoint_state_coherent=True,
            ),
            checkpoint_validator=checkpoint_validator,
        )

        self.assertEqual(result.classification, CORRUPT_STATE)
        self.assertEqual(calls, [{"runtime": "state"}])

    def test_all_required_checks_return_only_supported_and_allow_later_install(self):
        result = self._classify(
            self._record(),
            semantic_validator=lambda value: True,
            ending_validator=lambda value: True,
            location_matcher=lambda record: 1,
            checkpoint_validator=lambda record: True,
        )
        self.assertEqual(result.classification, SUPPORTED)
        self.assertTrue(result.install_allowed)
        self.assertTrue(result.loaded_scene_allowed)

    def test_classifier_internal_validator_failures_are_blocking(self):
        for hook_name in ("semantic_validator", "ending_validator", "location_matcher", "checkpoint_validator"):
            with self.subTest(hook_name=hook_name):
                def explode(_value):
                    raise RuntimeError("injected validator failure")

                hooks = {hook_name: explode}
                result = self._classify(self._record(), **hooks)
                self.assertEqual(result.classification, INTERNAL_LOAD_VALIDATION_FAILURE)

    def test_missing_owner_validators_fail_closed(self):
        result = classify_load(self._record())
        self.assertEqual(result.classification, INTERNAL_LOAD_VALIDATION_FAILURE)

    def test_falsey_callable_validators_are_not_replaced_by_fallbacks(self):
        class FalseyValidator:
            def __init__(self):
                self.calls = []

            def __bool__(self):
                return False

            def __call__(self, value):
                self.calls.append(value)
                return True

        semantic = FalseyValidator()
        ending = FalseyValidator()
        result = self._classify(
            self._record(),
            semantic_validator=semantic,
            ending_validator=ending,
        )
        self.assertEqual(result.classification, SUPPORTED)
        self.assertEqual(len(semantic.calls), 1)
        self.assertEqual(len(ending.calls), 1)

    def test_exact_input_schema_rejects_missing_extra_and_empty_dimensions(self):
        values = self._record().__dict__.copy()
        values.pop("checkpoint_kind")
        with self.assertRaises(LoadClassificationError):
            make_load_preflight_input(**values)

        values = self._record().__dict__.copy()
        values["extra_dimension"] = "forbidden"
        with self.assertRaises(LoadClassificationError):
            make_load_preflight_input(**values)

        self.assertEqual(
            self._classify(self._record(location_match_count=None)).classification,
            INTERNAL_LOAD_VALIDATION_FAILURE,
        )

    def test_preflight_decoded_wrong_shape_is_unreadable_and_never_installed(self):
        result = preflight_load_slot(
            "manual-1",
            True,
            detached_reader=lambda: {"not": "the exact envelope"},
        )
        self.assertEqual(result.classification, UNREADABLE_SAVE)
        self.assertFalse(result.install_allowed)
        self.assertFalse(result.loaded_scene_allowed)
        self.assertEqual(result.classifier_calls, 0)
        self.assertEqual(result.native_load_calls, 0)


if __name__ == "__main__":
    unittest.main()
