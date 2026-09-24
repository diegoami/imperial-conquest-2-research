# Diplomacy, the reparations formula, and the original's own instant battle resolution

Two of this project's longest-standing "not recoverable" conclusions turn out to be wrong:

- `decompiled-fleet-tax-and-mercenary-formulas.md` and `decompilation-plan.md` item 3 record the **diplomatic reparation formula** as a dead end — *"the AI-to-AI reparation seen in saves must be computed in unnamed AI code (`ComputerGeneral` or similar), not reachable by class name"*. It is reachable by class name: it is in `TBattlePols`, a form class that was sitting in `delphi_symbols.tsv` the whole time.
- `game-design.md` accordingly designs diplomacy from scratch as `[designed, dead end in the original's code]`. The relation model, the legality rules, the war-drags-in-allies propagation, the peace terms and the reparation arithmetic are all confirmable.

Separately, the original already contains a **non-tactical, instant battle resolver**, used whenever no human is involved — which is directly relevant to `game-design.md`'s decision to replace tactical battles with auto-resolve.

## The relation matrix

Each nation record carries a **16-entry `short` array at `+0x26`** holding its relation toward every nation (runtime base `0x00474696`, nation stride `0x494`). `decompiled-turn-and-calendar-sequencing.md` already identified one of the SAV's unlabelled blocks as a 16-entry table; this is the per-nation diplomatic row.

| Value | Meaning |
| ---: | --- |
| `0` | peace |
| `1` | trade |
| `2` | alliance |
| `3` | war |
| `< 0` | peace, plus a **cooldown counter** that must climb back to 0 before trade or alliance is possible again |

> **Addition (2026-09-24): where the row lives on disk, and the starting matrix.**
> - **SAV.** The row is at SAV nation-record `+0x26`, the same offset as at runtime, because the SAV writes the runtime record whole (stride 1,172 = `0x494`). The leader name therefore occupies `+0x0B…+0x25`, **27 bytes**, not 34 **[confirmed: `1_rome_270_summer_7.sav`, where the 16 × 16 shorts at `+0x26` are symmetric with a zero diagonal and hold 6 wars, and reading from `+0x2D` or `+0x2E` gives neither property]**.
> - **DAT.** The DAT loader `FUN_004481A0` reads each nation's 11-byte name, then **32 bytes straight into runtime `+0x26`**: `Read(rec, 0xb)` then `Read(rec + 0x26, 0x20)` (`%LOCALAPPDATA%\ReTools\news_log_decomp.txt` ~:193–194). The DAT record has no leader field, so on disk the row is at DAT nation-record **`+0x0B`** (table `0x1B100`, stride 1,055) **[confirmed from code]**.
> - **New game keeps it.** `FUN_00448AA4` writes the leader at `+0x0B` and UI fields at `+0x46B…+0x490`, and never writes `+0x26`. So **the original's starting relations are the DAT's matrix** **[confirmed from code]**.
> - **The starting matrix** **[confirmed: `Imperial Conquest 2.dat`]**: symmetric, zero diagonal, **5 wars, 13 trades, 4 alliances, no cooldowns**. Rome's row: trade with Macedonia (4) and Illyria (9), war with Gaul (6). Saves a year later (`1.sav`, `1_cartago_271_spring_1.sav`, `1_thracia_271_spring_1.sav`) differ from it in 15–22 of the 120 pairs. That is consistent with a year of diplomacy, and it has not been traced turn by turn.

`FUN_00449B40(a, b, state)` is the single setter and writes **both** `[a][b]` and `[b][a]` — the matrix is symmetric by construction. Setting `state = 0` (plain peace) is translated into a cooldown instead, by the previous state:

| Previous state | Cooldown written |
| --- | ---: |
| trade (1) | **−8** |
| alliance (2) | **−24** |
| war (3) | **−18** |

Two propagation rules live in the same function:

- Setting **alliance (2)** with `b`: every nation at war with `b` that you are not already at war with becomes **at war with you**.
- Setting **war (3)** with `b`: every nation allied to `b` that you are not already at war with becomes **at war with you**.

