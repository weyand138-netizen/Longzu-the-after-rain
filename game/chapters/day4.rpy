init python:
    # Build-time inputs only. No Day 4 partial or terminal manifest is created here.
    DAY4_SOURCE_UNIT_ID = "chapter_day4_seaside_train"
    DAY4_REQUIRED_SCENE_IDS = (
        "scene_day4_ticket_counter",
        "scene_day4_route_answer",
        "scene_day4_contact_channel",
        "scene_day4_sea_window",
    )
    DAY4_CHOICE_RECORDS = (
        (
            "day4_buy_two_tickets_real_name",
            "reaction_day4_buy_two_tickets_real_name",
            "payoff_day4_two_tickets_day6",
        ),
        (
            "day4_buy_single_ticket_cash",
            "reaction_day4_buy_single_ticket_cash",
            "payoff_day4_single_ticket_ending",
        ),
        (
            "day4_register_independent_contact",
            "reaction_day4_register_independent_contact",
            "payoff_day4_contact_ending",
        ),
        (
            "day4_decline_independent_contact",
            "reaction_day4_decline_independent_contact",
            "payoff_day4_decline_contact_ending",
        ),
        (
            "day4_follow_one_route_no_backup",
            "reaction_day4_follow_one_route_no_backup",
            "payoff_day4_no_backup_day6",
        ),
    )
    DAY4_CHOICE_EFFECTS = {
        "day4_buy_two_tickets_real_name": (
            "preparation",
            "sacrifice",
            "acquire:resource_two_tickets",
            "event:event_identity_exposed",
        ),
        "day4_buy_single_ticket_cash": (
            "preparation",
            "acquire:resource_single_ticket",
        ),
        "day4_register_independent_contact": (
            "truth",
            "consume:resource_arcade_token",
            "acquire:resource_contact_card",
            "event:event_contact_risk_handover_complete",
        ),
        "day4_decline_independent_contact": (
            "revoke:token_abandon_backup_plan",
            "event:event_contact_channel_declined",
        ),
        "day4_follow_one_route_no_backup": (
            "revoke:token_abandon_backup_plan",
        ),
    }
    DAY4_ROUTE_PREPARATION_REQUEST_ID = "event_route_preparation_requested"
    DAY4_ROUTE_PREPARATION_ANSWER_STATE = "preserve_executable_self_controlled_option"
    DAY4_INDEPENDENT_CONTACT_REQUEST_ID = "event_independent_contact_option_requested"
    DAY4_INDEPENDENT_CONTACT_ANSWER_STATE = "keep_independent_contact_option"
    DAY4_PLAYER_SAFE_CATALOG_INPUTS = (
        {
            "catalog_kind": "chapter",
            "catalog_id": "chapter_day4_seaside_train",
            "day_index": 4,
            "observable_fact_ids": (
                "fact_day4_self_controlled_option_presented",
                "fact_day4_ticket_or_contact_option_prepared",
            ),
            "source_unit_id": DAY4_SOURCE_UNIT_ID,
        },
        {
            "catalog_kind": "memory",
            "catalog_id": "memory_day4_seaside_window",
            "day_index": 4,
            "observable_fact_ids": ("fact_day4_self_controlled_option_presented",),
            "source_unit_id": DAY4_SOURCE_UNIT_ID,
        },
    )


default event_identity_exposed = False
default event_two_window_tickets_acquired = False
default cp_day4_two_tickets_complete = False
default event_contact_risk_handover_complete = False
default event_contact_channel_declined = False
default resource_two_tickets = False
default resource_single_ticket = False
default resource_contact_card = False
default agency_day4_route_preparation_request = None
default agency_day4_route_preparation_answer = None
default agency_day4_route_preparation_outcome = None
default agency_day4_independent_contact_request = None
default agency_day4_independent_contact_answer = None
default agency_day4_independent_contact_outcome = None


