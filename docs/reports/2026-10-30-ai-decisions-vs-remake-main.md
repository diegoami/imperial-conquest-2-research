# AI army decisions, original vs remake main: 390 of 749 match; two port gaps, each fixed by a one-line patch

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `3a51439` (PR #278).
- **Hook:** `patches/decide_hook.py`, observation-only, in the army phase F31C. It logs every
  branch input.
- **Data:** `runs/experiments/data/run-exp-aidecide/` (`report-v2.json`, `attribution-v1.json`,
  `capdef/`, and `diagnostics/` with the patches).
- **Release:** [`run-exp-aidecide`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-aidecide).
- **Starts:** the 16 New Game starts, S00–S15 `*_AUTO0720.SAV`, seed 12345, 5 rounds each.
- **Remake:** main `10d3bb81`, replaying each round from the original's own autosave.

**Tag:** `[confirmed]`. The threshold edges in §4 below are `[code]`.

**Review note (2026-10-30):**
- **Release integrity:** 176 of 176 files match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain saves myself: **86 of 86** pairs are
  byte-identical (the 80 rounds plus 6 capital-defence runs).
- **Decision categories,** read from `report-v2.json`: same 378, plus 12 same but unlogged
  (= 390); resupply-city differences 260; diplomacy 44; state 16 (battle 14, death 2); remake had
  no decision 46; city target 28; branch 41; city score 20; army target 16; army score 11. The
  draft's grouping into "390 same / 252 + 8 designed / 44 diplomacy / 17 state" is its
  attribution of these categories; I did not re-derive the grouping row by row.
- **The first port gap, in the disassembly.** In F31C:
  - the city scorer `FUN_0044ece4` is called with `edx = &[esp+2]`, its city-index output (taken
    after the `push`), and its score lands in `[esp+8]`;
  - after `FUN_0044e84c` (`0x44F485`), `0x44F48A` tests army score > 70 (`0x46`) and walks to
    the army target (`0x44F4A3`);
  - otherwise `0x44F4AA` tests city score > 85 (`0x55`) and walks to city `[esp+2]`, the **city
    target** (`0x44F4C7`).
- **The second port gap, in the disassembly.** The capital-defence walk at `0x44F2F9` targets the
  threat's position. The walker's distance-1 tail attacks an army at war when moves remain
  ([tail controls](2026-10-30-walker-distance1-tail-controls98.md)), so the responder fights the
  threat, and the next responder finds it dead.

## Answer

Of 749 AI army decisions:
- **390 are the same.** The branch, both scorers, F670 and the capital-defence tests match the
  original wherever the inputs match.
- **252 + 8 come from the remake's designed #925 reachable tiers.** The raw F670 pick equals the
  original's in 14 of 14 non-adjacent rows.
- **44 diplomacy and 17 battle-or-death state differences** are left out of the comparison.
- **Two port gaps,** each reproduced by a one-line patch in `diagnostics/`:
  1. **After `FUN_0044e84c`,** the "city > 85" branch (`0x44F4C7`) walks to the **city target**
     from `FUN_0044ece4`, not to the resupply city.
  2. **The capital-defence walk** (`0x44F2F9`) ends in the threat's cell and fights it, so the
     next responder finds the threat dead (S01 Rome, S05 Seleucid).

**§4, edge differences from the code** `[code]`, not exercised:
- the capital radius in EBE8 is `< 10` in the original, against `≤ 10` in the remake;
- the offer range in E84C is `< 20`, against `≤ 20`;
- ties go by table order in the original, against city id in the remake.

**Corrections to earlier reports:**
- [`2026-10-07-strategic-ai-turn.md`](2026-10-07-strategic-ai-turn.md) §3.3, "then: defend the
  resupply city", is corrected: the army marches at the **city target**.
- The resupply values in
  [`2026-10-30-carthage-army3-branch138.md`](2026-10-30-carthage-army3-branch138.md) are
  corrected to the values after the supply pass `FUN_0044e41c`: 49 < 246, not 37 < 90. The branch
  is unchanged.

## Recheck on remake main `05b02936` (T249, #1643), added 2026-10-30

The draft gained this at ic2-conquest `main` `02b2fef` (PR #280). The same 749 original decisions
were compared with remake main `05b02936`, which ports the two gaps above. The data is
`remake-05b02936-v1/`, `report-05b02936-v1.json` and `attribution-05b02936-v1.json`; the original
side is unchanged (`orig-v1/`).

| Cause | `10d3bb81` | `05b02936` |
|---|---|---|
| same | 390 | **422** |
| capital-defence attack (gap 2) | 17 | **0** |
| city > 85 target (gap 1) | 21 | **14**, all with the army already next to the city target, then the #925 garrison or emergency tier |
| #925 resupply / fallback | 252 / 8 | 250 / 8 |
| diplomacy / state | 44 / 17 | 41 / 14 |
| unattributed | 1 | **0** |

So **outside the #925 tiers, diplomacy and battle draws, every decision now matches the
original.** The §4 boundaries and ties
([#144](2026-10-30-garrison-and-mercenary-boundaries144.md)) are not in this remake commit.

*Review:* I read `attribution-05b02936-v1.json`. Its counts sum to 749 (422 + 250 + 41 + 14 + 8 +
14) and it has 0 unattributed rows. `report-05b02936-v1.json`'s raw categories are consistent:
410 same plus 12 same but unlogged. The remake replays were not re-executed.

## What this does not establish

- Whether `FUN_0044dba8` attacks on arrival beyond the capital defence (the march contract,
  #97).
- The diplomacy differences (peace and war timing), which need their own comparison.
- The §4 edges, which were not exercised.
- Rounds beyond 1–5.
