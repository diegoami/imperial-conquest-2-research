# Fleets: the map marker's ship band, and the three fleet icons

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit
`b208b2f` (`b208b2fccf5aee02b5cb81249886878f3cd238b2`); run data at `8d37a29`. Release
[`run-exp-fleet-marker-band`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleet-marker-band)
holds the 12 Part A saves, the 7 Part B variant saves with their `_screen.png` and `_tile.png`, and
`montage_bands.png` (34 files). Their SHA-256s are committed at
`runs/experiments/data/run-exp-fleet-marker-band/SAVES.sha256`. Wine-only evidence. It closes the
fleet half of the open item in
[`2026-10-08-army-icon-follows-the-size-band.md`](2026-10-08-army-icon-follows-the-size-band.md),
and it tests in play the `FUN_0044a878` reading in
[`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md) Part 3.

**Review note:**
- **Tile pixels.** The seven `_tile.png` files were downloaded and their decoded RGB pixels hashed
  on the reviewing side. The variants group by stored word (300 / 316 / 332), not by ships, and the
  three groups differ.
- **Screens.** Within each word, the `_screen.png` files are byte-identical by their `SAVES.sha256`
  entries. The pinned scroll worked.
- **Montage.** `montage_bands.png` shows a small sailboat, a galley with three shields and a larger
  galley with four.
- **Part A.** Each Part A `AFTER` save is the same file as the matching unpatched Part B variant
  (e.g. `s24_AFTER.SAV` = `w300_s24.SAV`), so the variants start from the joined state.
- **Agreement with earlier reports.** The boundaries match `FUN_0044a878`'s `ships < 25 / < 50`
  reading, and the `333` / `335` large-fleet markers that reading had explained.

**Tag:** `[confirmed]`.

## Answer

- **The fleet word is owner + 300 below 25 ships, + 316 below 50, + 332 from 50 up.** Live boundaries through Join fleets (Rome fleets 2 + 5, survivor fleet 2 at (101,46)): 24 → **300**, 25 → **316**, 49 → **316**, 50 → **332**. The word in the save and in memory agree. Before the join the word was 300, the pre-state's value; the edited ships were not re-banded on load. The join rewrote it.
- **Three icons**, pixel-different:
  - **300**: a small sailboat.
  - **316**: a galley with three shields along the hull.
  - **332**: a larger galley with a bigger sail and four shields.

  The tile RGB hashes are `ded897e0…`, `4c94b1dd…` and `2965e2ef…`; `montage_bands.png` shows them enlarged side by side.
- **The icon follows the stored word, not the ships**, as for armies:
  - 24 ships with word 316 draws the 316 icon;
  - 24 ships with word 332 draws the 332 icon;
  - 50 ships with word 300 draws the small boat.

  With the scroll pinned, the whole screen is byte-identical between variants with the same word (see the table).

| Variant | Word | Ships | Tile RGB hash | Screen RGB hash |
|---|---:|---:|---|---|
| w300_s24 | 300 | 24 | `ded897e0bb450a22` | `5251ba54cdeb5c38` |
| w316_s25 | 316 | 25 | `4c94b1ddeb2d5f1b` | `3605330b18a033a1` |
| w316_s49 | 316 | 49 | `4c94b1ddeb2d5f1b` | `3605330b18a033a1` |
| w332_s50 | 332 | 50 | `2965e2efa15363d8` | `2bde47f146a42b48` |
| w316_s24 | 316 (patched) | 24 | `4c94b1ddeb2d5f1b` | `3605330b18a033a1` |
| w332_s24 | 332 (patched) | 24 | `2965e2efa15363d8` | `2bde47f146a42b48` |
| w300_s50 | 300 (patched) | 50 | `ded897e0bb450a22` | `5251ba54cdeb5c38` |

Evidence: run-exp-fleet-marker-band. The Part A saves are `s24/s25/s49/s50_{PRE,BEFORE,AFTER}.SAV`; the Part B files are `<variant>.SAV`, `<variant>_screen.png`, `<variant>_tile.png` and `montage_bands.png` (release `run-exp-fleet-marker-band`; SHA-256 in `runs/experiments/data/run-exp-fleet-marker-band/SAVES.sha256`). Scripts and output: `probe_fleet_band.py`, `probe_fleet_band.log`, `probe_fleet_band.json`.

## Method

- The fixture is `saves/fleet-split-antium-0734.SAV`: Rome fleet 2 (20 ships) at (101,46) and fleet 5 (10 ships) at (101,47), neither carrying an army. Their ships are patched with `tests/test_orders.py::_make_patched_fleet_split_save(a, b)` (a content scan; +18 is the ships field).
- Fast rollingsave seed exe, seed 12345, Xvfb :99.
- **Part A:** load, save `BEFORE`, `g.join_fleets(2)`, save `AFTER`, then read the word at save offset 101 × 280 + 46 × 2 and `Game.cell(101, 46)`.
- **Part B:** load each variant, then click the Area map at (101,46). That pins the unit map at origin (95,39) every time, as research suggested after the army run. Park the pointer on the root window, capture the screen, and crop the 32×32 tile at (545,366).

## Not established

- Other owners' colours (only Rome was drawn).
- Which orders, besides Join fleets, re-band a fleet. Split fleet, Transfer ships, storms and battle losses were not run. **Settled since:** Split fleet and Transfer ships re-band in play, and storms and the winner's battle losses do so in code: [`2026-10-08-split-and-transfer-reband-fleets.md`](2026-10-08-split-and-transfer-reband-fleets.md).
