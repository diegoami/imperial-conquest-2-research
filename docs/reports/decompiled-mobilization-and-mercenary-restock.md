# Mobilization decompiled: `FUN_0044a4e0`, what `> 15` means, and the mobilization rate's missing increment

Continues [decompiled-recruitment-cost-formula.md](decompiled-recruitment-cost-formula.md), whose next-check #2 was *"decompile `FUN_0044a4e0` to see the exact garrison-to-army transfer and the `StateCode > 15` gate's meaning."* Both are now `[confirmed]`. So is [decompilation plan item 17](../decompilation-plan.md) — *what raises a nation's mobilization percentage* — which that plan correctly predicted **shares this target**. The mercenary pool's restock rule (`FUN_00449130`) fell out of the same pass and is included.

Everything here is read from `%LOCALAPPDATA%\ReTools\all_app_functions.txt` (the whole `0x401000`–`0x460000` range, already decompiled) plus two tables read directly out of `Imperial Conquest 2.dat`. Ghidra was not re-run.

---

## 1. `FUN_0044a4e0` is `MobilizeRecruitSlot(nation, slot, out ok)`

`[confirmed]` — the whole function, in full:

```c
void FUN_0044a4e0(short param_1 /*nation*/, short param_2 /*slot*/, undefined1 *param_3 /*out ok*/)
{
  *param_3 = 1;
  local_8 = *(short *)(&DAT_0047495a + param_2 * 8 + param_1 * 0x494);   // slot.city
  local_a = param_2;                                                     // slot
  local_6 = param_1;                                                     // nation
  FUN_0044a120(&local_c, &local_e, param_3, (int)&stack0xfffffffc);      // -> army, unitSlot
  if (local_c == -1) {                                                   // no army will take it
    FUN_00449f08(local_6, cityXY(local_8), &local_c);                    // create one
    local_e = 0;
  }
  if (local_c == -1) { *param_3 = 0; }                                   // and that failed too
  else {
    puVar1 = &DAT_0047c1fc + local_c * 0x148 + local_e * 0x10;           // army[a].unit[s]
    *puVar1   = 0;                                                       // +0  origin label = native
    puVar1[2] = (&DAT_00474958)[local_6 * 0x24a + local_a * 4];          // +4  troops  <- slot.troops
    puVar1[1] = (&DAT_00474956)[local_6 * 0x24a + local_a * 4];          // +2  type    <- slot.type
    iVar2 = (int)(short)(&DAT_00474954)[local_6 * 0x24a + local_a * 4];  //     slot.state
    if (iVar2 < 0) { iVar2 = iVar2 + 3; }
    puVar1[3] = (short)(iVar2 >> 2);                                     // +6  quality = state / 4
    FUN_0044a218(local_c, local_e);                                      // name the unit
    FUN_0044a610(local_6, local_a);                                      // delete the slot
    FUN_0044a80c(local_c);                                               // refresh the map marker
  }
}
```

**Parameters, named from use** `[confirmed]`: `param_1` is the **nation index** (the acting nation — see §4), `param_2` is the **index into that nation's 40-slot recruitment table**, `param_3` is an **out-parameter success flag**, set to `1` on entry and cleared only when no army could be found *and* none could be created.

**The three fields it copies are exactly the three the recruitment slot holds** `[confirmed]`. The slot is 8 bytes at `nation + 0x2E4 + slot × 8` (base `0x00474954`, 40 slots, nation stride `0x494`): `[0]` state, `[1]` unit type, `[2]` troops, `[3]` city index. The unit slot it writes is the 32-byte army unit slot already documented in [army-records-and-roman-roster.md](army-records-and-roman-roster.md): `+0` origin label, `+2` type, `+4` troops, `+6` quality, `+8` 24-byte name.

**Order matters, and it is this** `[confirmed]`: read the slot, write the unit, name it, *then* delete the slot, then refresh the marker. Nothing is written back to the city.

> **This is not a garrison transfer.** `[derived]` — from the fact that the source is the 40-slot recruitment table (`nation + 0x2E4`) and nothing in the function touches a city record. The "city units" the recruit dialog lists **are** the recruitment slots; mobilizing removes one from that list and creates an army unit. `decompiled-recruitment-cost-formula.md` and [city-units-army-transfer-and-mercenaries.md](city-units-army-transfer-and-mercenaries.md) both call this a "garrison to army transfer"; the mechanic is right, the word "garrison" is not — there is no separate garrison pool being drawn down.

