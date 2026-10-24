# Strategic continuation: matched economy controls and AI embark overflow

**Tag:** [confirmed, partial: original phase captures/instruction replays,
conditional native comparisons and declared synthetic controls].
**Issues:** conquest #176 (economy), #177 (diplomacy), #174 (fleets);
[Main #1412](https://github.com/diegoami/imperial_conquest_2/issues/1412) tracks
new embark-overflow evidence. **Status:** promoted from ic2-conquest [PR190](https://github.com/diegoami/ic2-conquest/pull/190), branch `main`, commit `7129418663447e0b242c0ad56afcb78f8af1ae0c`, after independent offline verification. No production change.

## Result and attribution

The measured faithful economy rules agree on 35 matched inputs when supplied
with the original draws. Diplomatic busy/war-target selection agrees on 24
inputs; alliance/trade execution remains outside that comparison. All 23 fleet
provider controls agree. Five valid over-capacity AI embark controls differ:
**the original lands whole overflow units; the remake scales troops away.**

The remake's proportional trim is explicitly tagged derived in its source,
based on the earlier absence of FUN_0044F8FC. This evidence resolves that gap
for the tested free-land/free-army-slot branch. It does not silently override
the owner's designed-mode or human refusal decisions.

## Sources, saves and observer gate

Native pin: `195a588e8eef03ad504b596e64f001ddb943121d` (T214 fleet budget fix).
Relevant AI/economy/recruitment/diplomacy source is unchanged from T213's
`933a5d4a`; only MoveFleetCommandHandler differs in those areas. Original EXE
SHA256 starts `9d753d5d`; listing starts `2018c205`. Full pins and semantic
function ledger are under
[the pinned source/data ledger](https://github.com/diegoami/ic2-conquest/blob/7129418663447e0b242c0ad56afcb78f8af1ae0c/runs/experiments/data/run-exp-strategic-tracks/).

One generated `ROM720.SAV` trajectory, startup seed 1, End turn 0720→0721:
`ST176-ST-rom-hook-v1-before.SAV`, `ST176-ST-rom-hook-v1-after.SAV`, and the
corresponding `plain` pair. Complete before and after SAV bytes agree between
observer and plain. This is one trajectory and its inertness control, not two
independent campaigns. The observer passes 360 CPU/flags/stack/capacity checks.

Ninety snapshots capture 45 phases: 15 diplomacy, 15 economy, 15 fleet. Actual
unmodified original instructions reproduce **all 45 complete captured exit RAM
blocks**, including RNG. Those replays record 54 actual draws: 12 diplomatic,
42 recruitment, none fleet. No Random/game/presentation helper is replaced.
Draw logs are conditional replay observations gated by exit identity; there is
no live per-draw hook or claim of native global-stream equivalence.

## Economy #176

The native faithful phase runs on each captured economy entry. Its injected
recorded-draw provider rejects any missing draw or bound mismatch. Named native
streams deliberately share this recorded sequence only in the diagnostic tool;
production RNG behavior is unchanged. All 15 phases consume precisely the
original draws and match the measured projection: own nation resources/tax/
mobilization, recruitment queue, army units/resources and fleets. All 23
commands are accepted. IDs are normalized only for the documented projection;
whole serialized native/original state or event parity is not claimed.

Twenty declared synthetic phase controls also agree: treasury around the debt
floor, mobilization 99/100, queue slots 39/40, week 9/11, unity 499/500/649/650,
and treasury −1/0/999/1000. Own/threat estimates agree on all 35 inputs. The
synthetic cases reuse a captured Galatian entry with exact declared field edits;
they are not new games or a multi-scenario campaign sample.

Evidence: `native-phases-v2.json`, `native-synthetic-v1.json`,
`phase-facts-v1.json`, `synthetic-manifest-v1.json`. Saves: each captured
`*-economy-*/before.SAV` / `expected.SAV`, and synthetic `1000-economy-12`
through `1019-economy-12`. The diagnostic SAVs are projections of captured or
declared RAM, not original Save As outputs.

## Diplomacy #177

The original's local busy/protection/trade helper and first war-candidate scan
are executed on the retained inputs. Native busy and best-war-target match for
15 captured entries and nine synthetic controls (mobilization 40/41, autumn/
winter and power-division boundaries at wealth 19,999/20,000/39,999/40,000,
plus a strong positive control). Input identity gates cover relevant units,
cities, fleets, nations, queues and relations before comparing.

Native alliance/trade/swap candidates are recorded for inspection, but are not
labelled equivalent to the original's whole atomic scan. No human offer was
accepted by the harness: the generated Roman turn displayed a Carthaginian
trade notice. Its presence is not a treaty write or consent. Matching busy/war
selection does not prove alliance candidate order, trade swaps, draw scheduling,
or a native whole-turn diplomatic outcome.

Evidence: `phase-facts-v1.json`, `native-phases-v2.json`, the nine synthetic
`1020-diplomacy-4` through `1028-diplomacy-4` projected save pairs, and the
actual `ST176-...` saves above. Across all 94 native comparisons, the retained
input gate field count is in `summary-v1.json`.

## Fleet providers and landing #174

Twenty-three provider controls compare original E5DC with native AiResupplyPass
on a generated state containing one own launched fleet and no armies. These
agree on measured fleet resources/condition, city stocks and nation treasuries:
own/foreign stock 0/1/100; foreign purse 0/1/4/5; distance 3/4; peace/trade/
alliance/war; own treasury 100/101; condition 94/95; capacity 79/80/81 for ten
ships. These are automatic phase effects, not dispatched player commands.

Four explicit disembarkation requests agree and are accepted: two real free
adjacent land cells, each with move budgets 0 and 8. Both budgets become zero,
carrier links clear and the land marker is restored. Native automatic landing
choice is recorded separately; it is not substituted for the original's named
land destination. Human UI legality and arbitrary occupied land are not tested.

Evidence: `fleet-native-providers-v1.json`, `fleet-original-v1.json` (provider
rows only), `fleet-original-v2.json`, `fleet-native-v2.json`. Generated save
pairs live under `fleet-controls-v1/<provider>/` and
`fleet-controls-v2/land-*/` in the archive.

## Over-capacity embarkation: new Main #1412

A ten-ship AI fleet at (40,33), adjacent army at (39,34), capacity 5,000:

| Original army slots | Original result | Native accepted result |
|---|---|---|
| 4,999 LI | All aboard unchanged | Matches |
| 5,000 LI | All aboard unchanged | Matches |
| 5,001 LI or 10,000 LI | Whole unit ashore; emptied transport army removed | Scales to 5,000 aboard |
| 4,000 LI + 2,000 HI | 4,000 aboard; 2,000 ashore | Scales total to 5,000 |
| 2,000 LI + 3,000 HI + 1,000 archers | 5,000 aboard; 1,000 ashore | Scales total to 5,000 |
| 5,000 LI + 1 HI | 5,000 aboard; 1 ashore | Drops overflow troop |
| 3,000 LI + 2,000 HI | Both aboard unchanged | Matches |

FUN_0044B79C calls F8FC only for an AI army over capacity. F8FC finds a land
receiver and scans unit slots in order. The first slot whose cumulative total
**exceeds** capacity and all subsequent slots are moved whole to the receiver;
units are not proportionally reduced. In the mixed controls, all original troops
survive, and money/supply split 67/33 and 60/30 from 100/90. Native
ArmyTransportTrim instead rescales slot troops, creates no overflow army and
loses surplus troops. The two single-unit and three mixed-unit overflow cases
are the five mismatches. The seven valid cargo controls at/below capacity or
explicitly landing agree.

Original removal/compaction changes army indices when the carrier army empties.
Compare carrier links and surviving records, not a presumed permanent army-0
identity. No-land, no-free-army-slot, existing receiver, every slot/type/count,
large capacity and human click/refusal branches remain untested. The source has
a no-receiver deletion branch; this batch does not establish its safe contract.
Main should consume Research's promoted rule and scope those limits explicitly.

Evidence: `fleet-original-v2/v3.json`, `fleet-native-v2/v3.json`;
`fleet-controls-v3/embark-units-4000-2000/before.SAV` / `expected.SAV` and the
other uniquely named case pairs. Zero original RNG calls in these controls.

## Stored-route limit and retained failures

One synthetic F608 call reaches its stored adjacent sea destination and retains
both stored coordinates. A second fresh-stack call with only a synthetic move
refresh leaves that destination and still retains it. The latter encounters the
known coincident CB40 stack dependency; **it is diagnostic, not a universal
next-turn routing rule**. No native stored-route support is invented: Main
#1405 still owns that state gap. See `fleet-route-lifetime-v1.json` and
`route-phase-0/1` projected saves.

The first cargo fixture used invalid quality code 50. Original instructions ran,
but native import correctly rejected it. All eight invalid cargo-v1 cases and
the failed log remain; they are excluded from comparisons. The 23 completed
provider results persisted before that failure and were recovered without a
rerun. Cargo v2/v3 use retained valid quality 7. No measured output was deleted
or overwritten; old native comparison v1 also remains beside strengthened v2.

## Scope and next work

This batch gives 35 economy matches, 24 local diplomatic gate/target matches,
23 provider matches and 12 valid cargo comparisons (seven match, five overflow
mismatches). It does not establish every strategic feature, multi-start campaign
parity, global RNG alignment or Windows acceptance. No production source or
save schema changed and no other repository was written.

Next #176: ready-queue mobilization/compaction, mercenary and consolidation edge
controls. Next #177: protected/alliance candidate and multi-partner trade/swap
controls, then actual accepted decisions with explicit stream/phase policy.
Next #174: overflow receiver/allocation failure branches and after-arrival
caller context; the prior paused battle queue remains paused.

Archive and recovery instructions are in the data README. The explicit generated
archive excludes all original EXE/DAT, runtime/prefix trees and owner material.
Research has now promoted this bounded evidence. Main owns the production correction and its reviewed scope and acceptance.

## Research verification

Research recovered the local archive into a new private temporary tree, checked its pinned size and SHA256, verified the exact 1,131-member inventory and every one of the 1,130 payload hashes/lengths, and reran its retained compiled tools. The recovered 30 native phase rows and four mixed-unit rows reproduce their authoritative JSON **byte for byte**. No downloaded remote digest, independent native rebuild or post-pin production validation is claimed.

From the original live entry snapshots, fresh unchanged-instruction execution reproduces all 45 captured exit RAM blocks and the complete phase/draw ledger: 54 draws. Fresh local diplomacy/power facts and all 29 synthetic controls reproduce their complete ledgers. Fresh native comparisons from the newly projected phase/synthetic containers reproduce all 59 economy/diplomacy result rows exactly. All 360 observer CPU/flags/stack/capacity tests pass; fake callee effects occur only in that CPU test. The retained complete observer/plain before/after saves were independently compared byte for byte; the Wine trajectory itself was not replayed as a new game.

For fleets, Research executed each retained valid before-RAM input through the unchanged original routine and compared the complete resulting game-RAM block with its expected RAM: 23 providers plus 12 valid cargo cases. Fresh projected containers then pass the retained native tool's input gates and reproduce the measured results, including the five discrepancies. Across all 94 native comparisons, the retained gate total is 227,833 fields; this is a count of the documented unit/city/fleet/nation/queue/relation checks, not proof of every original memory field or a whole-state equivalence claim.

There is one probe-version qualification. The recovered newer `FleetChecks.dll` adds `troops_before`, `troops_after_native` and `troops_after_original` to the older provider and cargo-v2 row shape. Provider rows are also returned in a different order from the recovered per-case ledger. Matched by unique case name, **every existing field** agrees for all 23 providers and eight cargo-v2 rows. The extra provider counts are all zero; fresh cargo counts independently retain the original totals and reproduce the two single-slot losses. Mixed-unit v3 rows already have those fields and reproduce exactly. No game-result field was normalized, and the older measurements were not overwritten.

Source rereading corroborates the interpretation: B79C invokes F8FC only for an over-capacity AI army; F8FC scans cumulative slot troops with a strict capacity comparison and transfers whole slots in the covered allocation branch. The retained remake `EmbarkArmyCommandHandler` invokes the explicitly derived `ArmyTransportTrim`, which proportionally scales the units. Research also rechecked the economy, diplomacy local scan and provider helpers against the pinned listing. The [older unit-map report](decompiled-unit-map-orders-and-record-fields.md) is corrected: F8FC was unavailable to that original packet, but is now available; exact-capacity proportional troop loss is not the observed whole-slot rule.

The [safe research receipt](../data/strategic190-intake-v1.json) records counts, source pin, caveats and cargo totals. Original assets, generated raw RAM/SAV/full traces, and private manifests remain outside research Git; no owner input was used. Allocation failures, existing receivers, human click/refusal, every slot/type/count and complete diplomacy/whole-turn/native RNG/Windows acceptance remain outside this promotion. Main [#1412](https://github.com/diegoami/imperial_conquest_2/issues/1412) is open with `triage:needed`, priority P1, at the live 2026-10-24 check. The draft remains upstream until the conquest session records its promotion.

Reproduction uses the [pinned runners](https://github.com/diegoami/ic2-conquest/blob/7129418663447e0b242c0ad56afcb78f8af1ae0c/runs/experiments/strategic-tracks/) and data README. Use fresh output directories: `verify_bundle.py --version UNIQUE`; then original phase/facts/synthetic replay, retained native probes on the regenerated containers, and direct unchanged-instruction replay of retained valid fleet before-RAM. Fixed-v1-output runners need a new private source tree; never route generated outputs through symlinks into the sibling checkout. The initial comparison attempt's row-shape/order difference is documented above. Upstream invalid quality-50 cargo and early EOF recovery attempts remain excluded and preserved.
