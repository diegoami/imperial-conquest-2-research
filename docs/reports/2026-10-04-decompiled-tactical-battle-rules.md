# The tactical battle (`TBattleMap`), decompiled: rules, AI general, write-back and graphics

**Question.** What exactly does the original's grid battle screen do, so that v0.5.0 "Battles" can be specified, built and checked half-round for half-round against the original? This pass read the whole battle module statically; the brief listed areas 1–11.

## Answer

- **Coverage.** All 57 functions of the module were read in full: the 19 `TBattleMap` methods (`0x436FB4`–`0x437C30`) and the 38 unnamed functions `0x437C40`–`0x43ABB4`. So were the adjacent pieces: `TBattleOver_InitializeForm`/`OK`, the `TPremierForm` battle methods, `TBattleDelays`, `TInformation_BattleUnitMoves`, the recolour `FUN_0044A6C8`, the DAT loader `FUN_004481A0` and the min/max/distance helpers. The `TBATTLEMAP`, `TBATTLEOVER` and `TBATTLEDELAYS` form resources were also parsed.
- **A correction that changes every melee number.** The 5×5 "type-effectiveness matrix" in [combat-type-effectiveness-matrix.md](combat-type-effectiveness-matrix.md) is **not** the table the melee code reads. The code reads `DAT_0047946C`, and the DAT loader fills that address from DAT offset `0x1F7A6`, not `0x1F3B8`. The real matrix appears below (§5). The old 25 values are two other tables: the AI placement formations (`0x479078`, 20 words) and the AI type order (`0x4790A0`, 5 words). Recorded exchange 1 of the replay (light infantry attacking heavy infantry, the attacker losing exactly its cap) is reachable only with the real matrix. `[confirmed: code + DAT loader]`
- **No terrain.** The module never reads the strategic map, the terrain table or the army's tile. Every empty cell is the same grass tile. `[confirmed: code, global inventory]`
- **No turn limit and no retreat.** A battle ends only when one side has no live unit. Surrender is that end, reached on purpose. `[confirmed: code]`
- **No siege battles.** The battle screen opens only from army-attacks-army `FUN_0044AEE4`, or from loading a save with the battle flag set. `[confirmed: whole-CODE E8 scan]`
- **Unit icons: 5 types × 3 sizes = 15 base icons**, 32 × 32. A unit's size is `min(2, troops div (standardBattalion div 3))`. Each side's copy is recoloured from its nation's three colours. A routed unit has no image: its cell becomes empty. `[confirmed: code + resource]`
- **Slot word `+2` (`DAT_004A0348`) is the origin label.** It is `0` for a national unit and non-zero for a mercenary. It is used only for display (" mercenaries") and is written back. `[confirmed: code]`
- **Promotion is located.** `TBattleOver_OK` sets each surviving winner unit's quality to `max(6, q)`, then raises it by 1 (to at most 9) on `Random(4) = 0`. `[confirmed: code]` This replaces the empirical reading of [battle-replayed-rout-mechanic-and-combat-constants.md](battle-replayed-rout-mechanic-and-combat-constants.md).

## Method

- Read `all_app_functions.txt` lines 37432–40297 (the module) in full, and the helpers by `grep -n` and `sed -n`.
- `EnemyUnitDetails` (`0x4378F8`) is not a function in the Ghidra project. It was disassembled with a read-only Ghidra post-script, `DisRange.java`, kept in the session scratchpad.
- Checked the nested procedures' parent-frame offsets against the listing: `FUN_00438D24` stores the slot at `EBP−6` and the target cell at `EBP−0xA`; `FUN_0043A160` stores the slot at `EBP−2` and the target at `EBP−4`.
- Read the DAT loader `FUN_004481A0` from `scratch/datload.txt`. It reads the DAT sequentially, so summing its block lengths gives each table's DAT offset. The stat table lands at `0x1F2F0`, where `find("Light infantry")` puts it, which validates the method.
- Scanned the `CODE` section for `E8 rel32` calls to the battle entry points and to `Random` (`0x40284C`).
- Parsed the `TPF0` resources with a small Python reader, and rendered the image list and glyphs locally (scratchpad only) to describe them. No bitmap, DAT or EXE bytes are reproduced here.

## 1. State, grid and battle block (areas 1, 11)

