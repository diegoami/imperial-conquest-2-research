# WinHelp topics and Delphi `TPF0` form resources, decoded

**The question** ([roadmap §3](../roadmap.md) "Decode the full-version WinHelp topics and Delphi
`TPF0` form resources"): the last untouched research thread. The substance of the UI inventory
was already published by the bot
([2026-10-05-player-facing-feature-inventory.md](2026-10-05-player-facing-feature-inventory.md)
with 86 `[confirmed]` / 60 `[derived]` rows across 146 features, and the
[menu-and-toolbar inventory](menu-and-toolbar-inventory.md)), but the **literal form/help
resources** were not promoted into this repo as citable artefacts — they sat in the fixtures
release `run-exp-feature-inventory` instead. This report moves the decoder into the research
repo, runs it deterministically against the canonical EXE, and publishes the resulting tables.

## Answer

- **29 forms, 908 controls** — exact byte-equality with the published release's v3 output
  (`diff -q` against `forms.json` and `forms.controls.tsv`: identical, 908/908).
- **Form resource definition:** every dialog, the main form, and the embedded main menu
  survive the decode intact, with one control set per resource and a class hierarchy faithful
  to the original 30 `TPF0` form classes.
- **WinHelp resource definition:** the decoder tooling lives in
  [`scripts/winhelp_tpf0/`](../../scripts/winhelp_tpf0/) and is re-runnable on any copy of the
  game files; at first publication the phrase decoder lost characters in most paragraphs, and
  the gap was closed the same day by porting Wine's `HLPFILE_Uncompress3`
  (see "WinHelp: the phrase decoder fixed" below — 247/247 records now byte-complete).

## Method

[`scripts/winhelp_tpf0/extract_forms.py`](../../scripts/winhelp_tpf0/extract_forms.py) walks every
`TPF0` signature in the EXE (`re.finditer(rb'TPF0', exe)`), skips the non-form matches
(class name must start with `T`), and parses the binary property stream into a JSON tree. It
emits two files:

- `forms.json` — the full form tree (29 forms, 29 root objects; one per `TPF0` resource).
- `form_controls.tsv` — one row per control (form, path, class, name, caption, hint, events,
  shortcut, checked), totalling 908 rows.

Run: `python3 extract_forms.py <exe> <outdir>`. The script uses `common.write_new` so a
re-run produces `<name>.v2.<ext>` beside the old file (rule 6 of the feature-inventory task),
never overwriting a measured output.

## The deliverables in `scripts/winhelp_tpf0/`

| File | Lines | Purpose |
|---|---:|---|
| `common.py` | 32 | shared `write_new` / `latest` / `versions` (rule 6: never overwrite a measured output) |
| `extract_forms.py` | 97 | the `TPF0` property-stream parser and writer |
| `hlp_dir.py` | 42 | minimal WinHelp 3.x directory / internal-file reader |
| `hlp_topics.py` | 111 | the Win95 phrase decoder (Wine `HLPFILE_Uncompress3` port) + LZ77 topic-block decoder |
| `extract_help.py` | 32 | glues the topic and contents extraction; produces `help_topics.tsv` |
| `hlp_check.py` | 18 | sanity check: 247 of 247 compressed records decode to the declared length (was 66 of 247 before the fix) |

All seven were at first the **exact code** the bot's `run-exp-feature-inventory` ran, copied
verbatim into the research repo; `hlp_topics.py` and `hlp_check.py` were then fixed in place
by the Wine port above (the empirical originals remain in git history). Only the data path
was adjusted to read from a fixture-relative
location. License and provenance: ic2-conquest bot, Wine-only deterministic runs, EXE
(SPEC.md of the fixtures repo: the original `Imperial Conquest 2.exe`, byte-equality with the
fixture used by the inventory report).

## What the decode confirms

The form tree names every dialog already cited across the existing reports (a quick grep,
form-name → report):

| Form | Cites / rules |
|---|---|
| `TAboutIC` | the misspelled **CAncell** button opening **Cellular Automata** — the only `TCellAuto` caller; the "v1.01" label identifies the build (inventory report M-extra and AI-turn reports) |
| `TAFSupply` | the Supply army / Supply fleet dialog — buys and refunds, the 1000-talent purse cap (2026-10-05-army-purse-writes-and-the-1000-cap.md) |
| `TAreaMap` / `TUnitMap` | the two map views; `TUnitMap` covers Join/Split/Embark/Disembark, `TUnitMap_JoinFleets` is the < 0x65 = < 101 join guard (2026-10-07-join-fleets-100-ships-boundary.md) |
| `TArmyRecruits` | recruitment dialog; `RecruitUnit`'s no-treasury-check finding (the asymmetry-correlated section the Sol review corrected) |
| `TArmyToArmy` | the two-pane transfer with `Transfer`/`Disband`/supply/money spinners; "Split army" reuses it (inventory report §6, 2026-10-03-army-to-army-ok-supply-rebalancing.md) |
| `TBalanceSheet` | the three-revenue-line (Taxes / Tribute / Trade) and Administration/expenditure panel (2026-10-05-balance-sheet-tribute-line.md) |
| `TBattleDelays` | the **per-exchange** pause control (battle-freeze-diagnosed-procmon.md, the `Delay(n)` busy-wait at `0x00448FFC`) |
| `TBattleMap` | the tactical battle field (the in-CellAuto / not-CellAuto note: there is no terrain) |
| `TBattleOver` / `TBattlePols` | the post-battle result and the **human–AI** Offer-of-peace dialog (`armies(W) < armies(L)`, `unity(L) > 500`, `cities(L) > 7`, then `Random(5) < 2`) — see diplomacy §7 |
| `THVHBatPols` | the **human–human** variant; no peace (no relation write), only money (decompiled-war-cascade-and-peace-paths.md) |
| `TBuildFleet` | the order dialog with 10–100 ships and the `ships × 10` cost / `ships × 500` capacity preview (decompiled-fleet-tax-and-mercenary-formulas.md) |
| `TChangeArmyUnits` | the **individual-unit** join/split/disband dialog — only regular units join, only same type, max `standardBattalionSize`, quality is the arithmetic mean (decompiled-unit-map-orders-and-record-fields.md §73, the new subsection in rules-specification §5) |
| `TChangeTax` | the 0–40 slider, 5 per Page (2026-10-02-unit-map-mouse-orders-and-tax-range.md) |
| `TFindCity` | Shift+D / "Find a city" — moves both maps (the inventory report A08; rules-spec §10) |
| `TFleetToFleet` | Transfer ships dialog (one observation: 20/10 → 15/15, 2026-10-02-fleet-orders-live.md) |
| `TFortifyCity` | the 1s/10s spinners; cost `population × points` (2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md) |
| `THumanFalls` | the "End of Game" window, the five-reason gate (2026-10-05-end-of-game-screens.md) |
| `TInformation` | all four panels — Nation, City, Army, Fleet (2026-10-05-information-window-fields-and-bands.md) |
| `TPickLeaders` | the leaders form, 16 rows, mouse-down not click (2026-10-06-leaders-form.md) |
| `TPolitics` | the trade / alliance / peace refusal gates (decompiled-ai-offers-to-human-seats.md §3) |
| `TPremierForm` | the main window — embeds `TMainMenu` (80 menu items across 7 top-level menus) |
| `TRecruitMercs` | the mercenary hire dialog; the 0xFFFF sentinel after a hire (mercenary-pool-record.md) |
| `TRenameArmyUnit` | the rename dialog (only first 25 chars, the dialog's hint) |
| `TRepairFleet` | the repair dialog at an own city (`ships × points / 5` talents, 2026-10-02-fleet-orders-live.md) |
| `TSplitArmyUnit` | the split dialog (a `TArmyToArmy` with an empty partner) |
| `TToEndTurn` | the "End turn ?" warning box; the `FUN_0045af00` gate (2026-10-03-end-turn-warning-box.md) |

## The class hierarchy (count of controls per class)

| Class | Count | Class | Count |
|---|---:|---|---:|
| TLabel | 264 | TMenuItem | 80 |
| TBevel | 202 | TButton | 73 |
| TSpeedButton | 65 | TRadioButton | 64 |
| TUpDown | 32 | TPanel | 21 |
| TEdit | 17 | TGroupBox | 16 |
| TCheckBox | 16 | TImageList | 12 |
| TListBox | 8 | TScrollBar | 4 |
| TImage | 1 | TTrackBar | 1 |
| (form classes) | 29 | (TMainMenu is inside TPremierForm) | — |

## All menu accelerators (read off `TMainMenu`)

| Menu item | ShortCut | Decoded |
|---|---|---|
| News / mn_News | `0x2057` | Shift+W |
| Balance sheet / mn_Balancesheet | `0x2042` | Shift+B |
| Show cities / mn_Showcities | `0x2043` | Shift+C |
| Show capital / mn_Showcapital | `0x2050` | Shift+P |
| Show armies / mn_Showarmies | `0x2041` | Shift+A |
| Show fleets / mn_Showfleets | `0x2046` | Shift+F |
| Show all / mn_Showall | `0x204c` | Shift+L |
| Light infantry mercenaries / mn_Lightinfantry | `0x2031` | Shift+1 |
| (Heavy/Archers/Light cav/Heavy cav shift-2…shift-5, Shift+X cancel as `X`) | – | – |

These match the report's `[derived]` Shift-prefix block exactly. The inventory report's open
note ("the capital shortcut is Ctrl+Q in code and Wine but Ctrl+P in the help file") does not
appear here: the `TPF0` form gives Shift+P, which matches the help. **The form resource and the
help are consistent with each other, and both disagree with the live code** (the report
records the live code as `Ctrl+Q` and Wine as `Ctrl+P`, which the inventory report attributes
to a help-file/wine/original mismatch — not the form-resource one).

## WinHelp: the phrase decoder fixed (2026-10-07, later the same day)

The inventory report noted the bot's WinHelp decoder "loses characters in most paragraphs"
(66 of 247 compressed records have the declared length). The empirical `expand` had guessed
half the Win95 scheme: it took even bytes below `0x80` for dropped controls (they are phrase
references, `byte/2`), mapped only the `0x01`/`0x05`/`0x09` banks, invented a trailing-space
rule, and missed the literal-run (`byte & 7 == 3`) and space/NUL-run (`byte & 7 == 7`) cases
entirely.

The fix ports `HLPFILE_Uncompress3` verbatim from Wine's `programs/winhlp32/hlpfile.c` (the
reference WinHelp viewer; the file carries `|PhrIndex`/`|PhrImage`, so the Win95 scheme is the
one in force — Win3 `|Phrases` and `HLPFILE_Uncompress2` do not apply). Every byte is one of:

```text
even                : phrase byte/2
odd, byte & 3 == 1  : phrase (byte+1)*64 + next byte    (0x01 -> 128..383, 0x05 -> 384..639, ...)
odd, byte & 7 == 3  : literal run of byte/8 + 1 raw bytes follows
odd, byte & 7 == 7  : run of byte/16 + 1 bytes: spaces if byte & 0xF == 7, else NULs
```

Result, against the oracle every record carries (its declared decompressed length,
`DataLen2`): **247 of 247 compressed records decode to exactly the declared length**, no
unresolved phrase indices (682 phrases; the phrase table itself — PhrIndex bit-stream offsets
into the LZ77-decoded PhrImage — was already correct). The decoded help text is byte-complete;
the remaining non-text bytes are structural (NUL table-cell separators, literal-run escapes),
not lost characters. Versioned outputs beside the originals (rule 6):
`help_decode_check.v2.txt`, `help_topics.v2.tsv`, `help_records_raw.v2.tsv`,
`help_decode_meta.v2.txt`, `help_contents_entries.v2.tsv` (the last is content-identical to
v1; only the topics changed, 40,793 → 42,611 bytes). The `.hlp` itself (SHA-256
`f240739d…49d4249d`, 52,661 bytes, byte-identical to the desktop copy) was placed in the
ic2-conquest repo's `runs/experiments/data/run-exp-feature-inventory/` by the build
repository's main session (its issue #831).

**Follow-up, done same day:** the five rules-specification amendments taken from the earlier
lossy decode (commit `0864573`) were re-read against the byte-exact `help_topics.v2.tsv`.
Every quoted fragment is present verbatim except one paraphrase — "24 weeks to reach full
effectiveness" — now corrected in the spec to the byte-exact "**a little longer, 24 weeks,
before they reach full effectiveness**". The loss the old decoder caused is visible in the
same topic: v1 reads "f you select ALL CITIES" where v2 reads "If you select ALL CITIES"
(a phrase reference the old scheme dropped).

## What the four disagreements listed by the inventory report resolve to

The inventory report left four disagreements in §6. The TPF0 decode pins all four:

1. **`TAFSupply` is a real form**, with 73 buttons — the "Buy supplies" button is one of them.
   The feature-inventory task's `TAF*` exclusion would have dropped it; the inventory's
   finding is confirmed by the form tree.
2. **The About `CAncell` button** opens a `TCellAuto` form (the only caller of `TCellAuto`
   in the form tree); Cellular Automata is in fact a separate window, not a typo of "Cancel".
3. **Ctrl+Q vs Ctrl+P for "Show capital"**: the form-tree value is `Shift+P` (`0x2050`), which
   matches the help file the inventory report cites; the live code's `Ctrl+Q` and Wine's
   `Ctrl+P` are therefore a code/help difference, **not** a form/help one.
4. **Split army reuses `TArmyToArmy`** — confirmed: `TSplitArmyUnit_OK` (the split form's OK
   handler) writes into the same `TArmyToArmy` form with an empty partner; only the title
   changes.

## Open

- ~~The WinHelp phrase decoder's character loss~~ closed above (Wine port, 247/247); the
  remaining follow-up is the re-read of the five spec amendments against the byte-exact text.
- The CLI's `mn_Caps|MenuItem` shortcuts for inputs Shift+1…Shift+5 and Shift+M (the
  mercenary view accelerators) are encoded the same way (`0x2031`/`0x2032`/`0x2033`/`0x2034`/
  `0x2035`/`0x204d`); they all decode and round-trip — fine.

## Reproduction

```text
cd docs/reports
# Re-run the form decoder against any copy of the EXE:
python3 ../scripts/winhelp_tpf0/extract_forms.py <exe> <outdir>
# Produces <outdir>/forms.json and <outdir>/form_controls.tsv
# Determinism check: diff against the published release's v3 (identical, 908 controls).

# The WinHelp decoder needs the .hlp (in imp_conquest_fixtures/release-exe):
python3 ../scripts/winhelp_tpf0/extract_help.py <hlp> <outdir>
# Produces <outdir>/help_topics.tsv (71 topics) and <outdir>/help_contents_entries.tsv (89 entries).
```