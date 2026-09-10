default current_chapter = "prologue"
default tension_mode_enabled = False
default save_contract_sentinel = None
default save_catalog_generation_id = None
default semantic_state = None
default state_schema_sentinel = None
default ending_flow_sentinel = None
default ending_flow_state = None
default pending_ending_id = None
default ending_completion_event_record = None

python early:
    # This registration must exist before Ren'Py consumes any startup
    # persistent payload.  The callback is pure and has no presentation or
    # live-notification authority.
    from modules.persist_merge import merge_sys_persist_state

    renpy.register_persistent("sys_persist_state", merge_sys_persist_state)

init python:
    import builtins
    import threading

    from modules.accessibility_focus import FocusAwareGraph
    from modules.control_catalog import CATALOG_GENERATION_ID
    from modules.ending_completion_projection import (
        EndingCompletionEvent,
        commit_ending_completion as _project_ending_completion,
    )
    from modules.ending_rules import (
        AXES,
        ENDING_PENDING_ID_PREFIX,
        ENDING_PENDING_IDS,
        ENDING_PRIORITY,
        _PROJECTION_INDEX,
        _build_detached_ending_snapshot,
        resolve_ending_record,
    )
    from modules.narrative_token_projection import has_unresolved_token as _has_unresolved_token
    from modules.durable_flush_bridge import DurableFlushBridge
    from modules.notification_durable_batch import (
        DUPLICATE_NOOP,
        NotificationMembershipOperationCoordinator,
    )
    from modules.persist_batch import (
        APPLIED_FLUSHED,
        COMMIT_STATUS_UNKNOWN,
        PERSIST_FLUSH_FAILED_SAFE,
        REJECTED_REENTRANT,
    )
    from modules.persist_merge import (
        STARTUP_PERSIST_READY,
        classify_startup_persist_root,
    )
    from modules.persist_schema import (
        build_fresh_persist_root,
        snapshot_persist_root,
        validate_persist_root,
    )

    STATE_SCHEMA_SENTINEL = "semantic_state:v2"
    ENDING_FLOW_SENTINEL = "ending_flow:v1"
    ACTIVE_ENDING_LIFECYCLE = "Active"
    ENDED_ENDING_LIFECYCLE = "Ended"
    # Ren'Py turns rollback-owned containers into these exact subclasses when
    # it restores a player save. Keep accepting only the two engine-owned
    # representations, rather than treating a valid restored state as a
    # malformed save and returning the player to the title page.
    _RUN_MAP_TYPES = (dict, renpy.revertable.RevertableDict)
    _RUN_LIST_TYPES = (list, renpy.revertable.RevertableList)
    _SEMANTIC_STATE_KEYS = ("schema_version", "axes", "choice_history")
    _ENDING_LABEL_MAP_ITEMS = (
        ("rain_stops", "ending_rain_stops"),
        ("her_own_name", "ending_her_own_name"),
        ("see_the_sea", "ending_see_the_sea"),
        ("one_person_train", "ending_one_person_train"),
        ("golden_cage", "ending_golden_cage"),
        ("unsent_postcard", "ending_unsent_postcard"),
    )
    ENDING_LABEL_MAP = dict(_ENDING_LABEL_MAP_ITEMS)
    _NOTIFICATION_MEMBERSHIP_SESSION_KEY = "longzu.persist_notification_membership:v1"
    _notification_membership_record_creation_lock = threading.RLock()
    _durable_flush_bridge = DurableFlushBridge()

    def _new_semantic_state():
        return {
            "schema_version": 2,
            "axes": {axis: 0 for axis in AXES},
            "choice_history": [],
        }

    def _require_exact_string(value, field_name):
        # Ren'Py restores rollback-owned scalar values as string subclasses.
        # Accept that engine representation while still rejecting all
        # non-string values at the persisted-state boundary.
        if not isinstance(value, str):
            raise TypeError("{} must be a string".format(field_name))
        if not value:
            raise ValueError("{} must be non-empty".format(field_name))

    def _normalise_loaded_runtime_sentinel(value, expected, field_name):
        """Restore a migrated guard without weakening saved-state validation.

        Older player saves can omit a ``default``-backed guard scalar when
        Ren'Py reconstructs the store. The guard is redundant: the semantic
        envelope and ending lifecycle below remain the authoritative state.
        Only an omitted value is migrated; supplied non-string or unsupported
        guard values are still rejected.
        """

        if value is None:
            return expected
        _require_exact_string(value, field_name)
        if value != expected:
            raise ValueError("{} is unsupported".format(field_name))
        return expected

    def _validate_axis_values(axes):
        if type(axes) not in _RUN_MAP_TYPES:
            raise TypeError("semantic_state.axes must be an exact RunMap")
        if tuple(axes.keys()) != AXES:
            raise ValueError("semantic_state.axes keys are invalid")
        for axis in AXES:
            value = axes[axis]
            if type(value) is not int:
                raise TypeError("semantic_state axis values must be exact ints")
            if value < 0 or value > 3:
                raise ValueError("semantic_state axis values must be in 0..3")

    def validate_active_semantic_state(sentinel, state):
        """Validate the live schema-2 envelope without normalising it."""

        if not isinstance(sentinel, str):
            raise TypeError("state_schema_sentinel must be a string")
        if sentinel != STATE_SCHEMA_SENTINEL:
            raise ValueError("state_schema_sentinel is unsupported")
        if type(state) not in _RUN_MAP_TYPES:
            raise TypeError("semantic_state must be an exact RunMap")
        if tuple(state.keys()) != _SEMANTIC_STATE_KEYS:
            raise ValueError("semantic_state keys are invalid")
        if type(state["schema_version"]) is not int:
            raise TypeError("semantic_state.schema_version must be an exact int")
        if state["schema_version"] != 2:
            raise ValueError("semantic_state schema is unsupported")
        _validate_axis_values(state["axes"])
        history = state["choice_history"]
        if type(history) not in _RUN_LIST_TYPES:
            raise TypeError("semantic_state.choice_history must be an exact RunList")
        for choice_id in history:
            if not isinstance(choice_id, str):
                raise TypeError("choice_history must contain strings")
            if not choice_id:
                raise ValueError("choice_history cannot contain empty IDs")
            if choice_id not in _PROJECTION_INDEX:
                raise ValueError("choice_history contains an unknown choice ID")
        if len(history) != len(set(history)):
            raise ValueError("choice_history cannot contain duplicate IDs")
        return state

    def _active_semantic_state():
        return validate_active_semantic_state(state_schema_sentinel, semantic_state)

    def validate_axis_deltas(axis_deltas):
        """Validate the sparse positive-evidence payload and return its size."""

        if type(axis_deltas) not in _RUN_MAP_TYPES:
            raise TypeError("axis_deltas must be an exact RunMap")
        for axis in axis_deltas:
            if not isinstance(axis, str):
                raise TypeError("axis_deltas keys must be strings")
            if axis not in AXES:
                raise ValueError("axis_deltas contains an unknown axis")
        for axis in AXES:
            if axis in axis_deltas:
                if type(axis_deltas[axis]) is not int:
                    raise TypeError("axis delta values must be exact ints")
                if axis_deltas[axis] != 1:
                    raise ValueError("axis deltas must be positive unit evidence")
        return len(axis_deltas)

    def _validate_choice_id(choice_id):
        if not isinstance(choice_id, str):
            raise TypeError("choice_id must be a string")
        if not choice_id:
            raise ValueError("choice_id must be non-empty")

    def reset_run_state():
        """Create the only supported new-game semantic/lifecycle envelope."""

        notification_begin_new_run()
        global current_chapter, save_contract_sentinel, save_catalog_generation_id
        global semantic_state, state_schema_sentinel, ending_flow_sentinel
        global ending_flow_state, pending_ending_id, ending_completion_event_record

        semantic_state = _new_semantic_state()
        state_schema_sentinel = STATE_SCHEMA_SENTINEL
        ending_flow_sentinel = ENDING_FLOW_SENTINEL
        ending_flow_state = ACTIVE_ENDING_LIFECYCLE
        pending_ending_id = None
        ending_completion_event_record = None
        save_contract_sentinel = "save_contract:v1"
        save_catalog_generation_id = CATALOG_GENERATION_ID
        current_chapter = "prologue"

    def normalise_loaded_runtime_sentinels():
        """Migrate absent, non-authoritative save guards after a load."""

        global semantic_state, state_schema_sentinel, ending_flow_sentinel
        global ending_flow_state

        state_schema_sentinel = _normalise_loaded_runtime_sentinel(
            state_schema_sentinel,
            STATE_SCHEMA_SENTINEL,
            "state_schema_sentinel",
        )
        ending_flow_sentinel = _normalise_loaded_runtime_sentinel(
            ending_flow_sentinel,
            ENDING_FLOW_SENTINEL,
            "ending_flow_sentinel",
        )
        # Schema-2 did not exist in legacy active-run saves. Their restored
        # narrative frame is still valid, but the new semantic envelope is
        # absent. There is exactly one safe migration only before terminal
        # flow has started: initialise the empty schema-2 envelope and retain
        # the loaded narrative position unchanged.
        if semantic_state is None:
            if pending_ending_id is not None or ending_completion_event_record is not None:
                raise ValueError("semantic_state is missing for terminal state")
            semantic_state = _new_semantic_state()
        # A missing lifecycle can be migrated only for a run that has no
        # pending ending and no completion event. That combination has exactly
        # one valid lifecycle: Active. Any terminal-shaped combination remains
        # invalid until its real lifecycle value is present.
        if ending_flow_state is None:
            if pending_ending_id is not None or ending_completion_event_record is not None:
                raise ValueError("ending_flow_state is missing for terminal state")
            ending_flow_state = ACTIVE_ENDING_LIFECYCLE

    def apply_choice(choice_id, axis_deltas):
        """Atomically append one declared choice and its sparse axis evidence."""

        global semantic_state

        state = _active_semantic_state()
        _active_ending_lifecycle()
        _validate_choice_id(choice_id)
        validate_axis_deltas(axis_deltas)
        if choice_id not in _PROJECTION_INDEX:
            raise ValueError("choice_id has no frozen projection")
        expected_deltas = _PROJECTION_INDEX[choice_id].axis_deltas
        supplied_deltas = tuple(axis_deltas.get(axis, 0) for axis in AXES)
        if supplied_deltas != expected_deltas:
            raise ValueError("axis_deltas do not match the frozen choice projection")
        history = state["choice_history"]
        if choice_id in history:
            return "DUPLICATE_NOOP"
        candidate_axes = {
            axis: min(3, state["axes"][axis] + axis_deltas.get(axis, 0))
            for axis in AXES
        }
        semantic_state = {
            "schema_version": 2,
            "axes": candidate_axes,
            "choice_history": history + [choice_id],
        }
        return "APPLIED"

    def current_axis_snapshot():
        """Return a detached display/test-only copy of current axis values."""

        state = _active_semantic_state()
        return {axis: state["axes"][axis] for axis in AXES}

    def current_choice_history():
        """Return a detached history copy for narrative membership checks."""

        return builtins.list(_active_semantic_state()["choice_history"])

    def current_ending_snapshot():
        """Transfer only validated immutable scalars across the pure boundary."""

        state = _active_semantic_state()
        axis_values = tuple(state["axes"][axis] for axis in AXES)
        history_ids = tuple(state["choice_history"])
        return _build_detached_ending_snapshot(
            state["schema_version"], axis_values, history_ids
        )

    def has_unresolved_token(token_id):
        """Expose the canonical-history token projection to narrative labels."""

        return _has_unresolved_token(
            _active_semantic_state()["choice_history"], token_id
        )

    def validate_ending_lifecycle(sentinel, lifecycle, pending_id):
        """Validate the frozen rollback-owned terminal-flow combinations."""

        if not isinstance(sentinel, str):
            raise TypeError("ending_flow_sentinel must be a string")
        if sentinel != ENDING_FLOW_SENTINEL:
            raise ValueError("ending_flow_sentinel is unsupported")
        if not isinstance(lifecycle, str):
            raise TypeError("ending_flow_state must be a string")
        if lifecycle not in (ACTIVE_ENDING_LIFECYCLE, ENDED_ENDING_LIFECYCLE):
            raise ValueError("ending_flow_state is invalid")
        if pending_id is not None:
            _require_exact_string(pending_id, "pending_ending_id")
            if pending_id not in ENDING_PENDING_IDS:
                raise ValueError("pending_ending_id is invalid")
        if lifecycle == ENDED_ENDING_LIFECYCLE and pending_id is None:
            raise ValueError("Ended lifecycle requires a pending ending ID")
        return lifecycle

    def _active_ending_lifecycle():
        lifecycle = validate_ending_lifecycle(
            ending_flow_sentinel, ending_flow_state, pending_ending_id
        )
        if lifecycle != ACTIVE_ENDING_LIFECYCLE:
            raise RuntimeError("ending already committed")
        return lifecycle

    def _pending_id_for(ending_id):
        if type(ending_id) is not str or ending_id not in ENDING_PRIORITY:
            raise ValueError("ending_id is not canonical")
        return ENDING_PENDING_ID_PREFIX + ending_id

    def _validate_ending_label_map():
        if tuple(ENDING_LABEL_MAP.keys()) != ENDING_PRIORITY:
            raise ValueError("ENDING_LABEL_MAP keys are not the frozen priority")
        labels = tuple(ENDING_LABEL_MAP.values())
        if any(type(label) is not str or not label for label in labels):
            raise TypeError("ENDING_LABEL_MAP labels must be non-empty exact strings")
        if len(set(labels)) != len(ENDING_PRIORITY):
            raise ValueError("ENDING_LABEL_MAP must be one-to-one")
        if tuple(_ENDING_LABEL_MAP_ITEMS) != tuple(ENDING_LABEL_MAP.items()):
            raise ValueError("ENDING_LABEL_MAP differs from the frozen mapping")
        return ENDING_LABEL_MAP

    def prepare_day7_ending_jump():
        """Resolve one active run once and stage its only permitted target label."""

        global pending_ending_id

        _active_ending_lifecycle()
        ending_labels = _validate_ending_label_map()
        snapshot = current_ending_snapshot()
        record = resolve_ending_record(snapshot)
        ending_id = record.ending_id
        if type(ending_id) is not str or ending_id not in ending_labels:
            raise ValueError("canonical resolver returned an unmapped ending")
        pending_ending_id = _pending_id_for(ending_id)
        return ending_labels[ending_id]

    def commit_ending_entry(expected_ending_id):
        """Perform the sole Active-to-Ended transition at a mapped label entry."""

        global ending_flow_state

        _active_ending_lifecycle()
        if pending_ending_id != _pending_id_for(expected_ending_id):
            raise ValueError("ending entry does not match the pending ending")
        ending_flow_state = ENDED_ENDING_LIFECYCLE
        return "APPLIED"

    def _replace_persistent_root(candidate_root):
        validate_persist_root(candidate_root)
        persistent.sys_persist_state = candidate_root
        persistent.settings = candidate_root["settings"]

    def _notification_membership_session_record():
        """Return the one session-local serialisation record for root writes."""

        # Session creation is separately locked so two first callers cannot
        # manufacture independent coordinators and lose one of their batches.
        with _notification_membership_record_creation_lock:
            record = renpy.session.get(_NOTIFICATION_MEMBERSHIP_SESSION_KEY)
            if record is None:
                operation_lock = threading.RLock()
                record = {
                    "operation_lock": operation_lock,
                    "coordinator": NotificationMembershipOperationCoordinator(
                        lambda: persistent.sys_persist_state,
                        _replace_persistent_root,
                        _durable_flush_bridge,
                        operation_lock=operation_lock,
                    ),
                }
                renpy.session[_NOTIFICATION_MEMBERSHIP_SESSION_KEY] = record
            if (
                type(record) is not dict
                or tuple(record.keys()) != ("operation_lock", "coordinator")
                or not isinstance(record["coordinator"], NotificationMembershipOperationCoordinator)
            ):
                raise RuntimeError("notification membership session owner is malformed")
            return record

    def _notification_membership_coordinator():
        """Return the one session-local owner of notification-capable writes."""

        return _notification_membership_session_record()["coordinator"]

    def commit_notification_membership(
        checkpoint_occurrence_id,
        achievement_ids=(),
        ending_ids=(),
        memory_ids=(),
    ):
        """Commit one catalog-authorized membership batch through 10_state only."""

        return _notification_membership_coordinator().commit(
            checkpoint_occurrence_id=checkpoint_occurrence_id,
            achievement_ids=achievement_ids,
            ending_ids=ending_ids,
            memory_ids=memory_ids,
        )

    def mark_persisted_achievements_seen(achievement_ids):
        """Acknowledge existing achievement memberships through SYS-PERSIST.

        Seen state is a canonical-root change, but never a new membership or
        a presentation instruction. The coordinator therefore applies the
        same operation lock and durable bridge while returning no raw group.
        """

        return _notification_membership_coordinator().mark_achievements_seen(
            achievement_ids=achievement_ids,
        )

    def notification_membership_commit_diagnostics():
        """Developer-only detached unknown-commit roots; never a recovery action."""

        return _notification_membership_coordinator().frozen_root_copies()

    def validate_ending_completion_state(lifecycle, pending_id, event, root):
        """Validate the rollback-owned completion event against durable state."""

        validate_persist_root(root)
        if lifecycle == ACTIVE_ENDING_LIFECYCLE:
            # A resolver handoff legitimately stages one of the six pending IDs
            # while remaining Active.  Only a completion record is impossible
            # until the mapped label has committed the Ended transition.
            if event is not None:
                raise ValueError("Active lifecycle cannot have a completion event")
            return None
        if event is None:
            return None
        if lifecycle != ENDED_ENDING_LIFECYCLE:
            raise ValueError("completion event requires an Ended lifecycle")
        expected_ending_id = pending_id[len(ENDING_PENDING_ID_PREFIX):]
        if type(event) is not EndingCompletionEvent:
            raise TypeError("ending_completion_event_record has an invalid type")
        if event.ending_id != expected_ending_id:
            raise ValueError("ending completion event does not match the pending ending")
        if event.completed_event_id != "ending_completed:" + expected_ending_id:
            raise ValueError("ending completion event has an invalid event ID")
        _require_exact_string(event.checkpoint_id, "completion checkpoint")
        if event.checkpoint_occurrence_id != event.checkpoint_id + ":1":
            raise ValueError("ending completion event has an invalid occurrence")
        if type(event.collection_epoch_id) is not int:
            raise TypeError("ending completion event epoch must be an exact int")
        if event.collection_epoch_id != root["collection_epoch_id"]:
            raise ValueError("ending completion event epoch does not match persistent state")
        if event.catalog_generation_id != root["catalog_generation_id"]:
            raise ValueError("ending completion event catalog does not match persistent state")
        if event.stable_completion_boundary is not True or event.owner_system != "SYS-ENDING":
            raise ValueError("ending completion event violates ADR-0006")
        if expected_ending_id not in root["ending_ids"]:
            raise ValueError("completion event lacks durable ending membership")
        return event

    def _validate_existing_completion_event(expected_ending_id, completion_checkpoint):
        event = validate_ending_completion_state(
            ending_flow_state,
            pending_ending_id,
            ending_completion_event_record,
            persistent.sys_persist_state,
        )
        if event.ending_id != expected_ending_id:
            raise ValueError("ending completion event does not match the ending")
        if event.checkpoint_id != completion_checkpoint:
            raise ValueError("ending completion event has an invalid checkpoint")

    def commit_ending_completion(ending_id, completion_checkpoint):
        """Emit the rollback-owned completion event after visible terminal closure."""

        global ending_completion_event_record

        validate_ending_lifecycle(
            ending_flow_sentinel, ending_flow_state, pending_ending_id
        )
        validate_ending_completion_state(
            ending_flow_state,
            pending_ending_id,
            ending_completion_event_record,
            persistent.sys_persist_state,
        )
        if ending_flow_state != ENDED_ENDING_LIFECYCLE:
            raise ValueError("ending completion requires an entered ending")
        if pending_ending_id != _pending_id_for(ending_id):
            raise ValueError("ending completion does not match the pending ending")
        _require_exact_string(completion_checkpoint, "completion_checkpoint")
        if ending_completion_event_record is not None:
            _validate_existing_completion_event(ending_id, completion_checkpoint)
            return "DUPLICATE_NOOP"
        durable_result = commit_notification_membership(
            completion_checkpoint + ":1",
            ending_ids=(ending_id,),
        )
        if durable_result.status not in (APPLIED_FLUSHED, DUPLICATE_NOOP):
            return durable_result.status
        root = persistent.sys_persist_state
        result = _project_ending_completion(
            root,
            ending_id=ending_id,
            checkpoint_id=completion_checkpoint,
            checkpoint_occurrence_id=completion_checkpoint + ":1",
            catalog_generation_id=root["catalog_generation_id"],
            notification_result=durable_result,
        )
        event = result.event
        if event is None:
            raise RuntimeError("durable ending completion lacks its exact event")
        if durable_result.status == DUPLICATE_NOOP:
            # Persistent membership can outlive the rollback-owned event record
            # after a pre-completion rollback. Reconstruct exactly that missing
            # record without writing or producing a new notification raw group.
            ending_completion_event_record = event
            return "DUPLICATE_NOOP"
        ending_completion_event_record = event
        if result.notification_result is not None:
            queue_live_notification_group(result.notification_result)
        return result.status

    def apply_accessibility_settings(
        font_scale,
        high_contrast,
        reduced_motion,
        flash_effects_enabled,
        screen_shake_enabled,
    ):
        """Commit the five project accessibility settings as one batch."""

        allowed_scales = (0.8, 1.0, 1.2, 1.5, 2.0)
        if font_scale not in allowed_scales:
            raise ValueError("Unsupported font scale: {!r}".format(font_scale))
        record = _notification_membership_session_record()
        coordinator = record["coordinator"]
        # Reserve before waiting for the root transaction lock. A second
        # accessibility request must be rejected at its entry boundary while
        # this request waits behind an existing durable flush; it must never
        # become a queued later root write.
        if not coordinator.begin_external_operation():
            return REJECTED_REENTRANT
        try:
            with record["operation_lock"]:
                # A membership flush with an unknown outcome freezes every
                # later root write, including SYS-ACCESS settings. Recheck
                # only after acquiring the transaction lock: a prior owner
                # can freeze while this reserved request is waiting.
                if coordinator.write_frozen:
                    return COMMIT_STATUS_UNKNOWN
                return _apply_accessibility_settings_admitted(
                    coordinator,
                    font_scale,
                    high_contrast,
                    reduced_motion,
                    flash_effects_enabled,
                    screen_shake_enabled,
                )
        finally:
            coordinator.end_external_operation()

    def _apply_accessibility_settings_admitted(
        coordinator,
        font_scale,
        high_contrast,
        reduced_motion,
        flash_effects_enabled,
        screen_shake_enabled,
    ):
        """Perform a settings batch after the shared owner admits its body."""

        current = persistent.sys_persist_state
        previous = snapshot_persist_root(current)
        preflight = _durable_flush_bridge.preflight()
        if not preflight.ready:
            # Preflight has proved that this operation cannot start a write,
            # so it is the only settings-path safe failure.
            return PERSIST_FLUSH_FAILED_SAFE
        candidate = build_fresh_persist_root()
        for field in (
            "schema_version",
            "catalog_generation_id",
            "collection_epoch_id",
        ):
            candidate[field] = current[field]
        for field in (
            "achievement_ids",
            "seen_achievement_ids",
            "ending_ids",
            "memory_ids",
        ):
            candidate[field] = builtins.list(current[field])
        candidate["settings"]["font_scale"] = font_scale
        candidate["settings"]["high_contrast"] = high_contrast
        candidate["settings"]["reduced_motion"] = reduced_motion
        candidate["settings"]["flash_effects_enabled"] = flash_effects_enabled
        candidate["settings"]["screen_shake_enabled"] = screen_shake_enabled
        validate_persist_root(candidate)
        try:
            # The callbacks receive a detached candidate. If either one
            # raises, we cannot prove whether the persistent root changed,
            # so the session-wide owner freezes before any later write.
            _replace_persistent_root(snapshot_persist_root(candidate))
            flush_result = _durable_flush_bridge.flush_after_replacement(
                preflight,
                snapshot_persist_root(candidate),
            )
            if not flush_result.verified:
                raise OSError("durable flush bridge could not verify the candidate")
        except Exception:
            coordinator.freeze_unknown_root_write(previous, candidate)
            return COMMIT_STATUS_UNKNOWN
        return APPLIED_FLUSHED

