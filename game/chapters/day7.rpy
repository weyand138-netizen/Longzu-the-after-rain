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
    scene bg red_well_steps

    # scene_day7_red_well_approach
    narrator "红井的石阶还湿着。风从井下吹上来，带着一股铁锈味。"
    narrator "我停下脚步。水声在深处回荡，忽近忽远，井壁上的水痕一直没入暗处。"
    narrator "绘梨衣站在我下面一级。她把愿望纸摊在掌心，拇指压着纸角。最外面的折痕已经磨软了，有几个字仍旧认不清。"
    narrator "我记得站台排水沟边的水声。那晚雨很大，纸被泡得发软，我怕一松手，它就会被水冲走。"
    narrator "她低头把翘起的边角抚平，避开字迹，慢慢折回去。"
    narrator "我本来有许多话想说。到了她面前，先听见的却是自己急促的呼吸。"
    narrator "我说：\"这几天的事，我还记得。\""
    narrator "她把纸收进袖口，手仍按在那里。我垂下手，站在高一级的石阶上。潮气透过鞋底，一点点渗上来。"
    narrator "风吹动她的发尾。我们之间隔着半步，我等呼吸平下来，才继续往下说。"

    # scene_day7_causal_recall
    scene bg red_well_steps
    narrator "我把前六日的事从头说起。最先记起来的，竟是衣架碰墙的声音、粥碗上的白气，还有从纸袋里滑出来的那张收据。"
    narrator "第一天，绘梨衣用筷子指着粥，把药盒留在一旁。那时我忙着替她准备东西，连她想吃什么都忘了问。"
    narrator "收据上的字，她用指尖点过，随后折好，放进自己的口袋。我的手伸到一半，又收了回来。"
    narrator "第二天，屏幕上的光标一闪一闪。她输入的昵称还在框里，返回键和确认键挨在一起。我的手离它们很近。"
    narrator "后来她把游戏币交给我。小小的一枚，落进掌心时还带着温度。那天机台很亮，站在井边想起来，竟觉得隔了许多年。"
    narrator "第三天的教室就冷多了。雨从窗边渗进来，红泥蹭在窗沿，门没有关严。门禁记录、时间表和泥印的照片，在课桌上铺了一排。"
    narrator "她合上档案的声音很轻。我问没问过，停没停下，有些话究竟说到哪里，我都记得。已经发生的事，重说一遍也改不了。"
    narrator "第四天，我们站在售票窗前。玻璃把我的倒影映在地图上，她指过的小站就在下面。她把零钱排好，将联系人纸片从地图底下抽出来，放到灯光里。"
    narrator "实名留下的痕迹、单人票和联系人卡各自的风险。那时说出口的，咽回去的，我都还记得。"
    narrator "第五天，家族档案摊在灯下。原页和摘要放在两边，我的批注混在那些旧签名里。哪几页交到了她手上，哪几页被我收起，我比谁都清楚。"
    narrator "说到责任那一栏，我慢了下来。那天，笔一直在我手里。"
    narrator "第六天，安全屋的门锁响了。走廊尽头亮起一盏不该亮的灯，我们又得走。桌上摊开的纸还没收完，旧身份凭据的边角已经捏卷。"
    narrator "她把写着自己名字的那一栏推开。动作不重。我至今记得她的手指停在哪里。"
    narrator "说到这里，我停了一会儿。井下的水声涌上来，先前那些门锁声、翻纸声，才渐渐远了。"
    narrator "有几处说到一半就卡住了。我低头看着石阶，缓过那口气，才接着说。她一直站在那里，袖口压着那张纸。"
    narrator "我曾盼着把一切解释清楚，她就会肯留下。如今说完，心里还是空着。井下的水声没有停。"

    # scene_day7_ending_entry
    scene bg red_well_steps
    narrator "绘梨衣看过最后一页，在自己的名字旁轻轻点了一下。"
    narrator "我看着她的手，等了一会儿。她没有别的动作。"
    narrator "风掀起纸边，我按住，等她移开手才把纸收回。上面的字没有变。"
    narrator "我想起地图上的小站、维修门的封条。那几晚伏在灯下看地图，总觉得出口就在下一道门后。"
    narrator "\"你指过的地方，我记得。\"我说。"
    narrator "她望向更低的石阶，按紧袖口。我顺着看过去，只看见一层层湿暗的石面。"
    narrator "天色亮了一点。积水映出她的影子，风一吹，肩膀的轮廓就散了。"
    if "day2_save_second_token" in current_choice_history() and "day4_register_independent_contact" not in current_choice_history():
        narrator "我把手插回口袋，指尖碰到那枚游戏币。边缘硌着手，早已没有她掌心的温度。"
    else:
        narrator "我把手插回口袋，指尖习惯性地摸了摸。那枚游戏币已经不在，只碰到纸张揉软的边角。"
    narrator "\"我不知道接下来会怎样。\""
    narrator "这句话说出来，比我想的还轻。绘梨衣没有回头，发尾被风吹到颊边，她抬手拨开。"
    narrator "我想再添一句保证，张了张嘴，还是咽下去了。井这么深，站在这里，连水面都看不见。"
    narrator "一片叶子贴着水渍打了个转，落在她鞋边。她向下走了一步，又停住。"
    narrator "我往旁边让了让，把石阶空出来。"
    narrator "我说：\"我在后面。\""
    narrator "她没有回头。我站在原处，看见手背上那道被纸边划出的浅痕，已经不疼了。"
    narrator "来路上的脚印还没干。井下又传来一阵水声，我抬起头，等着。"
    jump day7_resolve_ending
