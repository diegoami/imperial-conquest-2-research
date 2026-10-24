# Audited Main contains the tactical fixes and passes the recorded corpus

**Tag:** [confirmed, partial: merged-source audit, fresh current-Main builds,
strict recorded replay and native tactical tests].
**Tasks:** [conquest #157](https://github.com/diegoami/ic2-conquest/issues/157),
[Main #1355](https://github.com/diegoami/imperial_conquest_2/issues/1355).
**Status:** promoted from ic2-conquest [PR202](https://github.com/diegoami/ic2-conquest/pull/202), finding at `fd62cb58421b5fb62eae0058e676ad30e8f2fd2f`; reviewed with [PR203](https://github.com/diegoami/ic2-conquest/pull/203) qualification at `8abbdf61c1898be9d68e33d2943fcd538cf0b4ba`. Research independently rebuilt and reran the recorded checks. No production patch or issue-label change here.

## Corrected status and result

The statement that no battle fix had merged was incorrect. Main contains both:

- [PR1371 / T206](https://github.com/diegoami/imperial_conquest_2/pull/1371),
  merge `f0cd6296400f132d1387d717d5f767ace6834ad2`: faithful later-pass slot order.
- [PR1387 / #1377](https://github.com/diegoami/imperial_conquest_2/pull/1387),
  merge `3c1860079db6dd9b1fb11ceb8b726c7fd95293ac`: captured tactical Walk target
  plus positive-troop shot guard. Main #1377 is closed/status:merged.

At the audited current Main pin **b593c6e28939c1c7154f9a41d0436a8f14f352dc**, a
fresh engine and test-helper build passes all 318 recorded series for state and
ordered draws, the five fixed replays, all 14 recorded tactical-entry controls
including the owner case, and 2,420 tactical tests with zero failures/skips.
No tactical overlay, replacement general, fixture edit, tolerance change or
KnownFailures exemption is used. The current expected-failure registry is empty.

This is evidence against preparing another copy of the same patch. It does not
prove which executable the owner is running, or automatically accept #1355.
That issue remains open/status:blocked for its independent acceptance; conquest
changed no Main source, status or label.

## Source/build identity

The authoritative remote Main archive was recovered into a fresh task-owned
source copy. The sibling checkout was read-only and its task-branch HEAD was
not substituted for Main. Every source byte was preserved, including legacy
comment encodings. No build or fetch wrote another repository.

All four ordering files match the previously validated source candidate bytes
exactly: GeneralOrders, GeneralPassTwo, GeneralPassThree and ComputerGeneral.
Pass one keeps type order; pass two and all four pass-three entries use live
slot order. Current TacticalMovement captures the destination once per Walk,
passes that captured index to its checks and requires IsLive before shooting.

The corpus executable builds against the **current archived test project and
engine**, not a retained candidate binary. The recorded-entry replay likewise
compiles its production ComputerGeneral probe against this fresh engine/data.
The existing observer wrapper only records returned phase states. Three existing
Data nullable warnings are retained in the build log; probe builds are clean.
Source/assembly identities are in `source-audit-v2.json` and the corpus receipts.

## Fresh verification

| Check | Result | Meaning |
|---|---:|---|
| Strict hooked corpus | 318/318 state, 318/318 ordered draws | Original comparators called directly; no registry exemptions |
| Fixed recorded series | 5/5 | Includes the previously aliased seed2 gate case |
| Recorded tactical entries | 14/14 | 12 pilot cases, reference and owner input |
| Combat draws / boundary states in those controls | 2,331 / 253 | All match the recorded originals |
| Current tactical test suite | 2,420 pass, 0 fail, 0 skip | Test assertions, not 2,420 independent original battles |
| Focused ordering regressions | 6/6 | First-pass order, later slot order, bounds/liveness/end guards |
| Focused movement regressions | 5/5 | Captured-target and live-shot boundaries |
| Retained corpus integrity | 5,862 files unchanged | Every recovered battle file equals its pinned archive member |

Series names can alias the same recording; 318 is not an independent-scenario
count. The 14 recorded-entry controls compare all 40 terminal slots, grid, counter and
terminal tactical RNG. Where semantic logs exist, observed movement/shot/melee/
removal tuples agree, including the retained owner recording. The historical
entry assumption control also retains its old expected result, with its missing
runtime fields still explicitly assumed; it is not relabelled an observation.

The strict GoldenReplay.Passed result includes battle conclusion and comparison
of recorded post-battle fields where the series supplies a post save. Fresh-mode
series exercise production copy-in from their recorded start; Resume-mode series
use the saved block. This is not just a terminal survivor comparison.

**Coverage wording clarification:** the early scalar receipt says no strategic
copy-in acceptance. That means no newly established *natural owner End-turn to
battle* pipeline. It does not mean that fixture-start copy-in/writeback was
omitted by the unchanged GoldenReplay helper. Full-game action/RNG equivalence
and the actual owner's runtime protocol remain separate from these fixed inputs.

## Remaining acceptance, not a missing copy of these fixes

| Boundary | Current evidence/disposition |
|---|---|
| Merged tactical corrections | Both merged and present at the audited Main pin |
| Recorded engine fidelity at that pin | Fresh strict corpus and owner-entry checks pass |
| Owner's running desktop build | Identity/version not established by this audit |
| Natural owner tactical entry | Both armies, board, RNG, controller flags and protocol not freshly shown identical here |
| Whole End-turn behavior/RNG | Not claimed; prior bounded T212 strategic acceptance is separate |
| Native Windows original completion/reopen | Not newly performed; physical Escape stop remains respected |
| #1355 production acceptance | Main/owner decision; issue stays open/blocked |

The public [Windows note on #1355](https://github.com/diegoami/imperial_conquest_2/issues/1355#issuecomment-6382408367)
reports a completed fast-variant post-battle save (`B1355-WIN-AFTER-END.SAV`,
parsed turn 756), not an exact recorded tactical entry or a newly verified
unmodified-EXE round trip. Its reopen and screen/save count confirmation were
still pending in that note. No current result should silently replace those
variant/protocol limits.

Main should review this audit when refreshing #1355's blocker: it is no longer
waiting for these two source corrections to merge. Verify the actual deployed
build and the required natural-entry/writeback/native acceptance evidence under
its reviewed protocol. If a difference persists, compare the first input/event
boundary before proposing another tactical patch. Do not require full global
RNG parity where the game's documented stream design intentionally differs.
No Windows control, fresh game or unrelated paused battle was launched here.
The optional Improved general remains a separate dependent investigation.

## Evidence and preservation

Public data: [the pinned scalar package](https://github.com/diegoami/ic2-conquest/blob/8abbdf61c1898be9d68e33d2943fcd538cf0b4ba/runs/experiments/data/run-exp-battle-current157/), especially
`source-audit-v2.json`, `corpus-v1.json`, `corpus-fixed-v1.json`,
`control-replay-v1/verification-v1.json`, `input-test-gates-v1.json`, focused
regression results and `summary-v1.json`. Runners are under
[the pinned runner package](https://github.com/diegoami/ic2-conquest/blob/8abbdf61c1898be9d68e33d2943fcd538cf0b4ba/runs/experiments/battle-current157/). Engine/source pins identify the exact
build; no owner-input hashes or full states are public.

Saves cited are the retained recorded series' `BATTLE*.SAV` and post saves;
fixture revision `6319802a75067e7730e4f6a27dce3b4e296ddd9b` is unchanged. The
owner control reuses the existing private seed1 entry/terminal recording; no new
owner file is requested. All private corpus files, Original DAT/EXEs, raw
per-trial/owner traces and private manifests remain outside Git/public archives.
The public original pilot was the existing P01–P12 run, not a new game today.

Initial source scanning failed UTF8 decoding a legacy comment before its ledger
was written. The retained failure receipt documents it; the Latin1 scan does not
change raw source. No build was mislabelled a patched candidate. All results and
failed attempts are immutable/versioned, with per-batch commits/pushes. The
public audit and compilation/diff checks pass; no external reviewer was launched.
No duplicate production patch or blanket rebasing of fixtures is prepared.

## Independent Research verification and limits

Research recovered the audited Main `b593c6e28939c1c7154f9a41d0436a8f14f352dc` archive into a new private build tree. The pinned archive SHA256 matches. Against the authoritative GitHub tree for that commit, **1,228 extracted build-tree file blobs** match exactly, including test helpers and linked terrain-import tools. Four ordering files also equal the previously retained validated candidate bytes; the movement source contains capture-once, captured-index use and a positive-troop shot guard. Raw mixed comment encodings are preserved. No overlay, replacement general, source/fixture edit, tolerance relaxation or expected-failure allowance was applied.

Fresh Corpus, Replay, Regression and MovementRegression builds use this tree's engine/data/test project. Research reran all 318 hooked state/draw series, five fixed cases, 14 recorded tactical entries plus the separate historical assumption control, six ordering and five movement controls, and the tactical xunit suite. All aggregate results reproduce exactly; ordering/movement result objects and recorded-entry public verification reproduce completely. The suite reports **2,420 passed, zero failed and zero not executed**. All 5,862 retained corpus files still match their pinned archive members after execution, the Original DAT pin matches, and KnownFailures is empty. The shared engine DLL used by both corpus harnesses, the replay probes and the test project equals the fresh source-tree build byte for byte.

The [safe Research receipt](../data/current-main157-intake-v1.json) records the source/build checks, aggregate results and qualifications. Fresh assembly hashes identify these Research builds; they need not equal earlier builds at different filesystem paths. Corpus rows/errors, TRX, owner inputs, per-input hashes, complete states and semantic traces remain private. No public owner/corpus binary release is created.

**Recorded-runtime qualification:** three pilot selected-slot fields are still unobserved and use the pre-existing `−1` default. The owner selected slot was observed. Research counted these from the fresh private verification rows and reproduced the public assumption receipt; no field was backfilled or reclassified. The historical-entry control retains its missing-runtime assumptions, even though its survivor/counter check passes.

The original GoldenReplay `Passed` implementation was independently read: it requires recorded block agreement, a successful battle conclusion/writeback check, and equality of supplied recorded post fields. Fresh-mode fixtures use production tactical copy-in; Resume uses the saved block. These are fixed recorded inputs, not newly demonstrated natural owner entry, whole-game action/RNG parity, installed-build identity or unmodified Original Windows completion/reopen. Main #1355 remains open and `status:blocked`; #1377 is closed and `status:merged` at the live 2026-10-25 check. Conquest #157 stays separate and no issue labels, acceptance inventory or production code were changed by Research.

One Research preparation attempt omitted two linked terrain-tool files and failed compilation. The unchanged files were restored from the same verified archive, and new build logs were retained separately; no production fix or test failure is attributed to that setup error. Upstream's earlier UTF8 scan failure likewise remains historical. No new Original/Wine game, desktop control or owner-save request occurred. This is an independent Research build/check, not a separate model review.

For reproduction, follow the pinned README with a new private source/output tree, authoritative Main archive, existing fixture root and retained owner/historical inputs. Build the actual current-at-pin test helper project and probes; do not reuse an ordering-overlay binary. Use fresh versions for corpus/fixed runs, then verify recorded controls, tactical TRX/input integrity and the scalar audit. The upstream draft remains until conquest marks its promotion.
