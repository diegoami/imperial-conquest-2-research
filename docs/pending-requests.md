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

The prerequisite gate is now cleared at reviewed build PR #1156, merge
`257f2d2cd7510451d229a983553a54b89065b06c`, including the control correction
alongside #1103/#1105. The 318-hook comparison and recovered historical inventory
are promoted as [confirmed, partial](reports/2026-10-16-tactical-target-and-draw-attribution.md).

At that pin: 282 complete exact, 36 residual; 283 exact draw sequences. The old
42-series recovered working survey contains the historical 57-case/41-series
registry set plus `hi-ar-three_s3_r5_hook`; later 63/48 and post-T175 90 target/draw
registry entries are different snapshots/counting units, not residual series counts.

**Still open:** every one of the 36 residual whole-path causes. Nineteen series
have a reproduced local rule discrepancy on a model phase input, seventeen have
none in the evaluated probes. Original runtime claims and the general pass of
original shots are not in legacy logs/SAVs; these gaps cannot be filled by local
x86 execution on model state. Retain the state-only `ar-hi-three_s3` residual.

The requested `mix-rg_s1` starting case is now pinned: draw 24, HR6, site
`0x439557`, original Gaul23 -> Rome2 `Random(1085)=357`, model Gaul22 -> Rome1
`Random(172)=56`. The changed actor/target pair prevents treating it as a simple
range correction. Local threat aim/order differs, but complete causality is not proved.

**Next:** evaluate the accepted local source rules in bounded build-side correction
contracts, then rerun unchanged full comparisons and identify exactly which residual
paths disappear. Additional original runtime observations may be needed for the
missing claims/pass state and 24 stopped-before-shot Pass2 stages. Preserve original
fixtures/draw bounds and strict comparison behavior. No new expected-failure entry,
fixture repair or gameplay patch is authorized by this research report.

**Done when:** a reviewed report establishes the surviving complete causal paths.
Partial rule findings remain evidence for build evaluation; unexplained cases and
research #25 / build #1107 stay open until that attribution is established.
