# Shared action/notification voices; summary claims remain solely in 12_audio.
init 30 python:
    from modules.audio_oneshot import (
        OneShotCue, OneShotPool, claim_oneshot, dispatch_claimed_oneshot,
        reap_oneshots, retire_oneshots, allocate_oneshot_voice,
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
        # Notification cues can only use 12_audio's sealed-summary claim owner.
        # Reject before an authored claim can be created for that cue.
        if not isinstance(cue_id, str) or cue_id.startswith("audio.notification."):
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

    def audio_notification_output_inputs_locked(record, occurrence_id):
        """Inspect output only after 12_audio published its provisional claim."""
        claims = record["snapshot"].claims
        if (not claims or claims[-1].occurrence_id != occurrence_id or
                claims[-1].reason != "CLAIMED_PRE_GATE"):
            raise ValueError("Notification output requires the summary owner's claim")
        cue = _AUDIO_ADMITTED_ONESHOT_CUES.get("audio.notification.neutral_contact")
        asset_valid = (isinstance(cue, OneShotCue) and
                       cue.cue_id == "audio.notification.neutral_contact" and
                       cue.priority == "OPTIONAL_UI_NOTIFICATION" and
                       renpy.loadable(cue.filename))
        raw_sfx = _preferences.volumes.get("sfx", 1.0)
        if type(raw_sfx) not in (int, float) or not 0.0 <= raw_sfx <= 1.0:
            raise ValueError("Invalid SFX preference")
        # Ren'Py rewrites dict literals to rollback containers; the immutable
        # contract deliberately accepts only detached exact built-in dicts.
        preferences = builtins.dict({
            "main_gain_bps": (0 if audio_settings_game_gain() == 0 else
                              max(1, int(round(audio_settings_game_gain() * 10000)))),
            "global_game_mute": audio_settings_game_muted(),
            "environment_sfx_manual_mute": _preferences.mute.get("sfx", False),
            "environment_sfx_gain_bps": 0 if raw_sfx == 0 else max(1, int(round(raw_sfx * 10000))),
        })
        # Music mute has no bearing on the SFX-routed neutral notification.
        live = (_audio_lifecycle_locked(record)["phase"] == "LIVE" and
                not _notification_rollback_active() and not renpy.is_skipping())
        gates = builtins.dict({
            "asset_valid": bool(asset_valid),
            "blocking_safe": bool(live),
            "tts_active": bool(_audio_tts_suppressed()),
            "device_ready": bool(_AUDIO_ENGINE_GATE_SUPPORTED and _audio_engine.pcm_ok is True and
                                 not record.get("oneshot_faulted", False)),
            "pool_admitted": False,
        })
        eligible = (asset_valid and live and not gates["tts_active"] and gates["device_ready"] and
                    _audio_oneshot_raw_enabled())
        plan = None
        if eligible:
            pool = _audio_oneshot_pool_locked(record)
            busy = {i for i, channel in enumerate(_AUDIO_ONESHOT_CHANNELS)
                    if renpy.music.get_playing(channel=channel) is not None}
            pool = reap_oneshots(pool, busy)
            # This only chooses a voice. It cannot add notification identities
            # to pool.claimed or invent an authored-sfx occurrence.
            allocation = allocate_oneshot_voice(pool, cue, occurrence_id, True)
            gates["pool_admitted"] = allocation.disposition == "PLAY"
            if gates["pool_admitted"]:
                plan = (cue, allocation)
        return preferences, gates, plan

    def audio_adapter_dispatch_notification_locked(record, occurrence_id, plan):
        """Attempt one finalized summary dispatch without a second claim owner."""
        claims = tuple(claim for claim in record["snapshot"].claims
                       if claim.occurrence_id == occurrence_id)
        if plan is None or len(claims) != 1 or claims[0].disposition != "PLAY":
            return
        cue, allocation = plan
        record["oneshot_pool"] = allocation.pool
        _audio_apply_output_gate_locked(record)
        if not record.get("oneshot_gate_open", False):
            return
        channel = _AUDIO_ONESHOT_CHANNELS[allocation.slot]
        try:
            renpy.music.stop(channel=channel, fadeout=0)
            renpy.music.play(cue.filename, channel=channel, loop=False, if_changed=False)
        except Exception as exc:
            record["oneshot_faulted"] = True
            record["oneshot_last_fault"] = type(exc).__name__
            _audio_stop_oneshots_locked(record)
            _audio_apply_output_gate_locked(record)

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
                        _audio_oneshot_raw_enabled() and not record.get("ui_feedback_faulted", False))
            _audio_apply_output_gate_locked(record)
            if not eligible or not record.get("ui_feedback_gate_open", False):
                return None
            try:
                # Use Ren'Py's standard unbuffered sound channel. It is the
                # engine's immediate UI/SFX path. The physical output gate owns
                # project gain; reset legacy saved secondary gain to unity so
                # it cannot multiply the project setting a second time.
                renpy.music.set_volume(1.0, delay=0.0, channel="sound")
                renpy.music.play(
                    cue.filename, channel="sound", loop=False,
                    if_changed=False,
                )
                record["ui_feedback_last_play"] = (feedback_kind, sequence)
            except Exception as exc:
                # A UI cue must never block its button action.
                record["ui_feedback_faulted"] = True
                record["ui_feedback_last_fault"] = type(exc).__name__
                _audio_apply_output_gate_locked(record)
        # Ren'Py Function actions treat a non-None value as an interaction
        # result, which would prevent later actions in this button's list.
        return None

    def audio_ui_feedback_action(action, feedback_kind="click"):
        """Prepend feedback to a successful button action, flattening lists."""
        actions = list(action) if isinstance(action, (list, tuple)) else [action]
        return [Function(audio_dispatch_ui_feedback, feedback_kind)] + actions
