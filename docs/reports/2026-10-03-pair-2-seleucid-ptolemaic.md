# Pair 2 (Seleucid + Ptolemaic): a non-Roman nation builds a fleet at Issus in 12 turns, a fleet next to its own city cannot be attacked, and fresh supplied fleets fight as the strength formula says

**Status:** promoted from the `ic2-conquest` draft of the same name (branch `experiment/pair2`, commit `ff9e99a`), **with two explanations added at promotion (next block)**. **Wine-only: every result below is a candidate until the desktop original confirms it.** It is "pair 2" of `docs/proposals/fleet-battles-and-storms.md` §5 (Seleucid + Ptolemaic, both human, seed 12345), after pair 1 ([2026-10-02-fleets-sail-and-drift.md](2026-10-02-fleets-sail-and-drift.md), [2026-10-02-naval-battles.md](2026-10-02-naval-battles.md)). Everything is **natural** (no save edited). 20 battles, 10 seeds in each of two cells; one staging run.

> **Added at promotion (research repository).**
> 1. **The "draw follows the role" inference is established, and it is the code.** [decompiled-diplomacy-peace-terms-and-instant-battles.md](decompiled-diplomacy-peace-terms-and-instant-battles.md) reads from code that the attacker's `Random(4)` is drawn first and the defender's second. With the exact integer rule (a 0/10/20/30 % bonus, ties to the defender, see [2026-10-02-naval-battle-random-term.md](2026-10-02-naval-battle-random-term.md)), a **single pair of bonuses per seed reproduces both cells' winners and their exact damage in all 10 seeds** (six seeds identify the pair uniquely: (3,1) for seeds 1 and 4, (3,2) for 5 and 7, (3,0) for 8, (2,3) for 10; in seeds 2, 3, 6 and 9 the pair is any `(k, k)`). Draws attached to the **fleets** explain only 4 of the 10 seeds, those same `(k, k)` ones. That checks the draft's assumption that both fixtures start the battle from the same random stream (`scripts/naval-pair2-check.py`), and it makes the draft's caveat unnecessary. The same pair recurring across seeds (1 and 4, 5 and 7) agrees with the earlier observation that several seeds give identical draws.
> 2. **The expected rates are the exact rule's, not the continuous model's.** The draft's 0.27 and 0.73 use the continuous `1 + U(0, 0.3)` factor that the random-term report corrects. With the code's integer rule the attacker wins **0.375** (Seleucid, 582 against 623) and **0.625** (Ptolemaic, 623 against 582) of the time, i.e. 3.75 and 6.25 of 10; the observed 5 and 9. Nine or more of 10 at 0.625 has a chance of about 6 %, and the two cells share their seeds (their draws are the same pairs), so the 14 attacker wins of 20 are not independent evidence of an attacker lean. Nothing here contradicts the rule.

