# After the Rain

A free, non-commercial, unofficial Dragon Raja fan visual novel by Andwey.

## Download and play

[Download the Windows RC.1 build](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases/tag/v1-rc.1-local-20261024) · [All releases](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases)

Fully extract the Windows ZIP from the Release, then run `雨停之后.exe`. No separate Python or Ren’Py installation is needed. Keep the remaining runtime files alongside it. Windows 10/11 x86-64 is the target; this build's startup was verified on Windows 11.

The game contains the prologue, Days 1–7, six endings and 18 ending CGs. Build: `1-rc.1-local-20261024`. See the Release for changes, known issues and checksums. The existing save format and save-directory identifier are retained.

## Build from source

Build a Windows ZIP with the [official Ren’Py 8.5.3 SDK](https://www.renpy.org/release/8.5.3), then run:

```console
python scripts/package-player-windows.py --input After-Rain-v1-rc.1-local-20261024-win.zip --sdk-zip renpy-8.5.3-sdk.zip --output 雨停之后-Windows.zip
```

The script checks the official SDK ZIP SHA-256, uses stock official launchers, renames the entry point to `雨停之后.exe`, and excludes root readmes/review materials. Game code and assets are preserved; required runtime and font licenses remain included.

## Feedback and license

Report issues through [Issues](https://github.com/weyand138-netizen/Longzu-the-after-rain/issues) with the version, chapter or route, reproduction steps, device details and screenshots or errors.

This is an RC candidate. Complete human playthroughs, audible Chinese self-voicing and target-hardware verification remain pending. Extended soak testing was skipped. Automated results do not imply human acceptance of those items.

This project is not endorsed by any official rights holder. Original project content is governed by `LICENSE`; third-party components retain their respective licenses.
