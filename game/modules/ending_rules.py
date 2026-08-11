"""Deterministic ending resolution for Rain After.

This module deliberately has no Ren'Py imports and owns no mutable game state.
It can be tested with normal Python and safely called from Ren'Py with a snapshot.
"""

AXES = (
    "understanding",
    "autonomy",
    "truth",
    "preparation",
    "sacrifice",
)

ENDING_PRIORITY = (
    "rain_stops",
    "her_own_name",
    "see_the_sea",
    "one_person_train",
    "golden_cage",
    "unsent_postcard",
)
ENDING_PENDING_ID_PREFIX = "ending."
ENDING_PENDING_IDS = tuple(
    ENDING_PENDING_ID_PREFIX + ending_id for ending_id in ENDING_PRIORITY
)

ENDING_TITLES = {
    "rain_stops": "雨停之后",
    "her_own_name": "她自己的名字",
    "see_the_sea": "去看海吧",
    "one_person_train": "一个人的列车",
    "golden_cage": "金色的笼子",
    "unsent_postcard": "未寄出的明信片",
}


def validate_snapshot(snapshot):
    """Return a normalized copy after checking the complete 0..3 domain."""
    if not hasattr(snapshot, "keys"):
        raise TypeError("ending snapshot must be a mapping")

    missing = [axis for axis in AXES if axis not in snapshot]
    extra = [key for key in snapshot.keys() if key not in AXES]
    if missing or extra:
        raise ValueError(
            "invalid ending snapshot keys; missing={!r}, extra={!r}".format(
                missing, extra
            )
        )

    normalized = {}
    for axis in AXES:
        value = snapshot[axis]
        if type(value) is not int:
            raise TypeError("{} must be an integer".format(axis))
        if value < 0 or value > 3:
            raise ValueError("{} must be in the range 0..3".format(axis))
        normalized[axis] = value

    return normalized


def resolve_ending(snapshot):
    """Resolve one and only one stable ending ID."""
    state = validate_snapshot(snapshot)
    understanding = state["understanding"]
    autonomy = state["autonomy"]
    truth = state["truth"]
    preparation = state["preparation"]
    sacrifice = state["sacrifice"]

    if all(state[axis] >= 3 for axis in AXES):
        return "rain_stops"

    if understanding >= 2 and autonomy >= 3 and truth >= 3:
        return "her_own_name"

    if (
        understanding >= 2
        and autonomy >= 2
        and preparation >= 3
        and sacrifice >= 2
    ):
        return "see_the_sea"

    if autonomy >= 2 and (preparation >= 2 or truth >= 2):
        return "one_person_train"

    if autonomy <= 1 and (
        understanding >= 2 or truth >= 2 or preparation >= 2
    ):
        return "golden_cage"

    return "unsent_postcard"
