# City population growth: quarterly only, and the "weekly growth" is city supply production

The question: what is the exact arithmetic of city population growth? [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md) established that population grows each quarter toward its maximum, reduced by the tax rate and by mobilization, but gave no formula. [`decompiled-turn-and-calendar-sequencing.md`](decompiled-turn-and-calendar-sequencing.md) separately described a *weekly*, seasonal, loyalty-modulated growth with a Winter decline chance. Are they one mechanism or two?

**Answer: two mechanisms, and only one of them is population.**

- **Population (`+0x1c`) grows only in the quarterly tick `FUN_00451b40`**, by a deterministic step: about a quarter of the gap to the maximum, plus one, reduced by the tax rate and by mobilization. It uses no random draw **[confirmed: 6 save pairs, 2,004 city-quarters, 0 mismatches]**.
- **The weekly loop in `FUN_004514ec` does not touch population.** It writes the city's **supply stock** (`+0x18`, `CityRecord.Supplies`), which grows with population and season, is reduced by the owner's **mobilization** (not loyalty), and is capped at `population × 10`. Its "Winter decline" costs **1 point of loyalty**, not population, and only when the stock is empty **[confirmed: 33 save pairs, 10,693 of 10,980 city-turns exact]**.
- **There is no separate growth-rate table.** `DAT_004794a8` is the value word of the season records `DAT_004794a0` (Spring 50, Summer 80, Autumn 80, Winter 20), already located in the DAT at `0x1F7D8` by [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md). The same four values drive army supply consumption and city supply production.

All line numbers are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`. Helpers, read to be sure: `FUN_00448FD0(a,b) = min`, `FUN_00448FD8(a,b) = max`, and `FUN_0040284C(n)` is Delphi `Random(n)`, which returns `0 … n−1` from the seed at `DAT_0045E030` (`seed = seed × 0x08088405 + 1; return (n × seed) >> 32`).

## Every writer of city population [derived]

An exhaustive search of the dump for both indexed writes (`DAT_004795AC`) and walking-pointer writes (`+ 0x1c) =`) finds three writers, plus the file loaders:

| Writer | Effect on population `+0x1c` | Also |
| --- | --- | --- |
| `FUN_00451b40`, quarterly (`54812–54830`) | the growth step below | — |
| `FUN_0044b27c`, every siege attempt (`49803–49808`) | `FUN_0044b230` damage, then floored at `maxPop / 6 + 1` | the same damage applies to loyalty and fortification |
| capital relocation (`50293`, `50588`) | `+10` | maximum population `+20`, tribute `+25`, loyalty and fortification `+8`/`+10` capped at 99 |

So between quarter ticks, a city's population changes only through a siege or by becoming the new capital. This is why earlier reports saw population "frozen for several turns, then jumping": the jumps land on season boundaries.

## The quarterly step, exactly [confirmed]

`FUN_00451b40`'s city loop (`54810–54862`) visits the 334 cities in index order. For each city (`owner = city+0x12`, nation fields read from `nation[owner]`):

```text
if pop (+0x1c) < maxPop (+0x1e) and not FUN_004497cc(city):     // no hostile army adjacent
    d   = (maxPop − pop) >> 2                                     // gap / 4, truncated
    d   = d − (d × taxRate (+0x44a)) / 120                        // 0x78
    pop = pop + (d − (d × mobilized (+0x442)) / 300) + 1
    pop = min(pop, maxPop)

wealth  (+0x430) += pop × 3000                                    // reads the grown population
taxBase (+0x44c) += (tribute × pop / maxPop) << 2                 // likewise

