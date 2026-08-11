# VERTICAL SLICE - NOT FOR PRODUCTION
# Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality?
# Date: 2026-07-23

default understanding = 0
default autonomy = 0
default truth = 0
default preparation = 0
default sacrifice = 0
default choice_history = []
default payoff_lines = []
default persistent.slice_achievement_observer = False
default persistent.slice_memory = None
default persistent.slice_high_contrast = False

init python:
    SLICE_AXES = (
        "understanding",
        "autonomy",
        "truth",
        "preparation",
        "sacrifice",
    )
    SLICE_AXIS_MIN = 0
    SLICE_AXIS_MAX = 3

    achievement.register("SLICE_OBSERVER")

    def reset_slice_state():
        global understanding, autonomy, truth, preparation, sacrifice
        global choice_history, payoff_lines

        understanding = 0
        autonomy = 0
        truth = 0
        preparation = 0
        sacrifice = 0
        choice_history = []
        payoff_lines = []

    def _slice_clamp(value):
        return max(SLICE_AXIS_MIN, min(SLICE_AXIS_MAX, value))

    def apply_slice_choice(choice_id, deltas):
        global understanding, autonomy, truth, preparation, sacrifice
        global choice_history

        unknown = [key for key in deltas if key not in SLICE_AXES]
        if unknown:
            raise ValueError("Unknown slice axes: {!r}".format(unknown))
        if choice_id in choice_history:
            raise ValueError("Choice recorded twice: {}".format(choice_id))

        understanding = _slice_clamp(
            understanding + deltas.get("understanding", 0)
        )
        autonomy = _slice_clamp(autonomy + deltas.get("autonomy", 0))
        truth = _slice_clamp(truth + deltas.get("truth", 0))
        preparation = _slice_clamp(
            preparation + deltas.get("preparation", 0)
        )
        sacrifice = _slice_clamp(sacrifice + deltas.get("sacrifice", 0))
        choice_history = choice_history + [choice_id]

    def add_payoff(line):
        global payoff_lines
        payoff_lines = payoff_lines + [line]

    def unlock_observer_achievement():
        if not persistent.slice_achievement_observer:
            persistent.slice_achievement_observer = True
            achievement.grant("SLICE_OBSERVER")
            renpy.notify("成就解锁：被雨打湿的愿望")

    def slice_memory_summary():
        if "ask_destination" in choice_history:
            relation = "你把路线图转向了她，让她第一次亲手选择目的地。"
        else:
            relation = "你选了最快的路线，也记住了她点头点得有多快。"

        if "notice_tracker" in choice_history:
            observation = "你记住追踪者鞋底的红泥，确认他没有登上这班车。"
        elif "notice_service_door" in choice_history:
            observation = "你记住封闭维修门的位置，为下一次撤离留下备选出口。"
        else:
            observation = "你把一句承诺交给了她，也接受后果不再只属于一个人。"

        return relation + "\n" + observation
