# What still differs in the campaigns at remake v0.8.5: one weather draw, two unported fleet moves, one army target choice, and random draws

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `29d7535` (PR #275), run
at the owner's request, which was to stop at work the remake has not implemented yet.
- **Script:** `runs/experiments/campaign085/attribute.py`.
- **Data:** `runs/experiments/data/run-exp-campaign085/` (`groups-v1.json`, `aiprobe-rome-t1.jsonl`).
- **Remake saves:** release
  [`run-exp-recheck-1622407e`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-recheck-1622407e).
- It follows [`2026-10-30-recheck-v085.md`](2026-10-30-recheck-v085.md).

**Tag:** `[confirmed, partial]`.

**Review note (2026-10-30):**
- **The turn-16 jump, recounted from the saves.** Both games have 112 rough-sea cells at the start
  of turns 15 and 16. At the start of turn 17, after turn 16's End turn redraws the weather, the
  original has **0** and the remake **520**.
- **Turn 1 in the bot campaigns,** checked in Armenia's campaign. The original's End-turn autosave
  (`t01-a01`) has Carthage's fleet 0 at (74,71) and army 3 at (88,77). The remake has fleet 0
  unmoved at (49,62) and army 3 at (94,78). Nation 3's fleet 1 makes its swing in the original
  only: 28 moves → 5. This matches `groups-v1.json`.
  - *(Pairing note: checkpoints are numbered per action, so turn 1's End-turn state is `t01-a01`,
    not `t02-a00`. This review first compared the wrong save.)*
- **A refinement of the draft's army-3 attribution.** The remake's AI probe has army 3 aiming at
  the resupply city (95,77). It moves 1 cell to (94,78) with 8 moves left, and its distance after
  the walk is **1**.
  - The original's AI move keeps walking only while the distance is **above 1**
    ([continuation](2026-10-30-ai-march-continuation-missing-in-remake.md)). So on this move the
    missing continuation would not change the remake's result.
  - The difference here comes from **target selection**: the remake chose the resupply city, while
    the original sent the army west. The draft names "the resupply selector (#1402) plus the
    missing march continuation"; for this case only the first part applies.

## Answer

1. **All-human campaign, turn 16:** the first weather redraw gives 0 rough-sea cells in the
   original and 520 in the remake. The only other difference is one fleet's storm condition, 70 vs
   72. Over 32 turns there is **no rule difference**; the weather is a random draw.
2. **Bot campaigns, turn 1:** two AI fleets differ in 13 of 16 campaigns.
   - Carthage's fleet 0 sails to (74,71) in the original, and nation 3's fleet 1 makes its
     out-and-back swing.
   - The remake moves neither, because it has not ported F608/E1FC (#1405/#1409; see
     [fleet move contract](2026-10-30-fleet-move-contract131.md)).
3. **Carthage's army 3** (13 of 16 campaigns): the original sends it west, to (88,77).
   - Its only enemy-army candidate scored 93, so there was no attack. It took the over-70 army
     branch or a city target; which of the two is not established.
   - The remake chose "move to the resupply city" (the selector of #1402).
4. **Everything else** is random draws: city supplies ±1–2, AI recruitment, treasury, relations
   and map cells. The original's own values vary between campaigns; for example, city 1 ranges
   from 74 to 79.

## What this does not establish

- *(Since answered: [2026-10-30-carthage-army3-branch138.md](2026-10-30-carthage-army3-branch138.md). The original takes the `FUN_0044e84c` walk, because both scores are ≤ 100.)*
- A statistical test that the city-supply differences are purely random.
