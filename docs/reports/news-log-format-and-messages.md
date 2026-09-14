# The news log: 40 NUL-terminated 61-byte slots, 21 message templates, and no diplomatic offers

The question: how exactly does the original store and format its news log? [`decompiled-news-log-identified.md`](decompiled-news-log-identified.md) found the ring buffer (`DAT_0049F994`, 40 slots of 61 bytes, newest index in `DAT_004A031E`) and the writer `FUN_00449240`, but left the slot layout, the SAV sizing gap and the message set open. The dev repo's T10 review then read the saves and reported five things: thousands separators in numbers, a 60-byte text limit, stored date headers and blank lines, literals missing from its corpus, and no "*wants to trade*" line in any save. This report settles each from the code and checks it against all 54 local saves.

**Answer.**

- **A slot is a plain NUL-terminated single-byte string, 61 bytes, with no header.** The text is at most **60 bytes**. The writer never truncates, and no message the game can build is longer than **59** **[confirmed: 2,101 slots in 54 saves, every one NUL-terminated, longest 59, every byte 0x20–0x7E]**.
- **The log is a shift register, not a circular buffer.** Slot 0 is always the oldest. When all 40 are used, slots 1–39 are copied down one and the new message goes into slot 39. The SAV stores the newest index, then that many slots plus one, each a full 61 bytes including stale bytes after the NUL **[confirmed: 252 of 252 overlapping save pairs reproduce byte for byte]**.
- **The ~6-byte gap was an arithmetic slip.** The 3,042-byte region is `600 + 2 + 40 × 61` exactly. The old reconciliation subtracted the 55-byte trailer from a length that already excluded it **[confirmed]**.
- **Numbers are grouped with a hard-coded comma.** The only grouped number is the reparations amount: "*pays reparations of 2,269 talents.*" The formatter is the game's own `FUN_00448F3C`. It does not call `Format` or `FormatFloat` and does not read the locale **[confirmed: 2 amounts ≥ 1,000 carry a comma, 3 below 1,000 do not]**.
- **Date headers and blank lines are ordinary entries in the 40 slots.** At the very end of each round tick, `FUN_004514EC` writes a single space (`" "`), then `Week  9      Summer      270BC`. That happens once per completed round of 16 seats, which is two game weeks **[confirmed: every in-game header not already shifted into slot 0 follows a `" "` entry, 338 of 342]**.
- **The EXE has 24 calls to the writer, using 21 templates.** In the corpus, two entries lack their final period, three entries are not news at all, and 8 templates are missing (Q4).
- **A pending trade or alliance offer is announced by a modal `MessageDlg` (`mtInformation`, `[mbOK]`), never by the news log.** `TPremierForm_StartTurn` builds "*Greece wants to trade with Rome.*" and shows it in a dialog. Nothing calls the news writer **[confirmed: 6 saves hold a pending offer, and no news slot contains "wants"]**.

Line numbers are in `%LOCALAPPDATA%\ReTools\all_app_functions.txt`. There are two new dumps in the same folder. `news_log_listing.txt` is the instruction listing of the writer, the number formatter and `TPremierForm_StartTurn`. `news_log_decomp.txt` decompiles `FUN_00448AA4` (new game) and the DAT loader `FUN_004481A0`; neither is in the whole-application dump. The helpers are all Delphi `SysUtils` PChar routines: `FUN_00405B00` is `StrCopy` (unbounded), `FUN_00405BC8` is `StrCat`, `FUN_00405B54` is `StrLCopy`, `FUN_00405A98` is `StrLen`, `FUN_00405C98` is `StrUpper` (ASCII `a–z` only), and `FUN_004028C4` is `Str(int)`.

## Q1. The slot layout

### Memory and the writer [derived]

`FUN_00449240(message)` (`47869–47904`; listing `00449240–0044929d`):

```text
if newsIndex == 39:                       // full
    for i = 1 … 39: slot[i-1] = slot[i]   // REP MOVSD ×15 + MOVSB = 61 bytes, the whole slot, residue included
newsIndex = min(39, newsIndex + 1)
StrCopy(slot[newsIndex], message)         // writes text + NUL; bytes after the NUL are left as they were
```

