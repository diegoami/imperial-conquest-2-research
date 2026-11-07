#!/usr/bin/env python3
"""Check pinned original asset metadata; emit scalar JSON, never pixels/audio.

Usage: original-assets218-check.py EXE DUMP CONQUEST_SOURCE REMAKE_SOURCE
The last two directories must contain the pinned sources described in the report.
This reuses the existing TPF0 parser as an intake check, not a general PE extractor.
"""
import collections
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "winhelp_tpf0"))
import extract_forms as forms

EXE_SHA = "9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31"
DUMP_SHA = "2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8"
NATIONS = "Rome Carthage Seleucid Ptolemaic Macedonia Numidia Gaul Greece Celtiberia Illyria Dacia Bithynia Galatia Armenia Media Thracia".split()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bitmap(data):
    require(len(data) >= 54 and data[:2] == b"BM", "invalid BMP header")
    length, = struct.unpack_from("<I", data, 2)
    offset, dib = struct.unpack_from("<II", data, 10)
    width, height, planes, bpp, compression = struct.unpack_from("<iiHHI", data, 18)
    require(dib == 40 and planes == 1 and compression == 0, "unsupported BMP encoding")
    require(width > 0 and height != 0 and bpp in (1, 4, 8), "unsupported BMP dimensions/depth")
    colors, = struct.unpack_from("<I", data, 46)
    colors = colors or (1 << bpp)
    stride = ((width * bpp + 31) // 32) * 4
    require(colors <= (1 << bpp) and 54 + colors * 4 <= offset, "invalid BMP palette")
    require(offset + stride * abs(height) <= length <= len(data), "truncated BMP pixels")
    return {"width": width, "height": abs(height), "bpp": bpp,
            "orientation": "bottom-up" if height > 0 else "top-down"}


def inspect(exe, dump, conquest, remake):
    data = exe.read_bytes()
    require(hashlib.sha256(data).hexdigest() == EXE_SHA, "unsupported EXE profile")
    dump_bytes = dump.read_bytes()
    require(hashlib.sha256(dump_bytes).hexdigest() == DUMP_SHA, "unsupported decompilation")
    previous_value = forms.value

    def binary_value(reader):
        if reader.d[reader.p] == 10:
            reader.p += 1
            size = reader.i(4, "<I")
            require(reader.p + size <= len(reader.d), "truncated TPF0 binary property")
            value = bytes(reader.d[reader.p:reader.p + size])
            reader.p += size
            return {"bytes": value}
        return previous_value(reader)

    forms.value = binary_value
    lists = []
    glyphs = {}
    parsed = 0
    candidates = 0

    def walk(node, form):
        props = node["props"]
        if node["class"] == "TImageList" and "Bitmap" in props:
            blob = props["Bitmap"]["bytes"]
            length, count = struct.unpack_from("<II", blob)
            color = bitmap(blob[8:8 + length])
            mask_offset = blob.find(b"BM", 8 + length)
            require(mask_offset >= 0, "missing image-list mask")
            mask = bitmap(blob[mask_offset:])
            width, height = props.get("Width", 32), props.get("Height", 32)
            require(width > 0 and height > 0 and color["width"] % width == 0
                    and color["height"] % height == 0, "invalid cell geometry")
            require(0 < count <= (color["width"] // width) * (color["height"] // height),
                    "image count exceeds sheet capacity")
            require(mask["bpp"] == 1 and mask["width"] == color["width"]
                    and mask["height"] == color["height"], "incompatible mask geometry")
            lists.append({"list": form + "_" + node["name"], "count": count,
                          "cell": [width, height], "color": color, "mask": mask})
        if form == "TPremierForm" and node["name"] in {"sb_" + n for n in NATIONS}:
            blob = props["Glyph.Data"]["bytes"]
            length, = struct.unpack_from("<I", blob)
            glyph = bitmap(blob[4:4 + length])
            require(props.get("NumGlyphs") == 2 and glyph["width"] == 40
                    and glyph["height"] == 20 and glyph["bpp"] == 4, "unexpected nation glyph")
            glyphs[node["name"]] = {"name": node["name"], "frames": 2, **glyph}
        for child in node["children"]:
            walk(child, form)

    try:
        for match in re.finditer(rb"TPF0", data):
            pos = match.start()
            if not data[pos + 4] or data[pos + 5:pos + 6] != b"T":
                continue
            candidates += 1
            node = forms.obj(forms.P(data, pos + 4))
            parsed += 1
            walk(node, node["class"])
    finally:
        forms.value = previous_value
    retained = conquest / "runs/experiments/data/run-exp-unit-icon-resources"
    old = json.loads((retained / "imagelists_decoded.json").read_text())
    require(len(lists) == len(old) == 11, "image-list count mismatch")
    by_name = {row["list"]: row for row in lists}
    require(len(by_name) == 11, "duplicate image-list names")
    for row in old:
        actual = by_name[row["list"]]
        require(actual["count"] == row["count"] and row["mask"] is True,
                "retained image-list count/mask mismatch")
        require([actual["color"][k] for k in ("width", "height", "bpp")]
                == [row["bmp"][0], abs(row["bmp"][1]), row["bmp"][2]],
                "retained image-list geometry mismatch")
    require(len(glyphs) == 16, "nation glyph count mismatch")
    calls = collections.Counter(map(int, re.findall(
        r"TPremierForm_MakeSound\([^;\n]*,\s*(\d+)\);", dump_bytes.decode())))
    require(dict(calls) == {1: 4, 2: 1, 3: 1, 4: 1, 5: 2, 6: 1, 7: 1, 8: 3, 9: 1, 10: 1},
            "sound-call inventory mismatch")
    core_source = (remake / "src/IC2.Engine/Assets/AssetKeys.cs").read_text()
    constants = dict(re.findall(r'public const string (\w+) = "([^"]+)";', core_source))
    core = [constants[name] for name in re.findall(r"yield return (\w+);", core_source)]
    require(len(core) == len(set(core)) == 75, "core asset-key inventory changed")
    battle_source = (remake / "godot/Assets/BattleAssetKeys.cs").read_text()
    def strings(name):
        body = re.search(name + r"\s*=\s*new\[\]\s*\{([^}]+)\}", battle_source).group(1)
        return re.findall(r'"([^"]+)"', body)
    battle = [f"battle.unit.{t}.{s}" for t in strings("UnitTypes") for s in strings("Sizes")]
    battle += ["battle.ground", "battle.cursor"]
    battle += ["battle.toolbar." + s for s in strings("ToolbarButtons")]
    require(len(battle) == 25 and len(set(core + battle)) == 100, "battle key inventory changed")
    return {"conquest_tool_baseline": "f71c70ffa9ccf8f7cfbb5335fb28c4c44d341ed6",
            "upstream_handback_head": "36e4ad89ea57ea2f154652ddad84bd39fe6d1b11",
            "remake_revision": "55bd7fcef91e41b179a6df9851384bb687932e8e",
            "profile_exe_sha256": EXE_SHA, "dump_sha256": DUMP_SHA,
            "tpf0_candidates": candidates, "tpf0_parsed": parsed,
            "lists": sorted(lists, key=lambda row: row["list"]),
            "nation_glyphs": [glyphs["sb_" + n] for n in NATIONS],
            "sound_call_counts": dict(sorted(calls.items())),
            "core_keys": len(core), "battle_keys": len(battle), "union_keys": 100,
            "limits": ["signature-scan TPF0 parser, not PE resource enumeration",
                       "mask geometry checked; mask pixel semantics not revalidated",
                       "no pixels/audio exported; no game or native rendering run",
                       "WAV installation presence and format not measured"]}


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    print(json.dumps(inspect(*map(Path, sys.argv[1:])), indent=2))
