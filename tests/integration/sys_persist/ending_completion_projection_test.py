import unittest

from game.modules.ending_completion_projection import *
from game.modules.persist_schema import build_fresh_persist_root


class EndingCompletionProjectionTests(unittest.TestCase):
    def test_completion_emits_one_durable_event(self):
        root = build_fresh_persist_root()
        calls = []
        result = commit_ending_completion(root, ending_id="rain_stops", checkpoint_id="cp", checkpoint_occurrence_id="occ", catalog_generation_id="catalog:v2", replace_root=lambda value: calls.append(value), flush=lambda: calls.append("flush"))
        self.assertEqual(result.status, "APPLIED_FLUSHED")
        self.assertEqual(result.event.completed_event_id, "ending_completed:rain_stops")
        self.assertEqual(len(calls), 2)
        self.assertEqual(commit_ending_completion({**root, "ending_ids": ["rain_stops"]}, ending_id="rain_stops", checkpoint_id="cp", checkpoint_occurrence_id="occ", catalog_generation_id="catalog:v2", replace_root=lambda _: None, flush=lambda: None).status, "DUPLICATE_NOOP")


if __name__ == "__main__":
    unittest.main()
