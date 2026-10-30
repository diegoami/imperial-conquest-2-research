# Army paths in play match the emulator; fleets share the step rule and the human second walk

**Update 2026-10-30 (remake v0.8.5):** `fleet-second-walk-88-32` is fixed; `fleet-second-walk-87-47` now matches after the order and differs only after End turn. See [2026-10-30-recheck-v085.md](2026-10-30-recheck-v085.md).

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `37bdac5` (PR #247). It
answers the remaining parts of research issue
[#42](https://github.com/diegoami/imperial-conquest-2-research/issues/42) (build
[#1012](https://github.com/diegoami/imperial_conquest_2/issues/1012)), delegated to conquest on
2026-10-29. Sources:
- release [`run-exp-step-hook42`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-step-hook42)
  (army steps in play);
- `runs/experiments/data/run-exp-fleet42/` (fleet emulator controls and the real-map search);
- release [`run-exp-diff084-orders-b7`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-orders-b7)
  (two live fleet cases).

Remake **v0.8.4** (`d9cc71bc82e22ad1d3d7c373c3d80d61ed0bcbeb`).

**Tag:** `[confirmed, partial]`.
- **Army paths:** observed in the running original under Wine with an observation-only hook.
- **Fleet step rule:** emulator controls on the pinned EXE.
- **Human fleet second walk:** emulator and two live Wine cases.
- **AI fleet route-finder branch:** not established.
- Not run on native Windows.

**Review note (2026-10-29):**
- **Release integrity:** `run-exp-step-hook42` has 8 of 8 saves OK and `run-exp-diff084-orders-b7`
  12 of 12, against their `SAVES.sha256`.
- **Inertness:** I compared every hooked autosave with its plain counterpart, and all 4 pairs are
  byte-identical: C4 far, C4 near, and AI turns 1 and 2. The hook probes the prologue of
  `FUN_0044d420`.
- **C4 paths re-read** from `c4-far-steps.jsonl` and `c4-near-steps.jsonl` (army 0 at (100,37) with
  8 moves):
  - **far order to (100,25):** (100,37) → (100,36) → (100,35) → (100,34) → **(101,33)**
    (cursor (100,33), forest) → (100,32) → (100,31) → (100,30) → (100,29), 0 left;
  - **near order to (100,32):** the same path to (101,33), then (100,32), 3 left.

  This is exactly the emulator's trace in
  [`2026-10-21-strategic-lateral-steps-and-callers.md`](2026-10-21-strategic-lateral-steps-and-callers.md),
  so #42's C4 endpoint question is now answered at path level in play.
- **AI steps recounted** from `ai-2-steps.jsonl`, over two AI End turns from `BASE.SAV`:
  - 160 steps by 23 army-turns, all from call site `0x44d873`;
  - of 126 adjacent consecutive steps, **26 left the line** (position ≠ the previous cursor).
- **Fleet controls rerun:** `runs/experiments/fleet42/fleet_controls.py`, run on the pinned EXE and
  DAT, reproduces `fleet-controls-v2.json` exactly. The output includes one AI case (`ai-island`)
  that faults in emulation on the `FUN_0044d174` route-finder branch. That matches the draft's
  statement that this branch needs runtime sea-route tables.
- **Real-map search rerun:** `search_real_map.py` on `saves/fleet-port-antium-0734.SAV`
  (`34d31d8f…`), fleet 2, reproduces all **75** targets where the handler's second call changes the
  result. Only the save-path string differs. Its single-call and two-call predictions for (88,32)
  and (87,47) are exactly the live results below.
- **Live fleet cases re-read** from the `a001` saves of `run-exp-diff084-orders-b7`. Fleet 2 starts
  at (101,46) with 29 moves in both games:

  | Order | Original | Remake |
  |---|---|---|
  | toward (88,32) | (88,32), 14 left | (93,37), 19 left |
  | toward (87,47) | (87,47), 14 left | (89,48), 16 left |

- **Code re-read.**
  - `TUnitMap_MoveHumanFleet` (dump :46761/:46766) calls `FUN_0044e094`, then calls it again if the
    fleet is short of the target (`FUN_00449018` > 0) with moves left. This is the same shape as
    the army handler.
  - In the AI fleet wrapper `0x44e1fc`, the disassembly stores the target into the point local at
    `[esp+4]`/`[esp+6]` (`0x44e225`, `0x44e22a`) before the direct-line test at `0x44e245`. So
    unlike the army wrapper `0x44dba8`, it reads no stale word.

## Answer

1. **Army paths in play** equal the emulator's step rule. The C4 walks cross exactly the tiles the
   original-instruction replay predicted, including the lateral step to (101,33). In AI turns, about
   1 step in 5 (26 of 126) leaves the line. All AI army steps go through the walker's step call site
   `0x44d873`, the same one human walks use.
2. **Fleets use the same step rule as armies**, with sea costs (emulator controls):
   - with rough sea on the line and calm laterals, the fleet goes east;
   - if the east lateral is rough or a marker, it goes west;
   - if all three are rough, it goes straight;
   - a rough target whose cost equals the moves left is entered with 0 left;
   - a land wall stops it.
3. **The human fleet handler walks a second time,** exactly like the army handler. It changes the
   result for 103 of 400 synthetic maps and for 75 real-map targets from Antium. The two live cases
   show the original reaching the target where the remake stops short. The remake's
   `MoveFleetCommandHandler` makes one `MovementWalker.Walk`, so **the missing second walk also
   covers human fleets** ([walk report](2026-10-29-walk-stops-at-own-city-on-line230.md)).
4. **The AI fleet wrapper `0x44e1fc` has no stale-word issue.** Its continuation through the
   `FUN_0044d174` route finder is not established: it needs runtime sea-route tables, and no live
   hook was run for it.

## What this does not establish

- The AI fleet's recursion or continuation off the direct path. That needs a live hook. *(Since observed: [2026-10-30-ai-fleet-moves-in-play1409.md](2026-10-30-ai-fleet-moves-in-play1409.md).)*
- Paths beyond two AI End turns from one start, or other seeds.
- Native Windows behaviour.
- Fleet routes on real maps beyond the one-save search, or with storms during the walk.

## Evidence

- **Army steps:** `runs/experiments/data/run-exp-step-hook42/`: `c4-far-steps.jsonl`,
  `c4-near-steps.jsonl`, `ai-2-steps.jsonl`, the `*-inert.json` files and `ai-2-summary.txt`. The
  saves are in the release. Hook build: `patches/step_hook.py`, applied to the seed build
  (`354d8265…`).
- **Fleet controls:** `runs/experiments/fleet42/fleet_controls.py` and `search_real_map.py`, with
  outputs `runs/experiments/data/run-exp-fleet42/fleet-controls-v2.json` and
  `search-antium-fleet2-v1.json`.
- **Live fleet cases:** run `run-exp-diff084-orders-b7`, `fleet-second-walk-88-32/` and
  `fleet-second-walk-87-47/`, each with `original/` and `remake/` checkpoints. They were
  pre-registered in `difftest/cases/orders230_b7.py`.
