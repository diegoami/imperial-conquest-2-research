# Attack and siege are adjacency orders, not movement

**Evidence class: direct user observation of the original game, 2026-09-19.** Not decompilation, not a save diff. Recorded as its own report because it settles a question no existing report covers, and because the reimplementation was about to decide it the other way.

## The finding

> *"In the original game, first you select the army, then the town, and if they are adjacent there is a siege action. Same pattern for an army attacking an army, or a fleet attacking a fleet."*

Three consequences, all `[confirmed]` at the same strength as the observation:

1. **A siege is an order issued from adjacency**, not an army moving onto the city's tile.
2. **An army never occupies a city tile.** There is no game state in which an army and a city share coordinates.
3. **One interaction pattern governs all three attack forms** — army→city, army→army, fleet→fleet: select the actor, select the target, and if they are adjacent the action is offered.

## Why it needed recording

The reimplementation had two merged, individually correct facts that could not both be right, and no evidence to choose between them.

- `MoveArmyCommandHandler.IsBlocked` treats **every city cell as impassable**, including the mover's own nation's.
- A note in the build repo's issue [#190](https://github.com/diegoami/imperial_conquest_2/issues/190) (N5) recorded the opposite convention: *"distance **0** means the army stands in `meridia` — a state the rest of the engine reads as a **siege**."*

**The observation settles it for the movement rule.** The blanket city-cell block is **faithful**. N5's note described a *test fixture's* convention — a reviewer had parked a test army on a city's coordinates — and read a game rule into it that does not exist. That inference is now known to be wrong, and the build repo's note is being corrected.

## The second thing it settles

The build repo's `armies.disband-army` requires the army to be **co-located** with an owned city — a `[derived]` reading of the confirmed phrase *"near an owned city"*, chosen as the narrowest defensible option because no report decompiles a distance. Its review judged that honest, and it was, on the evidence then available.

**That state is now known to be permanently unreachable**, since an army can never stand on a city tile. So "near" must mean **adjacent**, and the disband rule widens accordingly (build repo [#215](https://github.com/diegoami/imperial_conquest_2/issues/215)).

Worth stating precisely, because it is a recurring shape: **two individually correct decisions in two different tasks produced an unreachable command.** Neither task was careless, and neither review could see both halves. What resolved it was not better reasoning but **new evidence of a kind the decompilation does not supply** — how the game behaves under a player's hands.

## What this does not establish

- **The exact adjacency metric.** "Adjacent" is observed; whether the game uses Chebyshev (8-way) or Manhattan (4-way) is not. The reimplementation uses Chebyshev as its shared map metric (`LandingTile.ChebyshevDistance`), and applying it here is `[derived]` until a decompilation or a controlled observation says otherwise.
- **What happens when the target is adjacent but the actor has no moves left**, or is embarked. The reimplementation gates both, from the merged battle rules rather than from this observation.
- **Whether a fleet can besiege a coastal city**, or whether sieges are army-only. Not observed; not assumed.

## How to confirm it further, cheaply

A recording of a single attack would pin the interaction order and the adjacency metric together: select an army, select a target two tiles away (no action offered), then one tile away (action offered). That is a 30-second capture, and [`/parse-recording`](https://github.com/diegoami/imperial_conquest_2/blob/main/docs/recording-analysis.md) reads it from a rough timestamp.

Worth doing on the next play-through, alongside the forced-capture observations [decompilation plan item 18](../decompilation-plan.md) wants.
