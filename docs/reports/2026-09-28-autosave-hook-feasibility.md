# Autosave hook: feasible, and a working proof of concept

The player never finished a game because saving is manual and every save needs a typed name, so turns go unsaved. The question was whether the original executable can save itself at the end of every player turn, to a generated name like `AUTO0042.SAV`, with no keystroke. It also has to log every firing, with the save routine's result, to `AUTOSAVE.LOG`, and do all this on both patched variants that `patch_exe.py` builds ("watch", the one the user plays, and "fast").

**Verdict: go.** The save routine takes no arguments and reads its file name from a global buffer, so it can be called with no dialog. There is one call site that every route into a human turn passes through, after all AI seats and the weekly tick have run and before the turn's UI starts. A 512-byte code cave in the `.patch` section that the watch patch already adds does the whole job. It is written as a new `autosave` option of `patch_exe.py`, and it has been run headless under Wine in this session: 5 turns ended, 5 log lines written, and one of them a deliberately forced failure that was logged and did not disturb the game. The autosave is **byte-identical** to a manual *Save* made at the start of the same turn. What is left is a run on the user's real Windows desktop.

Sources for everything below:

- the executable `Imperial Conquest 2.exe` (SHA-256 `9d753d5d…ba31`) and `patch_exe.py`, both in the root of `diegoami/imp_conquest_fixtures`, not in a release;
- a fresh Ghidra 12.1.3 headless decompile of 0x401000–0x460000 (2,011 functions), grepped per function, never read whole;
- the Delphi published-method tables, read directly out of the executable to recover the event-handler names;
- the save `1_rome_270_winter_11.sav` (`run-1-rome`) for the live runs.

## 1. The binary

| Question | Answer |
|---|---|
| Format | **32-bit PE** (machine `0x14C`, optional-header magic `0x10B`), not 16-bit NE. Image base `0x400000`, **DllCharacteristics `0`**: no ASLR, so it always loads at its preferred base. Absolute addresses in a cave are safe, and the `.reloc` section never comes into play. |
| Compiler / runtime | **Borland Delphi 2**. The evidence: linker version 2.25; the fixed Borland TimeDateStamp `0x2A425E19`; sections named `CODE`/`DATA`/`BSS`; Delphi's own exception code `0x0EEDFACE` in the RTL; VCL classes (`TFileStream`, `TSaveDialog`). There is no C runtime. |
| File I/O | Goes through **imported Win32 calls**, wrapped by the VCL. The save opens a `TFileStream` (class `0x4082A4`, constructor `0x40A75C`) on `CreateFileA`/`WriteFile`. The imports are reached through two `jmp [IAT]` thunk tables: the System unit's at `0x4012xx` and the Windows unit's at `0x4048xx`–`0x4049xx`. `GetTickCount` at `0x404914`, already used by `patch_exe.py`, is in the second. The cave uses the second table too: `CloseHandle 0x40489C`, `CreateFileA 0x4048AC`, `GetModuleFileNameA 0x4048FC`, `SetFilePointer 0x40499C`, `WriteFile 0x4049BC`. |
| Slack for a cave | `CODE` has only **0x2C bytes** of raw slack (VirtualSize `0x5B3D4` in a `0x5B400` raw block), which is too small. The usable space is the linker's **unused 9th section header**, which the watch patch already turns into a `.patch` section: VA `0x564000`, raw at end of file `0x11CC00`, 0x200 bytes. The autosave grows that section to 0x600 and puts its cave at `0x564200`. The whole section still fits in the one page that the `SizeOfImage` the watch patch writes (`0x165000`) already covers. |
| Does `patch_exe.py`'s approach extend? | **Yes, unchanged in style.** The new option uses the same `patch()` with its expected-bytes check, and the same two-pass `assemble()` with three small item kinds added: `("jmp", va)`, `("abs", label)`, and `("jn", …)` for a near conditional jump. The build refuses to run on anything but the known original, exactly as before. |

## 2. The save routine

The event handlers of the main form (`TPremierForm`) were recovered straight from the executable's published-method table. The names and addresses match the ones earlier reports quote from the recovered RTTI list.

```text
0x45AAD4 OpenGameFile   0x45AB84 SaveGameFile   0x45ABB0 SaveGameFileAs
0x45AC5C StartTurn      0x45B0A8 EndTurn        0x45BB1C StoreFormPositions
0x45C1C8 BattleConclusion (battle form's end → back into the seat loop)
```

**The routine is `FUN_004484d0`**, the writer half of the matched pair from [decompiled-sav-file-layout.md](decompiled-sav-file-layout.md).

