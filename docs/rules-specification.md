# Imperial Conquest 2 — rules specification

One consolidated specification of the original game's rules, distilled from the individual
reports in [`docs/reports/`](reports/). This is the roadmap §3 deliverable: every rule with its
source, tagged, with guesses excluded.

**How to read this document.**

- Every rule carries the strength tag its source report gave it: `[confirmed]` (code and/or
  controlled observation), `[confirmed: code]` / `[confirmed: decompile]` (read from the
  decompilation; listing or in-play corroboration may still be owed), `[derived]` (follows from
  confirmed rules), `[Wine candidate]` (observed under Wine only). Where a number is exact, the
  formula is given as the code computes it.
- Each rule ends with its source report in parentheses; the report is the authority, this file
  only consolidates. Where two reports disagreed, the later correction is stated and both are
  named.
- Rules the reports leave open are listed per section under **Open:** — they are questions, not
  specifications, and a reimplementation must not silently invent them.

**Record layouts** (bytes, from `decompiled-sav-file-layout.md`, exact): map 320×140 words
(89,600 bytes); 334 city records × 34 bytes; army count word; army records × 656; fleet count
word; fleet records × 26; 16 nation records × 1,172; 50 mercenary slots × 12; the 61-byte
records; fixed tail including the 16-entry turn-order table and the pending-offer block.
Field offsets are given in the sections that use them and in the individual reports.

**Contents**

1. Turn sequence, calendar, and the weekly tick
2. Economy, taxation, and the quarterly tick
3. Cities, the map, capture and defection
4. Recruitment, mobilisation, and mercenaries
5. Armies: records, movement, supply, and purses
6. Fleets and naval warfare
7. Diplomacy and war
8. Tactical battle
9. The computer seat's turn
10. Victory, defeat, and the player interface

*(assembled 2026-10-07 from the 111 reports in `docs/reports/`; the decompilation plan's
priority queue is closed, so every subsystem now has code-level rules available)*

## Turn sequence, calendar, and the weekly tick

### Seat and turn order

- On End turn, the game advances `nationTurnIndex = (nationTurnIndex + 1) mod 16` and sets `currentNation = turnOrderTable[nationTurnIndex]` — a 16-entry lookup table of 2-byte nation codes that determines which nation goes in which position, not necessarily nation-code order. When `nationTurnIndex == 0` (a full round of all 16 nations completed), the weekly tick `FUN_004514ec` runs before control passes on. [confirmed: code] (decompiled-turn-and-calendar-sequencing.md)
- New Game builds the order in `FUN_00448AA4`: the 16 shorts at `0x0049EFE8` are set to `0, 1, …, 15` in nation (DAT) order, then for `i = 0, 1, …, 15` ascending it takes `j = Random(16)` and swaps `order[i]` with `order[j]`. It is **not Fisher–Yates**: `j` ranges over the whole array every time (0–15), so it is the naive "swap each slot with any slot" shuffle, always exactly 16 draws, with `j = i` a no-op. The current nation is then `order[0]` and the turn position is 0. [confirmed: code] (2026-10-03-new-game-turn-order-shuffle.md)
- The generator is Delphi `System.Random` (`FUN_0040284C`): `RandSeed := RandSeed × $08088405 + 1` (32-bit LCG) and `Random(n) = (RandSeed × n) shr 32`. `FUN_00448AA4` begins with `Randomize` (`FUN_00402744`), which on the original sets `RandSeed` to the UTC time of day in milliseconds, `((h × 60 + m) × 60 + s) × 1000 + ms`. [confirmed: code] (2026-10-03-new-game-turn-order-shuffle.md)
- The number of draws before the shuffle is seed-dependent (every `Random(n)` advances `RandSeed` once regardless of `n`): the mercenary fill draws 2, 4 or 5 per slot, the Spring-week-1 weather overlay draws 20 plus 208 per storm centre that hits, then 16 × `Random(12)` for the leaders. For seed 12345 the count is 436 (192 + 228 + 16), so the shuffle uses draws 437–452. [confirmed: code, and by replay] (2026-10-03-new-game-turn-order-shuffle.md)
- The replay reproduces the observed order exactly: seed 12345 gives the observed order and the observed leaders (Carthage *Agis*, Ptolemaic *Thutmose*), and for two unpatched desktop games a search of all 86,400,000 clock seeds finds exactly one seed per game matching the 16 leader draws, which then also reproduces the saved turn order, filled mercenary slots and storm cells. [confirmed: code + Wine + 2 desktop saves] (2026-10-03-new-game-turn-order-shuffle.md)
- The human's choice of nation does not change the order — the shuffle has already run before the New Game form opens. All 16 one-human starts and the two-human start for seed 12345 share one order: Illyria, Numidia, Ptolemaic, Galatia, Seleucid, Thracia, Greece, Dacia, Macedonia, Media, Armenia, Rome (12th), Bithynia, Carthage, Gaul, Celtiberia (nation indices `9 5 3 12 2 15 7 10 4 14 13 0 11 1 6 8`). [confirmed: code + Wine] (2026-10-03-new-game-turn-order-shuffle.md; 2026-10-02-start-as-each-nation.md)
- The order is fixed for the whole game: its only writers are the New Game shuffle and the SAV loader; `TPremierForm_EndTurn` and the AI seat loop `FUN_0044FA20` only read it as `position := (position + 1) mod 16; nation := order[position]`. An eliminated nation keeps its slot — `FUN_0044FA20` skips the AI's work when unity ≤ 0 but still advances. [confirmed: code] (2026-10-03-new-game-turn-order-shuffle.md)
- All 16 nations can start and play two turns as the only human seat; the starting world is the world as it stands when the human's seat comes up, so the AI seats before you have already moved (e.g. Ptolemaic has −9 talents and no war in Rome's start but 4,900 talents and a war with Seleucid in its own). Wine-only. [confirmed: Wine-only] (2026-10-02-start-as-each-nation.md)
- For seed-for-seed parity a reimplementation must reproduce Delphi's LCG, the full New Game draw chain in order (fill branch draws, overlay 20 + 208-per-hit, 16 leader draws), then the 16-swap loop — otherwise the order drifts even with the right shuffle. For distribution-only parity, use the same loop on any uniform `Random(16)`: the result is not uniform over the 16! orders (16! does not divide 16¹⁶, so some orders are more likely), and a Fisher–Yates shuffle would not reproduce that bias. [derived] (2026-10-03-new-game-turn-order-shuffle.md)
- Test vectors (nation indices in DAT order, Rome = 0): seed 12345 → `9 5 3 12 2 15 7 10 4 14 13 0 11 1 6 8`; seed 81,899,841 → `13 10 14 4 8 12 1 9 0 5 15 2 7 3 6 11`; seed 8,363,996 → `2 12 3 9 11 6 7 0 4 13 8 15 1 10 14 5`. [confirmed] Prediction for seed 999: Rome, Armenia, Greece, Gaul, Carthage, Galatia, Celtiberia, Seleucid, Numidia, Illyria, Bithynia, Ptolemaic, Dacia, Thracia, Macedonia, Media (429 draws before; 42 slots filled; storm centre 11). [derived, untested] (2026-10-03-new-game-turn-order-shuffle.md)

### Hotseat (multiple human seats)

- Two human seats work: the New Game form accepts two "human" ticks, the autosave's human flags are exactly the two ticked nations, and the title bar and `CUR_NATION` follow whose seat it is. A round is the shared turn order — the human seats play in their positions, the AI seats between them play by themselves, and the calendar advances only at the round tick (week 1 → 3). End turn by one human hands control to the next human seat, not to a new round. Wine-only. [confirmed: Wine-only] (2026-10-02-two-human-seats.md)
- Both humans' round-1 autosaves share the name `AUTO0720.SAV`, so the second human's turn start overwrites the first's; only the last seat's save of a round survives, and a harness must copy the save after every End turn. Wine-only. [confirmed: Wine-only] (2026-10-02-two-human-seats.md)
- Orders act on the current seat's nation, and a battle involving a human seat opens the tactical screen for that human during the AI phase. A human–human war is one order, symmetric and immediate (both relation entries become 3 at once, no refusal or consent step). Wine-only. [confirmed: Wine-only] (2026-10-02-two-human-seats.md)
- The human-player flag is nation-record word `+0x490`; adding a human Ptolemaic player mid-game changed only three bytes in the whole save, all in that nation's record: `+0x490` `0 → 1` (human flag), and `+0x486`/`+0x488` (the nation's unit-map view origin, y and x: 45 → 90, 55 → 186). [confirmed: controlled save pair] (ptolemaic-player-and-week9.md)

### The week/season/year cycle

- Inside the weekly tick the calendar advances exactly as: `week = (week + 2) mod 12`; `if week == 1` (wrapped from 11 back to 1): `season = (season + 1) mod 4`; `if season == 0` (wrapped from Winter back to Spring): `year -= 1` (BC years count down). This is an exact code-level confirmation of the pattern earlier reports found only by observing season transitions land on the week-11-to-week-1 boundary, including the never-directly-observed year-decrement on New Year. [confirmed: code] (decompiled-turn-and-calendar-sequencing.md)
- One reported turn (one full round) advances the displayed week by 2 — observed as week 1 → 3, and the file grows by exactly three 61-byte news slots (183 bytes): a single-space separator slot, the `Week  N      Season      YYYBC` header, and the event line. [observed; separator/header role confirmed] (one-turn-save-comparison.md)
- In the 55-byte save trailer, byte `+40` is the week within the season (read 11, 1, 3, 5 across consecutive saves, matching the displayed weeks) — a week-of-season field, not a monotonic campaign counter — and byte `+44` is the season index (`0 = Spring`, `1 = Summer`). [observed; strong candidate at time of writing] (strategic-recording-and-summer-saves.md)
- Trailer word `+36` holds the active nation (observed changing 0 → 3 with Rome → Ptolemaic). [observed] (ptolemaic-player-and-week9.md)
- The week, year and season fields in the trailer equal the last news-log header in 54 of 54 saves. [confirmed: 54 saves] (decompiled-sav-file-layout.md)

### The weekly tick: what it does, and to whom

- `FUN_004514ec` loops all 334 cities, all armies and all fleets unconditionally — a true global weekly tick that runs once after every 16th nation's turn, not per-nation processing. [confirmed: code] (decompiled-turn-and-calendar-sequencing.md)
- City supply stock (city record `+0x18`): `supplies += pop × (seasonValue − 40) / 10`, minus that times the owner's mobilization (`nation +0x442`) `/ 200` (not loyalty), capped at `pop × 10` and floored at 0; a city with a hostile army adjacent cannot gain. The season values are the table at DAT `0x1F7D8` (50/80/80/20). The Winter decline is loyalty −1, 1 in 3, when the stock is empty; population is not touched. Confirmed on 33 save pairs (10,693 of 10,980 city-turns exact). Population grows only in the quarterly `FUN_00451b40`, not in the weekly tick. [confirmed: code + 33 save pairs] (decompiled-turn-and-calendar-sequencing.md)
- Each army's maximum moves for the week is recomputed as `moves = 10 − min(5, ⌊troops / 20000⌋)` (at `0x00451651`), then `−1` (at `0x004516D7`) when `⌊supplies × 10000 / troops⌋ < 10`. `FUN_0044a698` (the former "readiness" candidate) is just the army's total troop count — it sums `unit[i].troops` across all 20 slots and returns 1 when zero as a divide-by-zero guard; army size is the only input and unit-type composition plays no part. Checked against 627 army records in 54 saves. [confirmed] (decompiled-turn-and-calendar-sequencing.md)
- Army supply consumption is seasonal and depends on whether the army is stationed at a city: an army not at any city consumes supply proportional to troop count; an army at a city consumes at a rate modulated by a seasonal table. [confirmed: code] (decompiled-turn-and-calendar-sequencing.md)
- For an under-construction fleet (`X`/`Y` still `(0,0)`), the countdown field decrements each week (the field once observed decreasing by 2 per turn); when it reaches 0, `FUN_0044a050(fleetIndex)` is called — almost certainly the "construction complete, place the fleet" step (that function itself was not decompiled). [confirmed: code; completion step inferred from call site] (decompiled-turn-and-calendar-sequencing.md)
- For a fleet already at sea (countdown `== -1`) there is a random chance each week of being lost at sea entirely or damaged in a storm, with worse odds in Winter (a bad-weather value is doubled) — a mechanic with no prior observational evidence. [confirmed: code] (decompiled-turn-and-calendar-sequencing.md)
- Every active recruitment slot's state field (`StateCode`) increments by exactly 2 per week, clamped at 24 — so 24 is not an arbitrary fresh-recruit value but the cap a unit's readiness state reaches and holds after 12 weeks. Observed independently: the first word of 593 of 640 nation recruitment slots advanced by +2 in one turn, including 495 empty slots. [confirmed: code; +2 sweep observed] (decompiled-turn-and-calendar-sequencing.md; ptolemaic-player-and-week9.md)
- At the start of each nation's turn, `TPremierForm_StartTurn` checks for a pending trade or alliance proposal directed at that nation and, if present, shows a modal `MessageDlg` ("*X wants to trade with Y.*" / "*X wants to form an alliance with Y.*") — not a news-log line. The 4-byte block 22 bytes before end of file is `{short proposingNationIndex (0xFFFF = none), short proposedRelationState}`, the second word using the relation-matrix encoding (1 = trade, 2 = alliance). It is set by `FUN_00452034` at the start of every human seat's turn (cleared, rolled, then shown). [confirmed: code + saves] (decompiled-turn-and-calendar-sequencing.md)

### Save-file layout facts needed to play and verify

