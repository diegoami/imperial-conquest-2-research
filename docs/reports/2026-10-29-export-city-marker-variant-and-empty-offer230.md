# Converting a save through the remake refreshes stale city marker tiers and changes the empty offer's type

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `9ae4367` (PR #237),
conquest [#230](https://github.com/diegoami/ic2-conquest/issues/230) (tracker #228). Release
[`run-exp-diff084-orders-b3`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-orders-b3);
the save SHA-256s are committed at `runs/experiments/data/run-exp-diff084-orders-b3/SAVES.sha256`.
Wine-only. Remake **v0.8.4** (`d9cc71bc82e22ad1d3d7c373c3d80d61ed0bcbeb`).

**Tag:** `[confirmed, partial]` for the bytes (one start save). This review **establishes** the cause
of the marker change `[confirmed: decompile + saves]`; the draft had left it open. The cause of the
offer-type change is not established.

**Review note (2026-10-29):**
- **Release integrity:** the archive was downloaded and all 92 saves match `SAVES.sha256`.
- **Bytes re-read** with my own reader from `embark/original/a000.SAV` and `embark/remake/a000.SAV`
  (turn 0734):
  - exactly three map cells differ, with the words and cities in the table below;
  - the tail's empty offer is (−1, 1) in the original and (−1, 0) in the export.
- **Cause of the marker difference.**
  [`2026-10-07-city-marker-variants.md`](2026-10-07-city-marker-variants.md) establishes three
  facts `[confirmed: decompile + saves]`:
  - a city's variant is its population tier: `< 25`, `25–49`, `50–99`, `≥ 100`;
  - variant 4 marks a capital;
  - the original rewrites the tier only when a city **changes owner**, never as it grows, so a city
    keeps a stale, smaller icon after growing.

  I checked every city of both saves against that rule:
  - in the original, all 16 capitals carry variant 4, and the **only** non-capital cities whose
    variant differs from their population tier are Bordeaux (26 → tier 1, shows 0), Tarquinii
    (26 → 1, shows 0) and Tarrentum (51 → 2, shows 1);
  - in the remake's export **no** city is stale.

  So the exporter (or the importer's model) recomputes the tier from current population, while the
  original keeps the tier from the last change of owner. All three cities are conquered (owner ≠
  allegiance) because only a change of owner writes a tier at all. Conquered cities that have not
  crossed a threshold since their capture match.
- **The other raw bytes lie outside the parsed fields.** The two saves differ in 7,501 raw bytes in
  all. Apart from the three map cells and the offer, they fall in:
  - city-name bytes after the terminator (1,612);
  - army records (4,527);
  - the empty recruit-slot area of the nation records;
  - the news/tail area (820).

  The bot's parser (`state/sav.py`) finds every parsed field equal: the cities, the 14 armies, the
  fleets, the nations, the mercenaries and all 40 news lines. So these bytes are outside what it
  reads. I did not classify the army-record bytes field by field. See the export reports for the
  live regions
  ([`2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md`](2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md)).
- **Overlap:** no earlier conversion report
  ([`2026-10-23-remake-original-save-conversion-roundtrips.md`](2026-10-23-remake-original-save-conversion-roundtrips.md),
  [`2026-10-23-broad-save-conversion-matrix.md`](2026-10-23-broad-save-conversion-matrix.md))
  records the marker tier or the empty offer's type. This adds to them and contradicts nothing.

## Answer

`saves/fleet-port-antium-0734.SAV` (Rome, Autumn week 5, 270 BC) was imported into the remake
(`OriginalSaveImporter`) and exported straight back (`OriginalSaveExporter`), with no order in
between. Compared with the original's own save, there are two semantic differences:

1. **Three city marker cells.** A city's marker word is 20 + owner + 16 × variant
   ([`2026-10-09-city-marker-colours.md`](2026-10-09-city-marker-colours.md)). The owner part is
   unchanged. The export writes the variant one tier higher, which is the tier the city's current
   population calls for:

   | City (index) | Tile | Owner (allegiance) | Population / max | Original word | Exported word |
   |---|---|---|---|---|---|
   | Bordeaux (27) | (47,29) | Celtiberia (Gaul) | 26 / 27 | 28 (variant 0) | 44 (variant 1) |
   | Tarquinii (80) | (98,39) | Gaul (Rome) | 26 / 27 | 26 (variant 0) | 42 (variant 1) |
   | Tarrentum (123) | (124,52) | Gaul (Greece) | 51 / 56 | 42 (variant 1) | 58 (variant 2) |

2. **The empty pending offer's type.** With no offer pending (sender −1), the original's tail holds
   type 1 and the export writes 0. The cause is not established.

The Rome 270 BC start (`BASE.SAV`) round-trips exactly in both respects (`run-exp-diff084-tooling`,
checkpoint `a000`: 0 differences). Its cities have not grown past a tier since their last change of
owner, and its offer slot holds a real offer.

## Effect on the comparisons

Every #230 batch 3 case that starts from this save shows both differences at its start (`a000`),
and they stay unchanged after the orders. The sweep now sets aside a difference already present at
the start (`difftest/sweep.py`) and does not count it against the order. Batch 3's 14 fleet,
mobilization and unit orders otherwise came out the same in both games.

Whether the remake also draws these cities with a different icon in play was not checked. This is a
finding about the save conversion. If the remake's model recomputes the tier from population in
play, too, that is a separate display difference: the original keeps the stale icon until capture.

## Evidence

Run `run-exp-diff084-orders-b3` (turn 0734): `embark/original/a000.SAV` vs
`embark/remake/a000.SAV`. The same holds in every case of the batch that starts from
`fleet-port-antium-0734.SAV` or `fleet-split-antium-0734.SAV`. The data is in
`runs/experiments/data/run-exp-diff084-orders-b3/` (`results-rejudged-*.jsonl`,
`details.start_baseline`).

## What this does not establish

- Native Windows behaviour.
- Other saves: only one save had stale tiers here.
- The remake's in-play icon.
- Why the empty offer's type changes.
- Which of the remake's import or export step drops the stale tier.