if taxRate < 11 and loyalty (+0x16) < 80:  loyalty += Random(4)   // 0..3
if Random(3) == 0:                          loyalty −= Random(taxRate) / 8
if loyalty < 30 and the city is no nation's capital:  FUN_0044c204(city)   // rebellion
```

Arithmetic is 32-bit signed with truncating division, and every stored value is 16-bit. As a closed form:

```text
growth = d' − ⌊d' × mob / 300⌋ + 1,   d' = d − ⌊d × tax / 120⌋,   d = ⌊gap / 4⌋,   gap = maxPop − pop
```

**Properties that follow from the code:**

- **Growth is at least 1 and at most the gap** for any tax ≤ 120 and mobilization ≤ 300: `d' ≥ 0` and `d' × mob / 300 ≤ d'`, and `d + 1 ≤ gap` for every `gap ≥ 1`. The final `min(pop, maxPop)` is a safety cap that never binds for legal values (mobilization is capped at 100 by `TArmyRecruits_RecruitUnit`). So a city below its maximum always grows by at least one population unit per quarter unless an enemy army is adjacent. A city at or above its maximum never changes here.
- **With no tax and no mobilization**, growth by gap is: 1–3 → +1, 4–7 → +2, 8–11 → +3, and so on. That is roughly 25% of the remaining gap, plus one: a geometric approach to the maximum.
- **Tax and mobilization reduce growth only in steps.** The tax term needs `d × tax ≥ 120` to take anything off, and the mobilization term needs `d' × mob ≥ 300`. Most real cities are within 10 of their maximum (`d ≤ 2`), so for them neither term changes the result at all.
- **No randomness in the growth itself.** The loop's four `Random` draws (listed above, plus whatever `FUN_0044c204` draws) all come after the growth and touch only loyalty and rebellion. Growth is exactly reproducible from the pre-tick state.

**Fields read.** Population `+0x1c` and maximum `+0x1e`; the owner's tax rate `+0x44a` and mobilization `+0x442`; and, through `FUN_004497cc`, the map and the relation matrix. Nothing else: no loyalty, no season, no unity, no tribute.

**`FUN_004497cc(city)` is the "hostile army adjacent" test** (`48256–48296`). For each of the 9 cells centred on the city (`city+0xe`, `+0x10`) holding an army marker (`200 ≤ code < 248`), it takes the first live army standing there (`FUN_00449920`, `48337`). If that army's owner is at war (relation `3`, nation `+0x26` row) with the city's owner, the city counts as threatened. A threatened city does not grow this quarter.

**Order within `FUN_00451b40`** [derived, and the two marked parts confirmed]:

