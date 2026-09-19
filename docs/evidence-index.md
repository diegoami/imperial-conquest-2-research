# Evidence index

Every save, screenshot and recording the reports cite, and the release that holds it.

The reports cite **bare filenames** — `11_supply.sav`, `1_rome_270_winter_7.sav` — never paths, because the binaries have never been in a repository and never will be. This file is what turns such a citation into something retrievable.

The originals live in the private repository [`diegoami/imp_conquest_original`](https://github.com/diegoami/imp_conquest_original), organised as **one release per play-through**. Nothing here is committed to this repository or to the build repository: the game files, saves, screenshots and recordings stay out of both, and this index is a pointer, not a copy.

## The releases

| Release | What it is | Saves | Screenshots | Recordings |
|---|---|---|---|---|
| [`run-1-rome`](https://github.com/diegoami/imp_conquest_original/releases/tag/run-1-rome) | Run 1 — Rome (270 BC) | 16 | 5 | 8 |
| [`run-1-cartago`](https://github.com/diegoami/imp_conquest_original/releases/tag/run-1-cartago) | Run 1 — Carthage (271 BC) | 10 | 2 | 0 |
| [`run-1-thracia`](https://github.com/diegoami/imp_conquest_original/releases/tag/run-1-thracia) | Run 1 — Thracia (271 BC) | 13 | 0 | 0 |
| [`legacy-probes`](https://github.com/diegoami/imp_conquest_original/releases/tag/legacy-probes) | Legacy probes | 15 | 25 | 0 |

### Which release to reach for

- **[`legacy-probes`](https://github.com/diegoami/imp_conquest_original/releases/tag/legacy-probes)** holds the **most-cited files in this repository**. A report citing a bare number — `7.sav`, `11_supply.sav`, `12_rom_a.sav` — means this release. Its `11`/`12` chain is a sequence of **single documented actions**, so a byte difference there is attributable to one change in a way a turn step never is.
- **[`run-1-rome`](https://github.com/diegoami/imp_conquest_original/releases/tag/run-1-rome)** is the only run with **recordings and written per-turn observations**, so it is the only place a formula can be checked against a stated player intent rather than a byte difference alone.
- **[`run-1-thracia`](https://github.com/diegoami/imp_conquest_original/releases/tag/run-1-thracia)** is the **densest uninterrupted series** — twelve consecutive two-week steps, no gaps, no branches — and so the right one for anything verified turn over turn. It has **no notes**: it shows state, not intent.
- **[`run-1-cartago`](https://github.com/diegoami/imp_conquest_original/releases/tag/run-1-cartago)** is small but holds a **one-action save pair** (`spring_1` → `spring_1b`, a single fleet move) within the same turn.

## Three things that will mislead you if you do not know them

**1. A `_b` suffix is a branch, not a later turn.** `1_rome_270_winter_7` has two successors: `winter_9` (where the battle froze, four recordings) and `winter_7_b` → `winter_9_b` → `winter_11` (the same battle replayed on auto, no freeze). `winter_9` and `winter_9_b` are **two outcomes of the same week reached by different routes** — diffing them as consecutive turns produces nonsense. The `_b` chain is the one that continues.

**2. Some cited saves do not exist.** `1_rome_270_summer_9` and `summer_11` were never kept, and `1_rome.txt` says so; their events are documented but no save backs them. `1_cartago_271_spring_3` has a **screenshot but no save**. And the flat numbering has always skipped `2.sav` and `3.sav` — nothing is missing.

**3. GitHub rewrites spaces in asset names as dots.** A recording stored as `bandicam 2026-09-12 23-56-28-394.mp4` downloads as `bandicam.2026-09-12.23-56-28-394.mp4`. The **Asset** column below gives the name as it downloads.

## Saves

`cites` counts the reports in this repository that name the file — a rough guide to how load-bearing it is, not a quality judgement.

| Save | Release | Cites |
|---|---|---|
| [`11_supply.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/11_supply.sav) | `legacy-probes` | 9 |
| [`1_rome_270_winter_7.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_winter_7.sav) | `run-1-rome` | 7 |
| [`7.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/7.sav) | `legacy-probes` | 6 |
| [`11.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/11.sav) | `legacy-probes` | 5 |
| [`1_rome_270_winter_9.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_winter_9.sav) | `run-1-rome` | 5 |
| [`8.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/8.sav) | `legacy-probes` | 5 |
| [`1.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/1.sav) | `legacy-probes` | 4 |
| [`11_ptol.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/11_ptol.sav) | `legacy-probes` | 4 |
| [`12_rom_a.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/12_rom_a.sav) | `legacy-probes` | 4 |
| [`1_rome_270_summer_7.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_summer_7.sav) | `run-1-rome` | 4 |
| [`1_rome_270_winter_1.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_winter_1.sav) | `run-1-rome` | 4 |
| [`1_rome_270_winter_11.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_winter_11.sav) | `run-1-rome` | 4 |
| [`10.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/10.sav) | `legacy-probes` | 3 |
| [`1_rome_270_winter_3.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_winter_3.sav) | `run-1-rome` | 3 |
| [`1_rome_270_winter_7_b.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_winter_7_b.sav) | `run-1-rome` | 3 |
| [`1_rome_270_winter_9_b.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_winter_9_b.sav) | `run-1-rome` | 3 |
| [`4.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/4.sav) | `legacy-probes` | 3 |
| [`9.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/9.sav) | `legacy-probes` | 3 |
| [`12_mac.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/12_mac.sav) | `legacy-probes` | 2 |
| [`12_ptol.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/12_ptol.sav) | `legacy-probes` | 2 |
| [`1_rome_270_autumn_1.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_autumn_1.sav) | `run-1-rome` | 2 |
| [`1_rome_270_autumn_5.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_autumn_5.sav) | `run-1-rome` | 2 |
| [`1_rome_270_autumn_7.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_autumn_7.sav) | `run-1-rome` | 2 |
| [`1_rome_270_autumn_9.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_autumn_9.sav) | `run-1-rome` | 2 |
| [`1_rome_270_winter_5.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_winter_5.sav) | `run-1-rome` | 2 |
| [`1_thracia_271_spring_11.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_spring_11.sav) | `run-1-thracia` | 2 |
| [`12_ptol_b.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/12_ptol_b.sav) | `legacy-probes` | 1 |
| [`1_cartago_271_spring_1.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_spring_1.sav) | `run-1-cartago` | 1 |
| [`1_cartago_271_spring_1b.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_spring_1b.sav) | `run-1-cartago` | 1 |
| [`1_cartago_271_summer_9.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_summer_9.sav) | `run-1-cartago` | 1 |
| [`1_rome_270_autumn_11.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_autumn_11.sav) | `run-1-rome` | 1 |
| [`1_rome_270_autumn_3.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_autumn_3.sav) | `run-1-rome` | 1 |
| [`1_rome_270_autumn_7_fleet.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/1_rome_270_autumn_7_fleet.sav) | `run-1-rome` | 1 |
| [`1_thracia_271_autumn_1.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_autumn_1.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_spring_1.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_spring_1.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_spring_3.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_spring_3.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_spring_7.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_spring_7.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_summer_1.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_summer_1.sav) | `run-1-thracia` | 1 |
| [`1_thracia_271_summer_9.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_summer_9.sav) | `run-1-thracia` | 1 |
| [`5.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/5.sav) | `legacy-probes` | 1 |
| [`6.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/legacy-probes/6.sav) | `legacy-probes` | 1 |
| [`1_cartago_271_spring_11.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_spring_11.sav) | `run-1-cartago` | — |
| [`1_cartago_271_spring_5.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_spring_5.sav) | `run-1-cartago` | — |
| [`1_cartago_271_spring_7.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_spring_7.sav) | `run-1-cartago` | — |
| [`1_cartago_271_summer_1.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_summer_1.sav) | `run-1-cartago` | — |
| [`1_cartago_271_summer_3.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_summer_3.sav) | `run-1-cartago` | — |
| [`1_cartago_271_summer_5.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_summer_5.sav) | `run-1-cartago` | — |
| [`1_cartago_271_summer_7.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-cartago/1_cartago_271_summer_7.sav) | `run-1-cartago` | — |
| [`1_thracia_271_spring_5.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_spring_5.sav) | `run-1-thracia` | — |
| [`1_thracia_271_spring_9.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_spring_9.sav) | `run-1-thracia` | — |
| [`1_thracia_271_summer_11.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_summer_11.sav) | `run-1-thracia` | — |
| [`1_thracia_271_summer_3.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_summer_3.sav) | `run-1-thracia` | — |
| [`1_thracia_271_summer_5.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_summer_5.sav) | `run-1-thracia` | — |
| [`1_thracia_271_summer_7.sav`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-thracia/1_thracia_271_summer_7.sav) | `run-1-thracia` | — |

## Recordings

Only recordings that `notes/` ties to a specific save pair are published. **Three more exist locally and are deliberately not here** — nothing in the notes says what they show, and assigning them by timestamp would have been a guess dressed as evidence.

| Asset (as downloaded) | Spans | Release |
|---|---|---|
| [`bandicam.2026-09-12.23-56-28-394.mp4`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/bandicam.2026-09-12.23-56-28-394.mp4) | 1_rome_270_winter_3.sav .. 1_rome_270_winter_5.sav | `run-1-rome` |
| [`bandicam.2026-09-13.00-04-38-377.mp4`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/bandicam.2026-09-13.00-04-38-377.mp4) | 1_rome_270_winter_5.sav .. 1_rome_270_winter_7.sav | `run-1-rome` |
| [`bandicam.2026-09-13.00-31-14-131.mp4`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/bandicam.2026-09-13.00-31-14-131.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_9.sav (1 of 4) | `run-1-rome` |
| [`bandicam.2026-09-13.00-32-26-388.mp4`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/bandicam.2026-09-13.00-32-26-388.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_9.sav (2 of 4) | `run-1-rome` |
| [`bandicam.2026-09-13.00-35-54-640.mp4`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/bandicam.2026-09-13.00-35-54-640.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_9.sav (3 of 4) | `run-1-rome` |
| [`bandicam.2026-09-13.01-03-29-805.mp4`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/bandicam.2026-09-13.01-03-29-805.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_9.sav (4 of 4) | `run-1-rome` |
| [`bandicam.2026-09-13.22-49-01-893.mp4`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/bandicam.2026-09-13.22-49-01-893.mp4) | 1_rome_270_winter_7.sav .. 1_rome_270_winter_7_b.sav | `run-1-rome` |
| [`bandicam.2026-09-13.23-14-41-582.mp4`](https://github.com/diegoami/imp_conquest_original/releases/download/run-1-rome/bandicam.2026-09-13.23-14-41-582.mp4) | 1_rome_270_winter_9_b.sav .. 1_rome_270_winter_11.sav | `run-1-rome` |

## Screenshots

The two `.txt` files in `legacy-probes` — `11_supply.txt` and `12_ptol.txt` — are the contemporaneous notes saying what each image shows, and are **the authority over any later guess**. `11_supply.4/.5` carry the nation colour and identifier table (left to right for colours, top to bottom for names, 0–15 for identifiers), which is the source for the sixteen-nation palette.

| Release | Screenshots |
|---|---|
| [`run-1-rome`](https://github.com/diegoami/imp_conquest_original/releases/tag/run-1-rome) | `1_rome_270_autumn_1_1.png`, `1_rome_270_autumn_3_1.png`, `1_rome_270_autumn_7_1.png`, `1_rome_270_summer_7_1.png`, `1_rome_270_summer_9_1.png` |
| [`run-1-cartago`](https://github.com/diegoami/imp_conquest_original/releases/tag/run-1-cartago) | `1_cartago_271_spring_1b_1.png`, `1_cartago_271_spring_3_1.png` |
| [`legacy-probes`](https://github.com/diegoami/imp_conquest_original/releases/tag/legacy-probes) | `11_supply.1.png`, `11_supply.2.png`, `11_supply.3.png`, `11_supply.4.png`, `11_supply.5.png`, `11_supply.6.png`, `11_supply.7.png`, `11_supply.8.png`, `11_supply.txt`, `12_ptol.1.png`, `12_ptol.txt`, `12_ptol_2.png`, `12_ptol_3.png`, `12_rom_1.png`, `12_rom_2.png`, `12_rom_3.png`, `7.1.png`, `7.2.png`, `7.3.png`, `7.4.png`, `7.5.png`, `7.6.png`, `7.7.png`, `7.8.png`, `Initial_world.1.png` |

## Retrieving a file

The repository is private, so an authenticated `gh` is the way in:

```
gh release download run-1-rome --repo diegoami/imp_conquest_original \
    --pattern "1_rome_270_winter_7.sav" --dir .

gh release list --repo diegoami/imp_conquest_original
gh release view legacy-probes --repo diegoami/imp_conquest_original
```

## Keeping this file true

A new play-through means a **new release**, named `run-<n>-<nation>`, and a new row here. Three rules make the index worth trusting:

- **A recording goes up only when a note maps it to a save pair.** An unattributed video is not evidence, and putting it in a release implies it is.
- **Observation notes ship with their run.** A save series without its notes shows what the engine did but not what was asked of it, and the difference has mattered repeatedly.
- **Nothing here is copied into a repository.** This file points; it never holds.
