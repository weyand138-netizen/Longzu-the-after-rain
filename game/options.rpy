define config.name = _("雨停之后")
define config.version = "1-test-0.3.0"
define config.window_title = "雨停之后 — 《龙族》非官方同人视觉小说"
define config.window_icon = "gui/window_icon.png"

define config.screen_width = 1920
define config.screen_height = 1080
define config.physical_width = 1280
define config.physical_height = 720
# Ren'Py defaults this to 400 MiB, which can retain almost every decoded
# runtime texture. 128 MiB covers the active scene and nearby predictions
# while evicting portraits and backgrounds from completed scenes.
define config.image_cache_size_mb = 128
define config.window = "auto"
define config.rollback_enabled = True
define config.quicksave_slots = 3
define config.autosave_slots = 6
define config.default_text_cps = 35
define config.check_conflicting_properties = True

define config.has_sound = True
define config.has_music = True
define config.has_voice = True

# This candidate writes to its own Ren'Py preference/save namespace, leaving
# an existing player or development build's saves untouched.
define config.save_directory = "after-rain-v1-test-0.3.0"

init -999 python:
    # Keep the production virtual layout at 1920x1080, but render every
    # engine-hosted testcase at the Sprint 1 720p accessibility baseline.
    if renpy.game.args.command == "test":
        config.screen_width = 1280
        config.screen_height = 720

init python:
    build.name = "After-Rain"
    build.directory_name = "After-Rain-v1-test-0.3.0"
    build.executable_name = "After rain"

    # Ren'Py applies classifications from first match to last match. Admit
    # each distribution document before excluding its source directory.
    build.classify("README.md", "all")
    build.classify("README_EN.md", "all")

    # These workspace-only game subtrees must stop traversal before the
    # broader game directory admission below.
    build.classify("game/cache/", None)
    build.classify("game/cache/**", None)
    build.classify("game/saves/", None)
    build.classify("game/saves/**", None)
    build.classify("game/assets/backgrounds/sources/", None)
    build.classify("game/assets/backgrounds/sources/**", None)
    build.classify("game/assets/**/variants/", None)
    build.classify("game/assets/**/variants/**", None)

    # Ren'Py decides whether to recurse before it classifies a nested file.
    # These rules permit traversal only; the file-level admissions below and
    # final deny rule still determine what is distributed.
    build.classify("game/", "all")
    build.classify("game/**/", "all")

    # Keep the workspace, generated evidence, original masters, and local
    # saves out of the candidate. The final catch-all below is deliberately
    # after the runtime admissions, as Ren'Py uses the first matching rule.
    build.classify("art/", None)
    build.classify("art/**", None)
    build.classify("Formal assets/", None)
    build.classify("Formal assets/**", None)
    build.classify("Codex/", None)
    build.classify("Codex/**", None)
    build.classify("tools/", None)
    build.classify("tools/**", None)
    build.classify("production/", None)
    build.classify("production/**", None)
    build.classify("prototypes/", None)
    build.classify("prototypes/**", None)
    build.classify("tests/", None)
    build.classify("tests/**", None)
    build.classify("design/", None)
    build.classify("design/**", None)
    build.classify("__pycache__/", None)
    build.classify("__pycache__/**", None)
    build.classify("game/testcases.rpy", None)
    build.classify("game/testcases.rpyc", None)

    # Keep local QA helpers and visual candidates out of release archives.
    # They remain in the workspace until their evidence and asset-gate review
    # are complete.
    _development_only_modules = (
        "achievement_ui.py", "action_gates.py", "artifact_lifecycle.py",
        "blocking_safe_flow.py", "build_evidence.py",
        "ending_completion_restore.py", "evidence_bundle.py",
        "external_evidence.py", "gate_execution.py", "journal_gate.py",
        "load_classification.py", "narrative_partial_manifest.py",
        "persist_performance.py", "persist_recovery.py",
        "persistent_boundary.py", "production_closeout.py",
        "restore_semantics.py", "save_operations.py", "save_performance.py",
        "save_ui.py", "settings_flow.py", "test_manifest.py",
        "toolchain_isolation.py",
    )
    for _module_name in _development_only_modules:
        build.classify("game/modules/" + _module_name, None)

    _unadmitted_visual_candidates = (
        "game/assets/backgrounds/bg_main_menu_golden_hour.png",
        "game/assets/backgrounds/bg_main_menu_rain_after_station.png",
        "game/assets/ui/main_menu_golden_hour_tyndall_overlay.png",
        "game/assets/characters/erii/char_erii_arcade_input.png",
        "game/assets/characters/erii/char_erii_check_clothing_cuff.png",
        "game/assets/characters/lu_mingfei/char_lu_mingfei_wait_with_ticket.png",
        "game/assets/characters/npc/npc_ticket_clerk_check_card.png",
        "game/assets/characters/npc/npc_ticket_clerk_return_card.png",
        "game/assets/characters/npc/npc_train_attendant_passing.png",
        "game/assets/props/prop_archive_original_pages.png",
        "game/assets/props/prop_archive_summary_pages.png",
        "game/assets/props/prop_contact_card_blank.png",
        "game/assets/props/prop_folded_route_map.png",
        "game/assets/props/prop_train_ticket_blank.png",
    )
    for _candidate_path in _unadmitted_visual_candidates:
        build.classify(_candidate_path, None)

    # Ship compiled game scripts only. Source remains in Git for continued
    # development but is not needed by players at runtime.
    build.classify("game/**.rpy", None)
    build.classify("game/**.rpyc", "all")
    build.classify("game/**.py", "all")
    build.classify("game/**.png", "archive")
    build.classify("game/**.jpg", "archive")
    build.classify("game/**.webp", "archive")
    build.classify("game/**.ogg", "archive")
    build.classify("game/**.opus", "archive")
    build.classify("game/**.wav", "archive")
    build.classify("game/**.ttf", "archive")
    build.classify("game/archive.rpa", "all")
    build.classify("**", None)

    build.documentation("README.md")
    build.documentation("README_EN.md")
    build.package("win", "zip", "windows renpy all")

    # P0 keyboard navigation: Tab/Shift+Tab are focus traversal, not skip.
    config.keymap["toggle_skip"] = []
    config.keymap["focus_graph_next"] = ["K_TAB"]
    config.keymap["focus_graph_previous"] = ["shift_K_TAB"]
    config.keymap["focus_down"] = ["anyrepeat_K_DOWN", "anyrepeat_KP_DOWN"]
    config.keymap["focus_up"] = ["anyrepeat_K_UP", "anyrepeat_KP_UP"]
