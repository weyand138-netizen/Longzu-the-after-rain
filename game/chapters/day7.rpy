init python:
    # Day 7 owns acknowledgement only. SYS-ENDING owns all terminal derivation,
    # lifecycle, persistence, completion, labels, and ending presentation.
    from modules.day7_source_generation import DAY7_SOURCE_SHA256

    DAY7_SOURCE_UNIT_ID = "chapter_day7_before_red_well"
    DAY7_REQUIRED_SCENE_IDS = (
        "scene_day7_red_well_approach",
        "scene_day7_causal_recall",
        "scene_day7_ending_entry",
    )
    DAY7_CHOICE_RECORDS = ()
    DAY7_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day7_before_red_well",
            "day_index": 7,
            "observable_fact_ids": ("fact_days1_to6_acknowledged",),
            "source_unit_id": DAY7_SOURCE_UNIT_ID,
            "source_sha256": DAY7_SOURCE_SHA256,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_days1_to6_causal_recall",
            "day_index": 7,
            "observable_fact_ids": ("fact_days1_to6_acknowledged",),
            "source_unit_id": DAY7_SOURCE_UNIT_ID,
        },
    )


label chapter_day7_before_red_well:
    $ current_chapter = "day7"
    scene bg warm_room

    # scene_day7_red_well_approach
    narrator "红井前的风从潮湿的石阶间穿过去，把远处的水声推到两人脚边。"
    narrator "绘梨衣先停下，把折好的纸按在掌心；她没有替任何一条路补出一个答案。"

    # scene_day7_causal_recall
    narrator "路明非把前六日已经说出的话、留下的空白和没有被抹去的后果，一件件放回两人之间。"
    narrator "它们不替谁改写已经发生的事，也不把还没有被答应的事写成承诺。"

    # scene_day7_ending_entry
    narrator "到了这里，他不再替她把下一步写好，只把能被看见的路和代价留在原处。"
    narrator "绘梨衣看过最后一页，在自己的名字旁轻轻点了一下。"
    jump day7_resolve_ending
