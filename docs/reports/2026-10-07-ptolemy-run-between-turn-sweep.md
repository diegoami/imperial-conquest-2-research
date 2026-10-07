# The run-1-ptolemy between-turn sweep: a year dated, and four mechanisms confirmed in play

**Evidence class: 44 consecutive save diffs over all 45 `IP0*.sav` of
[run-1-ptolemy](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-ptolemy), read
2026-10-07 with `IC2.Inspect --compare-saves` / `--to-json`.** The written note
`notes/1_ptolemy.txt` ("Play-through 1, Ptolomeans, year 271. Complete playthrough…") is the intake
trigger; no video was opened for this report, so no recording is cited. Earlier passes over this run
read two recordings deeply and compared exactly one save pair of each kind
([`ptolemy-run-readiness-ladder-and-mobilization-rate-confirmed.md`](ptolemy-run-readiness-ladder-and-mobilization-rate-confirmed.md),
[`recording-ledger.md`](../recording-ledger.md)); this pass diffs the whole chain, which no earlier
report does.

## 0. Corrections to the record, from the note and the saves

- **The note's "year 271" is wrong; the run is entirely 270 BC.** `IP000.sav` reads Week 1 Spring
  270 BC and `IP021B.sav` Week 7 Winter 270 BC (`--inspect-turn`, all 45 files). The note's
  `IP1.xxx.mp4` pattern is also `IP1 NNN.mp4` — a space, not a dot — as the evidence directory
  already shows.
- **The recording ledger's claim "Ptolemaic besieged nothing across the whole of 270 BC" is
  false.** §2: the player assaulted eight Seleucid cities and received three more by cascade, all
  inside their own turns. The shopping-list item "a siege, fought and resolved… no other run holds
  one either" should stop citing this run's lack; the ledger has been amended.
- **Turn 4 (Week 9 Spring) has no `B` save** — `IP004.sav` only — so that turn's player orders are
  inside the `IP004 → IP005` diff. The `C`/`D` files (`IP002C`, `IP007C`, `IP007D`) are repeated
  end-of-turn saves: `IP007C → IP007D` changes no field the parser carries and differs only in
  bytes it does not decode (first difference at file offset 57034).

**Corpus and seating.** 22 turns, weeks 1–11 of each season at two weeks per turn, Spring through
Winter 270 BC. The player is Ptolemaic, seat **13** of the shuffled order in the save tail
(`13 10 14 4 8 12 1 9 0 5 15 2 7 3 6 11`, already recovered in
[2026-10-03-new-game-turn-order-shuffle.md](2026-10-03-new-game-turn-order-shuffle.md)); **only Gaul
(seat 14) and Bithynia (seat 15) act after the player**, which §4 turns into a measurement. A
between-turn diff `IPnnnB → IPnnn+1` therefore contains Gaul's and Bithynia's week-*W* AI turns,
the weekly (and at week 11, quarterly) tick, and the other thirteen nations' week-*W+2* AI turns.

## 1. The year, dated

The news-log frames ([`ptolemy-run-news-log-vocabulary-verified.md`](ptolemy-run-news-log-vocabulary-verified.md))
carry the sentences but no dates; the diffs date every one of them. Week = the player's turn the
diff opens on.

