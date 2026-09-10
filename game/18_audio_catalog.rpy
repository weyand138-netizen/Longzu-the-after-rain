# Formal runtime admission.  A stale source or changed binary leaves the game
# silent and makes the packaging preflight fail; it never retargets a cue.
init 50 python:
    from modules.audio_catalog import compile_production_scene_catalog, verify_audio_assets
    from modules.audio_production_catalog import (
        ACTION_BINDINGS, CONTEXT_RANGES, CONTINUOUS_CUES, ONESHOT_CUES,
        RESTORE_CONTEXTS, RUNTIME_AUDIO_ASSETS, validate_production_definition,
    )

    _AUDIO_CATALOG_STATUS = "UNINITIALIZED"
    _AUDIO_CATALOG_ERROR = None

    def _audio_catalog_read_file(path):
        with renpy.file(path) as handle:
            return handle.read()

    try:
        validate_production_definition()
        verify_audio_assets(RUNTIME_AUDIO_ASSETS, _audio_catalog_read_file)
        _audio_catalog = compile_production_scene_catalog(
            CONTEXT_RANGES, ACTION_BINDINGS, _audio_catalog_read_file
        )
        _AUDIO_ADMITTED_CONTINUOUS_CUES.clear()
        _AUDIO_ADMITTED_CONTINUOUS_CUES.update({cue.cue_id: cue for cue in CONTINUOUS_CUES})
        _AUDIO_ADMITTED_ONESHOT_CUES.clear()
        _AUDIO_ADMITTED_ONESHOT_CUES.update({cue.cue_id: cue for cue in ONESHOT_CUES})
        _AUDIO_RESTORE_CONTEXTS.clear()
        _AUDIO_RESTORE_CONTEXTS.update(RESTORE_CONTEXTS)
        _AUDIO_ADMITTED_SCENE_ANCHORS = _audio_catalog.anchors
        if not audio_scene_install(_audio_catalog.anchors, _audio_catalog.ranges):
            raise ValueError("Audio scene installation rejected production catalogue")
    except Exception as exc:
        _AUDIO_ADMITTED_CONTINUOUS_CUES.clear()
        _AUDIO_ADMITTED_ONESHOT_CUES.clear()
        _AUDIO_RESTORE_CONTEXTS.clear()
        _AUDIO_ADMITTED_SCENE_ANCHORS = ()
        audio_scene_install((), ())
        _AUDIO_CATALOG_STATUS = "FAILED"
        _AUDIO_CATALOG_ERROR = type(exc).__name__
    else:
        _AUDIO_CATALOG_STATUS = "READY"
