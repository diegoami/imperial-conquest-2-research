# Cross-family review of rules-specification.md (2026-10-07)

Reviewer: GPT-6.1 Sol via OpenCode (a different model family from the GLM-5.3 agents that
drafted the spec), run read-only against this repository. Brief: sample five rules per section,
check all Open lists against sources, scan coverage. Verdict: **redo** — 18 blocking findings.
Every finding was acted on the same day; see the commits that follow this file and the
correction notes in the affected reports. The text below is the reviewer's report verbatim.

## VERDICT: redo

Most sampled formulas are faithful, but the consolidation needs another reconciliation pass: it retains superseded claims, gives incompatible rules in different sections, drops several consequential qualifications, and omits part of the strategic order set.

I read the specification end to end, checked **five rules per section—50 total**, scanned all ten Open lists against their sources and relevant follow-ups, and checked report coverage. This was a document-to-source review; I did not re-verify the executable or saves. No repository files were modified.

All specification line numbers below refer to `docs/rules-specification.md`. Source filenames refer to `docs/reports/`.

## BLOCKING FINDINGS

1. **A small troop loss has become near-total annihilation.**

   **Spec, line 569:** “left every unit … between 2.50 % and 2.85 % of its troops”.

   **Source:** `field-recruitment-uniform-attrition-and-fleet-drift.md:43`:
   > “Every unit **lost** between 2.50% and 2.85% of its troops”

   **Correction:** Replace “left … between” with “each unit lost between”. The surviving fraction was approximately **97.15–97.50%**. Also retain the source’s inferential wording—“strongly suggests a single percentage”—rather than presenting that interpretation as an observed uniform multiplier.

2. **The supply-production worked example is attached to the wrong mobilisation rate.**

   **Spec, line 178:** After saying that mobilisation 100 halves every figure, it gives a population-50 example of `+50 / +200 / +200 / −100`.

   **Source:** `city-population-growth.md:102–111` explicitly introduces those numbers as:
   > “Per turn, at mobilization 0”

   and then states:
   > “At mobilization 100 every figure is halved, gains and Winter losses alike.”

   **Correction:** Label the existing example **mobilisation 0**. At mobilisation 100, population 50 gives **+25 / +100 / +100 / −50**.

   **Related contradiction, line 179:** “nations at mob 0 lose nothing in Winter” conflicts with the source’s exact formula:
   > `inc = s − (s × mobilized (+0x442)) / 200`

   That sentence is inherited from an internally inconsistent passage in the source, rather than newly invented by the consolidation. Nevertheless, it cannot stand as the specification of Winter supply change: at mobilisation 0 the formula gives the **full Winter loss**. If “lose nothing” means *no mobilisation reduction*, say that explicitly.

3. **The defender-strength fortification boundary differs from its cited source.**

   **Spec, line 284:** Fortification is decoded only when `> 100`.

   **Source:** `decompiled-city-capture-resolution.md:28`:
   > “fortification decoded: value **< 100 verbatim, else value % 100**”

   **Correction:** Preserve the source’s boundary: **100 is in the modulo branch**. The distinction changes defence by 25,000 at raw fortification 100. Line 970’s unconditional `mod 100` agrees with that boundary, so the two sections currently disagree. This is the defence calculation, distinct from the UI’s finished/pending-order boundary.

4. **The rebirth capital-selection explanation drops a qualification that can change the selected capital.**

   **Spec, line 193:** Describes strength at loyalty 90 as simply `90 × 150 + fortification × 250 + population × 200`.

   **Source:** `decompiled-quarterly-rebellion.md:222`:
   > “A **former capital of another nation** still passes `FUN_0044B8D0` through the stale pointer. With loyalty 90 > 59 it gets **× 5/3**, so it is strongly favoured `[derived]`.”

   **Correction:** Say selection uses the **full `FUN_0044A98C` result**, and retain the stale-capital bonus qualification with its derived strength. The parenthetical baseline must not imply that all candidate cities have only those three terms.

