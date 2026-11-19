#!/usr/bin/env python3
"""news-image-20261118 — Sum up 18 November 2026 world news in one image.

Entry for make.fun bounty news-image-20261118.

Writes a 1024x1024 PNG front page to <output>/entry.png (default /output,
overridable with MAKEFUN_OUTPUT_DIR / OUTPUT_DIR).

The image is rendered programmatically with Pillow from the fixed story data
below — no network, no downloaded assets, no randomness: two runs write
byte-identical files. Fonts are embedded in assets/fonts/ so rendering does
not depend on system fonts. If Pillow is unavailable, main() falls back to
copying the pre-rendered assets/entry.png (same bytes).

Stories (all reported on Wednesday 18 November 2026):
  1. Xi Jinping and Vladimir Putin meet in Shenzhen, a day before the
     first-ever three-way summit with Donald Trump (APEC opens; Quad meets
     in Manila; Trump announces a Philippines trade deal).
  2. Iran strikes U.S. bases in Kuwait and Bahrain after the U.S. hit
     Qeshm Island in the Strait of Hormuz; Houthis hit a Saudi pipeline.
  3. A Ukrainian strike partly collapses the Crimea (Kerch) bridge;
     drones injure six in Dnipro.
  4. Democrat Mary Peltola wins Alaska's Senate seat; Democrats take the
     U.S. Senate 56-44.
  5. Nvidia beats forecasts: Q3 revenue $115.8bn, up 103% year on year,
     in its first report since Jensen Huang's exit.
Also noted: U.S. loses measles-elimination status; Ebola grips children
in DRC; Gaza's displaced face winter cold. Markets: S&P 500 -1.03%,
Nasdaq -0.74%, Brent $91.55, gold $3,775, VIX 25.46.

Sources: Just Security Early Edition, Level Headlines daily brief, NPR
News Now, Horizon world news — see SOURCES.md.
"""

import hashlib
import math
import os
import shutil
import sys

W, H = 1024, 1024
MX = 36                      # side margin
CW = W - 2 * MX              # content width = 952

PAPER = (250, 246, 238)      # warm newsprint
INK = (26, 26, 26)
NAVY = (20, 33, 61)
RED = (185, 28, 28)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
FONTS = os.path.join(ASSETS, "fonts")
PRE_RENDERED = os.path.join(ASSETS, "entry.png")


# ---------------------------------------------------------------- fonts
def font(name, size):
    path = os.path.join(FONTS, name)
    try:
        from PIL import ImageFont
        return ImageFont.truetype(path, size)
    except Exception:
        from PIL import ImageFont
        return ImageFont.load_default()


# ---------------------------------------------------------------- helpers
def star_points(cx, cy, r_out, r_in, n=5, rot=-90.0):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, names, sizes, max_w):
    """Largest font (from sizes, descending) in which text fits max_w."""
    for size in sizes:
        fnt = font(names, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
    return font(names, sizes[-1])


# ---------------------------------------------------------------- flags
def draw_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy, r = x + w * 0.16, y + h * 0.28, h * 0.24
    d.polygon(star_points(cx, cy, r, r * 0.42), fill=GOLD)
    for sx, sy in [(0.34, 0.10), (0.42, 0.22), (0.42, 0.38), (0.34, 0.50)]:
        r2 = h * 0.085
        d.polygon(star_points(x + w * sx, y + h * sy, r2, r2 * 0.42),
                  fill=GOLD)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_russia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 0))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_usa(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        col = (179, 25, 66) if i % 2 == 0 else WHITE
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=col)
    cw, ch = w * 0.40, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(10, 49, 97))
    for row in range(5):
        for col in range(6):
            sx = x + cw * (col + 0.5) / 6.0
            sy = y + ch * (row + 0.5) / 5.0
            r = 2.5
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


# ---------------------------------------------------------------- icons
def rounded_tile(d, x, y, s, color):
    d.rounded_rectangle([x, y, x + s, y + s], radius=14, fill=color)


