# A removed army restores the terrain under it (disband, join, battle loss), unlike a sunk fleet

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commits
`d1e95c0` + `810e465`; run data at `9867eba`. Release
[`run-exp-army-removal-tile`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-army-removal-tile)
holds the 9 cited saves (`disband`, `join`, `battle`, each `PRE` / `BEFORE` / `AFTER`) and an uncited
attempt tarball. Their SHA-256s are committed at
`runs/experiments/data/run-exp-army-removal-tile/SAVES.sha256`. Wine-only evidence. The research side
asked for it after promoting [`2026-10-08-sunk-fleet-sets-its-tile-to-plain-sea.md`](2026-10-08-sunk-fleet-sets-its-tile-to-plain-sea.md).

**Review note:**
- **Saves.** The 9 saves were downloaded and matched `SAVES.sha256`. The tile words at (100,37),
  (101,45), (102,44), (86,28) and (85,28) were re-read with an independent reader, and every value
  agrees with the draft (removed army's tile → 4; Gaul's army 10 222 → 206).
- **Code.** `FUN_0044ab90` was re-read in ic2-conquest's `code_extract_q1_purse.txt` (:49372-49393).
  If the army is aboard a fleet (`+8 < 0`), it clears that fleet's carried-army field. Otherwise it
  writes `map[x][y] = army +8`, the covered cell. Either way it then tombstones the owner. The cited
  call sites (:46996, :49679, :57626-57627) match.
- **This corrects a research report.** [`decompiled-map-code1-overlay.md`](decompiled-map-code1-overlay.md)
  said map writers "write 0 (fleet or army removal)". For armies that is wrong on the main removal
  routine, which restores the covered cell; the sentence there has been corrected. The research side's
  own prediction from it (a destroyed army leaving calm sea on land) does not occur on these three
  paths.

**Tag:** `[confirmed]` for the three paths run.

## Answer

- **No.** In all three removal paths the army's tile gets its covered cell back. Each removed army's covered-cell field (+8) was patched from its real terrain, plain (2), to forest (**4**), and the tile read **4** afterwards, in the save and in memory:

  | Case | Fixture | Removed army | Tile before → after |
  |---|---|---|---|
  | disband | run-0 start, Rome army 0 at (100,37) by Arretium | army 0 (Disband army, Confirm Yes) | 200 → **4** |
  | join | fleet-port fixture, army 0 (101,45) + army 13 (102,44) | partner army 13 (Join armies) | 200 → **4** |
  | battle | FLD-RG (Rome army 0 at (86,28) vs Gaul army 10 at (85,28)), tactical battle with Computer general | Rome army 0 ("Gaul destroys army of Rome.") | 216 → **4** |

- This fits the code. All three go through `FUN_0044ab90`, which writes the army's covered cell back to the map (:49386-49389):
  - Join armies: :46996;
  - the tactical battle: `TBattleOver_OK` :57627;
  - the instant field battle: `FUN_0044aee4` :49679, not run here.
- **The winner is re-banded.** Gaul's army 10 fell from 46,700 to 17,239 troops and its word from 222 (band 216 + owner 6) to **206** (band 200), from `FUN_0044a80c` :57626.
- **Contrast with fleets:** a sunk fleet's tile becomes 0 even on rough sea (`4495fc6`), while a fleet that sails away restores its covered cell. For armies, no removal path run here wrote 0, so the "permanent calm sea on land" case did not occur. The research report's "writes 0 (army removal)" was not reached by disband, join or a field-battle loss, and `FUN_0044ab90` itself restores the cell, so that line has been corrected. Other army removals were not run: the last unit lost via `FUN_0044ac3c`, AI removals, sieges.

Evidence: run-exp-army-removal-tile, `disband_{PRE,BEFORE,AFTER}.SAV`, `join_*`, `battle_*` (release `run-exp-army-removal-tile`; SHA-256 in `runs/experiments/data/run-exp-army-removal-tile/SAVES.sha256`); `probe_army_tile.py`, `probe_army_tile.log`, `probe_army_tile_*.json`. The first battle attempt failed in the driver's view check (the FLD-RG save opens a 29 × 27-tile unit map, `runs/experiments/battles/common.py`); it is kept as `attempt_battle_view.tar.gz` and not cited.

## Method

Fast rollingsave seed exe, seed 12345, Xvfb :99. The pre-state patches only the +8 field of the army or armies that could be removed: in the battle both armies, since either could lose. Load, save `BEFORE`, run the order through the driver, save `AFTER`, then read the map word at each patched army's tile (offset x × 280 + y × 2) and `Game.cell`. For the battle the driver's view size is set to 29 × 27, as in the battle runners.

## Not established

- Army removal when the last unit is lost (mercenary desertion, `FUN_0044ac3c`), AI-side removals at the turn end, the instant AI-vs-AI field battle (`FUN_0044aee4`, which per the code uses the same `FUN_0044ab90`), and armies destroyed in a siege. **Siege settled since:** a besieger emptied by attrition is removed and its cover restored: [`2026-10-09-siege-removed-army-restores-its-tile.md`](2026-10-09-siege-removed-army-restores-its-tile.md). **AI-side and turn-end removals settled since** (elimination, mercenary desertion, AI-vs-AI battle, and compaction): [`2026-10-09-turn-end-and-ai-army-removals-restore-their-tile.md`](2026-10-09-turn-end-and-ai-army-removals-restore-their-tile.md).
