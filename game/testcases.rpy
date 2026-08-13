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

    def _focused_day4_choice_id():
        """Observe a rendered Day 4 focus target without assigning focus."""

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

    def _reset_day4_test_state():
        """Reset Day 4 rollback fields that are not owned by reset_run_state."""

        global event_identity_exposed, event_two_window_tickets_acquired
        global cp_day4_two_tickets_complete, event_contact_risk_handover_complete
        global event_contact_channel_declined, resource_two_tickets
        global resource_single_ticket, resource_contact_card
        global agency_day4_route_preparation_request, agency_day4_route_preparation_answer
        global agency_day4_route_preparation_outcome
        global agency_day4_independent_contact_request, agency_day4_independent_contact_answer
        global agency_day4_independent_contact_outcome, critical_choice_interaction

        event_identity_exposed = False
        event_two_window_tickets_acquired = False
        cp_day4_two_tickets_complete = False
        event_contact_risk_handover_complete = False
        event_contact_channel_declined = False
        resource_two_tickets = False
        resource_single_ticket = False
        resource_contact_card = False
        agency_day4_route_preparation_request = None
        agency_day4_route_preparation_answer = None
        agency_day4_route_preparation_outcome = None
        agency_day4_independent_contact_request = None
        agency_day4_independent_contact_answer = None
        agency_day4_independent_contact_outcome = None
        critical_choice_interaction = False

    def _focused_day5_choice_id():
        """Observe a rendered Day 5 focus target without assigning focus."""

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

    def _reset_day5_test_state():
        """Reset Day 5 rollback fields that are not owned by reset_run_state."""

        global event_full_archive_shared, cp_day5_full_archive_shared
        global event_self_liability_disclosed, event_external_blame_only
        global event_family_response_requested, event_erii_selects_route_response
        global cp_day5_route_answer_expressed, event_route_preference_honored
        global event_route_preference_overridden_to_old_order
        global event_daily_override_unrepaired, event_school_evidence_stays_hidden
        global day5_daily_override_was_unresolved, agency_day5_response_answer
        global agency_day5_response_outcome, agency_day5_response_derivation_record
        global critical_choice_interaction

        event_full_archive_shared = False
        cp_day5_full_archive_shared = False
        event_self_liability_disclosed = False
        event_external_blame_only = False
        event_family_response_requested = False
        event_erii_selects_route_response = False
        cp_day5_route_answer_expressed = False
        event_route_preference_honored = False
        event_route_preference_overridden_to_old_order = False
        event_daily_override_unrepaired = False
        event_school_evidence_stays_hidden = False
        day5_daily_override_was_unresolved = False
        agency_day5_response_answer = None
        agency_day5_response_outcome = None
        agency_day5_response_derivation_record = None
        critical_choice_interaction = False

    def _set_day5_route_facts(
        two_tickets=False,
        contact_card=False,
        contact_handover=False,
        single_ticket=False,
    ):
        """Seed only the closed Day 4 observable route facts for a Day 5 test."""

        global resource_two_tickets, resource_contact_card
        global event_contact_risk_handover_complete, resource_single_ticket

        resource_two_tickets = two_tickets
        resource_contact_card = contact_card
        event_contact_risk_handover_complete = contact_handover
        resource_single_ticket = single_ticket

    def _focused_day6_choice_id():
        """Observe a rendered Day 6 focus target without assigning focus."""

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

    def _reset_day6_test_state():
        """Reset Day 6 and its narrowly projected prologue facts."""

        global resource_service_exit, event_shared_cost_promised
        global event_note_preserved_by_erii, event_safehouse_failed
        global event_achievement_read_note_recovered, cp_day6_note_recovery_complete
        global event_service_exit_used, cp_day6_service_exit_complete
        global event_backup_stays_abandoned, event_family_truth_stays_withheld
        global event_cost_bearer_requested, event_erii_rejects_shifted_cost
        global event_cost_reconsideration_requested, event_erii_rejects_shifted_cost_again
        global event_shared_cost_acknowledged, event_prior_cost_promise_honored_without_shift
        global cp_day6_direct_cost_complete, event_shifted_cost_consequence_visible
        global event_shifted_cost_confirmed, event_independent_route_committed
        global event_shared_route_committed, event_solo_route_committed
        global event_no_continuing_contact_commitment, event_old_order_route_committed
        global event_route_collapse, cp_day6_cost_reconsideration_complete
        global agency_day6_cost_outcome, agency_day6_cost_reconsideration_outcome
        global agency_day6_commitment_derivation_record, agency_day6_commitment_state
        global critical_choice_interaction

        resource_service_exit = False
        event_shared_cost_promised = False
        event_note_preserved_by_erii = False
        event_safehouse_failed = False
        event_achievement_read_note_recovered = False
        cp_day6_note_recovery_complete = False
        event_service_exit_used = False
        cp_day6_service_exit_complete = False
        event_backup_stays_abandoned = False
        event_family_truth_stays_withheld = False
        event_cost_bearer_requested = False
        event_erii_rejects_shifted_cost = False
        event_cost_reconsideration_requested = False
        event_erii_rejects_shifted_cost_again = False
        event_shared_cost_acknowledged = False
        event_prior_cost_promise_honored_without_shift = False
        cp_day6_direct_cost_complete = False
        event_shifted_cost_consequence_visible = False
        event_shifted_cost_confirmed = False
        event_independent_route_committed = False
        event_shared_route_committed = False
        event_solo_route_committed = False
        event_no_continuing_contact_commitment = False
        event_old_order_route_committed = False
        event_route_collapse = False
        cp_day6_cost_reconsideration_complete = False
        agency_day6_cost_outcome = None
        agency_day6_cost_reconsideration_outcome = None
        agency_day6_commitment_derivation_record = None
        agency_day6_commitment_state = None
        critical_choice_interaction = False

    def _set_day6_route_context(answer, outcome, honored, overridden):
        """Seed the closed Day 5 answer/outcome facts for a Day 6 route test."""

        global agency_day5_response_answer, agency_day5_response_outcome
        global event_route_preference_honored, event_route_preference_overridden_to_old_order

        agency_day5_response_answer = answer
        agency_day5_response_outcome = outcome
        event_route_preference_honored = honored
        event_route_preference_overridden_to_old_order = overridden

    def _set_day6_preconditions(service_exit=False, shared_cost_promise=False, preserved_note=False):
        """Seed only the Day 6 facts projected by the frozen prologue scope."""

        global resource_service_exit, event_shared_cost_promised, event_note_preserved_by_erii

        resource_service_exit = service_exit
        event_shared_cost_promised = shared_cost_promise
        event_note_preserved_by_erii = preserved_note

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