def icon_rocket(d, x, y, s):
    # tile-local coords, tile s x s, origin (x, y)
    cx = x + s // 2
    d.polygon([(x + 34, y + 26), (x + 54, y + 26), (cx, y + 8)], fill=WHITE)
    d.rounded_rectangle([x + 34, y + 24, x + 54, y + 62], radius=9,
                        fill=WHITE)
    d.polygon([(x + 34, y + 50), (x + 34, y + 68), (x + 22, y + 64)],
              fill=WHITE)
    d.polygon([(x + 54, y + 50), (x + 54, y + 68), (x + 66, y + 64)],
              fill=WHITE)
    d.polygon([(x + 38, y + 62), (x + 50, y + 62), (cx, y + 80)],
              fill=(255, 200, 60))
    d.ellipse([cx - 6, y + 32, cx + 6, y + 44], fill=(194, 65, 12))


def icon_bridge(d, x, y, s):
    deck_y = y + 62
    # deck in two segments with a gap (partial collapse) + tilted piece
    d.line([x + 8, deck_y, x + 38, deck_y], fill=WHITE, width=6)
    d.line([x + 50, deck_y, x + 80, deck_y], fill=WHITE, width=6)
    d.line([x + 38, deck_y, x + 50, deck_y + 10], fill=WHITE, width=5)
    # arch
    d.arc([x + 8, y + 6, x + 80, y + 78], start=180, end=360,
          fill=WHITE, width=5)
    # pillars + suspenders
    for px in (x + 20, x + 68):
        d.line([px, deck_y, px, y + 34], fill=WHITE, width=4)
    for sx in (x + 30, x + 44, x + 58):
        d.line([sx, deck_y, sx, y + 26], fill=WHITE, width=3)


def icon_ballot(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=WHITE, width=5)
    d.line([cx - 16, cy, cx - 4, cy + 12, cx + 18, cy - 14],
           fill=WHITE, width=7, joint="curve")


def icon_chip(d, x, y, s):
    d.rectangle([x + 24, y + 24, x + 64, y + 64], outline=WHITE, width=4)
    d.rectangle([x + 36, y + 36, x + 52, y + 52], fill=WHITE)
    for i in range(3):
        off = 32 + i * 12
        d.line([x + off, y + 12, x + off, y + 24], fill=WHITE, width=4)
        d.line([x + off, y + 64, x + off, y + 76], fill=WHITE, width=4)
        d.line([x + 12, y + off, x + 24, y + off], fill=WHITE, width=4)
        d.line([x + 64, y + off, x + 76, y + off], fill=WHITE, width=4)


