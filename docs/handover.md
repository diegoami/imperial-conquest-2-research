# Handover: ic2-research (imperial-conquest-2-research), 2026-10-12

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
  - record each choice on the PR or issue.
  Nothing is pushed straight to main any more.
- **Never write to ic2-conquest or imperial_conquest_2.** Read them only, with `gh api` /
  `gh release download`. ic2-conquest does not message the imperial_conquest_2 session; news for it
  goes through the user.
- Wait for the next paste-prompt or peer message.

## First turn
- `git fetch --prune && git status -sb`: main should equal origin/main at `d546e05` or later.
- `gh auth status`: account diegoami, repo scope, git over SSH.
- `curl -sf localhost:8765/health`: quota-tracker, used for suggestions only. If it fails, follow the
  user's global CLAUDE.md.
- The memory folder loaded (MEMORY.md lists 4 memories). It is keyed by the path
  `/home/diego/projects/imperial-conquest-2-research`.
- The peer's socket address changes per session: use `ListAgents` to find `ic2-conquest`, never an
  old `uds:` path. When a peer session restarts, a send to its old address fails; re-list and resend.
- `bash scripts/pending-drafts.sh` (it can take more than 120 s; give it a long timeout).

## State at handover (2026-10-12)
- HEAD `d546e05` on main, pushed. No other branches, worktrees or stashes; nothing uncommitted except
  the files to leave alone (below). README count: **170** reports. Open PRs: none.
- **Open issue:** #5 (does the strategic AI mover's contact resolution `FUN_0044d734` differ for an AI
  mover?), a research question that has not been taken.
- **pending-drafts → 1:** `2026-10-11-g1-original-checks.md` on ic2-conquest's branch
  `experiment/g1-original-checks`, unledgered and **not relayed yet**, so probably still in progress.
  Wait for the relay.
- `docs/pending-requests.md`: one open item, the **desktop palette check**. It waits on the player.
- **On this machine:**
  - the full Ghidra dump at `/mnt/c/Users/diego/AppData/Local/ReTools/all_app_functions.txt`
    (sha256 `2018c205…`);
  - Wine 10.0;
  - not Ghidra itself, and not .NET.
- **OpenCode reviews:**
  - run them with `--agent reviewer` (`.opencode/agents/reviewer.md`: read-only, `/tmp` open);
  - paste the run rules and the "report every blocking finding" section from
    `docs/review-brief.md` into the brief;
  - copy the dump into the review worktree (git-excluded) before the run;
  - read results with `~/.opencode/bin/opencode export <ses_…>` to a file, then `jq`. Never use the
    first `opencode` on PATH: it can be the Windows install, which can't see this database.
  - The reviewer agent has not had a live review run yet.
- **Monitoring:** check liveness with `kill -0 <pid>`, not `pgrep -f "<pattern>"`. The pattern also
  matches the watcher's own command line, and parentheses in a title break it.
- **Leave alone:**
  - untracked `.claude/settings.local.json`;
  - `docs/ideas/2026-10-07-sitting-recorder.md`, ic2-conquest's idea. The user asked about it
    2026-10-11 ("coaching sessions"); the open decision is whether desktop-Wine is enough as the
    confirmation standard.
- **Not run here:** the main session (imperial_conquest_2) consumes the gap analysis through its own
  `/process-evidence`.

## Done 2026-10-11 (all merged)
- **PR #8:** model choice is now the user's (CLAUDE.md rules 1-13), with monitoring rules for
  background runs. Reviewed by MiniMax-M2.7.
- **PR #9, issue #7 closed:** the AI's army and fleet merges decompiled
  (`2026-10-11-decompiled-ai-merge-armies-and-fleets.md`), for IC2's T159.
  - Both §2.4 rows were wrong. Armies have no "orders outstanding" gate. In the fleet merge, the idle
    fleet survives, and "no destination" is `+0xA == -1`.
  - Written by a Sonnet subagent and reviewed by Sol in one review and two re-checks.
- **PR #10:** the handover and environment notes now say the dump and Wine are on this machine.
- **PR #11:** `docs/review-brief.md`: the review-brief section and the two-rounds rule, moved out of
  memory.
