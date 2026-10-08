# Map mouse actions — verification of rows MM01–MM10

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `e8b2984e`
(part of the `runs/experiments/data/run-exp-feature-inventory/` batch). The MM
rows all hinge on `TUnitMap_SelectUnit @ 0x004466cc` plus a small set of adjacent
handlers; this report consolidates the cell-level verification into one
document because a per-row draft would repeat the same evidence five times.

**Closes** the cell-level verification of MM01–MM10 of
[`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md).
The rows were already `[confirmed]` / `[derived]` at the row level; this report
tightens the cell-level extraction.

**Tag policy:** same as the inventory. A row or sub-row is `[confirmed]` when a
tracked file in `diegoami/ic2-conquest` lists the cited evidence; `[derived]`
when only a code reference is given.

## Answer

| Row | Claim (verbatim from inventory) | Cell-level source | Match |
|---|---|---|---|
| MM01 | A left click on the marker selects it (an army needs moves left) and shows the strip of buttons for it; it stays selected while it has moves and is dropped at 0 moves. | `function_list.tsv`: `TUnitMap_SelectUnit @ 0x004466cc` (markers `200..247` armies, `300..347` fleets per the inventory's `[derived]` note). Existing finding [`2026-10-02-unit-map-mouse-orders-and-tax-range.md`](2026-10-02-unit-map-mouse-orders-and-tax-range.md) (a)–(e) measures the same: selected army 0 → −1 at moves 0; `A_AFTER_CLICKS.SAV`. | identical |
| MM02 | A left click on an own city selects it and shows the city strip (Fortify city, Cancel selection) and its details panel. | `function_list.tsv`: `TUnitMap_CityButtonsOn @ 0x00446268`. Screen-shot `SS:FI_b1_24_city_left_click.png` (Rome city, fortification 78%, 14,000 conscripts, tribute 317, supply 990 tons). | identical |
| MM03 | With an army selected, a click on a reachable tile moves it at once; one click walks the whole route; a river tile costs 4 moves. | `function_list.tsv`: `TUnitMap_MoveHumanArmy @ 0x00446d9c`. `coverage.md` §1 row 15 ✅: `T_MOVE.SAV` army (100,37)→(101,36), moves 8→4 (river tile costs 4 — matches [`terrain-move-cost-table-in-dat.md`](terrain-move-cost-table-in-dat.md)). H:'Army move'. | identical |
| MM04 | With an army selected next to an enemy city, a click resolves a siege: at war no prompt, otherwise "Are you sure you want to attack this city ?". | `dump_string_literals.v2.tsv` row 258: `TUnitMap_SelectUnit 0x004466cc  literal="Are you sure you want to attack this city ?"`. `coverage.md` §1 row 16 ✅: `T_ATTACK.SAV` (Felsina, Gaul at war) army 23,700→21,765, Felsina loyalty 79→76, fort 68→65, pop 26→25. Existing finding `2026-10-02-unit-map-mouse-orders-and-tax-range.md` (b) measures the prompt (`B2_PEACE_GENUA_AFTER_NO.SAV`; Yes writes war + news "ROME DECLARES WAR ON GREECE."). | identical |
| MM05 | With an army selected next to an enemy army, a click asks "Are you sure you want to attack this army ?" and Yes declares war (relation 3, with the ally cascade) before the attack resolves, then opens the tactical battle. | `dump_string_literals.v2.tsv` row 259: `TUnitMap_SelectUnit 0x004466cc  literal="Are you sure you want to attack this army ?"`. `coverage.md` §1 row 17 🟡: battle-bar calibrated; [`2026-10-04-battle-probe.md`](2026-10-04-battle-probe.md) opens and ends the battle (`NB_post_battle.SAV`). The Yes-then-declares-war-and-tactical-screen flow is `[derived]` (code, not yet measured end-to-end against a save). | identical for the literal; `[derived]` for the war-cascade flow (carried from inventory) |
| MM06 | With a fleet selected next to an enemy fleet, a click asks "Are you sure you want to attack this fleet ?" when not at war, then resolves an instant naval battle (news "X sinks fleet of Y."). | `dump_string_literals.v2.tsv` row 261: `TUnitMap_SelectUnit 0x004466cc  literal="Are you sure you want to attack this fleet ?"`. Refusal row 262: `"You cannot attack a fleet docked at its own city !"`. `coverage.md` §1 row 'Fleet: attack' ✅ (`NB_P_seed1.SAV` etc.); the prompt itself ✅ in `PP_yes_seed1.SAV` (release `run-exp-peace-prompt`); [`2026-10-03-fleet-peace-prompt.md`](2026-10-03-fleet-peace-prompt.md). | identical |
| MM07 | With an army selected next to an own fleet, a click on the fleet loads the army; both lose their moves. | `dump_string_literals.v2.tsv` row 260: `TUnitMap_SelectUnit 0x004466cc  literal="The army is too large for this fleet ?"` (refusal). `coverage.md` §1 row 32 ✅: `T_EMBARK.SAV` (army 0 aboard: cell −1, fleet carries 0, both moves 0); refusal `T_EMBARK_REFUSED.SAV`. [`2026-10-02-fleet-orders-live.md`](2026-10-02-fleet-orders-live.md) for embark/unload. | identical |
| MM08 | With a loaded fleet selected on a sea tile next to land, a click on the land tile unloads the army. | `coverage.md` §1 row 32 ✅: `T_DISEMBARK.SAV` (release `run-exp-fleet-orders`); same row of `coverage.md`. | identical (covered by the same `2026-10-02-fleet-orders-live.md` source) |
| MM09 | With a fleet selected, a click on a sea tile moves it (auto path, or square by square); sea tiles cost 1 (calm) or 3 (rough). | `function_list.tsv`: `TUnitMap_MoveHumanFleet @ 0x00446e24`. `coverage.md` §1 row 32 ✅: `T_MOVE_FLEET.SAV`; H:'Fleet move'; R:[`terrain-move-cost-table-in-dat.md`](terrain-move-cost-table-in-dat.md) (codes 0=1, 1=3). | identical |
| MM10 | A left click on a foreign unit or city shows its details in the Information window without selecting it. | `function_list.tsv`: `TUnitMap_SelectUnit @ 0x004466cc` (single dispatcher handles every click). Existing finding `2026-10-02-unit-map-mouse-orders-and-tax-range.md` (Evidence (a)) measures the foreign-army case: a click on a foreign army only updates the Information panel. | identical |

**Single dispatcher, four message branches.** `TUnitMap_SelectUnit 0x004466cc`
is the only function the inventory cites for the click path, and
`dump_string_literals.v2.tsv` rows 258–262 are **all five literals in the same
function**: the three attack prompts (city / army / fleet), the embark refusal,
and the fleet-docked refusal. A faithful clone can reconstruct MM01–MM10 with
one function dispatch; the literals sit at the same addresses; the markers are
tile codes `200..247` (armies) and `300..347` (fleets) per the inventory's
`[derived]` note on MM01.

## Three open notes

1. **MM05's "Yes declares war then opens the battle" chain is `[derived]` in the
   inventory.** The literal `"Are you sure you want to attack this army ?"` is
   in `dump_string_literals.v2.tsv`, but the full chain — Yes writes relation 3
   with the ally cascade, then a `TBattleOver_OK` end-state — isn't measured
   end-to-end against one save. The closest measurement is
   `2026-10-04-battle-probe.md`'s `NB_post_battle.SAV` after a tactical battle,
   which covers the **resolution** side but not the **yes-write-war** side. A
   clone reproducing MM05 needs both: the prompt and the ally cascade. Recorded
   for the next pass.
2. **MM06's instant naval battle is `[confirmed]` in the inventory** but the
   inventory cites 50-battle trial saves, not the dialog. The dialog text is
   `dump_string_literals.v2.tsv` row 261; the resolution is
   `2026-10-03-fleet-peace-prompt.md`. The **Yes** branch of the fleet prompt is
   `PP_yes_seed1.SAV` (Yes declared war on the target and on its ally Numidia in
   the one case seen).
3. **The marker range `200..247 / 300..347` is `[derived]` (code only).**
   `coverage.md` doesn't carry the marker's tile-code range; the inventory's
   `[derived]` note on MM01 is the only cite. A faithful reproduction needs to
   read the dispatcher's `if/else if` chain against the marker code, not against
   the surrounding form/control dump. Not measured here; carrying from inventory.

## Method

- **Function + literal extraction.** `runs/experiments/feature_inventory/extract_dump_strings.py`
  reads the decompile dump and the EXE's Delphi RTTI; outputs `function_list.tsv`
  and `dump_string_literals.tsv` (the latter is `dump_string_literals.v2.tsv` after
  the 247/247 fix). The five function rows in the table are reproduced from
  `function_list.tsv`; the five literals are reproduced from
  `dump_string_literals.v2.tsv`.
- **Live evidence.** The pre-existing `coverage.md` ✅ rows, the
  `2026-10-02-*` finding pair, the `2026-10-03-fleet-peace-prompt.md` and
  `2026-10-04-battle-probe.md` saves; the test suite keeps the small
  `T_*.SAV` and `NB_post_battle.SAV` fixtures under `tests/saves/`.

## Reproduction

```bash
grep -E "TUnitMap_(SelectUnit|CityButtonsOn|MoveHumanArmy|MoveHumanFleet)" \
     runs/experiments/data/run-exp-feature-inventory/function_list.tsv
grep -nE "TUnitMap_SelectUnit.*Are you sure|The army is too large|cannot attack a fleet docked" \
     runs/experiments/data/run-exp-feature-inventory/dump_string_literals.v2.tsv
pytest -k orders                                              # keeps T_MOVE.SAV, T_ATTACK.SAV, T_EMBARK.SAV, T_DISEMBARK.SAV,
                                                              # T_MOVE_FLEET.SAV, T_JOIN_FLEETS.SAV under tests/saves/
```

The function + literals extracts are deterministic — they read the EXE and the
dump. Re-running the test suite is live (Wine session) and is the only step that
needs the game running; everything else is offline.

## Related

- [`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md)
  rows MM01–MM10 — this report's evidence column is appended in the inventory.
- [`2026-10-02-unit-map-mouse-orders-and-tax-range.md`](2026-10-02-unit-map-mouse-orders-and-tax-range.md)
  — the original cell-level measurement of clicks.
- [`terrain-move-cost-table-in-dat.md`](terrain-move-cost-table-in-dat.md) — the
  tile-cost table MM03 and MM09 cite.
- [`2026-10-07-ai-mover-contact.md`](2026-10-07-ai-mover-contact.md) — the
  non-MM (AI) twin: same contact resolver `FUN_0044d734` handles the AI's
  destination call (`FUN_0044dba8`), with the instant `FUN_0044aee4` path when
  both seats are computer.
