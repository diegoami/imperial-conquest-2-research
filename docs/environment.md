# Environment

## Startup

All clients share `CLAUDE.md`; Codex enters through `AGENTS.md`. Read
[cloud-continuation.md](cloud-continuation.md) for cloud inputs and current work.
Check `git status -sb`, `git worktree list`, `git log -1 --oneline`, fetch origin,
and inspect current GitHub issues/PRs. Historical paths, model names and review notes
are not current instructions. Work in the supplied checkout; isolation and reviews
are chosen by the session. No quota service, local memory store or other client is
required. Do not inspect local settings or credentials to discover model identity.

## Dependencies and validation

This is a research repository with no application build. Install Git, authenticated
GitHub CLI, Python 3.11+ and Bash. Private restoration also needs rclone, tar and
sha256sum. Some specialized analysis uses optional Unicorn, Pillow or binutils;
install only what the chosen script needs. Wine, .NET and a game launch are not
needed for static research or migration. A decompilation text dump is not a Ghidra
project; deeper computed-pointer analysis may require setting up Ghidra separately.

For documentation/process changes check `git diff --check`, relative links and the
shared skill symlink. For scripts, run the relevant checker on its documented inputs
and record unavailable evidence. Safe syntax checks:

```bash
bash -n scripts/pending-drafts.sh
python3 scripts/tests/test_pending_drafts.py
python3 -c 'import ast, pathlib; [ast.parse(p.read_text(), filename=str(p)) for p in pathlib.Path("scripts").rglob("*.py")]'
```

Most analysis scripts require external saves, trial JSON or game files. Use
[evidence-index.md](evidence-index.md), the private restoration guide and explicit input
paths rather than hardcoded desktop paths. `scripts/ai-turn-intake-check.py` also needs
the ic2-conquest parser; pass its checkout as the second argument if not a sibling.
`scripts/sav37-native-metadata-check.py` checks committed metadata, not private native
acceptance. Do not fake Windows process checks or promote a Linux hash check as a
new native Windows result.

## Optional tools and peer communication

Claude, Codex and OpenCode agent/session tools differ. Use only capabilities actually
available, and never claim delivery without a successful messaging result. The owner
allows messages to ic2-conquest. Owner rule (2026-10-21): send newly consolidated
research directly to the main-project cloud session titled "OIMP2"
(imperial_conquest_2; `session_01AY2hoWxpgkz4qN6t6FtLKM` on that date — re-check the
session list if it is gone). Raw, unreviewed drafts are not consolidated research. Without that bridge, supply a concrete relay message.

Separate reviews are optional; [review-brief.md](review-brief.md) offers guidance.
The OpenCode reviewer agent is read-only and does not configure Codex permissions.
Legacy OpenCode review receipts used 1.18.32: the desktop's default 2.0.28 was
incompatible with that invocation. The cloud harness need not install that CLI.
Never bundle provider authentication, a Wine prefix or local settings backups.
