# The AI army move's no-progress fallback (FUN_0044cec8), and CB40/DB38 against the remake's ClassicalArmyNavigation

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `b09403e` (PR #252). It
answers research issue [#105](https://github.com/diegoami/imperial-conquest-2-research/issues/105)
(for imperial_conquest_2#1592), delegated to conquest on 2026-10-29. Remake compared: v0.8.4
(`d9cc71b`), `src/IC2.Engine/Ai/ClassicalArmyNavigation.cs`.

**Tag:** `[confirmed: emulation of the pinned unpatched EXE]` (`9d753d5d…`). The routines run
unchanged in Unicorn, on real SAV grids and on the #187 live-RAM snapshot. Nothing here was observed
in play.

**Review note (2026-10-29):**
- **Routine controls rerun.** I ran ic2-conquest's `runs/experiments/fallback105/controls.py` from a
  scratch copy on the pinned EXE and the same 15 grids (14 committed saves plus `BASE.SAV`). The
  output is **identical** to `controls-v1.json`:
  - CEC8 with flag 0: 3,303 of 3,303 agree (12 "none");
  - CEC8 with flag 1: 2,214 of 3,303 agree, and the differences all have land origins;
  - CB40: 44,734 of 44,734 agree.
- **The "remake" side of those controls is a Python port.** I compared it line by line with the
  remake's `LocalFallback` and `DirectLine` at v0.8.4. It matches: loop order, clamp, three-cell
  probe, last success wins, Bresenham with the minor step first, and the final sample excluded. The
  remake's `IsSea` reads entity lists, while the port reads the save's map words, which encode the
  same markers (city and army markers are land, fleet markers are sea).
- **Wrapper controls rerun.** I ran `wrapper_controls.py` from a scratch copy with its output
  redirected. It reads conquest's `navigation187/core.py` and the private #187 RAM snapshot, and
  writes nothing there. All **80 rows are identical** to `wrapper-controls-v1.json`.
- **Decompile re-read.**
  - `FUN_0044cec8` (:51124) matches the stated contract: `out.x = −1`, the eight directions with dy
    inside dx, the clamp to 319/139, the sea test `< 2 || > 299`, and the `DAT_004a0340` tolerance.
  - `DAT_004a0340 = 0` at the top of `FUN_0044f31c` (army phase, :52917) and `= 1` at the top of
    `FUN_0044f608` (fleet phase, :53040). The seat loop calls F31C before F608 (:53219–53220).
  - The remake's `Intermediate` throws `NotSupportedException` once the depth exceeds
    `Points.Length` (58).
- **Overlap.** This completes "What this does not establish" in
  [`2026-10-30-ai-march-continuation-missing-in-remake.md`](2026-10-30-ai-march-continuation-missing-in-remake.md)
  (the semantics of CB40, DB38 and CEC8). It builds on
  [`2026-10-24-seleucid-strategic-target-routing1388.md`](2026-10-24-seleucid-strategic-target-routing1388.md)
  and the #97 stale word
  ([`2026-10-30-ai-move-stale-word-in-play97.md`](2026-10-30-ai-move-stale-word-in-play97.md)).
  There is no contradiction.

## Answer

1. **`FUN_0044cec8(P, &out)`: three steps on the same medium, last direction wins.**
   - It sets `out.x = −1`, then tries the eight directions `(dx, dy)`: dx = −1, 0, 1 in the outer
     loop and dy = −1, 0, 1 in the inner loop, skipping (0, 0).
   - A direction succeeds when each of its three cells `clamp(P + s·(dx, dy))` (s = 1, 2, 3; x
     clamped to 0–319, y to 0–139) has the same medium as P.
   - The medium is sea when the grid code is < 2 or > 299, so fleet markers count as sea. Terrain,
     city markers and army markers are land.
   - On success, `out = P + 3·(dx, dy)` (clamped), overwriting any earlier success, so the **last**
     successful direction wins.
   - It returns **none** (`out.x = −1`) only when all eight directions fail.
   - It reads no terrain cost, no unit and no random number.
   - **One extra input: `DAT_004a0340`.** A probe cell of the other medium is tolerated when that
     cell is sea and the flag is 1. The flag is **0 throughout the army phase**, so for armies it
     never matters. It is 1 for the fleet wrapper `FUN_0044e1fc` (relevant to #1409).
2. **How the wrapper uses it** (`FUN_0044dba8`):
   - The army first walks toward the target (direct line) or toward DB38's intermediate point.
   - If its moves are unchanged and positive, and `local_e ≥ 0`, it calls CEC8 on its **current
     position**. It walks toward the returned point if there is one, then **subtracts 1 move
     whether or not a point was found**.
   - It then recurses while the Chebyshev distance to the target is > 1, moves > 0, `local_e ≥ 0`
     and target x ≥ 0.
3. **The original's routines match the remake's for armies:** CB40 = `DirectLine`, D174 =
   `Intermediate`, DA88 = `RouteGroup`/`Classify`, CEC8 = `LocalFallback`.
   - CB40's final-sample mismatch is overridden (`local_1a < local_14`), which equals the remake's
     "excluding the final sample".
   - D174 has the same group bounds (1–25, 26–39, 40–54, 55–58), visibility lists, picks, the D010
     hand-off, and the same target-local recursion.
   - DB38 routes through D174 only when both points share (region, side). Otherwise it calls the
     ferry lookup D9A8, which the remake doesn't have (known; outside #105).

## Controls

**Routine level** (15 grids):

| Routine | Cases | Original = remake | Notes |
|---|---:|---:|---|
| CEC8, flag 0 (army phase) | 3,303 origins | **3,303** | 12 "none" |
| CEC8, flag 1 (fleet phase) | 3,303 | 2,214 | every difference has a land origin; none is in the army phase |
| CB40 | 44,734 random pairs (distance 1–40) | **44,734** | 33,614 true |

**Wrapper level:** the whole `FUN_0044dba8` on the #187 RAM snapshot, all cells Plain. Rome's army
2 stands at (100,40), and its march east is blocked by own army markers on (101,39), (101,40) and
(101,41).

| Case | Moves | Target | `local_e` | CEC8 point | Final cell | Moves left | Wrapper entries |
|---|---:|---|---:|---|---|---:|---:|
| open land | 1 | (103,40) or (106,40) | 0 | (103,43) | (100,41) | **−1** | 1 |
| open land | 2 | either | 0 | (103,43) | (100,41) | 0 | 1 |
| open land | 3 | either | 0 | (103,43) | (100,40) | 0 | 2 |
| open land | 5 | either | 0 | (103,43) ×2 | (100,41) | 0 | 3 |
| open land | 8 | either | 0 | (103,43) ×3 | (100,41) | 0 | 5 |
| open land | any | either | −1 | none called | (100,40) | unchanged | 1 |
| sea at (102,42) | m = 1–8 | either | 0 | **(103,40)**, m times | (100,40) | 0 | m |
| sea ring at Chebyshev 3 | 1–8 | (103,40) | 0 | none (all probes fail) | (100,40) | m − 1 | 1 |

What the rows show:
- **Moves can go to −1:** the fallback walk spends its step cost, and the wrapper then subtracts 1.
- **The army can oscillate:** at 3 moves it side-steps to (100,41), walks back on the next
  recursion, and ends where it started.
- **The fallback can point into the blockage:** with (1,1) cut by sea, the last successful
  direction is (1,0), the blocked direction itself. The army stands still and burns one move per
  recursion.
- **A "none" still costs 1 move.**
- **`local_e = −1` skips the fallback.** In play the word was never −1 (#97).

The remake's v0.8.4 faithful AI does not run this wrapper; it marches once per army per turn. So
these rows are the target behaviour for #1592, not a v0.8.4 diff.

**A divergent recursion, in both games.** When neither the target nor CEC8's point is visible from
the origin, D174 recurses on the point. With sea at x = 102–103, y = 37–43 and the target at
(103,40), the recursion cycles (103,40) → (103,43) → (103,40)… for 1,745 CEC8/D174 pairs in
Unicorn, until the emulated stack ran out. The remake's `Intermediate` throws past depth 58, and
`AiMilitaryPhase` drops the march. Here the target is a sea cell; a land target could cycle only in
narrow geometries, such as a diagonal strip of land.

## What this does not establish

- **Play.** No case ran in the game; the geometries are emulated only.
- **What the original does when D174 cycles in play:** a Delphi stack-overflow exception, a crash,
  or a geometry that never arises on the real map. No real-map pair was searched.
- **D010 and D9A8 beyond what #187 controlled,** and the fleet-phase sea tolerance (#1409).
- **The remake beyond v0.8.4.**

## Evidence

- **Scripts** (ic2-conquest): `runs/experiments/fallback105/controls.py` and `wrapper_controls.py`.
- **Data:** `runs/experiments/data/run-exp-fallback105/controls-v1.json` (with each grid save's
  SHA-256) and `wrapper-controls-v1.json`. The RAM snapshot stays private.
- **Decompile:** `all_app_functions.txt` (`2018c205…`). CB40 :50898, CEC8 :51124, D174 :51276,
  DA88 :51713, DB38 :51761, DBA8 :51792, F31C :52899, F608 :53028, FA20 :53210.
