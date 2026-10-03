# Naval battles with an army aboard: the cargo adds to the fleet's strength, the winner's army loses about three times the fleet's fraction, the loser's army sinks with it

**Status:** promoted from the `ic2-conquest` draft of the same name (branch `experiment/naval-cargo`, commit `e7ee4d0`), **with two explanations added at promotion (next block)**. **Wine-only: every result below is a candidate until the desktop original confirms it.** It is task T3 of `docs/proposals/fleet-battles-and-storms.md`, on the fixture of [2026-10-02-naval-battles.md](2026-10-02-naval-battles.md) (cell P: Ptolemaic 70 ships × condition 63 attacks Carthage 90 × 74, war, calm sea; no cargo: 0 of 10 won). **The cargo is a synthetic edit of the save** (see Method), 80 battles in eight cells (six first, then heavy infantry and a mixed army), 10 seeds each (seeds 1–10, the same draws in every cell).

> **Added at promotion (research repository).** Two things the draft calls unexplained or unsettled follow from the decompiled rule in [decompiled-diplomacy-peace-terms-and-instant-battles.md](decompiled-diplomacy-peace-terms-and-instant-battles.md).
> 1. **The winner's army and the "sharp loss threshold" are the code.** `FUN_0044B4F8` applies casualties to the carried army with `ratio = d` (the same `d = r² / 100` that sets the ships lost, `ships × d / 300`), which costs each unit about `d / (105 to 119)` of its troops, and when **`d > 70`** it also removes whole units, so **a one-unit carried army is always destroyed**. Ship loss fraction `f = d / 300`, so the factor of about 3 is `d / 100`, and `d > 70` is `f` above 0.2333, exactly the jump between 0.229 and 0.233. The single-unit armies here show it: all **51** won battles with a one-unit cargo agree with "all lost if and only if `d > 70`, otherwise a fraction within `d/119` to `d/105`" (30 destroyed, 21 partial, **0 inconsistent**, `d` bounded from the observed ship loss; `scripts/naval-cargo-check.py`). **The mixed army (M15) shows the other half of the rule.** With `d ≤ 70` (three battles, `d` 52 to 68) it keeps 4,280 to 5,248 of its 11,000 men; with `d > 70` (six battles, `d` 73 to 94) it keeps at most 1,766, down to nothing, because whole units are removed at random on top of the casualties. The break falls exactly at `d > 70`. The loser's army dying with its fleet is `FUN_0044AD38` deleting it. The exact distribution of the casualties and of the small-unit deletion pass (`FUN_0044AE20`) remains the open item the code report lists.
> 2. **The cargo-divisor claim does not survive the exact integer rule.** The draft's "expected" column and its divisor fit use the continuous `U(0, 0.3)` factor, which [2026-10-02-naval-battle-random-term.md](2026-10-02-naval-battle-random-term.md) shows is not the code's rule. With the code's discrete 0/10/20/30 % bonus and ties to the defender, the expected attacker win rates at the formula's `/50` are **0.0625** (L5), **0.25** (L10), **0.625** (L15, A5, H15 and M15), **0.9375** (L25) and **0.375** (L15D5), against the draft's 0.004, 0.22, 0.63, 1.00 and 0.25. The observed 1, 3, 9, 10 and 5 of 10 are then unremarkable except the 9 of 10 at 0.625 (chance of 9 or more: about 6 %), and **L15, A5, H15 and M15 are the same battle** (equal strength, equal draws, identical results in all 10 seeds, checked), so that one result is counted four times in any fit. The divisor sweep under the exact rule still prefers about `/40` (log-likelihood −31.0 against −38.3 at `/50`), but that rests on the four duplicated cells; `/50` is not rejected, and the cargo term `siegeStrength / 50` stands as read from the code.

