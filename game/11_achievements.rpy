default achievement_popup_queue = []

init python:
    from modules.persist_projections import ACHIEVEMENT_IDS

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
        candidate = dict(root)
        candidate["achievement_ids"] = sorted(root["achievement_ids"] + [achievement_id])
        persistent.sys_persist_state = candidate
        if defer_popup:
            achievement_popup_queue = achievement_popup_queue + [achievement_id]
        return True

    def unlock_memory(memory_id):
        root = dict(persistent.sys_persist_state)
        if memory_id not in root["memory_ids"]:
            root["memory_ids"] = sorted(root["memory_ids"] + [memory_id])
            persistent.sys_persist_state = root

    def unlock_ending(ending_id):
        if ending_id not in ENDING_IDS:
            raise ValueError("Unknown ending ID: {}".format(ending_id))
        root = dict(persistent.sys_persist_state)
        if ending_id not in root["ending_ids"]:
            root["ending_ids"] = sorted(root["ending_ids"] + [ending_id])
            persistent.sys_persist_state = root
        renpy.save_persistent()
