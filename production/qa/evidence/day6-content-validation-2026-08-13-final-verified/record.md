# Day 6 Route and Accessibility Evidence

**Date**: 2026-08-13
**Scope**: Sprint 5 / Story 018 deterministic Day 6 routes and approved
accessibility baselines after source-order review.

## Generation Binding

- **Day 6 source SHA-256**:
  `4571b38e0ad718d7ee0b2c581f4257c98e3f31fc948004408b204c6d3915f99e`
- **Testcases SHA-256**:
  `fb519258adcb0175589cf54c6cdb34cbbdc5a838eeb4a768ead95f88802c6b4a`
- **Runner stdout SHA-256**:
  `1985670b9f4353886286aa2a9d316cf95b544bc98a8d343aee068f5b255d6616`
- **Runner stderr SHA-256**:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Automated Result

`tools/run-renpy-day6-evidence.ps1` launched the pinned Ren'Py
8.5.3.26051504 global suite in a fresh evidence-local save directory. The
machine-readable result is `run-passed/result.json`: status
`[rpytest] Status: PASSED`, process exit `-1` after the runner's terminal
report, 45/45 testcases, and 386/386 assertions.

The Day 6 contracts exercise prepared/abandoned backup repair, late-truth
repair, direct cost, shifted cost plus second refusal/take-back, all five
guarded commitment/fallback states, and contradictory Day 5 facts that expose
no commitment choice. They additionally prove each commitment event follows
its immediate player-visible reaction, as ADR-0008 requires.

## Accessibility Captures

| Capture | SHA-256 | Baseline |
|---|---|---|
| `day6_cost_1280x720_keyboard_silent_reduced_motion.png` | `926fe9bf63e7ce935d70cf1537b6a34c0f10d38ad0584857d9971f5c02322bb0` | keyboard, silent, reduced motion |
| `day6_commitment_1280x720_keyboard_silent_reduced_motion.png` | `85a5bf2a276783db07ff739c454423f062c2fe209a39f4fd6d6b64fadf31a645` | keyboard, silent, reduced motion |
| `day6_cost_1280x720_font_1_5_high_contrast.png` | `426b749e4d7e3ec8fce15577cc8a09002faff2711e93c0a71f9248b5fe940844` | 1.5x font, high contrast, reduced motion |
| `day6_commitment_1280x720_font_1_5_high_contrast.png` | `739b2aab55494e87993db3b7e8b3ac5f7e905d85ab26185d742e0ed054fee5cd` | 1.5x font, high contrast, reduced motion |

Each capture is 1280x720. Engine assertions confirm native initial keyboard
focus, visible traversal, silent self-voicing setting, semantic text choices,
and no quick-menu focus target during critical interaction.

## Scope Boundary

This bundle verifies Day 6 only. It does not claim Day 7, a terminal witness,
route qualification, ending, epilogue, partial-manifest expansion, release, or
human narrative/readability approval.
