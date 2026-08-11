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
    $ critical_choice_interaction = True

    menu:
        "照她挑的便服收进行李":
            $ apply_choice("day1_accept_clothing", {"autonomy": 1})
            narrator "她把衣角抚平，自己把那件便服放进包里。"
            erii "嗯。"
            $ critical_choice_interaction = False

        "换成更厚的安全外套":
            $ apply_choice("day1_choose_safe_clothing", {})
            narrator "她接过外套，原先挑出的便服留在桌边，没有被收进包里。"
            $ critical_choice_interaction = False

    # scene_day1_food_gesture
    narrator "早餐送来时，绘梨衣把药盒推远，用筷子指向一碗热粥。"
    $ critical_choice_interaction = True

    menu:
        "问她是不是只想吃热粥":
            $ apply_choice("day1_read_food_gesture", {"understanding": 1})
            lm "只吃这个，好吗？"
            erii "嗯。"
            narrator "她把药盒合上，双手捧住热粥。"
            $ critical_choice_interaction = False

        "把药和早餐一起放到她面前":
            $ apply_choice("day1_assume_food_consent", {})
            narrator "她没有碰药盒，只把热粥拉近了一点。"
            $ critical_choice_interaction = False

    # scene_day1_receipt_name
    narrator "结账时，收据从柜台边滑下来。绘梨衣先按住纸角，再用指尖点了点打印出的名字。"
    lm "我会把这张收据留好。"
    narrator "她把收据折成很小的一片，放进自己的口袋。"
    return
