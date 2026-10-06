# The ten sounds: which game events play which WAV, and what each sounds like

**Status:** written directly from the decompile and a local measurement of the ten WAV files, for the clone's sound task (imperial_conquest_2 #790). **No play was run: every event mapping is `[derived: code]` and none has been heard in the running game.** The WAV files were analysed on the researcher's machine only; nothing of them (samples, waveform data, hashes) is reproduced here beyond a size and a duration.

> **Checked here:** agrees with the feature inventory's row M06 ([2026-10-05-player-facing-feature-inventory.md](2026-10-05-player-facing-feature-inventory.md): `TPremierForm_MakeSound`, cases 1-10, `PlaySoundA`) and with [decompiled-elimination-cleanup.md](decompiled-elimination-cleanup.md) (conquest starts with `MakeSound(10)`). Unit types, shot rules and the battle step functions are those of [2026-10-04-decompiled-tactical-battle-rules.md](2026-10-04-decompiled-tactical-battle-rules.md); the army and fleet walkers those of [decompiled-army-movement-and-river-cost.md](decompiled-army-movement-and-river-cost.md). **Not checked here:** anything in play (Wine or desktop).

**Tags.** `[derived: code]` = read from `all_app_functions.txt` (line numbers given as `:N`) or from a Ghidra scan of the EXE. `[derived: resource]` = read from the EXE's form resources. `[measured]` = measured from the WAV files with Python (`wave`, `numpy`). `[inference]` = what an observed code path means as a game event, where the code alone does not name it. `[open]` = not settled.

## Answer