5. **The prohibition on diplomacy against eliminated nations loses the human-defection exception.**

   **Spec, line 322:** “no one can declare war on an eliminated nation”, tagged `[confirmed]`.

   **Source:** `decompiled-elimination-cleanup.md:114–117`:
   > “a human eliminated by defection ends with **unity 150**, not 0.”

   > “The former human seat therefore keeps taking (empty) AI turns and **can still be targeted diplomatically**.”

   **Correction:** State the actual gate: nations with **unity ≤ 0** are skipped and excluded as diplomatic targets. Explicitly retain the exceptional human-defection path. Line 320 mentions the 150 value but line 322 incorrectly erases its consequence.

6. **The end-turn filter’s Boolean meaning is reversed.**

   **Spec, line 102:** Says `fullMoves != army[+6]` means “this army has not acted”.

   **Source:** `2026-10-03-end-turn-warning-box.md:28`:
   > “has **not acted** this week: `FUN_0044AAB4(a) == 0`, i.e. moves `+6` **equals** the recomputed full allowance”

   Its code excerpt at line 78 is:
   > `if (!FUN_0044aab4(a)) { // not acted`

   **Correction:** The helper returns true for **different allowance / acted**; the warning processes its **false** result. The older cited sequencing report contains the same mistaken English interpretation, but the later warning report resolves it. Cite both and use the corrected polarity.

7. **The fleet record section retains the superseded `CityIndex` interpretation.**

   **Spec, line 606:** Says deployed fleets carry a drifting or stale `CityIndex` that may reference a city which changed hands.

   **Source:** `decompiled-unit-map-orders-and-record-fields.md:50`:
   > “The ‘`CityIndex` drifts as a fleet acts’ observation … is a fleet’s **condition changing**”

   and:
   > “the four fleets at `(0,0)` are **under construction**”

   **Correction:** Remove the deployed-fleet city-index explanation. `+20` is **build city while under construction, condition after launch**, as line 601 already correctly states. Likewise, line 597’s assertion that completed in-port fleets also read `(0,0)` should be reconciled with the corrected construction identification rather than retained from the old owner report.

8. **The fleet-join boundary is contradictory, and the newer source is itself internally inconsistent.**

   **Spec, line 662:** Exactly 100 combined ships is refused; acceptance requires `< 100`.

   **Spec, line 1091:** Acceptance requires `sum < 101`.

   **Sources:**
   - `2026-10-07-join-fleets-100-ships-boundary.md:12–13`:
     > “The merge proceeds only when … **< 100**. Combined ships == 100 is refused”
   - But its quoted decompile at line 25 says:
     > `if (... + iVar2 < 0x65) {`
   - `2026-10-05-refusal-texts-and-conditions.md:126` quotes the same constant and describes refusal when:
     > “the ships add up to **101 or more**”

   **Correction:** Do not publish either boundary as reconciled confirmation. **`0x65` is 101**, so the newer report’s prose conflicts with its own evidence excerpt. Resolve that source conflict, then make lines 662 and 1091 consistent and name the correction. This review does not establish which comparison the executable actually contains.

9. **The mobilisation substitution has been upgraded from derived to confirmed.**

   **Spec, line 393:** Includes `1 + troops / (3 × totalPopulation)` inside the `[confirmed]` claim.

   **Source:** `decompiled-mobilization-and-mercenary-restock.md:271`:
   > “the increment is `1 + troops / (3 × totalPopulation)` … **`[derived]` — direct substitution**”

   **Correction:** Keep the stored-wealth expression `[confirmed]`; tag the population substitution `[derived]`. Also make clear that the substitution assumes wealth equals the relevant population sum, rather than silently substituting a live sum for persisted wealth between rebuilds.

