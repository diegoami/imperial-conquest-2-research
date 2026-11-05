# AI audit #195, step 7: the late-year rows (266–264 BC) classified; one fleet-route candidate

**Tag:** [measured: anchored remake replays of stored original games; heuristic classification]. Wine only for the
original side (the stored games).
**Provenance:** draft from `diegoami/ic2-conquest`, `findings/2026-11-05-audit195-step7-late-years.md` (PR #343, merge
`a1d16276`). Remake pin `168dbc04` (v0.9.4).
**Task:** research #195, step 7 of the [inventory](2026-11-04-ai-audit195-inventory.md): the first late-year rows. They
come from [the replays to 264 BC](2026-11-04-late-replays-and-observer-mode.md).

## Data and method

- **Data:** the 222 position rows from 266–264 BC in the three long games replayed on `168dbc04`: Carthage (104 rows),
  Rome-h1 (35) and Ptolemaic-rulebot2-h1 (83). The observer games were replayed only on `a44c42fc` and are left out.
- **Method:** `late_classify.py` gives each row the first class that applies:
  - **human_phase:** the human's nation, or units that already differ after the human phase;
  - **diplomacy:** the nation's own new relations differ;
  - **human_battle:** the nation's news this turn names the human;
  - **battle:** its battle or siege news differs;
  - **downstream:** an earlier seat in the round already has a row;
  - **quiet:** none of these. Quiet fleet rows are split: `quiet_fleet_ports` when both games' tiles are next to an own
    city, otherwise `quiet_fleet`.

## Result

| class | rows |
|---|---|
| human_phase (all Seleucid's armies, the rulebot-2 game's handed-over human seat) | 53 |
| diplomacy | 27 |
| battle | 26 |
| human_battle | 7 |
| downstream | 41 |
| quiet_fleet | 45 |
| quiet_fleet_ports | 3 |
| quiet (armies) | 20 |

- **Draws and their consequences** (diplomacy + battle + downstream) account for 94 rows: 42 % of all 222 rows, and 56 %
  of the 169 that are not from the human phase. The 7 human_battle rows are counted separately.
- **The 68 quiet rows are the rule candidates.** Their largest tile distance between the two games:
  - **armies:** 8 within 3 tiles (tie-like, around capitals), 11 farther, 1 unpaired;
  - **fleets:** 8 within 3 tiles, 39 farther, 1 unpaired.
- **One recurring pattern: Celtiberia's fleet 6.** In the Carthage game it has 14 rows, 12 of them quiet, mostly every
  other turn from t96 to t145.
  - The original sails it between (48,56) and about (70,67). The remake keeps it at (48,56).
  - The remake's AI log at t127 reads "original zero-move mercenary rendezvous army-15: fleet fleet-6 toward (48, 56)" and
    "fleet phase: fleet-6 stored-route".
  - So it is a candidate for the fleet route or the rendezvous (D19 territory).
- **Ptolemaic's fleets** have 14 quiet rows in the two rulebot-1 games. At t130 the remake gives both fleets "port".

## Open (scheduled)

`patches/fleetphase_hook.py` on the Carthage game's t127, t129 and t130. They start from the stored `t126-a00`,
`t128-a00` and `t129-a00` with their logged RandSeeds (`late-fleet-starts/seeds.json`); none of those turns has human
orders. The run is queued after C22 v4 and the `FB7C` stays run.

No inventory row changes yet.

## Intake verification (research, 2026-11-05)

**Checked:**
- **`late-classify-v2`:**
  - `rows.jsonl` has 222 rows, and the per-game and per-class counts match `summary.txt` and the table;
  - all 53 human_phase rows are Seleucid armies in `ptolemaic-rulebot2-150t-h1`;
  - Celtiberia's Carthage-game fleet rows are 14 (11 quiet_fleet, 1 quiet_fleet_ports, 2 battle) at the turns listed;
  - the Ptolemaic quiet fleet rows in the rulebot-1 games are 14.
- **`quiet_distances.jsonl` (`max_tiles`):** the buckets as tabled. The draft's message gave only the "39 farther" fleets;
  the 8 near and 1 unpaired are added here.
- **`late-ailog-v1`:**
  - the t127 fleet-6 lines ("original zero-move mercenary rendezvous army-15 … toward (48, 56)", "fleet-6
    stored-route");
  - Ptolemaic's t130 "port" for fleets 1 and 5.
- **Arithmetic:** 94 = 27 + 26 + 41, which is 42 % of 222 and 56 % of 169; quiet = 45 + 3 + 20 = 68.

**Narrowed:**
- **The classes are heuristics,** assigned first-match. "Battle" and "downstream" mean "plausibly a draw or a
  consequence", not traced. "Quiet" means none of the heuristics fired, so it is a candidate, not a found rule
  difference.
- **The rows carry no fleet id.** "Fleet 6" comes from the AI log at t127, not from every row.

**Not checked:** the classifier script, and the `seeds.json` starts.

## Evidence

- `runs/experiments/data/run-exp-audit195/` (conquest):
  - `late-classify-v1/` and `late-classify-v2/` (`rows.jsonl`, `summary.txt`, `quiet_distances.jsonl`);
  - `late-ailog-v1/` (Carthage t127, t130);
  - `late-fleet-starts/` (`seeds.json`).
- Tooling: `runs/experiments/audit195/late_classify.py`, and `patches/fleetphase_hook.py` (scheduled).
- The replays and their saves: [late replays](2026-11-04-late-replays-and-observer-mode.md) and the 168dbc04 recheck.
