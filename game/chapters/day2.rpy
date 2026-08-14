init python:
    # Build-time input only. No Day 2 manifest is created by this story.
    DAY2_SOURCE_UNIT_ID = "chapter_day2_two_game_tokens"
    DAY2_REQUIRED_SCENE_IDS = (
        "scene_day2_alias_answer",
        "scene_day2_two_tokens",
        "scene_day2_last_machine",
    )
    DAY2_CHOICE_RECORDS = (
        (
            "day2_accept_alias",
            "reaction_day2_accept_alias",
            "payoff_day2_alias_day4",
        ),
        (
            "day2_assign_alias",
            "reaction_day2_assign_alias",
            "payoff_day2_assigned_alias_day6",
        ),
        (
            "day2_admit_alias_unknown",
            "reaction_day2_admit_alias_unknown",
            "payoff_day2_admit_day5",
        ),
        (
            "day2_save_second_token",
            "reaction_day2_save_second_token",
            "payoff_day2_token_day6",
        ),
        (
            "day2_spend_both_tokens",
            "reaction_day2_spend_both_tokens",
            "payoff_day2_spend_day4",
        ),
    )
    DAY2_CHOICE_EFFECTS = {
        "day2_accept_alias": ("understanding", "autonomy"),
        "day2_assign_alias": ("revoke:token_override_daily_choice",),
        "day2_admit_alias_unknown": (
            "understanding",
            "repair:token_silence_as_consent",
        ),
        "day2_save_second_token": ("preparation", "acquire:resource_arcade_token"),
        "day2_spend_both_tokens": ("sacrifice", "event:event_both_tokens_spent"),
    }
    DAY2_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day2_two_game_tokens",
            "day_index": 2,
            "observable_fact_ids": (
                "fact_day2_erii_enters_alias",
                "fact_day2_last_machine_handoff",
            ),
            "source_unit_id": DAY2_SOURCE_UNIT_ID,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_day2_arcade_alias",
            "day_index": 2,
            "observable_fact_ids": ("fact_day2_erii_enters_alias",),
            "source_unit_id": DAY2_SOURCE_UNIT_ID,
        },
    )


