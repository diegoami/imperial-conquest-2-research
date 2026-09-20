# The instant resolver reproduces the total and not the shape

**Evidence class: the reimplementation's own `BattleCasualties.Apply` driven against an observed
battle, 2026-09-20.** Follows
[`ptolemy-run-ui-inventory-and-leader-draw.md`](ptolemy-run-ui-inventory-and-leader-draw.md) §3, which
transcribed the battle and asked whether the merged code reproduces it. It does not, and the way it
fails is informative.

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
shape completely.**

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
2. **The `ratio ≈ 46` calibration is worth keeping.** Whatever the two armies' powers were, the
   instant model reproduces this battle's *aggregate* at a ratio of about 46, which is a usable
   sanity check on any future `ArmyPower` work: the morale and quality that produce
   `loserPower × 40 / winnerPower ≈ 46` from 45,100 against 27,700 troops are a constraint, not a
   free choice.
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
- The actual `ArmyPower` values, morale or per-unit quality of either army. All three were swept past
  rather than measured.