- **Signature: `procedure SaveGame;`, with no parameters, no return value and no `Self`.** It turns the NUL-terminated name in the global **`char[100]` at `0x45E7A8`** into a string (length 100, at `0x4484F9`). It then opens `TFileStream.Create(name, fmCreate = 0xFFFF)`, writes every table, frees the stream in its own `try/finally`, and finally clears the map selection (`0x4A0328`/`0x4A032A` ← `‑1`). A live check agrees: File → Save sets the selected-army variable to −1 ([2026-10-02-unit-map-mouse-orders-and-tax-range.md](2026-10-02-unit-map-mouse-orders-and-tax-range.md), Pitfalls).
- **Failure is an exception, not a return code.** An `EFCreateError` or a write error propagates out of it. A caller that has to know the outcome must catch the exception. Left uncaught, it would unwind through `StartTurn`'s caller and abort the rest of the turn start.
- **How the name gets there.** `SaveGameFileAs` runs the save dialog (form `+0x2F0`, `Execute` at vtable `+0x30`), copies its `FileName` (`+0x44`) into `0x45E7A8` with `StrPCopy` (`0x405B88`), calls the routine, and sets `0x4A0334` ("the game has a file name") to 1. `SaveGameFile` calls `StoreFormPositions`, then calls the routine if `0x4A0334` is set, and falls back to *Save As* otherwise. `OpenGameFile` also copies the opened name into `0x45E7A8`, so after a load, *Save* overwrites the loaded file.
- **It can be called outside the dialog.** The dialog does not own the buffer; the buffer is a plain global. That removes the risk the brief named (a modal dialog owning the buffer). The only care needed is to put the player's own name back afterwards, or the next Ctrl-S would write to the autosave. The only callers are `0x45AB9A` and `0x45ABDC`.
- **A pre-existing quirk.** `StrPCopy` does not check length, so a dialog path longer than 99 characters already overruns the buffer in the original game. The cave refuses to save to such a path (status `LONG`) rather than repeat that.

## 3. The turn-end site

[decompiled-turn-and-calendar-sequencing.md](decompiled-turn-and-calendar-sequencing.md) names `EndTurn`, the weekly tick `FUN_004514ec` and `StartTurn`, but not the two routines between them. They are:

```c
void FUN_00451fdc(void) {                 // the seat loop
  FUN_0044adb0();
  while (DAT_004a0b7c == 0                 // no battle pending
         && nation[current].human == 0     // (+0x474B00, 0 = computer)
         && FUN_00449050()) {              // some seat is still human
    FUN_0044adb0();
    FUN_0044fa20();                        // one AI seat's whole turn
  }
  if (nation[current].human != 0)
    FUN_00452034();                        // a human seat is next
}
// FUN_00452034: roll the pending trade/alliance offer (0x49F008), then
//   0x452175  mov eax, [0x4A0BD0]         ; the main form
//   0x45217A  call StartTurn               ; <-- the hook site
//   0x45217F  ... further checks on the nation record in ebx
```

- **The AI's turns run inside the same routine chain.** `EndTurn` (0x45B0A8) advances the seat, runs the weekly tick when the round wraps (`0x45B139`), then calls the seat loop (`0x45B13E`). The loop runs every following AI seat back to back, and each AI turn advances the seat itself and can run the weekly tick again (`0x44FA98`). A hook at `EndTurn`'s entry, anywhere in the loop, or on the tick would therefore save mid-resolution, or once per AI seat.
- **The site: `0x45217A`**, the `call StartTurn` inside `FUN_00452034`. By then every AI seat has moved, the tick has run and the pending offer has been rolled. `StartTurn` has not yet started the turn: it has not printed the news, reopened the forms, set the title or shown the offer dialog. Every route into a human turn passes through this one instruction:
  - `EndTurn` (`0x45B13E`);
  - `BattleConclusion` (`0x45C1FF`), when a battle an AI started with the player has ended and the seat loop resumes;
  - `0x449107`, on the leader-falls path;
  - `NewGame` (`0x45AA8D`).

  **Loading a save does not pass through it**: `OpenGameFile` calls `StartTurn` directly at `0x45AB7B`, so loading does not autosave. All four points were confirmed live (§5), apart from the leader-falls and new-game routes.
- **What the save holds.** A save made here is the state the player would save by hand at the very start of the next turn. §5 shows this is byte-identical in practice. A save of the player's orders *before* resolution (the `IPnnnB.sav` kind) would need a different site, in `EndTurn` after the validity check (`0x45B0EC`). That is not recommended: nothing has resolved yet, and it is not what the user asked for.
- **Can the hook fire inside the watch patch's pumped loop? No.** It fires only at the turn-end site.
  - The busy-wait `Delay` (`0x448FFC`) that the watch patch replaces is called only from the battle form (`0x437B33`, `0x438D02`, `0x43934B`, `0x4398A2`).
  - The executable contains **no `TTimer`** at all.
  - The pumped loop discards keyboard, mouse and `WM_SYSCOMMAND`, and never calls `TranslateMessage`, so no menu, accelerator or button handler can run inside it.
  - The only way from a battle back to the hook is `BattleConclusion`, which the battle form's own End-turn handler calls (`0x437C28`) after its `Delay` calls have returned.
  - The seat loop exits while a battle is pending (`0x4A0B7C`), and the cave checks that flag again anyway (status `BUSY`).

  In the live watch run, a 5-minute paced battle (101 End-turn clicks) produced **no** log line; the line came once the battle had closed.

## 4. The hook design

**A call-site redirect into a cave.** The hook is not an inline detour. The 5 bytes at `0x45217A` change from `E8 DD 8A 00 00` (`call StartTurn`) to `E8 81 20 11 00` (`call 0x564200`). No original instruction is moved. The cave ends with `jmp StartTurn`, so `StartTurn` runs with exactly the registers and stack it would have had, and returns straight to `0x45217F`.

The cave, in order:

