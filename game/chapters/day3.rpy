init python:
    # Build-time inputs only. No Day 3 partial or terminal manifest is created here.
    DAY3_SOURCE_UNIT_ID = "chapter_day3_empty_school"
    DAY3_REQUIRED_SCENE_IDS = (
        "scene_day3_classroom_trace",
        "scene_day3_evidence_choice",
        "scene_day3_truth_pace_answer",
    )
    DAY3_CHOICE_RECORDS = (
        (
            "day3_share_school_evidence",
            "reaction_day3_share_school_evidence",
            "payoff_day3_share_day5",
        ),
        (
            "day3_hide_school_evidence",
            "reaction_day3_hide_school_evidence",
            "payoff_day3_hide_day5",
        ),
        (
            "day3_honor_pause",
            "reaction_day3_honor_pause",
            "payoff_day3_pause_day5",
        ),
        (
            "day3_force_explanation",
            "reaction_day3_force_explanation",
            "payoff_day3_force_day6",
        ),
    )
    DAY3_CHOICE_EFFECTS = {
        "day3_share_school_evidence": ("truth",),
        "day3_hide_school_evidence": ("revoke:token_hide_school_evidence",),
        "day3_honor_pause": ("understanding", "autonomy"),
        "day3_force_explanation": ("revoke:token_override_daily_choice",),
    }
    DAY3_AGENCY_REQUEST_ID = "event_truth_pace_requested"
    DAY3_AGENCY_PAUSE_ANSWER_ID = "event_erii_closes_archive"
    DAY3_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day3_empty_school",
            "day_index": 3,
            "observable_fact_ids": (
                "fact_day3_empty_school_trace_confirmed",
                "fact_day3_erii_closes_archive",
            ),
            "source_unit_id": DAY3_SOURCE_UNIT_ID,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_day3_empty_school_trace",
            "day_index": 3,
            "observable_fact_ids": ("fact_day3_empty_school_trace_confirmed",),
            "source_unit_id": DAY3_SOURCE_UNIT_ID,
        },
    )


default event_empty_school_trace_confirmed = False
default cp_day3_empty_school_trace_complete = False
default agency_day3_truth_pace_request = None
default agency_day3_truth_pace_answer = None
default agency_day3_truth_pace_outcome = None


