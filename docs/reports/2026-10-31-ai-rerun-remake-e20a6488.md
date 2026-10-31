# The AI comparisons rerun on remake main e20a6488: T253's army order is verified, and T254 changes no row

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `493f80d` (PR #297), owner
request 2026-10-31, after remake #1655 (T253) and #1657 (T254) merged. Remake: main `e20a6488`, not
released, which is two commits after `8e2d9053`:
- `a1a9c5d2`, T253: "finish faithful armies in physical table order on live state";
- `e20a6488`, T254: "execute faithful mercenary continuation with remaining moves".

It repeats [the 8e2d9053 rerun](2026-10-31-ai-rerun-remake-8e2d9053.md) on the same 80 equal-state
rounds: 16 New Game starts (S00–S15 `*_AUTO0720.SAV`) × 5, seed 12345, each from the original's own
round-start autosave.
- **Data:** `runs/experiments/data/run-exp-airerun-e20a/`:
  - `remake-e20a6488-v1/`: the 80 replays;
  - the reports `report-aidecide-v1.json`, `attribution-aidecide-v1.json`, `army-order-v1.json`,
    `report-diplo-v1.json`, `report-econ-v1.json`, `report-econ2-v1.json`, `report-fleet-v1.json` and
    `report-routes-v1.json`.
- **The original's side:** releases `run-exp-aidecide`, `run-exp-diplo`, `run-exp-econ`,
  `run-exp-fleetphase`, `run-exp-fleetroute174` and `run-exp-econ2`, all in the
  [evidence index](../evidence-index.md).

**Tag:** `[confirmed]`, Wine-only.

**Review note (2026-10-31):**
- **All eight reports rerun** from a scratch copy of `493f80d`, on the committed replays and the
  release saves: **byte-identical**.
  - The comparers are the army comparison plus its attribution, diplomacy, economy, supply/hire,
    fleet, routes and army order.
  - **The army-order filter:** `army-order-v1.json` reproduces only with the **8e2d9053** army
    report as its row filter (679 armies). With this run's own army report the count is **679 of 680**.
    The draft's revision `897411d` (PR #298) adds that as `army-order-v2.json`, which is
    **byte-identical** to my rerun.
- **Remake commits:** `8e2d9053..e20a6488` is exactly T253 and T254. I did not re-execute the replays.

## Result

| Comparison | `8e2d9053` | **`e20a6488`** |
|---|---|---|
| Seats where the remake ran armies out of table order | 96 of 158 | **0 of 156** |
| Armies' first action matching the original (each run filtered by its own army report) | 668 / 679 | **679 / 680** |
| Army decision records, by cause | 691 same, 41 diplomacy, 16 state, 1 other | 692 same, 40 diplomacy, 16 state, 1 other |
| Diplomacy: same seats; deterministic first divergences | 1,110; 0 | **1,139; 0** (21 draw, 19 battle) |
| Economy: seats with a difference | 0 | 0 (1,060 same, 140 state) |
| Supply, hire, consolidation, merges: same seats | 1,192 / 1,200 | **1,194 / 1,200** |
| Fleet branch rows differing | 27 | 27 |
| Fleet route rows: a route written on one side | 19 | 19 |

- **T253 (army order) is verified:**
  - no seat runs its armies out of order;
  - every army's first action matches, except the Galatia battle-draw row;
  - the two supply/hire seats that came from army order (S05/S09 r1) now match.
- **T254 (the continuation with moves left) changes no row here.** In the original, every remaining
  continuation row has either 0 moves at the ferry request or the seat replay.
- **The 19 fleet route rows:**

  | Rows | Cause |
  |---|---|
  | 13 | diplomacy state, as before |
  | 1 | S06 r5: state; its writer is `F31C` city > 100 ([zero moves](2026-10-31-ferry-route-written-at-zero-moves159.md)) |
  | 4 | S06 r3/r4 and S13 r4/r5: the ferry request at 0 army moves; the remake still stops at 0 moves |
  | 1 | S08 r2: [the original plays Carthage's seat twice](2026-10-31-ai-seat-replayed-after-human-battle.md) |

- **The 6 supply/hire seats:** 5 are state, and S10 r2 is the
  [treaty timing](2026-10-31-ai-supply-hire-consolidation-merges176.md). Two of the state seats, S03 r1
  Seleucid and S06 r2 Rome, are also seats the original played twice.

## Still open in the remake

1. The ferry request at 0 army moves (#1652's remaining case; research #159 measured it).
2. The post-battle treaty applied at the seat's end, not right after the battle.
3. The seat replay after a battle against the human.

## What this does not establish

Rounds 6 and later, other seeds, the fleet hunt branch, and native Windows behaviour.
