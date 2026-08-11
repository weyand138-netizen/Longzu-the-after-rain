import unittest
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.control_catalog import CHECKPOINT_KINDS  # noqa: E402
from modules.ending_rules import resolve_ending  # noqa: E402
from modules.restore_semantics import (  # noqa: E402
    ACTIVE_LIFECYCLE,
    ENDED_LIFECYCLE,
    RESTORE_SOURCES,
    LoadedRestoreSession,
    RestoreSemanticsError,
    build_restore_plan,
    canonical_restore_matrix,
    make_loaded_restore_session,
    make_restore_snapshot,
    rollback_loaded_save,
    run_observation_window,
)


class RestoreSemanticsTests(unittest.TestCase):
    def _snapshot(
        self,
        checkpoint_kind="before_choice",
        source="manual",
        lifecycle=ACTIVE_LIFECYCLE,
        pending=None,
        history=("choice.before",),
        axes=None,
    ):
        if axes is None:
            axes = {
                "understanding": 1,
                "autonomy": 0,
                "truth": 0,
                "preparation": 0,
                "sacrifice": 0,
            }
        return make_restore_snapshot(
            source=source,
            checkpoint_kind=checkpoint_kind,
            control_location_id="location." + checkpoint_kind,
            semantic_state={
                "schema_version": 2,
                "axes": axes,
                "choice_history": list(history),
            },
            ending_lifecycle=lifecycle,
            pending_ending_id=pending,
            observation_horizon_id="horizon." + checkpoint_kind,
            target_choice_id="choice.target",
            target_reaction_id="reaction.target",
            target_payoff_id_or_none="payoff.target",
        )

    def _trace(self, snapshot):
        calls = []

        def callback(name):
            def invoke(_snapshot):
                calls.append(name)

            return invoke

        trace = run_observation_window(
            snapshot,
            choice_commit=callback("choice"),
            reaction=callback("reaction"),
            payoff=callback("payoff"),
            resolver=callback("resolver"),
        )
        return trace, calls

    def test_before_choice_restore_starts_one_commit_and_reaction(self):
        trace, calls = self._trace(self._snapshot("before_choice"))
        self.assertEqual(calls, ["choice", "reaction"])
        self.assertEqual(trace.choice_commit_calls, 1)
        self.assertEqual(trace.reaction_calls, 1)
        self.assertEqual(trace.payoff_calls, 0)

    def test_after_reaction_preserves_history_and_axes_without_repeating_commit(self):
        snapshot = self._snapshot("after_reaction")
        trace, calls = self._trace(snapshot)
        self.assertEqual(snapshot.semantic_state["choice_history"], ["choice.before"])
        self.assertEqual(snapshot.semantic_state["axes"]["understanding"], 1)
        self.assertEqual(calls, [])
        self.assertEqual(trace.choice_commit_calls, 0)
        self.assertEqual(trace.reaction_calls, 0)
        self.assertEqual(trace.payoff_calls, 0)

    def test_before_payoff_restore_runs_target_payoff_once(self):
        trace, calls = self._trace(self._snapshot("before_payoff"))
        self.assertEqual(calls, ["payoff"])
        self.assertEqual(trace.choice_commit_calls, 0)
        self.assertEqual(trace.reaction_calls, 0)
        self.assertEqual(trace.payoff_calls, 1)

    def test_after_payoff_restore_does_not_replay_completed_payoff(self):
        trace, calls = self._trace(self._snapshot("after_payoff"))
        self.assertEqual(calls, [])
        self.assertEqual(trace.payoff_calls, 0)

    def test_manual_quick_auto_sources_share_all_twelve_checkpoint_semantics(self):
        matrix = canonical_restore_matrix()
        self.assertEqual(len(matrix), 12)
        self.assertEqual(set(source for source, _kind in matrix), set(RESTORE_SOURCES))
        self.assertEqual(set(kind for _source, kind in matrix), set(CHECKPOINT_KINDS))
        for source, checkpoint_kind in matrix:
            with self.subTest(source=source, checkpoint_kind=checkpoint_kind):
                plan = build_restore_plan(
                    self._snapshot(checkpoint_kind, source=source)
                )
                self.assertEqual(plan.snapshot.source, source)
                self.assertEqual(plan.snapshot.checkpoint_kind, checkpoint_kind)
                self.assertEqual(
                    plan.choice_commit_calls,
                    1 if checkpoint_kind == "before_choice" else 0,
                )
                self.assertEqual(
                    plan.reaction_calls,
                    1 if checkpoint_kind == "before_choice" else 0,
                )
                self.assertEqual(
                    plan.payoff_calls,
                    1 if checkpoint_kind == "before_payoff" else 0,
                )

    def test_repeated_before_payoff_loads_start_independent_observation_windows(self):
        for run in range(3):
            with self.subTest(run=run):
                trace, calls = self._trace(self._snapshot("before_payoff"))
                self.assertEqual(calls, ["payoff"])
                self.assertEqual(trace.payoff_calls, 1)

    def test_ended_snapshot_restores_pending_id_without_resolver_call(self):
        snapshot = self._snapshot(
            "after_payoff",
            lifecycle=ENDED_LIFECYCLE,
            pending="ending.rain_stops",
        )
        trace, calls = self._trace(snapshot)
        self.assertEqual(snapshot.ending_lifecycle, ENDED_LIFECYCLE)
        self.assertEqual(snapshot.pending_ending_id, "ending.rain_stops")
        self.assertEqual(calls, [])
        self.assertEqual(trace.resolver_calls, 0)

    def test_restore_snapshot_detaches_semantic_state_from_input(self):
        semantic_state = {
            "schema_version": 2,
            "axes": {
                "understanding": 1,
                "autonomy": 0,
                "truth": 0,
                "preparation": 0,
                "sacrifice": 0,
            },
            "choice_history": ["choice.before"],
        }
        values = self._snapshot().__dict__.copy()
        values["semantic_state"] = semantic_state
        snapshot = make_restore_snapshot(**values)

        semantic_state["axes"]["understanding"] = 3
        semantic_state["choice_history"].append("choice.after")

        self.assertEqual(snapshot.semantic_state["axes"]["understanding"], 1)
        self.assertEqual(snapshot.semantic_state["choice_history"], ["choice.before"])

    def test_restore_snapshot_semantic_state_is_deeply_immutable(self):
        snapshot = self._snapshot("after_payoff")
        session = make_loaded_restore_session((snapshot,), current_index=0)

        with self.assertRaises(TypeError):
            snapshot.semantic_state["axes"]["truth"] = 3
        with self.assertRaises(TypeError):
            snapshot.semantic_state["choice_history"].append("choice.after")

        result = rollback_loaded_save(session, target_index=0)
        self.assertEqual(result.restored_snapshot.semantic_state["axes"]["truth"], 0)
        self.assertEqual(
            result.restored_snapshot.semantic_state["choice_history"],
            ["choice.before"],
        )

    def test_loaded_session_rejects_direct_mutable_snapshot(self):
        values = self._snapshot("after_payoff").__dict__.copy()
        values["semantic_state"] = {
            "schema_version": 2,
            "axes": {"truth": 0},
            "choice_history": [],
        }
        mutable_snapshot = type(self._snapshot())(**values)

        with self.assertRaises(TypeError):
            make_loaded_restore_session((mutable_snapshot,), current_index=0)

    def test_rollback_across_ending_entry_restores_active_snapshot_and_same_result(self):
        ended = self._snapshot(
            "after_payoff",
            lifecycle=ENDED_LIFECYCLE,
            pending="ending.rain_stops",
            history=("choice.before",),
            axes={
                "understanding": 3,
                "autonomy": 3,
                "truth": 3,
                "preparation": 3,
                "sacrifice": 3,
            },
        )
        active = self._snapshot(
            "after_payoff",
            lifecycle=ACTIVE_LIFECYCLE,
            pending=None,
            history=("choice.before",),
            axes={
                "understanding": 3,
                "autonomy": 3,
                "truth": 3,
                "preparation": 3,
                "sacrifice": 3,
            },
        )
        session = make_loaded_restore_session((active, ended), current_index=1)
        result = rollback_loaded_save(session, target_index=0)
        self.assertEqual(result.restored_snapshot.ending_lifecycle, ACTIVE_LIFECYCLE)
        self.assertIsNone(result.restored_snapshot.pending_ending_id)
        self.assertEqual(result.restored_snapshot.semantic_state, active.semantic_state)
        self.assertEqual(
            resolve_ending(ended.semantic_state["axes"]),
            resolve_ending(result.restored_snapshot.semantic_state["axes"]),
        )
        self.assertEqual(
            resolve_ending(result.restored_snapshot.semantic_state["axes"]),
            "rain_stops",
        )
        self.assertEqual(result.invocation_count, 1)
        self.assertEqual(
            result.restored_snapshot.semantic_state["choice_history"],
            active.semantic_state["choice_history"],
        )

    def test_loaded_save_rollback_never_reaches_pre_load_history(self):
        pre_load = self._snapshot("before_choice", history=("pre.load",))
        loaded_start = self._snapshot("after_reaction", history=("loaded.start",))
        loaded_end = self._snapshot("after_payoff", history=("loaded.end",))
        session = make_loaded_restore_session((loaded_start, loaded_end), current_index=1)
        result = rollback_loaded_save(session, target_index=0)
        self.assertNotEqual(result.restored_snapshot.semantic_state, pre_load.semantic_state)
        self.assertEqual(
            result.restored_snapshot.semantic_state["choice_history"],
            ["loaded.start"],
        )
        self.assertEqual(result.session.snapshots, (loaded_start, loaded_end))

    def test_exhausted_rollback_disables_all_actions_without_invocation_or_mutation(self):
        current = self._snapshot("after_payoff", history=("current",))
        session = make_loaded_restore_session((current,), current_index=0)
        result = rollback_loaded_save(session, target_index=0)
        self.assertIs(result.restored_snapshot, current)
        self.assertEqual(result.action_state.save_allowed, False)
        self.assertEqual(result.action_state.load_allowed, False)
        self.assertEqual(result.action_state.rollback_allowed, False)
        self.assertEqual(result.invocation_count, 0)
        self.assertEqual(result.session, session)

    def test_rollback_to_first_loaded_snapshot_exhausts_all_actions(self):
        first = self._snapshot("after_reaction", history=("first",))
        current = self._snapshot("after_payoff", history=("current",))
        session = make_loaded_restore_session((first, current), current_index=1)

        result = rollback_loaded_save(session, target_index=0)

        self.assertIs(result.restored_snapshot, first)
        self.assertEqual(result.action_state.save_allowed, False)
        self.assertEqual(result.action_state.load_allowed, False)
        self.assertEqual(result.action_state.rollback_allowed, False)
        self.assertEqual(result.invocation_count, 1)

    def test_rollback_rejects_directly_constructed_invalid_session(self):
        current = self._snapshot("after_payoff", history=("current",))

        with self.assertRaises(RestoreSemanticsError):
            rollback_loaded_save(LoadedRestoreSession((current,), 1), 0)

        with self.assertRaises(RestoreSemanticsError):
            rollback_loaded_save(LoadedRestoreSession([current], 0), 0)

    def test_restore_snapshot_requires_exact_schema_and_supported_source(self):
        values = self._snapshot().__dict__.copy()
        values.pop("observation_horizon_id")
        with self.assertRaises(RestoreSemanticsError):
            make_restore_snapshot(**values)

        values = self._snapshot().__dict__.copy()
        values["extra_field"] = "forbidden"
        with self.assertRaises(RestoreSemanticsError):
            make_restore_snapshot(**values)

        with self.assertRaises(RestoreSemanticsError):
            self._snapshot(source="imported")

        active_pending = self._snapshot(
            "after_payoff",
            lifecycle=ACTIVE_LIFECYCLE,
            pending="ending.rain_stops",
        )
        self.assertEqual(active_pending.pending_ending_id, "ending.rain_stops")

        with self.assertRaises(RestoreSemanticsError):
            self._snapshot(
                "after_payoff",
                lifecycle=ACTIVE_LIFECYCLE,
                pending="ending.unknown",
            )

        with self.assertRaises(RestoreSemanticsError):
            self._snapshot(
                "after_payoff",
                lifecycle=ENDED_LIFECYCLE,
                pending="ending.unknown",
            )

        class LifecycleText(str):
            pass

        values = self._snapshot().__dict__.copy()
        values["ending_lifecycle"] = LifecycleText(ACTIVE_LIFECYCLE)
        with self.assertRaises(RestoreSemanticsError):
            make_restore_snapshot(**values)


if __name__ == "__main__":
    unittest.main()
