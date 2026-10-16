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

## Tactical target/draw divergences (research #25)

The original-side #24 predicate/timing evidence is promoted in
[2026-10-16-computer-general-predicate-and-reload.md](reports/2026-10-16-computer-general-predicate-and-reload.md).
The build's independently reviewed general-control correction must be integrated,
alongside build #1103 (`6d2d2fee`) and #1105 (`269a826c`), before a valid comparison.
Research intake is not that correction. Build #1104 was still open at intake.

The ic2-conquest `caf2a17` inventory audit (no comparison run) reproduces the
historical issue-1107 subset as 57 cases / 41 diagnostic series (T129 `9664936e`);
the recorded current subset is 63 / 48, registry blob `c0402c89`. Eight case IDs
were newly linked and two no longer linked. The old 42-series survey ID list is
missing; its unmatched series has not been identified or declared fixed.

After the prerequisites, begin with `mix-rg_s1` BATTLE06, Gaul slots 22/23:
reported first mismatch draw 24, half-round 6, site `0x439557`, original range
1085 versus port 172. Pin the comparison revision and preserve immutable draws,
fixtures and all first divergences. Attribute each cluster by original target
claims, pass/slot order, ties and flank rules; no range rebaseline or combined
emulation as proof. Return a reviewed findings draft through intake.

**Done when:** the gated comparison has an attributed, sourced report promoted,
with unexplained cases kept open. Full scope: research issue #25 / build #1107.
