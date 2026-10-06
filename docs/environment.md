# Environment

## Model quota availability: quota-tracker

A local service, quota-tracker, reports how much subscription quota is left on these
providers: claude, openai (ChatGPT plan, used via OpenCode), zai (GLM Coding Plan),
opencode_go (OpenCode Go), openrouter (prepaid credit), minimax (MiniMax Token Plan) and alibaba (Alibaba Token
Plan). Check it whenever you need
to know whether a provider can be used right now, before choosing, recommending or
delegating to a model.

### Querying (read-only, localhost, no auth, results cached 60 s)
- `curl -s localhost:8765/quota`: every provider
- `curl -s localhost:8765/quota/<provider>`: one provider
- `curl -s localhost:8765/best`: providers with quota left, most headroom first
- `curl -s localhost:8765/avoid`: providers out of quota, with when each is usable again
- Add `?refresh` to bypass the cache.

Each provider has:
- `status`: `ok` (under 80% used), `low` (80% or more), `exhausted` (95% or more:
  don't use until `available_at` / `available_in`), `error` (couldn't be checked;
  `error` says why), `not_configured`
- `headroom_pct`: percent left on its most-used window
- `windows[]`: every limit, with `name`, `used_pct`, `resets_at` (unix s), `resets_in`

### Usage history (what has been called, at what effort)
- `curl -s 'localhost:8765/usage?since=7d'`: per provider, the models called with
  `calls`, `sessions`, `tokens` and `effort` (reasoning-effort setting: Claude Code
  `effort`, OpenCode `variant`, Codex `effort`; `default` = none set)
