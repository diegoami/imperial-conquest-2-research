# Remake → original IC2 → remake: six scenarios, seven Wine sessions

**Status:** promoted candidate `[confirmed, partial]`, 2026-10-23. Original-program
observations under Wine/Xvfb; not native Windows acceptance or lossless conversion.
Intaken from ic2-conquest [PR #152](https://github.com/diegoami/ic2-conquest/pull/152),
merged commit [`4ca3afa04c3eb8454c63ed6a4984f5564e8e0496`](https://github.com/diegoami/ic2-conquest/commit/4ca3afa04c3eb8454c63ed6a4984f5564e8e0496),
finding blob `58e26a94b318b96e927a6c061022220fde0c6750`.
Research validation is recorded below; no separate model review was launched.
**Task:** [conquest #151](https://github.com/diegoami/ic2-conquest/issues/151),
explicitly approved by the owner in the desktop session.

## Answer

Here, **native save** means the remake's JSON format, not a native Windows run.

Six distinct native saves exported through the remake CLI, opened in the
unmodified original, accepted a tax order, saved to new files, and reopened in a
fresh original process. All six reopened resaves were byte-identical to the
original-written preceding save. The recruitment/fleet-order scenario also
completed one turn in the instrumented original: `AUTO0721.SAV`, Spring week 3,
270 BC. Its explicit SaveAs and fresh-reopen resave were byte-identical too.

All seven original-written results imported into the remake, survived native
save/reload, resumed as playable sessions, accepted tax 27, and re-exported.
The returned exports passed the conquest policy checker; among the fields read
by conquest's independent Python parser, the only difference from each
original-written result was the requested tax change, 26 → 27.

Native metadata and derived statistics differ across the conversion boundary;
the measured differences are listed below. This evidence supports these tested
strategic states, not general export readiness or closure of #99.

## Revisions, runtime and artifacts

- Conquest base: `e05570573b02ebb91b41b6e2d80d7f4ac2dedaff`.
- Remake: `a510c33f0aaa2998ff1186127ff18eb13f489496` (PR #1350).
  No source or build products were written into that checkout. Its assemblies
  were built into this experiment's ignored artifacts directory.
- .NET SDK 10.0.401; Wine 10.0 (Ubuntu package
  `10.0~repack-12ubuntu1`); private Xvfb display, 1280×1024, DejaVu Sans,
  no Liberation fonts. Full fingerprints are in `environment.jsonl`.
- Unmodified `Imperial Conquest 2.exe` SHA256:
  `9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31`.
- Instrumented `Imperial Conquest 2 fast rollingsave seed.exe` SHA256:
  `354d8265cba1dac2a80a0a96ce76367a368e37a4e79c30eb4f0bb587b35c532f`.
  Only the seventh session uses it, with startup seed 12345.
- Tracked commands, stdout/stderr, hashes, comparisons and validator:
  [`runs/experiments/data/run-exp-sav-conversion-roundtrip/`](https://github.com/diegoami/ic2-conquest/tree/4ca3afa04c3eb8454c63ed6a4984f5564e8e0496/runs/experiments/data/run-exp-sav-conversion-roundtrip).
  Final comparison: `comparison-v6.json`; audit: `validation-v2.json`.
- Binary/private artifacts:
  [Drive IC2/artifacts/run-exp-sav-conversion-roundtrip](https://drive.google.com/drive/folders/1OQWVtWzeN6k-_EgfU_3U_vFa4MjmXfqv).
  [Complete bundle](https://drive.google.com/file/d/10BGy85kM1jUA7iXCdvwzkYXcc1z6fZzQ/view),
  `batch2-complete.tar.gz`, 3,118,135 bytes, 85 files, SHA256
  `c21c8607eb1def47b7ea592d2494dd5b9a72ef9dea0cf1342b26205b94fdd91f`.
  The earlier `batch1-conversions.tar.gz` and both manifests remain available.
  Upload completion, file size and parent folder were verified with Drive
  metadata readback; a remote download/hash comparison was not performed.
  No EXE, DAT or prefix was included in either archive. No release was created:
  `IC2_RELEASE_TOKEN` is absent. Drive storage succeeded.

## Scenarios and original-program checks

The five gameplay-derived saves use a fresh classical-mediterranean /
classical-faithful session, seed 7, human Rome. The initial snapshot is the
first human Rome seat, after any preceding AI seats. All have 334 cities and
no eliminated nation or open battle. The additional cargo case is explicitly
synthetic, constructed through public native model records rather than play.

| Case | Native state | Armies / fleets / building / cargo | Original saves: immediate / order / fresh reopen | Original turn |
|---|---|---|---|---|
| A | Initial human turn | 14 / 2 / 0 / 0 | `P151AI.SAV` / `P151AO.SAV` / `P151AR.SAV` | 0720 |
| B | Tax25; 1,000 HI queued at Rome; 10 ships ordered at Neapolis | 14 / 3 / 1 / 0 | `P151BI.SAV` / `P151BO.SAV` / `P151BR.SAV` | 0720 |
| C | Same game, 6 turns later | 13 / 4 / 2 / 0 | `P151CI.SAV` / `P151CO.SAV` / `P151CR.SAV` | 0726 |
| D | 12 turns later, including launched construction | 17 / 4 / 2 / 0 | `P151DI.SAV` / `P151DO.SAV` / `P151DR.SAV` | 0732 |
| E | 24 turns later | 15 / 6 / 1 / 0 | `P151EI.SAV` / `P151EO.SAV` / `P151ER.SAV` | 0744 |
| F | Synthetic Rome army aboard a launched fleet | 14 / 2 / 0 / 1 | `P151FI.SAV` / `P151FO.SAV` / `P151FR.SAV` | 0720 |
| G | B again, instrumented original, then one End turn | 14 / 3 / 1 / 0 initially | `P151GI.SAV` / `P151GO.SAV`; `P151GT.SAV` / `P151GR.SAV` after turn | 0720 → 0721 |

For each, the actual `IC2.Cli --export-sav <native.json> --output <new.sav>
--template <original.sav>` interface wrote the input. The explicit template was
`run0-start-AUTO0720-seed12345.SAV`, used by the converter for interface settings.
All six exports passed `scripts/sav_export_policy_check.py` without `--source`.
The original was run in a copied private prefix without copying existing saves.
No original/owner save or measured output was overwritten or deleted.

All seven immediate original saves differ from their exports by exactly one
byte at the current nation's `+0x482`, inside `NATION.infowin` geometry
(atlas v13). Nothing else in the file differs. The original tax order changes
exactly one byte at `NATION.tax`, `+0x44A`; requested values are checked in the
save. Every fresh reopen produces an exactly matching file. Processes were
restarted after explicit SaveAs using the isolated wineserver; UI Exit/clean
application shutdown was not tested.

F's native army and fleet use matching owner, coordinates and reciprocal
references. `P151FR.SAV` retains army cell −1 and the carrier's army index 0.
It does not establish a natural embark/disembark sequence or cargo combat.

G advances exactly one calendar tick, 0720 → 0721. Its `AUTO0721.SAV`,
`P151GT.SAV` and `P151GR.SAV` all hash to
`beaf8057c6d5bd922a2511e24752e88c1f7b328c650b45ce43e311a59adfd264`.
This is continuation evidence in the instrumented original, not matching
future AI or combat outcomes between the two engines.

## What does not round-trip identically

`comparison-v6.json` compares all native state members after normalizing entity
IDs by record index and the documented mercenary-name alias, excluding RNG and
a launched fleet's native-only build-city metadata. It retains every observed
difference instead of declaring equal state:

| Source snapshot | Native field differences |
|---|---:|
| Initial | 11 |
| Orders | 12 |
| After 6 turns | 52 |
| After 12 turns | 55 |
| After 24 turns | 57 |
| Synthetic cargo | 11 |

The differences fall only in `Calendar.TurnIndex`, nation `Population`,
`PopulationAtStart`, `TreasuryAtStart`, `CityCountAtStart`, and fleet
`CoveredTileCode`. Exact paths, values and per-class counts are retained.
The importer starts elapsed turns at 0, keeps the actual BC/season/week, resets
the score baselines to import time and recomputes population from owned cities.
The native snapshots' population counters can already lag city ownership.
Several native fleets have a null covered-cell value where import reconstructs
sea code 0. Those are measured normalization boundaries, not silent equality.

Original SAV has no recoverable RNG stream. The importer supplies scenario seed
270; after the returned remake's accepted tax order the root seed is
11400714819323198755. This is exactly one normal `CommandDispatcher` advance
(`RngStreams.GoldenGamma`), even though the tax handler needs no random draw.
It is not original/remake RNG continuity.

Known upstream conqueror-history import loss remains tracked in
[remake #1351](https://github.com/diegoami/imperial_conquest_2/issues/1351).
None of these source snapshots has an eliminated nation, so this experiment
does not exercise or resolve that defect.

## Refusals, audit and remaining scope

- `improved` ruleset: actual CLI returns 2, `UNSUPPORTED_RULESET`, no SAV written.
- Existing destination: actual CLI returns 2, `Destination already exists`;
  SHA256 of the earlier export is unchanged.
- Final audit: 8 check groups pass, including 164 per-artifact SHA256 checks
  across the two retained bundles, all seven session receipts, the precise
  original byte differences, cargo references and all return continuations.
- Infrastructure failures remain recorded: redirected CLI assemblies initially
  lacked their `IC2.sln` ancestor; experiment-only read-only layout links fixed
  that. Initial checker calls omitted required `--out`; corrected invocations
  were separately retained. The first audit wrongly expected an accepted
  command to leave RNG unchanged; `validation-attempt-v1.json` records that
  error and the source-backed correction. No game trial failed or was rerun
  to hide a result.
- This is implementer validation, without an independent model review. It does
  not cover the owner's twelve JSON files, format-4 migration, native Windows,
  hotseat, pending offers, all refusal classes, battle saves, eliminated nations,
  all seeds, or naturally played cargo loading/landing. #99's owner gates remain.

Research consolidates this as **bounded Wine acceptance and playable bidirectional
strategic conversion** for the tested states, with normalization and untested cases
explicit. Research #37 and conquest #99 remain open.


## Research intake checks (2026-10-23)

The active research session read the full finding, command adapter, live-run driver,
comparison code, validator, complete final live receipts and retained failure records.
It then independently rehashed the available local archives/artifacts and reran the
unchanged pinned comparison and validator in an isolated temporary source snapshot.
No source, save or measurement in either sibling repository was changed.

- **Complete comparison:** byte-identical to `comparison-v6.json`, SHA256
  `3620da4f7e7b20aa9ccd62b3493fe52a960556d16aa9ebaa39a6dd0c912ca998`.
- **Complete validation:** byte-identical to `validation-v2.json`, SHA256
  `050db681562e2a6526955cbeaa2306b3eb4cf4a9e5a25ea323aa7f354caf29db`;
  eight passing groups and 164 manifest-entry hash checks across both bundles.
  These count archive entries, not 164 unique files. Archive contents were also
  freshly read and matched entry-by-entry to both pinned manifests (79 + 85).
- **Fresh policy checks:** all six source exports and seven returned exports pass
  without `--source`. Each of the seven return-command receipts reports native
  save/reload equality and the verified tax27 continuation, with no skipped army/fleet.
- **Recomputed native differences:** initial/cargo 11 each, orders 12, six turns 52,
  twelve turns 55, twenty-four turns 57. No unlisted differences were discarded by
  the comparator. Its explicit exclusions remain: record-ID normalization, RNG,
  launched-fleet build-city metadata and the documented mercenary-name alias.
- **Original-code explanation:** the pinned decompile
  (`all_app_functions.txt` SHA256 `2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8`)
  identifies `TInformation_InitializeForm` (`0x43B014`, lines 40323–40332): the
  current nation's word at `0x474AF2 + nation*0x494` is rounded down by its signed
  remainder modulo 16 before setting window height. Nation-relative `+0x482`
  changing 708 → 704 is therefore a checked UI normalization, not an unexplained
  gameplay-field difference. All seven measured immediate saves differ by exactly
  that one byte and retain equal file lengths.
- **Remake-code explanation:** at pinned `a510c33`,
  [OriginalSaveImporter](https://github.com/diegoami/imperial_conquest_2/blob/a510c33f0aaa2998ff1186127ff18eb13f489496/src/IC2.Engine/Import/OriginalSaveImporter.cs)
  lines 235–269, 378–389, 455–461 and 545 corroborate the population/baseline,
  covered-cell, elapsed-turn and seed boundaries. [CommandDispatcher](https://github.com/diegoami/imperial_conquest_2/blob/a510c33f0aaa2998ff1186127ff18eb13f489496/src/IC2.Engine/Core/Commands/CommandDispatcher.cs)
  line 201 and [RngStreams](https://github.com/diegoami/imperial_conquest_2/blob/a510c33f0aaa2998ff1186127ff18eb13f489496/src/IC2.Engine/Core/Rng/RngStreams.cs)
  lines 37/69 corroborate the single root-seed advance after the accepted command.
  The retained initial audit failure was an expectation error, not a hidden game failure.

Reproduction: [read-only intake runner](../../scripts/conversion151-intake-check.py)
and [scalar research receipt](../data/conversion151-intake-v1.json):

```bash
python3 scripts/conversion151-intake-check.py \
  --conquest "$IC2_CONQUEST" --artifacts "$IC2_CONVERSION151_ARTIFACTS" \
  --out /tmp/conversion151-new.json
```

The artifact directory must contain the two retained archives, extracted run files
and audit assemblies named by the pinned upstream validator. Hash verification
uses the measured local originals; research did not download the Drive copy and
cannot add a remote readback claim. No new .NET, Wine, native Windows or game run
occurred. Historical UI/CLI execution remains upstream observation, now checked
against retained outputs and receipts; this is not a separate live repetition.

## Relationship to existing acceptance gates

This extends the [gate-2 policy](2026-10-22-sav-export-gate2-policy.md) with actual
Wine acceptance of generated native exports and return continuation. It does not
replace the [native Windows tax-only evidence](2026-10-18-sav-export-original-windows-tax-candidates.md),
which remains a different 3/3 profile. The owner twelve-input manifest, T185 review,
format-4 migration and native Windows native-JSON outputs are still separate gates
in [pending requests](../pending-requests.md). Research #63 is a separate quality-range
investigation, not a result of this experiment. No build Evaluated marker or downstream
completion is asserted.
