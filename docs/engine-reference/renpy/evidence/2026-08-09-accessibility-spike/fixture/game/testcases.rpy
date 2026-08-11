testcase focus_viewport_and_reading_order:
    description "Keyboard focus order, viewport auto-scroll and fixed safe exit at 1280x720."

    run Jump("a11y_test_1")
    pause 0.1
    assert screen "a11y_spike"
    assert eval focused_name() == "first_action"
    screenshot "visual/focus_initial_1280x720.png"

    keysym "K_DOWN"
    pause 0.1
    run Function(record_runtime_state)
    assert eval "K_TAB" in config.keymap["focus_graph_next"] and "shift_K_TAB" in config.keymap["focus_graph_previous"]
    assert eval renpy.display.focus.focus_coordinates() is not None
    screenshot "visual/focus_second_visible_1280x720.png"
    keysym "K_UP"
    pause 0.1
    assert eval focused_name() == "first_action" and viewport_value() >= 0
    keysym "K_ESCAPE"
    assert not screen "a11y_spike" timeout 3.0

testcase font_scale_1_5_layout:
    description "1280x720 rendering with the approved candidate font at 1.5 scale."

    run Jump("a11y_test_1_5")
    pause 0.1
    assert eval focused_name() == "first_action"
    assert eval renpy.display.focus.focus_coordinates() is not None
    screenshot "visual/layout_1280x720_font_1_5.png"
    keysym "K_ESCAPE"
    assert not screen "a11y_spike" timeout 3.0

testcase viewport_auto_scroll_current_engine:
    description "RenPy must auto-scroll an offscreen focused child before activation."

    run Jump("a11y_test_1")
    pause 0.1
    keysym "K_DOWN"
    pause 0.1
    keysym "K_DOWN"
    pause 0.1
    assert eval viewport_value() > 0 and a11y_focus_graph.is_fully_visible("deep_action") and deep_action_count == 0
    screenshot "visual/focus_deep_visible_1280x720.png"
    keysym "K_ESCAPE"
    assert not screen "a11y_spike" timeout 3.0

testcase debug_self_voicing_transcript:
    description "RenPy debug self-voicing transcript follows focus and does not activate controls."

    run Jump("a11y_test_voicing")
    pause 0.1
    assert screen "a11y_spike"
    assert eval _preferences.self_voicing == "debug"
    assert eval "第一操作" in renpy.display.tts.last
    keysym "K_DOWN"
    pause 0.1
    assert eval focused_name() == "second_action"
    assert eval "第二操作" in renpy.display.tts.last
    assert eval deep_action_count == 0
    keysym "K_ESCAPE"
    assert not screen "a11y_spike" timeout 3.0
    run Function(write_runtime_evidence)
