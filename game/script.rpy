label splashscreen:
    scene bg black
    with dissolve
    centered "{size=38}非官方 · 免费 · 非商业同人作品{/size}\n\n本作不代表原作者、出版社或任何官方授权方。\n请勿将本作内容视为原作正典。"
    pause 1.5
    return

label start:
    $ reset_run_state()
    if renpy.is_in_test():
        call prologue_start
        return
    call production_end_to_end_orchestrator
    return

label accessibility_settings_test:
    $ apply_accessibility_settings(1.0, False, False, False, False)
    return
