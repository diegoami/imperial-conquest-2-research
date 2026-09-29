# Fortification orders: cost, rate, and a bug that resets a town to 0%

**Question.** [2026-09-29-which-cities-may-recruit-and-troop-amounts.md](2026-09-29-which-cities-may-recruit-and-troop-amounts.md) found that a town may recruit only if it is the capital or its fortification is at least 75%. That leaves fortifying a town as the only way to add recruiting towns. How much does a fortification order cost, how fast does it build, and what can go wrong?

**Answer.**
- **Cost:** one fortification point costs **the town's population** in talents. The whole order is paid up front.
- **Rate:** the order builds at **10 points per turn** at most.
- **Cancellation:** a hostile army next to the town cancels the rest of the order without a refund.
- **Bug:** an order that ends at **exactly 100%** with a last step smaller than 10 points leaves the town at **0%**. This was confirmed live in the headless game.
- **Live, all of it:** the dialog's clamp, its cost and the up-front payment, the build rate and the cancellation by an enemy army were each confirmed live (§6).
- **The AI never fortifies:** it places no fortification orders at all (§7).

## Method

- **The order dialog:** handlers located from the executable's published-method table and decompiled with Ghidra 12.1.3 headless: `InitializeForm` `0x4404C0`, `PrintNumbers` `0x440658`, `ChangeFortification` `0x44076C`, `OK` `0x4407E4`. Its caption is "Fortify <town>", and the town comes from the unit-map form (`+0x222`).
- **The build step:** the weekly tick `FUN_004514EC`, read instruction by instruction at `0x4515A2`–`0x4515FA`. It had already been described from decompiled text in [city-population-growth.md](city-population-growth.md).
- **Fields:**
  - city `+0x1A` is fortification: ≤ 100 is the current level; above 100 means `pending points × 100 + current`;
  - city `+0x1C` is **population** ([city-population-growth.md](city-population-growth.md));
  - nation `+0x438` is the treasury.
- **Live test:** `ng1_rome.sav` (fixtures `saves/new-game-probes/`) was edited to plant three pending orders in quiet Roman towns, saved as `fort_probe_before.sav`. It was loaded in the watch+autosave build under Wine and one turn was ended. The autosave is `fort_probe_after.sav`. Both are in fixtures `saves/fortification-probe/`:

  | File | SHA-256 |
  |---|---|
  | `fort_probe_before.sav` | `2a350117dcd451d460800fbe93002b97bf0365142dc487bebb36bdab1f8244a4` |
  | `fort_probe_after.sav` | `9f09f7fa8db06d18c920e9c9845c3d93a13ef3127265b16ccf7e67c0df9586b3` |

## Observations

### 1. The order dialog

```text
open:          points = 0; shows the current level
arrows:        points ± 1 (small spin) or ± 10 (large spin)
clamp:         points = max(0, min(points, 100 − fortification word))
shows:         new level = current + points;   cost = population × points
OK:            fortification word += points × 100          // becomes a pending order
               treasury (+0x438) −= population × points     // paid now, in full
```

- **No money check:** OK does not check the treasury, so the treasury can go negative.
- **One order at a time:** while an order is pending, the word is above 100, so `100 − word` is negative and the clamp forces points to 0. A second order cannot be placed until the first completes.

### 2. The build step, once per turn (the weekly tick, which runs once per full round of nations)

```text
if word > 100:
    if a hostile army threatens the town (FUN_004497CC):
        word = word % 100                          // pending points dropped; nothing refunded
    else:
        word += min(10, word / 100)                // add up to 10 points to the current level
        word −= min(1000, (word / 100) × 100)      // remove them from pending, computed on the NEW value
```

The second line reads `word` **after** the addition. When the current level reaches exactly 100 in that step, `word / 100` includes one extra hundred, and the whole word is removed.

### 3. The live test (one turn)

| Town | Word before (current + pending) | Expected by §2 | Word after |
|---|---:|---:|---:|
| Ariminum | 595 (95% + 5) | **0** | **0** |
| Altinum | 2550 (50% + 25) | 1560 | 1560 |
| Capua | 1857 (57% + 18) | 867 | 867 |

