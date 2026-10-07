# New games start with the DAT's recruitment queues, unchanged

**Question** ([imperial_conquest_2#514](https://github.com/diegoami/imperial_conquest_2/issues/514)): do new games start with regiments in training, and where do they come from?

The original's week-1 saves `1_cartago_271_spring_1.sav` and `1.sav` show Rome already holding 4 units in training, 14,000 troops. The build repository's world, exported from the DAT, has none. The lead was the DAT nation record's 320-byte recruitment block, which the loader reads and the T29 export never took.

**Answer.**
- **Fixed, and read straight from the DAT.** In three headless new games, two as Rome and one as Carthage, every nation's recruitment slots at game start were identical, slot by slot, to the 40 slots of its DAT record.
- **The DAT gives every nation a starting queue**: 2 to 8 regiments, 4,200 to 35,200 troops.
- **The only variation between games is additions.** The turn order is reshuffled for each new game. The AI nations seated *before* the human move before the first autosave, and some of them recruit, appending new slots (state 0).

## Method

- **Build:** `Imperial Conquest 2 watch autosave.exe`, SHA-256 `70aa4513c55eda4e2c164233afa5c3ae87d28e7ee95e2f551583666ce220b452`. This is the watch variant plus the autosave option of [2026-09-28-autosave-hook-feasibility.md](archive/2026-09-28-autosave-hook-feasibility.md).
- **Environment:** Wine 9.0 and Xvfb, driven by xdotool, in a fresh game folder holding only the executable, the DAT (SHA-256 `94d0ccfc67148d727de4c4e60aefc3c53ba9e67775bd689f0fcb2e23c12e5fbd`), the help files and `WAVS`.
- **The run:** *File → New*, tick one nation in *Human and computer leaders*, OK.
  - The autosave hook sits on the new-game route (`NewGame` → `FUN_00452034` → `call StartTurn` at `0x45217A`). It wrote `AUTO0720.SAV` (Spring week 1, 270 BC) just before the human's first turn started, with no end-turn and no other input.
  - The file was copied out and the game killed, three times.
- **Save parse:** `SaveRecruitmentTable` layout. The nation table follows the city, army and fleet tables ([decompiled-sav-file-layout.md](decompiled-sav-file-layout.md)): 16 records of 1,172 bytes. The recruitment table sits at `+0x2E4`: 40 slots of 8 bytes, as words `state, type, troops, city` ([decompiled-mobilization-and-mercenary-restock.md](decompiled-mobilization-and-mercenary-restock.md)).
- **DAT parse:** the loader (`0x4481A0`) reads each nation as 1,055 bytes (`0x41F`) in this order:

  ```text
  +0x000  name, 11 B
  +0x00B  relation row, 32 B
  +0x02B  neighbour mask, 2 B
  +0x02D  city list, 668 B
  +0x2C9  recruitment, 320 B
  +0x409  wealth, 4 B
  +0x40D  treasury, 4 B
  … then 7 more words
  ```

  - The records start at DAT `0x1B100`. The names `Rome` at `0x1B100`, `Carthage` at `+0x41F`, `Macedonia` at `+4×0x41F` and `Gaul` at `+6×0x41F` confirm the base and the stride.
  - The recruitment block uses the same 8-byte slot layout, copied into memory at nation `+0x2E4`.
- **Type codes:** 0 light infantry, 1 heavy infantry, 2 archers, 3 light cavalry, 4 heavy cavalry.

| Save | Human | SHA-256 | Turn-order index of the human |
|---|---|---|---:|
| `ng1_rome.sav` | Rome | `12f1f6a2fc547140cd224696ef674798818282f9e5b1794324174ac6b3748faa` | 13 |
| `ng2_rome.sav` | Rome | `fcb916825e1c254551d2e3330b58ee8582fe67fc05bb90b2708e40d720cb702a` | 10 |
| `ng3_carthage.sav` | Carthage | `5c928d446624fe790cbf919b0614521c60c272d889344dbd4c4b107d1a192d64` | 11 |

**Where the saves are:** committed in `diegoami/imp_conquest_fixtures` at `saves/new-game-probes/` (commit `a67ba3e`), not in a release. See [evidence-index.md](../evidence-index.md).

## Observations

1. **Every DAT slot is present unchanged in every game.** For all 16 nations, in all three saves, each non-empty DAT slot (state, type, troops and city) appears at the same slot index with the same four words. No DAT slot was altered or removed.
2. **Rome's queue in all three games** is the DAT's: light infantry 5,500 (state 9), heavy infantry 3,500 (13), heavy infantry 4,000 (17), heavy cavalry 1,000 (17), all at city 85, 14,000 troops. These are exactly the four units #514 reports from `1_cartago_271_spring_1.sav` and `1.sav`. In game 3 Rome was an AI seat that moved before Carthage, and it still added nothing.
3. **Extra slots appear only after the DAT slots, all with state 0**, and only in nations that sit before the human in that game's turn order:
   - game 1: 6 of the 13 nations seated before Rome;
   - game 2: 3 of 10;
   - game 3: 5 of 11.

   Nations after the human never have extra slots.
4. **The 16-entry turn-order table differs in each game.** Game 1 begins Bithynia, Gaul, Armenia…; game 2 Media, Numidia, Bithynia…; game 3 Dacia, Media, Thracia…. So the set of nations that move before the human differs too.
5. **Both Rome games have different nation tables overall**, because of observations 3 and 4. Their DAT-derived slots are identical.

The starting queues per nation, from the DAT, with the number of slots each game appended:

| # | Nation | DAT slots | DAT troops | DAT queue (type troops/state, city) | Game 1 added | Game 2 added | Game 3 added |
|---:|---|---:|---:|---|---:|---:|---:|
| 0 | Rome | 4 | 14,000 | LI 5,500/9, HI 3,500/13, HI 4,000/17, HC 1,000/17 (city 85) | — | — | — |
| 1 | Carthage | 2 | 4,200 | HC 1,200/11, HI 3,000/11 (city 72) | — | — | — |
| 2 | Seleucid | 8 | 35,200 | LI 6,000/7, LI 5,800/7, Ar 1,700/11, Ar 1,400/11, HI 4,500/15, LC 3,800/19, HI 4,000/21, LI 8,000/21 (city 259) | 8 | — | 8 |
| 3 | Ptolemaic | 5 | 24,400 | HC 900/7, LI 9,000/13, HI 5,000/15, Ar 2,000/17, LI 7,500/21 (city 214) | 6 | 4 | 4 |
| 4 | Macedonia | 2 | 9,000 | HI 4,000/7, LI 5,000/13 (city 144) | — | — | — |
| 5 | Numidia | 3 | 7,500 | LC 2,500/5, HC 700/9, LI 4,300/15 (city 47) | — | — | — |
| 6 | Gaul | 4 | 16,500 | HI 1,500/9, LI 8,500/13, HC 800/15, LI 5,700/19 (city 45) | 8 | 8 | 8 |
| 7 | Greece | 2 | 8,300 | HI 3,500/5, LI 4,800/13 (city 166) | — | — | — |
| 8 | Celtiberia | 4 | 15,000 | HC 1,300/7, LI 5,500/7, LC 3,000/17, LI 5,200/17 (city 23) | 8 | — | 8 |
| 9 | Illyria | 3 | 11,800 | LI 4,300/11, LI 5,000/15, LC 2,500/17 (city 126) | — | — | — |
| 10 | Dacia | 3 | 10,700 | LI 4,200/7, LI 3,800/11, HI 2,700/13 (city 133) | — | — | — |
| 11 | Bithynia | 3 | 10,100 | HI 2,800/7, LI 6,300/15, HC 1,000/17 (city 250) | 7 | 7 | — |
| 12 | Galatia | 3 | 13,100 | LC 3,100/9, LI 4,900/15, LI 5,100/21 (city 218) | 8 | — | 8 |
| 13 | Armenia | 3 | 12,000 | LI 5,000/13, LI 5,000/19, Ar 2,000/19 (city 297) | — | — | — |
| 14 | Media | 3 | 13,500 | Ar 2,500/7, LI 7,000/13, LC 4,000/17 (city 330) | — | — | — |
| 15 | Thracia | 3 | 10,300 | LI 5,300/9, HI 4,000/17, HC 1,000/17 (city 192) | — | — | — |

## Inferences

- **A new game copies the DAT's recruitment block as it is.** Nothing is generated and nothing is randomised in it. The "regiments in training at week 1" in the original's saves are the DAT's scripted queues, not a new-game roll. `[derived]`: from observation 1 across three games and two human nations. The copy itself is the loader's `Read(nation + 0x2E4, 0x140)`.
- **The per-game differences come from two other things.** New-game code shuffles the turn order. The AI seats ahead of the human then take their first turn, and the AI's own recruitment (state-0 slots) happens there. A save made at the human's first turn therefore mixes the DAT queue with some AI recruits. Only the DAT part is the same in every game. `[derived]`: observations 3 and 4. Where the shuffle happens was not located this pass.
- **For the build repository:** the world export should take the DAT's 320-byte block at nation record `+0x2C9` (1,055-byte records from DAT `0x1B100`) into each nation's recruitment table. The state word is the readiness counter the weekly tick raises by 2 up to 24 ([decompiled-turn-and-calendar-sequencing.md](decompiled-turn-and-calendar-sequencing.md)). The starting values are odd (5–21), so a scripted regiment matures in a staggered way. That the odd starting states keep their odd parity through the +2 tick was not checked here.

## What this does not establish

- The start year. All three games started at Spring week 1, 270 BC, and `1_cartago_271_spring_1.sav`'s name says 271. Whether a scenario or option changes the start year, and whether it then uses different queues, was not tested.
- The code that shuffles the turn order and runs the first AI seats at new game. It was inferred from the saves, not decompiled.
- Anything about scenarios other than the default DAT.

## Reproduction

1. Build the watch+autosave executable as in the autosave report.
2. In a clean game folder under Wine: *File → New*, tick one nation, OK.
3. `AUTO0720.SAV` appears beside the executable before the first turn. Parse both files with the layouts in **Method**.
