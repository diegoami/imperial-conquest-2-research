# The neighbour mask is in the DAT: nation +0x46 is loaded, never derived, and only conquest changes it

**The question** (dev-repo PR [#377](https://github.com/diegoami/imperial_conquest_2/pull/377), task T82): nation record `+0x46` is a symmetric 16-bit neighbour mask, and the AI's diplomacy reads it ([decompiled-ai-offers-to-human-seats.md](decompiled-ai-offers-to-human-seats.md) §1a, §1b). That report says where the mask is built "was not traced". T82 derives the relation geometrically instead, with a Voronoi over the starting city map. Is the mask in the DAT the scenario loads? And does anything recompute it during play?

All line numbers are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt` unless another file is named. Record bases: nation `0x00474670` (stride `0x494`), so field `+0x46` of nation `n` is `0x004746B6 + n × 0x494`. City `0x00479590` (stride `0x22`).

## Answer

1. **Yes, the mask is in the DAT, at nation-record offset `+0x2B`** (43), 2 bytes, little-endian `[confirmed: decompile + bytes]`. The DAT loader `FUN_004481A0` reads the 11-byte name, then 32 bytes into runtime `+0x26`, then **2 bytes into runtime `+0x46`**. On disk that is `11 + 32 = 43`. The absolute address for nation `i` is `0x1B12B + i × 1,055`. The relation-row shift `0x26 − 0x0B = 0x1B` gives the same answer, but here it is read from the loader, not assumed.
2. **The DAT mask is symmetric, has no self-bits and holds 24 pairs** `[confirmed: bytes]`. The full table is in §2. **All 16 rows are identical in every one of the 101 local saves**, including the three rows the offers report checked: Rome, Carthage and Thracia `[confirmed: saves]`.
3. **Three routines write `+0x46`, and only one of them during play** `[confirmed: decompile + whole-program instruction scan]`:
   - the DAT loader `FUN_004481A0` at New Game (and at program start);
   - the SAV loader `FUN_004487C4`, as part of the 0x4940-byte nation block;
   - **the conquest routine `FUN_0044C528`**, which merges the loser's neighbours into the winner's mask and sets the winner's bit in each of those neighbours' masks.

   Nothing else writes it. Defection elimination (`FUN_0044BED8`), rebirth (`FUN_0044C360`) and New Game's leader draw (`FUN_00448AA4`) all leave it untouched. There is no map pass. **Five places read it:** the AI's war pick and treaty picks (`FUN_0044FB7C`, twice), the offer roll (`FUN_00452034`), the quarterly rebellion's choice of recipient (`FUN_0044C204`, newly identified here), and the peace cascade (`FUN_00450C68`, also new here).
4. **The T82 derivation reproduces all 24 DAT pairs and adds 6 the original lacks** `[confirmed: engine run against the DAT]`. The three extras already known are really absent from the original: Rome–Greece, Thracia–Bithynia and Thracia–Seleucid. Three more were not known: **Seleucid–Macedonia, Seleucid–Greece and Ptolemaic–Greece**. No DAT pair is missing from the derivation.
5. **A reimplementation should load the mask from the DAT** into the world file, as T75 did for the relation matrix. That removes the geometric derivation and its six false pairs. **It must also apply the conquest merge**, because the original does rewrite the field after setup. The derivation's remark that the field is one "the original never rewrites after scenario setup" is not correct. See §6.

## 1. The loader reads it: `FUN_004481A0` `[confirmed: decompile + listing]`

`FUN_004481A0` is not in `all_app_functions.txt`. Ghidra's saved analysis leaves `0x00447B83 … 0x004484CF` undisassembled, which is also why the dump has no entry for it. Its decompile is in `%LOCALAPPDATA%\ReTools\scratch\datload.txt`, and the per-nation loop is at lines 189–213:

```c
for 16 nations, rec = 0x00474670 + i × 0x494:
    Read(rec,          0x0b);    // name              DAT +0x000
    Read(rec + 0x26,   0x20);    // relation row      DAT +0x00B
    Read(rec + 0x46,   2);       // neighbour mask    DAT +0x02B   <- datload.txt:195
    Read(rec + 0x48,   0x29c);   // city list etc.    DAT +0x02D
    Read(rec + 0x2e4,  0x140);   // recruitment       DAT +0x2C9
    ...                          // wealth +0x409, treasury +0x40D, unity +0x411 ... tax base +0x41B
```

The running sum reaches the offsets `IC2.Data/DatLayout.cs` already uses: `0x2C9` for recruitment, `0x409` for wealth and `0x40D` for treasury. So `+0x2B` sits exactly between the relation row and the next read. The whole-program scan in §3, with the gaps force-disassembled, finds the instruction `0x00448285 LEA EDX,[ESI + 0x46]`, the destination argument of that third `Read`.

**Callers.** `TPremierForm_InitialiseForm` (:57994) runs the DAT loader at program start. `TPremierForm_NewGame` (:58032) runs it again at every New Game, followed by `FUN_00448AA4`, which draws leaders and clears the human flag and does not touch `+0x46` (§3). The build repo's `docs/investigations/dat-file-layout.md` table already lists "`+0x046` | 2 | —": the read was known, but the field was not named.

## 2. The mask in the DAT `[confirmed: bytes]`

The DAT is the local `Imperial Conquest 2.dat` (140,706 bytes), with the nation table at `0x1B100` and a stride of 1,055. Names are the DAT's own, at record `+0`. Bit `j` of nation `i`'s word means that `i` borders `j`.

| # | Nation | DAT word (`+0x2B`) | Neighbours |
| ---: | --- | --- | --- |
| 0 | Rome | `0x0242` | Carthage, Gaul, Illyria |
| 1 | Carthage | `0x0129` | Rome, Ptolemaic, Numidia, Celtiberia |
| 2 | Seleucid | `0x7808` | Ptolemaic, Bithynia, Galatia, Armenia, Media |
| 3 | Ptolemaic | `0x0006` | Carthage, Seleucid |
| 4 | Macedonia | `0x8680` | Greece, Illyria, Dacia, Thracia |
| 5 | Numidia | `0x0002` | Carthage |
| 6 | Gaul | `0x0701` | Rome, Celtiberia, Illyria, Dacia |
| 7 | Greece | `0x0210` | Macedonia, Illyria |
| 8 | Celtiberia | `0x0042` | Carthage, Gaul |
| 9 | Illyria | `0x04D1` | Rome, Macedonia, Gaul, Greece, Dacia |
| 10 | Dacia | `0x8250` | Macedonia, Gaul, Illyria, Thracia |
| 11 | Bithynia | `0x3004` | Seleucid, Galatia, Armenia |
| 12 | Galatia | `0x0804` | Seleucid, Bithynia |
| 13 | Armenia | `0x4804` | Seleucid, Bithynia, Media |
| 14 | Media | `0x2004` | Seleucid, Armenia |
| 15 | Thracia | `0x0410` | Macedonia, Dacia |

- **Symmetric:** bit `j` of `i` equals bit `i` of `j` for all 256 cells. **No nation has its own bit.** Bits 16 and up do not exist: all 16 nations fit in the word.
- **The 24 pairs:**
  - Rome: Carthage, Gaul, Illyria.
  - Carthage: Ptolemaic, Numidia, Celtiberia.
  - Seleucid: Ptolemaic, Bithynia, Galatia, Armenia, Media.
  - Macedonia: Greece, Illyria, Dacia, Thracia.
  - Gaul: Celtiberia, Illyria, Dacia.
  - Greece–Illyria, Illyria–Dacia, Dacia–Thracia, Bithynia–Galatia, Bithynia–Armenia and Armenia–Media.
- **It looks like a hand-authored frontier graph, not a distance rule** `[derived]`. The T82 remarks measure the geometry. Carthage–Ptolemaic is in the mask with the capitals 98 tiles apart, while Rome–Greece is not, despite Greek cities two tiles from Roman ones. Thracia–Bithynia, across the Bosphorus, is not in it either.

### Against the saves `[confirmed: saves]`

A Python reader locates the SAV nation table at `89,600 + 11,356 + 2 + armies × 656 + 2 + fleets × 26` and reads `+0x46` from each 1,172-byte record, with the calendar taken from the 55-byte tail. It covered **all 101 local saves**:

- `saves\` (50): `1_rome_270_winter_3/5/11`, `IP000 … IP021B` and `discarded\`;
- `saves-processed\` (51): the `1.sav … 12_rom_a.sav` legacy probes, and the `1_rome_270_*`, `1_cartago_271_*` and `1_thracia_271_*` runs.

**In every save, all 16 names match the DAT's and all 16 masks equal the DAT word.**

| Save | Calendar (tail) | Rows compared | Result |
| --- | --- | --- | --- |
| `1_rome_270_winter_11.sav` | 270 BC, winter, week 11 (latest) | all 16, incl. Rome and Carthage (report's rows) | = DAT |
| `1_thracia_271_summer_9.sav`, `_11.sav` | summer | all 16, incl. Thracia (report's row) | = DAT |
| `1.sav`, `IP000.sav`, `1_cartago_271_spring_1.sav`, `1_thracia_271_spring_1.sav` | 270 BC, spring, week 1 (earliest) | all 16 | = DAT |
| `IP000.sav` … `IP021B.sav` (Ptolemy run) | spring week 1 to winter week 7 | all 16 | = DAT |
| every other save | — | all 16 | = DAT |

**The one conquest in the set does not test the merge.** Galatia is dead, conquered by Seleucid, in 6 saves, from `1_rome_270_winter_7.sav` on. Its mask is {Seleucid, Bithynia}, so the merge (§4) would give Seleucid the Bithynia bit it already has, and Bithynia the Seleucid bit it already has. The unchanged masks agree with the merge, but they would look the same without it `[confirmed: saves; the merge is untested by them]`.

## 3. Every reader and writer of `+0x46` `[confirmed: whole-program instruction scan]`

**Method.** A headless Ghidra post-script ran in a `-readOnly` session, so nothing was saved. It first force-disassembled every undisassembled run in the `CODE` block (`0x401000–0x45C3FF`), because the saved analysis leaves about 140 KB of it as raw bytes, `FUN_004481A0` among them. It then flagged every instruction with any of these:

- an absolute operand equal to `0x004746B6` or `0x004746B7` plus `n × 0x494`, for n = 0…15;
- a memory operand `[reg (+ reg×s) + 0x46]` or `[… + 0x47]`;
- an `ADD reg,0x46` or `ADD reg,0x47`.

Hits in library code below `0x420000` (`FUN_004178A8`, `FUN_00417968`, `0x0040B096`, TControl fields) and misdisassembled string bytes (`IMUL …,0x7465656c`) were discarded. What remains:

| Address | Function | Access | Role |
| --- | --- | --- | --- |
| `0x00448285` | `FUN_004481A0` (DAT load) | `LEA EDX,[ESI+0x46]` → `Read(…,2)` | **write**, New Game / program start |
| — | `FUN_004487C4` (SAV load, `save_load_impl.txt`:55) | `Read(0x00474670, 0x4940)` block | **write**, from the save |
| — | `FUN_004484D0` (SAV save, :47491) | `Write(0x00474670, 0x4940)` block | read, into the save |
| `0x0044C6A4`, `0x0044C6C7`, `0x0044C6DA` | `FUN_0044C528` (conquest, :50600) | `BT` loser, `BTS` winner, `BTS [EBP]` neighbour | **write**, the merge (§4) |
| `0x0044C2E8` | `FUN_0044C204` (rebellion, :50432, test :50477) | `BT [EBP+0x46],EAX` | read (§5) |
| `0x0044FCC5` | `FUN_0044FB7C` (AI turn, :53296, test :53355) | `BT [EBX+0x46],EAX` | read: war pick, `me ∈ neighbours(k)` |
| `0x0044FDA4` | `FUN_0044FB7C` (test :53388) | `BT [EAX+0x46],EDX` | read: treaty picks, `j ∈ neighbours(me)` |
| `0x00450FCF`, `0x0045107C` | `FUN_00450C68` (peace, :54049, loop :54163–:54201) | `MOV ESI,0x4746B6` then `BT [ESI],…` | read (§5) |
| `0x00452150` | `FUN_00452034` (offer roll, :54960, test :55019) | `BT [EBX+0x46],EAX` | read: alliance offer, `r ∈ neighbours(h)` |

- **Not the mask:** `FUN_0044B8F4` (:50038, `0x0044B975`, `0x0044B9F7`) addresses `base + 0x46 + count × 2`. That is the last slot of the city list at `+0x48`, indexed from 1, with the count at `+0x446`.
- **Absent:** there are no hits in `FUN_0044BED8` (defection, including its elimination block), `FUN_0044C360` (rebirth), `FUN_00448AA4` (New Game's leader and turn-order draw), `TPremierForm_StartTurn`, the quarterly pass or any form handler. **The mask changes during play only through conquest.**

## 4. The conquest merge, `FUN_0044C528(loser, winner)`, :50673–:50696 `[confirmed: decompile + listing]`

Registers in the listing: `EDI` = loser, `ESI` = winner, `EBX` = k, and `EBP` = `0x004746B6 + k × 0x494`.

```c
for k in 0..15:                                            // 0x0044C685
    setRelation(loser, k, 0);                              // FUN_00449B40, the relation reset
    if (bit(mask[loser], k) && k != winner) {              // 0x0044C6A4 BT, 0x0044C6AE CMP SI,BX
        mask[winner] |= 1 << k;                            // 0x0044C6C7 BTS
        mask[k]      |= 1 << winner;                       // 0x0044C6DA BTS [EBP]
    }
```

- **The merge keeps the mask symmetric.** It only adds bits, and adds them in pairs.
- **The loser's own word is not cleared, and nobody loses the loser's bit.** The dead nation still borders its old neighbours. That matters only after rebirth.
- **The winner does not gain the loser as a neighbour** if it was not one already: `k = loser` is never in the loser's own mask.
- **The defection path merges nothing.** A nation emptied by `FUN_0044BED8` leaves every mask as it was.
- **Rebirth restores nothing and clears nothing** (`FUN_0044C360`, no `+0x46` access). A reborn nation keeps its DAT-era mask plus nothing, while its conqueror keeps the neighbours it inherited.

## 5. Two readers the earlier reports did not connect to the mask `[confirmed: decompile + listing]`

**The quarterly rebellion, `FUN_0044C204`.** [city-population-growth.md](city-population-growth.md) calls the bitmask "unidentified". A non-capital city under 30 loyalty goes to its allegiance nation. If it already belongs to that nation, it goes to a nation at war with the owner that has an army within 10 tiles. **Failing that, it goes to the best nation `n` whose mask has the owner's bit** (so a neighbour of the owner) **with unity > 0**, scored `cities(n) − 2 × distance(city, capital(n))`, via `FUN_0044BED8`.

**The peace cascade, `FUN_00450C68(winner, loser)`**, final loop at `0x00450F79` (`EBP` = winner, `EDI` = loser, `ESI` = nation k's `+0x46`):

```c
for k in 0..15:
    if rel[winner][k] == 2 && rel[loser][k] == 3:          // k is the winner's ally, at war with the loser
        setRelation(winner, k, -8);                        // 0x00450FBF
        if !bit(mask[k], loser) && human[k] == 0:          // 0x00450FCF BT [ESI]; 0x00450FD4 [ESI+0x44A] = +0x490
            setRelation(loser, k, -8);                     // 0x00450FE8
            news("<loser> and <k> have agreed to end their war.")
    // mirror: k is the loser's ally at war with the winner, with winner and loser swapped (0x00451037 …)
```

**An ally makes peace alongside its partner only if it does not border the enemy and is not human.** A bordering ally stays at war. This refines the peace report's closing line, "any ally of either side still at war with the other gets `setRelation(..., -8)`". Read literally, the listing also resets the **winner–ally** alliance to `−8` before the mask test. That is outside this report's question and is left for the peace report to re-check `[confirmed: listing; its intent is not argued]`.

## 6. Against the T82 derivation `[confirmed: engine run]`

The input was `NeighbourGeography` at `origin/task/T82-ai-diplomacy-fidelity`, exported with `git archive` to a scratch directory outside both checkouts. A throwaway xUnit probe called `AreNeighbours` for all 120 unordered pairs on the committed `classical-mediterranean.json`, and the branch's own 16 `NeighbourGeographyTests` passed in the same run. The derivation yields 29 pairs:

| | Pairs |
| --- | --- |
| **In both** (24) | all 24 DAT pairs of §2: **full recall** |
| **Engine only** (6) | **Rome–Greece**, **Bithynia–Thracia**, **Seleucid–Thracia** (the three already known), plus **Seleucid–Macedonia**, **Seleucid–Greece**, **Ptolemaic–Greece** (new) |
| **DAT only** (0) | — |

- **The three known extras are really absent from the original.** Their bits are clear in the DAT and in all 101 saves.
- **The three new extras went unnoticed because the branch's tests checked only the Rome, Carthage and Thracia rows.** Two of them involve Greece, whose scattered colonial cities the T82 remarks already blame for Rome–Greece. The cause of the Seleucid–Macedonia pair was not examined `[hypothesis]`.
- **The six extras are behavioural, not cosmetic.** Each one widens every reader in §3 and §5:
  - the war pick's `me ∈ neighbours(k)`;
  - the treaty candidates;
  - the alliance offer to a human seat;
  - the rebellion's candidate recipients;
  - the peace cascade's gate, where an extra pair keeps an ally at war that the original would let make peace.
- **The derivation's claim that the field is fixed** is wrong on one point. It uses starting owners only, "matching a field the original never rewrites after scenario setup", but the conquest merge (§4) does rewrite it.

## 7. What a reimplementation must do

1. **Load the mask from the DAT, and do not derive it.** Read the word at DAT nation-record `+0x2B` for each of the 16 nations. The build repo would add `NationNeighbourOffset = 0x02B` beside `NationRelationOffset = 0x00B` in `DatLayout.cs`. Export it into the world file as a starting field, the way T75 exported `startingRelations`: for example `startingNeighbours` as an adjacency list or 16 words, keyed by the same `nationIds`. Keep it in the game state, not in `World`, because it changes (step 2). `[derived]`
2. **Apply the conquest merge** in the conquest-elimination path only, not the defection path. For each `k ≠ winner` in the loser's set, add `k ↔ winner`. Leave the loser's set and everyone's loser bit as they are. `[confirmed: decompile]`
3. **Persist the state** in saves, because the original round-trips it in the nation block. A save-import path can read SAV `+0x46` directly. `[confirmed: decompile + saves]`
4. **Route every rule in §3 and §5 through it.** That means the AI war and treaty picks, the offer roll, the rebellion recipient and the peace cascade's ally gate. `[confirmed: decompile]`

## What this does not establish

- **The merge has never been observed changing a mask.** The only conquest in the saves (Galatia → Seleucid) is a no-op for the merge. Every local save falls within 270 BC, spring week 1 to winter week 11, so there is no late-game save with a non-trivial conquest.
- **Why the original's frontier graph looks as it does.** It is hand-authored data. Nothing here says whether any rule made Carthage–Ptolemaic a pair and Rome–Greece not.
- **The winner–ally `−8` reset in the peace cascade**, and whether it is an original bug, is outside this question (§5).
- **Indirect accesses** that neither form nor offset the field address, such as a pointer to `+0x26` indexed 32 bytes on, would escape the scan. None is known, and the five readers found match the diplomacy code's known call graph.
- **A second scenario file.** Only one DAT exists locally, so this is about that scenario alone.

## Reproduction

- **Decompile:** `all_app_functions.txt` lines above. The DAT loader is in `%LOCALAPPDATA%\ReTools\scratch\datload.txt`:143–240, and the SAV loader is in `save_load_impl.txt`:1–106.
- **Scan:** a Ghidra post-script (`Scan2.java`, kept in the session scratchpad, not committed) run as `analyzeHeadless <ghidra_projects> IC2 -process "Imperial Conquest 2.exe" -noanalysis -readOnly -postScript Scan2.java`. It calls `disassemble()` at every non-zero undisassembled byte in `CODE`, then walks every instruction applying the tests in §3.
- **Listings:** `-readOnly -postScript DumpListing.java <out> 00450c68 0044c528`.
- **Bytes:**
  - DAT word = `u16le(dat, 0x1B100 + i × 1055 + 0x2B)`.
  - SAV word = `u16le(sav, T + i × 0x494 + 0x46)`, with `T = 89,600 + 11,356 + 2 + armies × 656 + 2 + fleets × 26`.
  - Calendar = tail `+40/+42/+44` (week, year BC, season) of the last 55 bytes.
- **Engine:** `git archive origin/task/T82-ai-diplomacy-fidelity` into a scratch folder, then a one-off xUnit fact that writes every `AreNeighbours` pair. It ran with `dotnet test --filter DumpPairsProbe|NeighbourGeographyTests`: 17 passed.
- **Nothing from the game** (EXE, DAT or SAV) was copied into a repository.

## Dev-repo engine, for comparison (read-only)

`src/IC2.Engine/Diplomacy/NeighbourGeography.cs` on `task/T82-ai-diplomacy-fidelity` (PR [#377](https://github.com/diegoami/imperial_conquest_2/pull/377)) derives the relation from a Voronoi of the world's starting city owners. It is restricted to each nation's largest connected region, with a 10-tile minimum border. It is cached per `World` and never changes during a game. `src/IC2.Data/DatLayout.cs` on `main` reads the relation row at `+0x0B` (T73) but not `+0x2B`, and the exported world has `startingRelations` but no neighbour field. §6 and §7 give the differences.