The quarterly tick (`FUN_00451B40`, the function in `decompiled-quarterly-billing-and-economy.md`) implements the "gradual diplomatic thaw" that report described in structure only: for each negative entry, `v += 1`, and with probability `1/3`, `v = min(0, v + 3)`. **The thaw loop runs only over the first 8 columns of each row** (`while (sVar6 != 8)`), so a cooldown between two nations both indexed ≥ 8 never decays — an original bug, not a design rule, but one a faithful reimplementation has to decide about consciously.

## Player-initiated diplomacy (`TPolitics`)

`TPolitics_ChangeIR` (`0x00452C9C`) decodes the clicked grid cell into `(nation, newState)` and dispatches:

- **Peace** (`TPolitics_MakePeace` `0x00452D94`): refused with *"`X` does not want to make peace at this time."* if the target is **computer-controlled** (`nation[+0x490] == 0`) **and** currently at war. A human-controlled nation — i.e. another hotseat seat — always accepts.
- **Trade** (`TPolitics_MakeTrade` `0x00452E94`): **maximum 3 trade partners** (*"You can only trade with 3 nations."*); refused if the relation is negative (cooldown, *"`X` does not want to trade with you."*) or greater than 1 (allied or at war, *"You cannot trade with `X`."*), or if the target already has 3 partners and this is a new one.
- **Alliance** (`TPolitics_MakeAlliance` `0x004530D8`): refused against an AI nation if either side is currently at war with anyone, or if the relation is negative. Always accepted from a human seat.
- **War**: set directly, no check.

> **Correction (2026-09-25):** see [`decompiled-ai-offers-to-human-seats.md`](decompiled-ai-offers-to-human-seats.md) §3, which reads `TPolitics_MakeAlliance` at instruction level (`0x00453101–0x0045317A`).
> - **Alliance: the gate checks only the human's side.** Against an AI target, the proposal is refused if any of these holds: the human's edited row contains a war; a nation that row marks allied is at war with anyone; the human is at war in the committed matrix; or the relation is negative. **The AI target's own wars are not checked**, so allying with an AI that is at war drags the human into that war. "*Always accepted from a human seat*" means **when the target seat is human-controlled**. That is hotseat play, human to human. The code tests the target's `+0x490`, not the proposer's.
> - **Trade:** the target's three-partner refusal is waived only when a pending trade offer **from that target** exists. There is no other AI willingness test.
> - **The AI side:** computer nations never go through these handlers. `FUN_0044FB7C` writes AI-to-AI trade and alliance directly. Toward a human, the AI either declares war or raises the turn-start notice, and the notice never writes a relation.

`TPolitics_OK` (`0x00453230`) commits the row. Notably, if you open trade with a nation that already has three partners, **that nation drops its poorest existing partner** — the one with the lowest nation field `+0x44C` (wealth) — back to peace.

Declaring war is not only done from this screen: `TUnitMap_SelectUnit` auto-declares it. Clicking an enemy city, army or fleet with your own unit selected prompts *"Are you sure you want to attack this …?"* and, on yes, calls `FUN_00449B40(you, them, 3)` before resolving the attack. Attacking **is** declaring war, with the ally-dragging propagation above.

## The peace treaty and the reparation formula

`FUN_00450C68(winner, loser)` is the whole treaty. It is reached from `TBattlePols_Yes` (the post-battle *"After defeating you in battle `X` are willing to end …"* dialog) and, for AI-vs-AI wars, automatically from the instant battle resolver below.

> **Correction (2026-09-14):** see [`nation-tax-base-and-city-economy-fields.md`](nation-tax-base-and-city-economy-fields.md). `+0x44C` is the nation's **tax base**, not "wealth" (wealth is `+0x430`). The reparation formula below checks out against Ptolemaic's 2,269 payment: `W = 6188`, 48 cities, range `[2027, 3573]`.


```c
W = nation[loser][+0x44C];                       // wealth (short)
reparations = W/4 + random(W/4) + nation[loser][+0x446] * 10;     // +0x446 = city count

setRelation(winner, loser, 0);                   // → the −18 war cooldown

score(n)  = (nation[n][+0x430] / 100) * nation[n][+0x440];        // population × unity
armies(n) = Σ FUN_0044A8CC(army) over n's armies;                 // total field strength

if (score(winner) < score(loser) || armies(winner) < armies(loser)) {
    news("<winner> and <loser> have agreed to end their war.");   // honourable peace, nothing paid
} else {
    news("<loser> sues <winner> for peace and;");
    news("    <loser> ends all current trading agreements.");
    news("    <loser>  ends all current alliances.");
    news("    <loser> pays reparations of N talents.");
    for each n: if relation[loser][n] is trade or alliance: setRelation(loser, n, -10);
    treasury[loser] -= reparations;  treasury[winner] += reparations;
}
// finally: any ally of either side still at war with the other gets setRelation(..., -8),
// with news "<A> and <B> have agreed to end their war."
```

