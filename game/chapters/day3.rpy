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
    $ event_empty_school_trace_confirmed = True
    $ cp_day3_empty_school_trace_complete = True

    # scene_day3_evidence_choice
    narrator "整理好的纸停在两人之间。绘梨衣没有伸手，只看着路明非。"
    $ critical_choice_interaction = True

    menu:
        "把门禁记录、时间和泥印都递给她":
            $ apply_choice("day3_share_school_evidence", {"truth": 1})
            narrator "她把三张纸一张张看完，随后把它们叠好，放在自己面前。"
            $ critical_choice_interaction = False

        "只告诉她已经核对出的结论":
            $ apply_choice("day3_hide_school_evidence", {})
            narrator "她听完结论，没有接过桌上的纸，只把手停在桌沿。"
            $ critical_choice_interaction = False

    # scene_day3_truth_pace_answer
    narrator "路明非把余下的纸留在手边，等她决定是否还要继续。"
    $ agency_day3_truth_pace_request = DAY3_AGENCY_REQUEST_ID
    narrator "绘梨衣合上档案，指尖压在封面上，没有抬头。"
    $ agency_day3_truth_pace_answer = DAY3_AGENCY_PAUSE_ANSWER_ID
    $ critical_choice_interaction = True

    menu:
        "先把档案收好，等她自己再打开":
            $ apply_choice("day3_honor_pause", {"understanding": 1, "autonomy": 1})
            $ agency_day3_truth_pace_outcome = "outcome_pause_honored"
            narrator "他把档案收在桌边。过了一会儿，她自己把最上面那页重新打开。"
            $ critical_choice_interaction = False

        "继续解释余下的内容":
            $ apply_choice("day3_force_explanation", {})
            $ agency_day3_truth_pace_outcome = "outcome_pause_overridden"
            narrator "他继续把余下的说明念完。她向后退，手从纸边移开，直到走廊灯在门缝里变窄。"
            $ critical_choice_interaction = False

    return
