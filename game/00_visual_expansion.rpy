# First candidate batch, 2026-09-18. Native show/hide participates in rollback/save.
# Separate aliases avoid replacing the existing character and prop tags.
image char lu mingfei clear_empty_bowl = Transform("assets/characters/lu_mingfei/char_lu_mingfei_clear_empty_bowl.png", xpos=410, xanchor=0.5, ypos=365, yanchor=0.0, ysize=1100, fit="contain")
image npc clothing_clerk_back = Transform("assets/characters/npc/npc_clothing_clerk_back.png", xpos=385, xanchor=0.5, ypos=235, yanchor=0.0, ysize=790, fit="contain", matrixcolor=BrightnessMatrix(-0.08))
image prop clothing_pair_table = Transform(Transform("assets/props/prop_clothing_pair_table.png", xysize=(396, 225)), xpos=1140, xanchor=0.5, ypos=615, yanchor=0.5, rotate=-10)
image prop hot_porridge = Transform("assets/props/prop_hot_porridge.png", xpos=1080, xanchor=0.5, ypos=550, yanchor=0.0, ysize=180, fit="contain")
image prop medicine_box_blister = Transform("assets/props/prop_medicine_box_blister.png", xpos=1240, xanchor=0.5, ypos=550, yanchor=0.0, ysize=125, fit="contain")
image prop medicine_box_far = Transform("assets/props/prop_medicine_box_blister.png", xpos=1390, xanchor=0.5, ypos=530, yanchor=0.0, ysize=105, fit="contain")
image char erii open_palm_arcade = Transform("assets/characters/erii/char_erii_open_palm_arcade.png", xpos=960, xanchor=0.5, ypos=35, yanchor=0.0, ysize=1220, fit="contain")
image char lu mingfei look_at_palm = Transform("assets/characters/lu_mingfei/char_lu_mingfei_look_at_palm.png", xpos=960, xanchor=0.5, ypos=35, yanchor=0.0, ysize=1220, fit="contain")
image prop clothing_cuff_pair = Transform("assets/props/prop_clothing_cuff_pair.png", xpos=960, xanchor=0.5, ypos=110, yanchor=0.0, ysize=590, fit="contain")
image prop arcade_control_panel = Transform("assets/props/prop_arcade_control_panel_v02.png", xpos=960, xanchor=0.5, ypos=60, yanchor=0.0, ysize=690, fit="contain")

# Day 3-6 admitted story poses. A shared tag guarantees that every pose
# replaces the previous one and that authored hide points clear the layer.
image story erii_read_archive = Transform("assets/characters/erii/char_erii_read_archive_pages.png", xpos=960, xanchor=0.5, ypos=35, yanchor=0.0, ysize=1220, fit="contain")
image story erii_arrange_route = Fixed(
    "bg station_ticket_window_action",
    Transform("assets/characters/erii/char_erii_arrange_route_papers.png", xpos=960, xanchor=0.5, ypos=35, yanchor=0.0, ysize=1220, fit="contain"),
    xysize=(1920, 1080),
)
image story erii_turn_exit = Transform("assets/characters/erii/char_erii_turn_toward_exit.png", xpos=675, xanchor=0.5, ypos=35, yanchor=0.0, ysize=1220, fit="contain")
image story lu_present_identity = Fixed(
    "bg station_ticket_window_action",
    Transform("assets/characters/lu_mingfei/char_lu_mingfei_present_identity_card.png", xpos=960, xanchor=0.5, ypos=35, yanchor=0.0, ysize=1220, fit="contain"),
    xysize=(1920, 1080),
)
image story lu_hold_classroom_door = Transform("assets/characters/lu_mingfei/char_lu_mingfei_hold_door_aside.png", xpos=1470, xanchor=0.5, ypos=70, yanchor=0.0, ysize=1190, fit="contain")
image story lu_hold_safehouse_door = Transform("assets/characters/lu_mingfei/char_lu_mingfei_hold_door_aside.png", xpos=875, xanchor=0.5, ypos=70, yanchor=0.0, ysize=1190, fit="contain")
