# Pending research requests

Requests from other sessions that are accepted but not done. Whoever picks one up (any session)
removes it here when its report is promoted, and tells the requester.

## Desktop palette check (with the player, via ic2-conquest)

Asked by the research session on 2026-10-09 (the user asked). Every marker-colour result so far is
Wine-only: [`2026-10-09-owner-colours-by-band.md`](reports/2026-10-09-owner-colours-by-band.md),
[`2026-10-09-city-marker-colours.md`](reports/2026-10-09-city-marker-colours.md) and
[`2026-10-09-unit-icon-recolour-and-nation-glyphs.md`](reports/2026-10-09-unit-icon-recolour-and-nation-glyphs.md).

**Steps** (ic2-conquest `runs/experiments/data/run-exp-desktop-palette/STEPS.md`): on the Windows
original, load `colours_PRE.SAV` (`run-exp-owner-colours`) and `cities_PRE.SAV`
(`run-exp-city-marker-colours`). Use the same view, take a screenshot of the map and of the
toolbar's nation buttons, and note the display's colour depth.

**Also asked:** where the 2026-09-29 strip of
[`2026-09-29-nation-marker-colours.md`](reports/2026-09-29-nation-marker-colours.md) was cropped
from (toolbar, raw glyph bitmaps, or map), and on which system. The current reading, that it
came from raw glyphs with the white transparent margin visible, is `[derived]`.

**Expected:** the glyphs and image lists carry their own palettes, so the desktop should draw the
same 16 colours. Numidia's grey unit fill is in the code's colour table, so it should be grey
on the desktop too.

**Done when:** a desktop draft is promoted, or the player declines. Remove this entry then.

## Tactical target/draw divergences (research #25)

The prerequisite gate is now cleared at reviewed build PR #1156, merge
`257f2d2cd7510451d229a983553a54b89065b06c`, including the control correction
alongside #1103/#1105. The 318-hook comparison and recovered historical inventory
are promoted as [confirmed, partial](reports/2026-10-16-tactical-target-and-draw-attribution.md).

At that pin: 282 complete exact, 36 residual; 283 exact draw sequences. The old
42-series recovered working survey contains the historical 57-case/41-series
registry set plus `hi-ar-three_s3_r5_hook`; later 63/48 and post-T175 90 target/draw
registry entries are different snapshots/counting units, not residual series counts.

**Fresh original progress:** the [decision trace](reports/2026-10-16-tactical25-original-decision-trace.md)
reproduces all 325 legacy draw tuples and all 15 full saves in both runs, with NEW original
claims/pass observations. At half-round 6, Gaul slot 22, original and port share all decoded
slots/names, grid and equivalent claim counts immediately before choosing goals;
original (5,3) versus port (6,4) is attributable to the actor-versus-enemy archer
condition. Rankings already differ at half-round 4 but choose the same goal there. This is
an observed shared-input decision cause, not a verified full corrected battle.

**Still open:** complete corrected battle matching for all 36 residual paths. Nineteen series
have a reproduced local rule discrepancy on a model phase input, seventeen have
none in the evaluated probes. Original runtime claims and the general pass of
original shots are not in legacy logs/SAVs; these gaps cannot be filled by local
x86 execution on model state. Retain the state-only `ar-hi-three_s3` residual.

The requested `mix-rg_s1` starting case is now pinned: draw 24, HR6, site
`0x439557`, original Gaul23 -> Rome2 `Random(1085)=357`, model Gaul22 -> Rome1
`Random(172)=56`. The changed actor/target pair prevents treating it as a simple
range correction. Local threat aim/order differs, but complete causality is not proved.

**Next:** evaluate a bounded actor/enemy threat-key correction against the pinned
source rules, then perform a separately reviewed sensitivity/full comparison and
identify exactly which complete residual paths disappear. The new original trace
supplies claims/pass input through HR6 for mix-rg_s1 only; it does not fill missing
legacy fields or the other cases. Further original observations may still be needed
for other paths and the 24 stopped-before-shot Pass2 stages. Preserve immutable
fixtures/draw bounds and strict comparison behavior; no gameplay, expected-failure
or fixture change is authorized merely by promoting this report.