1. `pushad; push ebp; mov ebp, esp; sub esp, 0x1A8`. All eight registers are saved. The two that matter are **`eax` = the main form**, `StartTurn`'s `Self`, loaded at `0x452175`, and **`ebx` = the nation record**, which `FUN_00452034` reads again after `StartTurn` returns. `ebp` is the frame pointer on purpose: Delphi's exception unwinding restores `ebp` from the frame, and nothing else.
2. **Turn number.** The game keeps no absolute turn counter, only week (`0x4A0330`, odd 1–11), season (`0x4A032E`, 0 = Spring … 3 = Winter) and year BC (`0x4A0332`, counting down). These are the same fields as the SAV tail. The cave computes **`nnnn = (300 − yearBC) × 24 + season × 6 + (week − 1) / 2`**, one step per two-week turn, 24 a year: Spring week 1 of 270 BC is `0720`. The number is the same after a reload, sorts in play order, and reads back to a date.
3. **File name.** `GetModuleFileNameA` gives the executable's folder, and the cave appends `AUTOnnnn.SAV`. It uses the executable's folder and not the current directory, because the common file dialog moves the current directory.
4. **Guards.** If a battle is pending, status is `BUSY` and nothing is saved. If the full path is longer than 99 characters, status is `LONG` and nothing is saved. These are the only two ways a firing skips the save, and both are logged.
5. Copy the player's 100-byte name from `0x45E7A8` to the stack, and write the autosave path in its place.
6. **`try` SaveGame `except`**, built exactly as Delphi builds one: the frame `{next, handler, ebp}` on `fs:[0]`, a handler of `jmp _HandleAnyException` (`0x402D6C`), and a body that calls `_DoneExcept` (`0x403088`). The RTL does the unwinding, so the save's own `finally` still closes the file, the exception object is freed, and no error box appears. Status is `OK ` if the call returned, `FAIL` if it raised.
7. Put the player's name back into `0x45E7A8`.
8. **Log, after the call, with its result.** The cave replaces the file name with `AUTOSAVE.LOG` and calls `CreateFileA(GENERIC_WRITE, FILE_SHARE_READ, OPEN_ALWAYS)`, `SetFilePointer(FILE_END)`, `WriteFile` and `CloseHandle`. The line is fixed-width, 24 bytes, CRLF-terminated: `0744 AUTO0744.SAV OK  `. If the log itself cannot be opened, no line is written, and a missing line is the signal the brief asked for.
9. `mov esp, ebp; pop ebp; popad; jmp StartTurn`.

**Preserved state.** All general registers, `ebp` and `esp` are restored, and the return address is still on top of the stack when `jmp StartTurn` runs. The direction flag is assumed clear, as Delphi code always leaves it. The `fs:[0]` chain is restored on both paths. `0x4A0334` is not touched. The selection that `SaveGame` clears is cleared again by `StartTurn` anyway.

**Re-entry.** Only the caller can re-enter the cave, and the caller is the turn cycle. `SaveGame` does not pump messages and runs no dialog.

**Cost at turn end.** The save is one file of about 132 KB (131–133 KB across these saves). The log is one 24-byte append. Neither was timed separately, but it was not noticeable in the runs. On disk, 24 turns a year is about 3 MB per game-year.

**Why not an external loader.** A loader would start the game suspended and write the same bytes into the running process. It needs a second executable, and a process-injecting tool is exactly what antivirus software flags. It gains nothing, because the game is already run from a patched copy. **Rejected.**

**Known behaviour worth stating.**

- *Hot-seat* (several human nations): each human seat gets the same `nnnn`, so the last seat's save wins. The log shows every firing.
- *Reload and replay*: replaying a turn overwrites `AUTOnnnn.SAV` with the new line of play. The log keeps both lines.
- The cave does not call `StoreFormPositions`, which records the current nation's window layout into its record and would record the wrong nation in hot-seat. In the single-player runs the files were identical anyway.

## 4b. Composition with the watch and fast variants

| Bytes (file offset) | fast | watch | autosave |
|---|---|---|---|
| `0x45C013` (raw `0x5B413`), 2 B: `PlaySoundA` flags | ✔ | ✔ | — |
| `0x448FFC` (raw `0x483FC`): `Delay` | 1 B `C3` | 5 B `jmp 0x564000` | — |
| `0x45217A` (raw `0x5157A`), 5 B: `call StartTurn` | — | — | ✔ |
| NumberOfSections `0x106`, SizeOfImage `0x150` | — | 9, `0x165000` | 9, `0x165000` (same values) |
| Section header #9, raw `0x338`–`0x35F` | — | `.patch` 0x200 | `.patch` **0x600** |
| Raw `0x11CC00`–`0x11CDFF` (VA `0x564000`) | — | delay routine | kept (watch) or `CC` fill (fast) |
| Raw `0x11CE00`–`0x11D3FF` (VA `0x564200`) | — | — | cave, 512 B, then `CC` |

- **The hook site and the cave overlap nothing** that the other patches touch. The one shared structure is the section header, and it is shared on purpose. `autosave` accepts either an untouched header (fast), which it turns into a new `.patch`, or the watch patch's 0x200-byte `.patch`, which it grows. It refuses anything else. It therefore has to come **after** `pumping_delay` in a build list.
- **Fast does not move the turn-end site.** `Delay` lives only in the battle form, and the seat loop, `FUN_00452034` and the hook are identical in both variants. Fast only shortens the time between the loop stopping for a battle and `BattleConclusion` resuming it. The cave bytes are identical in the two autosave builds.
- **The existing outputs do not change.** With the option added, `patch_exe.py` still writes `watch.exe` and `fast.exe` byte for byte as before (`8ecb3333…4125` and `f7fa64f5…0be7`).

## 5. Verification: headless under Wine works

**Set-up that worked in this session's container (Ubuntu 24.04):**

