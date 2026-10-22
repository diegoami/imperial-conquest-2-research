# Research #47 / conquest #107: SAV atlas intake (2026-10-21)

Cloud session, session-led workflow. The owner asked for the intake through the IC2 Conquest
session's relay, and confirmed it here. No game was launched from this session.

## Inputs and access

- **GitHub.** The research repo is reachable with push access. The ic2-conquest API is not
  attached (an attach with push access was refused by the session's permission classifier), so
  it was read through an anonymous clone and its public pages. `scripts/pending-drafts.sh` used
  to print `pending: 0` when the API refused; it now exits 2 with "queue unknown" (fixed in this
  branch). The draft queue was therefore **not** checked from this session.
- **Drive.** The injected `gdrive:` remote works. rclone warns that the shared OAuth client id
  is being retired during 2026.
- **Private inputs.** Both private bundles were restored: archive hashes match, and 128/128 and
  71/71 internal checksums pass. They sit outside Git in a private temp directory.
- **Upstream pins.** PR108 is merged (`a5051a3`), and ic2-conquest main is `29cc3a8`.

## Checks run

See [the report](../reports/2026-10-21-original-sav-semantic-atlas.md), Method. In short:
- every atlas receipt was rerun;
- the four atlas test suites and three repo checks pass;
- the serializer order and trailer layout were re-read;
- `scripts/unknown31-adversarial-check.py` ran with a positive control on +0x490;
- the 12 inert107 saves were rehashed and their diffs reproduced independently.

Scratch reruns stayed outside both checkouts. Nothing was written to ic2-conquest.

The first quick reach pass (ad hoc, not committed) reported 0 candidates. It had decoded the
application range as one contiguous block, which stops at the first undecodable byte. The
committed checker sweeps the code properly and finds 11, all false positives on reading. The
committed receipt is the authoritative one.

## Research #47 disposition

**Narrow, do not close.**
- The 31-byte UNKNOWN question is answered INERT for the original EXE profile, at the stated
  static scope plus one Wine round.
- Still open:
  - new-record minimal byte images (army 96/656 and fleet 10/26 written; the retained bytes ever
    read later);
  - inactive-slot and text-tail policy;
  - historical-profile applicability for fresh campaigns (the DAT-loader provenance of the
    baselines is now known);
  - optional native Windows or emulator confirmation of INERT beyond one round.

## Limits

- No upstream review of increments 3–4 and no separate review of this intake. The upstream
  scripts were rerun, not audited line by line.
- The native-run saves have no release yet; the owner's Drive is their only copy outside the
  bot's container.

## 2026-10-22: increment 5 (conquest `ad0af2d`)

The owner confirmed this intake after the IC2 Conquest session's relay.

**Checks.**
- The four atlas test suites pass, and the corpus was rerun with ledger v5.
- The ledger diff v4→v5 changes no class or offset.
- Corpus slot and fleet counts were recomputed over the same 56 saves.
- Re-read in source or x86: the army constructor, attrition and all four of its callers, fleet
  launch, the round tick's fleet branch, `ShowArmyDetails`, and the five allegiance readers.

The results are in the report's Increment 5 section.

**Finding.** The upstream slot counts exclude two tombstoned army records (owner −1) that still
hold live troops, and upstream doesn't say so. With them included the counts are 6,118 live
and 9,522 empty slots.

**Research #47: closed.** Its done-when (a field table with class and evidence for the 31
bytes and the new-record/residue/history fields) is met statically. The one residual is the
first-turn moves of a fleet launched into a reused index. That candidate effect needs an
owner-authorized game run, and it is recorded in the report and in `cloud-continuation.md`.

**Limits.**
- The other readers of an empty slot were not re-read one by one; ShowArmyDetails was
  spot-checked.
- The text-tail claim was not re-derived.
- There was no review of increments 3–5 and no separate review of this intake.