> **Note (2026-09-14):** `N` is printed by the game's own `FUN_00448F3C` (`FormStripNum1`). It groups digits with a hard-coded comma, independent of the locale, so a real line reads "*Ptolemaic pays reparations of 2,269 talents.*". See [`news-log-format-and-messages.md`](news-log-format-and-messages.md).

`TBattlePols_InitializeForm` (`0x004577EC`) previews exactly the same three terms and the same `reparations` expression before the player accepts, which is an independent check that the formula was read correctly.

This is consistent with the one real observation on record — `diplomatic-reparations-and-more-captures.md`'s Ptolemaic treasury going `999 → −1270`, a `−2269` payment — in shape and magnitude, but **the numbers were not independently reproduced**: `nation[+0x44C]` and `nation[+0x446]` for Ptolemaic at that moment were not read back out of the save, and the formula contains a `random(W/4)` term that a single observation cannot pin down anyway. Treating this as *confirmed formula, unverified against the one data point* is the honest label; verifying it is a cheap next check (read the two nation fields from the pre-treaty save, and check `2269` lands in `[W/4 + cities×10, W/2 + cities×10)`).

`THVHBatPols` (`0x00457FA8`) is the human-versus-human equivalent: a straight negotiated payment between two seats, `treasury[A] += amount; treasury[B] -= amount` (`THVHBatPols_OK` `0x00458688`), with no formula at all. It is directly relevant to `game-design.md`'s hotseat design, which currently has no post-battle negotiation step.

## The original's instant battle resolver

`FUN_0044AEE4(attackerArmy, defenderArmy)`, reached from `TUnitMap_SelectUnit` when one army attacks another on the strategic map:

```c
attacker.moves = 0;
if (both nations are computer-controlled) {
    // ---- instant resolution, no tactical battle ----
    pA = FUN_0044A8CC(attacker);  pB = FUN_0044A8CC(defender);   // power = Σ(weight[type]×troops/100)/80 × morale
    winner = (pB < pA) ? attacker : defender;                    // ties go to the defender
    applyCasualties(winner, loserPower * 40 / winnerPower);      // FUN_0044AE20
    winner.money    += loser.money;
    winner.supplies  = min(winner.supplies + loser.supplies, winnerTroops / 100);
    for each surviving unit of the winner:
        quality = max(quality, 6);                               // at least "average"
        if (random(4) == 0) quality = min(quality + 1, 9);       // 1-in-4 promotion
    deleteArmy(loser);
    unity[loserNation] -= 25;   unity[winnerNation] = min(990, unity[winnerNation] + 25);
    news("<winner> destroys army of <loser>.");
    if (random(5) < 2 && unity[loser] > 500 && cities[loser] > 7)
        FUN_00450C68(winnerNation, loserNation);                 // automatic peace + reparations
} else {
    TPremierForm_StartBattle(...);                               // the tactical TBattleMap
}
```

Three things follow that no existing report or design section accounts for:

1. **The original has both battle models.** A human-involved fight goes to the tactical grid; an AI-vs-AI fight is resolved in one shot by a power comparison. `game-design.md`'s choice of instant auto-resolve for *all* battles is therefore closer to the original than that document claims — but the auto-resolve math it proposes (running the tactical melee/shooting exchange loop internally with an invented `"pairing"` rule) is **not** the math the original uses for its own auto-resolve. The original's version is the two functions above: a single deterministic power comparison, total loss for the loser, proportional casualties for the winner.
2. **This is the missing AI-to-AI reparation trigger.** A 2-in-5 chance after any decisive AI-vs-AI field battle, gated on the loser's unity > 500 and city count > 7. That is exactly the kind of event `diplomatic-reparations-and-more-captures.md` observed happening between two AI nations with no player involvement, and it is why searching `TPolitics` for it found nothing.
3. **An explicit quality-promotion instruction exists after all.** `battle-quality-promotion-and-morale-array-decompiled.md` reported that *"None of the recovered battle-related functions contain an explicit 'increment quality' instruction"* — true for the tactical path, but the instant path promotes every surviving unit to at least `6` ("average") and then promotes 1-in-4 further. The empirically-derived adjacency rule in that report applies to the tactical path and is unaffected; this is a second, separate promotion rule on a different code path.

