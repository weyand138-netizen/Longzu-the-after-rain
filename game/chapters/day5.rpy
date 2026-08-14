init python:
    # Build-time inputs only. No Day 5 partial, terminal, or ending manifest is created here.
    from modules.day5_route_derivation import derive_route_answer_record
    from modules.day5_source_generation import DAY5_SOURCE_SHA256

    DAY5_SOURCE_UNIT_ID = "chapter_day5_family_lie"
    DAY5_REQUIRED_SCENE_IDS = (
        "scene_day5_family_archive",
        "scene_day5_truth_delivery",
        "scene_day5_response_answer",
        "scene_day5_shared_liability",
    )
    DAY5_CHOICE_RECORDS = (
        (
            "day5_share_full_archive",
            "reaction_day5_share_full_archive",
            "payoff_day5_full_archive_day7",
        ),
        (
            "day5_give_safe_summary",
            "reaction_day5_give_safe_summary",
            "payoff_day5_summary_day7",
        ),
        (
            "day5_include_self_in_truth",
            "reaction_day5_include_self_in_truth",
            "payoff_day5_self_liability_ending",
        ),
        (
            "day5_blame_family_only",
            "reaction_day5_blame_family_only",
            "payoff_day5_blame_day6",
        ),
        (
            "day5_honor_erii_response",
            "reaction_day5_honor_erii_response",
            "payoff_day5_honor_day6",
        ),
        (
            "day5_replace_erii_response",
            "reaction_day5_replace_erii_response",
            "payoff_day5_replace_ending",
        ),
        (
            "day5_repair_daily_choice",
            "reaction_day5_repair_daily_choice",
            "payoff_repair_daily_choice",
        ),
        (
            "day5_keep_daily_override",
            "reaction_day5_keep_daily_override",
            "payoff_keep_daily_override",
        ),
        (
            "day5_repair_school_evidence",
            "reaction_day5_repair_school_evidence",
            "payoff_repair_school_truth",
        ),
        (
            "day5_keep_school_evidence_hidden",
            "reaction_day5_keep_school_evidence_hidden",
            "payoff_keep_school_truth_hidden",
        ),
    )
    DAY5_CHOICE_EFFECTS = {
        "day5_share_full_archive": ("truth", "event:event_full_archive_shared"),
        "day5_give_safe_summary": ("revoke:token_withhold_family_truth",),
        "day5_include_self_in_truth": (
            "preparation",
            "sacrifice",
            "event:event_self_liability_disclosed",
        ),
        "day5_blame_family_only": ("event:event_external_blame_only",),
        "day5_honor_erii_response": (
            "autonomy",
            "event:event_route_preference_honored",
        ),
        "day5_replace_erii_response": (
            "revoke:token_override_daily_choice",
            "event:event_route_preference_overridden_to_old_order",
        ),
        "day5_repair_daily_choice": ("repair:token_override_daily_choice",),
        "day5_keep_daily_override": ("event:event_daily_override_unrepaired",),
        "day5_repair_school_evidence": ("repair:token_hide_school_evidence",),
        "day5_keep_school_evidence_hidden": (
            "event:event_school_evidence_stays_hidden",
        ),
    }
    DAY5_RESPONSE_REQUEST_ID = "event_family_response_requested"
    DAY5_RESPONSE_ANSWER_EVENT_ID = "event_erii_selects_route_response"
    DAY5_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day5_family_lie",
            "day_index": 5,
            "observable_fact_ids": (
                "fact_day5_family_archive_delivery",
                "fact_day5_route_answer_expressed",
            ),
            "source_unit_id": DAY5_SOURCE_UNIT_ID,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_day5_route_answer",
            "day_index": 5,
            "observable_fact_ids": ("fact_day5_route_answer_expressed",),
            "source_unit_id": DAY5_SOURCE_UNIT_ID,
        },
    )


default event_full_archive_shared = False
default cp_day5_full_archive_shared = False
default event_self_liability_disclosed = False
default event_external_blame_only = False
default event_family_response_requested = False
default event_erii_selects_route_response = False
default cp_day5_route_answer_expressed = False
default event_route_preference_honored = False
default event_route_preference_overridden_to_old_order = False
default event_daily_override_unrepaired = False
default event_school_evidence_stays_hidden = False
default day5_daily_override_was_unresolved = False
default agency_day5_response_answer = None
default agency_day5_response_outcome = None
default agency_day5_response_derivation_record = None


