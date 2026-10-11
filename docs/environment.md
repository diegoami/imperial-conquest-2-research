# Environment

## Model quota and choice: quota-tracker

The owner's global instructions (`~/.claude/CLAUDE.md`, section "Model quota availability:
quota-tracker") are the reference for the quota-tracker service, its endpoints, the models per
provider, free models, time-of-day pricing and what to do when the service is down. This file
does not copy them, because copies go stale (the model table here listed DeepSeek after it was
blacklisted).

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
- Claude Code sessions here run on the model the session was started with. As of 2026-10-10,
  `.claude/settings.local.json` holds only permissions; it no longer routes the project to Z.ai's
  GLM. If a session does run on a non-Anthropic backend, the `non-claude-backend` skill covers it.
- On this machine (2026-10-11): the full Ghidra dump at
  `/mnt/c/Users/diego/AppData/Local/ReTools/all_app_functions.txt`, and Wine 10.0. Not on it: Ghidra
  itself and .NET (the remake CLI can't be run). Pillow comes through `uv run -q --no-project --with pillow python -I -`.
