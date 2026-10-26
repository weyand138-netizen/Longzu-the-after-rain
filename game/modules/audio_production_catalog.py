"""The explicit admission list for the internal audio scene-audition build.

This data is intentionally explicit.  It is based on the narrated setting and
the named action at each source position, never on a background asset name.
No entry carries an output gain. Existing assets retain their reviewed bytes;
the six 2026-10-24 additions reuse original drafts for internal scene audition,
not a claim of physical-device listening or release approval.
"""
from .audio_catalog import AudioAssetRecord, AudioContextRange, AudioOneShotBinding
from .audio_continuous import ContinuousCue
from .audio_oneshot import OneShotCue


RUNTIME_AUDIO_ASSETS = (
    AudioAssetRecord("music.menu_rain", "assets/audio/music/m01_menu_rain.ogg", "3b83018ae5367e7295500605e13ecfa48e7e39c20483ca0a685f99e70036a97e"),
    AudioAssetRecord("music.visible_departure", "assets/audio/music/m02_visible_departure.ogg", "bb5e4124c2e89d02aac6e334272894b217b1de903e6aa951a06eef29d8fcd08f"),
    AudioAssetRecord("music.daily_room", "assets/audio/music/m03_daily_room.ogg", "2593b3406f47356d5af1985af9cf81b0670ac86bb2da0fc38b56a1234f36e6bb"),
    AudioAssetRecord("music.city_pause", "assets/audio/music/m04_city_pause.ogg", "6730855f04776d7c039b75cd6e8ce632a26bc52a5491ac4acf8b10d9cb25dacf"),
    AudioAssetRecord("music.archive_space", "assets/audio/music/m05_archive_space.ogg", "dac1775cad58b7aa2b5436427a1c450bf2aa711e51c61ba8403e9b33b44d9e89"),
    AudioAssetRecord("music.before_departure", "assets/audio/music/m06_before_departure.ogg", "0634c47a41e82f81a776b46270935ef0ea1c54ca10bf891eae2d1540b8348f11"),
    AudioAssetRecord("music.after_rain", "assets/audio/music/m07_after_rain.ogg", "03be7c6253a4d7d2ef6aa94ca13415f597d8cb3283732af72f6154cfc47624bc"),
    AudioAssetRecord("music.life_continues", "assets/audio/music/m08_life_continues.ogg", "8da9a5cf622c8961036fda69ce563df13baad93085ee3f0e3f15a351115c9a39"),
    AudioAssetRecord("ambience.rain_platform", "assets/audio/ambience/a01_rain_platform.ogg", "b2611bdfb693bed2df6f80b0db948319ce2d48fe9ebe2d77c5fc9ada364fa120"),
    AudioAssetRecord("ambience.room_rain", "assets/audio/ambience/a02_room_rain.ogg", "f805af352b9192723ea0a53285b67a83d062385942e823da2593cd3ee68f7e81"),
    AudioAssetRecord("ambience.internet_cafe", "assets/audio/ambience/a03_internet_cafe.ogg", "047f4505349e65b3ada047ad330a90ac680635a2b5ea7d851971822002855cc7"),
    AudioAssetRecord("ambience.empty_classroom", "assets/audio/ambience/a04_empty_classroom.ogg", "51b3e8aaa4494f8c78bed08d3dc1591bd71881bdbde9ea56585d601a22f3ff10"),
    AudioAssetRecord("ambience.train_carriage", "assets/audio/ambience/a05_train_carriage.ogg", "59b3c00496ef4b6c96c5eb9ae90a62fcc60b061728cfebd2b87e298a0e830643"),
    AudioAssetRecord("ambience.seaside", "assets/audio/ambience/a06_seaside.ogg", "3c071344937e7c4d4fd65fe59fd220fe3ad0453962cc12a2a1ef5d4490116404"),
    AudioAssetRecord("ambience.service_exit", "assets/audio/ambience/a07_service_exit.ogg", "977a6634505b92283a34b3caa1c8985795a5fff428cabc025493543d7dcf0381"),
    AudioAssetRecord("ambience.red_well", "assets/audio/ambience/a08_red_well.ogg", "fbd69264bf39f3b44a8a12aa4ac043168522366327816e2df46e03d49eaab89e"),
    AudioAssetRecord("sfx.paper_unfold", "assets/audio/sfx/s01_paper_unfold.wav", "abb62a90c8a853b4f55c461eed90fbfac900dc76050e6189719c4e955416a7b0"),
    AudioAssetRecord("sfx.paper_fold", "assets/audio/sfx/s02_paper_fold.wav", "97c8e9de5a8d5428975344c2767cefb166e9d237ca16b099539a341ee384ca5f"),
    AudioAssetRecord("sfx.cloth_shift", "assets/audio/sfx/s04_cloth_shift.wav", "410b5118c5e57bc8062f5a1a6c60a95c569edcaed2367aa96c4bb206c3ed5232"),
    AudioAssetRecord("sfx.wet_step", "assets/audio/sfx/s05_step_wet.wav", "e62c0ab9916c63401c3aa181458979279d0bfb5bf85e96d2c66f649adea95074"),
    AudioAssetRecord("sfx.interior_step", "assets/audio/sfx/s06_step_interior.wav", "cfb7e7e2a9db6ed8e4f7f9c23f93c95543bce193e2fee3bfa47cac2174d44dde"),
    AudioAssetRecord("sfx.two_coins", "assets/audio/sfx/s09_two_coins.wav", "afaa0bf95e190832ebb21776a262b5003de7878f14a28608dc80bbb7101b99cf"),
    AudioAssetRecord("sfx.keyboard", "assets/audio/sfx/s10_keyboard.wav", "4556a600f5fd4e154850fbfd75529cd13305de23c47f1b282764cf14d1ad585d"),
    AudioAssetRecord("sfx.pencil_write", "assets/audio/sfx/s03_pencil_write.wav", "ec2605b49e51945e41d13742fb4feef3d787234802792c957a0c99cfbd6d6d3b"),
    AudioAssetRecord("sfx.door_soft", "assets/audio/sfx/s07_door_soft.wav", "1c56abf856efc99e9925f218cdb2313f283f6cdb1f912197f6993adaf77ec7ac"),
    AudioAssetRecord("sfx.ticket_handle", "assets/audio/sfx/s12_ticket_take.wav", "0fbf35c5e175e5d226a02708e6f0baa95459d3c20e212cd93565d30a33ab3751"),
    AudioAssetRecord("sfx.train_latch", "assets/audio/sfx/s13_train_latch.wav", "ce82360e70e0e18a57db2e672aa8923b0fa9fcbb1d3401b5ebab85ca7508e3e0"),
    AudioAssetRecord("sfx.object_place", "assets/audio/sfx/s14_object_place.wav", "6cad43a3d58577bcad072028552f6c81e4cda431dd2f05f35af186edde854f08"),
    AudioAssetRecord("notification.neutral_contact", "assets/audio/sfx/n01_neutral_contact.wav", "f6f458d4d220725c6adb38b7442640876b705acaa785aaa5b88023eb00fc7ecd"),
    AudioAssetRecord("sfx.ui_click_soft", "assets/audio/sfx/ui_click_soft.wav", "ea3e085f926ae38a0f31d16ae661fcaf0589a1cad55dc9e464b3e8dab83324fe"),
    AudioAssetRecord("sfx.ui_choice_confirm", "assets/audio/sfx/ui_choice_confirm.wav", "37db8cd1785631c80d8d00858b911acdf8c44ecb662dea7bd5a75181ca6271f3"),
)


