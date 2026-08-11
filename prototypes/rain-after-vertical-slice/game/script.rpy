# VERTICAL SLICE - NOT FOR PRODUCTION
# Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality?
# Date: 2026-07-23

label splashscreen:
    scene bg slice_black
    centered "{size=38}垂直切片 · 非正式游戏代码{/size}\n\n免费、非商业、非官方同人作品。\n本切片不使用官方美术、音乐、Logo 或原著段落。"
    pause 1.2
    return

label start:
    jump slice_start

label slice_start:
    $ reset_slice_state()
    scene bg slice_platform
    with fade_rain

    narrator "雨从站台外斜着压进来，落在轨道、长椅和每一块来不及干的地砖上。"
    narrator "广播重复了两遍：末班车将在一分钟后进站。"
    narrator "路明非没有回头。玻璃倒影里，那几个撑黑伞的人也没有看时刻表。"
    narrator "绘梨衣站在半步之外，轻轻拉住他的袖口。"
    narrator "她没有开口，只把目光移向排水沟旁的一张纸。"

    menu:
        "先捡起那张被雨打湿的纸":
            $ apply_slice_choice("read_note", {"understanding": 1})
            $ unlock_observer_achievement()
            narrator "纸很薄，沾在金属格栅上。路明非用车票边缘把它一点点挑起来。"
            narrator "上面写着七件小事。字迹被水晕开，只剩最后一行还能认出："
            journal "在没有人认识我们的地方，玩一整晚游戏。"
            lm "这是你写的？"
            erii "嗯。"
            narrator "她点过头，又用指尖按住纸上几行没有完成的空白。"
            narrator "那张纸像是愿望，也像是她自己。"

        "先带她去站台尽头，离开监控范围":
            $ apply_slice_choice("move_to_cover", {})
            lm "先换位置。那边的灯坏了。"
            narrator "绘梨衣跟上来，却在经过排水沟时弯腰捡起了那张纸。"
            narrator "她把它折得很小，收进袖口。"
            narrator "路明非忽然觉得，“以后再看”不是一个可以随便使用的答案。"

    narrator "列车进站前的风从隧道里涌出来。路线图在头顶轻轻摇晃。"
    narrator "路明非已经算好最快的换乘：东线，两站后转地下通道。"
    narrator "绘梨衣抬头看着另一条线路。那一站没有换乘，也不在他的计划里。"

    menu:
        "把路线图转向她：你想去哪？":
            $ apply_slice_choice("ask_destination", {"autonomy": 1})
            lm "你来选。今天先去哪？"
            narrator "她的手停在线路图前，先看那些站名，又回头看他，像在确认这不是另一道命令。"
            lm "真的。选错了，就再换一班。"
            narrator "她沿着线路移动了很久，最后按住一座不起眼的小站，又在玻璃上画了一道波浪。"
            lm "名字像会有海？"
            narrator "她点头。"
            lm "地图上没有海。"
            narrator "她仍按着那座站，没有把手收回去。"

        "告诉她最快路线：跟紧我":
            $ apply_slice_choice("choose_fast_route", {})
            lm "走东线。换乘少，他们来不及封住第二个出口。"
            narrator "她立刻点头。快得让这个动作更像一次服从，而不是一次选择。"
            narrator "路明非把那张路线图记住，却没能把这个念头甩掉。"

    scene bg slice_gate
    with dissolve

    narrator "检票口只亮着一半。坏掉的闸机反复闪红，像一只不肯闭上的眼睛。"
    narrator "雨水从玻璃幕墙流下来。大厅里有三件事不对劲。"
    narrator "封条很新的维修门；一个从不看屏幕的男人；还有绘梨衣没有松开的手。"
    narrator "列车提示音响起。时间只够他真正记住一件。"

    menu:
        "记住维修门和旧锁的位置":
            $ apply_slice_choice(
                "notice_service_door",
                {"preparation": 1},
            )
            narrator "封条刚贴不久，门轴却锈得厉害。旁边的消防箱能挡住监控死角。"
            narrator "如果站台被堵住，这里也许会成为第二条路。"

        "记住男人鞋底不属于车站的红泥":
            $ apply_slice_choice("notice_tracker", {"truth": 1})
            narrator "东京连下三天雨，市区的泥都是黑的。那双鞋却带着干燥的红色粉末。"
            narrator "他不是临时发现他们。他从更远的地方一路跟来。"

        "对绘梨衣说：如果出事，我们一起决定":
            $ apply_slice_choice("promise_shared_cost", {})
            lm "如果他们追上来，你不用等我的命令。"
            narrator "她看着他，没有点头。"
            lm "我们一起决定。后果也一起担。"
            narrator "她把他的手翻过来，将自己的手掌覆在上面。"
            erii "嗯。"

    narrator "闸机亮起绿色。两个人穿过去时，身后的脚步声忽然快了。"
    narrator "路明非没有回头。回头不会让距离变远。"
    narrator "他听见绘梨衣的呼吸仍然很稳，于是也把自己的脚步压回正常速度。"
    narrator "车门在他们身后合拢。黑伞被留在玻璃外，变成雨里模糊的影子。"

    scene bg slice_train
    with fade_warm

    narrator "车厢几乎是空的。城市的灯在雨窗上拖成长线，一闪就不见了。"

    if "read_note" in choice_history:
        narrator "绘梨衣把那张被救回来的纸铺在两人之间的座位上。"
        narrator "她压平折痕，指了指完好无损的最后一行。"
        lm "没丢。第一件愿望也没有。"
        $ add_payoff("你停下来读了愿望纸，所以它现在摊在两个人之间。")
    else:
        narrator "绘梨衣从袖口取出那张纸。折痕把最后一行从中间切开。"
        narrator "她把纸举到路明非面前，等他看清，才重新收好。"
        lm "……下次提醒我别把重要的东西留给以后。"
        $ add_payoff("你先选择安全，她则替自己保存了那张愿望纸。")

    if "ask_destination" in choice_history:
        narrator "她把车票接过去，没有交还给路明非，而是自己放进口袋。"
        narrator "她先点了点车票上的站名，又轻轻碰了一下他的肩。"
        lm "到了那一站，你叫我？"
        narrator "她点头。"
        lm "好。今天听你的。"
        $ add_payoff("她保管了车票，因为目的地是她亲手选的。")
    else:
        narrator "她用指尖在车票上划过两站，又在换乘标记处转了一个方向。"
        lm "东线，两站，地下通道。你都记住了。"
        narrator "她点头，动作和刚才接受安排时一样快。"
        narrator "这本来应该让人放心。路明非却第一次觉得，被完全相信也可能是一种危险。"
        $ add_payoff("她用动作准确复现了你的计划，也让“替她决定”的重量变得可见。")

    if "notice_tracker" in choice_history:
        narrator "列车驶过下一座站台时，路明非看见玻璃倒影里没有那双沾红泥的鞋。"
        lm "他没上来。但他知道我们往哪个方向走。"
        narrator "绘梨衣看向车厢后方，又慢慢摇头。"
        lm "只是多了一点时间。"
        $ add_payoff("红泥线索确认了追踪并未结束，只为两人换来一点时间。")
    elif "notice_service_door" in choice_history:
        narrator "绘梨衣碰了碰他指腹沾到的铁锈，又用两根手指比出门轴开合的样子。"
        lm "你也看见那把旧锁了？"
        narrator "她点头，接着指了指他的眼睛，又指向自己。"
        narrator "那条备用路线现在不只存在于一个人的脑子里。"
        $ add_payoff("维修门成为两个人都知道的备选出口。")
    else:
        narrator "她把两张车票并排放好，一只手按住一张，然后让两只手在中间合拢。"
        lm "后果，是我们的。"
        erii "嗯。"
        narrator "这声确认不像安慰，更像一份刚刚成立的约定。"
        $ add_payoff("一句承诺变成共同约定，而不是英雄式的单方面保护。")

    narrator "雨还没有停。东京也没有因此变得安全。"
    narrator "但路线图、车票和那张湿纸第一次不全握在路明非一个人手里。"
    narrator "绘梨衣向他展开七根手指，又指了指窗外飞快退后的站台。"
    lm "你问七天够不够？"
    narrator "她点头。"
    lm "不知道。"
    narrator "他没有把“不知道”说成“没问题”。"
    lm "但第一天，从现在开始。"

    $ persistent.slice_memory = slice_memory_summary()
    $ renpy.save_persistent()
    call screen slice_complete("\n".join(payoff_lines))
    return
