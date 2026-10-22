# Four rules seen in play: disband and scuttle refunds, the foreign supply purchase, the Winter storm spike, and an AI war on a human seat

**Provenance:** promoted `[confirmed]` from [`diegoami/ic2-conquest`](https://github.com/diegoami/ic2-conquest)
`main` at `3e573e5` ([PR #140](https://github.com/diegoami/ic2-conquest/pull/140), run `run-exp-manual-gaps`,
owner-approved). Four drafts:
- [disband and scuttle](https://github.com/diegoami/ic2-conquest/blob/3e573e5/findings/2026-10-22-disband-and-scuttle-return-money-and-supplies.md);
- [buying supplies from a foreign city](https://github.com/diegoami/ic2-conquest/blob/3e573e5/findings/2026-10-22-buying-supplies-from-a-foreign-city.md);
- [Winter storm spike](https://github.com/diegoami/ic2-conquest/blob/3e573e5/findings/2026-10-22-winter-storm-spike-on-own-fleets.md);
- [AI declares war on a human seat](https://github.com/diegoami/ic2-conquest/blob/3e573e5/findings/2026-10-22-ai-declares-war-on-a-human-seat.md).

The run log is [`run-exp-manual-gaps/`](https://github.com/diegoami/ic2-conquest/tree/3e573e5/runs/experiments/data/run-exp-manual-gaps).

All four use **staged** saves: positions, owners or relations were set by save edits, and every edit is logged in
`staged-edits.jsonl`. Natural play follows on the seed build `354d8265…` under Wine, seed 12345 unless named. The
binaries are in release [`run-exp-manual-gaps`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-manual-gaps)
(published 2026-10-22: 46 saves and 39 screenshots, the hashes checked against `SAVES.sha256` before upload) and on
the owner's Drive (`IC2/artifacts/run-exp-manual-gaps/`).

**Intake by the research session (2026-10-22).**
- The 46 saves were fetched read-only from Drive, and all 46 match `SAVES.sha256`.
- The saves were decoded independently with
  [`scripts/manual-gaps-intake-check.py`](../../scripts/manual-gaps-intake-check.py). Receipt:
  [`manual-gaps-intake-v1.json`](../data/manual-gaps-intake-v1.json) (decoded scalars and news text only).
- The code was re-read in the pinned `all_app_functions.txt` (`2018c205…`), with one instruction-level check in the
  EXE (`9d753d5d…`).
- Three screenshots were viewed: the Offer of peace, the foreign purchase dialog and the news after the declaration.
- No game was launched, and there was no independent review.

## 1. Disband army and Scuttle fleet: the whole purse to the treasury, the whole stock to the city

**Answer [confirmed: code + one play each].** On Yes, `TUnitMap_DisbandArmy` (:47108–47115) and
`TUnitMap_ScuttleFleet` (:47347–47356) do the same things:
- add the unit's money to the nation's treasury (`+0x438`);
- add its supplies to the own city that `FUN_004494e4` returns (city `+0x18`);
- delete the unit.

Neither the city stock nor the treasury is capped, and the troops or ships are not refunded.

| Order | Unit before | Every changed field, before → after (field-by-field diff of the whole record area) |
|---|---|---|
| Disband army 0 next to Arretium, turn 0720 | 23,700 troops, money 100, supplies 170 | treasury 2,200 → **2,300**; Arretium stock 150 → **320**; army 0 owner 0 → −1; map (100,37) 200 → 2 |
| Scuttle fleet 2 next to Antium, turn 0734 | 20 ships, money 100, supplies 100, no army aboard | treasury 1,630 → **1,730**; Antium stock 230 → **330**; fleet 2 owner 0 → −1; map (101,46) 300 → 0 |

The news is unchanged in both. Arretium ends above its start, so no supply cap applied. Fleet 2's 100 talents and 100
tons were loaded in the same session by Supply fleet.

**Which city, when two own cities are adjacent [code; added here, not played].** `FUN_004494e4`
(:48068–48105) loops the x offset −1..1 outside and the y offset −1..1 inside. It overwrites its result at **every**
own-city marker it finds (`20 ≤ v < 100`, `(v − 20) mod 16 == nation`). So the **last** own city in that order
receives the supplies: the largest x offset, then the largest y offset. This agrees with the specification's "last
own city found" for the regular-unit disband test, which uses the same helper.

## 2. Buying supplies from a foreign city at peace

**Answer [confirmed: code + two plays].** Next to a foreign city whose owner is not at war with the player, Supply army
opens the **Buy supplies** layout. The screenshot shows "Supplies at Agrigentum", "Army's supplies", the 10s and 100s
arrows, "Supplies amount", "Supplies cost", the Buy supplies button and "Army's money", with **no National balance row**.

`TAFSupply_ChangeBuyAmount` (0x43FE4C) clamps the amount in this order:
1. at least 0;
2. at most the city's stock;
3. at most the room left: for an army `troops div 100 + 1 − supplies`, for a fleet `ships × 8 − supplies`;
4. at most `purse × 5`.

The `INC EDX` at `0x43FEF5` adds 1 to the cap before `min`, as
[supply-capacity-rounding](supply-capacity-rounding.md) already read. The decompiled C puts the `+ 1` outside the
`min`, as if it applied to the amount, which is wrong.

`TAFSupply_TransferSupply` (:43049–43085) then makes four writes:
- the unit's supplies rise by the amount;
- the city stock falls by the amount;
- the **city owner's** treasury rises by `amount div 5`;
- the unit's purse falls by the same `amount div 5`.

The buyer's treasury is never written.

| Case (Rome army 1 staged next to Agrigentum, Carthage, peace) | Asked | Bought / cost | Army after | Agrigentum | Carthage treasury | Rome treasury |
|---|---:|---|---|---:|---:|---:|
| capacity cap: 22,000 troops, supplies 176, purse 100 | 50 | **45 / 9** (= 220 + 1 − 176) | supplies 221, purse 91 | 197 → 152 | 11,000 → **11,009** | 2,200, unchanged |
| purse cap: supplies 0, purse 5 (staged) | 50 | **25 / 5** (= 5 × 5) | supplies 25, purse 0 | 197 → 172 | 11,000 → 11,005 | unchanged |

- **First case:** the diff holds only these fields plus Rome's two map-view words (`+0x486`, `+0x488`). The staged
  save's values are as stated.
- **Second case:** there is **no after-save**. Its result rests on the run's memory log (`run-log.jsonl`
  `B9b_buy`) and two screenshots.
- **Inference:** because the cost is `amount div 5`, an amount that is not a multiple of 5 gets up to 4 tons free.
  The arrows move in tens, but the stock and room clamps can leave other amounts. This was not played.

## 3. The Winter storm spike to 30, on own fleets

**Answer [confirmed: code + play].**

**Staging:** six Rome fleets of 50 ships, at condition 100 with 400 supplies, were placed on calm sea 6–9 tiles from
any city in Winter week 1 of 270 BC. Then there were six End turns on seeds 12345 and 1.

Decoding the 12 autosaves against the staged save, each fleet-turn falls into exactly one branch of the storm pass
(`supply-driven-morale-and-fleet-attrition.md`; `d = (10000 div (dmg + 100))² div 100`, and ships and condition each
lose `x · d div 300`):

| Outcome | Fleet-turns | Loss | Branch |
|---|---:|---|---|
| dmg 5 | 61 | condition −5 | dmg₀ = 1 → Winter 2 → away 2·2 + 1 |
| dmg 9 | 7 | ships and condition × 82/300 | dmg₀ = 2 → Winter 4 → away 9; d = 91²/100 = **82** (the draft's 84 was corrected upstream before merge) |
| **spike, dmg 30** | **4** | **−9 ships; −17, −17, −16, −15 condition** at condition 90, 90, 85, 80 | d = 76²/100 = **57** |

- **Where the spikes fell:** seed 12345, turn 0741, fleet 0; seed 1, turn 0741, fleet 1; seed 1, turn 0742, fleet 0;
  seed 1, turn 0743, fleet 4.
- **Rate:** 4 of 72 is 5.6 %, against the code's 1 in 20. That is consistent but not a measurement: 72 trials, two
  seeds, and the fleets of one seed are not independent draws.
- **Season:** the last autosave already reads Spring 269 BC, but all six of its ticks classify as Winter branches, so
  the storm pass ran before the season changed.
- **The spike costs fewer ships than the dmg-9 hit** (d 57 < 82), as the 2026-09-23 note derived. At condition ≥ 81 it
  is the only way a fleet on calm sea loses ships.
- **What this changes:** the [storms report](2026-10-03-storms-and-losses-at-sea.md) left the spike "neither confirmed
  nor excluded". Its single Ptolemaic spike (ships −13, condition −14) is now joined by four.

## 4. An AI nation declares war on the human seat, and an alliance drags the human into a war

**Answer [confirmed: two events in one staged run].**

**(a) Carthage's own war rule.** The staging is the two logged words: Carthage–Celtiberia 3 → −18, both ways
(`nation1+0x36`, `nation8+0x28`). Decoded per turn:

| | Staged (0720) | 0721–0733 | 0734 |
|---|---|---|---|
| Carthage at war with | nobody | nobody | Rome |
| Carthage mobilisation | 15 | 15 → 9 | 13 |
| Season | Spring | Spring, Summer, Autumn | Autumn |
| Rome allies (relation 2) | none | none | none |
| P(Carthage) / P(Rome), `wealth div 20000 × unity div 100` | 1,732 / 1,050 (8 × ratio 13.2) | → 1,859 / 630 | |
| Carthage ↔ Rome | 0 | 0 | **3, both ways** |

- Every gate of `FUN_0044FB7C` holds from the start
  ([decompiled-ai-offers-to-human-seats](decompiled-ai-offers-to-human-seats.md) §1a), so the 1-in-10 draw came on the
  14th AI turn. The chance of 13 misses first is 0.9¹³ ≈ 25 %.
- At 0734 the relation changes are Rome–Carthage and the cooldowns from Seleucid's conquest of Galatia, nothing else.
- The news line is "CARTHAGE DECLARES WAR ON ROME.", upper-cased because a human is involved. The screenshot shows it
  in the Information panel under Week 3 Autumn 270 BC.
- The run log records no message box.

**(b) Found here: Illyria's alliance with Gaul.** The upstream finding does not mention this. Between turns 0721 and
0722 the news reads "Illyria forms an alliance with Gaul." and then "ILLYRIA DECLARES WAR ON ROME.":
- Illyria–Gaul went −8 → 2;
- Rome–Illyria went from **trade (1) to war (3)**;
- Illyria–Dacia went 0 → 1, which is trade.

This is the AI's **alliance** rule with the setter's one-step cascade, not its war rule. Every gate holds:
- Illyria is at war with nobody, has mobilisation 0, and it is Spring;
- Rome is Illyria's neighbour, with relation 1, and is unprotected;
- Gaul is the first AI at war with Rome, with one war;
- Rome's 25 cities are fewer than Illyria's 9 plus Gaul's 28.

So the human was put at war without a prompt, and lost a trade agreement, by an alliance between two AI nations.
The [war-cascade report](decompiled-war-cascade-and-peace-paths.md) and the specification describe that path from
the code; this is its first observation against a human seat.

**What the human sees:** in both cases, only a news line. The run's End-turn and turn-start boxes were supply warnings
and trade offers.

## Also in the run (screenshots and staged checks, not rules)

- **Screenshots:** the attack-army and attack-fleet prompts, the "army too large" box, the Cellular Automata window and
  the Offer of peace after a human loss (seed 2; seed 1 gave none; answered No, relation stays 3, save checked). The
  End of Game window was shot three ways:
  - 250 BC: `AUTO1200` is Week 1 Spring 250 BC, with the treasury at 2,221;
  - deposition for debt: treasury −30,000;
  - a **staged** victory: only the city-count word was set to 334.

  These complete the manual's list, and only the Offer of peace screenshot was viewed here.
- The seed build draws one Cellular Automata pattern for every press. The original EXE draws a different one each
  time, consistent with [cellular-automata-savebmp-format](2026-10-09-cellular-automata-savebmp-format.md).
- **The clipped End of Game reason line:** ic2-conquest no longer sees the clipping noted in
  [end-of-game-screens](2026-10-05-end-of-game-screens.md) and attributes it to the font setup. That is not checked
  here.

## What this does not establish

- **One play each:**
  - for disband and scuttle;
  - for each purchase cap; the stock cap, the 100s arrow and a fleet purchase were not played;
  - for each declaration path.
- **Not played:**
  - the two-adjacent-cities choice;
  - the free tons of an amount that is not a multiple of 5;
  - the 1-in-10 and 1-in-20 rates, which are consistent but not measured;
  - rough sea and the near-city storm branch, which the 2026-10-03 storms report covers.
- **Staged positions:** the unit placements, the fleets and Carthage's peace with Celtiberia are save edits. In the
  unedited start Carthage is at war with Celtiberia and cannot declare.
- **Environment:** Wine and the seed build only. There was no native Windows run and no independent review.
