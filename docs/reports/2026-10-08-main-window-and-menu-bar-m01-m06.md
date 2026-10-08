# Main window and menu bar — verification of rows M01–M06

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit
`bc980f1` (one of the `runs/experiments/data/run-exp-feature-inventory/`
batch). Release `run-exp-feature-inventory`, asset `FI_batch1_screenshots.tar.gz`
+ `FI_batch2_screenshots.tar.gz`.

**Closes** the cell-level verification of M01–M06 of
[`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md).
Six rows anchored on `TPremierForm` (the main game-window class): the menu
bar (M01), the speed-button bar (M02), the four-window layout (M03), the
title bar (M04), the persisted window positions (M05), and the sound
dispatcher (M06). One consolidated draft.

**Tag policy:** carried from the inventory. M01–M03 = `[confirmed]`,
M04–M06 = `[derived]`. This draft tightens the cell-level evidence without
re-tagging. The M04/M05/M06 rows were already cell-verified in
[`2026-10-06-cosmetic-gaps.md`](2026-10-06-cosmetic-gaps.md) §1 / §5 / §2
(both that report and this one cite the same `dump_string_literals.v2.tsv`
rows for the title fragments, the `StoreFormPositions` address, and the
`MakeSound` literals); this draft is the cell-level map of the whole main
window, not a replacement.

## Answer

### M01 — Menu bar (seven top-level menus)

Form `TPremierForm` carries a `MainMenu` with seven `TMenuItem` entries, each
with a `caption` for the menu header (and no `OnClick` because they're parents,
not actions). Reproduced verbatim from `form_controls.tsv`:

| Path | Caption | Notes |
|---|---|---|
| `PremierForm/MainMenu/mt_file` | `File` | parent |
| `PremierForm/MainMenu/mt_Game` | `Game` | parent |
| `PremierForm/MainMenu/mt_Strategy` | `Strategy` | parent |
| `PremierForm/MainMenu/mt_Nations` | `Nations` | parent |
| `PremierForm/MainMenu/mt_Areamap` | `Area map` | parent |
| `PremierForm/MainMenu/mt_Unitmap` | `Unit map` | parent |
| `PremierForm/MainMenu/mt_Help` | `Help` | parent |

Each captures as `<mt_name>` only (no `OnClick`); children are one level deep
under the parent menu's path. The inventory's SS cites the seven screenshot
files `FI_b1_11_menu_file.png ... FI_b1_02_help_menu.png` (release asset
`FI_batch1_screenshots.tar.gz`, hashed in `MANIFEST-batch1.txt`).

### M02 — Main speed-button bar (nine main + sixteen nation + one All-nations)

`TPremierForm/Panel1` carries 26 `TSpeedButton` rows: 9 main bar buttons, 16
nation buttons, and `sb_Allnations`. Reproduced verbatim:

| Path | Hint (caption is empty for speed buttons) | OnClick |
|---|---|---|
| `…/sb_Open` | `Open saved game` | `OpenGameFile` |
| `…/sb_Save` | `Save game position` | `SaveGameFile` |
| `…/sb_Endturn` | `End player's turn` | `EndTurn` |
| `…/sb_News` | `News` | `StrategicDecision` |
| `…/sb_Pols` | `International relations` | `StrategicDecision` |
| `…/sb_Tax` | `Taxation` | `StrategicDecision` |
| `…/sb_Balance` | `Balance sheet` | `StrategicDecision` |
| `…/sb_Newunit` | `Recruit unit` | `StrategicDecision` |
| `…/sb_Newfleet` | `Build fleet` | `StrategicDecision` |
| `…/sb_Rome` … `…/sb_Thracia` | one row per nation | `ChangeNation` (16 rows, exactly matching `state/sav.py` `NATIONS`) |
| `…/sb_Allnations` | `All nations` | `ChangeNation` (sets the index to 0x10) |

Live screenshot: `FI_b1_01_main.png` (SHA-256
`4651bc79d81e259fb8eaeeed3949a2e0943a6ceab9f9e539b8389aa3fd3870dd`,
`MANIFEST-batch1.txt`). Help topic "Main speed buttons" (topic 47) reproduces
the same button names.

### M03 — Four windows

`forms.json` carries all four `TPF0` resources:

| Form | Class | Notes |
|---|---|---|
| `PremierForm` | `TPremierForm` | main window (with the menu + speed bar above) |
| `AreaMap` | `TAreaMap` | area-map child window |
| `UnitMap` | `TUnitMap` | unit-map child window |
| `Information` | `TInformation` | information panel |

Coverage: `forms.json` ships 29 forms total (4 of them the four windows; the
other 25 are dialogs/forms). `coverage.md §2 'Main window'` lists
`TAreaMap_AreaMapClick 0x0043e210` as the area-map click handler. Live
screenshot: `FI_b1_01_main.png` (same hash as M02 — one screenshot carries
all four windows in the four-windows layout).

### M04 — Title bar "Imperial Conquest 2    <Nation>'s turn   (<leader>)"

`TPremierForm_SetTurnTitle @ 0x0045c084` (function_list.tsv). The four
space-padded string fragments that compose the title are reproduced verbatim
from `dump_string_literals.v2.tsv` rows 482–485:

| row | literal |
|---|---|
| 482 | `"Imperial Conquest 2    "` |
| 483 | `"\'s turn"` |
| 484 | `"   ("` |
| 485 | `")"` |

The form's `Caption` (TPF0) carries a base caption — see
`coverage.md §2 'Main window'` — and `SetTurnTitle` overrides it per turn.
Live evidence per `explore/b1.log`: window title
`Imperial Conquest 2    Rome's turn   (Appius Claudius)`. **The cell-level
in-play evidence (the X window name for the empty-leader and named-leader
cases) is in [`2026-10-06-cosmetic-gaps.md`](2026-10-06-cosmetic-gaps.md) §1**;
this row's `F:` citation in the inventory was updated to point there.

### M05 — Window positions kept in the save

`TPremierForm_StoreFormPositions @ 0x0045bb1c` (function_list.tsv; row 5 of
the inventory cited `0x0045bb1c`, exact match). Coverage: 8 bytes of
geometry at the end of the `.sav` file (read by `state/sav.py` indirectly
via the SAV trailer) restored on load — research-side report
[`news-log-format-and-messages.md`](news-log-format-and-messages.md) Q1 'The
SAV' describes the +46 trailer and the window geometry inside it.
`[derived]` carry-over: code-only path; the trailer's geometry bytes are
read at runtime, not yet pinned byte-exact. **The cell-level in-play
evidence (the byte-exact `[42, 104, 170, 320]` round-trip from CG_T4_b8)
is in [`2026-10-06-cosmetic-gaps.md`](2026-10-06-cosmetic-gaps.md) §5**.

### M06 — Sound effects (10 WAV files in `WAVS/`)

`TPremierForm_MakeSound @ 0x0045bf28` (function_list.tsv). The
case-1-through-10 dispatch is verbatim against the literals table;
`\\\\WAVS\\\\` is the folder path:

| row | literal | role |
|---|---|---|
| 454 | `"\\\\WAVS\\\\"` (in `TPremierForm_InitialiseForm` 0x0045a780) | folder prefix used by `MakeSound` |
| 471 | `"Sound1"` | first WAV filename prefix |
| 472 | `"Sound2"` | … |
| … | … | … |
| 480 | `"Sound10"` | tenth WAV filename prefix |
| 481 | `".WAV"` | extension |

Construction: `MakeSound(n)` concatenates `"\\\\WAVS\\\\"`, `"Sound<n>"`,
`".WAV"` and calls PlaySoundA (per the inventory). Help topic "Improvements"
(topic 44) closes the loop: *"Ten sound files (WAVS\\SOUND1.WAV ...
SOUND10.WAV) are played through PlaySound."* **The cell-level in-play
evidence (strace `openat` of WAVS/SOUND<N>.WAV for cases 1, 2, 8, 9) is in
[`2026-10-06-cosmetic-gaps.md`](2026-10-06-cosmetic-gaps.md) §2.**

