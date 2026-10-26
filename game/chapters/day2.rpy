init python:
    # Build-time input only. No Day 2 manifest is created by this story.
    DAY2_SOURCE_UNIT_ID = "chapter_day2_two_game_tokens"
    DAY2_REQUIRED_SCENE_IDS = (
        "scene_day2_alias_answer",
        "scene_day2_two_tokens",
        "scene_day2_last_machine",
    )
    DAY2_CHOICE_RECORDS = (
        (
            "day2_accept_alias",
            "reaction_day2_accept_alias",
            "payoff_day2_alias_day4",
        ),
        (
            "day2_assign_alias",
            "reaction_day2_assign_alias",
            "payoff_day2_assigned_alias_day6",
        ),
        (
            "day2_admit_alias_unknown",
            "reaction_day2_admit_alias_unknown",
            "payoff_day2_admit_day5",
        ),
        (
            "day2_save_second_token",
            "reaction_day2_save_second_token",
            "payoff_day2_token_day6",
        ),
        (
            "day2_spend_both_tokens",
            "reaction_day2_spend_both_tokens",
            "payoff_day2_spend_day4",
        ),
    )
    DAY2_CHOICE_EFFECTS = {
        "day2_accept_alias": ("understanding", "autonomy"),
        "day2_assign_alias": ("revoke:token_override_daily_choice",),
        "day2_admit_alias_unknown": (
            "understanding",
            "repair:token_silence_as_consent",
        ),
        "day2_save_second_token": ("preparation", "acquire:resource_arcade_token"),
        "day2_spend_both_tokens": ("sacrifice", "event:event_both_tokens_spent"),
    }
    DAY2_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day2_two_game_tokens",
            "day_index": 2,
            "observable_fact_ids": (
                "fact_day2_erii_enters_alias",
                "fact_day2_last_machine_handoff",
            ),
            "source_unit_id": DAY2_SOURCE_UNIT_ID,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_day2_arcade_alias",
            "day_index": 2,
            "observable_fact_ids": ("fact_day2_erii_enters_alias",),
            "source_unit_id": DAY2_SOURCE_UNIT_ID,
        },
    )


