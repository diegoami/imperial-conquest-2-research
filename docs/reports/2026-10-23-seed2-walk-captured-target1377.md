# Seed2 residual: preserve the captured destination enemy, but never shoot it dead

**Status:** [confirmed, partial], 2026-10-23. Fresh original Wine semantic trace,
conditional native replay and strict full318 corpus controls. A tested source
candidate at the original packet; native Windows acceptance remains separate.
**Tasks:** [remake #1377](https://github.com/diegoami/imperial_conquest_2/issues/1377),
[conquest #157](https://github.com/diegoami/ic2-conquest/issues/157), related #1324.
This follows the accepted-scope T206 ordering correction; it does not impose a
new hold on that separately approved bounded fix or start Improved policy tuning.

**Research provenance:** reviewed from conquest [PR #165](https://github.com/diegoami/ic2-conquest/pull/165),
merged main `e1a943d5f9de8b88787112f137ad8053a699e6e0`, finding blob `8e5fe73982c14d22f911807f0750d84122ec56e7`.
The complete research checks and their limits are recorded below. No new original/Wine
execution or separate model review is claimed by research.

**Production status, 2026-10-25:** [Main PR1387](https://github.com/diegoami/imperial_conquest_2/pull/1387) merged at `3c1860079db6dd9b1fb11ceb8b726c7fd95293ac`; #1377 is closed/status:merged. The [fresh Main audit](2026-10-25-current-main-battle-replay157.md) independently builds pin `b593c6e2` and reproduces all318 strict state/draw series with an empty failure registry. This does not establish installed desktop identity, natural owner entry or #1355/Windows acceptance. Historical measurements below are unchanged.

## Answer

The later seed2 mismatch is a movement-control defect. The original captures
the enemy at the requested destination once for a Walk. The remake looks it up
again after each shot. If shooting routs that enemy, the remake sees an empty
destination and can take a step the original does not take.

A capture-only correction is incomplete: the original also tests that its
captured enemy is still alive before shooting. Keeping the index without that
guard introduces shots at an already removed unit, extra Random(1) calls and
incorrect rout/morale effects. Restoring both controls matches all318 hooked
series' strict recorded-state/post checks and ordered draw streams.

| Compiled engine control | State/post matches | Ordered-draw matches |
|---|---:|---:|
| T206 faithful-order baseline | 317/318 | 317/318 |
| Capture destination once, without live-shot guard | 316/318 | 316/318 |
| Capture once plus original live-shot guard | **318/318** | **318/318** |

These use the unmodified upstream `GoldenReplay` and `DrawComparison` helpers,
not the KnownFailures registry. No expected-failure exemption, fixture change,
range substitution or comparison tolerance is used. Fixture pairing is checked
before every trial, and errors fail the result. State/post comparison means the
fields checked by those upstream helpers, not every hidden original runtime field.
The five fixed series also pass strict replay, including `gate2_s2a` explicitly;
the baseline passes4/5 and fails that exact gate alias. All27 unmodified upstream
movement/exhausted-movement tests pass on the complete candidate, with no skips.

## Three reported comparisons, one original trajectory

The #1377 comparisons are hooked `mix-rg_s2_r5_hook` state and draws, and fixed
`gate2_s2a` state. Their **18 boundary saves and post save are pairwise
byte-identical**, verified from pinned fixture6319802 and their retrieved bytes.
They share the same strategic start, seed2 and armies. These names are two
fixture aliases, not independent battle reproductions.

Start: `FLD-RG_0743_rome_army0_at_86_28.SAV`, strategic turn **0743**, Rome army0
against Gaul army10. A fresh semantic observer run `seed2-residual-v1` matches
all **325 original draw tuples and 18 entire boundary SAV files**. The reader
has no overflow/reentry, has complete sequence/RNG checks and balanced routine
boundaries. Its observation code is byte-identical to the validated seed1
observer; only two fixed-seed immediates change from1 to2.

The fresh `seed2-residual-v1-AFTER.SAV` and fresh-process
`seed2-residual-v1-REOPEN.SAV` are byte-identical to each other. New outputs and
all earlier measurements are preserved. No EXE/DAT, owner input or full private
corpus is published.

## First causal difference

All **49** original Walk calls were separately replayed through the T206 native
`TacticalMovement.MoveUnit`, using each actual original's slots, grid, claims,
controller flags, requested destination and RNG state. Exactly one differs:
counter10, Gaul slot24, original sequences **874–891**, goal **(10,3)**.

1. Slot24 starts at(12,4), troops5596, moves4 and shots4. The goal contains Rome
   slot1, a heavy-infantry unit with621troops.
2. It steps to(11,3), spending one move. Both engines agree.
3. It shoots slot1 with bound252 and losses323, then bound150 and losses190.
   The target goes621→298→108 and routs below its floor. Both engines agree on
   those draws, losses, morale and removal. Slot24 now has moves1 and shots2.
4. The original keeps captured slot1. Its adjacent/last-move branch assigns
   target1 even though that unit has just routed, and stops at(11,3), moves1.
5. The native lookup sees the cleared cell, discards that reference and steps
   into(10,3), moves0 and target−1. That is the first differing movement action.

The conditional replay still has **the same RNG state** at this point: the
extra step itself draws nothing. The changed position alters a later shooting
opportunity. The first differing global draw is217/counter11: original melee
site0x439557 draws Random(361)=333; native instead draws Random(113)=104 for a
shot. Those are different actions, not evidence that equal-input melee arithmetic
uses a different formula. Do not force the old bound into the new shot.

The guarded correction matches **49/49 Walk endpoints/RNG states** and the full
**178-action interleaving**:67 movements,62 shots,38 melee exchanges and11 removals.
It reproduces original Gaul23,431survivors/counter18; the baseline had Gaul23,667
at counter16. Both sides' observed terminal slots/grid/counter/RNG are compared.
The original post-rout snapshot at sequence890 also matches an actual native
observer snapshot on all40 slots/names, grid, claim counts, counter/side and RNG
before the different next action; see `causal-proof-v1.json`. GUI Selected and
unobserved machine fields are not asserted equal.

## Why the earlier capture-only control conflicted

The incomplete control fixes the mixed seed2 case but introduces two exact
residuals:

- `lc-ar-three-half_s1_r5_hook`: BATTLE09 slot0 morale75 versus original70;
  draw29 takes Random(1) where the original proceeds to promotion Random(4).
- `lc-ar-three_s2_r5_hook`: BATTLE11 slot0 morale80 versus original65;
  draw108 takes Random(1) instead of the original shooting Random(366).

The dead cached unit is being shot and routed again. The positive-troop test in
the original Walk at **0x438ED1**, before its shot call at0x438EE2, supplies the
missing guard. This explains the historical "capture helps mix-rg but breaks
two cavalry cases" lead without changing morale, quality or damage coefficients.

Five small native regressions give baseline3/5, capture-only4/5 and complete5/5:
last-move retention, no shooting a dead captured target, normal live-target
engagement, unchanged human movement, and defender symmetry. These are native
regressions against the original control-flow contract, not additional fresh
original synthetic-game executions.

The complete source candidate also retains the prior **14 recorded controls**:
2,331 combat draw tuples,253 available boundaries, reference185 and owner346
combined actions, plus the explicitly assumed historical48,969/counter21 control.
Owner inputs, hashes and full replays stay private.

## Reproduction and limits

Evidence: `runs/experiments/data/run-exp-battle-residual157/`, especially
`original-gate-v1.json`, `fixture-recovery-v1.json`, `walk-before-v1.json`,
`walk-cached-live-v1.json`, the three `corpus-*-v1.json` files,
`movement-regression-*-v1.json`, `seed2-cached-live-action-comparison-v1.json`
and `control-replay-v1/verification-v1.json`.
Original raw logs are retained under
`runs/experiments/data/run-exp-battle-parity157/seed2-residual-v1/`.
The source candidate is `movement-cached-live.patch`; `movement-cached-only.patch`
is a deliberately incomplete experimental control and must not be deployed.

Native source is pinned to the T206 correction candidate plus one movement-file
overlay. The original's two-control behavior is source-backed and observed in
the fresh Wine trace; corpus helpers execute the real compiled engine. Build
outputs and fixtures are outside Git; all raw text results are retained.
This session never modifies another repository's source.

Research intake, normal remake PR/CI, the wider golden-master/Godot/solution
checks and native Windows acceptance remain separate. All318 hooked series
matching does not establish every crafted-grid behavior or all game fidelity.
#1377/#1355 are not closed by this candidate, and no fixture or known-failure
registry is changed here. The owner's approved T206 scope split remains intact.


## Research intake verification

Research read the full final finding and source candidate, original Walk body and
instruction listing, strict corpus/fixed-series runner, regressions, Walk probe,
recovery/control scripts and the final per-trial records. Both source variants
were applied only to isolated copies and checked against their preserved source
identities; the incomplete control is not an approved production alternative.

The original pinned EXE (`9d753d5d…ba31`) confirms capture at `0x438D66` and the
positive-troop test/JLE at `0x438ED1–0x438EDA`, before the shot call at `0x438EE2`.
The pinned decompile (`2018c205…87d8`), `FUN_00438D24` lines38739–38801,
shows the destination enemy resolved before the loop and the liveness guard only
on shooting. In particular the adjacent/last-move target assignment can still
retain the captured index after routing; moving the liveness guard around the
whole computer check would not reproduce that branch.

The unmodified upstream helpers were inspected and their five recorded source
hashes checked. `GoldenReplay.Passed` requires matching blocks, a successful battle
conclusion/writeback and no checked post-state difference. The corpus runner calls
those helpers directly, with no `KnownFailures.Check`/registry acceptance. Ordered
draw equality checks count, bound and result; it is not original caller-address or
hidden runtime-field equality. Fixed-series mode checks state/post, not a second
independent draw corpus. The fixture aliases are not additional independent evidence.

Research freshly reran the retained compiled controls offline and compared whole
summary and per-trial records rather than only their headline counts:

- Baseline:317/318 state and draws; capture-only:316/318; complete:318/318.
  Each entire summary and JSONL trial stream reproduces byte-for-byte, including
  the preserved baseline/incomplete failures. No registry exemption or tolerance.
- The five fixed series reproduce baseline4/5 and complete5/5. The explicit
  `gate2_s2a` state failure is recovered by the same complete correction.
- The five focused native regressions reproduce3/5,4/5 and5/5. The dead-target
  case rejects the incomplete correction; human behavior and defender symmetry
  remain covered. These are offline native tests, not new Wine synthetic runs.
- All49 conditional Walk replays reproduce the retained detailed results: one
  differing baseline Walk, none on the complete candidate, with endpoint RNG
  equality. This is conditional execution from contemporaneous original state,
  separate from the autonomous full-corpus battles.
- The full autonomous seed2 replay and178-action comparison reproduce in full;
  original events/actions/summaries regenerate byte-for-byte from raw hook/state
  records. The post-rout common-state proof was independently recomputed on all40
  slots/names,168cells,claim counts,counter/side andRNG, with only Selected/unknown
  fields excluded. The observer images differ only in the two1→2seed immediates.
- The prior14-control verification reproduces in full, including2,331 combat
  draw bounds/results,253available measured boundaries, reference185/owner346
  action tuples and the expressly assumed historical control. Its three pilots
  with unrecorded Selected defaulting to−1 retain that limit.
- All27 unchanged upstream movement/exhausted-movement tests pass, with zero
  skips. These are the scoped suite, not the full solution/Godot/main CI.
- The fresh original recorder gate reproduces all325 tuples and18 whole SAVs;
  the two fixture aliases agree on18boundaries pluspost. Recovered selected bytes
  match their pinned Git blob/digest records. No original fixture was changed.

The three public archives and all92members were checked against their pinned
inventories/digests. They exclude original EXE/DAT, the full private corpus and owner
inputs/traces. Research verified retained local bytes, not a Drive download.
Upstream GitGuardian **skipped** the large evidence PR (neutral); this is not a
passing scan claim. Local privacy/source-preservation checks are separate evidence.

[Read-only intake runner](../../scripts/walk1377-intake-check.py) and
[scalar research receipt](../data/walk1377-intake-v1.json):

```bash
python3 scripts/walk1377-intake-check.py \
  --conquest "$IC2_CONQUEST" --remake "$IC2_REMAKE" \
  --artifact-root "$IC2_CONQUEST_ARTIFACTS" --exe "$IC2_EXE" \
  --work "$IC2_NEW_PRIVATE_WORK" --out /tmp/walk1377-new.json
```

The work directory must be new and private: full corpus/control logs and owner
replay outputs must not enter Git/public artifacts. No new original game, Wine run,
independent rebuild, production source/registry/fixture edit or separate model review
occurred. An initial intake staging failure is retained separately; it changed no
measurement or source input.

## Relationship to earlier accepted work

This extends the [later-pass ordering evidence](2026-10-23-battle-general-later-pass-iteration1355.md)
with a separately scoped movement correction and full strict hooked-corpus result.
The older [tactical25 inventory](2026-10-16-tactical-target-and-draw-attribution.md)
remains a pinned historical result; its36residual count is not the residual count
of this new candidate. The endpoint-only state discrepancy and later draw mismatch
are linked by the shared-state Walk observation, not by substituting one random
range into a different action.

The original promotion established bounded control flow and a tested candidate. Main #1377 is now merged, and the later audit validates the retained corpus/current-at-pin engine; installed deployment, Main #1355 acceptance and Windows work remain separate. Broader crafted-grid/controller coverage remains outside this result. This does not reinstate
a hold on the owner's separately approved bounded T206 ordering fix, and Improved
controller policy remains a different task.
