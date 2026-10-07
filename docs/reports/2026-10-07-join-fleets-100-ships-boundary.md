# `TUnitMap_JoinFleets` accepts exactly 100 combined ships; the AI's merge refuses it

**The question** ([decompilation plan](../decompilation-plan.md) item 15, from build repo
[#166](https://github.com/diegoami/imperial_conquest_2/issues/166)): does the original's fleet
join refuse when the combined ships are **less than 100**, at **100**, or only above **100**? The
message says "*There are more than 100 ships in these fleets combined.*", the recorded guard was
"`Combined ships < 100`", and the reimplementation accepts exactly 100.

> **Correction of this report's own first version (commit `c94c0da`, same day).** The first
> version said combined 100 was refused, on a mis-converted constant: `0x65` was read as 100
> when it is **101**. The verdict below reverses it, and the mis-reading was caught by the
> cross-family review of `rules-specification.md` (GPT-6.1 Sol via OpenCode, 2026-10-07). The
> instruction-level caveat that report made — take the listing, not the prose — applies to this
> report's own prose now.

## Answer

**The human's Join fleets proceeds when `ships[selected] + ships[partner] < 0x65`, i.e. `< 101`:
combined ships of exactly 100 are accepted, 101 and above are refused**, with the "*more than
100 ships*" message — which is then exactly right for every refused case. The reimplementation's
`JoinFleetsCommandHandler` (and the fleet-to-fleet transfer mirroring it), which accept exactly
100, are **correct**; the recorded prose "`Combined ships **< 100**" in
[decompiled-unit-map-orders-and-record-fields.md](decompiled-unit-map-orders-and-record-fields.md)
was wrong by one (corrected there). **[confirmed: decompile]**

**The AI's once-per-turn fleet merge is stricter:** `FUN_00450b30` merges only when
`ships[a] + ships[b] < 100` — a literal `100`, not `0x65` — so the AI refuses a combined 100
that the human is allowed to make. The two sites are **not** the same rule; an earlier note here
claiming they corroborated each other was part of the same mis-reading. **[confirmed: decompile]**

## The evidence

`TUnitMap_JoinFleets` (`0x00447A48`, dump :47218–47267):

```c
if ((short)ships[sel] + iVar2 < 0x65) {        // :47234   0x65 = 101 → sum ≤ 100 merges
    <army-aboard check>;  <merge: ships, supplies, money carried over, partner deleted>
}
else {
    MessageDlg("There are more than 100 ships in these fleets combined.", …);   // :47260
}
```

`FUN_00450b30` (the computer seat's merge, see
[2026-10-07-strategic-ai-turn.md](2026-10-07-strategic-ai-turn.md) §2.4), dump :54028:

```c
if ((sVar2 < 0x22) && ((int)ships[a] + ships[b] < 100) && …)   // literal 100 → AI refuses 100
```

Both readings are decompiler-level (no new Ghidra listing was taken); the plan item's demand for
the `JL`/`JLE` byte still stands if instruction-level certainty is wanted — `DumpListing2.java`
on `0x00447A48` and `FUN_00450b30` settles both in one run. The refusal itself is already
save-confirmed above 100 (fixtures `UF05b`/`UF05c` in
[2026-10-05-refusal-texts-and-conditions.md](2026-10-05-refusal-texts-and-conditions.md) R15,
whose own description — "add up to 101 or more" — was right all along).

## What the reimplementation needs

No change to the accept-100 behaviour: it matches. Two smaller points: keep the message as the
original has it, and if the engine ever grows an AI fleet merge, gate it on `< 100`, not
`< 101` — the original's AI is stricter than its human UI.

## What this does not establish

- The `JL`/`JLE` instruction bytes themselves (decompiler-level verdict, doubly read: two
  independent sites with different constants, so a decompiler sign error would have to differ
  per site to mislead).
- Whether the AI's stricter bound is design or an off-by-one in the original's own AI code —
  not argued here; a faithful clone reproduces it either way.

## Reproduction

```text
TUnitMap_JoinFleets   dump :47218  (guard :47234 — 0x65 = 101, refusal :47260)
FUN_00450b30          dump :54028  (AI merge, literal < 100)
review that caught the first version's error: docs/rules-spec-review-2026-10-07.md, finding 8
```
