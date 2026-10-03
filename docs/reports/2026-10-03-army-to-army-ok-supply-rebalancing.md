# Army to army transfer: what `OK` does with supply and money

**The question** (clone bug [diegoami/imperial_conquest_2#619](https://github.com/diegoami/imperial_conquest_2/issues/619)). [supply-capacity-rounding.md](supply-capacity-rounding.md) says `TArmyToArmy_OK` caps each army at `troops div 100` and pushes the excess to the other army. [army-to-army-transfer-confirmed.md](army-to-army-transfer-confirmed.md) covers the dialog and the emptied-army merge. Four things are open:

- which army pushes first;
- what happens when both armies end above capacity;
- whether money is treated the same way;
- how this interacts with `FUN_0044A698` and the merge, and whether anything refuses the order.

Line numbers prefixed `:` are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`.

## Answer

Call **A** the army that was selected when the order was given (the form's `+0x76C`), and **B** its partner (`+0x76E`). `sX`, `mX` and `TX` are army X's supplies (`+0x0A`), money (`+0x0C`) and total troops. All arithmetic is signed 16-bit except the troop sums.

1. **A pushes first, then B pushes back.** `OK` runs these steps in this order (`:44572–44649`): `[confirmed: code]`
   1. Write the dialog's mobilisation value back to the nation (`+0x442`).
   2. Copy A's working record back, then call `FUN_0044A80C(A)`, which only redraws A's map marker by size.
   3. Do the same for B.
   4. `capA = FUN_0044A698(A) div 100`. If `capA < sA`: `sB := sB + (sA − capA)`, `sA := capA`.
   5. `capB = FUN_0044A698(B) div 100`. If `capB < sB` (this `sB` already includes step 4's push): `sA := sA + (sB − capB)`, `sB := capB`.
   6. If A's slot-0 troops are 0 (A is empty): select B, then `sB += sA`, `mB += mA`, and delete A (`FUN_0044AB90`).
   7. If B's slot-0 troops are 0: `sA += sB`, `mA += mB`, and delete B.
   8. Close with `ModalResult = 1`.
2. **Both armies above capacity: the surplus is kept, on A.** Write `S = sA + sB` for the committed totals. After steps 4–5:

   ```text
   a1 = min(sA, capA);   b1 = sB + max(0, sA − capA)
   B  = min(b1, capB);   A  = a1 + max(0, b1 − capB)
   ```

   Nothing is lost and nothing is clamped away: `A + B = S`. When `S > capA + capB`, **B ends at exactly `capB` and A holds `S − capB`**, which is above A's own capacity. The army you selected keeps all the excess. `[confirmed: code]`
3. **Money is not rebalanced.** `OK` never compares money with anything. Money moves in the dialog only, and only the merge adds it. The dialog's money stepper is a different rule from the supply stepper (see item 6). `[confirmed: code]`
4. **`FUN_0044A698` is not a readiness threshold.** It is the army's total troops, with 1 returned for an empty army. It is therefore the capacity in steps 4–5, not a second rule. An empty army has capacity `1 div 100 = 0`, so its whole supply is pushed out in step 4 or 5. The merge in step 6 or 7 then adds the emptied army's remainder back to the survivor. **When one army is emptied, the survivor ends with all of `S` and all of the money, uncapped**, even above its own capacity. Both armies empty (every unit disbanded): A merges into B and is deleted, then B's totals are added to A's dead record and B is deleted, so supply and money vanish. `[confirmed: code; derived for the both-empty edge]`
5. **Nothing refuses `OK`.** The refusals come earlier:
   - **The menu order** (`TUnitMap_ArmyToArmyTransfer`, `0x00447288`) silently does nothing in three cases:
     - no army is selected, or a fleet with no army aboard is selected;
     - the selected army is not the current nation's;
     - no other army of the same owner is at Chebyshev distance **exactly 1** (`FUN_00449D64` → `FUN_004492A0`).
   - **Per-unit Transfer in the dialog** refuses three cases, each with a message:
     - the receiving list already has 20 units: *"This army already has 20 units."*;
     - the receiver would pass 100,000 troops: *"An army can not hold more than 100,000 troops."*;
     - the receiving army is aboard a fleet and `ships < (troops + unit) div 500`: *"This fleet can not carry any more troops."* (`:44091–44250`).
   - **Disband in the dialog** refuses a *regular* unit unless an own city lies in the 3 × 3 around A: *"An army must be near its own city to disband a regular unit."* (`:44253–44336`).

   `[confirmed: code]`
6. **The dialog's steppers, for completeness.** `[confirmed: code]`
   - **Supply:** each click moves `min(step, room(receiver), sGiver)`. The step is 10 or 100. The room is `max(0, TroopCount(receiver) div 100 − sReceiver + 1)` (`FUN_00442310`, exported for this report). In the dialog an army can therefore be filled to `troops div 100 + 1`, and `OK` then trims it to `troops div 100`.
   - **Money:** each click moves `min(step, 1000 − mReceiver, mGiver)`, with **no floor at 0** (`:44044–44088`). So a receiver already above 1,000 gets a negative step: one click moves `mReceiver − 1000` the other way. A purse cannot be raised above 1,000 *in the dialog*, but the merge in item 4 can exceed 1,000.

**Split army uses the same form.** `TUnitMap_SplitArmy` creates an empty partner (`FUN_00449F08`) and opens this same `TArmyToArmy` class (`0x0044170C`). An empty partner is what makes the title read "Split army" (`FUN_00441B50`). All of the above applies to a split. Cancel on a split deletes the new army; Cancel otherwise commits nothing. `[confirmed: code]`

## Method

- Read `TArmyToArmy_InitializeForm`, `ChangeSupply`, `ChangeMoney`, `Army1Transfer`, `Army2Transfer`, `Army1Disband`, `MoveUnit`, `RemoveUnit`, `TroopCount`, `OK` and `Cancel` (`:43756–44660`). Also read `FUN_00441B50` (partner choice), `TUnitMap_ArmyToArmyTransfer`, `TUnitMap_SplitArmy`, `FUN_00449D64`, `FUN_0044A698`, `FUN_0044A80C`, `FUN_0044AB90`, and the min/max helpers `FUN_00448FD0`/`FD8`, which are signed 16-bit.
- `FUN_00442310`, the dialog's supply room, is missing from the dump. It was exported with `ExportAddresses.java 0x00442310`.
- Checked the one recorded transfer, `1_rome_270_winter_3.sav` → `_winter_5.sav` from [army-to-army-transfer-confirmed.md](army-to-army-transfer-confirmed.md), for an over-cap army.

## Observations

**`OK`, steps 4–7** (`:44604–44646`, abridged; `s[]` = `+0x0A` supplies, `m[]` = `+0x0C` money, `u0[]` = `+0x14` slot-0 troops):

```c
cap = (short)(FUN_0044a698(A) / 100);
if (cap < s[A]) { s[B] += s[A] - cap;  s[A] -= s[A] - cap; }
cap = (short)(FUN_0044a698(B) / 100);
if (cap < s[B]) { s[A] += s[B] - cap;  s[B] -= s[B] - cap; }
if (u0[A] == 0) { selection = B; s[B] += s[A]; m[B] += m[A]; FUN_0044ab90(A); }
if (u0[B] == 0) {                s[A] += s[B]; m[A] += m[B]; FUN_0044ab90(B); }
```

**The supply room** (`FUN_00442310`, Ghidra export):

```c
iVar1 = TArmyToArmy_TroopCount(form, armyCopy);              // plain sum, no 1-guard
FUN_00448fd8(0, (short)(iVar1 / 100) - armyCopy.supplies + 1);   // max(0, T div 100 - s + 1)
```

**The partner** (`FUN_00441B50`). B is the highest-index army of the same owner at Chebyshev distance 1, other than A. If any such army has slot-0 troops 0, B is the highest-index of those instead, and the split flag is set. `TUnitMap_ArmyToArmyTransfer`'s own scan (`FUN_00449D64`) is used only as the gate.

**The recorded transfer does not exercise the push.** Rome's armies are 0 and 2:

| Army | Week 3 | Week 5 |
| --- | --- | --- |
| 0 | 72,177 troops (cap 721), 470 t | 99,882 troops (cap 998), 204 t |
| 2 | 55,932 troops (cap 559), 365 t | 28,227 troops (cap 282), 184 t |

Both are under capacity on both sides, and a turn of consumption lies between the saves.

**Worked example** `[derived]`. A has 40,000 troops and 500 t; B has 40,000 troops and 500 t. In the dialog the player disbands a 10,000 mercenary unit from each, so `capA = capB = 300` and `S = 1000`.

- Step 4: A pushes 200, so A = 300 and B = 700.
- Step 5: B pushes 400 back, so A = 700 and B = 300.

Final: **A 700, B 300**. Had B been selected (roles swapped), the totals would be B 700, A 300.

## Inferences

- **The clone today.** `ArmyTransferCommandHandler` rejects a transfer whose supply would pass the receiver's capacity (`SupplyExceedsCapacity`). It also caps the merged purse and sends the excess to the treasury. The original does neither:
  - it never refuses at commit;
  - it pushes the excess per steps 4–5;
  - its merge adds money with no cap.

  A faithful port applies steps 4–7 after the unit and supply moves, and keeps the dialog-time limits (supply room `+1`, money `1000 − m`, unfloored) as the only input bounds. `[derived]`
- **The surplus left on A makes over-capacity armies reachable in normal play.** For example, disband in the dialog, or join with an army that holds more than its share. Those armies are then trimmed only by `FUN_0044F6D8` at a friendly city (excess back to the city), by the weekly consumption, or by the next `OK` that touches them ([supply-capacity-rounding.md](supply-capacity-rounding.md)). `[derived]`
- **A disband inside the dialog changes mobilisation.** A regular unit disbanded there lowers the nation's mobilisation by `troops × 1000 div wealth(+0x430) + 1`, floored at 0 (`RemoveUnit`, `:44466–44507`). It is committed at `OK` step 1. This is the inverse of mobilising. `[confirmed: code]`

## What this does not establish

- **A live confirmation of the A-keeps-surplus rule.** No save in hand has a transfer that left an army over capacity. A proposed run:
  - **Start:** any Rome save with two adjacent Rome armies next to a Rome city, each holding mercenary units and supply near `troops div 100`.
  - **Orders:** select army A; open *Army to army transfer*; in each list, disband one mercenary unit of about 10,000 troops (mercenaries need no city); OK; save.
  - **Measure:** both armies' supplies against `capA`, `capB` and `S` from the pre-save. Prediction: B = `capB`, A = `S − capB`.
  - **Second run:** the same with B selected, to confirm the asymmetry.
  - **Third run:** a transfer that empties A, to confirm the uncapped merge.
- The both-empty edge was read from code only.
- Whether an army aboard a fleet can be A. The order accepts a selected fleet's carried army, but the partner search uses that army's own stored position, which was not traced for aboard armies.
