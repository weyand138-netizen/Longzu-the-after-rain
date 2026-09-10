# Source-pinned output gate and reconstruction boundary. Production context
# mappings remain empty until approved scene/cue admission is complete.
init 20 python:
    import hashlib
    import renpy.audio.audio as _audio_engine

    _AUDIO_ENGINE_SOURCE_HASH = "17a02290d5b9cfe744a21472685176e31e0e3af5de8b5095d709105f9340c3ec"
    _AUDIO_RESTORE_CONTEXTS = {}
    _AUDIO_GATED_CHANNELS = tuple(
        channel for pair in _AUDIO_CONTINUOUS_CHANNELS.values() for channel in pair
    ) + tuple("audio_oneshot_{}".format(i) for i in range(4))

    def _audio_engine_gate_supported():
        try:
            if renpy.version_string != "Ren'Py 8.5.3.26051504":
                return False
            with open(_audio_engine.__file__, "rb") as source:
                return hashlib.sha256(source.read()).hexdigest() == _AUDIO_ENGINE_SOURCE_HASH
        except (OSError, TypeError):
            return False

    _AUDIO_ENGINE_GATE_SUPPORTED = _audio_engine_gate_supported()

    def _audio_lifecycle_locked(record):
        return record.setdefault("lifecycle", {"phase": "LIVE", "gate": None})

    def _audio_tts_suppressed():
        try:
            # Unknown/clipboard/active modes all fail closed. Never change
            # SAPI, its mixer, volume or the engine's raw player preferences.
            return _preferences.self_voicing is not False
        except Exception:
            return True

    def _audio_stop_authored_locked(record):
        stopped = True
        for name in _AUDIO_GATED_CHANNELS:
            try:
                renpy.music.stop(channel=name, fadeout=0)
            except Exception as exc:
                stopped = False
                record.setdefault("continuous_faults", {})[name] = type(exc).__name__
        if not stopped:
            _audio_lifecycle_locked(record)["phase"] = "STOP_FAILED"
        else:
            record["oneshot_faulted"] = False
            record["oneshot_pool"] = retire_oneshots(_audio_oneshot_pool_locked(record))
        return stopped

    def _audio_apply_output_gate_locked(record):
        lifecycle = _audio_lifecycle_locked(record)
        try:
            project_gain = audio_settings_game_output_multiplier()
        except Exception:
            project_gain = 0.0
        if type(project_gain) not in (int, float) or not 0.0 <= project_gain <= 1.0:
            project_gain = 0.0
        gate = project_gain if (lifecycle["phase"] == "LIVE" and not _audio_tts_suppressed()
                                and _AUDIO_ENGINE_GATE_SUPPORTED) else 0.0
        if not _AUDIO_ENGINE_GATE_SUPPORTED:
            lifecycle["gate"] = 0.0
            lifecycle["phase"] = "ENGINE_UNSUPPORTED"
            for channel in _AUDIO_GATED_CHANNELS:
                try:
                    renpy.music.stop(channel=channel, fadeout=0)
                except Exception:
                    pass
            return 0.0
        # chan_volume belongs to the physical Channel, not its rollback context.
        # Serialize coefficient changes and periodic application with the actual
        # audio thread. Public music.set_volume would alter context.secondary_volume.
        with _audio_engine.lock:
            oneshot_open = bool(gate and _audio_oneshot_raw_enabled() and not record.get("oneshot_faulted", False))
            if not oneshot_open and record.get("oneshot_gate_open") is not False:
                _audio_stop_oneshots_locked(record)
            record["oneshot_gate_open"] = oneshot_open
            for name in _AUDIO_GATED_CHANNELS:
                channel = None
                layer = next((key for key, pair in _AUDIO_CONTINUOUS_CHANNELS.items() if name in pair), None)
                states = _audio_continuous_states_locked(record)
                try:
                    channel = _audio_engine.get_channel(name)
                    channel_gate = 0.0 if layer and states[layer].status == "FAULT_SILENT" else gate
                    if name in _AUDIO_ONESHOT_CHANNELS and not oneshot_open:
                        channel_gate = 0.0
                    channel.set_volume(channel_gate)
                    if _audio_engine.pcm_ok:
                        channel.periodic()
                except Exception as exc:
                    # A failed decoder or device must not escape a GUI callback.
                    try:
                        if channel is not None:
                            channel.set_volume(0.0)
                    except Exception:
                        pass
                    record.setdefault("continuous_faults", {})[name] = type(exc).__name__
                    affected = _AUDIO_CONTINUOUS_CHANNELS[layer] if layer else (name,)
                    if layer:
                        states[layer] = fault_continuous(states[layer])
                    for target in affected:
                        try:
                            target_channel = _audio_engine.get_channel(target)
                            if target_channel is not None:
                                target_channel.set_volume(0.0)
                        except Exception:
                            pass
                        try:
                            renpy.music.stop(channel=target, fadeout=0)
                        except Exception:
                            pass
        lifecycle["gate"] = gate
        return gate

    def audio_adapter_refresh_output_gate():
        record = _notification_session_record()
        with record["lock"]:
            _audio_reap_retiring_continuous_locked(record)
            return _audio_apply_output_gate_locked(record)

    def _audio_context_cues(context_id):
        if not isinstance(context_id, str):
            return None
        pair = _AUDIO_RESTORE_CONTEXTS.get(context_id)
        if not isinstance(pair, tuple) or len(pair) != 2:
            return None
        if any(not isinstance(cue_id, str) for cue_id in pair):
            return None
        cues = tuple(_AUDIO_ADMITTED_CONTINUOUS_CUES.get(cue_id) for cue_id in pair)
        if any(not isinstance(cue, ContinuousCue) or cue.layer != layer
               for cue, layer in zip(cues, ("music", "ambience"))):
            return None
        return cues

    def _audio_commit_context_locked(record, cues):
        states = _audio_continuous_states_locked(record)
        for cue in cues:
            state, commands = request_continuous(states[cue.layer], cue)
            _audio_execute_continuous_locked(record, cue.layer, state, commands)

    def audio_adapter_enter_reconstruction(reason):
        if reason not in ("LOAD", "ROLLBACK", "BLOCKING", "NEW_RUN"):
            return "INVALID"
        record = _notification_session_record()
        with record["lock"]:
            lifecycle = _audio_lifecycle_locked(record)
            # Ren'Py unfreeze also sets after_rollback during FileLoad. Its
            # after-default observer must not bypass the stronger load barrier.
            if reason == "ROLLBACK" and lifecycle["phase"] in (
                "LOAD", "BLOCKING", "STOP_FAILED", "ENGINE_UNSUPPORTED"
            ):
                _audio_apply_output_gate_locked(record)
                return lifecycle["phase"]
            # Publish the phase and physical coefficient as one audio-thread
            # critical section; a concurrent periodic pass cannot see LOAD/1.
            with _audio_engine.lock:
                lifecycle["phase"] = reason
                _audio_apply_output_gate_locked(record)
            stopped = _audio_stop_authored_locked(record)
            states = _audio_continuous_states_locked(record)
            for layer, state in tuple(states.items()):
                states[layer] = ContinuousLayer(generation=state.generation+1)
            # Never resume the abandoned session's target after load/rollback.
            # A validated, approved stable context must replace both layers.
            if reason == "ROLLBACK" and stopped:
                lifecycle["phase"] = "WAIT_CONTEXT"
            elif reason == "NEW_RUN" and _AUDIO_ENGINE_GATE_SUPPORTED and stopped:
                record["scene_run"] = record.get("scene_run", 0) + 1
                lifecycle["phase"] = "LIVE"
                _audio_apply_output_gate_locked(record)
            return lifecycle["phase"]

    def audio_adapter_load_semantics_validated():
        record = _notification_session_record()
        with record["lock"]:
            lifecycle = _audio_lifecycle_locked(record)
            if lifecycle["phase"] == "LOAD":
                # The deserializer can restore old Channel contexts after the
                # before-load stop. Retire those queues while output is still 0.
                if _audio_stop_authored_locked(record):
                    lifecycle["phase"] = "WAIT_CONTEXT"
            return lifecycle["phase"]

    def audio_adapter_restore_context(context_id):
        cues = _audio_context_cues(context_id)
        if cues is None:
            return "INVALID"
        record = _notification_session_record()
        with record["lock"]:
            lifecycle = _audio_lifecycle_locked(record)
            if lifecycle["phase"] != "WAIT_CONTEXT" or not _AUDIO_ENGINE_GATE_SUPPORTED:
                return "GATED"
            # Rebuild both continuous targets while output is still zero.
            _audio_commit_context_locked(record, cues)
            lifecycle["phase"] = "LIVE"
            _audio_apply_output_gate_locked(record)
            return "CONTEXT_COMMITTED"

    def audio_adapter_enter_title_context(context_id):
        """Replace every narrative layer before the title context is audible."""
        cues = _audio_context_cues(context_id)
        if cues is None:
            return "INVALID"
        record = _notification_session_record()
        with record["lock"]:
            lifecycle = _audio_lifecycle_locked(record)
            lifecycle["phase"] = "TITLE"
            _audio_apply_output_gate_locked(record)
            if not _audio_stop_authored_locked(record):
                return lifecycle["phase"]
            states = _audio_continuous_states_locked(record)
            for layer, state in tuple(states.items()):
                states[layer] = ContinuousLayer(generation=state.generation + 1)
            lifecycle["phase"] = "WAIT_CONTEXT"
            _audio_commit_context_locked(record, cues)
            lifecycle["phase"] = "LIVE"
            _audio_apply_output_gate_locked(record)
            return "TITLE_CONTEXT_COMMITTED"

    if audio_adapter_refresh_output_gate not in config.interact_callbacks:
        config.interact_callbacks.append(audio_adapter_refresh_output_gate)
    if audio_adapter_refresh_output_gate not in config.periodic_callbacks:
        config.periodic_callbacks.append(audio_adapter_refresh_output_gate)
