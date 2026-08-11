init python:
    from modules.action_gates import (
        ALTERNATIVE_INPUT_SOURCE,
        AUTO_SAVE,
        AUTOSAVE_CYCLE_SOURCE,
        CRITICAL_INTERACTION,
        LOAD_SLOT,
        MANUAL_SAVE,
        PLAYABLE_STABLE,
        PLAYER_SOURCE,
        QUICK_SAVE,
        ROLLBACK,
        SCRIPT_SOURCE,
        SHORTCUT_SOURCE,
        admit_action_request,
        complete_operation,
        idle_operation_mutex,
        make_request_profile,
        make_ui_action_profile,
        ui_action_affordance,
    )
    from modules.save_operations import (
        AUTOSAVE_SLOT_COUNT,
        QUICKSAVE_SLOT_COUNT,
        autosave_trigger_allowed,
        snapshot_save_envelope,
    )
    from modules.control_catalog import CATALOG_GENERATION_ID, CHECKPOINT_KINDS
    from modules.load_classification import (
        LEGACY_INCOMPATIBLE,
        SUPPORTED,
        SUPPORTED_ENDING_FLOW_SENTINEL,
        SUPPORTED_SAVE_CONTRACT_SENTINEL,
        SUPPORTED_SEMANTIC_STATE_SENTINEL,
        classify_load,
        make_load_preflight_input,
    )
    from modules.restore_semantics import (
        ACTIVE_LIFECYCLE,
        ENDED_LIFECYCLE,
        build_restore_plan,
        make_loaded_restore_session,
        make_restore_snapshot,
        rollback_loaded_save,
        run_observation_window,
    )
    from modules.ending_completion_restore import (
        DUPLICATE_NOOP,
        classify_completion_replay,
        default_persistent_root,
        make_ending_completion_event_record,
        make_ending_completion_save_snapshot,
        make_persistent_boundary_snapshot,
        persistent_boundary_unchanged,
        restore_ending_completion_snapshot,
    )

    def _load_classification_test_record(**overrides):
        values = {
            "save_contract_sentinel": SUPPORTED_SAVE_CONTRACT_SENTINEL,
            "catalog_generation_id": CATALOG_GENERATION_ID,
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

    def _classify_load_test_record(**overrides):
        return classify_load(
            _load_classification_test_record(**overrides),
            semantic_validator=lambda value: True,
            ending_validator=lambda value: True,
            location_matcher=lambda record: 1,
            checkpoint_validator=lambda record: True,
        )

    def _restore_semantics_test_snapshot(
        checkpoint_kind="before_choice",
        lifecycle=ACTIVE_LIFECYCLE,
        pending=None,
    ):
        return make_restore_snapshot(
            source="manual",
            checkpoint_kind=checkpoint_kind,
            control_location_id="location." + checkpoint_kind,
            semantic_state={"schema_version": 2, "choice_history": ["choice.before"]},
            ending_lifecycle=lifecycle,
            pending_ending_id=pending,
            observation_horizon_id="horizon." + checkpoint_kind,
            target_choice_id="choice.target",
            target_reaction_id="reaction.target",
            target_payoff_id_or_none="payoff.target",
        )

    def _restore_exhaustion_test_result():
        first = _restore_semantics_test_snapshot("after_reaction")
        current = _restore_semantics_test_snapshot("after_payoff")
        session = make_loaded_restore_session((first, current), current_index=1)
        return rollback_loaded_save(session, target_index=0)

    def _restore_observation_trace_test_result():
        calls = []

        def callback(name):
            def invoke(_snapshot):
                calls.append(name)

            return invoke

        trace = run_observation_window(
            _restore_semantics_test_snapshot("before_choice"),
            choice_commit=callback("choice"),
            reaction=callback("reaction"),
            payoff=callback("payoff"),
            resolver=callback("resolver"),
        )
        return trace, calls

    def _ending_completion_restore_test_result():
        event = make_ending_completion_event_record(
            ending_id="rain_stops",
            completed_event_id="ending_completed:rain_stops",
            checkpoint_id="ending.rain_stops.completion",
            checkpoint_occurrence_id="ending.rain_stops.completion:1",
            collection_epoch_id=0,
            catalog_generation_id="catalog:v1",
            stable_completion_boundary=True,
            owner_system="SYS-ENDING",
        )
        pre_persistent = make_persistent_boundary_snapshot(
            default_persistent_root(),
            writer_count=0,
            flush_count=0,
        )
        post_persistent = make_persistent_boundary_snapshot(
            default_persistent_root(ending_ids=("rain_stops",)),
            writer_count=1,
            flush_count=1,
        )
        pre = make_ending_completion_save_snapshot(
            ending_id="rain_stops",
            control_location_id="ending.rain_stops.before_completion",
            ending_lifecycle="Active",
            ending_completion_event_record=None,
            persistent_snapshot=pre_persistent,
            ending_request_count=0,
            resolver_call_count=1,
        )
        post = make_ending_completion_save_snapshot(
            ending_id="rain_stops",
            control_location_id="ending.rain_stops.after_completion",
            ending_lifecycle="Ended",
            ending_completion_event_record=event,
            persistent_snapshot=post_persistent,
            ending_request_count=1,
            resolver_call_count=1,
        )
        restored = restore_ending_completion_snapshot(pre, post_persistent)
        replay = classify_completion_replay(event, restored.persistent_snapshot)
        return restored, replay, post

    def _focused_day2_choice_id():
        """Observe the rendered Day 2 focus target without assigning focus."""

        focused = renpy.display.focus.get_focused()
        for choice_id in ("day1_choice_0", "day1_choice_1", "day1_choice_2"):
            widget = renpy.get_displayable("choice", choice_id)
            if (
                focused is widget
                or getattr(focused, "child", None) is widget
                or getattr(widget, "child", None) is focused
            ):
                return choice_id
        return None

    def _focused_day3_choice_id():
        """Observe the rendered Day 3 focus target without assigning focus."""

        focused = renpy.display.focus.get_focused()
        for choice_id in ("day1_choice_0", "day1_choice_1"):
            widget = renpy.get_displayable("choice", choice_id)
            if (
                focused is widget
                or getattr(focused, "child", None) is widget
                or getattr(widget, "child", None) is focused
            ):
                return choice_id
        return None

    class _ActionGateEngineTestAdapter(NoRollback):
        def __init__(self, phase):
            self.phase = phase
            self.mutex_state = idle_operation_mutex()
            self.invocations = ()
            self.denials = ()
            self.output_channels = ()
            self.last_queue_length = 0
            self.publish_trace()

        def publish_trace(self):
            renpy._story006_action_gate_trace = (
                self.invocations,
                self.denials,
                self.output_channels,
                self.last_queue_length,
                self.mutex_state.active_operation,
            )

        def request(self, action, source, callback=None):
            profile = make_request_profile(
                request_enabled=True,
                location_registered=True,
                source=source,
            )
            admission = admit_action_request(
                self.mutex_state,
                phase=self.phase,
                action=action,
                request_profile=profile,
            )
            self.last_queue_length = admission.queue_length
            if admission.admitted is not True:
                self.denials = self.denials + (action,)
                self.publish_trace()
                return admission

            # Publish the claimed state before the engine callback can re-enter.
            self.mutex_state = admission.mutex_state
            self.invocations = self.invocations + (action,)
            if callback is not None:
                callback()
            self.publish_trace()
            return admission

        def screen_request(self, action, source):
            self.request(action, source)
            return None

        def switch_output_channel(self, channel):
            self.output_channels = self.output_channels + (channel,)
            self.publish_trace()

        def complete(self, operation):
            self.mutex_state = complete_operation(self.mutex_state, operation)
            self.publish_trace()

        def reset(self, phase):
            self.phase = phase
            self.mutex_state = idle_operation_mutex()
            self.invocations = ()
            self.denials = ()
            self.output_channels = ()
            self.last_queue_length = 0
            self.publish_trace()

    _action_gate_surface_adapter = _ActionGateEngineTestAdapter(CRITICAL_INTERACTION)
    _action_gate_reentrant_adapter = None

    def _reset_action_gate_surface_adapter():
        _action_gate_surface_adapter.reset(CRITICAL_INTERACTION)

    def _run_action_gate_reentrant_test():
        global _action_gate_reentrant_adapter
        adapter = _ActionGateEngineTestAdapter(PLAYABLE_STABLE)

        def nested_requests():
            adapter.request(MANUAL_SAVE, PLAYER_SOURCE)
            adapter.request(QUICK_SAVE, SHORTCUT_SOURCE)
            adapter.request(AUTO_SAVE, AUTOSAVE_CYCLE_SOURCE)
            adapter.request(LOAD_SLOT, SCRIPT_SOURCE)
            adapter.request(ROLLBACK, PLAYER_SOURCE)

        adapter.request(MANUAL_SAVE, PLAYER_SOURCE, nested_requests)
        _action_gate_reentrant_adapter = adapter

screen action_gate_quick_key_surface():
    key "K_q" action [
        Function(
            _action_gate_surface_adapter.screen_request,
            QUICK_SAVE,
            SHORTCUT_SOURCE,
        ),
        Return(),
    ]

screen action_gate_v_key_surface():
    key "K_v" action [
        Function(_action_gate_surface_adapter.switch_output_channel, "V"),
        Return(),
    ]

screen action_gate_shift_c_key_surface():
    key "shift_K_c" action [
        Function(
            _action_gate_surface_adapter.switch_output_channel,
            "Shift+C",
        ),
        Return(),
    ]

screen action_gate_alternative_key_surface():
    key "K_a" action [
        Function(
            _action_gate_surface_adapter.screen_request,
            MANUAL_SAVE,
            ALTERNATIVE_INPUT_SOURCE,
        ),
        Return(),
    ]

screen action_gate_unavailable_ui_surface():
    $ unavailable_request = make_request_profile(
        request_enabled=True,
        location_registered=True,
        source=PLAYER_SOURCE,
    )
    $ unavailable_ui = make_ui_action_profile(
        request_profile=unavailable_request,
        visible=True,
        enabled=False,
        focusable=True,
    )
    if ui_action_affordance(
        CRITICAL_INTERACTION,
        MANUAL_SAVE,
        unavailable_ui,
    ):
        textbutton "Unavailable action":
            id "action_gate_unavailable"
            action NullAction()
    key "K_ESCAPE" action Return()

label action_gate_quick_key_label:
    call screen action_gate_quick_key_surface
    return

label action_gate_v_key_label:
    call screen action_gate_v_key_surface
    return

label action_gate_shift_c_key_label:
    call screen action_gate_shift_c_key_surface
    return

label action_gate_alternative_key_label:
    call screen action_gate_alternative_key_surface
    return

label action_gate_unavailable_ui_label:
    call screen action_gate_unavailable_ui_surface
    return

testcase prologue_observe_and_ask:
    description "The observation/autonomy path completes the prologue."

    run Jump("start")
    advance until screen "choice"
    click "先读那张被雨打湿的纸"
    advance until screen "choice"
    click "问她想去哪里"
    advance until screen "choice"
    click "照她选的小站走，即使要多绕一小时"
    advance until screen "choice"
    click "对照红泥，并把追踪方向指给她看"
    advance until screen "chapter_complete"
    assert eval understanding == 1
    assert eval autonomy == 1
    assert eval truth == 1
    assert eval "prologue_read_note" in choice_history
    assert eval "prologue_ask_destination" in choice_history
    assert eval "prologue_accept_destination" in choice_history

testcase prologue_expressive_choices:
    description "Zero-delta safety, route, and promise choices remain recorded."

    run Jump("start")
    advance until screen "choice"
    click "先催她上车，离开这里再说"
    advance until screen "choice"
    click "替她选最快离开市区的路线"
    advance until screen "choice"
    click "告诉绘梨衣：如果出事，我们一起决定"
    advance until screen "chapter_complete"
    assert eval all(value == 0 for value in current_axis_snapshot().values())
    assert eval len(choice_history) == 3
    assert eval "prologue_hurry_to_train" in choice_history
    assert eval "prologue_choose_route" in choice_history
    assert eval "prologue_promise_cost" in choice_history

testcase day1_authored_route_contract:
    description "The authored Day 1 route reaches its receipt-name anchor by keyboard without exposing quick-menu focus during choices."

    run Jump("chapter_day1_her_own_name")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    advance repeat 3
    assert eval "day1_accept_clothing" in choice_history
    assert eval "day1_read_food_gesture" in choice_history

testcase day1_accessibility_visual_baselines:
    description "The Day 1 critical choice records default and 1.5x high-contrast reduced-motion visual baselines."

    # Screenshot comparison uses the physical render surface. Pin it so a
    # previously persisted/resized desktop window cannot invalidate the 720p
    # accessibility baseline.
    # Baselines are silent: a persisted clipboard/self-voicing preference must
    # not draw an engine notification over the tested choice surface.
    run Function(setattr, renpy.game.preferences, "self_voicing", False)
    run Function(renpy.set_physical_size, (1280, 720))
    assert eval renpy.game.preferences.self_voicing is False
    run Function(apply_accessibility_settings, 1.0, False, True, False, False)
    run Jump("chapter_day1_her_own_name")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    screenshot "visual/day1_choice_1280x720_keyboard_silent_reduced_motion.png"

    run Function(apply_accessibility_settings, 1.5, True, True, False, False)
    run Jump("chapter_day1_her_own_name")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    screenshot "visual/day1_choice_1280x720_font_1_5_high_contrast.png"

    run Function(apply_accessibility_settings, 1.0, False, False, False, False)

testcase day2_accept_alias_save_token_route_contract:
    description "The ordinary alias-acceptance path reaches the last-machine handoff by keyboard."

    run Function(reset_run_state)
    run Jump("chapter_day2_two_game_tokens")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_2") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "\u5979\u628a\u624b\u7559\u5728\u6309\u952e\u4e0a\uff0c\u770b\u7740\u6635\u79f0\u5728\u5f00\u573a\u753b\u9762\u91cc\u4eae\u8d77\u6765\u3002"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "\u5979\u628a\u7b2c\u4e8c\u679a\u5e01\u4ea4\u7ed9\u4ed6\u4fdd\u7ba1\uff0c\u7136\u540e\u7528\u7559\u4e0b\u7684\u4e00\u679a\u5e01\u5f00\u59cb\u6e38\u620f\u3002"
    advance repeat 3
    assert eval current_chapter == "day2"
    assert eval choice_history == ["day2_accept_alias", "day2_save_second_token"]

testcase day2_assign_alias_spend_tokens_route_contract:
    description "The ordinary assigned-alias path reaches the last-machine handoff by keyboard."

    run Function(reset_run_state)
    run Jump("chapter_day2_two_game_tokens")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_1")
    keysym "K_RETURN"
    assert "\u5979\u7167\u7740\u65b0\u7684\u540d\u5b57\u6309\u5b8c\u6700\u540e\u4e00\u4e2a\u952e\uff0c\u5374\u628a\u624b\u4ece\u9762\u677f\u4e0a\u79fb\u5f00\u3002"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_1")
    keysym "K_RETURN"
    assert "\u6700\u540e\u4e00\u679a\u5e01\u843d\u8fdb\u673a\u5668\u3002\u5979\u628a\u624b\u653e\u56de\u64cd\u7eb5\u6746\u4e0a\uff0c\u76f4\u5230\u8fd9\u4e00\u5c40\u7684\u97f3\u4e50\u505c\u4e0b\u3002"
    advance repeat 3
    assert eval current_chapter == "day2"
    assert eval choice_history == ["day2_assign_alias", "day2_spend_both_tokens"]

testcase day2_repair_alias_route_contract:
    description "The unresolved-silence repair route is keyboard-operable and resolves its canonical token."

    run Function(reset_run_state)
    run Function(apply_choice, "day1_assume_food_consent", {})
    assert eval has_unresolved_token("token_silence_as_consent") is True
    run Jump("chapter_day2_two_game_tokens")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_2") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_2")
    keysym "K_RETURN"
    assert "\u8def\u660e\u975e\u628a\u8bdd\u6536\u56de\u6765\u3002\u7ed8\u68a8\u8863\u91cd\u65b0\u6572\u4e0b\u81ea\u5df1\u7684\u6635\u79f0\uff0c\u518d\u628a\u5c4f\u5e55\u63a8\u5230\u4ed6\u9762\u524d\u3002"
    advance until screen "choice"
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "\u5979\u628a\u7b2c\u4e8c\u679a\u5e01\u4ea4\u7ed9\u4ed6\u4fdd\u7ba1\uff0c\u7136\u540e\u7528\u7559\u4e0b\u7684\u4e00\u679a\u5e01\u5f00\u59cb\u6e38\u620f\u3002"
    advance repeat 3
    assert eval current_chapter == "day2"
    assert eval has_unresolved_token("token_silence_as_consent") is False
    assert eval choice_history == ["day1_assume_food_consent", "day2_admit_alias_unknown", "day2_save_second_token"]

