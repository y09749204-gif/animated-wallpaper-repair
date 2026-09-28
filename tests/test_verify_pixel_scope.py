import sys
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_pixel_scope import verify_images  # noqa: E402


class VerifyPixelScopeTests(unittest.TestCase):
    def setUp(self):
        self.before = Image.new("RGBA", (8, 8), (120, 100, 90, 255))
        self.after = self.before.copy()

    def test_rgb_edit_inside_roi_passes(self):
        self.after.putpixel((3, 3), (130, 100, 90, 255))
        result = verify_images(self.before, self.after, (2, 2, 3, 3))
        self.assertTrue(result["passed"])
        self.assertEqual(result["changed_pixels"], 1)

    def test_edit_outside_roi_fails(self):
        self.after.putpixel((6, 3), (130, 100, 90, 255))
        result = verify_images(self.before, self.after, (2, 2, 3, 3))
        self.assertFalse(result["passed"])
        self.assertEqual(result["changed_outside_roi"], 1)

    def test_alpha_change_requires_opt_in(self):
        self.after.putpixel((3, 3), (120, 100, 90, 200))
        self.assertFalse(verify_images(self.before, self.after, (2, 2, 3, 3))["passed"])
        self.assertTrue(verify_images(self.before, self.after, (2, 2, 3, 3), True)["passed"])

    def test_invalid_roi_is_rejected(self):
        with self.assertRaises(ValueError):
            verify_images(self.before, self.after, (7, 7, 2, 2))


if __name__ == "__main__":
    unittest.main()
