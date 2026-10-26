# After the Rain

[简体中文](README.md) · [Game Releases](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases) · [All versions](docs/versions.md) · [Contact](SUPPORT.md)

*After the Rain* is a free, non-commercial, unofficial *Dragon Raja* fan visual novel.

From Lu Mingfei's limited point of view, accompany Erii through seven days. Observe, ask, prepare, and accept responsibility: choices leave later consequences and lead to six different endings.

Created by **Andwey** · Game language: **Simplified Chinese** · Target platform: **Windows 10 / 11 x86-64**

## Download and Versions

**[Download the Windows RC.1 build](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases/tag/v1-rc.1-local-20261024)** · [Game Releases](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases) · [All versions and downloads](docs/versions.md)

The current public build is `1-rc.1-local-20261024`, an RC prerelease candidate. The final release is not yet public. See the relevant Release for its content, known issues, and file checksums.

Download the **Windows game ZIP** attached to the desired Release, extract the complete archive, and launch the game. No separate Python or Ren'Py installation is required. The current RC.1 package uses `雨停之后.exe`; earlier public test builds use `After rain.exe`. Follow the instructions for the version downloaded. GitHub's `Source code` archives are not standalone game builds.

Keep the old installation and saves before updating. See the [FAQ](docs/faq.md) for installation, compatibility, and update information.

## Game Overview

The story begins on a rain-soaked station platform. Accompany Erii through seven days of brief everyday moments and gradually unfolding truths, paying attention to what she writes, the objects she hands over, and her reactions in moments of silence.

Decide when to explain, when to wait, and how to prepare for the road ahead. Earlier responses echo through later scenes and lead to different outcomes.

- A prologue and seven days of story.
- Six deterministic endings with their own epilogues.
- 18 ending event CGs, chapter backgrounds, and character actions.
- Background music, ambience, and story sound effects.
- Save/load, rollback, skip, and automatic reading.
- Font scaling, high contrast, reduced motion, and self-voicing settings.

There is currently no recorded character voice acting. This English README does not indicate an English translation of the game. Some endings contain separation and emotionally heavy scenes; please mark ending discussions and screenshots as spoilers.

[Current release notes](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases/tag/v1-rc.1-local-20261024) · [Proposed final-release introduction](docs/releases/v1.0.0_EN.md) · [中文正式版介绍草案](docs/releases/v1.0.0.md)

The game can be played offline; feedback is submitted manually by email or GitHub. See the relevant Release for its supported-device scope.

<details>
<summary>Build from source (developers)</summary>

Build a Windows ZIP with the [official Ren’Py 8.5.3 SDK](https://www.renpy.org/release/8.5.3), then run:

```console
python scripts/package-player-windows.py --input After-Rain-v1-rc.1-local-20261024-win.zip --sdk-zip renpy-8.5.3-sdk.zip --output 雨停之后-Windows.zip
```

The script checks the official SDK ZIP SHA-256, uses stock official launchers, renames the entry point to `雨停之后.exe`, and excludes root readmes/review materials. Game code and assets are preserved; required runtime and font licenses remain included.

</details>

## Feedback

**Email: [weyand138@gmail.com](mailto:weyand138@gmail.com)**

You may also report problems through [GitHub Issues](https://github.com/weyand138-netizen/Longzu-the-after-rain/issues). Include the version, chapter, reproduction steps, and relevant screenshots. See [SUPPORT.md](SUPPORT.md) for the reporting format.

[Known issues](docs/known-issues.md) · [Changelog](CHANGELOG.md)

## Support the Project

Star the repository, share its repository or Release link, or send useful playtest feedback. Please identify the version and mark spoilers when sharing.

The project remains free and non-commercial. It does not accept sponsorships or tips and has no paid unlocks or paid content.

## Rights

This is an unofficial fan work, unaffiliated with and not endorsed by the original author, publisher, or official rights holders. Rights relating to the original characters and setting belong to their respective owners.

The repository's [LICENSE](LICENSE) and individual notices govern use of its contents. Public access does not grant commercial reuse or unrestricted redistribution rights. Third-party content retains its own terms.

For credits, provenance, or rights-related questions, contact [weyand138@gmail.com](mailto:weyand138@gmail.com).

**AI-assisted production disclosure:** Generative AI and AI-assisted tools were used during development, including writing ideation and editing support, programming and testing assistance, and the generation or processing of some visual assets. Audio production also used procedural synthesis tools. The project is not entirely handmade. The creator is responsible for content selection, editing, integration, and the final publication decision. Notices concerning the original work and third-party materials continue to apply.

