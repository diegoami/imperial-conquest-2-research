#!/usr/bin/env python3
"""Checks the pair-2 trials of ic2-conquest's run-exp-pair2 against the decompiled naval rule, and tests whether the
random bonuses follow the ROLE (attacker drawn first) or the FLEET.

Usage: gh release download run-exp-pair2 --repo diegoami/ic2-conquest --pattern trials.json
       python3 scripts/naval-pair2-check.py trials.json

Rule (docs/reports/decompiled-diplomacy-peace-terms-and-instant-battles.md): base = ships * condition // 10,
strength = base + k * (base // 10) with k = Random(4) drawn for the attacker first, then the defender; the attacker
wins only if the defender's strength is strictly smaller; the winner then loses ships * d // 300 ships and
condition * d // 300 condition with d = max(1, loser*100 // winner) ** 2 // 100.
For each seed the script looks for a pair (k_attacker, k_defender) that reproduces the winner AND the exact damage in
both cells (role-based: the same pair in both cells), and for a pair (k_fleet1, k_fleet2) that does it with the
draws attached to the fleets (the pair swaps places between the cells).
"""
import collections, json, sys

def base(s, c): return s * c // 10
def st(b, k): return b + k * (b // 10)

def consistent(t):
    a, d = t['attacker_before'], t['defender_before']
    ba, bd = base(a['ships'], a['condition']), base(d['ships'], d['condition'])
    aw = t['attacker_alive'] and not t['defender_alive']
    w, wa = (a, t['attacker_after']) if aw else (d, t['defender_after'])
    lost = (w['ships'] - wa['ships'], w['condition'] - wa['condition'])
    ok = set()
    for ka in range(4):
        for kd in range(4):
            sa, sd = st(ba, ka), st(bd, kd)
            if (sd < sa) != aw: continue
            ws, ls = (sa, sd) if aw else (sd, sa)
            dd = max(1, ls * 100 // ws) ** 2 // 100
            if (w['ships'] * dd // 300, w['condition'] * dd // 300) == lost: ok.add((ka, kd))
    return ok

def main(path):
    T = [t for t in json.load(open(path)) if 'error' not in t]
    cells = collections.OrderedDict()
    for t in T: cells.setdefault(t['cell'], {})[t['seed']] = t
    for c, ts in cells.items():
        t0 = next(iter(ts.values())); a, d = t0['attacker_before'], t0['defender_before']
        ba, bd = base(a['ships'], a['condition']), base(d['ships'], d['condition'])
        p = sum(st(bd, kd) < st(ba, ka) for ka in range(4) for kd in range(4)) / 16
        k = sum(t['attacker_alive'] for t in ts.values())
        print(f"{c}: attacker {a['ships']}x{a['condition']} base {ba} v defender {d['ships']}x{d['condition']} base {bd}: "
              f"exact P(attacker wins) {p:.4f}, expected {len(ts) * p:.2f}, observed {k} of {len(ts)}")
    print('trials whose winner and exact damage fit some bonus pair:', sum(bool(consistent(t)) for t in T), 'of', len(T))
    names = list(cells)
    if len(names) == 2:
        x, y = cells[names[0]], cells[names[1]]
        seeds = sorted(set(x) & set(y))
        role = {s: sorted(consistent(x[s]) & consistent(y[s])) for s in seeds}
        fleet = {s: sorted(consistent(x[s]) & {(b, a) for (a, b) in consistent(y[s])}) for s in seeds}
        print('seeds explained by ONE pair of role-based bonuses (same pair in both cells): %d of %d' % (sum(bool(v) for v in role.values()), len(seeds)))
        print('   ', role)
        print('seeds explained by ONE pair of fleet-based bonuses (the pair swaps with the roles): %d of %d' % (sum(bool(v) for v in fleet.values()), len(seeds)))
        print('   ', fleet)

if __name__ == '__main__':
    main(sys.argv[1])