10. **The AI-versus-human recruitment statement contradicts the established human gate.**

    **Spec, line 994:** “the human’s dialog requires the money”, tagged `[confirmed: decompile]`.

    **Source:** `2026-09-29-which-cities-may-recruit-and-troop-amounts.md:64`:
    > “**No treasury check:** `RecruitUnit` has no money check, so the treasury can go negative through recruitment.”

    **Correction:** Remove the human affordability requirement. Line 367 already correctly says there is no treasury check. The assertion is inherited from the strategic-AI report’s asymmetry table, so this requires recording a **source disagreement**, not treating that table as authority over the earlier explicit handler analysis.

11. **The Information-band rule overstates both confirmation and range coverage.**

    **Spec, line 1084:** Tags the combined band rule `[confirmed]`, including morale “very low 40–54” and unbounded “blank at 1000+” / “blank 75+”.

    **Source:** `2026-10-05-information-window-fields-and-bands.md:178`:
    > “40–47 read the unity table’s entries … `[D]` (**not staged**)”

    Its explicit blank ranges are **unity 1000–1199** and **morale 75–80**. At line 268 it qualifies out-of-range readings:
    > “are … **[derived]; the ones staged are marked confirmed only where both sides were seen**.”

    **Correction:** Separate confirmed edges from code-only/derived extensions, particularly morale 40–47. Do not turn finite table ranges into unlimited “+” ranges. Reconcile the corresponding Open qualification at line 1116.

12. **The refusal summary drops the multiple-box exception.**

    **Spec, line 1089:** “the first-tested is shown and only one box appears”.

    **Source:** `2026-10-05-refusal-texts-and-conditions.md:19`:
    > “**The transfer dialog is the exception**: its 20-unit and 100,000-troop refusals are an else-if, but the fleet-capacity refusal is a **separate second box**.”

    **Correction:** Restrict the one-box statement to the relevant ordered refusal chains and retain the transfer-dialog exception. This changes observable behaviour, not merely wording.

13. **The no-mid-battle-save assertion is superseded by a controlled observation.**

    **Spec, line 88:** “saving during a battle is not possible in the game’s UI”, therefore every real save has no battle-state variant.

    **Source:** `2026-10-04-battle-probe.md:7`:
    > “**Save As inside a battle works through the File menu** … The file carries block 12 … the battle window stays open and the battle continues.”

    The same source qualifies this:
    > “It needs human control: with Computer general **on**, the battle runs at the next input event”

    **Correction:** Replace the impossibility claim with the observed **File → Save As, human-controlled phase, Wine-only** behaviour. Distinguish it from the toolbar Save button, which did nothing. Line 779 already incorporates the later finding and conflicts with line 88.

14. **Section 10 drops the sources’ overarching Wine-only qualification.**

    **Spec:** Bare `[confirmed]` claims throughout the end screens, leaders form, Information bands and refusal subsections—for example lines 1012–1026, 1034–1035 and 1077–1089—lack a subsection-wide Wine qualification.

    **Sources explicitly qualify their confirmation:**
    - `2026-10-05-end-of-game-screens.md:3`:
      > “**Wine-only, and every state that reaches a window is staged** … every observed result is a candidate until the desktop original confirms it”
    - `2026-10-06-leaders-form.md:3`:
      > “every `[confirmed]` result is seen under **Wine 9.0; the desktop original is not confirmed**”
    - The Information-window and refusal reports have equivalent qualifications in their opening status paragraphs.

    **Correction:** Add explicit subsection-wide evidence qualifications or qualify the individual tags. Preserve the distinction between source `[derived]` code readings and source `[confirmed]` Wine observations. The section’s Open list does not supply this missing qualification.