| Diff into | Week | Event, from the save diff alone |
| --- | --- | --- |
| `IP001` | W3 Sp | **Seleucid takes Sidon** from Ptolemaic (pop 50→43); Rome destroys Gaul's army (40,500; unity ±25); Carthage destroys Celtiberia's army (33,900; ±25) |
| `IP003` | W7 Sp | Seleucid–Galatia battle (unity ±25); the 19,300-troop Galatian army's record only clears one diff later, unexplained |
| `IP004` | W9 Sp | Seleucid takes Synnada from Galatia |
| `IP005` | W11 Sp | **Rome takes Brixia; Modena defects** (see §3); Seleucid takes Acroinon |
| `IP006` | W1 Su | Quarterly tick (Ptolemaic +1,679 net); Rome takes Verona; Greece's 71-ship Athens fleet has countdown 22 |
| `IP007` | W3 Su | Seleucid–Bithynia battle: a Seleucid army (21,899) destroyed, Bithynia −8,381, unity ±25 |
| `IP008` | W5 Su | Rome takes Altinum |
| `IP010` | W9 Su | **Seleucid takes Samaria; Jerusalem and Damascus cascade to Seleucid** (§3) |
| `IP011` | W11 Su | AI tax week (§4) |
| `IP011B`→`IP012` | tick | **Gaul deposes Caractacus** (debt; §6); Seleucid, army-less, raises two armies totalling 55,800 in one turn (§5) |
| `IP012B` | W1 Au | Player takes Jerusalem; raises a 62,500-troop army at the Nile delta (§5); merges the 5-ship fleet into the 65-ship fleet (65+5=70) |
| `IP013` | W3 Au | Galatia retakes Synnada; Seleucid +47,143 troops in one between-turn (§5) |
| `IP014` | W5 Au | Galatia's rebuilt army (55,012) destroyed again |
| `IP016` | W9 Au | Rome takes Taurasia; Gaul's army (71,400) destroyed |
| `IP017` | W11 Au | Rome takes Axima; AI tax week |
| `IP018` | W1 Wi | Tick: **Celtiberia deposes Sergius** (§6); Numidia orders a 58-ship fleet at Siga; Greece's fleet launches |
| `IP019` | W3 Wi | **Macedonia takes Phoenice** — after two failed attempts (§2.3) |
| `IP021` | W7 Wi | Rome takes Vindonissa |

Player-turn events (the `B` diffs) are in §2. Rome's northern war on Gaul runs all year: Brixia,
Modena, Verona, Altinum, Veldidena (W9 Su), Taurasia, Axima, Vindonissa — Gaul ends at 20 cities,
Rome at 33. The war declaration `CARTHAGE DECLARES WAR ON PTOLEMAIC.` cannot be dated from these
saves: the JSON dump carries no relations field, and no Carthage–Ptolemaic military contact ever
appears in the diffs.

## 2. The player's Levant campaign — eight assaults, three cascades `[confirmed]`

All in the player's own turns (`IPnnn → IPnnnB`), all against Seleucid, whose field army the player
annihilated in Week 11 Summer (§7). Pop = population thousands before → after; "floor" marks a drop
that sits exactly on the `× 3/4` clamp of `FUN_0044b230`.

| Turn | City | Pop | Loyalty lands | Seleucid unity |
| --- | --- | --- | ---: | --- |
| W1 Au `IP012B` | **Jerusalem** assaulted | 80→60 floor | 90 | 716→701 (−15) |
| W3 Au `IP013B` | **Samaria** assaulted | 35→26 floor | 90 | 701→686 (−15) |
| W11 Au `IP017B` | **Sidon** assaulted | 50→42 (r≈0.84) | 40 | 671→656 (−15) |
| W1 Wi `IP018B` | **Byblos** assaulted | 84→63 floor | 55 | 652→637 (−15) |
| W1 Wi `IP018B` | **Aradus** cascaded | 50→50 | 50 | 637→… |
| W1 Wi `IP018B` | **Hemesa** cascaded | 72→72 | 50 | …→597 (−20−20) |
| W3 Wi `IP019B` | **Damascus** assaulted | 138→103 floor | 40 | 597→582 (−15) |
| W3 Wi `IP019B` | **Palmyra** cascaded | 102→102 | 50 | 582→562 (−20) |
| W7 Wi `IP021B` | **Thapsacus** assaulted | 80→60 floor | 40 | 562→547 (−15) |

And the mirror event, Week 9 Summer (`IP009 → IP010`), when Seleucid's AI took three Ptolemaic
cities in one turn: **Samaria assaulted** (43→32, floor; Ptolemaic unity 661→646, −15) and
**Jerusalem (80→80) and Damascus (131→131) cascaded** to Seleucid (646→606, −20 −20).

### 2.1 The unity arithmetic is exact `[confirmed]`

Every winner/loser unity delta across all eleven events reproduces the decompiled rules — capture
`−15` ([decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md) :50182), defection
`−20` ([decompiled-defection-and-siege-attrition.md](decompiled-defection-and-siege-attrition.md))
— with **zero residual**, e.g. Ptolemaic 661−15−20−20 = 606 (observed 606) and Seleucid
652−15−20−20 = 597 (observed 597).

