# Project-only audio preferences.  These live in Ren'Py's preferences object,
# never in narrative save state or SYS-PERSIST.
init -999 python:
    import renpy.preferences as _audio_preferences_module

    _audio_preferences_module.Preference("rain_after_game_audio_gain", 1.0, (int, float))
    _audio_preferences_module.Preference("rain_after_game_audio_muted", False, bool)
    # The engine runs its broad preference type assertion later in init.  Add
    # these newly registered fields before that assertion, including on a
    # first launch with no existing preferences object field.
    _preferences.init()

init 5 python:
    from renpy.ui import BarValue
    import renpy.ui as _audio_ui

    _AUDIO_GAME_GAIN_PREFERENCE = "rain_after_game_audio_gain"
    _AUDIO_GAME_MUTE_PREFERENCE = "rain_after_game_audio_muted"

    def audio_settings_initialize():
        """Provision project preferences without changing SAPI's voice mixer."""
        _preferences.init()
        _preferences.init_mixers()
        # With no audio device the engine may omit unused mixers. Provision
        # this independent reserved category without clobbering a saved value.
        _preferences.volumes.setdefault("role_voice", 1.0)
        _preferences.mute.setdefault("role_voice", False)

    def audio_settings_game_gain():
        try:
            value = getattr(_preferences, _AUDIO_GAME_GAIN_PREFERENCE)
        except Exception:
            return 1.0
        if type(value) not in (int, float):
            return 1.0
        return min(1.0, max(0.0, float(value)))

    def audio_settings_game_muted():
        try:
            return getattr(_preferences, _AUDIO_GAME_MUTE_PREFERENCE) is True
        except Exception:
            return False

    def audio_settings_game_output_multiplier():
        # This intentionally never reads or writes the engine's "main" or
        # "voice" mixer, preserving system self-voicing volume unchanged.
        return 0.0 if audio_settings_game_muted() else audio_settings_game_gain()

    def _audio_settings_refresh():
        try:
            audio_adapter_refresh_output_gate()
        except Exception:
            pass
        renpy.restart_interaction()

    def audio_settings_set_game_gain(value):
        if type(value) not in (int, float):
            return
        setattr(_preferences, _AUDIO_GAME_GAIN_PREFERENCE, min(1.0, max(0.0, float(value))))
        _audio_settings_refresh()

    def audio_settings_set_visible_game_gain(value):
        """Convert the legacy master-mute overlay into the visible slider value."""
        if type(value) not in (int, float):
            return
        setattr(_preferences, _AUDIO_GAME_MUTE_PREFERENCE, False)
        audio_settings_set_game_gain(value)

    def audio_settings_toggle_game_mute():
        # Keep the prior gain intact so unmute restores exactly that setting.
        setattr(_preferences, _AUDIO_GAME_MUTE_PREFERENCE, not audio_settings_game_muted())
        _audio_settings_refresh()

    class AudioGameVolumeValue(BarValue):
        """A focusable 0–100% control for the project's gated channels only."""
        force_step = True

        @property
        def alt(self):
            value = 0.0 if audio_settings_game_muted() else audio_settings_game_gain()
            return audio_settings_volume_alt("主音量", value)

        def get_adjustment(self):
            return _audio_ui.adjustment(
                range=1.0,
                value=(0.0 if audio_settings_game_muted() else audio_settings_game_gain()),
                changed=audio_settings_set_visible_game_gain,
                step=0.05,
                force_step=True,
            )

        def get_style(self):
            return "slider", "vslider"

    class AudioMixerVolumeValue(MixerValue):
        """A slider-only category control compatible with legacy mute fields."""

        def __init__(self, mixer):
            super(AudioMixerVolumeValue, self).__init__(mixer, force_step=False)

        @property
        def alt(self):
            # Match the engine's slider position, including its logarithmic
            # volume mapping; raw linear amplitude is not the visible percent.
            maximum = 1.0 if config.quadratic_volumes else float(config.volume_db_range)
            return audio_settings_volume_alt(
                {"music": "音乐", "ambience": "环境", "sfx": "音效"}[self.mixer],
                self.get_mixer() / maximum,
            )

        def get_volume(self):
            if _preferences.get_mute(self.mixer):
                return 0.0
            return super(AudioMixerVolumeValue, self).get_volume()

        def set_volume(self, volume):
            _preferences.set_mute(self.mixer, False)
            super(AudioMixerVolumeValue, self).set_volume(volume)

    def audio_settings_volume_alt(label, fraction):
        # Reserve "0%" for actual slider zero, rather than rounding a small
        # nonzero value into an apparent mute. Reading has no side effects.
        percent = 0 if fraction <= 0.0 else min(100, max(1, int(round(fraction * 100))))
        return "{}，当前 {}%，立即生效；0% 为静音。".format(label, percent)

    _AUDIO_TTS_SESSION_KEY = "audio-settings:self-voicing-status:v1"

    def _audio_settings_tts_record():
        # Process handles are session-only; never store them in saves or
        # persistent preferences. No voice enumeration or probe utterance.
        return renpy.session.setdefault(_AUDIO_TTS_SESSION_KEY, {
            "mode": _preferences.self_voicing,
            "phase": "unverified",
            "process": None,
            "status_dirty": False,
        })

    def audio_settings_self_voicing_label():
        mode = _preferences.self_voicing
        if mode == "clipboard":
            return "自朗读：剪贴板"
        if mode == "debug":
            return "自朗读：调试"
        return "自朗读：开" if mode else "自朗读：关"

    def audio_settings_self_voicing_status():
        mode = _preferences.self_voicing
        if not mode:
            return "自朗读已关闭。"
        if mode == "clipboard":
            return "已启用剪贴板朗读；请使用外部屏幕阅读器。"
        if mode == "debug":
            return "已启用朗读调试；此模式不会发声。"
        record = _audio_settings_tts_record()
        if record["mode"] == mode and record["phase"] == "failed":
            return "系统朗读未能完成；请检查 Windows 中文语音与系统音量，或关闭后重试。"
        return "自朗读已开启；中文发音尚未验证。若无声音，请检查 Windows 中文语音与系统音量。"

    def audio_settings_self_voicing_alt():
        return "{}。{} 系统朗读音量独立于游戏音量。".format(
            audio_settings_self_voicing_label(), audio_settings_self_voicing_status())

    # Observe only speech the engine was already asked to produce. Catching
    # dispatch errors here retains a readable failure that Ren'Py tick() would
    # otherwise silently discard. No extra Speak, COM call, wait, or network.
    _audio_settings_tts_delegate = config.tts_function

    def _audio_settings_observed_tts(text):
        import renpy.display.tts as _settings_tts
        record = _audio_settings_tts_record()
        record.update(mode=_preferences.self_voicing, phase="unverified", process=None)
        try:
            result = _audio_settings_tts_delegate(text)
        except Exception:
            record["phase"] = "failed"
            record["status_dirty"] = True
            return None
        record["process"] = _settings_tts.process
        return result

    def audio_settings_poll_self_voicing():
        record = _audio_settings_tts_record()
        before = (record["mode"], record["phase"])
        mode = _preferences.self_voicing
        if record["mode"] != mode:
            record.update(mode=mode, phase="unverified", process=None)
        process = record["process"]
        if mode is True and process is not None:
            try:
                code = process.poll()
            except Exception:
                code = -1
            if code is not None:
                # Exit 0 proves only process completion. It cannot establish
                # that a Chinese voice exists or that the player heard speech.
                record.update(phase=("failed" if code else "unverified"), process=None)
        changed = record.pop("status_dirty", False) or before != (record["mode"], record["phase"])
        if changed and renpy.get_screen("preferences"):
            renpy.restart_interaction()

    config.tts_function = _audio_settings_observed_tts
    if audio_settings_poll_self_voicing not in config.periodic_callbacks:
        # Pinned SDK core invokes these before tts.periodic clears a finished
        # process, so a nonzero exit remains observable without blocking.
        config.periodic_callbacks.append(audio_settings_poll_self_voicing)

    if audio_settings_initialize not in config.start_callbacks:
        config.start_callbacks.append(audio_settings_initialize)
