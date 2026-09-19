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
        """Provision only this game's preferences and its ambience mixer."""
        _preferences.init()
        _preferences.init_mixers()

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

        def get_volume(self):
            if _preferences.get_mute(self.mixer):
                return 0.0
            return super(AudioMixerVolumeValue, self).get_volume()

        def set_volume(self, volume):
            _preferences.set_mute(self.mixer, False)
            super(AudioMixerVolumeValue, self).set_volume(volume)

    if audio_settings_initialize not in config.start_callbacks:
        config.start_callbacks.append(audio_settings_initialize)