label chapter_day4_seaside_train:
    $ current_chapter = "day4"
    scene bg station_ticket_window_interior

    # scene_day4_ticket_counter
    narrator "售票窗前只剩一盏低灯。玻璃刚擦过，水痕还没干。绘梨衣把路线图、联系人纸片和零钱摆在灯下。"
    narrator "她把硬币按大小排成一列，纸币压住地图的一角。最小的那枚滚向金属槽，被她用指尖挡了回来。"
    narrator "收据从她的夹层里露出来。她取出放在图旁，名字上横着一道折痕。"
    narrator "窗口里响着翻票本的声音。我把证件从钱包里抽出一半，又按住。玻璃上映着我的脸，恰好盖住地图上的小站。"
    narrator "我问：“这些，哪样要留给你？”"

    # scene_day4_route_answer
    $ agency_day4_route_preparation_request = DAY4_ROUTE_PREPARATION_REQUEST_ID
    narrator "她用指尖分别压住车次、窗口座位和联系人纸片。每碰一处，都停一下，等我看清。"
    $ agency_day4_route_preparation_answer = DAY4_ROUTE_PREPARATION_ANSWER_STATE
    narrator "我把地图摊平。她的手留在纸边，窗口里的笔也停了。"
    narrator "“两张靠窗票，要登记我的名字和车次。”我把证件放到灯下，“有人查记录，就能知道我们来过这里。”"
    narrator "“单人票用现金，不记名字。只有一个座位。”说到这里，我看了一眼她的手。她仍压着地图。"
    narrator "我又指向那张小纸片：“联系人要用你选的昵称。登记以后，也可能被顺着号码找到。”"
    narrator "广播催了一遍。绘梨衣把联系人纸片从地图下面抽出来，仍和车次、座位摆在一起。我低头重新数了数零钱。"
    $ critical_choice_interaction = True

    menu:
        "用真实姓名买两张靠窗票，交给她自己保管":
            $ critical_choice_interaction = False
            $ apply_choice("day4_buy_two_tickets_real_name", {"preparation": 1, "sacrifice": 1})
            narrator "两张靠窗票落进她掌心。售票员照着证件记下姓名和车次，笔尖停了一下。我看见自己的名字留在了本子上。"
            $ resource_two_tickets = True
            $ event_identity_exposed = True
            $ event_two_window_tickets_acquired = True
            $ cp_day4_two_tickets_complete = True
            $ agency_day4_route_preparation_outcome = "outcome_shared_option_prepared"
            show story lu_present_identity
            narrator "证件从窗口推回来，我收进钱包。绘梨衣把两张票错开，先看姓名，再看座位号。"
            show story erii_arrange_route
            narrator "票上的小字印得很密，她举到灯下，看了好一会儿。"
            narrator "我问：“放哪里？”"
            narrator "她打开路线图，把两张票塞进折痕内侧，再收进自己的夹层。我合上钱包，手里忽然空了。"
            narrator "站台广播又报了一遍车次。她抬头听着，指尖还按在夹层边上。我也想看看那两张票，最后只问了句：“收好了？”"
            narrator "她拍拍夹层，继续站在窗口前。"
            hide story

        "买一张现金票，让她决定是否独自上车":
            $ critical_choice_interaction = False
            $ apply_choice("day4_buy_single_ticket_cash", {"preparation": 1})
            narrator "现金推过窗口，换回来一张票。绘梨衣接过去，把路线图折到能独自展开的那一页。"
            $ resource_single_ticket = True
            $ agency_day4_route_preparation_outcome = "outcome_solo_option_prepared"
            narrator "她核对开车时间和座位号，把单人票夹在收据后面。两张纸一新一旧，边缘没有叠齐。"
            show story erii_arrange_route
            narrator "她沿着图上的线看过去，手指停在一个站名旁。我把挡住那处的折角抚平。"
            narrator "找零落进金属槽，叮当响了几声。我逐枚捡起，放回口袋。手心里只剩硬币的凉意。"
            narrator "“票你收着。”我说。"
            narrator "她把收据后露出的票角推好，扣上夹层。我本来想问她会不会用，到嘴边，又停了。"
            narrator "售票员还等在玻璃后。我挪开手，把柜台上的空处让出来。"
            hide story

        "只按眼前的路线走，不再留下另一种准备":
            $ critical_choice_interaction = False
            $ apply_choice("day4_follow_one_route_no_backup", {})
            narrator "我没有买票。绘梨衣折起路线图，把两条划掉的支线压在里面，正面只剩下一条。"
            $ agency_day4_route_preparation_outcome = "outcome_self_controlled_option_not_prepared"
            narrator "联系人纸片滑到图边，她拿起来，暂时收进袖口。"
            narrator "我看着那两条线消失在折痕里。图薄了许多，攥在手里倒比刚才紧。"
            narrator "“没另外买票。”我说。"
            narrator "她低头把图折好，没有接话。窗口里的票本翻过一页，我的零钱还原样放着。"

    # scene_day4_contact_channel
    if (
        "day2_save_second_token" in current_choice_history()
        and (
            "day2_accept_alias" in current_choice_history()
            or "day2_admit_alias_unknown" in current_choice_history()
        )
    ):
        $ agency_day4_independent_contact_request = DAY4_INDEPENDENT_CONTACT_REQUEST_ID
        narrator "绘梨衣把那枚留下的游戏币放到柜台上，又在联系人纸片上写下先前的昵称。她将两样东西推到窗口前，抬眼看我。"
        $ agency_day4_independent_contact_answer = DAY4_INDEPENDENT_CONTACT_ANSWER_STATE
        narrator "游戏币滚了一小圈，停在纸边。她用手指挡住，另一只手展开背面的折痕。"
        narrator "上面的字很小。我俯身念给她听：登记后可以通过这个号码联络，也可能被人顺着记录追查。"
        narrator "她把纸转向灯光，将那几行字从头看了一遍。游戏币压在空白处，边缘已经磨得发亮。"
        narrator "“用这个名字？”我问。"
        narrator "她点了点自己写下的字，又把纸往窗口推近了一点。游戏币还在她指边。"
        $ critical_choice_interaction = True

        menu:
            "用她保留的昵称和游戏币登记独立联系人":
                $ critical_choice_interaction = False
                $ apply_choice("day4_register_independent_contact", {"truth": 1})
                narrator "她自己念出昵称的读法，把游戏币交进窗口。金属轻响了一声，联系人卡从玻璃下推出来。她翻到背面，把风险说明看完，才拿起卡。"
                $ resource_contact_card = True
                $ event_contact_risk_handover_complete = True
                $ agency_day4_independent_contact_outcome = "outcome_independent_option_prepared"
                narrator "工作人员问她是否确认。她用指尖点了点卡上的名字，再把背面那几行小字转向我。"
                narrator "“要我记哪一条？”"
                narrator "她指着最下面的时限。我读了一遍，她才把说明折好，连同卡片收进自己的夹层。"
                narrator "柜台上少了那枚游戏币，空出一个很小的位置。那天机台的声音忽然在脑子里响了一下，很快又被站台广播盖过去。"

            "不登记联系人，让她把游戏币和纸片收回去":
                $ critical_choice_interaction = False
                $ apply_choice("day4_decline_independent_contact", {})
                narrator "她把游戏币和写着昵称的纸片收回掌心。窗口没有递出联系人卡，号码也没有登记。"
                $ event_contact_channel_declined = True
                $ agency_day4_independent_contact_outcome = "outcome_independent_option_declined"
                narrator "她把昵称折在里面，用纸包好游戏币。金属隔着薄纸，顶出一圈圆边。"
                narrator "售票员收走空白卡片。我望着玻璃下腾出的地方，半晌才把手拿开。"
                narrator "“收好。”我说。"
                narrator "她把纸和币放回口袋，按平袋口。隔着玻璃，售票员已经低头去翻下一本册子。"
    else:
        narrator "柜台上还缺登记用的东西。那张联系人纸片没有递进去，绘梨衣将它折好，收回袖口。"

    # scene_day4_sea_window
    scene bg seaside_station_window
    narrator "列车进站的风吹起地图一角。绘梨衣把它收好，走到黄线前。车灯沿着玻璃扫过去，照亮了她的袖口。"
    narrator "“东西都在？”我问。她拍了拍口袋。"
    narrator "车门打开，几个提行李的人先下来。她等人走空才上车，我落在后面半步。"
    narrator "门边靠着一把湿伞，水沿伞尖滴下来。她抓住扶杆，在晃动的车厢里站稳。"
    scene bg coastal_train_dawn
    narrator "列车开动，站台的灯向后退去。门边的人散开后，绘梨衣走到窗前，手在椅背上停了一下，坐了下来。"
    narrator "我坐在过道另一边。她把路线图摊在膝上，纸角随着车厢颠动，被她轻轻按住。"
    narrator "玻璃上蒙着雾。她用指尖擦出一小块，外面灰蓝色的水面闪了一下，又被信号灯遮住。"
    narrator "我将钱包往口袋深处塞了塞。证件还在最里层，边角抵着掌心。"
    if event_identity_exposed:
        narrator "售票员写下的那行名字，却留在了身后的车站。车走得越远，我越想回头看看。"
    narrator "窗外掠过一个小月台，灯只照着空椅子。有人拖着行李经过，她把膝盖往里收，我也收好脚。"
    narrator "车驶上桥，桥下的水亮起来。绘梨衣俯身靠近玻璃，额前的碎发碰到窗上。"
    narrator "“冷吗？”我问，“要往里坐一点吗？”"
    narrator "她把手从玻璃上移开，仍坐在那里。我靠回椅背，听着车轮一下一下压过接缝。"
    narrator "隧道吞没了窗外的水。黑玻璃里浮出车厢的灯，我们隔着过道，各有一个模糊的影子。"
    if event_identity_exposed:
        narrator "我又想起登记本上的车次，下意识摸了摸钱包，抬头看向车门。门边只有几个打盹的旅客。"
    narrator "广播报出下一站。绘梨衣将地图折回原样，抬头听了一会儿。"
    narrator "“要下去吗？”我问。她先看向门口，没有立刻起身。"
    narrator "车慢下来，站牌从薄雾里露出。她走到门边，我也跟过去。冷风钻进车厢，她望着外面的灯，停了片刻。"
    narrator "提示音再次响起。她退回座位，把地图放到膝上。门在身后合拢。"
    if event_identity_exposed:
        narrator "我的手还搭在钱包上，过了一会儿，才松开。"
    narrator "列车重新开动，站灯被拉成一条细线。她用袖口擦去玻璃上新起的雾，低头收好地图。"
    narrator "我有些困了，却舍不得闭眼。隧道出口的光正在变亮，海线又从她肩后露出来。"
    narrator "她望着窗外。我也转过头，等那片灰蓝色的水面绕过山脚，慢慢铺开。"
    return