- `slot[i]` is at `0x49F994 + 61 i`, `i = 0 … 39`. `newsIndex` (`DAT_004A031E`, signed 16-bit) is the index of the newest slot. It is `−1` for an empty log and `39` once full.
- There is no head pointer and no wrap-around. Display order is slot order, oldest first.
- **No truncation and no length check.** `StrCopy` copies up to the NUL, however long the message is. Every caller builds its message with `StrCopy`/`StrCat` in a 61- to 64-byte stack buffer. The limit therefore comes from the templates and the names in the DAT; the writer adds none. A 61st character would run into the next slot, or past slot 39 into `0x4A0318`.
- **Encoding.** Delphi's single-byte `Char`, one byte per character, drawn through the ANSI GDI path. Nothing converts code pages. The only transform is the ASCII-only `StrUpper` used for war declarations (Q2). The runtime code page is whatever the system ANSI page is, Windows-1252 on a Western install. It cannot matter in practice, because the DAT's names contain no byte ≥ 0x80 (all 16 nations ≤ 10 characters, all 334 cities ≤ 13, all 192 leader names ≤ 21).

Every other reference was found by a raw byte scan of the `CODE` section, not from the decompiler's cross-references. There are exactly **24** `E8` calls to `0x449240`, the same 24 as in the dump. The immediate `0x49F994` appears only in the DAT loader (`0x448493`), save (`0x448610`), load (`0x4488F8`), the writer and `TInformation_PaintForm`. `0x4A031E` is written only by the load, the new-game init (`0x448B08`) and the writer. So `FUN_00449240` is the only path that adds news.

`TInformation_PaintForm` (`40466–40687`) draws slots `0 … newsIndex` top to bottom, 16 px per line, and `TInformation_PrintNews` (`40729`) scrolls to the bottom. Nothing in the display treats any line specially. The same panel's "info" mode uses a second 40 × 61 array directly before the news, at `0x49F00C` (`DAT_004A031C` is its index). That array is never saved.

### The DAT seeds the log, and a new game starts at index 26 [confirmed]

The DAT loader reads the **last 2,440 bytes of the DAT (`0x21C1A`) straight into all 40 slots** (`news_log_decomp.txt` line 230: `Read(&DAT_0049f994, 0x988)`). The dev repo's `dat-file-layout.md` calls this a "static table". `FUN_00448AA4` then sets `newsIndex = 0x1A` (line 30). Slots 0–26 hold a scripted history, and slots 27–39 are zero:

```text
 0 272 BC                                  13 271 BC
 1 Tarrentum (Greece) falls to Rome.       14 Zela (Seleucid) falls to Bithynia.
 2 Croton (Greece) falls to Rome.          15 Synnada (Seleucid) falls to Galatia.
 3 Locri defects from Greece to Rome.      16 Laodicea defects from Seleucid to Media.
 4 Rhegium defects from Greece to Rome.    17 Helice (Celtiberia) falls to Carthage.
 5 Panormus defects from Greece to Carthage.   18 Chalcis defects from Greece to Macedonia.
 6 Mylae defects from Greece to Carthage.  19 Demetrias defects from Greece to Macedonia.
 7 Astacus (Seleucid) falls to Bithynia.   20 Marium defects from Greece to Ptolemaic.
 8 Heraclea (Greece) falls to Rome.        21 Sidon (Seleucid) falls to Ptolemaic.
 9 Thurii defects from Greece to Rome.     22 Marium defects from Greece to Ptolemaic.
10 Rome destroys army of Greece.           23 Pontica (Seleucid) falls to Bithynia.
11 Rome and Greece agree to end their war. 24 Damascus (Seleucid) falls to Ptolemaic.
12 " "                                     25 " "
                                           26 Week 1      Spring      270 BC
```

These lines are **scenario data, not EXE templates**. "*agree to end their war*", the single-spaced "*X (Y) falls to Z.*", the year lines and "*270 BC*" with a space appear nowhere in the EXE. A reimplementation must load them verbatim as the new-game log. It must not regenerate them.

**Seven saves are not yet full**, at index 27, 27, 27, 30, 31, 34 and 38 (`1.sav`, `1_cartago_271_spring_1.sav`, `1_cartago_271_spring_1b.sav`, `4.sav`, `1_thracia_271_spring_1.sav`, `_spring_3`, `_spring_5`). All seven reproduce byte for byte, residue included, by starting from the DAT's 40 slots at index 26 and applying the writer to their later lines.

### The SAV [confirmed]

