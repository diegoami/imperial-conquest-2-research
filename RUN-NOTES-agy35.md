# Task35: agy CLI / Sonnet trial

Owner requested adding an agy workflow task and trying Sonnet on an actual task.
Issue35 created. Implementation: current Codex/OpenAI session; reviewer explicitly
selected by owner: Sonnet via agy. Live model chosen claude-sonnet-5-5-medium;
no substitute authorized. CLI agy1.4.0 at /home/diego/.local/bin/agy.

Plan: discover CLI/model/permission capabilities, run a bounded additional review
of completed research33/PR34 with full brief, monitor one managed background run,
read/preserve complete response, record trial result and remaining integration work.
No changes to gameplay, fixtures, scientific claims or approval policy.

Progress:
- Initial restricted agy models failed: own log/crash writes and localhost socket
  denied. Reran discovery with runtime authorization; live Sonnet identifier found.
- Complete review brief prepared /tmp/ic2r35-sonnet-brief.md; existing copied
  research33 evidence available under /tmp/ic2r33-review-evidence. Review range
  2ed4625..64adfb1 immutable, extra review explicitly requested by owner.
- Will try plan+sandbox modes with structured output, no permission-bypass flag.
  These flags' actual permissions/results are part of the trial, not assumed
  equivalent to the existing OpenCode reviewer agent.

- Commitfbad0aa pushed: task35, selected live Sonnet ID and trial protocol.
- agy conversation b856691c-11f7-4200-b8d9-8f4f99cc2649, model
  claude-sonnet-5-5-medium, plan+sandbox reports permission_mode request-review.
- First managed run exited0/CLI SUCCESS in8.7s but denied RunCommand and returned
  only an intent to start. Read full result; it is NOT a completed review/approval.
- Resumed same conversation/model with unchanged permission restrictions and a
  full operator-captured diff, using view_file only. No bypass flag or new model.
- Resumed run exited0/CLI SUCCESS in218.9s and returned actual STATIC review:
  rework,6findings (2medium provenance/receipt,4low checker/status/coverage).
  Complete returned report read and retained in docs/data/agy-sonnet35-review.json.
- No reviewer tests/digests/runtime execution. The supplied evidence kit retained
  old OPEN PR96 metadata, not the later merge JSON; this limits its R2 assessment.
  Some line references refer to captured diff positions; normalize before fixes.
- No original research evidence, source report, runtime or fixtures changed by
  this trial. Existing source/MiniMax approvals and merged PR34 remain historical.

## END

- Issue35 created: integrate agy review route; still OPEN, trial is partial evidence
  rather than full harness integration. Sonnet produced a useful static review,
  not executed evidence verification or approval.
- Need explicit read-only command policy, structured result/verdict/denial checks,
  conversation resume and monitor integration before routine use. CLI exit0 or
  status SUCCESS alone is insufficient. Never use permission bypass as a fix.
- Preserve raw CLI logs/events and briefs under /tmp/ic2r35-*; internal CLI logs
  stay outside git. Published receipt contains only model review/result metadata.
- Full review goes on PR34 and issue35; proposed environment notes/receipt retained
  on an isolated branch/draft PR. No further model review or scientific fix launched.

## Owner-requested repeat without sandbox

- Owner: "ok then repeat it without sandbox". Live model list rechecked; same
  claude-sonnet-5-5-medium available. Resumed conversationb856691c-11f7-4200-b8d9-8f4f99cc2649
  without --sandbox, retaining plan mode/read-only brief and no bypass flag.
- Added later PR96 merge/tree metadata to the review inputs to address the earlier
  static review's missing publication-evidence context.
- Managed run exited0/CLI SUCCESS but again denied RunCommand and returned only
  "Terminal access should work now, so I'll start with the provenance commands."
  Read complete result. This is NOT a completed repeat review or an approval.
- Init still says permission_mode request-review. Omitting --sandbox alone did
  not enable terminal execution; earlier sandbox-specific causal attribution was
  too strong. Exact policy reason is not exposed by denied_actions.
- Receipt: docs/data/agy-sonnet35-nosandbox.json. Raw new events/logs remain under
  /tmp/ic2r35-agy-nosandbox-*. Existing complete static review remains unchanged.
- CLI duration_seconds appears conversation-level; do not interpret the returned
  duration as isolated runtime without verifying its semantics.
- Next integration work remains task35: command-approval behavior in print/plan
  mode, least-privilege execution and truthful result validation. No broader
  permission bypass or configuration change was made.

## voice-teacher PR74 investigation requested by owner

- Read PR74 body, full integration/runbook/schema/adapter/test diff at
  head4811d3739efbee5d8fe51510344ffc437a73a60d; PR OPEN at inspection. No sibling
  files modified, credentials accessed or additional model review launched.
- Their successful adapter intentionally DENIES shell commands; it prepares a
  committed task/diff/source packet for supplemental STATIC review. Fresh profile,
  bwrap read-only namespace/egress boundary, explicit policy, JSON schema and
  strict parser are the workflow integration, not unrestricted terminal execution.
- It keeps --sandbox and always eligible:false/modelIdentityVerified:false. Their
  existing review gate remains. Recorded trial is Sonnet medium, conversation
  b518e7c4-9b88-45e2-807e-2be541fbc91a. Did not rerun their tests or native trial.
- Official headless docs explain soft-denial/exit0 for tools needing unavailable
  approval; this explains the observed failure mode independently of sandbox flag.
  Earlier trial diagnosis should have consulted that documented policy sooner.
- Added pinned adoption reference to task35/environment notes; no new adapter
  implementation or global permission/authentication changes made in this check.

## Owner-requested Claude CLI review

Piped the pinned PR36 diff at e8b61a3 into Claude Code 2.1.293 print mode, safe mode, tools disabled. Requested sonnet alias; runtime reported MiniMax-M3[1m]. Completed exit 0, success, no permission denials; full result retained in docs/data/claude-cli35-review.json. Static review approved with no blocking findings and minor readability observations. External references and original trial execution were not independently verified by this reviewer. This is not an Anthropic Sonnet review. No routing/authentication changes; task35 remains open and PR36 remains draft.
