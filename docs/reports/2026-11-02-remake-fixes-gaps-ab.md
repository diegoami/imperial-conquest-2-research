# Remake fixes for the long-run AI gaps A and B (Faithful AI), from the confirmed original behaviour

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `8f204849` (PR #305), owner request 2026-11-02.
The owner wants this as a promoted report that the remake's main session can act on.

**Tag:** `[derived]`. There is no new measurement here. It rests on two promoted reports:
- [`2026-11-02-longrun-v090-ai-gaps.md`](2026-11-02-longrun-v090-ai-gaps.md) (PRs #165, #167);
- [`2026-11-02-gapb-siege-call168.md`](2026-11-02-gapb-siege-call168.md) (PR #169).

Both causes are `[confirmed: Wine hook]`, with no native Windows run.

**Remake:** v0.9.0, `88c1989b`; code references are at that commit. Both gaps are older than v0.9.0: they are also seen
on `e20a6488`, `8e2d9053` and v0.8.4.

**This is a specification for the remake, not a runtime change made here.** The remake's session decides how to
implement it.

## Gap A: gate the garrison fallback on the full budget, not on the tile

- **Original:** after a walk, F31C calls `FUN_0044aab4`, and the fallback `FUN_0044ebe8` runs only when it returns 0.
  AAB4 returns 1 when the recomputed full moves differ from the army's moves, that is, when the army has spent part
  of its allowance anywhere in the seat. Hook evidence: 38 walks, AAB4 = 0 only for the one army that spent nothing.
- **Remake:** `AiTurn.cs:336–351` (T156) runs `RunGarrisonFallback` when the command was accepted and the army's tile is
  unchanged, with moves > 0. An out-and-back walk (the original's swing) leaves the tile unchanged but spends moves, so
  the remake runs a fallback that the original skips. The capital armies then drift away every turn: 410 rows over four
  games.
- **Fix:**
  - Run the fallback only when the army's moves still equal its full allowance for the turn, and drop the tile
    comparison.
  - The full allowance is what the remake gives the army at the start of its seat, the counterpart of AAB4's
    recomputed value.
  - **Not** a per-command test ("moves after this command < moves before"). The original's test also counts moves spent
    earlier in the seat, for example by an E84C run walk or by capital defence. The two tests agreed on all 38 measured
    walks, but they were never compared in a case where they could differ. This corrects the fix wording first written
    in the long-run report.
- **Expected after the fix:** Macedonia army 8 at (144,42) stays on its tile, as do the Media, Thracia, Ptolemaic and
  Antioch capital armies and Armenia army 1 at Van. This matches the original.
- **Side fix:** the log line "garrison fallback moved army-N to (x, y)" prints the target. It should print the tile
  where the army ended.

## Gap B: the AI walk's end check besieges or attacks the adjacent target

- **Original:** the walk `FUN_0044dba8` calls the line walk `FUN_0044d734`. D734 steps along its line, then checks the
  target tile (0x44D895–0x44D98C, disassembly re-checked at intake):
  - The army must be next to the target: `FUN_00449018(target, army) == 1`. Otherwise D734 returns.
  - Land (map code 2–11) that the army has the moves to enter: D734 takes one more step.
  - **A city** (map code 20–99):
    - the seat's nation is at war (relation 3) with the city's **owner** and the army has moves > 0:
      `FUN_0044b27c(army, city)`, the siege, which sets moves to 0;
    - not at war: `FUN_0044f6d8(city, army)`.
  - **An army** (map code 200–247), at war, moves > 0: `FUN_0044aee4`, the attack.
  - The check does not test the city score, the mercenary offer or the branch that chose the target.
- **Measured:**
  - **Sieges:** all 5 AI sieges in the hook runs came from this check, through two F31C walk sites:
    - 0x44F4C7, the continuation of the `e84c+city>85` branch: the two gap-B armies, Carthage 2 at Castulo and
      Seleucid 5 at Astacus;
    - 0x44F43F, the `city>100` branch: 3 sieges.
  - **Army attack:** observed once, added at intake. In `hooks-gapb-v1/rome-t01end` (Rome game turn 2), Carthage
    army 2 walks from (42,63) by F31C 0x44F409 (`army>100`, DBA8 returning to 0x44F40E). Its last D734 step ends at
    (39,64), and AEE4 is entered with return address 0x44D9A0, which is D734's army branch.
- **Remake:** the MercenaryRun continuation `MarchAtCityTarget` (`AiMilitaryPhase.cs:433–440`) issues a plain march. The
  walker cannot enter the city, so it moves the army onto another tile next to the city, and no siege happens. The
  remake's `AttackCity` decision does besiege. It was seen at city score 102 (Galatia–Cius), which agrees with the
  original's `city>100` outcome. Its exact threshold was not checked here.
- **Fix:**
  - When an AI march at a city target ends next to that city, the city's owner is at war with the army's nation and
    the army has moves > 0: besiege the city (moves → 0) instead of stepping aside.
  - When the target tile holds an army at war: attack it.
- **Scope:**
  - **Measured:** the city end check through the continuation (0x44F4C7) and the `city>100` walk (0x44F43F); the army
    attack once through 0x44F409.
  - **Not observed, so not claimed:** E84C's own run walk (0x44E913), and the 0x44F409 and 0x44F47C walks ending next
    to an enemy city. The end check is shared code, so the same rule is likely there too.
  - **Code only:** the fail side of each guard (not adjacent, not at war, 0 moves). Only the pass side was measured.
- **Expected after the fix:** the army stays on its tile and the siege goes on every turn:
  - Castulo's loyalty falls 3 points a turn (80 → 77 → 74 → 71);
  - Astacus's falls 2 points a turn (52 → 50 → … → 44);
  - the besieging army loses roughly 600 to 1,150 troops a turn: Carthage 21,878 → 20,732; Seleucid 11,224 → 10,630.

**Recheck on `11f713e2` (fixes 1723 and 1724):**
[`2026-11-02-remake-11f713e2-recheck.md`](2026-11-02-remake-11f713e2-recheck.md).
- Gap A: 410 rows → 4. All 4 are turns where the remake declares a war the original doesn't.
- Gap B: 17 rows → 1. The row left is a **third measured caller** of the end check: the garrison fallback's own walk
  (EBE8 → DBA8, called at 0x44ECD6). It besieges in the original and steps aside in the remake. The scope above
  therefore extends to the fallback walk.

**Recheck on v0.9.1 `0d9d4729` (fix 1729):**
[`2026-11-03-remake-v091-recheck.md`](2026-11-03-remake-v091-recheck.md).
- Gap B: 1 row → 0. The fallback walk now besieges Sidon.
- **New, gap A on a second path.** The fallback for an army that the tree gave **no command**
  (`AiMilitaryPhase.cs:487–503`) runs on `mayMarch` alone. Fix 1723's full-allowance test (`AiTurn.cs:336–354`) covers
  only the fallback after a command. In the original both go through the same AAB4 call. Seen once: Galatia army 12,
  Ptolemaic game turn 1, with 8 of its 10 moves. The original keeps it in place; the remake walks it toward Iconium.
  **Fix:** the same full-allowance test on the no-command path under Classical Faithful navigation.

**More gaps from the Ptolemaic game on v0.9.1**, from
[`2026-11-03-ptolemaic-longrun-positions.md`](2026-11-03-ptolemaic-longrun-positions.md):
- **The no-command fallback:** two more cases, Seleucid armies with 1 move in turns 13 and 16. The fix is the one above.
- **Capital defence with a pending human battle:**
  - **The original:** the pass keeps going. The threat stays alive, and the next responder is sent toward it.
  - **The remake:** `AiCapitalDefence.Run` breaks at the interruption (lines 110 and 137).
  - **Fix:** under Classical Faithful, the pass continues, and the threat stays valid for later responders.
  - **Design question:** how the instant-battle mode should treat such a battle. It has no counterpart in the original.
- **The new fleet's launch tile:**
  - **The original:** the last match of the ring scan, x outer and y inner, outside the region x ≥ 248, or x ≥ 214 with
    y ≥ 99.
  - **The remake:** `CoastalCity.FirstAdjacentSeaTile` takes the row-major first.
  - **Fix** (corrected 2026-11-03): use `ClassicalFleetNavigation.ReplaceLandTarget(build city)` on the live
    `OriginalFleetPort.MapCode`, since the original also skips a tile holding a unit's marker. The AI disembark and
    the fleet route already follow the rule; the earlier "code only" disembark item is withdrawn
    ([placement and Macedonia](2026-11-03-placement-and-macedonia-longrun.md) §1).
- **The AI's fleet build city:**
  - **The original:** `FUN_004496e0` never picks a city in the eastern region (x ≥ 248, or x ≥ 214 with y ≥ 99).
  - **The remake:** `CoastalCity.FleetBuildCity` (through `AiFaithfulEconomy.ChoosePort`) has no zone test, so Media
    builds 64-ship fleets at Ardabil on the Caspian.
  - **Fix:** exclude `ClassicalFleetNavigation.ExcludedEasternZone` under Classical Faithful.
  - **Code only:** ties go by table order, not city id ([placement and Macedonia](2026-11-03-placement-and-macedonia-longrun.md) §2).
- **The resupply-city tie:** the original takes the first city in table order. The remake uses city-id order. Seen 4 more times in the
  Macedonia game.
- **The no-command fallback:** one more case, Carthage army 10 in Macedonia turn 26 (8 moves of 9).

## Reading moves in saves

AI armies get their moves back between Celtiberia's seat and Illyria's, in every measured round. So a save shows spent
moves for nations whose seat comes after that point, and full moves for those before it. Rechecks of both fixes should
compare positions, loyalty and troops, not moves read from a save, or read moves at the end of the seat itself (with a
hook).

## Recheck plan

On the pin with the fix:
1. `python3 -m difftest.pin build <ref>`;
2. the anchored long runs (`difftest/anchored.py`) on the stored original games;
3. `runs/experiments/longrun-v090/stays.py`.

Expected: the 410 capital-army rows and the 17 enemy-city rows go to 0. The other structural rows (relations, city
captures, battle outcomes) were never attributed to a cause, so they are not expected to change, and they are not
claimed to be random draws. Gap C (fleet hunt draws, the Alexandria port tile) is not addressed here.

## Corrections made at intake

- [`2026-11-02-longrun-v090-ai-gaps.md`](2026-11-02-longrun-v090-ai-gaps.md):
  - gap A's fix line now gives the full-budget gate (the draft's correction);
  - gap B's "500–700 troops a turn" now reads about 600–1,150. The report's own table shows Castulo's army losing
    1,146; the draft has 500–1,100.
- The draft's `AttackCity` "≥ 102" is stated here as the one sample it is.
- The draft's "the remaining rows are draws" is narrowed to "not attributed to a cause".
- The army-attack outcome is added from the `rome-t01end` log.
