# A no-offer recruitment action exposes a working carried-army Disband route

**Status:** promoted from ic2-conquest [PR219](https://github.com/diegoami/ic2-conquest/pull/219), branch `main`, source `77f4e21736670dcd7a3a8cb9221df2eccd82e0f8`, for conquest218 and the carried-Disband question left open by Research86 / residual in closed Main802. Research independently reaudited the retained evidence offline.
**Tags:** [confirmed, partial: stock-original Wine] for the controls below;
[code-derived] for caller interpretation and unplayed branches. No new Windows
or deployed Godot acceptance, remake modification or owner-policy change.

## Answer

**The original can disband an embarked army through its real GUI.** Direct
Disband after selecting its carrier is a no-op, but this sequence succeeds near
an own city when no mercenary offers are available:

1. Select the carrier.
2. Click its cargo **Recruit mercenaries** toolbar button; no offer dialog opens.
3. Click the cargo **Disband army** button before a map repaint resets selection.
4. Answer the real whole-army confirmation Yes.

The testedcargo of 5,000 troops is deleted (owner−1 tombstone), its carrier pointer
cleared0→−1, army37 talents refunded to national treasury1730→1767, and23 tons to
own Antium330→353. Mobilisation stays24. The tombstone still contains its old
5000troop record; it is not a surviving army. Normal source deletion clears the
valid carrier link, not a dangling-reference loss.

Three real-input sequences with configured0/20/150ms spacing all reached the
confirmation and same outcome. These are configured input spacings, **not a
measured maximum timing window**. A real No response leaves the army, link and
balances unchanged. Area-map panning between recruitment and Disband resets
the selection and prevents the command. Hence neither "always allowed while
carried" nor "unreachable from the GUI" describes the tested original.

## Why direct and indirect paths differ

`TUnitMap_SelectUnit004466CC` binds a fleet marker to form field+224 and clears
army field+220. `PaintForm00445D38` reselects the cursor's tile. Direct
`DisbandArmy004476AC` reads **only form+220**, so direct menu/button calls do
nothing even though `FleetButtonsOn00446188` visibly exposes the cargo buttons.
`TPremierForm_UnitMapAction0045B810` and the toolbar bind to these same callers.

`RecruitMercenaries00446FF4` resolves the selected carrier's army into+220 **before**
searching for offers. With no offer its early return skips Update/paint. The
working GUI controls observe main form `[army0,city−1,fleet2]` even while global
command selection remains `[army−1,fleet2]`. Disband captures that form army ID,
checks the own-city helper, asks confirmation, refunds, calls deletion
`0044AB90` and ends selection. The latter finds the fleet at cargo coordinates
and clears its+22 carried-army pointer before marking the army owner−1.

An explicit area-map pan calls`AreaMapClicked004462AC`→Paint→SelectUnit and
restores form `[−1,−1,2]`. Read-only sampling records+220 transitions during
ordinary GUI input; no direct handler invocation, memory write, debugger
breakpoint or executable patch is used. Earlier settled/tooltip-rechecked
no-offer sequences were negative and are preserved. The successful path avoids
intervening GUI operations that repaint the map; do not infer its state from a
later settled selection snapshot alone.

Information's retained form resource has no click/double-click selection picker.
Its key handler forwards to main map/info shortcuts; Disband menu has shortcut0.
The named writers/callbacks were reviewed, not treated as a whole-program
indirect-store/reentrancy absence proof. Supply/Change modal returns repaint and
clear the temporary army field in the tested controls.

## Separate unit-disband callers have different results

All inputs are private synthetic copies of`fleet-split-antium-0734.SAV`,turn 0734,
with coherent cargo coordinates/cell−1/carrier link,30ships, one regular HI unit of 5,000 troops
or one mercenary, purse37/supplies23. The only local own city is Antium89;
no-city controls change its record owner and marker coherently to1/37 and war.
An adjacent land partner is deliberately staged only for the transfer controls.

| Caller/control | Original result |
|---|---|
| Land Disband menu or tooltip-verified button,Yes | deletes army;treasury+37,city+23,mob unchanged |
| Direct carried menu/button,left/right fleet selection | no prompt/no resource or army change |
| Carried after unchanged Change units OK/Cancel | returned selection army−1;whole Disband no-op |
| No-offer recruitment then cargoDisband,0/20/150ms configured | real whole-army prompt;Yes deletes/unlinks/refunds |
| Same,real No | no army/link/balance change |
| No-offer then area-map pan then cargoDisband | form army reset−1;no prompt/no change |
| Change units,remove last regular nearowncity,OK | **empty owner0 army record remains;carrier still points0**;purse37/supply23 retained;mob24→21 |
| Same,final Cancel | strategic army/link/stores/mob unchanged |
| Change units,regular awayfromowncity | refusal after confirmation;unit retained |
| Change units,last mercenary awayfromowncity,OK | empty owner0 army/link retained;mob24 unchanged |
| Army transfer,disband all cargo units thenOK | deletes/unlinks empty cargo;partner gets all stores,not treasury/city |
| Same,final Cancel | strategic army/link/resources/mob unchanged |
| Actual disembark then wholeDisband | land whole-army refund succeeds;landing effects attributed separately |

For the transfer route, partner3000troops starts purse11/supply7;afterOK it
holds48talents/30tons, cargo owner−1/link−1, treasury1730/city330 unchanged,
mob24→21. The modal works on copies; its unit removal does not change global
records until OK. This is a legitimate separate way to dismiss the cargo units,
but not the same refund/accounting contract as whole-army Disband.

**Change units does not delete the emptied record.** `Disband004450C8` / remove
`004452C4` alter a working copy and mobilisation; `OK00445378` copies it back
without the explicit empty-army cleanup in `TArmyToArmy_OK00442EF8`. Both a
regular and mercenary empty cargo record survive save/reload/save, and also
separate cold Original process loads. The transfer-deleted/unlinked state also
survives a cold load. No later Endturn lifecycle is claimed.

## Evidence, audit and reproduction

Tracked [packet](https://github.com/diegoami/ic2-conquest/blob/77f4e21736670dcd7a3a8cb9221df2eccd82e0f8/runs/experiments/data/run-exp-carried-disband/); [runners](https://github.com/diegoami/ic2-conquest/blob/77f4e21736670dcd7a3a8cb9221df2eccd82e0f8/runs/experiments/carried-disband/). Plans/per-phase outputs are immutable and
versioned; original-written inputs/endpoints, full states/screenshots/identities/
private hashes stay ignored under`artifacts/run-exp-carried-disband/`. No
original binary release. Stock EXE/DAT identities checked privately in both task contexts; original source
and all existing evidence preserved.

- 23 action controls:pilot-v1(2),controls-v2(12),early-v3(3),fast-v4(4),boundary-v5(2).
- 3 separate cold Original process controls;3 same-process reload comparisons are
  explicitly separate.
- `audit-v2.json` reparses29 pairs over52 unique original-written SAVs and checks
  the whole parsed strategic world except the exact named effects and camera.
  It validates confirmations, link/stores/mob changes, working/global timing,
  no-offer preconditions and repaint transition. `audit-v1-failure.json` retains
  a wrong auditor expectation for zero-troop derived supplypercent; only that
  expectation was corrected, no original measurement changed.
- `source-sites-v1.json` records26 original sites and10 syntactic selection-store
  candidates;`resource-callbacks-v1.json` records117 bounded callback/shortcut
  rows, not full original resources/decompile. All raw original material stays
  private. Later source interpretation includes FleetButtonsOn and early return.

Primary positive endpoints:
`cd218-fast-v4_carried-nooffer-fast-20ms_before.SAV` /
`cd218-fast-v4_carried-nooffer-fast-20ms_after.SAV`,turn 0734.
Repaint countercontrol:
`cd218-boundary-v5_carried-nooffer-then-pan_before.SAV` / `_after.SAV`.
Empty-record control:
`cd218-pilot-v1_carried-change-last-ok_before.SAV` / `_after.SAV` /
`_reopened.SAV`;cold output
`cd218-cold-v1-c00_change-regular-empty_cold_saved.SAV`.

Native remake pin4d70275aac4e155c0370a3ee23525cf34450a908 was also current main
when checked. Four exact public command/handler blobs verified in
`native-source-v1.json`. Actual production dispatcher probe`Native.cs` gives
`armies.army-embarked` for the same5000troop/purse37/supply23 carried state,
leaving treasury1730/city330/link intact;per-unit disband returns
`armies.disband-unit-last-unit`. `native-v1.txt` holds exact outputs. Build
succeeds with3 pre-existing nullable warnings;no full-suite or Godot-scene claim.

## Intake / implementation handoff

This **supersedes the unresolved reachability** qualification in Research86's
manual-family sweep for the newly tested no-offer GUI path. Refresh that report
and the residual Main802 question; do not reopen the entire historical umbrella
or generalize the direct no-op into a universal restriction.

The current whole-army embarked refusal is documented as defensive/designed
without confirmed original evidence. There is now a player-facing original
counterexample and source-backed safe unlink/refund behavior. A reviewed
faithfulness/design decision should state whether to support that operation;
**do not simply remove the guard** while leaving native carrier references.
A support contract needs own-city selection,ownership/confirmation,army deletion,
carrier unlink,exact treasury/city refunds,mob unchanged,save/reopen validity,
No/Cancel and wrong-city controls. Emulating the original selection bug is a
separate UI choice from supporting the underlying valid operation.

Preserve the explicit owner last-unit refusal under565: Change units' empty
cargo anomaly is not authorization to weaken that safeguard. The transfer
modal's valid partner cleanup and whole-army refund are distinct contracts.
No owner-approved no-wrap,1340fleet safety,T207reserve,Improved affordability
orT216safe refusal policy changed;no production fix or acceptance closure here.

## Limits

Stock unmodified original, Wine10.0 Ubuntu10.0~repack-12ubuntu1,win32,two stopped
private task prefixes and fresh own1280×1024displays760/761. Nonfatal listener
warnings were checked against the recorded createdserver PID/Xlock. All game
sessions stop via own-prefix cleanup. No owner running game, native Windows,
Computer Use, Endturn,battle/AI,original patch/live memory write or sibling-repo
modification. No external reviewer. Other recruitment failure gates, unbounded
human timing thresholds, malformed links and later empty-army evolution remain
unplayed; the successful GUI path does not prove every carried context allows it.

## Independent Research verification

The unmodified audit run in a fresh private source/output tree reproduces **the complete v2 audit object exactly**: 23 action controls, three separate cold-process controls and three same-process reload comparisons, forming 29 pairs over 52 unique original-written SAVs. Reused source endpoints explain why this is not 58 independent files or 29 independent scenarios. All parsed strategic fields except the exact documented effects/camera agree; stored tombstone troops are not treated as a surviving army.

The three configured fast-spacing controls reproduce the original prompt/deletion/unlink/refunds; the recorded real No and explicit pan/repaint countercontrols retain their different results. The source runner verifies toolbar tooltips, uses ordinary pointer input and answers the actual confirmation. Read-only form sampling does not write memory or call the handler. Research rechecks these retained observations and endpoints, **not** a fresh UI experiment or a measured universal human timing threshold.

The exact source-site inventory (26 handlers, ten syntactic store candidates) and all 117 bounded resource/callback rows reproduce completely. Research re-read the no-offer recruitment early return, repaint/reselection, cargo button visibility, Disband ownership/city/confirmation, deletion unlink and the separate Change/Transfer commit paths in the pinned listing. This is a bounded caller audit, not proof that no other indirect writer, callback or recruitment failure path exists. Both task-context EXE/DAT byte identities and their retained fingerprints match the stock inputs privately; no original hashes are published.

A fresh native build from 1,242 authoritative `4d70275a` Git blobs, including the four disband command/handler blobs, reproduces both dispatcher output lines exactly: whole cargo refused as `armies.army-embarked`, last-unit removal refused as `armies.disband-unit-last-unit`. No source overlay or production change. This synthetic command comparison does not prove installed Godot behaviour or support for the corrected operation. The owner-selected last-unit refusal remains a deliberate separate policy.

The [safe Research receipt](../data/carried-disband218-intake-v1.json) contains aggregate checks and public synthetic scalar observations only. Raw original bytes, per-save hashes, full states, screenshots and traces stay private. A missing parser-helper dependency caused the first local resource-audit setup attempt to fail before output; its unchanged pinned dependency was restored and the full audit then reproduced. The source resource auditor's literal v1 output was isolated in a new tree, preserving the original; version-suffix-only follow-up does not change the measured resource rows.

This supersedes **only the prior unspecified carried-whole-Disband GUI reachability gap**. The initial Research85 direct-menu/after-Supply no-ops remain valid for those paths. Change units' empty linked record and Army transfer's delete/pool operation are distinct; neither authorizes dropping the owner last-unit safeguard. Main #802 remains a closed historical umbrella, not automatically reopened or entirely reclassified. Main must review whether and how to support the safe underlying operation, with atomic link cleanup and account/confirmation tests, rather than merely deleting a refusal guard or reproducing a transient-selection quirk.

No new Original/Wine game, cold process, desktop action, End turn, battle or Windows acceptance was performed by Research. Later empty-army evolution, malformed links, every city/caller and deployed GUI remain unproved. The source draft remains until conquest records promotion. Offline reproduction uses `audit.py --version UNIQUE`, source/resource auditors in a fresh namespace, and the unchanged native probe against the verified archived engine/test project. Do not run `run.py` or `cold_reopen.py` as part of a supposedly offline audit.