15. **The Open lists systematically retain resolved questions and obsolete evidence-status claims.**

    These are not requests for additional live corroboration of code-only rules; the listed claims say a mechanism, identification or observation remains unknown when another report supplies it.

    | Spec location and claim | Source’s actual statement | Correction |
    |---|---|---|
    | §1, line 110: seasonal table contents unextracted | `city-population-growth.md:9`: “already located … at `0x1F7D8`”; values **50/80/80/20** | Close the extraction question. |
    | §1, line 111: treasury/tax step “still unfound” | `decompiled-quarterly-billing-and-economy.md:3`: “`FUN_00451b40` is called exactly once per season” and resolves billing; its corrections give the credit | Replace with the quarterly location already specified in §2. |
    | §1, line 112: fleet completion not decompiled | `decompiled-unit-map-orders-and-record-fields.md:43`: “`FUN_0044A050` (construction completes)” followed by its launch writes | Close the decompilation question; retain any genuinely untested storm odds separately. |
    | §1, line 115: trailer `+38` unknown | `decompiled-sav-file-layout.md:37`: tail fields are “turn-order index, week, year BC and season” after current nation | Identify `+38` as turn-order index. |
    | §2, line 207: tax preview’s relationship to stored fields unknown | `decompiled-fleet-tax-and-mercenary-formulas.md`, “Tax income”: `income = nationTaxBase × taxRate / 100`; `nation-tax-base-and-city-economy-fields.md:5` locates the stored base | Close the formula/field question; distinguish preview from net treasury change. |
    | §2, lines 182/209: fortification-100 behaviour unsettled | `2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md:9`: “**confirmed live**”; line 65: “Ariminum … is at **0%** after one turn” | Use the resolved Wine observation already in §3. |
    | §2, line 210: mercenary table values and label backing unsolved | Hire-price report: “LI 1, HC 4”; offer-position report: “20-byte table at DAT **`0x1F8C6`**” with 52 names | Close the identified-table questions; retain limits of the particular live price tests. |
    | §2, line 214: exact AI stability trigger awaits an observed collapse | Quarterly-billing correction, line 61: “**leader deposition**”, exact trigger, “confirmed on **2 of 15**” | Close the trigger/identity question; do not call it an unobserved nation collapse. |
    | §3, line 333: weekly army moves maximum unknown | Army-moves report: “`10 − min(5, ⌊totalTroops / 20000⌋)`”, with the low-supply decrement | Close it; §§1 and 5 already state the answer. |
    | §3, line 340: supply ratio and resupply form unidentified | `supply-capacity-rounding.md:7`: dialog cap `troops div 100 + 1`; unit-map orders report, line 116: “`TAFSupply` … is the dialog … could not name” | Replace the approximate candidate with the path-specific caps and named form. |
    | §4, line 431: shuffle’s code location unknown | Shuffle report, line 9: “`FUN_00448AA4` … builds the order” | Close it. |
    | §4, line 433: no seed-exact New Game fill replay | Shuffle report, lines 18–22: recovered clock seeds reproduce turn order, filled-slot count and storm cells | Describe the completed replay checks and their precise scope instead of a blanket “not reproduced”. |
    | §5, line 588: human debt game-over code-only | End-screen report, lines 13–18, tags debt reasons `[confirmed]`; its evidence table supplies both staged debt thresholds | Update to staged Wine observation; desktop corroboration remains outstanding. |
    | §6, line 677: fleet peace prompt never exercised | `2026-10-03-fleet-peace-prompt.md:3`: “**closes the open item**”; five No/Cancel/Yes trials | Close it for the tested trade relation, retaining other relation values as untested. |
    | §6, line 683: parity difference unresolved | Naval-random-term correction, line 6: differences “follow from the **strict inequality and need no further effect**” | Remove the superseded continuous-model puzzle. |
    | §6, line 687: meaning of 333/335 distinction unknown | Fleet-order correction: “the **333/335 distinction is closed**”; unit-map report, line 177: different owners’ large fleets | Close the owner/size identification. |
    | §6, line 688: Split’s 20-ship minimum never played | Refusal report R17 lists the `< 20` refusal with **`[confirmed] F01`** evidence | Update the observation status; leave the untested exact Join boundary separate. |
    | §7, line 762: pre-treaty fields never read back | Diplomacy report correction, line 67: `W = 6188`, 48 cities, range `[2027,3573]` | Say the payment passes the range check; the exact RNG draw was not recovered. |
    | §7, line 761: uppercase war declaration observed only under Wine | `ptolemy-run-news-log-vocabulary-verified.md:69`: recorded original-game line “**CARTHAGE DECLARES WAR ON PTOLEMAIC.**” | Include this positive recording evidence and its target-human limitation. |
    | §8, line 887, and body line 878: Yes never observed/tried | Battle-peace-offer report, line 13: “**Yes versus No … 12 pairs**”, relation −18 after Yes | Close the Yes-behaviour question; retain the clipped terms-text limitation separately. |
    | §10, line 1113: uppercase declaration never saved; fleet-completion/sinking lines code-only | Vocabulary report: “**Greece finishes a new fleet at Athens.**”; fleet-peace-prompt report, line 58, reads uppercase declarations and sinking news from saves | Replace global “never observed/saved” claims with the actual evidence status. |

    **Correction needed overall:** Open lists should represent the **current consolidated knowledge**, not reproduce each source pass’s historical limitations without accounting for follow-ups.

