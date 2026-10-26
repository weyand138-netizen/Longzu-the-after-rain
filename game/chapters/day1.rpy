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
    scene bg clothing_shop_rain_morning
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "天刚亮，我们在去安全屋的路上停了几分钟。小店的卷帘只升起一半，我买下两件能换洗的衣服，没让绘梨衣在门口试穿。"
    show npc clothing_clerk_back as shop_clerk
    narrator "店员从柜台后取来袋子，将收据和衣服一起放入其中。我把袋口拢好，拿着袋子带着她离开。"
    hide shop_clerk
    narrator "经过早餐铺和药店时，我们买了些热粥和药品。抓紧时间赶往安全屋。"

    scene bg rain_stopped_morning_window
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "进屋后，我锁好门，拉严临街的窗帘。屋里设施虽然简陋，但足够我们休息会了。"
    narrator "我将买好的东西都放到桌面上。"

    # scene_day1_clothing_answer
    show char erii day1_corner as erii_day1
    show char lu mingfei day1_corner as lu_mingfei_day1
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    show prop clothing_pair_table as table_clothes
    narrator "绘梨衣从袋里取出两件便服，并排放到桌上，手指停在较浅的一件上。"
    narrator "窗帘缝里漏进一条很淡的光。她先把袖口翻过来，再把另一件衣服往旁边推了一点。"
    narrator "桌角放着昨晚折好的愿望纸和一支笔。她没有碰笔，只把较浅的便服拉近，抚平衣角。"
    narrator "我站在桌边，手里还拿着写过路线的车票。本来想说厚一点更安全，最后还是把车票放下，等她看完再说吧。"
    hide table_clothes
    show prop clothing_cuff_pair as visual_detail
    narrator "浅色便服很软，深色外套厚实。"
    show prop clothing_pair_table as table_clothes
    hide visual_detail
    hide table_clothes
    narrator "她举起浅色衣服，在身前比了一下，随后放回桌上。"
    narrator "我问她：\"这件要自己拿吗？\""
    narrator "她把浅色便服折成一个窄方块，放在包旁。"
    narrator "楼下有动静。我靠在门边听了一下，没有上楼的声音。绘梨衣抬头看我，我摇了摇头，重新坐回桌边。"
    hide erii_day1
    hide lu_mingfei_day1
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    $ critical_choice_interaction = True

    menu:
        "照她挑的便服收进行李":
            $ apply_choice("day1_accept_clothing", {"autonomy": 1})
            narrator "把那件便服放进包里。"
            erii "嗯。"
            narrator "我把厚外套折好，放在椅背上。她把包放到脚边。"
            $ critical_choice_interaction = False

        "换成更厚的安全外套":
            $ apply_choice("day1_choose_safe_clothing", {})
            narrator "她接过外套，浅色的那件放在桌边。"
            narrator "她把外套套上，抬了抬手臂，又把过长的袖口卷起来。"
            $ critical_choice_interaction = False

    show char erii day1_corner as erii_day1
    show char lu mingfei day1_corner as lu_mingfei_day1
    # scene_day1_food_gesture
    show prop hot_porridge as table_porridge
    show prop medicine_box_blister as table_medicine
    narrator "我打开保温袋，把打包的热粥倒进碗里。绘梨衣把药盒推远，用筷子指向那碗粥。"
    narrator "热气还没散。我把勺子和水杯放到碗旁，药盒留在桌沿，没有拆开里面的药板。"
    narrator "她又用筷子柄碰了一下碗边。我本来伸向药盒的手停住了。"
    narrator "一路上只顾着赶路，我知道她没吃早饭，身体也不太好，但没问过她想不想吃。"
    show prop medicine_box_far as table_medicine
    narrator "我把药盒移到桌子的另一端。"
    narrator "窗外有车驶过，她低头吹了吹粥。"
    $ critical_choice_interaction = True

    menu:
        "问她是不是只想吃热粥":
            $ apply_choice("day1_read_food_gesture", {"understanding": 1})
            lm "是不想吃药吗"
            erii "嗯。"
            hide table_medicine
            narrator "她把药盒合上，双手捧住热粥。"
            narrator "我把药盒放到靠墙的矮柜上，告诉她放在哪里。她喝了一小口粥，又伸手把水杯拉近。"
            hide table_porridge
            show char lu mingfei clear_empty_bowl as lu_mingfei_day1
            $ critical_choice_interaction = False

        "把药和早餐一起放到她面前":
            $ apply_choice("day1_assume_food_consent", {})
            show prop medicine_box_blister as table_medicine
            narrator "她没有碰药盒，只把热粥拉近了一点。"
            narrator "拿着勺子只在粥里轻轻搅了一下。"
            narrator "我说：\"抱歉没问你的意见\""
            narrator "她继续喝粥，没有拆药板。"
            $ critical_choice_interaction = False

    hide table_porridge
    hide table_medicine
    hide erii_day1
    hide lu_mingfei_day1
    # scene_day1_receipt_name
    narrator "收拾纸袋时，路上留下的收据滑到桌边。绘梨衣拿起收据用指尖点了点打印出的字。"
    show prop receipt_name
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "纸被袋里的热气捂软了，字还清楚。"
    lm "我会把这张收据留好。"
    hide prop receipt_name
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "她把收据折成很小的一片，放进自己的口袋。"
    narrator "我伸到一半的手收了回来，放在她那便好。"
    narrator "她抬头看了我一眼。我问：\"收好了？\"她拍了拍口袋"
    narrator "临走前，我把药品装进自己的背包，桌上的垃圾也一并带走。"
    narrator "绘梨衣重新扣好包带。我看了一眼椅背上留下的衣服，把窗帘拉回原处，确认门外没有危险。"
    narrator "她拿起门边的伞，等我收好钥匙。我们不能一直待在这里，接下来该怎么走"
    scene bg japanese_residential_street_rain_morning
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "我推开门下了楼，绕过路边的积水，她跟在后面。"
    narrator "我们又开始了新的逃亡。"
    return
