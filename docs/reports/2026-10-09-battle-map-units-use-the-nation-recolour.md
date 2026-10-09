# The battle map recolours its unit sprites with the same routine and nation dwords as the unit map: Numidia's units are grey-filled in battle, and their background is the battlefield's own lime

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `0faa66d`. Inputs: the B2 saves
and window screenshots of release
[`run-exp-battle-sweep`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-sweep)
(SHA-256 in `runs/experiments/data/run-exp-battle-sweep/SAVES.sha256`), and the `TBattleMap.BatMapList`
image list extracted in `run-exp-unit-icon-resources`. Wine-only. It checks the `[derived]` consequence
added at `4ef90ec` to
[`2026-10-09-unit-icon-recolour-and-nation-glyphs.md`](2026-10-09-unit-icon-recolour-and-nation-glyphs.md).
It agrees with [`2026-10-04-decompiled-tactical-battle-rules.md`](2026-10-04-decompiled-tactical-battle-rules.md),
"How a unit is drawn" (attacker copies 0-14, defender 15-29, via `FUN_0044A6C8`), and pins the call
sites (0x43711e, 0x437161) and the flag `0x4A0B7C`.

**Review note:**
- The 3 saves and 3 window screenshots hash OK.
- **At promotion, the template list was not published** (uploaded since; see the redone simulation below). `TBattleMap_BatMapList.png` has a line in
  `run-exp-unit-icon-resources/SAVES.sha256`, but neither it nor the `.bmp` the draft names is a release
  asset (56 assets, none matching). So I could not redo the template simulation of
  `check_battle_recolour.py`. Instead I checked the screenshots without the templates:
  - At x = 32·col, y = 30 + 32·row, each screenshot has exactly 14 sprite cells: 9 using only Rome's
    three dwords (from the save) plus lime and black, and 5 using only Gaul's. That is the draft's
    count, and it confirms the y = 30 grid.
  - Of Gaul's 3 distinct sprites, 2 equal one of Rome's 8 pixel for pixel after swapping the three
    colours (maroon → purple, cyan → white, grey → blue). The third is a sprite Rome does not field
    here.
  - So the drawn sprites are shared templates recoloured per side from the save's dwords
    `[confirmed]` (Wine). The template-exact match (0 differing pixels against `BatMapList`) rests on
    ic2-conquest's run (since redone here, below).
- **Template simulation, redone (2026-10-09, after the upload at ic2-conquest `b2abac3`):**
  `TBattleMap_BatMapList.bmp`, `_mask.bmp` and `.png` are now release assets and hash OK. With my own
  script (a 4-column grid of 32×32 images; templates 0-14 recoloured with each side's dwords from
  `B2_placement.SAV`):
  - **42 of 42** sprite cells equal a recoloured template over the full 32×32 tile (Rome 9, Gaul 5
    per screen).
  - **462 of 462** empty cells equal image 15 exactly. So image 15 *is* the ground tile `[confirmed]`
    (Wine), no longer only very likely.
  - Template 4 with Numidia's dwords gives lime 684, black 174 and grey 166, as the draft says.
- **Code:** the excerpt `battlemap_sprites_436fb4.asm` reads `[0x4A0B74]` / `[0x4A0B76]` and calls
  `0x44a6c8` at 0x43711e and 0x437161, as the draft says. `xrefs.txt` also lists `0x456969 movsx edx,
  word ptr [ebx + eax*2 + 0x42c]`. That is a word read at +0x42C from an unidentified base, probably
  another table; it is not explained in the draft. The claim that "the dwords are read only inside
  FUN_0044a6c8" holds for the absolute addresses `0x474a94/98/9c`, but this line is not ruled out.
  **Resolved since** (`word_array_456940.asm`, ic2-conquest `b2abac3`): 0x456940 lies inside
  `TCellAuto_NewPattern` (0x456744 to 0x4569c0), the easter-egg automaton. The loop copies a 301-word
  row from `+0x1D2` to `+0x42E`, then sets each cell from a rule table at `+0x688` indexed by the sum of
  the three neighbours at `+0x42C/+0x42E/+0x430`. That is form data, not the nation colours `[derived]`.
- **Corrected on promotion:** the empty battlefield is a textured tile, not pure lime (see below). Image
  15 is that tile.

**Tag:** `[confirmed: decompile]` for the mechanism; `[confirmed]` (Wine) for Rome and Gaul; `[derived]` for
Numidia, since no Numidian battle was drawn.

## Answer

