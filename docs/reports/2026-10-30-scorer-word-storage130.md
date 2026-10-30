# AI target scorers (FUN_0044ece4 city, FUN_0044ee60 army): 32-bit candidates, word-stored winners, a wrapping final add

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `adfc1b7` (PR #271). It
answers research issue [#130](https://github.com/diegoami/imperial-conquest-2-research/issues/130)
(remake [#1216](https://github.com/diegoami/imperial_conquest_2/issues/1216) item 2), delegated to
conquest on 2026-10-30.
- **Script:** `runs/experiments/scorer130/scorers.py`.
- **Data:** `runs/experiments/data/run-exp-scorer130/` (`controls-v1.json`, `survey-v1-public.json`).
  The full survey, with corpus hashes, stays private.

**Tag:** `[confirmed]`: disassembly plus emulation of the pinned unpatched EXE.

**Review note (2026-10-30):**
- **Controls rerun:** I ran `scorers.py controls --version v1` from a scratch copy, with outputs
  redirected. The result is **identical** to `controls-v1.json`: 24 rows, of which 22 boundary
  rows all match the word model and 2 are divide-by-zero rows (city and army). The draft's "22
  rows" counts only the model rows.
- **Survey:** I checked the public aggregates only: 10,105 saves, 1,233 unparsed (8,872 used),
  251,182 calls, 0 mismatches against the model. The survey itself was not rerun, since it scans
  the owner's private corpus.
- **Overlap:** this extends
  [`2026-10-16-strategic-ai-regions-resupply.md`](2026-10-16-strategic-ai-regions-resupply.md),
  which noted the word store and final word add but not the overflow cases. It is consistent
  with the tie rule in
  [`2026-10-30-army-table-order-after-deaths117.md`](2026-10-30-army-table-order-after-deaths117.md).

## Answer: the rule for both scorers

1. **Each candidate score is 32-bit.** It wins only if it is **strictly greater** (`>`) than the
   **sign-extended stored word** of the current winner. So the first candidate wins a tie, even
   after truncation.
2. **On a win, the low word of the candidate is stored.** This is the truncation point. The
   winner's distance is also stored as a word.
3. **The final `add word` of the distance wraps modulo 65536,** and callers read the score as a
   **signed word**.
4. **No target:** the score is −10000 and the distance 0. The city scorer leaves its index at −1;
   the army scorer leaves its index word untouched. *(The remake returns 0 here.)*

The controls cover 32767/32768, 65535/65536, negatives, final-distance carries, a truncated first
winner beaten by a smaller second candidate, a tie after truncation, and the army cap. All 22
model rows equal this word model.

## Reachability

- **The army scorer cannot truncate for any input:** every winner lies in (−10000, 2000], because
  of its 1000 cap plus the 1000 bonus.
- **The city scorer has no cap.** In the survey its largest candidate was 13,022, with no
  truncation and no wrapped addition. In normal early play the word rule is therefore observable
  only at its boundaries in controls.
- **Divide by zero:** 38 army-scorer calls hit `#DE` at `0x44EF2C`, all in staged saves. An enemy
  army with fewer than about 80 weighted troops has strength 0, and the original has no guard.

## What this does not establish

- Later play: the corpus runs up to turn 0759.
- Whether natural play produces a strength-0 enemy army that an AI army at war can reach. If it
  does, the original faults.
