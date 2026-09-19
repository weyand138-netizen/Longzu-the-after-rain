# Authored action/UI one-shot pool. Notification summary claims remain owned by
# 12_audio; no notification cue or live scene binding is admitted here.
init 30 python:
    from modules.audio_oneshot import (
        OneShotCue, OneShotPool, claim_oneshot, dispatch_claimed_oneshot,
        reap_oneshots, retire_oneshots,
    )
    _AUDIO_ADMITTED_ONESHOT_CUES = {}
    _AUDIO_ONESHOT_CHANNELS = tuple("audio_oneshot_{}".format(i) for i in range(4))

    def _audio_oneshot_pool_locked(record):
        return record.setdefault("oneshot_pool", OneShotPool())

    def _audio_oneshot_raw_enabled():
        try:
            sfx = _preferences.volumes.get("sfx", 1.0)
            return (audio_settings_game_output_multiplier() > 0 and
                    type(sfx) in (int, float) and 0 < sfx <= 1 and
                    _preferences.mute.get("sfx", False) is False)
        except Exception:
            return False

    def _audio_stop_oneshots_locked(record):
        for channel in _AUDIO_ONESHOT_CHANNELS:
            try:
                renpy.music.stop(channel=channel, fadeout=0)
            except Exception as exc:
                record["oneshot_faulted"] = True
                record["oneshot_last_fault"] = type(exc).__name__
        record["oneshot_pool"] = retire_oneshots(_audio_oneshot_pool_locked(record))

    def audio_adapter_dispatch_oneshot(cue_id, occurrence_id):
        if not isinstance(cue_id, str):
            return "INVALID"
        cue = _AUDIO_ADMITTED_ONESHOT_CUES.get(cue_id)
        if not isinstance(cue, OneShotCue):
            return "INVALID"
        record = _notification_session_record()
        with record["lock"]:
            pool, disposition = claim_oneshot(_audio_oneshot_pool_locked(record), occurrence_id)
            record["oneshot_pool"] = pool
            if disposition is not None:
                return disposition
            # Claim is installed before every preference/device/lifecycle gate.
            eligible = (_AUDIO_ENGINE_GATE_SUPPORTED and _audio_engine.pcm_ok is True and
                        _audio_lifecycle_locked(record)["phase"] == "LIVE" and
                        not _audio_tts_suppressed() and not _notification_rollback_active() and
                        _audio_oneshot_raw_enabled() and not record.get("oneshot_faulted", False))
            if eligible:
                try:
                    busy = {i for i, channel in enumerate(_AUDIO_ONESHOT_CHANNELS)
                            if renpy.music.get_playing(channel=channel) is not None}
                    pool = reap_oneshots(pool, busy)
                except Exception:
                    eligible = False
            decision = dispatch_claimed_oneshot(pool, cue, occurrence_id, eligible)
            record["oneshot_pool"] = decision.pool
            if decision.disposition != "PLAY":
                _audio_apply_output_gate_locked(record)
                return decision.disposition
            channel = _AUDIO_ONESHOT_CHANNELS[decision.slot]
            try:
                _audio_apply_output_gate_locked(record)
                # No queue and no if_changed shortcut; stop completes before reuse.
                renpy.music.stop(channel=channel, fadeout=0)
                renpy.music.play(cue.filename, channel=channel, loop=False, if_changed=False)
            except Exception as exc:
                record["oneshot_faulted"] = True
                record["oneshot_last_fault"] = type(exc).__name__
                _audio_stop_oneshots_locked(record)
                _audio_apply_output_gate_locked(record)
            # PLAY records an attempted dispatch, not a promise of audible success.
            return decision.disposition

    _AUDIO_UI_FEEDBACK_CUES = {
        "click": "audio.ui.click_soft",
        "choice": "audio.ui.choice_confirm",
    }

    def audio_dispatch_ui_feedback(feedback_kind):
        """Play one immediate UI confirmation outside narrative reconstruction."""
        cue_id = _AUDIO_UI_FEEDBACK_CUES.get(feedback_kind)
        if cue_id is None:
            return None
        cue = _AUDIO_ADMITTED_ONESHOT_CUES.get(cue_id)
        if not isinstance(cue, OneShotCue):
            return None
        record = _notification_session_record()
        with record["lock"]:
            sequence = record.get("ui_feedback_sequence", 0) + 1
            record["ui_feedback_sequence"] = sequence
            eligible = (_AUDIO_ENGINE_GATE_SUPPORTED and _audio_engine.pcm_ok is True and
                        _audio_lifecycle_locked(record)["phase"] == "LIVE" and
                        not _audio_tts_suppressed() and not _notification_rollback_active() and
                        _audio_oneshot_raw_enabled())
            if not eligible:
                return None
            try:
                # Use Ren'Py's standard unbuffered sound channel. It is the
                # engine's device-tested UI/SFX path and is not part of the
                # narrative channel set rebuilt by Start/MainMenu actions.
                # Project master gain and the SFX mixer both still apply.
                renpy.music.set_volume(
                    audio_settings_game_output_multiplier(), delay=0.0,
                    channel="sound",
                )
                renpy.music.play(
                    cue.filename, channel="sound", loop=False,
                    if_changed=False,
                )
                record["ui_feedback_last_play"] = (feedback_kind, sequence)
            except Exception as exc:
                # A UI cue must never block its button action.
                record["ui_feedback_last_fault"] = type(exc).__name__
        # Ren'Py Function actions treat a non-None value as an interaction
        # result, which would prevent later actions in this button's list.
        return None

    def audio_ui_feedback_action(action, feedback_kind="click"):
        """Prepend feedback to a successful button action, flattening lists."""
        actions = list(action) if isinstance(action, (list, tuple)) else [action]
        return [Function(audio_dispatch_ui_feedback, feedback_kind)] + actions
