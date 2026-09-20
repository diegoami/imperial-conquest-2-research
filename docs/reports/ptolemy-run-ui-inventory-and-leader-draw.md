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

**The foreign-army panel is a fog-of-war rule** — composition and terrain are visible for an enemy
army while moves, supply, morale and money are withheld (`IP1 021` t=140, `Army of Seleucid`, 57,733
troops itemised, `Terrain: Mountains`, the other four rows empty). Confirmed against an owned army in
§5.

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

## 4. The army command surface, and the Split army dialog `[confirmed]`

`IP1 021` t=80 has the `Unit map` menu open. The command surface is exhaustive and small:

```
Unit map
  Army  >  Supply army · Recruit mercenaries · Transfer unit ·
           Split army · Join armies · Change units · Disband army
  Fleet >
  City  >
  Cancel selection                                     Shift+X
```

Six seconds later, `t=86`, the **Split army** dialog. Two unit lists side by side, `Transfer` and
`Disband` under each, a running `15 units   69,491 troops` total, and — separately from the units —
**supply and money split by explicit spinners**, `10s` and `100s`, from first army to second:

```
First army's supply   524     10s [±]  100s [±]     Second army's supply   0
First army's money    442     10s [±]  100s [±]     Second army's money    0
```

**A split is allocated, not apportioned.** The units move individually and the supply and money are
dialled across by hand; nothing in the dialog divides anything proportionally.

### It reconciles unit-for-unit against the save

The dialog's visible rows against `--inspect-army IP021.sav 233 67` (army 10), **in order**:

| Dialog | Save | Type | Save flag |
|---|---|---|---|
| `1st Dragoons Battalion  Hvy cav  2,190  average` | `1st Dragoons Battalion` | heavy cavalry | — |
| `2nd Lancers Battalion  Lit cav  6,110  average` | `2nd Lancers Battalion` | light cavalry | — |
| `3rd Bowmen Battalion  Archers  3,054  average` | `3rd Bowmen Battalion` | archers | — |
| `4th Bowmen Battalion  Archers  3,052  average` | `4th Bowmen Battalion` | archers | — |
| `3rd Guards Battalion  Hvy inf  5,237  average` | `3rd Guards Battalion` | heavy infantry | — |
| `2nd Foot Battalion  Lit inf  8,699  average` | `2nd Foot Battalion` | light infantry | — |
| **`Elymaian  Lit inf  10,278  average`** | `Elymaian` | light infantry | **mercenary (label 9)** |
| `1st Bowmen  Battalion  Archers  353  average` | `1st Bowmen  Battalion` | archers | — |
| **`Egyptian  Hvy inf  2,513  average`** | `Egyptian` | heavy infantry | **mercenary (label 35)** |

Same names, same order, same types. Troop counts differ by 1–3% because the dialog is 80 seconds into
the turn and the save is 6 seconds in.

**Mercenary naming is confirmed** `[confirmed]`. Every regular is `<ordinal> <Role> Battalion`;
the two units the save flags as mercenaries are **bare ethnonyms — no ordinal, no `Battalion`**. The
UI draws exactly what the save holds, so a name alone distinguishes a mercenary from a regular. This
is the distinction T55's mercenary skip needed, observed rather than inferred.

**Role names are confirmed** as `Foot` (light infantry), `Guards` (heavy infantry), `Bowmen`
(archers), `Lancers` (light cavalry), `Dragoons` (heavy cavalry) — matching T15's `ArmyNaming`.

**Ordinals are nation-wide per role, with gaps across armies** `[confirmed]`: this one army holds
`1st`, `3rd`, `4th` Bowmen, and the full roster adds `2nd` and `5th`. So the series is per type across
the nation and an army holds an arbitrary subset.

### One thing to follow up

`1st Bowmen  Battalion` carries a **double space** between role and `Battalion`, in the save *and* on
screen, where its `3rd` and `4th` siblings carry one. Earlier work on T55 treated double-spaced names
as a defect to fix. **This frame suggests at least some double spacing is faithful to the original.**
One instance is not a rule and the mechanism is unknown — recorded here so the question is asked
before anything is "corrected".

## 5. Fog of war confirmed `[confirmed]`

§1 read the foreign-army panel's blank `Moves` / `Supply` / `Morale` / `Money` as withheld, but could
not separate "withheld" from "zero rendered as empty". `IP1 019` t=112 supplies the missing half — an
**owned** army panel:

```
Army of Ptolemaic
Moves        0
Supply       415 tons  (58%)
Morale       high
Money        412 talents
Terrain      Plain
```

**`Moves` reads `0`, not blank.** A zero is drawn as a zero, so the foreign panel's empty rows are a
deliberate withholding. Composition and terrain are public; moves, supply, morale and money are not.

This panel also reconciles against `IP021.sav` army 10 exactly — `71,420` total troops, `412` money,
`15` units.

**`Morale` is a third word-ladder** `[confirmed]`, after readiness and unity: the panel reads `high`
where the save holds `68`. None of the three ladders is mapped beyond the points observed so far.

## 6. What this pass did not do

- `IP1 019`'s remaining frames are largely repeats of the owned-army panel while panning.
- The supply purchase dialog is unread, as are the `Fleet` and `City` submenus and the `Supply fleet`
  dialog glimpsed at `IP1 019` t≈159.
- **No second battle was found.** The one in §3 remains the only fully-read combat resolution.
- **`IP1 016`'s 22 "distinct" frames turned out to be the player panning the map**, not a sequence of
  dialogs. The detector had fired on the map's **grey mountain tiles**, which pass a "bright and
  near-grey" test as readily as a dialog does. Nothing was lost — the frames were cheap — but the
  prediction that consecutive distinct frames meant battle animation was wrong for this run, and a
  texture test would separate the two.
