# Upkeep at the quarter boundary: the treasury pays regulars, the army purse pays mercenaries, and only mercenaries desert

The question: at the quarter boundary, where does upkeep come from, and what happens when it cannot be paid? [`decompiled-quarterly-billing-and-economy.md`](decompiled-quarterly-billing-and-economy.md) says army and garrison upkeep comes from "a nation's available funds", and that an unpaid army loses `troops / 100` and "degrades" through `FUN_0044ac3c`. [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md) shows a Thracian army's **own purse** falling `100 → 46 → 0` at two season boundaries. And the player remembers that an army that runs out of money, but not supplies, loses morale and sees its regiments desert, mercenaries first.

**Answer: the bill is split by unit kind, and only one kind can go unpaid.**

- **Regular units, city units (garrisons) and ships are paid from the national treasury**, with no balance check. The treasury simply goes negative **[confirmed: 27 of 80 nation-quarters exact with no adjustment, and the human nation in all 6 quarter pairs]**.
- **Mercenary units are paid from their own army's purse** (`ArmyRecord +12`): `(troops div 200) × price × quality div 5` per unit. They are never paid from the treasury, and the tick never refills the purse **[confirmed: 32 of 39 army-quarters exact; 6 of the other 7 exact once events in the round are counted]**.
- **If a mercenary unit comes up for payment while the purse is at 0 or below, the whole unit leaves.** It takes `troops div 100` tons of the army's supplies with it. Morale does not change, and there is no news message. **Regular units never leave for lack of pay**, however deep the debt **[confirmed: one desertion in the saves, exact down to the slot order; Roman regulars intact through two quarters of debt]**.
- **The last payment can overdraw the purse, and the overdraft is forgiven.** The purse is floored at 0 after each army **[confirmed: the Thracian 46 → 0]**.
- **Debt costs the leader his job, not the army its troops.** An AI nation below the debt line has a 1 in 9 chance each quarter of deposing its leader ("*X depose their leader Y.*"). This resets its treasury to 0 **[confirmed: 2 of 15 at-risk nation-quarters, 0 outside the condition]**. A human below the same line loses the game at the start of their next turn: "*Your army have deposed you because they have not been paid.*" **[derived]**
- **Order:** upkeep is billed first, before the tax-base rebuild and the income credit. No payment decision reads the treasury, so the order only matters for the debt test. That test sees the treasury after both upkeep and this quarter's income.

`FUN_0044ac3c` is not a "degrade" state. It is the generic **remove-unit** helper. The `troops / 100` the old report read as a troop loss is taken from **supplies** (`+10`), not troops.

Line numbers are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`. The instruction listing is new: `upkeep_listing.txt`, in the same folder. Helpers: `FUN_00448FD0(a,b) = min`, `FUN_00448FD8(a,b) = max`, `FUN_0040284C(n) = Random(n)`.

## The billing, exactly [derived]

`FUN_00451b40`, the quarterly tick, opens with three loops (`54726–54800`). Nation `n`'s treasury is the signed 32-bit word at `0x474670 + n × 0x494 + 0x438`. `price[type]` is the quarterly price word at `+0x24` of the DAT unit-type table ([`unit-type-stat-table-in-dat.md`](unit-type-stat-table-in-dat.md)): light infantry 1, heavy infantry 2, archers 1, light cavalry 3, heavy cavalry 4.

```text
// 1. Ships (54726–54740)
for each fleet f:
    if f.owner (+8) >= 0 and f[+10] == -1:              // launched; a fleet under construction holds its city here
        treasury[f.owner] -= f.ships (+18) × 3

// 2. Armies (54741–54782), in army-index order
for each army a with a.owner (+4) >= 0:                 // includes armies aboard a fleet
    for k = 0 … 19:                                      // slot k at a + 16 + 32k
        s = a.slot[k]
        if s.troops (+4) <= 0: continue
        cost = int16((s.troops div 200) × price[s.type (+2)])     // 16-bit IMUL
        if s.marker (+0) == 0:                                    // regular
            treasury[a.owner] -= cost
        else:                                                     // mercenary
            pay = int16((cost × s.quality (+6)) div 5)
            if a.money (+12) <= 0:
                a.supplies (+10) -= s.troops div 100
                removeUnit(a, k)                                  // FUN_0044ac3c
            else:
                a.money -= pay
    a.money    = max(0, a.money)
    a.supplies = max(0, a.supplies)

