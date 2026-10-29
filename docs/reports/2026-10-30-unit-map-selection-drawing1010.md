# Unit-map selection drawing: an SRCERASE rhombus over any selected cell, with no timer

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `edc13ea` (PR #255). It
answers imperial_conquest_2 [#1010](https://github.com/diegoami/imperial_conquest_2/issues/1010),
delegated to conquest on 2026-10-29.
- **Scripts:** `runs/experiments/selection1010/{capture.py, recheck.py}`.
- **Data:** `runs/experiments/data/run-exp-selection1010/` (`captures-v1.json` with the origin off
  by 1 px, kept as measured; `recheck-v2.json`; `SAVES.sha256`).

**Tag:** `[confirmed]` (decompile plus five controlled Wine captures). Release
[`run-exp-selection1010`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-selection1010)
holds the 20 screenshots; all 20 assets match `SAVES.sha256` by name and hash (checked 2026-10-29).
*(First promoted provisional, before the release existed.)*

**Review note (2026-10-29):**
- **Captures:** all **20** local capture files match `SAVES.sha256`. *(Corrected 2026-10-29: the
  first index listed each file twice, once with an `artifacts/run-exp-selection1010/` prefix and
  once bare, which this note first counted as 40 files. Since conquest PR #257 the index holds the
  20 bare-name lines, and `sha256sum -c` from the artifacts folder gives 20/20 OK.)*
- **Recheck rerun:** I ran `recheck.py` through a wrapper that redirects only its output; it reads
  the kept screenshots. The result equals `recheck-v2.json` exactly. All five cases match the
  per-pixel model on **1,024 of 1,024** pixels at all three times.
- **Decompile re-read.**
  - `FUN_004465a8` (:46433) checks that the selected cell (`+0x21a`/`+0x21c`) is inside the
    view, then draws image **12** (`0xc`) of the form's image list (`+0x1b0`), with the canvas
    `CopyMode` set to `0x00440328` (SRCERASE).
  - `TUnitMap_SelectUnit` calls it **before** its type branches, so a town, an army or a fleet,
    own or foreign, all get the frame.
- **This corrects** the open points of
  [`2026-10-12-unit-map-selection-rendering.md`](2026-10-12-unit-map-selection-rendering.md):
  - its "yellow rhombus" is the **inverted tile** around a **black** line;
  - the marker itself **is** recoloured (inverted);
  - there is **no** game timer and no blink;
  - October's "town" capture clicked (101,47), which is not a town.

  A one-line note links that report here.

## Answer

- **What draws it.** `TUnitMap_SelectUnit` calls the nested `FUN_004465a8` for **any** selected
  cell: town, army or fleet, own or foreign. If the cell is in view, it draws TerrainList
  **image 12** with `CopyMode = SRCERASE` (`0x00440328`), then restores SRCCOPY.
- **Image 12** (exact pixel rule: [2026-10-30-selection-rhombus-band124.md](2026-10-30-selection-rhombus-band124.md)) comes from the TUnitMap form resource, which holds 13 images with an opaque mask. It
  is a **black rhombus outline**: corners at the edge midpoints, 3–4 px thick, 240 black and 784
  white pixels.
- **What appears on screen:** where the image is white, the tile is **inverted**, so sea turns
  yellow and the marker is inverted too. On the line itself, it is **black**.
- **No game timer.** The only `SetTimer` is VCL's hint timer, so nothing blinks.
- **One tile size,** 32 px.
- **The five captures** (army, fleet, town, capital, foreign town) match the per-pixel model on
  1,024 of 1,024 pixels and are stable at 0.4 s, 1.4 s and 2.9 s. October's army capture matches
  too.

## What this does not establish

- Native Windows palettized rendering.
- Keyboard selection.
- The area-map cursor.
