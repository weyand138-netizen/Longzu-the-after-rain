style default:
    font "SourceHanSansLite.ttf"

style button:
    key_events True

init python:
    import json
    import os
    from renpy.exports import get_widget
    from renpy.display.screen import get_displayable
    from modules.accessibility_focus import FocusAwareGraph

    focus_log = []
    viewport_log = []
    transcript_log = []
    deep_action_count = 0
    a11y_focus_graph = FocusAwareGraph(
        "a11y_spike",
        [
            {"id": "first_action", "estimated_rect": (96, 315, 760, 36)},
            {"id": "second_action", "estimated_rect": (96, 365, 760, 36)},
            {"id": "deep_action", "estimated_rect": (96, 900, 760, 36)},
            {"id": "exit_action", "estimated_rect": (880, 179, 193, 36)},
        ],
        viewport_id="body_viewport",
        viewport_rect=(96, 285, 760, 430),
    )

    def focused_name():
        focused = renpy.display.focus.get_focused()
        if focused is None:
            return None
        graph_name = a11y_focus_graph.current_id()
        if graph_name is not None:
            return graph_name
        for name in ("first_action", "second_action", "deep_action", "exit_action"):
            widget = (
                get_displayable("a11y_spike", name, base=True)
                or get_widget(None, name)
                or get_widget("a11y_spike", name)
            )
            if focused == widget or getattr(focused, "child", None) == widget:
                return name
        return getattr(focused, "focus_name", None)

    def viewport_value():
        viewport = get_widget(None, "body_viewport")
        if viewport is None:
            return focus_log[-1]["viewport_y"] if focus_log else -1
        return viewport.yadjustment.value

    def record_runtime_state():
        name = focused_name()
        current_viewport = viewport_value()
        if (
            not focus_log
            or focus_log[-1]["focus"] != name
            or focus_log[-1]["viewport_y"] != current_viewport
        ):
            viewport = get_widget(None, "body_viewport")
            child = getattr(viewport, "child", None) if viewport is not None else None
            child_surface = renpy.display.render.render(child, 760, 430, 0, 0) if child is not None else None
            focused = renpy.display.focus.get_focused()
            focus_log.append({
                "focus": name,
                "semantic_id": name,
                "rect": renpy.display.focus.focus_coordinates(),
                "viewport_y": current_viewport,
                "viewport_range": getattr(getattr(viewport, "yadjustment", None), "range", None),
                "deep_rect": a11y_focus_graph._rect("deep_action"),
                "viewport_rect": a11y_focus_graph._viewport_rect()[1] if a11y_focus_graph._viewport_rect() else None,
                "deep_action_fully_visible": a11y_focus_graph.is_fully_visible("deep_action"),
                "viewport_child": type(child).__name__ if child is not None else None,
                "viewport_child_count": len(getattr(child, "children", [])) if child is not None else None,
                "viewport_child_surface": child_surface.get_size() if child_surface is not None else None,
                "focused_type": type(focused).__name__ if focused is not None else None,
                "focused_focus_name": getattr(focused, "focus_name", None) if focused is not None else None,
                "focused_id": getattr(focused, "id", None) if focused is not None else None,
                "focused_repr": repr(focused) if focused is not None else None,
                "screen_widget_repr": {
                    name: repr(get_widget(None, name)) for name in ("first_action", "second_action", "deep_action", "exit_action")
                },
                "focus_list": [
                    {"widget": repr(item.widget), "rect": [item.x, item.y, item.w, item.h]}
                    for item in renpy.display.focus.focus_list
                ],
            })
            viewport_log.append({
                "focus": name,
                "semantic_id": name,
                "viewport_y": current_viewport,
                "viewport_range": getattr(getattr(viewport, "yadjustment", None), "range", None),
                "deep_rect": a11y_focus_graph._rect("deep_action"),
                "viewport_rect": a11y_focus_graph._viewport_rect()[1] if a11y_focus_graph._viewport_rect() else None,
                "deep_action_fully_visible": a11y_focus_graph.is_fully_visible("deep_action"),
            })
            write_runtime_evidence()

        last = renpy.display.tts.last
        if last and (not transcript_log or transcript_log[-1] != last):
            transcript_log.append(last)

    def record_deep_action():
        global deep_action_count
        deep_action_count += 1

    def write_runtime_evidence():
        root = renpy.config.gamedir
        with open(os.path.join(root, "focus-log.json"), "w", encoding="utf-8") as stream:
            json.dump(focus_log, stream, ensure_ascii=False, indent=2)
        with open(os.path.join(root, "viewport-log.json"), "w", encoding="utf-8") as stream:
            json.dump(viewport_log, stream, ensure_ascii=False, indent=2)
        with open(os.path.join(root, "transcript-log.txt"), "w", encoding="utf-8") as stream:
            stream.write("\n".join(transcript_log) + "\n")

