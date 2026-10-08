# Naval battle: the loser's tile word goes to 0, and the survivors are re-banded

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commits
`41b3b08` + `c73c938`. There was no new play: the saves are those of release
[`run-exp-naval-battle`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-naval-battle)
(already indexed here, from [`2026-10-02-naval-battles.md`](2026-10-02-naval-battles.md)) and the
fixture `saves/fleets-adjacent-at-sea-0723.SAV`. The read-out, script and hashes are at
`runs/experiments/data/run-exp-naval-loser-word/`. Wine-only evidence. It answers the piece left
open in [`2026-10-08-split-and-transfer-reband-fleets.md`](2026-10-08-split-and-transfer-reband-fleets.md):
whether tombstoning a losing fleet (`FUN_0044ad38`) clears its map word.

**Review note:**
- **Hashes.** The nine release saves and the fixture were downloaded and checked against
  `run-exp-naval-loser-word/SAVES.sha256` (all match).
- **Independent read-out.** The map words at (110,73), (111,73) and (111,74) were read with a separate
  reader (save offset x × 280 + y × 2), not the bot's script. Every value agrees with the table below.
- **What 0 means here.** The empty sea tile (111,74) also reads 0 in the fixture, so 0 is this sea's
  plain value. This supports the caveat below: on these tiles "cleared" and "covered terrain
  restored" look the same.
- **Agreement with the code reading.** The survivors' bands agree with `FUN_0044b4f8` ending in
  `FUN_0044A878` (`decompiled-diplomacy-peace-terms-and-instant-battles.md`).

**Tag:** `[confirmed]` for "the word goes to 0 at the loser's tile" and for the survivors' bands, on sea tiles.

## Answer

- **The loser's tile word becomes 0.** The losing fleet is tombstoned (owner −1), keeping its pre-battle ships field. All nine losing fleets (PROBE_AFTER and the NB_* cells: Ptolemaic fleet 1 in seven saves, Carthage fleet 0 in C50 and P60) had word 335 or 333 at their tile before the battle and **0** after.
- **The survivors are re-banded.** Every surviving fleet's word equals owner + band of its ships after the battle, for example:
  - Carthage fleet 0 at 81 ships: 333; at 40 ships: 317.
  - Ptolemaic fleet 1 at 54 ships: 335; at 48 ships: 319.
  - Carthage fleet 2 at 20 ships: 301.

  That is 15 surviving fleets across the 9 saves. It fits research's code reading, `FUN_0044b4f8` calling `FUN_0044A878` for the winning fleet.
- **Cleared or restored?** The covered-cell field (+24) of every fleet here is **0** (sea), so these saves cannot tell "the word is cleared to 0" from "the covered terrain is restored". On rough sea (covered cell 1) the two readings would differ (`[derived]`).

| Save | Loser (tile, word after) | Survivors: ships → word (expected) |
|---|---|---|
| fixture (before) | | f0 90 → 333 (333); f1 70 → 335 (335) |
| PROBE_AFTER | f1 (111,73): 0 | f0 80 → 333 |
| NB_C | f1: 0 | f0 81 → 333 |
| NB_C50 | f0 (110,73): 0 | f1 48 → 319; f2 40 → 317 |
| NB_C55 | f1: 0 | f0 40 → 317; f2 35 → 317 |
| NB_C60 | f1: 0 | f0 46 → 317; f2 30 → 317 |
| NB_C65 | f1: 0 | f0 53 → 333; f2 25 → 317 |
| NB_C70 | f1: 0 | f0 59 → 333; f2 20 → 301 |
| NB_P | f1: 0 | f0 72 → 333 |
| NB_P60 | f0: 0 | f1 54 → 335; f2 30 → 317 |

Every survivor's word matched its expected band.

Evidence: release `run-exp-naval-battle` (`PROBE_AFTER.SAV`, `NB_*_seed1.SAV`) and the fixture `saves/fleets-adjacent-at-sea-0723.SAV`; their SHA-256 and the read-out are in `runs/experiments/data/run-exp-naval-loser-word/` (`SAVES.sha256`, `naval_words.log`, `read_naval_words.py`).

## Not established

- A loser on rough sea, which would separate "cleared to 0" from "covered terrain restored".
- Storm losses in play (research's code reading covers them).
