# Findings intake from ic2-conquest

The bot repository [`diegoami/ic2-conquest`](https://github.com/diegoami/ic2-conquest) explores the game by playing it headless and drafts rule discoveries in its `findings/` folder, in this repository's report format. It never writes here (its hard rule 2); this repository pulls. The procedure is the project skill `retrieve-findings` (`.claude/skills/retrieve-findings/SKILL.md`). A daily GitHub Action (`.github/workflows/pending-drafts.yml`, script `scripts/pending-drafts.sh`) lists the drafts this ledger has not reviewed and keeps one open issue while any exist. This ledger is what makes the pull incremental: a draft is **new** until it has a row here.

Rows are keyed by the draft's path and the blob it had when reviewed, so a draft that changes later shows up again.

| Draft (in ic2-conquest `findings/`) | Reviewed at (commit) | Outcome | Promoted as | Date |
|---|---|---|---|---|
| `2026-09-29-recruiting-cities-need-fortification-75.md` | `a1df3b4` | promoted | `2026-09-29-which-cities-may-recruit-and-troop-amounts.md` (independent confirmation noted) | 2026-09-29 |
| `2026-09-29-loading-a-save-does-not-reseed.md` | `a1df3b4` | promoted, corrected (the two other `RandSeed` writers are the treaty and `TBattlePols`, not paint routines) | `2026-09-29-loading-a-save-does-not-reseed.md` | 2026-09-29 |
| `2026-09-29-nation-view-origin-and-unit-map-clicks.md` | `a1df3b4` | promoted | `2026-09-29-nation-view-origin-and-unit-map-clicks.md` | 2026-09-29 |

Outcomes: `promoted`, `promoted, corrected`, `merged into <report>`, `rejected: <why>`, `deferred: <what evidence is missing>`.
