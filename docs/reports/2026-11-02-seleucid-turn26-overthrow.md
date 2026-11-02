# Seleucid long run, turn 26: the human leader is overthrown in both games; the "freeze" was the end of the game

**Tag:** [confirmed: Wine + native Windows + remake replay] for the overthrow. The frozen battle window is Wine-only and
unexplained.
**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `eeeaf35c` (PR #309). It resolves the turn-26
item in [`2026-11-02-longrun-v090-ai-gaps.md`](2026-11-02-longrun-v090-ai-gaps.md) and
[`2026-11-02-remake-11f713e2-recheck.md`](2026-11-02-remake-11f713e2-recheck.md).
**Task:** owner 2026-11-02: why the Seleucid long run stops at turn 26, whether it's the original or the remake, and a native
Windows check.

## Result

At the start of turn 26 (Spring week 5, 269 BC) Seleucid, the bot's nation, has unity 402, 48 cities and wars with Ptolemaic,
Bithynia and Galatia (`seleucid-rulebot1-40t-r7/original/t26-a00.SAV`). After its End turn, **both games overthrow the human
leader**:

| Game | From `t26-a00.SAV` | Message |
|---|---|---|
| Original, Wine (`turn26-repro/wine-v1`) | End turn → `AUTO0746.SAV OK` → "End of Game" | "The game is over for Darius the leader of Seleucid. Your unpopularity has forced the army to overthrow you." Cities 62 (270 BC) → 47 (269 BC) |
| Original, **native Windows** (`turn26-repro/windows-v1`, same exe bytes) | End turn → `AUTO0746.SAV OK` → "End of Game" (modal, the other windows disabled), game responsive | the same |
| Remake `11f713e2` (`turn26-repro/remake-11f713e2-v1`) | `end` | "Your unpopularity has forced the army to overthrow you. Seleucid has been overthrown by the army and handed to the AI. Watch mode from here on." The same week and the same news (Sagalassus falls to Galatia) |

So the Seleucid game legitimately ends for the human at turn 26 in both games, and can't run to 40 turns. One presentation
difference: the original ends the game (End of Game), while the remake hands the nation to the AI and continues in watch mode.

## The frozen window in the long runs (Wine, harness)

In the campaign itself (r1–r7, fast and watch builds alike), the same End turn left an unpainted battle window "Ptolemaic v
Seleucid — Seleucid to move units" instead of End of Game:
- battle flag 0, seat 2, all threads idle in the message loop, no hidden window;
- `no_delay` is not the cause: the watch build stops the same way.

The single-turn replays (load `t26-a00`, write the `RandSeed` that the campaign logged before End turn, 3576117115) show no
battle. Two paint routines set `RandSeed` from map coordinates (`patches/seed_patch.py` notes), so a fresh load does not
reproduce the campaign's draws exactly. The likely sequence in the campaign: Ptolemaic attacks the human in the same turn as
the overthrow, and the overthrown human's defending battle is left open, with End of Game never shown. This was not
reproduced exactly; Wine against Windows on that exact sequence remains untested.

**Harness consequence:** a long-run game whose human is overthrown or conquered stops there. The driver's `end_turn` raises
`GameOver` only for an End of Game window that appears before the autosave line; both cases here show it after.

## Tools

- `runs/experiments/turn26/repro_wine.py`: load a save, write `RandSeed`, End turn; then windows, flag, seat, screenshot.
- `runs/experiments/turn26/repro_windows.py`: the same natively, with Windows Python and ctypes. Menus are driven by
  WM_COMMAND, memory through Read/WriteProcessMemory, screenshots with PowerShell. Folder
  `C:\Users\diego\Documents\ic2-turn26-repro`.
- `IC2_LOG_RANDSEED=1` (`difftest/original.py`): `RandSeed` before every action.
- `patches/watch_seed_build.py`: the seeded watch build.

## Review at intake

- **Wine and native Windows:** I read `turn26-repro/wine-v1/result.json` and `windows-v1/result.json`. Both runs:
  - load `t26-a00.SAV`, whose RandSeed after load is 4169717509;
  - write 3576117115, then End turn;
  - log `AUTO0746.SAV OK`;
  - finish with an `End of Game` window (class `THumanFalls` in the Windows window list), battle flag 0, seat 2, and
    the **same RandSeed afterwards, 380787481**.

  The Windows run records `responds: true` and `hung: false`, and it was driven from a Windows folder
  (`C:\Users\diego\Documents\ic2-turn26-repro`).
- **Remake:** the receipt (`remake-11f713e2-v1/receipt.jsonl`) has "Your unpopularity has forced the army to overthrow
  you", "handed to the AI. Watch mode from here on" and "Sagalassus (Seleucid) falls to Galatia".
- **Closed after intake** (conquest `36a4309e`, PR #310):
  - **Same executable:** I hashed both copies myself, the Windows folder's and the Wine game folder's. Both are sha256
    `354d8265cba1dac2a80a0a96ce76367a368e37a4e79c30eb4f0bb587b35c532f`, as `turn26-repro/exe-sha256.txt` records.
  - **Message text:** I viewed both screenshots from `turn26-repro-saves-v2.tar.gz` (`wine-v1/after.png`,
    `windows-v1/after-game-only.png`). Both show "The game is over for Darius the leader of Seleucid. Your unpopularity
    has forced the army to overthrow you." They also show the changes panel: 270 BC with population 16,944,000, 62 cities
    and 2,700 talents; 269 BC with 13,767,000, 47 cities and 6,308 talents. This matches `end-of-game-text.txt`.
  - **Asset name:** the release asset is now `turn26-repro-saves-v2.tar.gz`. The first Windows screenshot captured the
    whole desktop, so conquest replaced it with a crop of the game window and deleted the old tarball.
- **Scope:**
  - **Established:** from `t26-a00` with the campaign's logged seed, End turn overthrows the human in all three runs.
  - **Inferred, not reproduced:** that the campaign's unpainted battle window comes from the same turn's overthrow.
    The campaign's own draws were not reproduced, so Wine and native Windows on that exact sequence are still
    untested.
  - **A remake difference to note:** the original ends the game for the human, while the remake continues in watch
    mode. Whether watch mode is a deliberate remake choice is for the remake to say.

