# The AI's army merge `FUN_004509f0` and fleet merge `FUN_00450b30`, decompiled: candidate order, every gate, the carry-over, the removal

**Provenance.** `%LOCALAPPDATA%\ReTools\all_app_functions.txt` (59,228 lines, Ghidra whole-application decompile). Primary bodies: `FUN_004509f0` :53949-53999, `FUN_00450b30` :54002-54046. Helpers read in full (every `FUN_` they call): `FUN_0044a698` :49042, `FUN_0044a66c` :49019, `FUN_00449018` :47727, `FUN_00448fd8` :47671, `FUN_0044acb4` :49464, `FUN_0044ac3c` :49430, `FUN_0044a80c` :49141, `FUN_0044a878` :49172, `FUN_0044ad38` :49493, `FUN_0044ab90` :49372. Caller chain: `FUN_0044ffbc` :53459 (tail :53570-53577), `FUN_0044fa20` :53208, `FUN_00451fdc` :54939, and the compaction `FUN_0044adb0` :49537 with `FUN_0044abe0` :49396 and `FUN_0044ad7c` :49515. Research issue [#7](https://github.com/diegoami/imperial-conquest-2-research/issues/7), for IC2 task T159 (`imperial_conquest_2#959`). Date: 2026-10-11. Tags: `[confirmed: decompile]` is read straight off the bodies below; `[derived]` is my trace or inference from them.

Record bases (established elsewhere): army `0x0047C1EC`, stride `0x290`, count `DAT_004a0324`; fleet `0x0049C26C`, stride `0x1A`, count `DAT_004a0326`; current nation `DAT_004a0320`. In the army code, `short` arrays stepped by `0x148` are the 656-byte record, so `DAT_0047c1f0` = `+4` (owner), `DAT_0047c1f2` = `+6` (moves, signed: [army-moves-field-signed-and-the-ffff-underflow.md](army-moves-field-signed-and-the-ffff-underflow.md)), `DAT_0047c1f4` = `+8` (covered map cell, `-1` = aboard), `DAT_0047c1f6` = `+0xA` (supplies), `DAT_0047c1f8` = `+0xC` (money), `DAT_0047c1fc` = `+0x10` (unit slot 0), `DAT_0047c200` = `+0x14` (slot 0 troops). In the fleet code, arrays stepped by `0xd` shorts: `DAT_0049c274` = `+8` owner, `DAT_0049c276` = `+0xA` construction countdown, `DAT_0049c27a` = `+0xE` supplies, `DAT_0049c27c` = `+0x10` money, `DAT_0049c27e` = `+0x12` ships, `DAT_0049c282` = `+0x16` carried army.

## Summary

- **Both merges are two nested table-order loops, not a sort.** The outer loop walks the table from index 0 and takes the first record that passes the outer gates *and* has at least one valid partner; the inner loop walks the whole table from 0 and takes the first valid partner. Nearest, smallest and largest play no part. Each function stops after its first merge and is called once per computer seat per round.
- **The army function has no "orders outstanding" gate.** The summary row in `2026-10-07-strategic-ai-turn.md` §2.4 was wrong on that. The only army-state gates are `+8 >= 0` ("not aboard") on both sides. "The smaller army" is also wrong: the two sizes are never compared, so the outer army (< 20,000 troops) can be the larger of the pair; the partner only has to be < 80,000. The outer army is the donor: its money and supplies are added to the partner, and when its slot-0 troops are > 0 its units move over and it is deleted (A12 covers the slot-0 <= 0 case).
- **The fleet merge runs the other way round from the way the row reads.** The *outer*, idle fleet (ships < 40) **survives and takes everything**; the *inner* partner (any size, combined < 100) is **deleted**. The "no destination" gate is not a destination: it is `+0xA == -1`, the construction countdown (launched). The fleet record has no destination field that this function reads. The partner's "free the same way" is the same `+0xA == -1` plus no carried army.
- **Distances are Chebyshev and strict**: armies `< 18` (so up to 17), fleets `< 34` (so up to 33), by `FUN_00449018` = `max(|dx|, |dy|)`. Neither merge uses `FUN_004492A0` ("distance == 1") or `FUN_00449DD8` (the partner finder of Join fleets and Transfer ships).
- **Carry-over is plain 16-bit addition** of money and supplies into the survivor: no cap, no clamp, nothing to the treasury. Army unit slots are appended whole (no merging of same-type slots, no quality averaging). The survivor does not move.
- **Removal is in place, by tombstone** (owner `-1`), not by moving; the table is compacted at the next invocation of `FUN_0044adb0` (on entry to `FUN_00451fdc`, or just before a later computer seat), see C2. The army donor is deleted only when its slot-0 troops are > 0 at the start of the unit loop (A12); otherwise it stays live.

## Findings

| # | Finding | Tag |
| --- | --- | --- |
| A1 | Army outer loop `sVar7` runs 0 .. `DAT_004a0324`-1 in table order; the donor is the first record that passes A2 *and* finds a partner. Inner loop `sVar8` runs 0 .. count-1 in table order, skipping `sVar8 == sVar7`; the first partner passing A3 is taken. A donor with no partner falls through to the next donor. | `[confirmed: decompile]` :53964-53994 |
| A2 | Donor gates (all must hold): `owner (+4) == DAT_004a0320`; `FUN_0044a698(donor) < 20000` (int, strict); `+8 >= 0` (signed short; not aboard); table count - 1 >= 0 (always true here). No order, destination or moves field is read by the gates. | `[confirmed: decompile]` :53965-53968 |
| A3 | Partner gates (all must hold): `owner (+4) == DAT_004a0320`; `FUN_00449018(donor.xy, partner.xy) < 0x12` (18, signed short, strict, so Chebyshev <= 17); `FUN_0044a66c(donor) + FUN_0044a66c(partner) < 0x14` (20, strict); `FUN_0044a698(partner) < 80000` (strict); partner `+8 >= 0` (not aboard). The partner's size relative to the donor is never compared. | `[confirmed: decompile]` :53973-53980 |
| A4 | `FUN_0044a698(a)` = sum of the 20 unit slots' troops words (`+0x14 + 0x20k`, signed shorts, summed in an int); returns 1 if the sum is 0. This is the "troop total" for both 20,000 and 80,000, each army's own. | `[confirmed: decompile]` :49042 |
| A5 | `FUN_0044a66c(a)` = (highest slot index whose troops word is > 0) + 1, or 0 for an army with no unit. It is the slot **extent**, not a count of occupied slots. "Combined slots < 20" means `extent(donor) + extent(partner) <= 19`. | `[confirmed: decompile]` :49019 |
| A6 | Carry-over, in order: `partner.money (+0xC) += donor.money`; `partner.supplies (+0xA) += donor.supplies`; both are plain 16-bit short adds (no min, no 1000 cap, no clamp at 32767, no treasury deposit). Then, while the donor's slot-0 troops word `> 0`, `FUN_0044acb4(donor, partner, 0)` moves one slot. | `[confirmed: decompile]` :53981-53985 |
| A7 | `FUN_0044acb4(src, dst, 0)`: copies the 32-byte slot 0 of `src` (8 dwords: label, type, troops, quality and the rest) to `dst`'s slot index `FUN_0044a66c(dst)` (the first slot after the highest occupied one; gaps are not reused); `if src.moves (+6) == 0 then dst.moves = 0` (otherwise `dst.moves` is left as it is: no min, no max); then `FUN_0044ac3c(src, 0)`; then `FUN_0044a80c(dst)`. | `[confirmed: decompile]` :49464-49488 |
| A8 | `FUN_0044ac3c(src, 0)`: copies the donor's last occupied slot over slot 0 and zeroes that last slot's troops word; if slot-0 troops is now 0 (the donor had one slot left) it calls `FUN_0044ab90(src)` (delete), else `FUN_0044a80c(src)` (re-band the marker). Order of arrival at the partner for donor slots `[a, b, c]` with no gaps: `a`, then `c`, then `b`; in general slot 0, then the last occupied slot, then the next last, and so on, each appended after the partner's last occupied slot. No slot is merged with another, no quality is averaged, and there is no cap check inside (the A3 extent test is the only cap). | `[confirmed: decompile]` for the copy; the order for a given layout is `[derived]` by tracing :49430 |
| A9 | When the unit loop runs to the end (A12), the donor is **deleted in place** by `FUN_0044ab90`, reached from the last `FUN_0044ac3c`: the map word at the donor's (x, y) is set back to the donor's `+8` covered cell, and owner `+4 = 0xFFFF`. No compaction here. | `[confirmed: decompile]` :49372 |
| A10 | The partner (survivor) keeps its x, y, morale `+0xE` and every other field; only money, supplies, appended unit slots and (conditionally, A7) moves change. Its map marker is rewritten by `FUN_0044a80c`: `owner + 200` for total troops / 1000 below 25, `owner + 0xD8` for 25-49, `owner + 0xE8` for 50 and up, at the partner's x, y, only if its `+8 >= 0`. | `[confirmed: decompile]` :49141-49167 |
| A11 | After one merge `bVar1 = true`: the inner loop completes its remaining iterations with matching disabled by `!bVar1`, then the outer loop exits and the function returns. At most one army is removed per call. No news line, event, treasury write or carried-army link is touched by this function or the helpers it calls. | `[confirmed: decompile]` :53986 |
| A12 | **Donor with slot-0 troops <= 0.** Money and supplies are added first (:53981-53982). The unit loop `while (0 < slot-0 troops)` (:53983) is then skipped, so no unit moves and the donor is not deleted; `bVar1 = true` is still set (:53986). The donor stays live holding its money and supplies (now also added to the partner), and the call's one merge is used up. The original has no slot-0 gate before this. Whether such a donor can exist in a running game is not established (see Not established). | `[confirmed: decompile]` :53981-53986 |
| A13 | **Same tile.** In `FUN_0044acb4` the call order is `FUN_0044ac3c(src, 0)` (:49487), which on emptying the donor runs `FUN_0044ab90(src)` (:49454-49455) and restores the donor's covered cell, and only then `FUN_0044a80c(dst)` (:49488), which writes the survivor's marker. So if donor and survivor share a tile, the final map word is the survivor's marker. (For a donor with several units the marker is written by `FUN_0044a80c(dst)` after each slot; the tombstone comes with the last one.) | `[confirmed: decompile]` :49454-49455, :49487-49488 |
| F1 | Fleet outer loop `sVar6` runs 0 .. `DAT_004a0326`-1 in table order, inner `sVar7` runs 0 .. count-1 in table order skipping `sVar7 == sVar6`; the first valid pair wins; an outer fleet with no partner falls through. | `[confirmed: decompile]` :54016-54042 |
| F2 | Outer (the idle fleet, the **survivor**) gates: `owner (+8) == DAT_004a0320`; `ships (+0x12) < 0x28` (40, signed, strict); `carried army (+0x16) == -1`; `construction countdown (+0xA) == -1`. | `[confirmed: decompile]` :54018-54020 |
| F3 | Inner (the **absorbed** fleet) gates: `owner (+8) == DAT_004a0320`; `FUN_00449018(outer.xy, inner.xy) < 0x22` (34, strict, Chebyshev <= 33); `outer.ships + inner.ships < 100` (signed shorts summed in an int, strict, so 99 is the largest total); `inner +0x16 == -1` (no army aboard); `inner +0xA == -1` (launched). The inner fleet is not limited to 40 ships and is not compared with the outer one: it may be larger. | `[confirmed: decompile]` :54025-54029 |
| F4 | Carry-over into the **outer** fleet: `ships (+0x12) += inner.ships`; `money (+0x10) += inner.money`; `supplies (+0xE) += inner.supplies`; plain 16-bit adds, no cap. Not touched: the outer's x, y, moves `+0xC`, condition `+0x14`, owner. The inner's moves and condition are discarded (condition is not averaged or weighted). | `[confirmed: decompile]` :54031-54033 |
| F5 | Then `FUN_0044a878(outer)` re-bands the outer fleet's map word (`owner + 300` for ships <= 24, `+ 0x13c` for 25-49, `+ 0x14c` for 50 and up), then `FUN_0044ad38(inner)`: because inner `+0xA == -1` it sets the map word at the inner's x, y **to 0** (not to the `+0x18` covered cell); inner `+0x16` is -1 so no army is deleted; it sets inner owner `+8 = 0xFFFF` (tombstone). | `[confirmed: decompile]` :54034-54035, :49172, :49493 |
| F6 | After the merge `bVar1 = true`: the inner loop completes its remaining iterations with matching disabled by `!bVar1`, then the outer loop exits; one merge per call. No news line, event or treasury write. | `[confirmed: decompile]` :54036 |
| C1 | **Distance** for both merges is `FUN_00449018(a, b)`: `max(|dx|, |dy|)` via `FUN_00448fd8` (signed-short maximum of the two absolute differences): Chebyshev. `FUN_004492A0` is `FUN_00449018(a, b) == 1` and neither merge uses it. `FUN_00449DD8` (Join fleets and Transfer ships: the last other fleet of the same owner with `+0xA == -1` at distance exactly 1, in table order) is not used by either merge. | `[confirmed: decompile]` :47727, :47671, :47907, :48627 |
| C2 | **Compaction.** `FUN_0044adb0` scans armies and then fleets from the top down and, for each record whose owner is `-1`, copies the last record into its slot and decrements the count. For armies, `FUN_0044abe0` first renumbers any fleet `+0x16` that pointed at the last army. `FUN_0044adb0` runs unconditionally on entry to `FUN_00451fdc` (:54946) and again just before each computer-seat call to `FUN_0044fa20` (:54950-54951). `TPremierForm_EndTurn` advances the seat index and then calls `FUN_00451fdc` (:58357-58362). So the merged-away record is removed at the next invocation of `FUN_0044adb0`: on dispatcher entry, or before a later computer seat. If the merging computer seat is followed by a human seat, the loop exits without calling it again (:54947, :54953), and the tombstone persists into that human turn until the next dispatcher entry. It is never removed during the merge. | `[confirmed: decompile]` :49537, :49396, :49515, :54939 |
| C3 | **Calls per turn.** Each merge function has exactly one call site: the tail of `FUN_0044ffbc` (:53573-53574), reached in every week (`goto LAB_004501d6` at :53548 skips only the tax block). `FUN_0044ffbc` has one call site, in `FUN_0044fa20` (:53218), which runs once per computer seat whose unity is > 0, from the loop in `FUN_00451fdc`. So at most one army and one fleet are merged per computer nation per round. The army merge runs before that nation's army phase, the fleet merge before its fleet phase. | `[confirmed: decompile]` for the call sites; "once per round" `[derived]` from the seat loop |

## What the clone needs: the record fields behind the summary-row words

| Word in the old summary | Original record field | Value set | Tag |
| --- | --- | --- | --- |
| army "orders outstanding" | **none.** The gates read only owner `+4`, covered cell `+8`, x, y and the 20 slots' troops (`+0x14 + 0x20k`); the body also reads money and supplies (:53981-53982) to add them, and its helper reads moves (A7); no order field is read. | n/a | `[confirmed: decompile]` |
| army "not aboard" (both sides) | `+8` covered map cell, signed short | `>= 0` = on the map; `-1` = aboard a fleet | `[confirmed: decompile]` |
| fleet "no army aboard" (both sides) | `+0x16` carried army index | `-1` = none; otherwise the carried army's index | `[confirmed: decompile]` |
| fleet "no destination" (outer fleet) | **not a destination.** `+0xA` construction countdown | `24` at order, counting down while under construction (per [decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md)); `-1` (`0xFFFF`) = launched. The gate is `== -1` exactly. | test `[confirmed: decompile]`; countdown range from the cited report |
| fleet "free the same way" (inner fleet) | `+0xA == -1` and `+0x16 == -1`, the same two tests as the outer fleet (the 40-ship cap is not applied to it) | as above | `[confirmed: decompile]` |

Every field these two bodies read is decoded.

## Corrections to the old summary rows

- Army row: "the smaller army ... with orders outstanding" is wrong in two places: there is no orders gate, and "smaller" is not tested. "Within 18" means strictly less than 18 (Chebyshev <= 17). "Purses and supplies carry over" is right (plain additions, no cap), and so is "one merge per turn" (one per computer nation per round).
- Fleet row: the row left "absorbs... is absorbed by" undecided. The body settles it: the idle fleet (ships < 40) **survives and absorbs** the partner; the partner is deleted. "No destination" is the construction countdown (`+0xA == -1`). "Within 34" means strictly less than 34 (Chebyshev <= 33).

## Excerpts

### `FUN_004509f0`, the army merge

```text
:53949  // ==== FUN_004509f0 @ 004509f0 ====
:53950
:53951  void FUN_004509f0(void)
:53952
:53953  {
:53954    bool bVar1;
:53955    short sVar2;
:53956    int iVar3;
:53957    int iVar4;
:53958    short *psVar5;
:53959    short sVar6;
:53960    short sVar7;
:53961    short sVar8;
:53962
:53963    bVar1 = false;
:53964    for (sVar7 = 0; (!bVar1 && (sVar7 < DAT_004a0324)); sVar7 = sVar7 + 1) {
:53965      if ((&DAT_0047c1f0)[sVar7 * 0x148] == DAT_004a0320) {
:53966        iVar3 = FUN_0044a698(sVar7);
:53967        if (((iVar3 < 20000) && (-1 < (short)(&DAT_0047c1f4)[sVar7 * 0x148])) &&
:53968           (-1 < (short)(DAT_004a0324 + -1))) {
:53969          sVar8 = 0;
:53970          psVar5 = &DAT_0047c1f0;
:53971          sVar6 = DAT_004a0324;
:53972          do {
:53973            if (((!bVar1) && (sVar7 != sVar8)) && (*psVar5 == DAT_004a0320)) {
:53974              sVar2 = FUN_00449018((&DAT_0047c1ec)[sVar7 * 0xa4],*(undefined4 *)(psVar5 + -2));
:53975              if (sVar2 < 0x12) {
:53976                iVar3 = FUN_0044a66c(sVar7);
:53977                iVar4 = FUN_0044a66c(sVar8);
:53978                if ((int)(short)iVar3 + (int)(short)iVar4 < 0x14) {
:53979                  iVar3 = FUN_0044a698(sVar8);
:53980                  if ((iVar3 < 80000) && (-1 < psVar5[2])) {
:53981                    psVar5[4] = psVar5[4] + (&DAT_0047c1f8)[sVar7 * 0x148];
:53982                    psVar5[3] = psVar5[3] + (&DAT_0047c1f6)[sVar7 * 0x148];
:53983                    while (0 < (short)(&DAT_0047c200)[sVar7 * 0x148]) {
:53984                      FUN_0044acb4(sVar7,sVar8,0);
:53985                    }
:53986                    bVar1 = true;
:53987                  }
:53988                }
:53989              }
:53990            }
:53991            sVar8 = sVar8 + 1;
:53992            psVar5 = psVar5 + 0x148;
:53993            sVar6 = sVar6 + -1;
:53994          } while (sVar6 != 0);
:53995        }
:53996      }
:53997    }
:53998    return;
:53999  }
```

### `FUN_00450b30`, the fleet merge

```text
:54002  // ==== FUN_00450b30 @ 00450b30 ====
:54003
:54004  void FUN_00450b30(void)
:54005
:54006  {
:54007    bool bVar1;
:54008    short sVar2;
:54009    int iVar3;
:54010    short *psVar4;
:54011    short sVar5;
:54012    short sVar6;
:54013    short sVar7;
:54014
:54015    bVar1 = false;
:54016    for (sVar6 = 0; (!bVar1 && (sVar6 < DAT_004a0326)); sVar6 = sVar6 + 1) {
:54017      iVar3 = (int)sVar6;
:54018      if (((&DAT_0049c274)[iVar3 * 0xd] == DAT_004a0320) &&
:54019         (((((short)(&DAT_0049c27e)[iVar3 * 0xd] < 0x28 && ((&DAT_0049c282)[iVar3 * 0xd] == -1)) &&
:54020           ((&DAT_0049c276)[iVar3 * 0xd] == -1)) && (-1 < (short)(DAT_004a0326 + -1))))) {
:54021        sVar7 = 0;
:54022        psVar4 = &DAT_0049c274;
:54023        sVar5 = DAT_004a0326;
:54024        do {
:54025          if (((!bVar1) && (sVar6 != sVar7)) && (*psVar4 == DAT_004a0320)) {
:54026            sVar2 = FUN_00449018(*(undefined4 *)((int)&DAT_0049c26c + sVar6 * 0x1a),
:54027                                 *(undefined4 *)(psVar4 + -4));
:54028            if (((sVar2 < 0x22) && ((int)(short)(&DAT_0049c27e)[sVar6 * 0xd] + (int)psVar4[5] < 100))
:54029               && ((psVar4[7] == -1 && (psVar4[1] == -1)))) {
:54030              iVar3 = (int)sVar6;
:54031              (&DAT_0049c27e)[iVar3 * 0xd] = (&DAT_0049c27e)[iVar3 * 0xd] + psVar4[5];
:54032              (&DAT_0049c27c)[iVar3 * 0xd] = (&DAT_0049c27c)[iVar3 * 0xd] + psVar4[4];
:54033              (&DAT_0049c27a)[iVar3 * 0xd] = (&DAT_0049c27a)[iVar3 * 0xd] + psVar4[3];
:54034              FUN_0044a878(sVar6);
:54035              FUN_0044ad38(sVar7);
:54036              bVar1 = true;
:54037            }
:54038          }
:54039          sVar7 = sVar7 + 1;
:54040          psVar4 = psVar4 + 0xd;
:54041          sVar5 = sVar5 + -1;
:54042        } while (sVar5 != 0);
:54043      }
:54044    }
:54045    return;
:54046  }
```

### Army helpers

`FUN_0044a698` (troop total), `FUN_0044a66c` (slot extent):

```text
:49042  // ==== FUN_0044a698 @ 0044a698 ====
:49043
:49044  int FUN_0044a698(short param_1)
:49045
:49046  {
:49047    int iVar1;
:49048    undefined4 *puVar2;
:49049    int iVar3;
:49050
:49051    iVar3 = 0;
:49052    iVar1 = 0x14;
:49053    puVar2 = &DAT_0047c1ec;
:49054    do {
:49055      iVar3 = iVar3 + *(short *)(puVar2 + param_1 * 0xa4 + 5);
:49056      puVar2 = puVar2 + 8;
:49057      iVar1 = iVar1 + -1;
:49058    } while (iVar1 != 0);
:49059    if (iVar3 == 0) {
:49060      iVar3 = 1;
:49061    }
:49062    return iVar3;
:49063  }
```

```text
:49019  // ==== FUN_0044a66c @ 0044a66c ====
:49020
:49021  int FUN_0044a66c(short param_1)
:49022
:49023  {
:49024    int iVar1;
:49025    undefined4 *puVar2;
:49026    int iVar3;
:49027
:49028    iVar3 = -1;
:49029    iVar1 = 0;
:49030    puVar2 = &DAT_0047c1ec;
:49031    do {
:49032      if (0 < *(short *)(puVar2 + param_1 * 0xa4 + 5)) {
:49033        iVar3 = iVar1;
:49034      }
:49035      iVar1 = iVar1 + 1;
:49036      puVar2 = puVar2 + 8;
:49037    } while ((short)iVar1 != 0x14);
:49038    return iVar3 + 1;
:49039  }
```

`FUN_0044acb4` (move one slot, moves rule), `FUN_0044ac3c` (close the gap, delete if empty):

```text
:49464  // ==== FUN_0044acb4 @ 0044acb4 ====
:49465
:49466  void FUN_0044acb4(short param_1,short param_2,short param_3)
:49467
:49468  {
:49469    int iVar1;
:49470    int iVar2;
:49471    undefined4 *puVar3;
:49472    undefined4 *puVar4;
:49473    byte bVar5;
:49474
:49475    bVar5 = 0;
:49476    iVar1 = FUN_0044a66c(param_2);
:49477    puVar3 = (undefined4 *)(&DAT_0047c1fc + param_1 * 0x148 + param_3 * 0x10);
:49478    puVar4 = (undefined4 *)(&DAT_0047c1fc + param_2 * 0x148 + (short)iVar1 * 0x10);
:49479    for (iVar2 = 8; iVar2 != 0; iVar2 = iVar2 + -1) {
:49480      *puVar4 = *puVar3;
:49481      puVar3 = puVar3 + (uint)bVar5 * -2 + 1;
:49482      puVar4 = puVar4 + (uint)bVar5 * -2 + 1;
:49483    }
:49484    if ((&DAT_0047c1f2)[param_1 * 0x148] == 0) {
:49485      (&DAT_0047c1f2)[param_2 * 0x148] = 0;
:49486    }
:49487    FUN_0044ac3c(param_1,param_3);
:49488    FUN_0044a80c(param_2);
:49489    return;
:49490  }
```

```text
:49430  // ==== FUN_0044ac3c @ 0044ac3c ====
:49431
:49432  void FUN_0044ac3c(short param_1,short param_2)
:49433
:49434  {
:49435    int iVar1;
:49436    int iVar2;
:49437    int iVar3;
:49438    undefined4 *puVar4;
:49439    undefined4 *puVar5;
:49440    byte bVar6;
:49441
:49442    bVar6 = 0;
:49443    iVar1 = FUN_0044a66c(param_1);
:49444    iVar2 = (int)(short)((short)iVar1 + -1);
:49445    iVar1 = (int)param_1;
:49446    puVar4 = (undefined4 *)(&DAT_0047c1fc + iVar1 * 0x148 + iVar2 * 0x10);
:49447    puVar5 = (undefined4 *)(&DAT_0047c1fc + iVar1 * 0x148 + param_2 * 0x10);
:49448    for (iVar3 = 8; iVar3 != 0; iVar3 = iVar3 + -1) {
:49449      *puVar5 = *puVar4;
:49450      puVar4 = puVar4 + (uint)bVar6 * -2 + 1;
:49451      puVar5 = puVar5 + (uint)bVar6 * -2 + 1;
:49452    }
:49453    (&DAT_0047c200)[iVar1 * 0x148 + iVar2 * 0x10] = 0;
:49454    if ((&DAT_0047c200)[iVar1 * 0x148] == 0) {
:49455      FUN_0044ab90(param_1);
:49456    }
:49457    else {
:49458      FUN_0044a80c(param_1);
:49459    }
:49460    return;
:49461  }
```

`FUN_0044a80c` (army marker band), `FUN_0044ab90` (army tombstone):

```text
:49141  // ==== FUN_0044a80c @ 0044a80c ====
:49142
:49143  void FUN_0044a80c(short param_1)
:49144
:49145  {
:49146    int iVar1;
:49147    int iVar2;
:49148    ushort uVar3;
:49149    short sVar4;
:49150
:49151    iVar1 = FUN_0044a698(param_1);
:49152    iVar2 = (int)param_1;
:49153    uVar3 = (ushort)(iVar1 / 1000);
:49154    if (uVar3 < 0x19) {
:49155      sVar4 = (&DAT_0047c1f0)[iVar2 * 0x148] + 200;
:49156    }
:49157    else if ((ushort)(uVar3 - 0x19) < 0x19) {
:49158      sVar4 = (&DAT_0047c1f0)[iVar2 * 0x148] + 0xd8;
:49159    }
:49160    else {
:49161      sVar4 = (&DAT_0047c1f0)[iVar2 * 0x148] + 0xe8;
:49162    }
:49163    if (-1 < (short)(&DAT_0047c1f4)[iVar2 * 0x148]) {
:49164      *(short *)(&DAT_0045e870 +
:49165                *(short *)((int)&DAT_0047c1ec + iVar2 * 0x290 + 2) * 2 +
:49166                *(short *)(&DAT_0047c1ec + iVar2 * 0xa4) * 0x118) = sVar4;
:49167    }
:49168    return;
:49169  }
```

```text
:49372  // ==== FUN_0044ab90 @ 0044ab90 ====
:49373
:49374  void FUN_0044ab90(short param_1)
:49375
:49376  {
:49377    int iVar1;
:49378    int iVar2;
:49379
:49380    iVar1 = (int)param_1;
:49381    if ((short)(&DAT_0047c1f4)[iVar1 * 0x148] < 0) {
:49382      iVar2 = FUN_00449970((&DAT_0047c1ec)[iVar1 * 0xa4]);
:49383      (&DAT_0049c282)[(short)iVar2 * 0xd] = 0xffff;
:49384    }
:49385    else {
:49386      *(undefined2 *)
:49387       (&DAT_0045e870 +
:49388       *(short *)((int)&DAT_0047c1ec + iVar1 * 0x290 + 2) * 2 +
:49389       *(short *)(&DAT_0047c1ec + iVar1 * 0xa4) * 0x118) = (&DAT_0047c1f4)[iVar1 * 0x148];
:49390    }
:49391    (&DAT_0047c1f0)[iVar1 * 0x148] = 0xffff;
:49392    return;
:49393  }
```

### Fleet helpers

`FUN_0044a878` (fleet marker band), `FUN_0044ad38` (fleet tombstone):

```text
:49172  // ==== FUN_0044a878 @ 0044a878 ====
:49173
:49174  void FUN_0044a878(short param_1)
:49175
:49176  {
:49177    int iVar1;
:49178    short sVar2;
:49179
:49180    iVar1 = (int)param_1;
:49181    if ((ushort)(&DAT_0049c27e)[iVar1 * 0xd] < 0x19) {
:49182      sVar2 = (&DAT_0049c274)[iVar1 * 0xd] + 300;
:49183    }
:49184    else if ((ushort)((&DAT_0049c27e)[iVar1 * 0xd] - 0x19) < 0x19) {
:49185      sVar2 = (&DAT_0049c274)[iVar1 * 0xd] + 0x13c;
:49186    }
:49187    else {
:49188      sVar2 = (&DAT_0049c274)[iVar1 * 0xd] + 0x14c;
:49189    }
:49190    *(short *)(&DAT_0045e870 +
:49191              *(short *)((int)&DAT_0049c26c + iVar1 * 0x1a + 2) * 2 +
:49192              *(short *)((int)&DAT_0049c26c + iVar1 * 0x1a) * 0x118) = sVar2;
:49193    return;
:49194  }
```

```text
:49493  // ==== FUN_0044ad38 @ 0044ad38 ====
:49494
:49495  void FUN_0044ad38(short param_1)
:49496
:49497  {
:49498    int iVar1;
:49499
:49500    iVar1 = (int)param_1;
:49501    if ((&DAT_0049c276)[iVar1 * 0xd] == -1) {
:49502      *(undefined2 *)
:49503       (&DAT_0045e870 +
:49504       *(short *)((int)&DAT_0049c26c + iVar1 * 0x1a + 2) * 2 +
:49505       *(short *)((int)&DAT_0049c26c + iVar1 * 0x1a) * 0x118) = 0;
:49506    }
:49507    if (-1 < (short)(&DAT_0049c282)[iVar1 * 0xd]) {
:49508      FUN_0044ab90((&DAT_0049c282)[iVar1 * 0xd]);
:49509    }
:49510    (&DAT_0049c274)[iVar1 * 0xd] = 0xffff;
:49511    return;
:49512  }
```

### Distance

```text
:47727  // ==== FUN_00449018 @ 00449018 ====
:47728
:47729  void FUN_00449018(undefined4 param_1,undefined4 param_2)
:47730
:47731  {
:47732    uint uVar1;
:47733    uint uVar2;
:47734    undefined2 local_8;
:47735    undefined2 uStack_6;
:47736    undefined2 local_4;
:47737    undefined2 uStack_2;
:47738
:47739    uStack_6 = (short)((uint)param_1 >> 0x10);
:47740    uStack_2 = (short)((uint)param_2 >> 0x10);
:47741    uVar1 = (int)uStack_6 - (int)uStack_2 >> 0x1f;
:47742    local_8 = (short)param_1;
:47743    local_4 = (short)param_2;
:47744    uVar2 = (int)local_8 - (int)local_4 >> 0x1f;
:47745    FUN_00448fd8(((int)local_8 - (int)local_4 ^ uVar2) - uVar2,
:47746                 ((int)uStack_6 - (int)uStack_2 ^ uVar1) - uVar1);
:47747    return;
:47748  }
```

```text
:47671  // ==== FUN_00448fd8 @ 00448fd8 ====
:47672
:47673  undefined4 FUN_00448fd8(undefined4 param_1,undefined4 param_2)
:47674
:47675  {
:47676    if ((short)param_1 <= (short)param_2) {
:47677      param_1 = param_2;
:47678    }
:47679    return param_1;
:47680  }
```

`FUN_004492a0` and `FUN_00449dd8` (not used by the merges):

```text
:47907  // ==== FUN_004492a0 @ 004492a0 ====
:47908
:47909  bool FUN_004492a0(undefined4 param_1,undefined4 param_2)
:47910
:47911  {
:47912    short sVar1;
:47913
:47914    sVar1 = FUN_00449018(param_1,param_2);
:47915    return sVar1 == 1;
:47916  }
```

```text
:48627  // ==== FUN_00449dd8 @ 00449dd8 ====
:48628
:48629  void FUN_00449dd8(short param_1,short *param_2)
:48630
:48631  {
:48632    bool bVar1;
:48633    short *psVar2;
:48634    short sVar3;
:48635    short sVar4;
:48636
:48637    *param_2 = -1;
:48638    if (-1 < (short)(DAT_004a0326 + -1)) {
:48639      sVar4 = 0;
:48640      psVar2 = &DAT_0049c274;
:48641      sVar3 = DAT_004a0326;
:48642      do {
:48643        if (((sVar4 != param_1) && ((&DAT_0049c274)[param_1 * 0xd] == *psVar2)) && (psVar2[1] == -1))
:48644        {
:48645          bVar1 = FUN_004492a0(*(undefined4 *)((int)&DAT_0049c26c + param_1 * 0x1a),
:48646                               *(undefined4 *)(psVar2 + -4));
:48647          if (bVar1) {
:48648            *param_2 = sVar4;
:48649          }
:48650        }
:48651        sVar4 = sVar4 + 1;
:48652        psVar2 = psVar2 + 0xd;
:48653        sVar3 = sVar3 + -1;
:48654      } while (sVar3 != 0);
:48655    }
:48656    return;
:48657  }
```

### Callers and compaction

The week test and tail of `FUN_0044ffbc`, `FUN_0044fa20`, `FUN_00451fdc`:

```text
:53548    if (DAT_004a0330 != 0xb) goto LAB_004501d6;
```

```text
:53570  LAB_004501d6:
:53571    FUN_00450768();
:53572    FUN_00450858();
:53573    FUN_004509f0();
:53574    FUN_00450b30();
:53575    return;
:53576  }
:53577
```

```text
:53208  // ==== FUN_0044fa20 @ 0044fa20 ====
:53209
:53210  void FUN_0044fa20(void)
:53211
:53212  {
:53213    uint uVar1;
:53214
:53215    if (0 < (short)(&DAT_00474ab0)[DAT_004a0320 * 0x24a]) {
:53216      TPremierForm_SetTurnTitle(DAT_004a0bd0);
:53217      FUN_0044fb7c();
:53218      FUN_0044ffbc();
:53219      FUN_0044f31c();
:53220      FUN_0044f608();
:53221    }
:53222    if (DAT_004a0b7c == '\0') {
:53223      uVar1 = (int)DAT_004a0322 + 1U & 0x8000000f;
:53224      if ((int)uVar1 < 0) {
:53225        uVar1 = (uVar1 - 1 | 0xfffffff0) + 1;
:53226      }
:53227      DAT_004a0322 = (short)uVar1;
:53228      DAT_004a0320 = *(short *)(&DAT_0049efe8 + DAT_004a0322 * 2);
```

```text
:54939  // ==== FUN_00451fdc @ 00451fdc ====
:54940
:54941  void FUN_00451fdc(void)
:54942
:54943  {
:54944    char cVar1;
:54945
:54946    FUN_0044adb0();
:54947    while ((DAT_004a0b7c == '\0' && ((&DAT_00474b00)[DAT_004a0320 * 0x494] == '\0'))) {
:54948      cVar1 = FUN_00449050();
:54949      if (cVar1 == '\0') break;
:54950      FUN_0044adb0();
:54951      FUN_0044fa20();
:54952    }
:54953    if ((&DAT_00474b00)[DAT_004a0320 * 0x494] != '\0') {
:54954      FUN_00452034();
:54955    }
:54956    return;
:54957  }
```

`FUN_0044adb0`, `FUN_0044abe0`, `FUN_0044ad7c`:

```text
:49537  // ==== FUN_0044adb0 @ 0044adb0 ====
:49538
:49539  void FUN_0044adb0(void)
:49540
:49541  {
:49542    short *psVar1;
:49543    short sVar2;
:49544
:49545    sVar2 = DAT_004a0324 + -1;
:49546    if (-1 < sVar2) {
:49547      psVar1 = &DAT_0047c1f0 + sVar2 * 0x148;
:49548      do {
:49549        if (*psVar1 == -1) {
:49550          FUN_0044abe0(sVar2);
:49551        }
:49552        sVar2 = sVar2 + -1;
:49553        psVar1 = psVar1 + -0x148;
:49554      } while (sVar2 != -1);
:49555    }
:49556    sVar2 = DAT_004a0326 + -1;
:49557    if (-1 < sVar2) {
:49558      psVar1 = &DAT_0049c274 + sVar2 * 0xd;
:49559      do {
:49560        if (*psVar1 == -1) {
:49561          FUN_0044ad7c(sVar2);
:49562        }
:49563        sVar2 = sVar2 + -1;
:49564        psVar1 = psVar1 + -0xd;
:49565      } while (sVar2 != -1);
:49566    }
:49567    return;
:49568  }
```

```text
:49396  // ==== FUN_0044abe0 @ 0044abe0 ====
:49397
:49398  void FUN_0044abe0(short param_1)
:49399
:49400  {
:49401    short sVar1;
:49402    int iVar2;
:49403    short *psVar3;
:49404    undefined4 *puVar4;
:49405    undefined4 *puVar5;
:49406
:49407    if (-1 < (short)(DAT_004a0326 + -1)) {
:49408      psVar3 = &DAT_0049c282;
:49409      sVar1 = DAT_004a0326;
:49410      do {
:49411        if ((int)*psVar3 == DAT_004a0324 + -1) {
:49412          *psVar3 = param_1;
:49413        }
:49414        psVar3 = psVar3 + 0xd;
:49415        sVar1 = sVar1 + -1;
:49416      } while (sVar1 != 0);
:49417    }
:49418    puVar4 = (undefined4 *)(&DAT_0047bf5c + DAT_004a0324 * 0x290);
:49419    puVar5 = &DAT_0047c1ec + param_1 * 0xa4;
:49420    for (iVar2 = 0xa4; iVar2 != 0; iVar2 = iVar2 + -1) {
:49421      *puVar5 = *puVar4;
:49422      puVar4 = puVar4 + 1;
:49423      puVar5 = puVar5 + 1;
:49424    }
:49425    DAT_004a0324 = DAT_004a0324 + -1;
:49426    return;
:49427  }
```

```text
:49515  // ==== FUN_0044ad7c @ 0044ad7c ====
:49516
:49517  void FUN_0044ad7c(short param_1)
:49518
:49519  {
:49520    int iVar1;
:49521    undefined4 *puVar2;
:49522    undefined4 *puVar3;
:49523
:49524    puVar2 = (undefined4 *)((int)&DAT_0049c252 + DAT_004a0326 * 0x1a);
:49525    puVar3 = (undefined4 *)((int)&DAT_0049c26c + param_1 * 0x1a);
:49526    for (iVar1 = 6; iVar1 != 0; iVar1 = iVar1 + -1) {
:49527      *puVar3 = *puVar2;
:49528      puVar2 = puVar2 + 1;
:49529      puVar3 = puVar3 + 1;
:49530    }
:49531    *(undefined2 *)puVar3 = *(undefined2 *)puVar2;
:49532    DAT_004a0326 = DAT_004a0326 + -1;
:49533    return;
:49534  }
```

## Not established
- **Whether a donor with slot-0 troops <= 0 and another occupied slot can exist.** A12 shows what the function does with one. `FUN_0044ac3c` closes the gap and deletes an army whose slot 0 empties, but that alone does not prove a global invariant for every writer of the unit slots, and no save was checked. Reachability is not established.
- **Observation in play.** `2026-10-07-ai-mover-contact.md` records identical-stat Media armies vanishing one record per turn with no news line, which agrees with A9, A11 and C2. No before/after save pair has been compared with the fields above, and the fleet merge's direction (outer survives) has not been seen in a save.
- **The range of `+0xA`.** 24 at order and `-1` once launched come from the layout report; the intermediate countdown values were not re-read here. The merges test only `== -1`.
- **Fleet `+4` and `+6`** stay unidentified; neither merge reads them.

## Reproduction

```bash
D=/mnt/c/Users/diego/AppData/Local/ReTools/all_app_functions.txt
sed -n '53949,53999p' $D     # FUN_004509f0
sed -n '54002,54046p' $D     # FUN_00450b30
sed -n '49042,49063p;49019,49039p;47727,47748p;47671,47680p' $D   # FUN_0044a698, FUN_0044a66c, FUN_00449018, FUN_00448fd8
sed -n '49464,49490p;49430,49461p;49141,49169p;49372,49393p' $D   # FUN_0044acb4, FUN_0044ac3c, FUN_0044a80c, FUN_0044ab90
sed -n '49172,49194p;49493,49512p' $D                             # FUN_0044a878, FUN_0044ad38
sed -n '47907,47916p;48627,48657p' $D                             # FUN_004492a0, FUN_00449dd8
sed -n '53548p;53570,53577p;53208,53228p;54939,54957p' $D         # callers
sed -n '49537,49568p;49396,49427p;49515,49534p' $D                # compaction
grep -n 'FUN_004509f0\|FUN_00450b30\|FUN_0044ffbc\|FUN_0044fa20' $D   # call sites
```
