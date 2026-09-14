# Where the nation tax base lives, how it is computed, and three economy fields corrected

The question: where does the original store each nation's **tax base** (`nationTaxBase`, solved to about 2,440 for Rome from its 15%/20% income figures in [`decompiled-fleet-tax-and-mercenary-formulas.md`](decompiled-fleet-tax-and-mercenary-formulas.md)), and is it stored at all, or only recomputed from cities?

**Answer [confirmed]: it is stored, and it is also derived.** It is the signed 16-bit word at nation-record **`+0x44c`** — the same offset in the SAV (whose nation record is the full 1,172-byte in-memory record) and at **`+0x41b`** in the DAT's 1,055-byte nation record, the word right after the tax rate at `+0x419`. The quarterly tick zeroes it and rebuilds it from the nation's cities, and captures adjust it in between. So a save carries the value as of the last quarterly rebuild plus any capture adjustments since; it is not a free input, but it is persisted state.

## Where it is read and written [confirmed]

In memory the 16 nation records start at `DAT_00474670`, stride `0x494` (1,172). `DAT_00474abc` is `0x474670 + 0x44c`.

**The quarterly rebuild — `FUN_00451b40`.** For every nation it sets `+0x430` and `+0x44c` to 0. Then, for every city, it credits the city's **owner** (`city+0x12`):

```text
nation[owner]+0x430 (wealth)    += city.population × 3000
nation[owner]+0x44c (tax base)  += cityContribution(city) << 2

cityContribution(city) = FUN_004498b0(city)
                       = city.tribute (+0x20) × city.population (+0x1c) / city.maxPopulation (+0x1e)
```

The city fields are the ones `IC2.Data`'s `CityRecord` already names at the same offsets: `TributeTalents` (`+32`), `PopulationThousands` (`+28`), `ReferencePopulationThousands` (`+30`). The panel function `TInformation_ShowCityDetails` (`0x0043BE5C`) prints `+0x1c × 1000` as "Population" and `+0x1c × 100 / +0x1e` as "% of maximum", which pins `+0x1c`/`+0x1e` as population and maximum population.

**Adjustments between quarters.**

| Function | Effect on `+0x44c` | Also |
| --- | --- | --- |
| `FUN_0044bb18` (ownership transfer on capture) | new owner `+= contribution << 2`, old owner `-= contribution << 2` | new owner's **treasury** `+0x438 += contribution × 4`; wealth `+0x430 ±= population × 3000`; unity `+9 / −15`; city count `±1` |
| `FUN_0044bed8` (a second ownership transfer: it rewrites `city+0x12`) | new owner `+= contribution << 2`, old owner `-= contribution << 2` | new owner's treasury `+= contribution × 6`; wealth `±= population × 3000`; city count `±1`; unity `+3`, and `−20` floored at 250 |
| `FUN_0044c528` (loops over cities) | `+= contribution << 2` for each city it credits | treasury `+= contribution × 6`; wealth `+= population × 3000`; city count `+1` |
| `FUN_0044c360` | set to 0 | resets the collapsing nation (unity 450, other fields) |

**The quarterly treasury credit — also `FUN_00451b40`**, read directly (it corrects [`decompiled-quarterly-billing-and-economy.md`](decompiled-quarterly-billing-and-economy.md), see below):

```text
treasury (+0x438) += taxBase (+0x44c) × taxRate (+0x44a) / 100
                   + taxBase / 4
                   - cityCount (+0x446) × 7
                   - wealth (+0x430) / 20000
                   + FUN_004499ec(nation)          // still undecompiled
```

