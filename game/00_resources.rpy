define narrator = Character(None)
define lm = Character("路明非", color="#f5e5b8")
define erii = Character("绘梨衣", color="#f3a7bd")
define system = Character("愿望手册", color="#8cc8d8")

define dissolve_slow = Dissolve(0.8)

image bg rain_platform = "assets/backgrounds/bg_station_platform_rain.png"
image bg ticket_gate = "assets/backgrounds/bg_ticket_gate.png"
image bg train_window = "assets/backgrounds/bg_train_window.png"
image bg main_menu_rainy = "assets/backgrounds/bg_main_menu_rainy.png"
image bg main_menu_dusk = "assets/backgrounds/bg_main_menu_dusk.png"
image bg main_menu_overcast = "assets/backgrounds/bg_main_menu_overcast.png"
image bg ordinary_rental_room_rain_night = "assets/backgrounds/bg_ordinary_rental_room_rain_night.png"
image bg clothing_shop_rain_morning = Transform("assets/backgrounds/bg_clothing_shop_rain_morning.png", xysize=(1920, 1080), fit="cover")
image bg mall_entrance_rain_night = Transform("assets/backgrounds/bg_mall_entrance_rain_night.png", xysize=(1920, 1080), fit="cover")
image bg quiet_arcade_corner = "assets/backgrounds/bg_quiet_arcade_corner.png"
image bg station_ticket_window_interior = "assets/backgrounds/bg_station_ticket_window_interior.png"
image bg rain_stopped_morning_window = "assets/backgrounds/bg_rain_stopped_morning_window.png"
image bg empty_school_classroom_rain = "assets/backgrounds/bg_empty_school_classroom_rain.png"
image bg seaside_station_window = "assets/backgrounds/bg_seaside_station_window.png"
image bg family_archive_table = "assets/backgrounds/bg_family_archive_table.png"
image bg safehouse_service_exit = "assets/backgrounds/bg_safehouse_service_exit.png"
image bg red_well_steps = "assets/backgrounds/bg_red_well_steps.png"
image bg neighborhood_internet_cafe_rain = "assets/backgrounds/bg_neighborhood_internet_cafe_rain.png"
image bg coastal_train_dawn = "assets/backgrounds/bg_coastal_train_dawn.png"
image bg empty_platform_departure = "assets/backgrounds/bg_empty_platform_departure.png"
image bg old_order_waiting_room = "assets/backgrounds/bg_old_order_waiting_room.png"
image bg unsent_postcard_table = "assets/backgrounds/bg_unsent_postcard_table.png"
image crowd rain_platform left_near = Transform("assets/overlays/passersby/passerby_rain_left_near.png", xalign=0.10, yanchor=1.0, ypos=850, zoom=0.60)
image crowd rain_platform left_far = Transform("assets/overlays/passersby/passerby_rain_left_far.png", xalign=0.25, yanchor=1.0, ypos=690, zoom=0.375)
image crowd rain_platform right_far = Transform("assets/overlays/passersby/passerby_rain_right_far.png", xalign=0.43, yanchor=1.0, ypos=650, zoom=0.33)
image crowd rain_platform right_near = Transform("assets/overlays/passersby/passerby_rain_right_near.png", xalign=0.43, yanchor=1.0, ypos=840, zoom=0.525)
image char erii neutral = Transform("assets/characters/erii/char_erii_stand_neutral.png", xalign=0.18, yalign=1.0, xzoom=-0.32, yzoom=0.32)
image char erii day1_corner = Transform("assets/characters/erii/char_erii_stand_neutral.png", xalign=0.74, yalign=1.0, zoom=0.36, xoffset=225, yoffset=360)
image char erii paper_observation = Transform("assets/characters/erii/char_erii_look_down_wish_paper.png", xalign=0.18, yalign=1.0, xzoom=-0.54, yzoom=0.54)
image char lu mingfei neutral = Transform("assets/characters/lu_mingfei/char_lu_mingfei_stand_neutral.png", xalign=0.18, yalign=1.0, zoom=0.36)
image char lu mingfei day1_corner = Transform("assets/characters/lu_mingfei/char_lu_mingfei_stand_neutral.png", xalign=0.18, yalign=1.0, zoom=0.36, xoffset=-225, yoffset=360)
image char lu mingfei look_erii = Transform("assets/characters/lu_mingfei/char_lu_mingfei_look_erii.png", xalign=0.18, yalign=1.0, zoom=0.58)
image char lu mingfei paper_observation = Transform("assets/characters/lu_mingfei/char_lu_mingfei_look_down_wish_paper.png", xalign=0.18, yalign=1.0, zoom=0.56)
image char lu mingfei paper_side = Transform("assets/characters/lu_mingfei/char_lu_mingfei_stand_neutral.png", xalign=0.70, yalign=1.0, zoom=0.34)
image char lu mingfei pick_up_wish_paper = Transform("assets/characters/lu_mingfei/char_lu_mingfei_pick_up_wish_paper.png", xalign=0.68, yalign=1.0, zoom=0.38)
image char lu mingfei inspect_wish_paper = Transform("assets/characters/lu_mingfei/char_lu_mingfei_inspect_wish_paper.png", xalign=0.65, yalign=1.0, zoom=0.55)
image char lu mingfei offer_wish_paper = Transform("assets/characters/lu_mingfei/char_lu_mingfei_offer_wish_paper.png", xalign=0.68, yalign=1.0, xzoom=-0.60, yzoom=0.60)
image prop wish_paper = Transform("assets/props/prop_wish_paper.png", xalign=0.53, yalign=0.39, zoom=0.20)
image prop game_coin_pair = Transform("assets/props/prop_game_coin_pair.png", xalign=0.50, yalign=0.43, zoom=0.34)
image prop receipt_name = Transform("assets/props/prop_receipt_name.png", xalign=0.78, yalign=0.06, zoom=0.55)
image ui life_tree = "assets/ui/life_tree.png"
image bg warm_room = Solid("#4a3840")
image bg black = Solid("#08090c")
