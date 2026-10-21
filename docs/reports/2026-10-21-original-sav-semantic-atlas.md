# Original SAV semantic atlas: whole-file field ledger, INERT nation bytes and native checks

**Provenance:** promoted, provisional `[confirmed, partial]` from
[`diegoami/ic2-conquest`](https://github.com/diegoami/ic2-conquest) `main` at
`29cc3a8` (PRs #108, #110, #111, #112), draft
[`findings/2026-10-21-original-sav-semantic-atlas.md`](https://github.com/diegoami/ic2-conquest/blob/29cc3a8/findings/2026-10-21-original-sav-semantic-atlas.md)
(blob `217de9d6`), increments 1–4 of
[conquest #107](https://github.com/diegoami/ic2-conquest/issues/107). The authoritative ledger
is [`field-map-v4.csv`](https://github.com/diegoami/ic2-conquest/blob/29cc3a8/runs/experiments/data/run-exp-sav-atlas107/field-map-v4.csv)
(SHA-256 `52ba0fd7…936e`). Research intake by the research session (2026-10-21): every receipt
rerun from the restored private bundle, the twelve native-run saves retrieved and diffed, and an
independent instruction-level adversarial check of the INERT claim. No upstream review was run
on increments 3–4, and none is claimed here. This session launched no game.

## Answer

- **Ledger.** 113 rows over 14 record types tile every record exactly. 79 are CONFIRMED,
  31 CONTEXTUAL and 3 INERT, with none PARTIAL or UNKNOWN. Every row has start value, writers,
  readers, evidence and uncertainty columns. Every one of the 111 leaf fields has a writer in the
  machine-code index. **This is physical identification, not semantic completion:** the 31
  CONTEXTUAL rows still need per-writer domains, sentinels and cross-record invariants. The
  value-policy column is unchanged from v1.
- **The 31 UNKNOWN nation bytes (+0x450..0x46A, +0x46D, +0x491..0x493) are INERT** in the
  pinned original EXE (`9d753d5d…ba31`), within the scope below. The only instructions that
  touch them are the SAV loader's and saver's whole-table stream transfers. Nothing in the DAT
  holds them, NewGame does not set them, and they are BSS zero at program start. File > New does
  not clear them, so they carry whatever the last loaded SAV in that process held. +0x46D and
  +0x491..0x493 are the natural-alignment holes of the Delphi record. +0x450..0x46A are the
  first 27 bytes of the settings sub-record, whose base the code forms but only dereferences at
  +0x1B and beyond.
- **Scope of INERT.** Static: one EXE profile, a linear-sweep and indexed instruction search,
  with the heuristics stated below. Dynamic: one 16-seat round from one start, seed 12345, under
  **Wine 9**, not native Windows. The round ran on the seed build (`354d8265…532f`); only Save
  As (T3) ran on the original EXE. The result is no observed reader. It does not prove that no
  code path in any state reads these bytes.
- **Other moves.** Trailer +0x32/+0x34 are the main form's ClientHeight/ClientWidth
  (CONFIRMED). Fleet +4/+6 is the AI fleet waypoint (CONTEXTUAL). Battle header +4 is the side
  to move (CONFIRMED). The start-of-game baselines wealth0, treasury0 and cities0 are copied by
  the DAT loader. `0x4A031C` is the information panel's line index.

## Method

Upstream evidence lives in
[run-exp-sav-atlas107](https://github.com/diegoami/ic2-conquest/blob/29cc3a8/runs/experiments/data/run-exp-sav-atlas107/README.md)
and [run-exp-sav-inert107](https://github.com/diegoami/ic2-conquest/blob/29cc3a8/runs/experiments/data/run-exp-sav-inert107/README.md).
This intake reran or checked it as follows, against the private bundle
`ic2-research-inputs-20261021` (archive and 128/128 internal checksums verified). Pins: EXE
`9d753d5d…ba31`, DAT `94d0ccfc…5fbd`, `all_app_functions.txt` `2018c205…87d8`.

1. **Offline tests.** `tests.test_sav_atlas_{coverage,access,asm,init}` all pass, and so do the
   repo's `test_reviewer_prompt`, `test_environment` and `test_archive_pycache`.
2. **Receipts, rerun to scratch** (Python 3.13, capstone 5.0.6, pefile 2024.8.26):

   | Receipt | Rerun result |
   |---|---|
   | `corpus-public-v1`, `corpus-private-bundle-v1` | identical |
   | `corpus-*-v3` | identical except the cited ledger: the script now defaults to v4 (`52ba0fd7…`). Every count is unchanged under v4 |
   | `access-summary-v1`, `access-refs-v1` | identical |
   | `access-index-v1.csv` | identical content. The committed file has CRLF line ends; the current script writes LF |
   | `asm-summary-v2`, `asm-index-v2`, `asm-refs-v2` | identical (3,414 hits; 111/111 leaf fields with a writer) |
   | `asm-dispscan-v1` | identical (5 operands in +0x450..0x46A, all `lea`; 0 in +0x46D and +0x491..0x493) |
   | `init-provenance-{private-bundle,public}-v1` | identical |

3. **Serializer and ledger.** The save order was read in the pinned serializer source
   (`FUN_004484D0`). Season follows year; the geometry words are form[9]/[10] and then the two
   VMT+0x2C GetClientRect helpers. The selected army and fleet are reset to −1, and the battle
   header is serialized in the order 0x4A0B74/76/78/7D/7A. The ClientHeight/ClientWidth
   assignment agrees with [2026-10-06-cosmetic-gaps](2026-10-06-cosmetic-gaps.md), which
   confirms the same helper pair in a played save for the secondary windows. The turn-order rule
   agrees with [2026-10-03-new-game-turn-order-shuffle](2026-10-03-new-game-turn-order-shuffle.md).
   The `0x4A031C` reading agrees with [news-log-format-and-messages](news-log-format-and-messages.md).
   Between ledger v1 and v4, eight rows change class and none change offsets:
   - fleet +4/+6: PARTIAL → CONTEXTUAL;
   - trailer +0x32/+0x34 and battle +4: PARTIAL → CONFIRMED;
   - the 3 nation ranges: UNKNOWN → INERT.

   Between v3 and v4 only the evidence and uncertainty cells of five rows change.
4. **Adversarial INERT check, independent of the upstream scripts.**
   [`scripts/unknown31-adversarial-check.py`](../../scripts/unknown31-adversarial-check.py)
   produced the receipt [`research47-unknown31-adversarial-v1.json`](../data/research47-unknown31-adversarial-v1.json).
   It linearly sweeps all executable code (131,970 instructions; a superset of a recursive
   traversal) and looks for what a displacement-in-field scan can miss:
   - **wide or overlapping accesses** that start outside a range and overlap it: **0**;
   - **absolute anchors** in the ranges: **3**. These are the known `lea [idx*4+0x474AC0]` at
     `0x445B61`, `0x445D96` and `0x4462C4`, whose consumers are viewport +0x486/+0x488
     ([bound tax report](2026-10-18-sav-export-bound-tax-subset-and-binary-alias-evidence.md));
   - **block-local reach:** a register given any nation address and dereferenced within 48
     instructions into the ranges: **0**;
   - **record-sized bulk operations:** the 35 `0x494` immediates are all loop-stride `add`s.
     The two `0x4940` immediates are the serializer's TStream read and write. Of the 29
     application `rep movs/stos`, two follow a nation write: both copy 0xA4 dwords, which is an
     army record, after writing nation mobilization +0x442;
   - **over-approximate reach** (window 400, register redefinitions ignored): **11
     candidates**, all false positives on reading the instructions. Nine are Delphi AnsiString
     length reads `[eax-4]` after `eax` was redefined. In the other two, `ebx` was reseeded
     from +0x490 to +0x440 (`0x44FE96`) before the word compare.

   **Positive control:** with the target set to the live human byte +0x490, the same code finds
   52 overlapping operands, matching the upstream displacement scan's 52, and 6 reaches. By hand
   I also read the two base-relative `lea +0x450` sites (`0x448B4F` NewGame, `0x4574A1`). Their
   dereferences are +0x1B, +0x1C, +0x1E..0x45 and +0x36..0x3F, which is nation +0x46B..0x48F.
   None fall in the ranges.
5. **Native saves.** The 12 saves were copied read-only from
   `gdrive:IC2/artifacts/run-exp-sav-inert107/`. All 12 match `SAVES.sha256.v2`. They were
   framed and diffed independently of the upstream `analyse.py`; see Observations.

## Observations

- **T1, INERT** (public start `run0-start-AUTO0720-seed12345.SAV`, `050bc354…574c`):
  - The marked input differs from the start save in exactly 496 bytes, all in the 31 ranges of
    the 16 nations, all nonzero.
  - Plain and marked Save As each change the same 2 bytes outside the ranges: nation 0 +0x482
    (information-window height) and +0x488 (viewport x). Both are UI state. The upstream README
    gives these as file offsets `0x1B2F6`/`0x1B2FC`; this report names their fields.
  - Plain and marked autosaves after the full round differ in exactly the 496 marker bytes, and
    in nothing else.
  - The File > New autosave of the marked process is byte-identical to the marked input. So
    File > New neither cleared the markers nor changed anything else from that start.
- **T3:** the original EXE's Save As of the marked input is byte-identical to the seed build's
  (`3f38a391…`).
- **T2, fleet waypoint** (public `fleet-split-antium-0734.SAV`, `20f38b88…`):
  - The plain Save As reproduces the input byte for byte.
  - The sentinel input differs only in route_y of fleets 0–4 (10 bytes).
  - After the round, plain and sentinel autosaves still differ only in those 10 bytes.
  - Split fleet 5's route went from (0;0) to (−1;0): x was reset by the round tick, and y was
    kept.
  - No AI army set a waypoint in this round.

## Inferences and scope

- The static result (no overlapping, anchoring or reaching access in the original EXE) and the
  dynamic result (a full Wine round with 496 marked bytes produced no other change) support
  INERT for the declared profile. Pointer flows across function boundaries and through memory,
  the 812 indirect edges of the earlier traversal, and untraversed states (battles, elimination,
  diplomacy outcomes not reached in one round) remain outside both checks.
- **Value policy is not changed by this report.** INERT means "no reader found". It does not
  make a canonical value safe for byte identity. A file begun by New Game in a fresh process
  holds zero there, but File > New after loading a SAV keeps that SAV's bytes. An exporter that
  wants byte identity with an original lineage must still carry the source bytes. The ledger's
  `UNKNOWN_REJECT_CHANGED_STATE` policy column is unchanged upstream as well.
- Fleet route_y is meaningful only while route_x ≥ 0. A new fleet record keeps its slot's old
  route bytes until the next round tick.

## Corrections and cross-links

Upstream corrections of its own earlier increments:
- `FUN_0044DBA8` passes the route as `param_3`, which is written, not read.
- Two v1 decompile writer pairs were false positives: `TAreaMap.ToggleMap` and `0x43CF3C`.

The x86 traversal behind the [bound tax report](2026-10-18-sav-export-bound-tax-subset-and-binary-alias-evidence.md)
ran on the seed build (`354d8265…`). This intake's check repeats its three +0x450 anchors on the
original EXE. The [live-regions report](2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md)
and the [unknown-access report](2026-10-18-sav-export-unknown-access-and-record-lineage-boundaries.md)
are superseded on the classification of the 31 bytes (UNKNOWN → INERT, with this scope) but not
on new-record residue, slot lineage or historical-profile rejection.

## What this does not establish

- Semantic completion for the CONTEXTUAL rows: domains, sentinels and cross-record invariants.
- Native Windows behaviour. Every dynamic check here is Wine, and only T3 ran on the original
  EXE.
- An AI-set waypoint observed natively.
- New-record minimal images (army 96/656, fleet 10/26 written), inactive-slot and text-tail
  policy, or historical-profile applicability. These are the remaining parts of research #47.
- Independent review of increments 3–4 or of this intake's checker.