The DAT loader (`FUN_004481a0`, see `imperial_conquest_2`'s `docs/investigations/dat-file-layout.md`) reads `+0x44c` as one of its fourteen pieces, so the DAT carries a starting tax base.

## Checked against every local save [confirmed]

Recomputing `Σ over owned cities (tribute × population / maxPopulation) << 2` and comparing with the stored `+0x44c`, over 54 saves and every nation that holds a city (864 pairs): **569 match exactly**, and the pattern of the others is the code's:

- **Right after a quarterly rebuild, all match.** `1_thracia_271_spring_11.sav`, still on the DAT's starting values: 2 of 16 nations match. `1_thracia_271_summer_1.sav`, after the spring→summer tick: **16 of 16**. `1_rome_270_winter_1.sav`: 16 of 16. Other season-start saves are 15 of 16, the one exception drifting by a capture or defection earlier in that round.
- **The DAT's starting values are not the rebuild's.** Rome `2528` stored vs `2464` recomputed; Carthage `8264` vs `8192`; Seleucid and Armenia match. The starting values survive only until the first quarterly tick.
- **Between rebuilds the stored value drifts**, because population and tribute keep changing without touching it, and captures adjust it by the city's contribution at capture time (after siege damage).
- **Rome's value is 2,444**, not 2,440 (`10.sav`, `11_*.sav`, `12_*.sav`, `1_rome_270_summer_7.sav`, all at 15%). The earlier solve from the dialog's income figures could not tell them apart: `2440 × 15 / 100` and `2444 × 15 / 100` both truncate to 366, and at 20% both give 488.

**The Naupactus capture, exactly** (`1_rome_270_winter_7_b.sav` → `1_rome_270_winter_9_b.sav`, Greece → Illyria). After siege damage Naupactus has tribute 15, population 25, maximum 30, so its contribution is `15 × 25 / 30 = 12`:

| Field | Illyria (new owner) | Greece (old owner) | Predicted |
| --- | --- | --- | --- |
| treasury `+0x438` | `−2021 → −1973` (`+48`) | unchanged | new owner `+ 12 × 4` |
| tax base `+0x44c` | `396 → 444` (`+48`) | `2296 → 2248` (`−48`) | `± 12 << 2` |
| wealth `+0x430` | `768,000 → 843,000` | `2,490,000 → 2,415,000` | `± 25 × 3000` |
| city count `+0x446` | `11 → 12` | `19 → 18` | `± 1` |

Every number lands. This closes the open item in [`pending-offer-block-army-split-and-naupactus.md`](pending-offer-block-army-split-and-naupactus.md): the `+48` was the capture's treasury credit, and "wealth" is a separate field at `+0x430`, keyed to population, not fortification.

**The reparation formula, against its one data point.** [`decompiled-diplomacy-peace-terms-and-instant-battles.md`](decompiled-diplomacy-peace-terms-and-instant-battles.md) gives `reparations = W/4 + random(W/4) + cities × 10` with `W = nation[+0x44C]`. In `1_rome_270_autumn_9.sav`, before Ptolemaic's 2,269-talent payment, Ptolemaic has `+0x44c = 6188` and 48 cities: the formula's range is `[1547 + 480, 1547 + 1546 + 480] = [2027, 3573]`, and **2,269 is inside it** (a `random(W/4)` draw of 242). `W` is the tax base.

## Corrections to existing reports

- [`decompiled-quarterly-billing-and-economy.md`](decompiled-quarterly-billing-and-economy.md): the income formula's second term is `taxBase / 4`, not `mobilization / 4`; the `× 7` term multiplies the **city count** (`+0x446`); the "wealth" pool is `Σ population × 3000`, not fortification; and what grows each quarter is a city's **population** toward its maximum (reduced by the tax rate and by mobilization), not its tribute.
- [`decompiled-city-capture-resolution.md`](decompiled-city-capture-resolution.md): the transfer's wealth term is `population × 3000`, the tax-base term is the city's contribution (`tribute × population / maxPopulation`) `× 4`, not a "per-army value", and the new owner's treasury is also credited `contribution × 4`.
- [`decompiled-diplomacy-peace-terms-and-instant-battles.md`](decompiled-diplomacy-peace-terms-and-instant-battles.md): `+0x44C` is the tax base, not "wealth". The reparation formula and the "drop the poorest trade partner" rule both key on it. Wealth is `+0x430`.

## Still open

- `FUN_004499ec(nation)`, the last income term — **[open] — pending controlled save** (below), or a decompilation pass.
- An exact whole-turn check of the quarterly treasury credit — **[open] — pending controlled save**.
- What `FUN_0044bed8` and `FUN_0044c528` are called from (the defection and cascading-defection paths are the likely callers; the table above records only what they write). One caller of `FUN_0044bed8` is now known: the quarterly rebellion `FUN_0044c204`, for a non-capital city under 30 loyalty — see [`city-population-growth.md`](city-population-growth.md).
**No controlled save is needed for the tax base itself**: where it lives, how it is rebuilt, and how captures adjust it are settled above by the code plus existing saves. A save pair would settle only the two income items. The experiment, to be done at the keyboard:

1. Play **Rome**, in any game, at the **last week of a season** (week 11), on Rome's own turn. Make no orders this turn: no recruiting, moving, supply purchase, tax change or diplomacy.
2. Save as `<n>_rome_<year>_<season>_11_pre.sav` (e.g. `4_rome_269_spring_11_pre.sav`).
3. End the turn, and let the round finish until it is Rome's turn again, at week 1 of the next season: the quarterly tick has run.
4. Save as `<n>_rome_<year>_<nextseason>_1_post.sav`, and write a `notes/<n>_rome.txt` entry naming the pair, "quarter boundary, no Rome actions", and anything the news log reports about Rome in that round (a battle, a lost city, a trade offer).
5. Optional second run: reload the `_pre` save, **raise the tax rate by 5**, end the turn, and save `…_1_post_tax.sav`.

What each hypothesis predicts for Rome between `_pre` and `_post`:

- Tax base `+0x44c` is rebuilt to `Σ over Rome's cities (tribute × population / maxPopulation) << 2`, and wealth `+0x430` to `Σ population × 3000`, both recomputable from the `_post` save's city records. **Both are already [confirmed]; this is a control.**
- Treasury `+0x438` changes by `taxBase × rate / 100 + taxBase / 4 − cities × 7 − wealth / 20000 − (regular army and garrison upkeep, Σ (troops / 200) × price) − (ships × 3) + FUN_004499ec(Rome)`. If the round had no battle or capture involving Rome, the residual after the known terms is `FUN_004499ec(Rome)`. The superseded reading (`mobilization / 4` in place of `taxBase / 4`) predicts a residual that differs by `(taxBase − mobilized) / 4`.
- With the optional run: the two `_post` saves' treasuries differ by exactly `taxBase × 5 / 100` if nothing else in the round depends on the rate. Replayed turns are deterministic for the AI ([`battle-replayed-rout-mechanic-and-combat-constants.md`](battle-replayed-rout-mechanic-and-combat-constants.md)), so the difference isolates the rate term.

## Reproduction

`FUN_00451b40`, `FUN_004498b0`, `FUN_0044bb18` and the other writers are in the local ReTools dump (`all_app_functions.txt`; the capture path also in `capture_transfer.txt`); search for `DAT_00474abc`. The save checks read the SAV nation table at `SharedPrefixLength (100,956) + 2 + armies × 656 + 2 + fleets × 26`, stride 1,172, and the DAT's at `0x1B100`, stride 1,055.
