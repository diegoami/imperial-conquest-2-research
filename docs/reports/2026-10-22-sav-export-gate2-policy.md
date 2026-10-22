# SAV export gate 2: per-field writer policy and checker

**Provenance:** promoted, provisional `[confirmed, partial]` from
[`diegoami/ic2-conquest`](https://github.com/diegoami/ic2-conquest) `main` at `80a3963`
(PR #130, commit `b7db6bb`), draft
[`findings/2026-10-22-sav-export-gate2-policy.md`](https://github.com/diegoami/ic2-conquest/blob/80a3963/findings/2026-10-22-sav-export-gate2-policy.md)
(blob `1da08914`). The checker is
[`scripts/sav_export_policy_check.py`](https://github.com/diegoami/ic2-conquest/blob/80a3963/scripts/sav_export_policy_check.py)
(SHA-256 `bad8477a…8cf5`). It answers **gate 2** of
[research #37](https://github.com/diegoami/imperial-conquest-2-research/issues/37) (see
[pending requests](../pending-requests.md)) and builds on the
[SAV semantic atlas](2026-10-21-original-sav-semantic-atlas.md) (ledger v12, no UNKNOWN rows).

Intake by the research session (2026-10-22): the receipts were reproduced, and positive and
negative controls were added (`scripts/gate2-policy-adversarial.py`). No upstream review exists.
No game was launched, and no SAV was written outside a private scratch directory.

## Answer

The policy says what an exporter writes for every SAV field class:
- **INERT nation bytes:** carried from the source, else zero.
- **New armies:** the header plus all five fields of each live slot, slots packed, troops ≥ 0,
  empty slots zeroed.
- **Fleets under construction:** moves 0 and route x −1.
- **Tombstones:** none; counts match the live records.
- **Record order:** the source order is kept, and any moved index is fixed up (`FLEET.army`).
- **Carried armies:** the fleet tile, army cell −1 and `FLEET.army` are written together.
- **Text:** NUL-terminated, then zeros.
- **`CITY.allegiance`:** supplied, because it affects play.
- **History fields:** `wealth0`, `treasury0`, `cities0` and `conqueror` are presentation only.
- **Derived fields are recomputed:** the city list in name order, counts, and the city, army and
  fleet markers. The stale army band and the stale count of an eliminated nation are allowed.
- **Refused:** an open battle block, tombstones, invariant violations, and a missing allegiance.

Research agrees that this answers gate 2's *policy* question, with **one checker defect**: the
allegiance refusal is stated but not implemented (below). Gates 1, 3 and 4 are untouched.

## Method and observations

- **Tests:** `tests.test_sav_export_policy_check` passes (7 cases).
- **Public receipts:** the 28 per-file receipts in
  [`export-policy-v2/`](https://github.com/diegoami/ic2-conquest/tree/80a3963/runs/experiments/data/run-exp-sav-atlas107/export-policy-v2)
  reproduce byte for byte: the 14 public saves, each with and without `--source`.
  - With the source equal to the candidate (identity), 14 of 14 are accepted.
  - From scratch, 14 of 14 are refused, only for text tails and empty-slot residue.
- **Private bundle, identity mode:** the group counts reproduce exactly.
  - 3 source saves: all accepted.
  - 23 owner-retained native-evidence saves: 21 accepted, 2 refused for tombstoned armies (the
    two owner −1 records found in the increment 5 intake).
  - 16 research40 saves: all refused for the battle block (14 of them also fail the battle-grid
    invariant, as crafted).

  Only counts are reported here; private names and hashes are not copied.
- **Upstream gap: no positive control for the from-scratch mode.** Every real save fails it for
  residue, so I built one. `scripts/gate2-policy-adversarial.py` rewrites each input the way the
  policy prescribes and expects acceptance:
  - INERT bytes zero;
  - text tails zero;
  - empty slots zero;
  - building fleets moves 0 and route x −1.

  It then applies one mutation at a time to each canonical save and expects refusal.
  Receipt: [`gate2-policy-adversarial-v1.json`](../data/gate2-policy-adversarial-v1.json). The
  inputs are the 14 public saves plus the natural-embark save from `run-exp-sav-aboard107`.

| Case | Expected | Result |
|---|---|---|
| Canonical from-scratch rewrite | accept | **15/15 accepted** |
| INERT byte non-zero | refuse | 15/15 refused |
| City-name tail dirty | refuse | 15/15 |
| Unit slots unpacked | refuse | 15/15 |
| Negative troops | refuse | 15/15 |
| Army tombstone; fleet tombstone | refuse | 15/15 each |
| City list out of name order | refuse | 15/15 |
| Live nation's count wrong | refuse | 15/15 |
| City marker of the wrong owner | refuse | 15/15 |
| Building fleet with moves 5 | refuse | 3/3 (the saves with a building fleet) |
| Carried army moved off its fleet's tile | refuse | 1/1 (the aboard save) |
| **`CITY.allegiance` = −1 (missing)** | refuse | **0/15: accepted** |
| **`CITY.allegiance` = 99 (out of range)** | refuse | **0/15: accepted** |

**Defect:** the policy (point 8 and point 10) refuses "a campaign with no allegiance profile",
but the checker has no allegiance rule. A candidate whose city allegiance is −1 or 99 passes
both modes. An out-of-range allegiance is used as a nation index by the defence, capture,
defection, rebellion and revival code (increments 5, 8 and 10). In all 56 original saves, all
18,704 allegiance values (and owner values) are in 0..15. So a `city_allegiance_in_range` rule
(0 ≤ allegiance ≤ 15) would accept every original save and close the gap. Proposed upstream; it
is not fixed here.

## Inferences and scope

- The identity runs show that the checker accepts every original-written save without a battle
  or a tombstone. They do not test an exporter: in identity mode the INERT and residue rules
  compare a file with itself.
- The canonical rewrite shows that the from-scratch rules are jointly satisfiable on real states
  and that the checker's other rules bind. It is a self-made exporter stand-in, not a native
  JSON → SAV conversion.
- **Narrower than the original.** The original writes tombstoned armies that still hold troops,
  and the policy refuses that state. The two refused native-evidence files are byte-identical
  copies of tax **case 2's post-turn/reopen save**. Its hash is already published in the
  [native Windows tax report](2026-10-18-sav-export-original-windows-tax-candidates.md). So the
  original EXE on native Windows wrote this tombstone state in ordinary play. The same holds for
  the battle block.
- **Not checked by the checker:**
  - record-order equivalence with a source (the policy assigns it to exporter tests);
  - news text tails;
  - the allegiance profile (defect above);
  - aggregate fields that are stored live rather than derived (nation wealth and tax base). The
    policy does not say how an exporter supplies them consistently;
    [nation-tax-base-and-city-economy-fields](nation-tax-base-and-city-economy-fields.md) has
    the rules.

## What this does not establish

- **Gate 4:** native acceptance of any exporter-written SAV.
- **Gate 1:** the twelve-input manifest.
- **Gate 3:** review of T185.
- **Launch-turn moves:** whether leftover fleet moves can be spent on the launch turn. The
  policy writes 0.
- **Eliminated nation's count:** what the original shows after a corrected count is written.
- **Review:** there has been no independent review of the policy or the checker.
