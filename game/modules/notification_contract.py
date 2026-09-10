"""Pure v1 notification identities and state transitions.

The runtime owner in ``12_audio.rpy`` keeps the mutable session record and its
``RLock``.  This module deliberately has no Ren'Py import, globals holding
runtime state, audio API, or test-only dependency; every transition receives
and returns immutable values.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
import re
from typing import Any, Iterable, Mapping


RAW_GROUP_VERSION = "notification-group:v1"
SUMMARY_VERSION = "notification-summary:v1"
RAW_GROUP_PREFIX = "notify-group:v1:"
SUMMARY_PREFIX = "notify-summary:v1:"
OCCURRENCE_PREFIX = "notification-audio:v1:"
LIVE_NOTIFICATION_SUMMARY = "LIVE_NOTIFICATION_SUMMARY"
NONLIVE_PROVENANCES = frozenset((
    "PERSISTENT_MERGE",
    "STARTUP_PROJECTION_REPAIR",
    "LOAD_RECONSTRUCTION",
    "ROLLBACK_RECONSTRUCTION",
    "NEW_GAME_RECONSTRUCTION",
    "DUPLICATE_RENDER",
    "REFRESH",
    "RECOVERY",
    "BLOCKING_SAFE_EXIT",
))
NOTIFICATION_DISPOSITIONS = frozenset((
    "PLAY",
    "SUPPRESSED_CONSUMED",
    "DROPPED_CONSUMED",
    "DUPLICATE_NOOP",
    "INVALID",
))
_RAW_GROUP_RE = re.compile(r"^notify-group:v1:[0-9a-f]{64}$")
_SUMMARY_RE = re.compile(r"^notify-summary:v1:[0-9a-f]{64}$")


class NotificationContractError(ValueError):
    """Raised when a notification identity or transition violates v1."""


@dataclass(frozen=True)
class NotificationRawGroup:
    """The detached, non-persistent result of one durable membership batch."""

    notification_group_id: str
    collection_epoch_id: int
    checkpoint_occurrence_id: str
    added_achievement_ids: tuple[str, ...]
    added_ending_ids: tuple[str, ...]
    added_memory_ids: tuple[str, ...]


@dataclass(frozen=True)
class NotificationSummary:
    """An immutable safe-boundary summary passed to presenters/dispatcher."""

    notification_summary_id: str
    collection_epoch_id: int
    member_notification_group_ids: tuple[str, ...]


@dataclass(frozen=True)
class NotificationClaim:
    """One terminal, session-only occurrence record."""

    occurrence_id: str
    summary_id: str
    provenance: str
    disposition: str
    reason: str


@dataclass(frozen=True)
class NotificationDiagnostic:
    """Developer-only metadata; no player-facing copy is derived from it."""

    occurrence_id: str
    provenance: str
    disposition: str
    reason: str


@dataclass(frozen=True)
class NotificationSessionSnapshot:
    """Immutable value stored inside the Ren'Py session record by the owner."""

    pending_raw_groups: tuple[NotificationRawGroup, ...] = ()
    retired_group_ids: tuple[str, ...] = ()
    sealed_summaries: tuple[NotificationSummary, ...] = ()
    group_summary_pairs: tuple[tuple[str, str], ...] = ()
    claims: tuple[NotificationClaim, ...] = ()
    diagnostics: tuple[NotificationDiagnostic, ...] = ()
    load_quarantine: bool = False
    blocking_safe_exit: bool = False


@dataclass(frozen=True)
class NotificationDispatchDecision:
    """A claimed terminal decision; the caller may invoke a test sink for PLAY."""

    snapshot: NotificationSessionSnapshot
    occurrence_id: str
    disposition: str
    reason: str
    adapter_attempt_required: bool
    claimed_before_output_gate: bool


