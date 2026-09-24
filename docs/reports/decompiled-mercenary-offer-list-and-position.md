# Mercenary offers are hired by position: adjacency for the player, radius 4 for the AI

## The question

Every mercenary-pool offer carries an `(x, y)` ([mercenary-pool-record.md](mercenary-pool-record.md): the one controlled hire consumed slot 33 at Felsina's exact tile). Does that position gate hiring? Specifically:

1. How does the `TRecruitMercs` dialog build the list of offers it shows? Does it filter by distance from the army, by the city's owner, by nation, or not at all?
2. Does `TUnitMap_RecruitMercenaries` (`0x00446FF4`) or `TRecruitMercs_RecruitMercUnit` (`0x00441360`) apply a position condition?
3. Does the AI hire mercenaries, and if so, does it use position the same way the player does?
4. Where is the offer's `(x, y)` written, is it always a city tile, and what else reads it?

## Answer

1. **The dialog lists the offers on one city tile, and only those.** `TRecruitMercs_InitializeForm` asks `FUN_00449D08` for "the city of the first live offer adjacent to this army". It then lists every live offer whose `(x, y)` equals that city's tile **exactly**. It does not filter by the city's owner, by the offer's `Label`, or by nation. There is no radius in the list-fill; the distance test happens once, in `FUN_00449D08`. `[confirmed]`
2. **The position gate is in the order, not in the hire.** `TUnitMap_RecruitMercenaries` calls the same `FUN_00449D08`. If no live offer lies at **Chebyshev distance exactly 1** from the army (`FUN_004492A0`: `FUN_00449018(a, b) == 1`), the order does **nothing and shows no message**. The order's other gates are: the army is 20 units full, it holds more than 100,000 troops, the city's owner is at war with the player, it has too few supplies, or its fleet is full. `TRecruitMercs_RecruitMercUnit` has no position check of its own and relies on the list it was given. `[confirmed]`
3. **The AI hires with a different, far looser rule.** `FUN_0044E41C` runs for each of a computer nation's armies at the start of its turn. It hires **every** live offer on the tile of **any** city within **Chebyshev distance < 5 (radius 4)**. It requires the nation to be at war with someone, the army to hold more than 50 money and the AI's relation toward the city's owner to be anything but war. It has **no cost check, no money deduction, no 100,000-troop cap, no supply check and no fleet check**. A second routine, `FUN_0044E84C`, steers AI armies toward the nearest offer city within radius 19. Across 20 single-turn save pairs, the rule predicts all 10 observed AI hires. Its only miss is an army absorbed into another army that same turn. It also predicts correctly that an army sitting adjacent to an offer for 10 turns never hires, because its nation was at peace. `[confirmed: code + saves]`
4. **`(x, y)` is written only by the quarterly restock `FUN_00449130`**, apart from the DAT and SAV loaders. The restock copies it from the fixed template table, and **all 201 templates sit on a city tile** (134 distinct cities). Neither hire routine ever writes `(x, y)`: both only set `troops = 0xFFFF`, so an empty slot keeps its last position. `(x, y)` is read by the player gate, the dialog, the AI hire, the AI seek, the city-info panel and the area-map overlay, and by nothing else. A byte scan of the whole EXE found 28 absolute references into the table, all in the functions named here. `[confirmed]`

A byproduct: the DAT offset of the template table and of the `Label` name table was located, which **resolves `Label`**. It indexes 52 ethnic names (`0 = Regular`, `11 = Gallic`, `35 = Egyptian`, …). See §5.

**For a reimplementation:** yes, a faithful engine needs a position on every pool slot, and that position is a city tile. The player may hire only when the army is at Chebyshev distance exactly 1 from the city holding the offers, and then only from that one city. The AI hires automatically from every city within Chebyshev distance ≤ 4 under its own gates (at war, money > 50, not at war with the owner, fewer than 20 units), with no cost check, no money deducted and no troop cap.

---

## Record layout used below

The runtime table starts at `0x0049D0A4`, with a 12-byte stride. Records `0`–`200` are the **templates**; records `201`–`250` (base `0x0049DA10`) are the **50 live slots** that the SAV stores. Within a record:

| Offset | Field |
| ---: | --- |
| `+0` | `x` |
| `+2` | `y` |
| `+4` | `Label` (name-table index) |
| `+6` | unit type |
| `+8` | troops (`0xFFFF` = empty) |
| `+10` | quality |

Earlier reports cite `+0 label … +6 quality`. Those offsets are relative to `0x0049D0A8`, the address the hire code indexes from. It is the same record.

## 1. The player's gate: `FUN_00449D08` and `FUN_004492A0`

`FUN_00449D08(army, out city)` (`all_app_functions.txt:48572–48592`):

```c
*city = -1;
for (i = 201; *city == -1 && i < 251; i++)                // live slots only
    if (pool[i].troops >= 0 &&                            // live offer
        FUN_004492a0(army.xy, pool[i].xy))                // Chebyshev == 1
        *city = FUN_004498d8(pool[i].xy);                 // city whose tile == offer tile
```

- `FUN_004492A0` (`:47907–47916`) is `return FUN_00449018(a, b) == 1;`, and `FUN_00449018` is the Chebyshev metric ([decompiled-mobilization-and-mercenary-restock.md](decompiled-mobilization-and-mercenary-restock.md) §3). So the test is **adjacent**, not "within 1", the same as the mobilization receiving-army test. `[confirmed]`
- `FUN_004498D8` (`:48312–48330`) scans the 334 cities for one whose `+0xE`/`+0x10` tile equals the offer's tile. It returns `-1` if there is none, and the loop then continues. `[confirmed]`
- **The first slot in slot order wins.** An army adjacent to two offer cities can reach only the city of the lower-numbered live slot. This can only happen when two offer cities are Chebyshev distance 2 apart. In the DAT, the closest pair of cities is exactly 2 apart, and exactly one pair of *template* cities is: `(156,80)`/`(158,78)`, Gortyna and Cnossus. `[confirmed: code]`, `[derived: reachability]`

`TUnitMap_RecruitMercenaries` (`0x00446FF4`, `:46858–46925`; instruction listing `0x00447058–0x00447062`):

```c
army = selectedFleet >= 0 ? fleet.carriedArmy : selectedArmy;
if (army >= 0 && army.owner == currentNation) {
    total = FUN_0044a698(army);
    FUN_00449d08(army, &city);
    if (city >= 0) {                                   // else: silent no-op
        if (army.slot[19].troops > 0)            "This army already has 20 units."
        else if (total > 100000)                 "This army cannot get any bigger."
        else if (relation[city.owner][me] == 3)  "You cannot recruit from an enemy city."
        else if (army.supplies*10000/total < 15) "No mercenaries will join an army with so few supplies."
        else if (fleet >= 0 && total/500 > fleet.ships)    "Your fleet cannot carry any more troops."
        else open TRecruitMercs
    }
}
```

`[confirmed]`. Three consequences:

- **An army that is not adjacent to an offer gets no feedback at all.** Unlike every other refusal, this one has no message. `[confirmed: JLE 0x00447186 straight to the epilogue]`
- **No ownership requirement.** Own, allied, neutral and peaceful foreign cities all qualify. The only refusal is the owner's relation toward the player being `3` (war; codes from [decompiled-diplomacy-peace-terms-and-instant-battles.md](decompiled-diplomacy-peace-terms-and-instant-battles.md)). `[confirmed]`
- The supply gate is `supplies ≥ 0.15 %` of troops. The army's supply cap is `troops div 100 + 1` ([supply-capacity-rounding.md](supply-capacity-rounding.md)), so this is about 15 % of a full load. `[derived]`

## 2. The list-fill: `TRecruitMercs_InitializeForm` (`0x00440FEC`, `:43490–43575`)

```c
army  = TUnitMap.selectedArmy;                        // DAT_0045e740 + 0x220
FUN_00449d08(army, &city);                            // same gate, recomputed
caption = "Units at " + city.name;
fleet = (army.+8 == -1) ? FUN_00449970(army.xy) : -1; // embarked army -> its fleet
n = 0;
for (i = 201; i < 251; i++)                           // :43536-43549
    if (pool[i].troops >= 0 && pool[i].x == city.x && pool[i].y == city.y) {
        list[n] = i;
        n = min(9, n + 1);                            // FUN_00448fd0 = min
    }
for each list entry: name[label] + "  " + typeName[type] + "  " + troops + "  " + qualityName[quality]
```

`[confirmed]`

- **The filter is exact tile equality with the chosen city.** There is no radius here, no owner or nation test, and no `Label` test. `[confirmed]`
- **At most 10 lines.** The index clamps at 9, so if an 11th offer matched it would overwrite the 10th. No sampled city has anywhere near 10 live offers (Felsina has 4 templates), so this is academic. `[confirmed: code]`
- `TRecruitMercs_ChangeUnit` (`0x00441274`) only displays the selected offer's cost. `TRecruitMercs_RecruitMercUnit` (`0x00441360`) checks money, the 100,000 cap and fleet space, copies the offer into slot `FUN_0044a66c(army)`, and sets the offer's troops to `0xFFFF`. It never reads `(x, y)`, which matches the existing account ([decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md)). `[confirmed]`

**Against the one controlled player hire** (`1_rome_270_winter_1` → `_winter_3`): Rome's army 0 was at `(98,28)` (distance 3 from Felsina `(98,31)`) and ended at `(99,30)`, distance **1**, holding the `Gallic` unit. That fits the rule: at distance 3 the order would have done nothing. It does not *prove* the rule, since the save pair does not show whether a hire was tried at distance 3. `[consistent]`

## 3. The AI: `FUN_0044E41C` (hire) and `FUN_0044E84C` (seek)

**Only computer nations reach them** `[confirmed]`. The chain is `FUN_00451FDC` (loops while the current nation's `+0x490` flag is `0`, i.e. computer) → `FUN_0044FA20` (`:53210`) → `FUN_0044F31C` (`:52901`), which calls `FUN_0044E41C(army)` for every army of the acting nation (`:52926`). These calls run while `DAT_004A0B7C == 0`, the battle-in-progress flag.

`FUN_0044E41C(army)` (`:52218–52278`):

```c
money   = army.money;                                 // +0xC
atWar   = FUN_00449cd8(me);                           // any relation == 3
lastPlus1 = FUN_0044a66c(army);
for (c = 0; c < 334; c++) {
    if (Chebyshev(city[c].xy, army.xy) < 5) {         // :52242 -- radius 4
        rel = relation[me][city[c].owner];
        ... (automatic resupply FUN_0044f6d8, not mercenary-related)
        if (money > 50 && atWar && rel != 3 && lastPlus1 < 19)     // :52248
            for (i = 201; i < 251; i++)
                if (pool[i].troops >= 0 && pool[i].xy == city[c].xy && army.slot[19].troops == 0) {
                    slot = FUN_0044a66c(army);
                    army.slot[slot] = { pool[i].label, type, troops, quality, name[label] };
                    pool[i].troops = -1;                               // :52264
                }
    }
}
```

`[confirmed]`. Compared with the player:

| | Player | AI |
| --- | --- | --- |
| Distance | army ↔ offer tile, Chebyshev **== 1** | army ↔ city tile, Chebyshev **< 5** (0–4) |
| Cities reachable per order | one (first adjacent live slot) | every city in range |
| Which offers | the player picks from the list | **all** live offers on those tiles |
| Owner test | `relation[owner][player] != 3` | `relation[AI][owner] != 3` |
| Must be at war with someone | no | **yes** (`FUN_00449CD8`) |
| Money | `money ≥ (troops × price / 1000) × quality`, per offer | `money > 50`, once; **nothing is deducted** |
| 100,000-troop cap | yes | **no** |
| Supply ≥ 0.15 % of troops | yes | **no** |
| Fleet space | yes | **no** |
| 20-unit cap | yes | yes (`lastPlus1 < 19` and slot 19 empty) |
| Army map marker refresh (`FUN_0044A80C`) | yes | no |

The two relation lookups index the matrix in opposite orders. For a war (`3`), which both sides declare, this probably makes no difference. That has not been checked. `[candidate]`

Compared with mobilization's receiving-army rule (player `d == 1`, AI `d < 6`), the mercenary rule has the same shape but a smaller AI radius: **4, not 5**.

`FUN_0044E84C(army)` (`:52382–52422`) steers AI armies toward mercenaries. It finds the live offer whose city is nearest, within Chebyshev distance `< 20` and with the AI's relation toward that city's owner `< 3` (not war), and sets it as the army's move target through `FUN_0044DBA8`. `FUN_0044F31C` calls it on one branch of its target selection (`:52940`), where a later `FUN_0044DBA8` call can overwrite the target. The branch conditions were not fully interpreted. `[confirmed: the function]`, `[open: when it wins]`

### Checked against the saves

`[confirmed]`. The three save series `1_thracia_271_*`, `1_cartago_271_summer_*` and `1_rome_270_autumn_*` give 20 single-turn pairs. For each pair, the rule above predicts hires from the earlier save's computer armies, and every hire observed in the later save is matched: the offer went to `0xFFFF` and an identical unit appeared in an army.

- **10 of 10 observed AI hires predicted, and no hire went unpredicted.** They were made at distances **2, 2, 3, 3, 3, 3, 3, 3, 4, 4**. None was at distance 1, so none would have been possible under the player's rule. One of them shows up in its army at `3,682` troops rather than `3,852`, because every unit of that army lost about 4.4 % that turn.
- **One predicted hire did not happen:** Ptolemaic army 11 (`1_rome_270_autumn_1`, distance 1 from an offer at its own city Naucratis). Its only unit turns up in Ptolemaic army 5 in the next save, so the army was merged into a lower-numbered army during that AI turn and never reached its own call. `[derived]`
- **Nation 14 is a peace control.** Its army sat at distance 1 from a live offer for **10 consecutive turns** with 378–878 money and never hired. Its nation was at war with no one, so `FUN_00449CD8` kept failing. `[confirmed]`
- **Distance 5 is a boundary control.** Three otherwise-eligible AI armies at distance 5 or 6 (five offers) did not hire. `[confirmed]`
- **The other refusals held too.** Armies with 0 money did not hire, and neither did an army whose nation was at war with the city's owner (relation `3`). `[confirmed]`

Every hiring nation was flagged computer (`+0x490 == 0`) in its save.

## 4. Who writes and reads `(x, y)`

**Exhaustiveness:** a byte scan of every EXE section found **28** absolute references into `0x0049D0A4–0x0049DC67`, all in `CODE`. They fall in the 12 functions below. The Ghidra dump misses two of them, the DAT loader `FUN_004481A0` and the SAV loader `FUN_004487C4`; both were decompiled for this report. `[confirmed]`

| Function | Role | Touches `(x, y)` |
| --- | --- | --- |
| `FUN_00449130` restock (`:47806`) | the only runtime writer | **writes**: `slot.xy = template[rand(200)].xy` (`:47828`) |
| `FUN_004481A0` DAT loader | new game | writes: bulk `Read(0x0049D0A4, 0xBC4)` = 201 templates + 50 live slots |
| `FUN_004487C4` / `FUN_004484D0` | SAV load / save | round-trip the 50 live slots |
| `FUN_00449D08` | player gate | reads (adjacency) |
| `TRecruitMercs_InitializeForm` | dialog list | reads (exact tile) |
| `TRecruitMercs_ChangeUnit` / `_RecruitMercUnit` | dialog | troops/label/type/quality only; hire writes `troops = 0xFFFF` |
| `FUN_0044E41C` / `FUN_0044E84C` | AI hire / seek | read (city tile / radius 19); hire writes `troops = -1` only |
| `TInformation_ShowCityUnits` (`0x0043CC40`) | city info panel, "Mercenaries at …" | reads (exact tile of the clicked city) |
| `TAreaMap_ShowMercs` (`0x0043E470`) + `ShowMercsLI/HI/Ar/LC/HC/All` | area-map overlay, by type or all | reads (draws the marker at the offer tile) |

- **Always a city tile.** The templates are read straight from the DAT: 3,012 bytes at DAT offset **`0x1FCD6`**, after the 20-byte-stride name table at `0x1F8C6` (52 names). Every one of the **201** template `(x, y)` pairs matches one of the 334 cities' tiles, and together they cover **134 distinct cities**. `[confirmed]`
- **Which city is fixed by the template.** Each template names its city through its tile. Felsina has four templates (Gallic LI, Gallic LC, Etruscan LI, Boii LI). `[confirmed]`
- **In saves.** In five saves (`1_rome_270_winter_1`, `_winter_3`, `7`, `1_cartago_271_summer_5`, `1_thracia_271_summer_11`), every live slot (38–50 per save) sits on a city tile, and every live slot's `(x, y, Label, type)` equals a template's. `[confirmed]`
- **Empty slots keep a stale position.** Neither hire clears `(x, y)`. The DAT ships the 50 live slots all empty as `(0, 0, 0, 0, -1, 0)`, and `7.sav` still holds six empty slots at `(0, 0)`, i.e. slots never filled since the start. Every reader tests `troops >= 0` first, so a stale position is never used. `[confirmed]`
- **Template 200 is unreachable.** `rand(200)` returns `0..199`, so the last of the 201 templates (Vologesias, light cavalry) can never be drawn. None of the 5 saves holds it. `[derived]`

## 5. Byproduct: `Label` is an ethnic name, now readable

The 20-byte table at DAT `0x1F8C6` (runtime `0x0049CC94`, read by the DAT loader just before the templates) holds these names:

`0 Regular`, `1 Numidian`, `2 Greek`, `3 Celtiberian`, `4 Moor`, `5 Persian`, `6 Mysian`, `7 Cilician`, `8 Thracian`, `9 Elymaian`, `10 Galatian`, **`11 Gallic`**, `12 Cretan`, `13 Bactrian`, `14 Kappadockian`, `15 Libyan`, `16 Arab`, `17 Thessalian`, `18 Paionian`, `19 Scythian`, `20 Sarmatian`, `21 Ligurian`, `22 Balearic`, `23 Median`, `24 Tarantine`, `25 Pergamene`, `26 Gaesatai`, `27 Nubian`, `28 Asturian`, `29 Boeotian`, `30 Kardackian`, `31 Sakan`, `32 Rhodian`, `33 Gastulian`, `34 Insubre`, **`35 Egyptian`**, `36 Vascone`, `37 Etruscan`, `38 Samnite`, `39 Syracusan`, `40 Boii`, `41 Spanish`, `42 African`, `43 Aetolian`, `44 Illyrian`, `45 Cenomani`, `46 Getai`, `47 Agriane`, `48 Rhoxolani`, `49 Dahai`, `50 Kyrtii`, `51 Cossaei`.

The strings are NUL-terminated, not length-prefixed. Two independent observations check the reading: `11 = Gallic` is the Felsina hire's unit name, and `35 = Egyptian` is the Alexandria offer in [city-units-army-transfer-and-mercenaries.md](city-units-army-transfer-and-mercenaries.md). The templates use labels `1`–`51`. Label `0`, "Regular", is the army unit slot's regular marker. `[confirmed]`

## What this does not establish

- **A failed player hire at distance > 1 has not been observed.** The code is unambiguous and the one controlled hire is consistent with it, but no recording shows the silent no-op.
- **When `FUN_0044E84C`'s target survives** `FUN_0044F31C`'s later target assignments. The branch conditions (`FUN_0044E670`, `FUN_0044ECE4`, `FUN_0044EE60` outputs) were not interpreted.
- **Whether the transposed relation lookups ever differ** (player: owner→player; AI: AI→owner) in a state where one side reads `3` and the other does not.
- **Whether an AI hire can push an army past 100,000 troops.** The code permits it; no save was checked for an AI army above the cap.
- **Whether the pool is filled at new game.** The DAT ships all 50 live slots empty, and `FUN_00449130`'s only caller is the quarterly tick, so the pool may start empty until the first quarter boundary. Not checked against a turn-1 save.

## Reproduction

```text
# decompiled text (toolchain, outside the repo)
all_app_functions.txt  :43490 InitializeForm  :46858 RecruitMercenaries  :47806 restock
                       :47907 FUN_004492a0    :48572 FUN_00449d08        :52218 FUN_0044e41c
                       :52382 FUN_0044e84c    :52901 FUN_0044f31c        :53210 FUN_0044fa20
# functions missing from the dump, decompiled for this report
ExportAddresses.java  <out> 0044819c 004487c4      (DAT loader FUN_004481A0; SAV loader)
# exhaustive reference scan: every 4-byte little-endian value in [0x0049D0A4, 0x0049DC68)
#   across all EXE sections -> 28 hits, all CODE, in the 12 functions of section 4
# DAT: templates at 0x1FCD6 (251 x 12 bytes), names at 0x1F8C6 (52 x 20 bytes);
#   cities at 0x15E00 (334 x 34 bytes, tile at +0xE)
```
