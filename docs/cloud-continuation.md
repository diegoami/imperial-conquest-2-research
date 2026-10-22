# Cloud continuation and private research inputs

Owner-requested checkpoint, 2026-10-21. Read [../CLAUDE.md](../CLAUDE.md) and
[environment.md](environment.md). Use the supplied checkout; worktrees, external
reviews and model-family restrictions are not compulsory. Migration preparation
launched no game. Experiments and bots remain paused pending owner authorization.

## GitHub and research checkpoint

Research [PR48](https://github.com/diegoami/imperial-conquest-2-research/pull/48)
merged at `16f019397e65ba521bbcee7acea2a7d2c9bd7c93`. Its complete GLM review and
independent unchanged-validator rerun are recorded in
[progress/research37-intake.md](progress/research37-intake.md). Read the
[native tax report](reports/2026-10-18-sav-export-original-windows-tax-candidates.md)
and [pending requests](pending-requests.md): three native Windows cases completed
the specified tax-only sequence, with 21 SAV and 38 PNG hashes reverified against
the readable owner-retained copy. This is **3/3 bound tax-only**, not general export
readiness or closure of [research37](https://github.com/diegoami/imperial-conquest-2-research/issues/37).
Native-JSON conversion remains **0/12**; UNKNOWN31 remains unknown and internal GUI
callback traces remain UNVERIFIED. Case3's recruitment state word was 24; its type
was 0. Do not resurrect the superseded “type24” interpretation.

The owner JSON inspection was read-only and aggregate-only: 12 saves, 11 unique
hashes, 11 format4 and one format7, null source provenance throughout, expected
save78 basename absent. Do not publish those private paths or individual hashes.
The four gates remain the input manifest, UNKNOWN/new-record policy, T185 review
and native acceptance of native-JSON outputs. The main project separately evaluates
promoted evidence through its Evaluated marker, T184–T186 and #1191; research must
not claim that routing or change the main project without authorization.

### Whole-SAV semantic atlas: continue the existing work

Read live [conquest107](https://github.com/diegoami/ic2-conquest/issues/107) and
[draft PR108](https://github.com/diegoami/ic2-conquest/pull/108), branch
`research/original-sav-semantic-atlas`. Its head advanced during preparation from
`97ba1d891f3487a6128dd6c68722f9104a425592` to
`9ebdc1541725c1d36c8c19636b6b26420021345b`; recheck before starting. It now includes
**increment1**, not just a proposed scope:

- `findings/2026-10-21-original-sav-semantic-atlas.md` and its unresolved register;
- `runs/experiments/data/run-exp-sav-atlas107/field-map-v1.csv`: 113 rows over
  14 record types, seeded from `nation-matrix-v2.csv`;
- `scripts/sav_atlas_coverage.py` and 11 offline tests;
- reported framing of 14 public and 42 private saves, including 16 conditional
  2,105-byte battle blocks, to exact EOF. These are upstream draft claims to check,
  not independently promoted research results. No separate review was recorded.

Physical coverage, semantic completion, byte identity and native acceptance are
separate. Its 100% physical coverage does not close meaning or lifecycle analysis.
The 31 unknown nation positions repeat across 496 bytes; they are not the only
whole-file semantic gaps. Constructor coverage (army96/656, fleet10/26), retained
residue/history, contextual unions and relocated indices remain unresolved.
[Research47](https://github.com/diegoami/imperial-conquest-2-research/issues/47)
owns the deep reader/writer and UNKNOWN/residue stream; do not create a duplicate.

**Next concrete task:** retrieve PR108 at its current immutable head read-only,
review increment1 with the findings-intake skill and rerun its offline tests and
framing against the restored corpus. Reconcile its field IDs and alias corrections
with reviewed research, then extend the SAME ledger with one bounded research47
reader/writer/lifecycle proof (start with a declared UNKNOWN31 access frontier).
Record computed-pointer, wide/overlapping-load and indirect-call edges explicitly;
a negative literal-offset search is not whole-program non-access proof. Do not
restart the atlas or run a game merely to verify framing. Research changes belong
here; send proposed upstream corrections through the authorized peer channel.

**Status 2026-10-21 (later):** done. PR108 merged and the atlas reached increment 4
(conquest main `29cc3a8`, ledger `field-map-v4.csv`). It was promoted, provisional, as
[reports/2026-10-21-original-sav-semantic-atlas.md](reports/2026-10-21-original-sav-semantic-atlas.md).
The 31 bytes are INERT at the stated scope, and research47 is narrowed to new-record residue,
slot/text lineage and historical-profile applicability. Notes are in
[progress/research47-atlas-intake.md](progress/research47-atlas-intake.md). Consolidated results
go to the OIMP2 session (see [environment.md](environment.md)).
Increment 5 (conquest `ad0af2d`, ledger v5) was added on 2026-10-22, and research47 was
closed. The only residual is the candidate first-turn moves of a fleet launched into a reused
index, which needs an owner-authorized game run.

At this checkpoint research open issues were 47,42,39,37,35,25,20. Reports from
research40/41/42 are already on main; check issue state rather than repeating their
completed intakes. Existing PR30 (`docs/session-handover-oct17`) and draft PR36
(`workflow/agy-sonnet-review`) remain preserved. PR30's old handover and PR36's
review-tool trial must not reinstate superseded workflow rules. No unfinished
research branch was deleted. Check live state after cloning/fetching.

## Authentication and dependencies

The reference is [ic2-conquest's continuation guide](https://github.com/diegoami/ic2-conquest/blob/80eaf3e1a303f86f90b72732e31bc0e8bd18ace3/docs/cloud-continuation.md).
Use managed GitHub authentication or a GitHub token injected through the cloud
secret facility (`GH_TOKEN`); verify repository access with `gh repo view`.
Never paste credentials into chat, commands, history or committed configuration.

Use the existing Windows rclone `gdrive:` remote on the desktop. Its configuration
is at `C:\Users\diego\AppData\Roaming\rclone\rclone.conf`; the WSL default has
different remotes. Pass the existing config by path without displaying it. In the
cloud, configure the equivalent remote through injected environment variables:

- `RCLONE_CONFIG_GDRIVE_TYPE=drive` (nonsecret);
- `RCLONE_CONFIG_GDRIVE_TOKEN`: full OAuth token JSON as a secret;
- `RCLONE_CONFIG_GDRIVE_CLIENT_ID` and `RCLONE_CONFIG_GDRIVE_CLIENT_SECRET` if
  the token was issued to a custom OAuth client. Token and client must match.

The owner will supply the token; this preparation does not prove cloud-secret
injection. Reuse conquest's setup if available. If it is unavailable, use rclone's
[headless authorization](https://rclone.org/remote_setup/) with the same OAuth client
and store the result directly as a secret. See [Drive setup](https://rclone.org/drive/)
and [environment configuration](https://rclone.org/docs/#environment-variables).
Do not print configuration, dump environment variables or enable verbose auth logs.
The desktop emitted a shared-client retirement notice; do not silently change the
OAuth client or assume a different client's token will work.

Linux dependencies: Git, GitHub CLI, Python3.11+, Bash, rclone, tar and sha256sum.
No application build is required. Optional scripts may need Unicorn2.1.4, Pillow or
binutils. Wine/.NET/OpenCode are unnecessary for the next static task. Full Ghidra
analysis may require a separately installed Ghidra; the bundle supplies text/source
extracts, not a ready Ghidra project. Use the active cloud harness for any optional
review. Legacy OpenCode1.x receipts are not a portable installation requirement.

## Verified private bundles

Both archives stay private, outside Git and public releases. Their internal
manifests contain private paths and per-input hashes: never copy them into reports.
The existing conquest bundle was downloaded and checked **before** preparing an
additional upload. Originals were preserved; no sync/delete operation was used.

| Remote folder | Archive | Bytes | SHA256 |
|---|---|---:|---|
| `gdrive:IC2/conquest/cloud-migration-20261021` | `ic2-research-inputs-20261021.tar.gz` | 2290243 | `2bea418bca6de330b2776c61581cf767d6b2829d4ac15dc03a728acdb693008e` |
| `gdrive:IC2/research/cloud-migration-20261021` | `ic2-research-continuation-20261021.tar.gz` | 1074444 | `9590ffcdc27cd4fb6f8e3ef82397722d5393bc086f6fa1b8b2e96e2a7299d56b` |

The base has 128 payload files: EXE/DAT, 27 decompile/symbol files, 63 retained
native-evidence files, three source saves, 16 crafted battle saves, 12 private
native JSON saves and five continuation/source-analysis receipts. Reuse it unchanged.
The supplement adds 70 files (5,981,748 payload bytes): unique research37/40/41/42
validation/review receipts and the unrelated, uncommitted sitting-recorder idea.
The idea is preserved, not approved or part of the research backlog. Its private
manifest records 37 deduplicated references to the base, pinned Git objects or other
supplement files. It is a provenance backup, not an executable cloud environment.
Full review exports can contain source excerpts and private paths: keep them private.
Credential patterns were checked without printing values; no matches were found.
Local settings backups were left untouched and excluded, as were credentials,
Wine prefixes, tool caches, disposable worktrees and Git metadata.

Fresh extraction of both archives passed every internal checksum: 128 base entries
and 71 supplement entries (70 payload files plus its manifest). Archive/readback
transfer verification is recorded in [progress/cloud-migration.md](progress/cloud-migration.md).

### Restore without overwriting existing inputs

Run outside the checkout with a fresh private directory. First verify both pinned
archive hashes, then extract and verify the internal checksums:

```bash
umask 077
# Run in Bash; stop immediately on a failed download or checksum.
set -e
export IC2_INPUTS_DIR="$(mktemp -d "$HOME/ic2-inputs.XXXXXX")"
rclone copyto gdrive:IC2/conquest/cloud-migration-20261021/ic2-research-inputs-20261021.tar.gz "$IC2_INPUTS_DIR/ic2-research-inputs-20261021.tar.gz" --immutable
rclone copyto gdrive:IC2/research/cloud-migration-20261021/ic2-research-continuation-20261021.tar.gz "$IC2_INPUTS_DIR/ic2-research-continuation-20261021.tar.gz" --immutable
cd "$IC2_INPUTS_DIR"
printf '%s  %s\n' 2bea418bca6de330b2776c61581cf767d6b2829d4ac15dc03a728acdb693008e ic2-research-inputs-20261021.tar.gz 9590ffcdc27cd4fb6f8e3ef82397722d5393bc086f6fa1b8b2e96e2a7299d56b ic2-research-continuation-20261021.tar.gz | sha256sum -c -
# Stop if either checksum fails. Run each extraction/check only after success.
tar -xzf ic2-research-inputs-20261021.tar.gz
tar -xzf ic2-research-continuation-20261021.tar.gz
(cd ic2-research-inputs-20261021 && sha256sum -c SHA256SUMS)
(cd ic2-research-continuation-20261021 && sha256sum -c SHA256SUMS)
export IC2_DECOMPILE="$IC2_INPUTS_DIR/ic2-research-inputs-20261021/decompile"
```

Preserve case (notably lowercase `.sav` on C1B/C1T) and duplicate JSON names.
Use the private manifests to resolve retained evidence, not historical desktop
absolute paths. Save new analysis outputs to new private paths; never overwrite
measured inputs. Retrieve public packet scripts/metadata from pinned conquest Git
objects listed in the private supplement manifest, not by recopying original bytes.

Original source pins: EXE SHA256
`9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31`, DAT
`94d0ccfc67148d727de4c4e60aefc3c53ba9e67775bd689f0fcb2e23c12e5fbd`,
`all_app_functions.txt`
`2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8`.
Other executable/data profiles need explicit applicability evidence.

## Remaining gaps and portable checks

The original native-evidence directory remains inaccessible; the bundle contains
the readable owner-copied evidence. Original writer candidate basenames/manifests
are absent. Temporary SHA-bound aliases used in the successful rerun did not
recover original writer-delivery provenance. Preserve that distinction.
The Windows validator's process checks and paths are not portable to Linux: do not
stub them out and call it a native pass. The metadata checker here is separate.
No cloud native Windows execution environment, authoritative twelve-input manifest
or missing save78 was supplied. Source provenance, UNKNOWN policy, construction,
history and callback gaps remain open; a hash match alone cannot close them.

After restore run the syntax/metadata checks in [environment.md](environment.md),
then PR108's offline tests and explicit-input framing. Check the pending draft queue
with authenticated `bash scripts/pending-drafts.sh`; network/auth failure is not an
empty queue. No game run is needed. A cloud target and its injected GitHub/Drive
secrets still need to be established by the owner.
