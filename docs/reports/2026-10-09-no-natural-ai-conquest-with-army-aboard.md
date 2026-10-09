# No natural AI conquest of a nation with a loaded fleet in 11 idle seeds (334 end turns): only Carthage, Ptolemaic and Greece load fleets, and none of them falls; an idle Rome is conquered within 29-50 end turns

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit `486f0d2` (run data at
`8dd4cd8`). Release
[`run-exp-ai-conquest-aboard`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-ai-conquest-aboard)
holds the kept autosaves (`IW_*.SAV`) and the `STUCK_*` / `GAMEOVER_*` screenshots, and their
SHA-256s are committed at `runs/experiments/data/run-exp-ai-conquest-aboard/SAVES.sha256`.
Wine-only. This is a negative result for the research request of 2026-10-09: the "natural
pre-state" item of
[`2026-10-09-elimination-removes-fleet-and-army-aboard.md`](2026-10-09-elimination-removes-fleet-and-army-aboard.md).

**Review note:**
- **Logs:** I re-read all 11 per-seed logs (`idle_watch_seed<k>.jsonl`). The table below
  holds, apart from one count in the text:
  - The conquest lines show "Seleucid conquers Galatia." in **6** seeds, not 7. The draft's own
    table has 6 such rows; the text is corrected below.
  - The 8 game-over texts give Gaul ×4, Carthage ×2 and Illyria ×2.
  - The logs have 342 rows, i.e. the 334 end turns plus the final failed or game-over attempt
    in seeds 10-17.
  - Across all seeds, the three nations that loaded fleets never dropped below 34 cities
    (Carthage), 46 (Ptolemaic) and 20 (Greece). None came near conquest.
- **Saves:** I hashed three kept saves (`IW_seed14_039_0759`, `IW_seed15_034_0754`,
  `IW_seed17_036_0756`; OK). For each logged loaded fleet, the map word at its tile is the
  owner's fleet marker in the ≥ 50-ship band (333 Carthage, 335 Ptolemaic, 339 Greece), and the
  logged cargo is that nation's own army.
- **A bias to note:** since `2ad4ebb` the driver answers every post-battle "Offer of peace" with
  No. So the idle Rome stays at war with whoever attacked it, which may shorten its survival
  (28-49 end turns here). It does not change what the AI nations do among themselves.
- The existing-save scan has no saved output (the draft says so). It is accepted as stated.

**Tag:** `[confirmed]` for what was observed; the absence is a sample only.

## Answer

- **Existing saves:** a scan of all 7,618 saves under `artifacts/`, `runs/`, `saves/` and `~/ic2-work` found **no natural case**:
  - the only AI conquest in them is "Seleucid conquers Galatia." (Galatia owned no fleet), already part of the shared history of most fixtures;
  - the only launched fleets with an army aboard are Carthage's early ones and the experiments' own edits.
- **Seeded idle runs:**
  - From `saves/run0-start-AUTO0720-seed12345.SAV` (Rome human, only ending turns), seeds 1-3 and 10-17: 11 seeds, 334 completed end turns, 0721 to 0769.
  - **Conquests seen in the news:** "Seleucid conquers Galatia." in **6** seeds (2, 10, 11, 12, 13, 17; the draft said 7), at 0731-0735 (Galatia had no army and no fleet in the save before), and, at the end of 8 seeds, **Rome itself** conquered (by Gaul ×4, Carthage ×2, Illyria ×2) at end turn 29 to 50. Rome never had a loaded fleet.
  - **Launched fleets with an army aboard:** only **Carthage** (all 11 seeds), **Ptolemaic** (3 seeds, 0745-0759) and **Greece** (1 seed, 0759), each carrying its own army. None of the three lost a city count near conquest in these runs.
  - **No case of an army of another nation aboard** a fleet.
- **For a natural case** one would need a nation that both launches a loaded fleet and is conquered: Carthage, Ptolemaic or Greece, or another nation late in the game. An idle human Rome ends the game too early for that. A longer game would need the human to survive, by playing it or by a stronger starting nation.

| Seed | End turns | Last turn | How it ended | Conquests (turn) | Loaded fleets seen (owner: turns) |
|---:|---:|---:|---|---|---|
| 1 | 3 | 0723 | trial | – | Carthage 0723 |
| 2 | 28 | 0748 | stuck: Offer of peace (fixed in `2ad4ebb`) | Galatia 0735 | Carthage 0723-0724 |
| 3 | 6 | 0726 | stopped for the fix | – | Carthage 0726 |
| 10 | 49 | 0769 | End of Game: Rome conquered by Illyria (stuck before `cee96e0`) | Galatia 0734 | Carthage 0723-0762 |
| 11 | 29 | 0749 | End of Game: Rome conquered by Carthage (stuck before `cee96e0`) | Galatia 0735 | Carthage 0730-0732 |
| 12 | 44 | 0764 | Rome conquered by Gaul | Galatia 0731 | Carthage 0723-0764 |
| 13 | 28 | 0748 | Rome conquered by Gaul | Galatia 0735 | Carthage 0726-0737 |
| 14 | 39 | 0759 | Rome conquered by Gaul | – | Carthage, Ptolemaic 0758-0759, Greece 0759 |
| 15 | 37 | 0757 | Rome conquered by Illyria | – | Carthage, Ptolemaic 0745-0756 |
| 16 | 30 | 0750 | Rome conquered by Carthage | – | Carthage 0730-0732 |
| 17 | 41 | 0761 | Rome conquered by Gaul | Galatia 0731 | Carthage, Ptolemaic 0751-0758 |

## Harness fixes made on the way

- **`end_turn` answers the post-battle "Offer of peace" box** (`2ad4ebb`, default No, verified). An AI army attacking the human's opened it and blocked until the timeout.
- **`end_turn` raises `GameOver(text)`** on the "End of Game" window (`cee96e0`). Seen working live in seeds 12-17.

Both are in `tests/results.md`.

## Evidence

- **Data:** `runs/experiments/data/run-exp-ai-conquest-aboard/`: `idle_watch.py`, `idle_watch_seed<k>.jsonl` (one line per end turn: loaded fleets, new conquest lines, cities per owner), `idle_summary.json` (`summarise.py`), `idle_watch.log`, `SAVES.sha256`.
- **Release** `run-exp-ai-conquest-aboard`: every autosave with a loaded fleet or a new conquest line (`IW_seed<k>_<end>_<turn>.SAV`), and the `STUCK_*` / `GAMEOVER_*` screenshots.
- **The existing-save scan** was a one-off read with no saved output. Its result is stated above and can be redone with the same test: launched fleets with `+22 >= 0` and news lines matching "X conquers Y".

## Not established

- Any natural case. The cleanup on conquest is established only with the edited pre-state (`c288059`) and in code.
- A defection elimination (`FUN_0044BED8`) in play.