- `dpkg --add-architecture i386`, then `apt-get install --no-install-recommends wine64 wine32:i386 xvfb xdotool imagemagick`. This container also needed `libgd3=2.3.3-9ubuntu5 libgd3:i386=2.3.3-9ubuntu5 --allow-downgrades`, because a PPA's `libgd3` blocked the i386 one.
- A 32-bit prefix (`WINEARCH=win32 wineboot -i`), with Xvfb on `:99`.
- The game folder copied into `C:\IC2`: the patched executable, `Imperial Conquest 2.dat`/`.hlp`/`.cnt`, `WAVS` and one save.

The game starts, loads and plays normally under Wine 9.0.

**Driving it** needs only fixed-position xdotool clicks on the 1280×1024 screen:

1. *File* (14,36) → *Open* (30,72); type the save name into the file field (636,450), then Enter.
2. Dismiss the offer dialog with *OK* (638,547) if one shows.
3. *Game* (45,30) → *End turn* (62,51), then confirm with *End turn* (122,307).
4. Wait until `AUTOSAVE.LOG` has one more line.

If an AI starts a tactical battle with the player, the battle screen stops the seat loop and waits for input. Clicking *Computer general on* (158,112), then *End turn* (110,112) until the battle closes, then *OK* on the result dialog (220,478), lets the loop resume. On the fast variant this takes two clicks. That is the procedure for a verification run and for the coach's grind runs: **fast + Computer general**.

**Results** (all from `1_rome_270_winter_11.sav`, Winter week 11, 270 BC):

| Run | Build | What happened | `AUTOSAVE.LOG` |
|---|---|---|---|
| 1 | watch+autosave | Loaded the save: no line (correct, loading bypasses the site). Ended the turn. | `0744 AUTO0744.SAV OK  ` |
| 1 | — | `AUTO0744.SAV` vs a manual *File → Save* made right after, at the start of that turn | **0 bytes differ** (132,149 B each). Tail: week 1, 269 BC, Spring, battle flag 0 |
| 1 | — | *File → Save* after the autosave | wrote `1_rome_270_winter_11.sav`, not `AUTO0744.SAV`: the player's name was restored |
| 2 | fast+autosave | A **directory** named `AUTO0744.SAV` put there to make the save fail. Ended the turn. | `0744 AUTO0744.SAV FAIL` — no error box, and the game reached Rome's turn normally |
| 2 | fast+autosave | Next turn: Gaul attacked Rome and the battle screen opened mid-AI-seat. No line while it was open. Played out with Computer general, OK clicked. | `0745 AUTO0745.SAV OK  ` (week 3, 269 BC, battle flag 0) |
| 3 | watch+autosave | The same two turns. The battle ran paced for 311 s (101 clicks, all discarded or handled by the battle form), with 1 line throughout; the line came after OK. | `0744 … OK  `, `0745 … OK  ` |

Every firing wrote exactly one line, after the call, with its result.

**What the desktop must still check by eye**, on real Windows, where the user plays:

1. The game folder is writable. A game under `Program Files` gets UAC file virtualisation, or a `FAIL` line, or no log at all.
2. `AUTOnnnn.SAV` and the log line appear after each End turn, and the next turn starts looking normal: news, window title, offer dialog.
3. Loading an `AUTOnnnn.SAV` with *File → Open* plays on.
4. Ctrl-S still writes to the player's own file.
5. Antivirus does not quarantine the patched executable.

### Build and check procedure (repeat after every change to the patch)

> **Update (2026-09-29): shipped as the "Rollingsave" builds.** The option below was adopted into `patch_exe.py` in `diegoami/imp_conquest_fixtures`, on branch `claude/admiring-feynman-c46hmx`, with the outputs renamed:
> - `Imperial Conquest 2 fast rollingsave.exe` (SHA-256 `95b93f03…a21fe`);
> - `Imperial Conquest 2 watch rollingsave.exe` (SHA-256 `70aa4513…b452`).
>
> These are byte-identical to the `… autosave.exe` builds tested here, and the procedure is unchanged apart from the names.

```text
# in the game folder, next to the untouched "Imperial Conquest 2.exe"
py patch_exe.py
#   up to date / wrote  Imperial Conquest 2 fast.exe
#   up to date / wrote  Imperial Conquest 2 watch.exe
#   wrote               Imperial Conquest 2 fast autosave.exe
#   wrote               Imperial Conquest 2 watch autosave.exe
```

Expected SHA-256 of the outputs, from original `9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31`:

| Output | SHA-256 |
|---|---|
| `Imperial Conquest 2 watch.exe` | `8ecb33333cb3658392fbd6838beac38d933cdb619413b99d30b181d435a64125` (unchanged) |
| `Imperial Conquest 2 fast.exe` | `f7fa64f5a2ffa0b573c324bdc694530bca6ce4d015d67cabff447e875c8b0be7` (unchanged) |
| `Imperial Conquest 2 watch autosave.exe` | `70aa4513c55eda4e2c164233afa5c3ae87d28e7ee95e2f551583666ce220b452` |
| `Imperial Conquest 2 fast autosave.exe` | `95b93f03ea9ce3581bb130491de17191d2d92843e785d98aeffff384748a21fe` |

Offsets touched, beyond each base variant: `0x45217A` (5 B), section header `0x338` (size fields `0x200 → 0x600`), and the appended raw `0x11CE00`–`0x11D3FF`. For fast+autosave, also `0x106`, `0x150`, the whole header at `0x338`, and raw `0x11CC00`–`0x11CDFF` (`CC`).

