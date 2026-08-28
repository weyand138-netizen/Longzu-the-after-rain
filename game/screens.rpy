style default:
    font "assets/fonts/SourceHanSansLite.ttf"
    size 34
    color "#f5f1e8"
    outlines [(2, "#101722", 0, 0)]

style button:
    background Solid("#24374cdd")
    hover_background Solid("#38566f")
    padding (28, 18)
    key_events True

style button_text:
    size 32
    color "#f7ead1"
    hover_color "#ffffff"

style settings_section_title:
    size 32
    color "#f4d7c0"

style settings_status_text:
    size 24
    color "#8dcbd6"

style settings_option_button is button:
    background Solid("#22364bdd")
    hover_background Solid("#38566f")
    padding (20, 14)

style settings_option_button_text is button_text:
    size 27

style window:
    background Solid("#0b1320dd")
    padding (54, 34)

default critical_choice_interaction = False

init python:
    AUTO_FORWARD_SPEEDS = (2, 3, 4)
    _AUTO_FORWARD_TIME_BY_SPEED = {
        2: 0.50,
        3: 0.34,
        4: 0.25,
    }
    ENDING_TREE_LAYOUT = (
        ("unsent_postcard", 0),
        ("golden_cage", 1),
        ("one_person_train", 2),
        ("see_the_sea", 3),
        ("her_own_name", 4),
        ("rain_stops", 5),
    )
    def _current_auto_forward_speed():
        current_time = renpy.game.preferences.afm_time
        for speed, expected_time in _AUTO_FORWARD_TIME_BY_SPEED.items():
            if abs(current_time - expected_time) < 0.02:
                return speed
        return 2

    def toggle_auto_forward():
        preferences = renpy.game.preferences
        preferences.using_afm_enable = True
        preferences.afm_enable = not preferences.afm_enable
        if preferences.afm_enable and preferences.afm_time <= 0:
            preferences.afm_time = _AUTO_FORWARD_TIME_BY_SPEED[2]
        renpy.restart_interaction()

    def set_auto_forward_speed(speed):
        if speed not in AUTO_FORWARD_SPEEDS:
            raise ValueError("Unsupported auto-forward speed: {!r}".format(speed))
        preferences = renpy.game.preferences
        preferences.using_afm_enable = True
        preferences.afm_time = _AUTO_FORWARD_TIME_BY_SPEED[speed]
        preferences.afm_enable = True
        renpy.restart_interaction()

    def completed_ending_ids():
        root = persistent.sys_persist_state
        return tuple(root["ending_ids"])

transform life_tree_locked:
    alpha 0.34
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.42)

transform life_tree_lit_static:
    alpha 0.96
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(0.08)

transform life_tree_lit_pulse:
    alpha 0.72
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(0.08)
    block:
        linear 1.35 alpha 1.0 zoom 1.025
        linear 1.35 alpha 0.72 zoom 1.0
        repeat

transform life_tree_true_static:
    alpha 0.96
    matrixcolor TintMatrix("#c88e9d") * SaturationMatrix(0.0)

transform life_tree_true_pulse:
    alpha 0.72
    matrixcolor TintMatrix("#c88e9d") * SaturationMatrix(0.0)
    block:
        linear 1.35 alpha 1.0 zoom 1.035
        linear 1.35 alpha 0.72 zoom 1.0
        repeat

