# AI fleet moves in play: the direct line or a group-0 waypoint, at most two levels deep; land-adjacent fleets swing out and back every turn

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `edc13ea` (PR #254). It
answers imperial_conquest_2 [#1409](https://github.com/diegoami/imperial_conquest_2/issues/1409)
and the leftover of research #42, delegated to conquest on 2026-10-29.
- **Hook:** `patches/fleet_hook.py`, observation-only, with five probes in `FUN_0044e1fc`.
- **Runner:** `difftest/probes/fleet_hook_run.py`.
- **Analysis:** `runs/experiments/fleethook1409/analyze.py`.
- **Data:** `runs/experiments/data/run-exp-fleethook1409/`.

**Tag:** `[confirmed, partial]`, observed in play: the seed build under Wine, 3 starts × 4 AI End
turns. **Promoted provisional:** the autosaves are in conquest's local artifacts only, and the
release `run-exp-fleethook1409` is not published yet (creating it awaits the owner).

**Review note (2026-10-29):**
- **Saves:** all 24 local autosaves match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain autosaves myself: **12 of 12** pairs are
  byte-identical.
- **Analysis rerun:** `analyze.py` (scratch copy, output redirected) reproduces `summary-v1.json`
  exactly:
  - 18 top-level fleet moves and 43 levels, of which 29 direct and 14 through D174;
  - 13 D174 points from the group-0 waypoint table; D174 never returned none;
  - 13 CEC8 fallbacks; 16 recursive calls; maximum depth 2.
- **Overlap.** This closes the open item of
  [`2026-10-30-paths-in-play-and-fleet-walks42.md`](2026-10-30-paths-in-play-and-fleet-walks42.md)
  (the AI fleet route-finder branch). It is consistent with
  [`2026-10-30-ai-move-fallback-point105.md`](2026-10-30-ai-move-fallback-point105.md): flag 1 in
  the fleet phase, but the sea tolerance never mattered here because all origins were sea.

## Answer

In the 12 AI turns:
1. **Routes:** 18 top-level fleet moves ran 43 wrapper levels.
   - 29 levels went by the **direct line** (CB40).
   - 14 went **through D174**. 13 of its points are **group-0 waypoints** (ids 5, 6, 7, 9 and
     22), and 1 is D174's origin-local CEC8 fallback. D174 never returned none.
2. **Recursion is shallow:** at most **2** levels.
3. **CEC8 fallbacks** (13) all came from fleets **at distance 1 from a land target**.
   - The fleet swings three cells out and back and ends on the same cell, having spent 7–23
     moves. It does this **every turn**.
   - Carthage's fleet 0 at (105,63) does it twice per turn.
   - Nation 3's fleet 1 at (189,93) does it via waypoint 22, spending 22–23 of its 28 moves.
4. **The fleet-phase sea tolerance** (`DAT_004a0340` = 1) never mattered: every origin was sea.

## What this does not establish

- The arrival part of the fleet move.
- The `FUN_0044939c` target replacement, and D174's internals: these were not logged.
- More than 3 starts and 4 turns each.
- Native Windows behaviour.
- **Public evidence:** the autosaves await the owner's release.