### Naval battles — a third, wholly undocumented combat model

`FUN_0044B5D0(attackerFleet, defenderFleet)`, from clicking an enemy fleet (*"Are you sure you want to attack this fleet ?"*; blocked by *"You cannot attack a fleet docked at its own city !"*):

```c
attacker.moves = 0;
base(f)     = ships × condition / 10 + (f carries an army ? siegeStrength(army) / 50 : 0);   // FUN_0044A930, not armyPower
strength(f) = base(f) + random(4) × (base(f) / 10);        // a 0/10/20/30% random bonus
winner = (strength(defender) < strength(attacker)) ? attacker : defender;   // ties to the defender
unity[loserNation] -= floor(loserShips / 2);
unity[winnerNation] = min(990, unity[winnerNation] + floor(loserShips / 2));
FUN_0044B4F8(winner, loserStrength, winnerStrength);   // damage to the winner (argument order corrected 2026-09-23)
deleteFleet(loser);                                    // and any army it carried
news("<winner> sinks fleet of <loser>.");
```

Winner damage (`FUN_0044B4F8`): with `r = max(1, loserStrength × 100 / winnerStrength)` and `d = r² / 100`, the winner loses `ships × d / 300` ships and `condition × d / 300` condition; a carried army takes casualties (`FUN_0044AE20`) **with `ratio = d`**, and if `d > 70` it also loses **`unitCount × d / 250 + 1`** whole units at random, with `unitCount` counted after those casualties.