label chapter_day2_two_game_tokens:
    $ current_chapter = "day2"
    scene bg quiet_arcade_corner

    # scene_day2_alias_answer
    narrator "站在商场角落的街机前，绘梨衣在输入昵称的界面停顿了一会，慢慢敲下几个字母，又把头转向我。"
    narrator "商场广播正在播报清场提示，远处的卷帘门一扇一扇落下。街机的光线打在在她的手背上。"
    narrator "她每输入一个字母，就停顿一下来确认屏幕有没有正确显示。"
    show prop arcade_control_panel as visual_detail
    narrator "我没有伸手去碰键盘，这是她的选择。"
    hide visual_detail
    narrator "她看向我，还没有按下确认。"
    narrator "街机外壳的划痕泛着银光，从投币口延到屏幕边，不知是哪个没素质的留下的。绘梨衣仍在看着我或许是等待我的回应。"
    narrator "我问：\"这是让我确认，还是要我改？\""
    narrator "她伸出手指指了一下昵称框，又指了一下我。看着屏幕Sakura？"
    narrator "我说：\"这是我的名字\""
    narrator "远处的卷帘门又落下一扇，金属撞击声在空商场里回荡。"
    narrator "昵称框提示着：请输入玩家名称。这一次是她自己输入的名字"
    narrator "居然输入的我的名字吗，虽然不是真名。"
    narrator "我说：\"确定用这个名字吗？\""
    narrator "她的表情没有立刻改变。她只是把手放在确认键上，却没有按下。我放任她使用这个假名以后被她发现我骗她会不会不太好。"
    narrator "清场广播又催了一遍，街机的音效把它压得断断续续。无论最后写下什么，至少这一刻不该因为我急着离开就被改成我的决定。"
    $ critical_choice_interaction = True

    menu:
        "按她输入的昵称确认":
            $ critical_choice_interaction = False
            $ apply_choice("day2_accept_alias", {"understanding": 1, "autonomy": 1})
            narrator "我说：\"就用这个昵称吧。\""
            erii "嗯。"
            narrator "她没有立刻开始游戏，先等名字在屏幕上完整显示一轮，又看了一遍那个昵称"
            narrator "我默默读了一遍这个昵称，没有解释什么。"
            narrator "我说：\"你很喜欢这个名字吗？\""
            narrator "她没有回复，只是把我推到操控杆前。好吧那就玩吧，不再在意名字。"
            narrator "她自己控制着游戏角色，调整方向。和她的手一样都在她眼前。我只是看着，不替她按下任何键。"

        "换成我替她想的昵称":
            $ critical_choice_interaction = False
            $ apply_choice("day2_assign_alias", {})
            narrator "我输入了新的昵称并按下确认键。"
            narrator "我想解释这个名字更容易记。她没有点头，但也没有删掉它。"
            narrator "新名字在屏幕上亮起。她没有伸手去改，也没有进行下一步操作。我看见她把手放在膝上，才意识到刚才那一下确认是我按下的。"
            narrator "我本想说的话到嘴边又停住。好记是我给出的理由，不是她给出的回答。她没有问我为什么，我也不该用解释来替代她自己的选择。"
            narrator "我说：\"抱歉不该替你决定的。\""
            narrator "她看了看屏幕，没有回答。"

        "重新问她,确认是这个昵称吗" if has_unresolved_token("token_silence_as_consent"):
            $ critical_choice_interaction = False
            $ apply_choice("day2_admit_alias_unknown", {"understanding": 1})
            narrator "绘梨衣重新敲下自己的昵称"
            narrator "这一次她输入得更慢，每个字母都停一下。"
            narrator "她按确认前又看了我一眼。开始音响起时，我听见她轻轻呼了一口气，她自己完成了目标。"

    # scene_day2_two_tokens
    narrator "拿出包里的两枚游戏币。绘梨衣把其中一枚放到我掌心，另一枚压在开始键旁。"
    show prop game_coin_pair
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "一枚币足够开始玩，第二枚币能延长游玩时间。"
    narrator "商场的广播再次催促顾客离场。绘梨衣看了看屏幕上显示的时间，又看向我手里的那枚币。"
    narrator "游戏时间快结束了，想继续玩的话要继续投币，商场要关门，外面下着雨，明天的逃亡方向还没定；留下一枚不一定能救我们，花掉一枚也不一定有严重后果。"
    hide prop game_coin_pair
    show char erii open_palm_arcade as visual_pose
    narrator "绘梨衣还在摆弄操控杆，她没有找我要那枚币。我看见她指尖有一点发红，或许是机器太凉，也或许只是光线。"
    narrator "我问：\"你想要玩吗\""
    hide visual_pose
    show prop game_coin_pair
    narrator "她没有马上点头，只是看向我"
    narrator "我问：\"不想玩的话就走吧\""
    narrator "她听完这句，视线落回机器。沉默了一会儿，她把手指放在开始键旁的那枚币上。"
    narrator "我问：\"那我把游戏币放进去了？\""
    narrator "她把手中的硬币推进去，屏幕亮起第一关，她开始沉浸玩游戏"
    narrator "不久一枚硬币的可玩时间要结束了，还要投入我手中的第二枚硬币吗"
    narrator "倒计时快结束时，她向我看了一眼。"
    hide prop game_coin_pair
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    $ critical_choice_interaction = True

    menu:
        "收好硬币，留作记号":
            $ critical_choice_interaction = False
            $ apply_choice("day2_save_second_token", {"preparation": 1})
            narrator "她把手指放在操纵杆上，屏幕上显示的倒计时快结束了。"
            narrator "我把手中的硬币放回口袋里，拒绝了她想继续玩的想法"
            narrator "没多少时间了我们还需要继续逃亡"
            narrator "这枚硬币就留作纪念吧"
            narrator "绘梨衣见此也起身离开了街机，没有反对"
            narrator "我们一起离开了商城，雨还在下。新的逃亡开始了。"

        "投入硬币，陪她玩会":
            $ critical_choice_interaction = False
            $ apply_choice("day2_spend_both_tokens", {"sacrifice": 1})
            narrator "最后一枚币落进机器。她把手放回操纵杆上，直到这一局的音乐停下。"
            narrator "第二枚币也消失在投币口里，机器的灯光因此更亮了一点。她没有回头看空掉的出票口，只把视线留在下一关的画面上。"
            narrator "我站在她身后，听着机器的提示音一声一声结束。想要把这一晚留得更久的愿望，先变成了一个不会再回到手里的动作。"
            narrator "我没有回头看空掉的出票口。她仍在屏幕前，我便把注意力留在这一局的节奏里；以后缺少什么，不能拿来抹掉她此刻确实想玩的东西。"
            narrator "第二枚币落下以后，机器把剩余时间延长。绘梨衣没有欢呼，只把操纵杆握得更紧。屏幕里的人物从刚才失败的地方重新开始，她自己试着绕过那面墙。"
            narrator "我没有把手覆到她手背上，也没有抢着说应该往哪边按。"
            narrator "她撞到障碍时停了一下，转头看我。我先问：\"要我说，还是你自己试？\""
            narrator "她把视线转回屏幕，自己又按了一次。角色绕开墙后，提示音响起。她没有看投币口，我也没有把这个小小的通过说成两枚币都花得值得。硬币已经不在手里，眼前这局仍然是她刚才选择留下的时间。"
            narrator "音乐越到后面越快，商场的清场广播几乎听不清。她没有要求我替她玩，我就站在旁边数着屏幕上的时间。她如果看向我，我才说剩几秒；她不看，我也不把倒计时喊成催促。"
            narrator "最后一关结束时，画面闪出一行短短的胜利字。她看着它，没有把手举起来。我也没有说恭喜得像是在替她把今晚定义成圆满。"
            narrator "机器的光照在她脸上，又很快暗了一点；她自己松开操纵杆，游戏才真正结束。"

    # scene_day2_last_machine
    narrator "最里面那台机器熄屏前，绘梨衣把掌心贴在玻璃上，又收回手。商场要打烊了。"
    narrator "屏幕的余光映在玻璃上，像一层很薄的雾。她把掌心贴上去时没有触碰任何按钮，只是在确认这台机器已经把这一局完整记住。"
    narrator "清场人员从远处走来，脚步声在空下来的商场里变得很清楚。绘梨衣先把包带拉紧，再确认口袋里的收据没有滑出来。"
    lm "走吧。明天再想下一站。"
    narrator "她走在我身边，没有催促，也没有回头。"
    narrator "离开街机区前，她回头看了一次刚才的屏幕。名字已经随着画面熄灭，却没有因此回到一个还未选择的状态。"
    if "day2_save_second_token" in current_choice_history():
        narrator "我摸了摸装着游戏币的口袋，确认金属仍在。门外的雨落在商场台阶上，明天的路线还没有写完，但今天留下的东西已经各自有了位置。"
    else:
        narrator "两枚游戏币都已经换成刚才那局游戏，口袋里没有留下金属的重量。门外的雨落在商场台阶上，今天花掉的东西也已经有了准确的位置。"
    scene bg mall_entrance_rain_night
    narrator "我没有拉着她加快脚步。自动门在身后合上，屏幕和名字一起熄灭；我仍记得她按下确认前停过的那一瞬，也记得两枚币最后去了哪里。"
    show char lu mingfei look_at_palm as visual_pose
    narrator "商场门口的感应灯亮了又灭。雨水顺着台阶一级级流下去，街机区的音乐被玻璃门隔在里面，只剩一点模糊的低音。我站到门外才发现自己一直握着拳，掌心里刚才压过的硬币纹路还没退。"
    hide visual_pose
    narrator "绘梨衣把肩上的包带往里拉了拉，站在雨棚下等自动门合拢。她没有回头要求我展示选择的结果，我也没有主动翻开口袋把它演成证明。"
    if "day2_save_second_token" in current_choice_history():
        narrator "我把口袋拍了一下，听见一声很轻的金属响。她听见了，目光停在我外套上，又移到街对面的站牌。那目光没有形成一句话，我也没有逼她把它变成路线。"
    else:
        narrator "我把手从空口袋旁移开。没有金属声，也没有需要被包装成路线的东西。她的目光越过我的外套，停在街对面的站牌上。"
    narrator "我问：“先去站牌那边？”"
    narrator "绘梨衣看了看台阶上的水，沿着边缘走下去。我撑开伞跟上，将伞面往她那边偏了偏。"
    narrator "雨点密密地敲在头顶。走出几步，耳边那段游戏音乐才渐渐散去。鞋面已经湿了，风一吹，有些凉。"
    narrator "站牌的玻璃上满是水，车次被遮住一半。我用袖口擦出一个角。她靠近看，收据从袋口露出白边，又被她按回去。"
    narrator "“等车，还是走一段？”"
    narrator "她抬头看了一眼电子屏，随后转向街口。我换了只手握伞，跟着走过去。"
    narrator "过街时，商场最后一盏灯在身后熄了。水坑里映着的招牌也暗下去，只剩街口那台贩卖机还亮着。"
    narrator "围墙上贴着褪色的比赛海报，下沿被雨泡得卷起。她在那张海报前停了几秒。我也停下来，雨水顺着伞骨落到脚边。"
    narrator "远处有人拉下店铺的铁门，声音拖得很长。她肩头微微一紧，抬眼看了过去。等那声响落下，才又往前走。"
    narrator "一辆夜班车从身后驶过。她看着车尾，红灯绕过拐角，消失了。我把伞压低一点，挡住车道上卷来的风。"
    narrator "雨渐渐小了，只有路灯下还看得见细线。我们走进一条安静些的街，脚步声从雨里慢慢露出来。"
    narrator "我说：“前面还有灯。慢慢走。”"
    narrator "她抬头望了一眼，拉紧包带。我举高伞沿，路灯的光便落到她肩上，又随着脚步一点点移开。"
    narrator "屋檐下的砖干一些，鞋底不再溅起水。我放慢脚步，听着伞上的雨，和她一起往前走。"
    return