- **The battle form builds its 30 sprites with `FUN_0044a6c8`, the unit map's recolour routine** `[confirmed: decompile]` (`battlemap_sprites_436fb4.asm`, from 0x436fb4):
  - It runs when the battle flag `0x4A0B7C` is set.
  - Images 0-14 of the list at form field `+0x1AC` are each copied, recoloured with `owner` = army `[0x4A0B74]`'s owner word, and added to the list at `+0x1B0` (0x4370fb to 0x437137). `0x4A0B74` is the attacker's army.
  - The same 15 images are then recoloured with army `[0x4A0B76]`'s owner, the defender's, and added as images 15-29 (0x437139 to 0x43717a).
  - The army records are read at `0x47C1EC + 0x290 × army + 4`, which is the owner field.
- **There are only two other callers of `FUN_0044a6c8`, both in the unit map** (0x445cbe/0x445cff and 0x445f91/0x445fd5; `xrefs.txt`). The recolour dwords at `0x474a94 + 0x494 × owner` (+0/+4/+8) are read only inside `FUN_0044a6c8` and written only by `FUN_00448aa4`.
- **The templates are `TBattleMap.BatMapList` images 0-14** (17 images in all): Rome's purple `800080` background, white and blue, plus a 28 px lime `00ff00` frame. These are the 15 sprites type × size class, matching the grid word `side × 20 + 3 × type + size` of `2026-10-04-tactical-battle-sweep.md`.
- **In Wine this reproduces the drawn sprites exactly** `[confirmed]`. All 42 occupied cells of B2's 3 save/screenshot pairs match with 0 differing pixels over the whole 32×32 tile: 14 cells per pair, Rome as attacker and Gaul as defender, 2 distinct screenshots (`battle_recolour_check.json`). Each cell is the sprite of its grid word, the template recoloured with its side's owner dwords from the save.
  - **Pixel offset correction:** the tiles are drawn at window y = 30 + 32·row, which is 2 px lower than the `y0 = 28` of `b2_probe.py`. That script's occupied-or-empty test, 4 px inside the corner, is not affected.
- **So Numidia's units in battle** `[derived]`: with Numidia's dwords (`00ff00`, `000000`, `808080`), the purple background becomes **lime**, the white outline black, and the blue fill **grey**. In the large sprite (template 4) that gives lime 684 px, black 174 px and grey 166 px.
  - The templates' frame is lime `00ff00`. *Corrected on promotion:* the empty ground is not pure lime. Every empty cell in the three screenshots is one textured tile: lime 752, green 75, olive 73, white 64 and black 60 px of 1,024. Those are the colours listed below for `BatMapList` image 15, which is that ground tile (confirmed after the upload; see the review note). `b2_probe.py`'s test samples a lime pixel, which is why it reads the ground as pure lime. **A Numidian sprite's background is the same colour as the ground's lime base** (about three quarters of a ground tile): its black outline and grey fill stand out, and so does the absence of the ground's grass pattern.
- **Grey fill is not unique to Numidia in battle:** the fill dword is `808080` for Macedonia, Numidia and Gaul (`recolour_check.json` of `run-exp-unit-icon-resources`). Gaul's B2 sprites were drawn grey-filled. Numidia is the only one whose city artwork's fill (teal) differs from that dword.

## Evidence

- **Data:** `runs/experiments/data/run-exp-battle-numidia-colour/`: `xrefs.py`, `xrefs.txt`, `disasm_range.py`, `battlemap_sprites_436fb4.asm`, `check_battle_recolour.py`, `battle_recolour_check.json`, `README.md`.
- **Inputs:** `B2_placement.SAV`, `B2_after_end_turn_1.SAV`, `B2_after_end_turn_2.SAV` and `b2_placement_window.png`, `b2_after_end_turn_1_window.png`, `b2_after_end_turn_2_window.png` (release `run-exp-battle-sweep`, SHA-256 in `runs/experiments/data/run-exp-battle-sweep/SAVES.sha256`); `TBattleMap_BatMapList.bmp` (release `run-exp-unit-icon-resources`).
- **Exe:** `Imperial Conquest 2.exe`, SHA-256 `9d753d5d…` (full hash in `run-exp-unit-icon-resources/imagelists.json`).

## Not established

- **A Numidian battle drawn in Wine:** none was run. It would need a battle with a Numidian army, for example an L1 owner edit of the defender army, or a game played as Numidia.
- **Images 15 and 16 of `BatMapList`** (lime, green, olive, white and black; white and black): not recoloured. Image 15 is the empty-ground tile (462 of 462 empty cells equal it); image 16 is unidentified.
- **The desktop original:** Wine only, as for the unit map.
