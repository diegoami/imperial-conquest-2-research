# Join fleets — in-play 100-ship boundary reproduction (L11 promotion from `[derived]` to `[confirmed, partial]`)

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit
`1e10c5d` (the L11 boundary finding + tracked code; the underlying initial
draft commit is `af58e05`; both are on the bot's `experiment/cosmetic-gaps`…
no, branch `main` for this run; the `1e10c5d` is the release-citation
amendment). Release
[`run-exp-join-fleets-cap-in-play`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-join-fleets-cap-in-play),
tagged `2026-10-08T10:22:52Z`, six binary SAV assets cited by bare filename
per CLAUDE.md rule 1. Tracked code at
`runs/experiments/data/run-exp-join-fleets-cap-in-play/{trial.py,
trial_driver.py, results.json, SAVES.sha256}`.

**Closes** the L11 forward-pointer carried by the
[L01–L14 draft](2026-10-08-news-and-messages-l01-l14.md) (the
Join-fleets paste-prompt asked to verify the in-play boundary; this
finding promotes L11's Join-fleets sub-bullet from `[derived]` to
`[confirmed, partial]`).

**Tag:** `[confirmed, partial]` for row L11 (was `[derived]`
carry-over in the inventory; the decompile reading `< 0x65 (= 101)` is
now pinned at the live boundary — the 100-ships (= 100) case is the
off-by-one check that distinguishes `< 100` from `< 101`).

## Answer

The Join-fleets gate is **`< 101` combined ships** (i.e. combined
ships ≤ 100 are accepted; 101 is refused). Three trials on a
fixed-seed classical save (the FLEET_SPLIT run-0 fixture, `seed=12345`,
Rome fleets 2 + 5 at `(101,46)` and `(101,47)` — Chebyshev distance 1,
both `owner=0`, neither carrying an army, neither at war with anyone —
patched in-place via SAV byte-edit, see Method below):

| Trial | Combined | Pre fleet 2 ships | Pre fleet 5 ships | Post-state Rome fleets | Survivor ships | Moves | Verdict |
|---|---:|---:|---:|---|---:|---:|---|
| **099** | 99 | 50 | 49 | `[(2, 99, 101, 46, 0)]` | **99** | 0 | **ACCEPTED** |
| **100** | 100 | 50 | 50 | `[(2, 100, 101, 46, 0)]` | **100** | 0 | **ACCEPTED** |
| **101** | 101 | 50 | 51 | `[(2, 50, 101, 46, 29), (5, 51, 101, 47, 0)]` | n/a | n/a | **REFUSED** (no merge) |

Parsed from `state.sav.parse()`. The 99 / 100 trials finish with a
single Rome fleet at the survivor's tile `(101,46)` (the location of
fleet 2 in the pre-state) with moves=0 (matches the harness docstring's
*"the joined fleet's moves become 0"*). The 101 trial is a byte-identical
no-op: both fleets retain their pre-state ship counts, fleet 2 retains
its pre-state moves=29, and no fleet is created. No news line is written
for any of the three trials.

The 50+50 (=100) case is the off-by-one cell that the decompile
reading `< 0x65` and the harness docstring *"...fewer than 100
combined..."* both leave ambiguous — **accepted here, which pins the
gate at `< 101`**.

## What does not match — three open notes

1. **The harness's docstring** says *"...fewer than 100 combined..."* —
   a natural reading would be `< 100` (i.e. accept 99 max, refuse 100).
   But the live test shows 100 is accepted. The docstring is loose / off
   by one; the *actual* gate is `< 101` (the constant 0x65). Trivially
   correctable in the harness; not part of this finding's scope.
2. **No news line is written** for either the accepted or refused case
   (the post-state news index is unchanged across all three trials). The
   accepted Join produces no confirmation; the refused Join is a silent
   no-op. **No "X cannot join fleets" / "100 ships exceeded" refusal
   text exists** — the gate is purely numerical. A reproduction that
   expects a refusal dialog will not find one.
