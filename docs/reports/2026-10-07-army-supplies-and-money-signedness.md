# Army supplies and money are signed words, never persistently negative

**The question** ([decompilation plan](../decompilation-plan.md) item 14, raised by T44 and its
reviewer, build repo PR #135): is `ArmyRecord.Supplies` (`+0x0A`) — and `Money` (`+0x0C`) — read
and written **signed** or **unsigned**? Two incidental `MOVSX` reads of `+0x0A` were known
(`0x004516A8`, `0x0044AAE4`), but the field had never had the exhaustive write-site enumeration
that `+6` (moves) received in
[army-moves-field-signed-and-the-ffff-underflow.md](army-moves-field-signed-and-the-ffff-underflow.md),
and no save in the corpus (maximum 796) can distinguish the two readings. Flipping `IC2.Data` to
`short` on partial evidence was the mistake this item existed to avoid.

## Answer

**Both fields are signed words — every reader in the application treats them signed, and no
unsigned (`JAE`/`JBE`-class) read exists** — and **no write path can persist a negative value**:
every subtraction that could overdraw is either capped before the write or floored at 0 by a
`max(0, ·)` in the same pass. `IC2.Data` may type both `short` with a "never persistently
negative" invariant; the invariant is the original's own, enforced in code, not an assumption.
`[confirmed: decompile]`

Two **transient** in-loop negatives exist, both inside the quarterly upkeep loop
([upkeep-payment-and-desertion.md](upkeep-payment-and-desertion.md)), both floored before the
loop moves on — the only places the fields are ever negative at all.

## 1. Supplies (`+0x0A`, `DAT_0047c1f6`): every write, with its guard

| # | Site | Write | Guard | Can go negative? |
| --- | --- | --- | --- | --- |
| 1 | `FUN_00449f08` :48738 (army creation) | `= 0` | — | no |
| 2 | weekly tick `FUN_004514ec` :54503/:54508 | `−= troops/200` (aboard a fleet) or `−= (90 − seasonTable[season]) × troops / 20000` | **`= max(0, ·)` immediately after** (:54510–54511) | no — floored every week |
| 3 | `TAFSupply_ChangeSupply` :42969 | `+= delta` | withdraw branch clamped by `max(delta, −supplies)` (:42923), deposit capped at capacity (:42959) | no |
| 4 | `TAFSupply_TransferSupply` :43065 | `+= buyAmount` | buy amount ≥ 0, capped (:43028, :43041) | no |
| 5 | `TArmyToArmy_OK` :44608–44621, :44629, :44639 | move-excess-above-requirement; additive merges | source left exactly at its requirement | no (from ≥ 0) |
| 6 | `TUnitMap_JoinArmies` :46994 | additive merge | — | no (from ≥ 0) |
| 7 | `TUnitMap_DisbandArmy` :47114 | read-only (into a city's stock) | — | — |
| 8 | instant battle `FUN_0044aee4` :49650–49654 | additive absorb, then `= min(supplies, troops/100)` | min cap | no |
| 9 | AI resupply `FUN_0044f6d8` :53112 | `+= min(troops/100 − supplies, cityStock)` | the min itself: above capacity the negative deficit *reduces* toward capacity, never past it | no |
| 10 | army split `FUN_0044f8fc` :53198–53200 | thirds to the new army | thirds of ≥ 0 | no |
| 11 | AI army merge `FUN_004509f0` :53982 | additive | — | no |
| 12 | `TBattleOver_OK` :57621–57625 | additive absorb, then min cap | — | no |
| 13 | quarterly upkeep `FUN_00451b40` :54760 | `−= troops/100` when a mercenary deserts | **unguarded — can overdraw in-loop**; `= max(0, ·)` at :54774 before the army's loop ends | transiently; never persisted |

Row 13 is the one new fact for
[upkeep-payment-and-desertion.md](upkeep-payment-and-desertion.md): the deserter's supply carry-off
is the only unguarded supplies subtraction in the application, and the same loop that allows it
floors the field back to 0 (:54774, `psVar11[3] = max(0, psVar11[3])`).

## 2. Money (`+0x0C`, `DAT_0047c1f8`): every write, with its guard

| # | Site | Write | Guard | Can go negative? |
| --- | --- | --- | --- | --- |
| 1 | `FUN_00449f08` :48740 | `= 0` | — | no |
| 2 | `TAFSupply_TransferSupply` :43080 | `−= payment` | buy amount capped at `money × 5` (:43041), so `payment = amount/5 ≤ money/5` | no |
| 3 | `TAFSupply_ChangeMoney` :43134/:43168 | `±= amount` | deposit capped at `1000 − money` (:43120), withdraw capped at `money` (:43155) — the same 1000 cap as [2026-10-05-army-purse-writes-and-the-1000-cap.md](2026-10-05-army-purse-writes-and-the-1000-cap.md) | no |
| 4 | mercenary hire | — | **no write at all**: the price is a gate, not a charge ([2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md](2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md)) | — |
| 5 | merges: `TArmyToArmy_OK` :44631/:44641, `TUnitMap_JoinArmies` :46992, `FUN_0044aee4` :49648/:49687, `FUN_004509f0` :53981, `TBattleOver_OK` :57618 | additive | — | no (from ≥ 0) |
| 6 | `TUnitMap_DisbandArmy` :47109 | read-only (into the treasury) | — | — |
| 7 | AI resupply `FUN_0044f6d8` :53092–53108 | cap 1000 / top-up +500 (own city); `−= amount/5` (foreign purchase) | top-up gated on `treasury > 0`; purchase amount `≤ money/5` (:53106), so `amount/5 ≤ money/25` | no |
| 8 | army split `FUN_0044f8fc` :53201–53203 | thirds | thirds of ≥ 0 | no |
| 9 | quarterly upkeep `FUN_00451b40` :54765 | `−= cost × quality / 5` per mercenary | **signed `purse < 1` desert gate before each unit** (`CMP/JLE` at `0x00451C1C`, per the upkeep report's listing); the last payment can overdraw; `= max(0, ·)` at :54772 | transiently; never persisted |

Row 9 restates the upkeep report's finding in this enumeration's terms: the overdraft is visible
only to the next unit's desert gate within the same loop, and is written off before the army is
left.

## 3. Every reader is signed

`+0x0A`: the two known `MOVSX` sites (weekly tick :54512 `supplies × 10000 / troops`;
`FUN_0044aab4` :49328, the multiply-order inconsistency already recorded), the display reads
(`TInformation_ShowArmyDetails` :41041/:41047, `TAFSupply_PrintNumbers` :42784,
`TBattleOver_InitializeForm` :57546 "no suuplies" — sic), the mercenary-supply gate
`TUnitMap_RecruitMercenaries` :46893 (`supplies × 10000 / troops < 15`), and the supply-percentage
helpers `FUN_00459740` :57698 / `FUN_0045ae68` :58248. `+0x0C`: the hire gate
`TRecruitMercs_RecruitMercUnit` :43633 (signed `<`), the end-turn mercenary-pay warnings
`TToEndTurn_InitializeForm` :57833 and `FUN_0045af00` :58320 (signed `<`), displays (:41060,
:42812, :57532), and the AI gates (`FUN_0044e41c` :52234 `> 50`, `FUN_0044e670` :52342 `/ 5`).
**No `JAE`/`JBE`-class unsigned comparison on either field appears anywhere in the dump.**
`[confirmed: decompile]`

Two look-alikes were excluded, both **fleet** records, not armies: the weekly tick's and the
end-turn check's `+0x0A == -1` tests (:54546/:54552, :57803, :58306) read the fleet construction
countdown, whose `-1` means "launched" — a genuine signed sentinel on a different table.

## 4. What the reimplementation needs

Type both fields `short` (signed 16-bit) in `IC2.Data`, matching every reader. Keep the
"never persistently negative" invariant explicit and test it where the original enforces it:
the weekly consumption floor, the two `TAFSupply` caps, and the quarterly loop's per-army
`max(0, ·)` on both fields — including the transient last-payment overdraft on money and the
deserter's unguarded supply carry-off, which a faithful clone reproduces and then forgives.

## What this does not establish

- The guards are classified at **decompiler level** (the `<`/`≤`/`max`/`min` renderings), except
  the one instruction the upkeep report already listed (`0x00451C1C`, `JLE`). No new Ghidra
  listing was taken; if instruction bytes are wanted, `DumpListing2.java` on `FUN_00451b40`'s
  army loop and `FUN_004514ec`'s covers all the load-bearing comparisons in one run.
- The enumeration walked every dump reference to `DAT_0047c1f6`/`DAT_0047c1f8` (93 lines) plus
  every base-relative `+10`/`+12` write inside functions that reference the army-table base. A
  write through a pointer alias not visibly anchored to `DAT_0047c1ec` would be missed — the same
  residual risk item 13's enumeration accepted.
- Whether any save ever held a negative value mid-loop: by construction above, none can persist,
  so the corpus's silence is expected and is not independent evidence.

## Reproduction

```text
weekly tick   FUN_004514ec :54497–54530   (consumption writes :54503/:54508, floor :54510–54511)
quarterly     FUN_00451b40 :54741–54781   (upkeep loop; gates :54759/:54765; floors :54772/:54774)
AI resupply   FUN_0044f6d8 :53089–53113
split         FUN_0044f8fc :53198–53203
all other sites: tables in §1–§2, dump line numbers in the Site column
```
