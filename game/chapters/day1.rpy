init python:
    # Build-time input only. Story 002 owns generation of the flow manifest.
    DAY1_SOURCE_UNIT_ID = "chapter_day1_her_own_name"
    DAY1_REQUIRED_SCENE_IDS = (
        "scene_day1_clothing_answer",
        "scene_day1_food_gesture",
        "scene_day1_receipt_name",
    )
    DAY1_CHOICE_RECORDS = (
        (
            "day1_accept_clothing",
            "reaction_day1_accept_clothing",
            "payoff_day1_clothing_day4",
        ),
        (
            "day1_choose_safe_clothing",
            "reaction_day1_choose_safe_clothing",
            "payoff_day1_safe_clothing_day5",
        ),
        (
            "day1_repair_first_destination",
            "reaction_day1_repair_first_destination",
            "payoff_repair_first_destination",
        ),
        (
            "day1_keep_first_override",
            "reaction_day1_keep_first_override",
            "payoff_keep_first_override",
        ),
        (
            "day1_read_food_gesture",
            "reaction_day1_read_food_gesture",
            "payoff_day1_food_day5",
        ),
        (
            "day1_assume_food_consent",
            "reaction_day1_assume_food_consent",
            "payoff_day1_assume_day5",
        ),
    )
    DAY1_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day1_her_own_name",
            "day_index": 1,
            "observable_fact_ids": (
                "fact_day1_erii_selects_casual_clothes",
                "fact_day1_erii_points_to_food",
                "fact_day1_receipt_has_name",
            ),
            "source_unit_id": DAY1_SOURCE_UNIT_ID,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_day1_receipt_name",
            "day_index": 1,
            "observable_fact_ids": ("fact_day1_receipt_has_name",),
            "source_unit_id": DAY1_SOURCE_UNIT_ID,
        },
    )

label chapter_day1_her_own_name:
    $ current_chapter = "day1"
    if persistent.sys_persist_state["settings"]["reduced_motion"]:
        scene bg warm_room
    else:
        scene bg warm_room
        with dissolve_slow

    # scene_day1_clothing_answer
    narrator "清晨的店里还没有客人。绘梨衣把两件便服并排放在桌上，手指停在较浅的一件上。"
    narrator "窗帘缝里漏进一条很淡的光，照出衣料上没有擦干的雨点。她先把袖口翻过来，再把另一件衣服往旁边推了一点。"
    narrator "桌上放着昨晚折好的愿望纸和一支没有盖帽的笔。她没有去碰笔，只把较浅的便服拉近，像是在把今天的范围缩小到一个可以自己完成的动作。"
    narrator "路明非站在桌边，手里还拿着那张写过路线的车票。他本来想说厚一点更安全，最后只看着她把衣角重新抚平。"
    narrator "外面的卷帘门还没有完全升起。店里没有客人的声音，只有衣架轻轻碰到墙面的响动，提醒他们今天也会从很小的决定开始。"
    $ critical_choice_interaction = True

    menu:
        "照她挑的便服收进行李":
            $ apply_choice("day1_accept_clothing", {"autonomy": 1})
            narrator "她把衣角抚平，自己把那件便服放进包里。"
            erii "嗯。"
            narrator "她把包的拉链拉到一半，停下来检查衣角有没有被夹住。确认没有皱折后，她才把拉链拉到底，并把包带调到自己方便拿取的位置。"
            narrator "路明非把厚外套折好放在旁边，没有再把它塞进她的包。她看见这个动作，伸手把外套往桌里推了推，给自己的选择留出空间。"
            $ critical_choice_interaction = False

        "换成更厚的安全外套":
            $ apply_choice("day1_choose_safe_clothing", {})
            narrator "她接过外套，原先挑出的便服留在桌边，没有被收进包里。"
            narrator "她把外套套上以后，先试着抬了抬手臂，又把原本挑出的便服折回椅背。那件衣服没有消失，只是暂时离开了今天的行李。"
            narrator "路明非把椅背对着她转过来，让衣服不会被门边的雨水溅到。她没有道谢，只抬眼确认衣角已经离开地面。"
            $ critical_choice_interaction = False

    # scene_day1_food_gesture
    narrator "早餐送来时，绘梨衣把药盒推远，用筷子指向一碗热粥。"
    narrator "热粥的蒸汽把窗玻璃蒙出一小块白。药盒上的说明被水汽遮住了半行，她用筷子柄敲了敲碗边，又把药盒往柜台方向推。"
    narrator "路明非把勺子放到碗旁，没有马上把药拿走。她看见他的手停住，才把筷子横放在碗上，像是把刚才的动作重新摆成一件可以被确认的事情。"
    narrator "店里有人从门外经过，雨伞收拢的声音短暂盖过了早餐的香气。绘梨衣仍看着热粥，没有把视线转向药盒。"
    narrator "路明非想起站台上的那张纸：愿望不一定先写成完整的句子。今天她给出的回答也只有碗、药盒和一段等待。"
    $ critical_choice_interaction = True

    menu:
        "问她是不是只想吃热粥":
            $ apply_choice("day1_read_food_gesture", {"understanding": 1})
            lm "只吃这个，好吗？"
            erii "嗯。"
            narrator "她把药盒合上，双手捧住热粥。"
            narrator "她先吹散表面的热气，喝了一小口，又把碗转到自己顺手的位置。药盒被推到看不见的位置，桌面因此清出了一条可以安心吃饭的边。"
            narrator "路明非把勺子放回她伸手就能拿到的地方，没有替她决定下一口该吃什么。她低头喝粥，肩膀慢慢从绷紧里放松下来。"
            $ critical_choice_interaction = False

        "把药和早餐一起放到她面前":
            $ apply_choice("day1_assume_food_consent", {})
            narrator "她没有碰药盒，只把热粥拉近了一点。"
            narrator "药盒仍在她和路明非之间，像一道被忽略却没有消失的边界。她把热粥拉近，勺子却只在碗里轻轻搅了一下。"
            narrator "路明非看见她的手停在药盒旁，随后收回袖口。他没有得到确认，桌上的沉默也没有替他补上确认。"
            $ critical_choice_interaction = False

    # scene_day1_receipt_name
    narrator "结账时，收据从柜台边滑下来。绘梨衣先按住纸角，再用指尖点了点打印出的名字。"
    narrator "打印机吐纸的声音很短，收据上的墨迹却比站台那张纸清楚。她先看日期，再看名字，最后用指甲沿着名字的边缘轻轻划过。"
    narrator "路明非把柜台上的零钱推到一旁，让她可以把收据摊平。那几个字没有因为被读出来就变成他的称呼，也没有因为沉默就失去作用。"
    lm "我会把这张收据留好。"
    narrator "她把收据折成很小的一片，放进自己的口袋。"
    narrator "她折的是收据上没有印字的边角，名字仍留在里面。每折一次，她都会先确认字没有被压进折痕。"
    narrator "门外的雨比早晨小了一些。她把口袋按住，确认收据还在，又看向桌上那件没有带走的便服，像是在把今天的几个决定放回同一张桌面。"
    narrator "路明非没有把这些决定总结成一句话。结账单、热粥和衣服都只是普通物件，却让明天可以从一件已经被她保留下来的东西继续。"
    return
