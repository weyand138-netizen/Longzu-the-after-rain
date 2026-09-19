default resource_service_exit = False
default event_shared_cost_promised = False
default event_note_preserved_by_erii = False


label prologue_start:
    $ current_chapter = "prologue"
    scene bg rain_platform
    with dissolve_slow

    narrator "雨把站台上的灯切成许多段，积水也映照这两人的倒影。"
    show crowd rain_platform left_near as prologue_rain_platform_crowd_left_near
    show crowd rain_platform left_far as prologue_rain_platform_crowd_left_far
    show crowd rain_platform right_far as prologue_rain_platform_crowd_right_far
    show crowd rain_platform right_near as prologue_rain_platform_crowd_right_near
    narrator "我把湿透的车票攥在掌心。广播正在报下一班车，身后的人群不时望向我们；他们真的是在等车吗。"
    narrator "绘梨衣没有在意人群，只是轻轻拉住我的袖口。"
    show char erii paper_observation as erii_paper_observation
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "她低头看着脚边，一张被雨打湿的纸贴在地面上。"
    hide erii_paper_observation
    show char lu mingfei look_erii as lu_mingfei_paper_observation
    show char lu mingfei paper_observation as lu_mingfei_paper_observation
    hide lu_mingfei_paper_observation
    show char lu mingfei neutral as lu_mingfei_dialogue
    show char erii neutral as erii_dialogue
    show char lu mingfei paper_side as lu_mingfei_dialogue
    narrator "雨水从站棚边缘一滴一滴落下，打在纸面上使墨迹散开。看着纸上我仍能辨认的几笔。"

    narrator "没人关心我们的注意力在一张纸上。广播重复了一遍车次，我们得尽快上车了。"
    show char lu mingfei pick_up_wish_paper as lu_mingfei_dialogue
    if not persistent.sys_persist_state["settings"]["reduced_motion"]:
        with dissolve_slow
    narrator "我把这张被打湿了的纸捡了起来。这张纸或许有些重要。"
    narrator "绘梨衣的袖口被雨打湿了一圈。她没有在意袖口，只把目光留在纸上。"
    narrator "站棚上的灯又闪了一下。水面里晃出我的脸，也晃出她站在我身后的影子。她没有靠得更近，只用鞋尖抵住一块松动的地砖，像是怕我一伸手就把纸冲进沟里。这个动作很小，我便把手伸得慢了一点。"
    narrator "常言道：管他的，先拿了再说。"
    show char lu mingfei inspect_wish_paper as lu_mingfei_dialogue
    narrator "纸上的墨被雨稀释成深浅不一的蓝黑色。有几处笔画被水拖得很长，应该是写字的人中途停过笔。我不知道那是名字、日期还是一段被划掉的话。"
    show char lu mingfei offer_wish_paper as lu_mingfei_dialogue
    narrator "我抬头问了一句：\"这是你的吗？\""
    narrator "绘梨衣没有马上出声。她先看着纸，又看向我伸开的手掌，最后把食指向下点了一下。那不是我熟悉的完整回答，但她的指尖确实落在纸的方向，应该是她的吧。"
    narrator "我把纸举到灯下。站台的白光很冷，照得墨迹比刚才清楚一点，也照得空白格外明显。我没有问她为什么空着，更没有说我能替她补完。她把视线停在那些空白上，我便把纸停在原处，等着她的回应。"
    narrator "抬头看一眼远处的检票闸机。人群已经散得差不多，广播开始念最后一次候车提醒。不能再等了得尽快上车"
    narrator "我把车票垫在下面，看向她问到：\"现在仔细看看，还是先上车再说？\""
    narrator "她看着我，没有点头，也没有摇头，只把纸边往我这边推了一点。"
    menu:
        "先读那张被雨打湿的纸":
            $ apply_choice("prologue_read_note", {"understanding": 1})
            show prop wish_paper as prologue_wish_paper_detail
            if not persistent.sys_persist_state["settings"]["reduced_motion"]:
                with dissolve_slow
            narrator "纸上只有七个计划，字迹被水晕开了一半。看起来像是愿望清单"
            narrator "最下面一行还能依稀认出：在没有人认识我们的地方，玩一整晚游戏。"
            lm "这是你写的？"
            erii "嗯。"
            hide prologue_wish_paper_detail
            if not persistent.sys_persist_state["settings"]["reduced_motion"]:
                with dissolve_slow
            narrator "她点点头，又用指尖指向纸上几行没有完成的空白。"
            narrator "那张纸像是她的愿望，我应该怎么办。"
            narrator "我没有急着把纸拿近。水迹把日期和地点冲成模糊的一团，剩下的字却都指向一些小事。"
            narrator "一枚游戏币、一盏不必整夜亮着的灯，还有一行被她反复涂黑的段落。"
            narrator "绘梨衣用指尖沿着空白轻轻抚摸了一下，又迅速把手收回。她没有解释纸上的内容，看着我的眼睛摇了摇头。"
            narrator "我把那一页停在雨棚的光里，没有替她念出被水冲掉的部分。能读出的字已经足够让我知道，这不是一张等我补充空白的纸。"

        "先催她上车，离开这里再说":
            $ apply_choice("prologue_hurry_to_train", {})
            lm "先走。等安全了，我们再看。"
            narrator "绘梨衣点头，把纸折小，藏进袖口。"
            $ event_note_preserved_by_erii = True
            narrator "看着她收纸，我忽然有些后悔说了那句“以后”。"
            narrator "广播又响了。她按紧袖口，才跟着我往前走。"

    narrator "列车进站的风从隧道里涌出来。绘梨衣抬头望向线路图。"
    narrator "几条线路在同一站交汇。走东线最快，也少换一趟车。"
    narrator "她的手指沿着另一条线缓缓移动，在一座小站旁停下。"
    narrator "我顺着她的指尖看过去。那地方有什么？"
    narrator "东线还有三分钟，那条支线却要等十七分钟。头顶的倒计时还在跳。"
    narrator "水珠从她的发尾滴下来。她抬起袖口擦了擦，又看回地图。"
    narrator "我正想催她，见她的手还停在图边，话便卡在了嘴里。"

    menu:
        "问她想去哪里":
            $ apply_choice("prologue_ask_destination", {})
            lm "你来选。今天先去哪？"
            narrator "她回头看我，疑惑地歪了歪头。"
            lm "真的。你想去哪。"
            narrator "她看了很久，最终指向刚才那座小站。"

            menu:
                "去她选择的地方，即使要多花一小时":
                    $ apply_choice("prologue_accept_destination", {"autonomy": 1})
                    $ grant_local_achievement("CHOICE_ASK_FIRST")
                    lm "就去那里。多花点时间也没关系。"
                    narrator "她等我看清换乘方向，才轻轻点头。"
                    narrator "她把换乘站名抄在愿望纸背面，看了好一会儿。"
                    narrator "检票提示响起。我收好车票，跟着她往前走。"

                "还是改走更快的东线":
                    $ apply_choice("prologue_override_destination", {})
                    lm "先走东线。等安全了，再去你看的那个地方。"
                    narrator "她的手在小站旁停了一下，随后挪向东线的换乘点。"
                    narrator "我又说了“等安全了”，却没说那是什么时候。"

        "替她选最快离开市区的路线":
            $ apply_choice("prologue_choose_route", {})
            lm "走东线。换乘少，更难被堵住，也更加安全。"
            narrator "她点了点头，把手从地图边收回来。"
            narrator "我记下换乘时间。她仍望着站棚外，没有再指哪一站。"

    scene bg ticket_gate
    with dissolve

    narrator "检票口前，坏掉的监控灯还在闪。旁边的维修门贴着封条，一个男人背对时刻表站着。"
    narrator "绘梨衣停在闸机旁，鞋尖避开地上的红泥。"
    narrator "两道闸机还开着，左边的过道却被清洁车堵住了。我又看了一眼右侧的维修门。"
    narrator "那男人没带行李，伞尖还在滴水，鞋边沾着红泥。他是在等我们吗？"
    narrator "我低声提醒她：\"那边的泥不对。\""
    narrator "她顺着看过去，又指了指维修门旁的告示。"
    narrator "维修日期是今天。封条很新，锁孔边却满是旧划痕。"
    narrator "广播叫到我们的车次，身后有人催促。我摸出车票，抹掉背面的水。"
    narrator "来不及细看了，先记下一件。"

    menu:
        "记住维修门的位置":
            $ apply_choice("prologue_notice_service_exit", {"preparation": 1})
            narrator "锁已经旧了。真要逃的时候，这扇门或许用得上。"
            $ resource_service_exit = True
            narrator "绘梨衣用鞋尖量了量门缝到墙角的距离，回头示意我看。"
            narrator "我把门的位置和编号记在车票背面。"

        "对照红泥，并把追踪方向指给她看":
            $ apply_choice("prologue_notice_tracker", {"truth": 1})
            narrator "东京连下三天雨，市区没有这种干燥的红泥。同色的鞋印从东侧入口一直延到男人脚下。"
            lm "红泥从东边延到这里。他不是临时发现我们的，也知道我们往哪边走。"
            narrator "绘梨衣顺着看过去，并起两根手指，朝相反方向轻轻一推。"
            lm "嗯。换方向，但不瞒你。"
            narrator "她又指了指耳朵。广播正在报下一班车，我抬头记下时间。"

        "告诉绘梨衣：如果出事，我们一起决定":
            $ apply_choice("prologue_promise_cost", {})
            lm "如果他们追上来，你不用听我的命令。我们一起决定。后果也一起担。"
            narrator "绘梨衣翻过我的手，将掌心覆在上面。"
            $ event_shared_cost_promised = True
            erii "嗯。"
            narrator "她的手很凉，握了一会儿才松开。那男人还站在原处，我们该走了。"

    scene bg train_window
    with dissolve_slow

    narrator "车门关闭。东京被雨推向玻璃另一侧。"
    narrator "绘梨衣把愿望纸摊在膝上，慢慢压平折痕。"
    narrator "她比了个七，又指向窗外远去的站台。"
    lm "你问七天够不够？"
    narrator "她点头。"
    lm "不知道。"
    narrator "我看着她，没能补上一句“没问题”。"
    lm "但第一天从现在开始。"
    narrator "她收回手，拇指压住纸角。车轮声渐渐盖过了雨声。"
    narrator "列车钻进隧道。检修灯从窗外掠过，车厢里没人注意我们。"
    narrator "我问：\"冷吗？\""
    narrator "她把手缩进袖口。我将外套放在座位之间，她伸手就能拿到。"
    narrator "我跟着车轮声数了几下，到第七声停住。七天，够做多少事？"
    narrator "我说：\"想换车时，告诉我。\""
    narrator "她低头展开路线图。我把车票翻到背面，又看了一遍换乘站名。"
    narrator "手机在口袋里震动。我调成静音，反扣在腿上。"
    narrator "列车驶上桥，雨声忽然重了。她靠近车窗，呼吸在玻璃上留下一小片白雾。"
    narrator "过了一会儿，她重新摊开愿望纸，指尖从第一行慢慢划到最后一行。"
    narrator "我说：\"想做哪件，指给我就好。\""
    narrator "她停在空白处，最终把纸折好，收回袖口。我没再追问。"
    narrator "列车减速，她抬头看站名。我拉好背包，等她起身。"
    narrator "门开了又关。她仍坐在窗边，我便靠回椅背，陪她等下一站。"

    $ unlock_memory("PROLOGUE")
    call notification_presentation_safe_boundary
    call screen chapter_complete(
        "序章完成",
        "请谨慎选择",
    )
    return
