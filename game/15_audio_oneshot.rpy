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