To confirm on a **fresh copy**:

1. Copy the autosave executable into a clean game folder with one save and no `AUTO*` files.
2. Start it, open the save (the log must **not** appear on load), and end the turn.
3. Expect exactly one new line in `AUTOSAVE.LOG` beside the executable, `nnnn AUTOnnnn.SAV OK  `, and `AUTOnnnn.SAV` beside it with the same size as a manual save. `nnnn` follows from the turn just started; 270 BC Spring week 1 is 0720.
4. Ending *k* turns must give *k* lines. A missing number, or anything but `OK`, is the fault report.

## 6. Estimate

| # | Task | Needs from Ghidra / the binary | Produces | State |
|---|---|---|---|---|
| 1 | Identify format, compiler, imports, slack | PE headers, import thunks | §1 | done |
| 2 | Find the save routine and how the name reaches it | `SaveGameFile(As)`, `OpenGameFile`, `FUN_004484d0` | §2 | done |
| 3 | Find the turn-end site and every route to it | `EndTurn`, `FUN_00451fdc`, `FUN_00452034`, xrefs of `StartTurn`/`BattleConclusion`, the `Delay` callers | §3 | done |
| 4 | Write the cave as a `patch_exe.py` option | the RTL's `_HandleAnyException`/`_DoneExcept`, the calendar globals, thunk addresses | Appendix A | done (proof of concept) |
| 5 | Headless verification under Wine | — | §5 runs | done |
| 6 | Desktop run on the user's Windows, fast+autosave and watch+autosave; the five eye checks | — | a short "confirmed on desktop" note | **open, about an hour** |
| 7 | Optional: cover the unexercised routes (new game, leader falls) and hot-seat | — | one line each in the log | open |
| 8 | Optional, for the coach: append the RNG seed or other runtime state (§7) | `0x45E030` | a small second file per turn | open |

**Go.** The one thing most likely to make it no-go is the **desktop environment rather than the code**: a game folder the user cannot write to (for example under `Program Files`), or antivirus refusing a modified executable. Either shows up in task 6 as `FAIL` lines or a missing log, and is fixed by moving the game folder, not by changing the patch.

## 7. Can the same site feed the coach?

**Yes, and it probably does not need a separate dump.**

- The site is exactly where the state is consistent for the player's decision.
- The file it writes is already a **complete state dump**: [decompiled-sav-file-layout.md](decompiled-sav-file-layout.md) accounts for every byte, and the build repository's parsers already read it.
- `AUTOSAVE.LOG` gives the coach a trigger: tail the log, and on each `OK` line read the named save.

If a different dump is wanted later, the cave's `call SAVE_GAME` is the only line that changes. Any routine that takes no arguments and follows Delphi's register convention can take its place, inside the same `try/except`, and the log line keeps working. The one piece of runtime state the save **lacks** that a coach might want is Delphi's `RandSeed` at **`0x45E030`**. The `Random` at `0x40284C` (107 call sites) advances it, and it is what makes AI turns differ between runs: two runs from the same save rolled different trade offers. A dump variant could append it as a 4-byte side file for reproducible forecasting.

## What this does not establish

- Behaviour on the user's real Windows desktop (task 6). Every run here was under Wine 9.0.
- The new-game (`0x45AA8D`) and leader-falls (`0x449107`) routes into the site, and hot-seat play. They are reached by code reading only, not run.
- How long the save and the log write take. They were not measured, only not noticed.
- Whether any other game function relies on `StoreFormPositions` running before a save. The autosave skips it, and the single-player files were identical anyway.

## Reproduction

The analysis:

- Ghidra 12.1.3 headless (`analyzeHeadless … -import "Imperial Conquest 2.exe" -postScript DumpApp.java all_app_functions.txt`, a 20-line script that decompiles every function between `0x401000` and `0x460000`), then per-function greps.
- Capstone disassembly of the listed addresses.
- Published-method names from a scan for Delphi method-table entries (`word size = 7 + len`, `dword code address`, `ShortString name`) in `CODE`.

The live runs: §5.

## Next checks

1. Task 6: build both autosave variants on the desktop, play three turns on each, and check the log, the files and the five eye checks.
2. Start a new game on an autosave build and check that the first human turn logs a line (the `0x45AA8D` route).
3. For the coach, decide whether the save alone is enough, or whether `RandSeed` should be dumped beside it.

## Appendix A: the proof of concept as a `patch_exe.py` option

This is a proof of concept, not a shipped patch. No modified executable exists outside this session's scratch space. Apply the diff below to `patch_exe.py`, then run `py patch_exe.py` in the game folder. The new function is `autosave`, and it composes with the existing options:

```python
build("Imperial Conquest 2 fast autosave.exe", async_sound, no_delay, autosave)
build("Imperial Conquest 2 watch autosave.exe", async_sound, pumping_delay, autosave)
```

**Hook**, VA `0x45217A`, raw `0x5157A`: `E8 DD 8A 00 00` → `E8 81 20 11 00`.

**Section header #9**, raw `0x338`, 40 bytes, after the patch:

```text
2E 70 61 74 63 68 00 00  00 06 00 00  00 40 16 00  00 06 00 00  00 CC 11 00  00…00 (12 B)  20 00 00 60
.patch                   VSize 0x600  VA 0x164000  RawSize 0x600 RawPtr 0x11CC00             code|exec|read
```

**Cave**, VA `0x564200`, raw `0x11CE00`, 512 bytes. It is followed by `CC` up to raw `0x11D3FF`.

