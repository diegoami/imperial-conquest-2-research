# Findings intake from ic2-conquest

The bot repository [`diegoami/ic2-conquest`](https://github.com/diegoami/ic2-conquest) explores the game by playing it headless and drafts rule discoveries in its `findings/` folder, in this repository's report format. It never writes here (its hard rule 2); this repository pulls. The procedure is the project skill `retrieve-findings` (`.claude/skills/retrieve-findings/SKILL.md`). A daily GitHub Action (`.github/workflows/pending-drafts.yml`, script `scripts/pending-drafts.sh`) lists the drafts this ledger has not reviewed and keeps one open issue while any exist. This ledger is what makes the pull incremental: a draft is **new** until it has a row here.

Rows are keyed by the draft's path and the blob it had when reviewed, so a draft that changes later shows up again.

| Draft (in ic2-conquest `findings/`) | Reviewed at (commit) | Outcome | Promoted as | Date |
|---|---|---|---|---|
| `2026-09-29-recruiting-cities-need-fortification-75.md` | `a1df3b4` | promoted | `2026-09-29-which-cities-may-recruit-and-troop-amounts.md` (independent confirmation noted) | 2026-09-29 |
| `2026-09-29-loading-a-save-does-not-reseed.md` | `a1df3b4` | promoted, corrected (the two other `RandSeed` writers are the treaty and `TBattlePols`, not paint routines) | `2026-09-29-loading-a-save-does-not-reseed.md` | 2026-09-29 |
| `2026-09-29-nation-view-origin-and-unit-map-clicks.md` | `a1df3b4` | promoted | `2026-09-29-nation-view-origin-and-unit-map-clicks.md` | 2026-09-29 |
| `2026-10-02-unit-map-mouse-orders-and-tax-range.md` | `8c86cc1` | promoted (branch `experiment/unit-map-mouse`). Wine-only, so desktop confirmation is still owed; release `run-exp-unitmap-mouse` found and its saves re-checked against the report's tables; no contradiction with existing reports. Re-reviewed at `8c86cc1`: the only changes since `0a404f2` are the bot's own record of this promotion and a pointer to the fleet finding, no new claim | `2026-10-02-unit-map-mouse-orders-and-tax-range.md`; cross-links in three reports; evidence-index rows added | 2026-10-02 |
| `2026-10-02-fleet-orders-live.md` | `8c86cc1` | promoted (branch `feat/fleet-orders`). Wine-only, desktop confirmation owed; saves retrieved (git and release `run-exp-fleet-orders`) and re-read, every checkable number matches; confirms the fleet code reports, no contradiction; answers (f) of the unit-map draft | `2026-10-02-fleet-orders-live.md`; cross-links in two reports; evidence-index rows added | 2026-10-02 |

Outcomes: `promoted`, `promoted, corrected`, `promoted, provisional: <what is missing>`, `merged into <report>`, `rejected: <why>`, `deferred: <what evidence is missing>`.
