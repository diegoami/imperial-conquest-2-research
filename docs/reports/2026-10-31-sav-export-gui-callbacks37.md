# SAV export #37, Q2: the tax and rename refreshes write only the current nation's viewport, plus a map-click re-run

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `7346f48` (PR #283). It
answers Q2 of research issue [#37](https://github.com/diegoami/imperial-conquest-2-research/issues/37)
(remake #1191), delegated on 2026-10-31: the GUI callbacks still marked UNVERIFIED in
[`2026-10-18-sav-export-bound-tax-subset-and-binary-alias-evidence.md`](2026-10-18-sav-export-bound-tax-subset-and-binary-alias-evidence.md).
- **Code:** `runs/experiments/savexport37/closure.py`, a static call closure over direct calls, filtered
  to the blocks the saver `FUN_004484d0` streams. `runs/experiments/savexport37/selectunit.py` is a
  Unicorn control on the #187 RAM snapshot.
- **Data:** `runs/experiments/data/run-exp-savexport37/` (`closure-*.json`, `selectunit-v1/v2.json`).
  No save was written, and no game was run. The snapshot and the decompile stay private.

**Tags:**
- `[code]` for the call paths and the saved-state writes;
- `[confirmed: emulation]` for the map-click re-run.

**Review note (2026-10-31):**
- **Reruns from a scratch copy,** with outputs redirected:
  - all three closures (`refreshforms`, `refreshforms-full`, `updateumselection`) are **identical**
    to the committed JSON;
  - `selectunit-v2.json` is **identical**;
  - `selectunit-v1.json` differs only by fields that the later script adds (`real_order_routines`,
    `enemy_square_code`, `own_moves`). Every result is identical.
- **Disassembly:**
  - `TChangeTax_OK` stores the tax word at `0x4540CF` (`[nation*0x494 + 0x474ABA]`, +0x44A), then
    calls `TPremierForm_RefreshForms` (`0x4540DC` → `0x45BA6C`) and the close helper `0x42313C`.
  - `RefreshForms` calls `TUnitMap_PaintForm` (`0x445D38`) first.
  - `PaintForm` sets `edi` to the current nation's +0x450 (`0x445D96`) and has exactly four stores,
    to `[edi+0x36]` and `[edi+0x38]` (+0x486 and +0x488), at `0x445DAD`, `0x445DCB`, `0x445DDF` and
    `0x445DFD`.
  - `PaintForm` ends with `cmp word [form+0x21A], -1` and `call 0x4466CC` (`TUnitMap_SelectUnit`)
    at `0x446078–0x44608E`.
- **Not checked:** the rename-dialog internals beyond the draft's decompile reading, and the 28
  functions that make indirect calls (the draft states this limit too).

## Answer

**Both callbacks end in the same `TUnitMap_PaintForm`:**
- **Tax:** `TChangeTax_OK` (`0x4540B8`) → `TPremierForm_RefreshForms` (`0x45BA6C`), which runs
  `PaintForm`, then `TInformation_ShowNationStatus`. That writes only the panel line `0x4A031C`, which is
  not saved.
- **Rename:** `TUnitMap_ChangeUnitDetails` (`0x447644`) opens the units dialog.
  - Its commit is `TChangeArmyUnits_OK` (`0x445378`), which writes mobilization +0x442 and copies the
    whole 656-byte army.
  - `TUnitMap_UpdateUMSelection` (`0x446EF4`) then shows the details for the highlighted square and
    runs `PaintForm` and `TInformation_PrintInfo`.
  - A rename is allowed for exactly one selected regular unit.

**Beyond the commits, the only saved writes are the current nation's viewport +0x486/+0x488.**
`PaintForm` reads them from the scroll bars and clamps them to the map size, so they depend on the
window's geometry, not on game state. The static closures cover 145 functions (tax) and 154
(rename), with `TUnitMap_SelectUnit` handled separately.

**The map-click re-run** `[confirmed: emulation]`: `PaintForm` re-runs `TUnitMap_SelectUnit` on
the highlighted square (form +0x21A).
- **Branches that can't repeat:** every state-changing branch (the attack on an army, the attack on a
  city, embarking) resets the selected army to −1. A re-run then only re-selects.
- **The exception is the enemy-fleet branch,** which keeps the selected fleet. On the snapshot, with
  the real naval battle and relation setter:

  | Case | Click | Refresh re-run |
  |---|---|---|
  | at war | naval battle; the attacker's moves go to 0; the loser is deleted | nothing |
  | at peace, answer No | "Are you sure you want to attack this fleet ?" | **the same question again** |
  | at peace, answer Yes | war set, naval battle | nothing |

  So a refresh writes saved state beyond the viewport only if the player answered No to an
  attack-fleet question and then answers Yes when it is asked again.

**For the exporter**, a tax-only or rename-only edit serializes as:
- **tax:** +0x44A;
- **rename:** the army record plus +0x442;
- **both:** the current nation's +0x486/+0x488, clamped by the window size.

## What this does not establish

- **The 28 functions with indirect calls** (VCL virtual methods and event pointers), and any message
  pumping inside the modal dialogs.
- **What is selected and highlighted when a dialog opens:** that is the player's doing, and it was
  not observed in a live GUI.
- Native Windows behaviour.
