# Pending research requests

Requests from other sessions that are accepted but not done. Whoever picks one up (any session)
removes it here when its report is promoted, and tells the requester.

## Desktop palette check (with the player, via ic2-conquest)

Asked by the research session on 2026-10-09 (the user asked). Every marker-colour result so far is
Wine-only: [`2026-10-09-owner-colours-by-band.md`](reports/2026-10-09-owner-colours-by-band.md),
[`2026-10-09-city-marker-colours.md`](reports/2026-10-09-city-marker-colours.md) and
[`2026-10-09-unit-icon-recolour-and-nation-glyphs.md`](reports/2026-10-09-unit-icon-recolour-and-nation-glyphs.md).

**Steps** (ic2-conquest `runs/experiments/data/run-exp-desktop-palette/STEPS.md`): on the Windows
original, load `colours_PRE.SAV` (`run-exp-owner-colours`) and `cities_PRE.SAV`
(`run-exp-city-marker-colours`). Use the same view, take a screenshot of the map and of the
toolbar's nation buttons, and note the display's colour depth.

**Also asked:** where the 2026-09-29 strip of
[`2026-09-29-nation-marker-colours.md`](reports/2026-09-29-nation-marker-colours.md) was cropped
from (toolbar, raw glyph bitmaps, or map), and on which system. The current reading, that it
came from raw glyphs with the white transparent margin visible, is `[derived]`.

**Expected:** the glyphs and image lists carry their own palettes, so the desktop should draw the
same 16 colours. Numidia's grey unit fill is in the code's colour table, so it should be grey
on the desktop too.

**Done when:** a desktop draft is promoted, or the player declines. Remove this entry then.
