# A complete tactical battle, captured end to end, plus two new UI screens

`2_rome.txt`'s third entry: `1_rome_270_winter_7.sav → 1_rome_270_winter_9.sav`, across four recordings (`00-31-14-131.mp4`, 58s; `00-32-26-388.mp4`, 3:14; `00-35-54-640.mp4`, 27:23; `01-03-29-805.mp4`, 29s). The user reports the game reliably freezes during the early stages of a battle even with the "AIM toolkit" compatibility workaround running, so the middle of an actual fight is still not directly observable move-by-move. Despite that, this set of recordings caught something better than any prior sample: the tactical battle screen itself, a per-unit combat info panel never seen before, and — thanks to the freeze forcing a long, sparse recording — the complete final battle-resolution dialog with exact numbers.

## The save-level result

`1_rome_270_winter_7.sav → 1_rome_270_winter_9.sav` is a 682-byte size decrease: exactly `656 + 26`, i.e. one whole army record plus one whole fleet record removed. That arithmetic alone predicts two entities were destroyed outright before any JSON inspection — and it's exactly what happened:

- **Gaul's army 13** (83,348 troops, at (88,25)) — destroyed entirely, removed from the army table.
- **A Carthaginian fleet** (fleet slot formerly at Andematunum, 49 ships) — lost; the news log calls it "lost at sea," distinct wording from the "damaged in a storm" events seen earlier for other Carthage fleets, though both are presumably variants of the same weather-event system (`decompiled-weather-events.md`).

Rome's army 0 fought and won, but at real cost: 19 → 14 units, 99,882 → 63,282 troops (−36,600), moving from (90,28) to (88,26) — onto the battlefield itself.

Naupactus (Greece) also falls to Illyria this turn, showing the familiar forced-capture byte signature (offsets 18/22/26/28 all changed) — unrelated to Rome's fight, just concurrent AI activity.

## The tactical battle screen, confirmed directly

`frames5b/f_001.png` through `f_019.png` (extracted from the second recording) show the actual "Rome v Gaul" tactical map: a small 14×~20 visible grid with Rome's 19 units placed in the top rows (blue = regulars, purple = a distinguished sub-group — possibly the currently-selected/movable set) and Gaul's units placed in the bottom rows (red). The header cycles between **"Rome to place units."**, **"Gaul to move units."**, and **"Rome to move units."** — direct, literal confirmation of the turn-alternation structure already inferred from `FUN_00439c84`/`FUN_00439ce8` in `decompiled-combat-formula-structure.md`. One frame (`f_018.png`) shows a Gaul unit highlighted with a black-diamond target cursor while it's Rome's move — the attack-target-selection step.

This closes an item that was previously only understood from decompiled code: the placement phase, the per-side turn order, and the visual grid layout are now all directly observed.

## A new UI screen: the per-unit combat info panel

`frames5c/start.png` and `frames5c/mid.png` (from the long third recording) show a panel never encountered before in this project, displayed while selecting a unit mid-battle:

```text
Rome's army
6th Guards Battalion
Heavy infantry
Troops      4,527
Quality     good
Morale      normal
Moves       1
Shots       0

Unit set to attack
2nd Guards Battalion       (Gaul's unit)
Heavy infantry
Troops  4,165
```

and, for an archer unit later in the same battle:

```text
Rome's army
4th Bowmen Battalion
Archers
Troops      3,312
Quality     average
Morale      very low
Moves       4
Shots       19
```

This is the first direct evidence of **`Morale` as a named, tiered stat** (`"normal"`, `"very low"` observed; by analogy with the 5-tier `Quality` scale — poor/average/good/very good/elite — a `very low`/`low`/`normal`/`high`/`very high` scale is a plausible guess, not confirmed). This is a strong candidate for the unidentified `+0x350` field in `decompiled-combat-formula-structure.md`'s melee routine (`attacker.<field @ +0x350> += ... +2 : -3`) — a per-exchange adjustment to exactly this kind of morale stat would explain why it drifts during a fight. Not proven this pass (no raw byte was cross-referenced against a save), but the categorical values now give a concrete target to look for.

`Shots` is new too: it's 0 for the melee heavy-infantry unit and 19 for the archer unit, strongly suggesting a per-battle ranged-attack counter, separate from `Moves` (both had already-consumed values consistent with mid-battle state, e.g. the heavy infantry's `Moves: 1` remaining vs. its stated 4-per-turn baseline elsewhere in this project's data).

