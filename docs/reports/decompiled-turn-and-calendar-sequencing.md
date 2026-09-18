# Turn sequencing and the weekly tick, decompiled

The last item in the original decompilation priority queue. `TPremierForm_EndTurn` (the real end-turn handler, distinct from `TToEndTurn_EndTurnOK`'s confirmation-dialog UI code) revealed the nation turn cycle, and following it to `FUN_004514ec` — the function that runs once every full round of nations — revealed the whole weekly economic/calendar tick in one place. This closes several previously-open questions across multiple earlier reports at once.

## Nation turn order and the calendar cycle

```text
TPremierForm_EndTurn:
    nationTurnIndex = (nationTurnIndex + 1) mod 16
    currentNation = turnOrderTable[nationTurnIndex]   // 16-entry lookup table
    if nationTurnIndex == 0:            // completed a full round of all 16 nations
        FUN_004514ec()                  // the weekly tick, below
    <hand control to currentNation>
```

The 16-entry `turnOrderTable` is a **direct identification of one of the "unidentified 32-byte fixed blocks"** from `decompiled-sav-file-layout.md` (32 bytes = 16 × 2-byte nation codes) — it determines which nation goes in which position, not necessarily nation-code order.

Inside `FUN_004514ec`, the week/season/year advance exactly as multiple prior reports had only observed empirically:

```text
week = (week + 2) mod 12
if week == 1:                        // wrapped from 11 back to 1
    season = (season + 1) mod 4
    if season == 0:                  // wrapped from Winter back to Spring
        year -= 1                    // BC year counts down
```

This is an exact, code-level confirmation of the pattern `rome-tax-increase-and-sidon-capture.md` and `diplomatic-reparations-and-more-captures.md` both found only by observing two different season transitions land on the same week-11-to-week-1 boundary — closing the roadmap's original "confirm autumn/winter and year boundaries" item completely, including the year-decrements-on-New-Year behavior that was never directly observed before.

## The weekly tick applies to every city, army, and fleet in the game — not just the ending nation's

`FUN_004514ec` loops all 334 cities, all armies, and all fleets unconditionally, confirming this is a true global weekly tick (runs once, after every 16th nation's turn) rather than per-nation processing:

> **Correction (2026-09-14):** see [`city-population-growth.md`](city-population-growth.md). The city loop below is not population growth. It writes the city's **supply stock** (`+0x18`): `supplies += pop × (seasonValue − 40) / 10`, minus that times the owner's **mobilization** (`+0x442`) `/ 200` (not loyalty), capped at `pop × 10` and floored at 0; a city with a hostile army adjacent cannot gain. The Winter decline is **loyalty −1**, 1 in 3, when the stock is empty; population is not touched. Population grows only in the quarterly `FUN_00451b40`. The "per-season rate table" is the season table at DAT `0x1F7D8` (50/80/80/20), already extracted. Confirmed on 33 save pairs (10,693 of 10,980 city-turns exact).

- **Population growth is seasonal and loyalty-modulated.** Each city's growth increment is computed from a per-season rate table (4 entries), then reduced proportionally to that nation's loyalty (lower loyalty measurably slows population growth). Growth accumulates fractionally rather than jumping every week — consistent with population having been observed to stay exactly frozen across several turns before jumping in earlier reports. **Winter carries a specific population-decline chance**: when a city's growth accumulator bottoms out during Winter, there's a 1-in-3 random chance it loses a population unit instead.
- **Army supply consumption is seasonal and depends on whether the army is stationed at a city.** An army not at any city consumes supply proportional to troop count; an army at a city consumes at a rate modulated by a seasonal table (this is the actual mechanism behind supply drain this project could previously only observe the net effect of, never the rule). Each army's maximum moves for the week is also recomputed here, reduced when a per-army "readiness" value (fed by `FUN_0044a698`, the same helper used in the nation tax-base and mercenary logic) is low.

  > **Correction (2026-09-18):** there is no "readiness" value. **`FUN_0044a698` is the army's total troop count** — it sums `unit[i].troops` across all 20 slots and returns `1` when the total is zero, purely as a divide-by-zero guard for the supply-percentage `IDIV` below it. The recompute is `moves = 10 − min(5, ⌊troops / 20000⌋)` (`0x00451651`), then `−1` (`0x004516D7`) when `⌊supplies × 10000 / troops⌋ < 10`. Army size is the only input; unit-type composition plays no part. Checked against 627 army records in 54 saves. See [army-moves-field-signed-and-the-ffff-underflow.md](army-moves-field-signed-and-the-ffff-underflow.md).
- **Fleet construction countdown and completion, confirmed exactly.** For an under-construction fleet (`X`/`Y` still `(0,0)`), its countdown field decrements — this is the exact field `diplomatic-reparations-and-more-captures.md` had only observed decreasing by 2 per turn and called a "candidate countdown." When it reaches 0, `FUN_0044a050(fleetIndex)` is called — almost certainly the actual "construction complete, place the fleet on the map" step.
- **A weather/storm mechanic for deployed fleets, not previously known at all.** For a fleet already at sea (countdown `== -1`), there's a random chance each week of being "lost at sea" entirely or "damaged in a storm," with worse odds specifically in Winter (a bad-weather value is doubled). This is a genuinely new mechanic this project had no prior evidence for.
- **City-unit `StateCode` increments by exactly 2 per week, capped at 24 — confirmed exactly.** `mobilization-movement-and-city-capture-modes.md` observed a garrison unit's `StateCode` go `8 → 10 → 12 → 14` across turns and called it "a candidate duration counter." This function shows precisely that: every active recruitment slot's state field is incremented by 2 weekly, clamped to a maximum of 24 — meaning **24 is not an arbitrary starting value for a freshly recruited unit, it's the cap a unit's readiness state reaches and holds at** after 12 weeks (matching why freshly-recruited/mobilized units in this project's saves have always read exactly 24).

## Diplomacy and end-turn validation

`TPremierForm_StartTurn` checks, at the start of each nation's turn, whether there's a pending trade or alliance proposal directed at them (comparing against a nation index and proposal-type value) and announces it if so ("*X wants to trade/form an alliance with Y*") — this identifies the other previously-unidentified fixed block from the SAV layout report (the 4-byte block right after the 61-byte-record region) as a pending-diplomatic-offer indicator.

**Update: confirmed against real saves, and the second word decoded.** The block sits 22 bytes before end of file and is `{short proposingNationIndex (0xFFFF = none), short proposedRelationState}`, the second word reusing the relation-matrix encoding (`1` = trade). Two consecutive saves carrying the news "Greece wants to trade with Rome" and "Bythinia wants to trade with Rome" read `07 00 01 00` and `0B 00 01 00`, with nation 7 = Greece and 11 = Bithynia, and the saves either side read `FF FF`. See [pending-offer-block-army-split-and-naupactus.md](pending-offer-block-army-split-and-naupactus.md).

> **Correction (2026-09-14):** "announces" means a modal `MessageDlg(…, mtInformation, [mbOK])` with the text "*X wants to trade with Y.*" or "*X wants to form an alliance with Y.*". It is **not** a news-log line: no save's news log contains "wants" (6 saves hold an offer). The two "news" items quoted above are the dialog text recorded in the session notes.
> - The block is set by `FUN_00452034` at the start of every human seat's turn. It is cleared first, then rolled, then shown by `StartTurn`.
> - The code writes `2` for an alliance offer.
>
> See [`news-log-format-and-messages.md`](news-log-format-and-messages.md).

`FUN_0045af00`, called at the very start of `TPremierForm_EndTurn`, is an end-turn validity check: it scans the current nation's armies and fleets and refuses to end the turn (clears a "ready" flag) if any unit still has moves remaining under certain conditions — the standard "you still have units that can act" guard familiar from turn-based strategy games.

> **Correction (2026-09-18):** `FUN_0045af00` never reads the moves field (`ArmyRecord +6`) at all. The "still has moves" filter is the helper `FUN_0044aab4`, which recomputes the army's full weekly maximum and returns `fullMoves != army[+6]` — i.e. **"this army has not acted at all this week"**. For each such army `FUN_0045af00` then warns on *supply and money*, not moves: `FUN_0045ae68` returns a required-supply and a supply-percentage pair, and the flag is cleared when the percentage is under `0x14` with a further condition, or when the army's **money** (`+12`, `puVar3 + 3`) is below the required amount. The fleet half of the loop is the same shape on the fleet record. The tail (`(&DAT_00474b00)[currentNation * 0x494] == 0` → force ready `= 1`) is what stops the check ever blocking an AI seat, and is one of the four call sites that fix the flag's polarity as *0 = computer-controlled*. This closes the "exact conditions" item below. See [army-moves-field-signed-and-the-ffff-underflow.md](army-moves-field-signed-and-the-ffff-underflow.md).
>
> `FUN_0044aab4` also carries a genuine inconsistency in the original: its low-supply test is `supplies × troops / 10000 < 10`, while the weekly tick that *wrote* the value uses `supplies × 10000 / troops < 10`. The two agree only near 10,000 troops, so the reference value this check compares against is wrong for armies far from that size.

## What this does not establish

- The exact per-season growth-rate and supply-consumption table values (the tables' addresses are known, their contents weren't extracted this pass, unlike the unit-type table which was found in the DAT file).
- Treasury/tax collection's exact location in the weekly tick — `FUN_00451304` (the step right after city/army/fleet processing) turned out **not** to be this; it's a seasonal weather-event system instead. See `decompiled-weather-events.md`.
- ~~The exact conditions in `FUN_0045af00` gating the end-turn refusal.~~ **Closed 2026-09-18** — see the correction above.
- `FUN_0044a050` (fleet construction completion) itself was not decompiled, only inferred from its call site and countdown-reaches-zero trigger.

## Reproduction

Found via the recovered RTTI symbol list (`TPremierForm_EndTurn`, `TPremierForm_StartTurn`), then followed two calls deep to `FUN_004514ec`/`FUN_0045af00` with `ExportAddresses.java`.

## Next checks

1. Extract the per-season growth-rate and supply-consumption tables (`DAT_004794a8`/`DAT_004794a0`, 10-byte stride, 4 seasons) the same way the unit-type table was found in the DAT file, if they live there too.
2. Find the real treasury/tax-collection step in the weekly tick — not `FUN_00451304`, which turned out to be a weather-event system (see `decompiled-weather-events.md`).
3. Test the storm/loss mechanic's odds against a controlled multi-turn save sequence with a fleet at sea over a Winter transition, if one becomes available.
