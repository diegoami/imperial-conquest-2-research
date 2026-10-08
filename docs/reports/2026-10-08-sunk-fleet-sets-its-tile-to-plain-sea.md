# A sunk fleet's tile becomes plain sea (0), even on rough sea; a fleet that sails away restores its tile

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commits
`faf030d` + `8bf62da`; run data at `df3f461`. Release
[`run-exp-naval-loser-rough-sea`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-naval-loser-rough-sea)
holds the 9 cited saves (`cover0`, `cover1`, `move_cover1`, each `PRE` / `BEFORE` / `AFTER`) and an
uncited attempt tarball. Their SHA-256s are committed at
`runs/experiments/data/run-exp-naval-loser-rough-sea/SAVES.sha256`. Wine-only evidence. It settles
the open item of [`2026-10-08-naval-battle-loser-clears-its-tile.md`](2026-10-08-naval-battle-loser-clears-its-tile.md).

**Review note:**
- **Saves and patch.** The 9 saves were downloaded and matched `SAVES.sha256`. The tile words at
  (110,73), (111,73) and (111,74) were re-read with an independent reader and agree with the table.
  `cover0_BEFORE` and `cover1_BEFORE` differ in exactly two bytes (offsets 108,200 and 108,226, both
  0 → 1). They are 26 bytes apart, one fleet-record stride, so the patch is the two `+24` fields and
  nothing else, and it survived the load.
- **Reproducibility.** `cover0_PRE` is the fixture, and `cover0_AFTER` is byte-identical to
  `PROBE_AFTER.SAV` of `run-exp-naval-battle`: the same battle reproduced exactly.
- **Agreement with an earlier code reading.** The result matches
  [`decompiled-map-code1-overlay.md`](decompiled-map-code1-overlay.md): "every other writer copies a
  unit's covered cell back, writes a marker, or writes 0 (fleet or army removal)" `[confirmed]`. It
  also matches the fleet step `FUN_0044dd70`, which swaps `+24` with the map cell as the fleet moves.
- **Correction to the draft's consequence.** The draft says a fleet sunk on rough sea turns that tile
  into plain sea **permanently**. That does not hold. Rough sea (code 1) is a weekly weather overlay:
  `FUN_00451304` clears every code 1 within ±10 of its 20 centres and re-rolls them each week ("code 1
  lives exactly one week", same report). So the sunk fleet only ends that tile's rough sea for the rest
  of the week, and the next roll can paint it again. The corrected consequence is below.

**Tag:** `[confirmed]` for the observed behaviour. `[derived]` for its consequence on the map.

## Answer

- **Battle loss: cleared to 0.**
  - **Setup:** the losing fleet's covered-cell field (+24) was set to **1** (rough sea).
  - **After:** its tile reads **0** in the save and in memory.
  - **Unpatched control** (covered cell 0): also 0.
  - **Same battle both times:** seed 12345, the fixture of `run-exp-naval-battle`. Carthage sinks Ptolemaic's fleet and keeps 80 ships; the news line "Carthage sinks fleet of Ptolemaic." appears in both.
- **Sailing away: restored.** With the same covered cell **1**, Ptolemaic's fleet sailed from (111,73) to (111,74). The old tile went back to **1** and the fleet's marker moved to (111,74) as 335. So the game does use the covered-cell field when a fleet leaves a tile; tombstoning a fleet (`FUN_0044ad38`, research reading) writes 0 instead.
- **Consequence (`[derived]`, corrected on promotion):** a fleet sunk on a rough-sea tile leaves calm sea (0) there for the rest of the week. Rough sea is a weekly weather overlay that `FUN_00451304` clears and re-rolls every week ([`decompiled-map-code1-overlay.md`](decompiled-map-code1-overlay.md)), so the change lasts at most until the next weekly roll. Rough sea costs 3 moves per tile and calm sea 1 ([`terrain-move-cost-table-in-dat.md`](terrain-move-cost-table-in-dat.md)). The draft's "permanent" reading would only apply to a covered code that the weather does not repaint.

| Case | Loser's covered cell before | Order | Word at (111,73) after | Save = memory |
|---|---:|---|---:|---|
| cover0 | 0 | attack, Ptolemaic sunk | **0** | yes |
| cover1 | 1 | attack, Ptolemaic sunk | **0** | yes |
| move_cover1 | 1 | Ptolemaic sails to (111,74) | **1** (marker 335 now at (111,74)) | yes |

Evidence: run-exp-naval-loser-rough-sea, `cover0_{PRE,BEFORE,AFTER}.SAV`, `cover1_*`, `move_cover1_*` (release `run-exp-naval-loser-rough-sea`; SHA-256 in `runs/experiments/data/run-exp-naval-loser-rough-sea/SAVES.sha256`); `probe_rough.py`, `probe_rough.log`, `probe_rough_*.json`. One control attempt that targeted a land tile ((112,73), word 2, so the fleet did not move) is kept in `attempt_move_to_land.tar.gz` (release) and not cited.

## Method

- **Fixture:** `saves/fleets-adjacent-at-sea-0723.SAV` (Ptolemaic's turn, at war with Carthage): Ptolemaic fleet 1 (70 ships) at (111,73), Carthage fleet 0 (90 ships) at (110,73).
- **Patch:** both fleets' covered-cell field (+24) set to 1 for cover1 and move_cover1. Check: the `BEFORE` save of cover1 shows 1 in both records after the load.
- **Run:** fast rollingsave seed exe, seed 12345, Xvfb :99. Select fleet 1, then click Carthage's fleet (attack) or the sea tile (111,74) (move). Save, then read the words at (110,73), (111,73) and (111,74) and `Game.cell` for each.

## Not established

- A fleet sunk by a storm, or a loser on a real (unpatched) rough-sea tile. The patched field is what the game reads, so the result should carry over (`[derived]`).
- Armies: whether a destroyed army also writes 0, or restores its covered cell. From code, army removal writes 0 too (`decompiled-map-code1-overlay.md`). An army covers land codes 2-11, which no weekly pass repaints, so that predicts a destroyed army leaves code 0 (calm sea) on a land tile. That is untested in play (`[derived]`).
