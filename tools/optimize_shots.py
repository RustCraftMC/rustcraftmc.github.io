"""Turn raw launcher screenshots (PNG) into WebP files for the website.

Usage:
    python -I optimize_shots.py <input_dir> [--out <output_dir>]

Every *.png in <input_dir> named "<scene>.<lang>.<mode>.png" becomes two WebP files in the output
folder. The names use dashes instead of dots, e.g. "home-zh-dark.webp":
    <name>.webp       1680 px wide, quality 82 (quality 76 if that file would exceed 300 KB)
    <name>-840.webp   840 px wide, quality 80
The default output folder is cairnlauncher/assets/shots, next to this tools folder.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

WIDE_PX = 1680
NARROW_PX = 840
WIDE_QUALITY = 82
WIDE_FALLBACK_QUALITY = 76
NARROW_QUALITY = 80
WIDE_BUDGET_BYTES = 300 * 1024

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "cairnlauncher" / "assets" / "shots"


def scaled(img, width):
    if img.width == width:
        return img
    height = round(img.height * width / img.width)
    return img.resize((width, height), Image.Resampling.LANCZOS)


def save_webp(img, path, quality):
    img.save(path, "WEBP", quality=quality, method=6)
    return path.stat().st_size


def convert(png, out_dir):
    stem = png.name[: -len(".png")].replace(".", "-")
    with Image.open(png) as src:
        rgba = src.convert("RGBA")
    alpha_min, _ = rgba.getchannel("A").getextrema()
    notes = []
    if alpha_min != 255:
        notes.append(f"alpha is not all 255 (min {alpha_min})")
        base = rgba
    else:
        # Fully opaque pictures do not need an alpha channel. Dropping it makes the files smaller.
        base = rgba.convert("RGB")

    wide = scaled(base, WIDE_PX)
    wide_path = out_dir / f"{stem}.webp"
    wide_size = save_webp(wide, wide_path, WIDE_QUALITY)
    if wide_size > WIDE_BUDGET_BYTES:
        wide_size = save_webp(wide, wide_path, WIDE_FALLBACK_QUALITY)
        notes.append(f"quality {WIDE_FALLBACK_QUALITY}: {WIDE_QUALITY} gave more than 300 KB")

    narrow = scaled(base, NARROW_PX)
    narrow_size = save_webp(narrow, out_dir / f"{stem}-840.webp", NARROW_QUALITY)
    return stem, wide_size, narrow_size, notes


def main():
    parser = argparse.ArgumentParser(description="Convert screenshot PNG files into website WebP files.")
    parser.add_argument("input_dir", type=Path, help="folder that holds the PNG screenshots")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output folder (default: {DEFAULT_OUT})")
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        print(f"not a folder: {args.input_dir}", file=sys.stderr)
        return 2
    pngs = sorted(args.input_dir.glob("*.png"))
    if not pngs:
        print(f"no PNG files in {args.input_dir}", file=sys.stderr)
        return 1
    args.out.mkdir(parents=True, exist_ok=True)

    total = 0
    for png in pngs:
        stem, wide_size, narrow_size, notes = convert(png, args.out)
        total += wide_size + narrow_size
        line = f"{stem}: {wide_size / 1024:.0f} KB + {narrow_size / 1024:.0f} KB"
        if notes:
            line += "  [" + "; ".join(notes) + "]"
        print(line)
    print(f"{len(pngs)} PNG files -> {2 * len(pngs)} WebP files, {total / 1024 / 1024:.2f} MB in total, written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
