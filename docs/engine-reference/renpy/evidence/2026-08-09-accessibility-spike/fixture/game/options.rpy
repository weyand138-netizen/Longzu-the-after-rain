define config.name = "RenPy Accessibility Spike"
define config.version = "a11y-spike-2026-08-09"
define config.window_title = "RenPy Accessibility Spike"
define config.screen_width = 1280
define config.screen_height = 720
define config.window = "auto"
define config.has_sound = False
define config.has_music = False
define config.has_voice = False
define config.scrollbar_child_size = False

init python:
    config.scrollbar_child_size = False
    config.keymap["self_voicing"] = ["K_F9"]
    config.keymap["toggle_skip"] = []
    config.keymap["focus_graph_next"] = ["K_TAB"]
    config.keymap["focus_graph_previous"] = ["shift_K_TAB"]
    config.keymap["focus_down"] = ["anyrepeat_K_DOWN", "anyrepeat_KP_DOWN"]
    config.keymap["focus_up"] = ["anyrepeat_K_UP", "anyrepeat_KP_UP"]
