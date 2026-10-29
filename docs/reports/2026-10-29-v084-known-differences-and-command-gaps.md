# Remake v0.8.4: three known differences remain, and its commands accept what both interfaces refuse

**Provenance:** draft from `diegoami/ic2-conquest`, branch `research/diff084-stats233`, commit
`2e5c8dc`. Conquest [#229](https://github.com/diegoami/ic2-conquest/issues/229) and
[#230](https://github.com/diegoami/ic2-conquest/issues/230) (tracker #228). Releases
[`run-exp-diff084-orders`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-orders),
[`run-exp-diff084-orders-b2`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-orders-b2)
and
[`run-exp-diff084-tooling`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-tooling).
Their SHA-256s are committed at `runs/experiments/data/<run>/SAVES.sha256`. Remake **v0.8.4**
(`d9cc71bc82e22ad1d3d7c373c3d80d61ed0bcbeb`), `classical-faithful`. Original:
`Imperial Conquest 2 fast rollingsave seed.exe` (SHA-256 `354d8265…`), startup seed 12345. Harness:
ic2-conquest `difftest/`.

**Tag:** `[confirmed, partial]`. These are original-vs-remake differential runs under Wine, with
the same start save and the same orders in both games. Not run on native Windows. The remake
*interface* rows are `[code: remake v0.8.4]`: read from source, not played.

**Review note (2026-10-29):**
- **Release integrity:** all three archives were downloaded. All 494 saves match the committed
  `SAVES.sha256` files (400 + 30 + 64 of 494 OK).
- **§1 reproduces.** Rome's fleet under construction reads build city 82 (Caere) in the original and
  71 (Pisae) in the remake. That holds in `fleet-10`, `fleet-25` (`*-r2`) and `fleet-two`, with
  equal ship counts and treasuries.
  - The first `fleet-25/original` run built 34 ships, not 25 (treasury 1,860). The harness judged it
    `harness` (an input fault) and reran it as `*-r2`, which the draft cites. This is disclosed,
    not a contradiction.
- **§2 reproduces.**
  - **Recruit:** the original driver's receipt reads `Recruit amount stuck at 1200, wanted 1000`.
    In the remake, `self5-remake-1/a003.SAV` has a new heavy-infantry slot of 1,000 troops and the
    treasury down 100 (2,200 → 2,100).
  - **Moves:** in `move-far` and `move-sea` the original's army is unchanged. The remake's army
    goes from (100,37) with 8 moves to (98,41) with 4, and from (120,53) with 8 to (121,54) with 7.
  - **Remake source at tag `v0.8.4`:**
    - `RecruitUnitDialogModel` (`godot/UI/Dialogs/StrategyDialogModels.cs`:538) documents the
      bounds `standardBattalionSize / 5` … `standardBattalionSize`.
    - `MapClickRules.cs`:302–306 returns `Nothing` for an army clicked on a non-land tile.
    - `RecruitStandingUnitCommandHandler` checks the amount only as `Troops <= 0`. Its other
      refusals are the slot table, the mobilization cap and town eligibility.
  - **Original dialog minimum:** 1,200 is the heavy-infantry minimum of
    [`2026-09-29-which-cities-may-recruit-and-troop-amounts.md`](2026-09-29-which-cities-may-recruit-and-troop-amounts.md)
    (battalion 6,000 / 5).
- **§3 is corrected in two counts and one attribution.** I compared `toy3b-original-1` with
  `toy3b-remake-1` using my own reader:
  - `a000`–`a003` agree in every gameplay field.
  - At `a004` (after End turn), **six** AI armies (3, 5, 8, 9, 12, 13) and two fleets differ, not
    seven armies. The harness's own report for the pair lists the same six.
  - The **48** cities with different supplies belong to Gaul, Celtiberia, Bithynia **and Galatia**.
    Three of them are Galatia's (Acroinon, Gordium, Iconium), alongside Galatia's army 12
    (supplies 193 vs 111). So the supply differences are not all recruitment-driven.
  - Recruit slots differ for Gaul, Celtiberia and Bithynia. Mobilization differs: Gaul 50 vs 63,
    Celtiberia 56 vs 73 and Bithynia 47 vs 45. Treasuries differ for those three.
  - The pending offer comes from Celtiberia (8) vs Seleucid (2).
- **Rome's raw bytes differ, its gameplay fields don't.** Rome's 1,172-byte nation record already
  differs at `a000`–`a003` in `+0x482` (the Save-As byte of
  [`2026-10-21-original-sav-semantic-atlas.md`](2026-10-21-original-sav-semantic-atlas.md)) and in
  the view origin `+0x486`/`+0x488`. After End turn it also differs in the filler of empty recruit
  slots. Its relations, occupied slots, treasury, scalars, cities, armies and fleets are equal.
- **§3's "52 single-order cases" is restated.** I could not reproduce that count. The final verdict
  files hold **54** cases (46 `same`, 6 `differs-immediate`, 2 `refusal-difference`), 6 of which
  have more than one order.
  - In all 54, End turn **added no new difference** to Rome's records.
  - 46 are equal after End turn. The 8 others carry only their immediate difference: fleet city ×3,
    army position ×2 and ally relation ×3
    ([`2026-10-29-war-declaration-ally-cooldown-diff230.md`](2026-10-29-war-declaration-ally-cooldown-diff230.md)).
- **Dangling citation:** the draft cites `findings/2026-10-29-ai-fleet-hunt-absent-in-remake233.md`.
  No ic2-conquest branch had that file on 2026-10-29. It is not promoted or relied on here.

## 1. Build fleet still uses a different city (known since 2026-10-09)

[`2026-10-09-fleet-build-city-nearest-capital.md`](2026-10-09-fleet-build-city-nearest-capital.md)
found that the original builds at the free coastal city nearest the capital, while the remake takes
the first free one in world order. At v0.8.4 this is unchanged. From the Rome 270 BC start, the
original builds at **Caere** (city 82) and the remake at **Pisae** (city 71). The fleet's size and
its cost agree.

Evidence (run `run-exp-diff084-orders`, turn 0720): `fleet-10/original/a001.SAV` vs
`fleet-10/remake/a001.SAV`; `fleet-25/original-r2/a001.SAV` vs `fleet-25/remake-r2/a001.SAV`;
`fleet-two/{original,remake}/a001.SAV`.

## 2. The remake's engine commands accept orders that both games' interfaces refuse

These differences appear only through the remake's command layer: the CLI, scripts, and anything
that submits `GameSession` commands directly. According to its source, the remake's own interface
refuses these orders as the original does: its dialog clamps the amount and its map click ignores
the order. They matter for automation, and for any AI or tool that issues the same commands.

| Order | Original | Remake interface (source) | Remake command | Evidence |
|---|---|---|---|---|
| Recruit below battalion / 5 (1,000 heavy infantry) | the dialog cannot go below 1,200 (the arrows stop) | the Recruit dialog clamps to battalion / 5 (`RecruitUnitDialogModel`, `godot/UI/Dialogs/StrategyDialogModels.cs`) | `recruit-standing … 1000` is accepted: slot of 1,000 troops, 100 talents | run `run-exp-diff084-tooling`, `toy3-original-1` receipt ("stuck at 1200"); `self5-remake-1/a003.SAV` |
| Move an army toward a sea tile | the click does nothing | the map click does nothing (`godot/UI/MapClickRules.cs`: an army on a non-land tile gets `Nothing`) | `move` walks toward it as far as the shore (4 moves to (98,41); 1 move to (121,54)) | run `run-exp-diff084-orders`, `move-far` and `move-sea`: `original*/a001.SAV` vs `remake*/a001.SAV` |

The engine's only check on the recruit amount is that it is positive
(`RecruitStandingUnitCommandHandler`).

## 3. After the first End turn, the AI nations act differently (known families)

The same orders give identical states in both games up to the first End turn. The orders were tax
20, a move, and a recruit of 1,200 heavy infantry at Rome (run `run-exp-diff084-tooling`,
`toy3b-original-1` vs `toy3b-remake-1`, checkpoints `a000`–`a003`: 0 gameplay-field differences).
Rome's own gameplay records also stay equal after it. Over that End turn (turn 0720 → 0721):
- six AI armies and two fleets stand elsewhere, or have different moves or supplies;
- Bithynia, Celtiberia and Gaul queue different recruits (mobilization: Gaul 50 vs 63,
  Celtiberia 56 vs 73, Bithynia 47 vs 45);
- the pending offer comes from Celtiberia in the original and from Seleucid in the remake;
- the 48 cities whose supplies differ all belong to Gaul, Celtiberia, Bithynia and Galatia. Their
  supply follows the different recruitment and, for Galatia, a differing army.

These are the AI recruitment and diplomacy families of conquest #176 and #177. The remake was given
no recorded original draws here. In all 54 cases of the two order batches, End turn added no
difference to Rome's own records.

## Not covered

Fleet orders, mobilization and unit-level orders (#230 batch 3), battles (#231), multi-turn play
(#232) and random outcomes (#233). The test registry is ic2-conquest's `difftest/REGISTRY.md`.

## What this does not establish

- Native Windows behaviour.
- The remake's interface rows were read from source at v0.8.4, not played.
- Which AI draw or rule produces each §3 difference. Those are the open families, not new findings.