All three match. Ariminum shows the bug: a town at 95% ordered to 100% is at **0%** after one turn.

### 4. Which orders are hit

- **When it happens:** exactly when `current + points = 100` and `points % 10 ≠ 0`, because the final, partial step is the one that lands on 100.
- **Examples:** 95 + 5 → 0; 62 + 38 → 72 → 82 → 92 → **0**. By contrast, 60 + 40 → 100 correctly.
- **Maximal orders are the risky ones:** the dialog's maximum order is exactly `100 − current`, so a "fortify to the top" order is hit whenever the current level does not end in 0.
- **Orders to 75% are never affected.**

### 5. What it costs Rome at game start (from `ng1_rome.sav`)

- **Start position:** Rome's treasury is 2,200. Two of its 25 towns can already recruit: the capital (78%) and **Luceria (77%)**.
- **Cheapest towns to bring to 75%:**

  | Town | Fortification | Population | Points to 75 | Cost | Turns |
  |---|---:|---:|---:|---:|---:|
  | Arretium | 72 | 33 | 3 | 99 | 1 |
  | Pisae | 69 | 23 | 6 | 138 | 1 |
  | Antium | 69 | 33 | 6 | 198 | 1 |
  | Hadria | 62 | 18 | 13 | 234 | 2 |
  | Alba Fucens | 61 | 23 | 14 | 322 | 2 |
  | Fregellae | 61 | 23 | 14 | 322 | 2 |
  | Paestum | 58 | 19 | 17 | 323 | 2 |
  | Capua | 57 | 27 | 18 | 486 | 2 |
  | Tarrentum | 62 | 47 | 13 | 611 | 2 |
  | Neapolis | 40 | 34 | 35 | 1,190 | 4 |

- **Cost per point is population,** so small towns are cheap to fortify. The towns that reach 75% cheaply are mostly small ones.

### 6. Live checks of the dialog and of cancellation

**The dialog, driven headless.**
- **Setup:** `ng1_rome.sav` was loaded, Capua was selected on the unit map, and **Unit map → City → Fortify city** opened the dialog "Fortify Capua" (initial 57%, cost 0).
- **The clamp:** five presses of the 10s up-arrow stopped at **100%, cost 1,161**, which is 43 points × population 27.
- **The order:** stepping back to 18 points showed **75%, cost 486**.
- **Paid at once:** after OK, the Information panel showed `57% (under construction)`. A save made right away (`fort_ui_after_ok.sav`) had Rome's treasury at **1,714** (from 2,200, −486) and Capua's word at **1857**.
- **One turn later** (`fort_ui_after_turn.sav`) the word was **867**, that is 67% with 8 pending.

**Cancellation.**
- **Setup** (`cancel_probe.sav`): in `ng1_rome.sav`, Gaul's army 9 was moved from (96,30) to (94,34), next to Pisae (93,35), by editing its record and the two map squares (an army square is `200 + terrain`). Rome and Gaul are at war in that save (relation 3 both ways). Orders were planted at Pisae (669: 69% + 6) and at Arretium (372: 72% + 3); Arretium's only neighbouring army is Roman.
- **One turn later** (`cancel_probe_after.sav`): **Pisae 69** (the pending points dropped, nothing refunded) and **Arretium 75** (completed).
- **It was the tick, not a siege.** In that game's turn order the weekly tick runs before Gaul's seat, so the tick saw the Gallic army first. The news log has no siege of Pisae. Gaul's army went on to take Tarquinii in its own seat.

| File (fixtures `saves/fortification-probe/`) | SHA-256 |
|---|---|
| `fort_ui_after_ok.sav` | `6f736a962808666421680805af1f219683ee8800ae9dfb7d748a1683ebb8b54a` |
| `fort_ui_after_turn.sav` | `50c62970270b7dd6dea17b762cdff1727d7bdd34883d8ffc4baf2730977e45c8` |
| `cancel_probe.sav` | `36ab223fdc586b7ff77438d72e25227f66e787dea7efd17acea334b9a7484ff2` |
| `cancel_probe_after.sav` | `cc28a69ebed076340a360c4136b5cb0a695620a61d0b823cadea158e0a1fb80d` |