testcase day4_two_ticket_contact_register_route_contract:
    description "A Day 3-compatible two-ticket route registers independent contact by keyboard."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_share_school_evidence", {"truth": 1})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Jump("chapter_day4_seaside_train")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_2") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "两张靠窗票落进她掌心。售票员核对姓名时停了一下，路明非知道这会留下被人找到的代价。"
    advance
    assert eval current_chapter == "day4"
    assert eval agency_day4_route_preparation_request == "event_route_preparation_requested"
    assert eval agency_day4_route_preparation_answer == "preserve_executable_self_controlled_option"
    assert eval agency_day4_route_preparation_outcome == "outcome_shared_option_prepared"
    assert eval resource_two_tickets is True
    assert eval event_identity_exposed is True
    assert eval event_two_window_tickets_acquired is True
    assert eval cp_day4_two_tickets_complete is True
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_2") is None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "她自己念出昵称的读法，把游戏币交给窗口后拿走联系人卡，也看完了背面写着的风险。"
    advance
    assert eval agency_day4_independent_contact_request == "event_independent_contact_option_requested"
    assert eval agency_day4_independent_contact_answer == "keep_independent_contact_option"
    assert eval agency_day4_independent_contact_outcome == "outcome_independent_option_prepared"
    assert eval resource_contact_card is True
    assert eval event_contact_risk_handover_complete is True
    assert eval choice_history == ["day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_honor_pause", "day4_buy_two_tickets_real_name", "day4_register_independent_contact"]
    advance until screen "choice"
    assert eval current_chapter == "prologue"

