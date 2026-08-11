# VERTICAL SLICE - NOT FOR PRODUCTION
# Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality?
# Date: 2026-07-23

testcase observe_ask_truth:
    description "Observe, ask, and identify the tracker; verify all delayed payoffs."

    run Jump("slice_start")
    advance until screen "choice"
    click "先捡起那张被雨打湿的纸"
    advance until screen "choice"
    click "把路线图转向她：你想去哪？"
    advance until screen "choice"
    click "记住男人鞋底不属于车站的红泥"
    advance until screen "slice_complete"
    assert eval understanding == 1
    assert eval autonomy == 1
    assert eval truth == 1
    assert eval len(payoff_lines) == 3
    assert eval any("愿望纸" in line for line in payoff_lines)
    assert eval any("车票" in line for line in payoff_lines)
    assert eval any("红泥" in line for line in payoff_lines)

testcase prepare_decide_exit:
    description "Record expressive safety/route choices and one valid preparation."

    run Jump("slice_start")
    advance until screen "choice"
    click "先带她去站台尽头，离开监控范围"
    advance until screen "choice"
    click "告诉她最快路线：跟紧我"
    advance until screen "choice"
    click "记住维修门和旧锁的位置"
    advance until screen "slice_complete"
    assert eval preparation == 1
    assert eval autonomy == 0
    assert eval sacrifice == 0
    assert eval "move_to_cover" in choice_history
    assert eval "choose_fast_route" in choice_history
    assert eval len(payoff_lines) == 3
    assert eval any("她则替自己保存" in line for line in payoff_lines)
    assert eval any("替她决定" in line for line in payoff_lines)
    assert eval any("备选出口" in line for line in payoff_lines)

testcase keyboard_complete_and_journal:
    description "Complete the whole slice and open/close the journal using keyboard input."

    run Jump("slice_start")
    advance until screen "choice"
    screenshot f"visual/choice_default_window_{renpy.get_physical_size()[0]}x{renpy.get_physical_size()[1]}.png"
    keysym "K_DOWN"
    keysym "K_RETURN"
    advance until screen "choice"
    keysym "K_DOWN"
    keysym "K_RETURN"
    advance until screen "choice"
    keysym "K_DOWN"
    keysym "K_RETURN"
    advance until screen "slice_complete"
    screenshot f"visual/complete_communication_v2_{renpy.get_physical_size()[0]}x{renpy.get_physical_size()[1]}.png"
    assert eval len(choice_history) == 3
    keysym "K_DOWN"
    keysym "K_RETURN"
    assert screen "slice_journal" timeout 3.0
    screenshot f"visual/journal_communication_v2_{renpy.get_physical_size()[0]}x{renpy.get_physical_size()[1]}.png"
    keysym "K_ESCAPE"
    assert not screen "slice_journal" timeout 3.0
