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
    narrator "店员背对着我们，从柜台后取来袋子。收据压在衣服上，我把袋口拢好，带她离开。"
    hide shop_clerk
    narrator "经过早餐铺和药店时，我们又买了打包的热粥和备用药品。纸袋贴着手心发烫，我没有停下来拆开，沿来时记住的小巷赶往安全屋。"

    scene bg ordinary_rental_room_rain_night
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "进屋后，我锁好门，拉严临街的窗帘。屋里的桌椅虽然简陋，够我们换下湿衣服，吃完早饭，再商量下一段路。"
    narrator "我把几个袋子放到桌上，粥留在保温袋里，药品放在另一边。走廊暂时没有脚步声，我脱下滴水的外套，搭在门边。"

    # scene_day1_clothing_answer
    show char erii day1_corner as erii_day1
    show char lu mingfei day1_corner as lu_mingfei_day1
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    show prop clothing_pair_table as table_clothes
    narrator "绘梨衣从袋里取出两件便服，并排放在桌上，手指停在较浅的一件上。"
    narrator "窗帘缝里漏进一条很淡的光。她先把袖口翻过来，再把另一件衣服往旁边推了一点。"
    narrator "桌角放着昨晚折好的愿望纸和一支笔。她没有碰笔，只把较浅的便服拉近，抚平衣角。"
    narrator "我站在桌边，手里还拿着写过路线的车票。本来想说厚一点更安全，最后还是把车票放下，等她看完。"
    hide table_clothes
    show prop clothing_cuff_pair as visual_detail
    narrator "浅色便服的领口洗得很软，深色外套的扣子却扣得严实。我碰了碰外套的布料，又收回手。保暖、遮挡、好走路，理由都很充分，可她还没有点头。"
    show prop clothing_pair_table as table_clothes
    hide visual_detail
    hide table_clothes
    narrator "她举起浅色衣服，在身前比了一下，随后放回桌上。纸袋里的收据滑出半截，被她压在衣角下面。"
    narrator "我问她：\"这件要自己拿吗？\""
    narrator "她把浅色便服折成一个窄方块，放在包旁。拉链还开着，两件衣服都没有收进去。"
    narrator "楼下有门关上。我停下来听了一会儿，声音没有沿楼梯上来。绘梨衣抬头看我，我示意没事，重新坐回桌边。"
    hide erii_day1
    hide lu_mingfei_day1
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    $ critical_choice_interaction = True

    menu:
        "照她挑的便服收进行李":
            $ apply_choice("day1_accept_clothing", {"autonomy": 1})
            narrator "她把衣角抚平，自己把那件便服放进包里。"
            erii "嗯。"
            narrator "拉链拉到一半，她停下来，把夹住的布角捋平，再拉到底。我没有伸手接过去。"
            narrator "我把厚外套折好，留在椅背上。她试了试包带，才把包放到脚边。"
            $ critical_choice_interaction = False

        "换成更厚的安全外套":
            $ apply_choice("day1_choose_safe_clothing", {})
            narrator "她接过外套，原先挑出的便服留在桌边，没有被收进包里。"
            narrator "她把外套套上，抬了抬手臂，又把过长的袖口卷起来。浅色便服被她折好，放在椅背上。"
            narrator "我问：\"那件也带着吗？\"她看了一眼，没有伸手。我把包放回她脚边，不再催她回答。"
            $ critical_choice_interaction = False

    # scene_day1_food_gesture
    show prop hot_porridge as table_porridge
    show prop medicine_box_blister as table_medicine
    narrator "我打开保温袋，把路上买的热粥倒进屋里的碗。绘梨衣把药盒推远，用筷子指向那碗粥。"
    narrator "热气还没散。我把勺子和水杯放到碗旁，药盒留在桌沿，没有拆开里面的药板。"
    narrator "她又用筷子柄碰了一下碗边。我本来伸向药盒的手停住了。"
    narrator "一路上顾着赶路，我只知道她没吃早饭，没问过她现在想先做什么。买了药带来，也不能算她已经答应吃。"
    show prop medicine_box_far as table_medicine
    narrator "我把药盒移到桌子的另一端。盒盖没扣紧，露出一角说明书；她没有去看，只把粥碗转到自己面前。"
    narrator "窗外有车驶过，声音隔着窗帘渐渐远了。她低头吹了吹粥，等我把挡在碗旁的纸袋拿开。"
    $ critical_choice_interaction = True

    menu:
        "问她是不是只想吃热粥":
            $ apply_choice("day1_read_food_gesture", {"understanding": 1})
            lm "只吃这个，好吗？"
            erii "嗯。"
            hide table_medicine
            narrator "她把药盒合上，双手捧住热粥。"
            narrator "我把药盒拿到靠墙的矮柜上，告诉她放在哪里。她喝了一小口粥，又伸手把水杯拉近。"
            narrator "她吃得很慢。我也拆开自己的早餐，坐在桌子的另一边，没有再提药。"
            hide table_porridge
            narrator "粥见底时，我问还要不要添。她摇头，我才把空碗收到水槽里，用纸巾擦掉桌上的水。"
            $ critical_choice_interaction = False

        "把药和早餐一起放到她面前":
            $ apply_choice("day1_assume_food_consent", {})
            show prop medicine_box_blister as table_medicine
            narrator "她没有碰药盒，只把热粥拉近了一点。"
            narrator "药盒挡在碗和水杯之间。她的手停在盒边，随后收回袖口，勺子只在粥里轻轻搅了一下。"
            narrator "我说：\"我刚才没有先问。现在先不碰它。\""
            narrator "她没有回答。我把药盒挪到不挡着碗的地方，坐回去。她继续喝粥，没有拆药板，我也不再替她安排。"
            $ critical_choice_interaction = False

    hide table_porridge
    hide table_medicine
    # scene_day1_receipt_name
    narrator "收拾纸袋时，路上留下的收据滑到桌边。绘梨衣先按住纸角，再用指尖点了点打印出的名字。"
    show prop receipt_name
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "纸被袋里的热气捂软了，字还清楚。她先看日期，再看名字，最后用指甲沿着那一行轻轻划过。"
    narrator "我把桌上的零钱拢到一旁，让她把收据摊平。结账时只顾着离开，我到现在才留意付款信息留下的名字。"
    lm "我会把这张收据留好。"
    narrator "她把收据折成很小的一片，放进自己的口袋。"
    narrator "我伸到一半的手收了回来。她折的是没有印字的边角，名字藏在里面，不需要再交给我保管。"
    narrator "她抬头看了我一眼。我问：\"要写在别的地方吗？\"她摇头，把口袋盖压平。"
    hide prop receipt_name
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "临走前，我把药品装回单独的小袋，收进自己的背包。桌上的垃圾也一并带走，没把没吃的药混进她的东西。"
    narrator "绘梨衣重新扣好包带。我看了一眼椅背上留下的衣服，把窗帘拉回原处，确认门外没有人停留。"
    narrator "她拿起门边的伞，等我收好钥匙。我们不能一直待在这里，但出门后往哪边走，还可以一起看。"
    scene bg black
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "我推开楼下的门，让她先看清雨里的台阶。她撑开伞，绕过门边的积水，我跟在后面，鞋底踩到水坑边缘，溅湿了裤脚。"
    narrator "到了路口，她先看车流，再迈出脚。我没有抓住她的袖子，只跟着过街。"
    narrator "收据在她的口袋里，药品在我的包里。早饭留下的热意还没散，我们沿屋檐继续走，没有再停下来逛店。"
    return
