# Supply drives army morale, and the naval death spiral — the turn tick's two unread branches

[decompiled-turn-and-calendar-sequencing.md](decompiled-turn-and-calendar-sequencing.md) decompiled `FUN_004514ec`, the turn tick, and recovered its calendar arithmetic, its seasonal population/supply formulas, a "readiness" value that reduces moves, and a fleet storm/loss mechanic. It stopped a few lines short of two things in the same function: the tick **writes army morale** (`ArmyRecord +14`) from each army's supply percentage, every army, every turn; and the fleet storm mechanic is an **escalating feedback loop**, not a flat per-turn risk.

Both are now confirmed against real saves, turn for turn. This report also corrects a reading in [battle-quality-promotion-and-morale-array-decompiled.md](battle-quality-promotion-and-morale-array-decompiled.md) — `+14` is not "army experience", it is the army's morale and it has a live driver — and closes the "unexplained morale swing with no recorded combat" item that [field-recruitment-uniform-attrition-and-fleet-drift.md](field-recruitment-uniform-attrition-and-fleet-drift.md) and `decompilation-plan.md` §4 have both carried as open.

All addresses are from `%LOCALAPPDATA%\ReTools\all_app_functions.txt`, with line numbers for reproducibility. Runtime array bases as established in [decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md): armies `0x0047C1EC` (stride 656), fleets `0x0049C26C` (stride 26).

## Why this was re-opened

A pass over the decompiled combat code concluded there was no supply/morale link, on two grounds: the tactical per-unit morale formula (`clamp(random(quality × 4) + armyMorale[armyIdx], …)`, adjusted `±2`/`−3` per melee exchange, array `DAT_004A0350`) has no supply term, and one save snapshot showed two armies both at morale 68 with 0 % and 65 % supply.

Both observations are correct and neither is evidence against a link. The tactical array is a **different field** that only exists mid-battle. And a single snapshot of two armies cannot separate "supply has no effect" from "two armies at the same point on different trajectories" — `+14` is a slow accumulator with a hard ceiling that most adequately-supplied armies sit at permanently.

The trigger for re-opening was a player recollection of a Thracian army that ran out of supplies and then visibly lost morale over the following turns. That is exactly what happens, and it reproduces in 13 consecutive saves.

## One save = one turn = two weeks

Stated explicitly because every rate below is per-turn. Three independent confirmations:

1. The tick ends with `week = (week + 2) % 12`, season advancing on the wrap to 1 and the BC year decrementing on the wrap to season 0 (`54663-54677`) — a season is 12 weeks = **6 turns**. The save series below is exactly 6 spring saves, 6 summer saves, then `autumn_1`, matching [decompiled-turn-and-calendar-sequencing.md](decompiled-turn-and-calendar-sequencing.md)'s calendar finding.
2. The fleet construction countdown decrements by 2 per call. Macedonia's fleet ordered at `summer_1` reads `24, 22, 20, 18, 16, 14, 12` across the seven saves to `autumn_1` — exactly one tick per save.
3. Army supply drains by a fixed per-turn amount (below) and steps exactly once per save.

## Part 1: the army rule

