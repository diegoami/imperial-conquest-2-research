# Supply capacity: `troops div 100 + 1` in the supply dialog, `troops div 100` everywhere else

The question: what is the most supply an army or fleet can hold or buy? [`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md) gave the army capacity as `troops / 100`. But its own evidence disagrees by a ton. The Roman army in `11_supply.sav` holds **482 t** against **48,173** troops, and `48173 / 100` is **481**. Is the division a `Round` (481.73 → 482), a ceiling, a `Trunc`, or something else? And do all the ways an army gains supply use the same limit?

**Answer: there are two limits, and neither uses rounding.**

- **The supply dialog (`TAFSupply`) caps an army at `troops div 100 + 1`.** It uses integer division (`IDIV` by 100) followed by an `INC`. There is no FPU instruction, no `System.@Round` and no `@Trunc`. The own-city (free) and foreign-city (paid) paths both apply the same cap. For 48,173 troops the cap is 481 + 1 = **482**. **[confirmed: code, plus the one dialog fill in the data, `11.sav → 11_supply.sav`]**
- **Every other path caps an army at `troops div 100`, with no `+1`.** This covers automatic resupply when an army moves onto a friendly or neutral city, the AI's resupply pass, the army-to-army dialog's rebalancing, and battle winners absorbing the loser's supplies. **[confirmed: 75 distinct army states sit at exactly `troops div 100`, 13 of them with `troops mod 100 ≥ 50`, and none at `troops div 100 + 1` except the dialog fill above]**
- **A fleet's cap is `ships × 8` on every path, with no `+1`.** **[confirmed: code, plus one fleet held at exactly 70 × 8 = 560 t in 26 saves]**
- **Can supply read above 100 %? Yes.** The displayed percentage is `supplies × 10000 div troops`. A dialog fill reads **exactly 100 %** for any army of more than 10,000 troops, including the Roman 482 t. Smaller armies read **above 100 %** when filled through the dialog: 5,000 troops → 51 t → 102 %. The automatic fill reads 99 % for most armies. It reads 100 % only when troops are a multiple of 100.

Line numbers are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`. The instruction listing is new: `supply_capacity_listing.txt`, in the same folder, was made with a new `scripts\DumpListing.java`. Helpers: `FUN_00448FD0(a,b) = min` and `FUN_00448FD8(a,b) = max`, both on 16-bit values. `FUN_0044A698(army)` is the army's total troops: the sum of the 20 slots' `+4` words, floored at 1 (`49042–49063`).

## The instructions [confirmed]

`TAFSupply_ChangeSupply` (`0x0043FC74`) is the free own-city path. This is its army branch:

```text
0043fd8d  CALL 0x0044a698                 ; EAX = total troops
0043fd92  MOV  ECX,0x64
0043fd97  CDQ
0043fd98  IDIV ECX                        ; EAX = troops div 100 (truncating)
0043fd9a  MOV  EDX,EAX
0043fda6  SUB  DX,word ptr [EAX*8+0x47c1f6] ; − army supplies (+10)
0043fdae  INC  EDX                        ; + 1
0043fdb1  CALL 0x00448fd0                 ; step = min(step, room)
```

`TAFSupply_ChangeBuyAmount` (`0x0043FE4C`), the paid foreign path, has the identical sequence at `0043fed4–0043fef8`: `IDIV ECX`, `SUB`, `INC EDX`, `min`. Neither function has an FPU instruction, and neither calls anything but `FUN_0044A698`, `min` and `max`. The fleet branch of both is `MOV DX, ships (+18); SHL EDX,3; SUB DX, supplies (+14)`, with no `INC` (`0043fdba–0043fdd9`, `0043ff06–0043ff25`).

## Which path a purchase takes [derived]

`TAFSupply_FindProviders` (`42569–42747`) offers every city within one tile whose owner is not at war (relation `3`) with the current nation. It also offers the nation's own fleets within one tile. `TAFSupply_CityOrFleet` (`42443–42465`) sets the flag `+0x27d` when the provider is a fleet or a city the current nation owns. That flag enables one of two panels:

**Own city or own fleet: free, immediate** (`TAFSupply_ChangeSupply`, `42890–42982`). Each `+` press applies straight to the army and the provider:

```text
step = +10 or +100
step = min(step, provider stock)                      // city +0x18, or the fleet's supplies
army:  step = min(step, troops div 100 − supplies + 1)
fleet: step = min(step, ships × 8 − supplies)
target.supplies += step;  provider.supplies −= step   // no money moves
```

**Foreign city: paid, staged** (`TAFSupply_ChangeBuyAmount`, `42985–43046`, then `TAFSupply_TransferSupply`, `43049–43086`):

```text
amount = max(0, amount ± 10 or 100)
amount = min(amount, city stock)
army:  amount = min(amount, troops div 100 − supplies + 1)
fleet: amount = min(amount, ships × 8 − supplies)
amount = min(amount, money × 5)                       // the unit's own purse
-- Transfer button --
target.supplies += amount;  city.supplies −= amount
treasury[city owner] += amount div 5;  target.money −= amount div 5
```

So the `+1` applies on both dialog paths, and the fleet cap on neither. [`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md) described only the second path. The first is the one every own-city transfer uses, including the controlled `11_supply` one. That is why army money did not change there.

Two consequences of the code as written:

- **The room term can go negative, and nothing floors it at 0.** If an army holds more than `troops div 100 + 1`, for example after losing troops, then `+` gives a negative step. The army loses supply back to the provider, down to the cap. On the paid path, a negative amount is refunded at `amount div 5`, which truncates toward zero.
- **Cost truncates.** `amount div 5` means 4 t are free and 79 t cost 15 talents.

## Every other writer caps at `troops div 100` [derived, then confirmed below]

| Writer | Cap | Lines |
| --- | --- | --- |
| `FUN_0044F6D8(city, army)`: army resupply without the dialog | `min(troops div 100 − supplies, city stock)` | `53077–53115` |
| — called when a human's move ends against a non-hostile city (`TUnitMap_MoveHumanArmy` → `FUN_0044D734`'s tail) | same | `51646–51656` |
| — called by the AI army pass (`FUN_0044F31C` → `FUN_0044E41C`) for every non-hostile city within 4 tiles | same | `52240–52247`, `52926` |
| `FUN_0044F7E4(city, fleet)`: fleet resupply, AI fleet pass only (`FUN_0044F608` → `FUN_0044E1FC` / `FUN_0044E5DC`) | `min(ships × 8 − supplies, city stock)` | `53120–53158` |
| `TArmyToArmy_OK`: each army's supplies above `troops div 100` are pushed to the other | `troops div 100` | `44604–44622` |
| `TBattleOver_OK`: the tactical winner absorbs the loser's supplies | `min(sum, troops div 100)` | `57620–57625` |
| `FUN_0044AEE4`, instant battle, **attacker wins** | `min(sum, troops div 100)` | `49647–49654` |
| `FUN_0044AEE4`, instant battle, **defender wins** | none: plain sum | `49687–49690` |
| `TUnitMap_JoinArmies` | none: plain sum | `46991–46995` |

`FUN_0044F6D8` uses the same `IDIV` by 100 as the dialog, then `SUB AX, supplies`, with no `INC` (`0044f6ef–0044f712`). Like the dialog, its room term is not floored at 0. An over-cap army that reaches a friendly city is trimmed to `troops div 100`, and the surplus goes back to the city.

`FUN_0044F6D8` also differs from the dialog in two ways that T08's automatic resupply would need:

- **Own city:** it is free. Then, if the army's purse is over 1,000, the excess goes to the treasury. If the purse is under 500 and the treasury is positive, the purse gains 500 from the treasury (`53091–53104`). That fits the many AI armies seen holding exactly 500 or 1,000 money.
- **Foreign city:** tons are capped at `money div 5`, **not** `money × 5` as in the dialog. The cost is again `tons div 5` (`53106–53110`).

Resolved open items: this is the "auto-resupply" left untraced by [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md). It is also the withdrawal from city stocks that [`city-population-growth.md`](city-population-growth.md) attributed to `53090–53156`.

## Checked against saves

All 54 local saves were read directly. They are all distinct. Army records start at `0x18A5E`, 656 bytes each: supplies at `+10`, money at `+12`, and troops as the sum of the 20 slot words at `+20 + 32·i`. Fleets follow the army table, 26 bytes each: supplies at `+14`, ships at `+18`. The scan covered 627 army records and 158 fleet records. Tombstones and empty records (troops ≤ 1) are excluded.

### The dialog fill: `11.sav → 11_supply.sav` [confirmed, 1 of 1]

| | `11.sav` | `11_supply.sav` |
| --- | ---: | ---: |
| Roman army 0 troops | 48,173 | 48,173 |
| supplies | 403 | **482** |
| money | 296 | 296 |
| Rome (city 85) stock | 1,810 | 1,731 |

The army is at `(100, 42)`, next to Rome, which Rome owns, so this is the free `ChangeSupply` path. Money is unchanged, as that path predicts.

The value itself pins the cap. Every step is ±10 or ±100, so 403 can only reach a value ending in 2 on a step the code clipped. The two clips are provider stock (1,731, far from binding) and capacity. So the capacity was 482 = `48173 div 100 + 1`. The same state reappears in `11_ptol.sav` and `1_rome_270_summer_7.sav`.

This one sample cannot tell `div + 1` from `Round`, because `48173 mod 100 = 73`. The code can: there is no rounding, just `IDIV` then `INC`.

### The other paths: 75 distinct states at exactly `troops div 100` [confirmed]

| Army supplies | `troops mod 100 = 0` | `1–49` | `50–99` | Distinct states | Records |
| --- | ---: | ---: | ---: | ---: | ---: |
| `= troops div 100` | 39 | 23 | **13** | 75 | 198 |
| `= troops div 100 + 1` | 0 | 0 | 1 (the dialog fill) | 1 | 3 |

Two groups separate the candidate formulas:

- **The 13 states with `mod ≥ 50` rule out `Round` and a ceiling.** Examples: 58,372 troops → 583 t, 69,199 → 691, 72,662 → 726, 57,099 → 570. Each would be one ton higher under either. Some hold that value across many saves, e.g. 58,372 → 583 in 8 saves.
- **The 62 states with `mod < 50` rule out `+1` on these paths.**

The Roman army in the `1_cartago_271_*` series (an AI there) shows the automatic fill turn after turn. Its supplies step through 377, 363, 351, 341 and 326. Each is exactly `div 100` of a troop total it held: 37,744, 36,392, 35,120, 34,184 and 32,689. Three of those totals have `mod ≥ 50`. The army keeps losing troops after each fill, so a save often shows the fill for the previous troop total.

About 400 records sit below capacity, and 21 live records sit above it. Most above-capacity records read 101–109 %; two read 127 % and 332 %. The ones traced are armies whose troops fell after a fill. For example, that Roman army dropped from 37,744 to 36,392 troops with its supplies still at 377. Merges can also do it, since `JoinArmies` sums without a cap. Not every over-capacity record was traced.

### Fleets [confirmed]

One fleet (owner 3, 70 ships) holds exactly **560 = 70 × 8** in 26 saves. Only one fleet ever holds more than `ships × 8`: the Carthaginian fleet in the `1_rome_270_*` series. It held 630 t at 90 ships (cap 720). It still held 630 t after losing ships at sea down to 67, then 563 t and 514 t at 49 ships (cap 392). The other 128 fleet records are below capacity.

## The percentage display [confirmed]

`TInformation_ShowArmyDetails` prints `supplies × 10000 div troops` (`41047`), for the current nation's armies only. With `k = troops div 100` and `r = troops mod 100`:

| Fill | Reads |
| --- | --- |
| dialog, `k + 1` | **≥ 100 % always.** Exactly 100 % for any army over 10,000 troops. Above 100 % when `100k + 101r ≤ 10,000`: 10,000 troops → 101 t → 101 %; 5,000 → 51 t → 102 %; 1,000 → 11 t → 110 %. |
| automatic, `k` | **≤ 100 % always.** Exactly 100 % only when `r = 0`. 99 % for any army of 9,900 or more troops otherwise; this is the "99 %" on most AI armies in the saves. |

So yes, a legitimately bought stock can exceed 100 %, but only through the dialog and only for armies of 10,000 troops or fewer. Losing troops after a fill can push any army over 100 %, as the over-capacity records above show. Nothing treats values over 100 % specially. The morale rule in [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md) compares the percentage with 10 and 15 only, and consumption depends on troops, not the percentage.

The `+1` looks like it exists so that a dialog fill reads 100 % rather than 99 %. That is an interpretation. The code gives no reason.

## What an implementation needs

- **Dialog, army:** room = `troops div 100 + 1 − supplies`, using integer division. It applies on both the own-city (free) and foreign-city (paid) paths.
- **Dialog, fleet:** room = `ships × 8 − supplies`.
- **Everything else, army:** `troops div 100`. This covers automatic resupply, army-to-army rebalancing, battle absorption and instant-battle attacker wins. Two paths have no cap: defender wins and joins.
- **Fleet everywhere:** `ships × 8`.
- The room is not floored at 0 in the original. A port that floors it will differ only for armies already over their cap.
- The foreign credit side, which T08 has tagged open: `TransferSupply` pays `amount div 5` into the **selling city's owner's** treasury (`43071–43073`). This is code only; no save has a foreign purchase yet.

## Corrections to existing reports

- [`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md) §TAFSupply: the dialog's army cap is `troops div 100 + 1`, not `troops / 100`. The Roman 482 t is the cap, not a 1-ton excess. The own-city path is `ChangeSupply`, which is free and has no money cap. The `money × 5` cap and the `amount / 5` cost belong to the foreign path only.
- [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md), "Auto-resupply": traced above (`FUN_0044F6D8`, `FUN_0044F7E4`).
- [`city-population-growth.md`](city-population-growth.md), "Who withdraws from city stocks between ticks": the same functions.
- [`pending-offer-block-army-split-and-naupactus.md`](pending-offer-block-army-split-and-naupactus.md) asked whether the split dialog's supply is capped. `TArmyToArmy_OK` pushes each side's supplies above `troops div 100` to the other army on `OK`.

## Still open

- **A second dialog fill** with `troops mod 100 < 50` would show `div + 1` in a save, not just in code. For example, fill a 22,000-troop army at an own city by pressing `+10` until it stops. It should stop at **221** t and read **100 %**. A 5,000-troop army should stop at **51** t and read **102 %**.
- **A foreign purchase** has still never been saved. It would confirm the `money × 5` cap, the `amount div 5` cost and the credit to the seller.
- **A human move onto a friendly city.** The code says it fills to `troops div 100`, not `+1`. No controlled save shows it yet.

## Reproduction

- **Dialog:** `TAFSupply_ChangeSupply` `42890–42982`, `TAFSupply_ChangeBuyAmount` `42985–43046`, `TAFSupply_TransferSupply` `43049–43086`, `TAFSupply_CityOrFleet` `42443–42465`, `TAFSupply_FindProviders` `42569–42747`.
- **Automatic:** `FUN_0044F6D8` `53077`, `FUN_0044F7E4` `53120`, `FUN_0044D734` tail `51629–51657`, `FUN_0044E41C` `52220`, `FUN_0044F31C` `52901`, `FUN_0044FA20` `53208`.
- **Other writers:** `TArmyToArmy_OK` `44572`, `TUnitMap_JoinArmies` `46950`, `FUN_0044AEE4` `49608`, `TBattleOver_OK` `57566`, `TInformation_ShowArmyDetails` `41000`.
- **Listing:** `analyzeHeadless <ReTools>\ghidra_projects IC2 -process "Imperial Conquest 2.exe" -noanalysis -readOnly -scriptPath <ReTools>\scripts -postScript DumpListing.java supply_capacity_listing.txt 0x0043fc74 0x0043fe4c 0x0043ff98 0x0044f6d8 0x0044f7e4 0x0044a698 0x0044aee4 0x00459220`. The project path is the `ghidra_projects` folder itself, not `ghidra_projects\IC2`.
- **Save checks:** a direct Python reader over the local saves using the offsets above. Nothing was written to either repository.