### 2.2 The cascade gates, including two negative controls `[confirmed]`

`FUN_0044ba1c`'s gates (loser unity < 650 read **after** the capture's −15; distance < 10 from the
attacking army; loyalty < 65; not a capital) decide exactly which neighbours flip:

- **Gate closed, correctly:** after Sidon (W11 Au) the loser sits at 656 — nothing cascades. After
  Jerusalem (W1 Au) 701, after Samaria (W3 Au) 686 — nothing.
- **Gate open, members correct:** after Byblos (637) — Aradus (Chebyshev 3, loyalty 60) and Hemesa
  (4, 62) flip; after Damascus (582) — Palmyra (7, 60) flips. **Thapsacus (loyalty 84 ≥ 65) stays**
  and has to be assaulted two turns later; in the Seleucid mirror, Samaria (distance 10, not < 10)
  likewise does not cascade when Jerusalem falls.
- **The ÷3 sympathy branch** ([decompiled-defection-and-siege-attrition.md](decompiled-defection-and-siege-attrition.md)):
  Damascus's allegiance was already Seleucid while Ptolemaic-owned, so when Seleucid took Samaria,
  Damascus's cascade defence was divided by three — the branch doing visible work.
- **Loyalty landings match the formulas**: allegiant recapture `min(90, 140−L)` gives Jerusalem and
  Samaria 90; non-allegiant assault floors at 40; cascade cities land on 50; Byblos's 55 is a
  `min(65, max(50, 100−L))` mid-value.

What is new against the eight run-1-rome instances (which included Modena cascading **to** the
human Rome) is the direction reversed: here the human's own cities cascade **away** (Jerusalem and
Damascus to Seleucid), and the ÷3 sympathy branch is seen working for and against the same player
within one run.

### 2.3 The erosion formula, and the failed attempts `[confirmed]`

`FUN_0044b230` = `field = max(field×3/4, min(field×19/20 + 1, field×def/atk))` on loyalty,
fortification, population, per attack attempt. In these saves:

