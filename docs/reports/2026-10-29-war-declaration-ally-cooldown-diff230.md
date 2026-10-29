# Declaring war from International Relations leaves a higher-index ally at peace (−18); the remake puts it at war

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `171eada` (draft last
changed at `0c3080e`), conquest [#230](https://github.com/diegoami/ic2-conquest/issues/230)
(tracker #228). Releases
[`run-exp-diff084-orders`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-orders)
(batch 1) and
[`run-exp-diff084-orders-b2`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-diff084-orders-b2)
(batch 2); their SHA-256s are committed at `runs/experiments/data/<run>/SAVES.sha256`. Wine-only.
Remake **v0.8.4** (`d9cc71bc82e22ad1d3d7c373c3d80d61ed0bcbeb`), `classical-faithful`.

**Tag:** `[confirmed, partial]`: five original-vs-remake cases under Wine, same start save, same
order. The explanation is `[confirmed: decompile]`: it was `[derived]` in the draft and this review
re-read both functions. Not run on native Windows.

**Review note (2026-10-29):**
- **Release integrity:** both release archives were downloaded. Their 400 + 30 saves match the
  committed `SAVES.sha256` files (430 of 430 OK). The hash files are identical on ic2-conquest
  `main` and `research/diff084-stats233`.
- **Every table cell was re-read from the saves** with my own relation-matrix reader (nation records
  after the army and fleet tables, relation row at `+0x26`). For all five cases, both games, I read
  `a000` (before), `a001` (after the order) and `a002` (after End turn). The table below reproduces
  in both directions (`[me][k]` and `[k][me]`). Each target–ally pair is allied (2) in `a000`.
  The −18 is still there after End turn: the quarterly thaw had not run yet.
- **The code explanation holds in the pinned decompile** (`all_app_functions.txt`, SHA-256
  `2018c205…`):
  - `TPolitics_OK` (`0x00453230`, :55335) commits in a loop `k = 0..15`. For each `k` it compares
    the **live** committed `rel[me][k]`, re-read on every iteration, with the dialog's copy.
  - It calls the setter `FUN_00449b40(me, k, dialog[k])` when the two differ and either the
    committed value is ≥ 0 or the dialog's value is war.
  - The setter turns a 0 written over an old 3 into −18 (`-0x12`), over 2 into −24 and over 1
    into −8. It writes both `[a][b]` and `[b][a]`, and runs the one-step war cascade only for the
    values 2 and 3.
  - So an ally with a lower index has already been visited when the cascade sets it to 3, and it
    stays at war. An ally with a higher index is visited afterwards. Its committed 3 differs from
    the dialog's 0 and is ≥ 0, so it is written back to 0, which becomes −18.
- **This corrects an earlier report.** Row S02c of
  [`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md)
  says the dialog's war order "declares war on a nation and on each of its allies". That holds only
  for allies with a lower index than the target's. The row now links here.
- **Overlap.** This report is consistent with
  [`decompiled-war-cascade-and-peace-paths.md`](decompiled-war-cascade-and-peace-paths.md) §1.3
  ("`TPolitics_OK` walks the human's whole row… each call cascades one step"). That report did not
  draw the order-dependent consequence. Two other reports fit:
  - [`2026-10-03-fleet-peace-prompt.md`](2026-10-03-fleet-peace-prompt.md) declared war on Carthage
    by the **unit-map path** (a fleet attack, Yes). Carthage's ally Numidia has a higher index (5),
    and there it ended **at war (3)**. That is one live observation for the attack-path prediction
    below.
  - [`2026-10-09-remake-v050-gap-analysis.md`](2026-10-09-remake-v050-gap-analysis.md) row S02c
    describes the remake side.
- **News: unverified.** The setter prints the "declares war" news line only for the cascade. The
  write-back of 0 prints nothing (§1.2 of the war-cascade report). So the original probably shows
  "… declares war on <ally>" and then silently leaves the ally at −18. This review did not read the
  news lines in the saves.

## Answer

When the human declares war on a nation that has an ally, the two games end in different states:

- **Remake:** the ally goes to war with the human (relation 3 both ways), whatever its index.
- **Original, from the International Relations dialog:** the ally goes to war only if its nation
  index is **lower** than the target's. If the ally's index is **higher**, it ends at **−18 both
  ways**. That is peace with the cooldown a war leaves behind.

| Case (start: Rome, 270 BC, `BASE.SAV`) | Target (index) | Ally (index) | Original: Rome–ally | Remake: Rome–ally |
|---|---|---|---|---|
| `rel-war-carthage` | Carthage (1) | Numidia (5), higher | **−18** | 3 |
| `rel-war-dacia` | Dacia (10) | Thracia (15), higher | **−18** | 3 |
| `rel-war-bithynia` | Bithynia (11) | Galatia (12), higher | **−18** | 3 |
| `rel-war-numidia` | Numidia (5) | Carthage (1), lower | 3 | 3 |
| `rel-war-thracia` | Thracia (15) | Dacia (10), lower | 3 | 3 |

In every case the relation with the target itself is 3 in both games. Nothing else in Rome's
records differs right after the order (re-checked: relations, recruit slots, treasury, nation
scalars, cities, armies, fleets). After the following End turn, Rome's records still differ only in
that relation.

## Explanation `[confirmed: decompile]`

`TPolitics_OK` commits every changed cell of the human's row through the relation setter, in nation
order. The setter drags the target's allies into war, one step only
([`2026-10-05-refused-attack-declares-nothing.md`](2026-10-05-refused-attack-declares-nothing.md)).
Ending a war through the setter writes the −18 cooldown
([`decompiled-diplomacy-peace-terms-and-instant-battles.md`](decompiled-diplomacy-peace-terms-and-instant-battles.md)).

So the loop reaches the target, declares war, and the setter sets the ally to 3. If the ally's cell
comes later in the loop, the dialog's copy of that cell still says peace (0). The committed value
(3) differs from it, so the loop writes 0, and 0 over war becomes −18. If the ally's cell came
earlier, the loop has already passed it, and it stays 3.

The conquest session ran the four control cases after explaining the first one. It wrote its
predictions down before the run (`difftest/cases/orders230_b2.py`, committed before the run), and
all four came out as predicted.

**Not tested:**
- Declaring war by attacking (the unit-map path, `TUnitMap_SelectUnit`) was not tested in this
  differential. That path calls the setter once and never walks the row, so the ally is expected to
  stay at war. One earlier case supports this: the fleet attack in
  [`2026-10-03-fleet-peace-prompt.md`](2026-10-03-fleet-peace-prompt.md), where the higher-index
  ally Numidia ended at 3.
- An ally of the human, and an AI's own declarations.
- Two declarations in one dialog session.
- Whether the "declares war on <ally>" news line still appears for the reverted ally.

## Remake side

The remake's `declare-war` (the command the CLI and the harness use) applies the cascade and stops.
The draft did not read the remake's International Relations dialog. If that dialog submits the same
command, a remake player always gets the ally at war.

## Evidence

The differential harness (ic2-conquest `difftest/`, `python3 -m difftest.sweep`) produced the data:
- **Data folders:** `runs/experiments/data/run-exp-diff084-orders/` (batch 1) and
  `runs/experiments/data/run-exp-diff084-orders-b2/` (batch 2). Each holds `results.jsonl`,
  `results-rejudged-*.jsonl` (the final verdicts) and, per case, `original/receipt.jsonl` and
  `remake/receipt.jsonl`.
- **Saves:** per case, `rel-war-<target>/original/a000.SAV` (before), `a001.SAV` (turn 0720, after
  the order) and `a002.SAV` (turn 0721, after End turn), plus the remake's `rel-war-<target>/remake/`
  exports with the same names. Carthage is in batch 1; Dacia, Bithynia, Numidia and Thracia are in
  batch 2.
- **Original build:** `Imperial Conquest 2 fast rollingsave seed.exe` (SHA-256 `354d8265…`), startup
  seed 12345, Wine 10.0.

## What this does not establish

- Native Windows behaviour.
- The unit-map (attack) declaration path.
- Allies of the human.
- The remake's International Relations dialog. Only its `declare-war` command was run.