**Battle block** (saved in this order after the battle flag, `FUN_004484D0`) `[confirmed: code]`:

| Address | Size | Field |
| --- | --- | --- |
| `0x4A0B7C` | 1 | battle in progress |
| `0x4A0B74` | 2 | attacker army (side 0) |
| `0x4A0B76` | 2 | defender army (side 1) |
| `0x4A0B78` | 2 | side to move: 0 attacker, 1 defender |
| `0x4A0B7D` | 1 | placement finished |
| `0x4A0B7A` | 2 | half-round counter |
| `0x4A0344` | 40 × 44 | unit slots: 0–19 attacker, 20–39 defender |
| `0x4A0A24` | 14 × 12 words | grid, `cell(x,y) = [x·12 + y]` |

**Unit slot**, 22 words, every field now named:

| Word | Address | Field |
| --- | --- | --- |
| 0, 1 | `0x4A0344/46` | x (0–13), y (0–11) |
| 2 | `0x4A0348` | origin label: 0 national, > 0 mercenary (army unit `+0`) |
| 3 | `0x4A034A` | type: 0 LI, 1 HI, 2 archers, 3 LC, 4 HC |
| 4 | `0x4A034C` | troops (0 = not in the battle) |
| 5 | `0x4A034E` | quality (constant during the battle) |
| 6 | `0x4A0350` | battle morale |
| 7 | `0x4A0352` | moves left this half-round |
| 8 | `0x4A0354` | shots left for the battle (initially stat `+0x1C`: 7/0/25/9/0) |
| 9 | `0x4A0356` | melee target slot, −1 none |
| 10–21 | `0x4A0358` | name, 24 bytes |

**Grid** `[confirmed: FUN_00437C40, TBattleMap_PrintSquare]`:

- A grid cell holds an **icon code, not a slot**. This corrects the feasibility report's "otherwise a unit slot".
- Codes: `50` is empty; `type·3 + size` for the attacker (0–14); `type·3 + size + 20` for the defender (20–34). The size is `min(2, troops div (std div 3))`.
- The slot at a cell is found by scanning the 40 slots for a live unit with that position (`FUN_004383BC`). When two units share a cell, the last one in the scan wins.

**Geometry and terrain.** The grid is 14 × 12 cells of 32 px. The map is drawn at `(32x, 32y + 30)` in a 448 × 414 client area. The distance is Chebyshev, `max(|dx|,|dy|)` (`FUN_00449018`), and adjacent means distance 1. There is no terrain, no impassable cell, and no movement-cost or modifier table. `[confirmed: code]`

## 2. Deployment (area 2)

**Copy-in** (`FUN_00437DE4`, fresh battles only) `[confirmed: code]`:

1. For each side whose nation is computer-controlled (nation `+0x490 = 0`):
   - The **strategic** army morale `+14` gets `+= 3`. The change persists in the army record.
   - The army's 20 unit records are selection-sorted, descending, in place (`FUN_00437D10`). The key is `troops · M[type][0] div M[0][type]`, which multiplies troops by {LI 1, HI 15, archers 0.5, LC 5, HC 6} in integer form. The sort uses `i = 0..18`, `j = i+1..19`, a strict `>`, and swaps whole records. This order is persistent and also fixes the AI's iteration order.
   - The nation adopts the opponent nation's two pause settings (`+0x48C`, `+0x48E`).
2. The grid is set to all 50, and troops to 0 in all 40 slots.
3. For each attacker army slot `s` = 0..19 with troops > 0, in order:
   - position `(s mod 13, s div 13)`;
   - copy origin, type, troops, quality and name; shots from the stat table;
   - `morale = max(60, min(90, Random(q·4) + army+14))`;
   - set the grid code.
4. The same for the defender, at `(s mod 13, 11 − s div 13)`.
5. `flag = 1`, side = 1, counter = 0, then the half-round setup.

**Placement.** The defender places first (half-round 1). The attacker places second (half-round 2), and then moves first (half-round 3).

**Human placement** (`TBattleMap_PlaceUnit`) `[confirmed: code]`:

- Left-click an own unit, then left-click an empty cell.
- The cell must be in the side's home rows: attacker `y < 3`, defender `y > 8`.
- Placement is free and repeatable during the side's placement half-round.
- Not placing keeps the copy-in positions.

