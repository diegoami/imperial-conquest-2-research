# Research37 SAV export intake running notes

Plan: verify the pinned ic2-conquest PR #100 source packet against source, public saves, DAT and bounded original x86; promote only the partial safety result; correct related serialization prose; keep the writer and Windows gate open.

Owner choice: Codex Sol medium subagent implements. The quota service suggested MiniMax M3 (rank 1, spare seven-day capacity, reliability factor 0.962); this suggestion did not select the implementer. Owner selected Gemini Flash for the independent PR review; the parent session will run it after this handoff.

Progress — commit 1: independently checked the v2 matrix (33 contiguous regions, 1,172 bytes, 31 UNKNOWN), 14 public SHA256 saves and 224 nation owned-city lists/baselines, DAT hash and 16 profiles, source hash and all 1,111 focused lines. Reran ten original-x86 controls on the pinned executable; generated JSON exactly matches the retained v2 result. Promoted the partial report, corrected the old serialization layout, and updated ledger, evidence index, rules summary, pending gate and README count. `git diff --check` and relative-link checks passed. No private owner saves, candidate exports or Windows outputs were supplied to this intake; no live game was run.

## Reproducible intake receipt

All packet paths below are at ic2-conquest `ac958a0fa58984098641a7992a42d0fbf517d473` under `runs/experiments/data/run-exp-sav-export37/`. Their SHA256s at intake:

| Artifact | SHA256 |
|---|---|
| `nation-matrix-v2.csv` | `7a087d53d2e1b983834a39a928c63f298c3efd0dd9ca0ece69c1a2769abc5fd5` |
| `public-scalar-audit-initial.json` | `7824735f2f8f56a2bf22db69f769a44fd36815f46ef1bb88ede914b9d4bcdce4` |
| `dat-profile-initial.json` | `cb1ae4b78332249d41c33b89e381fdeb6a73f353d8b3fcb61b8ae694fe7fbba6` |
| `source-focused-v1.txt` | `bf229a5cc6c64e37d7cbc3ad8f5f5d35d7d12a1db371914193bcc03aabcda9e2` |
| `x86-controls-v2.json` | `69d640e9ee224dd6e9878fb083196a248e5c793770325d78dc5a04af7164c6da` |

The independent raw-save decoder read each of the fourteen filenames in `public-scalar-audit-initial.json` from the tracked ic2-conquest `saves/` directory and checked its SHA256 before parsing. It found army count as little-endian signed WORD at absolute `100956`, skipped `100958 + 656*army_count` to the fleet count, then skipped `2 + 26*fleet_count` to the sixteen 1,172-byte nation records. It decoded all 334 city owners from city-record `+18` at `89600 + 34*city_id`; each nation record's current count at `+446` and 334 signed city IDs at `+048`; and asserted each active list equals the owned city IDs sorted by raw ASCII city-name bytes, with every inactive ID `-1`. All 224 records passed. In each record, `+450..46A`, `+46D` and `+491..493` were zero in this sampled family; that observation does not establish a default. The decoder directly compared current population/treasury at `+430/+438` with historical fields `+434/+43C`, and checked the three historical values against sixteen independently decoded DAT records (`0x1B100 + 1055*n`, baseline offsets `+1033/+1037`, count `+1047`). All 224 historical triples matched; current treasury differed from its historical baseline in 131 records. The DAT SHA256 was `94d0ccfc67148d727de4c4e60aefc3c53ba9e67775bd689f0fcb2e23c12e5fbd`.

The independent matrix parser converted each hex `first,last` pair to an inclusive interval, checked the declared byte length, and asserted their concatenation equals `range(1172)`. Exactly 33 intervals cover the record without gaps or overlap; three `UNKNOWN_REJECT_CHANGED_STATE` intervals total 31 bytes. The original whole-source SHA256 was `2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8`; every one of the 1,111 numbered focused lines matched that source at its original line number. This is a source/extract identity check, not exhaustive read-path analysis.

The bounded control rerun used the pinned recovery layout and wrote only a new `/tmp` result:

```bash
cd /home/diego/projects/ic2-work/sav-export37/conquest
python3 runs/experiments/sav_export37/controls.py --output /tmp/sav37-controls-intake.json
python3 runs/experiments/sav_export37/validate_packet.py --output /tmp/sav37-packet-intake.json
```

The ten-control result was JSON-equal and SHA256-equal (`69d640e9ee224dd6e9878fb083196a248e5c793770325d78dc5a04af7164c6da`) to the retained v2 file: ten passes, zero errors. The offline packet validator reported 14 saves, 224 records, 247 functions, 2,040 references, 1,111 focused lines, ten controls, 33 regions, 1,172 bytes and 31 UNKNOWN bytes, with `Windows_output_round_trips: 0` and `changed_state_export_readiness: false`. Neither command ran the game or produced an exported SAV.

Progress — commit 2: made the independent check receipt durable with pinned packet hashes, raw offset and assertion method, and bounded x86 reproduction command.

END: research #37 and main #1194/T185 remain open; three native Windows output round trips and changed-state semantics remain unmet. Task #25 and immutable fixtures were not changed. PR review and merge belong to the parent session.
