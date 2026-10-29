# Clarifications for the original manual's five inconsistencies (research #91), from promoted evidence

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `9b4f667` (PR #248). It
answers research issue [#91](https://github.com/diegoami/imperial-conquest-2-research/issues/91)
(Main #1551), delegated to conquest on 2026-10-29.

**Tag:** each row carries the tag of the reports it cites. There was **no new playtest**.

**Review note (2026-10-29):**
- **What was checked.** This is a synthesis of promoted reports, so the review checked each
  "What the original does" cell against the report it cites:
  - **R04:** score = queued units + 1 for the capital; strict `>`, so the first-listed town keeps a
    tie; All cities appears only when more than one town queues; a unit ordered under All cities is
    raised at the capital. The Tarquinii-before-Rome tie control is in
    [`2026-10-26-recruitment-default-gui81.md`](2026-10-26-recruitment-default-gui81.md).
  - **C01:** the list uses the decoded current level (`% 100` while an order is in progress); the
    Recruit button and the AI compare the raw word with 74, so a town with an order in progress
    passes. See
    [`2026-09-29-which-cities-may-recruit-and-troop-amounts.md`](2026-09-29-which-cities-may-recruit-and-troop-amounts.md),
    and G8 in [`2026-10-11-g1-original-checks.md`](2026-10-11-g1-original-checks.md) (fort 60,
    still listed, order refused).
  - **C02:** the E03 order is upkeep → wealth and tax base rebuilt → city loop (growth) → nation
    loop (income) (feature inventory E03). The new-game base differs from the live sum: 2,528 vs
    2,464 in [`2026-10-05-balance-sheet-tribute-line.md`](2026-10-05-balance-sheet-tribute-line.md).
    The quarter income check is case I of
    [`2026-10-12-g4-followups.md`](2026-10-12-g4-followups.md): one set of 15 AI nation-quarters
    plus Rome.
  - **C03:** the gate matches the rules specification §7 Politics-screen alliance bullet word for
    word.

  Every cell agrees with its source.
- **The manual itself was not read, by either session.** The manual's sentences come from #91 and
  Main's audit (`docs/investigations/manual-ui-reference-audit.md`). Neither ic2-conquest nor this
  research session has the private manual copy. *(Research's delegation brief wrongly said
  conquest held it; the draft states the limit correctly.)* So the table resolves what the
  original does, and the "Supported wording" column is a proposal to compare against the actual
  manual text before any erratum is written.
- **No new rule.** Every rule here is already in the promoted reports and the rules specification,
  so the specification is unchanged.

## Table

| # | Manual (per #91 / the audit) | What the original does: evidence | Supported wording | Remaining uncertainty |
|---|---|---|---|---|
| R04 | §5.3.1 describes "All cities" through a non-capital queue and a first position | **Default town** (gui81, nine Wine controls): with no queued unit, the capital; otherwise the town with the highest score (its queued units, +1 if capital), ties to the **first listed** town in the nation's city-list order. **"All cities"** is inserted at the **top** only when **more than one** town holds queued units, and it does not replace the default selection. A new unit created under All cities goes to the capital. The default is recomputed each time the dialog opens. **One non-capital town queuing, capital queuing nothing:** there is no All cities row; that town and the capital both score 1, so whichever is listed first is selected (Tarquinii before Rome → Tarquinii). | "When you open Recruit, the town with the most units in training is selected (the capital counts one extra; on a tie, the first town in the list). If more than one town is training units, an 'All cities' entry appears at the top; units ordered there are raised at the capital." | The 'All cities' row with a gapped queue table is code-derived, not played (gui81). The remake's opening city (T162/T166, first listed) is a deliberate remake policy, separate from this. |
| C01 | §§5.3.1 and 11.1.8: towns "below 75%" fortification cannot recruit | Two different tests. **The list** shows a town if it is the capital, or its current level is ≥ 75 (with an order in progress, the low two digits of the word, e.g. 578 → 78), or it already holds queued units. **The Recruit button** refuses ("This city's fortification has fallen below 75%.") only if the town is not the capital and its **raw fortification word** is ≤ 74. Played at fort 60: a town with queued units stays listed and its new order is refused (G8). | "You can recruit at your capital and at towns fortified to at least 75%. A town that already trains units stays in the list after its fortification falls below 75%, but no new unit can be ordered there." | **Pending-order edge (code-derived, unplayed):** a listed town (it has queued units) at level 72 with an order in progress (word 572) passes the button's raw-word test (572 > 74), so the order is accepted although its level is 72. |
| C02 | §3.5 puts the tax base before growth; §8.2 after cities grow | The quarterly tick's order (E03; `FUN_00451b40`): upkeep → **wealth and tax base rebuilt from the cities** → the city loop (**growth**, loyalty, rebellion) → the nation loop (mobilisation −3, **income** = taxBase × rate div 100 + taxBase div 4 …, trade, unity). Income was reproduced for 15 AI nations and Rome over one quarter (g4 case I). | "Each quarter the tax base is recalculated from your cities as they stand before that quarter's growth, and your income uses it. Growth during the quarter shows in the next quarter's tax base." | Before the first quarterly tick, the stored base is the new-game value, not the cities' live sum (2,528 vs 2,464). |
| C03 | §9.2's table and §9.4's text differ on which side's wars block an alliance | Rules spec §7 (Politics screen; `decompiled-ai-offers-to-human-seats.md`). Against an **AI target**, a proposal is refused if the human's edited row contains a war, a nation that row marks allied is at war with anyone, the human is at war in the committed matrix, or the relation is negative. **The AI target's own wars are not checked**, so allying with an AI that is at war drags the human into that war (the cascade). Against a **human target** (hotseat), the proposal is always accepted. | "You cannot propose an alliance while you, or any nation you are allied with, are at war, or while a peace cooldown runs with that nation. The other nation's own wars are not checked: allying with a nation at war brings you into its wars." | The AI's acceptance beyond the gate is not covered. |
| — | Metadata: the README says 95 screenshots; the HTML and the chapter Markdown each reference 109 images, 104 unique | Main's audit counted 109 references and 104 unique images in both, with no content mismatch in the 13 groups it checked. Conquest #133's completion note said "95 screenshots" and lists `all-screenshots/` with 160 captures. | "104 screenshots (109 references; some appear twice); 160 captures in the full set." | The 95 likely predates the last chapter edits; not re-counted (no access). |

**Also kept, per #91:**
- The nominal "500 men per ship" is a simplification. Human embark and mercenary transport round
  exactly as [`2026-10-26-human-transport-rounding83.md`](2026-10-26-human-transport-rounding83.md)
  measured, and the remake's T232 Improved/AI policy is separate.
- The remake's newer flexible money behaviour (T231) is a remake exception, not original behaviour
  to write into the manual.

## What this does not establish

- The manual's exact current sentences. Neither session re-read them; the passages follow #91 and
  Main's audit.
- The C01 pending-order edge and the R04 gapped-queue All-cities row in play. Both are
  code-derived.
- Any change to the remake. #91 requests none.
