#!/usr/bin/env python3
"""Reads the tactical-battle block of ic2-conquest's lab-build saves independently of the bot's decoder, using only the
layout in docs/reports/2026-10-04-decompiled-tactical-battle-rules.md, and checks the byte-identity claims.

Usage: python3 scripts/battle-block-check.py <dir with the downloaded .SAV files>
  gh release download run-exp-battle-probe --repo diegoami/ic2-conquest --pattern 'gate2_*.SAV' --pattern 'lab1_t0_*.SAV' \
      --pattern 'resume05_gate2_a_r*.SAV' --dir probe
  gh release download run-exp-battle-sweep --repo diegoami/ic2-conquest --pattern 'hi-hi-one_s*_r*_*.SAV' --dir sweep

A save written inside a battle is the 132,149-byte base save plus a 2,105-byte block at its end:
  header 9 bytes: attacker army (2), defender army (2), side (2), placed (1), half-round counter (2)
  40 slots of 44 bytes (22 words): x, y, origin label, type, troops, quality, morale, moves left, shots left, target, name[24]
  14 x 12 words of icon codes, cell(x, y) = [x * 12 + y]: 50 empty, else side * 20 + type * 3 + min(2, troops // (std // 3))
Types 0 LI, 1 HI, 2 archers, 3 LC, 4 HC;  std 15000, 6000, 3500, 7000, 2500;  moves 4/2/4/6/5;  initial shots 7/0/25/9/0.
"""
import collections, glob, hashlib, os, re, struct, sys

BLOCK = 2105
STD = (15000, 6000, 3500, 7000, 2500); MOVES = (4, 2, 4, 6, 5); SHOTS = (7, 0, 25, 9, 0)

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]

def read_block(path):
    d = open(path, 'rb').read()
    if len(d) < 134000: return None
    b = d[-BLOCK:]
    att, dfn, side = struct.unpack_from('<3h', b, 0); placed = b[6]; counter = struct.unpack_from('<h', b, 7)[0]
    slots = []
    for i in range(40):
        w = struct.unpack_from('<10h', b, 9 + 44 * i)
        slots.append(dict(x=w[0], y=w[1], label=w[2], type=w[3], troops=w[4], q=w[5], morale=w[6], moves=w[7], shots=w[8], target=w[9]))
    grid = struct.unpack_from('<168h', b, 9 + 1760)
    return dict(att=att, dfn=dfn, side=side, placed=placed, counter=counter, slots=slots, grid=grid, size=len(d))

def check_grid(blk):
    """-> number of cells whose code differs from the rule (the last live slot at a cell wins)."""
    exp = [50] * 168
    for i, s in enumerate(blk['slots']):
        if s['troops'] > 0 and 0 <= s['x'] < 14 and 0 <= s['y'] < 12:
            exp[s['x'] * 12 + s['y']] = (0 if i < 20 else 20) + s['type'] * 3 + min(2, s['troops'] // (STD[s['type']] // 3))
    return sum(a != b for a, b in zip(exp, blk['grid']))

def series(d, prefix):
    fs = sorted(glob.glob(os.path.join(d, prefix + '_BATTLE*.SAV')))
    return [f for f in fs if re.search(r'BATTLE\d+\.SAV$', f)]

def main(root):
    files = sorted(glob.glob(os.path.join(root, '*', '*.SAV')) + glob.glob(os.path.join(root, '*.SAV')))
    n = bad_grid = bad_morale = bad_target = 0; sizes = collections.Counter()
    first = {}
    for f in files:
        b = read_block(f)
        if not b: continue
        n += 1; sizes[b['size']] += 1
        bad_grid += check_grid(b) > 0
        bad_morale += any(s['morale'] > 99 or (s['troops'] > 0 and s['morale'] < 0) for s in b['slots'])
        bad_target += any(not (-1 <= s['target'] < 40) for s in b['slots'])
    print(f'{n} saves with a battle block; sizes {dict(sizes)} (base 132,149 + {BLOCK} = {132149 + BLOCK})')
    print(f'grid differs from the icon rule in {bad_grid} files; morale above 99 in {bad_morale}; target out of range in {bad_target}')
    # header sequence and first-file contents of a series
    for pref in ('gate2_a', 'gate2_s2a'):
        for d in (os.path.join(root, 'probe'), root):
            fs = series(d, pref)
            if fs:
                hs = [read_block(f) for f in fs]
                print(f'{pref}: {len(fs)} files; attacker/defender {hs[0]["att"]}/{hs[0]["dfn"]}; side {[h["side"] for h in hs[:10]]}'
                      f'; placed {[h["placed"] for h in hs[:6]]}; counter {[h["counter"] for h in hs[:6]]}')
                s0 = hs[0]['slots']
                print('   first file: moves by type', sorted({(s['type'], s['moves']) for s in s0 if s['troops'] > 0}),
                      '| shots by type', sorted({(s['type'], s['shots']) for s in s0 if s['troops'] > 0}))
                break
    # byte identity
    P = os.path.join(root, 'probe')
    def same(group):
        hs = [tuple(sha(f) for f in series(P, g)) for g in group]
        return len(set(hs)) == 1, len(hs[0])
    seed1 = ['gate2_a', 'gate2_b', 'gate2_c', 'gate2_d', 'gate2_e', 'gate2_f', 'lab1_t0']
    ok, k = same([g for g in seed1 if series(P, g)])
    print(f'seed 1: {len([g for g in seed1 if series(P, g)])} series of {k} files, identical file by file: {ok}')
    print('seed 2 twice identical:', same(['gate2_s2a', 'gate2_s2b'])[0] if series(P, 'gate2_s2b') else 'n/a (only s2a downloaded)')
    r1, r2 = series(P, 'resume05_gate2_a_r1'), series(P, 'resume05_gate2_a_r2')
    if r1 and r2:
        orig = series(P, 'gate2_a')[5:]
        print(f'resume: {len(r1)} files; r1 == r2 file by file: {[sha(a) for a in r1] == [sha(b) for b in r2]}; '
              f'any file equal to the original tail: {bool(set(sha(a) for a in r1) & set(sha(b) for b in orig))}')
    # sweep: hi-hi-one runs of a seed
    S = os.path.join(root, 'sweep')
    if os.path.isdir(S):
        for seed in (1, 2, 3):
            runs = [series(S, f'hi-hi-one_s{seed}_r{r}') for r in (1, 2, 3, 4)]
            runs = [r for r in runs if r]
            same_ = len({tuple(sha(f) for f in r) for r in runs}) == 1 if runs else None
            print(f'hi-hi-one seed {seed}: {len(runs)} runs of {len(runs[0]) if runs else 0} files, identical across runs: {same_}'
                  f'; first BATTLE sha {sha(runs[0][0]) if runs else ""}')

if __name__ == '__main__':
    main(sys.argv[1])