testcase day4_single_ticket_contact_decline_route_contract:
    description "A Day 3-compatible single-ticket route declines independent contact by keyboard."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_hide_school_evidence", {})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Jump("chapter_day4_seaside_train")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_2") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_1")
    keysym "K_RETURN"
    assert "她接过那张票，没有把它塞回他手里，只把路线图折到能一个人展开的那一页。"
    advance
    assert eval agency_day4_route_preparation_outcome == "outcome_solo_option_prepared"
    assert eval resource_single_ticket is True
    assert eval resource_two_tickets is False
    assert eval event_identity_exposed is False
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_1")
    keysym "K_RETURN"
    assert "她把游戏币和写着昵称的纸片收回掌心。她保留了它们，也没有留下能继续联系的号码。"
    advance
    assert eval agency_day4_independent_contact_outcome == "outcome_independent_option_declined"
    assert eval event_contact_channel_declined is True
    assert eval resource_contact_card is False
    assert eval has_unresolved_token("token_abandon_backup_plan") is True
    assert eval choice_history == ["day2_accept_alias", "day2_save_second_token", "day3_hide_school_evidence", "day3_honor_pause", "day4_buy_single_ticket_cash", "day4_decline_independent_contact"]
    advance until screen "choice"
    assert eval current_chapter == "prologue"

