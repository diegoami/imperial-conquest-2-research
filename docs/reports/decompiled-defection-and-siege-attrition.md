# A cascading defection mechanic, and where siege losses actually come from

Following up on `decompiled-city-capture-resolution.md`'s open item: `FUN_0044ba1c` turned out not to be a population/fortification-loss formula, but something more interesting.

## `FUN_0044ba1c`: cascading defection after a capture

Called at the end of the forced-capture transfer, this loops **every other city** and, for each one that shared the *same previous owner* as the city just captured:

```text
if other_city.owner == just_captured_city's_old_owner and other_city != just_captured_city:
    if not already contested:
        distance = grid_distance(other_city, attacking_army_position)
        if distance < 10:
            otherDefense = defender_strength(other_city)
            if other_city.allegiance == new_owner: otherDefense /= 3   // rebellious sympathy weakens it further
            if new_owner.unity < 650 and otherDefense < attacker_strength and other_city.loyalty < 65:
                FUN_0044bed8(other_city, new_owner)   // the city defects, no siege needed
```

A single successful capture can cause **nearby, weakly-defended, low-loyalty cities of the same defeated nation to defect automatically** — no army or battle involved for the secondary cities. This is very plausibly the mechanism behind every "X defects to Y" news event seen throughout this project's saves (Modena, Taurasia), which previously had no known trigger condition.

## `FUN_0044bed8`: the defection routine itself — confirms Modena's finding exactly

Structurally similar to the forced-capture transfer (`FUN_0044bb18`), but with real differences:

- **Never writes to population or fortification anywhere.** This is an exact, code-level confirmation of the Modena defection in `mobilization-movement-and-city-capture-modes.md`, where population and fortification were completely untouched while only owner and loyalty changed.
- Unity change is **+3/−20** (vs. +9/−15 for forced capture) — losing a city to defection costs the losing nation *more* unity than losing it in a straight fight.
- Loyalty, if the city ends up with a non-allegiant owner, is pulled toward a floor of **65** (vs. 40 for forced capture) — defection is gentler on loyalty than conquest, consistent with it being a "voluntary" switch.
  > **Correction (2026-09-26):** it is a formula, not a floor. Allegiant receiver: `min(90, 140 − L)`. Otherwise: `min(65, max(50, 100 − L))`, so a cascade city usually lands on **50**. All 8 cascade defections in the saves match, for example Modena 63 → 50 and Synnada 62 → 78. The old owner's unity is `max(250, unity − 20)`, which raises a unity below 270 to 250. See [decompiled-quarterly-rebellion.md](decompiled-quarterly-rebellion.md) §2–§3.
- The garrison at that city is still cleared (same as forced capture).
- **New mechanic found: nation elimination.** If the losing nation's city count reaches 0 after this defection, the nation is disabled (`TPremierForm_DisableNation`), its armies are processed via another routine, and its diplomatic/mercenary state is cleaned up — a previously unknown "last city lost" cascade, not decompiled in depth this pass.

## Where does population/fortification loss actually come from, then?

Not from either transfer routine. Back in the siege function `FUN_0044b27c` (from `decompiled-city-capture-resolution.md`), two calls happen **unconditionally, on every attack attempt — win or lose**:

- **`FUN_0044ae20(armyIdx, ratio)`**: applies a small random-percentage troop loss to *every unit in the attacking army* (`troops -= troops / (Random(15) + 105) * ratio`), then a second pass over slots 19…0 that **deletes** (`FUN_0044ac3c`, the remove-unit helper) any unit left below `standardBattalionSize / 10` (table `+0x1A`, `DAT_00478fca`) if it is national (origin label `0`), or below `/ 5` if it is a mercenary. *(Corrected 2026-09-23: this was first read as "a unit-state change if ammunition/readiness drops below a threshold". The same helper applies the instant resolver's casualties; see [instant-resolver-cannot-reproduce-a-tactical-battle.md](instant-resolver-cannot-reproduce-a-tactical-battle.md).)* This is the **attacking army's own casualties from attempting a siege**, separate from anything happening to the city. *(Added 2026-09-23: the `ratio` at this call site is `max(1, min(15, defenderStrength × 6 / attackerStrength))`, see [the instruction-level section below](#fun_0044b27c-instruction-by-instruction-2026-09-23).)*
- **`FUN_0044b230`**, called three times on three different city-stat fields, is a smoothing/decay helper: it nudges a field toward a target value derived from the current defense calculation, rather than setting it directly. Because this runs on *every* attack attempt regardless of success, it's the most likely source of the population/fortification decline observed in every successful capture in this project's data — but which of the three fields is fortification vs. population vs. something else, and the exact numeric target/rate, weren't pinned down this pass.

> **Correction (2026-09-23)**, from a targeted pass on [`imperial_conquest_2#290`](https://github.com/diegoami/imperial_conquest_2/issues/290). `FUN_0044b230` is not a smoothing helper with a target and a rate. It is a deterministic clamp, with no `Random` call: `field = max(field × 3/4, min(field × 19/20 + 1, field × defenderStrength / attackerStrength))`. The three fields are **loyalty `+0x16`, fortification `+0x1a` and population `+0x1c`**, in that order `[confirmed]`. See the section below.

**What this means for the existing empirical readings:** the population/fortification drop seen at the moment of a successful capture may be the *accumulated* effect of however many attack attempts preceded the win, not a one-time "capture penalty" applied at the transfer step — a materially different picture than assumed in earlier reports, and worth keeping in mind if a future controlled experiment tries to isolate a single-attack population-loss formula.

## `FUN_0044b27c`, instruction by instruction (2026-09-23)

Read from a headless-Ghidra machine-code listing (`DumpListing.java`, `0x0044B27C`–`0x0044B4C0`) for [`imperial_conquest_2#290`](https://github.com/diegoami/imperial_conquest_2/issues/290), which read this call site from the decompiled dump alone. Everything below is from the instructions, not from Ghidra's pseudocode.

**Registers and records.** Delphi register convention (`EAX`, `EDX`, `ECX` carry the first three arguments). `EDI` holds the army index and `ESI` the city index throughout. `EBX = 0x479590 + city × 0x22` is the city record. `[EBP−8]` is the attacker's strength and `[EBP−4]` the defender's. City fields follow the label table in the build repo's `docs/investigations/siege-defender-strength.md`: `+0x12` owner, `+0x14` allegiance, `+0x16` loyalty, `+0x1a` fortification, `+0x1c` population, `+0x1e` maximum population. The army's owner is army `+4` (`0x47C1F0`) and its moves are army `+6` (`0x47C1F2`).

| Address | Instructions | What it does | Tag |
| --- | --- | --- | --- |
| `0x0044B28B`–`B290` | `CALL 0x0044A930`; `MOV [EBP-8],EAX` | `atk = FUN_0044A930(army)` | `[confirmed]` |
| `0x0044B2A4`–`B2B9` | `CMP CX,0x64`; `JLE`; `IDIV 100`; `MOV [EBX+0x1A],DX` | if `fortification > 100`: `fortification = fortification % 100`. **A siege attempt discards a fortification order in progress**, before anything else is computed. | `[confirmed]` |
| `0x0044B2BF`–`B2C4` | `CALL 0x0044A98C`; `MOV [EBP-4],EAX` | `def = FUN_0044A98C(city)` | `[confirmed]` |
| `0x0044B2CD`–`B2E9` | `MOV AX,[army×0x290+0x47C1F0]`; `CMP AX,[EBX+0x14]`; `JNZ`; `LEA EAX,[EAX+EAX*8]`; `IDIV 10` | if `army.owner == city.allegiance`: `def = def × 9 / 10`, multiplied first and then divided with truncation | `[confirmed]` |
| `0x0044B2EC`–`B309` | `PUSH EBP`; `LEA EAX,[EBX+0x16 / 0x1A / 0x1C]`; `CALL 0x0044B230`, three times | erodes loyalty, then fortification, then population, each against the **post-×9/10** `def` | `[confirmed]` |
| `0x0044B30A`–`B322` | `MOVSX EAX,[EBX+0x1E]`; `IDIV 6`; `INC EDX`; `CALL 0x00448FD8` | `population = max(population, maxPopulation / 6 + 1)` | `[confirmed]` |
| `0x0044B328` | `CALL 0x0044A794` | redraws the city's map marker (it writes the tile code at `0x45E870` by population band `<25`, `<50`, `<100`, else). It writes no game-state field. | `[confirmed]` (listing of `FUN_0044A794`) |
| `0x0044B32D`–`B336` | `MOV EAX,[EBP-4]`; `ADD EAX,EAX`; `LEA EAX,[EAX+EAX*2]`; `CDQ`; `IDIV [EBP-8]` | `q = (def × 6) / atk`, with **`def` on top and `atk` as the divisor**, in 32 bits and truncated | `[confirmed]` |
| `0x0044B339`–`B34A` | `MOV AX,0xF`; `CALL 0x00448FD0`; `MOV AX,0x1`; `CALL 0x00448FD8` | `ratio = max(1, min(15, q))` | `[confirmed]` |
| `0x0044B355` | `MOV BX,[army+4]` | saves the attacker's nation, for the news line only | `[confirmed]` |
| `0x0044B35D`–`B361` | `MOV EDX,EAX`; `MOV EAX,EDI`; `CALL 0x0044AE20` | `FUN_0044AE20(army, ratio)`: **unconditional**, before the outcome test, and so the same on a win or a loss | `[confirmed]` |
| `0x0044B36C` | `MOV word ptr [army+6],0` | `army.moves = 0`, after the casualties | `[confirmed]` |
| `0x0044B376`–`B37C` | `MOV EAX,[EBP-8]`; `CMP EAX,[EBP-4]`; `JG 0x0044B41C` | `atk > def` → *"falls to"* and `FUN_0044BB18(city, army)`. Otherwise *"fails to capture"*. A tie goes to the defender. | `[confirmed]` |

`FUN_00448FD0` is `CMP DX,AX; JG; MOV EAX,EDX`, which is **`min`**. `FUN_00448FD8` is `CMP DX,AX; JL; MOV EAX,EDX`, which is **`max`**. These are the same two functions research `1762c84` confirmed for the tactical-morale clamp (`0x00438029`–`0x00438162`), and this pass reread both bodies. Both compare **16-bit words**.

**`FUN_0044B230(&field)`: the city erosion `[confirmed]`.** This is a nested Delphi procedure. The caller pushes its own `EBP` as a static link, which the callee reads back as `[EBP+8]`, so `[link−4]` is `def` and `[link−8]` is `atk`:

```text
t     = (field × def) / atk            // 0x0044B237–B249: IMUL dword, then CDQ, so a 32-bit product; IDIV atk
cap   = (field × 19) / 20 + 1          // 0x0044B24C–B257
floor = (field × 3) / 4                // 0x0044B260–B26A: SAR 2 with the +3 bias, i.e. truncation toward zero
field = max(floor, min(cap, t))        // 0x0044B259 min (FUN_00448FD0), 0x0044B26D max (FUN_00448FD8)
```

There is no `FUN_0040284C` (`Random`) call in it. **The erosion is deterministic.**

**Consequences `[derived]`** (arithmetic on the transcription above):

- **Attacker's attrition ratio.** `q = def × 6 / atk` rises with how badly the attacker is outmatched, and on a win it is the same function as on a loss. For example, `def = atk / 2` gives `3`, a narrow win gives `5`, a tie (which the attacker loses) gives `6`, and `def ≥ 2.5 × atk` gives `15`. Through `FUN_0044AE20`, each attacking unit loses `troops / (Random(15) + 105) × ratio`, which is at most about 14 % per attempt.
- **City erosion on a successful siege** (`def < atk`, so `t < field`): each of the three fields loses between about 5 % and 25 %, following `def / atk`. A narrow win costs the city about 5 % and a crushing one 25 %.
- **City erosion on a failed siege** (`def ≥ atk`, so `t ≥ field ≥ cap`): `field = field × 19/20 + 1`. A field at or below 20 is unchanged, and a larger one loses about 5 % per attempt. That answers this report's open item on whether a failed attempt erodes fortification: it does, for any field above 20.
- **Plan item 18's two captures** ([decompilation-plan.md](../decompilation-plan.md)) are consistent with this, assuming one attempt each. At Laranda (fortification 41 → 30, population 59 → 44), both values are exactly `field × 3/4`, so the floor binds, which needs any `def / atk < 0.756`. At Gordium (54 → 42, 23 → 18), the `t` branch binds for both fields, which needs `def / atk ∈ [0.7826, 0.7963)`, a range that is not empty. The "one random draw per capture" hypothesis there is superseded: the per-capture factor is `def / atk`. The two sieges' actual strengths were not reconstructed, so this is a consistency check and not a confirmation.

**The defender's troops take no casualties `[confirmed]`.** `FUN_0044B27C` writes no recruitment slot (nation `+0x2E4`) and no army other than the attacker. The garrison addend inside `FUN_0044A98C` is read and never written. The defender's side of a siege is exactly the three eroded fields, the population floor and the fortification-order strip. On a capture, `FUN_0044BB18` clears the old owner's slots that target the city, as [decompiled-city-capture-resolution.md](decompiled-city-capture-resolution.md) records.

**The two strength functions `[confirmed]`.** `FUN_0044A930` (`0x0044A930`–`0x0044A988`) sums over all 20 slots `troops × 3` when the unit type (`+2`) is `2` (archers) and `troops` otherwise, divides the sum by `80`, and multiplies by the army's morale (`+0xE`, `0x47C1FA`). `FUN_0044A98C` is transcribed in the build repo's `docs/investigations/siege-defender-strength.md`. Its fortification decode at `0x0044A9A7` uses the same `> 100 → % 100` guard as the siege's strip at `0x0044B2A8`, so the strip does not change `def`. Neither function calls `Random`. The only draws on the siege path are `FUN_0044AE20`'s: **exactly 20 `Random(15)` calls**, one per slot whether it is occupied or not (`0x0044AE2B` `MOV BX,0x14` … `0x0044AE61` `DEC BX; JNZ`, with the `CALL 0x0040284C` at `0x0044AE43` unconditional).

**Edge behaviour of the original `[derived]`:**

- **16-bit clamps.** `q` and `t` are 32-bit, but `min` and `max` compare only their low words. A `q ≥ 32768` therefore wraps before the clamp. That happens for a near-empty besieger against a strong city: `atk` in the low double digits against `def` near 100,000. For example, `q = 501,996` has the low word `−22,292`, which clamps to `1`, not `15`. `t` wraps the same way inside `FUN_0044B230` once `field × def / atk ≥ 32768`.
- **`atk = 0`** (no troops, or morale 0): `IDIV` by zero at `0x0044B249` in the first `FUN_0044B230` call. The original has no guard.
- **A besieger emptied by its own attrition.** If `FUN_0044AE20`'s deletion pass removes every unit, `FUN_0044AC3C` → `FUN_0044AB90` tombstones the army (owner `+4 = 0xFFFF`). The outcome test still uses the `atk` computed before the losses, and on a "win" `FUN_0044BB18` reads the new owner from army `+4` (dump: `local_14 = DAT_0047c1f0[param_2 * 0x148]`), which is now `−1`. This is a latent defect in the original. It is reachable only when every unit of a winning besieger falls below its deletion threshold after a loss of at most 15/105.

## What this does not establish

- ~~Which of the three `FUN_0044b230`-adjusted fields is fortification, which (if either) is population, and the exact smoothing formula's target/rate.~~ *Settled 2026-09-23, see the section above.*
- The nation-elimination cascade's full effects (armies, diplomacy, mercenaries).
- ~~Whether a *failed* capture attempt (city successfully defends) still measurably erodes its fortification via this same mechanism~~: *settled from the code 2026-09-23. It does, by `field × 19/20 + 1`, for any field above 20. No save pair has checked it yet.*
- Whether the Galatian captures' actual `def / atk` fall in the windows derived above.

## Reproduction

Both functions were already present in the whole-application-range dump from `decompiled-city-capture-resolution.md` (`all_app_functions.txt`); no new Ghidra invocation was needed this pass, just further reading of already-decompiled output.

The 2026-09-23 section is from the machine code:

```text
set JAVA_HOME=%LOCALAPPDATA%\ReTools\jdk-21.0.12.1+1
analyzeHeadless.bat %LOCALAPPDATA%\ReTools\ghidra_projects IC2 -process "Imperial Conquest 2.exe" -noanalysis -readOnly ^
  -scriptPath %LOCALAPPDATA%\ReTools\scripts -postScript DumpListing.java out.txt ^
  0x0044b27c 0x0044b230 0x00448fd0 0x00448fd8 0x0044a930 0x0044a98c 0x0044a794 0x0044ae20 0x0044ac3c 0x0044a66c
```

## Next checks

1. A controlled save pair around a single *failed* capture attempt (no other activity that turn). The code now predicts `field × 19/20 + 1` for loyalty, fortification and population, so one such pair confirms it.
2. ~~Identify the three `DAT_004795a6/aa/ac` fields definitively against known SAV city-record offsets, to confirm which is fortification.~~ *Done: loyalty, fortification and population. See the build repo's `docs/investigations/siege-defender-strength.md`, which reads the labels off `TInformation_ShowCityDetails`.*
3. ~~Decompile the nation-elimination cascade (`FUN_0044ab90`, `FUN_0044ad38`, `TPremierForm_DisableNation`) if a save ever shows a nation actually being eliminated.~~ **Done 2026-09-25**, see [decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md): armies are deleted, launched fleets are deleted with their passengers, and fleets under construction go to the receiver.
