# Imperial Conquest 2 — reverse-engineering research

Static reverse-engineering research on *Imperial Conquest 2* (1996, Delphi/Win32), a 4X strategy game — save/DAT file format, decompiled game formulas, and evidence-based reports building toward a modern reimplementation.

**This is the research record, not the game.** The actual reimplementation (data parsers, the game engine, the Godot client) lives at **[diegoami/imperial_conquest_2](https://github.com/diegoami/imperial_conquest_2)**, which cites the reports here directly. Split out into its own repository so the reverse-engineering work — reading a commercial 1996 game's internals — and the game engine itself — a clean-room, moddable reimplementation — can be published, shared, and licensed separately.

No original game files (EXE, DAT, HLP, SAV, screenshots, recordings) are included here — everything is a report *about* them, written from static analysis and controlled in-game experiments. See `docs/research.md` for the evidence-provenance overview.

## Contents

- `docs/research.md` — static research notes and the evidence-provenance overview.
- `docs/roadmap.md` — the staged research plan and its status.
- `docs/decompilation-plan.md` — the Ghidra static-decompilation priority queue and status.
- `docs/reports/` — 51 individual findings, from initial file-format analysis through fully decompiled game formulas (economy, combat, movement, diplomacy, AI dispatch, and more).

## Toolchain

The local decompilation toolchain (Ghidra, recovered Delphi symbols, decompiled-function dumps) lives outside both repositories, on the researcher's own machine — not checked into either repo, consistent with never distributing the original game's files or a full disassembly of its executable.