`FUN_004484D0` (`47499–47508`) writes `int16 newsIndex`, then `newsIndex + 1` whole 61-byte slots, so the stale bytes after each NUL go into the file. Across the 54 saves:

| | Result |
| --- | --- |
| Layout `100,956 + 2 + A×656 + 2 + F×26 + 18,752 + 600 + 2 + (newsIndex+1)×61 + 55 = file length` | 54 of 54 |
| `newsIndex` | 39 in 47 saves; 27–38 in 7 |
| Slots read | 2,101 |
| Slots with a NUL within 61 bytes | 2,101 |
| Longest text | 59 bytes (the dash line); next longest 52 |
| Bytes outside 0x20–0x7E in text | 0 |
| Slots with non-zero bytes after the NUL | 1,117 (stale residue) |
| Consecutive full-log pairs re-derived by the shift + `StrCopy` model | 252 of 252 byte-exact |
| Partial logs re-derived from the DAT seed | 7 of 7 byte-exact |

The residue is just the slot's previous contents: the shift copies all 61 bytes, and `StrCopy` overwrites only up to the new NUL. Load (`FUN_004487C4`) reads `newsIndex + 1` slots and clears nothing beyond them. A port that zero-fills after the NUL shows identical text but writes a different file.

### The 6-byte gap, closed [confirmed]

[`mercenary-pool-record.md`](mercenary-pool-record.md) measured **3,042 bytes between the end of the nation table and the start of the 55-byte trailer**, constant in every save it checked. All of those saves had a full log. [`decompiled-sav-file-layout.md`](decompiled-sav-file-layout.md) then solved `3,042 = 600 + 2 + 55 + (n)×61`, which does not come out whole. But the 3,042 already excluded the trailer:

```text
3,042 = 600 (mercenaries) + 2 (newsIndex) + 40 × 61 (2,440)      exactly
```

The "~2,442 unidentified bytes" left over after the mercenary table in the mercenary report are `2 + 2,440`. The 55-byte trailer is fully named by the save code (`47509–47523`) and checks out on all 54 saves:

| Trailer offset | Bytes | Field | Check |
| ---: | ---: | --- | --- |
| `+0` | 32 | turn order, 16 × int16 (`DAT_0049EFE8`) | `order[turnIndex] == currentNation` in 54 of 54 |
| `+32` | 4 | pending offer: proposer, relation code (`DAT_0049F008`) | Q5 |
| `+36` | 2 | current nation (`DAT_004A0320`) | |
| `+38` | 2 | turn index into the order, 0–15 (`DAT_004A0322`) | |
| `+40` | 2 | week (`DAT_004A0330`) | equals the last header's week in 54 of 54 |
| `+42` | 2 | year BC (`DAT_004A0332`) | equals the last header's year in 54 of 54 |
| `+44` | 2 | season (`DAT_004A032E`) | equals the last header's season in 54 of 54 |
| `+46` | 8 | main-window geometry, UI state only | `(-8, -8, 1349, 2560)` on a maximised window |
| `+54` | 1 | battle-in-progress flag | 0 in all |

## Q2. The writer's formatting

### Every message is built by `StrCopy`/`StrCat` in the caller [derived]

No message uses `Format`. Each caller concatenates literals and name fields: nation name `0x474670 + n×0x494` (+0), leader name at nation `+0x0B`, and city name `0x479590 + c×0x22` (+0). Then it calls `FUN_00449240`. Two callers transform the text:

- **War declarations are shouted when a human is involved.** In `FUN_00449A44` (`48460–48466`), if the relation is war (3) and either nation's human flag (`+0x490`) is set, the whole message goes through `StrUpper`: "*ROME DECLARES WAR ON GAUL.*" Alliances are never uppercased. This is code-only: all 7 declarations in the saves are between AI nations, and they are lowercase.
- **The reparations amount** goes through `FUN_00448F3C` (`54143`).

### Numbers: a hand-written formatter with a fixed comma [derived, then confirmed]

Three routines, two of which the EXE's own leaked source names. Delphi left editor-buffer fragments in the EXE's slack space (file offsets `0xA07E0–0xA5E44`), including `FormStripNum1 (shipstot*10, numstr);` in `TBuildFleet` and `FormatNumber (pop, numstr)` / `FormStripNum (money, numstr)` in `THumanFalls`. `TBuildFleet_PrintNumbers` calls `FUN_00448F3C` for exactly those two ship quantities.

