# Carthage's army 3 on turn 1: the original takes the FUN_0044e84c walk because both target scores are ≤ 100; the remake's main differs in EE60's halving test

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `c3f2cad` (PR #277). It
answers research issue [#138](https://github.com/diegoami/imperial-conquest-2-research/issues/138)
(remake [#1628](https://github.com/diegoami/imperial_conquest_2/issues/1628)), delegated to conquest
on 2026-10-30.
- **Data:** `runs/experiments/data/run-exp-army3-138/`: the remake's own decision logs at
  `1622407e` (v0.8.5), `dab3a2ea` and `d8e7a646` (main), a patched copy of main, and
  `ee60-classify.patch.txt`.
- **Original side:** the earlier inert hook logs `run-exp-walk-hook97/BASE-walk.jsonl` and
  `run-exp-tiehook117-long/rome-BASE-ties.jsonl` (`BASE.SAV`, turn 1, seed 12345).

**Tag:** `[confirmed]`: hooks observing the original in play, decompile, and the remake's own
decision records.

**Review note (2026-10-30):**
- **The original, from the committed hook logs:**
  - the enemy-army pick for actor 3 chose army 10 with score 34 and distance 59, so the final
    score is **93**, not above 100;
  - its first move (call site `e913`, `FUN_0044e84c`'s walk) heads for (111,69) from (93,79) with
    8 moves;
  - a second call (`f4a3`, toward army 10 at (34,63)) comes with **0** moves and does not move it.
- **The halving test in the decompile:** `FUN_0044eb9c` compares `FUN_0044eb18` (the
  region-and-side classification, the remake's `Classify`) of the two points, and halving applies
  when they differ.
- **The remake source:**
  - at `d8e7a646`, `AiArmyTargetTree.cs:293` halves the army score when `RegionOf` differs;
  - the city scorer (line 185) already uses `Classify` under faithful navigation;
  - at `1622407e`, the extra `IsReachable` gates are visible at lines 161 and 280.
- **The decision logs** for Carthage's army 3:
  - `1622407e`: `MoveToResupplyCity`, with no city or army target and 20 skipped;
  - `d8e7a646`: `AttackArmy`, army score **126**;
  - the patched copy: `MercenaryRun`, army score **93**, city score 91 (osca).

  The patch replaces `RegionOf` with `Classify` in the army scorer's halving test, and it
  reproduces the original's branch and scores.

## Answer

1. **The original** (army phase F31C, `BASE`, turn 1):
   - Army 10 scores 93 and city osca 91; neither is above 100, so neither is attacked.
   - Resupply is false: a city target exists, and troops/500 = 49 (24,600 / 500) is below the 246 supplies. These are the values after the supply pass `FUN_0044e41c`, which F31C runs just before the decision. *(Corrected 2026-10-30: the first version read 37 and 90 from the save; the branch is unchanged. See [ai decisions vs remake main](2026-10-30-ai-decisions-vs-remake-main.md).)*
   - So it takes the `FUN_0044e84c` walk (call `e913`) toward (111,69), and ends at **(88,77) with
     0 moves**.
   - The following over-70 step (`f4a3`) toward army 10 does not move it, since it has no moves
     left.
2. **Remake v0.8.5** finds **no** city or army target: 20 are skipped by an extra `IsReachable`
   gate for a different geography. So its no-target clause sends the army to resupply.
   **The resupply selector is not at fault.**
3. **Remake main `d8e7a646`** (T247, unreleased) ends on the same cell, but through `AttackArmy`
   at score 126.
   - Its army scorer halves by the nearest city's region (`RegionOf`).
   - The original's EE60 halves when `FUN_0044eb9c`/`eb18` (= `Classify`) differs: 67 − 33 = 34,
     plus 59 = 93.
   - The city scorer and the capital defence on main already use `Classify`.
   - A one-line change to `Classify` reproduces the original's branch (`MercenaryRun`), aim
     (111,69), score 93 and end cell (88,77).

**For #1628:** on main the target-gate part is fixed. One rule gap remains: EE60's geography
halving should use `Classify`.

## What this does not establish

- Later turns: main's `AttackArmy` leaves a stored route at (34,63).
- A recheck of the 13 campaigns at main.
- The `FUN_0044e84c` table contract compared against the remake.
- The original's city score, which was not hooked; it does not matter here.