### `FUN_0044a610` — the slot deletion is a compacting shift

`[confirmed]`:

```c
void FUN_0044a610(short nation, short slot)          // delete recruitment slot
{
  if (slot < 0x27)
    do {   // slot[i] = slot[i+1], 8 bytes at a time
      *(undefined4 *)(base + nation*0x494 + 0x2e4) = *(undefined4 *)(base + nation*0x494 + 0x2ec);
      *(undefined4 *)(base + nation*0x494 + 0x2e8) = *(undefined4 *)(base + nation*0x494 + 0x2f0);
      slot++; base += 8;
    } while (slot != 0x27);
  *(undefined2 *)(&DAT_00474a90 + nation * 0x494) = 0;   // slot[39].troops = 0
}
```

The 40 slots are a **compacted list, not a sparse array** `[confirmed]`: deleting slot *k* shifts every later slot down one and zeroes slot 39's troop count. `TArmyRecruits_RecruitUnit` matches — it takes the **first** slot whose troops are `0`, and refuses outright when slot 39 is occupied, with the literal *"You have reached your limit of 40 units."* `[confirmed]`

---

## 2. The `> 15` gate: a threshold with a precise, readable meaning

The gate in `TArmyRecruits_MobilizeUnits` `[confirmed]`:

```c
if (0xf < (short)(&DAT_00474954)[DAT_004a0320 * 0x24a + iVar5 * 4])   // slot.state > 15
    FUN_0044a4e0(DAT_004a0320, sVar1, (undefined1 *)&uStack_14);
```

**It is not an artefact.** `[confirmed]` Three facts, together, explain it completely:

1. `FUN_0044a4e0` sets the new unit's **quality** to `state / 4` (truncating toward zero).
2. `TArmyRecruits_SetCityRecruits` renders each pending slot's status column with **the identical expression**:
   ```c
   iVar3 = (int)*psVar1;  if (iVar3 < 0) iVar3 += 3;
   FUN_00405bc8(acStack_4a, &DAT_0047938c + (iVar3 >> 2) * 0xb);   // qualityNames[state / 4]
   ```
3. `DAT_0047938c` is BSS — it is loaded from the DAT file. Read directly out of `Imperial Conquest 2.dat` at **`0x1F6CA`**, 11-byte stride:

   | index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
   | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
   | name | `not ready` | `not ready` | `not ready` | `not ready` | `very poor` | `poor` | `average` | `good` | `very good` | `elite` |

So **`state > 15` is exactly `quality >= 4`, which is exactly "the slot no longer reads *not ready*"** `[confirmed]`. States `0`–`15` all map to quality `0`–`3`, all four of which print the same string.

**A lower state code exists and is what the gate excludes.** `[confirmed]` — `TArmyRecruits_RecruitUnit` and the AI's `FUN_004501f4` both write `*puVar1 = 0` when creating an order. A recruitment slot **starts at state `0`**, not `24`. The `24` this project has always observed in saves is the *cap*, already `[confirmed]` in [decompiled-turn-and-calendar-sequencing.md](decompiled-turn-and-calendar-sequencing.md): the weekly tick `FUN_004514ec` runs

```c
sVar14 = 0x10;  local_160 = &DAT_00474954;        // 16 nations
do { sVar11 = 0x28; psVar10 = local_160;          // 40 slots each
     do { if (-1 < *psVar10) *psVar10 = min(0x18, *psVar10 + 2);
          psVar10 += 4; } while (--sVar11);
     local_160 += 0x24a; } while (--sVar14);
```

**The readiness ladder, end to end** `[derived]` — from the `+2`/week cap-24 tick composed with `quality = state / 4` and the name table above:

| weeks since order | state | quality | shown as | mobilizable? |
| ---: | ---: | ---: | --- | --- |
| 0–7 | 0–14 | 0–3 | `not ready` | no |
| 8–9 | 16–18 | 4 | `very poor` | **yes** (player) |
| 10–11 | 20–22 | 5 | `poor` | yes (player) |
| 12+ | 24 | 6 | `average` | yes (player and AI) |

A unit mobilized early is permanently worse. That is the design the threshold encodes, and it is a genuinely new mechanic for this project: nothing in the reports had connected the recruit list's status column to the unit's quality stat.

---

## 3. What the transfer does to the receiving army — and the 20-unit cap

