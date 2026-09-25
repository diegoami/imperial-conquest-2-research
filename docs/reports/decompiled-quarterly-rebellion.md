# The quarterly rebellion, decompiled: allegiance first, then a nearby enemy, then the best-placed neighbour

**The question** (dev-repo [#389](https://github.com/diegoami/imperial_conquest_2/issues/389), re-planned as T89 [#397](https://github.com/diegoami/imperial_conquest_2/issues/397)): what exactly does `FUN_0044C204` do? The quarterly city loop in `FUN_00451B40` calls it for a non-capital city whose loyalty is below 30. The dev engine publishes `RebellionRiskDetected` and nothing consumes it, so no city ever rebels.

Line numbers are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`. The machine listing of `FUN_0044C204`, `FUN_0044C360`, `FUN_0044BED8`, `FUN_00449018` and `FUN_00451B40` is in `%LOCALAPPDATA%\ReTools\scratch\rebellion_listing.txt` (see Reproduction). Every condition below was read from the instructions, not only from Ghidra's pseudocode.

Record bases are as in [decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md):

- **City** `0x00479590`, stride `0x22`: `+0x0E/+0x10` x, y; `+0x12` owner; `+0x14` allegiance; `+0x16` loyalty; `+0x1A` fortification; `+0x1C` population; `+0x1E` maximum population; `+0x20` tribute.
- **Nation** `0x00474670`, stride `0x494`: `+0x26` relation row (16 words, `3` = war); `+0x46` neighbour mask; `+0x2E4` 40 recruitment slots; `+0x430` wealth; `+0x438` treasury; `+0x440` unity; `+0x442` mobilization; `+0x444` capital; `+0x446` city count; `+0x44A` tax rate; `+0x44C` tax base; `+0x44E` conquered-by; `+0x490` human flag.
- **Army** `0x0047C1EC`, stride `0x290`, count `DAT_004A0324`: `+0/+2` x, y; `+4` owner (`−1` = tombstone).

## Answer

The outline in [dat-neighbour-mask.md](dat-neighbour-mask.md) §5 and [decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md) §4 is right in substance. It did not follow the code's order, and it left out several conditions. In code order `[confirmed: listing 0x0044C204–0x0044C35D]`:

```text
FUN_0044C204(city):                                   // :50432
    owner = city.owner (+0x12);  alleg = city.allegiance (+0x14)
    if owner != alleg:                                // 0x0044C22E
        if nation[alleg].unity (+0x440) <= 0:         // 0x0044C23C  CMP word,0 ; JLE
            FUN_0044C360(alleg)                       // (a) rebirth attempt; nothing else, whatever it decides
        else:
            FUN_0044BED8(city, alleg)                 // (b) the city returns to its allegiance nation
        return
    // owner == alleg from here on
    pick = −1
    for a in 0 .. armyCount−1:                        // (c) ascending, no break
        if army[a].owner >= 0                         // 0x0044C27B  CMP word,−1 ; JLE skip
           and cheb(army[a].xy, city.xy) < 10         // 0x0044C28C  CMP AX,0xA ; JGE skip
           and nation[owner].rel[army[a].owner] == 3: // 0x0044C2A7  war with the city's owner
            pick = army[a].owner                      // a later match overwrites an earlier one
    if pick == −1:                                    // (d)
        best = −1000                                  // 0x0044C2CA  0xFC18
        for n in 0 .. 15:                             // ascending
            if bit owner of nation[n].mask (+0x46)    // 0x0044C2E8  BT [EBP+0x46],EAX
               and nation[n].unity > 0:               // 0x0044C2EE  CMP word,0 ; JLE skip
                s = nation[n].cities (+0x446) − 2 × cheb(city.xy, city[nation[n].capital (+0x444)].xy)
                if s > best:  best = s; pick = n      // 0x0044C323  strict: ties keep the lower n
    if pick >= 0:  FUN_0044BED8(city, pick)           // 0x0044C341
```

- **(a) and (b) come first, and they apply only when the owner is not the allegiance nation.** "Alive" is unity `> 0`. The test is `unity ≤ 0`, the same "dead" the turn loop and the diplomacy use `[confirmed]`.
- **(a) is final.** When rebirth declines (7 or fewer disloyal cities, §4), the city stays where it is. There is no fallback to (c) or (d) `[confirmed]`.
- **(b) has no other condition.** It needs no war, no distance and no AI check. A city can return to a human nation `[confirmed]`.
- **(c) and (d) run only when the owner is the allegiance nation.** (c) is not "the city is already the allegiance nation's" in any wider sense: it is exactly `owner == allegiance` `[confirmed]`.
- **(d) has no relation test.** An ally, a trade partner or a human neighbour can receive the city `[confirmed]`.
- **When (c) and (d) both find nothing, nothing happens.** No news, no loyalty change, no write at all `[confirmed]`. For (d) to find nothing, every neighbour of the owner must be dead. A candidate with a score of −1000 or below would also be skipped, but that cannot happen on a 320 × 140 map, where the score is at least `−2 × 319` `[derived]`.
- **The routine writes nothing itself.** Every change is made by `FUN_0044BED8` or `FUN_0044C360` `[confirmed]`.

## 1. The details

### The distance is Chebyshev, in map tiles `[confirmed: listing 0x00449018–0x0044904D]`

`FUN_00449018(p, q)` takes two packed `(x, y)` word pairs. It returns `max(|p.x − q.x|, |p.y − q.y|)`, through the word `max` `FUN_00448FD8`. The unit is one map tile. The city's position is the dword at city `+0x0E`, the army's is the dword at army `+0`, and (d) uses the capital city's `+0x0E`. **"Within 10 tiles" is Chebyshev ≤ 9**, because the test is `< 10`.

This is the same metric and bound as the capture cascade `FUN_0044BA1C`, which the engine already implements as `CascadeDistanceMax` = 10 with `>=` rejecting.

### (c): the last matching army in table order wins `[confirmed]`

- The scan runs over army records `0 … DAT_004A0324 − 1` in ascending order and never breaks. Each match overwrites `pick`, so **the highest-indexed matching army decides**. It is not the nearest army, and it is not the strongest.
- **The scan order matters** whenever two nations at war with the owner both have an army within 9 tiles. Army indices are creation order, except that compaction (`FUN_0044ADB0`, at each AI seat's turn) moves the last record into each hole ([decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md) §2). A reimplementation that wants the same recipient has to keep the same army order `[derived]`.
- **What is required:**
  - The army record must be live (owner `≥ 0`). A tombstone left inside the current seat's turn is skipped.
  - The **owner's** relation row must hold `3` (war) at the army's nation. Relations are written symmetrically, so this is war between the two nations.
- **What is not required:**
  - Nothing about the army's own state: troops, morale, moves, or whether it is aboard a fleet. The army's `+0/+2` position is used as it stands `[confirmed: no other field is read]`.
  - The army's nation need not be the allegiance nation or a neighbour, and it may be human.
  - Nothing checks the war nation's unity. A dead nation has no armies anyway, because elimination deletes them `[derived]`.
- The city's owner can never be its own `pick`: nothing writes `3` into a nation's own relation entry `[derived: every setter call on the diagonal writes 0 or a cooldown]`.

### (d): the lowest nation index wins a tie `[confirmed]`

- `n` runs from 0 to 15. The comparison is `JLE` over a 16-bit score, so an equal score keeps the earlier, lower-indexed nation. The start value is −1000.
- The owner is never a candidate. The DAT mask has no self-bits, and the conquest merge never adds one (it skips `k = winner`) ([dat-neighbour-mask.md](dat-neighbour-mask.md) §2, §4) `[derived]`.
- `cities(n)` and `unity(n)` are read **live**. An earlier rebellion in the same quarterly loop has already moved a city and changed the counts. So a later city's score can differ from what a snapshot taken at the top of the loop would give `[derived]`.
- The capital is `nation[n] +0x444`, read with `MOVSX`. A live nation always has one. The single exception is a human seat eliminated by defection, which keeps unity 150 and a stale capital ([decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md) §3). That is an edge case of an edge case `[derived]`.

### Random draws: none in `FUN_0044C204` itself `[confirmed: no CALL 0x0040284C in 0x0044C204–0x0044C35D]`

The city loop's draws for one city are, in order `[confirmed: listing 0x00451DB6–0x00451E1D]`:

1. `Random(4)`, only if the owner's tax rate `≤ 10` and loyalty `< 80`.
2. `Random(3)`.
3. `Random(taxRate)`, only if the `Random(3)` returned 0.
4. The rebellion, only if loyalty `< 30` and the city is not a capital.

The rebellion adds draws only as follows:

- **(b), (c) and (d): none**, as long as the transfer does not eliminate the old owner. `FUN_0044BED8` and its helpers `FUN_0044B8F4`, `FUN_004498B0`, `FUN_0044A610`, `FUN_0044A794` and `FUN_00449240` draw nothing. Elimination needs the old owner's city count to reach 0, and a non-capital city cannot be the last city of a nation that holds its capital. So these branches draw only in the stale-capital state below `[derived]`.
- **(a), when rebirth goes ahead:** exactly one `Random(12)`, for the new leader (`0x0044C410`), before any city moves. After that, one or more `Random(12)` for each **human** owner that the rebirth's defections empty, through `FUN_0044C8F0`'s redraw loop (it redraws until the name differs) `[confirmed]`.
- **(a), when rebirth declines:** none.

`Random` is `FUN_0040284C`: `seed = seed × 0x08088405 + 1; return (seed × range) >> 32`. It **advances the seed even for `range = 0`** (:1585) `[confirmed]`. That matters for draw 3 at tax 0; see §5.

### News: one line per moved city, from `FUN_0044BED8` `[confirmed]`

It is "*C defects from X to Y.*" (:50373–50379), where X is the old owner and Y the receiver. It is the same line the capture cascade writes, so a rebellion shows in the log only by where it appears:

- The quarterly tick runs inside `FUN_004514EC` **before** that round's `" "` and `Week  1 …` header (:54666 then :54678–54690).
- So a rebellion line sits at the end of the week-11 round, just before the new season's header, and with no "*falls to*" line in front of it.

Rebirth writes no news of its own. It writes only the defection lines, one per city.

### A capital never rebels, but a capital can defect in a rebirth `[confirmed]`

The caller tests `FUN_0044B8D0(city)` (:54853), which is true if the city is the `+0x444` of **any** of the 16 nations, dead ones included. So:

- A capital never reaches `FUN_0044C204`.
- A dead nation's stale capital pointer also protects that city from rebelling.

Rebirth's own transfer loop has no capital check, though (§4).

### Nothing is written before the transfer `[confirmed]`

`FUN_0044C204` changes no loyalty, unity or anything else before or after it calls `FUN_0044BED8`. The only loyalty change is `FUN_0044BED8`'s own (§2).

## 2. Effects of the transfer: `FUN_0044BED8`, :50307, in the rebellion case

[decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md) §4 already covers the elimination block, so it is not repeated here. The rest, in order `[confirmed: listing 0x0044BED8–0x0044C0D2]`:

1. `FUN_0044B8F4(city, receiver)` moves the city index from the old owner's city list (`+0x48`, `0xFFFF`-terminated) into the receiver's.
2. `city.owner = receiver`.
3. **The receiver:**
   - unity `= min(990, unity + 3)`;
   - wealth `+= pop × 3000`;
   - city count `+1`;
   - **treasury `+= contribution × 6`**;
   - tax base `+= contribution × 4`.

   Here `contribution` is `FUN_004498B0(city)`, the city's tribute share, as in the quarterly rebuild.
4. **The old owner:**
   - **unity `= max(250, unity − 20)`**;
   - wealth `−= pop × 3000`;
   - city count `−1`;
   - tax base `−= contribution × 4`;
   - treasury unchanged.

   The floor is a `max`. **An old owner below 270 unity is raised to 250**, not lowered. The engine already has this as `DefectionUnityLossFloor` = 250.
5. **Recruitment slots.** The old owner's 40 slots are scanned **from 39 down to 0**. Each slot with troops `> 0` (`+4`) and target city `==` this city (`+6`) is removed by `FUN_0044A610`, which shifts the later slots down and zeroes slot 39's troops. A slot at this city **with 0 troops is kept**, still pointing at a city its nation no longer owns. The receiver's slots are not touched.
6. **Loyalty** (:50363–50370):
   - if `allegiance == receiver`: `L = min(90, 140 − L)`;
   - else: `L = min(65, max(50, 100 − L))`.

   With `L < 30`, as in every rebellion, this is **always 90 in (b)** (the receiver is the allegiance nation) **and always 65 in (c) and (d)** (it is not, because owner = allegiance ≠ receiver). A rebirth moves cities with `L < 40` to their allegiance nation, so they also get exactly 90.
7. `FUN_0044A794` repaints the city marker, and the news line is written.
8. The elimination block runs if the old owner's city count is now 0 (see the cross-reference above).
9. `RefreshForms` runs if the receiver is human.

Population, fortification, tribute, allegiance and the old owner's treasury are never written. Allegiance does not change: a city captured by rebellion keeps rebelling back while its loyalty stays low.

**How the transfer interacts with the quarterly loop** `[derived]`. `FUN_00451B40` zeroes every nation's wealth and tax base before the city loop, then adds each city's share to its owner as it goes (:54832–54836). The rebelling city's own share was added to the old owner earlier in the same iteration. So `FUN_0044BED8`'s move leaves both totals exactly as if the city had belonged to the receiver all along.

The treasury credit (`× 6`), the unity changes and the city counts all land **before** the nation loop that follows. That loop reads the city count (`−7` per city), the tax base and the wealth for this quarter's income.

A rebirth also moves cities with a **higher** index than the current one, and their shares have not been added yet. For each such city the old owner ends the quarter `pop × 3000` short on wealth and `contribution × 4` short on tax base, and the reborn nation counts both twice (once in the move, once when the loop reaches the city). Those cities then grow and draw loyalty under the reborn nation's tax rate (20) and mobilization (50), which can change whether `Random(4)` is drawn.

## 3. Correction: `FUN_0044BED8`'s loyalty is a formula, not a floor `[confirmed: decompile + 8 save transfers]`

[decompiled-defection-and-siege-attrition.md](decompiled-defection-and-siege-attrition.md) says a defection pulls loyalty "toward a floor of 65". The code is the step 6 formula above. Rebellion never sees the difference, because at `L < 30` both formulas give their constant. The capture cascade does see it, because it moves cities with `L < 65`.

Every non-scripted defection in the local saves is a cascade defection, and all 8 match the formula:

| Pair | City | Receiver | Allegiant? | L before → after | Formula |
| --- | --- | --- | --- | --- | --- |
| `IP018 → IP018B` | Aradus | Ptolemaic | no | 56 → **50** | `max(50, 44)` |
| `IP018 → IP018B` | Hemesa | Ptolemaic | no | 62 → **50** | `max(50, 38)` |
| `IP019 → IP019B` | Palmyra | Ptolemaic | no | 57 → **50** | `max(50, 43)` |
| `1_rome_270_autumn_5 → _7` (and `IP004 → IP005`) | Modena | Rome | no | 63 → **50** | `max(50, 37)` |
| `1_rome_270_winter_5 → _7` | Acroinon | Seleucid | no | 59 → **50** | `max(50, 41)` |
| `1_rome_270_winter_5 → _7` | Synnada | Seleucid | yes | 62 → **78** | `min(90, 78)` |
| `9 → 10` | Tarquinii | Rome | yes | 42 → **90** | `min(90, 98)` |
| `9 → 10` | Ariminum | Rome | yes | 43 → **90** | `min(90, 97)` |

**The engine's constant 65 and 90 are wrong for 6 of these 8.** It gives 65 for all five non-allegiant cities and 90 for Synnada.

**The same shape holds for a forced capture** (`FUN_0044BB18`, :50200–50209), applied to the loyalty `L′` left after the siege erosion:

- if the capturer is the allegiance nation: `min(90, 140 − L′)`;
- else: `max(40, min(60, 100 − L′))`.

The constant 40 in [decompiled-city-capture-resolution.md](decompiled-city-capture-resolution.md) is only the floor. Seven save captures fit, where `L′` is the erosion floor `⌊L × 3/4⌋` unless noted:

- Mediolanum 77 → 43 (`L′ = 57`);
- Felsina 79 → 41 (`L′ = 59`);
- Brixia 75 → 44 (`L′ = 56`);
- Byblos 61 → 55 (`L′ = 45`);
- Damascus 85 → 40;
- Gordium 65 → 49 (`L′ = 51`, inside the erosion window);
- Laranda and Caere, both allegiant, → 90.

The engine's constant 40 gives the wrong value for five of them `[confirmed: decompile; the saves fit, but L′ was not recomputed from the siege strengths]`. This is outside the rebellion question. It is recorded here because the rebellion reuses the same routine and the same ruleset fields.

## 4. Rebirth, `FUN_0044C360`: confirmed, with additions `[confirmed: listing 0x0044C360–0x0044C525]`

The outline in [decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md) §4 is correct:

- the count is cities with `allegiance == nation` and `loyalty < 40` (`CMP word,0x28; JGE`);
- it proceeds only if the count is `> 7` (`CMP DX,7; JLE` exits).

These points add to it:

- **The count and the transfer cover every city, whoever owns it.** That includes the calling city, other nations' capitals, and cities the loop has not reached yet this quarter. There is no capital test and no ownership test.
  - A capital that defects leaves its old owner's `+0x444` pointing at a city it no longer owns. That is the stale-capital state the elimination report's open item asks about.
  - If the capital was that owner's last city, the elimination block runs, with `FUN_0044C8F0` for a human seat `[derived]`.
- **The transfer loop re-tests each city** with the same predicate, in ascending index order. Nothing earlier in the loop changes another city's loyalty or allegiance, so it moves exactly the counted cities `[derived]`.
- **Relations.** Only the reborn nation's **own row** (`+0x26`) is zeroed. Other nations' entries toward it are left as they are. Then, **for each moved city and before its defection**, `FUN_00449B40(reborn, owner, −8)` writes a symmetric −8 cooldown with that city's owner. It is written again for each further city of the same owner. The result can be asymmetric: a third nation that holds a cooldown toward the dead nation keeps it, while the reborn nation's row says 0 `[derived]`.
- **Reset fields:**
  - unity 450;
  - conquered-by −1;
  - treasury 0 (the dword at `+0x438`);
  - tax base 0;
  - city count 0, so the old stale count is discarded;
  - **tax rate 20** (`+0x44A`);
  - **mobilization 50** (`+0x442`);
  - all 40 slots' troops 0 (state, type and city are kept).

  It does not reset wealth, which the quarterly loop has already zeroed and which the moves then refill. It also leaves the neighbour mask and the human flag alone. A human seat that fell was turned over to the computer, and it comes back as a computer nation.
- **The leader** is one `Random(12)` from the nation's 12 names, with no "differs from the current name" retry, unlike `FUN_0044C8F0`.
- **The capital** is the city now owned by the nation with the greatest `FUN_0044A98C` strength, first by index on a tie. The search starts at `best = 0` with a strict `>`.
  - Every moved city has loyalty 90 and is allegiant, so the strength is `90 × 150 + fortification × 250 + population × 200`.
  - A **former capital of another nation** still passes `FUN_0044B8D0` through the stale pointer. With loyalty 90 > 59 it gets `× 5/3`, so it is strongly favoured `[derived]`.
  - If no city had strength above 0, the capital would be an uninitialised stack word (`PUSH ECX` at `0x0044C364`). Ghidra shows this as a third parameter. It cannot happen when at least 8 cities at loyalty 90 were just moved `[derived]`.
- **The new capital** gets:
  - loyalty `min(99, L + 8)`, so 98;
  - fortification `min(99, F + 10)`, which also discards a fortification order in progress (`F > 100`);
  - population `+10`;
  - maximum population `+20`;
  - tribute `+25`;
  - the capital marker `nation + 0x54` on the map.

  Then `TPremierForm_EnableNation`.
- [city-population-growth.md](city-population-growth.md)'s table lists `50588` as a "capital relocation" population writer. That line is this rebirth capital step. The relocation proper is `FUN_0044BD2C` at `50293`.

**Rebirth never happens outside a quarter tick.** Its only caller is branch (a). So a dead nation comes back only when one of its allegiant cities is under 30 at a tick, and the count is taken at `< 40`.

## 5. The engine today (dev repo `main`, read only)

**What it does with a city under 30** `[confirmed: code]`:

- `QuarterlyCityEconomySystem` (`src/IC2.Engine/Economy/QuarterlyCityEconomySystem.cs:94–96`) publishes `RebellionRiskDetected(cityId, loyalty)` when `CityLoyaltyDraws.Apply` reports that loyalty is below `RebellionLoyaltyThreshold` (30) and the city is not a capital.
- Only the tests reference the event (`tests/IC2.Engine.Tests/Economy/QuarterlyCityEconomySystemTests.cs:78`, `:103`). **Nothing consumes it**, and no city changes owner.
- The capital set is a snapshot, taken once before the loyalty pass.

**`CityState.Allegiance`** exists (`src/IC2.Engine/Model/GameState.cs:191`). Only two places write it: `GameStateFactory` from the world definition, and `OriginalSaveImporter.cs:194` from the save's city `+20` (`+0x14`). No engine code changes it later. That matches the original, where this pass found no write to city `+0x14` outside the loaders `[derived: dump grep]`.

**`CityCaptureResolver.Defect`** (`src/IC2.Engine/Cities/Capture/CityCaptureResolver.cs:219`) is `FUN_0044BED8`:

- the tax-base and wealth move;
- the treasury `× 6` credit;
- unity `+3` capped at 990, and `−20` floored at 250;
- the slot removal, the elimination and the `city.defects-to` event.

**Branches (b), (c) and (d) can call it as it is.** For `L < 30` its constant loyalties (90 and 65) equal the original's formula, and the rebellion cannot reach its elimination path except from a stale capital. Two small differences remain:

- it removes **every** old-owner slot targeting the city, where the original keeps those with 0 troops;
- the formula difference in §3 affects the cascade, not the rebellion.

**What the engine lacks for the rebellion:**

1. **The transfer.** A consumer is needed, or better an inline step, run in city index order right after each city's draws and before `QuarterlyNationEconomySystem`. It is the whole decision in the Answer: (a) or (b) when `owner ≠ allegiance`, otherwise (c), then (d), then nothing.
2. **Unity ≤ 0 as "dead"** for (a), (b) and (d). The engine's `Eliminated` flag and `Unity` 0 coincide today. One exception: the engine's defection path gives an eliminated human 0, where the original leaves 150.
3. **A live, per-state neighbour mask** for (d). Today the mask is `World.StartingNeighbours` or the geometric fallback (`NeighbourGeography`). The original's mask changes through the conquest merge, and T86 is to move it into `GameState`.
4. **Army order for (c).** "The last matching army wins" depends on the order of `GameState.Armies`. The engine's order follows the original only if its deletions compact as the original does, with the last record moved into the hole.
5. **Live reads inside the loop.** Recipient scores read city counts after earlier rebellions in the same quarter. The capital test must see a capital that a rebirth set mid-loop. The two-pass structure (growth for every city, then draws for every city) stays equivalent for (b), (c) and (d), because those move only the current city. A rebirth moves later cities before their growth and draws, so it breaks the equivalence (§2).
6. **Rebirth itself**, `FUN_0044C360` (T87).
7. **A draw for `Random(0)`.** `CityLoyaltyDraws` skips `Random(taxRate)` when the tax rate is 0 (`ownerTaxRatePercent > 0 ? rng.NextInt(…) : 0`). The original's `Random(0)` still advances the seed. At tax 0, every city that rolls `Random(3) == 0` leaves the engine one draw behind the original's stream `[confirmed: both codes]`.
8. **The loyalty formula** in `LoyaltyAfterTransfer` for the cascade and for forced captures (§3). This is not needed for the rebellion, but it uses the same method.

## 6. Evidence in the saves: no rebellion has happened `[confirmed: saves]`

- **Loyalty.** Across the 99 unique local saves (`Documents\imp_conq_original\saves`, `saves-processed`, `releases\run-1-cartago`, and the fixture set), **no city ever has loyalty below 39**. No rebellion can have fired or been pending in any of them. The lowest values are Sidon (Ptolemaic, allegiance Seleucid) at 39–40 and Ambracia (Illyria, allegiance Greece) at 39.
- **News.** The logs hold 23 distinct "*defects from*" lines.
  - 9 are the scenario's scripted history (the DAT's seed log, [news-log-format-and-messages.md](news-log-format-and-messages.md) Q1).
  - The other 14 all directly follow a "*falls to*" by the same receiver against the same old owner, in the same round. They are **capture-cascade** defections (`FUN_0044BA1C`).
  - None sits at the end of a week-11 round, where a rebellion would appear.
- **The rule cannot be checked on a real rebellion.** The saves do check the shared transfer: the §3 table is 8 of 8 on loyalty, and population and fortification are unchanged in every one of them.

**What would confirm it.** Take an AI city with low loyalty and a high tax rate, such as Sidon (39–40, Ptolemaic, allegiance Seleucid). Save at week 11 before the quarter tick and again at week 1. If Sidon falls below 30 at the tick, branch (b) predicts: Sidon goes to Seleucid, loyalty 90, and "*Sidon defects from Ptolemaic to Seleucid.*" appears just before the `Week  1` header. Raising the owner's tax makes the fall more likely: each draw at `taxRate` costs up to `taxRate / 8`.

## What this does not establish

- No save shows a rebellion or a rebirth. Everything in the Answer and §4 is from code.
- Whether a real game reaches the stale-capital states that let a rebellion eliminate its owner.
- The forced-capture `L′` values in §3 were inferred from the erosion window, not recomputed from the sieges' strengths.
- `FUN_0044B8F4`'s list insertion order was not checked (whether it sorts). It changes no game rule read here.

## Reproduction

```text
# dump slices
sed -n 50432,50505p all_app_functions.txt   # FUN_0044C204
sed -n 50507,50600p all_app_functions.txt   # FUN_0044C360
sed -n 50305,50430p all_app_functions.txt   # FUN_0044BED8
sed -n 47727,47747p all_app_functions.txt   # FUN_00449018
sed -n 54836,54862p all_app_functions.txt   # the city loop's draws and the call
sed -n 50198,50210p all_app_functions.txt   # FUN_0044BB18's loyalty (§3)

# machine listing
set JAVA_HOME=%LOCALAPPDATA%\ReTools\jdk-21.0.12.1+1
analyzeHeadless.bat %LOCALAPPDATA%\ReTools\ghidra_projects IC2 -process "Imperial Conquest 2.exe" -noanalysis -readOnly ^
  -scriptPath %LOCALAPPDATA%\ReTools\scripts -postScript DumpListing2.java %LOCALAPPDATA%\ReTools\scratch\rebellion_listing.txt ^
  0x0044c204 0x00451b40 0x0044bed8 0x0044c360 0x00449018
```

The saves were read with an ad-hoc Python reader, which was not committed. It reads cities at `320 × 140 × 2` (334 × 34 bytes: owner `+0x12`, allegiance `+0x14`, loyalty `+0x16`, fortification `+0x1A`, population `+0x1C`). Then come the army count and table (`× 0x290`), the fleet count and table (`× 26`), and the 16 nation records (`× 0x494`). The news log was read as 61-byte slots behind the index word.