**AI placement** (`FUN_004381A4`) `[confirmed: code]`:

1. Clear the side's cells, then draw `r = Random(5)`.
2. The base row is 2 with a step of −1 (attacker), or 9 with a step of +1 (defender).
3. For each block `g` = 0..3:
   - the type is `t = Form[r][g]`, and the columns are `3g+1 … 3g+3`;
   - place every live own unit of type `t`, in slot order, filling columns, then the next row;
   - after the third row the row is held at the third row, so a block with more than 9 units **stacks units on occupied cells**;
   - when `t` = HI, archers follow in the same block, continuing the same counters.

`Form` comes from the DAT, at `0x479078` (DAT `0x1F3B8`):

| r | Columns 1–3 | Columns 4–6 | Columns 7–9 | Columns 10–12 |
| --- | --- | --- | --- | --- |
| 0 | HC | HI + Ar | LI | LC |
| 1 | LI | HI + Ar | HC | LC |
| 2 | LC | HC | LI | HI + Ar |
| 3 | LC | LI | HI + Ar | HC |
| 4 | HC | LC | HI + Ar | LI |

## 3. The half-round loop and movement (area 3)

**The loop** `[confirmed: code]`. There is no initiative stat: sides alternate, and the attacker moves first.

**Half-round setup** (`FUN_00439968`, which is also the resume path):