### `FUN_0044a120` — pick the receiving army

`[confirmed]`:

```c
void FUN_0044a120(short *armyOut, short *slotOut, undefined4 unused, int frame)
{
  *armyOut = -1;
  for (a = 0; a < DAT_004a0324 /*army count*/; a++)
    if (army[a].owner == nation) {
      d = FUN_00449018(army[a].xy, cityTable[city].xy);
      if (d == 1 || (((&DAT_00474b00)[nation * 0x494] == '\0') && d < 6))
          *armyOut = a;                       // no break: the LAST match wins
    }
  if (-1 < *armyOut) {
    *slotOut = FUN_0044a66c(*armyOut);        // first free unit slot
    if (*slotOut != 0x14 &&
        FUN_0044a698(*armyOut) + slot.troops < 0x186a1) return;     // accepted
    *armyOut = -1;                            // army full -> caller creates a new one
  }
}
```

- **`FUN_00449018` is Chebyshev distance** `[confirmed]` — `max(|x1-x2|, |y1-y2|)`, via two `abs` idioms feeding `FUN_00448fd8` (`max`). This **closes the open question in [attack-and-siege-are-adjacency-orders.md](attack-and-siege-are-adjacency-orders.md)**: the game's grid metric is Chebyshev, 8-way, not Manhattan. The reimplementation's `LandingTile.ChebyshevDistance` choice is faithful, and that report's `[derived]` caveat can be retired.
- **`d == 1`, not `d <= 1`** `[confirmed]`. The receiving army must be *adjacent* to the city. This is consistent with — and independent corroboration of — that same report's observation that an army never occupies a city tile.
- **The AI gets a radius of 5, the player a radius of 1** `[confirmed]`. `(&DAT_00474b00)[nation × 0x494] == 0` is *computer-controlled* (polarity fixed in [army-moves-field-signed-and-the-ffff-underflow.md](army-moves-field-signed-and-the-ffff-underflow.md)). A real, asymmetric AI advantage.
- **`FUN_0044a66c` returns `lastOccupiedSlot + 1`, not the first hole** `[confirmed]` — it scans all 20 slots and remembers the highest index with `troops > 0`. Gaps are never reused. Returning `20` is the rejection.
- **The 20-unit cap is enforced here** `[confirmed]`, and **an army may not exceed 100,000 troops** `[confirmed]` — `total + incoming < 0x186A1`, the same constant behind the mercenary dialog's literal *"An army can not contain more than 100,000 troops."*

### `FUN_00449f08` — create a new army when none will take it

`[confirmed]`:

```c
void FUN_00449f08(short nation, undefined4 cityXY, short *armyOut)
{
  *armyOut = -1;  local_12 = cityXY;
  FUN_004492c0((short *)&local_12, 1);                 // find a free land cell next to the city
  if (-1 < (short)local_12 && DAT_004a0324 < 0xc6) {   // hard cap: 198 armies
    *armyOut = DAT_004a0324++;
    army.x = local_12.x;  army.y = local_12.y;
    army.owner   = nation;                                           // +4
    army.moves   = 0;  if (nationIsComputer) army.moves = 1;         // +6
    army.covered = map[x][y];                                        // +8  the cell the marker hides
    army.supplies = 0;                                               // +0xA
    army.money    = 0;                                               // +0xC
    army.morale   = 0x3b;                                            // +0xE  = 59
    for (i = 0; i < 20; i++) { unit[i].troops = 0; unit[i].type = 0; }
    map[x][y] = nation + 200;                                        // army marker
  }
}
```

`FUN_004492c0(xy, 1)` scans the 3×3 neighbourhood (`dx, dy` in `{-1, 0, 1}`, clamped to the 320×140 map) for a cell whose map code is in **`[2, 11]`**, taking the last match `[confirmed]`. That range is the land terrain codes `[derived]` — from [rivers-and-map-markers.md](rivers-and-map-markers.md), an occupied city cell reads `20 + owner + 16 × variant >= 20`, so the city's own centre cell can never satisfy it, and a new army is always placed on an adjacent land tile. That is the mechanism behind "an army never occupies a city tile".

**A newly created army starts with 0 supplies, 0 money and morale 59** `[confirmed]`, and with **0 moves for a human nation, 1 for an AI nation** `[confirmed]` — so a player's freshly mobilized army cannot act in the week it appears. **The engine holds at most 198 armies** `[confirmed]`.

