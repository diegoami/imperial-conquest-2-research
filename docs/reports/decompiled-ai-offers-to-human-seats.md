# AI offers to human seats: a notice, not a treaty; and the AI does not declare war on an ally

**The question** (dev-repo follow-up [#334](https://github.com/diegoami/imperial_conquest_2/issues/334)): when a computer nation proposes trade or an alliance to a human nation, what does the original do? Is the offer accepted automatically, or does the human decide? Can an AI nation then declare war on a nation it is allied to?

## Answer

- **The human decides, and nothing happens unless the human acts.** The "offer" is a roll made at the start of a human seat's turn (`FUN_00452034`). It stores `(proposer, 1 | 2)` in the pending-offer block and shows `"X wants to trade with Y."` / `"X wants to form an alliance with Y."` in an OK-only information box. The box's return value is thrown away, and no code writes the relation. To take the deal, the human opens the Politics screen and makes the trade or alliance there, under the ordinary `TPolitics_*` rules. Doing nothing lets the offer lapse: the next human turn start clears it. **[confirmed: code, instruction level; and 4 of 4 follow-up saves keep the relation at 0 after the offer is gone]**
- **The AI never forms a treaty with a human seat on its own.** Its per-turn diplomacy (`FUN_0044FB7C`) writes trade and alliance directly, but only with computer-controlled partners. Toward a human it can do two things only: declare war, or raise the turn-start notice above **[confirmed: code]**.
- **An alliance offer has no mechanical effect.** Nothing reads it after the dialog. A trade offer has one: in `TPolitics_MakeTrade` it waives the refusal when the **proposer** already has three partners. On OK, the proposer then drops its poorest partner **[confirmed: code]**.
- **The AI's own war rule never picks a current ally that holds a city.** The target must not be "protected by an ally", and the declaring AI counts as its own ally's ally. An alliance can still turn into war through the setter's cascade, and only in a narrow case (below) **[confirmed: code]**. Across 32 consecutive save pairs, none of 109 allied-pair observations turns into war **[confirmed: saves, consistent but not a proof]**.

## 1. Where AI diplomacy happens

`FUN_00451FDC` (`all_app_functions.txt` :54939) runs the computer seats one after another. For each it calls `FUN_0044FA20` (:53208), which calls `FUN_0044FB7C` (:53296) first if the nation's unity `+0x440 > 0`. When the loop reaches a human seat, it calls `FUN_00452034` (:54962). There are exactly two AI diplomacy paths, one per seat type.

### 1a. `FUN_0044FB7C`: an AI seat's own turn [confirmed: decompile, key compares checked in the listing]

`me` is the acting AI (`DAT_004A0320`). The helpers are:

- `FUN_0044FAA0(n)` (:53237) returns three things: `trades(n)`, the count of `1`s in n's row; `atWar(n)`, true if n's row holds any `3`; and `protected(n)`. `protected(n)` is true if n has an ally `a` with `cities[n] + cities[a] > cities[me]` (`+0x446`, compare at `0x0044FB1F`).
- `FUN_0044FB50(n)` (:53273) is the number of n's wars.
- `+0x46` is a 16-bit **neighbour mask**. This is a new identification, from saves: it is symmetric and geographic. Rome holds {Carthage, Gaul, Illyria}; Carthage holds {Rome, Ptolemaic, Numidia, Celtiberia}; Thracia holds {Macedonia, Dacia}. It was checked in `1_rome_270_winter_11.sav` and `1_thracia_271_summer_9/11.sav`. **[confirmed: saves; the name is derived]**
- The power is `P(n) = (wealth +0x430 / 20000) × (unity +0x440 / 100)`.

```text
busy(me) = atWar(me) or mobilization(me) > 40 or season == 3           // 0x0044FC26–0x0044FC53
for k in 0..15, k != me, unity[k] > 0, 0 <= rel[k][me] < 3:              // peace, trade or ALLIANCE
    if not busy(me) and not protected(k) and me in neighbours(k) and 8·P(me)/max(1,P(k)) > best:
        warTarget = k; best = ratio                                      // best starts at 10
    else if rel == 0 and trades(me) < 3 and trades(k) < 3 and k is AI:
        setRelation(me, k, TRADE)                                        // immediate, no consent step
if warTarget and Random(10) == 0: setRelation(me, warTarget, WAR); busy = true
if not busy and Random(20) == 0:                                         // alliance, AI partners only
    for j in neighbours(me) with 0 <= rel[me][j] <= 1, unity[j] > 0, not protected(j):
        for m: m is AI, rel[m][j] == 3, m != me, wars(m) < 2,
               cities[j] < cities[me] + cities[m], first match only:
            setRelation(me, m, ALLIANCE)                                 // cascade → war with j
for k: rel[me][k] == 0, unity[k] > 0, trades(me) < 3, trades(k) < 3, k is AI:  setRelation(me, k, TRADE)
for each partner s of me, for k with rel[me][k] == 0, taxBase[s] < taxBase[k], trades(k) < 3, k is AI:
    setRelation(me, s, 0) ; setRelation(me, k, TRADE)                    // swap a poorer partner
```

Every trade and alliance write checks that the partner is AI (`+0x490 == 0`, e.g. `0x0044FCF7`). The war write does not, so the AI declares war on humans directly. These are the only AI-originated writes of trade, alliance or war; the other callers (treaty `FUN_00450C68`, defection and elimination `FUN_0044BED8`/`FUN_0044C360`/`FUN_0044C528`/`FUN_0044C8F0`, the quarterly thaw) write only peace or cooldowns. The setter's callers that can pass `3` are exactly `TUnitMap_SelectUnit` ×3 (human UI), `TPolitics_OK` (human UI) and this one call at :53375 **[confirmed: all 22 decompiled `FUN_00449B40(` call sites in `all_app_functions.txt`]**. The "season 3 = Winter" reading is `[derived]` from the Spring = 0 and Summer = 1 observations.

### 1b. `FUN_00452034`: the offer roll at a human seat's turn start [confirmed: decompile + listing]

```text
h = current human seat
offer = (-1, ·)                                          // DAT_0049F008 = 0xFFFF
r = Random(16)
if rel[h][r] == 0 and unity[r] > 0 and Random(3) == 0 and r is AI:
    floor = (trades(h) < 3) ? 0 : min taxBase over h's partners
    if taxBase[r] > floor and r has a partner k with taxBase[k] < taxBase[h]:
        offer = (r, TRADE)                               // "r would swap a poorer partner for h"
    if r in neighbours(h) and not atWar(h):              // 0x00452150 BT [EBX+0x46]; 0x0045215C FUN_00449CD8(h)
        offer = (r, ALLIANCE)                            // overrides trade
TPremierForm_StartTurn()
(game-over check for h)
```

The target is always the human whose turn is starting, and the roll never touches the relation matrix. Read from the saved state, which is written later in the same human turn, all six observed offers pass the trade test. All six also fail the alliance gate, which is why none became an alliance offer: Rome is at war with Gaul in its three saves, and none of Thracia's three proposers borders Thracia **[confirmed: saves]**. One example is `1_thracia_271_summer_9.sav`, Rome → Thracia. Thracia has no partners, so the floor is 0. Rome trades with Seleucid, Macedonia and Numidia, and Numidia's tax base, 440, is below Thracia's 652 **[confirmed: save]**. An alliance offer additionally needs `r` to border `h` and `h` to be at war with nobody. No alliance offer has been observed.

## 2. What `TPremierForm_StartTurn` does with it [confirmed: listing]

`TPremierForm_StartTurn` (`0x0045AC5C`, :58175) is the only place the offer is shown. If `offer.nation ≥ 0` and `rel[h][offer.nation] != offer.type`, it builds the sentence and calls `FUN_0042D750` (`Dialogs.MessageDlg`) with `DL = 2` (`mtInformation`) and `CX = [0x0045AE64] = 0x0004` (`[mbOK]`). The next instruction, `0x0045AE07 XOR EAX,EAX`, discards the modal result. Nothing follows except the exception-frame teardown.

For contrast, `TUnitMap_SelectUnit`'s "*Are you sure you want to attack this …?*" uses `DL = 3` (`mtConfirmation`) and tests the result against `6` (`mrYes`). The offer box has no such test and no Yes/No buttons.

- **Cleared:** only by `FUN_00452034`'s first write, at the next human turn start, whether or not anything was done. In hotseat play every human turn start re-rolls it, so the block always belongs to the current human.
- **Read:** by `StartTurn` (the dialog) and by `TPolitics_MakeTrade` at `0x00452E94` (:55229). `TPolitics_MakeAlliance` does not read it.
- **Saves agree.** In each of 4 offer → next-save pairs, the offer is gone in the next save and the human–proposer relation is still `0`: Media → Rome (`1_rome_270_autumn_5` → `_7`), Ptolemaic → Thracia (`1_thracia_271_spring_7` → `_9`), Armenia → Thracia (`spring_11` → `summer_1`), and Rome → Thracia (`summer_9` → `summer_11`). The user's notes record the trades the user did make through Politics ("*Rome trades with Dacia*", `1_rome_270_winter_3`), and they appear in the matrix.

## 3. The other direction: a human proposes to an AI (`TPolitics`)

`TPolitics_ChangeIR` (:55103) calls the handler only when the clicked value differs from the working row (`form + 900`). `TPolitics_OK` (:55335) commits it through the setter. A cooldown (`< 0`) can be overwritten only by war.

- **Trade** (`TPolitics_MakeTrade`, :55190): the handler refuses in four cases.
  - The human's working row already has 3 partners.
  - The relation is negative: "*X does not want to trade with you.*"
  - The relation is above 1 (allied or at war): "*You cannot trade with X.*"
  - The target already has 3 partners **and** there is no pending trade offer from that target.

  There is no AI willingness test. On OK, if the target has 3 partners, it drops its lowest-tax-base partner to peace, a `−8` cooldown **[confirmed: code]**.
- **Alliance** (`TPolitics_MakeAlliance`, :55271): if the target is human, it is always accepted. If the target is AI, it is refused ("*X does not want to ally with your nation.*") when:
  - the human's working row contains a war, or
  - any nation the working row marks allied is at war with anyone (`FUN_00449CD8`), or
  - the human is at war in the committed matrix, or
  - the relation is negative.

  **The AI target's own wars are not checked** (listing `0x00453101–0x0045317A`). So allying with an AI at war drags the human into that war through the setter's cascade **[confirmed: code]**. This corrects the earlier "either side" wording (see the correction note in the diplomacy report).

## 4. Can an AI declare war on its own ally?

**Not by its own choice.** A war target `k` must satisfy `not protected(k)`. If `k` is allied to `me`, then `me` is one of k's allies, and the test `cities[k] + cities[me] > cities[me]` is true whenever `cities[k] ≥ 1`. The AI also declares only while it is at war with nobody, its mobilization is ≤ 40, and it is not season 3; the chance is 1 in 10 per turn, and there is at most one declaration per turn. AI armies and fleets never attack a nation they are not at war with: `FUN_0044D734` (:51517) calls `FUN_0044AEE4` and `FUN_0044B27C` only if `rel == 3`, and `FUN_0044E1FC` (:52115) calls `FUN_0044B5D0` only if `rel == 3`. So there is no implicit declaration by attack **[confirmed: code]**.

**The alliance is not "broken first" either.** The setter `FUN_00449B40` (:48472) does not check a prior alliance. Declaring war on `b` writes `3` over anything and drags in every ally of `b` that `me` is not already at war with, **including `me`'s own allies**. So an alliance can turn into war only through a cascade:

1. `me` declares war on `X`, and `X` is allied to `me`'s ally `Y`. This needs `X` to be unprotected: for every ally `a` of `X` (Y included), `cities[X] + cities[a] ≤ cities[me]`.
2. `me`'s ally `Y` declares war on `X`, and `X` is allied to `me`. The same test applies from Y's side.

The alliance cascade cannot break an alliance. `me` allies only with an `m` that is at war with exactly one nation, `j` (`wars(m) < 2`), and `j` is not `me`'s ally (`rel[me][j] ≤ 1`).

## 5. What a reimplementation needs

- **AI → human, trade or alliance:** roll it at the human's turn start with the rule in §1b, and show an OK-only notice. **Never write the relation.** Accepting means the human uses the normal proposal path: trade through the `TPolitics_MakeTrade` rule, with the target's full-roster refusal waived for the pending proposer, and alliance through the `TPolitics_MakeAlliance` rule, unchanged. An "accept" button is a UI convenience the original lacks. If one is added, it must apply those same gates, and for an alliance that means the **human-side** war checks, not the proposer's. Clear the offer at the next human turn start.
- **AI → AI:** trade and alliance are written directly, with no consent step, subject to the gates in §1a.
- **War on an ally:** the AI's direct rule must exclude any ally holding a city. There is no alliance-break step. War overwrites alliance only through the setter's cascade, in the two cases in §4. AI units must attack only nations they are already at war with.

## What this does not establish

- **Whether a nation with `unity > 0` but 0 cities can exist.** That is the only case in which the "ally is protected" test fails for a direct ally. It has not been checked.
- **An alliance offer, or a cascade that turns an alliance into war,** has never been observed in a save. Both are code-only.
- **The two "busy" conditions, mobilization > 40 and season 3,** are read literally from the listing. Their design intent is not argued here, and no save pair was used to test the war rule's other terms: the power ratio, the neighbour test and the 1-in-10 chance.
- **The `+0x46` "neighbour" name** rests on three saves' masks being symmetric and geographic. Where the mask is built (the DAT or a map pass) was not traced.

## Reproduction

- **Decompile:** `%LOCALAPPDATA%\ReTools\all_app_functions.txt`, lines cited above.
- **Listings:** `analyzeHeadless … -readOnly -postScript DumpListing.java ai_diplomacy_listing.txt 0x0044fb7c 0x0044faa0 0x00452034 0x004530d8`. `StartTurn`'s listing is in `news_log_listing.txt`, lines 242–258.
- **Saves:** a Python reader computes the nation table at `89,600 + 11,356 + 2 + armies × 656 + 2 + fleets × 26` and reads the 16 × 1,172-byte records: name at `+0`, relation row `+0x26`, neighbour mask `+0x46`, unity `+0x440`, mobilization `+0x442`, cities `+0x446`, tax base `+0x44C` and human flag `+0x490`. The offer is at trailer `+32`. The ally-to-war scan covers the consecutive saves of the `1_rome_270_*` (13), `1_cartago_271_*` (9) and `1_thracia_271_*` (13) runs, 32 pairs in all. Nothing from either the saves or the game was copied into a repository.

## Dev-repo engine, for comparison (read-only)

`src/IC2.Engine/Ai/AiDiplomacyPhase.cs` emits `ProposeAllianceCommand` and `ProposeTradeCommand` candidates toward any nation, human seats included. `ProposeAllianceCommandHandler` accepts a human target unconditionally, mirroring the `TPolitics_MakeAlliance` branch for a human target. In the original, that branch is reachable only when a human proposes to another human in hotseat play. `src/IC2.Engine/Ai/AiMilitaryPhase.cs` pairs `DeclareWarCommand` with an attack on any adjacent foreign city or army, with no exclusion for allies. Both differ from the original. See §5.
