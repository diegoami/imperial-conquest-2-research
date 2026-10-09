# When a nation is conquered, its fleet and the army aboard are removed with it; the fleet's tile is written 0, even over rough sea

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit
`382d210` (`382d2109466f5d227e4609b483f5ec3149274fa1`; run data at `3931714`). Release
[`run-exp-elimination-army-aboard`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-elimination-army-aboard)
holds the 9 saves, and their SHA-256s are committed at
`runs/experiments/data/run-exp-elimination-army-aboard/SAVES.sha256`. Wine-only evidence, with
an edited pre-state. It answers the open item "armies aboard a fleet at elimination" left by
[`2026-10-09-turn-end-and-ai-army-removals-restore-their-tile.md`](2026-10-09-turn-end-and-ai-army-removals-restore-their-tile.md).

**Review note:**
- I downloaded all 9 saves and checked them against `SAVES.sha256` (9 OK). I read the words at
  (74,71), (42,63) and (38,64) with my own reader. Every `PRE`/`BEFORE` save has 337 / 221 / 2,
  and every `AFTER` save has **0 / 2 / 2**, as the draft says. `probe_aboard_sieges_cover1.json`
  shows the fleet's cell at 1 before the conquest.
- **The draft's open code question is settled from
  [`decompiled-elimination-cleanup.md`](decompiled-elimination-cleanup.md).** The conquest
  (`FUN_0044C528`, step 6) runs the same army loop and fleet loop as `FUN_0044BED8`, armies
  first:
  1. The army loop calls `FUN_0044AB90(10)`. The army's cell is −1 (aboard), so the function
     finds the carrier by coordinates and sets its `+22` to −1 **without writing the map**, then
     tombstones the army. That is the fleet's army field 10 → −1 and the missing 0xFFFF write.
  2. The fleet loop calls `FUN_0044AD38(0)` on the launched fleet. That writes **0** to its tile
     (not `+24`), finds `+22` already −1 so nothing is deleted twice, and tombstones the fleet.
  3. The compaction at End turn (`FUN_0044ADB0`, from the AI-seat loop) removes the tombstones and
     renumbers the carried indices, which explains the 14 → 12 armies and the clean `+22` fields.
  The mechanism is `[confirmed]` by code and play together, for this edited pre-state.
- **This also settles what the storm run could not.** In
  [`2026-10-09-storm-sunk-fleet-clears-its-tile.md`](2026-10-09-storm-sunk-fleet-clears-its-tile.md),
  the weekly re-roll ran after the loss, so play could not tell "write 0" from "restore the
  covered cell". Here no weekly tick runs between the captures and the save, and the
  `sieges_cover1` tile still reads 0 over a covered cell of 1. So `FUN_0044ad38` writes 0, seen
  in play without the re-roll in between.

**Tag:** `[confirmed]` (3 runs, seed 12345, synthetic pre-state; code path by decompile).

## Answer

In all three cases, Rome's third capture leaves Numidia with 5 cities, and the news reads "Rome conquers Numidia."

- **Fleet:** its record gets owner **−1**, and its carried-army field goes from 10 to **−1**. Ships (90) and position (74,71) are left as they were.
- **Army aboard (record 10):** its record gets owner **−1**. It keeps x,y = the fleet's tile, cell −1 and its 33,900 troops.
- **Fleet tile (74,71):** marker 337 → **0**, in the save and in memory.
  - When the fleet's covered cell (+24) was set to 1 (rough sea) before the sieges (`sieges_cover1`), the tile still reads **0**. The conquest writes 0; it does not restore the covered cell. This matches the battle-sunk fleet (`2026-10-08-sunk-fleet-sets-its-tile-to-plain-sea.md`).
  - The army aboard leaves nothing on the map. Its cell field is −1, and no −1 (0xFFFF) is written to the fleet's tile.