### The answer to "new unit or moved unit"

**The transfer creates a new army unit; `ArmyState.Units` grows by one.** `[confirmed]` Either an adjacent army gains a unit in slot `lastOccupied + 1`, or a brand-new one-unit army is created next to the city. The recruitment slot is deleted, so the nation's *pending* list shrinks by one. No existing army unit is moved or merged.

### `FUN_0044a218` — the unit's name

`[confirmed]`: it picks the lowest ordinal `N` in `1..99` not already borne by a unit of **the same type**, with `troops > 0` and **origin label `0`**, in any army of the same owner, then formats `"<N>st|nd|rd|th <TypeName> Battalion"` with `TypeName` in `{Foot, Guards, Bowmen, Lancers, Dragoons}` for types 0–4, and the usual 11/12/13 → "th" exception. Matches the Roman roster in [army-records-and-roman-roster.md](army-records-and-roman-roster.md) exactly. If all of 1..98 are taken it sticks at 99.

> **Correction to [army-records-and-roman-roster.md](army-records-and-roman-roster.md) (2026-09-19).** That report records *"an unknown word at `+0`"* in each unit slot. **`+0` is the unit's origin label**: `0` for a nationally recruited unit (written by `FUN_0044a4e0`), and the mercenary offer's `Label` for a hired unit — `TRecruitMercs_RecruitMercUnit` writes `*psVar1 = label` and then names the unit from `&DAT_0049CC94 + label × 0x14` ("Gallic"), instead of numbering it. `FUN_0044a218`'s ordinal scan skips every unit whose `+0` is non-zero, which is exactly why mercenaries never take a battalion number. `[confirmed]` [Decompilation plan item 11](../decompilation-plan.md)'s class sweep had already recorded that *"the pool record's `Label` is a name-table index that doubles as the army unit slot's regular/mercenary marker"*; what is new here is the **address of that name table, `0x0049CC94`, on a 20-byte stride**, and the fact that `army-records-and-roman-roster.md` was never updated to match.

### `FUN_0044a80c` — the army's map marker is a size band

`[confirmed]`:

```c
total = FUN_0044a698(army);                    // sum of unit troops
band  = total / 1000;
marker = owner + (band < 25 ? 200 : band < 50 ? 216 : 232);
if (-1 < army.covered) map[army.x][army.y] = marker;      // not aboard a fleet
```

Three army marker bands at **25,000 and 50,000 troops** `[confirmed]`.

---

## 4. The two call sites: both are mobilization, and `DAT_004a0320` is the acting nation

`[confirmed]`. `DAT_004a0320` is the **index of the nation whose turn is being processed**, assigned in the turn loop as `DAT_004a0320 = *(short *)(&DAT_0049efe8 + DAT_004a0322 * 2)` — the same global every other report reads as "current nation". It is not a player index; the AI path passes it for itself.

**Call site B (line 56077) — `TArmyRecruits_MobilizeUnits`, the player's dialog** `[confirmed]`. It walks the listbox selection backwards, maps each selected row to a slot through the form's `+0x4DE` row-to-slot table, applies the `> 15` gate, and calls `FUN_0044a4e0`. If any call cleared the flag it shows *"You cannot mobilise a unit at this time."*

**Call site A (line 53794) — `FUN_004504f4`, the AI's recruit-and-mobilize routine** `[confirmed]`. Called once per AI turn from `FUN_0044ffbc` as `FUN_004504f4(threat - ownStrength)`, i.e. with a **strength deficit as a budget**. Its policy:

```c
// pass 1: may we mobilize at all?
ready = 0; haveNearbyArmy = 0;
for (s = 0; s < 40; s++)
  if (slot[s].troops > 0 && slot[s].state == 0x18) {          // note: == 24, not > 15
    ready++;
    for each army a of this nation
      if (Chebyshev(army[a].xy, cityXY(slot[s].city)) < 6) haveNearbyArmy = 1;
  }
mayMobilize = haveNearbyArmy || ready >= 4;

// pass 2: mobilize until the budget is met
spent = 0;
for (s = 0; s < 40; s++)
  if (slot[s].troops > 0) {
    value = (slot[s].troops / 100) * DAT_00478fd6[slot[s].type * 0x28];
    if (slot[s].state == 0x18 && spent < budget && mayMobilize) {
      FUN_0044a4e0(nation, s, &ok);
      if (ok) spent += value;
    }
  }

// pass 3: place up to 8 new recruit orders (see section 5)
```

