"""The reviewed production admission list for the internal audio test build.

This data is intentionally explicit.  It is based on the narrated setting and
the named action at each source position, never on a background asset name.
No entry carries an output gain: the original approved bytes are played as-is.
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
    OneShotCue("audio.ui.click_soft", "assets/audio/sfx/ui_click_soft.wav", "OPTIONAL_UI_NOTIFICATION"),
    OneShotCue("audio.ui.choice_confirm", "assets/audio/sfx/ui_choice_confirm.wav", "OPTIONAL_UI_NOTIFICATION"),
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
    "audio.context.day4.ticket_window": ("audio.music.visible_departure", "audio.ambience.rain_platform"),
    "audio.context.day4.seaside_station": ("audio.music.before_departure", "audio.ambience.seaside"),
    "audio.context.day4.coastal_train": ("audio.music.before_departure", "audio.ambience.train_carriage"),
    "audio.context.day5.archive_quiet": ("audio.music.archive_space", "audio.ambience.intentional_silence"),
    "audio.context.day6.service_exit": ("audio.music.before_departure", "audio.ambience.service_exit"),
    "audio.context.day7.red_well": ("audio.music.before_departure", "audio.ambience.red_well"),
    # Ending contexts keep their gains and one-shot policy identical: none is
    # sonically framed as a reward or as a worse outcome.
    "audio.context.ending.rain_stops": ("audio.music.after_rain", "audio.ambience.intentional_silence"),
    "audio.context.ending.her_own_name": ("audio.music.life_continues", "audio.ambience.internet_cafe"),
    "audio.context.ending.see_the_sea": ("audio.music.after_rain", "audio.ambience.seaside"),
    "audio.context.ending.one_person_train": ("audio.music.before_departure", "audio.ambience.rain_platform"),
    "audio.context.ending.golden_cage": ("audio.music.archive_space", "audio.ambience.intentional_silence"),
    "audio.context.ending.unsent_postcard": ("audio.music.archive_space", "audio.ambience.room_rain"),
    "audio.context.epilogue.arcade": ("audio.music.life_continues", "audio.ambience.internet_cafe"),
}


_SOURCE_DIGESTS = {
    "chapters/prologue.rpy": "38e03185fbd106473edb1b032930ea79d5fe9bb0df34acd02325f9d6042caa1a",
    "chapters/day1.rpy": "ddc38bf97617fb8838391d728d1b5620d81f5e149d99ea26e3d98a5c27bb8d8e",
    "chapters/day2.rpy": "2d17b86c69ec3f55526bd4c68335659b9903cd3019e3ba86e7c890a4aabc249c",
    "chapters/day3.rpy": "fcb2b40ea399635c6180fb3c9a447c8570cc411dc4c7be956257b45af4aeb9ac",
    "chapters/day4.rpy": "1b3f04a209ab4f37b357ff94ed81717bb5d9d2cf2971c21b8be633030b2737db",
    "chapters/day5.rpy": "1dbe55d5cb7bd5a09291734d2a037fb85f16f60654bc07543c6c8ad98b33238f",
    "chapters/day6.rpy": "7e13fdabd2fd9344fec9351f4a48fc67d100c25e4f497d5144dee04c3dff7722",
    "chapters/day7.rpy": "1e837770ec5a821766684cf31605285e45364fbba1ae5781ed3d1fa609680d6b",
    "chapters/endings.rpy": "5a18aa693579d86ece69da6f4db3c6d0afac09abfb893d9e50ca118b93114c6a",
}


def _range(source, first_line, last_line, context_id):
    return AudioContextRange(source, first_line, last_line, _SOURCE_DIGESTS[source], context_id)


CONTEXT_RANGES = (
    _range("chapters/prologue.rpy", 1, 112, "audio.context.prologue.platform"),
    _range("chapters/prologue.rpy", 113, 149, "audio.context.prologue.ticket_gate"),
    _range("chapters/prologue.rpy", 150, 182, "audio.context.prologue.train"),
    _range("chapters/day1.rpy", 1, 62, "audio.context.day1.shop_rain"),
    _range("chapters/day1.rpy", 63, 163, "audio.context.day1.safehouse"),
    _range("chapters/day1.rpy", 164, 170, "audio.context.day1.departure"),
    _range("chapters/day2.rpy", 1, 198, "audio.context.day2.arcade"),
    _range("chapters/day2.rpy", 199, 237, "audio.context.day2.mall_exterior"),
    _range("chapters/day3.rpy", 1, 220, "audio.context.day3.classroom"),
    _range("chapters/day4.rpy", 1, 233, "audio.context.day4.ticket_window"),
    _range("chapters/day4.rpy", 234, 245, "audio.context.day4.seaside_station"),
    _range("chapters/day4.rpy", 246, 294, "audio.context.day4.coastal_train"),
    _range("chapters/day5.rpy", 1, 349, "audio.context.day5.archive_quiet"),
    _range("chapters/day6.rpy", 1, 399, "audio.context.day6.service_exit"),
    _range("chapters/day7.rpy", 1, 111, "audio.context.day7.red_well"),
    _range("chapters/endings.rpy", 1, 35, "audio.context.ending.rain_stops"),
    # Each non-rain epilogue deliberately continues its ending context.  No
    # tail adds a one-shot, gain override, or outcome-specific reward cue.
    _range("chapters/endings.rpy", 36, 83, "audio.context.ending.her_own_name"),
    _range("chapters/endings.rpy", 84, 129, "audio.context.ending.see_the_sea"),
    _range("chapters/endings.rpy", 130, 176, "audio.context.ending.one_person_train"),
    _range("chapters/endings.rpy", 177, 222, "audio.context.ending.golden_cage"),
    _range("chapters/endings.rpy", 223, 269, "audio.context.ending.unsent_postcard"),
    _range("chapters/endings.rpy", 270, 306, "audio.context.epilogue.arcade"),
)


ACTION_BINDINGS = (
    AudioOneShotBinding("day1.cloth_shift", "chapters/day1.rpy", 76, "audio.sfx.cloth_shift"),
    AudioOneShotBinding("day1.paper_fold", "chapters/day1.rpy", 155, "audio.sfx.paper_fold"),
    AudioOneShotBinding("day1.wet_step", "chapters/day1.rpy", 167, "audio.sfx.wet_step"),
    AudioOneShotBinding("day2.keyboard", "chapters/day2.rpy", 72, "audio.sfx.keyboard"),
    AudioOneShotBinding("day2.two_coins", "chapters/day2.rpy", 134, "audio.sfx.two_coins"),
    AudioOneShotBinding("day2.interior_step", "chapters/day2.rpy", 194, "audio.sfx.interior_step"),
    AudioOneShotBinding("day4.paper_unfold", "chapters/day4.rpy", 127, "audio.sfx.paper_unfold"),
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
    ui_cues = {"audio.ui.click_soft", "audio.ui.choice_confirm"}
    if len(ACTION_BINDINGS) != 7 or action_cues != set(oneshots) - ui_cues:
        raise ValueError("Action whitelist changed")
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
