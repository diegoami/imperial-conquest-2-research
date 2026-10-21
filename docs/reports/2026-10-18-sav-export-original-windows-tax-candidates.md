# Three bound-original tax candidates: native Windows observations

**Tag:** [confirmed: native Windows, bounded tax-only subset; partial]

## Provenance and review note

Promoted from `diegoami/ic2-conquest` main
[`7fe20bedba0b9cdbb012b1b348c96507f6a65768`](https://github.com/diegoami/ic2-conquest/commit/7fe20bedba0b9cdbb012b1b348c96507f6a65768),
[draft](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/findings/2026-10-18-sav-export-original-windows-tax-candidates.md)
blob `749755e9b38b74b365669c002c2e522170530fa9`. Original publication:
[PR #104](https://github.com/diegoami/ic2-conquest/pull/104), merge
`c8193ca1ebbb8f024963c4961bac8be02e940542`, final head
`92652b03ec8ba0f1fadf25ad65e2cc2bef9db4a4`.

The [complete Kimi review/dispositions](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/docs/review-briefs/pr104-result.md)
approved reviewed head `95d906e3c2db1e2fa53a76f21fb22acb1401eb90` with three
nonblocking notes. It was static: private paths were unavailable to that
reviewer. The notes fixed the validator's three-phase comparison, disclosed
ad-hoc UI steps outside committed orchestration, and clarified case 1's separate
economy receipt. This was not an independent native replay.

**Current packet is v3.** The [packet README](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/README.md)
points to [native-packet-validation-v3.json](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/native-packet-validation-v3.json).
The draft's v2 link and 334-JSON count are historical. V3 records 336 parsed
measurement JSON files and 38 private capture hashes; the committed packet now
contains 337 JSON files, including v3 itself. V2/v3 input, stage, capture and
case-chain records agree. V3 replaces a chained inequality with three-way
byte-value distinctness, closing the possible load==post-turn!=order gap.
Research executed the actual v3 guard on synthetic counterexamples; it rejects
both duplicate-phase cases and accepts three distinct phases.

**Fresh read-only intake validation passed.** Initial attempts could not access
the historical source/candidate/output locations. The owner subsequently made
retained private native copies readable. Research reran the **unchanged
`verify_native_packet.main` function**, configuring relocated source and native
folders. The original writer directory/manifests remain unavailable: temporary
candidate-basename links **outside Git** point to retained input transport copies
whose freshly computed digests exactly match the fixed writer outputs in the
[published production-delivery receipt](https://github.com/diegoami/imperial-conquest-2-research/issues/37#issuecomment-6247428351)
for `8c31728bf4124cd87465568e4429d202ddaf2f8d`. No candidate was regenerated,
no validator condition was disabled, and no input bytes were copied by intake.
This binds accessible retained bytes to the published candidate digests; it
does not claim recovery of the missing original writer directory or manifests.

All **21 manifested stage/reference SAV files and 38 manifested PNG captures**
match their recorded lengths and hashes. The validator passes all three
sequences, current 337 measurement JSON files, script compilation, full strategic
framing and zero current original processes. Its case checks, immutable-input,
stage/capture and EXE records match v3 exactly; the JSON count is now 337 rather
than the historical 336. Fresh source/EXE hashes match too. Research additionally
compared every byte of all three candidate-transport/load and post-turn/reopen
pairs, both exact controls, and control 1's geometry masks. **This rerun launches
no game, creates no save and supplies no new native UI observations.** Capture
hashes were checked; pixels were not newly inspected by intake.

The [metadata checker](../../scripts/sav37-native-metadata-check.py) separately
checks the 337 committed JSON records, recorded chains and actual v3 guard. Its
normal/optimized results agree; corrupted phase metadata is rejected. It is
**metadata consistency only**, not the private-byte validator. The
[sanitized combined receipt](../data/sav37-native-intake.json) distinguishes those
checks from the fresh private-copy validation. No game file, private save,
capture, private JSON inventory/path or native-JSON input hash enters research Git.

## Runtime and physical writer outputs

Observed runtime: Windows NT 10.0.26200.0 x64; original EXE SHA-256
`9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31`.
File/product version metadata was null. The observation used the original
Windows game, with no Wine, memory writes, executable patches or installs.
Matching the binary hash identifies the researched executable; version metadata
alone does not establish equivalence.

All candidates were physical outputs of the separately reviewed writer in
main [PR #1202](https://github.com/diegoami/imperial_conquest_2/pull/1202),
commit `8c31728bf4124cd87465568e4429d202ddaf2f8d`. Byte-identical short private
transport copies worked around the original Open dialog's long-path truncation;
that transport failure was not a candidate-format rejection. Files remain private.

| Case | Candidate basename | Current nation / tax | Actual initial calendar | Armies / fleets | Bytes |
|---|---|---|---|---|---:|
| 1 | `t184-tax-1-n0-0.SAV` | Rome 0 / 0 | 270 Spring week 1 | 14 / 2 | 131313 |
| 2 | `t184-tax-thracia-n15-40.SAV` | Thracia 15 / 40 | 270 Spring week 1 | 14 / 2 | 131557 |
| 3 | `t184-tax-rome-n0-30.SAV` | Rome 0 / 30 | 270 Winter week 7 | 14 / 6 | 132149 |

Case 2's historical source basename contains 271; the saved/runtime year is
270. These tables use the actual scalar observations.

| Case | Candidate = initial-load/save SHA-256 | Post-turn = fresh-reopen/save SHA-256 |
|---|---|---|
| 1 | `5e85a985382dc56ae964889ed01d4fda56b0e2414ccaede5e18d03b3bd2a314c` | `96ef516dda14b154928684ad9635e9bc254aa45d52a3d3b56a65181dd618684c` |
| 2 | `2afa2d64170a63fefbf12c5678700a02024f01eb0f682a0cbc7efffa63b7288f` | `13a64beae3e90d60ad4179e24b0d51e178698347725e567af3096a2887df4498` |
| 3 | `5d82f47aa77f2736afddeac8c23754305455afa7e524636b98d12b4c2a88669a` | `3e867d29fc18a69e6e9a9d6569f3246c1dff16b2062687952b143d362e703d3d` |

The recorded equalities compare entire serialized files, including news and
trailing state. They are not an assertion that every city/unit dialog was
manually opened or that all possible queued runtime work was proved absent.

## Three observed native sequences

Each candidate completed **open → ordinary Recruit order → one End turn → new
Save As → normal close → fresh reopen → new Save As**. The ordinary action
recruited 3,000 regular light infantry, confirmed by a newly occupied queue slot
and original-save treasury/mobilization changes.

| Case | City / queue slot | Treasury | Mobilization | After the one End turn |
|---|---|---|---|---|
| 1 | Rome 85 / 4 | 2200 → 2170 | 30 → 32 | Spring 270 week 3; tax 0 |
| 2 | Byzantium 192 / 3 | 520 → 490 | 22 → 25 | Spring 270 week 3; tax 40 |
| 3 | Rome 85 / 1 | -818 → -848 | 59 → 61 | Winter 270 week 9; tax 30 |

[Case 1](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/case1-completion-v1.json),
[case 2](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/case2-completion-v1.json),
and [case 3](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/case3-completion-v1.json)
retain per-case details. Case 1's earlier cumulative 1/3 and unperformed-control
status remains a chronological record, superseded by the consolidated result.

All initially loaded with offer source -1 and sampled army/fleet/cell selectors
-1. Recorded Tax-dialog observations were tax/income 0/0, 40/262 and 30/787;
the dialogs were cancelled without a tax change. In case 3, the unused queue
slot had raw words `[24,0,0,0]` in `(state,type,troops,city)` order before the
original UI replaced it with `[0,0,3000,85]`. The draft calls 24 a type; it is
the first/state word, while the type word is 0. This does not establish any
canonical default or general semantic meaning for the unused state value.
Recruitment was permitted despite the negative treasury; no balance was patched.

Case 3's single End-turn command raised the supply warning. One confirmation
completed that pending turn, with no second menu command. A retained Python
continuation failure happened after fresh reopen/scalar sampling and before
the new save; recovery resumed the same process without repeating order/turn.
Cases 1/2 had no blocking event dialog observed. Recorded final normal quits
left zero original processes. No battle control was needed in these sequences.

Case 1's fresh-reopen Information captures were blank despite News refresh;
its reopened-state evidence is scalar sampling and whole-save equality, not
visible news text. Case 3's post-turn capture showed Winter week 9. Captures
were inspected upstream and remain private; no new visual inspection is claimed.

## Reference controls and geometry

| Control | Original tax change | Whole-file result |
|---|---|---|
| 1, owner manual | 10 → 0 | Tax plus area-map left/top changed in the control action; not byte-identical to the writer candidate. |
| 2, fresh process | 9 → 40 | Before equals original source; after equals candidate; only offset 128874 changed. |
| 3, fresh process | 20 → 30 | Before equals original source; after equals candidate; only offset 111398 changed. |

[Control 1's complete span comparison](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/control1-comparison-v1.json)
records five changed bytes **between its before/after saves**: tax at 111294,
area-map left/top at 111330–111333, from (2,72) to (1168,293). Its earlier
source-to-baseline save also moved Information-window left/top. Consequently,
**candidate versus final control** differs at eight geometry bytes: area-map
and Information-window positions. These are distinct comparisons, not extra
gameplay changes. Viewport remains (97,39). No movement cause or internal GUI
callback trace is established by these saved geometry values.

[Control 2](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/control2-comparison-v1.json)
and [control 3](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/runs/experiments/data/run-exp-sav-export37-native/control3-comparison-v1.json)
used original trackbar keyboard events/OK, scalar readback and distinct new
saves. Their complete after-save hashes equal their production candidates,
with no geometry or other serialized changes in those controls.

## Scope, reproduction and remaining gates

The committed UI scripts are not a self-contained end-to-end replay driver:
some recruitment configuration clicks and case 3's supply-warning confirmation
were ad-hoc bridge calls preserved in per-action receipts. The task bridge
identified actual owned forms; a zero-size application dummy was insufficient.
Reads of numeric process state were read-only. Private output destinations were
exclusive. Failed launches, long-path transport and recovery errors are retained.

The native tax gate is **3/3 for the bound-original tax-only profile**. The
separate native-JSON conversion/validation gate remains **0/12**: tax-only
cases count as **zero of the twelve conversions**, and native-JSON-derived
outputs still need their own original-Windows validation. See the four current
gates and aggregate-only preflight in [pending requests](../pending-requests.md#sav-export-semantic-and-native-windows-gate-research-37).

Internal GUI callback instruction traces remain **UNVERIFIED**. UNKNOWN31
remains unknown and preserved, with no padding/default or universal-unused
conclusion. General changed-state export, new-record/residue/relocation policy,
other edits, arbitrary history/profile lineage and future RNG equivalence are
not established. Bound-original provenance/edit restrictions still apply.
**Research #37 stays open.** The main project must evaluate this promoted
revision through its evidence pipeline before routing into T184–T186/#1191;
this research promotion does not grant those tasks completion or readiness.