**The AI only ever mobilizes a fully ready slot (`state == 24`)** `[confirmed]`, where the player may mobilize from `16`. And it will mobilize with no army nearby only once four or more slots are ready `[confirmed]` — which is the case that creates new armies.

> **`DAT_00478fd6` is identified.** `[confirmed]` It is the unit-type table column [unit-type-stat-table-in-dat.md](unit-type-stat-table-in-dat.md) lists as *unidentified* at DAT `+0x26` (light inf 20, heavy inf 100, archers 40, light cav 60, heavy cav 120). It is the **AI's per-type combat value**: strength is `(troops / 100) × value[type]`, summed over units and over recruitment slots, and it is what the AI compares against perceived threat to decide how much to build. The in-memory table base is `0x00478FC0` (the type name), and the DAT offsets in that report run `0x10` higher than the in-memory ones — `+0x1A` size ↔ `DAT_00478FCA`, `+0x22` initial cost ↔ `DAT_00478FD2`, `+0x24` quarterly ↔ `DAT_00478FD4`, `+0x26` value ↔ `DAT_00478FD6`.

---

## 5. Plan item 17 is answered: what raises the mobilization percentage

**Mobilizing does not change it. Placing a recruitment order does.** `[confirmed]`

`TArmyRecruits_RecruitUnit`, on the nation record (`local_c = &DAT_00474670 + nation × 0x494`):

```c
*(int *)(local_c + 0x438) -= (troops / 200) * initialPrice[type];           // treasury
iVar4 = (*(short *)(param_1 + 0x240) * 1000) / *(int *)(local_c + 0x430);   // troops*1000 / wealth
sVar8 = (short)iVar4 + *(short *)(local_c + 0x442) + 1;
*(short *)(local_c + 0x442) = sVar8;
*(short *)(local_c + 0x442) = FUN_00448fd0(100, sVar8);                     // min(100, ...)
```

and `TArmyRecruits_DisbandUnits`, exactly symmetric, with `FUN_00448fd8` (`max`) against `0`:

```c
mobilized = max(0, mobilized - 1 - (slot.troops * 1000) / wealth);
```

So `[confirmed]`:

```text
order placed   : mobilized (+0x442) = min(100, mobilized + 1 + (troops × 1000) / wealth (+0x430))
order cancelled: mobilized (+0x442) = max(0,   mobilized - 1 - (troops × 1000) / wealth)
quarterly      : mobilized          = max(0,   mobilized - 3)      // FUN_00451b40, already confirmed
```

The AI's `FUN_004504f4` applies the **identical** increment inline when it places an order, and gates new orders on `mobilized < 100` `[confirmed]` — the same cap the player's dialog reports as *"Your mobilisation rate is already 100%."*

**`+0x430` is `wealth`, already `[confirmed]`** in [nation-tax-base-and-city-economy-fields.md](nation-tax-base-and-city-economy-fields.md) as the sum over the nation's cities of `population × 3000`, rebuilt quarterly. So the increment is `1 + troops / (3 × totalPopulation)` in the game's own units `[derived]` — direct substitution. **A nation's mobilization rate is its standing army expressed as a fraction of its people, accumulated one order at a time.** That is why it feeds back into population growth and city supply production the way [city-population-growth.md](city-population-growth.md) found: mobilizing a country starves it.

**Magnitude check** `[derived]`, from that report's own figures: Rome at wealth `768,000` ordering a 15,000-troop light-infantry unit gains `1 + 15,000,000/768,000 = 1 + 19 = 20` points at once, against a `-3` quarterly decay. The observed spread in the saves — Rome at 30, Gaul/Celtiberia/Galatia at 97–100, four nations at 0 — is exactly what this rule produces, and the initial value is `50` (`(&DAT_00474ab2)[nation × 0x24a] = 0x32` at nation setup) `[confirmed]`.

> **Plan item 17's alternative outcome is ruled out.** It allowed for *"a demonstration that nothing in `CODE` writes the field upward"*. Three sites write it upward: `TArmyRecruits_RecruitUnit` (`0x00454E78`), `FUN_004504f4` (`0x004504F4`), and nation setup's `= 50`.

---

## 6. The mercenary pool does restock — `FUN_00449130`, quarterly

