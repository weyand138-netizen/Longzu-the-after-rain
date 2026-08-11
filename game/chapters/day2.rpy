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
    $ critical_choice_interaction = True

    menu:
        "按她输入的昵称确认":
            $ apply_choice("day2_accept_alias", {"understanding": 1, "autonomy": 1})
            narrator "她把手留在按键上，看着昵称在开场画面里亮起来。"
            erii "嗯。"
            $ critical_choice_interaction = False

        "换成我替她想的昵称":
            $ apply_choice("day2_assign_alias", {})
            narrator "她照着新的名字按完最后一个键，却把手从面板上移开。"
            $ critical_choice_interaction = False

        "承认刚才没有听懂，重新问她" if has_unresolved_token("token_silence_as_consent"):
            $ apply_choice("day2_admit_alias_unknown", {"understanding": 1})
            narrator "路明非把话收回来。绘梨衣重新敲下自己的昵称，再把屏幕推到他面前。"
            $ critical_choice_interaction = False

    # scene_day2_two_tokens
    narrator "出票口吐出两枚游戏币。绘梨衣把其中一枚放到路明非掌心，另一枚压在开始键旁。"
    $ critical_choice_interaction = True

    menu:
        "把第二枚币收好，留作之后认得出彼此的记号":
            $ apply_choice("day2_save_second_token", {"preparation": 1})
            narrator "她把第二枚币交给他保管，然后用留下的一枚币开始游戏。"
            $ critical_choice_interaction = False

        "把两枚币都投进去，陪她打完这一局":
            $ apply_choice("day2_spend_both_tokens", {"sacrifice": 1})
            narrator "最后一枚币落进机器。她把手放回操纵杆上，直到这一局的音乐停下。"
            $ critical_choice_interaction = False

    # scene_day2_last_machine
    narrator "最里面那台机器熄屏前，绘梨衣把掌心贴在玻璃上，又收回手。商场要打烊了。"
    lm "走吧。明天再想下一站。"
    narrator "她跟在他身边，没有催促，也没有回头。"
    return