### 7. The AI does not fortify

A sweep of the whole code section looked for word writes to a city record's `+0x1A` near a load of the city-table base (`0x479590`). It finds four writers besides the weekly tick, which walks the table with its own pointer:

| Address | Function | Effect on the fortification word |
|---|---|---|
| `0x440801` | Fortify dialog `OK` (`0x4407E4`) | `+= points × 100` (places an order) |
| `0x44B2B9` | siege attempt `FUN_0044B27C` | `%= 100` (drops a pending order) |
| `0x44BE6F` | capital relocation `FUN_0044BD2C` | the new capital gets `min(99, fortification + 10)` |
| `0x44C4E8` | rebirth `FUN_0044C360` | the same, for a reborn nation's new capital |

**Only the dialog places orders, and only a human seat opens the dialog.** So the AI never fortifies. Its towns change fortification only through sieges and capital moves.

### 8. A newly fortified town recruits the next turn

- **Setup:** `cancel_probe_after.sav` is the turn after Arretium's order completed (72% → 75%). Loaded headless, **Strategy → Recruit unit** opened "Army recruits".
- **The town list read "Arretium, Luceria, ROME":** the capital plus the two towns at ≥ 75%. Pisae (69%, its order cancelled) was not listed.
- **The order:** Arretium was selected, Heavy infantry chosen, and the dialog showed the default **1,200** (6,000 ÷ 5), initial cost **120** and quarterly cost **12**. Recruit unit added "Hvy inf 1,200 not ready" under Arretium, and an **"All cities"** entry appeared, as the code predicts once two towns have units in training.
- **In the save** (`recruit_after.sav`, SHA-256 `ce704324d830f4fa3539387ac87f60eaf3b8ded7755c245473b3de0c6a60d53a`), against the save loaded:
  - the treasury went 2,200 → **2,080**;
  - mobilisation went 30 → **31**;
  - a new slot holds `state 0, type 1, 1,200 troops, city 81` (Arretium).

## Inferences

- **For the build repository:**
  - a fortification order costs `population × points`, paid when placed, with no treasury check;
  - it adds at most 10 points per turn, and at most one order per town at a time;
  - a hostile army next to the town cancels the remainder with no refund.

  Whether to reproduce the 100% bug is a design decision. A faithful mode would reproduce it. `[derived]`: observations 1–3.
- **For a player or a bot:**
  - fortify to 75%, not 100%;
  - if an order must reach 100%, make `100 − current` a multiple of 10, or split it into two orders so the final step is a full 10;
  - choose small towns near the front;
  - keep enemy armies away from a town while its order is pending.

  `[derived]`
- **An AI town never fortifies.** An AI nation's recruiting towns stay the ones it starts with, plus a new capital's +10 when it moves, so only the human's recruiting base can grow. `[derived]`: §7.
- **Why this was never seen in play:** no evidence save had an order in progress ([city-population-growth.md](city-population-growth.md), "What this does not establish"). A player who fortified a town to the top and saw it at 0% would have taken it for a siege.

## What this does not establish

- Cancellation was observed once, through the tick. The siege path clears a pending order the same way, but in the code only.
- The AI search is a pattern sweep, not an exhaustive data-flow proof. A writer that reaches the field through an unusual pointer would be missed. The four hits match every writer the decompiled dump shows.

## Reproduction

1. **Plant the orders:** in `ng1_rome.sav`, set the fortification word (city record `+0x1A`, SAV offset `89,600 + city × 34 + 0x1A`) of cities 87, 86 and 100 to 595, 2550 and 1857.
2. **Play one turn:** load the edited save in a build with the autosave option and end one turn.
3. **Check:** read the three words from the autosave.

## Next checks

- None open for fortification. The AI search (§7) could be made exhaustive with a data-flow pass if it ever matters.
