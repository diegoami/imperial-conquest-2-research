# The pending-diplomatic-offer block confirmed, an army split checked against its code, and Naupactus

The rest of `notes/2_rome_s.txt` and the first entry of `notes/3_rome.txt`, covering `1_rome_270_winter_7_b.sav → 1_rome_270_winter_9_b.sav → 1_rome_270_winter_11.sav` (recording `bandicam 2026-09-13 23-14-41-582.mp4`, 2:50). The battle that opens this sequence is in [battle-replayed-rout-mechanic-and-combat-constants.md](battle-replayed-rout-mechanic-and-combat-constants.md); this report covers everything else in the two notes. Two of the three items are clean confirmations of things already decompiled, one of them settling an inferred SAV field exactly; the third is a plainly negative result that is worth recording so it isn't re-investigated.

## The pending-diplomatic-offer block, pinned to two nations

`decompiled-turn-and-calendar-sequencing.md` found that `TPremierForm_StartTurn` checks, at the start of each nation's turn, for a pending trade or alliance proposal aimed at that nation and announces it as *"X wants to trade/form an alliance with Y"* — and identified, by elimination, "the 4-byte block right after the 61-byte-record region" in the SAV as where that lives. It was an inference from which block was left over, with no observation attached.

The two notes supply exactly the right pair of observations: *"Greece wants to trade with Rome"* between `winter_7_b` and `winter_9_b`, and *"Bythinia wants to trade with Rome"* between `winter_9_b` and `winter_11`. Reading the 4 bytes at **`fileLength − 22`** across the whole series:

| Save | Bytes | Reads as | News that turn |
| --- | --- | --- | --- |
| `1_rome_270_winter_7.sav` | `FF FF 01 00` | −1 · 1 | — |
| `1_rome_270_winter_7_b.sav` | `FF FF 01 00` | −1 · 1 | — |
| `1_rome_270_winter_9.sav` | `FF FF 01 00` | −1 · 1 | — |
| `1_rome_270_winter_9_b.sav` | **`07 00 01 00`** | **7 · 1** | **"Greece wants to trade with Rome"** |
| `1_rome_270_winter_11.sav` | **`0B 00 01 00`** | **11 · 1** | **"Bythinia wants to trade with Rome"** |

Nation 7 is Greece and nation 11 is Bithynia in this project's confirmed nation-index table, and `1` is the relation code for **trade** in the 16×16 relation matrix decompiled in `decompiled-diplomacy-peace-terms-and-instant-battles.md`. So the block is:

```text
short  proposingNationIndex     // 0xFFFF = no offer pending
short  proposedRelationState    // reuses the relation-matrix encoding: 1 = trade, 2 = alliance
```

Both shorts match independently, on two different nations, in two consecutive saves — and the field goes back to `−1` on the saves either side. The second word being a relation code rather than a bespoke "offer type" enum is the part that was not predictable from the turn-sequencing report's description. `[confirmed]`

The offer is addressed at the nation whose turn is starting (Rome in every save here), so the block holds one pending offer at a time for the whole game, not one per nation — consistent with the block being 4 bytes rather than 64.

## The army split: the code's constants, checked against a real split

`decompiled-unit-map-orders-and-record-fields.md` decompiled `TUnitMap_SplitArmy`/`FUN_00449F08` and listed the new record's constants — **≥ 2 units required, army-table cap 198, moves 0 for a human nation, supplies 0, money 0, morale 59** — all read from code, none checked against an observed split. The note's *"the other army was split and now there are three armies total"* provides one.

`1_rome_270_winter_9_b.sav → 1_rome_270_winter_11.sav`, Rome's army 0 becoming armies 0 and 13:

| | Before (army 0) | After (army 0) | After (army 13, new) |
| --- | ---: | ---: | ---: |
| Troops | 75,536 | 37,081 | 38,455 |
| Units | 16 | 9 | 7 |
| Morale (`ArmyRecord +14`) | 66 | 64 | **57** |
| Money | 256 | 156 | 100 |
| Position | (88, 26) | (92, 27) | (93, 28) |

