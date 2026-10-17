# Research37 SAV export intake running notes

Plan: verify the pinned ic2-conquest PR #100 source packet against source, public saves, DAT and bounded original x86; promote only the partial safety result; correct related serialization prose; keep the writer and Windows gate open.

Owner choice: Codex Sol medium subagent implements. The quota service suggested MiniMax M3 (rank 1, spare seven-day capacity, reliability factor 0.962); this suggestion did not select the implementer. Owner selected Gemini Flash for the independent PR review; the parent session will run it after this handoff.

Progress — commit 1: independently checked the v2 matrix (33 contiguous regions, 1,172 bytes, 31 UNKNOWN), 14 public SHA256 saves and 224 nation owned-city lists/baselines, DAT hash and 16 profiles, source hash and all 1,111 focused lines. Reran ten original-x86 controls on the pinned executable; generated JSON exactly matches the retained v2 result. Promoted the partial report, corrected the old serialization layout, and updated ledger, evidence index, rules summary, pending gate and README count. `git diff --check` and relative-link checks passed. No private owner saves, candidate exports or Windows outputs were supplied to this intake; no live game was run.

END: research #37 and main #1194/T185 remain open; three native Windows output round trips and changed-state semantics remain unmet. Task #25 and immutable fixtures were not changed. PR review and merge belong to the parent session.
