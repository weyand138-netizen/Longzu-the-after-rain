"""SYS-PERSIST schema-v2 validation and detached snapshot contracts."""

from copy import deepcopy
from typing import Any, Mapping


PERSIST_SCHEMA_VERSION = 2
PERSIST_CATALOG_GENERATION_ID = "catalog:v2"
PERSIST_ROOT_FIELDS = (
    "schema_version",
    "catalog_generation_id",
    "collection_epoch_id",
    "achievement_ids",
    "seen_achievement_ids",
    "ending_ids",
    "memory_ids",
    "settings",
)
SETTING_FIELDS = (
    "font_scale",
    "high_contrast",
    "reduced_motion",
    "flash_effects_enabled",
    "screen_shake_enabled",
)
NORMATIVE_LEAF_COUNT = 12
ALLOWED_FONT_SCALES = (0.8, 1.0, 1.2, 1.5, 2.0)


class PersistSchemaError(ValueError):
    """Raised when a persistent root is not the exact schema-v2 contract."""


def build_fresh_persist_root() -> dict[str, Any]:
    """Return the only supported fresh persistent root."""

    return {
        "schema_version": PERSIST_SCHEMA_VERSION,
        "catalog_generation_id": PERSIST_CATALOG_GENERATION_ID,
        "collection_epoch_id": 0,
        "achievement_ids": [],
        "seen_achievement_ids": [],
        "ending_ids": [],
        "memory_ids": [],
        "settings": {
            "font_scale": 1.0,
            "high_contrast": False,
            "reduced_motion": False,
            "flash_effects_enabled": True,
            "screen_shake_enabled": True,
        },
    }


def _exact_string_list(value: Any, field: str) -> None:
    if type(value) is not list:
        raise PersistSchemaError(f"{field} must be an exact list")
    if any(type(item) is not str or not item for item in value):
        raise PersistSchemaError(f"{field} must contain non-empty exact strings")
    if len(value) != len(set(value)):
        raise PersistSchemaError(f"{field} must not contain duplicates")
    if value != sorted(value):
        raise PersistSchemaError(f"{field} must use canonical order")


def _validate_container(root: Any) -> None:
    if type(root) is not dict:
        raise PersistSchemaError("root must be an exact dict")
    if tuple(root.keys()) != PERSIST_ROOT_FIELDS:
        raise PersistSchemaError("root keys must match the exact canonical order")
    settings = root["settings"]
    if type(settings) is not dict or tuple(settings.keys()) != SETTING_FIELDS:
        raise PersistSchemaError("settings keys must match the exact canonical order")


def _validate_values(root: dict[str, Any]) -> None:
    if type(root["schema_version"]) is not int or root["schema_version"] != 2:
        raise PersistSchemaError("schema_version must be exact integer 2")
    if type(root["catalog_generation_id"]) is not str or not root["catalog_generation_id"]:
        raise PersistSchemaError("catalog_generation_id must be a non-empty string")
    if type(root["collection_epoch_id"]) is not int or root["collection_epoch_id"] < 0:
        raise PersistSchemaError("collection_epoch_id must be a non-negative exact int")
    for field in ("achievement_ids", "seen_achievement_ids", "ending_ids", "memory_ids"):
        _exact_string_list(root[field], field)
    if not set(root["seen_achievement_ids"]).issubset(root["achievement_ids"]):
        raise PersistSchemaError("seen achievements must be a subset of achievements")
    settings = root["settings"]
    if type(settings["font_scale"]) is not float or settings["font_scale"] not in ALLOWED_FONT_SCALES:
        raise PersistSchemaError("font_scale is not an approved exact float")
    for field in SETTING_FIELDS[1:]:
        if type(settings[field]) is not bool:
            raise PersistSchemaError(f"{field} must be an exact bool")


def validate_persist_root(root: Any) -> dict[str, Any]:
    """Validate in fixed container-then-value order and return the same root."""

    _validate_container(root)
    _validate_values(root)
    return root


def count_normative_leaves(root: Any) -> int:
    """Return the schema leaf count only after full validation."""

    validate_persist_root(root)
    return len(PERSIST_ROOT_FIELDS) - 1 + len(SETTING_FIELDS)


def snapshot_persist_root(root: Mapping[str, Any]) -> dict[str, Any]:
    """Return a detached built-in snapshot without aliasing the live root."""

    if type(root) is not dict:
        raise PersistSchemaError("root must be an exact dict")
    validate_persist_root(root)
    snapshot = deepcopy(root)
    validate_persist_root(snapshot)
    return snapshot


def build_ownership_manifest() -> dict[str, Any]:
    """Return the frozen owner/requester/merge/reset contract."""

    return {
        "root_field_name": "persistent.sys_persist_state",
        "leaf_paths": [
            "schema_version", "catalog_generation_id", "collection_epoch_id",
            "achievement_ids", "seen_achievement_ids", "ending_ids", "memory_ids",
            "settings.font_scale", "settings.high_contrast", "settings.reduced_motion",
            "settings.flash_effects_enabled", "settings.screen_shake_enabled",
        ],
        "owners": ["SYS-PERSIST"] * NORMATIVE_LEAF_COUNT,
        "requesters": ["SYS-ACHIEVE", "SYS-ACHIEVE", "SYS-ACHIEVE", "SYS-ACHIEVE", "SYS-ACHIEVE", "SYS-ENDING", "SYS-JOURNAL", "SYS-ACCESS", "SYS-ACCESS", "SYS-ACCESS", "SYS-ACCESS", "SYS-ACCESS"],
        "merge_policy": ["replace", "replace", "max", "union", "union", "union", "union", "replace", "replace", "replace", "replace", "replace"],
        "reset_policy": ["preserve", "preserve", "increment", "clear", "clear", "clear", "clear", "preserve", "preserve", "preserve", "preserve", "preserve"],
        "migration_policy": "schema-v2-only; future changes require migration ADR",
    }


def validate_ownership_manifest(manifest: Any) -> None:
    """Validate exact manifest shape and parallel-array lengths."""

    if type(manifest) is not dict:
        raise PersistSchemaError("ownership manifest must be an exact dict")
    expected = {"root_field_name", "leaf_paths", "owners", "requesters", "merge_policy", "reset_policy", "migration_policy"}
    if set(manifest) != expected:
        raise PersistSchemaError("ownership manifest has unknown or missing fields")
    if manifest["root_field_name"] != "persistent.sys_persist_state":
        raise PersistSchemaError("unexpected persistent root owner")
    if any(type(manifest[field]) is not list for field in ("leaf_paths", "owners", "requesters", "merge_policy", "reset_policy")):
        raise PersistSchemaError("manifest arrays must be exact lists")
    if len(manifest["leaf_paths"]) != NORMATIVE_LEAF_COUNT or len({*manifest["leaf_paths"]}) != NORMATIVE_LEAF_COUNT:
        raise PersistSchemaError("manifest must contain exactly 12 unique leaf paths")
    lengths = {len(manifest[field]) for field in ("owners", "requesters", "merge_policy", "reset_policy")}
    if lengths != {NORMATIVE_LEAF_COUNT}:
        raise PersistSchemaError("manifest parallel arrays must be length 12")
    if type(manifest["migration_policy"]) is not str or not manifest["migration_policy"]:
        raise PersistSchemaError("migration policy must be explicit")
