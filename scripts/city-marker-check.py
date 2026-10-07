#!/usr/bin/env python3
"""Check city marker variants against city records and nation capitals.

Usage: city-marker-check.py <save> [...]

For every save: parses the map array (first 89,600 bytes, element = word at
y*2 + x*0x118, i.e. index y + x*140), the 334-city table at 89,600 (stride 34)
and the nation table (after armies and fleets; capital word at +0x444, unity
at +0x440). Reports the population range per marker variant and whether
variant 4 is exactly the set of live capitals.

Companion to docs/reports/2026-10-07-city-marker-variants.md.
"""
import struct, sys, collections

CITY_BASE = 89600
NCITIES = 334

def parse(path):
    d = open(path, 'rb').read()
    cities = []
    for i in range(NCITIES):
        r = d[CITY_BASE + i*34 : CITY_BASE + (i+1)*34]
        x, y, owner, orig, loyal, supply, fort, pop, maxpop = struct.unpack_from('<9h', r, 0x0E)
        code = struct.unpack_from('<h', d, (y + x*140)*2)[0]
        cities.append(dict(i=i, x=x, y=y, owner=owner, pop=pop, code=code))
    off = CITY_BASE + NCITIES*34
    narm = struct.unpack_from('<h', d, off)[0]; off += 2 + narm*656
    nfle = struct.unpack_from('<h', d, off)[0]; off += 2 + nfle*26
    caps = []
    for n in range(16):
        r = d[off + n*1172 : off + (n+1)*1172]
        unity = struct.unpack_from('<h', r, 0x440)[0]
        capital = struct.unpack_from('<h', r, 0x444)[0]
        caps.append((unity, capital))
    return cities, caps, narm, nfle

def main(paths):
    for path in paths:
        cities, caps, narm, nfle = parse(path)
        live = {c for u, c in caps if u > 0}
        bad = 0
        var_pop = collections.defaultdict(list)
        cap_ok = cap_bad = v4_notcap = 0
        for c in cities:
            if not (20 <= c['code'] < 100) or (c['code'] - 20 - c['owner']) % 16:
                bad += 1
                continue
            v = (c['code'] - 20 - c['owner']) // 16
            var_pop[v].append(c['pop'])
            if v == 4:
                if c['i'] in live: cap_ok += 1
                else: v4_notcap += 1
            elif c['i'] in live:
                cap_bad += 1
        name = path.rsplit('/', 1)[-1]
        print(f"== {name} (armies {narm}, fleets {nfle}, non-conforming {bad}) ==")
        for v in sorted(var_pop):
            ps = sorted(var_pop[v])
            print(f"  variant {v}: n={len(ps):3d}  pop {ps[0]}..{ps[-1]}")
        print(f"  capitals: variant4&cap={cap_ok}  cap&other={cap_bad}  variant4&notcap={v4_notcap}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
