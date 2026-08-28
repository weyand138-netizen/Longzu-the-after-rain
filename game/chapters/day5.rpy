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
    narrator "桌上的家族档案没有封口。我看见绘梨衣把先前留下的车票、联系人卡、单人票，或空路线图放在一旁，再把档案推到灯下。"
    narrator "我看见她先确认手边还剩什么，再等我决定交出哪一部分。"
    narrator "灯下的纸边把每一处折痕都照了出来；没有被说出口的那一页，也和已经交出的部分一样占着位置。"
    narrator "我把手放在档案封面上，能感觉到纸页受潮后微微发软。里面有我已经读过的原页，也有我还没有说出口的空白；我不能因为先知道，就替她承受这份信息。"
    narrator "档案的纸张比愿望纸厚，边缘却被翻得起毛。最上面一页有铅笔写过又擦掉的编号，擦痕下还留着一点灰。没有谁在这张桌子旁替我解释那些编号，只有我昨晚看过的原件、今天还没有交出的纸，以及绘梨衣放在旁边的票和卡。"
    narrator "我把原页和摘要分开放。摘要只有两张，句子很短，读起来像能让人立刻知道该往哪儿走；原页有许多日期、签名和互相对不上的记录。把摘要交出去会让这段时间少一点重量，把原页交出去会让她不得不面对更多我也无法回答的空白。两种做法都不是没有代价的保护。"
    narrator "绘梨衣没有翻开档案。她先把手边的票、卡或路线图摆正，确认它们没有压在档案下面，然后才把手停到封面附近。她没有碰到封面，我也没有替她把手放上去。她先确认能离开的东西还在，才允许这份纸出现在灯下。"
    narrator "我说：\"这里有原件，也有我写的摘要。原件里有我也说不清的地方。你想看哪个，我给哪个。\""
    narrator "她抬头看我，又看纸。她没有给出完整的口头回答，只把离自己最近的票往旁边推开一点，给档案腾出位置。这个动作没有替我选出交付方式，却让我知道她没有要我把档案立刻收走。剩下要交出多少，仍然是我必须承担的决定。"
    narrator "灯泡发出细微的嗡鸣，窗外的风把桌上的纸角吹起又落下。我把手掌从封面上挪开，免得自己一直压着它像在替她保管答案。她看得见原页的厚度，也看得见摘要的薄；我不再用“更安全”掩盖我删掉了什么。"
    narrator "原页最下面有一段被水渍糊住的备注，我昨夜看了很久也没完全读懂。摘要里没有写它，因为我不知道它意味着什么；可不写并不等于它不存在。我把那页翻到能看见的位置，先告诉她：\"这里我也不确定。\""
    narrator "绘梨衣没有马上看那段备注。她把票或卡放回夹层，先把夹层扣好。然后她才把指尖放到原页边缘，轻轻掀开一角。我没有抢着把纸推平，只等她自己决定要不要翻到那一页。"
    narrator "纸页翻开以后，旧墨水的颜色比灯光更深。里面有名字、日期、被划掉的路线，还有一处我没能核实的空白。她的眼睛沿着字移动，我却不知道她读到哪一句。解释从我嘴里出来会很容易填满房间，可她没有要我替她读，我便只留在椅子里。"
    narrator "我问：\"哪一行要我念？\""
    narrator "她把手指停在一个日期旁。那是我能看清的回答。我按着她指的那一行读，不往前也不往后。读到不确定的字时，我说不知道；读完后我把声音停住，等她决定还要不要看下一行。"
    narrator "她没有拿走档案，也没有把它推回我面前。她把那一页压平，手掌留在纸上。这个动作不等于她接受了所有内容，但它让原页仍在她能重新核对的地方。我不能再说我已经替她把最坏的部分挡住了，因为她现在看见的正是我以前想替她略过的东西。"

    # scene_day5_truth_delivery
    $ critical_choice_interaction = True
    menu:
        "把原始档案和其中不能确定的部分都交给她":
            $ apply_choice("day5_share_full_archive", {"truth": 1})
            narrator "她把原页、被划去的日期和没有答案的空白一并摊开，逐页看完后仍把它们留在自己面前。"
            narrator "原页翻到中间时，夹着一张很薄的复印纸。她先把复印纸抽出来，举到灯下看背面的印章。印章有一半被裁掉，我没有说那代表什么，因为我也不能确认。她把它放在原页旁边，没有让我替她把两张纸重新叠好。"
            narrator "我坐在桌子的另一侧，能看见她每次翻页前都会把纸角对齐。她没有问我哪一页最重要，我也没有指着某一行要求她先看。档案的顺序是我带来的，阅读的顺序却在她自己的手里。"
            narrator "我说：\"这一页我没有答案。那一页我也没有。\""
            narrator "她听完，手指停在被划去的日期旁。她没有逼我给出完整解释，也没有把纸还给我。我知道把不确定交出去不是把责任一并丢给她；我还得继续对自己隐瞒过的、没核对过的部分负责。"
            narrator "灯下的纸越来越多，桌面几乎被占满。她把票、卡或路线图移到最边上，给原页留出位置。我没有把这种让位说成她愿意承受全部，只承认她现在选择让这些纸仍然摆在眼前。"
            $ event_full_archive_shared = True
            $ cp_day5_full_archive_shared = True
            $ critical_choice_interaction = False

        "只说一个更安全、却无法核对来源的结论":
            $ apply_choice("day5_give_safe_summary", {})
            narrator "我收起原页，只留下一个听上去足够安全的结论。她没有接那张被折小的纸。"
            narrator "我把答案说出口时，纸页还压在掌心下面。她没有伸手来拿，我便知道这句结论没有替她看见来源，也不能把她的沉默算作接受。"
            narrator "结论只有几句话，原页却在我掌心里越压越厚。我讲完以后，教室里没有任何东西因此变轻。她的眼睛停在我没递出去的纸边，我能看见那条边，却还是没有把手松开。"
            narrator "我说“这样比较安全”时，自己先听见了这句话里的问题。安全的是我不必让她看见全部，还是她真的少受一点伤？我不能从她没有回应的脸上替自己选一个更好听的答案。"
            narrator "她没有接纸。我没有问她要不要原件，因为这个问题到了这里已经像是让她替我的隐瞒做裁决。我只是把纸继续放在手里，承认此刻没有交出去的来源仍然由我扣着。"
            narrator "窗外风掀起一页档案的边，她没有去按。我把那页按回去，听见纸张摩擦的声音。这个动作很小，却足以提醒我：我选择了只说结论，而不是让她自己看见。后面不论她是否追问，我都不能假装这不是我的选择。"
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
        narrator "她把空路线图推回我和她之间，手没有离开纸边。"
    else:
        narrator "手边的东西彼此对不上。绘梨衣没有把任何一张纸按成答案。"
    narrator "她看着这些物件之间留下的空隙，等我先承认眼前能做的事，而不是替空隙补上名字。"
    narrator "两张靠窗票并排时，座位号朝上；联系人卡收进夹层时，背面的风险说明还露着一角；单人票合起来以后，只剩出发时间能看见。每一种排列都是她已经做过的动作，我可以看见，也可以回应，却不能跳过询问，把它们称作她已经向我许下的终点。"
    narrator "我把昨天售票窗前的事重新想了一遍。实名的代价落在我身上，卡片被追到的风险落在她能看见的说明上，单人票则让她保留一个我不能替走的出口。现在这些物件摆在桌上，并没有自己开口说哪条路线更正确。它们只把此前的选择带回到今天。"
    narrator "她把一张纸往前推一点，又停住。纸没有越过桌子的中线，也没有塞进我的手里。我看见这个距离，便把自己的椅子往后挪开，不让膝盖堵住她想拿回物件的方向。"
    narrator "我问：\"你要我先准备哪一个？\""
    narrator "她没有替我写步骤。她只是把票、卡或单人票留在能够看见的位置，或把空路线图推回来。我等她把手离开，才承认这些是我现在能够回应的东西：不是她的心意，不是她对我的保证，而是一件件被她留在桌上的可执行物。"
    narrator "我把笔放在纸旁，却没有立即写。写下路线、联络时间或撤离点很容易让纸看起来像已经达成的协议。我先把笔横放，告诉她：\"我写的是我该做的部分。你随时能把它划掉。\""
    narrator "她把夹层合上以后，没有把它交给我。票、卡或单人票留在她手里时，桌面上就多出了一条我不能替走的边界。我可以把门外的时间、我能去的地点、需要承担的联络写下来；她要不要沿着那条信息走，仍然要由她自己的手把物件拿出来。"
    narrator "我把纸翻到空白的一面，先写下我会做的三件事：确认出口、处理我的身份、把能核对的原页留在她能拿到的地方。写到这里，我停住。后面本能地想写“她会……”，笔尖却悬在纸上。我把那一行留白，知道那不是漏写，而是不该由我写。"
    narrator "我把纸转向她，让她能读到已经写下的部分。她没有拿笔改，也没有把纸推回。她先看了看门口，又看夹层。我的字没有因此变成共同计划，只是把我不能再逃掉的步骤摆在她面前。"
    narrator "我说：\"这几项是我的。你的票、卡和路线，还是你的。\""
    narrator "她把手放在夹层上，随后轻点一下。我没有把这一点解释成同意同行、同意联系或同意留下。它只让我知道她听见了物件仍在她手里。于是我把笔放下，等她自己决定是否再打开路线图。"

    if agency_day5_response_answer != "undetermined":
        $ event_family_response_requested = True
        $ event_erii_selects_route_response = True
        $ cp_day5_route_answer_expressed = True
        $ critical_choice_interaction = True

        menu:
            "按她已经放下的方案继续准备":
                $ apply_choice("day5_honor_erii_response", {"autonomy": 1})
                narrator "我把自己的手移开，让她先收好票、卡或路线图，再把下一步写在她能看见的位置。"
                $ event_route_preference_honored = True
                $ agency_day5_response_outcome = "outcome_route_preference_honored_" + agency_day5_response_answer
                narrator "我等她把手边的东西收稳，才把自己的下一步写在没有遮住她视线的位置。"
                narrator "纸上的字是我需要完成的部分，不是替她签下的承诺。我写完以后把笔横放，等她自己决定是否还要看路线图。"
                narrator "我写下时间、出口和能联系的地点，每写完一项都停下来确认没有把她的名字写进去。她的票、卡或路线图留在她手边，不需要我用笔替她确认去向。写到最后一行时，我把纸转过去，让她能看清我承诺的是我自己要做的事。"
                narrator "她没有立刻读。她先把手边的物件收好，又把路线图的一角露在外面。我不把这个顺序理解成她已经同意我的安排。它只让我知道她仍在保管自己先前摆下的东西，我的字不能越过这条界线。"
                narrator "我说：\"这些是我的准备。要不要用，你自己决定。\""
                narrator "她看了看纸，没有接笔。我把笔放下。写在桌上的步骤会在以后被核对，也会暴露我有没有做到；这比让我在今天得到一句肯定更重要。"
                $ critical_choice_interaction = False

            "用旧秩序的安全方案替换她刚刚放下的选择":
                $ apply_choice("day5_replace_erii_response", {})
                narrator "我把纸张重新排成自己熟悉的顺序。她没有再把票、卡或路线图推回来。"
                $ event_route_preference_overridden_to_old_order = True
                $ agency_day5_response_outcome = "outcome_route_preference_overridden_to_old_order"
                narrator "重新排好的纸面看似整齐，却把她刚才留下的顺序压回了下面。"
                narrator "我把票、卡或路线图挪开时，纸面确实看起来更像我熟悉的方案。熟悉不等于她选过。她没有抢回来，我也没有因此觉得自己得到许可。物件被我重新排列的事实摆在桌上，比任何自我解释都更清楚。"
                narrator "她的手停在桌边，没有碰被压住的那张纸。我没有问她为什么不拿。旧秩序常常就是这样起作用：把人逼到要先越过别人的手和安排，才能碰到原本属于自己的东西。此刻那只手是我的。"
                narrator "我没有再说这是为了安全。纸上的顺序已经替我说明，我把她刚才留下的回答推到了下面。她没有点头，我也不能再把沉默当成可以替我盖章的东西。"
                $ critical_choice_interaction = False

    # scene_day5_shared_liability
    $ critical_choice_interaction = True
    narrator "档案里有别人的签名，也有我的批注。它们挤在同一页上，看起来像只要把责任推给更早写下名字的人，我后来做过的选择就能从纸上消失。我知道事实不是这样：我曾经选择过路线、催过时间，也曾把自以为安全的答案放到她面前。"
    narrator "我不能替绘梨衣承担她没有交给我的决定，也不能用“都是他们逼的”把自己已经做过的部分擦掉。承认这一点不会让档案里的伤害变轻，更不会要求她原谅。它只是在这张纸上留出一栏，让我不能继续站在故事外面。"
    narrator "她看着档案的空白处，手没有来拿笔。笔放在我这边，我便把它留在我这边。要写谁的名字、要做哪些补救，是我现在能亲手完成、也该由我承担的事；我不需要她点头来证明我该负责。"
    narrator "我曾把某些选择说成形势所迫：雨太大、时间太少、追踪者太近、别人给的命令太硬。那些话里有事实，也有我借来躲开自己的部分。形势不会因为我承认而消失，可我在形势里动过的手、说过的话、没问出口的问题，也不会因为形势艰难就变成别人的笔迹。"
    narrator "绘梨衣的名字还在路线图另一侧，和空白责任栏隔着一段纸。我把纸拉正，确保那一栏没有压到她的名字上。这个动作很小，甚至不像补救；但至少我不再让纸面看起来像我们可以共享一个不清楚的代价。"
    narrator "我说：\"这部分是我做的。我会处理，不写到你这里。\""
    narrator "她没有替我回答，也没有替我原谅自己。她只看着纸上的字，手指在空白边缘停了一会儿。那一会儿足够让我明白，承认不是一次说完就能索取回应的行为。我要写下后续步骤，是为了让她日后能核对我有没有做到，不是为了让她当场给我轻一点的结论。"
    narrator "我把写好的纸放到档案旁，不盖住原页，也不折成她看不见的样子。风从窗缝里进来，纸角颤了一下。我用杯子压住自己的那一页，没有去压她手边的票和卡。"
    menu:
        "承认自己的选择也造成了风险，并写下由自己承担的后续步骤":
            $ apply_choice("day5_include_self_in_truth", {"preparation": 1, "sacrifice": 1})
            narrator "我在档案旁写下自己的名字和要承担的步骤，没有把那一栏留给她。她看完后，把纸留在我们之间。"
            $ event_self_liability_disclosed = True
            narrator "她的手指停在那一栏旁，没有替我把承认改写成一句轻松的话。"
            narrator "我写下每一步时都停了一下：谁会被联系、我该怎样处理旧身份、哪些地方不能再让她替我挡。字迹因为手指发紧有些歪，我没有重写得漂亮。责任不是一份写得好看的声明，它得留下她以后能照着核对的具体东西。"
            narrator "她看完后没有把纸折起来。她把纸留在原页旁，手指碰到我的名字又收回。我没有问她是不是相信，也没有问她能不能原谅。她没有替我填那一栏，我也不需要她替我证明这几步应该由我做。"
            narrator "我说：\"你可以留着。\""
            narrator "她没有立刻收走，却把路线图放到纸边。两样东西没有叠在一起：路线仍是她的，责任仍是我的。我看见这道分开，便不再把共同待在一张桌子旁说成她已经答应和我一起承担。"
            $ critical_choice_interaction = False

        "把责任都归到家族身上，不提自己的选择":
            $ apply_choice("day5_blame_family_only", {})
            narrator "我只说档案里的人和他们的命令。她听完，仍把空着的那一栏朝着我。"
            narrator "我看见那一栏仍然空着，也听见自己把句子说得像是在讲别人的事。她没有替我把名字填进去，我也没有资格让纸面替我省略。"
            $ event_external_blame_only = True
            narrator "空着的地方没有因为责任被移开就消失，反而把桌面分成两段。"
            narrator "我讲那些更早的命令、那些档案里陌生的签名时，自己的声音听起来很顺。绘梨衣没有打断，却把空白栏朝我推近一点。她没有写我的名字，也没有问我为何避开。我看见她把纸推近，不去假装那一栏不存在。"
            narrator "我没有接笔。纸停在我面前，空白比刚才更显眼。把责任讲成别人的事确实能让我暂时少看一点，可我不能让这种轻松冒充事实。她没有替我补，我也没有资格要求她替我把沉默叫作理解。"
            narrator "窗外的风吹动纸角，她用杯子压住档案的一边，我压住另一边。我们没有同时按住空白栏。那一栏仍然朝着我，等待的不是她给答案，而是我终于愿不愿意把自己的部分写进去。"
            $ critical_choice_interaction = False

    if has_unresolved_token("token_hide_school_evidence"):
        $ critical_choice_interaction = True
        menu:
            "先补交第三日没有交出的原始证据":
                $ apply_choice("day5_repair_school_evidence", {})
                narrator "我把那几页被留下的记录补到档案里，承认先前只给过结论。她把两组纸放到同一盏灯下。"
                narrator "两组纸的日期终于挨在一起，迟到本身仍留在它们之间。"
                narrator "我把第三天的门禁记录、照片和时间表按原来的顺序放到档案旁。它们比摘要凌乱得多，也有我没能说清的地方。我没有再把它们压成一个好听的方向，只对绘梨衣说：\"那天我没给你看这些。现在给你。\""
                narrator "她先看日期，再看照片。纸页在灯下挨着，晚了几天的事实也挨在一起。我没有说现在交出来就等于及时。她没有替我说。她只是把纸放到自己能再打开的位置，让我不能再假装那几页没有被她看见。"
                narrator "我把手从记录边移开，等她翻页。迟到已经发生，补交不能变成擦掉；可原页现在在灯下，至少以后再谈它时，不只剩我一个人的结论。"
                $ critical_choice_interaction = False

            "继续只给结论，不补交原始证据":
                $ apply_choice("day5_keep_school_evidence_hidden", {})
                narrator "我没有把那几页拿出来。她把档案合上，却没有把它收走。"
                narrator "合上的封面挡住了字，她的手却仍停在那处空白旁；我看得出来源没有被真正交到她手里。"
                narrator "我没有把第三天的纸拿出来，档案因此合得很平。绘梨衣的手停在封面边缘，没有把它推回我。她没有要求我解释为什么还扣着来源，我也没有用她没问来安慰自己。未交出去的纸仍在我这边，这件事比合上的封面更沉。"
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

    narrator "桌上的纸终于不再被风吹动。档案、票、卡、路线图和我写下或没有写下的那一栏仍然分开摆着。我没有把它们叠成一份好看的结论，因为它们来自不同的日子：站台的路线、街机的名字、空教室的记录、售票窗的风险，以及我今天必须面对的责任。"
    narrator "绘梨衣先检查夹层，再把手放到档案旁。她没有把所有纸拿走，也没有把所有纸留给我。她只把自己要保管的物件收好，其他的仍留在灯下。我看见她这样分开，便不替她替任何一张纸决定最终去处。"
    narrator "我把自己的笔记翻到空白页。上面没有她的名字，只有我还得去做的事。那些事不会因为我说过真话就自动完成，也不会因为她没有当场回答就变得无关。我把笔记合上，决定先按写下的部分去做。"
    narrator "我说：\"这些我会带着。你的东西在你这里。\""
    narrator "她没有给我一个总的回答。她只是把路线图边缘压平，又向门口看了一眼。窗外的雨已经比白天小，门外却仍然有风。我没有替她先走，也没有用档案里的话挡住门。今天能被说清的部分已经在纸上，剩下的要靠之后真正去做。"
    narrator "离开桌子前，我把原页放回她能看见的位置，摘要没有压在上面。无论她今天看过多少、有没有要我继续读，来源和结论都不再被我故意混在一起。她如果以后想重新核对，纸还在那里；我如果想再逃开，也得先经过自己写下的那一栏。"
    narrator "桌灯照着原页上的折痕，像把前几天留下的时间一格格摊开。我先看见站台路线图的一角，又看见收据露出的白边、游戏币压过纸面的圆印、空教室照片上没有被解释的阴影。它们没有自动排成一条通往正确答案的线，只让每一次交出、扣住、等待和催促都有了能被重新看见的地方。"
    narrator "我把笔帽盖上，没把笔递给绘梨衣。空白栏如果还在，应该由我承担它空着的含义，而不是让她替我写一段能让我舒服的原谅；已经写下的栏也不能因为墨迹干了，就变成她必须相信的保证。"
    narrator "她把档案往自己这边挪了一点，停在桌灯能照到的位置。我看见她没有把它塞进包底，也没有把它推回我面前。这个位置并不告诉我她现在想知道多少，只告诉我纸还在她够得着的地方。于是我没有替她合上，也没有继续翻。"
    narrator "窗缝里钻进来的风把路线图吹得微微起伏。我用杯子压住空白的一角，刻意没有压到她正看的那一页。压住纸和替她决定阅读到哪里只有一指宽的差别，我今天已经错过太多次，不想再用一个看似体贴的动作把这点差别抹掉。"
    narrator "我想起第三天空教室里，她的指尖停在门禁时间上。那时我以为只要把数字说出来就算诚实；现在我看着原页才知道，诚实还包括承认哪些数字我没有核实、哪些页我曾经没交、哪些结论是我自己替她整理出来的。"
    narrator "我说：\"看不懂的地方，你指。我只念你指的。\""
    narrator "她没有立即指向哪一行。她先把纸页边缘捋平，随后把手停在一段被水渍晕开的字旁。我没有抢着凑近解释。等她真的碰到某一行，或者把纸转向我，我再把我能确认的部分说出来；没被指到的部分先留在原地。"
    narrator "桌外传来有人收伞的水声。我没有因为那个声音把文件匆忙收起，也没有说外面可能有人。声音来自门外是事实，它是不是冲着我们来不是。我不再让猜测借着紧张抢走她还在看的纸。"
    narrator "她把路线图和档案分开叠好，两个折痕没有对齐。我看见这道不齐，反而松了一点：路线不必替真相盖章，真相也不必替她把下一站选好。我们可以在同一张桌上面对它们，又让它们各自保留不同的问题。"
    narrator "我把自己写下的责任纸留在最外侧，名字朝上。那张纸不应该藏进我口袋，像一种只在我需要时才拿出来的保证。她如果要看，就能看见我写了什么；她不看，我也仍得按上面的事去做，不能等她监督才开始承担。"
    narrator "她抬头看向门口，我先看了她一眼，再看门。我们都听见外面的风，没有谁给出要离开的明确信号。我没有收拢她的物件，只把自己的笔记夹好，等她先把要带走的东西放到合适的位置。"
    narrator "我问：\"要把灯留着，还是先走？\""
    narrator "她把最上面的纸按平，随后朝门口走了一步。我看见这个动作，只把桌灯关到较暗的一档，没有把档案塞进抽屉。她选择先离开桌边，不表示她选择永远不再看；门还在，纸也还在，我要让以后重新回来仍然可能。"
    narrator "走到门边时，我回头确认桌面没有被我无意间收得像从没发生过。原页、摘要、责任纸和路线图仍能被分开辨认。这样的凌乱不漂亮，却比一张被我整理好的答案更接近我们确实经历过的顺序。"
    narrator "她的包带擦过门框，收据在里面轻轻响了一下。我没有伸手替她按住口袋。第一天她把那张纸折进自己的衣物里，之后又把昵称、硬币、票或卡放到自己选择的位置；我今天不能因为要谈真相和责任，就把那些普通物件重新变成我可以检查的证据。"
    narrator "楼道的灯比桌灯冷一些。我先让她走到灯下，再把门留出一条缝。她要回头，能看见屋里的纸；她要继续，也不会被我站在门中央挡住。我做不到把所有后果在今天修好，至少可以不让我的身体变成又一道替她安排的门。"
    narrator "我说：\"我写的事，从今天开始做。你不用先答应。\""
    narrator "她没有为这句话点头。我听见自己的声音落下后，便不再追加更多承诺。承诺的可信度不在于我说得多完整，而在于之后每一次遇到来源、路线、旧身份和她的停顿时，我是否真的按今天写下的方式停下来问。"
    narrator "走廊尽头的窗里映出湿漉漉的夜色。我记住这一晚不是因为终于得到一个结论，而是因为有些结论被拆开：她亲自看过什么、我承认什么、我还要做什么、她仍能保留什么。它们不能相互替代，正好也不能再被我用一句“为了她”统统包住。"
    narrator "她在台阶前停了一次，先确认包带没有被门框挂住，才往下走。我没有把手伸向她的包，也没有抢着去开更下面的灯。她自己迈出的那一阶很小，却比我替她许诺的所有远方都清楚；我只在她已经走出去以后跟上。"
    narrator "身后的门没有自动锁死，风仍能把它吹开一点。我没有回去把一切归档得整整齐齐。被交出的事实、还没被原谅的选择和已经写下的责任，都需要保留它们原本不舒服的边缘，才不会在我下一次害怕时又被改造成一个省略过来源的故事。"
    narrator "走廊的窗玻璃映出我手里的笔记本。我没有把它塞到看不见的口袋，只夹在自己能随时翻出的地方。上面写的是我要去处理的旧身份、要补上的来源、不能再让她替我挡的风险；每一项都是我的事，不需要她在旁边确认才成立。"
    narrator "绘梨衣走到下一盏灯下，先把包带从肩上拉好。她没有回头问档案会被谁看到，也没有把路线图交给我。我看见她继续保管自己的物件，便不拿我刚刚写下的责任纸去交换她对我更多的信任。"
    narrator "我想起第一天她把收据折好时，也没有让我替她解释我的名字。那张纸后来没有自动长成一个答案，正像今天的档案不会因为我终于交到灯下就自动修复。记住这些物件来自不同日子，是为了不再把它们混成只服务我一种解释的证据。"
    narrator "楼下传来有人开门的声音，我们都停了一下。她没有指向出口，我也没有替她把档案重新抱走。声音过去以后，门外仍旧安静；我只看见她先迈下一阶，便在她之后走。"
    narrator "我说：\"明天要核对哪一页，你选。\""
    narrator "她没有立刻回应。我把这句话留给以后，不在台阶上重新拿出纸。能重新选择阅读的速度，不是要她当场替我证明已经没事，而是让每一次她真正想看时，来源和我的责任都还摆在能被看见的位置。"
    narrator "夜风吹起她衣角，她自己压住。我没有伸手把她拉进我认为安全的方向。今天我能带走的是一份不完整但没有再被藏起来的记录，和必须兑现的几件具体事；她带走的是她选择留在自己身边的纸和路线。"
    narrator "我们下到一楼时，桌灯的光已经被楼板挡住。我没有把灯熄灭说成结束，也没有把她没有回头说成原谅。真相、修复和责任在今晚刚刚被摆开，之后还要在每一次真实行动里重新经得起看。"
    narrator "我把责任纸上的日期也记住。它不是一张让我暂时轻松的收据，而是从今晚起要被后来每一次行动核对的起点：旧身份的线索是否由我去收束，没交过的来源是否仍能由她看到，危险是否还会被我推到她面前。她不需要替这张纸作证，我也不能把它折回口袋就当作完成。"
    narrator "走出这层楼时，雨声已经停在远处。我没有把停雨说成事情结束，也没有把她没说话说成原谅。今晚只是把能放到灯下的东西放到灯下；以后它们会要求我用行动回应，而她仍可以在任何一次真正被问到时，给出或保留自己的答案。"
    return
