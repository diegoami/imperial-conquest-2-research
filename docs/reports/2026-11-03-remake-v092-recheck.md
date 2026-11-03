# Recheck on remake v0.9.2 (1723c673): four fixes confirmed, a regression in the launch fix, and the stale walk word at −1 in play

**Tag:** `[confirmed: remake replays against the stored original games; Wine hooks (inert) + code in both games]`. Wine only.
**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `2ec0ca26` (PR #320).
**Task:** owner 2026-11-03, "ok we have a new release, 0.9.2".

**The release.** Remake `v0.9.2` = main `1723c673` = `0d9d4729` + 3 commits:
- **`36ab15ec`, T274 + fix 1739:** the Faithful trade order (D3, #1732) and the full move budget before the no-command
  garrison fallback;
- **`1723c673`, T275:** the resupply ties and the fleet launch placement;
- **`1c21cd4b`:** evidence only.

**Not touched:** `AiCapitalDefence` (capital defence while a human battle is pending) and `CoastalCity.FleetBuildCity` (the
Caspian build city).

## 1. Anchored replay of the six stored long games (265 turns)

`python3 -m difftest.anchored <game> --pin 1723c673 --out anchored-1723c673`: Rome, Carthage, Gaul and Seleucid
(`run-exp-longrun-v090`), Ptolemaic and Macedonia (`run-exp-longrun-v091`). No remake error. The comparison with the
v0.9.1 replays is in `anchored-1723c673-vs-0d9d4729-v1.txt`.

| Game | Position nation-turns, v0.9.1 → v0.9.2 | Gone | New |
|---|---|---|---|
| Rome | 22 → 19 | Seleucid fleet t24, Numidia fleet t30 (launch); Ptolemaic t24; Thracia fleet t36 | Seleucid fleet t36 (§2) |
| Carthage | 30 → 22 | launch rows t18 and t30; Seleucid t20 and t23; Bithynia t22; Ptolemaic t24; Media t39 | — |
| Gaul | 29 → 25 | Seleucid fleet t18, Numidia fleet t30 (launch); Ptolemaic t24; Celtiberia t25 (tie); Thracia fleet t36 | Seleucid fleet t30 (§2) |
| Seleucid | 11 → 10 | Celtiberia t24 (tie) | — |
| Ptolemaic | 15 → 8 | all 3 no-command fallback rows and the Bithynia row that followed; both ties; both launches | Carthage t16 (a draw, §4) |
| Macedonia | 33 → 25 | Carthage t26 (fallback); Seleucid t19 and Celtiberia t24, t31 (ties); launch t18 and t30; Illyria and Seleucid t22; Seleucid t26 | Seleucid fleet t30 (§2) |

**`stays.py`** (`stays-1723c673-v1.txt`):
- The Ptolemaic Galatia t1 and Macedonia Carthage t26 rows are gone: the no-command fallback is fixed.
- 8 rows remain, all from the first four games and as on v0.9.1: the four war-declaration rows and the four fleet rows
  (Alexandria port ×3, gap C; the Utica hunt).

**Still as on v0.9.1, not addressed by this release:**
- the four Media Caspian fleet rows (Macedonia t19, 25–27);
- the capital-defence rows (Ptolemaic t1, Seleucid and Bithynia);
- gap C at Salamis (Macedonia t23).

**Per-turn counts:** every changed turn has fewer differences, except the regression in §2 and three Ptolemaic turns whose
map-cell count grows (t1 545 → 963). The sampled cells there are all calm against rough sea (0/1): the release changes how
many draws the remake consumes, so the weather pattern moves. That is not a rule difference.

## 2. Regression: the launch fix ignores units on the map (3 rows)

T275's `CoastalCity.LaunchTile` scans `world.Terrain` (static terrain, `cells[...] is 0 or 1`). The original's
`FUN_0044939c` reads the live map, where a unit's marker replaces the code: [placement and Macedonia](2026-11-03-placement-and-macedonia-longrun.md) (research PR #186), "the launch scan reads the live
map". T275 cites research `bc8d720`, which is earlier.

**Gaul game, turn 30** (start `t29`): Seleucid's fleet 2 stands on (219,55), and the new fleet 5 at Issus launches.

| | Fleet 5 (new) | Fleet 2 |
|---|---|---|
| original | (219,54): (219,55) holds fleet 2's marker | sails to Antioch (220,65) |
| v0.9.1 (row-major first) | (219,54) | (220,65): matched |
| **v0.9.2** | **(219,55)**, on fleet 2's tile | (219,54), 2 moves left, does not sail |

The same row appears in the Rome (t36) and Macedonia (t30) games. **Fix:** use the live map code, `OriginalFleetPort.MapCode`
(fleets 300, armies 200, cities 20), in `LaunchTile`.

## 3. The registry is unchanged

`python3 -m difftest.recheck 1723c673 --version v1` (`run-exp-recheck-1723c673/report-v1.json`): unchanged 113, FIXED 11,
REGRESSED 11, CHANGED 4, row for row identical to v0.9.1 and v0.9.0.

## 4. Harness: anchored replays drew the same random streams every turn

The remake's importer gives every imported save the scenario's fixed `RandomSeed` and `TurnIndex` 0
(`OriginalSaveImporter.cs:470, 554`). The AI's rolls draw from streams keyed by nation and `TurnIndex`, for example
`ai.ownDiplomacy.warRoll:{nation}:{turn}` (`AiMilitaryPhase.cs:201`). `difftest/anchored.py` passed no seed, so **every
anchored turn replayed the same draws**: a roll that hit once hit in every turn where the same candidate existed.

**Seen in the new Numidia game** (§5): Seleucid "declares war on Armenia" (Media is drawn in through the alliance) in turns 9,
10 and 11. That is 3 hits in a row for a 1-in-10 roll, giving 9 stay rows.

**Fix:** `anchored.py --turn-seed B` replays turn k with seed B + k. On the Numidia game the stay rows go from 12 to 5, and the
remaining war rows (turns 6 and 11) are independent hits. The original's own Seleucid declares the same war at turn 15.

**Consequence for earlier reports:** the "remake-only war declarations" of the v0.9.0 to v0.9.2 anchored replays (for
example Macedonia against Illyria in the Carthage and Gaul games) were rolls, as attributed, but correlated across turns by
this artefact. Their counts are not independent samples.

## 5. A new long game on v0.9.2: Numidia, and the stale walk word at −1 in play

Numidia, rulebot-1, 40 turns, seed 12345, `IC2_LOG_RANDSEED=1` (`run-exp-longrun-v092`). 40 turns played, no game over; the
RandSeed is logged for every action.
- **Classify:** 154 AI relation nation-turns, 27 position, 3 count, 17 draw-only turns.
- **Stays:** 12 rows with the default seed, 5 with `--turn-seed 12345` (`stays-numidia-v1.txt`,
  `stays-numidia-turnseed-v1.txt`). Four of the five are the war rolls of §4. The fifth is new.

**Ptolemaic army 13, turn 37.** It has 10,557 troops at (193,96), next to its own city Naucratis (193,97), and 10 moves.

**Original.** The walk hook `patches/walk_hook.py`, run `hooks-walk-num37-v1`, is inert: its autosave is byte-identical to
the plain build.

| Seq | Walk (caller) | Target | `[ebp-0xa]` | Result |
|---|---|---|---|---|
| 1 | E84C mercenary run (`e913`) | (192,77) | 0 at entry | no direct line → `FUN_0044db38` |
| 2 | the same, no-progress test | | **−1** (DB38 found no intermediate point) | `jle`: no fallback swing; moves stay 10 |
| 3 | the same, recursion test | | −1 | no recursion |
| 4 | EBE8 garrison fallback (`ecd6`), the same stack depth | (193,97) Naucratis | **−1 at entry**, left by the walk above | direct line (CB40 = 1), so the word is not written |
| 5 | the same, no-progress test | | −1 | no swing |

The army stays at (193,96), as in the campaign.

**Remake.**
1. The mercenary run gives no movement.
2. The after-command gate passes, because the army has its full 10 moves.
3. `RunGarrisonFallback` targets Naucratis (193,97), as in the original.
4. Its march (`MoveWalkPolicy.AiContinuation`, `MoveArmyCommandHandler.cs:186–280`) sees no progress and swings to the local
   fallback point: the loop takes that branch "whenever the walk left the moves unchanged and positive".
5. The army ends at (195,97): "garrison fallback moved army-13 to (195, 97)" (`probes/1723c673-num-t37pre`).

**What this adds to [`2026-10-30-ai-move-stale-word-in-play97.md`](2026-10-30-ai-move-stale-word-in-play97.md).** That finding measured the stale word at 49, 71 or 0,
never −1, in 25 turns, so the remake always swings and recurses. Here it is −1. A walk whose `FUN_0044db38` finds no
intermediate point writes −1. A later walk at the same stack depth that takes the direct line (so writes nothing) inherits
it, and skips both the swing and the recursion. Here that is the garrison fallback after the mercenary run in F31C. The
mercenary-run walk itself also skips the swing when its own DB38 returns −1.

**Fix direction:** see the specification in the intake section below.

**A hook caution.** The gap-B hook (`patches/gapb_hook.py`) puts a probe at DBA8's **entry**. Its `pushfd/pushad` writes
where DBA8's frame, and `[ebp-0xa]`, will lie, so the hook can change the stale word. Run `hooks-gapb-num37-v1` is **not
inert** (hooked ≠ plain): with the overwritten word, the original also swings, via (196,99), and ends at (195,97). That run
is kept as a negative control and not used as evidence. Earlier gap-B runs were inert because the stale word did not matter
on their paths. For any walk question, use `walk_hook`, whose probes sit inside the frame.

## Open

- §2: the launch fix needs the live map.
- §5: the stale word's carry-over between walks (fix direction for research and IC main).
- Not fixed in v0.9.2: capital defence while a human battle is pending; the Caspian build city.
- Gap C (the port case).
- Anchored replays from now on should use `--turn-seed`. The six stored games were not re-run with it.

## Evidence

**Data:**
- `runs/experiments/data/run-exp-longrun-v092/`: `stays-1723c673-v1.txt`, `anchored-1723c673-vs-0d9d4729-v1.txt`,
  `numidia-rulebot1-40t` (its `anchored` and `anchored-turnseed`), `stays-numidia*-v1.txt`, `classify-numidia-v1.txt`,
  `hooks-walk-num37-v1`, `hooks-gapb-num37-v1` (not inert, kept), `probes/1723c673-num-t09pre`, `probes/1723c673-num-t37pre`,
  `probes/*-ptol-t16pre`;
- `run-exp-longrun-v090/*/anchored-1723c673`, `run-exp-longrun-v091/*/anchored-1723c673`, `run-exp-recheck-1723c673`.

**Saves:** releases `run-exp-longrun-v092` (`numidia-rulebot1-40t-saves.tar.gz`, `v092-hooks-saves.tar.gz`) and
`run-exp-longrun-v090` / `run-exp-longrun-v091` (`recheck-1723c673-saves.tar.gz`). The Numidia starts are the campaign's
checkpoints before End turn (`decidestarts/num-tNNpre.SAV`).

**Tooling:** `difftest/anchored.py --turn-seed`.

## Intake (research, 2026-11-03)

**Verified:**
- **The remake at `1723c673`:**
  - the commit list;
  - `CoastalCity.LaunchTile` (lines 82–107) runs the ring rule, x outer, with the eastern-zone test, on
    `world.Terrain.Decode`: static terrain, not the live map;
  - `OriginalSaveImporter.cs:470` sets `TurnIndex: 0` and `:554` sets `RandomSeed: scenario.RandomSeed`;
  - `AiMilitaryPhase.cs:201` draws `ai.ownDiplomacy.warRoll:{nation}:{TurnIndex}`.
- **The seed build's disassembly, `FUN_0044dba8`** (0x44DBA8–0x44DCAB):
  - `[ebp-0xa]` is a local that DBA8 never initialises;
  - on the direct path (CB40 = 1, 0x44DC0D) the word isn't written;
  - on the other path, `FUN_0044db38` writes it (−1 first, at 0x44DB47) and the walk to it is skipped when it is ≤ −1
    (0x44DC2C);
  - the no-progress swing (0x44DC4D) and the recursion (0x44DC8C) both skip when it is ≤ −1.
- **The hooks:** `hooks-walk-num37-v1` seq 1–5 match the table in §5, and its `inert.json` records hooked = plain.
  `hooks-gapb-num37-v1`'s records hooked ≠ plain, as the draft says.
- **The data:** the stays file for the turn-seed replay has the 5 rows; the totals in the anchored comparison and the
  recheck counts match the draft.

**Not re-checked:**
- the per-game row lists in §1's table;
- the Gaul t30 launch probe;
- the 0/1 weather reading of the Ptolemaic map-cell growth;
- the claim that E84C's and EBE8's DBA8 frames share an address (the hook shows the value carried over, not the
  address).

The tarballs were not downloaded.

**On the gap-B hook caution:** earlier gap-B runs recorded hooked = plain, so their conclusions stand. But "inert" only
means the autosave matched. A hook at DBA8's entry can change the stale word on paths where it matters, as it did here.

### Specification for the remake: the stale walk word

This is the original's behaviour as far as it is measured. It is not a model of the whole stack.
- **The word:** DBA8 tests an uninitialised local, `[ebp-0xa]`, before its no-progress swing and before its recursion.
  Only DB38 writes it, when the walk takes the intermediate path. When DB38 finds no intermediate point, it leaves −1.
- **Measured:**
  - 25 turns (5 starts × 5 AI End turns): on the direct path the word held 49, 71 or 0, never −1. The walk swings
    and recurses, which is the remake's T239 behaviour.
  - Numidia turn 37, Ptolemaic army 13: the E84C walk found no intermediate point, and the word became −1. The garrison
    fallback's walk, next and on the direct path, read that −1 and did neither the swing nor the recursion. The E84C
    walk also skipped both, on its own −1.
- **Rule for Classical Faithful:**
  - When a walk's intermediate search fails, that walk does no swing and no recursion.
  - When the next walk in the same F31C army pass is the garrison fallback for the same army and takes the direct path,
    it doesn't either.
  - Otherwise, keep T239's behaviour (swing and recurse).
- **Not known:** what the word holds after other sequences, across armies, or across seats. Other stack writes leave 49,
  71 or 0, and the rule above covers only the measured carry-over.

### Method note: anchored replays need a seed per turn

Before `--turn-seed`, every anchored remake turn started from the same random seed and turn index. So the remake's
per-turn AI rolls were the same draws every turn. The remake-only war rows in the anchored replays of v0.9.0–v0.9.2 are
rolls, as attributed, but correlated, so their counts are not independent samples. New anchored replays should use
`--turn-seed`. The six stored games have not been re-run with it.
