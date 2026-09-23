# The same battle fought twice: the rout mechanic, the attacker-side cap, and two resolved constants

`notes/2_rome_s.txt`'s first entry — `1_rome_270_winter_7.sav → 1_rome_270_winter_7_b.sav`, recording `bandicam 2026-09-13 22-49-01-893.mp4` (9:38), the user's note reading *"Rome defeats army of Gaul (auto battle, complete, no freeze)"*.

This is the **same starting save** as `full-battle-resolution-rome-vs-gaul.md`'s battle (`1_rome_270_winter_7.sav`), replayed. That makes it the first controlled A/B this project has had on the tactical resolver: identical pre-battle state, identical armies, fought twice. It also — because the per-action pause was neutralised this session, see the update appended to `battle-freeze-diagnosed-procmon.md` — is the first recording in which the individual `ATTACKS`/`SHOOTS AT` exchange panels are legible end to end. 23 shooting and 15 melee exchanges were read off it.

Two of the three things that came out of it were not looked for: an entirely undocumented **rout mechanic** that turns out to be the reason units ever reach zero troops, and the refutation of `battle-quality-promotion-and-morale-array-decompiled.md`'s promotion rule.

## The same battle, twice, with different results

| | Battle 1 (`→ winter_9.sav`, manual) | Battle 2 (`→ winter_7_b.sav`, this pass) |
| --- | ---: | ---: |
| Rome start | 99,882 (19 units) | 99,882 (19 units) |
| Rome finish | 63,282 (14 units) | **75,536 (16 units)** |
| Rome losses | −36,600 (36.6%) | **−24,346 (24.4%)** |
| Units destroyed | 5 (slots 3, 5, 10, 11, 14) | **3 (slots 0, 3, 6)** |
| Units promoted | 3 | 3 |
| Gaul | 83,348 → 0, army record deleted | 83,348 → 0, army record deleted |
| Rome unity | 856 → 881 | 856 → 881 |
| Gaul unity | 427 → 402 | 427 → 402 |

The `Battle ended` dialog in this recording reads `99,882 → 75,536` against `83,348 → 0`, matching the save diff to the troop — the same cross-check `full-battle-resolution-rome-vs-gaul.md` made for battle 1, repeated. The header text is the tactical-path string *"Rome's army defeats Gaul's army."*, not the instant resolver's *"X destroys army of Y"*, so both battles went through `TBattleMap`/`FUN_004393ec`, not `FUN_0044AEE4`.

**The tactical resolver is strongly stochastic.** The same two armies, from the same bytes, differ by 12,254 troops (a third of the total loss) and by which two extra units die. Anything this project does with the tactical formula — a reimplementation's parity test especially — has to be a distribution test, not an equality test. `[confirmed]`

### Post-battle bookkeeping, and what the two paths share

Reading battle 2's save diff against `decompiled-diplomacy-peace-terms-and-instant-battles.md`'s decompiled instant resolver (`FUN_0044AEE4`):

