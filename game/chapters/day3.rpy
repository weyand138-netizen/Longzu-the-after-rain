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
    scene bg warm_room

    # scene_day3_classroom_trace
    narrator "傍晚的教学楼里只亮着走廊尽头一盏灯。空教室的门半开着，窗框下留着一小片红泥。"
    narrator "路明非把门禁记录、走廊时间和窗边的泥印放在同一张桌上。三处时间对得上，泥印也和先前见过的痕迹相同。"
    narrator "绘梨衣把三张纸排齐，先用指尖压住门禁记录，再看向窗边。"
    narrator "门禁、时间和泥印指向同一段来路；她看过后，慢慢合上最上面的纸。"
    narrator "教室里的桌椅按照老师离开时的样子排着，只有靠窗的一张椅子向后歪了一点。雨水从窗框渗进来，把红泥的边缘冲得发亮。"
    narrator "路明非把门禁记录放在最左边，时间表放在中间，最后才把泥印旁边拍下的照片压在右边。三张纸没有彼此解释，却在相同的时间停住。"
    narrator "绘梨衣没有先看照片。她用指尖沿着门禁记录上的一行数字走过，再抬头看向门缝，像是在把纸上的时间放回这间真实的教室。"
    narrator "走廊尽头的灯闪了一下，门上的玻璃映出两个人的影子。影子没有经过窗边，却让那片泥印显得更像一个刚刚离开的痕迹。"
    narrator "路明非想起站台上的红泥和维修门，没有把它们直接拼成结论。他把那两件事写在纸的背面，留给绘梨衣自己决定是否要连起来。"
    $ event_empty_school_trace_confirmed = True
    $ cp_day3_empty_school_trace_complete = True

    # scene_day3_evidence_choice
    narrator "整理好的纸停在两人之间。绘梨衣没有伸手，只看着路明非。"
    narrator "纸角被风从半开的窗缝里吹起，门禁记录翻到下一页，又被她按住。她看见路明非已经把答案写在表情里，却仍然等着他决定把哪一种信息交到她手中。"
    narrator "教室里没有老师的声音，也没有谁能替他们证明那段时间发生过什么。能被核对的事实只剩下纸面、泥印和一个没有关严的窗。"
    $ critical_choice_interaction = True

    menu:
        "把门禁记录、时间和泥印都递给她":
            $ apply_choice("day3_share_school_evidence", {"truth": 1})
            narrator "她把三张纸一张张看完，随后把它们叠好，放在自己面前。"
            narrator "她先把照片翻到背面，再把门禁记录压在最上面。每换一次顺序，她都会停下来确认路明非没有替她跳过某一页。"
            narrator "确认完最后一行时间后，她把纸叠成和愿望纸相同的大小，放在自己能够再次打开的位置。空教室里的事实因此有了一个可以被带走的形状。"
            $ critical_choice_interaction = False

        "只告诉她已经核对出的结论":
            $ apply_choice("day3_hide_school_evidence", {})
            narrator "她听完结论，没有接过桌上的纸，只把手停在桌沿。"
            narrator "她的目光仍落在那叠没有被递出的纸上。路明非说的是已经整理好的方向，纸面上那些还没有被她亲自看过的细节却留在两人之间。"
            narrator "她把手从桌沿收回，袖口擦过一小块未干的泥。那个动作没有变成反驳，只让“已经知道”与“亲眼看过”之间留下了清楚的距离。"
            $ critical_choice_interaction = False

    # scene_day3_truth_pace_answer
    narrator "路明非把余下的纸留在手边，等她决定是否还要继续。"
    $ agency_day3_truth_pace_request = DAY3_AGENCY_REQUEST_ID
    narrator "绘梨衣合上档案，指尖压在封面上，没有抬头。"
    $ agency_day3_truth_pace_answer = DAY3_AGENCY_PAUSE_ANSWER_ID
    narrator "封面上的灰尘被她的指尖推成一道很窄的线。她没有把档案推远，也没有把它重新打开，只让这一页停在她可以再次触碰的位置。"
    narrator "走廊里的灯又闪了一次。路明非把已经说到嘴边的解释压回去，听见楼下有人锁门，知道等待本身也会消耗今天剩下的时间。"
    $ critical_choice_interaction = True

    menu:
        "先把档案收好，等她自己再打开":
            $ apply_choice("day3_honor_pause", {"understanding": 1, "autonomy": 1})
            $ agency_day3_truth_pace_outcome = "outcome_pause_honored"
            narrator "他把档案收在桌边。过了一会儿，她自己把最上面那页重新打开。"
            narrator "她先看路明非一眼，确认他没有把手伸向档案，才用两根手指把最上面那页翻回来。纸张摩擦桌面的声音很轻，却把继续阅读变成了她自己的动作。"
            narrator "她没有一次看完所有内容，只沿着门禁时间读到窗边的泥印，再把照片放在对应的位置。事实被拆成几步，速度也由她自己掌握。"
            $ critical_choice_interaction = False

        "继续解释余下的内容":
            $ apply_choice("day3_force_explanation", {})
            $ agency_day3_truth_pace_outcome = "outcome_pause_overridden"
            narrator "他继续把余下的说明念完。她向后退，手从纸边移开，直到走廊灯在门缝里变窄。"
            narrator "每说完一段，路明非都能听见自己的声音在空教室里撞回墙面。绘梨衣没有打断他，却把身体一步步移到门边，让档案离自己更远。"
            narrator "最后一页被念到时，窗外的雨已经停了。她看向纸面，又看向被关窄的门缝，像是在记住这一次不是事实太少，而是事实被推进得太快。"
            $ critical_choice_interaction = False

    return