// 3. City units (54783–54800), all 16 nations
for each nation n, for each of its 40 city-unit slots u (n + 0x2e4 + 8i):
    if u.troops (+4) > 0:
        treasury[n] -= (u.troops div 200) × price[u.type (+2)]   // 32-bit; the +0 and +6 words are not read
```

The test is `CMP word ptr [ESI+0x8],0` / `JLE` at `00451c1c`, so a purse of exactly 0 fails. The decompiler writes it as `< 1`. Division truncates (`CDQ`/`IDIV`). The army-loop cost is a 16-bit product, while the city-unit cost is 32-bit, but no real slot comes close to overflowing either one.

### Per-unit amounts

| Unit | Formula | Examples |
| --- | --- | --- |
| Regular, army or city unit | `(troops div 200) × price` | 15,000 light infantry → **75**; 6,000 heavy infantry → **60**; 2,500 heavy cavalry → **48** |
| Mercenary | `((troops div 200) × price × quality) div 5` | Gallic 6,438 light infantry, quality 8 → `32 × 8 div 5` = **51** (the "51 quarterly" hire); Bactrian 4,200 light infantry, quality 6 → **25**; Thessalian 1,400 light cavalry, quality 7 → **29** |
| Ship | `3 × ships` | 90 ships → **270**; 70 → **210** |

At quality 5 a mercenary costs exactly its regular rate. At quality 9 it costs 1.8 times as much. This is the same split `TInformation_ShowArmyDetails` prints as "regular cost" and "mercenary pay" ([`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md)). The panel's two lines are also the two different payers.

## Where the money comes from

| Charge | Paid from | Balance checked? | If short |
| --- | --- | --- | --- |
| Regular army units | owner's treasury | no | treasury goes negative |
| City units (40 slots per nation, "not ready" ones included) | treasury | no | treasury goes negative |
| Launched fleets | treasury | no | treasury goes negative |
| Fleets under construction | — | — | nothing charged |
| Mercenary units | **that army's purse** | yes, before each unit: `purse ≤ 0`? | the unit deserts |

**There is no "purse first, then treasury" fallback.** A rich treasury does not stop a mercenary from leaving. Carthage had 11,000 talents when its Moor unit walked out (below).

The tick never credits a purse. A purse is refilled only outside the tick: by the player's money control in the supply dialog (`TAFSupply_ChangeMoney`) or the army-to-army dialog, and by the automatic resupply `FUN_0044F6D8`. When an army's move ends against one of its own cities, and its purse is under 500 while the treasury is positive, that function moves 500 from the treasury ([`supply-capacity-rounding.md`](supply-capacity-rounding.md)). AI armies do this constantly, which is why they seldom run dry.

## What happens when a mercenary can't be paid

### `FUN_0044ac3c` is "remove unit k from army a" [derived]

`FUN_0044ac3c` (`49430`, listing `0044ac3c–0044acb3`):

```text
last = highest slot index with troops > 0             // FUN_0044a66c(a) − 1
a.slot[k] = a.slot[last]                              // 32-byte copy (REP MOVSD, 8 dwords)
a.slot[last].troops = 0                               // marker, type and name words stay behind
if a.slot[0].troops == 0:  FUN_0044ab90(a)            // army deleted: owner = −1, map cell restored
else:                      FUN_0044a80c(a)            // map marker redrawn (size band)
```

It has seven call sites, and none of them is a "degrade" state. They are this desertion; post-battle and siege attrition (`FUN_0044ae20`, which drops regulars under a tenth of standard battalion size and mercenaries under a fifth); fleet losses (`FUN_0044b4f8`); the AI over-capacity trim (`FUN_0044f8fc`); unit transfer (`FUN_0044acb4`); and the AI's per-turn consolidation (`FUN_00450858`, twice). That consolidation merges small same-type regulars and dismisses mercenaries under a sixth of standard size. The zeroed-troops slot with its old name still in place explains the "slot with zero troops can still retain a name" in [`army-records-and-roman-roster.md`](army-records-and-roman-roster.md).

