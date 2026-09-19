## Reusable real-time weather controller.
##
## Weather state is deliberately kept separate from background images. The
## controller only supplies interpolated parameters to overlay displayables;
## it never moves, scales, or replaces the current scene image.

default weather_enabled = False
default weather_name = "after_rain"
default weather_transition = None
default weather_masks = {
    "sky": None,
    "ground": None,
    "roof": None,
    "distance": None,
}

define weather_white_mask = Solid("#ffffff")

init -100 python:
    # The weather layer is above scene art but below transient dialogue and
    # screens. It therefore cannot affect focus, buttons, or the fixed camera.
    if "weather" not in config.layers:
        renpy.add_layer("weather", below="transient", menu_clear=False)

init python:
    import renpy.store as store

    WEATHER_PRESETS = {
        "sunset": {
            "rain_strength": 0.0,
            "wind": 0.10,
            "rain_fog_strength": 0.0,
            "sunset_strength": 0.90,
            "godray_strength": 0.70,
            "cloud_darkness": 0.20,
        },
        "drizzle": {
            "rain_strength": 0.20,
            "wind": 0.20,
            "rain_fog_strength": 0.15,
            "sunset_strength": 0.60,
            "godray_strength": 0.40,
            "cloud_darkness": 0.40,
        },
        # A cool, wet menu-only overcast profile. It intentionally has no
        # amber horizon pass: the matching menu artwork is fully clouded.
        "overcast": {
            "rain_strength": 0.18,
            "wind": 0.16,
            "rain_fog_strength": 0.32,
            "sunset_strength": 0.0,
            "godray_strength": 0.0,
            "cloud_darkness": 0.58,
        },
        "rain": {
            "rain_strength": 0.55,
            "wind": 0.35,
            "rain_fog_strength": 0.45,
            "sunset_strength": 0.25,
            "godray_strength": 0.15,
            "cloud_darkness": 0.70,
        },
        "storm": {
            "rain_strength": 1.0,
            "wind": 0.70,
            "rain_fog_strength": 0.80,
            "sunset_strength": 0.0,
            "godray_strength": 0.0,
            "cloud_darkness": 1.0,
        },
        "after_rain": {
            "rain_strength": 0.0,
            "wind": 0.05,
            "rain_fog_strength": 0.20,
            "sunset_strength": 0.50,
            "godray_strength": 0.30,
            "cloud_darkness": 0.25,
        },
    }

    WEATHER_PARAMETER_NAMES = tuple(next(iter(WEATHER_PRESETS.values())).keys())

    def _weather_now():
        """Ren'Py's time-warp aware clock, used for deterministic test runs."""
        return renpy.display.core.get_time()

    def _weather_smoothstep(value):
        value = max(0.0, min(1.0, value))
        return value * value * (3.0 - 2.0 * value)

    def _weather_copy(values):
        return {name: float(values[name]) for name in WEATHER_PARAMETER_NAMES}

    def weather_params(now=None):
        """Return the current interpolated weather parameters without mutation."""
        if now is None:
            now = _weather_now()

        transition = store.weather_transition
        if not transition:
            return _weather_copy(WEATHER_PRESETS[store.weather_name])

        started, duration, source, target = transition
        if duration <= 0.0:
            return _weather_copy(target)

        eased = _weather_smoothstep((now - started) / duration)
        return {
            name: source[name] + (target[name] - source[name]) * eased
            for name in WEATHER_PARAMETER_NAMES
        }

    def set_weather(name, duration=5.0, activate=True):
        """Smoothly transition the reusable weather layer to a named preset.

        Example: ``$ set_weather("storm", duration=15.0)``.
        ``activate=False`` is reserved for menu previews; story calls use the
        default and automatically put the overlay on the weather layer.
        """
        if name not in WEATHER_PRESETS:
            raise ValueError("Unknown weather preset: {!r}".format(name))

        duration = float(duration)
        if duration < 0.0:
            raise ValueError("Weather transition duration must be >= 0.0")

        now = _weather_now()
        store.weather_transition = (
            now,
            duration,
            weather_params(now),
            _weather_copy(WEATHER_PRESETS[name]),
        )
        store.weather_name = name

        if activate:
            store.weather_enabled = True
            renpy.show_screen("weather_scene_overlay", _layer="weather")

        renpy.restart_interaction()

    def disable_weather():
        """Hide all narrative weather overlays while leaving the selected preset intact."""
        store.weather_enabled = False
        renpy.hide_screen("weather_scene_overlay", layer="weather")
        renpy.restart_interaction()

    def set_weather_mask(kind, path=None):
        """Assign an optional black/white mask for sky, ground, roof, or distance."""
        if kind not in store.weather_masks:
            raise ValueError("Unknown weather mask: {!r}".format(kind))
        if path is not None and not renpy.loadable(path):
            raise ValueError("Weather mask is not loadable: {!r}".format(path))

        updated_masks = dict(store.weather_masks)
        updated_masks[kind] = path
        store.weather_masks = updated_masks
        renpy.restart_interaction()

    def weather_mask_payload(kind):
        """Return a sampler and an enabled flag without per-frame I/O."""
        path = store.weather_masks[kind]
        if path is None:
            return store.weather_white_mask, 0.0
        return path, 1.0

    def weather_motion_allowed():
        """Honor the project's reduced-motion accessibility setting."""
        try:
            return not persistent.sys_persist_state["settings"]["reduced_motion"]
        except Exception:
            return True

    def set_weather_preview(name):
        """Set menu-preview parameters without retaining a story overlay."""
        # The title embeds weather_effects beneath its controls. Clear a
        # possible narrative-layer screen first, otherwise returning to the
        # menu from a rainy scene could draw two independent rain passes.
        store.weather_enabled = False
        renpy.hide_screen("weather_scene_overlay", layer="weather")
        set_weather(name, duration=0.0, activate=False)
