# Fleet continuation: stored destinations need native state support

**Tag:** [confirmed, partial: fourteen synthetic original-instruction/native
fleet controls; not fresh original gameplay or accepted native action parity].
**Tasks:** [#174](https://github.com/diegoami/ic2-conquest/issues/174), parent171;
new [remake1405](https://github.com/diegoami/imperial_conquest_2/issues/1405).
Research intake: reviewed `[confirmed, partial]`. Remake source/data pin55d96876.

**Provenance:** consolidated from conquest [PR #179](https://github.com/diegoami/ic2-conquest/pull/179),
merged main `8d975efddd66fd81371991936a7fd0cbc58016be`, finding blob `bf9ae8be1786e50e15256169be7bef344780b37d`.
Research reran the bounded controls offline as described below; no original/Wine
run or separate model review occurred.

## Answer

Original fleet stored destinations affect which destination routine is called.
The native model cannot distinguish the measured absent/A/B route states.
This is explicitly documented as unsupported native state with canonical export
reset, rather than a hidden violation of the current converter's policy.

The original phase chooses port `(45,68)` when no route is stored. With routes
A=`(48,66)` or B=`(47,67)`, it calls `0044E1FC` through the stored-route site
`0044F667` with A or B respectively. The resulting diagnostic SAVs differ from
the absent-route control **only in fleet0's four route bytes, +4/+6**.

All three import to identical serialized native GameState hashes and offer
identical native fleet-march proposals. `OriginalSaveExportFieldMapping` states
that `OriginalFleet.RouteX/RouteY` have no native field and writes absent-route
sentinels. A faithful stored-route feature needs explicit native state and
decision support, with save/load/export lifecycle tests; changing proposal
weights alone does not represent the missing destination.

## What was actually executed

The batch begins with the retained generated original decision snapshot from
`SF-N-rome-hook-v1-before/after.SAV`, turn0720→0721, then constructs fourteen
synthetic fleet-phase inputs. No owner1355/1388 input or fresh game run is used.
Original current nation is set to computer Carthage. Fleet0 is at `(49,62)`;
another fleet is placed on verified sea cells at distance3 or18. Relations,
fleet strengths, construction/moves and stored-route fields are varied as
declared in `case-manifest-v1.json` before execution.

Actual unmodified original `FUN0044F608` instructions execute their automatic
supply/repair prepass, port selector and hunt scorer. The collector stops at the
first `FUN0044E1FC` entry, **before movement**, or at normal phase return when
there is no move. No port, strength, movement or Random helper is replaced.

Original fleet strength really consumes `Random(4)`. Bounds, results, caller
returns and before/after seeds are retained. Stored-route cases consume zero
hunt draws; ordinary peace consumes one actor-strength draw, and eligible war
targets consume two. Separate actual scorer replays verify returned scores
253/90/1797 and the strict **100 versus101** port/hunt boundary. The original
uses the real seeded instruction stream, not an injected favorable outcome.

Native production `AiMilitaryPhase.ProposeFleetMarches` is invoked on imported
original pre-move state, after verifying fleet and relation inputs (**3568
checks**). Its real outer launched/moves guards are respected. This measures
**proposals**, not the winner of the entire native greedy AI loop.

| Control | Original first destination | Native offered fleet march |
|---|---|---|
| Peace / trade / alliance | Port `(45,68)` | Foreign fleet `(48,65)` |
| War, baseline / weaker enemy | Enemy `(48,65)` | Enemy `(48,65)` |
| War, stronger enemy | Port `(45,68)` | Enemy `(48,65)` |
| Stored A / B | Stored A / B | Same proposal as absent route |
| Original hunt score100 /101, distance18 | Port / enemy | No march proposal in either |
| Zero actor moves / actor under construction | No move | No proposal |
| Target under construction / same owner | Port | No proposal |

The native sailing weights and minimum score are explicitly marked **designed**
in the ruleset. The distance18 proposal cutoff and relationship/strength
differences are therefore measured policy differences requiring faithful versus
designed-mode reconciliation, **not automatically unintended defects**. No
accepted-action, naval combat or full fleet strategy equivalence is claimed.

## Evidence and follow-up

Tracked text: `runs/experiments/data/run-exp-strategic-fleet/`:
`summary-v1.json`, `original-fleet-controls-v1.json`,
`native-fleet-controls-v1.json`, `original-score-controls-v1.json`,
`stored-route-byte-control-v1.json`, manifest, build and execution receipts.
Runners: `runs/experiments/strategic-fleet/`.

Synthetic diagnostic containers are named
`controls-v1/<case>/pre-move.SAV`, with input and pre-move RAM beside them.
They are not original Save As files or turn-progress claims. Generated binary
evidence/tools/data are off Git; archive hashes and upload receipts are tracked.
Original EXE/DAT, runtime trees, credentials and owner material are excluded.

Remake1405 scopes stored-route state support and actual accepted-behavior tests.
Existing1394 owns army target eligibility/routing;1402 owns the independently
controlled resupply selector. Scorer1216's approved tie policies remain separate.
Conquest #174 next needs actual fleet-phase observations and accepted native
command traces, protected ports, provider thresholds, cargo and routing/contact.
Research175–178 track homeland, economy, diplomacy and later campaign expansion.
No production correction, new native schema, live fleet run or Windows acceptance
is implied by this conditional batch.


## Later movement evidence

The later [accepted-movement intake](2026-10-24-fleet-accepted-movement174.md) extends this first-destination study through original movement and accepted native commands. Its synthetic stored-route/zero-move case closes this report's *untested combination* only at that declared control; native route persistence remains unsupported. It also isolates a separate AI fleet insufficient-step move-budget discrepancy (#1408). Do not reinterpret this report's proposal rows as accepted actions or whole-turn equivalence.

## Research intake verification

Research read the full finding, declarations, original phase/scorer runners,
production-proposal probe, audit and bundle-recovery code. All fourteen original
F608 controls and the six separate hunt-score controls were regenerated through
unchanged original instructions, with real RNG and automatic prepass execution.
The entire declaration, original choices/draws and score records reproduce
byte-for-byte. Collection stops at the first destination routine's entry; it does
not replace that routine with invented movement or claim its downstream result.

All76local archive members match pinned digests and the exact tar inventory.
Fresh recovery executes the retained native tool; a second invocation on the
freshly regenerated controls reproduces **all14native rows byte-for-byte**.
All3,568fleet/relation input checks pass. The recovered engine matches the prior
pilot's pinned assembly, and all349archived Engine/Data/data Git blobs were
rechecked. Research did not independently rebuild the binaries or download Drive
copies. The whole scalar summary reproduces exactly.

The absent/A/B byte proof was independently recalculated: equal lengths, only
fleet0's words+4/+6 differ (four bytes). All three imported native state hashes and
proposal lists agree. This is stronger than inferring missing state from a final
move, but it does not exercise native save/load/export lifecycle after adding a
new route field. The field mapping and exporter explicitly classify RouteX/RouteY
as no-native-field/canonical, resetting x to−1 and y to0; synthetic absent input
uses−1/−1. No original-route byte-identity promise is being asserted.

Source checks used the pinned original decompile (`2018c205…87d8`):
`FUN_0044F4F8`, lines52991–53024, and `FUN_0044F608`, lines53040–53069.
They distinguish stored route, port and hunt branches, with hunt scores below101
choosing port and101eligible for hunting. The actual original fleet-strength
Random calls are retained in the control records, including return sites and seed
transitions. This is not a matched native/original global draw-stream test.

The pinned native source (`55d96876`) independently corroborates classification:
`OriginalSaveExportFieldMapping` declares the two route words canonical with no
native field; `OriginalSaveExporter` documents x−1/y0; `AiMilitaryPhase` computes
sailing proposals from the designed base/distance/minimum-score fields. Those
weights are explicitly labelled designed in `Ruleset`. A generated proposal to a
foreign fleet is not proof of an accepted attack, nor does this batch select a
new faithful/designed policy. Stored-destination state support is the bounded
feature gap; changing a weight cannot represent the missing information.

**Additional limit:** zero-move/construction agreement refers to the declared
controls. Stored-route+zero-move is not tested. In the original body the stored-route
branch bypasses the absent-route moves test; movement outcomes of that combination,
route completion/cancellation and persistent save lifecycle still need controls.
No universal outer-guard equivalence follows from the two no-proposal cases.
The earlier phase intro in strategic-ai-turn and the specification is clarified
to include stored routes and to test the signed X word, rather than the packed pair.

[Read-only reproduction runner](../../scripts/fleet174-intake-check.py) and
[scalar receipt](../data/fleet174-intake-v1.json):

```bash
python3 scripts/fleet174-intake-check.py \
  --conquest "$IC2_CONQUEST" --artifact-root "$IC2_CONQUEST_ARTIFACTS" \
  --work "$IC2_NEW_PRIVATE_WORK" --out /tmp/fleet174-new.json
```

The work directory must be new and remain outside Git/public artifacts. These are
synthetic diagnostic containers and conditional proposals, not original Save As,
accepted whole-turn commands, naval combat equivalence, a production correction
or Windows acceptance. The [army targeting/routing](2026-10-24-seleucid-strategic-target-routing1388.md)
and [resupply pilot](2026-10-24-strategic-fidelity-pilot171.md) remain separate evidence.

The first isolated intake run omitted a canonical expected native-row file needed
by the recovery verifier. That staging failure is retained separately; the corrected
run uses a fresh output path and reproduces the full expected record unchanged.
