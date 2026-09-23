# Digging into the promotion effect: the morale array identified, a clean promotion rule, and a new open field

Follow-up to `full-battle-resolution-rome-vs-gaul.md`'s open question — why did three surviving units (all "average" quality) get bumped to "good" after the Rome/Gaul battle, including one (4th Bowmen) that took zero troop losses? This traces the runtime battle-unit data structure in the decompiled code to answer it, and along the way pins down the identity of the "unidentified `+0x350` field" flagged as open in `decompiled-combat-formula-structure.md`.

> **Correction (2026-09-23)**, from a targeted pass on [`imperial_conquest_2#288`](https://github.com/diegoami/imperial_conquest_2/issues/288). Four fixes are made in the text below. (1) The `+3` on battle entry is conditional on the army's **own** nation being computer-controlled, not on the opponent's alive/dead status. It writes the strategic morale at `+14`. Confirmed from the `FUN_00437de4` listing and from Gaul's tombstoned record in `1_rome_270_winter_7_b.sav` (62 → 65). (2) The initial-morale clamp is `[60, 90]`: 60 is a floor, not a second upper bound. (3) Rome's `+14` fall 68 → 66 is the end-of-turn supply decay, not a battle effect. (4) The promotion table claimed all 19 units but omitted slot 1 (2nd Guards, good, not adjacent to a casualty, unchanged). With it restored, the survivors number **14**, matching `full-battle-resolution-rome-vs-gaul.md`, not 13. The promotion rule itself stays withdrawn, as the note in that section says.

## The runtime battle-unit struct, mapped field by field

`TBattleMap_StartBattle` calls `FUN_00437de4` the first time a battle is entered. That function copies both armies' units from the **persistent SAV-shaped army table** (`&DAT_0047c1ec + armyIdx×0xa4`, the same 656-byte-per-army / 32-byte-per-unit-slot layout `TArmyToArmy` writes back to — see `army-to-army-transfer-confirmed.md`) into a **flat 20-slot working array per side** (`DAT_004a0344` for side A's 20 slots, `DAT_004a06b4` for side B's, each unit occupying 0x16 = 22 words = 44 bytes). Reading the copy-in code field by field against the known SAV unit-slot layout (type at +2, troops at +4, quality at +6, name at +8) pins down every global Ghidra assigned in the combat functions:

| Runtime array | Word offset in the 44-byte slot | Field |
| --- | --- | --- |
| `DAT_004a0344` / `DAT_004a06b4` | +0 | battle-grid X |
| +2 | +1 | battle-grid Y |
| `DAT_004a0348` | +2 | (copied from SAV slot+0, meaning not yet identified) |
| `DAT_004a034a` | +3 | unit type code |
| `DAT_004a034c` | +4 | **troops** (matches every prior combat report's reading) |
| `DAT_004a034e` | +5 | **quality** (copied directly from the SAV's persisted quality byte) |
| `DAT_004a0350` | +6 | **morale** — see below |
| ... | +9 | `DAT_004a0356`, the assigned-target slot (`0xffff` = none) |
| ... | +10 | `DAT_004a0358`, the unit's name string |

This corrects `decompiled-combat-formula-structure.md`'s notation: the "`+0x350` field" isn't a struct-offset from some base — it's simply the array `DAT_004a0350`, a flat per-slot morale value, distinct from (and copied independently of) the persisted `quality` field. **`DAT_004a0350` is now confirmed as the exact source of the "Morale" line in the per-unit combat info panel** documented in `full-battle-resolution-rome-vs-gaul.md` (`"Morale: normal"`, `"Morale: very low"`), closing that report's open question about the field's identity.

## The morale formula, in full

At battle start (still in `FUN_00437de4`), each unit's initial morale is:

```text
morale = max(60, min(90, Random(quality × 4) + armyMorale[armyIdx]))     // i.e. clamped to [60, 90]
```

`[confirmed]` at instruction level (`0x00438029`–`0x0043804d` for side A, `0x0043813e`–`0x00438162` for side B): the sum is passed as `min(90, ·)` (`FUN_00448fd0`, `EAX = 0x5A`) and the result as `max(60, ·)` (`FUN_00448fd8`, `EAX = 0x3C`). The "upper bounds ≈ 90 then 60" this section first gave was the same two calls misread: 60 is a **floor**, not a second cap.

where `armyMorale` is `DAT_0047c1fa`, read with the same per-army stride as the persistent army table — i.e. it lives at **byte offset +14 within the 16-byte army header**, immediately after `Money` (+12) and before the first unit slot (+16). This pass first called it "army experience"; it is the army's **strategic morale**, displayed as a tier and driven each turn by supply ([supply-driven-morale-and-fleet-attrition.md](supply-driven-morale-and-fleet-attrition.md)). It is a different number from the per-unit tactical morale `DAT_004a0350` that it seeds. `SaveArmyTable.cs`'s `ArmyRecord` treated bytes 14–15 as unused padding; a direct read of both saves in this pair shows a real, changing value there — `68` in `1_rome_270_winter_7.sav`, `66` in `1_rome_270_winter_9.sav`, for Rome's army 0.

**The `+3` on battle entry, and its condition** `[confirmed]`. Before the copy-in, `FUN_00437de4` tests each side's army in turn:

```text
00437e05  CMP byte ptr [0x474670 + owner(armyA)×0x494 + 0x490], 0x0   ; nation's human/computer flag
00437e0d  JNZ 0x00437e87                                              ; human: skip
00437e0f  ADD word ptr [armyA×0x290 + 0x47c1fa], 0x3                  ; strategic morale (+14) += 3
00437e1e  CALL 0x00437d10                                             ; re-sort that army's unit slots
          ...copy nation[+0x48C], nation[+0x48E] from the opponent's nation into this army's nation
00437e9f  CMP / 00437ea7 JNZ / 00437ea9 ADD ... 0x3                   ; the same block for army B
```

- **Condition:** the army's **own** nation is computer-controlled (nation `+0x490 == 0`, the flag whose polarity [army-moves-field-signed-and-the-ffff-underflow.md](army-moves-field-signed-and-the-ffff-underflow.md) fixed). It is not tied to the opponent, and not to anyone's alive/dead status; this paragraph's earlier reading was wrong on both counts.
- **Target:** the **strategic** army morale at army record `+14`, the persistent field. Not the tactical array `DAT_004a0350`, although the array is seeded from `+14` a few instructions later, so the AI's units start 3 points higher too.
- **Amount:** exactly `+3`, with no clamp: an AI army at 70 would go to 73.
- **When:** once per battle. `TBattleMap_StartBattle` calls `FUN_00437de4` only while `DAT_004a0b7c == 0`, and the function sets it to 1 on exit. Because the instant resolver `FUN_0044AEE4` handles every AI-vs-AI fight, a tactical battle always has a human side, so in practice **the computer-controlled side of a tactical battle gets `+3` and the human side gets nothing**. The instant resolver writes no `+14` at all.
- The two nation words copied alongside are the **battle-delay settings**: `TBattleDelays_InitializeForm` reads and writes them, and the shooting (`FUN_0043910c`) and melee (`FUN_004393ec`) functions pass them to the `GetTickCount` wait loop `FUN_00448ffc` (×100 ms). So the AI side also adopts its human opponent's display delays. `[confirmed]`

**Checked against the saves** `[confirmed]`:

| Save pair | Army | Nation | `+14` before | `+14` after | Reading |
| --- | --- | --- | ---: | ---: | --- |
| `1_rome_270_winter_7` → `_7_b` (mid-turn, no tick between) | Rome 0 | human | 68 | **68** | no `+3` |
| same | Gaul 13, tombstoned at `0x1ABAE` | computer | 62 | **65** | **`+3`** |
| `7.sav` → `8.sav` (one tick, supply 80 %) | Rome 0 | human | 70 | **70** | no `+3` (a `+3` would have left 73; regen never lowers it) |
| `1_rome_270_winter_7` → `_9` (one tick, supply 0 %) | Rome 0 | human | 68 | **66** | no `+3`; the tick's `pct < 10` decay, `−2` |

Gaul's tombstoned record in `1_rome_270_winter_7_b.sav` also carries the other half of the branch. Its units still hold their pre-battle troops (the record was not written back), but they are **re-sorted**: `2nd Guards` (heavy infantry, 4,165) moves from slot 4 to slot 0, and `2nd Foot` (light infantry, 5,649) from slot 0 to slot 10. Rome's slots in `_7_b` and `_9` keep their original order, compacted. This is `FUN_00437d10`'s re-sort, which runs only for the AI army. The +14 fall 68 → 66 that this report once found puzzling is therefore not a battle effect at all. Rome's army 0 read `supplyPercent 0` in both `winter_7` and `winter_9`, and the end-of-turn tick took `−2` for it.

During melee (`FUN_004393ec`), `DAT_004a0350` is adjusted by exactly `+2`/`−3` per exchange depending on which side had the better power ratio, clamped to a `[?, 99]` range — this part was already correctly described in `decompiled-combat-formula-structure.md`, just mislabeled as a struct offset.

## The quality-promotion rule: fully explained by one clean pattern

None of the recovered battle-related functions (`TBattleMap_StartBattle`'s copy-in, `TBattleMap_FinishBattle`, `TBattleMap_EndTurn`, `TBattleMap_ComputerGeneral`, `TBattleMap_Surrender`, the melee function, the shooting function) contain an explicit "increment quality" instruction — a thorough read of all of them turned up nothing. But the save data itself gives an unambiguous empirical rule. Tabulating all 19 of Rome's pre-battle units by their original army-slot index, quality, and outcome (slots and qualities read from `1_rome_270_winter_7.sav` / `1_rome_270_winter_9.sav`, army 0):

| Slot | Unit | Quality before | Adjacent slot wiped? | Outcome |
| --- | --- | --- | --- | --- |
| 3, 5, 10, 11, 14 | (5 units) | various | — | **wiped** (0 troops) |
| 6 | 1st Bowmen | average | yes (slot 5) | **promoted → good** |
| 9 | 3rd Foot | average | yes (slot 10) | **promoted → good** |
| 13 | 4th Bowmen | average | yes (slot 14) | **promoted → good** |
| 2, 12 | 3rd Guards, 6th Guards | good | yes (slot 3 / 11) | unchanged |
| 1 | 2nd Guards (heavy infantry, 4,782 → 2,382) | good | **no** (slots 0 and 2 both survived) | unchanged |
| 4 | 4th Guards | elite | yes (slot 3) | unchanged (already max tier) |
| 15 | 1st Guards | very good | yes (slot 14) | unchanged |
| 0, 7, 8, 16, 17, 18 | (6 average-quality units) | average | **no** | unchanged |

The rule that fits all 14 non-wiped units with zero exceptions: **an "average"-quality unit occupying an army slot immediately adjacent to a slot whose unit was destroyed in the same battle is promoted to "good"; units that already started above "average," and "average" units not adjacent to a casualty, are unaffected.** This is not a losses-based or morale-based effect — 4th Bowmen took zero troop losses and had "very low" morale mid-battle, yet was still promoted, while several harder-hit non-adjacent units (3rd Foot's neighbor 3rd Bowmen, 2nd Foot, etc.) were not.

> **Withdrawn.** The very same battle was later replayed from the identical starting save, and the adjacency rule fails on that second sample three separate ways: an "average" unit adjacent to a destroyed slot was *not* promoted, an "average" unit with no adjacent casualty *was*, and a "very good" unit was promoted to "elite". What fits both battles (6 promotions across 30 surviving units, including one above the "average" tier) is the uniform rule the instant resolver already uses in code — `quality = max(quality, 6)` then a 1-in-4 `min(quality + 1, 9)` per surviving unit. The single-battle adjacency pattern was a coincidence. See [battle-replayed-rout-mechanic-and-combat-constants.md](battle-replayed-rout-mechanic-and-combat-constants.md). Everything else in this report — the `DAT_004a0350` morale array, its initialization formula, and the `ArmyRecord`+14 correction — is unaffected.

This reads like a genuine "closing ranks" veterancy mechanic (a survivor next to a fallen comrade's slot gains experience) rather than a bug, but the implementing code wasn't located — it's most likely inside a unit-slot compaction/write-back routine that runs when destroyed units are removed from the army table, which wasn't among the 282 recovered RTTI method names and wasn't reachable by tracing calls from the known battle-lifecycle functions.

## What this does not establish

- The exact code implementing the adjacency-promotion rule — only its precise external behavior, from one battle's worth of data (14 relevant units, 0 exceptions).
- Whether the rule generalizes past "average → good" (e.g., would a "good" unit adjacent to a casualty ever reach "very good"? The one candidate case here, slot 2/12, sits at "good" and didn't change — consistent with a rule that only fires from the "average" tier, or with a rule that fires from any tier but happened not to trigger here for an unrelated reason).
- The meaning of `DAT_004a0348` (the SAV unit-slot+0 field, copied into the runtime struct but never referenced in any decompiled combat function read so far).

## Reproduction

```text
dotnet run --project src/IC2.Inspect -- --to-json saves/1_rome_270_winter_7.sav w7.json
dotnet run --project src/IC2.Inspect -- --to-json saves/1_rome_270_winter_9.sav w9.json
# compare Rome's army-0 units by slot index and quality code between the two files
```
Ghidra: `grep -n "DAT_004a03" all_app_functions.txt` and `grep -n "0047c1ec" all_app_functions.txt` to re-trace the copy-in/runtime-array mapping; `FUN_00437de4 @ 00437de4` is the key function.

## Next checks

1. A second battle with destroyed units (ideally one with a "good"-or-above unit adjacent to a casualty and nothing else confounding) would test whether the promotion rule is "average-only" or applies at every tier.
2. Locate the slot-compaction/write-back routine directly — searching for code that shifts unit slots down (removing gaps left by destroyed units) in the region between `TBattleMap_FinishBattle` and wherever the strategic-map army display next reads the table.
3. ~~Track `ArmyRecord`+14 across a longer save sequence with no battles at all.~~ Done: it drifts every turn with supply ([supply-driven-morale-and-fleet-attrition.md](supply-driven-morale-and-fleet-attrition.md)), and a battle adds `+3` only to a computer-controlled side (§"The morale formula").
