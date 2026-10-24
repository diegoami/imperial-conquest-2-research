# Live army quality 4: very poor, normally mobilizable, preserved by serialization

**Status:** `[confirmed, partial: original source/instructions and bounded original-x86 controls]`.
Research [#63](https://github.com/diegoami/imperial-conquest-2-research/issues/63), for
[build #1352](https://github.com/diegoami/imperial_conquest_2/issues/1352) / T185.
Original research by the active desktop session, not a findings intake or an
independent review. No game, Wine or native Windows process ran. No owner save was
read, patched, converted or published.

## Answer and recommended export policy

**Preserve live-unit quality `4` unchanged. It means `very poor`, on the same scale as
`5` poor through `9` elite.** The original human mobilization action can create it
from recruitment readiness 16–19. The army loader/writer copy its word unchanged;
the army list selects its proper DAT string; tactical battle entry copies it
unchanged and calls `Random(16)` for its initial morale contribution.

The supported live-army quality domain recommended by this research is **4–9**, extending the build reader's former 5–9 restriction by one tier. Do not convert 4 to 5 or 6 or interpret it on
another scale. A battle winner's later quality floor of 6 is a gameplay effect,
not a load/export normalization rule. Main implemented that policy in [PR1353](https://github.com/diegoami/imperial_conquest_2/pull/1353), merged at `ae614899d63ac721ee46d1e3213191fe1f43a676` on 2026-10-23, with focused reader/exporter tests and typed refusal outside 4–9. No build code is changed here.

Distinguish the **raw storage domain** (a 16-bit word copied without validation) from
the **supported gameplay domain**. Raw load/save success for negative values, 0–3
or values above 9 does not establish valid gameplay. Retain typed refusal for such
unsupported live values until applicable evidence supports them. The ten-entry
display table is not itself a live-unit validity specification.

**Native Windows open → inspect → order/End turn → saveNEW → fresh reopen is not tested by this report.** These controls do not clear research #37's native-JSON gate, prove the
owner's entire state exportable, or change the twelve-save run's acceptance status.

## Input identity and representation

All inputs were freshly checked by the runner before execution:

| Input | SHA-256 |
| --- | --- |
| Original EXE | `9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31` |
| Original DAT | `94d0ccfc67148d727de4c4e60aefc3c53ba9e67775bd689f0fcb2e23c12e5fbd` |
| `all_app_functions.txt` | `2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8` |

Each 656-byte army has a 16-byte header and twenty 32-byte slots. Quality is the
**word** at slot `+6`, not a byte. For the classical 334-city SAV, its file offset is
`0x18A5E + armyIndex*656 + 16 + slotIndex*32 + 6`. Its runtime address is
`0x47C202 + armyIndex*656 + slotIndex*32`. Consumers below use signed 16-bit reads
(`MOVSX`); 4–9 has the same representation under signed/unsigned decoding.

## Original paths checked

Line references use the pinned whole-application dump. DAT/SAV stream functions
omitted from that dump were checked in the pinned EXE's disassembly and, where
available, retained `save_load_impl.txt`. Addresses are virtual addresses.

| Path | Exact evidence | Consequence |
| --- | --- | --- |
| Initial DAT load `FUN_004481A0` | `0x448201–0x44822C`: fifteen raw 656-byte army reads; `0x4483E2–0x4483F0`: 110-byte quality table read | Initial qualities copied directly; table loads to `0x47938C` |
| New army `FUN_00449F08` | dump 48713–48749 | Clears twenty troop/type words, not quality words; empty-slot quality can be residue |
| Recruitment order `TArmyRecruits_RecruitUnit` | dump 55972–55980, state initialized to 0, type/troops set separately | Readiness is not yet a live army quality |
| Weekly recruitment training `FUN_004514EC` | `calendar_and_endturn.txt` 245–263: nonnegative readiness becomes `min(24,state+2)` | Fresh ordinary recruit reaches readiness 16 after eight ticks |
| Human mobilization `TArmyRecruits_MobilizeUnits` | dump 56044–56098; compare with 16 at `0x455311`, signed `JL` at `0x45531A` | Readiness 16–19 is eligible |
| Recruit-to-live-unit `FUN_0044A4E0` | dump 48951–48990; `0x44A5D1` signed readiness load, negative correction then `SAR 2`; `0x44A5E3` writes slot `+6` | Truncating `state/4`: 16–19 → 4, 20–23 → 5, 24 → 6 |
| AI mobilization `FUN_004504F4` | dump 53752–53798 | Requires `state == 24`, creating quality 6; separate from the human gate |
| Mercenary restock `FUN_00449130` | dump 47806–47865 | Clamps restocked offer quality to 5–9; not the regular-army lower bound |
| Mercenary hire `TRecruitMercs_RecruitMercUnit` | dump 43658–43669 | Copies offer quality directly to slot `+6` |
| SAV load `FUN_004487C4` | `0x448835–0x448864`: count-controlled raw reads of `0x290` bytes | No per-slot quality rejection, clamp or conversion in this loader |
| SAV save `FUN_004484D0` | `0x448547–0x448577`: corresponding raw writes | Preserves quality, including empty-slot/tombstone residue |
| Open/save wrappers | dump 58057–58132 | Open calls loader then turn/battle setup; Save/Save As call writer. Raw routines do not replace whole-UI acceptance |
| Army list `TInformation_ShowArmyUnits` | dump 41276–41308; `0x43CEB2–0x43CEC5` signed quality load, multiply by 11, string lookup | Direct index 4 selects `very poor`; no remapping |
| Battle copy-in `FUN_00437DE4` | dump 38122–38167, both sides | Copies persisted word to tactical slot `+10`; initial morale uses `Random(quality*4)` |
| Tactical winner `TBattleOver_OK` | dump 57587–57616; `0x4592A7–0x4592D4` | Survivor gets `max(6,q)`, then on `Random(4)==0`, `min(9,q+1)` |
| Instant winner `FUN_0044AEE4` | dump 49655–49714, both winner branches | Same floor/promotion rule; not a serialization rule |

The army part of the weekly tick (dump 54493–54530) changes moves, supply and
strategic morale in the header, not unit quality. Advancing recruitment readiness
does not automatically train existing army units. This checks the identified body,
not every possible whole-program quality write.

## Display and slot classes

The DAT quality strings begin at file offset `0x1F6CA`, ten eleven-byte entries:

| Code | Word | Meaning in this finding |
| --- | --- | --- |
| 0–3 | not ready | Recruitment below human mobilization readiness; not newly approved live qualities |
| 4 | very poor | Normal early human mobilization |
| 5 | poor | Later human mobilization; mercenary minimum |
| 6 | average | Fully trained ordinary mobilization; battle winner floor |
| 7 | good | Existing higher tier |
| 8 | very good | Existing higher tier |
| 9 | elite | Existing upper tier / promotion cap |

The army list stops at the first nonpositive troop word. Empty slots can retain
quality/name bytes; a new army does not initialize every quality word. Tombstoned
armies retain opaque bytes too. Applying live 4–9 validation indiscriminately would
misclassify residue. Canonicalization/tombstone refusal remains governed by the
[gate-2 policy](2026-10-22-sav-export-gate2-policy.md).

The older [roster report](army-records-and-roman-roster.md) observed 5–9 in its sample,
not the complete range. The [mobilization report](decompiled-mobilization-and-mercenary-restock.md)
already describes 4; the [information-window report](2026-10-05-information-window-fields-and-bands.md)
records staged Wine display of 4. Those old captures were not reopened here and
are not new native Windows evidence.

## Fresh bounded execution

[Runner](../../scripts/research63-quality-check.py), Unicorn 2.1.4; complete scalar
[receipt](../data/research63-quality-controls-v1.json). Original PE sections are
mapped without instruction patches. Each run checks its stop point and instruction
limit; full function returns also check stack balance. No SAV file is read or written.

- **Initialization:** complete DAT loader against the pinned DAT through an in-memory
  stream. All fifteen army records and the quality table equal the input regions.
  Complete new-army constructor with synthetic placement: twenty troop/type fields
  clear while twenty seeded quality residue words remain unchanged.
- **Human mobilization:** complete original action with one selected recruitment row
  and an adjacent army. Readiness −1, 0, 15 is refused; 16, 17, 18, 19 produces a
  live 3,500-troop archer of quality 4; 20, 23 produces 5; 24 produces 6. Destination
  selection, capacity/troop checks, queue deletion and marker helpers run original code.
- **Display:** original army-list routine selects exact DAT indices 4, 5, 9 for
  qualities 4, 5, 9 without changing quality. This checks string selection, not pixels.
- **Serialization:** complete writer → fresh loader → writer for synthetic two-army,
  one-fleet streams, strategic and with a battle block. Framing is 121,707 / 123,812
  bytes, 68 / 75 stream transfers. All 1,312 army bytes and complete output streams
  are identical. Raw controls −1, 0, 3, 4, 5, 6, 9, 10, 32,767 copy unchanged;
  out-of-domain values demonstrate copying only. Synthetic records include residue
  and a tombstone and are not valid supported export candidates.
- **Battle entry:** complete copy-in with qualities 4, 5, 9 on each side preserves
  them and uses original RNG bounds 16, 20, 36. Original RNG/min/max/grid-icon helpers
  execute. Both synthetic nation flags are human to omit AI sorting/+3.
- **Winner write-back:** prefix `0x459220–0x4592ED`, stopped before loot/diplomacy/UI.
  Input `[4,5,6,8,9]`, forced roll 0 → `[7,7,7,9,9]`; forced roll 1 → `[6,6,6,8,9]`.
  These force two branches, not a promotion-rate measurement or battle replay.

**Interceptions:** stream constructor/read/write/destructor use in-memory adapters;
filename conversion/release and geometry calls are stubs. Mobilization GUI count/
selection return one selected row; list refresh/painting and national unit naming
are skipped. Constructor placement supplies `(20,20)`. Display string copy uses a
bounded NUL-string adapter; appending/number formatting and panel painting are
skipped while recording the original selected index. Battle name copying uses that
adapter; post-copy turn/UI setup is skipped; winner-prefix RNG is forced as above.
These controls do not execute Delphi stream internals, Windows file I/O, full battle
actions, an End turn or whole-game UI.

Reproduce with existing private inputs and a new output path:

```bash
python3 scripts/research63-quality-check.py \
  --exe "$IC2_EXE" --dat "$IC2_DAT" \
  --dump "$IC2_DECOMPILE/all_app_functions.txt" --out /tmp/quality63-new.json
```

## Remaining acceptance

Quality 4's original-code meaning and supported policy are answered at this scope.
An optional coordinated native check can open a separate private candidate, inspect
`very poor`, issue an order/End turn, saveNEW and fresh-reopen while recording any
intervening battle. It requires owner approval and was not performed here. A winner
promotion must be separated from load/save behavior. Build evaluation is complete as noted above; research #63 stays open for its native coordination. This finding does not clear #37's other gates.

## Verification before merge (2026-10-24)

The active research session reviewed the mobilization gate and readiness conversion, direct display index, battle copy-in and winner floor/promotion against the pinned listing. A fresh run of the unchanged checker with pinned EXE/DAT/listing reproduced the **entire committed JSON receipt exactly**, including the checker digest. Initialization, constructor residue, all ten readiness cases, three display indices, both complete in-memory serialization round trips, battle copy-in and two forced promotion branches pass. These are offline instruction controls with the interceptions listed above; no new game, owner-save access, independent reviewer or native Windows validation is claimed.