CONTINUOUS_CUES = (
    ContinuousCue("audio.music.menu_rain", "music", "assets/audio/music/m01_menu_rain.ogg", 1.0),
    ContinuousCue("audio.music.visible_departure", "music", "assets/audio/music/m02_visible_departure.ogg", 1.0),
    ContinuousCue("audio.music.daily_room", "music", "assets/audio/music/m03_daily_room.ogg", 1.0),
    ContinuousCue("audio.music.city_pause", "music", "assets/audio/music/m04_city_pause.ogg", 1.0),
    ContinuousCue("audio.music.archive_space", "music", "assets/audio/music/m05_archive_space.ogg", 1.0),
    ContinuousCue("audio.music.before_departure", "music", "assets/audio/music/m06_before_departure.ogg", 1.0),
    ContinuousCue("audio.music.after_rain", "music", "assets/audio/music/m07_after_rain.ogg", 1.0),
    ContinuousCue("audio.music.life_continues", "music", "assets/audio/music/m08_life_continues.ogg", 1.0),
    ContinuousCue("audio.ambience.rain_platform", "ambience", "assets/audio/ambience/a01_rain_platform.ogg", 0.75),
    ContinuousCue("audio.ambience.room_rain", "ambience", "assets/audio/ambience/a02_room_rain.ogg", 0.75),
    ContinuousCue("audio.ambience.internet_cafe", "ambience", "assets/audio/ambience/a03_internet_cafe.ogg", 0.75),
    ContinuousCue("audio.ambience.empty_classroom", "ambience", "assets/audio/ambience/a04_empty_classroom.ogg", 0.75),
    ContinuousCue("audio.ambience.train_carriage", "ambience", "assets/audio/ambience/a05_train_carriage.ogg", 0.75),
    ContinuousCue("audio.ambience.seaside", "ambience", "assets/audio/ambience/a06_seaside.ogg", 0.75),
    ContinuousCue("audio.ambience.service_exit", "ambience", "assets/audio/ambience/a07_service_exit.ogg", 0.75),
    ContinuousCue("audio.ambience.red_well", "ambience", "assets/audio/ambience/a08_red_well.ogg", 0.75),
    # These are intentional documented quiet environments, not missing work.
    ContinuousCue("audio.ambience.intentional_silence", "ambience", None, 0.75),
)