16. **The full strategic order set is missing individual-unit join/split mechanics.**

    **Spec claim:** The introduction promises “every rule with its source”; §5 covers army joins/splits and individual-unit disbanding, but omits the individual-unit join/split rules.

    **Source:** `decompiled-unit-map-orders-and-record-fields.md:73`:
    > “only **regular** units may be joined … only units of the **same type** … combined troop count must not exceed … **standard battalion size**”

    > “The merged unit’s quality is the **arithmetic mean** … A split unit inherits type and quality”

    **Correction:** Add these operations, their limits, quality effects and naming behaviour. Mentioning Change units only in the disband subsection does not consolidate this report’s complete order-set finding.

17. **The player-interface consolidation omits a substantial source’s main finding.**

    **Spec claim:** Section 10 consolidates the player interface, but has no menu/view-command inventory, Find-city behaviour or Show-hints behaviour.

    **Source:** `2026-10-05-player-facing-feature-inventory.md:12`:
    > “**146 feature rows** … **86 [confirmed]** … **60 [derived]**”

    Concrete load-bearing rows include:
    > “Find a city … **OK moves the maps to the chosen city**” — A08

    and:
    > “Show hints … **hint present, absent after one click, present again after a second**” — Inferences

    **Correction:** Consolidate the functional interface commands and their behaviour, or explicitly narrow the deliverable’s coverage claim. This is a whole omitted interface family, rather than missing pixel-layout detail.

18. **Battle pacing is mentioned but its governing rule is absent.**

    **Spec:** Line 784 mentions adopting two delay settings, but §8 never specifies their adjustable behaviour or the delay mechanism.

    **Source:** `battle-freeze-diagnosed-procmon.md:47`:
    > `while ((int)(GetTickCount() - start) <= n * 100); // n × 100 ms`

    At lines 58–70:
    > “one pause per **exchange**, not one per sound”

    > “**a player-adjustable setting, stored per nation**”

    > “Setting both to **0** makes battles run at full speed”

    **Correction:** Add a short battle-pacing subsection covering separate shooting/melee preferences, the `n × 100 ms` wait, applicable visibility guard, and zero-delay behaviour. Preserve later sources where record-offset descriptions differ.

## NON-BLOCKING

- Evidence tags are absent from numerous bullets, especially in §§2, 3 and 9, despite the introduction’s “every rule carries” promise; apply them consistently.
- Line 85 calls the news log a ring buffer, while line 1041 correctly describes a shift register; standardise the terminology.
- Line 605’s `25–50 / ≥50` fleet-marker bands overlap at 50; use the later source’s unambiguous `25–49 / ≥50`.
- Distinguish “not observed in this particular pass” from “never observed anywhere” when retaining source limitations.
- Older reports contain corrected prose followed by obsolete originals; cite the correction explicitly to make the authoritative passage easy to find.

