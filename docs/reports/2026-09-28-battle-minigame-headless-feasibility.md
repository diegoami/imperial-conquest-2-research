# Battle minigame: research and replication through headless runs

> **Correction (2026-10-04)**, from [2026-10-04-decompiled-tactical-battle-rules.md](2026-10-04-decompiled-tactical-battle-rules.md):
>
> - The grid holds **icon codes** (`type·3 + size`, +20 for the defender, 50 empty), not slot indices.
> - Slot word `+2` is the unit's origin label (mercenary marker).
> - All 22 slot words are now named.
> - A lab snapshot is taken before the moving side's melee, and resuming one re-runs that side's half-round setup. A resume is therefore not a continuation.


**Question.** Can the tactical battle minigame (the grid battle screen, `TBattleMap`) be researched and replicated in the build repository's game from headless runs of the original? The method asked about: provoke battles, record them, and extract the rules according to who took part. The deliverable is this feasibility report.

**Answer: feasible, and better than the question assumed.** Three things this session proved on the running game (Wine 9.0, Xvfb, `fast` build with the autosave option from [2026-09-28-autosave-hook-feasibility.md](2026-09-28-autosave-hook-feasibility.md)) change what is possible. This project has so far treated a battle as "strongly stochastic", checkable only by distribution.

1. **A battle replays exactly.** Fix `RandSeed` when the battle starts, and two runs produce byte-identical battle state at every half-round, and a pixel-identical result dialog. This held even though the strategic turns around the battle differed.
2. **The whole battle state can be recorded.** A save written from inside the battle carries the SAV's battle block: every unit slot's position, type, troops, quality and battle-local **morale**, and the grid, once per half-round. No save has ever held this before.
3. **Scenarios can be injected.** Loading such a save resumes the battle. It resumes deterministically: two resumed runs were identical over 20 half-rounds. An **edited** save plays out from the edited state.

Together these support a stronger method than statistical rule extraction: a **golden master**. Decompile the battle code in full; it is bounded, at about 49 functions and 2,600 decompiled lines. Implement it in the build repository with Delphi's random-number generator. Then check it **half-round for half-round**, and with one more hook exchange for exchange, against the original on a corpus of seeded scenarios. Provoking battles and fitting rules by participant becomes the verification harness and the way to find surprises, not the primary source of the rules.

## 1. Where the research stands

The existing battle reports are summarised here; the detail stays in them.

- **Exact, from decompile plus recording:**
  - the melee loss cap `min(raw, ⌊0.4·troops⌋) + 1` ([battle-recording-melee-cap-confirmed.md](battle-recording-melee-cap-confirmed.md));
  - the rout threshold of half the standard battalion (600/240/140/280/100) and initial morale `clamp[60,90](Random(q·4) + army[+14])`, with `+3` for a computer side ([battle-replayed-rout-mechanic-and-combat-constants.md](battle-replayed-rout-mechanic-and-combat-constants.md), [battle-quality-promotion-and-morale-array-decompiled.md](battle-quality-promotion-and-morale-array-decompiled.md)).
- **Decompiled but only structurally checked:**
  - the type matrix ([combat-type-effectiveness-matrix.md](combat-type-effectiveness-matrix.md));
  - the power term `m·troops·(q·10+morale)/2000+12`, the focus/defence factors, and the shooting formula and its constants;
  - the morale deltas and the rout cascade.
- **Open:**
  - movement, initiative, target choice (the AI general);
  - surrender, capture of money and supplies, promotion (only modelled empirically);
  - terrain; the unknown slot word `+2` (`DAT_004a0348`).
- **Evidence so far:** 44 exchanges transcribed from two screen recordings, most of them from two battles fought from one starting state. Battle-local quality and morale never reached a save, so only the caps could be checked exactly.
- **The build repository** has no tactical model. Its instant resolver cannot reproduce a tactical battle ([instant-resolver-cannot-reproduce-a-tactical-battle.md](instant-resolver-cannot-reproduce-a-tactical-battle.md)).

## 2. The code a harness hooks into

Found this session from the executable and a fresh Ghidra 12.1.3 decompile:

