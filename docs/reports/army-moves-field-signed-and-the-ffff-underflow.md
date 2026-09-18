# `ArmyRecord +6` is a signed count, `0xFFFF` is −1 from an unfloored decrement, and the weekly moves formula is `10 − min(5, troops/20000)`

One army record in this project's save corpus reads `0xFFFF` in the `moves` field (`ArmyRecord +6`):

```text
Army 9 at (192, 96) · owner code 3 (Ptolemaic) · Summer 270, week 7
2 units (1st Dragoons Battalion, heavy cavalry, 900; 1st Guards Battalion, heavy infantry, 5,000)
5,900 troops · 59 tons supply (100%) · 500 money · moves 65535 · morale 59 · covered map cell 2
```

`coveredCell` is `2`, not the `0xFFFF` aboard-a-fleet marker, so this is a live on-map army. The question was whether `0xFFFF` is a deliberate sentinel ("created this turn, weekly maximum not yet computed") or something else. It is **something else**: the field is read signed everywhere, nothing in the binary ever writes `−1` to it deliberately, and exactly one of the thirteen instructions that write it has no floor. **`0xFFFF` is `−1` produced by an underflow — a bug in the original.** The "not yet computed" hypothesis is refuted, not merely unconfirmed.

The same pass settles the long-open weekly-moves formula (`army-to-army-transfer-confirmed.md` "Next checks" item 3, `decompiled-army-movement-and-river-cost.md`'s "Whether Moves itself depends on army composition").

---

## 1. The field is read **signed**, without exception `[confirmed]`

Every comparison and every sign-extension in the binary treats `+6` as a signed 16-bit integer. The x86 gives this away unambiguously: signed `JLE`/`JGE`, and `MOVSX` rather than `MOVZX` on every widening read. There is not one `JBE`/`JAE`/`MOVZX` on this field anywhere.

| Site | Instruction | Meaning at `moves = −1` |
| --- | --- | --- |
| `FUN_004466CC` (unit selection) | `004466EF CMP word ptr [EAX*0x8 + 0x47C1F2],0x0` / `004466F8 JLE` | army **cannot be selected or ordered** |
| `FUN_0044D420` (one movement step) | `0044D70E CMP AX,word ptr [EBX + 0x6]` / `0044D712 JLE` | terrain cost is never affordable |
| `FUN_0044DBA8` (strategic move) | `0044DC48 TEST AX,AX` / `0044DC4B JLE`; `0044DC85 CMP word ptr [EBX + 0x6],0x0` / `0044DC8A JLE` | both further-move branches are skipped |
| `FUN_0044F31C` (AI army driver) | `0044F37C CMP word ptr [EBX + 0x6],0x0` / `0044F381 JLE` | army is skipped for the rest of the AI turn |
| `TUnitMap_MoveHumanArmy` | `0 < (short)army[+6]` | no further path segment is attempted |
| `TInformation_ShowArmyDetails` | `0043C3C6 MOVSX EAX,word ptr [EAX + 0x6]` | the panel **sign-extends** before formatting |

A signed read makes `0xFFFF` mean `−1`. It is therefore not a sentinel value the code tests for — nothing anywhere compares `+6` against `−1` or `0xFFFF`. Its only effect is that every guard fails, so **the army is frozen: it cannot be selected, moved, or acted on for the remainder of the turn.** It is repaired by the next weekly tick (§4), so the bug is self-healing within one week.

## 2. Every write to `+6`, and the one that has no floor `[confirmed]`

Two independent sweeps were used, because trusting either alone would be a mistake. First, the whole-application decompiled dump (`all_app_functions.txt`, 1,881 functions, `0x401338`–`0x45C300`) was grepped for the symbol `DAT_0047C1F2`, for every pointer form `*(short *)(x + 6) =`, and for every `ptr[3] =` word-index form. Second, all 71 functions that reference the army table base `0x0047C1EC` were disassembled (`DumpListing.java`) and every instruction writing to offset `+6` of a record was read by hand and its base register identified. (Both sweeps flag the same false positives: `+6` inside a 32-byte *unit slot* is the unit's **quality** code, and several UI/AI structs also have a `+6` field. Those are excluded below.)

The complete set:

| Address | Instruction | Value written | Floored? |
| --- | --- | --- | --- |
| `0x00449F77` (`FUN_00449F08`, create) | `MOV word ptr [EDX + 0x6],0x0` | `0` | n/a |
| `0x00449F91` (`FUN_00449F08`, create) | `MOV word ptr [EDX + 0x6],0x1` | `1` (AI nations only) | n/a |
| `TUnitMap_JoinArmies` | `army[+6] = 0` | `0` | n/a |
| `0x0044AD18` (`FUN_0044ACB4`, unit transfer) | `MOV word ptr [EAX*0x8 + 0x47C1F2],0x0` | `0`, only if the source army's moves is `0` | n/a |
| `0x0044AEF5` (`FUN_0044AEE4`, field battle) | `MOV word ptr [EAX*0x8 + 0x47C1F2],0x0` | `0` | n/a |
| `0x0044B36C` (`FUN_0044B27C`, siege) | `MOV word ptr [EAX*0x8 + 0x47C1F2],0x0` | `0` | n/a |
| `0x0044B80A` (`FUN_0044B79C`, embark) | `MOV word ptr [EBX + 0x6],0x0` | `0` | n/a |
| `0x0044B8C5` (`FUN_0044B840`, disembark) | `MOV word ptr [EBX + 0x6],0x0` | `0` | n/a |
| `0x0044D6A2` (`FUN_0044D420`) | `SUB word ptr [EBX + 0x6],AX` | `−= terrainCost` | **yes** — guarded by `cost <= moves` |
| `0x0044D714` (`FUN_0044D420`) | `MOV word ptr [EBX + 0x6],0x0` | `0` | n/a |
| `0x0044DBF7` (`FUN_0044DBA8`) | `SUB word ptr [EBX + 0x6],0x2` | `−= 2` | **NO** |
| `0x0044DC71` (`FUN_0044DBA8`) | `DEC word ptr [EBX + 0x6]` | `−= 1` | **yes** — `TEST AX,AX` / `JLE` above it |
| `0x00451651` (`FUN_004514EC`, weekly tick) | `MOV word ptr [EBX + 0x6],DX` | `10 − min(5, troops/20000)` | n/a |
| `0x004516D7` (`FUN_004514EC`, weekly tick) | `DEC word ptr [EBX + 0x6]` | `−= 1` when supply < 10 % | n/a (floor 4) |

**Nothing writes `0xFFFF`, `−1`, or any negative constant to this field.** `FUN_00449F08` does contain `MOV word ptr [EBX],0xFFFF` at `0x00449F18`, and that is almost certainly what seeded the "sentinel" reading in the original question — but `EBX` there is the caller's **out-parameter for the new army's index**, pre-set to `−1` so the caller can detect the "table full / invalid position" failure. It is not the record, which does not yet exist at that point. The record's `+6` is written 100 bytes later, at `0x00449F77`/`0x00449F91`.

### The single unfloored decrement

`FUN_0044DBA8` is the strategic move driver (the AI's equivalent of `TUnitMap_MoveHumanArmy`). Its first branch is "this army is aboard a fleet":

```text
0044DBB7  MOVSX EAX,word ptr [EBP + -0x2]        ; army index
0044DBBB  IMUL EAX,EAX,0x52
0044DBBE  LEA EBX,[EAX*0x8 + 0x47C1EC]           ; EBX = &armyRecord   (656-byte stride)
0044DBC5  MOV SI,word ptr [EBX + 0x6]            ; save moves on entry
0044DBC9  CMP word ptr [EBX + 0x8],-0x1          ; coveredCell == -1  →  aboard a fleet
0044DBCE  JNZ 0x0044DC01
0044DBD0  MOV EAX,dword ptr [EBX]
0044DBD2  CALL 0x00449970                        ; find the fleet on this tile
...
0044DBF2  CALL 0x0044CD08                        ; plot the naval route (pure geometry)
0044DBF7  SUB word ptr [EBX + 0x6],0x2           ; <-- no lower bound, no check
0044DBFC  JMP 0x0044DCA6
```

`0x0044CD08` was read in full: it is a pure Bresenham path-plotter that writes the last reachable tile into the fleet record and touches no army field. So `0x0044DBF7` operates on whatever `+6` holds, with no comparison of any kind before it. Compare `0x0044DC71` twelve instructions below, which *is* guarded — the omission at `0x0044DBF7` looks like a plain oversight rather than a decision.

The two entry points that reach `FUN_0044DBA8` from the AI turn both require `moves >= 1` (`FUN_0044EFC8` at the head of `FUN_0044F31C`, and `FUN_0044F31C`'s own loop, both `CMP ...,0x0 / JLE`). So the pre-value at `0x0044DBF7` is at least `1`, and:

- `moves == 2` → `0`
- **`moves == 1` → `−1` = `0xFFFF`** — the observed value.

`−1` is therefore reachable only from a pre-value of exactly `1`, and it **sticks**: once the field is `−1`, `FUN_0044F31C`'s signed guard skips the army for the rest of the turn, so no second decrement follows. (A pre-value of `2` gives `0` and stops there; `0` is indistinguishable from every other zeroing path.) That asymmetry is why `−1` and not `−2`/`−3` is what shows up in a save.

`FUN_0044EBE8` and `FUN_0044E84C` also call `FUN_0044DBA8` without re-checking moves, so more than one decrement per turn is possible in principle; `FUN_0044F31C` gates `FUN_0044EBE8` behind `FUN_0044AAB4(army) == 0` ("this army has not acted yet", §4), which is false after any decrement, so in practice the extra calls do not chain.

## 3. What produces a pre-value of exactly `1` `[derived]`

Only one instruction in the binary writes `1` to this field: `0x00449F91`, in the army-record creator `FUN_00449F08`, and only for an AI nation:

```text
00449F77  MOV word ptr [EDX + 0x6],0x0           ; moves = 0
00449F7D  MOVSX EAX,word ptr [ESP]
00449F81  IMUL EAX,EAX,0x125
00449F87  CMP byte ptr [EAX*0x4 + 0x474B00],0x0  ; nation's human/computer flag
00449F8F  JNZ 0x00449F97
00449F91  MOV word ptr [EDX + 0x6],0x1           ; AI nation → moves = 1
```

This is the instruction-level confirmation of `decompiled-unit-map-orders-and-record-fields.md`'s "moves `0` for a human nation and `1` for an AI one", which the brief asked to re-derive rather than trust — it is correct as written. The flag polarity (`0x00474B00 + nation × 0x494 == 0` ⇒ computer-controlled) is fixed independently by four call sites: `FUN_0045AF00` marks the seat ready-to-end-turn unconditionally when it is `0` (you never block an AI's end turn), `FUN_0044D420` redraws the map square and plays the move sound only when it is non-zero, and `FUN_0044B79C`/`FUN_0044B840` take the automatic over-capacity-trim and automatic-landing-tile branches when it is `0`.

Everything else about the anomalous record agrees with "created during the turn that was saved": morale is exactly `0x3B = 59`, the value `0x00449FB5` writes at creation, and it holds the highest army index in the table.

**What is not established `[open]`:** the exact sequence that left *this particular* record at `moves = −1` **and** `coveredCell = 2`. `0x0044DBF7` fires only when `coveredCell == −1`, and the only function that restores `+8` from `−1` to a real cell is `FUN_0044B840` (disembark), which also writes `army[+6] = 0` at `0x0044B8C5` — so the obvious "it was aboard, it underflowed, it landed" story does not close, because landing would have overwritten the `−1`. Two candidate explanations were identified but neither is proven:

- A record-pointer aliasing hazard. `FUN_0044ABE0` deletes an army by **swap-remove** (it copies the last record over the deleted slot and decrements the count). `FUN_0044DBA8` caches `EBX = &armyRecord` at entry and `FUN_0044F31C` caches both the record pointer and the army count for its whole loop, across calls that can delete an army (a battle via `FUN_0044AEE4`, a siege via `FUN_0044B27C`). After such a deletion, a cached pointer or index addresses a *different* army — one that may be aboard a fleet with `moves == 1` while the loop believes it is working on the army on land. This is a real, demonstrable structural hazard in the code, but no specific execution trace was reconstructed for it.
- A path not found this pass.

Reported as open rather than dressed up: the **mechanism** of `0xFFFF` is settled (§1–§2 are instruction-level and exhaustive), the **provenance of this one record** is not.

## 4. The weekly moves maximum — formula recovered `[confirmed]`

`FUN_004514EC`'s army loop, the global weekly tick (runs once per full round of 16 nations):

```text
00451633  MOV EAX,dword ptr [ESP + 0x4]          ; FUN_0044A698(army) = total troops
00451637  MOV ECX,0x4E20                         ; 20000
0045163D  IDIV ECX
0045163F  MOV EDX,EAX
00451641  MOV AX,0x5
00451645  CALL 0x00448FD0                        ; min(5, troops/20000)
0045164A  MOV DX,0xA
0045164E  SUB DX,AX
00451651  MOV word ptr [EBX + 0x6],DX            ; moves = 10 - min(5, troops/20000)
...                                              ; (supply consumption happens here)
004516A8  MOVSX EAX,word ptr [EBX + 0xA]         ; supplies
004516AC  IMUL EAX,EAX,0x2710                    ; x 10000
004516B3  IDIV dword ptr [ESP + 0x4]             ; / troops        = supply percent
004516BB  CMP word ptr [ESP],0xA
004516C0  JGE 0x004516DB
004516C2  ...                                    ; morale = max(51, morale - 2)
004516D7  DEC word ptr [EBX + 0x6]               ; moves -= 1
```

> **`moves = 10 − min(5, ⌊totalTroops / 20000⌋)`, minus a further `1` when `⌊supplies × 10000 / totalTroops⌋ < 10` (supply below 10 %).**

So the weekly allowance runs **10 down to 5** by army size in five steps of 20,000 troops, with a floor of **4** for a large, starving army. It is recomputed for *every* army in the game each week, unconditionally — including armies aboard a fleet.

Two supporting identifications:

- **`FUN_0044A698` is total troops, not "readiness".** It sums `army.unit[i].troops` over all 20 slots (`puVar2 + param_1*0xA4 + 5`, stepping `+8` dwords = one 32-byte unit slot) and returns `1` if the sum is zero — a divide-by-zero guard for the `IDIV` above. `decompiled-turn-and-calendar-sequencing.md` described it as "a per-army *readiness* value"; it is a troop count, and that is the whole of the army-size dependence.
- **`FUN_0044AAB4` is "has this army acted yet?"** It recomputes the same maximum and returns `fullMoves != army[+6]`:

  ```text
  0044AAD2  CALL 0x00448FD0                       ; min(5, troops/20000)
  0044AAD7  MOV CX,0xA
  0044AADB  SUB CX,AX                             ; CX = full weekly moves
  0044AAE4  MOVSX EAX,word ptr [EDI*0x8 + 0x47C1F6]   ; supplies
  0044AAEC  IMUL ESI                                  ; x troops   (!)
  0044AAF4  IDIV ESI                                  ; / 10000
  0044AAF6  CMP AX,0xA
  0044AAFA  JGE 0x0044AAFD
  0044AAFC  DEC ECX
  0044AAFD  CMP CX,word ptr [EDI*0x8 + 0x47C1F2]
  0044AB05  SETNZ AL
  ```

  Note the low-supply test here is `supplies × troops / 10000 < 10`, whereas the weekly tick uses `supplies × 10000 / troops < 10`. **These are different expressions** — a genuine inconsistency in the original, not a decompiler artifact (`0044AAEC IMUL ESI` then `0044AAF3 CDQ` discards the high half, so it really is a 32-bit `supplies × troops / 10000`). They agree only near 10,000 troops. For a 100,000-troop army on 50 tons the tick applies the penalty and `FUN_0044AAB4` does not, so `FUN_0044AAB4`'s reference value is wrong for that army and the end-turn prompt that depends on it misfires. Flagged, not pursued.

### Checked against the corpus

`10 − min(5, ⌊troops/20000⌋)`, minus 1 for supply < 10 %, evaluated against **627 army records across 54 saves**:

| Outcome | Records |
| ---: | --- |
| `moves == 0` (acted, or zeroed by join/battle/siege/embark/unaffordable step) | 248 |
| `0 < moves == computed weekly maximum` (untouched since the tick) | 312 |
| `0 < moves < computed maximum` (partially spent) | 61 |
| `moves > computed maximum` | **2** |
| `moves < 0` | **4** (all four are the one anomalous state; `11.sav`, `11_ptol.sav`, `11_supply.sav` and `1_rome_270_summer_7.sav` are the same save) |

625 of 627 satisfy `0 ≤ moves ≤ maximum`. The two exceptions are the same record in `12_mac.sav` and `12_rom_a.sav`: the Roman army at `(100, 42)` with 63,173 troops and `moves = 8`, where the formula gives 7. That army held **48,173** troops at the previous tick (`11_supply.sav`) — 8 is exactly right for 48,173 — and grew by 15,000 through a mid-week city transfer. **The maximum is computed once a week and is not re-derived when an army's composition changes**, so an army that grows mid-week keeps the larger allowance until the next tick. That is `army-to-army-transfer-confirmed.md`'s "Next checks" item 3 answered: there is no recomputation after a composition change.

Three worked examples, all exact:

| Save | Army | Troops | Supply | Formula | Stored |
| --- | --- | ---: | ---: | ---: | ---: |
| `11_supply.sav` | Rome @ (100,42) | 48,173 | 100 % | `10 − 2 = 8` | 8 |
| `1_rome_270_summer_7.sav` | Carthage @ (41,63) | 43,791 | 95 % | `10 − 2 = 8` | 8 |
| `decompiled-unit-map-orders-and-record-fields.md` | Army 0 @ (90,28) | 99,882 | 0 % | `10 − 4 − 1 = 5` | 5 |

The anomalous army's 5,900 troops at 100 % supply would give **10**. It reads `−1`.

**Still open on movement:** unit-type composition plays no part — only the troop total does. Whether a *fleet's* moves and an army's interact beyond the flat `−2` per naval order was not pursued.

## 5. What the original displays for such an army `[confirmed]`

`TInformation_ShowArmyDetails` (`0x0043C33C`) builds the army panel's "Moves" line:

```text
0043C3C2  MOV EAX,dword ptr [ESP + 0x18]         ; &armyRecord
0043C3C6  MOVSX EAX,word ptr [EAX + 0x6]         ; sign-extend moves to int
0043C3CA  CALL 0x004028C4                        ; int -> decimal string
...
0043C3DC  MOV EDX,0x43C7E0                       ; "Moves -"
0043C3E1  MOV EAX,0x49F049
0043C3E6  CALL 0x00405B00
```

`MOVSX`, then the signed integer-to-string routine, then appended to the literal `"Moves -"`. There is no clamp and no special case. **The panel would read `Moves --1`** — the label's own trailing hyphen followed by the minus sign. That settles the player-visible semantics: the original does not treat the value as unsigned or as a sentinel, it prints the negative number.

One qualifier: the decompiled form shows the number is appended only when the army belongs to the viewing nation —

```c
FUN_00405B00(&DAT_0049F049,"Moves -");
if ((&DAT_0047C1F0)[iVar5 * 0x148] == DAT_004A0320) {
    FUN_00405BC8(&DAT_0049F049,(char *)local_134);
}
```

— so for this Ptolemaic army inspected by the Roman player the line reads just `Moves -`, with nothing after it. `Moves --1` is what its *owner* would see. Since the owner is an AI, in practice no player ever saw it.

## Implications for the rebuild

- `+6` must be a **signed** 16-bit field in `IC2.Data`, not unsigned. Decoding it as `ushort` is what turns a `−1` into `65535`; the inspector currently prints `Moves 65535`.
- Do not implement a `0xFFFF` sentinel for "moves not yet computed". There is no such state: every army-creation path writes a concrete `0` or `1`, and the weekly tick overwrites all of them.
- The weekly allowance is `10 − min(5, troops/20000)`, `−1` below 10 % supply, **computed once per week and not refreshed when the army changes size**. That last clause is a real rule, not an artifact — reproducing it is what makes a mid-week reinforcement keep its old allowance.
- A faithful port should *not* reproduce the `0x0044DBF7` underflow. Floor the naval-order cost at 0.

## Reproduction

```text
# every write to the moves field, from the whole-application decompiled dump
grep -n "DAT_0047c1f2" all_app_functions.txt
grep -nE "\+ 6\) =|\[3\] = " all_app_functions.txt

# instruction-level confirmation (project dir is ghidra_projects, project name IC2)
set JAVA_HOME=%LOCALAPPDATA%\ReTools\jdk-21.0.12.1+1
analyzeHeadless.bat %LOCALAPPDATA%\ReTools\ghidra_projects IC2 ^
  -process "Imperial Conquest 2.exe" -noanalysis ^
  -scriptPath %LOCALAPPDATA%\ReTools\scripts ^
  -postScript DumpListing.java out.txt 00449f08 0044dba8 0044aab4 004514ec 0043c33c
```

The corpus check parses each save's army table directly (count at `0x18A5C`, 656-byte records from `0x18A5E`, troops at unit slot `+4`).

## Next checks

1. The provenance of the one `−1` record (§3). The record-pointer aliasing hazard around `FUN_0044ABE0`'s swap-remove is worth a dedicated pass on its own merits — it would affect more than this field.
2. `FUN_0044AAB4`'s `supplies × troops / 10000` vs the tick's `supplies × 10000 / troops`. Which one the end-turn prompt and the AI actually want, and whether a large starving army is therefore never warned about.
3. Fleet `+4`/`+6`, listed as unidentified in `decompiled-unit-map-orders-and-record-fields.md`, are written by `FUN_0044CD08` as the last reachable tile of a plotted naval route (`0xFFFF` when none) — a scratch waypoint, not persistent state. Worth confirming against a save pair before labelling.
