# Army-table order after deaths: the original's swap-remove sweep reorders survivors, and the small-army merge depends on that order

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `5ae30c9` (PR #259). It
answers research issue [#117](https://github.com/diegoami/imperial-conquest-2-research/issues/117)
(raised during the main project's evaluation of #1439), delegated to conquest on 2026-10-29.
- **Scripts:** `runs/experiments/armyorder117/*.py`.
- **Data:** `runs/experiments/data/run-exp-armyorder117/`.
- **Original saves:** release
  [`run-exp-diff084-campaign`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-campaign).
- **Remake runs:** release
  [`run-exp-armyorder117`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-armyorder117).

**Tag:** `[confirmed]`. The orders come from Wine play and remake runs; the merge dependence comes
from emulation of the pinned EXE on the #187 RAM snapshot.

**Review note (2026-10-29):**
- **Analyses rerun.** I reran four of the scripts from scratch copies with outputs redirected,
  reading the local campaign saves. Their outputs are **identical** to the committed files:
  - `order_in_play.py` v2;
  - `sweep_model.py --input v2` v2;
  - `same_nation.py` v1;
  - `visit_order.py` v3 (the merge control, Unicorn).
- **Headline numbers, recomputed from that data:**
  - 64 End-turn transitions, **19** with deaths or merges;
  - survivor order preserved in only **2 of 19**;
  - the sweep model explains **18 of 19**; the exception is Macedonia's turn 2, the draft's
    identity ambiguity;
  - **0** inversions of two armies of the same nation;
  - dead records carried in **3** post-turn autosaves (Bithynia twice, Carthage-r2 once).
- **Remake runs:** the release's 38 saves match `SAVES.sha256` (38 of 38). The remake-order
  results were not rebuilt here, since that needs the .NET remake.
- **Decompile re-read.** `FUN_004509f0` (:53949) walks the army table in **ascending index**
  order, stops at the first qualifying pair, and moves the lower-indexed army's units into the
  other one. So its donor and receiver depend on table order. The sweep (`FUN_0044adb0`) and
  swap-remove (`FUN_0044abe0`) are as in
  [`2026-10-30-all-ashore-army-order1439.md`](2026-10-30-all-ashore-army-order1439.md), whose open
  item ("the remake's own order for removing dead armies") this answers.

## Answer

1. **The orders diverge whenever armies die.** In the original's #232 campaigns, 19 of 64 End-turn
   transitions had deaths, and the survivors kept their relative order in only 2.
   - The remake, run from the **original's own pre-End-turn saves** of those 19 turns, keeps the
     order in 19 of 19.
   - The remake's own campaigns had no deaths in 80 turns.
2. **The sweep model reproduces the original.** Grouping the deaths into successive sweeps
   (`FUN_0044adb0`, swap-remove, highest index first) reproduces the original's observed order
   exactly in 18 of 19 turns. Examples:
   - deaths at 9 and 10 of 14 records give …, 8, 13, 12, 11;
   - the death of record 0 brings the last record to the front.
3. **The exported save order differs accordingly.**
   - The original's saves can also hold **dead records**: 3 autosaves carry one, created during
     the human's own turn, which survived the End turn. That path was not traced.
   - The remake never exports a dead record.
4. **AI decisions.**
   - **The small-army merge depends on table order.** `FUN_004509f0` (economy phase, via
     `FUN_0044ffbc`) picks the donor and receiver by index. On the #187 RAM, unmodified,
     Carthage's two 12,000-troop armies at (47,62) and (45,63) merge onto (45,63) in the captured
     order, and onto (47,62) when the two records are swapped.
   - **The army phase visits in table order** (F31C). Swapping nations 0, 1 and 2's two armies at
     game start changed nothing: the armies were far apart and no random draws were involved.
   - **No observed case where it mattered:** none of the 19 death turns inverted two surviving
     armies of the **same** nation (1–2 armies per nation early on).

## What this does not establish

- Later games with several armies per nation, where same-nation inversions and the merge
  dependence would show up.
- Cross-nation tie-breaks, such as target choice or interception: not read.
- Which path leaves a dead record across an End turn.
- How the remake handles an imported dead record.
- Native Windows behaviour.
