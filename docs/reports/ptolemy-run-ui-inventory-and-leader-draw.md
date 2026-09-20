# The UI inventory, the leader draw, and a complete battle resolution

**Evidence class: automated dialog scan over 22 recordings, plus frames read against the saves and
against a second play-through, 2026-09-20.** Pass A of the
[`run-1-ptolemy`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-ptolemy) sweep.
Coverage and what remains: [`recording-ledger.md`](../recording-ledger.md).

## 1. What a turn's UI actually consists of

All 22 recordings were scanned for frames containing a dialog — the game map is saturated green, blue
and yellow, a Windows dialog is bright and near-grey, so the fraction of grey pixels inside the map
viewport detects one reliably. 118 dialog-bearing frames reduced, by perceptual hash, to **62 distinct
screens**.

Twelve distinct screen types account for all of them:

| Screen | What it carries |
|---|---|
| Nation panel | leader, capital, cities, population, unity **as a word**, tax %, mobilized %, treasury, and a per-nation international-relations list |
| News log | cumulative event history — see [`ptolemy-run-news-log-vocabulary-verified.md`](ptolemy-run-news-log-vocabulary-verified.md) |
| Army recruits | the recruitment table with readiness **as words**, initial and quarterly cost, `Recruit unit` / `Mobilize` / `Disband` |
| Own-army information | moves, supply, morale, money, terrain, and per-type troop counts |
| **Foreign-army information** | per-type troop counts and terrain — **moves, supply, morale and money are blank** |
| Battle resolution | §3 |
| Two-army transfer | both armies' unit lists, plus supply and money spinners |
| Change tax level | current/new tax beside current/new income, over a slider |
| Supply purchase entry | quantity spinners |
| Human and computer leaders | §2 |
| Game-start unit placement | a unit palette and *"&lt;Nation&gt; to place units"* |
| Save As / Open | OS file chrome, not game UI |

**The foreign-army panel is a fog-of-war rule** `[derived]`: composition and terrain are visible for
an enemy army while moves, supply, morale and money are withheld. Read from one frame
(`IP1 021` t=140, `Army of Seleucid`, 57,733 troops itemised, `Terrain: Mountains`, the other four
rows empty). It is `[derived]` rather than `[confirmed]` because **no frame of an *owned* army was read
at full resolution in the same pass**, so "blank because withheld" has not been separated from "blank
because zero". That comparison is one frame away and should be the first thing done next.

## 2. Leader names are drawn per game — do not treat them as data `[confirmed]`

The New Game screen lists every nation with a `human` checkbox and an **editable** leader name. From
`IP1 000` t=12:

| Nation | Leader | | Nation | Leader |
|---|---|---|---|---|
| Rome | Publius Scipio | | Celtiberia | Sergius |
| Carthage | Hanno | | Illyria | Kallinos |
| Seleucid | Sennacherib | | Dacia | Stilicho |
| **Ptolemaic** ☑ | **Cleopatra** | | Bithynia | Stesichorus |
| Macedonia | Demetrius Poliorcetes | | Galatia | Thrasamunde |
| Numidia | Megabyzus | | Armenia | Nabopolassar |
| Gaul | Caractacus | | Media | Samsuiluna |
| Greece | Pericles | | Thracia | Xenophon |

**This roster is not canonical.** The same four nations in `1_rome_270_winter_3.sav` and
`_winter_11.sav`, a different play-through of the same scenario, carry entirely different names:

| Nation | `run-1-ptolemy` | `run-1-rome` |
|---|---|---|
| Rome | Publius Scipio | Licinus Crassus |
| Ptolemaic | Cleopatra | Ptolemy Euergetes |
| Seleucid | Sennacherib | Darius |
| Gaul | Caractacus | Arminius |

Four for four different. **Leader names are drawn at New Game**, exactly as the build repo's exported
world already says with `leaderName: "(unassigned -- drawn at New Game)"`. That placeholder is correct
and must stay; transcribing the table above into the export would have been a straightforward defect,
and it is recorded here so that nobody does it later.

**The pool is nation-specific, not global** `[derived]`. Ptolemaic drew Cleopatra and Ptolemy
Euergetes; Rome drew Publius Scipio and Licinus Crassus; Gaul drew Caractacus and Arminius. Eight
observations, every one consistent with its nation's history and none appearing under a second nation.
Two draws per nation cannot size a pool or prove exclusivity, so this stays `[derived]`; the DAT
presumably holds the table, and that is where it should be settled.

Two smaller `[confirmed]` points from the same screen: the **`human` flag is per nation**, so several
human seats are selectable — which is what the scenario schema's `blindHotseat` is for — and leader
names are **editable text fields**, so a player can override the draw.

## 3. A complete battle resolution `[confirmed]`

`IP1 000` t=25. **Seleucid's army defeats Ptolemaic's army.**

| | Seleucid start | Seleucid finish | Ptolemaic start | Ptolemaic finish |
|---|---|---|---|---|
| light infantry | 27,300 | 17,025 | 21,300 | 0 |
| heavy infantry | 8,400 | 5,916 | 3,200 | 0 |
| archers | 5,200 | **0** | 0 | 0 |
| light cavalry | 1,800 | 1,452 | 2,300 | 0 |
| heavy cavalry | 2,400 | 2,303 | 900 | 0 |
| **total troops** | **45,100** | **26,696** | **27,700** | **0** |

> The army of Seleucid captured 100 talents.
> The army of Seleucid captured 158 tons of supplies.

The loser is annihilated in every category. The winner's losses are **not uniform**, and the ordering
is the interesting part:

| Type | Lost | Rate |
|---|---|---|
| archers | 5,200 | **100%** |
| light infantry | 10,275 | 37.6% |
| heavy infantry | 2,484 | 29.6% |
| light cavalry | 348 | 19.3% |
| heavy cavalry | 97 | **4.0%** |

A strict ordering — archers, then light infantry, heavy infantry, light cavalry, heavy cavalry — with
**cavalry losing an order of magnitude less than infantry**, and archers eliminated outright while
heavy cavalry lost 4%. The winner still lost **40.8%** of its strength against an enemy 61% its size.

This is one battle, so the ordering is an observation about this engagement, not a coefficient.
It is recorded here as a **check against**
[`decompiled-combat-formula-structure.md`](decompiled-combat-formula-structure.md) and
[`combat-type-effectiveness-matrix.md`](combat-type-effectiveness-matrix.md) rather than as new
theory — those reports derive the structure, and this frame is a fully specified instance to test any
implementation against. **Whether the merged combat code reproduces these six numbers from these six
inputs is a question worth asking directly**, and it has not been asked here.

Also `[confirmed]`: a victorious army **captures the loser's talents and supplies**, reported as two
separate sentences with explicit amounts.

## 4. What this pass did not do

- **~25 single-occurrence screens in `IP1 016`, `IP1 019` and `IP1 021` are unread.** Runs of
  consecutive distinct frames usually mean animation; more battles are the likeliest content.
- **The two-army transfer dialog was surveyed, not transcribed** — it is the highest-value unread
  screen, and the direct UI for T15's join/split/transfer.
- The supply purchase dialog is unread.
- No frame of an **owned** army was read at full resolution, which is what §1's fog-of-war reading
  needs to become `[confirmed]`.
