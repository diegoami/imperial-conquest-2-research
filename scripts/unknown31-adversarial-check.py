#!/usr/bin/env python3
"""Adversarial cross-check of the INERT claim for the 31 UNKNOWN nation bytes (research #47).

    python3 -I scripts/unknown31-adversarial-check.py --exe "$ORIG/Imperial Conquest 2.exe" --out <new>.json

Needs capstone 5 and pefile. Linear sweep of every executable section (a superset of the
recursive traversal: it may decode data as code, which can only add candidates). Reports:

  overlap   a memory operand (not lea) whose accessed byte range, taken as a nation-record
            offset, overlaps UNKNOWN31; the start may lie outside it (wide/overlapping access).
            Absolute or indexed operands use (disp - base) mod 0x494; a base-register operand
            with a small displacement is taken as an offset from a record start.
  anchor    lea or immediate forming a nation address that lies in UNKNOWN31.
  reach     a register given any nation address (lea/mov imm) and dereferenced within the next
            48 instructions, before redefinition, at a displacement whose bytes overlap UNKNOWN31.
  bulk      rep movs/stos, and immediates 0x494/0x4940 or 0x125/0x24A counts (record-sized moves).

It has no proof value when clean beyond these rules; every listed candidate is to be read by hand.
The output holds addresses, offsets and classes only, never instruction bytes or text.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

BASE, STRIDE, NREC = 0x474670, 0x494, 16
LO, HI = BASE - STRIDE, BASE + STRIDE * NREC
UNKNOWN = set(range(0x450, 0x46B)) | {0x46D} | set(range(0x491, 0x494))
BULK_IMM = {0x494, 0x4940, 0x125, 0x24A}
WINDOW = 48
OVER_WINDOW = 400
APP_LO, APP_HI = 0x436000, 0x45C3D4   # application code (atlas APP_LO) to the end of CODE


def overlap(off, size):
    return sorted({(off + k) % STRIDE for k in range(max(size, 1))} & UNKNOWN)


def sweep(exe):
    import capstone
    import pefile
    from capstone import x86
    pe = pefile.PE(exe)
    ib = pe.OPTIONAL_HEADER.ImageBase
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    cs.detail = True
    for s in pe.sections:
        if not s.Characteristics & 0x20000000:          # IMAGE_SCN_MEM_EXECUTE
            continue
        data, va = s.get_data(), ib + s.VirtualAddress
        off = 0
        while off < len(data):
            n = 0
            for ins in cs.disasm(data[off:], va + off):
                n += 1
                yield ins, x86
                off = ins.address - va + ins.size
            if n == 0:
                off += 1                                   # skip an undecodable byte


def overapprox(exe):
    """Over-approximation in the application code: every nation-address seed (lea/mov imm) is
    followed for OVER_WINDOW instructions with register redefinitions ignored, up to a ret; and
    each rep movs/stos lists the nation-address operands of its 12 preceding instructions."""
    from capstone import x86 as X
    ins = [i for i, _ in sweep(exe) if APP_LO <= i.address < APP_HI]
    reach, bulk = [], []

    def nation_value(i, op):
        if op.type == X.X86_OP_IMM:
            return op.imm & 0xFFFFFFFF
        if op.type == X.X86_OP_MEM:
            return op.mem.disp & 0xFFFFFFFF
        return None

    for k, i in enumerate(ins):
        if i.mnemonic in ("lea", "mov") and len(i.operands) == 2 and i.operands[0].type == X.X86_OP_REG:
            src = i.operands[1]
            if (i.mnemonic == "lea") != (src.type == X.X86_OP_MEM):
                continue
            v = nation_value(i, src)
            if v is None or not LO <= v < HI:
                continue
            ao, reg = (v - BASE) % STRIDE, i.reg_name(i.operands[0].reg)
            for j in ins[k + 1:k + 1 + OVER_WINDOW]:
                if j.mnemonic == "ret":
                    break
                for op in j.operands:
                    m = op.mem if op.type == X.X86_OP_MEM else None
                    if m and m.base and not m.index and j.reg_name(m.base) == reg and abs(m.disp) < STRIDE:
                        hit = overlap(ao + m.disp, 1 if j.mnemonic == "lea" else op.size)
                        if hit:
                            reach.append({"pc": hex(j.address), "anchor_pc": hex(i.address),
                                          "anchor": hex(ao), "disp": m.disp, "bytes": [hex(h) for h in hit]})
        if i.mnemonic.startswith("rep") and ("movs" in i.mnemonic or "stos" in i.mnemonic):
            near = [hex(p.address) for p in ins[max(0, k - 12):k] for op in p.operands
                    if (v := nation_value(p, op)) is not None and LO <= v < HI]
            bulk.append({"pc": hex(i.address), "nation_operands_before": near})
    return reach, bulk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    exe_sha = hashlib.sha256(Path(a.exe).read_bytes()).hexdigest()
    res = {"overlap": [], "anchor": [], "reach": [], "bulk": []}
    recent = []                                            # (index, reg, nation offset, pc)
    count = 0
    for i, (ins, X) in enumerate(sweep(a.exe)):
        count += 1
        pc = hex(ins.address)
        regs_w = set()
        try:
            _, w = ins.regs_access()
            regs_w = {ins.reg_name(r) for r in w}
        except Exception:
            pass
        for op in ins.operands:
            if op.type == X.X86_OP_MEM:
                m = op.mem
                d = m.disp & 0xFFFFFFFF
                base = ins.reg_name(m.base) if m.base else None
                index = ins.reg_name(m.index) if m.index else None
                if LO <= d < HI:
                    o = (d - BASE) % STRIDE
                    form = "absolute" if not (base or index) else "indexed"
                elif base and 0 <= d < STRIDE:
                    o, form = d, "relative"
                else:
                    o = None
                if o is not None:
                    if ins.mnemonic == "lea":
                        if o in UNKNOWN and form != "relative":
                            res["anchor"].append({"pc": pc, "kind": "lea", "offset": hex(o)})
                    else:
                        hit = overlap(o, op.size)
                        if hit:
                            res["overlap"].append({"pc": pc, "form": form, "start": hex(o),
                                                   "size": op.size, "bytes": [hex(h) for h in hit],
                                                   "starts_inside": o in UNKNOWN})
                # dereference of a recently anchored register
                if ins.mnemonic != "lea" and base and not index and abs(m.disp) < STRIDE:
                    for (j, reg, ao, apc) in recent:
                        if reg == base and i - j <= WINDOW:
                            hit = overlap(ao + m.disp, op.size)
                            if hit:
                                res["reach"].append({"pc": pc, "anchor_pc": apc, "anchor": hex(ao),
                                                     "disp": m.disp, "size": op.size,
                                                     "bytes": [hex(h) for h in hit]})
            elif op.type == X.X86_OP_IMM:
                v = op.imm & 0xFFFFFFFF
                if LO <= v < HI and (v - BASE) % STRIDE in UNKNOWN:
                    res["anchor"].append({"pc": pc, "kind": "imm", "offset": hex((v - BASE) % STRIDE)})
                if v in BULK_IMM:
                    res["bulk"].append({"pc": pc, "kind": "imm", "value": hex(v)})
        if ins.mnemonic.startswith("rep") and ("movs" in ins.mnemonic or "stos" in ins.mnemonic):
            res["bulk"].append({"pc": pc, "kind": ins.mnemonic.split()[0] + "-string"})
        # anchors: a register given a nation address, by lea or mov imm
        recent = [r for r in recent if r[1] not in regs_w and i - r[0] <= WINDOW]
        if ins.mnemonic in ("lea", "mov") and len(ins.operands) == 2 and ins.operands[0].type == X.X86_OP_REG:
            src = ins.operands[1]
            v = None
            if ins.mnemonic == "lea" and src.type == X.X86_OP_MEM:
                v = src.mem.disp & 0xFFFFFFFF
            elif ins.mnemonic == "mov" and src.type == X.X86_OP_IMM:
                v = src.imm & 0xFFFFFFFF
            if v is not None and LO <= v < HI:
                recent.append((i, ins.reg_name(ins.operands[0].reg), (v - BASE) % STRIDE, pc))
        if ins.mnemonic in ("ret", "jmp") or ins.mnemonic.startswith("call"):
            recent = [r for r in recent if ins.mnemonic.startswith("call") and r[1] in ("ebx", "esi", "edi", "ebp")]
    res["reach_overapprox"], res["bulk_near_nation"] = overapprox(a.exe)
    summary = {"exe_sha256": exe_sha, "decoded_linear": count, "window": WINDOW,
               "overapprox_window": OVER_WINDOW, "app_range": [hex(APP_LO), hex(APP_HI)],
               "method": "linear sweep of executable sections; candidates for manual reading, not proof",
               "counts": {k: len(v) for k, v in res.items()}, **res}
    with open(out, "x") as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps(summary["counts"]))


if __name__ == "__main__":
    sys.exit(main())
