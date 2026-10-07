# City marker variants: four population tiers plus the capital

**The question** ([decompilation plan](../decompilation-plan.md) item 16): what do the **five**
city marker variants mean (`map code = 20 + owner + 16 × variant`, variants 0–4,
[rivers-and-map-markers.md](rivers-and-map-markers.md)), and where are the "three city size
tiers" the asset specification assumed?

## Answer

- **Variants 0–3 are population size tiers**, by **unsigned** thresholds on the city's current
  population (`+0x1C`, thousands): `< 25`, `25–49`, `50–99`, `≥ 100`. The marker writer is
  `FUN_0044a794` **[confirmed: decompile, :49107–49135]**.
- **Variant 4 is the national capital.** `FUN_0044a794` refuses to touch a capital
  (`FUN_0044b8d0` gate); the variant-4 marker (`owner + 0x54`) is written by the capital
  relocation routine `FUN_0044bd2c` (:50296, the "*have moved their capital to …*" path) and by
  rebirth `FUN_0044c360` (:50591) **[confirmed: decompile]**. Empirically the correspondence is
  exact: in eighteen saves (five evidence-indexed fixtures plus thirteen local
  ic2-conquest saves), every live nation's capital city and only those carry variant 4 (16/16 in seventeen,
  15/15 in the one with an eliminated nation) **[confirmed: saves]**.
- **There is no "three size tiers"** — the asset specification's premise was wrong twice over:
  four size tiers, plus the capital marker as the fifth variant.
- **The tier is refreshed only when the city changes owner, never by growth.** The writer's
  callers are the ownership-change paths — siege transfer `FUN_0044b27c` (:49809), transfer/
  defection `FUN_0044bb18` (:50229), elimination `FUN_0044bed8` (:50372), conquest
  `FUN_0044c528` (:50636, :50746) — and nothing in the weekly or quarterly tick calls it. So a
  city that grows past a threshold keeps its old, smaller icon until captured **[confirmed:
  decompile + saves]**: the long runs hold variant-0 cities at population 26–28, above the
  variant-1 threshold.

**Also found, completing the marker family: fleet markers carry size bands.** `FUN_0044a878`
(:49145–49172) writes `owner + 300 / + 316 / + 332` at **< 25, 25–49, ≥ 50 ships** (unsigned), and
it is called wherever a fleet's ship count changes: joins and splits (`TFleetToFleet_OK`,
`TUnitMap_JoinFleets`, construction completion `FUN_0044a050`), storm damage `FUN_0044b4f8`, and
the AI merge `FUN_00450b30`. This explains the `332 + owner` and `333`/`335` fleet codes
[rivers-and-map-markers.md](rivers-and-map-markers.md) could only fit **[confirmed: decompile]**.
Army markers are the known three bands at 25,000/50,000 troops (`FUN_0044a80c`, same shape).

## The writer, in full [confirmed: decompile]

```c
void FUN_0044a794(short city)
{
    if (!FUN_0044b8d0(city)) {                    // not any nation's capital
        pop = city[+0x1C];                        // unsigned
        marker = owner + 0x14;                    // variant 0: pop < 25
               or owner + 0x24;                   // variant 1: 25 ≤ pop < 50
               or owner + 0x34;                   // variant 2: 50 ≤ pop < 100
               or owner + 0x44;                   // variant 3: pop ≥ 100
        map[city.xy] = marker;
    }                                             // a capital keeps its variant-4 marker
}
```

## The saves

Five evidence-indexed saves plus the bot's thirteen local ones (corroboration only), parsed with
`scripts/city-marker-check.py`: every one of the 334 cities in every save satisfies
`(code − 20 − owner) ∈ {0, 16, 32, 48, 64}` exactly, so the owner residue is current even in the
conquering runs. Population ranges per variant (eighteen saves, near-start `7.sav` and the long runs):

| variant | meaning | pop min–max observed | count (typical) |
| ---: | --- | --- | ---: |
| 0 | size tier 0 | 7–**28** (24 at game start) | ~102–105 |
| 1 | size tier 1 | 25–54 (25–49 at start) | ~94–97 |
| 2 | size tier 2 | 50–98 | ~87–89 |
| 3 | size tier 3 | 101–220 | 31 |
| 4 | capital | 26–197 (any) | live nations |

The variant-0 maxima above 25 and variant-1 maxima above 49 in the long runs are the staleness
evidence: those cities grew past the threshold without a marker refresh.

## What the reimplementation needs

Render city icons from `population` tiers at 25/50/100 (four sizes) plus a distinct capital icon,
recomputed **on ownership change only** — a faithful clone reproduces the original's stale-tier
behaviour, or must consciously decide to "fix" it. Fleet icons take three bands at 25/50 ships,
refreshed on every ship-count change; army icons three bands at 25,000/50,000 troops (already
faithful in the engine's `FUN_0044a80c` equivalent).

## What this does not establish

- The exact division of labour between `FUN_0044b8f4`, `FUN_0044bb18` and `FUN_0044bd2c` inside
  the transfer/relocation machinery was not traced call by call; only their marker writes and the
  `FUN_0044a794` call sites are cited here.
- The DAT's initial map variants were not read directly; `7.sav` (near start) is consistent with
  the tiers throughout, which is sufficient for the starting state.
- Whether a demoted ex-capital's refresh to a population tier is observable in a save (it needs a
  capital relocation followed by a capture of the old capital in one run) — none of the eighteen
  saves shows a variant-4 city that is not a live capital, so the demotion path works, but no
  single save displays the before/after pair.

## Reproduction

```text
writer        FUN_0044a794 :49107   (fleet: FUN_0044a878 :49145; army: FUN_0044a80c :49164)
capital sites FUN_0044bd2c :50296, FUN_0044c360 :50591
callers       :49809 :50229 :50372 :50636 :50746 (city), :44994 :45004 :47250 :48795 :49880 :54034 (fleet)
saves         7.sav, 1_rome_270_winter_7/autumn_7, 1_thracia_271_spring_7, 1_cartago_271_spring_7
              (evidence-indexed, fixtures releases), plus thirteen local ic2-conquest saves as corroboration
script        scripts/city-marker-check.py <save>…  (map at 0, city table at 89,600, nation capital +0x444)
```