`[confirmed]`. Called from exactly one place, inside `FUN_004514ec`'s week-wrap branch, immediately after the quarterly economy:

```c
DAT_004a0330 = (week + 2) % 0xc;
if (DAT_004a0330 == 1) {
    FUN_00451b40((week + 2) / 0xc, ...);   // the quarterly tick
    FUN_00449130();                        // <- mercenary restock
    ...
}
```

so **once per season**, on the same boundary as tax collection and upkeep `[confirmed]`.

```c
void FUN_00449130(void)
{
  psVar4 = &DAT_0049da18;                      // live pool: 50 slots x 12 bytes, base 0x0049DA10
  for (i = 0; i < 0x32; i++, psVar4 += 6) {
    if (*psVar4 == -1) {                       // slot empty (troops == 0xFFFF)
        if (rand(6) > 4) goto occupied_roll;   // 1 in 6: fall through to the replace roll
        goto refill;                           // 5 in 6: refill
    } else {
     occupied_roll:
        if (rand(9) > 7) goto refill;          // 1 in 9: replace a live offer
        continue;
    }
  refill:
    n = rand(200);                             // template table at 0x0049D0A4, 12 bytes each
    slot.x, slot.y        = tmpl[n].x, tmpl[n].y;
    slot.label, slot.type = tmpl[n].label, tmpl[n].type;
    base = (tmpl[n].troops * 3) / 2;                                // truncating toward zero
    slot.troops  = rand(base) + base;                               // uniform in [base, 2*base - 1]
    slot.troops  = min(slot.troops, standardSize[tmpl[n].type]);    // DAT_00478FCA
    slot.quality = min(9, max(5, tmpl[n].quality + 1 - rand(2)));
  }
}
```

`FUN_0040284c(n)` is Delphi's `Random(n)` — an LCG scaled by `(n × state) >> 32`, so `0 <= result < n` `[confirmed]`; independently corroborated by `FUN_004501f4`'s five type buckets over `rand(100)` partitioning `0..99` exactly.

Consequences `[confirmed]` unless noted:

- **An empty slot refills with probability `5/6 + (1/6)(1/9) = 46/54`, about 85%, each quarter; a live offer is replaced with probability `1/9`.** `[derived]` — composing the two rolls through the fallthrough.
- **Mercenary quality is always `5`–`9`** (`poor` through `elite`), never lower. Matches the `quality 0 or 5–9` plausibility range [mercenary-pool-record.md](mercenary-pool-record.md) arrived at empirically, and the observed `8` on the confirmed Felsina hire.
- **Offer size is `1.5x` to `3x` the template's value, capped at the type's standard battalion size** (`DAT_00478FCA`: light inf 15,000, heavy inf 6,000, archers 3,500, light cav 7,000, heavy cav 2,500) — the same column `TArmyRecruits_NewUnitType` divides by 5 for the dialog default.
- **The `0xFFFF` empty sentinel is the code's own test**, not just a save-file convention: `if (*psVar4 == -1)`.
- **A mercenary offer's coordinates, label and type are drawn wholesale from a fixed 201-record template table at `0x0049D0A4`**; only troops and quality are randomized. That is why the same `(x, y)` and `label` recur across saves.

> **Answers an open item in [mercenary-pool-record.md](mercenary-pool-record.md) (2026-09-19).** That report listed *"whether/how often the 49-of-50 non-empty offers reshuffle turn-to-turn on their own (ordinary market turnover wasn't ruled out)"* as unsettled. Turnover is real, it is **quarterly, not per-turn**, and it is `1/9` per live slot per quarter.

---

## 7. Verified end to end against the one controlled mobilization in the corpus

[mobilization-movement-and-city-capture-modes.md](mobilization-movement-and-city-capture-modes.md) recorded a single-click mobilization of Rome's whole ready garrison across `1_rome_270_autumn_1.sav` → `1_rome_270_autumn_3.sav`. Re-parsing both army tables byte for byte checks **every** clause above. Rome is city `(101, 43)`.

