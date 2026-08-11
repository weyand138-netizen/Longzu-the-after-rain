# Technical Preferences

## Engine & Language

- Engine: Ren'Py 8.5.3
- Script: Ren'Py Script
- Logic modules: Python compatible with 3.12 and later
- Encoding: UTF-8

## Naming Conventions

- Ren'Py labels: `snake_case`, prefixed by chapter where useful (`prologue_station`)
- Store variables: `snake_case`
- Pure Python functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Screens: `snake_case`
- Asset files: lowercase `snake_case`
- Achievement IDs: uppercase namespaced strings (`ENDING_RAIN_STOPS`)

## Input & Platform

- Target platforms: Windows 10/11 x86-64
- Input methods: keyboard and mouse
- Primary input: mouse
- Keyboard support: full navigation for every interactive screen
- Gamepad support: partial, using Ren'Py defaults
- Touch support: none
- No interaction may require hover.

## Performance Budgets

- Target framerate: 60 fps
- Frame budget: 16.6 ms during interactive screens
- Startup target: main menu visible within 5 seconds on minimum target hardware
- Save target: complete within 500 ms for normal saves
- Base memory target: below 1 GB excluding platform overhead
- Image policy: avoid loading full-resolution CGs before their scene

## Testing

- Ren'Py 8.5 testcase framework for end-to-end choice flows.
- Python `unittest` for pure ending and catalog logic.
- Ren'Py lint must report no errors before any hand-off build.
- Six canonical ending vectors plus exclusivity checks are mandatory.

## Allowed Libraries

- Ren'Py standard runtime only.
- Python standard library only in pure logic tests.

## Forbidden Patterns

- Network clients, telemetry SDKs, ad SDKs, analytics, or crash uploaders.
- Randomness in ending resolution.
- Mutating imported Python objects as live rollback state.
- Direct ending-condition copies in chapter scripts.
- Hard-coded official/source-unknown assets.

## Review Mode

- Solo/lean workflow. External director gates are deferred until a closed playtest build exists.

