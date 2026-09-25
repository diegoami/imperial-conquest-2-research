# The war cascade is one step deep, and an AI never ends a war with a human on its own

**The questions** (dev-repo bugs [#383](https://github.com/diegoami/imperial_conquest_2/issues/383) and [#384](https://github.com/diegoami/imperial_conquest_2/issues/384), both from T82's review of PR #377):

- **#383.** When the relation setter `FUN_00449B40` declares a war or forms an alliance, how far does the cascade reach? Does it write the dragged-in wars directly, or call itself again?
- **#384.** By which paths can peace, or a cooldown, be written between an AI nation and a human nation? Is the human's consent needed on each path? Can an AI end a war with a human without it?

## Answer

- **The cascade is one step and does not recurse.** The setter writes each dragged-in war straight into the matrix (both cells) and calls only `FUN_00449A44`, a nested procedure that formats one news line. Nothing in the setter calls the setter. A whole-program byte scan finds 22 calls to `FUN_00449B40`, none inside it, and 4 calls to `FUN_00449A44`, all from the setter **[confirmed: listing + byte scan]**.
- **The engine recurses, and the original does not.** `RelationTransitions.DeclareWar` calls itself for each dragged-in ally, and `FormAlliance` routes its cascade through `DeclareWar`. Its doc comment says "the original's own `FUN_00449B40` is one function calling itself". That premise is false. In a chain of alliances A–B–C–D, a war on A reaches B only in the original, and B, C and D in the engine (§1.4).
- **No AI path ever writes peace over a war with a human.** The AI's diplomacy (`FUN_0044FB7C`) never writes peace over a war, with anyone. The offer roll never offers peace. The instant resolver's treaty is AI-vs-AI only **[confirmed: code]**.
- **A human–AI war ends in only two ways.**
  - **The post-battle treaty, which needs the human's Yes.** After a tactical battle, `TBattleOver_OK` may open the `TBattlePols` dialog, and only `TBattlePols_Yes` calls the treaty **[confirmed]**. The dialog's gate makes this treaty always the honourable one, with no reparations (§2.3) **[derived]**.
  - **Elimination of either side,** which resets every relation of the eliminated nation. Nobody chooses it **[confirmed]**.
- **The human's own Politics screen cannot end a war with an AI** ("*X does not want to make peace at this time.*"). It can end a trade or an alliance with an AI at will **[confirmed: listing]**.
- **Three writes do touch a human without consent, and none of them ends a war:**
  - an AI drops its trade with a human when it can swap to a richer AI partner;
  - a treaty breaks the winner's alliance with a human ally (−8) and leaves the human at war;
  - the honourable treaty also breaks the loser's alliance with a human ally.

  §2 has the table **[confirmed: code]**.
- **The neighbour-mask report's note on the treaty's ally loop is right, and there is more to it.** The winner's alliance with each ally still at war with the loser is written to **−8**, and the write has no gate. Only after that does the loop test the border and the human flag. The mirror half, for the loser's allies, can fire only in the honourable branch (§3) **[confirmed: listing]**.
- **Also found: the treaty reseeds the RNG.** `FUN_00450C68` and `TBattlePols_InitializeForm` both set Delphi's `RandSeed` to `winner + loser` before drawing `Random(W/4)`. So the preview and the payment always agree (§4) **[confirmed: listing]**.

## 1. The setter's cascade (#383)

### 1.1 `FUN_00449B40(a, b, state)`, `0x00449B40`, dump :48472–48546 `[confirmed: listing]`

`a` is in `[EBP-2]` (from `AX`), `b` in `EDI` and the state in `[EBP-4]`. The nation table starts at `0x474670`, with stride `0x494` (`IMUL …,0x125` then `*4`). The relation row is at `+0x26`.

| Address | Instructions | What it does |
| --- | --- | --- |
| `0x00449B53`–`B94` | `CMP [EBP-4],0`; `DEC AX` ×3 | state `0` becomes `−8`, `−24` or `−18` from a current trade, alliance or war; otherwise it stays `0` |
| `0x00449BB2`, `0x00449BC8` | two `MOV word ptr` | writes `rel[a][b]` and `rel[b][a]` |
| `0x00449BCD`–`BDB` | `CMP [EBP-4],2`; `PUSH EBP`; `MOV DX,2`; `MOV EAX,EDI`; `CALL 0x00449A44` | alliance: news "*a forms an alliance with b.*" |
| `0x00449BEF`–`C4D` | loop `ESI = 0…15`: `CMP rel[b][k],3`; `CMP rel[a][k],3; JZ`; `MOV word ptr rel[a][k],3`; `MOV word ptr rel[k][a],3`; `CALL 0x00449A44` (`DX = 3`, `EAX = k`) | every `k` at war with `b` that `a` is not at war with: **two direct stores of `3`**, then the news line "*a declares war on k.*" |
| `0x00449C4F`–`C5D` | `CMP [EBP-4],3`; `CALL 0x00449A44` (`DX = 3`, `EAX = b`) | war: news "*a declares war on b.*" |
| `0x00449C71`–`CCF` | loop `k = 0…15`: `CMP rel[b][k],2`; `CMP rel[a][k],3; JZ`; two `MOV word ptr …,3`; `CALL 0x00449A44` | every ally `k` of `b` that `a` is not at war with: **two direct stores of `3`** and a news line |
| `0x00449CD1`–`CD7` | `RET` | — |

There is no `CALL 0x00449B40` anywhere in the setter's body. The cascade's wars are plain stores. They do not map a cooldown, they emit no "forms an alliance" line, and they start **no further cascade**.

### 1.2 `FUN_00449A44`, `0x00449A44`, dump :48439–48470: a news line and nothing else `[confirmed: listing]`

This is a Delphi **nested procedure**. The setter pushes its own frame pointer (`PUSH EBP` before each call, `POP ECX` after), and the callee reads the setter's `a` at `[[EBP+8] − 2]` (`0x00449A50`–`A53`). The procedure then:

1. Builds "*`<a>` forms an alliance with `<k>`.*" (`DX = 2`) or "*`<a>` declares war on `<k>`.*" (`DX = 3`).
2. For a war, upper-cases the whole line through `FUN_00405C98` if `a` or `k` is human (`+0x490`, `0x00449ABF`–`AE7`).
3. Calls the news writer `FUN_00449240`.

Its only calls are the string helpers `0x00405B00`/`0x00405BC8`/`0x00405C98` and `0x00449240`. **It writes no relation.**

### 1.3 The complete call graph `[confirmed: byte scan]`

A Ghidra post-script (`ScanCalls.java`) scanned every executable byte for `E8 rel32` calls. It does not depend on Ghidra having disassembled the region, which matters because `TPolitics_OK` and `TBattlePols_Yes` sit in an undisassembled gap and `FindXrefs` misses them.

- **`FUN_00449B40`, 22 callers.**
  - `TUnitMap_SelectUnit`: `0x0044682D`, `0x00446916`, `0x00446B00`.
  - `FUN_0044BED8`: `0x0044C149`.
  - `FUN_0044C360`: `0x0044C450`.
  - `FUN_0044C528`: `0x0044C68B`.
  - `FUN_0044C8F0`: `0x0044C9FF`.
  - `FUN_0044FB7C`: `0x0044FD0C`, `0x0044FD47`, `0x0044FE5A`, `0x0044FEEF`, `0x0044FF7E`, `0x0044FF8F`.
  - `FUN_00450C68`: `0x00450D72`, `0x00450F3F`, `0x00450FBF`, `0x00450FE8`, `0x0045106C`, `0x00451095`.
  - `FUN_00451B40`: `0x00451FB5`.
  - `TPolitics_OK`: `0x004532B8`, `0x00453338`.

  This is the same set of 22 that [decompiled-ai-offers-to-human-seats.md](decompiled-ai-offers-to-human-seats.md) counted in the decompile.
- **`FUN_00449A44`, 4 callers**, all in the setter: `0x00449BDB`, `0x00449C38`, `0x00449C5D`, `0x00449CBA`.
- **`FUN_00450C68`, 2 callers:** the instant resolver `FUN_0044AEE4` (`0x0044B20A`) and `TBattlePols_Yes` (`0x00457C71`).

A caller can still call the setter several times in a loop (`TPolitics_OK` walks the human's whole row, and elimination resets all 16 columns). Each of those calls cascades one step on its own. Nothing re-enters.

### 1.4 Worked examples

**A chain of alliances.** A–B, B–C and C–D are allied. X is at peace with all four and declares war on A.

| | Original (`FUN_00449B40(X, A, 3)`) | Engine (`DeclareWar(X, A)`) |
| --- | --- | --- |
| X–A | war | war |
| X–B | war (A's ally) | war (A's ally) |
| X–C | **peace** | war: `DeclareWar(X, B)` recurses into B's ally C |
| X–D | **peace** | war: `DeclareWar(X, C)` recurses into C's ally D |
| News | "X declares war on A." / "X declares war on B." | the same two, then "X declares war on C." / "X declares war on D." |

The original therefore leaves B at war with X while B is still allied to C, and C at peace with X. Nothing later corrects that. The AI's own turn has no "join an ally's war" rule, and its alliance pick only allies **with** a nation's enemy ([decompiled-ai-offers-to-human-seats.md](decompiled-ai-offers-to-human-seats.md) §1a) `[original: confirmed; engine: read from RelationTransitions.cs:211–244]`.

**The alliance cascade.** A is at war with X, and X is allied to Z. Y forms an alliance with A.

- **Original:** Y–A allied, and Y goes to war with X ("*Y declares war on X.*"). Z is untouched. The alliance cascade drags in the partner's enemies, never those enemies' allies.
- **Engine:** `FormAlliance` calls `DeclareWar(Y, X)`, which recurses into X's ally Z, and so on down Z's own allies. Y ends at war with X, Z and the rest of that chain.

**Verdict:** the engine's recursion is wrong against the original, in both `DeclareWar` and `FormAlliance`'s use of it. The engine should write the one-step wars directly: a `WithRelation(…, War)` plus the war news line, with no nested call, for exactly the `k` the loops in §1.1 select. The guard stays the same (`rel[a][k] != 3`, evaluated live). The engine's news shouting rule already matches `FUN_00449A44`.

## 2. Every peace path between an AI and a human (#384)

| # | Path | Pair written | Human consent | Gate | News |
| --- | --- | --- | --- | --- | --- |
| 1 | Human's Politics screen, `TPolitics_MakePeace` → `TPolitics_OK` | human–AI: trade → −8, alliance → −24 | the human's own act | target not self, unity > 0; **refused if the target is AI and at war** | none |
| 2 | AI trade swap, `FUN_0044FB7C` :53444 | AI–(human trade partner) → −8 | **none** | a richer AI `k` at peace with fewer than 3 partners | none |
| 3 | Post-battle treaty, `TBattleOver_OK` → `TBattlePols` → `FUN_00450C68` | human–AI war → −18; human–enemy's AI allies → −8; human's own alliances → −8 | **yes: the Yes/No dialog** | human-involved battle; `armies(W) < armies(L)`, `unity(L) > 500`, `cities(L) > 7`, `Random(5) < 2` | honourable line + ally lines |
| 4 | AI–AI treaty's ally loop, `FUN_0044AEE4` → `FUN_00450C68` | (AI winner)–(human ally) alliance → −8; also the loser's human ally, honourable only | **none** | the human is allied to one side and at war with the other | none for the human |
| 4b | AI–AI treaty, sues branch | loser AI–(human trade or alliance partner) → −10 | **none** | the treaty took the sues branch | "*L ends all current trading agreements / alliances.*" |
| 5 | Elimination, `FUN_0044BED8` :50390 and `FUN_0044C528` :50677 | eliminated–everyone: war → −18, other cooldowns → 0 | none | the nation is eliminated | only the "defects"/"conquers" banner |
| 6 | Leader falls, `FUN_0044C8F0` :50811 | fallen nation–anyone, −5…−1 → 0 | none | deposition | none for the relations |
| 7 | Rebirth, `FUN_0044C360` :50558 | reborn–(each defecting city's owner) → −8 | none | rebirth | none for the relations |
| 8 | Quarterly thaw, `FUN_00451B40` :54925 | cooldown → towards 0 | none | negative entries, first 8 columns | none |

Rows 5–8 never turn a war into peace **by anyone's decision**. Row 5 ends a war only because one side has ceased to exist, and rows 6–8 only move an existing cooldown. **Only row 3 ends a live human–AI war, and it needs the human's Yes** `[confirmed: all 22 setter calls in §1.3 classified]`. No code writes the relation matrix outside the setter except the rebirth's own row reset (:50548) and `TPolitics_OK`'s diagonal (:55390) `[confirmed: decompile]`.

### 2.1 The human's Politics screen `[confirmed: listing]`

`TPolitics_ChangeIR` (`0x00452C9C`) decodes the clicked cell. It returns early if the target is the human itself (`0x00452CDC`), if the value is unchanged (`0x00452CE8`), or if the target's unity is ≤ 0 (`0x00452CFB`). A click on "peace" calls `TPolitics_MakePeace` (`0x00452D21`).

`TPolitics_MakePeace` (`0x00452D94`, dump :55148):

```text
0x00452DB3–DC4  if human[target] == 0                            // +0x490 via 0x474B00
0x00452DC6–DE0     and rel[me][target] == 3 (committed matrix):
0x00452DE2–E22        MessageDlg("<target> does not want to make peace at this time.", mtInformation, [mbOK])
                       // DL = 2; nothing else happens
0x00452E29–E34  else if working[target] > 0: working[target] = 0   // form +0x384
```

`TPolitics_OK` (`0x00453230`, :55335) commits every changed cell through the setter. A cell goes through if the committed value is ≥ 0 or the new value is war (:55380–55385). `0` then becomes the cooldown for the old state. The setter writes news only for alliance and war (§1.2), so **ending a trade, an alliance or a hotseat war from this screen writes no news line**.

To sum up: against an AI, the human can end a trade (→ −8) or an alliance (→ −24) and cannot end a war. Against another human, all three are accepted. The engine's `MakePeaceCommandHandler` accepts war only (`NotAtWar` otherwise), so it has no route for the human to end a trade or an alliance. This report did not check whether another engine command covers that.

### 2.2 The AI's own turn never makes peace from war `[confirmed: decompile, :53296–53455]`

`FUN_0044FB7C` has six setter calls: trade at :53364 and :53427, war at :53375, alliance at :53404, and the swap pair at :53444–53445. The war-candidate loop only considers `0 ≤ rel < 3`, so an existing war is never revisited. **The AI never writes peace over a war, with an AI or with a human.** AI–AI wars end only through the instant resolver's treaty or through elimination.

Its one state-0 write is the **trade swap** at :53444:

```text
for each s with rel[me][s] == 1:                       // s: any trade partner, human or AI
    for k != me with unity[k] > 0, rel[me][k] == 0, taxBase[s] < taxBase[k],
                     trades(k) < 3, human[k] == 0:     // only k is tested for being AI
        setRelation(me, s, 0)                           // trade → −8, no news
        setRelation(me, k, 1)
```

The swap tests only the **new** partner `k` for being AI (`psVar7[0x28]` = `+0x490`), never the dropped partner `s`. A human can open a trade with an AI unilaterally (`TPolitics_MakeTrade` has no willingness test). So the AI can later drop that trade on its own turn, without news or consent, and leave a −8 cooldown `[confirmed: decompile]`. The earlier report's summary "the other callers … write only peace or cooldowns" is correct. This is the one peace-type write inside `FUN_0044FB7C` itself.

The offer roll `FUN_00452034` offers only trade (1) or alliance (2) ([decompiled-ai-offers-to-human-seats.md](decompiled-ai-offers-to-human-seats.md) §1b). **There is no AI peace offer of any kind, not even a notice.**

### 2.3 The post-battle treaty: the human's Yes, and always honourable

**Where the dialog comes from** `[confirmed: listing of TBattleOver_OK 0x00459220, dump :57566–57684]`. `TBattleOver_OK` closes a tactical battle, and a tactical battle happens only when a human is involved (`FUN_0044AEE4` sends AI-vs-AI fights to the instant resolver). It:

1. applies the result;
2. writes "*W destroys army of L.*";
3. sums `FUN_0044A8CC` over each side's remaining armies: winner `bc6` into `EDI`, loser `bc8` into `[ESP+8]`, at `0x0045940A`–`9447`;
4. stores the pair in `DAT_004A0328` / `DAT_004A032A` (`0x00459449`–`945B`);
5. picks one of two dialogs:

```text
0x00459461–948D  if both sides are human:  show THVHBatPols (0x457CD0)      // money only, see below
0x004594DC       else if armies(W) < armies(L)                               // CMP EDI,[ESP+8]; JGE skip
0x004594E6–94FD       and unity[L] > 500                                     // CMP …,0x1F4; JLE skip
0x004594FF–9515       and cities[L] > 7                                      // CMP …,7; JLE skip
0x00459517–9524       and Random(5) < 2:                                     // drawn only if the three pass
0x0045955A–9569           show TBattlePols (0x457600)
```

A dword scan finds `0x457600` (the `TBattlePols` class) at two addresses only `[confirmed: ScanDword]`. One is this `MOV EDX` at `0x00459560`. The other, `0x004577D1`, lies in the class's own data just before `TBattlePols_InitializeForm` `[derived]`. So this is the **only** place the peace dialog is ever shown.

**The dialog is the consent** `[confirmed: decompile :56987–57124]`. `TBattlePols_InitializeForm` words the offer for the human's side:

- "*After defeating you in battle `<W>` are willing to end …*" when the winner is AI;
- "*After losing to you in battle `<L>` are willing to end …*" when the winner is human.

The dialog previews the terms. `TBattlePols_Yes` calls `FUN_00450C68(W, L)` (`0x00457C71`) and closes with `ModalResult 6`. `TBattlePols_No` sets `ModalResult 7` and does nothing else, so the war goes on. **An AI can offer a human peace only here, and only a Yes writes it.**

**Always honourable** `[derived]`. The treaty takes the sues branch only if `score(W) ≥ score(L)` **and** `armies(W) ≥ armies(L)` (`0x00450D77`–`0D88`, with `[ESP]` = winner's armies and `[ESP+4]` = loser's). The dialog is shown only if `armies(W) < armies(L)`. The same sums are recomputed from the same army records, and nothing can move between the gate and Yes except a modal dialog. So a treaty reached through `TBattlePols` always writes "*W and L have agreed to end their war.*" and pays nothing. The dialog's "*You/They will pay reparations of …*" lines are therefore unreachable in play. Reparations happen only between two AIs, which matches the one observed payment (Ptolemaic, AI–AI).

**Human versus human.** `THVHBatPols_OK` (:57334) moves the agreed money and writes **no relation**, so a hotseat battle never makes peace `[confirmed: decompile; no setter call in §1.3]`.

### 2.4 The AI–AI treaty's effect on humans `[confirmed: listing]`

The instant resolver calls the treaty for AI-vs-AI battles only (:49729–49733). The draw is `Random(5)` **first**, then `unity(L) > 500 && cities(L) > 7`. There is no armies test, so both branches are reachable. The human is never the winner or the loser. The ally loop (§3) can still touch the human:

- A human **allied to the winner** and at war with the loser has its alliance with the winner written to **−8**. The human is then excluded from the peace, so it stays at war with the loser. No line is written for either change.
- A human **allied to the loser** and at war with the winner (honourable branch only) has its alliance with the loser written to −8, and stays at war with the winner.
- In the sues branch, the loser's trades and alliances with everyone, humans included, go to **−10**. The only news is the loser-wide "*… ends all current trading agreements.*" / "*… ends all current alliances.*" lines.

## 3. The treaty's ally loop, re-checked `[confirmed: listing 0x00450F79–0x004510F8]`

`EBP` is the winner and `EDI` the loser (`0x00450C6F`–`0C71`; `TBattlePols_Yes` passes `DAT_004A0328` first, and the instant resolver passes the army that won). `ESI` walks nation `k`'s `+0x46`.

```text
for k in 0..15:
    if rel[W][k] == 2 and rel[L][k] == 3:                 // 0x00450F8A–0FAE
        setRelation(W, k, -8)                             // 0x00450FB4–0FBF  — ungated
        if !bit(mask[k], L) and human[k] == 0:            // 0x00450FC4–0FDB  BT [ESI]; [ESI+0x44A] = +0x490
            setRelation(L, k, -8)                         // 0x00450FDD–0FE8
            news("<L> and <k> have agreed to end their war.")   // 0x00450FED–1032
    if rel[L][k] == 2 and rel[W][k] == 3:                 // 0x00451037–105B
        setRelation(L, k, -8)                             // 0x00451061–106C  — ungated
        if !bit(mask[k], W) and human[k] == 0:            // 0x00451071–1088
            setRelation(W, k, -8)                         // 0x0045108A–1095
            news("<W> and <k> have agreed to end their war.")   // 0x0045109A–10DF
```

- **The note in [dat-neighbour-mask.md](dat-neighbour-mask.md) §5 is confirmed.** An ally makes peace alongside its partner only if it does not border the enemy and is not human. The partner's alliance with that ally is reset first, with no gate.
- **The reset is to −8, not −24.** The setter maps only state `0` to a cooldown, and a non-zero argument is stored as given (§1.1). So every ally of the winner that is at war with the loser **loses the alliance**, bordering or not, human or not. A bordering or human ally loses the alliance **and** stays at war.
- **The mirror half is dead in the sues branch.** That branch has already written −10 over every alliance of the loser (:54152–54159, `0x00450F3F`), so `rel[L][k] == 2` never holds by the time the loop runs.
- **The name order** is `<enemy> and <ally>`: the loser first for the winner's allies, the winner first for the loser's allies.
- **Intent.** The ungated reset reads like a deliberate "an ally that keeps fighting leaves the alliance". It also dissolves the alliance of an ally that did make peace, which is harder to read as intent. Whether it is a bug is not argued here `[hypothesis]`. A faithful reimplementation reproduces it either way.

The engine's `PeaceTreatySystem.ApplyAllyPeaceCascade` differs in four ways:

1. It never writes the partner–ally −8.
2. It has no border or human gate.
3. It names the ally first (`PeaceAllyAgreement(allyName, otherName)`), where the original names the enemy first.
4. It writes all the winner-side lines before the loser-side ones. The original interleaves them per `k`.

## 4. Also found: the treaty reseeds the RNG `[confirmed: listing]`

`0x00450C73`–`0C7B`: `MOVSX EDX,BP; MOVSX EAX,DI; ADD EDX,EAX; MOV [0x0045E030],EDX`. `0x0045E030` is Delphi's `RandSeed`: `FUN_0040284C` is `Random(n)`, `seed = seed × 0x08088405 + 1; return (n × seed) >> 32` (:1585–1592). So **`RandSeed := winner + loser`** is set, and then `Random(taxBase(L) / 4)` is drawn, unconditionally and before the branch (`0x00450C9F`). `TBattlePols_InitializeForm` does the same (:57034) before computing the preview, so the previewed and the paid amounts are identical.

Two consequences follow `[derived]`:

- The reparation for a given pair and tax base is **deterministic**, and the unused draw happens in the honourable branch too.
- **Every treaty resets the global random stream**, so the draws that follow it in the same turn repeat from game to game.

The engine draws `rng.NextInt(share)` only in the sues branch and only when `share > 0`, and it does not reseed. That matters only if bit-exact random streams are a goal.

## 5. What the engine must change

1. **#383: remove the recursion.** `DeclareWar`'s cascade and `FormAlliance`'s cascade should write the dragged-in war directly, with its news line and no nested `DeclareWar`. A chain-of-four test pins it: war on A reaches A and B only. The doc comment claiming the original recurses should go.
2. **#384: the AI must not make peace with a human.** `AiDiplomacyPhase.ProposePeace` issues a `MakePeaceCommand` against a human target, and the handler's "human always accepts" branch then writes −18 directly. That branch is the original's hotseat rule, human to human. The original has **no** AI peace proposal to anyone. The faithful change is to remove it. If a design keeps an AI peace overture, it must be an offer the human accepts, and that is a design addition, not the original.
3. **#384: the human-involved treaty needs consent and the tactical gate.** `InstantBattleResolver` publishes `PeaceTreatyTriggered` for every battle on the AI–AI gate (`Random(5) < 2`, unity > 500, cities > 7). When a human is in the battle, the original:
   - also requires `armies(W) < armies(L)`;
   - draws `Random(5)` only after the other three tests pass;
   - asks the human Yes/No;
   - on Yes, always applies the honourable branch.

   Today the engine writes that treaty without consent, and it can charge a human reparations. The original never does either.
4. **The treaty's ally loop** (§3): add the ungated partner–ally −8, the neighbour-mask gate and the human exclusion. Order the names enemy first, and interleave the two halves per `k`.
5. **Optional fidelity:** reseed on each treaty (§4), and let the AI trade swap drop a human partner (§2.2), if the engine's AI trade logic is meant to follow `FUN_0044FB7C`.

## What this does not establish

- **No save or recording** shows a cascade reaching a second hop, or failing to. The one-step rule is from code. An in-game check would be three chained alliances, then a declaration.
- **No `TBattlePols` dialog has been observed.** The "always honourable" result is derived from two confirmed gates, and it assumes the dialog is modal: it sets `ModalResult` and is closed through `FUN_0042313C`.
- **Whether the engine has another command for a human to end a trade or an alliance** was not checked outside `src/IC2.Engine/Diplomacy/`.
- **Whether the ungated partner–ally −8 is intended** is not argued (§3).

## Reproduction

- **Decompile:** `%LOCALAPPDATA%\ReTools\all_app_functions.txt`:
  - the setter :48439–48546;
  - the AI's diplomacy :53296–53455;
  - the treaty :54049–54203;
  - `TPolitics_MakePeace` :55148, `TPolitics_OK` :55335;
  - `TBattlePols_*` :56987–57124, `THVHBatPols_OK` :57334, `TBattleOver_OK` :57566–57684;
  - the instant resolver's treaty call :49729;
  - the elimination, rebirth, leader-falls and thaw calls at :50390, :50558, :50677, :50811 and :54925.
- **Listings:** `analyzeHeadless <ghidra_projects> IC2 -process "Imperial Conquest 2.exe" -noanalysis -readOnly -scriptPath %LOCALAPPDATA%\ReTools\scripts`, then:
  - `-postScript DumpListing.java <out> 0x00449b40 0x00449a44 0x00452d94 0x00452c9c`;
  - `-postScript DumpListing2.java <out> 0x00450c68 0x00453230 0x00457c60 0x004577ec 0x00459220`. `DumpListing2` forces `disassemble()` first, because those functions sit in a gap the saved project never disassembled, and `DumpListing` prints them empty.
- **Call scan:** `-postScript ScanCalls.java 449b40 450c68 449a44 452d94` lists every `E8 rel32` whose target matches. `-postScript ScanDword.java 457600 457cd0` finds the form-class references. All three scripts are in `%LOCALAPPDATA%\ReTools\scripts`, outside both repositories.
- **Engine, read-only:** `src/IC2.Engine/Diplomacy/RelationTransitions.cs` (`DeclareWar`, `FormAlliance`), `PeaceTreatySystem.cs`, `Commands/MakePeaceCommand.cs`; `src/IC2.Engine/Ai/AiDiplomacyPhase.cs` (`ProposePeace`); `src/IC2.Engine/Battle/InstantBattleResolver.cs` (`peaceFired`).
- **Nothing from the game** (EXE, DAT or SAV) was copied into a repository.
