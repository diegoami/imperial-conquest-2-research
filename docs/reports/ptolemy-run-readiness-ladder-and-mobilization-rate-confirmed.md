# The readiness ladder and the mobilization rate, confirmed against a live UI

**Evidence class: recording frames reconciled against the save pair either side, 2026-09-20.** First
findings from [`run-1-ptolemy`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-ptolemy)
— a Ptolemaic play-through of the whole of 270 BC. This is a first pass over two recordings, not a
sweep of the run.

Two rules this project had only from decompilation are now confirmed against the game's own screen,
and one of them is confirmed **at a wealth scale where a wrong reading would have shown**.

## The corpus, and why it is the best one yet

22 recordings, 45 saves, 63.8 minutes, one nation, one unbroken year:

| | |
|---|---|
| Nation | Ptolemaic (seat 3), leader **Cleopatra**, capital Alexandria, 46 cities |
| Span | Week 1 Spring 270 BC → Week 7 Winter 270 BC, **22 consecutive turns**, two weeks each |
| Naming | `IPnnn.sav` = turn *n* **before** the player's orders; `IPnnnB.sav` = the same week **after** them; `IP1 nnn.mp4` = that turn being played |

The `IPnnn → IPnnnB` pair isolates **the player's orders alone** — no AI, no turn processing, no
calendar advance. `IPnnnB → IPnnn+1` isolates **everything the engine does between turns**. That is a
controlled experiment design, and it is what makes the numbers below attributable.

**No written notes exist for this run, and none are needed.** File modification times plus each
recording's duration align every save to a second inside a recording; the method is recorded in the
build repo's `recording-analysis.md`.

## 1. `quality = state / 4` — confirmed, five points at once `[confirmed]`

One frame of the **Army recruits** dialog (`IP1 000.mp4` at **t=180s**) lists the units standing at
Alexandria with their readiness **as words**. `IP000.sav` holds the same five rows as **state codes**:

| On screen | Save state code | `state / 4` | DAT label at that index |
|---|---|---|---|
| `Hvy cav 900 not ready` | 7 | 1 | `not ready` (0–3) |
| `Lit inf 9,000 not ready` | 13 | 3 | `not ready` (0–3) |
| `Hvy inf 5,000 not ready` | 15 | 3 | `not ready` (0–3) |
| `Archers 2,000 very poor` | 17 | 4 | `very poor` |
| `Lit inf 7,500 poor` | 21 | 5 | `poor` |

Every row agrees. The two interesting ones are **15 → not ready** and **17 → very poor**: they sit
either side of the `state > 15` gate, and they confirm that the gate is not a separate threshold but
simply `quality >= 4` — *"no longer not ready"* — exactly as
[`decompiled-mobilization-and-mercenary-restock.md`](decompiled-mobilization-and-mercenary-restock.md) §4
derived from the DAT name table at `0x1F6CA`.

Until now that ladder was read out of a name table and a division in decompiled code. It is now also
read off the game's own screen, in words, for five different states.

## 2. The mobilization rate truncates — confirmed at a scale that discriminates `[confirmed]`

`IP000 → IP000B` is one player turn at Alexandria. The save diff shows **exactly 13 new recruitment
orders** appear, all at `state code 0`:

```
heavy infantry  6,000  x4      archers        3,500  x4
light infantry 10,000  x2      light cavalry  7,000  x2
                               heavy cavalry  2,500  x1
```

Over the same pair, Ptolemaic's mobilized percentage moves **17% → 30%**. Thirteen orders, **+13**.

The merged rule is `mobilized = min(100, mobilized + 1 + (troops * 1000) / wealth)`, with
`wealth = sum of population * 3000`. Ptolemaic's population is 10,191 thousand, so
`wealth = 30,573,000`, and the **largest** order in the batch gives
`10,000 * 1000 / 30,573,000 = 0` under integer division. All thirteen contribute exactly `1`.

**This is a discriminating test, not a coincidence.** Had that division been real-valued, the thirteen
orders would have added about `13 + 2.8`, landing on 32 or 33 — not 30. The corpus that produced the
rule was Roman; this confirms it on a different nation at roughly twelve times the wealth, which is
the wealth regime where the truncation actually bites.

## 3. Smaller confirmations from the same two frames

- **Leader names are drawn per nation and shown in the title bar** `[confirmed]`. `Ptolemaic's turn
  (Cleopatra)`, and in the placement phase `Seleucid's turn (Sennacherib)`. The build repo's exported
  world carries `leaderName: "(unassigned -- drawn at New Game)"` for every nation; these are two real
  values, and they are drawn **before** the first turn.
- **Unity is stored as a number and displayed as a word** `[confirmed]`. `IP000.sav` holds
  `unity value 666`; the nation panel at the same moment reads `Unity  normal`. A ladder like the
  readiness one exists for unity and is **not yet mapped** — one point is not a ladder.
