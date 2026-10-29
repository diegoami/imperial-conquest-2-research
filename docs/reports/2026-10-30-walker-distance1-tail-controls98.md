# The army walker's distance-1 tail: contact branches confirmed; the strict-cost re-entry never decides in these controls

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `5275b9e` (PR #245). This
answers research issue [#98](https://github.com/diegoami/imperial-conquest-2-research/issues/98)
(for remake [#1329](https://github.com/diegoami/imperial_conquest_2/issues/1329) item 2), which was
delegated to conquest on 2026-10-29. Runner: ic2-conquest `runs/experiments/walker98/tail_controls.py`,
which follows the method of `runs/experiments/terrain42/original_steps.py`. Data:
`runs/experiments/data/run-exp-walker98/tail-controls-v1.json`.

**Tag:** `[confirmed, partial]`: 27 synthetic controls on the pinned unpatched EXE (`9d753d5d…`) in
Unicorn, each run with the current seat's human flag off and on. Not a Wine or Windows run, and not
original gameplay.

**Review note (2026-10-29):**
- **Rerun:** I ran the committed runner on the pinned EXE and DAT (`94d0ccfc…`) with Unicorn 2.1.4.
  Its output equals `tail-controls-v1.json` exactly: all 27 cases under both flags, the input
  hashes, the runner hash and the terrain costs.
- **The tail re-read in the decompile** (:51629–51657) matches the draft's description. It runs
  only when the walk ends exactly 1 from the target, and then reads the target cell:
  - **terrain 2..11:** the walker re-enters only if `cost < moves` (strict);
  - **a city marker 20..99:** siege (`FUN_0044b27c`) if the current nation's relation to the city's
    owner is 3 and moves > 0; otherwise `FUN_0044f6d8`;
  - **an army marker 200..247:** attack (`FUN_0044aee4`) if the relation to its owner is 3 and
    moves > 0;
  - **anything else:** nothing.

  An own city takes the `FUN_0044f6d8` branch because a nation's relation to itself is not 3:
  `TPolitics_OK` writes the diagonal as 0 (dump :55390; see also
  [`decompiled-war-cascade-and-peace-paths.md`](decompiled-war-cascade-and-peace-paths.md) §2).
- **Overlap.** This adds controls to the source-only reading in
  [`2026-10-21-strategic-lateral-steps-and-callers.md`](2026-10-21-strategic-lateral-steps-and-callers.md)
  ("Caller and termination matrix"). There, "Same unaffordable input, AI/human" already showed the
  one flag difference. Nothing contradicts it.

## Method

- **Map:** a synthetic all-plain 320 × 140 map.
- **Army:** the current nation's army 0 (3,000 light infantry) at (10,10), with the case's moves.
- **Target:** (10,9), 1 away, or (10,8), a 2-tile walk.
- **Contacts:** where a case needs one, a city record (owner 0 or 1) or an enemy army record
  (owner 1) sits at the target. Nation 0's relation to nation 1 is set to 0 or 3.
- **Terrain costs** come from the DAT: 1, 3, 1, 1, 2, 4, 4, 4, 4, 4, 4, 4.
- **Stubs:** presentation only (redraw `0x445B38`, sound `0x45BF28`). The three contact routines
  are intercepted at entry and recorded, not run.

## Results (identical for the AI and the human flag, except where noted)

| Target 1 away | Moves | Result |
|---|---|---|
| plain (cost 1) | 1, 2 | enters; 0 / 1 left |
| forest (cost 2) | 1 | stays. **AI: moves 0; human: moves 1** |
| forest | 2 (= cost) | **enters, 0 left** |
| forest | 3 | enters, 1 left |
| mountains / river (cost 4) | 3 | stays. AI: moves 0; human: moves 3 |
| mountains / river | 4 (= cost) | enters, 0 left |
| mountains / river | 5 | enters, 1 left |
| sea | 8 | stays, 8 left, no contact |
| own city (owner 0) | 8 | stays, 8 left, **`FUN_0044f6d8`** (non-war city) |
| city of nation 1 at peace | 8 | stays, 8 left, `FUN_0044f6d8` |
| city of nation 1 at war | 8 | stays, 8 left, **siege** |
| city at war | 0 | stays, no contact |
| enemy army at war | 8 | stays, 8 left, **attack** |
| enemy army at peace | 8 | stays, no contact |
| enemy army at war | 0 | stays, no contact |

**2-tile walks.** The first step is plain, so the last step has moves − 1 left:
- **Forest:** with 2 moves the army stays at (10,9) (AI 0 left, human 1); with 3 it enters with 0
  left.
- **Mountains:** with 4 moves it stays (AI 0 left, human 3); with 5 it enters with 0 left.
- **A city or army at war, with 1 move:** the first step spends it, so there is no siege or attack.

## Answers

1. **Contact branches:** confirmed as read. A siege or attack happens at war with moves > 0.
   `FUN_0044f6d8` handles a city not at war, own or at peace. Nothing happens for an army not at war
   or with 0 moves. The army never enters a marker cell.
2. **Cost == moves:** the step into terrain whose cost equals the moves left is taken, leaving 0.
   That is the line loop's step (`FUN_0044d420`), not the tail. In every terrain case here, the
   tail's own strict re-entry **never decides**:
   - when the loop's step enters, the tail is not needed;
   - when the step is refused (cost > moves), the strict test fails too.
3. **Human vs AI callers:**
   - **Inside the walker:** `TUnitMap_MoveHumanArmy` (`0x446d9c`) and the AI move (`0x44dba8`) run
     the same walker and tail, and the tail's branches are identical under both flags. The flag
     changes only an unaffordable step: the AI's moves fall to 0, a human's are kept.
   - **After the walker returns:** the human handler walks once more
     ([`2026-10-29-walk-stops-at-own-city-on-line230.md`](2026-10-29-walk-stops-at-own-city-on-line230.md)),
     and the AI move recurses
     ([`2026-10-30-ai-march-continuation-missing-in-remake.md`](2026-10-30-ai-march-continuation-missing-in-remake.md),
     [`2026-10-30-ai-move-stale-word-in-play97.md`](2026-10-30-ai-move-stale-word-in-play97.md)).

## What this does not establish

- A case where the tail's terrain re-entry decides the outcome. No synthetic walk here ends 1 away
  with cost < moves unless the loop has already stepped. Whether a lateral step on the last stretch
  can produce such a case is open.
- The battle, siege or supply that follows a contact: those routines were intercepted at entry.
- Wine or Windows behaviour, real maps, or several armies or cities interacting. The army marker
  code used (203) is a synthetic marker in the 200..247 range.