label chapter_day3_empty_school:
    $ current_chapter = "day3"
    scene bg empty_school_classroom_rain

    # scene_day3_classroom_trace
    narrator "教学楼里没有人声。走廊尽头亮着一盏灯，光从半开的教室门里漏进去，只照到一排歪斜的椅脚。"
    narrator "我停在门前。窗框底下沾着一小片红泥，雨水正沿着窗缝往下淌，将泥印的边缘冲得发亮。"
    narrator "绘梨衣走到窗边，低头看了一会儿。我把门禁记录、时间表和照片摊在课桌上，字朝着自己。"
    narrator "六点十二分的门禁，六点十四分的走廊截屏，照片拍得更晚。我用手指压住数字，从头又核了一遍。"
    narrator "照片里的泥印，与眼前这一片能对上。站台上那道红色也浮了上来，还有旁边的维修门。我把记得的几处位置写在纸背。"
    narrator "门禁、时间和泥印指向同一段来路。我圈出能对上的地方，在两处空白旁各留了一个问号。"
    narrator "窗下的泥半干了，边缘冲出几道细沟。我蹲下去看，仍分不清那脚印是朝门口来，还是往窗边去。"
    narrator "“时间对得上。”我说，“泥的颜色，也和站台上的一样。再往下，我还不知道。”"
    narrator "绘梨衣抬头看向门缝。走廊里的灯闪了一下，她的影子在桌边晃动，随后又停住。"
    narrator "我把门推开一些。铰链响了很长一声，等它停下来，才听见后排粉笔盒里的轻响。风从窗口直穿过这间屋子。"
    narrator "她从窗边回来，指节沾着一点红泥。袖口擦过去，留下一道淡痕。我低头看纸，照片的边已被自己捏出了一条折印。"
    $ event_empty_school_trace_confirmed = True
    $ cp_day3_empty_school_trace_complete = True

    # scene_day3_evidence_choice
    narrator "绘梨衣停在桌子另一边，看着我手里的纸。我把捏皱的照片边压平。"
    narrator "原记录铺了半张桌子，摘要却只有几行。写摘要时，我略去了时间里的空白，也没写那两个问号。"
    narrator "窗边的水滴下来，落在课桌脚旁。她等着，我却迟迟没有把手移开。"
    narrator "“要看原来的，还是先听我说？”"
    narrator "她的视线从纸页移到我脸上。我等了一会儿，手指仍压在原件上，指腹有些发白。"
    $ critical_choice_interaction = True

    menu:
        "把门禁记录、时间和泥印都递给她":
            $ apply_choice("day3_share_school_evidence", {"truth": 1})
            $ critical_choice_interaction = False
            narrator "我把门禁记录、时间表和照片一起递过去。她把三张纸一张张看完，再换了个顺序，重新摆到面前。"
            narrator "我在桌子这边坐下。她将照片转向窗光，凑近看边角的时间。"
            show story erii_read_archive
            narrator "翻到时间表背面时，她停住了。那两个问号被透过纸页的光照得很淡。"
            narrator "“这两处还没核实。”我说。"
            narrator "她用指甲轻轻碰了碰其中一个，接着往下看。风掀起纸角，她伸手按住，没有把那一页翻过去。"
            narrator "我原本还想补几句话，见她正沿着那行字看，便停了。"
            narrator "读完后，她把三张纸叠好，放在自己的包旁。我把手从桌面上收回来，听见雨水又滴了一声。"
            hide story

        "只告诉她已经核对出的结论":
            $ apply_choice("day3_hide_school_evidence", {})
            $ critical_choice_interaction = False
            narrator "她听完结论，手还停在桌沿。我把摘要留在她面前，原页收在自己这边。"
            narrator "几句话很快说完，教室里只剩雨声。她低头看了看摘要，又望向我掌下露出的照片边角。"
            narrator "我等着她点头，等了好一会儿。她把手从桌沿移开，收回袖口。"
            narrator "“原件在这里。”我说。"
            narrator "话说完，手却没有松开。纸角硌着掌心，像是连这句话也显得多余。"

    # scene_day3_truth_pace_answer
    narrator "我把余下的说明放到手边，刚要接着说，绘梨衣动了一下。"
    $ agency_day3_truth_pace_request = DAY3_AGENCY_REQUEST_ID
    narrator "绘梨衣合上档案，指尖压在封面上，没抬头。"
    $ agency_day3_truth_pace_answer = DAY3_AGENCY_PAUSE_ANSWER_ID
    narrator "封面的布边起了毛，她的指尖停在那里。合拢的纸页慢慢落平，最后一点翻动声也消失了。"
    narrator "楼下响起锁链声。我看了一眼门口，又低头看手机。没有新消息。"
    narrator "那声音又响了一次。我想赶紧把余下的话说完，带她离开；她压着封面的手却一直没动。"
    narrator "“要先收起来吗？”我问。"
    narrator "她的指尖挪到封面边缘，停住。我握着手里的纸，听见雨水落在走廊外的铁栏上。"
    $ critical_choice_interaction = True

    menu:
        "先把档案收好，等她自己再打开":
            $ apply_choice("day3_honor_pause", {"understanding": 1, "autonomy": 1})
            $ critical_choice_interaction = False
            $ agency_day3_truth_pace_outcome = "outcome_pause_honored"
            narrator "我把档案收在桌边，停下来。绘梨衣的手慢慢松开。"
            narrator "过了一会儿，她看了我一眼，自己把最上面那页重新翻开。"
            show story erii_read_archive
            narrator "我把椅子往后挪了挪。椅脚擦过地板，她抬眼看了一下，随即又低下头。"
            narrator "她沿着手边那页往下看，指尖在一行字旁停住，转过来给我看。"
            narrator "我靠到桌角，将她指的那一行念出来。念完，她的手还压在那里，我便等着。"
            narrator "这次翻页声隔了很久才响。"
            show story lu_hold_classroom_door
            narrator "走廊里响起拖桶的声音，由近到远。风把门吹开，我起身抵住门边，回头时，她还坐在桌前。"
            hide story

        "继续解释余下的内容":
            $ apply_choice("day3_force_explanation", {})
            $ critical_choice_interaction = False
            $ agency_day3_truth_pace_outcome = "outcome_pause_overridden"
            narrator "我继续把余下的说明念完。绘梨衣的手离开纸边，退了一步，又退了一步。"
            narrator "空教室里还荡着我的声音。我低头攥着那几页纸，半天没松开。"
            show story erii_turn_exit
            narrator "再抬头时，她已站在门口。走廊的光从身后照来，我看不清她的脸。"
            narrator "我想说自己只是怕来不及。她的手停在门把旁，没向桌子这边伸。"
            narrator "最后一个字的回声散了。窗外的雨不知什么时候停了，水沿着窗框，断断续续往下滴。"
            narrator "我把纸放下，退到桌边。我和她之间，空出了一大段地面。"
            hide story

    narrator "离开前，我又看了一眼窗下的红泥。边缘干了些，那几道被雨冲出的细沟还在。"
    narrator "绘梨衣拉好包带，走向门口。我说：“楼梯在左边。”"
    scene bg residential_stairwell_night
    narrator "她穿过走廊的灯影，我才跟上。教室门留着一条缝，风从里面吹出来，带着潮湿的粉笔味。"
    narrator "二楼的平台上，她停了一会儿。窗外操场空着，红色跑道在暮色里只露出一小段。我握着扶手等，掉漆的地方有些硌手。"
    narrator "楼下的感应灯灭了。她迈下一阶，灯重新亮起，将出口照成一小块白色。"
    narrator "“以后还想看，我带你回来。”我说。"
    scene bg school_exit_dusk
    narrator "她望了眼门内，便转向街上。我把钥匙攥在手里，那句话的尾音还留在楼道里。"
    narrator "校门旁停着几辆自行车，车座上积着水。她从车缝里穿过去，避开一只倒扣的桶。"
    narrator "走到路灯下，她抬手看了看指节。那点红泥已经干了，颜色比刚才浅。她用袖口擦过，随后把手缩了回去。"
    narrator "我也停下来。远处一辆公交车驶过，轮胎碾开积水，车尾的红灯很快消失。"
    narrator "树叶还在滴水。绘梨衣走出屋檐，我提着收拢的伞，跟到街口。"
    narrator "红灯亮着，我们站在人行道边。风把灯柱上的广告吹得轻响，我望着她肩后的街道，忽然想不起刚才那几句说明是怎么说完的。"
    narrator "绿灯亮了。她先迈出一步，我跟上去。鞋底踩过积水时，半开的教室门又在脑子里闪了一下。"
    return
