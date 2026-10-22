# Contradictions surfaced by the original-game manual (conquest #133), consolidated

**Provenance:** relayed by the ic2-conquest session on 2026-10-22 (owner request). ic2-conquest
wrote a user manual of the original game ([issue #133](https://github.com/diegoami/ic2-conquest/issues/133),
closed): 160 pages, on the owner's Drive at `IC2/manual/`. Its screenshot index is in
[ic2-conquest PR #134](https://github.com/diegoami/ic2-conquest/pull/134) (merge `c080439`,
`runs/experiments/data/run-exp-manual133/`). The manual is a synthesis, not a finding, and its
review was same-model only. While writing it, ic2-conquest listed 14 places where the documents
disagree. This report settles each one against **research's own reports** and the pinned
decompilation (`all_app_functions.txt` `2018c205…`). Research did not read the manual itself, no
game was launched, and nothing below is a new play result.

## Outcome per item

| # | Item | Research's state before | Settled by | Change made here |
|---|---|---|---|---|
| 1 | Join fleets over 100 ships | [join-fleets-cap-in-play](2026-10-08-join-fleets-cap-in-play.md) said the refusal is silent, with no dialog | Refusal R15 was played with a screenshot of the box *"There are more than 100 ships in these fleets combined."* (`TUnitMap_JoinFleets`:47260); the cap-in-play run read saves only | Correction note in the cap-in-play report. The boundary (100 accepted, 101 refused) stands |
| 2 | Transfer ships "> 100 ships" refusal | [UF01–UF06](2026-10-08-unit-map-fleet-uf01-uf06.md) attributed that refusal to Transfer ships | [supply-providers-and-transfer-clamps](2026-10-09-supply-providers-and-transfer-clamps.md) §2 (played and code-read): `TFleetToFleet` has no box, the arrows clamp at 100, and emptying a carrying fleet destroys its army | Correction note on UF03 |
| 3 | Melee matrix | The [rules specification](../rules-specification.md) already uses the decompiled table and the −3/+2 morale rule ([2026-10-04-decompiled-tactical-battle-rules](2026-10-04-decompiled-tactical-battle-rules.md)) | — | None. ic2-conquest's rules digest was stale and is now corrected upstream (`4fe93bb`, PR #135). [combat-type-effectiveness-matrix](combat-type-effectiveness-matrix.md) keeps its old title, but its 2026-10-04 banner already says DAT `0x1F3B8` is the AI placement/type-order data, not the melee matrix |
| 4 | Automatic resupply for a human army | The specification was already right (AI path only, [army-purse-writes](2026-10-05-army-purse-writes-and-the-1000-cap.md)). Feature-inventory row **E12** still said "human army" | The purse report | E12 marked as corrected |
| 5 | Selecting an army with 0 moves | Already corrected on 2026-10-11 ([army-moves-field](army-moves-field-signed-and-the-ffff-underflow.md); specification) | g2 | None |
| 6 | Relation thaw on mixed pairs | Row 8 of [war cascade](decompiled-war-cascade-and-peace-paths.md) said only "first 8 columns" | Re-read at `FUN_00451B40` :54908–54931. Columns 0–7 only, and the write goes through `FUN_00449B40`, which sets both sides. A pair with one index below 8 thaws both sides; both below 8 can thaw twice; both 8 or higher never thaw. This matches rebellion107 | Detail added to war-cascade row 8; atlas increment 11 and rebellion notes refined |
| 7 | Mobilise refusal text | [S01–S12](2026-10-08-strategy-menu-s01-s12.md) S05a already cites the exe offset `0x54784` and the 2026-10-12 play (g1 G9) | g1 | None |
| 8 | Ctrl+P "byte-identical" | [K01–K03](2026-10-08-keyboard-shortcuts-k01-k03.md) called the files byte-identical but lists two different hashes (`b3da86b4…`, `ecb0a7e9…`, as in ic2-conquest `MANIFEST-batch1.txt`) | The hashes differ, so the files are not byte-identical | Corrected. Pixel identity is unverified, because the PNGs are not individually downloadable from the release |
| 9 | City panel bracket number | Row UM02 said "troops in training"; [information-window fields](2026-10-05-information-window-fields-and-bands.md) already has the code rule: all the controlling nation's recruit slots at the city, whatever their state | — | UM02 cross-linked |
| 10 | Help file vs code | [H05](2026-10-08-help-reference-tables-h05.md) called the fleet symbol bands "identical" | `FUN_0044A878` bands ships **< 25 / 25–49 / ≥ 50**; the help says 10–25 / 26–50 / 51–100 | H05 corrected. The other help points (winter supply, winter city stores of −2 × pop, news span) are already as the code in the specification; not re-derived |
| 11 | Naval battle random term | Already settled at promotion of [naval-battle-random-term](2026-10-02-naval-battle-random-term.md): the discrete code term `Random(4) × base / 10`. [Naval-battle-army-aboard](2026-10-02-naval-battle-army-aboard.md) leaves `/40` vs `/50` open | — | None |
| 12 | Fleets under construction on the Balance sheet vs the quarterly bill | Not measured anywhere | **Settled (2026-10-22)** by ic2-conquest [fleet under construction not billed](https://github.com/diegoami/ic2-conquest/blob/1f14b4c/findings/2026-10-22-fleet-under-construction-not-billed.md) (PR #137). The quarterly fleet loop at the start of `FUN_00451B40` charges `3 × ships` only for `owner ≥ 0` and `countdown == −1` (re-read here). A paired Wine run from `M133_session1_AUTO0725.SAV` gave Rome's treasury 1,781 → 1,804 without a fleet, and 1,781 → 1,281 at the order then → 1,304 with 50 ships ordered (the same +23); the fleet still has countdown 22. Saves re-hashed and decoded here | The Balance sheet's Fleet line (g1 G2) counts building fleets, so it overstates the next bill by 3 per ship under construction. The specification and g1 are cross-linked |
| 13 | Unit-map visible area 13×13 vs 13×12 | Both figures appear | `TUnitMap_PaintForm` computes its loop bounds from the window's client width and height in 32-pixel steps; the battle probe saw 29×27 | Note in [A01–A10](2026-10-08-area-map-a01-a10.md): the count depends on the window size |
| 14 | Battle window title | "Battlefield" in [tactical rules](2026-10-04-decompiled-tactical-battle-rules.md); `Rome  v  Gaul …` in [battle probe](2026-10-04-battle-probe.md) | The design-time caption against the runtime caption | Both stated in the tactical report |

**Also corrected:** the [rules specification](../rules-specification.md) said "a fleet has 0
moves on its launch turn". That holds only for a fresh table index: atlas increment 6 (Wine)
shows that a launched fleet keeps the leftover moves of a reused index.

## Still unobserved (from the manual's list; research agrees, nothing added here)

- the Offer of peace seen from a human's loss;
- the "attack this army ?" prompt;
- the AI declaring war on a human;
- reparations "sues" seen from a human seat;
- the 250 BC and victory endings;
- New nation / New player after Yes;
- the Yes effects of disband (P01) and scuttle (P02);
- the winter storm spike to 30;
- foreign supply purchase.

## Limits

- **Two reports only:** items were settled against research's reports and the decompilation.
  The manual's own text was not reviewed.
- **No game was run:** item 12 stays open.
- **Ctrl+P pixels:** pixel identity for item 8 is not checked.
- **Visible area:** the exact window sizes behind 13×13 and 13×12 are not reconstructed.
