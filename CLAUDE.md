# Agent rules

## Choosing models

L50 (harness_imperial). Before choosing, recommending or delegating to a model (an OpenCode
implementer or reviewer, a Claude agent or subagent, an OpenRouter or ElevenLabs model), check how
much quota its provider has left with quota-tracker (see `docs/environment.md`). A provider whose
status is `exhausted` is not used until it is usable again: take the next model of the chain whose
provider has quota, pass it explicitly (the model of an Agent call or of `opencode -m`), and say so
in the run's report or the PR body ("GLM skipped: zai exhausted until 21:40; reviewed by Luna").
Exception: `openai/gpt-5.6-luna` has its own weekly pool, so for light tasks openai stays usable
while the `gpt-5.6-luna:7d` window in `/quota/openai` is under 95%, even if openai is exhausted.
Where the service is not installed, go on without it and count a usage-limit error as `exhausted`.
Model ids come from the provider's live list (`opencode models <provider>`), never memory.

L51 (harness_imperial). The light OpenAI model, and the default reviewer `luna`, is GPT-5.6 Luna on
the direct OpenAI route: `openai/gpt-5.6-luna`, effort `high`. It is not GPT-6 Luna
(`openai/gpt-6-luna`), which draws on OpenAI's main pool with Sol; never use GPT-6 Luna as the
reviewer. Never use a Luna on OpenCode Go (`opencode-go/...`): a proxy behind it returns
`Bad Request` in long agent loops.

Effort: for heavy models use medium rather than high, or better light when medium is not needed.
Sol is used sparingly.

The reviewer is always of a different model family from the implementer. For findings reviews, see
`.claude/skills/retrieve-findings/SKILL.md`.

## Delegated runs: read what they returned (owner rule, 2026-10-05)

Before you retry a delegated run, re-route it to another model, or call it a failure, read what it
returned. Never retry blind.

- OpenCode runs (implement.mjs / review.mjs): exit 1 with an empty diff looks the same for an early
  end and for a run that stopped and reported a blocker. The log's tail shows only the last tool
  output, not the model's final message. Read the final message from the session record:

  ```
  python3 - <<'EOF'
  import sqlite3, json
  db = 'file:/home/diego/.local/share/harness-opencode/data/opencode/opencode.db?mode=ro'
  c = sqlite3.connect(db, uri=True)
  sid = 'ses_...'   # the "session ses_..." line in the run's log
  parts = c.execute("select data from part where session_id=? order by time_created", (sid,)).fetchall()
  texts = [json.loads(d) for (d,) in parts if json.loads(d).get('type') == 'text']
  print(texts[-1]['text'] if texts else 'no text part')
  EOF
  ```

  Open it read-only. Never read auth.json in that directory.
- Claude agents: read the agent's final report (its hand-back) in full before acting.
- A run that stopped and reported gets an answer to its report: amend the task, decide, or
  escalate. Post the report on the task's issue so it is kept.
- Treat any earlier "model X ends runs early" verdict as unconfirmed until its runs' final messages
  have been read.

Why: in goal2-archaeology, T23's GLM-5.3 run stopped correctly and reported a real blocker in the
Done-when. Its report was only in the session record; the main session misread it as an early end
and moved the task to another model, which spent quota on a contract that could not be met.
