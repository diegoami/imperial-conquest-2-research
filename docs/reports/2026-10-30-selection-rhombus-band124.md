# The selection rhombus (image 12): black exactly when 14 ≤ |x − 15.5| + |y − 15.5| ≤ 17

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `a6878fb` (PR #266). It
answers research issue [#124](https://github.com/diegoami/imperial-conquest-2-research/issues/124)
(for imperial_conquest_2 T242/#1010), delegated to conquest on 2026-10-29.
- **Script:** `runs/experiments/selection1010/band_rule.py`.
- **Data:** `runs/experiments/data/run-exp-selection1010/band-rule-v1.json`, with the counts, the
  unique match and the per-row runs.

No image is reproduced here or in the draft.

**Tag:** `[confirmed]`, read from the pinned EXE's TUnitMap form resource (the TerrainList bitmap,
image 12). It extends
[`2026-10-30-unit-map-selection-drawing1010.md`](2026-10-30-unit-map-selection-drawing1010.md).

**Review note (2026-10-29):**
- **Rerun:** I ran `band_rule.py` through a wrapper that redirects only its output. It decodes
  image 12 from the EXE resource. The result is identical to `band-rule-v1.json`: 240 black, and
  the only match is centre (15.5, 15.5) with band 14..17.
- **The formula on its own:** computing it independently gives exactly 240 black and 784 white
  pixels, with the row runs listed below.
- **The main project's two candidates,** both centred on (16,16), each give 238 pixels:
  - band 14..17: 56 pixels differ from the image in total;
  - band 15..18: 112 pixels differ.

  The draft's "29 wrong" and "57 wrong" count one side of each difference.

## Answer

With x, y = 0…31, a pixel of image 12 is **black exactly when 14 ≤ |x − 15.5| + |y − 15.5| ≤ 17**.
- The centre is the pixel corner (15.5, 15.5), so the distances are whole numbers from 1 to 31, and
  the band is 14, 15, 16 and 17.
- This gives 240 black and 784 white pixels, with none missing and none extra.
- It is the **only** match among centres 15, 15.5, 16 and 16.5 on each axis and every band within
  10..23.

**Row runs** (inclusive x ranges; rows mirror, y ↔ 31 − y):

| Rows | Black x |
|---|---|
| 0 and 31 | 14–17 |
| 1 and 30 | 13–18 |
| 2 and 29 | 12–19 |
| y = 3…14 (and 31 − y) | (14 − y)…(17 − y), and (14 + y)…(17 + y) |
| 15 and 16 | 0–2, and 29–31 |

The line is 4 px wide, except in rows 15 and 16, where it meets the tile edge and is 3 px.

## What this does not establish

- Rendering on native Windows: the palette and display.
- Other images in the list.
