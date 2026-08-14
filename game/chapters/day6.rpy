init python:
    # Build-time inputs only. Day 6 stages facts for later systems but does not
    # enter Day 7, invoke a resolver, write a qualification, or complete an ending.
    from modules.day6_commitment_derivation import derive_commitment_record
    from modules.day6_source_generation import DAY6_SOURCE_SHA256

    DAY6_SOURCE_UNIT_ID = "chapter_day6_no_safe_house"
    DAY6_REQUIRED_SCENE_IDS = (
        "scene_day6_safehouse_failure",
        "scene_day6_backup_exit",
        "scene_day6_cost_inventory",
        "scene_day6_route_commitment",
    )
    DAY6_CHOICE_RECORDS = (
        ("day6_reopen_service_exit", "reaction_day6_reopen_service_exit", "payoff_day6_exit_ending"),
        ("day6_abandon_backup", "reaction_day6_abandon_backup", "payoff_day6_abandon_ending"),
        ("day6_use_service_exit", "reaction_day6_use_service_exit", "payoff_day6_use_exit_ending"),
        ("day6_keep_backup_abandoned", "reaction_day6_keep_backup_abandoned", "payoff_day6_keep_backup_ending"),
        ("day6_disclose_withheld_archive", "reaction_day6_disclose_withheld_archive", "payoff_day6_late_truth_ending"),
        ("day6_keep_archive_withheld", "reaction_day6_keep_archive_withheld", "payoff_day6_keep_truth_ending"),
        ("day6_burn_old_identity", "reaction_day6_burn_old_identity", "payoff_day6_identity_cost_ending"),
        ("day6_shift_cost_to_erii", "reaction_day6_shift_cost_to_erii", "payoff_day6_shift_cost_ending"),
        ("day6_take_cost_back", "reaction_day6_take_cost_back", "payoff_day6_take_back_ending"),
        ("day6_leave_cost_shifted", "reaction_day6_leave_cost_shifted", "payoff_day6_leave_cost_ending"),
        ("day6_commit_independent_contact", "reaction_day6_commit_independent_contact", "payoff_route_independent_ending"),
        ("day6_commit_shared_escape", "reaction_day6_commit_shared_escape", "payoff_route_shared_ending"),
        ("day6_commit_solo_departure", "reaction_day6_commit_solo_departure", "payoff_route_solo_ending"),
        ("day6_commit_old_order_return", "reaction_day6_commit_old_order_return", "payoff_route_old_order_ending"),
        ("day6_no_executable_route", "reaction_day6_no_executable_route", "payoff_route_collapse_ending"),
    )
    DAY6_CHOICE_EFFECTS = {
        "day6_reopen_service_exit": ("preparation", "repair:token_abandon_backup_plan"),
        "day6_abandon_backup": ("revoke:token_abandon_backup_plan",),
        "day6_use_service_exit": ("event:event_service_exit_used",),
        "day6_keep_backup_abandoned": ("event:event_backup_stays_abandoned",),
        "day6_disclose_withheld_archive": ("truth", "repair:token_withhold_family_truth"),
        "day6_keep_archive_withheld": ("event:event_family_truth_stays_withheld",),
        "day6_burn_old_identity": ("sacrifice", "event:event_shared_cost_acknowledged"),
        "day6_shift_cost_to_erii": ("revoke:token_shift_promised_cost",),
        "day6_take_cost_back": ("sacrifice", "repair:token_shift_promised_cost", "event:event_shared_cost_acknowledged"),
        "day6_leave_cost_shifted": ("event:event_shifted_cost_confirmed",),
        "day6_commit_independent_contact": ("event:event_independent_route_committed",),
        "day6_commit_shared_escape": ("event:event_shared_route_committed",),
        "day6_commit_solo_departure": ("event:event_solo_route_committed", "event:event_no_continuing_contact_commitment"),
        "day6_commit_old_order_return": ("event:event_old_order_route_committed",),
        "day6_no_executable_route": ("event:event_route_collapse",),
    }
    DAY6_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day6_no_safe_house",
            "day_index": 6,
            "observable_fact_ids": (
                "fact_day6_safehouse_failure",
                "fact_day6_cost_consequence_expressed",
                "fact_day6_route_commitment_expressed",
            ),
            "source_unit_id": DAY6_SOURCE_UNIT_ID,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_day6_cost_and_route",
            "day_index": 6,
            "observable_fact_ids": ("fact_day6_route_commitment_expressed",),
            "source_unit_id": DAY6_SOURCE_UNIT_ID,
        },
    )


