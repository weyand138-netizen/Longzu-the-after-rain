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
    scene bg safehouse_service_exit

    # scene_day6_safehouse_failure
    narrator "安全屋的门锁在雨停前先响了一次。屋内没人进来，走廊尽头却亮起本不该亮的灯。"
    narrator "绘梨衣把夹层里的纸和那张折过的纸逐一放在桌上，没有替任何一件说它一定能救谁。"
    $ event_safehouse_failed = True
    narrator "门外的声音只出现过一次，桌上的东西却因此都显出各自要承担的距离。"
    narrator "我清点一遍：手边的纸留着旧折痕，愿望纸也干了——它们都来自前几天的选择，越急越要分清手里究竟有什么。"
    narrator "她把手边的纸分开，摊平路线图，没有递来任何一件。我便收住手，先问：\"你要先带哪一个？\""
    show story erii_turn_exit
    narrator "她压住离自己最近的东西，看向门口。我把能看清的出口先告诉她：\"门口、维修门、楼梯，我现在只看见这三个。没有一个保证安全。\""
    narrator "她把路线图转了半圈，维修门的位置露出来，旁边还留着被划掉的支线。过去记过门，不等于今天就必须用门；它只让我们在失效时仍有一件可以重新面对的事实。"
    hide story
    if event_note_preserved_by_erii:
        narrator "她从袖口取出那张被雨打湿的愿望纸。纸边已经干了，字仍在。我把它放回她手边，没有拿来替换任何路线。"
        $ event_achievement_read_note_recovered = True
        $ cp_day6_note_recovery_complete = True
        narrator "她把纸边压平，仍让那行字停在自己的手边，没有把它变成谁都必须遵守的路线。"

    # scene_day6_backup_exit
    scene bg safehouse_exit_route_ready
    if has_unresolved_token("token_abandon_backup_plan"):
        narrator "先前被放弃的备选路线现在已经有了代价：门锁、走廊灯和桌上的地图都把那段空白留在眼前。"
        if resource_service_exit:
            $ critical_choice_interaction = True
            menu:
                "重新打开此前记住的维修通道，并承担暴露位置的风险":
                    $ apply_choice("day6_reopen_service_exit", {"preparation": 1})
                    narrator "我撕下那道旧封条，把维修门的位置和暴露的风险一并写到地图边。绘梨衣看完，自己把路线图折到那一页。"
                    narrator "封条裂开时灰尘落下，门后只有一段窄走廊和滴水声。我把门推到她也能看清的位置：\"门能开，但这里会留下我们来过的痕迹。\"她先确认夹层扣好才靠近门缝；我没有伸手拉她。"
                    narrator "她停在哪里，我就停在哪里；那点距离留给她自己，我只等她把脚步落到愿意落的地方。"
                    $ critical_choice_interaction = False

                "承认备选已经被放弃，不再留作可走路线":
                    $ apply_choice("day6_keep_backup_abandoned", {})
                    narrator "我没有去碰维修门的标记。绘梨衣把那处空白留在地图上，没有替我补成一条路。"
                    $ event_backup_stays_abandoned = True
                    narrator "那处空白像一块没有封好的门缝，提醒我和她它曾经可以被选择，却不再假装仍然可用。"
                    narrator "我没有用笔在空白上补一条虚线。封条、旧锁和记得的位置都还在，可我没有为今天留下真正能用的准备。把它画得像出口只会让她在需要决定时相信一份我不能兑现的安全。"
                    narrator "她把地图压平，空白没有消失。她没有替我画出门，也没有问我为什么当初放弃。我看见她把那块空白留着，便把笔放下；这不是一个舒服的选择，却是我不能再对她遮掉的事实。"
                    $ critical_choice_interaction = False
        else:
            $ critical_choice_interaction = True
            menu:
                "承认从未留下可重开的出口，继续面对这段缺口":
                    $ apply_choice("day6_keep_backup_abandoned", {})
                    narrator "我把没有出口的那一边留在桌上。绘梨衣没有把空白当作安全，也没有替我画出不存在的门。"
                    $ event_backup_stays_abandoned = True
                    narrator "没有出口的事实没有更好听的写法；她只把地图转回我和她都能看见的方向。"
                    $ critical_choice_interaction = False
    elif resource_service_exit:
        narrator "维修门的位置还在地图上。它不是突然出现的希望，只是此前被记下、现在仍能选择承担的路线。"
        $ critical_choice_interaction = True
        menu:
            "按已准备的计划启用维修通道，让她带着自己的票、卡或地图离开封锁区":
                $ apply_choice("day6_use_service_exit", {})
                narrator "我先打开维修门，再让她自己收好票、卡或地图。我们离开封锁区时，门后的灯没有替我们决定下一步。"
                $ event_service_exit_used = True
                $ cp_day6_service_exit_complete = True
                narrator "维修门合上时，留下的不是保证，只是我们都看见过的那段短暂通路。我让她先确认自己要带的东西都在手里才推门；她没把任何一件交给我，我站到门侧把通道留出来，等她自己决定什么时候跨过去。"
                narrator "门扣上前她回头看了一眼桌子——愿望纸、档案和铁盒都在各自的位置。我没有替她解释那一眼，只听见锁舌落回去，知道这一小段路已被走过，接下来还得继续选择。"
                $ critical_choice_interaction = False

            "把这条备选也留在封锁区，只走眼前没有准备的路":
                $ apply_choice("day6_abandon_backup", {})
                narrator "我把维修门的位置划出地图。绘梨衣看着那道划痕停了一会儿，随后把纸收回自己手边。"
                narrator "划痕留在纸上，像一条被主动放弃、却不能从记忆里擦掉的边界。"
                $ critical_choice_interaction = False

    if has_unresolved_token("token_withhold_family_truth"):
        narrator "这份被我省略过的来源，还欠她一个交代。安全屋失效以后，它不再是能藏住的事。"
        $ critical_choice_interaction = True
        menu:
            "交出此前省略的原始页，承认已经失去提前准备的时间":
                $ apply_choice("day6_disclose_withheld_archive", {"truth": 1})
                narrator "我把原始页摊在她面前，把来得太晚写在日期旁。绘梨衣逐行看完，没有替我把迟到圆成及时。"
                narrator "来源补回了，错过的准备时间却补不回。她停在一处被擦过的字旁，我只说我看不清；我们不拿更安全的结论盖住不知道。"
                narrator "门外的灯照到纸边，她把原页放回手边，我没有收走——以后这来源再被提起，她不必只听我复述。"
                $ critical_choice_interaction = False

            "继续只留下安全化结论，不让她核对原始页":
                $ apply_choice("day6_keep_archive_withheld", {})
                narrator "我没有把原始页拿出来。绘梨衣看着那份结论，手仍压在缺少来源的空白处。"
                $ event_family_truth_stays_withheld = True
                narrator "她没有撕掉结论，只让那处空白继续留在旁边。我把原页压在笔记下面，纸面上只剩整理过的几句话；她没有来掀，我也没把她的沉默当作愿意相信我。"
                narrator "省掉的东西没有因此消失，它仍在我这里，和这间失效的安全屋一样，成为后来必须面对的缺口。"
                $ critical_choice_interaction = False

    # scene_day6_cost_inventory
    narrator "桌上剩下必须由谁承担的代价：旧身份、被追到的风险，以及谁还能保留自己选的路线。"
    if event_shared_cost_promised:
        narrator "她把当初覆在我掌心上的手收回自己一边，等我先说明那句共同承担还算不算。"
    $ event_cost_bearer_requested = True
    narrator "绘梨衣把写着她名字的那一栏推开，没有替我接受任何把代价转给她的安排。"
    $ event_erii_rejects_shifted_cost = True
    narrator "我把笔停在半空，才看清桌面并没有一栏能替谁自动承担后果。铁盒、笔和路线图之间只隔一点桌面；那句“我会处理”却还不是谁已同意的安排。"
    narrator "旧身份凭据纸角被捏卷，照片、旧名字和那串数字都能让人查回来——烧掉它少一份证明，却不会让过去和追查一起消失。"
    narrator "路线图上她的名字写在另一侧，离铁盒很远；把代价往那边挪只需一笔，纸面甚至会显得更整齐。我握着笔才明白方便有多可怕：它会让一个我不想面对的后果，看起来像改一下位置就已解决。"
    narrator "她把那一栏推开，手指没碰我的笔，也没把铁盒推到火边。那是清楚的拒绝：她不接。至于她如何评价我，我不能从这一个动作里给自己找宽恕，也不能假装她没有表达。"
    narrator "旧照片上的脸仍看得清，它属于我，不属于她；无论怎么处理，都不能把过去转给她承担，也不能拿我的牺牲向她换回应。"
    narrator "她把离铁盒最近的一件先挪开，给自己的物件留出距离，我便没有把铁盒推回桌子中间——代价归谁、该离谁多远，都该由我控制的部分来决定。"
    narrator "走廊灯又闪了一次。安全屋已经失效，出口、卡片和我名字留下的风险都还在；我只是把它们一项项说清，让她在看得见的地方保管自己的东西。"
    narrator "我说：\"我先出去看门口。你要带什么，自己拿。\"她没有把东西递来，先检查夹层，再把手停到路线图上。我没有催——时间不能替我把她的手从纸上掰开。"
    narrator "她收好哪一件，我就记住哪一件，其余留在桌上。"
    $ critical_choice_interaction = True

    menu:
        "烧掉自己的旧身份凭据，把风险和后果写在自己名下":
            $ apply_choice("day6_burn_old_identity", {"sacrifice": 1})
            narrator "我把旧身份凭据烧在空铁盒里，再把要承担的联络、追踪和失去写到自己一栏。绘梨衣看完，把她的路线留在纸上。"
            $ event_shared_cost_acknowledged = True
            $ agency_day6_cost_outcome = "outcome_cost_borne_by_lu"
            if event_shared_cost_promised and "day6_shift_cost_to_erii" not in current_choice_history():
                $ event_prior_cost_promise_honored_without_shift = True
                $ cp_day6_direct_cost_complete = True
            narrator "火焰熄后，铁盒里只剩卷起的纸灰。我把盒盖合上，没有推给她。旧身份少了一份凭据，不等于追查也消失；我把还会发生的联络、失去证件的麻烦和要面对的人，写在自己一栏。"
            narrator "她没有给奖赏似的回应，只把路线留在另一侧，没让我的名字越过去。我看见那条界线仍在——承担不是把她拉进来一起看火，而是让我的代价待在自己名字下面。我说：\"这些由我处理。"
            narrator "你不需要替我签。\"她没有接笔，只把手放到自己的票、卡或地图上；我也没有从那动作里索取原谅，只把笔留在桌边，让她随时能看见我写了什么，也随时能拿着自己的东西离开。"
            $ critical_choice_interaction = False

        "把旧身份和追踪的代价写到她的路线与名字上":
            $ apply_choice("day6_shift_cost_to_erii", {})
            narrator "我把需要付出的代价移到她的路线旁。纸没有变轻，只是她的名字被写进了原本不属于她的那一栏。"
            $ event_shifted_cost_consequence_visible = True
            $ agency_day6_cost_outcome = "outcome_cost_shifted_to_erii"
            narrator "那道笔画没有让纸面变轻，只让我和她都更清楚它是谁写下的。铁盒、证件和我能处理的联络都还在手边，我却把最难看的部分挪到她的路线旁——这件事连我自己也无法再装作没看见。"
            $ critical_choice_interaction = False

            narrator "她把那一栏推回我面前，再一次摇头。被写下的后果已经摆在我和她之间，不能靠沉默消失。"
            $ event_cost_reconsideration_requested = True
            $ event_erii_rejects_shifted_cost_again = True
            $ critical_choice_interaction = True
            menu:
                "收回已经转嫁的代价，烧掉自己的旧身份并承认这次伤害仍会留下痕迹":
                    $ apply_choice("day6_take_cost_back", {"sacrifice": 1})
                    narrator "我划掉她名字旁的安排，烧掉自己的旧身份凭据，也没有划掉先前写过的那一笔。绘梨衣看着那道痕迹，才把路线重新放回桌上。"
                    $ event_shared_cost_acknowledged = True
                    $ cp_day6_cost_reconsideration_complete = True
                    $ agency_day6_cost_reconsideration_outcome = "outcome_cost_returned_to_lu"
                    narrator "划回自己名下以后，先前那道越界的笔画仍在纸上，不能被当作没有发生——伤害留下的痕迹，我承认它还在。"
                    $ critical_choice_interaction = False

                "维持由她承担的安排，把已经显出的后果留给她":
                    $ apply_choice("day6_leave_cost_shifted", {})
                    narrator "我没有划掉那一栏。绘梨衣把纸翻到背面，留下没有被共同承担的正面。"
                    $ event_shifted_cost_confirmed = True
                    $ agency_day6_cost_reconsideration_outcome = "outcome_cost_shift_confirmed"
                    narrator "纸翻到背面，代价却没有跟着翻过去；她留下的沉默，成了桌面上最重的一项。"
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
    narrator "我重新核对她留下的票据或记录——路不是从我的愿望里长出来的，而是从她拿过、留下或推开的物件里暂时显出形状。"
    narrator "\"我们怎么办\"不能只由我回答。门外的灯没有催我选路，却提醒我手里的路线不能都当作用得上的。我把手从桌面移开，给她留出拿起、收好或放下的空间。"
    narrator "我问：\"这件，你还要带着吗？\"她的手指在卡、票或地图上停了一会儿，再把东西收好或留在桌面。我等她做完，才说门外的时间、出口和自己的安排——至少这次没有替她答应。"

    if agency_day6_commitment_state == "independent_contact":
        narrator "她把联系人卡和风险说明收进自己的夹层，手没有离开卡边。"
        $ critical_choice_interaction = True
        menu:
            "确认由她独立保管联系人与风险说明，按她已经收好的方案离开":
                $ apply_choice("day6_commit_independent_contact", {})
                narrator "我没有再替她拿卡，只把安全屋外的时间和位置写给她看。她收好卡，先走到门边。"
                $ event_independent_route_committed = True
                narrator "门边的光先落在她手里的卡上，随后才照到我还没收起的纸。我写下会合点和下次确认时间，把纸放到她看得见的位置——卡没交给我，风险说明也没被我折起。"
                narrator "我没有问她会不会联系，也不从她收好卡的动作里替自己读出一条线；卡在她手里意味着她能决定是否使用，我能做的只是把自己该处理的追踪和旧身份写清，别让那部分再压到她的选择上。"
                narrator "她走到门边停了一下，回头看我写下的时间，没有点头，我也没有追加承诺；门外的光照着卡片边缘，我站在原地，等她先跨过那道门。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "shared_escape":
        narrator "她把两张票并排放在路线图上，又把其中一张留在自己手边。"
        $ critical_choice_interaction = True
        menu:
            "确认两张票和共同路线，由两人一起承担已经写下的代价":
                $ apply_choice("day6_commit_shared_escape", {})
                narrator "我把自己的票放在她那张旁边，没有替她收走路线图。她确认站名后，才把两张票一起放进夹层。"
                $ event_shared_route_committed = True
                narrator "两张票贴在一起，却没有把各自要承担的那段路变成同一张纸。她先看站名再看座位号，票面上的名字仍分开；我没有抽走她的路线图，也没让我的票盖住她那张。"
                narrator "同行只能建立在她留住的那张票和我自己承担的代价上。我说：\"我的名字留下的风险，我自己处理。票怎么用，到站再看。\"她把两张票放进同一夹层，却把路线图留在外面——没有交给我。"
                narrator "门锁又响了一声，我们没有因此把票攥成保证书，只是在她确认站名后，一起往已经看见的出口走。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "solo_departure":
        narrator "她把单人票放进自己的证件夹，联系人卡的位置仍是空的。"
        $ critical_choice_interaction = True
        menu:
            "确认她独自持票离开，这条路线不附带持续联系的承诺":
                $ apply_choice("day6_commit_solo_departure", {})
                narrator "我没有替她补上一张联系人卡。她收好单人票，自己把证件夹扣上。"
                $ event_solo_route_committed = True
                $ event_no_continuing_contact_commitment = True
                narrator "证件夹扣上的声音很轻，空着的联系人位置却让这条路显得格外清楚。"
                narrator "我把能走的出口和列车时间写在另一张纸上，放到她证件夹旁。纸上没有我的号码，也没有一句要她到站后联络。她看完后把单人票压住，纸还留在桌上。我没有把它塞进她口袋。"
                narrator "我说：\"票是你的。门口在那边。\""
                narrator "她没有回答，只把证件夹合紧。那是她能自己带走的东西。我退到门侧，让通道露出来。没有联系人卡的空位仍旧空着，我没有把自己的不舍变成要她带上的联系。"
                narrator "她走向门口时，我没有伸手去拉住她。失效的安全屋、铁盒和路线图都留在身后；她带走的只是她自己的票和能由她执行的方向。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "old_order_return":
        narrator "旧秩序的路线纸被放在桌上，压住了她先前自己收好的票、卡或地图。"
        $ critical_choice_interaction = True
        menu:
            "确认旧秩序方案压过了她的回答，但那不是她选的":
                $ apply_choice("day6_commit_old_order_return", {})
                narrator "我把旧路线带离桌面，却没有说那是她同意的事。绘梨衣没有伸手去拿那张被压住的纸。"
                $ event_old_order_route_committed = True
                narrator "被压住的纸没被撕开，旧秩序仍在场，却不再冒充她的回答。旧纸压得很平，连折痕都像被提前抚过——它遮住了票、卡或地图，而她没有伸手掀开。"
                narrator "她没有伸手，不等于同意；我反而更清楚，是自己把她放到了必须越过我的安排、才能重新碰到自己物件的位置。门外的灯照进来，我没有再用“安全”给这张纸找一个让人好受的名字。"
                narrator "她站在原处，手离被压住的东西很远；我知道走出去也抹不掉这段距离，旧路线会继续带来后果，而我只能承认那后果不是由她选择的。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "no_executable_route":
        narrator "手边没有一项能被诚实地叫作可执行路线。绘梨衣把空白留在我和她之间。"
        $ critical_choice_interaction = True
        menu:
            "承认现在没有可执行路线，把空白留在地图上":
                $ apply_choice("day6_no_executable_route", {})
                narrator "我没有替她补上答案。我和她把空白留在地图上，先离开这间已经失效的安全屋。"
                $ event_route_collapse = True
                narrator "离开时那张空白地图没有被带走，像一件不能执行却必须记住的东西。我把手边的东西又数了一遍，没有一件能诚实地指向现在能走的路——这样说出来很难，也不能让门外的人消失。"
                narrator "绘梨衣把空白留在桌上，我没有用笔画一条虚线安慰她。"
                narrator "我说：\"现在没有。我不会说有。\"她没有给我新的方向，只把袖口里的纸按住。"
                narrator "我们离开时，我先让她走过门口，再把灯关掉；空白地图留在桌上，提醒我不是所有缺口都能在最后一分钟被当作准备好了。"
                narrator "走廊很暗，出口仍在那里——没有路线不等于她已经把决定交给我，我只是走在能看见的地方，等下一件真实发生的事出现。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "undetermined":
        narrator "票、卡和地图的记录对不上，我没有把任何一张纸推成她的答案。"

    narrator "离开前，我又看了眼桌面：铁盒扣好，水杯还在窗边，灯照着路线图的折痕。这里不再是能藏身的地方，只是一间门锁响过、灯光异常的屋子。"
    narrator "她检查夹层，按住最先保留的物件，可能是票、卡，也可能只是一张纸；我没要求翻开，只记住写在名字下的责任。"
    show story erii_turn_exit
    narrator "我把门把轻轻按下，先听走廊里有没有脚步。没有声音不等于没有人，只是我此刻没听见。我把这点说出来：\"外面暂时安静。\"我没有说安全，也没有说已经没人。"
    narrator "她听见后看向门口，没有把手里的东西交给我。"
    narrator "我说：\"我先走半步。你要停，我就停。\"她先看门口，再把夹层按紧一点；我等她从桌边离开，才推开门。"
    narrator "她走在我前面或后面，都不让我有权替她说自己选了什么——我只在她停下时停下，在她走动时让出能通过的地方。"
    show story lu_hold_safehouse_door
    narrator "门在身后合上时没有很大声音。安全屋里的纸、灰和水杯被关在里面，前几天留下的物件却还在我们手中：票可能带来实名痕迹，卡可能带来被联系的风险，空白地图则提醒我没有准备过什么。"
    narrator "票面、卡片说明或地图上的空白，她已经看过；我没再重复，只说明自己会处理的部分——旧身份、追踪线索和联络，其余仍由她保留。"
    hide story
    scene bg residential_stairwell_night
    narrator "走到楼梯口时，风从破开的窗缝钻进来。她停下来把纸角压平，我站在旁边等。没有人追来，也没有奇迹替我们解决门锁和档案。"
    narrator "只有她把纸收好、我没有抢过去的这一小段时间，真实地留在楼梯的冷风里。"
    narrator "楼梯的应急灯忽明忽暗，把她握住的夹层照出一条窄边。我没有问里面是哪张票、哪张卡或哪一页纸；今晚我已经数过能走的出口和要承担的代价，数清并不赋予我翻开她手里东西的权利。"
    narrator "我们同下一步步往下，脚步落在湿冷台阶上，间隔没有被我强行缩短。"
    narrator "走到一楼，风从门缝吹进来，带着雨后水泥地的味道。她停在门内侧，没有立刻拉门；我也停下，没有把门把先压下去。外面是下一步，不是我替她抢下的答案。"
    narrator "我把门只推开一掌宽，站在侧边，让她自己看见外面的路；她没有把夹层交给我，我也没有去碰。跨不跨过去，仍由她决定。"
    scene bg residential_street_after_rain_night
    narrator "门在身后缓缓合上，安全屋最后留给我的只是一声很轻的碰响。我没有回头确认铁盒、纸和水杯是否还在原位——那些会在之后构成后果，而此刻她已在门外站稳。"
    narrator "把注意力放回她已经走出的这一步，比回头检查我的布置更重要。"
    narrator "街上的风把她衣角吹起，她自己压住。我没有说我们总能找到下一处地方，也没有用一段未来的保证覆盖现在仍可见的风险。"
    narrator "今晚的出口只是出口；她手里保住的物件、我写下的代价和还没解决的事，会跟着我们进入下一天。代价正在由我承担，选择仍在她手里，我们只把脚步放到下一段能看见的路上。"
    return
