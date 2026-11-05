# Faithful AI: the remake's Tactical retained pass replays an interrupted AI seat like the original; Instant play has no replay (audit #195, X3)

**Tag:** [confirmed: remake replays of the original's round-start saves, against the original's hook logs and end saves].
Remake only. The original side is the hook runs of 2026-10-31; no new Wine run.
**Provenance:** draft from `diegoami/ic2-conquest`, `findings/2026-11-05-x3-seat-replay-remake.md` (PR #336, merge
`cb9b2b2f`). Remake pin `168dbc04` (v0.9.4). Ruleset `classical-faithful`.
**Task:** research #195, cross-cutting difference X3 of the [inventory](2026-11-04-ai-audit195-inventory.md): an AI seat
replayed after a human battle (pass 1, step 5). Until now the remake had never been measured end to end on this path,
because every anchored replay runs in Instant mode.

## The original

From the [seat-replay report](2026-10-31-ai-seat-replayed-after-human-battle.md): an AI army's attack can open a battle
with the human's army.
- The battle flag `0x4A0B7C` stops `F31C`: the seat's remaining armies are skipped, and the fleet phase still runs.
- After the battle, `FA20` runs the same seat again on the current state: diplomacy, the economy, every army's support
  pass, the armies with moves left, and the fleets.

Five seats did this in the 2026-10-31 hook runs: S01 r5 Celtiberia, S02 r4 Bithynia, S03 r1 Seleucid, S06 r2 Rome and
S08 r2 Carthage.

## Method

`x3_seat_replay.py` plays each seat's round on the remake from the original's round-start save:
- the human gives no orders;
- modes Instant and Tactical, seeds 12345, 99 and 7;
- a battle that opens is fought for the human by the computer general (`battle general on`).