### Which units leave, and in what order [derived, confirmed once]

- **Mercenary slots only, in slot order 0 → 19.** A mercenary leaves if the purse is already at 0 or below when the loop reaches it. The one that drives the purse negative still gets paid; the overdraft is written off at the end.
- **The army's last unit fills each hole, and the loop does not go back for it.** A mercenary moved into an already-visited slot escapes both payment and desertion this quarter. A regular moved there skips its upkeep, so the treasury is charged less.
- **So an unpaid all-mercenary army of `n` units loses `⌈n/2⌉` of them per quarter**, and the last one deletes the army. Which mercenaries go depends on slot positions, not on cost, type or quality.
- **Whole units, not troop fractions.** The `troops div 100` is subtracted from supplies. It equals the deserting unit's share of the army's supply capacity (`troops div 100`, [`supply-capacity-rounding.md`](supply-capacity-rounding.md)), so the mercenaries leave with their rations.

### No morale write, and no message [derived, confirmed once]

`FUN_00451b40` never touches `ArmyRecord +14`. The morale writers are the nine listed in [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md) plus the tick's supply rule, and none is on this path. Neither the billing, `FUN_0044ac3c`, `FUN_0044ab90` nor `FUN_0044a80c` calls the news writer `FUN_00449240`.

**There is an indirect route to morale, through supply [derived].** Write the stock as a fraction `p` of capacity and the deserters as a fraction `f` of the army's troops. After they leave, the fraction is `(p − f) / (1 − f)`. At full stock nothing changes. Below full, the percentage falls, and it can fall under 10 %, where the next turn's tick starts taking 2 morale and 1 move per turn. For example, an army at 30 % that loses a fifth of its troops to desertion drops to 12 %. If it loses a quarter, it drops to 7 %. The morale effect shows one turn after the quarter, because the supply-and-morale loop runs before `FUN_00451b40` in the same tick.

## What happens when the treasury can't pay: deposition [derived, AI side confirmed]

Regulars, city units and ships are billed whatever the balance. The only consequence of debt is a leadership test. It uses the same line for both sides:

```text
inDebt = treasury < −(wealth div 500)  or  treasury < −20000  or  unity < 400
```

Wealth (`+0x430`) is `Σ population × 3000`, so the debt line is `6 × total population`, capped at 20,000.

- **AI**, in `FUN_00451b40`'s nation loop, after the income credit and the unity update (`54891–54901`): if `Random(9) == 0` and `inDebt`, it calls `FUN_0044c8f0(n)`.
- **Human**, in `FUN_00452034` (`55032`), which runs at the start of every human nation's turn, not only at quarters: if `inDebt`, it calls `FUN_0044c8f0(n)` deterministically. The same test also covers the end of the game at 250 BC and a win at 334 cities.

`FUN_0044c8f0` (`50761`):

```text
if nation is AI:  news("<nation> depose their leader <old leader>.")
else:             TPremierForm_HumanLeaderFalls           // THumanFalls dialog, then the nation turns AI (FUN_00449078)
leader  = a different random name from the nation's 12-name table
unity   = max(unity, min(550, unity + 150))
treasury = (treasury < 0) ? 0 : treasury + 1000
relations −5 … −1 with any nation → 0
```

The human dialog (`THumanFalls_InitializeForm`, `56394–56403`) picks its reason from the state. If the nation was not conquered and it is not 250 BC, it reads "*Your unpopularity has forced the army to overthrow you.*" when unity is below 400, and "*Your army have deposed you because they have not been paid.*" otherwise. So that message is the treasury condition.

## Order within the quarter [derived]

[`city-population-growth.md`](city-population-growth.md) gives `FUN_00451b40`'s step order. Step 1, "ship upkeep, army and garrison upkeep", expands to:

