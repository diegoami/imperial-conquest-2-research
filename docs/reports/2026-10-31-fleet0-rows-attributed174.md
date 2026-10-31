# Carthage fleet 0, attributed: 8 rows are the same outcome, 13 follow a diplomacy divergence, 6 are a port gap (the mercenary run's continuation walk)

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `e3245d4` (PR #294), for
conquest #174, owner request 2026-10-31. It attributes the 27 differing rows of the
[AI fleet phase comparison](2026-10-31-ai-fleets-vs-remake-main.md), as rechecked in the
[rerun on `8e2d9053`](2026-10-31-ai-rerun-remake-8e2d9053.md). Remake: main `8e2d9053`, not released.
- **Original:** `patches/fleetroute_hook.py`, observation-only. Per seat, it logs:
  - the fleet phase's branch inputs (the two probes of `patches/fleetphase_hook.py`);
  - **both writers of a stored fleet route**
    ([route lifetime](2026-10-30-fleet-route-lifetime131.md)): `FUN_0044d9a8`'s ferry rendezvous,
    at `0x44DA74` after its call to `FUN_0044cd08`, and `FUN_0044dba8`'s aboard landing cell, at
    `0x44DBF7`.
- **Runs:** 16 New Game starts (S00–S15 `*_AUTO0720.SAV`) × 5 End turns, seed 12345, the same starts
  as every earlier comparison.
- **Remake:** the same 80 rounds from the original's autosaves. `RemakeAdapter aiprobe ... fleetlog=`
  logs each seat's `OriginalFleetRouteRequested` (its army-phase route writer, T247) and
  `OriginalFleetDecision`.
- **Comparison:** `runs/experiments/fleetroute174/compare.py`, per round, nation and fleet. It sets
  the routes each side's army phase wrote and the fleet branch against the nation's rows in the
  army comparison (`run-exp-airerun/report-aidecide-v1.json`).
- **Data:** `runs/experiments/data/run-exp-fleetroute174/` (`orig-v1/`, `remake-8e2d9053-v1/`,
  `report-routes-v1.json`, `README.md`).
- **Release:** [`run-exp-fleetroute174`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleetroute174).

**Tag:** `[confirmed]`, Wine-only, for the original's side: a hook and the disassembly. The remake
side is its own fleet events plus a code reading; no remake diagnostic was built for the gap.

**Review note (2026-10-31):**
- **Release integrity:** 160 of 160 files match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain autosaves myself: **80 of 80** pairs are
  byte-identical.
- **Comparison rerun:** I ran `compare.py` from a scratch copy of `e3245d4`. The output is
  **byte-identical** to `report-routes-v1.json`: 131 same, 19 route-written.
- **The 27 rows:** I mapped each differing row of the rerun's fleet report onto the route report.
  - 8 are "same" there, and all 8 are original `none` against remake `idle`.
  - The other 19 are route-written: 13 with Carthage army 3 a "diplomacy" row, and 6 without (S06
    r3/r4/r5, S08 r2, S13 r4/r5).
- **Disassembly:**
  - **Both hook sites follow a route write:** `0x44DA74` follows `call 0x44cd08` in `D9A8` and stores
    the route at `[edx-0x6]`. `0x44DBF7` follows the `CD08` call in `DBA8`.
  - **Every rendezvous goes through `DBA8`:** `D9A8`'s only caller is inside `FUN_0044db38`
    (`0x44DB8B`), which `DBA8` calls (`0x44DC26`).
  - **The run is a walk:** `FUN_0044e84c` walks the army itself, through `DBA8` at `0x44E913`.
  - **Then a second walk:** after `call 0x44e84c` (`0x44F485`), `F31C` tests the army score
    `> 0x46` (70) and calls `DBA8` at the army target (`0x44F4A3`). Otherwise it tests the city
    score `> 0x55` (85) and calls `DBA8` at the city target (`0x44F4C7`). So a mercenary run is
    followed by a second walk in the same army turn.
- **S06 round 3, checked:**
  - **Hook log:** the rendezvous writes fleet 0's route (85,78) with the army point (83,84). The
    fleet record that follows has route (85,78), position (85,78) and 26 moves. So the fleet is
    already at the rendezvous, and following the route keeps it there instead of sailing to port.
  - **Saves:** army 3 in `run-exp-aidecide` stands at (86,78), (83,84) and (78,85) at the ends of
    rounds 2, 3 and 4, with 0 moves.
- **Remake code** at `8e2d9053`: `AiMilitaryPhase.cs:389–398`. In `Kind.MercenaryRun`, while
  `MercenaryRunDestination` finds an offer, it adds the run's march and `break`s, so no
  continuation is proposed. The comment reads: "the one march a turn allows an army goes to the run
  while there is an offer to run to".
- **"`D9A8` writes the route whatever the army's moves", supported but not proven (follow-up,
  2026-10-31):**
  - **Code:** on the path `DBA8` → `DB38` → `D9A8` up to the write, I find no test of the army's
    moves (+6). `DBA8` loads them into `si` at `0x44DBC5` but compares them only after the `DB38`
    call (`0x44DC43`). `D9A8`'s own tests are on the fleet (+0x16, +0xA, +0xC). `DB38` compares
    locals I did not trace back.
  - **Play (from ic2-conquest):** in S06 round 4, the remake's identical run walk spends all 9 moves,
    (83,84) → (78,85), with 0 left (`remake-8e2d9053-v1/S06_Gaul_AUTO0720-t04-probe.jsonl`). The
    original's save puts army 3 on the same tile, and its hook logs the rendezvous from (78,85) in
    that seat. So the original very likely wrote the route at 0 moves.
  - Not read: the army's moves at the moment of the write.

## Result: the 27 rows

| Group | Rows | Cause |
|---|---|---|
| "none" against "idle" | **8** | **Not a difference.** The fleet has no route and 0 moves. The original's fleet phase does nothing, and the remake logs that as `idle`. The earlier comparer treated the two labels as different. |
| a route written on one side, during a diplomacy divergence | **13** | **State.** In every one, Carthage's army 3 is a "diplomacy" row in the army comparison: the war with Celtiberia ends after a battle on one side only. |
| a route written only in the original | **6** | **Port gap:** the mercenary run's continuation walk (below). |

- **A "state" example, S00 round 2:** in the original, army 2's battle ends the war, so army 3 has
  no enemy and walks home over land. In the remake the war goes on. Army 3 marches across the sea,
  and its ferry request gives fleet 0 the route (86,76).
- **Every row is a route written by one side's army phase.** The fleet phase itself agrees wherever
  both sides have the same route and moves, as the fleet report found.

## The port gap: after the mercenary run, the original also makes the continuation walk

**Rows:** S06 rounds 3, 4 and 5, S13 rounds 4 and 5, and S08 round 2, all Carthage's army 3 on the
`e84c+city>85` branch. In S06 round 5 the army rows are "state-battle" (a battle earlier in the
round), but the route comes from the same continuation walk.

**Original:**
- The mercenary run walks the army toward the offer.
- Then, in the same army turn, the continuation walk: at the army target if its score is > 70,
  otherwise at the city target if its score is > 85.
- Here the second walk needs a ferry, so `D9A8` writes fleet 0's route from the army's position
  after the run:
  - S06 round 3: army point (83,84), route (85,78);
  - S06 round 4 and later: army point (78,85);
  - S08 round 2: (87,77) → (86,77).
- The army does not move further: the saves show it on the run's last tile.
- The fleet keeps a stored route and follows it instead of going to port.

**Remake:** the run is the same; army-3 walks (86,78) → (83,84) → (78,85) in S06, as in the
original. But no continuation walk follows, so there is no ferry request, and fleet 0 takes the port
branch.

**For the remake (classical-faithful, inference):**
- After the mercenary-run walk, run the continuation walk too, in the same army turn, with the moves
  left and the original's `> 70` / `> 85` tests. That includes any ferry rendezvous it triggers.
- With no moves left, the walk very likely still asks for a ferry (see the review note).

## What this does not establish

- **The continuation walk's effect on the army:** in these rows the army does not move, because it
  is out of moves or waiting for the ferry. A run that ends on land with moves left would also move
  the army. That case did not occur here.
- **The 13 diplomacy rows:** their own causes are the "battle" and "draw" first divergences of the
  [diplomacy comparison](2026-10-30-ai-diplomacy-vs-remake-main.md). They are not re-attributed here.
- **The army order gap** ([army order within a seat](2026-10-31-army-order-within-a-seat.md)) changes
  none of the 27 rows, as drafted: under the table-order diagnostic, the fleet report has the same
  27 rows.
- Rounds 6 and later, other seeds, the hunt branch (no fleet had a hunt candidate), and native
  Windows behaviour.
