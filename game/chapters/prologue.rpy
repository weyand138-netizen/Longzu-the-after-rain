label prologue_start:
    $ current_chapter = "prologue"
    scene bg rain_platform
    with dissolve_slow

    narrator "雨把站台上的灯切成许多段。每一段都落在积水里，像一条走不通的路。"
    narrator "路明非把湿透的车票攥在掌心。广播正在报下一班车，身后的人群却没有谁真的在等车。"
    narrator "绘梨衣没有催他，只是轻轻拉住他的袖口。"
    narrator "她低头看着脚边，一张被雨打湿的纸贴在排水沟旁。"

    menu:
        "先读那张被雨打湿的纸":
            $ apply_choice("prologue_read_note", {"understanding": 1})
            narrator "纸上没有求救，也没有路线。只有七件小事，字迹被水晕开了一半。"
            narrator "最下面一行还能认出来：想在没有人认识我们的地方，玩一整晚游戏。"
            lm "这是你写的？"
            erii "嗯。"
            narrator "她点过头，又用指尖按住纸上几行没有完成的空白。"
            narrator "那张纸像是愿望，也像是她自己。"

        "先催她上车，离开这里再说":
            $ apply_choice("prologue_hurry_to_train", {})
            lm "先走。等安全了，我们再看。"
            narrator "绘梨衣点头，却弯腰把那张纸捡了起来。她把它折得很小，藏进袖口。"
            narrator "路明非忽然意识到，“以后”可能不是一个可以随便使用的词。"

    narrator "列车进站的风从隧道里涌出来。绘梨衣抬头望着线路图，像在看一张没有图例的地图。"

    menu:
        "问她想去哪里":
            $ apply_choice("prologue_ask_destination", {})
            lm "你来选。今天先去哪？"
            narrator "她的手停在线路图前，回头看他，像在确认这不是另一道命令。"
            lm "真的。选错了就再换一班。"
            narrator "她看了很久，手指最终停在一座并不起眼的小站上，没有再移开。"

            menu:
                "照她选的小站走，即使要多绕一小时":
                    $ apply_choice("prologue_accept_destination", {"autonomy": 1})
                    $ grant_local_achievement("CHOICE_ASK_FIRST")
                    lm "就去那里。慢一点也没关系。"
                    narrator "绘梨衣把手指留在线路图上，直到他也看清换乘的方向，才轻轻点头。"

                "还是改走更快的东线":
                    $ apply_choice("prologue_override_destination", {})
                    lm "先走东线。等安全了，再去你选的地方。"
                    narrator "她收回手，线路图上那座小站重新变成了一个没有被回答的名字。"

        "替她选最快离开市区的路线":
            $ apply_choice("prologue_choose_route", {})
            lm "走东线。换乘少，也更难被堵住。"
            narrator "她立刻点头。太快了，快得让这个动作更像服从而不是选择。"

    scene bg ticket_gate
    with dissolve

    narrator "检票口前有三件不对劲的东西。坏掉的监控灯、贴着封条的维修门，还有一个从不看时刻表的男人。"
    narrator "广播开始倒数。路明非只能把其中一件事牢牢记住。"

    menu:
        "记住维修门的位置":
            $ apply_choice("prologue_notice_service_exit", {"preparation": 1})
            narrator "封条是新的，锁却很旧。真要逃的时候，那里或许比站台更可靠。"

        "对照红泥，并把追踪方向指给她看":
            $ apply_choice("prologue_notice_tracker", {"truth": 1})
            narrator "东京连下三天雨，市区没有这种干燥的红泥。路明非又看了一眼站台边缘同色的鞋印：那个人从东侧入口一路跟来。"
            lm "红泥从东边延到这里。他不是临时发现我们的，也知道我们往哪边走。"
            narrator "绘梨衣顺着他指的方向看过去，又把两根手指并在一起，朝相反方向轻轻一推。"
            lm "嗯。换方向，但不瞒你。"

        "告诉绘梨衣：如果出事，我们一起决定":
            $ apply_choice("prologue_promise_cost", {})
            lm "如果他们追上来，你不用听我的命令。我们一起决定。后果也一起担。"
            narrator "绘梨衣把他的手翻过来，将自己的手掌覆在上面。"
            erii "嗯。"

    scene bg train_window
    with dissolve_slow

    narrator "车门关闭。东京被雨推向玻璃另一侧。"
    narrator "绘梨衣把那张纸摊在膝上，用指甲慢慢压平折痕。"
    narrator "她向路明非展开七根手指，又指了指窗外飞快退后的站台。"
    lm "你问七天够不够？"
    narrator "她点头。"
    lm "不知道。"
    narrator "这一次，他没有把不知道说成没问题。"
    lm "但第一天从现在开始。"

    $ unlock_memory("PROLOGUE")
    $ renpy.save_persistent()

    call screen chapter_complete(
        "序章完成",
        "有些选择不会立刻告诉你答案。它们会在之后重新出现。",
    )
    return
