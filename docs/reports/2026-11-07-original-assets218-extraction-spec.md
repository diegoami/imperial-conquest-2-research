# Original artwork and sounds: local extraction contract and reviewed coverage

**Status:** reviewed static consolidation and proposed extraction contract for
[research #218](https://github.com/diegoami/imperial-conquest-2-research/issues/218)
and [remake #1740](https://github.com/diegoami/imperial_conquest_2/issues/1740).
The known image-list and nation-glyph geometry is freshly checked against the
pinned EXE. Palette roles, sprite meaning and retained Wine observations come
from the linked promoted reports. A portable general extractor was subsequently
[accepted for the qualified static scope](../progress/research218-extractor-review.md),
at conquest `1544d666` (version 1.0.1). Complete adapter/native-rendering acceptance
remains outstanding; this report does not close #218.

**Sources:** conquest [PR #346](https://github.com/diegoami/ic2-conquest/pull/346),
branch `research/original-assets218-intake`, reviewed head
`36e4ad89ea57ea2f154652ddad84bd39fe6d1b11`, file `RUN-NOTES-assets218.md`;
existing extraction tools/data at conquest
`f71c70ffa9ccf8f7cfbb5335fb28c4c44d341ed6`; research baseline
`18da3a324cae3e5356bc72109f90c3495b0bc675`; remake asset consumers at
`55bd7fcef91e41b179a6df9851384bb687932e8e`.
EXE profile SHA256 `9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31`;
decompilation SHA256 `2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8`.
Applicability to other originals, translated builds or patched resources is unproved.

## What was independently checked

[original-assets218-check.py](../../scripts/original-assets218-check.py) reads the
private EXE without exporting media, using the existing research TPF0 parser.
All **29 signature-qualified forms parse**, with **11 image lists** matching
the retained `imagelists_decoded.json` counts and sheet geometry. Each has an
uncompressed 8-bit colour BMP and a 1-bit mask BMP of equal sheet dimensions.
All **16 nation glyphs** are 40×20, 4-bit BMPs with `NumGlyphs=2`.
The [scalar receipt](../data/research218-assets-intake-v1.json) records results.
This is a bounded intake check: signature coverage is not PE resource-directory
coverage, and matching mask dimensions is not a transparency/compositing proof.

The pinned dump contains **16 MakeSound calls covering 1–10**. Re-reading the
sound routine, map draw dispatch and recolour routine agrees with the existing
reports. The six pinned remake source files confirm **75 core + 25 tactical =
100 distinct keys**, file-based asset loading/fallback and the three-region
battle recolour. This is source inspection, not an executed Godot adapter test.
This initial consolidation decoded no WAV and reran no pixel matching or game.
The later linked extractor review independently decodes supplied WAVs and static
exports; it performs no game or native-rendering run.

The required whole-queue scan stopped with `tree of audit-195-b is truncated`;
it did not establish an empty queue. This intake reviews only the requested PR.
Skimming conquest's handover/results found continuing AI-audit work already
owned by #195, not an additional asset finding promoted here.

## Category matrix and exact crosswalk

Dimensions below are **cell/frame dimensions**, not full sheet dimensions.
"Understood" refers to the pinned resource and linked semantics; conversion and
consumer support are separate. The accepted extractor supplies PE resource
IDs/languages; component names below must not be presented as PE directory IDs.
Its 63 glyph sheets now include 44 command-key candidates; component correspondence
remains separate from consumer rendering and suitability.

| Category | Resource/component and stored count | Current remake key/correspondence | Disposition |
| --- | --- | --- | --- |
| Sea/land | `TUnitMap.TerrainList[0..5]`, 32×32 | 0 `terrain.sea_calm.tile`; 1 `terrain.sea_rough.tile`; 2 `terrain.plain.tile`; 3 `terrain.desert.tile`; 4 `terrain.forest.tile`; 5 `terrain.mountain.tile` | Understood resource/code crosswalk; indexed BMP conversion required. Code 1 is weather rough sea, not deep water. |
| Rivers | same list `[6..11]`, 32×32 | 6 EW; 7 NS; 8 NE; 9 ES; 10 SW; 11 NW → family `terrain.river.tile` | Stored shapes understood; one current key cannot represent six shapes. Shape metadata/consumer work required. |
| Strategic selection | same list `[12]`, 32×32 | no core key identified | Runtime SRCERASE composition; static alpha substitution cannot reproduce destination inversion. |
| Army/fleet markers | `TUnitMap.ArmiesList`, `FleetsList`, three 32×32 templates each | `[0..2]` → `army.tier1..3.icon`, `fleet.tier1..3.icon` | Understood; preserve size order and exact nation recolour roles. |
| Towns | `TUnitMap.Cities1List..Cities4List`, 16 owner pictures per list, 32×32 | four lists → `city.tier1..4.icon` | Understood artwork/order; owner identity is an additional dimension absent from these generic keys. |
| Capitals | `TUnitMap.CapitalsList`, 16 owner pictures, 32×32 | `city.capital.icon` | Same owner-variant gap; do not apply unit-template tint to stored city art. |
| Tactical units | `TBattleMap.BatMapList[0..14]`, 32×32 | index `3*type+size` → `battle.unit.<type>.<small|medium|large>` | LI, HI, archers, LC, HC; three sizes each. Exact three-region recolour, with other pixels preserved. |
| Tactical ground/selection | same list `[15]`/`[16]`, 32×32 | `battle.ground`, `battle.cursor` | Ground understood; cursor needs original raster-operation semantics. |
| Area-map base/points | `TAreaMap.MapsList`, 2 × 320×140; `PointsList`, 10 × 8×8 | no reviewed one-to-one key mapping | Partial; point-index meaning and compositing remain unresolved. |
| Nation buttons | `TPremierForm.sb_<Nation>.Glyph.Data`, 16 sheets, 2 × 20×20 frames | no nation-button asset keys among the 100 | Understood stored sheets/palette; all VCL button-state synthesis not established. |
| General toolbar/chrome | other DFM glyphs, PE cursors/icons/bitmaps, backgrounds | 36 `ui.command.*`, 8 `battle.toolbar.*`; five `unit.*.icon` choices | Partial/unresolved component-to-key mapping. Nation glyph extraction does not cover these commands. |
| Terrain surfaces | no demonstrated original equivalent | six `terrain.*.surface` keys | Authored seamless textures; extracting 32×32 tiles does not supply these assets or prove their current rendering use. |
| Audio | `WAVS/SOUND1.WAV` … `SOUND10.WAV` | ten `sfx.*` keys below | Code mapping understood; per-installation presence, original/converted format and consumer decoding need validation. |
| New scenarios/custom nations | no demonstrated matching original art | existing keys/fallbacks | Explicitly unavailable unless a supported mapping is evidenced; preserve existing fallback policy. |

The eleven lists total **128 stored images**: 2 + 10 + 17 + 13 + 3 + 3 +
5×16. The 32 stored nation frames are separate. Spare cells in the sheets are
not additional images. The new checker validates counts, not every frame's meaning.

Terrain semantics come from [rivers and markers](rivers-and-map-markers.md),
[terrain table](terrain-move-cost-table-in-dat.md) and the corrected
[rough-sea report](decompiled-map-code1-overlay.md). Map drawing reads terrain
image *code* for codes below 12 (`TUnitMap_PrintMapSquare`, dump :45941–45946).
City variant/owner dispatch follows immediately (:45948–45962); army/fleet
band/owner separation is :45964–45985. City population tiers are <25, 25–49,
50–99, ≥100, with capital overriding population, from
[city variants](2026-10-07-city-marker-variants.md).

## Colour, mask and compositing contract

Conquest's current experimental scripts are under
`runs/experiments/data/run-exp-unit-icon-resources/`: `extract_imagelists.py`,
`decode_imagelists.py`, `extract_glyphs.py` and their comparison helpers.
They reuse `runs/experiments/feature_inventory/extract_forms.py`; research has
the shared parser in `scripts/winhelp_tpf0/`. The scripts scan signatures, skip
some parse failures, assume particular BMP encodings and use ImageMagick for
PNG conversion. They are evidence/tools to extend, not a supported adapter.

Required decoder behavior for the next static packet:

1. Enumerate the PE resource tree, retaining type/name-or-ID/language and file
   bounds. Parse DFM component/property paths within the selected resource.
   Reject truncated data and report unsupported types explicitly; never silently
   treat a failed parse as an absent category. Preserve an explicit supported
   profile registry rather than assuming every Delphi executable matches.
2. For this profile's image-list blob, read the leading little-endian colour-BMP
   byte length and image count, the colour BMP, and the following mask BMP.
   Validate lengths, DIB header/compression, palette bounds, pixel offset, padded
   stride, signed height, count and sheet capacity before slicing. Read actual
   cell Width/Height (defaults 32), using columns = sheet-width / cell-width:
   `x=(index % columns)*cell-width`, `y=(index // columns)*cell-height` in logical
   top-left coordinates. Do not hardcode four columns for every resource.
3. Decode palette BGR entries to RGB, keeping indexed colours exact. Support the
   observed 8-bit list colour, 1-bit mask and 4-bit nation glyph formats; other
   formats are unsupported until separately tested. Convert to the consumer's
   file format locally, leaving the source and measured outputs unchanged.
4. Validate mask bit polarity and actual AND/XOR/raster-operation behavior with
   synthetic reference cases before assigning alpha. An image-list mask is not
   its palette's colour key. Opaque marker backgrounds must stay opaque where
   the original draws them that way. The fresh check establishes mask geometry
   only; no blanket "1 means transparent" assertion is promoted here.
5. Army/fleet/tactical templates substitute purple `#800080`, white `#ffffff`
   and blue `#0000ff` with nation fields +0x424/+0x428/+0x42c respectively.
   Normalize Delphi TColor byte order: the code compares blue as `0x00ff0000`,
   not the RGB literal `0x0000ff` (:49066–49105). Classify each source pixel once,
   then substitute; never recolour an already substituted value a second time.
   Preserve non-marker pixels. Unit colour fields need valid source provenance;
   generic nation accent colours do not replace the evidenced three fields.
6. Cities/capitals and nation glyphs retain their own palettes/owner pictures.
   Numidia's city/glyph fill is teal while its unit fill is grey. Nation glyph
   sheets have two horizontal frames; the bottom-left transparent colour is
   yellow for owners 0–4 and 15, white for 5–14. Stored frames alone do not
   establish disabled/pressed state behavior or license a general key-colour rule.
7. Strategic image 12 uses SRCERASE (`0x00440328`): the source is ANDed with the
   inverted destination. White source inverts the destination, black remains
   black. Preserve this operation separately from the image bytes. Retained Wine
   evidence establishes stable strategic selection without a game blink timer;
   do not generalize that timing result to every cursor or UI state.

The [unit/glyph report](2026-10-09-unit-icon-recolour-and-nation-glyphs.md),
[city report](2026-10-09-city-marker-colours.md),
[battle recolour report](2026-10-09-battle-map-units-use-the-nation-recolour.md)
and [selection report](2026-10-30-unit-map-selection-drawing1010.md) own the
retained pixel/Wine proofs. Those media were not re-exported or freshly matched.

## Sound crosswalk and partial installations

| File | Original event(s) | Remake key |
| --- | --- | --- |
| `SOUND1.WAV` | human strategic army step; tactical placement and step | `sfx.unit_move` |
| `SOUND2.WAV` | human strategic fleet step | `sfx.fleet_move` |
| `SOUND3.WAV` | archer shot | `sfx.battle_arrows` |
| `SOUND4.WAV` | light infantry/light cavalry shot | `sfx.battle_javelin` |
| `SOUND5.WAV` | human melee target and resolved melee exchange | `sfx.battle_melee` |
| `SOUND6.WAV` | failed siege | `sfx.siege_failed` |
| `SOUND7.WAV` | city captured | `sfx.city_captured` |
| `SOUND8.WAV` | fleet scuttled, sunk in combat or lost in storm | `sfx.fleet_sunk` |
| `SOUND9.WAV` | field battle with neither owner local/human | `sfx.battle` |
| `SOUND10.WAV` | nation conquered | `sfx.nation_conquered` |

[Sound research](2026-10-06-sound-events.md) supplies all 16 code call sites.
The later [cosmetic-gaps report](2026-10-06-cosmetic-gaps.md) supplies retained
Wine file-open evidence for strategic 1/2, scuttle 8 and computer battle 9.
File opens are not audible-output proof or native Windows acceptance; the other
triggers remain code-derived here. The fresh checker recounts all 16 call sites,
and source inspection confirms `MakeSound` selects Sound1–Sound10 and calls
`PlaySoundA` with flags zero (:59010–59050). No new audio measurements are claimed.

| Installation/profile | Required treatment | Current evidence |
| --- | --- | --- |
| Pinned EXE, supported embedded resources | inventory and decode supported categories locally | scalar geometry/counts checked; semantic coverage as above |
| Other EXE hash/language/variant | identify profile; return unsupported until separately qualified | no general-version compatibility evidence |
| WAVS with ten valid files | inspect RIFF/fmt/data bounds and actual PCM encoding/rate; decode or convert only as needed by the consumer | prior research records differing 8/16-bit mono sample rates, including converted working copies; this intake did not reopen audio |
| Missing/partial WAVS | report presence per sound; resolve only verified files and retain consumer fallback for missing keys | normal install cannot be assumed complete |
| Case variants/duplicates | case-insensitive logical discovery with original basename retained; reject ambiguous duplicate candidates | required portability behavior, not a newly observed original feature |
| User-selected EXE versus working directory | make sound-root selection explicit; never assume EXE folder and original sound working directory coincide | original path helper interpretation remains an inference in the sound report |
| Custom world/nations | report unavailable pictures; use existing fallback policy | no demonstrated original counterparts |

Original missing-file/default-sound and synchronous-play behavior describe the
original; this specification does not change remake playback, timing or policy.

## Output, validation and ownership

The proposed extractor emits a versioned **metadata manifest** with source profile,
resource identity/language, component/property, cell/frame index, dimensions,
encoding, mask/compositing mode, colour role, semantic ID, candidate remake key,
and per-category state (`available`, `partial`, `unsupported`, `missing`). Explicitly
separate source indices from consumer keys; retain owner/river-shape dimensions
even where a current consumer cannot express them. Missing mappings stay missing.

Media/cache files belong in a fresh private directory outside Git. Use atomic
no-overwrite publication and preserve the measured source. Cache identity must
include source content/profile, extractor version and conversion/compositing
options, including colour inputs when caching recoloured results. A cache hit
requires all relevant identities to match. No original bytes, extracted media,
screenshots or audio enter public repositories/releases. Public receipts contain
approved scalar metadata only. This is a proposed cache contract, not implemented
or tested remake behavior.

Extractor acceptance checklist (review outcome linked above):

- Reproduce the 11 lists/128 images and 16 nation sheets/32 stored frames, with
  explicit PE identity and complete per-category unavailable/unsupported results.
- Test palette channel order, row padding, top/bottom-up rows, 1-bit masks,
  4-bit glyph nibbles, spare-sheet cells and multi-frame slicing. Test malformed
  lengths/counts/offsets, unsupported encodings and no-overwrite publication.
- Check mask/compositing truth tables and exact source-index/semantic ordering;
  include the six river shapes, owner-colour exception and marker non-colours.
- Produce the per-installation ten-file WAV presence/format manifest without
  copying audio to public outputs. Keep source-file and converted-copy evidence
  distinct. Validate a decoder on supplied files; no audible/native claim follows.
- Research reviews tool/manifest results against private inputs and these pinned
  expectations. The remake session separately validates actual load/fallback,
  river/owner variants and rendered consumers. A key's existence is not proof that
  a screen draws it; no adapter or original UI-layout equivalence is established.

**Agreed research-side ownership:** consolidation/specification and independent
review. Conquest owns the proposed general static inventory/extractor packet;
the remake owner/session owns consumer/layout/adapter feasibility under #1740.
The initial intake supplied the consolidation and metadata checker. The later
accepted packet supplies bounded PE/DFM inventory, general glyphs, bitmap and
native cursor/icon containers, separate masks, compositing helpers and supplied
WAV validation. Area-map meanings, background/chrome completeness, native
composition and consumer acceptance retain explicit partial/unresolved status.
A rendering experiment, if needed, requires a separate bounded request; none was
run or authorized by this intake.

Reproduce this scalar check with explicit inputs:

```bash
python3 -B scripts/original-assets218-check.py "$ORIGINAL_EXE" \
  "$IC2_DECOMPILE/all_app_functions.txt" "$CONQUEST_SOURCE" "$REMAKE_SOURCE"
```

Use the source pins above; the checker itself supports only the pinned EXE/dump.
Its synthetic bitmap/rejection tests do not replace the next packet's extractor
tests. The receipt contains no media or private save identities. Research #218
stays open for the remaining semantic/consumer boundaries; the static packet and
research review are now delivered at the pin recorded above.
