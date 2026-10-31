# AI supply and hire pass, consolidation and merges, original vs remake main: 1,192 of 1,200 seats identical; a new gap in when the post-battle peace treaty takes effect

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `152b2f2` (PR #295), for
the rest of conquest #176 (owner request 2026-10-31). It follows the
[AI economy comparison](2026-10-31-ai-economy-vs-remake-main.md) (budgets, recruitment, tax).
Remake: main `8e2d9053`, not released.
- **Hook:** `patches/econ2_hook.py`, observation-only, with eight probes:
  - the army phase's supply and hire pass `FUN_0044e41c`: entry, each `FUN_0044f6d8` city transfer,
    each hire (`0x44E5AC`), and exit;
  - slot removal `FUN_0044ac3c` (consolidation joins and disbands, and merge slot moves) and slot move
    `FUN_0044acb4`;
  - fleet deletion `FUN_0044ad38` (the fleet merge) and fleet order `FUN_0044a004`;
  - each with its caller.
- **Starts:** the 16 New Game starts, S00–S15 `*_AUTO0720.SAV`, seed 12345, 5 End turns each.
- **Remake side:** the rerun's AI logs (`run-exp-airerun/remake-8e2d9053-v1`): the `resupply`,
  `mercenary hire`, `faithful consolidate`, `faithful merge` and `faithful fleet order` lines.
- **Comparison:** `runs/experiments/econ2/compare.py`, per seat: transfers, tons, talents, hires,
  hiring armies, joins, disbands, army merges, fleet merges and fleet orders.
- **Data:** `runs/experiments/data/run-exp-econ2/`:
  - `orig-v1/` and `smoke/`;
  - `report-v1.json` and `report-order-diag-v1.json`;
  - `remake-e41c-diag-v1/` (each army at its supply pass, all 80 rounds) and `remake-e41c-diag-v2/`
    (S10 r2, the hire gates);
  - `e41c-diag*.patch.txt`: scratch patches, never pushed.
- **Release:** [`run-exp-econ2`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-econ2).

**Tag:** `[confirmed]`, Wine-only. The treaty-timing gap is one observation in 80 rounds.

**Review note (2026-10-31):**
- **Release integrity:** 162 of 162 files match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain autosaves myself: **80 of 80** pairs are
  byte-identical.
- **Comparison reruns:** I ran `compare.py` from a scratch copy of `152b2f2`:
  - against remake main: **byte-identical** to `report-v1.json` (1,192 same, 8 differ);
  - against the table-order diagnostic (`run-exp-fleetroute174/remake-order-diag-v2`): **byte-identical**
    to `report-order-diag-v1.json` (1,194 same).
- **The hire gate, in the disassembly:** in `FUN_0044e41c`, `0x44E497` compares the nation's live
  relation toward the city's owner (+0x26) with 3, and `sete bl` keeps the result. The hire block is
  skipped when `bl` is set (`test bl,bl` / `jne` at `0x44E4E5`). So the pass never hires at a city
  whose owner is at war with the nation **at that moment**.
- **S10 round 2, checked in the original's saves** (`run-exp-econ2`, decoded with conquest's
  `state/sav.py`):
  - **Round start** (`hooked-t01-AUTO0721.SAV`): Rome and Gaul at relation 3 both ways. Rome army 0
    at (97,33) has 23,700 troops; Gaul's only army is army 9, at (96,30), with 40,500.
  - **Round end** (`hooked-t02-AUTO0722.SAV`): the relation is −18 both ways, Gaul has no army, and
    Rome army 0 stands at (97,31) with 22,989 troops.
  - **Hook log:** in round 2, Rome army 0 hires offer 14 (mercenary label 37, 4,257 troops).
- **Remake:** `PeaceTreatySystem` is declared `[GameSystem(TurnPhase.SeatEnd, …)]`
  (`PeaceTreatySystem.cs:41`). The diagnostic line at the hire reads "warWithOwner True".
- **The post-battle treaty in the original** runs inside the battle path: the gate at
  `0x44B1C4–0x44B20A` calls `FUN_00450c68` ([AI diplomacy](2026-10-30-ai-diplomacy-vs-remake-main.md),
  review note). So the treaty is in effect before the seat goes on.