1. Ship upkeep, army and garrison upkeep (see [`decompiled-quarterly-billing-and-economy.md`](decompiled-quarterly-billing-and-economy.md)). **(Corrected 2026-09-14:** ships, regular army units and city units are billed to the treasury with no check. Mercenary units are billed to their army's purse, and desert when it is empty. See [`upkeep-payment-and-desertion.md`](upkeep-payment-and-desertion.md). The `FUN_004499ec` in step 4 is trade and alliance income.**)**
2. Every nation's wealth `+0x430` and tax base `+0x44c` are zeroed.
3. The city loop above. Growth comes first, so **the tax-base and wealth rebuild use the grown population [confirmed, below]**. It reads the tax rate and the mobilization **before** this quarter's mobilization decay in step 4.
4. The nation loop (`54864–54905`), for every nation with unity > 0:
   - mobilization −3 (floored at 0) **[confirmed, below]**;
   - the treasury credit, which reads the tax base and wealth **just rebuilt in step 3**;
   - `FUN_004499ec`;
   - the unity update;
   - the AI stability check.
5. The relation thaw.

So the treasury credit this quarter uses the tax base computed from this quarter's grown populations, not the stored value from before the tick. That settles T35's "before or after the rebuild" question: after.

`FUN_00451b40` itself runs from `FUN_004514ec` (`54666`) once per season. It runs after that tick's city, army and fleet loops and the weather step, and after the week counter wraps to 1, but before the season counter advances.

### Worked examples

- **Sala (Carthage), `1_thracia_271_spring_11 → summer_1`:** pop 60 of 70, tax 5, mob 15. `d = 10 >> 2 = 2`; `2 × 5 / 120 = 0`; `2 × 15 / 300 = 0`. Growth `2 + 1 = 3` → **63**, as saved.
- **Laranda (Galatia), `1_rome_270_autumn_11 → winter_1`:** pop 56 of 72, tax 40, mob 100. `d = 16 >> 2 = 4`. The tax term is `4 × 40 / 120 = 1`, so `d' = 3`. The mob term is `3 × 100 / 300 = 1`. Growth `3 − 1 + 1 = 3` → **59**, as saved. This is the only city in the data where both reductions bite, and removing either one predicts 60.

## The weekly step is city supply production [confirmed]

The first loop of `FUN_004514ec` (`54443–54492`) runs once per round (one save, one turn, two weeks), before the army and fleet loops, over all 334 cities:

```text
v   = seasonValue[season]                     // DAT_004794a8 + season × 10: 50, 80, 80, 20
s   = (pop × (v − 40)) / 10                   // Spring +pop, Summer/Autumn +4·pop, Winter −2·pop
inc = s − (s × mobilized (+0x442)) / 200      // mobilization shrinks gains and losses alike
if FUN_004497cc(city): inc = min(inc, 0)      // a threatened city cannot gain
supplies (+0x18) = max(0, min(supplies + inc, pop × 10))

if supplies == 0 and season == Winter and Random(3) == 0:
    loyalty (+0x16) −= 1                      // famine unrest; the loop's only Random draw

if fortification (+0x1a) > 100:               // a fortify order in progress, points × 100 + current
    if not FUN_004497cc(city): fort += min(10, fort / 100);  fort −= min(1000, (fort / 100) × 100)
    else:                      fort = fort % 100            // cancelled by a hostile army
```

Per turn, at mobilization 0:

| Season | `v − 40` | Supply change per turn | A city of pop 50 |
| --- | ---: | --- | ---: |
| Spring | +10 | `+pop` | +50 t |
| Summer | +40 | `+4 × pop` | +200 t |
| Autumn | +40 | `+4 × pop` | +200 t |
| Winter | −20 | `−2 × pop` | −100 t |

At mobilization 100 every figure is halved, gains and Winter losses alike. The ceiling `pop × 10` is where most cities sit for most of the year. For example, Rome's capital (pop 181) holds exactly 1,810 in several saves.

The previous reading, "reduced proportionally to that nation's **loyalty**", was the wrong nation field: `+0x442` is mobilization ([`ptolemaic-player-and-week9.md`](ptolemaic-player-and-week9.md), `IC2.Data`'s `MobilizedPercent`). The saves settle it. Numidia, Illyria, Dacia and Armenia at mobilization 0 lose nothing; Gaul, Celtiberia and Galatia at 97–100 lose exactly half; Rome at 30 loses 15%.

## The season table [confirmed]

`&DAT_004794a0 + season × 10` is the season **name** printed in the tick's `"Week N  <season>  YYY BC"` line (`54684`). `&DAT_004794a8 + season × 10` is the **value** word 8 bytes into the same record. They are one 10-byte struct, `{char name[8]; short value}`, and [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md) already found it in the DAT at `0x1F7D8`:

```text
0x1F7D8:  "Spring\0\0" 50   "Summer\0\0" 80   "Autumn\0\0" 80   "Winter\0\0" 20
```

It is used three times in the tick: army supply consumption `((90 − v) × troops) / 20000`, city supply production `pop × (v − 40) / 10`, and the date line. There is no separate growth-rate table, and population growth does not read the season at all.

## Checked against saves

The saves were read directly: cities at byte 89,600 (334 × 34), and the nation table at `SharedPrefixLength + 2 + armies × 656 + 2 + fleets × 26` (stride 1,172). The calendar and the 16-entry turn order are in the 55-byte trailer, at `+40/+42/+44` and `+0`.

### Quarterly growth: 6 pairs, 0 mismatches

| Pair | Turns | Grew exactly as predicted | At maximum, unchanged | Threatened, did not grow | Owner changed (excluded) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `1_thracia_271_spring_11 → summer_1` | 1 | 90 | 241 | 1 | 2 |
| `1_thracia_271_summer_11 → autumn_1` | 1 | 72 | 255 | 1 | 6 |
| `1_cartago_271_spring_11 → summer_1` | 1 | 91 | 242 | 0 | 1 |
| `7.sav → 8.sav` | 1 | 94 | 239 | 1 | 0 |
| `1_rome_270_summer_7 → autumn_1` | 3 | 76 | 257 | 0 | 1 |
| `1_rome_270_autumn_11 → winter_1` | 1 | 71 | 263 | 0 | 0 |
| **Total** | | **494** | **1,497** | **3** | 10 |

Tax and mobilization were read from the first save of each pair. The three-turn pair is valid because nothing else grows population between ticks.

- **The three non-growers are the threat predicate, 3 of 3.** Castulo (Celtiberia) twice and Lissus (Illyria) were below maximum and did not grow. Each had an army of a nation at war with its owner inside the 3 × 3 block in both saves of its pair. No unthreatened city below maximum ever failed to grow.
- **The core `gap >> 2, + 1` is pinned.** The same 497 cities fit `gap / 4 + 1` in 493 cases, `gap / 3 + 1` in 366, and `gap / 5 + 1` in 398. Dropping the `+ 1` fits **1** of 497.
- **The tax and mobilization terms are pinned only once.** Because real gaps are small, they change the prediction in exactly one city, Laranda (above). There they fit, and dropping either one fails. The divisors 120 (`0x78`) and 300 are read from the code's immediate operands. The saves support them but cannot isolate them: `d × mob / 200` fits the same 494.
- **The rebuild reads the grown population.** Recomputing `Σ (tribute × pop / maxPop) << 2` and `Σ pop × 3000` from each post-tick save's own cities matches the stored tax base and wealth for 78 of 80 nation-quarters. Using the pre-tick populations instead matches 13 and 7. The two misses are captures in the round after the tick.

### Weekly supply: 33 pairs

Every one-turn pair inside a season across the five play-throughs (`1_thracia_*`, `1_cartago_*`, `1.sav`–`12_rom_a.sav`, `1_rome_270_*`, `*_b`), 11,022 city-turns:

| Outcome | City-turns |
| --- | ---: |
| Exact, using the first save's mobilization | 10,473 |
| Exact with the second save's mobilization (an AI changed it during the round, before the tick) | 220 |
| Friendly or enemy army/fleet within 2 tiles (resupply, disband, scuttle) | 172 |
| Other: supplies **below** prediction | 111 |
| Other: supplies above prediction | 3 |
| Owner changed / population changed by a siege (excluded) | 42 / 1 |

The 111 residuals below prediction fit AI armies drawing on a city's stock during the round (`53090–53156`) and then moving off before the next save. [`supply-driven-morale-and-fleet-attrition.md`](supply-driven-morale-and-fleet-attrition.md) already lists this auto-resupply as untraced.

- **Order at a quarter tick.** On the 5 one-turn quarter pairs, 1,078 city-ticks can tell the difference: all use the **pre-growth** population and the **ending** season. That confirms that the city supply loop runs before `FUN_00451b40` and before the season advances.
- **Winter famine: loyalty, 1 in 3.** In Winter pairs, cities whose stock ends the turn at 0 lost exactly 1 loyalty in **39 of 108** cases (36%; 1/3 expected) and kept it in 69. Cities with stock left, and every city outside Winter, never lose loyalty this way (1,874 and 8,980 city-turns unchanged, apart from a handful of other events). No city lost population in any within-season pair except by siege.

### Also in `FUN_00451b40`: mobilization decays, not unity [confirmed]

The nation loop's `−3` is applied to `+0x442`, mobilization, not to unity:

```text
mobilized (+0x442) = max(0, mobilized − 3)
unity (+0x440)     = min(990, max(300, unity + 25 − taxRate / 2 − mobilized / 5))   // after the decay
```

Across the 5 one-turn quarter pairs, mobilization fell by exactly 3 in **71 of 80** nation-quarters; the other 9 were AIs recruiting or disbanding in the round. Unity matched the formula exactly in **60 of 80**; the other 20 had a battle, capture or elimination in the round (±25, +9/−15, reset). So unity drifts **up** by 25 a quarter, minus half the tax rate and a fifth of the mobilization, within 300…990. It does not erode by 3.

## Corrections to existing reports

- [`decompiled-turn-and-calendar-sequencing.md`](decompiled-turn-and-calendar-sequencing.md): the weekly city loop is **supply production**, `+0x18`, not population growth. It is modulated by **mobilization** `+0x442`, not loyalty, and capped at `pop × 10`. The Winter decline is **loyalty −1**, 1 in 3, when the stock is empty. The "unextracted growth-rate table" is the season table, already extracted.
- [`decompiled-quarterly-billing-and-economy.md`](decompiled-quarterly-billing-and-economy.md): the growth formula is above. "Unity decays by 3 every quarter, clamped at 0" is **mobilization** decaying by 3. Unity is recomputed as `clamp(unity + 25 − tax/2 − mobilized/5, 300, 990)`.
- [`roadmap.md`](../roadmap.md) and [`decompilation-plan.md`](../decompilation-plan.md) repeat both readings in their summaries.

## What an implementation needs to reproduce

For an engine test on a scripted state, with `quarterlyGrowth` as above:

| Claim | Verdict |
| --- | --- |
| A city below its maximum grows | **Holds** — by at least 1 each quarter, unless a hostile army is adjacent. 494 of 494 unthreatened cases. |
| A city at its maximum doesn't grow | **Holds** — 1,497 of 1,497. |
| A higher tax rate grows it less | **Holds, non-strictly.** Growth never increases with tax, but it only decreases where `d × tax` crosses a multiple of 120. For gap 16, tax 40 → +3 but tax 0 → +4 at mob 100; for gap 8, tax 0 and tax 40 both give +3 at mob 0. A test must use a gap and tax large enough for the term to bite, e.g. pop 44 of 72 (`d = 7`): tax 17 → +8, tax 18 → +7 (mob 0). |
| Higher mobilization grows it less | **Holds, non-strictly**, the same way with 300. pop 44 of 72, tax 0: mob 42 → +8, mob 43 → +7. |
| Growth never exceeds the maximum | **Holds** — explicit cap, and never reached from below by overshoot. |

Also:

- The rebuild and the treasury credit read the **grown** population.
- The weekly supply step is a separate rule. It belongs in the per-turn city phase, reads the season *before* it advances, and does not touch population.

## Still open

- **The tax and mobilization divisors in isolation.** Code gives 120 and 300. One save city confirms both terms together. The controlled pair below pins them.
- **Who withdraws from city stocks between ticks.** The 111 residuals are one-directional, which fits the AI auto-resupply path (`53090–53156`), but it is not traced. **(Traced 2026-09-14:** the AI army pass `FUN_0044E41C` calls `FUN_0044F6D8` for every non-hostile city within 4 tiles, and the AI fleet pass calls `FUN_0044F7E4`. See [`supply-capacity-rounding.md`](supply-capacity-rounding.md).**)**
- **The fortify-order step** is read from code only; no save has an order in progress. Read literally, it applies up to 10 points per turn. But an order whose last step completes the city to **exactly 100** with fewer than 10 points pending (e.g. fortification 95, 5 points ordered: `595 → 600 → 600 − 600 = 0`) would leave fortification at **0**, not 100. That is either an original bug or a misreading. [`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md)'s next check 3 (order a fortification, save each turn until it completes) would settle it.
- **`FUN_0044c204`, the quarterly rebellion**, is one caller of `FUN_0044bed8` (the open item in [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md)). A city under 30 loyalty that is not a capital goes to its allegiance nation. If it is already the allegiance nation's, it goes instead to a nation at war whose army is within 10 tiles, or failing that to the best-scoring nation by `cities − 2 × distance to capital` among those set in a bitmask at nation `+0x46`. The bitmask is unidentified. The rebellion never changes population.

## Controlled-save recipe (extends the pending Rome recipe)

The pending recipe (Rome at week 11, no orders, `_pre`, end turn, `_post`, optionally `_pre` again with tax +5) is a good **control** for this formula but cannot isolate the tax or mobilization terms. Rome's largest gap in `1_rome_270_winter_11.sav` is 10 (`d = 2`), where tax would have to reach 60 and mobilization 150 before either term bites. For that run, the `_post` save should show every Roman city below its maximum grown as follows, unless a hostile army is adjacent:

- Mediolanum 27 → 30, Caere 28 → 30, Felsina 21 → 23, Verona 19 → 21, Brixia 17 → 19;
- Tarrentum 54 → 55, Tarquinii 25 → 26, Hadria 22 → 23, Ariminum 23 → 24.

These results are the same at tax 25 or tax 30.

Only three cities in that save could show a term: Laranda (Seleucid, 44 of 72, tax 40, mob 61), Byblos and Sidon (Ptolemaic). **Seleucid moves first in the turn order**, so its week-1 turn comes immediately after the quarterly tick, with no other nation moving in between. That makes a clean pair:

1. Load `1_rome_270_winter_9.sav`. Add a human player for **Seleucid**, the same way Ptolemaic was added for `11_ptol.sav`. End turns with no orders until **Seleucid's turn at Week 11, Winter**. Save `<n>_seleucid_270_winter_11_pre.sav`. Check that Laranda is still Seleucid's, at 44 of 72.
2. Set Seleucid's tax to **17**. End every human turn with no orders until Seleucid's next turn (**Week 1, Spring, 269 BC**). Save `<n>_seleucid_269_spring_1_tax17.sav`.
3. Reload `_pre`. Set the tax to **18**, repeat, and save `…_spring_1_tax18.sav`.
4. Optional, for mobilization: reload `_pre`, set the tax to 17, and disband Seleucid garrison recruits until mobilization reads **42 or less**. Repeat, and save `…_spring_1_mob42.sav`.

What each proves (Laranda, `d = 7`):

| Save | Prediction | Shows |
| --- | --- | --- |
| `_tax17` | 44 → **51** | `7 × 17 / 120 = 0`, and mob 61 takes `7 × 61 / 300 = 1` |
| `_tax18` | 44 → **50** | `7 × 18 / 120 = 1`: the tax divisor lies in 120…126 |
| `_mob42` | 44 → **52** | `7 × 42 / 300 = 0`: the mobilization term, isolated |

Every other city's population should be identical across the runs. Both tax values are ≥ 11, so the tick draws the same random numbers either way. If Laranda changes owner or has a hostile army adjacent at the tick, the pair shows nothing. Say so in the notes and fall back to Sidon, which is 45 at tax 0 against 44 at tax 40 if Ptolemaic is made human instead. The pair also gives the tax-base report a clean treasury comparison: the two runs' Seleucid treasuries differ only through the rate term and Laranda's contribution.

## Reproduction

- **Quarterly tick:** `FUN_00451b40`, `54695–54938` (city loop `54810–54862`).
- **Weekly tick:** `FUN_004514ec`, `54400–54692` (city loop `54443–54492`).
- **Threat predicate:** `FUN_004497cc` at `48256`.
- **Other population writers:** `FUN_0044b27c` / `FUN_0044b230` (`49744–49808`) and the capital relocation at `50280–50295` and `50575–50590`.
- **Rebellion:** `FUN_0044c204` at `50432`.
- **Save checks:** a direct Python reader over the local saves using the offsets above; nothing was written to either repository.