`FUN_004514ec` (`0x004514EC`), army loop, `54501-54529`. `puVar13` walks the army table at stride `0xA4` dwords = 656 bytes, so `puVar13 + 0xe` is `ArmyRecord +14`. Helpers, read to be sure: `FUN_00448FD0(a,b) = min`, `FUN_00448FD8(a,b) = max`, `FUN_0044A698(i)` = total troops of army `i` (sum of the 20 unit slots' `+4` words, floored at 1).

```c
troops   = FUN_0044a698(i);                                   // 0x0044A698
moves    = 10 - min(5, troops / 20000);                        // army[+6]

if (army[+8] == -1)                                            // aboard a fleet
    army[+10] = max(0, army[+10] - troops / 200);
else
    army[+10] = max(0, army[+10] - ((90 - seasonVal) * troops) / 20000);

pct = army[+10] * 10000 / troops;                              // the panel's supply %

if (pct < 10) {                                                // ---- DECAY ----
    army[+14] = max(51, army[+14] - 2);                        // 0x33
    army[+6] -= 1;
}
if (pct > 15 && army[+14] < 70)                                // 0x46  ---- REGEN ----
    army[+14] += 1;
```

| Supply % (**after** this turn's consumption) | Effect on `ArmyRecord +14` |
| --- | --- |
| `< 10` | **−2**, floored at **51**; also **−1 move** |
| `10 … 15` | **no change** — a dead band |
| `> 15` | **+1**, capped at **70** |

Three things worth keeping:

- **The percentage is computed after consumption**, so the value driving the change is the value the save then shows — which is what makes the table below predictable turn for turn.
- **51 and 70 are the field's real bounds**, and not arbitrary ones: `TInformation_ShowArmyDetails` prints morale as a tier via `moraleNames[(v − 51) >> 2]` with a `v − 48` fallback below 51 (`41052-41058`, string table `DAT_00479428`, 11-byte entries). `51 … 70` is exactly five 4-wide tiers. A fresh army from `TUnitMap_SplitArmy` starts at **59** (`48739`), mid-range — consistent with [decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md).
- **Decay and regen are asymmetric, 2:1.** Falling from the ceiling to the floor takes 10 turns of starvation; climbing back takes 19 turns of good supply.

### Seasonal consumption, and the season table located in the DAT

The season record is a 10-byte struct — 8-byte name then a `word` — at **DAT offset `0x1F7D8`**, matching the code's `&DAT_004794a0 + season*10` (name, printed in the "Week N  Season  YYY BC" line) and `&DAT_004794a8 + season*10` (value):

```
0x1F7D8:  "Spring\0\0" 0x0032(50)   "Summer\0\0" 0x0050(80)
          "Autumn\0\0" 0x0050(80)   "Winter\0\0" 0x0014(20)
```

So per-turn consumption `= ((90 − seasonVal) × troops) / 20000`:

| Season | `seasonVal` | Consumption per turn | 22,000-troop army |
| --- | --- | --- | --- |
| Spring | 50 | `troops / 500` | 44 t |
| Summer | 80 | `troops / 2000` | 11 t |
| Autumn | 80 | `troops / 2000` | 11 t |
| Winter | 20 | `troops × 7 / 2000` | 77 t |

**Winter costs 7× summer.** The same table drives the city food term in the same function as `seasonVal − 40` — Spring `+10`, Summer/Autumn `+40`, Winter `−20`, i.e. winter is a net food *loss*. An army **aboard a fleet** uses the flat `troops / 200` instead, with no seasonal term — 5× the summer rate, year-round.

### The data: Thracia, army 6, 271 BC

`1_thracia_271_*.sav`, 13 consecutive saves. Nation code 15, army index 6, at `(160, 30)` in every one. Capacity `troops / 100` = 220 t.

| Save | Supplies | Supply % | Morale `+14` | Δ | Rule | Predicted |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| `spring_1`  | 142 | 64 % | 65 | — | (initial) | — |
| `spring_3`  |  98 | 44 % | 66 | +1 | `> 15` | 66 ✓ |
| `spring_5`  |  54 | 24 % | 67 | +1 | `> 15` | 67 ✓ |
| `spring_7`  |  10 |  4 % | 65 | −2 | `< 10` | 65 ✓ |
| `spring_9`  |   0 |  0 % | 63 | −2 | `< 10` | 63 ✓ |
| `spring_11` |   0 |  0 % | 61 | −2 | `< 10` | 61 ✓ |
| `summer_1`  |   0 |  0 % | 59 | −2 | `< 10` | 59 ✓ |
| `summer_3`  |   0 |  0 % | 57 | −2 | `< 10` | 57 ✓ |
| `summer_5`  |   0 |  0 % | 55 | −2 | `< 10` | 55 ✓ |
| `summer_7`  |   0 |  0 % | 53 | −2 | `< 10` | 53 ✓ |
| `summer_9`  |   0 |  0 % | 51 | −2 | `< 10` | 51 ✓ |
| `summer_11` |   0 |  0 % | 51 |  0 | `max(51, 49)` — **floor** | 51 ✓ |
| `autumn_1`  |   0 |  0 % | 51 |  0 | `max(51, 49)` — **floor** | 51 ✓ |

**12 of 12 transitions predicted exactly, including the floor.**

The `spring_5 → spring_7` step is the one that proves the threshold is a *percentage* and not "supply reached zero": supply was still 10 t there, but 10 t against a 220 t capacity is 4 %, already under the line — morale began falling a full turn **before** the tanks ran dry.

Supply drains `142 → 98 → 54 → 10`, i.e. **−44, −44, −44** — an exact match to the spring value solved independently out of the DAT table above.

The `moves` column corroborates independently: `10 − min(5, 22000/20000) = 9`, and the saves read **9** in `spring_3`/`spring_5` and **8** from `spring_7` on, the `pct < 10` penalty. (`spring_1` reads 8, but so does every other army in that save while later saves read 9/10 — `spring_1` is a session-start state, not a post-tick one.)

### Confounds excluded

Morale can also move via the tactical `±2`/`−3` melee path and a `+3` on battle entry, so a battle in the window would invalidate the reading. There was none — this army did nothing for 13 turns:

- **Position identical** in all 13 saves: `(160, 30)`. No movement, so no attack and no siege.
- **The entire unit-slot block is byte-identical** in all 13 saves — SHA-256 prefix `d55d02c58cf6` for every one. Seven units, 22,000 troops, unchanged names, types and qualities. A battle cannot leave troop counts untouched (melee always applies losses to both sides — [decompiled-combat-formula-structure.md](decompiled-combat-formula-structure.md)) and cannot leave qualities untouched either ([battle-quality-promotion-and-morale-array-decompiled.md](battle-quality-promotion-and-morale-array-decompiled.md)).
- **The only other field that moved** is money: `100 → 46` at `summer_1`, `46 → 0` at `autumn_1` — both season boundaries, the quarterly upkeep in `FUN_00451B40` from [decompiled-quarterly-billing-and-economy.md](decompiled-quarterly-billing-and-economy.md), and the reason this army could never buy its way out at 1 talent per 5 tons.
- **`FUN_00451304`**, the only other function the tick calls between the army loop and the calendar update, is the seasonal weather system ([decompiled-weather-events.md](decompiled-weather-events.md)). It writes no army field.

### It is the only supply-driven morale path in the binary

Every indexed access to the morale word (`DAT_0047C1FA` = `0x0047C1EC + 0xE`) in the whole-application dump, nine sites:

| Line | What it is |
| --- | --- |
| `38084`, `38092` | `+= 3` to each side on battle entry, in `FUN_00437DE4` (`TBattleMap_StartBattle`'s copy-in) |
| `38135`, `38162` | seeds the tactical array `DAT_004A0350` — the known formula |
| `41054`, `41056` | the panel's tier display |
| `48739` | `= 0x3B` (59), new-army initialisation |
| `49216`, `49245` | `(troops / 0x50) × morale`, the two army-strength formulas |

Plus the two writes inside `FUN_004514ec`, which use a walking pointer rather than the indexed form and so do not appear in that grep. That is the complete set — there is no second decay rule.

## Part 2: the fleet side

### There is no fleet morale field

`FleetRecord` is 26 bytes and [decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md) labelled all of it except `+4` and `+6`. Both are ruled out as morale candidates directly from save data:

- **`+4` is written to `0xFFFF` unconditionally at the top of every fleet's turn** (`54538`). All saves agree: every launched fleet reads `−1`, and freshly-ordered fleets read `0` until their first tick flips them. A field reset every turn cannot accumulate anything.
- **`+6` reads `0`, then `77`, then `65`** for a fleet as it moves, and stays `0` for a parked one — it tracks position, not a unit stat.

**Condition (`+20`) is the structural analog of army morale**: `FUN_0044AA54` computes naval strength as `ships × condition / 10`, against the army formulas' `(troops / 80) × morale` — in both cases the size term scaled by the softer stat. The `0x46` (70) constant even recurs as the threshold below which condition starts costing moves.

### The fleet loop, in order

`54537-54632`. The ordering matters and is easy to get wrong: the **storm pass runs first, on every at-sea fleet, regardless of supply**. The supply penalty is a smaller rider applied afterwards.

```c
fleet[+14] = max(0, fleet[+14] - fleet[+18]);         // supplies -= ships, EVERY turn, every fleet

if (fleet[+10] == -1) {                               // launched and at sea
    // ---- 1. STORM PASS (54553-54592) — unconditional ----
    dmg = max(1, FUN_0040284c(100 - fleet[+20]) / 10);     // scales with damage already taken
    if (season == winter) dmg = min(5, dmg * 2);
    if (fleet[+24] == 1)  dmg = min(8, dmg * 3);
    if (FUN_004494e4(fleet[+8], &fleet[+0]) < 0) {         // away from friendly coast
        dmg = dmg * 2 + 1;                                 // always ODD on this branch
        if (season == winter && FUN_0040284c(20) == 0) dmg = 30;
    } else dmg /= 2;
    if (dmg < 6) fleet[+20] -= dmg;
    else         FUN_0044b4f8(i, 100, dmg + 100);          // heavier: costs SHIPS as well

    // ---- 2. DEATH CHECK (54593) ----
    if (fleet[+20] < 40) { news("A fleet belonging to X is lost at sea."); FUN_0044ad38(i); }
    else if (dmg > 5)    { news("A fleet belonging to X is damaged in a storm."); }

    // ---- 3. MOVES (54607-54616) ----
    fleet[+12] = 30 - (fleet[+18] - 50) / 10;
    if (fleet[+22] >= 0)
        fleet[+12] -= troops(fleet[+22]) / 100 / fleet[+18] + 1;

    // ---- 4. OUT OF SUPPLY (54618-54623) ----
    if (fleet[+14] == 0) {
        fleet[+12] -= 3;
        fleet[+20] -= FUN_0040284c(2);                     // condition -= random(0..1)
    }
    // ---- 5. DAMAGE SLOWS YOU DOWN (54624-54631) ----
    if (fleet[+20] < 70) fleet[+12] -= (70 - fleet[+20]) >> 2;
}
```

Two consequences. The **death check precedes the supply penalty**, so `−random(0..1)` can leave a fleet below 40 without killing it until the next turn's check. And `random(100 − condition) / 10` **escalates as the fleet degrades** — naval attrition is a death spiral, not the flat per-turn risk [decompiled-turn-and-calendar-sequencing.md](decompiled-turn-and-calendar-sequencing.md) recorded.

### The data: a Carthaginian fleet starved at sea until it sank

`1_cartago_271_*.sav`, 10 saves, a second run branching from the same `spring_1` state as the Thracian series, in which a fleet's supply was deliberately allowed to run out at sea. Fleet index 0, owner 1, **90 ships in every save** — so `FUN_0044B4F8` never fired and storm damage stayed under 6 throughout. Base moves `= 30 − (90 − 50)/10 = 26`.

| Save | Supply | Cond | Δ cond | Moves | Predicted |
| --- | ---: | ---: | ---: | ---: | --- |
| `spring_1`  |  80 | 85 | — | 25 | (session start, pre-tick) |
| `spring_1b` |  80 | 85 | — | 23 | (mid-turn reload, 2 moves spent) |
| `spring_5`  | **0** | 79 | −6 / 2 turns | 23 | `26 − 3` ✓ |
| `spring_7`  | **0** | 76 | −3 | 23 | `26 − 3` ✓ |
| `spring_11` | **0** | 66 | −10 / 2 turns | 22 | `26 − 3 − (70−66)>>2` ✓ |
| `summer_1`  | **0** | 62 | **−4** | 21 | `26 − 3 − (70−62)>>2` ✓ |
| `summer_3`  | **0** | 56 | **−6** | 20 | `26 − 3 − (70−56)>>2` ✓ |
| `summer_5`  | **0** | 51 | −5 | 19 | `26 − 3 − (70−51)>>2` ✓ |
| `summer_7`  | **0** | 48 | −3 | 18 | `26 − 3 − (70−48)>>2` ✓ |
| `summer_9`  | — | — | **destroyed** | — | *"lost at sea"* |

**The `−3 moves` term, isolated exactly.** Seven of seven post-tick saves match to the move. The control is the Ptolemaic fleet across the same ten saves — 70 ships, supplied, condition 100, predicted `30 − (70−50)/10 = 28` with no penalties — which reads **28 in all ten**. Same formula, same turns, one starved and one not.

**The `−random(0..1)` condition term, isolated by parity.** This looks untestable because the storm pass dominates, but the shapes separate them. Ship count never changed, so `dmg < 6` held every turn, and the magnitudes put the fleet on the `dmg × 2 + 1` branch — which is **always odd** and, bounded below 6, confined to `{3, 5}`. The supply rider adds `{0, 1}`. Every turn's total must therefore lie in `{3, 4, 5, 6}`, and **any even total proves the supply roll came up 1**. All five single-turn deltas — `−3, −4, −6, −5, −3` — fall inside that set, and **two are even**. The two-turn gaps agree (`−6 = 3+3`, `−10 = 5+5`).

**Destruction below 40, from the game's own news log.** `summer_7` leaves the fleet at condition **48**; in `summer_9` the record is simply gone (2 fleets, not 3), with the ship count never having dropped — so not naval combat, which reduces `+18`. Reading the news-log ring buffer ([decompiled-news-log-identified.md](decompiled-news-log-identified.md)) out of `1_cartago_271_summer_9.sav` gives the literal string:

```
A fleet belonging to Carthage is lost at sea.
```

exactly the message assembled at `54595-54597` immediately before `FUN_0044AD38` deletes the fleet.

**What the series does not show.** The fleet died mainly of **storms**, not starvation. Over the seven turns from condition 79 to 48, the storm term alone accounts for roughly `−28 … −35` of the `−31` observed; the supply rider contributes at most `−7`, on average about `−3.5`. Zero supply is a real aggravating factor but not the cause of death — a fleet left at sea away from friendly coast rots and sinks whether or not it is fed. The starvation penalty that actually bites is the **−3 moves**, large against a base of 26, which combined with the damage-driven move loss leaves a dying fleet progressively less able to reach a port and repair.

### "Repair" is the condition dialog, not a separate field

Checked because the displayed "repair" value could have been a distinct record field. It is not. `TRepairFleet` (`0x00440AC4`, `43341-43480`) is a dialog over `+20` and nothing else; the number the player adjusts lives at **form offset `0x206`**, a dialog-local scratch counter never written to any record:

- `InitializeForm` shows `fleet[+20]` as `"N %"`, sets `0x206 = 0`.
- `ChangeRepair` steps it `±1` / `±10`, clamped to `[0, 100 − fleet[+20]]`.
- `PrintNumbers` shows `fleet[+20] + repair` and the price `ships × repair / 5`.
- `OK` commits `fleet[+20] += repair`, `fleet[+12] = 0`, `treasury -= ships × repair / 5`.

Exactly the `ships × points / 5` already recorded. A separate AI-side auto-repair exists at `53140-53146` (if `condition < 95`, pay `(100 − condition) × ships / 5`, set condition to 100), same price formula.

## Corrections to existing reports

- [battle-quality-promotion-and-morale-array-decompiled.md](battle-quality-promotion-and-morale-array-decompiled.md) flagged `ArmyRecord +14` as a real non-padding field and called it "army experience". It is the army's **morale**, it is displayed as a tier, and it has a live per-turn driver. The two morales are distinct and must not be conflated: `+14` is strategic and persisted; `DAT_004A0350` is per-unit, tactical, and exists only mid-battle.
- [decompiled-turn-and-calendar-sequencing.md](decompiled-turn-and-calendar-sequencing.md) covered this function's supply consumption and the readiness/moves effect but not the two `+0xe` writes; its fleet storm/loss note can now be stated as the full escalating formula above.
- `decompilation-plan.md` §4's "unexplained 9→2 morale swing with no recorded combat" was the old mislabelled `+8` field (the covered map cell), already corrected in [decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md). With `+14` now having a known driver, that item can be closed.

## Still open

- **The storm-damage predicates.** `FUN_004494e4` (the test that doubles damage, inferred here as "away from friendly coast") and `fleet[+24] == 1` (which triples it) are inferred from magnitudes, not decompiled. The Cartago series is consistent with the doubling branch being active throughout but cannot prove which predicate selected it.
- **Auto-resupply.** Several armies and fleets hold a constant supply percentage for many turns against the consumption rule — e.g. an army at 80 % then 95 % for nine consecutive turns — so something resupplies units near friendly cities outside the `TAFSupply` dialog path. Not traced. It never touched the Thracian army, which is why that series is clean.
- **The 2:1 decay-to-regen asymmetry** is confirmed as code but unexplained as design.
- **`FleetRecord +6`** is ruled out as morale but not positively identified; it tracks something position-shaped.
- **An `IC2.Data` parser bug found on the way.** `SaveArmyTable.Parse`'s `owner > 15` check rejects the `0xFFFF` no-owner tombstone and aborts the entire save, making `1_thracia_271_spring_3.sav` and `1_thracia_271_autumn_1.sav` unreadable by `IC2.Inspect` (both were decoded from raw bytes for this report). It is the same sentinel [galatia-elimination-and-city-resupply-confirmed.md](galatia-elimination-and-city-resupply-confirmed.md) had to special-case for the capital field — a slot for an army merged or eliminated during the turn and not yet compacted. In `spring_3` the record duplicates an army that had just been resupplied; in `autumn_1` it is an emptied shell with zero troops in all 20 slots.