testcase day4_no_backup_contact_register_route_contract:
    description "A Day 3-compatible no-backup route still exposes the guarded contact response by keyboard."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(apply_choice, "day2_admit_alias_unknown", {"understanding": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_share_school_evidence", {"truth": 1})
    run Function(apply_choice, "day3_force_explanation", {})
    run Jump("chapter_day4_seaside_train")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_2") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_2")
    keysym "K_RETURN"
    assert "路线图上只剩一条被折出来的线。她把联系人纸片收回袖口，没有替他补上空白。"
    advance
    assert eval agency_day4_route_preparation_outcome == "outcome_self_controlled_option_not_prepared"
    assert eval has_unresolved_token("token_abandon_backup_plan") is True
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    assert eval renpy.get_displayable("choice", "day1_choice_0") is not None
    assert eval renpy.get_displayable("choice", "day1_choice_1") is not None
    run Function(renpy.set_focus, "choice", "day1_choice_0")
    keysym "K_RETURN"
    assert "她自己念出昵称的读法，把游戏币交给窗口后拿走联系人卡，也看完了背面写着的风险。"
    advance
    assert eval agency_day4_independent_contact_outcome == "outcome_independent_option_prepared"
    assert eval resource_contact_card is True
    assert eval event_contact_risk_handover_complete is True
    assert eval choice_history == ["day2_admit_alias_unknown", "day2_save_second_token", "day3_share_school_evidence", "day3_force_explanation", "day4_follow_one_route_no_backup", "day4_register_independent_contact"]
    advance until screen "choice"
    assert eval current_chapter == "prologue"

testcase day4_contact_requires_approved_alias_and_retained_token_contract:
    description "A retained token without an approved alias cannot create a Day 4 contact response."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(apply_choice, "day2_assign_alias", {})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_hide_school_evidence", {})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Jump("chapter_day4_seaside_train")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    run Function(renpy.set_focus, "choice", "day1_choice_2")
    keysym "K_RETURN"
    assert eval agency_day4_independent_contact_request is None
    assert eval agency_day4_independent_contact_answer is None
    assert eval agency_day4_independent_contact_outcome is None
    assert eval has_unresolved_token("token_abandon_backup_plan") is True
    assert eval choice_history == ["day2_assign_alias", "day2_save_second_token", "day3_hide_school_evidence", "day3_honor_pause", "day4_follow_one_route_no_backup"]
    advance until screen "choice"
    assert eval current_chapter == "prologue"

testcase day4_keyboard_default_focus_and_traversal_contract:
    description "Day 4 surfaces set native focus, traverse all siblings by arrows, and hide quick-menu targets."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_share_school_evidence", {"truth": 1})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Jump("chapter_day4_seaside_train")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_1"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_2"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_1"
    keysym "K_RETURN"
    assert eval choice_history == ["day2_accept_alias", "day2_save_second_token", "day3_share_school_evidence", "day3_honor_pause", "day4_follow_one_route_no_backup", "day4_decline_independent_contact"]

testcase day4_accessibility_visual_baselines:
    description "Day 4 critical choice surfaces remain readable, focused, silent, and reduced-motion at both required baselines."

    run Function(renpy.set_physical_size, (1280, 720))
    run Function(setattr, renpy.game.preferences, "self_voicing", False)
    assert eval renpy.game.preferences.self_voicing is False
    run Function(apply_accessibility_settings, 1.0, False, True, False, False)
    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_share_school_evidence", {"truth": 1})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Jump("chapter_day4_seaside_train")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_0"
    screenshot "visual/day4_route_1280x720_keyboard_silent_reduced_motion.png"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_0"
    screenshot "visual/day4_contact_1280x720_keyboard_silent_reduced_motion.png"

    run Function(apply_accessibility_settings, 1.5, True, True, False, False)
    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_share_school_evidence", {"truth": 1})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Jump("chapter_day4_seaside_train")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_0"
    screenshot "visual/day4_route_1280x720_font_1_5_high_contrast.png"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day4_choice_id() == "day1_choice_0"
    screenshot "visual/day4_contact_1280x720_font_1_5_high_contrast.png"

    run Function(apply_accessibility_settings, 1.0, False, False, False, False)

testcase day5_shared_honor_and_repair_route_contract:
    description "A compatible shared Day 4 route honors Erii's answer and repairs only pre-existing Day 3 and daily overrides."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(apply_choice, "day2_assign_alias", {})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_hide_school_evidence", {})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day4_buy_two_tickets_real_name", {"preparation": 1, "sacrifice": 1})
    run Function(apply_choice, "day4_register_independent_contact", {"truth": 1})
    run Function(_set_day5_route_facts, True, True, True, False)
    run Jump("chapter_day5_family_lie")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_0"
    keysym "K_RETURN"
    assert "她把原页、被划去的日期和没有答案的空白一并摊开，逐页看完后仍把它们留在自己面前。"
    advance
    assert eval event_full_archive_shared is True
    assert eval cp_day5_full_archive_shared is True
    assert eval current_chapter == "day5"
    assert eval agency_day5_response_derivation_record["derivation_id"] == "erii_route_answer_derivation:v1"
    assert eval agency_day5_response_derivation_record["transaction_id"] == "agency_day5_response"
    assert eval agency_day5_response_derivation_record["input_fact_ids"] == ("resource_two_tickets", "resource_contact_card", "event_contact_risk_handover_complete", "resource_single_ticket")
    assert eval agency_day5_response_derivation_record["selected_answer_state_id"] == "shared_escape"
    assert eval agency_day5_response_derivation_record["observable_action_or_object_ids"] == ("action_erii_places_two_tickets_on_map",)
    assert eval agency_day5_response_derivation_record["unresolved_defect_ids"] == ()
    assert "她把两张票并排压在路线图上，没有把其中一张推回去。"
    advance until screen "choice"
    assert eval event_family_response_requested is True
    assert eval event_erii_selects_route_response is True
    assert eval cp_day5_route_answer_expressed is True
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    advance until screen "choice"
    keysym "K_RETURN"
    assert "路明非把自己的手移开，让她先收好票、卡或路线图，再把下一步写在她能看见的位置。"
    advance until screen "choice"
    assert eval event_route_preference_honored is True
    assert eval agency_day5_response_outcome == "outcome_route_preference_honored_shared_escape"
    keysym "K_RETURN"
    assert "他在档案旁写下自己的名字和要承担的步骤，没有把那一栏留给她。她看完后，把纸留在两人之间。"
    advance until screen "choice"
    assert eval event_self_liability_disclosed is True
    assert eval has_unresolved_token("token_hide_school_evidence") is True
    keysym "K_RETURN"
    assert "他把那几页被留下的记录补到档案里，承认先前只给过结论。她把两组纸放到同一盏灯下。"
    advance until screen "choice"
    assert eval has_unresolved_token("token_hide_school_evidence") is False
    assert eval has_unresolved_token("token_override_daily_choice") is True
    keysym "K_RETURN"
    assert "他逐项承认自己替她安排过什么，把仍在生效的安排划掉，等她自己把纸重新摆好。"
    assert eval choice_history == ["day2_assign_alias", "day2_save_second_token", "day3_hide_school_evidence", "day3_honor_pause", "day4_buy_two_tickets_real_name", "day4_register_independent_contact", "day5_share_full_archive", "day5_honor_erii_response", "day5_include_self_in_truth", "day5_repair_school_evidence", "day5_repair_daily_choice"]
    assert eval current_axis_snapshot() == {"understanding": 1, "autonomy": 2, "truth": 2, "preparation": 3, "sacrifice": 2}
    assert eval has_unresolved_token("token_hide_school_evidence") is False
    assert eval has_unresolved_token("token_override_daily_choice") is False

