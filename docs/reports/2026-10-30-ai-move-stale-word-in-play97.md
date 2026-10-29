# In play, the original's AI move always walked again: the stale word it tests was never −1

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `5275b9e` (PR #245). This
answers research issue [#97](https://github.com/diegoami/imperial-conquest-2-research/issues/97)
(for remake [#1585](https://github.com/diegoami/imperial_conquest_2/issues/1585)), which was
delegated to conquest on 2026-10-29. Release
[`run-exp-walk-hook97`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-walk-hook97);
the data is committed at `runs/experiments/data/run-exp-walk-hook97/`. It follows
[`2026-10-30-ai-march-continuation-missing-in-remake.md`](2026-10-30-ai-march-continuation-missing-in-remake.md).

**Tag:** `[confirmed, partial]`: observed in the running original under Wine with an
observation-only hook, over 5 starts × 5 AI End turns with seed 12345. Not run on native Windows.

**Review note (2026-10-29):**
- **Release integrity:** all 54 saves match `SAVES.sha256`.
- **Inertness:** I compared every hooked autosave with its plain counterpart myself, and all 27
  pairs are byte-identical (25 from the five starts and 2 from the `BASE.SAV` smoke run). The hook
  changes no game state that the autosaves record.
- **Every count recomputed** from the five `t5/*-walk.jsonl` files (666 records):
  - **A (AI moves past the fleet branch):** 424, of which 346 took the direct path and 78 the
    intermediate path.
  - **`[ebp-0xa]` at entry, direct path:** 49 (207), 71 (133), 0 (6). It was **never −1**.
  - **`[ebp-0xa]` at entry, intermediate path,** before `FUN_0044db38` writes it: 49 (49),
    71 (19), 0 (10).
  - **B (recursion tests):** 152. Linked to their frame's A record, 131 are on the direct path and
    21 on the intermediate path, and every one passed. The lowest word seen is 0.
  - **C (no-progress tests):** 90, all on the direct path, all passed. The lowest word is 0.
  - **Moves left at B:** 1 (6), 2 (13), 3 (18), 4 (16), 5 (83), 6 (12), 7 (4).
  - **A records by return site:** recursion 152, `0x44f47c` 117, `0x44f43f` 52, `0x44f409` 49,
    `0x44f2f9` (intercept) 23, `0x44e913` 12, `0x44f4c7` 10, `0x44f4a3` 5, `0x44ec7d` 2,
    `0x44ecd6` 2.
  - All of these match the draft.
- **Correction (a side detail).** The draft says the B tests "were reached mostly within recursive
  calls (138)". That is wrong. Linking each B record to its own frame's A record, only **11** B
  tests occur inside a recursive frame. The other **141** occur in top-level frames: `0x44f47c` 93,
  `0x44f43f` 18, `0x44f409` 15, `0x44f2f9` 11, `0x44e913` 2, `0x44ecd6` 1, `0x44ec7d` 1. The B
  records' own caller field gives the same split. The main result is unaffected.
- **Call sites: research's earlier list was incomplete.** The disassembly has **10** calls into
  `0x44dba8` plus the self-call at `0x44dca1`. The 10th is `0x44f4c7`, a move to a city's
  coordinates, which my list in the AI march report had missed: I had cut the scan output short.
  The AI march report is corrected. `0x44f2e7` (intercept toward the capital) was not seen in play.
- **The hook design** is the draft's: probe A wraps the call to `FUN_0044cb40` at `0x44dc06`, and
  probes B and C replace the tests at `0x44dc8c` and `0x44dc4d`, each saving and restoring EFLAGS
  and all registers. I did not re-read `patches/walk_hook.py` byte by byte. The identical autosaves
  are the inertness evidence.

## Answer

In 25 AI End turns of real play, the stale word that `FUN_0044dba8` tests on its direct-line path
held 49, 71 or 0, and was never −1. Every recursion test (152) and every no-progress test (90)
passed. So in these turns, the original's AI **always walked again** when a walk ended more than 1
short of the target with moves left, on either path.

Research's x86 replay showed that both outcomes are possible in principle: a stale −1 gives one walk
(the remake's result), and a stale 0 gives recursion. In play, only the second occurred.

**Consequence.** In the AI march report, the bracket for the share of AI marches that end
differently in the original (0.5–28%) collapses to its upper end. **About 28% of the remake's AI
marches stop where the original's AI would walk on.** This still assumes the original takes the
same path as the remake's AI.

## What this does not establish

- That the word can never be −1 in play. This covers one seed, 5 starts and 5 turns; the value is
  whatever earlier calls left in that stack slot.
- Which earlier routine leaves 49, 71 or 0 there.
- That the original takes the same path as the remake's AI for the same march.
- Native Windows behaviour.

## Evidence

- **Data:** `runs/experiments/data/run-exp-walk-hook97/`:
  - `t5/<start>-walk.jsonl` (decoded records with the turn);
  - `t5/summary-v1.txt`;
  - `t5/<start>/inert.json`.
- **Saves:** `t5/<start>/hooked-tNN-AUTOnnnn.SAV` and `plain-tNN-…`, in release
  `run-exp-walk-hook97`. The starts are the Rome, Carthage, Gaul, Seleucid and Armenia New Game
  starts.
- **Hooked build:** `patches/walk_hook.py`, applied to `Imperial Conquest 2 fast rollingsave
  seed.exe` (`354d8265…`).
