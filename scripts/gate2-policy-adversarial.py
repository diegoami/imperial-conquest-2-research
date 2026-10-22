#!/usr/bin/env python3
"""Positive and negative controls for ic2-conquest's gate-2 export-policy checker (research #37).

    python3 -I scripts/gate2-policy-adversarial.py --conquest ../ic2-conquest --saves ../ic2-conquest/saves \
        [--aboard ABOARD.SAV] --work <new scratch dir> --out <new receipt>.json

Upstream's from-scratch mode refuses every real save (they all carry residue), so it has no positive
control on real states. This script:
  1. canonicalises each input save the way the policy says a from-scratch exporter writes it
     (INERT bytes zero, text tails zero, empty unit slots zero, building fleets moves 0 / route x -1)
     and expects the checker to ACCEPT it without a source;
  2. applies one mutation at a time to a canonical save and expects the checker to REFUSE it.
Candidate SAVs are written only under --work (never committed). The receipt holds file names of the
public inputs, mutation names, expected and actual verdicts and the checker's failing rules; no bytes.
"""
import argparse
import hashlib
import json
import struct
import subprocess
import sys
from pathlib import Path

INERT = [(0x450, 0x46A), (0x46D, 0x46D), (0x491, 0x493)]


def i16(b, o):
    return struct.unpack_from("<h", b, o)[0]


def put16(b, o, v):
    struct.pack_into("<h", b, o, v)


def frame(b):
    o = 89600 + 11356
    A = i16(b, o)
    army = o + 2
    o = army + A * 656
    F = i16(b, o)
    fleet = o + 2
    nation = fleet + F * 26
    return dict(A=A, F=F, army=army, fleet=fleet, nation=nation, city=89600)


def zero_tail(b, off, n):
    k = bytes(b[off:off + n]).find(b"\0")
    if k >= 0:
        b[off + k:off + n] = bytes(n - k)


def canonical(src):
    b = bytearray(src)
    f = frame(b)
    for n in range(16):
        r = f["nation"] + 1172 * n
        for lo, hi in INERT:
            b[r + lo:r + hi + 1] = bytes(hi - lo + 1)
        zero_tail(b, r, 11)
        zero_tail(b, r + 0x0B, 27)
    for c in range(334):
        zero_tail(b, f["city"] + 34 * c, 14)
    for k in range(f["A"]):
        for s in range(20):
            so = f["army"] + 656 * k + 16 + 32 * s
            if i16(b, so + 4) > 0:
                zero_tail(b, so + 8, 24)
            else:
                b[so:so + 32] = bytes(32)
    for j in range(f["F"]):
        o = f["fleet"] + 26 * j
        if i16(b, o + 8) >= 0 and i16(b, o + 10) >= 0:
            put16(b, o + 12, 0)
            put16(b, o + 4, -1)
    return b


def mutations(b):
    """(name, mutated bytes) pairs, each expected to be refused."""
    f = frame(b)
    out = []

    def m(name, fn):
        c = bytearray(b)
        if fn(c) is not False:
            out.append((name, c))

    m("inert_byte_nonzero", lambda c: c.__setitem__(f["nation"] + 0x455, 7))
    m("city_name_tail_dirty", lambda c: c.__setitem__(f["city"] + 13, 0x41))

    def unpack(c):
        for k in range(f["A"]):
            so = f["army"] + 656 * k + 16
            if i16(c, so + 4) > 0 and i16(c, so + 32 + 4) > 0:
                c[so:so + 32] = bytes(32)
                return
        return False
    m("slot_unpacked", unpack)

    def neg(c):
        for k in range(f["A"]):
            so = f["army"] + 656 * k + 16
            if i16(c, so + 4) > 0:
                put16(c, so + 4, -5)
                return
        return False
    m("slot_troops_negative", neg)

    def tomb(c):
        if f["A"] < 1:
            return False
        put16(c, f["army"] + 4, -1)
    m("army_tombstone", tomb)

    def fleet_tomb(c):
        if f["F"] < 1:
            return False
        put16(c, f["fleet"] + 8, -1)
    m("fleet_tombstone", fleet_tomb)

    def building_moves(c):
        for j in range(f["F"]):
            o = f["fleet"] + 26 * j
            if i16(c, o + 8) >= 0 and i16(c, o + 10) >= 0:
                put16(c, o + 12, 5)
                return
        return False
    m("building_fleet_moves_5", building_moves)

    def list_order(c):
        for n in range(16):
            lo = f["nation"] + 1172 * n + 0x48
            if i16(c, lo) >= 0 and i16(c, lo + 2) >= 0:
                a, z = c[lo:lo + 2], c[lo + 2:lo + 4]
                c[lo:lo + 2], c[lo + 2:lo + 4] = z, a
                return
        return False
    m("city_list_order_swapped", list_order)

    def live_count(c):
        for n in range(16):
            r = f["nation"] + 1172 * n
            if i16(c, r + 0x440) > 0:
                put16(c, r + 0x446, i16(c, r + 0x446) + 1)
                return
        return False
    m("live_nation_count_wrong", live_count)

    def city_marker(c):
        x, y = i16(c, f["city"] + 14), i16(c, f["city"] + 16)
        put16(c, (x * 140 + y) * 2, i16(c, (x * 140 + y) * 2) + 1)
    m("city_marker_wrong_owner", city_marker)

    m("city_allegiance_missing", lambda c: put16(c, f["city"] + 0x14, -1))
    m("city_allegiance_out_of_range", lambda c: put16(c, f["city"] + 0x14, 99))
    return out


