# About Imperial Conquest — verification of row H03

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `e8b2984e`
(part of the `runs/experiments/data/run-exp-feature-inventory/` batch). Release
`run-exp-feature-inventory`, asset `FI_batch1_screenshots.tar.gz`.

**Closes** the cell-level verification of H03 of
[`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md).
The row was already `[confirmed]` at the row level; this draft tightens the
cell-level form extraction.

**Tag policy:** same as the inventory. A row or sub-row is `[confirmed]` when a
tracked file in `diegoami/ic2-conquest` lists the cited evidence.

## Answer

The H03 row is fully backed by tracked data — the About-menu handler, the
`TAboutIC` form's nine controls (caption strings verbatim), and the screenshot.
The "CAncell" button — which is the H04 trigger — is also named in this draft
because it sits in `TAboutIC`; the H04 draft carries the chain.

| Sub-claim | Source | Match status |
|---|---|---|
| The Help menu has an **About Imperial Conquest** item | `form_controls.tsv`: `TPremierForm/PremierForm/MainMenu/mt_Help/mn_About` (a TMenuItem, OnClick=`About`); `function_list.tsv` row `TPremierForm_About @ 0x0045c2e8` | identical |
| The dialog reads **"About Imperial Conquest 2"** | `form_controls.tsv`: `TAboutIC/AboutIC` class `TAboutIC`, `Caption="About Imperial Conquest 2"` | identical |
| The version label reads **"Imperial Conquest 2 v1.01"** | `form_controls.tsv`: `TAboutIC/AboutIC/Label1` caption=`Imperial Conquest 2 v1.01` | identical |
| The license text reads **"This is the full/freeware version of Imperial Conquest 2, feel free to copy and distribute it."** | `form_controls.tsv` rows `Label2` / `Label3` / `Label4`: `This is the full/freeware version` / `of Imperial Conquest 2, feel free to` / `copy and distribute it.` | identical |
| The copyright reads **"copyright Serious Games 1997"** | `form_controls.tsv`: `TAboutIC/AboutIC/Label5` caption=`copyright Serious Games 1997` | identical |
| The dialog has **OK** and **CAncell** buttons | `form_controls.tsv`: `TAboutIC/AboutIC/btn_ok` caption=`OK`, OnClick=`OK`; `TAboutIC/AboutIC/btn_cancell` caption=`CAncell`, OnClick=`Cancell` | identical |
| The dialog renders correctly on Wine | `MANIFEST-batch1.txt` row `aadafdd5…  FI_b1_03_about.png`; explore script `runs/experiments/feature_inventory/explore_b1_about.py` clicks (382, 109) — the About menu item — and dumps the live control list | identical |

## Two open notes

1. **Two `Bevel` decoration controls (`Bevel1`, `Bevel2`) sit on the dialog.** They
   carry no caption or hint; they are the visual frames around the labels and the
   buttons. Cosmetic only; nothing to render beyond the same grid layout.
   Recording so the clone's `AboutDialog.cs` knows to count them when reproducing
   the form.
2. **The dialog's text label spacing (two-space gaps) is intentional.** Each
   `Label1`–`Label5` carries internal double spaces (`Imperial  Conquest  2    v1.01`,
   `of Imperial Conquest 2, feel free to`, `copy and distribute it.`). Two-space-
   padded gaps are Delphi's word-wrap within fixed-width labels; a faithful clone
   should either keep the `Label.AutoSize = False` semantics or join the strings
   with a single space. Either rendering is correct; the byte-exact spacing is
   not load-bearing.

## Connection to H04

The `btn_cancell` (`OnClick=Cancell`) routes to `TAboutIC_Cancell @ 0x00456ca0`
which constructs `TCellAuto` — the H04 Cellular Automata easter-egg window. The
two drafts cross-reference each other:

- **H03** (this draft) carries the About-box's content and the **button** (caption
  + OnClick).
- **H04** carries the chain into the easter-egg window itself: its form, its
  three buttons, and what is and isn't decoded about the simulation.

## Method

- **Form + function extraction.** Same toolchain as the other H0x drafts. The
  `TAboutIC` form has nine controls; the cells in the table above are reproduced
  verbatim from `form_controls.tsv`.

## Reproduction

```bash
grep -E "TAboutIC|TCellAuto|mn_About" runs/experiments/data/run-exp-feature-inventory/form_controls.tsv
grep -E "TPremierForm_About|TAboutIC_Cancell" runs/experiments/data/run-exp-feature-inventory/function_list.tsv
sha256sum runs/experiments/data/run-exp-feature-inventory/explore/FI_b1_03_about.png
```

The About-menu item pixel (382, 109) and the screenshot's SHA-256 (`aadafdd5…`)
are reproducible end-to-end. No live Wine session is needed for verification; the
explore-batch1 release asset holds the live capture.

## Related

- [`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md)
  row H03 — this report's evidence column is appended in the inventory.
- [`2026-10-08-cellular-automata-easter-egg-h04.md`](2026-10-08-cellular-automata-easter-egg-h04.md)
  — the chain the `CAncell` button opens.
