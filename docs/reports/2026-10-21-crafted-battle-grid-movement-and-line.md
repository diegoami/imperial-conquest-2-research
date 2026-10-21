# Crafted battle grids: stored-icon movement and equal-coordinate clear-line

**Tag:** [confirmed, partial: static original instructions and retained Wine saves].
**Scope:** research [#40](https://github.com/diegoami/imperial-conquest-2-research/issues/40),
build [#1106](https://github.com/diegoami/imperial_conquest_2/issues/1106).

## Provenance and independent checks

This research-authored report follows the authorized ic2-conquest peer handoff
`RESEARCH40-SOURCE-ANALYSIS.md`, SHA256
`c972a30db004ab24acb2c5218389a53fb18a84e83aafe1625fb9bbd193e40def`,
received 2026-10-21. There is no new committed bot findings draft. Historical
packet references below are pinned to ic2-conquest
[`c8193ca1ebbb8f024963c4961bac8be02e940542`](https://github.com/diegoami/ic2-conquest/tree/c8193ca1ebbb8f024963c4961bac8be02e940542).
The historical saves are from release
[`run-exp-battle-sweep`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-battle-sweep),
checked against that revision's
[`SAVES.sha256`](https://github.com/diegoami/ic2-conquest/blob/c8193ca1ebbb8f024963c4961bac8be02e940542/runs/experiments/data/run-exp-battle-sweep/SAVES.sha256).

Research independently checked all sixteen whole-save hashes against that manifest,
redecoded the trailing 2,105-byte battle blocks with
[research40-grid-check.py](../../scripts/research40-grid-check.py), and checked
three c5/c6 whole-save identity pairs. The committed
[hash manifest](../data/research40-save-hashes.json) and
[scalar audit](../data/research40-grid-audit.json) retain exact names, digests,
headers, live slots and nonempty cells. The checker reads original bytes only;
it does not execute the original or the remake.

The complete local Ghidra listing SHA256 is
`2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8`;
the original executable SHA256 is
`9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31`.
Research rehashed both, read the cited source paths, and statically disassembled
the movement, lookup and equal-coordinate return instructions. These are source
and instruction reads, not fresh x86 execution or runtime traces. Binaries and
the full listing remain outside Git.

Remake comparisons are pinned to
[`9462e50786a34a9b4508b41c2f08727a02b5c853`](https://github.com/diegoami/imperial_conquest_2/tree/9462e50786a34a9b4508b41c2f08727a02b5c853).
The peer checked six normalized working-file blobs against that revision
(Board, Movement, Shooting, Melee, GeneralLine, GeneralEngage). Research reads
those same mounted files; this does not attest the whole mounted checkout or
a new replay at that revision.

## Stored-icon movement: c5, c6 and d5

`FUN_00438A6C`, listing lines 38694–38702, saves the old stored icon, clears
the old cell to 50, repaints it, writes the slot coordinates, stores the saved
icon at the destination, repaints it, and decrements moves. At `0x438CA7` the
old WORD is read, at `0x438CAB` saved on the stack, and at `0x438CE5/0x438CE9`
reloaded/written. Movement does not derive a replacement icon from the live slot.

At the pinned remake, `TacticalMovement.cs` calls `PaintIcon(slot)` after
updating position. A live defender HI6000 therefore paints 25, even when its
old stored cell was empty 50. On a northward step from (4,9), the first
**source-derived** unequal write is (4,8), original 50 versus remake 25.
The saved-boundary registry reports (4,7) after two steps. The intermediate
write has not been observed in a fresh runtime trace.

| Case | Before defender movement | Later retained boundary |
|---|---|---|
| c5 stale grid | BATTLE02: slot20 (4,9), moves2, stored cell50 | BATTLE03: slot20 (4,7), moves0, stored cell50 |
| c6 same cell | BATTLE02 byte-identical to c5 | BATTLE03 byte-identical to c5 |
| d5 stale grid | BATTLE01: slot20 (4,9), moves2, stored cell50 | BATTLE02: slot20 (4,7), moves0, stored cell50 |

Each listed boundary has two live HI6000 units and zero remaining shots.
Those saved troop values do not by themselves establish a complete intervening
operation log. c5/c6 BATTLE01, BATTLE02 and BATTLE03 match whole-file, pairwise.
Their exact filenames and hashes are in the committed audit.

In c6 the crafted start co-locates slots0/20 at (4,9), with stored attacker
icon5. AI placement `FUN_004381A4`, lines38200–38240, clears moving-side old
cells before writing their new positions/icons. Moving attacker0 away leaves
defender20 over empty50. This explains convergence with c5 without any grid
repair. These are deliberately crafted inputs; natural frequency is unproved.

## Equal-coordinate clear-line: d6

`CRAFT_d6_same_cell.SAV` starts with slots0/20 both at (4,9), stored icon5.
`FUN_00439F00`, lines39542–39543, returns false when both coordinate direction
components are zero. Instructions `0x439F84/0x439F89` test the components;
`0x439F91` clears ECX, `0x439F93` jumps to `0x43A04E`, and that return path
copies ECX to EAX. No occupancy lookup is needed for this branch.

For the nonarcher engage path, `FUN_0043A160`, lines39704–39752, this false
result selects the empty-cell box search. The x-offset outer/y-offset inner
scan uses strict nearest replacement; for the crafted overlapping input its
first acceptable adjacent cell is (3,8). In the pinned remake,
`GeneralLine.cs` skips its traversal and returns true for identical endpoints;
`GeneralEngage.cs` instead takes the line approach, initially asking Walk to
move to its current cell. This is a concrete source-derived branch difference.

The retained `b3_d6_same_cell_BATTLE01.SAV` has slot0 at (3,8), moves1,
target20; slot20 remains (4,9). Only grid(3,8)=5 is nonempty: the old shared
cell was cleared despite its surviving co-occupant. This matches the original
box branch. The registered remake x=6 is a later boundary; the full downstream
path to6 has not been traced or rerun here. A lookup-priority patch alone is
not established as its explanation.

## Operation matrix and separate findings


| Operation | Exact original source evidence | Semantics relevant to corrupt/doubled cells |
|---|---|---|
| Draw a square |004371E4,37528–37558|Reads grid WORD and draws corresponding sprite; no slot scan or grid write; repaint is not repair.|
| Compute/write icon |00437C40,37960–37979|Derives side/type/size and overwrites slot's current cell; no co-occupant arbitration. Caller chooses when.|
| Slot lookup |004383BC,38293–38315|Scans40 slots, troops>0 and XY equal, last matching index wins; independent of grid.|
| Empty/cost |00438848,38476–38510|Checks on-board and stored grid==50 plus distance bounds, not presence of a live slot.|
| Walk target capture |00438D24,38739–38748|Only if signed stored grid<50, resolve live-slot identity and filter friendly side; retain this target index in the walk.|
| Last-move danger |004389AC,38531–38583|Clamps neighbor coordinates, tests stored grid<50 before lookup/strength check.|
| Move |00438A6C,38694–38702|Copy old stored icon; clear old; repaint; update XY; store copied icon; repaint; decrement.|
| Human placement |004375EC,37733–37750|Also copies stored old icon, clears old, writes new XY and copied icon; not a global repair.|
| AI placement |004381A4,38200–38240|Clears moving side live-slot old cells then places and computes their icons; other co-occupants are not restored.|
| Remove |00438F78,38840–38850|Troops=0, stored cell=50, repaint; no survivor restoration.|
| Shot |0043910C,39013–39035|After troop/morale loss run rout first; only if target still live compute/write its icon and repaint.|
| Melee |004393EC,39146–39177|Rout actor then defender, then compute/write actor icon if live and defender icon if live, in that order.|
| Setup/resume |00439968,39191–39282;00436FB4,37447–37457|Refills side moves/clears targets/claims/increments counter; no global grid rewrite. Resume invokes setup, not fresh copy-in.|

Lookup no-match caveat is now bounded by static instructions, not guessed:
4383BC saves incomingESI;4383E6 overwritesESI only for a live coordinate match;
4383F2 returnsESI. There is no initialized -1/no-match default. On zero matches
the return depends on incomingESI. Do not replace this with a universal invented
default or classify any stale icon as a valid target without caller evidence.
No arbitrary malformed-input fidelity policy is selected by this observation.

Two additional source differences need separate scope decisions, not automatic
edits under the four-case correction:
- Build ComputerChecks/InDanger use SlotAt without the original stored-grid
  gate; original Walk captures destination identity once, not each loop.
- Build Shooting paints before rout; Melee paints both before routing. Original
  rout-before-live-repaint can change final grid contents on co-located deaths.
Neither is demonstrated as the first cause of these four saved discrepancies;
ordinary nonoverlap boards can hide the ordering difference. Original and port
Remove both clear a co-occupied cell without reconstructing survivors.

## Bounded follow-up and limits

Evaluate stored-icon movement and line-to-self first, with the four immutable
crafted fixtures and ordinary-grid controls. `GeneralLine.cs` requires explicit
ownership in a reviewed build contract. Keep shot/melee repaint ordering and
destination-grid gates separate unless that contract deliberately includes them.
Do not normalize grids, change global lookup defaults, edit golden fixtures,
relax comparison tolerances or infer arbitrary malformed-input policy.

Discriminating follow-up controls, **not executed here**:

1. Move the same HI6000 slot with old cell50 versus25; destination should inherit
   the stored value, with all other inputs identical.
2. Move either of two co-located slots; distinguish stored-icon transport from
   last-live-slot lookup and old-cell clearing.
3. Compare the actual d6 engage input with distinct adjacent endpoints; isolate
   the equal-coordinate false return and the (3,8) box choice.
4. Separate stored-empty/live-enemy occupancy from stored-nonempty/multiple-live
   occupancy; retain exact caller/register evidence for lookup without a match.
5. Route one co-located unit while the other survives; discriminate removal and
   repaint order only under a separately reviewed scope.

No fresh game, emulator, corrected remake or full-battle replay was run.
The old Wine observations and new static reads are distinct evidence classes.
No normal-game occurrence, complete four-case parity, native Windows confirmation
or research #40/build #1106 closure follows from this report. Research #25 and
SAV-export #37 are separate; no fixture, registry or build code changed.