**Answer.**
- **Build fleet works for a nation that is not Rome, with no refusal:** Seleucid's order for 60 ships (turn 0720, its own seat 4) said "The fleet will be built at **Issus**"; the fleet appeared at **0732, twelve turns later**, at (219,55) next to Issus with **0 moves, supplies 50, condition 100** and the news "Seleucid finishes a new fleet at Issus." (the countdown 24 falling by 2 a turn, as for Rome).
- **A fleet next to its own city cannot be attacked.** With Ptolemaic's fleet adjacent to Seleucid's new fleet, which was **adjacent to Issus** (219,55) against (220,54), the attack click opened a box whose text was read as "You cannot attack a fleet docked at its own city !" (the read of the box has garbled letters; the message is the one the research reports quote) and nothing changed. After Seleucid moved the fleet **3 tiles from Issus** the same click was allowed (the 20 battles below).
- **The strength formula decides these battles as in pair 1:** with both fleets **supplied** (170 and 190 tons) and condition 97 and 89, Seleucid attacking (strength 582 against 623) **won 5 of 10**, Ptolemaic attacking (623 against 582) **won 9 of 10**; the formula with `1 + U(0, 0.3)` on each side expects 0.27 and 0.73. The loser always sank whole (20 of 20) and the winner lost 0.157 to 0.317 of both ships and condition by one fraction.
- **The random draw seems to follow the role, not the fleet** (an inference, see the assumption below): in five seeds (1, 4, 5, 7, 8) the **attacker** won in **both** cells, so Seleucid won when it attacked and Ptolemaic won when it attacked, with the same seed; in seeds 2, 3, 6 and 9 Ptolemaic won in both roles (Seleucid's attack lost), and in seed 10 the defender won in both (Ptolemaic when attacked, Seleucid when attacked by Ptolemaic). A draw tied to the fleet could not have produced the flips. (This assumes the two fixtures start the battle from the same random stream for a given seed: the generator is seeded at program start and loading a save does not reseed it, [2026-09-29-loading-a-save-does-not-reseed.md](2026-09-29-loading-a-save-does-not-reseed.md), so the stream does not depend on the fixture; a direct check across the two fixtures was not made, so this is an **unestablished inference**.)

## Method

- **Build and seed:** `Imperial Conquest 2 fast rollingsave seed.exe` (SHA-256 `354d8265…532f`), Wine 9.0, Xvfb. New Game with rows 2 (Seleucid) and 3 (Ptolemaic) human, seed 12345 (`SEED.TXT`): the turn order of the seed puts Ptolemaic first (seat 2) and Seleucid second (seat 4) in each round; both start at war (relation 3, as in each one's own start, [2026-10-02-start-as-each-nation.md](2026-10-02-start-as-each-nation.md)). Treasuries 4,900 (Ptolemaic) and 2,700 (Seleucid). Scripts `runs/experiments/pair2/phase1.py`, `phase2.py`, `trials.py`.
- **Phase 1** (`P2_0720_s02_Ptolemaic.SAV` … `P2_0732_s02_Ptolemaic.SAV`, every seat's autosave copied at once): at its first turn Ptolemaic sailed its fleet (70 ships, condition 75, (189,89)) 4 tiles to (189,93) next to Alexandria, **repaired it to 100** (`repair_fleet`) and **supplied it** (400 tons, 80 → 480); Seleucid ordered 60 ships; both then only ended turns for twelve turns.
- **Phase 2** (from `P2_0732_s02_Ptolemaic.SAV`): Seleucid supplied its fleet (50 → 350 tons) and stayed at Issus; Ptolemaic supplied again (400 tons) and sailed to it (38 tiles: 25 + 13 in two turns, along the sea planner's path); at 0734 Ptolemaic tried the attack next to Issus (refused); Seleucid then sailed out to (217,56) (3 tiles from Issus) and Ptolemaic, at (218,56), ended its turn adjacent. The autosaves at turn 0735, `FIX_S2_seleucid_seat_0735.SAV` (Seleucid's seat: it attacks) and `FIX_S2_ptolemaic_seat_0735.SAV` (Ptolemaic's seat: it attacks), are the fixtures.
- **Trials** (`trials.py`): load a fixture with the seed, read both fleets, `Game.attack_fleet(attacker, defender)`, read both again; one process per seed, seeds 1 to 10 in each cell. Cells: **S** Seleucid 60 × 97 attacks Ptolemaic 70 × 89 (strengths 582 v 623, ratio 0.93); **P** Ptolemaic 70 × 89 attacks Seleucid 60 × 97 (623 v 582, ratio 1.07).

## Observations

Saves (every seat's autosave of both phases, the two fixtures, `P2B_S_seed1.SAV`, `P2B_P_seed1.SAV`), `trials.json` and the logs are in the release [`run-exp-pair2`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-pair2) (indexed in [`evidence-index.md`](../evidence-index.md)).

**Build and launch** (`P2_phase1_log.json`): Seleucid's treasury was 2,700 at its seat and 2,100 at the next round (a cost of about 600 talents for 60 ships, mixed with one round's income). The fleet record had countdown 8 at 0728, 6 at 0729, 4 at 0730, 2 at 0731 and was launched at **0732** (`P2_0732_s02_Ptolemaic.SAV`): (219,55), 60 ships, condition 100, supplies 50, moves 0. The next turn it had 29 moves (formula for 60 ships: 30 − 1 = 29).

**Ptolemaic's docked fleet:** repaired to 100 at 0720; supplies fell to 0 by 0728 (480 − 70 a turn) and condition fell to 99 (0729) and 98 (0732), the out-of-supply term; docked next to Alexandria no storm hit it.

**The docked-fleet refusal** (`P2_0734_s02_Ptolemaic.SAV`, `phase2.log`): `attack_fleet` left a box read as "You cannot attack a fleet docked a its awn city! aK" (the box read by the driver's text reader; the reading is garbled) and neither fleet changed; the fleets were adjacent and Seleucid's fleet was adjacent to Issus. "Docked" is therefore **within one tile of an own city**, not on the city's tile.

**The 20 battles** (`trials.json`):

| cell | attacker wins | formula expects | winner's ships lost (fraction) | winner's condition lost (fraction) |
|---|---|---|---|---|
| S: Seleucid attacks, 582 v 623 | **5** / 10 (seeds 1, 4, 5, 7, 8) | 0.27 | 0.217–0.317 | 0.216–0.320 |
| P: Ptolemaic attacks, 623 v 582 | **9** / 10 (not seed 10) | 0.73 | 0.157–0.317 | 0.157–0.320 |

In every battle the loser's fleet was destroyed and the winner's ships and condition fell by the same fraction (within 0.01). The winning attackers (14) ended with 0 moves and their supplies unchanged (170 and 190 tons). In seeds 2, 3, 6 and 9 the winner was Ptolemaic in both cells and ended with the same 50 of its 70 ships (condition 64), as defender in S and as attacker in P.

## Inferences

- Pair 2 behaves like pair 1: the same formula, the same sinking, the same single loss fraction. **Fresh, supplied fleets of unequal size and condition fit** `ships × condition / 10` with the random 0–30 % on each side: 5 and 9 against 0.27 and 0.73 are an 11 % and a 20 % one-sided tail of one cell each, and together 14 attacker wins of 20 (expected 10) has about a 6 % chance (`runs/experiments/pair2/analysis.py`; the two cells share their seeds, so they are not independent samples), the same mild attacker lean that [2026-10-02-naval-battle-random-term.md](2026-10-02-naval-battle-random-term.md) found settled as no attacker bonus with 160 battles. The symmetric random term is not contradicted.
- The seed flips are what a draw attached to the **role** gives (attacker's random factor and defender's random factor per seed, in order of the battle), as a symmetric model would use; it also means two cells with the same seeds are not independent samples.
- For play: **a fresh fleet at its port is safe from attack**; it must sail more than one tile from every own city to be attackable, and a nation's built fleet can be kept at port as long as its owner wants. For staging: pair 2 needs 12 turns of waiting and 38 tiles of sailing (about 20 minutes of game time).

## What this does not establish

- **One seed's world, one pair of fixtures**, both fleets supplied; conditions 97 and 89 only. No equal-condition cell, no zero-supply comparison with this pair (supplies were not varied; T2's pair had both at 0).
- **The peace prompt for fleets** ("Are you sure you want to attack this fleet ?") was not tested: the nations were already at war from the start.
- **The refusal's exact distance** (within one tile, including diagonal): tested at one geometry, Seleucid's fleet diagonal to Issus; whether a fleet one tile from the city's other sides, or two tiles away, is refused was not tried (the attack at 3 tiles was allowed).
- **The cost of the fleet** (about 600 talents for 60 ships) is read off treasuries that include income and other spending, not from a before and after of the order alone.
- **No natural interference** from AI fleets or Bithynia and Galatia was seen in the staging; that is one run.
- **Wine-only.**

## Reproduction

```text
setup/setup.sh
python3 runs/experiments/pair2/phase1.py     # Seleucid builds, Ptolemaic docks; to the launch (about 45 minutes)
python3 runs/experiments/pair2/phase2.py     # the meeting, the refused attack, the two fixtures (about 15 minutes; re-run once and the fixtures came out byte for byte identical to the first run's)
python3 runs/experiments/pair2/trials.py     # 20 battles (about 25 minutes)
python3 runs/experiments/pair2/analysis.py   # expected rates, tails, the per-seed winners
```

## Review notes (research repository, 2026-10-03)

- **Saves and results retrieved and re-read** (the release [`run-exp-pair2`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-pair2), with the bot's parser). Seleucid's fleet is under construction with countdown 2 at 0731 and launches at 0732 at (219,55): 60 ships, condition 100, supplies 50, moves 0, a tile from Issus at (220,54). The two fixtures at 0735 read Seleucid 60 ships, condition 97, 170 tons at (217,56) and Ptolemaic 70, 89, 190 tons at (218,56), at war, as the draft says. All 20 trials: winner and exact damage fit some bonus pair (20 of 20). The refusal box, its garbled text, the cost of the fleet (about 600 talents, read off treasuries that include income) and the 29 moves the turn after launch are not in the files checked here.
- **The refusal fits a predicate the code reports already have.** [decompiled-map-code1-overlay.md](decompiled-map-code1-overlay.md) decompiles `FUN_004494e4`, which returns an own city within the clamped 3×3 around a fleet and is the test the storm pass uses for "next to its own city". The draft's observation (refused with the fleet diagonal to Issus, allowed 3 tiles away) is the same predicate; that the attack check calls this very function is not read from the code here.
- **Consistent with no contradiction:** the 12-turn build and the countdown falling 2 a turn, the siege-free sinking of the loser, one loss fraction for ships and condition, the formula for fleet moves (60 ships: 29).
- **Not re-run.** No code address was re-read from the executable (no Ghidra dumps in this review).