label chapter_day5_family_lie:
    $ current_chapter = "day5"
    scene bg warm_room

    # scene_day5_family_archive
    narrator "桌上的家族档案没有封口。绘梨衣把先前留下的车票、联系人卡、单人票，或空路线图放在一旁，再把档案推到灯下。"
    narrator "路明非看见她先确认手边还剩什么，再等他决定交出哪一部分。"
    narrator "灯下的纸边把每一处折痕都照了出来；没有被说出口的那一页，也和已经交出的部分一样占着位置。"

    # scene_day5_truth_delivery
    $ critical_choice_interaction = True
    menu:
        "把原始档案和其中不能确定的部分都交给她":
            $ apply_choice("day5_share_full_archive", {"truth": 1})
            narrator "她把原页、被划去的日期和没有答案的空白一并摊开，逐页看完后仍把它们留在自己面前。"
            $ event_full_archive_shared = True
            $ cp_day5_full_archive_shared = True
            $ critical_choice_interaction = False

        "只说一个更安全、却无法核对来源的结论":
            $ apply_choice("day5_give_safe_summary", {})
            narrator "他收起原页，只留下一个听上去足够安全的结论。她没有接那张被折小的纸。"
            $ critical_choice_interaction = False

    # scene_day5_response_answer
    $ day5_daily_override_was_unresolved = has_unresolved_token("token_override_daily_choice")
    $ agency_day5_response_derivation_record = derive_route_answer_record(
        {
            "resource_two_tickets": resource_two_tickets,
            "resource_contact_card": resource_contact_card,
            "event_contact_risk_handover_complete": event_contact_risk_handover_complete,
            "resource_single_ticket": resource_single_ticket,
        },
        DAY5_SOURCE_SHA256,
    )
    $ agency_day5_response_answer = agency_day5_response_derivation_record["selected_answer_state_id"]

    if agency_day5_response_answer == "shared_escape":
        narrator "她把两张票并排压在路线图上，没有把其中一张推回去。"
    elif agency_day5_response_answer == "independent_contact":
        narrator "她把联系人卡收进自己的夹层，指尖在风险说明上停了一下。"
    elif agency_day5_response_answer == "solo_departure":
        narrator "她把单人票放进自己的证件夹，合上夹子后才抬眼。"
    elif agency_day5_response_answer == "continue_without_executable_route":
        narrator "她把空路线图推回两人之间，手没有离开纸边。"
    else:
        narrator "手边的东西彼此对不上。绘梨衣没有把任何一张纸按成答案。"
    narrator "她看着这些物件之间留下的空隙，等他先承认眼前能做的事，而不是替空隙补上名字。"

    if agency_day5_response_answer != "undetermined":
        $ event_family_response_requested = True
        $ event_erii_selects_route_response = True
        $ cp_day5_route_answer_expressed = True
        $ critical_choice_interaction = True

        menu:
            "按她已经放下的方案继续准备":
                $ apply_choice("day5_honor_erii_response", {"autonomy": 1})
                narrator "路明非把自己的手移开，让她先收好票、卡或路线图，再把下一步写在她能看见的位置。"
                $ event_route_preference_honored = True
                $ agency_day5_response_outcome = "outcome_route_preference_honored_" + agency_day5_response_answer
                narrator "他等她把手边的东西收稳，才把自己的下一步写在没有遮住她视线的位置。"
                $ critical_choice_interaction = False

            "用旧秩序的安全方案替换她刚刚放下的选择":
                $ apply_choice("day5_replace_erii_response", {})
                narrator "他把纸张重新排成自己熟悉的顺序。她没有再把票、卡或路线图推回来。"
                $ event_route_preference_overridden_to_old_order = True
                $ agency_day5_response_outcome = "outcome_route_preference_overridden_to_old_order"
                narrator "重新排好的纸面看似整齐，却把她刚才留下的顺序压回了下面。"
                $ critical_choice_interaction = False

    # scene_day5_shared_liability
    $ critical_choice_interaction = True
    menu:
        "承认自己的选择也造成了风险，并写下由自己承担的后续步骤":
            $ apply_choice("day5_include_self_in_truth", {"preparation": 1, "sacrifice": 1})
            narrator "他在档案旁写下自己的名字和要承担的步骤，没有把那一栏留给她。她看完后，把纸留在两人之间。"
            $ event_self_liability_disclosed = True
            narrator "她的手指停在那一栏旁，没有替他把承认改写成一句轻松的话。"
            $ critical_choice_interaction = False

        "把责任都归到家族身上，不提自己的选择":
            $ apply_choice("day5_blame_family_only", {})
            narrator "他只说档案里的人和他们的命令。她听完，仍把空着的那一栏朝着他。"
            $ event_external_blame_only = True
            narrator "空着的地方没有因为责任被移开就消失，反而把桌面分成两段。"
            $ critical_choice_interaction = False

    if has_unresolved_token("token_hide_school_evidence"):
        $ critical_choice_interaction = True
        menu:
            "先补交第三日没有交出的原始证据":
                $ apply_choice("day5_repair_school_evidence", {})
                narrator "他把那几页被留下的记录补到档案里，承认先前只给过结论。她把两组纸放到同一盏灯下。"
                narrator "两组纸的日期终于挨在一起，迟到本身仍留在它们之间。"
                $ critical_choice_interaction = False

            "继续只给结论，不补交原始证据":
                $ apply_choice("day5_keep_school_evidence_hidden", {})
                narrator "他没有把那几页拿出来。她把档案合上，却没有把它收走。"
                narrator "合上的封面挡住了字，却没有挡住她知道那里仍缺了一段来源。"
                $ critical_choice_interaction = False

    if day5_daily_override_was_unresolved:
        $ critical_choice_interaction = True
        menu:
            "承认此前替她安排的决定，并撤回仍在生效的替代方案":
                $ apply_choice("day5_repair_daily_choice", {})
                narrator "他逐项承认自己替她安排过什么，把仍在生效的安排划掉，等她自己把纸重新摆好。"
                narrator "划去以后，纸面并没有恢复原样；她只把能由自己决定的那一格重新留给自己。"
                $ critical_choice_interaction = False

            "维持此前替她安排的方案":
                $ apply_choice("day5_keep_daily_override", {})
                narrator "他没有改动那几项安排。她把手从纸边收回，留下一段没有被填上的空白。"
                $ event_daily_override_unrepaired = True
                narrator "那段空白没有被解释成同意，安静地留在两人都看得见的地方。"
                $ critical_choice_interaction = False

    return