# ---------------------------------------------------------------- render
def render():
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font("DejaVuSerif-Bold.ttf", 58)
    f_date = font("DejaVuSans-Bold.ttf", 21)
    f_kick = font("DejaVuSans-Bold.ttf", 20)
    f_lead = font("DejaVuSans-Bold.ttf", 46)
    f_sub = font("DejaVuSans.ttf", 23)
    f_head = font("DejaVuSans-Bold.ttf", 28)
    f_sum = font("DejaVuSans.ttf", 21)
    f_also = font("DejaVuSans.ttf", 19)
    f_mkt = font("DejaVuSans-Bold.ttf", 20)
    f_foot = font("DejaVuSans.ttf", 14)
    f_flag = font("DejaVuSans-Bold.ttf", 17)

    # ---- masthead
    d.text((W // 2, 26), "THE WORLD TODAY", font=f_mast, fill=NAVY,
           anchor="ma")
    d.text((W // 2, 94), "WEDNESDAY, 18 NOVEMBER 2026", font=f_date,
           fill=RED, anchor="ma")
    d.line([MX, 126, MX + CW, 126], fill=NAVY, width=3)
    d.line([MX, 132, MX + CW, 132], fill=NAVY, width=1)

    # ---- lead story
    y = 148
    d.text((MX, y), "SUMMIT IN SHENZHEN  •  LEAD STORY", font=f_kick,
           fill=RED)
    y = 176
    lead_lines = ["XI AND PUTIN MEET IN SHENZHEN",
                  "AS TRUMP HEADS FOR SUMMIT"]
    for line in lead_lines:
        d.text((MX, y), line, font=f_lead, fill=INK)
        y += 56
    y = 292
    sub = ("Xi and Putin open talks in Shenzhen a day before the "
           "first-ever three-way summit with Trump. "
           "APEC opens; the Quad meets in Manila.")
    for line in wrap(d, sub, f_sub, CW)[:2]:
        d.text((MX, y), line, font=f_sub, fill=INK)
        y += 30

    # ---- flag strip (drawn programmatically)
    fy = 366
    fw, fh = 220, 110
    gap = (CW - 3 * fw) // 2
    flags = [(draw_china, "CHINA"), (draw_russia, "RUSSIA"),
             (draw_usa, "UNITED STATES")]
    fx = MX
    for draw_fn, label in flags:
        draw_fn(d, fx, fy, fw, fh)
        d.text((fx + fw // 2, fy + fh + 8), label, font=f_flag,
               fill=INK, anchor="ma")
        fx += fw + gap

    # ---- divider
    d.line([MX, 514, MX + CW, 514], fill=NAVY, width=3)

    # ---- four story rows
    stories = [
        ("IRAN STRIKES U.S. BASES IN KUWAIT AND BAHRAIN",
         "Tehran answers the U.S. strike on Qeshm Island; Houthi drones "
         "hit a Saudi pipeline.",
         (194, 65, 12), icon_rocket),
        ("UKRAINE STRIKE PARTLY COLLAPSES CRIMEA BRIDGE",
         "Drones injure six in Dnipro as Kyiv steps up attacks on "
         "Russian supply lines.",
         (37, 99, 235), icon_bridge),
        ("DEMOCRATS TAKE THE U.S. SENATE, 56–44",
         "Peltola wins Alaska, unseating Sullivan in the last midterm "
         "race to be called.",
         (109, 40, 217), icon_ballot),
        ("NVIDIA BEATS FORECASTS: REVENUE $115.8BN",
         "Sales up 103% in the first report since Jensen Huang's exit; "
         "he will not return.",
         (21, 128, 61), icon_chip),
    ]
    ry = 532
    tile = 88
    for headline, summary, color, icon in stories:
        rounded_tile(d, MX, ry, tile, color)
        icon(d, MX, ry, tile)
        tx = MX + tile + 16
        tw = CW - tile - 16
        hf = fit_font(d, headline, "DejaVuSans-Bold.ttf",
                      [28, 27, 26, 25, 24], tw)
        d.text((tx, ry + 2), headline, font=hf, fill=INK)
        sy = ry + 38
        for line in wrap(d, summary, f_sum, tw)[:2]:
            d.text((tx, sy), line, font=f_sum, fill=(60, 60, 60))
            sy += 26
        ry += 98

    # ---- also in the news
    also = ("ALSO:  U.S. loses measles-free status  •  Ebola grips "
            "children in DRC  •  Cold grips Gaza's displaced")
    ay = 932
    for line in wrap(d, also, f_also, CW)[:2]:
        d.text((MX, ay), line, font=f_also, fill=GREY)
        ay += 24

    # ---- markets band
    d.rectangle([0, 962, W, 1000], fill=NAVY)
    mkt = ("MARKETS   S&P 500  −1.03%    Nasdaq  −0.74%    Brent $91.55    "
           "Gold $3,775    VIX 25.46")
    d.text((W // 2, 970), mkt, font=f_mkt, fill=WHITE, anchor="ma")

    # ---- footer
    d.text((W // 2, 1005), "A summary of world news — Wednesday 18 November 2026",
           font=f_foot, fill=GREY, anchor="ma")

    return img


def main():
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
               or os.environ.get("OUTPUT_DIR") or "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")

    try:
        img = render()
        img.save(out_path, format="PNG")
    except Exception as exc:  # Pillow missing/broken: use pre-rendered
        print(f"render failed ({exc}); copying pre-rendered image",
              file=sys.stderr)
        if not os.path.exists(PRE_RENDERED):
            raise
        shutil.copyfile(PRE_RENDERED, out_path)

    with open(out_path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    size = os.path.getsize(out_path)
    print(f"wrote {out_path} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
