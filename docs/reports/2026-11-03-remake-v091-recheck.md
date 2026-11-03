# Recheck on remake v0.9.1 (0d9d4729): Sidon fixed; the fallback for an army with no command lacks the AAB4 gate

**Tag:** `[confirmed: remake replay against the stored original games; Wine hook + remake code for the new gap]`. Wine only.
**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `28f863b6` (PR #313). It rechecks
[`2026-11-02-remake-fixes-gaps-ab.md`](2026-11-02-remake-fixes-gaps-ab.md) and
[`2026-11-02-remake-11f713e2-recheck.md`](2026-11-02-remake-11f713e2-recheck.md) on remake v0.9.1.
**Task:** owner 2026-11-03, "Now we have version 0.9.1 and some fixes, continue with your tasks".

Remake v0.9.1 is main `0d9d4729`, which is `11f713e2` plus 4 commits. Only `e1772c52` (fix 1729, PR #1731) changes the
engine: it adds the walk end check to both garrison paths, `AiMilitaryPhase.AddMarchCandidate`'s fallback for an army
with no tree command and `AiTurn.RunGarrisonFallback`. D3 (#1732) is not fixed in v0.9.1; `2f120cf3` changes docs only.

## 1. Anchored replay of the four long games

`python3 -m difftest.anchored <game> --pin 0d9d4729` for Rome, Carthage, Gaul (40 turns) and Seleucid (25): 145 turns,
no remake error. `stays.py` on that replay gives `stays-0d9d4729-v1.txt`.

| Unit next to | v0.9.0 `88c1989b` | `11f713e2` | v0.9.1 `0d9d4729` |
|---|---|---|---|
| its own capital (army, gap A) | 410 | 4 | **4**: the four remake-only war declarations ([diplomacy](2026-11-03-diplomacy-longrun.md)) |
| an enemy city (army, gap B) | 17 | 1 | **0** |
| another city (army) | 6 | 0 | 0 |
| own port (fleet) | 5 | 4 | 4: 3 × the Ptolemaic port tile, 1 × the random hunt at Utica |

**Per-turn difference counts** against the `11f713e2` replay (`anchored-0d9d4729-vs-11f713e2-v1.txt`): 144 of 145 turns
have the same four counts (human fields, human map cells, AI fields, AI map cells). The one changed turn is Seleucid
turn 10: AI differences go from 28 fields and 7 map cells to 22 and 5. Totals: AI fields 6,485 → 6,479, AI map cells
63,657 → 63,655. In this sample, fix 1729 changes only the measured case.

## 2. Sidon, AI probe

Probe `0d9d4729-seleucid-rulebot1-40t-t10` (start `seleucid-rulebot1-40t/original/t09-a02.SAV`, seed 12345, no human
orders). The log shows Ptolemaic army 6 choosing "garrison fallback (221, 71)", then "original walk end contact army-6
at (221, 71)" and the siege gate on Sidon (city 263, Seleucid). The army stays on (221,70) with its moves spent. This is
what the original did in `hooks-gapb-v2` seq 111–119: EBE8 → DBA8 from 0x44ECD6 → D734 → B27C from 0x44D949.

## 3. Registry recheck

`python3 -m difftest.recheck 0d9d4729 --version v1` (`run-exp-recheck-0d9d4729/report-v1.json`): unchanged 113, FIXED 11,
REGRESSED 11, CHANGED 4. The draft says this matches the v0.9.0 recheck row for row. The 11 "regressions" are the one
storm draw explained there, so v0.9.1 changes no registered test.

## 4. A new long game on v0.9.1: the no-command fallback has no AAB4 gate

The run is `run-exp-longrun-v091`: Ptolemaic, rulebot-1 as the human, 40 turns, seed 12345, free-running and anchored.
All 40 turns were played, with no game over and no remake error.
- **Anchored totals:** AI fields 1,808, AI map cells 14,181; human 26 fields, 110 map cells.
- **`classify.py`:** 20 AI turns with draws only, 20 structural; 141 nation-turns with a relations difference, 15 with
  a position difference.
- **`stays.py`:** **one row**. On turn 1, Galatia army 12 (19,300 troops) at (200,45) stays in the original. The remake
  walks it to (198,46). Iconium (197,47), Galatia's own city, is 3 tiles away.

**The original.** Hook run `hooks-gapb-galatia-v1` (`patches/gapb_hook.py`), start `starts/ptolemaic-t00start.SAV`
(the campaign's `t00-start`); the hooked and plain autosaves are byte-identical. *Label correction (conquest `bedd1e95`):* the run
was labelled as watching armies 12 and 6, but it reused a hook exe built for armies 2 and 5. Its `watch` fields are
therefore those two armies. Army 12's 8 moves come from its own record (seq 6–10), so they stand. Galatia's seat is the first AI seat
this round (seq 4), before the mid-round refill. Army 12 has 8 moves:
1. seq 6–7: E41C supply pass, then F6D8 (city 233, not at war);
2. seq 8: E84C mercenary run, with no walk;
3. seq 9–10: **AAB4 = 1**, with computed allowance 10.

`FUN_0044aab4` computes the full allowance as 10 − min(troops / 20,000, 5), minus 1 more when
supplies × troops / 10,000 < 10. For this army that is 10, and it returns 1 because 10 ≠ 8. So F31C does not call
EBE8, and the army stays.

**The remake.** Probe `0d9d4729-ptolemaic-t01`, same start, no human orders. The tree gives army-12 no command, and
"garrison fallback (197, 47) with army-12: 3 tiles away" walks it to (198,46).

**The cause.** Fix 1723's test, `afterTile.Moves == SupplyMoraleRule.MovesForActionCheck(...)` under Classical
navigation (`AiTurn.cs:336–354`), gates only the fallback after an executed command. The fallback for an army with no
command (`AiMilitaryPhase.cs:487–503`) runs on `mayMarch` alone, and `mayMarch` means only "has not marched yet this
seat" (line 352). In the original both cases go through the same AAB4 call in F31C.

**Fix for IC main:** apply the same full-allowance test to that path under Classical Faithful navigation. See
[`2026-11-02-remake-fixes-gaps-ab.md`](2026-11-02-remake-fixes-gaps-ab.md).

It shows only for an army with fewer than its full moves at its seat. One row in 40 turns, and none in the other four
games, where every fallback row was gap A after a command.

## Harness

`end_turn` now raises `GameOver` when End of Game opens after the autosave line (the human was overthrown), and
`difftest.campaign` stops cleanly after that turn. It was checked on Wine from the turn-26 start
(`turn26-repro/wine-v2-gameover`). The frozen battle window seen in the campaign
([turn-26 overthrow](2026-11-02-seleucid-turn26-overthrow.md)) is a different screen, and this change does not handle it.

## Open

- The remake army's own moves at seat start were not read; the probe's allowance is computed. Either way, the
  no-command path has no moves test.
- The other 14 position nation-turns of the Ptolemaic game are not stay-versus-move rows, and they are not attributed.
- D3 (#1732), code only, is unfixed in v0.9.1.
- The Ptolemaic port tile (3 fleet rows) and the hunt-score distributions.
- Why some battles happen in one game only (army side).

## Verified at intake

- The remake code at `0d9d4729`: both fallback paths, the `mayMarch` definition and the commit list.
- AAB4's formula, in the seed build's disassembly at 0x44AAB4–0x44AB0B.
- Hook seq 4–10, and the hooked and plain autosave hashes in `inert.json`, which are equal.
- The probe log lines for Galatia army 12 and Ptolemaic army 6.
- The anchored diff file, the `stays` outputs, and the recheck summary counts.
- Correction: the draft cites `report-v1.md`, but the recheck file is `report-v1.json`.
- Not re-checked: the row-for-row comparison with the v0.9.0 recheck, `classify.py`'s counts and the harness change.
- The tarballs were not downloaded.
- "The army had spent moves earlier" is the draft's reading of why it has 8 moves. This intake did not trace it.
