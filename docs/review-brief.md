# Review briefs

Every review brief written in this project carries the section below. That covers a reviewer's
brief file, or a review-request PR body. Owner's rule of 2026-10-04.

- **Where:** paste the section in full, right after the brief's "Blocking means" section. Briefs
  reach the reviewer as a file, so paste the text itself; never point to where it came from.
- **Why:** in ic2-conquest PR #38 (2026-10-04) a reviewer asked for rework eight times, naming
  exactly one blocking finding per round. Every finding was valid, and most were visible in the
  first round. One review that lists everything costs far less than one review per finding.
- **Two-rounds rule:** if a reviewer still reports one blocker per round, stop after the second such
  round. Before the next review, go through the whole diff yourself for the same class of problem,
  and record the pattern on the PR.
- **Which model reviews:** the user picks it at every review (`CLAUDE.md`, rule 2). Its family must
  differ from the implementer's.

## Running an OpenCode review (since 2026-10-11)

- **Use the reviewer agent:** `opencode run --agent reviewer -m <model> --dir <review worktree>`,
  in the background with stdin from a file (`< /dev/null`), watched under rules 8-13. The agent
  (`.opencode/agents/reviewer.md`) denies edits, commits, pushes, comments and merges, and opens
  `/tmp` for scratch.
- **Outside files:** anything the reviewer must read from outside its worktree and `/tmp` (the dump
  under `/mnt/c/...`, logs, another repo) is copied into the worktree (git-excluded) or into a
  `/tmp` folder before the run, and the brief points there. Never widen the permission to the
  outside folder.
- **A refused call:** stop after the first refusal and fix the cause (the agent's permissions or
  the brief's run rules), then resume the same session (`--session <ses_...>`). Never retry the
  same model with a reworded brief. On 2026-10-11 the PR #12 review was refused twice, first on
  `/tmp` and then on `cd release` plus a `../` path.

## The run rules, to paste at the top of every OpenCode brief, before the task text

```
## Run rules

1. Never `cd`, and never write `..`: run every command from the worktree root with relative
   paths. OpenCode resolves `cd X && ...` and `../...` against the worktree and refuses anything
   that lands outside it.
2. /tmp is open to you: use it freely for scratch files, your own scripts and a TMPDIR
   (e.g. /tmp/ic2r-review-<pr>).
3. Run commands directly, one per call (with `TMPDIR=<folder>` in front where it matters), not
   through a wrapper script you write. Your own parsers for reading saves are fine: run them as
   `python3 -I /tmp/<folder>/<script>.py <file>`.
```

## The section, to paste

```
## Report every blocking finding in this one review

This review is your only pass before the author fixes. Do not stop at the first blocking
finding: finish reading the whole diff and the task file, check every Done-when line and
every item under "Blocking means", and report all blocking findings together.

- Before you write the verdict, make one last pass over the full diff for anything you have
  not yet rated, and say "Final pass done" as the last line before the verdict.
- Number the findings R1, R2, … in order of severity. A finding you held back because an
  earlier one was already blocking is a review defect: if two problems share a cause, list
  both and say so.
- Do not rely on a later round. The author fixes everything you list, and the next review
  checks those fixes and new code only, not anything you saw but did not report.
- If you ran out of time or context before covering the whole diff, say which files or
  sections you did not cover. Do not approve in that case.
```