- **Troops and units are conserved exactly**: `37,081 + 38,455 = 75,536`, `9 + 7 = 16`. No rounding, no loss, no minimum. `[confirmed]`
- **Morale 59 is confirmed, indirectly but cleanly.** The new army reads 57, not 59 — but a full turn elapsed, and `supply-driven-morale-and-fleet-attrition.md` established that the weekly tick rewrites `+14` from the army's supply percentage, `−2` when below 10%. Both armies are at **0% supply**, and the parent army moved `66 → 64` in the same window: exactly `−2`. `59 − 2 = 57`. The new army was created at 59 and took the same penalty as its parent. `[confirmed]`
- **Money is not 0 as `FUN_00449F08` sets it — because the split dialog lets the player change it before committing.** The recording shows `TSplitArmyUnit` directly, and it is a two-pane transfer screen rather than a confirmation box: *"Units in first army"* / *"Units in second army"*, a `Transfer` and a `Disband` button under each, live `N units / N troops` totals under both, and below that **`First army's supply` / `Second army's supply` and `First army's money` / `Second army's money` spinners with 10s and 100s steppers** — the same shape as the `TArmyToArmy` dialog confirmed in `army-to-army-transfer-confirmed.md`. A mid-drag frame shows the two panes at `13 units / 63,458 troops` and `3 units / 12,078 troops` while the final save reads 9 and 7, so the player was still moving units at that point.

  So `FUN_00449F08`'s `money = 0`, `supplies = 0` are the *initial* values the dialog opens with, not the committed ones; the observed `156 / 100` is the player having pushed the money spinner, and the exact conservation of 256 talents is the dialog's reciprocal-transfer behaviour, not an accident. The decompiled constant and the observation agree once that is accounted for. `[confirmed]`

### "Supplied from Mediolanum / Brixia" is descriptive, not a mechanic

The note says one of the new armies is *"supplied from Mediolanum, the other from Brixia"*. There is **no home-city, garrison-of-origin or supply-source field** on an army record — `decompiled-unit-map-orders-and-record-fields.md` accounts for every word of the 16-byte army header (`x`, `y`, `owner`, covered map cell, moves, supplies, money, morale) and `army[+8]`, the one field that might have looked like a candidate, is the **terrain code of the cell the army is standing on** (army 0 reads 2 = plain, army 13 reads 5). Nothing persists a relationship to a city.

The save data says the same thing. Both armies finish at **0 tons of supply, 0%**, and the two named cities were nearly empty when the armies reached them:

| City | Position | Supply at `winter_9_b` | Supply at `winter_11` |
| --- | --- | ---: | ---: |
| Mediolanum | (91, 27) | 8 | 0 |
| Brixia | (94, 27) | 0 | 0 |

Army 0 ends adjacent to Mediolanum and army 13 adjacent to Brixia, so the positions match the description — the player walked each army to a city and used the city-to-army resupply dialog confirmed in `galatia-elimination-and-city-resupply-confirmed.md`. It simply delivered nothing worth having: 8 tons against a 370-ton capacity, and 0 from Brixia. The phrase records where the player clicked, not a state the game tracks. Worth saying plainly because the same wording recurs throughout the session notes (`1_rome.txt`: *"Both armies resupply at Brixia and Verona"*, *"First army supplied from Arretum"*) and it would be easy to read a mechanic into it. `[confirmed — negative]`

## Naupactus falls to Illyria: the unity constants, verified

`decompiled-city-capture-resolution.md`'s next-check 2 asks for the decompiled `unity +9 / −15` transfer constants to be cross-checked against a real capture. Naupactus is close to that: it is the **only ownership change in the whole turn** `winter_7_b → winter_9_b`.

| Nation | Unity before | Unity after | Δ | Cities |
| --- | ---: | ---: | ---: | --- |
| Greece (loser) | 528 | 513 | **−15** | 19 → 18 |
| Illyria (winner) | 706 | 715 | **+9** | 11 → 12 |