ONESHOT_CUES = (
    OneShotCue("audio.sfx.paper_unfold", "assets/audio/sfx/s01_paper_unfold.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.paper_fold", "assets/audio/sfx/s02_paper_fold.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.cloth_shift", "assets/audio/sfx/s04_cloth_shift.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.wet_step", "assets/audio/sfx/s05_step_wet.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.interior_step", "assets/audio/sfx/s06_step_interior.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.two_coins", "assets/audio/sfx/s09_two_coins.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.keyboard", "assets/audio/sfx/s10_keyboard.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.pencil_write", "assets/audio/sfx/s03_pencil_write.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.door_soft", "assets/audio/sfx/s07_door_soft.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.ticket_handle", "assets/audio/sfx/s12_ticket_take.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.train_latch", "assets/audio/sfx/s13_train_latch.wav", "DECORATIVE"),
    OneShotCue("audio.sfx.object_place", "assets/audio/sfx/s14_object_place.wav", "DECORATIVE"),
    OneShotCue("audio.ui.click_soft", "assets/audio/sfx/ui_click_soft.wav", "OPTIONAL_UI_NOTIFICATION"),
    OneShotCue("audio.ui.choice_confirm", "assets/audio/sfx/ui_choice_confirm.wav", "OPTIONAL_UI_NOTIFICATION"),
    # Only the sealed notification-summary owner may dispatch this cue. It is
    # never a narrative action or a choice/outcome reward.
    OneShotCue("audio.notification.neutral_contact", "assets/audio/sfx/n01_neutral_contact.wav", "OPTIONAL_UI_NOTIFICATION"),
)