default event_safehouse_failed = False
default event_achievement_read_note_recovered = False
default cp_day6_note_recovery_complete = False
default event_service_exit_used = False
default cp_day6_service_exit_complete = False
default event_backup_stays_abandoned = False
default event_family_truth_stays_withheld = False
default event_cost_bearer_requested = False
default event_erii_rejects_shifted_cost = False
default event_cost_reconsideration_requested = False
default event_erii_rejects_shifted_cost_again = False
default event_shared_cost_acknowledged = False
default event_prior_cost_promise_honored_without_shift = False
default cp_day6_direct_cost_complete = False
default event_shifted_cost_consequence_visible = False
default event_shifted_cost_confirmed = False
default event_independent_route_committed = False
default event_shared_route_committed = False
default event_solo_route_committed = False
default event_no_continuing_contact_commitment = False
default event_old_order_route_committed = False
default event_route_collapse = False
default cp_day6_cost_reconsideration_complete = False
default agency_day6_cost_outcome = None
default agency_day6_cost_reconsideration_outcome = None
default agency_day6_commitment_derivation_record = None
default agency_day6_commitment_state = None


label chapter_day6_no_safe_house:
    $ current_chapter = "day6"
    scene bg warm_room

    # scene_day6_safehouse_failure
    narrator "安全屋的门锁在雨停前先响了一次。屋内没有人进来，走廊尽头却亮起了本不该亮的灯。"
    narrator "绘梨衣把票、卡、路线图和那张折过的纸逐一放在桌上，没有替任何一件东西说它一定能救谁。"
    $ event_safehouse_failed = True
    narrator "门外的声音只出现了一次，桌上的东西却因此都显出各自要承担的距离。"
    if event_note_preserved_by_erii:
        narrator "她从袖口取出那张被雨打湿的愿望纸。纸边已经干了，字仍在。路明非把它放回她手边，没有拿来替换任何路线。"
        $ event_achievement_read_note_recovered = True
        $ cp_day6_note_recovery_complete = True
        narrator "她把纸边压平，仍让那行字停在自己的手边，没有把它变成谁都必须遵守的路线。"

    # scene_day6_backup_exit
    if has_unresolved_token("token_abandon_backup_plan"):
        narrator "先前被放弃的备选路线现在已经有了代价：门锁、走廊灯和桌上的地图都把那段空白留在眼前。"
        if resource_service_exit:
            $ critical_choice_interaction = True
            menu:
                "重新打开此前记住的维修通道，并承担暴露位置的风险":
                    $ apply_choice("day6_reopen_service_exit", {"preparation": 1})
                    narrator "他撕下那道旧封条，把维修门的位置和暴露的风险一并写到地图边。绘梨衣看完，自己把路线图折到那一页。"
                    narrator "被重新打开的门没有抹掉先前放弃它的痕迹，地图上两道线仍然并排存在。"
                    $ critical_choice_interaction = False

                "承认备选已经被放弃，继续不把它伪装成还能使用":
                    $ apply_choice("day6_keep_backup_abandoned", {})
                    narrator "他没有去碰维修门的标记。绘梨衣把那处空白留在地图上，没有替他补成一条路。"
                    $ event_backup_stays_abandoned = True
                    narrator "那处空白像一块没有封好的门缝，提醒两人它曾经可以被选择，却不再假装仍然可用。"
                    $ critical_choice_interaction = False
        else:
            $ critical_choice_interaction = True
            menu:
                "承认从未留下可重开的出口，继续面对这段缺口":
                    $ apply_choice("day6_keep_backup_abandoned", {})
                    narrator "他把没有出口的那一边留在桌上。绘梨衣没有把空白说成安全，也没有替他画出不存在的门。"
                    $ event_backup_stays_abandoned = True
                    narrator "没有出口的事实没有更好听的写法；她只把地图转回两人都能看见的方向。"
                    $ critical_choice_interaction = False
    elif resource_service_exit:
        narrator "维修门的位置还在地图上。它不是突然出现的希望，只是此前被记下、现在仍能选择承担的路线。"
        $ critical_choice_interaction = True
        menu:
            "按已准备的计划启用维修通道，让她带着自己的票、卡或地图离开封锁区":
                $ apply_choice("day6_use_service_exit", {})
                narrator "他先打开维修门，再让她自己收好票、卡或地图。两人离开封锁区时，门后的灯没有替他们决定下一步。"
                $ event_service_exit_used = True
                $ cp_day6_service_exit_complete = True
                narrator "维修门合上时，留下的不是保证，而是两人都看见过的那段短暂通路。"
                $ critical_choice_interaction = False

            "把这条备选也留在封锁区，只走眼前没有准备的路":
                $ apply_choice("day6_abandon_backup", {})
                narrator "他把维修门的位置划出地图。绘梨衣看着那道划痕停了一会儿，随后把纸收回自己手边。"
                narrator "划痕留在纸上，像一条被主动放弃、却不能从记忆里擦掉的边界。"
                $ critical_choice_interaction = False

    if has_unresolved_token("token_withhold_family_truth"):
        narrator "安全屋失效的后果已经落到桌上：少掉的原始页让路线图只能写下更安全的结论，却少了一段不能核对的来处。"
        $ critical_choice_interaction = True
        menu:
            "交出此前省略的原始页，承认已经失去提前准备的时间":
                $ apply_choice("day6_disclose_withheld_archive", {"truth": 1})
                narrator "他把原始页摊在她面前，也把来得太晚写在日期旁。绘梨衣逐行看完后，没有替他把迟到说成及时。"
                narrator "迟到的纸页补回了来源，却没有把已经错过的准备时间一并补回。"
                $ critical_choice_interaction = False

            "继续只留下安全化结论，不让她核对原始页":
                $ apply_choice("day6_keep_archive_withheld", {})
                narrator "他没有把原始页拿出来。绘梨衣只看着那份结论，手仍压在缺少来源的空白处。"
                $ event_family_truth_stays_withheld = True
                narrator "她没有把那份结论撕掉，只让缺少来源的空白继续留在它旁边。"
                $ critical_choice_interaction = False

    # scene_day6_cost_inventory
    narrator "桌上剩下的是必须由谁承担的代价：旧身份、被追到的风险，以及谁还能保留自己选的路线。"
    if event_shared_cost_promised:
        narrator "她把当初覆在他掌心上的手收回到自己一边，等他先说明那句共同承担还算不算。"
    $ event_cost_bearer_requested = True
    narrator "绘梨衣把写着她名字的那一栏推开，没有替他接受任何把代价转给她的安排。"
    $ event_erii_rejects_shifted_cost = True
    narrator "他把笔停在半空，第一次看清桌面上并没有一栏可以替谁自动承担后果。"
    $ critical_choice_interaction = True

    menu:
        "烧掉自己的旧身份凭据，把风险和后果写在自己名下":
            $ apply_choice("day6_burn_old_identity", {"sacrifice": 1})
            narrator "他把旧身份凭据烧在空铁盒里，再把要承担的联络、追踪和失去写到自己一栏。绘梨衣看完后，把她的路线留在纸上。"
            $ event_shared_cost_acknowledged = True
            $ agency_day6_cost_outcome = "outcome_cost_borne_by_lu"
            if event_shared_cost_promised and "day6_shift_cost_to_erii" not in current_choice_history():
                $ event_prior_cost_promise_honored_without_shift = True
                $ cp_day6_direct_cost_complete = True
            $ critical_choice_interaction = False

        "把旧身份和追踪的代价写到她的路线与名字上":
            $ apply_choice("day6_shift_cost_to_erii", {})
            narrator "他把需要付出的代价移到她的路线旁。纸张没有变轻，只是她的名字被写进了原本不属于她的那一栏。"
            $ event_shifted_cost_consequence_visible = True
            $ agency_day6_cost_outcome = "outcome_cost_shifted_to_erii"
            narrator "那道被移过去的笔画没有让纸面变轻，只让两人都更清楚它是谁写下的。"
            $ critical_choice_interaction = False

            narrator "她把那一栏推回他面前，再一次摇头。被写下的后果已经摆在两人之间，不能靠沉默消失。"
            $ event_cost_reconsideration_requested = True
            $ event_erii_rejects_shifted_cost_again = True
            $ critical_choice_interaction = True
            menu:
                "收回已经转嫁的代价，烧掉自己的旧身份并承认这次伤害仍会留下痕迹":
                    $ apply_choice("day6_take_cost_back", {"sacrifice": 1})
                    narrator "他划掉她名字旁的安排，烧掉自己的旧身份凭据，也没有划掉先前写过那一笔。绘梨衣看着那道痕迹，才把路线重新放回桌上。"
                    $ event_shared_cost_acknowledged = True
                    $ cp_day6_cost_reconsideration_complete = True
                    $ agency_day6_cost_reconsideration_outcome = "outcome_cost_returned_to_lu"
                    narrator "划回自己名下以后，先前那道越界的笔画仍在纸上，不能被当作没有发生。"
                    $ critical_choice_interaction = False

                "维持由她承担的安排，把已经显出的后果留给她":
                    $ apply_choice("day6_leave_cost_shifted", {})
                    narrator "他没有划掉那一栏。绘梨衣把纸翻到背面，留下没有被共同承担的正面。"
                    $ event_shifted_cost_confirmed = True
                    $ agency_day6_cost_reconsideration_outcome = "outcome_cost_shift_confirmed"
                    narrator "纸被翻到背面，代价却没有跟着翻过去；她留下的沉默成为桌面上最重的一项。"
                    $ critical_choice_interaction = False

    # scene_day6_route_commitment
    $ agency_day6_commitment_derivation_record = derive_commitment_record(
        {
            "day5_answer_state_id": agency_day5_response_answer,
            "day5_response_outcome_id": agency_day5_response_outcome,
            "event_route_preference_honored": event_route_preference_honored,
            "event_route_preference_overridden_to_old_order": event_route_preference_overridden_to_old_order,
            "resource_contact_card": resource_contact_card,
            "event_contact_risk_handover_complete": event_contact_risk_handover_complete,
            "resource_two_tickets": resource_two_tickets,
            "event_shared_cost_acknowledged": event_shared_cost_acknowledged,
            "resource_single_ticket": resource_single_ticket,
            "token_override_daily_choice_unresolved": has_unresolved_token("token_override_daily_choice"),
        },
        DAY6_SOURCE_SHA256,
    )
    $ agency_day6_commitment_state = agency_day6_commitment_derivation_record["selected_commitment_state_id"]
    narrator "最后摆在桌上的不是一句保证，而是她仍愿意握住、或决定放开的那件东西。"

    if agency_day6_commitment_state == "independent_contact":
        narrator "她把联系人卡和风险说明收进自己的夹层，手没有离开卡边。"
        $ critical_choice_interaction = True
        menu:
            "确认由她独立保管联系人与风险说明，按她已经收好的方案离开":
                $ apply_choice("day6_commit_independent_contact", {})
                narrator "他没有再替她拿卡，只把安全屋外的时间和位置写给她看。她收好卡，先走到门边。"
                $ event_independent_route_committed = True
                narrator "门边的光先落在她手里的卡上，随后才照到他还没收起的纸。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "shared_escape":
        narrator "她把两张票并排放在路线图上，又把其中一张留在自己手边。"
        $ critical_choice_interaction = True
        menu:
            "确认两张票和共同路线，由两人一起承担已经写下的代价":
                $ apply_choice("day6_commit_shared_escape", {})
                narrator "他把自己的票放在她那张旁边，没有替她收走路线图。她确认站名后，才把两张票一起放进夹层。"
                $ event_shared_route_committed = True
                narrator "两张票贴在一起，却没有把各自要承担的那一段路变成同一张纸。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "solo_departure":
        narrator "她把单人票放进自己的证件夹，联系人卡的位置仍是空的。"
        $ critical_choice_interaction = True
        menu:
            "确认她独自持票离开，并不把持续联系承诺塞进这条路线":
                $ apply_choice("day6_commit_solo_departure", {})
                narrator "他没有替她补上一张联系人卡。她收好单人票，自己把证件夹扣上。"
                $ event_solo_route_committed = True
                $ event_no_continuing_contact_commitment = True
                narrator "证件夹扣上的声音很轻，空着的联系人位置却让这条路显得格外清楚。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "old_order_return":
        narrator "旧秩序的路线纸被放在桌上，压住了她先前自己收好的票、卡或地图。"
        $ critical_choice_interaction = True
        menu:
            "确认那份旧秩序方案已经取代她的回答，不把它称作她的选择":
                $ apply_choice("day6_commit_old_order_return", {})
                narrator "他把旧路线带离桌面，却没有说那是她同意的事。绘梨衣没有伸手去拿那张被压住的纸。"
                $ event_old_order_route_committed = True
                narrator "被压住的纸没有被撕开，旧秩序因此仍在场，却不再冒充她的回答。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "no_executable_route":
        narrator "票、卡和地图之间没有一项能被诚实地叫作可执行路线。绘梨衣把空白留在两人之间。"
        $ critical_choice_interaction = True
        menu:
            "承认现在没有可执行路线，不把空白伪装成她已经答应的方向":
                $ apply_choice("day6_no_executable_route", {})
                narrator "他没有替她补上答案。两人把空白留在地图上，先离开这间已经失效的安全屋。"
                $ event_route_collapse = True
                narrator "离开时那张空白地图没有被带走，像一件不能执行却必须记住的东西。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "undetermined":
        narrator "票、卡和地图的记录对不上，他没有把任何一张纸推成她的答案。"

    return
