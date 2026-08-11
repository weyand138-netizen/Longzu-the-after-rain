# VERTICAL SLICE - NOT FOR PRODUCTION
# Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality?
# Date: 2026-07-23

define config.name = _("雨停之后：垂直切片")
define config.version = "vs-0.1.0"
define config.window_title = "雨停之后 — 垂直切片（非正式游戏）"
define config.screen_width = 1920
define config.screen_height = 1080
define config.physical_width = 1280
define config.physical_height = 720
define config.window = "auto"
define config.rollback_enabled = True
define config.default_text_cps = 32
define config.check_conflicting_properties = True
define config.has_sound = False
define config.has_music = False
define config.has_voice = False
define config.save_directory = "rain-after-vertical-slice-20260723"

init python:
    build.name = "rain-after-vertical-slice"
    build.directory_name = "rain-after-vertical-slice"
    build.executable_name = "雨停之后-垂直切片"
