# Army-table order after deaths: the original's swap-remove sweep reorders survivors, and the small-army merge depends on that order

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`. First version at commit `5ae30c9`
(PR #259); **corrected** at `791bc4f` (PR #260). It answers research issue
[#117](https://github.com/diegoami/imperial-conquest-2-research/issues/117) (raised during the main
project's evaluation of #1439), delegated to conquest on 2026-10-29.
- **Scripts:** `runs/experiments/armyorder117/*.py`.
- **Data:** `runs/experiments/data/run-exp-armyorder117/`.
- **Original saves:** release
  [`run-exp-diff084-campaign`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-campaign).
- **Remake runs:** release
  [`run-exp-armyorder117`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-armyorder117),
  with `run-exp-armyorder117.tar.gz` for v1 and `run-exp-armyorder117-v2.tar.gz` for v2.

**Tag:** `[confirmed]`. The orders come from Wine play and remake runs; the merge dependence comes
from emulation of the pinned EXE on the #187 RAM snapshot.

## Correction (2026-10-29)

The first version paired campaign checkpoints **by name**: turn N's last checkpoint against turn
N+1's `a00`. Checkpoints are numbered per **action**, though. When a turn has orders, `a00` is the
save after its first order.
- So 27 of the first version's 64 pairs ended mid-turn, with no AI round, and 43 of the 80 End
  turns were missing.
- The remake pairs compared a turn's end with the same state re-imported, which produced the false
  "no remake deaths".

The corrected version pairs each End turn **from the receipts**: the state at the End-turn click
against that End turn's autosave. The autosave is written after every AI seat, just before
`StartTurn`.

| | First version (PR #118) | Corrected |
|---|---|---|
| original End turns / with deaths | 64 / 19 | **80 / 43** |
| survivor order kept (original) | 2 of 19 | **4 of 43** |
| sweep model reproduces the original | 18 of 19 | **42 of 43** |
| remake, from the original's click states | order kept 19/19 | deaths in **37**, order kept **37/37** |
| remake's own campaigns | "no deaths in 80 turns" | **44 death turns of 80, order kept 44/44** |
| same-nation inversions | 0 of 19 | **0 of 43** |
| dead records in autosaves | 3, "created during the human's turn" | **4**: deaths after the last sweep |

**Withdrawn:**
- the claim that dead records were "created during the human's own turn and survived the End turn";
- the related open item about an untraced path.

**Unchanged:** the merge control and the F31C swaps. The conclusions stand.

This research session promoted the first version after rerunning its scripts. Those reruns could
not catch a wrong pairing of their inputs; the correction came from conquest itself.

**Review of the correction:**
- **Reruns from scratch copies, outputs redirected,** all identical to the committed files:
  - `order_in_play.py --version v3` (receipt pairing);
  - `sweep_model.py --input v3 --version v5`;
  - `remake_order.py --version v2`;
  - `same_nation.py --input v3 --version v2`. The script reads `order-in-play` and
    `sweep-model` under one label, so it was run against the intermediate `sweep-model-v3`. The
    fields it uses, `actual` and `remake_rule`, are identical in v3 and v5.
- **Every corrected number** in the table above was recomputed from that data, including the
  remake-same-turns result (37/37) from the committed `remake-same-turns-v2.json`.
- **The release's remake-v2 saves:** 86 of 86 match `SAVES.sha256`. The remake runs were not
  re-executed here, since that needs the .NET remake.
- **Decompile:** `FUN_004509f0` (:53949) walks the army table in ascending index order, stops at
  the first qualifying pair, and moves the lower-indexed army's units into the other one.

## Answer

1. **The orders diverge whenever armies die.** In the original's #232 campaigns, 43 of 80 End turns
   had deaths, and the survivors kept their relative order in only 4.
   - The remake keeps the order in every death turn: 37 of 37 from the original's own End-turn
     click states, and 44 of 44 in its own campaigns.
2. **The sweep model reproduces the original.** Grouping the deaths into successive sweeps
   (`FUN_0044adb0`, swap-remove, highest index first) reproduces the observed order in 42 of 43
   turns. The model sweeps the pre-turn table's old dead records first and leaves deaths after the
   last sweep in place. The 43rd turn is an identity ambiguity: a human Join plus a battle-mauled
   army.
3. **Exported save order differs accordingly.** The original's End-turn autosaves can hold **dead
   records** (4 cases).
   - These are deaths after the last sweep, from a late AI seat or from the AI merge's donor, as
     the code predicts.
   - The next End turn's first sweep removes them.
   - The remake never exports a dead record.
4. **AI decisions.**
   - **The small-army merge depends on table order.** `FUN_004509f0` (economy phase) picks the
     donor and receiver by index. On the #187 RAM, Carthage's two 12,000-troop armies merge onto
     (45,63) in the captured order and onto (47,62) when the records are swapped.
   - **The army phase visits in table order** (F31C). Swapping armies at game start changed
     nothing.
   - **No observed case where it mattered:** none of the 43 death turns inverted two surviving
     armies of the same nation.
   - **Cross-nation targeting also follows table order** (addendum, conquest PR #261, commit
     `46cbf74`).
     - **The enemy army an AI army goes for:** `FUN_0044ee60` (:52715–52776) scans every army of
       a nation at war in table order. Score = `min(1000, strength × 110 / enemy − distance)`
       (halved by `FUN_0044eb9c`'s test), +1000 if weaker and within 7. It replaces the current
       pick only when **strictly** greater, so the lowest index wins ties. Because the cap applies
       before distance can separate candidates, a strong army scores **every** weak enemy within
       7 tiles at 2000, and it picks the first in table order, not the nearest.
     - **Emulated** on the #187 RAM, unmodified: Carthage's 33,900 troops at (47,62), at war with
       Rome, with two 2,000-troop Roman armies. In the staged order the target is (44,62); with the
       records swapped it is (50,62). With the Romans 3 and 4 tiles away, swapping makes it chase
       the **farther** one, (51,62).
     - **Capital defence:** `FUN_0044efc8` (:52776–52899, read only) lists the enemy armies near
       the capital in table order, at most 10, then assigns its own armies in list order
       `[derived]`.
     - **So a cross-nation reorder after deaths can change an AI army's target and its capital
       defence.**
     - **Review:** I reran `tiebreak.py` from a scratch copy (with `visit_order.py`, outputs
       redirected); the result is identical to `tiebreak-v1.json`. The scoring lines of
       `FUN_0044ee60` were re-read: the cap at 1000, the +1000 bonus, and the strict `<`
       replacement.

## What this does not establish

- Later games with several armies per nation, where same-nation inversions and the merge
  dependence would show up.
- Other cross-nation scans (`FUN_004502e0`, `FUN_0044ffbc`): not read. Whether an `FUN_0044ee60` tie actually occurred in the 43 observed death turns was not checked.
- How the remake handles an imported dead record.
- Native Windows behaviour.
