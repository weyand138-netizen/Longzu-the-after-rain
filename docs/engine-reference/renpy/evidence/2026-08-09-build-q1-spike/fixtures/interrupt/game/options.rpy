define config.name = "RenPy Build Spike"
define config.version = "0.0.1"
define config.window_title = "RenPy Build Spike"

init python:
    build.name = "renpy-build-spike"
    build.directory_name = "renpy-build-spike-0.0.1"
    build.executable_name = "renpy-build-spike"
    build.package("win", "zip", "windows renpy all")
init python:
    import time
    time.sleep(30)