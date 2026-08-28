default achievement_popup_queue = []

init python:
    import builtins

    from modules.persist_projections import ACHIEVEMENT_IDS
    from modules.persist_schema import snapshot_persist_root

    ACHIEVEMENTS = {
        achievement_id: (achievement_id.replace("_", " "), False)
        for achievement_id in ACHIEVEMENT_IDS
    }

    ENDING_IDS = (
        "unsent_postcard", "golden_cage", "one_person_train",
        "see_the_sea", "her_own_name", "rain_stops",
    )

    for achievement_id in ACHIEVEMENT_IDS:
        achievement.register(achievement_id)

    def grant_local_achievement(achievement_id, defer_popup=True):
        global achievement_popup_queue
        if achievement_id not in ACHIEVEMENT_IDS:
            raise ValueError("Unknown achievement ID: {}".format(achievement_id))
        root = persistent.sys_persist_state
        if achievement_id in root["achievement_ids"]:
            return False
        achievement.grant(achievement_id)
        candidate = snapshot_persist_root(root)
        candidate["achievement_ids"] = builtins.sorted(
            builtins.tuple(candidate["achievement_ids"]) + (achievement_id,)
        )
        persistent.sys_persist_state = candidate
        persistent.settings = candidate["settings"]
        if defer_popup:
            achievement_popup_queue = achievement_popup_queue + [achievement_id]
        return True

    def unlock_memory(memory_id):
        candidate = snapshot_persist_root(persistent.sys_persist_state)
        if memory_id not in candidate["memory_ids"]:
            candidate["memory_ids"] = builtins.sorted(
                builtins.tuple(candidate["memory_ids"]) + (memory_id,)
            )
            persistent.sys_persist_state = candidate
            persistent.settings = candidate["settings"]

    def unlock_ending(ending_id):
        if ending_id not in ENDING_IDS:
            raise ValueError("Unknown ending ID: {}".format(ending_id))
        candidate = snapshot_persist_root(persistent.sys_persist_state)
        if ending_id not in candidate["ending_ids"]:
            candidate["ending_ids"] = builtins.sorted(
                builtins.tuple(candidate["ending_ids"]) + (ending_id,)
            )
            persistent.sys_persist_state = candidate
            persistent.settings = candidate["settings"]
        renpy.save_persistent()
