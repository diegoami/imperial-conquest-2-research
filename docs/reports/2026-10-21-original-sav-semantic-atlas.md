# Original SAV semantic atlas: whole-file field ledger, INERT nation bytes and native checks

**Provenance:** promoted, provisional `[confirmed, partial]` from
[`diegoami/ic2-conquest`](https://github.com/diegoami/ic2-conquest) `main` at
`29cc3a8` (PRs #108, #110, #111, #112), draft
[`findings/2026-10-21-original-sav-semantic-atlas.md`](https://github.com/diegoami/ic2-conquest/blob/29cc3a8/findings/2026-10-21-original-sav-semantic-atlas.md)
(blob `217de9d6`), increments 1–4 of
[conquest #107](https://github.com/diegoami/ic2-conquest/issues/107). The authoritative ledger
is [`field-map-v4.csv`](https://github.com/diegoami/ic2-conquest/blob/29cc3a8/runs/experiments/data/run-exp-sav-atlas107/field-map-v4.csv)
(SHA-256 `52ba0fd7…936e`). Increments 5–11 (conquest `ad0af2d` through `b3cf8dc`; ledgers v5–v11) have their own sections below. Research intake by the research session (2026-10-21): every receipt
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

## Increment 5: new-record residue, deleted slots, text tails and history

**Provenance:** conquest `main` `ad0af2d` (PR #115). The ledger is
[`field-map-v5.csv`](https://github.com/diegoami/ic2-conquest/blob/ad0af2d/runs/experiments/data/run-exp-sav-atlas107/field-map-v5.csv).
It is static only, and no review was run upstream. **Intake (2026-10-22):**
- The four atlas test suites pass at `ad0af2d`.
- Ledger v4 → v5 changes no class or offset, only notes, evidence and value policies:
  - route_x/route_y become `LIVE_AND_RESIDUE`;
  - the 3 INERT rows become `PRESERVE_OR_ZERO`;
  - `CITY.allegiance` becomes `HISTORICAL_PROFILE`.
- Each claim below was re-read in the pinned decompilation or the original EXE, and the corpus
  counts were recomputed independently.

| Claim | Intake check | Result |
|---|---|---|
| The army constructor `FUN_00449F08` writes 96/656 bytes | read | **holds**: the 16-byte header, then type and troops (= 0) in each of the 20 slots |
| Troops never go negative | read `FUN_0044AE20` and every caller | **holds**. The subtraction is `(troops div (Random(15)+105)) × p`, with p as follows:<br>• battle (`FUN_0044AEE4`): 40 × smaller div larger, so < 40<br>• siege (`FUN_0044B27C`): clamped 1..15<br>• naval/storm (`FUN_0044B4F8`): r²/100 with r ≤ 100; the storm calls it only when the loss is ≥ 6, so r = 10000/(≥106) |
| An empty slot's label, quality and name have no effect | spot-checked `TInformation.ShowArmyDetails` | **holds** there: type, label and quality are read for every slot, but each term is multiplied by `troops div 200` = 0. The other readers' guards were not re-read one by one |
| Corpus: 6,102 live and 9,498 empty slots; none negative; no live slot after an empty one | recount over the same 56 saves | **holds when tombstones are excluded.** Two owner −1 army records, in one owner-retained group, still hold 8 slots with troops > 0 each. With them included the counts are 6,118/9,522. Upstream did not state that exclusion; it now states both counts (conquest `80a3963`) |
| Launch `FUN_0044A050` does not write fleet moves; a fleet launched in a tick keeps its old moves until the next tick | read the launch; disassembled the round tick `FUN_004514EC` | **holds.** The tick decrements countdown by 2. At 0 it calls the launch and jumps to the next fleet (`0x451758`). The moves refresh (`0x4518FC`) runs only for already launched fleets |
| All 120 fleets under construction hold 0 in the leftover words | recount | **holds**. army = −1 and route_x = −1 are written by the order and the tick; x, y, route_y, moves, supplies, money and cell are 0 |
| wealth0, treasury0, cities0 and conqueror are presentation only | `asm-index-v2` reader sets | **holds**. Readers: the saver, `THumanFalls.InitializeForm` and, for conqueror only, `TInformation.ShowNationStatus` |
| `CITY.allegiance` drives gameplay | read `FUN_0044A98C`, `FUN_0044B27C`, `FUN_0044BB18`, `FUN_0044BED8`, `FUN_0044C204` | **holds**:<br>• defence × 4/5 when the owner is not the allegiance nation<br>• × 9/10 in a siege by the allegiance nation<br>• capture by the allegiance nation sets loyalty to min(90, 140 − L)<br>• the rebellion compares owner and allegiance<br>These agree with E14/E21 of the [feature inventory](2026-10-05-player-facing-feature-inventory.md) and with [decompiled-quarterly-rebellion](decompiled-quarterly-rebellion.md). That report already gives the full rebellion rule that increment 5 lists as open |
| Text tails after the NUL are never interpreted | not re-derived | upstream static claim. It is consistent with the StrCopy semantics in the [unknown-access report](2026-10-18-sav-export-unknown-access-and-record-lineage-boundaries.md) |

Consequences:
- **Byte identity.** Residue and text tails still matter, which is why the unknown-access
  report's lineage rejection stands.
- **Semantic export.** An army slot with troops 0 may hold any label, quality or name. A fleet
  index reused after compaction carries its previous moves into the first turn after launch.
  This candidate effect is not observed in a game; checking it needs an owner-authorized run.
- **Fresh campaigns** must supply `CITY.allegiance`. The four nation history fields affect only
  presentation.

## Increment 6: fleet leftovers observed in a game

**Provenance:** conquest `main` `22b450d` (PR #117). The ledger is
[`field-map-v6.csv`](https://github.com/diegoami/ic2-conquest/blob/22b450d/runs/experiments/data/run-exp-sav-atlas107/field-map-v6.csv)
(`d7ff9f9b…91bf1`). The run is
[run-exp-sav-fleetmoves107](https://github.com/diegoami/ic2-conquest/blob/22b450d/runs/experiments/data/run-exp-sav-fleetmoves107/README.md),
owner-approved upstream, on the seed build, seed 12345, under Wine. **Intake (2026-10-22):**
- The four atlas test suites pass.
- Ledger v5 → v6 changes only the evidence and uncertainty cells of eight fleet rows.
- The 7 saves were copied read-only from `gdrive:IC2/artifacts/run-exp-sav-fleetmoves107/`
  and match `SAVES.sha256`. Their fleet tables were decoded independently.

Observations:
- **T4, natural path** (start `fleet-split-antium-0734.SAV`):
  - **Scuttle:** after scuttling fleet 2 and End turn, the count is 5, and slot 2 holds the old
    fleet 5, ticked (moves 31, condition 96).
  - **Build:** a Build fleet order then creates index 5 with owner, countdown 24, ships 10, build
    city 89 and army −1. It keeps the pre-tick copy's x,y (101,47) and route (0;0), and those are
    saved. Moves, supplies, money and cell were also kept, but the copy held 0 in each.
  - **Next tick:** route_x becomes −1, and x,y stay (101,47) while the fleet is building.

  The past-count copy itself is not in any save (it is beyond the count). Its pre-tick values
  come from upstream memory dumps, which were not re-read here.
- **T5, direct:** a building fleet (countdown 2) holds a crafted moves 17, and its control holds
  0. After End turn both fleets have launched at (219,55) with supplies 50 and condition 100.
  The sentinel keeps **moves 17** in the autosave. The two autosaves differ in exactly that one
  byte.
- **Not exercised:** spending leftover moves on the launch turn.

This confirms in Wine what increment 5 predicted. Launch does not set moves, so a fleet keeps
its index's leftover moves, x,y, route and other unwritten words until the next round tick. A
reused index can therefore carry a moved fleet's pre-tick values.

## Increment 7: cross-record invariants

**Provenance:** conquest `main` `b4f17a4` (PR #120). The checker is
[`scripts/sav_atlas_invariants.py`](https://github.com/diegoami/ic2-conquest/blob/e8c8e5d/scripts/sav_atlas_invariants.py),
with receipts `invariants-{private-bundle,public}-v1.json` (counts, indices and observed domains
only). The ledger is `field-map-v7.csv`. **Intake (2026-10-22, at `1642f6d`):**
- The five atlas test suites pass.
- Both receipts reproduce exactly, except for the ledger they cite (v8 is now the default).
- Ledgers v6 → v8 change no class, offset or value policy, only the notes, evidence and
  uncertainty of 13 rows.

The main invariants were recomputed independently over the same 56 saves:

| Invariant | Independent result |
|---|---|
| City marker: `(m − 20) mod 16 = owner`, with 20 ≤ m < 100 | 18,704/18,704 |
| Each nation's city list (+0x48, −1-terminated) is exactly the set of its owned cities | 896/896 |
| **The list is ordered by city name** | 896/896 in name order. Only the 25 empty lists (dead nations) are also in index order |
| A live nation's count (+0x446) equals its list length, and its capital is owned | 871/871 and 871/871 |
| A dead nation keeps a stale count | 25/25 |

**Code check of the order:** `FUN_0044B8F4` removes the city from its old owner's list. It then
inserts it into the new owner's list before the first entry with
`StrComp(new name, entry name) < 0`, i.e. in byte-wise name order. The helper writes neither the
owner nor the counts; its callers do.

Not recomputed here, and upstream's results only:
- fleet markers;
- army marker bands, which lag in 17 of 362 natural private-bundle armies;
- fleet countdown parity;
- merc placement.

The v1 fort-encoding line was void; see Increments 9–10.

Untestable on this corpus: aboard links (no army is aboard in any save) and the battle-grid
icon count (the only battle saves are the crafted research40 cases).

## Increment 8: the rebellion and revival rule

**Provenance:** conquest `main` `e8c8e5d` (PR #121), ledger `field-map-v8.csv`
(`277b4636…e920`). Static only. It restates
[decompiled-quarterly-rebellion](decompiled-quarterly-rebellion.md), which research already
holds in more detail. The trigger and branch order agree: quarterly, non-capital, loyalty < 30.
- **Owner = allegiance:** an at-war army within Chebyshev distance < 10; otherwise the
  best-scoring living neighbour (cities − 2 × distance to its capital).
- **Owner ≠ allegiance:** the city returns to its allegiance nation, or the revival is
  attempted when that nation is dead. The revival needs more than 7 allegiant cities with
  loyalty < 40.

**Corrections to increment 8** (re-read in `FUN_0044C360`):
- **Relations:** "at peace with everyone" overstates it. Only the revived nation's **own**
  16-entry relation row (+0x26) is zeroed; other nations' entries toward it are left alone.
  Then `FUN_00449B40(reborn, old owner, −8)` writes a symmetric −8 cooldown for each moved
  city.
- **Recruitment:** "recruit entries emptied" means that only the troops word of each of the
  40 entries is zeroed; state, type and city stay.

The research report's other details are not in increment 8:
- wealth is not reset;
- the leader draw has no "differs" retry;
- moved cities get loyalty 90;
- a former capital is favoured by × 5/3.

The reset values (unity 450, treasury 0, tax base 0, cities 0, tax 20, mobilisation 50,
conqueror −1) and the capital bonuses (loyalty and fort +8/+10 capped at 99, pop +10, max pop
+20, tribute +25, marker owner + 84) agree. The revival is not observed natively.

## Increments 9–10: natural aboard and battle-grid checks, and a second-look review

**Provenance:** conquest `main` `de952d1` (PRs #123, #124; #125 is notes only), ledger
`field-map-v10.csv` (`bb4dba7e…8cb2`). Increment 10 is a review of increments 3–8 by a second
agent of the same model family. It is a second look, **not an independent review**.
**Intake (2026-10-22, at `a4e2293`):**
- The five atlas test suites pass.
- Ledgers v8 → v10 change no class, offset or value policy, only notes, evidence and one writer
  list.
- All four v2 invariants receipts reproduce exactly, except for the ledger they cite: private
  bundle, public saves, battle releases and aboard run.
  - For the battle-release receipt, the 23 `run-exp-battle-probe` saves were downloaded from
    the public release and match `invariants-battle-releases-v1.sha256`.
  - For the aboard receipt, the 2 `run-exp-sav-aboard107` saves were copied read-only from
    `gdrive:IC2/artifacts/run-exp-sav-aboard107/` and match `SAVES.sha256`.

Observations:
- **Battle grid** (increment 9): one icon per live battle slot holds in 6/6 Save-As-in-battle
  saves and 15/15 half-round saves. The crafted research40 cases are the only failures.
- **Aboard links, natural embark** (Wine, seed build). Decoded independently:
  - army 0 has cell −1 at fleet 2's tile (101,46), and fleet 2's cargo is army 0, same owner;
  - the tile's marker is 316, i.e. owner 0 + 316 (30 ships);
  - moves are 0/0 after the embark and 9/25 after the tick.

  The research `run-exp-naval-battle-cargo` saves also pass, but they are synthetic edits and
  carry no weight as game evidence.

Increment 10 corrections, re-read here:
- **Fort-encoding invariant.** The v1 test was vacuous and read the population word, so any v1
  fort-encoding count is void. The v2 check (fort ≥ 0, pending + current ≤ 100) has
  0 violations on all four corpora. This report never relied on the v1 line.
- **Revival relations.** The same correction this intake already made from `FUN_0044C360`
  (Increment 8 section).
- **Route residue.** `FUN_0044CD08` initialises only the low word of its last-tile local
  (`0xFFFF`) and stores the whole dword. So a walk that ends at once writes route x = −1 with
  stack residue in y; the round tick is not the only x = −1 writer.
- **Two more allegiance effects** are already in research and agree with the code:
  - the defection cascade `FUN_0044BA1C` divides a city's defence by 3 when its allegiance is
    the new owner ([decompiled-defection-and-siege-attrition](decompiled-defection-and-siege-attrition.md));
  - on elimination (`FUN_0044C528`) a city whose allegiance is the winner gets loyalty
    min(80, 120 − L), otherwise min(70, max(40, 100 − L)), then + Random(6)
    ([decompiled-elimination-cleanup](decompiled-elimination-cleanup.md)).
- **Neighbours writer.** `FUN_0044B8F4` was credited as a `NATION.neighbours` writer only by a
  lead-index artefact (its terminator write reaches +0x46 when the count is 0). No research
  report relied on it.

## Increment 11: rebellion and revival observed in a game

**Provenance:** conquest `main` `b3cf8dc` (PR #126), ledger `field-map-v11.csv`
(`f5de0e7e…13b4`). The run is
[run-exp-sav-rebellion107](https://github.com/diegoami/ic2-conquest/blob/b3cf8dc/runs/experiments/data/run-exp-sav-rebellion107/README.md),
owner-approved upstream, on the seed build, seed 12345, under Wine, with one End turn (one
quarterly loop). **Intake (2026-10-22):**
- Ledger v10 → v11 changes only the notes, evidence and uncertainty of two rows.
- The 4 saves were copied read-only from `gdrive:IC2/artifacts/run-exp-sav-rebellion107/` and
  match `SAVES.sha256`.
- The input equals research's natural `1_rome_270_winter_11.sav` (`76b09ee3…`). The same file
  is in the `imp_conquest_fixtures` release `run-1-rome` and the conquest release
  `run-exp-battle-probe`.
- Everything below was decoded independently.

| Check | Observed |
|---|---|
| Crafted input vs natural save | 11 bytes differ: the loyalty words of 11 cities. The 8 Galatian-allegiance cities → 20, Agrigentum → 5, Ebora → 5, Carthago → 5 |
| Galatia, dead before the revival | unity 0, capital −1, **stale count 5**, conqueror 2 |
| Galatia after | unity 480, capital 218 (Ancyra), count 8, conqueror −1, tax 20, new leader, all 8 allegiance cities owned |
| Moved cities' loyalty after | 90 (one shows 89), capital 98 = 90 + 8 |
| Capital map marker | 96 = Galatia 12 + 84 |
| Relations toward Galatia | Before: Seleucid −18, Media −8. After: Seleucid ↔ Galatia −7 (the −8 cooldown after one thaw), Media −8 kept, and trades (1) with Numidia, Gaul and Armenia made during the round. **Not peace with everyone** |
| Agrigentum (owner Carthage, allegiance Greece) | goes to Greece |
| Ebora (owner = allegiance = Celtiberia) | Celtiberia's only war is with Carthage, and no Carthaginian army is within Chebyshev 10, so the neighbour rule applies: Gaul −83, Carthage −124 → Gaul |
| Control: Carthago, a capital at loyalty 5 | stays Carthaginian |
| Plain control run | only Messene changes owner, as part of the round |

This independently **reproduces** earlier Wine observations of the
[decompiled quarterly rebellion](decompiled-quarterly-rebellion.md), now on a natural start
save changed only in loyalty. The earlier observations were all on staged saves:
- [g3 §1a–1c](2026-10-12-g3-original-checks.md): rebellion, return and rebirth, including the
  seven-city control in which nothing moves;
- [g4 H](2026-10-12-g4-followups.md): the at-war branch (c), where the highest-index war army
  within distance 10 wins;
- [g4 J](2026-10-12-g4-followups.md): the −8 relation cooldown.

Every branch has therefore been seen in a game, each on a staged state.

Limits:
- This run does not exercise branch (c); g4 H covers it.
- Unity, mobilisation and treasury had already moved on by the autosave, because the rest of
  the loop and the round ran first.
- It is Wine on the seed build.

## What this does not establish

- Semantic completion for the CONTEXTUAL rows: domains, sentinels and cross-record invariants.
- Native Windows behaviour. Every dynamic check here is Wine, and only T3 ran on the original
  EXE.
- An AI-set waypoint observed natively.
- Whether leftover moves can be spent on the launch turn (not exercised in increment 6).
- Independent review of increments 3–10 or of this intake's checker. Increment 10 is a same-model second look.