- The complete SAV sequence, read directly from the matched load/save pair `FUN_004487c4`/`FUN_004484d0`: map 89,600 bytes (320×140×2, `WorldPrefix.MapByteLength`); city table 11,356 (334 × 34); army count 2 then army records of 656 each; fleet count 2 then fleet records of 26 each; nation table 18,752 (16 × 1,172); mercenary table fixed at 50 × 12 bytes; a 2-byte count then (count+1) records of 61 bytes each (the news log, a 40-slot ring buffer where "count" is the most-recently-used slot index); then the 55-byte tail: 32-byte turn order, 4-byte pending offer, 2-byte current nation, 2+2+2+2 = turn-order index, week, year BC, season, 8 bytes of main-window geometry (UI state), 1-byte battle flag. [confirmed: code] (decompiled-sav-file-layout.md)
- The turn order is the 32-byte block written after the news log, at SAV offset `len − 55` as 16 × int16, with the current nation at `len − 19` and the turn position at `len − 17`. [confirmed: code + 54 saves] (2026-10-03-new-game-turn-order-shuffle.md; decompiled-sav-file-layout.md)
- The earlier 3,042-byte gap measured from nation-table end to trailer start is exactly `600 + 2 + 40 × 61` (mercenary table + count field + full 40-slot log) — the previous ~6-byte reconciliation gap came from subtracting the 55-byte tail twice. [confirmed] (decompiled-sav-file-layout.md)
- The battle-in-progress flag and its conditional block (2+2+2+1+2+1,760+336 bytes of tactical state) exist in the code, but saving during a battle is not possible in the game's UI, so every real save's length is fully accounted for by the fields above with no battle-state variant. [confirmed: code + user confirmation] (decompiled-sav-file-layout.md)
- Between two one-turn-apart saves, 311 map cells changed `1 → 0`, exactly reversing the DAT's `0 → 1` overlay differences — the transient New Game weather-overlay cells are cleared as the game progresses (the shuffle report independently uses these code-1 cells as storm evidence). [observed] (one-turn-save-comparison.md; strategic-recording-and-summer-saves.md)
- City record word `+24` is the mutable city-supply field (changed in 331 of 334 records over one turn; Rome's capital rose 1,731 → 1,810 in one reported turn); word `+18` encodes owner nation (0 = Rome, 6 = Gaul, 3 = Ptolemaic, 2 = Seleucid). [observed; +18 label confirmed by later capture/defection evidence] (one-turn-save-comparison.md; strategic-recording-and-summer-saves.md)

### RNG seeding on load

- `System.Randomize` (`RandSeed := clock`) has exactly two call sites; one is inside `FUN_00448AA4` (New Game's leader and turn-order draw), which is called from program start (`TPremierForm_InitialiseForm`) and from New Game (`TPremierForm_NewGame`); the other (`0x456759`) sits in a handler with no direct caller and never fired in these runs. [confirmed: code] (2026-09-29-loading-a-save-does-not-reseed.md)
- File → Open does not reseed: the load routine `FUN_004487C4` (called only from `OpenGameFile`) contains no call to `Randomize`, and a second File → Open in a running game logs no reseed. [confirmed: code + observed SEED.LOG] (2026-09-29-loading-a-save-does-not-reseed.md)
- Two runs from one save diverge because each process start seeds from the clock, not because each load does. A turn is repeatable if the process is started with a fixed seed and the same save and orders follow: turn N = f(save, seed, orders). Same seed + same save + same orders gives byte-identical autosaves, for a whole scripted turn and for a New Game. [confirmed] (2026-09-29-loading-a-save-does-not-reseed.md)
- Two further writers of `RandSeed` exist: the peace treaty `FUN_00450C68` and `TBattlePols_InitializeForm`, both setting `RandSeed = winner + loser` before their draws — deterministic, so they do not break repeatability, but they reset the stream whenever a treaty is made. [confirmed: code] (2026-09-29-loading-a-save-does-not-reseed.md)
- On the patched build, `Randomize` is routed through the `SEED.TXT` cave, so New Game's `RandSeed` is the file's value (falling back to the clock when absent). [confirmed: build behaviour] (2026-10-03-new-game-turn-order-shuffle.md; 2026-09-29-loading-a-save-does-not-reseed.md)

### End-turn gating

- `FUN_0045af00`, called at the very start of `TPremierForm_EndTurn`, is the end-turn validity check — but it never reads the moves field (`ArmyRecord +6`). The "has not acted" filter is `FUN_0044aab4`, which recomputes the army's full weekly maximum and returns `fullMoves != army[+6]`, i.e. "this army has not acted at all this week". For each such army the check warns on supply and money: `FUN_0045ae68` returns a required-supply and supply-percentage pair, and the ready flag is cleared when the percentage is under `0x14` with a further condition, or when the army's money (`+12`) is below the required amount. The fleet half of the loop is the same shape on the fleet record. [confirmed] (decompiled-turn-and-calendar-sequencing.md)
- The check never blocks an AI seat: the tail `(&DAT_00474b00)[currentNation * 0x494] == 0` forces ready `= 1`, one of four call sites fixing the flag's polarity as 0 = computer-controlled. [confirmed] (decompiled-turn-and-calendar-sequencing.md)
- The original code carries a genuine inconsistency here: `FUN_0044aab4`'s low-supply test is `supplies × troops / 10000 < 10`, while the weekly tick that wrote the value uses `supplies × 10000 / troops < 10`; the two agree only near 10,000 troops, so the reference value is wrong for armies far from that size. [confirmed: code] (decompiled-turn-and-calendar-sequencing.md)
- Observed UI: End turn can pop an "End turn ?" box — "An army of yours cannot afford to pay its mercenary units…" (a second wording of the "needs supplies" box) — followed by Confirm boxes, before play continues. Wine-only. [observed: Wine-only] (2026-10-02-two-human-seats.md)
- End turn's first click did not register in 3 of 21 starts (Illyria, Armenia, Dacia — all armyless nations; no dialog shown, calendar unchanged), and no nation failed twice: intermittent, cause unknown. Wine-only. [observed: Wine-only] (2026-10-02-start-as-each-nation.md)

### Open

- The exact per-season growth-rate and supply-consumption table contents at `DAT_004794a8`/`DAT_004794a0` (10-byte stride, 4 seasons) were not extracted that pass. (decompiled-turn-and-calendar-sequencing.md)
- The real treasury/tax-collection step in the weekly tick is still unfound — `FUN_00451304`, the step right after city/army/fleet processing, is a seasonal weather-event system, not taxes. (decompiled-turn-and-calendar-sequencing.md)
- `FUN_0044a050` (fleet construction completion) was not decompiled, only inferred from its call site; the storm/loss odds are untested against a controlled Winter-transition save sequence. (decompiled-turn-and-calendar-sequencing.md)
- Whether the desktop original takes the `Randomize` branch when started from `SEED.TXT`; whether `Randomize`'s other call site (`0x456759`, handler with no direct caller) can re-seed mid-game; and the weather overlay's edge behaviour for a storm centre whose 17 × 17 box crosses the map edge. (2026-10-03-new-game-turn-order-shuffle.md; 2026-09-29-loading-a-save-does-not-reseed.md)
- Repeatability through a tactical battle fought with *Computer general* inside the AI phase (no battle occurred in the tested turns). (2026-09-29-loading-a-save-does-not-reseed.md)
- Trailer word `+38` changed 7 → 2 over one turn; its meaning is unknown. (ptolemaic-player-and-week9.md)
- In the two-human run: nothing after the war order (no fleets, no human–human battle), whether both humans are asked to place units when their units meet, whether the "mercenary pay" End-turn box appears for the same reason in every start, and whether a two-human round repeats byte for byte from the seed (same state observed twice, but saves not compared byte for byte). One and a half rounds, one seed, one pair. (2026-10-02-two-human-seats.md)
- The cause of the intermittent End-turn click failures. (2026-10-02-start-as-each-nation.md)
- Everything in the two Wine-only reports remains a candidate until the desktop original confirms it. (2026-10-02-start-as-each-nation.md; 2026-10-02-two-human-seats.md)

## Economy, taxation, and the quarterly tick

### Tax income and the tax-rate field

- **"Quarterly" means once per season, four times a year.** `FUN_00451b40` is called exactly once, at the week-11→1 wrap, after that tick's city/army/fleet loops and weather step and after the week counter resets to 1, but before the season counter advances (decompiled-quarterly-billing-and-economy.md).
- **Tax income formula:** `income = nationTaxBase × taxRate / 100`, computed by `TChangeTax_PrintNewNumbers`; verified against Rome's own dialog figures 366 (15%) and 488 (20%), both solving to base 2,440 with no rounding (decompiled-fleet-tax-and-mercenary-formulas.md).
- **The tax rate field** is `NationRecord.TaxRatePercent` at nation `+0x44A`; a controlled change moved it exactly 15 → 20, matching the dialog (rome-tax-increase-and-sidon-capture.md).
- Rome's actual stored base is 2,444, not 2,440 — `2440 × 15/100` and `2444 × 15/100` both truncate to 366 (and both give 488 at 20%), so the dialog solve cannot distinguish them (nation-tax-base-and-city-economy-fields.md).
- The tax dialog's displayed "income" is a preview, not a stored field: treasury fell further into deficit (-644 → -759) across the same turns, so displayed income is not the stored treasury delta (rome-tax-increase-and-sidon-capture.md).

### Wealth and tax-base construction

- **The tax base is stored and derived:** the signed 16-bit word at nation `+0x44c` (same offset in the SAV's 1,172-byte record; `+0x41b` in the DAT's 1,055-byte record, right after the tax rate at `+0x419`). The quarterly tick zeroes and rebuilds it from the cities; captures adjust it in between. A save carries the last rebuild plus capture adjustments — persisted state, not a free input [confirmed] (nation-tax-base-and-city-economy-fields.md).
- **Quarterly rebuild:** for every nation, wealth `+0x430` and tax base `+0x44c` are zeroed; then per city, credited to the owner (`city+0x12`): `wealth += population × 3000`; `taxBase += contribution << 2`, where `contribution = city.tribute (+0x20) × population (+0x1c) / maxPopulation (+0x1e)` (`FUN_004498b0`) [confirmed] (nation-tax-base-and-city-economy-fields.md).
- The rebuild uses the **grown** population (growth runs before the contributions are added); recomputation from post-tick saves matches the stored tax base and wealth for 78 of 80 nation-quarters, pre-tick populations for only 13 and 7 [confirmed] (city-population-growth.md).
- Checked over 54 saves / 864 nation-city pairs: 569 match exactly; all nations match right after a rebuild (16 of 16 in season-start saves), and drift between rebuilds follows the code's pattern (population/tribute change, capture adjustments after siege damage) [confirmed] (nation-tax-base-and-city-economy-fields.md).
- The DAT's starting values are not the rebuild's (Rome 2,528 stored vs 2,464 recomputed; Carthage 8,264 vs 8,192) and survive only until the first quarterly tick [confirmed] (nation-tax-base-and-city-economy-fields.md).
- **Capture transfer** (`FUN_0044bb18`): new owner `taxBase += contribution << 2`, `treasury += contribution × 4`; both owners' wealth `± population × 3000`; unity `+9 / −15`; city count `±1` [confirmed exactly on the Naupactus capture: +48 treasury, ±48 tax base, ±75,000 wealth, ±1 city] (nation-tax-base-and-city-economy-fields.md).
- **Defection transfer** (`FUN_0044bed8`): new owner `taxBase += contribution << 2`, `treasury += contribution × 6`, unity `+3`; old owner `taxBase −= contribution << 2`, unity `−20` floored at 250, treasury unchanged; wealth `± population × 3000`; city count `±1` [confirmed] (nation-tax-base-and-city-economy-fields.md, decompiled-quarterly-rebellion.md).
- "Wealth" is `Σ population × 3000` keyed to population (not fortification) [confirmed] (nation-tax-base-and-city-economy-fields.md).

### Quarterly billing: the treasury credit and upkeep

- **Treasury credit**, for every nation with unity > 0, reading the just-rebuilt values: `treasury += taxBase × taxRate / 100 + taxBase / 4 − cityCount × 7 − wealth / 20000 + FUN_004499ec(nation)` (`FUN_00451b40`) [derived; verified exact for the human nation in all 6 quarter pairs and for 27 of 80 nation-quarters with no adjustment] (nation-tax-base-and-city-economy-fields.md, city-population-growth.md, 2026-10-05-balance-sheet-tribute-line.md).
- **`FUN_004499ec` is trade and alliance income:** `Σ taxBase[j] div 12` over all 16 nations `j` whose relation to this nation is 1 (trade) or 2 (alliance), accumulated in a signed 16-bit word (decompiled-quarterly-billing-and-economy.md, 2026-10-05-balance-sheet-tribute-line.md).
- **Ship upkeep:** for every deployed fleet, `owner.treasury -= shipCount × 3` — 3 talents per ship per quarter; the `TBuildFleet` "ships × 3" display previews this (decompiled-quarterly-billing-and-economy.md, decompiled-fleet-tax-and-mercenary-formulas.md).
- **Regular army and garrison upkeep use the recruitment price table:** for every unit in every army and every occupied city-garrison slot, `upkeep = (troops / 200) × quarterlyPriceTable[unitType]` (table `DAT_00478fd4`, the same table as recruitment), billed to the treasury with **no balance check** (decompiled-quarterly-billing-and-economy.md).
- **Mercenary upkeep** (slot `+0` ≠ 0): `((troops div 200) × price × quality) div 5`, billed to the **army's purse** (`+12`), never the treasury; the non-payment test is per-slot `purse ≤ 0`, and on failure the whole mercenary unit is removed and `troops div 100` is taken from the army's **supplies** (`+10`). Regular units never leave for lack of pay; debt's only consequence is leader deposition (decompiled-quarterly-billing-and-economy.md).
- **Mobilization decays by 3 each quarter** (floored at 0): `mobilized (+0x442) = max(0, mobilized − 3)` — confirmed 71 of 80 nation-quarters; the 9 exceptions are AI recruit/disband orders (city-population-growth.md).
- **Unity is recomputed, not decayed:** `unity (+0x440) = min(990, max(300, unity + 25 − taxRate / 2 − mobilized / 5))` after the mobilization decay — it drifts up; confirmed 60 of 80 (the rest had battles, captures or orders in the round) (city-population-growth.md).
- **AI leader deposition** (`FUN_0044c8f0`, AI nations only, after the income credit): trigger `Random(9) == 0` and (treasury `< −(wealth div 500)`, or `< −20000`, or unity `< 400`); effect: new leader, `unity = max(unity, min(550, unity + 150))`, negative treasury reset to 0 (otherwise `+1000`); confirmed on 2 of 15 in-debt AI nation-quarters. A human nation faces the same test at the start of each of its turns and failing it ends the game (decompiled-quarterly-billing-and-economy.md).
- **Diplomatic thaw:** every nation pair with a hostile (negative) relation has a 1-in-3 chance per quarter of a small automatic improvement (decompiled-quarterly-billing-and-economy.md).
- Order within the tick: (1) ship/army/garrison upkeep, (2) wealth and tax base zeroed, (3) the city loop (growth, then contributions, loyalty draws, rebellion), (4) the nation loop (mobilization decay, treasury credit, trade income, unity update, AI stability check), (5) the relation thaw [derived, with steps 3–4's marked parts confirmed] (city-population-growth.md).

### The Balance sheet and the tribute line

- **"Tribute" on the Balance sheet is `nation.taxBase div 4`** — Rome: taxBase 2,528 → Tribute 632 `[derived] [confirmed]` (2026-10-05-balance-sheet-tribute-line.md).
- **Tribute does not depend on the tax rate** `[confirmed]`: at 10% and 20% the Tribute line read 632 in both screenshots; only Taxes moved (252 → 505) and the revenue total (913 → 1,166) (2026-10-05-balance-sheet-tribute-line.md).
- **The three revenue lines** (`TBalanceSheet_PaintBalance`) `[derived]`, all `[confirmed]` on Rome: **Taxes** = `taxBase × taxRate div 100`; **Tribute** = `taxBase div 4` (for a negative word, `(x + 3) >> 2`, truncation toward zero); **Trade** = `FUN_004499EC(nation)` = `Σ taxBase[j] div 12` over nations `j` with relation 1 or 2; **Total** = their sum — so the revenue column is the quarterly credit's three positive terms (2026-10-05-balance-sheet-tribute-line.md).
- **Administration** (expenditure) = `wealth div 20000 + cities × 7`; the expenditure column is the negative terms plus unit upkeep (2026-10-05-balance-sheet-tribute-line.md).
- **Debt limit** = `wealth div 500`, capped at 20,000, then rounded down: to a multiple of 100 below 5,001; of 500 from 5,001 to 10,000; of 1,000 from 10,001 to 20,000. Rome: 2,577,000 div 500 = 5,154 → 5,000 (2026-10-05-balance-sheet-tribute-line.md).
- The Tribute line follows the **stored** word, not the live city sum: at game start the stored 2,528 differs from the recomputed 2,464 `[confirmed]` (2026-10-05-balance-sheet-tribute-line.md).
- **Reparations formula** (peace terms): `reparations = W/4 + random(W/4) + cities × 10` with `W = nation[+0x44C]` — the tax base; verified on its one data point (Ptolemaic's 2,269 falls inside the predicted range [2027, 3573] for `W = 6188`, 48 cities) [confirmed] (nation-tax-base-and-city-economy-fields.md).

### City population growth

- **Population grows only in the quarterly tick** — the weekly loop never touches it. Exact step, per city with `pop < maxPop` and no hostile army adjacent: `d = (maxPop − pop) >> 2`; `d = d − d × taxRate / 120`; `pop = pop + (d − d × mobilized / 300) + 1`; `pop = min(pop, maxPop)`. 32-bit signed arithmetic, truncating division, 16-bit stores, **no random draw** [confirmed: 6 save pairs, 2,004 city-quarters, 0 mismatches] (city-population-growth.md).
- **Growth is at least 1 and at most the gap** for any tax ≤ 120 and mobilization ≤ 300; the `min` cap never binds for legal values (mobilization is capped at 100). A city at or above its maximum never changes here [derived from the code] (city-population-growth.md).
- With no tax and no mobilization, growth by gap is: 1–3 → +1, 4–7 → +2, 8–11 → +3 (≈ 25% of the remaining gap plus one — geometric approach to the maximum) [derived] (city-population-growth.md).
- Tax and mobilization reduce growth only in steps: the tax term needs `d × tax ≥ 120` to bite, the mobilization term `d' × mob ≥ 300`. Most real cities (gap ≤ 2) are unaffected; the terms are jointly pinned by exactly one save city (Laranda: pop 56 of 72, tax 40, mob 100 → +3) (city-population-growth.md).
- **Threatened cities do not grow:** `FUN_004497cc` is true when a live army whose owner is at war (relation 3) with the city's owner stands anywhere in the 3 × 3 block centred on the city; 3 of 3 threatened below-max cities failed to grow, and no unthreatened one ever did [confirmed] (city-population-growth.md).
- Fields read: population, maximum, the owner's tax rate and mobilization (read **before** this quarter's mobilization decay) — no loyalty, no season, no unity, no tribute, no randomness (city-population-growth.md).
- **Only three writers of population** besides the loaders: the quarterly growth step; siege damage (`FUN_0044b27c`/`FUN_0044b230`, floored at `maxPop / 6 + 1`, same damage to loyalty and fortification); capital relocation `+10` (and a rebirth's new capital). So population is frozen between quarter ticks except under siege or a new capital [derived] (city-population-growth.md).
- There is **no separate growth-rate table**: `DAT_004794a8` is the value word of the season records (Spring 50, Summer 80, Autumn 80, Winter 20; DAT `0x1F7D8`), shared by army supply consumption and city supply production — population growth does not read the season at all [confirmed] (city-population-growth.md).

### City supply-stock production (the weekly step)

- The weekly loop in `FUN_004514ec` writes the city's **supply stock** (`+0x18`), once per round before the army and fleet loops: `v = seasonValue[season]` (50 / 80 / 80 / 20); `s = (pop × (v − 40)) / 10`; `inc = s − (s × mobilized) / 200`; if threatened (`FUN_004497cc`), `inc = min(inc, 0)`; `supplies = max(0, min(supplies + inc, pop × 10))` [confirmed: 33 save pairs, 10,693 of 10,980 city-turns exact] (city-population-growth.md).
- Per turn at mobilization 0: Spring `+pop`, Summer `+4 × pop`, Autumn `+4 × pop`, Winter `−2 × pop`. At mobilization 100 every figure is halved, gains and Winter losses alike (e.g. pop-50 city: +50 / +200 / +200 / −100). The ceiling `pop × 10` is where most cities sit most of the year (Rome's capital, pop 181, holds exactly 1,810) [confirmed] (city-population-growth.md).
- The step is modulated by the owner's **mobilization** (`+0x442`), not loyalty — nations at mob 0 lose nothing in Winter, nations at 97–100 lose exactly half, Rome at 30 loses 15% [confirmed] (city-population-growth.md).
- **Winter decline is loyalty, not population:** if `supplies == 0` and `season == Winter` and `Random(3) == 0`, `loyalty (+0x16) −= 1` (famine unrest; the loop's only Random draw) — 39 of 108 empty-stock Winter city-turns lost exactly 1 loyalty (≈ 1/3); cities with stock, and all cities outside Winter, never do [confirmed] (city-population-growth.md).
- The supply loop runs before `FUN_00451b40` and before the season advances: city-ticks use the **pre-growth** population and the **ending** season [confirmed on 5 one-turn quarter pairs] (city-population-growth.md).
- The fortify-order step (up to 10 points per turn when `fortification > 100`, cancelled to `fort % 100` when threatened) is read from code only; no save has an order in progress, and a literal reading would zero a city completed to exactly 100 with < 10 points pending — original bug or misreading, unsettled (city-population-growth.md).

### Quarterly rebellion and defection

- **Loyalty draws in the city loop, in order:** (1) `Random(4)` (0..3 added) only if the owner's tax rate ≤ 10 and loyalty < 80 — low tax raises loyalty; (2) `Random(3)`; (3) only if (2) returned 0, `loyalty −= Random(taxRate) / 8` — a 1-in-3 chance of a penalty scaled to the tax rate; (4) the rebellion, only if loyalty < 30 and the city is no nation's capital (decompiled-quarterly-billing-and-economy.md, decompiled-quarterly-rebellion.md).
- `Random(0)` at tax 0 still advances the seed, so a reimplementation must not skip the draw [confirmed] (decompiled-quarterly-rebellion.md).
- **A capital never rebels:** the caller's test is true for the `+0x444` capital of any of the 16 nations, dead ones included [confirmed] (decompiled-quarterly-rebellion.md).
- **The rebellion decision (`FUN_0044C204`), in code order** [confirmed: listing]: if `owner ≠ allegiance`: (a) if `nation[allegiance].unity ≤ 0`, a rebirth attempt `FUN_0044C360` — final, no fallback if it declines; else (b) the city returns to its allegiance nation via `FUN_0044BED8`, with no other condition (no war, distance or AI check; a city can return to a human nation). If `owner == allegiance`: (c) scan all army records in ascending order with no break — the **last** matching army wins, matching being a live army (owner ≥ 0), Chebyshev distance to the city `< 10` tiles, and the owner at war (relation 3) with that army's nation; else (d) the best live neighbour: among nations with the owner's bit set in their neighbour mask (`nation +0x46`) and unity > 0, the highest `s = cities − 2 × cheb(city, nation.capital)`, ties to the lower index. If both find nothing, nothing happens at all (decompiled-quarterly-rebellion.md).
- **Transfer effects (`FUN_0044BED8`):** receiver: unity `min(990, +3)`, wealth `+ pop × 3000`, city count `+1`, treasury `+ contribution × 6`, tax base `+ contribution × 4`; old owner: unity `max(250, unity − 20)` (an owner below 270 is *raised* to 250), wealth `− pop × 3000`, count `−1`, tax base `− contribution × 4`, treasury unchanged. Loyalty after transfer: if `allegiance == receiver`, `L = min(90, 140 − L)`; else `L = min(65, max(50, 100 − L))` — at `L < 30` always 90 in (b) and 65 in (c)/(d). The old owner's recruitment slots targeting the city are removed from slot 39 down, but only those with troops > 0. Population, fortification, tribute, allegiance and the old owner's treasury are never written [confirmed] (decompiled-quarterly-rebellion.md).
- Because the tick zeroes and rebuilds wealth/tax base around the city loop, a rebellion leaves both totals as if the city had always belonged to the receiver; the `× 6` treasury credit, unity changes and city counts land before the nation loop reads them for this quarter's income [derived] (decompiled-quarterly-rebellion.md).
- News: one line per moved city, "*C defects from X to Y.*", sitting at the end of the week-11 round just before the new season's header [confirmed] (decompiled-quarterly-rebellion.md).
- **Rebirth (`FUN_0044C360`)** [confirmed: listing]: counts every city (whoever owns it) with `allegiance == nation` and `loyalty < 40`; proceeds only if the count is `> 7`; moves exactly those cities. Resets: unity 450, conquered-by −1, treasury 0, tax base 0, city count 0, **tax rate 20, mobilization 50**, all 40 recruitment slots' troops to 0 (state/type/city kept); does not reset wealth (the loop refills it), the neighbour mask or the human flag. Its own relation row is zeroed, and a symmetric −8 cooldown is written per moved city with that city's owner. New leader: one `Random(12)`. New capital: the moved city with the greatest `FUN_0044A98C` strength (first by index on a tie; at loyalty 90, `90 × 150 + fortification × 250 + population × 200`); it gets loyalty `min(99, L + 8)` (so 98), fortification `min(99, F + 10)`, population `+10`, maximum population `+20`, tribute `+25`. Rebirth never happens outside a quarter tick (decompiled-quarterly-rebellion.md).
- `FUN_0044C204` itself draws no Random and writes nothing — all effects come from the transfer or rebirth [confirmed] (decompiled-quarterly-rebellion.md).
- No rebellion or rebirth has ever been observed in the 99 local saves (no city ever below 39 loyalty); the rule rests on the decompile alone, though the shared transfer routine is confirmed 8-for-8 on loyalty by cascade defections [confirmed: saves] (decompiled-quarterly-rebellion.md).

### Fleet order: cost, capacity, and upkeep

- **Build cost:** `n × 10` talents — matched exactly the observed 100-talent 10-ship order (decompiled-fleet-tax-and-mercenary-formulas.md).
- **Quarterly upkeep:** `n × 3` talents, charged per deployed fleet every season by the quarterly tick (`owner.treasury -= shipCount × 3`); the dialog's "ships × 3" value previews this (decompiled-fleet-tax-and-mercenary-formulas.md, decompiled-quarterly-billing-and-economy.md).
- **Troop capacity:** `n × 500` troops — matches the reported 500/ship and reappears independently as the divisor in the mercenary-boarding capacity check (decompiled-fleet-tax-and-mercenary-formulas.md).
- The ship-count spinner is clamped to `[10, 100]`: 10 is the dialog minimum, 100 the single-order cap (matching the "100 ships when combining fleets" error string) (decompiled-fleet-tax-and-mercenary-formulas.md).
- The nation-record stride of 1,172 bytes and the 34-byte city-record stride were both independently confirmed from these form classes (decompiled-fleet-tax-and-mercenary-formulas.md).

### Open:

- The exact relationship between the tax dialog's displayed "income" and any stored nation field (rome-tax-increase-and-sidon-capture.md).
- The tax (120) and mobilization (300) growth divisors in isolation: code gives the immediates, one save city pins both terms together, but the controlled save pair (Laranda at tax 17 vs 18, mob 42) has not been run (city-population-growth.md).
- The fortify-order step's reading and whether the "completes to exactly 100 with < 10 points pending → fortification 0" behaviour is an original bug (city-population-growth.md).
- The mercenary cost formula's concrete table values (`troops × priceTable[type] / 1000 × qualityFactor` is visible but unsolved against the Felsina hire) and the label→name table's DAT backing (decompiled-fleet-tax-and-mercenary-formulas.md).
- No rebellion or rebirth has been seen in play — everything about `FUN_0044C204`/`FUN_0044C360` is from code; whether real games reach the stale-capital states that let a rebellion eliminate its owner, and the forced-capture `L′` values inferred from the erosion window, are unverified (decompiled-quarterly-rebellion.md).
- A negative tax base (the `(x + 3) >> 2` tribute form) has not been seen in play; the tick's credit was not re-measured in the balance-sheet task itself (2026-10-05-balance-sheet-tribute-line.md).
- Whether a captured city's allegiance later converges to its new owner (rome-tax-increase-and-sidon-capture.md).
- The AI stability check's exact trigger ("collapse if unhealthy" as read, or something more nuanced) awaits an observed AI collapse; the quarterly-formula pass performed no numeric whole-tick cross-check of its own beyond the terms already verified (decompiled-quarterly-billing-and-economy.md).

## Cities, the map, capture and defection

### Map size, layout and terrain codes

- The world grid is **320 × 140** cells, stored as 44,800 little-endian 16-bit words; storage is **column-major**: the value at `(x, y)` is the word at byte offset `2 × (x × 140 + y)` (map-layout.md)
- The first 89,600 bytes of the DAT are the map; the 334 city coordinates follow in the records after it. City coordinates align with expected geography: Rome `(101, 43)`, Carthago `(93, 78)`, Alexandria `(190, 94)`, Sidon `(221, 71)`, Rhagae `(317, 49)` (map-layout.md)
- Terrain codes identified from screenshots: `0` water, `2` green land (Plain), `3` desert, `4` forest, `5` mountains (map-layout.md)
- The terrain table sits at **DAT offset `0x1F622`**: twelve 14-byte records `[12-byte NUL-padded name][2-byte move cost]`, covering cell codes 0–11 exactly (terrain-move-cost-table-in-dat.md)

### Move costs

- Move costs: `0` Sea 1, `1` Sea 3, `2` Plain 1, `3` Desert 1, `4` Forest 2, `5` Mountains 4, `6`–`11` River 4 (terrain-move-cost-table-in-dat.md)
- The army step (`FUN_0044d420`) accepts **only land cells 2–11** and pays the table value; codes ≥ 12 (city 20–99, army 200–247, fleet 300–347 markers) are not steppable mid-path — a marker in the path aborts the move, interactions are handled at the destination (terrain-move-cost-table-in-dat.md)
- The "insufficient moves zeroes the turn's movement" rule fires **only for AI nations** (human/computer flag at nation `+0x490` is computer); a human walk simply aborts at the blocking tile with moves intact (terrain-move-cost-table-in-dat.md)
- Fleets traverse **only cell codes 0 and 1**, paying 1 and 3; a fleet carrying an army drags the army's coordinates along (terrain-move-cost-table-in-dat.md)

### Rivers

- Values `6`–`11` are **river shapes**, not forest kinds: `6` east–west, `7` north–south, `8` north–east, `9` east–south, `10` south–west, `11` north–west; together 1,142 river cells; original river colour ≈ `#000080` (rivers-and-map-markers.md)
- A river crossing costs **4**, equal to mountains — not uniquely expensive (terrain-move-cost-table-in-dat.md)

### Rough sea (map code 1)

- Code `1` is **rough sea**, a weekly weather overlay (`FUN_00451304`/`FUN_004511bc`), not a terrain type: the DAT holds no code-1 cell; it is painted onto calm sea (code 0) and cleared a week later `[confirmed: decompiled; 99/99 corpus saves consistent]` (decompiled-map-code1-overlay.md)
- Odds and radius by season/week — Spring weeks < 6: `N=15, r=4`; Spring ≥ 6: `N=30, r=3`; Summer: `N=40, r=2`; Autumn < 7: `N=30, r=3`; Autumn ≥ 7: `N=15, r=4`; Winter: `N=5, r=5`. Each of 20 fixed centres (DAT `0x1F876`) rolls `Random(N) == 0` independently (decompiled-map-code1-overlay.md)
- The painted shape is a **square (Chebyshev)**: the inner `(2r+1)²` square always, the ring out to `±2r` at 50 % per cell; each call first clears every code-1 cell within ±10 of each centre (the maximum paint reach), so code 1 lives exactly one week `[confirmed]` (decompiled-map-code1-overlay.md)
- A cell is painted only if it is currently code 0 and **no city marker (codes 20–99) lies in its clamped 3×3 neighbourhood** — rough sea never touches a city tile, not even diagonally; land does not block it `[confirmed]` (decompiled-map-code1-overlay.md)
- A hit on a fleet marker sets that fleet's `CoveredCell` (`+24`) to 1 instead (decompiled-map-code1-overlay.md)
- Effects: a fleet pays **3** moves to enter a rough cell vs 1; the weekly storm pass applies `dmg = min(8, dmg × 3)` when `CoveredCell == 1`; the fleet panel prints `Sea-rough`/`Sea-calm`; army movement and every "is this sea?" test treat 0 and 1 alike `[confirmed]` (decompiled-map-code1-overlay.md)

### Marker encodings

- **City markers:** `map code = 20 + owner code + 16 × variant`; the occupied range is **20–99** (the formula tops out at `20 + 15 + 64 = 99`) — do not derive a 180-value marker space from the 20–199 search bound; the relation holds for 334/334 cities in `7.sav` (rivers-and-map-markers.md)
- **City variants 0–3 are population size tiers** by unsigned thresholds on the city's current population (`+0x1C`, thousands): `< 25`, `25–49`, `50–99`, `≥ 100`; marker `owner + 0x14/0x24/0x34/0x44`; writer `FUN_0044a794` `[confirmed: decompile]` (2026-10-07-city-marker-variants.md)
- **Variant 4 is the national capital** (`owner + 0x54`), written by capital relocation `FUN_0044bd2c` and rebirth `FUN_0044c360`; `FUN_0044a794` refuses to touch a capital; in eighteen saves every live nation's capital and only those carry variant 4 `[confirmed: decompile + saves]` (2026-10-07-city-marker-variants.md)
- There is **no "three city size tiers"** — four size tiers plus the capital marker make the five variants (2026-10-07-city-marker-variants.md)
- The tier is refreshed **only when the city changes owner** (the writer's callers are the siege-transfer, transfer/defection, elimination and conquest paths), never by growth: a city that grows past a threshold keeps its smaller icon until captured `[confirmed: decompile + saves]` (2026-10-07-city-marker-variants.md)
- **Army markers:** `200 + owner code + 16 × variant`, three bands at **25,000 / 50,000 troops** (`FUN_0044a80c`) (rivers-and-map-markers.md; 2026-10-07-city-marker-variants.md)
- **Fleet markers:** `owner + 300 / + 316 / + 332` at **< 25, 25–49, ≥ 50 ships** (unsigned), written by `FUN_0044a878` on every ship-count change (joins, splits, construction, storm damage, AI merge) `[confirmed: decompile]` (2026-10-07-city-marker-variants.md)
- The map code is **not a unique entity ID** — two army cells can share code `201` (rivers-and-map-markers.md)
- City-tile corner colours by owner code: `0` purple `#800080`, `1` red, `2` olive, `3` navy, `4` white, `5` lime, `6` maroon, `7` aqua, `8` yellow, `9` navy, `10` green, `11` teal, `12` blue, `13` magenta, `14` red, `15` gray (rivers-and-map-markers.md)

### Fortification orders, cost, and the 100 bug

- City `+0x1A` is the fortification word: ≤ 100 is the current level; above 100 means `pending points × 100 + current` (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md)
- **Cost:** one fortification point costs **the town's population** in talents; the whole order (`population × points`) is paid up front from the treasury (nation `+0x438`); OK performs **no treasury check**, so the treasury can go negative (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md)
- The dialog clamps `points = max(0, min(points, 100 − fortification word))`; while an order is pending the word is above 100, the clamp is negative and points are forced to 0 — **one order per town at a time** (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md)
- **Rate:** the weekly tick builds at most **10 points per turn**: `word += min(10, word / 100)`, then `word −= min(1000, (word / 100) × 100)` — the second line computed on the **new** value (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md)
- **Cancellation:** a hostile army next to the town (checked by the tick, and independently by a siege attempt) sets `word = word % 100`: the pending points are dropped with **no refund** `[live-confirmed]` (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md)
- **The 100 bug:** when an order ends at exactly 100 % with a last step smaller than 10 points (`current + points = 100` and `points % 10 ≠ 0`), the recomputed subtraction removes the whole word and leaves the town at **0 %** — e.g. 95 + 5 → 0, and 62 + 38 → 72 → 82 → 92 → 0; by contrast 60 + 40 → 100 correctly. Maximal "fortify to the top" orders are hit whenever the current level does not end in 0; orders to 75 % are never affected `[confirmed live]` (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md)
- **The AI never fortifies:** the only writers of `+0x1A` are the dialog OK, the siege strip, capital relocation (`min(99, fortification + 10)`) and rebirth (same); only a human seat opens the dialog, so an AI nation's recruiting towns stay the ones it starts with, plus a new capital's +10 `[derived]` (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md)
- A town recruits at fortification ≥ 75 % (or as capital); a newly fortified town recruits the next turn `[live-confirmed]` (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md)

### The neighbour mask

- Nation record `+0x46` is a symmetric 16-bit neighbour mask **loaded from the DAT** at nation-record offset `+0x2B` (2 bytes LE; absolute `0x1B12B + i × 1,055`), never derived `[confirmed: decompile + bytes]` (dat-neighbour-mask.md)
- The DAT mask is symmetric, has no self-bits and holds **24 pairs**; all 16 rows are identical in every one of 101 saves `[confirmed: bytes / saves]` (dat-neighbour-mask.md)
- Only **three routines write `+0x46`**: the DAT loader, the SAV loader, and the conquest routine `FUN_0044C528`; nothing recomputes it from the map — defection elimination, rebirth and the New Game leader draw leave it untouched `[confirmed: decompile + whole-program instruction scan]` (dat-neighbour-mask.md)
- The **conquest merge**: for each `k` in the loser's mask with `k ≠ winner`, `mask[winner] |= 1 << k` and `mask[k] |= 1 << winner`; the loser's own word is not cleared and nobody loses the loser's bit; the winner does not gain the loser itself `[confirmed: decompile]` (dat-neighbour-mask.md)
- Five readers route through the mask: the AI war pick, the AI treaty picks, the alliance offer roll, the quarterly rebellion's choice of recipient, and the peace cascade's ally gate (an ally makes peace alongside its partner only if it does **not** border the enemy and is not human) `[confirmed: decompile]` (dat-neighbour-mask.md)
- A geometric (Voronoi) derivation reproduces all 24 DAT pairs but adds **6 false pairs** (Rome–Greece, Thracia–Bithynia, Thracia–Seleucid, Seleucid–Macedonia, Seleucid–Greece, Ptolemaic–Greece); a reimplementation must load the mask and apply the conquest merge `[confirmed: engine run]` (dat-neighbour-mask.md)
- The graph looks hand-authored, not a distance rule: Carthage–Ptolemaic is in the mask with capitals 98 tiles apart, while Rome–Greece is not despite Greek cities two tiles from Roman ones `[derived]` (dat-neighbour-mask.md)

### City capture resolution

- Siege `FUN_0044b27c(army, city)`, in order: compute attacker strength; **strip any fortification order** (`fort > 100 → fort % 100`); compute defender strength; if `army.owner == city.allegiance`, `def = def × 9 / 10`; erode loyalty, fortification and population; apply the population floor `max(pop, maxPop / 6 + 1)`; repaint the marker; attacker casualties `FUN_0044ae20(army, max(1, min(15, def × 6 / atk)))` unconditionally; `army.moves = 0`; then the outcome test `[confirmed]` (decompiled-defection-and-siege-attrition.md)
- **Outcome:** `atk > def` → "*{City} ({OldOwner}) falls to {NewOwner}.*" and the transfer `FUN_0044bb18`; otherwise "*{AttackerNation} fails to capture {CityName}.*" — **a tie goes to the defender**; the test compares the post-×9/10 defender strength `[confirmed]` (decompiled-city-capture-resolution.md; decompiled-defection-and-siege-attrition.md)
- **Attacker strength** (`FUN_0044a930`): `Σ(troops × 3 for unit type 2/archers, troops otherwise) / 80 × morale (+0xE)` over the army's 20 slots `[confirmed]` (decompiled-defection-and-siege-attrition.md)
- **Defender strength** (`FUN_0044a98c`): `loyalty × 150 + fortification × 250 + population × 200` (fortification decoded `> 100 → % 100`); `× 5 / 3` if the city is the capital and loyalty > 59; `× 4 / 5` if `owner != allegiance` (integer truncation — not exactly "−20 %"); `+ garrison troops assigned to the city / 2` — a captured city is measurably easier to attack again while unassimilated (decompiled-city-capture-resolution.md)
- **Ownership transfer** (`FUN_0044bb18`): `city.owner = newOwner`; new owner gets `unity +9` (clamped to 990), `wealth + population × 3000`, `cityCount + 1`, `taxBase + tribute × population / maxPopulation × 4` and treasury credited `contribution × 4`; old owner gets `unity −15`, `wealth − population × 3000`, `cityCount − 1`, `taxBase − contribution × 4` (the unity penalty is asymmetric: −15 vs +9) (decompiled-city-capture-resolution.md, as corrected 2026-09-14)
- The old owner's recruitment slots targeting the city are **cleared** — the garrison is wiped on transfer (decompiled-city-capture-resolution.md)
- **Loyalty after capture:** allegiant receiver `min(90, 140 − L′)`; otherwise `max(40, min(60, 100 − L′))`, with `L′` the loyalty after siege erosion (decompiled-city-capture-resolution.md, correction 2026-09-26)

### Siege attrition

- The erosion `FUN_0044b230`, applied to **loyalty (`+0x16`), fortification (`+0x1a`), population (`+0x1c`)** in that order, on every attempt win or lose, is deterministic (no `Random`): `field = max(field × 3/4, min(field × 19/20 + 1, field × def / atk))`, against the post-×9/10 `def` `[confirmed]` (decompiled-defection-and-siege-attrition.md)
- On a successful siege each field loses between ~5 % and ~25 % following `def / atk`; on a failed siege `field = field × 19/20 + 1`, so any field above 20 loses ~5 % per attempt `[derived]` (decompiled-defection-and-siege-attrition.md)
- Attacker casualties per attempt: every unit loses `troops −= troops / (Random(15) + 105) × ratio` (at most ~14 %), with exactly **20 `Random(15)` calls** (one per slot, occupied or not); a second pass deletes units below `standardBattalionSize / 10` (national) or `/ 5` (mercenary) `[confirmed]` (decompiled-defection-and-siege-attrition.md)
- The defender's troops take **no casualties**: the defender's side of a siege is exactly the three eroded fields, the population floor and the fortification-order strip `[confirmed]` (decompiled-defection-and-siege-attrition.md)
- Edge behaviour: `min`/`max` compare 16-bit words, so `q` or `t` ≥ 32768 wraps before the clamp; `atk = 0` divides by zero with no guard; a winning besieger emptied by its own attrition tombstones and the transfer then reads owner `−1` — a latent defect `[derived]` (decompiled-defection-and-siege-attrition.md)

### Cascading defection

- After a forced capture, `FUN_0044ba1c` loops **every other city of the same previous owner**: capitals (`FUN_0044b8d0` — any nation's capital, alive or not) never defect; otherwise, if `grid_distance(city, attacking army) < 10`, `otherDefense = defender_strength` (`÷ 3` if the city's allegiance is the new owner), and if the **loser's** unity `< 650` (i.e. after the capture's −15), `otherDefense < attacker_strength`, and `loyalty < 65`, the city defects via `FUN_0044bed8` — no siege needed `[confirmed: decompile; matches the Galatia news log]` (decompiled-defection-and-siege-attrition.md)
- The defection routine `FUN_0044bed8` **never writes population or fortification** (confirmed city-by-city in the Galatia save pair); unity change is **+3 / −20** (old owner's unity `max(250, unity − 20)`); garrison at the city is cleared (decompiled-defection-and-siege-attrition.md; galatia-elimination-and-city-resupply-confirmed.md)
- Loyalty on defection: allegiant receiver `min(90, 140 − L)`; otherwise `min(65, max(50, 100 − L))` — a cascade city usually lands on **50**; all 8 cascade defections in the saves match (decompiled-defection-and-siege-attrition.md, correction 2026-09-26)
- If the loser's city count reaches 0 after a defection, the nation is eliminated through the defection path (decompiled-defection-and-siege-attrition.md)

### Capital relocation

- When the loser's **capital** falls, `FUN_0044bb18` attempts a move if `loser.unity > 400 and loser.cityCount > 6` (tested after the capture's own −15 / −1, so the loser needed unity ≥ 416 and ≥ 8 cities before the capture); otherwise the conquest fires `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- `FUN_0044bd2c`: `unity −= 50` first, unconditionally, whether or not a city qualifies (a successful move costs the loser 65 unity in total); candidates are the loser's own cities at **Chebyshev distance ≥ 11** from the fallen capital; `score = (defender_strength / 10) / d` must be ≥ 1; strict `>` tie-break keeps the **lowest city index** `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- On success: news "*<nation> have moved their capital to <city>.*"; the new capital gets `loyalty = min(99, L + 8)`, `fortification = min(99, F + 10)` (which **discards any pending order**), `population +10`, `maxPopulation +20`, `tribute +25` (all uncapped), and the capital marker `owner + 0x54`; the fallen city is repainted by `FUN_0044a794` as the capturer's ordinary population-band city `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- If no candidate qualifies, only the unity −50 is written and the caller runs the conquest (decompiled-elimination-cleanup.md)

### Elimination: conquest path, cleanup and rebirth

- **Trigger:** the conquest routine `FUN_0044C528` (called only from the capture transfer) fires when a **non-capital capture leaves the loser with fewer than 6 cities**, or when the capital falls and cannot be moved — it is not "lose the last city" `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- It annexes every remaining city at once: loyalty `min(80, 120 − L)` if `allegiance == winner`, else `min(70, max(40, 100 − L))`, then `+ Random(6)`; per city the winner gets `cityCount +1`, `wealth + pop × 3000`, `treasury + contribution × 6`, `taxBase + contribution × 4`; **the loser's city count, wealth and tax base are never decremented** — Galatia's stale `cities = 5` `[confirmed: decompile + save]` (decompiled-elimination-cleanup.md)
- Winner unity `= min(990, unity + 50)`; if the loser's treasury is positive it is **copied** to the winner (the loser's is not zeroed); relations reset for all `k` via `FUN_00449B40(loser, k, 0)`: trade `1 → −8`, alliance `2 → −24`, war `3 → −18`, everything else (including existing cooldowns) `→ 0`, written symmetrically; the neighbour-mask merge runs (decompiled-elimination-cleanup.md)
- **Forces:** every army the nation owns is deleted (tombstone `owner = −1`; an embarked army clears its carrier's `+22`; otherwise the covered map cell is restored); every **launched** fleet is deleted — writing `0` to its map cell — together with the army aboard, **whoever owns it**; fleets still under construction go to the receiver with countdown and build city unchanged; units, supplies and money are **destroyed, not credited** `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- Deletion is a tombstone; compaction (`FUN_0044ADB0`, run in the AI-seat loop) moves the **last** record into each hole and renumbers only a fleet's carried-army index `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- Nation fields: `DisableNation`; `conqueredBy (+0x44E) = winner`; `unity = 0`; `capital (+0x444) = −1` sentinel and the old capital repainted; **all 40 recruitment slots' troops zeroed** (state, type and city stay); news is a dashed "*<winner> conquers <loser>.*" banner; victory screen if the winner now holds more than 333 cities `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- Only the captures and their cascade defections get individual news lines; the conquest loop's transfers are silent under the banner (galatia-elimination-and-city-resupply-confirmed.md)
- A human seat eliminated by conquest is shown "*Your nation has been conquerred by X*" (`FUN_0044C8F0`), turned over to the computer, and the game ends if no human seat is left; the defection path zeroes unity **before** this, so a human eliminated by defection ends at unity 150, not 0 `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- The defection-path elimination block (`FUN_0044BED8` at city count 0) does the DisableNation, unity 0, conquered-by, relation reset and the same army/fleet loops — but writes no conquest news, no capital sentinel, and no slot wipe beyond the per-city one `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- The turn order is untouched; the seat stays and is skipped while unity ≤ 0; every diplomatic path requires unity > 0, so **no one can declare war on an eliminated nation** `[confirmed]` (decompiled-elimination-cleanup.md)
- **Elimination is not permanent:** rebirth `FUN_0044C360` fires from the quarterly rebellion when the allegiance nation's unity < 1 and more than 7 cities still holding that allegiance have loyalty < 40; the nation returns with unity 450, zeroed treasury/tax base/city count, those cities defecting to it, and the strongest as new capital `[confirmed: decompile]` (decompiled-elimination-cleanup.md)
- Elimination signature in saves: capital `0xFFFF`, unity 0, conquered-by set, stale city count `[confirmed: saves]` (galatia-elimination-and-city-resupply-confirmed.md)

### City resupply

- Selecting an army at/near a friendly city opens a **city-to-army resupply dialog**: a city supply-stock ↔ army supply transfer plus a national-treasury ↔ army-money pair, with the same 10s/100s steppers as `TArmyToArmy`; observed as an exact reciprocal 100-ton transfer (city 226 → 126, army 204 → 304) (galatia-elimination-and-city-resupply-confirmed.md)
- Supply is shown as a percentage; two data points imply a capacity of roughly **1 ton per ~98–100 troops** — a candidate formula, not yet confirmed (galatia-elimination-and-city-resupply-confirmed.md)

### Open:

- Whether the terrain-table DAT offset `0x1F622` is stable across DAT builds; what `FUN_0044d31c(...) < 10` actually measures; what sets an army's weekly `Moves` maximum (terrain-move-cost-table-in-dat.md)
- Which cell codes the *original map* uses for Desert/Forest/Mountains awaits a render-vs-screenshot check; the human-vs-AI moves-zeroing asymmetry awaits a controlled save pair (terrain-move-cost-table-in-dat.md)
- The rough-sea tile graphic; whether the AI steers fleets away from rough water; the bitwise RNG draw order (no seeded replay); why the 20 storm centres are where they are (decompiled-map-code1-overlay.md)
- Whether city coordinates refer to the cell itself, a nearby symbol, or a visual anchor (map-layout.md)
- Whether a demoted ex-capital's marker refresh is observable in a single save; the DAT's initial map variants were not read directly (2026-10-07-city-marker-variants.md)
- The conquest neighbour-mask merge has never been observed changing a mask (the only conquest in the saves is a no-op for it); why the hand-authored frontier graph looks as it does (dat-neighbour-mask.md)
- The `unity +9/−15` and `wealth ± population × 3000` capture formulas await a controlled same-turn save pair; the Galatian captures' actual `def / atk` windows were not reconstructed; no save pair has yet checked the failed-siege erosion prediction (decompiled-city-capture-resolution.md; decompiled-defection-and-siege-attrition.md)
- The supply-capacity-per-troop ratio (~98–100) rests on two data points; what fully drained Army 0's supply by the save point; the resupply dialog's RTTI class is not yet located (galatia-elimination-and-city-resupply-confirmed.md)
- No save shows an eliminated nation's armies or fleets being disposed of (Galatia had none) — the disposal is code-only; whether cross-nation embarkation exists; whether any path other than rebirth lets defection take a nation's last city; the capital move has not been checked against a save; the `DisableNation` UI reading was not verified against the form resources (decompiled-elimination-cleanup.md)

## Recruitment, mobilisation, and mercenaries

### Cost formula and the DAT unit-type table

- The recruit dialog computes its displayed costs as `initialCost = (troopSize / 200) × priceTable[type]` (table at `DAT_00478fd2`, stride `0x28`/40 per type) and `quarterlyCost = (troopSize / 200) × quarterlyPriceTable[type]` (`DAT_00478fd4`, same stride). `DAT_00478fd4` is the same per-type quarterly-price table the mercenary hire reads, so it is a shared upkeep-per-type table `[confirmed]` (decompiled-recruitment-cost-formula.md). Independently matched against two save-diffs: 1,400 light cavalry = 105 initial / 21 quarterly (15/3 per 200); a 15,000-troop light-infantry transfer raised quarterly cost by exactly +75 (1 per 200) `[confirmed]` (decompiled-recruitment-cost-formula.md).
- The unit-type stat table lives in the DAT at `0x1f2f0`, 40-byte records (`[16-byte name][8-byte abbreviation][8 stat words]`), five types: light infantry, heavy infantry, archers, light cavalry, heavy cavalry (type codes 0–4). Full stat decode `[confirmed]` (unit-type-stat-table-in-dat.md):

| Offset | Light inf | Heavy inf | Archers | Light cav | Heavy cav | Field |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `+0x18` | 4 | 2 | 4 | 6 | 5 | Moves |
| `+0x1A` | 15,000 | 6,000 | 3,500 | 7,000 | 2,500 | Standard battalion size |
| `+0x1C` | 7 | 0 | 25 | 9 | 0 | Shots (0 = melee-only) |
| `+0x1E` | 1 | 0 | 2 | 1 | 0 | Range |
| `+0x20` | 18 | 2 | 18 | 15 | 4 | Shooting vulnerability (target's type) |
| `+0x22` | 2 | 20 | 4 | 15 | 30 | Recruit cost, initial |
| `+0x24` | 1 | 2 | 1 | 3 | 4 | Recruit cost, quarterly |
| `+0x26` | 20 | 100 | 40 | 60 | 120 | AI combat value |

- `+0x26` is the AI's per-type combat value: the AI scores armies and pending slots as `(troops / 100) × value[type]` (in-memory `DAT_00478FD6`) `[confirmed]` (unit-type-stat-table-in-dat.md, decompiled-mobilization-and-mercenary-restock.md). `+0x20` is a per-type shooting vulnerability read for the target's type `[confirmed]` (unit-type-stat-table-in-dat.md). `+0x1A` (standard battalion size) doubles as the ceiling on mercenary offer size at restock and as the tactical rout threshold divided by 25 `[confirmed]` (unit-type-stat-table-in-dat.md, decompiled-mobilization-and-mercenary-restock.md).
- The dialog's default troop count on choosing a type is `baseTable[type] / 5` (`DAT_00478fca`, stride 20) — i.e. one fifth of the standard battalion `[confirmed]` (decompiled-recruitment-cost-formula.md, 2026-09-29-which-cities-may-recruit-and-troop-amounts.md).

### Which cities may recruit, and troop amounts

- A town may take a new recruitment order if it is the nation's capital or its fortification is at least 75% `[derived]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md). The dialog's town list also keeps listing a town that already holds units in training (any slot with troops > 0 at that town), and adds an "All cities" entry when more than one town has units in training `[confirmed]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md). The list test decodes the current fortification level (`% 100` while a fortify order is in progress), while `RecruitUnit` and the AI compare the raw word with 74, so a town with an order in progress passes whatever its current level `[derived]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md).
- `RecruitUnit` refusals, in order checked: slot 39 occupied — "You have reached your limit of 40 units."; mobilisation already 100 — "Your mobilisation rate is already 100%."; a non-capital selected town with fortification word ≤ 74 — "This city's fortification has fallen below 75%." There is no treasury check, so the treasury can go negative through recruitment `[confirmed]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md). "All cities" means the capital `[confirmed]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md).
- Amounts: from one fifth of the standard battalion up to the full battalion, spinner steps of ±100 (small) and ±1,000 (large), clamped after every change to `max(battalion/5, min(battalion, amount))`; choosing a type sets the amount to one fifth; the last step near a limit can be partial. Maxima equal the DAT battalion sizes exactly (LI 15,000 / HI 6,000 / archers 3,500 / LC 7,000 / HC 2,500; minima = defaults 3,000 / 1,200 / 700 / 1,400 / 500) `[confirmed]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md).
- Save check: 118 town checks across six saves, 0 exceptions — every town holding units in training is the capital or fortification ≥ 75%; at game start only 23 of 334 towns have fortification ≥ 75% `[confirmed]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md).
- The AI recruits at its capital by default; it picks another town only when at war, one of its armies is within 15 squares of the capital, and more than a third of its units in training are at the capital — then the nearest-to-enemy-capital among its towns with fortification word > 74 `[confirmed]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md). AI type from `Random(100)`: LI 0–34, HI 35–59, archers 60–74, LC 75–89, HC 90–99; amount `battalion/3 + Random(battalion/5 × 4)`, floored to hundreds, capped at the battalion; at most 8 new orders per AI turn, stopping at mobilisation 100 or the troop target `[confirmed]` (2026-09-29-which-cities-may-recruit-and-troop-amounts.md).

### The 40-slot queue and the weekly readiness ladder

- Each nation has a 40-slot recruitment table (8 bytes per slot: `state, type, troops, city`, at nation `+0x2E4`). It is a compacted list: deleting slot k shifts every later slot down one and zeroes slot 39's troops; `RecruitUnit` takes the first slot with troops 0 and refuses when slot 39 is occupied `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- A recruitment order is created with state `0`; the weekly tick runs `state = min(24, state + 2)` over all 16 nations × 40 slots `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md). The mobilized unit's quality is `state / 4` (truncating toward zero) `[confirmed]`, verified end to end against the one controlled mobilization (11 units at state 24 all quality 6) `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md) and against the live Army-recruits dialog for five states at once (7, 13, 15 → "not ready"; 17 → "very poor"; 21 → "poor") `[confirmed]` (ptolemy-run-readiness-ladder-and-mobilization-rate-confirmed.md).
- The quality-name table (DAT `0x1F6CA`, 11-byte stride) prints indices 0–3 all as `not ready`, then `very poor`, `poor`, `average`, `good`, `very good`, `elite` `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- The player's mobilize gate `state > 15` is exactly `quality >= 4`, i.e. "no longer not ready"; the AI only ever mobilizes a fully ready slot (`state == 24`) `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md). The AI will mobilize with no army nearby only once four or more slots are ready `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- Readiness ladder end to end: weeks 0–7 (state 0–14) `not ready`, not mobilizable; weeks 8–9 (16–18) `very poor`, mobilizable by the player; weeks 10–11 (20–22) `poor`; week 12+ (24) `average`, mobilizable by player and AI. A unit mobilized early is permanently worse `[derived]` (decompiled-mobilization-and-mercenary-restock.md).
- New games copy the DAT's 320-byte recruitment block (nation record `+0x2C9`, 1,055-byte records from DAT `0x1B100`) unchanged into each nation's table — nothing generated or randomised; every nation gets 2–8 scripted regiments (4,200–35,200 troops) with odd starting states 5–21, so scripted regiments mature staggered `[derived]` (2026-09-29-new-game-recruitment-queues-come-from-the-dat.md). Per-game differences come only from AI seats before the human appending state-0 slots before the first autosave `[derived]` (2026-09-29-new-game-recruitment-queues-come-from-the-dat.md).

### Mobilisation mechanics (the transfer)

- Mobilizing a slot creates a new army unit; either an adjacent army gains a unit in slot `lastOccupied + 1` (gaps never reused; `FUN_0044a66c` returns the highest occupied index + 1), or a brand-new one-unit army is created next to the city. The slot is then deleted; no existing unit is moved or merged, and nothing is written back to the city. The "city units" the dialog lists are the recruitment slots — there is no separate garrison pool `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- The receiving army must be at Chebyshev distance exactly `1` (`d == 1`) from the slot's city for the player; the AI gets a radius of 5 (`d < 6`). Chebyshev (`max(|dx|, |dy|)`) is the game's grid metric, 8-way `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md). The scan keeps the LAST matching army (no break) `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- The receiving army may not exceed 20 units or 100,000 troops (`total + incoming < 0x186A1`); a full army forces creation of a new one `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- A new army is created by scanning the 3×3 neighbourhood of the city for a cell with map code in `[2, 11]` (land), taking the last match — so it lands on the south-east neighbour whenever that is land, never on the city tile `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md). The engine holds at most 198 armies `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- A newly created army starts with 0 supplies, 0 money, morale 59, and 0 moves for a human nation (1 for an AI nation) — so a player's freshly mobilized army cannot act in the week it appears `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md). Only `0 money` is a creation value; moves, supplies and the morale word observed in older reports are weekly-tick recomputations `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- The new unit is named `"<N>st|nd|rd|th <TypeName> Battalion"` with `TypeName` in `{Foot, Guards, Bowmen, Lancers, Dragoons}` for types 0–4, taking the lowest free ordinal 1–99 nation-wide among units of the same type with origin label `0`; mercenaries (label ≠ 0) never take a battalion number `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md). The army's map marker is refreshed as a size band at 25,000 and 50,000 troops `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- `TArmyRecruits_MobilizeUnits` walks the selection backwards (descending slot order) — required because the row-to-slot table is built before any deletion and the compaction shift only moves later slots `[derived]` (decompiled-mobilization-and-mercenary-restock.md).