- **Recruitment cost, one point** `[confirmed]`: a new `Hvy inf 6,000` order quotes
  `Initial cost 600` and `Quarterly cost 60`. That is `0.1 talents per troop` up front and **10% of
  the initial cost per quarter**, but with a single unit type at a single size it is one point on two
  curves, not a formula.
- **A game-start unit placement phase exists** `[confirmed]`. At `IP1 000.mp4` **t=20s** the status
  line reads `Seleucid v Ptolemaic — Ptolemaic to place units`, with a unit palette along the bottom
  and a `Computer general on` toggle. The reimplementation has no such phase — its worlds ship fixed
  `startingArmies`. Whether placement is free or constrained is **not established**; one frame shows
  the screen exists, nothing more.
- **The tax dialog previews income before committing** `[confirmed]`: `Current tax 13 / New tax 13`
  beside `Current income 801 / New income 801`, over a slider. So `tax 13% → income 801` is one real
  point on the income function. A frame where the slider has **moved but not been accepted** would
  give a second point for free, and across a few, the function itself. That frame was not in this pass
  and is the single cheapest next thing to look for.

  **An open dialog is an intent, not a commit.** This frame shows `New tax 13` — unchanged — and says
  nothing about what was finally applied. Across the same pair the saves do move, `IP000` holding
  `tax 13%` and `IP000B` holding `18%`, so the change was made at some other moment in the turn. Read
  the committed value from the save every time; a panel only ever shows what was on screen.

## 4. What did not reconcile

**A 3-talent treasury gap.** The nation panel at `t=250s` reads `Treasury 615 talents`. `IP000B.sav`,
written at `t=292s` of the same recording, holds **618**. `IP000.sav` holds 4,900, so the turn spent
4,282 talents and the direction is not in doubt — but 615 and 618 are 42 seconds and an unknown number
of clicks apart, and nothing in this pass accounts for the difference. **Recorded, not resolved.**

Two other deltas across `IP000 → IP000B` at Alexandria are noted without explanation, because neither
was watched on screen: supplies `969 → 489` tons, and the fortification line's city-unit troops
`24,400 → 98,900` while the percentage stayed at 77%.

## 5. What this pass deliberately did not do

Two recordings of twenty-two were opened, at four timestamps total. Nothing here rests on more than
one frame except sections 1 and 2, which rest on a frame **and** a save diff. In particular:

- No battle appears in the frames examined.
- The remaining 20 recordings are unexamined.

## 6. A correction, and the news log

An earlier draft of this report claimed the run had **gaps** — that each recording stopped before the
turn was ended, leaving the quarterly economy and the AI's moves unrecorded. **That was wrong**, and
it was wrong in an instructive way: it was inferred from arithmetic on file modification times
(`IP012.sav` is written after `IP1 011.mp4`'s mtime) rather than from looking at the frames.

The coverage is **continuous**. `IP1 011.mp4` at **t=135s** and `IP1 012.mp4` at **t=2s** show the
same screen at the same wall-clock minute. An `.mp4`'s mtime lags the moment recording stopped, so the
alignment in §1 places saves *within* a recording reliably but **must not be used to infer that
anything is missing between two recordings**.

What is actually there at that boundary is the **news log**, and it is the most valuable panel in the
run: a **cumulative scrollback of every event in the world since the game began**, in the game's own
words. One frame yields the whole year. From `IP1 011.mp4` t=135s alone:

| Sentence, verbatim | What it names |
|---|---|
| `Brixia  (Gaul)  falls to Rome.` | capture |
| `Modena defects from Gaul to Rome.` | **defection — a different word for a different mechanic** |
| `Seleucid destroys army of Galatia.` | army elimination |
| `Celtiberia pays reparations of 384 talents.` | reparations, with the amount |
| `Bithynia and Seleucid have agreed to end their war.` | peace |
| `Gaul depose their leader Caractacus.` | **leader deposition** |

Two of these matter beyond their wording. **`falls to` against `defects from … to`** is the exact
capture-versus-defection distinction T17 was built on, now confirmed as two separate sentences the
game itself emits. And **`depose their leader`** is a mechanic no report in this repository describes
and no task in the build repository models — leaders can evidently be removed and replaced during
play, which the exported world's static `leaderName` field cannot represent.

The news log is also **cheap**: because it is cumulative, a single frame late in a run substitutes for
watching the run. It should be the **first** thing read from any new recording set.

## How to re-extract any frame cited here

```bash
FF="$LOCALAPPDATA/ReTools/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
"$FF" -ss 180 -i "IP1 000.mp4" -frames:v 1 recruits.png     # 1, and the recruitment cost
"$FF" -ss 250 -i "IP1 000.mp4" -frames:v 1 nation.png       # leader, unity, the tax dialog
"$FF" -ss  20 -i "IP1 000.mp4" -frames:v 1 placement.png    # the unit placement phase
```
