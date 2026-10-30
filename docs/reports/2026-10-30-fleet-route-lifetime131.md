# Stored fleet route lifetime and the fleet phase's order (FUN_0044f608): written by the army phase, read once, cleared by the tick

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `d3542f4` (PR #270). It
answers parts 1–2 of research issue
[#131](https://github.com/diegoami/imperial-conquest-2-research/issues/131) (remake
[#1405](https://github.com/diegoami/imperial_conquest_2/issues/1405) and
[#1409](https://github.com/diegoami/imperial_conquest_2/issues/1409)), delegated to conquest on
2026-10-30. Part 3 (the movement and arrival boundary) follows in a separate delivery.
- **Scripts:** `runs/experiments/fleetroute131/{phase.py, scan.py}`.
- **Data:** `runs/experiments/data/run-exp-fleetroute131/` (`phase-v1/v2.json`,
  `scan-v1-public.json`). The full scan stays private, because it includes owner-derived material.

**Tag:** `[confirmed]`: unmodified original instructions in Unicorn, from the fleet174 synthetic
phase inputs and cases derived from them, with the run stopping before naval combat.

**Review note (2026-10-30):**
- **Phase rerun:** I ran `phase.py --version v2` from a scratch copy, with output redirected. It
  reads conquest's private fleet174 inputs and writes nothing there. The result is **identical**
  to `phase-v2.json`. Across all 39 cases there are **0 route writes**, 42 E1FC calls and 30
  Random draws.
- **Scan:** I checked only the public aggregates (corpus 10,105). The scan was not rerun, since it
  reads the owner's private corpus.
- **Privacy note:** conquest reports that its PR #270's first push contained an unredacted scan
  with hash prefixes of owner-derived saves. It was replaced before the squash-merge, so conquest's
  `main` never held it, but the old commit is still reachable through that PR's history. Nothing
  of it is copied here.

## Answer

**1. The route fields** (fleet `+4` = route_x, `+6` = route_y, both signed words):
- **A route is present exactly when route_x ≥ 0.** route_y is meaningful only then.
- **Only the AI army phase writes a route,** through `FUN_0044cd08`:
  - D9A8 writes it for a ferry rendezvous;
  - DBA8 writes it for an army already aboard, as the landing cell.
- **Only F608 reads it, in the same seat.** The round tick sets route_x to −1 and leaves y as it
  was.
- **The fleet phase never writes a route.** In all 39 emulations there was no route write: arrival,
  landing, docking, inland targets, zero moves, negative x, the (0;0) residue, and a fleet already
  on its cell.
- **Consequence for saves:** a route found in a save is never read. Import and export can carry
  `+4`/`+6` as opaque bytes; inactive residual Y is not gameplay state. This is consistent with
  the [SAV atlas](2026-10-21-original-sav-semantic-atlas.md) (`LIVE_AND_RESIDUE`).
  - The public scan found 558 of 44,113 live fleets in saves holding x ≥ 0, which is consistent
    with saves taken mid-turn.

**2. F608's order:** prepass → port pick → **stored route** (followed with any moves) → **hunt**
(needs moves > 0; score strictly above 100) → **port**.
- **The hunt:**
  - It uses 1 Random draw plus one per eligible target.
  - A target is **protected** when a map city code of its owner lies in its 3 × 3 neighbourhood.
  - A tie goes to the first in table order; both orders were measured.
  - It uses the same word store and final add as #130
    ([scorer word storage](2026-10-30-scorer-word-storage130.md)).
- **The port pick runs in two passes.** Pass 2 always runs after a foreign pass-1 port. Cities
  with x > 247, or with x > 213 and y > 98, are never ports.
- **Arrival branches** are read from the disassembly; landing and docking at an own port were
  measured.

Earlier promoted work this builds on, without repeating it:
[`2026-10-24-strategic-fleet-controls174.md`](2026-10-24-strategic-fleet-controls174.md),
[`2026-10-24-fleet-accepted-movement174.md`](2026-10-24-fleet-accepted-movement174.md),
[`2026-10-29-ai-fleet-hunt-absent-in-remake233.md`](2026-10-29-ai-fleet-hunt-absent-in-remake233.md),
[`2026-10-30-ai-fleet-moves-in-play1409.md`](2026-10-30-ai-fleet-moves-in-play1409.md).

## What this does not establish

- **Part 3 of #131:** D174's waypoint choice and the `FUN_0044939c` target replacement (for
  example, why land routes across the coast head east to (74,69)). It follows in a separate
  delivery.
- Naval-combat outcomes.
- Record compaction during the phase.
- Full-seat or global RNG parity.
