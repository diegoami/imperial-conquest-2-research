# Research session state — 2026-10-17

Read `CLAUDE.md` for shared Codex/Claude policy and [environment.md](environment.md)
for startup. This file replaces the obsolete October 12 session snapshot. Check
`git status -sb`, `git worktree list` and origin before treating dated paths as current.

## Current boundary

Research main was `0a51774445ddbdef587aa5c858354ab5828e4053` when checked.
Research PRs [27](https://github.com/diegoami/imperial-conquest-2-research/pull/27),
[28](https://github.com/diegoami/imperial-conquest-2-research/pull/28) and
[29](https://github.com/diegoami/imperial-conquest-2-research/pull/29) are merged;
their full MiniMax reviews are preserved on the PRs. Earlier intake running notes
that say review pending describe their pre-review commits, not current status.
Issues **5, 22, 23, 24 and 26 are closed; 25 remains open**, verified on October 17.
Do not reopen completed work from the old handover's g4 hold or issue-5 TODO.
Use [findings-intake.md](findings-intake.md) for source pins and intake status.

## Why issue 25 remains open

The control/timing prerequisite was cleared by reviewed build PR #1156 at
`257f2d2cd7510451d229a983553a54b89065b06c`. The unchanged pinned comparison
has 318 hook trials: 282 complete exact, 36 residual, 283 exact draw streams.
The [target/draw report](reports/2026-10-16-tactical-target-and-draw-attribution.md)
explains why historical registry counts are different counting units and cannot
replace those residual counts.

The [fresh original decision trace](reports/2026-10-16-tactical25-original-decision-trace.md)
(source ic2-conquest `f872057ed455e977c33fc9ca2439b73a3a6f3c91`) establishes a
shared-input decision cause in mix-rg_s1: HR6 Gaul slot 22 selects original goal
(5,3), port goal (6,4), because the port's threat key tests the enemy archer
rather than the actor. Earlier ranking differences select the same goal. Both
fresh Wine observers reproduce all 325 legacy draw tuples and all 15 full saves
byte-for-byte. This supports the observed prefix; it does **not** establish a
corrected full battle or explain all 36 residual paths. Retain the state-only
ar-hi-three_s3 case and distinguish original observations from model-input probes.

The intake independently checked hashes, decoded raw observations, compared state
and audited helper bytes. It did not rerun Wine, Unicorn, .NET or a corrected-port
full replay. Native Windows confirmation is also outstanding. Permanent report
provenance and checker commands are authoritative; `/tmp` evidence copies may vanish.
The fixture repository is private `diegoami/ic2-test-fixtures`, pinned to
`6319802a75067e7730e4f6a27dce3b4e296ddd9b`; an older similarly named local
Windows fixture checkout is not this corpus.

## Next work and coordination

[Pending requests](pending-requests.md) owns the actual open-work specification:
a bounded build evaluation of the actor/enemy threat-key correction, followed by
separately reviewed sensitivity and full comparisons that identify which complete
residual paths disappear. No further original probe was requested in the latest
acknowledgment. Further observations may be needed for other cases. A research
intake alone authorizes no gameplay, fixture, draw-bound or expected-failure edits.
The desktop palette request still waits on the player.

This is the research session: verify and promote ic2-conquest drafts, then acknowledge
merged intakes. Read sibling repositories only; do not modify their files or message
the remake session without user authorization. The user authorized direct contact
with ic2-conquest; the latest acknowledgment included the PR-29 merge and next boundary.
Discover live peers through the current client's tools; old thread/socket identifiers
are historical. If messaging is unavailable, give the user concrete relay text.

The user selected direct Codex implementation and MiniMax review during the completed
session. Record new-session model choices according to `CLAUDE.md`; do not silently
choose a substitute. Shared policy remains in `CLAUDE.md`, with `AGENTS.md` as the
Codex entry point and the intake skill shared through the `.agents/skills` symlink.

Leave these unrelated untracked paths untouched: `.claude/settings.local.json`,
`.claude/settings.local.json.clother-20261012-120302.bak`, and `docs/ideas/`.
Never read the settings files. Only the main worktree existed before preparing this
handover; inspect the live worktree list for its review branch rather than assuming
historical intake worktrees still exist.
