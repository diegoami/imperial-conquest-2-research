# Agent rules

## Choosing models: the user decides (owner's decision, 2026-10-11)

This replaces every earlier model-choice rule of the project (L50/L51 of harness_imperial, the
quota-tracker "follow `/recommend`" rule, default reviewers, chains, substitute orders). Those are
kept only as history where docs still show them.

1. Before implementing anything (a task, a fix, a plan change), ask the user ONE question with the
   question tool: does the main session implement it, or a subagent, and which model?
   - The main session: it implements itself, in its own git worktree (never the main checkout).
   - A subagent: the Agent tool with the model the user names (any model this session's backend
     offers), or an external run (e.g. OpenCode) with the model the user names.
   Whoever implements works in its own worktree, keeps a short running-notes file there (plan, a
   progress line per commit, an END block before stopping), pushes after every commit, and opens
   the PR. When a subagent ends, the main session reads its final report before acting and posts
   its notes on the issue.
2. At every review (first review, re-review, re-check of named fixes), ask the user ONE question:
   which external model reviews? Run that review alone (one at a time), and relay its findings to
   the user in full. A PR gets one review unless the user asks for more. Every review brief
   carries the section in `docs/review-brief.md`.
3. With each question, show the quota service's recommendation as a SUGGESTION ONLY:
   `curl -s "http://localhost:8765/recommend?tier=heavy"` for heavy work, `tier=light` for small
   work (its `pick`/`pair` with rank, outlook and reliability). If it doesn't answer, ask without
   the suggestion.
4. The only fixed rules: the reviewer is never of the implementer's model family; DeepSeek is never
   used; Alibaba only when the user asks.
5. Record each choice (who, which model, the suggestion's reasons) on the issue or PR.
6. These rules hold whatever model the orchestrating session runs on; they never name it.
7. A failed run is diagnosed and fixed, not silently re-routed: another model only when the
   provider does not answer, and the user names it.

Facts for running the model the user names (not a choice rule):
- Model ids come from the provider's live list (`opencode models <provider>`), never memory.
- "Luna" on OpenAI is `openai/gpt-5.6-luna` (direct route), not `openai/gpt-6-luna`. Never run a
  Luna through OpenCode Go (`opencode-go/...`): a proxy behind it returns `Bad Request` in long
  agent loops.
- Effort: for heavy models prefer medium over high, or light when medium is not needed, unless the
  user says otherwise.

## Monitoring OpenCode sessions (and any other background agent)

8. Start every OpenCode run in the background, with stdin from a file (never an inherited pipe:
   `opencode run` waits for stdin's end-of-file before it creates a session). Never wait on it
   blind. Reviews run with `--agent reviewer` (`.opencode/agents/reviewer.md`: read-only, `/tmp`
   open), and their briefs start with the run rules in `docs/review-brief.md`.
9. Watch it with one monitor that checks every 1-2 minutes and reports only changes:
   - the session started (`opencode session list` in the run's directory, or the run's
     "session ses_... started" line), and the run's exit;
   - progress: the OpenCode log's size and the session's `updated` time, the worktree's changed
     files, new lines in the running-notes file, and new commits pushed to the branch;
   - "possibly stuck" after ~10 minutes with no change; "unpushed" when a commit sits on the
     branch but not on origin for ~15 minutes (push it for the run and record it);
   - free memory, if the machine is short of it: run reviews and builds one at a time.
   For a Claude subagent, the progress signal is its transcript file's size plus its worktree.
10. Tell the user, in plain language, what each running agent is doing: the step it is on, what it
    committed, what it found (from its notes, commits and latest session messages). Never raw log
    lines or byte counts.
11. On a "possibly stuck" flag: check the process is alive, read its newest session messages
    (`opencode export <ses_...>` or the session reader under "Delegated runs" below); a long build
    or test step is not stuck. A dead or 20-minute-silent run is stuck: record the cause, fix it
    if it is ours.
12. When a run ends, read its final message before doing anything else. A run that stopped and
    reported a blocker gets an answer (fix the brief or the setup), not a retry on another model.
13. A run interrupted by our own limits (an idle or total timeout) is RESUMED in its own session
    and worktree (`opencode run --session <ses_...>`, with a short "continue where you stopped"
    message and a longer limit), not restarted from scratch.

For findings reviews, see `.claude/skills/retrieve-findings/SKILL.md`.

## Delegated runs: read what they returned (owner rule, 2026-10-05)

Before you retry a delegated run, re-route it to another model (only under rule 7), or call it a
failure, read what it returned. Never retry blind.

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