```text
autumn_1  army 0 @ (100,42)  13 units  48,173 troops  moves 8  covered 9  supply 410  money 296  morale 70
autumn_3  army 0 @ (100,42)  20 units  83,173 troops  moves 6  covered 9  supply 791  money 296  morale 70
              + slot 13..17  5 x archers 3,500   quality 6   "1st".."5th Bowmen Battalion"
              + slot 18      light inf 15,000    quality 6   "3rd Foot Battalion"
              + slot 19      heavy cav 2,500     quality 6   "3rd Dragoons Battalion"
autumn_3  army 14 @ (102,44)  4 units  43,000 troops  moves 8  covered 2  supply 410  money 0  morale 60
              slot 0  light cav  7,000  quality 6  "3rd Lancers Battalion"
              slot 1  heavy inf  6,000  quality 6  "9th Guards Battalion"
              slot 2  light inf 15,000  quality 6  "4th Foot Battalion"
              slot 3  light inf 15,000  quality 6  "5th Foot Battalion"
```

Eleven ready slots (state `24`) were mobilized; a twelfth, a light cavalry unit at state `8`, stayed behind and read `10` the next turn. Point by point:

| Claim | Prediction | Save |
| --- | --- | --- |
| `quality = state / 4` | all 11 units quality `6` | **all 11 are `6`** `[confirmed]` |
| the `> 15` gate | the state-`8` slot is not mobilized | **it stayed, and ticked to `10`** `[confirmed]` |
| origin label `+0` is `0` for national units | `0` on all 24 units | **`0` on all 24** `[confirmed]` |
| an *adjacent* army receives (`d == 1`) | army 0 at `(100,42)` is `d = 1` from Rome | **yes** `[confirmed]` |
| 20-unit cap forces the split | army 0 fills `13 → 20`, then overflow | **exactly 20, then a new army** `[confirmed]` |
| new army placed on the **last** cell of the 3×3 scan | `(101+1, 43+1) = (102, 44)` | **`(102, 44)`** `[confirmed]` |
| the placement cell's terrain is in `[2, 11]` | covered code in range | **covered = `2`** `[confirmed]` |
| "last army index wins" in `FUN_0044a120` | once army 14 exists, the rest go to it | **all 4 remainder units are in army 14** `[confirmed]` |
| new army money `= 0` | `0` | **`0`** `[confirmed]` |
| new army morale `= 59` | `59`, `+1` by the elapsed weekly tick at >15 % supply | **`60`** `[confirmed]` |
| new army moves `= 0` | `0`, then recomputed weekly to `10 − ⌊43,000/20,000⌋ = 8` | **`8`** `[confirmed]` |
| the naming scan is **nation-wide**, not per-army | army 0 already held 1st/2nd Foot, 1st–8th Guards, 1st/2nd Dragoons, 2nd Lancers | **the new units continue those series across both armies: 3rd Foot in army 0, then 4th and 5th Foot in army 14; 9th Guards; 3rd Dragoons; 3rd Lancers** `[confirmed]` |
| mobilizing does not touch the mobilization rate | unchanged | **Rome stayed at 62 %** `[confirmed]`, as that report already noted |

The troop split is the unique 7-unit subset summing to `35,000` (`15,000 + 2,500 + 5 × 3,500`), and the order the units appear in confirms the **backwards** iteration of `TArmyRecruits_MobilizeUnits` — which is not a stylistic choice: the form's row-to-slot table is built once, before any deletion, and `FUN_0044a610` shifts only slots *above* the one it deletes, so descending order is the only order under which the stale table stays correct `[derived]`.

> **Correction to [mobilization-movement-and-city-capture-modes.md](mobilization-movement-and-city-capture-modes.md) (2026-09-19).** That report gives a freshly created army the fingerprint *"410 tons supply, 0 money, 8 moves, morale 2"* and [roadmap.md](../roadmap.md) still asks for a same-day pair to test it. **Only `0 money` is a creation value.** `FUN_00449f08` creates an army with **0 supplies, 0 money, 0 moves (1 for an AI nation) and morale 59**. The observed `8 moves` is the weekly tick's recomputation `10 − min(5, ⌊troops/20000⌋)`; the `410 tons` is a resupply the report itself suspected (*"multi-turn pairs conflate transfer, movement consumption, and city production"* — it was right); and the `morale 2` is not morale at all but the `+8` **covered map cell**, already corrected in [army-records-and-roman-roster.md](army-records-and-roman-roster.md) — the real morale word reads `60`, which is the created `59` plus the tick's `+1`. The same-day pair is still worth taking, but it now has a specific prediction to test rather than an unexplained fingerprint.

### Reproduction of this check

