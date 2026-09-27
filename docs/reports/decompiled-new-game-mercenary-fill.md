# The New Game mercenary fill: one pass of the quarterly restock over an empty pool

**The question** (dev-repo [#457](https://github.com/diegoami/imperial_conquest_2/issues/457), "A new game starts with no mercenary offers"): the original starts a new game with plenty of mercenary offers, and the user confirms this from play. The DAT ships the 50 live pool slots empty ([decompiled-mercenary-offer-list-and-position.md](decompiled-mercenary-offer-list-and-position.md) §4). The only known writer of the pool, the quarterly restock `FUN_00449130`, was believed to have a single caller, the quarterly tick ([decompiled-mobilization-and-mercenary-restock.md](decompiled-mobilization-and-mercenary-restock.md) §6). So how is the pool filled at New Game, exactly what does the fill do, does loading a SAV skip it, and what is the template table's DAT format?

Line numbers prefixed `:` are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`. `FUN_00448AA4` and the DAT loader `FUN_004481A0` are missing from that dump. Their decompile is in `%LOCALAPPDATA%\ReTools\news_log_decomp.txt`, exported for [news-log-format-and-messages.md](news-log-format-and-messages.md), and is cited as `nl:<line>`. The SAV loader `FUN_004487C4` is in `save_load_impl.txt`, cited as `sl:<line>`.

## Answer

1. **New Game runs the quarterly restock once, and that is the whole fill.** `TPremierForm_NewGame` reloads the DAT, which empties all 50 live slots. It then calls `FUN_00448AA4`, and `FUN_00448AA4` calls `FUN_00449130()` with no arguments and no loop around it (`nl:31`). The routine is the same one the quarterly tick calls, over the same 50 slots. Nothing else fills the pool, and the DAT puts nothing into it. `[confirmed: code]`
2. **Each slot refills with probability 46/54 (about 85 %), from a random template.** Every slot starts empty, so every slot takes the restock's empty-slot branch. It refills on `Random(6) ≤ 4`, or on `Random(6) = 5` followed by `Random(9) = 8`. A refill copies `x, y, Label, type` from template `Random(200)`. It sets troops to `min(b + Random(b), standardSize[type])` with `b = (3 × template.troops) div 2`, and quality to `min(9, max(5, template.quality + 1 − Random(2)))`. That is the quarterly rule unchanged. **About 42.6 of the 50 slots start filled** (binomial, standard deviation 2.5). The fill is the first consumer of the RNG after New Game's `Randomize`, ahead of the weather overlay, the leader draw and the turn-order shuffle. `[confirmed: code]`
3. **Loading a SAV bypasses the fill.** `TPremierForm_OpenGameFile` calls only the SAV loader. The loader reads the 50 live slots from the file and never calls `FUN_00448AA4` or `FUN_00449130`. The template table is not in the SAV; it stays in memory from the DAT load at program start. `[confirmed: code]`
4. **The template table is at DAT `0x1FCD6`: 251 records of six signed 16-bit little-endian words.** In order the words are `x, y, Label, type, troops, quality`. Records `0`–`200` are the 201 templates. Records `201`–`250` are the 50 live slots, all shipped as `(0, 0, 0, 0, −1, 0)`. The field meanings are confirmed, with one exception: `troops` is a *base* the fill scales rather than an offer size. §4 gives the tag for each field.
5. **Four independent turn-1 saves match the prediction.** Every live offer is a template with troops and quality inside the predicted ranges (0 exceptions). The number of slots ever filled is 43, 45, 46 and 40 against an expected 42.6 ± 2.5. Across all 111 local save files, all 5,041 live offers are inside the predicted ranges, and none uses template 200. `[confirmed: saves]`

**This corrects two earlier statements.** [decompiled-mobilization-and-mercenary-restock.md](decompiled-mobilization-and-mercenary-restock.md) §6 said `FUN_00449130` is "called from exactly one place". [decompiled-mercenary-offer-list-and-position.md](decompiled-mercenary-offer-list-and-position.md) left open whether "the pool may start empty until the first quarter boundary". Both came from the whole-application dump, which lacks `FUN_00448AA4`. The restock has **two** callers, and the pool starts full.

---

## 1. The call chain from `TPremierForm_NewGame`

```c
TPremierForm_NewGame(form):                       // :58008
    [confirm dialog; close forms or reset a battle]
    FUN_004481A0();                               // :58032  DAT loader: reloads everything, pool slots empty
    FUN_00448AA4();                               // :58033  New Game setup, below
    CreateForm(0x00456D00, &DAT_004A0BA4);        // :58034  the TPickLeaders dialog (human/computer per seat)
    if any seat is human: enable menus; start the first turn (FUN_00452034 or FUN_00451FDC)
```

```c
FUN_00448AA4():                                   // nl:7
    FUN_00402744();                               // nl:20  Randomize: RandSeed = UTC milliseconds since midnight (:1463)
    h = GetSystemMetrics(SM_CYSCREEN);            // nl:21  (window layout only)
    ... season = 0; week = 1; year = 270;         // nl:25-27 (DAT_004A032E, DAT_004A0330, DAT_004A0332)
    newsIndex = 0x1A;                             // nl:30
    FUN_00449130();                               // nl:31  <- the mercenary fill: the quarterly restock, once
    FUN_00451304();                               // nl:32  the weather overlay's roll
    for nation in 0..15: leader = pool[Random(12)]; human = 0; ...   // nl:36-71
    turnOrder = 0..15; for i in 0..15: swap(turnOrder[i], turnOrder[Random(16)])  // nl:72-86
    currentNation = turnOrder[0]; ...
```

`[confirmed: code]`

- **The DAT loader empties the pool first.** `FUN_004481A0` reads `0xBC4` bytes into `0x0049D0A4` (`nl:228`). That is 251 × 12 bytes: the 201 templates and all 50 live slots. The DAT holds the live slots as `(0, 0, 0, 0, −1, 0)` (§4), so every New Game fill starts from an all-empty pool, whatever was in memory before.
- **The fill is a plain call.** `FUN_00449130` takes no arguments (`:47808`). It walks all 50 slots itself (`sVar5 = 0x32`, base `0x0049DA10`), and `FUN_00448AA4` calls it once, with no loop around it.
- **Program start does the same.** `TPremierForm_InitialiseForm` ends with the same two calls (`:57994–57995`), so a pool already exists before the user picks New Game. New Game discards it by reloading the DAT.
- **The dialog does not touch the pool.** `TPickLeaders_OK` (`:56908`) draws `Random(12)` only for a seat switched from human to computer. That cannot happen straight after `FUN_00448AA4` has cleared every human flag (`nl:39`, `puStack_20[0x490] = 0`). It never references the pool. `[derived: code]`
- **The first quarterly restock** comes on the week-wrap into Summer (`:54665–54667`), six turns later.

## 2. What the fill does, per slot

`FUN_00449130` is transcribed in [decompiled-mobilization-and-mercenary-restock.md](decompiled-mobilization-and-mercenary-restock.md) §6 (`:47806–47866`). The New Game fill differs only in its input: every slot's troops word is `−1`. So every slot takes the empty branch (`:47821`), in slot order 0 to 49. `[confirmed: code]`

```text
for slot in 0..49:                               // live slot s at 0x0049DA10 + 12*s
    d = Random(6)                                // :47822
    if d == 5:                                   // "4 < d": fall through to the occupied roll
        if Random(9) <= 7: continue              // :47857-47858  slot stays (0,0,0,0,-1,0)
    n = Random(200)                              // :47825  template 0..199
    slot.x, slot.y, slot.label, slot.type = tmpl[n].x, .y, .label, .type      // :47828-47830
    b = (3 * tmpl[n].troops) div 2               // :47831  (templates are positive: plain floor)
    slot.troops = min(b + Random(b), standardSize[tmpl[n].type])              // :47835-47846
    slot.quality = min(9, max(5, tmpl[n].quality + 1 - Random(2)))            // :47847-47853
```

- **Which template:** a uniform random draw, `Random(200)`, independent for each slot. There is no fixed or sequential mapping. Two slots can draw the same template, and template 200 (Vologesias, light cavalry) can never be drawn. `[confirmed: code]`
- **Troops:** uniform on `[b, 2b − 1]`, i.e. 1.5× to just under 3× the template value, then capped at the type's standard battalion size (DAT unit table `+0x1A`: 15,000 / 6,000 / 3,500 / 7,000 / 2,500 for types 0–4). For 3 of the 201 templates, `b` alone already reaches the cap, so their offer is always exactly the cap. `[confirmed: code; the count is derived from the DAT]`
- **Quality:** the template's value or one above it, 50/50, clamped to 5–9. A template at 9 always gives 9. `[confirmed: code]`
- **How many start filled:** each slot independently with `P = 5/6 + (1/6)(1/9) = 46/54 ≈ 0.852`. The count is Binomial(50, 46/54), with mean 42.6, standard deviation 2.51, and a full pool of 50 has probability ≈ 3 × 10⁻⁴. `[derived]`
- **The exact draws, in order, per slot:**

  | Outcome | Draws | Count |
  | --- | --- | ---: |
  | refilled on the first roll (`d ≤ 4`, p = 5/6) | `Random(6)`, `Random(200)`, `Random(b)`, `Random(2)` | 4 |
  | refilled on the second roll (p = 1/54) | `Random(6)`, `Random(9)`, `Random(200)`, `Random(b)`, `Random(2)` | 5 |
  | left empty (p = 8/54) | `Random(6)`, `Random(9)` | 2 |

  That averages 3.72 draws a slot, about 186 for the fill. `[derived]`
- **Where it sits among New Game's draws:** `Randomize` (`nl:20`), **then this fill** (`nl:31`), then the weather overlay (`nl:32`), then 16 × `Random(12)` for the leaders (`nl:37`), then 16 × `Random(16)` for the turn-order shuffle (`nl:82`). The fill is the first thing to draw from the fresh seed. `[confirmed: code]`

`Random(n)` is Delphi's `System.Random` (`FUN_0040284C`), `0 ≤ r < n`, as established in the restock report.

## 3. A loaded game does not refill

```c
TPremierForm_OpenGameFile(form):                  // :58059
    [file dialog; close forms; reset a battle]
    FUN_004487C4();                               // :58076  SAV loader
    [enable nations; set title; start the turn or the battle]
```

`FUN_004487C4` reads the map, the cities, the armies, the fleets and the nation block (`sl:33–55`). It then reads **50 × 12 bytes into `0x0049DA10`** (`sl:56–62`), then the news log, the turn order and the calendar. It does not reload the DAT. It calls neither `FUN_00448AA4` nor `FUN_00449130`. `[confirmed: code]`

So a loaded game's pool is exactly the SAV's 50 slots, and everything else the pool depends on comes from the DAT loaded at program start (`:57994`). That covers the 201 templates, the 52 `Label` names at `0x0049CC94` and the unit table's standard sizes. None of these is in the SAV. `[confirmed: code]`

## 4. The template table's DAT format

**Location.** The DAT loader's reads are sequential (`nl:146–230`). The name table is 52 × 20 bytes at `0x1F8C6` (`nl:227`), so the mercenary block begins at `0x1F8C6 + 0x410 = 0x1FCD6` (`nl:228`). Counting backwards pins the same offset: `0x1FCD6 + 0xBC4 (merc block) + 0x1380 (leader pool) + 0x988 (news seed) = 0x225A2`, which is the DAT's length (140,706 bytes). `[confirmed]`

**Shape.** 251 records × 12 bytes = 3,012 bytes, each record six signed 16-bit little-endian words. Records `0`–`200` are the templates. Records `201`–`250` are the live slots, and the DAT holds all 50 as `(0, 0, 0, 0, −1, 0)`. `[confirmed]`

| Word | Offset | Field | Values in the 201 templates | Tag |
| ---: | ---: | --- | --- | --- |
| 0 | `+0` | `x`, the offer city's tile | all 201 `(x, y)` pairs are city tiles, 134 distinct cities | `[confirmed: code reads it as a position; DAT]` |
| 1 | `+2` | `y` | | same |
| 2 | `+4` | `Label`: index into the 52 ethnic names at DAT `0x1F8C6` | 1–51 | `[confirmed]` ([offer-list report](decompiled-mercenary-offer-list-and-position.md) §5) |
| 3 | `+6` | unit type, indexing the DAT unit table (`0x1F2F0`, stride 40) | 0 LI ×90, 1 HI ×33, 2 archers ×26, 3 LC ×37, 4 HC ×15 | `[confirmed: code indexes standardSize by it]` |
| 4 | `+8` | troops **base**; an offer is 1.5×–3× it, capped | 400–7,000 | `[confirmed: code]` |
| 5 | `+10` | quality base, 5 = poor … 9 = elite; an offer is this or one above | 5 ×8, 6 ×55, 7 ×70, 8 ×47, 9 ×21 | `[confirmed: code]`; the names are from [mercenary-pool-record.md](mercenary-pool-record.md) |

- **No two templates are identical.** Four `(x, y, Label, type)` keys appear twice, differing only in troops or quality. A consumer must not key templates by city and label alone. `[confirmed: DAT]`
- **Template 200 is data the fill never uses.** An exporter should still carry all 201, in order, so that `Random(200)` indexes the same records. `[derived]`
- **The type-code names** (0 light infantry … 4 heavy cavalry) follow the unit-type table order in [unit-type-stat-table-in-dat.md](unit-type-stat-table-in-dat.md). `[confirmed]`

## 5. Checked against turn-1 saves

**Method.** A throwaway Python script (not committed) read the DAT templates and every `.sav` under `saves/`, `saves-processed/` and `releases/`. It located the pool after the nation table, as `SaveMercenaryTable` does, and the calendar at `len − 55 + 40` as `(week, year, season)`. For every live offer, it checked the following:

- that `(x, y, Label, type)` equals some template's;
- that troops lie in `[min(b, cap), min(2b − 1, cap)]`;
- that quality lies in the clamped `[q, q + 1]`.

It also counted the slots still at `(0, 0)`. Such a slot was never filled, because a hire sets only `troops = −1` and leaves the stale position.

The eight saves dated Spring week 1 hold four distinct new games:

| Save | Turn position of the saving seat | Live | Hired this turn (stale `(x, y)`) | Never filled `(0, 0)` | Filled at New Game | Offers off-rule |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `1_cartago_271_spring_1.sav` (and `_1b`) | 7 | 43 | 0 | 7 | **43** | 0 |
| `1.sav` (legacy probes) | 7 | 41 | 4 | 5 | **45** | 0 |
| `1_thracia_271_spring_1.sav` | 5 | 44 | 2 | 4 | **46** | 0 |
| `IP000.sav` (and `IP000B`) | 13 | 40 | 0 | 10 | **40** | 0 |

- **Every live offer fits the fill rule** `[confirmed: saves]`. The four fill counts, 43, 45, 46 and 40, all lie within 1.5 standard deviations of the predicted 42.6. That agrees with the 46/54 rate, but four samples cannot pin it `[derived]`.
- **The empty slots with a position are first-turn AI hires** `[derived]`. In every one of these saves the saving seat is 5th to 13th in the turn order, so 5 to 13 computer seats had already played turn 1. Their hire (`FUN_0044E41C`) sets `troops = −1` and nothing else. No quarterly restock has run by Spring week 1, so nothing else can have emptied a filled slot. The attribution of each individual slot to a specific army was not checked.
- **Whole corpus:** 111 save files (some are copies across folders) hold 5,041 live offers. All of them are inside the predicted ranges, and none is template 200. `[confirmed: saves]`

## What this does not establish

- **Seed-exact replay.** The fill's draws are pinned, but no save's pool was reproduced from a seed. The seed is wall-clock milliseconds and is not stored. `[open]`
- **Per-slot attribution of the first-turn hires** in `1.sav` and `1_thracia_271_spring_1.sav` (see §5). `[open]`, low value.
- **Whether any New Game path skips `FUN_00448AA4`.** Its two callers are `TPremierForm_InitialiseForm` and `TPremierForm_NewGame`, from the dump. A whole-program `E8` scan for other callers was not run. `[open]`, low risk: no other path starts a game.

## Reproduction

```text
# decompiled text (toolchain, outside the repo)
all_app_functions.txt  :57994-57995 InitialiseForm's DAT load + setup
                       :58008 TPremierForm_NewGame (:58032 DAT loader, :58033 FUN_00448AA4, :58034 TPickLeaders)
                       :58059 TPremierForm_OpenGameFile (:58076 SAV loader only)
                       :47806 FUN_00449130 restock     :54665-54667 its quarterly call
                       :56908 TPickLeaders_OK          :1463 FUN_00402744 Randomize
news_log_decomp.txt    FUN_00448AA4 (nl:20 Randomize, nl:31 restock, nl:32 overlay, nl:37 leaders, nl:82 shuffle)
                       FUN_004481A0 (nl:227 names 0x410, nl:228 merc block 0xBC4)
save_load_impl.txt     FUN_004487C4 (sl:56-62: 50 x 12 bytes into 0x0049DA10)
# DAT: merc block 0x1FCD6, 251 x 12 bytes (<6h each); templates 0-200, live slots 201-250
#      unit table 0x1F2F0, stride 40, standard size at +0x1A; cities 0x15E00 (334 x 34, tile at +0xE)
# SAV: pool = 16 x 1172-byte nation table end; calendar <3H at len-55+40 = (week, year, season);
#      turn order <16h at len-55, current nation and turn position <2h at len-55+36
```
