# The #925 reachable tiers: Improved preset only; classical-faithful marches like the original (owner decision)

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `b6ff266` (PR #287). The
owner confirmed the decision in this research session on 2026-10-31.

**Tag:** owner decision. The evidence it rests on is `[confirmed]` and is cited below. This is a
direction for the remake, not a rule of the original game, so it is not part of the rules
specification.

## Decision (the owner, 2026-10-31)

The remake's #925 "Hazards" tiers apply **in the Improved preset only**. The owner adopted them on
remake #925 on 2026-10-10. They are:
- the reachable resupply city;
- the reachable garrison fallback;
- the emergency move.

**In classical-faithful:**
- AI armies march at the original's destination:
  - `FUN_0044e670`'s resupply pick; or
  - `FUN_0044ebe8`'s nearest city of any owner (strict `< 10` capital radius, first in the city
    table) or the capital.
- They use the original walk `FUN_0044dba8`, including the no-progress swing
  ([#105](2026-10-30-ai-move-fallback-point105.md)) and the stay-put case.
- The emergency tier does not run.

**The Improved preset keeps the tiers unchanged.**

## Evidence

- [AI decisions vs remake main](2026-10-30-ai-decisions-vs-remake-main.md):
  - 252 resupply rows and 8 fallback rows of 749 differ through the tiers, the largest group after
    "same";
  - in the 14 non-adjacent rows the remake's raw pick equals the original's (14 of 14); the other
    238 have the army already next to its home city;
  - on the `05b02936` recheck, 250 + 8 rows remain, and every other army decision outside diplomacy
    and battle draws matches.
- [Garrison and mercenary boundaries](2026-10-30-garrison-and-mercenary-boundaries144.md): `< 10`,
  `< 20` and table-order ties in the same functions.
- [AI diplomacy](2026-10-30-ai-diplomacy-vs-remake-main.md) and
  [AI economy](2026-10-31-ai-economy-vs-remake-main.md): no tier involvement.

*Review:* I checked these figures against the cited reports. 238 + 14 = 252, which matches the
reports' 252 resupply rows and their 14 of 14 non-adjacent rows.

## For the remake

- In classical-faithful:
  - `ResolveResupplyCity` returns `ScoreResupplyCity`'s pick;
  - `GarrisonFallback` returns the nearest city of any owner (strict `<`, first in table order), or
    the capital;
  - the emergency tier is skipped.
- After the change, the 252 resupply rows and the 8 fallback rows are expected to match. They can be
  rechecked with conquest's `runs/experiments/aidecide/compare.py`.

## What this does not decide

- Anything about the Improved preset beyond keeping the tiers.
- The remake's implementation.
