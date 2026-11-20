#!/usr/bin/env python3
"""Build social/favicon assets for the portfolio site.

Run:  python3 tools/build_assets.py

Outputs (written into the site's static/ dir):
  static/images/og-card.jpg   1200x630 Open Graph / Twitter card image
  static/favicon.svg          vector monogram
  static/favicon-32.png       raster fallback
  static/apple-touch-icon.png 180x180 iOS home-screen icon

Fonts are pulled from the google/fonts repo into the scratch dir; the site
itself loads them from Google Fonts.
"""
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
STATIC = os.path.join(SITE, "static")
FONTS = os.path.join(HERE, "fonts")

FONT_SOURCES = {
    "InstrumentSerif-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/instrumentserif/InstrumentSerif-Regular.ttf",
    "InstrumentSerif-Italic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/instrumentserif/InstrumentSerif-Italic.ttf",
    "Inter.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf",
    "JBMono.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}


def ensure_fonts():
    """Fetch the OFL fonts the site uses (Google Fonts repo) on first run."""
    os.makedirs(FONTS, exist_ok=True)
    for name, url in FONT_SOURCES.items():
        dest = os.path.join(FONTS, name)
        if not os.path.exists(dest):
            print("fetching", name)
            urllib.request.urlretrieve(url, dest)

NAVY = (11, 26, 51)
NAVY_SOFT = (17, 35, 64)
CREAM = (247, 245, 240)
GOLD = (200, 164, 92)
STONE = (232, 226, 214)

SERIF = os.path.join(FONTS, "InstrumentSerif-Regular.ttf")
SERIF_IT = os.path.join(FONTS, "InstrumentSerif-Italic.ttf")
SANS = os.path.join(FONTS, "Inter.ttf")
MONO = os.path.join(FONTS, "JBMono.ttf")


def tracked(draw, xy, text, font, fill, tracking=3.0):
    """Draw text with manual letter-spacing (PIL has none)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def tracked_width(draw, text, font, tracking=3.0):
    return sum(draw.textlength(c, font=font) + tracking for c in text) - tracking


def circle_portrait(size, border=3):
    """Circular crop of the site headshot with a thin gold ring."""
    src = Image.open(os.path.join(STATIC, "images", "headshot.jpg")).convert("RGB")
    src = src.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size + border * 4, size + border * 4), (0, 0, 0, 0))
    ring = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse(
        (0, 0, out.size[0] - 1, out.size[1] - 1), outline=GOLD + (255,), width=border
    )
    out.paste(src, (border * 2, border * 2), mask)
    out.alpha_composite(ring)
    return out


def build_og():
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(card)

    # soft vertical warmth: navy -> slightly lighter navy at the bottom
    for y in range(H):
        t = y / H
        d.line(
            [(0, y), (W, y)],
            fill=tuple(int(NAVY[i] + (NAVY_SOFT[i] - NAVY[i]) * t) for i in range(3)),
        )

    # inset hairline frame
    d.rectangle([28, 28, W - 29, H - 29], outline=(255, 255, 255, 0) if False else (38, 56, 86), width=1)

    pad = 84
    f_label = ImageFont.truetype(MONO, 19)
    f_name = ImageFont.truetype(SERIF, 92)
    f_role = ImageFont.truetype(SANS, 28)
    f_org = ImageFont.truetype(SANS, 28)
    f_foot = ImageFont.truetype(MONO, 17)

    # portrait, right side
    p = circle_portrait(300)
    card.paste(p, (W - p.size[0] - 66, 132), p)

    # eyebrow label
    label = "STRATEGY \u00b7 HEALTHCARE AI \u00b7 INNOVATION"
    tracked(d, (pad, 150), label, f_label, GOLD, tracking=2.4)

    # name
    d.text((pad - 4, 186), "Christopher Khoury", font=f_name, fill=CREAM)

    # gold rule
    d.line([(pad, 344), (pad + 96, 344)], fill=GOLD, width=3)

    # role
    d.text((pad, 382), "Vice President, Strategic Insights", font=f_role, fill=CREAM)
    d.text((pad, 422), "American Medical Association", font=f_org, fill=(190, 186, 176))

    # footer line
    tracked(d, (pad, 520), "BOARD MEMBER \u00b7 ADVISOR \u00b7 SPEAKER", f_foot, (150, 148, 140), tracking=2.0)

    out = os.path.join(STATIC, "images", "og-card.jpg")
    card.save(out, quality=92, optimize=True)
    print("wrote", out, os.path.getsize(out) // 1024, "KB")


def build_favicon_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Christopher Khoury">
  <rect width="64" height="64" rx="10" fill="#0B1A33"/>
  <text x="32" y="45" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif" font-size="34"
        letter-spacing="-1" fill="#F7F5F0">CK</text>
  <rect x="20" y="49" width="24" height="2" fill="#C8A45C"/>
</svg>
"""
    out = os.path.join(STATIC, "favicon.svg")
    with open(out, "w") as fh:
        fh.write(svg)
    print("wrote", out)


def build_favicon_png(size, path, radius_ratio=0.16, rule=True, fill_ratio=0.52):
    """Raster monogram: navy rounded square, cream CK, gold hairline."""
    scale = 8  # supersample for clean edges
    S = size * scale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius_ratio), fill=NAVY + (255,))

    font = ImageFont.truetype(SERIF, int(S * fill_ratio))
    text = "CK"
    # optical centering: measure actual ink box
    box = d.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    cy = S * 0.44 if rule else S * 0.50
    d.text(((S - tw) / 2 - box[0], cy - th / 2 - box[1]), text, font=font, fill=CREAM + (255,))

    if rule:
        # gold hairline under the monogram
        rw = int(S * 0.32)
        ry = int(S * 0.74)
        d.rounded_rectangle([(S - rw) // 2, ry, (S + rw) // 2, ry + max(2, int(S * 0.028))],
                            radius=int(S * 0.014), fill=GOLD + (255,))

    img = img.resize((size, size), Image.LANCZOS)
    img.save(path)
    print("wrote", path, os.path.getsize(path) // 1024, "KB")


if __name__ == "__main__":
    ensure_fonts()
    build_og()
    build_favicon_svg()
    build_favicon_png(32, os.path.join(STATIC, "favicon-32.png"), radius_ratio=0.22, rule=False, fill_ratio=0.58)
    build_favicon_png(180, os.path.join(STATIC, "apple-touch-icon.png"), radius_ratio=0.0)
