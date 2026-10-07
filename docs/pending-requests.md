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

## AI-mover contact resolution: open-terrain fight, no tactical battle? (experiment request from imperial-conquest-main)

Asked by the imperial-conquest-main session on 2026-10-07, passed through the research
session as a forwarded experiment request. Closes the named strategic-AI report open-list
item: "Whether `FUN_0044d734`'s contact resolution differs for an AI mover" — and lets the
clone's faithful-AI path share one contact resolver with the human twin (already in
T112 #570).

**Design (as specified by the requester):** a fixed-seed new game on a known map where a
computer seat has an army that will move onto a tile holding an opposing army. If the
runner-3 stock new-game doesn't place an opposing army, drive a manual `move` and let the
next computer-seat turn resolve the contact (the contact resolution runs on the AI's turn,
not the human's). Three before-and-after save pairs:

  (i) AI mover onto an open tile holding an enemy army — no movement cost deducted, defender
      resolves, no tactical battle in the open field (hypothesis from the human twin).
  (ii) AI mover onto a city tile — siege path, owner and population may move.
  (iii) Human mover control — same defender, for cross-check.

**Measure:** the SAV fields that move — the mover's armyRecord after-state (rows, supplies,
money, moves), the defender's, the city's owner and population (case ii), the news log of the
AI's turn, and whether a tactical battle opened (autosave at the AI's battle screen vs
autosave at the AI's map view).

**Already known:** `2026-10-07-strategic-ai-turn.md` §2.2 names `FUN_0044dba8` as the
destination call (the mover itself, no waypoints); §3's open-list item explicitly:
"`FUN_0044d734`'s contact resolution for an AI mover"; the human twin's path through
`TUnitMap_MoveArmy` and `FUN_004492C0`'s 3×3 placement scan is in
`decompiled-unit-map-orders-and-record-fields.md`.

**Deliverables, in ic2-conquest's usual way:**

  - the three saves in one run-<id> release, cited by bare file name.
  - a findings/ draft with Method, Observations, Inferences kept apart, and a "What this does
    not establish" section; Wine-only is a candidate until the desktop confirms it.
  - tell the user the draft's file name and branch, so the research repository's findings
    intake can review it.

**Rules:** do not write to imperial_conquest_2 or the research repository; cite the saves
through `docs/evidence-index.md` as usual; remove this entry when the draft is promoted or
rejected.
