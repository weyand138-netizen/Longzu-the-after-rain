# Day 1 Asset Admission Consistency Check

**Story**: S1-04 — Day 1 asset admission records  
**Recorded**: 2026-08-10  
**Verdict**: **PASS**

## Scope

Grep-first review of `game/chapters/day1.rpy`, `game/00_resources.rpy`,
`game/screens.rpy`, and the actual `game/assets/` tree, cross-checked against
`design/assets/entity-inventory.md` and `docs/legal/asset-register.md`.

## Results

| Check | Result |
|---|---|
| Actual Day 1 scene reference | `bg warm_room` only; it is registered as the code-defined `Solid("#4a3840")` primitive. |
| Actual file assets | `game/assets/fonts/SourceHanSansLite.ttf` only; its SHA-256 is `b2aaf73b7acc23d746b110f1caeaecc93d4292824979af44e96000200591b2a7`. |
| Code-defined hashes | `game/00_resources.rpy`: `4333d936fbe481f61c4cb828e43e17057133ae5af99b79cdf76e76545ee49801`; `game/screens.rpy`: `094cdd02273dd8c88f6a0f1eb6feebde3cf44ef56d2a0347ebc951406fab8e9d`. Both match both registers. |
| Legal/admission join | The inventory and legal register contain the same three admitted IDs: `FONT-SOURCEHAN-LITE-P0`, `RUNTIME-SOLID-DAY1-WARM-ROOM`, and `RUNTIME-UI-DAY1-CHOICE-SURFACE`. Each has provenance/licence, SHA-256, runtime path, and `a11y.day1.*` semantic binding. |
| Nonexistent planned files | Station-platform, ticket-gate, train-window, wish-paper, receipt, and focus-frame files are all marked not present and not admitted. No document claims that they exist. |

## Accessibility conclusion

The room `Solid()` is decorative. Day 1 causality and choice meaning remain in
visible/localizable dialogue and keyboard-operable choice captions; the choice
surface records stable focus IDs and a non-colour-only high-contrast focus
treatment. The existing Day 1 evidence bundle covers silent, reduced-motion,
1280x720, and 1.5x/high-contrast baselines.

## Separate test-gate note

The static Day 1 test suite passed 30/30 and the content constraint scan
passed. A current Ren'Py global re-run passed 12/13 testcases and 62/62
assertions, but its visual baseline case stopped on an expected-screenshot size
mismatch (`1738x977` actual, `1280x720` expected). This is not an asset
admission discrepancy; the Sprint-wide test gate remains open until that
fixture/environment mismatch is resolved.
