# Frozen SYS-ENDING closures. These labels present an already-selected result;
# they do not inspect or derive the ending from gameplay state.

default event_epilogue_first_guest_completed = False
default cp_epilogue_first_guest_complete = False
default event_epilogue_lights_out_completed = False
default cp_epilogue_lights_out_complete = False


label ending_rain_stops:
    $ commit_ending_entry("rain_stops")
    scene bg warm_room

    # scene_ending_rain_stops
    narrator "雨停在窗外。路明非把旧身份和曾经能支配一切的力量留在门外，没有再把它们带回她自己的名字里。"
    narrator "绘梨衣把路线图折好，自己写下明天要去的地方。那些完整说出的真相和已经付出的代价，没有替她决定生活，只让这份生活终于可以被保住。"
    narrator "他们没有给未来起一个更大的名字；街上的灯亮起来，普通的一天等着开始。"
    $ commit_ending_completion("rain_stops", "ending.rain_stops.completion")
    jump epilogue_rain_stops_arcade


label ending_her_own_name:
    $ commit_ending_entry("her_own_name")
    scene bg warm_room

    # scene_ending_her_own_name
    narrator "她把联系人卡和写着自己名字的纸放进外套口袋，按自己选好的路线离开。"
    narrator "分别没有被说成轻松，也没有被当作替她收回决定权的理由。路明非留在原地，知道下一次联系要等她自己拨通。"
    narrator "列车开走以后，屏幕上那个由她选出的昵称还亮着；两人隔着距离，仍保留一条可以由她开启的线。"
    $ commit_ending_completion("her_own_name", "ending.her_own_name.completion")
    return


label ending_see_the_sea:
    $ commit_ending_entry("see_the_sea")
    scene bg warm_room

    # scene_ending_see_the_sea
    narrator "两张靠窗的票被并排放在桌上。路线仍然危险，但它不再是假装没有代价的承诺。"
    narrator "路明非先烧掉旧身份留下的凭据；绘梨衣看完路线和风险，自己把票收进包里。"
    narrator "他们朝同一片海出发。未来并没有被保证，只是这一次，代价和选择都由愿意同行的人共同承担。"
    $ commit_ending_completion("see_the_sea", "ending.see_the_sea.completion")
    return


label ending_one_person_train:
    $ commit_ending_entry("one_person_train")
    scene bg warm_room

    # scene_ending_one_person_train
    narrator "单人票在她手里，能离开的路线确实存在。"
    narrator "可是没有被补上的理解和准备，已经让同行的承诺失去可以站立的地方；他们没有再把这种空缺叫作一起出发。"
    narrator "车门合上时，绘梨衣独自带着自己的票离开。路明非没有追上去，只把这场失散当成已经发生的后果。"
    $ commit_ending_completion("one_person_train", "ending.one_person_train.completion")
    return


label ending_golden_cage:
    $ commit_ending_entry("golden_cage")
    scene bg warm_room

    # scene_ending_golden_cage
    narrator "被称作安全的方案盖过了她已经说出的决定。路线图被收起时，没有人再问她要走向哪里。"
    narrator "那些没有被承认的日常替代和最初的覆盖，终于不再只是纸上的痕迹；旧秩序重新把她带回可以被安排的位置。"
    narrator "路明非站在门外，明白自己留下的不是保护，而是一座把选择锁在里面的笼子。"
    $ commit_ending_completion("golden_cage", "ending.golden_cage.completion")
    return


label ending_unsent_postcard:
    $ commit_ending_entry("unsent_postcard")
    scene bg warm_room

    # scene_ending_unsent_postcard
    narrator "桌上没有一条还能执行的路线。被省略的真相、太晚的准备和没有被承担的代价，把每一张纸都留在原处。"
    narrator "绘梨衣把愿望纸压在那张没有寄出的明信片下面；它们没有替谁原谅什么，也没有忽然变成新的出路。"
    narrator "雨又落下来。路明非看着没有送出的地址，承认有些愿望若没有在该承担的时候行动，只会留下完整的后果。"
    $ commit_ending_completion("unsent_postcard", "ending.unsent_postcard.completion")
    return


label epilogue_rain_stops_arcade:
    scene bg warm_room

    # scene_epilogue_first_guest
    narrator "傍晚的网吧只开了几盏灯。那枚被留作识别物的第二枚游戏币放在机台边，像一段没有被花掉的旧日时间。"
    narrator "绘梨衣坐到屏幕前，自己敲下曾经选过的昵称，再把键盘推回一个刚好够两个人看见的位置。"
    narrator "屏幕亮出今天第一位客人的预约。她核对完时间和座位，点头把这件普通的小事做完。"
    $ event_epilogue_first_guest_completed = True
    $ cp_epilogue_first_guest_complete = True

    # scene_epilogue_lights_out
    narrator "最后一局结束后，她先关掉机台的声音，再伸手关灯。路明非替她拿起外套，却没有替她决定明天。"
    narrator "门锁合上，他们一起回家；没有人宣布胜利，只有灯灭之后仍然可以继续过下去的晚上。"
    $ event_epilogue_lights_out_completed = True
    $ cp_epilogue_lights_out_complete = True

    # story_025_tail_observer: ordinary neighborhood view, no named reunion.
    narrator "【普通街坊观察】多年以后，小网吧还在街角开着；路过的街坊只把它当作一家安静的普通小店。"
    narrator "偶尔有几个不具名的旧友来坐一会儿，普通顾客在熟悉的机台前等空位，谁也不需要把这些日子说成传奇。"

    # story_025_tail_written_note: complex content is written, never erii speech.
    narrator "【绘梨衣的书面手记】纸上留下几行简短的记录：今天的灯按时亮过，也按时熄灭；明天要做的事，仍然可以由自己写下。"
    narrator "手记没有替任何人宣布答案，只把那些被认真保留下来的普通日子，一页一页放回桌面。"
    return
