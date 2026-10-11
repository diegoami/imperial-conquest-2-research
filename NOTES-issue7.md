# Notes for research issue #7 (AI merge decompile)

## Plan
1. Read `FUN_004509f0` (:53949) and `FUN_00450b30` (:54002) and every helper and caller.
2. Write `docs/reports/2026-10-11-decompiled-ai-merge-armies-and-fleets.md` with tagged findings, verbatim excerpts, Not established, Reproduction.
3. Correct §2.4 of `2026-10-07-strategic-ai-turn.md`, the two spec bullets in `docs/rules-specification.md`, add a pointer to row 13 of the purse report.
4. README count 168 to 169; add the intake row.
5. Push, open PR against main. Do not merge, do not touch issue #7.

## Progress
- Commit 1: new report, the corrections, README count, intake row, these notes.
- Commit 2: END block with the PR URL.
- Commit 3: review fixes R1-R6, a, b (Sol): owner gate, fleet fall-through, same-tile settled (A13), compaction timing (C2), slot-0 donor (A12), spec local tags.

## END
Done: all four points of the issue established; report, corrections and review fixes R1-R6, a, b applied (PR #9 updated).
Open (Not established): whether a donor with slot-0 troops <= 0 and another occupied slot can exist (A12 says what the function does with one); no save-pair observation of the merges; `+0xA` countdown range quoted, not re-read; fleet `+4`/`+6` unidentified.
PR: https://github.com/diegoami/imperial-conquest-2-research/pull/9