label chapter_day2_two_game_tokens:
    $ current_chapter = "day2"
    scene bg warm_room

    # scene_day2_alias_answer
    narrator "商场角落的街机还亮着。绘梨衣把光标停在昵称框里，慢慢敲下几个字母，又把屏幕转向路明非。"
    narrator "商场广播正在提醒最后一轮清场，远处的卷帘门一扇一扇落下。街机的彩色光落在她的手背上，把刚才那张收据的折痕照得很清楚。"
    narrator "她输入一个字母，就停下来确认屏幕有没有正确显示。光标闪了几次，像在等待一个不必由别人替她完成的结尾。"
    narrator "路明非没有伸手去碰键盘。那件没有带走的便服、口袋里的收据和今天还剩的时间，都不能替她决定屏幕上的名字。"
    narrator "她把屏幕转向他时，显示框还没有按下确认。名字停在可以修改的位置，也停在可以被看见的位置。"
    narrator "机器旁边贴着褪色的活动海报，边角已经卷起。她看了海报一眼，又把注意力收回昵称框，像是在区分环境留下的字和自己刚刚写下的字。"
    $ critical_choice_interaction = True

    menu:
        "按她输入的昵称确认":
            $ apply_choice("day2_accept_alias", {"understanding": 1, "autonomy": 1})
            narrator "她把手留在按键上，看着昵称在开场画面里亮起来。"
            erii "嗯。"
            narrator "她没有立刻开始游戏，先等名字在屏幕上完整显示一轮。随后她用指尖碰了碰确认键旁的空白处，确认那不是机器自动替换的默认名称。"
            narrator "路明非把这个名字读了一遍，没有加上自己的解释。她听完后把屏幕推回原来的角度，手仍然放在可以随时重新输入的位置。"
            $ critical_choice_interaction = False

        "换成我替她想的昵称":
            $ apply_choice("day2_assign_alias", {})
            narrator "她照着新的名字按完最后一个键，却把手从面板上移开。"
            narrator "新名字亮起时，机器立刻播出欢迎音。她没有去看排行榜，只把手收回到膝前，像是把刚才留下的字和自己保持了一点距离。"
            narrator "路明非想解释这个名字更容易记，却看见她把屏幕边缘转向自己。她没有删掉它，也没有用动作把它变成真正属于自己的标记。"
            $ critical_choice_interaction = False

        "承认刚才没有听懂，重新问她" if has_unresolved_token("token_silence_as_consent"):
            $ apply_choice("day2_admit_alias_unknown", {"understanding": 1})
            narrator "路明非把话收回来。绘梨衣重新敲下自己的昵称，再把屏幕推到他面前。"
            narrator "这一次她输入得更慢，每个字母都停一下。她把屏幕推过来后没有松开确认键，等他看完，又把手指放回原处。"
            narrator "路明非先复述他看见的字，再让出键盘。她按下确认，机器的欢迎音响起；刚才没有听懂的部分没有被假装不存在，而是被重新摆到两个人都能看见的位置。"
            $ critical_choice_interaction = False

    # scene_day2_two_tokens
    narrator "出票口吐出两枚游戏币。绘梨衣把其中一枚放到路明非掌心，另一枚压在开始键旁。"
    narrator "两枚游戏币在金属槽里滚了几圈，停下时一枚朝上、一枚侧立。她先把侧立的那枚扶正，再把它们分别放到两个人面前。"
    narrator "屏幕上的倒计时已经开始。第一枚币足够让机器亮起，第二枚币却让今天的结束多出一个可以延后的选择。"
    narrator "她把自己的那枚推向开始键，又把另一枚推回他掌心。这个动作很轻，仍然足以让两枚币不再是同一种用途。"
    narrator "路明非握住游戏币，金属的边缘硌在指节上。他想起收据上被折进去的名字，知道有些东西留下来以后，意义不会在当场说明。"
    narrator "商场的广播再次催促顾客离场。绘梨衣看了看最后一局的时间，又看向他手里的那枚币，等待他把这件小事当成她交来的东西。"
    $ critical_choice_interaction = True

    menu:
        "把第二枚币收好，留作之后认得出彼此的记号":
            $ apply_choice("day2_save_second_token", {"preparation": 1})
            narrator "她把第二枚币交给他保管，然后用留下的一枚币开始游戏。"
            narrator "她确认游戏币已经落进他的掌心，才把自己的那枚投进机器。机器启动时发出短促的提示音，她先看他一眼，再把手放上操纵杆。"
            narrator "路明非把游戏币放进和收据不同的口袋。它们一个留下名字，一个留下可以再次认出的机会，谁也没有被他说成更重要的那一个。"
            $ critical_choice_interaction = False

        "把两枚币都投进去，陪她打完这一局":
            $ apply_choice("day2_spend_both_tokens", {"sacrifice": 1})
            narrator "最后一枚币落进机器。她把手放回操纵杆上，直到这一局的音乐停下。"
            narrator "两枚币同时消失在投币口里，机器的灯光因此更亮了一点。她没有回头看空掉的出票口，只把视线留在下一关的画面上。"
            narrator "路明非站在她身后，听着机器的提示音一声一声结束。想要把这一晚留得更久的愿望，先变成了一个不会再回到手里的动作。"
            $ critical_choice_interaction = False

    # scene_day2_last_machine
    narrator "最里面那台机器熄屏前，绘梨衣把掌心贴在玻璃上，又收回手。商场要打烊了。"
    narrator "屏幕的余光映在玻璃上，像一层很薄的雾。她把掌心贴上去时没有触碰任何按钮，只是在确认这台机器已经把这一局完整记住。"
    narrator "清场人员从远处走来，脚步声在空下来的商场里变得很清楚。绘梨衣先把包带拉紧，再确认口袋里的收据没有滑出来。"
    lm "走吧。明天再想下一站。"
    narrator "她跟在他身边，没有催促，也没有回头。"
    narrator "离开街机区前，她回头看了一次刚才的屏幕。名字已经随着画面熄灭，却没有因此回到一个还未选择的状态。"
    narrator "路明非摸了摸装着游戏币的口袋，确认金属仍在。门外的雨落在商场台阶上，明天的路线还没有写完，但今天留下的东西已经各自有了位置。"
    return
