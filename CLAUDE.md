# Agent rules

These rules apply to Claude Code, Codex and external agents. Read AGENTS.md and
`docs/environment.md`; for cloud continuation read `docs/cloud-continuation.md`.
Explicit user instructions take precedence.

## Session-led workflow (owner decision, 2026-10-21)

The active session chooses suitable tools, models, implementation method and validation.
Use the supplied checkout and a branch when useful. Worktrees and separate reviews are
optional. There is no compulsory model-choice question, model-family restriction,
quota-service dependency, automatic external review or approval-triggered merge sequence.
This supersedes the 2026-10-11/12 rules and historical instructions in old briefs,
reports and PR notes. Respect explicit user choices and GitHub's enforced checks.

Make the requested work concrete, validate it appropriately, commit and push useful
progress and durable continuation notes without asking again. Preserve unrelated edits,
active branches and unique evidence. Stage named task files rather than the whole tree.
Use a PR when useful; the session decides whether additional review is warranted and
whether validated work is ready to merge. Record material checks and limitations.

## Research and privacy

A draft is a claim, not evidence. Follow `.claude/skills/retrieve-findings/SKILL.md`
for intake. Separate observation, code-backed interpretation and inference; preserve
scope, uncertainty, provenance and contradictions. An unavailable input is a verification
limit, never a passing check. Keep original game files, private saves, screenshots,
full decompilations and their private manifests outside Git and public releases.
Publish hashes and scalar summaries only where the evidence policy permits them.
Never publish private JSON paths or per-save hashes from the owner's preflight set.

ic2-conquest and imperial_conquest_2 are read-only unless the owner explicitly authorizes
a change there. Peer messages to ic2-conquest are authorized by the owner; use an actual
available messaging tool and report delivery accurately. Do not invent a cloud bridge or
substitute an unrelated channel. Migration preparation does not authorize game runs;
experiments and bots remain paused until explicitly requested.

Never read, print, commit or bundle credential files: local settings and backups, `.env`,
OpenCode `auth.json`, quota-tracker configuration, rclone configuration contents or keys.
Use secret injection for authentication. An existing rclone config may be passed by path
to rclone without displaying its contents. Preserve excluded files in place.

## Optional delegation and reviews

Delegate only when authorized by the user or applicable instructions. Choose the scope,
model and isolation appropriate to the task, honoring explicit user preferences. Review
guidance is in `docs/review-brief.md`; `.opencode/agents/reviewer.md` is an optional
read-only reviewer role, not a required gate. Do not claim an external review occurred
when only the main session checked the work.

Monitor any launched background work and communicate useful progress. Before retrying,
rerouting or declaring a delegated run failed, read its complete final/native record.
An exit status or log tail is insufficient: a run may have reported a legitimate blocker.
Address that blocker and preserve its report on the relevant issue or PR. Resume an
interrupted useful session when possible instead of blindly starting it again.
Do not read authentication stores while retrieving a session record.