**Answer.**
- **A carried army raises the fleet's chance of winning**, in the direction and roughly the size of the research formula (`ships × condition / 10 + siegeStrength / 50`, random 0–30 % on each side): attacker wins out of 10, with 0 for no cargo — 5,000 light infantry **1**, 10,000 **3**, 15,000 **9**, 25,000 **10**.
- **Composition counts as the formula says (archers ×3):** 5,000 archers and 15,000 light infantry have the same siege strength and gave **the same result in all 10 seeds**, ship for ship (9 wins, identical losses), though the archers are a third of the men. **15,000 heavy infantry (H15) and a mixed army of 11,000 men of five types (M15), both built to the same siege-weighted 15,000, again gave the same result in all 10 seeds** (winner, ships and condition lost): the siege strength weights only archers, not heavy infantry or cavalry.
- **The defender's cargo counts too:** with the attacker at 15,000 light infantry, giving the defender 5,000 light infantry lowered the attacker's wins from **9 to 5** of 10.
- **The loser's army is destroyed with its fleet** (owner −1) in all **28** battles whose losing fleet carried one (the 18 lost attacks in the five cells where only the attacker carries, and all 10 battles of L15D5, whose loser always carries), including a defending army (5,000 → 0). Where the loser carried nothing (32 battles) Carthage's army 2 is not aboard and was untouched.
- **The winner's army pays more than the fleet does:** when the winning fleet lost a fraction `f` of ships, the army aboard lost about **2.6 to 3.0 × f** (for `f` from 0.10 to 0.229, 21 battles of single-unit armies) and **all of it** when `f` ≥ 0.233 (30 battles of single-unit armies). **A mixed army loses unit by unit and keeps a remnant:** the mixed M15 army (11,000) lost 84–100 % when `f` ≥ 0.243 but only the weakest units went to zero. Morale was unchanged (the army's own, 67 for Ptolemaic's and 65 for Carthage's) and the attacker's moves ended at 0.
- **The size of the cargo effect is not settled:** the data lean to a larger effect than `/50` (a divisor near 40 fits best), but the formula's `/50` is not excluded.

## Method