**Done when:** a reviewed report establishes the surviving complete causal paths.
Partial rule findings remain evidence for build evaluation; unexplained cases and
research #25 / build #1107 stay open until that attribution is established.

**Earlier owner reproduction (2026-10-23, build #1355 / conquest #154):**
[Ptolemaic–Seleucid Computer general gap](reports/2026-10-23-ptolemaic-seleucid-computer-general-gap1355.md)
is confirmed under Wine. The matched-original-entry/RNG native control still diverges;
six positions differ after the first completed movement half, before casualties.
That packet reproduced the private audit/entry checks without establishing an exact
first original instruction, cause or fix; the later control evidence below advances
that scope. Keep #1355 open. This is separate from the historical
318-hook/36-residual inventory above; no rebaseline, balance or fixture change.

**Later causal/control evidence (conquest #157, PR #161):** the
[later-pass iteration report](reports/2026-10-23-battle-general-later-pass-iteration1355.md)
establishes slot-versus-type iteration on a new fixed-seed owner-derived case.
The actual compiled four-file correction reproduces 14 recorded tactical controls,
2,331 combat draw bounds/results, 253 available boundaries and measured terminal
slots/grid/counter/RNG. Research independently reran those checks and the focused
before/after regressions, CPU preservation and parser corruption controls.
The natural-RNG historical case remains an assumption control, and the full318,
independent copy-in/writeback, native Windows and main-project review/CI remain
pending. #1355/#157 stay open; no production patch is merged by research. Owner's
faithful-first choice and the later optional controller investigation (#1362) are
separate; no optional general is implemented here.

**Seed2 movement follow-up (#1377 / conquest #157):** the
[captured-target/live-shot finding](reports/2026-10-23-seed2-walk-captured-target1377.md)
links the remaining seed2 Walk step to the later draw mismatch. Keeping the captured
destination enemy plus checking liveness before shooting yields strict318/318 state/
post and ordered-draw matches; capture-only introduces two cavalry failures.
Research reproduces all three full-corpus results, fixed-series/regr-ession/Walk
controls and27unchanged movement tests. The old36-residual inventory above remains
historical; the new candidate has zero residuals in this sampled hooked corpus.
No registry/fixture rebaseline, production merge, blanket crafted-grid fidelity,
main/Godot/solution CI or Windows acceptance is asserted. Keep the owner's separate
T206 ordering scope and #1377 movement follow-up distinct.

## SAV export semantic and native Windows gate (research #37)

The [partial safety finding](reports/2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md) establishes the live city list, historical baselines, 31 UNKNOWN nation bytes and constructor residue. It does not clear changed-state export. Main #1194/T185 stays open. An unchanged authentic identity path still requires complete-state and framing/version validation; same-template lineage does not establish safe changed-state inheritance.

**Historical next-step record (previous intake; superseded below).**

**Next:** establish the missing semantic/record-residue policy and produce applicable candidate exports without modifying private originals. With owner coordination and a native Windows runtime, open at least three distinct representative outputs, inspect state, perform an ordinary action/end turn, save each to a new copy and reopen. Preserve private inputs/outputs outside code repositories; record approved redacted/scalar evidence. No owner-private inputs, candidate paths or coordinated Windows run were supplied to this intake. Wine and self-reader checks do not satisfy this gate. Task #25 remains a separate open request above.


**Superseding status (2026-10-21):** [promoted native Windows report](reports/2026-10-18-sav-export-original-windows-tax-candidates.md)
records three physical bound-original tax candidates completing open → Recruit →
one End turn → new save → normal close → fresh reopen/new save. The native tax
gate is **3/3 for that tax-only profile**. The separate **native-JSON gate is
still 0/12**; no tax case counts as a native-JSON conversion. Internal callback
instruction traces remain UNVERIFIED and UNKNOWN31 remains unknown. This intake
verified committed receipts and freshly rehashed retained private copies with
the unchanged read-only validator. Original writer-folder/manifests remain
unavailable; retained transport digests bind the candidate bytes. No game ran.

**Current-gates handoff:** folded from ic2-conquest
[main `7fe20be`](https://github.com/diegoami/ic2-conquest/blob/7fe20bedba0b9cdbb012b1b348c96507f6a65768/findings/2026-10-21-sav-export37-current-gates-and-input-preflight.md),
blob `3bde157c4217183a32a7f05fed69babe53ae5b01`; it is a status handoff, not
a new native result. Its aggregate-only upstream inspection found 12 JSON files,
11 unique hashes (two byte-identical files), 11 format 4 and one format 7,
null source provenance in all 12, 16 nations/334 cities each, turn indices 0–6,
and the expected save78 basename absent. This is not proof of the authoritative
twelve-input selection and was not independently reopened by this intake.
No private path, individual native-JSON hash or private inventory is included.
Do not silently substitute/rename files or drop the duplicate-content input.

The handoff records main PR1202 merged on 2026-10-20 at `e5f1bd76802ef583cf48a63c7582ee87b80a586a`;
that writer groundwork does not complete the native writer/export bridge.
Research #37 remains open. Four gates remain:

1. Confirm the authoritative **twelve-input manifest**, including any rename or
   content equivalence; preserve each input identity and source unchanged.
2. Complete the applicable **UNKNOWN/new-record policy**, history/profile,
   inactive/text residue, record ordering/relocation and carrier representation,
   or define evidence-backed refusals. No arbitrary template inheritance.
   **Status 2026-10-22:** the policy is answered by the
   [gate-2 export policy](reports/2026-10-22-sav-export-gate2-policy.md) (ic2-conquest `80a3963`),
   promoted provisional. The one checker defect found at intake (the allegiance refusal was not
   enforced) was fixed upstream in `2fd663a`, and the fix is verified here.
3. Independently review **T185 migration/export** (format 4 → current), checked
   capacities/encoding/indices and no-overwrite publication before candidates.
4. Validate supported outputs from **that native-JSON set**: independent decode,
   deterministic/rejection/full-suite checks, then the required original-Windows
   order/End-turn/new-save/fresh-reopen gate. Existing tax-only 3/3 does not waive it.

The main project evaluates the promoted revision and routes evidence into
T184–T186/#1191; no Evaluated marker or downstream completion is asserted here.

**Separate conversion progress (2026-10-23, conquest #151):** the
[six-scenario/seven-session report](reports/2026-10-23-remake-original-save-conversion-roundtrips.md)
records generated remake JSON → original Wine → remake acceptance. Research
reproduced the full comparison/audit, 164 archive-entry hashes and thirteen policy
passes. It is not the owner's twelve-save set, format-4 migration, T185 review or
native Windows validation; none of research #37's remaining gates is waived.
Research #63's quality-range work is separate. No new game ran during intake.

**Broader generated-input evidence (conquest #153):**
[77 strategic round trips](reports/2026-10-23-broad-save-conversion-matrix.md)
cover all16 nation starts, four progressed states, 56 feature cases and one synthetic
format4 migration; 12 converter/input refusals remain safe. Four deterministic
action gaps and the known conqueror-history import loss are explicitly retained.
Research reproduces the full comparison/coverage/audit and freshly passes 154 policy
checks. This expands Wine evidence; it neither validates the owner's twelve inputs
nor clears the native Windows gate or establishes tactical outcome equivalence.

## Crafted battle-grid fidelity (research #40)

[Source and retained-save audit](reports/2026-10-21-crafted-battle-grid-movement-and-line.md)
identifies stored-icon movement (c5/c6/d5) and equal-coordinate clear-line false
(d6), with an operation matrix and exact legacy save hashes. The intermediate
first write/branch is source-derived; later Wine save boundaries are observed.
Next: reviewed bounded build correction including explicit GeneralLine ownership,
then immutable complete comparisons and ordinary-grid controls. Additional grid
gates and combat repaint ordering remain separately scoped. No corrected replay,
native confirmation or natural occurrence is established; #40/#1106 stay open.

## Transported-army coordinate lifecycle (research #41)

[Source lifecycle report](reports/2026-10-21-transported-army-coordinate-lifecycle.md)
locates successful-step army/fleet X/Y synchronization, unload writes, independent
whole-record persistence and army-support-before-fleet-movement order. This
extends the settled aboard-support matrix without repeating it. Next: coordinated
native Windows near-to-far/far-to-near carrier movement, budget-refresh and blocked
controls, saveNEW/reopen and actual landing observations with both records and
provider/accounting fields. Static evidence does not complete those controls;
#41/build759 remain open. No remake correction is selected by this report.

## Strategic lateral steps and callers (research #42)

[Promoted source/x86 finding](reports/2026-10-21-strategic-lateral-steps-and-callers.md)
settles cheaper-lateral selection, first-after-swap ties, final-destination bypass
and post-selection affordability. Separate army/sea helpers and human/AI callers
are pinned. Independent11-step/2-walk rerun reproduces the retained JSON exactly;
redraw/sound stubs and synthetic parent frames are explicit. Next: narrowly
owned build evaluation with normal/contact/endpoint/edge controls and separately
coordinated native routing evidence. Historical C4 Wine totals remain endpoints,
not observed crossed tiles; #42/build1012 stay open. Contact#5 remains separate.


## Strategic target eligibility, routing and resupply (#1388 / conquest #171)

[Owner routing control](reports/2026-10-24-seleucid-strategic-target-routing1388.md)
and [generated-input pilot](reports/2026-10-24-strategic-fidelity-pilot171.md) are
promoted as bounded source/instruction/retained-observation findings. Research
reproduced their audits and conditional tools; the original own-city selector
correction is applied in strategic-ai-turn §3.3 and the rules specification.
This does not require a new low-level land-step rule: the owner control's21steps
already match when given the original intermediate destination.

Remaining downstream work is original navigation data/eligibility plus wrapper
routing, faithful selector evaluation and broader same-input strategic families.
The112pilot decision states are correlated snapshots, not112campaigns. Full native
greedy selection, homeland/fleet/economy/diplomacy/recruitment decision+global RNG
comparisons, all16starts/continuations and Windows acceptance remain open. No
production correction, battle/ex-port gate closure or optional Improved-policy
change is selected by this intake. Research42's terrain-step/native routing limits
and contact5 remain separate.


## Fleet state, accepted actions and movement (conquest #174)

The [stored-destination finding](reports/2026-10-24-strategic-fleet-controls174.md)
and [accepted-movement follow-up](reports/2026-10-24-fleet-accepted-movement174.md)
are distinct bounded intakes. The follow-up confirms that native fleet approaches
can be accepted commands, while original fleet-phase and native full-seat histories
remain incomparable as whole turns. Fresh offline original/native controls reproduce the budget counterexample at the retained build. Main #1408 is now closed and `status:merged`; no post-fix build was tested here.

Main [#1408](https://github.com/diegoami/imperial_conquest_2/issues/1408)
holds the merged narrow budget correction;
[#1409](https://github.com/diegoami/imperial_conquest_2/issues/1409)
separates faithful selection and waypoint execution from intentionally designed
sailing policy;
[#1405](https://github.com/diegoami/imperial_conquest_2/issues/1405)
retains stored-route state support beyond v0.8 by owner decision. Disembarkation,
capacity, provider thresholds, route lifetime, naval combat, global RNG and
native-Windows acceptance remain unproved. The [navigation-rule intake](reports/2026-10-24-army-navigation-rule187.md) now supplies static data and a bounded eligibility/first-destination contract for conquest #187. Main #1394/T212 remains open and `status:blocked`: F31C continuation is covered, other caller histories are not. No new caller experiment is authorized by this intake.

## New continuation packet awaiting intake

Conquest [PR190](https://github.com/diegoami/ic2-conquest/pull/190), source `71294186`, was relayed while the #174/#187 consolidation was under review. Its economy/diplomacy/fleet continuation and cargo-overflow claim (Main #1412) are **queued, not promoted or independently verified here**. They are separate from the bounded fleet-at-sea cargo and navigation findings above.
