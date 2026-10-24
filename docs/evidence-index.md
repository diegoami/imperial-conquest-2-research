# Evidence index

Every save, screenshot and recording the reports cite, and the release that holds it.

Research #63 adds a [scalar original-x86 receipt](data/research63-quality-controls-v1.json)
and [report](reports/2026-10-23-live-unit-quality-four.md), with no new SAV, screenshot
or release. Its controls use synthetic memory and the pinned private EXE/DAT; they
are not native Windows play evidence. Reproduction is in the report.

The reports cite **bare filenames** — `11_supply.sav`, `1_rome_270_winter_7.sav` — never paths, because the binaries have never been in a repository and never will be. This file is what turns such a citation into something retrievable.

The originals live in the repository [`diegoami/imp_conquest_fixtures`](https://github.com/diegoami/imp_conquest_fixtures), organised as **one release per play-through**. Nothing here is committed to this repository or to the build repository: the game files, saves, screenshots and recordings stay out of both, and this index is a pointer, not a copy.

## The releases

The conversion experiment below is on Drive rather than in a release; its original
game observations are Wine-only. It adds no native Windows acceptance result.

The releases `run-exp-*` are in `diegoami/ic2-conquest`, not in the fixtures repository: each holds one bot experiment's saves and screenshots, which are Wine-only evidence (retrieve with `gh release download <tag> --repo diegoami/ic2-conquest`).

A few small probe saves are committed in the fixtures repository itself rather than in a release: `saves/new-game-probes/` (three new-game autosaves, 2026-09-29) and `saves/fortification-probe/` (a planted-order pair, 2026-09-29). Their rows in the table below link to the files in the repository.

| Release | What it is | Saves | Screenshots | Recordings |
|---|---|---|---|---|
| [`run-exp-manual-gaps`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-manual-gaps) | Bot experiment (2026-10-22, **Wine-only**, seed build; staged saves + natural play): disband/scuttle refunds, foreign supply purchase, Winter storm spike, AI war on a human, manual screenshots; [report](reports/2026-10-22-manual-gaps-disband-purchase-storm-ai-war.md) | 46 | 39 | 0 |
| [`run-exp-fleet-bill`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleet-bill) | Bot experiment (2026-10-22, **Wine-only**): fleet under construction not billed, paired quarter from `M133_session1_AUTO0725.SAV`; [manual consolidation item 12](reports/2026-10-22-manual133-contradictions-consolidated.md) | 2 | 0 | 0 |
| [`run-exp-sav-rebellion107`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-sav-rebellion107) | Bot experiment (2026-10-22, **Wine-only**): SAV atlas increment 11, loyalty-only craft, revival and return (2 run saves + 2 inputs); [atlas](reports/2026-10-21-original-sav-semantic-atlas.md) | 4 | 0 | 0 |
| [`run-exp-sav-aboard107`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-sav-aboard107) | Bot experiment (2026-10-22, **Wine-only**): natural embark, army aboard links (atlas increments 9–10); [atlas](reports/2026-10-21-original-sav-semantic-atlas.md) | 2 | 0 | 0 |
| [`run-exp-sav-fleetmoves107`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-sav-fleetmoves107) | Bot experiment (2026-10-22, **Wine-only**): leftover fleet moves of a reused index (atlas increment 6; 5 run saves + 2 inputs); [atlas](reports/2026-10-21-original-sav-semantic-atlas.md) | 7 | 0 | 0 |
| [`run-exp-sav-inert107`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-sav-inert107) | Bot experiment (2026-10-21, **Wine-only**): UNKNOWN31 INERT write probes (atlas increments 1–4; 10 run saves + 2 inputs); [atlas](reports/2026-10-21-original-sav-semantic-atlas.md) | 12 | 0 | 0 |
| [`run-exp-resupply33`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-resupply33) | Hostile-control recruitment ledger: 3 fresh staged Wine endpoint replays; reviewed source packet merged in PR96 | 9 | 0 | 0 |
| [`run-exp-resupply31`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-resupply31) | Foreign-city automatic support, original code/x86 + 56 staged Wine cases; 227 complete saves, interrupted/empty copy excluded | 227 | 0 | 0 |
| [`run-exp-tactical25-trace`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-tactical25-trace) | Fresh mix-rg_s1 original/Wine decision trace, all 325 legacy draws/all 15 saves matched in both runs; also four EXEs and three buffers | 33 | 0 | 0 |
| [`run-exp-ai-oct16`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-ai-oct16) | Original strategic AI regions/resupply and tactical Computer General; code/x86 + staged Wine, turn 0734/0743; five EXEs also released, never copied here | 252 | 0 | 0 |
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
| [`run-exp-g4-followups`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-g4-followups) | Bot experiment (2026-10-12, **Wine-only**, repo `diegoami/ic2-conquest`): twelve follow-up cases from issue #83 (file-menu save flag, deposition conditions, trade-radio refusal, mercenary hire in play, mobilising, rebellion with two war armies, AI quarter income, Greece's -8 relation gate, unhalved storm rolls, trade and alliance offers, weather-painted rough tiles, real X-button click) | 484 | 201 | 0 |

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
| [`merc_desertion_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/merc_desertion_PRE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`merc_desertion_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/merc_desertion_BEFORE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`merc_desertion_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/merc_desertion_AFTER.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`merc_desertion_single_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/merc_desertion_single_PRE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`merc_desertion_single_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/merc_desertion_single_BEFORE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`merc_desertion_single_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/merc_desertion_single_AFTER.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`elimination_numidia_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/elimination_numidia_PRE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`elimination_numidia_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/elimination_numidia_BEFORE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`elimination_numidia_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/elimination_numidia_AFTER.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`elimination_end_turn_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/elimination_end_turn_PRE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`elimination_end_turn_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/elimination_end_turn_BEFORE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`elimination_end_turn_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/elimination_end_turn_AFTER.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`ai_battle_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/ai_battle_PRE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`ai_battle_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/ai_battle_BEFORE.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`ai_battle_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-turn-end-army-removal/ai_battle_AFTER.SAV) | `run-exp-turn-end-army-removal` (repo `ic2-conquest`) | 1 |
| [`fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/blob/feat/fleet-orders/saves/fleet-port-antium-0734.SAV) | repo `ic2-conquest` `saves/` | 3 |
| [`fleet-split-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/blob/feat/fleet-orders/saves/fleet-split-antium-0734.SAV) | repo `ic2-conquest` `saves/` | 2 |
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
| [`FIX_T4_R85sA.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_R85sA.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 2 |
| [`FIX_T4_R85w.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/FIX_T4_R85w.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed2_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed2_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed3_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed3_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed4_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed4_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`PROBE_seed5_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/PROBE_seed5_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_H45s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_H45s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_H85s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_H85s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed10_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed10_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_K45s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 2 |
| [`ST_K45s_seed2_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_K45s_seed2_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 2 |
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
| [`ST_R45s_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 2 |
| [`ST_R45s_seed2_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed2_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`ST_R45s_seed3_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R45s_seed3_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 2 |
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
| [`ST_R85sA_seed1_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/ST_R85sA_seed1_AUTO0721.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 2 |
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
| [`NAT_seed1_11_0726_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_11_0726_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 2 |
| [`NAT_seed1_12_0726_seat13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_12_0726_seat13.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 1 |
| [`NAT_seed1_13_0727_seat02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-storms/NAT_seed1_13_0727_seat02.SAV) | `run-exp-storms` (repo `ic2-conquest`) | 2 |
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
| [`B2_after_end_turn_1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_after_end_turn_1.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 3 |
| [`B2_after_end_turn_2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_after_end_turn_2.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 3 |
| [`B2_nat_p1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_nat_p1.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`B2_nat_p2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_nat_p2.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`B2_placement.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/B2_placement.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 3 |
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
| [`b3_c5_stale_grid_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c5_stale_grid_BATTLE01.SAV) … `b3_c5_stale_grid_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 3 |
| [`b3_c5_stale_grid_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c5_stale_grid_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c6_same_cell_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c6_same_cell_BATTLE01.SAV) … `b3_c6_same_cell_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 3 |
| [`b3_c6_same_cell_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c6_same_cell_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c7_type_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c7_type_BATTLE01.SAV) … `b3_c7_type_BATTLE16.SAV` (16 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_c7_type_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_c7_type_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d0_control_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d0_control_BATTLE01.SAV) … `b3_d0_control_BATTLE13.SAV` (13 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d0_control_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d0_control_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d3_adjacent_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d3_adjacent_BATTLE01.SAV) … `b3_d3_adjacent_BATTLE11.SAV` (11 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d3_adjacent_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d3_adjacent_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d5_stale_grid_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d5_stale_grid_BATTLE01.SAV) … `b3_d5_stale_grid_BATTLE13.SAV` (13 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 3 |
| [`b3_d5_stale_grid_post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d5_stale_grid_post.SAV) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 2 |
| [`b3_d6_same_cell_BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b3_d6_same_cell_BATTLE01.SAV) … `b3_d6_same_cell_BATTLE11.SAV` (11 files, the same series, one file per half-round or trial) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 3 |
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
| [`sieges_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_PRE.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`sieges_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_BEFORE.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`sieges_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_AFTER.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`sieges_cover1_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_cover1_PRE.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`sieges_cover1_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_cover1_BEFORE.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`sieges_cover1_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_cover1_AFTER.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`sieges_end_turn_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_end_turn_PRE.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`sieges_end_turn_BEFORE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_end_turn_BEFORE.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`sieges_end_turn_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-elimination-army-aboard/sieges_end_turn_AFTER.SAV) | `run-exp-elimination-army-aboard` (repo `ic2-conquest`) | 1 |
| [`colours_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-owner-colours/colours_PRE.SAV) | `run-exp-owner-colours` (repo `ic2-conquest`) | 1 |
| [`colours_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-owner-colours/colours_AFTER.SAV) | `run-exp-owner-colours` (repo `ic2-conquest`) | 1 |
| [`colours_screen.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-owner-colours/colours_screen.png) | `run-exp-owner-colours` (repo `ic2-conquest`) | 1 |
| [`montage_army.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-owner-colours/montage_army.png) | `run-exp-owner-colours` (repo `ic2-conquest`) | 1 |
| [`montage_fleet.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-owner-colours/montage_fleet.png) | `run-exp-owner-colours` (repo `ic2-conquest`) | 1 |
| [`montage_both.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-owner-colours/montage_both.png) | `run-exp-owner-colours` (repo `ic2-conquest`) | 1 |
| [`cities_PRE.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-city-marker-colours/cities_PRE.SAV) | `run-exp-city-marker-colours` (repo `ic2-conquest`) | 1 |
| [`cities_AFTER.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-city-marker-colours/cities_AFTER.SAV) | `run-exp-city-marker-colours` (repo `ic2-conquest`) | 1 |
| [`cities_screen1.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-city-marker-colours/cities_screen1.png) | `run-exp-city-marker-colours` (repo `ic2-conquest`) | 1 |
| [`cities_screen2.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-city-marker-colours/cities_screen2.png) | `run-exp-city-marker-colours` (repo `ic2-conquest`) | 1 |
| [`montage_cities.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-city-marker-colours/montage_cities.png) | `run-exp-city-marker-colours` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_ArmiesList.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_ArmiesList.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_ArmiesList_mask.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_ArmiesList_mask.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_CapitalsList.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_CapitalsList.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_CapitalsList_mask.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_CapitalsList_mask.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_Cities1List.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_Cities1List.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_Cities1List_mask.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_Cities1List_mask.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_Cities2List.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_Cities2List.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_Cities2List_mask.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_Cities2List_mask.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_Cities3List.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_Cities3List.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_Cities3List_mask.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_Cities3List_mask.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_Cities4List.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_Cities4List.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_Cities4List_mask.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_Cities4List_mask.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_FleetsList.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_FleetsList.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_FleetsList_mask.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_FleetsList_mask.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_TerrainList.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_TerrainList.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TUnitMap_TerrainList_mask.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TUnitMap_TerrainList_mask.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Armenia.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Armenia.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Bithynia.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Bithynia.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Carthage.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Carthage.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Celtiberia.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Celtiberia.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Dacia.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Dacia.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Galatia.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Galatia.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Gaul.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Gaul.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Greece.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Greece.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Illyria.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Illyria.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Macedonia.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Macedonia.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Media.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Media.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Numidia.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Numidia.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Ptolemaic.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Ptolemaic.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Rome.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Rome.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Seleucid.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Seleucid.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`glyph_sb_Thracia.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/glyph_sb_Thracia.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`IW_seed14_039_0759.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-conquest-aboard/IW_seed14_039_0759.SAV) | `run-exp-ai-conquest-aboard` (repo `ic2-conquest`) | 1 |
| [`IW_seed15_034_0754.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-conquest-aboard/IW_seed15_034_0754.SAV) | `run-exp-ai-conquest-aboard` (repo `ic2-conquest`) | 1 |
| [`IW_seed17_036_0756.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-conquest-aboard/IW_seed17_036_0756.SAV) | `run-exp-ai-conquest-aboard` (repo `ic2-conquest`) | 1 |
| [`b2_placement_window.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b2_placement_window.png) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 1 |
| [`b2_after_end_turn_1_window.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b2_after_end_turn_1_window.png) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 1 |
| [`b2_after_end_turn_2_window.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-sweep/b2_after_end_turn_2_window.png) | `run-exp-battle-sweep` (repo `ic2-conquest`) | 1 |
| [`TBattleMap_BatMapList.bmp`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TBattleMap_BatMapList.bmp) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`TBattleMap_BatMapList.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-unit-icon-resources/TBattleMap_BatMapList.png) | `run-exp-unit-icon-resources` (repo `ic2-conquest`) | 1 |
| [`20261009-141127_NUM_start.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-numidia-colour/20261009-141127_NUM_start.SAV) | `run-exp-battle-numidia-colour` (repo `ic2-conquest`) | 1 |
| [`20261009-141127_NUM_placement.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-numidia-colour/20261009-141127_NUM_placement.SAV) | `run-exp-battle-numidia-colour` (repo `ic2-conquest`) | 1 |
| [`20261009-141127_NUM_after_end_turn_1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-numidia-colour/20261009-141127_NUM_after_end_turn_1.SAV) | `run-exp-battle-numidia-colour` (repo `ic2-conquest`) | 1 |
| [`20261009-141127_NUM_placement_window.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-numidia-colour/20261009-141127_NUM_placement_window.png) | `run-exp-battle-numidia-colour` (repo `ic2-conquest`) | 1 |
| [`20261009-141127_NUM_after_end_turn_1_window.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-numidia-colour/20261009-141127_NUM_after_end_turn_1_window.png) | `run-exp-battle-numidia-colour` (repo `ic2-conquest`) | 1 |
| [`run-exp-ai-intercept-hunt-saves.tar.gz`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-intercept-hunt/run-exp-ai-intercept-hunt-saves.tar.gz) (213 saves, incl. `hook_s2_AUTO0751.SAV`, `hook_s2_AUTO0755.SAV`, `hook_s14_AUTO0758.SAV`, `staged_hunt_s1_AUTO0724.SAV`) | `run-exp-ai-intercept-hunt` (repo `ic2-conquest`) | 1 |
| [`run-exp-gap-v050-saves.tar.gz`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-gap-v050/run-exp-gap-v050-saves.tar.gz) (1,342 remake v0.5.0 JSON saves; all match `SAVES.sha256` since ic2-conquest `e823910`) | `run-exp-gap-v050` (repo `ic2-conquest`) | 1 |
| [`A_20261009-175015_A_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-radio/A_20261009-175015_A_before.SAV) | `run-exp-peace-radio` (repo `ic2-conquest`) | 1 |
| [`A_20261009-175015_A_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-radio/A_20261009-175015_A_after.SAV) | `run-exp-peace-radio` (repo `ic2-conquest`) | 1 |
| [`A_20261009-175015_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-radio/A_20261009-175015_AUTO0721.SAV) | `run-exp-peace-radio` (repo `ic2-conquest`) | 1 |
| [`B_20261009-175604_B_after_cancel.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-radio/B_20261009-175604_B_after_cancel.SAV) | `run-exp-peace-radio` (repo `ic2-conquest`) | 1 |
| [`D_20261009-175644_start_rome_illyria_allied.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-radio/D_20261009-175644_start_rome_illyria_allied.SAV) | `run-exp-peace-radio` (repo `ic2-conquest`) | 1 |
| [`D_20261009-175644_D_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-radio/D_20261009-175644_D_after.SAV) | `run-exp-peace-radio` (repo `ic2-conquest`) | 1 |
| [`D_20261009-175644_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-peace-radio/D_20261009-175644_AUTO0721.SAV) | `run-exp-peace-radio` (repo `ic2-conquest`) | 1 |
| [`20261009-183238_FB_after_1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-build-city/20261009-183238_FB_after_1.SAV) | `run-exp-fleet-build-city` (repo `ic2-conquest`) | 1 |
| [`20261009-183238_FB_end.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-build-city/20261009-183238_FB_end.SAV) | `run-exp-fleet-build-city` (repo `ic2-conquest`) | 1 |
| [`P5_20261009-193415_split.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-supply-transfer-clamps/P5_20261009-193415_split.SAV) | `run-exp-supply-transfer-clamps` (repo `ic2-conquest`) | 1 |
| [`Ta2_20261009-194517_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-supply-transfer-clamps/Ta2_20261009-194517_after.SAV) | `run-exp-supply-transfer-clamps` (repo `ic2-conquest`) | 1 |
| [`Ta4_20261009-194605_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-supply-transfer-clamps/Ta4_20261009-194605_before.SAV) | `run-exp-supply-transfer-clamps` (repo `ic2-conquest`) | 1 |
| [`Ta4_20261009-194605_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-supply-transfer-clamps/Ta4_20261009-194605_after.SAV) | `run-exp-supply-transfer-clamps` (repo `ic2-conquest`) | 1 |
| [`U1_20261009-194123_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-supply-transfer-clamps/U1_20261009-194123_after.SAV) | `run-exp-supply-transfer-clamps` (repo `ic2-conquest`) | 1 |
| [`U3_20261009-194306_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-supply-transfer-clamps/U3_20261009-194306_after.SAV) | `run-exp-supply-transfer-clamps` (repo `ic2-conquest`) | 1 |
| [`U3b_20261009-194355_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-supply-transfer-clamps/U3b_20261009-194355_after.SAV) | `run-exp-supply-transfer-clamps` (repo `ic2-conquest`) | 1 |
| [`Td0_20261010-213628_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-empty-transfer/Td0_20261010-213628_before.SAV) | `run-exp-fleet-empty-transfer` (repo `ic2-conquest`) | 1 |
| [`Td0_20261010-213628_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-empty-transfer/Td0_20261010-213628_after.SAV) | `run-exp-fleet-empty-transfer` (repo `ic2-conquest`) | 1 |
| [`Td1_20261010-213503_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-empty-transfer/Td1_20261010-213503_before.SAV) | `run-exp-fleet-empty-transfer` (repo `ic2-conquest`) | 1 |
| [`Td1_20261010-213503_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-empty-transfer/Td1_20261010-213503_after.SAV) | `run-exp-fleet-empty-transfer` (repo `ic2-conquest`) | 1 |
| [`Td2_20261010-213548_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-empty-transfer/Td2_20261010-213548_before.SAV) | `run-exp-fleet-empty-transfer` (repo `ic2-conquest`) | 1 |
| [`Td2_20261010-213548_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-empty-transfer/Td2_20261010-213548_after.SAV) | `run-exp-fleet-empty-transfer` (repo `ic2-conquest`) | 1 |
| [`Td1_20261010-213503_dialog_before_ok.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-fleet-empty-transfer/Td1_20261010-213503_dialog_before_ok.png) | `run-exp-fleet-empty-transfer` (repo `ic2-conquest`) | 1 |
| [`C3_20261011-185659_zero_moves_loaded.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C3_20261011-185659_zero_moves_loaded.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C3_20261011-185659_zero_moves_end.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C3_20261011-185659_zero_moves_end.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C3_20261011-185659_control_moves8_loaded.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C3_20261011-185659_control_moves8_loaded.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C3_20261011-185659_control_moves8_end.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C3_20261011-185659_control_moves8_end.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C3_20261011-185659_staged_army12_moves8_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C3_20261011-185659_staged_army12_moves8_fleet-port-antium-0734.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C3_20261011-185659_info_panel_78461.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C3_20261011-185659_info_panel_78461.png) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4_20261011-185907_far12_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4_20261011-185907_far12_before.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4_20261011-185907_far12_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4_20261011-185907_far12_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4_20261011-185907_near5_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4_20261011-185907_near5_before.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4_20261011-185907_near5_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4_20261011-185907_near5_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4b_20261011-190051_steps_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4b_20261011-190051_steps_before.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4b_20261011-190051_steps_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4b_20261011-190051_steps_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4b_20261011-190051_staged_army0_moves11_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4b_20261011-190051_staged_army0_moves11_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4b_20261011-190051_river_with_1_move_left_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4b_20261011-190051_river_with_1_move_left_before.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C4b_20261011-190051_river_with_1_move_left_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C4b_20261011-190051_river_with_1_move_left_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5a_20261011-190227_join3_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5a_20261011-190227_join3_before.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5a_20261011-190227_join3_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5a_20261011-190227_join3_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5a_20261011-190227_join4_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5a_20261011-190227_join4_before.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5a_20261011-190227_join4_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5a_20261011-190227_join4_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5a_20261011-190227_join2_control_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5a_20261011-190227_join2_control_before.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5a_20261011-190227_join2_control_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5a_20261011-190227_join2_control_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5b_20261011-190426_before.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5b_20261011-190426_before.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5b_20261011-190426_after_two.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5b_20261011-190426_after_two.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5b_20261011-190426_after_one.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5b_20261011-190426_after_one.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5b_20261011-190426_two_selected.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5b_20261011-190426_two_selected.png) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_ar100_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_ar100_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_ar1399_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_ar1399_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_ar1400_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_ar1400_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_hc1000_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_hc1000_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_hc100_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_hc100_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_hc999_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_hc999_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_hi100_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_hi100_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_hi2399_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_hi2399_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_hi2400_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_hi2400_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_hi5000_ext_A_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_hi5000_ext_A_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_hi5000_ext_B_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_hi5000_ext_B_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_lc100_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_lc100_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_lc2799_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_lc2799_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_lc2800_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_lc2800_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_li100_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_li100_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_li4800_probe_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_li4800_probe_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_li5999_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_li5999_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-191316_li6000_default_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-191316_li6000_default_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-195827_hi5000_probe_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-195827_hi5000_probe_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-195827_hi5000_ext_A_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-195827_hi5000_ext_A_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`C5c_20261011-195827_hi5000_ext_B_after.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g2-original-checks/C5c_20261011-195827_hi5000_ext_B_after.SAV) | `run-exp-g2-original-checks` (repo `ic2-conquest`) | 1 |
| [`G10_20261011-235901_recovered_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G10_20261011-235901_recovered_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G10_20261011-235901_recovered_AUTO0722.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G10_20261011-235901_recovered_AUTO0722.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G10_20261011-235901_recovered_AUTO0723.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G10_20261011-235901_recovered_AUTO0723.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G10_20261011-235901_recovered_AUTO0724.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G10_20261011-235901_recovered_AUTO0724.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G10_20261011-235901_recovered_AUTO0725.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G10_20261011-235901_recovered_AUTO0725.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G10_20261011-235901_recovered_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G10_20261011-235901_recovered_AUTO0726.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth10000000_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth10000000_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth12000000_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth12000000_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth2400000_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth2400000_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth2499999_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth2499999_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth2500500_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth2500500_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth2577000_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth2577000_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth3000000_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth3000000_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth6000000_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth6000000_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_debt_20261011-232502_staged_wealth9999999_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_debt_20261011-232502_staged_wealth9999999_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_20261011-234640_staged_mid_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_20261011-234640_staged_mid_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_20261011-234713_staged_below_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_20261011-234713_staged_below_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_20261011-234745_staged_above_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_20261011-234745_staged_above_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_20261011-234836_staged_mid_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_20261011-234836_staged_mid_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_20261011-234911_staged_below_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_20261011-234911_staged_below_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_20261011-234946_staged_above_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_20261011-234946_staged_above_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002323_staged_control5200_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002323_staged_control5200_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002407_autosave_721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002407_autosave_721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002407_staged_control5200_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002407_staged_control5200_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002407_staged_test5100_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002407_staged_test5100_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002523_autosave01_control_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002523_autosave01_control_t721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002523_autosave02_test_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002523_autosave02_test_t721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002523_staged_control5200_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002523_staged_control5200_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002523_staged_test5100_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002523_staged_test5100_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002629_autosave01_test_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002629_autosave01_test_t721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002629_autosave02_control_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002629_autosave02_control_t721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002629_staged_control5200_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002629_staged_control5200_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002629_staged_test5100_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002629_staged_test5100_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002727_autosave01_control_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002727_autosave01_control_t721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002727_autosave02_test_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002727_autosave02_test_t721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002727_staged_control5200_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002727_staged_control5200_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002727_staged_test4990_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002727_staged_test4990_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002825_autosave01_test_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002825_autosave01_test_t721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002825_autosave02_control_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002825_autosave02_control_t721_AUTO0721.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002825_staged_control5200_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002825_staged_control5200_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_pair_20261012-002825_staged_test4990_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_pair_20261012-002825_staged_test4990_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_fleet_20261011-232354_under_construction.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_fleet_20261011-232354_under_construction.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-231938_control_loaded.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-231938_control_loaded.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-231938_staged_merc_hc2400_q9_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-231938_staged_merc_hc2400_q9_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-231938_staged_merc_li3000_q6_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-231938_staged_merc_li3000_q6_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-232104_control_loaded.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-232104_control_loaded.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-232104_staged_merc_li3000_q6_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-232104_staged_merc_li3000_q6_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-232204_control_loaded.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-232204_control_loaded.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-232204_staged_merc_hc2400_q9_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-232204_staged_merc_hc2400_q9_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-232259_control_loaded.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-232259_control_loaded.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-232259_staged_merc_hi4000_q8_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-232259_staged_merc_hi4000_q8_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261012-065006_control_loaded.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261012-065006_control_loaded.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261012-065006_staged_merc_hc2400_q9_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261012-065006_staged_merc_hc2400_q9_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G3_cap_20261011-233117_after_control.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G3_cap_20261011-233117_after_control.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G3_cap_20261011-233212_staged_own2_control_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G3_cap_20261011-233212_staged_own2_control_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G3_cap_20261011-233212_staged_own3_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G3_cap_20261011-233212_staged_own3_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261011-233302_X_after_save.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261011-233302_X_after_save.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261011-233302_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261011-233302_X_original_before_anything.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261011-233412_X_after_save.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261011-233412_X_after_save.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261011-233412_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261011-233412_X_original_before_anything.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-065259_X_after_save.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-065259_X_after_save.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-065259_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-065259_X_original_before_anything.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-065348_X_after_save.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-065348_X_after_save.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-065348_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-065348_X_original_before_anything.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-065502_X_after_save.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-065502_X_after_save.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-065502_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-065502_X_original_before_anything.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-065502_recovered_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-065502_recovered_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-071546_X_after_save.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-071546_X_after_save.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-071546_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-071546_X_original_before_anything.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261012-071546_autosave01_newgame_t720_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261012-071546_autosave01_newgame_t720_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235055_seed12345_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235055_seed12345_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235123_seed1_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235123_seed1_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235146_seed2_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235146_seed2_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235209_seed3_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235209_seed3_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235231_seed4_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235231_seed4_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235254_seed5_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235254_seed5_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235317_seed6_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235317_seed6_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235340_seed7_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235340_seed7_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235403_seed8_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235403_seed8_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235426_seed9_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235426_seed9_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G7_20261011-235448_seed10_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G7_20261011-235448_seed10_AUTO0720.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G8_20261012-000014_after_luceria_recruit.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G8_20261012-000014_after_luceria_recruit.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G8_20261012-000108_staged_low_both_G8_20261012-000014_after_luceria_recruit.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G8_20261012-000108_staged_low_both_G8_20261012-000014_after_luceria_recruit.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G9_20261012-000239_staged_padded198_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G9_20261012-000239_staged_padded198_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G10_20261011-235901_round1.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G10_20261011-235901_round1.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_depose_20261011-234713_below_after_end_turn.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_depose_20261011-234713_below_after_end_turn.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_fleet_20261011-232354_balance_fleet_under_construction.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_fleet_20261011-232354_balance_fleet_under_construction.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_fleet_20261011-232354_balance_port_save_finished_fleets.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_fleet_20261011-232354_balance_port_save_finished_fleets.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-231938_balance_control_no_merc.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-231938_balance_control_no_merc.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261011-232104_balance_merc_li3000_q6.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261011-232104_balance_merc_li3000_q6.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261012-065006_balance_control_no_merc.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261012-065006_balance_control_no_merc.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G2_merc_20261012-065006_balance_merc_hc2400_q9.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G2_merc_20261012-065006_balance_merc_hc2400_q9.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G3_cap_20261011-233117_box_542996.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G3_cap_20261011-233117_box_542996.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G3_cap_20261011-233212_box_543546.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G3_cap_20261011-233212_box_543546.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261011-233302_after_save_after_new.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261011-233302_after_save_after_new.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G5_20261011-233302_save_as_default_name.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G5_20261011-233302_save_as_default_name.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G6_20261011-233555_box_545767.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G6_20261011-233555_box_545767.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G8_20261012-000014_natural_dialog.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G8_20261012-000014_natural_dialog.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G8_20261012-000108_box_560938.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G8_20261012-000108_box_560938.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`G9_20261012-000239_box_561853.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g1-original-checks/G9_20261012-000239_box_561853.png) | `run-exp-g1-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_autosave01_q1ab_ctl_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_autosave01_q1ab_ctl_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_autosave02_q1ab_capua_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_autosave02_q1ab_capua_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_autosave03_q1ab_venusia_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_autosave03_q1ab_venusia_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_autosave04_q1ab_pisae_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_autosave04_q1ab_pisae_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_autosave05_q1ab_heraclea_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_autosave05_q1ab_heraclea_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_q1ab_capua_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_q1ab_capua_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_q1ab_ctl_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_q1ab_ctl_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_q1ab_heraclea_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_q1ab_heraclea_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_q1ab_pisae_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_q1ab_pisae_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_q1ab_venusia_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_q1ab_venusia_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_staged_q1ab_capua_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_staged_q1ab_capua_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_staged_q1ab_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_staged_q1ab_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_staged_q1ab_heraclea_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_staged_q1ab_heraclea_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_staged_q1ab_pisae_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_staged_q1ab_pisae_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074558_staged_q1ab_venusia_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074558_staged_q1ab_venusia_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_autosave01_q1ab_ariminum_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_autosave01_q1ab_ariminum_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_autosave02_q1ab_arretium_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_autosave02_q1ab_arretium_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_autosave03_q1ab_pisae_gaul_dead_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_autosave03_q1ab_pisae_gaul_dead_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_q1ab_ariminum_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_q1ab_ariminum_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_q1ab_arretium_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_q1ab_arretium_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_q1ab_pisae_gaul_dead_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_q1ab_pisae_gaul_dead_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_staged_q1ab_ariminum_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_staged_q1ab_ariminum_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_staged_q1ab_arretium_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_staged_q1ab_arretium_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1ab_20261012-074808_staged_q1ab_pisae_gaul_dead_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1ab_20261012-074808_staged_q1ab_pisae_gaul_dead_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_20261012-074922_autosave01_q1c_nine_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_20261012-074922_autosave01_q1c_nine_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_20261012-074922_autosave02_q1c_seven_control_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_20261012-074922_autosave02_q1c_seven_control_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_20261012-074922_q1c_nine_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_20261012-074922_q1c_nine_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_20261012-074922_q1c_seven_control_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_20261012-074922_q1c_seven_control_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_20261012-074922_staged_q1c_nine_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_20261012-074922_staged_q1c_nine_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_20261012-074922_staged_q1c_seven_control_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_20261012-074922_staged_q1c_seven_control_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_autosave01_q1d_one_purse100_control_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_autosave01_q1d_one_purse100_control_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_autosave02_q1d_one_purse0_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_autosave02_q1d_one_purse0_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_autosave03_q1d_two_purse100_control_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_autosave03_q1d_two_purse100_control_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_autosave04_q1d_two_purse0_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_autosave04_q1d_two_purse0_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_q1d_one_purse0_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_q1d_one_purse0_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_q1d_one_purse100_control_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_q1d_one_purse100_control_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_q1d_two_purse0_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_q1d_two_purse0_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_q1d_two_purse100_control_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_q1d_two_purse100_control_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_staged_q1d_one_purse0_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_staged_q1d_one_purse0_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_staged_q1d_one_purse100_control_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_staged_q1d_one_purse100_control_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_staged_q1d_two_purse0_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_staged_q1d_two_purse0_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1d_20261012-075010_staged_q1d_two_purse100_control_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1d_20261012-075010_staged_q1d_two_purse100_control_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1e_20261012-075216_autosave01_q1e_winter_t739_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1e_20261012-075216_autosave01_q1e_winter_t739_AUTO0739.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1e_20261012-075216_autosave04_q1e_winter_t742_AUTO0742.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1e_20261012-075216_autosave04_q1e_winter_t742_AUTO0742.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1e_20261012-075216_q1e_winter_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1e_20261012-075216_q1e_winter_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1e_20261012-075216_staged_q1e_winter_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1e_20261012-075216_staged_q1e_winter_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q3_20261012-075346_start.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q3_20261012-075346_start.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q3_20261012-075346_news_tool.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q3_20261012-075346_news_tool.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q3_20261012-075346_information_window.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q3_20261012-075346_information_window.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1f_20261012-075413_staged_q1f_debt50000_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1f_20261012-075413_staged_q1f_debt50000_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1f_20261012-075413_autosave01_q1f_r01_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1f_20261012-075413_autosave01_q1f_r01_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q2_20261012-075845_autosave01_round1_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q2_20261012-075845_autosave01_round1_t721_AUTO0721.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q2_20261012-075845_autosave06_round6_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q2_20261012-075845_autosave06_round6_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-080017_staged_q5_move_rough_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-080017_staged_q5_move_rough_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-080017_rough_info.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-080017_rough_info.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-080017_staged_q5_move_calm_control_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-080017_staged_q5_move_calm_control_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-080017_calm_control_info.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-080017_calm_control_info.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-080017_staged_q5_move_rough_again_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-080017_staged_q5_move_rough_again_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-080017_rough_again_info.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-080017_rough_again_info.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q2b_20261012-080344_staged_q2b_week11_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q2b_20261012-080344_staged_q2b_week11_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q2b_20261012-080344_autosave01_q2b_1_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q2b_20261012-080344_autosave01_q2b_1_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q2b_20261012-080344_autosave02_q2b_2_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q2b_20261012-080344_autosave02_q2b_2_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q2b_20261012-080344_autosave03_q2b_3_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q2b_20261012-080344_autosave03_q2b_3_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1f_20261012-080534_staged_q1f_debt50000_unity_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1f_20261012-080534_staged_q1f_debt50000_unity_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1f_20261012-080534_autosave03_q1f_r03_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1f_20261012-080534_autosave03_q1f_r03_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_staged_q1c_nine_dead_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_staged_q1c_nine_dead_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_q1c_nine_dead_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_q1c_nine_dead_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_autosave01_q1c_nine_dead_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_autosave01_q1c_nine_dead_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_staged_q1c_seven_dead_control_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_staged_q1c_seven_dead_control_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_q1c_seven_dead_control_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_q1c_seven_dead_control_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_autosave02_q1c_seven_dead_control_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_autosave02_q1c_seven_dead_control_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_staged_q1c_nine_dead_again_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_staged_q1c_nine_dead_again_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_q1c_nine_dead_again_opened.png`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_q1c_nine_dead_again_opened.png) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q1c_dead_20261012-081033_autosave03_q1c_nine_dead_again_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q1c_dead_20261012-081033_autosave03_q1c_nine_dead_again_t726_AUTO0726.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-081320_staged_q5_storm_rough_c80_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-081320_staged_q5_storm_rough_c80_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-081320_staged_q5_storm_calm_c80_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-081320_staged_q5_storm_calm_c80_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-081320_autosave01_q5_storm_rough_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-081320_autosave01_q5_storm_rough_01_t735_AUTO0735.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-081320_autosave02_q5_storm_calm_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-081320_autosave02_q5_storm_calm_01_t735_AUTO0735.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q6_20261012-082004_staged_q6_peace_only_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q6_20261012-082004_staged_q6_peace_only_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q6_20261012-082004_autosave01_q6_t001_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q6_20261012-082004_autosave01_q6_t001_t721_AUTO0721.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-090225_staged_q5_storm_rough_c60_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-090225_staged_q5_storm_rough_c60_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-090225_staged_q5_storm_calm_c60_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-090225_staged_q5_storm_calm_c60_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-091054_staged_q5_storm_rough_c60_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-091054_staged_q5_storm_rough_c60_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-091054_staged_q5_storm_calm_c60_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-091054_staged_q5_storm_calm_c60_fleet-port-antium-0734.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-091054_autosave01_q5_storm_rough_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-091054_autosave01_q5_storm_rough_01_t735_AUTO0735.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`Q5_20261012-091054_autosave02_q5_storm_calm_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g3-original-checks/Q5_20261012-091054_autosave02_q5_storm_calm_01_t735_AUTO0735.SAV) | `run-exp-g3-original-checks` (repo `ic2-conquest`) | 1 |
| [`run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/blob/main/saves/run0-start-AUTO0720-seed12345.SAV) | repo `ic2-conquest` `saves/` | 3 |
| [`mobilize-new-army-0720.SAV`](https://github.com/diegoami/ic2-conquest/blob/ac958a0fa58984098641a7992a42d0fbf517d473/saves/mobilize-new-army-0720.SAV) | repo `ic2-conquest` `saves/` | 1 |
| [`det-AUTO0721-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/blob/ac958a0fa58984098641a7992a42d0fbf517d473/saves/det-AUTO0721-seed12345.SAV) | repo `ic2-conquest` `saves/` | 1 |

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
| [`A_20261012-104940_after_hire1.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/A_20261012-104940_after_hire1.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`A_20261012-104940_after_hire2.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/A_20261012-104940_after_hire2.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`B_20261012-104629_staged_carthage_full_no_offer_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/B_20261012-104629_staged_carthage_full_no_offer_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`B_20261012-104629_staged_carthage_full_offer_from_carthage_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/B_20261012-104629_staged_carthage_full_offer_from_carthage_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`B_20261012-104629_staged_carthage_full_offer_from_seleucid_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/B_20261012-104629_staged_carthage_full_offer_from_seleucid_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`B_20261012-104629_staged_galatia_ally2_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/B_20261012-104629_staged_galatia_ally2_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`B_20261012-104629_staged_galatia_cooldown_m8_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/B_20261012-104629_staged_galatia_cooldown_m8_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`B_20261012-104629_staged_galatia_peace_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/B_20261012-104629_staged_galatia_peace_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`B_20261012-104629_staged_galatia_war3_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/B_20261012-104629_staged_galatia_war3_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave01_pos_treasury_m5200_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave01_pos_treasury_m5200_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave02_unity399_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave02_unity399_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave03_unity400_ctl_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave03_unity400_ctl_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave04_year250_t1201_AUTO1201.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave04_year250_t1201_AUTO1201.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave05_year251_ctl_t1177_AUTO1177.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave05_year251_ctl_t1177_AUTO1177.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave06_year251_roll_t1200_AUTO1200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave06_year251_roll_t1200_AUTO1200.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave07_year252_roll_ctl_t1176_AUTO1176.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave07_year252_roll_ctl_t1176_AUTO1176.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave08_cities334_word_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave08_cities334_word_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_autosave09_cities333_word_ctl_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_autosave09_cities333_word_ctl_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_cities333_word_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_cities333_word_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_cities334_word_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_cities334_word_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_pos_treasury_m5200_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_pos_treasury_m5200_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_unity399_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_unity399_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_unity400_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_unity400_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_year250_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_year250_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_year251_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_year251_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_year251_roll_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_year251_roll_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_20261012-104019_staged_year252_roll_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_20261012-104019_staged_year252_roll_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-104410_autosave01_pos_unity399_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-104410_autosave01_pos_unity399_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-104410_autosave02_cities333_real_ctl_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-104410_autosave02_cities333_real_ctl_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-104410_autosave03_cities334_real_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-104410_autosave03_cities334_real_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-104410_staged_cities333_real_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-104410_staged_cities333_real_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-104410_staged_cities334_real_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-104410_staged_cities334_real_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-104410_staged_pos_unity399_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-104410_staged_pos_unity399_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-144010_autosave01_pos_unity399_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-144010_autosave01_pos_unity399_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-144010_autosave02_cities333_real_ctl_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-144010_autosave02_cities333_real_ctl_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-144010_autosave03_cities334_real_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-144010_autosave03_cities334_real_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-144010_staged_cities333_real_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-144010_staged_cities333_real_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-144010_staged_cities334_real_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-144010_staged_cities334_real_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`C_real_20261012-144010_staged_pos_unity399_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/C_real_20261012-144010_staged_pos_unity399_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D2_20261012-105329_autosave01_ai_carthage_dist1_state24_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D2_20261012-105329_autosave01_ai_carthage_dist1_state24_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D2_20261012-105329_autosave02_ai_thracia_dist4_state24_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D2_20261012-105329_autosave02_ai_thracia_dist4_state24_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D2_20261012-105329_autosave03_ai_thracia_dist4_state24_allslots_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D2_20261012-105329_autosave03_ai_thracia_dist4_state24_allslots_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D2_20261012-105329_autosave04_ai_thracia_dist4_natural_ctl_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D2_20261012-105329_autosave04_ai_thracia_dist4_natural_ctl_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D2_20261012-105329_staged_ai_carthage_dist1_state24_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D2_20261012-105329_staged_ai_carthage_dist1_state24_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D2_20261012-105329_staged_ai_thracia_dist4_natural_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D2_20261012-105329_staged_ai_thracia_dist4_natural_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D2_20261012-105329_staged_ai_thracia_dist4_state24_allslots_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D2_20261012-105329_staged_ai_thracia_dist4_state24_allslots_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D2_20261012-105329_staged_ai_thracia_dist4_state24_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D2_20261012-105329_staged_ai_thracia_dist4_state24_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D3_20261012-105648_autosave01_human_dist1_turn2_t1_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D3_20261012-105648_autosave01_human_dist1_turn2_t1_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D3_20261012-105648_autosave02_human_dist0_turn2_t1_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D3_20261012-105648_autosave02_human_dist0_turn2_t1_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D3_20261012-105648_autosave03_human_dist2_turn2_t1_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D3_20261012-105648_autosave03_human_dist2_turn2_t1_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D4_20261012-105843_autosave01_d4_thracia_dist4_wars8_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D4_20261012-105843_autosave01_d4_thracia_dist4_wars8_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D4_20261012-105843_autosave02_d4_carthage_dist1_wars8_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D4_20261012-105843_autosave02_d4_carthage_dist1_wars8_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D4_20261012-105843_autosave03_d4_galatia_dist8_wars8_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D4_20261012-105843_autosave03_d4_galatia_dist8_wars8_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D4_20261012-105843_autosave04_d4_thracia_dist4_nowars_ctl_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D4_20261012-105843_autosave04_d4_thracia_dist4_nowars_ctl_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D4_20261012-105843_staged_d4_carthage_dist1_wars8_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D4_20261012-105843_staged_d4_carthage_dist1_wars8_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D4_20261012-105843_staged_d4_galatia_dist8_wars8_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D4_20261012-105843_staged_d4_galatia_dist8_wars8_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D4_20261012-105843_staged_d4_thracia_dist4_nowars_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D4_20261012-105843_staged_d4_thracia_dist4_nowars_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D4_20261012-105843_staged_d4_thracia_dist4_wars8_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D4_20261012-105843_staged_d4_thracia_dist4_wars8_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D5_20261012-110504_autosave01_d5_galatia_4ready_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D5_20261012-110504_autosave01_d5_galatia_4ready_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D5_20261012-110504_autosave02_d5_galatia_3ready_ctl_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D5_20261012-110504_autosave02_d5_galatia_3ready_ctl_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D5_20261012-110504_staged_d5_galatia_3ready_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D5_20261012-110504_staged_d5_galatia_3ready_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D5_20261012-110504_staged_d5_galatia_4ready_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D5_20261012-110504_staged_d5_galatia_4ready_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D_20261012-105131_staged_d1_ctl_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D_20261012-105131_staged_d1_ctl_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D_20261012-105131_staged_d1_none_free_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D_20261012-105131_staged_d1_none_free_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D_20261012-105131_staged_d1_one_free_100_42_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D_20261012-105131_staged_d1_one_free_100_42_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`D_20261012-105131_staged_d1_two_free_100_42_and_102_44_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/D_20261012-105131_staged_d1_two_free_100_42_and_102_44_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`E_20261012-125222_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/E_20261012-125222_X_original_before_anything.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`E_20261012-125252_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/E_20261012-125252_X_original_before_anything.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`E_20261012-130227_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/E_20261012-130227_X_original_before_anything.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`E_20261012-131240_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/E_20261012-131240_X_original_before_anything.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`E_20261012-132209_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/E_20261012-132209_X_original_before_anything.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`E_20261012-133143_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/E_20261012-133143_X_original_before_anything.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`E_20261012-144638_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/E_20261012-144638_X_original_before_anything.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`F_20261012-103825_X_original_before_anything.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/F_20261012-103825_X_original_before_anything.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`F_20261012-103825_autosave01_newgame_t720_AUTO0720.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/F_20261012-103825_autosave01_newgame_t720_AUTO0720.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave01_g_near_calm_c80_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave01_g_near_calm_c80_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave02_g_near_rough_c80_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave02_g_near_rough_c80_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave03_g_away_calm_c80_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave03_g_away_calm_c80_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave04_g_away_rough_c80_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave04_g_away_rough_c80_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave05_g_near_rough_c80_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave05_g_near_rough_c80_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave06_g_away_calm_c80_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave06_g_away_calm_c80_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave07_g_away_rough_c80_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave07_g_away_rough_c80_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave08_g_near_calm_c80_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave08_g_near_calm_c80_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave09_g_away_calm_c80_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave09_g_away_calm_c80_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave10_g_away_rough_c80_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave10_g_away_rough_c80_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_autosave11_g_near_calm_c80_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_autosave11_g_near_calm_c80_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_away_calm_c80_01_G_20261012-110607_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_away_calm_c80_01_G_20261012-110607_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_away_calm_c80_02_G_20261012-110607_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_away_calm_c80_02_G_20261012-110607_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_away_calm_c80_03_G_20261012-110607_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_away_calm_c80_03_G_20261012-110607_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_away_rough_c80_01_G_20261012-110607_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_away_rough_c80_01_G_20261012-110607_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_away_rough_c80_02_G_20261012-110607_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_away_rough_c80_02_G_20261012-110607_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_away_rough_c80_03_G_20261012-110607_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_away_rough_c80_03_G_20261012-110607_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_near_calm_c80_01_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_near_calm_c80_01_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_near_calm_c80_02_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_near_calm_c80_02_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_near_calm_c80_03_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_near_calm_c80_03_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_near_rough_c80_01_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_near_rough_c80_01_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_near_rough_c80_02_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_near_rough_c80_02_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-110607_staged_g_near_rough_c80_03_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-110607_staged_g_near_rough_c80_03_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-111026_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-111026_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-111026_staged_g_near_calm_c80_01_G_20261012-111026_staged_g_port_peace_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-111026_staged_g_near_calm_c80_01_G_20261012-111026_staged_g_port_peace_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-111026_staged_g_port_peace_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-111026_staged_g_port_peace_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave01_g_near_calm_c80_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave01_g_near_calm_c80_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave02_g_near_rough_c80_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave02_g_near_rough_c80_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave03_g_away_calm_c80_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave03_g_away_calm_c80_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave04_g_away_rough_c80_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave04_g_away_rough_c80_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave05_g_near_rough_c80_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave05_g_near_rough_c80_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave06_g_away_calm_c80_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave06_g_away_calm_c80_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave07_g_away_rough_c80_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave07_g_away_rough_c80_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave08_g_near_calm_c80_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave08_g_near_calm_c80_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave09_g_away_calm_c80_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave09_g_away_calm_c80_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave10_g_away_rough_c80_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave10_g_away_rough_c80_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave11_g_near_calm_c80_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave11_g_near_calm_c80_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave12_g_near_rough_c80_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave12_g_near_rough_c80_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave13_g_away_rough_c80_04_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave13_g_away_rough_c80_04_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave14_g_near_calm_c80_04_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave14_g_near_calm_c80_04_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave15_g_near_rough_c80_04_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave15_g_near_rough_c80_04_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave16_g_away_calm_c80_04_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave16_g_away_calm_c80_04_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave17_g_near_calm_c80_05_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave17_g_near_calm_c80_05_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave18_g_near_rough_c80_05_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave18_g_near_rough_c80_05_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave19_g_away_calm_c80_05_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave19_g_away_calm_c80_05_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave20_g_away_rough_c80_05_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave20_g_away_rough_c80_05_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave21_g_near_rough_c80_06_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave21_g_near_rough_c80_06_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave22_g_away_calm_c80_06_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave22_g_away_calm_c80_06_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave23_g_away_rough_c80_06_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave23_g_away_rough_c80_06_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave24_g_near_calm_c80_06_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave24_g_near_calm_c80_06_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave25_g_near_calm_c60_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave25_g_near_calm_c60_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave26_g_near_rough_c60_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave26_g_near_rough_c60_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave27_g_away_calm_c60_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave27_g_away_calm_c60_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave28_g_away_rough_c60_01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave28_g_away_rough_c60_01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave29_g_near_rough_c60_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave29_g_near_rough_c60_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave30_g_away_calm_c60_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave30_g_away_calm_c60_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave31_g_away_rough_c60_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave31_g_away_rough_c60_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave32_g_near_calm_c60_02_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave32_g_near_calm_c60_02_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave33_g_away_calm_c60_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave33_g_away_calm_c60_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave34_g_away_rough_c60_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave34_g_away_rough_c60_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave35_g_near_calm_c60_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave35_g_near_calm_c60_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave36_g_near_rough_c60_03_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave36_g_near_rough_c60_03_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave37_g_away_rough_c60_04_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave37_g_away_rough_c60_04_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave38_g_near_calm_c60_04_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave38_g_near_calm_c60_04_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave39_g_near_rough_c60_04_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave39_g_near_rough_c60_04_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave40_g_away_calm_c60_04_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave40_g_away_calm_c60_04_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave41_g_near_calm_c60_05_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave41_g_near_calm_c60_05_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave42_g_near_rough_c60_05_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave42_g_near_rough_c60_05_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave43_g_away_calm_c60_05_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave43_g_away_calm_c60_05_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave44_g_away_rough_c60_05_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave44_g_away_rough_c60_05_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave45_g_near_rough_c60_06_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave45_g_near_rough_c60_06_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave46_g_away_calm_c60_06_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave46_g_away_calm_c60_06_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave47_g_away_rough_c60_06_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave47_g_away_rough_c60_06_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_autosave48_g_near_calm_c60_06_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_autosave48_g_near_calm_c60_06_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_away_base.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_away_base.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c60_01_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c60_01_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c60_02_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c60_02_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c60_03_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c60_03_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c60_04_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c60_04_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c60_05_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c60_05_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c60_06_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c60_06_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c80_01_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c80_01_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c80_02_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c80_02_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c80_03_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c80_03_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c80_04_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c80_04_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c80_05_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c80_05_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_calm_c80_06_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_calm_c80_06_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c60_01_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c60_01_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c60_02_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c60_02_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c60_03_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c60_03_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c60_04_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c60_04_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c60_05_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c60_05_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c60_06_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c60_06_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c80_01_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c80_01_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c80_02_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c80_02_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c80_03_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c80_03_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c80_04_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c80_04_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c80_05_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c80_05_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_away_rough_c80_06_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_away_rough_c80_06_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c60_01_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c60_01_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c60_02_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c60_02_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c60_03_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c60_03_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c60_04_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c60_04_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c60_05_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c60_05_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c60_06_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c60_06_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c80_01_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c80_01_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c80_02_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c80_02_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c80_03_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c80_03_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c80_04_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c80_04_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c80_05_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c80_05_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_calm_c80_06_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_calm_c80_06_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c60_01_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c60_01_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c60_02_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c60_02_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c60_03_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c60_03_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c60_04_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c60_04_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c60_05_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c60_05_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c60_06_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c60_06_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c80_01_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c80_01_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c80_02_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c80_02_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c80_03_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c80_03_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c80_04_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c80_04_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c80_05_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c80_05_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_near_rough_c80_06_b.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_near_rough_c80_06_b.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`G_20261012-115755_staged_g_port_peace_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/G_20261012-115755_staged_g_port_peace_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`H_20261012-110012_autosave01_h_ctl_gaul_only_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/H_20261012-110012_autosave01_h_ctl_gaul_only_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`H_20261012-110012_autosave02_h_idx0_gaul_idx9_dacia_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/H_20261012-110012_autosave02_h_idx0_gaul_idx9_dacia_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`H_20261012-110012_autosave03_h_idx0_dacia_idx9_gaul_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/H_20261012-110012_autosave03_h_idx0_dacia_idx9_gaul_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`H_20261012-110012_staged_h_ctl_gaul_only_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/H_20261012-110012_staged_h_ctl_gaul_only_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`H_20261012-110012_staged_h_idx0_dacia_idx9_gaul_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/H_20261012-110012_staged_h_idx0_dacia_idx9_gaul_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`H_20261012-110012_staged_h_idx0_gaul_idx9_dacia_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/H_20261012-110012_staged_h_idx0_gaul_idx9_dacia_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`I_20261012-110121_autosave01_i_1_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/I_20261012-110121_autosave01_i_1_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`I_20261012-110121_autosave02_i_2_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/I_20261012-110121_autosave02_i_2_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`I_20261012-110121_autosave03_i_3_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/I_20261012-110121_autosave03_i_3_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`I_20261012-110121_autosave04_i_4_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/I_20261012-110121_autosave04_i_4_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`I_20261012-110121_staged_i_week11_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/I_20261012-110121_staged_i_week11_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_autosave01_j_control_nostage_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_autosave01_j_control_nostage_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_autosave02_j_dead_0_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_autosave02_j_dead_0_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_autosave03_j_dead_7_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_autosave03_j_dead_7_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_autosave04_j_dead_9_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_autosave04_j_dead_9_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_autosave05_j_alive_unity0_9_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_autosave05_j_alive_unity0_9_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_autosave06_j_control_nostage_again_t726_AUTO0726.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_autosave06_j_control_nostage_again_t726_AUTO0726.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_staged_j_alive_unity0_9_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_staged_j_alive_unity0_9_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_staged_j_control_nostage_again_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_staged_j_control_nostage_again_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_staged_j_control_nostage_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_staged_j_control_nostage_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_staged_j_dead_0_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_staged_j_dead_0_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_staged_j_dead_7_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_staged_j_dead_7_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`J_20261012-110249_staged_j_dead_9_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/J_20261012-110249_staged_j_dead_9_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave01_k_nat_t001_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave01_k_nat_t001_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave02_k_nat_t002_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave02_k_nat_t002_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave03_k_nat_t003_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave03_k_nat_t003_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave04_k_nat_t004_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave04_k_nat_t004_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave05_k_nat_t005_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave05_k_nat_t005_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave06_k_nat_t006_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave06_k_nat_t006_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave07_k_nat_t007_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave07_k_nat_t007_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave08_k_nat_t008_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave08_k_nat_t008_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave09_k_nat_t009_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave09_k_nat_t009_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave10_k_nat_t010_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave10_k_nat_t010_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave11_k_nat_t011_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave11_k_nat_t011_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave12_k_nat_t012_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave12_k_nat_t012_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave13_k_nat_t013_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave13_k_nat_t013_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave14_k_nat_t014_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave14_k_nat_t014_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave15_k_nat_t015_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave15_k_nat_t015_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave16_k_nat_t016_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave16_k_nat_t016_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave17_k_nat_t017_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave17_k_nat_t017_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave18_k_nat_t018_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave18_k_nat_t018_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave19_k_nat_t019_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave19_k_nat_t019_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave20_k_nat_t020_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave20_k_nat_t020_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave21_k_nat_t021_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave21_k_nat_t021_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave22_k_nat_t022_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave22_k_nat_t022_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave23_k_nat_t023_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave23_k_nat_t023_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave24_k_nat_t024_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave24_k_nat_t024_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave25_k_nat_t025_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave25_k_nat_t025_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave26_k_nat_t026_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave26_k_nat_t026_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave27_k_nat_t027_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave27_k_nat_t027_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave28_k_nat_t028_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave28_k_nat_t028_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave29_k_nat_t029_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave29_k_nat_t029_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave30_k_nat_t030_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave30_k_nat_t030_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave31_k_nat_t031_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave31_k_nat_t031_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave32_k_nat_t032_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave32_k_nat_t032_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave33_k_nat_t033_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave33_k_nat_t033_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave34_k_nat_t034_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave34_k_nat_t034_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave35_k_nat_t035_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave35_k_nat_t035_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave36_k_nat_t036_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave36_k_nat_t036_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave37_k_nat_t037_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave37_k_nat_t037_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave38_k_nat_t038_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave38_k_nat_t038_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave39_k_nat_t039_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave39_k_nat_t039_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave40_k_nat_t040_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave40_k_nat_t040_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave41_k_nat_t041_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave41_k_nat_t041_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave42_k_nat_t042_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave42_k_nat_t042_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave43_k_nat_t043_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave43_k_nat_t043_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave44_k_nat_t044_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave44_k_nat_t044_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave45_k_nat_t045_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave45_k_nat_t045_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave46_k_nat_t046_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave46_k_nat_t046_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave47_k_nat_t047_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave47_k_nat_t047_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave48_k_nat_t048_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave48_k_nat_t048_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave49_k_nat_t049_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave49_k_nat_t049_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave50_k_nat_t050_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave50_k_nat_t050_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave51_k_nat_t051_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave51_k_nat_t051_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave52_k_nat_t052_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave52_k_nat_t052_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave53_k_nat_t053_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave53_k_nat_t053_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave54_k_nat_t054_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave54_k_nat_t054_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave55_k_nat_t055_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave55_k_nat_t055_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave56_k_nat_t056_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave56_k_nat_t056_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave57_k_nat_t057_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave57_k_nat_t057_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave58_k_nat_t058_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave58_k_nat_t058_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave59_k_nat_t059_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave59_k_nat_t059_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_autosave60_k_nat_t060_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_autosave60_k_nat_t060_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-111608_staged_k_nat_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-111608_staged_k_nat_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave01_k_p3_t001_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave01_k_p3_t001_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave02_k_p3_t002_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave02_k_p3_t002_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave03_k_p3_t003_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave03_k_p3_t003_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave04_k_p3_t004_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave04_k_p3_t004_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave05_k_p3_t005_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave05_k_p3_t005_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave06_k_p3_t006_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave06_k_p3_t006_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave07_k_p3_t007_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave07_k_p3_t007_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave08_k_p3_t008_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave08_k_p3_t008_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave09_k_p3_t009_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave09_k_p3_t009_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave10_k_p3_t010_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave10_k_p3_t010_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave11_k_p3_t011_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave11_k_p3_t011_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave12_k_p3_t012_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave12_k_p3_t012_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave13_k_p3_t013_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave13_k_p3_t013_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave14_k_p3_t014_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave14_k_p3_t014_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave15_k_p3_t015_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave15_k_p3_t015_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave16_k_p3_t016_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave16_k_p3_t016_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave17_k_p3_t017_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave17_k_p3_t017_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave18_k_p3_t018_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave18_k_p3_t018_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave19_k_p3_t019_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave19_k_p3_t019_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave20_k_p3_t020_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave20_k_p3_t020_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave21_k_p3_t021_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave21_k_p3_t021_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave22_k_p3_t022_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave22_k_p3_t022_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave23_k_p3_t023_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave23_k_p3_t023_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave24_k_p3_t024_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave24_k_p3_t024_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave25_k_p3_t025_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave25_k_p3_t025_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave26_k_p3_t026_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave26_k_p3_t026_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave27_k_p3_t027_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave27_k_p3_t027_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave28_k_p3_t028_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave28_k_p3_t028_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave29_k_p3_t029_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave29_k_p3_t029_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave30_k_p3_t030_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave30_k_p3_t030_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave31_k_p3_t031_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave31_k_p3_t031_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave32_k_p3_t032_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave32_k_p3_t032_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave33_k_p3_t033_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave33_k_p3_t033_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave34_k_p3_t034_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave34_k_p3_t034_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave35_k_p3_t035_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave35_k_p3_t035_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave36_k_p3_t036_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave36_k_p3_t036_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave37_k_p3_t037_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave37_k_p3_t037_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave38_k_p3_t038_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave38_k_p3_t038_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave39_k_p3_t039_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave39_k_p3_t039_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave40_k_p3_t040_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave40_k_p3_t040_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave41_k_p3_t041_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave41_k_p3_t041_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave42_k_p3_t042_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave42_k_p3_t042_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave43_k_p3_t043_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave43_k_p3_t043_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave44_k_p3_t044_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave44_k_p3_t044_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave45_k_p3_t045_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave45_k_p3_t045_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave46_k_p3_t046_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave46_k_p3_t046_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave47_k_p3_t047_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave47_k_p3_t047_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave48_k_p3_t048_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave48_k_p3_t048_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave49_k_p3_t049_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave49_k_p3_t049_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave50_k_p3_t050_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave50_k_p3_t050_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave51_k_p3_t051_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave51_k_p3_t051_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave52_k_p3_t052_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave52_k_p3_t052_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave53_k_p3_t053_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave53_k_p3_t053_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave54_k_p3_t054_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave54_k_p3_t054_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave55_k_p3_t055_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave55_k_p3_t055_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave56_k_p3_t056_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave56_k_p3_t056_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave57_k_p3_t057_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave57_k_p3_t057_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave58_k_p3_t058_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave58_k_p3_t058_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave59_k_p3_t059_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave59_k_p3_t059_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_autosave60_k_p3_t060_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_autosave60_k_p3_t060_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-113704_staged_k_p3_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-113704_staged_k_p3_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave01_k_nowar_t001_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave01_k_nowar_t001_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave02_k_nowar_t002_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave02_k_nowar_t002_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave03_k_nowar_t003_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave03_k_nowar_t003_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave04_k_nowar_t004_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave04_k_nowar_t004_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave05_k_nowar_t005_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave05_k_nowar_t005_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave06_k_nowar_t006_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave06_k_nowar_t006_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave07_k_nowar_t007_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave07_k_nowar_t007_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave08_k_nowar_t008_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave08_k_nowar_t008_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave09_k_nowar_t009_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave09_k_nowar_t009_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave10_k_nowar_t010_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave10_k_nowar_t010_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave11_k_nowar_t011_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave11_k_nowar_t011_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave12_k_nowar_t012_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave12_k_nowar_t012_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave13_k_nowar_t013_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave13_k_nowar_t013_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave14_k_nowar_t014_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave14_k_nowar_t014_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave15_k_nowar_t015_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave15_k_nowar_t015_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave16_k_nowar_t016_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave16_k_nowar_t016_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave17_k_nowar_t017_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave17_k_nowar_t017_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave18_k_nowar_t018_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave18_k_nowar_t018_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave19_k_nowar_t019_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave19_k_nowar_t019_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave20_k_nowar_t020_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave20_k_nowar_t020_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave21_k_nowar_t021_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave21_k_nowar_t021_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave22_k_nowar_t022_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave22_k_nowar_t022_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave23_k_nowar_t023_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave23_k_nowar_t023_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave24_k_nowar_t024_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave24_k_nowar_t024_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave25_k_nowar_t025_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave25_k_nowar_t025_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave26_k_nowar_t026_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave26_k_nowar_t026_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave27_k_nowar_t027_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave27_k_nowar_t027_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave28_k_nowar_t028_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave28_k_nowar_t028_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave29_k_nowar_t029_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave29_k_nowar_t029_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave30_k_nowar_t030_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave30_k_nowar_t030_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave31_k_nowar_t031_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave31_k_nowar_t031_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave32_k_nowar_t032_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave32_k_nowar_t032_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave33_k_nowar_t033_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave33_k_nowar_t033_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave34_k_nowar_t034_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave34_k_nowar_t034_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave35_k_nowar_t035_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave35_k_nowar_t035_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave36_k_nowar_t036_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave36_k_nowar_t036_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave37_k_nowar_t037_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave37_k_nowar_t037_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave38_k_nowar_t038_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave38_k_nowar_t038_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave39_k_nowar_t039_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave39_k_nowar_t039_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave40_k_nowar_t040_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave40_k_nowar_t040_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave41_k_nowar_t041_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave41_k_nowar_t041_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave42_k_nowar_t042_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave42_k_nowar_t042_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave43_k_nowar_t043_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave43_k_nowar_t043_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave44_k_nowar_t044_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave44_k_nowar_t044_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave45_k_nowar_t045_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave45_k_nowar_t045_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave46_k_nowar_t046_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave46_k_nowar_t046_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave47_k_nowar_t047_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave47_k_nowar_t047_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave48_k_nowar_t048_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave48_k_nowar_t048_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave49_k_nowar_t049_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave49_k_nowar_t049_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave50_k_nowar_t050_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave50_k_nowar_t050_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave51_k_nowar_t051_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave51_k_nowar_t051_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave52_k_nowar_t052_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave52_k_nowar_t052_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave53_k_nowar_t053_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave53_k_nowar_t053_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave54_k_nowar_t054_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave54_k_nowar_t054_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave55_k_nowar_t055_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave55_k_nowar_t055_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave56_k_nowar_t056_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave56_k_nowar_t056_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave57_k_nowar_t057_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave57_k_nowar_t057_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave58_k_nowar_t058_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave58_k_nowar_t058_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave59_k_nowar_t059_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave59_k_nowar_t059_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_autosave60_k_nowar_t060_t721_AUTO0721.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_autosave60_k_nowar_t060_t721_AUTO0721.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`K_20261012-122049_staged_k_nowar_run0-start-AUTO0720-seed12345.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/K_20261012-122049_staged_k_nowar_run0-start-AUTO0720-seed12345.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave01_l_r01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave01_l_r01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave02_l_r02_t736_AUTO0736.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave02_l_r02_t736_AUTO0736.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave03_l_r03_t737_AUTO0737.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave03_l_r03_t737_AUTO0737.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave04_l_r04_t738_AUTO0738.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave04_l_r04_t738_AUTO0738.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave05_l_r05_t739_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave05_l_r05_t739_AUTO0739.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave06_l_r06_t740_AUTO0740.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave06_l_r06_t740_AUTO0740.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave07_l_r07_t741_AUTO0741.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave07_l_r07_t741_AUTO0741.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave08_l_r08_t742_AUTO0742.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave08_l_r08_t742_AUTO0742.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave09_l_r09_t743_AUTO0743.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave09_l_r09_t743_AUTO0743.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave10_l_r10_t744_AUTO0744.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave10_l_r10_t744_AUTO0744.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave11_l_r11_t745_AUTO0745.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave11_l_r11_t745_AUTO0745.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave12_l_r12_t746_AUTO0746.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave12_l_r12_t746_AUTO0746.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave13_l_r13_t747_AUTO0747.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave13_l_r13_t747_AUTO0747.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave14_l_r14_t748_AUTO0748.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave14_l_r14_t748_AUTO0748.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave15_l_r15_t749_AUTO0749.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave15_l_r15_t749_AUTO0749.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave16_l_r16_t750_AUTO0750.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave16_l_r16_t750_AUTO0750.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave17_l_r17_t751_AUTO0751.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave17_l_r17_t751_AUTO0751.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave18_l_r18_t752_AUTO0752.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave18_l_r18_t752_AUTO0752.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave19_l_r19_t753_AUTO0753.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave19_l_r19_t753_AUTO0753.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave20_l_r20_t754_AUTO0754.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave20_l_r20_t754_AUTO0754.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave21_l_r21_t755_AUTO0755.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave21_l_r21_t755_AUTO0755.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave22_l_r22_t756_AUTO0756.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave22_l_r22_t756_AUTO0756.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave23_l_r23_t757_AUTO0757.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave23_l_r23_t757_AUTO0757.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave24_l_r24_t758_AUTO0758.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave24_l_r24_t758_AUTO0758.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave25_l_r25_t759_AUTO0759.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave25_l_r25_t759_AUTO0759.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave26_l_r26_t760_AUTO0760.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave26_l_r26_t760_AUTO0760.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave27_l_r27_t761_AUTO0761.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave27_l_r27_t761_AUTO0761.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave28_l_r28_t762_AUTO0762.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave28_l_r28_t762_AUTO0762.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave29_l_r29_t763_AUTO0763.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave29_l_r29_t763_AUTO0763.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave30_l_r30_t764_AUTO0764.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave30_l_r30_t764_AUTO0764.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave31_l_r31_t765_AUTO0765.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave31_l_r31_t765_AUTO0765.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave32_l_r32_t766_AUTO0766.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave32_l_r32_t766_AUTO0766.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave33_l_r33_t767_AUTO0767.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave33_l_r33_t767_AUTO0767.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave34_l_r34_t768_AUTO0768.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave34_l_r34_t768_AUTO0768.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave35_l_r35_t769_AUTO0769.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave35_l_r35_t769_AUTO0769.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave36_l_r36_t770_AUTO0770.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave36_l_r36_t770_AUTO0770.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave37_l_r37_t771_AUTO0771.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave37_l_r37_t771_AUTO0771.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave38_l_r38_t772_AUTO0772.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave38_l_r38_t772_AUTO0772.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave39_l_r39_t773_AUTO0773.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave39_l_r39_t773_AUTO0773.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_autosave40_l_r40_t774_AUTO0774.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_autosave40_l_r40_t774_AUTO0774.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-121353_staged_l_peace_supplies500_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-121353_staged_l_peace_supplies500_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave01_l_r01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave01_l_r01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave02_l_r02_t736_AUTO0736.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave02_l_r02_t736_AUTO0736.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave03_l_r03_t737_AUTO0737.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave03_l_r03_t737_AUTO0737.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave04_l_r04_t738_AUTO0738.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave04_l_r04_t738_AUTO0738.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave05_l_r05_t739_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave05_l_r05_t739_AUTO0739.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave06_l_r06_t740_AUTO0740.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave06_l_r06_t740_AUTO0740.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave07_l_r07_t741_AUTO0741.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave07_l_r07_t741_AUTO0741.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave08_l_r08_t742_AUTO0742.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave08_l_r08_t742_AUTO0742.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave09_l_r09_t743_AUTO0743.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave09_l_r09_t743_AUTO0743.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave10_l_r10_t744_AUTO0744.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave10_l_r10_t744_AUTO0744.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave11_l_r11_t745_AUTO0745.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave11_l_r11_t745_AUTO0745.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave12_l_r12_t746_AUTO0746.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave12_l_r12_t746_AUTO0746.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave13_l_r13_t747_AUTO0747.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave13_l_r13_t747_AUTO0747.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave14_l_r14_t748_AUTO0748.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave14_l_r14_t748_AUTO0748.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave15_l_r15_t749_AUTO0749.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave15_l_r15_t749_AUTO0749.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave16_l_r16_t750_AUTO0750.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave16_l_r16_t750_AUTO0750.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave17_l_r17_t751_AUTO0751.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave17_l_r17_t751_AUTO0751.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave18_l_r18_t752_AUTO0752.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave18_l_r18_t752_AUTO0752.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave19_l_r19_t753_AUTO0753.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave19_l_r19_t753_AUTO0753.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave20_l_r20_t754_AUTO0754.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave20_l_r20_t754_AUTO0754.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave21_l_r21_t755_AUTO0755.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave21_l_r21_t755_AUTO0755.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave22_l_r22_t756_AUTO0756.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave22_l_r22_t756_AUTO0756.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave23_l_r23_t757_AUTO0757.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave23_l_r23_t757_AUTO0757.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave24_l_r24_t758_AUTO0758.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave24_l_r24_t758_AUTO0758.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_autosave25_l_r25_t759_AUTO0759.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_autosave25_l_r25_t759_AUTO0759.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124307_staged_l_peace_supplies500_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124307_staged_l_peace_supplies500_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124813_autosave01_l_r01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124813_autosave01_l_r01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124813_autosave02_l_r02_t736_AUTO0736.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124813_autosave02_l_r02_t736_AUTO0736.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124813_autosave03_l_r03_t737_AUTO0737.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124813_autosave03_l_r03_t737_AUTO0737.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124813_staged_l_peace_supplies500_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124813_staged_l_peace_supplies500_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124913_autosave01_l_r01_t735_AUTO0735.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124913_autosave01_l_r01_t735_AUTO0735.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124913_autosave02_l_r02_t736_AUTO0736.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124913_autosave02_l_r02_t736_AUTO0736.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124913_autosave03_l_r03_t737_AUTO0737.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124913_autosave03_l_r03_t737_AUTO0737.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124913_autosave04_l_r04_t738_AUTO0738.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124913_autosave04_l_r04_t738_AUTO0738.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124913_autosave05_l_r05_t739_AUTO0739.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124913_autosave05_l_r05_t739_AUTO0739.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124913_autosave06_l_r06_t740_AUTO0740.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124913_autosave06_l_r06_t740_AUTO0740.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |
| [`L_20261012-124913_staged_l_peace_supplies500_fleet-port-antium-0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-g4-followups/L_20261012-124913_staged_l_peace_supplies500_fleet-port-antium-0734.SAV) | `run-exp-g4-followups` (repo `ic2-conquest`) | 1 |

## Original AI probes (2026-10-16)

Pinned source: `diegoami/ic2-conquest` main `caf2a17d420cfca35757fad60311cae9514af257`,
`runs/experiments/data/run-exp-ai-oct16/SAVES.sha256`. Intake checked all 257 local
artifact hashes against this manifest and release digests; 252 are saves and five
are EXEs. Text logs, input manifests, final `observations-20261016-153620.json`
and source references remain in that pinned data folder. No native Windows evidence.

| Save | Release (repo `ic2-conquest`) |
|---|---|
| [`a_dist4-20261016-144810-509878-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_dist4-20261016-144810-509878-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`a_dist4-20261016-144810-509878.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_dist4-20261016-144810-509878.SAV) | `run-exp-ai-oct16` |
| [`a_dist4-20261016-145017-521550-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_dist4-20261016-145017-521550-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`a_dist4-20261016-145017-521550-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_dist4-20261016-145017-521550-post.SAV) | `run-exp-ai-oct16` |
| [`a_dist4-20261016-145017-521550.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_dist4-20261016-145017-521550.SAV) | `run-exp-ai-oct16` |
| [`a_dist5-20261016-145017-521550-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_dist5-20261016-145017-521550-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`a_dist5-20261016-145017-521550-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_dist5-20261016-145017-521550-post.SAV) | `run-exp-ai-oct16` |
| [`a_dist5-20261016-145017-521550.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_dist5-20261016-145017-521550.SAV) | `run-exp-ai-oct16` |
| [`a_empty-20261016-145017-521550-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_empty-20261016-145017-521550-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`a_empty-20261016-145017-521550-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_empty-20261016-145017-521550-post.SAV) | `run-exp-ai-oct16` |
| [`a_empty-20261016-145017-521550.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_empty-20261016-145017-521550.SAV) | `run-exp-ai-oct16` |
| [`a_hostile-20261016-150546-540049-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_hostile-20261016-150546-540049-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`a_hostile-20261016-150546-540049-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_hostile-20261016-150546-540049-post.SAV) | `run-exp-ai-oct16` |
| [`a_hostile-20261016-150546-540049.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_hostile-20261016-150546-540049.SAV) | `run-exp-ai-oct16` |
| [`a_positive-20261016-145017-521550-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_positive-20261016-145017-521550-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`a_positive-20261016-145017-521550-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_positive-20261016-145017-521550-post.SAV) | `run-exp-ai-oct16` |
| [`a_positive-20261016-145017-521550.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_positive-20261016-145017-521550.SAV) | `run-exp-ai-oct16` |
| [`a_repeat-20261016-145017-521550-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_repeat-20261016-145017-521550-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`a_repeat-20261016-145017-521550-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_repeat-20261016-145017-521550-post.SAV) | `run-exp-ai-oct16` |
| [`a_repeat-20261016-145017-521550.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_repeat-20261016-145017-521550.SAV) | `run-exp-ai-oct16` |
| [`a_zero-20261016-145017-521550-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_zero-20261016-145017-521550-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`a_zero-20261016-145017-521550-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_zero-20261016-145017-521550-post.SAV) | `run-exp-ai-oct16` |
| [`a_zero-20261016-145017-521550.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/a_zero-20261016-145017-521550.SAV) | `run-exp-ai-oct16` |
| [`aboard-20261016-144810-509878-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/aboard-20261016-144810-509878-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`aboard-20261016-144810-509878-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/aboard-20261016-144810-509878-post.SAV) | `run-exp-ai-oct16` |
| [`aboard-20261016-144810-509878.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/aboard-20261016-144810-509878.SAV) | `run-exp-ai-oct16` |
| [`aboard-20261016-145017-521550-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/aboard-20261016-145017-521550-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`aboard-20261016-145017-521550-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/aboard-20261016-145017-521550-post.SAV) | `run-exp-ai-oct16` |
| [`aboard-20261016-145017-521550.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/aboard-20261016-145017-521550.SAV) | `run-exp-ai-oct16` |
| [`f0t101-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f0t101-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f0t101-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f0t101-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f0t101-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f0t101-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f100t101-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f100t101-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f100t101-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f100t101-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f100t101-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f100t101-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f101t101-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f101t101-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f101t101-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f101t101-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f101t101-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f101t101-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f94-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f94-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f94-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f94grant-20261016-150546-540049-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94grant-20261016-150546-540049-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f94grant-20261016-150546-540049-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94grant-20261016-150546-540049-post.SAV) | `run-exp-ai-oct16` |
| [`f94grant-20261016-150546-540049.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94grant-20261016-150546-540049.SAV) | `run-exp-ai-oct16` |
| [`f94s91-20261016-150546-540049-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94s91-20261016-150546-540049-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f94s91-20261016-150546-540049-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94s91-20261016-150546-540049-post.SAV) | `run-exp-ai-oct16` |
| [`f94s91-20261016-150546-540049.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94s91-20261016-150546-540049.SAV) | `run-exp-ai-oct16` |
| [`f94t101-20261016-150546-540049-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94t101-20261016-150546-540049-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f94t101-20261016-150546-540049-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94t101-20261016-150546-540049-post.SAV) | `run-exp-ai-oct16` |
| [`f94t101-20261016-150546-540049.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f94t101-20261016-150546-540049.SAV) | `run-exp-ai-oct16` |
| [`f95-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f95-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f95-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f95-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f95-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f95-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f96-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f96-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f96-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f96-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f96-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f96-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f99t100-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f99t100-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f99t100-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f99t100-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f99t100-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f99t100-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f99t101-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f99t101-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f99t101-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f99t101-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f99t101-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f99t101-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f_cap-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_cap-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f_cap-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_cap-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f_cap-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_cap-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f_dist3-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_dist3-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f_dist3-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_dist3-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f_dist3-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_dist3-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f_dist4-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_dist4-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f_dist4-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_dist4-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f_dist4-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_dist4-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f_empty-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_empty-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f_empty-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_empty-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f_empty-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_empty-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f_hostile-20261016-145549-528200-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_hostile-20261016-145549-528200-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f_hostile-20261016-145549-528200-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_hostile-20261016-145549-528200-post.SAV) | `run-exp-ai-oct16` |
| [`f_hostile-20261016-145549-528200.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_hostile-20261016-145549-528200.SAV) | `run-exp-ai-oct16` |
| [`f_repeat-20261016-150546-540049-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_repeat-20261016-150546-540049-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f_repeat-20261016-150546-540049-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_repeat-20261016-150546-540049-post.SAV) | `run-exp-ai-oct16` |
| [`f_repeat-20261016-150546-540049.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_repeat-20261016-150546-540049.SAV) | `run-exp-ai-oct16` |
| [`f_y3-20261016-150546-540049-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_y3-20261016-150546-540049-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f_y3-20261016-150546-540049-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_y3-20261016-150546-540049-post.SAV) | `run-exp-ai-oct16` |
| [`f_y3-20261016-150546-540049.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_y3-20261016-150546-540049.SAV) | `run-exp-ai-oct16` |
| [`f_y4-20261016-150546-540049-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_y4-20261016-150546-540049-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`f_y4-20261016-150546-540049-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_y4-20261016-150546-540049-post.SAV) | `run-exp-ai-oct16` |
| [`f_y4-20261016-150546-540049.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/f_y4-20261016-150546-540049.SAV) | `run-exp-ai-oct16` |
| [`gen_ai_control-20261016-150636-540904-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_ai_control-20261016-150636-540904-BATTLE01.SAV) | `run-exp-ai-oct16` |
| [`gen_ai_control-20261016-150636-540904-BATTLE02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_ai_control-20261016-150636-540904-BATTLE02.SAV) | `run-exp-ai-oct16` |
| [`gen_ai_control-20261016-150636-540904.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_ai_control-20261016-150636-540904.SAV) | `run-exp-ai-oct16` |
| [`gen_human_off-20261016-150636-540904-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_off-20261016-150636-540904-BATTLE01.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE01.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE02.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE03.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE03.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE04.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE04.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE05.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE05.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE06.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE06.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE07.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE07.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE08.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE08.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE09.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE09.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE10.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE11.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE11.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE12.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE12.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE13.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE14.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE14.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE15.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE16.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE16.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE17.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE17.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE18.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE18.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE19.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE19.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE20.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE20.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE21.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE21.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE22.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE22.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE23.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE23.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE24.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE24.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE25.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE25.SAV) | `run-exp-ai-oct16` |
| [`gen_human_on-20261016-150636-540904-BATTLE26.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_human_on-20261016-150636-540904-BATTLE26.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE01.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE02.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE03.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE03.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE04.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE04.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE05.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE05.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE06.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE06.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE07.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE07.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE08.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE08.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE09.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE09.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE10.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE11.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE11.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE12.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE12.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE13.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE14.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE14.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE15.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE16.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE16.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE17.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE17.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE18.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE18.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE19.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE19.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE20.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE20.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE21.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE21.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE22.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE22.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE23.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE23.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE24.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE24.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE25.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE25.SAV) | `run-exp-ai-oct16` |
| [`gen_interrupt_on-20261016-150939-545243-BATTLE26.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_interrupt_on-20261016-150939-545243-BATTLE26.SAV) | `run-exp-ai-oct16` |
| [`gen_plain_off-20261016-150636-540904-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_plain_off-20261016-150636-540904-BATTLE01.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE01.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE02.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE03.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE03.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE04.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE04.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE05.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE05.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE06.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE06.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE07.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE07.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE08.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE08.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE09.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE09.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE10.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE11.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE11.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE12.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE12.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE13.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE14.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE14.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE15.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE16.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE16.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE17.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE17.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE18.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE18.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE19.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE19.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE20.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE20.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE21.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE21.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE22.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE22.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE23.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE23.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE24.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE24.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE25.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE25.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-150636-540904-BATTLE26.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-150636-540904-BATTLE26.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE01.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE02.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE03.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE03.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE04.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE04.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE05.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE05.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE06.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE06.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE07.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE07.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE08.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE08.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE09.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE09.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE10.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE11.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE11.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE12.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE12.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE13.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE14.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE14.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE15.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE16.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE16.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE17.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE17.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE18.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE18.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE19.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE19.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE20.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE20.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE21.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE21.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE22.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE22.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE23.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE23.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE24.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE24.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE25.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE25.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE26.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE26.SAV) | `run-exp-ai-oct16` |
| [`gen_reload_on-20261016-152304-549608-BATTLE27.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/gen_reload_on-20261016-152304-549608-BATTLE27.SAV) | `run-exp-ai-oct16` |
| [`land-20261016-144810-509878-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/land-20261016-144810-509878-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`land-20261016-144810-509878-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/land-20261016-144810-509878-post.SAV) | `run-exp-ai-oct16` |
| [`land-20261016-144810-509878.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/land-20261016-144810-509878.SAV) | `run-exp-ai-oct16` |
| [`land-20261016-145017-521550-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/land-20261016-145017-521550-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`land-20261016-145017-521550-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/land-20261016-145017-521550-post.SAV) | `run-exp-ai-oct16` |
| [`land-20261016-145017-521550.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/land-20261016-145017-521550.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary-20261016-145723-529357.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary-20261016-145723-529357.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary-20261016-150204-535849.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary-20261016-150204-535849.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary_observed-20261016-145723-529357-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary_observed-20261016-145723-529357-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary_observed-20261016-145723-529357-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary_observed-20261016-145723-529357-post.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary_observed-20261016-150204-535849-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary_observed-20261016-150204-535849-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary_observed-20261016-150204-535849-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary_observed-20261016-150204-535849-post.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary_plain-20261016-145723-529357-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary_plain-20261016-145723-529357-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary_plain-20261016-145723-529357-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary_plain-20261016-145723-529357-post.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary_plain-20261016-150204-535849-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary_plain-20261016-150204-535849-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_boundary_plain-20261016-150204-535849-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_boundary_plain-20261016-150204-535849-post.SAV) | `run-exp-ai-oct16` |
| [`reg_cross_only-20261016-151025-546199.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_cross_only-20261016-151025-546199.SAV) | `run-exp-ai-oct16` |
| [`reg_cross_only_observed-20261016-151025-546199-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_cross_only_observed-20261016-151025-546199-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_cross_only_observed-20261016-151025-546199-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_cross_only_observed-20261016-151025-546199-post.SAV) | `run-exp-ai-oct16` |
| [`reg_cross_only_plain-20261016-151025-546199-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_cross_only_plain-20261016-151025-546199-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_cross_only_plain-20261016-151025-546199-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_cross_only_plain-20261016-151025-546199-post.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_cross-20261016-151025-546199.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_cross-20261016-151025-546199.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_cross_observed-20261016-151025-546199-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_cross_observed-20261016-151025-546199-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_cross_observed-20261016-151025-546199-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_cross_observed-20261016-151025-546199-post.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_cross_plain-20261016-151025-546199-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_cross_plain-20261016-151025-546199-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_cross_plain-20261016-151025-546199-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_cross_plain-20261016-151025-546199-post.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_same-20261016-151025-546199.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_same-20261016-151025-546199.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_same_observed-20261016-151025-546199-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_same_observed-20261016-151025-546199-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_same_observed-20261016-151025-546199-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_same_observed-20261016-151025-546199-post.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_same_plain-20261016-151025-546199-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_same_plain-20261016-151025-546199-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_fallback_same_plain-20261016-151025-546199-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_fallback_same_plain-20261016-151025-546199-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left-20261016-145723-529357.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left-20261016-145723-529357.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left-20261016-150204-535849.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left-20261016-150204-535849.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left_observed-20261016-145723-529357-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left_observed-20261016-145723-529357-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left_observed-20261016-145723-529357-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left_observed-20261016-145723-529357-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left_observed-20261016-150204-535849-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left_observed-20261016-150204-535849-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left_observed-20261016-150204-535849-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left_observed-20261016-150204-535849-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left_plain-20261016-145723-529357-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left_plain-20261016-145723-529357-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left_plain-20261016-145723-529357-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left_plain-20261016-145723-529357-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left_plain-20261016-150204-535849-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left_plain-20261016-150204-535849-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_left_plain-20261016-150204-535849-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_left_plain-20261016-150204-535849-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_only-20261016-151025-546199.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_only-20261016-151025-546199.SAV) | `run-exp-ai-oct16` |
| [`reg_same_only_observed-20261016-151025-546199-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_only_observed-20261016-151025-546199-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_only_observed-20261016-151025-546199-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_only_observed-20261016-151025-546199-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_only_plain-20261016-151025-546199-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_only_plain-20261016-151025-546199-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_only_plain-20261016-151025-546199-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_only_plain-20261016-151025-546199-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right-20261016-145723-529357.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right-20261016-145723-529357.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right-20261016-150204-535849.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right-20261016-150204-535849.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right_observed-20261016-145723-529357-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right_observed-20261016-145723-529357-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right_observed-20261016-145723-529357-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right_observed-20261016-145723-529357-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right_observed-20261016-150204-535849-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right_observed-20261016-150204-535849-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right_observed-20261016-150204-535849-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right_observed-20261016-150204-535849-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right_plain-20261016-145723-529357-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right_plain-20261016-145723-529357-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right_plain-20261016-145723-529357-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right_plain-20261016-145723-529357-post.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right_plain-20261016-150204-535849-AUTO0734.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right_plain-20261016-150204-535849-AUTO0734.SAV) | `run-exp-ai-oct16` |
| [`reg_same_right_plain-20261016-150204-535849-post.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-ai-oct16/reg_same_right_plain-20261016-150204-535849-post.SAV) | `run-exp-ai-oct16` |

## Tactical target and draw attribution (2026-10-16)

No new binary artifacts were produced. The existing original corpus is in
[run-exp-battle-hook](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-hook).
The pinned private fixture mirror is `diegoami/ic2-test-fixtures` commit
`6319802a75067e7730e4f6a27dce3b4e296ddd9b`; its `battles/README.md` records
release mapping and CSV line endings. Intake checked all 318 hook hashes and the
following raw first-divergence boundaries against its `battles/SHA256SUMS`.

`mix-rg_s1_r5_hook_BATTLE06.SAV` is also an exact member of the published
[`b11-hook-batch-v2-mix.tar.gz`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-battle-hook/b11-hook-batch-v2-mix.tar.gz),
archive SHA256 `463596123364e6d6ac739bc6ab4e4f7e584d9501f9fdfbee01cae05063d9e020`.
The downloaded member matches the pinned fixture bytes. The start
`FLD-RG_0743_rome_army0_at_86_28.SAV` is already indexed above under battle-sweep.
Full text captures/inventory: ic2-conquest `586d361`,
`runs/experiments/data/run-exp-tactical25/`. These are old Wine originals plus
new model captures/x86 local probes; no native Windows confirmation.

| First differing boundary save (turn 0743) | SHA256 |
|---|---|
| [`ar-hc-three_s1_r5_hook_BATTLE14.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/ar-hc-three_s1_r5_hook_BATTLE14.SAV) | `642964ad85a2a197e00d14d2b8354cec27b5b71cbf748a609f81a5a4992015cf` |
| [`ar-hi-three_s2_r5_hook_BATTLE19.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/ar-hi-three_s2_r5_hook_BATTLE19.SAV) | `6a6fb4c7dae75cda7becfc4af259a1a1aa8b6c1a5fa29127847d7c3f2c98b655` |
| [`ar-hi-three_s3_r5_hook_BATTLE19.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/ar-hi-three_s3_r5_hook_BATTLE19.SAV) | `d1418830551c0efad887065e4b825b238be657f1d13bbf5fe4e0956d66c02718` |
| [`ar-lc-three_s2_r5_hook_BATTLE08.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/ar-lc-three_s2_r5_hook_BATTLE08.SAV) | `3e5e8efb1545187acc66c6e4629834b8bf4a970f512b023935364be08d468366` |
| [`ar-li-three_s1_r5_hook_BATTLE08.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/ar-li-three_s1_r5_hook_BATTLE08.SAV) | `65e1830ab838bbec2998d6cdcfae48e4644e15d6d9e834f945ff1963c17d4083` |
| [`ar-li-three_s2_r5_hook_BATTLE08.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/ar-li-three_s2_r5_hook_BATTLE08.SAV) | `7104c8cb9522c8b8c97d52b3b8c492944ac9470c4d36d2aa7ead2cd365b4be29` |
| [`ar-li-three_s3_r5_hook_BATTLE08.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/ar-li-three_s3_r5_hook_BATTLE08.SAV) | `885607aabc737d69fe197334278d4ae051d3ad2c025434154c568bfc77f73574` |
| [`hc-ar-three_s1_r5_hook_BATTLE16.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hc-ar-three_s1_r5_hook_BATTLE16.SAV) | `50e3991a64976a925b2fa7915ec502663a5de88ee3478de7027f81c7464d850d` |
| [`hc-ar-three_s3_r5_hook_BATTLE20.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hc-ar-three_s3_r5_hook_BATTLE20.SAV) | `4e84c1b531ea96947ec38db155fcd93b09de812140e9926d6ea6113e3589a45c` |
| [`hc-hc-three_s2_r5_hook_BATTLE11.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hc-hc-three_s2_r5_hook_BATTLE11.SAV) | `00b7a7aa63301b842d115931b9bf565f9ff8e5a84a79f4ea971802e830ff6a80` |
| [`hc-hi-three_s3_r5_hook_BATTLE08.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hc-hi-three_s3_r5_hook_BATTLE08.SAV) | `768e73258abfedec118549a1de7b840a11f814b5075dd12ca07cfc1d13143c02` |
| [`hi-ar-three_s1_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hi-ar-three_s1_r5_hook_BATTLE07.SAV) | `a760387bba1e63d310e7144c0c8e892a9e897bd4b0aa4047e5a6856646d78462` |
| [`hi-ar-three_s2_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hi-ar-three_s2_r5_hook_BATTLE07.SAV) | `90e2bc9f6b7e9f1aa616fde6337b1547df66ec6c0599db022b3d29e4fd4ba00e` |
| [`hi-ar-three_s3_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hi-ar-three_s3_r5_hook_BATTLE07.SAV) | `f6a3b63a071ba5a9ce50eceb46072032e2ef37459eadfd0e1dbd8db6824f468a` |
| [`hi-lc-three_s1_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hi-lc-three_s1_r5_hook_BATTLE07.SAV) | `7cff7f515f280deb1010654bb77acfe7857ac3b92f9fd444773c036b009f0d7d` |
| [`hi-li-three_s3_r5_hook_BATTLE06.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/hi-li-three_s3_r5_hook_BATTLE06.SAV) | `ade5261f08ed242a4a9bfb2a331fc290dc65d77d74d369ccb506f1613b7c4bd1` |
| [`lc-ar-three_s1_r5_hook_BATTLE09.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/lc-ar-three_s1_r5_hook_BATTLE09.SAV) | `aaf11f228ce731e7ebf502e66913a09d86ae1175e1732363dab71d27a422c334` |
| [`lc-ar-three_s2_r5_hook_BATTLE09.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/lc-ar-three_s2_r5_hook_BATTLE09.SAV) | `dbedbb6d956089bc8c37076c4c0978d0cf29a537808b5503dd9eff00c45edc20` |
| [`lc-hi-three_s1_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/lc-hi-three_s1_r5_hook_BATTLE07.SAV) | `af0e5fa239a8de87356748e283235cbd1b7f75b22f125faa4691856f5d2e2e31` |
| [`lc-hi-three_s2_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/lc-hi-three_s2_r5_hook_BATTLE07.SAV) | `e1d2eaf42a365af69fe9e01ce08b8b5d2f6fead5b7fdfd93c7cfce24d54184ea` |
| [`lc-li-three_s2_r5_hook_BATTLE11.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/lc-li-three_s2_r5_hook_BATTLE11.SAV) | `daffbc267add5e2bd830cc6b81477db076ea6c148a9b4f5cc34a02ce81faad34` |
| [`lc-li-three_s3_r5_hook_BATTLE08.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/lc-li-three_s3_r5_hook_BATTLE08.SAV) | `fa8bed462f3480d2a1f7b705163390628031161f713e0ec579f0db9cff80fb22` |
| [`li-ar-three_s2_r5_hook_BATTLE09.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-ar-three_s2_r5_hook_BATTLE09.SAV) | `24d24e378d16f215b56230a56c4d3335969a539c6456c455e31780527cc1895d` |
| [`li-hc-three_s1_r5_hook_BATTLE09.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-hc-three_s1_r5_hook_BATTLE09.SAV) | `48583435948db462e7ca4f63847a76d1fda5b8f707374606819343b64558bf8d` |
| [`li-hc-three_s3_r5_hook_BATTLE11.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-hc-three_s3_r5_hook_BATTLE11.SAV) | `9375c1e3698efbc2c38e50998d7463db9acd324b08384c21a3e603cc9e63e035` |
| [`li-hi-half-three_s1_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-hi-half-three_s1_r5_hook_BATTLE07.SAV) | `049e723fd9a1fc7b7f76aa965f9798deea14aaa491e8670406a23b82ee649439` |
| [`li-hi-half-three_s3_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-hi-half-three_s3_r5_hook_BATTLE07.SAV) | `543bdc8087bfbb203f8d42387a999709b3dc22f53c147dfa76c42920d1483458` |
| [`li-hi-one-three_s1_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-hi-one-three_s1_r5_hook_BATTLE07.SAV) | `46ce077ebc1eb51ddcdec31fb2f270bd26de64d9b902a80a60efc63897219bdb` |
| [`li-hi-one-three_s3_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-hi-one-three_s3_r5_hook_BATTLE07.SAV) | `f4d0957937872c90a594829111914bc667bf784fb818a86fda8588b5cd026c7a` |
| [`li-hi-three_s2_r5_hook_BATTLE07.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-hi-three_s2_r5_hook_BATTLE07.SAV) | `4306eb1e7efb3ff2d107ac045aab9b5ace074826bafe8519de8be8670b412537` |
| [`li-lc-three_s1_r5_hook_BATTLE08.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-lc-three_s1_r5_hook_BATTLE08.SAV) | `6fb505c9c49594623a90df25531e4afbcb64092e0e122c9020dd6c788617264c` |
| [`li-lc-three_s2_r5_hook_BATTLE10.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-lc-three_s2_r5_hook_BATTLE10.SAV) | `25472ca1829f34321f8755fe50e4001245b9b6b44157b87af3a02d5d81fcf727` |
| [`li-lc-three_s3_r5_hook_BATTLE08.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/li-lc-three_s3_r5_hook_BATTLE08.SAV) | `dffd4d8f09e245a65b5c790f2c0a2b24f18cd516b6cff950397ba003b0bf37f7` |
| [`mix-rg_s1_r5_hook_BATTLE06.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/mix-rg_s1_r5_hook_BATTLE06.SAV) | `de69151203cd4bb20c34a136b32a1ce68110ddc9fb2e0e685940a06eeb082ae9` |
| [`mix-rg_s2_r5_hook_BATTLE06.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/mix-rg_s2_r5_hook_BATTLE06.SAV) | `953a8c3941b5d523cc51ab9c131324eacad93b676a089a912c491a81b716db6d` |
| [`mix-rg_s3_r5_hook_BATTLE04.SAV`](https://github.com/diegoami/ic2-test-fixtures/blob/6319802a75067e7730e4f6a27dce3b4e296ddd9b/battles/hook/mix-rg_s3_r5_hook_BATTLE04.SAV) | `02aa2f0f9144259532bb1d81566fa027218fdee2cc3a96a5498e1003128f0add` |

## Tactical25 original decision trace (2026-10-16)

Pinned source: ic2-conquest `f872057ed455e977c33fc9ca2439b73a3a6f3c91`,
`runs/experiments/data/run-exp-tactical25-trace/`. All 40 local artifact hashes
match the pinned `SAVES.sha256`, release mapping and live release digests.
The 33 saves include starts; four EXEs and three buffers are linked for complete
recorder provenance. No binary is copied into this research tree.

Working alias `MIX-RG_start.SAV` is an unedited copy of already-indexed
`FLD-RG_0743_rome_army0_at_86_28.SAV`, hash
`39edecd1fa74776ef7ed817794b2f2bea951b6b2b36ef09ab42813208095f0ad`;
its three uniquely prefixed released copies below have the same bytes.
Both fresh runs' fifteen BATTLE files match the corresponding immutable legacy
mix-rg_s1 files byte-for-byte. In particular the new state-observer
`20261016-191329-1302174-BATTLE06.SAV` equals the previously indexed
`mix-rg_s1_r5_hook_BATTLE06.SAV`, turn 0743.

| Released artifact | Kind |
|---|---|
| [`20261016-190528-1258374-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE01.SAV) | save |
| [`20261016-190528-1258374-BATTLE02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE02.SAV) | save |
| [`20261016-190528-1258374-BATTLE03.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE03.SAV) | save |
| [`20261016-190528-1258374-BATTLE04.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE04.SAV) | save |
| [`20261016-190528-1258374-BATTLE05.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE05.SAV) | save |
| [`20261016-190528-1258374-BATTLE06.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE06.SAV) | save |
| [`20261016-190528-1258374-BATTLE07.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE07.SAV) | save |
| [`20261016-190528-1258374-BATTLE08.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE08.SAV) | save |
| [`20261016-190528-1258374-BATTLE09.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE09.SAV) | save |
| [`20261016-190528-1258374-BATTLE10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE10.SAV) | save |
| [`20261016-190528-1258374-BATTLE11.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE11.SAV) | save |
| [`20261016-190528-1258374-BATTLE12.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE12.SAV) | save |
| [`20261016-190528-1258374-BATTLE13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE13.SAV) | save |
| [`20261016-190528-1258374-BATTLE14.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE14.SAV) | save |
| [`20261016-190528-1258374-BATTLE15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-BATTLE15.SAV) | save |
| [`20261016-190528-1258374-Imperial.Conquest.2.tactical25.standard.exe`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-Imperial.Conquest.2.tactical25.standard.exe) | observer EXE |
| [`20261016-190528-1258374-MIX-RG_start.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-MIX-RG_start.SAV) | save |
| [`20261016-190528-1258374-hookbuf.bin`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-190528-1258374-hookbuf.bin) | raw recorder buffer |
| [`20261016-191329-1302174-BATTLE01.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE01.SAV) | save |
| [`20261016-191329-1302174-BATTLE02.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE02.SAV) | save |
| [`20261016-191329-1302174-BATTLE03.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE03.SAV) | save |
| [`20261016-191329-1302174-BATTLE04.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE04.SAV) | save |
| [`20261016-191329-1302174-BATTLE05.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE05.SAV) | save |
| [`20261016-191329-1302174-BATTLE06.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE06.SAV) | save |
| [`20261016-191329-1302174-BATTLE07.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE07.SAV) | save |
| [`20261016-191329-1302174-BATTLE08.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE08.SAV) | save |
| [`20261016-191329-1302174-BATTLE09.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE09.SAV) | save |
| [`20261016-191329-1302174-BATTLE10.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE10.SAV) | save |
| [`20261016-191329-1302174-BATTLE11.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE11.SAV) | save |
| [`20261016-191329-1302174-BATTLE12.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE12.SAV) | save |
| [`20261016-191329-1302174-BATTLE13.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE13.SAV) | save |
| [`20261016-191329-1302174-BATTLE14.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE14.SAV) | save |
| [`20261016-191329-1302174-BATTLE15.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-BATTLE15.SAV) | save |
| [`20261016-191329-1302174-Imperial.Conquest.2.tactical25.state.exe`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-Imperial.Conquest.2.tactical25.state.exe) | observer EXE |
| [`20261016-191329-1302174-MIX-RG_start.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-MIX-RG_start.SAV) | save |
| [`20261016-191329-1302174-hookbuf.bin`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-hookbuf.bin) | raw recorder buffer |
| [`20261016-191329-1302174-statebuf.bin`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-191329-1302174-statebuf.bin) | raw recorder buffer |
| [`20261016-210410-1249075-Imperial.Conquest.2.tactical25.standard.exe`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-210410-1249075-Imperial.Conquest.2.tactical25.standard.exe) | observer EXE |
| [`20261016-210410-1249075-MIX-RG_start.SAV`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/20261016-210410-1249075-MIX-RG_start.SAV) | save |
| [`state-observer-20261016-191329.exe`](https://github.com/diegoami/ic2-conquest/releases/download/run-exp-tactical25-trace/state-observer-20261016-191329.exe) | observer EXE |

## Foreign-city automatic resupply (2026-10-17)

For [the promoted report](reports/2026-10-17-foreign-city-automatic-resupply.md),
source is ic2-conquest merge `27488fa4fe2a1918eff4a66f3f21fe886a67a58b` ([PR93](https://github.com/diegoami/ic2-conquest/pull/93)).
Binary evidence is [release run-exp-resupply31](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-resupply31).
All 227 complete saves match both local SHA256 and GitHub asset digests at intake.
The retained zero-byte interrupted copy is not a valid save or release asset.

- [Packet selection and limits](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/data/run-exp-resupply31/README.md).
- [Full 56-case matrix](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/data/run-exp-resupply31/matrix-final.md),
  [canonical raw-save summary](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/data/run-exp-resupply31/summary-final-20261017.json),
  [58-input original-x86 audit](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/data/run-exp-resupply31/audit-final-20261017.json).
- [All complete bare filenames and SHA256](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/data/run-exp-resupply31/SAVES.sha256),
  [release verification](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/data/run-exp-resupply31/release-verified-final-20261017.json),
  [excluded interrupted copy](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/data/run-exp-resupply31/incomplete-artifacts.json).
- [Source ranges and caller inventory](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/data/run-exp-resupply31/complete-source-provenance.json)
  and [runners](https://github.com/diegoami/ic2-conquest/blob/27488fa4fe2a1918eff4a66f3f21fe886a67a58b/runs/experiments/resupply31).
- Research [raw-byte intake checker](../scripts/resupply31-intake-check.py) and
  [recorded result](data/resupply31-intake.json). It needs the pinned conquest text,
  external saves, live release/tree metadata and original dump, all outside research git.

Representative post saves (all turn **0734**; loaded/input partners and every other
case resolve via the manifest and matrix above):

| Case | Post save | Provenance / limit |
|---|---|---|
| land peace | `land-peace-20261017-082729-8913-post.SAV` | staged Wine, supply50→150/purse500→480 |
| embarked peace | `aboard-peace-20261017-083008-11228-post.SAV` | same army support fields; human-owned carrier |
| fleet peace | `fleet-peace-20261017-083008-11228-post.SAV` | supply50→150/purse500→480; condition94 unchanged |
| separated carrier | `aboard-carrier_far-20261017-084100-17426-post.SAV` | army(102,49), carrier(150,90); no synchronization claim |
| two providers | `land-two_foreign-20261017-084057-17118-post.SAV` | city88 then89; quantities5 then4; purse25→24 |
| above capacity | `fleet-above-20261017-084059-17272-post.SAV` | supply730→720/purse500→502; seller treasury−2 |
| hostile fleet | `fleet-war-20261017-084059-17272-post.SAV` | support unchanged; buyer treasury1000→−445 is a full-seat confound |

No native Windows confirmation. All other pending research requests retain their
own scope; these assets do not authorize build or T177 changes.

## Hostile-control recruitment ledger (2026-10-17)

For the [promoted report](reports/2026-10-17-hostile-control-recruitment-treasury-ledger.md),
source is conquest `main` merge `356171b0e27d6f188a9f45f60eceda277c5dbfd5`
([PR96](https://github.com/diegoami/ic2-conquest/pull/96)). All35 packet blobs
match the original reviewed experiment pin `4e4eed591ab1696e761a0cc9fafa6ba7ad50f178`.
The owner explicitly approved the source merge despite its NEUTRAL size-skipped
security scan; no successful scan is claimed. The
[publication receipt](data/resupply33-publication.json) preserves both pins.

- [Canonical packet README](https://github.com/diegoami/ic2-conquest/blob/4e4eed591ab1696e761a0cc9fafa6ba7ad50f178/runs/experiments/data/run-exp-resupply33/README.md),
  [summary](https://github.com/diegoami/ic2-conquest/blob/4e4eed591ab1696e761a0cc9fafa6ba7ad50f178/runs/experiments/data/run-exp-resupply33/summary-canonical-20261017.json),
  [all nine bare filenames and hashes](https://github.com/diegoami/ic2-conquest/blob/4e4eed591ab1696e761a0cc9fafa6ba7ad50f178/runs/experiments/data/run-exp-resupply33/SAVES.sha256),
  [release verification](https://github.com/diegoami/ic2-conquest/blob/4e4eed591ab1696e761a0cc9fafa6ba7ad50f178/runs/experiments/data/run-exp-resupply33/release-verification-20261017-1031.json).
- [Source ranges](https://github.com/diegoami/ic2-conquest/blob/4e4eed591ab1696e761a0cc9fafa6ba7ad50f178/runs/experiments/data/run-exp-resupply33/source-provenance-initial.json),
  [instruction bytes](https://github.com/diegoami/ic2-conquest/blob/4e4eed591ab1696e761a0cc9fafa6ba7ad50f178/runs/experiments/data/run-exp-resupply33/recruitment-disassembly-20261017.txt),
  [UI exception source](https://github.com/diegoami/ic2-conquest/blob/4e4eed591ab1696e761a0cc9fafa6ba7ad50f178/runs/experiments/data/run-exp-resupply33/ui-size-source-20261017.txt),
  [source-phase controls/runners](https://github.com/diegoami/ic2-conquest/blob/4e4eed591ab1696e761a0cc9fafa6ba7ad50f178/runs/experiments/resupply33).
- [Research checker](../scripts/resupply33-intake-check.py) and
  [intake result](data/resupply33-intake.json). It needs external pinned EXE/DAT/dump,
  source text, fresh/legacy saves and live release/tree metadata; none of those
  original binaries are stored in research git.

All rows are turn **0734**. Legacy input/loaded/post files resolve through
[run-exp-resupply31](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-resupply31);
fresh replay files resolve through
[run-exp-resupply33](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-resupply33).
Append `-input.SAV`, `-loaded.SAV`, `-post.SAV` to a legacy stem. Fresh stems have
`-loaded.SAV`, `-auto.SAV`, `-post.SAV`. Nine new and nine selected legacy saves
were independently hashed against their release digests; all three loaded/post
replay pairs are byte-identical. The historical31 matrix remains unchanged.

| Case | Legacy stem | Fresh replay stem |
|---|---|---|
| land | `land-war-20261017-083008-11228` | `land-war-20261017-083008-11228-replay-20261017-101820-85339` |
| aboard | `aboard-war-20261017-084100-17426` | `aboard-war-20261017-084100-17426-replay-20261017-101914-87061` |
| fleet | `fleet-war-20261017-084059-17272` | `fleet-war-20261017-084059-17272-replay-20261017-101915-87214` |

All four original phase boundaries are emulator controls initialized with fresh
**pre-click** runtime observations, not Wine phase-entry captures or a recovered
legacy seed. The canonical three `phases-*-byte-audit-20261017.json` records retain
the next-human Bithynia UI mismatch. Input→loaded UI normalization in Armenia is
also explicit in the independent intake result. No native/natural/full-world or
complete-turn equivalence, foreign supply charge, build/T177 or fixture change.

## SAV export safety packet (2026-10-17)

The [pinned ic2-conquest packet](https://github.com/diegoami/ic2-conquest/blob/ac958a0fa58984098641a7992a42d0fbf517d473/runs/experiments/data/run-exp-sav-export37/README.md) contains the authoritative `nation-matrix-v2.csv`, source inventory/extracts, public-save scalar audit, DAT profile, ten bounded original-x86 controls and validation receipt. `nation-matrix-initial.csv` is a retained draft and is not the matrix cited by the [promoted report](reports/2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md). Fourteen already-public saves were sampled; the report names five examples, whose save-table rows above provide retrieval links. There are no new save release assets, candidate exports, private owner inputs or Windows outputs from this packet.

## Bound-tax public source pointer (2026-10-18)

| Save | Public retrieval / SHA-256 | Scope |
| --- | --- | --- |
| [`det-AUTO0721-clock.SAV`](https://github.com/diegoami/ic2-conquest/blob/88ac03972d9f8d972fd7a72344c7406a4b4f0c96/saves/det-AUTO0721-clock.SAV) | `ee4550c1094847310fe3eafaa8077481474d0ef3b4a5259acd397f4a74b862eb` | Existing public turn-0721 clock fixture; source for two in-memory tax projections in the [tax profile report](reports/2026-10-18-sav-export-bound-tax-subset-and-binary-alias-evidence.md). Independently retrieved/hashed at intake; no new save output or release. |


## Native Windows bound-tax candidates (2026-10-18; promoted 2026-10-21)

For the [native report](reports/2026-10-18-sav-export-original-windows-tax-candidates.md),
source is ic2-conquest main `7fe20bedba0b9cdbb012b1b348c96507f6a65768`,
original [PR104](https://github.com/diegoami/ic2-conquest/pull/104) merge
`c8193ca1ebbb8f024963c4961bac8be02e940542`.
**These are private native artifacts, not downloadable release assets.** No
SAV/PNG/original bytes are stored or uploaded here. Bare basenames resolve to
the committed scalar/hash receipts below; private location/access must be
coordinated separately. Fresh intake rehashed all21manifested SAVs and38captures using owner-provided
readable copies, then reran the unchanged no-game validator. Original writer
folder/manifests remain unavailable; retained transport bytes match the fixed
writer candidate digests. The [sanitized receipt](data/sav37-native-intake.json)
records both private-copy validation and separate metadata consistency.

| Artifact basename / case | SHA-256 | Scalar provenance / access |
|---|---|---|
| `t184-tax-1-n0-0.SAV` / Rome tax 0 | `5e85a985382dc56ae964889ed01d4fda56b0e2414ccaede5e18d03b3bd2a314c` | [v3 manifest](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/native-packet-validation-v3.json), case 1; retained transport bytes freshly hash-verified; no download |
| `t184-tax-thracia-n15-40.SAV` / Thracia tax 40 | `2afa2d64170a63fefbf12c5678700a02024f01eb0f682a0cbc7efffa63b7288f` | same v3 manifest, case 2; retained transport bytes freshly hash-verified; no download |
| `t184-tax-rome-n0-30.SAV` / Rome tax 30 | `5d82f47aa77f2736afddeac8c23754305455afa7e524636b98d12b4c2a88669a` | same v3 manifest, case 3; retained transport bytes freshly hash-verified; no download |

[Packet README](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/README.md),
[three completion/control records](https://github.com/diegoami/ic2-conquest/tree/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native),
and [read-only validator](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/sav_export37_native/verify_native_packet.py)
retain source/candidate/input/load/order/post-turn/reopen hashes. Initial/save
and post-turn/reopen pairs agree in all three recorded cases. Controls 2/3
are exact candidate matches; control 1 retains area-map and earlier baseline
Information-window geometry differences. No capture image or private path is
reproduced. Internal callback traces remain UNVERIFIED, UNKNOWN31 unknown;
this 3/3 tax-only result is zero of twelve native-JSON conversions.


## Remake ↔ original Wine conversion (#151, 2026-10-23)

[Consolidated report](reports/2026-10-23-remake-original-save-conversion-roundtrips.md),
conquest [PR #152](https://github.com/diegoami/ic2-conquest/pull/152), immutable
source `4ca3afa04c3eb8454c63ed6a4984f5564e8e0496`.
[Tracked manifests, commands and receipts](https://github.com/diegoami/ic2-conquest/tree/4ca3afa04c3eb8454c63ed6a4984f5564e8e0496/runs/experiments/data/run-exp-sav-conversion-roundtrip).

The private [Drive folder](https://drive.google.com/drive/folders/1OQWVtWzeN6k-_EgfU_3U_vFa4MjmXfqv)
holds the complete [batch2 archive](https://drive.google.com/file/d/10BGy85kM1jUA7iXCdvwzkYXcc1z6fZzQ/view):
`batch2-complete.tar.gz`, 3,118,135 bytes / 85 files, SHA256
`c21c8607eb1def47b7ea592d2494dd5b9a72ef9dea0cf1342b26205b94fdd91f`.
The earlier `batch1-conversions.tar.gz`, 3,007,535 bytes / 79 files, SHA256
`819dc8fc5891487893bdebba32b9fec21bdb99711cc2559cc76e5c70f36e7058`,
is retained too. Research freshly verified both local archives, every tar member and
all 164 manifest entries; many entries occur in both archives. No Drive download/hash
readback was performed by research. No release or original EXE/DAT is included.

| Case / runtime | Original-produced save basenames | What they bind |
| --- | --- | --- |
| A / unmodified EXE, Wine | `P151AI.SAV`, `P151AO.SAV`, `P151AR.SAV` | Initial generated remake state: immediate save, tax26, fresh-process reopen/resave |
| B / unmodified EXE, Wine | `P151BI.SAV`, `P151BO.SAV`, `P151BR.SAV` | Queued HI and fleet construction, same three boundaries |
| C / unmodified EXE, Wine | `P151CI.SAV`, `P151CO.SAV`, `P151CR.SAV` | Six remake turns later |
| D / unmodified EXE, Wine | `P151DI.SAV`, `P151DO.SAV`, `P151DR.SAV` | Twelve remake turns later |
| E / unmodified EXE, Wine | `P151EI.SAV`, `P151EO.SAV`, `P151ER.SAV` | Twenty-four remake turns later |
| F / unmodified EXE, Wine | `P151FI.SAV`, `P151FO.SAV`, `P151FR.SAV` | Explicitly synthetic carrier/army linkage |
| G / instrumented seed EXE, Wine | `P151GI.SAV`, `P151GO.SAV`, `AUTO0721.SAV`, `P151GT.SAV`, `P151GR.SAV` | B input repeated, tax26, one End turn, explicit save, fresh-process reopen/resave |
| A–G / remake re-exports | `RETURNA.SAV`, `RETURNB.SAV`, `RETURNC.SAV`, `RETURND.SAV`, `RETURNE.SAV`, `RETURNF.SAV`, `RETURNG.SAV` | Original results imported/reloaded/resumed, accepted tax27, re-exported; all policy passes |

Bare names resolve through the pinned complete manifest to their case directory in
the archive. The JSON snapshots are newly generated experimental states, not the
owner's twelve private preflight inputs. Save bytes, native JSON and screenshots
remain outside research Git. The [research receipt](data/conversion151-intake-v1.json)
contains scalar checks only; the report preserves normalization, RNG and runtime limits.


## Broad strategic conversion (#153, 2026-10-23)

[Report](reports/2026-10-23-broad-save-conversion-matrix.md), conquest
[PR #155](https://github.com/diegoami/ic2-conquest/pull/155), source
`83d52d2bad99ad8e3870f498cd7d939e0354f482`. The
[complete per-case coverage CSV](https://github.com/diegoami/ic2-conquest/blob/83d52d2bad99ad8e3870f498cd7d939e0354f482/runs/experiments/data/run-exp-sav-conversion-broad153/coverage-final.csv)
and [packet/manifests](https://github.com/diegoami/ic2-conquest/tree/83d52d2bad99ad8e3870f498cd7d939e0354f482/runs/experiments/data/run-exp-sav-conversion-broad153)
resolve every selected original save and its versioned case. There are 77 round
trips but only 53 distinct exported input SAVs; cases intentionally reuse states.
These are generated/synthetic inputs, not the owner's twelve-save set or #1355 files.

Complete [Drive archive](https://drive.google.com/file/d/16xF3L8qDSFcotMLhA5yOon2Rqm56gJXc/view):
`batch-final.tar.gz`, 21,030,521 bytes / 900 files, SHA256
`35db99998eb18955469200eb3af755d0abc6cf980cc5f9dd38a13f43905688c1`.
The [Drive folder](https://drive.google.com/drive/folders/1PwRAw0xg4WKp5MpgpcRO3Fg6B4H5dnmn)
also retains earlier batches. The valid third archive is `batch-03-complete.tar.gz`
on Drive (`batch-03.tar.gz` in the local manifest); the earlier partial upload is
marked `INCOMPLETE-do-not-use`. Research verified all four complete local archives,
2,516 tar-member entries and the 2,754-check audit. Entries overlap across batches;
these are not unique-save counts. Drive copies were not downloaded by research.

| Cited original save basename | Case / scope |
| --- | --- |
| `Q15359R.SAV` | F39 naval battle, instrumented original, turn0720; continuation, not equal combat outcome |
| `Q15360R.SAV` | F40 siege/capture, instrumented original, turn0720 |
| `Q15361R.SAV` | F41 aftermath of a native field battle, original turn0721; not tactical outcome parity |
| `Q15357R.SAV` | F37 two-human handoff, instrumented original |
| `Q15375R.SAV` | F54 reversed cargo arrays and landing, turn0720 |
| `Q15377R.SAV` | F56 fleet removal before a live cargo carrier; reciprocal army13 link survives, turn0720 |

All source/return exports, original immediate/order/reopen saves and screenshots
remain outside research Git. The shared [scalar intake receipt](data/conversion153-battle1355-intake-v1.json)
records exact comparison/coverage/audit reproduction and 154 fresh policy passes.

## Private owner battle #1355 (2026-10-23)

[Focused report](reports/2026-10-23-ptolemaic-seleucid-computer-general-gap1355.md),
conquest [PR #156](https://github.com/diegoami/ic2-conquest/pull/156), source
`12ae80280609d8d40ec3eca942a7a893af3e5161`. The
[public-safe aggregate audit and probe code](https://github.com/diegoami/ic2-conquest/tree/12ae80280609d8d40ec3eca942a7a893af3e5161/runs/experiments/data/run-exp-battle1355)
and research's shared scalar receipt contain no owner input paths, input hashes,
full state, screenshot or trace. Private access requires owner coordination; none
of that evidence is in #153's Drive bundle or a public release.

Research checked private preservation/export equality, complete safe-audit
reproduction, controlled entry fields, repeated control state and the original
result screenshot against terminal memory. The battle completed; the recorder
failed after its battle flag cleared. No final original SAV/reopen is claimed.
Wine only; no exact first original instruction, cause, fix or Windows acceptance.


## Later-pass iteration and faithful-general candidate (#157, 2026-10-23)

[Research report](reports/2026-10-23-battle-general-later-pass-iteration1355.md),
source conquest [PR #161](https://github.com/diegoami/ic2-conquest/pull/161),
`b7f11a3ff9b2f93e111c5ea13b6b66e919cc6688` (including earlier PR #159).
[Original observer/pilot packet](https://github.com/diegoami/ic2-conquest/tree/b7f11a3ff9b2f93e111c5ea13b6b66e919cc6688/runs/experiments/data/run-exp-battle-parity157)
and [compiled candidate packet](https://github.com/diegoami/ic2-conquest/tree/b7f11a3ff9b2f93e111c5ea13b6b66e919cc6688/runs/experiments/data/run-exp-faithful-general157)
pin the scripts, manifests, source/assembly identities and scalar checks.

| Private Drive retrieval | Bytes / files | SHA256 |
| --- | --- | --- |
| [reference-batch01.tar.gz](https://drive.google.com/file/d/1q-BM_9QjvpvLDCu-TYSi6wm4xuY_J6Uh/view) | 1,419,660 / 58 | `5feaf72645a0d93eea1681368c6d9eea0b339892edcf1ff8902e01b1e9d07ddd` |
| [pilot-semantic-batch02.tar.gz](https://drive.google.com/file/d/1CKvkjvsykKXP4q9SS9APbiOzY1ZOHjuW/view) | 7,038,349 / 316 | `e0f6d4976054a3ccdf3144c2d9eb85cd1cb797c1e46250a870eb414395a238d8` |
| [faithful-engine-candidate-v1.tar.gz](https://drive.google.com/file/d/1pTuqmpNKd4-uhHW9wAhcknJ_n5BQA6aH/view) | 600,501 / 8 | `7811e54a7f5e1e425dbec0252a2a6266330f57be8d5c286cce023ad897b0c84b` |

Research rehashed all local archive bytes and all 382 members. The first two
contain public-reference/synthetic-pilot saves and logs, not owner evidence or
original EXE/DAT/prefixes. `BATTLE01.SAV` onward resolve by the case folders in
the manifests; the reference is the already indexed turn0743 fixture. The
candidate contains compiled remake engine/data and regression/replay tools,
not a deployed game; shared engine DLLs must accompany the extracted tool DLLs.
Drive metadata readback is upstream; no remote download/digest claim is added here.

Owner-derived turn0756 saves, fresh-reopen pairs, original observations and full
native replay outputs remain private and require owner coordination. No individual
owner hash or input path is reproduced. New seed1 owner controls and the earlier
historical natural-RNG reproduction are different evidence streams; the latter
keeps its missing-field assumptions. Research's
[scalar receipt](data/faithful157-intake-v1.json) records fresh offline validation,
including entire14-control verification equality and recorder checks, without
publishing private traces. No new Wine/original run, Windows validation, full318
acceptance, strategic copy-in/writeback validation or production merge is claimed.


## Seed2 Walk target lifetime (#1377, 2026-10-23)

[Research report](reports/2026-10-23-seed2-walk-captured-target1377.md), conquest
[PR #165](https://github.com/diegoami/ic2-conquest/pull/165), merged source
`e1a943d5f9de8b88787112f137ad8053a699e6e0`.
[Evidence/source patch](https://github.com/diegoami/ic2-conquest/tree/e1a943d5f9de8b88787112f137ad8053a699e6e0/runs/experiments/data/run-exp-battle-residual157)
and [original semantic records](https://github.com/diegoami/ic2-conquest/tree/e1a943d5f9de8b88787112f137ad8053a699e6e0/runs/experiments/data/run-exp-battle-parity157/seed2-residual-v1)
retain the baseline, incomplete and complete controls. The two fixture aliases
`mix-rg_s2_r5_hook` and `gate2_s2a` share18boundary saves andpost exactly;
they do not count as two independent original trajectories.

The [Drive folder](https://drive.google.com/drive/folders/1_NkvDEBYL1IO_2uPGPp5TffTuRHM7oxs)
holds three explicitly selected bundles:

| Archive | Bytes / members | SHA256 |
| --- | --- | --- |
| `seed2-semantic-batch01.tar.gz` | 562,897 / 22 | `a589e6875625aeb620d1a2572bb9da81f8fb98a1cd6c7a01a2118e21d1d94325` |
| `cached-live-tools-batch02.tar.gz` | 4,371,549 / 40 | `a02049656087296f8d1ef9885a626fe26eabc32c3a7c8845959193aebdde5ad0` |
| `fixed-corpus-tools-batch03.tar.gz` | 3,186,327 / 30 | `ba996c8328fecb9636f935278d71abee8f1c028c0f0454ddca03dbc2520bae3d` |

Research verified all local archive bytes and92members, not a remote download.
The original bundle resolves `BATTLE01.SAV` through `BATTLE18.SAV` under the
seed2 case folder and the fresh `seed2-residual-v1-AFTER.SAV` /
`seed2-residual-v1-REOPEN.SAV` pair. The strategic start is the already indexed
`FLD-RG_0743_rome_army0_at_86_28.SAV`, turn0743, fixture revision6319802.
Tool bundles contain compiled remake/test/replay dependencies, not a deployed game.
Original EXE/DAT, the full recovered private corpus, owner inputs/hashes and owner
replays are excluded. Those private inputs require separate owner coordination.

The [scalar intake receipt](data/walk1377-intake-v1.json) records exact full-corpus
summary/row reproduction, five fixed-series and five regression controls,49Walks,
178actions, the prior14controls,27upstream movement tests and the325draw/18SAV
recorder gate. Strict state/post comparison follows the named upstream helpers;
it is not every hidden runtime field, whole-file export identity or Windows
acceptance. No fixture, known-failure registry or sibling source was changed.


## Owner strategic destination/routing (#1388, 2026-10-24)

[Report](reports/2026-10-24-seleucid-strategic-target-routing1388.md), conquest
[PR167](https://github.com/diegoami/ic2-conquest/pull/167), original merge
`889557fa2d8f1dd6f36bc5ef3a06bcaf3532082c`, reviewed in source main
`363a9069089bd400c6905f3b93975162395031b3`.
[Public scalar audit/source/build records](https://github.com/diegoami/ic2-conquest/tree/363a9069089bd400c6905f3b93975162395031b3/runs/experiments/data/run-exp-seleucid1388)
contain no owner inputs or full RAM/logs. Private turn0755→0756 before/after pairs,
pre-walk RAM and complete original/native diagnostics require owner coordination;
no public binary archive or new owner release exists. The three same-seed runs
are observer controls on one owner trajectory, not independent scenarios.

Research replays the original helpers from that captured RAM and reproduces the
complete safe audit, full656-byte post-walk record and21paired steps. Private
input/save hashes, paths and full state are excluded from the
[shared scalar receipt](data/strategic171-intake-v1.json). No new original game,
full-turn RNG parity, deployed correction or Windows result is claimed.

## Generated strategic fidelity pilot (#171, 2026-10-24)

[Report](reports/2026-10-24-strategic-fidelity-pilot171.md), conquest
[PR172](https://github.com/diegoami/ic2-conquest/pull/172), source
`363a9069089bd400c6905f3b93975162395031b3`.
[Per-case declarations/audits](https://github.com/diegoami/ic2-conquest/tree/363a9069089bd400c6905f3b93975162395031b3/runs/experiments/data/run-exp-strategic-fidelity)
resolve the generated cases and original turn0720→0721 before/after files.
Bare examples: `SF-N-rome-hook-v1-after.SAV`,
`SF-L-ptolemaic-isolated-hook-v1-after.SAV`. The pattern
`SF-<case>-hook-v1-before.SAV` / `SF-<case>-hook-v1-after.SAV` and the two `plain-v1`
control pairs resolve through the manifests, rather than an owner-input list.

Private [Drive folder](https://drive.google.com/drive/folders/1gNiyzqi7RbgV0U4AJ5xwiYeDzK58H8-i):

| Archive | Bytes / members | SHA256 |
| --- | --- | --- |
| [pilot-evidence-batch01.tar.gz](https://drive.google.com/file/d/17WwEnBzQTlrOgJ-n7bTbBq7jwjEKLzRD/view) | 9,008,591 / 455 | `03f77f01cf23cac83cd86598115aa482f2903826efb525bbb719e8222cbf4f24` |
| [isolated-scarcity-and-tools-batch02.tar.gz](https://drive.google.com/file/d/1cF2nLkQPvkTMl98UIuG7lPm2VEqr3v1z/view) | 1,301,860 / 42 | `e3dfd26a4607d20832790f6e139daec5c10543734971c560f79550e500c519cc` |
| [terrain-sidecars-batch03.tar.gz](https://drive.google.com/file/d/1ICs45mHD4lvbV7Utol6H-AQAv5VDGw5D/view) | 12,551 / 2 | `d52e297b3211890af5c51dc917c2cb0d7a3c9d71419cd2012e45ef1c84b2d620` |
| [geometry-audit-tools-batch04.tar.gz](https://drive.google.com/file/d/1k5tbljKOYEJX6McF4bMepmUQLB0yoll9/view) | 601,045 / 5 | `f0b92b307836a78e9c7017762dd99f20ec7fd48588ec3da7ab94e6163bac8613` |

Research rehashed/recovered all504members, checked exact archive inventories and
reran retained compiled tools. All three modes match over112states; the recovered
geometry tool reproduces all112rows. Batch02 `tools-v7` supersedes batch01's
initial tool; batch03's terrain sidecars and batch04 geometry tool are required.
The first failed sidecar recovery remains recorded. These bundles contain generated
RAM/diagnostic containers, not owner1355/1388 inputs or original EXE/DAT/runtime.
RAM-projection SAVs are synthetic containers, never original Save As evidence.
Local archive verification adds no remote-download digest claim. Eleven distinct
inputs do not establish full greedy/global RNG/strategic or Windows equivalence.


## Synthetic fleet-phase controls (#174, 2026-10-24)

[Report](reports/2026-10-24-strategic-fleet-controls174.md), conquest
[PR179](https://github.com/diegoami/ic2-conquest/pull/179), source
`8d975efddd66fd81371991936a7fd0cbc58016be`.
[Manifest/source/results](https://github.com/diegoami/ic2-conquest/tree/8d975efddd66fd81371991936a7fd0cbc58016be/runs/experiments/data/run-exp-strategic-fleet)
resolve fourteen cases, including `stored-a` and `stored-b`. Each `pre-move.SAV`
is a synthetic diagnostic container; it is not an original Save As or a new played
turn. The clock field is0720 from the generated pilot snapshot lineage. The first
original movement call is intercepted before executing movement.

Private [Drive folder](https://drive.google.com/drive/folders/1WtM93OfebUVt7vkA1EsWAsSnpWeGVdk8):
`fleet-controls-batch01.tar.gz`,2,094,486bytes/76members, SHA256
`9262baa50a70ae5b4fb0dcfffc8317687e173ad01a4c14a9b7629afe8a94682f`.
Research rehashed all local members, checked the exact inventory, and recovered
the bundle into a new tree. Recovered and fresh-input compiled native tools
reproduce all14rows exactly. There is no remote-download digest claim.

Inputs are generated RAM/SAV/expected-JSON controls, native data/terrain sidecars
and compiled probe/Engine/Data tools. Original EXE/DAT, runtime/credentials and
owner1355/1388 inputs/traces are excluded. The [scalar intake receipt](data/fleet174-intake-v1.json)
records original phase/scorer reproduction,3,568fleet/relation gates and the
four-byte stored-route proof. Native state/proposal hashes refer to synthetic
controls, not owner preflight saves. Proposed marches are not accepted actions;
no naval combat, full fleet/global RNG or native Windows equivalence is claimed.


## Accepted fleet movement and army navigation (#174/#187, 2026-10-24)

Reports: [fleet accepted actions](reports/2026-10-24-fleet-accepted-movement174.md),
[army navigation](reports/2026-10-24-army-navigation-rule187.md).
Common source pin `1525f3985cc54834c5855055599188197c9ec4d4`; [fleet manifest and case ledgers](https://github.com/diegoami/ic2-conquest/blob/1525f3985cc54834c5855055599188197c9ec4d4/runs/experiments/data/run-exp-fleet-actions174/),
[navigation tables, source ledger and scalar controls](https://github.com/diegoami/ic2-conquest/blob/1525f3985cc54834c5855055599188197c9ec4d4/runs/experiments/data/run-exp-navigation187/).
Generated before/after Save As names include `FA174-live-rom-hook-v1-before.SAV`
and `FA174-live-rom-hook-v1-after.SAV`, with matching `plain-v1` counterparts.
These four files describe one generated Rome trajectory, not independent campaigns.
Other synthetic projected SAVs in the manifest are diagnostic containers.

Private [Drive folder](https://drive.google.com/drive/folders/19FVgahM2dSCOBxYyHV0ZR2P4TEyU2d5D):
[fleet-actions-batch01.tar.gz](https://drive.google.com/file/d/1fFCIu5lKk3LuUO-ILGSI9FR8UYa7055d/view),
8,322,493 bytes / 466 members, SHA256
`3189e5084511e54e926c74222e766658f6e8c4d2aef0a3f12c1e93662deabecd`.
Research checked the local archive hash, every member hash and exact inventory,
recovered it into a new tree, and reproduced all 33 native path results byte for
byte. No remote-download digest claim. Generated evidence/compiled probes are
included; original assets, runtime, credentials and owner inputs are excluded.

Navigation's static table extraction uses separately retained original assets
and generated pilot RAM. Public interpreted tables are not a binary release.
The final private #1388 regression remains private and is represented only by
its safe audit; no owner input names, hashes, RAM or complete traces are indexed.
The [research scalar receipt](data/actions-navigation187-intake-v1.json) records
fresh instruction/native checks and the exact observer-only trace difference.
No new original game, universal caller contract, global RNG or Windows claim.


## Garrison/mercenary caller guards (#187 follow-up, 2026-10-24)

[Report](reports/2026-10-24-garrison-mercenary-caller-guards187.md), conquest
[PR194](https://github.com/diegoami/ic2-conquest/pull/194), source
`0cda6c4417202d39e848ab00569a61f004d7c9ff`.
[Public ledgers/source provenance](https://github.com/diegoami/ic2-conquest/blob/0cda6c4417202d39e848ab00569a61f004d7c9ff/runs/experiments/data/run-exp-navigation187-callers/)
identify 24 isolated, 24 parent, 32 offer-history and eight progress controls.
Their bare `before.SAV` / `after.SAV` citations resolve through each ledger's
case and private group (`controls-v1`, `parent-v1`, `history-v1`, `progress-v1`).
These are generated turn-0720 diagnostic containers, not original Save As files,
new played games or owner #1355/#1388 inputs. No public binary archive is asserted.

Research regenerated all 88 controls in a new private tree and matched every
public result field. The fresh verifier proves 88 complete game-RAM/stack
observer/plain identities and 20 input pairs differing only in the mercenary
troop WORD at 49DA18. Its summary/paired/identity outputs equal upstream v3.
The [safe receipt](data/navigation187-callers-intake-v1.json) publishes counts,
original asset identity and scope only. Generated raw RAM/SAV/full traces and
private hash manifests remain private; no native caller or whole-turn claim.