```text
FormatNumber  FUN_00448E74(n, buf)        // listing 00448e74–00448f06
    buf = 13 spaces + NUL
    if n < 0: buf[1] = '-'
    digits = Str(|n|)                       // System Str, no locale
    write digits from buf[3]; after each digit, if (remaining digits) mod 3 == 0
        and digits remain, write ','          // MOV byte ptr [EDI+EAX],0x2c at 00448ef0
FormStripNum  FUN_00448F18(n, buf)        // trailing spaces → NUL
FormStripNum1 FUN_00448F3C(n, out)        // also drops the leading pad:
    out = buf from index 3 (n ≥ 0) or from index 1 (n < 0)
```

- **The separator is the literal byte `0x2C`.** Nothing reads `ThousandSeparator` or the locale, so every machine prints `2,269`.
- Grouping is from the right in threes: `334`, `2,269`, `32,767`. A negative prints as `- 1,234`, with a space, because pad index 2 stays blank. No news message can be negative: the reparation is `random(W/4) + cities×10 + W/4`.
- **Only reparations are grouped.** Week and year go through plain `Str`, so there is no grouping and no padding: `Week  9`, `Week  11`, `270BC`.

Observed [confirmed]: "*Ptolemaic pays reparations of 2,242 talents.*" and "*… 2,269 talents.*", which are two distinct settlements, and "*… 334 …*", "*… 159 …*", "*… 998 …*". Five of five settlements are formatted as the code predicts.

## Q3. Date headers and blank lines

`FUN_004514EC` is the round tick. `TPremierForm_EndTurn` runs it after the 16th seat. It ends (`54677–54690`) with:

```text
news(" ")                                                        // one space, 0x20 — not an empty string
news("Week  " + Str(week) + "      " + seasonName[season] + "      " + Str(year) + "BC")
```

- It is called **once per completed round**, after the calendar has advanced (week `+2`), so the header names the week that is starting. Weeks are always odd: 1, 3, 5, 7, 9, 11. The spacing is "Week" + 2 spaces, then 6 spaces on each side of the season name, and no space before "BC". Season names are the DAT's season table at `0x1F7D8`: `Spring`, `Summer`, `Autumn`, `Winter`.
- **Both lines are ordinary writer calls and use up slots.** A quiet round costs 2 of the 40 slots.
- **They come after everything else in the tick.** Storm and loss-at-sea lines, fleet completions and the quarterly tick's deposed-leader lines all come first. So those lines appear under the *old* week's header. Everything a seat does in the new round follows the new header.

Confirmed in the saves:

| Check | Result |
| --- | --- |
| In-game header instances preceded by `" "` | 338 of 342 (about 44 distinct headers). The other 4 sit in slot 0, where the shift has already dropped the blank before them. |
| "*X depose their leader Y.*" directly before `" "` + header | 17 of 17 instances (2 distinct events) |
| Header text equals the trailer's week/season/year | 54 of 54 |
| Distinct `" "` entries | 46 (44 from ticks, 2 in the DAT seed) |

## Q4. Every news literal the EXE can emit

The 24 call sites, grouped by template. `N`, `A`, `B` are nation names, `C` a city name and `L` a leader name. Spacing is exact; each run of more than one space is written out in the notes.