screen say(who, what):
    $ accessibility_settings = persistent.sys_persist_state["settings"]
    $ accessibility_scale = accessibility_settings["font_scale"]
    $ accessibility_high_contrast = accessibility_settings["high_contrast"]
    window:
        id "window"
        xalign 0.5
        yalign 0.94
        xsize 1760
        yminimum 230
        background Solid(("#000000f2" if accessibility_high_contrast else "#0b1320dd"))

        vbox:
            spacing 14
            if who is not None:
                text who:
                    id "who"
                    size int(36 * accessibility_scale)
                    color ("#ffffff" if accessibility_high_contrast else "#f2c6d3")
            text what:
                id "what"
                size int(34 * accessibility_scale)
                color ("#ffffff" if accessibility_high_contrast else "#f5f1e8")
                line_spacing 10

    if not critical_choice_interaction:
        use quick_menu
        $ auto_forward_enabled = renpy.game.preferences.afm_enable
        $ auto_forward_speed = _current_auto_forward_speed()
        hbox:
            xalign 0.93
            yalign 0.91
            spacing 8
            textbutton "自动：[('开' if auto_forward_enabled else '关')]" action Function(toggle_auto_forward)
            for speed in AUTO_FORWARD_SPEEDS:
                textbutton "[speed]X":
                    action Function(set_auto_forward_speed, speed)
                    selected (auto_forward_enabled and auto_forward_speed == speed)

screen choice(items):
    $ accessibility_settings = persistent.sys_persist_state["settings"]
    $ accessibility_scale = accessibility_settings["font_scale"]
    $ accessibility_high_contrast = accessibility_settings["high_contrast"]
    modal True
    vbox:
        xalign 0.5
        yalign 0.68
        xsize 1260
        spacing 18

        for index, item in enumerate(items):
            textbutton item.caption:
                id "day1_choice_{}".format(index)
                action item.action
                xfill True
                text_align 0.5
                key_events True
                default_focus (index == 0)
                background Solid(("#000000" if accessibility_high_contrast else "#24374cdd"))
                hover_background Solid(("#ffffff" if accessibility_high_contrast else "#38566f"))
                text_size int(32 * accessibility_scale)
                text_color ("#ffffff" if accessibility_high_contrast else "#f7ead1")
                text_hover_color ("#000000" if accessibility_high_contrast else "#ffffff")
                text_hover_underline (current_chapter in ("day3", "day4", "day5", "day6"))

screen quick_menu():
    zorder 100
    # Stable narrative frames expose Settings on Escape. Critical choices do
    # not use this screen, so the shortcut cannot bypass a decision surface.
    key "K_ESCAPE" action ShowMenu("preferences")

    hbox:
        id "quick_menu_root"
        xalign 0.98
        yalign 0.02
        spacing 8

        textbutton "回退" action Rollback()
        textbutton "保存" action ShowMenu("save")
        textbutton "读取" action ShowMenu("load")
        textbutton "设置" action ShowMenu("preferences")

screen main_menu():
    tag menu
    $ main_menu_high_contrast = persistent.sys_persist_state["settings"]["high_contrast"]
    default main_menu_focus_graph = FocusAwareGraph(
        "main_menu",
        ["main_start", "main_load", "main_about", "main_settings", "main_quit"],
    )
    use focus_graph_bindings(main_menu_focus_graph)

    if main_menu_high_contrast:
        add Solid("#0b1826")
    elif main_menu_weather == "heavy_rain":
        add Transform("bg main_menu_rainy", xsize=config.screen_width, ysize=config.screen_height)
    elif main_menu_weather == "overcast":
        add Transform("bg main_menu_overcast", xsize=config.screen_width, ysize=config.screen_height)
    elif main_menu_weather == "dusk":
        add Transform("bg main_menu_dusk", xsize=config.screen_width, ysize=config.screen_height)
    else:
        # A safe static fallback for an unknown persisted title state.
        add Transform("bg main_menu_rainy", xsize=config.screen_width, ysize=config.screen_height)

    # Disabled by default while the title page uses only its three static
    # background artworks. Retaining the guarded branch keeps restoration to
    # the realtime system a one-constant change later.
    if MAIN_MENU_ENVIRONMENT_EFFECTS_ENABLED and not main_menu_high_contrast and weather_motion_allowed():
        use weather_effects

    vbox:
        xalign 0.14
        yalign 0.5
        spacing 24

        text "雨停之后":
            size 92
            color "#f4d7c0"
        null height 30
        # A native main-menu session must leave that context before gameplay;
        # otherwise Ren'Py disables FileSave for the whole run. Launcher and
        # testcase entry can invoke this screen directly, where a normal Jump
        # is the safe equivalent because there is no menu context to leave.
        textbutton "开始" id "main_start" action If(renpy.context()._main_menu, Start("begin_game"), Jump("begin_game"))
        textbutton "读取存档" id "main_load" action ShowMenu("load")
        textbutton "制作说明" id "main_about" action Show("production_notes")
        textbutton "设置" id "main_settings" action ShowMenu("preferences")
        textbutton "退出" id "main_quit" action Quit(confirm=True)

    frame:
        xalign 0.98
        yalign 0.97
        background Solid("#101722aa")
        padding (24, 16)
        text "制作：Andwey":
            size 22
            text_align 1.0

