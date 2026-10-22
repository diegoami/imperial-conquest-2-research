#!/usr/bin/env python3
"""Re-decodes ic2-conquest's run-exp-manual-gaps saves (PR #140) for research's intake.

    rclone copy gdrive:IC2/artifacts/run-exp-manual-gaps/saves <dir>
    python3 -I scripts/manual-gaps-intake-check.py --saves <dir> \
        --sums ../ic2-conquest/runs/experiments/data/run-exp-manual-gaps/SAVES.sha256 \
        --base ../ic2-conquest/saves --out <new receipt>.json

Checks, each against the saves only (no game is run):
  B7/B8/B9  every changed field between the before and after saves, by record;
  B10       each fleet-turn of the 12 Winter autosaves classified against the storm pass
            (dmg 5: condition -5; dmg 9: d = 82; spike dmg 30: d = 57; d = (10000 div (dmg+100))^2 div 100,
            ships and condition each lose x*d div 300);
  B11       the staging edit, the per-turn relation, war, mobilisation and power values, every relation
            change from turn to turn and the news lines naming Rome.
The receipt holds public file names, decoded scalars and news text; no save bytes.
"""
import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

NAMES = ['Rome', 'Carthage', 'Seleucid', 'Ptolemaic', 'Macedonia', 'Numidia', 'Gaul', 'Greece', 'Celtiberia',
         'Illyria', 'Dacia', 'Bithynia', 'Galatia', 'Armenia', 'Media', 'Thracia']


