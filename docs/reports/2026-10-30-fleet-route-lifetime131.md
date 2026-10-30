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

## Source-precision addendum (2026-10-30, issue #131)

**Tag:** `[code-backed interpretation]`, not a new emulation or game result.
Research re-read the complete original functions below in the local listing and
rechecked its SHA256:
`2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8`.
The following is interpreted functional pseudocode, not original source.
Line references identify that pinned listing. No private saves were inspected and
the existing 39/41 controls were not repeated.

### Port selection: E9A8 and E920

`FUN_0044E9A8` (:52473–52533) returns a **city index through its output**.
`current` means the current AI nation, not a newly derived fleet owner. `distance`
is Chebyshev distance (`FUN_00449018`). City, fleet supply/money and score values
are signed words; compare the strict thresholds below literally. The city scan
is ascending index 0 through 333.

```text
chosen = -1
best = 1000
for city in city-table order:
    own = city.owner == current
    eligible = (own and city.stock > 20) or
               (relation(current, city.owner) < 3 and
                city.stock > 120 and fleet.money > 10)
    if eligible and isPort(city.position):
        score = distance(city.position, fleet.position)
        if own:
            if score == 1 and fleet.supplies > 0:
                score = -1
        else:
            score = signedWord(score + 50)
        if score < best:
            chosen = city.index
            best = score

if chosen == -1 or (city[chosen].owner != current and best > 30):
    best = 1000
    # Keep chosen: the original does not reset the output here.
    for city in city-table order:
        if city.owner == current and isPort(city.position):
            score = distance(city.position, fleet.position)
            if score < best:
                chosen = city.index
                best = score
return chosen
```

The adjacent/supplied `-1` is a **ranking score**, not a no-port return. Supply
means the fleet supply word `+0x0E > 0`, with no per-ship threshold. The money
word is `+0x10`. An own adjacent port with stock > 20 remains the selected city.
The foreign branch needs relation < 3, stock > 120 and money > 10. The literal
second disjunct also permits own cities, but adds nothing to the own stock > 20
branch. Neither pass checks a direct line or a path to the port.

Pass 2 considers every own port regardless of stock, money or fleet supply, uses
raw distance (no adjacent bonus), and retains the foreign result if it finds no
own port. On valid map coordinates foreign distance + 50 is always > 30, hence
the earlier prose that pass 2 always runs after a foreign winner. Both passes
replace only on strict improvement, so the first equal city wins. The 1000
initial ceiling is part of both scans.

`FUN_0044E920` (:52426–52468) means:

```text
isPort(position) =
    any signed map[x + dx, y + dy] < 2 for dx,dy in -1..1
    and not eastern(position)
eastern(x,y) = x >= 248 or (x >= 214 and y >= 99)
```

This includes the centre cell and has no clamp or bounds check in this helper.
The eastern predicate is `FUN_004496BC` (:48187–48197), expressed here for valid
map coordinates. Sea/rough-sea codes 0/1 qualify. Fleet markers >= 300 do **not**
qualify, even though other navigation helpers classify them as sea. This is a
local coastal predicate, not sea reachability.

### CD08: the eastern exception forces continuation from land

`FUN_0044CD08` (:51018–51119) walks the original integer line from its first
point toward its second point, starting with the first sampled step after the
origin. It classifies the origin and each sampled cell as sea exactly when its
signed map code is < 2 or > 299. Normally it accepts another sample while that
classification equals the origin's classification.

**If the origin is land and the sampled coordinate is eastern, it forces the
sample to be accepted even when its map code is sea.** It then records that
sample as the last accepted cell and continues the line. It does not force a
stop, reject the route or change the sea-origin case. The first rejected sample
and the last accepted sample are returned separately. If no sample was accepted,
only the last-accepted X is initialized to -1; its Y remains stack residue.
There is no stop-at-requested-target check in CD08: its stopping condition is the
first rejected sample. If every sample through the requested endpoint is accepted
(including eastern sea for a land origin), CD08 continues beyond that endpoint;
it does not return the requested point merely because it was reached. When a
later sample is rejected, output 3 is the last accepted point and output 4 is
that first rejected point. If no sample is ever rejected, this body establishes
no normal return or output assignment. Coincident or out-of-map histories are
not newly resolved by this reading.

These details refine the same-seat D9A8/DBA8 route producers only. They do not
establish execution of saved routes, wider ferry/capacity behavior, a full-seat
result, naval combat or native Windows acceptance.

## CD08 caller direction and output assignment (2026-10-30)

**Tag:** `[code-backed interpretation]`, same listing pin as the source-precision
addendum, SHA256 rechecked. Research read complete D9A8 (:51665–51710) and DBA8
(:51792–51846), including their CD08 calls. No new instruction replay or game run.
`lastAccepted` and `firstRejected` below name CD08's third and fourth outputs.

| Caller | First point → second point | lastAccepted output | firstRejected output |
| --- | --- | --- | --- |
| D9A8, nonadjacent selected ferry (:51704–51706) | army position → selected fleet position | army approach, also copied into the caller's target local | fleet route (+4/+6) |
| DBA8, embarked army (:51815–51818) | requested target → carrier position | fleet route (+4/+6) | temporary local, not used afterward |

D9A8's separate distance-exactly-1 branch calls B79C to board and sets approach X
to -1; it does not call CD08 in that branch. If no eligible ferry was found,
D9A8 does not initialize a new output itself. For its nonadjacent CD08 call,
there is no requirement that the last accepted approach X be nonnegative before
the first rejected cell is written to the fleet route. Thus an immediate
land-to-sea mismatch can produce approach X = -1 and a valid first-sea fleet route.

DBA8 does **not** reverse this line to scan from the ship. With an ordinary land
requested target and an immediately rejected first sea sample, CD08 writes fleet
route X = -1; the route Y is residue because CD08 initialized only the X word of
its last-accepted local. This does not create an active route. Immediately after
CD08, DBA8 subtracts **two army moves unconditionally**: no successful-route,
positive-budget or distance guard intervenes. The signed-word underflow behavior
is the already documented original behavior, not a new policy correction. The
embarked branch does not execute DBA8's separate land-army walker/fallback/recursion.

For either caller, accepting every sample up to the second point does not finish
CD08. The helper has no endpoint comparison and continues sampling beyond that
point until the medium/eastern test rejects a cell. There is no separate
all-accepted-path success return. This source reading does not establish safe
out-of-map or coincident-input behavior. Directional integer-line rounding must
therefore be preserved; reversing the inputs or substituting the other output
is not equivalent to the original calls.
