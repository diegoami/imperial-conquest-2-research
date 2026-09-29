# Which cities may recruit, and the recruit dialog's troop amounts

**Question** ([imperial_conquest_2#515](https://github.com/diegoami/imperial_conquest_2/issues/515)): which cities may train regiments in the original? The player recalls that a non-capital town needs a high fortification level to recruit. The build repository applies no such rule. The follow-up asks for the dialog's troop-amount rule per unit type (maximum, minimum, step, default), and whether it equals the DAT's standard battalion sizes.

**Answer.**
- **A town may recruit if it is the nation's capital, or if its fortification is at least 75%.** The recruit dialog also keeps listing a town that already has units in training, but a new recruitment there is refused once its fortification is below 75%.
- The AI's own recruitment obeys the same threshold.
- **Amounts:**
  - the dialog allows from **one fifth of the standard battalion up to the full battalion**, in steps of 100 and 1,000;
  - choosing a unit type sets the amount to one fifth;
  - the maxima equal the DAT battalion sizes exactly.

Found by decompiling the recruit dialog (`TArmyRecruits`), and checked against every town holding units in six saves: 118 checks, 0 exceptions. The dialog was **not** driven live headless in this pass.

## Method

- **Handlers:** the `TArmyRecruits` handlers were located from the executable's published-method table:
  - `InitializeForm` `0x45489C`;
  - `SetCityRecruits` `0x45495C`;
  - `ChangeCity` `0x454BDC`;
  - `NewUnitType` `0x454D5C`;
  - `ChangeUnitSize` `0x454DE0`;
  - `RecruitUnit` `0x454E78`.

  These handlers are reached only through the method table, so Ghidra's auto-analysis had not created functions for them. They were created and decompiled at those addresses with Ghidra 12.1.3 headless.
- **Two more routines:** the town-list builder `FUN_004544E0`, called from `InitializeForm`, and the AI's recruitment `FUN_004504F4`, with its helpers `FUN_004502E0` (which town) and `FUN_004501F4` (which unit).
- **Clamp helpers:** `FUN_00448FD0` = `min(a, b)`, `FUN_00448FD8` = `max(a, b)`, read from their four instructions each.
- **Fields:**
  - city record `+0x1A` is **fortification**. Values ≤ 100 are the current percentage; values above 100 encode a fortify order in progress as `points × 100 + current` ([city-population-growth.md](city-population-growth.md), [decompiled-city-capture-resolution.md](decompiled-city-capture-resolution.md));
  - nation `+0x444` is the **capital**;
  - nation `+0x442` is **mobilisation**, capped at 100;
  - nation `+0x2E4` is the 40-slot recruitment table;
  - unit-type table (DAT `0x1F2F0`, stride `0x28`): `+0x1A` is the standard battalion, `+0x22` is the cost per 200 troops.
- **Saves checked:**
  - `1_rome_270_winter_3.sav`, `1_rome_270_winter_5.sav`, `1_rome_270_winter_11.sav` (`run-1-rome`);
  - `ng1_rome.sav`, `ng2_rome.sav`, `ng3_carthage.sav` (fixtures repo `saves/new-game-probes/`).

## Observations

### 1. The dialog's list of towns (`FUN_004544E0`)

For each town in the current nation's city list (nation `+0x48`), the town is listed if **any** of these holds:

```text
the town already holds a unit in the nation's recruitment table (slot troops > 0 and slot city = town)
fortification in 75..100
fortification > 100 and fortification % 100 >= 75     // an order in progress; current level >= 75
the town is the nation's capital
```

If more than one town already has units in training, an **"All cities"** entry is added at the top of the list. The default selection is the capital, or the town with the most units in training.

### 2. What `RecruitUnit` refuses, with the exact texts

| Condition, in the order checked | Message |
|---|---|
| the 40th recruitment slot is occupied (nation `+0x420`, which is slot 39's troops) | `You have reached your limit of 40 units.` |
| mobilisation (nation `+0x442`) is already 100 | `Your mobilisation rate is already 100%.` |
| a town is selected, it is not the capital, and its fortification word is ≤ 74 | `This city's fortification has fallen below 75%.` |

- **"Fallen below"** matches the case the list allows: a town still listed only because it has units in training, whose fortification has since dropped.
- **No treasury check:** `RecruitUnit` has no money check, so the treasury can go negative through recruitment.
- **When accepted:**
  - the first empty slot gets `state 0, type, troops, city`, and **"All cities"** means the capital;
  - the treasury (`+0x438`) drops by `troops / 200 × cost(type)`, matching [decompiled-recruitment-cost-formula.md](decompiled-recruitment-cost-formula.md);
  - mobilisation rises by `troops × 1000 / wealth(+0x430) + 1`, capped at 100.

### 3. Troop amounts in the dialog (`NewUnitType`, `ChangeUnitSize`)

```text
on choosing a type:   amount = battalion(type) / 5
arrow buttons:        amount ± 100 (small spin) or ± 1,000 (large spin)
after every change:   amount = max(battalion / 5, min(battalion, amount))
```

| Type | DAT battalion (`+0x1A`) | Dialog maximum | Dialog minimum = default | Cost per 200 (`+0x22`) |
|---|---:|---:|---:|---:|
| Light infantry | 15,000 | 15,000 | 3,000 | 2 |
| Heavy infantry | 6,000 | 6,000 | 1,200 | 20 |
| Archers | 3,500 | 3,500 | 700 | 4 |
| Light cavalry | 7,000 | 7,000 | 1,400 | 15 |
| Heavy cavalry | 2,500 | 2,500 | 500 | 30 |

- **The maxima equal the DAT battalion sizes.** Light infantry 15,000 matches the player's recollection. For archers the dialog maximum is **3,500**, not 3,000.
- **Where "3,000" appears:** it is the light-infantry *minimum*, and also its default when the type is picked. That may be what the player remembers.
- **Not whole battalions:** the amount does *not* default to the full battalion. It starts at one fifth.
- **The last step can be partial.** Because of the clamp, a ±1,000 step near the limits can move by less than 1,000.

### 4. The AI's recruitment (`FUN_004504F4`)

- **Where** (`FUN_004502E0`):
  - The AI recruits at its **capital** by default.
  - It picks another town only when all three hold: it is at war with someone (a relation value of 3), one of its armies is within 15 squares of its capital, and more than a third of its units in training are already at the capital.
  - Then it chooses, among its own towns with **fortification word > 74** and fewer units than the capital, the one nearest the enemy's capital.
- **What** (`FUN_004501F4`):
  - The type comes from `Random(100)`: light infantry 0–34, heavy infantry 35–59, archers 60–74, light cavalry 75–89, heavy cavalry 90–99.
  - The amount is `battalion/3 + Random(battalion/5 × 4)`, rounded down to hundreds, capped at the battalion. That gives, for example, light infantry 5,000–15,000.
- **Limits:** at most 8 new orders per AI turn. The AI stops once mobilisation reaches 100 or the troop target is met.

### 5. Against the saves

- Every town holding units in training, for every nation, in the six saves: **118 town checks, 0 exceptions**. Each is either the nation's capital or has fortification ≥ 75.
- The non-capital recruiting towns are exactly the high-fortification ones. In `1_rome_270_winter_*.sav` they are:

  | City index | Fortification | Units in training |
  |---:|---:|---:|
  | 206 | 76% | 14 |
  | 267 | 98% | 1 |
  | 154 | 89% | 3 |
  | 104 | 91% | 3 |
  | 28 | 78% | 1 |
  | 114 | 78% | 3 |

  City 206 at 76% is the Isaura of #515, and 267 at 98% is Masada.
- **Few towns qualify:** at game start (`ng1_rome.sav`), only **23 of 334** towns have fortification ≥ 75%. The rest are 19 below 25%, 134 at 25–49% and 158 at 50–74%.

## Inferences

- **The rule for the build repository:** a town may take a new recruitment order if it is its nation's capital or its current fortification is ≥ 75%. A town below 75% that still has units in training keeps them, but takes no new order. `[derived]`: observations 1, 2 and 5.
- **Fortifying a town to 75% is how a player adds a recruiting town.** This matches the player's account. The fortification order itself (a `ChangeFortification` dialog at `0x44076C`, steps of 1 and 10) and its cost were not traced in this pass.
- **Two slightly different tests.** The dialog's list uses the decoded current level (`% 100` while an order is in progress). `RecruitUnit` and the AI compare the raw word with 74. A town with a fortify order in progress (raw value > 100) therefore passes `RecruitUnit` whatever its current level. That can only matter for a town that is already listed, which means it has units in training or is the capital. `[derived]`: from the code, not observed.
- **The AI and the player recruit differently:** the AI uses random types and roughly battalion-sized orders, while the dialog defaults to one fifth of a battalion. The composition of AI armies is random at recruitment, not chosen against an enemy.

## What this does not establish

- **No live run.** The dialog was not driven headless: the list contents and refusal texts come from the code, and the save check covers only towns that already hold units.
- The fortification order's cost, build rate and dialog limits.
- What the dialog's `PrintNumbers` shows beyond the cost already documented.

## Reproduction

1. In `Imperial Conquest 2.exe`, find `TArmyRecruits`'s method table (`RecruitUnit` at `0x454E78`).
2. In Ghidra, create functions at the handler addresses above and decompile them. The dump misses them, because they are reached only through the method table.
3. For the save check: for each nation, read its recruitment slots (nation `+0x2E4`, 8 bytes each), take each slot's city, and read that city's word at `+0x1A` in the city table (SAV offset `89,600 + city × 34`). Compare with the capital (nation `+0x444`).

## Next checks

1. Drive the recruit dialog headless on one save, at a capital, a 76% town and a 60% town: confirm the listed towns and the refusal text.
2. Trace the fortification order: its cost, its points per turn, and how long a town takes to reach 75%.