```text
#   Function (lines)                      Template                                             Seen
1   FUN_00449A44 via FUN_00449B40 (48452)  A forms an alliance with B.                          4 events
2   FUN_00449A44 via FUN_00449B40 (48455)  A declares war on B.            (StrUpper if A or B human)  7 events
3   FUN_0044A050 (48782)                   N finishes a new fleet at C.                         —
4   FUN_0044AEE4 instant battle (49723)    A destroys army of B.                                24 events (with #21)
5   FUN_0044B27C capture (49818)           C   (A)  falls to B.                                 40 events
6   FUN_0044B27C capture (49829)           N fails to capture C   (A).                          14 events
7   FUN_0044B5D0 naval battle (49944)      A sinks fleet of B.                                  —
8   FUN_0044BD2C capital move (50279)      N have moved their capital to C.                     —
9   FUN_0044BED8 defection (50373)         C defects from A to B.                               18 events
10  FUN_0044C528 elimination (50728)       ----------------------------------------------------------- (59 dashes)
11  FUN_0044C528 (50730)                   A conquers B.                                        2 events
12  FUN_0044C528 (50736)                   (59 dashes again)
13  FUN_0044C8F0 AI deposed (50779)        N depose their leader L.                             2 events
14  FUN_00450C68 peace (54122)             A and B have agreed to end their war.                1 event
15  FUN_00450C68 (54130)                   B sues A for peace and;                              5 events
16  FUN_00450C68 (54135)                       B ends all current trading agreements.           5 events
17  FUN_00450C68 (54139)                       B  ends all current alliances.                   5 events
18  FUN_00450C68 (54144)                       B pays reparations of #,### talents.             5 events
    FUN_00450C68 (54176, 54192)            (#14 again, for each ally that also makes peace)
19  FUN_004514EC round tick (54595)        A fleet belonging to N is lost at sea.               2 events
20  FUN_004514EC (54602)                   A fleet belonging to N is damaged in a storm.        2 events
21  TBattleOver_OK tactical (57633)        A destroys army of B.                                (counted with #4)
22  FUN_004514EC (54677)                   " "  (a single space)                                44 events
23  FUN_004514EC (54679)                   Week  W      Season      YYYBC                       44 events
```

"Events" are distinct occurrences after removing the same event seen in several saves. The count is done by matching each line's preceding context, and is approximate for the most repeated lines. Notes, all **[derived]** from the code unless tagged:

- **#5, #6** have 3 spaces before `(`. #5 also has 2 spaces after `)`. The DAT seed's single-spaced form is scenario text only.
- **#16, #17, #18** start with 4 spaces. #17 has 2 spaces before "ends". #15 ends with "and;", semicolon included. #18's amount is `FormStripNum1` (Q2).
- **#10–#12:** an elimination always writes three slots, the banner between two 59-dash lines **[confirmed: 2 of 2]**.
- **#1–#2 cascade.** `FUN_00449B40` sets a relation and emits news only for alliance (2) and war (3). An alliance between A and B also makes A declare war on each nation at war with B. A declaration on B also makes A declare war on each of B's allies. Each of those gets its own "*A declares war on K.*" line, written directly after. **[confirmed: 4 of 4 alliance events are followed by A's cascade declaration, e.g. "Dacia forms an alliance with Rome." → "Dacia declares war on Gaul."]** Trade (1) and peace/cool-down (≤ 0) write nothing, so **a new trade agreement is never in the news**.
- **#13** is AI-only. `FUN_00451B40` rolls it 1 in 9 per quarter for an indebted AI. For a human, `FUN_0044C8F0` opens the `THumanFalls` game-over form instead.
- **#15–#18** follow an instant battle 2 times in 5 when the loser's unity is above 500 and it holds more than 7 cities (`49728–49733`). `TBattlePols_Yes` is the path after a tactical battle **[confirmed: all 5 settlements come directly after "A destroys army of B."]**.
- Code-only, never observed: #3, #7, #8, the uppercase war form, and any "*have agreed*" line produced for an ally.

### Compared with the dev repo's `tests/fixtures/corpus.json` `newsMessage.*`

