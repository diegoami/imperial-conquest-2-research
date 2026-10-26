# Transported army coordinates: fleet steps, unload, persistence and support timing

**Tag:** [confirmed, partial: original source and static instructions; native lifecycle open].
**Scope:** research [#41](https://github.com/diegoami/imperial-conquest-2-research/issues/41),
follow-up to settled embarked-support research; build
[#759](https://github.com/diegoami/imperial_conquest_2/issues/759).

## Answer

Every successful step through the ordinary fleet-step helper writes the carried
army's X/Y to the fleet's new X/Y. Both human and AI movement reach this helper.
Army support reads the army record, with no carrier dereference. The AI seat's
army support occurs before its fleet movement, so the same seat uses the army's
pre-fleet-movement coordinates; a later support call reads its then-current
stored coordinates. If no further position change intervenes, these are the
synchronized post-movement coordinates. This ordering is distinct from stale
coordinate behavior.

Unloading clears the fleet link and writes the army's actual landing coordinate
and underlying map cell. Save/load stores and restores whole army and fleet
records independently; the inspected loader contains no coordinate-reconciliation
loop. These are bounded source/instruction findings, not a new played lifecycle.

## Provenance and independent checks

Research-authored report from the authorized ic2-conquest peer handoff
`RESEARCH41-SOURCE-ANALYSIS.md`, SHA256
`f0f94bacbb290b42a39d4720304c084524a6551000f0f5df7dddc07b136e13ab`,
received 2026-10-21. There is no new committed bot `findings/` draft.

Research independently rehashed the complete Ghidra listing:
`2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8`;
original executable:
`9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31`.
Listing line numbers below refer to that exact source. The dump and executable
remain outside Git. Research read the boarding/unload, fleet step/walker/callers,
army support/AI phases and save routine, and independently disassembled
`0x44B79C–0x44B8D0`, `0x44DD70–0x44E094`, `0x4487C4–0x448AA4` and
`0x44E41C–0x44E4B2`. These are static reads, with no original instruction execution.
The [audit receipt](../data/research41-source-audit.json) pins scope and hashes;
it is an inspection receipt, not a test result or runtime trace.

This extends [strategic AI regions/resupply](2026-10-16-strategic-ai-regions-resupply.md)
and [foreign-city automatic resupply](2026-10-17-foreign-city-automatic-resupply.md).
Their matched aboard/land and separated-carrier controls remain historical
staged Wine/x86 evidence. They establish which record support reads, rather
than the coordinate lifecycle of a moving carrier. No legacy save or new
runtime result is claimed by this report.

## Record fields and representations

| Record | Fields | Runtime address/stride |
|---|---|---|
| Army | X/Y+0/+2; owner+4; moves+6; covered cell+8; supply+10; purse+12 |47C1EC, stride290hex=656bytes|
| Fleet | X/Y+0/+2; route target+4/+6; owner+8; launch countdown+10; moves+12; supply+14; purse+16; ships+18; condition+20; carried army index+22; covered cell+24 |49C26C, stride1Ahex=26bytes|

Army covered-cell=-1 denotes no independent map marker while aboard. It is not
an army-side carrier ID. Fleet+22 is the carried army index and is what the step
uses to synchronize. Fleet+4/+6 route-target coordinates must not be mistaken
for current fleet X/Y. Support reads current army X/Y, not either target pair.

## Boarding: restore land cell, set link/sentinel, snap coordinates

FUN0044B79C source49955–49982, parameters(army index,fleet index):

1. Fleet moves=0; fleet+22=army index (49963–49964).
2. Restore army's old map cell from army+8 (49967–49970).
3. Army+8=-1 (49971).
4. Army X/Y=fleet current X/Y (49972–49974).
5. Army moves=0 (49975).

Instructions44B7AF/44B7B5 establish fleet moves/link,44B7E9 restores old map,
44B7ED writes covered-cell=-1,44B7FB/44B806 write army X/Y,44B80A zeroes
army moves. The AI-only oversized-army trim49976–49979 is separate; use a
within-capacity control to avoid altering the subject's support capacity.

Human select/embark caller is at46601; AI boarding helper0044D9A8 calls it
at51700 when its selected fleet is adjacent. Boarding gives neither unit a
move budget to sail immediately; a natural followup must retain the actual
budget-refresh/tick boundary instead of silently replenishing moves.

## Fleet movement: shared walker, per-successful-step army coordinate writes

Human: TUnitMap_MoveHumanFleet00446E24 at46761 calls fleet walk0044E094,
with a possible second call46766 when still short of target and moves remain.

AI: fleet phase0044F608 calls route/order wrapper0044E1FC at53054/53058/53063.
Wrapper calls0044E094 at52152/52156/52162/52177 as routing requires; it can
recurse itself52169. Walker0044E094 calls step0044DD70 at52086/52103.

Successful step0044DD70 source51960–51985:

1. Check water-coded selected cell, affordability and step-cost helper<10.
2. Restore fleet old map cell from fleet+24 (51963–51966).
3. Write fleet X/Y (51970–51971).
4. Store destination covered cell in fleet+24; move old map marker into new
   map cell (51972–51973).
5. Subtract terrain cost from fleet moves (51974–51975).
6. Read fleet+22; if signed index>=0, write that army's X and Y to the same
   selected destination (51976–51979).

Exact instructions44DFA1/44DFA4 write fleet X/Y;44DFE5 subtracts moves;
44DFE9 reads fleet+22;44DFED/44DFF1 checks it>-1;44DFF9/44E001 write army
X/Y. The subsequent human-only redraw/sound gate starts44E009; synchronization
is before that gate and therefore is not limited to human-controlled movement.

There is NO write here to army covered-cell, army moves, either purse or supply,
or the fleet link. With valid boarding invariants, army covered-cell stays-1,
link stays the same, and no army marker is painted along the sea route. A
failed step's source51988–51994 does not perform either coordinate write;
the AI insufficient-moves branch may zero fleet moves only. A zero-distance
walk0044E094 exits without steps (52058–52111), so it also is not a repair/sync pass.

The step only checks that carried index is nonnegative; it does not validate
index bounds, owners or an army-side sentinel before writing. This report
describes valid linked records. It does not authorize a policy for corrupted
links or infer that all possible original coordinate mutations use this step.

## Unloading: landing coordinates become independent, fleet stays at sea

FUN0044B840 source49988–50011, parameters(fleet index,landing coordinate):

- For an AI seat only,0044939C may replace the requested coordinate with a
  nearby land cell (49996–49997); capture actual destination, not just click.
- Fleet moves=0, copy its carried army index, then fleet+22=-1 (50000–50002).
- Write army X/Y to resolved landing coordinate (50004–50005).
- Army+8=map at landing coordinate (50006–50008).
-0044A80C paints army marker (50009); army moves=0 (50010).

Instructions44B877/44B881 zero fleet moves/clear link,44B89A/44B8A2 set army
X/Y,44B8BA records covered cell,44B8C0 calls marker update,44B8C5 zeroes
army moves. The shown helper does not move the fleet's own X/Y.

Human move dispatcher00446CA4 calls it46701 for an adjacent land target and
existing carried index. AI0044E1FC calls it52184 in its adjacent land branch
with moves remaining. This bounds the next control's land/sea separation;
it is not a new claim about every UI eligibility gate.

## Save/load: whole record transport, no carrier-coordinate reconstruction

Save004484D0 source47469–47489 writes map, city table, army count and each
whole290hex-byte army, then fleet count and each whole1Ahex-byte fleet.
Thus both current coordinate pairs, army covered-cell and fleet link are stored
independently, not re-derived from a carrier at serialization.

The complete source file omits loader body4487C4 (OpenGameFile58076 calls it
as func_0x004487c4), so the load evidence here comes directly from static EXE
disassembly:

-448805–448823 restores map/cities.
-448825–448864 reads army count and whole290hex-byte records at47C1EC.
-448866–4488A2 reads fleet count and whole1Ahex-byte records at49C26C.
- The rest of4487C4 through448AA0 restores remaining saved blocks, window
  geometry and selection state; no army/fleet cross-coordinate synchronization
  loop or shared movement helper is present in this loader.

This means the loader itself restores each pair as saved, including an authored
inconsistent pair; it does not normalize it from fleet+22. Do not extrapolate
that bounded fact into a promise about arbitrary UI callbacks, corrupt-input
safety or whole-process load identity. The ordinary consistent sequence is
board -> per-step sync -> save both synchronized pairs -> load both stored pairs.
Actual native before/after files remain required for runtime confirmation.

## Subsequent support and phase order

0044FA20 source53217–53220 runs diplomacy, economy (including recruitment), army phase0044F31C,
then fleet phase0044F608. Army phase52924–52928 calls0044E41C for own armies
while no battle is active BEFORE checking positive army moves.
0044E41C source52241 loads packed army X/Y directly for each city's Chebyshev
distance test<5. Instructions44E466 loads army X/Y,44E46D loads city X/Y,
44E470 calls distance,44E475 tests5. No carrier dereference is involved.

Fleet phase53046–53063 first runs fleet support0044E5DC, then fleet movement.
Movement can change both positions after this seat's army support has already
finished. Fleet wrapper's adjacent-city support52193 is fleet helper0044F7E4,
not a rerun of army helper0044F6D8. Ordinary unloading does not itself call
the army provider scan. A later army scan uses that army's then-current stored
coordinates, whether still aboard or now disembarked.

An aboard army's AI routing0044DBA8 source51814–51818 finds its fleet from
current position, updates route target via0044CD08 and spends army moves;
it does not perform an independent land walk. Route target updates are distinct
from the current-position synchronization later in the actual fleet step.

Retain established own-stock>0, foreign-entry-purse and live-quantity rules.
Recruitment precedes army support; whole-seat treasury deltas must remain
separate from provider purchase/grant costs. The older separated-carrier Wine
control tests which record support reads, not this moving-carrier lifecycle.

## Minimal next native/original controls and remaining blockers

No new control was executed here. Suggested bounded owner-coordinated sequence:

1. Valid within-capacity pair board near one isolated provider; record both
   positions, covered cells/link, moves, supply/purse, stock, treasuries.
2. Preserve real budget refresh, sail across army support radius4->5; capture
   both pairs after each actual step and before the next army scan. Confirm
   link/sentinel retained and no independent army map marker appears.
3. Reverse geography5->4. Distinguish this seat's pre-fleet-move army scan from
   next seat's post-move scan; label any intervening weekly events.
4. Zero-fleet-move/blocked-step control: neither record's position changes.
5. Save to NEW file after movement; fresh reopen/readback pairs/link/sentinel;
   do not assume load synchronizes intentionally different inputs.
6. Unload at known land cell; record actual AI-resolved landing if applicable,
   cleared link/stored underlying map cell, army marker and both moves0.
   Keep subsequent army support separate from fleet supply.

Use retained source/native identity, unique outputs and no overwrite. Owner
coordination is required before game execution; no active game interruption.
No native lifecycle sequence or new matched moving-provider outcomes are
available from this pass. Source access is resolved; current blockers are
runtime/control evidence and normal independent review/intake, not whether a
synchronization write exists. No remake comparison or correction is selected.


Follow-up (2026-10-26): [carried-army-supply-gui79](2026-10-26-carried-army-supply-gui79.md). Six coherent stock-Wine controls now establish selected-carrier cargo supply, carrier-as-provider, actual moved coordinates and immediate Close persistence. This does not clear native Windows/full lifecycle acceptance.
