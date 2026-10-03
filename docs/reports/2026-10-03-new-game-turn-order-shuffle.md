# The New Game turn-order shuffle: a 16-swap shuffle on Delphi's `Random(16)`, draw 437 onward for seed 12345

**The question** (clone issue [diegoami/imperial_conquest_2#602](https://github.com/diegoami/imperial_conquest_2/issues/602)). The clone's classical-faithful preset is to shuffle the turn order at New Game the way the original does, using the original's actual algorithm. Where does New Game build the turn order? What is the shuffle, which generator does it use, and how is that generator seeded? How many draws come before it, and where is the order saved? Does the human's choice of nation change it? [2026-10-02-start-as-each-nation.md](2026-10-02-start-as-each-nation.md) saw one order in all 16 seed-12345 starts: Illyria, Numidia, Ptolemaic, Galatia, Seleucid, Thracia, Greece, Dacia, Macedonia, Media, Armenia, Rome, Bithynia, Carthage, Gaul, Celtiberia.

Line numbers prefixed `:` are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`. `nl:` lines are in `news_log_decomp.txt`, the export of `FUN_00448AA4`, which the whole-application dump lacks.

## Answer

1. **Where.** `FUN_00448AA4` (New Game setup) builds the order. `TPremierForm_NewGame` (`0x0045A9E0`) calls it after the DAT reload and **before** the New Game form where the human seats are ticked (`:58032–58034`). Program start (`TPremierForm_InitialiseForm`) calls it too, but New Game runs it again and replaces everything. `[confirmed: code]`
2. **The algorithm.** The 16 shorts at `0x0049EFE8` are set to `0, 1, …, 15` in nation (DAT) order. Then, for `i = 0, 1, …, 15` ascending, the code takes `j = Random(16)` and swaps `order[i]` with `order[j]` (`nl:72–86`, swap helper `FUN_00448FE0`). **It is not Fisher–Yates.** `j` ranges over the whole array every time (0–15), not over `i..15`, so it is the naive "swap each slot with any slot" shuffle. It always makes exactly 16 draws, and a swap with `j = i` is a no-op. The current nation is then `order[0]` and the turn position is 0. `[confirmed: code]`
3. **The generator.** It is Delphi `System.Random`, `FUN_0040284C`: `RandSeed := RandSeed × $08088405 + 1` (32-bit), and `Random(n) = (RandSeed × n) shr 32` (`:1585–1592`). `FUN_00448AA4` begins with `Randomize`, `FUN_00402744` (`nl:20`). On the original that sets `RandSeed` to the **UTC time of day in milliseconds**, `((h × 60 + m) × 60 + s) × 1000 + ms` (`:1463–1474`). On the patched build, the `Randomize` call is routed through the `SEED.TXT` cave, so New Game's `RandSeed` is the file's value ([2026-09-29-loading-a-save-does-not-reseed.md](2026-09-29-loading-a-save-does-not-reseed.md)). `[confirmed: code]`
4. **What comes before the shuffle.** Every `Random(n)` advances `RandSeed` once, whatever `n` is. So only the branch draws decide the count. The draws come in this order:
   - the mercenary fill `FUN_00449130`, at 2, 4 or 5 draws a slot;
   - the weather overlay `FUN_00451304` at Spring week 1: 20 draws, plus 208 for each storm centre that hits;
   - 16 × `Random(12)` for the leaders.

   The count therefore depends on the seed. For seed 12345 it is **436** (192 + 228 + 16), so the shuffle uses draws 437–452. `[confirmed: code, and by replay below]`
5. **The replay reproduces it exactly.** Seed 12345 gives the observed order, and so do two unpatched desktop games once their clock seeds are recovered:
   - **seed 12345** (Wine): the observed order, plus the leaders the two-human run saw in the title bar (Carthage *Agis*, Ptolemaic *Thutmose*);
   - **two desktop games** (`IP000.sav`, `1.sav`): a search of all 86,400,000 clock seeds finds exactly one seed per game whose 16 leader draws match the saved leaders. That same seed then reproduces the saved turn order, the number of mercenary slots filled, and the storm cells.

   `[confirmed: code + Wine + 2 desktop saves]`
6. **The human's choice does not change the order.** The shuffle has run before the New Game form opens. `TPickLeaders_OK` draws `Random(12)` only for a seat switched from human to computer, which cannot happen at that point ([decompiled-new-game-mercenary-fill.md](decompiled-new-game-mercenary-fill.md) §1). All 16 one-human starts and the two-human start share one order. `[confirmed: code + Wine]`
7. **It is fixed for the whole game.** The only writers of `0x0049EFE8` are this shuffle and the SAV loader. `TPremierForm_EndTurn` (`:58349–58360`) and the AI seat loop `FUN_0044FA20` (`:53221–53231`) only read it, as `position := (position + 1) mod 16; nation := order[position]`. The weekly tick fires when the position wraps to 0. An eliminated nation keeps its slot: `FUN_0044FA20` skips the AI's work when unity ≤ 0 but still advances. `[confirmed: code]`
8. **In the save.** The order is the 32-byte block written after the news log (`:47509`), followed by the 4-byte pending offer, current nation, turn position, week, year and season. That is SAV offset `len − 55`, 16 × int16, with the current nation at `len − 19` and the position at `len − 17` ([decompiled-sav-file-layout.md](decompiled-sav-file-layout.md)). `[confirmed: code + 54 saves]`

## Method

- Read `TPremierForm_NewGame`, `TPremierForm_EndTurn`, `FUN_0044FA20`, `Random` and `Randomize` in the dump, and `FUN_00448AA4` in its export. Grepped every reference to `0x0049EFE8` (`all_app_functions.txt`, `save_load_impl.txt`).
- Wrote `scripts/new-game-draw-chain.py`, which replays `FUN_00448AA4`'s draws for a given seed. Branch rules come from the restock (`:47806–47866`) and the overlay rule ([decompiled-map-code1-overlay.md](decompiled-map-code1-overlay.md) §5: `N = 15`, `r = 4` at Spring week 1).
- First check, seed 12345 without the chain model: a scan of offsets 0–19,999 for the observed order. Exactly one offset matches, **436**. The chain model then predicts 436 on its own (fill 192, overlay 228, leaders 16).
- **Clock-seed search** (scratch C# port of the same loop, about 6 s). For two desktop New Games, the leaders and turn order were read from the saves: the nation table `+0x0B` and the tail at `len − 55`. Leader names map to pool indices through the DAT leader pool (`0x2089A`, 16 × 12 × 26 bytes). Every seed in `[0, 86,400,000)` was then run and compared on the 16 leader draws alone. The turn order, filled-slot count and storm cells were checked afterwards, as independent predictions.

## Observations

**The code** (`FUN_00448AA4`, `nl:20–89`, abridged):

```c
FUN_00402744();                      // Randomize
...
FUN_00449130();                      // mercenary fill (first consumer of the seed)
FUN_00451304();                      // weather overlay, Spring week 1
for (n = 0; n < 16; n++) leader[n] = pool[n][FUN_0040284c(12)]; ...
for (i = 0; i < 16; i++) order[i] = i;
p = order; k = 16;
do { j = FUN_0040284c(0x10); FUN_00448fe0(p, &order[j]); p++; } while (--k);   // swap
DAT_004a0322 = 0;                    // turn position
DAT_004a0320 = order[0];             // current nation
```

**Replays** (`python scripts/new-game-draw-chain.py 12345 81899841 8363996`):

| Game | Seed (`RandSeed` after `Randomize`) | Fill draws / slots filled | Storm centres | Draws before shuffle | Predicted order = saved order | Other checks |
| --- | --- | --- | --- | ---: | --- | --- |
| Wine, `SEED.TXT` 12345 | 12345 | 192 / 46 | 1 | 436 | yes (Illyria … Celtiberia, as observed) | Carthage → index 6 *Agis*, Ptolemaic → index 5 *Thutmose*, as in the title bars of [2026-10-02-two-human-seats.md](2026-10-02-two-human-seats.md) |
| desktop, `IP000.sav` (run-1-ptolemy) | 81,899,841 (22:44:59.841 UTC) | 181 / **40** | none | 217 | yes: `13 10 14 4 8 12 1 9 0 5 15 2 7 3 6 11` | the save has 40 ever-filled slots and **0** code-1 cells |
| desktop, `1.sav` (run-1-rome) | 8,363,996 (02:19:23.996 UTC) | 189 / **44** | **15, 18** | 641 | yes: `2 12 3 9 11 6 7 0 4 13 8 15 1 10 14 5` | the save has 44 ever-filled slots (41 live, 3 hired by earlier seats), and all **311** code-1 cells lie inside the 17 × 17 boxes of centres 15 `(153,48)` and 18 `(209,12)`, none outside |

In both desktop searches, exactly one seed in the day matched the 16 leader draws. The chance of a false leader match is about 12⁻¹⁶ per seed, so 86.4 M seeds give about 1.5 × 10⁻⁹ expected false matches. The turn order, the filled count and the storm cells were not used to find the seed.

The 16 seed-12345 starts and the two-human start all saved the same `turn_order` ([2026-10-02-start-as-each-nation.md](2026-10-02-start-as-each-nation.md), [2026-10-02-two-human-seats.md](2026-10-02-two-human-seats.md)).

## Inferences

- **For a reimplementation that wants seed-for-seed parity** `[derived]`, reproduce the following:
  - Delphi's LCG.
  - The New Game draw chain in order: the fill's branch draws, the overlay's 20 + 208-per-hit draws, the 16 leader draws.
  - Then the 16-swap loop.

  The clone's own mercenary fill, overlay and leader draw must consume the same number of draws. Otherwise the order drifts even with the right shuffle.
- **For a preset that wants only the original's distribution** `[derived]`, use the same loop on any uniform `Random(16)`: `for i in 0..15: swap(order[i], order[Random(16)])`. The result is **not uniform over the 16! orders**. There are 16¹⁶ equally likely swap sequences, and 16! does not divide 16¹⁶, so some orders are more likely than others. That bias is the original's behaviour, and a Fisher–Yates shuffle would not reproduce it.
- **Test vectors for the clone** `[confirmed]`: seed 12345 → `9 5 3 12 2 15 7 10 4 14 13 0 11 1 6 8`; seed 81,899,841 → `13 10 14 4 8 12 1 9 0 5 15 2 7 3 6 11`; seed 8,363,996 → `2 12 3 9 11 6 7 0 4 13 8 15 1 10 14 5` (nation indices in DAT order, Rome = 0).
- **Predictions for other seeds** `[derived, untested]`: seed 999 → Rome, Armenia, Greece, Gaul, Carthage, Galatia, Celtiberia, Seleucid, Numidia, Illyria, Bithynia, Ptolemaic, Dacia, Thracia, Macedonia, Media (429 draws before; 42 slots filled; storm centre 11).
- `rules-digest.md`'s observation that Rome's seat differs per game (13, 10, 7, 5) is this shuffle on a clock seed.

## What this does not establish

- That the desktop original takes the `Randomize` branch when started from `SEED.TXT`. The patched build replaces it, and the desktop games above were clock-seeded. This is not needed: both paths feed the same `RandSeed` into the same chain.
- Whether `Randomize`'s other call site (`0x456759`, in a handler with no direct caller) can re-seed mid-game. It does not touch the turn order, which nothing rewrites.
- The overlay's edge behaviour for a centre whose 17 × 17 box crosses the map edge. The replay assumes all 208 ring draws are made, which holds for centres 1, 15 and 18. A centre near an edge was not exercised.

## Reproduction

```text
python scripts/new-game-draw-chain.py 12345 81899841 8363996 999
# saves: IP000.sav and saves-processed/1.sav in the user's local original folder (not in any repository)
# turn order <16h at len-55; leaders: nation table +0x0B; DAT leader pool 0x2089A (16 x 0x138, 12 x 26-byte names)
# pool: 50 x <6h after the nation table; code-1 cells: map shorts == 1 (column-major, 140 per column)
```
