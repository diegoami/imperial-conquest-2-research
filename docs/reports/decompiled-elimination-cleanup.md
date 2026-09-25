# Nation elimination, decompiled: armies deleted, fleets at sea sunk, fleets on the slipway handed over

**The question** (dev-repo bug [#366](https://github.com/diegoami/imperial_conquest_2/issues/366)): when a nation is eliminated, what does the original do with its armies, fleets and related state? The dev engine keeps them on the map. Its T69 is about to reset the eliminated nation's relations to cooldowns and reject a war declaration against it, which would leave those forces untouchable forever.

All line numbers are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`. Callers were checked with `FindXrefs.java` (see Reproduction). Record bases: city `0x00479590` (stride `0x22`), nation `0x00474670` (stride `0x494`), army `0x0047C1EC` (stride `0x290`), fleet `0x0049C26C` (stride `0x1A`), map grid `0x0045E870` (`x × 0x118 + y × 2`).

## Answer

- **The original deletes every army the eliminated nation owns** `[confirmed: decompile]`. It deletes every one of its fleets that is on the map, and with each fleet the army it carries. Fleets still under construction are **not** deleted: they go to the conqueror, with the countdown and build city unchanged `[confirmed: decompile]`. Units, supplies and the money in each deleted army or fleet are destroyed, not credited to anyone `[confirmed: decompile]`.
- **Deletion is a tombstone** (owner = `-1`), and the record is compacted later, at the next AI-loop pass. Compaction moves the **last** record into the hole, so exactly one record changes index. The only cross-reference it renumbers is a fleet's carried-army index `[confirmed: decompile]`.
- **Both elimination paths run the same two loops.** They are the defection path `FUN_0044BED8` (when the old owner's city count reaches 0) and the conquest path `FUN_0044C528` (`"X conquers Y."`). The conquest path does much more besides, below `[confirmed: decompile]`.
- **In practice, elimination is almost always the conquest path.** It fires **when a capture leaves the loser with fewer than 6 cities** (or takes its capital when the capital cannot be moved), and it annexes every remaining city at once. It is not "lose the last city". Defection alone cannot empty a live nation, because capitals never defect through the normal defection routes `[confirmed: decompile; the "almost always" is derived]`.
- **`FUN_0044C8F0` is not an elimination cleanup.** It is the leader-falls routine (deposition), and elimination calls it only for a human seat. It shows `THumanFalls` ("*Your nation has been conquerred by X*") and turns the seat over to the computer `[confirmed: decompile]`.
- **Galatia's elimination** (`1_rome_270_winter_5.sav → _7.sav`, the only elimination in the local save set) agrees on every field that can be checked: unity 0, capital `0xFFFF`, conquered-by = Seleucid, relations reset, recruitment troops zeroed, and a stale city count of 5. Galatia had **no armies or fleets** at the time, though, so the save cannot confirm the disposal `[confirmed: saves, for the nation fields only]`.

## 1. The two tables

### `DAT_0047C1F0` is the army table's owner word

The army record is 656 bytes (`0x290`) at `0x0047C1EC`, with count `DAT_004A0324`. The loops step a `short*` by `0x148` (= `0x290 / 2`), so `DAT_0047C1F0` is **`+4`, the owner**. The fields this pass uses, all already named in [decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md):

| Offset | Address | Field |
| --- | --- | --- |
| `+0 / +2` | `0x47C1EC / EE` | x, y |
| `+4` | `0x47C1F0` | owner; `0xFFFF` = tombstone |
| `+8` | `0x47C1F4` | `CoveredCell`, the map code under the marker; `-1` = aboard a fleet |
| `+10 / +12 / +14` | | supplies, money, morale |
| `+16 + 32k` | `0x47C1FC` | 20 unit slots |

### `DAT_0049C26C` is the fleet table

The fleet record is 26 bytes (`0x1A`) at `0x0049C26C`, with count `DAT_004A0326`. It is the same table as `supply-driven-morale-and-fleet-attrition.md` and `decompiled-map-code1-overlay.md` use:

| Offset | Address | Field |
| --- | --- | --- |
| `+0 / +2` | `0x49C26C / 6E` | x, y |
| **`+8`** | `0x49C274` | **owner**; `0xFFFF` = tombstone |
| **`+10`** | `0x49C276` | **construction countdown**: 24 when ordered, **`0xFFFF` once launched**, so `-1` means "on the map" |
| `+12 … +18` | | moves, supplies, money, ships |
| `+20` | `0x49C280` | build city while under construction, condition % once launched |
| `+22` | `0x49C282` | carried army index; `0xFFFF` = none |
| `+24` | `0x49C284` | `CoveredCell` |

So the elimination loop's test `+10 == -1` means "the fleet is launched" `[confirmed: decompile; the +10 identification is from FUN_0044A004/FUN_0044A050 in the record-fields report]`. It is neither a garrison nor a mercenary list. Garrisons are the nation's 40 recruitment slots (`nation +0x2E4`), covered in §5. Mercenary offers are a separate table (`DAT_0049DA18`), which elimination never touches.

## 2. `FUN_0044AB90` and `FUN_0044AD38`: tombstone, do not compact

### `FUN_0044AB90(army)`, :49372: delete an army `[confirmed: decompile]`

```text
if army[+8] < 0:                                   // aboard a fleet
    f = FUN_00449970(army.x, army.y)               // :48366, the first live fleet at that tile
    fleet[f][+22] = -1                             // the carrier forgets it
else:
    map[army.x][army.y] = army[+8]                 // restore the covered cell (a city marker if it stood in a city)
army[+4] = -1                                      // tombstone
```

Nothing else is written. The 20 unit slots, supplies (`+10`) and money (`+12`) stay in the dead record until compaction overwrites it. They are **not** credited to any treasury or city.

A quirk: if `FUN_00449970` finds no fleet it returns `-1`, and the write lands at `fleet[-1]+22`. That happens only if the state is already inconsistent `[derived]`.

### `FUN_0044AD38(fleet)`, :49493: delete a fleet `[confirmed: decompile]`

```text
if fleet[+10] == -1:  map[fleet.x][fleet.y] = 0    // writes 0, not the covered cell (+24)
if fleet[+22] >= 0:   FUN_0044AB90(fleet[+22])     // the army aboard dies with the fleet
fleet[+8] = -1                                     // tombstone
```

The carried army is deleted **whoever owns it**. The fleet's money (`+16`), supplies and ships are destroyed.

### Compaction happens later, and it swaps in the last record `[confirmed: decompile]`

`FUN_0044ADB0` (:49537) walks each table **from the top down**. For each tombstone it calls:

- `FUN_0044ABE0(i)` (:49396), for armies. It first renumbers every fleet whose `+22 == count − 1` to `i`, then copies army `count − 1` into slot `i`, then decrements `DAT_004A0324`.
- `FUN_0044AD7C(i)` (:49515), for fleets. It copies fleet `count − 1` into slot `i` and decrements `DAT_004A0326`. Nothing needs renumbering, because no record stores a fleet index: a carried army finds its carrier by coordinates.

Walking from the top means the record moved into a hole is always live. Only the moved record changes index. The single renumbered reference is the fleet's `+22`. Nothing else that holds an army index, such as the UI selection or AI targets, is fixed up `[derived: nothing else is written in FUN_0044ABE0]`.

`FUN_0044ADB0` is called only from `FUN_00451FDC` (:54939), the AI-seat loop: once on entry and again before each computer seat's turn. So tombstones persist within a seat's turn and can appear in a save `[confirmed: decompile]`. The dev repo's `SaveArmyTable`/`SaveFleetTable` already skip them.

Inside the elimination loops, `FUN_0044AB90`/`FUN_0044AD38` only tombstone, so iterating by index while deleting is safe.

### Order inside elimination: armies first, then fleets

1. **Army loop.** An eliminated army aboard its own fleet clears that fleet's `+22`.
2. **Fleet loop.** A launched fleet is deleted. Its `+22` is already `-1` by then, so nothing is deleted twice. A fleet under construction changes owner only.

An army of **another** nation aboard an eliminated fleet dies with it, if cross-nation embarkation is possible. `TUnitMap_SelectUnit` only asks for a "friendly" fleet, so that case is `[hypothesis]`.

## 3. `FUN_0044C8F0`, :50761: leader falls; elimination uses it for human seats only

This routine is already decoded in [upkeep-payment-and-desertion.md](upkeep-payment-and-desertion.md). Re-read `[confirmed: decompile]`:

```text
if AI:    news("<nation> depose their leader <leader>.")
else:     DAT_004A032C = nation; TPremierForm_HumanLeaderFalls()   // :59142
leader   = another random name from the nation's 12
unity    = max(unity, min(550, unity + 150))
treasury = treasury < 0 ? 0 : treasury + 1000
relations −5 … −1 with anyone → 0  (via FUN_00449B40(n, k, 0))
```

`TPremierForm_HumanLeaderFalls` shows the `THumanFalls` form, then calls `FUN_00449078` (:47777), which clears the human flag `+0x490` and gives the seat a new leader. If no human seat is left, it closes the forms and the game is over. If the fallen seat is the active one and humans remain, it ends the turn.

`THumanFalls_InitializeForm` (:56353) picks the text from `+0x44E`. When that field is `≥ 0`, it prints "*Your nation has been conquerred by <nation[+0x44E]>.*". Both elimination paths write `+0x44E` **before** calling `FUN_0044C8F0`. That confirms `+0x44E` as **conquered-by**, which the diplomacy report left inferred. The Galatia save also reads `+0x44E = 2`, Seleucid `[confirmed: decompile + save]`.

**Callers** (`FindXrefs`): `FUN_0044BED8` (`0x0044C13C`) and `FUN_0044C528` (`0x0044C81E`), human-only in both; `FUN_00451B40` (AI debt deposition, `Random(9) == 0`); and `FUN_00452034` (every human turn start: 250 BC, 334 cities, unity < 400, or in debt).

**An order quirk** `[derived]`:

- `FUN_0044BED8` zeroes unity **before** calling `FUN_0044C8F0`, so a human eliminated by defection ends with **unity 150**, not 0.
- `FUN_0044C528` zeroes unity **after**, so a human it eliminates ends at 0.

Unity `> 0` is what the turn loop, the AI and Politics treat as "alive" (§5). The former human seat therefore keeps taking (empty) AI turns and can still be targeted diplomatically.

## 4. The two elimination paths

### Who calls what (`FindXrefs`, all direct calls)

| Function | Callers |
| --- | --- |
| `FUN_0044C528` (conquest) | `FUN_0044BB18` only (`0x0044BCF7`, `0x0044BD19`), the forced-capture transfer. The "reached from `"conquer"`" of `decompiled-city-capture-resolution.md` is the string **inside** it, not a caller. |
| `FUN_0044BED8` (defection) | `FUN_0044BA1C` (capture cascade), `FUN_0044C204` twice (quarterly rebellion, from `FUN_00451B40` :54856, non-capitals with loyalty < 30), `FUN_0044C360` (rebirth) |
| `FUN_0044C360` (rebirth) | `FUN_0044C204` only |
| `FUN_0044C8F0` | see §3 |

### When the conquest fires: `FUN_0044BB18`, :50150 `[confirmed: decompile]`

These checks run after the city has moved and the cascade `FUN_0044BA1C` has run. `FUN_0044B8D0` (:50015) is "this city is some nation's capital".

```text
if captured city is not a capital:
    if loser.cityCount (+0x446) < 6:  FUN_0044C528(loser, capturer)
else:                                                  // the loser's capital fell
    moved = false
    if loser.unity > 400 and loser.cityCount > 6:  FUN_0044BD2C(loser, &moved)   // :50234, unity −50, then
                                                   // "<X> have moved their capital to <city>." if a city > 10 tiles away exists
    if not moved:  FUN_0044C528(loser, capturer)
```

So **a nation is conquered as soon as a capture leaves it with 5 or fewer cities**, and every remaining city goes to the capturer at once. Galatia fits exactly: the save's stale city count is **5** (below), the value at the moment `FUN_0044C528` fired. Its 5 silent transfers are the 5 cities with no news line in [galatia-elimination-and-city-resupply-confirmed.md](galatia-elimination-and-city-resupply-confirmed.md) `[confirmed: code + save]`.

### Why defection almost never empties a nation `[derived]`

`FUN_0044BA1C` and the rebellion caller of `FUN_0044C204` both skip capitals. A live nation always holds its capital: when the capital is captured, it is either moved or the whole nation is conquered. So `FUN_0044BED8` can take a nation's last city only through `FUN_0044C360` (rebirth), which calls `FUN_0044BED8` **without** a capital check, or from a state where the capital pointer is already stale.

### `FUN_0044BED8`, :50307: the defection path's elimination block (from :50382) `[confirmed: decompile]`

```text
if old.cityCount == 0:
    TPremierForm_DisableNation(old)        // :58988, greys the nation's entry in the premier form's list and menu
    old.unity (+0x440)  = 0
    old.conqueredBy (+0x44E) = receiver    // the nation that got the last city
    if old is human: FUN_0044C8F0(old)
    for k in 0..15: FUN_00449B40(old, k, 0)
    for each army a:  if a.owner == old: FUN_0044AB90(a)
    for each fleet f: if f.owner == old:
        if f[+10] == -1: FUN_0044AD38(f)  else f.owner = receiver
if receiver is human: TPremierForm_RefreshForms
```

It writes no conquest news (the only line is the ordinary "*C defects from X to Y.*"), no treasury, no capital sentinel (`+0x444` is left as it was) and no recruitment-slot wipe beyond the ordinary per-city one.

### `FUN_0044C528(loser, winner)`, :50602: conquest, in order `[confirmed: decompile]`

1. `MakeSound(10)`.
2. **Every city with `owner == loser`** goes to the winner. `FUN_0044B8F4` moves the city between the sorted city lists, the owner is written, and `FUN_0044A794` repaints the marker.
   - Loyalty: `min(80, 120 − L)` if `allegiance == winner`, else `min(70, max(40, 100 − L))`; then `+ Random(6)`.
   - The winner gets: city count `+1`, wealth `+ pop × 3000`, treasury `+ contribution × 6`, tax base `+ contribution × 4`.
   - **The loser's city count, wealth and tax base are never decremented.** This is Galatia's stale `cities = 5`, the open anomaly in the Galatia report.
3. Winner unity `= min(990, unity + 50)`.
4. **If the loser's treasury is > 0, the winner gains it.** The loser's treasury is not zeroed, so the amount is copied, not moved. Galatia's was `−911` and nothing moved: Seleucid went `−860 → −592` from its own income, and Galatia stayed `−911`.
5. For `k` in 0..15:
   - `FUN_00449B40(loser, k, 0)`, the relation reset.
   - If `k` is in the loser's **neighbour mask** (`+0x46`) and `k ≠ winner`: the winner gains `k` as a neighbour, and `k` gains the winner.
6. The army loop and the fleet loop, **identical to `FUN_0044BED8`'s**, with `winner` as the receiver of fleets under construction.
7. News: a dashed line, "*<winner> conquers <loser>.*", a dashed line.
8. `TPremierForm_DisableNation(loser)`; `loser.conqueredBy (+0x44E) = winner`; if the loser is human, `FUN_0044C8F0(loser)`.
9. `loser.unity = 0`; `loser.capital (+0x444) = -1`, then `FUN_0044A794(old capital)` repaints it as an ordinary city.
10. **All 40 recruitment slots: `troops (+4) = 0`.** State, type and city stay. Galatia's slots read `(24,3,0,218) (24,0,0,218) (18,0,0,218) (6,2,0,218)` afterwards, with their states still ageing.
11. `RefreshForms`. If the winner now holds more than 333 cities, `DAT_004A032C = winner` and `HumanLeaderFalls`, which is the victory screen.

### The relation reset, `FUN_00449B40(a, b, 0)`, :48472 `[confirmed: decompile + save]`

With value 0 the setter maps the current `r = rel[a][b]` as follows: trade `1 → −8`, alliance `2 → −24`, war `3 → −18`, **anything else → 0**. It writes the result to both `[a][b]` and `[b][a]`. The ally-war cascade runs only for values 2 and 3, so it never fires here. The loop also covers `k = a`, and it **zeroes cooldowns the nation already had**.

Galatia before: `[0,−7,3,0,0,−5,−1,−7,−8,−8,−8,−10,0,−8,1,−8]`. After: `[0,0,−18,0,0,0,0,0,0,0,0,0,0,0,−8,0]`. The war with Seleucid became `−18`, the trade with nation 14 became `−8`, and every existing cooldown became 0. Seleucid's row reads `−18` at Galatia.

### `FUN_0044C360`, :50507: rebirth, not a collapse `[confirmed: decompile]`

`FUN_0044C204` (:50432) is the quarterly rebellion of a non-capital city with loyalty < 30. When the city's allegiance (`+0x14`) differs from its owner and **the allegiance nation's unity is < 1**, it calls `FUN_0044C360(allegiance)`:

```text
n = cities with allegiance == nation and loyalty < 40
if n > 7:
    unity 450, conqueredBy −1, treasury 0, taxBase 0, cityCount 0, +0x44A = 20, +0x442 = 50,
    40 slot troops 0, relation row +0x26 all 0, new leader name
    for each such city: FUN_00449B40(nation, city.owner, −8); FUN_0044BED8(city, nation)
    capital = the strongest such city (+8 loyalty, +10 fortification, +10 population, +20, +25, capital marker)
    TPremierForm_EnableNation(nation)
```

**Elimination is not permanent in the original.** A dead nation comes back when more than 7 cities that still hold allegiance to it are disloyal. It comes back with no armies and no fleets, because those were deleted when it died. This corrects the "resets the collapsing nation" row in [nation-tax-base-and-city-economy-fields.md](nation-tax-base-and-city-economy-fields.md).

## 5. What else elimination does and does not touch

- **Turn order.** The rotation `DAT_0049EFE8` is untouched, and the seat stays in it. `FUN_0044FA20` (:53208) simply skips a seat's AI phases while its unity `≤ 0` `[confirmed]`.
- **Being targeted.** Every diplomatic path requires the target's unity `> 0` `[confirmed]`:
  - The AI's war and treaty picks, `FUN_0044FB7C` (:53335 and the loops that follow).
  - The human's Politics screen: `TPolitics_InitialiseForm` (:55042) disables all four relation buttons of a nation with unity 0, and `TPolitics_ChangeIR` (:55103) refuses unless unity `> 0`.
  - The turn-start offer roll, `FUN_00452034`.

  So **no one can declare war on an eliminated nation**. That matches T69. The original has no stranded forces to worry about, because it deleted them.
- **Pending offer.** `FUN_00452034` excludes dead proposers, and elimination does not clear the pending-offer block `DAT_0049F008`. The block is written and shown within the same turn start, so it probably cannot straddle an elimination `[hypothesis]`.
- **Mercenaries.** The offer table `DAT_0049DA18` is not touched. Hired mercenaries are ordinary units in armies and die with them `[confirmed: absence in the three functions]`.
- **Garrisons (recruitment slots).**
  - Conquest zeroes every slot's troops.
  - Defection removes only the slots at the defecting city, through the ordinary per-city step `FUN_0044A610` (:48994), which runs on every defection.
  - Capture (`FUN_0044BB18`) removes the slots at the captured city `[confirmed]`.
- **Treasury.** Conquest copies a positive treasury to the winner, and defection does not transfer it. The loser's treasury is never zeroed, which does not matter unless the nation is reborn, and rebirth zeroes it `[confirmed]`.
- **News.** Conquest writes the dashed "*X conquers Y.*" banner. Defection writes no elimination news `[confirmed]`.
- **Premier form.** `DisableNation` greys the nation's list entry and menu item. `EnableNation` reverses it on rebirth `[confirmed: decompile; the UI reading is derived]`.

## 6. What a reimplementation must do

1. On elimination, **delete every army the nation owns**. Unembark any of them from its carrier by clearing the carrier's carried-army id. Restore the map cell each army covered.
2. **Delete every launched fleet the nation owns, together with the army aboard**, whoever owns that army. Clear its map marker.
3. **Give every fleet still under construction to the receiving nation**: the capturer in a conquest, or the nation that received the last city in a defection. Keep its countdown and build city.
4. **Destroy, do not transfer,** the deleted records' units, supplies and money. No treasury or city is credited.
5. Leave no dangling ids. With string ids there is nothing to renumber, but a carrier's carried-army id and any cached selection or AI target must be cleared.
6. Reset relations with `FUN_00449B40(dead, k, 0)` for all `k`: trade → −8, alliance → −24, war → −18, **everything else, including existing cooldowns, → 0**. Write it symmetrically.
7. Set conquered-by. Keep the nation record and its seat. Treat unity `≤ 0` as "skip its turn and refuse it as a diplomatic target".
8. For a human seat: show the "conquered by" screen, turn the seat over to the computer, and end the game if no human seat is left.
9. For fidelity beyond #366, the conquest path (`FUN_0044C528`):
   - a capture that leaves the loser with fewer than 6 cities, or that takes a capital which cannot move, annexes everything;
   - the winner gets `+50` unity, the positive treasury and the neighbour mask;
   - every recruitment slot's troops are zeroed;
   - the capital is set to the sentinel;
   - the banner news is written;
   - capital relocation (`FUN_0044BD2C`) and rebirth (`FUN_0044C360`) are related mechanics.

## What this does not establish

- **No save shows an eliminated nation's forces being disposed of.** Galatia had none, and it is the only elimination in the 99-save fixture set and the local `imp_conq_original` saves. The disposal is `[confirmed]` from code only. A save pair where a nation with a standing army or a launched fleet is conquered would confirm it, and would also show whether tombstones appear before compaction.
- Whether cross-nation embarkation exists, which decides whether the fleet loop can kill a third nation's army.
- Whether any path other than `FUN_0044C360` lets `FUN_0044BED8` take a nation's last city in real play.
- The `DisableNation` UI reading (which list and which menu) was not checked against the form resources.
- `FUN_0044BD2C`'s capital-move choice (`strength / 10 / distance`, distance > 10) is only summarised here and was not checked against a save.

## Dev-repo engine, for comparison (read-only)

These files were read, not modified:

- `src/IC2.Engine/Cities/Capture/NationElimination.cs`
- `src/IC2.Engine/Cities/Capture/CityCaptureResolver.cs`
- `src/IC2.Engine/Model/GameState.cs`

`NationElimination.ApplyIfLastCityLost` sets `Eliminated`, `CapitalCityId = null` and `Unity = EliminationUnityReset` (0). Both `Capture` and `Defect` call it when the old owner holds zero cities, and both publish `NationConquered`. **What the engine does not yet do:**

1. **Dispose of the eliminated nation's armies.** They stay in `state.Armies`, which is bug #366.
2. **Dispose of its launched fleets** and the army each carries, and **hand fleets under construction** (`ConstructionTicksRemaining != null`) to the receiver.
3. **Clear the carrier link** when an embarked army is deleted (`FleetState.CarriedArmyId`), and restore the army's covered cell.
4. **Reset relations as the original does.** This is T69, in flight. The original also zeroes pre-existing cooldowns and the self entry.
5. **Record conquered-by.** The engine has no `+0x44E` equivalent. `NationConquered` carries the name, but the state does not keep it.
6. **Handle a human seat's fall.** The seat is not turned over to the computer and the game does not end.
7. **Run the conquest cascade `FUN_0044C528`.** The engine eliminates only at zero cities, one capture at a time. The original annexes everything once a capture leaves fewer than 6 cities, or takes an immovable capital. With it go:
   - the winner's `+50` unity, `× 6` treasury credit per city and different loyalty rule;
   - the transfer of a positive treasury;
   - the neighbour-mask merge;
   - zeroing all 40 slots' troops.

   The resolver's own remarks call this "not implemented here".
8. **Relocate the capital** (`FUN_0044BD2C`). The news template `nation.capital-moved` exists, but nothing calls it.
9. **Rebirth** (`FUN_0044C360`). The engine's `Eliminated` is a one-way flag, while the original's "dead" is unity 0, which rebirth reverses.

Three differences are the other way round: the engine does something the original's **defection** path does not.

- It publishes `NationConquered`.
- It clears the capital.
- It applies unity 0 to a human seat (the original leaves 150 after `FUN_0044C8F0`).

These matter only if `Defect`-driven elimination is reachable in the engine. In the original it is nearly unreachable (§4).

## Reproduction

```text
# dump slices
sed -n 49372,49560p all_app_functions.txt   # FUN_0044AB90 … FUN_0044ADB0
sed -n 50150,50306p all_app_functions.txt   # FUN_0044BB18, FUN_0044BD2C
sed -n 50305,50430p all_app_functions.txt   # FUN_0044BED8
sed -n 50432,50880p all_app_functions.txt   # FUN_0044C204, FUN_0044C360, FUN_0044C528, FUN_0044C8F0

# callers
set JAVA_HOME=%LOCALAPPDATA%\ReTools\jdk-21.0.12.1+1
analyzeHeadless.bat %LOCALAPPDATA%\ReTools\ghidra_projects IC2 -process "Imperial Conquest 2.exe" -noanalysis -readOnly ^
  -scriptPath %LOCALAPPDATA%\ReTools\scripts -postScript FindXrefs.java 0044c528     (and 0044bed8, 0044c360, 0044c8f0)
```

The saves were read with an ad-hoc parser (not committed). Army table at `320×140×2 + 334×34`, preceded by its count word, then the fleet count and table, then 16 nation records. The script read Galatia (nation 12) in `1_rome_270_winter_5.sav` and `1_rome_270_winter_7.sav`, and it scanned every local `.sav` for a nation with unity ≤ 0 or capital `0xFFFF`. Only Galatia appears, in `1_rome_270_winter_7/7_b/9/9_b/11.sav` and `1_thracia_271_autumn_1.sav`, always with 0 armies and 0 fleets.
