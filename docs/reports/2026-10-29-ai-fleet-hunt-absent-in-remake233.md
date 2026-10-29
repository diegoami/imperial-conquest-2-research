# An AI fleet at war hunts and sinks a nearby enemy fleet in the original; in the remake it stays in port

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `9ae4367` (PR #237),
conquest [#233](https://github.com/diegoami/ic2-conquest/issues/233) (tracker #228). Release
[`run-exp-diff084-stats`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-stats);
the save SHA-256s are committed at `runs/experiments/data/run-exp-diff084-stats/SAVES.sha256`.
Wine-only. Remake **v0.8.4** (`d9cc71bc82e22ad1d3d7c373c3d80d61ed0bcbeb`), `classical-faithful`.
The pre-registered scenario `storm30` (`difftest/cases/stats233.py`) found this difference; it was
designed to measure storm damage.

**Tag:** `[confirmed, partial]`: 30 seeds in each game, one start state, Wine. The original's hunt
matches its decompiled scorer `[confirmed: decompile]`, as recomputed below. The remake-side cause
is not established.

**Review note (2026-10-29):**
- **Release integrity:** the archive was downloaded and all 582 saves match `SAVES.sha256`.
- **Every trial re-read** with my own reader: `a001` (after the sail) and `a002` (after End turn)
  of all 60 `storm30` and 60 `storm30b` trials.
  - **`storm30`:** Rome's fleet is at (97,48) in all 60 `a001` saves. It survives the End turn in
    0 of 30 original trials and 30 of 30 remake trials. Carthage's fleet stands at (98,49) after the
    turn in 30 of 30 original trials and 0 of 30 remake trials.
  - **`storm30b`:** Rome and Carthage start at peace in every trial. Carthage is at war with Rome
    after the turn in 4 original trials (seeds 9, 18, 21, 27) and 5 remake trials (seeds 3, 6, 12,
    13, 23). Its fleet hunted in all 4 original wars and in none of the 5 remake wars.
  - **Storm damage** of the surviving Rome fleets: original mean 3.35 (17 × 3, 9 × 4, n = 26),
    remake 3.60 (12 × 3, 18 × 4, n = 30). In `storm30`'s remake trials it was 15 × 3 and 15 × 4.
  - Everything above matches the draft.
- **Statistics corrected.** The draft quotes Holm p = 0.0012. That is from the first analysis
  (`analysis-20261029-014718.txt`, 13 tests). The final analysis (`analysis-20261029-021154.txt`,
  17 tests) gives raw p = 0.0001 and Holm p = 0.0016 for `fleet_survives`. The raw value is the
  floor of a 10,000-permutation test. With 0/30 against 30/30 and no overlap, the difference is not
  in doubt.
- **The original's choice is what its scorer predicts.**
  [`2026-10-09-ai-intercept-and-fleet-hunt-in-play.md`](2026-10-09-ai-intercept-and-fleet-hunt-in-play.md)
  gives the scorer (`FUN_0044f4f8`, called from `FUN_0044f608`): strength
  `ships×condition/10` plus jitter, score `my×100/their − d`, doubled when `their < my` and `d < 18`,
  hunt above 100.
  - Carthage has 90 ships at condition 100, a strength of about 900. Rome has 30 at 97, about 291.
    The distance is 14–15.
  - That gives a score of about 294, doubled to about 590, far above the threshold under any jitter.
    This is my arithmetic; the conquest run had no hook.
- **What the remake source shows (v0.8.4, static).**
  - No source file under `src/` references the original's hunt routines (`FUN_0044f608`,
    `FUN_0044f4f8`).
  - `src/IC2.Engine/Ai/AiMilitaryPhase.cs` has a generic `ProposeFleetMarches` candidate, which
    sails a fleet at an enemy fleet, plus an adjacent-only `attack-fleet` candidate gated on
    `IsAtWar`.
  - I did not determine why that march candidate was not chosen here: its scoring, or whether
    `classical-faithful` runs it. This is the draft's own open question.
- **Overlap.** This fits the earlier reports, with no contradiction:
  - [`2026-10-09-ai-intercept-and-fleet-hunt-in-play.md`](2026-10-09-ai-intercept-and-fleet-hunt-in-play.md)
    describes the original hunt;
  - [`2026-10-22-manual-gaps-disband-purchase-storm-ai-war.md`](2026-10-22-manual-gaps-disband-purchase-storm-ai-war.md)
    covers the AI's war declaration on a human seat;
  - [`2026-10-24-strategic-fleet-controls174.md`](2026-10-24-strategic-fleet-controls174.md) and
    [`2026-10-24-fleet-accepted-movement174.md`](2026-10-24-fleet-accepted-movement174.md) compared
    fleet decisions on synthetic inputs at older remake pins. They did not run a live hunt at
    v0.8.4.

## Answer

The start is `saves/fleet-port-antium-0734.SAV`: Rome human, Autumn week 5, 270 BC, with Rome and
Carthage at war. The order: Rome's fleet 2 (30 ships, condition 97, empty) sails from Antium
(101,46) to open calm sea at (97,48). Then End turn.

| | Original (startup seeds 1–30) | Remake (state seeds 1–30) |
|---|---|---|
| Carthage's fleet (90 ships at (110,63)) | sails to (98,49), next to Rome's fleet, and attacks | does not move (stays at (110,63), condition 100) |
| Rome's fleet survives the turn | **0 of 30** (all 30 ships lost) | **30 of 30** (0 ships lost; condition −3 or −4) |

The permutation test gives p = 0.0001, Holm-corrected 0.0016 over the final analysis's 17 tests,
and the samples do not overlap at all. In the original, Carthage's fleet loses 3 ships in the battle
and falls to condition 93 (seed 1, from the draft).

The original's behaviour is its documented AI fleet hunt. In the remake, the same state, with
Carthage at war with Rome, never produces a hunt.

## A second scenario repeats it after an AI declaration of war (`storm30b`)

`storm30b` gives the same order from a staged copy in which Rome and Carthage are at peace. It was
pre-registered to measure storms. During the End turn, Carthage's AI declared war on Rome in
**4 of 30** original trials and **5 of 30** remake trials. That rate is consistent between the games
and with the documented `Random(10) == 0` gate. After the declaration:
- **original (4 of 4):** Carthage's fleet sailed to (98,49) and sank Rome's ("Carthage sinks fleet
  of Rome.");
- **remake (0 of 5):** no hunt, and Rome's fleet survived.

This was observed after the run and was not one of `storm30b`'s pre-registered metrics. The original
seeds are 9, 18, 21 and 27 (`storm30b/original-s<seed>/a002.SAV`, turn 0735).

## What this does and does not establish

- **Established:** for this state, the remake's AI does not hunt a reachable enemy fleet at sea,
  while the original's does in every seed. A remake player can therefore leave a fleet at sea next
  to a hostile navy without the loss the original inflicts.
- **Not established:**
  - whether the remake ever hunts, at other distances, fleet sizes or nations;
  - which step differs: the scorer, its eligibility, the candidate choice or the movement.
- **Storm damage:** `storm30` could not compare it, because no original fleet survived. `storm30b`
  measured it: condition lost 3.35 (original, 26 surviving fleets) vs 3.60 (remake, 30), Holm
  p = 1.0, consistent.

## Evidence

The data is in `runs/experiments/data/run-exp-diff084-stats/`:
- `trials.jsonl` has one line per trial. Its first 30 `naval30` remake lines are a metric bug, kept
  in the file and re-run.
- `analysis-*.json` and `.txt` hold the tests, and each trial has its own `receipt.jsonl`.

The saves are in release `run-exp-diff084-stats`:
- `storm30/original-s1/a001.SAV` (turn 0734, after the sail: Rome's fleet at (97,48));
- `storm30/original-s1/a002.SAV` (turn 0735: Carthage's fleet at (98,49), Rome's gone);
- `storm30/remake-s1/a002.SAV` (Rome's fleet at (97,48); Carthage's at (110,63));
- the same names for seeds 1–30, and likewise for `storm30b`.

The original build is `Imperial Conquest 2 fast rollingsave seed.exe` (SHA-256 `354d8265…`),
under Wine 10.0.