RESTORE_CONTEXTS = {
    "audio.context.title": ("audio.music.menu_rain", "audio.ambience.rain_platform"),
    "audio.context.prologue.platform": ("audio.music.visible_departure", "audio.ambience.rain_platform"),
    "audio.context.prologue.ticket_gate": ("audio.music.visible_departure", "audio.ambience.rain_platform"),
    "audio.context.prologue.train": ("audio.music.visible_departure", "audio.ambience.train_carriage"),
    # Day 1 is explicitly the quiet rain-dampened shop described by the text;
    # its background filename is not used as a sound classification signal.
    "audio.context.day1.shop_rain": ("audio.music.daily_room", "audio.ambience.room_rain"),
    "audio.context.day1.safehouse": ("audio.music.daily_room", "audio.ambience.room_rain"),
    "audio.context.day1.departure": ("audio.music.daily_room", "audio.ambience.rain_platform"),
    "audio.context.day2.arcade": ("audio.music.city_pause", "audio.ambience.internet_cafe"),
    "audio.context.day2.mall_exterior": ("audio.music.city_pause", "audio.ambience.rain_platform"),
    "audio.context.day3.classroom": ("audio.music.city_pause", "audio.ambience.empty_classroom"),
    "audio.context.day3.departure": ("audio.music.city_pause", "audio.ambience.intentional_silence"),
    "audio.context.day4.ticket_window": ("audio.music.visible_departure", "audio.ambience.rain_platform"),
    "audio.context.day4.seaside_station": ("audio.music.before_departure", "audio.ambience.seaside"),
    "audio.context.day4.coastal_train": ("audio.music.before_departure", "audio.ambience.train_carriage"),
    "audio.context.day5.archive_quiet": ("audio.music.archive_space", "audio.ambience.intentional_silence"),
    "audio.context.day5.departure": ("audio.music.archive_space", "audio.ambience.intentional_silence"),
    "audio.context.day6.service_exit": ("audio.music.before_departure", "audio.ambience.service_exit"),
    "audio.context.day6.departure": ("audio.music.before_departure", "audio.ambience.intentional_silence"),
    "audio.context.day7.red_well": ("audio.music.before_departure", "audio.ambience.red_well"),
    # Ending contexts keep their gains and one-shot policy identical: none is
    # sonically framed as a reward or as a worse outcome.
    "audio.context.ending.rain_stops": ("audio.music.after_rain", "audio.ambience.intentional_silence"),
    "audio.context.ending.her_own_name": ("audio.music.life_continues", "audio.ambience.rain_platform"),
    "audio.context.ending.her_own_name.train": ("audio.music.life_continues", "audio.ambience.train_carriage"),
    "audio.context.ending.see_the_sea.train": ("audio.music.after_rain", "audio.ambience.train_carriage"),
    "audio.context.ending.see_the_sea": ("audio.music.after_rain", "audio.ambience.seaside"),
    "audio.context.ending.one_person_train": ("audio.music.before_departure", "audio.ambience.rain_platform"),
    "audio.context.ending.one_person_train.train": ("audio.music.before_departure", "audio.ambience.train_carriage"),
    # The epilogue cuts to a departed observer / a paper-covered table and
    # finally a summary. No rain or room sound is established in those views.
    "audio.context.ending.one_person_train.quiet": ("audio.music.before_departure", "audio.ambience.intentional_silence"),
    "audio.context.ending.golden_cage": ("audio.music.archive_space", "audio.ambience.intentional_silence"),
    "audio.context.ending.unsent_postcard": ("audio.music.archive_space", "audio.ambience.room_rain"),
    "audio.context.epilogue.arcade": ("audio.music.life_continues", "audio.ambience.internet_cafe"),
    "audio.context.epilogue.closed": ("audio.music.life_continues", "audio.ambience.intentional_silence"),
}


_SOURCE_DIGESTS = {
    "chapters/prologue.rpy": "38e03185fbd106473edb1b032930ea79d5fe9bb0df34acd02325f9d6042caa1a",
    "chapters/day1.rpy": "ec75a288458d11b87858938f0d9351b75725c07bf8bffb8ef94bb50d046d6b6a",
    "chapters/day2.rpy": "e2344f7e413ef5a06000cbcdd3c09e72f8cbb5bd84f498e44675c718dfa495c8",
    "chapters/day3.rpy": "252f3f8bd9b79af67e1d7c52f7d953068be1226360314d03ace22e2e76bbc45a",
    "chapters/day4.rpy": "fc5d8b8a8fb45eb2d64d314a9a50e53119d92d73946afca0a25f3872edb4d13b",
    "chapters/day5.rpy": "48248d5e2fab5a549204f592d94087a5c117eaec31ce56e31986209cbc2b4ce7",
    "chapters/day6.rpy": "75d002a86f9e9d0dbc1dbc3927ef0ee88b39bc00aa984fb887d6f82860bbfd96",
    "chapters/day7.rpy": "69da9fcf9e20f3f9300fcecc01166d8782d0ce0977b86b402f66ccdc645d515c",
    "chapters/endings.rpy": "1fcdf7e670cc5a8f21a4cc56dc28165b081ca758eb4b12a4065d2d21ed904382",
}


def _range(source, first_line, last_line, context_id):
    return AudioContextRange(source, first_line, last_line, _SOURCE_DIGESTS[source], context_id)


