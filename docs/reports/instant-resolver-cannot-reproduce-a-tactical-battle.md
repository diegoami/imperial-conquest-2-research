# The instant resolver reproduces neither the shape nor, at any reachable ratio, the total

**Evidence class: the reimplementation's own `BattleCasualties.Apply` driven against an observed
battle, 2026-09-20.** Follows
[`ptolemy-run-ui-inventory-and-leader-draw.md`](ptolemy-run-ui-inventory-and-leader-draw.md) §3, which
transcribed the battle and asked whether the merged code reproduces it. It does not, and the way it
fails is informative.

> **Correction (2026-09-23)**, from a targeted pass on [`imperial_conquest_2#288`](https://github.com/diegoami/imperial_conquest_2/issues/288).
> This report first said the instant model "reproduces this battle's aggregate at a ratio of about
> 46", and treated that ratio as a constraint on morale and quality. Both readings are wrong. The
> ratio the resolver actually computes is `loserPower × 40 / winnerPower` with the winner never the
> weaker side, so **it cannot exceed 40**. For these two armies it lies between **14 and 27** over
> the whole legal morale range. The power formula has **no quality term**. So `ratio ≈ 46` is not a
> reachable input, and it constrains neither morale nor quality. The title, §"The result", "What
> follows" 2 and "What this does not establish" are corrected below. The sweep table and the shape
> finding are unchanged.

## The battle was tactical, not instant

`IP1 000.mp4` t=21, four seconds before the summary panel, is the **tactical** screen:

```
Seleucid v Ptolemaic    Seleucid to move units

    Greek mercenaries          ATTACKS      Thracian mercenaries
    Light infantry                          Light infantry
    Troops  717                             Troops  2,487

    UNIT LOSSES
    Attacker  routed
    Defender  130
```

`ATTACKS`, `UNIT LOSSES`, and the word **`routed`** — the mechanic
[`battle-replayed-rout-mechanic-and-combat-constants.md`](battle-replayed-rout-mechanic-and-combat-constants.md)
decompiled as `FUN_00438fb0`. The player confirms the EXE was patched to run tactical battles **fast**,
not to auto-resolve them, so the accelerated timing is not evidence of instant resolution.

This matters because the reimplementation has **only** the instant path.
`InstantBattleResolver`'s own header says the tactical model — the type-effectiveness matrix, the
per-type shooting-vulnerability weight, the melee caps, the tactical morale array and the rout
mechanic — is not implemented there. So the comparison below is between two different mechanisms, and
it is worth making precisely because **every battle in the reimplementation resolves through the
instant path**, including ones the original would fight tactically.

## The test

`BattleCasualties.Apply` was driven directly, with the winner's five type totals as five slots,
against `classical-faithful` (`numerator=40`, divisor in `[105, 120)`), averaged over 400 seeds per
ratio. The casualty ratio depends on both sides' `ArmyPower`, which depends on morale and per-unit
quality that the panel does not show — so rather than guess them, the ratio was **swept**.

| ratio | total | light inf | heavy inf | archers | light cav | heavy cav |
|---|---|---|---|---|---|---|
| 5 | 4.4% | 4.5% | 4.4% | 4.4% | 4.3% | 4.4% |
| 20 | 17.7% | 17.8% | 17.8% | 17.7% | 17.3% | 17.5% |
| 40 | 35.5% | 35.6% | 35.5% | 35.4% | 34.6% | 34.9% |
| 43 | 38.2% | 38.3% | 38.2% | 38.0% | 37.2% | 37.5% |
| **46** | **40.8%** | **41.0%** | **40.8%** | **40.7%** | **39.8%** | **40.1%** |
| 49 | 43.5% | 43.6% | 43.5% | 43.4% | 42.4% | 42.8% |
| 60 | 53.2% | 53.4% | 53.3% | 53.1% | 51.9% | 52.4% |
| 105 | 93.2% | 93.5% | 93.2% | 92.9% | 90.8% | 91.6% |
| 120 | 100.0% | 100.0% | 100.0% | 99.9% | 100.0% | 100.0% |
| | | | | | | |
| **observed** | **40.8%** | **37.6%** | **29.6%** | **100.0%** | **19.3%** | **4.0%** |

## The result

**At `ratio = 46` the model hits the observed total exactly — 40.8% against 40.8% — and misses the
shape completely. But `ratio = 46` is not an input the resolver can produce** (below), so in practice
it misses the total as well.

**The reachable ratios** `[confirmed]` code, `[derived]` numbers. `FUN_0044AEE4` computes both
powers with `FUN_0044A8CC`, `Σ(weight[type] × troops / 100) / 80 × morale[+14]`. There is no quality
term. The stronger side wins (`pB < pA` for the attacker; a tie goes to the defender), and the
winner's ratio is `weakerPower × 0x28 / strongerPower` (`iVar4 * 0x28 / iVar3`, or the mirror in
the defender branch). That is **at most 40**, reached only at equal powers. For this battle, the
panel's type totals and the confirmed weights 20/100/40/60/120 give Seleucid
`1,990,000 / 100 / 80 ≈ 248 × M_S` and Ptolemaic `992,000 / 100 / 80 ≈ 124 × M_P`. The ratio is then
`≈ 20 × M_P / M_S`, which over the whole strategic-morale range 51–70 on both sides is
**14.6–27.5, i.e. 14–27 after truncation**. The per-unit `/100` truncation, which needs the unit
breakdown the panel does not show, moves this by a fraction of a point. On the sweep above, that is
a winner's loss of roughly **12–24%**. The observed 40.8% sits above that range, and above the
resolver's absolute ceiling, about 35.5% at ratio 40.

