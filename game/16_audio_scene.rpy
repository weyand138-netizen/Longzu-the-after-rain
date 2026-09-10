# Exact source anchors are supplied only after scene/cue admission. This callback
# does not edit story scripts, infer meaning from backgrounds, or admit drafts.
init 40 python:
    from modules.audio_scene import AudioSceneAnchor, compile_scene_anchors
    from modules.audio_catalog import compile_context_ranges

    _AUDIO_ADMITTED_SCENE_ANCHORS = ()
    _AUDIO_SCENE_INDEX = {}
    _AUDIO_SCENE_RANGES_BY_SOURCE = {}

    def _audio_scene_source_name(filename):
        if not isinstance(filename, str):
            return None
        source = filename.replace("\\", "/")
        return source[5:] if source.startswith("game/") else source

    def audio_scene_install(anchors, ranges=()):
        global _AUDIO_SCENE_INDEX, _AUDIO_SCENE_RANGES_BY_SOURCE
        def read_source(source):
            with renpy.file(source) as handle:
                return handle.read()
        try:
            if not anchors and not ranges:
                _AUDIO_SCENE_INDEX = {}
                _AUDIO_SCENE_RANGES_BY_SOURCE = {}
                return True
            index = compile_scene_anchors(anchors, read_source)
            ranges_by_source = compile_context_ranges(ranges, read_source)
            for anchor in index.values():
                if anchor.context_id != _audio_scene_context_for_location(
                    ranges_by_source, anchor.source, anchor.line
                ):
                    raise ValueError("Anchor does not match context range")
                pair = _AUDIO_RESTORE_CONTEXTS.get(anchor.context_id)
                if not isinstance(pair, tuple) or len(pair) != 2:
                    raise ValueError("Missing continuous context")
                for cue_id, layer in zip(pair, ("music", "ambience")):
                    cue = _AUDIO_ADMITTED_CONTINUOUS_CUES.get(cue_id)
                    if not isinstance(cue, ContinuousCue) or cue.layer != layer:
                        raise ValueError("Unadmitted continuous cue")
                if anchor.oneshot_id is not None and not isinstance(_AUDIO_ADMITTED_ONESHOT_CUES.get(anchor.oneshot_id), OneShotCue):
                    raise ValueError("Unadmitted one-shot cue")
        except Exception:
            _AUDIO_SCENE_INDEX = {}
            _AUDIO_SCENE_RANGES_BY_SOURCE = {}
            return False
        _AUDIO_SCENE_INDEX = index
        _AUDIO_SCENE_RANGES_BY_SOURCE = ranges_by_source
        return True

    def _audio_scene_context_for_location(ranges_by_source, source, line):
        if not isinstance(source, str) or type(line) is not int:
            return None
        for item in ranges_by_source.get(source, ()):
            if item.first_line <= line <= item.last_line:
                return item.context_id
        return None

    def audio_scene_context_at_current_location():
        try:
            filename, line = renpy.get_filename_line()
        except Exception:
            return None
        return _audio_scene_context_for_location(
            _AUDIO_SCENE_RANGES_BY_SOURCE, _audio_scene_source_name(filename), line
        )

    def audio_scene_restore_current_location():
        """Restore only continuous layers; a historical action is never replayed."""
        context_id = audio_scene_context_at_current_location()
        if context_id is None:
            return "NO_CONTEXT"
        return audio_adapter_restore_context(context_id)

    def _audio_scene_restore_waiting_context():
        # `after_load` runs inside its own label.  At the first interaction
        # afterwards Ren'Py exposes the restored script location, including a
        # normal line with no action anchor, so resolve the range there.
        if renpy.context_nesting_level() != 0 or main_menu or _in_replay:
            return
        record = _notification_session_record()
        with record["lock"]:
            waiting = _audio_lifecycle_locked(record)["phase"] == "WAIT_CONTEXT"
        if waiting:
            audio_scene_restore_current_location()

    def audio_scene_enter_title():
        return audio_adapter_enter_title_context("audio.context.title")

    def _audio_scene_statement(statement):
        if statement != "say" or not _AUDIO_SCENE_INDEX:
            return
        # Menu/replay contexts must not generate story occurrences.
        if renpy.context_nesting_level() != 0 or main_menu or _in_replay:
            return
        filename, line = renpy.get_filename_line()
        source = _audio_scene_source_name(filename)
        anchor = _AUDIO_SCENE_INDEX.get((source, line))
        if anchor is None:
            return
        record = _notification_session_record()
        with record["lock"]:
            phase = _audio_lifecycle_locked(record)["phase"]
            historical = phase != "LIVE" or _notification_rollback_active()
            if phase == "WAIT_CONTEXT":
                audio_adapter_restore_context(anchor.context_id)
            elif phase == "LIVE":
                for cue_id in _AUDIO_RESTORE_CONTEXTS[anchor.context_id]:
                    audio_adapter_request_continuous(cue_id)
            if anchor.oneshot_id is not None:
                occurrence = "authored-sfx:v1:scene:{}:{}".format(record.get("scene_run", 0), anchor.anchor_id)
                if historical or renpy.is_skipping():
                    pool, _ = claim_oneshot(_audio_oneshot_pool_locked(record), occurrence)
                    record["oneshot_pool"] = pool
                else:
                    audio_adapter_dispatch_oneshot(anchor.oneshot_id, occurrence)

    audio_scene_install(_AUDIO_ADMITTED_SCENE_ANCHORS)
    if _audio_scene_statement not in config.statement_callbacks:
        config.statement_callbacks.append(_audio_scene_statement)
    if _audio_scene_restore_waiting_context not in config.interact_callbacks:
        config.interact_callbacks.append(_audio_scene_restore_waiting_context)
