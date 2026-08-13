init python:
    # Build-time inputs only. No Day 4 partial or terminal manifest is created here.
    DAY4_SOURCE_UNIT_ID = "chapter_day4_seaside_train"
    DAY4_REQUIRED_SCENE_IDS = (
        "scene_day4_ticket_counter",
        "scene_day4_route_answer",
        "scene_day4_contact_channel",
        "scene_day4_sea_window",
    )
    DAY4_CHOICE_RECORDS = (
        (
            "day4_buy_two_tickets_real_name",
            "reaction_day4_buy_two_tickets_real_name",
            "payoff_day4_two_tickets_day6",
        ),
        (
            "day4_buy_single_ticket_cash",
            "reaction_day4_buy_single_ticket_cash",
            "payoff_day4_single_ticket_ending",
        ),
        (
            "day4_register_independent_contact",
            "reaction_day4_register_independent_contact",
            "payoff_day4_contact_ending",
        ),
        (
            "day4_decline_independent_contact",
            "reaction_day4_decline_independent_contact",
            "payoff_day4_decline_contact_ending",
        ),
        (
            "day4_follow_one_route_no_backup",
            "reaction_day4_follow_one_route_no_backup",
            "payoff_day4_no_backup_day6",
        ),
    )
    DAY4_CHOICE_EFFECTS = {
        "day4_buy_two_tickets_real_name": (
            "preparation",
            "sacrifice",
            "acquire:resource_two_tickets",
            "event:event_identity_exposed",
        ),
        "day4_buy_single_ticket_cash": (
            "preparation",
            "acquire:resource_single_ticket",
        ),
        "day4_register_independent_contact": (
            "truth",
            "consume:resource_arcade_token",
            "acquire:resource_contact_card",
            "event:event_contact_risk_handover_complete",
        ),
        "day4_decline_independent_contact": (
            "revoke:token_abandon_backup_plan",
            "event:event_contact_channel_declined",
        ),
        "day4_follow_one_route_no_backup": (
            "revoke:token_abandon_backup_plan",
        ),
    }
    DAY4_ROUTE_PREPARATION_REQUEST_ID = "event_route_preparation_requested"
    DAY4_ROUTE_PREPARATION_ANSWER_STATE = "preserve_executable_self_controlled_option"
    DAY4_INDEPENDENT_CONTACT_REQUEST_ID = "event_independent_contact_option_requested"
    DAY4_INDEPENDENT_CONTACT_ANSWER_STATE = "keep_independent_contact_option"
    DAY4_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day4_seaside_train",
            "day_index": 4,
            "observable_fact_ids": (
                "fact_day4_self_controlled_option_presented",
                "fact_day4_ticket_or_contact_option_prepared",
            ),
            "source_unit_id": DAY4_SOURCE_UNIT_ID,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_day4_seaside_window",
            "day_index": 4,
            "observable_fact_ids": ("fact_day4_self_controlled_option_presented",),
            "source_unit_id": DAY4_SOURCE_UNIT_ID,
        },
    )


default event_identity_exposed = False
default event_two_window_tickets_acquired = False
default cp_day4_two_tickets_complete = False
default event_contact_risk_handover_complete = False
default event_contact_channel_declined = False
default resource_two_tickets = False
default resource_single_ticket = False
default resource_contact_card = False
default agency_day4_route_preparation_request = None
default agency_day4_route_preparation_answer = None
default agency_day4_route_preparation_outcome = None
default agency_day4_independent_contact_request = None
default agency_day4_independent_contact_answer = None
default agency_day4_independent_contact_outcome = None


label chapter_day4_seaside_train:
    $ current_chapter = "day4"
    scene bg warm_room

    # scene_day4_ticket_counter
    narrator "售票窗前只剩一盏低灯。绘梨衣把路线图、空白联系人纸片和零钱并排放在玻璃下。"
    narrator "她先把路线图推回路明非面前，再把能自己收下的票和纸片留在手边。"

    # scene_day4_route_answer
    $ agency_day4_route_preparation_request = DAY4_ROUTE_PREPARATION_REQUEST_ID
    narrator "她用指尖分别压住车次、窗口座位和联系人纸片，等他看清这些不是替她决定的答案。"
    $ agency_day4_route_preparation_answer = DAY4_ROUTE_PREPARATION_ANSWER_STATE
    $ critical_choice_interaction = True

    menu:
        "用真实姓名买两张靠窗票，交给她自己保管":
            $ apply_choice("day4_buy_two_tickets_real_name", {"preparation": 1, "sacrifice": 1})
            narrator "两张靠窗票落进她掌心。售票员核对姓名时停了一下，路明非知道这会留下被人找到的代价。"
            $ resource_two_tickets = True
            $ event_identity_exposed = True
            $ event_two_window_tickets_acquired = True
            $ cp_day4_two_tickets_complete = True
            $ agency_day4_route_preparation_outcome = "outcome_shared_option_prepared"
            $ critical_choice_interaction = False

        "买一张现金票，让她决定是否独自上车":
            $ apply_choice("day4_buy_single_ticket_cash", {"preparation": 1})
            narrator "她接过那张票，没有把它塞回他手里，只把路线图折到能一个人展开的那一页。"
            $ resource_single_ticket = True
            $ agency_day4_route_preparation_outcome = "outcome_solo_option_prepared"
            $ critical_choice_interaction = False

        "只按眼前的路线走，不再留下另一种准备":
            $ apply_choice("day4_follow_one_route_no_backup", {})
            narrator "路线图上只剩一条被折出来的线。她把联系人纸片收回袖口，没有替他补上空白。"
            $ agency_day4_route_preparation_outcome = "outcome_self_controlled_option_not_prepared"
            $ critical_choice_interaction = False

    # scene_day4_contact_channel
    if (
        "day2_save_second_token" in current_choice_history()
        and (
            "day2_accept_alias" in current_choice_history()
            or "day2_admit_alias_unknown" in current_choice_history()
        )
    ):
        $ agency_day4_independent_contact_request = DAY4_INDEPENDENT_CONTACT_REQUEST_ID
        narrator "那枚留下的游戏币和她自己输入过的昵称还在。她把它们放到联系人纸片旁，抬眼等他回应。"
        $ agency_day4_independent_contact_answer = DAY4_INDEPENDENT_CONTACT_ANSWER_STATE
        $ critical_choice_interaction = True

        menu:
            "用她保留的昵称和游戏币登记独立联系人":
                $ apply_choice("day4_register_independent_contact", {"truth": 1})
                narrator "她自己念出昵称的读法，把游戏币交给窗口后拿走联系人卡，也看完了背面写着的风险。"
                $ resource_contact_card = True
                $ event_contact_risk_handover_complete = True
                $ agency_day4_independent_contact_outcome = "outcome_independent_option_prepared"
                $ critical_choice_interaction = False

            "不登记联系人，让她把游戏币和纸片收回去":
                $ apply_choice("day4_decline_independent_contact", {})
                narrator "她把游戏币和写着昵称的纸片收回掌心。她保留了它们，也没有留下能继续联系的号码。"
                $ event_contact_channel_declined = True
                $ agency_day4_independent_contact_outcome = "outcome_independent_option_declined"
                $ critical_choice_interaction = False
    else:
        narrator "联系人纸片没有可用的识别物。绘梨衣把它折好，没有假装空白已经能替她留下一条路。"

    # scene_day4_sea_window
    narrator "列车进站的风从站台尽头吹进来。绘梨衣把票、路线图或纸片放进自己能拿到的口袋，再看向海的方向。"
    return
