default main_menu_weather = "heavy_rain"

# Temporary title-page switch. The reusable story weather system remains
# available; keep the menu itself as static artwork until this is re-enabled.
define MAIN_MENU_ENVIRONMENT_EFFECTS_ENABLED = False

init python:
    MAIN_MENU_WEATHER_STATES = ("heavy_rain", "overcast", "dusk")
    # These choose realtime overlay behaviour only. The three menu artworks
    # below remain independent, fixed background images.
    MAIN_MENU_WEATHER_PRESETS = {
        "heavy_rain": "storm",
        "overcast": "overcast",
        "dusk": "sunset",
    }

    def select_main_menu_weather():
        """Pick ambience only when the title route is entered, never on screen swaps."""
        if renpy.is_in_test():
            return "heavy_rain"
        return renpy.random.choice(MAIN_MENU_WEATHER_STATES)

    def apply_main_menu_weather_preview(weather_state):
        """Synchronize the selected static menu art with its live overlay."""
        preset = MAIN_MENU_WEATHER_PRESETS.get(weather_state, "storm")
        set_weather_preview(preset)

    def prepare_main_menu_weather(weather_state):
        """Keep title weather isolated from reusable narrative weather."""
        if MAIN_MENU_ENVIRONMENT_EFFECTS_ENABLED:
            apply_main_menu_weather_preview(weather_state)
        else:
            disable_weather()

label splashscreen:
    scene bg black
    with dissolve
    centered "{size=38}非官方 · 免费 · 非商业同人作品{/size}\n\n本作不代表原作者、出版社或任何官方授权方。\n请勿将本作内容视为原作正典。"
    pause 1.5
    return

# Let Ren'Py own the ordinary title-page context. The native main-menu
# controller creates a child context for this label, so Start("begin_game")
# can safely leave it before a playable run begins. In particular, a save
# restored later will no longer inherit the title screen's return stack.
label main_menu:
    if renpy.is_in_test():
        return
    call launch_title_page
    return

label start:
    if renpy.is_in_test():
        $ reset_run_state()
        call prologue_start
        return

    call launch_title_page
    return


label launch_title_page:
    # Title entry is a high-level lifecycle boundary: it stops every prior
    # narrative layer before the separately admitted title context begins.
    $ audio_scene_enter_title()
    $ main_menu_weather = select_main_menu_weather()
    $ prepare_main_menu_weather(main_menu_weather)
    call screen main_menu
    return


label begin_game:
    # `begin_game` is the sole playable entry point. Normalise the menu flags
    # here as a defensive boundary as well as using Start() from the native
    # menu: FileSave refuses every write while either menu flag is retained.
    $ main_menu = False
    $ renpy.context()._main_menu = False
    $ reset_run_state()
    call production_end_to_end_orchestrator
    return

label accessibility_settings_test:
    $ apply_accessibility_settings(1.0, False, False, False, False)
    return
