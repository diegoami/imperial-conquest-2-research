# Environment

## Starting in Codex or Claude Code

`CLAUDE.md` is the shared repository policy. Claude Code loads it through its normal
entry point; Codex loads `AGENTS.md`, which instructs it to read the same file. The intake
skill stays in `.claude/skills/retrieve-findings/`; `.agents/skills/retrieve-findings`
links to that directory for Codex discovery. No global Codex fallback configuration is
required. Restart an existing Codex session after adding the entry point.

Read `docs/handover.md` for dated research state and `docs/pending-requests.md` for open
requests. Check current state with `git status -sb`, `git worktree list` and
`git log -1 --oneline`; fetch before comparing with origin when network access is available.
Do not assume an old HEAD or preserved worktree still exists.

Use `gh auth status` to check GitHub access without displaying credentials. Quota-tracker
is optional: `curl -fsS --max-time 3 'http://localhost:8765/recommend?tier=light'` (or
`tier=heavy`) supplies a suggestion only. If unavailable, continue without a suggestion.
Do not read credentials or depend on another client's global instructions to recover it.

Identify the active model from the current client's session information. The
`ANTHROPIC_*` variables in the handover concern Claude Code provider routing, not Codex's
model identity. Record only a model identity that is actually exposed; do not guess it.
An OpenAI implementer requires a reviewer from another model family under `CLAUDE.md`.
Model selection remains the user's choice, including after provider exhaustion.

Claude memory, `ListAgents`, `SendMessage` and the Claude Agent tool are client-specific.
Codex's local subagents are not the separate ic2-conquest peer session. Use peer discovery
and messaging only when equivalent tools are actually available and the communication is
authorized. Otherwise, use the repository's reports and ledger for context and give the
user concrete request or acknowledgment text to relay. Do not invent a socket address or
post to GitHub as a substitute for messaging.

## Validation and evidence access

There is no application build or package install for this research repository. Python 3
and Bash run the checked-in analysis scripts; `gh` supplies GitHub reads. For process-only
edits, check `git diff --check`, relative documentation links and skill discovery. For
script changes, run the relevant checker on its documented inputs and report unavailable
evidence explicitly. `bash -n scripts/pending-drafts.sh` checks shell syntax without
network access. Python syntax can be checked without executing the evidence readers:

```bash
python3 -c 'import ast, pathlib; [ast.parse(p.read_text(), filename=str(p)) for p in pathlib.Path("scripts").rglob("*.py")]'
```

Most analysis scripts need external saves, trial JSON or original game files. Retrieve
evidence using `docs/evidence-index.md`; keep binaries and decompilation output out of git.
`scripts/ai-turn-intake-check.py` also needs ic2-conquest's parser: pass its checkout as the
second argument when it is not a sibling of this worktree. Missing local dumps or private
release access must remain stated verification limits.

Review briefs follow `docs/review-brief.md`. `.opencode/agents/reviewer.md` configures
OpenCode only; it does not enforce permissions in Codex. If Codex is the selected reviewer,
use its available read-only sandbox configuration and the same complete-review brief.
Do not launch a review that depends on unavailable isolation or invent a review result.

## Model quota and choice: quota-tracker

For Claude Code, the owner's global instructions (`~/.claude/CLAUDE.md`, section "Model quota availability:
quota-tracker") are the reference for the quota-tracker service, its endpoints, the models per
provider, free models, time-of-day pricing and what to do when the service is down. This file
does not copy them, because copies go stale (the model table here listed DeepSeek after it was
blacklisted). Codex does not need that global file; the portable steps above and the shared
repository policy apply independently.

**Who chooses:** the user (`CLAUDE.md`, "Choosing models: the user decides", 2026-10-11). Here the
quota service gives only the suggestion shown with each question (`/recommend?tier=heavy|light`). If
it doesn't answer (`curl -sf localhost:8765/health`), ask without one.

*Superseded 2026-10-11, kept as history:* the earlier short version (CLAUDE.md L50/L51) chose the
model itself. It followed `/recommend`'s `rank` and `pair`, moved to the next model of the chain when
a provider was exhausted, and used `openai/gpt-5.6-luna` (effort high) as the default reviewer. None
of these choose a model any more.

Still in force:
- Model ids come from `opencode models <provider>`, never memory.
- DeepSeek is never used, and Alibaba only when the user asks.
- Never read `~/.config/quota-tracker/config.toml` or any OpenCode `auth.json`.

## This repo in particular
- Claude Code sessions here run on the model the session was started with. Its local
  `.claude/settings.local.json` may contain provider routing and credentials: leave it alone,
  including in Codex sessions. The handover's non-Claude-backend guidance concerns Claude Code
  routed through another provider; apply a `non-claude-backend` skill only if available.
- On this machine (2026-10-11): the full Ghidra dump at
  `/mnt/c/Users/diego/AppData/Local/ReTools/all_app_functions.txt`, and Wine 10.0. Not on it: Ghidra
  itself and .NET (the remake CLI can't be run). Pillow comes through `uv run -q --no-project --with pillow python -I -`.
