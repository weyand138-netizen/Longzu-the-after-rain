# Continuous playback core only. No production cue/scene or output is admitted
# here. Future catalogue and lifecycle integration must supply those boundaries.
init 10 python:
    from modules.audio_continuous import (
        ContinuousCue, ContinuousLayer, request_continuous,
        fault_continuous, finish_continuous,
    )

    _AUDIO_CONTINUOUS_CHANNELS = {
        "music": ("audio_music_a", "audio_music_b"),
        "ambience": ("audio_ambience_a", "audio_ambience_b"),
    }
    _AUDIO_ADMITTED_CONTINUOUS_CUES = {}

    for _audio_layer, _audio_channels in _AUDIO_CONTINUOUS_CHANNELS.items():
        for _audio_channel in _audio_channels:
            renpy.music.register_channel(
                _audio_channel, mixer="music" if _audio_layer == "music" else "ambience",
                loop=True, stop_on_mute=False, tight=False,
                buffer_queue=True, synchro_start=False,
            )
    for _audio_index in range(4):
        renpy.music.register_channel(
            "audio_oneshot_{}".format(_audio_index), mixer="sfx", loop=False,
            stop_on_mute=False, tight=False, buffer_queue=True, synchro_start=False,
        )
    renpy.music.register_channel(
        "audio_role_voice", mixer="voice", loop=False,
        stop_on_mute=False, tight=False, buffer_queue=True, synchro_start=False,
    )

    def _audio_continuous_states_locked(record):
        # Same record and RLock as the existing notification owner. No imported
        # module, store default, save field or persistent leaf owns live state.
        return record.setdefault("continuous_layers", {
            "music": ContinuousLayer(), "ambience": ContinuousLayer(),
        })

    def _audio_execute_continuous_locked(record, layer, state, commands):
        states = _audio_continuous_states_locked(record)
        channels = _AUDIO_CONTINUOUS_CHANNELS[layer]
        states[layer] = state
        try:
            for command in commands:
                channel = channels[command.slot]
                if command.operation == "stop":
                    renpy.music.stop(channel=channel, fadeout=command.fade_seconds)
                else:
                    renpy.music.play(command.filename, channel=channel, loop=True,
                                     fadein=command.fade_seconds, if_changed=False)
        except Exception as exc:
            # A dispatch exception affects only this layer. Deferred decoder/
            # device failures require the later periodic fault observer.
            for channel in channels:
                try:
                    renpy.music.stop(channel=channel, fadeout=0)
                except Exception:
                    pass
            states[layer] = fault_continuous(state)
            record.setdefault("continuous_faults", {})[layer] = type(exc).__name__
        return states[layer]

    def audio_adapter_request_continuous(cue_id):
        if not isinstance(cue_id, str):
            return "INVALID"
        cue = _AUDIO_ADMITTED_CONTINUOUS_CUES.get(cue_id)
        if not isinstance(cue, ContinuousCue):
            return "INVALID"
        record = _notification_session_record()
        with record["lock"]:
            if not _AUDIO_ENGINE_GATE_SUPPORTED:
                return "FAULT_SILENT"
            if _audio_lifecycle_locked(record)["phase"] != "LIVE":
                return "GATED"
            _audio_apply_output_gate_locked(record)
            states = _audio_continuous_states_locked(record)
            state, commands = request_continuous(states[cue.layer], cue)
            if commands:
                state = _audio_execute_continuous_locked(record, cue.layer, state, commands)
                _audio_apply_output_gate_locked(record)
                state = states[cue.layer]
            return state.status

    def audio_adapter_finish_continuous(layer, generation):
        if layer not in _AUDIO_CONTINUOUS_CHANNELS:
            return "INVALID"
        record = _notification_session_record()
        with record["lock"]:
            states = _audio_continuous_states_locked(record)
            state, commands = finish_continuous(states[layer], generation)
            if commands:
                state = _audio_execute_continuous_locked(record, layer, state, commands)
            return state.status

    def _audio_reap_retiring_continuous_locked(record):
        """Retire completed fades from real channel state during normal play.

        The pure transition machine intentionally does not poll an engine.  The
        adapter does, so a normal A→B→C sequence reclaims the old physical
        channel without a testcase or chapter script calling a finish helper.
        """
        states = _audio_continuous_states_locked(record)
        for layer, state in tuple(states.items()):
            if state.retiring is None:
                continue
            channel = _AUDIO_CONTINUOUS_CHANNELS[layer][state.retiring]
            try:
                retired = renpy.music.get_playing(channel=channel) is None
            except Exception as exc:
                retired = False
                record.setdefault("continuous_faults", {})[channel] = type(exc).__name__
            if not retired:
                continue
            next_state, commands = finish_continuous(state, state.generation)
            if commands:
                _audio_execute_continuous_locked(record, layer, next_state, commands)
