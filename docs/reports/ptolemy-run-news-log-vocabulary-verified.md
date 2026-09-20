# The news log's vocabulary, verified against a played year

**Evidence class: two recording frames, read against the reimplementation's shipped message catalogue, 2026-09-20.**
Pass 0 of the [`run-1-ptolemy`](https://github.com/diegoami/imp_conquest_fixtures/releases/tag/run-1-ptolemy)
sweep. Companion to
[`ptolemy-run-readiness-ladder-and-mobilization-rate-confirmed.md`](ptolemy-run-readiness-ladder-and-mobilization-rate-confirmed.md)
and to [`news-log-format-and-messages.md`](news-log-format-and-messages.md), which decompiled this
catalogue in the first place.

**The result is a confirmation, not a gap.** Every message form the game emitted across a full played
year is already in the reimplementation, worded identically. And the one rule that had been derived
from decompiled code with **zero positive observations** has now been observed.

## Why two frames were enough

The news log is **cumulative** — the panel holds every event since the game began, not just the
current turn. So a single frame late in a run carries the whole run. Two frames, at
`IP1 011.mp4` **t=135s** and `IP1 021.mp4` **t=1s**, span Week 1 Spring to Week 7 Winter 270 BC
between them: 22 turns of a sixteen-nation world, at a cost of two image reads.

This is the cheapest high-value extraction available from any recording, and it should be the first
thing done with a new set.

## 1. Thirteen message forms, all already shipped `[confirmed]`

Every distinct sentence observed, against `src/IC2.Engine/News/NewsMessageCatalog.cs` in the build
repository:

| Observed, verbatim | Catalogue key | Matches |
|---|---|---|
| `Brixia  (Gaul)  falls to Rome.` | `city.falls-to` | yes |
| `Modena defects from Gaul to Rome.` | `city.defects-to` | yes |
| `Rome destroys army of Gaul.` | `battle.army-destroyed` | yes |
| `Macedonia fails to capture Phoenice  (Greece).` | `city.fails-to-capture` | yes |
| `Bithynia and Seleucid have agreed to end their war.` | `peace.honourable` | yes |
| `Galatia sues Seleucid for peace and;` | `peace.sues-for` | yes |
| `Galatia ends all current trading agreements.` | `peace.ends-trading-agreements` | yes |
| `Galatia ends all current alliances.` | `peace.ends-alliances` | yes |
| `Galatia pays reparations of 140 talents.` | `peace.pays-reparations` | yes |
| `Macedonia forms an alliance with Illyria.` | `alliance.formed` | yes |
| `Macedonia declares war on Greece.` | `war.declared` | yes |
| `Greece finishes a new fleet at Athens.` | `fleet.finished` | yes |
| `Celtiberia depose their leader Sergius.` | `nation.leader-deposed` | yes |

**Thirteen of thirteen.** Including the awkward details that would be easy to get wrong and that no
one would invent: the **double space** around the parenthesised owner in `falls to`, the **semicolon**
ending `sues … for peace and;`, and the **four-space indent** on the three consequence lines that
follow it.

The catalogue also carries five forms this run did not produce — `battle.fleet-sunk`,
`fleet.lost-at-sea`, `fleet.damaged-in-storm`, `nation.conquered`, `nation.capital-moved`. Their
absence here is not evidence against them; a single year of one seat's view simply did not trigger
them.

## 2. The war-declaration shouting rule, observed for the first time `[confirmed]`

`NewsLogWriter.ApplyWarDeclarationShouting` uppercases a war declaration when either nation is
human-controlled. Its own documentation states the evidential position plainly:

> *confirmed against 7 of 7 observed war declarations — all lowercase, because all are between AI
> nations; **the uppercase form has never been observed in a save**.*

It has now, and in the best possible form — **both cases in the same frame**, from the same log, in
the same game:

| Line | Human involved? | Case |
|---|---|---|
| `Macedonia declares war on Greece.` | no — two AI nations | lowercase |
| `CARTHAGE DECLARES WAR ON PTOLEMAIC.` | **yes** — Ptolemaic is the player | **UPPERCASE** |

A matched pair is worth far more than either line alone. A rule derived from a `StrUpper` call in
`FUN_00449A44`, with no positive instance behind it, now has one — and the negative case sits
directly above it to rule out "this game always shouts war declarations."

**The reimplementation's behaviour is correct as shipped.** No change follows from this; what changes
is that the claim is no longer resting on decompilation alone.

## 3. What this does not establish

- **Whether the shouting depends on the player being the *target*.** In the observed instance
  Ptolemaic is the one declared upon. A declaration *by* the human against an AI would discriminate
  between "either nation is human" (what the code implements) and "the human is the target". The
  code's reading comes from `FUN_00449A44` itself and is the better authority; this frame simply does
  not separate the two.
- **Ordering within a week.** [`news-log-format-and-messages.md`](news-log-format-and-messages.md)
  §146 establishes that deposed-leader and fleet lines precede the week header, and nothing here
  contradicts that, but these frames were not read for ordering.
- **The five unobserved forms**, above.

## How to re-extract

```bash
FF="$LOCALAPPDATA/ReTools/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
"$FF" -ss 135 -i "IP1 011.mp4" -frames:v 1 news_spring_to_autumn.png
"$FF" -ss   1 -i "IP1 021.mp4" -frames:v 1 news_autumn_to_winter.png
```

The log occupies the left `Information` pane; the map beside it is irrelevant to this reading.
