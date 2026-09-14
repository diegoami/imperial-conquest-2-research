# The quarterly billing cycle: upkeep, treasury income, tribute, and rebellion

The biggest single result of this decompilation pass. `FUN_00451b40` is called exactly once per season (at the week-11-to-1 wrap, right before the season counter itself advances) — confirming **"quarterly" means once per season, four times a year**, not a separate real-time-style billing period. This one function resolves several previously-open questions from multiple earlier reports at once.

## Ship upkeep: the mystery "ships × 3" value, solved

`decompiled-fleet-tax-and-mercenary-formulas.md` found `TBuildFleet` displays `shipCount × 3` alongside the confirmed cost (`×10`) and capacity (`×500`) values, with no explanation. Here, for every deployed fleet:

```text
owner.treasury -= shipCount × 3
```

**That's the quarterly upkeep cost per ship: 3 talents/ship/quarter**, charged here every season. The `TBuildFleet` dialog was previewing this cost at order time, exactly like it previews the one-time build cost and the capacity.

## Army and garrison upkeep use the same price table as recruitment

> **Correction (2026-09-14):** see [`upkeep-payment-and-desertion.md`](upkeep-payment-and-desertion.md). The formula below applies to **regular** units and city-unit slots, and those are billed to the treasury with no balance check. **Mercenary** units (slot `+0` ≠ 0) cost `((troops div 200) × price × quality) div 5`, billed to **their army's purse** (`+12`), never the treasury. The non-payment test is per mercenary slot: `purse ≤ 0` before that slot. When it fails, the whole mercenary unit is removed, and `troops div 100` is taken from the army's **supplies** (`+10`), not its troops. `FUN_0044ac3c` is the generic remove-unit helper, not a "degrade" state. Regular units never leave for lack of pay. Morale is not touched, and no news is written. Debt's only consequence is leader deposition (below).

For every unit in every army, and separately for every occupied city-garrison recruitment slot:

```text
unitUpkeep = (troops / 200) × quarterlyPriceTable[unitType]
```

This is the exact same table (`DAT_00478fd4`) and formula shape `decompiled-recruitment-cost-formula.md` already solved for the *initial* recruitment decision — now confirmed as the ongoing charge too, applied quarterly to every unit a nation fields, whether in the field or garrisoned.

**A real consequence for not being able to pay:** if a nation's available funds for this purpose drop below 1, army units start **losing troops** (reduced by `troops/100`) and a state-change is triggered (`FUN_0044ac3c`, the same "unit degrades" helper seen gating readiness in the weekly tick) — i.e., **an unpaid army mutinies/disbands partially**, not just accruing debt silently.

## The treasury income formula

> **Correction (2026-09-14):** see [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md). The second term below is `taxBase / 4`, not `mobilization / 4`; the `× 7` term multiplies the city count (`+0x446`); "wealth" (`+0x430`) is `Σ population × 3000`. The tax base is nation `+0x44c`, rebuilt here each quarter from cities.

For each nation once per quarter:

```text
treasury += (nationTaxBase × taxRate) / 100        // the exact formula from decompiled-fleet-tax-and-mercenary-formulas.md
         + mobilization / 4
         - <upkeep field> × 7
         - wealth / 20000
         + <another income term, from an undecompiled helper>
```

> **Correction (2026-09-14):** see [`upkeep-payment-and-desertion.md`](upkeep-payment-and-desertion.md). The last term, `FUN_004499ec`, is trade and alliance income: `Σ taxBase[j] div 12` over nations `j` with relation 1 or 2. The complete formula, with ship, regular and city-unit upkeep, is exact for the human nation in all 6 quarter pairs and for 27 of 80 nation-quarters with no adjustment.

The first term is the same `income = nationTaxBase × tax% / 100` formula already solved exactly from Rome's own 15%/20% data (`nationTaxBase = 2,440`) — this confirms it's not just a dialog preview number, it's the literal quarterly treasury credit. The other terms (a mobilization-linked bonus, a flat upkeep-style cost, and a small drain proportional to the accumulated "wealth" pool) are new context but not individually verified against an observation this pass.

## Tribute grows toward a population-based target, moderated by tax rate

> **Correction (2026-09-14):** see [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md). What grows each quarter is a city's **population** (`+0x1c`) toward its maximum (`+0x1e`), reduced by the tax rate and by mobilization — not its tribute. The wealth contribution is `population × 3000`, not fortification.

