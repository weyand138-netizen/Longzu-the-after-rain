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
    narrator "售票员把玻璃窗擦过一遍，留下几道没有完全干透的水痕。路线图上的支线、窗口座位和联系人纸片被水痕切开，却仍然可以被她逐一指出。"
    narrator "路明非把前几天留下的收据放在路线图旁，没有把它递进窗口。绘梨衣看见名字的折痕，伸手把收据和联系人纸片分开，给每件东西留下独立的位置。"
    narrator "窗内的钟走得比站台广播慢半拍。能买到什么、要留下什么、谁来拿走，先在这块玻璃下变成了几件可以看清的物件。"
    narrator "绘梨衣把零钱按面额排好，最后才把路线图转回路明非面前。她的动作没有要求他马上回答，却把需要回答的东西全部放到了灯下。"

    # scene_day4_route_answer
    $ agency_day4_route_preparation_request = DAY4_ROUTE_PREPARATION_REQUEST_ID
    narrator "她用指尖分别压住车次、窗口座位和联系人纸片，等他看清这些不是替她决定的答案。"
    $ agency_day4_route_preparation_answer = DAY4_ROUTE_PREPARATION_ANSWER_STATE
    narrator "她先压住车次，再压住窗口座位，最后碰了一下联系人纸片。三个动作之间留有间隔，像是在确认它们可以被分别保留，而不是只能被一次性接受。"
    narrator "路明非把路线图上的折痕展开，让她指过的地方都露出来。过去几天留下的名字、游戏币和维修门没有自动变成路线，只在这张纸上提供了可以核对的背景。"
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
            narrator "她先看票面上的姓名，再把两张票错开叠放，让靠窗的位置仍然清楚可见。售票员的停顿没有被解释成偶然，路明非把自己的证件收回，却没有把票也收回。"
            narrator "她把票放进路线图折出的夹层，手指在夹层边缘停了一秒，确认两张票都在自己能够取到的位置。代价因此跟着票一起被保存，而不是被藏在售票窗后。"
            $ critical_choice_interaction = False

        "买一张现金票，让她决定是否独自上车":
            $ apply_choice("day4_buy_single_ticket_cash", {"preparation": 1})
            narrator "她接过那张票，没有把它塞回他手里，只把路线图折到能一个人展开的那一页。"
            $ resource_single_ticket = True
            $ agency_day4_route_preparation_outcome = "outcome_solo_option_prepared"
            narrator "她把单人票翻到背面，看清开车时间和座位号，再把它夹在收据后面。这个位置让票不会被风吹走，也让她不用现在就宣布是否要使用。"
            narrator "路明非把路线图剩下的折痕抚平。她没有把票交还，只用指尖沿着能够独自展开的那一页走了一遍。"
            $ critical_choice_interaction = False

        "只按眼前的路线走，不再留下另一种准备":
            $ apply_choice("day4_follow_one_route_no_backup", {})
            narrator "路线图上只剩一条被折出来的线。她把联系人纸片收回袖口，没有替他补上空白。"
            $ agency_day4_route_preparation_outcome = "outcome_self_controlled_option_not_prepared"
            narrator "她折路线图时避开了两条已经被划掉的支线，把剩下的一条压得很深。联系人纸片藏回袖口，边角却仍露出一点，像一条被放弃但没有被忘记的可能。"
            narrator "路明非看见自己的手停在另一张空白纸片上，随后把手收回。路线变得更简单，能由她保留的选择也因此变少。"
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
        narrator "游戏币在玻璃下滚了一小圈，停在纸片边缘。她用手指挡住它，没有让它继续滚到窗口另一端。"
        narrator "联系人纸片背面印着几行很小的字，风险说明被折痕遮住了一半。她先把纸片摊平，再把游戏币压在上面，等所有字都能被看见。"
        $ critical_choice_interaction = True

        menu:
            "用她保留的昵称和游戏币登记独立联系人":
                $ apply_choice("day4_register_independent_contact", {"truth": 1})
                narrator "她自己念出昵称的读法，把游戏币交给窗口后拿走联系人卡，也看完了背面写着的风险。"
                $ resource_contact_card = True
                $ event_contact_risk_handover_complete = True
                $ agency_day4_independent_contact_outcome = "outcome_independent_option_prepared"
                narrator "她拿到联系人卡后先没有放进包里，而是把背面的风险一行行看完。看完最后一行，她把卡片转到自己熟悉的方向，才把游戏币交出。"
                narrator "窗口里的工作人员问了一个确认问题。路明非没有替她回答，她用手指点了点卡片上的名字，等确认完成后把卡片收进自己的夹层。"
                $ critical_choice_interaction = False

            "不登记联系人，让她把游戏币和纸片收回去":
                $ apply_choice("day4_decline_independent_contact", {})
                narrator "她把游戏币和写着昵称的纸片收回掌心。她保留了它们，也没有留下能继续联系的号码。"
                $ event_contact_channel_declined = True
                $ agency_day4_independent_contact_outcome = "outcome_independent_option_declined"
                narrator "她先把纸片上的名字折进里面，再把游戏币包在纸片外侧。收回来的东西仍然属于她，却不再承担一条已经登记的联系路径。"
                narrator "路明非看着窗口把空白卡片收走，没有把“以后还能想办法”说出口。拒绝留下的不是一句话，而是一个以后可以被找到的地址。"
                $ critical_choice_interaction = False
    else:
        narrator "联系人纸片没有可用的识别物。绘梨衣把它折好，没有假装空白已经能替她留下一条路。"

    # scene_day4_sea_window
    narrator "列车进站的风从站台尽头吹进来。绘梨衣把票、路线图或纸片放进自己能拿到的口袋，再看向海的方向。"
    narrator "风把售票窗旁的纸屑卷到脚边。她先按住口袋里的票或卡片，再把路线图折成不会遮住姓名和时间的大小。"
    narrator "站台另一端亮起一排车灯，海的方向被玻璃反光切成几块。路明非没有告诉她应该看哪一块，只把自己手里的空白纸片收好。"
    narrator "她最后检查了一次口袋的开口，确认物件没有滑出来。当天的准备没有替他们决定旅程，只让下一步能够被她自己拿在手里。"
    narrator "列车停稳前，售票窗内的低灯熄了一盏。她回头看了一眼那块玻璃，再跟着人群走向站台边缘。"
    return
