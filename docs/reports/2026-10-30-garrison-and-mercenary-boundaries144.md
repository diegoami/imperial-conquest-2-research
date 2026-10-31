# Garrison fallback (FUN_0044ebe8) and mercenary-run offer (FUN_0044e84c): strict < 10 and < 20, first record wins

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `de94c3a` (PR #279). It
answers research issue [#144](https://github.com/diegoami/imperial-conquest-2-research/issues/144)
(remake #1640), routed to conquest on 2026-10-30. It follows §4 of
[`2026-10-30-ai-decisions-vs-remake-main.md`](2026-10-30-ai-decisions-vs-remake-main.md).
- **Original side:** `runs/experiments/boundary144/controls.py` (Unicorn on the #187 snapshot,
  stopped at the `FUN_0044dba8` entry, no RNG).
- **Remake side:** main `10d3bb81`'s `GarrisonFallback` and `MercenaryRunDestination`, run on the
  same synthetic states through the new `RemakeAdapter helperprobe`.
- **Data:** `runs/experiments/data/run-exp-boundary144/` (`controls-v1/v2.json`,
  `native-10d3bb81-v1/v2.jsonl`, `city-record-ids.json`).

**Tag:** `[confirmed]`: executed controls on both sides. Nothing here is a claim about play or
native Windows.

**Remake main `8e2d9053` (2026-10-31):** the three corrections are in, faithful-only; 28 of 30 controls now match, and the two left are the capital −1 case below. See [the rerun](2026-10-31-ai-rerun-remake-8e2d9053.md).

**Review note (2026-10-30):**
- **Disassembly:**
  - `0x44EC3F` is `cmp ax, 0xa; jge` past the near-capital flag, so the test is strict **< 10**;
  - `0x44E884` is `cmp ax, 0x14; jge` past the offer, so the test is strict **< 20**.
- **Original controls rerun:** I ran `controls.py` from a scratch copy with output redirected, for
  both layouts (`v1`, and `land` = v2).
  - `controls-v2.json` is **identical**.
  - `controls-v1.json` differs only by the `layout` field that the later script adds; every result
    is identical.
- **Both sides read row by row:** 16 original rows and 15 remake rows. Every claim below matches.
- **The remake probe was not re-executed** here, since that needs the .NET build.

## Answer

| Control | Original | Remake main `10d3bb81` |
|---|---|---|
| EBE8, capital distance 9 / 10 / 11 | nearest city / **capital** / capital | nearest city / **nearest city** / capital |
| E84C, single offer at 19 / 20 / 21 | taken / **none** / none | taken / **taken** / none |
| E84C, pair 19 vs 20 (either slot order) | 19 | 19 |
| EBE8 tie between two cities | the **first city record** (olisipo, record 1) in both position layouts | city id (ebora) both times |
| E84C tie at distance 5 | the **first pool slot** (201 before 202) in all 4 slot × record permutations | city id (ebora) every time |

**Helpers:**
- `FUN_00449018` is the Chebyshev distance.
- `FUN_004498d8` returns the city **at exactly** a position (the first in table order), or −1. It
  is not the nearest city.
- `FUN_00448fd0` is min.

**Tables:**
- EBE8 follows the **city record table** (`0x479590`).
- E84C follows the **mercenary pool** (slots 201–250 at `0x49D0A4`).

**Ambiguities, reported before any correction is chosen:**
- **EBE8 has no capital guard.** With capital −1 it reads city record −1: (153,48) in the control.
  The remake returns null.
- **E84C has no −1 guard** after `FUN_004498d8`. This is code only.
- **EBE8's nearest-city loop has no eligibility gate,** so a "no eligible city" control does not
  exist.

**The owner's #925 policy is kept separate.** On layout v1, the remake's `GarrisonFallback`
returned null everywhere, because of the retained reachable-fallback policy. Layout v2 is a free
land strip where that policy accepts every candidate, so the `≤` and city-id differences show up
literally.

## What this does not establish

- What happens with record −1 for an offer that is not on a city; this is code only.
- Play or native Windows behaviour.
- **A label error:** the v2 absent-capital row's label says the army is 20 from the old capital;
  it is actually 8.
