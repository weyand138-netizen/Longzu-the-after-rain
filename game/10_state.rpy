default understanding = 0
default autonomy = 0
default truth = 0
default preparation = 0
default sacrifice = 0
default choice_history = []
default current_chapter = "prologue"
default tension_mode_enabled = False
default save_contract_sentinel = None
default save_catalog_generation_id = None
default semantic_state = None
default state_schema_sentinel = None
default ending_flow_sentinel = None
default ending_flow_state = None
default pending_ending_id = None

init python:
    import builtins
    from modules.ending_rules import AXES, ENDING_TITLES, resolve_ending
    from modules.accessibility_focus import FocusAwareGraph
    from modules.persist_schema import (
        build_fresh_persist_root,
        validate_persist_root,
    )
    from modules.narrative_token_projection import has_unresolved_token as _has_unresolved_token

    def reset_run_state():
        global understanding, autonomy, truth, preparation, sacrifice
        global choice_history, current_chapter

        understanding = 0
        autonomy = 0
        truth = 0
        preparation = 0
        sacrifice = 0
        choice_history = []
        current_chapter = "prologue"

    def _clamp_axis(value):
        return max(0, min(3, value))

    def apply_choice(choice_id, deltas):
        global understanding, autonomy, truth, preparation, sacrifice
        global choice_history

        unknown = [key for key in deltas if key not in AXES]
        if unknown:
            raise ValueError("Unknown story axes: {!r}".format(unknown))

        understanding = _clamp_axis(
            understanding + deltas.get("understanding", 0)
        )
        autonomy = _clamp_axis(autonomy + deltas.get("autonomy", 0))
        truth = _clamp_axis(truth + deltas.get("truth", 0))
        preparation = _clamp_axis(
            preparation + deltas.get("preparation", 0)
        )
        sacrifice = _clamp_axis(sacrifice + deltas.get("sacrifice", 0))
        choice_history = choice_history + [choice_id]

    def current_axis_snapshot():
        return {
            "understanding": understanding,
            "autonomy": autonomy,
            "truth": truth,
            "preparation": preparation,
            "sacrifice": sacrifice,
        }

    def has_unresolved_token(token_id):
        """Expose the pure canonical-history token projection to narrative labels."""

        return _has_unresolved_token(choice_history, token_id)

    def preview_current_ending():
        return resolve_ending(current_axis_snapshot())

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
