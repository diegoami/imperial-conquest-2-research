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