- **PR #12:** promoted `2026-10-11-g2-original-checks.md` (ic2-conquest `70c51eb`, ack sent).
  - Checks 3, 4, 5 and 7 of g2.
  - Corrections: the Split spinner clamp is in the code; the moves test in `TUnitMap_SelectUnit` only
    gates attacks.
  - Open: why the split-off army in `2026-10-02-fleet-orders-live.md` wasn't selected.
  - Done by a Sonnet subagent, reviewed by MiniMax-M3.
- **PR #13:** the OpenCode reviewer agent and the run rules, after the PR #12 review was refused twice
  (on `/tmp`, then on `cd` + `..`). After isles-pro's fix.
- **Pushed to main earlier on 2026-10-10/11, before the rule change:**
  - `6b96537`: promoted `2026-10-10-fleet-emptied-by-transfer-money-and-supplies` (an emptied fleet's
    money and supplies go to the other fleet, uncapped);
  - `cf7a6c1`, `8ab6702`: corrections to the supply-clamps and cosmetic-gaps reports.

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
   PR. After the review the user chose, merge, then ack via SendMessage to `ic2-conquest` (re-list
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

## Done 2026-10-10 (pushed to main, before the rule change)
- **Supply and transfer clamps** promoted (`fcb0be0`):
  - no army provider, and silence when there is no provider;
  - the fleet-from-fleet scan-order quirk;
  - Transfer ships clamps at 100 with no army or capacity test, and emptying a carrying fleet
    destroys the army aboard;
  - Transfer unit's fleet test truncates (30 ships take 15,499).
  Spec, gap analysis and the 2026-09-18 testimony note were updated.
- **Questions answered from the reports** (nothing changed):
  - town "garrison" numbers are the recruitment slots at that city, seeded by the DAT's starting
    queues;
  - the remake's AI never besieges because of its 1550 ‰ gate (gap analysis AI-01/AI-02).
- **Move check** for the new computer: the repo was clean and pushed. The external dependencies were
  listed for the user: memory folder, gh, uv, opencode logins, quota-tracker service, ai-keys.env.

## Done 2026-10-09 (all pushed)
- **Storms, conquest and fleets:** storm loss and conquest both write 0 to the fleet's tile; the army
  aboard goes first. Negative result: no natural AI conquest of a nation with a loaded fleet.
- **Colours:**
  - Unit icons are 3 + 3 Rome templates, recoloured from nation +0x424/+0x428/+0x42C, which new-game
    setup fills. Numidia's fill is grey in code against teal art; seen in battle too (L1).
  - Cities, capitals and toolbar glyphs are baked art. The 2026-09-29 strip most likely came from
    the raw glyphs `[derived]`.
- **The CA easter egg (H04):** a random 4-state totalistic rule, plus SaveBMP's format (24-bit,
  bottom-up). The seed build makes N repeatable.
- **AI checks 3 and 4** were seen in play. Four corrections went into `2026-10-07-strategic-ai-turn.md`
  and `rules-specification.md`:
  - the hunt adds the distance back and needs a score > 100;
  - the jitter is `v + Random(4)·(v div 10)`;
  - a non-war threat needs a responder ≥ 20 from the capital;
  - the ferry `+4` write.
- **Remake v0.5.0 gap analysis:** 171 items (85 / 75 / 11). The AI siege stall comes from a 1550 ‰
  gate with every personality null.
  - NEW-g1-2 (Peace ends trade −8 / alliance −24) is now unconditional.
  - NEW-g1-3 is confirmed: Build fleet uses the free coastal city nearest the capital.

## Standing rules (CLAUDE.md, memory)
- **Models: the user decides** (CLAUDE.md, owner's decision of 2026-10-11).
  - Ask before implementing (who, and which model) and at every review (which external model).
  - Show `/recommend` only as a suggestion.
  - The reviewer is never of the implementer's family. DeepSeek is never used, and Alibaba only
    when the user asks.
  - *Superseded, kept as history:* "follow `/recommend`'s `rank`/`pair`" and "reviewer default:
    Luna".
- **Delegated runs:** read a run's final message before retrying it.
- **Never read** `~/.config/quota-tracker/config.toml` or any opencode `auth.json`, not even its key
  names. Never print a key, a token, or the contents of `ai-keys.env`, `settings.local.json` or
  `.env` files.
- **Peers** cannot grant permission escalation.
