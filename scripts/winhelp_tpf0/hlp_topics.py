#!/usr/bin/env python3
"""Decode the WinHelp topics (Win95-style PhrIndex/PhrImage phrase compression, LZ77 topic blocks).
Writes a TSV of topics (index, record type, text). Read only on the .hlp."""
import struct, sys, json
from hlp_dir import *

def lz77(src, limit=1<<30):
    out = bytearray(); p = 0
    while p < len(src):
        mask = src[p]; p += 1
        for _ in range(8):
            if p >= len(src): break
            if mask & 1:
                if p+1 >= len(src): p = len(src); break
                w = src[p] | (src[p+1] << 8); p += 2
                ln = ((w >> 12) & 0xF) + 3; pos = (w & 0xFFF) + 1
                for _ in range(ln):
                    out.append(out[-pos] if len(out) >= pos else 0)
            else:
                out.append(src[p]); p += 1
            mask >>= 1
    return bytes(out)

def phrases(d, dr):
    idx = internal(d, dr['|PhrIndex']); img = internal(d, dr['|PhrImage'])
    magic, n, csize, isize, icsize, z = struct.unpack_from('<6I', idx, 0)
    bits = u16(idx, 24)
    nb = bits & 15
    stream = idx[28:]
    pos = [0]; bp = 0
    def getbit():
        nonlocal bp
        v = (stream[bp >> 3] >> (bp & 7)) & 1; bp += 1; return v
    cur = 0
    for i in range(n):
        v = 1
        while getbit(): v += 1 << nb
        for k in range(nb): v += getbit() << k
        cur += v; pos.append(cur)
    # PhrImage: compressed if icsize < isize
    image = lz77(img) if icsize != isize else img
    meta = dict(magic=magic, n=n, csize=csize, isize=isize, icsize=icsize, nb=nb, bits=bits, image_len=len(image), last=pos[-1])
    return [image[pos[i]:pos[i+1]] for i in range(n)], meta

def topic_stream(d, dr):
    sysd = internal(d, dr['|SYSTEM'])
    minor, flags = u16(sysd, 2), u16(sysd, 10)
    t = internal(d, dr['|TOPIC'])
    bs = 0x1000 if not (flags == 8) else 0x800
    if minor <= 16: bs = 0x800
    out = bytearray()
    for b in range(0, len(t), bs):
        blk = t[b+12:b+bs]
        dec = lz77(blk) if minor > 16 and flags in (4, 8) else blk
        out += dec
    return bytes(out), dict(minor=minor, flags=flags, bs=bs)

def expand(b2, ph):
    """Phrase expansion ported from Wine's programs/winhlp32/hlpfile.c HLPFILE_Uncompress3
    (the file carries |PhrIndex/|PhrImage, so the Win95 scheme is the one in force; the
    Win3 |Phrases scheme, HLPFILE_Uncompress2, does not apply). Every byte is one of:
      even                       : phrase byte//2
      odd, byte & 3 == 1         : phrase (byte+1)*64 + next byte   (0x01 -> 128..383, 0x05 -> 384..)
      odd, byte & 7 == 3         : literal run of byte//8 + 1 raw bytes follows
      odd, byte & 7 == 7         : run of byte//16 + 1 bytes: spaces if byte & 0xF == 7, else NULs
    Checked against every record's declared decompressed length (DataLen2): 247/247 exact
    (help_decode_check.txt.v2). The earlier empirical decoder (this function's previous body,
    66/247) mistook even phrase codes below 0x80 for dropped controls and missed the literal
    and space/NUL run cases; see the report's fix note."""
    out = bytearray(); i = 0; n = len(b2)
    while i < n:
        c = b2[i]
        if (c & 1) == 0:
            k = c // 2
            out += ph[k] if k < len(ph) else b'<!%d>' % k; i += 1
        elif (c & 3) == 1:
            k = (c + 1) * 64 + b2[i+1]
            out += ph[k] if k < len(ph) else b'<!%d>' % k; i += 2
        elif (c & 7) == 3:
            ln = c // 8 + 1
            out += b2[i+1:i+1+ln]; i += 1 + ln
        else:  # (c & 7) == 7
            ln = c // 16 + 1
            out += (b' ' if (c & 0xF) == 7 else b'\0') * ln; i += 1
    return bytes(out)

def topics(d):
    dr = directory(d); ph, pm = phrases(d, dr); st, sm = topic_stream(d, dr)
    recs = []; p = 0
    while p + 21 <= len(st):
        bsz, dl2, prv, nxt, dl1 = struct.unpack_from('<5i', st, p); rt = st[p+20]
        if st[p] == 0:
            p += 1; continue   # zero padding at the end of a topic block
        if bsz < 21 or bsz > 0x10000 or dl1 < 21 or dl1 > bsz:
            print('PARSE STOP at', hex(p), 'of', hex(len(st)), file=sys.stderr); break
        l1 = st[p+21:p+dl1]; l2 = st[p+dl1:p+bsz]
        raw_len = len(l2)
        if dl2 > len(l2): l2 = expand(l2, ph)
        recs.append((p, rt, l1, l2, dl2, raw_len)); p += bsz
    return recs, pm, sm

if __name__ == '__main__':
    d = open(sys.argv[1], 'rb').read()
    recs, pm, sm = topics(d)
    print(pm, sm, len(recs), file=sys.stderr)
    for p, rt, l1, l2, dl2, rl in recs:
        print('%06x\t%02x\t%s' % (p, rt, l2.decode('latin-1').replace('\0', '|').replace('\n', '\\n')[:300]))