testcase day2_keyboard_default_focus_and_traversal_contract:
    description "Day 2 surfaces set first focus automatically and traverse by real arrow-key input."

    # These assertions observe screen default focus and player keyboard
    # traversal before the activation that commits the route.
    run Function(reset_run_state)
    run Jump("chapter_day2_two_game_tokens")
    advance until screen "choice"
    pause 0.1
    assert eval _focused_day2_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day2_choice_id() == "day1_choice_1"
    keysym "K_RETURN"
    assert "\u5979\u7167\u7740\u65b0\u7684\u540d\u5b57\u6309\u5b8c\u6700\u540e\u4e00\u4e2a\u952e\uff0c\u5374\u628a\u624b\u4ece\u9762\u677f\u4e0a\u79fb\u5f00\u3002"
    advance until screen "choice"
    pause 0.1
    assert eval _focused_day2_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day2_choice_id() == "day1_choice_1"
    keysym "K_RETURN"
    assert "\u6700\u540e\u4e00\u679a\u5e01\u843d\u8fdb\u673a\u5668\u3002\u5979\u628a\u624b\u653e\u56de\u64cd\u7eb5\u6746\u4e0a\uff0c\u76f4\u5230\u8fd9\u4e00\u5c40\u7684\u97f3\u4e50\u505c\u4e0b\u3002"
    advance repeat 3
    assert eval choice_history == ["day2_assign_alias", "day2_spend_both_tokens"]

    # The conditional third alias choice is reachable from the automatic
    # first focus, with no test-only focus assignment.
    run Function(reset_run_state)
    run Function(apply_choice, "day1_assume_food_consent", {})
    run Jump("chapter_day2_two_game_tokens")
    advance until screen "choice"
    pause 0.1
    assert eval _focused_day2_choice_id() == "day1_choice_0"
    keysym "K_DOWN" repeat 2
    pause 0.1
    assert eval _focused_day2_choice_id() == "day1_choice_2"
    keysym "K_RETURN"
    assert "\u8def\u660e\u975e\u628a\u8bdd\u6536\u56de\u6765\u3002\u7ed8\u68a8\u8863\u91cd\u65b0\u6572\u4e0b\u81ea\u5df1\u7684\u6635\u79f0\uff0c\u518d\u628a\u5c4f\u5e55\u63a8\u5230\u4ed6\u9762\u524d\u3002"
    advance until screen "choice"
    pause 0.1
    assert eval _focused_day2_choice_id() == "day1_choice_0"
    keysym "K_RETURN"
    assert eval choice_history == ["day1_assume_food_consent", "day2_admit_alias_unknown", "day2_save_second_token"]

