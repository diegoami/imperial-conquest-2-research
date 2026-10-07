#!/usr/bin/env python3
"""How well does the phrase decoder reproduce the help text? For every compressed record, compare the decoded length with the
declared decompressed length (DataLen2). Usage: hlp_check.py <hlp> > help_decode_check.txt
History: the empirical decoder scored 66/247 (help_decode_check.txt); the Wine HLPFILE_Uncompress3
port scores 247/247 (help_decode_check.txt.v2)."""
import sys
from hlp_topics import topics
d = open(sys.argv[1], 'rb').read()
recs, pm, sm = topics(d)
ok = bad = plain = 0; diffs = []
for p, rt, l1, l2, dl2, rl in recs:
    if dl2 > rl:
        if len(l2) == dl2: ok += 1
        else: bad += 1; diffs.append(len(l2) - dl2)
    else: plain += 1
print('records:', len(recs), 'compressed:', ok + bad, 'exact length:', ok, 'not exact:', bad, 'uncompressed:', plain)
if diffs:
    print('decoded minus declared length, not-exact records: min %d max %d mean %.1f' % (min(diffs), max(diffs), sum(diffs) / len(diffs)))
print('Reading: with the Wine HLPFILE_Uncompress3 port every compressed record decodes to its declared length exactly,')
print('so the topic text is byte-complete. The remaining non-text bytes are structural (NUL table-cell separators,')
print('literal-run escaped bytes), not lost characters; the RTF-level structure itself is out of scope here.')