```python
import struct, os
d = open(os.path.join(base, '1_rome_270_autumn_3.sav'), 'rb').read()
off = 0x18A5C                                  # end of the 334-city table
n   = struct.unpack_from('<H', d, off)[0]      # army count
for i in range(n):                             # 656-byte records
    r = d[off + 2 + i*656 : off + 2 + (i+1)*656]
    x, y, owner, moves, covered, supply, money, morale = struct.unpack_from('<8h', r, 0)
    for s in range(20):                        # 32-byte unit slots at +16
        label, typ, troops, quality = struct.unpack_from('<4h', r, 16 + s*32)
        name = r[16 + s*32 + 8 : 16 + s*32 + 32].split(b'\0')[0]
```

---

## 8. What this does not settle

- **Whether `state` is ever negative.** The weekly readiness tick guards with `if (-1 < *psVar10)`, but no write in the whole dump sets a recruitment slot's state below `0`. The guard may be dead, or may cover a DAT/SAV-loaded value this project has never seen. Not resolved.
- **Nation setup clears only `slot.troops`**, not `slot.state` — the setup routine zeroes `(&DAT_00474958)[...]` for all 40 slots and nothing else. A recycled slot therefore carries a stale state until `RecruitUnit` overwrites it with `0`. Harmless as far as the read goes, but not verified against a save.
- **A possible original-game overflow in the mercenary hire.** `TRecruitMercs_RecruitMercUnit` calls `FUN_0044a66c` and writes to the returned slot **without checking for `20`** — unlike `FUN_0044a120`, which does. Writing slot 20 lands on `army + 0x290`, the next army record's header. The dialog closes itself when slot `0x13` is filled, which probably makes it unreachable in practice, but "probably" is the honest word: not tested, not observed, and not something to reproduce in the reimplementation.
- **What `Label` means** — section 3 identifies the table it indexes (`0x0049CC94`, 20-byte strings) but the table is BSS, loaded from the DAT, and its DAT offset was not located this pass. The strings are readable the same way `0x1F6CA` was.
- **The `d == 1` / `d < 6` asymmetry has not been checked against play.** It is unambiguous in the code, but it predicts something a player could notice — that a mobilized unit joins an adjacent army rather than a nearby one — and no recording covers it.
- **`FUN_004492c0`'s "last match wins" placement** means a new army appears at the city's south-east neighbour whenever that cell is land. Unverified against a save pair.

---

## 9. Reproduction

```bash
# The target and its helpers, from the existing whole-application dump
awk '/^\/\/ ==== FUN_0044a4e0 @/{p=1} p{print} p&&/^\/\/ ==== /&&!/FUN_0044a4e0/{exit}' \
  "$LOCALAPPDATA/ReTools/all_app_functions.txt"
# helpers: FUN_0044a120 FUN_00449f08 FUN_0044a218 FUN_0044a610 FUN_0044a66c
#          FUN_0044a698 FUN_0044a80c FUN_004492c0 FUN_00449018 FUN_00448fd0/fd8 FUN_0040284c
# call sites: TArmyRecruits_MobilizeUnits (0x004552A8), FUN_004504f4 (0x004504F4)
# rate:       TArmyRecruits_RecruitUnit (0x00454E78), TArmyRecruits_DisbandUnits (0x004553B0)
# restock:    FUN_00449130 (0x00449130), called from FUN_004514ec
```

The quality-name table, read straight out of the DAT (the in-memory `DAT_0047938C` is BSS and empty in the EXE):

```python
d = open(r'Imperial Conquest 2.dat', 'rb').read()
start = d.find(b'not ready')          # 0x1F6CA
[d[start + i*11 : start + i*11 + 11] for i in range(10)]
```

---

## 10. Next checks

1. **`FUN_0044b230`** — [plan item 18](../decompilation-plan.md), the forced-capture erosion factor. Still the largest fully-specified open formula, and the plan already states exactly what the answer has to look like.
2. **The `Label` name table's DAT offset**, by the `0x1F6CA` method — search the DAT for a nation or ethnicity name like `Gallic` on a 20-byte stride. Cheap, and it finishes [mercenary-pool-record.md](mercenary-pool-record.md).
3. **`TUnitMap_JoinFleets` at `0x00447A48`** — [plan item 15](../decompilation-plan.md), one comparison instruction, `<` against `<=`.
4. **A save pair across a mobilization order** would confirm section 5's increment arithmetically the way the tax and capture formulas were confirmed: record `wealth`, `mobilized` and the troop count before and after placing one recruitment order.
