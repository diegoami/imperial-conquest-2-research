# Research cloud migration verification — 2026-10-21

Owner authorized migration preparation, use of the existing private Windows rclone
remote and session-led workflow. No game run was launched. Restore instructions,
archive pins, dependencies, evidence gaps and next task are in
[../cloud-continuation.md](../cloud-continuation.md).

## Private transfers

Before any research upload, downloaded the existing conquest archive and checksum
from `gdrive:IC2/conquest/cloud-migration-20261021`. The archive's 2,290,243 bytes
matched SHA256 `2bea418bca6de330b2776c61581cf767d6b2829d4ac15dc03a728acdb693008e`.
All 128 payload sizes/hashes matched its private manifest. Fresh extraction also
passed all 128 SHA256SUMS entries. This bundle was reused unchanged.

The separate research destination was checked and returned directory-not-found
before upload. Uploaded only the research supplement archive and its checksum to
`gdrive:IC2/research/cloud-migration-20261021`, using immutable copy semantics.
Archive: 1,074,444 bytes, SHA256
`9590ffcdc27cd4fb6f8e3ef82397722d5393bc086f6fa1b8b2e96e2a7299d56b`.
Full remote readback of both files matched local SHA256; `rclone check --download`
completed **0 differences, 2 matching files** at 2026-10-21 21:48:44 UTC.
The supplement's fresh extraction passed 71 checksums (70 payload files and its
private manifest). Source payload hashes were rechecked after archiving; originals
were retained. Deduplicated dependencies are recorded privately at immutable Git
commits or base-bundle hashes. No original-game inputs were reuploaded.

The allowlisted payload contained unique research validation/review receipts and
one unrelated uncommitted idea. Credential-pattern scanning returned no matches;
no settings backups, authentication/configuration files, caches, Wine prefixes,
Git directories or disposable worktrees were selected. Private manifests and raw
review exports remain private, including their source excerpts and private paths.

## Repository verification and preservation

- Shared CLAUDE/AGENTS/environment/intake/review guidance now follows the owner's
  session-led policy. `.agents/skills/retrieve-findings` still resolves to the
  maintained `.claude` skill. Historical review records remain unchanged except
  an appended PR48 completion receipt.
- Relative links and restore-command Bash syntax checked; `git diff --check`,
  Python script AST parsing and `bash -n scripts/pending-drafts.sh` passed.
- SAV37 metadata-only checker passed against pinned conquest records, with a fresh
  output outside Git. This did not open private evidence or establish a new native pass.
- Research PR48 is merged at16f0193. Research37/47 and conquest107 remain open;
  conquest draft PR108 advanced to9ebdc15 during preparation. The guide includes
  its field ledger/checker increment as unpromoted upstream evidence to review.
- Existing research PR30/36 branches and unrelated untracked local settings backups
  and idea file were preserved. Credentials were not read or transferred. No sibling
  repository was modified; migration used the supplied research checkout and branch.

No separate external review was launched for this documentation/process change.
The session checked the final changes and transfer receipts. Actual cloud secret
injection, selected cloud runtime and Windows-only native execution are still
unverified. Missing original writer manifests, authoritative twelve-input binding
and save78 are not supplied by migration; semantic uncertainty is unchanged.
