#!/usr/bin/env python3
"""Checks the army-aboard naval trials of ic2-conquest's run-exp-naval-battle-cargo against the decompiled rule.

Usage: gh release download run-exp-naval-battle-cargo --repo diegoami/ic2-conquest --pattern t3_trials.json
       python3 scripts/naval-cargo-check.py t3_trials.json

Rule (docs/reports/decompiled-diplomacy-peace-terms-and-instant-battles.md, FUN_0044B5D0 / FUN_0044B4F8):
  base = ships * condition // 10 + siegeStrength(army) // 50,  siegeStrength = (troops * (3 if archers else 1)) // 80 * morale
  strength = base + random(4) * (base // 10); the attacker wins only if strength(defender) < strength(attacker)
  r = max(1, loserStrength * 100 // winnerStrength); d = r * r // 100; the winner loses ships * d // 300 ships;
  its carried army takes casualties with ratio d (about d / (105..119) of its troops), and when d > 70 loses
  unitCount * d // 250 + 1 whole units: a one-unit army is always destroyed.
Prints (1) the exact win probability per cell against the observed wins, with the log-likelihood and a sweep of the
cargo divisor; (2) for the won battles of one-unit armies, whether the army's loss agrees with 'all lost iff d > 70,
otherwise a fraction within d/119 .. d/105', with d bounded by the observed ship loss.
"""
import collections, json, math, sys

# siege-weighted troops per cell where the unit types matter (archers count three times); trials.json holds only totals:
# A5 = 5,000 archers; M15 = 4,000 + 3,000 + 2,000 archers x 3 + 1,000 + 1,000 = 15,000
WEIGHTED = {'A5': 15000, 'M15': 15000}
def siege(troops, cell, morale): return WEIGHTED.get(cell, troops) // 80 * morale
def strength(b, k): return b + k * (b // 10)
def p_attacker(ba, bd): return sum(strength(bd, kd) < strength(ba, ka) for ka in range(4) for kd in range(4)) / 16

def main(path):
    trials = [t for t in json.load(open(path)) if 'error' not in t]
    cells = collections.OrderedDict()
    for t in trials: cells.setdefault(t['cell'], []).append(t)

    def bases(ts, div):
        t0 = ts[0]; a, d = t0['attacker_before'], t0['defender_before']
        ca = siege(t0['att_army_before']['troops'], t0['cell'], t0['att_army_before']['morale']) // div if a['army'] >= 0 else 0
        cd = siege(t0['def_army_before']['troops'], 'D', t0['def_army_before']['morale']) // div if d['army'] >= 0 else 0
        return a['ships'] * a['condition'] // 10 + ca, d['ships'] * d['condition'] // 10 + cd

    print('cell   n  wins  exact-rule P(attacker)  (expected)   base attacker v defender at /50')
    ll = 0.0
    for c, ts in cells.items():
        ba, bd = bases(ts, 50); n, k = len(ts), sum(t['attacker_alive'] for t in ts); p = p_attacker(ba, bd)
        q = min(max(p, 1e-9), 1 - 1e-9); ll += k * math.log(q) + (n - k) * math.log(1 - q)
        print(f'{c:6}{n:3}{k:6}   {p:.4f}                 ({n * p:.2f})       {ba} v {bd}')
    print('log-likelihood at /50: %.2f' % ll)
    sweep = {}
    for div in (30, 35, 40, 45, 50, 55, 60, 70):
        tot = 0.0
        for c, ts in cells.items():
            ba, bd = bases(ts, div); n, k = len(ts), sum(t['attacker_alive'] for t in ts)
            p = min(max(p_attacker(ba, bd), 1e-3), 1 - 1e-3); tot += k * math.log(p) + (n - k) * math.log(1 - p)
        sweep[div] = round(tot, 1)
    print('divisor sweep (probabilities clipped to 1e-3):', sweep)

    n_ok = n_bad = n_all = 0
    for t in trials:
        if t['cell'] == 'M15': continue          # a five-unit army: casualties fall unit by unit, see below
        a, d = t['attacker_before'], t['defender_before']
        aw = t['attacker_alive'] and not t['defender_alive']; dw = t['defender_alive'] and not t['attacker_alive']
        if aw: w, wa, ar = a, t['attacker_after'], ('att_army_before', 'att_army_after')
        elif dw: w, wa, ar = d, t['defender_after'], ('def_army_before', 'def_army_after')
        else: continue
        if w['army'] < 0: continue
        S, s = w['ships'], w['ships'] - wa['ships']
        lo, hi = -(-300 * s // S), -(-300 * (s + 1) // S) - 1          # d consistent with ships * d // 300 == s
        before, after = t[ar[0]], t[ar[1]]
        dead = after['owner'] == -1
        frac = 1.0 if dead else 1 - after['troops'] / before['troops']
        ok = hi >= 71 if dead else (lo <= 70 and lo / 119 - 0.02 <= frac <= hi / 105 + 0.02)
        n_all += dead; n_ok += ok; n_bad += not ok
    print('won battles of one-unit armies: %d; all lost %d, partial %d; inconsistent with the rule: %d'
          % (n_ok + n_bad, n_all, n_ok + n_bad - n_all, n_bad))
    # the five-unit army (M15): total troops left against d, which the ship loss bounds
    m = []
    for t in trials:
        if t['cell'] != 'M15' or not t['attacker_alive']: continue
        S, s = t['attacker_before']['ships'], t['attacker_before']['ships'] - t['attacker_after']['ships']
        lo, hi = -(-300 * s // S), -(-300 * (s + 1) // S) - 1
        left = 0 if t['att_army_after']['owner'] == -1 else t['att_army_after']['troops']
        m.append((lo, hi, left))
    print('M15 (11,000 men, five units): (d low, d high, troops left) =', sorted(m))
    print('  d <= 70 everywhere in %s; d > 70 everywhere in %s' % (
        [x for x in sorted(m) if x[1] <= 70], [x for x in sorted(m) if x[0] > 70]))

if __name__ == '__main__':
    main(sys.argv[1])