Notably, the archer unit's `Quality` here still reads `average` mid-battle, even though it's the same "4th Bowmen Battalion" whose post-battle SAV record shows quality bumped to `good` (see below) — the promotion, whatever triggers it, happens after the fight concludes, not incrementally during it.

## The battle resolution screen: full numbers, exact match to the save diff

`frames5c/end.png` (the last usable frame, extracted from 5 seconds before the third recording ends) is the complete "Rome's army defeats Gaul's army" summary dialog:

| Type | Rome start | Rome finish | Gaul start | Gaul finish |
| --- | ---: | ---: | ---: | ---: |
| Light infantry | 45,087 | 26,032 | 57,973 | 0 |
| Heavy infantry | 28,057 | 20,675 | 7,635 | 0 |
| Archers | 16,856 | 11,883 | 3,867 | 0 |
| Light cavalry | 6,695 | 4,692 | 10,899 | 0 |
| Heavy cavalry | 3,187 | 0 | 2,974 | 0 |
| **Total** | **99,882** | **63,282** | **83,348** | **0** |
| Money captured | — none — | | | |
| Supplies captured | — none — (dialog text literally reads "suuplies", a typo in the original game) | | | |

Rome's finish total (63,282) matches the save-diff-derived value **exactly**. Gaul's army is annihilated (0 across every type) — consistent with it being fully removed from the SAV army table. This is the most complete single-battle dataset the project has: full per-type before/after for both sides in one authoritative screen, not reconstructed from partial samples.

**Heavy cavalry is the standout result**: Rome's two heavy-cavalry units (1st Dragoons, 755 troops; 3rd Dragoons, 2,432 troops) were both wiped to exactly 0, a 100% loss, while every other type retained 57–74%. Both were small in absolute troops, though 3rd Dragoons was a near-full heavy-cavalry battalion (2,432 of 2,500). Under the confirmed 40%-of-own-troops melee cap (`floor(0.4×troops)+1`), repeated losing exchanges compound multiplicatively (`0.6ⁿ`) — a small unit can be driven from a few thousand to zero over several rounds of a multi-round battle far more easily than a large one, without needing any special "heavy cavalry is weak here" rule. Consistent with, but not proof of, a type-effectiveness disadvantage against Gaul's composition — the matrix's exact values are still unextracted for these specific type pairs.

> **Correction to the explanation** (the observation stands; this note revised 2026-09-23). The `0.6ⁿ` reading is wrong: a 40%-of-own-troops cap can never reach 0, only approach 1. Units leave a tactical battle through a separate **rout check** (`FUN_00438fb0`). It removes a unit whose troops fall below its type's standard battalion size ÷ 25, or that fails a morale test (automatic at tactical morale ≤ 19, a `Random(m) + Random(m) ≤ 29` roll at 20–39), and every rout costs each other friendly unit 6 morale. See [battle-replayed-rout-mechanic-and-combat-constants.md](battle-replayed-rout-mechanic-and-combat-constants.md). The first version of this note added that heavy cavalry's threshold is "the lowest in the game (100), so small heavy-cavalry units collapse first". **That was backwards.** The floor is 4% of a full battalion for every type (600, 240, 140, 280, 100 against 15,000, 6,000, 3,500, 7,000, 2,500), and at equal troops a lower floor takes *more* losses to cross. What the evidence supports is narrower. **1st Dragoons** (755 troops, 30% of a battalion) started 7.6× its floor, the second-closest unit in Rome's army after 1st Foot (6.8×). About four maximal capped melee losses would take it under `[derived]`, and it was destroyed in both this battle and the replay from the same save `[confirmed]`, so being a small unit near its floor is a **candidate**. **3rd Dragoons** (2,432, a near-full battalion) started 24× its floor, as far from it as any full battalion of any type. It needed about seven maximal melee losses, or a large shot, to cross it. In the replay it lost 95 troops and survived. Which mechanism removed it here (troop attrition past the floor, the 20–39 morale test, or the −6 cascade after friendly routs) is **[open]**: this battle's recordings did not capture the exchanges. Heavy cavalry's 100% here is two units, not a type property. The replay's Rome heavy cavalry lost 26.7% (3,187 → 2,337), and the Seleucid winner in `ptolemy-run-ui-inventory-and-leader-draw.md` §3 lost 4%.

