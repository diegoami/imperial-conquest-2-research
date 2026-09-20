# Recording ledger

**What has been extracted from which recording, and what is left.** Append to this file every time a
recording set is worked on. Runs arrive incrementally, so the cost of re-deriving "what did we already
look at" grows with every pass that does not write it down.

Method: [`recording-analysis.md`](https://github.com/diegoami/imperial_conquest_2/blob/main/docs/recording-analysis.md)
in the build repo. Release contents: [`evidence-index.md`](evidence-index.md).

## Depth levels

| Level | Meaning |
|---|---|
| **scanned** | Run through the automated dialog detector; distinct-screen timestamps known. No frame read by a human or a model. |
| **surveyed** | Representative frames read at contact-sheet scale. Dialog types identified; numbers not transcribed. |
| **read** | Specific frames read at full resolution and transcribed into a report. |
| **exhausted** | Every distinct screen read. **No recording is at this level.** |

## `run-1-ptolemy` — Ptolemaic, 270 BC, 22 recordings / 45 saves / 63.8 min

Scanned in full on **2026-09-20**: 118 dialog-bearing frames, deduplicated to **62 distinct screens**
across the run. All 22 recordings are at least **scanned**; the table records anything deeper.

| Recording | Len | Depth | Read at | Harvested |
|---|---|---|---|---|
| `IP1 000` | 314s | **read** | t=12, 20, 25, 180, 250 | Leader roster (all 16 nations); game-start unit placement phase; **full battle resolution panel**; Army recruits dialog; nation panel; Change tax dialog |
| `IP1 001` – `IP1 010` | — | scanned | — | — |
| `IP1 011` | 137s | **read** | t=135 | News log, Spring → Autumn wk1 |
| `IP1 012` | 190s | **read** | t=2 | Continuity check against `IP1 011` (no gap) |
| `IP1 013` – `IP1 020` | — | scanned | — | — |
| `IP1 021` | 398s | **read** | t=1, 85, 140 | News log, Autumn → Winter wk7; foreign-army information panel; two-army transfer dialog (**surveyed only, not transcribed**) |

**Saves**: all 45 dumped for calendar; `IP000`/`IP000B` inspected in full (nation + Alexandria);
`IP011B`/`IP012` compared across the season boundary.

### Distinct screens found, and whether they were read

| Screen | Occurrences | Read at full res |
|---|---|---|
| Nation panel (leader, cities, population, unity, tax, mobilized, treasury, international relations) | 15 | yes |
| News log (cumulative) | 7 | yes |
| Army recruits (recruitment table, costs, Mobilize/Disband) | 5 | yes |
| Own-army information panel | 5 | no — surveyed |
| Foreign-army information panel (fog of war) | 4 | yes |
| Save As / Open dialogs | 6 | n/a — OS chrome |
| Battle resolution ("Battle ended") | 4 | yes |
| Two-army transfer (units, supply, money) | 2 | **no — highest-value unread screen** |
| Change tax level | 2 | yes |
| Supply purchase entry | 2 | no |
| Human and computer leaders (New Game) | 2 | yes |
| Game-start unit placement | 3 | partially |
| Remaining single-occurrence screens in `016`, `019`, `021` | ~25 | **no** |

### What is most worth doing next, in order

1. **`IP1 016`, `IP1 019`, `IP1 021` have ~25 unread single-occurrence screens** between them — far more
   than any other recording. Consecutive distinct frames at 5-second spacing usually means an
   animation, and the strongest candidate is **more battles**. The battle panel is the densest frame
   in the game.
2. **The two-army transfer dialog** (`IP1 021` t≈85, t≈145). Surveyed only. It shows both armies' unit
   lists with names, types, troops and quality, plus supply and money spinners — it is the direct UI
   for T15's join/split/transfer and nothing has transcribed it.
3. **The supply purchase entry dialog** (`IP1 000` t≈115 and three others), unread; T10's territory.
4. **A tax slider mid-drag**, for a second `(tax, income)` point. Not yet found.

## Standing notes for future runs

- **Do not treat leader names as fixture data.** They are drawn per game — see
  [`ptolemy-run-ui-inventory-and-leader-draw.md`](reports/ptolemy-run-ui-inventory-and-leader-draw.md) §2.
- **Recordings in this run are continuous.** An earlier claim of gaps was an artifact of mtime
  arithmetic; do not repeat it.
- **Nothing has been moved to `recordings-processed/`.** With every recording short of *exhausted*,
  moving them would assert a completeness that does not exist. Move a recording only when its row here
  says **exhausted**.
