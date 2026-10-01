---
name: retrieve-findings
description: Pull new rule-discovery drafts from the ic2-conquest bot repository, review them against the code and saves, and promote them into docs/reports. Use when asked to retrieve, sync, intake or promote findings from ic2-conquest.
---

# Retrieve findings from ic2-conquest

`ic2-conquest` (local clone `../ic2-conquest`, remote `diegoami/ic2-conquest`) plays the original game headless and drafts discoveries in `findings/`. This repo is the gate: nothing enters `docs/reports/` unreviewed. **Never write to ic2-conquest**; everything below is read-only there. State lives in `docs/findings-intake.md`.

## 1. Find candidates

```bash
cd ../ic2-conquest && git fetch --all --prune
for r in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin); do
  git ls-tree -r --name-only $r -- findings/ | grep -v -e README -e PROMPT | sed "s|^|$r |"
done | sort -k2 -u
```

Drafts can sit on feature branches that are not merged, so scan every remote branch, and read a draft from the newest branch that has it (`git show <ref>:findings/<file>`). Drop every path already in the ledger with the same reviewed commit or blob. The rest are candidates.

Also skim, without promoting anything: `HANDOVER.md`, `coverage.md`, `tests/results.md` and `runs/experiments/*` for facts about the rules that have no draft yet. List them for the user as "possible future findings"; the bot drafts them, not you.

If there are no candidates, say so and stop.

## 2. Review each candidate

A draft is a claim, not evidence. For each one:

- **Cited saves**: each bare filename must resolve in `docs/evidence-index.md`, or in ic2-conquest's `saves/README.md` / release `run-<id>`. A claim with no retrievable save and no code corroboration is `deferred`. If the draft is honest that it is Wine-only or its saves are unpublished and the claims are consistent with existing reports, promote it as `promoted, provisional`: the status line says what is missing, and the ledger row names the follow-up (publish the release, add to `evidence-index.md`).
- **Code claims** (addresses, function names): re-check against the Ghidra dumps on the researcher's machine when they are available (see README, Toolchain); say in the report when you could not.
- **Overlap**: `grep -ril` the key terms in `docs/reports/`. A draft may confirm, extend, or contradict an existing report. Contradictions are the valuable ones: fix the old report's sentence and link the new one (see how `2026-09-29-loading-a-save-does-not-reseed.md` corrected the battle feasibility report).
- **Scope**: keep "What this does not establish" honest. Do not promote an inference as an observation.

## 3. Promote

1. Write `docs/reports/<date>-<slug>.md` (the draft's own name is usually right; keep the draft's Method / Observations / Inferences structure). Change the Status line from "draft … awaiting promotion" to a statement of provenance: the draft's repo, branch and commit.
2. Edit existing reports the finding touches: a one-line cross-link or correction, not a rewrite.
3. New saves go into `docs/evidence-index.md`; bare filenames only, no binaries in git.
4. Update the report count in `README.md` if it states one.
5. Add a row to `docs/findings-intake.md`, including for rejected and deferred drafts, so they are not re-reviewed.
6. Commit with a body listing each draft, what was corrected, and `Drafts from diegoami/ic2-conquest, branch <b>, commit <sha>`. Do not push unless asked.

## 4. Report to the user

For each candidate: outcome, what you corrected or could not verify, which existing reports changed. Mention that ic2-conquest still lists the draft: the player removes or marks it there, since this session must not write to that repo.

## Daily check

`.github/workflows/pending-drafts.yml` runs `scripts/pending-drafts.sh` every day and keeps one issue, "Pending ic2-conquest findings drafts", open while any draft is unledgered or changed since its reviewed commit; it closes the issue at zero. It reads ic2-conquest through the GitHub API only. Run the same script locally for step 1: `bash scripts/pending-drafts.sh`. It replaces the manual loop above and is the quickest way to see the queue.