The conquest adapter gained an opt-in `ailog` option. It writes each `AiTurnDecided` (one per AI pass: orders and the
AI's log lines) to the receipt. The default behaviour is unchanged; this is a harness change, not a remake change.

## Results

**1. Structure.** All 15 Tactical runs play the seat in two passes, and all 15 Instant runs in one. In Tactical:
- pass 1 ends with "army phase interrupted; retaining the fleet pass", then runs support, hire and fleets;
- pass 2 runs the Faithful economy again, the armies with moves left, and the fleets.

**2. The economy (own / threat).**

| seat | original pass 1 | remake pass 1 (3 seeds) | original pass 2 | remake pass 2 (s12345 / s99 / s7) |
|---|---|---|---|---|
| S01 r5 Celtiberia | 14,973 / 42,027 | identical | 0 / 32,514 | 0 / 33,837; 0 / 32,451; 0 / 30,561 |
| S02 r4 Bithynia | 24,290 / 45,836 | identical | 9,638 / 41,216 | 9,638 / 37,784; 11,018 / 31,448; 9,638 / 38,444 |
| S03 r1 Seleucid | 30,836 / 96,707 | identical | 27,721 / 84,431 | 26,247; 27,855; 27,453 / 84,431 |
| S06 r2 Rome | 33,530 / 30,990 | identical | 28,361 / 15,000 | 26,171; 28,580; 27,558 / 15,000 |
| S08 r2 Carthage | 40,509 / 30,008 | identical | 30,220 / 15,000 | 29,590 / 15,000; 23,290 / 17,546; 28,470 / 15,000 |

- Pass 1 matches exactly in all 15 runs.
- Pass 2 exists and runs on the state after the battle. Its values differ by the battle's casualties, because the
  remake's tactical battle is not the seed build's instant battle.

**3. End tiles of the seat's units** (troops ignored):

| seat | Tactical (s12345 / s99 / s7) | Instant (all 3 seeds) |
|---|---|---|
| S01 r5 | match / match / match | match |
| S02 r4 | match / army 11 survives / match | army 11 survives at (173,48) |
| S03 r1 | match / match / match | army 5 at (178,47); original (178,48) |
| S06 r2 | match / match / match | army 0 stays at (94,29); in the original's pass 2 it joins army 1 |
| S08 r2 | match / army at (35,63) destroyed / match | army 3 embarks at (86,76) and fleet 0 stays; original army 3 at (88,79), fleet 0 on its route at (86,77) |

- **Tactical matches in 13 of 15 runs.** The two misses are battles with a different outcome.
- **Instant matches in 3 of 15** (S01 only).
  - In S03, S06 and S08 it misses what the original's second pass does. S08 Tactical reproduces the traced sequence:
    fleet 0 goes to port in pass 1, then pass 2 writes the route (86,77).
  - S02's Instant row is the battle outcome, not the replay. The seed build's instant battle is the fixtures' patch, not
    an original rule, so it is noted for X6 and not claimed.

**4. Diplomacy draws in pass 2 (E18, A13): not observable.**
- No war, alliance or peace roll fired in any of the 30 runs.
- One trade swap (S08 s99) moved from Instant pass 1 to Tactical pass 2. The end state was the same, and the original
  didn't swap there. It is a draw.
- Whether pass 2 draws fresh, as in the original, stays unaudited. It needs a seat where a war or alliance roll fires in
  pass 1.

**5. Capital defence while the battle is pending.** In S03 and S06 Tactical, pass 1 logs a second capital-defence move
after the attack. That is T277's `continuePending` (#1741). The end tiles match the original. These are the first stored
runs that exercise #1741.

## What it settles

- **The remake's Tactical retained pass matches the original's seat replay** in structure, in the pass-1 economy, and in
  end tiles wherever the battle ends as in the original (5 of 5 seats).
- **Instant, headless and observer play have no replay.** It is the same gate as X2: `UsesAiPhaseBattleGate` needs
  Tactical battles, a living human seat and no watch mode. Those seats differ wherever the second pass would have moved
  something: 3 of 5 here.
- **Candidate fix:** in Faithful, interrupt and replay the seat whenever an AI attack on the human's army opens a battle,
  whatever the battle mode. In Instant, resolve the battle at the interruption point, then run the second pass. This is a
  design proposal, not tested.
- **Not settled:**
  - E18/A13, the pass-2 draws;
  - D19, a stored route surviving into pass 2 when pass 1 already stored one;
  - battles other than an AI attack on the human's army.

## Intake verification (research, 2026-11-05)

**Checked:**
- **`passes.jsonl`** (30 runs):
  - every run exits 0;
  - every Tactical run has 2 passes and logs "army phase interrupted", and every Instant run has 1;
  - every pass-1 economy line and every remake pass-2 value is as tabled.
- **The original's hook logs** (`run-exp-econ/orig-v1/*-econ.jsonl`): for each of the five seats, the budget record
  equals the remake's pass 1, and the same nation's next budget in that turn is the original pass 2 tabled above.
- **`positions.jsonl`** (30 rows):
  - Tactical: 13 empty diffs. S02 s99 is the remake-only army at (173,48); S08 s99 is the original-only army at (35,63).
  - Instant: S01 matches on 3 seeds; S02, S03, S06 and S08 differ as tabled.
- **The inventory totals** in PR #336 sum to 229, the row count.

**Narrowed:**
- "Matches in state" means end tiles of the seat nation's units only: troops are ignored, and pass 2's budgets differ by
  casualties.
- That the two Tactical misses come from the battle outcome is an inference from which army survives. It is not traced
  in the receipts.

**Not checked:**
- the scripts and the adapter change;
- the per-run receipts beyond the AI pass lines;
- the capital-defence log lines of S03 and S06;
- the inventory row moves themselves.

## Evidence

- `runs/experiments/data/run-exp-audit195/x3-seat-replay-v1/` (conquest): `passes.jsonl`, `positions.jsonl`, and per run
  `commands.txt`, `receipt.jsonl` and `stderr.txt`; hashes in `SAVES.sha256`.
- Saves:
  - remake: release `run-exp-audit195`, `audit195-x3-saves.tar.gz`;
  - original round starts and ends: release `run-exp-aidecide` (`aidecide-saves.tar.xz`), and `run-exp-civ-sweep`
    (`S03_Ptolemaic_AUTO0720.SAV`).
- Original hook logs: `runs/experiments/data/run-exp-econ/orig-v1/*-econ.jsonl`.
- Tooling: `runs/experiments/audit195/x3_seat_replay.py`, `x3_positions.py`; the adapter's `ailog` option.
