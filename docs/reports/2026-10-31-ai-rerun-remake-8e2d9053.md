# The AI comparisons rerun on remake main 8e2d9053: the T250–T252 corrections close every attributed gap

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `44805be` (PR #289), revised
at `1860893` (PR #290), `a982d43` (PR #291, the Galatia attribution) and `beb08f8` (PR #292, the
#144 boundaries), owner
request 2026-10-31, after remake #1650 merged the corrections. It reruns the four equal-state
comparisons on remake main `8e2d9053` ("T250–T252: correct Faithful AI destinations, trade swaps and
recruitment city", not released):
- [AI decisions](2026-10-30-ai-decisions-vs-remake-main.md) (armies);
- [AI diplomacy](2026-10-30-ai-diplomacy-vs-remake-main.md);
- [AI economy](2026-10-31-ai-economy-vs-remake-main.md);
- [AI fleet phase](2026-10-31-ai-fleets-vs-remake-main.md).

The original's side is unchanged: the same hook logs, 16 New Game starts (S00–S15 `*_AUTO0720.SAV`)
× 5 rounds, seed 12345. Each round is replayed in the remake from the original's own round-start
autosave (`hooked-tNN-*.SAV`).
- **Data:** `runs/experiments/data/run-exp-airerun/`, tracked in Git:
  - `remake-8e2d9053-v1/`: 80 replays;
  - `report-aidecide-v1.json`, `attribution-aidecide-v1.json`, `report-diplo-v1.json`,
    `report-econ-v1.json` and `report-fleet-v1.json`;
  - `aborted/`: a first replay that pointed at a folder with no saves; rounds 2–5 failed with "file
    not found".
- **Releases (the original's side):** `run-exp-aidecide`, `run-exp-diplo`, `run-exp-econ` and
  `run-exp-fleetphase`, already in the [evidence index](../evidence-index.md). This rerun adds no
  release.

**Tag:** `[confirmed]`, Wine-only, for the three corrections. Every army row is now explained; the
fleet rows remain open. The #144 boundaries are in this commit too (28 of 30 controls match).

**Review note (2026-10-31):**
- **Release integrity:** I downloaded `run-exp-aidecide` and `run-exp-econ` again. Every file matches
  its `SAVES.sha256`.
- **Comparison reruns:** I ran all four comparers and `aidecide/attribute.py` from a scratch copy of
  conquest main `44805be`, on the committed replays and the release saves. All five outputs are
  **byte-identical** to the committed reports.
- **Remake commit:** `8e2d9053` is remake main, the single commit after `05b02936`. I did not
  re-execute the remake replays, which need the .NET build.
- **Label in the attribution file:** `attribution-aidecide-v1.json` counts the Galatia row under
  `h925-fallback`, the category it had before; the file is kept as measured. The label comes from `attribute.py:37`, which files every "no remake decision +
  garrison fallback" row as `h925-fallback`. In faithful mode that fallback is the original's own
  `FUN_0044ebe8` pick, not the #925 tier. The row is now attributed to state (below).
- **The remake log line:** "mercenary hire: 0 offer(s) hired across 0 army/armies" is the summary of
  `AiMercenaryHirePass` (`AiMercenaryHirePass.cs:100`). It counts offers **hired**, not offers found.
  The draft's first version read it as "found no offer"; the offer search plays no part in the row.
- **Galatia attribution, checked (2026-10-31):**
  - **The original's saves** (`run-exp-aidecide`, S02, decoded with conquest's `state/sav.py`): at the
    round start (`hooked-t03-AUTO0723.SAV`), Seleucid army 5 at (172,49) has 37,300 troops and
    Bithynia army 11 at (177,44) has 32,800. At the round end (`hooked-t04-AUTO0724.SAV`), army 5 has
    **26,137** and Bithynia (owner 11) has **no army**: the table drops from 12 to 11 records.
  - **The report:** Bithynia army 11's row is "same" (target army 5, score 1112, distance 5).
    Galatia's original row targets army 5 at score 91, distance 23.
  - **The remake replay:** `events.jsonl` has the army-11 against army-5 battle, then
    `BattleArmyDestroyed` (winner Bithynia, loser Seleucid).
  - **The diagnostic** (`diag-galatia-v1/`, `diag-galatia-v2/`): the patch adds two stderr lines only,
    and both runs' AI logs are identical to the v1 replay's. Its tree line shows Galatia army 0 at
    (195,42): `MercenaryRun`, city aradus (score 77, distance 26), army target army-4 (score 57),
    0 commands offered, then the garrison-fallback march.
  - Not re-executed: the diagnostic build itself.

## Result

| Comparison | 05b02936 | **8e2d9053** |
|---|---|---|
| Army decisions (749), by cause | 422 same, 250 #925 resupply, 8 #925 fallback, 14 "city > 85" target, 41 diplomacy, 14 state | **691 same**, 41 diplomacy, **17 state** (16, plus the Galatia row below) |
| Diplomacy seats (1,280) | 1,088 same; first divergences: 10 deterministic, 21 draw, 19 battle | **1,110 same**; first divergences: **0 deterministic**, 22 draw, 21 battle |
| Economy seats (1,200) | 1,055 same, 4 order city differs, 141 state | **1,063 same, 0 differ**, 137 state |
| Fleet decisions (150) | 124 same, 26 differ (Carthage fleet 0) | 123 same, 27 differ (**still only Carthage fleet 0**) |

The "diplomacy", "state", "draw" and "battle" rows are not port gaps. In each of them the round has
already differed before the compared decision, through random battle draws or through wars that
changed during the round. The earlier reports define these categories.

- **#925 (T250):** in classical-faithful, the AI now marches at the original's destination, as the
  [owner decision](2026-10-31-reachable-tiers-faithful-decision.md) requires. All 250 resupply rows
  match, and 7 of the 8 fallback rows match.
- **"City > 85" and capital defence:** the 14 rows stay fixed, as they were in T249.
- **Swap pass (T251):** none of the 10 deterministic diplomacy divergences remains. Every remaining
  first divergence is a draw or a battle.
- **Order city once per seat (T252):** the 4 economy seats now match. Deployments, the order counts
  (both games follow the original's stopping rule, 263 of 263) and the week-11 tax (113 of 113) all
  match.

## The Galatia row is a battle draw (attributed 2026-10-31)

S02 (Seleucid start), round 4 (`hooked-t03-AUTO0723.SAV`), Galatia army 0 at (195,42). The original
takes the mercenary-run branch, then attacks army 5 because its score of 91 is above 70. The remake
ends in the garrison fallback.
- **Same branch, same city:** the remake's tree also picks `MercenaryRun` and aradus (221,65), score
  77, distance 26.
- **Different army target:** army 5 is gone, so the remake's target is army-4 at (223,65), score 57.
  That is below the continuation threshold of 71, and the city's 77 is not above 85. No command is
  offered, and the fallback runs.
- **Why army 5 is gone:** both games play the seats in the same order from the human seat, and in
  both, Bithynia army 11 attacks Seleucid army 5 before Galatia's turn.
  - **Original:** the attack fails. Army 5 survives with 26,137 of 37,300 troops, and Bithynia's army
    is destroyed.
  - **Remake:** the attack wins (power 14,652 against 14,388 in `events.jsonl`), and army 5 is destroyed.
- **Cause: state,** a random battle result earlier in the round, not a port gap. `compare.py`'s state
  flag misses it because it covers an army's own battle or death, not its target's.

**So on `8e2d9053` no army decision in these 80 rounds remains unexplained.** This holds for the decision records only: [army order within a seat](2026-10-31-army-order-within-a-seat.md) finds 10 more armies whose first action differs, because the remake runs armies out of table order.

## The #144 boundaries are in 8e2d9053 (correction, 2026-10-31)

The draft's earlier versions, and this report until this revision, said the
[#144 corrections](2026-10-30-garrison-and-mercenary-boundaries144.md) were not in this commit.
**They are.** T250 made all three faithful-only, in `AiArmyTargetTree.cs`:
- the garrison fallback's capital radius is `< 10`, and the nearest city is taken in city-table
  order (strict `<`);
- the mercenary run skips offers at `>= 20` and walks the pool in slot order (strict `<`).

I read this in the `05b02936..8e2d9053` diff, where each rule sits behind
`ClassicalArmyNavigation.Applies`.

**Executed by conquest:** the #144 synthetic controls, rerun with `RemakeAdapter helperprobe` on
`8e2d9053`, in both layouts, 15 controls each. Data: `run-exp-boundary144/native-8e2d9053-v1.jsonl`
and `-v2.jsonl`. I paired each row with the original's emulated answer (`controls-v1.json`,
`controls-v2.json`, whose 16th row is a relation value, not a control) and compared destinations:

| Remake | Controls matching the original |
|---|---|
| `10d3bb81` | 14 of 30 (6 in v1, 8 in v2) |
| **`8e2d9053`** | **28 of 30** |

- **All distance and tie controls match:** capital distance 9/10/11, offers at 19/20/21, the
  19-against-20 pairs, the EBE8 table-order ties and the four E84C slot-order ties.
- **The two left are "capital index −1", once per layout.** The original has no capital guard: it
  reads city record −1, the bytes before the table, and walks to (153,48). The remake returns no
  destination. The #144 report already lists this as an ambiguity of the original.
- Not re-executed: the remake helper probe itself.

## Open

- **#144 control "capital index −1":** see the section above. The original's behaviour there is an
  ambiguity of the original, not a boundary.
- **Carthage fleet 0 (#174):** unchanged, since T250–T252 did not touch the fleet phase. Three rows
  changed verdict because earlier moves in their rounds changed; I checked this against the two
  reports:
  - S02 r4 is now the same;
  - S02 r5 and S15 r3 now differ.

  The cause is still the route and moves state at the fleet's turn, as the fleet report's
  "Round-start state of the differing fleet" section describes. Now attributed: 8 no difference,
  14 state, 5 a port gap ([fleet 0 attributed](2026-10-31-fleet0-rows-attributed174.md), as corrected).
- **Not covered, as before:** rounds 6 and later, other seeds, the fleet hunt branch, and the rest of
  #176.

## What this does not establish

- Anything about rounds 6 and later, other seeds or human choices.
- That the remake matches where the round had already differed (the "diplomacy", "state", "draw" and
  "battle" rows).
- Native Windows behaviour.
