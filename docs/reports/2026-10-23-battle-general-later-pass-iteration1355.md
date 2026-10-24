# Computer general: later-pass iteration changes the owner battle's winner

**Status:** [confirmed, partial], 2026-10-23. Fresh original Wine execution,
CPU/live recorder validation and diagnostic native controls. No production fix,
native Windows acceptance or full-corpus clearance.
**Task:** [conquest #157](https://github.com/diegoami/ic2-conquest/issues/157),
following [the owner #1355 reproduction](2026-10-23-ptolemaic-seleucid-computer-general-gap1355.md).

**Research intake:** reviewed from ic2-conquest [PR #161](https://github.com/diegoami/ic2-conquest/pull/161),
merged main `b7f11a3ff9b2f93e111c5ea13b6b66e919cc6688`, finding blob `36b4cfad405bdb64596491b6c442e98f851d88f2`.
This includes the earlier PR #159 diagnostic evidence and the actual compiled
source-correction follow-up. Research's independent offline checks and limits
are recorded below; no new original/Wine run or separate model review occurred.

## Answer

**Later strict-corpus result:** the [#1377 Walk follow-up](2026-10-23-seed2-walk-captured-target1377.md)
finds one remaining hooked trajectory on the faithful-order baseline (317/318).
A separate capture-once/live-shot-guard movement correction restores318/318 state/
post and ordered-draw comparisons. This does not retroactively assign the complete
result to the four-file ordering patch alone or waive broader CI/Windows acceptance.

The original's later Computer general passes iterate in **slot order**. The
remake runs those passes in **type order, then slot order**, reusing pass one's
ordering. On the owner's mixed, interleaved army this changes movement, draw
consumption and the eventual winner.

This is a **new fixed-seed 1 control** from the owner's preserved after-End save,
not a rerun of the previous natural-RNG 48,969/20,946 survivor measurements.
The new original has the same 73,564 attacking and 78,857 defending troops but
newly generated tactical morale/placement under the declared lab seed.

| Controller | Attacker survivors | Defender survivors | Terminal counter |
|---|---:|---:|---:|
| Original, observer off or on | 0 | **51,178** | **15** |
| Production remake, actual original entry and RNG | **38,088** | 0 | 23 |
| Native diagnostic: slot order in pass three only | 0 | 52,068 | 14 |
| Native diagnostic: slot order in both later passes | 0 | **51,178** | **15** |

The last row also matches **all 498 combat draw bounds/results**, all 40 terminal
slots including names, all 168 grid cells, terminal RNG, and all 14 available
after-placement/movement boundaries at counters 2–15. These are unchanged native
unit/combat routines called with different loop ordering in a task-owned harness;
the remake repository and production assemblies were not modified.

Owner observed/plain postbattle and fresh-reopen saves, strategic turn **0756**,
and fifteen boundary saves per private runtime are retained outside Git/Drive/releases.
Owner input bytes, individual hashes, screenshots and full traces remain private.
The public scalar audit is
`runs/experiments/data/run-exp-battle-parity157/owner-iteration-audit-v3.json`
(earlier v1/v2 retained).

The earlier historical entry was also replayed as an explicitly labelled
assumption control: production gives the same **22,090 / counter 29** as before;
pass-three-only gives **40,130 / counter 23**; both later passes give
**48,969 / counter 21**, matching the original historical result. That replay
retains the earlier assumed clear claims/flags and selected=-1. It does not
invent observations of those missing historical fields or claim exact equality
of the historical event stream.

## First observed decision divergence on shared input

The existing tactical25 observer was rebuilt byte-identically and applied to
this new run. It captures actual slots, grid, actor-target claims, flags, stack,
helper/pass entries and Walk requests, rather than approximating them by polling.

All **60 individual pass-one engagements** through counter 6 agree on chosen
target, requested Walk goal and post-engage slots/grid/claim counts when each
native routine receives the original's contemporaneous input.

At counter **3**, pass three:

| Original sequence | Original next actor | Native next actor | Shared input? |
|---:|---:|---:|---|
| 74 | 0 | 0 | yes |
| 76 | 1 | 1 | yes |
| **78** | **2** | **10** | **yes** |

The inputs at sequence 78 still have identical 40 slots, grid and claim counts.
The native general chooses which unit acts next differently before its next
unit routine executes. This establishes an iteration discrepancy; it is not
an attribution from different final survivor totals alone.

Changing pass three alone restores the entire first movement phase, including
its RNG state. That variant matches measured boundaries through counter 6,
then differs at counter 7. Changing both later passes restores every measured
remaining boundary and the complete terminal tactical result in this control.

Static original checks agree: `FUN_0043A544` starts at own-first and advances
through its twenty slots; `FUN_0043ABB4` does the same for threat and flank.
The native `GeneralPassTwo.Apply` and `GeneralPassThree.Apply` instead call
`GeneralOrders.InOrder`, whose order is type then slot. Earlier tactical25 work
listed iteration as a source-backed lead; this control establishes its causal
effect on a new owner-derived case.

## Recorder and control validity

Reference input `FLD-RG_0743_rome_army0_at_86_28.SAV`, turn **0743**, seed 1,
fixture revision `6319802a75067e7730e4f6a27dce3b4e296ddd9b`:

- Fresh observer matches **325 complete reference draw tuples and 15 whole SAVs**.
- Computer-general-only and computer-general-plus-initial-End controls agree on
  all 320 combat draws and all 15 whole SAVs in that reference case.
- The first collector stopped before result acknowledgement and missed five
  post-battle draws. Its two strict failures are retained. The corrected collector
  preserves the pre-result log and adds a post-writeback log; its full check passes.
- In the owner case, observer-on/off also gives 15 byte-identical whole boundary
  saves and identical terminal slots/grid/counter/RNG. Both save and fresh reopen
  succeed byte-identically. Nation controllers were checked: human attacker,
  computer defender; placement claims are actually clear and general flags off.
- Fresh CPU checks cover existing recorder registers/flags/stack/seed, reentry,
  overflow and active snapshot payloads. They are separate from live inertness.

Production routines come from the previously pinned effective engine
`ae614899d63ac721ee46d1e3213191fe1f43a676`; live main
`8e5f0a35c9dd45a8ec31b38154406843b131013a` adds the #1356 presentation change,
with no production tactical-source difference in the inspected comparison.
The reused engine build/source receipts are in the broad #153 evidence.

Public reference binaries are archived in `reference-batch01.tar.gz`, Drive
`IC2/artifacts/run-exp-battle-parity157/`; its manifest and SHA-256 are tracked.
No EXE/DAT, prefix, registry or owner input is included.

## Full movement and exchange logs

A separately expanded observer now captures movement-step entry/exit, Walk
exit, shot/melee-pass/rout exits, removal, placement and setup boundaries through
the whole battle. It preserves original register/flag/stack/seed semantics in
the CPU checks, passes the complete reference325-draw/15-SAV live gate, and
matches all15 owner plain-control boundary files and terminal state/RNG.

The original owner trace has **2,310 semantic records**, with balanced routine
boundaries and no gaps/overflow/reentry. Independent decoding and native
comparison give:

| Action family | Original count | Both-later-pass slot-order control |
|---|---:|---|
| Actual movement steps | 162 | every actor, step, coordinate and moves-left matches |
| Shots | 108 | every bound, loss, target troops and morale value matches |
| Melee exchanges | 57 | every actor/target, focus, power, bound, loss, troops and morale value matches |
| Removals | 19 | every removed slot and its order matches |
| Combined action stream | **346** | all tuples and interleaving match |

Melee actor/focus/powers are decoded from the original's observed stack locals;
they are not supplied by the port. Shot/melee completion is observed before
the first rout call, so cascade removals cannot be mistaken for direct losses.
The complete498 combat draw sequence also matches. In the public reference,
all185 combined actions (63moves/78shots/34melee/10removals) match this control;
the production general differs later in that reference battle too.

Readable owner original logs remain private; native production and both diagnostic variants have separate
event JSONL files. Public reference logs and
`reference-semantic-comparison-v2.json` are tracked. A positive parser control
passes and five corruption controls reject sequence gaps, missing snapshots,
incorrect draw results, unknown markers and unbalanced routine boundaries.

## Declared synthetic pilot

All **12** declared synthetic strategic inputs complete original attack,
SaveAs/fresh reopen and matched-entry native replay. Each production/control
variant matches its original's full measured tactical state/result/RNG,
combat draws and available boundaries: **1,528 combat draws and 225 boundaries**
across the original cases. Nation pairs are Rome–Gaul, Ptolemaic–Seleucid and
Carthage–Numidia. Cases cover single melee/ranged/cavalry units, small mixed
formations, one slot permutation, quality4/9 and army morale50/90.

These small fixtures do **not** trigger the iteration defect. This is useful
negative coverage, not evidence that mixed battles in general agree. Original
copy-in generates each measured tactical entry; native replay starts there.
The pilot therefore tests subsequent battle behavior, not independent strategic
copy-in or JSON/export conversion equivalence. Actual tactical morale, quality
and original RNG are held equal for each engine comparison. See
`pilot-manifest-v1.json` and `pilot-audit-v2.json`.

## Limits and next tests

### Compiled source correction follow-up

The owner subsequently chose faithful behavior first, with a separately
selectable improved general investigated afterward. Remake #1355 remains the
fidelity task; [#1362](https://github.com/diegoami/imperial_conquest_2/issues/1362)
tracks the optional-controller investigation and waits on that baseline.

A four-file source correction is now prepared in
`runs/experiments/data/run-exp-faithful-general157/faithful-general-portable.patch`.
It preserves pass one's type order and uses lazy live-slot order in pass two
and all pass-three entrypoints. Original/patched source hashes are pinned to
main8e5f0a3. The patch passes read-only application checks and was compiled as
the actual engine through source overlays; no other checkout was modified.

Six focused regressions pass after the patch; the unchanged engine fails the
actual threat/shooting-order cases and lacks the new iterator. The real patched
`ComputerGeneral`, without a diagnostic replacement controller, reproduces all
14 recorded controls: **2,331 combat draw tuples, 253 available boundaries**,
terminal tactical state/RNG, reference185 and owner346 combined actions.
The historical assumption control also recovers48,969/counter21.
See that folder's `verification-v1.json` and README for receipts, preserved
preparation failures, scope and downstream acceptance still required.

This is a tested source-correction candidate, not a merged/deployed remake fix.
Full318-corpus, native Windows, independent copy-in and strategic writeback
acceptance remain open. The proposed optional general is not implemented.

This supports an **AI fidelity/order defect**. It does not measure whether the
original AI is generally stronger. No morale/training/exchange-formula change
is needed to recover this control, but independent kernels and parameter
sweeps are still needed to establish their broader fidelity.

The old prefix observer stops after counter6; the new semantic capture continues
through the full battle and actually samples selected=-1. Individual placement
write order and silent target writes are not asserted. Native strategic
writeback remains separate from tactical equality.
The v3 diagnostic's middle pass-two interval included subsequent flank effects;
those retained rows are not isolated pass-two evidence. Later versions omit it.

Further seeds, the full25-melee/15-ranged kernel matrix, full318-series corpus
and native Windows remain separate work. Historical survivor/counter recovery
above retains its explicit assumptions and is weaker than a fresh exact trace.
Upstream #1355 and conquest #157 stay open. Correction proposals belong in the
remake workflow with a minimal regression and broader corpus verification.


## Research validation of the compiled candidate

Research read the complete finding, handoff, four-file patch, regression/replay
sources, original recorder/semantic decoder, diagnostic and compiled verification
code, final records and retained preparation/collector failures. The original
source was re-read from the pinned decompile (`2018c205…87d8`):

- `FUN_0043A31C`, lines 39782–39851, loops over the type-order table and then slots.
- `FUN_0043A544`, lines 39882–39936, starts at own-first and increments one slot.
- `FUN_0043ABB4`, lines 40238–40289, traverses slots separately for threat/flank,
  with the nested pass-two calls preserved at 40271/40291.

The portable patch was applied **only to an isolated four-file tree**. Original
Git blob/SHA256 pins and all four patched SHA256 values match; the resulting
bytes equal the preserved compile overlay. It leaves `ComputerGeneral` pass one
using `InOrder` and changes five later-pass iterator call sites to `InSlotOrder`.
That iterator checks live state lazily and stops if the battle ends. No formula,
parameter, optional controller, serialization schema or sibling checkout changed.

Research independently checked 23 retained candidate binary files. The shared
actual compiled engine is SHA256
`05572a10b3b8d94fdf2ddd3bd1cc0c50de2cb5a1f2690733f4b74c54cf294771`.
The retained source-overlay build is not an official-release binary identity;
research did not independently rebuild it. The initial unchanged build after a
failed preparer remains explicitly excluded from candidate evidence.

The retained regression and replay tools were then executed **offline** against
those binaries and recorded inputs, writing only new private work outputs:

- Complete before/after regression JSON reproduces: baseline 1/6, candidate 6/6.
  Two failing-before/passing-after checks use the actual public threat and shooting
  APIs; the others cover preserved pass-one order and the iterator's side/liveness/
  battle-end behavior. These are behavioral tests, not only method-existence checks.
- The unchanged 14-control verifier reproduces the **entire** `verification-v1.json`
  byte-for-byte, SHA256
  `06f2d24a3d9a41624aaeaf47b55f12a9aecfa5f0be730e73e5fac0fcc0900b18`:
  2,331 combat draw bounds/results, 253 available after-placement/movement boundary
  comparisons, terminal slot/grid/counter/RNG checks, reference185 and owner346
  combined movement/shot/melee/removal tuples. The historical assumption control
  again gives 48,969/counter21; it remains an assumption control.
- All 325 complete reference draw tuples and 15 whole boundary SAVs freshly match
  the preserved reference corpus. Original reference/owner semantic events, actions
  and summaries are regenerated directly from their raw hook/state records and
  reproduce byte-for-byte, without using port data to infer original actions.
- Complete owner diagnostic and twelve-pilot audit outputs also reproduce exactly.
  This keeps the diagnostic result distinct from the actual compiled general.
- The expanded observer's complete CPU preservation result reproduces exactly,
  including active payload/DF/counter/capacity cases. Fresh parser controls accept
  the valid reference trace and reject sequence gaps, missing snapshots, changed
  draw results, unknown markers and unbalanced routine boundaries.
- Both public reference/pilot archives and every member (58 + 316), plus all eight
  candidate archive members, match their pinned manifests/binary hashes. Research
  verified local retained bytes, not a remote Drive download.

**Wording and acceptance limits:** “terminal state” above means all 40 observed
slots (including names), 168 grid cells, terminal counter and RNG. It is not equality
of every hidden flag/claim/controller field or strategic writeback. Draw equality
means bounds/results in order, not an original-instruction address mapping.
Three pilots (`P01-hi-duel`, `P04-heavy-cavalry-ps`, `P06-mixed`) did not record the
selected slot and default it to `-1`. The fresh owner semantic entry does record
selected=`-1`, clear actor claims and disabled initial general flags; the historical
entry's missing fields remain explicitly assumed. These samples do not settle all
controller/interruption or copy-in paths.

[Read-only intake runner](../../scripts/faithful157-intake-check.py) and
[public scalar receipt](../data/faithful157-intake-v1.json):

```bash
python3 scripts/faithful157-intake-check.py \
  --conquest "$IC2_CONQUEST" --remake "$IC2_REMAKE" \
  --artifact-root "$IC2_CONQUEST_ARTIFACTS" \
  --work "$IC2_NEW_PRIVATE_WORK" --out /tmp/faithful157-new.json
```

The work directory must be new and private: it retains full owner replay outputs
and command logs, which must never be copied to Git or public artifacts. Three
intake staging failures (namespace/dependency setup and a copied output colliding
with exclusive creation) remain in separate private work versions; the final
isolated run passes without changing source inputs or measurements.

## Consequence for earlier research

This establishes a later-pass order defect and a tested correction candidate for
the measured new seed1 owner-derived control. It advances the earlier
[unlocalized #1355 reproduction](2026-10-23-ptolemaic-seleucid-computer-general-gap1355.md)
and [tactical25 iteration lead](2026-10-16-tactical-target-and-draw-attribution.md)
at that scope. The new original winner/result differs from the historical natural-RNG
run; their counts and evidence streams must not be combined. No full-corpus residual
is declared resolved, no legacy draw/state fixture is rebaselined, and the proposed
selectable improved general remains separate.

The faithful correction still needs the remake's normal branch/review/CI workflow,
full318-series comparison, and the stated copy-in/writeback and Windows acceptance
work before broader completion claims. Research does not merge a production fix or
close remake #1355/conquest #157 by promoting this report.