1. **a** ships → treasury; **b** armies: regulars → treasury, mercenaries → purse or desertion; **c** city units → treasury.
2. Wealth and tax base zeroed.
3. City loop: growth, rebuild, loyalty, rebellion.
4. Nation loop: mobilization −3; the treasury credit; the trade term `FUN_004499ec`; unity; **the AI debt test**.
5. Relation thaw.

**What an implementation needs from this:**

- **A mercenary's ability to pay is the army purse at the tick, with no income in it.** Nothing credits a purse in the tick.
- **Regular, city-unit and ship upkeep need no ability-to-pay test at all.**
- **The debt test sees the treasury after upkeep and after this quarter's income.** For the AI it runs in the same tick. For a human it runs at the start of their next turn, after the rest of the round.

### The trade term, `FUN_004499ec`, solved [confirmed]

The last income term, left undecompiled by [`decompiled-quarterly-billing-and-economy.md`](decompiled-quarterly-billing-and-economy.md), is trade:

```text
FUN_004499ec(n) = Σ over nations j with relation[n][j] (+0x26 + 2j) ∈ {1 trade, 2 alliance} of taxBase[j] div 12
```

It reads the partners' tax bases as just rebuilt in step 3. The complete quarterly treasury change is therefore:

```text
Δtreasury = −3 × launched ships − Σ regular army units − Σ city units
            + taxBase × taxRate div 100 + taxBase div 4 − cities × 7 − wealth div 20000
            + Σ trade/alliance partners' taxBase div 12
```

## Fleets [derived, confirmed]

- **Ship upkeep is `3 × ships`, from the treasury**, for every fleet with an owner and `+10 == −1`. A fleet under construction (`+10` = its city) pays nothing.
- **The fleet purse (`+16`) is never read or written by the tick.** Nothing happens to a fleet whose nation cannot pay: it loses no ships and no condition. The only consequence is the nation-level debt test. The purse is spent only on supply purchases on the foreign path and on transfers. Even repairs bill the treasury.
- Saves: all **10 of 10** launched fleets kept their purse across the tick. The starving Carthaginian fleet kept its 1,000 while its 270 was billed to Carthage's treasury (exact, below). Rome's 10-ship order at Caere was not charged: Rome's `autumn_11 → winter_1` treasury is exact with 0 ships.

## Checked against saves

The saves were read directly: armies at `100,958` (656 bytes), fleets after them (26 bytes), and nations at `SharedPrefixLength + 2 + armies × 656 + 2 + fleets × 26` (1,172 bytes). The news ring buffer follows the 600-byte mercenary table. The 55-byte trailer ends at the file's end, which checked on all 54 saves. The pairs are the six quarter pairs of [`city-population-growth.md`](city-population-growth.md): five one-turn pairs, plus `1_rome_270_summer_7 → autumn_1` over three turns.

### Mercenary pay comes out of the purse: 39 army-quarters

Every army that exists on both sides of a tick, matched by owner and unit roster:

| Outcome | Army-quarters |
| --- | ---: |
| Holds mercenaries; purse exactly as predicted | **32** |
| Purse exactly **+500** over the prediction: the automatic top-up from the treasury (`FUN_0044F6D8`) in the round | 4 |
| The Carthaginian army besieging Castulo, in two pairs: it lost troops in the round before the tick, and is exact with the post-round troop counts | 2 |
| Bithynian army moved and resupplied in the round (20 talents lower than predicted, not traced) | 1 |
| All-regular army; purse unchanged | 12 of 12 |

The Thracian army from the 47th report, `1_thracia_271_*`, army 6, 7 units, 5 regular and 2 mercenary:

| Tick | Purse before | Bactrian (slot 2), pay 25 | Thessalian (slot 5), pay 29 | Floored | Saved | Units |
| --- | ---: | --- | --- | ---: | ---: | --- |
| `spring_11 → summer_1` | 100 | 100 > 0: paid → 75 | 75 > 0: paid → 46 | 46 | **46** | 7, identical |
| `summer_11 → autumn_1` | 46 | 46 > 0: paid → 21 | 21 > 0: paid → **−8** | **0** | **0** | 7, identical |

The second tick is the overdraft rule. A "can this unit be afforded?" test would have dismissed the Thessalian (29 > 21). The code only asks whether the purse is still positive, and the save keeps all seven units. Thracia's treasury matches exactly **without** the 54 talents in both quarters. It pays the regulars' 103 and the city units' 86.

