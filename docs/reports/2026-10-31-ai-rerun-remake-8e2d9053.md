# The AI comparisons rerun on remake main 8e2d9053: the T250–T252 corrections close every attributed gap

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `44805be` (PR #289), owner
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

**Tag:** `[confirmed]`, Wine-only, for the three corrections. One army row and the fleet rows remain
open.

**Review note (2026-10-31):**
- **Release integrity:** I downloaded `run-exp-aidecide` and `run-exp-econ` again. Every file matches
  its `SAVES.sha256`.
- **Comparison reruns:** I ran all four comparers and `aidecide/attribute.py` from a scratch copy of
  conquest main `44805be`, on the committed replays and the release saves. All five outputs are
  **byte-identical** to the committed reports.
- **Remake commit:** `8e2d9053` is remake main, the single commit after `05b02936`. I did not
  re-execute the remake replays, which need the .NET build.
- **Label in the attribution file:** `attribution-aidecide-v1.json` counts the open Galatia row
  under `h925-fallback`, the category it had before. The draft treats it as **unattributed**,
  because the faithful fallback now matches the original's. I follow the draft; the count is the
  same either way (1).
- **The remake log line:** "mercenary hire: 0 offer(s) hired across 0 army/armies" is the summary of
  `AiMercenaryHirePass` (`AiMercenaryHirePass.cs:100`). It counts offers **hired**, not offers found.
  So the log shows that the remake hired nothing and chose the garrison fallback. It does not show
  by itself that the remake found no offer.

## Result

| Comparison | 05b02936 | **8e2d9053** |
|---|---|---|
| Army decisions (749), by cause | 422 same, 250 #925 resupply, 8 #925 fallback, 14 "city > 85" target, 41 diplomacy, 14 state | **691 same**, 41 diplomacy, 16 state, **1 unattributed** |
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

## Open

- **One army row:** S02 (Seleucid start), round 4 (`hooked-t03-AUTO0723.SAV`), Galatia army 0.
  - **The original** takes the mercenary run: `FUN_0044e84c` finds an offer, then the army score of
    91 > 70 attacks army 5.
  - **The remake** hires nothing ("mercenary hire: 0 offer(s) hired") and chooses the garrison
    fallback, one tile away.
  - Before, this was one of the 8 "#925 fallback" rows. With the faithful fallback in place, it
    shows as a separate difference.
  - **It is not the #144 offer-range boundary.** There, the remake is the more permissive side
    (`<= 20` against the original's `< 20`). The open #144 corrections (capital radius `< 10`, offer
    range `< 20`, ties in table order) are not in this commit.
  - Not attributed.
- **Carthage fleet 0 (#174):** unchanged, since T250–T252 did not touch the fleet phase. Three rows
  changed verdict because earlier moves in their rounds changed; I checked this against the two
  reports:
  - S02 r4 is now the same;
  - S02 r5 and S15 r3 now differ.

  The cause is still the route and moves state at the fleet's turn, as the fleet report's
  "Round-start state of the differing fleet" section describes.
- **Not covered, as before:** rounds 6 and later, other seeds, the fleet hunt branch, and the rest of
  #176.

## What this does not establish

- Anything about rounds 6 and later, other seeds or human choices.
- That the remake matches where the round had already differed (the "diplomacy", "state", "draw" and
  "battle" rows).
- Native Windows behaviour.
