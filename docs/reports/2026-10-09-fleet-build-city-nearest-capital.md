# Build fleet in the original builds at the own coastal city nearest the capital that has no fleet under construction; the remake takes the first in world order

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `d13eaca`. Release
[`run-exp-fleet-build-city`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleet-build-city)
holds the saves and the order-7 screenshot, and their SHA-256s are committed at
`runs/experiments/data/run-exp-fleet-build-city/SAVES.sha256`. Wine-only. This is an original-side
check for [`2026-10-09-remake-v050-gap-analysis.md`](2026-10-09-remake-v050-gap-analysis.md) (rows_g1
NEW-g1-3, rows_g2 check 8).

**Review note:**
- The cited run's saves (`183238_FB_after_1`, `183238_FB_end`) and the screenshot hash OK.
- **From `20261009-183238_FB_end.SAV`, read with my own script:** fleets 2-7 are Rome's (owner 0),
  countdown 24, and their `+20` build-city indices are 82, 89, 80, 71, 101 and 87. Those are Caere,
  Antium, Tarquinii, Pisae, Neapolis and Ariminum, at Chebyshev distance 2, 3, 4, 8, 9 and 10 from
  Rome (101,43).
- **Using `+20` as the build city is right for a fleet under construction.**
  [`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md)
  has `FUN_0044A004` write the build-city index there, and `FUN_0044A050` overwrite it with condition
  100 at launch.
- **Water adjacency, recomputed from the save's map** (a code 0 or 1 in the 3×3 around the city):
  Rome's cities in distance order are Rome (no water), Caere ✓, Carsioli ✗, Antium ✓, Alba Fucens ✗,
  Fregellae ✗, Tarquinii ✓, Hadria ✗, Cales ✗, Arretium ✗, Capua ✗, Pisae ✓, Neapolis ✓ and
  Ariminum ✓. The six fleets took exactly the ✓ cities, in that order.
- **It matches the code reading** of `FUN_004496e0` in
  [`2026-10-07-strategic-ai-turn.md`](2026-10-07-strategic-ai-turn.md) (the AI's fleet order: "own
  coastal city with a free adjacent water cell, nearest the capital, not already hosting a
  construction order"). This run shows the same choice for a human Build fleet order.
- **Not checked here:** the remake side (code reading).

**Tag:** `[confirmed]` (Wine) for the six choices; the rule `[derived]`; the remake side is a code
reading.

## Answer

- **Six Build fleet orders in one turn** (`build_city-20261009-183238.jsonl`; start `run0-start-AUTO0720-seed12345.SAV`, Rome; 10 ships each) were built, in this order, at:
  - **Caere** (Chebyshev distance 2 from Rome), **Antium** (3), **Tarquinii** (4), **Pisae** (8), **Neapolis** (9), **Ariminum** (10);
  - each box read "The fleet will be built at <city>.";
  - the treasury fell 2,200 → 1,600, 100 per order (ships × 10).
- **The save confirms it** (`20261009-183238_FB_end.SAV`): six fleet records, each under construction (countdown 24), with build city Caere, Antium, Tarquinii, Pisae, Neapolis and Ariminum.
- **That is exactly Rome's cities touching the sea, nearest the capital first**, each taken once (the table in the same log's `rome_cities` step). Cities with no sea in their 3×3 (Carsioli 2, Alba Fucens 3, Fregellae 3, …) are skipped `[confirmed]`.
- **A city with a fleet under construction is not free** `[confirmed]`: no city got a second order.
- **The rule** `[derived]`: the own coastal city nearest the capital that is not already building a fleet. It agrees with the research report's AI port rule `FUN_004496e0` ("own coastal city with a free adjacent water cell, nearest the capital, not already hosting a construction order", `2026-10-07-strategic-ai-turn.md` §2.4). No tie between equal distances occurred, so the tie-break is not established.
- **N02 notices:** from the second order on, opening Build fleet first showed a notice, "A fleet of 10 ships will be ready in 24 weeks at <city>." (the research refusal-texts N02, information only). The driver now dismisses these notices and waits for the dialog.
- **Order 7** opened neither the dialog nor a box within 20 s (`20261009-183238_timeout_order7.png`). Not explained, and not counted.
- **The remake v0.5.0 (code reading):**
  - `FreeCoastalCities` (`godot/UI/Dialogs/StrategyDialogModels.cs:372-400`) excludes the cities already building a fleet, which **matches**.
  - But it lists the cities **in world order** (`CoastalCities`, `:344-363`, a plain scan of `_state.Cities`), and the dialog's OK builds at the first (`godot/UI/Dialogs/BuildFleetDialog.cs:249`). For Rome that is Pisae, the first Roman coastal city in the world's order, not Caere.
  - So the remake's dialog **differs** in which city builds (fidelity only, NEW-g1-3 as drafted).
  - The remake's `CoastalCity.IsCoastal` test was not compared with the original's "free adjacent water cell".

## Evidence

- **Data:** `runs/experiments/data/run-exp-fleet-build-city/` (`build_city.py`, `build_city-*.jsonl`, `SAVES.sha256`, `README.md`).
- **Release:** [`run-exp-fleet-build-city`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-fleet-build-city) (`20261009-183238_FB_after_1.SAV`, `20261009-183238_FB_end.SAV`, the order-7 screenshot).
- **Driver:** `harness/driver.py` `Game.build_fleet` (the N02 handling).

## Not established

- **The tie-break between equally distant cities**, and whether the sea must be free of other units ("free adjacent water cell").
- **Another nation or capital:** only Rome's capital was tried.
- **Order 7's silence.**
- **The desktop original.**
