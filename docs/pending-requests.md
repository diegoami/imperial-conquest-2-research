# Pending research requests

Requests from other sessions that are accepted but not done. Whoever picks one up (any session)
removes it here when its report is promoted, and tells the requester.

## In-play corroboration of the strategic AI turn (imperial_conquest_2 #816 follow-up)

Asked by the research session (ic2-conquest) on 2026-10-07. `docs/reports/2026-10-07-strategic-ai-turn.md`
is decompile-only; its "What this does not establish" names the in-play checks. One findings draft
from the EXPLORE runner (ic2-conquest), on a fixed seed, covering any subset of:

1. **The week-11 tax policy** (`FUN_0044ffbc`): an AI nation's `+0x44A` moving by the cut/raise/zero
   rules at the season's last week (cut to `max(5, tax−6)` if unity < 650 or treasury > wealth/2000;
   `min(40, tax+9)` in deficit or threatened-and-broke; 0 if unity < 500 with positive treasury).
2. **A free AI mercenary hire** (`FUN_0044e41c`): an at-war AI army with money > 50 acquiring a
   pool offer on a city tile within Chebyshev 4, with no payment anywhere in the diff.
3. **A homeland intercept dispatch** (`FUN_0044efc8`): an own army diverting toward a threatening
   foreign army (within 20 of the capital at war, 10 otherwise) instead of its usual target.
4. **A fleet hunt-vs-port decision** (`FUN_0044f4f8`/`FUN_0044e9a8`): a fleet chasing an enemy
   fleet (score ≥ 100) vs sailing to a resupply port, and the foreign-port purchase at amount/5.

Rules: watch AI turns on a fixed seed; cite the saves; never write to imperial_conquest_2. The
draft goes through the findings intake as usual. Remove this entry when the draft is promoted
(or rejected), and reply to the research session.