## COVERAGE GAPS

Three report families have load-bearing findings missing or materially incomplete:

1. **`decompiled-unit-map-orders-and-record-fields.md`** — individual-unit join/split rules, quality effects and naming behaviour.
2. **`2026-10-05-player-facing-feature-inventory.md`** — functional menu/view commands, Find city, hints and remaining interface operations; `menu-and-toolbar-inventory.md` covers the same missing family.
3. **`battle-freeze-diagnosed-procmon.md`** — configurable per-exchange pacing and zero-delay behaviour.

The ten titles otherwise cover the major gameplay subsystems. I did not count tooling feasibility, initial archaeological inventory or facts superseded by later reports as missing gameplay families.

## WHAT YOU CHECKED

Exactly five sampled rule bullets per section:

### 1. Turn sequence, calendar, and the weekly tick
- §1 — 16-swap New Game shuffle (L47) — `2026-10-03-new-game-turn-order-shuffle.md`
- §1 — week/season/year advance (L66) — `decompiled-turn-and-calendar-sequencing.md`
- §1 — weekly city supply production (L75) — `decompiled-turn-and-calendar-sequencing.md`
- §1 — complete SAV sequence and tail (L85) — `decompiled-sav-file-layout.md`
- §1 — end-turn “not acted” filter (L102) — `decompiled-turn-and-calendar-sequencing.md`; `2026-10-03-end-turn-warning-box.md`

### 2. Economy, taxation, and the quarterly tick
- §2 — quarterly treasury-credit formula (L143) — `nation-tax-base-and-city-economy-fields.md`; `city-population-growth.md`; `2026-10-05-balance-sheet-tribute-line.md`
- §2 — exact population-growth arithmetic (L166) — `city-population-growth.md`
- §2 — seasonal supply rates and mobilisation-100 example (L178) — `city-population-growth.md`
- §2 — mobilisation modulation and Winter statement (L179) — `city-population-growth.md`
- §2 — rebellion recipient decision tree (L189) — `decompiled-quarterly-rebellion.md`

### 3. Cities, the map, capture and defection
- §3 — rough-sea odds and radius table (L240) — `decompiled-map-code1-overlay.md`
- §3 — fortification-100 completion bug (L265) — `2026-09-29-fortification-orders-cost-rate-and-the-100-bug.md`
- §3 — conquest neighbour-mask merge (L274) — `dat-neighbour-mask.md`
- §3 — defender-strength formula and fortification decoding (L284) — `decompiled-city-capture-resolution.md`
- §3 — conquest trigger below six cities / immovable capital (L313) — `decompiled-elimination-cleanup.md`

### 4. Recruitment, mobilisation, and mercenaries
- §4 — readiness increment and quality conversion (L375) — `decompiled-mobilization-and-mercenary-restock.md`; `ptolemy-run-readiness-ladder-and-mobilization-rate-confirmed.md`
- §4 — mobilisation receiving radius and last-match selection (L384) — `decompiled-mobilization-and-mercenary-restock.md`
- §4 — mobilisation increment, inverse and population substitution (L393) — `decompiled-mobilization-and-mercenary-restock.md`
- §4 — mercenary refill troop and quality formulas (L404) — `decompiled-mobilization-and-mercenary-restock.md`; `decompiled-new-game-mercenary-fill.md`
- §4 — player mercenary-hire gates and check order (L411) — `decompiled-mercenary-offer-list-and-position.md`; `2026-10-05-mercenary-hire-price-is-a-gate-not-a-charge.md`

