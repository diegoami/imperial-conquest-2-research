# The complete SAV file layout, from the actual read/write code

> **Correction (2026-10-17):** The news log is a shift register, and [Save As during a human-controlled battle](2026-10-04-battle-probe.md) produces the conditional tactical block. The [SAV export safety finding](2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md) maps the nation record and record-residue limits; this layout alone does not establish changed-state export readiness. The table below incorporates the later corrections.
>
> **Update (2026-10-04):** the battle block is fully named: flag, attacker, defender, side to move, placed, half-round counter, 40 × 44-byte slots and a 14 × 12 icon-code grid. See [2026-10-04-decompiled-tactical-battle-rules.md](2026-10-04-decompiled-tactical-battle-rules.md) §1.


The single strongest confirmation this project has produced. Tracing forward from `TPremierForm_OpenGameFile`/`SaveGameFile(As)` (found directly in the recovered RTTI symbol list — no string search needed this time) reached `FUN_004487c4` (load) and `FUN_004484d0` (save), a matched pair of functions that read/write the exact same fields in the exact same order via a stream object's `Read`/`Write` virtual methods (vtable slot 0 and slot +4 respectively). This is, byte-count for byte-count, the authoritative SAV file format — not inferred from diffing, but read directly from the code that produces the files.

## The full sequence, in order

| Field | Byte count | Matches |
| --- | ---: | --- |
| Map | 89,600 | `WorldPrefix.MapByteLength` (320×140×2) — exact |
| City table | 11,356 | `334 × 34` (`WorldPrefix.CityCount × CityRecordLength`) — exact |
| Army count | 2 | — |
| Army records × count | 656 each | `SaveArmyTable.RecordLength` — exact |
| Fleet count | 2 | — |
| Fleet records × count | 26 each | `SaveFleetTable.RecordLength` — exact |
| Nation table | 18,752 | `16 × 1,172` (`SaveNationLayout.NationRecordLength`) — exact |
| **Mercenary table** | **50 × 12 bytes, fixed** | **`SaveMercenaryTable`'s 50-slot, 12-byte-record structure — confirmed directly in code**, not just inferred from where plausible data stopped in `mercenary-pool-record.md`. This is no longer a "candidate" finding. |
| A count field, then `(count+1)` records | 61 bytes each | **The news/event log — identified in [decompiled-news-log-identified.md](archive/decompiled-news-log-identified.md).** A 40-slot shift register of news messages; the "count" field is actually the index of the most-recently-used slot, not a record count. |
| Turn order | 32 | 16 signed WORDs |
| Pending offer | 4 | source nation and proposed relation, two WORDs |
| Current nation | 2 | matches `DAT_004a0320`, used throughout this project's decompiled code as "current nation index" |
| Turn-order index, week, year BC, season | 2+2+2+2 | four WORDs |
| Main-window geometry | 8 | four WORDs, UI state |
| **Battle-in-progress flag** | 1 | **Confirmed in code and in [Wine File → Save As battle saves](2026-10-04-battle-probe.md)**; the toolbar Save does nothing in that battle phase. |
| *(conditional, only if battle flag set)* | 2+2+2+1+2+1,760+336 | Tactical battle state — 9 header bytes, 40 × 44-byte slots (`0x6e0` = 1,760 bytes) and a 14 × 12 two-byte grid (`0x150` = 336 bytes); observed in Wine File → Save As battle saves. |

## The 61-byte record type: the news log (resolved)

Immediately after the (now code-confirmed) mercenary table, the save reads a 2-byte value, then that-value-plus-1 records of exactly 61 bytes each. **Identified in a follow-up pass:** this is the game's news/event log, a 40-slot shift register where every capture, defection, and battle-result message this project has decompiled gets appended, and the "count" field is actually the index of the most-recently-used slot (not a record count) — see `decompiled-news-log-identified.md` for the confirming code.

**Reconciliation corrected (2026-09-14):** the measured 3,042-byte interval runs from the nation-table end to the trailer start: `600 + 2 + 40 × 61`. The earlier six-byte mismatch subtracted the 55-byte trailer from this interval again. See [news-log format](news-log-format-and-messages.md) for the full shift-register evidence and pending-offer distinction.

## Why this matters

This single pair of functions independently reconfirms, from the actual serialization code rather than inference, nearly every structural fact this project has built up from save-diffing over many reports: the map size, city table size and stride, the army/fleet/nation table record lengths, and — most importantly — the mercenary table's 50-slot capacity that `mercenary-pool-record.md` had to discover empirically by testing where plausible data stopped. It also reveals the conditional battle-state block. Human-controlled File → Save As has produced that variant under Wine; its 2,105 bytes must be included when the saved battle flag is set. The strategic sequence accounts for saves with the flag clear.

For the provisional original-bound current-human tax transformation and the distinction between serialized byte projections and complete GUI/native validation, see the [tax profile evidence](2026-10-18-sav-export-bound-tax-subset-and-binary-alias-evidence.md). The serializer still consumes all 31 UNKNOWN nation bytes wholesale.

## What this does not establish

- Whether arbitrary changed native state can safely inherit unmapped original record bytes; see the [SAV export safety finding](2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md).
- Native Windows acceptance of a newly exported candidate or equivalence of future RNG behavior.

## Reproduction

Found via the recovered RTTI symbol list directly (`grep -i "open\|save\|load\|game" delphi_symbols.tsv`), then:
```text
analyzeHeadless <project> IC2 -process "Imperial Conquest 2.exe" -noanalysis -scriptPath <scripts>
  -postScript ExportAddresses.java out.txt 0045aad4 0045ab84 0045abb0 004487c4 004484d0
```

## Next checks

The remaining export work is the semantic mapping and Windows three-output gate in the [SAV export safety finding](2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md). The news framing and battle-block reachability questions above are settled by the linked later reports.
