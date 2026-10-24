#!/usr/bin/env python3
"""Research #63: bounded original-x86 controls on synthetic memory only.

Requires Unicorn 2.1.4. Arguments: --exe EXE --dat DAT --dump all_app_functions.txt
--out NEW.json. Never loads/writes a SAV or launches a Windows process. Output is
scalar evidence; original assets and instructions are never copied into it.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

import unicorn
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import (
    UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDX,
    UC_X86_REG_ESP, UC_X86_REG_EIP,
)

PINS = {
    "exe": "9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31",
    "dat": "94d0ccfc67148d727de4c4e60aefc3c53ba9e67775bd689f0fcb2e23c12e5fbd",
    "dump": "2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8",
}
ARMY, RECRUIT, BATTLE = 0x47C1EC, 0x474954, 0x4A0344
FORM, LIST, ITEMS, VMT = 0x600000, 0x601000, 0x602000, 0x603000
STOP, FAKE_READ, FAKE_WRITE, FAKE_CLOSE, FAKE_COUNT = range(0x610000, 0x610050, 0x10)
STACK = 0x70FF00


def require(ok, detail):
    if not ok:
        raise RuntimeError(detail)


class Machine:
    def __init__(self, exe):
        self.u = Uc(UC_ARCH_X86, UC_MODE_32)
        self.u.mem_map(0, 0x1000)  # synthetic FS:[0] exception-chain head
        self.u.mem_map(0x400000, 0x164000)
        self.u.mem_map(0x600000, 0x20000)
        self.u.mem_map(0x700000, 0x10000)
        pe = struct.unpack_from("<I", exe, 0x3C)[0]
        n, opt = struct.unpack_from("<H", exe, pe + 6)[0], struct.unpack_from("<H", exe, pe + 20)[0]
        require(exe[pe:pe+4] == b"PE\0\0", "not PE")
        require(struct.unpack_from("<I", exe, pe + 52)[0] == 0x400000, "image base")
        for i in range(n):
            off = pe + 24 + opt + i * 40
            _, va, size, raw = struct.unpack_from("<4I", exe, off + 8)
            self.u.mem_write(0x400000 + va, exe[raw:raw + size])
        self.hooks, self.visits = {}, {}
        self.u.hook_add(UC_HOOK_CODE, self.on_code)
        self.w32(FORM, VMT)
        self.w32(VMT - 4, FAKE_CLOSE)
        self.w32(VMT, FAKE_READ)
        self.w32(VMT + 4, FAKE_WRITE)
        self.w32(0x4A0BD0, FORM)

    def r(self, reg):
        return self.u.reg_read(reg)

    def ret(self, value=None, pop=0):
        sp = self.r(UC_X86_REG_ESP)
        dest = self.u32(sp)
        if value is not None:
            self.u.reg_write(UC_X86_REG_EAX, value & 0xFFFFFFFF)
        self.u.reg_write(UC_X86_REG_ESP, sp + 4 + pop)
        self.u.reg_write(UC_X86_REG_EIP, dest)

    def on_code(self, _, addr, size, data):
        self.visits[addr] = self.visits.get(addr, 0) + 1
        if addr == self.end:
            self.done = True
            self.u.emu_stop()
        elif addr in self.hooks:
            self.hooks[addr]()
        else:
            require(0x401000 <= addr < 0x45D000, f"unexpected execution {addr:x}")

    def run(self, start, eax=0, edx=0, ecx=0, end=STOP):
        self.done, self.end = False, end
        self.w32(STACK, STOP)
        for reg, val in [(UC_X86_REG_ESP, STACK), (UC_X86_REG_EAX, eax),
                         (UC_X86_REG_EDX, edx), (UC_X86_REG_ECX, ecx)]:
            self.u.reg_write(reg, val)
        self.u.emu_start(start, 0xFFFFFFFF, count=200000)
        require(self.done, f"instruction bound reached from {start:x}")
        if end == STOP:
            require(self.r(UC_X86_REG_ESP) == STACK + 4, "unbalanced stack")

    def w16(self, addr, val):
        self.u.mem_write(addr, struct.pack("<H", val & 0xFFFF))

    def w32(self, addr, val):
        self.u.mem_write(addr, struct.pack("<I", val))

    def i16(self, addr):
        return struct.unpack("<h", self.u.mem_read(addr, 2))[0]

    def u32(self, addr):
        return struct.unpack("<I", self.u.mem_read(addr, 4))[0]

    def copy_string(self):
        dst, src = self.r(UC_X86_REG_EAX), self.r(UC_X86_REG_EDX)
        n = 0
        while self.u.mem_read(src + n, 1) != b"\0":
            n += 1
            require(n < 255, "string bound")
        self.u.mem_write(dst, bytes(self.u.mem_read(src, n + 1)))
        self.ret(dst)


def mobilisation(exe):
    rows = []
    for state in [-1, 0, 15, 16, 17, 18, 19, 20, 23, 24]:
        m = Machine(exe)
        # One selected recruitment row, one same-nation adjacent receiving army.
        m.w32(FORM + 0x220, LIST)
        m.w32(LIST + 0xFC, ITEMS)
        m.w32(ITEMS, VMT)
        m.w32(VMT + 0x10, FAKE_COUNT)
        for a in [FAKE_COUNT, 0x429EB8, 0x429FB4]:
            m.hooks[a] = lambda: m.ret(1)
        for a in [0x45495C, 0x45BA6C, 0x44A218]:
            m.hooks[a] = lambda: m.ret()  # list refresh, paint, unit naming
        m.w16(0x4A0324, 1)
        m.u.mem_write(0x474B00, b"\1")  # human nation
        m.w16(ARMY, 20)
        m.w16(ARMY + 2, 20)
        m.w16(ARMY + 8, 2)
        m.w16(0x47959E, 21)
        m.w16(0x4795A0, 20)
        for addr, val in [(RECRUIT, state), (RECRUIT + 2, 2), (RECRUIT + 4, 3500)]:
            m.w16(addr, val)
        m.run(0x4552A8, eax=FORM)
        entered = m.visits.get(0x44A4E0, 0)
        expected = state >= 16
        require(entered == int(expected), f"readiness gate {state}")
        if expected:
            require([m.i16(ARMY + 16 + j * 2) for j in range(4)] ==
                    [0, 2, 3500, state // 4], f"mobilise {state}")
            require(m.i16(RECRUIT + 4) == 0, "queue not removed")
        else:
            require(m.i16(ARMY + 20) == 0 and m.i16(RECRUIT + 4) == 3500, "blocked mutation")
        rows.append(dict(readiness=state, mobilised=bool(entered),
                         quality=m.i16(ARMY + 22) if entered else None))
    return rows


def stream_machine(exe, source=None):
    m, data, calls = Machine(exe), bytearray(), []
    cursor = 0

    def transfer(read):
        nonlocal cursor
        addr, size = m.r(UC_X86_REG_EDX), m.r(UC_X86_REG_ECX)
        require(size <= 89600, "unexpected stream size")
        if read:
            require(source is not None and cursor + size <= len(source), "short stream")
            m.u.mem_write(addr, source[cursor:cursor + size])
        else:
            data.extend(m.u.mem_read(addr, size))
        calls.append((addr, size))
        cursor += size
        m.ret(size)

    m.hooks[FAKE_READ] = lambda: transfer(True)
    m.hooks[FAKE_WRITE] = lambda: transfer(False)
    m.hooks[FAKE_CLOSE] = lambda: m.ret()
    m.hooks[0x40A75C] = lambda: m.ret(FORM, pop=4)  # file ctor, mode argument
    m.hooks[0x403458] = lambda: m.ret()  # filename string conversion
    m.hooks[0x4032FC] = lambda: m.ret()  # string release
    for a in [0x4127A0, 0x4127C0, 0x420C58, 0x420C84, 0x412880, 0x4128C4]:
        m.hooks[a] = lambda: m.ret(0)  # form geometry
    return m, data, calls


def serialisation(exe):
    rows = []
    qualities = [-1, 0, 3, 4, 5, 6, 9, 10, 32767]
    for battle in [0, 1]:
        m, data, writes = stream_machine(exe)
        m.w16(0x4A0324, 2)
        m.w16(0x4A0326, 1)
        m.w16(0x4A031E, -1)
        m.u.mem_write(0x4A0B7C, bytes([battle]))
        for army in range(2):
            # Distinct synthetic bytes, including empty-slot and tombstone residue.
            m.u.mem_write(ARMY + army * 656, bytes((j * 17 + army) % 256 for j in range(656)))
            m.w16(ARMY + army * 656 + 4, 0 if army == 0 else -1)
            for slot, q in enumerate(qualities):
                m.w16(ARMY + army * 656 + 16 + slot * 32 + 6, q)
        records = bytes(m.u.mem_read(ARMY, 1312))
        m.run(0x4484D0)
        expected_len = 100956 + 2 + 1312 + 2 + 26 + 18752 + 600 + 2 + 55 + battle * 2105
        require(len(data) == expected_len, "serialized framing")
        require(data[100958:102270] == records, "save changed army bytes")
        loader, _, reads = stream_machine(exe, bytes(data))
        loader.run(0x4487C4)
        require(reads == writes, "load/save transfer regions differ")
        require(bytes(loader.u.mem_read(ARMY, 1312)) == records, "load changed army bytes")
        require(loader.visits.get(FAKE_CLOSE) == 1, "file close")
        # Read loaded memory through a second execution of the original writer.
        reread = bytearray()

        def write_again():
            reread.extend(loader.u.mem_read(loader.r(UC_X86_REG_EDX), loader.r(UC_X86_REG_ECX)))
            loader.ret()

        loader.hooks[FAKE_WRITE] = write_again
        loader.run(0x4484D0)
        require(reread == data, "save/load/save differs")
        rows.append(dict(battle=bool(battle), bytes=len(data), transfer_calls=len(writes),
                         army_bytes_identical=True, stream_round_trip_identical=True,
                         raw_quality_controls=qualities,
                         note="Out-of-domain controls demonstrate raw copying, not gameplay validity."))
    return rows


def initialisation(exe, dat):
    m, _, reads = stream_machine(exe, dat)
    m.run(0x4481A0)
    require(m.i16(0x4A0324) == 15, "DAT army count")
    require(bytes(m.u.mem_read(ARMY, 15 * 656)) == dat[100956:100956 + 15 * 656],
            "DAT army copy")
    require(bytes(m.u.mem_read(0x47938C, 110)) == dat[0x1F6CA:0x1F6CA + 110], "DAT table load")
    require(sum(n for _, n in reads) == len(dat), "DAT framing")
    # A new army clears type/troops, but not every quality/residue word.
    c = Machine(exe)
    c.u.mem_write(ARMY, bytes([0x55]) * 656)
    c.w16(0x4A0324, 0)
    c.u.mem_write(0x474B00, b"\1")
    # Placement is explicit synthetic input; execute the complete constructor.
    def place():
        c.w16(c.r(UC_X86_REG_EAX), 20)
        c.w16(c.r(UC_X86_REG_EAX) + 2, 20)
        c.ret()
    c.hooks[0x4492C0] = place
    c.run(0x449F08, eax=0, edx=0, ecx=LIST)
    require(c.i16(LIST) == 0, "constructor result")
    require(all(c.i16(ARMY + 18 + i * 32) == 0 and c.i16(ARMY + 20 + i * 32) == 0
                and c.i16(ARMY + 22 + i * 32) == 0x5555 for i in range(20)), "empty-slot residue")
    return dict(dat_army_records=15, dat_army_bytes_identical=True,
                dat_quality_table_identical=True, dat_bytes_read=sum(n for _, n in reads),
                constructor_empty_slots=20, constructor_quality_residue_preserved=True)


def display(exe, dat):
    rows = []
    for q in [4, 5, 9]:
        m, table_reads = Machine(exe), []
        m.u.mem_write(0x47938C, dat[0x1F6CA:0x1F6CA + 110])
        m.w16(0x4A0324, 1)
        m.w16(ARMY, 20)
        m.w16(ARMY + 2, 20)
        m.w16(ARMY + 20, 3500)
        m.w16(ARMY + 22, q)
        m.hooks[0x405B00] = m.copy_string
        def append():
            src = m.r(UC_X86_REG_EDX)
            if 0x47938C <= src < 0x47938C + 110:
                table_reads.append((src - 0x47938C) // 11)
            m.ret()
        m.hooks[0x405BC8] = append
        m.hooks[0x448F18] = lambda: m.ret()  # number formatting
        m.hooks[0x43B9F4] = lambda: m.ret()  # panel painting
        m.run(0x43CDD8, eax=FORM, edx=20 | (20 << 16))
        require(table_reads == [q], "display index remapped")
        require(m.i16(ARMY + 22) == q, "display changed quality")
        word = dat[0x1F6CA + q * 11:0x1F6CA + (q + 1) * 11].split(b"\0")[0].decode("ascii")
        rows.append(dict(quality=q, selected_table_index=table_reads[0], word=word))
    return rows


def combat(exe):
    m, bounds = Machine(exe), []
    m.hooks[0x405B00] = m.copy_string
    m.hooks[0x439968] = lambda: m.ret()  # post-copy battle-turn/UI setup
    m.w16(0x4A0B74, 0)
    m.w16(0x4A0B76, 1)
    for army in range(2):
        m.w16(ARMY + army * 656 + 4, army)
        m.w16(ARMY + army * 656 + 14, 65)
        m.u.mem_write(0x474B00 + army * 1172, b"\1")  # skip AI sort/+3
        for slot, q in enumerate([4, 5, 9]):
            p = ARMY + army * 656 + 16 + slot * 32
            m.w16(p + 4, 3500)
            m.w16(p + 6, q)
    m.w16(0x478FCA, 15000)  # type-0 capacity for real grid-icon helper
    # Record bounds without replacing the original RNG.
    def record_rng(_, addr, size, data):
        if addr == 0x40284C:
            bounds.append(m.r(UC_X86_REG_EAX))
    m.u.hook_add(UC_HOOK_CODE, record_rng)
    m.run(0x437DE4)
    copied = [m.i16(BATTLE + side * 880 + slot * 44 + 10)
              for side in range(2) for slot in range(3)]
    require(copied == [4, 5, 9] * 2 and bounds == [16, 20, 36] * 2, "battle copy/RNG")
    rows = []
    for result in [0, 1]:
        p = Machine(exe)
        p.hooks[0x405B00] = p.copy_string
        rng_bounds = []
        def forced_rng():
            rng_bounds.append(p.r(UC_X86_REG_EAX))
            p.ret(result)
        p.hooks[0x40284C] = forced_rng
        for slot, q in enumerate([4, 5, 6, 8, 9]):
            p.w16(BATTLE + slot * 44 + 8, 3500)
            p.w16(BATTLE + slot * 44 + 10, q)
        # Original winner-copy/promotion prefix only; stop before loot/UI/diplomacy.
        p.run(0x459220, end=0x4592ED)
        got = [p.i16(ARMY + 22 + slot * 32) for slot in range(5)]
        expected = [7, 7, 7, 9, 9] if result == 0 else [6, 6, 6, 8, 9]
        require(got == expected and rng_bounds == [4] * 5, "winner promotion")
        rows.append(dict(forced_random4=result, inputs=[4, 5, 6, 8, 9], outputs=got))
    return dict(copy_in_quality=copied, original_rng_bounds=bounds, winner_prefix=rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ["exe", "dat", "dump", "out"]:
        ap.add_argument("--" + name, type=Path, required=True)
    a = ap.parse_args()
    inputs = {name: getattr(a, name).read_bytes() for name in PINS}
    for name, expected in PINS.items():
        require(hashlib.sha256(inputs[name]).hexdigest() == expected, f"{name} pin mismatch")
    require(unicorn.__version__ == "2.1.4", "requires Unicorn 2.1.4")
    names = [inputs["dat"][0x1F6CA + i * 11:0x1F6CA + (i + 1) * 11]
             .split(b"\0")[0].decode("ascii") for i in range(10)]
    require(names == ["not ready"] * 4 + ["very poor", "poor", "average", "good", "very good", "elite"],
            "quality table")
    receipt = dict(scope="synthetic original-x86 controls; no native Windows/game execution",
                   pins=PINS, unicorn=unicorn.__version__, quality_names=names,
                   checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   initialisation=initialisation(inputs["exe"], inputs["dat"]),
                   display=display(inputs["exe"], inputs["dat"]),
                   mobilisation=mobilisation(inputs["exe"]),
                   serialisation=serialisation(inputs["exe"]), combat=combat(inputs["exe"]))
    with a.out.open("x") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")
    print("PASS: DAT load, constructor, 3 display indices, 10 readiness controls, "
          "2 raw serialization round trips, battle copy-in, 2 promotion branches")


if __name__ == "__main__":
    main()