default persistent.sys_persist_state = build_fresh_persist_root()

label day7_resolve_ending:
    python:
        try:
            _day7_target_label = prepare_day7_ending_jump()
        except (TypeError, ValueError):
            _day7_target_label = None
    if _day7_target_label is None:
        jump ending_resolution_safe_boundary
    jump expression _day7_target_label

label after_load:
    python:
        try:
            # The exact merge marker is classified before any default/root
            # validation or subsystem read.  A merge/recovery load is never a
            # live notification path and therefore reaches the blocking-safe
            # boundary without a projection or presentation call.
            _after_load_persist_status = classify_startup_persist_root(
                persistent.sys_persist_state
            )
            if _after_load_persist_status != STARTUP_PERSIST_READY:
                _after_load_terminal_state_valid = False
            else:
                normalise_loaded_runtime_sentinels()
                validate_active_semantic_state(state_schema_sentinel, semantic_state)
                validate_ending_lifecycle(
                    ending_flow_sentinel, ending_flow_state, pending_ending_id
                )
                validate_ending_completion_state(
                    ending_flow_state,
                    pending_ending_id,
                    ending_completion_event_record,
                    persistent.sys_persist_state,
                )
                _after_load_terminal_state_valid = True
        except (TypeError, ValueError):
            _after_load_terminal_state_valid = False
    if not _after_load_terminal_state_valid:
        jump ending_resolution_safe_boundary
    $ notification_after_load_semantic_validation_succeeded()
    return

label ending_resolution_safe_boundary:
    $ notification_enter_blocking_safe_exit()
    $ renpy.full_restart()
