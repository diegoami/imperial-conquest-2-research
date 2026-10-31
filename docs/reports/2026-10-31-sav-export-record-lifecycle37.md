# SAV export #37, Q3: how the original creates, removes and moves army and fleet records

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `5e32e9a` (PR #284). It
answers Q3 of research issue [#37](https://github.com/diegoami/imperial-conquest-2-research/issues/37)
(remake #1191, for T184): the record-ordering, relocation, carrier-link and new-record rules for
writing native state into a SAV when the source JSON has no provenance. It builds on the
[semantic atlas](2026-10-21-original-sav-semantic-atlas.md) (increments 5–7) and the
[live-regions report](2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md).
- **Code:** `runs/experiments/savexport37/lifecycle.py` runs the original routines in Unicorn on the
  #187 RAM snapshot, with every record pre-filled with the canary byte `0xA5`.
- **Data:** `runs/experiments/data/run-exp-savexport37/lifecycle-v1.json`. No save was written, and
  no game was run. The snapshot and the decompile stay private.

**Tags:**
- `[code]` for the path table and the compaction timing;
- `[confirmed: emulation]` for the prototypes and the compaction;
- the exporter rules in the last section are **inference**.

**Review note (2026-10-31):**
- **Emulation rerun:** I ran `lifecycle.py --version v1` from a scratch copy with the output
  redirected. The result is **byte-identical** to `lifecycle-v1.json`.
- **Disassembly:**
  - **Compaction callers:** `FUN_0044adb0` has exactly two call sites, both in `FUN_00451fdc`.
    - `0x451FDC` runs once on entry.
    - `0x451FE3` runs inside the loop, immediately before each AI seat's `FUN_0044fa20`
      (`0x451FE8`). The loop continues while there is no battle (`0x4A0B7C`), the current seat is
      AI (`+0x490`) and `FUN_00449050` advances.
    - On a human seat it falls through to `FUN_00452034` (`0x45202D`), with no compaction in between.
  - **Army cap:** the constructor tests `count` against `0xC6` (198) at `0x449F3C`.
  - **AI fleet build:** `FUN_00450768` tests the fleet count against `0x63` (99) at `0x45076A` and
    the treasury (+0x438) against `0xBB8` (3,000) at `0x450785`.
- **Not checked:** recruitment and the AI split were read in the decompile only, as the draft says.
  The other field lists are taken from the emulation receipt.

## Answer

**Every path that changes the army or fleet tables** `[code]`:

| Event | Routine | Effect |
|---|---|---|
| new army | `FUN_00449f08` | appends at index = count, only while count < **198** and a free cell is found near the point. Callers: recruitment, the AI split, the player's split |
| unit into an army | `FUN_0044a4e0` | uses an own army at the recruiting city with a free slot, or creates one. It fills the slot, names it (`FUN_0044a218`), clears the recruit entry and sets the size-band marker |
| AI over-capacity split | `FUN_0044f8fc` | a new army at the same position takes whole slots from the first slot where cumulative troops exceed the capacity, plus **a third** of the supplies and of the money |
| new fleet | `FUN_0044a004` | appends at index = count and charges 10 × ships. There is no cap inside; the AI caller requires fewer than **99** fleets and a treasury above 3,000 |
| fleet launch | `FUN_0044a050`, from the round tick | places the fleet next to its build city and sets its condition, supplies, money and marker |
| army removed | `FUN_0044ab90` (12 callers) | **tombstone**, owner −1. If the army is aboard, the first live fleet at its coordinates gets carrier −1; otherwise the map cell gets its underlay back |
| fleet removed | `FUN_0044ad38` (11 callers) | **tombstone**. A launched fleet's cell becomes sea, and **a carried army is removed with it** |
| fleet merge | `TUnitMap_JoinFleets` | refused if either fleet carries an army, or above 100 ships. Ships, supplies and money are summed, moves are set to 0, and the other fleet is tombstoned |
| compaction | `FUN_0044adb0`, only from `FUN_00451fdc` | armies, then fleets, from the last index down. Each tombstone receives the current last record, and the count drops by 1 |

**When compaction runs:** once on entry to `FUN_00451fdc`, then before every AI seat, and never after
the last AI seat. So tombstones from the last AI seat, or from the human, survive into the human's
turn and its saves, and are compacted at the next End turn. This matches the
[sweep model](2026-10-30-army-table-order-after-deaths117.md).

**Prototypes** `[confirmed: emulation]`:
- **Army constructor** (Carthage, AI): index 14 = the old count, count 14 → 15. It writes **96 of 656
  bytes**:
  - x, y, owner, **moves 1** (0 for a human nation), the covered cell, supplies 0, money 0,
    **morale 59**;
  - type 0 and troops 0 in each of the 20 slots;
  - the map cell becomes 200 + owner.

  Each slot's label, quality and 24-byte name stay as residue.
- **Fleet order** (12 ships): **10 of 26 bytes**: owner, countdown 24, ships, build city, carrier −1;
  treasury −120.
- **Launch:**
  - it writes x, y, countdown −1, supplies 50, money 0, condition 100 (reusing the build-city word),
    +0x18 = 0 and the marker 300 + owner;
  - **the route words +4..+7 and moves +0xC are left as residue**, as the atlas observed in Wine.
- **Compaction** (14 armies, tombstones at 1 and 4, the last army aboard fleet 0):
  - the new order, as the old index per new index, is `0, 12, 2, 3, 13, 5, 6, 7, 8, 9, 10, 11`;
  - **fleet 0's carrier is repointed 13 → 4** (`FUN_0044abe0` rewrites every fleet whose carrier
    equals count − 1);
  - the two vacated slots keep their bytes.

## Rules for writing native state without provenance (inference)

- **Order:** a compacted table (no owner −1 records) in creation order with last-into-gap removal is
  a state the original produces after every compaction, so it is valid original state. Tombstones
  are optional. The order still matters for the AI's tie-breaks
  ([#117](2026-10-30-army-table-order-after-deaths117.md)).
- **Carrier link:**
  - fleet +0x16 holds the army's index;
  - the army has cell +8 < 0 and the fleet's exact coordinates, since removal finds the fleet by
    coordinates;
  - **a fleet carries at most one army**;
  - reordering armies means rewriting every fleet's +0x16; fleets can be reordered freely.
- **A new army record:**
  - write the constructor's 96 bytes;
  - fully write each live slot (label, type, troops, quality, name);
  - in empty slots, set type and troops to 0. Their other fields are residue with no effect, and zero
    is what a never-used slot holds.
- **Unit names:** "&lt;N&gt;&lt;st/nd/rd/th&gt; &lt;Foot|Guards|Bowmen|Lancers|Dragoons&gt; Battalion".
  - N is the lowest number from 1 that no live regular unit of the same owner and type uses, capped
    at 99.
  - The suffix follows N mod 10, except 11–13, which take "th".
  - Names are text only, so remake-chosen names are valid.
- **A new fleet record:**
  - a launched fleet takes the launch's fields plus moves and route_x = −1;
  - a fleet under construction takes the order's 10 bytes with the other words 0, as all 120 such
    fleets in the atlas corpus hold.
- **Caps:**
  - armies: fewer than 198 when one is created;
  - fleets: fewer than 99 for AI builds, with no cap in the human order routine;
  - at most 100 ships after a merge;
  - the fleet table holds 140 records in memory.

  A native state beyond these has no original equivalent.

## What this does not establish

- **Read but not executed:** recruitment and the AI split, which need a ready recruit entry or an
  over-capacity embark.
- **Not traced:** the player's split dialog beyond its constructor call.
- **Byte identity** for records without lineage: residue makes it impossible by construction. These
  rules are about valid original state only.
- Native Windows behaviour, live game runs, or the owner's JSON files.
