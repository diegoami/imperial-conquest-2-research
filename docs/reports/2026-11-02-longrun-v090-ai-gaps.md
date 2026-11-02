# Long runs against remake v0.9.0: two AI army gaps that repeat every turn (capital armies walked away; sieges by the mercenary-run branch dropped)

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `23aca35d` (PR #300), owner
request 2026-11-02 ("parallel long runs with the original and the remake", anchored + free-running,
4 starts × 40 turns). Remake compared: tag **v0.9.0**, `88c1989b`.

**Tag:**
- Gaps A and B: `[confirmed: Wine hook + remake AI log]`. Decide hook (`patches/decide_hook.py`)
  in Wine; hooked and plain autosaves byte-identical in all three runs. Remake `aiprobe` decision and
  walk logs.
- Gap C: partial. Two hunt samples, one port-tile row unexplained.
- Gap A's cause in the original: `[code-backed interpretation]` added at intake (below), not hooked.

## Method

`difftest/campaign.py` plays the rule bot (rulebot-1) as the human for 40 turns in both games. The
original runs as one process (seed 12345). `difftest/anchored.py` then replays **every turn** in the
remake from the **original's own save** at the start of that turn, with the original's orders, and
compares the end of the turn. No difference carries over between turns. `classify.py` sorts each
turn's differences by kind. `stays.py` lists the AI units that end the original's turn on their
starting tile but end somewhere else in the remake.

| Game | Turns | Human phase (our orders) | AI phase: structural turns |
|---|---|---|---|
| Rome | 40 | 40 × draws only | 39 |
| Carthage | 40 | 40 × draws only | 38 |
| Gaul | 40 | 40 × draws only | 39 |
| Seleucid | 25 (harness stop at turn 26, below) | 25 × draws only | 23 |

"Draws only" covers troop sizes, recruit types, supplies, treasury and storm tiles. The structural AI
rows are mostly the two gaps below. The rest (relations, city captures, battle outcomes) are not
attributed.

`stays.py` over the four games (`stays-v2.txt`):

| Unit next to | Rows | Cases |
|---|---|---|
| its own capital (army) | 410 | Macedonia (Pella), Media (Ecbatana), Thracia (Byzantium), Ptolemaic (Alexandria), Seleucid (Antioch), every turn they are idle |
| an enemy city (army) | 17 | Carthage–Castulo, Seleucid–Astacus, Seleucid–Synnada, Ptolemaic–Sidon, Galatia–Cius (random) |
| another nation's city (army) | 3 | Armenia–Van (same mechanism as gap A) |
| own port (fleet) | 5 | Ptolemaic–Alexandria (port tile), Carthage–Utica, Leptis Magna (random hunt draw): gap C |

## Gap A: an army whose walk ends where it started gets a second march (garrison fallback) in the remake

**Original** (hook run `hooks-decide-v1/t01-a04`, from the Rome game's save before turn 2):
Macedonia army 8 at (144,42), next to Pella (143,41), at peace, 9 moves. F31C inputs `city = -1`
lead to the **resupply** branch. The turn ends with the army at **(144,42), 2 moves left**. In the
Rome game it stays there from turn 2 to turn 40. The walk is the out-and-back swing measured on
2026-10-30 ([`2026-10-30-ai-decisions-vs-remake-main.md`](2026-10-30-ai-decisions-vs-remake-main.md):
out to (147,44) and back).

**Remake** (`probes/capital-armies-t05`, from the Rome save before turn 5): the same branch
(`MoveToResupplyCity`). The walk returns to (144,42) (2 walks, 6 of 9 moves, 3 left). Because the
tile is unchanged, `AiTurn` (`88c1989b` `src/IC2.Engine/Ai/AiTurn.cs:330–351`, T156) runs
`RunGarrisonFallback`, a march toward the capital (143,41). The army ends at **(146,44)**, 3 tiles
from the capital. The log line "garrison fallback moved army-8 to (143, 41)" names the target, not
the end tile.

The same happens to Media army 10 (307,58) → (309,60), Thracia army 6 (169,38) → (167,38),
Ptolemaic army 7 (191,95) → (192,97), Seleucid at Antioch (221,60) → (223,62), and Armenia army 1 at
Van (256,47) → (257,44) (`probes/carthage-rulebot1-40t-t36`: mercenary run, walk back to (256,47),
then the fallback toward (262,34)).

**Effect over a game:** in the free-running remake game these capital armies drift away from their
capitals (Rome game: Macedonia's army at (146,53) by turn 30, Media's at (283,58) by turn 40). The
original's armies stay put for 40 turns.

**Intake interpretation (code-backed, not hooked):** the original decides whether to run the
fallback with `FUN_0044aab4`, which returns `recomputedFullMoves != army[+6]`. That is, "did the
army spend moves", not "did the army change tile"
([`2026-10-07-strategic-ai-turn.md`](2026-10-07-strategic-ai-turn.md) §3.5). A swing that spends 7
of 9 moves and comes back counts as having moved, so `FUN_0044ebe8` does not run. The remake's T156
condition compares the tile before and after (`beforeTile.X == afterTile.X && …`), which treats the
same swing as "no movement". This matches every gap-A row: in each one, the walk spent moves and
returned. A hook at `0x44aab4` on `t01-a04` would confirm it.

## Gap B: the mercenary-run branch next to an enemy city besieges in the original and steps aside in the remake

**Original** (hook runs `t03-a03` and `t06-a03`, from the Rome game's saves before turns 4 and 7):

| Army | Inputs | Branch | End of the turn |
|---|---|---|---|
| Carthage army 2 at (37,62), Castulo (36,61) at war | city score 98, dist 1; army score −10000; supplies 141 > 21,878/500 | `e84c+city>85` (mercenary run) | stays at (37,62); Castulo loyalty 77 → 74; 21,878 → 20,732 troops |
| Seleucid army 5 at (178,41), Astacus (177,41) at war | city score 97, dist 1; supplies 474 > 11,224/500 | `e84c+city>85` | stays at (178,41); Astacus loyalty 52 → 50; 11,224 → 10,630 troops |

I re-derived the Carthage branch from the logged inputs with the hook's own `branch()` rules:
army score −10000 is ≤ 100, city score 98 is ≤ 100, 21,878 // 500 = 43 < 141 and the city is set,
so the resupply walk is skipped. Then army score ≤ 70 and city score 98 > 85 give `e84c+city>85`.

In the Rome game this repeats every turn: Castulo 80 → 77 → 74 → 71 (turns 3–5), Astacus 52 → 50
→ 48 → 46 → 44 (turns 7–10), the army losing 500–700 troops a turn, until the army is gone or the
score passes 100 (`city>100` attacks).

**Remake** (`probes/seleucid-siege-t08`, `probes/gaul-rulebot1-40t-t6`,
`probes/seleucid-rulebot1-40t-t8`): the same branch (`MercenaryRun`, city scores 94, 95, 88). No
mercenary offer is in reach, so the continuation `MarchAtCityTarget` adds a plain march at the city
(`88c1989b` `AiMilitaryPhase.cs:433–440`, "march at the enemy-city target"; I confirmed the
lines). The walker cannot enter the city and moves the army to another tile next to it: Astacus
(178,41) → (178,42), Synnada (186,44) → (187,44), Sidon (221,70) → (222,71), with 1, 9 and 3 moves
left. **No siege happens**: the city's loyalty and the army's troops do not change. With a city
score of 102 the tree selects `AttackCity` and the remake besieges like the original (Galatia–Cius,
Seleucid game turn 12).

## Gap C: AI fleets in their own port: a random hunt draw, plus one port tile (not a rule gap)

Fleet-phase hook (`patches/fleetphase_hook.py`, run `hooks-fleet-v1`; hooked and plain autosaves
byte-identical in all three runs):

| Start | Original (F608 inputs, end) | Remake (`aiprobe`, seeds 12345, 1–5) |
|---|---|---|
| Gaul game, before turn 31: Carthage fleet 0 at Utica (93,76) | hunt score **106** → hunts to (122,80) in the hooked run; **stayed** in port in the game itself | 116 at seed 12345; 82, 117, 127, 106, 90 at seeds 1–5 (hunt when > 100) |
| Gaul game, before turn 40: Carthage fleet 0 at Leptis Magna (111,93) | score **98** → port, stays | 107; 108, 107, 116, 91, 90 |
| Rome game, before turn 17: Ptolemaic fleet 1 at (189,93), port Alexandria | no route, hunt −10000 → port branch; stays at (189,93) | port branch; ends at (188,92) |

- **The hunt score is random in both games.** The original hunted from the same state in the hooked
  run but not in the game (a different random stream), and the remake's score ranges from 82 to
  127 over seeds. This is the first time the hunt branch and its `> 100` boundary are exercised.
  This corrects nothing, but it closes the "not exercised" line of
  [`2026-10-31-ai-fleets-vs-remake-main.md`](2026-10-31-ai-fleets-vs-remake-main.md), where every
  score was −10000.
- **Port tile (open, small):** for Ptolemaic fleet 1 next to Alexandria, both games choose the port
  branch. The original's fleet stays on its tile, while the remake's moves one tile, to (188,92).
  This accounts for 3 rows (Rome game turn 17, Carthage game turn 2, Seleucid game turn 20). The
  port pick is `FUN_0044e9a8`.

## Other results of the long runs

- **Registered difftests rechecked on `88c1989b`:** 113 unchanged, 11 FIXED (walk stops at own city
  on the line ×4, fleet second walk 87-47, move-far / move-sea refusals, walk-line-clear, storm30
  ×3, fleet-sail). The 11 REGRESSED all come from one random storm draw on the human fleet
  (condition 96 vs 97). Remake seeds 1–12 give both values on v0.9.0 and v0.8.4, so this is not a
  regression.
- **Free-running games** diverge from turn 1 (random draws). In the remake's Rome game, Seleucid
  takes all of Bithynia and Galatia by turn 20, while the original's Galatia survives with 9 cities.
  At turn 40 the remake has 20 armies against the original's 9. The anchored replays show equal
  army counts turn by turn, so the gap builds up through wars that went differently, not through a
  rule applied every turn.
- **Harness limit (conquest, open):** the Seleucid game stops at turn 26 in every run. A battle the
  human must defend leaves a dialog open that blocks File > Save, and the driver's battle flag
  `0x4A0B7C` reads 0. This is a driver limitation, not a game difference.

## Review at intake

- Remake source at `88c1989b` (local pin checkout): `AiTurn.cs:330–351` is the T156 fallback with
  the tile-equality condition. `AiMilitaryPhase.cs:433–440` is the `MarchAtCityTarget`
  continuation. Both are as cited.
- Hook logs: Macedonia army 8 `inputs` with `city = -1` and the `resupply` record
  (`t01-a04-decide.jsonl`). Carthage army 2's inputs are as tabled (`t03-a03-decide.jsonl`). The
  remake log has "garrison fallback moved army-8 to (143, 41)" and the same line for armies 6, 7
  and 10 (`capital-armies-t05/ailog.txt`).
- Inertness: in `SAVES.sha256`, the hooked and plain autosaves are identical for the three decide
  runs, and each fleet run's `inert.json` reports the same hash for both.
- Saves: the game saves are in release `run-exp-longrun-v090` (per-game tarballs, hashes in
  `SAVES.sha256`). The three **fleet-start saves** (`fleetstarts/*.SAV`) are hashed but are not
  among the release's seven assets, so gap C's original side is local to the bot's machine for now.
- I did not rerun Wine or the remake.

## What this does not establish

- Gap A's cause in the original is an interpretation from the decompile (`FUN_0044aab4`), not a
  hook result.
- Gap B: which original call turns the mercenary-run continuation into a siege, given that the army
  does not leave its tile (Carthage kept 9 moves). The outcome is measured; the mechanism is not.
- Gap C: whether the two games' hunt-score distributions match. That needs a seed sweep of
  `FUN_0044f4f8`. The cause of the Alexandria port-tile difference (`FUN_0044e9a8`) is also open.
- The unattributed structural rows (relations, captures, battles), and turns 26–40 of the Seleucid
  game.

## Data

[`runs/experiments/data/run-exp-longrun-v090/`](https://github.com/diegoami/ic2-conquest/tree/23aca35d/runs/experiments/data/run-exp-longrun-v090)
(anchored rows, probes, hook logs, `stays-v2.txt`, `SAVES.sha256`). Saves are in release
[`run-exp-longrun-v090`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-longrun-v090).