```text
00564200  60 55 8B EC 81 EC A8 01 00 00 0F BF 05 32 03 4A 00 B9 2C 01 00 00 2B C8 6B C9 18 0F BF 05 2E 03
00564220  4A 00 6B C0 06 03 C8 0F BF 05 30 03 4A 00 48 D1 F8 03 C8 8B C1 BB 0A 00 00 00 33 D2 F7 F3 80 C2
00564240  30 88 95 67 FE FF FF 33 D2 F7 F3 80 C2 30 88 95 66 FE FF FF 33 D2 F7 F3 80 C2 30 88 95 65 FE FF
00564260  FF 33 D2 F7 F3 80 C2 30 88 95 64 FE FF FF C6 85 68 FE FF FF 20 C7 85 69 FE FF FF 41 55 54 4F 8B
00564280  85 64 FE FF FF 89 85 6D FE FF FF C7 85 71 FE FF FF 2E 53 41 56 C6 85 75 FE FF FF 20 66 C7 85 7A
005642A0  FE FF FF 0D 0A 68 04 01 00 00 8D 85 E0 FE FF FF 50 6A 00 E8 44 06 EA FF 8D BD E0 FE FF FF 03 F8
005642C0  4F 8D 85 E0 FE FF FF 3B F8 72 05 80 3F 5C 75 F0 47 89 BD 58 FE FF FF 8D B5 69 FE FF FF B9 0C 00
005642E0  00 00 F3 A4 C6 07 00 C7 85 76 FE FF FF 42 55 53 59 80 3D 7C 0B 4A 00 00 0F 85 8C 00 00 00 C7 85
00564300  76 FE FF FF 4C 4F 4E 47 8D 85 E0 FE FF FF 8B CF 2B C8 83 F9 63 0F 87 6F 00 00 00 41 51 BE A8 E7
00564320  45 00 8D BD 7C FE FF FF B9 64 00 00 00 F3 A4 59 8D B5 E0 FE FF FF BF A8 E7 45 00 F3 A4 C7 85 76
00564340  FE FF FF 46 41 49 4C 33 C0 55 68 6E 43 56 00 64 FF 30 64 89 20 E8 76 41 EE FF C7 85 76 FE FF FF
00564360  4F 4B 20 20 33 C0 5A 59 59 64 89 10 EB 0A E9 F9 E9 E9 FF E8 10 ED E9 FF 8D B5 7C FE FF FF BF A8
00564380  E7 45 00 B9 64 00 00 00 F3 A4 8B BD 58 FE FF FF C7 07 41 55 54 4F C7 47 04 53 41 56 45 C7 47 08
005643A0  2E 4C 4F 47 C6 47 0C 00 6A 00 68 80 00 00 00 6A 04 6A 00 6A 01 68 00 00 00 40 8D 85 E0 FE FF FF
005643C0  50 E8 E6 04 EA FF 83 F8 FF 74 2C 8B D8 6A 02 6A 00 6A 00 53 E8 C3 05 EA FF 6A 00 8D 85 60 FE FF
005643E0  FF 50 6A 18 8D 85 64 FE FF FF 50 53 E8 CB 05 EA FF 53 E8 A5 04 EA FF 8B E5 5D 61 E9 5C 68 EF FF
```

**The diff to `patch_exe.py`**:

