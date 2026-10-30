# The AI's capital defence (FUN_0044efc8): the first 9 threats in table order; the nearest wins, the earlier list entry on ties

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `2d1d7ed` (PR #268). It
answers research issue [#123](https://github.com/diegoami/imperial-conquest-2-research/issues/123)
(for imperial_conquest_2 T240/#1216), delegated to conquest on 2026-10-29.
- **Scripts:** `runs/experiments/capdef123/{controls.py, analyze.py}`.
- **Hook:** `patches/capdef_hook.py`.
- **Data:** `runs/experiments/data/run-exp-capdef123/`.
- **Release:** [`run-exp-capdef123`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-capdef123).

The same conquest PR corrects the #117 addendum's "at most 10" threats to 9.

**Tag:** `[confirmed]`: decompile, disassembly, emulation, and play under Wine.

**Review note (2026-10-30):**
- **Release integrity:** 183 of 183 files match `SAVES.sha256`.
- **Inertness:** I compared the hooked and plain autosaves myself: **90 of 90** pairs are
  byte-identical.
- **Reruns:** I ran both scripts from scratch copies with outputs redirected.
  - `analyze.py` over the release layout reproduces `summary-v1.json`: 179 calls, 0 threats
    dropped by the cap, 134 decisions, 89 dispatches, 0 ties.
  - `controls.py --version v2` (Unicorn on the #187 RAM) reproduces `controls-v2.json`.
- **Decompile re-read** (:52776–52899):
  - an at-war threat beyond Chebyshev 19 is skipped;
  - the threat count is `min(9, n + 1)`;
  - responders are dispatched while fewer than `n + 2`;
  - a responder is skipped when its `FUN_0044ee60`/`FUN_0044ece4` pick qualifies under the
    3 × moves test;
  - a threat is eligible at war or when the responder is 20 or more from the capital;
  - the responder walks toward the capital when the **chosen threat** is aboard a fleet or its owner is not at war; otherwise it walks toward the threat. *(Corrected 2026-10-30: this note first said "a responder aboard"; see the correction below.)*

  The strict tie comparison (`jge`) is the draft's disassembly reading and was not re-read here.
- **Consistency:** the rules spec §9 already gives up to 9 threats, the radii (within 20 at war,
  within 10 otherwise, the same bounds as ≤ 19 and ≤ 9), the `threats + 2` dispatch limit, and
  the capital fallback. This report adds the table-order dependence, the tie rule, the pre-emption
  of the enemy pick, and the in-play counts.

## Answer

1. **The threats are listed in table order.** A foreign army qualifies when it is in the capital's
   region and coast side (`FUN_0044eb9c` = 0) and within Chebyshev **19** of the capital if its
   owner is at war with the nation, otherwise within **9**.
   - The list stores the entry first, then sets `n = min(9, n + 1)`.
   - So it keeps the **first 9** threats in table order. Later threats overwrite an uncounted
     10th slot.
2. **The responders are also taken in table order:** own armies with moves left, until `n + 2`
   have been dispatched.
   - A responder is skipped if its own enemy pick (`FUN_0044ee60` or `FUN_0044ece4`) scores above
     100 with a target closer than its moves, **and** the capital is more than 3 × moves away.
3. **The choice:** the nearest listed live threat that is eligible. Eligible means its owner is at
   war, or the responder is 20 or more from the capital. The comparison is strict, so on ties the
   **earlier list entry** wins.
4. **The responder walks** (`FUN_0044dba8`) toward the **chosen threat** if that threat is not
   aboard a fleet and its owner is at war with the nation. Otherwise it walks toward the capital.
   The test is on the **threat**, not on the responder (see the correction below).
   - A responder that is itself aboard is not tested here. Its walk goes through `FUN_0044dba8`,
     whose own aboard branch makes it move its fleet toward the destination instead.
5. **Order in the army phase:** EFC8 runs **first** in F31C, before the per-army loop, and that
   loop only runs for armies with moves left. So EFC8 **pre-empts** the `FUN_0044ee60` pick by
   spending the army's moves; it does not replace the pick.

**Controls (emulation, #187 RAM, unmodified).** Carthage's capital is at (93,78), with responder
army 3 at (93,79).
- **Tie:** a Roman army at (90,79) and a Seleucid one at (96,79), both 3 away. The responder goes
  to (90,79) as staged, and to (96,79) with records 0 and 4 swapped.
- **Cap:** 12 threats in the region. The nearest, (90,76), is 12th in table order, so it is
  unlisted, and the responder goes to (74,79). Swapped into record 0, it is chosen: (90,76).

**In play** (hook on Rome `BASE`, S13 Armenia and S10 Dacia × 30 End turns, seed 12345; 90 of 90
inert):
- 179 calls, with 1 threat (157 calls) or 2 (22), never more;
- 0 threats dropped by the cap;
- 134 decisions and 89 dispatches;
- **0 ties.**

So in these turns no capital defence was decided by table order.

## Correction (2026-10-30): the aboard test is on the threat, not the responder

The main project's evidence intake (comment on #123) found that this report said a **responder
aboard** walks to the capital, while the rules specification §9 says an **aboard threat** cannot
be intercepted. The disassembly settles it in favour of the specification:

| Address | Instruction | Meaning |
|---|---|---|
| `0x44F29B` | `movsx eax, word [esp+0xa]` | `local_3e`: the index of the **chosen threat** |
| `0x44F2A3` | `cmp word [eax*8+0x47C1F4], -1` → `je 0x44F2D2` | the threat's army record `+8` (the covered cell) is −1: the **threat is aboard** → walk to the capital |
| `0x44F2CA` | `cmp word [ecx+edx*2+0x26], 3` → `je 0x44F2EE` | relation of the nation to the threat's owner (`+4`) is war → walk to the threat |
| `0x44F2D2`–`0x44F2E7` | `mov edx, [eax*2+0x47959E]`; `call 0x44DBA8` | the walk to the capital city's coordinates |
| `0x44F2EE`–`0x44F2F9` | `mov edx, [eax*8+0x47C1EC]`; `call 0x44DBA8` | the walk to the threat's position |

The responder's own index (`[esp]`, `local_48`) is passed to `FUN_0044dba8` but never tested for
being aboard in this routine. These are not two separate predicates: the one test is "chosen
threat aboard, or not at war", and the earlier wording simply named the wrong army. The draft's
"if at war and not aboard" did not name its subject, and this research intake misread it as the
responder. The specification's bullet ("a threat aboard a fleet cannot be intercepted — the
responder goes to the capital") is correct and unchanged.

## What this does not establish

- Crowded or later games, with more than 9 threats or equal distances.
- Order effects inside `FUN_0044ece4`: not read.
- An aboard threat, and the 20-tile exemption, isolated in play.
- The remake, which has no port yet. Its T240 needs the table order together with the sweep, plus
  the 9-threat cap.