testcase day2_accessibility_visual_baselines:
    description "Day 2 critical choice surfaces retain keyboard focus and readable silent reduced-motion baselines."

    # The physical surface and silent setting make captures deterministic when
    # a prior run persisted a resized window or self-voicing preference.
    run Function(setattr, renpy.game.preferences, "self_voicing", False)
    run Function(renpy.set_physical_size, (1280, 720))
    assert eval renpy.game.preferences.self_voicing is False
    run Function(apply_accessibility_settings, 1.0, False, True, False, False)
    run Function(reset_run_state)
    run Jump("chapter_day2_two_game_tokens")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    screenshot "visual/day2_alias_1280x720_keyboard_silent_reduced_motion.png"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    screenshot "visual/day2_tokens_1280x720_keyboard_silent_reduced_motion.png"

    run Function(apply_accessibility_settings, 1.5, True, True, False, False)
    run Function(reset_run_state)
    run Jump("chapter_day2_two_game_tokens")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    screenshot "visual/day2_alias_1280x720_font_1_5_high_contrast.png"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    screenshot "visual/day2_tokens_1280x720_font_1_5_high_contrast.png"

    run Function(apply_accessibility_settings, 1.0, False, False, False, False)

testcase day3_share_honor_route_contract:
    description "A Day 2-compatible share-and-honor path reaches the Day 3 handoff by keyboard."

    run Function(reset_run_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Jump("chapter_day3_empty_school")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "\u5979\u628a\u4e09\u5f20\u7eb8\u4e00\u5f20\u5f20\u770b\u5b8c\uff0c\u968f\u540e\u628a\u5b83\u4eec\u53e0\u597d\uff0c\u653e\u5728\u81ea\u5df1\u9762\u524d\u3002"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "\u4ed6\u628a\u6863\u6848\u6536\u5728\u684c\u8fb9\u3002\u8fc7\u4e86\u4e00\u4f1a\u513f\uff0c\u5979\u81ea\u5df1\u628a\u6700\u4e0a\u9762\u90a3\u9875\u91cd\u65b0\u6253\u5f00\u3002"
    assert eval current_chapter == "day3"
    assert eval event_empty_school_trace_confirmed is True
    assert eval cp_day3_empty_school_trace_complete is True
    assert eval agency_day3_truth_pace_request == "event_truth_pace_requested"
    assert eval agency_day3_truth_pace_answer == "event_erii_closes_archive"
    assert eval agency_day3_truth_pace_outcome == "outcome_pause_honored"
    assert eval choice_history == ["day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_honor_pause"]
    advance until screen "choice"
    assert eval current_chapter == "prologue"

testcase day3_share_force_route_contract:
    description "A Day 2-compatible share-and-force path reaches the Day 3 handoff by keyboard."

    run Function(reset_run_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Jump("chapter_day3_empty_school")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "\u5979\u628a\u4e09\u5f20\u7eb8\u4e00\u5f20\u5f20\u770b\u5b8c\uff0c\u968f\u540e\u628a\u5b83\u4eec\u53e0\u597d\uff0c\u653e\u5728\u81ea\u5df1\u9762\u524d\u3002"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_1")
    keysym "K_RETURN"
    assert "\u4ed6\u7ee7\u7eed\u628a\u4f59\u4e0b\u7684\u8bf4\u660e\u5ff5\u5b8c\u3002\u5979\u5411\u540e\u9000\uff0c\u624b\u4ece\u7eb8\u8fb9\u79fb\u5f00\uff0c\u76f4\u5230\u8d70\u5eca\u706f\u5728\u95e8\u7f1d\u91cc\u53d8\u7a84\u3002"
    assert eval current_chapter == "day3"
    assert eval agency_day3_truth_pace_outcome == "outcome_pause_overridden"
    assert eval choice_history == ["day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_force_explanation"]
    advance until screen "choice"
    assert eval current_chapter == "prologue"

testcase day3_hide_honor_route_contract:
    description "A Day 2-compatible withhold-and-honor path reaches the Day 3 handoff by keyboard."

    run Function(reset_run_state)
    run Function(apply_choice, "day2_assign_alias", {})
    run Function(apply_choice, "day2_spend_both_tokens", {"sacrifice": 1})
    run Jump("chapter_day3_empty_school")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_1")
    keysym "K_RETURN"
    assert "\u5979\u542c\u5b8c\u7ed3\u8bba\uff0c\u6ca1\u6709\u63a5\u8fc7\u684c\u4e0a\u7684\u7eb8\uff0c\u53ea\u628a\u624b\u505c\u5728\u684c\u6cbf\u3002"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "\u4ed6\u628a\u6863\u6848\u6536\u5728\u684c\u8fb9\u3002\u8fc7\u4e86\u4e00\u4f1a\u513f\uff0c\u5979\u81ea\u5df1\u628a\u6700\u4e0a\u9762\u90a3\u9875\u91cd\u65b0\u6253\u5f00\u3002"
    assert eval current_chapter == "day3"
    assert eval agency_day3_truth_pace_outcome == "outcome_pause_honored"
    assert eval choice_history == ["day2_assign_alias", "day2_spend_both_tokens", "day3_hide_school_evidence", "day3_honor_pause"]
    advance until screen "choice"
    assert eval current_chapter == "prologue"

testcase day3_hide_force_route_contract:
    description "A Day 2-compatible withhold-and-force path reaches the Day 3 handoff by keyboard."

    run Function(reset_run_state)
    run Function(apply_choice, "day2_assign_alias", {})
    run Function(apply_choice, "day2_spend_both_tokens", {"sacrifice": 1})
    run Jump("chapter_day3_empty_school")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_1")
    keysym "K_RETURN"
    assert "\u5979\u542c\u5b8c\u7ed3\u8bba\uff0c\u6ca1\u6709\u63a5\u8fc7\u684c\u4e0a\u7684\u7eb8\uff0c\u53ea\u628a\u624b\u505c\u5728\u684c\u6cbf\u3002"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_1")
    keysym "K_RETURN"
    assert "\u4ed6\u7ee7\u7eed\u628a\u4f59\u4e0b\u7684\u8bf4\u660e\u5ff5\u5b8c\u3002\u5979\u5411\u540e\u9000\uff0c\u624b\u4ece\u7eb8\u8fb9\u79fb\u5f00\uff0c\u76f4\u5230\u8d70\u5eca\u706f\u5728\u95e8\u7f1d\u91cc\u53d8\u7a84\u3002"
    assert eval current_chapter == "day3"
    assert eval agency_day3_truth_pace_outcome == "outcome_pause_overridden"
    assert eval choice_history == ["day2_assign_alias", "day2_spend_both_tokens", "day3_hide_school_evidence", "day3_force_explanation"]
    advance until screen "choice"
    assert eval current_chapter == "prologue"

testcase day3_keyboard_default_focus_and_traversal_contract:
    description "Day 3 surfaces default focus, traverse by arrows, and expose no quick-menu target."

    run Function(reset_run_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Jump("chapter_day3_empty_school")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day3_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day3_choice_id() == "day1_choice_1"
    keysym "K_RETURN"
    assert "\u5979\u542c\u5b8c\u7ed3\u8bba\uff0c\u6ca1\u6709\u63a5\u8fc7\u684c\u4e0a\u7684\u7eb8\uff0c\u53ea\u628a\u624b\u505c\u5728\u684c\u6cbf\u3002"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day3_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day3_choice_id() == "day1_choice_1"
    keysym "K_RETURN"
    assert "\u4ed6\u7ee7\u7eed\u628a\u4f59\u4e0b\u7684\u8bf4\u660e\u5ff5\u5b8c\u3002\u5979\u5411\u540e\u9000\uff0c\u624b\u4ece\u7eb8\u8fb9\u79fb\u5f00\uff0c\u76f4\u5230\u8d70\u5eca\u706f\u5728\u95e8\u7f1d\u91cc\u53d8\u7a84\u3002"
    assert eval choice_history == ["day2_accept_alias", "day2_save_second_token", "day3_hide_school_evidence", "day3_force_explanation"]

testcase day3_accessibility_visual_baselines:
    description "Day 3 critical choice surfaces retain keyboard focus and readable silent reduced-motion baselines."

    run Function(renpy.set_physical_size, (1280, 720))
    run Function(setattr, renpy.game.preferences, "self_voicing", False)
    assert eval renpy.game.preferences.self_voicing is False
    run Function(apply_accessibility_settings, 1.0, False, True, False, False)
    run Function(reset_run_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Jump("chapter_day3_empty_school")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day3_choice_id() == "day1_choice_0"
    screenshot "visual/day3_evidence_1280x720_keyboard_silent_reduced_motion.png"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day3_choice_id() == "day1_choice_0"
    screenshot "visual/day3_truth_pace_1280x720_keyboard_silent_reduced_motion.png"

    run Function(apply_accessibility_settings, 1.5, True, True, False, False)
    run Function(reset_run_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Jump("chapter_day3_empty_school")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day3_choice_id() == "day1_choice_0"
    screenshot "visual/day3_evidence_1280x720_font_1_5_high_contrast.png"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day3_choice_id() == "day1_choice_0"
    screenshot "visual/day3_truth_pace_1280x720_font_1_5_high_contrast.png"

    run Function(apply_accessibility_settings, 1.0, False, False, False, False)

testcase accessibility_settings_batch_contract:
    description "Accessibility settings accept only the approved scale values and persist one batch."

    run Jump("accessibility_settings_test")
    run Function(apply_accessibility_settings, 1.5, True, True, False, False)
    assert eval persistent.settings["font_scale"] == 1.5
    assert eval persistent.settings["high_contrast"] and persistent.settings["reduced_motion"]
    run Function(apply_accessibility_settings, 1.0, False, False, False, False)

testcase save_write_atomicity_contract:
    description "Save operation helpers preserve snapshot, rotation, overwrite, and metadata boundaries."

    run Function(
        snapshot_save_envelope,
        save_contract_sentinel="save_contract:v1",
        catalog_generation_id="catalog:v1",
        semantic_state={"axes": {"truth": 1}},
        ending_state={"lifecycle": "Active"},
        rollback_fields={"chapter": "prologue"},
    )
    run Function(
        autosave_trigger_allowed,
        checkpoint_kind="after_reaction",
        location_registered=True,
        save_request_allowed=True,
    )
    assert eval AUTOSAVE_SLOT_COUNT == 6
    assert eval QUICKSAVE_SLOT_COUNT == 3
    assert eval config.autosave_slots == 6
    assert eval config.quicksave_slots == 3

testcase control_catalog_contract:
    description "The production checkpoint catalog exposes the four stable kinds and one generation."

    assert eval len(CHECKPOINT_KINDS) == 4
    assert eval CATALOG_GENERATION_ID == "catalog:v1"

testcase load_classification_contract:
    description "Detached load classification rejects legacy state before any loaded scene is allowed."

    assert eval _classify_load_test_record().classification == SUPPORTED
    assert eval _classify_load_test_record(state_schema_sentinel=None).classification == LEGACY_INCOMPATIBLE

testcase restore_semantics_contract:
    description "Stable checkpoint kinds open only their permitted fresh observation actions."

    assert eval build_restore_plan(_restore_semantics_test_snapshot("before_choice")).choice_commit_calls == 1
    assert eval build_restore_plan(_restore_semantics_test_snapshot("before_choice")).reaction_calls == 1
    assert eval build_restore_plan(_restore_semantics_test_snapshot("before_payoff")).payoff_calls == 1
    assert eval build_restore_plan(_restore_semantics_test_snapshot("after_payoff")).payoff_calls == 0
    assert eval build_restore_plan(_restore_semantics_test_snapshot("after_payoff", ENDED_LIFECYCLE, "ending.rain_stops")).resolver_calls == 0

testcase restore_exhaustion_contract:
    description "Loaded-save rollback exhaustion disables all actions after reaching the first snapshot."

    assert eval _restore_exhaustion_test_result().action_state.save_allowed is False
    assert eval _restore_exhaustion_test_result().action_state.load_allowed is False
    assert eval _restore_exhaustion_test_result().action_state.rollback_allowed is False
    assert eval _restore_exhaustion_test_result().invocation_count == 1

testcase restore_observation_window_contract:
    description "Ren'Py traversal invokes the before-choice callbacks in the stable order."

    assert eval _restore_observation_trace_test_result()[1] == ["choice", "reaction"]
    assert eval _restore_observation_trace_test_result()[0].choice_commit_calls == 1
    assert eval _restore_observation_trace_test_result()[0].reaction_calls == 1
    assert eval _restore_observation_trace_test_result()[0].payoff_calls == 0

testcase ending_completion_restore_contract:
    description "Ending completion restores its event/control state without changing persistent membership."

    assert eval _ending_completion_restore_test_result()[0].restored_snapshot.ending_completion_event_record is None
    assert eval _ending_completion_restore_test_result()[0].restored_snapshot.ending_request_count == 0
    assert eval _ending_completion_restore_test_result()[0].resolver_call_count == 0
    assert eval _ending_completion_restore_test_result()[1].status == DUPLICATE_NOOP
    assert eval _ending_completion_restore_test_result()[1].notification_count == 0
    assert eval _ending_completion_restore_test_result()[1].writer_count == 0
    assert eval _ending_completion_restore_test_result()[1].flush_count == 0
    assert eval persistent_boundary_unchanged(
        _ending_completion_restore_test_result()[2].persistent_snapshot,
        _ending_completion_restore_test_result()[1].persistent_snapshot,
    )

testcase action_gate_mutex_contract:
    description "Adapters publish the mutex before callbacks and gate screen/keyboard actions."

    run Function(_run_action_gate_reentrant_test)
    assert eval _action_gate_reentrant_adapter.invocations == (MANUAL_SAVE,)
    assert eval len(_action_gate_reentrant_adapter.denials) == 5
    assert eval _action_gate_reentrant_adapter.last_queue_length == 0
    assert eval _action_gate_reentrant_adapter.mutex_state.active_operation == MANUAL_SAVE

    run Function(_reset_action_gate_surface_adapter)
    run Jump("action_gate_quick_key_label")
    advance until screen "action_gate_quick_key_surface"
    keysym "q"
    assert eval renpy._story006_action_gate_trace[0] == ()
    assert eval QUICK_SAVE in renpy._story006_action_gate_trace[1]
    assert eval renpy._story006_action_gate_trace[3] == 0

    run Function(_reset_action_gate_surface_adapter)
    run Jump("action_gate_v_key_label")
    advance until screen "action_gate_v_key_surface"
    keysym "v"
    assert eval renpy._story006_action_gate_trace[0] == ()
    assert eval renpy._story006_action_gate_trace[2] == ("V",)

    run Function(_reset_action_gate_surface_adapter)
    run Jump("action_gate_shift_c_key_label")
    advance until screen "action_gate_shift_c_key_surface"
    keysym "shift_c"
    assert eval renpy._story006_action_gate_trace[0] == ()
    assert eval renpy._story006_action_gate_trace[2] == ("Shift+C",)

    run Function(_reset_action_gate_surface_adapter)
    run Jump("action_gate_alternative_key_label")
    advance until screen "action_gate_alternative_key_surface"
    keysym "a"
    assert eval renpy._story006_action_gate_trace[0] == ()
    assert eval MANUAL_SAVE in renpy._story006_action_gate_trace[1]
    assert eval renpy._story006_action_gate_trace[3] == 0

    run Jump("action_gate_unavailable_ui_label")
    advance until screen "action_gate_unavailable_ui_surface"
    assert eval renpy.get_displayable(
        "action_gate_unavailable_ui_surface",
        "action_gate_unavailable",
    ) is None
    keysym "K_ESCAPE"