def _require_string(value: Any, field_name: str) -> str:
    if type(value) is not str or not value:
        raise NotificationContractError(field_name + " must be a non-empty exact string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise NotificationContractError(field_name + " must contain Unicode scalar values") from error
    return value


def _require_epoch(value: Any) -> int:
    if type(value) is not int or value < 0:
        raise NotificationContractError("collection_epoch_id must be a non-negative exact integer")
    return value


def utf8_byte_sort(values: Iterable[str]) -> tuple[str, ...]:
    """Freeze a tuple in the ADR-0007 byte ordering, not locale ordering."""

    return tuple(sorted(values, key=lambda value: value.encode("utf-8")))


def _normalise_ids(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, (tuple, list)):
        raise NotificationContractError(field_name + " must be a tuple/list")
    items = tuple(_require_string(value, field_name + " member") for value in values)
    if len(items) != len(set(items)):
        raise NotificationContractError(field_name + " must not contain duplicates")
    return utf8_byte_sort(items)


def canonical_json_bytes(value: Any) -> bytes:
    """Return the exact UTF-8-no-BOM-LF canonical JSON identity bytes."""

    def validate(node: Any) -> None:
        if node is None or type(node) in (bool, int, str):
            if type(node) is str:
                _require_string(node, "identity string")
            return
        if type(node) is float:
            raise NotificationContractError("floats are forbidden in identity inputs")
        if isinstance(node, (tuple, list)):
            for item in node:
                validate(item)
            return
        if isinstance(node, dict):
            for key, item in node.items():
                if type(key) is not str:
                    raise NotificationContractError("canonical JSON object keys must be strings")
                validate(item)
            return
        raise NotificationContractError("unsupported identity input type: " + type(node).__name__)

    validate(value)
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    if encoded.startswith(b"\xef\xbb\xbf") or b"\r" in encoded or b"\n" in encoded:
        raise NotificationContractError("identity bytes must be UTF-8 without BOM or line endings")
    return encoded


def make_notification_raw_group(
    *,
    collection_epoch_id: int,
    checkpoint_occurrence_id: str,
    added_achievement_ids: Iterable[str] = (),
    added_ending_ids: Iterable[str] = (),
    added_memory_ids: Iterable[str] = (),
) -> NotificationRawGroup:
    """Create the only permitted ``notify-group:v1`` durable-result ID."""

    epoch = _require_epoch(collection_epoch_id)
    checkpoint = _require_string(checkpoint_occurrence_id, "checkpoint_occurrence_id")
    achievements = _normalise_ids(added_achievement_ids, "added_achievement_ids")
    endings = _normalise_ids(added_ending_ids, "added_ending_ids")
    memories = _normalise_ids(added_memory_ids, "added_memory_ids")
    if not achievements and not endings and not memories:
        raise NotificationContractError("a raw notification group requires newly added membership")
    payload = {
        "version": RAW_GROUP_VERSION,
        "collection_epoch_id": epoch,
        "checkpoint_occurrence_id": checkpoint,
        "added_achievement_ids": list(achievements),
        "added_ending_ids": list(endings),
        "added_memory_ids": list(memories),
    }
    group_id = RAW_GROUP_PREFIX + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    return NotificationRawGroup(group_id, epoch, checkpoint, achievements, endings, memories)


def validate_notification_raw_group(value: Any) -> NotificationRawGroup:
    """Reject forged IDs or mutable/incorrect raw-group field combinations."""

    if type(value) is not NotificationRawGroup:
        raise NotificationContractError("notification raw group has an invalid type")
    expected = make_notification_raw_group(
        collection_epoch_id=value.collection_epoch_id,
        checkpoint_occurrence_id=value.checkpoint_occurrence_id,
        added_achievement_ids=value.added_achievement_ids,
        added_ending_ids=value.added_ending_ids,
        added_memory_ids=value.added_memory_ids,
    )
    if value != expected:
        raise NotificationContractError("notification raw group does not match its canonical identity")
    return expected


def _normalise_group_ids(group_ids: Iterable[str]) -> tuple[str, ...]:
    if not isinstance(group_ids, (tuple, list)):
        raise NotificationContractError("member_notification_group_ids must be a tuple/list")
    members = tuple(_require_string(value, "notification_group_id") for value in group_ids)
    if not members or len(members) != len(set(members)):
        raise NotificationContractError("summary members must be non-empty and unique")
    if any(_RAW_GROUP_RE.fullmatch(value) is None for value in members):
        raise NotificationContractError("summary member is not a notify-group:v1 identity")
    return utf8_byte_sort(members)


def make_notification_summary_from_group_ids(
    *, collection_epoch_id: int, member_notification_group_ids: Iterable[str]
) -> NotificationSummary:
    """Seal exactly one v1 summary from already-validated raw member IDs."""

    epoch = _require_epoch(collection_epoch_id)
    members = _normalise_group_ids(member_notification_group_ids)
    payload = {
        "version": SUMMARY_VERSION,
        "collection_epoch_id": epoch,
        "member_notification_group_ids": list(members),
    }
    summary_id = SUMMARY_PREFIX + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    return NotificationSummary(summary_id, epoch, members)


def make_notification_summary(raw_groups: Iterable[NotificationRawGroup]) -> NotificationSummary:
    """Validate same-epoch raw groups before deriving their immutable summary."""

    if not isinstance(raw_groups, (tuple, list)) or not raw_groups:
        raise NotificationContractError("a summary requires non-empty raw groups")
    groups = tuple(validate_notification_raw_group(group) for group in raw_groups)
    epochs = {group.collection_epoch_id for group in groups}
    if len(epochs) != 1:
        raise NotificationContractError("summary raw groups must share one collection epoch")
    return make_notification_summary_from_group_ids(
        collection_epoch_id=groups[0].collection_epoch_id,
        member_notification_group_ids=tuple(group.notification_group_id for group in groups),
    )


def validate_notification_summary(value: Any) -> NotificationSummary:
    """Recompute and verify a supplied sealed-summary identity."""

    if type(value) is not NotificationSummary:
        raise NotificationContractError("notification summary has an invalid type")
    expected = make_notification_summary_from_group_ids(
        collection_epoch_id=value.collection_epoch_id,
        member_notification_group_ids=value.member_notification_group_ids,
    )
    if value != expected:
        raise NotificationContractError("notification summary does not match its canonical identity")
    return expected


def notification_audio_occurrence_id(summary_id: str) -> str:
    """Return the only notification-audio occurrence identity form."""

    value = _require_string(summary_id, "notification_summary_id")
    if _SUMMARY_RE.fullmatch(value) is None:
        raise NotificationContractError("notification_summary_id is not a notify-summary:v1 identity")
    return OCCURRENCE_PREFIX + value


def notification_audio_preference_enabled(preferences: Mapping[str, Any]) -> bool:
    """Evaluate exactly the four approved notification eligibility inputs."""

    required = {
        "main_gain_bps",
        "global_game_mute",
        "environment_sfx_manual_mute",
        "environment_sfx_gain_bps",
    }
    allowed = required | {"music_manual_mute"}
    if type(preferences) is not dict or not required.issubset(preferences) or not set(preferences).issubset(allowed):
        raise NotificationContractError("notification preference shape is invalid")
    for field in ("main_gain_bps", "environment_sfx_gain_bps"):
        value = preferences[field]
        if type(value) is not int or value < 0 or value > 10000:
            raise NotificationContractError(field + " must be an integer basis-point value")
    for field in ("global_game_mute", "environment_sfx_manual_mute"):
        if type(preferences[field]) is not bool:
            raise NotificationContractError(field + " must be an exact bool")
    # Music mute is deliberately optional validation-only input.  It is never
    # read by the predicate, so a music-only change cannot alter eligibility.
    if "music_manual_mute" in preferences and type(preferences["music_manual_mute"]) is not bool:
        raise NotificationContractError("music_manual_mute must be an exact bool")
    return (
        not preferences["global_game_mute"]
        and preferences["main_gain_bps"] > 0
        and not preferences["environment_sfx_manual_mute"]
        and preferences["environment_sfx_gain_bps"] > 0
    )


def _validate_gates(gates: Mapping[str, Any]) -> Mapping[str, bool]:
    fields = {"asset_valid", "blocking_safe", "tts_active", "device_ready", "pool_admitted"}
    if type(gates) is not dict or set(gates) != fields:
        raise NotificationContractError("notification output-gate shape is invalid")
    if any(type(gates[field]) is not bool for field in fields):
        raise NotificationContractError("notification output gates must be exact bools")
    return gates


def new_notification_session_snapshot() -> NotificationSessionSnapshot:
    """Return the empty immutable value placed in the session-owned record."""

    return NotificationSessionSnapshot()


def _diagnose(
    snapshot: NotificationSessionSnapshot,
    occurrence_id: str,
    provenance: str,
    disposition: str,
    reason: str,
) -> NotificationSessionSnapshot:
    return replace(
        snapshot,
        diagnostics=snapshot.diagnostics + (
            NotificationDiagnostic(occurrence_id, provenance, disposition, reason),
        ),
    )


def queue_live_raw_group(
    snapshot: NotificationSessionSnapshot, raw_group: NotificationRawGroup
) -> tuple[NotificationSessionSnapshot, bool]:
    """Queue a durable live group once; retired/sealed groups cannot return."""

    if type(snapshot) is not NotificationSessionSnapshot:
        raise NotificationContractError("notification session snapshot has an invalid type")
    group = validate_notification_raw_group(raw_group)
    known = (
        {item.notification_group_id for item in snapshot.pending_raw_groups}
        | set(snapshot.retired_group_ids)
        | {pair[0] for pair in snapshot.group_summary_pairs}
    )
    if snapshot.load_quarantine or snapshot.blocking_safe_exit:
        reason = "LOAD_QUARANTINE" if snapshot.load_quarantine else "BLOCKING_SAFE_EXIT"
        updated = replace(snapshot, retired_group_ids=utf8_byte_sort(snapshot.retired_group_ids + (group.notification_group_id,)))
        return _diagnose(updated, "", LIVE_NOTIFICATION_SUMMARY, "SUPPRESSED_CONSUMED", reason), False
    if group.notification_group_id in known:
        return _diagnose(snapshot, "", LIVE_NOTIFICATION_SUMMARY, "DUPLICATE_NOOP", "RAW_GROUP_ALREADY_CONSUMED"), False
    return replace(snapshot, pending_raw_groups=snapshot.pending_raw_groups + (group,)), True


def _discard_pending(
    snapshot: NotificationSessionSnapshot, provenance: str, reason: str, *, load_quarantine: bool | None = None, blocking_safe_exit: bool | None = None
) -> NotificationSessionSnapshot:
    retired = utf8_byte_sort(
        snapshot.retired_group_ids
        + tuple(group.notification_group_id for group in snapshot.pending_raw_groups)
    )
    updated = replace(
        snapshot,
        pending_raw_groups=(),
        retired_group_ids=retired,
        load_quarantine=snapshot.load_quarantine if load_quarantine is None else load_quarantine,
        blocking_safe_exit=snapshot.blocking_safe_exit if blocking_safe_exit is None else blocking_safe_exit,
    )
    for group in snapshot.pending_raw_groups:
        updated = _diagnose(updated, "", provenance, "SUPPRESSED_CONSUMED", reason + ":" + group.notification_group_id)
    return updated


def enter_load_quarantine(snapshot: NotificationSessionSnapshot) -> NotificationSessionSnapshot:
    """Discard pending history and consume unclaimed sealed summaries without replay."""

    if type(snapshot) is not NotificationSessionSnapshot:
        raise NotificationContractError("notification session snapshot has an invalid type")
    return _consume_nonlive_work(
        snapshot,
        "LOAD_RECONSTRUCTION",
        "LOAD_QUARANTINE",
        load_quarantine=True,
    )


def _consume_nonlive_work(
    snapshot: NotificationSessionSnapshot,
    provenance: str,
    reason: str,
    *,
    load_quarantine: bool | None = None,
    blocking_safe_exit: bool | None = None,
) -> NotificationSessionSnapshot:
    """Retire pending work and claim every historical unclaimed summary once."""

    updated = _discard_pending(
        snapshot,
        provenance,
        reason,
        load_quarantine=load_quarantine,
        blocking_safe_exit=blocking_safe_exit,
    )
    claimed = {claim.occurrence_id for claim in updated.claims}
    for summary in updated.sealed_summaries:
        occurrence = notification_audio_occurrence_id(summary.notification_summary_id)
        if occurrence not in claimed:
            claim = NotificationClaim(
                occurrence,
                summary.notification_summary_id,
                provenance,
                "SUPPRESSED_CONSUMED",
                reason + "_HISTORICAL",
            )
            updated = replace(updated, claims=updated.claims + (claim,))
            updated = _diagnose(updated, occurrence, claim.provenance, claim.disposition, claim.reason)
            claimed.add(occurrence)
    return updated


def clear_load_quarantine_after_validation(snapshot: NotificationSessionSnapshot) -> NotificationSessionSnapshot:
    """Allow only future live arrivals after existing semantic validation succeeds."""

    if type(snapshot) is not NotificationSessionSnapshot:
        raise NotificationContractError("notification session snapshot has an invalid type")
    return replace(snapshot, load_quarantine=False)


def enter_blocking_safe_exit(snapshot: NotificationSessionSnapshot) -> NotificationSessionSnapshot:
    """Make a blocking-safe exit non-live and discard pending groups permanently."""

    if type(snapshot) is not NotificationSessionSnapshot:
        raise NotificationContractError("notification session snapshot has an invalid type")
    return _consume_nonlive_work(
        snapshot,
        "BLOCKING_SAFE_EXIT",
        "BLOCKING_SAFE_EXIT",
        blocking_safe_exit=True,
    )


def enter_rollback_reconstruction(snapshot: NotificationSessionSnapshot) -> NotificationSessionSnapshot:
    """Consume pre-rollback session work before a divergent branch can reuse it."""

    if type(snapshot) is not NotificationSessionSnapshot:
        raise NotificationContractError("notification session snapshot has an invalid type")
    return _consume_nonlive_work(
        snapshot,
        "ROLLBACK_RECONSTRUCTION",
        "ROLLBACK_RECONSTRUCTION",
    )


def begin_new_game_reconstruction(snapshot: NotificationSessionSnapshot) -> NotificationSessionSnapshot:
    """Retire an abandoned run, then admit only genuinely new future arrivals."""

    if type(snapshot) is not NotificationSessionSnapshot:
        raise NotificationContractError("notification session snapshot has an invalid type")
    updated = _consume_nonlive_work(
        snapshot,
        "NEW_GAME_RECONSTRUCTION",
        "NEW_GAME_RECONSTRUCTION",
    )
    # Old occurrence claims and retired group IDs are intentionally retained:
    # session history must never become a replay source.  A new game only
    # releases the two safety gates for future, newly durable live work.
    return replace(updated, load_quarantine=False, blocking_safe_exit=False)


def seal_pending_live_summary(
    snapshot: NotificationSessionSnapshot, *, rollback_active: bool = False
) -> tuple[NotificationSessionSnapshot, NotificationSummary | None]:
    """Seal all currently pending same-epoch groups once, or consume non-live work."""

    if type(snapshot) is not NotificationSessionSnapshot:
        raise NotificationContractError("notification session snapshot has an invalid type")
    if rollback_active:
        return _consume_nonlive_work(
            snapshot,
            "ROLLBACK_RECONSTRUCTION",
            "ROLLBACK_ACTIVE",
        ), None
    if snapshot.load_quarantine:
        return _consume_nonlive_work(
            snapshot,
            "LOAD_RECONSTRUCTION",
            "LOAD_QUARANTINE",
        ), None
    if snapshot.blocking_safe_exit:
        return _consume_nonlive_work(
            snapshot,
            "BLOCKING_SAFE_EXIT",
            "BLOCKING_SAFE_EXIT",
        ), None
    if not snapshot.pending_raw_groups:
        return snapshot, None
    try:
        summary = make_notification_summary(snapshot.pending_raw_groups)
    except NotificationContractError as error:
        return _diagnose(
            _discard_pending(snapshot, LIVE_NOTIFICATION_SUMMARY, "INVALID_PENDING_GROUP"),
            "",
            LIVE_NOTIFICATION_SUMMARY,
            "INVALID",
            str(error),
        ), None
    group_map = dict(snapshot.group_summary_pairs)
    summary_ids = {item.notification_summary_id for item in snapshot.sealed_summaries}
    if summary.notification_summary_id in summary_ids or any(
        member in group_map for member in summary.member_notification_group_ids
    ):
        return _diagnose(
            _discard_pending(snapshot, LIVE_NOTIFICATION_SUMMARY, "SEALED_MEMBERSHIP_CONFLICT"),
            "",
            LIVE_NOTIFICATION_SUMMARY,
            "INVALID",
            "SUMMARY_APPEND_SPLIT_OR_REGENERATION_REJECTED",
        ), None
    pairs = snapshot.group_summary_pairs + tuple(
        (member, summary.notification_summary_id)
        for member in summary.member_notification_group_ids
    )
    return replace(
        snapshot,
        pending_raw_groups=(),
        sealed_summaries=snapshot.sealed_summaries + (summary,),
        group_summary_pairs=tuple(sorted(pairs)),
    ), summary


def dispatch_sealed_summary(
    snapshot: NotificationSessionSnapshot,
    summary: NotificationSummary,
    *,
    provenance: str,
    preferences: Mapping[str, Any] | None,
    gates: Mapping[str, Any] | None,
    test_sink_available: bool,
) -> NotificationDispatchDecision:
    """Claim before all gates and return one legal terminal disposition."""

    if type(snapshot) is not NotificationSessionSnapshot:
        raise NotificationContractError("notification session snapshot has an invalid type")
    try:
        sealed = validate_notification_summary(summary)
    except NotificationContractError as error:
        invalid = _diagnose(snapshot, "", provenance, "INVALID", str(error))
        return NotificationDispatchDecision(invalid, "", "INVALID", str(error), False, False)
    if provenance != LIVE_NOTIFICATION_SUMMARY and provenance not in NONLIVE_PROVENANCES:
        invalid = _diagnose(snapshot, "", provenance, "INVALID", "UNKNOWN_PROVENANCE")
        return NotificationDispatchDecision(invalid, "", "INVALID", "UNKNOWN_PROVENANCE", False, False)
    if sealed not in snapshot.sealed_summaries:
        invalid = _diagnose(snapshot, "", provenance, "INVALID", "SUMMARY_NOT_SESSION_SEALED")
        return NotificationDispatchDecision(invalid, "", "INVALID", "SUMMARY_NOT_SESSION_SEALED", False, False)
    occurrence = notification_audio_occurrence_id(sealed.notification_summary_id)
    if any(claim.occurrence_id == occurrence for claim in snapshot.claims):
        duplicate = _diagnose(snapshot, occurrence, provenance, "DUPLICATE_NOOP", "OCCURRENCE_ALREADY_CLAIMED")
        return NotificationDispatchDecision(duplicate, occurrence, "DUPLICATE_NOOP", "OCCURRENCE_ALREADY_CLAIMED", False, False)

    # The session occurrence claim is installed before preferences, TTS, device,
    # load, blocking, pool, asset, or test-sink checks are considered.  The
    # terminal record replaces this provisional claim after those gates finish.
    provisional_claim = NotificationClaim(
        occurrence,
        sealed.notification_summary_id,
        provenance,
        "SUPPRESSED_CONSUMED",
        "CLAIMED_PRE_GATE",
    )
    claimed_snapshot = replace(snapshot, claims=snapshot.claims + (provisional_claim,))
    disposition = "SUPPRESSED_CONSUMED"
    reason = "NONLIVE_PROVENANCE"
    attempt = False
    if provenance == LIVE_NOTIFICATION_SUMMARY:
        if claimed_snapshot.load_quarantine:
            reason = "LOAD_QUARANTINE"
        elif claimed_snapshot.blocking_safe_exit:
            reason = "BLOCKING_SAFE_EXIT"
        elif preferences is None or gates is None:
            reason = "OUTPUT_INPUT_UNAVAILABLE"
        else:
            try:
                eligible = notification_audio_preference_enabled(preferences)
                gate_values = _validate_gates(gates)
            except NotificationContractError as error:
                eligible = False
                gate_values = None
                reason = "INVALID_OUTPUT_INPUT:" + str(error)
            if gate_values is not None:
                if not eligible:
                    reason = "PREFERENCE_DISABLED"
                elif not gate_values["asset_valid"]:
                    disposition = "INVALID"
                    reason = "ASSET_UNAVAILABLE"
                elif not gate_values["blocking_safe"]:
                    reason = "LOAD_OR_BLOCKING_QUARANTINE"
                elif gate_values["tts_active"]:
                    reason = "TTS_ACTIVE"
                elif not gate_values["device_ready"]:
                    reason = "NO_DEVICE"
                elif not gate_values["pool_admitted"]:
                    disposition = "DROPPED_CONSUMED"
                    reason = "POOL_DROP"
                elif not test_sink_available:
                    disposition = "INVALID"
                    reason = "NO_ADMITTED_OUTPUT_TARGET"
                else:
                    disposition = "PLAY"
                    reason = "TEST_SINK_DISPATCH"
                    attempt = True
    claim = NotificationClaim(occurrence, sealed.notification_summary_id, provenance, disposition, reason)
    updated = replace(claimed_snapshot, claims=claimed_snapshot.claims[:-1] + (claim,))
    updated = _diagnose(updated, occurrence, provenance, disposition, reason)
    return NotificationDispatchDecision(updated, occurrence, disposition, reason, attempt, True)
