default achievement_popup_queue = []

init python:
    from modules.ending_rules import ENDING_PRIORITY
    from modules.notification_durable_batch import MEMORY_IDS
    from modules.persist_batch import APPLIED_FLUSHED
    from modules.persist_projections import ACHIEVEMENT_IDS

    ACHIEVEMENTS = {
        achievement_id: (achievement_id.replace("_", " "), False)
        for achievement_id in ACHIEVEMENT_IDS
    }

    ENDING_IDS = ENDING_PRIORITY

    for achievement_id in ACHIEVEMENT_IDS:
        achievement.register(achievement_id)

    def _queue_durable_notification_result(result):
        """Give only a proven live durable result to the session coordinator."""

        if result.status == APPLIED_FLUSHED and result.raw_group is not None:
            queue_live_notification_group(result)

    def _commit_notification_membership(
        checkpoint_occurrence_id,
        achievement_ids=(),
        ending_ids=(),
        memory_ids=(),
    ):
        """Use the sole 10_state root owner for all live membership categories."""

        return commit_notification_membership(
            checkpoint_occurrence_id=checkpoint_occurrence_id,
            achievement_ids=achievement_ids,
            ending_ids=ending_ids,
            memory_ids=memory_ids,
        )

    def grant_local_achievement(achievement_id, defer_popup=True):
        global achievement_popup_queue
        if achievement_id not in ACHIEVEMENT_IDS:
            raise ValueError("Unknown achievement ID: {}".format(achievement_id))
        result = _commit_notification_membership(
            "achievement:{}:1".format(achievement_id),
            achievement_ids=(achievement_id,),
        )
        if result.status != APPLIED_FLUSHED:
            return False
        achievement.grant(achievement_id)
        if defer_popup:
            achievement_popup_queue = achievement_popup_queue + [achievement_id]
        _queue_durable_notification_result(result)
        return True

    def unlock_memory(memory_id):
        if memory_id not in MEMORY_IDS:
            # The live prologue still uses its historical ``PROLOGUE`` callsite,
            # but the approved catalog contains only Day 1–7 memory IDs. Do not
            # turn an unapproved narrative location into a durable root entry.
            return False
        result = _commit_notification_membership(
            "memory:{}:1".format(memory_id),
            memory_ids=(memory_id,),
        )
        _queue_durable_notification_result(result)
        return result.status == APPLIED_FLUSHED

    def unlock_ending(ending_id):
        if ending_id not in ENDING_IDS:
            raise ValueError("Unknown ending ID: {}".format(ending_id))
        result = _commit_notification_membership(
            "ending:{}:1".format(ending_id),
            ending_ids=(ending_id,),
        )
        _queue_durable_notification_result(result)
        return result.status == APPLIED_FLUSHED