### The mobilisation rate

- Placing a recruitment order raises it: `mobilized = min(100, mobilized + 1 + (troops × 1000) / wealth)` with `wealth` = nation `+0x430` = sum over cities of `population × 3000`, rebuilt quarterly. In game units the step is `1 + troops / (3 × totalPopulation)` `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md). Cancelling an order and disbanding a queued entry apply the exact inverse without the cap: `mobilized = max(0, mobilized − 1 − (troops × 1000) / wealth)`. Quarterly decay is `max(0, mobilized − 3)`. The initial value at nation setup is 50 `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- Mobilizing units does not change the rate; only placing orders does `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md). Three sites write it upward: `TArmyRecruits_RecruitUnit`, the AI's `FUN_004504f4` (identical inline increment, gated on `mobilized < 100`), and setup's `= 50` `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md).
- The rate is capped at exactly 100 ("Your mobilisation rate is already 100%.") `[confirmed]` (decompiled-recruitment-cost-formula.md, decompiled-mobilization-and-mercenary-restock.md). A nation's mobilization rate is its standing army expressed as a fraction of its people, accumulated one order at a time — which is why it feeds back into population growth and city supply production `[derived]` (decompiled-mobilization-and-mercenary-restock.md).
- The division truncates: confirmed at a discriminating wealth scale — 13 Ptolemaic orders (wealth 30,573,000; largest step `10,000 × 1000 / 30,573,000 = 0` under integer division) moved the rate exactly 17% → 30%, +13 from the flat `+1` terms; real-valued division would have given 32–33 `[confirmed]` (ptolemy-run-readiness-ladder-and-mobilization-rate-confirmed.md).

### The mercenary pool

