# `TUnitMap_JoinFleets` refuses at exactly 100 combined ships

**The question** ([decompilation plan](../decompilation-plan.md) item 15, from build repo
[#166](https://github.com/diegoami/imperial_conquest_2/issues/166)): does the original's fleet
join refuse when the combined ships are **less than 100** or only when **more than 100**? The
message says "*There are more than 100 ships in these fleets combined.*" but the recorded guard was
"`Combined ships < 100`", and the reimplementation accepts exactly 100 — so one of the two is off
by one.

## Answer

**The merge proceeds only when `ships[selected] + ships[partner] < 100`. Combined ships == 100 is
refused**, with the "*more than 100*" message — which is then wrong by one for that exact case.
`TUnitMap_JoinFleets`' recorded prose "`Combined ships **< 100**" in
[decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md)
is the correct reading, and the reimplementation's `JoinFleetsCommandHandler` (and the fleet-to-
fleet transfer mirroring it), which accept exactly 100, are off by one against the original.
**[confirmed: decompile]**

## The evidence

`TUnitMap_JoinFleets` (`0x00447A48`, dump :47218–47267):

```c
if ((short)(&DAT_0049c27e)[sVar1 * 0xd] + iVar2 < 0x65) {     // :47234  combined < 100
    <army-aboard check>;  <merge: ships, supplies, money carried over, partner deleted>
}
else {
    MessageDlg("There are more than 100 ships in these fleets combined.", …);   // :47260
}
```

The plan asked for the comparison *instruction* (`JL` vs `JLE`) rather than a prose summary. No new
Ghidra listing was taken for this report (the toolchain is Windows-side and was not re-run), so the
claim rests on the decompiler's own `<`, which distinguishes `JL` from `JLE` exactly — the same
evidence class as every `[confirmed: decompile]` claim in this repo — plus one independent
corroboration inside the same dump:

- **The AI's fleet merge uses the same strict bound.** `FUN_00450b30` (:54028, the computer seat's
  once-per-turn merge, see [2026-10-07-strategic-ai-turn.md](2026-10-07-strategic-ai-turn.md) §2.4)
  merges only when `(int)ships[a] + ships[b] < 100` — a second decompiled site choosing `<`, not
  `<=`, for the same 100-ship rule **[confirmed: decompile]**.
- The refusal itself is already save-confirmed (fixtures `UF05b`/`UF05c` in
  [2026-10-05-refusal-texts-and-conditions.md](2026-10-05-refusal-texts-and-conditions.md) R15),
  though those fixtures exceed 100 and so do not pin the boundary; the boundary comes from the code.

## What the reimplementation needs

Change `JoinFleetsCommandHandler` (and the fleet-to-fleet transfer's mirror of it) from
`combined <= 100` to `combined < 100`: a join that would land on exactly 100 ships is refused.
Keep the message as the original has it — the original itself shows "*more than 100*" for a
combined value of exactly 100, and a faithful clone reproduces that wording quirk.

## What this does not establish

- The `JL`/`JLE` instruction itself was not read from a listing; the verdict is decompiler-level,
  doubly corroborated. If the instruction byte is ever wanted, `DumpListing2.java` on `0x00447A48`
  settles it in one run.
- Whether the army-aboard refusal (the inner check, "*You cannot join fleets if one is carrying an
  army.*") shares any boundary subtlety was not re-examined; it is a plain either-or test.

## Reproduction

```text
TUnitMap_JoinFleets   dump :47218  (guard :47234, refusal :47260)
FUN_00450b30          dump :54028  (AI merge, same strict < 100)
```
