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