- The pool is a fixed 50-slot table of 12-byte records (`x, y, Label, type, troops, quality`); `troops = 0xFFFF` is the empty sentinel and is the code's own test; a hire consumes the whole offer by setting `troops = 0xFFFF` and leaves the stale position `[confirmed]` (mercenary-pool-record.md, decompiled-mobilization-and-mercenary-restock.md).
- `Label` indexes a 52-name ethnic table at DAT `0x1F8C6` (20-byte NUL-terminated strings; `0 Regular`, `11 Gallic`, `35 Egyptian`, …); templates use labels 1–51, and label 0 marks a regular army unit `[confirmed]` (decompiled-mercenary-offer-list-and-position.md).
- Coordinates, label and type are drawn wholesale from a fixed 201-record template table (runtime `0x0049D0A4`, DAT `0x1FCD6`, records 201–250 of the same 251×12-byte block); only troops and quality are randomized. All 201 template positions are city tiles (134 distinct cities), so an offer's position is always a city tile `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md, decompiled-mercenary-offer-list-and-position.md). `rand(200)` returns 0–199, so template 200 (Vologesias LC) is unreachable `[derived]` (decompiled-mercenary-offer-list-and-position.md).
- Restock (`FUN_00449130`) runs quarterly, on the same boundary as tax and upkeep. An empty slot refills with probability `5/6 + (1/6)(1/9) = 46/54` (about 85%); a live offer is replaced with probability `1/9` `[confirmed]`/`[derived]` (decompiled-mobilization-and-mercenary-restock.md).
- On a refill: troops = `min(b + Random(b), standardSize[type])` with `b = (3 × template.troops) div 2` — uniform on `[b, 2b−1]`, i.e. 1.5× to just under 3× the template base, capped at the type's standard battalion size; quality = `min(9, max(5, template.quality + 1 − Random(2)))` — always 5–9 (`poor` through `elite`), the template value or one above, never lower `[confirmed]` (decompiled-mobilization-and-mercenary-restock.md, decompiled-new-game-mercenary-fill.md).
- New Game fills the pool by running the same restock once over the all-empty pool (`FUN_00448AA4` → `FUN_00449130`), so about 42.6 of 50 slots start filled (sd 2.5); it is the first consumer of the RNG after `Randomize`, ahead of the weather overlay, leader draw and turn-order shuffle. Loading a SAV bypasses the fill entirely `[confirmed: code]` (decompiled-new-game-mercenary-fill.md). Four turn-1 saves fit: fill counts 43, 45, 46, 40, and all 5,041 live offers across the 111-save corpus lie inside the predicted ranges `[confirmed: saves]` (decompiled-new-game-mercenary-fill.md).

### Hire rules (price as a gate, AI free hire)

- The hire price is a gate, not a charge `[derived]` `[confirmed]`: `TRecruitMercs_RecruitMercUnit` refuses when `army purse < (troops × price[type] div 1000) × quality` ("Your army has too little money to pay these mercenaries."), and nothing in the function writes the purse or the treasury — two live hires left purse 30 and treasury 2,270 unchanged (2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md).
- Three different numbers use the quarterly price table (`DAT_00478FD4`; LI 1, HC 4): the hire gate `(troops × price div 1000) × quality` (division first); the dialog's displayed "Quarterly cost" `(troops × price × quality) div 1000` (division last); and the actual quarterly pay `((troops div 200) × price × quality) div 5`, billed from the purse at the tick. They do not agree in general: Samnite LI 3,868 q8 gives 24/30/30; Etruscan HC 960 q9 gives 27/34/28 — the box overstates the HC's pay. The panel confirmed 58 = 30 + 28 `[derived]`/`[confirmed]` (2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md).
- The player's "Recruit mercenaries" order, in check order: own army (or the army the selected fleet carries); a live offer at Chebyshev distance exactly 1, else a silent no-op with no message; slot 20 empty ("This army already has 20 units."); troops ≤ 100,000 ("This army cannot get any bigger."); the offer city's owner not at war ("You cannot recruit from an enemy city."); supplies ≥ 15% (`supplies × 10000 div troops ≥ 15`, about 15% of a full load) ("No mercenaries will join an army with so few supplies."); with a fleet selected, `troops div 500 ≤ ships` ("Your fleet cannot carry any more troops."). In the dialog, per hire: the purse gate, then `army troops + offer troops < 100,001` ("An army can not contain more than 100,000 troops."), then fleet space `(troops + offer troops) div 500 ≤ ships` ("This fleet has too little space for these mercenaries.") `[confirmed]` (decompiled-mercenary-offer-list-and-position.md, 2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md).
- The dialog lists every live offer whose `(x, y)` equals exactly the tile of the first live adjacent offer's city — first slot in slot order wins; no owner, nation or label filter; at most 10 lines `[confirmed]` (decompiled-mercenary-offer-list-and-position.md). There is no ownership requirement: own, allied, neutral and peaceful foreign cities all qualify `[confirmed]` (decompiled-mercenary-offer-list-and-position.md).
- The AI hires for free and loose: `FUN_0044E41C` hires every live offer on the tile of any city within Chebyshev distance < 5 (radius 4), gated on the nation being at war with someone, army money > 50, relation toward the city's owner ≠ war, and a free unit slot — with no cost check, no money deducted, no 100,000-troop cap, no supply check and no fleet check `[confirmed: code + saves]` (decompiled-mercenary-offer-list-and-position.md). Verified against 20 single-turn save pairs: 10 of 10 observed AI hires predicted at distances 2–4 (none possible under the player's rule), no unpredicted hires; a peaceful nation's army sat adjacent to an offer for 10 turns without hiring; distance 5 is a boundary control `[confirmed]` (decompiled-mercenary-offer-list-and-position.md). A second routine `FUN_0044E84C` steers AI armies toward the nearest offer city within radius 19 `[confirmed: the function]` (decompiled-mercenary-offer-list-and-position.md).
- The hired unit keeps the offer's label (ethnic name), type, troops and quality, and its non-zero origin label marks it as a mercenary slot: paid from the purse every quarter and exempt from the mobilisation rule of disbanding `[derived]` `[confirmed]` (2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md, 2026-10-05-disbanding-a-regular-unit-lowers-mobilisation.md).

### Disbanding effects

