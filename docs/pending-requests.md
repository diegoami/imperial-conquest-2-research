# Pending research requests

Requests from other sessions that are accepted but not done. Whoever picks one up (any session)
removes it here when its report is promoted, and tells the requester.

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
