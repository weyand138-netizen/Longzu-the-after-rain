"""Detached achievement presentation model with hidden-state exclusion."""

from dataclasses import dataclass

from .persist_projections import ACHIEVEMENT_IDS, AchievementProjectionResult


@dataclass(frozen=True)
class AchievementRow:
    achievement_id: str
    state: str
    display_name: str


def build_achievement_rows(unlocked: tuple[str, ...] | list[str], seen: tuple[str, ...] | list[str]) -> tuple[AchievementRow, ...]:
    """Render only approved public state; locked internals are absent."""

    unlocked_set = set(unlocked)
    seen_set = set(seen)
    return tuple(AchievementRow(item, "seen" if item in seen_set else "new", item.replace("_", " ").title()) for item in ACHIEVEMENT_IDS if item in unlocked_set)


def presentation_decision(result: AchievementProjectionResult, safe_boundary: bool) -> tuple[str, tuple[str, ...]]:
    if result.status != "APPLIED_FLUSHED" or not result.added_achievement_ids:
        return "NO_PRESENTATION", ()
    if not safe_boundary:
        return "DEFER", result.added_achievement_ids
    return "PRESENT", result.added_achievement_ids
