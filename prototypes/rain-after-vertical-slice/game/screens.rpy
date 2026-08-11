# VERTICAL SLICE - NOT FOR PRODUCTION
# Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality?
# Date: 2026-07-23

style default:
    font "SourceHanSansLite.ttf"
    size 34
    color "#f5f1e8"
    outlines [(2, "#0a111c", 0, 0)]

style button:
    background Solid("#20364be8")
    hover_background Solid("#3c6076")
    insensitive_background Solid("#1a2632aa")
    padding (30, 18)

style button_text:
    font "SourceHanSansLite.ttf"
    size 31
    color "#f7e8cb"
    hover_color "#ffffff"
    insensitive_color "#85919a"

style window:
    background Solid("#09131fe8")
    padding (52, 34)

screen say(who, what):
    window:
        id "window"
        xalign 0.5
        yalign 0.95
        xsize 1760
        yminimum 238

        vbox:
            spacing 12
            if who is not None:
                text who:
                    id "who"
                    size 36
                    color "#f3b3c5"
            text what:
                id "what"
                size 34
                line_spacing 10

    use slice_quick_menu

screen choice(items):
    modal True
    key "K_ESCAPE" action NullAction()

    frame:
        xalign 0.5
        yalign 0.66
        xsize 1380
        background Solid("#07111cdd")
        padding (34, 30)

        vbox:
            spacing 16
            text "你要怎么做？":
                size 27
                color "#8dcbd6"
                xalign 0.5

            for index, item in enumerate(items):
                textbutton item.caption:
                    action item.action
                    xfill True
                    text_align 0.5
                    default_focus (index == 0)

screen slice_quick_menu():
    zorder 100
    hbox:
        xalign 0.985
        yalign 0.018
        spacing 8
        textbutton "回退" action Rollback()
        textbutton "快存" action QuickSave()
        textbutton "快读" action QuickLoad()
        textbutton "手册" action Show("slice_journal")
        textbutton "设置" action ShowMenu("preferences")

screen main_menu():
    tag menu
    add "bg slice_platform"
    add Solid("#07101cc4")

    frame:
        xalign 0.12
        yalign 0.48
        xsize 760
        background Solid("#0a1522d8")
        padding (56, 48)

        vbox:
            spacing 20
            text "雨停之后":
                size 86
                color "#f1d8bd"
            text "垂直切片 · 观察 / 询问 / 承担":
                size 29
                color "#9dd2dc"
            null height 26
            textbutton "开始切片":
                action Start()
                default_focus True
            textbutton "读取存档" action ShowMenu("load")
            textbutton "设置" action ShowMenu("preferences")
            textbutton "退出" action Quit(confirm=True)

    frame:
        xalign 0.985
        yalign 0.97
        background Solid("#07111cbb")
        padding (22, 14)
        text "非正式游戏 · 免费非商业同人\n制作：Andwey":
            size 21
            text_align 1.0

screen game_menu(title):
    tag menu
    add Solid("#0a1422")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1640
        ysize 900
        background Solid("#142436f4")
        padding (50, 40)
        vbox:
            spacing 24
            text title:
                size 52
                color "#f1d8bd"
            transclude
    textbutton "返回":
        xalign 0.95
        yalign 0.94
        action Return()

screen save():
    use game_menu("保存"):
        use slice_file_slots

screen load():
    use game_menu("读取"):
        use slice_file_slots

screen slice_file_slots():
    grid 3 2:
        xfill True
        yfill True
        spacing 22
        for slot in range(1, 7):
            button:
                action FileAction(slot)
                has vbox
                spacing 8
                add FileScreenshot(slot) xalign 0.5
                text FileTime(
                    slot,
                    format=_("{#file_time}%Y-%m-%d %H:%M"),
                    empty=_("空存档"),
                ):
                    size 23
                    xalign 0.5
                text FileSaveName(slot):
                    size 21
                    xalign 0.5

screen preferences():
    use game_menu("设置"):
        vbox:
            spacing 24
            text "显示"
            hbox:
                spacing 16
                textbutton "窗口" action Preference("display", "window")
                textbutton "全屏" action Preference("display", "fullscreen")
            text "文字速度"
            hbox:
                spacing 16
                textbutton "慢" action Preference("text speed", 20)
                textbutton "标准" action Preference("text speed", 32)
                textbutton "即时" action Preference("text speed", 0)
            text "辅助"
            hbox:
                spacing 16
                textbutton "自发声" action Preference("self voicing", "toggle")
                textbutton "高对比度标记" action ToggleField(
                    persistent,
                    "slice_high_contrast",
                )
            text "所有选择和结束页均支持方向键、Tab 与 Enter。":
                size 25
                color "#afc8d2"

screen slice_journal():
    modal True
    zorder 220
    key "K_ESCAPE" action Hide("slice_journal")

    add Solid("#050a10dd")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1420
        ysize 780
        background Solid("#e9dfc8f7")
        padding (62, 50)

        vbox:
            spacing 24
            text "绘梨衣的愿望手册":
                size 54
                color "#593d49"
                outlines []
            text "被记住的事":
                size 30
                color "#345365"
                outlines []

            if persistent.slice_memory:
                text persistent.slice_memory:
                    size 30
                    color "#36393b"
                    line_spacing 12
                    outlines []
            else:
                text "纸页还是空的。某些选择要过一会儿，才知道留下了什么。":
                    size 28
                    color "#66635e"
                    outlines []

            null height 20
            textbutton "合上手册  [[Esc]":
                action Hide("slice_journal")
                xalign 1.0
                default_focus True

screen slice_complete(summary):
    modal True
    add Solid("#05090fd9")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        background Solid("#eadfc8f8")
        padding (72, 58)

        vbox:
            spacing 25
            text "序章完成":
                size 60
                color "#593d49"
                outlines []
                xalign 0.5
            text "没有数值告诉你做得对不对。\n但有人记住了你让她选择，或替她选择的那一刻。":
                size 29
                color "#3b505a"
                text_align 0.5
                outlines []
                xalign 0.5
            frame:
                background Solid("#fffaf0")
                padding (34, 28)
                xfill True
                text summary:
                    size 27
                    color "#383b3d"
                    line_spacing 12
                    outlines []
            hbox:
                spacing 20
                xalign 0.5
                textbutton "打开手册":
                    action Show("slice_journal")
                    default_focus True
                textbutton "回到标题" action Return()

screen confirm(message, yes_action, no_action):
    modal True
    add Solid("#000000b8")
    frame:
        xalign 0.5
        yalign 0.5
        padding (54, 42)
        vbox:
            spacing 22
            text message
            hbox:
                spacing 20
                xalign 0.5
                textbutton "确定" action yes_action
                textbutton "取消" action no_action

screen notify(message):
    zorder 300
    frame:
        xalign 0.5
        yalign 0.08
        background Solid("#153247ee")
        padding (30, 18)
        text message:
            size 27
    timer 3.0 action Hide("notify")
