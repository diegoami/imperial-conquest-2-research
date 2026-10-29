# All-ashore unload with several live armies: the receiver is appended, and the next sweep swaps it into the source's slot

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `de1b7bb` (PR #253). It
answers imperial_conquest_2 [#1439](https://github.com/diegoami/imperial_conquest_2/issues/1439),
delegated to conquest on 2026-10-29. Runner: ic2-conquest `runs/experiments/ashore1439/original.py`,
on the #174 overflow runner and its RAM baseline. Data:
`runs/experiments/data/run-exp-ashore1439/` (`v1_*` without the sweep, `v2_*` with it). The RAM and
the SAV projections stay private.

**Tag:**
- the tables: `[confirmed: emulation]` of the unmodified original routine `0x44B79C` in Unicorn;
- the sweep timing and turn order: `[derived: code]`.
- No game run.

**Review note (2026-10-29):**
- **Rerun:** I ran a scratch copy of `original.py` with its output redirected. It reads
  conquest's #174 module and the private baseline and writes nothing in conquest. All four
  `v2_*.json` cases are **identical** to the committed ones: the source at raw index 0, 2 or 4 of
  5, and the source at 2 with a prior tombstone at 1.
- **Decompile re-read:**
  - **The sweep** `FUN_0044adb0` (:49537) walks the army table from the last index down and calls
    `FUN_0044abe0` for each record whose owner is −1. It does the same for fleets with
    `FUN_0044ad7c`.
  - **The swap-remove** `FUN_0044abe0` (:49396) copies the **last** record into slot *i*,
    repoints any fleet's carried-army index that pointed at the old last index, and decrements
    the count.
  - **`FUN_00451fdc`** (:54939) sweeps once at its start, then before each AI seat's
    `FUN_0044fa20`, while the current seat is not human.
- **Overlap.**
  - [`2026-10-26-fleet-overflow-receiver174.md`](2026-10-26-fleet-overflow-receiver174.md) showed,
    for one input, that the source is tombstoned and ABE0 is not called at the embark. This
    extends it to several live armies.
  - The rules spec §3 already describes the sweep for elimination
    ([`decompiled-elimination-cleanup.md`](decompiled-elimination-cleanup.md)).
  - Nothing is contradicted.

## Answer

The control: the unmodified all-ashore AI embark (`0x44B79C`) with **5 live armies**.

1. **At the embark**, `F8FC`/`49F08` **appends** the land receiver at raw index = count (5 → 6).
   `AB90` **tombstones** the source in place: owner −1, troops 0, at the fleet cell. ABE0 is not
   called, and an existing tombstone is not reused.
2. **At the next dead-record sweep** (`FUN_0044adb0`), ABE0 swap-removes each tombstone: the last
   record moves into its slot, and fleet links are repointed.
   - So, when there is no other tombstone, the receiver **lands exactly at the source's index**.
     That is the same table as the remake v0.8.4's in-place replacement.
   - With another tombstone present, the sweep also reorders unrelated armies. In the
     tombstone-at-1 case, the last record (F4) moves into slot 1. This is how the sweep always
     behaves, not something specific to the embark.
3. **Timing** `[derived: code]`:
   - `F31C` snapshots the army count, so the receiver is not visited in the rest of that army
     phase.
   - The sweep runs at the start of `FUN_00451fdc` and before each AI seat.
   - If the embarking seat is the last AI seat before a human seat, the human's turn and its
     autosave see the **unswept** table: the tombstone still in place and the receiver last.

**For #1439:** the "append, then compact" hypothesis is half right. The receiver is appended at the
embark. The compaction is a later swap-remove sweep, not something done at the embark. For the
swept state no remake change is needed.

## What this does not establish

- Play: everything here is emulated.
- Saving and loading an unswept table.
- The remake's own order for removing dead armies. *(Since answered: [2026-10-30-army-table-order-after-deaths117.md](2026-10-30-army-table-order-after-deaths117.md).)*
- The fleet sweep (`FUN_0044ad7c`), which these controls did not exercise.
