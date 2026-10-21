#!/usr/bin/env python3
"""Audit sixteen immutable battle-sweep saves for research #40.

Usage: python3 -I scripts/research40-grid-check.py SAVE_DIRECTORY
Optional --hashes selects the manifest; --output writes a scalar JSON receipt.
No game, emulator or port replay is executed. Only original retained bytes are read.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def check(saves, hashes):
    manifest = json.loads(hashes.read_text())
    decoded = {}
    for name, expected in manifest['saves'].items():
        data = (saves / name).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != expected:
            raise ValueError(f'{name}: SHA256 mismatch')
        # Fixed trailing block for this pinned lab corpus, not a general SAV reader.
        block = data[-2105:]
        if len(block) != 2105:
            raise ValueError(f'{name}: short battle block')
        slots = [struct.unpack_from('<10h', block, 9 + 44 * i) for i in range(40)]
        grid = struct.unpack_from('<168h', block, 1769)
        decoded[name] = {
            'sha256': digest,
            'side': struct.unpack_from('<h', block, 4)[0],
            'placed': block[6],
            'counter': struct.unpack_from('<h', block, 7)[0],
            'live_slots': [dict(zip(
                ('slot', 'x', 'y', 'label', 'type', 'troops', 'quality',
                 'morale', 'moves', 'shots', 'target'), (i, *w)))
                for i, w in enumerate(slots) if w[4] > 0],
            'nonempty_grid': [[x, y, grid[x * 12 + y]]
                              for x in range(14) for y in range(12)
                              if grid[x * 12 + y] != 50],
        }

    def require(condition, label):
        if not condition:
            raise ValueError(label)

    def slot(name, index):
        return next(s for s in decoded[name]['live_slots'] if s['slot'] == index)

    for case, before, after in (('c5_stale_grid', 2, 3),
                                 ('c6_same_cell', 2, 3), ('d5_stale_grid', 1, 2)):
        first, last = (f'b3_{case}_BATTLE{n:02}.SAV' for n in (before, after))
        a, b = slot(first, 20), slot(last, 20)
        require((a['x'], a['y'], a['moves']) == (4, 9, 2), first)
        require((b['x'], b['y'], b['moves']) == (4, 7, 0), last)
        require(all(c[:2] != [4, 9] for c in decoded[first]['nonempty_grid']), first)
        require(all(c[:2] != [4, 7] for c in decoded[last]['nonempty_grid']), last)
        for name in (first, last):
            require(len(decoded[name]['live_slots']) == 2, name)
            require(all(s['troops'] == 6000 and s['shots'] == 0
                        for s in decoded[name]['live_slots']), name)
    for n in (1, 2, 3):
        a, b = (decoded[f'b3_{case}_BATTLE{n:02}.SAV']['sha256']
                for case in ('c5_stale_grid', 'c6_same_cell'))
        require(a == b, f'c5/c6 BATTLE{n:02} identity')
    first = 'CRAFT_d6_same_cell.SAV'
    require([(s['x'], s['y']) for s in decoded[first]['live_slots']]
            == [(4, 9), (4, 9)], 'd6 original overlap')
    last = 'b3_d6_same_cell_BATTLE01.SAV'
    a, b = slot(last, 0), slot(last, 20)
    require((a['x'], a['y'], a['moves'], a['target']) == (3, 8, 1, 20), last)
    require((b['x'], b['y']) == (4, 9), last)
    require(decoded[last]['nonempty_grid'] == [[3, 8, 5]], last)
    return {'scope': 'retained original Wine saves; no execution or port replay',
            'save_count': len(decoded), 'checks': 'PASS', 'saves': decoded}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('saves', type=Path)
    parser.add_argument('--hashes', type=Path, default=Path(__file__).resolve().parents[1]
                        / 'docs/data/research40-save-hashes.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = check(args.saves, args.hashes)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(f"PASS: {result['save_count']} hashes, three movement boundaries, "
          'three c5/c6 whole-save pairs and d6 overlap/boundary')


if __name__ == '__main__':
    main()