### 5. Armies: records, movement, supply, and purses
- §5 — signed moves underflow and next-tick repair (L453) — `army-moves-field-signed-and-the-ffff-underflow.md`
- §5 — selected army keeps transfer surplus (L489) — `2026-10-03-army-to-army-ok-supply-rebalancing.md`
- §5 — supplies/money nonnegative-persistence claim (L531) — `2026-10-07-army-supplies-and-money-signedness.md`
- §5 — seasonal and embarked supply consumption (L552) — `supply-driven-morale-and-fleet-attrition.md`
- §5 — uniform troop-loss observation (L569) — `field-recruitment-uniform-attrition-and-fleet-drift.md`

### 6. Fleets and naval warfare
- §6 — discrete naval strength bonus and defender-wins-ties (L639) — `2026-10-02-naval-battle-random-term.md`
- §6 — carried-army siege-strength contribution (L641) — `2026-10-02-naval-battle-army-aboard.md`
- §6 — winner ship/condition damage formula (L643) — `2026-10-02-naval-battles.md`
- §6 — storm damage composition and Winter spike (L652) — `2026-10-03-storms-and-losses-at-sea.md`
- §6 — exactly-100 fleet-join boundary (L662) — `2026-10-07-join-fleets-100-ships-boundary.md`

### 7. Diplomacy and war
- §7 — AI war-target score and declaration chance (L706) — `decompiled-ai-offers-to-human-seats.md`
- §7 — human trade refusals and pending-offer waiver (L728) — `decompiled-ai-offers-to-human-seats.md`; `decompiled-diplomacy-peace-terms-and-instant-battles.md`
- §7 — tactical post-battle peace-offer gate (L736) — `decompiled-war-cascade-and-peace-paths.md`; `2026-10-05-battle-peace-offer.md`
- §7 — treaty ally loop and ungated alliance reset (L742) — `decompiled-war-cascade-and-peace-paths.md`; `dat-neighbour-mask.md`
- §7 — quarterly cooldown thaw and eight-column bug (L747) — `decompiled-diplomacy-peace-terms-and-instant-battles.md`

### 8. Tactical battle
- §8 — shooting loss and morale formulas (L795) — `2026-10-04-decompiled-tactical-battle-rules.md`
- §8 — attacker melee-loss formula (L802) — `2026-10-04-decompiled-tactical-battle-rules.md`
- §8 — loss-formula versus rout explanation (L807) — `battle-replayed-rout-mechanic-and-combat-constants.md`
- §8 — troop/morale rout predicate (L829) — `battle-replayed-rout-mechanic-and-combat-constants.md`; `2026-10-04-decompiled-tactical-battle-rules.md`
- §8 — surviving-winner quality promotion (L839) — `2026-10-04-decompiled-tactical-battle-rules.md`

### 9. The computer seat’s turn
- §9 — threat-budget constants and proximity sums (L905) — `2026-10-07-strategic-ai-turn.md`
- §9 — deficit recruitment floor and three-order exception (L913) — `2026-10-07-strategic-ai-turn.md`
- §9 — week-11 tax-policy timing statement (L920) — `2026-10-07-strategic-ai-turn.md`
- §9 — AI city-defence scorer arithmetic (L970) — `2026-10-07-strategic-ai-turn.md`
- §9 — claimed human-versus-AI affordability asymmetry (L994) — `2026-10-07-strategic-ai-turn.md`; `2026-09-29-which-cities-may-recruit-and-troop-amounts.md`

### 10. Victory, defeat, and the player interface
- §10 — end-screen population/start-value fields (L1023) — `2026-10-05-end-of-game-screens.md`
- §10 — leaders-form human/computer transition floors (L1036) — `2026-10-06-leaders-form.md`
- §10 — end-turn supply-percentage threshold (L1055) — `2026-10-03-end-turn-warning-box.md`
- §10 — unity/loyalty/morale/quality display bands (L1084) — `2026-10-05-information-window-fields-and-bands.md`
- §10 — consolidated order limits, including fleet join (L1091) — `2026-10-05-refusal-texts-and-conditions.md`
