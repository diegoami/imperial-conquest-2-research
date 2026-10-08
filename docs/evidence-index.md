# Evidence index

Every save, screenshot and recording the reports cite, and the release that holds it.

The reports cite **bare filenames** — `11_supply.sav`, `1_rome_270_winter_7.sav` — never paths, because the binaries have never been in a repository and never will be. This file is what turns such a citation into something retrievable.

The originals live in the repository [`diegoami/imp_conquest_fixtures`](https://github.com/diegoami/imp_conquest_fixtures), organised as **one release per play-through**. Nothing here is committed to this repository or to the build repository: the game files, saves, screenshots and recordings stay out of both, and this index is a pointer, not a copy.

## The releases

The releases `run-exp-*` are in `diegoami/ic2-conquest`, not in the fixtures repository: each holds one bot experiment's saves and screenshots, which are Wine-only evidence (retrieve with `gh release download <tag> --repo diegoami/ic2-conquest`).

A few small probe saves are committed in the fixtures repository itself rather than in a release: `saves/new-game-probes/` (three new-game autosaves, 2026-09-29) and `saves/fortification-probe/` (a planted-order pair, 2026-09-29). Their rows in the table below link to the files in the repository.

| Release | What it is | Saves | Screenshots | Recordings |
|---|---|---|---|---|
| [`run-1-rome`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-rome) | Run 1 — Rome (270 BC) | 16 | 5 | 8 |
| [`run-1-cartago`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-cartago) | Run 1 — Carthage (271 BC) | 10 | 2 | 0 |
| [`run-1-thracia`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-thracia) | Run 1 — Thracia (271 BC) | 13 | 0 | 0 |
| [`run-1-ptolemy`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-ptolemy) | Run 1 — Ptolemaic (270 BC), the whole year | 45 | 0 | 22 |
| [`legacy-probes`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/legacy-probes) | Legacy probes | 15 | 25 | 3 |
| [`run-exp-unitmap-mouse`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-unitmap-mouse) | Bot experiment (2026-10-01/02, **Wine-only**, repo `diegoami/ic2-conquest`): Unit-map mouse orders and the Taxation range, from the fixed-seed start save | 15 | 15 | 0 |
| [`run-exp-fleet-orders`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleet-orders) | Bot experiment (2026-10-02, **Wine-only**, repo `diegoami/ic2-conquest`): fleet orders live (launch, embark/unload, supply, repair, split, join, transfer, scuttle) | 12 | 11 | 0 |
| [`run-exp-civ-sweep`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-civ-sweep) | Bot experiment (2026-10-02, **Wine-only**, repo `diegoami/ic2-conquest`): New Game as each of the 16 nations, two turns each | 48 | 28 | 0 |
| [`run-exp-two-humans`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-two-humans) | Bot experiment (2026-10-02, **Wine-only**, repo `diegoami/ic2-conquest`): two human seats (Carthage + Ptolemaic) | 4 | 6 | 0 |
| [`run-exp-fleet-battles`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleet-battles) | Bot experiment (2026-10-02, **Wine-only**, repo `diegoami/ic2-conquest`): two fleets (Carthage 90, Ptolemaic 70 ships) sailing toward each other, three rounds | 7 | 0 | 0 |
| [`run-exp-naval-battle`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-naval-battle) | Bot experiment (2026-10-02, **Wine-only**, repo `diegoami/ic2-conquest`): 160 naval battles between two fleets at war (`trials.json`), the fixtures and a probe | 13 | 3 | 0 |
| [`run-exp-naval-battle-cargo`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-naval-battle-cargo) | Bot experiment (2026-10-02/03, **Wine-only**, repo `diegoami/ic2-conquest`): 80 naval battles with an army aboard (a synthetic cargo edit), the eight fixtures and a natural-embark check (`t3_trials.json`) | 27 | 0 | 0 |
| [`run-exp-storms`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-storms) | Bot experiment (2026-10-03, **Wine-only**, repo `diegoami/ic2-conquest`): 90 storms on Carthage's fleet in 12 cells, some with condition, season or cargo edited (`t4_trials.json`), and a 7-turn natural idle run ending in a loss at sea | 87 | 0 | 0 |
| [`run-exp-pair2`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-pair2) | Bot experiment (2026-10-03, **Wine-only**, repo `diegoami/ic2-conquest`): Seleucid + Ptolemaic human, a built fleet at Issus, the refused attack, 20 battles of supplied fleets (`trials.json`) | 37 | 0 | 0 |
| [`run-exp-peace-prompt`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-peace-prompt) | Bot experiment (2026-10-03, **Wine-only**, repo `diegoami/ic2-conquest`): attacking a fleet of a nation on trade terms (No, Cancel, Yes) | 10 | 2 | 0 |
| [`run-exp-battle-sweep`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-sweep) | Bot experiment (2026-10-04, **Wine-only**, repo `diegoami/ic2-conquest`): the battle block decoded, crafted mid-battle saves, HI v HI end to end (running deliverable) | 467 | 53 | 0 |
| [`run-exp-battle-probe`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-probe) | Bot experiment (2026-10-04, **Wine-only**, repo `diegoami/ic2-conquest`): one tactical battle end to end on the lab build (gate runs, Save As, resume, the Offer of peace) | 366 | 59 | 0 |

### Which release to reach for

- **[`run-1-ptolemy`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-ptolemy)** is the **largest and best-structured run**, and the right one for almost any new question. One nation (Ptolemaic) across **22 consecutive turns** covering all of 270 BC, every turn recorded, and — uniquely — **every turn saved twice**: `IPnnn.sav` before the player's orders and `IPnnnB.sav` after them. That pair isolates the player's orders from the engine's between-turn processing, which no other release does. Its one gap is that the between-turn processing itself was **not recorded**.
- **[`legacy-probes`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/legacy-probes)** holds the **most-cited files in this repository**. A report citing a bare number — `7.sav`, `11_supply.sav`, `12_rom_a.sav` — means this release. Its `11`/`12` chain is a sequence of **single documented actions**, so a byte difference there is attributable to one change in a way a turn step never is.
- **[`run-1-rome`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-rome)** is the only run with **recordings and written per-turn observations**, so it is the only place a formula can be checked against a stated player intent rather than a byte difference alone.
- **[`run-1-thracia`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-thracia)** is the **densest uninterrupted series** — twelve consecutive two-week steps, no gaps, no branches — and so the right one for anything verified turn over turn. It has **no notes**: it shows state, not intent.
- **[`run-1-cartago`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-cartago)** is small but holds a **one-action save pair** (`spring_1` → `spring_1b`, a single fleet move) within the same turn.

**What has already been extracted from which recording is tracked in [`recording-ledger.md`](recording-ledger.md).** Read it before opening a video: runs arrive incrementally and it is the only record of which screens have been transcribed and which are merely known to exist.

## Three things that will mislead you if you do not know them

**1. A `_b` suffix is a branch, not a later turn.** `1_rome_270_winter_7` has two successors: `winter_9` (where the battle froze, four recordings) and `winter_7_b` → `winter_9_b` → `winter_11` (the same battle replayed on auto, no freeze). `winter_9` and `winter_9_b` are **two outcomes of the same week reached by different routes** — diffing them as consecutive turns produces nonsense. The `_b` chain is the one that continues.

**2. Some cited saves do not exist.** `1_rome_270_summer_9` and `summer_11` were never kept, and `1_rome.txt` says so; their events are documented but no save backs them. `1_cartago_271_spring_3` has a **screenshot but no save**. And the flat numbering has always skipped `2.sav` and `3.sav` — nothing is missing.

**3. GitHub rewrites spaces in asset names as dots.** A recording stored as `bandicam 2026-09-12 23-56-28-394.mp4` downloads as `bandicam.2026-09-12.23-56-28-394.mp4`. The **Asset** column below gives the name as it downloads.

## Saves

`cites` counts the reports in this repository that name the file — a rough guide to how load-bearing it is, not a quality judgement.

| Save | Release | Cites |
|---|---|---|
| [`recruit_after.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/fortification-probe/recruit_after.sav) | repo `saves/fortification-probe/` | 1 |
| [`fort_ui_after_ok.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/fortification-probe/fort_ui_after_ok.sav) | repo `saves/fortification-probe/` | 1 |
| [`fort_ui_after_turn.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/fortification-probe/fort_ui_after_turn.sav) | repo `saves/fortification-probe/` | 1 |
| [`cancel_probe.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/fortification-probe/cancel_probe.sav) | repo `saves/fortification-probe/` | 1 |
| [`cancel_probe_after.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/fortification-probe/cancel_probe_after.sav) | repo `saves/fortification-probe/` | 1 |
| [`fort_probe_before.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/fortification-probe/fort_probe_before.sav) | repo `saves/fortification-probe/` | 1 |
| [`fort_probe_after.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/fortification-probe/fort_probe_after.sav) | repo `saves/fortification-probe/` | 1 |
| [`ng1_rome.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/new-game-probes/ng1_rome.sav) | repo `saves/new-game-probes/` | 1 |
| [`ng2_rome.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/new-game-probes/ng2_rome.sav) | repo `saves/new-game-probes/` | 1 |
| [`ng3_carthage.sav`](https://github.com/diegoami/imp_conquest_fixtures/blob/main/saves/new-game-probes/ng3_carthage.sav) | repo `saves/new-game-probes/` | 1 |
| [`11_supply.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/11_supply.sav) | `legacy-probes` | 9 |
| [`1_rome_270_winter_7.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_winter_7.sav) | `run-1-rome` | 7 |
| [`7.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/7.sav) | `legacy-probes` | 6 |
| [`11.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/11.sav) | `legacy-probes` | 5 |
| [`1_rome_270_winter_9.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_winter_9.sav) | `run-1-rome` | 5 |
| [`8.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/8.sav) | `legacy-probes` | 5 |
| [`1.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/1.sav) | `legacy-probes` | 4 |
| [`11_ptol.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/11_ptol.sav) | `legacy-probes` | 4 |
| [`12_rom_a.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/12_rom_a.sav) | `legacy-probes` | 4 |
| [`1_rome_270_summer_7.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_summer_7.sav) | `run-1-rome` | 4 |
| [`1_rome_270_winter_1.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_winter_1.sav) | `run-1-rome` | 4 |
| [`1_rome_270_winter_11.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_winter_11.sav) | `run-1-rome` | 4 |
| [`10.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/10.sav) | `legacy-probes` | 3 |
| [`1_rome_270_winter_3.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_winter_3.sav) | `run-1-rome` | 3 |
| [`1_rome_270_winter_7_b.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_winter_7_b.sav) | `run-1-rome` | 3 |
| [`1_rome_270_winter_9_b.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_winter_9_b.sav) | `run-1-rome` | 3 |
| [`4.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/4.sav) | `legacy-probes` | 3 |
| [`9.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/9.sav) | `legacy-probes` | 3 |
| [`12_mac.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/12_mac.sav) | `legacy-probes` | 2 |
| [`12_ptol.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/12_ptol.sav) | `legacy-probes` | 2 |
| [`1_rome_270_autumn_1.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_autumn_1.sav) | `run-1-rome` | 2 |
| [`1_rome_270_autumn_5.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_autumn_5.sav) | `run-1-rome` | 2 |
| [`1_rome_270_autumn_7.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_autumn_7.sav) | `run-1-rome` | 2 |
| [`1_rome_270_autumn_9.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_autumn_9.sav) | `run-1-rome` | 2 |
| [`1_rome_270_winter_5.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_winter_5.sav) | `run-1-rome` | 2 |
| [`1_thracia_271_spring_11.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_spring_11.sav) | `run-1-thracia` | 2 |
| [`12_ptol_b.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/12_ptol_b.sav) | `legacy-probes` | 1 |
| [`1_cartago_271_spring_1.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_spring_1.sav) | `run-1-cartago` | 1 |
| [`1_cartago_271_spring_1b.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_spring_1b.sav) | `run-1-cartago` | 1 |
| [`1_cartago_271_summer_9.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_summer_9.sav) | `run-1-cartago` | 1 |
| [`1_rome_270_autumn_11.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_autumn_11.sav) | `run-1-rome` | 1 |
| [`1_rome_270_autumn_3.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_autumn_3.sav) | `run-1-rome` | 1 |
| [`1_rome_270_autumn_7_fleet.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/1_rome_270_autumn_7_fleet.sav) | `run-1-rome` | 1 |
| [`1_thracia_271_autumn_1.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_autumn_1.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_spring_1.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_spring_1.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_spring_3.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_spring_3.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_spring_7.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_spring_7.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_summer_1.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_summer_1.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_summer_9.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_summer_9.sav) | `run-1-thracia` | 1 |
| [`5.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/5.sav) | `legacy-probes` | 1 |
| [`6.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/6.sav) | `legacy-probes` | 1 |
| [`1_cartago_271_spring_11.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_spring_11.sav) | `run-1-cartago` | — |
| [`1_cartago_271_spring_5.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_spring_5.sav) | `run-1-cartago` | — |
| [`1_cartago_271_spring_7.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_spring_7.sav) | `run-1-cartago` | — |
| [`1_cartago_271_summer_1.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_summer_1.sav) | `run-1-cartago` | — |
| [`1_cartago_271_summer_3.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_summer_3.sav) | `run-1-cartago` | — |
| [`1_cartago_271_summer_5.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_summer_5.sav) | `run-1-cartago` | — |
| [`1_cartago_271_summer_7.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-cartago/1_cartago_271_summer_7.sav) | `run-1-cartago` | — |
| [`1_thracia_271_spring_5.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_spring_5.sav) | `run-1-thracia` | — |
| [`1_thracia_271_spring_9.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_spring_9.sav) | `run-1-thracia` | — |
| [`1_thracia_271_summer_11.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_summer_11.sav) | `run-1-thracia` | — |
| [`1_thracia_271_summer_3.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_summer_3.sav) | `run-1-thracia` | — |
| [`1_thracia_271_summer_5.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_summer_5.sav) | `run-1-thracia` | — |
| [`1_thracia_271_summer_7.sav`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-thracia/1_thracia_271_summer_7.sav) | `run-1-thracia` | — |
| [`A_AFTER_CLICKS.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/A_AFTER_CLICKS.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`B2_PEACE_GENUA_AFTER_NO.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/B2_PEACE_GENUA_AFTER_NO.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`C_AFTER_RIGHT_CLICK.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/C_AFTER_RIGHT_CLICK.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`D_AFTER_SHIFT_X.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/D_AFTER_SHIFT_X.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`E_AFTER_SPLIT.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/E_AFTER_SPLIT.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`G_TAX_MAX.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/G_TAX_MAX.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`G_TAX_MIN.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/G_TAX_MIN.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`T_SPLIT.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/T_SPLIT.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`B2_PEACE_GENUA_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/B2_PEACE_GENUA_BEFORE.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`B2_PEACE_GENUA_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/B2_PEACE_GENUA_AFTER.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`B2_WAR_FELSINA_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/B2_WAR_FELSINA_BEFORE.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`B2_WAR_FELSINA_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unitmap-mouse/B2_WAR_FELSINA_AFTER.SAV) | `run-exp-unitmap-mouse` (repo `ic2-conquest`) | 1 |
| [`FLEET.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/FLEET.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`FLEET2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/FLEET2.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_DISEMBARK.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_DISEMBARK.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_EMBARK.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_EMBARK.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_EMBARK_REFUSED.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_EMBARK_REFUSED.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_JOIN_FLEETS.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_JOIN_FLEETS.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_MOVE_FLEET.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_MOVE_FLEET.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_REPAIR_FLEET.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_REPAIR_FLEET.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_SCUTTLE_FLEET.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_SCUTTLE_FLEET.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_SPLIT_FLEET.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_SPLIT_FLEET.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_SUPPLY_FLEET.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_SUPPLY_FLEET.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_TRANSFER_SHIPS.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-orders/T_TRANSFER_SHIPS.SAV) | `run-exp-fleet-orders` (repo `ic2-conquest`) | 1 |
| [`T_SPLIT_198_ARMIES.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-l11-198-armies/T_SPLIT_198_ARMIES.SAV) | `run-exp-l11-198-armies` (repo `ic2-conquest`) | 1 |
| [`T_RECRUIT_40SLOTS.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-l11-40-recruit-slots/T_RECRUIT_40SLOTS.SAV) | `run-exp-l11-40-recruit-slots` (repo `ic2-conquest`) | 1 |
| [`MIRROR_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-l11-40-recruit-slots/MIRROR_PRE.SAV) | `run-exp-l11-40-recruit-slots` (repo `ic2-conquest`) | 1 |
| [`MIRROR_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-l11-40-recruit-slots/MIRROR_BEFORE.SAV) | `run-exp-l11-40-recruit-slots` (repo `ic2-conquest`) | 1 |
| [`MIRROR_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-l11-40-recruit-slots/MIRROR_AFTER.SAV) | `run-exp-l11-40-recruit-slots` (repo `ic2-conquest`) | 1 |
| [`c1_empty_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c1_empty_PRE.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c1_empty_0.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c1_empty_0.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c1_empty_1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c1_empty_1.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c2_gap_slot1_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c2_gap_slot1_PRE.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c2_gap_slot1_0.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c2_gap_slot1_0.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c2_gap_slot1_1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c2_gap_slot1_1.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c3_gap_slot0_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c3_gap_slot0_PRE.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c3_gap_slot0_0.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c3_gap_slot0_0.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c3_gap_slot0_1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c3_gap_slot0_1.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c3_gap_slot0_2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c3_gap_slot0_2.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c3_gap_slot0_3.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-recruit-slot-landing/c3_gap_slot0_3.SAV) | `run-exp-recruit-slot-landing` (repo `ic2-conquest`) | 1 |
| [`c1_10_10_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c1_10_10_PRE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c1_10_10_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c1_10_10_BEFORE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c1_10_10_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c1_10_10_AFTER.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c2_10_11_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c2_10_11_PRE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c2_10_11_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c2_10_11_BEFORE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c2_10_11_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c2_10_11_AFTER.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c3_gap_value21_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c3_gap_value21_PRE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c3_gap_value21_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c3_gap_value21_BEFORE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c3_gap_value21_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c3_gap_value21_AFTER.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c4_gap_value20_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c4_gap_value20_PRE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c4_gap_value20_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c4_gap_value20_BEFORE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c4_gap_value20_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c4_gap_value20_AFTER.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c5_partner_slot0_empty_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c5_partner_slot0_empty_PRE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c5_partner_slot0_empty_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c5_partner_slot0_empty_BEFORE.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c5_partner_slot0_empty_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-join-20-units/c5_partner_slot0_empty_AFTER.SAV) | `run-exp-join-20-units` (repo `ic2-conquest`) | 1 |
| [`c1_full_queue_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c1_full_queue_PRE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c1_full_queue_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c1_full_queue_BEFORE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c1_full_queue_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c1_full_queue_AFTER.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c2_empty_queue_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c2_empty_queue_PRE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c2_empty_queue_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c2_empty_queue_BEFORE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c2_empty_queue_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c2_empty_queue_AFTER.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c3_army_20_slots_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c3_army_20_slots_PRE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c3_army_20_slots_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c3_army_20_slots_BEFORE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c3_army_20_slots_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c3_army_20_slots_AFTER.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c4_army_gap_0_18_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c4_army_gap_0_18_PRE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c4_army_gap_0_18_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c4_army_gap_0_18_BEFORE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c4_army_gap_0_18_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c4_army_gap_0_18_AFTER.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c5_army_only_slot19_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c5_army_only_slot19_PRE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c5_army_only_slot19_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c5_army_only_slot19_BEFORE.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c5_army_only_slot19_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-merc-full-queue/c5_army_only_slot19_AFTER.SAV) | `run-exp-merc-full-queue` (repo `ic2-conquest`) | 1 |
| [`c1_18_plus_3_left_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c1_18_plus_3_left_PRE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c1_18_plus_3_left_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c1_18_plus_3_left_BEFORE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c1_18_plus_3_left_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c1_18_plus_3_left_AFTER.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c2_target_only_slot19_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c2_target_only_slot19_PRE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c2_target_only_slot19_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c2_target_only_slot19_BEFORE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c2_target_only_slot19_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c2_target_only_slot19_AFTER.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c2b_target_only_slot19_cancel_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c2b_target_only_slot19_cancel_PRE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c2b_target_only_slot19_cancel_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c2b_target_only_slot19_cancel_BEFORE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c2b_target_only_slot19_cancel_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c2b_target_only_slot19_cancel_AFTER.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c3_target_gap_0_9_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c3_target_gap_0_9_PRE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c3_target_gap_0_9_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c3_target_gap_0_9_BEFORE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c3_target_gap_0_9_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c3_target_gap_0_9_AFTER.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c4_18_plus_3_right_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c4_18_plus_3_right_PRE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c4_18_plus_3_right_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c4_18_plus_3_right_BEFORE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c4_18_plus_3_right_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c4_18_plus_3_right_AFTER.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c5_18_plus_3_cancel_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c5_18_plus_3_cancel_PRE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c5_18_plus_3_cancel_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c5_18_plus_3_cancel_BEFORE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c5_18_plus_3_cancel_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c5_18_plus_3_cancel_AFTER.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c6_target_gap_0_2_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c6_target_gap_0_2_PRE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c6_target_gap_0_2_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c6_target_gap_0_2_BEFORE.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c6_target_gap_0_2_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c6_target_gap_0_2_AFTER.SAV) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`c1_18_plus_3_left_selection.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-transfer-20-units/c1_18_plus_3_left_selection.png) | `run-exp-transfer-20-units` (repo `ic2-conquest`) | 1 |
| [`t24999_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t24999_PRE.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t24999_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t24999_BEFORE.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t24999_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t24999_AFTER.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t25000_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t25000_PRE.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t25000_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t25000_BEFORE.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t25000_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t25000_AFTER.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t49999_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t49999_PRE.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t49999_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t49999_BEFORE.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t49999_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t49999_AFTER.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t50000_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t50000_PRE.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t50000_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t50000_BEFORE.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`t50000_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-band/t50000_AFTER.SAV) | `run-exp-army-marker-band` (repo `ic2-conquest`) | 1 |
| [`w200_t24999.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w200_t24999.SAV) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w200_t24999_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w200_t24999_tile.png) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w216_t25000.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w216_t25000.SAV) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w216_t25000_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w216_t25000_tile.png) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w232_t50000.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w232_t50000.SAV) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w232_t50000_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w232_t50000_tile.png) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w216_t24999.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w216_t24999.SAV) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w216_t24999_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w216_t24999_tile.png) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w232_t24999.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w232_t24999.SAV) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w232_t24999_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w232_t24999_tile.png) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w200_t50000.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w200_t50000.SAV) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`w200_t50000_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/w200_t50000_tile.png) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`montage_bands.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-marker-icon/montage_bands.png) | `run-exp-army-marker-icon` (repo `ic2-conquest`) | 1 |
| [`s24_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s24_PRE.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s24_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s24_BEFORE.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s24_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s24_AFTER.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s25_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s25_PRE.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s25_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s25_BEFORE.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s25_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s25_AFTER.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s49_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s49_PRE.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s49_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s49_BEFORE.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s49_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s49_AFTER.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s50_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s50_PRE.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s50_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s50_BEFORE.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`s50_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/s50_AFTER.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w300_s24.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w300_s24.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w300_s24_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w300_s24_tile.png) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w316_s25.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w316_s25.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w316_s25_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w316_s25_tile.png) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w316_s49.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w316_s49.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w316_s49_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w316_s49_tile.png) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w332_s50.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w332_s50.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w332_s50_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w332_s50_tile.png) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w316_s24.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w316_s24.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w316_s24_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w316_s24_tile.png) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w332_s24.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w332_s24.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w332_s24_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w332_s24_tile.png) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w300_s50.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w300_s50.SAV) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`w300_s50_tile.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-marker-band/w300_s50_tile.png) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| `montage_bands.png` (fleet) | `run-exp-fleet-marker-band` (repo `ic2-conquest`) | 1 |
| [`sp1_split_30_by_10_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/sp1_split_30_by_10_PRE.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`sp1_split_30_by_10_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/sp1_split_30_by_10_BEFORE.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`sp1_split_30_by_10_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/sp1_split_30_by_10_AFTER.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`sp2_split_50_by_1_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/sp2_split_50_by_1_PRE.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`sp2_split_50_by_1_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/sp2_split_50_by_1_BEFORE.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`sp2_split_50_by_1_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/sp2_split_50_by_1_AFTER.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`tr1_transfer_25_24_by_1_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/tr1_transfer_25_24_by_1_PRE.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`tr1_transfer_25_24_by_1_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/tr1_transfer_25_24_by_1_BEFORE.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`tr1_transfer_25_24_by_1_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/tr1_transfer_25_24_by_1_AFTER.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`tr2_transfer_50_10_by_1_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/tr2_transfer_50_10_by_1_PRE.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`tr2_transfer_50_10_by_1_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/tr2_transfer_50_10_by_1_BEFORE.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`tr2_transfer_50_10_by_1_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-reband-orders/tr2_transfer_50_10_by_1_AFTER.SAV) | `run-exp-fleet-reband-orders` (repo `ic2-conquest`) | 1 |
| [`cover0_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/cover0_PRE.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`cover0_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/cover0_BEFORE.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`cover0_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/cover0_AFTER.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`cover1_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/cover1_PRE.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`cover1_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/cover1_BEFORE.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`cover1_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/cover1_AFTER.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`move_cover1_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/move_cover1_PRE.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`move_cover1_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/move_cover1_BEFORE.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`move_cover1_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-loser-rough-sea/move_cover1_AFTER.SAV) | `run-exp-naval-loser-rough-sea` (repo `ic2-conquest`) | 1 |
| [`disband_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/disband_PRE.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`disband_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/disband_BEFORE.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`disband_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/disband_AFTER.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`join_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/join_PRE.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`join_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/join_BEFORE.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`join_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/join_AFTER.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`battle_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/battle_PRE.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`battle_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/battle_BEFORE.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`battle_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-army-removal-tile/battle_AFTER.SAV) | `run-exp-army-removal-tile` (repo `ic2-conquest`) | 1 |
| [`one_man_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/one_man_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`one_man_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/one_man_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`one_man_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/one_man_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`spread_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/spread_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`spread_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/spread_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`spread_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/spread_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u99_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u99_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u99_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u99_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u99_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u99_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u100_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u100_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u100_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u100_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u100_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u100_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u150_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u150_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u150_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u150_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u150_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u150_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u79_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u79_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u79_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u79_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u79_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u79_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u80_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u80_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u80_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u80_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`u80_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/u80_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`ar26_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/ar26_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`ar26_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/ar26_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`ar26_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/ar26_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`ar27_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/ar27_PRE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`ar27_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/ar27_BEFORE.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`ar27_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-siege-army-removal/ar27_AFTER.SAV) | `run-exp-siege-army-removal` (repo `ic2-conquest`) | 1 |
| [`fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/blob/feat/fleet-orders/saves/fleet-port-antium-0734.SAV) | repo `ic2-conquest` `saves/` | 1 |
| [`fleet-split-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/blob/feat/fleet-orders/saves/fleet-split-antium-0734.SAV) | repo `ic2-conquest` `saves/` | 1 |
| [`S00_Rome_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S00_Rome_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S01_Carthage_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S01_Carthage_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S02_Seleucid_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S02_Seleucid_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S03_Ptolemaic_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S03_Ptolemaic_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S04_Macedonia_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S04_Macedonia_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S05_Numidia_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S05_Numidia_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S06_Gaul_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S06_Gaul_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S07_Greece_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S07_Greece_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S08_Celtiberia_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S08_Celtiberia_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S09_Illyria_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S09_Illyria_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S10_Dacia_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S10_Dacia_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S11_Bithynia_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S11_Bithynia_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S12_Galatia_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S12_Galatia_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S13_Armenia_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S13_Armenia_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S14_Media_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S14_Media_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`S15_Thracia_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-civ-sweep/S15_Thracia_AUTO0720.SAV) | `run-exp-civ-sweep` (repo `ic2-conquest`) | 1 |
| [`T0_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-two-humans/T0_AUTO0720.SAV) | `run-exp-two-humans` (repo `ic2-conquest`) | 1 |
| [`T0_NEWGAME_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-two-humans/T0_NEWGAME_AUTO0720.SAV) | `run-exp-two-humans` (repo `ic2-conquest`) | 1 |
| [`T0_P2_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-two-humans/T0_P2_AUTO0721.SAV) | `run-exp-two-humans` (repo `ic2-conquest`) | 1 |
| [`T0_P2_WAR.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-two-humans/T0_P2_WAR.SAV) | `run-exp-two-humans` (repo `ic2-conquest`) | 1 |
| [`T1_0720_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-battles/T1_0720_s02_Ptolemaic.SAV) | `run-exp-fleet-battles` (repo `ic2-conquest`) | 1 |
| [`T1_0720_s13_Carthage.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-battles/T1_0720_s13_Carthage.SAV) | `run-exp-fleet-battles` (repo `ic2-conquest`) | 1 |
| [`T1_0721_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-battles/T1_0721_s02_Ptolemaic.SAV) | `run-exp-fleet-battles` (repo `ic2-conquest`) | 1 |
| [`T1_0721_s13_Carthage.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-battles/T1_0721_s13_Carthage.SAV) | `run-exp-fleet-battles` (repo `ic2-conquest`) | 1 |
| [`T1_0722_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-battles/T1_0722_s02_Ptolemaic.SAV) | `run-exp-fleet-battles` (repo `ic2-conquest`) | 1 |
| [`T1_0722_s13_Carthage.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-battles/T1_0722_s13_Carthage.SAV) | `run-exp-fleet-battles` (repo `ic2-conquest`) | 1 |
| [`T1_0723_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-battles/T1_0723_s02_Ptolemaic.SAV) | `run-exp-fleet-battles` (repo `ic2-conquest`) | 1 |
| [`fleets-adjacent-at-sea-0723.SAV`](https://github.com/diegoami/ic2-conquest/blob/edf6d34/saves/fleets-adjacent-at-sea-0723.SAV) | repo `ic2-conquest` `saves/` | 1 |
| [`FIX_C_0723_carthage_seat.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/FIX_C_0723_carthage_seat.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`FIX_P2_0724_ptolemaic_seat_c60.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/FIX_P2_0724_ptolemaic_seat_c60.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`FIX_P_0723_ptolemaic_seat.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/FIX_P_0723_ptolemaic_seat.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`NB_C50_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/NB_C50_seed1.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`NB_C55_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/NB_C55_seed1.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`NB_C60_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/NB_C60_seed1.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`NB_C65_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/NB_C65_seed1.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`NB_C70_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/NB_C70_seed1.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`NB_C_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/NB_C_seed1.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`NB_P60_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/NB_P60_seed1.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`NB_P_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/NB_P_seed1.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`PROBE_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/PROBE_AFTER.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`PROBE_START.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle/PROBE_START.SAV) | `run-exp-naval-battle` (repo `ic2-conquest`) | 2 |
| [`FIX_T3_L25.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/FIX_T3_L25.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`FIX_T3_L10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/FIX_T3_L10.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`FIX_T3_L15D5.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/FIX_T3_L15D5.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`FIX_T3_A5.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/FIX_T3_A5.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`FIX_T3_L15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/FIX_T3_L15.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`FIX_T3_L5.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/FIX_T3_L5.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L15D5_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L15D5_seed1.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L15_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L15_seed1.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L25_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L25_seed1.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L5_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L5_seed1.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`T3_EDIT_CHECK.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/T3_EDIT_CHECK.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`T3_NATURAL_EMBARK.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/T3_NATURAL_EMBARK.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L15D5_seed2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L15D5_seed2.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L5_seed8.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L5_seed8.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L15_seed10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L15_seed10.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`FIX_T3_H15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/FIX_T3_H15.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`FIX_T3_M15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/FIX_T3_M15.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_A5_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_A5_seed1.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_A5_seed10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_A5_seed10.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_H15_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_H15_seed1.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L10_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L10_seed1.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_L10_seed2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_L10_seed2.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_M15_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_M15_seed1.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_M15_seed2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_M15_seed2.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_M15_seed5.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_M15_seed5.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_H15_seed10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_H15_seed10.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`NBC_M15_seed10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-naval-battle-cargo/NBC_M15_seed10.SAV) | `run-exp-naval-battle-cargo` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_H45s.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_H45s.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_H85s.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_H85s.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_K45s.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_K45s.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_K45w.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_K45w.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_K85s.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_K85s.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_K85w.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_K85w.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_R45s.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_R45s.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_R45sA.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_R45sA.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_R45w.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_R45w.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_R85s.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_R85s.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_R85sA.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_R85sA.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_T4_R85w.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_R85w.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed2_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed2_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed3_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed3_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed4_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed4_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed5_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed5_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_H45s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_H45s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_H85s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_H85s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed10_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed10_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed2_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed2_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed3_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed3_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed4_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed4_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed5_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed5_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed6_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed6_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed7_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed7_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed8_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed8_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed9_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed9_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed10_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed10_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed1_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed1_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed2_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed2_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed3_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed3_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed4_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed4_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed5_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed5_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed6_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed6_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed7_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed7_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed8_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed8_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45w_seed9_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45w_seed9_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K85s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K85s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K85w_seed1_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K85w_seed1_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed10_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed10_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed2_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed2_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed3_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed3_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed4_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed4_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed5_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed5_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed6_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed6_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed7_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed7_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed8_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed8_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45sA_seed9_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45sA_seed9_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed10_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed10_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed2_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed2_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed3_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed3_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed4_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed4_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed5_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed5_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed6_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed6_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed7_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed7_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed8_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed8_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed9_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed9_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed10_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed10_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed1_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed1_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed2_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed2_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed3_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed3_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed4_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed4_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed5_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed5_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed6_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed6_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed7_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed7_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed8_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed8_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45w_seed9_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45w_seed9_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R85sA_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R85sA_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R85s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R85s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R85w_seed1_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R85w_seed1_AUTO0739.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_01_0721_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_01_0721_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_02_0721_seat13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_02_0721_seat13.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_03_0722_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_03_0722_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_04_0722_seat13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_04_0722_seat13.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_05_0723_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_05_0723_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_06_0723_seat13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_06_0723_seat13.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_07_0724_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_07_0724_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_08_0724_seat13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_08_0724_seat13.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_09_0725_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_09_0725_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_10_0725_seat13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_10_0725_seat13.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_11_0726_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_11_0726_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_12_0726_seat13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_12_0726_seat13.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_13_0727_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_13_0727_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`FIX_S2_ptolemaic_seat_0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/FIX_S2_ptolemaic_seat_0735.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`FIX_S2_seleucid_seat_0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/FIX_S2_seleucid_seat_0735.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2B_P_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2B_P_seed1.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2B_S_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2B_S_seed1.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0720_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0720_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0720_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0720_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0721_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0721_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0721_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0721_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0722_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0722_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0722_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0722_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0723_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0723_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0723_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0723_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0724_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0724_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0724_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0724_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0725_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0725_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0725_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0725_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0726_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0726_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0726_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0726_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0727_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0727_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0727_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0727_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0728_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0728_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0728_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0728_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0729_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0729_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0729_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0729_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0730_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0730_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0730_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0730_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0731_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0731_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0731_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0731_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0732_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0732_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0732_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0732_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0733_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0733_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0733_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0733_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0734_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0734_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0734_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0734_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0735_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0735_s02_Ptolemaic.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_0735_s04_Seleucid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_0735_s04_Seleucid.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`P2_FIXTURE_seleucid_seat.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-pair2/P2_FIXTURE_seleucid_seat.SAV) | `run-exp-pair2` (repo `ic2-conquest`) | 1 |
| [`PP_yes_seed1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/PP_yes_seed1.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`PP_yes_seed1_AUTO0723.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/PP_yes_seed1_AUTO0723.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`T1P_0720_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/T1P_0720_s02_Ptolemaic.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`T1P_0720_s13_Carthage.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/T1P_0720_s13_Carthage.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`T1P_0721_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/T1P_0721_s02_Ptolemaic.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`T1P_0721_s13_Carthage.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/T1P_0721_s13_Carthage.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`T1P_0722_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/T1P_0722_s02_Ptolemaic.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`T1P_0722_s13_Carthage.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/T1P_0722_s13_Carthage.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`T1P_0723_s02_Ptolemaic.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/T1P_0723_s02_Ptolemaic.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`T1P_FIXTURE_fleets_adjacent.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-prompt/T1P_FIXTURE_fleets_adjacent.SAV) | `run-exp-peace-prompt` (repo `ic2-conquest`) | 1 |
| [`gate2_a_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_a_BATTLE01.SAV) … `gate2_a_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_a_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_a_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_b_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_b_BATTLE01.SAV) … `gate2_b_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_b_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_b_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_c_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_c_BATTLE01.SAV) … `gate2_c_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_c_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_c_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_d_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_d_BATTLE01.SAV) … `gate2_d_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_d_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_d_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_e_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_e_BATTLE01.SAV) … `gate2_e_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_e_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_e_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_f_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_f_BATTLE01.SAV) … `gate2_f_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_f_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_f_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_s2a_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_s2a_BATTLE01.SAV) … `gate2_s2a_BATTLE18.SAV` (18 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_s2a_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_s2a_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_s2b_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_s2b_BATTLE01.SAV) … `gate2_s2b_BATTLE18.SAV` (18 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`gate2_s2b_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/gate2_s2b_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_a_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_a_BATTLE01.SAV) … `lab1_a_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_a_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_a_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_b_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_b_BATTLE01.SAV) … `lab1_b_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_b_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_b_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_c_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_c_BATTLE01.SAV) … `lab1_c_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_c_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_c_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_d_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_d_BATTLE01.SAV) … `lab1_d_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_d_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_d_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_e_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_e_BATTLE01.SAV) … `lab1_e_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_e_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_e_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_t0_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_t0_BATTLE01.SAV) … `lab1_t0_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab1_t0_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab1_t0_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab2_a_after_no.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab2_a_after_no.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab2_a_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab2_a_BATTLE01.SAV) … `lab2_a_BATTLE18.SAV` (18 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab2_b_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab2_b_BATTLE01.SAV) … `lab2_b_BATTLE18.SAV` (18 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`lab2_b_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/lab2_b_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`NB_post_battle.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/NB_post_battle.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`NB_pre_attack-20261004-081149.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/NB_pre_attack-20261004-081149.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`NB_pre_attack.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/NB_pre_attack.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume01_lab1_a_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume01_lab1_a_BATTLE01.SAV) … `resume01_lab1_a_BATTLE22.SAV` (22 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume05_gate2_a_r1_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume05_gate2_a_r1_BATTLE01.SAV) … `resume05_gate2_a_r1_BATTLE10.SAV` (10 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume05_gate2_a_r2_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume05_gate2_a_r2_BATTLE01.SAV) … `resume05_gate2_a_r2_BATTLE10.SAV` (10 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume05_lab1_a_BATTLE01-20261004-083212.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume05_lab1_a_BATTLE01-20261004-083212.SAV) … `resume05_lab1_a_BATTLE10-20261004-083212.SAV` (10 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume05_lab1_a_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume05_lab1_a_BATTLE01.SAV) … `resume05_lab1_a_BATTLE10.SAV` (10 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`RESUME_01_lab1_a.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/RESUME_01_lab1_a.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume_01_lab1_a_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume_01_lab1_a_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`RESUME_05_gate2_a_r1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/RESUME_05_gate2_a_r1.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume_05_gate2_a_r1_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume_05_gate2_a_r1_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`RESUME_05_gate2_a_r2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/RESUME_05_gate2_a_r2.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume_05_gate2_a_r2_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume_05_gate2_a_r2_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`RESUME_05_lab1_a.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/RESUME_05_lab1_a.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`resume_05_lab1_a_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/resume_05_lab1_a_post.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`silab_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/silab_BATTLE01.SAV) … `silab_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`SI_lab_mid2_menu.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/SI_lab_mid2_menu.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`SI_lab_mid_menu.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/SI_lab_mid_menu.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`SI_lab_placement_menu.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/SI_lab_placement_menu.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`SI_lab_post_battle.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/SI_lab_post_battle.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`SI_mid2_menu.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/SI_mid2_menu.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`SI_mid_menu.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/SI_mid_menu.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`SI_placement_menu.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/SI_placement_menu.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`SI_post_battle.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/SI_post_battle.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`WIN_post_battle.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-probe/WIN_post_battle.SAV) | `run-exp-battle-probe` (repo `ic2-conquest`) | 2 |
| [`B2_after_end2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_after_end2.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`B2_after_end_turn_1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_after_end_turn_1.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`B2_after_end_turn_2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_after_end_turn_2.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`B2_nat_p1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_nat_p1.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`B2_nat_p2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_nat_p2.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`B2_placement.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_placement.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c0_control_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c0_control_BATTLE01.SAV) … `b3_c0_control_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c0_control_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c0_control_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c1_noop_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c1_noop_BATTLE01.SAV) … `b3_c1_noop_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c1_noop_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c1_noop_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c2_troops_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c2_troops_BATTLE01.SAV) … `b3_c2_troops_BATTLE11.SAV` (11 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c2_troops_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c2_troops_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c3_adjacent_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c3_adjacent_BATTLE01.SAV) … `b3_c3_adjacent_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c3_adjacent_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c3_adjacent_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c4_slot_only_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c4_slot_only_BATTLE01.SAV) … `b3_c4_slot_only_BATTLE11.SAV` (11 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c4_slot_only_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c4_slot_only_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c5_stale_grid_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c5_stale_grid_BATTLE01.SAV) … `b3_c5_stale_grid_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c5_stale_grid_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c5_stale_grid_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c6_same_cell_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c6_same_cell_BATTLE01.SAV) … `b3_c6_same_cell_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c6_same_cell_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c6_same_cell_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c7_type_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c7_type_BATTLE01.SAV) … `b3_c7_type_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c7_type_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c7_type_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d0_control_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d0_control_BATTLE01.SAV) … `b3_d0_control_BATTLE13.SAV` (13 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d0_control_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d0_control_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d3_adjacent_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d3_adjacent_BATTLE01.SAV) … `b3_d3_adjacent_BATTLE11.SAV` (11 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d3_adjacent_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d3_adjacent_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d5_stale_grid_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d5_stale_grid_BATTLE01.SAV) … `b3_d5_stale_grid_BATTLE13.SAV` (13 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d5_stale_grid_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d5_stale_grid_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d6_same_cell_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d6_same_cell_BATTLE01.SAV) … `b3_d6_same_cell_BATTLE11.SAV` (11 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d6_same_cell_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d6_same_cell_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d8_far_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d8_far_BATTLE01.SAV) … `b3_d8_far_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d8_far_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d8_far_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_e0_x2_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_e0_x2_BATTLE01.SAV) … `b3_e0_x2_BATTLE11.SAV` (11 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_e0_x2_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_e0_x2_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_c0_control.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_c0_control.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_c1_noop.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_c1_noop.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_c2_troops.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_c2_troops.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_c3_adjacent.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_c3_adjacent.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_c4_slot_only.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_c4_slot_only.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_c5_stale_grid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_c5_stale_grid.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_c6_same_cell.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_c6_same_cell.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_c7_type.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_c7_type.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_d0_control.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_d0_control.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_d3_adjacent.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_d3_adjacent.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_d5_stale_grid.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_d5_stale_grid.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_d6_same_cell.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_d6_same_cell.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_d8_far.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_d8_far.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`CRAFT_e0_x2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/CRAFT_e0_x2.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`FLD-RG_0743_rome_army0_at_86_28.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/FLD-RG_0743_rome_army0_at_86_28.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`FLD-RG_build_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/FLD-RG_build_b.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`gate2_a_BATTLE04.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/gate2_a_BATTLE04.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s1_r1_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s1_r1_BATTLE01.SAV) … `hi-hi-one_s1_r1_BATTLE19.SAV` (19 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s1_r1_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s1_r1_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s1_r2_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s1_r2_BATTLE01.SAV) … `hi-hi-one_s1_r2_BATTLE19.SAV` (19 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s1_r2_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s1_r2_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s1_r3_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s1_r3_BATTLE01.SAV) … `hi-hi-one_s1_r3_BATTLE19.SAV` (19 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s1_r3_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s1_r3_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s1_r4_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s1_r4_BATTLE01.SAV) … `hi-hi-one_s1_r4_BATTLE19.SAV` (19 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s1_r4_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s1_r4_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s2_r1_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s2_r1_BATTLE01.SAV) … `hi-hi-one_s2_r1_BATTLE18.SAV` (18 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s2_r1_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s2_r1_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s2_r2_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s2_r2_BATTLE01.SAV) … `hi-hi-one_s2_r2_BATTLE18.SAV` (18 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s2_r2_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s2_r2_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s2_r3_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s2_r3_BATTLE01.SAV) … `hi-hi-one_s2_r3_BATTLE18.SAV` (18 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s2_r3_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s2_r3_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s2_r4_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s2_r4_BATTLE01.SAV) … `hi-hi-one_s2_r4_BATTLE18.SAV` (18 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s2_r4_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s2_r4_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s3_r1_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s3_r1_BATTLE01.SAV) … `hi-hi-one_s3_r1_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s3_r1_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s3_r1_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s3_r2_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s3_r2_BATTLE01.SAV) … `hi-hi-one_s3_r2_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s3_r2_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s3_r2_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s3_r3_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s3_r3_BATTLE01.SAV) … `hi-hi-one_s3_r3_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s3_r3_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s3_r3_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s3_r4_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s3_r4_BATTLE01.SAV) … `hi-hi-one_s3_r4_BATTLE15.SAV` (15 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_s3_r4_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_s3_r4_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`hi-hi-one_start.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/hi-hi-one_start.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`stray_b2_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/stray_b2_BATTLE01.SAV) … `stray_b2_BATTLE06.SAV` (6 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`stray_b3_c0_control_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/stray_b3_c0_control_BATTLE01.SAV) … `stray_b3_c0_control_BATTLE11.SAV` (11 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |

## Recordings

Every recording that **any source** ties to specific evidence is published.

**Correction, 2026-09-19.** This section first said three recordings were *"deliberately not here — nothing in the notes says what they show."* That was wrong, and the mistake is worth stating rather than quietly fixing: the check looked only at `notes/`, and **all three are cited in reports** — they are among the most load-bearing recordings in the corpus. `bandicam 2026-09-12 05-27-11-464` alone is cited by four documents and is the source of every tactical combat constant in [`battle-recording-melee-cap-confirmed.md`](reports/battle-recording-melee-cap-confirmed.md). All three are now in `legacy-probes`.

**The lesson for anything added later**: `notes/` is *a* mapping, not *the* mapping. A recording is attributed if a note names it **or** a report cites it — check both.

| Asset (as downloaded) | Spans | Release |
|---|---|---|
| [`bandicam.2026-09-12.05-27-11-464.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/bandicam.2026-09-12.05-27-11-464.mp4) | A tactical battle. **Six fully-specified combat exchanges** around 1:48–3:00; the source for the melee cap and the tactical constants. Cited by four documents. | `legacy-probes` |
| [`bandicam.2026-09-12.05-42-33-198.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/bandicam.2026-09-12.05-42-33-198.mp4) | Strategic play across `7.sav`–`10.sav`. See [`strategic-recording-and-summer-saves.md`](reports/strategic-recording-and-summer-saves.md). | `legacy-probes` |
| [`bandicam.2026-09-12.06-04-01-165.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/legacy-probes/bandicam.2026-09-12.06-04-01-165.mp4) | The menus and toolbars, panel by panel. See [`menu-and-toolbar-inventory.md`](reports/menu-and-toolbar-inventory.md). | `legacy-probes` |
| [`bandicam.2026-09-12.23-56-28-394.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/bandicam.2026-09-12.23-56-28-394.mp4) | 1_rome_270_winter_3.sav .. 1_rome_270_winter_5.sav | `run-1-rome` |
| [`bandicam.2026-09-13.00-04-38-377.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/bandicam.2026-09-13.00-04-38-377.mp4) | 1_rome_270_winter_5.sav .. 1_rome_270_winter_7.sav | `run-1-rome` |
| [`bandicam.2026-09-13.00-31-14-131.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/bandicam.2026-09-13.00-31-14-131.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_9.sav (1 of 4) | `run-1-rome` |
| [`bandicam.2026-09-13.00-32-26-388.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/bandicam.2026-09-13.00-32-26-388.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_9.sav (2 of 4) | `run-1-rome` |
| [`bandicam.2026-09-13.00-35-54-640.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/bandicam.2026-09-13.00-35-54-640.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_9.sav (3 of 4) | `run-1-rome` |
| [`bandicam.2026-09-13.01-03-29-805.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/bandicam.2026-09-13.01-03-29-805.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_9.sav (4 of 4) | `run-1-rome` |
| [`bandicam.2026-09-13.22-49-01-893.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/bandicam.2026-09-13.22-49-01-893.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_7_b.sav | `run-1-rome` |
| [`bandicam.2026-09-13.23-14-41-582.mp4`](https://github.com/diegoami/imp_conquest_fixtures/releases/download/run-1-rome/bandicam.2026-09-13.23-14-41-582.mp4) | 1_rome_270_winter_9_b.sav .. 1_rome_270_winter_11.sav | `run-1-rome` |

## Screenshots

The two `.txt` files in `legacy-probes` — `11_supply.txt` and `12_ptol.txt` — are the contemporaneous notes saying what each image shows, and are **the authority over any later guess**. `11_supply.4/.5` carry the nation colour and identifier table (left to right for colours, top to bottom for names, 0–15 for identifiers), which is the source for the sixteen-nation palette.

| Release | Screenshots |
|---|---|
| [`run-1-rome`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-rome) | `1_rome_270_autumn_1_1.png`, `1_rome_270_autumn_3_1.png`, `1_rome_270_autumn_7_1.png`, `1_rome_270_summer_7_1.png`, `1_rome_270_summer_9_1.png` |
| [`run-1-cartago`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-cartago) | `1_cartago_271_spring_1b_1.png`, `1_cartago_271_spring_3_1.png` |
| [`legacy-probes`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/legacy-probes) | `11_supply.1.png`, `11_supply.2.png`, `11_supply.3.png`, `11_supply.4.png`, `11_supply.5.png`, `11_supply.6.png`, `11_supply.7.png`, `11_supply.8.png`, `11_supply.txt`, `12_ptol.1.png`, `12_ptol.txt`, `12_ptol_2.png`, `12_ptol_3.png`, `12_rom_1.png`, `12_rom_2.png`, `12_rom_3.png`, `7.1.png`, `7.2.png`, `7.3.png`, `7.4.png`, `7.5.png`, `7.6.png`, `7.7.png`, `7.8.png`, `Initial_world.1.png` |
| [`run-exp-unitmap-mouse`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-unitmap-mouse) (repo `ic2-conquest`) | `A_1_selected.png`, `A_2_after_moves.png`, `B2_PEACE_GENUA_click1.png`, `B2_PEACE_GENUA_click2.png`, `B2_WAR_FELSINA_click1.png`, `B_control_after_click.png`, `B_test_prompt.png`, `C_1_left_click.png`, `C_2_right_click.png`, `D_1_selected.png`, `D_2_after_shift_x.png`, `tax_end.png`, `tax_home.png`, `tax_open.png`, `X_end_turn_supplies_prompt.png` |
| [`run-exp-fleet-orders`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleet-orders) (repo `ic2-conquest`) | `disembark.png`, `embark_box.png`, `embark_ok.png`, `fleet4_join.png`, `fleet4_repair.png`, `fleet4_scuttle.png`, `fleet4_supply.png`, `fleet4_transfer.png`, `fleet_sel.png`, `fleet_split.png`, `sp2_all.png` |
| [`run-exp-civ-sweep`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-civ-sweep) (repo `ic2-conquest`) | `S00_Rome_army_selected.png`, `S00_Rome_recruit.png`, `S01_Carthage_army_selected.png`, `S01_Carthage_recruit.png`, `S02_Seleucid_army_selected.png`, `S02_Seleucid_recruit.png`, `S03_Ptolemaic_army_selected.png`, `S03_Ptolemaic_recruit.png`, `S04_Macedonia_army_selected.png`, `S04_Macedonia_recruit.png`, `S05_Numidia_recruit.png`, `S06_Gaul_army_selected.png`, `S06_Gaul_recruit.png`, `S07_Greece_recruit.png`, `S08_Celtiberia_army_selected.png`, `S08_Celtiberia_recruit.png`, `S09_Illyria_recruit.png`, `S10_Dacia_end_turn_stuck.png`, `S10_Dacia_recruit.png`, `S11_Bithynia_army_selected.png`, `S11_Bithynia_recruit.png`, `S12_Galatia_army_selected.png`, `S12_Galatia_recruit.png`, `S13_Armenia_recruit.png`, `S14_Media_army_selected.png`, `S14_Media_recruit.png`, `S15_Thracia_army_selected.png`, `S15_Thracia_recruit.png` |
| [`run-exp-two-humans`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-two-humans) (repo `ic2-conquest`) | `t0_after_A_end.png`, `t0_final.png`, `t0_p2_after_war.png`, `t0_p2_next_round.png`, `t0_relations_dialog_carthage.png`, `t0_seatA.png` |
| [`run-exp-naval-battle`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-naval-battle) (repo `ic2-conquest`) | `probe_1_selected.png`, `probe_2_t00_1.png`, `probe_3_after.png` |
| [`run-exp-peace-prompt`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-peace-prompt) (repo `ic2-conquest`) | `peace_prompt_box_cancel_seed1.png`, `peace_prompt_box_no_seed1.png` |
| [`run-exp-battle-probe`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-probe) (repo `ic2-conquest`) | `b0-gate-20261004-082351-battle-ended-window.png`, `b0-gate-20261004-085012-battle-ended-window.png`, `b0-gate-20261004-085012-offer-of-peace-root.png`, `b0-gate-20261004-085012-offer-of-peace-window.png`, `b0-lab-b-20261004-083709-battle-ended-window.png`, `b0-lab-b-20261004-083709-offer-of-peace-root.png`, `b0-lab-b-20261004-083709-offer-of-peace-window.png`, `b0-lab-t0-20261004-082246-battle-ended-window.png`, `b0-normal-20261004-080731-01-loaded.png`, `b0-normal-20261004-081149-01-loaded.png`, `b0-normal-20261004-081149-02-battle-placement.png`, `b0-normal-20261004-081149-03-after-computer-general.png`, `b0-normal-20261004-081149-04-battle-ended.png`, `b0-normal-20261004-081149-04b-battle-ended-window.png`, `b0-normal-20261004-081149-05-after-ok-open.png`, `b0-peace-capture-20261004-083010-01-offer-of-peace-root.png`, `b0-peace-capture-20261004-083010-01b-offer-of-peace-window.png`, `b0-peace-capture-20261004-083010-02-after-no.png`, `b0-resume-gate2_a-05_r1-20261004-085805-01-resumed.png`, `b0-resume-gate2_a-05_r1-20261004-085805-battle-ended-window.png`, `b0-resume-gate2_a-05_r2-20261004-085841-01-resumed.png`, `b0-resume-gate2_a-05_r2-20261004-085841-battle-ended-window.png`, `b0-resume-lab1_a-01-20261004-083247-01-resumed.png`, `b0-resume-lab1_a-01-20261004-083247-battle-ended-window.png`, `b0-resume-lab1_a-05-20261004-083111-01-resumed.png`, `b0-resume-lab1_a-05-20261004-083111-battle-ended-window.png`, `b0-resume-lab1_a-05-20261004-083212-01-resumed.png`, `b0-resume-lab1_a-05-20261004-083212-battle-ended-window.png`, `b0-savein-20261004-081536-01-placement.png`, `b0-savein-20261004-081536-02-move-phase.png`, `b0-savein-20261004-081536-move-menu-after-menu.png`, `b0-savein-20261004-081536-placement-menu-after-menu.png`, `b0-savein-20261004-081536-placement-toolbar-after-toolbar.png`, `b0-savein-20261004-081801-01-placement.png`, `b0-savein-20261004-081801-02-move-phase.png`, `b0-savein-20261004-081801-move-menu-noreset-after-menu.png`, `b0-savein-20261004-081801-placement-menu-after-menu.png`, `b0-savein-20261004-081801-placement-toolbar-after-toolbar.png`, `b0-savein-20261004-082013-01-placement.png`, `b0-savein-20261004-082013-02-after-end-turn-1.png`, `b0-savein-20261004-082013-02-after-end-turn-2.png`, `b0-savein-20261004-082013-battle-ended-window.png`, `b0-savein-20261004-082013-mid-menu-after-menu.png`, `b0-savein-20261004-082013-mid2-menu-after-menu.png`, `b0-savein-20261004-082013-placement-menu-after-menu.png`, `b0-savein-20261004-082013-placement-toolbar-after-toolbar.png`, `b0-savein-lab-20261004-083350-01-placement.png`, `b0-savein-lab-20261004-083350-02-after-end-turn-1.png`, `b0-savein-lab-20261004-083350-02-after-end-turn-2.png`, `b0-savein-lab-20261004-083350-battle-ended-window.png`, `b0-savein-lab-20261004-083350-mid-menu-after-menu.png`, `b0-savein-lab-20261004-083350-mid2-menu-after-menu.png`, `b0-savein-lab-20261004-083350-offer-of-peace-root.png`, `b0-savein-lab-20261004-083350-offer-of-peace-window.png`, `b0-savein-lab-20261004-083350-placement-menu-after-menu.png`, `b0-savein-lab-20261004-083350-placement-toolbar-after-toolbar.png`, `b0-win-20261004-083605-01-placement.png`, `b0-win-20261004-083605-02-after-ok.png`, `b0-win-20261004-083605-battle-ended-window.png` |
| [`run-exp-battle-sweep`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-sweep) (repo `ic2-conquest`) | `b2_after_end1_window.png`, `b2_after_end2_window.png`, `b2_after_end_turn_1_window.png`, `b2_after_end_turn_2_window.png`, `b2_placement_root.png`, `b2_placement_window.png`, `b3_c0_control_battle-ended.png`, `b3_c0_control_resumed.png`, `b3_c1_noop_battle-ended.png`, `b3_c1_noop_resumed.png`, `b3_c2_troops_battle-ended.png`, `b3_c2_troops_resumed.png`, `b3_c3_adjacent_battle-ended.png`, `b3_c3_adjacent_resumed.png`, `b3_c4_slot_only_battle-ended.png`, `b3_c4_slot_only_resumed.png`, `b3_c5_stale_grid_battle-ended.png`, `b3_c5_stale_grid_resumed.png`, `b3_c6_same_cell_battle-ended.png`, `b3_c6_same_cell_resumed.png`, `b3_c7_type_battle-ended.png`, `b3_c7_type_resumed.png`, `b3_d0_control_battle-ended.png`, `b3_d0_control_resumed.png`, `b3_d3_adjacent_battle-ended.png`, `b3_d3_adjacent_resumed.png`, `b3_d5_stale_grid_battle-ended.png`, `b3_d5_stale_grid_resumed.png`, `b3_d6_same_cell_battle-ended.png`, `b3_d6_same_cell_resumed.png`, `b3_d8_far_battle-ended.png`, `b3_d8_far_resumed.png`, `b3_e0_x2_battle-ended.png`, `b3_e0_x2_resumed.png`, `hi-hi-one_s1_r1_dialog-Offer_of_peace-1791098296.png`, `hi-hi-one_s1_r2_battle-ended.png`, `hi-hi-one_s1_r2_dialog-Offer_of_peace-1791098612.png`, `hi-hi-one_s1_r3_battle-ended.png`, `hi-hi-one_s1_r3_dialog-Offer_of_peace-1791100415.png`, `hi-hi-one_s1_r4_battle-ended.png`, `hi-hi-one_s1_r4_dialog-Offer_of_peace-1791100472.png`, `hi-hi-one_s2_r1_battle-ended.png`, `hi-hi-one_s2_r2_battle-ended.png`, `hi-hi-one_s2_r3_battle-ended.png`, `hi-hi-one_s2_r4_battle-ended.png`, `hi-hi-one_s3_r1_battle-ended.png`, `hi-hi-one_s3_r1_dialog-Offer_of_peace-1791098775.png`, `hi-hi-one_s3_r2_battle-ended.png`, `hi-hi-one_s3_r2_dialog-Offer_of_peace-1791098834.png`, `hi-hi-one_s3_r3_battle-ended.png`, `hi-hi-one_s3_r3_dialog-Offer_of_peace-1791100633.png`, `hi-hi-one_s3_r4_battle-ended.png`, `hi-hi-one_s3_r4_dialog-Offer_of_peace-1791100690.png` |
| [`run-exp-leaders-form`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-leaders-form) (repo `ic2-conquest`) | recordings of the 15 plays in five archives, one per runner batch: `batch-b1-b3.tar.gz`, `batch-b4-b5.tar.gz`, `batch-b6.tar.gz`, `batch-b7.tar.gz`, `batch-b8.tar.gz` (`batch-b8.tar.gz` is the evidence batch cited by `reports/2026-10-06-leaders-form.md`: raw helper output, nation-record dumps, autosaves and screenshots; data under `runs/experiments/data/run-exp-leaders-form/`) |
| [`run-exp-ai-turn`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-ai-turn) (repo `ic2-conquest`) | bot experiment (2026-10-07, Wine-only, fixed seed 424242, natural play): one autosave per turn 0720-0732 across two season boundaries, plus the aborted attempt's saves under `pre-run-game-folder/`; two archives `batch-b1.tar.gz`, `batch-b2.tar.gz` (13 saves, SHA-256 in the repo's `runs/experiments/data/run-exp-ai-turn/SAVES.sha256`); the in-play corroboration of the strategic-AI-turn report's week-11 tax policy and free AI mercenary hire (`reports/2026-10-07-ai-turn-corroboration.md`) |
| [`run-exp-cosmetic-gaps`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-cosmetic-gaps) (repo `ic2-conquest`) | bot experiment (2026-10-06/07, Wine-only, repo fixtures plus one staged save `STAGED-felsina-neutral-0721.SAV`): five archives `batch-b1.tar.gz`, `batch-b3.tar.gz`, `batch-b4.tar.gz` (with b5/b6/first-probe binaries), `batch-b7.tar.gz`, `batch-b8.tar.gz`; the in-play confirmation of the title bar, the ten sound files (cases 1, 2, 8, 9 by strace `openat`; the rest `[derived]` only), the area-map colour toggle (the byte at +0x46C, the run-length measurement across two clicks, the markers-cleared result), window positions kept in the save (Area map L+T+H+W per nation record at +0x46E/+0x470/+0x472/+0x474; save→reload round-trip), and the Supply army dialog's `Buy supplies` button visibility per case (own city: hidden; hostile: no dialog; non-hostile [STAGED]: present at the resource's declared rectangle; buttons toggle Visible, not Enabled) — audit `claims_audit_cosmetic.v13.txt` 348 checks 0 mismatches (`reports/2026-10-06-cosmetic-gaps.md`) |
| [`run-exp-feature-inventory`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-feature-inventory) (repo `ic2-conquest`) | bot experiment (2026-10-08, Wine-only, own Xvfb `:700`, own copy of the game folder, fixture `BASE.SAV` seed 12345): two screenshot archives `FI_batch1_screenshots.tar.gz` (43 screenshots, including the About box with its `CAncell` button, the Cellular Automata window after N, the Help topics viewer, the Unit-map submenus, every menu, the nation status panel, the city/army/foreign-army information panels, the new-player/new-nation/abdicate prompts) and `FI_batch2_screenshots.tar.gz` (18 screenshots, including the on→off→on hint cycle, the byte-identical SHA-256 of `FI_b2_03_hint_on_before.png` and `FI_b2_03_hint_on_again.png`); data under `runs/experiments/data/run-exp-feature-inventory/` (form controls, function list, dump string literals, help_topics/help_contents_entries TSVs after the 247/247 phrase-decoder fix, MANIFEST-batch1.txt and MANIFEST-batch2.txt). Source for the cell-level verifications of feature-inventory rows H01–H05, MM01–MM10 — six reports promoted from this release: `2026-10-08-help-topics-h01.md`, `2026-10-08-show-hints-h02.md`, `2026-10-08-about-imperial-conquest-h03.md`, `2026-10-08-cellular-automata-easter-egg-h04.md`, `2026-10-08-help-reference-tables-h05.md`, `2026-10-08-map-mouse-actions-mm01-mm10.md` |
| [`run-exp-ai-contact`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-ai-contact) (repo `ic2-conquest`) | bot experiment (2026-10-07, Wine-only, fixed seed 424242, natural play): b1 the 12-turn control run (0720-0732, one save per turn); b3 the human-mover staged plays plus the chase that followed a stale memory slot (`b3a_*` 0733-0738); two archives `batch-b1.tar.gz`, `batch-b3.tar.gz` (SHA-256 in the repo's `runs/experiments/data/run-exp-ai-contact/SAVES.sha256`); the in-play corroboration that `FUN_0044d734`'s contact resolution is shared between AI and human, with the AI-mover army-tile branch resolving instantly through `FUN_0044aee4` when both seats are computer, the human-involved branch opening the tactical battle, and the human long walk unable to reach an enemy tile (`reports/2026-10-07-ai-mover-contact.md`) |

## Retrieving a file

The repository is public, but an authenticated `gh` is still the simplest way in:

```
gh release download run-1-rome --repo diegoami/imp_conquest_fixtures \
    --pattern "1_rome_270_winter_7.sav" --dir .

gh release list --repo diegoami/imp_conquest_fixtures
gh release view legacy-probes --repo diegoami/imp_conquest_fixtures
```

## Keeping this file true

A new play-through means a **new release**, named `run-<n>-<nation>`, and a new row here. Three rules make the index worth trusting:

- **A recording goes up when a note maps it to a save pair *or* a report cites it.** Checking only one of the two is how three of the most-cited recordings in the corpus were nearly left out. A genuinely unattributed video can wait — but establish that it *is* unattributed by checking both.
- **A recording without notes is still readable.** [`/parse-recording`](https://github.com/diegoami/imperial_conquest_2/blob/main/docs/recording-analysis.md) takes a recording, the saves either side and **rough timestamps**, and extracts the frames itself. Written session notes are no longer a precondition for using a recording — the melee-cap report was produced from the pointer *"around 1:48, a few interactions"*.
- **Observation notes ship with their run, when they exist.** A save series without notes shows what the engine did but not what was asked of it, and the difference has mattered repeatedly — but a recording plus timestamps now recovers most of it, so the absence of notes is no longer a reason to hold evidence back.
- **Nothing here is copied into a repository.** This file points; it never holds.