| Corpus id | Verdict |
| --- | --- |
| `fallsTo`, `failsToCapture`, `destroysArmy`, `sinksFleet`, `honourablePeace`, `suesForPeace`, `endsTradingAgreements`, `endsAlliances`, `allyPeaceAgreement` | Exact. |
| `defectsFromObservedExample`, `conquersNationObservedExample` | The text is right, and the templates are now confirmed in code (#9, #11). But `conquers` never appears alone: it is always the middle of 3 slots between two 59-dash lines. |
| `paysReparations` | The text is right. `N` must be printed comma-grouped (`2,269`), not with `ToString()`. |
| `fleetLostAtSeaObservedExample` | **Wrong: missing the final period.** The literal is `" is lost at sea."` in both the EXE and the saves (4 slot instances). |
| `fleetFinished` | **Wrong: missing the final period.** The code does `StrCat(".")` (`48785`). |
| `victoryAllCities`, `conqueredByNation` | **Not news.** These are `THumanFalls_InitializeForm` labels on the game-over form (`56398–56416`). They never reach `FUN_00449240`. |
| `pendingDiplomaticOfferParaphrase` | **Not news** (Q5). The exact dialog text is `X wants to trade with Y.` / `X wants to form an alliance with Y.`, period included. |
| *(missing)* | #1 alliance, #2 war (plus its uppercase rule), #8 capital, #10/#12 dash line, #13 depose, #20 storm, #22 blank `" "`, #23 week header, and the 27-line DAT seed. |

## Q5. Pending trade and alliance offers: a dialog, never news

### The code [derived]

The offer is rolled and announced in one step, at the start of each **human** seat's turn. `FUN_00451FDC` runs the AI seats and calls `FUN_00452034` when it reaches a human (`54941–54957`). `TPremierForm_NewGame` does the same.

```text
FUN_00452034 (54962–55039):
    offer = (−1, ·)                                   // cleared every human turn start, accepted or not
    r = Random(16)
    if relation[human][r] == 0 and r alive and Random(3) == 0 and r is AI:
        possibly offer = (r, 1)                        // trade, from a tax-base comparison
        possibly offer = (r, 2)                        // alliance, overrides trade
    TPremierForm_StartTurn()
    (debt / unity check → FUN_0044C8F0 → game over for a human)

TPremierForm_StartTurn (58175–58235):
    ... SelectNation, PrintNews, OpenAllForms ...
    if offer.nation ≥ 0 and relation[current][offer.nation] != offer.type:
        s = name[offer.nation] + " wants to " + ("trade" | "form an alliance") + " with " + name[current] + "."
        MessageDlg(s, mtInformation, [mbOK], 0)        // FUN_0042D750, DL = 2, CX = [0x45AE64] = 0x0004
```

- `FUN_0042D750` is `Dialogs.MessageDlg` (→ `MessageDlgPos(…, −1, −1)` → `CreateMessageDialog`). The same routine shows "*Are you sure you want to quit ?*" (with `mtConfirmation`) and "*You can only trade with 3 nations.*". The string pool at `0x45AE30` holds `trade`, `form an alliance`, ` wants to `, ` with `, `.`, and then the button-set word `04 00`, which is `[mbOK]`.
- `StartTurn` never calls `FUN_00449240`, and none of the 24 calls is on this path.
- **Loading a save re-announces the offer.** `TPremierForm_OpenGameFile` calls `StartTurn` directly, not `FUN_00452034`, so a loaded offer is shown again rather than re-rolled. It is not shown if the player accepted before saving, because then the relation equals the offer.
- **Accepting does not clear it.** The offer's only other reader is `TPolitics_MakeTrade` (`55225–55231`), where a pending trade offer from that nation waives the three-partner limit. Nothing else writes the block except the reset at the next human turn start. No code path reads an alliance offer again after the dialog.
- AI seats never receive offers. The recipient is always the human whose turn is starting, which is why the block needs no recipient field.

### The saves [confirmed]

| Save | Block | Dialog text the code builds | Note in `notes/` | News slots with "wants" |
| --- | --- | --- | --- | ---: |
| `1_rome_270_autumn_5.sav` | Media, 1 | Media wants to trade with Rome. | `1_rome.txt`: "*Media wants to trade with Rome*" | 0 |
| `1_rome_270_winter_9_b.sav` | Greece, 1 | Greece wants to trade with Rome. | `2_rome_s.txt` | 0 |
| `1_rome_270_winter_11.sav` | Bithynia, 1 | Bithynia wants to trade with Rome. | `3_rome.txt` ("*Bythinia*", the user's spelling) | 0 |
| `1_thracia_271_spring_7.sav` | Ptolemaic, 1 | Ptolemaic wants to trade with Thracia. | — | 0 |
| `1_thracia_271_spring_11.sav` | Armenia, 1 | Armenia wants to trade with Thracia. | — | 0 |
| `1_thracia_271_summer_9.sav` | Rome, 1 | Rome wants to trade with Thracia. | — | 0 |

In all six, the recipient is the save's current nation and the current relation is 0. No slot among the 2,101 contains "wants". The three notes recorded what the dialog said. An alliance offer (`2`) is written by the code but has never been observed.

## What an implementation needs

- **Storage:** 40 slots, oldest at index 0, shifted down when full. The text is at most **60** single-byte characters; the 61st byte of the slot is the NUL. The index is the newest slot, `−1` when empty.
- **Truncation:** none in the original, and no message reaches 60 with the shipped names. The longest possible is the 59-dash line. Next are "*fails to capture*" at 56 and "*have agreed*" / "*damaged in a storm*" at 54. A port should reject anything over 60 bytes, or cut at 60. It must never keep 61 characters. Count bytes in a single-byte code page, not UTF-8.
- **Numbers:** only the reparations amount is grouped, with a comma every three digits regardless of locale.
- **Round tick:** after every other message in the tick, append `" "` then `"Week  {w}      {Season}      {year}BC"`.
- **War declarations** that involve a human are uppercased in full (ASCII `a–z` only). The cascade declarations follow the same rule. Alliance lines are never uppercased.
- **New game:** the log is the DAT's 27 seeded lines, with index 26.
- **Diplomatic offers are a turn-start dialog, not a news event.** Clear at every human turn start, roll, show once, and show again on load.
- **Byte-exact saves only:** write whole 61-byte slots including residue. This is the only place the residue matters.

## Corrections to existing reports

- [`decompiled-news-log-identified.md`](decompiled-news-log-identified.md): the slot layout and the 6-byte gap are closed above. It is right that capture, defection and battle messages go through `FUN_00449240`. So does every other news line, including the week header and the blank line: 21 templates in all.
- [`decompiled-sav-file-layout.md`](decompiled-sav-file-layout.md): the reconciliation gap was the trailer counted twice. The "2+2+2+2 unidentified" fields are turn index, week, year and season. The 8-byte "calendar/turn block" is window geometry.
- [`mercenary-pool-record.md`](mercenary-pool-record.md): the "~2,442 unidentified bytes" are the news index plus 40 slots.
- [`one-turn-save-comparison.md`](one-turn-save-comparison.md): the added blank slot is the round tick's `" "` separator.
- [`decompiled-turn-and-calendar-sequencing.md`](decompiled-turn-and-calendar-sequencing.md) and [`pending-offer-block-army-split-and-naupactus.md`](pending-offer-block-army-split-and-naupactus.md): "announces" means a `MessageDlg`, not a news line. `FUN_00452034` sets the block, and the code writes `2` for alliances.
- [`fleet-owner-field-confirmed.md`](fleet-owner-field-confirmed.md) quotes the lost-at-sea line without its final period. [`decompiled-unit-map-orders-and-record-fields.md`](decompiled-unit-map-orders-and-record-fields.md) quotes the fleet-completion line without its period.
- [`decompiled-diplomacy-peace-terms-and-instant-battles.md`](decompiled-diplomacy-peace-terms-and-instant-battles.md): the `N` in "*pays reparations of N talents*" is comma-grouped.

## Still open

- **An uppercase war declaration** has never been saved. Declaring war on anyone as Rome, then saving, would show "*ROME DECLARES WAR ON …*".
- **An alliance offer** (`offer.type = 2`) and its dialog text have not been observed.
- "*finishes a new fleet at*", "*sinks fleet of*" and "*have moved their capital to*" are code-only so far.
- `FUN_00452034`'s trade/alliance decision rule was read only as far as needed here. It is AI decision code.

## Reproduction

- **Writer and callers:** `FUN_00449240` `47869`, and the 24 calls listed in Q4. The raw `E8` scan of the `CODE` section (file `0x400` → VA `0x401000`) finds exactly 24 calls to `0x449240`.
- **Formatter:** `FUN_00448E74` `47544`, `FUN_00448F18` `47581`, `FUN_00448F3C` `47596`. The leaked source is in the EXE at file offsets `0xA07E0–0xA5E44`.
- **Offer:** `FUN_00452034` `54962`, `TPremierForm_StartTurn` `58175`, `TPolitics_MakeTrade` `55190`, `FUN_0042D750` `31768`.
- **New dumps:** `analyzeHeadless <ReTools>\ghidra_projects IC2 -process "Imperial Conquest 2.exe" -noanalysis -readOnly -scriptPath <ReTools>\scripts -postScript ExportAddresses.java news_log_decomp.txt 00448aa4 004481a0 -postScript DumpListing.java news_log_listing.txt 0x00449240 0x00448e74 0x00448f18 0x00448f3c 0x0045ac5c`.
- **Saves:** a direct Python reader over all 54 local saves, at the offsets in the Q1 table. It checks the layout, re-derives every overlapping pair and the 7 partial logs from the DAT seed, and reads the trailer. Nothing was written to either repository by it.
