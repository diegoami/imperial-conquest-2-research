# Faithful AI: the remake supports and hires for every army up front outside the tactical gate; the original does it per army (audit #195, X2)

**Tag:** [confirmed: disassembly of the seed build; anchored remake replays of a stored original game, 3 seeds × 2
modes]. Wine only for the original side (the stored game).
**Provenance:** draft from `diegoami/ic2-conquest`, `findings/2026-11-05-x2-support-pass-timing.md`, commit `89cf67e3`
(PR #332, main `b44ed2a2`). Remake pin `168dbc04` (v0.9.4, T277). Ruleset `classical-faithful`.
**Task:** research #195 (comprehensive AI audit), cross-cutting difference X2 of the
[inventory](2026-11-04-ai-audit195-inventory.md) (rows A09, B22, C08). Written as a remake issue candidate.

## The rule in the original

`FUN_0044f31c` (the army phase) calls `FUN_0044e41c` (support and hire) as each army's first call, at `0x44F366`
(`call 0x44e41c`). Army k's resupply, transfers and mercenary hire therefore see the state left by armies 0..k−1 of the
same seat: their moves, battles, conquests and the money they spent.

## The remake at `168dbc04`

- `src/IC2.Engine/Ai/AiTurn.cs:142`: `retainedPass = commands is IAiBattleInterruption { RetainPartialAiPass: true }`.
- `AiTurn.cs:186`: when `retainedPass` is false, `AiMercenaryHirePass.Run` supports and hires for **every army up front**,
  before any army moves.
- `AiTurn.cs:251`: when it is true, `ProposeInOriginalArmyOrder` gets `PrepareArmy`, which runs the pass per army: the
  original's timing.

`RetainPartialAiPass` is true only under `GameSession`'s `AiPhaseBattleGate` built with a battle identity
(`Presentation/GameSession.cs:2315`). `PlaySeatTurn` (line 2163) builds that gate only when `UsesAiPhaseBattleGate()`
(line 2398) holds, and passes the identity only when `ClassicalArmyNavigation.Applies`. So the per-army path needs all of:
- `HumanBattles == Tactical`;
- not watch mode;
- a living human seat;
- the Faithful (classical) army navigation.

No pending battle is needed. **Instant battles, the CLI, and every headless, anchored or observer run take the up-front
pass.**

## Minimal trigger

Stored game `greece-rulebot1-40t` (release `run-exp-longrun-v092`), turn 21, from the original's start save `t20-a01.SAV`.
The human's only order is a recruit. No battle opens in either mode. Seat: Seleucid, with two armies near Antioch (221,60)
of 27,113 and 20,400 men. Probe: `runs/experiments/audit195/x2_mode_probe.py`, seeds 12366, 12345 and 99.

| | 27,113-man army | 20,400-man army |
|---|---|---|
| **Original** (stored game, t21 end) | stays at Antioch (221,60) | (221,64) |
| **Remake, Tactical** (per-army pass), 3 seeds | (221,60) | (221,64): matches |
| **Remake, Instant** (up-front pass), 3 seeds | **(221,64)** | **(222,64)** |

Every other nation is equal in both modes, and the result doesn't depend on the seed. In this turn the mode switch
changes only where the support pass runs. The flag's other readers act only on an opened or pending battle, and none
opened. So the up-front pass is the cause (settled from the code at intake: [inventory](2026-11-04-ai-audit195-inventory.md),
pass-1 intake, research PR #204).

## Expected, actual, fix

- **Expected (original):** each army's support and hire runs when that army's turn comes, after the earlier armies have
  moved.
- **Actual (remake, outside the tactical gate):** every army is supplied before any of them moves.
- **Candidate fix:** run the per-army `PrepareArmy` path in every Faithful mode, not only when a tactical battle could
  interrupt the seat. The Tactical path already has the original's timing; only its gate is narrower than the rule.

## Scope

- **Not the cause of the other 11 stays rows.** In `x2-stays-v1` each gives the same result in both modes on all 3 seeds.
  They are not X2, and they stay unattributed (inventory, pass 1).
- **Every anchored replay so far ran outside the gate.** Some earlier AI-phase residuals may include X2 effects that were
  never separated.
- **Open:** the mechanism inside the hire pass (which purse or troop count differs when army 1 is supplied before army 0
  moves) was not traced.

## Intake verification (research, 2026-11-05)

**Checked:**
- **The original:** the call `e8 b1 f0 ff ff` at `0x44F366` targets `0x44e41c` (`objdump -d -M intel`, seed build).
- **The remake at `168dbc04`:** `AiTurn.cs` lines 142, 186 and 251 read as cited. The gate's construction is at
  `GameSession.cs:2163–2166` and `UsesAiPhaseBattleGate` at 2398–2401. Every reader of `RetainPartialAiPass` was grepped
  under `src`.
- **`x2-greece-t21-v1/result.json`:**
  - Instant mode: on each seed, only Seleucid differs, with exactly the positions in the table.
  - Tactical mode: no nation differs on any seed.
- **`x2-stays-v1`:** in all 11 results files, each seed gives the same differing set in both modes (3 seeds each).

**Corrected:** the draft's wording precision ("the gate needs Faithful plus Tactical, not a human seat … as such") is
half right. No pending battle is needed. But `UsesAiPhaseBattleGate` does require a living human seat, and it excludes
watch mode. So an observer game with Tactical battles also takes the up-front pass.

**Not checked:** the probe script itself; the saves archive's hash.

## Evidence

- `runs/experiments/data/run-exp-audit195/x2-greece-t21-v1/result.json` and `x2-stays-v1/` (conquest); hashes in
  `SAVES.sha256`.
- Saves: release `run-exp-audit195`, `audit195-x2-saves.tar.gz`. The original game: release `run-exp-longrun-v092`,
  `greece-rulebot1-40t-saves.tar.gz`.
- Tooling: `runs/experiments/audit195/x2_mode_probe.py`, `x2_stays_batch.sh`.