Exact, both sides, asymmetric as decompiled. The caveat is that unity has other sources (a battle elsewhere would also move it) so this is one turn's clean read rather than a same-day isolated pair — but no battle involving either nation appears in this turn's news, and the city-count fields move by exactly one each, so the attribution is about as tight as a full-turn save pair gets. `[confirmed]`

Illyria's treasury moves `−2021 → −1973` (`+48`) rather than by `fortification × 3000`, which is nowhere near any plausible fortification value — so the **wealth** half of that next-check is *not* confirmed by this data. Either the wealth field is not `treasuryTalents` (most likely: `decompiled-diplomacy-peace-terms-and-instant-battles.md` uses nation field `+0x44C` for "wealth" and the reparation formula, which is a different field from the treasury at `+0x438`), or the constant is wrong. Left open.

> **Correction (2026-09-14):** closed in [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md). The `+48` is the capture's treasury credit to the new owner, `contribution × 4` with Naupactus's contribution `15 × 25 / 30 = 12`; the tax base (`+0x44C`) moves by the same `± 48`; and "wealth" is a third field, `+0x430`, which moves by `± population × 3000` (`± 75,000`), not fortification.

## A side observation: the AI turn replayed almost identically

Because the battle was replayed from the same save, the *same* AI turn was also played twice — `winter_7 → winter_9` and `winter_7_b → winter_9_b`. Diffing the two resulting worlds against each other, the **only** two things that differ in the entire game state are:

- Rome's own army 0 — the battle result, which is the point of the experiment; and
- Illyria's army 12, whose eight units differ by a few troops each (42,034 vs 42,024 total, net −10) from that turn's supply attrition rolls.

Everything else is byte-for-byte the same decision: Naupactus falls to Illyria either way, the same Carthaginian fleet is lost at sea, all nine other AI armies move to identical coordinates, and every nation's unity, treasury, city count and tax field matches exactly.

So AI *decisions* in this window are deterministic given the world state, while the random-draw-driven arithmetic downstream of them diverges — unsurprising, since the player's battle consumed a different number of RNG draws in between. It is not proof that the AI never rolls dice (one turn, one window), but it does mean **a replayed turn is a usable controlled experiment**: the AI won't wander off and invalidate the comparison. That is worth knowing before designing any future A/B of this kind. `[derived]`

## What this does not establish

- Whether the pending-offer block can hold an alliance proposal (`2`) as well as a trade one — only `1` was observed, twice.
- What sets the block, and whether the AI's decision to offer is reachable in code (the roadmap already scopes unnamed AI decision code out).
- Whether the split dialog's supply spinner is constrained by the receiving army's capacity (`troops / 100`), the way the city-to-army dialog appears to be — both armies were at 0 supply here, so nothing was exercised.
- ~~The `wealth ± fortification × 3000` half of the capture formula~~ — closed: it is `± population × 3000` on `+0x430`, see [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md).
- Whether AI determinism holds over more than the one replayed turn examined here.

## Reproduction

```text
ffmpeg -ss 98 -i "recordings/bandicam 2026-09-13 23-14-41-582.mp4" -frames:v 1 \
       -vf "crop=740:340:0:0" split.png            # the TSplitArmyUnit dialog

dotnet run --project src/IC2.Inspect -- --to-json saves/1_rome_270_winter_9_b.sav w9b.json
dotnet run --project src/IC2.Inspect -- --to-json saves/1_rome_270_winter_11.sav  w11.json
dotnet run --project src/IC2.Inspect -- --compare-saves saves/1_rome_270_winter_9_b.sav saves/1_rome_270_winter_11.sav

python -c "d=open('1_rome_270_winter_11.sav','rb').read(); print(d[-22:-18].hex())"   # 0b000100
```

## Next checks

1. A single-click controlled pair around one `SplitArmy` (save, split with the money/supply spinners left alone, save, no turn end) would pin the new record's untouched defaults — money, supply and moves — directly, and is cheap.
2. Offer an alliance rather than a trade and save at the receiving nation's turn start, to confirm the block's second word takes `2`.
3. ~~Identify which nation field the capture formula's "wealth" term actually writes~~ — done in [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md).