CONTEXT_RANGES = (
    _range("chapters/prologue.rpy", 1, 112, "audio.context.prologue.platform"),
    _range("chapters/prologue.rpy", 113, 149, "audio.context.prologue.ticket_gate"),
    _range("chapters/prologue.rpy", 150, 182, "audio.context.prologue.train"),
    _range("chapters/day1.rpy", 1, 62, "audio.context.day1.shop_rain"),
    _range("chapters/day1.rpy", 63, 163, "audio.context.day1.safehouse"),
    _range("chapters/day1.rpy", 164, 169, "audio.context.day1.departure"),
    _range("chapters/day2.rpy", 1, 182, "audio.context.day2.arcade"),
    _range("chapters/day2.rpy", 183, 207, "audio.context.day2.mall_exterior"),
    _range("chapters/day3.rpy", 1, 159, "audio.context.day3.classroom"),
    _range("chapters/day3.rpy", 160, 173, "audio.context.day3.departure"),
    _range("chapters/day4.rpy", 1, 214, "audio.context.day4.ticket_window"),
    _range("chapters/day4.rpy", 215, 219, "audio.context.day4.seaside_station"),
    _range("chapters/day4.rpy", 220, 243, "audio.context.day4.coastal_train"),
    _range("chapters/day5.rpy", 1, 308, "audio.context.day5.archive_quiet"),
    _range("chapters/day5.rpy", 309, 316, "audio.context.day5.departure"),
    _range("chapters/day6.rpy", 1, 351, "audio.context.day6.service_exit"),
    _range("chapters/day6.rpy", 352, 364, "audio.context.day6.departure"),
    _range("chapters/day7.rpy", 1, 87, "audio.context.day7.red_well"),
    _range("chapters/endings.rpy", 1, 43, "audio.context.ending.rain_stops"),
    # Epilogues follow the currently narrated space without adding a one-shot,
    # gain override, or outcome-specific reward cue. Brief references to an
    # absent person do not change the space; an explicit focal cut does.
    _range("chapters/endings.rpy", 44, 75, "audio.context.ending.her_own_name"),
    _range("chapters/endings.rpy", 76, 101, "audio.context.ending.her_own_name.train"),
    # Seeing the sea through a moving train window is still a carriage. The
    # actual alighting scene starts at 124, after the doors open in line 123.
    _range("chapters/endings.rpy", 102, 123, "audio.context.ending.see_the_sea.train"),
    _range("chapters/endings.rpy", 124, 157, "audio.context.ending.see_the_sea"),
    _range("chapters/endings.rpy", 158, 189, "audio.context.ending.one_person_train"),
    # Coherent focal paragraphs, not every passing mention of a train or a
    # platform. The off-train cuts never infer an unestablished rain bed.
    _range("chapters/endings.rpy", 190, 199, "audio.context.ending.one_person_train.train"),
    _range("chapters/endings.rpy", 200, 201, "audio.context.ending.one_person_train.quiet"),
    _range("chapters/endings.rpy", 202, 203, "audio.context.ending.one_person_train.train"),
    _range("chapters/endings.rpy", 204, 206, "audio.context.ending.one_person_train.quiet"),
    _range("chapters/endings.rpy", 207, 207, "audio.context.ending.one_person_train.train"),
    _range("chapters/endings.rpy", 208, 214, "audio.context.ending.one_person_train.quiet"),
    _range("chapters/endings.rpy", 215, 270, "audio.context.ending.golden_cage"),
    _range("chapters/endings.rpy", 271, 326, "audio.context.ending.unsent_postcard"),
    _range("chapters/endings.rpy", 327, 349, "audio.context.epilogue.arcade"),
    _range("chapters/endings.rpy", 350, 360, "audio.context.epilogue.closed"),
    _range("chapters/endings.rpy", 361, 364, "audio.context.epilogue.closed"),
    _range("chapters/endings.rpy", 365, 372, "audio.context.epilogue.arcade"),
    _range("chapters/endings.rpy", 373, 377, "audio.context.epilogue.closed"),
    _range("chapters/endings.rpy", 378, 384, "audio.context.epilogue.arcade"),
    _range("chapters/endings.rpy", 385, 393, "audio.context.epilogue.closed"),
)