## Three open notes

1. **M05 is `[derived]` because the 8-byte trailer geometry is read at runtime
   but not pinned.** The `StoreFormPositions @ 0x0045bb1c` +
   [`news-log-format-and-messages.md`](news-log-format-and-messages.md) Q1
   'The SAV' citation covers the *where*; the *how* (the 8-byte field layout,
   which 2-byte shorts are x / y / width / height, what the right window's
   view-state byte is) is open. Would need capstone on the function body to
   close.
2. **M04's title-bar fragments concatenate with `<Nation>'s turn   (<leader>)`**
   — the full string template lives inside `SetTurnTitle`'s prologue, not in
   the literals table. The 4-row literal list above is the building blocks;
   the joining blanks and "   (..." separator come from the function's
   text-format logic. A faithful reproduction needs capstone on the function.
3. **The `mt_file` / `mt_Game` / `mt_Strategy` / `mt_Nations` / `mt_Areamap` /
   `mt_Unitmap` / `mt_Help` rows carry no `OnClick`** — they're parents;
   child menu items inherit one menu level deeper. The reproduction needs to
   add children one path level below each `mt_*` for the Inventory's children
   rows to verify (F01–F06 are children of `mt_file`, etc.). This is
   consistent with the existing form extraction but doesn't preclude a clone
   from missing a parent.

## Inferences

- **M01–M02 are co-located** — the same TPremierForm/Panel1 carries the menu
  bar (`MainMenu`) and the speed-button bar (`Panel1`). A reproduction can
  build both with one form's resources; the layout in the inventory's claims
  matches the decompile order (menu first, then speed buttons below).
- **The hint on a speed button is the button's display label** (the `caption`
  column is empty for `TSpeedButton`s; the hint column carries the
  human-readable text shown on hover). M02's hints (`"Open saved game"`,
  `"Save game position"`, …) are the canonical labels — a reproduction should
  set the hover label to that text and the visible glyph to the standard
  icon.
- **M05's trailer is a known structural feature of the SAV format.** The
  +46-byte trailer plus 8 bytes of geometry is per `state/sav.py`'s read;
  reproducing it requires `state/sav.py` to read exactly the same offsets on
  load. Not verified cell-by-cell against the SAV reader in this draft.

## What this does not establish

- M04's full title-bar template (the join string between the four literals).
- M05's 8-byte geometry field layout inside the SAV trailer.
- M06's `PlaySoundA` parameter set (the inventory cites `PlaySoundA`; the
  literal `uFlags` argument to PlaySoundA isn't pinned).

## Reproduction

```bash
cd ~/projects/ic2-conquest
python3 runs/experiments/feature_inventory/extract_forms.py           # regenerate form_controls.tsv + forms.json
python3 runs/experiments/feature_inventory/extract_dump_strings.py     # regenerate function_list.tsv + dump_string_literals.tsv

