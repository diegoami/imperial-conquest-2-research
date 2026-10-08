# Siege: an army needs an attack strength of at least 1 (80 men, or 27 archers) to besiege

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commits
`a24bf69` + `f22ffc4`; run data at `f83d9f9`. The saves were added to release
[`run-exp-siege-army-removal`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-siege-army-removal)
(`u79`, `u80`, `ar26`, `ar27`, each `PRE` / `BEFORE` / `AFTER`), and their SHA-256s are in
`runs/experiments/data/run-exp-siege-army-removal/SAVES.sha256`. Wine-only evidence. This is an
addendum to [`2026-10-09-siege-removed-army-restores-its-tile.md`](2026-10-09-siege-removed-army-restores-its-tile.md).
It is the 79 / 80 check the research side proposed from
[`decompiled-defection-and-siege-attrition.md`](decompiled-defection-and-siege-attrition.md)'s
reading of `FUN_0044a930`.

**Review note:**
- **Saves.** The 12 new saves were downloaded and matched `SAVES.sha256`. The tile word at (99,32) was
  re-read independently: 200 → 5 for u80 and ar27, and 200 throughout for u79 and ar26.
- **Hashes.** The two no-siege cases are byte-identical across `PRE` / `BEFORE` / `AFTER`, so nothing
  at all changed. `u80_AFTER` is byte-identical to the u99 / u100 / u150 `AFTER` saves of the first
  batch: the same removed-army end state was reached again.

**Tag:** `[confirmed]` for the boundary. `[derived]` for the cause (the division by zero at 0x0044B249 per research).

## Answer

| Army 0 | Σ troops (archers × 3) | div 80 | Result |
|---|---:|---:|---|
| 79 heavy infantry | 79 | 0 | **no siege**: moves stay 8, Felsina unchanged, army unchanged |
| 80 heavy infantry | 80 | 1 | **siege** (Felsina fort 65 → 62), army removed by attrition |
| 26 archers | 78 | 0 | **no siege** |
| 27 archers | 81 | 1 | **siege**, army removed by attrition |

- The boundary is exactly where Σ troops (archers counted × 3) div 80 reaches 1. Morale was 70 in every case.
- The armies that besieged were then removed by attrition (units under 600 men are deleted, per research). Their tiles read **5**, the patched covered cell, as in the 99/100/150 cases.
- The armies that did not besiege kept their moves (8), so the order left no trace: no siege, no move spent, no box.

Evidence: run-exp-siege-army-removal, `u79_*`, `u80_*`, `ar26_*`, `ar27_*` `{PRE,BEFORE,AFTER}.SAV` (release `run-exp-siege-army-removal`; SHA-256 in `runs/experiments/data/run-exp-siege-army-removal/SAVES.sha256`); `probe_siege.v2.py`, `probe_siege.v2.log` (batch 2), `probe_siege_u79_u80_ar26_ar27.json`.

## Method

As in `2026-10-09-siege-removed-army-restores-its-tile.md`:
- The fixture is `saves/siege-felsina-failed-0721.SAV`. The patch gives Rome army 0 at (99,32) moves 8, covered cell 5, and a single quality-7 unit: heavy infantry (type 1) or archers (type 2).
- Fast rollingsave seed exe, seed 12345, Xvfb :99. Then `g.attack(0, 98, 31)`.