- **Six assaults sit exactly on the ×3/4 floor** (Jerusalem, Samaria, Byblos, Damascus, Thapsacus,
  and Seleucid's Samaria), fortification included (Brixia 37→27, Verona 45→33, Altinum 21→15).
- **Sidon's −16%** (50→42) and Rome's Axima (15→14), Vindonissa (19→18) are mid-window values,
  i.e. `def/atk` between 3/4 and 19/20.
- **Failed attempts erode — first save-pair confirmation** of the claim settled from code but
  "checked by no save pair" ([decompiled-defection-and-siege-attrition.md](decompiled-defection-and-siege-attrition.md)
  open list): **Phoenice**, besieged by Macedonia across the autumn, shows fort 44→42→40 and loyalty
  77→74→71 over the `IP012 → IP015 → IP016` diffs while its population (19) stays pinned — each
  step is exactly `field×19/20 + 1` in integer arithmetic (`(44×19)/20+1 = 42`, `(77×19)/20+1 = 74`,
  `(19×19)/20+1 = 19`). It falls at W3 Wi (`IP019`) with pop 19→18.
- **A ±1 wobble in the mid-window cases**: Verona (pop −4 fits `r≈0.79` but fort −12 is the floor),
  Veldidena and Vindonissa each admit no single `r` that reproduces both fields exactly. Either the
  ratio is recomputed between attempts of the same turn (attacker casualties in `FUN_0044ae20`
  change it), or the division semantics of `FUN_0044b230` are not what the pseudocode assumes. A
  re-read of the machine code at `0x0044B230` against these three cities would settle it; this
  report does not.

## 3. Modena, dated and explained

`Modena defects from Gaul to Rome.` (W11 Sp, `IP004 → IP005`) is the cascade working for Rome:
Brixia assaulted (18→13 floor), Gaul 552−15 = 537 < 650 → gate open, Modena (pop 20→20, loyalty to
50) flips, Gaul unity 552→517 = −15−20 exact. The mechanism the defection report proposed for
"defects from" sentences is now observed on both sides of the human/AI line.

## 4. The AI tax policy, week 11 only — fifteen changes, all matching `[confirmed]`

[2026-10-07-strategic-ai-turn.md](2026-10-07-strategic-ai-turn.md) §2.3 derives, from code only:

```text
if (unity < 650 or treasury > wealth/2000):  tax = max(5, tax − 6)
if (treasury < 0 or (own ≤ threat and treasury < 1000)):  tax = min(40, tax + 9)
if (treasury > 0 and unity < 500):  tax = 0
```

The run supplies **fifteen** in-play evaluations (all pre-change state readable in the saves), and
every one matches, including the interesting cases:

| Nation, quarter | Change | Reading |
| --- | --- | --- |
| Rome, Sp→Su | 10→5 | cut clamped at the `max(5, …)` floor |
| Gaul, Sp→Su | 10→14 | **cut then raise in one evaluation** (10−6→5, +9→14) |
| Gaul, Su→Au | 14→17 | cut then raise again (14−6→8, +9→17) |
| Greece, Su→Au | 14→8 | cut alone |
| Greece, Au→Wi | 8→14 | cut clamped (8−6→5) then raise |
| Galatia, Au→Wi | 32→35 | cut then raise |
| Celtiberia, Au→Wi | 33→40 | raise clamped at the `min(40, …)` ceiling |
| Bithynia, all three quarters | 12→21→30→39 | raise (in deficit every quarter) |
| Seleucid, Sp→Su→Au→Wi | 18→27→36→40 | monotone climb from deficit, ceiling at 40 |

Carthage never moves (already at 5, nothing raises it); Macedonia, Media, Numidia, Thracia never
meet a condition. **The seat order is the tell**: week-11 changes for the thirteen nations seated
before the player land in the `IPnnn → IPnnn+1` diff *into* week 11, while **Gaul's and Bithynia's
— the only two seats after the player — land one diff later, in the quarter-boundary diff**,
because their week-11 AI turns run after the player's save. The observed split is exactly
{Bithynia, Gaul} versus everyone else.

## 5. Rearmament and army management at scale `[confirmed]`

- **An annihilated AI rebuilds immediately.** Seleucid's last field army (43,293) dies to the player
  in W11 Su; the next between-turn (`IP011B → IP012`) shows **two new armies, 55,800 troops, all
  regular**, in Cilicia (206,58) and Anatolia (188,59). The turn after: +47,143 more, including
  8,343 mercenaries hired into army 12. The §2.2/§3.2 gates of the AI turn
  ([2026-10-07-strategic-ai-turn.md](2026-10-07-strategic-ai-turn.md)) are seen operating at a
  wealth scale no earlier corpus reached.
- **The human can do the same: a 62,500-troop army appears in one player turn** (`IP012B`, at
  (191,95) in the Nile delta beside Alexandria — the city whose garrison line held 98,900
  city-unit troops in the readiness report), then is split into two ~30,000 armies the following
  turn (`IP013B`). All-eleven units regular; treasury moves only −594 that turn, so this is
  mobilization, not recruitment.
- **One merge per turn, for human and AI alike**: the player's 900-troop army 5 is absorbed the
  same turn the delta army appears; the player's 5-ship fleet joins the 65-ship fleet exactly
  (65+5 = 70 ships at `IP012B`); Seleucid's army count falls 4→3 with no troop loss in `IP017`
  (AI merge).
- **Fleet construction counts down in weeks**: the player's 30-ship Alexandria order (`IP007C`,
  treasury −300 = 30 × 10 talents, the `TBuildFleet` cost confirmed as charged) runs countdown
  24→18→14→4→2 at one per week; Greece's 71-ship Athens fleet, countdown 22 at `IP007B`, launches
  at the Autumn→Winter tick — dating the `Greece finishes a new fleet at Athens` news line to W1 Wi.

## 6. Two more AI depositions, both debt, both at quarter ticks `[confirmed]`

