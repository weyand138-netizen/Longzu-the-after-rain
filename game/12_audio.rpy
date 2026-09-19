# Session-only notification summary coordinator.  This Story intentionally
# admits no authored cue, asset, native `renpy.music` call, device probe, or
# player-facing audio setting.  It nevertheless makes the live durable-result
# handoff and no-replay boundary real so a later admitted adapter has one owner.

init python:
    import builtins
    import threading

    from modules.notification_contract import (
        LIVE_NOTIFICATION_SUMMARY,
        begin_new_game_reconstruction,
        clear_load_quarantine_after_validation,
        dispatch_sealed_summary,
        enter_blocking_safe_exit,
        enter_load_quarantine,
        enter_rollback_reconstruction,
        new_notification_session_snapshot,
        queue_live_raw_group,
        seal_pending_live_summary,
        validate_notification_summary,
    )
    from modules.notification_durable_batch import DurableNotificationResult
    from modules.persist_batch import APPLIED_FLUSHED

    _NOTIFICATION_SESSION_KEY = "longzu.audio_adapter:v1"
    _NOTIFICATION_TEST_CONFIG_KEY = "longzu.audio_adapter:test:v1"

    def _new_notification_session_record():
        """Build the exact mutable record stored only in ``renpy.session``."""

        return {
            "lock": threading.RLock(),
            "snapshot": new_notification_session_snapshot(),
            "generation": 0,
            # This is a transient visual receipt only. It carries no raw
            # membership, summary identity, claim, or retry information.
            "presentation_receipt_pending": False,
        }

    def _notification_session_record():
        """Return the sole mutable owner; never persist it in save/root state."""

        # ``dict.setdefault`` returns the already-installed record if another
        # presenter won first use.  This avoids the former get/create/assign
        # split that could hand two threads different RLocks.
        return renpy.session.setdefault(
            _NOTIFICATION_SESSION_KEY,
            _new_notification_session_record(),
        )

    def _notification_rollback_active():
        """Use the public transient guard only at this authored boundary."""

        try:
            return bool(renpy.in_rollback())
        except Exception:
            # This source-pinned boundary fails safely if the engine surface is
            # unavailable rather than attempting historical notification output.
            return True

    def queue_live_notification_group(result):
        """Accept only the raw group attached to a real APPLIED_FLUSHED result."""

        if type(result) is not DurableNotificationResult:
            return False
        if result.status != APPLIED_FLUSHED or result.raw_group is None:
            return False
        record = _notification_session_record()
        with record["lock"]:
            snapshot, queued = queue_live_raw_group(record["snapshot"], result.raw_group)
            record["snapshot"] = snapshot
            record["generation"] += 1
            return queued

    def notification_before_load_quarantine():
        """Discard pending live groups and preserve already claimed occurrences."""

        record = _notification_session_record()
        with record["lock"]:
            audio_adapter_enter_reconstruction("LOAD")
            record["snapshot"] = enter_load_quarantine(record["snapshot"])
            record["presentation_receipt_pending"] = False
            record["generation"] += 1

    def notification_after_load_semantic_validation_succeeded():
        """Release quarantine only after the existing 10_state validation passed."""

        record = _notification_session_record()
        with record["lock"]:
            audio_adapter_load_semantics_validated()
            record["snapshot"] = clear_load_quarantine_after_validation(record["snapshot"])
            record["presentation_receipt_pending"] = False
            record["generation"] += 1

    def notification_enter_blocking_safe_exit():
        """Make a blocking-safe exit permanently non-live for pending groups."""

        record = _notification_session_record()
        with record["lock"]:
            audio_adapter_enter_reconstruction("BLOCKING")
            record["snapshot"] = enter_blocking_safe_exit(record["snapshot"])
            record["presentation_receipt_pending"] = False
            record["generation"] += 1

    def notification_after_rollback_reconstruction():
        """Retire historical session work as soon as Ren'Py restores a rollback."""

        record = _notification_session_record()
        with record["lock"]:
            audio_adapter_enter_reconstruction("ROLLBACK")
            record["snapshot"] = enter_rollback_reconstruction(record["snapshot"])
            record["presentation_receipt_pending"] = False
            record["generation"] += 1

    def notification_begin_new_run():
        """Discard an abandoned run without making future live work permanently silent."""

        record = _notification_session_record()
        with record["lock"]:
            audio_adapter_enter_reconstruction("NEW_RUN")
            record["snapshot"] = begin_new_game_reconstruction(record["snapshot"])
            record["presentation_receipt_pending"] = False
            record["generation"] += 1

    def _present_sealed_summary_locked(record, summary):
        """Accept one validated summary without retaining its identity in UI state."""

        validated = validate_notification_summary(summary)
        # The existing completion cards consume only this ephemeral visual
        # receipt. They never receive raw groups, construct IDs, claim audio,
        # or retain a second dedupe ledger.
        record["presentation_receipt_pending"] = True
        return validated

    def notification_present_sealed_summary(summary):
        """Give a real visual presenter bridge one sealed summary only."""

        record = _notification_session_record()
        with record["lock"]:
            return _present_sealed_summary_locked(record, summary)

    def notification_current_presentation_receipt():
        """Expose only whether the current completion UI has a live receipt."""

        record = _notification_session_record()
        with record["lock"]:
            return record["presentation_receipt_pending"]

    def notification_clear_presentation_receipt():
        """Dismiss the transient visual receipt with its completion card."""

        record = _notification_session_record()
        with record["lock"]:
            was_pending = record["presentation_receipt_pending"]
            record["presentation_receipt_pending"] = False
            return was_pending

    def _notification_test_dispatch_config():
        """Expose a sink only to the Ren'Py ``test`` command, never gameplay."""

        try:
            if renpy.game.args.command != "test":
                return None
        except Exception:
            return None
        config_record = renpy.session.get(_NOTIFICATION_TEST_CONFIG_KEY)
        if not isinstance(config_record, dict):
            return None
        if set(config_record) != {"preferences", "gates", "sink"}:
            return None
        if not isinstance(config_record["preferences"], dict):
            return None
        if not isinstance(config_record["gates"], dict):
            return None
        if not isinstance(config_record["sink"], list):
            return None
        # Testcase values pass through Ren'Py's rollback container machinery;
        # detach them back to exact built-in dicts before the pure contract's
        # strict shape/type validation. The sink itself remains test-only.
        return {
            "preferences": builtins.dict(config_record["preferences"]),
            "gates": builtins.dict(config_record["gates"]),
            "sink": config_record["sink"],
        }

    def _dispatch_notification_summary(summary):
        """The one central dispatcher callsite; no production output target exists yet."""

        record = _notification_session_record()
        with record["lock"]:
            test_config = _notification_test_dispatch_config()
            decision = dispatch_sealed_summary(
                record["snapshot"],
                summary,
                provenance=LIVE_NOTIFICATION_SUMMARY,
                preferences=None if test_config is None else test_config["preferences"],
                gates=None if test_config is None else test_config["gates"],
                test_sink_available=test_config is not None,
            )
            record["snapshot"] = decision.snapshot
            record["generation"] += 1
            if decision.adapter_attempt_required:
                # This is an ADR-0007-isolated test record, not a cue, asset,
                # native audio call, device probe, or player-visible feature.
                test_config["sink"].append(decision.occurrence_id)
            return decision

    def notification_presentation_safe_boundary_dispatch():
        """Seal current live arrivals once, then give the immutable summary to both owners."""

        record = _notification_session_record()
        with record["lock"]:
            # A previous card must not be re-rendered at this new boundary.
            record["presentation_receipt_pending"] = False
            snapshot, summary = seal_pending_live_summary(
                record["snapshot"],
                rollback_active=_notification_rollback_active(),
            )
            record["snapshot"] = snapshot
            record["generation"] += 1
            if summary is not None:
                summary = _present_sealed_summary_locked(record, summary)
        if summary is None:
            return None
        # Existing chapter/ending cards read the session-only visual receipt
        # even when the following dispatcher conservatively consumes sound.
        return _dispatch_notification_summary(summary)

    def notification_developer_diagnostics():
        """Expose developer-only immutable diagnostics without player UI wiring."""

        record = _notification_session_record()
        with record["lock"]:
            return record["snapshot"].diagnostics

    def _notification_after_default_rollback_observer():
        """Ren'Py 8.5.3 invokes after-default callbacks after rollback restore."""

        try:
            rollback_restored = bool(renpy.game.after_rollback)
        except Exception:
            rollback_restored = False
        if rollback_restored:
            notification_after_rollback_reconstruction()

    if _notification_after_default_rollback_observer not in config.after_default_callbacks:
        config.after_default_callbacks.append(_notification_after_default_rollback_observer)


label before_load:
    $ notification_before_load_quarantine()
    return


label notification_presentation_safe_boundary:
    $ notification_presentation_safe_boundary_dispatch()
    return
