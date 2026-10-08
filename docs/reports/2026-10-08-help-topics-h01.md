# Help topics — verification of row H01

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `e8b2984e`
(part of the same `runs/experiments/data/run-exp-feature-inventory/` batch as
`2026-10-08-help-reference-tables-h05.md`, which is also promoted in this round).
The release `run-exp-feature-inventory` carries the `FI_batch1_screenshots.tar.gz`
asset with the live Wine capture.

**Closes** the cell-level verification of H01 of
[`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md);
the row was already `[confirmed]` at the row level; this draft tightens the
cell-level form/menu extraction (caption, OnClick, menu path).

**Tag policy:** same as the inventory. A row or sub-row is `[confirmed]` when a
tracked file in `diegoami/ic2-conquest` lists the cited evidence.

## Answer

The H01 row is fully backed by tracked data — the form decoder, the function list,
and the contents-list decoder all reproduce the row's prose.

| Sub-claim | Source | Match status |
|---|---|---|
| The Help menu item **Help topics** opens the WinHelp file `Imperial Conquest 2.hlp` | `runs/experiments/data/run-exp-feature-inventory/form_controls.tsv`: `TPremierForm/PremierForm/MainMenu/mt_help/mn_Helptopics` (a TMenuItem, OnClick=`HelpTopics`); `function_list.tsv` row `TPremierForm_HelpTopics @ 0x0045c280`; the .hlp is `runs/experiments/data/run-exp-feature-inventory/Imperial Conquest 2.hlp` | identical |
| The viewer shows the **Introduction** topic first | `help_contents_entries.v2.tsv` row 1: `level=2 path="Game aspects > Introduction" title="Introduction" context="Describe_game"`; `help_topics.tsv` row 43 (offset `0x003ae3`) is the topic "Introduction" with the body that opens with "*Imperial Conquest 2 is based in the ancient Mediterranean …*" | identical |
| The .hlp holds **71 topics** and the contents holds **89 entries** | `wc -l help_topics.v2.tsv` = 72 (one header + 71); `wc -l help_contents_entries.v2.tsv` = 90 (one header + 89) | identical |
| The decoder is the post-fix one (247/247 records exact) | `coverage_report.v8.txt` self-test (commit `a3ad689`); the .hlp is committed at `runs/experiments/data/run-exp-feature-inventory/Imperial Conquest 2.hlp` with SHA-256 in `SAVES.sha256` | identical |
| The viewer screenshot shows the live window | `MANIFEST-batch1.txt` row `3e9e17da…  FI_b1_06_help_topics.png` (release asset `FI_batch1_screenshots.tar.gz`) | identical |

## Two open notes

1. **Help → top-level menu order in the contents list.** The contents file opens
   with `level=1 path="Game aspects"` (no `title`), then jumps to level 2 entries
   starting with `Introduction`. The "first shown topic" interpretation tracks this:
   Wine viewers render the first contents entry as the first topic the user sees.
   A clone's HelpTopic index should reproduce this ordering — `Game aspects` is a
   category header (level 1), the eight children (`Introduction`, `Improvements`,
   `Cities`, `Armies`, `Fleets`, `Battle`, `Time`, `Fonts`) are the topics. The
   contents have 89 entries across multiple category headers (Menu, Map keys, etc.,
   per the contents file). This isn't an open *bug* but is the kind of layout detail
   a renderer needs to get right.
2. **The .hlp file itself isn't text-readable end to end.** The phrase decoder is
   247/247, but the **topic bodies** are decoded row by row in `help_topics.tsv`
   and not human-checked at body level on every row; the readme says a few
   characters still drift in compressed paragraphs. The H01 row only requires the
   *index* to be exact (which it is); the topic bodies are H05
   (terrain/symbols/colours/costs/details/matrix) territory and were verified
   verbatim under that draft.

## Method

- **Form + function extraction.** `runs/experiments/feature_inventory/extract_forms.py`
  (form controls) + `extract_dump_strings.py` (function list). The `HelpTopics` menu
  item lives under the Help menu (`mt_help`); the handler is the named function
  reproduced above.
- **Help decoder.** `runs/experiments/feature_inventory/hlp_dir.py`, `hlp_topics.py`,
  `extract_help.py`, `hlp_check.py` (a from-scratch WinHelp 3.x reader; the
  phrase-code table is recovered empirically). Outputs `help_topics.tsv` (71 topics
  × title/text) and `help_contents_entries.tsv` (89 contents entries ×
  level/path/title/context). Phrase decoder is the post-fix version (commit
  `a3ad689`).

## Reproduction

```bash
python3 runs/experiments/feature_inventory/hlp_topics.py "Imperial Conquest 2.hlp" \
    > runs/experiments/data/run-exp-feature-inventory/help_topics.v3.tsv
python3 runs/experiments/feature_inventory/extract_help.py "Imperial Conquest 2.hlp" \
    > runs/experiments/data/run-exp-feature-inventory/help_contents_entries.v3.tsv
grep -E "HelpTopics|ToggleHints|About\b" runs/experiments/data/run-exp-feature-inventory/function_list.tsv
grep -E "mn_Helptopics|mn_About|mn_Showhints" runs/experiments/data/run-exp-feature-inventory/form_controls.tsv
```

The form and function extracts are deterministic — they read the EXE and the .hlp,
neither of which changes. No live Wine session is needed; the screenshot evidence
is the `FI_batch1_screenshots.tar.gz` release asset.

## Related

- [`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md)
  row H01 — this report's evidence column is appended in the inventory.
- [`2026-10-07-winhelp-tpf0-decoded.md`](2026-10-07-winhelp-tpf0-decoded.md) — the
  phrase decoder that takes the .hlp from 181/247 to 247/247.
- [`2026-10-08-help-reference-tables-h05.md`](2026-10-08-help-reference-tables-h05.md)
  — the H05 verification, which uses the same topic bodies; the row H01 ↔ H05
  split keeps the topics index (H01) separate from the reference-table content
  (H05).
