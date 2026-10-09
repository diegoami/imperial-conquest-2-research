# Every owner's army and fleet icons: one background colour per owner, the same three band shapes for all; 96 distinct icons

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `7f2e337`; run data
at `91cd1e8`. Release
[`run-exp-owner-colours`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-owner-colours)
holds `colours_PRE.SAV`, `colours_AFTER.SAV`, `colours_screen.png` and the montages, and their
SHA-256s are committed at `runs/experiments/data/run-exp-owner-colours/SAVES.sha256`. Wine-only
evidence. It closes "other owners' colours by band", left open by
[`2026-10-08-army-icon-follows-the-size-band.md`](2026-10-08-army-icon-follows-the-size-band.md)
and [`2026-10-08-fleet-marker-band-and-icon.md`](2026-10-08-fleet-marker-band-and-icon.md).

**Review note:**
- I downloaded the two saves, the screenshot and the three montages and checked them against
  `SAVES.sha256` (6 OK). Every patched tile in `colours_PRE.SAV` holds the word `probe_colours.json`
  gives (108 of 108).
- I re-cropped all 108 tiles from `colours_screen.png` with my own script, using the driver's
  paint box (`UNIT_PAINT = (337, 96)`, tile (ox+c, oy+r) at x 337+32c, y 126+32r) and a 2 px
  inset. The draft reproduces: **96 distinct icons**, 16 per (kind, band); each of the 12 repeats
  is pixel-identical to its first copy; and the most frequent colour of each inset is one
  background per owner across its six icons, **14 distinct** for 16 owners (Carthage/Media red,
  Ptolemaic/Illyria navy).
- **Agreement with the city markers.** All 16 backgrounds, and both shared pairs, are the ones
  [`2026-09-29-nation-marker-colours.md`](2026-09-29-nation-marker-colours.md) read from the
  city icons. The two figure colours agree with that report's (outline, foreground) pair for 11
  owners. They differ for 5 (Macedonia, Numidia, Gaul, Illyria, Media; Macedonia only by swapping
  the two). Either the unit icons are separate bitmaps with their own figure colours, or the
  2026-09-29 reading (a user-supplied strip, snapped to the palette) is off for those nations.
  This run cannot tell which, and the city icons were not drawn here. The table below lists both. **Since drawn** ([`2026-10-09-city-marker-colours.md`](2026-10-09-city-marker-colours.md)): the cities share the unit icons' (A, B) for 15 owners, with A as the outline role. Numidia's city fill is teal, so its grey is a unit-icon difference. **Explained:** the unit icons are Rome-coloured templates recoloured from nation fields `+0x424/+0x428/+0x42C`, which new-game setup fills with grey for Numidia: [`2026-10-09-unit-icon-recolour-and-nation-glyphs.md`](2026-10-09-unit-icon-recolour-and-nation-glyphs.md). The other four remain differences between the strip and Wine.
- **Table corrected** (see the note under it): the draft ordered the two figure colours by
  frequency, which flips between icons. They are now listed by fixed pixel role.

**Tag:** `[confirmed]` for the drawing of each stored word (Wine, patched map words). The colour
roles and the comparison with the city markers are from my own reading of the same screenshot.

## Answer

- **All 96 words draw distinct icons:** army 200/216/232 + owner and fleet 300/316/332 + owner, for owners 0-15. Each (kind, band) has 16 different icons, one per owner (hashes over the 28×28 inset).
- **Shape is set by the band, colour by the owner.** Every owner gets the same three soldiers (small, medium, large with mace) and the same three ships (small, medium, large), drawn in its own colours (`montage_army.png`, `montage_fleet.png`: one row per owner, one column per band).
- **One background colour per owner,** the same in all six of its icons. 14 backgrounds for 16 owners:
  - Carthage (1) and Media (14) share red;
  - Ptolemaic (3) and Illyria (9) share navy;
  - the figure colours of each pair differ (table).
- **The terrain under the icon does not show.** The icon is opaque: four repeats of 200 (Rome army), 238 (Gaul army) and 333 (Carthage fleet) on other tiles, over the map words 0, 2 and 36, are pixel-identical inside a 2 px border. Only the dotted tile edges differ, which follow the neighbouring tiles.
- **Control:** Rome army 1's own tile (120,53), word 200, left unpatched, matches the earlier Rome 200 icon of `run-exp-army-marker-icon` pixel for pixel inside the border (`e6129bbc48e5e3ee` for both). The earlier full-tile hashes differ only by the dotted edges, and by the earlier hash being taken on 16-bit RGB.

