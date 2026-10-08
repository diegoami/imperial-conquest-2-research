# The army marker on the map carries a troop-size band (the "0x10 bit" of the mercenary run)

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commits
`32007e0` + `dab3fff` (draft) and `b12265f` (run data). Release
[`run-exp-army-marker-band`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-army-marker-band)
holds the 12 saves (`t24999`, `t25000`, `t49999`, `t50000`, each `PRE` / `BEFORE` / `AFTER`), and
their SHA-256s are committed at `runs/experiments/data/run-exp-army-marker-band/SAVES.sha256`.
Wine-only evidence. It explains the open item in
[`2026-10-08-merc-hire-ignores-queue-r08-guards-slot-20.md`](2026-10-08-merc-hire-ignores-queue-r08-guards-slot-20.md)
(army 1's map word 200 → 216 in c1).

**Review note:**
- **The function body is already on this side.** The draft says the body of `FUN_0044a80c` is
  not in its extracts, but it is decompiled here, in
  [`decompiled-mobilization-and-mercenary-restock.md`](decompiled-mobilization-and-mercenary-restock.md)
  ("the army's map marker is a size band") and
  [`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md)
  Part 3:
  - `band = FUN_0044a698(army) / 1000; marker = owner + (band < 25 ? 200 : band < 50 ? 216 : 232)`;
  - the marker is written only while the army is not aboard a fleet.
- **The run confirms that reading in play at both boundaries.** Integer division puts 24,999 in band 24
  (200) and 25,000 in band 25 (216); 49,999 → 49 (216) and 50,000 → 50 (232).
- **Call sites.** They match ic2-conquest's committed extracts: :43670 (`code_extract_refusals.txt`)
  and :44594, :44603 and :49488 (`code_extract_q1_purse.txt`).
- **Not on a load.** That a load does not recompute the marker is new. Before this run, nothing on
  this side said when the marker is written.

**Tag:** `[confirmed]` for the boundaries 25,000 and 50,000. `[confirmed]` for "a load does not recompute the marker".

## Answer

- An army's map word is **owner + 200 below 25,000 troops, owner + 216 below 50,000, owner + 232 from 50,000 up**, as `docs/sav-layout-notes.md` reads it from the research reports. So the "0x10 bit" is the step into the second size band.
- In the mercenary run, the Samnite (3,868) took army 1 from 22,000 to **25,868** in c1 and c2, so 200 → 216. In c4 the army went from 2,000 to 5,868 and stayed at 200.
- **Live boundaries** (the Samnite hire into army 1, sized so the total lands on the boundary):

  | Army 1 after the hire | Map word at (120,53) | Band |
  |---:|---:|---|
  | 24,999 | 200 | < 25,000 |
  | 25,000 | **216** | 25,000-49,999 |
  | 49,999 | 216 | 25,000-49,999 |
  | 50,000 | **232** | ≥ 50,000 |

- **The word is stored, not derived on load.** In t49999 and t50000, the `BEFORE` save (just loaded, army 1 at 46,131 / 46,132 men, which is band 216) still had **200**, the word from the edited pre-state. It changed only when the hire rewrote the army: `TRecruitMercs_RecruitMercUnit` calls `FUN_0044a80c(army)` right after adding the unit (:43670). The formula is the research reports' decompiled reading of `FUN_0044a80c`, matched here at both boundaries. The same function also runs after a Join (`FUN_0044acb4`), and after `TArmyToArmy_OK` (:44594, :44603). So an edited save keeps a stale band until the army is next changed by one of those (`[derived]`).

Evidence: run-exp-army-marker-band, `t24999_{PRE,BEFORE,AFTER}.SAV`, `t25000_*`, `t49999_*`, `t50000_*` (release `run-exp-army-marker-band`; SHA-256 in `runs/experiments/data/run-exp-army-marker-band/SAVES.sha256`); `probe_band.py`, `probe_band.log`, `probe_band_*.json`. Also the c1/c2/c4 saves of `run-exp-merc-full-queue`.

## Method

The fixture is `saves/run0-start-AUTO0720-seed12345.SAV`: Rome army 1 at (120,53), next to Heraclea's Samnite offer; purse 100, supplies 176. Army 1's 20 slots were replaced by two regular heavy-infantry units summing to (target − 3,868). Fast rollingsave seed exe, seed 12345, Xvfb :99. Load, save `BEFORE`, `g.hire_mercs(1, rows=(0,))`, save `AFTER`; then read the map word at (120,53), offset 120 × 280 + 53 × 2 in the save.

## Not established

- Whether the band is shown on screen (a different marker icon). The unit-map icon was not compared. **Settled since:** three icon sizes, chosen by the stored word, not by the troops: [`2026-10-08-army-icon-follows-the-size-band.md`](2026-10-08-army-icon-follows-the-size-band.md).