```diff
--- a/patch_exe.py
+++ b/patch_exe.py
@@ -14,6 +14,12 @@
                                  stays visible. Keyboard and mouse input is
                                  discarded during the wait, so clicks can't
                                  interfere with a battle in progress.
+  Imperial Conquest 2 fast autosave.exe   fast, and the game saves itself
+  Imperial Conquest 2 watch autosave.exe  watch, and the game saves itself:
+                                 before each human turn starts it writes
+                                 AUTOnnnn.SAV beside the exe and appends
+                                 "nnnn AUTOnnnn.SAV OK" (or FAIL, BUSY, LONG)
+                                 to AUTOSAVE.LOG there.
 """
 
 import struct
@@ -39,6 +45,24 @@
 EXTRA_HEADER = 0x1F8 + 8 * 40
 EXTRA_VA, EXTRA_RAW, EXTRA_SIZE = 0x564000, 0x11CC00, 0x200
 
+# Autosave: the seat-start routine calls StartTurn at HOOK_SITE once the AI
+# seats and the weekly tick are done; the call is sent through a cave that
+# saves first. The cave goes after the delay routine, growing .patch to 0x600.
+HOOK_SITE = 0x45217A                    # call StartTurn
+START_TURN = 0x45AC5C
+SAVE_GAME = 0x4484D0                    # writes the save to the name in FILE_NAME
+FILE_NAME = 0x45E7A8                    # char[100]
+BATTLE_FLAG = 0x4A0B7C
+SEASON, WEEK, YEAR_BC = 0x4A032E, 0x4A0330, 0x4A0332
+HANDLE_ANY_EXCEPTION = 0x402D6C         # RTL: try/except handler, _DoneExcept
+DONE_EXCEPT = 0x403088
+CLOSE_HANDLE = 0x40489C
+CREATE_FILE = 0x4048AC
+GET_MODULE_FILE_NAME = 0x4048FC
+SET_FILE_POINTER = 0x40499C
+WRITE_FILE = 0x4049BC
+CAVE_VA, CAVE_RAW, PATCH_SIZE = EXTRA_VA + 0x200, EXTRA_RAW + 0x200, 0x600
+
 
 def off(va):
     return va - CODE_VA + CODE_RAW
@@ -66,7 +90,8 @@
 
 def assemble(origin, items):
     """Tiny two-pass assembler: bytes, ("label", name), ("call", va),
-    ("j", opcode, name) for short jumps."""
+    ("jmp", va), ("abs", name) for a label's address, ("j", opcode, name)
+    for short jumps, ("jn", opcode, name) for the near form of a short jcc."""
     labels, out = {}, bytearray()
     for _ in range(2):
         out = bytearray()
@@ -75,8 +100,13 @@
                 out += it
             elif it[0] == "label":
                 labels[it[1]] = len(out)
-            elif it[0] == "call":
-                out += b"\xE8" + rel32(origin + len(out), it[1])
+            elif it[0] in ("call", "jmp"):
+                out += (b"\xE8" if it[0] == "call" else b"\xE9") + rel32(origin + len(out), it[1])
+            elif it[0] == "abs":
+                out += struct.pack("<I", origin + labels.get(it[1], 0))
+            elif it[0] == "jn":
+                rel = labels.get(it[2], len(out)) - (len(out) + 6)
+                out += bytes([0x0F, it[1] + 0x10]) + struct.pack("<i", rel)
             else:
                 rel = labels.get(it[2], len(out)) - (len(out) + 2)
                 out += bytes([it[1]]) + struct.pack("<b", rel)
@@ -134,6 +164,108 @@
     patch(b, DELAY, bytes.fromhex("53568BF0E8"), b"\xE9" + rel32(DELAY, EXTRA_VA))
 
 
+def ebp(op, disp, imm=b""):
+    return op + struct.pack("<i", disp) + imm
+
+
+def autosave(b):
+    # Before StartTurn, save to AUTOnnnn.SAV beside the exe and append
+    # "nnnn AUTOnnnn.SAV STAT" to AUTOSAVE.LOG there, STAT being OK, FAIL (the
+    # save raised), BUSY (battle pending, not saved) or LONG (path > 99 chars,
+    # not saved). nnnn = (300 - year BC) * 24 + season * 6 + (week - 1) / 2.
+    # The player's own file name is put back after the save.
+    PATH, SAVED, LINE, WRITTEN, NAME = -0x120, -0x184, -0x19C, -0x1A0, -0x1A8
+    OK, FAIL, BUSY, LONG = (struct.pack("<4s", s) for s in (b"OK  ", b"FAIL", b"BUSY", b"LONG"))
+    JB, JE, JA, JNE, JMP = 0x72, 0x74, 0x77, 0x75, 0xEB
+
+    def digit(i):                                 # eax /= 10, digit i = remainder
+        return b"\x33\xD2\xF7\xF3\x80\xC2\x30" + ebp(b"\x88\x95", LINE + i)
+
+    code = assemble(CAVE_VA, [
+        b"\x60\x55\x8B\xEC",                      # pushad; push ebp; mov ebp, esp
+        b"\x81\xEC" + struct.pack("<I", -NAME),     # sub  esp, locals
+        b"\x0F\xBF\x05" + struct.pack("<I", YEAR_BC),
+        b"\xB9\x2C\x01\x00\x00\x2B\xC8",          # mov ecx, 300; sub ecx, eax
+        b"\x6B\xC9\x18",                          # imul ecx, ecx, 24
+        b"\x0F\xBF\x05" + struct.pack("<I", SEASON),
+        b"\x6B\xC0\x06\x03\xC8",                  # imul eax, eax, 6; add ecx, eax
+        b"\x0F\xBF\x05" + struct.pack("<I", WEEK),
+        b"\x48\xD1\xF8\x03\xC8",                  # dec eax; sar eax, 1; add ecx, eax
+        b"\x8B\xC1\xBB\x0A\x00\x00\x00",          # mov eax, ecx; mov ebx, 10
+        digit(3), digit(2), digit(1), digit(0),     # LINE = "nnnn AUTOnnnn.SAV ????\r\n"
+        ebp(b"\xC6\x85", LINE + 4, b" "),
+        ebp(b"\xC7\x85", LINE + 5, b"AUTO"),
+        ebp(b"\x8B\x85", LINE), ebp(b"\x89\x85", LINE + 9),
+        ebp(b"\xC7\x85", LINE + 13, b".SAV"),
+        ebp(b"\xC6\x85", LINE + 17, b" "),
+        ebp(b"\x66\xC7\x85", LINE + 22, b"\r\n"),
+        b"\x68\x04\x01\x00\x00",                  # GetModuleFileNameA(0, PATH, 260)
+        ebp(b"\x8D\x85", PATH), b"\x50\x6A\x00",
+        ("call", GET_MODULE_FILE_NAME),
+        ebp(b"\x8D\xBD", PATH), b"\x03\xF8",        # edi = PATH + length
+        ("label", "back"),                          # back up to the last backslash
+        b"\x4F", ebp(b"\x8D\x85", PATH), b"\x3B\xF8", ("j", JB, "dir"),
+        b"\x80\x3F\x5C", ("j", JNE, "back"),
+        ("label", "dir"),
+        b"\x47", ebp(b"\x89\xBD", NAME),            # inc edi; NAME = edi
+        ebp(b"\x8D\xB5", LINE + 5),                 # PATH = dir + "AUTOnnnn.SAV"
+        b"\xB9\x0C\x00\x00\x00\xF3\xA4\xC6\x07\x00",
+        ebp(b"\xC7\x85", LINE + 18, BUSY),
+        b"\x80\x3D" + struct.pack("<I", BATTLE_FLAG) + b"\x00", ("jn", JNE, "log"),
+        ebp(b"\xC7\x85", LINE + 18, LONG),
+        ebp(b"\x8D\x85", PATH), b"\x8B\xCF\x2B\xC8",  # ecx = strlen(PATH)
+        b"\x83\xF9\x63", ("jn", JA, "log"),
+        b"\x41\x51",                               # inc ecx; push ecx
+        b"\xBE" + struct.pack("<I", FILE_NAME),     # SAVED = FILE_NAME
+        ebp(b"\x8D\xBD", SAVED), b"\xB9\x64\x00\x00\x00\xF3\xA4",
+        b"\x59", ebp(b"\x8D\xB5", PATH),            # FILE_NAME = PATH
+        b"\xBF" + struct.pack("<I", FILE_NAME), b"\xF3\xA4",
+        ebp(b"\xC7\x85", LINE + 18, FAIL),
+        b"\x33\xC0\x55\x68", ("abs", "except"),     # try
+        b"\x64\xFF\x30\x64\x89\x20",
+        ("call", SAVE_GAME),
+        ebp(b"\xC7\x85", LINE + 18, OK),
+        b"\x33\xC0\x5A\x59\x59\x64\x89\x10",      # end try
+        ("j", JMP, "restore"),
+        ("label", "except"),
+        ("jmp", HANDLE_ANY_EXCEPTION),
+        ("call", DONE_EXCEPT),
+        ("label", "restore"),                       # FILE_NAME = SAVED
+        ebp(b"\x8D\xB5", SAVED), b"\xBF" + struct.pack("<I", FILE_NAME),
+        b"\xB9\x64\x00\x00\x00\xF3\xA4",
+        ("label", "log"),                           # PATH = dir + "AUTOSAVE.LOG"
+        ebp(b"\x8B\xBD", NAME),
+        b"\xC7\x07AUTO\xC7\x47\x04SAVE\xC7\x47\x08.LOG\xC6\x47\x0C\x00",
+        b"\x6A\x00\x68\x80\x00\x00\x00\x6A\x04\x6A\x00\x6A\x01\x68\x00\x00\x00\x40",
+        ebp(b"\x8D\x85", PATH), b"\x50",            # CreateFileA(PATH, GENERIC_WRITE,
+        ("call", CREATE_FILE),                      #   share read, 0, OPEN_ALWAYS, normal, 0)
+        b"\x83\xF8\xFF", ("j", JE, "done"),
+        b"\x8B\xD8\x6A\x02\x6A\x00\x6A\x00\x53",  # SetFilePointer(h, 0, 0, FILE_END)
+        ("call", SET_FILE_POINTER),
+        b"\x6A\x00", ebp(b"\x8D\x85", WRITTEN), b"\x50\x6A\x18",
+        ebp(b"\x8D\x85", LINE), b"\x50\x53",         # WriteFile(h, LINE, 24, &WRITTEN, 0)
+        ("call", WRITE_FILE),
+        b"\x53", ("call", CLOSE_HANDLE),
+        ("label", "done"),
+        b"\x8B\xE5\x5D\x61",                      # mov esp, ebp; pop ebp; popad
+        ("jmp", START_TURN),                        # eax (Self) as the caller left it
+    ])
+    assert len(code) <= PATCH_SIZE - (CAVE_RAW - EXTRA_RAW)
+
+    hdr = struct.unpack_from("<8sIIII", b, EXTRA_HEADER)
+    if hdr == (bytes(8), 0, EXTRA_VA - BASE, 0, EXTRA_RAW) and len(b) == EXTRA_RAW:
+        b += b"\xCC" * (CAVE_RAW - EXTRA_RAW)       # no delay routine (fast)
+        struct.pack_into("<H", b, NUM_SECTIONS_FIELD, 9)
+        struct.pack_into("<I", b, SIZE_OF_IMAGE_FIELD, EXTRA_VA - BASE + 0x1000)
+    elif hdr != (b".patch\0\0", EXTRA_SIZE, EXTRA_VA - BASE, EXTRA_SIZE, EXTRA_RAW) \
+            or len(b) != CAVE_RAW:
+        raise SystemExit("spare section header not as expected")
+    struct.pack_into("<8sIIIIIIHHI", b, EXTRA_HEADER, b".patch", PATCH_SIZE, EXTRA_VA - BASE,
+                     PATCH_SIZE, EXTRA_RAW, 0, 0, 0, 0, 0x60000020)
+    b += code.ljust(PATCH_SIZE - (CAVE_RAW - EXTRA_RAW), b"\xCC")
+    patch(b, HOOK_SITE, b"\xE8" + rel32(HOOK_SITE, START_TURN), b"\xE8" + rel32(HOOK_SITE, CAVE_VA))
+
+
 def build(name, *patches):
     b = bytearray(ORIGINAL.read_bytes())
     if struct.unpack_from("<I", b, CODE_VSIZE_FIELD)[0] != 0x5B3D4:
@@ -154,3 +286,5 @@
 if __name__ == "__main__":
     build("Imperial Conquest 2 fast.exe", async_sound, no_delay)
     build("Imperial Conquest 2 watch.exe", async_sound, pumping_delay)
+    build("Imperial Conquest 2 fast autosave.exe", async_sound, no_delay, autosave)
+    build("Imperial Conquest 2 watch autosave.exe", async_sound, pumping_delay, autosave)
```
