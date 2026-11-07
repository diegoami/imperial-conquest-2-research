"""Synthetic boundary tests for the intake checker; no original media needed."""
import importlib.util
from pathlib import Path
import struct
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "assets218", Path(__file__).resolve().parents[1] / "original-assets218-check.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def bmp(width=3, height=2, depth=8):
    palette = (1 << depth) * 4
    offset = 54 + palette
    stride = ((width * depth + 31) // 32) * 4
    result = bytearray(offset + stride * abs(height))
    result[:2] = b"BM"
    struct.pack_into("<I", result, 2, len(result))
    struct.pack_into("<II", result, 10, offset, 40)
    struct.pack_into("<iiHHI", result, 18, width, height, 1, depth, 0)
    return result


class BitmapBounds(unittest.TestCase):
    def test_unknown_executable_rejected_before_other_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            exe = Path(directory) / "unsupported.exe"
            exe.write_bytes(b"synthetic unsupported profile")
            with self.assertRaisesRegex(ValueError, "unsupported EXE profile"):
                checker.inspect(exe, Path("absent-dump"), Path("absent-source"),
                                Path("absent-remake"))

    def test_padded_rows_and_signed_height(self):
        for depth in (1, 4, 8):
            for height, orientation in ((2, "bottom-up"), (-2, "top-down")):
                with self.subTest(depth=depth, height=height):
                    self.assertEqual(checker.bitmap(bmp(height=height, depth=depth)),
                                     {"width": 3, "height": 2, "bpp": depth,
                                      "orientation": orientation})

    def test_truncated_final_padded_row(self):
        with self.assertRaisesRegex(ValueError, "truncated"):
            checker.bitmap(bmp()[:-1])

    def test_palette_overlaps_pixels(self):
        data = bmp()
        struct.pack_into("<I", data, 10, 54)
        with self.assertRaisesRegex(ValueError, "palette"):
            checker.bitmap(data)

    def test_compressed_bitmap_is_unsupported(self):
        data = bmp()
        struct.pack_into("<I", data, 30, 1)
        with self.assertRaisesRegex(ValueError, "encoding"):
            checker.bitmap(data)

    def test_impossible_palette_count(self):
        data = bmp(depth=4)
        struct.pack_into("<I", data, 46, 17)
        with self.assertRaisesRegex(ValueError, "palette"):
            checker.bitmap(data)

    def test_empty_and_negative_geometry(self):
        for offset, value in ((18, 0), (18, -1), (22, 0)):
            data = bmp()
            struct.pack_into("<i", data, offset, value)
            with self.assertRaisesRegex(ValueError, "dimensions"):
                checker.bitmap(data)


if __name__ == "__main__":
    unittest.main()
