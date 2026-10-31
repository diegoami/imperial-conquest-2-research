# AI fleet phase, original vs remake main: the branch rule matches; one fleet's route and moves state differs

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `1027118` (PR #288), for
conquest #174 (fleet hunt, port and stored-destination decisions), owner request 2026-10-31. It uses
the method of the [AI decisions](2026-10-30-ai-decisions-vs-remake-main.md) comparison and its
diplomacy and economy successors.
- **Hook:** `patches/fleetphase_hook.py`, observation-only, with two probes in `FUN_0044f608`:
  - `0x44F65B`: the port pick (`FUN_0044e9a8`), the stored route, the position and the moves;
  - `0x44F682`: `FUN_0044f4f8`'s hunt score and target.
- **Data:** `runs/experiments/data/run-exp-fleetphase/` (`orig-v1/`, `report-v1.json`). The remake side
  is the diplomacy run's `remake-05b02936-v1` logs.
- **Release:** [`run-exp-fleetphase`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleetphase).
- **Starts:** the 16 New Game starts, S00–S15 `*_AUTO0720.SAV`, seed 12345, 5 rounds each.
- **Remake:** main `05b02936` (T247 ported the fleet phase).

**Tag:** `[confirmed, partial]`, Wine-only. The 26 differences are not attributed.

**Rerun on remake main `8e2d9053` (2026-10-31):** see [the rerun](2026-10-31-ai-rerun-remake-8e2d9053.md). Still only Carthage fleet 0 differs (27 rows).

**Review note (2026-10-31):**
- **Release integrity:** 162 of 162 files match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain saves myself: **80 of 80** pairs are
  byte-identical. The plain saves are also identical to the diplomacy run's (80 of 80).
- **Comparison rerun:** I ran `runs/experiments/fleetphase/compare.py` from a scratch copy. The output
  is **identical** to `report-v1.json`: 124 same, 26 differ.
- **My own decode** of Carthage fleet 0 in the round-start saves is the section "Round-start state of
  the differing fleet" below.

## Answer

Of 150 AI fleet decisions, **124 are the same**: 87 port and 37 stored route. The branch rule is
F608's:
1. route_x ≥ 0 → the stored route;
2. otherwise, with moves > 0, hunt if the hunt score is > 100;
3. otherwise the port, if there is one;
4. otherwise nothing.

**Not exercised:** no fleet hunted in either game, because every hunt score was −10000 (no
candidate).

**All 26 differences are one fleet:** Carthage's fleet 0, the fleet that sails through
a D174 waypoint in round 1 ([fleet move contract](2026-10-30-fleet-move-contract131.md)). The draft says rounds 2–5, but one row is round 1: S06 r1, where the fleet already stands at (74,71) at its turn. The other 25 are rounds 2–5.

| Pattern | Rows | Original | Remake main |
|---|---|---|---|
| no route in the original | 9 | route_x −1 → **port** | **stored route** |
| route in the original | 9 | **stored route** | **port** |
| no moves in the original | 8 | moves 0 at its turn → nothing | **port** |

So the branch rule agrees wherever both games see the same route and moves. What differs is that one
fleet's route and moves state at its turn, which is the route lifetime of
[#131](2026-10-30-fleet-route-lifetime131.md).

## Round-start state of the differing fleet (review addition, observation)

I decoded fleet 0 (Carthage) in each round's start save: the previous round's hooked autosave, with
the fleet record at army-table end + 2, so +4/+6 is the route and +0xC the moves. The original's
fleet phase runs later in the round, so the save is the state **before** the round's earlier seats.

- **"No route in the original" rows (9):** I decoded 8 of them; the ninth, S06 r1, starts from the New Game start save, which is not in this release. All 8 start saves have **route_x −1** (route_y 76) and moves
  26. The original sees no route, and the remake chooses the stored route. The remake therefore has a
  route that neither the save nor the original's state holds. That points at the remake's side: its
  import of +4/+6 (route_y 76 with route_x −1) or a route it sets earlier in the round. It is not the
  original's route lifetime.
- **"No moves in the original" rows (8):** the saves have moves 26 (in one case route (86,77) and
  moves 4). The original sees **0**, so something in the original spent them earlier in the round.
  The fleet stands at (86,76); an army-phase transport request charging moves (CD08) is a candidate.
- **"Route in the original" rows (9):**
  - In 4 (S06 r3–r5, S08 r2), the save already holds the route, at the fleet's own position (85,78)
    or (86,76), and the remake chooses the port. The remake drops or ignores a saved route.
  - In 5 (S06 r2, S13 r3–r5, S14 r5), the save has route_x −1, and the original sees a route. The
    original wrote it earlier in the round.

These are inferences from the saves, not attributions; the writer hook proposed below is still needed.

## Open

- **Which writer differs:**
  - the round tick's clear (`0x451723`);
  - the arrival;
  - the army phase's transport request (D9A8, through CD08);
  - the remake's import of fleet +4/+6.

  The draft proposes a route/moves hook at those writers on the 26 rounds; the decode above narrows
  where to look.
- **The hunt branch** was not exercised.
- **The port city:** the remake logs the branch, not the city.
- Rounds 6+, other seeds, fleets carrying armies, native Windows.