| Owner | Nation | Background | Colour A | Colour B | City marker (outline, foreground), `2026-09-29-nation-marker-colours.md` | A, B against it |
|---:|---|---|---|---|---|---|
| 0 | Rome | `#800080` purple | `#ffffff` white | `#0000ff` blue | white, blue | match |
| 1 | Carthage | `#ff0000` red | `#000000` black | `#ffffff` white | black, white | match |
| 2 | Seleucid | `#808000` olive | `#ffffff` white | `#800000` maroon | white, maroon | match |
| 3 | Ptolemaic | `#000080` navy | `#ffffff` white | `#ff00ff` magenta | white, magenta | match |
| 4 | Macedonia | `#ffffff` white | `#0000ff` blue | `#808080` grey | grey, blue | the two swapped |
| 5 | Numidia | `#00ff00` lime | `#000000` black | `#808080` grey | black, teal | B differs (grey vs teal) |
| 6 | Gaul | `#800000` maroon | `#00ffff` cyan | `#808080` grey | white, cyan | differs |
| 7 | Greece | `#00ffff` cyan | `#000000` black | `#ff00ff` magenta | black, magenta | match |
| 8 | Celtiberia | `#ffff00` yellow | `#000000` black | `#ff0000` red | black, red | match |
| 9 | Illyria | `#000080` navy | `#808000` olive | `#00ffff` cyan | white, olive | differs |
| 10 | Dacia | `#008000` green | `#000000` black | `#ffff00` yellow | black, yellow | match |
| 11 | Bithynia | `#008080` teal | `#000000` black | `#0000ff` blue | black, blue | match |
| 12 | Galatia | `#0000ff` blue | `#000000` black | `#00ffff` cyan | black, cyan | match |
| 13 | Armenia | `#ff00ff` magenta | `#000000` black | `#ff0000` red | black, red | match |
| 14 | Media | `#ff0000` red | `#c0c0c0` silver | `#800080` purple | white, purple | A differs (silver vs white) |
| 15 | Thracia | `#808080` grey | `#ffffff` white | `#000000` black | white, black | match |

*Table rebuilt on promotion (see the review note).* Every icon uses exactly three colours, on the same pixels for every owner: the background, colour A and colour B. Summed over an owner's six icons, they cover 3,357, 740 and 607 pixels of the 28×28 insets, for every owner. Which of A and B is more frequent depends on the icon (Rome: white leads in the army icons and the small fleet, blue in the medium and large fleets). So the draft's frequency order of the "next two colours" was not a fixed role, and six rows (Rome, Seleucid, Ptolemaic, Illyria, Media, Thracia) listed them the other way round. The set of colours per owner is the draft's.

## Method

- **Save:** `artifacts/run-exp-army-marker-band/t24999_AFTER.SAV` (Rome army 1 at (120,53)). The unit-map view is at origin (114,46) after the load, checked in memory: 13 × 12 tiles, (120,53) at screen (545,366).
- **Patch:** every visible tile except (120,53) gets one word: the 96 words above, then 12 repeats (200, 238, 333 four times each) on other tiles. Map words only; no records changed.
- **Run:** fast rollingsave seed exe, seed 12345, Xvfb. Load, `Game.show(120,53)` (the view does not move), pointer parked off the map, one screenshot.
- **Measure:** every tile cropped at `UNIT_PAINT + 32·(c, r)` and hashed as 8-bit RGB, whole and inset by 2 px. *(2026-10-09: the drawn tile sits 1 px left of these crops, offset (−1, 0); comparisons among the crops still hold, but a comparison with the stored images needs the shift: [`2026-10-09-unit-icon-recolour-and-nation-glyphs.md`](2026-10-09-unit-icon-recolour-and-nation-glyphs.md).)* The memory word of every tile equals the patched word (`mem_word`).

## Evidence

- **Data:** `runs/experiments/data/run-exp-owner-colours/`: `probe_colours.py`, `analyse_colours.py`, `probe_colours.json`, `analyse_colours.json` (per tile: word, terrain under, memory word, hashes, top colours), `SAVES.sha256`.
- **Release** `run-exp-owner-colours`: `colours_PRE.SAV`, `colours_AFTER.SAV`, `colours_screen.png`, `montage_army.png`, `montage_fleet.png`, `montage_both.png`, and `tiles.tar.gz` (the 109 cropped tiles).

## Not established

- **Real armies and fleets of each owner:** the words were written into the map, not produced by armies of those owners. The earlier Rome tests showed the icon follows the stored word (`e18eaad`), so this should hold for every owner (`[derived]`).
- **The desktop palette:** Wine draws a 16-colour palette here. On the original Windows the colours should be the same standard 16, but this was not checked.
- **Owner words above 15 and the other marker families** (cities, etc.) were not drawn.
