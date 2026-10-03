#!/usr/bin/env python3
"""Checks the storm trials of ic2-conquest's run-exp-storms against the decompiled storm pass.

Usage: gh release download run-exp-storms --repo diegoami/ic2-conquest --pattern t4_trials.json
       python3 scripts/storm-model-check.py t4_trials.json

The storm pass (docs/reports/supply-driven-morale-and-fleet-attrition.md, fleet loop, steps 1-2 and 4):
  supplies -= ships;  dmg = max(1, Random(100 - condition) // 10)
  winter: dmg = min(5, dmg * 2);  rough sea (covered field 1): dmg = min(8, dmg * 3)
  away from a friendly coast: dmg = dmg * 2 + 1, and in winter Random(20) == 0 makes it 30;  next to one: dmg //= 2
  dmg < 6: condition -= dmg;  else r = max(1, 10000 // (dmg + 100)), d = r * r // 100,
           ships -= ships * d // 300, condition -= condition * d // 300
  condition < 40: the fleet is lost;  then, with 0 supplies, condition -= Random(2)
Every Random(n) is uniform on 0 .. n-1.  For each cell the script enumerates the draws, prints the exact outcome
distribution next to the observed counts, and reports whether every observed outcome is possible and the exact
probability of seeing a result at least as unlikely as the observed one (a multinomial tail, by simulation).
The trials of a cell use different seeds, so a cell's trials are independent samples; cells share seeds.
"""
import collections, json, random, sys

def outcomes(ships, cond, winter, rough, near, no_supply):
    """-> {outcome: probability}; outcome = 'lost' or (ships_lost, condition_lost)."""
    out = collections.Counter()
    n1 = 100 - cond
    for r1 in range(n1):
        dmg0 = max(1, r1 // 10)
        base = dmg0
        if winter: base = min(5, base * 2)
        if rough: base = min(8, base * 3)
        branches = []
        if near:
            branches = [(base // 2, 1.0)]
        else:
            b = base * 2 + 1
            branches = [(b, 19 / 20), (30, 1 / 20)] if winter else [(b, 1.0)]
        for dmg, pw in branches:
            s, c = ships, cond
            if dmg < 6:
                c -= dmg
            else:
                r = max(1, 10000 // (dmg + 100)); d = r * r // 100
                s -= ships * d // 300; c -= cond * d // 300
            if c < 40:
                out['lost'] += pw / n1
                continue
            if no_supply:
                for x in (0, 1): out[(ships - s, cond - (c - x))] += pw / n1 / 2
            else:
                out[(ships - s, cond - c)] += pw / n1
    return out

def cell_params(name):
    return dict(rough=name[0] == 'R', near=name[0] == 'H', winter=name[-1] == 'w' or name.endswith('wA'))

def observed(t, key):
    b, a = t[key + 'before'], t.get(key + 'after')
    if a is None or a.get('owner') == -1: return 'lost'
    return (b['ships'] - a['ships'], b['condition'] - a['condition'])

def tail_p(dist, counts, n, trials=20000, seed=1):
    keys = list(dist); w = [dist[k] for k in keys]
    import math
    def logp(c):
        # multinomial log-probability up to the (shared) coefficient: sum n_k log p_k - sum log n_k!
        return sum(m * math.log(dist[k]) - math.lgamma(m + 1) for k, m in c.items())
    lp = logp(counts); rnd = random.Random(seed); hit = 0
    for _ in range(trials):
        c = collections.Counter(rnd.choices(keys, w, k=n))
        hit += logp(c) <= lp + 1e-9
    return hit / trials

def main(path):
    T = [t for t in json.load(open(path)) if 'error' not in t]
    cells = collections.OrderedDict()
    for t in T: cells.setdefault(t['cell'], []).append(t)
    print('Carthage fleet 0 (zero supplies at the tick):')
    for name, ts in cells.items():
        P = cell_params(name); b = ts[0]['before']
        dist = outcomes(b['ships'], b['condition'], P['winter'], P['rough'], P['near'], True)
        obs = collections.Counter(observed(t, '') for t in ts)
        impossible = [k for k in obs if dist.get(k, 0) == 0]
        p = tail_p(dist, obs, len(ts))
        exp_lost = dist.get('lost', 0)
        print(f'{name:6} n={len(ts):2}  observed {dict(obs)}')
        print(f'        expected lost {exp_lost:.2f} of 1; impossible outcomes seen: {impossible or "none"}; '
              f'chance of a result this unlikely or worse: {p:.2f}')
    print('\nPtolemaic fleet 1 (70 ships, condition 75, 10 tons of supplies left, calm sea away from cities), one per seed:')
    for season in ('s', 'w'):
        sel = [t for name, ts in cells.items() if name.endswith(season) for t in ts]
        per = collections.defaultdict(set)
        for t in sel: per[t['seed']].add(observed(t, 'ptolemaic_'))
        one = [next(iter(v)) for v in per.values() if len(v) == 1]
        dist = outcomes(70, 75, season == 'w', False, False, False)
        print(f'  {"Winter" if season == "w" else "Spring"}: {len(per)} seeds, same result in every cell for {len(one)} of them; '
              f'observed {dict(collections.Counter(one))}')
        print('     expected', {k: round(v, 3) for k, v in sorted(dist.items(), key=lambda x: -x[1])[:6]})

if __name__ == '__main__':
    main(sys.argv[1])