testcase day5_contact_replace_route_contract:
    description "A compatible contact route permits a safe summary and an explicit replacement without a same-scene repair."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_hide_school_evidence", {})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day4_follow_one_route_no_backup", {})
    run Function(apply_choice, "day4_register_independent_contact", {"truth": 1})
    run Function(_set_day5_route_facts, False, True, True, False)
    run Jump("chapter_day5_family_lie")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    keysym "K_DOWN"
    keysym "K_RETURN"
    assert "他收起原页，只留下一个听上去足够安全的结论。她没有接那张被折小的纸。"
    advance
    assert eval agency_day5_response_answer == "independent_contact"
    assert eval agency_day5_response_derivation_record["observable_action_or_object_ids"] == ("action_erii_secures_contact_card",)
    assert eval has_unresolved_token("token_withhold_family_truth") is True
    advance until screen "choice"
    keysym "K_DOWN"
    keysym "K_RETURN"
    assert "他把纸张重新排成自己熟悉的顺序。她没有再把票、卡或路线图推回来。"
    advance until screen "choice"
    assert eval event_route_preference_overridden_to_old_order is True
    assert eval agency_day5_response_outcome == "outcome_route_preference_overridden_to_old_order"
    keysym "K_DOWN"
    keysym "K_RETURN"
    assert "他只说档案里的人和他们的命令。她听完，仍把空着的那一栏朝着他。"
    advance until screen "choice"
    assert eval event_external_blame_only is True
    assert eval day5_daily_override_was_unresolved is False
    assert eval event_daily_override_unrepaired is False
    assert eval choice_history == ["day2_accept_alias", "day2_save_second_token", "day3_hide_school_evidence", "day3_honor_pause", "day4_follow_one_route_no_backup", "day4_register_independent_contact", "day5_give_safe_summary", "day5_replace_erii_response", "day5_blame_family_only"]
    assert eval has_unresolved_token("token_withhold_family_truth") is True
    assert eval has_unresolved_token("token_override_daily_choice") is True
    assert eval has_unresolved_token("token_hide_school_evidence") is True

testcase day5_solo_route_answer_contract:
    description "A compatible single-ticket route derives only solo departure from the closed Day 4 facts."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_hide_school_evidence", {})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day4_buy_single_ticket_cash", {"preparation": 1})
    run Function(apply_choice, "day4_decline_independent_contact", {})
    run Function(_set_day5_route_facts, False, False, False, True)
    run Jump("chapter_day5_family_lie")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    keysym "K_RETURN"
    assert "她把原页、被划去的日期和没有答案的空白一并摊开，逐页看完后仍把它们留在自己面前。"
    advance
    assert eval agency_day5_response_answer == "solo_departure"
    assert eval agency_day5_response_derivation_record["observable_action_or_object_ids"] == ("action_erii_places_single_ticket_in_document_case",)
    advance until screen "choice"
    keysym "K_RETURN"
    assert "路明非把自己的手移开，让她先收好票、卡或路线图，再把下一步写在她能看见的位置。"
    advance until screen "choice"
    keysym "K_DOWN"
    keysym "K_RETURN"
    assert "他只说档案里的人和他们的命令。她听完，仍把空着的那一栏朝着他。"
    advance until screen "choice"
    assert eval agency_day5_response_outcome == "outcome_route_preference_honored_solo_departure"
    assert eval event_external_blame_only is True

