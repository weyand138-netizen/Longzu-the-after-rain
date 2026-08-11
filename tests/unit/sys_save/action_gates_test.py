import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from modules.action_gates import (  # noqa: E402
    ACTIONS,
    ALTERNATIVE_INPUT_SOURCE,
    AUTO_SAVE,
    AUTOSAVE_CYCLE_SOURCE,
    BLOCKING_SAFE_FLOW,
    CRITICAL_INTERACTION,
    LOAD_OPERATION,
    LOAD_SLOT,
    LOADED_UNVALIDATED,
    MAIN_MENU,
    MANUAL_SAVE,
    OPERATIONS,
    PHASES,
    PLAYABLE_STABLE,
    PLAYER_FACING_ACTIONS,
    PLAYER_SOURCE,
    QUICK_LOAD,
    QUICK_SAVE,
    ROLLBACK,
    SCRIPT_SOURCE,
    SHORTCUT_SOURCE,
    ActionAdmissionResult,
    OperationMutexState,
    RequestProfile,
    UIActionProfile,
    admit_action_request,
    complete_operation,
    idle_operation_mutex,
    make_request_profile,
    make_ui_action_profile,
    registered_request_matrix,
    save_request_allowed,
    ui_action_affordance,
)


class ProtocolBomb:
    def __init__(self):
        self.calls = []

    def _explode(self, name):
        self.calls.append(name)
        raise AssertionError("protocol dispatch is forbidden: " + name)

    def __bool__(self):
        return self._explode("bool")

    def __eq__(self, other):
        return self._explode("eq")

    def __hash__(self):
        return self._explode("hash")

    def __call__(self):
        return self._explode("call")


class LocalActionGateAdapter:
    """Test adapter that publishes an admitted mutex before callback entry."""

    def __init__(self):
        self.state = idle_operation_mutex()
        self.invocations = []

    def request(self, phase, action, profile, callback=None):
        admission = admit_action_request(
            self.state,
            phase=phase,
            action=action,
            request_profile=profile,
        )
        if admission.admitted is not True:
            return admission
        self.state = admission.mutex_state
        self.invocations.append(action)
        if callback is not None:
            callback()
        return admission

    def complete(self, operation):
        self.state = complete_operation(self.state, operation)


