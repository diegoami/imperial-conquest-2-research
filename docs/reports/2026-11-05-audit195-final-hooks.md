# AI audit #195, final hook runs: C22's recursion bucket attributed; the own-capital stays confirmed as diplomacy draws; the late fleet rows traced to the stored route

**Tag:** [confirmed: Wine hooks of the seed build (observation-only; hooked autosaves byte-identical to the plain build,
27/27)]. Wine only.
**Provenance:** raw evidence from `diegoami/ic2-conquest` (PR #345, merge `f71c70ff`). ic2-conquest made the runs but did
not interpret them: the owner ended that session and asked research to analyse the evidence. **The analysis below is
research's own (2026-11-05).**
**Task:** research #195, the open points of
[C22/C23/stays](2026-11-05-audit195-c22-c23-stays.md) and [step 7](2026-11-05-audit195-step7-late-years.md).

All paths are under `runs/experiments/data/run-exp-audit195/` (conquest). Saves: release `run-exp-audit195`
(`audit195-final-hooks-saves.tar.gz`; hashes in `SAVES.sha256`).

## 1. C22: the 37 recursion-bucket sieges and attacks (`c22c23-hook-v4/`)

**The run:** hook v2, whose outer caller walks past `FUN_0044dba8`'s recursion frames (`0x44DCA6`). It uses the same 16
civ-sweep starts × 5 rounds, seed 12345, no human orders. The exe is `709ba0ef…`; v2, v3 and v3b used `08b41284…`,
which had no frame walk.

**The totals are unchanged** from v2: 1,525 entries, 571 resupplies, 49 sieges and 64 attacks. So the frame walk changes
only the attribution. v2's recursion bucket (435 entries, 258 resupplies, 10 sieges, 27 attacks) redistributes exactly
onto the outer callers (return addresses):

| outer caller | entries v2 → v4 | resupply | siege | attack |
|---|---|---|---|---|
| `F31C` army target (`0x44F40E`) | 158 → 203 | — | — | 17 → **32** |
| `F31C` city target (`0x44F444`) | 141 → 213 | — | 21 → **24** | — |
| `F31C` resupply walk (`0x44F481`) | 603 → 868 | 306 → 562 | — | — |
| `F31C` chase after `E84C` (`0x44F4A8`) | 16 → 16 | — | — | — |
| `F31C` after `E84C` (`0x44F4CC`) | 47 → 54 | — | 15 → **22** | — |
| `EFC8` capital defence (`0x44F2FE`) | 87 → 128 | — | — | 20 → **32** |
| `E84C` (`0x44E918`) | 29 → 32 | 4 → 5 | — | — |
| `EBE8` (`0x44EC82`, `0x44ECDB`) | 2 → 3, 7 → 8 | 3 → 4 | 3 → 3 | — |

**C22 is settled in the measured scope.** The three callers the row names never besiege or attack in 80 rounds, now
including every recursion frame: the `E84C` walk, the chase (`0x44F4A3`) and the resupply walk (`0x44F47C`). The 37
actions belong to the army-target walk (+15 attacks), capital defence (+12 attacks), the city target (+3 sieges) and the
walk at `0x44F4C7` after `E84C` (+7 sieges). Row C22: **MATCH (iv)** at the named callers.

Two side results:
- **C23:** the walk-end resupply comes from the resupply walk 562 times, not 306. Its rows are unchanged: missing in
  code, with no measured effect.
- **The walk at `0x44F4C7`** (the `DBA8` call after `E84C`'s branch) besieges 22 times. It is not one of C22's callers.
  Whether the remake's mirror of that walk carries a City end check is not checked here.

## 2. The own-capital stays: the original's roll missed (`stays-fb7c-v1/`)

**The run:** `patches/fb7c_hook.py` on the 8 exact starts, one round each. It records:
- `war_target` for every seat: the search's result, or −1 for none;
- `war_declared` only when `Random(10)` returned 0;
- `alliance` when a relation-2 write happens.

Nation indices follow the game's order (Rome 0 … Thracia 15).

**Across all 8 rounds, the original declares no war and forms no alliance:** there are 0 `war_declared` and 0 `alliance`
records. The `war_target` results per row:

| row | seat | the original's war search | the remake |
|---|---|---|---|
| Carthage t33 | Ptolemaic | **Carthage**; roll missed | declared war on Carthage |
| Carthage t35 | Ptolemaic | **Carthage**; roll missed | war on Carthage; ally Celtiberia |
| Gaul t29 | Seleucid | **Armenia**; roll missed | declared war on Armenia |
| Ptolemaic t9 | Rome | **Illyria**; roll missed | declared war on Illyria |
| Greece t6 | Carthage | **Rome**; roll missed | declared war on Rome |
| Numidia t6, Media | Seleucid | **Armenia**; roll missed | declared war on Armenia, extended to Media |
| Numidia t11, Media and Seleucid | Seleucid | **Armenia**; roll missed | the same |
| Rome t10 | Macedonia | −1, no target | allied with Illyria, after Greece's war on Illyria |
| (Rome t10) | Greece | **Illyria**; roll missed | declared war on Illyria |

**What this settles:**
- **In 8 of the 9 rows** (all but Rome t10), the original's search found the same target as the remake's, and its
  1-in-10 roll missed. That is a draw, measured.
- **Rome t10 is a downstream draw.** The remake's alliance reason is "already at war with a shared, unprotected
  neighbour". Its precondition is Greece's war on Illyria, and in the original Greece's search found Illyria and its roll
  missed.
- **One part is not observed:** Carthage t35's alliance with Celtiberia. The hook logs an alliance only when one is
  formed, not the alliance search or its roll, so it is shown only that the original formed none.

The 9 rows therefore leave the open-rows list as **diplomacy draws (measured)**: no capital-defence, garrison or
diplomacy rule difference. The hook's absence-of-record logic rests on its Unicorn tests (4/4 per the draft), which were
not re-run here.

## 3. The late fleet rows: F608 agrees given its inputs; the stored route differs (`late-fleet-hook-v1/`)

**The run:** `patches/fleetphase_hook.py` on the Carthage game's t127, t129 and t130, from the stored starts with their
logged RandSeeds. It records `F608`'s inputs per fleet: stored route, position, moves, port, and the hunt score.

**Celtiberia's fleet 6:**

| turn | position at `F608` | stored route | moves | branch |
|---|---|---|---|---|
| t127 | (48,56) | (48,56) | 32 | stored-route (to its own tile) |
| t129 | (48,54) | (48,54) | 32 | stored-route (to its own tile) |
| t130 | **(70,66)** | (49,54) | 32 | stored-route |

- **At t127, the remake agrees with the original's `F608` inputs.** Its log has the same "fleet-6 stored-route" toward
  (48,56), written by the "zero-move mercenary rendezvous army-15".
- **The original's move to about (70,67) is not made by `F608` in these turns.** By t130's `F608` entry, the fleet is
  already at (70,66), with a new route to (49,54). So the shuttle comes from what writes the route and moves the fleet
  outside `F608`: the army phase's fleet routing (the rendezvous, or `D9A8` → `CD08`), or the stored-route walk itself,
  whose after-state the hook doesn't log.

**Ptolemaic at t130:**
- **Fleet 1:** no stored route, 27 moves, hunt −10,000, port 214, so the original's branch is **port**. The remake also
  picks port.
- **Fleet 5:** the original has a stored route (113,72) at `F608` entry, so it takes **stored-route**. The remake picks
  port. At t129 its route was (189,94); between the two entries it was rewritten to (113,72), outside `F608`.

**What this settles:**
- **Both late fleet candidates are differences in the stored route that reaches `F608`, not in `F608`'s branch.** This
  is D19 territory: who writes a fleet's route, and when.
- **The writer is not identified.** The next probe is a hook on the route writers (the rendezvous and `CD08`) in t129–t130,
  plus `F608`'s after-state.

## Intake verification (research, 2026-11-05)

**Checked:**
- **`c22c23-hook-v4/summary.json`:**
  - the per-caller counts sum to 1,525 / 571 / 49 / 64;
  - the v2 → v4 differences sum to v2's recursion bucket (435 / 258 / 10 / 27);
  - no siege or attack rows at `0x44E918`, `0x44F481` or `0x44F4A8`.
- **The disassembly:** `0x44F4C7` is a `DBA8` call reached after `E84C`'s branch (the `jmp`/`jle` to `0x44F4CC` at
  `0x44F4A8` and `0x44F4B0`).
- **`stays-fb7c-v1`:** all 8 files decoded, each one round (`turn` 1), 14–15 records. The only record kinds are
  `war_target`, and the non-empty targets are as tabled.
- **`late-fleet-hook-v1`:** the three files decoded. Fleet branches were derived with the module's `branch()` rule
  (stored route first, then moves, hunt > 100, port).

**Not checked:**
- the hooks' Unicorn tests and the 27/27 byte-identity;
- the exe hashes;
- the remake's t129 fleet log, which has no AI log;
- the end positions of the t127/t129 rows in the saves.

## Evidence

- `c22c23-hook-v4/` (`summary.json`, per-start logs, the runner log).
- `stays-fb7c-v1/` (`<start>-fb7c.jsonl`); its starts are `stays-hook-v1/starts/` and `seeds.json`.
- `late-fleet-hook-v1/` (`carthage-t127/129/130-fleet.jsonl`); its starts are `late-fleet-starts/seeds.json`.
- Hooks: `patches/d734tail_hook.py`, `patches/fb7c_hook.py`, `patches/fleetphase_hook.py`.
- Saves: release `run-exp-audit195`, `audit195-final-hooks-saves.tar.gz`.