> **Correction (2026-09-14):** the exact step is in [`city-population-growth.md`](city-population-growth.md): `d = (maxPop − pop) >> 2; d −= d × taxRate / 120; pop += d − d × mobilized / 300 + 1`, capped at `maxPop`, skipped when a hostile army is adjacent, with no random draw. It runs before the city's wealth and tax-base contributions are added, so the rebuild and the treasury credit use the grown population.

Each city's tribute value is nudged toward a target derived from its population, with the tax rate reducing how much it can grow — a plausible design reason a heavily-taxed city's tribute contribution plateaus lower than a lightly-taxed one's. The city's "wealth" contribution (`fortification × 3000`, the same formula already seen applied instantly on capture in `decompiled-city-capture-resolution.md`) and its contribution to the nation's `taxBase` field are both **recomputed here every quarter for every city**, not just adjusted at the moment of capture — capture's immediate adjustment was a special-case correction to a total that's normally rebalanced quarterly anyway.

## Loyalty, rebellion, and diplomatic thaw

- **Low tax raises loyalty; high tax risks it.** If a nation's tax rate is under 11% and a city's loyalty is below 80, there's a chance loyalty rises. Separately, there's a 1-in-3 chance of a loyalty penalty scaled to the tax rate.
- **A rebellion/unrest check exists below a loyalty threshold** (`FUN_0044c204`, not decompiled) — cities with loyalty under 30 can trigger it.
- **A computer-controlled nation stability check**: roughly a 1-in-9 chance per quarter of evaluating whether the nation is prosperous (unity above a threshold and finances healthy); if not, it calls the same cleanup function (`FUN_0044c8f0`) already seen in the "nation eliminated" cascade from `decompiled-defection-and-siege-attrition.md` — plausibly an AI-nation collapse/instability consequence for sustained poor management, not confirmed in detail.
> **Correction (2026-09-14):** see [`upkeep-payment-and-desertion.md`](upkeep-payment-and-desertion.md). `FUN_0044c8f0` is **leader deposition** ("*X depose their leader Y.*"). The trigger, for AI nations only and after the income credit, is `Random(9) == 0` and (treasury `< −(wealth div 500)`, or `< −20000`, or unity `< 400`). It gives the nation a new leader, sets unity to `max(unity, min(550, unity + 150))`, and resets a negative treasury to 0 (otherwise `+1000`). It is confirmed on 2 of 15 in-debt AI nation-quarters (Galatia, Gaul). A human nation faces the same test at the start of each of its turns, and failing it ends the game: "*Your army have deposed you because they have not been paid.*"

- **Diplomatic relations drift toward peace over time.** For every nation pair with a negative (hostile) relation value, there's a 1-in-3 chance per quarter of a small automatic improvement — wars don't stay maximally hostile forever even without a peace treaty.
- **Unity decays by 3 every quarter**, clamped at 0 — a baseline erosion that must be offset by successful captures/growth (`+9` per capture, seen in earlier reports) to hold steady or rise.

> **Correction (2026-09-14):** see [`city-population-growth.md`](city-population-growth.md). The `−3` (floored at 0) applies to **mobilization** (`+0x442`), not unity. Unity (`+0x440`) is then recomputed as `min(990, max(300, unity + 25 − taxRate / 2 − mobilized / 5))`, so it drifts up, not down. Confirmed on 5 quarter pairs: mobilization 71 of 80 nation-quarters exact, unity 60 of 80 (the rest had battles, captures or orders in the round).

## What this does not establish

- The exact identity/units of several fields referenced only by offset (the mobilization-linked income term, the flat upkeep-cost term, the "wealth" drain).
- `FUN_004499ec` (an additional income source per nation) and `FUN_0044c204` (the rebellion check) — neither decompiled this pass.
- Whether the AI-nation stability check's exact trigger condition is "collapse if unhealthy" as read here, or something more nuanced.
- No numeric cross-check against a real save was performed this pass — this report establishes the formula shapes and confirms prior guesses/dialog previews, but doesn't verify exact totals against an observed quarterly treasury change the way the tax and fleet formulas were originally verified.

## Reproduction

Found by tracing one call deeper than `decompiled-turn-and-calendar-sequencing.md`'s weekly tick: `FUN_00451b40`, called from `FUN_004514ec` only when the week counter is about to wrap from 11 to 1.

## Next checks

1. Find a same-season-boundary save pair (one just before a week-11→1 wrap, one just after) to numerically verify the treasury formula's remaining terms, the way the tax formula was originally verified from Rome's dialog values.
2. Decompile `FUN_004499ec` and `FUN_0044c204` for the remaining income term and the rebellion mechanic.
3. Watch for an AI nation actually collapsing in a future save to confirm the stability-check's real trigger and effect.
