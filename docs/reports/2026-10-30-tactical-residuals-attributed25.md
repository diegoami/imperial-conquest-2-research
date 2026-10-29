# All 36 residual series of the 318-series tactical corpus are attributed: four main-project commits removed them

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `5621812` (PR #249). It
answers research issue [#25](https://github.com/diegoami/imperial-conquest-2-research/issues/25)
(build [#1107](https://github.com/diegoami/imperial_conquest_2/issues/1107)), delegated to conquest on
2026-10-29. Receipts are committed at `runs/experiments/data/run-exp-tactical25-attrib/`
(`pins-v1/v2/v3.json`, `attribution-v1.txt`). The runner is
`runs/experiments/tactical25-attrib/run_pins.py`. Per-series rows and fixture paths stay private.

**Tag:** `[confirmed]` as an **attribution by source change**:
- the unchanged strict #157 `Corpus.cs` (GoldenReplay plus ordered DrawComparison, no
  KnownFailures), compiled against each main-project pin's own engine and test helpers;
- run on the same private pinned corpus (revision `6319802a`);
- no game run, and no fixture, draw-bound or tolerance change.

Per-series instruction-level causality is not established.

**Review note (2026-10-29):**
- **The baseline matches the promoted inventory.** At `257f2d2` the receipt shows 318 trials,
  282 exact states, 283 exact draw sequences and 36 residual series: exactly the inventory in
  [`2026-10-16-tactical-target-and-draw-attribution.md`](2026-10-16-tactical-target-and-draw-attribution.md)
  and `pending-requests.md`.
- **The receipts match the raw runs.** I recomputed every pin's state count, draw count and
  residual set from the per-series `rows.jsonl` retained in conquest's local artifacts (not
  published). All 29 receipt entries (v1 4, v2 5, v3 20) agree exactly.
- **The attribution reproduces from the receipts:**
  - 36 → 13 at the Pass2 fix: 23 removed;
  - 13 → 2 at the threat correction: 11 removed;
  - 2 → 1 at PR1371, removing `mix-rg_s1`;
  - 1 → 0 at PR1387, removing `mix-rg_s2`.

  Along main, every later residual set is a subset of the earlier one, so nothing breaks again.
  The two main commits tested between the Pass2 branch and its integration (`305b2b1`, `b2d6b52`)
  still show 36, as they should.
- **The commits** were checked in the main project's repository; all are now on its `main`:
  - `32f3ce7` "Fix Pass2 weighted candidate eligibility and strict minimum";
  - `65cfc1f` "Correct threat movement actor shooting mode and radius";
  - `f0cd629` (PR1371);
  - `3c18600` (PR1387).
- **Corrections (both minor).**
  - The draft says the Pass2 fix was "merged into main by `30e1386`". In fact `30e1386` merges
    `origin/main` **into** the fix's branch (`task/T188-pass2-weighted-eligibility`). It is the
    first tested pin that combines the fix with then-current main, and the fix reached main later
    through that branch's PR. The attribution is unaffected.
  - The draft says "21 pins". The receipts hold **23** distinct pins: v3's 20 plus `f0cd629`,
    `3c18600` and `b593c6e` from v1/v2.
- **What this does to #25's open work.** #25's done-when was "a reviewed report establishes the
  surviving complete causal paths". At current main, none survive. The original-side trace gaps
  in `pending-requests.md` (runtime claims, the shot general pass, the 24 stopped-before-shot Pass2
  stages) are therefore not needed to attribute these 36. They may still matter for anything
  beyond this corpus.

## Answer

Each of the 36 residual series disappears at exactly one main-project commit, and none comes back
later:

| Commit | What it changed | Series removed |
|---|---|---|
| `32f3ce7`, first tested on main at `30e1386` | Pass2 weighted candidate eligibility and strict minimum | 23 |
| `65cfc1f` | threat movement actor shooting mode and radius | 11, including the state-only `ar-hi-three_s3` and `hi-ar-three_s3`, and `mix-rg_s3` |
| `f0cd629` (PR1371) | later-pass slot order | `mix-rg_s1` |
| `3c18600` (PR1387) | captured Walk target / live-shot guard | `mix-rg_s2` |

The 16 other tactical-touching commits tested change no result. At `b593c6e` (the #157 audit pin),
all 318 series pass.

**On the pinned HR6 starting case:** `mix-rg_s1` is **not** removed by the threat-actor
correction. It needs PR1371's slot order. This settles the open note in `pending-requests.md` that
the changed actor/target pair "prevents treating it as a simple range correction".

## What this does not establish

- **Instruction-level causality per series.** This is attribution by source change. PR1371's four
  files were not separated.
- **Anything beyond this recorded corpus:** natural End-turn battle entry, the deployed build and
  native Windows.
- **The intermediate pins' other behaviour.** They were built only to replay the corpus.
