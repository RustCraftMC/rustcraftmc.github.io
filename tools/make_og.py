"""Make the link-preview images and the app icon for the website.

Usage:
    python -I make_og.py

Inputs: cairnlauncher/assets/brand/logo.png, assets/brand/rustcraftmc.png (the organization icon) and
cairnlauncher/assets/shots/home-{zh,en}-dark.webp (run optimize_shots.py first). Outputs, overwritten on every run:
    cairnlauncher/assets/og-zh.png, og-en.png   1200 x 630 link previews for the Cairn Launcher page
    cairnlauncher/assets/apple-touch-icon.png    180 x 180 home-screen icon of the Cairn Launcher page
    assets/og.png                                1200 x 630 link preview for the organization page
    assets/favicon.png, assets/apple-touch-icon.png   icons of the organization page (from rustcraftmc.png)
Fonts are read from the Windows font folder (Segoe UI and Microsoft YaHei).
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
BRAND = SITE / "cairnlauncher" / "assets" / "brand"
SHOTS = SITE / "cairnlauncher" / "assets" / "shots"
CAIRN_ASSETS = SITE / "cairnlauncher" / "assets"
ROOT_ASSETS = SITE / "assets"

FONT_DIR = Path(r"C:\Windows\Fonts")
SEGOE_BOLD = FONT_DIR / "segoeuib.ttf"
SEGOE = FONT_DIR / "segoeui.ttf"
YAHEI = FONT_DIR / "msyh.ttc"

BG = (11, 12, 15)  # #0b0c0f
INK = (241, 237, 228)  # #f1ede4
GOLD = (228, 184, 99)  # #E4B863
MUTED = (154, 150, 140)  # #9a968c

W, H = 1200, 630
MARGIN = 72
SHOT_W = 760
SHOT_RADIUS = 14
SHOT_OVERHANG = 36  # the screenshot runs this many pixels past the right edge of the image
URL_TEXT = "rustcraftmc.github.io/cairnlauncher"
TAGLINE = {
    "zh": ("纯粹 · 优雅 · 灵动的现代 Minecraft 启动器", YAHEI),
    "en": ("Pure, elegant, and modern Minecraft launcher", SEGOE),
}


def load_font(path, size):
    if not path.exists():
        sys.exit(f"font not found: {path}")
    return ImageFont.truetype(str(path), size)


def fit(img, box):
    """Scale an image to fit inside a box x box square, keeping its proportions."""
    img = img.convert("RGBA")
    scale = min(box / img.width, box / img.height)
    size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
    return img.resize(size, Image.Resampling.LANCZOS)


def rounded_mask(size, radius, scale=4):
    """Anti-aliased rounded-rectangle mask."""
    w, h = size
    big = Image.new("L", (w * scale, h * scale), 0)
    ImageDraw.Draw(big).rounded_rectangle((0, 0, w * scale - 1, h * scale - 1), radius=radius * scale, fill=255)
    return big.resize((w, h), Image.Resampling.LANCZOS)


def wrap(text, fnt, max_width):
    """Greedy line wrap. CJK characters can break anywhere; Latin words break at spaces."""
    parts = re.findall(r"[\u3000-\u9fff]|[^\s\u3000-\u9fff]+|\s+", text)
    lines, line = [], ""
    for part in parts:
        if part.isspace():
            line += " " if line else ""
            continue
        candidate = line + part
        if line and fnt.getlength(candidate.rstrip()) > max_width:
            lines.append(line.rstrip())
            line = part
        else:
            line = candidate
    if line.strip():
        lines.append(line.rstrip())
    return lines


def draw_block(draw, x, y, lines, fnt, fill, leading):
    for text in lines:
        draw.text((x, y), text, font=fnt, fill=fill)
        y += leading
    return y


def link_card(lang, logo):
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # Left column: logo, product name, tagline.
    text_width = (W + SHOT_OVERHANG - SHOT_W) - MARGIN - 40
    tagline, tagline_path = TAGLINE[lang]
    title_font = load_font(SEGOE_BOLD, 78)
    tagline_font = load_font(tagline_path, 34)
    title_lines = wrap("Cairn Launcher", title_font, text_width)
    tagline_lines = wrap(tagline, tagline_font, text_width)
    mark = fit(logo, 104)
    title_leading, tagline_leading = 84, 48
    block = mark.height + 34 + len(title_lines) * title_leading + 26 + len(tagline_lines) * tagline_leading
    top = (H - block) // 2 - 8

    canvas.paste(mark, (MARGIN, top), mark)
    y = top + mark.height + 34
    y = draw_block(draw, MARGIN, y, title_lines, title_font, INK, title_leading) + 26
    draw_block(draw, MARGIN, y, tagline_lines, tagline_font, GOLD, tagline_leading)
    draw.text((MARGIN, H - 56), URL_TEXT, font=load_font(SEGOE, 22), fill=MUTED)

    # Right: the home page screenshot, rounded, with a faint 1 px border.
    shot = Image.open(SHOTS / f"home-{lang}-dark.webp").convert("RGB")
    shot = shot.resize((SHOT_W, round(shot.height * SHOT_W / shot.width)), Image.Resampling.LANCZOS)
    x = W + SHOT_OVERHANG - SHOT_W
    y = (H - shot.height) // 2
    outer = rounded_mask(shot.size, SHOT_RADIUS)
    inner = Image.new("L", shot.size, 0)
    inner.paste(rounded_mask((shot.width - 2, shot.height - 2), SHOT_RADIUS - 1), (1, 1))
    border = ImageChops.subtract(outer, inner).point(lambda v: round(v * 0.12))
    canvas.paste(shot, (x, y), outer)
    canvas.paste((255, 255, 255), (x, y, x + shot.width, y + shot.height), border)
    return canvas


def apple_touch_icon(logo):
    size = 180
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base = Image.new("RGBA", (size, size), BG + (255,))
    icon.paste(base, (0, 0), rounded_mask((size, size), 40))
    mark = fit(logo, round(size * 0.70))
    icon.alpha_composite(mark, ((size - mark.width) // 2, (size - mark.height) // 2))
    return icon


def root_card(logo):
    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)
    size = 128
    word_font = load_font(SEGOE_BOLD, size)
    team = " Team"
    # Keep "RustCraftMC Team" on one line inside the margins.
    while word_font.getlength("RustCraftMC" + team) > W - 2 * MARGIN and size > 60:
        size -= 2
        word_font = load_font(SEGOE_BOLD, size)
    y = 200
    draw.text((MARGIN, y), "RustCraftMC", font=word_font, fill=INK)
    draw.text((MARGIN + word_font.getlength("RustCraftMC"), y), team, font=word_font, fill=GOLD)
    draw.text((MARGIN, y + round(size * 1.25)), "github.com/RustCraftMC", font=load_font(SEGOE, 30), fill=MUTED)
    mark = fit(logo, 220)
    canvas.paste(mark, (W - 60 - mark.width, H - 60 - mark.height), mark)
    return canvas, size


ORG_LOGO = ROOT_ASSETS / "brand" / "rustcraftmc.png"  # the organization icon, supplied by the maintainer


def org_mark(logo):
    """The grass block and the crab without the RUSTCRAFT lettering, as a square. Readable at 32 px."""
    art = logo.crop((0, 0, logo.width, round(logo.height * 0.87)))  # drop the lettering at the bottom
    box = art.getchannel("A").getbbox()
    art = art.crop(box)
    side = max(art.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.alpha_composite(art, ((side - art.width) // 2, (side - art.height) // 2))
    return square


def org_icons(logo):
    mark = org_mark(logo)
    favicon = mark.resize((64, 64), Image.Resampling.LANCZOS)
    size = 180
    touch = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    touch.paste(Image.new("RGBA", (size, size), BG + (255,)), (0, 0), rounded_mask((size, size), 40))
    inner = fit(mark, round(size * 0.72))
    touch.alpha_composite(inner, ((size - inner.width) // 2, (size - inner.height) // 2))
    return favicon, touch


def main():
    if not (SHOTS / "home-zh-dark.webp").exists():
        sys.exit("screenshots missing: run optimize_shots.py first")
    logo = Image.open(BRAND / "logo.png").convert("RGBA")
    org_logo = Image.open(ORG_LOGO).convert("RGBA")
    CAIRN_ASSETS.mkdir(parents=True, exist_ok=True)
    ROOT_ASSETS.mkdir(parents=True, exist_ok=True)
    favicon, touch = org_icons(org_logo)
    favicon.save(ROOT_ASSETS / "favicon.png", "PNG", optimize=True)
    touch.save(ROOT_ASSETS / "apple-touch-icon.png", "PNG", optimize=True)
    print("wrote assets/favicon.png and assets/apple-touch-icon.png")

    for lang in ("zh", "en"):
        out = CAIRN_ASSETS / f"og-{lang}.png"
        link_card(lang, logo).save(out, "PNG", optimize=True)
        print(f"wrote {out}")

    icon = CAIRN_ASSETS / "apple-touch-icon.png"
    apple_touch_icon(logo).save(icon, "PNG", optimize=True)
    print(f"wrote {icon}")

    canvas, size = root_card(org_logo)
    out = ROOT_ASSETS / "og.png"
    canvas.save(out, "PNG", optimize=True)
    print(f"wrote {out} (title size {size}px)")


if __name__ == "__main__":
    main()