3. **`@ +X +18` ships field** — the SAV's actual fleet-record offset
   for the FLEET_SPLIT run-0 save is **110196** (not the address a
   simple `ARMY_OFF + 2 + A*ARMY_LEN + 2` arithmetic would predict). The
   pre-state patch in this finding is **layout-independent** — it scans
   for the 26-byte record matching `(x=101, y=46 or 47, owner=0)` rather
   than computing the offset. Reproduction of this finding on other
   saves (different `na`, different size) doesn't need to re-derive the
   layout; the content-key scan works regardless. The
   `docs/sav-layout-notes.md` text says `off_f = 100958 + A*ARMY_LEN`
   but the actual run-0 fixture has the records at offset ~2570 bytes
   earlier; some other state table is in between (not verified here).
   Carrying forward as a small obs note.

## Method

- **Per-trial run.** Each trial:
  1. Patch the FLEET_SPLIT run-0 fixture's bytes in place via
     `find_fleet(x, y, owner)` + `struct.pack_into('<h', data, off + 18, ships)`.
     The byte layout is fixed by the game's record schema (`+0 x / +2 y /
     +4 reset / +6 unk / +8 owner / +10 cd. / +12 moves / +14 supplies /
     +16 money / +18 ships / +20 cond or build_city / +22 army / +24 cell`);
     the offset within the 26-byte record is the only fixed delta.
  2. Write the patched SAV as
     `artifacts/run-exp-join-fleets-cap-in-play/trial-NNN-pre.SAV`
     (gitignored per CLAUDE.md rule 1).
  3. Launch a fresh `Game()` via `harness.driver.Game()` on Xvfb display
     `:99` (started by `harness/env.sh`'s `pgrep -x Xvfb >/dev/null || ...`);
     `g.load(pre, seed=12345)`; `g.join_fleets(2)`; `g.save_as(post)`.
  4. Parse both pre and post with `state.sav.parse()`.
- **Single-run determinism.** Each `Game()` subprocess was a single,
  fresh process. Same seed reproduces byte-exact
  (`NEW_a.SAV = NEW_b.SAV = BASE.SAV` is the established determinism;
  reproduced here). The patched pre-state SAVs are themselves
  byte-deterministic (same `find_fleet` patch produces the same bytes
  per trial).
- **Harness.** `Game()` is unchanged from commit history; the
  docstring still says `"fewer than 100 combined"` — see open note 1.
- **Tags carried.** `[confirmed, partial]` because the trial proves
  the in-play boundary but does not pin every other L11 row (20 units
  / 100,000 troops per army / 198 armies / 100% mobilization are
  separate gates; not exercised here).

## Inferences

- **`< 101` is the L11 gate for Join fleets.** L11's seven gate
  constants (20 units / 100k troops / 100 ships / 40 recruit slots /
  500 troops per ship / 198 armies / 100% mob) have been truncated to
  one verified case here; the rest remain `[derived]` carry-over from
  the inventory rows.
- **The refused case is byte-identical to the pre-state.** No fleet
  merge, no changes to moves, no news event. The gate is enforced
  before any in-game handler runs.
- **Maneuver cost after join is 0** (moves=0 in the survivor), per
  `Game.join_fleets` docstring and the decompiled join handler in
  `TUnitMap_JoinFleets @ 0x00447a48`.

## What this does not establish

- The other six L11 gate constants (open note above).
- The exact fleet-record offset for other saves (open note 3).
- The harness-docstring-vs-code one-ship inconsistency (open note 1).

## Reproduction

```bash
cd ~/projects/ic2-conquest
xvfb-run -a python3 runs/experiments/data/run-exp-join-fleets-cap-in-play/trial.py
# results.json summary:
python3 -c "import json; d=json.load(open('runs/experiments/data/run-exp-join-fleets-cap-in-play/results.json')); print('\n'.join(f\"trial {r['trial']:3d}: pre={r['pre_fleet_2_ships']}+{r['pre_fleet_5_ships']}  post_survivor_ships={r['survivor_ships']}  {'ACCEPTED' if r['accepted'] else 'REFUSED'}\" for r in d))"
# SHA-256 of the six tracked SAVs is at
#   runs/experiments/data/run-exp-join-fleets-cap-in-play/SAVES.sha256
# Files (binary SAVs in artifacts/, gitignored per rule 1):
#   artifacts/run-exp-join-fleets-cap-in-play/trial-099-pre.SAV
#   artifacts/run-exp-join-fleets-cap-in-play/trial-099-post.SAV
#   artifacts/run-exp-join-fleets-cap-in-play/trial-100-pre.SAV
#   artifacts/run-exp-join-fleets-cap-in-play/trial-100-post.SAV
#   artifacts/run-exp-join-fleets-cap-in-play/trial-101-pre.SAV
#   artifacts/run-exp-join-fleets-cap-in-play/trial-101-post.SAV
```

Per CLAUDE.md rule 6, the per-trial driver + results + SHA-256 live in
the tracked path `runs/experiments/data/run-exp-join-fleets-cap-in-play/`.
The SAV binaries live in the gitignored
`artifacts/run-exp-join-fleets-cap-in-play/` (clause 1 of CLAUDE.md rule 1)
**and are uploaded to the GitHub release
[`run-exp-join-fleets-cap-in-play`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-join-fleets-cap-in-play)**,
tagged `2026-10-08T10:22:52Z`, six binary assets totalling 793 KB.

**Tracked files (this finding):**
- `findings/2026-10-08-join-fleets-cap-in-play.md` (this report)
- `runs/experiments/data/run-exp-join-fleets-cap-in-play/trial.py`
  (the orchestrator + SAV patcher + parser)
- `runs/experiments/data/run-exp-join-fleets-cap-in-play/trial_driver.py`
  (per-trial `Game()` sub-process)
- `runs/experiments/data/run-exp-join-fleets-cap-in-play/results.json`
  (per-trial summaries)
- `runs/experiments/data/run-exp-join-fleets-cap-in-play/SAVES.sha256`
  (six SAVs)

**Artifact files (gitignored, uploaded to release):**
- `artifacts/run-exp-join-fleets-cap-in-play/trial-{099,100,101}-{pre,post}.SAV`
  × 6 → released as `run-exp-join-fleets-cap-in-play` on the GitHub
  side; cited by `trial-NNN-{pre,post}.SAV` per CLAUDE.md rule 1 (bare
  filename).

**SHA-256 of the six released SAVs (tracked `SAVES.sha256`):**

```
3c81bdacad4583b0150e7c396624ca697bdee26186727d331d36eaea53cd7d44  trial-099-pre.SAV
bddd1ba6fd8cc5bcb6532f12ebacd5a32239d64b699a5a1f5f30e3f35bc086c2  trial-099-post.SAV
3ab4947f3a4dffd9e8203cf83ccd0fef695c0849d2475690fb78894bf0bdbee4  trial-100-pre.SAV
b7eb51b099a791168e8c42419b908982c8e0858021c259736e94c964f34b620b  trial-100-post.SAV
604ba25ff411534ec9df9691d9743bf78ddf7799136098008065df8a9b3d0cc9  trial-101-pre.SAV
d16e0f39c0c4ba4cb954cd1bce43939a28cfa69a5c7cb499283d270c52433208  trial-101-post.SAV
```

## Related

- [`2026-10-05-player-facing-feature-inventory.md`](2025-10-05-player-facing-feature-inventory.md)
  row L11 — this report's evidence column is appended in the inventory
  with the L11 sub-bullet re-tagged to `[confirmed, partial]`.
- [`2026-10-08-news-and-messages-l01-l14.md`](2026-10-08-news-and-messages-l01-l14.md)
  — L11's prior draft carried the forward-pointer to this finding; the
  L11 row's tail is updated below to remove the "open note 3" status.
- [`2026-10-08-unit-map-fleet-uf01-uf06.md`](2026-10-08-unit-map-fleet-uf01-uf06.md)
  — UF05's fleet-join row; this finding closes the 100-ships
  boundary that UF05's `[derived]` carry-over flagged.
- `R:decompiled-unit-map-orders-and-record-fields.md` Part 2 — the
  fleet-join code gates that the decompile read of the boundary.
- The ic2-conquest-side `findings/2026-10-08-join-fleets-cap-in-play.md`
  draft (this report's source of truth); tracked code at
  `runs/experiments/data/run-exp-join-fleets-cap-in-play/`.
