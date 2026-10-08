# Split fleet and Transfer ships re-band the fleets they change

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit
`69820e1` (`69820e1d32a818189021c1c524c05e81a17f6e62`); run data at `f70c13c`. Release
[`run-exp-fleet-reband-orders`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleet-reband-orders)
holds the 12 saves (`sp1`, `sp2`, `tr1`, `tr2`, each `PRE` / `BEFORE` / `AFTER`), and their
SHA-256s are committed at `runs/experiments/data/run-exp-fleet-reband-orders/SAVES.sha256`.
Wine-only evidence. It answers "which orders besides Join fleets re-band a fleet" from
[`2026-10-08-fleet-marker-band-and-icon.md`](2026-10-08-fleet-marker-band-and-icon.md).

**Review note: the code sites are already on this side.** The draft lists the code site of the
re-band as open, because its extracts show `FUN_0044a878` called only from `TUnitMap_JoinFleets`.
[`2026-10-07-city-marker-variants.md`](2026-10-07-city-marker-variants.md) (Reproduction) lists
all its callers:
- `TFleetToFleet_OK` (:44994, :45004): the OK of the split / transfer dialog, which fits both
  results here;
- `TUnitMap_JoinFleets` (:47250);
- construction completion `FUN_0044a050` (:48795);
- `FUN_0044b4f8` (:49880);
- the AI merge `FUN_00450b30` (:54034).

[`decompiled-diplomacy-peace-terms-and-instant-battles.md`](decompiled-diplomacy-peace-terms-and-instant-battles.md)
shows that `FUN_0044b4f8` is the ship-loss routine. It ends with `FUN_0044A878(fleet)` at
`0x0044B5C3`, and the naval battle calls it for the **winning** fleet; the city-marker report
names it as the storm damage too. So from code, storm losses and the winner's battle losses
re-band (`[confirmed]` as a code reading; not run). The losing fleet is tombstoned by
`FUN_0044ad38` instead, and whether that clears its map word is not established here.

**Saves.** In every case the `PRE` and `BEFORE` hashes are equal (the load changed nothing), and
`AFTER` differs.

**Tag:** `[confirmed]` for Split fleet and Transfer ships. Storms and battle losses were not run.

## Answer

After each order, every Rome fleet's map word equals its band (owner + 300 / 316 / 332 for ships < 25 / < 50 / more), in the save and in memory, in both directions across both boundaries:

| Case | Before (fleet: ships / word) | Order | After (fleet: ships / word) |
|---|---|---|---|
| sp1 | 2: 30 / 316 | Split fleet, 10 off | 2: 20 / **300**; new fleet 5 at (101,47): 10 / 300 |
| sp2 | 2: 50 / 332 | Split fleet, 1 off | 2: 49 / **316**; new fleet 5: 1 / 300 |
| tr1 | 2: 25 / 316; 5: 24 / 300 | Transfer ships, 1 from 2 to 5 | 2: 24 / **300**; 5: 25 / **316** |
| tr2 | 2: 50 / 332; 5: 10 / 300 | Transfer ships, 1 from 2 to 5 | 2: 49 / **316**; 5: 11 / 300 |

- **Split fleet** re-bands the source fleet and draws the new fleet at its own band.
- **Transfer ships** re-bands both fleets, the one that loses ships and the one that gains them.

The pre-state words were set to the band of the patched ships, so each change seen is the order's re-band and not a stale word from the edited save. Loads do not re-band (`be0691a`, `bff6bff`).

Code: the bot's extracts show `FUN_0044a878` called only from `TUnitMap_JoinFleets` (:47250). The research side's caller list (review note above) puts these re-bands in `TFleetToFleet_OK` (:44994, :45004).

Evidence: run-exp-fleet-reband-orders, `<case>_{PRE,BEFORE,AFTER}.SAV` for sp1_split_30_by_10, sp2_split_50_by_1, tr1_transfer_25_24_by_1 and tr2_transfer_50_10_by_1 (release `run-exp-fleet-reband-orders`; SHA-256 in `runs/experiments/data/run-exp-fleet-reband-orders/SAVES.sha256`); `probe_reband.py`, `probe_reband.log`, `probe_reband_*.json`.

## Method

- **Fixtures:** `saves/fleet-port-antium-0734.SAV` (Rome fleet 2, 30 ships, at (101,46)) for the splits; `saves/fleet-split-antium-0734.SAV` (fleets 2 and 5 at (101,46) and (101,47)) for the transfers.
- **Pre-state:** the ships were patched through a content scan on (x, y, owner 0) at +18, and each fleet's map word was set to its band.
- **Run:** fast rollingsave seed exe, seed 12345, Xvfb :99. Load, save `BEFORE`, then `g.split_fleet(2, n)` or `g.transfer_ships(2, n)`, save `AFTER`, and read the words at each Rome fleet's tile.

## Not established

- **Storms and naval-battle losses in play:** they change ships at the turn end or in a battle and could not be forced here. From code they re-band through `FUN_0044b4f8` (review note).
- **The losing fleet's map word** after a naval battle (`FUN_0044ad38` tombstones it).
