#!/usr/bin/env python3
"""Intake re-read of the run-exp-ai-turn saves: recompute the week-11 tax rule
(reports/2026-10-07-strategic-ai-turn.md §2.3, as corrected by the corroboration) and the free
AI mercenary hire (§3.2) from the raw SAVs, independently of the bot's snapshots.
Usage: ai-turn-intake-check.py <dir-with-AUTO*.SAV> [<ic2-conquest checkout>]
The second argument (default: sibling checkout ../ic2-conquest) supplies state/sav.py — this
repo does not vendor the parser."""
import glob, os, struct, sys

CONQUEST = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'ic2-conquest')
sys.path.insert(0, os.path.abspath(CONQUEST))
import state.sav as SAV  # noqa: E402


def snap(path):
    b = open(path, 'rb').read()
    return SAV.parse(b)


def tax_rule(n):
    """§2.3 sequential rules from a nation row at turn start. Returns
    (tax_out, cut, raise_unconditional, raise_blocked, zero). The raise's own<=threat half is
    not save-visible: it can matter only when 0 <= treasury < 1000."""
    tax, unity, tre, w = n['tax'], n['unity'], n['treasury'], n['wealth']
    cut = unity < 650 or tre > w // 2000
    raise_uncond = tre < 0       # fires regardless of threat
    raise_blocked = tre >= 1000  # both disjuncts impossible
    t = tax
    if cut: t = max(5, t - 6)
    if raise_uncond: t = min(40, t + 9)
    zero = tre > 0 and unity < 500
    if zero: t = 0
    return t, cut, raise_uncond, raise_blocked, zero


files = sorted(glob.glob(os.path.join(sys.argv[1], 'AUTO*.SAV')))
snaps = {os.path.basename(f): snap(f) for f in files}
order = sorted(snaps)
print('saves:', ', '.join(order))

# --- check 1: the week-11 tax policy. The rule fires only in the transition INTO a week-11 save. ---
rows = mismatch = undec = nonweek_moves = 0
for a, b in zip(order, order[1:]):
    A, B = snaps[a], snaps[b]
    if B['week'] != 11:
        for na, nb in zip(A['nations'], B['nations']):
            if na['id'] != 0 and na['tax'] != nb['tax']:
                nonweek_moves += 1
                print('NON-WEEK-11 MOVE', a, '->', b, na['name'], na['tax'], nb['tax'])
        continue
    for na, nb in zip(A['nations'], B['nations']):
        if na['id'] == 0:
            continue  # human control
        exp, cut, ru, rb, zero = tax_rule(na)
        if ru or rb:
            rows += 1
            if nb['tax'] != exp:
                mismatch += 1
                print('MISMATCH', a, '->', b, na['name'], na['tax'], '->', nb['tax'],
                      'expected', exp, '(cut=%s raise=%s)' % (cut, ru))
        else:  # 0 <= treasury < 1000: the threat branch could add +9
            undec += 1
            if nb['tax'] != exp and nb['tax'] != min(40, exp + 9):
                mismatch += 1
                print('MISMATCH even allowing threat-raise', a, b, na['name'],
                      na['tax'], nb['tax'], exp)
print('week-11 rows: %d decidable (%d matched, %d mismatch), %d with undecided threat branch; '
      'moves at non-week-11 transitions: %d' % (rows + undec, rows - mismatch, mismatch, undec, nonweek_moves))
print('Rome (human) tax per save:', [snaps[n]['nations'][0]['tax'] for n in order])

# --- check 2: the two natural hires (Gaul Felsina; Carthage both Theveste offers) ---
for (a, b), nation, aid, slots in (
        (('AUTO0720.SAV', 'AUTO0721.SAV'), 'Gaul', 9, (13,)),
        (('AUTO0721.SAV', 'AUTO0722.SAV'), 'Carthage', 3, (0, 4))):
    A, B = snaps[a], snaps[b]
    na = next(n for n in A['nations'] if n['name'] == nation)
    nb = next(n for n in B['nations'] if n['name'] == nation)
    arma = next(x for x in A['armies'] if x['id'] == aid)
    armb = next(x for x in B['armies'] if x['id'] == aid)
    pa = {m['slot']: m for m in A['mercenaries']}
    pb = {m['slot']: m for m in B['mercenaries']}
    for sl in slots:
        m = pa.get(sl)
        print(nation, 'pool slot', sl, 'before', m, '; after',
              'EMPTIED' if m and sl not in pb else pb.get(sl))
    print(nation, 'army', aid, 'money', arma['money'], '->', armb['money'],
          '; treasury', na['treasury'], '->', nb['treasury'])