class Sav:
    def __init__(self, path):
        self.b = b = path.read_bytes()
        self.army = 100958
        self.na = self.h(100956)
        fc = self.army + self.na * 656
        self.nf = self.h(fc)
        self.fleet = fc + 2
        self.nation = self.fleet + self.nf * 26
        self.news = self.nation + 16 * 1172 + 600
        self.term = self.news + 2 + (self.h(self.news) + 1) * 61
        assert len(b) >= self.term + 55, path

    def h(self, o):
        return struct.unpack_from('<h', self.b, o)[0]

    def i(self, o):
        return struct.unpack_from('<i', self.b, o)[0]

    def cal(self):
        return dict(week=self.h(self.term + 40), year=self.h(self.term + 42), season=self.h(self.term + 44))

    def n(self, k, off):
        return self.nation + 1172 * k + off

    def rel(self, a, k):
        return self.h(self.n(a, 0x26 + 2 * k))

    def news_lines(self):
        return [self.b[self.news + 2 + 61 * i:self.news + 63 + 61 * i].split(b'\0')[0].decode('latin1')
                for i in range(self.h(self.news) + 1)]

    def fields(self):
        """{label: value} for every 16-bit field before the news, labelled by record."""
        out = {}
        for o in range(0, 89600, 2):
            out['map(%d,%d)' % divmod(o // 2, 140)] = self.h(o)
        for c in range(334):
            for r in range(0, 34, 2):
                out['city%d+%d' % (c, r)] = self.h(89600 + 34 * c + r)
        for a in range(self.na):
            for r in range(0, 656, 2):
                out['army%d+%d' % (a, r)] = self.h(self.army + 656 * a + r)
        for f in range(self.nf):
            for r in range(0, 26, 2):
                out['fleet%d+%d' % (f, r)] = self.h(self.fleet + 26 * f + r)
        for k in range(16):
            for r in range(0, 1172, 2):
                out['nation%d+0x%x' % (k, r)] = self.h(self.n(k, r))
        return out


def field_diff(a, b):
    fa, fb = a.fields(), b.fields()
    d = {k: [fa.get(k), fb.get(k)] for k in sorted(set(fa) | set(fb)) if fa.get(k) != fb.get(k)}
    # the treasury is a 32-bit word: report it whole
    for k in range(16):
        lo = 'nation%d+0x438' % k
        if lo in d or 'nation%d+0x43a' % k in d:
            d.pop('nation%d+0x43a' % k, None)
            d[lo + ' (int32)'] = [a.i(a.n(k, 0x438)), b.i(b.n(k, 0x438))]
            d.pop(lo, None)
    return d, a.news_lines() == b.news_lines()


def storm_class(s0, c0, s1, c1):
    ds, dc = s0 - s1, c0 - c1
    for name, d in (('dmg9', 82), ('dmg30', 57)):
        if (ds, dc) == (s0 * d // 300, c0 * d // 300):
            return name
    if (ds, dc) == (0, 5):
        return 'dmg5'
    return 'other %d,%d' % (ds, dc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saves', type=Path, required=True)
    ap.add_argument('--sums', type=Path, required=True)
    ap.add_argument('--base', type=Path, required=True, help="ic2-conquest's tracked saves/ directory")
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    S = lambda name: Sav(a.saves / name)
    r = {}

    sums = dict(line.split()[::-1] for line in a.sums.read_text().splitlines() if line.strip())
    bad = [n for n, h in sums.items() if hashlib.sha256((a.saves / n).read_bytes()).hexdigest() != h]
    r['hashes'] = dict(listed=len(sums), mismatched=bad)

    for key, before, after in (('B7_disband', 'MG_B7_before_disband.SAV', 'MG_B7_after_disband.SAV'),
                               ('B8_scuttle', 'MG_B8_before_scuttle.SAV', 'MG_B8_after_scuttle.SAV'),
                               ('B9_buy', 'MG_B9_before_buy.SAV', 'MG_B9_after_buy.SAV')):
        d, same_news = field_diff(S(before), S(after))
        r[key] = dict(changed=d, news_unchanged=same_news)
    s = S('MG_B7_before_disband.SAV')
    r['B7_disband']['army0_before'] = dict(supplies=s.h(s.army + 10), purse=s.h(s.army + 12))
    s = S('MG_B8_before_scuttle.SAV')
    f = s.fleet + 26 * 2
    r['B8_scuttle']['fleet2_before'] = dict(supplies=s.h(f + 14), money=s.h(f + 16), ships=s.h(f + 18),
                                            army=s.h(f + 22))
    s = S('MG_B9b_staged_army1_purse5_supplies0.SAV')
    o = s.army + 656
    r['B9b_staged'] = dict(supplies=s.h(o + 10), purse=s.h(o + 12), note='no after save; result is in run-log only')

    staged = S('MG_B10_staged_6_rome_fleets_at_sea_winter_270.SAV')
    counts, spikes = {}, []
    for seed in ('12345', '1'):
        prev = staged
        for t in range(739, 745):
            cur = S('MG_B10_seed%s_AUTO%04d.SAV' % (seed, t))
            for j in range(6):
                p, c = prev.fleet + 26 * j, cur.fleet + 26 * j
                assert cur.h(c + 8) == 0 and cur.h(c + 10) == -1
                k = storm_class(prev.h(p + 18), prev.h(p + 20), cur.h(c + 18), cur.h(c + 20))
                counts[k] = counts.get(k, 0) + 1
                if k == 'dmg30':
                    spikes.append(dict(seed=seed, turn=t, fleet=j, ships=prev.h(p + 18), condition=prev.h(p + 20),
                                       lost=[prev.h(p + 18) - cur.h(c + 18), prev.h(p + 20) - cur.h(c + 20)]))
            prev = cur
    r['B10_storms'] = dict(start_calendar=staged.cal(), counts=counts, spikes=spikes)

    d, _ = field_diff(Sav(a.base / 'run0-start-AUTO0720-seed12345.SAV'), S('MG_B11_staged_carthage_celtiberia_-18.SAV'))
    turns, changes = [], []
    prev = None
    for t in ['staged'] + ['%04d' % i for i in range(721, 735)]:
        cur = S('MG_B11_staged_carthage_celtiberia_-18.SAV' if t == 'staged' else 'MG_B11_seed12345_AUTO%s.SAV' % t)
        P = lambda k: cur.i(cur.n(k, 0x430)) // 20000 * cur.h(cur.n(k, 0x440)) // 100
        turns.append(dict(turn=t, calendar=cur.cal(), carthage_rome=cur.rel(1, 0), rome_carthage=cur.rel(0, 1),
                          carthage_wars=[NAMES[k] for k in range(16) if cur.rel(1, k) == 3],
                          rome_allies=[NAMES[k] for k in range(16) if cur.rel(0, k) == 2],
                          carthage_mob=cur.h(cur.n(1, 0x442)), P_carthage=P(1), P_rome=P(0),
                          rome_cities=cur.h(cur.n(0, 0x446))))
        if prev is not None:
            ch = [[NAMES[i], NAMES[k], prev.rel(i, k), cur.rel(i, k)] for i in range(16) for k in range(16)
                  if prev.rel(i, k) != cur.rel(i, k) and not (prev.rel(i, k) < 0 and cur.rel(i, k) - prev.rel(i, k) in (1, 2, 3))]
            old, now = prev.news_lines(), cur.news_lines()
            # the log drops its oldest lines as it grows: new lines follow the longest overlap of old's tail
            k = max(k for k in range(min(len(old), len(now)) + 1) if old[len(old) - k:] == now[:k])
            changes.append(dict(turn=t, relation_changes=ch,
                                news_naming_rome=[x for x in now[k:] if 'ROME' in x.upper() and 'WAR' in x.upper()]))
        prev = cur
    r['B11_war'] = dict(staging_edits=d, turns=turns,
                        changes=[c for c in changes if c['relation_changes']])
    with open(a.out, 'x') as fh:
        json.dump(r, fh, indent=1)
        fh.write('\n')
    print(json.dumps(dict(hashes=r['hashes'], storms=counts,
                          b11=[(c['turn'], c['news_naming_rome']) for c in r['B11_war']['changes'] if c['news_naming_rome']])))


if __name__ == '__main__':
    sys.exit(main())