1. **`TPremierForm_MakeSound` @ 0045BF28 (:59008-59050)** copies the sound folder path (form field `+0x36A`), appends `Sound1` ... `Sound10` for the argument 1-10 (a `switch`; any other value appends nothing, giving a path ending in `.WAV` only), appends `.WAV`, and calls `PlaySoundA(path, NULL, 0)` `[derived: code]`.
   - **Flags 0** = `SND_SYNC` with no `SND_FILENAME`, `SND_ASYNC`, `SND_LOOP` or `SND_NODEFAULT`: each sound **plays to its end and blocks the game while it plays**; nothing loops; Windows first tries the string as a registry sound alias, then as a file; and if the file is missing Windows plays its **default system sound** instead of staying silent (Win32 `PlaySound` semantics) `[derived: code]`.
   - **The folder** is set once in `TPremierForm_InitialiseForm` (:57986-57993): the name `1.wav` is expanded to a full path, cut to its directory, and `\WAVS\` is appended. The two RTL helpers (`func_0x00405a5c`, `FUN_004059d4`) are unnamed; read as `ExpandFileName` and `ExtractFileDir`, the folder is **`<current directory>\WAVS\`**, not necessarily the EXE's folder `[inference]`.
2. **There is no sound option.** `MakeSound` has no guard, no caller tests a sound flag, the main menu (File / Game / Strategy / Nations / Area map / Unit map / Help, all items read from the `TPREMIERFORM` resource) has no sound item, and the EXE holds no string such as Sound on/off, mute or volume `[derived: code + resource]`. The only control is the presence of the `WAVS` folder (and, with flag 0, a missing file beeps). The help's Improvements topic lists the sounds as a new feature (the decompressed words read "simple sounds ... clarify ... user's actions ... occurring elsewhere"; the topic text is phrase-compressed and the exact sentence was not rebuilt) `[open: exact wording]`.
3. **16 call sites, 10 sounds, every sound is used** (table below). The dump's 16 `TPremierForm_MakeSound(...)` calls equal a whole-CODE byte scan for `CALL 0045BF28` (Ghidra `ScanCalls.java`: 16 calls; the reference-based `FindXrefs.java` lists 14, missing the two in functions the Ghidra project has not defined, `TBattleMap_PlaceUnit` and `TUnitMap_ScuttleFleet`) `[derived: code]`.
4. **Who hears what.** Strategic sieges, fleet battles, storm losses, conquests and computer-against-computer field battles play their sound **whoever is involved**, including during computer turns (the help's "occurring elsewhere"); the step ticks (1, 2) play only while the **current seat is human**; the tactical-battle sounds play for both sides. A human's own field battle has **no** result sound: it opens the battle screen, whose shots, melee and moves have sounds, and its end window (`TBattleOver`) plays none `[derived: code]`.

## The call sites `[derived: code]`

Line numbers are of `all_app_functions.txt`; the call address is the scan's.

| # | Sound | Call (address) | Function | :line | What the code does at that point | Event `[inference]` |
|---|---:|---|---|---:|---|---|
| 1 | 1 | 0x00437629 | `TBattleMap_PlaceUnit` @ 004375EC | 37735 | inside the test "target cell is in the side's home rows" (attacker y < 3, defender y > 8), before the unit is moved there | human places a unit (battle placement) |
| 2 | 1 | 0x004382C8 | `FUN_004381A4` (AI placement) | 38236 | once per unit as the AI puts it on its formation cell | computer places a unit |
| 3 | 1 | 0x00438C91 | `FUN_00438A6C` (one step of the battle move `FUN_00438D24`) | 38694 | in the branch that performs the step (moves > 0, no blocking target, distance ≤ 9), before the cell swap | a battle unit moves one cell (human or AI) |
| 4 | 3 | 0x00439155 | `FUN_0043910C` (a shot) | 38975 | shooter type = 2 | **archers** shoot |
| 5 | 4 | 0x00439165 | `FUN_0043910C` | 38978 | shooter type ≠ 2 (only LI and LC also have shots) | light infantry or light cavalry throw (javelins) |
| 6 | 5 | 0x0043751B | `TBattleMap_SelectUnit` @ 0043747C | 37682 | a selected unit with moves ≥ 1 and an adjacent enemy clicked: its melee target is set | human orders a melee attack |
| 7 | 5 | 0x00439478 | `FUN_004393EC` (melee resolution) | 39077 | once per own unit with a live target, at each melee of the moving side's half-round | a melee exchange (both sides) |
| 8 | 8 | 0x00447EEB | `TUnitMap_ScuttleFleet` @ 00447E34 | 47348 | after Yes to "Are you sure you want to scuttle this fleet ?" | human scuttles a fleet |
| 9 | 9 | 0x0044AF61 | `FUN_0044AEE4` (army attacks army) | 49639 | only when **neither** army's owner is human (`+0x490` both 0), before the instant resolution | a field battle between two computer nations |
| 10 | 7 | 0x0044B38B | `FUN_0044B27C` (siege) | 49817 | besieger's strength beats the city's; then the news line `<city> (<owner>) falls to <nation>.` and the capture `FUN_0044BB18` | a city is taken |
| 11 | 6 | 0x0044B425 | `FUN_0044B27C` | 49828 | otherwise; news `<nation> fails to capture <city> (<owner>).` | a siege fails |
| 12 | 8 | 0x0044B5E4 | `FUN_0044B5D0` (fleet attacks fleet) | 49902 | first statement; the loser is always removed; news `<winner> sinks fleet of <loser>.` | a fleet battle (a fleet is sunk) |
| 13 | 10 | 0x0044C53C | `FUN_0044C528` (conquest) | 50627 | first statement; every city of the loser then goes to the winner | a nation is conquered (falls below 6 cities on a capture, from `FUN_0044BB18` :50214/:50226) |
| 14 | 1 | 0x0044D6D2 | `FUN_0044D420` (one step of the army walker `FUN_0044D734`) | 51503 | after a step is made, only if the current seat is human (`DAT_004A0320`'s `+0x490`) | an army moves one tile on the unit map (a tick per tile) |
| 15 | 2 | 0x0044E035 | `FUN_0044DD70` (one step of the fleet walker `FUN_0044E094`) | 51985 | after a step is made, only if the current seat is human | a fleet moves one tile (a tick per tile) |
| 16 | 8 | 0x00451852 | `FUN_004514EC` (weekly tick, storms) | 54594 | a storm leaves the fleet's ships below 40; news `A fleet belonging to <nation> is lost at sea.`, fleet removed | a fleet is lost in a storm |

## The ten sounds

Each file is mono. "Original" is the shipped format (`WAVS - Copy`); the measurements are of the working copies converted to 16-bit / 44.1 kHz `[measured]`.

| Sound | Original format, size | Duration | Measured character `[measured]` |
|---:|---|---:|---|
| 1 | 8-bit 11,025 Hz, 274 B | 0.02 s | A single 20 ms click at full scale, mostly below 250 Hz; no decay (it is cut off at full level). A dry tick. |
| 2 | 16-bit 22,050 Hz, 2,158 B | 0.05 s | A 50 ms soft tonal blip around 450-550 Hz (peak -8 dBFS), short fade. A muted "plip". |
| 3 | 8-bit 11,025 Hz, 3,926 B | 0.35 s | Two parts: 0.15 s of quiet, rising, airy tone (450/900 Hz), then a sharp low thud (75-100 Hz) at 0.2 s that decays in 0.14 s. A whoosh ending in an impact. |
| 4 | 8-bit 11,025 Hz, 1,658 B | 0.15 s | A 0.1 s tonal "zip" centred near 1.1 kHz, fast attack, fast decay. |
| 5 | 8-bit 11,025 Hz, 4,148 B | 0.37 s | Bright and metallic: a noisy attack, then inharmonic ringing partials around 2.0, 2.2 and 3.2 kHz that decay slowly over the whole file. A blade clang. |
| 6 | 8-bit 11,025 Hz, 5,016 B | 0.45 s | Low (125-300 Hz), loud at once, four overlapping dull knocks, decaying to 10 % by the end. Thuds against something heavy. |
| 7 | 8-bit 11,025 Hz, 9,104 B | 0.82 s | The loudest file (RMS -6 dBFS): 0.2 s of mid-high noisy rattle (about 2 kHz), then a heavy low boom (75-100 Hz) peaking at 0.44 s and rumbling out by 0.8 s. A crash and collapse. |
| 8 | 8-bit 5,512 Hz, 1,706 B | 0.30 s | 0.13 s of faint low hum, then a 0.1 s burst whose pitch falls from about 800 Hz to 200 Hz, then silence. A short downward "bloop" (something going under). |
| 9 | 16-bit 22,050 Hz, 18,274 B | 0.41 s | Quieter (RMS -19 dBFS): bell-like inharmonic partials at about 1.0, 1.4, 1.8 and 2.3 kHz from the first instant, decaying steadily. A distant metallic ring. |
| 10 | 8-bit 11,025 Hz, 15,612 B | 1.41 s | The longest: one sustained tone at a steady 168-170 Hz (about E3) with strong harmonics (340, 510, 680, 850 Hz), full level for 0.2-1.0 s, then fading. A single low horn blast. |

None loops (and `MakeSound` never loops a sound). Because play is synchronous, sound 10 freezes the game for 1.4 s, and an army walk plays sound 1 once per tile.

## Sound → events → suggested replacement

| Sound | Events (call-site rows) | Original's character | Suggested generation prompt (original-free) |
|---:|---|---|---|
| 1 | army step on the unit map, human seat (14); battle unit placed, human or AI (1, 2); battle unit moves one cell (3) | 20 ms dry low click | "single very short soft wooden footstep tick, dry, no reverb, 0.05 s" |
| 2 | fleet step on the unit map, human seat (15) | 50 ms soft blip, 500 Hz | "single short oar dip into calm water, soft plip, 0.1 s" |
| 3 | archers shoot (4) | whoosh then thud, 0.35 s | "ancient arrow flying past then striking a wooden shield, whoosh and thunk, 0.4 s" |
| 4 | light infantry or light cavalry shoot (5) | 0.15 s tonal zip, 1.1 kHz | "thrown javelin whizzing through the air, quick zip, 0.2 s" |
| 5 | human sets a melee target (6); each melee exchange (7) | 0.37 s bright metallic clang | "two iron swords clashing once, bright metallic clang with short ring, 0.4 s" |
| 6 | a siege fails (11) | 0.45 s low dull thuds | "battering ram hitting a heavy wooden city gate that holds, dull thuds, 0.5 s" |
| 7 | a city is taken (10) | 0.8 s rattle then heavy boom | "stone city wall collapsing, rattle then a heavy rumbling crash, 0.8 s" |
| 8 | a fleet battle, a fleet sunk (12); a fleet lost in a storm (16); a fleet scuttled (8) | 0.3 s falling-pitch bloop | "wooden ship sinking, short splash and falling gurgle, 0.5 s" |
| 9 | a field battle between two computer nations (9) | 0.4 s quiet distant ring | "distant ancient battle, faint clash of metal echoing far away, quiet, 0.5 s" |
| 10 | a nation is conquered (13) | 1.4 s single low horn note | "single low ancient war horn blast, solemn, steady note fading out, 1.5 s" |

## Notes for the clone `[inference]`

- Keep the triggers, not the blocking: the original's `SND_SYNC` stalls the game for each sound (most visible with sound 10 and with sound 1 on long walks); an asynchronous player with one voice per sound reproduces what is heard without the stall.
- Gate 1 and 2 on "the current seat is human", as the original does; play 3 to 10 regardless of who is involved.
- No option to switch sounds off exists to copy; any toggle the clone adds is new.

## Method

- `grep` of `all_app_functions.txt` for `TPremierForm_MakeSound` (16 call lines), each read in its function; enclosing function names from the dump's `// ====` headers and `delphi_symbols.tsv`.
- Completeness: Ghidra headless on the project `IC2`, read-only: `FindXrefs.java 0045bf28` (14 references) and `ScanCalls.java 0045bf28` (16 `E8` calls in CODE; the two extra are the dump's `TBattleMap_PlaceUnit` and `TUnitMap_ScuttleFleet`). `PlaySoundA` appears once in the dump (:59048); no `sndPlaySound` or `mci` call.
- Menu and option search: captions of all form resources in the EXE (352 `Caption` strings, the full main menu among them), and an ASCII search of the EXE for sound / mute / quiet / volume / audio. Help: the `|TOPIC` file of the `.hlp` LZ77-decompressed; it is also phrase-compressed (`|PhrIndex`/`|PhrImage`), which was not undone.
- Audio: Python `wave` + `numpy`: duration, peak and RMS level, a 10 ms RMS envelope (attack, decay to 10 %, bursts), whole-file band energies and per-40 ms frames (top spectral peaks, spectral flatness, autocorrelation pitch).

## Open

- `[open]` Nothing here is heard in play; a Wine or desktop run that logs `PlaySoundA` (or listens) at a siege, a storm loss and a battle would confirm the mapping.
- `[open]` The help's exact sentence on sounds (phrase decompression not done).
- `[open]` Whether the folder is the current directory or the EXE's (the two RTL helpers are unnamed); the release readme only says to keep the `WAVS` subfolder.
- `[open]` The full ZIP places the WAVs at the archive root while the EXE expects `WAVS\` ([research.md](../research.md)); with flag 0 a missing file plays the Windows default sound, so an install without the folder would beep at every event `[inference]`.