- **Numidian army on land (record 2, control):** owner −1, and its tile goes from marker 221 back to its covered cell **2**, as in the earlier conquest case.
- **After End turn** (`sieges_end_turn`, autosave `AUTO0722.SAV`): the tombstoned records are compacted away. Armies go from 14 → **12** (records 2 and 10 gone, later records shift down). The dead fleet record is gone, and Ptolemaic's fleet is now record 0. No fleet is left carrying an index into the shifted army table: every fleet's carried-army field is −1. The second fleet record in that save is a Carthaginian fleet being built (countdown 22), started during the AI turn.
- **No message** names the fleet or the army. The news has only the three captures and "Rome conquers Numidia."; no confirm box appeared (popups: none).

| Case | Fleet owner after | Fleet's army field | Army 10 owner after | Tile (74,71) after | Land army tile (42,63) after | Records after |
|---|---:|---:|---:|---:|---:|---|
| `sieges` | −1 | −1 | −1 | 0 | 2 | 14 armies, 2 fleets (tombstones kept) |
| `sieges_cover1` (fleet covered cell 1) | −1 | −1 | −1 | **0** | 2 | same |
| `sieges_end_turn` | (record removed) | – | (record removed) | 0 | 2 | 12 armies; fleets: Ptolemaic + a Carthage fleet being built |

## Method

- **Base:** `saves/siege-felsina-failed-0721.SAV` (Rome's turn, 0721). The consistent elimination pre-state of `run-exp-turn-end-army-removal`:
  - three Rome armies of 2 × 30,000 heavy infantry are placed next to Capsa, Ghadames and Ghirza (Numidia holds 8 cities);
  - Carthage army 2 at (42,63) is re-owned to Numidia;
  - Rome and Numidia are set at war.
- **Added for this test (synthetic edits):**
  - Carthage fleet 0 (90 ships, at (74,71)) is re-owned to Numidia, with marker 333 → 337 (owner 5 + 332, band unchanged).
  - Celtiberia army 10 (33,900 men, at (38,64)) is re-owned to Numidia and put aboard that fleet. This is the edit of `runs/experiments/fleet-battles/t3_stage.py`, byte-checked there against a natural embark: army x,y = the fleet's tile, moves 0, cell −1; fleet +22 = 10; the army's old tile restored to its covered cell 2.
  - `sieges_cover1` also sets the fleet's +24 to 1.
- **Run:** fast rollingsave seed exe, seed 12345, Xvfb. The three armies attack their cities in turn (`Game.attack`), and the save is taken after the third capture. `sieges_end_turn` then ends the turn and saves again.
- **Read:** the fleet and army records, the words at (74,71), (42,63) and (38,64), in the save and in game memory (`Game.cell`).

## Evidence

- **Data:** `runs/experiments/data/run-exp-elimination-army-aboard/`: `probe_aboard.py`, `probe_aboard_{sieges,sieges_cover1,sieges_end_turn}.json`, `SAVES.sha256`.
- **Saves:** release `run-exp-elimination-army-aboard`: `<case>_PRE.SAV` (edited), `<case>_BEFORE.SAV` (after the load), `<case>_AFTER.SAV`, for the cases `sieges`, `sieges_cover1` and `sieges_end_turn`. Turn 0721; `sieges_end_turn_AFTER.SAV` is at 0722.

## Not established

- **A natural pre-state:** the fleet and the army aboard come from save edits. A Numidian fleet that embarked an army in play, and an AI nation conquered in an AI-side capture, were not run. **Searched since, none found:** 7,618 existing saves and 11 idle seeds (334 end turns) show loaded fleets only for Carthage, Ptolemaic and Greece, none of which fell: [`2026-10-09-no-natural-ai-conquest-with-army-aboard.md`](2026-10-09-no-natural-ai-conquest-with-army-aboard.md).
- ~~**Code path**~~: settled from code (see the review note). The army loop calls `FUN_0044AB90` on the army aboard first, and then the fleet loop calls `FUN_0044AD38`.
- **Other elimination paths:** defection elimination (`FUN_0044BED8`, via rebirth) was recorded by code only and was not run here.
