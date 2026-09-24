# Map code 1 is "rough sea": a weekly weather overlay, not a terrain type

**Question** (dev-repo bug [#339](https://github.com/diegoami/imperial_conquest_2/issues/339)). Saved games carry cells that read map code `1` where the DAT reads `0` (sea). There are 19,639 such cells in 63 of the 99 corpus saves, with no unit or city on them. The DAT has no code-1 cell at all, and the count is seasonal. What writes code 1, what clears it, what reads it, what does it mean, and is the dev repo's `sea_deep` tile type a misreading of it?

## Answer

1. **Writer.** `FUN_00451304` (`0x00451304`) rolls the overlay once a week, through its per-cell painter `FUN_004511bc` (`0x004511bc`). It runs in two places: in the weekly tick `FUN_004514ec`, after the fleet loop and **before** the calendar advances, and once in new-game setup `FUN_00448aa4`, right after that function sets Spring, week 1, 270 BC. Every call first clears **every** code-1 cell within ±10 tiles of 20 fixed centres, and sets **every** fleet's `+24` word to 0. It then rolls each centre independently. The odds and radius depend on the season and week, and a hit paints a square. A cell can be painted only if it is currently code `0`, and only if no city marker (codes 20–99) lies in its 3×3 neighbourhood. When a hit lands on a fleet's marker instead, that fleet's `+24` is set to 1. `[confirmed: decompiled; 99/99 corpus saves consistent]`
2. **Readers.** Four things read code 1 differently from code 0:
   - A fleet pays **3** moves to enter a code-1 cell against 1 for code 0, and its step chooser prefers the cheaper of its candidate steps.
   - The weekly fleet storm pass triples damage (capped at 8) when the fleet's `+24` is 1. That word is `CoveredCell`, the map code under the fleet's marker.
   - The fleet panel prints `Sea-rough` when `CoveredCell` is not 0 and `Sea-calm` when it is 0.
   - The map draws terrain image 1 for the cell.

   Army movement and every "is this sea?" test (`< 2`) treat 0 and 1 alike. `[confirmed]`
3. **Meaning.** The meaning is **rough sea**, a weather state. The game's own string pair `"Sea-"` + `"calm"`/`"rough"` keys on exactly this value. The terrain table names both codes `Sea`, with costs 1 and 3. `[confirmed: strings at all_app_functions.txt:41219–41225]` Calling it "storm" is fair shorthand. It is not deep water, ice or fog. `[derived]`
4. **`sea_deep`.** The name is a misreading, but the entry itself is not wrong. Code 1 is a real row of the terrain table (name `Sea`, cost 3), so a tile type for it is legitimate. What is wrong is the meaning: "deep" water, and code 0 as "coastal" water. No cell of the world is ever statically code 1, so the exported world is right to have none. What is missing is the overlay as game state. `[derived from 1–3]`
5. **Reimplementation.** Code 1 must be modelled as **mutable per-cell state**, persisted in the save. It cannot be rederived on load, because it is one RNG draw per week. The rule, its constants and its RNG order are in [§5](#5-the-rule-for-a-reimplementation).

## Evidence

### 1. The writer: `FUN_00451304` and `FUN_004511bc`

`all_app_functions.txt:54272–54397` and `:54207–54268`. The pseudocode below uses `map[x][y]`, the in-memory grid `DAT_0045e870`, which stores 140 shorts per column (`x × 0x118 + y × 2`). `fleet[i]` is the 26-byte record at `DAT_0049c26c`. `Random(n)` is `FUN_0040284c`, the Delphi LCG `seed = seed × 0x08088405 + 1; return (n × seed) >> 32` (`:1585–1592`).

```c
void FUN_00451304() {
    for (i = 0; i < fleetCount; i++) fleet[i].coveredCell /* +24 */ = 0;    // every slot
    for (k = 0; k < 20; k++)                                                // clear
        for (x = c[k].x-10; x <= c[k].x+10; x++)
            for (y = c[k].y-10; y <= c[k].y+10; y++)
                if (map[x][y] == 1) map[x][y] = 0;
    (N, r) = table(season, week);                                            // below
    for (k = 0; k < 20; k++)                                                // roll
        if (Random(N) == 0)
            for (dx = -2r; dx <= 2r; dx++)
                for (dy = -2r; dy <= 2r; dy++)
                    if (|dx| <= r && |dy| <= r)  paint(k, dx, dy);          // inner square: always
                    else if (Random(2) == 0)     paint(k, dx, dy);          // outer ring: 50 %
}

void paint(k, dx, dy) {                                                      // FUN_004511bc
    x = c[k].x + dx;  y = c[k].y + dy;
    for (i = -1; i <= 1; i++) for (j = -1; j <= 1; j++)                      // clamped 3×3
        if (20 <= map[clamp(x+i,0,319)][clamp(y+j,0,139)] <= 99) return;     // a city is near
    if (map[x][y] == 0)                       map[x][y] = 1;
    else if (300 <= map[x][y] && map[x][y] <= 347)
        fleet[FUN_00449970(x, y)].coveredCell = 1;                           // fleet at (x,y)
}
```

| `season` (`DAT_004a032e`) | `week` (`DAT_004a0330`) | `N` (hit = 1 in N) | `r` | Painted area |
| --- | --- | ---: | ---: | --- |
| 0 Spring | < 6 (1, 3, 5) | 15 | 4 | 9×9 always, rest of 17×17 at 50 % |
| 0 Spring | ≥ 6 (7, 9, 11) | 30 | 3 | 7×7, rest of 13×13 |
| 1 Summer | any | 40 | 2 | 5×5, rest of 9×9 |
| 2 Autumn | < 7 (1, 3, 5) | 30 | 3 | 7×7, rest of 13×13 |
| 2 Autumn | ≥ 7 (7, 9, 11) | 15 | 4 | 9×9, rest of 17×17 |
| 3 Winter | any | **5** | **5** | 11×11, rest of 21×21 |

Details that matter:

- **The shape is a square (Chebyshev), not a diamond.** The inner test is `-r ≤ dx ≤ r && -r ≤ dy ≤ r`, and the outer ring spans `±2r`. `[confirmed]` `decompiled-weather-events.md` said diamond; see the correction there.
- **The exclusion is "near a city", not "near land".** Codes 20–99 are city markers (`terrain-move-cost-table-in-dat.md` §corrected movement rule). Land codes 2–11 do not block painting, and a land cell itself is simply never 0. So rough sea can touch a coast. It never touches a city tile, not even diagonally. `[confirmed]`
- **The clear box, ±10, equals the largest paint reach** (`2r = 10` in Winter). So each call removes all of last week's overlay, and code 1 lives exactly one week. `[confirmed]`
- **The 20 centres are DAT data.** `FUN_004481a0` reads `0x50` bytes into `DAT_00479540` (export of `0x004481a0`), at DAT offset **`0x1F876`**, the gap between the terrain/static tables and the mercenary name table at `0x1F8C6`. Values: `(10,10) (32,79) (74,50) (68,68) (92,68) (100,56) (105,81) (131,66) (126,89) (148,86) (177,83) (206,83) (213,70) (180,74) (158,69) (153,48) (177,24) (191,10) (209,12) (233,22)`. All lie ≥ 10 from every map edge, so the unclamped write and clear never leave the grid. `[confirmed: DAT bytes]` They are open-sea regions of the Mediterranean and the Atlantic approaches. `[derived]` The SAV has no copy of them (see `decompiled-sav-file-layout.md`). The game reloads the DAT at start-up and on New Game (`TPremierForm_InitialiseForm`, `TPremierForm_NewGame`), so they always come from the DAT. `[derived]`
- **Call sites.** In the weekly tick (`:54641`), the call comes after the fleet loop and before `week = (week+2) mod 12` and the season wrap (`:54662–54675`). So a save dated *S / W* shows the overlay rolled with the **previous** week's parameters. In `FUN_00448aa4` (new-game fill-in; not in the dump, exported from `0x00448aa4`), the call comes right after `season = 0; week = 1; year = 270`. So a brand-new game already has a Spring-week-1 overlay. `[confirmed]`
- **An edge case, not observed.** `FUN_00449970` (`:48366`) returns −1 when no live fleet stands at the position. A fleet-marker code with no matching fleet would then write through index −1. Nothing in the corpus shows this. `[confirmed as code; unobserved]`

**Nothing else writes code 1.** Every write to `DAT_0045e870` in the dump was enumerated. Every other writer copies a unit's covered cell back, writes a marker, or writes 0 (fleet or army removal). `[confirmed]`

### 2. The readers

| Reader | What it does with code 1 | Where |
| --- | --- | --- |
| Fleet step `FUN_0044dd70` | enters only `cell < 2`, pays `terrain[cell].moveCost` = **1 or 3** (DAT `0x1F622`: `Sea` 1, `Sea` 3); swaps its `+24` `CoveredCell` with the map cell as it moves, so a fleet sitting on rough water carries the 1 and restores it on leaving | `:51879–51990` (`+24` swap `:51964–51973`) |
| Fleet step cost `FUN_0044dcac` | returns the table cost (1/3), or 10 for a non-sea cell or a non-adjacent step. The walker compares the direct Bresenham step with its two alternative neighbours and takes a cheaper one, so fleets **sidestep rough cells locally** | `:51849–51872`, comparison `:51939–51952` |
| Fleet storm pass in `FUN_004514ec` | `if (*(short*)(fleet+24) == 1) dmg = min(8, dmg × 3)`. This is the `fleet[+24] == 1` of `supply-driven-morale-and-fleet-attrition.md`, and **`+24` is `CoveredCell`** | `:54565–54568` |
| `TInformation_ShowFleetDetails` `0x0043c890` | `"Sea-"` + (`CoveredCell == 0` ? `"calm"` : `"rough"`) | `:41219–41225` |
| `TUnitMap_PrintMapSquare` `0x00445b38`, `TUnitMap_PaintForm` | codes `< 12` draw terrain image *code*; code 1 has its own tile | `:45941–45946`, `:46055–46061` |
| `TUnitMap_CheckForMove` | `cell < 2` → fleet move, `cell > 1` → army move: 0 and 1 alike | `:46684–46695` |
| `FUN_0044d420`/`FUN_0044d31c` (army) | accept `2..11` only; 0 and 1 both impassable (cost 10) | `:51378`, `:51478` |
| `FUN_0044939c` (fleet placement), `FUN_0044cb40`/`cd08`/`cec8`, `FUN_0044e920`, `TAFSupply_FindProviders` | test `cell < 2` or the range 0..1: sea, either kind | `:48032`, `:50928–51171`, `:52444` |

A fleet built at a city (`FUN_0044a050`, `:48772`) starts with `CoveredCell = 0` whatever cell it was placed on. The same holds when a fleet is removed (`FUN_0044ad38`, `:49493`): it writes 0 to its cell. Both can drop a rough cell a week early. In practice a new fleet is placed next to its city, where rough sea is never painted. `[confirmed as code]`

**The weekly sequence as the player experiences it.** The overlay rolled at the end of week *W* is visible for the whole of week *W+2*, across all 16 nations' turns. A fleet that ends that week on a rough cell, whether it sailed in or the storm was painted onto it, has `CoveredCell == 1` when the next tick's storm pass runs, and takes up to triple damage. Only then is the overlay rerolled. `[confirmed: order at :54537–54641]`

### 3. The corpus agrees on all 99 saves

`FUN_004511bc` and the table above were checked against every corpus save: 49 in `saves/` and 50 in `saves-processed/`. The script reads the SAV map (the first 89,600 bytes), the calendar trailer (`len − 55 + 40/42/44`) and the fleet table, and uses the DAT for base terrain and centres.

| Check | Result |
| --- | --- |
| saves with code-1 cells / total code-1 cells | **63 / 19,639** (matches #339) |
| code-1 cells on a DAT cell that is not `0` | **0** |
| code-1 cells with a city in the 3×3 | **0** |
| code-1 cells farther than `2r` (Chebyshev) from every centre, `r` from the **generating** week | **0** |
| code-1 cells not within `2r` of a centre whose inner `(2r+1)²` square is fully rough | **0** |
| outer-ring cells painted, over hit centres (eligible cells only, not in any inner square) | 10,295 / 20,348 = **50.6 %** (rule: 50 %) |
| mean detected hits per save vs `20/N` | Winter 3.5 vs 4.0 · N=15: 1.03 vs 1.33 · N=30: 0.91 vs 0.67 · Summer 0.62 vs 0.5 |
| fleets with `CoveredCell == 1` | 1 (`1_rome_270_winter_3.sav`, on a rough cell); all others 0 |

**The previous-week rule is tested and holds.** At every season or half-season boundary where the two candidate radii differ, the largest fully rough inner square has the radius of the **pre-advance** week. There are 14 such saves: Summer 1 → 3 (from late Spring), Autumn 1 → 2, Autumn 7 → 3, Winter 1 → 4 and Spring 7 → 4. The six Spring-week-1 saves at first look contradict it: two show `r = 4`, not the Winter week 11 value of 5. They are all **270 BC**, the first turn of a new game. The overlay is `FUN_00448aa4`'s roll with Spring-week-1 parameters, which is exactly `r = 4`. `[confirmed]`

The per-label means are Spring 127, Summer 36, Autumn 143 and Winter 746 cells. The shoulder seasons are high because their stormy half, late Autumn or early Spring, feeds the next save.

## 4. `sea_deep` in the dev repo

`jq '.tileTypes'` on `data/worlds/classical-mediterranean.json` gives `sea_coastal` = code 0 and `sea_deep` = code 1. Both cite `terrain-move-cost-table-in-dat.md`, which read code 1 as "a deep/open-water versus coastal-water distinction". That reading is corrected by this report:

- **The code and cost are right.** The terrain table's entry 1 exists: `Sea`, cost 3.
- **The names are wrong.** Code 0 is all calm sea, open ocean included, not "coastal". Code 1 is transient rough sea, not "deep".
- **The world export is right to contain no code-1 cell.** The DAT has none, and the game creates them only at run time.
- **What the dev repo lacks is the overlay as state,** together with its readers: the storm-pass tripling, the "calm/rough" display, and the 3-move fleet cost applied to the week's rough cells.

The asset key `terrain.sea_deep.tile` ("darker blue, same wave motif") and the rulesets' `sea_deep` move-cost rows carry the same misnomer. `[derived]`

## 5. The rule for a reimplementation

**State.** The grid needs a `RoughSea` flag per sea cell. A code-1 value in a code-0/1 grid does the same job. Each fleet needs its `CoveredCell`, or equivalently `InRoughSea = CoveredCell == 1`. Both are persisted: the SAV map already carries the flags, and fleet `+24` carries the fleet's own. The 20 centres are static world data (DAT `0x1F876`).

**When.**

- `RollWeather(season, week)` runs in the weekly tick, after the per-fleet storm/supply loop and before the calendar advance.
- It also runs once at new game, with `(Spring, 1)`.

**Rule.**

1. Set `CoveredCell = 0` for every fleet slot.
2. For each centre, clear the flag in the 21×21 box around it.
3. Take `(N, r)` from the table in §1, using the **pre-advance** season and week.
4. For `k = 0..19` in order: `if Random(N) == 0`, then for `dx = −2r..2r` (outer loop) and `dy = −2r..2r` (inner loop):
   - paint the cell unconditionally when `|dx| ≤ r && |dy| ≤ r`;
   - otherwise paint it only when `Random(2) == 0`.

   That is one draw per centre, plus one per outer-ring cell of each hit, in that order.
5. Painting `(x, y)` does nothing if any cell of the clamped 3×3 is a city. Otherwise:
   - a calm sea cell becomes rough;
   - if a fleet stands there, that fleet's `CoveredCell` becomes 1.

**Effects.**

- A fleet pays 3 moves to enter a rough cell, and 1 to enter a calm one.
- In the storm pass, `CoveredCell == 1` applies `dmg = min(8, dmg × 3)`. This comes after the Winter `min(5, dmg × 2)` and before the not-at-own-city doubling (below).
- The fleet panel shows `Sea-rough` or `Sea-calm`.
- The map shows a distinct tile.

**A related predicate, now decompiled.** The storm pass's other test, `FUN_004494e4(fleet.owner, fleet.xy) < 0` (`:48066–48118`), returns the index of a city **owned by the fleet's nation** within the clamped 3×3, else −1. `(code − 20) & 0xF` is the marker's owner nation. So the doubling reads *not adjacent to one of its own cities*. It was previously inferred as "away from friendly coast". It does not look at allies or at land in general. `[confirmed]`

## What this does not establish

- **The tile graphic.** Nothing here shows what image 1 in the terrain image list looks like. Presumably rough water. `[open]`
- **Whether the AI steers fleets away from rough water deliberately.** The only avoidance found is the walker's local cheaper-step choice. No AI routine was found that reads the flag. `[open]`
- **The bitwise exactness of the RNG order against a live run.** The corpus confirms shapes, placement, radii and the 50 % ring. It cannot confirm the draw order without a seeded replay. `[derived from code]`
- **Why the centres are where they are.** Their values are extracted, but any design intent behind them is not. `[open]`

## Reproduction

Decompiled from `all_app_functions.txt` (lines cited above). `FUN_004481a0` and `FUN_00448aa4` are missing from the dump and were exported with `ExportAddresses.java 0x004481a0 0x00448aa4`. The corpus check is a ~90-line Python script (not committed). It reads `Imperial Conquest 2.dat` for the base grid (`<44800H` at 0) and centres (`<40h` at `0x1F876`). For each SAV it reads the grid, the calendar (`<HHH` at `len − 55 + 40`), and the fleet table at `89600 + 334×34 + 2 + armyCount×656`, with the count word first. It then applies the checks in the §3 table, taking `(N, r)` from the pre-advance week, or `(Spring, 1)` for a 270 BC Spring-week-1 save.