- `curl -s 'localhost:8765/usage/sessions?since=7d&model=glm-5.3&effort=high'`: the
  sessions behind those calls, with `title`, `project`, `tool` and, for OpenCode,
  `data_dir` (harnesses run OpenCode with their own data dirs), and `launched_by`
  (the Claude Code session, title and project, when the run started from a Claude
  session's scratchpad). Filters: `provider`, `model`, `effort`; all optional.
- `since` accepts `90m`, `24h`, `7d`, `4w` or `all`. Sources are local logs (Claude
  Code, OpenCode, Codex, in WSL and on the Windows side; Windows OpenCode data can
  lag by up to an hour, and results are cached for 5 minutes); for zai, totals come from Z.ai's API, which also counts
  calls from other machines.

### Models per provider
| provider    | heavy                                             | light                                                 |
|-------------|---------------------------------------------------|-------------------------------------------------------|
| claude      | `claude --model opus`                             | `claude --model sonnet`                               |
| openai      | `opencode -m openai/gpt-6.1-sol`                  | `opencode -m openai/gpt-5.6-luna`                     |
| zai         | `opencode -m zai-coding-plan/glm-5.3`             | `opencode -m zai-coding-plan/glm-5.3-flash`           |
| opencode_go | `opencode -m opencode-go/deepseek-v4-pro`         | `opencode -m opencode-go/deepseek-v4.1-flash`         |
| openrouter  | `opencode -m openrouter/deepseek/deepseek-v4-pro` | `opencode -m openrouter/deepseek/deepseek-v4.1-flash` |
| alibaba: DeepSeek | `opencode -m alibaba-token-plan/deepseek-v4-pro-0813` | `opencode -m alibaba-token-plan/deepseek-v4.1-flash` |
| alibaba: Qwen     | `opencode -m alibaba-token-plan/qwen3.8-max`     | `opencode -m alibaba-token-plan/qwen3.8-flash`       |
| alibaba: GLM      | `opencode -m alibaba-token-plan/glm-5.3`         | none on Alibaba (zai has `glm-5.3-flash`)            |
| minimax           | `opencode -m minimax/MiniMax-M3`                 | `opencode -m minimax/MiniMax-M2.7`                   |

### Free models (OpenRouter): supplement only
For smaller tasks and additional reviews (a second opinion next to a regular model),
never as the main model for important work:
- `opencode -m openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`: the stronger one
- `opencode -m openrouter/cohere/north-mini-code:free`: coding-focused, faster
- also usable: `openrouter/thinkingmachines/inkling:free` (only through OpenCode, not the
  raw API) and `openrouter/poolside/laguna-s-2.1:free` (often rate-limited)

Cautions:
- Shared allowance of 1,000 requests/day and ~20/min across all free models; each agent
  step is one request. Remaining: `free_model_daily_requests` in `/quota/openrouter`.
- Free providers may log and train on prompts: don't send private or client code,
  secrets, or anything under NDA.
- Free models come and go and get rate-limited; on a 429, fall back instead of retrying.
- Check their output like any unreviewed contribution; they're tested only on small tasks.

Time-of-day pricing (`pricing` in `/quota/alibaba` and `/quota/zai`, computed from the
providers' published rules):
- alibaba: `discount_now` and `next_change_at` (unix s). From 22:00 to 08:00 UTC+8,
  `discount_pct` lists the cheaper models: qwen3.8-max and qwen3.8-flash 60% off,
  deepseek-v4-pro-0813, deepseek-v4-flash-0731 and deepseek-v4.1-flash 50% off.
  glm-5.3 and plain deepseek-v4-pro have no discount.
- zai: `peak_now` and `next_change_at`. Peak is Mon-Fri 14:00-18:00 UTC+8, when glm-5.3
  costs 3x quota (1x off-peak) and glm-5.3-flash 1.2x (0.4x). `promo_off_peak_until` is
  set while a promotion bills everything at off-peak rates.
- Example: `curl -s localhost:8765/quota/alibaba | jq .pricing.discount_now`

Facts that affect availability:
- `gpt-5.6-luna` has its own weekly limit: for light tasks openai is usable while the
  `gpt-5.6-luna:7d` window in `/quota/openai` is under 95%, even if openai is exhausted.
- openrouter is prepaid credit: its windows never reset, and `remaining_usd` is
  the balance.
- minimax (Token Plan) has a 5-hour and a weekly window (`/quota/minimax`); its key is
  `MINIMAX_API_KEY` from `~/.config/ai-keys.env`. MiniMax-M3 is the heavy model (effort
  variants `none`/`thinking`: use `thinking`), MiniMax-M2.7 the light one (no variants).
- alibaba (Token Plan) is one monthly credit pool shared by all its models (DeepSeek,
  Qwen, GLM, Kimi, MiniMax); its quota is the `month` window.
- alibaba (Token Plan) is read through the Bailian CLI's console login; if it shows
  `not_configured` or a login error, ask the owner to run
  `bl auth login --console --console-site international`.

### If the service isn't running
Check: `curl -sf localhost:8765/health`. If that fails:
1. `systemctl --user restart quota-tracker`, wait a few seconds, check `/health` again.
2. If systemctl says `Failed to connect to bus`, the user's systemd instance isn't
   running: ask the owner to run `sudo loginctl enable-linger $USER`, then retry step 1.
3. If it still fails, read `journalctl --user -u quota-tracker -n 50` and tell the owner
   what it says.
4. To run it without the service: `cd ~/projects/models_quota_tracker && uv run
   quota-tracker serve` (in the background; it stops when the session ends).

### Don't
- Don't read or edit `~/.config/quota-tracker/config.toml`; it holds account tokens.
- If a provider shows `error` about an expired cookie or token, tell the owner; renewing
  it needs their browser or login.

## This repo in particular
- This project's Claude Code sessions run on Z.ai's GLM: `.claude/settings.local.json`
  sets `ANTHROPIC_BASE_URL` to `https://api.z.ai` with glm-5.3 / glm-5.3-flash. That
  spends the Z.ai GLM Coding Plan (`curl -s localhost:8765/quota/zai`), not Claude quota.
- From 8 Oct 2026, Z.ai's glm-5.3 costs 3x quota on weekdays 14:00-18:00 UTC+8
  (08:00-12:00 Europe summer time); `curl -s localhost:8765/quota/zai | jq .pricing.peak_now`
  says when. Tell the owner before starting long work in those hours. Don't change
  `.claude/settings.local.json` yourself; it holds a token.
- New models usable for delegation (`opencode -m`, key in the environment from
  `~/.config/ai-keys.env`): MiniMax-M3 (heavy, variant `thinking`) and MiniMax-M2.7
  (light, no variants) on `minimax/`, and on `alibaba-token-plan/`: qwen3.8-max,
  qwen3.8-flash, deepseek-v4-pro-0813, deepseek-v4.1-flash, glm-5.3. Alibaba's Qwen and
  dated DeepSeek models are cheaper 22:00-08:00 UTC+8
  (`curl -s localhost:8765/quota/alibaba | jq .pricing.discount_now`).