testcase day5_continue_without_route_answer_contract:
    description "A compatible no-backup route derives only continuation without an executable route."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_spend_both_tokens", {"sacrifice": 1})
    run Function(apply_choice, "day3_hide_school_evidence", {})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day4_follow_one_route_no_backup", {})
    run Function(_set_day5_route_facts, False, False, False, False)
    run Jump("chapter_day5_family_lie")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    keysym "K_DOWN"
    keysym "K_RETURN"
    assert "他收起原页，只留下一个听上去足够安全的结论。她没有接那张被折小的纸。"
    advance
    assert eval agency_day5_response_answer == "continue_without_executable_route"
    assert eval agency_day5_response_derivation_record["observable_action_or_object_ids"] == ("action_erii_returns_empty_route_map",)
    advance until screen "choice"
    keysym "K_RETURN"
    assert "路明非把自己的手移开，让她先收好票、卡或路线图，再把下一步写在她能看见的位置。"
    advance until screen "choice"
    keysym "K_RETURN"
    assert "他在档案旁写下自己的名字和要承担的步骤，没有把那一栏留给她。她看完后，把纸留在两人之间。"
    advance until screen "choice"
    assert eval agency_day5_response_outcome == "outcome_route_preference_honored_continue_without_executable_route"
    assert eval event_self_liability_disclosed is True

testcase day5_invalid_route_facts_hide_response_contract:
    description "Contradictory closed Day 4 route facts fail closed and expose no Day 5 response transaction."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_spend_both_tokens", {"sacrifice": 1})
    run Function(apply_choice, "day3_hide_school_evidence", {})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Function(_set_day5_route_facts, True, False, False, True)
    run Jump("chapter_day5_family_lie")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    keysym "K_RETURN"
    advance
    assert eval agency_day5_response_answer == "undetermined"
    assert eval agency_day5_response_derivation_record["observable_action_or_object_ids"] == ()
    assert eval agency_day5_response_derivation_record["unresolved_defect_ids"] == ("contradictory_ticket_resources",)
    assert eval event_family_response_requested is False
    assert eval event_erii_selects_route_response is False
    assert eval cp_day5_route_answer_expressed is False
    assert eval agency_day5_response_outcome is None
    advance until screen "choice"
    keysym "K_DOWN"
    keysym "K_RETURN"
    assert "他只说档案里的人和他们的命令。她听完，仍把空着的那一栏朝着他。"
    advance until screen "choice"
    assert eval event_external_blame_only is True

testcase day5_keyboard_default_focus_and_traversal_contract:
    description "Day 5 truth and route-response surfaces expose native keyboard focus and no quick-menu target."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_hide_school_evidence", {})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day4_buy_two_tickets_real_name", {"preparation": 1, "sacrifice": 1})
    run Function(_set_day5_route_facts, True, False, False, False)
    run Jump("chapter_day5_family_lie")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_1"
    keysym "K_UP"
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_0"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_1"