| Effect | Instant resolver (code) | Tactical path (observed, battle 2) |
| --- | --- | --- |
| `unity[loser] −= 25`, `unity[winner] += 25` (cap 990) | yes | **yes — 856→881 / 427→402, exactly ±25** |
| loser's army record deleted outright | yes | yes — but *tombstoned first*, see below |
| `attacker.moves = 0` | yes | yes (Rome's army 0: moves 5 → 0) |
| `winner.money += loser.money` | yes | consistent, Gaul's army held 0 |
| winner's supply capacity | — | `supplyCapacityTons = totalTroops / 100` holds exactly: 99,882→998, 75,536→755 |

The ±25 unity swing was previously only known from the instant resolver's decompiled code. It fires on the tactical path too, in both battles. `[confirmed]`

### The `0xFFFF` army tombstone, caught being created

`1_rome_270_winter_7_b.sav` is **the same size as its predecessor** (132,149 bytes) despite Gaul losing an entire army, while `1_rome_270_winter_9.sav` is 682 bytes smaller (`656 + 26` — one army record plus one fleet). The reason is directly visible in the bytes: the destroyed army's record is still physically in the table, with its owner word replaced by the no-owner sentinel.

```text
offset 0x1ABAE   winter_7.sav    58 00 19 00 | 06 00 | ...      x=88 y=25 owner=6 (Gaul)
offset 0x1ABAE   winter_7_b.sav  58 00 19 00 | FF FF | ...      x=88 y=25 owner=0xFFFF
```

So the `0xFFFF` army tombstone — which `imperial_conquest_2`'s build task T30 had to make `IC2.Data` tolerate, from three saves that merely *contained* one — is created by combat resolution **during** a turn and compacted out by the **end-of-turn** tick. `winter_7_b` is a mid-turn save (taken right after the battle, before ending the turn); `winter_9`/`winter_9_b` are start-of-turn saves and have the record gone. That is the whole lifecycle, observed on a controlled pair for the first time, and it means mid-turn saves should be *expected* to carry tombstones rather than treated as anomalies. `[confirmed]`

## The rout mechanic (`FUN_00438fb0`) — new

Two exchanges in this recording end with the word **`routed`** rather than a number, against defenders that the 40% cap mathematically cannot kill:

```text
3rd Dragoons Battalion   Heavy cavalry  Troops 2,429
  ATTACKS
3rd Guards Battalion     Heavy infantry Troops   360
  UNIT LOSSES   Attacker 6   Defender routed        ← cap would be ⌊0.4×360⌋+1 = 145
```

Chasing that led to `FUN_00438fb0(slot)`, which the melee function calls on **both** participants after every exchange and the shooting function calls on the target after every shot — and which no report had touched. It is the game's morale/strength collapse check:

```c
size      = unitTypeTable[type].standardBattalionSize;   // DAT_00478fca, i.e. table field +0x1A
troops    = DAT_004a034c[slot];
morale    = DAT_004a0350[slot];

if (troops >= size / 25 && morale > 19) {
    if (morale > 39) return;                    // safe outright
    if (Random(morale) + Random(morale) > 29) return;    // survived the check
}
// ---- the unit routs ----
FUN_00438f78(slot);                             // troops = 0, its grid square cleared
for each unit on the same side:                 // cascade
    morale -= 6;  if (morale < 30) FUN_00438f78 removes it too   // one level only: no further
                                                    // cascade and no +5 for these
for each unit on the other side:
    morale = min(99, morale + 5);
    if it was targeting the routed unit, clear its target
if (either side now has zero live units) battle over
```

So the rout threshold is the unit type's **standard battalion size divided by 25** — which makes `unit-type-stat-table-in-dat.md`'s `+0x1A` field do double duty (recruitment batch size *and* battle collapse floor):

| | Light inf | Heavy inf | Archers | Light cav | Heavy cav |
| --- | ---: | ---: | ---: | ---: | ---: |
| Standard battalion size (`+0x1A`) | 15,000 | 6,000 | 3,500 | 7,000 | 2,500 |
| **Rout threshold (`/25`)** | **600** | **240** | **140** | **280** | **100** |

Both observed routs land exactly on it:

| Routed unit | Type | Troops before | Loss applied (cap) | Troops after | Threshold | Routed? |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 3rd Guards Battalion | heavy infantry | 360 | 145 | 215 | 240 | **yes — 215 < 240** |
| 2nd Bowmen Battalion | archers | 207 | 83 | 124 | 140 | **yes — 124 < 140** |

A third case is consistent on the shooting side: a light-cavalry unit at 594 troops takes a shot and the panel prints `Unit destroyed !` — light cavalry's threshold is 280, and that shot's maximum possible loss (`min(shooterTroops/3, targetTroops/2)` doubled = 594) easily crosses it.

Three consequences, all of which change how this project has been reading its own battle data:

1. **Nothing is ever ground down to exactly zero by the loss formula.** Both loss caps are 40% of the side's *own* troops, so troops can only asymptote toward 1. Every unit this project has ever recorded as "wiped" in a tactical battle — the five in battle 1, the three in battle 2 — was removed by this function, not by attrition. `full-battle-resolution-rome-vs-gaul.md` explained Rome's two heavy-cavalry units going to exactly 0 as `0.6ⁿ` compounding on small units; the real mechanism is this function. The observation stands, the explanation was wrong. `[confirmed, corrects a prior report]` *Which* branch removed them is not settled. This consequence first said heavy cavalry has "the lowest rout threshold in the game (100)", so its small units "crossed it early". **That is backwards** *(corrected 2026-09-23)*: the floor is 4% of a full battalion for every type, and at equal troops a lower floor takes more losses to cross. What matters is troops relative to the floor. 1st Dragoons (755, 7.6× its floor, the second-closest unit in Rome's army) was destroyed in both battles, which makes small-unit proximity a **candidate** for it `[derived]`. 3rd Dragoons (2,432, 24× its floor, a near-full battalion) died in battle 1 and lost only 95 troops in battle 2. For battle 1 the floor gives it no special exposure, and which branch removed it (troops, the 20–39 morale test, or the cascade in consequence 3) is **[open]**, since battle 1's exchanges were not captured. The morale branches were not easy to reach either `[derived]`. Rome's units began at tactical morale 68–90: strategic 68, no `+3` for a human side, and the `[60, 90]` clamp, all in [battle-quality-promotion-and-morale-array-decompiled.md](battle-quality-promotion-and-morale-array-decompiled.md). Either morale branch therefore needed a net fall of at least 29 points. That is possible late in the battle, after several friendly routs (−6 each) and lost exchanges (−3 each), but it works against +2 per won exchange and +5 per Gaul rout. Nor does battle 1's destroyed set follow floor proximity: 1st Foot, closest to its floor (6.8×), survived, while 5th Bowmen (24×) died. See [full-battle-resolution-rome-vs-gaul.md](full-battle-resolution-rome-vs-gaul.md)'s revised note.
2. **Morale is a second, independent kill condition.** A unit at any troop strength routs outright at morale ≤ 19, and routs on a coin-flip-ish check (`Random(m)+Random(m) ≤ 29`) anywhere in 20…39. `full-battle-resolution-rome-vs-gaul.md`'s info-panel screenshot of a unit at `Morale: very low` was a unit that was one bad roll from vanishing.
3. **Routs cascade, one level deep.** Every rout that `FUN_00438fb0` itself decides costs every surviving friendly unit 6 morale and removes anyone left below 30, while handing every live enemy unit +5 (capped at 99). A unit the cascade removes goes through `FUN_00438f78` directly, so it triggers no second cascade and no further +5. This report first said "(recursively)", which the decompiled loop does not do *(corrected 2026-09-23)*. That is a genuine army-collapse mechanic, and it is the most plausible explanation for why these battles end in *total* annihilation of the loser (0 troops of every type, twice) rather than a fighting retreat: once a side starts losing units the morale spiral finishes it. Nothing in `game-design.md` has an equivalent.

## The 40% cap: confirmed on the attacker side, and five more defender hits

`battle-recording-melee-cap-confirmed.md` pinned `⌊0.4 × troops⌋ + 1` on four defender-side exchanges and explicitly left open that *"every attacker-side loss [is] still just 'plausible'"*. This recording closes that, because it caught a badly-losing attacker:

```text
6th Foot Battalion   Light infantry  Troops 7,135      ← Gaul
  ATTACKS
3rd Guards Battalion Heavy infantry  Troops 5,405      ← Rome
  UNIT LOSSES   Attacker 2,855   Defender 49
```

`⌊0.4 × 7,135⌋ + 1 = 2,854 + 1 = 2,855`. **Exact.** The attacker-side cap is now confirmed to the integer, on the same formula and the same `+1`. `[confirmed]`

All 15 melee exchanges read from this recording (both sides' battalions use the same naming scheme, so rows are not labelled by nation except where the roster makes it unambiguous):

| # | Attacker | Troops | Defender | Troops | Atk loss | Def loss | `⌊0.4·def⌋+1` |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: |
| 1 | 6th Foot (light inf, Gaul) | 7,135 | 3rd Guards (heavy inf, Rome) | 5,405 | **2,855** ← atk cap | 49 | 2,163 |
| 2 | 2nd Guards (heavy inf) | 4,668 | 3rd Guards (heavy inf) | 3,216 | 85 | **1,287** | **1,287** |
| 3 | 3rd Guards (heavy inf) | 5,356 | 3rd Guards (heavy inf) | 1,929 | 90 | 702 | 772 |
| 4 | 1st Dragoons (heavy cav) | 718 | 3rd Guards (heavy inf) | 1,227 | 16 | 225 | 491 |
| 5 | 8th Guards (heavy inf) | 2,930 | 2nd Dragoons (heavy cav) | 2,151 | 77 | 551 | 861 |
| 6 | 3rd Foot (light inf) | 14,619 | 2nd Dragoons (heavy cav) | 1,600 | 714 | 573 | 641 |
| 7 | 3rd Dragoons (heavy cav) | 2,432 | 2nd Bowmen (archers) | 1,982 | 3 | 715 | 793 |
| 8 | 6th Guards (heavy inf) | 4,267 | 2nd Guards (heavy inf) | 4,165 | 221 | 603 | 1,667 |
| 9 | 2nd Guards (heavy inf) | 4,221 | 3rd Guards (heavy inf) | 1,002 | 13 | **401** | **401** |
| 10 | 3rd Guards (heavy inf) | 5,266 | 3rd Guards (heavy inf) | 601 | 9 | **241** | **241** |
| 11 | 4th Guards (heavy inf) | 4,948 | 2nd Guards (heavy inf) | 3,361 | 136 | 743 | 1,345 |
| 12 | 8th Guards (heavy inf) | 2,665 | 2nd Dragoons (heavy cav) | 348 | 13 | **140** | **140** |
| 13 | 3rd Foot (light inf) | 13,905 | 2nd Dragoons (heavy cav) | 208 | 15 | **84** | **84** |
| 14 | 3rd Dragoons (heavy cav) | 2,429 | 3rd Guards (heavy inf) | 360 | 6 | *routed* | 145 |
| 15 | Gallic mercenaries (light inf) | 6,438 | 2nd Bowmen (archers) | 207 | 2 | *routed* | 83 |

**Five more exact defender-cap hits** (rows 2, 9, 10, 12, 13), one exact attacker-cap hit (row 1), and every other row strictly below its cap. Combined with the earlier six exchanges, the cap formula is now confirmed on eleven separate observations across two recordings and both sides of the exchange.

Row 1 is also the clearest type-effectiveness data the project has: **light infantry attacking heavy infantry is catastrophic for the attacker** — it loses 40% of itself and inflicts 49 casualties, a 58:1 exchange rate — while row 6 (light infantry attacking heavy cavalry with a 9:1 troop advantage) still loses more than it inflicts. Both are consistent with the matrix's light-infantry row (`4 1 0 3 0`) being genuinely terrible against everything but light infantry and light cavalry.

## `+0x20` in the unit-type table identified: shooting vulnerability

`unit-type-stat-table-in-dat.md` left fields `+0x20` and `+0x26` unidentified. `FUN_0043845c` (the shooting-range helper) reads `+0x20` — `DAT_00478fd0`, i.e. table base `+0x20` — **indexed by the target's type, not the shooter's**:

```c
base = (shooterTroops × shooterQuality × shooterMorale × vuln[targetType])
       / (shooterTroops × 5 + 150000);
if (gridDistance(shooter, target) < range[shooterType]) base *= 2;
range_ = min(min(shooterTroops / 3, targetTroops / 2), base) + 1;
loss   = Random(range_) + Random(range_);       // FUN_0043910c
```

| | Light inf | Heavy inf | Archers | Light cav | Heavy cav |
| --- | ---: | ---: | ---: | ---: | ---: |
| `+0x20` (shooting vulnerability) | 18 | **2** | 18 | 15 | **4** |

That is exactly the shape the name implies: unarmoured targets (light infantry, archers) take nine times the fire that heavy infantry does, with heavy cavalry nearly as protected and light cavalry in between. The 23 shooting exchanges read off this recording bear it out:

| Shooter | Troops | Target | Troops | `vuln` | Loss |
| --- | ---: | --- | ---: | ---: | ---: |
| 3rd Lancers (light cav) | 6,695 | 2nd Lancers (light cav) | 3,331 / 2,948 / 2,599 / 2,386 / 2,223 | 15 | 383 / 152 / 213 / 163 / 354 |
| 3rd Lancers (light cav) | 6,625 | 2nd Lancers (light cav) | 851 / 702 / 594 | 15 | 70 / 108 / *destroyed* |
| 2nd Lancers (light cav) | 1,121 | 1st Bowmen (archers) | 2,193 / 2,092 / 2,044 | 18 | 71 / 48 / 4 |
| 3rd Foot (light inf) | 2,907 | 4th Bowmen (archers) | 1,326 | 18 | 98 |
| 3rd Foot (light inf) | 10,799 | 4th Bowmen (archers) | 3,312 | 18 | **675** |
| 4th Foot (light inf) | 14,726 | 3rd Foot (light inf) | 8,704 | 18 | 367 |
| 5th Foot (light inf) | 13,676 | 2nd Guards (heavy inf) | 4,583 / 4,469 / 4,391 | 2 | 68 / 78 / 108 |
| 6th Foot (light inf) | 4,280 | 2nd Guards (heavy inf) | 4,283 / 4,246 / 4,242 | 2 | 29 / 4 / 21 |
| 4th Foot (light inf) | 12,285 | 1st Dragoons (heavy cav) | 282 / 218 | 4 | 64 / 61 |
| 2nd Foot (light inf) | 5,203 | 2nd Dragoons (heavy cav) | 392 | 4 | 44 |

The decisive comparison is the one where the *same shooter* fires at two different target types. 4th Foot (light infantry) does a mean 62 to heavy cavalry at 12,285 troops and 367 to light infantry at 14,726 — feeding those back through the formula gives an implied `quality × morale` of 269 and 310, i.e. the same unit, consistent. Drop the `vuln` factor and the same two observations imply 1,076 and 5,573 for one unit inside one battle, which nothing can explain. Across all ten shooter groups the implied `quality × morale` lands in 269…710, exactly the band quality 6–9 × morale 40–90 produces. `[confirmed — identification; the implied constants are consistent, not independently pinned, since quality and morale are battle-local and unobservable in a save]`

That was the last unidentified field in that table: `+0x26` was already identified in the design-audit pass as the per-type combat-power weight used by the strategic strength function `FUN_0044A8CC`.

## The effectiveness matrix's axis ambiguity, resolved

`combat-type-effectiveness-matrix.md` chose `value[attackerType][defenderType]` because it "produces coherent unit-vs-unit relationships" and flagged the orientation as a reasoned guess. Re-reading the melee function's index arithmetic settles it — no new recording needed, it was in the dump the whole time:

```c
attackerType = *(short *)((int)local_24 + 6);          // DAT_004a034a[attackerSlot]
defenderType = (&DAT_004a034a)[targetSlot * 0x16];

atkPower = (*(short *)(&DAT_0047946c + defenderType*2 + attackerType*10) * atkTroops
            * (atkQuality*10 + atkMorale)) / 2000 + 12;
defPower = (*(short *)(&DAT_0047946c + attackerType*2 + defenderType*10) * defTroops
            * (defQuality*10 + defMorale)) / 2000 + 12;
```

`&DAT_0047946c` is a byte pointer: the row stride is **10 bytes** (5 words) and is indexed by the **attacker's** type; the column stride is 2 bytes and is indexed by the **defender's** type. So the table as read row-major out of the DAT is `value[attackerType][defenderType]`, which is the orientation that report already published. Both type fields are independently confirmed — the very same `local_24 + 6` and `DAT_004a034a[target]` values index the unit-type *name* table (`&DAT_00478fb0 + type * 0x28`) to print "Light infantry"/"Heavy infantry" in the panels this report transcribes. `[confirmed]`

The same read also pins the previously hand-waved "quality term": it is literally `quality × 10 + morale`, with quality the 5–9 tier code and morale the battle-local `DAT_004a0350` value.

## Two small corrections to `decompiled-combat-formula-structure.md`

`FUN_00448fd0(a, b)` is `min(a, b)` on shorts (`if ((short)b <= (short)a) a = b; return a;`). That report describes two of its uses as a *floor* (`clamp(..., floor≈4)`, `clamp(..., floor≈3)`); they are **ceilings**:

- `defFactor = min(4, focusCount)` — the focus-fire counter is capped at 4, not floored at it. With `focusCount` attackers on one defender, the attacker-loss multiplier is `(5 − defFactor)/5` (4/5, 3/5, 2/5, 1/5) and the defender-loss multiplier is `(2·defFactor + 5)/5` (7/5, 9/5, 11/5, 13/5). Piling a fourth unit onto one target is worth 3.25× the damage and a fifth of the return fire; a fifth unit adds nothing.
- the shooting side-effect on morale is `min(3, loss × 35 / (targetTroops + 1))` — a hit of at most 3 morale per shot.

## The promotion "adjacency rule" does not survive the replay

`battle-quality-promotion-and-morale-array-decompiled.md` derived, from battle 1 alone: *"an 'average'-quality unit occupying an army slot immediately adjacent to a slot whose unit was destroyed in the same battle is promoted to 'good'"*, holding with zero exceptions across 13 units. Battle 2 breaks it three ways.

Battle 2 destroyed pre-battle slots **0, 3, 6**. It promoted slots **7** (2nd Bowmen, average → good), **9** (3rd Foot, average → good) and **11** (Gallic mercenaries, very good → **elite**).

| Prediction | Outcome |
| --- | --- |
| slot 5 (8th Guards, average, adjacent to destroyed slot 6) → promoted | **not promoted** |
| slot 9 (3rd Foot, average, adjacent to 8 and 10, neither destroyed) → not promoted | **promoted** |
| rule only fires average → good | **very good → elite** observed |

What does fit both battles is the rule the instant resolver already uses in code (`decompiled-diplomacy-peace-terms-and-instant-battles.md`): `quality = max(quality, 6)` then `if (Random(4) == 0) quality = min(quality + 1, 9)` for every surviving unit. Battle 1 promoted 3 of 14 survivors; battle 2 promoted 3 of 16 — 6 of 30 combined, against 7.5 expected at p = ¼, and the `min(quality+1, 9)` clause is exactly the very-good→elite jump battle 2 produced. Battle 1's adjacency pattern (3 of 3 adjacent average units promoted, 0 of 6 non-adjacent) was a 1-in-84 coincidence, which is unlikely but is what a second sample says happened.

So: **the tactical path's post-battle promotion is best modelled as the same uniform ~1-in-4 roll per surviving unit as the instant path**, and the adjacency rule should be withdrawn. The implementing code still hasn't been located, so this remains the empirical reading of two battles, not a decompiled fact. `[derived, supersedes a prior derived rule]`

## What this does not establish

- The promotion code itself — still not located in any recovered function; the 1-in-4 reading is inference from 30 units across two battles.
- Exact predicted numbers for any single exchange: `quality` and `morale` inside a battle are battle-local arrays (`DAT_004a034e`/`DAT_004a0350`) that never reach a save file, so every formula check here is a magnitude/ratio check plus the two caps, which are troop-only and therefore exactly checkable.
- Whether the rout check's `Random(m) + Random(m) > 29` branch was actually exercised in these battles (no unit's morale is observable), or whether every observed rout was the troop-threshold branch. The two transcribed cases are both cleanly explained by the threshold alone.
- Which side each unlabelled exchange row belongs to — both nations field identically-named battalions.

## Reproduction

```text
dotnet run --project src/IC2.Inspect -- --compare-saves saves/1_rome_270_winter_7.sav saves/1_rome_270_winter_7_b.sav
dotnet run --project src/IC2.Inspect -- --to-json saves/1_rome_270_winter_7.sav   w7.json
dotnet run --project src/IC2.Inspect -- --to-json saves/1_rome_270_winter_7_b.sav w7b.json

# the exchange panels: crop the Information pane and tile 12 frames per sheet
ffmpeg -ss 60 -t 300 -i "recordings/bandicam 2026-09-13 22-49-01-893.mp4" \
       -vf "fps=1/3,crop=810:560:1110:90,tile=3x4" tiles/t_%03d.png
ffmpeg -i "recordings/bandicam 2026-09-13 22-49-01-893.mp4" -vf fps=1/15 f6a/f_%03d.png
# f6a/f_037.png is the "Battle ended" dialog; f6a/f_005.png is the attacker-cap exchange.

# in all_app_functions.txt: FUN_00438fb0 (rout), FUN_00438f78 (remove unit),
#   FUN_00438420 (focus count), FUN_0043845c (shooting range), FUN_00448fd0 (min),
#   FUN_004393ec (melee), FUN_0043910c (shooting)
```

## Next checks

1. Simulate both battles with the now-complete rule set (matrix + unit-type table + melee/shooting formulas + the rout check) over many seeds and compare the *distribution* of Rome's final troop count against the two observed outcomes, 63,282 and 75,536. Two samples from the same starting state is exactly the data a distribution test needs, and this project has never had it before.
2. The rout cascade (`−6` morale to every friendly unit, `+5` to every enemy) is the one part of the mechanic with no direct observation. A recording where the info panel's `Morale` line is captured for the same unit before and after a nearby unit routs would confirm it, and would also give the first real reading of the morale scale's numbers against its tier names.
3. The `+0x20` identification is supported by magnitudes and by one same-shooter cross-type comparison, not pinned to the integer, because battle-local quality and morale never reach a save. A recording that captures the per-unit info panel (which prints both `Quality` and a tiered `Morale`) *and* a shot by that same unit in the same minute would let one exchange be predicted end to end, closing the last gap in the shooting formula.
