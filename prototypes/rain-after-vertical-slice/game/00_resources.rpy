# VERTICAL SLICE - NOT FOR PRODUCTION
# Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality?
# Date: 2026-07-23

define narrator = Character(None)
define lm = Character("路明非", color="#f5dfbc")
define erii = Character("绘梨衣", color="#f3aabe")
define journal = Character("愿望手册", color="#91d4dd")

define fade_rain = Dissolve(0.7)
define fade_warm = Dissolve(1.1)

image bg slice_platform = Transform(
    "images/bg_rain_platform.png",
    size=(1920, 1080),
)
image bg slice_gate = Transform(
    "images/bg_ticket_gate.png",
    size=(1920, 1080),
)
image bg slice_train = Transform(
    "images/bg_train_window.png",
    size=(1920, 1080),
)
image bg slice_black = Solid("#070b12")

