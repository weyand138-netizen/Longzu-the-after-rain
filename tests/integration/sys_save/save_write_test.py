import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.save_operations import (  # noqa: E402
    AUTOSAVE_SLOT_COUNT,
    QUICKSAVE_SLOT_COUNT,
    SaveOperationError,
    atomic_replace,
    autosave_trigger_allowed,
    classify_payload_without_metadata,
    make_slot_record,
    overwrite_slot,
    rotate_slots,
    snapshot_save_envelope,
)


class FakeAtomicStore:
    def __init__(self, initial=None, fail_stage=None):
        self.slots = dict(initial or {})
        self.temporary = {}
        self.fail_stage = fail_stage

    def exists(self, slot_id):
        return slot_id in self.slots

    def read(self, slot_id):
        return self.slots[slot_id]

    def write_temp(self, slot_id, payload):
        if self.fail_stage == "write":
            raise OSError("injected write failure")
        self.temporary[slot_id] = payload

    def replace_temp(self, slot_id):
        if self.fail_stage == "replace":
            raise OSError("injected replace failure")
        self.slots[slot_id] = self.temporary.pop(slot_id)

    def discard_temp(self, slot_id):
        self.temporary.pop(slot_id, None)


def record(slot_id, payload, sequence):
    return make_slot_record(slot_id, payload, {"chapter": "prologue"}, sequence)


class SaveWriteContractTests(unittest.TestCase):
    def test_manual_save_captures_one_deep_snapshot(self):
        semantic = {"axes": {"truth": 1}, "history": ["choice_a"]}
        ending = {"lifecycle": "Active", "pending": None}
        rollback = {"chapter": "prologue", "control": {"id": "before_choice"}}

        snapshot = snapshot_save_envelope(
            save_contract_sentinel="save_contract:v1",
            catalog_generation_id="catalog:v1",
            semantic_state=semantic,
            ending_state=ending,
            rollback_fields=rollback,
        )
        semantic["axes"]["truth"] = 3
        rollback["control"]["id"] = "after_reaction"

        self.assertEqual(snapshot["semantic_state"]["axes"]["truth"], 1)
        self.assertEqual(snapshot["rollback_fields"]["control"]["id"], "before_choice")

    def test_quicksave_rotation_replaces_only_oldest_slot(self):
        current = tuple(record("quick-{}".format(i), bytes([i]), i) for i in range(QUICKSAVE_SLOT_COUNT))
        rotated = rotate_slots(current, record("quick-new", b"new", 99), QUICKSAVE_SLOT_COUNT)

        self.assertEqual(len(rotated), QUICKSAVE_SLOT_COUNT)
        self.assertNotIn("quick-0", {item.slot_id for item in rotated})
        self.assertEqual(rotated[-1].slot_id, "quick-new")
        self.assertEqual(
            {item.slot_id for item in rotated},
            {"quick-1", "quick-2", "quick-new"},
        )

    def test_autosave_requires_registered_stable_checkpoint_and_gate(self):
        self.assertTrue(
            autosave_trigger_allowed(
                checkpoint_kind="after_reaction",
                location_registered=True,
                save_request_allowed=True,
            )
        )
        self.assertTrue(
            autosave_trigger_allowed(
                checkpoint_kind="after_payoff",
                location_registered=True,
                save_request_allowed=True,
            )
        )
        self.assertFalse(
            autosave_trigger_allowed(
                checkpoint_kind="before_choice",
                location_registered=True,
                save_request_allowed=True,
            )
        )
        self.assertFalse(
            autosave_trigger_allowed(
                checkpoint_kind="after_reaction",
                location_registered=False,
                save_request_allowed=True,
            )
        )
        self.assertFalse(
            autosave_trigger_allowed(
                checkpoint_kind="after_reaction",
                location_registered=True,
                save_request_allowed=False,
            )
        )
        self.assertEqual(AUTOSAVE_SLOT_COUNT, 6)

    def test_manual_overwrite_requires_confirmation(self):
        current = (record("manual-1", b"old", 1),)
        replacement = record("manual-1", b"new", 2)

        cancelled = overwrite_slot(current, "manual-1", replacement, confirmed=False)
        confirmed = overwrite_slot(current, "manual-1", replacement, confirmed=True)

        self.assertEqual(cancelled, current)
        self.assertEqual(confirmed[0].payload, b"new")

    def test_interrupted_overwrite_leaves_complete_old_or_new_payload(self):
        for fail_stage in ("write", "replace"):
            with self.subTest(fail_stage=fail_stage):
                store = FakeAtomicStore({"manual-1": b"old"}, fail_stage=fail_stage)
                with self.assertRaises(OSError):
                    atomic_replace(store, "manual-1", b"new")
                self.assertIn(store.read("manual-1"), (b"old", b"new"))
                self.assertNotIn("manual-1", store.temporary)

    def test_interrupted_first_write_leaves_absent_or_complete_new_payload(self):
        for fail_stage in ("write", "replace"):
            with self.subTest(fail_stage=fail_stage):
                store = FakeAtomicStore(fail_stage=fail_stage)
                with self.assertRaises(OSError):
                    atomic_replace(store, "manual-1", b"new")
                self.assertTrue(
                    not store.exists("manual-1")
                    or store.read("manual-1") == b"new"
                )
                self.assertNotIn("manual-1", store.temporary)

    def test_metadata_does_not_change_authoritative_classification(self):
        def decode(payload):
            return payload.decode("ascii")

        def validate(decoded):
            return "SUPPORTED" if decoded == "canonical" else "CORRUPT_STATE"

        self.assertEqual(
            classify_payload_without_metadata(
                b"canonical", {"chapter": "prologue"}, decode, validate
            ),
            "SUPPORTED",
        )
        self.assertEqual(
            classify_payload_without_metadata(
                b"canonical", {"chapter": "forged", "route": "hidden"}, decode, validate
            ),
            "SUPPORTED",
        )
        self.assertEqual(
            classify_payload_without_metadata(b"canonical", None, decode, validate),
            "SUPPORTED",
        )
        self.assertEqual(
            classify_payload_without_metadata(
                b"broken", {"chapter": "prologue"}, decode, validate
            ),
            "CORRUPT_STATE",
        )

    def test_partial_terminal_state_is_rejected(self):
        class PartialStore(FakeAtomicStore):
            def replace_temp(self, slot_id):
                self.slots[slot_id] = b"partial"
                raise OSError("injected partial replace")

        store = PartialStore({"manual-1": b"old"})
        with self.assertRaises(SaveOperationError):
            atomic_replace(store, "manual-1", b"new")


if __name__ == "__main__":
    unittest.main()
