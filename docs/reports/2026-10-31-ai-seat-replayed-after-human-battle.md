# An AI seat is played twice when one of its attacks opens a battle with the human: the partial first pass is kept, then the whole seat runs again

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `493f80d` (PR #297). It came
up in the e20a6488 rerun ([below](2026-10-31-ai-rerun-remake-e20a6488.md)), from Carthage's fleet-0
row in S08 round 2.
- **Evidence:** the existing hook runs `run-exp-econ` (budget records), `run-exp-econ2` (`E41C`
  records) and `run-exp-routemoves159` (S08, seq 38–44). No new run was made.
- **Saves:** `S08_Celtiberia_AUTO0720.SAV`, with `hooked-t01-AUTO0721.SAV` → `hooked-t02-AUTO0722.SAV`
  for S08 round 2.

**Tag:** `[confirmed: code + Wine hook]`, seed build in Wine.

**Review note (2026-10-31):**
- **The flag `0x4A0B7C`, in my full disassembly:**
  - It is set to 1 at `0x43817F`, inside `FUN_00437de4` (battle setup), as drafted.
  - It is cleared at `0x437B8C`, the first instruction of a routine called from `0x439CDE` (in
    `FUN_00439c84`), and also at `0x448ACA` and `0x45C21F`.
  - **Discrepancy:** the draft names `FUN_00436434` as the clear at the battle's end. I could not
    connect that function to any of these clears; I did not trace the call chain further.
- **The army loop:** `F31C` tests the flag at the top of every iteration (`0x44F348`: `cmp byte
  [0x4A0B7C],0` / `jne` to the loop's step). So once it is set, the remaining armies are skipped.
- **The seat:** `FA20` still calls `F608` (`0x44FA51`). Then at `0x44FA56` it tests the flag and, if
  it is set, returns **without advancing the seat** (`0x44FA5D` → `ret`).
- **The dispatcher:** `FUN_00451fdc`'s loop runs only while the flag is 0 (call site `0x451FED`;
  see the [record lifecycle](2026-10-31-sav-export-record-lifecycle37.md) review note).
- **Hook logs:**
  - **Budget records** in `run-exp-econ`'s original logs (`budget` twice in the same seat-turn): exactly
    the 5 drafted seats. These are S01 r5 Celtiberia, S02 r4 Bithynia, S03 r1 Seleucid, S06 r2 Rome
    and S08 r2 Carthage.
  - **`E41C` records** in `run-exp-econ2`: only in S08 r2 does an army's supply pass appear twice
    (army 2, armies `[2, 2, 3]`). In the other four seats every army appears once. That is
    consistent with the attacking army dying in its battle, but I did not check each battle.
  - **S08 r2** (`run-exp-routemoves159`): seq 38 is army 2's walk at the human's army, `f31c-army>100`,
    with 9 moves. Seq 39 and 40 are the fleet phase: fleet 0 at (86,76), no route, 26 moves. Seq 41 is
    army 3's continuation (`f31c-e84c-city>85`, 9 moves). Seq 42 is the route write (86,77). Seq 44
    is the fleet phase again: fleet 0 at (83,78), stored route (86,77), 23 moves.
- **Remake** at `e20a6488`, `GameSession.cs`:
  - `AiPhaseBattleGate` (line 2270) applies only under `HumanBattleMode.Tactical`. The first time an
    AI attack on a human army is met, "the turn is abandoned"; on the replay, the fought battle's
    result is used.
  - `PlaySeatTurn` (line 2141) catches `AiPhaseBattleSuspended` and opens the battle.
  - Under Instant mode the attack is dispatched normally, with no interruption.
- **Not checked:** the draft's pass-1 and pass-2 budget figures (40,509 / 30,008, then 30,220 /
  15,000).

## The rule

1. An AI army's attack on a human's army (or another battle that goes through `FUN_00437de4`) sets
   the battle flag `0x4A0B7C`.
2. **The rest of that army phase is skipped:** `F31C` handles an army only while the flag is 0.
3. `FA20` still runs the **fleet phase** (`F608`). It then sees the flag and **does not advance the
   seat**, and the dispatcher stops.
4. The battle is fought. When it ends, the flag is cleared.
5. **`FA20` runs again for the same nation, from the start:** diplomacy, economy, every army's
   supply pass, the armies with moves, and the fleet phase.
6. **The first pass is not undone.** Its moves, its battle, and its fleet phase's moves stay in place,
   and the second pass plays on that state.

**S08 round 2, Carthage:**
- **Pass 1:** army 2 attacks the human's army at (34,63), and army 3 is skipped. The fleet phase sends
  fleet 0 toward port, (86,76) → (83,78), spending 26 → 23 moves.
- **Pass 2:** army 3's continuation (9 moves) needs a ferry. With fleet 0 now 2 tiles away, `D9A8`
  writes the route (86,77). The fleet phase then runs again and follows the stored route.

So the original's S08 r2 fleet-0 row comes from the seat replay, not from the continuation alone.
The draft adds that without the first pass's move the continuation would have embarked (distance 1);
that is inference.

**Seats played twice in 80 rounds:** 5, listed above. The draft names the human targets for S02 r4
(Seleucid army 5) and S08 r2 (Celtiberia army 10).

## The remake

- **Instant mode:** an AI attack on a human army does not interrupt the seat; the seat runs once.
- **Tactical mode** (`AiPhaseBattleGate`, `PlaySeatTurn`): the turn is abandoned at the attack and
  replayed from the **pre-turn** state, with the battle's result injected. The first pass's other
  effects (here, the fleet's move) are discarded.
- **Neither matches the original**, which keeps the partial first pass and then plays the whole seat
  again.

## What this does not establish

- **Other battle kinds:** which other paths reach `FUN_00437de4` and set the flag (sieges, naval
  battles, AI attacks on human cities).
- **The unpatched original:** the evidence is the seed build's hook runs in Wine.
- **The clear's exact routine** (see the review note).
- **Per-pass tallies** for the comparisons: they count a seat played twice as one seat.
- Rounds 6 and later, other seeds, and native Windows behaviour.