The rule ([upkeep-payment-and-desertion.md](upkeep-payment-and-desertion.md): `Random(9)==0` and
in debt, at the quarterly update) already had two in-play instances from run-1-rome. This run adds
two, with the same arithmetic: **Gaul** at the Summer→Autumn tick (`IP011B → IP012`: −3,993 → 0,
Caractacus → Arminius, unity 473 → 550 = `max(unity, min(550, unity+150))`) and **Celtiberia** at
the Autumn→Winter tick (`IP017B → IP018`: −2,619 → 0, Sergius → Gelo, unity 684 unchanged by the
reset and only −7 ordinary drift — the `max()` leaving a high unity alone, as with run-1-rome's
Galatia 698). Bithynia, Galatia and Seleucid are in debt at the same ticks and are *not* deposed —
the one-in-nine gate failing, as expected.

## 7. Two battles the recording scan never read `[confirmed]`

The ledger's dialog detector found no second battle in the recordings; the saves hold two, both
fought by the player, both army annihilations, both with the winner/loser unity swing **±25**
already established in [`2026-10-04-battle-probe.md`](2026-10-04-battle-probe.md):

- **W11 Summer** (`IP011 → IP011B`): Seleucid army 4 at (222,88), 43,293 troops (11,315 of them
  mercenaries), annihilated. Ptolemaic −13,156: light infantry 57,600→52,259, heavy infantry
  19,488→15,579, archers 3,200→1,271, **light cavalry 1,700→0**, heavy cavalry 3,800→3,523.
  Unity Ptolemaic 606→631, Seleucid 740→715.
- **W9 Autumn** (`IP016 → IP016B`): Seleucid army 13 at (222,69), 20,300 troops, annihilated for
  −2,600 Ptolemaic losses. Unity 658→683 / 696→671.

Two more AI-vs-AI ±25 pairs sit in the chain (Rome/Gaul and Carthage/Celtiberia at W3 Spring,
Bithynia/Seleucid at W3 Summer). One Galatian sequence does not align — the ±25 lands one diff
before the army record clears (§1) — recorded, not resolved. **Methodological point for the
ledger: a save pair is a battle index; `IP1 016`'s frames were map panning, but `IP016/IP016B`
hold the battle.**

Smaller observations from the same sweep, all `[confirmed]` as values, none explained here: the
player's quarterly treasury nets at the three ticks are **+1,679 (tax 21, 45 cities), +1,662 (tax
22, 42), +1,047 (tax 22, 45)** — the winter dip coincides with the army having doubled to ~129,000
troops and three fleets, i.e. the derived upkeep terms, but the decomposition is not attempted;
Alexandria's city supplies fall 969→489 over the player's first turn (already noted unexplained in
the readiness report, still unexplained); army annihilation by battle is worth ±25 unity to both
sides in every clean instance.

## What this does not establish

- **The exact division semantics of `FUN_0044b230`** in its mid-window (the ±1 wobble of §2.3);
  needs the machine code re-read against Verona/Veldidena/Vindonissa.
- **The defence-side strength magnitudes** of the cascade gate (`otherDefense < attackerStrength`):
  the unity/distance/loyalty/allegiance gates are confirmed, but no absolute strength was
  recomputed from these saves.
- **Dating the Carthage→Ptolemaic war declaration** (no relations field in the dump).
- **The quarterly income decomposition** (§7's nets); the formula's other terms are derived in
  [upkeep-payment-and-desertion.md](upkeep-payment-and-desertion.md) and were not re-verified here.
- **What the between-turn diffs of the player's own supply purchases did** (the −200 at `IP002C`
  is undated by any dialog); no recording was opened to check.

## Reproduction

```bash
INS=../imperial_conquest_2/src/IC2.Inspect/bin/Debug/net10.0/IC2.Inspect.exe
CFG=../imperial_conquest_2/assets.local.ini
S=~/Documents/imp_conq_original/saves
for f in IP000 IP000B IP001 … IP021B; do
  "$INS" --config "$CFG" --to-json "$S/$f.sav" "$f.json"   # then diff the JSONs in save order
done
"$INS" --config "$CFG" --compare-saves "$S/IP000.sav" "$S/IP000B.sav"
```

Save order within a turn is `n, nB, nC, nD`; turn 4 has no `B`. All 45 saves are cited by this
report and have been moved to `saves-processed/`. The note `notes/1_ptolemy.txt` stays untouched.