## Unit-level detail, matched by name across the save pair

19 units before, 14 after (5 wiped entirely: Gallic, 8th Guards, 5th Bowmen, 3rd Dragoons, 1st Dragoons). Of the 14 survivors, most kept their quality tier; **three gained one tier** (average → good): 3rd Foot Battalion (lost 57% of its troops), 1st Bowmen Battalion (lost 49%), and — notably — **4th Bowmen Battalion, which lost zero troops** (3,312 → 3,312 exactly) yet was still promoted. Losses don't predict promotion. This looks like a previously undocumented **post-battle veterancy/promotion mechanic**, independent of the melee/shooting formulas already decompiled, and independent of the `Morale` value observed mid-fight (4th Bowmen's morale was seen as `"very low"` during the battle, yet it was still promoted afterward — ruling out a simple "high morale → promotion" reading). Not decompiled this pass; a good target for a future Ghidra search once "quality"/"promote" or similar Delphi-recovered symbol names turn up.

## On the freeze

The recordings confirm the freeze is not a hard, permanent hang: `frames5c/mid.png`, sampled roughly 13 minutes into the 27-minute third recording, shows the battle mid-progress with different units and updated state — real computation is happening, just slowly and with the UI seemingly unresponsive or barely responsive for long stretches (consistent with the user's report that AIM toolkit didn't resolve it). This means future battle recordings from this setup will likely keep missing the individual `SHOOTS AT`/`ATTACKS` exchange messages in real time, but the placement screen, per-unit info panel, and final resolution dialog remain reliably capturable — which is enough to keep confirming aggregate combat outcomes precisely, as this report shows.

## What this does not establish

- The exact promotion trigger/formula for the quality-tier bump.
- Whether `Morale`'s tiers map onto the decompiled `+0x350` field's numeric range, or the tier boundaries.
- The type-effectiveness matrix values for heavy-cavalry-vs-Gaul's-composition specifically.
- Individual exchange-by-exchange combat log — still unobservable due to the freeze.

## Reproduction

```text
ffmpeg -i "recordings/bandicam 2026-09-13 00-31-14-131.mp4" -vf fps=1/5  frames5a/f_%03d.png
ffmpeg -i "recordings/bandicam 2026-09-13 00-32-26-388.mp4" -vf fps=1/10 frames5b/f_%03d.png
ffmpeg -ss 0    -i "recordings/bandicam 2026-09-13 00-35-54-640.mp4" -frames:v 1 frames5c/start.png
ffmpeg -ss 800  -i "recordings/bandicam 2026-09-13 00-35-54-640.mp4" -frames:v 1 frames5c/mid.png
ffmpeg -sseof -5 -i "recordings/bandicam 2026-09-13 00-35-54-640.mp4" -frames:v 1 frames5c/end.png
ffmpeg -i "recordings/bandicam 2026-09-13 01-03-29-805.mp4" -vf fps=1/3 frames5d/f_%03d.png
dotnet run --project src/IC2.Inspect -- --compare-saves saves/1_rome_270_winter_7.sav saves/1_rome_270_winter_9.sav
dotnet run --project src/IC2.Inspect -- --to-json saves/1_rome_270_winter_7.sav w7.json
dotnet run --project src/IC2.Inspect -- --to-json saves/1_rome_270_winter_9.sav w9.json
```

## Next checks

1. Search the recovered Delphi symbol table for anything resembling "promote"/"veteran"/"experience" near the battle-resolution code, now that a concrete promotion effect is confirmed to exist.
2. If a future recording catches the per-unit info panel on the same unit at two different points in one battle, the `Morale` tier transitions could be correlated against the decompiled `+0x350` adjustment logic.
3. A battle recording using the "Fast Battle" / auto-resolve option (if one exists in the UI) might sidestep the freeze entirely, if the freeze is specific to the manual step-by-step tactical mode. **Answered:** the pause is a stored per-nation setting edited by a `TBattleDelays` dialog and can simply be set to 0; this exact battle was then replayed from the same starting save with the pause neutralised, yielding a legible per-exchange log and a materially different outcome. See [battle-replayed-rout-mechanic-and-combat-constants.md](battle-replayed-rout-mechanic-and-combat-constants.md) and the update to [battle-freeze-diagnosed-procmon.md](battle-freeze-diagnosed-procmon.md).
