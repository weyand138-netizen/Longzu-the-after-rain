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

style window:
    background Solid("#0b1320dd")
    padding (54, 34)

default critical_choice_interaction = False

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
    hbox:
        id "quick_menu_root"
        xalign 0.98
        yalign 0.02
        spacing 8

        textbutton "回退" action Rollback()
        textbutton "快存" action QuickSave()
        textbutton "快读" action QuickLoad()
        textbutton "手册" action Show("wish_journal")
        textbutton "设置" action ShowMenu("preferences")

screen main_menu():
    tag menu
    default main_menu_focus_graph = FocusAwareGraph(
        "main_menu",
        ["main_start", "main_load", "main_journal", "main_settings", "main_quit"],
    )
    use focus_graph_bindings(main_menu_focus_graph)
    add Solid("#0e1826")

    vbox:
        xalign 0.14
        yalign 0.5
        spacing 24

        text "雨停之后":
            size 92
            color "#f4d7c0"
        text "《龙族》非官方同人视觉小说":
            size 30
            color "#9fc5d6"

        null height 30
        textbutton "开始" id "main_start" action Start()
        textbutton "读取" id "main_load" action ShowMenu("load")
        textbutton "愿望手册" id "main_journal" action Show("wish_journal")
        textbutton "设置" id "main_settings" action ShowMenu("preferences")
        textbutton "退出" id "main_quit" action Quit(confirm=True)

    frame:
        xalign 0.98
        yalign 0.97
        background Solid("#101722aa")
        padding (24, 16)
        text "免费 · 非商业 · 非官方同人\n制作：Andwey":
            size 22
            text_align 1.0

screen game_menu(title):
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

    textbutton "返回":
        xalign 0.95
        yalign 0.94
        action Return()

screen save():
    use game_menu("保存"):
        use file_slots

screen load():
    use game_menu("读取"):
        use file_slots

screen file_slots():
    grid 3 2:
        xfill True
        yfill True
        spacing 24

        for slot in range(1, 7):
            button:
                action FileAction(slot)
                has vbox
                spacing 10
                add FileScreenshot(slot) xalign 0.5
                text FileTime(
                    slot,
                    format=_("{#file_time}%Y-%m-%d %H:%M"),
                    empty=_("空存档"),
                ):
                    size 24
                    xalign 0.5
                text FileSaveName(slot):
                    size 22
                    xalign 0.5

screen preferences():
    default settings_font_scale = persistent.sys_persist_state["settings"]["font_scale"]
    default settings_high_contrast = persistent.sys_persist_state["settings"]["high_contrast"]
    default settings_reduced_motion = persistent.sys_persist_state["settings"]["reduced_motion"]
    default settings_flash_effects = persistent.sys_persist_state["settings"]["flash_effects_enabled"]
    default settings_screen_shake = persistent.sys_persist_state["settings"]["screen_shake_enabled"]

    use game_menu("设置"):
        vbox:
            spacing 22
            text "显示与无障碍"
            text "字体大小：[int(settings_font_scale * 100)]%"
            hbox:
                spacing 16
                textbutton "100%" action SetScreenVariable("settings_font_scale", 1.0)
                textbutton "125%" action SetScreenVariable("settings_font_scale", 1.25)
                textbutton "150%" action SetScreenVariable("settings_font_scale", 1.5)

            text "显示模式"
            hbox:
                spacing 16
                textbutton "窗口" action Preference("display", "window")
                textbutton "全屏" action Preference("display", "fullscreen")

            text "辅助开关"
            hbox:
                spacing 16
                textbutton "高对比度：[if settings_high_contrast]开[else]关[endif]" action SetScreenVariable(
                    "settings_high_contrast", not settings_high_contrast
                )
                textbutton "减弱动效：[if settings_reduced_motion]开[else]关[endif]" action SetScreenVariable(
                    "settings_reduced_motion", not settings_reduced_motion
                )
            hbox:
                spacing 16
                textbutton "闪烁效果：[if settings_flash_effects]开[else]关[endif]" action SetScreenVariable(
                    "settings_flash_effects", not settings_flash_effects
                )
                textbutton "屏幕震动：[if settings_screen_shake]开[else]关[endif]" action SetScreenVariable(
                    "settings_screen_shake", not settings_screen_shake
                )

            text "文字速度"
            hbox:
                spacing 16
                textbutton "慢" action Preference("text speed", 20)
                textbutton "标准" action Preference("text speed", 35)
                textbutton "即时" action Preference("text speed", 0)

            text "辅助"
            hbox:
                spacing 16
                textbutton "自发声开关" action Preference("self voicing", "toggle")
            text "应用保存后生效；自发声与文字速度即时生效。":
                size 24
                color "#8dcbd6"
            textbutton "应用无障碍设置" id "settings_apply" action Function(
                apply_accessibility_settings,
                settings_font_scale,
                settings_high_contrast,
                settings_reduced_motion,
                settings_flash_effects,
                settings_screen_shake,
            )

screen wish_journal():
    modal True
    zorder 200
    default journal_focus_graph = FocusAwareGraph(
        "wish_journal",
        ["journal_close"],
        viewport_id="journal_viewport",
    )
    use focus_graph_bindings(journal_focus_graph)
    add Solid("#0b111bdd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1480
        ysize 820
        background Solid("#e8dfc8f5")
        padding (54, 42)

        vbox:
            spacing 22
            text "绘梨衣的愿望手册":
                size 54
                color "#603f4b"
                outlines []
            viewport:
                id "journal_viewport"
                xfill True
                ymaximum 570
                mousewheel True
                arrowkeys False
                pagekeys True
                draggable False

                has vbox
                spacing 18
                text "已经记住的章节":
                    size 30
                    color "#31475a"
                    outlines []

                if persistent.memories_unlocked:
                    for memory_id in persistent.memories_unlocked:
                        text "· [memory_id]":
                            size 27
                            color "#3d3a38"
                            outlines []
                else:
                    text "还没有。":
                        size 27
                        color "#6b6660"
                        outlines []

                text "已解锁成就：[len(persistent.achievements_unlocked)] / 24":
                    size 28
                    color "#31475a"
                    outlines []

            textbutton "合上手册":
                id "journal_close"
                key_events True
                action Hide("wish_journal")
                xalign 1.0

screen focus_graph_bindings(graph):
    key "focus_graph_next" action Function(graph.move, 1)
    key "focus_graph_previous" action Function(graph.move, -1)
    timer 0.05 repeat True action Function(graph.ensure_initial_focus)
    key "K_DOWN" action Function(graph.move, 1)
    key "K_UP" action Function(graph.move, -1)

screen chapter_complete(title, message):
    modal True
    add Solid("#080d15cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1160
        background Solid("#eadfc7")
        padding (70, 58)

        vbox:
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
                action Return()
                xalign 0.5

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
