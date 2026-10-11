# Running notes: intake of findings/2026-10-11-g2-original-checks.md

Branch `intake/2026-10-11-g2-original-checks`. Draft: diegoami/ic2-conquest commit 70c51eb760ff5d5628f9d7f9485352b6229e9a28 (SHA checked: it is the newest commit touching the file).

## Plan
1. Fetch the draft, the run's data dir and the release (417 assets); `sha256sum -c`.
2. Re-read saves with my own parser (C3, C4, C4b, C5a, C5b, C5c, C7), re-run the C7 model.
3. Read the cited dump lines (dump sha 2018c205...).
4. Write `docs/reports/2026-10-11-g2-original-checks.md`, cross-links, spec, evidence index, intake row, README 169 -> 170.
5. `bash scripts/pending-drafts.sh`, push, open PR (no merge, no ack).

## Progress
- (start) verification done in the scratchpad: 417/417 release files OK, dump hash matches, saves and code re-read.
- commit 1: report, cross-links (gap analysis, inventory, refusal texts, mouse reports, army-moves-field, fleet-orders-live, storms), spec, evidence index (47 rows + 3 bumps), intake row, README 169 -> 170.
- `bash scripts/pending-drafts.sh`: `pending: 0`.

## END
Done. Verified: 417/417 release files, 2 storms saves, dump hash 2018c205; saves re-read; model re-run. Nothing blocked. Not merged, draft not acked (main session does that after review).
