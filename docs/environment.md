# Environment

## Model quota and choice: quota-tracker

The owner's global instructions (`~/.claude/CLAUDE.md`, section "Model quota availability:
quota-tracker") are the reference for the quota-tracker service, its endpoints, the models per
provider, free models, time-of-day pricing and what to do when the service is down. This file
does not copy them, because copies go stale (the model table here listed DeepSeek after it was
blacklisted).

The short version, for choosing or delegating a model (CLAUDE.md L50/L51):
- `curl -sf localhost:8765/health` first; if it fails, follow the global instructions.
- `curl -s 'localhost:8765/recommend?tier=heavy'` (or `tier=light`): follow `rank`; `pair` gives an
  implementer and a reviewer of a different family. `tight` rows are usable, `skipped` rows are not.
- Model ids come from `opencode models <provider>`, never memory.
- DeepSeek (any route) is blacklisted and Alibaba is not used, unless the owner asks.
- The default reviewer is `openai/gpt-5.6-luna`, effort `high`.
- Never read `~/.config/quota-tracker/config.toml` or any OpenCode `auth.json`.

## This repo in particular
- Claude Code sessions here run on the model the session was started with. As of 2026-10-10,
  `.claude/settings.local.json` holds only permissions; it no longer routes the project to Z.ai's
  GLM. If a session does run on a non-Anthropic backend, the `non-claude-backend` skill covers it.
- Not on this machine (2026-10-10): Ghidra, the full dump, Wine and .NET (the remake CLI can't be
  run). Pillow comes through `uv run -q --no-project --with pillow python -I -`.
