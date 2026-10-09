# Cellular Automata (hidden easter-egg) — verification of row H04

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `e8b2984e`
(part of the `runs/experiments/data/run-exp-feature-inventory/` batch). Release
`run-exp-feature-inventory`, asset `FI_batch1_screenshots.tar.gz`.

**Closes** the cell-level verification of H04 of
[`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md).
The row was already `[confirmed]` at the row level (the live Wine screenshot
proves the window exists); this draft tightens the cell-level form/handler
extraction. The reproduction decision (whether to render the easter egg at all)
is the question on clone-side issue #722, not data.

**Tag policy:** same as the inventory. A row or sub-row is `[confirmed]` when a
tracked file in `diegoami/ic2-conquest` lists the cited evidence.

## Answer

The H04 row is fully explainable from this repo's tracked forms and function-
list extracts plus the two screenshots. Every byte the original draws is named in
tracked files; nothing here would prevent a faithful reproduction if the owner
chooses to render it.

| Sub-claim | Source | Match status |
|---|---|---|
| The About box's button reads **"CAncell"** (deliberate misspelling) | `runs/experiments/data/run-exp-feature-inventory/form_controls.tsv` row `TAboutIC/AboutIC/btn_cancell` — `name=btn_cancell`, `caption=CAncell`, `OnClick=Cancell` | identical |
| Clicking that button creates the **Cellular Automata** window | `function_list.tsv` row `TAboutIC_Cancell @ 0x00456ca0` (which the decompile shows constructs `TCellAuto`); form `TCellAuto` `caption=Cellular Automata`, `OnCreate=InitializeForm` | identical |
| The window has buttons **N (New structure)**, a **save icon (Save structure as .BMP)** and **X (Close)** | `form_controls.tsv` rows under `TCellAuto/CellAuto/Panel1/`: `sb_next` (caption `N`, hint `New structure`, OnClick=`TCellAuto_NewPattern`); `sb_Save` (no caption, hint `Save structure as .BMP`, OnClick=`TCellAuto_SaveBMP`); `sb_OK` (caption `X`, hint `Close Cellular Automata`, OnClick=`TCellAuto_OK`) | identical (every caption, hint and handler matches the row's prose) |
| The handler chain | `function_list.tsv`: `TCellAuto_InitializeForm @ 0x00456668`, `TCellAuto_NewPattern @ 0x00456744`, `TCellAuto_SaveBMP @ 0x004569c0`, `TCellAuto_OK @ 0x00456a70`, `TAboutIC_Cancell @ 0x00456ca0` | identical |
| The window actually shows a pattern after N | Wine screenshot `FI_b1_05_cellauto_N.png` (release asset `FI_batch1_screenshots.tar.gz`, hashed in `SAVES.sha256`); explore script `runs/experiments/feature_inventory/explore_b1_ca.py` clicks (509, 341) — the N button — and takes the screenshot. | identical |
| The X button closes the window | `explore_b1_ca.py` clicks (776, 341) — the X button — and snapshots `Cellular Automata` no longer in the window list; `explore_b1_ca2.py` repeats this three times, then closes the About box. | identical |
| The non-gameplay call | Clone's `imperial_conquest_2/docs/design-audit.md` line 19: "*Two whole classes turned out to be non-gameplay (`TCellAuto` is a cellular-automaton toy with a `SaveBMP` button …); `TBattleDelays` is a settings dialog for the tactical pacing pauses …)*" | identical |

## Three open items

1. **The CA rule set itself is not decoded.** The form has an `Image1` (the
   canvas) and a `Panel1` with the three buttons. The simulation's *content* is
   computed by `TCellAuto_InitializeForm` and `TCellAuto_NewPattern`, both at
   decompile addresses but neither rule listed in tracked data. A faithful
   reproduction needs the rule (Conway Game-of-Life? a Wolfram 1D rule? an
   L-system?). The clone can render the *form* from the controls above; the
   *content* of the canvas is the open piece.
   **Partly answered (2026-10-09):** a loop inside `TCellAuto_NewPattern` (0x456940-0x456985) is a
   **one-dimensional totalistic automaton**. It copies a 301-cell row of words (`+0x1D2` → `+0x42E`,
   with a cell of padding on each side), then gives each cell the rule-table entry at `+0x688`
   indexed by the sum of its left, centre and right neighbours. The table's contents, the cell
   states and how rows are drawn are not read `[derived]` from the excerpt
   `word_array_456940.asm` (ic2-conquest `b2abac3`, `run-exp-battle-numidia-colour`), noted in
   [`2026-10-09-battle-map-units-use-the-nation-recolour.md`](2026-10-09-battle-map-units-use-the-nation-recolour.md).
   **Answered since:** a random 4-state totalistic rule (`T[0..9] = Random(4)` at every N), 300 cells,
   seed 144-155 = 1, 400 generations; colours white/red/blue/green. One N press is reproduced pixel
   for pixel in Wine: [`2026-10-09-cellular-automata-rule-h04.md`](2026-10-09-cellular-automata-rule-h04.md).
2. **The SaveBMP format is unspecified.** `TCellAuto_SaveBMP @ 0x004569c0` writes
   a `*.BMP` file. The size of the bitmap (the Image1 width × height), the palette
   (16-colour VGA? 256-colour?), and the cell-to-pixel mapping are not in this
   repo's tracked data; a faithful clone would need to read `SaveBMP` byte-exact
   or pick a simple default (e.g. 1 bit per cell, 1 byte per pixel = `BMP` mode).
   **Mostly answered since:** the file is `ca` + the 10 rule digits + `.BMP` in the current directory,
   and holds `Image1`'s 300 × 400 bitmap, which is never cleared. Its pixel format was open at that point: [`2026-10-09-cellular-automata-rule-h04.md`](2026-10-09-cellular-automata-rule-h04.md).
   **Answered since:** a 24-bit bottom-up BMP under Wine, made at the first N, white at first, then carrying over between patterns; the depth on a desktop is open: [`2026-10-09-cellular-automata-savebmp-format.md`](2026-10-09-cellular-automata-savebmp-format.md).
3. **The About-box layout has two buttons (`OK` and `CAncell`); the clone's
   `godot/UI/AboutDialog.cs:43–52` has only `OK`.** The reproduction question is
   whether the second button should exist at all. If yes: the misspelling must be
   **preserved** (`CAncell`, capital A, capital C, lowercase rest) to keep the
   easter-egg discoverable; if no: omit the control, leaving the OK-only dialogue
   as the clone's current shape.

## Method

- **Form extraction.** `runs/experiments/feature_inventory/extract_forms.py`
  parses every `TPF0` resource of `Imperial Conquest 2.exe`; outputs
  `runs/experiments/data/run-exp-feature-inventory/forms.json` (29 forms) and
  `form_controls.tsv` (908 controls, with caption / hint / event handler / Delphi
  `ShortCut` columns). The two relevant form rows here — `TCellAuto` with five
  controls and `TAboutIC` with nine — are reproduced verbatim from
  `form_controls.tsv`.
- **Function symbols.** `runs/experiments/feature_inventory/extract_dump_strings.py`
  and the EXE's Delphi RTTI produce `function_list.tsv` (with `addr`, `name`,
  `symbol`, `dump_line` columns) and `dump_string_literals.tsv`. The five
  function rows cited are reproduced verbatim.

## Reproduction

```bash
python3 runs/experiments/feature_inventory/extract_forms.py    # regenerate form_controls.tsv
grep -E "TAboutIC|TCellAuto" runs/experiments/data/run-exp-feature-inventory/form_controls.tsv
grep -E "TAboutIC_Cancell|TCellAuto_" runs/experiments/data/run-exp-feature-inventory/function_list.tsv
```

The form and function extracts are deterministic — they read the EXE and DAT,
neither of which changes. No live Wine session is needed for verification; the
explore scripts in batch 1 of `run-exp-feature-inventory` (release asset
`FI_batch1_screenshots.tar.gz`) hold the live screenshots.

## Related

- [`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md)
  row H04 — this report's evidence column is appended in the inventory.
- [`2026-10-08-about-imperial-conquest-h03.md`](2026-10-08-about-imperial-conquest-h03.md)
  — the H03 form whose `CAncell` button opens this window.
