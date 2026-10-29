# Unit-map selection: army/fleet diamonds confirmed; blink and town claims withheld

**Update 2026-10-29:** the open points are resolved, and two readings corrected, in [2026-10-30-unit-map-selection-drawing1010.md](2026-10-30-unit-map-selection-drawing1010.md). The yellow is the inverted tile around a black SRCERASE rhombus, the marker is inverted too, there is no timer, and the earlier "town" capture was not a town.

**Status:** promoted `[confirmed, partial: published patched-Wine screenshots]` from ic2-conquest branch `run/unit-map-selection-rendering`, source `9da03bc625bfaf57c7eaec6c8a1029ff2ce699a9`. The original October12 draft's interpretation is corrected by this October26 intake. [Main #1010](https://github.com/diegoami/imperial_conquest_2/issues/1010) remains open; this report changes no implementation, release gate or acceptance status.

## Supported observations

The retained selected-army and selected-fleet screenshots visibly show a bright yellow rhombus surrounding their tile. At this captured zoom it fits approximately one tile; this is visual evidence, not an exact vector/offset specification. The screenshots have corresponding army/fleet information panels, and the retained metadata identifies selected army0/fleet2. There is no new Original game, Windows or deployed-remake GUI check.

The source describes fast-rollingsave-seed EXE under Wine10.0, one process per case and turn0734. This is **patched-Wine evidence**, not the stock-original controls in the later Research85 packet. The first failed screen-centre analysis and corrected source draft remain historical; neither interpretation is accepted without checking the actual images.

## What the frame differences actually measure

Research downloaded all16 published release assets and checked every unique file against `SAVES.sha256` and its published asset size. The manifest has32 records with repeated entries, not32 independent files. Selected/frame3 files agree. Independent ImageMagick comparisons give:

| Label | Selected versus frame2 changed pixels | Bounding rectangle |
| --- | ---: | --- |
| army |98|15×13 at (467,543)|
| fleet |98|15×13 at (467,543)|
| town |98|15×13 at (470,543)|

These rectangles lie in the unit map's **horizontal scrollbar area**, away from the army/fleet selection tiles. Comparing the32×32 army/fleet tile regions gives **zero changed pixels**. Thus the source's98pixel differences do not show the rhombus toggling and cannot establish a600ms blink period or300ms on/off timer. The nominal capture interval alone cannot identify a period. The source's suggested300ms implementation timer is **not promoted**.

The town-labelled selected screenshot does not independently demonstrate the claimed town rhombus or city-information panel; it shows news. Its generic selected-index field is−1 and does not prove a successful town-selection stimulus. This is an unresolved capture/interpretation boundary, **not** a claim that the original cannot select towns or never draws their frame. Town shape/colour/timing remain open.

## Provenance and limits

[Source draft](https://github.com/diegoami/ic2-conquest/blob/9da03bc625bfaf57c7eaec6c8a1029ff2ce699a9/findings/2026-10-12-unit-map-selection-rendering.md), [metadata/runner](https://github.com/diegoami/ic2-conquest/blob/9da03bc625bfaf57c7eaec6c8a1029ff2ce699a9/runs/experiments/data/run-exp-unit-map-selection/), release [run-exp-unit-map-selection](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-unit-map-selection). Representative assets are `sel_20261012-203220_army_selected.png`, `sel_20261012-203220_fleet_selected.png` and their `_frame2.png`/`_frame3.png` partners. The town-labelled file is `sel_20261012-203220_town_selected.png`. No raw images or SAVs are copied into research Git.

The [safe verification receipt](../data/findings-queue-reconciliation-v1.json) records counts and pixel bounds. Research visually inspected the three selected images and computed differences without modifying them. It does not establish independent marker recolouring, exact vector dimensions, blink timing, town behaviour, every zoom or native Windows. Main's accepted T196 clear army/fleet-feedback milestone (PR1255) is separate; the draft's old MapViewer circle comparison is historical and must not be presented as the current shipped implementation. Do not close #1010 from this partial evidence.

Further source/capture interpretation is required for town selection and timing before an original-fidelity implementation contract uses them. No new live experiment is authorized or launched by this intake. The source peer was notified of the scrollbar attribution and acknowledged the correction; source changes remain that session's responsibility.
