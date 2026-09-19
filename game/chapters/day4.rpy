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
    narrator "售票窗前只剩一盏低灯。我看见绘梨衣把路线图、空白联系人纸片和零钱并排放在玻璃下。"
    narrator "她先把路线图推回我面前，再把能自己收下的票和纸片留在手边。"
    narrator "售票员把玻璃窗擦过一遍，留下几道没有完全干透的水痕。路线图上的支线、窗口座位和联系人纸片被水痕切开，却仍然可以被她逐一指出。"
    narrator "我把前几天留下的收据放在路线图旁，没有把它递进窗口。绘梨衣看见名字的折痕，伸手把收据和联系人纸片分开，给每件东西留下独立的位置。"
    narrator "窗内的钟走得比站台广播慢半拍。能买到什么、要留下什么、谁来拿走，先在这块玻璃下变成了几件我能看清的物件。"
    narrator "绘梨衣把零钱按面额排好，最后才把路线图转回我面前。她的动作没有要求我马上回答，却把需要回答的东西全部放到了灯下。"
    narrator "玻璃把我的倒影压在路线图上。我看见她先把零钱和票位分开，便明白至少不能把这些不同的东西说成同一个安排；至于她愿意留下哪一个，我还得等她继续指给我看。"
    narrator "售票窗下的金属槽很窄，零钱滚进去就不容易拿。她把硬币排成一列，最小的推到里面，纸币压在路线图角上。我看着她分开这些东西，没有打乱顺序。"
    narrator "玻璃另一边的售票员偶尔抬眼，等候队伍却只有我们。这样的安静反而让我听见自己的顾虑：实名会留下痕迹，现金票又可能把人推到一条没有同行者的路上。顾虑是真的，选哪种代价却不是可以从顾虑里自动推出的答案。"
    narrator "联系人纸片比车票小很多，边角还留着昨天街机券的折痕。她把它放在路线图旁时，纸片几乎要被图压住。随后她又把它抽出来，摆到玻璃下最亮的那一块。我看见这一点，便没有把它当成一个可以随意丢掉的备用物。"
    narrator "我问：\"这些里，哪一个要留给你自己？\""
    narrator "她先把路线图翻到背面，再把票位指了一下，又用指尖碰到联系人纸片。她没有选出唯一一件，也没有要我替她选。三个动作隔着一点距离，我便把路线图铺平，让她能够继续指，而不是急着把手伸进窗口。"
    narrator "我把证件抽出钱包，又放回去。交出照片和名字，风险先落在我身上；票打出来以后，要不要拿、要不要上车，却得由她决定。这两件事不能混在一起。"

    # scene_day4_route_answer
    $ agency_day4_route_preparation_request = DAY4_ROUTE_PREPARATION_REQUEST_ID
    narrator "她用指尖分别压住车次、窗口座位和联系人纸片，等我看清这些不是替她决定的答案。"
    $ agency_day4_route_preparation_answer = DAY4_ROUTE_PREPARATION_ANSWER_STATE
    narrator "她先压住车次，再压住窗口座位，最后碰了一下联系人纸片。三个动作之间留有间隔，像是在确认它们可以被分别保留，而不是只能被一次性接受。"
    narrator "我把路线图上的折痕展开，让她指过的地方都露出来。过去几天留下的名字、游戏币和维修门没有自动变成路线，只在这张纸上提供了可以核对的背景。"
    narrator "我没有把收据上的名字当成她会同意出发的凭据，也没有把留在口袋里的硬币当成她一定要联系谁的理由。纸上的每个位置都比我的猜测先出现。"
    narrator "我算了一遍票价：两张靠窗票要报姓名，留下车次记录；一张现金票能少留记录，却空出另一个座位。我把这些代价逐条说清，等她回应。"
    narrator "她听着，手指压在路线图边缘。窗口传来翻票本的声音，最后购票时间还在牌子上闪。她没收回纸片，我便继续等，没有拿倒计时催她。"
    narrator "我说：\"两张票会用我的名字。单人票不需要。联系人卡要把你写下的昵称交出去。你想先留哪个，我按你指的做。\""
    narrator "她把票位、联系人纸片和路线图依次碰了一遍，最后把手停在玻璃下。她的指尖没有穿过售票口，我也没有抓着它替她把纸递进去。我们都看得见窗口，却没有谁有权把没有发生的下一步提前写在她手上。"
    narrator "我的名字印在收据上时，她曾经把它折起来留好。现在证件就在我掌心，我不能借那张收据假装她已经答应我用同一个名字买两张票。过去被她保留的物件只能提供回响，不能变成逼她照着走的证据。"
    $ critical_choice_interaction = True

    menu:
        "用真实姓名买两张靠窗票，交给她自己保管":
            $ apply_choice("day4_buy_two_tickets_real_name", {"preparation": 1, "sacrifice": 1})
            narrator "两张靠窗票落进她掌心。售票员核对姓名时停了一下，我知道这会留下被人找到的代价。"
            $ resource_two_tickets = True
            $ event_identity_exposed = True
            $ event_two_window_tickets_acquired = True
            $ cp_day4_two_tickets_complete = True
            $ agency_day4_route_preparation_outcome = "outcome_shared_option_prepared"
            narrator "她先看票面上的姓名，再把两张票错开叠放，让靠窗的位置仍然清楚可见。售票员的停顿没有被解释成偶然，我把自己的证件收回，却没有把票也收回。"
            narrator "她把票放进路线图折出的夹层，手指在夹层边缘停了一秒，确认两张票都在自己能够取到的位置。代价因此跟着票一起被保存，而不是被藏在售票窗后。"
            narrator "我听见打印机吐纸，也看见她没有把其中一张递还给我。那不保证我们会同行，只说明这两张票现在在她能够决定的位置。"
            narrator "售票员把证件推回来时，玻璃下留着一小块潮气。我把证件收进钱包，没有去碰她手里的票。我的名字已经被窗口看见，车次也被记录下来，这些代价先落在我身上；票留在她掌心，能不能使用却不能由我替她决定。"
            narrator "她把两张票错开，先看其中一张的座位，再看另一张。靠窗的位置印得很小，她把票举到灯下，确认两张都没有夹在一起。我没有替她保管其中一张，也没有说这两张票一定会把我们带到同一个地方。"
            narrator "我问：\"票要放哪里？\""
            narrator "她把路线图打开，在折痕内侧塞进两张票，又把夹层扣住。她没有把夹层交给我。我看见票已经在她手里有了位置，便把自己的钱包合上。玻璃窗后的售票员转向下一项工作，留下的姓名却不会因为窗口移开就没有代价。"
            narrator "站台广播开始报车次。她先拍了拍夹层，再看向站台方向。我没有把这解释成她决定同行。我只跟着她走到黄线外侧，等她下一次真正把票拿出来。"
            $ critical_choice_interaction = False

        "买一张现金票，让她决定是否独自上车":
            $ apply_choice("day4_buy_single_ticket_cash", {"preparation": 1})
            narrator "她接过那张票，没有把它塞回我手里，只把路线图折到能一个人展开的那一页。"
            $ resource_single_ticket = True
            $ agency_day4_route_preparation_outcome = "outcome_solo_option_prepared"
            narrator "她把单人票翻到背面，看清开车时间和座位号，再把它夹在收据后面。这个位置让票不会被风吹走，也让她不用现在就宣布是否要使用。"
            narrator "我把路线图剩下的折痕抚平。她没有把票交还，只用指尖沿着能够独自展开的那一页走了一遍。"
            narrator "我把手停在另一页外侧，没有替她补上一张同行的票。单人票在她指下，能说明的只有她已经看见一个由自己打开的方向。"
            narrator "现金找零落到金属槽里，她没有来拿。我把零钱收起，没有把它和票放在一起。票是她手里的方向，零钱只是我还没花掉的东西；把它们混在一起，反而像我还想用自己的钱替这张单人票附带一个她没要的安排。"
            narrator "她把票背面对着我，读了一遍开车时间。票没退回窗口，她也没说要上车。我收住追问，免得她还要替我的担心作答。"
            narrator "我说：\"你要走的时候，票在你这里。\""
            narrator "她把票压进收据后面，指尖停在写着我名字的那一折。我没有说那行名字意味着我该跟着她，也没有拿回收据。两张纸被她自己放在一起，能说明的只是在今天它们都由她保管。"
            narrator "她把路线图折到单人能看懂的一页。纸上没有第二张票，我也没有拿笔去补。她把那一页收好以后，先朝站台走；我落在半步后面，直到她回头或继续往前，都不替她把距离缩成同行。"
            $ critical_choice_interaction = False

        "只按眼前的路线走，不再留下另一种准备":
            $ apply_choice("day4_follow_one_route_no_backup", {})
            narrator "路线图上只剩一条被折出来的线。她把联系人纸片收回袖口，没有替我补上空白。"
            $ agency_day4_route_preparation_outcome = "outcome_self_controlled_option_not_prepared"
            narrator "她折路线图时避开了两条已经被划掉的支线，把剩下的一条压得很深。联系人纸片藏回袖口，边角却仍露出一点，像一条被放弃但没有被忘记的可能。"
            narrator "我看见自己的手停在另一张空白纸片上，随后把手收回。路线变得更简单，能由她保留的选择也因此变少。"
            narrator "我没把“简单”说成“更好”。她把支线压进折痕里，我只能看见纸变薄了一点，不能替她补出那条原本可能通向哪里的路。"
            narrator "联系人纸片露在袖口外的一小角，很快又被她收进去。我没有伸手把它抽出来，也没有说仍然可以临时登记。被放弃的准备在纸上留下的不是一个等我随时反悔的按钮，而是一段我已经没有替她留下的可执行空间。"
            narrator "我把路线图的正面朝她转过去，那里只剩下一条清楚的线。她没有立刻收走，也没有让我按住。她看了一会儿，才把折痕压得更深。我看见的是纸被她折好，不把这说成她赞同我让路线变窄。"
            narrator "我说：\"我没留别的。\""
            narrator "她没有回答。她把路线图放回夹层，纸片仍在袖口。我没有用一句以后再想办法安慰自己，因为没有准备的以后只会在真正需要时显得更空。站台风吹来时，我只帮她挡住飘起的纸角，没去碰她的袖口。"
            $ critical_choice_interaction = False

    # scene_day4_contact_channel
    if (
        "day2_save_second_token" in current_choice_history()
        and (
            "day2_accept_alias" in current_choice_history()
            or "day2_admit_alias_unknown" in current_choice_history()
        )
    ):
        $ agency_day4_independent_contact_request = DAY4_INDEPENDENT_CONTACT_REQUEST_ID
        narrator "那枚留下的游戏币和她自己输入过的昵称还在。她把它们放到联系人纸片旁，抬眼等我回应。"
        $ agency_day4_independent_contact_answer = DAY4_INDEPENDENT_CONTACT_ANSWER_STATE
        narrator "游戏币在玻璃下滚了一小圈，停在纸片边缘。她用手指挡住它，没有让它继续滚到窗口另一端。"
        narrator "联系人纸片背面印着几行很小的字，风险说明被折痕遮住了一半。她先把纸片摊平，再把游戏币压在上面，等所有字都能被看见。"
        narrator "我把纸片上的小字一行行读出来：登记以后，号码可能被追到；不登记，就没有可直接联络的地方。字写得很冷静，像是在描述别人的麻烦。我没有把它读成警告她必须怎么选，只把每个能看见的后果放到她和窗口之间。"
        narrator "那枚游戏币在纸上压出一个圆形阴影。它从昨晚留到今天，金属边缘比我的口袋更暖。她没有把币递给售票员，也没有把它塞回包里，只用一根手指挡着它。我看见她在留住它，至于她是想登记还是想收回，我仍然得问。"
        narrator "我问：\"要把这个名字留在这里吗？\""
        narrator "她把纸片转了半圈，露出昨晚写下的昵称。然后她抬眼看窗口，又看向我。她的手没有离开游戏币。我没有把这个眼神当成把决定交给我；我只是告诉她，卡会放在哪儿，风险字在哪里，等她自己把手伸出去或收回来。"
        $ critical_choice_interaction = True

        menu:
            "用她保留的昵称和游戏币登记独立联系人":
                $ apply_choice("day4_register_independent_contact", {"truth": 1})
                narrator "她自己念出昵称的读法，把游戏币交给窗口后拿走联系人卡，也看完了背面写着的风险。"
                $ resource_contact_card = True
                $ event_contact_risk_handover_complete = True
                $ agency_day4_independent_contact_outcome = "outcome_independent_option_prepared"
                narrator "她拿到联系人卡后先没有放进包里，而是把背面的风险一行行看完。看完最后一行，她把卡片转到自己熟悉的方向，才把游戏币交出。"
                narrator "窗口里的工作人员问了一个确认问题。我没有替她回答，她用手指点了点卡片上的名字，等确认完成后把卡片收进自己的夹层。"
                narrator "我看着卡片从窗口滑回来，先让她把风险说明折好。她点过的名字属于她；我只在旁边记住了卡片被收进哪个夹层。"
                narrator "工作人员把卡片推出玻璃下的缝时，先问她是否确认风险。她没有看我找答案，只看着卡片背面那几行小字。她用手指点到自己的昵称，又把卡片翻回正面。我听见她念出读法，声音很轻，却足够让窗口里的人照着登记。"
                narrator "我没有替她补充别的称呼，也没有把收据上的名字递过去。昨天她输入的字、今天她念出的读法，都由她自己放到窗口前。我的位置只是在旁边确认她能看见风险，能在卡片滑走前把手收回来。"
                narrator "卡片回到她掌心后，她没有立刻塞进口袋。她把背面的说明又看了一遍，才把它收进夹层。我问：\"要我记住哪一条？\"她用指尖点了点最下面的时限。我把那一条记下，没有替她决定什么时候使用。"
                narrator "游戏币交出去时，金属在窗口里响了一声。她看着它消失，没有回头看我。我没有说它换来了一条更好的路。它换来的是一张她亲自看过风险、自己保管的卡；以后能不能用，仍在她手里。"
                $ critical_choice_interaction = False

            "不登记联系人，让她把游戏币和纸片收回去":
                $ apply_choice("day4_decline_independent_contact", {})
                narrator "她把游戏币和写着昵称的纸片收回掌心。她保留了它们，也没有留下能继续联系的号码。"
                $ event_contact_channel_declined = True
                $ agency_day4_independent_contact_outcome = "outcome_independent_option_declined"
                narrator "她先把纸片上的名字折进里面，再把游戏币包在纸片外侧。收回来的东西仍然属于她，却不再承担一条已经登记的联系路径。"
                narrator "我看着窗口把空白卡片收走，没有把“以后还能想办法”说出口。拒绝留下的不是一句话，而是一个以后可以被找到的地址。"
                narrator "她把昵称折到纸片里面，游戏币压在外层，一起收进口袋，又按了按袋口。窗口没有递出卡片，号码也没登记，这条联系暂时留空。"
                narrator "我没有劝她再想一遍。窗口前的时间、追查的风险和她刚才收回的动作都已经足够清楚。要不要留下地址，她已经通过自己把纸和币收回去给出了能看见的回答；我不能因为自己害怕失去联系，就再把问题推给她。"
                narrator "我说：\"它们在你这里。\""
                narrator "她没有出声，只把口袋按平。售票员收走空白卡片，玻璃重新映出我们的影子。我把手从柜台上拿开，知道没有联系通道的路会更窄，却不能把窄说成她必须回头的理由。"
                $ critical_choice_interaction = False
    else:
        narrator "联系人纸片没有可用的识别物。绘梨衣把它折好，没有假装空白已经能替她留下一条路。"

    # scene_day4_sea_window
    scene bg seaside_station_window
    narrator "列车进站的风从站台尽头吹进来。绘梨衣把票、路线图或纸片放进自己能拿到的口袋，再看向海的方向。"
    narrator "风把售票窗旁的纸屑卷到脚边。她先按住口袋里的票或卡片，再把路线图折成不会遮住姓名和时间的大小。"
    narrator "站台另一端亮起一排车灯，海的方向被玻璃反光切成几块。我没有告诉她应该看哪一块，只把自己手里的空白纸片收好。"
    narrator "她最后检查了一次口袋的开口，确认物件没有滑出来。当天的准备没有替我们决定旅程，只让下一步能够被她自己拿在手里。"
    narrator "我跟着她走到站台边缘，却给她留出半步。风里有潮湿的铁锈味，车灯一次次扫过票、卡或折好的纸；我看见她把它们按稳，便不再替那只手决定该往哪边抬起。"
    narrator "列车停稳前，售票窗内的低灯熄了一盏。她回头看了一眼那块玻璃，再跟着人群走向站台边缘。"
    narrator "站台边的黄线被雨水洗得发亮。她走到线前停住，先摸了摸口袋，再看列车门会开在哪一节。她没有回头要我替她确认，我便站在她侧后，目光留在门、黄线和她已经按稳的口袋上。"
    narrator "海的方向没有真正的海，只是一条被玻璃反光映成灰蓝色的缝。她看了那条缝一会儿，又把路线图边缘捏紧。这样的停顿也许和上车有关，也许只是在躲风；我不必急着把它变成对未来的表态。"
    narrator "我问：\"票和卡都还在吗？\""
    narrator "她拍了拍口袋，随后把手抽出来。那是我能确认的回答。我没有再检查她的包，也没有替她拿住路线图。列车门打开的提示音响起时，我只把脚步放慢，等她先朝门口走。"
    narrator "车门里暖气扑到脸上，带着旧座椅的织物味。她跨上踏板前看了我一眼，又把目光移到车厢内侧。我看见她先上车，便跟着上去，不说这证明她选了哪条路，只承认下一步已经由她踏出来。"
    scene bg coastal_train_dawn
    narrator "车厢里有人把湿伞靠在门边，水顺着伞尖滴到地板。绘梨衣没有坐下，先站在门旁看路线图。她把票、卡或纸片按在夹层里，另一只手抓住扶杆。我没有替她挑座位，也没有把靠窗的位置说成她一定想要。"
    narrator "列车开动，站台的灯向后退。她等门边的人散开，才走到窗前。海线还是一道灰蓝色的缝，偶尔被隧道遮住。我陪她望着，没有急着说愿望已经实现。"
    narrator "我问：\"要坐这里吗？\""
    narrator "她把手放到靠窗座位的椅背上，停了一下，然后自己坐下。票、卡或纸片还在她口袋，我没有要她拿出来给我看。座位只是她当下选的位置，不是我能够借来解释整个旅程的证据。"
    narrator "我坐到隔着过道的一边，路线图放在她能够看到的地方。车厢晃动时，地图边角翘起来，她自己按平。我没有伸手越过过道。她如果要我看，能把纸转过来；没有转过来时，我只看窗外后退的站牌。"
    narrator "广播报出下一站，声音掺着雨后的电流杂音。她抬头听完，又低头看票面。她没有对我说要不要下车，我也没有替她把站名圈出来。每一站都会给我们一个新的时刻，却不能替她替我决定哪个时刻就是答案。"
    narrator "我说：\"到站我会先问。\""
    narrator "她把夹层扣住，轻轻点了一下。这个点头只回答她听见了。我没有把它扩大成同意所有后续，也没有立刻拿出备用方案。车继续往前，窗外的灰蓝色时有时无，我只在她真正停下或指向什么时再做回应。"
    narrator "玻璃渐渐起雾，她用指尖擦出一小块。水面的纹路刚显出来，又被信号灯切开。列车继续向前，票和路线图还收在原处。"
    narrator "车轮压过一段接缝，座椅轻轻晃了一下。绘梨衣用手按住口袋，等晃动过去才松开。我看见她确认票、卡或纸片还在，没有伸手替她检查。准备好的东西只有在她自己能随时取到时，才不是我用来安排她的证据。"
    narrator "我坐在过道另一边，证件仍在钱包最里层。售票窗留下的姓名不会因为列车启动就消失；那是我选择承担的暴露，不该被我说成她已经同意与我共同承担的风险。她手里的票也不能反过来证明她会陪我走到任何终点。"
    narrator "窗外掠过一处没有站名的小月台，灯光只照亮几把空椅子。她抬头看了一次，又把视线放回玻璃。我没有问要不要下车。列车没有停，问题也就没有落到她面前；我不把尚未发生的岔路提前变成一道要她回答的题。"
    narrator "有人从车厢另一头拖着行李经过，轮子在地板上发出断续的响。绘梨衣把膝盖往里收了一点，让出过道。我跟着把自己的脚收好。我们此刻共同做的只是在同一节车厢里给别人留路，并不替任何更大的同行作证明。"
    narrator "她把路线图摊在腿上，折痕压着窗光。我没要求她打开夹层。里面留下的是票、卡还是纸片，都由她收在自己够得到的地方。"
    narrator "钱包贴着掌心，边角还湿着。我想起窗口前在证件与零钱之间的犹豫。付过钱，也交过名字，却不能拿这些催她使用手里的票。"
    narrator "列车穿进隧道，玻璃变成镜子。黑色的窗里只剩车厢灯和我们隔着过道的影子。我看见她抬手碰了一下玻璃，又收回去。镜中的影子靠得很近，现实里的距离却仍在。我不把反光剪掉的距离叫成她没有说过的话。"
    narrator "隧道尽头亮起来，她眯了眯眼，继续看窗外。灰蓝色的海线又出现了。看得见海，还没到海边，我把那句庆祝的话咽了回去。"
    narrator "我问：\"窗太冷吗？要换到里面一点吗？\""
    narrator "她把手从玻璃上移开，却没有离开座位。这个动作只说明她把手收回了；我便没有替她起身，也没有把自己的外套递过去。车厢里的暖气时有时无，能被确认的冷暖还不够多，我不愿用关心逼她接下一件东西。"
    narrator "下一站的牌子从窗外闪过去，她没有拿出地图对照。我也没有在纸上圈站名。我们现在没有停靠，纸上那条线仍只是能被看的路线，不是一句命令。等车门真的打开、她真的看向某个方向，我再问。"
    narrator "广播平静地念着安全提示。绘梨衣听完，把口袋按平。我也看了一遍出口，没有再把每条提示念给她听。"
    narrator "我的手机在口袋里震了一下，屏幕上只是电量提示。我没有掏出来给她看，也没有假装新消息带来更快的答案。列车还在走，联系人是否存在、能否使用、会不会带来风险，都不是一条电量提示能解决的事。"
    narrator "她抬眼看向我时，我先把手机扣回口袋。她没有指向它，我便不擅自解释。她的目光停了一秒又回到窗外，我把这当作我看见的一次抬眼，而不是一份交给我解读的请求。"
    narrator "车轮声持续得很稳，反而让我听见自己一直想把所有准备列成一张清单：票、证件、零钱、纸片、游戏币、可能的号码。清单能让我觉得自己没有漏掉什么，却不能替她决定哪一项应该先被使用。于是我没有把它念出来。"
    narrator "她把路线图折回原来的大小，手指停在最外面的折痕。没有拿出来的票也好、没有登记的卡也好、留在我口袋里的东西也好，都还没有自动变成答案。我看见她把纸折好，只把那当作她暂时不让它在车厢里展开。"
    narrator "我说：\"到站前，我不替你收东西。\""
    narrator "她没有回答，只把夹层再次按住。她不需要替我肯定这句承诺；我说出口，是为了提醒自己不要在车门快开时以为帮忙就可以越过她的手。她要我拿，我再拿；她没有交来，我就让它留在她那里。"
    narrator "车厢里的孩子把糖纸揉成团，滚到了过道中央。绘梨衣看了一眼。我弯腰把糖纸拨到鞋边，等乘务员过来，没打断她。"
    narrator "经过河桥时，桥下的水面短暂亮起来。她把额头靠近玻璃，却没有贴上去。风景从窗外向后退，我看不见她眼里留下了什么。她若要告诉我，我会听；她没有告诉我，我就不把河、海和任何远处的颜色排成她心里的顺序。"
    narrator "她在窗口分别碰过车次、座位和联系人纸片。那些东西各有用处，不能因为我承担了实名的风险，就把它们一并替她收走。"
    narrator "车门上方的绿灯亮着，紧急拉手就在不远处。她没有看它，我也没有把它指给她。能看见的出口已经在车厢里，不需要我反复用手指出，像是在提醒她随时逃离我安排的路。"
    narrator "我把背靠回座椅，给她留出完整的视线。她如果要把路线图转过来，我能看见；她不转过来，我就继续看窗外。互相可见和必须共享不是一回事，我以前总把它们混在一起。"
    narrator "广播提醒下一站即将到达。她没有立刻站起，只把脚尖轻轻向内收。我等车速慢下来，没有伸手去够她口袋里的物件，也没有先把自己的证件拿出来。下不下车、在哪一站停，都还没有被她用行动回答。"
    narrator "我问：\"车门开了，我先等你看。可以吗？\""
    narrator "她抬眼看我，随后轻轻点头。这个点头只回答我会等她看。我把它记得很清楚，不拿它去覆盖她对车票、联系人或整个旅程尚未作出的所有回答。"
    narrator "列车减速时，站牌从雾气里露出来。她先把路线图按在掌下，再从窗边看向门口。我跟着站起来，却停在她后面。她如果坐着，我就坐回去；她如果走到门边，我才跟上。"
    narrator "车门打开，站台的冷风钻进来。她没有立刻跨出去，只看了一眼外面的灯。我没有问那盏灯是不是她想找的地方。等待她看清，和替她把灯命名，是两件不同的事。"
    narrator "提示音响了第二次，她把手从夹层上拿开，又没有掏出里面的东西。她决定留在车上还是下车，只有真正跨出或不跨出的动作才能让我知道。我站在后面，连自己的呼吸都尽量放轻。"
    narrator "门在短暂停留后重新合上。她回到座位旁，没有看我解释什么。我也不说还好、可惜或下一站更合适。门刚才开过，这是事实；她没有从这节车厢离开，也是事实。比起替它们立刻编出意义，我更该让下一次停靠仍属于她。"
    narrator "她坐回窗边，把票、卡或纸片的边角压得更深。我不追问刚才为什么没有下车。站台的灯、车门的提示音和她没有跨出的那一步都已经足够清楚；如果她要说原因，会由她自己把那件事带到我面前。"
    narrator "我把自己的证件夹回钱包，听见扣子合上的声音。实名留下的痕迹并没有因此被收好，我却也不能拿它提醒她欠我一次同行。选择暴露名字是我在窗口前做的承担，不能变成她必须报答的票价。"
    narrator "列车又驶进一段暗处，路线图的折痕只在顶灯下露出细白的线。我没有把头凑过去看她压着哪一条。不同路线和不同准备已经各自留在她手里，能否使用不需要我在每一站替她复核。"
    narrator "我说：\"下一站也先看你。\""
    narrator "她没有再点头，只把眼睛移到窗外。那不是把刚才的回答收回，而是她不必重复同一句话来让我安心。我坐回原位，等车轮声把下一次真正需要选择的时刻带来。"
    narrator "靠窗的雾慢慢散开，远处的水面和陆地仍被夜色混在一起。她没有把它们指成海，我也没有替她说我们已经离目的地很近。车在走，准备在她口袋，代价在我的名字下；除此以外，我不让自己的希望先于她的回答。"
    narrator "路线图在她膝上留下一道浅浅的压痕，车票或卡片仍由她自己按住。我看见那些物件没有滑走，也看见她没有交给我；这比任何关于抵达的句子都更明确地提醒我，准备的价值是让她还能选择，而不是让我替她宣布已经选好。"
    narrator "列车重新启动，窗外的站灯被拉成一条细线。她把路线图收好，手还留在口袋边。我把自己放回过道另一侧，知道今天准备出来的每一种方向都没有替她完成选择，只让她在真正需要时仍有东西可以从自己手里拿出来。"
    return
