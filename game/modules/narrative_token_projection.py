"""Pure, history-derived token projection for authored narrative gates.

This module owns no live Ren'Py state. Chapters query the projection through
``has_unresolved_token`` so a repair gate is determined solely by the ordered
canonical choice history.
"""

from __future__ import annotations


TOKEN_REVOKE_BY_CHOICE = {
    "day1_assume_food_consent": "token_silence_as_consent",
    "day2_assign_alias": "token_override_daily_choice",
    "day3_hide_school_evidence": "token_hide_school_evidence",
    "day3_force_explanation": "token_override_daily_choice",
    "day4_decline_independent_contact": "token_abandon_backup_plan",
    "day4_follow_one_route_no_backup": "token_abandon_backup_plan",
    "day5_give_safe_summary": "token_withhold_family_truth",
    "day5_replace_erii_response": "token_override_daily_choice",
}
TOKEN_REPAIR_BY_CHOICE = {
    "day2_admit_alias_unknown": "token_silence_as_consent",
    "day5_repair_daily_choice": "token_override_daily_choice",
    "day5_repair_school_evidence": "token_hide_school_evidence",
}


def unresolved_token_ids(choice_history: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    """Project unresolved tokens from ordered choice history without mutation."""

    unresolved: list[str] = []
    for choice_id in choice_history:
        revoked_token = TOKEN_REVOKE_BY_CHOICE.get(choice_id)
        if revoked_token is not None and revoked_token not in unresolved:
            unresolved.append(revoked_token)

        repaired_token = TOKEN_REPAIR_BY_CHOICE.get(choice_id)
        if repaired_token is not None and repaired_token in unresolved:
            unresolved.remove(repaired_token)
    return tuple(unresolved)


def has_unresolved_token(
    choice_history: tuple[str, ...] | list[str], token_id: str
) -> bool:
    """Return whether ``token_id`` remains unresolved for this history."""

    return token_id in unresolved_token_ids(choice_history)