ACTION_BINDINGS = (
    AudioOneShotBinding("day1.cloth_shift", "chapters/day1.rpy", 76, "audio.sfx.cloth_shift"),
    AudioOneShotBinding("day1.paper_fold", "chapters/day1.rpy", 158, "audio.sfx.paper_fold"),
    AudioOneShotBinding("day1.wet_step", "chapters/day1.rpy", 167, "audio.sfx.wet_step"),
    AudioOneShotBinding("day2.keyboard", "chapters/day2.rpy", 72, "audio.sfx.keyboard"),
    AudioOneShotBinding("day2.two_coins", "chapters/day2.rpy", 121, "audio.sfx.two_coins"),
    AudioOneShotBinding("day2.interior_step", "chapters/day2.rpy", 175, "audio.sfx.interior_step"),
    AudioOneShotBinding("day4.paper_unfold", "chapters/day4.rpy", 118, "audio.sfx.paper_unfold"),
    # One event per selected visible physical action, not a keyword mapper.
    # The source only says "pen"; the historical asset name does not establish
    # pencil material. These two shared scenes perform actual writing.
    AudioOneShotBinding("day3.write_note", "chapters/day3.rpy", 76, "audio.sfx.pencil_write"),
    AudioOneShotBinding("day5.write_plan", "chapters/day5.rpy", 199, "audio.sfx.pencil_write"),
    AudioOneShotBinding("day6.door_soft", "chapters/day6.rpy", 349, "audio.sfx.door_soft"),
    # Single and double tickets receive the same one-time paper sound when
    # finally put away, without a gain, priority, or quality distinction.
    AudioOneShotBinding("day4.ticket_handle_two", "chapters/day4.rpy", 140, "audio.sfx.ticket_handle"),
    AudioOneShotBinding("day4.ticket_handle_single", "chapters/day4.rpy", 156, "audio.sfx.ticket_handle"),
    AudioOneShotBinding("prologue.train_latch", "chapters/prologue.rpy", 153, "audio.sfx.train_latch"),
    AudioOneShotBinding("day4.train_latch", "chapters/day4.rpy", 237, "audio.sfx.train_latch"),
    # Medicine-box contact only. Do not reuse this generic draft for bowls,
    # water glasses, metal boxes, paper, or clothing.
    AudioOneShotBinding("day1.object_place", "chapters/day1.rpy", 119, "audio.sfx.object_place"),
)


def validate_production_definition():
    """Ensure the reviewed table has no hidden source, action, or gain path."""
    continuous = {cue.cue_id: cue for cue in CONTINUOUS_CUES}
    oneshots = {cue.cue_id: cue for cue in ONESHOT_CUES}
    assets = {asset.filename for asset in RUNTIME_AUDIO_ASSETS}
    if len(continuous) != len(CONTINUOUS_CUES) or len(oneshots) != len(ONESHOT_CUES):
        raise ValueError("Duplicate cue admission")
    if len(assets) != len(RUNTIME_AUDIO_ASSETS):
        raise ValueError("Duplicate asset admission")
    action_cues = {item.cue_id for item in ACTION_BINDINGS}
    non_action_cues = {"audio.ui.click_soft", "audio.ui.choice_confirm", "audio.notification.neutral_contact"}
    if (
        len(ACTION_BINDINGS) != 15
        or len(oneshots) != 15
        or len(RUNTIME_AUDIO_ASSETS) != 31
        or not non_action_cues.issubset(oneshots)
        or action_cues != set(oneshots) - non_action_cues
    ):
        raise ValueError("Action whitelist changed")
    if any(oneshots[cue_id].priority != "DECORATIVE" for cue_id in action_cues):
        raise ValueError("Narrative actions must remain decorative")
    if any(oneshots[cue_id].priority != "OPTIONAL_UI_NOTIFICATION" for cue_id in non_action_cues):
        raise ValueError("UI and notification priorities changed")
    for music_id, ambience_id in RESTORE_CONTEXTS.values():
        if continuous.get(music_id, None) is None or continuous[music_id].layer != "music":
            raise ValueError("Invalid music context")
        if continuous.get(ambience_id, None) is None or continuous[ambience_id].layer != "ambience":
            raise ValueError("Invalid ambience context")
    referenced = {cue.filename for cue in CONTINUOUS_CUES if cue.filename is not None}
    referenced.update(cue.filename for cue in ONESHOT_CUES)
    if referenced != assets:
        raise ValueError("Runtime asset admission is not exact")
    return True
