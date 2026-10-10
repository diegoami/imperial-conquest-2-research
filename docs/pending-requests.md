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

## Money and supplies of a fleet emptied by Transfer ships (via ic2-conquest)

Asked by the research session on 2026-10-10 (the user asked). The draft's claim that the other
fleet takes them was corrected in
[`2026-10-09-supply-providers-and-transfer-clamps.md`](reports/2026-10-09-supply-providers-and-transfer-clamps.md)
(`cf7a6c1`): every played fleet held 0 of both, and `FUN_0044ad38` does not move them
([`decompiled-elimination-cleanup.md`](reports/decompiled-elimination-cleanup.md) §2). Open: does
the TFleetToFleet OK handler (`0x443b48`) pass them on first, or are they lost?

**Method:** like Tc1/Tc2 (`fleet-split-antium-0734.SAV`), with the fleet to be emptied staged to
distinct supplies (`+14`) and money (`+16`), and the receiver to other distinct values. Empty it
with the ship arrows only, then OK. One case where the receiver has room for the supplies
(capacity `8 × ships`) and one where it doesn't. Optional: the code of `0x443b48`.

**Taken** 2026-10-10 by ic2-conquest as `run-exp-fleet-empty-transfer` (branch
`experiment/fleet-empty-transfer`): Td1, Td2, and Td0 (a partial transfer with the Td1 values, as a control).

**Done when:** a draft is promoted, or the peer reports it can't be done. Remove this entry then.