### The one desertion: a Carthaginian army, `1_cartago_271_spring_11 → summer_1`

The human Carthaginian army at `(93, 79)`, purse 100, supply 0, treasury **11,000**:

| Slot | Before | Loop | After (`summer_1`) |
| ---: | --- | --- | --- |
| 0 | Greek, light inf, 4,800, merc (pay 33) | 100 > 0: paid → 67 | Greek |
| 1 | 2nd Guards, heavy inf, 2,300 | regular → treasury | 2nd Guards |
| 2 | Greek, heavy inf, 5,700, merc (pay 78) | 67 > 0: paid → **−11** | Greek |
| 3 | Moor, archers, 2,700, merc (pay 15) | −11 ≤ 0: **deserts**; slot 5 moves in | **Numidian** |
| 4 | 2nd Dragoons, heavy cav, 1,100 | regular → treasury | 2nd Dragoons |
| 5 | Numidian, heavy cav, 2,000, merc (pay 56) | moved to slot 3, **not visited** | — |

The save matches in every detail. The Moor unit is gone, troops fall 18,600 → 15,900, and the purse ends at 0. The Numidian unit sits in **slot 3**, not slot 5, which shows it was swapped in rather than shifted along. And the Numidian **survived**, although the purse was negative: moved into a visited slot, it was never asked. A rule of "every unpaid mercenary leaves" predicts two desertions; the code predicts one, and the save has one.

Also in this pair:

- **Morale** went 61 → 59, exactly the supply rule at 0 % (−2), and it kept falling 2 per turn to 51 by `summer_9`. There was no extra penalty.
- **The news log** gained three lines: the week header, "Macedonia declares war on Illyria.", and "Verona (Gaul) falls to Rome." Nothing about the Moors.
- **The treasury** matches exactly: 11,000 → 13,828. It includes the 270 ship upkeep and excludes the army's 182 mercenary pay.

No other army in the data reached a quarter with mercenaries and an empty purse, except a Gaul army that Rome destroyed in the same round (`7 → 8`).

### Regulars under debt: Rome, two quarters

Human Rome carries a negative treasury through 30 saves, between −75 and −904, against a debt line near −5,000 to −5,900. Across `1_rome_270_autumn_11 → winter_1` (−783 → −904) its two armies, 24 regular units and 123,231 troops, are **unit-for-unit identical**. Its 7,000 city-unit troops are unchanged too, and morale moved only by the supply rule (70 → 70, 64 → 65). Across `summer_7 → autumn_1` (−644 → −759), the 13-unit army and 85,000 city-unit troops are likewise identical. The upkeep was unpayable on any reading, and nothing left.

### The treasury formula: 27 of 80 exact, and the human nation 6 of 6

Over the five one-turn pairs, the complete formula above is exact for **27 of 80** living nation-quarters with no adjustment. The rest are AIs that acted in the round (recruiting, 500-talent purse top-ups, captures, reparations, a deposition). The exact 27 pin every term:

- **16** would break if their mercenary pay were charged to the treasury.
- **All 27** need the city-unit term.
- **26** need the trade term `FUN_004499ec`.
- **4** need the ship term.

The human nation, whose round is known from the notes, is exact in all six pairs:

| Pair | Nation | Adjustment |
| --- | --- | --- |
| `thracia spring_11 → summer_1` | Thracia | none (409) |
| `thracia summer_11 → autumn_1` | Thracia | none (298) |
| `cartago spring_11 → summer_1` | Carthage | none (13,828) |
| `7 → 8` | Rome | Rome's battle, in its own turn before the tick, cut army 0's regular upkeep from 513 to 393. Using those troop counts: −237 ✓ |
| `rome autumn_11 → winter_1` | Rome | Armenia's trade with Rome ended in the round (relation 1 → −5). Without its 36: −904 ✓ |
| `rome summer_7 → autumn_1` (3 turns) | Rome | Tax 20, as the player set it in the round: −759 ✓ |

This also settles [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md)'s open "exact whole-turn check of the quarterly treasury credit", without a controlled save.