> **Correction (2026-09-23)**, from a targeted pass on [`imperial_conquest_2#290`](https://github.com/diegoami/imperial_conquest_2/issues/290). This report corrects three things at instruction level; the section below has the evidence. (1) The call is `FUN_0044B4F8(winner, loserStrength, winnerStrength)`. The block above first gave the two strengths in the opposite order, although the `r` formula was right. The wrong order was copied into the reimplementation's storm call site, which reuses this function (see below). (2) The whole-unit loss removes `unitCount × d / 250` **plus one** units. It is a Delphi `for i := 0 to n` loop, and the text first said `unitCount × d / 250`. (3) A carried army adds its **siege** strength (`FUN_0044A930`) divided by 50, not its field power. The build repo's T31 had already caught that one.

### `FUN_0044B5D0` and `FUN_0044B4F8`, instruction by instruction (2026-09-23)

Read from a headless-Ghidra machine-code listing (`DumpListing.java`). The fleet record is `0x49C26C + fleet × 0x1A`: `+8` owner, `+0xC` moves, `+0x12` ships, `+0x14` condition, `+0x16` carried army (`−1` = none). The nation's unity is `0x474AB0 + nation × 0x494`, which is nation `+0x440`.

**`FUN_0044B5D0(attacker = EBX, defender = EDI)` `[confirmed]`:**

| Address | Instructions | What it does |
| --- | --- | --- |
| `0x0044B5EF` | `MOV word ptr [attacker+0xC],0` | `attacker.moves = 0` |
| `0x0044B5FB`–`B60A` | `CALL 0x0044AA54` (attacker), result to `[ESP]`; `CALL 0x0044AA54` (defender), result in `EAX` | `pA`, then `pD`. The attacker's `Random(4)` is drawn first. |
| `0x0044B60A`–`B60D` | `CMP EAX,[ESP]`; `JGE 0x0044B68D` | the defender wins if `pD ≥ pA` |
| `0x0044B631`–`B66F` | `SAR EDX,1`; `ADC EDX,0`; `SUB`/`ADD word ptr [nation×0x494+0x474AB0]` | `unity[loser] −= loserShips / 2` and `unity[winner] += loserShips / 2`, truncated toward zero |
| `0x0044B677`–`B67F` | `MOV CX,[ESP]` (`pA`); `MOV EDX,EAX` (`pD`); `MOV EAX,EBX`; `CALL 0x0044B4F8` | attacker won: **`FUN_0044B4F8(attacker, pD, pA)`** = (winner, **loser**, **winner**) |
| `0x0044B684` | `CALL 0x0044AD38` (defender) | the loser's fleet is tombstoned (owner `+8 = 0xFFFF`), and its carried army is deleted through `FUN_0044AB90` |
| `0x0044B6F5`–`B6FD` | `MOV ECX,EAX` (`pD`); `MOV DX,[ESP]` (`pA`); `MOV EAX,EDI`; `CALL 0x0044B4F8` | defender won: **`FUN_0044B4F8(defender, pA, pD)`** = (winner, **loser**, **winner**) |
| `0x0044B709`–`B723` | `MOV AX,0x3DE`; `CALL 0x00448FD0` | `unity[winner] = min(990, ·)`. The loser's unity has no floor. |

In both branches, `param_2` is the **loser's** power and `param_3` the **winner's**. Both are passed as 16-bit words (`MOV CX,word`; `MOVSX` in the callee). A fleet's power is at most about `1,000 + siegeStrength / 50`, so `[derived]` that truncation never binds.

**`FUN_0044B4F8(fleet = EDI, param_2 = EBX, param_3 = CX)` `[confirmed]`:**

```text
0x0044B500–B50C  raw = (sext(param_2) × 100) / sext(param_3)      // 32-bit IDIV, truncation toward zero
0x0044B50E–B514  r   = max(1, raw)                                // FUN_00448FD8, AX = 1
0x0044B51B–B528  d   = (r × r) / 100                              // IDIV 100
0x0044B539–B54A  ships     −= (ships × d) / 300                   // IDIV 0x12C
0x0044B54E–B55C  condition −= (condition × d) / 300
0x0044B560–B568  if carried (+0x16) ≤ −1: goto end
0x0044B56A–B56C  FUN_0044AE20(carried, d)                         // EDX = ESI = d: the ratio IS d
0x0044B571–B579  re-read carried; if now ≤ −1: goto end           // the deletion pass may have emptied it
0x0044B57B–B57F  CMP SI,0x46; JLE end                             // requires d > 70
0x0044B581–B596  n = (FUN_0044A66C(carried) × d) / 250            // IDIV 0xFA; the count is taken AFTER FUN_0044AE20
0x0044B59A–B59D  TEST SI,SI; JL end
0x0044B59F       INC ESI                                          // loop counter = n + 1
0x0044B5A0–B5BF  loop: c = FUN_0044A66C(carried);                 // re-read every pass
                       k = FUN_0040284C(c);                       // Random(c): 0 … c−1
                       FUN_0044AC3C(carried, k);                  // remove unit k
                       DEC SI; JNZ loop                           // exactly n + 1 passes
0x0044B5C3       end: FUN_0044A878(fleet)                         // map-marker redraw by ship band only
```

The helpers, from their own listings `[confirmed]`: `FUN_0044A66C(army)` returns one more than the highest slot index with `troops > 0` (`0x0044A66E`–`A692`), which is the unit count because slots are kept packed. `FUN_0044AC3C(army, k)` copies the **last** occupied slot over slot `k` (`REP MOVSD`, 8 dwords), zeroes the last slot's troops (`0x0044AC8C`), and, if slot 0's troops are then `0`, deletes the army through `FUN_0044AB90` (`0x0044AC93`–`ACA0`). That function writes `0xFFFF` into the carrying fleet's `+0x16` and tombstones the army's owner. The removal is **swap-with-last, not a shift**, so it reorders the survivors.

**Consequences `[derived]`:**

- The winner has power `≥` the loser's, so `r ∈ [1, 100]` and **`d ∈ [0, 100]`**. `d = 0` whenever `r ≤ 9`, i.e. when the loser has under 10 % of the winner's power. `FUN_0044AE20` is then still called with `ratio 0`: no troops are lost and its 20 draws are consumed, but its small-unit deletion pass still runs.
- `d ≤ 100` gives `n ≤ 0.4 × c`, so `n + 1 ≤ c` for every `c ≥ 1`, and the loop never outruns the army. With `c ≤ 2`, `n = 0` and exactly one unit goes, so **a one-unit carried army is always destroyed when `d > 70`**.
- An even fight (`d = 100`) costs each carried unit `troops / (Random(15)+105) × 100`, about 84–95 %, before the whole-unit loss.
- If both powers are 0, the defender wins the tie and `0x0044B50C` divides by zero. That needs two fleets with no ships or no condition and no army aboard.

**The storm reuses this function, with the arguments the other way round from the battle `[confirmed]`.** `FUN_004514EC`'s fleet tick (`0x00451823`–`0x00451832`: `MOV CX,[ESP+2]; ADD CX,0x64; MOV DX,0x64; MOV EAX,EDI; CALL 0x0044B4F8`) calls **`FUN_0044B4F8(fleet, 100, dmg + 100)`** for `dmg ≥ 6` (`CMP [ESP+2],5; JLE` at `0x0045181B`). So `r = 10000 / (dmg + 100)`, and `d` *falls* as `dmg` rises `[derived]`: `dmg` 7 → `d` 86, 9 → 82, 11 → 81, 13 → 77, 15 → 73, 17 → 72, and the winter spike 30 → 57. (Per [supply-driven-morale-and-fleet-attrition.md](supply-driven-morale-and-fleet-attrition.md), `dmg ≥ 6` is reached only away from a friendly coast, where it is odd, or through the winter spike.) Every heavy storm except the winter spike therefore has `d > 70`. An army aboard takes `FUN_0044AE20` at that `d` and loses `n + 1` whole units, the same as a winning fleet's army.

The loser's fleet is destroyed outright regardless of margin — there is no partial naval defeat. Nothing in `docs/game-design.md` covers naval combat at all.

## Victory condition — it is in the code

`game-design.md` lists victory conditions as `[designed, never reverse-engineered]`. `THumanFalls_InitializeForm` (`0x00455E38`), the game-over screen, tests

```c
if (nation[+0x446] < 334)   // city count < the total number of cities
     ... "Your nation has been conquerred by <nation[+0x44E]>." or the year-limit message
else "You have conquerred the Mediterranean, a unique achievement."
```

so the win condition is **holding all 334 cities**, and the screen also handles a time limit: it compares the current year `DAT_004A0332` against `250` (`0xFA`) and reports the reign's length as `270 − year` years, confirming **270 BC start**. It then prints a start-versus-end scorecard from nation fields `+0x430`/`+0x434` (population now/at start), `+0x446`/`+0x448` (cities now/at start) and `+0x438`/`+0x43C` (treasury now/at start).

`TPremierForm_Abdicate` (`0x0045B24C`) and `TPremierForm_HumanLeaderFalls` (`0x0045C238`) both route to the same "nation drops out" handler `FUN_00449078` — voluntary abdication and defeat use one path.

## What this does not establish

- The AI's *decision* to offer or accept diplomacy outside the two triggers above — still unnamed AI code, still out of scope per the roadmap.
- The reparation formula against real save bytes (see the check suggested above).
- Whether the 250 BC comparison is the actual end-of-game trigger or only the game-over screen's wording; the turn loop was not re-read for a year check this pass.
- `nation[+0x44E]` ("conquered by") — inferred from its only use, not otherwise confirmed.
- `FUN_0044AE20`'s exact casualty distribution (already noted as open in `decompiled-defection-and-siege-attrition.md`).

## Reproduction

```text
grep -n "TPolitics_\|TBattlePols_\|THVHBatPols_\|THumanFalls_" delphi_symbols.tsv
# in all_app_functions.txt: FUN_00449b40, FUN_00450c68, FUN_0044aee4, FUN_0044b5d0, FUN_0044b4f8
grep -n "sues \| destroys army of \| sinks fleet of " all_app_functions.txt
```

The 2026-09-23 naval section is from the machine code (headless Ghidra, `-noanalysis -readOnly`, `-postScript DumpListing.java out.txt`), with the listings of `0x0044b5d0 0x0044b4f8 0x0044aa54 0x0044a66c 0x0044ac3c 0x0044ad38 0x0044a878 0x0044ae20 0x00448fd0 0x00448fd8 0x0040284c 0x004514ec`.

## Next checks

1. Read `nation[+0x44C]` (wealth) and `nation[+0x446]` (cities) for Ptolemaic out of the save immediately before the `999 → −1270` reparation and check `2269` falls in the formula's range.
2. Search the news logs of existing saves for the literal strings `"sues "`, `" destroys army of "` and `" sinks fleet of "` — every one found is a free confirmation of one of the three resolvers above, with no new play session needed.
3. Re-read the turn loop for a year-250 end-of-game check to confirm or refute the time limit.
