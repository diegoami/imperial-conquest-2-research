# The unit-map army icon has three sizes, chosen by the stored marker band

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit
`a7e8246` (`a7e8246181b7f0811ca73e86eb46af262cdf9014`); run data at `2ba9bd2`. Release
[`run-exp-army-marker-icon`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-army-marker-icon)
holds the six variant saves, their `_screen.png` and `_tile.png` captures and `montage_bands.png`;
their SHA-256s are committed at `runs/experiments/data/run-exp-army-marker-icon/SAVES.sha256`.
Wine-only evidence. It closes the open item "whether the on-screen icon differs by band" in
[`2026-10-08-army-marker-size-band-on-the-map.md`](2026-10-08-army-marker-size-band-on-the-map.md).

**Review note:**
- **Tile pixels.** The six `_tile.png` files were downloaded and their decoded RGB pixels hashed
  on the reviewing side. Each patched variant is pixel-identical to the unpatched variant of the
  same word, and the three bands are pairwise different, as the draft says. The hash values differ
  from the draft's because a different digest was used; they agree pair for pair.
- **Montage.** `montage_bands.png` shows three icons of increasing size: a small soldier with a
  spear, a medium one, and a large one with a bigger shield and a mace.
- **The two 216 screenshots.** They differ outside the tile (bounding box (6,78)-(752,542)),
  probably from a different map scroll after the Area-map click. The cropped tile is identical,
  so this does not affect the result.

**Tag:** `[confirmed]`.

## Answer

- **The icon differs by band.** Rome army 1 is drawn as a small soldier at map word 200 (under 25,000 troops), a medium one at 216 (25,000-49,999), and a large one with a bigger shield and a mace at 232 (50,000 and up). The three 32×32 tiles are pixel-different (RGB hashes `347b29fc…`, `8d952a53…`, `cad8d407…`; enlarged side by side in `montage_bands.png`).
- **The icon follows the stored word, not the troops.** With the troops held fixed and only the map word patched, the tile is pixel-identical to the band of the word:
  - 24,999 troops with word 216 gives the 216 icon;
  - 24,999 with word 232 gives the 232 icon;
  - 50,000 with word 200 gives the small 200 icon.
- Since a load does not recompute the word (`be0691a`), an edited save shows the stale icon until the army is next rewritten.

| Variant | Word (save = memory) | Troops | Tile RGB hash |
|---|---:|---:|---|
| w200_t24999 | 200 | 24,999 | `347b29fc65a7e7b7` |
| w216_t25000 | 216 | 25,000 | `8d952a534782b236` |
| w232_t50000 | 232 | 50,000 | `cad8d407c66e802f` |
| w216_t24999 | 216 (patched) | 24,999 | `8d952a534782b236` |
| w232_t24999 | 232 (patched) | 24,999 | `cad8d407c66e802f` |
| w200_t50000 | 200 (patched) | 50,000 | `347b29fc65a7e7b7` |

Evidence: run-exp-army-marker-icon. `<variant>.SAV`, `<variant>_screen.png` and `<variant>_tile.png` for the six variants, plus `montage_bands.png` (release `run-exp-army-marker-icon`; SHA-256 in `runs/experiments/data/run-exp-army-marker-icon/SAVES.sha256`); `probe_icon.py`, `probe_icon.log`, `probe_icon.json`. The source saves are `t24999_AFTER.SAV`, `t25000_AFTER.SAV` and `t50000_AFTER.SAV` of run-exp-army-marker-band.

## Method

Each variant is loaded with the fast rollingsave seed exe, seed 12345, Xvfb :99. `Game.show(120, 53)` brings army 1's tile into the unit map (an Area map click when needed; nothing is selected), the pointer is parked on the bare root window, and the screen is captured. The tile is cropped at its centre ± 16 px ((545,366) in every run) and its RGB bytes are hashed. The patched variants change only the map word at save offset 120 × 280 + 53 × 2; the game's memory held the same word after the load (`mem_word`).

## Not established

- The fleet icons (bands 300 / 316 / 332 by ships, `FUN_0044a878` in the research reports). **Settled since:** a small sailboat, a galley with three shields and a larger galley with four, also chosen by the stored word: [`2026-10-08-fleet-marker-band-and-icon.md`](2026-10-08-fleet-marker-band-and-icon.md).
- Other owners' colours by band (only Rome was drawn).
