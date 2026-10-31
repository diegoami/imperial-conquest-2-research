# The original moves a seat's armies one at a time in table order; remake main picks the best action across armies

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `09acc36` (PR #293). It was
found during the #174 fleet-0 attribution (owner request 2026-10-31). It compares the original with
remake main `8e2d9053` (T250–T252, not released), on the same 80 equal-state rounds as the
[rerun](2026-10-31-ai-rerun-remake-8e2d9053.md): 16 New Game starts (S00–S15 `*_AUTO0720.SAV`) × 5,
seed 12345, each replayed in the remake from the original's own round-start autosave.
- **Data:** `runs/experiments/data/run-exp-fleetroute174/`:
  - `remake-order-diag-v2/`: the 80 diagnostic rounds;
  - `army-order-diag-v2.patch.txt`;
  - `army-order-v4.json`, cited here. v1–v3 are earlier classifier versions, and v1 of the patch is
    kept as measured: it also counted candidates below the minimum score.
- **Code:** `runs/experiments/fleetroute174/army_order.py`.
- **Main run:** `run-exp-airerun/remake-8e2d9053-v1/`. **Original:** release `run-exp-aidecide` (decide
  hook logs and round-start saves).

**Remake T253 (2026-10-31):** fixed and verified on `e20a6488`, with 0 of 156 seats out of order ([the e20a6488 rerun](2026-10-31-ai-rerun-remake-e20a6488.md)).

**Tag:** `[confirmed]`, Wine-only. It confirms in play the rule already in the
[rules specification](../rules-specification.md) ("Seat loop and phase order"), and it is a new port
gap for the remake's classical-faithful mode.

**Review note (2026-10-31):**
- **Classifier rerun:** I ran `army_order.py` from a scratch copy of `09acc36` on the rerun's army
  report, with `main=` the main run and `order=` the diagnostic run. The output is
  **byte-identical** to `army-order-v4.json`: main 668 of 679, table order 678 of 679; 96 of 158
  seats out of id order on main, 0 of 156 with the diagnostic.
- **Disassembly** of the original:
  - `FUN_0044fa20` calls `FB7C` (diplomacy), `FFBC` (economy), `F31C` (armies) and `F608` (fleets),
    in that order (`0x44FA42–0x44FA51`).
  - `F31C` is **one loop** over the army table: index `esi` from 0, record pointer `edi` from
    `0x47C1EC` with stride `0x290` (656 bytes), and the count read **once at entry** from `0x4A0324`
    (`0x44F32F`).
  - Each own army with `+6 > 0` is handled whole before `esi` advances (`0x44F4DE`): the target tree
    (`E670`, `ECE4`, `EE60`, `E84C`), the action `DBA8`, then `AAB4` and the fallback `EBE8`. There is
    no second pass and no comparison between armies.
- **The S03 round 2 example, checked:**
  - **Original decide log:** Carthage army 2 (42,63) has target army 10 at score 1126, distance 4.
    Army 3's inputs, logged next, have the same target 10 at score −10000.
  - **Original saves:** at the round start (`hooked-t01-AUTO0721.SAV`), Celtiberia's only army is
    army 10 at (38,64), with 33,900 troops. At the round end (`hooked-t02-AUTO0722.SAV`), Celtiberia
    has no army, and Carthage army 2 stands at (39,64) with 22,942 of 33,900 troops.
  - **Remake AI log:** "approach target army (38, 64) with army-3", score 1651 of 2 candidates;
    then army-2's approach, score 1651; then army-2 attacks army-10.
- **Remake code** at `8e2d9053`: `AiTurn.cs` takes the highest score at or above the minimum, and an
  exact tie goes to one draw from the seat's stream (`AiTurn.cs:342–371`).
- **Diagnostic patch:** a filter in `AiTurn.cs`, active only with `IC2_DIAG_ARMY_ORDER=1` and
  `ClassicalArmyNavigation.Applies`. It keeps only the military candidates of the first own army in
  `state.Armies` order that has one at or above the minimum score. I did not re-execute the
  diagnostic build.

## The difference

- **Original:** the army phase runs each own army in table order. Each army decides, walks and
  attacks before the next one decides. So a later army sees what the earlier ones left: their
  positions, their kills, and a war ended by a treaty after a battle.
  - Example, S03 round 2: Carthage army 2 attacks Celtiberia's army 10 and destroys it. Army 3 then
    has no enemy army (score −10000), takes `e84c+city>85` and marches on the city osca at (49,41).
- **Remake main:** `AiTurn` proposes candidates for **all** own armies on the current state. It
  executes the best one, with exact ties drawn from the seat's random stream, then proposes again.
  - So a later army can act first, on a state the earlier armies have not changed yet.
  - S03 round 2: army-3's march and army-2's approach both score 1651. The draw picks army-3. It
    chases army-10 at (38,64), 50 tiles away across the sea, and army-2 destroys that army moments
    later.
  - In 96 of 158 seats where two or more armies acted, the remake ran them out of army-id order. Id
    order is the table order unless a death moved records.

## Measured on 80 rounds

`army_order.py` takes each army's **first action** in the remake's AI log. It checks the action's
kind (target army, city at the original's position, resupply, or the mercenary run) against the
original's branch at that army's turn. Rows that are "diplomacy" or "state" in the army comparison
are skipped.

| Remake | First actions matching the original (679 armies) |
|---|---|
| main `8e2d9053` | 668 |
| main + **table order** (diagnostic) | **678** |

- **The 10 armies the diagnostic fixes:**
  - Carthage army 3, round 2, in S03, S04, S05, S08, S11 and S12. Main chases army-10, which army 2
    is about to destroy. The original and the diagnostic march on osca (49,41).
  - Seleucid army 4, round 3, in S01, S07 and S13. Main approaches (220,35); the original and the
    diagnostic approach (177,41).
  - Seleucid army 4, S03 round 4. The original attacks army 0 (`army>100`); main approaches a city;
    the diagnostic approaches the target army.
- **It breaks none.** The one row left is the Galatia battle draw (S02 round 4, see the rerun).
- **Why the earlier comparisons missed it:** `aidecide/compare.py` reads each army's **first** remake
  decision record. The remake writes it on the first proposal pass, before any army has acted. So
  the record matched the original's inputs even where the army later acted on that stale state.
  - **This narrows the rerun's result:** "no army row unexplained" holds for decision records. Ten
    more armies differ in their first action.
- **Other comparisons, as drafted:** under the v1 diagnostic, the diplomacy, economy and fleet
  results are the same or better (diplomacy 1,133 same seats against 1,110, with no deterministic
  first divergence; fleets unchanged, 27 rows). I did not rerun these.

## For the remake (inference)

In classical-faithful (`ClassicalArmyNavigation.Applies`):
- Run the military phase **one own army at a time, in live table order** (`state.Armies`, T240).
- Each army takes its target-tree action, its walk, its attack and its fallback, on the state the
  earlier armies left.
- No cross-army score competition, and no random tie draw between armies.
- The designed / Improved AI keeps its candidate selection.

## What this does not establish

- **Where diplomacy and economy sit:** the original runs them as whole phases before the armies
  (above, `0x44FA42–0x44FA47`). The diagnostic left those candidates in the remake's shared pool,
  so the remake's interleaving is not tested here.
- **The remake's implementation:** the diagnostic is a filter on the existing loop, not a patch
  proposal.
- Rounds 6 and later, other seeds, and native Windows behaviour.
