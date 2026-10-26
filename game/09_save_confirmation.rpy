# This project defines its screens directly, without gui.init(). Ren'Py's
# save-token verifier still calls layout.yesno_prompt for imported saves.
# Install the standard screen-backed adapter, retaining token verification
# and the existing confirmation screen instead of bypassing either one.
init 10 python:
    if not hasattr(layout, "yesno_prompt"):
        renpy.load_module("_layout/screen_yesno_prompt")
