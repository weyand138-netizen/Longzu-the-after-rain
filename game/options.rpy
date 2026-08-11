define config.name = _("雨停之后")
define config.version = "0.1.0-dev"
define config.window_title = "雨停之后 — 《龙族》非官方同人视觉小说"

define config.screen_width = 1920
define config.screen_height = 1080
define config.physical_width = 1280
define config.physical_height = 720
define config.window = "auto"
define config.rollback_enabled = True
define config.quicksave_slots = 3
define config.autosave_slots = 6
define config.default_text_cps = 35
define config.check_conflicting_properties = True

define config.has_sound = True
define config.has_music = True
define config.has_voice = True

define config.save_directory = "rain-after-andwey-019f8e03"

init -999 python:
    # Keep the production virtual layout at 1920x1080, but render every
    # engine-hosted testcase at the Sprint 1 720p accessibility baseline.
    if renpy.game.args.command == "test":
        config.screen_width = 1280
        config.screen_height = 720

init python:
    build.name = "rain-after"
    build.directory_name = "rain-after-{version}"
    build.executable_name = "雨停之后"

    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("game/**.rpy", "all")
    build.classify("game/**.py", "all")
    build.classify("game/**.png", "archive")
    build.classify("game/**.jpg", "archive")
    build.classify("game/**.webp", "archive")
    build.classify("game/**.ogg", "archive")
    build.classify("game/**.opus", "archive")

    build.documentation("README.md")
    build.documentation("docs/legal/fan-work-notice.md")

    # P0 keyboard navigation: Tab/Shift+Tab are focus traversal, not skip.
    config.keymap["toggle_skip"] = []
    config.keymap["focus_graph_next"] = ["K_TAB"]
    config.keymap["focus_graph_previous"] = ["shift_K_TAB"]
    config.keymap["focus_down"] = ["anyrepeat_K_DOWN", "anyrepeat_KP_DOWN"]
    config.keymap["focus_up"] = ["anyrepeat_K_UP", "anyrepeat_KP_UP"]