- **Build and seed:** `Imperial Conquest 2 fast rollingsave seed.exe` (SHA-256 `354d8265…532f`), Wine 9.0, Xvfb; one fresh process per trial, `SEED.TXT` = the seed (read at program start only).
- **Fixture and the synthetic cargo:** every cell starts from `FIX_P` (`saves/fleets-adjacent-at-sea-0723.SAV`'s Ptolemaic-seat fixture of the T2 finding: Ptolemaic fleet 1, 70 ships, condition 63, supplies 0, next to Carthage fleet 0, 90 ships, condition 74). An army can only embark from a land tile next to the fleet and the starting armies are 18,600 to 56,400 men, so the cargo is **written into the save** by `runs/experiments/fleet-battles/t3_stage.py`: the army's position becomes the fleet's tile, its cell −1, its moves 0, the fleet's carried-army field the army's index, the map cell the army left its terrain, and the army's units are replaced by the chosen ones (one unit of the chosen type and size, quality average, morale as it was: Ptolemaic army 7 at 67, Carthage army 2 at 65). **The edit was checked against a natural embark:** at the two-human start (`T1_0720_s13_Carthage.SAV`) army 2 was moved to (48,62) and embarked by clicks onto fleet 0 (`t3_natural_embark.py` → `T3_NATURAL_EMBARK.SAV`); the same edit's **positional and staging fields** (the army's tile, cell and moves, the fleet's carried-army field, the vacated map cell; army 2 kept its own units) applied to the same start give a save with the same parsed map, cities, armies (position, owner, moves, cell, troops) and fleets, and **3 raw bytes differ** (offsets 112522, 112526 and 112528, inside the nation records' tail; they changed in the natural embark too, with different values, and look like the view position; not understood). The part of the edit that rewrites the units (sizes, types) was **not** compared with a natural save: the game read the edited troops back from its own memory before every battle (`army_state` before = 5,000/10,000/15,000/25,000), and the archers' result shows it used the types. It is **not** a natural staging of the battle: the game never saw the army board in these fixtures, and the fleet kept its 24 moves (a natural embark leaves it 0).
- **Cells** (attacker Ptolemaic fleet 1 always; `strength` before the random term; cargo = `siegeStrength / 50`, `siegeStrength = troops/80 × morale` with archers' troops ×3, `state/sav.py`):

| cell | attacker carries | defender carries | attacker strength (rounded) | defender strength (rounded) |
|---|---|---|---|---|
| (P, T2) | nothing | nothing | 441 | 666 |
| L5 | 5,000 light infantry (+83.1) | nothing | 524 | 666 |
| L10 | 10,000 (+167.5) | nothing | 609 | 666 |
| L15 | 15,000 (+250.6) | nothing | 692 | 666 |
| A5 | 5,000 archers (+250.6) | nothing | 692 | 666 |
| L25 | 25,000 (+418.1) | nothing | 859 | 666 |
| L15D5 | 15,000 (+250.6) | 5,000 light infantry (+80.6) | 692 | 747 |
| H15 | 15,000 heavy infantry (+250.6) | nothing | 692 | 666 |
| M15 | 4,000 light + 3,000 heavy infantry, 2,000 archers, 1,000 light + 1,000 heavy cavalry (+250.6) | nothing | 692 | 666 |

- **Driver and script:** `Game.attack_fleet(1, 0)`; `t3_trials.py` reads both fleets and both armies from game memory before and after (`army_state`), saves seed 1 of each cell. `python3 runs/experiments/fleet-battles/t3_stage.py build` writes the eight fixtures.

## Observations

Saves (`NBC_<cell>_seed1.SAV` for every cell and `NBC_M15_seed2`, `NBC_M15_seed5` (the units after a heavy and a medium loss), and one more of the other outcome: `NBC_L5_seed8` (the only L5 win), `NBC_L10_seed2`, `NBC_L15_seed10`, `NBC_A5_seed10`, `NBC_L15D5_seed2` (losses); L25 has no loss to save; the extra saves are re-runs of those seeds, which reproduced the original outcome and losses exactly), the six fixtures, `t3_trials.json` and the log are in the release [`run-exp-naval-battle-cargo`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-naval-battle-cargo) (indexed in [`evidence-index.md`](../evidence-index.md)).

| cell | attacker wins | the formula (`/50`, random 0–30 % on both sides) expects | fraction of ships the winner lost | the winner's army lost |
|---|---|---|---|---|
| L5 | **1** / 10 (seed 8) | 0.004 | 0.300 | all (5,000 → 0) |
| L10 | **3** / 10 (seeds 1, 4, 8) | 0.22 | 0.229–0.271 | all, all, 61 % |
| L15 | **9** / 10 (not seed 10) | 0.63 | 0.171–0.300 | 47–59 % in three, all in six |
| A5 | **9** / 10 (not seed 10) | 0.63 | the same, seed by seed | 46–59 % in three, all in six |
| L25 | **10** / 10 | 1.00 | 0.100–0.214 | 30–62 % in all ten |
| H15 | **9** / 10 (not seed 10) | 0.63 | 0.171–0.300 | the same fractions as L15, seed by seed |
| M15 | **9** / 10 (not seed 10) | 0.63 | 0.171–0.300 (same as L15) | a remnant in 8 of 9 (see below), nothing left in one |
| L15D5 | **5** / 10 (seeds 1, 4, 5, 7, 8) | 0.25 | 0.214–0.314 (attacker wins); 0.233–0.278 (the 5 defender wins) | attacker's army: all in four, 59 % in one; defender's army (5,000): all in the five defender wins |

**Seeds share draws across cells.** Seeds 2, 3, 6 and 9 gave the same winner's loss (ships 70 → 49) in L15 and A5, and seeds 1 and 4 the same loss to each other within L10 (70 → 51), L15 and A5 (70 → 55): the random draws are tied to the seed, not to the cell (the T2 finding noted the same).

**L15 and A5 are the same battle.** For every seed the attacker's ships and condition after, the army's loss fraction of the three survivors in `A5` (0.585, 0.559, 0.464 against 0.589, 0.559, 0.472) and the winner agree, though one army is 15,000 men of one kind and the other 5,000 archers.

**The winner's army.** Over the 51 won battles of single-unit armies (46 attacker wins, the 5 defender wins of L15D5; M15 is below), the army's loss fraction against the winner's loss of ships `f`:

| `f` of ships | battles | the army lost |
|---|---|---|
| 0.100–0.129 | 3 | 0.298–0.381 (2.8–3.0 × f) |
| 0.157–0.186 | 9 | 0.442–0.531 (2.7–2.9 × f) |
| 0.214 | 8 | 0.559–0.623 (2.6–2.9 × f) |
| 0.229 | 1 | 0.609 (2.66 × f) |
| 0.233–0.314 | 30 | **1.000 (all)** |

(The 0.214 and 0.229 rows are single values of f.) Morale after: unchanged in every case (67 for Ptolemaic's army 7, 65 for Carthage's army 2 in the five defender wins of L15D5); a winning attacker's moves 0, a winning defender's unchanged.

**The mixed army** (M15, seeds as L15): the winner and its ships and condition lost are the same as L15's in every seed, but the army aboard is not lost whole: troops left of 11,000 at `f` = 0.171, 0.214, 0.214, 0.243, 0.243, 0.300, 0.300, 0.300, 0.300: 5,248; 4,280; 4,475; 1,458; 1,766; 528; 436; 700; 0. In the three saved cases the units differ: at 0.214 (seed 1, `NBC_M15_seed1.SAV`) light infantry 4,000 → 1,660, heavy infantry 3,000 → 1,310, archers 2,000 → 895, heavy cavalry 1,000 → 415 and the light cavalry gone; at 0.300 (seed 2) only 528 archers remain; at 0.243 (seed 5) 614 archers and 844 heavy infantry. So the casualties fall **unit by unit**, each unit losing about the same fraction (55–59 % at 0.214, a multiple of 2.6–2.7 × f) up to all of it, and the light cavalry (the smallest unit, 1,000) first; a one-unit army of 15,000 loses it all at the same `f` where a mixed one loses 84–100 % in total, so the all-or-nothing rows above describe single-unit armies, not armies in general.

**The defender with cargo** (L15D5, seeds 2, 3, 6, 9, 10): the defender won, lost 0.233–0.278 of its ships and its army (5,000) went to 0 in each; and Carthage's 33,900-man army 2, **not** aboard in the other five cells, was untouched in all 50 battles of those cells (33,900 → 33,900).

## Inferences

- The cargo term is real and of the formula's order: 5,000 light infantry turn 0 of 10 into 1, 15,000 into 9, 25,000 into 10, and the archers' triple weight is exactly what the siege formula gives (same strength, same outcome seed by seed).
- **Size of the effect.** The attacker won more than the formula expects at L15/A5 (9 of 10 against 0.63: the chance of 9 or more is about 7 %) and L15D5 (5 against 0.25: about 8 %), and L5 won once (0.4 % expected: about 4 % for one or more). A Monte-Carlo with a divisor `k` in `siegeStrength / k` gives the highest likelihood at **k = 40** (log-likelihood −23.9 against −30.5 at k = 50, −35.9 at 30 and −42.3 at 60), counting the defender's cargo with the same `k`. This is a **post-hoc fit to six cells of ten that share their random draws (L15 = A5)**, not a measurement: `/50` is not excluded, and the tie to the seed's draws means the cells are not independent samples.
- **The winner's casualties:** a third of the damage goes to the ships and **about three times that fraction to the soldiers aboard, capped at all of them**; in a close fight the whole army is lost (`f` ≥ 0.233 in all 30 single-unit armies; not in a mixed one). A large cargo adds more strength than the ships' own 441, but the winner pays for it in a close fight. The jump between 0.229 (61 %) and 0.233 (all) is **sharp and unexplained**: a multiple of 2.6–3.0 would give about 0.65 at 0.233 (one of the two cases is a defending army, the other an attacking one).
- For play: an army aboard is both the strongest single lever on a naval battle (25,000 men turned a 0.66 ratio into a win in 10 of 10) and a risk: the army dies with its fleet, and the winner's army is wasted by about half to all of it.

## What this does not establish

- **A natural cargo:** every cargo here is edited into the save. The edit reproduces a natural embark except for 3 unexplained bytes, but no battle was fought from a naturally embarked fleet (the fleets still had the moves a boarded fleet would not).
- **Quality, morale and more mixtures:** every unit is of average quality at one morale; one mixed army (M15) was tried, with one composition; cavalry alone was not.
- **Plan acceptance not fully met:** the plan asked for a win and a loss saved per cell (done except L25, which never lost) and for a heavy-infantry or mixed cell (done afterwards: H15 and M15). The cargo is synthetic where the plan wanted natural staging; the player is asked to accept that deviation in the review of this PR.
- **Both fleets in the real order of a game**: one fixture, worn unsupplied fleets, calm sea, one pair.
- **The cargo's effect on moves** (`troops/100/ships + 1` fewer): not measured here. The natural embark save has the cargo aboard and could be ended a turn to read it; not done.
- **The divisor and the 0–30 % term:** see Inferences; 10 seeds per cell with shared draws cannot separate `/40` from `/50` firmly.
- **The sharp loss threshold of the winner's army** (`f` between 0.229 and 0.233) rests on 30 + 21 battles of single-unit armies from seven cargos (the cases at 0.229 and 0.233 are one each); the rule behind it is unknown.
- **Peace prompt, rough sea, storms:** not tested. **Wine-only.**

## Reproduction

```text
setup/setup.sh
python3 -m tests.make_fleet_battle_fixture                         # the T1 fixture (or use saves/fleets-adjacent-at-sea-0723.SAV)
python3 runs/experiments/fleet-battles/stage_cells.py              # FIX_P / FIX_C (see the T2 finding)
python3 runs/experiments/fleet-battles/t3_natural_embark.py        # the natural embark, for the edit check
python3 runs/experiments/fleet-battles/t3_stage.py check           # the edit against it
python3 runs/experiments/fleet-battles/t3_stage.py build           # the eight cargo fixtures
python3 runs/experiments/fleet-battles/t3_trials.py                # 80 battles, about 80 minutes
python3 runs/experiments/fleet-battles/t3_analysis.py              # the win table, the winner's army table, the divisor fit
```

## Review notes (research repository, 2026-10-03)

- **Saves and results retrieved.** `t3_trials.json` (80 trials, 0 errors) and the saves are in the release [`run-exp-naval-battle-cargo`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-naval-battle-cargo). `scripts/naval-cargo-check.py` reproduces the draft's win counts per cell (1, 3, 9, 9, 10, 5, 9, 9 of 10) and the win, loss and "all of it" counts of the winner's-army table (30 destroyed and 21 partial among the one-unit armies); it also confirms that A5, H15 and M15 give the same winner, ships and condition as L15 in all 10 seeds. The stages, clicks and the unit-by-unit records inside the saves beyond what `trials.json` holds were not re-checked.
- **The edit check's 3 unexplained bytes are the unit-map view origin.** `T3_NATURAL_EMBARK.SAV` and `T3_EDIT_CHECK.SAV` differ in exactly offsets 112522, 112526 and 112528, and parsed with the bot's parser the only field that differs is Carthage's (the current nation's) view: [41, 55] after the natural embark, which scrolled the map to the army, against [89, 74] in the edited save. That is the nation record's `+0x488`/`+0x486` pair described in [2026-09-29-nation-view-origin-and-unit-map-clicks.md](2026-09-29-nation-view-origin-and-unit-map-clicks.md). So the positional and staging part of the edit is **identical to a natural embark apart from the view**, which strengthens the draft's check; the part that rewrites the units (sizes, types) was still not compared with a natural save.
- **Siege strength weights only archers**, as the draft found: 15,000 heavy infantry (H15) and the mixed 11,000 men (M15) both have a siege-weighted 15,000 and fought exactly as 15,000 light infantry did, seed by seed. That is the bot's reading of `FUN_0044A930` (`state/sav.py`), now supported by three cells that agree; the function itself was not re-read here.
- **Still true as the draft says:** the cargo is a synthetic edit (the fleets kept their 24 moves), calm sea, one fleet pair, one seed range, Wine-only; quality and morale were not varied, one mixed composition was tried, and the cargo's effect on moves is untested.
- **Not re-run.** No code address was re-read from the executable (no Ghidra dumps in this review).
