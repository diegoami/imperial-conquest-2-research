# The strategic AI turn, decompiled: `FUN_0044fa20` and its four phases

**The question** (imperial_conquest_2 #816, recorded in `docs/pending-requests.md`): what does the
original do when a computer seat takes its turn — the shape of the turn, recruiting and mobilisation,
movement destinations, attack and siege choices, defence and supply, and where randomness and
human-versus-AI asymmetries sit. The clone's AI is designed, not the original's (27 `[designed]`
weights in its ruleset `ai` block); this report is the original's side of that comparison.

Everything here is read from `%LOCALAPPDATA%\ReTools\all_app_functions.txt` (line references `:n`).
Ghidra was not re-run; no listing was taken, so instruction-level claims keep the dump as their only
source. Field names reused from earlier reports (army `+0x0A` supplies, fleet `+0x14` condition,
city `+0x1A` fortification, nation `+0x44A` tax rate, …) carry those reports' confirmations; names
new to this report are tagged `[derived]`.

## Answer

- **A computer seat's turn is four fixed phases, per nation, in this order: diplomacy, economy,
  armies, fleets** (`FUN_0044fa20`, :53208). Within the army and fleet phases the loop is per unit,
  in table order, each unit decided and moved once `[confirmed: decompile]`.
- **The economy phase is a threat budget plus a tax policy.** It sums a threat (wars, enemy army
  values, proximity to the capital) against own strength (allies, own armies), spends the deficit
  through the known recruit-and-mobilise routine, and — on the last week of every season only —
  adjusts the nation's tax rate up or down `[confirmed: decompile]`.
- **Armies move to a scored destination, decided per army**: intercept homeland threats first, then
  a target-priority tree between attacking an enemy army, attacking an enemy city, defending or
  resupplying, and running to hire mercenaries. The "destination" call is itself the mover: it walks
  the army step by step, spending moves, resolving attacks when it bumps an enemy at war
  `[confirmed: decompile]`.
- **Fleets resupply and repair at ports, then either hunt an enemy fleet (scored) or sail to a
  port city** (own under-supplied port first, a rich foreign port if close, else the nearest own
  port). Contact with an enemy fleet at war resolves as the instant naval battle `[confirmed:
  decompile]`.
- **The AI's resupply and purse rules are the interesting part**: armies and fleets top their purses
  up from the national treasury at own cities (army purse held between 500 and 1000), buy supply
  from foreign non-war cities at ⅕ talent per ton, repair fleet condition at own ports, and **the
  AI hires mercenaries for free** — the only gate is army money > 50 `[confirmed: decompile]`.
- **Six asymmetries against the human** are collected in §7, three of them new to this report
  (auto-tax, free mercenary hires, the AI's deficit-recruitment floor) `[confirmed: decompile]`.

## 1. The turn's shape [confirmed: decompile]

`TPremierForm_EndTurn` advances the seat index, reloads `DAT_004a0320` (current nation) from the
16-entry turn-order table `DAT_0049efe8`, and calls `FUN_00451fdc` when the wrap lands on seat 0
(the weekly tick `FUN_004514ec` runs there; already confirmed in
[decompiled-turn-and-calendar-sequencing.md](decompiled-turn-and-calendar-sequencing.md)). What that
report did not spell out is the seat loop itself:

```text
FUN_00451fdc (:54939):
    FUN_0044adb0()                          // compact dead armies and fleets (owner == -1)
    while (not game-over && current seat is computer):     // +0x490 == 0
        if (!FUN_00449050()) break           // no human seat left in the game at all
        FUN_0044adb0()
        FUN_0044fa20()                       // one computer seat's turn, then it advances the seat
    if (current seat is human):
        FUN_00452034()                       // human turn start (offer roll; known)
```

- `FUN_00449050` (:47751) scans all 16 `+0x490` flags and returns true if **any** human seat
  remains. A game whose humans are all eliminated runs computer turns with no break condition
  beyond game-over `[confirmed: decompile]`.
- `FUN_0044fa20` itself (:53208) is guarded by `unity (+0x440) > 0` — an eliminated nation's seat
  advances silently — and after the four phases it advances the seat index itself, so one call is
  exactly one seat:

```text
FUN_0044fa20 (a computer seat's turn):
    if (unity > 0):
        TPremierForm_SetTurnTitle
        FUN_0044fb7c()      // 1. diplomacy            (known: war/trade/alliance writes)
        FUN_0044ffbc()      // 2. economy: threat budget, recruit, tax, build, consolidate, merge
        FUN_0044f31c()      // 3. armies:  homeland dispatch, resupply+hire, target, move
        FUN_0044f608()      // 4. fleets:  resupply+repair, hunt or port, move
    advance seat index; on wrap, weekly tick
```

`DAT_004a0340` is set to 0 at the top of the army phase and 1 at the top of the fleet phase — a
global "which phase am I in" mode flag the movement helpers read `[confirmed: decompile; the readers
were not traced]`. There is no planning pass and no re-evaluation loop: each army is scored against
the state as left by the previous army, in table order.

## 2. The economy phase: `FUN_0044ffbc` [confirmed: decompile]

### 2.1 The threat budget

```text
threat = 15000 × (number of nations at war with me)
       + Σ FUN_0044a8cc(a)  over every army of a nation at war with me
       + Σ value/4 over foreign armies within 10 of my capital (+0x444 city)
       + Σ value/2 over armies at war within 20 of my capital          // both sums rounded down
own   = 6000 × (number of allies)
       + Σ FUN_0044a8cc(a)  over my armies
       + Σ value/2 over allied armies
if (own < threat): FUN_004504f4(threat − own)
```

`FUN_0044a8cc` is the per-type AI combat value already identified
([decompiled-mobilization-and-mercenary-restock.md](decompiled-mobilization-and-mercenary-restock.md)
§4: `(troops/100) × DAT_00478FD6[type]`). Distances are Chebyshev from the capital city.

### 2.2 Recruit and mobilise: `FUN_004504f4` — the three gates not in the earlier report

The mobilisation report covered this routine's passes; three gates are added here (:53730–53834):

- **Deficit spending is allowed**: a new order may be placed while `treasury > wealth(+0x430) /
  −500`, i.e. the treasury may go up to `wealth/500` into the red; below that floor an AI may still
  place **at most 3 orders per turn** (`sVar9 < 3`).
- **At most 8 new orders per turn** (`sVar9 < 8`), each charged `(troops/200) × initialPrice[type]`
  exactly like the player's dialog, each raising mobilisation by the identical increment.
- The orders' **city** comes from `FUN_004502e0` (:53626): the capital by default; when at war, an
  own army sits within 15 of the capital, and more than a third of all queued orders already sit at
  the capital, new orders go instead to the own city with **fortification ≥ 75** that has fewer
  queued orders than the capital and lies nearest to an enemy capital `[confirmed: decompile]`.

`FUN_004501f4` (:53579) fills each order: unit type by `Random(100)` buckets — Foot < 35, Guards
35–59, Bowmen 60–74, Lancers 75–89, Dragoons 90–99 — and troops `= standardSize/3 +
Random(standardSize × 4/5)` rounded down to a multiple of 100 `[confirmed: decompile]` (the buckets
were already confirmed via the mercenary restock report).

### 2.3 The tax policy: week 11 only, on `+0x44A`

The block runs only when `DAT_004a0330 == 0xb` — the last week of the season, immediately before
the quarterly tick (`(week+2) mod 12 == 11` in the weekly tick's own numbering):

> **Placement, corrected in play (2026-10-07):** at save granularity the write lands **one weekly
> tick earlier than "immediately before the quarterly tick" reads**: the new tax is already in the
> **week-11 save** (the transition week 9 → 11), and the week-11 → new-season transition (the
> quarterly tick itself) carries no tax write. The block therefore fires during the end-of-turn
> processing leading INTO week 11 — consistent with §1 if the weekly tick runs at the seat-0 wrap
> before the AI seats act, so their economy phases see the counter at `0xb`. See
> [2026-10-07-ai-turn-corroboration.md](2026-10-07-ai-turn-corroboration.md).

```text
if (unity < 650  or  treasury > wealth/2000):   tax = max(5, tax − 6)
if (treasury < 0  or  (own ≤ threat and treasury < 1000)):
                                                tax = min(40, tax + 9)
if (treasury > 0 and unity < 500):              tax = 0
```

`+0x44A` is the tax-rate field the human sets through the Taxation slider (0–40,
[2026-10-02-unit-map-mouse-orders-and-tax-range.md](2026-10-02-unit-map-mouse-orders-and-tax-range.md));
the AI writes the same field itself, once per season. The cuts respond to low unity or a treasury
that is large relative to wealth; the raise responds to deficit, or to being threatened while
nearly broke; a very low-unity nation with money zeroes its tax `[confirmed: decompile]`.

**Corroborated in play** (2026-10-07, [2026-10-07-ai-turn-corroboration.md](2026-10-07-ai-turn-corroboration.md),
Wine-only): across two season boundaries the three rules reproduce **18 of 18 decidable
nation rows** (raise decided by `treasury < 0` or blocked at `≥ 1000`; the 12 rows where only
the threat budget could add `+9` are consistent with and without it), **no AI tax moves at any
non-week-11 transition**, and the human seat never auto-taxes (cut trigger held, tax unchanged).
The zero rule never triggered (no nation's unity fell below 500) and stays `[derived]`.

### 2.4 The four tail sub-phases

| Call | What it does | Gates |
| --- | --- | --- |
| `FUN_00450768` (:53838) | **order a new fleet** at a port: ships `= min(100, cities + 50)` `[derived: the size parameter's meaning]` | fleet count < 99, treasury > 3000, and fleet score (own fleet +1, at sea +4) is 0, or 1 with > 50 cities, or 2 with > 100 cities. Port from `FUN_004496e0`: own coastal city with a free adjacent water cell, nearest the capital, not already hosting a construction order |
| `FUN_00450858` (:53884) | **consolidate army units**: a regular unit (origin label 0) below ⅔ standard size merges with the next same-type slot below ⅓ (quality averaged); a mercenary unit below ⅙ standard is disbanded | per unit slot, all own armies |
| `FUN_004509f0` (:53949) | **merge two armies**: the smaller (< 20,000 troops, not aboard a fleet, with orders outstanding) is absorbed by an own army within 18, if combined slots < 20 and target < 80,000 troops and not aboard; purses and supplies carry over | **one merge per turn** |
| `FUN_00450b30` (:54002) | **merge two fleets**: an idle fleet (ships < 40, no army aboard, no destination) absorbs… is absorbed by an own fleet within 34 if combined ships < 100 and the target is free the same way | **one merge per turn** |

## 3. The army phase: `FUN_0044f31c` [confirmed: decompile]

### 3.1 Homeland defence dispatch: `FUN_0044efc8` (:52776)

First, a list of up to 9 **threatening armies**: foreign, in the capital's region (the region and
coast boxes of `FUN_0044eb18`), within 20 of the capital if at war, within 10 otherwise. Then up to
`threats + 2` of the nation's armies that still have moves and are not committed to a reachable
attack (no army or city target scoring ≥ 100 reachable this turn, or the capital within 3× their
moves) are dispatched: toward the nearest threatening army if it is at war and on land, otherwise
back to the capital. A threat that is aboard a fleet cannot be intercepted — the responder goes to
the capital. **Correction (2026-10-09):** a threat whose owner is not at war is accepted only by a
responder at least 20 from the capital (`cmp [esp+6], 0x14` at 0x44f257). The dispatch was seen
in play: 102 dispatches toward an enemy army, and 7 sent home under that rule. Details in
[`2026-10-09-ai-intercept-and-fleet-hunt-in-play.md`](2026-10-09-ai-intercept-and-fleet-hunt-in-play.md).

### 3.2 Per army: resupply and hire — `FUN_0044e41c` (:52218), every own army

For each of the 334 cities within Chebyshev 4 of the army:

- **Own city** (`FUN_0044f6d8`, :53077): the army takes
  `min(troops/100 − supplies, city supply stock)` tons free; its purse is then normalised against
  the national treasury — surplus above 1000 deposited, and below 500 topped up by 500 while the
  treasury is positive. This is the mechanism behind the army-purse 1000 cap of
  [2026-10-05-army-purse-writes-and-the-1000-cap.md](2026-10-05-army-purse-writes-and-the-1000-cap.md).
- **Foreign city not at war**: the same tonnage is *bought* — capped at `money/5`, paid at
  `amount/5` talents into the city owner's national treasury.
- **Mercenaries**: while at war, army money > 50, the city not at war, a free unit slot, and an
  unidentified byte at army `+0x274` clear — every live pool offer whose `(x, y)` is this city's is
  hired outright: label, name, type, troops and quality copied into the slot, pool slot emptied.
  **No price is paid** — money > 50 is a gate, not a charge, exactly as the human's hire turned out
  to be ([2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md](2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md)),
  but the human's gate is the full price and the AI's is 50 talents flat.
  **Corroborated in play** (2026-10-07, [2026-10-07-ai-turn-corroboration.md](2026-10-07-ai-turn-corroboration.md)):
  Gaul hired one offer (Felsina) and Carthage hired **both** Theveste offers in a single army-turn
  — the "every live offer" loop — with army money and treasury unchanged to the talent.
  The `+0x274` gate itself remains unopened.

### 3.3 Per army with moves: the target tree

Three scorers run per army (`FUN_0044f31c`, :52919–52971):

- `FUN_0044e670` (:52307) — **resupply/defence city**: an own city whose supply stock is below the
  army's strength (`troops/100`), or (only while at war) a foreign non-war city with stock above
  strength + 80 and `money > strength/5`; own cities score −20 if they are a capital
  (`FUN_0044b8d0` — see §5), foreign +20. If nothing qualifies or the best foreign city is beyond
  15, fall back to the nearest own city.
- `FUN_0044ece4` (:52655) — **best enemy city to attack** (cities of nations at war, reachable by
  land or because the nation owns a fleet, `FUN_0044cab4`):

  ```text
  score = strength×110 / cityDefense − distance      // strength = FUN_0044a930, §5
  score −= score/2 if the city is in another region
  score ×2 if cityDefense < strength and distance < 7
  score ×2 if the city is a capital and cityDefense×⅔ < strength
  return (city, score + distance, distance)
  ```
- `FUN_0044ee60` (:52715) — **best enemy field army** (on land, at war, reachable): the same
  `strength×110/theirStrength − distance`, halved across regions, capped at 1000, **+1000** when
  the enemy is weaker and within 7.

The decision, with `moves` the army's remaining moves:

```text
if (armyScore < 100                                        // no worthwhile army target
    or (supplies < 1 and morale < 60 and armyDist > 8)      // demoralised, can't reach
    or (cityScore > 100 and cityDist < moves and armyDist > 2×moves)):   // city is the better buy
    if (cityScore < 100 or (supplies < 1 and cityDist > 19)):
        if (troops/500 < supplies and a city target exists):
            FUN_0044e84c(army)                             // run to hire mercenaries, §3.4
            then: defend the resupply city (armyScore < 71 and cityScore > 85),
                  or still chase the army target (armyScore ≥ 71)
        else: move to the resupply/defence city
    else: attack the city
else: attack the army target
if (FUN_0044aab4(army) == 0):                              // the army did not actually move
    FUN_0044ebe8(army)                                     // garrison fallback, §3.5
```

### 3.4 The mercenary run: `FUN_0044e84c` (:52382)

When an army is well supplied relative to its size (`troops/500 < supplies`) but has no attractive
combat target, it walks the 50 live pool offers (records 201–250 of the 251-entry table at
`0x0049D0A4`, matching [decompiled-mercenary-offer-list-and-position.md](decompiled-mercenary-offer-list-and-position.md)),
keeps those within 20 whose nearest city's owner is not at war, and moves to the nearest one —
arriving to hire it through §3.2 `[confirmed: decompile]`.

### 3.5 Movement is the destination call: `FUN_0044dba8` (:51790)

`FUN_0044dba8(army, xy)` does not store a waypoint; it **moves now**: it computes the next path step
(`FUN_0044db38`), executes it (`FUN_0044d734` — the move step that resolves contact with an enemy
army or city as battle or siege only at `rel == 3`, per
[decompiled-ai-offers-to-human-seats.md](decompiled-ai-offers-to-human-seats.md) §4 and the
capture reports), spends a move, and recurses while moves remain and the target is farther than 1.
An army **aboard a fleet** (covered `+0x08 == -1`) instead drives the fleet: `FUN_0044cd08` moves
the fleet toward the target and the order costs the army 2 moves `[confirmed: decompile]`.

`FUN_0044aab4` (:49315) returns `recomputedFullMoves != army[+6]`; the phase reads it as "did this
army actually move". An army whose whole tree produced no movement gets `FUN_0044ebe8` (:52599): if
some own army is already within 10 of the capital, go to the nearest city of any owner; otherwise
go to the capital `[confirmed: decompile]`.

## 4. The fleet phase: `FUN_0044f608` [confirmed: decompile]

For every own launched fleet (construction countdown `+0x0A == -1`) with no pending destination
(the packed `xy` at `+0x4`, read as "no destination" when negative `[derived]`):

1. **Resupply and repair** — `FUN_0044e5dc` (:52278) for each city within 4, then
   `FUN_0044f7e4` (:53120):
   - own port: take `min(ships×8 − supplies, city stock)` tons free; purse topped to 100 from the
     treasury when below 100 and the treasury exceeds 100; **condition repaired** — below 95 it is
     restored to 100 for `(100 − condition) × ships / 5` talents (this can drive the treasury
     negative), or for a flat 100 talents when the treasury is above 100;
   - foreign non-war port: buy tons at `amount/5`, paid to the port owner's treasury.
2. **Pick a port** — `FUN_0044e9a8` (:52471): own coastal city with stock > 20 (score = distance,
   −1 to dock when already adjacent and supplied), or a foreign non-war city with stock > 120 and
   money > 10 at distance + 50; fallback: the nearest own coastal city. All candidates must be
   reachable by sea (`FUN_0044e920`: water in the 3×3 around the city and a sea path exists).
3. **Hunt** — `FUN_0044f4f8` (:52976): the best enemy fleet at sea, not docked at its own city
   (`FUN_004494e4`, the same predicate behind refusal R07), scored
   ~~`myStrength×100/theirStrength − distance`, doubled when the enemy is weaker and within 18.
   Score ≥ 100: chase it.~~ **Corrected 2026-10-09:**
   - Candidates are ranked by `my×100/their − d`, doubled when the target is weaker and
     `d < 18`.
   - The chosen target's `d` is then **added back** (0x44f5f4), so the score tested is
     `my×100/their`, or `2 × (ratio − d) + d` for a weaker target closer than 18.
   - Score **> 100** (strictly): chase it. Otherwise: sail to the port from step 2.
   - Distance ranks the candidates but does not stop a hunt: AI fleets were seen chasing across
     26-181 tiles.
   - A fleet that already has a stored destination (for example, called as a ferry by an army)
     sails there, with no hunt or port choice.
   Seen in play: [`2026-10-09-ai-intercept-and-fleet-hunt-in-play.md`](2026-10-09-ai-intercept-and-fleet-hunt-in-play.md).
4. **Move** — `FUN_0044e1fc` (:52115), the fleet's `FUN_0044dba8`: walks the sea path spending
   moves; on the final step, a land cell disembarks the carried army (for a computer nation the
   free cell is picked automatically, `FUN_0044b840`), a **city** cell resupplies through
   `FUN_0044f7e4` when not at war, and an enemy **fleet** at war resolves through `FUN_0044b5d0`
   (:49885): two `FUN_0044aa54` strength draws, the loser's fleet deleted, ± half the loser's ships
   of unity, and the "*X sinks fleet of Y.*" news line.

## 5. The scorers' arithmetic [confirmed: decompile]

- `FUN_0044a930(army)` — assault strength: `Σ troops ×3 for type 2 (Bowmen), else ×1`, divided by
  80, times morale. The Bowmen triple weight is read literally; no design intent is argued.
- `FUN_0044a98c(city)` — city defense:
  `loyalty(+0x16)×150 + fortification(+0x1A mod 100)×250 + population(+0x1C)×200`, ×5/3 for a
  capital with loyalty > 59, ×⅘ when the owner is not the original owner, plus half the troops
  queued in recruitment slots at that city.
- `FUN_0044aa54(fleet)` — fleet strength: `ships × condition / 10`, plus the carried army's assault
  strength / 50, **plus `Random(4) × value/10`** — every evaluation of a fleet's strength, including
  both sides of a naval battle, carries a fresh 0–30 % jitter. *(Corrected 2026-10-09: exactly
  `v + Random(4) × (v div 10)`, rounded as written; the carried army's term uses its morale at the
  moment of evaluation: [`2026-10-09-ai-intercept-and-fleet-hunt-in-play.md`](2026-10-09-ai-intercept-and-fleet-hunt-in-play.md).)*
- `FUN_0044b8d0(city)` — the city is **some nation's capital** (a scan of all 16 `+0x444` fields).
  This corrects nothing published (it had not been named), but it is what the "×2 on a weak
  capital" and "prefer defending capitals" modifiers key on, and it is why capitals never defect in
  the quarterly rebellion.
- `FUN_0044cab4(army, xy)` — reachable: true if the nation owns any fleet, or both endpoints are in
  the same region box (`FUN_0044eb18`).

## 6. Randomness in the AI turn

| Draw | Where | Rate |
| --- | --- | --- |
| `Random(10)` | war declaration | 1/10 per turn, at most one |
| `Random(20)` | alliance formation | 1/20 per turn |
| `Random(16)`, `Random(3)` | human-side offer roll (`FUN_00452034`) | not AI-turn proper |
| `Random(100)` | new order's unit type | buckets 35/25/15/15/10 |
| `Random(std×4/5)` | new order's troop count | uniform addend over ⅘ of standard size |
| `Random(4) × (v div 10)` *(corrected 2026-10-09)* | every fleet-strength evaluation | 0–30 % jitter, both sides of a battle |

Two interactions with earlier findings: the post-battle treaty **reseeds the global RNG**
(`RandSeed := winner + loser`,
[decompiled-war-cascade-and-peace-paths.md](decompiled-war-cascade-and-peace-paths.md) §4), so AI
draws after a treaty repeat deterministically; and the human seat's offer roll shares the same
global stream, so AI draws shift a human offer's outcome and vice versa `[derived]`.

## 7. Human-versus-AI asymmetries

| # | Asymmetry | Source |
| --- | --- | --- |
| 1 | mobilisation-receiving radius 5 vs 1; new army 1 move vs 0 | known, [decompiled-mobilization-and-mercenary-restock.md](decompiled-mobilization-and-mercenary-restock.md) §3 |
| 2 | AI mobilises only fully ready slots (state 24) vs player 16 | known, ibid. §4 |
| 3 | end-turn warning never blocks an AI seat | known, [army-moves-field-signed-and-the-ffff-underflow.md](army-moves-field-signed-and-the-ffff-underflow.md) |
| 4 | **the AI changes its own tax rate weekly (week 11); the human only via the slider** | this report §2.3 |
| 5 | **the AI hires mercenaries with no charge (gate: army money > 50); the human's gate is the full price** | this report §3.2 |
| 6 | **the AI's recruitment is gated by a deficit floor (`treasury > −wealth/500`, else max 3 orders) — the human's dialog has no affordability check at all and can drive the treasury arbitrarily negative** | this report §2.2; 2026-09-29-which-cities-may-recruit-and-troop-amounts.md |

(Correction, 2026-10-07, from the spec's cross-family review: the human's `TArmyRecruits_RecruitUnit` has **no
treasury check at all** — it charges `(troops/200) × initialPrice` and the treasury simply goes negative
([2026-09-29-which-cities-may-recruit-and-troop-amounts.md](2026-09-29-which-cities-may-recruit-and-troop-amounts.md));
the deficit floor exists only in `FUN_004504f4` `[confirmed: decompile]`. A disembarking
computer fleet also picks its landing cell automatically (`FUN_0044b840`), where a human clicks.)

## 8. What a reimplementation needs

The engine's AI (`src/IC2.Engine/Ai/`, read-only here) already reproduces the two unconditional
passes — `AiMercenaryHirePass` documents itself as "reproduces the original's single `FUN_0044E41C`
step" and `AiResupplyPass` the fleet half — but the rest is a designed greedy candidate loop with a
`MaxActionsPerTurn` cap and tie-breaking randomness. The original's shape differs on points a
faithful mode would need:

1. **Fixed phase order** (diplomacy → economy → armies → fleets), per-unit in table order, no
   candidate re-scoring loop and no action cap; "did it move" (`FUN_0044aab4`) is the only
   re-trigger.
2. **The threat budget** (§2.1) as the recruit-and-mobilise driver, with the deficit floor and the
   8-order cap.
3. **The week-11 tax policy** (§2.3) writing `+0x44A` directly.
4. **The army decision tree** (§3.3) with its exact thresholds (100 / 85 / 71 / distance terms) and
   the mercenary run, and the fleet hunt/port choice with the 100-score boundary (strictly above 100, with the distance added back: see the §4 correction).
5. **Free AI mercenary hires** and **free-for-100-talents fleet repair**, if fidelity is the goal —
   both are quirks, and §7 makes them explicit rather than accidental.

## What this does not establish

- **Two of the four in-play checks are now corroborated** (2026-10-07,
  [2026-10-07-ai-turn-corroboration.md](2026-10-07-ai-turn-corroboration.md)): the week-11 tax
  moves (§2.3, with the placement correction above) and a free AI mercenary hire (§3.2, two
  natural observations incl. a double hire, no payment anywhere in the diff). Still not observed
  in play: an intercept dispatch (§3.1), a hunt-vs-port fleet decision (§4). Everything else
  remains decompile-only (`[confirmed: decompile]` means the dump, not a listing or a save). **Both seen since** (2026-10-09, an inert hook over 144 End turns, 457 decisions): [`2026-10-09-ai-intercept-and-fleet-hunt-in-play.md`](2026-10-09-ai-intercept-and-fleet-hunt-in-play.md).
- **The `FUN_0044d734` contact resolution question is now settled** (2026-10-07,
  [2026-10-07-ai-mover-contact.md](2026-10-07-ai-mover-contact.md)): the AI mover and the human
  mover share the resolver; the AI-mover army-tile branch resolves instantly through
  `FUN_0044aee4` whenever both seats are computer (no battle screen), and the
  human-involved branch opens the tactical battle. The clone's faithful-AI path can therefore
  share one contact resolver with the human twin (the design goal of the pending request that
  named this gap).
- **`FUN_0044a004`** (the fleet order itself) and the `+0x274` byte gate on mercenary hires were
  not opened; the fleet-size parameter's meaning is `[derived]`.
- **The `+0x4` packed fleet destination** and the marker-range arithmetic in `FUN_0044e1fc`'s final
  step are read at decompile granularity only.
- The **Bowmen ×3** assault weight is literal; whether it is a design choice or a decompile
  artefact of the type encoding is not argued.

## Reproduction

```bash
# All functions cited, from the whole-application dump:
D="$LOCALAPPDATA/ReTools/all_app_functions.txt"   # WSL: /mnt/c/Users/diego/AppData/Local/ReTools/
# turn shape:  :54939 FUN_00451fdc, :47751 FUN_00449050, :49537 FUN_0044adb0, :53208 FUN_0044fa20
# economy:     :53459 FUN_0044ffbc, :53730 FUN_004504f4, :53579 FUN_004501f4, :53626 FUN_004502e0
#              :53838 FUN_00450768, :53884 FUN_00450858, :53949 FUN_004509f0, :54002 FUN_00450b30
# armies:      :52899 FUN_0044f31c, :52776 FUN_0044efc8, :52218 FUN_0044e41c, :52307 FUN_0044e670
#              :52655 FUN_0044ece4, :52715 FUN_0044ee60, :52382 FUN_0044e84c, :52599 FUN_0044ebe8
#              :51790 FUN_0044dba8, :49315 FUN_0044aab4, :53077 FUN_0044f6d8, :53161 FUN_0044f8fc
# fleets:      :53028 FUN_0044f608, :52278 FUN_0044e5dc, :53120 FUN_0044f7e4, :52471 FUN_0044e9a8
#              :52976 FUN_0044f4f8, :52115 FUN_0044e1fc, :49986 FUN_0044b840, :49885 FUN_0044b5d0
# scorers:     :49220 FUN_0044a930, :49249 FUN_0044a98c, :49296 FUN_0044aa54, :50015 FUN_0044b8d0
#              :50856 FUN_0044cab4, :48549 FUN_00449cd8, :48200 FUN_004496e0
```

Record layouts are the established ones: army 656 bytes (`+0x0A` supplies, `+0x0C` money, `+0x0E`
morale, `+0x10` unit slots, `+0x290` stride), fleet 26 bytes (`+0x0A` countdown, `+0x0C` moves,
`+0x0E` supplies, `+0x10` money, `+0x12` ships, `+0x14` condition, `+0x16` carried army), city 34
bytes (`+0x12` owner, `+0x16` loyalty, `+0x18` supply stock, `+0x1A` fortification, `+0x1C`
population), nation (`+0x430` wealth, `+0x438` treasury, `+0x440` unity, `+0x442` mobilisation,
`+0x444` capital, `+0x44A` tax, `+0x490` computer flag). Engine sources read at
`src/IC2.Engine/Ai/AiTurn.cs` (doc comment) only. Nothing from the game was copied into a
repository.
