# SAV export #37, Q1 addendum: the 31 INERT nation bytes stay untouched through battle, siege, elimination and treaties

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `d6a04fb` (PR #285). It
answers Q1 of research issue [#37](https://github.com/diegoami/imperial-conquest-2-research/issues/37),
option (b), as asked on 2026-10-31. It extends the INERT result of the
[semantic atlas](2026-10-21-original-sav-semantic-atlas.md) to the states the atlas named as its gap.
- **Code:** `runs/experiments/savexport37/q1canary.py`, Unicorn on the pinned EXE with the #187 RAM
  snapshot.
- **Data:** `runs/experiments/data/run-exp-savexport37/q1canary-v1.json`, with the development runs
  `dev1..dev4` kept. No save was written, and the snapshot stays private.

**Tag:** `[confirmed: emulation]`.

**Review note (2026-10-31):**
- **Rerun:** I ran `q1canary.py --version v1` from a scratch copy with the output redirected. The
  result is **byte-identical** to `q1canary-v1.json`.
- **The hook's scope,** read in the script:
  - the canary covers `+0x450..+0x46A`, `+0x46D` and `+0x491..+0x493` (31 offsets) in all 16
    records;
  - the read and write hook spans the whole nation table;
  - an access counts as a hit if any byte it touches is one of those offsets.

## Answer

All 16 nation records get a canary in the 31 bytes, and every seat is set to AI. Only presentation
is stubbed (sound, redraw, news text, the turn title, `TPremierForm_RefreshForms`); the routines and
their RNG run unmodified.

| Path | What ran | Accesses to the 31 bytes | Control accesses (unity +0x440, human +0x490) |
|---|---|---|---|
| treaty `FUN_00450c68`, honourable | war → −18, 1 news line | **0** | 2 / 0 |
| treaty, sues | war → −18; the loser's trades and alliances end | **0** | 2 / 0 |
| instant battle `FUN_0044aee4` | the defender destroyed | **0** | 7 / 2 |
| siege `FUN_0044b27c` → capture → elimination | the victim's unity → 0 | **0** | 7 / 1 |
| a full AI round, `FUN_0044fa20` × 16 seats | diplomacy, economy, armies, fleets | **0** | 4,446 / 213 |

In every case the canary bytes are unchanged afterwards. **So within this scope, INERT also holds for
battle, siege, capture, elimination, both treaty branches and a whole AI round.** The exporter policy
is unchanged: PRESERVE_OR_ZERO, and byte identity with an original lineage still carries the source
bytes. The atlas's 812 indirect edges did not need resolving (option (a)).

## What this does not establish

- **Paths not run:** rebellion and revival (`FUN_0044c360`), the human's dialogs, tactical battles,
  and the round, weekly and quarterly ticks outside the AI seat turn.
- **Copies elsewhere:** the hook covers the nation table only. A copy of the record elsewhere is seen
  only when the copy reads the 31 bytes.
- **One state:** the snapshot is a single state, and the outcomes follow its RNG.
- Native Windows behaviour.