```text
FUN_0044aee4(attacker, defender)            army attacks army (unit map, or AI seat)
  both nations computer  -> instant resolver (strategic code, no battle screen)
  otherwise              -> [0x4A0B74] = attacker, [0x4A0B76] = defender
                            0x44AF4E  call TPremierForm.StartBattle (0x45C178)
TPremierForm.StartBattle -> 0x45C1AE  call TBattleMap.StartBattle (0x436FB4)
TBattleMap.StartBattle:  if battle flag [0x4A0B7C] == 0: FUN_00437de4  (fresh: copy armies in, roll morale)
                         else                          : FUN_00439968  (resume: state from the loaded save)
OpenGameFile: if the loaded save's battle flag is set  -> 0x45AB72 call TPremierForm.StartBattle
ComputerGeneral -> FUN_00439c84: loop while the side to move is computer-controlled
                   (or has "Computer general" on) and the battle is not over:
                     FUN_00439ce8: placement FUN_004381a4 if not placed, else moves/targets
                     (FUN_0043a31c ...), then 0x439D06 call FUN_00439c20 (the half-round's end)
TBattleMap.EndTurn (human side): 0x437A94 call FUN_00439c20; call FUN_00439c84
```

- **Randomness.** `Random` (`0x40284C`, Delphi's LCG `seed = seed·0x08088405 + 1; result = (seed·n) >> 32`) is called from **12 sites** inside the battle code: copy-in 2, AI placement 1, rout 2, shooting 2, melee 4, `FUN_0043aa60` 1.
- **`RandSeed` is not in the save.** It lives at `0x45E030`, and **the load routine reseeds it from the clock** (`0x448AB0` → `Randomize` `0x402744`). So every load starts a new random stream. This is why two runs from one save diverge in the strategic turns. Earlier reports disagreed on whether replayed turns are deterministic; this settles the mechanism: they are not, unless the seed is fixed.

  > **Correction (2026-09-29):** the load routine does **not** reseed. `FUN_004487C4` (the loader) returns at `0x448AA0`. The `Randomize` call at `0x448AB0` is the first call of the **next** function, `FUN_00448AA4`, which is New Game's setup: [decompiled-new-game-mercenary-fill.md](decompiled-new-game-mercenary-fill.md) already names it. It is called only from the main form's `InitialiseForm` (`0x45A93A`, program start) and `NewGame` (`0x45AA32`). So `RandSeed` is seeded from the clock **at program start and at New Game**; a peace treaty also reseeds it ([decompiled-war-cascade-and-peace-paths.md](decompiled-war-cascade-and-peace-paths.md) §4).
  >
  > Runs A–E each started a fresh game process, which is why their strategic turns differed. The conclusions of §3 stand, because they rest on the seed being fixed at battle start. Found by the `ic2-conquest` bot session: loading one save twice in a single process with a fixed seed gives byte-identical turns ([2026-09-29-loading-a-save-does-not-reseed.md](2026-09-29-loading-a-save-does-not-reseed.md)), and confirmed here from the call sites.
- **Delay does not matter.** `Delay` (`0x448FFC`) is the only timing, so on the `fast` build a whole battle computes in 1.3–1.9 s, 13–20 half-rounds, including a 135 KB snapshot write each.

## 3. What was run (all from `1_rome_270_winter_11.sav`, `run-1-rome`)

The probe build is `IC2 lab.exe`: fast, plus autosave, plus the two hooks of Appendix A. Seed 12345.

| Run | Start | What it shows |
|---|---|---|
| A | Load the save, end the turn twice. On the second turn **Gaul's army (index 10) attacks Rome's (index 0)**, as in every earlier run from this save. Battle played with *Computer general on*. | 13 snapshots `BATTLE01…13.SAV`, 134,910 B each (the save plus the battle block) |
| B | Same as A, a fresh process | **Battle block identical in all 13 snapshots.** The 594 bytes that differ per file are all outside it: map, cities, news, army 12, nations and fleets, because the strategic turn is not seeded. **Result dialog: 0 differing pixels.** |
| C, D | Load `BATTLE01.SAV` from A, twice | The battle screen reopens mid-battle ("Rome to place units"). **C and D identical in all 20 snapshots, result dialogs 0 px apart.** They differ from A, as expected, because the seed is reset on resume. |
| E | `BATTLE01.SAV` with every attacker's troops halved and every defender's quality set to 9 | Loads and plays from the edited state: 13 half-rounds, and the outcome flips to "Rome's army defeats Gaul's army". |

What one snapshot holds, decoded from run A:

- **Header:** attacker army 10, defender army 0, side to move (`0x4A0B78`, alternating), a placed flag (`0x4A0B7D`), and a half-round counter (`0x4A0B7A`, 1…13).
- **Unit table:** 40 slots × 44 bytes (`0x4A0344`), 20 per side. Words: X, Y, `+2`, type, troops, quality, morale, …, target, then the unit's name. For example, slot 0 = `4th Guards Battalion`, type 1, 5,900 troops, quality 6, morale 63.
- **Grid:** 14 × 12 words (`0x4A0A24`), an occupancy map: 50 = empty, otherwise a unit slot. **No terrain value appears in it.** 18 cells changed between half-rounds 1 and 13.

Over run A the defender's minimum morale fell 61 → 30 and the attacker's maximum rose to 99, the cap in [battle-replayed-rout-mechanic-and-combat-constants.md](battle-replayed-rout-mechanic-and-combat-constants.md). These are the battle-local values no earlier evidence could see.

## 4. Provoking battles "by who took part"

Three routes, in order of control:

1. **Natural.** A strategic save in which an AI attacks next turn. Runs A and B show the attack itself repeats even though the strategic RNG does not; this save gives Gaul against Rome on the second end-turn every time. Cheap, but the participants are whoever the AI picks.
2. **Edited snapshot (route E): the workhorse.** Take any start-of-battle snapshot and rewrite the 40 slots: type, troops, quality, morale, positions (keeping the occupancy grid consistent), and which side is computer-controlled. **Any matchup the data format can express becomes a scenario file.** The strategic part of the save only has to be a valid game.
3. **Crafted from scratch.** Write a battle block into any save, with army indices and the placed flag chosen. **Not tested:** whether the resume path accepts an unplaced block (`0x4A0B7D = 0`) and runs placement itself, and how the post-battle write-back treats army records that disagree with the block. Route 2 does not need this.

"Who took part" maps onto the fields a scenario controls:

- nation: whether each side is human or computer, which carries the `+3` morale;
- per slot: unit type (5), troops, quality, morale (seeded from army `+14`), position;
- which side attacks.

The sweep design is **common random numbers**: the same seed, one field changed per run. With the seed fixed, a changed outcome is caused by the changed field, not by chance. Paired runs remain exactly comparable until the two random streams diverge. From that point, the exchange log (§6) re-derives every draw anyway.

## 5. Replicating it in the build repository

What the build repository needs:

- **A tactical rules engine:** placement legality, movement, shooting, melee, rout and cascade, morale, end conditions, surrender, and the post-battle write-back (losses, unity, promotion, capture). The write-back is visible in the autosave taken after the battle.
- **A tactical AI.** It is needed for the computer side, and for the player's *Computer general* button.

**Exact parity needs the same AI decisions and the same order of `Random` calls.** The AI chooses which exchanges happen, and every draw shifts the stream. Porting the rules and swapping in a redesigned AI would bring the verification back down to distributions. The scope note in [decompilation-plan.md](../decompilation-plan.md) (faithful rules, redesigned AI) was written for the *strategic* AI. The **tactical** general is small: `FUN_004381a4`, `FUN_00439ce8`, `FUN_0043a160`–`FUN_0043abb4` and their helpers are roughly a third of the ~2,600 decompiled lines of the battle form. The recommendation is to **port the tactical AI faithfully** as the reference behaviour. A redesigned AI can then sit behind a switch, verified against the same rules engine.

**The harness.** Each corpus entry is a scenario snapshot plus a seed.

1. Run the original: load the scenario, turn on *Computer general*. The lab build writes the snapshot sequence, and the exchange log once it exists.
2. Run the build repository's engine: read the same starting block and seed, and produce the same sequence.
3. Compare half-round by half-round, or exchange by exchange. **The first differing field names the rule that is wrong.**

This is a stronger test than anything the project has had: an exact diff against the original, on inputs chosen to exercise each rule.

**The corpus is evidence and stays out of both repositories**, as every save does. The natural home is a new `imp_conquest_fixtures` release, `battle-lab`, with scenarios, seeds and outputs. The build repository's tests would fetch it the way reports cite releases, or commit only derived numeric vectors.

## 6. What is not yet built or known

- **Exchange granularity.** A half-round snapshot can hold several exchanges. For exact per-exchange equations, a logging hook at the exchange call sites should write a compact record (acting and target slots, the unit table before and after, `RandSeed` before) to a binary log, the way the autosave writes its line:
  - melee `0x439C6A`;
  - shooting `0x437459` (human), and `0x438EE2`, `0x43A0C2`, `0x43A136`, `0x43A5CD` (AI);
  - rout `0x4392D1`, `0x4397E2`, `0x439829`.

  Because `Random(n)` is a pure function of the seed, logging the seed makes every roll inside an exchange **known**. Formulas are then fitted exactly, not statistically. Designed, not built.
- **The human path.** *Computer general* plays both sides through the AI. Manual play (`MoveHumanUnit` `0x43755C`, `OnMapClick` `0x437308`, whose shooting call is `0x437459`) shares the rules but has its own legality checks. It needs decompiling, and can be exercised headless by clicking grid cells: the grid origin and cell size can be read from the battle window.
- **Hook placement.** The half-round end must be hooked at the *call sites* (`0x439D06`, `0x437A94`). A first attempt that redirected `TBattleMap.EndTurn`'s published-method entry saw nothing, because with *Computer general on* the battle never passes through `EndTurn`: `ComputerGeneral`'s loop runs the whole battle.
- **Unlabelled fields.** Slot word `+2`, the header word at `0x4A0B7A` (a half-round counter by behaviour), and whether the grid ever holds anything but occupancy.
- **Other paths.** Surrender, and the instant resolver for computer-vs-computer battles, which is a separate code path.
- **Only one battle has been played so far**, from one strategic save, and only under Wine. Battle logic is pure computation, so Windows should not differ, but it has not been checked there.

## 7. Plan and estimate

| # | Task | Needs | Produces |
|---|---|---|---|
| 1 | Make the lab hooks a `patch_exe.py` option (`battle_lab`, on fast+autosave), seed from a file beside the executable | Appendix A | reproducible runs |
| 2 | Exchange log hook | the call sites in §6 | per-exchange records with `RandSeed` |
| 3 | Scenario tool: read and edit the battle block (slots, grid consistency, sides), and a headless batch driver that loads a scenario and plays it | block layout above; the xdotool driver from the autosave report | `battle-lab` corpus |
| 4 | Decompile the battle form fully: rules first, then the tactical AI (~49 functions) | Ghidra dump, grep per function | a rules specification report per subsystem |
| 5 | Implement in the build repository: rules engine plus the ported tactical AI plus Delphi's `Random` | 4 | tactical model |
| 6 | Golden-master comparison over the corpus; fix until 0 diffs, then targeted sweeps per participant field | 1–3, 5 | parity report |
| 7 | Human path and post-battle write-back, checked through the autosave after each battle | 4 | the remaining rules |

Tasks 1–3 are harness work of the size of the autosave task. Task 4 is the bulk; its size is known. Throughput is not a constraint: the battle itself takes about 2 s. The scripted load and clicks dominate at about 30 s with the current fixed sleeps. Reusing one process with *File → Open* per scenario, and running parallel Xvfb displays, gives hundreds of battles an hour.

**Go.** The most likely thing to break the plan is **scenario injection beyond edited snapshots** (route 3): a resume path that refuses an unplaced block, or a post-battle write-back that corrupts the strategic save when the block and the army records disagree. Route 2 avoids both, so the plan does not depend on it.

## Reproduction

The seeded replay and snapshots, the resume, and the edited scenario were all run on the lab build of Appendix A: Ubuntu 24.04, Wine 9.0, Xvfb, xdotool, driven as in the autosave report's §5. On the battle window:

- *Computer general on*: (158, 112) on the 1280×1024 screen;
- *End turn*: (110, 112);
- the result dialog's *OK*: (220, 478).

Snapshot comparison: `cmp -l` per file, and a byte classifier over the SAV sections from [decompiled-sav-file-layout.md](decompiled-sav-file-layout.md). Result dialogs compared with ImageMagick `compare -metric AE`. None of the snapshots is stored in a repository or release yet.

## Next checks

1. Build tasks 1–2 and repeat runs A and B with the exchange log: every exchange's rolls should be reproducible from the logged seed with the Delphi LCG.
2. Route 3: craft an unplaced block and see whether the game runs placement on resume.
3. Upload a first `battle-lab` release: run A's snapshots, the edited scenario, and seeds.

## Appendix A: the battle-lab probe

This is a probe, not a shipped patch. It builds on `patch_exe.py` with the autosave option from the autosave report's Appendix A applied. Put `lab.py` beside `patch_exe.py` and the original executable, then run `py lab.py [seed]`. It writes `IC2 lab.exe`, SHA-256 `fa21f33c212b5e95f91ff0e6753d8415b95a302d9602b6ebf977d9de0248f719` for seed 12345.

Offsets and bytes on top of fast+autosave:

- `0x45C1AE`: `E8 01 AE FD FF` → `E8 4D 82 10 00` (the seed cave at `0x564400`).
- `0x439D06`: `E8 15 FF FF FF` → `E8 15 A7 12 00`, and `0x437A94`: `E8 87 21 00 00` → `E8 87 C9 12 00`. Both become calls to the snapshot cave at `0x564420`.
- `.patch` characteristics (raw `0x35C`): `60000020` → `E0000020`, writable, because the cave keeps a counter at `0x5645F0` and the player's file name at `0x564580`.
- Snapshot saves go to `BATTLEnn.SAV` in the current directory. They are written without a `try`: a probe, unlike the autosave.

```python
# Battle-lab probe (not a shipped patch): fast + autosave, plus a fixed battle
# seed and a snapshot save at every half-round of a tactical battle.
#   py lab.py [seed]      -> "IC2 lab.exe" next to the original
import struct, sys
import patch_exe as P

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
RAND_SEED = 0x45E030                    # System.RandSeed
BATTLE_START_CALL = 0x45C1AE            # TPremierForm.StartBattle: call TBattleMap.StartBattle
TBATTLE_START = 0x436FB4                # also the resume path when a battle save is loaded
ROUND_END = 0x439C20                    # end of one side's half-round (melee phase)
ROUND_END_CALLS = (0x439D06, 0x437A94)  # computer side / TBattleMap.EndTurn (human side)
SEED_CAVE, SNAP_CAVE, SAVED, COUNTER = 0x564400, 0x564420, 0x564580, 0x5645F0


def battle_lab(b):
    # RandSeed := SEED whenever a battle starts or resumes; before every
    # half-round, save to BATTLEnn.SAV (the save then carries the battle block).
    raw = lambda va: va - P.EXTRA_VA + P.EXTRA_RAW
    seed = P.assemble(SEED_CAVE, [b"\xC7\x05" + struct.pack("<II", RAND_SEED, SEED), ("jmp", TBATTLE_START)])
    snap = P.assemble(SNAP_CAVE, [
        b"\x60\xFE\x05" + struct.pack("<I", COUNTER),                    # pushad; inc byte [COUNTER]
        b"\xBE" + struct.pack("<I", P.FILE_NAME), b"\xBF" + struct.pack("<I", SAVED),
        b"\xB9\x64\x00\x00\x00\xF3\xA4",                                  # SAVED = FILE_NAME
        b"\xBF" + struct.pack("<I", P.FILE_NAME),                        # FILE_NAME = "BATTLEnn.SAV"
        b"\xC7\x07BATT\xC7\x47\x02TTLE\xC7\x47\x08.SAV\xC6\x47\x0C\x00",
        b"\x0F\xB6\x05" + struct.pack("<I", COUNTER), b"\xD4\x0A\x66\x05\x30\x30",   # movzx; aam; add ax,'00'
        b"\x88\x67\x06\x88\x47\x07",
        ("call", P.SAVE_GAME),
        b"\xBE" + struct.pack("<I", SAVED), b"\xBF" + struct.pack("<I", P.FILE_NAME),
        b"\xB9\x64\x00\x00\x00\xF3\xA4",                                  # FILE_NAME = SAVED
        b"\x61", ("jmp", ROUND_END)])
    b[raw(SEED_CAVE):raw(SEED_CAVE) + len(seed)] = seed
    b[raw(SNAP_CAVE):raw(SNAP_CAVE) + len(snap)] = snap
    b[raw(COUNTER)] = 0
    struct.pack_into("<I", b, P.EXTRA_HEADER + 36, 0xE0000020)          # .patch writable (counter, SAVED)
    P.patch(b, BATTLE_START_CALL, b"\xE8" + P.rel32(BATTLE_START_CALL, TBATTLE_START),
            b"\xE8" + P.rel32(BATTLE_START_CALL, SEED_CAVE))
    for site in ROUND_END_CALLS:
        P.patch(b, site, b"\xE8" + P.rel32(site, ROUND_END), b"\xE8" + P.rel32(site, SNAP_CAVE))


P.build("IC2 lab.exe", P.async_sound, P.no_delay, P.autosave, battle_lab)
```