label start:
    scene black
    pause

label a11y_test_1:
    call screen a11y_spike(scale=1.0, voicing=False)
    return

label a11y_test_1_5:
    call screen a11y_spike(scale=1.5, voicing=False)
    return

label a11y_test_voicing:
    call screen a11y_spike(scale=1.0, voicing=True)
    return

screen main_menu():
    tag menu
    modal True
    add Solid("#0b1826")
    textbutton "进入 Spike":
        xalign 0.5
        yalign 0.5
        action Start()

screen a11y_spike(scale=1.0, voicing=False):
    modal True
    default body_scroll = ui.adjustment(value=0)

    if voicing:
        $ _preferences.self_voicing = "debug"
    else:
        $ _preferences.self_voicing = False

    timer 0.05 repeat True action [
        Function(a11y_focus_graph.ensure_initial_focus),
        Function(record_runtime_state),
    ]
    key "focus_graph_next" action Function(a11y_focus_graph.move, 1)
    key "focus_graph_previous" action Function(a11y_focus_graph.move, -1)
    key "K_TAB" action Function(a11y_focus_graph.move, 1)
    key "shift_K_TAB" action Function(a11y_focus_graph.move, -1)

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1160
        ysize 660
        background Solid("#0b1826")
        padding (36, 30)

        vbox:
            spacing 18

            text "无障碍能力 Spike":
                size int(42 * scale)
                color "#e9dfc8"
                alt "无障碍能力 Spike，当前测试屏幕"

            text "标题 → 说明 → 可操作内容 → 固定安全操作":
                size int(24 * scale)
                color "#8dcbd6"

            hbox:
                spacing 24

                viewport:
                    id "body_viewport"
                    xminimum 760
                    xmaximum 760
                    yminimum 430
                    ymaximum 430
                    xfill True
                    child_size (None, None)
                    mousewheel True
                    arrowkeys False
                    pagekeys True
                    draggable False
                    yinitial 0.0
                    yadjustment body_scroll
                    viewport_yfill False

                    has vbox:
                        spacing 14
                        xfill True
                        text "BODY CONTENT":
                            size int(28 * scale)
                        text "说明：焦点进入下方内容时，viewport 应自动滚入；滚动不应提交 action。":
                            size int(28 * scale)
                            color "#f5f1e8"
                            alt "说明。焦点进入下方内容时，viewport 应自动滚入；滚动不提交操作。"
                        textbutton "第一操作":
                            id "first_action"
                            key_events True
                            action NullAction()
                            alt "第一操作，安全的无副作用操作"
                            text_size int(28 * scale)
                            xfill True
                        textbutton "第二操作":
                            id "second_action"
                            key_events True
                            action NullAction()
                            alt "第二操作，安全的无副作用操作"
                            text_size int(28 * scale)
                            xfill True
                        text "第一段：这是用于验证长文换行、键盘可达性和读序的中文文本。":
                            size int(28 * scale)
                        text "第二段：这是第二个可观察事实，不能依赖颜色、声音或动画。":
                            size int(28 * scale)
                        text "第三段：字体放大后仍须保留完整语义与安全操作。":
                            size int(28 * scale)
                        text "第四段：继续向下移动焦点，直到深层操作进入视野。":
                            size int(28 * scale)
                        text "第五段：焦点顺序必须与标题、说明、内容、操作的读序一致。":
                            size int(28 * scale)
                        text "第六段：viewport 只负责滚动，不得因为焦点进入而触发任何 action。":
                            size int(28 * scale)
                        text "第七段：键盘用户应能在不依赖鼠标的情况下完成进入、移动、确认和退出。":
                            size int(28 * scale)
                        text "第八段：文本换行、按钮命中区和焦点矩形必须在放大后仍可见。":
                            size int(28 * scale)
                        text "第九段：本段用于把深层操作推过 viewport 的初始可视区域。":
                            size int(28 * scale)
                        text "第十段：继续向下移动焦点后，viewport 应自动滚入深层操作。":
                            size int(28 * scale)
                        textbutton "深层操作（不自动执行）":
                            id "deep_action"
                            key_events True
                            action Function(record_deep_action)
                            alt "深层操作，不自动执行"
                            text_size int(28 * scale)
                            xfill True

                vbox:
                    spacing 18
                    textbutton "退出 Spike":
                        id "exit_action"
                        key_events True
                        action [Function(write_runtime_evidence), Return()]
                        alt "退出 Spike 并保存测试证据"
                        text_size int(28 * scale)

    key "focus_graph_next" action Function(a11y_focus_graph.move, 1)
    key "focus_graph_previous" action Function(a11y_focus_graph.move, -1)
    key "K_DOWN" action Function(a11y_focus_graph.move, 1)
    key "K_UP" action Function(a11y_focus_graph.move, -1)
    key "K_ESCAPE" action [Function(write_runtime_evidence), Return()]
