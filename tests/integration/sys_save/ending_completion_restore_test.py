import unittest
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.ending_completion_restore import (  # noqa: E402
    DUPLICATE_NOOP,
    ENDING_COMPLETION_EVENT_FIELDS,
    EndingCompletionSaveSnapshot,
    EndingCompletionRestoreError,
    classify_completion_replay,
    default_persistent_root,
    make_ending_completion_event_record,
    make_ending_completion_save_snapshot,
    make_persistent_boundary_snapshot,
    persistent_boundary_unchanged,
    restore_ending_completion_snapshot,
)


class EndingCompletionRestoreTests(unittest.TestCase):
    def _persistent(self, ending_ids=(), writer_count=0, flush_count=0):
        return make_persistent_boundary_snapshot(
            default_persistent_root(ending_ids=ending_ids),
            writer_count=writer_count,
            flush_count=flush_count,
        )

    def _event(self):
        return make_ending_completion_event_record(
            ending_id="rain_stops",
            completed_event_id="ending_completed:rain_stops",
            checkpoint_id="ending.rain_stops.completion",
            checkpoint_occurrence_id="ending.rain_stops.completion:1",
            collection_epoch_id=0,
            catalog_generation_id="catalog:v1",
            stable_completion_boundary=True,
            owner_system="SYS-ENDING",
        )

    def _pre_snapshot(self):
        return make_ending_completion_save_snapshot(
            ending_id="rain_stops",
            control_location_id="ending.rain_stops.before_completion",
            ending_lifecycle="Active",
            ending_completion_event_record=None,
            persistent_snapshot=self._persistent(),
            ending_request_count=0,
            resolver_call_count=1,
        )

    def _post_snapshot(self):
        return make_ending_completion_save_snapshot(
            ending_id="rain_stops",
            control_location_id="ending.rain_stops.after_completion",
            ending_lifecycle="Ended",
            ending_completion_event_record=self._event(),
            persistent_snapshot=self._persistent(
                ending_ids=("rain_stops",),
                writer_count=1,
                flush_count=1,
            ),
            ending_request_count=1,
            resolver_call_count=1,
        )

    def test_pre_completion_restore_has_no_event_or_request_and_does_not_resolve(self):
        pre = self._pre_snapshot()
        post = self._post_snapshot()

        result = restore_ending_completion_snapshot(pre, post.persistent_snapshot)

        self.assertIsNone(result.restored_snapshot.ending_completion_event_record)
        self.assertEqual(result.restored_snapshot.ending_lifecycle, "Active")
        self.assertEqual(result.restored_snapshot.ending_request_count, 0)
        self.assertEqual(
            result.restored_snapshot.control_location_id,
            "ending.rain_stops.before_completion",
        )
        self.assertEqual(result.resolver_call_count, 0)
        self.assertTrue(
            persistent_boundary_unchanged(post.persistent_snapshot, result.persistent_snapshot)
        )

    def test_post_completion_restore_preserves_exact_event_and_control_location(self):
        post = self._post_snapshot()
        result = restore_ending_completion_snapshot(post, post.persistent_snapshot)
        event = result.restored_snapshot.ending_completion_event_record

        self.assertEqual(tuple(event.__dataclass_fields__), ENDING_COMPLETION_EVENT_FIELDS)
        self.assertEqual(event.ending_id, "rain_stops")
        self.assertEqual(event.completed_event_id, "ending_completed:rain_stops")
        self.assertEqual(event.checkpoint_id, "ending.rain_stops.completion")
        self.assertEqual(event.checkpoint_occurrence_id, "ending.rain_stops.completion:1")
        self.assertEqual(event.collection_epoch_id, 0)
        self.assertEqual(event.catalog_generation_id, "catalog:v1")
        self.assertIs(event.stable_completion_boundary, True)
        self.assertEqual(event.owner_system, "SYS-ENDING")
        self.assertEqual(result.restored_snapshot.control_location_id, "ending.rain_stops.after_completion")
        self.assertEqual(result.restored_snapshot.ending_lifecycle, "Ended")
        self.assertEqual(result.resolver_call_count, 0)

    def test_rollback_before_completion_keeps_flushed_membership_and_replay_is_duplicate_noop(self):
        pre = self._pre_snapshot()
        post = self._post_snapshot()
        restored = restore_ending_completion_snapshot(pre, post.persistent_snapshot)
        replay = classify_completion_replay(post.ending_completion_event_record, restored.persistent_snapshot)

        self.assertEqual(replay.status, DUPLICATE_NOOP)
        self.assertEqual(replay.ending_request_count, 0)
        self.assertEqual(replay.writer_count, 0)
        self.assertEqual(replay.flush_count, 0)
        self.assertEqual(replay.notification_count, 0)
        self.assertEqual(replay.resolver_call_count, 0)
        self.assertTrue(
            persistent_boundary_unchanged(post.persistent_snapshot, replay.persistent_snapshot)
        )
        self.assertEqual(replay.persistent_snapshot.ending_membership, ("rain_stops",))
        self.assertEqual(replay.persistent_snapshot.collection_epoch_id, 0)

    def test_event_record_rejects_wrong_owner_or_completion_reference(self):
        values = self._event().__dict__.copy()
        values["owner_system"] = "SYS-SAVE"
        with self.assertRaises(EndingCompletionRestoreError):
            make_ending_completion_event_record(**values)

    def test_restore_rejects_directly_constructed_malformed_save_snapshot(self):
        persistent = self._persistent()
        malformed = EndingCompletionSaveSnapshot(
            "rain_stops",
            "ending.rain_stops.before_completion",
            "Ended",
            None,
            persistent,
            9,
            0,
        )
        with self.assertRaises(EndingCompletionRestoreError):
            restore_ending_completion_snapshot(malformed, persistent)

    def test_post_completion_requires_one_writer_and_one_flush(self):
        event = self._event()
        persistent = self._persistent(ending_ids=("rain_stops",))
        with self.assertRaises(EndingCompletionRestoreError):
            make_ending_completion_save_snapshot(
                ending_id="rain_stops",
                control_location_id="ending.rain_stops.after_completion",
                ending_lifecycle="Ended",
                ending_completion_event_record=event,
                persistent_snapshot=persistent,
                ending_request_count=1,
                resolver_call_count=1,
            )

        values = self._event().__dict__.copy()
        values["completed_event_id"] = "ending_completed:see_the_sea"
        with self.assertRaises(EndingCompletionRestoreError):
            make_ending_completion_event_record(**values)

    def test_persistent_snapshot_rejects_a_thirteenth_leaf_and_detaches_root(self):
        root = default_persistent_root()
        root["ending_completion_event_record"] = self._event()
        with self.assertRaises(EndingCompletionRestoreError):
            make_persistent_boundary_snapshot(root, writer_count=0, flush_count=0)

        detached_root = default_persistent_root()
        snapshot = make_persistent_boundary_snapshot(
            detached_root,
            writer_count=0,
            flush_count=0,
        )
        detached_root["ending_ids"] = ("rain_stops",)
        self.assertEqual(snapshot.ending_membership, ())
        with self.assertRaises(TypeError):
            snapshot.root["ending_ids"] = ("rain_stops",)


if __name__ == "__main__":
    unittest.main()