- Disbanding a queued recruitment loses 100% of the recruiting cost — `DisbandUnits` never writes the treasury, no refund whether the unit is ready or not; two live disbands left the treasury at 1,880 both times `[derived]` `[confirmed]` (2026-10-05-disbanding-a-queued-recruitment.md). The entry is removed and later entries shift up (the compaction shift), clearing the queue-full word `[derived]` `[confirmed]` (2026-10-05-disbanding-a-queued-recruitment.md).
- Mobilisation is given back per disbanded queue entry: `mobilisation := max(0, mobilisation − 1 − troops × 1000 div wealth)` (integer division, floor: HI 3,200 gave 32 → 30; HI 4,000 gave 30 → 28, where 1.55 floors to 1) `[derived]` `[confirmed]` (2026-10-05-disbanding-a-queued-recruitment.md). It is the exact inverse of queueing only when the order did not hit the 100 cap and troops/wealth are unchanged (from 99 with a step of 2: recruit gives 100, disband gives 98) `[derived]` (2026-10-05-disbanding-a-queued-recruitment.md). Entries are processed last list row to first, each with its own troops; no distance, readiness or ownership condition `[derived]` (2026-10-05-disbanding-a-queued-recruitment.md).
- Disbanding a regular unit in Change units (or either Disband button of Army to army transfer) lowers mobilisation by `1 + troops × 1000 div wealth`, floored at 0 — Rome HI 5,900 at wealth 2,577,000: 30 → 27 `[derived]` `[confirmed]` (2026-10-05-disbanding-a-regular-unit-lowers-mobilisation.md). A mercenary unit does not change mobilisation (test is `slot +0 == 0`; a mercenary's `+0` is its label): 30 → 30 `[derived]` `[confirmed]` (2026-10-05-disbanding-a-regular-unit-lowers-mobilisation.md). Nothing else changes: no refund of any kind; the army's troops fall by the unit's troops `[confirmed]` (2026-10-05-disbanding-a-regular-unit-lowers-mobilisation.md).
- A regular unit may be disbanded only when an own city lies in the 3×3 around the army (last own city found); otherwise the unit is skipped and "An army must be near its own city to disband a regular unit." shows once; a mercenary has no such condition `[derived]` (2026-10-05-disbanding-a-regular-unit-lowers-mobilisation.md). The mobilisation value is committed at OK, not at Disband — Cancel discards it `[derived]` (2026-10-05-disbanding-a-regular-unit-lowers-mobilisation.md).

Open:

- Whether hiring only part of an offer decrements `Troops` instead of setting the sentinel — only full-offer hires observed (mercenary-pool-record.md).
- A failed player hire at distance > 1 has not been observed (the silent no-op); when `FUN_0044E84C`'s seek target survives later target assignments; whether the transposed relation lookups (player: owner→player; AI: AI→owner) ever differ; whether an AI hire can push an army past 100,000 troops (decompiled-mercenary-offer-list-and-position.md).
- Whether recruitment-slot `state` is ever negative (the weekly tick guards `if (-1 < state)`, but no write sets it below 0); whether a recycled slot's stale state matters before `RecruitUnit` overwrites it (decompiled-mobilization-and-mercenary-restock.md).
- The first quarterly charge of hired mercenaries was not run live (needs End turns to the week-11 tick); only LI q8 and HC q9 tested for the gate/display/pay triple; the refusal was tested at purse 20 only; Wine-only, so play results are candidates until the desktop original confirms them (2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md).
- The floor-vs-rounding separation for the regular-unit disband (5,900 → 2.29 under both); the refusal away from an own city, Cancel, the Army-to-army Disband buttons and multi-unit disbands are code-only; also Wine-only (2026-10-05-disbanding-a-regular-unit-lowers-mobilisation.md).
- The multi-entry disband and the post-disband Balance sheet were not run in play; the price paid for entries already queued by the new-game fill was not observed (2026-10-05-disbanding-a-queued-recruitment.md).
- Whether a scenario or option changes the start year and then uses different starting queues; where the new-game turn-order shuffle happens in code (2026-09-29-new-game-recruitment-queues-come-from-the-dat.md).
- Whether the DAT unit-table offset `0x1f2f0` is stable across DAT builds; whether the mercenary price lookup is byte-identical to the shared quarterly table (only LI 1 and HC 4 re-read from the DAT for the hire test) (unit-type-stat-table-in-dat.md, 2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md).
- Seed-exact replay of the New Game mercenary fill (the seed is wall-clock milliseconds and is not stored) (decompiled-new-game-mercenary-fill.md).

## Armies: records, movement, supply, and purses

### Record layout and unit slots

- In SAV files a little-endian 16-bit army count sits at `0x18A5C` (end of the 334-city table); 656-byte army records follow from `0x18A5E` (army-records-and-roman-roster.md).
- Record header: `+0/+2` x,y; `+4` owner code; `+6` moves remaining (signed); `+8` the map cell the army's marker covers (a terrain code; `-1` means the army is aboard a fleet — not morale, an earlier mislabel); `+10` supplies in tons; `+12` money; `+14` morale; `+16..+655` twenty 32-byte unit slots (army-records-and-roman-roster.md).
- Unit slot: `+0` origin label (`0` = nationally recruited, written by the mobilization routine; the mercenary offer's `Label` for a hired unit, which is why a hire shows as "Gallic" rather than a battalion number — the naming routine skips non-zero labels when assigning ordinals); `+2` type code; `+4` troop count; `+6` quality code; `+8` a 24-byte NUL-terminated name area (army-records-and-roman-roster.md).
- Type codes: `0` light infantry, `1` heavy infantry, `2` archers, `3` light cavalry, `4` heavy cavalry. Quality codes: `5` poor, `6` average, `7` good, `8` very good, `9` elite (army-records-and-roman-roster.md; city-units-army-transfer-and-mercenaries.md).
- A slot with zero troops can still retain a name or filler bytes; zero-troop slots are not active units (army-records-and-roman-roster.md).
- Army panel decodes: supply percentage = `supplies × 10000 / troops`; "N talents per quarter" = `Σ (troops / 200) × quarterlyPrice[type]` over the units; morale tier via `moraleNames[(v − 51) >> 2]` (army-records-and-roman-roster.md).
- The army panel widens `+6` with `MOVSX` and every binary comparison is signed `JLE`/`JGE` (army-records-and-roman-roster.md).
- A newly created army starts with 0 supplies, 0 money, moves 0 (1 for an AI nation), and morale 59 (`FUN_00449F08`) (2026-10-05-split-army-aboard-a-fleet.md; mobilization-movement-and-city-capture-modes.md correction).

### Weekly moves recompute and the signed/FFFF behaviour

- `+6` is a **signed** 16-bit field, read signed everywhere (signed jumps, `MOVSX` on every widening read); nothing ever deliberately writes `−1` (army-moves-field-signed-and-the-ffff-underflow.md).
- Weekly maximum: `moves = 10 − min(5, ⌊totalTroops / 20000⌋)`, minus a further `1` when `⌊supplies × 10000 / totalTroops⌋ < 10` (supply below 10 %). Range 10 down to 5 in five steps of 20,000 troops, floor 4; troop total only, unit-type composition plays no part `[confirmed]` (army-moves-field-signed-and-the-ffff-underflow.md).
- The maximum is computed once per week by the global tick for every army (including armies aboard a fleet) and is **not re-derived when composition changes**: an army reinforced mid-week keeps the larger allowance until the next tick — the only 2 of 627 corpus records exceeding the formula are exactly that case `[confirmed]` (army-moves-field-signed-and-the-ffff-underflow.md).
- `0xFFFF` in a save is `−1` from an underflow bug at `0x0044DBF7` (`SUB word ptr [EBX+0x6],0x2`, the AI's naval-order cost, the one unfloored write), reachable only from a pre-value of exactly `1`; it is not a sentinel. Once `−1`, every guard fails: the army cannot be selected, moved, or acted on for the rest of the turn, and the next weekly tick repairs it `[confirmed]` (army-moves-field-signed-and-the-ffff-underflow.md).
- Complete set of writers: create → 0 (human) / 1 (AI); join → 0; unit transfer (only if source moves is 0) → 0; field battle → 0; siege → 0; embark → 0; disembark → 0; terrain step `−= cost` (guarded by `cost <= moves`); strategic naval `−= 2` (unguarded); strategic `−= 1` (guarded); weekly tick `= 10 − min(5, troops/20000)`; tick `−= 1` below 10 % supply `[confirmed]` (army-moves-field-signed-and-the-ffff-underflow.md).
- `FUN_0044AAB4` ("has this army acted yet?") tests low supply as `supplies × troops / 10000 < 10` while the tick uses `supplies × 10000 / troops < 10` — a genuine inconsistency in the original; they agree only near 10,000 troops, so the end-turn prompt misfires for a large starving army `[confirmed]` (army-moves-field-signed-and-the-ffff-underflow.md).
- The panel prints the field signed and unclamped; an owner would see `Moves --1` (label's hyphen plus the minus sign) `[confirmed]` (army-moves-field-signed-and-the-ffff-underflow.md).

### Movement costs, including rivers

- Terrain cost table `DAT_004792F0` (DAT offset `0x1F622`, 14-byte records `[12-byte name][2-byte cost]`): Sea 1 · Sea 3 · Plain 1 · Desert 1 · Forest 2 · Mountains 4 · River ×6 at 4 `[confirmed]` (decompiled-army-movement-and-river-cost.md, corrected).
- `FUN_0044D420`'s `2 ≤ cellValue ≤ 11` guard is **all land terrain** — every land tile costs moves; the original "only rivers cost" headline was wrong (decompiled-army-movement-and-river-cost.md, corrected).
- Per step: if `cost <= movesRemaining`, move and subtract; else `movesRemaining = 0` — an unaffordable step aborts the whole move this turn; the zeroing fires only for AI-controlled nations (branch guarded on the computer flag). Cell codes ≥ 12 (city/army/fleet markers) block the walk entirely `[confirmed]` (decompiled-army-movement-and-river-cost.md, corrected).
- Dispatch: `TUnitMap_CheckForMove → TUnitMap_MoveHumanArmy → FUN_0044D734 → FUN_0044D420`; the walk is a Bresenham line, so one click issues the whole multi-tile move `[confirmed]` (decompiled-army-movement-and-river-cost.md).
- Entering a city tile at the destination triggers a siege attempt if hostile (`FUN_0044B27C`) or the friendly-city interaction (`FUN_0044F6D8`); landing on another army's marker triggers `FUN_0044AEE4` (decompiled-army-movement-and-river-cost.md).
- Each naval order costs an army a flat `−2` moves (the unfloored instruction above); embark and disembark zero moves `[confirmed]` (army-moves-field-signed-and-the-ffff-underflow.md).

### Attack and siege are adjacency orders

- A siege is an order issued from adjacency, not an army moving onto the city tile `[confirmed]` (attack-and-siege-are-adjacency-orders.md).
- An army never occupies a city tile — no game state has an army and a city sharing coordinates `[confirmed]` (attack-and-siege-are-adjacency-orders.md).
- One interaction pattern governs army→city, army→army, and fleet→fleet: select the actor, select the target; if adjacent, the action is offered `[confirmed]` (attack-and-siege-are-adjacency-orders.md).
- The engine's grid distance is Chebyshev, `max(|x1−x2|, |y1−y2|)` (`FUN_00449018`), used engine-wide `[confirmed]` (attack-and-siege-are-adjacency-orders.md).
- Consequently "near an owned city" for Disband army means adjacent (an own city in the 3 × 3), since co-location is unreachable (attack-and-siege-are-adjacency-orders.md).

### What a refused attack does

- Order of operations: legality check, "Are you sure…?" prompt, war declaration, attack — in that sequence `[derived]` (2026-10-05-refused-attack-declares-nothing.md).
- Legality (city/army target): an army is selected, its moves ≥ 1, and it stands at Chebyshev distance exactly 1 from the clicked tile; the target must be owned by another nation `[derived]` (2026-10-05-refused-attack-declares-nothing.md).
- A refused attack declares nothing: no prompt, no relation change, no news, no change to the army — seen in play for an army 4 tiles away and an adjacent army with 0 moves `[confirmed]` (2026-10-05-refused-attack-declares-nothing.md).
- Fleet target legality is the selected fleet's (selected, moves ≥ 1, distance 1) plus: no city of the target's owner anywhere in the 3 × 3 around the target fleet, else "You cannot attack a fleet docked at its own city !" — refused before any prompt `[derived]` (2026-10-05-refused-attack-declares-nothing.md).
- The prompt appears for any relation except war (`relation == 3`): peace, peace-with-cooldown (negative), trade, and alliance all get the box `[derived]` (2026-10-05-refused-attack-declares-nothing.md).
- Yes declares war both directions (`relation[me][them] := relation[them][me] := 3`), emits news, and cascades one step to every ally of the target; no check follows the declaration, and the attack functions have no refusal branch `[derived]` (2026-10-05-refused-attack-declares-nothing.md).
- A move never attacks: a terrain click is a move; only a marker click reaches `SelectUnit` `[derived]` (2026-10-05-refused-attack-declares-nothing.md).

### Army-to-army transfer and supply rebalancing

- Units move one at a time via `Transfer` into a working buffer; troops and money transfers are exactly reciprocal (`+n`/`−n` pairs) `[confirmed]` (army-to-army-transfer-confirmed.md).
- `OK` writes the mobilization value back, commits both working records, then caps supply: `capA = troops(A) div 100`; if `capA < sA`, push `sA − capA` to B; then the same for B (with B already including A's push) `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- When both armies end above capacity, the surplus is kept on the **selected** army: `A + B = S` always, B ends at exactly `capB` and A holds `S − capB`; nothing is lost or clamped away `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- Money is never rebalanced by `OK` — it moves only in the dialog (steppers) or in the emptied-army merge `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- If a side is emptied (slot-0 troops 0): the survivor absorbs all its supplies and money, uncapped, and the empty army is deleted; if both empty, everything vanishes `[confirmed: code; derived for the both-empty edge]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- `FUN_0044A698` is the army's total troops (1 for an empty army), so an empty army's capacity is `1 div 100 = 0` and its whole supply is pushed out, then merged back `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- The menu order silently does nothing when: no army selected (or a fleet with no army aboard), the army is not the current nation's, or no other same-owner army is at Chebyshev distance exactly 1 `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- Per-unit Transfer refuses, with a message: receiver already has 20 units ("This army already has 20 units."); receiver would pass 100,000 troops ("An army can not hold more than 100,000 troops."); receiver aboard a fleet with `ships < (troops + unit) div 500` ("This fleet can not carry any more troops.") `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- Dialog steppers: each supply click moves `min(step, room(receiver), sGiver)` with step 10 or 100 and room `max(0, troops div 100 − sReceiver + 1)` (so the dialog can fill to `troops div 100 + 1`, which `OK` then trims); each money click moves `min(step, 1000 − mReceiver, mGiver)` with **no floor at 0**, so a receiver above 1,000 gets a negative step `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- The partner B is the highest-index same-owner army at Chebyshev distance 1 other than A; if any such army has slot-0 troops 0, B is the highest-index of those and the split flag is set `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- A disband inside the dialog lowers the nation's mobilisation by `troops × 1000 div wealth + 1`, floored at 0 (the inverse of mobilising), committed at `OK` `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- Transferring every unit out via the dialog therefore merges supply/money into the other army and disbands the emptied one `[confirmed: code]` (army-to-army-transfer-confirmed.md).
- Source-army moves are zeroed by a unit transfer only if they were already 0 (`0x0044AD18`) (army-moves-field-signed-and-the-ffff-underflow.md).

### Joining armies

- Gates, in order: an own army selected (the fleet's carried army when a fleet is selected); a partner exists — the highest-index own army at Chebyshev distance 1; neither army aboard a fleet ("An army on a fleet cannot be combined with another."); combined units fewer than 21 ("These 2 armies combined contain more than 20 units."); combined troops at most 100,000 `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- On join: the units move over, `kept.purse += partner.purse` and `kept.supplies += partner.supplies` (both uncapped), the partner is deleted, and the kept army's moves become 0 `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- Join armies adds purses with no cap — 1,000 + 1,000 = 2,000 seen in play `[confirmed]`; a 16-bit wrap above 32,767 is possible `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).

### Splitting an army (including aboard a fleet)

- Split army uses the same `TArmyToArmy` form with an empty partner; an empty partner is what makes the title read "Split army"; Cancel on a split deletes the new army `[confirmed: code]` (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- Split gates: own army (or the fleet's carried army), more than one unit ("You can not split an army containing only 1 unit."), a free land tile nearby, and fewer than 198 armies `[derived]` (2026-10-05-split-army-aboard-a-fleet.md).
- Splitting an army aboard a fleet is allowed: the new army lands on a land tile next to the fleet (diagonal in the observed case), is not aboard, with moves 0, supplies 0, purse 0; the rest stays aboard `[confirmed]` — one case, four Wine runs (2026-10-05-split-army-aboard-a-fleet.md).
- Placement: `FUN_004492C0` scans the 3 × 3 around the position (the fleet's tile when aboard) and keeps the **last** tile whose map code is 2..11 (markers are ≥ 20, so occupied tiles are skipped); the new army's `+8` is set from that tile `[derived]`, confirmed on one position (2026-10-05-split-army-aboard-a-fleet.md).
- No free land tile: no army is created, the dialog does not open, no message `[derived]` (2026-10-05-split-army-aboard-a-fleet.md).
- The AI's split of a landing army (when `ships × 500 < troops`) gives the new army `purse div 3` and a third of the supplies `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).

### Purses: the 1,000 cap and its writers

- Only three paths cap a purse at 1,000, all minimum rules in a dialog or the own-city refill: the Supply army money arrows and the Army-to-army money arrows (both `min(step, 1000 − receiver's purse)`, no floor at 0, so a purse above 1,000 gets a negative step and is pulled back), and the own-city refill `FUN_0044F6D8` (excess above 1,000 goes to the treasury) `[derived]`; the Supply-army cap seen in play `[confirmed]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- Every other purse-adding path adds uncapped: Buy supplies with a negative amount (purse rises by `−amount div 5`), the AI's foreign-city resupply in the same signed case, Join armies, the emptied-army merge in `OK`, the captured purse of a won battle (`winner.purse += loser.purse`), and the AI's merge of a small army `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- Supply army, money up: `step := min(step, 1000 − purse)`, treasury (or the fleet provider's purse) pays; money down: `step := min(step, army's purse)` to the treasury; with a fleet provider, `min(step, 1000 − fleet purse)` caps the fleet `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- Own-city refill `FUN_0044F6D8` (AI path): purse > 1000 → excess to treasury, purse := 1000; purse < 500 and treasury > 0 → purse += 500, treasury −= 500 `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- The refill on a move is an AI path: a human move ending next to own cities triggers no refill, and a click on an adjacent own city changes nothing in the save `[confirmed]`; the code path is `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- Disband army: the whole purse goes to the owner's treasury, the supplies to the nearby own city's stock, the army is deleted `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- An army that loses its last unit is deleted; its purse and supplies are gone, not paid to the treasury `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- The weekly tick never adds to a purse; the quarterly tick only subtracts and floors at 0 `[derived]` (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- A purse over 1,000 is trimmed only by the Supply army dialog (one click moved `min(100, 1000 − 2000) = −1,000`, purse to 1,000, treasury +1,000) `[confirmed]` or the own-city refill (2026-10-05-army-purse-writes-and-the-1000-cap.md).

### Supplies and money: signedness invariant

- `ArmyRecord.Supplies` (`+0x0A`) and `Money` (`+0x0C`) are signed words; every reader in the application treats them signed, and no `JAE`/`JBE`-class unsigned read exists `[confirmed: decompile]` (2026-10-07-army-supplies-and-money-signedness.md).
- No write path can persist a negative value: every subtraction that could overdraw is either capped before the write or floored at 0 by `max(0, ·)` in the same pass; type both `short` with a "never persistently negative" invariant `[confirmed: decompile]` (2026-10-07-army-supplies-and-money-signedness.md).
- Two transient in-loop negatives exist, both in the quarterly upkeep loop: the last mercenary payment can overdraw money, and the deserter's supply carry-off (`−= troops/100`) is the application's only unguarded supplies subtraction; both are floored at 0 per army before the loop moves on `[confirmed: decompile]` (2026-10-07-army-supplies-and-money-signedness.md).

### Supply capacity and percentage formulas

- The supply dialog (`TAFSupply`) caps an army at `troops div 100 + 1` (integer `IDIV` by 100 then `INC`; no rounding), on both the own-city (free) and foreign-city (paid) paths `[confirmed: code + the one dialog fill 403 → 482 for 48,173 troops]` (supply-capacity-rounding.md).
- Every other path caps at `troops div 100` with no `+1`: automatic resupply `FUN_0044F6D8`, the army-to-army rebalancing, battle-winner absorption, instant-battle attacker wins; no cap at all on instant-battle defender wins and joins `[confirmed: 75 distinct army states at exactly troops div 100, none at +1 except the dialog fill]` (supply-capacity-rounding.md).
- A fleet's cap is `ships × 8` on every path, no `+1` `[confirmed]` (supply-capacity-rounding.md).
- The room term is not floored at 0: an over-capacity army gets a negative step and gives supply back to the provider; on the paid path the refund is `amount div 5`, truncating toward zero `[derived]` (supply-capacity-rounding.md).
- Foreign purchase: amount clamped in order to ≥ 0, city stock, army room, and `money × 5`; on transfer `supplies += amount`, city stock `-= amount`, the selling city owner's `treasury += amount div 5`, `purse -= amount div 5` `[derived]` (supply-capacity-rounding.md).
- `FUN_0044F6D8`'s foreign path caps tons at `money div 5` (not `money × 5`), cost again `tons div 5` `[derived]` (supply-capacity-rounding.md).
- Displayed percentage = `supplies × 10000 div troops`: a dialog fill reads ≥ 100 % (exactly 100 % for armies over 10,000 troops; above 100 % for smaller ones, e.g. 5,000 troops → 51 t → 102 %); the automatic fill reads ≤ 100 % (99 % for most armies) `[confirmed]` (supply-capacity-rounding.md).
- City → army supply transfer with no turn advance is exactly conserved tons-for-tons (79 t: city `+24` −79, army `+10` +79), which also identifies the city `+24` word as the city's supply stock `[confirmed]` (controlled-army-supply-transfer.md).
- Over-capacity armies are reachable in normal play (the selected army keeps the transfer surplus; joins sum uncapped; troops lost after a fill); they are trimmed only by `FUN_0044F6D8` at a friendly city, weekly consumption, or the next `OK` `[derived]` (2026-10-03-army-to-army-ok-supply-rebalancing.md; supply-capacity-rounding.md).

### Morale: writers and thresholds

- The weekly tick writes morale (`+14`) from the supply percentage computed **after** this turn's consumption: `pct < 10` → `max(51, morale − 2)` and `−1` move; `10 … 15` → no change (dead band); `> 15` and morale `< 70` → `+1` `[confirmed: 12 of 12 transitions exact]` (supply-driven-morale-and-fleet-attrition.md).
- 51 and 70 are the field's real bounds — exactly five 4-wide display tiers via `moraleNames[(v − 51) >> 2]`, with a `v − 48` fallback below 51; decay and regen are asymmetric 2:1 (10 turns down, 19 up); a new army starts at 59 `[confirmed]` (supply-driven-morale-and-fleet-attrition.md).
- The threshold is a percentage, not "supply reached zero": morale began falling at 10 t against a 220 t capacity (4 %), a turn before the tanks ran dry `[confirmed]` (supply-driven-morale-and-fleet-attrition.md).
- Complete set of morale (`+14`) writers: the tick's two writes; `+= 3` on battle entry, only for a computer-controlled side; the tactical-array seeds (a different, mid-battle field `DAT_004A0350`); the panel tier display; new-army initialisation to 59; and the two army-strength formulas `(troops / 0x50) × morale` — there is no second decay rule `[confirmed]` (supply-driven-morale-and-fleet-attrition.md).
- Weekly supply consumption: aboard a fleet `troops / 200` (flat, year-round); otherwise `((90 − seasonVal) × troops) / 20000` with the DAT season table Spring 50, Summer 80, Autumn 80, Winter 20 — i.e. Spring `troops/500`, Summer/Autumn `troops/2000`, Winter 7 × summer; floored at 0 `[confirmed]` (supply-driven-morale-and-fleet-attrition.md).
- The quarterly upkeep loop never writes morale; desertion can cut morale only indirectly, by dropping the supply percentage under 10 % one turn later `[confirmed/derived]` (upkeep-payment-and-desertion.md).

### Upkeep and desertion

- The bill is split by unit kind: regular army units, city-unit garrisons, and ships are paid from the national treasury with no balance check (the treasury simply goes negative); price table per unit type: light infantry 1, heavy infantry 2, archers 1, light cavalry 3, heavy cavalry 4; per unit `(troops div 200) × price`; ships cost `3 × ships` `[confirmed]` (upkeep-payment-and-desertion.md).
- Mercenary units are paid from their own army's purse: `(troops div 200) × price × quality div 5` — never from the treasury, and the tick never refills the purse; at quality 5 a mercenary costs exactly its regular rate, at quality 9 1.8 × `[confirmed]` (upkeep-payment-and-desertion.md).
- If a mercenary slot comes up while `purse ≤ 0`, the whole unit deserts, taking `troops div 100` tons of the army's supplies; no morale change, no news message; regular units never leave for lack of pay, however deep the debt `[confirmed]` (upkeep-payment-and-desertion.md).
- Slots are processed in order 0 → 19; the army's last unit fills each hole and the loop does not revisit it (a unit moved into a visited slot escapes both payment and desertion this quarter); an all-mercenary army of n units loses `⌈n/2⌉` per quarter, the last desertion deleting the army `[derived, confirmed once]` (upkeep-payment-and-desertion.md).
- The last payment can overdraw the purse and the overdraft is forgiven: purse and supplies are floored at 0 after each army `[confirmed]` (upkeep-payment-and-desertion.md).
- `FUN_0044AC3C` is the generic remove-unit helper (swap-with-last-slot), not a "degrade" state; the `troops / 100` is taken from supplies, not troops `[derived]` (upkeep-payment-and-desertion.md).
- Debt costs the leader his job: `inDebt = treasury < −(wealth div 500)` or `< −20000` or `unity < 400` (the line is ~6 talents per 1,000 population, capped at 20,000); an AI nation failing a 1-in-9 quarterly roll deposes its leader (treasury reset to 0); a human below the line loses the game at the start of their next turn `[derived; AI side confirmed]` (upkeep-payment-and-desertion.md).
- Upkeep is billed first, before the tax-base rebuild and income credit; the debt test sees the treasury after both `[derived]` (upkeep-payment-and-desertion.md).
- A mercenary hire is a gate, not a charge: the price is only tested against the purse ("Your army has too little money to pay these mercenaries."), nothing is subtracted at hire (2026-10-05-army-purse-writes-and-the-1000-cap.md).

### Field attrition and mobilization

- One turn of movement/combat left every unit of an army between 2.50 % and 2.85 % of its troops — a single percentage applied uniformly army-wide, across unit types and qualities, rather than per-unit front-line losses; the pair cannot separate combat from supply attrition `[observed]` (field-recruitment-uniform-attrition-and-fleet-drift.md).
- A mercenary hire adds a new unit slot at the hired quantity and quality, named after the local nation, unlike mobilization or army creation (field-recruitment-uniform-attrition-and-fleet-drift.md).
- Mobilizing city-unit garrison troops into field armies conserves troop count exactly (85,000 − 7,000 = 78,000 = 35,000 refilled + 43,000 new army) `[confirmed]` (mobilization-movement-and-city-capture-modes.md).
- An army fills to exactly 20 units before the overflow creates a new army, placed on the last cell of a placement scan around the source (observed at Rome +(+1,+1)) `[confirmed]` (mobilization-movement-and-city-capture-modes.md correction).
- Transferring a city unit into an army adds it as a new slot (15,000 light infantry, quality 5 = poor) with the army's supply, money, and moves unchanged — direct evidence the moves maximum is not recomputed on composition change `[confirmed]` (city-units-army-transfer-and-mercenaries.md).
- Multi-turn save pairs conflate transfer, movement consumption, and city production; clean per-ton conservation holds only in same-day, single-action pairs `[confirmed]` (mobilization-movement-and-city-capture-modes.md).

Open:

- The provenance of the one `moves = −1` record (with `coveredCell = 2`): a record-pointer aliasing hazard around `FUN_0044ABE0`'s swap-remove is a candidate, unproven (army-moves-field-signed-and-the-ffff-underflow.md).
- Which low-supply expression the end-turn prompt and AI actually want — the `FUN_0044AAB4` vs tick divergence; whether a large starving army is never warned about (army-moves-field-signed-and-the-ffff-underflow.md).
- Whether a fleet's moves and an army's interact beyond the flat `−2` per naval order (army-moves-field-signed-and-the-ffff-underflow.md).
- Whether the ~2.7 % uniform troop loss is combat, supply attrition, or both, and whether the percentage is fixed or situational (field-recruitment-uniform-attrition-and-fleet-drift.md).
- A live confirmation of the selected-army-keeps-surplus rule, the both-empty edge, and whether an army aboard a fleet can be side A of a transfer (2026-10-03-army-to-army-ok-supply-rebalancing.md).
- The general split-aboard rules beyond the one observed case (other positions, the no-free-tile case, army-selected route), and which land tile is chosen when several are free beyond the one confirmed position (2026-10-05-split-army-aboard-a-fleet.md).
- The own-city purse refill has not been seen in play (no human path reaches it; the AI case needs an End-turn save pair) (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- The 16-bit purse wrap above 32,767, and rows 3, 8, 12, 13, 14 of the purse table are code-only; whether the dialog lets a human fund a purse from a negative treasury is untested (2026-10-05-army-purse-writes-and-the-1000-cap.md).
- A foreign supply purchase has never been saved (the `money × 5` cap, `amount div 5` cost, and the credit to the seller); a second dialog fill with `troops mod 100 < 50` would show `div + 1` in a save (supply-capacity-rounding.md).
- Whether a fleet can besiege a coastal city, or sieges are army-only (attack-and-siege-are-adjacency-orders.md).
- The desertion supply deduction is code-only (both save cases had 0 supplies); the human debt game-over is code-only; the deposition's relation reset unobserved (upkeep-payment-and-desertion.md).
- The 2:1 morale decay/regen asymmetry is confirmed as code but unexplained as design (supply-driven-morale-and-fleet-attrition.md).
- The split-aboard, purse, and refused-attack play results are Wine-only candidates until the desktop original confirms them (2026-10-05-split-army-aboard-a-fleet.md; 2026-10-05-army-purse-writes-and-the-1000-cap.md; 2026-10-05-refused-attack-declares-nothing.md).

## Fleets and naval warfare

### Fleet record layout

- Fleets are stored in a fixed table of **26-byte records** (fleet table at `0x49C26C` in memory, 26 bytes each; a fleet order appends exactly +26 bytes to the save) — confirmed (save diff / live memory read) (fleet-order-at-caere.md; 2026-10-02-fleet-orders-live.md).
- `X`/`Y` at word offsets `+0`/`+2`: real map position once deployed; `(0,0)` marks a fleet under construction, and completed fleets sitting in port also read `(0,0)` — confirmed (save) (fleet-order-at-caere.md; fleet-owner-field-confirmed.md).
- `OwnerCode` at word 4 (byte offset `+8`): the owning nation's code; matches 6 of 6 fleets against independent identity evidence (Rome's ordered fleet, Carthage's lost-at-sea fleet, in-port fleets vs their port's owner) — confirmed (save) (fleet-owner-field-confirmed.md).
- `ShipCount` at `+18` — confirmed (controlled save diff) (fleet-order-at-caere.md).
- Word at `+10`: the **construction countdown** (24 at order, `0xFFFF` once launched) — confirmed (decompile, via correction) (fleet-order-at-caere.md).
- Word at `+20`: the **build-city index** while under construction; `FUN_0044A050` (construction completes) overwrites it with `100`, and from then on it is the fleet's **condition percentage** (displayed "N %", drives repair cost and battle strength) — confirmed (decompile + save) (fleet-order-at-caere.md).
- Word at `+22`: `0xFFFF` sentinel, unchanged across every fleet record seen — confirmed (save) (fleet-order-at-caere.md).
- Covered-terrain field at offset `+24`: reads 1 when the fleet is on rough sea (used by the storm pass) — confirmed (save + decompile) (2026-10-03-storms-and-losses-at-sea.md).
- The record also carries supplies (tons), money (talents) and a carried-army field (army index, −1 when none) — live (Wine-only) (2026-10-02-fleet-orders-live.md).
- Map markers: fleet cells encode `owner + a size band` — 300/316/332 for `<25` / `25–50` / `≥50` ships (so 333 is Carthage's 90-ship fleet, 335 Ptolemaic's 70-ship) — confirmed (decompile + owner words) (fleet-order-at-caere.md).
- `CityIndex` drifts away from the home port as a fleet acts; a stale `CityIndex` pointing at a city that changed hands is expected, so it is not an ownership field — confirmed (save) (fleet-owner-field-confirmed.md).

### Ordering fleets (cost, countdown, placement)

- The Build-fleet ship spinner is clamped to **[10, 100]** ships (single-order cap 100, floor 10) — confirmed (decompile) (decompiled-fleet-tax-and-mercenary-formulas.md).
- Cost is **ships × 10 talents**, deducted from the treasury only (no population, garrison or city-stock cost); observed 10 ships → 100 talents, 30 ships → 300 (2,200 → 1,900) — confirmed (decompile + save) (decompiled-fleet-tax-and-mercenary-formulas.md; fleet-order-at-caere.md; 2026-10-02-fleet-orders-live.md).
- The construction countdown starts at **24** and falls **2 per turn**; the fleet launches **12 turns** after the order (countdown observed 24 → 22 → … → 2 → −1 over the autosaves) — confirmed (decompile + live, Wine-only) (fleet-order-at-caere.md; 2026-10-02-fleet-orders-live.md; 2026-10-03-pair-2-seleucid-ptolemaic.md).
- The launched fleet appears on the **sea tile next to the build city** with **0 moves, supplies 50, condition 100, no army aboard**, news "X finishes a new fleet at <city>."; the port city changing hands during construction does not stop the launch — live (Wine-only) (2026-10-02-fleet-orders-live.md; 2026-10-03-pair-2-seleucid-ptolemaic.md).
- The Build dialog's "N soldiers" display is `ships × 500` transport capacity, not a stored troop count — confirmed (decompile) (decompiled-fleet-tax-and-mercenary-formulas.md; fleet-order-at-caere.md).

### Capacity

- A fleet carries up to **ships × 500** troops; the same `/500` constant appears independently in the mercenary boarding check — confirmed (decompile + live, Wine-only) (decompiled-fleet-tax-and-mercenary-formulas.md; 2026-10-02-fleet-orders-live.md).
- Embark is refused with "The army is too large for this fleet ?" (OK only) when troops exceed `ships × 500` (10,700 troops refused against 20 ships / 10,000 capacity, accepted against 30 ships / 15,000); the refusal click then selects the fleet — live (Wine-only) (2026-10-02-fleet-orders-live.md).

### Movement, supplies and drift

- Moves per turn: **`30 − (ships − 50)/10`**, minus **3 at zero supplies**, minus **`(70 − condition) >> 2` below condition 70** — confirmed in 6 of 6 post-first-turn readings, live (Wine-only; formula from code) (2026-10-02-fleets-sail-and-drift.md).
- A fleet has **0 moves on its launch turn**; the next turn it gets the full formula (30 ships → 32, 60 → 29) — live (Wine-only) (2026-10-02-fleet-orders-live.md; 2026-10-03-pair-2-seleucid-ptolemaic.md).
- Supplies burn **`ships` tons per turn** (90 ships: 80 → 0 in one turn; 70 ships: 80 → 10 → 0) — live (Wine-only; formula from code) (2026-10-02-fleets-sail-and-drift.md).
- Sailing costs 1 move per calm-sea tile (29 → 27 over two tiles); the game accepted every one-tile click along a computed path — live (Wine-only) (2026-10-02-fleet-orders-live.md; 2026-10-02-fleets-sail-and-drift.md).
- On calm sea away from any own city, condition drifts down **3 to 5 points a turn** (the storm formula's ordinary damage plus the zero-supply rider) — live (Wine-only) (2026-10-02-fleets-sail-and-drift.md; 2026-10-03-storms-and-losses-at-sea.md).
- At a New Game, fleets start with a fixed **25 moves** regardless of ship count (90- and 70-ship fleets both 25 before the first weekly tick) — inference from three saves, not read from code (2026-10-02-fleets-sail-and-drift.md).

### Boarding and disembarking armies

- Embark = select the army, click the adjacent own fleet: the army moves onto the fleet's tile, its cell becomes −1, the fleet's carried-army field becomes the army's index, and **both units' moves become 0** — live (Wine-only) (2026-10-02-fleet-orders-live.md).
- An army produced by Split army has 0 moves and cannot be selected, so it cannot embark that turn — live (Wine-only) (2026-10-02-fleet-orders-live.md).
- Unload = select the fleet, click an adjacent land tile: the army lands there (cell = terrain code), the fleet's carried-army field becomes −1, and **both units' moves become 0** again; both need moves, so a landing is a whole turn for both — live (Wine-only) (2026-10-02-fleet-orders-live.md).

### Naval battle resolution

- A battle is **instant**: clicking an adjacent enemy fleet while at war opens no window or box; the next turn's news says "X sinks fleet of Y." — live (Wine-only) (2026-10-02-naval-battles.md).
- Base strength is **`ships × condition / 10`**; the exact random term from the code is **discrete and integer**: `strength = base + random(4) × (base / 10)` — a bonus of 0, 10, 20 or 30 % in four steps — with **the attacker winning only if the defender's strength is strictly smaller (ties go to the defender)**; this rule fits all 160 battles (log-likelihood −79.89, chi-square 3.56) — confirmed (decompile + live fit, Wine-only) (2026-10-02-naval-battle-random-term.md).
- The attacker's `Random(4)` is drawn first, the defender's second (draws follow the role, not the fleet; one bonus pair per seed reproduces both roles' cells in all 10 seeds) — confirmed (decompile + check) (2026-10-03-pair-2-seleucid-ptolemaic.md).
- A carried army adds **`siegeStrength / 50`** to the fleet's strength, where `siegeStrength = troops/80 × morale` with **archers' troops ×3** (only archers are weighted; heavy infantry and cavalry count as light: equal siege-weighted cargos fought identically seed by seed); the defender's cargo counts too — confirmed (decompile read; live support, Wine-only) (2026-10-02-naval-battle-army-aboard.md).
- The **loser always sinks whole** (owner −1; 50 of 50, then 160 of 160, plus pair 2's 20 of 20) — live (Wine-only) (2026-10-02-naval-battles.md; 2026-10-03-pair-2-seleucid-ptolemaic.md).
- The winner loses one fraction of both ships and condition: **`ships × d / 300` ships and `condition × d / 300` condition**, with `r = max(1, loserStrength × 100 / winnerStrength)`, `d = r² / 100` (integer division); this reproduces the observed pair in **160 of 160** battles (divisors 250/350/200 pass only 112/75/19) — confirmed (decompile + live, Wine-only) (2026-10-02-naval-battles.md).
- The winner's carried army takes casualties with the same `d`: each unit loses **`(troops // (Random(15) + 105)) × d`** (division first; exact in 21 of 21 partial losses), and when **`d > 70`** whole units are removed at random on top — so a **one-unit carried army is always destroyed when `d > 70`** (all 51 won single-unit-cargo battles consistent, 0 inconsistent) — confirmed (decompile + live, Wine-only) (2026-10-02-naval-battle-army-aboard.md).
- The loser's army is destroyed with its fleet (`FUN_0044AD38` deletes it), including a defending army — confirmed (decompile + live, Wine-only) (2026-10-02-naval-battle-army-aboard.md).
- The **attacker spends all its moves** (23 → 0); a defender that wins keeps its moves — live (Wine-only) (2026-10-02-naval-battles.md).
- **A fleet within one tile (clamped 3×3) of an own city cannot be attacked**: "You cannot attack a fleet docked at its own city !" (refused with the fleet diagonal to Issus; allowed at 3 tiles) — live (Wine-only; the predicate `FUN_004494e4` is decompiled) (2026-10-03-pair-2-seleucid-ptolemaic.md).
- Practical ratios: a 17 % strength edge wins about 81–93 % of battles, a 50 % edge is certain — live fit (Wine-only) (2026-10-02-naval-battle-random-term.md).

### Storms and losses at sea

- The storm pass, per turn: **`dmg = max(1, Random(100 − condition)/10)`**; Winter: `min(5, 2·dmg)`; rough sea: `min(8, 3·dmg)` (Winter first, then rough, then coast); away from cities the damage becomes **`2·dmg + 1`** (Winter: a 1-in-20 spike to 30); next to an own city it is **halved** (`dmg/2`) — confirmed (formula from code; reproduced exactly in all 12 live cells, Wine-only) (2026-10-03-storms-and-losses-at-sea.md).
- If `dmg < 6`: condition −= dmg only; otherwise **ships and condition each lose `d/300`** of themselves with **`d = (10000/(dmg+100))² / 100`** in integer steps — confirmed (code + live, Wine-only) (2026-10-03-storms-and-losses-at-sea.md).
- **A fleet whose condition after storm damage is below 40 is lost at sea** (fleet removed, news "A fleet belonging to X is lost at sea."); the test runs **before** the out-of-supply decrement (fleets ended at 39 and survived) — confirmed (code + live, Wine-only) (2026-10-03-storms-and-losses-at-sea.md).
- Out of supplies: condition −= `Random(2)` — confirmed (code + live, Wine-only) (2026-10-03-storms-and-losses-at-sea.md).
- Loss rates at condition 45: rough sea **10 of 10** (certain), calm open water 6–7 of 10, next to an own city **0 of 10**; a natural unedited loss was observed (Ptolemaic, condition 52, turn 0727) — live (Wine-only; natural cells and one natural loss) (2026-10-03-storms-and-losses-at-sea.md).
- Rough-sea tiles last one turn (the paint is replaced every turn), so a fleet is at risk only where it sits at the tick — live (Wine-only) (2026-10-03-storms-and-losses-at-sea.md).
- An army aboard a fleet lost at sea is lost with it; aboard a surviving fleet it takes the `d` casualties above — at `d = 86` an 11,000-man mixed army was cut to one shrunken unit (22.6–31.2 % of its size) or to nothing — live (Wine-only) (2026-10-03-storms-and-losses-at-sea.md).

### Fleet joins, splits and transfers

- **Join proceeds only when `ships[selected] + ships[partner] < 100`; exactly 100 combined is refused** with "There are more than 100 ships in these fleets combined." (the message is wrong by one for that case); the AI's once-per-turn merge `FUN_00450b30` uses the same strict `< 100` — **[confirmed: decompile]** (2026-10-07-join-fleets-100-ships-boundary.md).
- Join is one click with no dialog: ships, supplies and money are carried over, the partner record is deleted, and **the survivor's moves are set to 0** — confirmed (decompile; live, Wine-only) (2026-10-07-join-fleets-100-ships-boundary.md; 2026-10-02-fleet-orders-live.md).
- Join refuses if either fleet is carrying an army ("You cannot join fleets if one is carrying an army.") — confirmed (decompile) (2026-10-07-join-fleets-100-ships-boundary.md).
- **Split fleet**: the dialog divides ships, supplies and money between the two columns; the new fleet appears on an adjacent tile with **0 moves** (one observation: (101,46) → (101,47)) — live (Wine-only) (2026-10-02-fleet-orders-live.md).
- **Transfer ships** moves ships between two adjacent fleets via the same two-column window (20/10 → 15/15) — live (Wine-only) (2026-10-02-fleet-orders-live.md).
- **Repair** at an own city costs **`ships × points / 5`** talents (30 ships, 3 points → 18) and zeroes the fleet's moves; refused away from an own city — live (Wine-only; formula from code) (2026-10-02-fleet-orders-live.md).
- **Supply fleet** moves tons from an adjacent own city to the fleet (100 tons: city 330 → 230, fleet 0 → 100) — live (Wine-only) (2026-10-02-fleet-orders-live.md).
- **Scuttle** asks "Are you sure you want to scuttle this fleet ?" (Yes/No/Cancel), requires proximity to an own city, and removes the fleet on Yes — live (Wine-only) (2026-10-02-fleet-orders-live.md).

### Upkeep

- Every deployed fleet costs **`shipCount × 3` talents charged once per season** (`owner.treasury -= shipCount × 3` in the quarterly billing); the Build dialog previews this same `n × 3` value — confirmed (decompile) (decompiled-fleet-tax-and-mercenary-formulas.md).

Open:

- The peace prompt for attacking a fleet ("Are you sure you want to attack this fleet ?" and the war declaration on Yes) was never exercised (2026-10-02-naval-battles.md; 2026-10-03-pair-2-seleucid-ptolemaic.md).
- Whether `random(4)` is uniform over 0–3 (win rates test it only in aggregate) and whether equal seeds share a draw across cells (2026-10-02-naval-battle-random-term.md).
- The cargo divisor: the data lean to `siegeStrength / 40` but `/50` is not excluded (the fit rests on duplicated cells sharing draws) (2026-10-02-naval-battle-army-aboard.md).
- The exact distribution of the winner's-army casualties and of the small-unit deletion pass (`FUN_0044AE20`, which units go when `d > 70`) — seen only in outcome (2026-10-02-naval-battle-army-aboard.md).
- The cargo's effect on moves (`troops/100/ships + 1` fewer) is untested; no battle was fought from a naturally embarked fleet (all T3 cargos were save edits) (2026-10-02-naval-battle-army-aboard.md).
- The New-Game fill that sets fleet moves to 25 has not been read from the code (2026-10-02-fleets-sail-and-drift.md).
- The P60-versus-C60 parity difference is unresolved; the strength exponent γ is consistent with 1 but pinned only to 1.0–1.2 (2026-10-02-naval-battle-random-term.md).
- The Winter 1-in-20 damage spike is neither confirmed nor excluded; the weather's own rolls were not measured (2026-10-03-storms-and-losses-at-sea.md).
- Whether a fleet on rough sea with its moves spent can leave (cost 3 per tile) was not run (2026-10-03-storms-and-losses-at-sea.md).
- The docked-fleet attack refusal was tested at one geometry (fleet diagonal to the city); other sides and a 2-tile distance were not tried (2026-10-03-pair-2-seleucid-ptolemaic.md).
- The exact meaning of the 333-vs-335-style marker distinction beyond owner+size band; several fleet-record words remain unlabelled (including word 3, nonzero only for the Carthage fleet in one sample); `OwnerCode` behaviour mid-construction is unverified (fleet-order-at-caere.md; fleet-owner-field-confirmed.md).
- Not tested live though the code reports state them: the 20-ship minimum for Split, the 100-ship Join cap at the boundary, Scuttle returning the fleet's money to the treasury and its supplies to the city; whether the new fleet's tile after Split is a rule (one observation) (2026-10-02-fleet-orders-live.md).

## Diplomacy and war

### The relation matrix and its writer

- Each nation record holds a 16-entry `short` array at `+0x26` with its relation toward every nation: `0` peace, `1` trade, `2` alliance, `3` war, `< 0` peace plus a cooldown counter that must climb back to 0 before trade or alliance is possible again (decompiled-diplomacy-peace-terms-and-instant-battles.md).
- On disk the row is at SAV nation-record `+0x26` (stride 1,172 = `0x494`, the runtime record written whole; leader name `+0x0B…+0x25`, 27 bytes) and at DAT nation-record `+0x0B` (stride 1,055); New Game never writes `+0x26`, so the starting relations are the DAT's matrix — symmetric, zero diagonal, 5 wars, 13 trades, 4 alliances, no cooldowns (decompiled-diplomacy-peace-terms-and-instant-battles.md).
- `FUN_00449B40(a, b, state)` is the single setter and writes both `[a][b]` and `[b][a]`, so the matrix is symmetric by construction (decompiled-diplomacy-peace-terms-and-instant-battles.md).
- Setting `state = 0` is translated into a cooldown by the previous state: trade → **−8**, alliance → **−24**, war → **−18**; a non-zero argument is stored as given, which is how the treaty writes −8 and −10 directly (decompiled-diplomacy-peace-terms-and-instant-battles.md, decompiled-war-cascade-and-peace-paths.md).
- Two one-step propagation rules live in the setter: setting **alliance** with `b` makes `a` declare war on every nation at war with `b` that `a` is not already at war with; setting **war** on `b` makes `a` declare war on every ally of `b` that `a` is not already at war with (decompiled-diplomacy-peace-terms-and-instant-battles.md).
- The cascade is **one step and does not recurse**: the dragged-in wars are two direct stores of `3` plus one news line from the nested procedure `FUN_00449A44`; nothing in the setter calls the setter (22 callers, none inside it). In an alliance chain A–B–C–D, a war on A reaches B only, never C or D (decompiled-war-cascade-and-peace-paths.md).
- Each nation also carries a 16-bit **neighbour mask** at `+0x46`, loaded from DAT nation-record `+0x2B` and never derived from the map: symmetric, no self-bits, 24 hand-authored pairs. Only conquest (`FUN_0044C528`) changes it during play, merging the loser's neighbours into the winner's mask in pairs. It gates the AI's war pick and treaty picks, the offer roll's alliance branch, the rebellion recipient and the peace cascade (dat-neighbour-mask.md).
- No code writes the relation matrix outside the setter except the rebirth routine's own row reset and `TPolitics_OK`'s diagonal (decompiled-war-cascade-and-peace-paths.md).

### The AI's own diplomacy (`FUN_0044FB7C`)

- The AI is "busy" (no war declaration, no alliance) while `atWar(me)` or `mobilization(me) > 40` or `season == 3` (Winter; the season reading is `[derived]`) (decompiled-ai-offers-to-human-seats.md).
- **War target:** among `k != me` with `unity[k] > 0` and `0 <= rel[k][me] < 3` (peace, trade or alliance), not busy, `not protected(k)`, and `me` in `neighbours(k)`, the best score `8·P(me)/max(1,P(k))` wins (`best` starts at 10). If a target exists, war is declared with chance `Random(10) == 0`, at most one declaration per turn. The war write has no AI-partner test, so the AI declares war on humans directly (decompiled-ai-offers-to-human-seats.md).
- **Protected:** `protected(k)` is true if `k` has an ally `a` with `cities[k] + cities[a] > cities[me]`. The declaring AI counts as its own ally's ally, so the AI's own war rule never picks a current ally that holds a city; an alliance can turn into war only through the setter's cascade (decompiled-ai-offers-to-human-seats.md).
- **Power formula:** `P(n) = (wealth +0x430 / 20000) × (unity +0x440 / 100)` (decompiled-ai-offers-to-human-seats.md).
- **Trade:** for `k` at peace with `me` (`rel == 0`) with `unity[k] > 0`, `trades(me) < 3`, `trades(k) < 3` and `k` AI, the relation is set to trade directly — no consent step. Every AI trade/alliance write checks the partner is AI (`+0x490 == 0`) (decompiled-ai-offers-to-human-seats.md).
- **Alliance:** when not busy, with chance `Random(20) == 0`, for a neighbour `j` of `me` with `0 <= rel[me][j] <= 1`, `unity[j] > 0`, not protected: ally with the **first** AI `m` that is at war with `j` (`rel[m][j] == 3`), `m != me`, `wars(m) < 2`, and `cities[j] < cities[me] + cities[m]` — the setter's cascade then brings the war on `j`. The AI allies only with a nation's enemy, never joins an ally's war otherwise (decompiled-ai-offers-to-human-seats.md).
- **Trade swap:** for each trade partner `s` of `me`, if a richer `k` exists with `rel[me][k] == 0`, `unity[k] > 0`, `taxBase[s] < taxBase[k]`, `trades(k) < 3` and `k` AI, the AI drops `s` to −8 and trades with `k`. Only the **new** partner is tested for being AI, so a **human** trade partner can be dropped to −8 without consent or news (decompiled-war-cascade-and-peace-paths.md).
- **The AI never writes peace over a war, with anyone.** The war-candidate loop only considers `0 <= rel < 3`, and there is no AI peace offer of any kind, not even a notice. AI–AI wars end only through the instant resolver's treaty or elimination (decompiled-war-cascade-and-peace-paths.md).
- AI armies and fleets never attack a nation they are not at war with (`rel == 3` gates every attack call), so there is no implicit declaration by attack (decompiled-ai-offers-to-human-seats.md).
- Toward a human seat the AI can do exactly two things: declare war, or raise the turn-start notice below. It never forms a treaty with a human on its own (decompiled-ai-offers-to-human-seats.md).

### The offer roll at a human turn start (`FUN_00452034`)

- At each human seat's turn start the pending offer is cleared, then `r = Random(16)`; an offer requires `rel[h][r] == 0`, `unity[r] > 0`, `Random(3) == 0` and `r` AI (decompiled-ai-offers-to-human-seats.md).
- **Trade test:** `floor = (trades(h) < 3) ? 0 : min taxBase over h's partners`; the offer is made if `taxBase[r] > floor` and `r` has a partner `k` with `taxBase[k] < taxBase[h]` ("r would swap a poorer partner for h") (decompiled-ai-offers-to-human-seats.md).
- **Alliance test (overrides trade):** `r` in `neighbours(h)` and `h` at war with nobody. No alliance offer has ever been observed (decompiled-ai-offers-to-human-seats.md).
- The offer is a **notice only**: `TPremierForm_StartTurn` shows "X wants to trade with Y." / "X wants to form an alliance with Y." in an OK-only `mtInformation` box whose modal result is discarded; no code writes the relation (decompiled-ai-offers-to-human-seats.md).
- Accepting means the human uses the Politics screen under the ordinary rules; the pending trade offer's only mechanical effect is to waive the proposer's three-partner refusal in `TPolitics_MakeTrade` (the proposer then drops its poorest partner on OK). An alliance offer has no mechanical effect — nothing reads it after the dialog (decompiled-ai-offers-to-human-seats.md).
- Doing nothing lets the offer lapse: the next human turn start clears it whether or not anything was done. In 4 of 4 offer → next-save pairs the offer is gone and the relation is still 0. Loading a save re-announces a stored offer (via `StartTurn` directly), unless the relation already equals the offer type (decompiled-ai-offers-to-human-seats.md, news-log-format-and-messages.md).

### The human's Politics screen (`TPolitics`)

- `TPolitics_ChangeIR` dispatches only when the clicked value differs from the working row; `TPolitics_OK` commits each changed cell through the setter. A cell goes through if the committed value is ≥ 0 or the new value is war, so a cooldown (`< 0`) can be overwritten only by war (decompiled-war-cascade-and-peace-paths.md).
- **Trade** (`TPolitics_MakeTrade`) refuses in four cases: the human already has 3 partners ("You can only trade with 3 nations."); the relation is negative ("X does not want to trade with you."); the relation is above 1 ("You cannot trade with X."); the target already has 3 partners **and** there is no pending trade offer from that target. There is no other AI willingness test. On OK, if the target has 3 partners, it drops its lowest-tax-base partner to peace (−8) (decompiled-ai-offers-to-human-seats.md, decompiled-diplomacy-peace-terms-and-instant-battles.md).
- **Alliance** (`TPolitics_MakeAlliance`): a human target is always accepted (hotseat). An AI target refuses ("X does not want to ally with your nation.") when the human's working row contains a war, or any nation the working row marks allied is at war with anyone, or the human is at war in the committed matrix, or the relation is negative. **The AI target's own wars are not checked**, so allying with an AI at war drags the human into that war through the cascade (decompiled-ai-offers-to-human-seats.md).
- **Peace** (`TPolitics_MakePeace`): refused with "X does not want to make peace at this time." if the target is AI (`+0x490 == 0`) and currently at war; a human (hotseat) target always accepts; otherwise the working value goes to 0 and the setter maps it to the cooldown (trade −8, alliance −24). A click is also ignored if the target is the human itself, the value is unchanged, or the target's unity ≤ 0 (decompiled-war-cascade-and-peace-paths.md, decompiled-diplomacy-peace-terms-and-instant-battles.md).
- Against an AI the human can end a trade (→ −8) or an alliance (→ −24) at will and **cannot** end a war; against another human, all three are accepted. Ending a trade, an alliance or a hotseat war from this screen writes no news line — the setter emits news only for alliance and war (decompiled-war-cascade-and-peace-paths.md).
- **War** is set directly, no check. Declaring war is not only done here: clicking an enemy city, army or fleet with a unit selected (`TUnitMap_SelectUnit`) prompts "Are you sure you want to attack this …?" and on Yes calls the setter with 3 before resolving the attack — attacking is declaring war, with the one-step ally cascade. No box appears when already at war; No and Cancel change nothing; between two human seats a war order is immediate and symmetric (decompiled-diplomacy-peace-terms-and-instant-battles.md, 2026-10-03-fleet-peace-prompt.md).

### Paths that end or change a relation

- **Post-battle treaty (`FUN_00450C68`)** — the only path that ends a live human–AI war, and it needs the human's Yes. After a tactical battle (human-involved by definition), `TBattleOver_OK` shows the `TBattlePols` "Offer of peace" dialog only if `armies(W) < armies(L)`, `unity(L) > 500`, `cities(L) > 7`, and then `Random(5) < 2` — the draw is made only if the three tests pass (code: decompiled-war-cascade-and-peace-paths.md; thresholds and draw measured: 2026-10-05-battle-peace-offer.md).
- `TBattlePols_Yes` calls the treaty; `No` does nothing and the war goes on. Measured, Yes changes only the 2 relation words (3 → **−18** both directions) plus one news line "<Winner> and <Loser> have agreed to end their war."; on the next End turn the −18 becomes −14 (the quarterly thaw) (2026-10-05-battle-peace-offer.md).
- The dialog's own gate (`armies(W) < armies(L)`) makes a treaty reached through `TBattlePols` **always the honourable branch** — no reparations; the dialog's reparation lines are unreachable in play (decompiled-war-cascade-and-peace-paths.md, derived; observed honourable-only in the 2026-10-04 probes).
- **Reparations (AI–AI only):** `W = taxBase(loser)` (`+0x44C`); `reparations = W/4 + Random(W/4) + cities(loser) × 10`. The sues branch is taken when `score(W) >= score(L)` **and** `armies(W) >= armies(L)`, with `score(n) = (wealth +0x430 / 100) × unity +0x440` and `armies(n)` the sum of field strength over n's armies; it writes the four "sues" news lines, sets every loser trade/alliance to **−10**, and moves the money. Otherwise the honourable line and nothing paid. Formula confirmed in code, unverified against the one save data point (decompiled-diplomacy-peace-terms-and-instant-battles.md).
- The treaty sets `RandSeed := winner + loser` before the draw (both in the dialog preview and the payment, so they always agree); the reparation for a given pair and tax base is deterministic, and every treaty resets the global random stream (decompiled-war-cascade-and-peace-paths.md).
- **AI–AI treaty trigger:** after a decisive instant AI-vs-AI field battle, `Random(5) < 2` is drawn **first**, then `unity(loser) > 500 && cities(loser) > 7`; there is no armies test, so both branches are reachable (decompiled-war-cascade-and-peace-paths.md).
- **Treaty ally loop:** for each `k` allied to one side and at war with the other, the side's alliance with `k` is first written to **−8 with no gate** (every such ally loses the alliance). Only then, if `k` does not border the enemy and is not human, is `k`'s war also written to −8 with the news "<enemy> and <k> have agreed to end their war." — enemy named first, the two halves interleaved per `k`. A bordering or human ally loses the alliance **and** stays at war. The loser's half cannot fire after a sues branch (which already wrote −10 over the loser's alliances) (decompiled-war-cascade-and-peace-paths.md, dat-neighbour-mask.md).
- **AI–AI treaty touching humans without consent:** a human allied to the winner and at war with the loser has that alliance written to −8 and stays at war; likewise the loser's human ally in the honourable branch; the sues branch sends the loser's trades and alliances with everyone, humans included, to −10 (decompiled-war-cascade-and-peace-paths.md).
- **Hotseat battles make no peace:** `THVHBatPols_OK` moves the agreed money and writes no relation (decompiled-war-cascade-and-peace-paths.md).
- **Elimination** (`FUN_0044BED8` / `FUN_0044C528`) resets every relation of the eliminated nation: war → −18, other cooldowns → 0; nobody consents, and it ends a war only because one side has ceased to exist. Conquest also merges the loser's neighbour mask into the winner's (decompiled-war-cascade-and-peace-paths.md, dat-neighbour-mask.md).
- **Leader falls** (`FUN_0044C8F0`): the fallen nation's relations of −5…−1 go to 0; **rebirth** (`FUN_0044C360`) writes −8 between the reborn nation and each defecting city's owner; neither moves a war (decompiled-war-cascade-and-peace-paths.md).
- **Quarterly thaw** (`FUN_00451B40`): each negative entry gets `v += 1`, and with probability 1/3, `v = min(0, v + 3)`. The loop runs only over the **first 8 columns** of each row, so a cooldown between two nations both indexed ≥ 8 never decays — an original bug a reimplementation must decide about consciously (decompiled-diplomacy-peace-terms-and-instant-battles.md).
- The AI trade swap (dropping a human partner to −8, above) is the one other consent-free write that touches a human; none of these paths ends a war by anyone's decision (decompiled-war-cascade-and-peace-paths.md).

### Diplomacy news lines

- The setter emits news only for alliance and war: "A forms an alliance with B." and "A declares war on B." — the dragged-in cascade wars each get their own "A declares war on K." line, written in the setter's order (the declaration on `b` first, then the allies). Trade and peace/cooldown writes produce no news, so a new trade agreement is never in the news (decompiled-war-cascade-and-peace-paths.md, news-log-format-and-messages.md).
- A war declaration is upper-cased in full (ASCII `StrUpper`) when either nation is human: "PTOLEMAIC DECLARES WAR ON CARTHAGE." Alliances are never uppercased (news-log-format-and-messages.md, observed live in 2026-10-03-fleet-peace-prompt.md).
- Treaty lines: "A and B have agreed to end their war." (honourable, and for each ally that also makes peace, enemy named first); the sues branch writes "B sues A for peace and;", "    B ends all current trading agreements.", "    B  ends all current alliances." (4-space indent, double space in the alliances line), and "    B pays reparations of N talents." with N comma-grouped by the game's own formatter, locale-independent (news-log-format-and-messages.md).
- Diplomatic offers are never news: the pending trade/alliance offer is announced only by the turn-start modal dialog, and no news slot in any save contains "wants" (news-log-format-and-messages.md).
- Observed live (Wine-only): a fleet attack at trade terms produced "PTOLEMAIC DECLARES WAR ON CARTHAGE.", "PTOLEMAIC DECLARES WAR ON NUMIDIA." (the target's ally, one step only), then "Carthage sinks fleet of Ptolemaic." in that order (2026-10-03-fleet-peace-prompt.md).

Open:

- Whether a nation with `unity > 0` but 0 cities can exist — the only case where the "ally is protected" test could fail for a direct ally; not checked (decompiled-ai-offers-to-human-seats.md).
- An alliance offer, and a cascade that turns an alliance into war, have never been observed in a save; both are code-only. An upper-case war declaration has been observed only under Wine, never in a desktop-original save (decompiled-ai-offers-to-human-seats.md, news-log-format-and-messages.md).
- The reparations formula is confirmed in code but not verified against the one recorded payment (the loser's tax base and city count were not read back from the pre-treaty save) (decompiled-diplomacy-peace-terms-and-instant-battles.md).
- Whether the ungated partner–ally −8 in the treaty's ally loop is intended is not argued; the ally loop was never exercised in the live battle probes (decompiled-war-cascade-and-peace-paths.md, 2026-10-05-battle-peace-offer.md).
- The attack confirmation was tested only at trade terms (1): peace, alliance and cooldown values were not, and an attack on an ally may be refused outright; the cascade's reach beyond one step was predicted from code, not observed (2026-10-03-fleet-peace-prompt.md).
- The `TBattlePols` results (open rate, Yes/No diff, thresholds) are Wine-only; `armies(W) == armies(L)`, human-versus-human `THVHBatPols` and more than one box per turn were not tested (2026-10-05-battle-peace-offer.md).
- The conquest merge of the neighbour mask has never been observed changing a mask (the one conquest in the saves is a no-op for it), and only one DAT/scenario exists locally (dat-neighbour-mask.md).
- The "season 3 = Winter" reading is derived, and the war rule's other terms (power ratio, neighbour test, 1-in-10 chance) were not tested against save pairs (decompiled-ai-offers-to-human-seats.md).

## Tactical battle

### When a tactical battle happens (vs the instant resolver)

- AI-vs-AI fights are resolved by the instant resolver `FUN_0044AEE4`; a tactical battle (`TBattleMap`) always has a human side (battle-quality-promotion-and-morale-array-decompiled.md, `[confirmed]`).
- The battle screen opens only from army-attacks-army (`FUN_0044AEE4`) or from loading a save with the battle flag set; there are no siege battles (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: whole-CODE E8 scan]`).
- The instant path is a whole-army ratio, not the tactical model: power `= Σ(weight[type] × troops / 100) / 80 × morale[+14]` with **no quality term**; the stronger side wins (tie to the defender) and the winner's loss ratio is `weakerPower × 40 / strongerPower`, capped at 40; after the per-unit loss `FUN_0044AE20` deletes units below `standardBattalionSize / 10` (national) or `/ 5` (mercenary) (instant-resolver-cannot-reproduce-a-tactical-battle.md, `[confirmed]` code, `[derived]` numbers).
- The instant resolver cannot reproduce a tactical outcome: its per-type rates are locked within a ±7% band, and a recorded tactical battle's spread (archers 100% vs heavy cavalry 4%) is unreachable at any ratio (instant-resolver-cannot-reproduce-a-tactical-battle.md).
- The two paths are distinguishable in text: the tactical result header reads "X's army defeats Y's army", the instant resolver's "X destroys army of Y" (battle-replayed-rout-mechanic-and-combat-constants.md).
- No terrain: the battle module never reads the strategic map or terrain table; every empty cell is grass. No turn limit, no retreat; a battle ends only when one side has no live unit (or Surrender) (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- A mid-battle File → Save As writes a 2,105-byte block 12 (9 header bytes, 40 slots × 44 bytes, 14×12 icon grid) and the battle continues; File → Open resumes it, but not as a continuation: the resume path re-runs the half-round setup, incrementing the counter, refilling moves and dropping the pending melee (2026-10-04-battle-probe.md; 2026-10-04-decompiled-tactical-battle-rules.md, `[derived from code]`).

### Battle start: copy-in, morale, deployment

- The 14×12 grid alternates sides; the defender places first (half-round 1), the attacker second (half-round 2) and then moves first (half-round 3) (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Before copy-in, each side whose **own** nation is computer-controlled gets its strategic army morale (`+14`) `+= 3` (persistent, no clamp), its 20 unit records selection-sorted descending by `troops · M[type][0] div M[0][type]`, and its nation adopts the opponent's two battle-delay settings (battle-quality-promotion-and-morale-array-decompiled.md, `[confirmed]`; 2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Initial per-unit tactical morale: `morale = max(60, min(90, Random(quality × 4) + armyMorale[+14]))` (battle-quality-promotion-and-morale-array-decompiled.md, `[confirmed]` at instruction level).
- Initial shots by type: LI 7, HI 0, archers 25, LC 9, HC 0; moves 4/2/4/6/5 (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Human placement: click unit, click an empty cell in the side's home rows (attacker `y < 3`, defender `y > 8`); free and repeatable; not placing keeps copy-in positions (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Unit icons: 5 types × 3 sizes; `size = min(2, troops div (standardBattalion div 3))` — thresholds LI 5,000/10,000, HI 2,000/4,000, Ar 1,166/2,332, LC 2,333/4,666, HC 833/1,666, confirmed exact on both sides (2026-10-04-decompiled-tactical-battle-rules.md `[confirmed: code]`; 2026-10-04-tactical-battle-sweep.md `[O]`).

### The exchange formulas

**Shooting** (`FUN_0043910C`, `[confirmed: code]`, replayed exactly in 318 hooked battles):

- Shooters: LI (range 1), archers (range 2), LC (range 1); test is `distance ≤ range`, no line-of-sight check; a shot costs 1 shot and 1 move.
- `base = (tr_s·q_s·m_s·vuln[type_t]) div (tr_s·5 + 150000)`; doubled if `dist < range` (only archers at distance 1); `n = min(base, min(tr_s div 3, tr_t div 2)) + 1`; `loss = Random(n) + Random(n)`; target morale `-= min(3, (loss·35) div (tr_t + 1))` (troops before the loss); then the rout check.
- `vuln` (stat `+0x20`, indexed by target type): LI 18, HI 2, Ar 18, LC 15, HC 4 — unarmoured targets take nine times heavy infantry's fire (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed — identification]`).

**Melee** (`FUN_004393EC`, resolved at the end of the mover's half-round for each own slot in order with a live target):

- `f = min(4, focus count)` — the focus-fire counter saturates at four attackers (a ceiling, not a floor) (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]`).
- `A = (M[ta][td]·tr_a·(q_a·10 + m_a)) div 2000 + 12`; `D = (M[td][ta]·tr_d·(q_d·10 + m_d)) div 2000 + 12` — the quality term is literally `quality × 10 + morale` (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]`).
- Attacker loss: `nA = ((tr_a·D) div A) div 12 + 1`; `la = min(30000, ((Random(nA)+Random(nA))·(5−f)) div 5)`; `la = min(la, (tr_a·4) div 10) + 1`.
- Defender loss: `nD = ((tr_d·A) div D) div 10 + 1`; `ld = min(30000, ((Random(nD)+Random(nD))·(2f+5)) div 5)`; `ld = min(ld, (tr_d·4) div 10) + 1`.
- **Both sides lose troops simultaneously** in one resolution (decompiled-combat-formula-structure.md).
- The 40%-of-own-troops cap `⌊0.4 × troops⌋ + 1` is confirmed to the integer on eleven observations across two recordings and both sides (battle-recording-melee-cap-confirmed.md, `[confirmed]` exact; battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]` on the attacker side).
- With `f` focus attackers the attacker-loss multiplier is `(5−f)/5` and the defender's `(2f+5)/5`: a fourth attacker is worth 3.25× damage and a fifth of the return fire; a fifth adds nothing (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]`).
- Because both caps are 40% of the side's own troops, a unit is never ground to exactly zero by the loss formula — troops only asymptote toward 1 (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed, corrects a prior report]`).
- A matrix value of 0 only removes the type multiplier, leaving the `+12` floor (combat-type-effectiveness-matrix.md).

### The 5×5 type matrix

- The melee code reads `DAT_0047946C`, filled from **DAT offset `0x1F7A6`** (not `0x1F3B8`, which holds the AI placement formations and type order). Real `M[attacker][defender]` (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code + DAT loader]`):

| Att \ def | LI | HI | Ar | LC | HC |
| --- | ---: | ---: | ---: | ---: | ---: |
| LI | 15 | 4 | 20 | 5 | 3 |
| HI | 60 | 5 | 65 | 15 | 8 |
| Ar | 10 | 3 | 18 | 5 | 3 |
| LC | 25 | 8 | 28 | 15 | 8 |
| HC | 18 | 12 | 20 | 12 | 8 |

- Orientation `value[attackerType][defenderType]` (10-byte row stride on attacker, 2-byte column on defender) is settled from the index arithmetic; only the real matrix reproduces the recorded LI-vs-HI exchange that hit the attacker's cap (battle-replayed-rout-mechanic-and-combat-constants.md `[confirmed]`; 2026-10-04-decompiled-tactical-battle-rules.md).
- Mutation checks on real battles: changing `M[hi][hi]` 5→6 makes 4 of 63 replayed melees miss; `vuln[li]`→17 makes 37 of 80 shots miss (2026-10-04-battle-exchange-hook.md, `[D]`, Wine-only).

### Morale effects and the rout mechanic

- Melee morale: the side that lost the larger troop fraction (integer `troops div loss`) takes −3, the other +2; **ties go against the attacker**; clamped at 99 (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`, correcting the earlier "better power ratio" reading).
- Shot hit: target `−min(3, ⌊35·loss/(troops+1)⌋)` — at most 3 morale per shot (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]`).
- Rout (`FUN_00438FB0`, called on both melee participants after each exchange and on the shot target): a unit survives if `troops ≥ standardBattalionSize / 25` **and** (`morale > 39`, or `morale > 19` and `Random(m) + Random(m) > 29`); otherwise it is removed (troops 0, cell cleared) (battle-replayed-rout-mechanic-and-combat-constants.md; 2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Rout thresholds (`std / 25`): LI 600, HI 240, Ar 140, LC 280, HC 100; both observed routs land exactly below their threshold (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]`).
- Cascade, one level deep: every live friendly unit −6 morale, any left below 30 removed (no further cascade, no +5 for these); every live enemy +5 capped at 99, and units targeting the routed one clear their target; if either side empties, the battle ends (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]` code, cascade itself `[open]` to direct observation).
- Morale is a second, independent kill condition: automatic rout at morale ≤ 19 at any strength, a coin-flip-ish check in 20–39 (battle-replayed-rout-mechanic-and-combat-constants.md).
- There is no morale floor and no recovery between half-rounds (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Surrender removes every own unit with no cascade and ends the battle (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- The winner: attacker if any attacker slot has troops > 0, else defender; if both emptied the defender "wins" with no units (2026-10-04-decompiled-tactical-battle-rules.md, `[derived: unexercised edge]`).

### Quality promotion

- `TBattleOver_OK` sets each surviving winner unit's quality to `max(6, q)`, then raises it by 1 (to at most 9) on `Random(4) = 0` (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- This supersedes two earlier readings: the withdrawn "adjacency rule" (average-quality units next to a destroyed slot promoted — a 1-in-84 coincidence of one battle) and the empirical 1-in-4 model inferred from 30 survivors (battle-replayed-rout-mechanic-and-combat-constants.md, `[derived, supersedes a prior derived rule]`).
- Promotion happens after the battle, not incrementally during it (full-battle-resolution-rome-vs-gaul.md).

### The battle AI (ComputerGeneral)

- `TBattleMap_ComputerGeneral` sets a "which side is thinking" flag; `FUN_00439c84` repeats the AI move until a human's turn or battle end; there is no initiative stat — sides alternate, attacker first (decompiled-combat-formula-structure.md; 2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Half-round setup resets moves and targets; a computer side's non-HI units get `moves = 1` (the slow advance) while the minimum enemy distance `dmin > 2` and the half-round counter `< 10` (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`; confirmed in saves by 2026-10-04-tactical-battle-sweep.md).
- AI placement draws `r = Random(5)` and fills 3-column blocks by type from the DAT `Form` table (rows: HC/HI+Ar/LI/LC; LI/HI+Ar/HC/LC; LC/HC/LI/HI+Ar; LC/LI/HI+Ar/HC; HC/LC/HI+Ar/LI), rows stepping inward; blocks with more than 9 units stack on occupied cells; archers continue HI's block (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- The AI move half-round (`FUN_0043A31C`) takes types in the order HI, HC, LC, LI, archers, units of a type in slot order (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Target choice by type: LI prefers archers, then LI, then any; HI and HC prefer HI, then any; archers and LC take any. Score: minimum of `v = tr·q·m·M[their][my] div 10000` among live enemies of the wanted type, then `v div (claims+1)` while claims < 4, else `v·2`; ties to the first (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Engage: archers with shots at distance < 3 fire until out of moves/shots or target removed; else if adjacent, shoot while shots > 0 then set the melee target; else move toward the target, or toward the nearest empty cell with a clear line in a (2r+1)² box around it (r = 2 for archers) (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Pass 2: units with shots pick the in-range enemy minimising `troops div shotBound` (+ `shotBound div 4` if the enemy has shots) and fire until moves = 0 or target removed — this loop does not check shots, so shots can go negative; then take as melee target the adjacent enemy minimising `theirs − focus·theirs`, subject to `2·theirs' div 3 < mine` (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Pass 3 adds a flank move: horizontal direction from the enemy span, flipped on `Random(3) = 0`, vertical from enemy counts, tried clamped with a clear-line requirement; then pass 2 twice (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Movement is an 8-connected Bresenham line, 1 move per step, with fixed detour rules and a cost of 10 for off-path cells; a computer-controlled unit with a target does not move, and forfeits its **last** move if a ≥-as-strong enemy is in the 3×3 around the next path cell (`S = (troops·q div 100)·m·M[me][them]`) (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Melee target setting costs no move; moving clears the target (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- The tactical resolver is strongly stochastic: the same armies from identical bytes differ by a third of the total loss and by which units die — parity tests must be distribution tests (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]`).

### Draw order of all Random sites

- 12 sites in the module (`0x43801A, 0x43812F, 0x43820D, 0x438FFB, 0x439006, 0x439188, 0x439191, 0x439557, 0x43955F, 0x4395CE, 0x4395D8, 0x43AA88`) plus two after the battle (`0x4592BD`, `0x45951C`), confirmed by an E8 scan (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Order: (1) copy-in `Random(q·4)` per live attacker slot 0–19, then per defender slot — `Random(0)` still advances the seed; (2) `Random(5)` per computer-controlled placement half-round; (3) per shot `Random(n)` twice, then the target's rout test; each rout test draws 2, only when `troops ≥ floor` and `20 ≤ m ≤ 39`; each flank `Random(3)`; (4) at each half-round end, per melee 4 draws (attacker, attacker, defender, defender), then Rout(attacker), Rout(defender); (5) after the battle `Random(4)` per surviving winner unit in slot order, then the possible `Random(5)`; `TBattlePols` then reseeds (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- The exchange hook observed this order with **no mismatch in 318 battles** (52,787 records, 0 seed-chain breaks): every shot, melee and rout range equals the formulas, and the replay reproduces every slot of every half-round — 9,339 of 9,339 exchanges (2026-10-04-battle-exchange-hook.md, formulas `[D]`, Wine-only; observations `[O]`).
- The battle flag is cleared at `0x437B8C` (never `0x45C21F` in 318 battles); the reseed `0x457907` fires only when the Offer-of-peace box opens (2026-10-04-battle-exchange-hook.md, observed).
- The random stream is consumed by the exchanges, not by movement: five different geometries of the same HI-v-HI battle end in the same post-battle save (2026-10-04-tactical-battle-sweep.md, `[D]`, Wine-only).

### Write-back to the strategic map

- The result dialog shows per-type and total start/finish, captured talents, and "suuplies" (sic); the winner's finish matches the save diff exactly (full-battle-resolution-rome-vs-gaul.md; battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]`).
- `TBattleOver_OK`, in order: zero the winner's unit troops, copy the surviving battle slots back compacted in slot order (origin, type, troops, name) with the promotion roll; winner's money += loser's money; winner's supplies += loser's supplies, capped at `totalTroops div 100`; redraw the winner's marker; delete the loser army (tombstone); unity: winner `min(990, +25)`, loser `−25`; news "W destroys army of L." (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: TBattleOver_InitializeForm/OK]`).
- The ±25 unity swing and `attacker.moves = 0` (set by `FUN_0044AEE4` before the battle) fire on the tactical path exactly as in the instant resolver's code; the loser's army record is tombstoned with the `0xFFFF` owner during the turn and compacted out by the end-of-turn tick — mid-turn saves should be expected to carry tombstones (battle-replayed-rout-mechanic-and-combat-constants.md, `[confirmed]`).
- The supply-cap identity `supplyCapacityTons = totalTroops / 100` holds exactly after battle (battle-replayed-rout-mechanic-and-combat-constants.md).
- There is no other strategic morale change: the AI army's copy-in `+3` stays, and the winner's strategic `+14` is untouched (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).

### The post-battle peace-offer gate

- After OK, a human–AI battle with `strength(W) < strength(L)`, `unity(L) > 500` and `cities(L) > 7` draws `Random(5) < 2`; if it passes, the "Offer of peace" window (`TBattlePols`, an honourable peace with no reparations) opens; human vs human always shows `THVHBatPols` (2026-10-04-decompiled-tactical-battle-rules.md, `[confirmed: code]`).
- Observed: the box appeared in 3 of 16 logged defeats (one seeded 40% draw per battle, identical across runs of a seed) and in 76 of 315 sweep rows, always after a Gaul win, always captured and declined (2026-10-04-battle-probe.md, observed; 2026-10-04-tactical-battle-sweep.md `[O]`, Wine-only).
- The box opened exactly when the peace draw was < 2 — 77 of 77 times (2026-10-04-battle-exchange-hook.md, observed).
- Answering No closes it and the war continues (relations unchanged, no news line); Yes was never tried (2026-10-04-battle-probe.md).

Open:

- The un-capped raw melee output is not independently re-derived from the random-roll term (only cap-hitting cases are pinned exactly) (battle-recording-melee-cap-confirmed.md).
- Whether the rout check's 20–39 morale branch or the cascade was actually exercised in the recorded battles, and which branch removed specific units in battle 1 — not settled; the cascade's −6/+5 has no direct observation (battle-replayed-rout-mechanic-and-combat-constants.md).
- Whether the instant path's small-unit deletion (`/10` national, `/5` mercenary) can lift a winner's total above the ratio — needs unit-level rosters (instant-resolver-cannot-reproduce-a-tactical-battle.md).
- Win rates/odds: the sweep's 3 seeds per cell describe how battles unfold, not probabilities; mixed armies, swapped sides, terrain and human play are not covered; everything in the sweep, probe and hook is Wine-only, a candidate until the desktop original confirms it (2026-10-04-tactical-battle-sweep.md; 2026-10-04-battle-probe.md; 2026-10-04-battle-exchange-hook.md).
- The AI general's *choices* (who it targets, where it moves) are observed from snapshots, not independently decompiled; the flank draw count is not predictable from snapshots (2026-10-04-battle-exchange-hook.md; 2026-10-04-tactical-battle-sweep.md).
- What follows a Yes on the Offer of peace, and the full terms-row text beyond the clipped label, were not observed (2026-10-04-battle-probe.md).
- The `TInformation` window's pixel layout, and the int32 wrap the decompile warns about (melee `tr·D` above ~23,000 troops against a high-power defender), were not exercised (2026-10-04-decompiled-tactical-battle-rules.md, `[derived]`).

## The computer seat's turn

Source: 2026-10-07-strategic-ai-turn.md (decompilation of `FUN_0044fa20` and its callees, read from `all_app_functions.txt`).

### Seat loop and phase order

- `TPremierForm_EndTurn` advances the seat index, reloads the current nation from the 16-entry turn-order table `DAT_0049efe8`, and on wrap to seat 0 runs the weekly tick (2026-10-07-strategic-ai-turn.md).
- `FUN_00451fdc` compacts dead armies/fleets (`owner == -1`), then loops while the current seat is a computer (`+0x490 == 0`) and the game is not over, calling `FUN_0044fa20` once per seat; it breaks if `FUN_00449050` finds no human seat left anywhere (2026-10-07-strategic-ai-turn.md).
- `FUN_0044fa20` is guarded by `unity (+0x440) > 0` — an eliminated nation's seat advances silently — and runs exactly four phases per nation, in fixed order: **1. diplomacy (`FUN_0044fb7c`), 2. economy (`FUN_0044ffbc`), 3. armies (`FUN_0044f31c`), 4. fleets (`FUN_0044f608`)**, then advances the seat index itself (2026-10-07-strategic-ai-turn.md).
- Within the army and fleet phases the loop is per unit, in table order, each unit decided and moved once; there is no planning pass and no re-evaluation loop — each army is scored against the state left by the previous army (2026-10-07-strategic-ai-turn.md).
- `DAT_004a0340` is set 0 at the top of the army phase and 1 at the top of the fleet phase — a global phase-mode flag the movement helpers read [confirmed: decompile; the readers were not traced] (2026-10-07-strategic-ai-turn.md).
- Cross-reference, one line: the diplomacy phase's gates (power-ratio `8·P(me)/max(1,P(k)) > best` war target, `Random(10)` war / `Random(20)` alliance, AI-only trade/alliance writes, war writable against humans) are covered by §1a of decompiled-ai-offers-to-human-seats.md.

### The threat-versus-own budget (economy phase)

- `threat = 15000 × (nations at war with me) + Σ FUN_0044a8cc(a) over every army of a nation at war with me + Σ value/4 over foreign armies within 10 of my capital + Σ value/2 over armies at war within 20 of my capital` (both sums rounded down) (2026-10-07-strategic-ai-turn.md).
- `own = 6000 × (number of allies) + Σ FUN_0044a8cc(a) over my armies + Σ value/2 over allied armies`; distances are Chebyshev from the capital city (`+0x444`) (2026-10-07-strategic-ai-turn.md).
- If `own < threat`, the deficit `threat − own` is passed as the budget to the recruit-and-mobilise routine `FUN_004504f4` (2026-10-07-strategic-ai-turn.md).
- `FUN_0044a8cc` is the per-type AI combat value `(troops/100) × DAT_00478FD6[type]` (2026-10-07-strategic-ai-turn.md).
- Cross-reference, one line: that routine's mobilise passes (only fully ready slots `state == 24`, no-army-nearby mobilise only once ≥ 4 slots ready, spend until the deficit budget is met) are §4 of decompiled-mobilization-and-mercenary-restock.md.

### Recruit-and-mobilise gates: deficit floor, order cap, city placement

- **Deficit spending**: a new order may be placed while `treasury > wealth(+0x430) / −500`, i.e. the treasury may go up to `wealth/500` into the red; below that floor an AI may still place **at most 3 orders per turn** (`sVar9 < 3`) (2026-10-07-strategic-ai-turn.md).
- **Order cap**: at most **8 new orders per turn** (`sVar9 < 8`), each charged `(troops/200) × initialPrice[type]` exactly like the player's dialog, each raising mobilisation by the identical increment (2026-10-07-strategic-ai-turn.md).
- **City placement** (`FUN_004502e0`): the capital by default; when at war, an own army sits within 15 of the capital, and more than a third of all queued orders already sit at the capital, new orders go instead to the own city with **fortification ≥ 75** that has fewer queued orders than the capital and lies nearest to an enemy capital [confirmed: decompile] (2026-10-07-strategic-ai-turn.md).
- Order fill (`FUN_004501f4`): unit type by `Random(100)` buckets — Foot < 35, Guards 35–59, Bowmen 60–74, Lancers 75–89, Dragoons 90–99 — and troops `= standardSize/3 + Random(standardSize × 4/5)` rounded down to a multiple of 100 [confirmed: decompile] (2026-10-07-strategic-ai-turn.md).

### The week-11 tax policy

- The block runs only when `DAT_004a0330 == 0xb` — the last week of the season, immediately before the quarterly tick (`(week+2) mod 12 == 11` in the weekly tick's numbering) (2026-10-07-strategic-ai-turn.md).
- `if (unity < 650 or treasury > wealth/2000): tax = max(5, tax − 6)` (2026-10-07-strategic-ai-turn.md).
- `if (treasury < 0 or (own ≤ threat and treasury < 1000)): tax = min(40, tax + 9)` (2026-10-07-strategic-ai-turn.md).
- `if (treasury > 0 and unity < 500): tax = 0` (2026-10-07-strategic-ai-turn.md).
- The AI writes the same `+0x44A` tax-rate field the human's Taxation slider sets (0–40), once per season [confirmed: decompile] (2026-10-07-strategic-ai-turn.md).

### The four tail sub-phases (end of economy)

- **Fleet construction** `FUN_00450768`: orders a new fleet with ships `= min(100, cities + 50)` [derived: the size parameter's meaning]; gates: fleet count < 99, treasury > 3000, and fleet score (own fleet +1, at sea +4) is 0, or 1 with > 50 cities, or 2 with > 100 cities; port from `FUN_004496e0`: own coastal city with a free adjacent water cell, nearest the capital, not already hosting a construction order (2026-10-07-strategic-ai-turn.md).
- **Unit consolidation** `FUN_00450858`: per unit slot of all own armies, a regular unit (origin label 0) below ⅔ standard size merges with the next same-type slot below ⅓ (quality averaged); a mercenary unit below ⅙ standard is disbanded (2026-10-07-strategic-ai-turn.md).
- **Army merge** `FUN_004509f0`: the smaller army (< 20,000 troops, not aboard a fleet, with orders outstanding) is absorbed by an own army within 18 if combined slots < 20 and target < 80,000 troops and not aboard; purses and supplies carry over; **one merge per turn** (2026-10-07-strategic-ai-turn.md).
- **Fleet merge** `FUN_00450b30`: an idle fleet (ships < 40, no army aboard, no destination) is absorbed by an own fleet within 34 if combined ships < 100 and the target is free the same way; **one merge per turn** (2026-10-07-strategic-ai-turn.md).

### The army phase

**Homeland defence dispatch** (`FUN_0044efc8`, before the per-army loop):
- Builds a list of up to 9 **threatening armies**: foreign, in the capital's region (the region and coast boxes of `FUN_0044eb18`), within 20 of the capital if at war, within 10 otherwise (2026-10-07-strategic-ai-turn.md).
- Up to `threats + 2` own armies that still have moves and are not committed to a reachable attack (no army or city target scoring ≥ 100 reachable this turn, or the capital within 3× their moves) are dispatched toward the nearest threatening army if it is at war and on land, otherwise back to the capital (2026-10-07-strategic-ai-turn.md).
- A threat aboard a fleet cannot be intercepted — the responder goes to the capital (2026-10-07-strategic-ai-turn.md).

**Resupply and free mercenary hire** (`FUN_0044e41c`, every own army, over the 334 cities within Chebyshev 4):
- Own city: the army takes `min(troops/100 − supplies, city supply stock)` tons free; its purse is then normalised against the national treasury — surplus above 1000 deposited, below 500 topped up by 500 while the treasury is positive (this is the mechanism behind the army-purse 1000 cap) (2026-10-07-strategic-ai-turn.md).
- Foreign city not at war: the same tonnage is bought — capped at `money/5`, paid at `amount/5` talents into the city owner's national treasury (2026-10-07-strategic-ai-turn.md).
- Mercenaries: while at war, army money > 50, the city not at war, a free unit slot, and the byte at army `+0x274` clear — every live pool offer whose `(x, y)` is this city's is hired outright (label, name, type, troops, quality copied into the slot, pool slot emptied); **no price is paid** — money > 50 is a gate, not a charge, where the human's gate is the full price (2026-10-07-strategic-ai-turn.md).

**The target tree and its thresholds** (per army with moves; `moves` = remaining moves):
- Resupply/defence city scorer `FUN_0044e670`: an own city whose supply stock is below the army's strength (`troops/100`), or (only while at war) a foreign non-war city with stock above strength + 80 and `money > strength/5`; own cities score −20 if a capital, foreign +20; if nothing qualifies or the best foreign city is beyond 15, fall back to the nearest own city (2026-10-07-strategic-ai-turn.md).
- Enemy-city scorer `FUN_0044ece4` (cities of nations at war, reachable): `score = strength×110 / cityDefense − distance`; `score −= score/2` if the city is in another region; `score ×2` if `cityDefense < strength and distance < 7`; `score ×2` if the city is a capital and `cityDefense×⅔ < strength`; returns `(city, score + distance, distance)` (2026-10-07-strategic-ai-turn.md).
- Enemy-army scorer `FUN_0044ee60` (on land, at war, reachable): the same `strength×110/theirStrength − distance`, halved across regions, capped at 1000, **+1000** when the enemy is weaker and within 7 (2026-10-07-strategic-ai-turn.md).
- Decision: attack the army target unless `armyScore < 100`, or (`supplies < 1 and morale < 60 and armyDist > 8`), or (`cityScore > 100 and cityDist < moves and armyDist > 2×moves`); in the fallback, attack the city unless `cityScore < 100` or (`supplies < 1 and cityDist > 19`); otherwise, if `troops/500 < supplies` and a city target exists, run the mercenary run then defend the resupply city (`armyScore < 71 and cityScore > 85`) or still chase the army target (`armyScore ≥ 71`); else move to the resupply/defence city (2026-10-07-strategic-ai-turn.md).
- The mercenary run `FUN_0044e84c`: walks the 50 live pool offers (records 201–250 of the 251-entry table at `0x0049D0A4`), keeps those within 20 whose nearest city's owner is not at war, and moves to the nearest one — arriving to hire it through the resupply pass [confirmed: decompile] (2026-10-07-strategic-ai-turn.md).

**Movement execution**:
- `FUN_0044dba8(army, xy)` stores no waypoint; it **moves now**: computes the next path step (`FUN_0044db38`), executes it (`FUN_0044d734`, resolving contact with an enemy army or city as battle or siege only at `rel == 3`), spends a move, and recurses while moves remain and the target is farther than 1 (2026-10-07-strategic-ai-turn.md).
- An army aboard a fleet (covered `+0x08 == -1`) instead drives the fleet: `FUN_0044cd08` moves the fleet toward the target and the order costs the army 2 moves [confirmed: decompile] (2026-10-07-strategic-ai-turn.md).

**The idle fallback**:
- `FUN_0044aab4` returns `recomputedFullMoves != army[+6]`; the phase reads it as "did this army actually move"; an army whose whole tree produced no movement gets `FUN_0044ebe8`: if some own army is already within 10 of the capital, go to the nearest city of any owner, otherwise go to the capital [confirmed: decompile] (2026-10-07-strategic-ai-turn.md).

### The fleet phase

- Scope: every own launched fleet (construction countdown `+0x0A == -1`) with no pending destination (the packed `xy` at `+0x4`, read as "no destination" when negative [derived]) (2026-10-07-strategic-ai-turn.md).
- **Resupply and repair** (`FUN_0044e5dc` per city within 4, then `FUN_0044f7e4`): own port — take `min(ships×8 − supplies, city stock)` tons free; purse topped to 100 from the treasury when below 100 and the treasury exceeds 100; condition repaired — below 95 restored to 100 for `(100 − condition) × ships / 5` talents (this can drive the treasury negative), or a flat 100 talents when the treasury is above 100; foreign non-war port — buy tons at `amount/5`, paid to the port owner's treasury (2026-10-07-strategic-ai-turn.md).
- **Port pick** `FUN_0044e9a8`: own coastal city with stock > 20 (score = distance, −1 to dock when already adjacent and supplied), or a foreign non-war city with stock > 120 and money > 10 at distance + 50; fallback the nearest own coastal city; all candidates must be reachable by sea (`FUN_0044e920`: water in the 3×3 around the city and a sea path exists) (2026-10-07-strategic-ai-turn.md).
- **Hunt** `FUN_0044f4f8`: the best enemy fleet at sea, not docked at its own city (`FUN_004494e4`, the same predicate behind refusal R07), scored `myStrength×100/theirStrength − distance`, doubled when the enemy is weaker and within 18; score ≥ 100 → chase it, otherwise sail to the port from the port pick (2026-10-07-strategic-ai-turn.md).
- **Step-mover contacts** (`FUN_0044e1fc`, the fleet's `FUN_0044dba8`): walks the sea path spending moves; on the final step, a land cell disembarks the carried army (a computer nation's free cell is picked automatically, `FUN_0044b840`), a **city** cell resupplies through `FUN_0044f7e4` when not at war, and an enemy **fleet** at war resolves through `FUN_0044b5d0`: two `FUN_0044aa54` strength draws, the loser's fleet deleted, ± half the loser's ships of unity, and the "*X sinks fleet of Y.*" news line (2026-10-07-strategic-ai-turn.md).

### The scorers' arithmetic

- `FUN_0044a930(army)` — assault strength: `Σ troops ×3 for type 2 (Bowmen), else ×1`, divided by 80, times morale; the Bowmen triple weight is read literally, no design intent argued (2026-10-07-strategic-ai-turn.md).
- `FUN_0044a98c(city)` — city defense: `loyalty(+0x16)×150 + fortification(+0x1A mod 100)×250 + population(+0x1C)×200`, ×5/3 for a capital with loyalty > 59, ×⅘ when the owner is not the original owner, plus half the troops queued in recruitment slots at that city (2026-10-07-strategic-ai-turn.md).
- `FUN_0044aa54(fleet)` — fleet strength: `ships × condition / 10`, plus the carried army's assault strength / 50, **plus `Random(4) × value/10`** — every evaluation, including both sides of a naval battle, carries a fresh 0–30% jitter (2026-10-07-strategic-ai-turn.md).
- `FUN_0044b8d0(city)` — the capital test: true if the city is some nation's capital (a scan of all 16 `+0x444` fields); this is what the "×2 on a weak capital" and "prefer defending capitals" modifiers key on (2026-10-07-strategic-ai-turn.md).
- `FUN_0044cab4(army, xy)` — reachability: true if the nation owns any fleet, or both endpoints are in the same region box (`FUN_0044eb18`) (2026-10-07-strategic-ai-turn.md).

### The Random(n) inventory

- `Random(10)` — war declaration, 1/10 per turn, at most one (2026-10-07-strategic-ai-turn.md).
- `Random(20)` — alliance formation, 1/20 per turn (2026-10-07-strategic-ai-turn.md).
- `Random(16)`, `Random(3)` — the human-side offer roll (`FUN_00452034`); not AI-turn proper (2026-10-07-strategic-ai-turn.md).
- `Random(100)` — new order's unit type, buckets 35/25/15/15/10 (2026-10-07-strategic-ai-turn.md).
- `Random(std×4/5)` — new order's troop count, uniform addend over ⅘ of standard size (2026-10-07-strategic-ai-turn.md).
- `Random(4) × v/10` — every fleet-strength evaluation, 0–30% jitter, both sides of a battle (2026-10-07-strategic-ai-turn.md).
- Interactions: the post-battle treaty reseeds the global RNG (`RandSeed := winner + loser`), so AI draws after a treaty repeat deterministically; and the human seat's offer roll shares the same global stream, so AI draws shift a human offer's outcome and vice versa [derived] (2026-10-07-strategic-ai-turn.md).

### Human-versus-AI asymmetries

| # | Asymmetry | Source |
| --- | --- | --- |
| 1 | Mobilisation-receiving radius 5 vs 1; new army 1 move vs 0 | decompiled-mobilization-and-mercenary-restock.md §3 |
| 2 | AI mobilises only fully ready slots (state 24) vs player 16 | decompiled-mobilization-and-mercenary-restock.md §4 |
| 3 | End-turn warning never blocks an AI seat | army-moves-field-signed-and-the-ffff-underflow.md |
| 4 | The AI changes its own tax rate (week 11); the human only via the slider [confirmed: decompile] | 2026-10-07-strategic-ai-turn.md §2.3 |
| 5 | The AI hires mercenaries with no charge (gate: army money > 50); the human's gate is the full price [confirmed: decompile] | 2026-10-07-strategic-ai-turn.md §3.2 |
| 6 | The AI recruits into treasury deficit down to `−wealth/500`; the human's dialog requires the money [confirmed: decompile] | 2026-10-07-strategic-ai-turn.md §2.2 |

- Also: the human's `TArmyRecruits_RecruitUnit` charges `(troops/200) × initialPrice`; the deficit gate is checked only in `FUN_004504f4` [confirmed: decompile]; a disembarking computer fleet picks its landing cell automatically (`FUN_0044b840`), where a human clicks (2026-10-07-strategic-ai-turn.md).

Open:

- Nothing here was observed in play — every claim is decompile-only (`[confirmed: decompile]` means the dump, not a listing or a save); a fixed-seed EXPLORE run could corroborate the week-11 tax moves, a free mercenary hire, an intercept dispatch, a hunt-vs-port fleet decision (2026-10-07-strategic-ai-turn.md).
- `FUN_0044a004` (the fleet order itself) and the `+0x274` byte gate on mercenary hires were not opened; the fleet-size parameter's meaning is `[derived]` (2026-10-07-strategic-ai-turn.md).
- The `+0x4` packed fleet destination and the marker-range arithmetic in `FUN_0044e1fc`'s final step are read at decompile granularity only (2026-10-07-strategic-ai-turn.md).
- Whether `FUN_0044d734`'s contact resolution differs when the mover is AI was not re-checked; the attack gating is inherited from the diplomacy and capture reports (2026-10-07-strategic-ai-turn.md).
- The Bowmen ×3 assault weight is literal; design choice vs decompile artefact of the type encoding is not argued (2026-10-07-strategic-ai-turn.md).
- The readers of the phase-mode flag `DAT_004a0340` were not traced [confirmed: decompile; the readers were not traced] (2026-10-07-strategic-ai-turn.md).

## Victory, defeat, and the player interface

### Victory and defeat conditions

- The turn-start check `FUN_00452034` (run at every human turn start and at New Game) fires the fall routine `FUN_0044c8f0` when **any** of five conditions holds: year equals 250, cities above 333 (i.e. 334 of 334), unity below 400, treasury below -(wealth div 500), or treasury below -20,000 `[derived]` (2026-10-05-end-of-game-screens.md)
- **Victory** (cities `+0x446` not below 334): `You have conquerred the Mediterranean, a unique achievement.` — confirmed two ways, by the count word alone and by owning all 334 cities `[confirmed]` (2026-10-05-end-of-game-screens.md)
- **250 BC** is a real trigger, not just screen wording: `You have reached the end of your allotted 20 years.` `[confirmed]` (2026-10-05-end-of-game-screens.md)
- **Conquered**: `Your nation has been conquerred by <nation>.`, the conqueror read from nation `+0x44E` `[confirmed]` (2026-10-05-end-of-game-screens.md)
- **Unity below 400**: `Your unpopularity has forced the army to overthrow you.`; **debt** (either threshold): `Your army have deposed you because they have not been paid.` `[confirmed]` (2026-10-05-end-of-game-screens.md)
- When two reasons hold, the window shows the first of the order **victory → 250 BC → conquered → unity → debt** `[derived]`; the pairs victory>250 BC, 250 BC>unity and unity>debt were played `[confirmed]`; conquered against the others is derived only (2026-10-05-end-of-game-screens.md)
- The autosave of the turn is written **before** the test, so it holds the state the window shows `[confirmed]` (2026-10-05-end-of-game-screens.md)

### The End of Game screen

- One window `THumanFalls` ("End of Game", 450 x 347, one OK) serves all five reasons; first line always `The game is over for <leader> the leader of <nation>.` `[confirmed]` (2026-10-05-end-of-game-screens.md)
- Years in power: `N years` with N = 270 - year, printed only below 269 (test `< 0x10d`), otherwise ` short time ` (two spaces); `1 years` never appears `[confirmed]`/`[derived]` (2026-10-05-end-of-game-screens.md)
- Start-versus-end table (population, cities, treasury): the left column is fixed `<nation> in 270 BC.`; population is the **wealth field** (Σ pop x 3000), not a head count; the start triple (+0x434 wealth, +0x43C treasury, +0x448 city count) is frozen from New Game `[confirmed]` (2026-10-05-end-of-game-screens.md)
- After a fall: the seat's human flag is cleared, a new leader drawn, unity = max(unity, min(550, unity + 150)), treasury = 0 if negative else + 1000, relations of -5 to -1 reset `[derived]` (2026-10-05-end-of-game-screens.md)
- If no human is left, the maps close, the main window is left blank with caption `Imperial Conquest 2`, only File > New / Open / Close stay enabled, and **the program keeps running**; with another human the game goes on with that human `[confirmed]` (2026-10-05-end-of-game-screens.md)
- **Abdicate** shows only the Confirm box `Are you sure you want to abdicate ?` (Yes/No/Cancel); Yes hands the seat over at once, with **no** End of Game window and no unity/treasury change `[confirmed]` (2026-10-05-end-of-game-screens.md)
- For an AI nation the same routine runs from the quarterly update with a **1-in-9** chance when the debt test fails, writing the news line `<nation> depose their leader <leader>.` `[derived]` (2026-10-05-end-of-game-screens.md)

### Leader falls and the leaders form

- The leader pool sits in the DAT: **12 names per nation, 16 nations, 26 bytes each** (192 names; only two names appear in two nations' lists) `[derived]` (2026-10-06-leaders-form.md)
- Every New Game draws `Random(12)` for each nation **before** the form opens, and clears every human flag; the turn order is drawn in the same setup, and the first human in that order plays first `[derived, confirmed]` (2026-10-06-leaders-form.md)
- A human fall makes **two draws**: `FUN_00449078` writes a first `Random(12)` draw into the leader field, then `FUN_0044c8f0` repeats a second draw until it differs from the first (so the final name can equal the one the window showed) `[derived]` (2026-10-05-end-of-game-screens.md)
- The form `TPickLeaders` ("Human and computer leaders") has 16 rows (Rome … Thracia), each a human tick box and a name box limited to **25 characters**; OK never refuses: empty, spaces-only, duplicate and odd-character names are all accepted `[confirmed]` (2026-10-06-leaders-form.md)
- The tick handler is bound to **mouse-down**, not click: the space bar ticks the box but leaves the name box greyed, and OK then keeps the drawn name `[confirmed]` (2026-10-06-leaders-form.md)
- OK on a newly ticked row copies the name box text into the nation record (+0x0B), sets the human flag, floors a negative treasury to 0 and the unity word (+0x440) to at least **450**; an unticked human row (mid-game only) is cleared, redraws `Random(12)`, and floors unity to at least **500** `[derived]` (2026-10-06-leaders-form.md)
- Leader names are drawn per game, not canonical (the same nations carry different names across play-throughs); the pool is nation-specific, and the names are editable text fields so a player can override the draw `[confirmed]` (ptolemy-run-ui-inventory-and-leader-draw.md)

### The news log

- Storage: **40 slots of 61 bytes**, plain NUL-terminated strings of at most 60 single-byte characters, a shift register (slot 0 always oldest; when full, slots 1-39 copy down and the new message enters slot 39); the index (DAT_004A031E) is -1 when empty and 39 when full `[confirmed]` (news-log-format-and-messages.md)
- The writer `FUN_00449240` never truncates; no message the game can build exceeds 59 bytes (the dash banner) `[confirmed]` (news-log-format-and-messages.md)
- 24 call sites use **21 templates**, among them: `A declares war on B.`, `A forms an alliance with B.`, `C   (A)  falls to B.` (3 spaces before the bracket, 2 after), `N fails to capture C   (A).`, `A destroys army of B.`, `A sinks fleet of B.`, `C defects from A to B.`, `A conquers B.` between two 59-dash lines, `N depose their leader L.`, `N have moved their capital to C.`, `N finishes a new fleet at C.`, fleet lost-at-sea and storm lines, and the peace block (`B sues A for peace and;` plus three indented lines) `[derived]` (news-log-format-and-messages.md)
- **Shouting rule**: a war declaration in which either nation's human flag (+0x490) is set goes through `StrUpper` in full (ASCII a-z only): `ROME DECLARES WAR ON GAUL.`; alliance lines are never uppercased; the cascade declarations follow the same rule `[derived]` (news-log-format-and-messages.md)
- Only the reparations amount is comma-grouped, by a hand-written formatter with the literal byte 0x2C (never the locale); week and year print through plain `Str` `[derived, confirmed]` (news-log-format-and-messages.md)
- Each completed round tick ends with a single space `" "` then `Week  W      Season      YYYBC` (2 spaces after "Week", 6 around the season, none before "BC"); both lines consume slots `[confirmed]` (news-log-format-and-messages.md)
- A new game seeds the log with the DAT's 27 scripted history lines at index 26; they are scenario data and must be loaded verbatim, not regenerated `[confirmed]` (news-log-format-and-messages.md)
- A pending trade or alliance offer is **never** news: it is a modal `MessageDlg` (`X wants to trade with Y.` / `X wants to form an alliance with Y.`) at the human turn start, cleared each turn start and re-shown on load `[confirmed]` (news-log-format-and-messages.md)
- The SAV stores the newest index then that many slots plus one, each a whole 61 bytes including stale residue after the NUL `[confirmed]` (news-log-format-and-messages.md)

### The "End turn ?" warning box

- The gate `FUN_0045AF00` clears the ready flag when a trigger holds; the flag is forced back to 1 for a computer nation, so **AI seats never see the box** `[confirmed: code]` (2026-10-03-end-turn-warning-box.md)
- Triggers, per army/fleet (never per unit) that has **not acted** this week: army supplyPct < 20 with an army source available; army money strictly below its mercenary pay; a launched fleet with no own city in its 3 x 3; fleet supplies < ships div 5 with a fleet source available; an army aboard a fleet is tested only through its fleet, using the fleet's port test `[confirmed: code]` (2026-10-03-end-turn-warning-box.md)
- `supplyPct = int16((supplies x 10000) div total troops)`, so the test is exactly **500 x supplies < T** (under 20 % of capacity troops div 100) `[confirmed: code]` (2026-10-03-end-turn-warning-box.md)
- `mercPay` = Σ int16(((troops div 200) x price[type] x quality) div 5) over mercenary slots only — one full round of mercenary pay; an army without mercenaries fires only on a negative purse `[confirmed: code]` (2026-10-03-end-turn-warning-box.md)
- `armySource` holds whenever the nation owns any city; otherwise only at war and at a foreign non-hostile city with stock > T div 1000 + 80 and army money > (T div 1000) div 5 — so in practice the supply line fires for any nation that owns a city `[confirmed: code]` (2026-10-03-end-turn-warning-box.md)
- `fleetSource` holds when the nation owns a port city, or a non-hostile foreign port has stock > 120 and the fleet has money > 10 `[confirmed: code]` (2026-10-03-end-turn-warning-box.md)
- The repair line `A fleet of yours needs repairing.` (condition < 65) is added only when the box is already open and is **never a trigger**; at most one box per click, capped at **5 lines**, not de-duplicated `[confirmed: code]` (2026-10-03-end-turn-warning-box.md)
- End turn sets the flag to 1 and proceeds; Make more moves sets 0 and the human keeps playing; closing the box any other way behaves like Make more moves `[confirmed: code / derived]` (2026-10-03-end-turn-warning-box.md)

### Unit-map mouse orders, selection, and taxation

- A left click on an own army (which needs moves > 0 to be selectable) selects it; it stays selected while it has moves and is deselected when its moves reach 0 `[confirmed]` (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- With an army selected, a click on a reachable tile moves it at once; one click walks the whole route `[confirmed]` (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- Attack on an adjacent enemy city: **at war, no prompt**, the siege resolves on the click; at peace, a Yes/No/Cancel box `Are you sure you want to attack this city?` — No changes nothing and leaves the army selected, Yes writes war (relation 0 → 3, news `ROME DECLARES WAR ON GREECE.`) and the siege follows `[confirmed]` (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- A right click on an own army replaces the panel with its unit list; neither click opens a window `[confirmed]` (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- Shift+X (Cancel selection) drops the selection (index 0 → -1) but does not clear the Information panel `[confirmed]` (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- Split army places the new army on an adjacent tile, one step diagonally (+1,+1) in the observed split `[confirmed]` (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- The Taxation slider ("Change tax level") runs **0 to 40**, 1 per arrow key and 5 per page key (clamped at both ends); OK writes the rate to nation `+0x44A` `[confirmed]` (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- File > Save sets the selected-army variable (0x4A0328) to -1 `[confirmed]` (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- A unit-map click resolves to tile x = X div 32 + nation[+0x488], y = (Y - 30) div 32 + nation[+0x486]; the marker word dispatches 20-99 city, 200-247 army, 300-347 fleet `[derived]` (2026-09-29-nation-view-origin-and-unit-map-clicks.md)
- A left click on the area map centres the clicked tile at column 6, row 7 of the unit map `[confirmed]` (2026-09-29-nation-view-origin-and-unit-map-clicks.md)

### Information-window fields and bands

- **Nation panel**: Nation, Leader, Capital, Cities, Population, Unity (word), Tax rate always; Mobilized and Treasury only when the shown nation is the current nation; Population is the stored wealth field (3000 x the sum of city populations in thousands) `[confirmed]` (2026-10-05-information-window-fields-and-bands.md)
- Relations rows print a word only when the value is > 0: 1 trade, 2 ally, 3 war; **peace (0, and any value <= 0) prints blank** — the word exists in the DAT but is never printed; a nation whose unity is 0 gets the red row `( X conquerred by Y )` `[confirmed]` (2026-10-05-information-window-fields-and-bands.md)
- **City panel**: population in thousands plus percent of maximum; loyalty as a word; fortification prints the raw word below 101, else raw mod 100 plus ` (under construction)`; the bracket after it is the sum of troops over **all** of the controller's recruit slots at that city whatever their state (shown when > 0, on foreign cities too); Tribute and Supply lines only for an own city `[confirmed]` (2026-10-05-information-window-fields-and-bands.md)
- Foreign-city tribute words: <= 10 poor, 11-30 moderate, 31-100 rich, 101-10000 very rich; above 10000 no word `[confirmed]` (2026-10-05-information-window-fields-and-bands.md)
- **Army panel**: an own army shows Moves, Supply (tons and percent), Morale, Money, Terrain, the five type lines, Total troops, No. of units, Regulars cost and Mercenary pay; a foreign army shows only composition, terrain and total (a fog-of-war rule) `[confirmed]` (2026-10-05-information-window-fields-and-bands.md; ptolemy-run-ui-inventory-and-leader-draw.md)
- Regulars cost = Σ s over regular slots with s = i16(trunc(troops / 200) x price[type]); Mercenary pay = Σ trunc((s x quality) / 5) over mercenary slots; the per-slot product is narrowed to signed 16 bits `[confirmed]` (2026-10-05-information-window-fields-and-bands.md)
- **Fleet panel**: Capacity = ships x 500; Sea is `calm` when the map-code field (+0x18) is 0, otherwise `rough`; a foreign fleet shows Fleet of, Ships, Capacity and Sea only `[confirmed]` (2026-10-05-information-window-fields-and-bands.md)
- **Bands**: unity word = table[trunc(unity / 100)] — very low below 500, low 500-599, normal 600-699, high 700-799, very high 800-899, excellent 900-999, blank at 1000+; loyalty uses the same table with div 10 (very low below 50 … excellent 90-99); morale indexes the same table from entry 4 via ((m - 51), or (m - 48) when negative) sar 2 (very low 40-54 … excellent 71-74, blank 75+); quality is a plain index 0-9 (0-3 not ready, 4 very poor, 5 poor, 6 average, 7 good, 8 very good, 9 elite) — 36 of 41 edges confirmed on both sides in play `[confirmed]` (2026-10-05-information-window-fields-and-bands.md)

### Refusal texts and their conditions

- The game holds **74 message-box calls: 57 refusals, 13 prompts, 3 notices** (plus the excluded battle Surrender); every refusal is an OK-only information box except embark's `The army is too large for this fleet ?`, which is a Confirmation `[derived]` (2026-10-05-refusal-texts-and-conditions.md)
- When two refusals hold, **the first-tested is shown and only one box appears** (played: 20-units before 100,000-troops; 100-ships before carrying-an-army) `[confirmed]` (2026-10-05-refusal-texts-and-conditions.md)
- Most refusals drop the order and change nothing; the transfer dialogs' per-unit tests, the three disband paths and Mobilize instead **clamp** — units that pass are still moved or removed and the box follows `[confirmed/derived]` (2026-10-05-refusal-texts-and-conditions.md)
- Order limits (conditions `[derived]`, most played `[confirmed]`): 20 units per army (`These 2 armies combined contain more than 20 units.`, tested before troops), 100,000 troops per army (100,000 itself allowed), troops at most ships x 500 on embark/transfer, 100 ships per fleet on join (sum < 101, tested before the army test), neither fleet carrying an army to join or split fleets, split needs 20+ ships, army split needs 2+ units, fortify refused under siege / at 100 / with a pending order (word >= 101), recruit refused at 40 queued units / 100% mobilisation / a city under 75% fortification that is not the capital, mercenary hire refused at under 15% supplies / enemy city / purse below the price (2026-10-05-refusal-texts-and-conditions.md)
- Diplomacy refusals: `You can only trade with 3 nations.`; `<nation> does not want to trade with you.` on a negative (cooldown) relation; `You cannot trade with <nation>.` when the target has three partners or the relation is 2-3; `<nation> does not want to make peace at this time.` for an AI at war; `<nation> does not want to ally with your nation.` when you (or an ally) are at war or the relation is negative `[confirmed/derived]` (2026-10-05-refusal-texts-and-conditions.md)
- Build fleet: `Only nations with coastal cities can build fleets.`, then `You do not have a free coastal city at this time.`, then `You cannot build a fleet at this time.` (fleet table full at 99) `[derived]` (2026-10-05-refusal-texts-and-conditions.md)
- Orders that fail with **no box at all**: Join armies/fleets with no partner one tile away, Split army with no free adjacent tile or 198 armies, Recruit mercenaries with no offer one tile away, embarking without moves or onto a fleet already carrying an army `[derived]` (2026-10-05-refusal-texts-and-conditions.md)

### Nation marker colours

- Every city, army and fleet marker is a square filled with the owner's **background** colour carrying the glyph in the owner's **foreground** colour plus a black or white outline; all colours are 16 standard VGA palette entries `[observation]` (2026-09-29-nation-marker-colours.md)
- Pairs (background / foreground): Rome purple/blue, Carthage red/white, Seleucid olive/maroon, Ptolemaic navy/magenta, Macedonia white/blue, Numidia lime/teal, Gaul maroon/cyan, Greece cyan/magenta, Celtiberia yellow/red, Illyria navy/olive, Dacia green/yellow, Bithynia teal/blue, Galatia blue/cyan, Armenia magenta/red, Media red/purple, Thracia grey/black `[observation]` (2026-09-29-nation-marker-colours.md)
- Two backgrounds are shared and told apart by the foreground only: red (Carthage white, Media purple) and navy (Ptolemaic magenta, Illyria olive) — the original's own design, not a defect `[observation]` (2026-09-29-nation-marker-colours.md)

### Sound events

- `TPremierForm_MakeSound` plays `WAVS\Sound1.WAV` … `Sound10.WAV` through `PlaySoundA(path, NULL, 0)`; flags 0 mean synchronous — each sound plays to its end and **blocks the game** (sound 10 freezes it for about 1.4 s; an army walk plays sound 1 once per tile) `[derived: code]` (2026-10-06-sound-events.md)
- There is **no sound option** anywhere: no guard, no menu item, no on/off string in the EXE `[derived: code + resource]` (2026-10-06-sound-events.md)
- Event mapping (all `[derived: code]`): **1** click — an army step on the unit map and battle-unit placement/moves; **2** blip — a fleet step on the unit map; **3** arrow whoosh — archers shoot; **4** javelin zip — light infantry or light cavalry throw; **5** metallic clang — a melee target set and each melee exchange; **6** dull thuds — a siege fails; **7** crash — a city is taken; **8** falling bloop — a fleet sunk in battle, lost in a storm, or scuttled; **9** distant ring — a field battle between two computer nations; **10** low horn — a nation is conquered (2026-10-06-sound-events.md)
- Sounds 1 and 2 play only while the **current seat is human**; sounds 3-10 play whoever is involved, including during computer turns; a human's own field battle has no result sound (it opens the battle screen) `[derived: code]` (2026-10-06-sound-events.md)

Open:

- End screens: the reason order for conquered against the others is derived only; where the start triple is first written (New Game or each nation's first move) is not separated; a window for an AI conqueror, the defection-elimination path, a fall with three or more humans, and 269 BC / years 2-19 were not played; every state that reached a window was staged (2026-10-05-end-of-game-screens.md)
- Leaders form: the mid-game branches (New player / New nation: OK's untick redraw, an already-human row) and `FUN_00449078` are derived only; the original's clock seeding of the draw was not played (2026-10-06-leaders-form.md)
- News log: an uppercase war declaration has never been saved; an alliance-offer dialog has never been observed; `finishes a new fleet at`, `sinks fleet of` and `have moved their capital to` are code-only (news-log-format-and-messages.md)
- End-turn box: the five-line cap and the "not acted" filter were not exercised live; the fleet-allowance formula behind the not-acted test is unchecked against saves (2026-10-03-end-turn-warning-box.md)
- Unit map: whether Split army's placement tile follows a rule (the one observation is (+1,+1)); the slider's opening position; embark/unload by click were not run here (2026-10-02-unit-map-mouse-orders-and-tax-range.md)
- Information window: band edges outside the values the game produces (loyalty below 0 or above 109, unity 1000+, morale below 48 or above 75, relations above 5) are derived only; whether the panel is redrawn after an order was not studied (2026-10-05-information-window-fields-and-bands.md)
- Refusals: nine rows (R07, R12, R19, R27, R33, R48, R49, R56, R57) were never reached in play; the plain-language condition and effect columns were not machine-audited (2026-10-05-refusal-texts-and-conditions.md)
- Marker colours: where the (background, foreground) pairs are stored (DAT or EXE) is not located (2026-09-29-nation-marker-colours.md)
- Sounds: nothing was heard in play — every mapping is code-only; whether the WAVS folder is resolved against the current directory or the EXE's, and the help's exact sentence on sounds, are unsettled (2026-10-06-sound-events.md)