- **The attack comes before army 0's own turn (follow-up, 2026-10-31):**
  - **Hook log:** Rome army 0's `e41c-in` record (seq 81, round 2) has position (97,31), where the
    round-start save has (97,33). The hire at that pass needs the war already ended. So the battle
    with army 9 at (96,30), next to (97,31), came first.
  - **Code:** `E41C` is the first call of each army's turn in `F31C` (`0x44F366`). Army 0 is the
    loop's first index, so before its pass `F31C` has called only `EFC8`, at entry (`0x44F32A`).
    So the move and attack came from `EFC8`'s capital defence or from an earlier phase.
  - Neither hook logs the routine, and the remake's log names capital defence for the same step.
    This is code-backed inference, not an observed call.
- **Not checked:** the S05/S09 detail (Ptolemaic armies 6 and 7, the +600 money) beyond the
  diagnostic comparison.

## Result: 1,200 seat-turns

| | Seats |
|---|---|
| **same on every item** | **1,192** |
| differs | 8: 5 state, 2 army order, 1 treaty timing |

What the 80 rounds exercised in the original:

| Item | Count | Seats where the item matches |
|---|---|---|
| supply transfers | 826 (50,184 tons, 171 talents paid) | 1,197 / 1,200 (talents 1,200) |
| mercenary hires | 22 | 1,199 |
| consolidation joins | 54 | 1,198 |
| consolidation disbands | 16 | 1,200 |
| army merges | 18 | 1,199 |
| fleet merges, fleet orders | **0** (none in either game) | not exercised |

## The 8 seats

| Seat | Item | Cause |
|---|---|---|
| S01 r3 Seleucid, S03 r1 Seleucid, S06 r2 Rome, S09 r5 Media, S14 r3 Seleucid | joins, transfers, a merge, tons | **State.** The seat's budget (own and threat) already differs on `8e2d9053`, from earlier differences in the round. |
| S05 r1 Seleucid, S09 r1 Seleucid | transfers and tons (original 1 transfer, 121 tons; remake 2, 272) | **The [army order gap](2026-10-31-army-order-within-a-seat.md).** |
| S10 r2 Rome | hires (original 1, remake 0) | **New gap: when the post-battle peace treaty takes effect.** |

### S05/S09 round 1: downstream of the army order

- **Original:** Ptolemaic's army 6 decides before army 7. Army 7 is still within 10 of the capital, so
  army 6's garrison fallback (`FUN_0044ebe8`) takes the nearest-city branch. Army 6 is gone after the
  round. Seleucid's army 4 reaches its supply pass with **+600 money** (army 6's purse) and +72 tons,
  needs nothing from the cities around it, and makes 1 transfer.
- **Remake:** army-7 scores higher and moves first, so army-6 marches on the capital (190,94).
  Seleucid's army-4 reaches the pass with the round-start 300 supplies and 100 money, and takes
  151 tons (its troops/100 minus its supplies, 451 − 300).
- **With the table-order diagnostic,** both seats match (1,194 same seats).

### S10 round 2, Rome: the remake applies the post-battle treaty at the seat's end

- **Original:**
  - Rome and Gaul are at war at the round start.
  - Rome's army 0 attacks and destroys Gaul's army 9, and `FUN_00450c68`'s treaty follows the
    AI–AI battle.
  - Army 0's supply pass then **hires offer 14** at Felsina (98,31), a Gaul city. Since the pass
    skips any city whose owner is at war with the nation, **the war had already ended when the pass
    ran**.
- **Remake:** the same attack, the same battle and the same `PeaceTreatyTriggered`. But
  `PeaceTreatySystem` applies the treaty at `TurnPhase.SeatEnd`, after the whole seat. At the hire,
  the diagnostic shows `warWithOwner True`, so **no hire**.
- The relation after the round is the same in both games (−18).
- **For the remake (classical-faithful, inference):** apply the post-battle treaty immediately after
  the AI–AI battle that triggers it, as `FUN_00450c68` runs. The rest of the seat should then see
  the peace: this hire gate, and also later armies' targets and war candidates.

## Also measured, and not compared

- **Own-city purse moves** (`FUN_0044f6d8`): the army's purse is capped at 1,000, with the excess
  going to the treasury, and topped up by 500 from the treasury when below 500. They are in the
  original's logs (`own_purse` in the report); the remake does not log them.
- **The consolidation's slot numbers:** the original logs the removed slot, and the remake names
  another slot (S05 r1 Seleucid: original slots 7 and 10, remake "slot 6" and "slot 9"). Only the
  counts are compared.

## What this does not establish

- **Fleet merges and fleet orders:** none occurred in these 80 rounds, in either game.
- **The hire's mercenary label and troops:** compared only as counts per seat.
- **A remake build with the immediate treaty:** not made.
- **How often the treaty timing changes other decisions:** not measured.
- Rounds 6 and later, other seeds, and native Windows behaviour.