### Deposition: 2 of 15

Among AI nation-quarters in the six pairs, **15** were in debt by the rule above, and **2** deposed their leader. That is 13 %, against 1 in 9 expected. No nation outside the condition did.

| Pair | Nation | Treasury after income | Debt line | Leader | Treasury saved | Unity saved |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| `7 → 8` | Galatia | −1,705 | −1,422 | Gunthemunde → Thrasamunde | 20 (0, then +20 in the round) | 698 (`max(698, 550)`) ✓ |
| `thracia summer_11 → autumn_1` | Gaul | −5,030 | −2,658 | Ariovistus → Gundebald | **0** ✓ | **550** (`min(550, 470 + 150)`) ✓ |

Both news logs carry the literal line, "*Galatia depose their leader Gunthemunde.*" and "*Gaul depose their leader Ariovistus.*". Each sits just before the new week header, where the quarterly tick writes it.

## The recollection, tested

| Recollection | Verdict |
| --- | --- |
| An army that runs out of money loses morale | **Not directly** [confirmed, 1 case]. Non-payment writes no morale. It can cut morale **indirectly**: deserters take their share of supplies, and an army pushed under 10 % supply then loses 2 a turn [derived]. Many broke armies are also out of supplies, like both human armies above, and lose morale for that reason. |
| …but not supplies | "Money" has to mean the army's own purse, the one on its information panel. The treasury does not count, rich or poor. |
| Its regiments desert | **Holds**, for mercenaries: whole units, with their rations, and no message [confirmed, 1 case]. |
| Mercenaries first, then regulars | **Wrong.** Mercenaries only. Regular regiments never desert for lack of pay [confirmed: Rome]. The penalty for unpaid regulars falls on the leader: deposition. |

## Corrections to existing reports

- [`decompiled-quarterly-billing-and-economy.md`](decompiled-quarterly-billing-and-economy.md):
  - Mercenary units are billed `× quality div 5` to their army's **purse**, not to the treasury.
  - The non-payment test is the **army purse** (`≤ 0`), applied to mercenary slots only.
  - `troops / 100` is taken from the army's **supplies**, and `FUN_0044ac3c` **removes the unit**. It is not a partial troop loss, and not a "degrade" state.
  - The AI stability check is a **leader deposition** with an exact debt rule.
  - The "undecompiled" income term is trade and alliance income.
- [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md): the whole-turn treasury check is done (above), including `FUN_004499ec`.
- [`city-population-growth.md`](city-population-growth.md): step 1 expands as above.
- [`roadmap.md`](../roadmap.md) and [`decompilation-plan.md`](../decompilation-plan.md) repeat "a mutiny/disband consequence for unpaid armies".

## What an implementation needs

- **Treasury, every quarter, no check:**
  - `Σ (troops div 200) × price` over regular army units and all city-unit slots;
  - `3 × ships` over launched fleets.
- **Purse, per mercenary slot, in slot order:**
  - if `purse ≤ 0`, the unit leaves, taking `troops div 100` supplies with it;
  - otherwise the purse pays `(troops div 200) × price × quality div 5`, and may go negative.
  - Fill the hole with the army's last unit and do not revisit it. Floor purse and supplies at 0 after the army. Delete the army if it empties.
- **No morale change, no message, no regular-unit loss.**
- **Debt:** `treasury < −(wealth div 500)`, or `< −20000`, or unity `< 400`.
  - AI: a 1-in-9 deposition check each quarter, after income.
  - Human: a game-over check at the start of each of their turns.
- **Trade income:** `Σ partner taxBase div 12` for relations 1 and 2.

## Still open

