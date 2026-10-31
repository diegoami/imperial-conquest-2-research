# AI economy, original vs remake main: one port gap (the order city is chosen once per turn); budgets, deployments, counts and tax match

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `cdd4005` (PR #286), for
conquest #176 (strategic fidelity), owner request 2026-10-31. It uses the method of the
[AI decisions](2026-10-30-ai-decisions-vs-remake-main.md) and
[AI diplomacy](2026-10-30-ai-diplomacy-vs-remake-main.md) comparisons.
- **Hook:** `patches/econ_hook.py`, observation-only, with four probes:
  - the own/threat comparison in `FUN_0044ffbc` (`0x45011E`);
  - the state after recruiting and the week-11 tax policy (`0x4501D6`);
  - each new order at `FUN_004501f4`'s epilogue (`0x4502D9`);
  - each deployment at `FUN_0044a4e0`'s entry.
- **Data:** `runs/experiments/data/run-exp-econ/` (`orig-v1/`, `report-v1.json`, `remake-cityonce-v1/`,
  `eco-city-once.patch.txt`). The remake side is the diplomacy run's `remake-05b02936-v1` logs.
- **Release:** [`run-exp-econ`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-econ).
- **Starts:** the 16 New Game starts, S00–S15 `*_AUTO0720.SAV`, seed 12345, 5 rounds each.
- **Remake:** main `05b02936`, not released.

**Tag:** `[confirmed]`, Wine-only.

**Review note (2026-10-31):**
- **Release integrity:** 162 of 162 files match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain saves myself: **80 of 80** pairs are
  byte-identical. The plain saves are also identical to the diplomacy run's (80 of 80).
- **Comparison rerun:** I ran `runs/experiments/econ/compare.py` from a scratch copy, reading the
  start saves read-only. The output is **identical** to `report-v1.json`.
- **Disassembly** of `FUN_004504f4`:
  - `call 0x4502E0` (the city choice) appears once, at `0x450664`;
  - the order loop starts at `0x450672` (the back-jump at `0x45075A`) and calls `FUN_004501f4` at
    `0x4506C9` inside it.
- **Remake code** at `05b02936`: `AiFaithfulEconomy.cs:333` calls `ChooseCity` inside the order loop
  that begins at line 310.
- **Not re-executed:** the remake replays and the patch check.

## Answer

Over 1,200 AI seat-turns:

| | Seats |
|---|---|
| **same:** budget, deployments, order city, order counts consistent with the rule, tax | **1,055** |
| state: the budget already differs (earlier battles or diplomacy in the round) | 141 |
| **differs** | **4**, all in the order city |

Over the 1,059 seats with equal budgets:
- deployments match 1,059 of 1,059;
- order city 1,055 of 1,059;
- week-11 tax 113 of 113;
- 794 seats placed no orders in either game.

**Order counts:** 265 seats placed orders. In 265 of 265, both games' counts follow the original's
stopping rule. The unit types and troop sizes are random draws, so the count is checked by replaying
`FUN_004504f4`'s rule on each side's own draws, with the original's inputs. Orders are placed while
all of these hold:
- k < 8;
- the queued value is below the deficit;
- mobilization < 100;
- the treasury is above −wealth/500, or k < 3.

**The one port gap:**
- **Original:** `FUN_004504f4` chooses the order city (`FUN_004502e0`) **once**, before its order
  loop, and every order of the turn goes there.
- **Remake:** `AiFaithfulEconomy` chooses again for each order, on the updated state. `FUN_004502e0`'s
  "more than a third of the queued orders are at the capital" test can therefore flip mid-turn.
- **Where it happened:** S03 r2 Seleucid, S05 r1 Ptolemaic, S06 r4 Rome and S13 r4 Rome.
- **Patch check:** a scratch patch that chooses once gives the original's city in all 4.

## What this does not establish

- **Not checked directly:** the random draws themselves; only their consequences, the counts.
- **Not compared branch by branch:** `FUN_004502e0`'s own branches. The 1,055 equal cities cover the
  branches those states reached.
- **Not hooked in the original:**
  - consolidation (`FUN_00450858`);
  - merging (`FUN_004509f0`);
  - `FUN_00450b30`;
  - the supply pass;
  - mercenary hire.
- Rounds 6+, other seeds, and native Windows behaviour.
