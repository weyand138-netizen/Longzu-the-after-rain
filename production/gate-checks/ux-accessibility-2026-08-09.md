# UX / Accessibility Gate — 2026-08-09

**Scope:** seven P0 key screens plus shared interaction patterns  
**Tier:** `P0-ACCESS-KEYBOARD-MOUSE-SAPI-EQUIVALENCE`  
**Reviewer:** UX review + targeted implementation verification  
**Verdict:** **PASS — UX gate**

## Blocking findings

None. The prior P0 blockers are closed for this UX gate:

| Finding | Closure evidence |
|---|---|
| Offscreen focus could not auto-scroll before activation | Ren'Py 8.5.3 rerun-27: 4/4 testcases, 18/18 assertions; `viewport_y` 0 → 221 and `deep_action_count = 0` |
| Player arrival context was not represented by a journey artifact | `design/player-journey.md` added and referenced by the cross-reference |
| Runtime menu entry diverged from the UX contract | Production main menu now exposes `愿望手册` with stable semantic ID and focus-graph ordering |
| High-contrast control was marked as reserved | Settings now exposes the five project accessibility settings and one batch apply action backed by the canonical `persistent.settings` root; copy lock updated |
| UX specs still referenced an unfrozen/provisional tier | All seven specs and the interaction library reference the single frozen P0 tier |
| UX review status remained stale | Seven screen specs, shared patterns, and cross-reference are marked `Approved` |

## Review coverage

| Artifact | Result |
|---|---|
| `main-menu.md` | APPROVED |
| `game-menu.md` | APPROVED |
| `narrative-choice.md` | APPROVED |
| `journal.md` | APPROVED |
| `save-load.md` | APPROVED |
| `settings.md` | APPROVED |
| `ending.md` | APPROVED |
| `interaction-patterns.md` | APPROVED |
| `cross-reference.md` | APPROVED |

Each screen has player need/context, navigation and entry/exit points, layout
and component inventory, loading/empty/error or recovery states, keyboard and
mouse interaction mapping, data/event ownership, transitions, performance,
accessibility, localization, and testable acceptance criteria. The shared
pattern library covers semantic buttons, choice surfaces, fixed rails,
keyboard viewports, modals, blocking recovery, announcements, causal cards,
standard controls, animation, and sound rules.

## Verification

- Production Ren'Py tests: **3/3 testcases, 13/13 assertions passed**.
- Ren'Py lint: **clean** under Ren'Py 8.5.3.26051504.
- Accessibility spike rerun-27: **4/4 testcases, 18/18 assertions passed**.
- SAPI preflight: **3 voices enumerated**, including Simplified Chinese. This is capability evidence only; no human listening PASS is claimed.
- Runtime font source, SHA-256, and bundled OFL 1.1 text are recorded in `docs/legal/asset-register.md`.

## Downstream advisories

This PASS is limited to the UX gate. Production/Release still require the
evidence matrix items explicitly marked downstream: per-screen screenshot and
transcript matrix, SAPI human listening adjudication, semantic-equivalence
review, and final archive hash verification. These are not unresolved UX
blockers and must not be represented as completed by this report.
