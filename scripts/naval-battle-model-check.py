#!/usr/bin/env python3
"""Checks the naval-battle trials of ic2-conquest's run-exp-naval-battle against the decompiled rule.

Usage: gh release download run-exp-naval-battle --repo diegoami/ic2-conquest --pattern trials.json
       python3 scripts/naval-battle-model-check.py trials.json

The rule (FUN_0044B5D0 / FUN_0044B4F8, docs/reports/decompiled-diplomacy-peace-terms-and-instant-battles.md):
  base = ships * condition // 10;  strength = base + random(4) * (base // 10)   (a 0/10/20/30 % bonus, integers)
  the attacker wins only if strength(defender) < strength(attacker)               (ties go to the defender)
  r = max(1, loserStrength * 100 // winnerStrength);  d = r * r // 100
  the winner loses ships * d // 300 ships and condition * d // 300 condition.
Prints, per cell, the observed attacker wins against the rule's exact win probability (16 equally likely
bonus pairs), the log-likelihood and chi-square of the rule over all cells, a continuous-uniform
0..30 % model for comparison, and how many battles have an observed (ships lost, condition lost) pair that
the damage formula reproduces for at least one bonus pair consistent with the observed winner.
"""
import collections, json, math, sys

def base(s, c): return s * c // 10
def strength(b, k): return b + k * (b // 10)

def p_discrete(A, D):
    ba, bd = base(*A), base(*D)
    return sum(strength(bd, kd) < strength(ba, ka) for ka in range(4) for kd in range(4)) / 16

def p_uniform(A, D, w=0.3, n=400):
    ba, bd = A[0] * A[1] / 10, D[0] * D[1] / 10
    return sum(bd * (1 + w * (j + .5) / n) < ba * (1 + w * (i + .5) / n) for i in range(n) for j in range(n)) / n / n

def fleet(t, key): return (t[key]['ships'], t[key]['condition'])

def main(path):
    trials = json.load(open(path))
    cells = collections.OrderedDict()
    for t in trials: cells.setdefault(t['cell'], []).append(t)
    ll = {'discrete': 0.0, 'uniform': 0.0}; chi = {'discrete': 0.0, 'uniform': 0.0}
    print('cell   n  attacker wins  exact rule (expected)  uniform 0-30 % (expected)  attacker v defender (base)')
    for c, ts in cells.items():
        A, D = fleet(ts[0], 'attacker_before'), fleet(ts[0], 'defender_before')
        assert all(fleet(t, 'attacker_before') == A and fleet(t, 'defender_before') == D for t in ts), c
        n, k = len(ts), sum(t['attacker_alive'] for t in ts)
        row = []
        for name, p in (('discrete', p_discrete(A, D)), ('uniform', p_uniform(A, D))):
            q = min(max(p, 1e-12), 1 - 1e-12)
            ll[name] += k * math.log(q) + (n - k) * math.log(1 - q)
            v = n * p * (1 - p)
            chi[name] += ((k - n * p) ** 2 / v) if v > 1e-9 else 0.0
            row.append(f'{p:.4f} ({n * p:.1f})')
        print(f'{c:5} {n:3} {k:8d}        {row[0]:18}   {row[1]:18}   {A} {base(*A)} v {D} {base(*D)}')
    print('log-likelihood: exact rule %.2f, uniform %.2f; chi-square: exact rule %.2f, uniform %.2f (%d cells)'
          % (ll['discrete'], ll['uniform'], chi['discrete'], chi['uniform'], len(cells)))
    ok = 0
    for t in trials:
        a, d, aw = fleet(t, 'attacker_before'), fleet(t, 'defender_before'), t['attacker_alive']
        w = a if aw else d
        after = t['attacker_after'] if aw else t['defender_after']
        lost_s, lost_c = w[0] - after['ships'], w[1] - after['condition']
        found = False
        for ka in range(4):
            for kd in range(4):
                sa, sd = strength(base(*a), ka), strength(base(*d), kd)
                if (sd < sa) != aw: continue
                ws, ls = (sa, sd) if aw else (sd, sa)
                dd = max(1, ls * 100 // ws) ** 2 // 100
                found |= w[0] * dd // 300 == lost_s and w[1] * dd // 300 == lost_c
        ok += found
    print('damage formula reproduces the observed (ships lost, condition lost) in %d of %d battles' % (ok, len(trials)))

if __name__ == '__main__':
    main(sys.argv[1])
