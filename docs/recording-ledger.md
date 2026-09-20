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
| `IP1 000` | 314s | **read** | t=12, 20, 21, 25, 180, 250 | Leader roster (all 16); game-start unit placement; **full battle resolution**; **tactical battle screen (`Attacker routed`)**; Army recruits; nation panel; Change tax |
| `IP1 001` – `IP1 015` | — | scanned | — | — |
| `IP1 016` | 212s | **surveyed** | t=140–200 | **Nothing new — map panning.** Its 22 "distinct" frames were grey mountain terrain tripping the dialog detector |
| `IP1 017`, `IP1 018` | — | scanned | — | — |
| `IP1 019` | 294s | **read** | t=112, 159 | **Owned-army panel** (settles fog of war); fleet panel and `Supply fleet` dialog seen, unread |
| `IP1 020` | — | scanned | — | — |
| `IP1 021` | 398s | **read** | t=1, 80, 86, 140 | News log Autumn→Winter; **`Unit map` command menu**; **Split army dialog, reconciled unit-for-unit**; foreign-army panel |
| `IP1 011` | 137s | **read** | t=135 | News log, Spring → Autumn wk1 |
| `IP1 012` | 190s | **read** | t=2 | Continuity check against `IP1 011` (no gap) |

**Saves**: all 45 dumped for calendar; `IP000`/`IP000B` inspected in full (nation + Alexandria);
`IP011B`/`IP012` compared across the season boundary.

### Distinct screens found, and whether they were read

| Screen | Occurrences | Read at full res |
|---|---|---|
| Nation panel (leader, cities, population, unity, tax, mobilized, treasury, international relations) | 15 | yes |
| News log (cumulative) | 7 | yes |
| Army recruits (recruitment table, costs, Mobilize/Disband) | 5 | yes |
| Own-army information panel | 5 | yes |
| Foreign-army information panel (fog of war) | 4 | yes |
| Save As / Open dialogs | 6 | n/a — OS chrome |
| Battle resolution ("Battle ended") | 4 | yes |
| Split army (two unit lists, supply and money spinners) | 2 | yes — reconciled against the save |
| Change tax level | 2 | yes |
| Supply purchase entry | 2 | no |
| Human and computer leaders (New Game) | 2 | yes |
| Game-start unit placement | 3 | partially |
| `Unit map` command menu (Army / Fleet / City) | 1 | yes — `Army` submenu; `Fleet` and `City` unopened |
| Fleet information panel, `Supply fleet` dialog | 2 | no |
| Remaining single-occurrence frames in `016`, `019` | ~30 | **not dialogs** — map panning, see the caveat above |

### What is most worth doing next, in order

1. **The tactical battle frames — now the highest-value target in the run.** `IP1 000` t≈19–24 holds
   the per-exchange screen (`ATTACKS`, `UNIT LOSSES`, `Attacker routed`), and
   [`instant-resolver-cannot-reproduce-a-tactical-battle.md`](reports/instant-resolver-cannot-reproduce-a-tactical-battle.md)
   showed why it matters: the reimplementation's instant path reproduces a tactical battle's **total**
   exactly and its **per-type shape** not at all, and cannot at any ratio. The per-exchange panel is
   the only source for the model that produces the shape. Extract at `fps=2` over t=18–26, not
   `fps=1` — exchanges resolve in under a second on the patched EXE.
2. **A second battle**, for the per-type ordering. The current detector will not find one reliably —
   see the note below.
3. **The `Fleet` and `City` submenus**, and the `Supply fleet` dialog (`IP1 019` t≈159). The `Army`
   submenu is fully transcribed; its two siblings are not, and together they are the rest of the
   command surface.
4. **The supply purchase entry dialog** (`IP1 000` t≈115 and three others), unread; T10's territory.
5. **A tax slider mid-drag**, for a second `(tax, income)` point. Not yet found.
6. `IP1 001`–`IP1 015`, `017`, `018`, `020` are scanned but nothing in them was read. Their dialog
   frames all deduplicated into screen types already transcribed, so the expected yield is low.

### Detector caveat, learned the hard way

The dialog detector scores the **near-grey fraction inside the map viewport**. The map's **mountain
tiles are grey**, so a recording where the player pans across mountains produces a long run of
high-scoring frames with no dialog in them — which is exactly what `IP1 016` was. Add a texture or
rectangularity test before trusting a run of consecutive hits, and do not read "many distinct frames"
as "an animation".


## Standing notes for future runs

- **Do not treat leader names as fixture data.** They are drawn per game — see
  [`ptolemy-run-ui-inventory-and-leader-draw.md`](reports/ptolemy-run-ui-inventory-and-leader-draw.md) §2.
- **Recordings in this run are continuous.** An earlier claim of gaps was an artifact of mtime
  arithmetic; do not repeat it.
- **The UI sweep of this run is complete**: all 22 scanned, 12 screen types identified, every
  recurring screen transcribed. What remains is the named residue in the list above, not an unknown.
- **Nothing has been moved to `recordings-processed/`.** With every recording short of *exhausted*,
  moving them would assert a completeness that does not exist. Move a recording only when its row here
  says **exhausted**.