grep -E "mt_file|mt_Game|mt_Strategy|mt_Nations|mt_Areamap|mt_Unitmap|mt_Help" \
     runs/experiments/data/run-exp-feature-inventory/form_controls.tsv
grep -E "TPremierForm_SetTurnTitle|TPremierForm_StoreFormPositions|TPremierForm_MakeSound" \
     runs/experiments/data/run-exp-feature-inventory/function_list.tsv
grep -nE "TPremierForm_MakeSound|TPremierForm_SetTurnTitle" \
     runs/experiments/data/run-exp-feature-inventory/dump_string_literals.v2.tsv
sha256sum runs/experiments/data/run-exp-feature-inventory/explore/FI_b1_01_main.png
```

The form, function and literal extracts are deterministic — they read the
EXE + dump. The `FI_b1_01_main.png` hash should match `MANIFEST-batch1.txt`.

## Related

- [`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md)
  rows M01–M06 — this report's evidence column is appended in the inventory.
- [`2026-10-06-cosmetic-gaps.md`](2026-10-06-cosmetic-gaps.md) — the in-play
  evidence for M04, M05, M06 (title bar, window positions, sound openat).
- [`2026-10-08-keyboard-shortcuts-k01-k03.md`](2026-10-08-keyboard-shortcuts-k01-k03.md)
  — K01 shares the same `form_controls.tsv` and `mn_*` paths.
- [`news-log-format-and-messages.md`](news-log-format-and-messages.md) Q1
  'The SAV' — the SAV-trailer description that M05's row cites.
