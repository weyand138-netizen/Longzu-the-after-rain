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

init python:
    import builtins

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
    from modules.persist_schema import (
        build_fresh_persist_root,
        validate_persist_root,
    )

    STATE_SCHEMA_SENTINEL = "semantic_state:v2"
    ENDING_FLOW_SENTINEL = "ending_flow:v1"
    ACTIVE_ENDING_LIFECYCLE = "Active"
    ENDED_ENDING_LIFECYCLE = "Ended"
    _RUN_MAP_TYPE = type({})
    _RUN_LIST_TYPE = type([])
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

    def _new_semantic_state():
        return {
            "schema_version": 2,
            "axes": {axis: 0 for axis in AXES},
            "choice_history": [],
        }

    def _require_exact_string(value, field_name):
        if type(value) is not str:
            raise TypeError("{} must be an exact string".format(field_name))
        if not value:
            raise ValueError("{} must be non-empty".format(field_name))

    def _validate_axis_values(axes):
        if type(axes) is not _RUN_MAP_TYPE:
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

        if type(sentinel) is not str:
            raise TypeError("state_schema_sentinel must be an exact string")
        if sentinel != STATE_SCHEMA_SENTINEL:
            raise ValueError("state_schema_sentinel is unsupported")
        if type(state) is not _RUN_MAP_TYPE:
            raise TypeError("semantic_state must be an exact RunMap")
        if tuple(state.keys()) != _SEMANTIC_STATE_KEYS:
            raise ValueError("semantic_state keys are invalid")
        if type(state["schema_version"]) is not int:
            raise TypeError("semantic_state.schema_version must be an exact int")
        if state["schema_version"] != 2:
            raise ValueError("semantic_state schema is unsupported")
        _validate_axis_values(state["axes"])
        history = state["choice_history"]
        if type(history) is not _RUN_LIST_TYPE:
            raise TypeError("semantic_state.choice_history must be an exact RunList")
        for choice_id in history:
            if type(choice_id) is not str:
                raise TypeError("choice_history must contain exact strings")
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

        if type(axis_deltas) is not _RUN_MAP_TYPE:
            raise TypeError("axis_deltas must be an exact RunMap")
        for axis in axis_deltas:
            if type(axis) is not str:
                raise TypeError("axis_deltas keys must be exact strings")
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
        if type(choice_id) is not str:
            raise TypeError("choice_id must be an exact string")
        if not choice_id:
            raise ValueError("choice_id must be non-empty")

    def reset_run_state():
        """Create the only supported new-game semantic/lifecycle envelope."""

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

        if type(sentinel) is not str:
            raise TypeError("ending_flow_sentinel must be an exact string")
        if sentinel != ENDING_FLOW_SENTINEL:
            raise ValueError("ending_flow_sentinel is unsupported")
        if type(lifecycle) is not str:
            raise TypeError("ending_flow_state must be an exact string")
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

    def _flush_persistent_root():
        renpy.save_persistent()

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
        root = persistent.sys_persist_state
        result = _project_ending_completion(
            root,
            ending_id=ending_id,
            checkpoint_id=completion_checkpoint,
            checkpoint_occurrence_id=completion_checkpoint + ":1",
            catalog_generation_id=root["catalog_generation_id"],
            replace_root=_replace_persistent_root,
            flush=_flush_persistent_root,
        )
        event = result.event
        if event is None:
            event = EndingCompletionEvent(
                ending_id,
                "ending_completed:" + ending_id,
                completion_checkpoint,
                completion_checkpoint + ":1",
                root["collection_epoch_id"],
                root["catalog_generation_id"],
                True,
            )
        ending_completion_event_record = event
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
        current = persistent.sys_persist_state
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
        persistent.sys_persist_state = candidate
        persistent.settings = candidate["settings"]
        renpy.save_persistent()

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
    return

label ending_resolution_safe_boundary:
    $ renpy.full_restart()
