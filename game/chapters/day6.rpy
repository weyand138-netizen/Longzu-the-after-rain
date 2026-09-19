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
    narrator "安全屋的门锁在雨停前先响了一次。我听见屋内没有人进来，走廊尽头却亮起了本不该亮的灯。"
    narrator "绘梨衣把票、卡、路线图和那张折过的纸逐一放在桌上，没有替任何一件东西说它一定能救谁。"
    $ event_safehouse_failed = True
    narrator "门外的声音只出现了一次，桌上的东西却因此都显出各自要承担的距离。"
    narrator "我先看门缝，再看桌面。灯光把票边、卡片和路线图的折痕照得太清楚；没有任何一件东西自己开口告诉我该带走什么、该交给谁。"
    narrator "门锁响过，屋里却没变：水杯在窗沿，外套在椅背，铁盒还开着。没人闯入，本该熄灭的走廊灯却从门缝照进来。我没看见谁动过开关，更不能放心。"
    narrator "我清点桌上的东西：票边干着，卡在夹层，路线图还留着旧折痕，愿望纸也干了。它们来自前几天的选择。越是着急，越要分清手里究竟有什么。"
    narrator "她把票和卡分开，摊平路线图，没有递来任何一件。我便收住手，没往自己的包里装。门外的动静再急，也得先问她。"
    narrator "我问：\"你要先带哪一个？\""
    narrator "她压住离自己最近的东西，看向门口。票还没递来，路线也没指出。我先把能看清的出口告诉她，等她收好手边的物件。"
    narrator "我低声说：\"门口、维修门、楼梯，我现在只看见这三个。没有一个保证安全。\""
    narrator "她听完，把路线图向我转了半圈。纸上曾经写过的维修门位置露出来，旁边也留着被划掉的支线。我把视线停在那儿，没有马上伸手按住它。过去记过门，不等于今天就必须用门；它只让我们在失效时仍有一件可以重新面对的事实。"
    if event_note_preserved_by_erii:
        narrator "她从袖口取出那张被雨打湿的愿望纸。纸边已经干了，字仍在。我把它放回她手边，没有拿来替换任何路线。"
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
                    narrator "我撕下那道旧封条，把维修门的位置和暴露的风险一并写到地图边。绘梨衣看完，自己把路线图折到那一页。"
                    narrator "被重新打开的门没有抹掉先前放弃它的痕迹，地图上两道线仍然并排存在。"
                    narrator "封条裂开时，灰尘从门缝里落下来。门后没有灯，只有一段窄走廊和我能听见的滴水声。我先把门推到她也能看清里面的位置，告诉她：\"门能开，但这里会留下我们来过的痕迹。\""
                    narrator "她没有把票、卡或地图交给我，只把路线图折到门的编号旁。她先确认夹层扣好，才靠近门缝。我站在一侧，不用身体挡住她回到桌边的路。维修门能不能走是一件事，谁带着自己的东西走又是另一件事。"
                    narrator "她往门后看了一会儿，没有立刻跨进去。我没有把停住说成拒绝，也不伸手拉她。走廊里的水声、门外的灯和地图上的风险都在眼前；我只等她先让脚步落到她愿意落的地方。"
                    $ critical_choice_interaction = False

                "承认备选已经被放弃，继续不把它伪装成还能使用":
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
                    narrator "我把没有出口的那一边留在桌上。绘梨衣没有把空白说成安全，也没有替我画出不存在的门。"
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
                narrator "维修门合上时，留下的不是保证，而是我和她都看见过的那段短暂通路。"
                narrator "我让她先确认票、卡和路线图都在自己手里，才把门推开。她没有把任何一件交给我保管。我站到门侧，把通道留出来，等她自己选择什么时候跨过去。"
                narrator "门后的灯闪了一次，她先看脚下，再看我写在地图边的时间。我没有把手伸到她背后催她走。她迈过门槛以后我才跟上；这不是谁带谁逃离，只是同一条先前准备过的通道被依次走过。"
                narrator "门扣上前，她回头看了一眼桌子。愿望纸、档案和铁盒都已经在各自的位置。我没有替她解释那一眼，只听见锁舌落回去，知道这一小段路已经被走过，接下来还得继续选择。"
                $ critical_choice_interaction = False

            "把这条备选也留在封锁区，只走眼前没有准备的路":
                $ apply_choice("day6_abandon_backup", {})
                narrator "我把维修门的位置划出地图。绘梨衣看着那道划痕停了一会儿，随后把纸收回自己手边。"
                narrator "划痕留在纸上，像一条被主动放弃、却不能从记忆里擦掉的边界。"
                $ critical_choice_interaction = False

    if has_unresolved_token("token_withhold_family_truth"):
        narrator "安全屋失效的后果已经落到桌上：少掉的原始页让路线图只能写下更安全的结论，却少了一段不能核对的来处。"
        $ critical_choice_interaction = True
        menu:
            "交出此前省略的原始页，承认已经失去提前准备的时间":
                $ apply_choice("day6_disclose_withheld_archive", {"truth": 1})
                narrator "我把原始页摊在她面前，也把来得太晚写在日期旁。绘梨衣逐行看完后，没有替我把迟到说成及时。"
                narrator "迟到的纸页补回了来源，却没有把已经错过的准备时间一并补回。"
                narrator "原始页摊在安全屋的桌上，和第五天灯下的纸一样有潮软的边。绘梨衣先看日期，再看我写在旁边的迟到。她没有把纸推回，也没有替我把那两个字划掉。我知道来源现在能被她自己核对，来晚的事实也一样能被她看见。"
                narrator "我没有把她逐行阅读当成已经原谅。她停在一处被擦过的字旁，我只说我看不清。她没有逼我猜，也没有接过我的笔。我们把不知道留在纸上，不再拿更安全的结论盖住它。"
                narrator "门外的灯照到原页边缘，她把纸放回自己手边。我没有收走。以后若这份来源又被提起，她不必只听我复述；我也不能再说我替她保管是为了她好。"
                $ critical_choice_interaction = False

            "继续只留下安全化结论，不让她核对原始页":
                $ apply_choice("day6_keep_archive_withheld", {})
                narrator "我没有把原始页拿出来。绘梨衣只看着那份结论，手仍压在缺少来源的空白处。"
                $ event_family_truth_stays_withheld = True
                narrator "她没有把那份结论撕掉，只让缺少来源的空白继续留在它旁边。"
                narrator "我把原始页留在自己的笔记下面，纸面上只剩整理过的几句话。绘梨衣看见结论，也看见它旁边没有可翻开的来源。她没有来掀我的笔记，我也不把她没有来掀说成她愿意相信我。"
                narrator "她把结论折了一下又展开，像是在确认纸上没有更多内容。我听见折痕压过纸面的声音，知道我省掉的东西并没有因此从房间里消失。它仍在我这里，和这间失效的安全屋一样，成为后来必须面对的缺口。"
                narrator "我没有再说时间不够。时间确实不够，却不是让我继续扣住来源的许可。她把纸留在桌上，我把笔记留在自己手边；两件东西之间的距离，说明我还没有交出什么。"
                $ critical_choice_interaction = False

    # scene_day6_cost_inventory
    narrator "桌上剩下的是必须由谁承担的代价：旧身份、被追到的风险，以及谁还能保留自己选的路线。"
    if event_shared_cost_promised:
        narrator "她把当初覆在我掌心上的手收回到自己一边，等我先说明那句共同承担还算不算。"
    $ event_cost_bearer_requested = True
    narrator "绘梨衣把写着她名字的那一栏推开，没有替我接受任何把代价转给她的安排。"
    $ event_erii_rejects_shifted_cost = True
    narrator "我把笔停在半空，第一次看清桌面上并没有一栏可以替谁自动承担后果。"
    narrator "铁盒、笔和路线图之间只隔着一点桌面。我可以看见她把名字推开，也可以看见自己仍握着笔；我不能把“我会处理”当成已经由谁同意的安排。"
    narrator "旧身份凭据放在铁盒旁，纸角被捏卷了。照片、旧名字和那串数字，都能让人查回来。烧掉它，会少一份身份证明，却不会让过去和追查一起消失。"
    narrator "路线图上她的名字写在另一侧，离铁盒很远。把代价往那边挪，只需要一笔，纸面上甚至会显得更整齐。我握着笔时才明白方便有多可怕：它会让一个我不想面对的后果，看起来像是只要改一下位置就已经被解决。"
    narrator "绘梨衣把那一栏推开，手指没有碰到我的笔。她没有替我写一句责备，也没有把铁盒推到火边。我看见的是清楚的拒绝：她不接那一栏。至于她此刻如何评价我，我不能从这一个动作里给自己找宽恕，也不能假装她没有表达。"
    narrator "我说：\"这是我的旧名字。跟着它来的事，也该先写在我这里。\""
    narrator "她看完铁盒，又望向路线图，没有伸手帮我点火。我把笔移回自己的名字下，逐条写下要联系谁、怎样拖住追踪，以及失去证件后怎么办。"
    narrator "火柴划过盒盖时，声音很轻。纸边先卷起来，照片上的脸在火光里变黑。我没有移开视线，也没有去看她是否愿意看。空气里有一股焦糊味，提醒我这不是一句说完就能撤销的承诺。"
    narrator "火光映在路线图上，纸面的折痕一明一暗。我把铁盒放到远离她物件的一边，免得灰落到票和卡上。这个动作不会使已经写下的代价变轻，却至少不再让我的旧身份和她的路线混在同一块桌面上。"
    narrator "绘梨衣看着铁盒，没有伸手来关盖。我等火彻底熄掉，才把水杯移近。她没有要我这么做，也没有反对。我没有把递水说成她接受了这段燃烧，只把可能烫到纸的东西移开，留出她可以自己离桌的空间。"
    narrator "我问：\"烟太大吗？\""
    narrator "她把袖口抬到鼻子前，又把袖口放下。她没有点头，也没有摇头。我把窗推开一条缝，站到另一侧。风把焦味带走一些，也把路线图边缘吹起来。她自己按住纸角，我没有替她拿走。"
    narrator "桌上的旧照片已经卷黑，照片上的脸看不清了。可我记得照片属于我，不属于她。烧掉凭据不是把过去转给她承担的理由，也不是要她看着我牺牲来换一个回应。我把铁盒盖好，只在自己笔记上写下下一步。"
    narrator "她把票、卡或地图重新排好，先把离铁盒最近的一样挪开。她没有说原因。我看见她给自己的物件留出距离，便没有把铁盒推回桌子中间。代价归谁，连同它该离谁多远，都应当在我能控制的部分由我处理。"
    narrator "走廊灯又闪了一次，门锁没有再响。我没有把短暂安静说成危险已经过去。安全屋已经失效，出口的风险、卡片的风险和我名字留下的风险都还在；我只是把它们一项项说清，让她能在看得见的地方保管她自己的东西。"
    narrator "我说：\"我先出去看门口。你要带什么，自己拿。\""
    narrator "她没有把东西递给我。她先检查夹层，再把手停到路线图上。我没有催。门外的时间还在走，可时间不能替我把她的手从纸上掰开。她收好哪一件，我就记住哪一件，其他仍然留在桌上。"
    $ critical_choice_interaction = True

    menu:
        "烧掉自己的旧身份凭据，把风险和后果写在自己名下":
            $ apply_choice("day6_burn_old_identity", {"sacrifice": 1})
            narrator "我把旧身份凭据烧在空铁盒里，再把要承担的联络、追踪和失去写到自己一栏。绘梨衣看完后，把她的路线留在纸上。"
            $ event_shared_cost_acknowledged = True
            $ agency_day6_cost_outcome = "outcome_cost_borne_by_lu"
            if event_shared_cost_promised and "day6_shift_cost_to_erii" not in current_choice_history():
                $ event_prior_cost_promise_honored_without_shift = True
                $ cp_day6_direct_cost_complete = True
            narrator "火焰熄下去以后，铁盒里只剩卷起的纸灰。我把盒盖合上，没有把它推给绘梨衣。旧身份少了一份凭据，并不等于追查也跟着消失；我把还会发生的联络、失去证件后的麻烦和需要面对的人写在自己一栏。"
            narrator "她看着纸上的步骤，没有给我任何奖赏似的回应。她只是把自己的路线留在另一侧，没有让我的名字越过去。我看见那条界线仍然在，才知道承担不是把她拉进来一起看火，而是让自己的代价待在自己的名字下面。"
            narrator "我说：\"这些由我处理。你不需要替我签。\""
            narrator "她没有接笔。她把手放到自己的票、卡或地图上。我没有从这个动作里索取原谅，只把笔留在桌边，确认她随时能看见我写下了什么，也随时能拿着自己的东西离开。"
            $ critical_choice_interaction = False

        "把旧身份和追踪的代价写到她的路线与名字上":
            $ apply_choice("day6_shift_cost_to_erii", {})
            narrator "我把需要付出的代价移到她的路线旁。纸张没有变轻，只是她的名字被写进了原本不属于她的那一栏。"
            $ event_shifted_cost_consequence_visible = True
            $ agency_day6_cost_outcome = "outcome_cost_shifted_to_erii"
            narrator "那道被移过去的笔画没有让纸面变轻，只让我和她都更清楚它是谁写下的。"
            narrator "笔尖离开纸面后，我先看见的是她名字旁边那一小段新字。它没有因为写得整齐就变得合理。铁盒、证件和我能处理的联络都还在我手边，我却把最难看的部分挪到她的路线旁；这件事连我自己也无法再装作没看见。"
            $ critical_choice_interaction = False

            narrator "她把那一栏推回我面前，再一次摇头。被写下的后果已经摆在我和她之间，不能靠沉默消失。"
            $ event_cost_reconsideration_requested = True
            $ event_erii_rejects_shifted_cost_again = True
            $ critical_choice_interaction = True
            menu:
                "收回已经转嫁的代价，烧掉自己的旧身份并承认这次伤害仍会留下痕迹":
                    $ apply_choice("day6_take_cost_back", {"sacrifice": 1})
                    narrator "我划掉她名字旁的安排，烧掉自己的旧身份凭据，也没有划掉先前写过那一笔。绘梨衣看着那道痕迹，才把路线重新放回桌上。"
                    $ event_shared_cost_acknowledged = True
                    $ cp_day6_cost_reconsideration_complete = True
                    $ agency_day6_cost_reconsideration_outcome = "outcome_cost_returned_to_lu"
                    narrator "划回自己名下以后，先前那道越界的笔画仍在纸上，不能被当作没有发生。"
                    $ critical_choice_interaction = False

                "维持由她承担的安排，把已经显出的后果留给她":
                    $ apply_choice("day6_leave_cost_shifted", {})
                    narrator "我没有划掉那一栏。绘梨衣把纸翻到背面，留下没有被共同承担的正面。"
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
    narrator "我把桌面重新看了一遍。联系人卡的边没有弯，两张票仍能读到座位号，单人票的日期没有改，空路线图也依旧空着。路不是从我的愿望里长出来的，而是从这些已经被她拿过、留下或推开的物件里暂时显出形状。"
    narrator "“我们怎么办”不能只由我回答。她握着卡、把票留在夹层，或只留下空纸，指向的是不同处境。我得照眼前的事实行动，也承担各自的代价。"
    narrator "门外的灯仍亮着。它没有催我选择哪条路线，却提醒我不能把所有路线同时说成可用。我把手从桌面移开，给她留出拿起、收好或放下东西的空间。她先做出的动作不是给我安慰，而是我们接下来必须如实面对的条件。"
    narrator "我问：\"这件，你还要带着吗？\""
    narrator "她的手指在卡、票或地图上停了一会儿，再把东西收好，或留在桌面。我等她做完，才说门外的时间、出口和自己的安排。至少这次没有替她答应。"

    if agency_day6_commitment_state == "independent_contact":
        narrator "她把联系人卡和风险说明收进自己的夹层，手没有离开卡边。"
        $ critical_choice_interaction = True
        menu:
            "确认由她独立保管联系人与风险说明，按她已经收好的方案离开":
                $ apply_choice("day6_commit_independent_contact", {})
                narrator "我没有再替她拿卡，只把安全屋外的时间和位置写给她看。她收好卡，先走到门边。"
                $ event_independent_route_committed = True
                narrator "门边的光先落在她手里的卡上，随后才照到我还没收起的纸。"
                narrator "我写下门外会合点和下一次能够确认时间的方式，把纸放到她看得见的位置。联系人卡没有交给我，风险说明也没有被我折起来。她先把卡按进夹层，才把纸拿走。"
                narrator "我没有问她会不会联系，也没有把她收好卡的动作说成我得到了一条线。卡在她手里意味着她能决定是否使用；我能做的是把自己该处理的追踪和旧身份写清，别让那部分再压到她的选择上。"
                narrator "她走到门边后停了一下，回头看我写下的时间。她没有点头，我也没有追加承诺。门外的光照着卡片边缘，我站在原地，等她先跨过那道门。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "shared_escape":
        narrator "她把两张票并排放在路线图上，又把其中一张留在自己手边。"
        $ critical_choice_interaction = True
        menu:
            "确认两张票和共同路线，由两人一起承担已经写下的代价":
                $ apply_choice("day6_commit_shared_escape", {})
                narrator "我把自己的票放在她那张旁边，没有替她收走路线图。她确认站名后，才把两张票一起放进夹层。"
                $ event_shared_route_committed = True
                narrator "两张票贴在一起，却没有把各自要承担的那一段路变成同一张纸。"
                narrator "她先看站名，再看两张座位号。票靠在一起，票面上的名字却仍然分开。我没有把路线图从她手里抽出来，也没有让我的票盖住她那张。同行只能建立在她已经留住的那张票和我自己承担的代价上，不能把其中一张吞进另一张。"
                narrator "我说：\"我的名字留下的风险，我自己处理。票怎么用，我们到站再看。\""
                narrator "她把两张票放进同一个夹层，却把路线图留在外面。她没有把图交给我。我看见她还要看路线，便把门边的位置让出来，等她自己收好最后一角。"
                narrator "门锁又响了一声，走廊灯没有灭。我们没有因此把票攥成一张保证书，只是在她确认站名以后，一起往已经看见的出口走。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "solo_departure":
        narrator "她把单人票放进自己的证件夹，联系人卡的位置仍是空的。"
        $ critical_choice_interaction = True
        menu:
            "确认她独自持票离开，并不把持续联系承诺塞进这条路线":
                $ apply_choice("day6_commit_solo_departure", {})
                narrator "我没有替她补上一张联系人卡。她收好单人票，自己把证件夹扣上。"
                $ event_solo_route_committed = True
                $ event_no_continuing_contact_commitment = True
                narrator "证件夹扣上的声音很轻，空着的联系人位置却让这条路显得格外清楚。"
                narrator "我把能走的出口和列车时间写在另一张纸上，放到她证件夹旁。纸上没有我的号码，也没有一句要她到站后联络。她看完后把单人票压住，纸还留在桌上。我没有把它塞进她口袋。"
                narrator "我说：\"票是你的。门口在那边。\""
                narrator "她没有回答，只把证件夹合紧。那是她能自己带走的东西。我退到门侧，让通道露出来。没有联系人卡的空位仍旧空着，我不把自己的不舍写成她必须带上的联系。"
                narrator "她走向门口时，我没有伸手去拉住她。失效的安全屋、铁盒和路线图都留在身后；她带走的只是她自己的票和能由她执行的方向。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "old_order_return":
        narrator "旧秩序的路线纸被放在桌上，压住了她先前自己收好的票、卡或地图。"
        $ critical_choice_interaction = True
        menu:
            "确认那份旧秩序方案已经取代她的回答，不把它称作她的选择":
                $ apply_choice("day6_commit_old_order_return", {})
                narrator "我把旧路线带离桌面，却没有说那是她同意的事。绘梨衣没有伸手去拿那张被压住的纸。"
                $ event_old_order_route_committed = True
                narrator "被压住的纸没有被撕开，旧秩序因此仍在场，却不再冒充她的回答。"
                narrator "旧路线的纸压得很平，连折痕都像被提前抚过。我看见它遮住了票、卡或地图，也看见绘梨衣没有伸手去掀开。我没有把她没有伸手当成她同意，反而更清楚自己把她放到了必须越过我安排才能重新碰到自己的位置。"
                narrator "我把旧纸放到桌边，仍没有交到她手里。它现在是我选择维持的秩序，不是她说出的方向。门外的灯照进来，我没有再用“安全”给这张纸找一个让人好受的名字。"
                narrator "她站在原处，手离被压住的东西很远。我知道接下来走出去也不能抹掉这段距离。旧路线会继续带来后果，而我只能承认后果不是由她选择的。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "no_executable_route":
        narrator "票、卡和地图之间没有一项能被诚实地叫作可执行路线。绘梨衣把空白留在我和她之间。"
        $ critical_choice_interaction = True
        menu:
            "承认现在没有可执行路线，不把空白伪装成她已经答应的方向":
                $ apply_choice("day6_no_executable_route", {})
                narrator "我没有替她补上答案。我和她把空白留在地图上，先离开这间已经失效的安全屋。"
                $ event_route_collapse = True
                narrator "离开时那张空白地图没有被带走，像一件不能执行却必须记住的东西。"
                narrator "我把票、卡和路线图又数了一遍，没有一件能诚实地指向一条现在能走的路。这样说出来很难，也不能让门外的人消失。绘梨衣把空白留在桌上，我没有用自己的笔画出一条虚线安慰她。"
                narrator "我说：\"现在没有。我不会说有。\""
                narrator "她没有给我新的方向，只把袖口里的纸按住。我们离开时，我先让她走过门口，再把灯关掉。空白地图留在桌上，提醒我不是所有缺口都能在最后一分钟被说成准备好了。"
                narrator "走廊很暗，出口仍然在那里。没有路线不等于她已经把决定交给我；我只是走在能看见的地方，等下一件真实发生的事出现。"
                $ critical_choice_interaction = False
    elif agency_day6_commitment_state == "undetermined":
        narrator "票、卡和地图的记录对不上，我没有把任何一张纸推成她的答案。"

    narrator "离开前，我又看了眼桌面：铁盒扣好了，水杯还在窗边，灯照着路线图的折痕。这里不再是能安心藏身的地方，只是一间门锁响过、灯光异常的屋子。"
    narrator "她检查夹层，按住最先保留的物件，可能是票、卡，也可能只是一张纸。我没要求翻开。她收好自己的东西，我记住写在名字下的责任。"
    narrator "我把门把轻轻按下，先听走廊里有没有脚步。没有声音并不等于没有人，只有我此刻没有听见。我把这点说出来：\"外面暂时安静。\"我没有说安全，也没有说已经没人。她听见后看向门口，没有把手里的东西交给我。"
    narrator "走廊灯在地板上拉出一条线。走就得经过，停就还留在门锁被注意到的房间。两边都有风险，不会因为我替它们取个好听的说法而减少。"
    narrator "我说：\"我先走半步。你要停，我就停。\""
    narrator "她没有回答完整的句子。她先看门口，再把夹层按紧一点。我等她从桌边离开，才推开门。她走在我后面或前面，都不会让我有权替她说自己选了什么；我只能在她停下时也停下，在她走动时让出能通过的地方。"
    narrator "门在身后合上时没有发出很大声音。安全屋里的纸、灰和水杯被关在里面，前几天留下的物件却还在我们手中。它们不再是装饰在路线上的道具：票可能带来实名的痕迹，卡可能带来被联系的风险，空白地图则提醒我没有准备过什么。"
    narrator "票面、卡片说明或地图上的空白，她已经看过。我没再重复，只说明自己会处理的部分：旧身份、追踪线索和联络。其余仍由她保留。"
    narrator "走到楼梯口时，风从破开的窗缝钻进来。她停下来把纸角压平，我站在旁边等。没有人追来，也没有奇迹替我们解决门锁和档案。只有她把纸收好、我没有抢过去的这一小段时间，真实地留在楼梯的冷风里。"
    narrator "我想起站台上的共同承担。走到这里，才知道不是把东西全攥在一起。我处理自己造成的风险，她保留自己的票、卡、名字和路线。"
    narrator "我走到门边，让她看清出口、走廊转角和闪动的灯。她若望向别处，我会先停下问，不再说一句“我来处理”就把她挡在身后。"
    narrator "楼梯下方传来一声水管滴落的响。我没有把它当成脚步。她没有因为声音抓住我，我也没有借机拉住她。我们继续往下时，脚步各自落在湿冷的台阶上，间隔没有被我强行缩短。"
    narrator "到下一层，她回头看了一眼上面的门。我看见她回头，不问是不是后悔，也不说不要回头。门、灯、铁盒和纸都还在上面；我们已经离开，却不表示那些事没有留下。她转回身时，我才继续走，像把这一眼也留给她自己。"
    narrator "楼梯间的应急灯忽明忽暗，把她握住的夹层照出一条窄边。我没有问里面是哪张票、哪张卡或哪一页纸。今晚我已经亲自数过能走的出口和需要承担的代价，数清并不赋予我翻开她手里东西的权利。"
    narrator "墙角堆着几只空纸箱，潮气让纸板软下来。她绕开纸箱时脚步放轻，我也跟着绕开。安全屋失效以后，任何一条走廊都不值得被我叫作绝对安全；但眼前没有塌掉的台阶、没有传来的脚步，也是不必夸大或省略的事实。"
    narrator "我把手机的屏幕调暗，先看时间，再收回口袋。时间正在过去，这让我想加快；她没有加快，我便不把自己的急切变成拉着她跑的理由。能跑多快不是唯一的准备，知道何时停下来让她看清也是。"
    narrator "她在楼梯拐角碰了一下墙，指尖很快收回。我没有去抓她的手。墙面冰冷、灯光不稳、门锁已经响过，这些都让我想把她护在身后；可我明白把人放到身后并不能证明我在保护，尤其当她没有要求。"
    narrator "我说：\"这边有扶手。要用就用。\""
    narrator "她没有伸向扶手，只继续扶着自己的夹层。这个选择很清楚，我便没有再把手伸过去。扶手仍在墙边，她随时可以拿；我把自己的手放在看得见的位置，既不代替她抓住，也不假装自己看不见她需要保持距离。"
    narrator "楼下传来门被风吹动的轻响，我停住听了一次。声音没有再来。我只告诉她：\"刚才有门响。现在没听见别的。\"我没有把这句话剪成“没事”，也没有把一次轻响扩成追来的人。她抬头看向出口，我等她决定下一步。"
    narrator "出口的标志在楼道尽头亮着，箭头指向左边。箭头只说明楼梯通向左边，不说明左边有什么人、有什么路或什么结局。我没有把它当成我们已经得到的答案，只让她先看见标志和门把的位置。"
    narrator "她把夹层压紧，又走了一阶。我看见她往下走，才把脚迈出去。我们此刻都在同一段楼梯上，是双方明确做出的共同动作；我不把它扩大成她已经接受我为她选择的任何路线。"
    narrator "我想起桌上那张空白地图。它没有被带走，却留在我脑子里。空白不是让我临时画一条线的许可，也不是把她推进最窄路线的借口。今晚能执行的事如果只有让她先通过出口、把我造成的风险写在自己名下，我就只做这两件。"
    narrator "走到一楼时，风从门缝里吹进来，带来雨后水泥地的味道。她停在门内侧，没有立刻拉门。我也停下，没有把门把先压下去。外面是下一步，不是我替她抢下的一份答案。"
    narrator "我问：\"要我开着，你先看一眼吗？\""
    narrator "她看着门缝的光，随后轻轻点头。我把门只推开一掌宽，站在侧边，让她能自己看见外面的路。她没有把夹层交给我，我也没有去碰。门被我推开是我的动作；跨不跨过去仍由她决定。"
    narrator "外面没有人声，只有雨水从屋檐滴到台阶。她看了一会儿，先把脚放到门槛外。我跟在她身后，没把伞抬到她头顶前。她如果想要，会看向伞或伸手；没有这种动作时，我只让门口的光照着她自己选择的方向。"
    narrator "门在身后缓缓合上，安全屋最后留给我的只是一声很轻的碰响。我没有回头确认铁盒、纸和水杯是不是还在原位。那些东西会在之后构成后果，而此刻她已在门外站稳。把注意力放回她已经走出的这一步，比回头检查我的布置更重要。"
    narrator "街上的风把她衣角吹起，她自己压住。我没有说我们总能找到下一处地方，也没有用一段未来的保证覆盖现在仍然可见的风险。今晚的出口只是出口；她手里保住的物件、我写下的代价和还没被解决的事，会跟着我们进入下一天。"
    narrator "我把门锁失效、出口位置和离开时的时间记在心里，不把它们说成已经足够的安全方案。以后若有人问起，我会从自己看见、听见和做过的部分开始说，不再替她补上一句她没有给过的话。"
    narrator "她在路灯下停了一秒，确认夹层没有被风吹开，才继续向街口走。我没有替她拿住纸，也没有把她的步子拉快。此刻能共同确认的只是她在走、我在后面让出位置；所有更远的方向仍要等她真正选择。"
    narrator "雨后的台阶在身后发亮，安全屋的灯已被门遮住。我没有回头把它叫作最后一次失去，也没有把前方叫作新的开始。代价正在由我承担，选择仍在她手里，我们只把脚步放到下一段能看见的路上。"
    narrator "我站在她侧后，等她看向街口或停下。没有路线时，我不画；有路线时，我不替她抓住；需要我承担的部分，我会按自己已经写下的去做。风穿过空街，灯仍然忽明忽暗，我只让下一次问话在她真正需要时才出现。"
    return
