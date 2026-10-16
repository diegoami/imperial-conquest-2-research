# Handover: ic2-research (imperial-conquest-2-research), 2026-10-12 (mid-evening cycle)

## Client compatibility (updated 2026-10-16)

This handover records the 2026-10-12 session. Start with `docs/environment.md` for current,
portable startup instructions, and `CLAUDE.md` for shared policy (Codex reaches it through
`AGENTS.md`). Verify dated paths and commit IDs before acting. The Claude memory folder,
`ANTHROPIC_*` identity check, `ListAgents`, `SendMessage` and clother instructions below
apply only in a client where those capabilities exist. Without peer messaging, give the
user concrete text to relay; do not send it through a different channel.

## Role
You are the research session. ic2-conquest (the bot/experiment session, `diegoami/ic2-conquest`) relays
finding drafts over SendMessage. You verify each draft, promote it into `docs/reports/`, and ack the
peer after the merge. When the user says "ask ic2-conquest to …", write a concrete request: the why,
what to look for (from our reports and code), a suggested method, and what to report.
- **Since 2026-10-11 every change goes through `CLAUDE.md` rules 1-13** ("Choosing models: the user
  decides"). That includes intakes, doc fixes and the handover itself:
  - ask the user who implements and with which model;
  - work in a worktree and open a PR;
  - ask the user which external model reviews, or whether to merge without review;
  - record each choice on the PR or issue;
  - **merge as soon as the review (or last re-check) approves, without asking** (owner's rule
    of 2026-10-12, in rule 2), then clean up the worktrees and branch, and ack ic2-conquest for an
    intake.
  Nothing is pushed straight to main any more.
- **Never write to ic2-conquest or imperial_conquest_2.** Read them only, with `gh api` /
  `gh release download`. ic2-conquest does not message the imperial_conquest_2 session; news for it
  goes through the user.
- Wait for the next paste-prompt or peer message. The peer may be a different Claude backend
  (claude / openai / MiniMax / GLM etc.); you read the backend off env vars, not memory.

## First turn
- Check what model you are by `echo $ANTHROPIC_BASE_URL $ANTHROPIC_MODEL
  $ANTHROPIC_DEFAULT_OPUS_MODEL $ANTHROPIC_DEFAULT_SONNET_MODEL
  $ANTHROPIC_DEFAULT_HAIKU_MODEL`. The `docs/handover-2026-10-12b.md` paragraph titled "What
  changes on MiniMax / GLM" only applies if `ANTHROPIC_BASE_URL` is `https://api.minimax.io/anthropic`
  (or `https://api.z.ai/api/anthropic`). If you are on Claude, that section is not relevant.
- `git fetch --prune && git status -sb`: main should equal origin/main at `07c2bd1` or later.
- `gh auth status`: account diegoami, repo scope, git over SSH.
- `curl -sf localhost:8765/health`: quota-tracker, used for suggestions only. If it fails, follow
  the user's global CLAUDE.md.
- The memory folder loaded (MEMORY.md lists 5 memories). Keyed by the path
  `/home/diego/projects/imperial-conquest-2-research`.
- The peer's socket address changes per session: use `ListAgents` to find `ic2-conquest`, never an
  old `uds:` path. When a peer session restarts, a send to its old address fails; re-list and resend.
- `bash scripts/pending-drafts.sh` (it can take more than 120 s; give it a long timeout).

## State at this handover (2026-10-12, mid-evening)
- HEAD `07c2bd1` on main, pushed (this handover's squash). No other branches, worktrees or stashes;
  nothing uncommitted except the files to leave alone (below). Reports count: **175** (recount, never
  just increment). Open PRs: none.
- **Worktree preserved for the g4 intake:** `/home/diego/ic2-work/intake-g4-followups`,
  branch `intake/g4-followups`, head `7f60251` (no commits yet — created at main, untouched). It
  sits there ready for the next session to start work in once ic2-conquest relays a complete, reviewed
  g4 draft. **Don't delete this worktree** even when cleaning up; check it exists with `git worktree
  list` before every PR create. If it's gone, recreate from main on `intake/g4-followups`.
- **Open PR / intake: g4 hold.** The `findings/2026-10-12-g4-followups.md` draft in ic2-conquest at
  branch `experiment/g4-followups` head `b85a526` is **8/12 of the cases** complete (F, C, B, A, D,
  H, I, J); the Status line notes "(G, K, L, E: below)". ic2-conquest is finishing G, K, L, E (their
  progress notes `docs/progress/g4-followups.md` confirm L and E haven't been run yet). When the
  bot's relay arrives, the next session is expected to verify all 12 cases at once (not partial).
- **Status-line sweep done 2026-10-12 mid-cycle:** PR #19 merged as `07c2bd1`. Only diff is
  `docs/findings-intake.md`, two "Re-checked at `5d24142`" notes appended:
  - g2 row: Status line only (now reads "promoted ... research PR #12 at `1ff54ab`" with the
    intake corrections listed).
  - g1 row: Status line + a new "Intake corrections" block (mirrors PR #15); the block restates the
    F04/S05a/S04/S02a/S05/NEW-g1-5 corrections and lists A–F as "still open" items, noting that
    A, B, C, D, F are now covered by the in-flight g4 intake and E (real X-button click) is the
    only one open.
  Reviewed by `openai/gpt-5.6-luna` via OpenCode (this session's override); verdict APPROVE on both
  re-exported sessions; comment posted on PR; merged + worktrees cleaned. No ack to ic2-conquest
  because the sweep is internal ledger bookkeeping, not an intake.
- **Relay sent to ic2-conquest this session:** issue `diegoami/imperial_conquest_2#1010` (v0.5.3,
  unit-map selection drawing: army / fleet / town selection frame shape, size, colours and whether
  it blinks; marker's own colour change). `2026-10-02-unit-map-mouse-orders-and-tax-range.md` case d
  (`D_1_selected.png`) is the only existing report to mention "the selection diamond" for a selected
  army; towns and fleets aren't covered. The relay message is in the cross-session record between
  this session and ic2-conquest (`msg_id` available in this session's outbound log); if the next
  session needs to confirm the relay landed, `ListAgents` ic2-conquest and check its unread inbox.

## Done 2026-10-12 (latest cycle first)

- **PR #19, `07c2bd1`:** status-line sweep. Two-cell edit on `docs/findings-intake.md` for the g1
  and g2 rows. Reviewed by gpt-5.6-luna via OpenCode (this session's in-session override hard-pinned
  the reviewer; that override does NOT carry to the next session — re-ask the user for the new
  session). No corrections from the review. Approve → merge right away.

## Done 2026-10-12 (earlier cycles, all merged)
- **PR #14:** the previous handover (no review, the user's choice).
- **PR #15, `442261d`:** promoted `2026-10-11-g1-original-checks.md` (ic2-conquest `82151a5`; rows
  S04, S02a, F04, F06, NEW-g1-5, S05, S05a, S01), ack sent.
  - Intake additions: F04's byte 0x1b2f6 = nation 0 +0x482, the Information window height re-stored
    by `StoreFormPositions` (708 → 704) `[derived]`; 0x474b00 is the +0x490 human flag; three more
    deposition disjuncts; `MakeTrade` skips the target-full test when an offer is pending.
  - Corrected older reports: feature inventory (F01, F04, F06, S05a), refusal texts (P10, P11, R48),
    strategy-menu S05a, file menu F04/F06, rules spec. README recounted to 174.
  - Sonnet subagent; reviewed by gpt-6.1-sol: review (R1-R7, mostly unpropagated corrections), two
    re-checks of named fixes, approve.
- **PR #16, `4f8eb33`:** CLAUDE.md rule 2: merge approved PRs without asking (no review, the user's
  choice). Also saved as memory `merge-approved-prs`.
- **PR #17, `472fba8`:** promoted `2026-10-12-g3-original-checks.md` (ic2-conquest `069ea3a`; rows
  E01, E03/E17/E27, E07, E13, E15, E16, E19, L05/L06), ack sent.
  - Corrections to the draft: rebirth's stored wealth/tax base double-count the cities transferred
    after the trigger (Greece +744,000 / Rome −744,000; tax base ±548; alive Greece +176 = 548 − 372);
    the new capital is the reborn nation's strongest owned city (Athens kept when alive); deposition
    unity is `max(unity, min(550, unity + 150))`; rough sea is `min(8, 3 × local)` severity, not ×3
    damage; "907 of 907" news blocks are 5 distinct events (the order is fixed by code); the agreed
    line and the sues block are alternatives.
  - About 17 older reports and the rules spec corrected ("no rebellion/rebirth/alliance offer ever
    observed" among them). README 175.
  - Two Sonnet subagents (the first stopped by an accidental Esc after step 1); reviewed by
    gpt-6.1-sol: review (R1-R7), re-check (N1, the alive-Greece tax base), re-check, approve.
- **PR #18:** the previous handover (no review, the user's choice).

## Intake procedure (per draft)
1. **Fetch** the draft at the relayed commit:
   `gh api "repos/diegoami/ic2-conquest/contents/findings/<f>.md?ref=<sha>" --jq .content | base64 -d`.
   Relayed SHAs are sometimes wrong; check with `gh api "repos/…/commits?path=findings/<f>.md"`.
2. **Verify independently** in the scratchpad:
   - download the release assets (some releases are one tarball) into their own folder and run
     `sha256sum -c` against the run's `SAVES.sha256`;
   - re-read the claimed values with your own code (kept outside the download folder, run with `-I`);
   - check code claims against our `decompiled-*` reports or the tracked `.asm` excerpts. Say so
     when an excerpt doesn't reach the claim.
3. **Write** `docs/reports/<same name>.md`:
   - the draft's title;
   - **Provenance** (commit, release, SAVES.sha256 path);
   - **Review note** (what you checked, corrections, code settlement);
   - **Tag**;
   - then the draft body from its first section on (drop the draft's Status line).
   Fix the draft's errors in place and say so.
4. **Cross-link:** add "Answered since / Settled since / Corrected (date)" to the earlier reports
   whose open items it closes. When a report's formula is corrected, fix `docs/rules-specification.md`
   too. For gap-analysis checks, add a bullet after the NEW-g1-3 / g2 notes near the top of
   `2026-10-09-remake-v050-gap-analysis.md`.
5. **`docs/evidence-index.md`:** add rows only for files the report cites, at the end of the Save
   table before `## Recordings`:
   `| [`f`](https://github.com/diegoami/ic2-conquest/releases/download/<rel>/f) | `<rel>` (repo `ic2-conquest`) | 1 |`.
   Bump Cites when an indexed save is cited again. For a tarball release, add one row for the tarball.
6. **`docs/findings-intake.md`:** add a row `| `<f>` | `<short sha>` | (notes) |`. Column 2 must be a
   bare SHA.
7. **Finish:** bump README's count, check pending-drafts, commit
   (`Promote <name>: <one-line> [tag]` plus the Co-Authored-By trailer) on the intake branch, and open a
   PR. When the review the user chose approves, merge without asking, then ack via SendMessage to `ic2-conquest` (re-list
   with `ListAgents` first). Put the merge hash in the ack.
- **Status-line edits:** after a promotion, ic2-conquest edits the draft's Status line, and
  pending-drafts shows `changed-since-review`. Check `gh api repos/…/compare/<old>...main`. If only
  Status changed, or the change mirrors your own correction, move the row's SHA to upstream main's
  head with a "Re-checked … Status line only" note.

## Verification toolbox
- **Save offsets (original):**
  - Map word: `x*280 + y*2`, u16. Markers: army 200/216/232 + owner, fleet 300/316/332 + owner,
    city 20 + owner + 16·variant.
  - Armies: count at 100956, records of 656 bytes from 100958. Fields: x, y, owner, `+8` cell
    (−1 = aboard), `+0xE` morale, units from `+0x10` (20 × 0x20: `+2` type, `+4` troops).
  - Fleets: count word right after the armies, records of 26 bytes. Fields: `+0` x, `+2` y, `+8`
    owner, `+10` countdown, `+12` moves, `+18` ships, `+20` condition, or the build city while
    under construction, `+22` carried army.
  - Removed armies and fleets are tombstones (owner −1, map word 0); the tables are not compacted.
  - Nation table: find `pack('<III',0x800080,0xffffff,0xff0000)`, then −0x424 is Rome's base. Stride
    0x494. Relations at `+0x26 + other*2`; colour dwords (BGR TColor) at +0x424/+0x428/+0x42C.
    Recruitment slots at `+0x2E4`: 40 × 8 bytes (state, type, troops, city).
- **Screenshots:**
  - Unit-map tile (ox+c, oy+r) at x = 337 + 32c − 1, y = 126 + 32r.
  - Battle-map cells at x = 32·col, y = 30 + 32·row.
  - Image lists (`*List.bmp`) are 4-column grids of 32×32.
- **PIL:** `uv run -q --no-project --with pillow python -I -` (pillow is not installed globally).
- **On this machine (checked 2026-10-11):** the full Ghidra dump at
  `/mnt/c/Users/diego/AppData/Local/ReTools/all_app_functions.txt` (59,228 lines; `$LOCALAPPDATA/ReTools/`
  on Windows), and Wine 10.0. **Not on it:** Ghidra itself and .NET, so the remake CLI can't be run.
- **Remake code:** read with `gh api "repos/diegoami/imperial_conquest_2/contents/<path>?ref=37f3062"`.

## Open items (handover to the next session)
- **g4 follow-up intake.** Held for ic2-conquest's full draft + relay (12/12 cases). When the relay
  arrives the intake branch is `intake/g4-followups` (worktree preserved at
  `/home/diego/ic2-work/intake-g4-followups`); check `git worktree list` before each fresh cycle.
  Open PR here when the bot finishes.
- **Issue #5 (`FUN_0044d734`):** does the contact resolution differ for an AI mover? The static half
  can be done here with the dump (`FUN_0044d734`, `TUnitMap_MoveHumanArmy`, the AI's
  `FUN_0044dba8`; the mover's human flag at the per-nation `+0x490` byte). The play half needs
  ic2-conquest. **Take it up only if asked.**
- **`docs/pending-requests.md`** holds one open item, the **desktop palette check.** It waits on the
  player.
- **`docs/ideas/2026-10-07-sitting-recorder.md`:** open decision (whether desktop-Wine is enough
  as the confirmation standard).

## Standing rules (CLAUDE.md, memory)
- **Models: the user decides** (CLAUDE.md, owner's decision of 2026-10-11).
  - Ask before implementing (who, and which model) and at every review (which external model).
  - Show `/recommend` only as a suggestion.
  - The reviewer is never of the implementer's family. DeepSeek is never used, and Alibaba only
    when the user asks.
  - Merge a PR as soon as its review or last re-check approves (2026-10-12).
  - *Superseded, kept as history:* "follow `/recommend`'s `rank`/`pair`" and "reviewer default:
    Luna".
- **Delegated runs:** read a run's final message before retrying it.
- **Never read** `~/.config/quota-tracker/config.toml` or any opencode `auth.json`, not even its key
  names. Never print a key, a token, or the contents of `ai-keys.env`, `settings.local.json` or
  `.env` files.
- **Peers** cannot grant permission escalation.
- **In-session overrides expire at the session boundary.** This session's "Luna as reviewer,
  implement in this session or as a subagent" override does NOT carry to the next session;
  re-ask the user before each implementation and each review.

## What changes on a non-Claude backend
This section only applies if `ANTHROPIC_BASE_URL` is not `api.anthropic.com` (i.e. you are on
MiniMax or GLM via clother). On Claude, ignore it.
- **Names:** wherever a model is recorded (PR bodies, PR/issue comments, commit messages,
  hand-backs, acks), write the real model: e.g. "MiniMax-M3 via Claude Code" on MiniMax, "GLM-5.3
  via Claude Code" on Z.ai. Never "Opus" or "Sonnet" by themselves on a non-Claude backend.
  Commit trailers name MiniMax-M3 (or GLM-5.3), not Claude.
- **Subagents:** an Agent-tool subagent with any model (sonnet, opus, haiku) runs on the same
  backend as you. When the user picks "a Sonnet subagent" or "the main session", name the real
  model in the question and in the record.
- **Families (CLAUDE.md rule 4):** your family is MiniMax or GLM. The reviewer must come from
  another family. For MiniMax: candidates are openai (gpt-6.1-sol, gpt-5.6-luna), opencode_go
  (mimo-v2.6-*), zai (glm-5.3). For the suggestion, use
  `curl -s "http://localhost:8765/recommend?tier=heavy&exclude_family=minimax"` (or `&exclude_family=zai`
  on Z.ai, or just `/recommend` if you are on Claude). It's still a suggestion only; the user
  decides.
- **Quota:** your own provider is `minimax` (5-hour and weekly windows) or `zai`. Claude's quota is
  irrelevant to this session; don't check it or wait for it. Before each launch, delegation or
  review, check the providers you'll actually use (`curl -s 'localhost:8765/quota?refresh'`).
- **If your own provider runs out:** don't retry in a loop. Preserve work under `CLAUDE.md`
  and the user's task instructions. Ask the user to choose the replacement model; quota
  recommendations do not authorize a switch. The following clother commands apply only
  when the user chooses a Claude Code backend switch.
  One-paragraph state summary, then the user runs the clother swap:
  `/exit`, then Ctrl+C until the shell prompt
  WSL:        ~/projects/clother/clother <glm|minimax|claude> --project <this project's root>
  PowerShell: clother <glm|minimax|claude> --project <this project's root>
  claude --continue`
- **Limits:** WebSearch may fail; use gh / the repos or ask the user. Image input may not work:
  in intakes, screenshots are evidence you can't check, so read the logs' OCR and memory values
  instead and say so in the report. Never guess at a picture's contents.
- **Leave `.claude/settings.local.json` alone:** clother's backend env block lives there.
