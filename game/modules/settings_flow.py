"""SYS-PERSIST settings draft/rebase/conflict transaction semantics."""

from dataclasses import dataclass
from typing import Any

from .persist_schema import SETTING_FIELDS, snapshot_persist_root, validate_persist_root


STALE_DRAFT_CONFLICT = "STALE_DRAFT_CONFLICT"


@dataclass(frozen=True)
class SettingsDraft:
    """Detached draft with the root revision it was based on."""

    base_revision: int
    values: dict[str, Any]
    dirty: bool


def make_settings_draft(root: dict[str, Any], revision: int) -> SettingsDraft:
    validate_persist_root(root)
    if type(revision) is not int or revision < 0:
        raise TypeError("revision must be a non-negative exact int")
    return SettingsDraft(revision, dict(root["settings"]), False)


def update_draft(draft: SettingsDraft, **changes: Any) -> SettingsDraft:
    if set(changes) - set(SETTING_FIELDS):
        raise ValueError("unknown settings field")
    values = dict(draft.values)
    values.update(changes)
    return SettingsDraft(draft.base_revision, values, True)


def rebase_draft(draft: SettingsDraft, latest_root: dict[str, Any], latest_revision: int) -> tuple[SettingsDraft, str | None]:
    validate_persist_root(latest_root)
    if not draft.dirty:
        return SettingsDraft(latest_revision, dict(latest_root["settings"]), False), None
    changed_externally = {key for key in SETTING_FIELDS if draft.base_revision != latest_revision and latest_root["settings"][key] != draft.values[key]}
    if draft.base_revision != latest_revision and changed_externally:
        return SettingsDraft(latest_revision, dict(latest_root["settings"]), True), STALE_DRAFT_CONFLICT
    return SettingsDraft(latest_revision, dict(draft.values), True), None


def apply_settings_draft(root: dict[str, Any], draft: SettingsDraft, revision: int) -> dict[str, Any]:
    validate_persist_root(root)
    if draft.base_revision != revision:
        raise ValueError(STALE_DRAFT_CONFLICT)
    candidate = snapshot_persist_root(root)
    candidate["settings"] = dict(draft.values)
    validate_persist_root(candidate)
    return candidate