- **The supply deduction on desertion** is read from code only. Both save cases had 0 supplies, so the `− troops div 100` was floored away.
- **An army emptied by desertion** being deleted, and the resulting indirect morale effect, are both code-only.
- **The human debt game-over** is code-only. Rome's deepest debt in the data, −904, is far above its −5,856 line. **User testimony (2026-09-14):** the user has played long stretches with a negative treasury without being deposed, and some nations start the game with a negative treasury. Both fit the rule, because "in debt" here does not mean "treasury below 0". It means below `−(wealth div 500)`, which is about 6 talents per 1,000 population and capped at 20,000, or unity below 400. A human deposition would contradict the rule only if it happened, or failed to happen, when the treasury was below that line or unity was under 400.
- **The deposition's relation reset** (−5 … −1 → 0) is not observed: neither deposed nation had such a relation.
- `TAFSupply_ChangeMoney` has no treasury sign check in code. Whether the dialog lets a human fund a purse from a negative treasury is untested.

## Controlled-save recipe

**Recipe 1 — desertion, the slot swap, and a 5-talent treasury check.** Start from `1_rome_270_winter_11.sav`. It is Rome's turn at Winter week 11, so the next end of turn runs the quarter tick. Army 0 at `(92, 27)` holds one mercenary, the Gallic light infantry in slot 3 (5,895 troops, quality 9, pay **52**), with purse **156** and supply 0. Army 13 stands next to it at `(93, 28)`.

1. **Control.** Load the save, give no orders, and end turn until Rome's next turn (Spring week 1, 269 BC). Save `1_rome_269_spring_1_pay.sav`.
2. **Unpaid.** Reload `winter_11`. Open the army-to-army dialog between armies 0 and 13 and move **all** of army 0's money to army 13, so that army 0 reads 0 and army 13 reads 256. Press OK, give no other orders, and end turn as before. Save `1_rome_269_spring_1_nopay.sav`.

| | `_pay` | `_nopay` |
| --- | --- | --- |
| Army 0 purse | 104 | 0 |
| Gallic unit | stays | **gone**; slot 3 holds the **2nd Foot Battalion** (from slot 8) |
| Army 0 units / troops | 9 / 37,081 | 8 / 31,186 |
| Army 0 morale | 62 | 62 (supply rule only) |
| News line about it | — | none |
| Rome's treasury | T | **T + 5**: the 2nd Foot Battalion (1,120 troops) is skipped after its move |

Replayed turns are deterministic for the AI ([`battle-replayed-rout-mechanic-and-combat-constants.md`](battle-replayed-rout-mechanic-and-combat-constants.md)), so the two runs should differ only by the desertion. If an AI capture, trade change or reparation involving Rome shows up in only one run's news log, the `+ 5` comparison fails. Note which one.

**Recipe 2 (optional) — the supply cut and the morale knock-on.** Use any week 11 outside Winter, with a human army that holds a mercenary unit and stands next to one of its own cities that has stock. In the supply dialog, set its supplies to about half of capacity, empty its purse, and end turn. Save at week 1 and again at week 3, and repeat with the purse kept as the control. The prediction at week 1 is supplies = `S − ((90 − season) × troops) div 20000 − Σ deserters' troops div 100`. From week 3 the morale should follow [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md)'s rule on the new percentage. Send the week-11 save first, and exact numbers can be worked out before the turn is ended.

## Reproduction

- **Billing:** `FUN_00451b40`, `54726–54800` (listing `00451b40–00451cd2`). The nation loop and AI debt test are at `54864–54905`.
- **Remove unit:** `FUN_0044ac3c` `49430`, `FUN_0044a66c` `49019`, `FUN_0044ab90` `49372`, `FUN_0044a80c` `49141`. The other call sites were found with `FindXrefs.java 0x0044ac3c`.
- **Debt:**
  - `FUN_0044c8f0` `50761`;
  - `FUN_00452034` `54960` (test at `55032`);
  - `THumanFalls_InitializeForm` `56353`;
  - `FUN_00449078` (turns the nation AI);
  - `FindXrefs.java 0x0044c8f0` and `0x0045c238` list every caller.
- **Trade:** `FUN_004499ec` `48415`.
- **Listing:** `analyzeHeadless <ReTools>\ghidra_projects IC2 -process "Imperial Conquest 2.exe" -noanalysis -readOnly -scriptPath <ReTools>\scripts -postScript DumpListing.java upkeep_listing.txt 0x00451b40 0x0044ac3c 0x0044c8f0`.
- **Save checks:** a direct Python reader over the local saves using the offsets above. Nothing was written to either repository.