class ActionGateTests(unittest.TestCase):
    def profile(self, action, *, enabled=True, registered=True, source=None):
        if source is None:
            source = AUTOSAVE_CYCLE_SOURCE if action == AUTO_SAVE else PLAYER_SOURCE
        return make_request_profile(
            request_enabled=enabled,
            location_registered=registered,
            source=source,
        )

    def ui_profile(self, action, **overrides):
        values = {
            "request_profile": self.profile(action),
            "visible": True,
            "enabled": True,
            "focusable": True,
        }
        values.update(overrides)
        return make_ui_action_profile(**values)

    def admit(self, state, phase, action, profile=None):
        if profile is None:
            profile = self.profile(action)
        return admit_action_request(
            state,
            phase=phase,
            action=action,
            request_profile=profile,
        )

    def test_request_matrix_exact_for_all_registered_phases_and_actions(self):
        expected = {
            (phase, action): (
                phase == PLAYABLE_STABLE
                or (phase == MAIN_MENU and action in (LOAD_SLOT, QUICK_LOAD))
            )
            for phase in PHASES
            for action in ACTIONS
        }
        rows = registered_request_matrix()
        self.assertEqual(len(rows), len(PHASES) * len(ACTIONS))
        self.assertEqual(len({(phase, action) for phase, action, _ in rows}), len(rows))
        self.assertEqual(
            {(phase, action): allowed for phase, action, allowed in rows},
            expected,
        )
        for phase, action, allowed in rows:
            with self.subTest(phase=phase, action=action):
                profile = self.profile(
                    action,
                    registered=phase == PLAYABLE_STABLE,
                )
                self.assertIs(save_request_allowed(phase, action, profile), allowed)

    def test_playable_stable_supported_save_requests_are_allowed(self):
        for action in (MANUAL_SAVE, QUICK_SAVE, AUTO_SAVE):
            with self.subTest(action=action):
                self.assertIs(
                    save_request_allowed(
                        PLAYABLE_STABLE,
                        action,
                        self.profile(action),
                    ),
                    True,
                )

    def test_autosave_has_permission_without_ui_affordance(self):
        request = self.profile(AUTO_SAVE)
        self.assertIs(save_request_allowed(PLAYABLE_STABLE, AUTO_SAVE, request), True)
        self.assertIs(
            ui_action_affordance(
                PLAYABLE_STABLE,
                AUTO_SAVE,
                UIActionProfile(request, True, True, True),
            ),
            False,
        )

    def test_player_facing_affordance_requires_all_ui_flags(self):
        for phase in PHASES:
            for action in PLAYER_FACING_ACTIONS:
                with self.subTest(phase=phase, action=action):
                    expected = (
                        phase == PLAYABLE_STABLE
                        or (
                            phase == MAIN_MENU
                            and action in (LOAD_SLOT, QUICK_LOAD)
                        )
                    )
                    request = self.profile(
                        action,
                        registered=phase == PLAYABLE_STABLE,
                    )
                    profile = self.ui_profile(
                        action,
                        request_profile=request,
                    )
                    self.assertIs(
                        ui_action_affordance(phase, action, profile),
                        expected,
                    )
        denied_request = self.ui_profile(
            MANUAL_SAVE,
            request_profile=self.profile(MANUAL_SAVE, enabled=False),
        )
        self.assertIs(
            ui_action_affordance(PLAYABLE_STABLE, MANUAL_SAVE, denied_request),
            False,
        )

    def test_each_false_ui_flag_disables_affordance(self):
        for flag in ("visible", "enabled", "focusable"):
            with self.subTest(flag=flag):
                self.assertIs(
                    ui_action_affordance(
                        PLAYABLE_STABLE,
                        MANUAL_SAVE,
                        self.ui_profile(MANUAL_SAVE, **{flag: False}),
                    ),
                    False,
                )

    def test_missing_extra_and_wrong_type_manifest_inputs_fail_closed(self):
        malformed_request_profiles = (
            {"request_enabled": True, "location_registered": True},
            {
                "request_enabled": True,
                "location_registered": True,
                "source": PLAYER_SOURCE,
                "extra": True,
            },
            RequestProfile(1, True, PLAYER_SOURCE),
            RequestProfile(True, 1, PLAYER_SOURCE),
        )
        for profile in malformed_request_profiles:
            with self.subTest(profile_type=type(profile).__name__):
                self.assertIs(
                    save_request_allowed(PLAYABLE_STABLE, MANUAL_SAVE, profile),
                    False,
                )

        malformed_ui_profiles = (
            {"request_profile": self.profile(MANUAL_SAVE)},
            {
                "request_profile": self.profile(MANUAL_SAVE),
                "visible": True,
                "enabled": True,
                "focusable": True,
                "extra": True,
            },
            UIActionProfile(self.profile(MANUAL_SAVE), 1, True, True),
        )
        for profile in malformed_ui_profiles:
            with self.subTest(profile_type=type(profile).__name__):
                self.assertIs(
                    ui_action_affordance(PLAYABLE_STABLE, MANUAL_SAVE, profile),
                    False,
                )

        deleted_request = self.profile(MANUAL_SAVE)
        object.__delattr__(deleted_request, "source")
        self.assertIs(
            save_request_allowed(PLAYABLE_STABLE, MANUAL_SAVE, deleted_request),
            False,
        )
        deleted_ui = self.ui_profile(MANUAL_SAVE)
        object.__delattr__(deleted_ui, "focusable")
        self.assertIs(
            ui_action_affordance(PLAYABLE_STABLE, MANUAL_SAVE, deleted_ui),
            False,
        )
        with self.assertRaises(AttributeError):
            object.__setattr__(self.profile(MANUAL_SAVE), "extra", True)

    def test_wrong_type_values_are_not_coerced_by_truthiness(self):
        bomb = ProtocolBomb()
        for phase, action, profile in (
            (bomb, MANUAL_SAVE, self.profile(MANUAL_SAVE)),
            (PLAYABLE_STABLE, bomb, self.profile(MANUAL_SAVE)),
            (PLAYABLE_STABLE, MANUAL_SAVE, RequestProfile(bomb, True, PLAYER_SOURCE)),
            (PLAYABLE_STABLE, MANUAL_SAVE, RequestProfile(True, bomb, PLAYER_SOURCE)),
            (PLAYABLE_STABLE, MANUAL_SAVE, RequestProfile(True, True, bomb)),
        ):
            with self.subTest(phase_type=type(phase), action_type=type(action)):
                self.assertIs(save_request_allowed(phase, action, profile), False)
        for flag in ("visible", "enabled", "focusable"):
            values = {
                "request_profile": self.profile(MANUAL_SAVE),
                "visible": True,
                "enabled": True,
                "focusable": True,
            }
            values[flag] = bomb
            with self.subTest(ui_protocol_bomb=flag):
                self.assertIs(
                    ui_action_affordance(
                        PLAYABLE_STABLE,
                        MANUAL_SAVE,
                        UIActionProfile(**values),
                    ),
                    False,
                )
        mutex_bomb = OperationMutexState(bomb)
        admission = self.admit(
            mutex_bomb,
            PLAYABLE_STABLE,
            MANUAL_SAVE,
        )
        self.assertIs(admission.admitted, False)
        self.assertEqual(admission.queue_length, 0)
        self.assertEqual(bomb.calls, [])

    def test_unknown_phase_or_action_fails_closed(self):
        state = idle_operation_mutex()
        for phase, action in (
            ("UnknownPhase", MANUAL_SAVE),
            (PLAYABLE_STABLE, "unknown_action"),
        ):
            with self.subTest(phase=phase, action=action):
                result = self.admit(
                    state,
                    phase,
                    action,
                    profile=self.profile(MANUAL_SAVE),
                )
                self.assertEqual(result, ActionAdmissionResult(state, 0, False))

    def test_location_and_request_profile_preconditions_fail_closed(self):
        profiles = (
            self.profile(MANUAL_SAVE, registered=False),
            self.profile(MANUAL_SAVE, source="unsupported"),
            self.profile(MANUAL_SAVE, enabled=False),
        )
        for profile in profiles:
            with self.subTest(profile=profile):
                adapter = LocalActionGateAdapter()
                result = adapter.request(
                    PLAYABLE_STABLE,
                    MANUAL_SAVE,
                    profile,
                )
                self.assertIs(result.admitted, False)
                self.assertEqual(result.queue_length, 0)
                self.assertEqual(adapter.invocations, [])

    def test_critical_interaction_denies_every_source_without_queue(self):
        sources = (
            PLAYER_SOURCE,
            SHORTCUT_SOURCE,
            SCRIPT_SOURCE,
            ALTERNATIVE_INPUT_SOURCE,
        )
        for source in sources:
            for action in PLAYER_FACING_ACTIONS:
                with self.subTest(source=source, action=action):
                    adapter = LocalActionGateAdapter()
                    result = adapter.request(
                        CRITICAL_INTERACTION,
                        action,
                        self.profile(action, source=source),
                    )
                    self.assertIs(result.admitted, False)
                    self.assertEqual(result.queue_length, 0)
                    self.assertIsNone(result.mutex_state.active_operation)
                    self.assertEqual(adapter.invocations, [])

    def test_disallowed_phases_skip_autosave_without_deferred_replay(self):
        adapter = LocalActionGateAdapter()
        for phase in (
            CRITICAL_INTERACTION,
            LOADED_UNVALIDATED,
            BLOCKING_SAFE_FLOW,
        ):
            with self.subTest(phase=phase):
                result = adapter.request(
                    phase,
                    AUTO_SAVE,
                    self.profile(AUTO_SAVE),
                )
                self.assertIs(result.admitted, False)
                self.assertEqual(result.queue_length, 0)
                self.assertEqual(result.mutex_state, adapter.state)
        later = adapter.request(
            PLAYABLE_STABLE,
            AUTO_SAVE,
            self.profile(AUTO_SAVE),
        )
        self.assertIs(later.admitted, True)
        self.assertEqual(adapter.invocations, [AUTO_SAVE])

    def test_mutex_rejects_all_five_by_five_followup_combinations(self):
        action_for_operation = {
            MANUAL_SAVE: MANUAL_SAVE,
            QUICK_SAVE: QUICK_SAVE,
            AUTO_SAVE: AUTO_SAVE,
            LOAD_OPERATION: LOAD_SLOT,
            ROLLBACK: ROLLBACK,
        }
        for active_operation in OPERATIONS:
            with self.subTest(active=active_operation):
                adapter = LocalActionGateAdapter()
                nested_results = []

                def nested_requests():
                    for followup_operation in OPERATIONS:
                        action = action_for_operation[followup_operation]
                        nested_results.append(
                            adapter.request(
                                PLAYABLE_STABLE,
                                action,
                                self.profile(action),
                            )
                        )

                active_action = action_for_operation[active_operation]
                admitted = adapter.request(
                    PLAYABLE_STABLE,
                    active_action,
                    self.profile(active_action),
                    callback=nested_requests,
                )
                self.assertIs(admitted.admitted, True)
                self.assertEqual(adapter.state.active_operation, active_operation)
                self.assertEqual(adapter.invocations, [active_action])
                self.assertEqual(len(nested_results), len(OPERATIONS))
                self.assertTrue(all(result.admitted is False for result in nested_results))
                self.assertTrue(all(result.queue_length == 0 for result in nested_results))
                self.assertTrue(
                    all(
                        result.mutex_state.active_operation == active_operation
                        for result in nested_results
                    )
                )

    def test_mutex_does_not_replay_rejected_requests_after_completion(self):
        adapter = LocalActionGateAdapter()
        first = adapter.request(
            PLAYABLE_STABLE, MANUAL_SAVE, self.profile(MANUAL_SAVE)
        )
        rejected = adapter.request(
            PLAYABLE_STABLE, LOAD_SLOT, self.profile(LOAD_SLOT)
        )
        adapter.complete(MANUAL_SAVE)
        self.assertEqual(adapter.invocations, [MANUAL_SAVE])
        self.assertIs(rejected.admitted, False)
        self.assertEqual(rejected.queue_length, 0)
        self.assertIsNone(adapter.state.active_operation)
        self.assertEqual(adapter.invocations, [MANUAL_SAVE])

    def test_new_request_is_allowed_after_operation_completion(self):
        adapter = LocalActionGateAdapter()
        adapter.request(
            PLAYABLE_STABLE, MANUAL_SAVE, self.profile(MANUAL_SAVE)
        )
        adapter.complete(MANUAL_SAVE)
        second = adapter.request(
            PLAYABLE_STABLE,
            LOAD_SLOT,
            self.profile(LOAD_SLOT),
        )
        self.assertEqual(adapter.invocations, [MANUAL_SAVE, LOAD_SLOT])
        self.assertEqual(second.queue_length, 0)
        self.assertIs(second.admitted, True)
        self.assertEqual(second.mutex_state.active_operation, LOAD_OPERATION)


if __name__ == "__main__":
    unittest.main()
