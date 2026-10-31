# AI diplomacy, original vs remake main: one rule gap (the trade-swap pass), everything else starts with a roll

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `eab913d` (PR #281). It
follows [`2026-10-30-ai-decisions-vs-remake-main.md`](2026-10-30-ai-decisions-vs-remake-main.md),
which left diplomacy out of its comparison.
- **Hook:** `patches/diplo_hook.py`, observation-only. It logs every relation write through
  `FUN_00449b40` with its caller, `FUN_0044fb7c`'s war candidate (`0x44FD22`) and both rolls:
  `Random(10)` for war (`0x44FD2F`) and `Random(20)` for the alliance search (`0x44FD61`).
- **Data:** `runs/experiments/data/run-exp-diplo/` (`orig-v2/`, `remake-05b02936-v1/`,
  `remake-diag-v1/`, `remake-diag-v2/`, `report-main-v2.json`, `report-diag-v3.json`,
  `diag.patch.txt`, `diag-v2.patch.txt`).
- **Release:** [`run-exp-diplo`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diplo).
- **Starts:** the 16 New Game starts, S00–S15 `*_AUTO0720.SAV`, seed 12345, 5 rounds each.
- **Remake:** main `05b02936` (T249, not released), replaying each round from the original's own
  autosave.

**Tag:** `[confirmed]`, Wine-only.

**Rerun on remake main `8e2d9053` (2026-10-31):** see [the rerun](2026-10-31-ai-rerun-remake-8e2d9053.md). With the T251 one-pass swap, 0 deterministic first divergences remain.

**Review note (2026-10-30):**
- **Release integrity:** 170 of 170 files match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain saves myself: **80 of 80** pairs are
  byte-identical. The plain saves are also byte-identical to the
  [AI-decisions](2026-10-30-ai-decisions-vs-remake-main.md) run's plain saves (80 of 80), so both
  comparisons use the same states.
- **Comparison rerun:** I ran `runs/experiments/diplo/compare.py` from a scratch copy on
  `orig-v2` against `remake-05b02936-v1` and against `remake-diag-v2`. Both outputs are
  **identical** to `report-main-v2.json` and `report-diag-v3.json`.
- **Roll counts,** read from the original logs: 107 war rolls with 8 hits, 666 alliance rolls with
  23 hits, and 27 treaty writes over a war.
- **Disassembly:**
  - The swap loop `0x44FF04–0x44FFAC` is two nested loops: partner `i` (`di`) outside, replacement
    `s` (`si`) inside, both 0..15, nation stride `0x494`, ending at `ret`. It is **one pass**, with
    no restart after a swap.
  - The war roll: `Random(10)`, and `jne` skips the war write (`0x44FD47`) unless the result is 0.
    The alliance roll: `Random(20)`, and the search runs only on 0.
  - The treaty gate at `0x44B1C4–0x44B20A`: `Random(5) < 2`, then the loser's `+0x440 > 500`, then
    its `+0x446 > 7`, then `FUN_00450c68`.
- **Remake code** at `05b02936`: `AiOwnDiplomacyRule.FindTradeSwap` (`AiOwnDiplomacyRule.cs:367`)
  returns the first `(partner, candidate)` pair from the start of the tables, and
  `AiDiplomacyPhase.ProposeOwnTradeSwap` offers it as a candidate each time the seat picks again.
- **Not re-executed:** the remake replays and the diagnostic builds, which need the .NET build. I
  also did not check that the remake's `TaxBase` is the original's `+0x44C` field.

## Answer

Over 1,280 seat-turns:

| | Remake main `05b02936` | Main + one-pass swap (diagnostic) |
|---|---|---|
| seats the same | 1,088 | 1,132 |
| first divergence: **deterministic** | **10** | **0** |
| first divergence: war or alliance roll | 21 | 25 |
| first divergence: treaty roll | 19 | 19 |
| after the round's first divergence | 142 | 104 |
| war candidates, seats before divergence | not logged | **833 of 833 equal** (82 with a candidate) |

**The one rule gap is the trade-swap loop.** In the original it is a single pass, partner `i`
outside and replacement `s` inside, both in table order:
- a partner gained during the pass is visited as `i` only if its index is above the current `i`;
- a dropped partner is never revisited.

The remake searches again from the start of the table after every swap, so a partner gained earlier
in the turn can be swapped away again. Example: S02 round 3, Media. The original swaps Illyria →
Gaul, then Bithynia → Celtiberia. The remake swaps Illyria → Gaul, then **Gaul → Celtiberia**;
Gaul, index 6, was already passed in the original. All 10 deterministic rounds are rounds 1 or 3.
A scratch patch that plans the original's single pass once per seat, after the trade loops, takes
them to **0**.

**Everything else starts with a chance roll.** The war-target search, the trade loops and the
alliance candidate agree whenever the state agrees. The roll rates are consistent:
- war: 8 of 107 rolls with a candidate in the original, 11 of 107 in the remake (10% expected);
- treaties: 27 against 31;
- alliance search: 23 of 666 in the original (5% expected).

The two games use different generators, so draw-by-draw differences are not rule differences.

**Two structural notes, with no row attributed to them:**
- The original runs a seat's diplomacy, economy, armies and fleets as separate steps. The remake's
  seat is one greedy loop by score: trades (520) and swaps (480) score below army marches (about
  1,500). A seat's own battles and their treaties can therefore come before its trades.
- The post-battle treaty gate is the same in both games.

## What this does not establish

- Rounds 6+, other seeds, and diplomacy that involves a human's choices.
- The alliance partner choice when both games hit the roll in the same seat; that did not happen
  here.
- Whether battle outcomes match; they are random draws.
- Native Windows behaviour.
