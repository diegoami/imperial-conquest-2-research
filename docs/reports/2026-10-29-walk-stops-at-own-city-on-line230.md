# A player's move walks a second time in the original when the first walk ends short; the remake walks once

**Update 2026-10-30 (remake v0.8.5):** the human army second walk is fixed. All four walk cases now match the original. See [2026-10-30-recheck-v085.md](2026-10-30-recheck-v085.md).

*(First seen with an own city on the line; the file name keeps that first case.)*

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `7c5803b` (PR #239, branch
`research/diff084-campaign232`), conquest [#230](https://github.com/diegoami/ic2-conquest/issues/230).
The [#232](https://github.com/diegoami/ic2-conquest/issues/232) rule-bot campaign found it. Releases
[`run-exp-diff084-orders-b4`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-orders-b4)
and
[`run-exp-diff084-campaign`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-campaign);
the save SHA-256s are committed at `runs/experiments/data/<run>/SAVES.sha256`. Wine-only. Remake
**v0.8.4** (`d9cc71bc82e22ad1d3d7c373c3d80d61ed0bcbeb`), `classical-faithful`.

**Tag:** `[confirmed, partial]` for the observation: single deterministic orders from three saves
(Rome, Carthage, Gaul), three armies. This review **establishes the cause** `[confirmed: original x86 replay]`:
the original's click handler calls the walker a second time, and the remake does not.

**Review note (2026-10-29):**
- **Release integrity:** all 24 + 49 saves match the committed `SAVES.sha256` files.
- **Saves re-read** with my own reader:
  - Venusia (city 115, Rome's) is at (118,51) with marker word 36;
  - army 1 starts at (120,53) with 8 moves;
  - every row of the table below reproduces from the `a001` saves of both games.
- **The cause, in the decompile.** `TUnitMap_MoveHumanArmy` (`0x00446d9c`, :46713) handles a human
  army's click.
  - It calls the army walker `FUN_0044d734` once.
  - If the army has not reached the clicked tile (`FUN_00449018` > 0) and still has moves left, it
    calls the walker **a second time**, from the army's new position and with a fresh line.
  - [`2026-10-21-strategic-lateral-steps-and-callers.md`](2026-10-21-strategic-lateral-steps-and-callers.md)
    already lists this ("Second walk when not at target and moves remain") but never observed it in
    play. This is that observation.
- **The cause, replayed.** I replayed the original's own instructions in Unicorn 2.1.4, following
  ic2-conquest's `runs/experiments/terrain42/original_steps.py`:
  - inputs: the pinned EXE (`9d753d5d…`) and DAT (`94d0ccfc…`), and the case's own `a000.SAV`
    (map and all army records);
  - only the redraw and sound calls are stubbed, as in that runner; my wrapper is a private
    scratch script.

  | Order | One walker call | The click handler's two calls | Original game (save) | Remake (save) |
  |---|---|---|---|---|
  | toward (99,32) | (118,52), 6 left | **(115,49), 1 left** | (115,49), 1 left | (118,52), 6 left |
  | toward (116,49) | (118,52), 6 left | **(116,49), 3 left** | (116,49), 3 left | (118,52), 6 left |
  | to (120,48), clear line | (120,48), 3 left | (120,48), 3 left (no second call) | (120,48), 3 left | (120,48), 3 left |

  The steps of the first call are (120,53) → (119,52) → (118,52). There the line's next tile is
  Venusia, and the walk ends. The second call for (99,32) goes (118,52) → (117,51) → (116,50) →
  (116,49) → (115,49), the last step into forest, which costs 2.
  - **So the remake's walk equals the original walker's single call exactly.** What the remake
    lacks is the handler's second call.
  - In the remake v0.8.4 source, `TUnitMap_MoveHumanArmy` is cited only for the stay-selected rule
    (`godot/UI/MapClickRules.cs`:170, `godot/UI/GameMapView.cs`:1327). I found no second walk; this
    was a static search, not a trace.
- **Campaign:** in `rome-rulebot1-5t`, the orders are equal in turns 1–3 and differ from turn 4. At
  the start of turn 2, army 1 stands at (115,49) in the original and at (118,52) in the remake, and
  it stays apart afterwards. This matches the draft.
- **`walk-line-clear` is not a control.** Its target (120,45) is sea. The original leaves the army
  in place; the remake walks to (119,46) with 1 move left. That is the known sea-target command gap
  of
  [`2026-10-29-v084-known-differences-and-command-gaps.md`](2026-10-29-v084-known-differences-and-command-gaps.md)
  §2.
- **Overlap.** These reports fit, and none is contradicted:
  - [`decompiled-army-movement-and-river-cost.md`](decompiled-army-movement-and-river-cost.md)
    gives the call chain;
  - [`2026-10-24-army-navigation-rule187.md`](2026-10-24-army-navigation-rule187.md) covers army
    navigation;
  - the lateral-steps report's step rule is consistent: the walker's step does not detour around a
    city on the line, and the second call's fresh line does.

## Answer

The start is `BASE.SAV` (Rome, 270 BC, Spring week 1). Rome's army 1 (8 moves) stands at (120,53).
On the exact diagonal toward the north-west, its second tile (118,51) is Venusia, Rome's own city,
and a city marker blocks an army's path.

| Order (army 1, one click / one `move`) | Original | Remake |
|---|---|---|
| toward (99,32), 21 tiles | ends at **(115,49)**, 1 move left | ends at **(118,52)**, 6 moves left ("spending 2 of 8 moves") |
| toward (116,49), within reach | ends at **(116,49)**, 3 moves left | ends at **(118,52)**, 6 moves left |
| north to (120,48), clear land line (control) | (120,48) | (120,48): same |

**Why:** one click in the original walks the line, and if the walk ends short of the target with
moves left, it walks again from where it stopped. The first walk ends beside Venusia. The second
walk starts a new line from (118,52), which passes the city. The remake performs only the first
walk.

## In general (added 2026-10-29, draft at ic2-conquest `main` `50ab1a7`, PR #241)

**The rule.** After a human army's move order, the original calls the army walker. If the army is
still short of the target with moves left, it calls the walker once more, from the new position on
a fresh line (`TUnitMap_MoveHumanArmy`). The remake calls it once, and its single walk equals the
original's first call step for step. This holds in all three replayed cases, below.

**When a first walk ends short.** It does so when its chosen step is blocked (a city or army marker
on the line) or costs more than the moves left. A neighbouring tile may still be affordable. This
follows from the step rule of
[`2026-10-21-strategic-lateral-steps-and-callers.md`](2026-10-21-strategic-lateral-steps-and-callers.md):
- affordability is tested after the candidate is chosen;
- a human army's unaffordable step keeps its moves.

This reading is code-backed `[code]`; it was not replayed for each campaign move.

**How often, in the #232 campaigns.** The release `run-exp-diff084-campaign` holds three archives.
All 453 saves match `SAVES.sha256`. I parsed every remake `move` receipt of the **16** completed
campaigns (the folders with `summary.json`):
- **32 move orders**, of which **21 ended short of the target with moves left**. The draft says
  "15 finished campaigns"; the 32 and 21 reproduce over the 16 folders.
- The 21 come from only 7 armies, re-ordered turn after turn: Carthage's army 3 and Rome's army 1
  five times each, Bithynia's army 11 and Ptolemaic's army 7 four times each, and one order each for
  Celtiberia, Gaul and Seleucid. Carthage's army 3 sits at (87,76) from turn 2, and Ptolemaic's
  army 7 at (189,94) from turn 1, since its target lies across the sea.
- These are the moves where the original would walk a second time, but that second walk can be
  blocked too. So 21 is an upper bound on the orders that end differently, not a count of observed
  differences.
- The original's own receipts were not parsed for this count.

**Fleets too:** the human fleet handler makes the same second walk, and the remake's fleet move
walks once ([2026-10-30-paths-in-play-and-fleet-walks42.md](2026-10-30-paths-in-play-and-fleet-walks42.md)).

## Two more cases, with no city on the line (added 2026-10-29)

The draft gained these at ic2-conquest `main` `e6ee978` (PR #240), from the #232 campaigns of other
nations. Both were reproduced as single orders (run
[`run-exp-diff084-orders-b5`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-orders-b5),
turn 0720; the starts come from release `run-exp-civ-sweep`). This review checked all 12 saves
against `SAVES.sha256` (12 of 12 OK), re-read the endpoints from the `a001` saves, and replayed the
original walker on each case's `a000.SAV`. For the replay, the acting nation was set as the current
human seat.

| Start | Order | Original (save) | Remake (save) | One walker call | Two calls |
|---|---|---|---|---|---|
| `S01_Carthage_AUTO0720.SAV` | army 3 from (93,79) toward (61,56) | (89,76), 0 left | (90,77), 1 left | (90,77), 1 left | **(89,76), 0 left** |
| `S06_Gaul_AUTO0720.SAV` | army 9 from (93,28) toward (92,34) | (92,34), 1 left | (92,32), 3 left | (92,32), 3 left | **(92,34), 1 left** |

The first walk ends short with moves left in both cases, although no city is on the line:
- **Carthage:** (93,79) → (92,78) → (92,77) → (91,77) (a 4-point step) → (90,77).
- **Gaul:** (93,28) → (92,28) → … → (92,32).

The handler's second walk then continues: Carthage (90,77) → (89,76); Gaul (92,32) → (92,33) →
(92,34). So the difference is **not specific to cities**. It appears whenever the original's first
walk stops short of the target with moves left. The remake again equals the single call exactly.

The draft adds that, in the Gaul campaign, Rome's AI destroyed the Gaulish army at (92,34), where
the original's walk had put it. In the remake the army stood two tiles away and survived. This
review did not re-read that campaign.

## Found in play

The #232 campaign `rome-rulebot1-5t` (rule bot, 5 turns, seed 12345) gave both games the same orders
in turns 1–3. Rome's own records differed from turn 1 because of this walk: army 1 was ordered to
(99,32). Army 1's different position then made the bot's turn-4 orders differ: it bought supplies
in the original and marched in the remake. The data is in
`runs/experiments/data/run-exp-diff084-campaign/`.

## Evidence

Run `run-exp-diff084-orders-b4` (turn 0720): `walk-city-on-line/original/a001.SAV` vs
`walk-city-on-line/remake/a001.SAV`, and the same for `walk-city-on-line-near/` and
`walk-line-clear-land/`. Original: `Imperial Conquest 2 fast rollingsave seed.exe` (SHA-256
`354d8265…`), seed 12345, Wine 10.0. The x86 replay used the unpatched pinned EXE
`Imperial Conquest 2.exe` (`9d753d5d…`), not the patched build that played the game. This review did
not diff the patched build's movement code. The replay matching every played endpoint is consistent
with that code being unchanged.

## What this does not establish

- Native Windows behaviour.
- Every geometry that makes the first walk end short. Three cases are covered: one with an own city on the line, two without.
- Whether a second walk can itself end short and leave moves unused. The handler calls the walker
  at most twice.
- The AI's walks, which go through a separate routing wrapper (`0x0044dba8`): see
  [2026-10-30-ai-march-continuation-missing-in-remake.md](2026-10-30-ai-march-continuation-missing-in-remake.md).
- Where exactly the remake's move command would need the second call.
