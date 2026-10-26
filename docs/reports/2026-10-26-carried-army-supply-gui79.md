# Supply army through a selected carrier targets its cargo and can use that carrier

**Research promotion (2026-10-26):** [PR214](https://github.com/diegoami/ic2-conquest/pull/214), branch `main`, source `9a2009de95efedd4be64c38a499fc3539c96b150`. Independently reaudited offline and promoted as `[confirmed, partial: stock-original Wine]`; source-only/unplayed qualifications below remain. No new game or deployed Godot/Windows acceptance.

**Tag:** [confirmed, partial], six coherent stock-original Wine controls.
Research79/82. Existing promoted single-provider and Research77 manual-funding
findings read first; this adds the exact selected-carrier caller.

## Exact original rule and observations

`TUnitMap_SupplyArmy00446F50` resolves the selected fleet's army into the form's
army field. `TAFSupply_InitializeForm0043EDC0` then binds **target army0**, target
fleet−1. `FindProviders0043F468` searches around the **army record's coordinates**.
Consequently the carrier itself is eligible: only target-fleet ID is excluded,
and this is an army-target dialog. This is separate from Supply fleet.

Private copies of`fleet-split-antium-0734.SAV`,turn0734: army10000troops,purse37,
carrier2 supplies123,purse321; other fleet5 supplies77,purse217. Army supply0
or full101. Known city Antium is either own or coherently foreign/at war. Actual
Unit map > Army > Supply army menu invoked with the carrier selected.

| Control | Army dialog providers / selected source tested | After10tons and100talents |
|---|---|---|
| Carrier alone | carrier2 | army10/137;carrier113/221 |
| Carrier + owncity | city89,carrier2; last selectedcarrier2 | army10/137;carrier113/221 |
| Carrier + other ownfleet | carrier2,fleet5; selected5 | army10/137;fleet5 stock67,purse117;carrier123/321 |
| Full army + city + otherfleet | city89,carrier2,fleet5; selected5 | army101/137;fleet5 stock77,purse117 |
| Carrier moved in actual play101,46→100,46 | army follows100,46;city89 now outofrange;carrier2,fleet5 | army10/137;fleet5 stock67,purse117 |
| Immediate transfers then Alt+F4 Close | city/carrier/other; selected5 | same10/137 persisted after Close |

All links remain mutual; no unit/move change caused by supply/funding. Actual
fleet movement is measured before the supply input snapshot and attributed
separately. Globals change **at the supply/money arrows**, before OK; Close
keeps those changes. No visible Cancel button exists on this original form;
this is not the transactional Army transfer Cancel contract.

**Fleet > Supply fleet control:** after the army dialog, the same carrier opens
as target fleet2, target army−1; provider enumeration excludes itself. Coherent
carrier-alone input has no FleetSupply dialog, whereas carrier+otherfleet uses
fleet5. City-present cases also open. These control dialogs were inspected and
closed unchanged; no new fleet-target transfer measurement is claimed. Prior
promoted Research77 separately established that fleet-target money uses national
treasury, even with another fleet selected for supplies.

## Evidence / corrections

`runs/experiments/data/run-exp-restrictions85/audit-carried-v1.json` reparses12
saves for6coherent cases, validates citymarker/owner agreement, cargo coordinates,
mutual carrier link, actual supplier resource deltas and distinct FleetSupply
target. Cases are`gui79-v1_carried-city` /`carried-full-city-other`,
`gui79-marker-v4_carried-carrier-alone` /`carried-other-fleet`,
`gui79-moved-v2_carried-moved-carrier`,and`gui79-close-v3_carried-close`.
Each JSON cites original-written before/after SAV names,turn0734. Example:
`gui79-moved-v2_carried-moved-carrier_before.SAV` / `_after.SAV`.

Earlier no-city cases set cityowner1 but left Roman marker36: opening helper
trusted that marker, yielding an empty FleetSupply form. Those rows are retained
but **excluded as natural opening-gate evidence**. Coherent marker37 repeats
correct it. A deliberately stale cargo-coordinate fixture failed carrier
selection itself; preserved as a failed stimulus, not a supply rule. No memory
write or direct handler invocation bypassed that failure.

Private original copies, screenshots, fullstates, EXE identity and hashes stay
under ignored`artifacts/run-exp-restrictions85/private-gui79-*/`; no public
release. Reproduction:`runs/experiments/restrictions85/gui_supply.py` plus
`common.py`,`lists.c`; all measurements uniquely versioned.

## Implementation handoff and limits

Remake4d70275a`OpenSupplyArmyDialog` resolving`SelectedArmyOrCarried()` is supported
by this original caller. In consistent states the carrier and army coordinates
move together; searching around the cargo is correct. Carrier-as-provider must
remain distinguishable from FleetSupply's self-exclusion. Bind transactions to
the army and actual selected provider, rather than modifying the carrier as a
target. No new mismatch established for this target-resolution rule.

Retain owner-approved army providers, extra money picker and automatic funding
reserve; none is established as original by these tests. Deliberate presentation
and source choices remain separate from the verified cargo binding.

Stock unmodified original,private identity verification;Wine10.0 Ubuntu
10.0~repack-12ubuntu1,win32,own1280×1024Xvfb. Original UI and Save as endpoints,
read-only memory for timing. No native Windows, patch, owner game, Endturn,
battle/AI resupply investigation or remake modification. Malformed stale links,
multiple competing carriers and cross-session selection are unestablished.

## Independent Research verification and disposition

Research freshly re-ran the pinned save-audit code against retained private original endpoints: Six coherent cargo/marker/provider pairs, including actual carrier movement and Close. The corresponding complete published audit objects reproduce exactly. Private staged/working/live observations retain their source scope; Research did not replay the original UI. All nine findings share the [safe scalar receipt](../data/restrictions85-intake-v1.json).

Across the packet, 102 current save pairs, six historical pairs and three additional supporting pilot pairs were reparsed. The two corrected paid cases have coherent owner1/marker37 and bilateral peace at both endpoints; earlier 17 entry-marker caveats remain explicit. Invalid/failed selections, stale cargo coordinates, inconsistent GUI79 marker trials and load-reset false-zero labels are not promoted to successful natural controls.

Research independently matched 1,242 build-tree files to the authoritative remake `4d70275a` Git tree, including all 13 specifically audited source files. Fresh builds of the unchanged Audit, NativeExtra and NativeGui probes reproduce every scalar output line of authoritative v2/v4/v3 respectively. These execute production model/helper/dispatcher seams and synthetic testbed states, not installed Godot scenes or full native UI acceptance. Original handler/decompile and the recruitment/enemy-details disassembly were re-read; source-only outcomes stay labelled.

Research #79/#82; confirms cargo target/provider binding, excludes malformed stale-coordinate/marker attempts, and preserves extra army/money providers. No Main implementation, labels, release/tag, owner-policy or automatic reserve changed here. Main #1486–#1489 and #1326 and Research #78–#85 remain open at this verification; this promotion supplies evidence rather than automatic closure. Original EXE/DAT, raw saves, images, full states and per-input hashes stay private. The source draft remains upstream until conquest marks promotion.