1. Set the side's nation and its own/enemy slot bases. Set the caption `"A  v  D          N to place units."` (or `to move units.`).
2. Compute `dmin`, the minimum distance between any live own unit and any live enemy unit.
3. For each of the side's **20** slots:
   - `target = −1`;
   - `moves = stat moves` (4/2/4/6/5);
   - if the side is computer-controlled, the type is not HI, `dmin > 2` and `counter < 10` (read before the increment), then `moves = 1` (the AI's slow advance).
4. Clear the 40 AI claims, then `counter += 1`.

**Half-round end** (`FUN_00439C20`):

1. Advance the phase. During placement, side 1 → 0, and side 0 → `placed = 1` with no side change. Afterwards the side toggles.
2. Resolve melee **for the side that just moved** (`FUN_004393EC`), using the targets it set.
3. If the battle is not over, set up the next half-round.

**Who drives a half-round** (`FUN_00439C84`):

- The general loop runs while the side's nation is computer-controlled, or *Computer general* is on for that side, and the battle is not over. Each pass is placement or the AI move, then the half-round end.
- A human side waits for clicks. *End turn* calls the half-round end, then the loop.
- *Computer general* sets the flag for the side to move. A left click on the Information window during the AI's turn clears the flag and leaves the half-round unfinished, for the human to complete.

**Human actions** (`OnMapClick`):

- Left on a unit: select it and show its details.
- Left on an empty cell with a unit selected: place it (during placement) or move it.
- Left on an adjacent enemy, with the selected unit's `moves ≥ 1`: set the melee target. This costs no move.
- Right on an enemy, with the selected unit's shots > 0, moves > 0 and distance ≤ range: shoot.
- Right on an own unit: clear its target.
- Moving a unit clears its target.

**Movement** (`FUN_00438D24` with its step `FUN_00438A6C`):

- **The path.** An 8-connected Bresenham line to the destination: `err = 2·minor − major`. While `err ≥ 0`, take a minor step and `err −= 2·major`. Then take the major step and `err += 2·minor`.
- **One step costs one move.** The unit goes to the path cell when it is empty.
- **Detours.** If the path cell is blocked, two alternatives are tried:
  - along a column: `(px±1, py)`;
  - along a row: `(px, py±1)`;
  - diagonally: `(ux+sx, uy)` and `(ux, uy+sy)` from the unit, swapped when y is the major axis.
- **Cost.** A cell costs 1 if it is on the grid, empty, and within distance 1 of both the path cursor and the unit; otherwise it costs 10.
- **Choice.** Take the cheaper alternative when it is cheaper than the path cell, ties to the first.
- **Stop** when moves < 1, the chosen cost is > 9, or the path reaches an occupied destination.
- **Computer-controlled only:**
  - a unit with a target does not move;
  - before spending its **last** move, a unit forfeits it (moves := 0) if the 3 × 3 around the next path cell holds an enemy at least as strong as itself (`S = (troops·q div 100)·m·M[me][them]`);
  - each loop iteration first checks two things. If the unit is adjacent to the enemy at the destination and (`moves < 2` or `shots < 1`) and (it is not archers or `shots < 1`), it sets that target and stops. If the enemy is in range, the unit has moves and shots, and it has no target, it shoots once and re-checks.
- **The human second call.** `MoveHumanUnit` calls the move twice when the first call did not arrive.
- The inner `if (err > 0) step` is dead code.

## 4. Shooting (area 4) `[confirmed: code]`

- **Who and how far.** Types with shots: LI (range 1), archers (range 2), LC (range 1). The range test is `distance ≤ range`. There is no line-of-sight test for shooting.
- **What a shot (`FUN_0043910C`) does:**

```text
shots_s -= 1; moves_s -= 1; target_s = -1
base = (tr_s·q_s·m_s·vuln[type_t]) div (tr_s·5 + 150000)       // int32
if dist(s,t) < range[type_s]: base *= 2                          // only archers at distance 1
n    = min(base, min(tr_s div 3, tr_t div 2)) + 1                // 16-bit min
loss = Random(n) + Random(n)
m_t -= min(3, (loss·35) div (tr_t + 1))                          // troops before the loss
tr_t -= loss
Rout(t)
```

- `vuln` is stat `+0x20` (18/2/18/15/4).

## 5. Melee (area 5) `[confirmed: code]`

**The real matrix** (`DAT_0047946C`, DAT `0x1F7A6`), `M[attackerType][defenderType]`:

| Attacker \ defender | LI | HI | Ar | LC | HC |
| --- | ---: | ---: | ---: | ---: | ---: |
| LI | 15 | 4 | 20 | 5 | 3 |
| HI | 60 | 5 | 65 | 15 | 8 |
| Ar | 10 | 3 | 18 | 5 | 3 |
| LC | 25 | 8 | 28 | 15 | 8 |
| HC | 18 | 12 | 20 | 12 | 8 |

**Initiation.** At the end of the moving side's half-round, each own slot in order with troops > 0, a target ≥ 0 and target troops > 0 resolves its melee:

```text
f  = min(4, #own slots (alive or not) whose target == d)        // ≥ 1
A  = (M[ta][td]·tr_a·(q_a·10+m_a)) div 2000 + 12
D  = (M[td][ta]·tr_d·(q_d·10+m_d)) div 2000 + 12
nA = ((tr_a·D) div A) div 12 + 1
la = min(30000, ((Random(nA)+Random(nA))·(5−f)) div 5);  la = min(la, (tr_a·4) div 10) + 1
nD = ((tr_d·A) div D) div 10 + 1
ld = min(30000, ((Random(nD)+Random(nD))·(2f+5)) div 5); ld = min(ld, (tr_d·4) div 10) + 1
if tr_d div ld < tr_a div la: m_a = min(99,m_a+2); m_d = min(99,m_d−3)
else:                         m_a = min(99,m_a−3); m_d = min(99,m_d+2)
tr_a -= la; tr_d -= ld
Rout(a); Rout(d)
```

- The target persists until the side's next half-round setup.
- A **corrected morale rule**: the side that lost the larger fraction of its troops (by the integer ratio `troops div loss`) takes −3, and the other +2. Ties go against the attacker. This was described as "the better power ratio" in [decompiled-combat-formula-structure.md](decompiled-combat-formula-structure.md).

## 6. Morale and rout (area 6) `[confirmed: code]`

- **Initial morale.** As in §2.
- **The deltas:**

| Trigger | Change |
| --- | --- |
| Shot hit | target −min(3, ⌊35·loss/(troops+1)⌋) |
| Melee | ±2 / −3, as in §5 |
| A friendly unit routs | −6 to every live friend |
| An enemy unit routs | +5 to every live enemy, capped at 99 |

- There is no floor and no recovery between half-rounds.

**`Rout(u)`** (`FUN_00438FB0`):

```text
if tr_u ≥ std(type) div 25 and m_u > 19:
    if m_u > 39: return
    if Random(m_u) + Random(m_u) > 29: return
remove u (troops 0, cell empty)
for live friends: m −= 6; if m < 30: remove (no further cascade)
for live enemies: m = min(99, m+5); if target == u: target = −1
if either side has no live unit: battle over
```

- **Surrender** removes every own unit with no cascade, ends the battle and ends the half-round.

## 7. The AI general (area 7) `[confirmed: code]`

The AI's movement half-round is `FUN_0043A31C`. It takes types in the order `[1, 4, 3, 0, 2]` from `0x4790A0` (HI, HC, LC, LI, archers). Within each type, it takes the side's live units in slot order.

**Pass 1, choose and engage.**

- **Target choice** (`FUN_00439E08`), by the unit's type:
  - LI prefers archers, then LI, then any;
  - HI prefers HI, then any;
  - HC prefers HI, then any;
  - archers and LC take any.
- **The target score.** Among the live enemies of the wanted type, take the minimum of `v = tr·q·m·M[their][my] div 10000`. Let `c` = focus count + claims. `v` becomes `v div (c+1)` when `c < 4`, else `v·2`. Ties go to the first. The unit's claim is recorded.
- **Engage** (`FUN_0043A160`):
  - archers with shots at distance < 3: fire until moves = 0, shots = 0, or the target is removed;
  - else if adjacent: shoot while shots > 0 until moves = 1 or shots = 0, then set the melee target if the enemy lives;
  - else if the line is clear: move toward the target;
  - else: move toward the nearest empty cell with a clear line in the (2r+1)² box around the target (r = 2 for archers, 1 otherwise; dx outer, dy inner; strict <).

**Pass 2** (`FUN_0043A544`). For each unit with moves > 0 and no target:

- If it has shots, it picks the in-range enemy minimising `troops div s`, where `s = shotBound` (`n` above), plus `s div 4` if the enemy has shots. It fires until moves = 0 or the target is removed. **This loop does not check shots**, so shots can go negative.
- It then takes as melee target the adjacent enemy minimising `theirs' = theirs − focus·theirs`, subject to `2·theirs' div 3 < mine`.

**Pass 3** (`FUN_0043ABB4`):

- For units with moves > 0 and no target: sort the enemies by threat (ascending `tr·q·m·M[their][my] div 10000`; archers with shots use `−shotBound`, so the most damage comes first), with a selection sort. Pick the first enemy with a clear line, or an empty cell with a clear line in its box, and move there.
- Then run pass 2.
- Then the **flank**: each unit with no target whose moves are untouched (or `= 1` with `counter < 10` and type ≠ HI) gets a horizontal direction `h`:
  - `h = −1` if the enemy's `minX ≤ 13 − maxX`, else `+1`;
  - `Random(3) = 0` flips `h`;
  - the vertical direction is the sign of (enemies below − enemies above), with 0 taken as −1;
  - the unit tries `(x+moves·h, y+moves·v)`, then `(x+moves·h, y)`, clamped, each needing an empty cell and a clear line.
- Then pass 2 again.

**The clear-line test** (`FUN_00439F00`) walks the same Bresenham line and requires the cells strictly between the two ends to be empty. Adjacent counts as clear.

## 8. End conditions (area 8) `[confirmed: code]`

- The battle is over when, after any rout, side 0 or side 1 has no live unit, or after *Surrender*. Nothing else ends it: no half-round limit, and no retreat.
- The window's close is refused unless the application is quitting (`CheckQuit`).
- The winner is the attacker if any attacker slot has troops > 0, else the defender. If both sides are emptied, the defender "wins" with no units `[derived: unexercised edge]`.

## 9. Write-back (area 9) `[confirmed: TBattleOver_InitializeForm/OK]`

**The result dialog** ("Battle ended") shows:

- `"W's  army  defeats  L's  army."`;
- per type and in total: the winner's start (its strategic army before the write-back), the winner's finish (the battle survivors) and the loser's start (the loser finishes at 0);
- `"The army of W captured N talents."` / `"no money."`;
- `"… N tons of supplies."` / `"no suuplies."` (sic).

**OK** does the following, in order:

1. Zero the winner army's 20 unit troops. Copy each surviving battle slot, compacted in slot order, into units 0, 1, … (origin, type, troops, name). Each gets `quality = max(6, q)`, then on **`Random(4) = 0`** `quality = min(9, quality + 1)`.
2. The winner's money += the loser's money. The winner's supplies += the loser's supplies, then `min(supplies, totalTroops div 100)`.
3. Redraw the winner's marker (`FUN_0044A80C`), and delete the loser army (`FUN_0044AB90`, tombstone).
4. Unity: winner `min(990, +25)`, loser `−25`.
5. News: `"W destroys army of L."`.
6. The peace dialog, as in [decompiled-war-cascade-and-peace-paths.md](decompiled-war-cascade-and-peace-paths.md): a human–AI battle with `strength(W) < strength(L)`, `unity(L) > 500` and `cities(L) > 7` draws **`Random(5) < 2`** after those tests; human vs human always shows `THVHBatPols`.

There is no other strategic morale change. The AI army's `+3` from copy-in stays. The attacker's moves were set to 0 by `FUN_0044AEE4` before the battle.

## 10. UI and unit drawing (area 10) `[confirmed: code + TBATTLEMAP resource]`

**The form.** `TBattleMap` is titled "Battlefield", has a 448 × 414 client area and is stay-on-top. It is placed at left 2, and the Information window is moved beside it (x 458, 330 × 414).

**The toolbar.** A 28 px panel holds eight 22 × 22 speed buttons with 20 × 20 glyphs, left to right:

| Button | Glyph | Action |
| --- | --- | --- |
| Unit moves | spear on green | list own units: name, type, `mv`, `sh`, attack target |
| Friendly units | white skull on green | own units: name, type, troops, Q tier, M tier |
| Enemy units | black skull on green | enemy units: name, type, troops |
| Cancel selection | empty circle | deselect |
| End turn | red curved arrow | end the half-round |
| Change pauses | hourglass | dialog: shot delay and attack delay, 0–3.0 s in 0.1 s / 1.0 s steps; UI only |
| Computer general on | castle wall | AI plays this side |
| Surrender | white flag on red | "Are you sure you want to surrender ?" |

There is no menu.

**The side panel** is the Information window:

- **Unit details:** nation, name (+ " mercenaries"), type and troops. For the side to move it adds Quality, the Morale tier `(m − 27) div 8` into very low ×5 / low / normal / high / very high / excellent, Moves, Shots, and "Unit set to attack" with the target.
- **Exchange panels:** `SHOOTS AT` with `TROOP LOSSES n` or `Unit destroyed !`; `ATTACKS` with `UNIT  LOSSES`, attacker/defender `n` or `routed`.

**The images.** `BatMapList` is a 32 × 32 image list of 17 images, stored as one 128 × 160, 8 bpp bitmap with a mask:

- 0–2: LI (a spear and sword crossed), small, medium, large;
- 3–5: HI (a shield with crossed swords);
- 6–8: archers (a bow and arrow);
- 9–11: LC (a horse's head over two lances);
- 12–14: HC (a horse's head on a shield);
- 15: the empty-cell grass tile (green, with brown contour lines);
- 16: the selection cursor (a black diamond on white, drawn with raster op `0x440328`, SRCERASE).

**How a unit is drawn:**

- In each unit icon, the purple background `0x800080` becomes nation colour `+0x424`, white becomes `+0x428` and blue becomes `+0x42C` (`FUN_0044A6C8`). The green dotted cell border is kept.
- The attacker's 15 recoloured copies are `UnitsList` 0–14, and the defender's are 15–29.
- The **size thresholds** are `troops < std div 3` → small, `< 2·(std div 3)` → medium, otherwise large. That gives LI 5,000/10,000, HI 2,000/4,000, archers 1,166/2,332, LC 2,333/4,666 and HC 833/1,666. The icon is recomputed after every loss.
- There is no routed, selected or wounded image. Selection and the AI's highlight of attacker and target use the cursor overlay.

**For the clone:** 15 unit icons (5 types × 3 sizes) with three recolourable regions, one ground tile, one cursor, and eight toolbar glyphs.

## Every `Random` call, in draw order

There are 12 sites in the module, confirmed by the `E8` scan: `0x43801A`, `0x43812F`, `0x43820D`, `0x438FFB`, `0x439006`, `0x439188`, `0x439191`, `0x439557`, `0x43955F`, `0x4395CE`, `0x4395D8` and `0x43AA88`. There are two more after the battle: `0x4592BD` and `0x45951C`.

1. **Copy-in:** `Random(q·4)` per live attacker slot 0..19, then per live defender slot. `Random(0)` still advances the seed.
2. **Placement half-rounds** (defender, then attacker): `Random(5)` for each computer-controlled side.
3. **Movement half-rounds:**
   - each shot: `Random(n)`, `Random(n)`, then `Rout(target)`;
   - each `Rout`: 2 draws, only when `troops ≥ floor` and `20 ≤ m ≤ 39`;
   - each flank: `Random(3)`.
   - The order of all these follows the AI passes of §7, or the human's clicks.
4. **End of each half-round:** melee per own slot in order. Each draws 4 (attacker, attacker, defender, defender), then `Rout(attacker)`, then `Rout(defender)`.
5. **After the battle:** `Random(4)` per surviving winner unit in slot order, then the possible `Random(5)`. `TBattlePols` then reseeds.

## Inferences, kept apart

- **int32 wrap is possible.** Delphi integer products wrap with no overflow check. The overflow-prone terms are melee `tr·D`, which overflows above about 23,000 troops against a high-power defender, and pass 2's `theirs − focus·theirs` when `focus ≥ 4`. `[derived]`
- **The interrupt window.** It is the Information window `DAT_0045E70C` (`FUN_00416360` is taken to be its handle). `[derived]`
- **Resuming a lab snapshot is not a continuation.** The lab hooks sit at the calls to the half-round end, so a snapshot is the state **after a side's moves and before its melee**. Loading one re-runs that side's half-round setup: moves and targets are reset and the counter is incremented again. So the pending melee is lost, and the slow-advance window shifts by one half-round. This explains why runs C/D restarted at "Rome to place units". `[derived from code; consistent with the feasibility runs]`

## What the EXPLORE golden master should check

Each check is seeded and taken half-round for half-round.

1. **Copy-in morale:** every slot's morale equals the formula under the seed. The AI army's unit order equals the §2 sort, and the strategic `+14` goes up by 3.
2. **AI placement:** the positions match `Form[Random(5)]`. An army of more than 9 HI + archers should show stacked cells.
3. **Grid codes:** they equal `type·3 + size (+20)` after every exchange.
4. **Setup:** moves are reset, targets are −1, and moves = 1 for non-HI AI units while `dmin > 2` and the counter is ≤ 10.
5. **Every shot:** the loss from `n` and the logged seed, the morale −min(3, …) and the shot/move decrements. AI shots can go negative.
6. **Every melee:** both losses, the cap, the `(5−f)/(2f+5)` factors, and the ±2/−3 by troop ratio.
7. **The real matrix:** an LI-vs-HI melee should produce the attacker's cap often. It discriminates against the old table.
8. **Rout:** the floor, the 20–39 two-draw test, the cascade −6/<30 and +5/99, and the target clearing.
9. **The AI path:** each unit's destination and path, the detours, and the last-move danger forfeit.
10. **The end:** the winner, compaction, `max(6, q)` plus `Random(4)` promotion, money, the supply cap, unity ±25 and the news line.
11. **Snapshot semantics:** whether a resumed snapshot reproduces the inference above.

## What this does not establish

- No battle was run in this pass. Everything is static, and the golden master is still to come.
- The `TInformation` window's own painting and layout were not read. The text lines are known; their pixel layout is not.
- `FUN_0044A80C`, `FUN_0044AB90`, `FUN_0044A8CC`, `TBattlePols` and `THVHBatPols` are taken from earlier reports, not re-read.
- The nation colour fields `+0x424/+0x428/+0x42C` are named only by their use here. Which colours each nation has was not read.

## Reproduction

- Read `all_app_functions.txt` `:37432–40297`, `:57359–57687` and `:59086–59140`. Read `scratch/datload.txt` for `FUN_004481A0`.
- Ghidra `analyzeHeadless … -readOnly -postScript DisRange.java out.txt 004378f8 00437a60`, and `DumpListing.java` for the frame offsets.
- Python, kept in the scratchpad: a PE resource walker plus a `TPF0` reader for `TBATTLEMAP`, `TBATTLEOVER` and `TBATTLEDELAYS`; an `E8 rel32` scan of `CODE`; and DAT offsets summed from the loader's block lengths.
