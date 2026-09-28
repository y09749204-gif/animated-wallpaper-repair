"""Check that a local PNG edit stays inside an explicit source-pixel rectangle.

Requires Pillow. Exit 0 on pass, 1 on invariant failure, 2 on invalid input.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw
except ImportError as exc:
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc


def _binary(mask: Image.Image) -> Image.Image:
    return mask.point(lambda value: 255 if value else 0)


def verify_images(
    before: Image.Image,
    after: Image.Image,
    roi: tuple[int, int, int, int],
    allow_alpha_change: bool = False,
) -> dict[str, object]:
    if before.size != after.size:
        raise ValueError(f"Image dimensions differ: {before.size} vs {after.size}")
    x, y, width, height = roi
    image_width, image_height = before.size
    if width <= 0 or height <= 0 or x < 0 or y < 0 or x + width > image_width or y + height > image_height:
        raise ValueError(f"ROI {roi} is outside image dimensions {before.size}")

    channels = ImageChops.difference(before.convert("RGBA"), after.convert("RGBA")).split()
    changed = _binary(ImageChops.lighter(ImageChops.lighter(channels[0], channels[1]),
                                    ImageChops.lighter(channels[2], channels[3])))
    alpha_changed = _binary(channels[3])
    outside = Image.new("L", before.size, 255)
    ImageDraw.Draw(outside).rectangle((x, y, x + width - 1, y + height - 1), fill=0)
    outside_changed = ImageChops.multiply(changed, outside)

    changed_pixels = changed.histogram()[255]
    outside_pixels = outside_changed.histogram()[255]
    alpha_pixels = alpha_changed.histogram()[255]
    passed = outside_pixels == 0 and (allow_alpha_change or alpha_pixels == 0)
    return {
        "passed": passed,
        "image_size": [image_width, image_height],
        "roi": [x, y, width, height],
        "changed_pixels": changed_pixels,
        "changed_outside_roi": outside_pixels,
        "alpha_changed_pixels": alpha_pixels,
        "changed_bbox": list(changed.getbbox()) if changed.getbbox() else None,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--roi", nargs=4, metavar=("X", "Y", "WIDTH", "HEIGHT"), type=int, required=True)
    parser.add_argument("--allow-alpha-change", action="store_true",
                        help="Allow alpha edits inside the ROI; edits outside it still fail")
    args = parser.parse_args(argv)
    try:
        with Image.open(args.before) as before, Image.open(args.after) as after:
            result = verify_images(before, after, tuple(args.roi), args.allow_alpha_change)
    except (OSError, ValueError) as exc:
        print(f"pixel-scope error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