screen production_notes():
    modal True
    zorder 220
    add Solid("#080d15dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1180
        ysize 650
        background Solid("#172536f8")
        padding (62, 54)

        vbox:
            spacing 24
            text "制作说明":
                size 56
                color "#f4d7c0"
            text "《雨停之后》是一部免费、非商业的《龙族》非官方同人视觉小说。\n\n本作以观察、询问、准备与承担为叙事核心；所有选择的意义由对话、旁白与可操作选项表达。\n\n当前版本为开发中测试构建，请通过试玩反馈帮助完善阅读体验。":
                size 30
                line_spacing 12
            textbutton "返回":
                id "production_notes_close"
                action Hide("production_notes")
                xalign 1.0

screen game_menu(title, show_return=True, return_to_title=False):
    tag menu
    add Solid("#101a28")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1660
        ysize 900
        background Solid("#172536f4")
        padding (48, 38)

        vbox:
            spacing 24
            text title:
                size 54
                color "#f4d7c0"
            transclude

    if show_return:
        if return_to_title:
            hbox:
                xalign 0.90
                yalign 0.90
                spacing 14

                textbutton "返回标题页" id "settings_return_to_title":
                    xsize 230
                    action MainMenu(confirm=True)
                textbutton "返回" id "game_menu_return":
                    xsize 170
                    action Return()
        else:
            textbutton "返回" id "game_menu_return":
                xalign 0.92
                yalign 0.90
                action Return()

screen save():
    # This state belongs to the top-level screen. `manual_slot_browser` is
    # used below, and SetScreenVariable intentionally targets this caller.
    default selected_slot = None
    use game_menu("保存", show_return=False):
        use manual_slot_browser("save", selected_slot)

screen load():
    # Keep the load selection in the same top-level scope as save selection.
    default selected_slot = None
    use game_menu("读取", show_return=False):
        use manual_slot_browser("load", selected_slot)

screen manual_slot_browser(mode, selected_slot):
    $ selected_loadable = selected_slot is not None and FileLoadable(selected_slot, page="1")
    $ completed_endings = completed_ending_ids()

    vbox:
        xfill True
        spacing 14

        fixed:
            id "manual_slot_list"
            xalign 0.5
            xsize 1480
            xfill True
            ysize 468

            for slot in range(1, 11):
                $ slot_loadable = FileLoadable(slot, page="1")
                $ slot_selected = selected_slot == slot
                $ slot_number = "{:02d}".format(slot)
                button:
                    id "{}_slot_{}".format(mode, slot)
                    # This writes the caller-owned screen variable above, so
                    # the selection remains after the pointer leaves this row.
                    action SetScreenVariable("selected_slot", slot)
                    sensitive (mode == "save" or slot_loadable)
                    selected slot_selected
                    default_focus (slot == 1 and (mode == "save" or slot_loadable))
                    xpos 54
                    ypos ((slot - 1) * 44 + 8)
                    xsize 1372
                    ysize 34
                    padding (18, 2)
                    background Solid("#00000000")
                    hover_background Solid("#8dcbd614")
                    selected_background Solid("#8dcbd6")
                    selected_hover_background Solid("#b7e4ea")

                    hbox:
                        xfill True
                        spacing 24
                        text ("◆" if slot_selected else slot_number):
                            size 23
                            xsize 72
                            color ("#101722" if slot_selected else "#8dcbd6")
                        text FileSaveName(slot, empty="—", page="1"):
                            size 22
                            xsize 920
                            color ("#101722" if slot_selected else "#f5f1e8")
                        text FileTime(
                            slot,
                            format=_("{#file_time}%Y-%m-%d %H:%M"),
                            empty=_("—"),
                            page="1",
                        ):
                            size 17
                            bold False
                            xalign 1.0
                            color ("#2f4956" if slot_selected else "#8dcbd6")

        use ending_tree_progress(completed_endings)

        hbox:
            xalign 1.0
            spacing 16
            if mode == "save":
                textbutton "确认保存":
                    id "confirm_save"
                    action FileSave(selected_slot, confirm=False, page="1")
                    # Match the visual enabled state to Ren'Py's real save
                    # action. This prevents a click that silently does
                    # nothing if an invalid menu context ever leaks through.
                    sensitive (selected_slot is not None and FileSave(selected_slot, confirm=False, page="1").get_sensitive())
            else:
                textbutton "确认读取":
                    id "confirm_load"
                    action FileLoad(selected_slot, confirm=False, page="1")
                    sensitive selected_loadable
            textbutton "返回":
                id "slot_browser_return"
                action Return()

screen ending_tree_progress(completed_endings):
    $ reduced_motion = persistent.sys_persist_state["settings"]["reduced_motion"]
    fixed:
        id "ending_tree_icons"
        xalign 0.5
        xsize 1200
        ysize 154

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 44
            for ending_id, _tree_index in ENDING_TREE_LAYOUT:
                $ is_complete = ending_id in completed_endings
                $ is_true_ending = ending_id == "rain_stops"
                fixed:
                    xsize 150
                    ysize 150
                    if not is_complete:
                        add "ui life_tree" at life_tree_locked xalign 0.5 yalign 0.5 zoom 0.115
                    elif is_true_ending and reduced_motion:
                        add "ui life_tree" at life_tree_true_static xalign 0.5 yalign 0.5 zoom 0.115
                    elif is_true_ending:
                        add "ui life_tree" at life_tree_true_pulse xalign 0.5 yalign 0.5 zoom 0.115
                    elif reduced_motion:
                        add "ui life_tree" at life_tree_lit_static xalign 0.5 yalign 0.5 zoom 0.115
                    else:
                        add "ui life_tree" at life_tree_lit_pulse xalign 0.5 yalign 0.5 zoom 0.115

screen preferences():
    default settings_font_scale = persistent.sys_persist_state["settings"]["font_scale"]
    default settings_high_contrast = persistent.sys_persist_state["settings"]["high_contrast"]
    default settings_reduced_motion = persistent.sys_persist_state["settings"]["reduced_motion"]
    default settings_flash_effects = persistent.sys_persist_state["settings"]["flash_effects_enabled"]
    default settings_screen_shake = persistent.sys_persist_state["settings"]["screen_shake_enabled"]
    key "K_ESCAPE" action Return()

    use game_menu("设置", return_to_title=not main_menu):
        hbox:
            xfill True
            spacing 64

            vbox:
                xsize 700
                spacing 16

                text "文字与显示" style "settings_section_title"
                text "字体大小：[int(settings_font_scale * 100)]%"
                hbox:
                    spacing 14
                    textbutton "100%" style "settings_option_button" xsize 190 action SetScreenVariable("settings_font_scale", 1.0)
                    textbutton "125%" style "settings_option_button" xsize 190 action SetScreenVariable("settings_font_scale", 1.25)
                    textbutton "150%" style "settings_option_button" xsize 190 action SetScreenVariable("settings_font_scale", 1.5)

                null height 8
                text "显示模式" style "settings_section_title"
                hbox:
                    spacing 14
                    textbutton "窗口" style "settings_option_button" xsize 250 action Preference("display", "window")
                    textbutton "全屏" style "settings_option_button" xsize 250 action Preference("display", "fullscreen")

            vbox:
                xsize 700
                spacing 16

                text "辅助功能" style "settings_section_title"
                hbox:
                    spacing 14
                    textbutton "高对比度：[('开' if settings_high_contrast else '关')]" style "settings_option_button" xsize 330 action SetScreenVariable(
                        "settings_high_contrast", not settings_high_contrast
                    )
                    textbutton "减弱动效：[('开' if settings_reduced_motion else '关')]" style "settings_option_button" xsize 330 action SetScreenVariable(
                        "settings_reduced_motion", not settings_reduced_motion
                    )
                hbox:
                    spacing 14
                    textbutton "闪烁效果：[('开' if settings_flash_effects else '关')]" style "settings_option_button" xsize 330 action SetScreenVariable(
                        "settings_flash_effects", not settings_flash_effects
                    )
                    textbutton "屏幕震动：[('开' if settings_screen_shake else '关')]" style "settings_option_button" xsize 330 action SetScreenVariable(
                        "settings_screen_shake", not settings_screen_shake
                    )

                null height 8
                text "文字速度" style "settings_section_title"
                hbox:
                    spacing 14
                    textbutton "慢" style "settings_option_button" xsize 150 action Preference("text speed", 20)
                    textbutton "标准" style "settings_option_button" xsize 150 action Preference("text speed", 35)
                    textbutton "即时" style "settings_option_button" xsize 150 action Preference("text speed", 0)
                    textbutton "自发声" style "settings_option_button" xsize 170 action Preference("self voicing", "toggle")

                text "无障碍选项点击“应用”后保存；文字速度与自发声即时生效。" style "settings_status_text"
                textbutton "应用无障碍设置" id "settings_apply" style "settings_option_button" xsize 310 action Function(
                    apply_accessibility_settings,
                    settings_font_scale,
                    settings_high_contrast,
                    settings_reduced_motion,
                    settings_flash_effects,
                    settings_screen_shake,
                )
screen focus_graph_bindings(graph):
    key "focus_graph_next" action Function(graph.move, 1)
    key "focus_graph_previous" action Function(graph.move, -1)
    timer 0.05 action Function(graph.ensure_initial_focus)
    key "K_DOWN" action Function(graph.move, 1)
    key "K_UP" action Function(graph.move, -1)

screen chapter_complete(title, message):
    modal True
    add Solid("#080d15cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1160
        ysize 420
        background Solid("#eadfc7")
        padding (70, 58)

        vbox:
            xfill True
            yalign 0.5
            spacing 26
            text title:
                size 58
                color "#5b3d48"
                outlines []
                xalign 0.5
            text message:
                size 30
                color "#384653"
                outlines []
                text_align 0.5
                xalign 0.5
            textbutton "继续旅程":
                action Return()
                xalign 0.5

screen ending_complete(title, message):
    modal True
    add Solid("#080d15cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1160
        ysize 420
        background Solid("#eadfc7")
        padding (70, 58)

        fixed:
            xfill True
            yfill True
            vbox:
                xfill True
                yalign 0.42
                spacing 26
                text title:
                    size 58
                    color "#5b3d48"
                    outlines []
                    xalign 0.5
                text message:
                    size 30
                    color "#384653"
                    outlines []
                    text_align 0.5
                    xalign 0.5
            textbutton "回到标题":
                action MainMenu(confirm=False)
                xalign 1.0
                yalign 1.0

screen confirm(message, yes_action, no_action):
    modal True
    add Solid("#000000aa")
    frame:
        xalign 0.5
        yalign 0.5
        padding (54, 42)
        vbox:
            spacing 24
            text message
            hbox:
                spacing 20
                xalign 0.5
                textbutton "确定" action yes_action
                textbutton "取消" action no_action

screen notify(message):
    zorder 300
    frame at notify_appear:
        xalign 0.5
        yalign 0.08
        text message
    timer 3.25 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear 0.2 alpha 1
    on hide:
        linear 0.3 alpha 0