One mechanism in the original's instant path can take more than the ratio implies, and the sweep
did not model it. After the per-unit loss, `FUN_0044AE20` (`0x0044AE20`, the second loop) deletes,
through `FUN_0044AC3C`, any unit left below `standardBattalionSize / 10` if it is national (origin
label `0`), or below `/ 5` if it is a mercenary. `[confirmed]` code. Whether that could lift this
battle's total needs the winner's unit-level roster, which the panel does not give. **[open]**

- Model spread across types at that ratio: **1.2 percentage points** (39.8 – 41.0).
- Observed spread: **96 percentage points** (4.0 – 100.0).

And **no ratio can close it.** The model's per-type rates are locked together by construction: every
slot takes the same `ratio` and differs only by a divisor drawn from `[105, 120)`, a ±7% band. To get
archers to 100% the ratio must reach ~120, and at that ratio *everything* is at 100% and the total is
wrong. The two constraints — matching the total and reproducing the spread — cannot be satisfied
together by this function at any ratio.

**This is not a defect in the instant resolver.** It is the instant resolver being what it says it is:
a whole-army ratio applied slot by slot, with no notion that archers are more vulnerable than heavy
cavalry. The observed differentiation is the tactical model's, and the tactical model is unbuilt.

## What follows

1. **The reimplementation's battles are flat where the original's are shaped.** A player who loses an
   army in the reimplementation loses ~40% of every type; in the original they lose their archers
   outright and barely scratch their heavy cavalry. That is a visible difference in play, not only in
   the numbers, and it is the strongest argument yet for the tactical path being more than a nicety.
2. **`ratio ≈ 46` describes the tactical outcome. It does not constrain `ArmyPower`.** It is only
   the ratio at which the instant casualty function's mean loss equals this battle's observed 40.8%.
   It is **not reachable**: the ratio is capped at 40, and these two compositions give 14–27 at
   every morale in 51–70. So it cannot be used to back out morale, and quality does not enter the
   power formula at all. What it **does** say is that this tactical battle cost the winner more than
   the instant resolver can charge any winner. Excluding the small-unit deletion noted above, the
   ceiling is about 35.5% at the tie ratio of 40, and about 12–24% for this matchup. The gap belongs
   to the tactical model, the same rout-and-matrix machinery that produces the shape (point 1). It is
   not a mis-set power. As a calibration target it is usable only by a resolver that models those
   tactical effects, and it is a single sample.
3. **The per-type ordering wants more instances.** One battle gives archers > light infantry > heavy
   infantry > light cavalry > heavy cavalry. That ordering is consistent with a type-vulnerability
   weighting, and
   [`combat-type-effectiveness-matrix.md`](combat-type-effectiveness-matrix.md) has the matrix — but
   one engagement cannot separate the matrix's contribution from the rout mechanic's, and the archers'
   100% is far more likely to be a rout than a casualty roll.

## What this does not establish

- **Nothing about whether the instant resolver is faithful to the original's own instant path.** The
  original has one (`FUN_0044AEE4`, decompiled); no observation of it exists in this corpus. This
  report compares the instant resolver to a *tactical* outcome, which is the only kind the run
  recorded.
- The actual `ArmyPower` values or strategic morale of either army. They were swept past rather than
  measured, and the 14–27 range above brackets them. Per-unit quality does not enter `ArmyPower`.
