# The AI fleet move contract (FUN_0044e1fc): replace a land target by nearby sea, route through a group-0 waypoint, fall back, recurse, arrive at every level

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `3452f6e` (PR #272). It
answers part 3 of research issue
[#131](https://github.com/diegoami/imperial-conquest-2-research/issues/131) (remake #1405/#1409),
completing it; parts 1–2 are in
[`2026-10-30-fleet-route-lifetime131.md`](2026-10-30-fleet-route-lifetime131.md).
- **Script:** `runs/experiments/fleetroute131/part3.py`.
- **Data:** `runs/experiments/data/run-exp-fleetroute131/part3-v3.json`. `part3-v1` and `v2` are
  kept as superseded: their level bookkeeping was wrong, though their D174 checks are unaffected.

**Tag:** `[confirmed]`: unmodified original instructions in Unicorn, traced level by level with
no helper replaced.

**Review note (2026-10-30):**
- **Rerun:** I ran `part3.py --version v3` from a scratch copy, with a redirected copy of
  `phase.py` alongside it. It reads conquest's private fleet174 inputs and the #187 model and
  writes nothing there. The result is **identical** to `part3-v3.json`: 41 cases, and 21 D174
  calls that all equal the #187 portable model for group 0.
- **Overlap.** This explains the "(74,69) endpoint" of
  [`2026-10-24-fleet-accepted-movement174.md`](2026-10-24-fleet-accepted-movement174.md) and the
  out-and-back swing of
  [`2026-10-30-ai-fleet-moves-in-play1409.md`](2026-10-30-ai-fleet-moves-in-play1409.md). Nothing is
  contradicted.

## Answer: the contract of `FUN_0044e1fc`

1. **The target's map code is read once,** at entry, from the original target.
2. **If the direct line passes** (CB40), the fleet walks toward the target.
3. **Otherwise, a land, city or army target** (map code 2–247) is **replaced** by
   `FUN_0044939c`.
   - It searches squares of growing radius around the target for sea.
   - The **last** match in scan order wins: largest x offset, then largest y.
   - The eastern zone is skipped.
   - D174 group 0 is then applied to the replaced point. The direct line is **not** tested again.
4. **If no move was made,** CEC8 picks a fallback cell and **1 move is charged, even if CEC8
   finds nothing.**
5. **It recurses on the original target.**
6. **The arrival branch,** chosen by the original target's code, runs **at every level** as the
   recursion returns.

**Decisive rows:**

| Case | Result |
|---|---|
| a land route across the coast, target (47,64) | replaced by (48,65), only 3 cells away. D174 still takes the common-visible waypoint nearest the origin, node 5 at (75,69), so the fleet ends at **(74,69) with 0 moves**. A carried army stays aboard and follows it |
| the swing beside a land target | costs **7 moves** (25 → 18); the landing happens at recursion depth 1 |
| docking at an own port | the docking runs **twice** in one move, at depth 1 and at depth 0 |
| a fleet starting on its route cell | a **24-move round trip** to (39,78) |
| a stored route with zero moves | nothing happens |

## What this does not establish

- **CB40 at distance 0** reads an uninitialised value (#187). It returned false in these runs;
  another stack history could return true.
- Naval combat, and arrival at a city at war, were not executed.
- The arrival branch for a plain sea step did not occur.
