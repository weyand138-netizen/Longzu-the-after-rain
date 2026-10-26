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
    scene bg family_archive_table

    # scene_day5_family_archive
    narrator "桌上的档案还没封口。绘梨衣把手边的纸放到一边，再把档案推到灯下。"
    narrator "我把原件和摘要放到她面前。原件里有我也说不清的地方。"
    narrator "我说：\"你想看哪一份，我就给你哪一份。\""
    narrator "她没立刻翻档案，只把手边能离开的东西整理好。等我把纸摊开，她才把手停在封面边。"
    narrator "我把那段被水渍糊住的备注翻到她面前：\"这里我也不确定。\""
    narrator "她没急着看，先把手边的东西收回夹层，再轻轻掀开一角。"
    show story erii_read_archive
    narrator "我问：\"哪一行要我念？\""
    narrator "她指到一个日期。我按着那一行读，遇到不确定的字就说不知道。"
    narrator "她没把档案拿走，只压平那页，一直盯着那一处。"

    # scene_day5_truth_delivery
    $ critical_choice_interaction = True
    menu:
        "把原始档案和其中不能确定的部分都交给她":
            $ apply_choice("day5_share_full_archive", {"truth": 1})
            narrator "她把原页和划掉的日期一起摊开，逐页看完，也没让我替她做结论。"
            narrator "我坐在另一边，看她翻页，直到她停在那张复印纸。"
            narrator "我说：\"这页我也没有答案。\""
            narrator "她没有逼我解释，只把纸留在眼前。"
            hide story
            $ event_full_archive_shared = True
            $ cp_day5_full_archive_shared = True
            $ critical_choice_interaction = False

        "只说一个更安全、却无法核对来源的结论":
            $ apply_choice("day5_give_safe_summary", {})
            narrator "我收起原页，只留下一个更稳的说法。"
            narrator "她没接过去。我知道我没有给她来源。"
            hide story
            narrator "我说完以后，纸页还压在掌心里。她没接过去，我也没再硬塞给她。"
            narrator "安全不等于真相。我不该用它来掩盖我没交出的部分。"
            $ critical_choice_interaction = False

    # scene_day5_response_answer
    scene bg family_archive_evidence_sorted
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
        narrator "她把联系人卡收进自己的夹层，指尖停在风险说明上。"
    elif agency_day5_response_answer == "solo_departure":
        narrator "她把单人票放进证件夹，合上夹子后才抬眼。"
    elif agency_day5_response_answer == "continue_without_executable_route":
        narrator "她把空路线图推回我和她之间，手没离开纸边。"
    else:
        narrator "手边的东西对不上。绘梨衣没有把任何一张纸当成答案。"
    narrator "她摆出来的方案还留在桌上：纸上记着的，都只是关于离开的线索。"
    narrator "我想起昨天的事：准备路线时说过的代价和漏洞。"
    narrator "她把一张纸往前推，又停住。"
    narrator "我问：\"你要我先准备哪一个？\""
    narrator "她没有替我写步骤，只把手边的纸放在能看见的位置。我等她把手拿开，才知道自己还要想。"
    narrator "我把笔放在纸旁，却没立刻写。\"我们应该一起决定。\""
    narrator "她合好夹层，没有递给我。我可以决定一切，但要不要照着做，还得看她。"
    narrator "我在空白页写下三件事：确认出口、处理身份、把原页留在她拿得到的地方。笔尖停在一行上，写不下\"她会怎么做\"。"
    narrator "我把纸转给她，让她能看到我写过的部分。她没有改，也没有推回去。"
    narrator "我说：\"这几项是我的。要走哪条路线，还是由你决定。\""
    narrator "她把手放在夹层上，轻轻点了一下。我把笔放下，等她自己决定要不要再看路线图。"

    if agency_day5_response_answer != "undetermined":
        $ event_family_response_requested = True
        $ event_erii_selects_route_response = True
        $ cp_day5_route_answer_expressed = True
        $ critical_choice_interaction = True

        menu:
            "按她已经放下的方案继续准备":
                $ apply_choice("day5_honor_erii_response", {"autonomy": 1})
                narrator "我把手移开，让她先收好手边的纸，再把下一步写在她能看见的位置。"
                $ event_route_preference_honored = True
                $ agency_day5_response_outcome = "outcome_route_preference_honored_" + agency_day5_response_answer
                narrator "我把自己的计划写下来，不是替她签字。只是把我能做的部分摆在她面前。"
                narrator "我写下时间、出口和能联系的地点，不把她的名字写进去。她留下的纸仍在她手边，我不能越过那条界线。"
                narrator "我说：\"这些是我的准备。要不要用，你自己决定。\""
                narrator "她看了看纸，然后把手收回去。"
                $ critical_choice_interaction = False

            "用旧秩序的安全方案替换她刚刚放下的选择":
                $ apply_choice("day5_replace_erii_response", {})
                narrator "我把纸重新排成自己熟悉的顺序。她没有再把票、卡或路线图推回来。"
                $ event_route_preference_overridden_to_old_order = True
                $ agency_day5_response_outcome = "outcome_route_preference_overridden_to_old_order"
                narrator "重新排好的纸面看起来更整齐，但那不等于她选过。"
                narrator "我知道自己在动她刚才留在桌上的东西。她没阻止，我也不能把这叫作同意。"
                narrator "我没有再说这是为了安全。纸上的顺序已经说明了我的意思。"
                $ critical_choice_interaction = False

    # scene_day5_shared_liability
    $ critical_choice_interaction = True
    narrator "档案里有别人的签名，也有我的批注。它们挤在同一页上，看起来像我可以把责任推给更早写名字的人。"
    narrator "但事实不是这样。我做过的选择，早就留在路线上了。"
    narrator "我不能替绘梨衣承担她没交给我的决定，也不能用\"都是他们逼的\"把自己的部分抹掉。"
    narrator "她看着档案的空白处，手没伸过来。我把笔留在自己这边。要写谁的名字、要做什么补救，都是我该负责的事。"
    narrator "我想起雨大、时间紧、追踪者太近，里面有事实，也有我逃避的借口。"
    narrator "我把纸拉正，确保空白栏不压到她的名字上。动作很小，但至少我不再假装一切都能共享。"
    narrator "我说：\"这部分是我做的。我会处理，不写到你这里。\""
    narrator "她看着纸上的字，没有替我开脱。我写下后续步骤，给她以后核对。"
    narrator "我把写好的纸放到档案旁，不盖住原页，也不折成她看不见的样子。"
    menu:
        "承认自己的选择也造成了风险，并写下由自己承担的后续步骤":
            $ apply_choice("day5_include_self_in_truth", {"preparation": 1, "sacrifice": 1})
            narrator "我在档案旁写下自己的名字和要承担的步骤，没有把那一栏留给她。她看完后，把纸留在我们之间。"
            $ event_self_liability_disclosed = True
            narrator "责任不是一句漂亮的话，它得留下能核对的东西。"
            narrator "我写下每一步时都停一下：谁会被联系、我该怎样处理旧身份、哪些地方不能再让她替我挡。"
            narrator "她没有立刻收走那张纸，但把路线图放到纸边。两样东西分开摆着：路线仍是她的，责任仍是我的。"
            $ critical_choice_interaction = False

        "把责任都归到家族身上，不提自己的选择":
            $ apply_choice("day5_blame_family_only", {})
            narrator "我只说档案里的人和他们的命令。她还是把那一栏留给我。"
            narrator "我看见空白栏还在，也知道自己不能继续装作这件事跟我无关。"
            $ event_external_blame_only = True
            narrator "说别人的事能让我暂时轻一点，但纸面上空着的地方没有消失。"
            narrator "她没替我填名字，也没问我为什么避开。我只能看着那一栏，知道我该自己去写。"
            $ critical_choice_interaction = False

    if has_unresolved_token("token_hide_school_evidence"):
        $ critical_choice_interaction = True
        menu:
            "先补交第三日没有交出的原始证据":
                $ apply_choice("day5_repair_school_evidence", {})
                narrator "我把那几页被留下的记录补到档案里，承认先前只给过结论。她把两组纸放到同一盏灯下。"
                narrator "两组纸的日期终于挨在一起，迟到本身仍留在它们之间。"
                narrator "我把第三天的门禁记录、照片和时间表按原来的顺序放到档案旁。它们比摘要凌乱得多，也有我没能说清的地方。我没有再把它们压成一个好听的方向，只对绘梨衣说：\"那天我没给你看这些。"
                narrator "现在给你。\""
                narrator "她先看日期，再看照片。纸页在灯下挨着，晚了几天的事实也挨在一起。我没有说现在交出来就等于及时。她没有替我说。她只是把纸放到自己能再打开的位置，让我不能再假装那几页没有被她看见。"
                narrator "我把手从记录边移开，等她翻页。迟到已经发生，补交不能变成擦掉；可原页现在在灯下，至少以后再谈它时，不只剩我一个人的结论。"
                $ critical_choice_interaction = False

            "继续只给结论，不补交原始证据":
                $ apply_choice("day5_keep_school_evidence_hidden", {})
                narrator "我没有把那几页拿出来。她把档案合上，却没有把它收走。"
                narrator "合上的封面挡住了字，她的手却仍停在那处空白旁；我看得出来源没有被真正交到她手里。"
                narrator "我没有把第三天的纸拿出来，档案因此合得很平。绘梨衣的手停在封面边缘，没有把它推回我。她没有要求我解释为什么还扣着来源，我也没有用她没问来安慰自己。"
                narrator "未交出去的纸仍在我这边，这件事比合上的封面更沉。"
                narrator "我看见她把路线图放在档案旁，却没有把两样东西叠到一起。路线可以摆在眼前，来源却还缺着一段。她没有替我把缺口补上，我也不把这种安静称作接受。"
                $ critical_choice_interaction = False

    if day5_daily_override_was_unresolved:
        $ critical_choice_interaction = True
        menu:
            "承认此前替她安排的决定，并撤回仍在生效的替代方案":
                $ apply_choice("day5_repair_daily_choice", {})
                narrator "我逐项承认自己替她安排过什么，把仍在生效的安排划掉，等她自己把纸重新摆好。"
                narrator "划去以后，纸面并没有恢复原样；她只把能由自己决定的那一格重新留给自己。"
                $ critical_choice_interaction = False

            "维持此前替她安排的方案":
                $ apply_choice("day5_keep_daily_override", {})
                narrator "我没有改动那几项安排。她把手从纸边收回，留下一段没有被填上的空白。"
                $ event_daily_override_unrepaired = True
                narrator "那段空白没有被解释成同意，安静地留在我和她都看得见的地方。"
                $ critical_choice_interaction = False

    narrator "风停了，桌上的纸也不再动。杯底压着路线图的一角，边上留着一道湿印。"
    narrator "绘梨衣把手边的纸往灯下挪了挪，指尖停在页边。我说：\"还要念吗？\""
    narrator "她没抬头。纸角卷着，她低头慢慢捋平，手在上面停了片刻。"
    narrator "门外传来收伞的声音，水滴零零落落敲在地上。我侧耳听了一会儿，再转回来时，她已经开始叠纸了。"
    narrator "她把要带的纸收进夹层。收据露出一小截白边，她用指尖推了进去，拉好包带。"
    narrator "我扣上笔帽，合好自己的笔记。桌上那一栏还在灯下，我看了一眼，把手收回来。"
    narrator "我问：\"走吗？\""
    narrator "她朝门口迈了一步。我把桌灯拧暗，起身时椅脚擦过地面，响得有些突兀。"
    narrator "走到门边，我回头看了一眼。档案留在桌上，封皮的边缘被灯照得发白。"
    scene bg residential_stairwell_night
    narrator "楼道里的灯比屋里冷。包带擦过门框，绘梨衣停下来理好，再迈下第一级台阶。"
    narrator "我跟在后面，笔记本夹在臂弯里。窗玻璃上映着两个人的影子，走过拐角，就看不见了。"
    narrator "楼下有人开门。她停住，我也停住。门合拢以后，我们又等了一会儿。"
    narrator "她扶了扶肩上的包带，继续往下走。我跟上去，鞋底在湿冷的台阶上轻轻一响。"
    scene bg residential_street_after_rain_night
    narrator "到一楼时，已经看不见桌灯了。夜风从门口吹来，她抬手压住衣角。我把笔记夹紧，跟着走了出去。"
    return
