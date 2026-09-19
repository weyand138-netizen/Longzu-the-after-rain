# Sprint 013 Content-Lock Semantic Diff

Date: 2026-08-16
Trusted baseline: `HEAD ff00c7aff4c1ff5f5c12c85cab43a0d8c4e1c9aa`
Lock: `content_lock:player_visible:v6`

## Result

PASS — zero player-visible copy delta was introduced by the Sprint 013 worktree changes.

`game/screens.rpy` and `game/11_achievements.rpy` were compared against the trusted HEAD using a focused player-visible text inventory and word-level semantic review. The source identity rows had stale line/hash values; the current rows were refreshed to the current line counts and SHA-256 values. This is a structure/implementation identity refresh, not a rollback and not a content-lock version increment.

| Source | Trusted HEAD semantic copy delta | Current lines | Current SHA-256 | Lock action |
|---|---|---:|---|---|
| `game/screens.rpy` | None | 377 | `72d963e5c0df442dec889d1024f82a8951af573575ad5ebd84a8c0e5a7e5a291` | Refresh v6 identity row |
| `game/11_achievements.rpy` | None | 47 | `18bca7c444314b451f41ab094656f6f8346273ae5a2b22c0fc58dfe8eca5d17c` | Refresh v6 identity row |

No hidden-score, completion-rate, ending-prompt, or accessibility-semantic delta was introduced by this change set. Targeted UX/content/source-manifest checks remain automated; human GUI and semantic review belong to the future asset-merged Production RC closeout.