def run_checker(conquest, cand, out):
    p = subprocess.run([sys.executable, "-I", str(conquest / "scripts/sav_export_policy_check.py"), str(cand),
                        "--out", str(out)], capture_output=True, text=True)
    d = json.loads(out.read_text())
    failed = sorted(set(d["invariant_failures"]) | {r["rule"] for r in d["rules"] if not r["ok"] and r["required"]})
    return d["accepted"], failed, p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conquest", type=Path, required=True)
    ap.add_argument("--saves", type=Path, required=True)
    ap.add_argument("--aboard", type=Path, help="a save with an army aboard, for the carrier mutation")
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=False)
    checker = a.conquest / "scripts/sav_export_policy_check.py"
    rows = []
    inputs = sorted(p for p in a.saves.iterdir() if p.suffix.lower() == ".sav")
    if a.aboard:
        inputs.append(a.aboard)
    for p in inputs:
        can = canonical(p.read_bytes())
        cp = a.work / (p.stem + ".canonical.SAV")
        cp.write_bytes(can)
        ok, failed, _ = run_checker(a.conquest, cp, a.work / (p.stem + ".canonical.json"))
        rows.append(dict(input=p.name, case="canonical", expect="accept", accepted=ok, failed=failed,
                         as_expected=ok))
        muts = mutations(can)
        if a.aboard and p == a.aboard:
            f = frame(can)
            for j in range(f["F"]):
                o = f["fleet"] + 26 * j
                if i16(can, o + 8) >= 0 and i16(can, o + 22) >= 0:
                    c = bytearray(can)
                    ao = f["army"] + 656 * i16(c, o + 22)
                    put16(c, ao, i16(c, ao) + 1)
                    muts.append(("carried_army_off_fleet_tile", c))
                    break
        for name, c in muts:
            mp = a.work / f"{p.stem}.{name}.SAV"
            mp.write_bytes(c)
            ok, failed, _ = run_checker(a.conquest, mp, a.work / f"{p.stem}.{name}.json")
            rows.append(dict(input=p.name, case=name, expect="refuse", accepted=ok, failed=failed,
                             as_expected=not ok))
    summary = dict(
        checker_sha256=hashlib.sha256(checker.read_bytes()).hexdigest(),
        method="canonical from-scratch rewrite of each input must be accepted; each single mutation of a "
               "canonical save must be refused",
        canonical=dict(n=sum(r["case"] == "canonical" for r in rows),
                       accepted=sum(r["case"] == "canonical" and r["accepted"] for r in rows)),
        mutations={},
        unexpected=[r for r in rows if not r["as_expected"]],
        rows=rows)
    for r in rows:
        if r["case"] != "canonical":
            s = summary["mutations"].setdefault(r["case"], dict(n=0, refused=0))
            s["n"] += 1
            s["refused"] += not r["accepted"]
    with open(a.out, "x") as fh:
        json.dump(summary, fh, indent=1)
        fh.write("\n")
    print(json.dumps(dict(canonical=summary["canonical"], mutations=summary["mutations"],
                          unexpected=len(summary["unexpected"]))))


if __name__ == "__main__":
    sys.exit(main())
