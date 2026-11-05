# Faithful AI: a war declared in an AI seat mobilises in the same seat in the original, one round later in the remake (audit #195, X1)

**Tag:** [confirmed: decompile; anchored remake replays of stored original games]. Wine only for the original side (the
stored games). No new Wine run.
**Provenance:** draft from `diegoami/ic2-conquest`, `findings/2026-11-05-x1-war-before-economy.md` (PR #333, merge
`71b2e780`; follow-up PR #334, merge `0e8a4e69`). Remake pin `168dbc04` (v0.9.4). Ruleset `classical-faithful`, Instant battles (anchored replays).
**Task:** research #195, cross-cutting difference X1 (phase order) of the [inventory](2026-11-04-ai-audit195-inventory.md).
It had been confirmed in code on both sides but not measured. Written as a remake issue candidate.

## The two orders

- **Original:** `FUN_0044fa20` (the AI seat) runs `SetTurnTitle`, diplomacy `FB7C`, the economy `FFBC`, the armies
  `F31C`, then the fleets `F608`.
  - `FFBC` sums a **threat**: 15,000 per nation at war with the actor (relation 3), plus the enemies' armies and the
    near foreign and enemy armies.
  - It sums a **strength**: 6,000 per ally, plus its own armies and half of its allies' armies.
  - When strength < threat, it calls `FUN_004504f4(threat − strength)`, which mobilises ready recruits.
  - So a war that `FB7C` declares in the seat already counts in that seat's mobilisation.
- **Remake** (`src/IC2.Engine/Ai/AiTurn.cs` at `168dbc04`):
  - `AiFaithfulEconomy.Run` runs at line 150. Its threat is `FaithfulThreatPerEnemyNation × wars + …`
    (`AiFaithfulEconomy.cs:252`; the ruleset documents the value as the original's 15,000).
  - Capital defence follows (line 158), then the hire pass (line 187).
  - The war candidate comes only later, from `AiDiplomacyPhase.Propose` inside the scored loop (line 241).
  - So the economy sees a war declared in the seat only in the nation's next seat.

## Measurement

`x1_war_seats.py` scans the 19 stored games replayed on `168dbc04` (anchored, `--turn-seed`; the 898 turns of the
[v0.9.4 recheck](2026-11-04-remake-v094-recheck.md)):
- It finds **234 war starts in the AI phase**: 109 in the original only, 105 in the remake only. Wars are draws, and the
  turn seed is not the original's.
- **20 start in both games**: the same pair in the same seat. They come from 13 declarer seats, 11 of them distinct (the
  Rome 40-turn and 150-turn games repeat t26 and t29).
- Every declarer was at war with no one before.

`x1_mobilise.py` reads each declarer's ready recruits (recruit slots at state 24), treasury and mobilisation level
(`+0x442`) at three points: before the AI phase, at the original's end, and at the remake's end.

| game | turn | declarer | ready recruits: before → original / remake | position rows |
|---|---|---|---|---|
| rome-rulebot1-40t (and -150t) | 29 | Ptolemaic (war on Carthage, Numidia) | 46,300 → **24,900** / 46,300 | Ptolemaic armies, fleets |
| macedonia-rulebot1-40t | 27 | Seleucid (war on Armenia, Media) | 78,600 → **39,400** / 78,600 | Seleucid armies |
| armenia-rulebot1-40t | 36 | Ptolemaic | 46,300 → **24,900** / 46,300 | Ptolemaic armies, fleets |
| greece-rulebot1-40t | 8 | Carthage | 4,200 → **3,000** / 4,200 | none |
| gaul-rulebot1-40t | 7 | Carthage | 0 → **3,000** / 4,200 | none |

**What it moves, Rome t29 (Ptolemaic):**
- Five ready slots are mobilised: hc 900, hi 5,000 and li 7,500 at the capital (190,94), and hc 2,200 and lc 5,800 at city
  267 (223,88).
- The capital's three slots join the main army, which grows from 64,030 to 77,430 at (192,94). City 267's two form a new
  8,000-man army at (223,89).
- In the remake, the main army stays at 64,030 and there is no second army.

Macedonia t27 (Seleucid) is the same pattern: 16,200 men join the main army at (211,45), and a new 23,000-man army appears
at (188,59), from city 206. These seats' position rows were unattributed until now. They are now attributed to X1.

## Expected, actual, fix

- **Expected (original):** the AI economy's threat includes wars declared earlier in the same seat. The nation mobilises
  in the seat where it declares war.
- **Actual (remake):** the economy runs before the war candidate is chosen, so mobilisation waits one round.
- **Candidate fix:** in Faithful, run the nation's own diplomacy decision as a phase before `AiFaithfulEconomy.Run`, as
  FA20 does. A narrower alternative: re-run the Faithful economy after a war is declared in the seat.

## Scope and open

- **Only the economy consequence is measured.** The inventory lists three other consequences of the same order, all
  unmeasured: the capital-defence radius (19 at war, 9 otherwise), the hire gate ("at war with someone") and the busy
  test. In the remake, capital defence runs before the loop (line 158). In the original it runs at F31C entry, after
  FB7C.
- **Not traced:** the Ptolemaic fleet row, (218,85) in the original against (192,93) in the remake.
- **Not re-read at intake:** where in FB7C the relation is set to 3. The phase order itself was confirmed earlier
  (research PR #156) and re-read here.

## Intake verification (research, 2026-11-05)

**Checked:**
- **The decompile** (`all_app_functions.txt`, sha256 `2018c205…`):
  - `FUN_0044fa20` calls `FB7C` before `FFBC` (lines 53217–53218).
  - `FUN_0044ffbc` adds 15,000 per relation-3 nation and 6,000 per ally. Under `if (local_1c < local_18)` it calls
    `FUN_004504f4(local_18 - local_1c)`.
- **The remake at `168dbc04`:** `AiTurn.cs` lines 150, 158, 187 and 241, `AiDiplomacyPhase.Propose` inside the loop, and
  `AiFaithfulEconomy.cs:252`.
- **`war_seats.jsonl`:** 234 rows, with 109 / 105 / 20 as stated.
- **`mobilise.jsonl`:** 13 rows, which are 11 distinct seats. Every `wars_before` is empty. The rows for Rome t29,
  Macedonia t27, Armenia t36 and Greece t8 are as tabled.

**Narrowed: the draft's count understates the effect.** The draft says that "the 7 other seats [are] equal in both
games". That holds for ready recruits in only 6 of them:
- **Gaul t7, Carthage** repeats the Greece t8 pattern. Ready recruits end at 3,000 in the original and 4,200 in the remake,
  and the mobilisation level ends at 13 against 12.
- **The mobilisation level, by seat:** the original ends higher than the remake in 8 of the 11 seats and equal in 3
  (Rome t26, Gaul t31, Numidia t30). It is never lower.

  | seat | before | original | remake |
  |---|---|---|---|
  | Rome t29 | 9 | 12 | 9 |
  | Gaul t7 | 12 | 13 | 12 |
  | Macedonia t12 | 12 | 13 | 9 |
  | Macedonia t27 | 15 | 16 | 15 |
  | Greece t8 | 12 | 14 | 12 |
  | Armenia t36 | 6 | 6 | 3 |
  | Media t1 | 0 | 13 | 0, with Greece's treasury 920 → −134 in the original against 948 |
  | Media t5 | 15 | 17 | 15 |

  This is consistent with X1 and with "no seat shows the reverse". But the level has other writers too: recruit orders,
  and the quarterly decay of 3. So only the three decomposed seats are attributed here. The other five are candidates.

**Not checked:** the two scripts, and the per-slot decomposition of Rome t29 and Macedonia t27.

## Follow-up: all 11 seats decomposed (conquest PR #334)

Asked at intake, the peer decomposed each same-war seat. `x1_decompose.py` matches recruit slots as a (type, troops,
city) multiset (`decompose.jsonl`, 13 rows).

**The gap call.** `FUN_004504f4(gap)` has two parts:
- **(a) Mobilise:** it mobilises ready slots (state 24) through `FUN_0044a4e0`. It does this only if one of its own
  armies is within 6 tiles of the slot's city, or if there are at least 4 ready slots.
- **(b) Raise:** it raises up to 8 new slots through `FUN_004501f4`, while the recruits are below the gap and the
  mobilisation level (`+0x442`) is below 100. Raising costs treasury and adds `troops × 1000 / wealth + 1` to the level.

**Its callers** (decompile, checked at intake):
- `FUN_004501f4` is called only from `FUN_004504f4`.
- `FUN_004504f4` is called only from `FFBC`.
- `FUN_0044a4e0` is called from `FUN_004504f4` and from `TArmyRecruits_MobilizeUnits`, the human's dialog.

So in an AI seat, any mobilise or raise is FFBC's gap call.

**Per seat (original; the remake does neither in any of the 11):**

| seat | declarer | (a) mobilised | (b) raised | level |
|---|---|---|---|---|
| Rome t29 | Ptolemaic | 5 slots, 21,400 | hc 2,100, lc 6,700, li 9,100 at 214 | 9 → 12 |
| Armenia t36 | Ptolemaic | the same 5 | hi 4,500, lc 7,000, li 5,100 at 214 | 6 → 6 (remake 3) |
| Macedonia t27 | Seleucid | 8 slots, 39,200 | ar 2,900 at 292 | 15 → 16 |
| Greece t8 | Carthage | hc 1,200 at 72 | lc 7,000 at 70 | 12 → 14 |
| Gaul t7 | Carthage | — | hi 4,200 at 70 | 12 → 13 |
| Macedonia t12 | Carthage | — | ar 2,000, li 11,000 at 72 | 12 → 13 (remake 9) |
| Media t5 | Carthage | — | hi 6,000 at 70 | 15 → 17 |
| Media t1 | Greece | — | 5 slots at 166 (hi 2,600 / 2,800 / 3,900, li 6,300 / 10,000) | 0 → 13; treasury 920 → −134 |
| Rome t26, Gaul t31, Numidia t30 | Armenia, Seleucid, Macedonia | — | — | neither game |

**Result: the original runs the gap call in 8 of the 11 seats, the remake in none.** All 5 intake candidates are the gap
call. Only the three seats with mobilised slots that formed or joined armies have position rows. The other five raised
recruits, not armies.

**Stated assumption (inference):** the war-free threat is equal in both games. They share the start state, and the
remake never runs its gap call in these seats. So the same-seat war is what tips the original over.

**Checked at intake (2026-11-05):**
- **The decompile:** the callers above; and in `FUN_004504f4`, the `< 6` distance and `< 4` ready-slot gates, the
  `< 8` raise loop, the level `< 100` test, and the `× 1000` level term.
- **`decompose.jsonl`:** all 13 rows, against the table.
  - The Rome t29 mobilised slots sum to 21,400, which is 46,300 − 24,900.
  - Armenia t36's flat level fits the quarterly −3 decay: the remake shows the decay alone.

This supersedes the "8 of 11 by the mobilisation level; candidates" narrowing above. It is now decomposed: 8 of 11, all
the gap call.

**Not checked:** `x1_decompose.py`; the treasury gate in the raise loop; whether the remake's own Faithful gap path
matches parts (a) and (b) once a war is counted.

## Evidence

- `runs/experiments/data/run-exp-audit195/x1-war-seats-v1/` (conquest): `war_seats.jsonl` (234 rows) and
  `mobilise.jsonl` (13 rows).
- Original games: releases `run-exp-longrun-v090` (`rome-rulebot1-40t-saves.tar.gz`), `run-exp-longrun-v091`
  (`macedonia-…`), `run-exp-longrun-v092` (`greece-…`) and `run-exp-longrun-v093` (`armenia-…`). Seats: `t29-a00.SAV` →
  `t29-a01.SAV` (Rome), `t26-a01.SAV` → `t27-a00.SAV` (Macedonia).
- Remake replays: release `run-exp-longrun-v093`, `recheck-168dbc04-anchored-saves.tar.gz`.
- Tooling: `runs/experiments/audit195/x1_war_seats.py`, `x1_mobilise.py`.