testcase day5_accessibility_visual_baselines:
    description "Day 5 truth and derived route-response surfaces remain focused, silent, and readable at both required baselines."

    run Function(renpy.set_physical_size, (1280, 720))
    run Function(setattr, renpy.game.preferences, "self_voicing", False)
    assert eval renpy.game.preferences.self_voicing is False
    run Function(apply_accessibility_settings, 1.0, False, True, False, False)
    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_share_school_evidence", {"truth": 1})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day4_buy_two_tickets_real_name", {"preparation": 1, "sacrifice": 1})
    run Function(_set_day5_route_facts, True, False, False, False)
    run Jump("chapter_day5_family_lie")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_0"
    screenshot "visual/day5_truth_1280x720_keyboard_silent_reduced_motion.png"
    keysym "K_RETURN"
    advance
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_0"
    screenshot "visual/day5_response_1280x720_keyboard_silent_reduced_motion.png"

    run Function(apply_accessibility_settings, 1.5, True, True, False, False)
    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(apply_choice, "day2_accept_alias", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day2_save_second_token", {"preparation": 1})
    run Function(apply_choice, "day3_share_school_evidence", {"truth": 1})
    run Function(apply_choice, "day3_honor_pause", {"understanding": 1, "autonomy": 1})
    run Function(apply_choice, "day4_buy_two_tickets_real_name", {"preparation": 1, "sacrifice": 1})
    run Function(_set_day5_route_facts, True, False, False, False)
    run Jump("chapter_day5_family_lie")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_0"
    screenshot "visual/day5_truth_1280x720_font_1_5_high_contrast.png"
    keysym "K_RETURN"
    advance
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day5_choice_id() == "day1_choice_0"
    screenshot "visual/day5_response_1280x720_font_1_5_high_contrast.png"

    run Function(apply_accessibility_settings, 1.0, False, False, False, False)

testcase day6_backup_truth_fallback_contract:
    description "An abandoned prepared backup and withheld archive expose only their legal repairs before a truthful fallback route."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(apply_choice, "day4_follow_one_route_no_backup", {})
    run Function(apply_choice, "day5_give_safe_summary", {})
    run Function(_set_day5_route_facts, False, False, False, False)
    run Function(_set_day6_route_context, "continue_without_executable_route", "outcome_route_preference_honored_continue_without_executable_route", True, False)
    run Function(_set_day6_preconditions, True, False, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    keysym "K_RETURN"
    advance until screen "choice"
    keysym "K_RETURN"
    advance until screen "choice"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval agency_day6_commitment_state == "no_executable_route"
    keysym "K_RETURN"
    assert eval event_shared_cost_acknowledged is True
    assert eval choice_history == ["day4_follow_one_route_no_backup", "day5_give_safe_summary", "day6_reopen_service_exit", "day6_disclose_withheld_archive", "day6_burn_old_identity", "day6_no_executable_route"]

testcase day6_shared_commitment_contract:
    description "A Day 5 shared answer plus two tickets and direct cost exposes only the shared commitment."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(_set_day5_route_facts, True, False, False, False)
    run Function(_set_day6_route_context, "shared_escape", "outcome_route_preference_honored_shared_escape", True, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval agency_day6_commitment_state == "shared_escape"
    assert eval agency_day6_commitment_derivation_record["observable_action_or_object_ids"] == ("action_erii_confirms_two_tickets_and_shared_route",)
    keysym "K_RETURN"
    assert eval event_shared_cost_acknowledged is True
    assert eval choice_history == ["day6_burn_old_identity", "day6_commit_shared_escape"]

testcase day6_independent_commitment_contract:
    description "A closed independent-contact answer with handover facts exposes only independent contact commitment."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(_set_day5_route_facts, False, True, True, False)
    run Function(_set_day6_route_context, "independent_contact", "outcome_route_preference_honored_independent_contact", True, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval agency_day6_commitment_state == "independent_contact"
    keysym "K_RETURN"

testcase day6_solo_commitment_contract:
    description "A closed solo answer and a single ticket expose only solo commitment without a contact promise."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(_set_day5_route_facts, False, False, False, True)
    run Function(_set_day6_route_context, "solo_departure", "outcome_route_preference_honored_solo_departure", True, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval agency_day6_commitment_state == "solo_departure"
    keysym "K_RETURN"

testcase day6_shift_takeback_old_order_contract:
    description "A visible shifted cost requires a second refusal before take-back and preserves the old-order override fact."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(apply_choice, "day2_assign_alias", {"understanding": 1, "autonomy": 1})
    run Function(_set_day5_route_facts, False, False, False, False)
    run Function(_set_day6_route_context, "independent_contact", "outcome_route_preference_overridden_to_old_order", False, True)
    run Function(_set_day6_preconditions, False, True, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    keysym "K_DOWN"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval event_shifted_cost_consequence_visible is True
    assert eval event_cost_reconsideration_requested is True
    assert eval event_erii_rejects_shifted_cost_again is True
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval agency_day6_commitment_state == "old_order_return"
    keysym "K_RETURN"
    assert eval has_unresolved_token("token_shift_promised_cost") is False
    assert eval cp_day6_cost_reconsideration_complete is True
    assert eval choice_history == ["day2_assign_alias", "day6_shift_cost_to_erii", "day6_take_cost_back", "day6_commit_old_order_return"]

testcase day6_invalid_facts_hide_commitment_contract:
    description "Contradictory closed Day 5 answer/outcome facts stop before any Day 6 commitment choice is exposed."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(_set_day5_route_facts, True, False, False, False)
    run Function(_set_day6_route_context, "shared_escape", "outcome_route_preference_honored_independent_contact", True, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    keysym "K_RETURN"
    advance
    assert eval agency_day6_commitment_state == "undetermined"
    assert eval agency_day6_commitment_derivation_record["observable_action_or_object_ids"] == ()
    assert eval agency_day6_commitment_derivation_record["unresolved_defect_ids"] == ("day5_answer_outcome_mismatch",)
    assert eval event_independent_route_committed is False
    assert eval event_shared_route_committed is False
    assert eval event_solo_route_committed is False
    assert eval event_old_order_route_committed is False
    assert eval event_route_collapse is False

testcase day6_keyboard_default_focus_and_traversal_contract:
    description "Day 6 cost and commitment surfaces expose native keyboard focus and no quick-menu target."

    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(_set_day5_route_facts, True, False, False, False)
    run Function(_set_day6_route_context, "shared_escape", "outcome_route_preference_honored_shared_escape", True, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day6_choice_id() == "day1_choice_0"
    keysym "K_DOWN"
    pause 0.1
    assert eval _focused_day6_choice_id() == "day1_choice_1"
    keysym "K_UP"
    pause 0.1
    assert eval _focused_day6_choice_id() == "day1_choice_0"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day6_choice_id() == "day1_choice_0"

testcase day6_accessibility_visual_baselines:
    description "Day 6 cost and guarded route commitment surfaces remain focused, silent, and readable at both required baselines."

    run Function(renpy.set_physical_size, (1280, 720))
    run Function(setattr, renpy.game.preferences, "self_voicing", False)
    assert eval renpy.game.preferences.self_voicing is False
    run Function(apply_accessibility_settings, 1.0, False, True, False, False)
    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(_set_day5_route_facts, True, False, False, False)
    run Function(_set_day6_route_context, "shared_escape", "outcome_route_preference_honored_shared_escape", True, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day6_choice_id() == "day1_choice_0"
    screenshot "visual/day6_cost_1280x720_keyboard_silent_reduced_motion.png"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day6_choice_id() == "day1_choice_0"
    screenshot "visual/day6_commitment_1280x720_keyboard_silent_reduced_motion.png"

    run Function(apply_accessibility_settings, 1.5, True, True, False, False)
    run Function(reset_run_state)
    run Function(_reset_day4_test_state)
    run Function(_reset_day5_test_state)
    run Function(_reset_day6_test_state)
    run Function(_set_day5_route_facts, True, False, False, False)
    run Function(_set_day6_route_context, "shared_escape", "outcome_route_preference_honored_shared_escape", True, False)
    run Jump("chapter_day6_no_safe_house")
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day6_choice_id() == "day1_choice_0"
    screenshot "visual/day6_cost_1280x720_font_1_5_high_contrast.png"
    keysym "K_RETURN"
    advance until screen "choice"
    assert eval renpy.get_displayable("quick_menu", "quick_menu_root") is None
    pause 0.1
    assert eval _focused_day6_choice_id() == "day1_choice_0"
    screenshot "visual/day6_commitment_1280x720_font_1_5_high_contrast.png"

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
