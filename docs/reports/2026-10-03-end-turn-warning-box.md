# The "End turn ?" box: every trigger, its threshold, and what the buttons do

**The question** (clone bug [diegoami/imperial_conquest_2#586](https://github.com/diegoami/imperial_conquest_2/issues/586)). End turn sometimes opens a box titled "End turn ?" that reads "An army of yours needs supplies." ([2026-10-02-unit-map-mouse-orders-and-tax-range.md](2026-10-02-unit-map-mouse-orders-and-tax-range.md)), or "An army of yours cannot afford to pay its mercenary units." ([2026-10-02-two-human-seats.md](2026-10-02-two-human-seats.md)), and once read several lines ([2026-10-02-naval-battles.md](2026-10-02-naval-battles.md)). The questions:

- every trigger, with its exact condition;
- whether "needs supplies" is per army or per unit, and against which threshold;
- whether armies aboard a fleet count;
- what the mercenary line tests;
- the order of the checks, how many boxes can appear, and what each button does.

Line numbers prefixed `:` are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`.

## Answer

**Flow** `[confirmed: code]`:

1. `TPremierForm_EndTurn` (`0x0045B0A8`, `:58338`) sets the form's ready flag (`+0x434`) to 1.
2. It calls the gate `FUN_0045AF00` (`:58264`), which clears the flag when any trigger below holds. The gate forces the flag back to 1 when the current nation is computer-controlled (nation `+0x490 == 0`), so **AI seats never see the box**.
3. If the flag is 0, `EndTurn` opens `TToEndTurn` modally (`0x004595D8`). Its `InitializeForm` (`0x00459828`) re-runs the same tests to build the text lines.
4. After the box closes, `EndTurn` ends the turn only if the flag is now 1.

**Per army, per fleet, never per unit.** A unit matters only through its army's totals. Each record that trips adds one line, so two hungry armies give two identical lines.

**The triggers, in the order they are checked.** All armies come first in table order, then all fleets in table order.

| # | Record | Filter | Trigger (opens the box) | Line |
| --- | --- | --- | --- | --- |
| 1 | each army with owner (`+4`) = current nation and `+8 ≥ 0` (**not aboard a fleet**) | has **not acted** this week: `FUN_0044AAB4(a) == 0`, i.e. moves `+6` equals the recomputed full allowance | `supplyPct < 20` **and** `armySource(a) ≥ 0` | *An army of yours needs supplies.* |
| 2 | same army | same | `money(+0x0C) < mercPay` (strict) | *An army of yours cannot afford to pay its mercenary units.* |
| 3 | each fleet with owner (`+8`) = current nation and `+10 == −1` (launched) | has not acted: `FUN_0044AB0C(f) == 0` | no own city in the 3 × 3 around the fleet (`FUN_004494E4 == −1`) | *One of your fleets is not docked at its own city.* |
| 4 | same fleet | same | `supplies(+14) < ships(+18) div 5` **and** `fleetSource(f) ≥ 0` | *A fleet of yours needs supplies.* |
| 5 | the army aboard that fleet (`+22 ≥ 0`) | the **fleet's** not-acted test | `supplyPct(army) < 20` **and** `fleetSource(f) ≥ 0` | *An army of yours needs supplies.* |
| 6 | same aboard army | same | `army.money < mercPay(army)` | *An army of yours cannot afford to pay its mercenary units.* |
| — | same fleet | same | **never opens the box**: `condition(+20) < 65` only adds a line when the box is already open | *A fleet of yours needs repairing.* |

**The formulas** (`FUN_0045AE68` for the gate and `FUN_00459740` for the box; the two are identical) `[confirmed: code]`:

- `T = FUN_0044A698(army)`, the sum of the 20 slots' troops, or 1 when that sum is 0.
- `supplyPct = int16((supplies × 10000) div T)`: supply as a percentage of capacity `troops / 100`. The test `supplyPct < 20` is, for `supplies ≥ 0`, exactly **`500 × supplies < T`**: under **20 % of capacity**. Example: a 50,000-troop army (capacity 500) warns at 99 t and not at 100 t.
- `mercPay = Σ int16(((troops div 200) × price[type] × quality) div 5)`, accumulated in an int16, over the slots with `troops > 0` and marker (`+0`) `> 0`, i.e. **mercenary units only**. This is one round of mercenary pay as charged by the upkeep code ([upkeep-payment-and-desertion.md](upkeep-payment-and-desertion.md)). The box fires when the purse is **strictly below** it. An army with no mercenaries has `mercPay = 0`, so it fires only on a negative purse. The weekly upkeep floors purses at 0 ([upkeep-payment-and-desertion.md](upkeep-payment-and-desertion.md)).
- **`armySource(a) ≥ 0`** (`FUN_0044E670`) holds whenever the nation owns at least one city. Its fallback picks the nearest own city whatever its stock. Without a city, the test can still pass on a foreign, non-hostile city in two-stage form:
  - **The nation must be at war with someone.** Without a war, the test fails.
  - **The city must qualify:** relation to its owner `< 3`, stock `> T div 1000 + 80`, and army money `> (T div 1000) div 5`.

  In practice: **"needs supplies" fires for any nation that owns a city.** `[confirmed: code]`
- **`fleetSource(f) ≥ 0`** (`FUN_0044E9A8`) holds when the nation owns a **port city**, or when a non-hostile foreign port has stock `> 120` and the fleet has money `> 10`. A port city is one with a sea or rough-sea cell (map code `< 2`) in its 3 × 3 (`FUN_0044E920`), outside the eastern zone `x ≥ 248`, or `x ≥ 214` and `y ≥ 99` (`FUN_004496BC`). `[confirmed: code]`

**Aboard armies are checked only through their fleet** (rows 5–6). They are skipped by the army loop (`+8 == −1`). They are checked only when the carrying fleet is launched and has not acted, and their supply line uses the **fleet's** port test, not the army's city test. `[confirmed: code]`

**One box per End turn click, at most five lines.** `FUN_004597D8` appends a line and caps the count at 5. A sixth or later trigger overwrites an unpainted sixth slot, so the first five triggers in the order above are what shows. Lines are not de-duplicated. The fixed text comes from the form resource:

- caption **"End turn ?"**;
- *"If you have not finished your turn click MAKE MORE MOVES."*;
- *"If you are finished moving this turn click END TURN."*;
- buttons **End turn** (`btn_ok`, `OnClick = EndTurnOK`) and **Make more moves** (`Button1`, `OnClick = EndTurnCancel`).

`[confirmed: code + the TPF0 resource]`

**The buttons** `[confirmed: code]`:

- **End turn** (`TToEndTurn_EndTurnOK`, `0x00459B44`) sets the ready flag to 1 and closes the box. `EndTurn` then ends the turn: forms close, the turn position advances, the weekly tick runs on the wrap, and the next seat starts.
- **Make more moves** (`EndTurnCancel`, `0x00459B80`) sets the flag to 0 and closes the box. `EndTurn` returns and the human keeps playing. The next End turn click re-runs every check from scratch.
- Closing the box any other way leaves the gate's 0, which behaves like Make more moves. `[derived]`

## Method

- Read `TPremierForm_EndTurn`, `FUN_0045AF00`, `FUN_0045AE68`, the `TToEndTurn` methods (`InitializeForm`, `EndTurnOK`, `EndTurnCancel`, `PaintForm`) and `FUN_00459740`/`FUN_004597D8`, all in the dump (`:57688–57920`, `:58238–58366`).
- Read the helpers there too: `FUN_0044AAB4`, `FUN_0044AB0C`, `FUN_0044E670`, `FUN_0044E9A8`, `FUN_0044E920`, `FUN_004496BC`, `FUN_004494E4` and `FUN_0044A698`.
- Searched the original EXE's bytes, locally, for the form's static strings to read the `TToEndTurn` `TPF0` resource. No bytes from it enter this repository.

## Observations

**The gate, army half** (`FUN_0045AF00`, `:58264–58300`, abridged):

```c
for (a = 0; a < armyCount; a++)
  if (army[a].owner == cur && army[a].cell /*+8*/ >= 0)
    if (!FUN_0044aab4(a)) {                              // not acted
      FUN_0045ae68(a, &mercPay, &supplyPct);
      FUN_0044e670(a, &src);
      if ((supplyPct < 0x14 && src >= 0) || army[a].money /*+0xC*/ < mercPay) ready = 0;
    }
```

**The gate, fleet half** (`:58301–58333`):

```c
for (f = 0; f < fleetCount; f++)
  if (fleet[f].owner == cur && fleet[f].countdown /*+10*/ == -1)
    if (!FUN_0044ab0c(f)) {                              // not acted
      FUN_0044e9a8(f, &src);
      if (FUN_004494e4(owner, fleet[f].xy) == -1 ||
          (fleet[f].supplies < fleet[f].ships / 5 && src >= 0)) ready = 0;
      if (fleet[f].army >= 0) {
        FUN_0045ae68(fleet[f].army, &mercPay, &supplyPct);
        if ((supplyPct < 0x14 && src >= 0) || army[fleet[f].army].money < mercPay) ready = 0;
      }
    }
if (nation[cur].human /*+0x490*/ == 0) ready = 1;
```

**The box's lines** (`TToEndTurn_InitializeForm`, `:57731–57847`). It runs the same two loops in the same order, with the same conditions. Each condition appends its line. The repair line is added before the docked line, at `condition < 0x41`. That condition appears only here, not in the gate.

**The line buffer** (`FUN_004597D8`): `strcpy(form + 0x1C8 + count × 0x51, text); count = min(5, count + 1)`. `PaintForm` draws `count` lines at `y = 0x18 + 16 i`.

**The resource.** `TPF0 TToEndTurn` holds Caption `End turn ?`, `Label6` "If you have not finished your turn click   MAKE MORE MOVES.", `Label1` "If you are finished moving this turn click   END TURN.", `btn_ok` "End turn" → `EndTurnOK`, and `Button1` "Make more moves" → `EndTurnCancel`.

**Agreement with the live boxes:**

| Box | Report | Code row |
| --- | --- | --- |
| "needs supplies" alone | Rome, unit-map run | row 1 |
| "cannot afford to pay its mercenary units" alone | Ptolemaic, two-human run | row 2 or 6 |
| armies + repair + not docked + fleet supplies together | naval run | rows 1, 2, —, 3, 4 |

The order in the naval run's box (army lines first, then *repairing*, *not docked*, *fleet needs supplies*) is the code's order.

## Inferences

- **"Has not acted" is the filter, so the box ignores armies that have moved.** `FUN_0044AAB4` returns *acted* when the moves field differs from the recomputed full allowance. Three kinds of army are therefore never warned about:
  - an army that has moved this turn;
  - a new army from Split army, which starts with moves 0 for a human;
  - an army whose weekly allowance was written with the tick's supply penalty but is recomputed here without it, or the reverse. `FUN_0044AAB4` tests `supplies × troops div 10000 < 10` while the tick tests `supplies × 10000 div troops < 10` ([army-moves-field-signed-and-the-ffff-underflow.md](army-moves-field-signed-and-the-ffff-underflow.md)).

  The third case bites hardest for large starving armies, the ones the warning is for: a 100,000-troop army on 50 t gets the tick's −1 but not the recomputation's, so it reads as "acted" and gets no warning. `[derived]`
- **`supplyPct` is cast to int16.** An army holding more than about 3.28 t per soldier (`supplies × 10000 div T ≥ 32768`) wraps negative and is reported as needing supplies. This needs supply above ~328 × capacity, so it is practically unreachable. `[derived]`
- **The mercenary line is a forecast, not the desertion rule.** Desertion happens at pay time when the purse is `≤ 0` ([upkeep-payment-and-desertion.md](upkeep-payment-and-desertion.md)). The box warns whenever the purse is below one full round of pay, every turn, whether or not a pay day is near. `[derived]`
- **For the clone:** a faithful box is a list built in this order, capped at five lines, shown only for human seats, with *End turn* (proceed) and *Make more moves* (abort). The repair line is not a trigger. `[derived]`

## What this does not establish

- **The full fleet-allowance formula behind `FUN_0044AB0C`.** It was read but not checked against saves:
  - start at `30 − (ships − 50) div 10`;
  - subtract `(troops div 100) div ships + 1` when carrying an army;
  - subtract 3 when supplies are 0;
  - subtract `(70 − condition) >> 2` when condition < 70.

  Whether launched fleets' saved moves match it is untested.
- **The "not acted" filter, live.** A cheap EXPLORE run:
  - **Start:** a human-seat save with two land armies, both under 20 % of capacity, the nation owning a city.
  - **Orders:** move one army one tile, leave the other, then End turn.
  - **Prediction:** one "needs supplies" line, not two.
  - **Second run:** move both. Prediction: no box at all.
- **The five-line cap, live.** It needs six or more simultaneous triggers.
- **The eastern exclusion zone in `FUN_004496BC`.** That it is the Caspian is an inference. That it explains Build fleet's refusal for Media ([2026-10-02-start-as-each-nation.md](2026-10-02-start-as-each-nation.md)) is likely but not traced: Build fleet's own port test was not read in this pass.
