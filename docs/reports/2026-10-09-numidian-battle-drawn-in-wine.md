# A Rome v Numidia battle drawn in Wine: Numidia's battle units are lime, black and grey, exactly the recoloured templates

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `b1a67d3`. Release
[`run-exp-battle-numidia-colour`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-numidia-colour)
holds `20261009-141127_NUM_start.SAV`, `_NUM_placement.SAV`, `_NUM_after_end_turn_1.SAV` and their
`*_window.png` screenshots. Their SHA-256s are committed at
`runs/experiments/data/run-exp-battle-numidia-colour/SAVES.sha256`. Wine-only, from an L1
(synthetic, labelled) start. It closes the "Not established" item "a Numidian battle drawn in
Wine" of
[`2026-10-09-battle-map-units-use-the-nation-recolour.md`](2026-10-09-battle-map-units-use-the-nation-recolour.md).

**Review note:**
- The 3 saves and 2 screenshots hash OK. The two screenshots are byte-identical, as the draft says,
  so there is one distinct image.
- **The edit:** in `_NUM_start.SAV` and `_NUM_placement.SAV`, army 10 is at (85,28) with owner 5,
  next to Rome's army 0 at (86,28).
- **Numidia's dwords in the save:** `00ff00`, `000000`, `808080`.
- **Template check, my own script** (as for the B2 check: `BatMapList` 0-14 recoloured with the
  save's dwords, cells at x = 32·col, y = 30 + 32·row):
  - 14 of 14 occupied cells equal a recoloured template exactly, 9 Roman and 5 Numidian;
  - 154 of 154 empty cells equal image 15;
  - the Numidian cells hold only lime 3,393, black 895 and grey 832 px, with no teal.
  All three match the draft.

**Tag:** `[confirmed]` (Wine, L1 start) for Numidia's battle sprites.

## Answer

- **The setup** (`draw-20261009-141127.jsonl`):
  - FLD-RG, Rome's army 0 next to army 10 at (85,28). Army 10 was given to Numidia (`owner` 10 → 5) and the Rome-Numidia relation set to 3, the Rome-Gaul value. Positions and units are untouched: Gaul's five LI/HI units.
  - Game memory read back army 10's owner as 5.
  - The attack opened a battle titled **"Rome  v  Numidia"** (lab build s1). Header: attacker army 0, defender army 10.
- **The drawing** (`numidia_draw_check.json`): at the placement phase, all **14 occupied cells** (9 Roman, 5 Numidian: words 21, 22 and 25 at row 9) equal the `BatMapList` templates recoloured with each side's save dwords. There are **0 differing pixels over the full 32 × 32 tile** at the known offset (0, +2).
  - Numidia's dwords are `00ff00` / `000000` / `808080`.
  - **The 5 Numidian cells are lime 3,393, black 895 and grey 832 pixels**, and nothing else: no teal anywhere.
- **The ground:** all **154 empty cells** equal `BatMapList` image 15 pixel for pixel, as research found for B2 (`010c9c2`). The lime of the Numidian sprites' background is the ground tile's base lime, but it has no grass pattern, so each Numidian unit shows as a flat lime square with a black outline and a grey fill.
- **The same after one End turn:** the second phase's save and block give the same 14 cells and 154 ground cells, all exact. Its screenshot is byte-identical to the placement one, so this is one distinct image.

## Evidence

- **Data:** `runs/experiments/data/run-exp-battle-numidia-colour/`: `draw_numidia_battle.py`, `draw-20261009-141127.jsonl`, `check_battle_recolour.py`, `numidia_draw_check.json`, `SAVES.sha256`, `README.md`.
- **Release** [`run-exp-battle-numidia-colour`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-numidia-colour): `20261009-141127_NUM_start.SAV` (the L1 start), `20261009-141127_NUM_placement.SAV` and `20261009-141127_NUM_placement_window.png`, `20261009-141127_NUM_after_end_turn_1.SAV` and `…_window.png`, and the `BATTLE*.SAV` the lab build wrote.
- **Source save:** `FLD-RG_0743_rome_army0_at_86_28.SAV` (SHA-256 `39edecd1…`, release `run-exp-battle-sweep`).
- **Templates:** `TBattleMap_BatMapList.bmp` (release `run-exp-unit-icon-resources`).

## Not established

- **A natural Numidian battle** (no edit). The sprites follow only the army's owner and the nation's three dwords (`2026-10-09-battle-map-units-use-the-nation-recolour.md`), so nothing else is expected to differ `[derived]`.
- **The rest of the battle:** it was not played out. The process was killed after the second phase.
- **The desktop original.**
