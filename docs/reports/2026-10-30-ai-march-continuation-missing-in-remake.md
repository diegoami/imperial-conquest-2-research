# The original's AI army move can keep walking within a turn; the remake's AI marches once

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `ac2d617` (PR #243), written
for research issue [#97](https://github.com/diegoami/imperial-conquest-2-research/issues/97)
(remake [#1585](https://github.com/diegoami/imperial_conquest_2/issues/1585)). Remake **v0.8.4**
(`d9cc71bc82e22ad1d3d7c373c3d80d61ed0bcbeb`).

**Tag:**
- Original: `[confirmed: decompile + disassembly + x86 replay of the mechanism]`, with one condition
  **corrected** (below).
- Remake: `[code: v0.8.4 source]`.
- Not measured in play.

**Review note (2026-10-29):**
- **The decompile matches the draft's reading.** `FUN_0044dba8` is at :51790 of `all_app_functions.txt`
  (`2018c205…`).
  - An army whose cell field `+8` is −1 (aboard) moves its fleet, `FUN_0044cd08`, for 2 moves.
  - Otherwise, if `FUN_0044cb40` passes, it walks toward the target with `FUN_0044d734`. If not, it
    walks toward an intermediate point from `FUN_0044db38`.
  - If its moves are unchanged and still positive, it walks toward a fallback point from
    `FUN_0044cec8` and spends 1 move.
  - Then, while the distance to the target (`FUN_00449018`) is above 1 and moves remain, it calls
    itself.
- **Correction: the direct-line path reads an uninitialised stack word.** In the disassembly
  (pinned EXE `9d753d5d…`), the intermediate point lives at `[ebp-0xa]`.
  - Only the `FUN_0044db38` branch writes it (`0x44dc1e`–`0x44dc26`). The direct branch
    (`0x44dc0f`–`0x44dc1b`) jumps over that write.
  - Both later tests still read the slot: the fallback at `0x44dc4d` and the recursion at
    `0x44dc8c` (`cmp word [ebp-0xa], -1; jle`).
  - So on the direct-line path, the fallback and the recursion run only if a **stale** stack value
    happens to be ≥ 0. The draft's "re-walks until within 1 tile or out of moves" holds for the
    intermediate-point path; on the direct path it depends on what the caller left in that slot.
- **The x86 replay** (Unicorn 2.1.4, the method of
  [`2026-10-29-walk-stops-at-own-city-on-line230.md`](2026-10-29-walk-stops-at-own-city-on-line230.md),
  entry `0x44dba8`, human flag off). I loaded only the map and the army records; other tables
  (cities, fleets) read as zeros, so the routes below show the mechanism, not the game's choices.

  | Case | Path | Stale `[ebp-0xa]` | Calls of `0x44dba8` | End |
  |---|---|---|---|---|
  | Rome army 1, (120,53) 8 moves → (99,32) (`walk-city-on-line/original/a000.SAV`) | direct (`cb40` = 1) | −1 | 1 | (118,52), 6 left, identical to the remake's single walk |
  | the same | direct | 0 | 2 | (115,49), 0 left (the AI's unaffordable step zeroes its moves) |
  | Carthage army 3, (93,79) 8 moves → (61,56) (`walk-carthage-army3/original/a000.SAV`) | intermediate (`cb40` = 0) | −1 or 0 (unused) | 3: from (93,79) with 8, (93,82) with 5, (93,85) with 2 | moves exhausted; the slot held a real point each time (x = 93) |

  - On the intermediate path, the recursion is real and repeats with a fresh point each time,
    independent of stale memory.
  - On the direct path, the same state gives one walk or a continued walk depending only on the
    stale word.
- **What the game reads there: measured later, never −1.** There are **10** call sites
  (`0x44e913`, `0x44ec7d`, `0x44ecd6`, `0x44f2e7`, `0x44f2f9`, `0x44f409`, `0x44f43f`, `0x44f47c`,
  `0x44f4a3`, `0x44f4c7`), plus the self-call `0x44dca1`.
  - *Corrected:* this note first listed nine, because I had cut the scan output short.
  - ic2-conquest's observation-only hook measured the word in play: 5 starts × 5 AI End turns,
    autosaves byte-identical to the plain build. The word was 49, 71 or 0 and never −1, and every
    recursion and no-progress test passed. See
    [`2026-10-30-ai-move-stale-word-in-play97.md`](2026-10-30-ai-move-stale-word-in-play97.md).
- **The remake side is confirmed in source at v0.8.4.**
  - `AiMilitaryPhase.cs`:307 says "an army that has already marched this turn is offered only the
    attack its target allows, never a second march".
  - March candidates come from `AddMarchCandidate` (:598), with one
    `ClassicalArmyNavigation.Intermediate` point (:568).
  - `AiTurn.cs`:232/:415 add the army to `marched`.
- **Overlap.**
  - [`2026-10-21-strategic-lateral-steps-and-callers.md`](2026-10-21-strategic-lateral-steps-and-callers.md)
    lists the AI army caller `0044DBA8` ("routing before walking and fallback moves accounting")
    without the recursion's conditions. Its control "Same unaffordable input, AI" (runner case `ai_unaffordable_zeroes`)
    explains the 0 moves above.
  - The human-move counterpart is the walk report linked above: exactly one second walk, with no
    stale-stack dependence.

## Answer

**Original.** The AI army move `FUN_0044dba8(army, target)`:
1. **Aboard a fleet:** the army moves the fleet (`FUN_0044cd08`) and loses 2 moves; there is no
   walk.
2. **Otherwise:** if `FUN_0044cb40` passes, it walks toward the target (`FUN_0044d734`, the same
   walker as human moves). If not, it walks toward an intermediate point from `FUN_0044db38`.
3. **No progress:** if the walk left the army's moves unchanged, moves remain and the point is
   valid, it walks toward a fallback point from `FUN_0044cec8`, then spends 1 move whatever
   happened.
4. **Recursion:** if the Chebyshev distance to the target is still more than 1, moves remain, and
   the point and target are valid, it **calls itself again** from the new position, with a fresh
   line and a fresh intermediate point.

On the intermediate-point path, an AI army therefore re-walks until it is next to its target or out
of moves, with no fixed limit; step 3's forced cost guarantees an end. On the direct-line path,
steps 3 and 4 test an intermediate-point slot that this path never writes. They run only when that
stale value is ≥ 0, and this review does not establish what it is in play.

**Remake.** An AI march is one `MoveArmyCommand`, aimed at the target or at a single intermediate
point. It is executed once, by the same handler as human moves, and the army is then not offered a
second march that turn. An AI walk that ends short with moves left stops there.

## How often (remake, measured; added 2026-10-29)

The draft gained this at ic2-conquest `main` `fbd77a7` (PR #244). The probe is `RemakeAdapter aiprobe`
(ic2-conquest `difftest/remake_adapter/AiProbe.cs`), run on remake v0.8.4, `classical-faithful`:
- it plays 10 End turns from each of the 16 New Game starts, with seeds 1–3 (48 runs);
- the human seat gives no orders;
- for every AI march named in the remake's AI log, it records the march's own `ArmyMoved` event.

The data, one jsonl per run, is committed at `runs/experiments/data/run-exp-diff084-aiprobe/`. This
review parsed all 48 files independently, and the figures reproduce exactly:

| | AI marches |
|---|---|
| logged | 5,105 (94 armies gone by the end of their round: no position or moves) |
| walked | 5,011 |
| ended within 1 tile of the aimed point | 2,984 (59.5%) |
| **ended more than 1 tile short, with moves left** | **1,406 (28.1%)** |
| ended short with no moves left | 621 |

**The 1,406 by reason:**

| Reason | Marches |
|---|---|
| approach an enemy army | 781 |
| approach a city | 436 |
| mercenary run | 100 |
| garrison fallback | 32 |
| approach an army via a waypoint | 26 |
| move to the resupply city | 24 |
| defend the resupply city | 7 |

The draft's list leaves out the last 7, so its categories sum to 1,399.

**Moves left in the 1,406:**

| Moves left | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Marches | 365 | 197 | 245 | 127 | 56 | 145 | 86 | 142 | 43 |

**How to read it.**
- **Remake only.** No original game is played, so this counts where the *remake's* AI stops short.
- **Moves left are estimated.** They come from the remake's refill rule applied to the army at the
  end of the round (`SupplyMoraleRule.BaseMoves` with the supply penalty). This is an estimate where
  troops or supplies changed during the round.
- **The bounds assume the original routes the same way.** The draft brackets the share that ends
  differently in the original between 26/5,011 (0.5%), the waypoint marches, and 1,406/5,011 (28%).
  This assumes the original's `FUN_0044cb40` test sends the same marches through an intermediate
  point as the remake's waypoint choice, which the probe does not check. The stale `[ebp-0xa]`
  above decides where in that range the original falls. In play it was never −1, so the share is
  about 28%, the upper end
  ([`2026-10-30-ai-move-stale-word-in-play97.md`](2026-10-30-ai-move-stale-word-in-play97.md)).
- **Distance is measured to the aimed point.** The original's recursion test measures distance to
  the *target*.

## Consequence for #1585

| Mover | Original | Remake v0.8.4 |
|---|---|---|
| human army | walker, plus **one** second walk if short with moves left | one walk |
| AI army, intermediate-point path | walker repeated (fresh point each time) until within 1 tile or out of moves; forced 1-move cost when stuck | one walk per turn |
| AI army, direct-line path | one walk, or continued as above, depending on a stale stack word | one walk per turn |

A fix that adds one second walk to the shared move command would match human moves only. The AI's
intermediate-point continuation needs the recursion of `FUN_0044dba8` or an equivalent loop. The
direct-line behaviour should be settled before the remake reproduces it, for example by hooking it
in play.

## What this does not establish

- Any AI walk observed in play. The #232 campaigns cannot isolate one, because the two games' AIs
  pick different targets after the first End turn.
- The stale value at `[ebp-0xa]` on the direct path for any real caller.
- Real routes. The replay lacked the city and fleet tables.
- The semantics of `FUN_0044cb40`, `FUN_0044db38` and `FUN_0044cec8`. Only their use is read here.
- How often an AI walk ends short in the original. The remake's share (28.1%) is measured above.
