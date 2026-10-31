# The original writes the ferry route for an army with 0 moves: no army-moves gate from the mercenary-run continuation to the route write

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `543f522` (PR #296). It
answers research issue [#159](https://github.com/diegoami/imperial-conquest-2-research/issues/159)
(remake #1652's zero-move case, left open by remake #1657), owner request 2026-10-31. It measures
what [fleet 0 attributed](2026-10-31-fleet0-rows-attributed174.md) had as "supported, not proven".
- **Hook:** `patches/routemoves_hook.py`, observation-only. It logs:
  - `DBA8`'s entry (`0x44DBA8`): the army, the target, the caller and the army's moves;
  - the route write (`0x44DA74`, after `D9A8`'s call to `CD08`): the fleet, the route, the army from
    `DBA8`'s frame, and the army's moves at the write;
  - the fleet phase's two probes.
- **Runs:** S06, S08 and S13 (`S06_Gaul_AUTO0720.SAV`, `S08_Celtiberia_AUTO0720.SAV`,
  `S13_armenia_AUTO0720.SAV`), 5 End turns each, seed 12345.
- **Data:** `runs/experiments/data/run-exp-routemoves159/` (`orig-v1/` logs and inert checks,
  `README.md`).
- **Release:** [`run-exp-routemoves159`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-routemoves159).

**Tag:** `[confirmed: code + Wine hook]`, seed build in Wine; no Windows claim.

**Review note (2026-10-31):**
- **Release integrity:** 30 of 30 files match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain autosaves myself: **15 of 15** pairs are
  byte-identical.
- **Disassembly:**
  - **Single callers:** in my full dump, `DB38` has exactly one caller (`0x44DC26`, in `DBA8`), and
    `D9A8` has exactly one (`0x44DB8B`, in `DB38`).
  - **`DB38` reads no moves.** It stores its two point arguments at `[ebp-4]` (the army's point) and
    `[ebp-8]` (the target), and calls `FUN_0044da88` on each. It compares the results
    (`[ebp-0x9]` against `[ebp-0xa]`, `[ebp-0xc]` against `[ebp-0xe]`), then calls `D9A8` or
    `FUN_0044d174`.
  - **`D9A8`'s gates are on the fleet:** the owner against the current nation, `+0x16 == -1`,
    `+0xA == -1` and moves `+0xC > 0`.
  - **`DBA8`:** together with my earlier reading (`si` loaded at `0x44DBC5` and compared only after
    `DB38`, at `0x44DC43`), the path from the continuation to the write has **no test of the army's
    moves**. I did not trace inside `FUN_0044da88`, which receives points, not the army record.
- **Hook logs, re-read:** I paired each route write with the `DBA8` entry just before it:

  | Start | Round | Caller of the writing `DBA8` | Army moves at entry and at the write |
  |---|---|---|---|
  | S06 | 2 | `E84C` run | 9 |
  | S06 | 2, 3, 4 | continuation, city > 85 | **0** |
  | S06 | 5 | `F31C` city > 100 | 9 |
  | S08 | 1 | continuation, army > 70 | 9 |
  | S08 | 2, 3 | continuation, city > 85 | 9 |
  | S13 | 1 | `E84C` run | 8 |
  | S13 | 1 | continuation, army > 70 | **0** |
  | S13 | 3 | `E84C` run | 9 |
  | S13 | 3, 4, 5 | continuation, city > 85 | **0** |

  That is **7 writes at 0 moves, all from the continuation**, as drafted.

## Answer

- **Measured:** in 7 route writes the army had **0 moves at the write**, each from `F31C`'s
  continuation after the mercenary run: S06 rounds 2, 3 and 4, and S13 rounds 1, 3, 4 and 5. In
  each, the moves were already 0 when the continuation's `DBA8` began, spent by `E84C`'s run.
- **The code has no army-moves test** on the path from the continuation to the write. The only
  moves condition is on the **fleet** (`+0xC > 0`).
- **S06 round 4, Carthage army 3** (the case #159 names), in order:

  | seq | Record | Army moves |
  |---|---|---|
  | 86 | `DBA8` from `E84C`'s run, toward the offer at (67,79) | 9 |
  | 87 | `DBA8` re-entering itself (same target) | 5 |
  | 88 | `DBA8` from `F31C`'s continuation (city > 85), toward the city at (121,53) | **0** |
  | 89 | **route write:** fleet 0, route (85,78), army 3 | **0** |
  | 90 | the fleet phase: fleet 0 at (85,78), stored route (85,78), 26 moves → stored route | |

- **Positive-move writes also occur:** the S08 continuations at 9 moves, the `E84C` runs, and
  `F31C`'s city > 100.

## For the remake (classical-faithful, inference)

The continuation's ferry request must not stop at zero army moves. With 0 moves the walk moves
nothing, but the rendezvous route is still written, and the fleet sails on it in its fleet phase.

## Correction to the fleet-0 report

[Fleet 0 attributed](2026-10-31-fleet0-rows-attributed174.md) said that in S06 round 5 the route
comes from "the same continuation walk". In this run, S06 round 5's write comes from `F31C`'s
`city > 100` branch (9 moves), not from the mercenary continuation.
- **Why the earlier run could not tell:** the fleet-0 hook logged only a `caller_frame`. It is the
  same value (3,275,704) for S06 rounds 3, 4 and 5, but both `DBA8` calls in `F31C` give the same
  frame. This run's hook names the caller.
- **The state is the same:** both runs' hooked saves are byte-identical to the plain build, from the
  same starts and seed.
- **So S06 round 5 is a "state" row, not a port gap,** as its own army rows ("state-battle")
  already suggested. The fleet-0 tally becomes 8 no difference, 14 state and **5** port gap.
- **Later (same day):** S08 r2 turned out to be the [seat replayed](2026-10-31-ai-seat-replayed-after-human-battle.md), so the final tally is 8 / 14 / **4 continuation at 0 moves** / 1 seat replay.

## What this does not establish

- **The embark branch** (distance 1) at 0 moves: not exercised.
- **No crafted sweep** was run; the in-play writes and the code answered the question.
- Rounds 6 and later, other seeds, and native Windows behaviour.
