# Nation marker colours: a background and a foreground per nation

The original draws every city, army and fleet marker as a **square filled with the owner's background
colour**, with the glyph (a temple, a house, a figure) drawn on it in the owner's **foreground colour** and
a black or white outline. Each of the 16 nations has its own (background, foreground) pair. Every colour is
one of the 16 standard Windows/VGA palette colours. Two pairs of nations share a background and are told
apart by their foreground. Two nations have green backgrounds, which stay readable on the green map
because the whole square is filled.

The build repository had the backgrounds from 2026-09-12 (commit `ca541b1`, the research inspector's
`OwnerColor` table) and lost them when a designed palette replaced that table (T49's specification, applied
by T94). The foregrounds had never been recorded before this report.

## Sources

- **A screenshot supplied by the user on 2026-09-29.** It is a 480 × 32 strip of the original's 16 nation
  icons (temples on coloured squares) in nation order, with two close-ups: Rome, "blue on purple
  background", and Carthage, "white on red background", in the user's words. It is not archived in
  `imp_conquest_fixtures`, so it is **observation by the main session, not re-checkable from a release**.
  The pixel values below were read from it with Pillow, snapping each colour to the nearest palette entry.
- **`1_rome_270_summer_7_1.png`** (`run-1-rome`), the original's Unit map around Italy at week 7, summer
  270 BC. Its city squares, read the same way, give Rome purple (128, 0, 128) with a white house glyph,
  Gaul maroon (128, 0, 0) with a cyan glyph, bright red (255, 0, 0) on Sardinia/Corsica, cyan (0, 255, 255)
  at Massalia, and navy (0, 0, 128) across the Adriatic. The land is green (0, 128, 0) and the sea blue
  (0, 0, 255).
- **The build repository's `godot/MapViewer.cs` at `ca541b1`** (2026-09-12) up to T94. Its
  `OwnerColor(code)` table, and its "dark glyph" code list {4, 5, 7, 8, 13, 14}.

## The pairs (observation)

Nation codes follow `NationCatalog` (confirmed against the DAT's nation table elsewhere). The background is the square; the foreground is the glyph's coloured part.

| Code | Nation | Background | RGB | Foreground | RGB | Outline |
| ---: | --- | --- | --- | --- | --- | --- |
| 0 | Rome | purple | (128, 0, 128) | blue | (0, 0, 255) | white |
| 1 | Carthage | red | (255, 0, 0) | white | (255, 255, 255) | black |
| 2 | Seleucid | olive | (128, 128, 0) | maroon | (128, 0, 0) | white |
| 3 | Ptolemaic | navy | (0, 0, 128) | magenta | (255, 0, 255) | white |
| 4 | Macedonia | white | (255, 255, 255) | blue | (0, 0, 255) | grey |
| 5 | Numidia | lime | (0, 255, 0) | teal | (0, 128, 128) | black |
| 6 | Gaul | maroon | (128, 0, 0) | cyan | (0, 255, 255) | white |
| 7 | Greece | cyan | (0, 255, 255) | magenta | (255, 0, 255) | black |
| 8 | Celtiberia | yellow | (255, 255, 0) | red | (255, 0, 0) | black |
| 9 | Illyria | navy | (0, 0, 128) | olive | (128, 128, 0) | white |
| 10 | Dacia | green | (0, 128, 0) | yellow | (255, 255, 0) | black |
| 11 | Bithynia | teal | (0, 128, 128) | blue | (0, 0, 255) | black |
| 12 | Galatia | blue | (0, 0, 255) | cyan | (0, 255, 255) | black |
| 13 | Armenia | magenta | (255, 0, 255) | red | (255, 0, 0) | black |
| 14 | Media | red | (255, 0, 0) | purple | (128, 0, 128) | white |
| 15 | Thracia | grey | (128, 128, 128) | black | (0, 0, 0) | white |

Shared backgrounds, each told apart by its foreground:
- red: Carthage (white) and Media (purple);
- navy: Ptolemaic (magenta) and Illyria (olive).

## Cross-checks (observation)

- **All 16 backgrounds equal the pre-T94 `OwnerColor` table** entry for entry. That table's two "byte-identical
  pairs" (Carthage/Media, Ptolemaic/Illyria), which build issue #154 treated as a defect, are the original's
  own shared backgrounds, and the foreground is what separates them.
- **The Unit-map screenshot agrees** on every nation visible in it: Rome, Gaul, Carthage, the cyan Massalia
  square (Greece) and the navy squares (Illyria). It also shows Rome's glyph as white there, where the strip
  shows blue columns in a white outline. The two views may render the glyph differently: the strip is an
  icon, the map glyph is smaller.

- **The army and fleet icons** (2026-10-09, Wine, every owner and size band drawn) have the same 16 backgrounds and shared pairs. Their two figure colours agree with this table's (outline, foreground) for 11 nations and differ for Macedonia (swapped), Numidia, Gaul, Illyria and Media: [`2026-10-09-owner-colours-by-band.md`](2026-10-09-owner-colours-by-band.md). Whether this table or the unit icons are the odd one out for those five is open. **Narrowed since** ([`2026-10-09-city-marker-colours.md`](2026-10-09-city-marker-colours.md), every owner's five city markers drawn in Wine): the cities use the unit icons' colours for 15 owners. Numidia's cities really are black and teal, as here; only its unit icons use grey. For Macedonia (possibly a role swap: in the capital temple the "outline" role is most of the glyph), Gaul, Illyria and Media, Wine's cities differ from this table too. So the open question is now strip vs Wine, for the desktop check.

## Inferences (candidates, not confirmed)

- The pre-T94 "dark glyph" list {4, 5, 7, 8, 13, 14} matches this table's black outlines for 4, 5, 7, 8 and
  13. Media (14) has a white outline in the strip, and 10, 11 and 12 have black outlines that the list does
  not include. The list was an approximation for the inspector, not the original's rule.
- Where the pairs are stored (the DAT's nation record, or constants in the executable) is **not located**.
  Worth a static search: the 16 backgrounds should appear as a table of palette indices or RGB triples.

## What this changes in the build repository

T97 (the correction task filed on 2026-09-29): a nation carries both colours, the map draws the
background square with the foreground-tinted glyph, and Rome goes back to purple. That replaces T49's
designed palette for the game and the inspector.
