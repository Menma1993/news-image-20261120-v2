#!/usr/bin/env python3
"""Draw the v2 front page for news-image-20261120 (Friday 20 November 2026).

Fresh build, drawn from scratch with PIL. Deterministic (seeded random).
Run: python3 draw.py  ->  writes entry.png (1024x1024, <=1 MiB).
The submitted program (main.py) only copies entry.png to /output/entry.png.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
M = 16                      # page margin
CW = W - 2 * M              # content width = 992

PAPER = (247, 242, 231)
PAPER_DK = (238, 231, 214)
INK = (20, 20, 20)
RED = (176, 30, 30)
RED_BR = (198, 44, 36)
NAVY = (13, 43, 69)
NAVY_LT = (42, 74, 107)
TEAL = (14, 90, 102)
TEAL_DK = (10, 58, 66)
GOLD = (201, 162, 39)
GREY = (107, 107, 107)
GREY_LT = (140, 134, 120)
CREAM_CARD = (252, 249, 240)

FDIR = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF = "NotoSerif-Regular.ttf"
SERIF_B = "NotoSerif-Bold.ttf"
SERIF_I = "NotoSerif-Italic.ttf"
SERIF_BI = "NotoSerif-BoldItalic.ttf"
SANS = "NotoSans-Regular.ttf"
SANS_B = "NotoSans-Bold.ttf"
SANS_I = "NotoSans-Italic.ttf"

rnd = random.Random(42)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# ---------- helpers ----------
def wrap(text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

def hline(y, fill=INK, width=1, x0=None, x1=None):
    d.line([(x0 if x0 is not None else M, y), (x1 if x1 is not None else W - M, y)],
           fill=fill, width=width)

def vgrad(x0, y0, x1, y1, top, bottom):
    """Vertical gradient rectangle."""
    h = max(1, y1 - y0)
    g = Image.new("RGB", (1, h))
    px = g.load()
    for i in range(h):
        t = i / max(1, h - 1)
        px[0, i] = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
    g = g.resize((x1 - x0, h))
    img.paste(g, (x0, y0))

def glow_layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def paste_glow(layer, blur=6):
    img.paste(Image.alpha_composite(img.convert("RGBA"),
              layer.filter(ImageFilter.GaussianBlur(blur))).convert("RGB"), (0, 0))

def chip(x, y, s, fnt, fg=(255, 255, 255), bg=RED, pad=5, h=None):
    w = int(d.textlength(s, font=fnt)) + 2 * pad
    hh = h or (fnt.size + 2 * pad - 2)
    d.rounded_rectangle([x, y, x + w, y + hh], radius=2, fill=bg)
    d.text((x + pad, y + (hh - fnt.size) / 2 - 1), s, font=fnt, fill=fg)
    return w, hh

def paper_texture():
    for _ in range(2600):
        x = rnd.randint(0, W - 1)
        y = rnd.randint(0, H - 1)
        a = rnd.randint(4, 12)
        d.point((x, y), fill=(120, 110, 90, a))

paper_texture()

# ---------- header ----------
y = 12
hline(y, width=2)
y += 6
text(M, y, "THE WORLD IN ONE DAY", font(SANS_B, 13), fill=RED)
r = "38 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
text(W - M, y, r, font(SANS_B, 11), fill=INK, anchor="ra")
y += 20
hline(y, width=1)
y += 4
text(W // 2, y, "Friday 20 November 2026", font(SERIF_B, 62), anchor="ma")
y += 68
text(W // 2, y, "Russian missiles hit Kyiv's bridges  ·  Cyclone Akvan strikes India  ·  "
     "An AI sell-off sinks Asia's markets  ·  UK and EU seal a deal",
     font(SERIF_I, 16), fill=RED, anchor="ma")
y += 26
hline(y, width=2)
y += 6

# ---------- UTC timeline strip ----------
tl = [("00:00", "Kyiv bridges hit"), ("02:00", "Akvan landfall"),
      ("05:30", "Taiex ends -6.2%"), ("05:50", "Missile lands in Poland"),
      ("15:00", "COP31 runs past close"), ("19:10", "California probes Nvidia"),
      ("21:00", "Wall St falls a 5th day")]
d.rectangle([M, y, W - M, y + 26], fill=NAVY)
text(M + 8, y + 6, "THE DAY IN UTC", font(SANS_B, 11), fill=(255, 214, 90))
tx = M + 118
step = (W - M - tx - 6) / len(tl)
for i, (t, label) in enumerate(tl):
    x = tx + i * step
    d.text((x, y + 2), t, font=font(SANS_B, 11), fill=(255, 214, 90))
    d.text((x, y + 13), label, font=font(SANS, 9), fill=(235, 238, 240))
y += 30

# ---------- numbers strip ----------
nums = [
    ("110+", "missiles fired at Ukraine", "27 of them ballistic", "ZELENSKY"),
    ("300,000+", "people moved to shelters", "ahead of Cyclone Akvan", "IMD"),
    ("-6.2%", "Taiex, Friday's close", "worst week since 1991", "TAIEX"),
    ("2.2%", "Japan core CPI, October", "highest this year", "STATISTICS BUREAU"),
    ("$48.3bn", "US cost of the Iran war", "Pentagon estimate", "PENTAGON"),
    ("118", "Phillips' runs vs India", "hundreds in all formats", "ICC"),
]
ny = y
cell_w = CW / 6
for i, (v, c1, c2, src) in enumerate(nums):
    x0 = M + i * cell_w
    if i:
        d.line([(x0, ny + 4), (x0, ny + 52)], fill=(190, 180, 160), width=1)
    cx = x0 + cell_w / 2
    text(cx, ny, v, font(SANS_B, 25), fill=RED, anchor="ma")
    text(cx, ny + 30, c1, font(SANS_B, 10), anchor="ma")
    text(cx, ny + 42, c2 + "  ·  " + src, font(SANS, 8.5), fill=GREY, anchor="ma")
y += 54
hline(y, width=1)
y += 5

# ---------- region chips ----------
regions = [("EUROPE", 9, (44, 84, 140)), ("AMERICAS", 4, (120, 60, 60)),
           ("ASIA-PACIFIC", 8, (176, 30, 30)), ("MIDDLE EAST", 4, (120, 90, 20)),
           ("AFRICA", 7, (30, 110, 70)), ("OCEANIA", 4, (20, 120, 130)),
           ("WORLD", 2, (90, 90, 90))]
rx = M
for name, n, col in regions:
    s = f"{name} {n}"
    w, _ = chip(rx, y, s, font(SANS_B, 10), bg=col, pad=6, h=17)
    rx += w + 6
y += 24

# ---------- lead art ----------
def art_kyiv(x0, y0, w, h):
    """Night Kyiv: gradient sky, stars, skyline, burning bridges, missile trails."""
    vgrad(x0, y0, x0 + w, y0 + h, (8, 22, 46), (24, 62, 102))
    gl = glow_layer()
    g = ImageDraw.Draw(gl)
    # stars
    for _ in range(46):
        sx = x0 + rnd.randint(4, w - 4)
        sy = y0 + rnd.randint(3, int(h * 0.45))
        r = rnd.choice([1, 1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255, rnd.randint(140, 230)))
    # moon glow
    g.ellipse([x0 + w - 52, y0 + 8, x0 + w - 22, y0 + 38], fill=(255, 244, 200, 160))
    d.ellipse([x0 + w - 50, y0 + 10, x0 + w - 24, y0 + 36], fill=(255, 246, 214))
    # skyline silhouette
    base = y0 + h - 26
    bx = x0
    while bx < x0 + w:
        bw = rnd.randint(14, 30)
        bh = rnd.randint(18, 52)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(6, 12, 24))
        for _ in range(rnd.randint(2, 6)):
            wx = bx + rnd.randint(3, max(4, bw - 5))
            wy = base - bh + rnd.randint(4, max(5, bh - 6))
            d.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 200, 90, 220))
        bx += bw + rnd.randint(1, 5)
    # river band
    d.rectangle([x0, base, x0 + w, y0 + h], fill=(10, 26, 48))
    # bridges (3 arches) + fire glow
    for i, bx0 in enumerate([x0 + 12, x0 + w // 2 - 42, x0 + w - 108]):
        bw = 88
        d.arc([bx0, base - 16, bx0 + bw, base + 16], 180, 360, fill=(200, 210, 220), width=3)
        d.line([(bx0 - 4, base - 2), (bx0 + bw + 4, base - 2)], fill=(200, 210, 220), width=2)
        fx = bx0 + bw // 2
        g.ellipse([fx - 16, base - 22, fx + 16, base + 6], fill=(255, 140, 30, 200))
        g.ellipse([fx - 8, base - 14, fx + 8, base + 2], fill=(255, 210, 90, 230))
        d.ellipse([fx - 4, base - 8, fx + 4, base], fill=(255, 220, 120))
    paste_glow(gl, blur=5)
    # missile trails: glowing dotted arcs
    gl2 = glow_layer()
    g2 = ImageDraw.Draw(gl2)
    for (sx, sy, ex, ey) in [(x0 + 30, y0 + 12, x0 + 150, base - 30),
                             (x0 + 120, y0 + 6, x0 + 230, base - 40),
                             (x0 + 210, y0 + 16, x0 + 300, base - 26)]:
        pts = []
        for t_i in range(21):
            t = t_i / 20
            px = sx + (ex - sx) * t
            py = sy + (ey - sy) * t - 26 * math.sin(math.pi * t)
            pts.append((px, py))
        for (px, py) in pts[::2]:
            g2.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 190, 80, 250))
        d.line(pts, fill=(255, 220, 150, 170), width=1)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 230, 150))
    paste_glow(gl2, blur=3)

def art_akvan(x0, y0, w, h):
    """Bay of Bengal: sea gradient, India coast, bold cyclone spiral, landfall dot."""
    vgrad(x0, y0, x0 + w, y0 + h, (16, 96, 122), (10, 58, 84))
    # land mass (east India coast, simplified) upper-left
    land = [(x0, y0), (x0 + int(w * 0.52), y0), (x0 + int(w * 0.46), y0 + int(h * 0.34)),
            (x0 + int(w * 0.40), y0 + int(h * 0.55)), (x0 + int(w * 0.30), y0 + int(h * 0.72)),
            (x0 + int(w * 0.16), y0 + int(h * 0.86)), (x0, y0 + h)]
    d.polygon(land, fill=(214, 190, 138))
    d.line(land[1:], fill=(150, 125, 80), width=2)
    text(x0 + 8, y0 + 6, "ODISHA", font(SANS_B, 11), fill=(90, 70, 40))
    text(x0 + 8, y0 + 20, "INDIA", font(SANS, 9), fill=(90, 70, 40))
    text(x0 + w - 8, y0 + h - 16, "BAY OF BENGAL", font(SANS_B, 9),
         fill=(210, 225, 230), anchor="ra")
    # cyclone spiral, centred offshore
    cx, cy = x0 + int(w * 0.66), y0 + int(h * 0.52)
    gl = glow_layer()
    g = ImageDraw.Draw(gl)
    for ring in range(5):
        r0 = 12 + ring * 11
        a0 = ring * 55
        pts = []
        for a in range(a0, a0 + 300, 6):
            rr = r0 + (a - a0) * 0.045
            pts.append((cx + rr * math.cos(math.radians(a)),
                        cy + rr * math.sin(math.radians(a)) * 0.92))
        g.line(pts, fill=(255, 255, 255, 235), width=4 if ring < 2 else 3)
    g.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255, 240))
    paste_glow(gl, blur=2)
    # landfall dot + dashed track
    gx, gy = x0 + int(w * 0.47), y0 + int(h * 0.44)
    for i in range(8):
        t = i / 7
        px = cx + (gx - cx) * t
        py = cy + (gy - cy) * t
        if i % 2 == 0:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 90, 70))
    d.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=RED_BR, outline=(255, 255, 255), width=2)
    # rain bands
    for _ in range(26):
        rx = x0 + rnd.randint(int(w * 0.5), w - 8)
        ry = y0 + rnd.randint(6, h - 14)
        d.line([(rx, ry), (rx - 5, ry + 9)], fill=(255, 255, 255, 90), width=1)

def art_markets(x0, y0, w, h):
    """Dark market chart: grid, red falling line, candlesticks, index labels."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(10, 22, 38))
    for gy in range(1, 4):
        yy = y0 + h * gy / 4
        d.line([(x0 + 6, yy), (x0 + w - 6, yy)], fill=(255, 255, 255, 28), width=1)
    # candlesticks
    n = 9
    cw = (w - 24) / n
    vals = [0.86, 0.80, 0.82, 0.70, 0.66, 0.58, 0.52, 0.40, 0.30]
    for i, v in enumerate(vals):
        cx = x0 + 16 + i * cw + cw / 2
        top = y0 + 14 + (1 - v) * (h - 34)
        bh = (h - 40) * 0.16
        col = (210, 60, 50) if i % 3 else (90, 160, 110)
        d.rectangle([cx - 4, top, cx + 4, top + bh], fill=col)
        d.line([(cx, top - 5), (cx, top + bh + 5)], fill=col, width=1)
    # falling line with glow
    gl = glow_layer()
    g = ImageDraw.Draw(gl)
    pts = []
    for i, v in enumerate(vals):
        pts.append((x0 + 16 + i * cw + cw / 2, y0 + 14 + (1 - v) * (h - 34) + 6))
    g.line(pts, fill=(255, 80, 60, 230), width=4)
    paste_glow(gl, blur=3)
    d.line(pts, fill=(255, 120, 100), width=2)
    # arrow head
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 3), (ex - 5, ey + 9)], fill=(255, 120, 100))
    # index labels
    labels = [("TAIPEI", "-6.2%"), ("SEOUL", "-5.2%"), ("TOKYO", "-5.1%"), ("HONG KONG", "-1.9%")]
    ly = y0 + h - 52
    for name, v in labels:
        text(x0 + w - 10, ly, f"{name}   {v}", font(SANS_B, 11),
             fill=(255, 255, 255), anchor="ra")
        ly += 13

# ---------- leads row ----------
LEAD_H = 258
LEAD_ART_H = 142
leads = [
    ("KYIV", "1  KYIV, UKRAINE  ·  WAR", "Russia hits three Kyiv bridges\nin biggest barrage",
     "110+ missiles, 27 ballistic, and 400 drones overnight; 3 killed in Kyiv, 8 across "
     "Ukraine; power and water cut. (Zelensky · Kyiv Post)", "OFFICIAL", art_kyiv),
    ("CYCLONE AKVAN", "2  ODISHA, INDIA  ·  CYCLONE", "Cyclone Akvan makes landfall\nin eastern India",
     "Storm crosses near Gopalpur, Odisha, 07:30 IST; winds 70–80 km/h, gusts 90; 300,000+ "
     "moved to shelters; no deaths yet. (IMD · The Hindu)", "OFFICIAL", art_akvan),
    ("AI SELL-OFF", "3  TAIPEI · SEOUL · TOKYO  ·  MARKETS", "AI sell-off sinks Asia's\nstock markets",
     "Taiex -6.2%, its worst week since 1991; Kospi -5.2%, Nikkei -5.1%; SoftBank -16%; "
     "MSCI Asia's worst week since 2020. (Reuters)", "CONFIRMED", art_markets),
]
lx = M
lead_w = (CW - 16) // 3
for banner, kicker, head, deck, tag, art in leads:
    art(x0=lx, y0=y, w=lead_w, h=LEAD_ART_H)
    # banner on art
    bw = int(d.textlength(banner, font=font(SANS_B, 13))) + 16
    d.rectangle([lx, y + LEAD_ART_H - 24, lx + bw, y + LEAD_ART_H], fill=RED)
    text(lx + 8, y + LEAD_ART_H - 21, banner, font(SANS_B, 13), fill=(255, 255, 255))
    ty = y + LEAD_ART_H + 6
    text(lx, ty, kicker, font(SANS_B, 10), fill=RED)
    text(lx + lead_w, ty, tag, font(SANS_B, 9), fill=(255, 255, 255), anchor="ra")
    # tag chip behind
    tw = int(d.textlength(tag, font=font(SANS_B, 9))) + 10
    d.rectangle([lx + lead_w - tw, ty - 2, lx + lead_w, ty + 12], fill=(30, 90, 60))
    text(lx + lead_w - 5, ty, tag, font(SANS_B, 9), fill=(255, 255, 255), anchor="ra")
    ty += 15
    for ln in head.split("\n"):
        text(lx, ty, ln, font(SERIF_B, 19))
        ty += 22
    for ln in wrap(deck, font(SANS, 12), lead_w):
        text(lx, ty, ln, font(SANS, 12))
        ty += 15
    lx += lead_w + 8
y += LEAD_H + 6
hline(y, width=1)
y += 6

# ---------- small card art (196 x 58 mini-illustrations, bold silhouettes) ----------
def mini_flags_uk_eu(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 40, 80))
    # UK flag (left half)
    d.rectangle([x0 + 8, y0 + 10, x0 + w // 2 - 4, y0 + h - 10], fill=(200, 40, 50))
    d.rectangle([x0 + 8, y0 + 10, x0 + w // 2 - 4, y0 + h - 10], outline=(255, 255, 255), width=2)
    d.line([(x0 + 8, y0 + 10), (x0 + w // 2 - 4, y0 + h - 10)], fill=(255, 255, 255), width=2)
    d.line([(x0 + w // 2 - 4, y0 + 10), (x0 + 8, y0 + h - 10)], fill=(255, 255, 255), width=2)
    # EU flag (right half)
    d.rectangle([x0 + w // 2 + 4, y0 + 10, x0 + w - 8, y0 + h - 10], fill=(30, 60, 160))
    for k in range(8):
        a = k * math.pi / 4
        cx = x0 + w // 2 + 4 + (w // 2 - 12) / 2 + 26 * math.cos(a)
        cy = y0 + h // 2 + 12 * math.sin(a)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 220, 60))

def mini_cop31(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(12, 70, 80))
    cx, cy, r = x0 + 48, y0 + h // 2, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 170, 150))
    d.ellipse([cx - 12, cy - 8, cx - 2, cy + 2], fill=(30, 120, 100))
    d.ellipse([cx + 2, cy + 4, cx + 12, cy + 12], fill=(30, 120, 100))
    d.ellipse([cx - 4, cy - 16, cx + 8, cy - 8], fill=(30, 120, 100))
    # thermometer
    tx = x0 + w - 34
    d.rounded_rectangle([tx, y0 + 8, tx + 12, y0 + h - 8], radius=6, fill=(240, 240, 235))
    d.rectangle([tx + 3, y0 + 16, tx + 9, y0 + h - 16], fill=(220, 60, 50))
    d.ellipse([tx - 3, y0 + h - 20, tx + 15, y0 + h - 2], fill=(220, 60, 50))
    text(x0 + w - 44, y0 + 8, "+1.5°", font(SANS_B, 9), fill=(255, 255, 255), anchor="ra")

def mini_poland(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(150, 180, 120))
    d.polygon([(x0, y0 + h - 14), (x0 + w, y0 + h - 14), (x0 + w, y0 + h), (x0, y0 + h)],
              fill=(90, 130, 70))
    # missile lying in field
    mx, my = x0 + w // 2 - 30, y0 + h // 2 - 4
    d.polygon([(mx, my + 8), (mx + 62, my + 8), (mx + 72, my + 13), (mx + 62, my + 18),
               (mx, my + 18)], fill=(220, 220, 215))
    d.polygon([(mx + 62, my + 8), (mx + 72, my + 13), (mx + 62, my + 18)], fill=(180, 40, 30))
    d.ellipse([mx + 74, my + 8, mx + 84, my + 18], fill=(120, 120, 115))
    text(x0 + 8, y0 + 6, "KH-101", font(SANS_B, 10), fill=(40, 50, 30))

def mini_iraq(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(210, 180, 120))
    d.rectangle([x0, y0 + h - 18, x0 + w, y0 + h], fill=(160, 125, 70))
    for i, tx in enumerate([x0 + 14, x0 + 78, x0 + 142]):
        d.rectangle([tx, y0 + h - 34, tx + 46, y0 + h - 20], fill=(70, 80, 60))
        d.rectangle([tx + 10, y0 + h - 44, tx + 30, y0 + h - 34], fill=(70, 80, 60))
        d.ellipse([tx + 6, y0 + h - 20, tx + 14, y0 + h - 12], fill=(30, 30, 30))
        d.ellipse([tx + 32, y0 + h - 20, tx + 40, y0 + h - 12], fill=(30, 30, 30))
    d.ellipse([x0 + w - 26, y0 + 6, x0 + w - 8, y0 + 24], fill=(255, 220, 120))

def mini_italy(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 60, 100))
    # crowd: rows of heads + placards
    for row, yy in enumerate([y0 + h - 26, y0 + h - 14]):
        for i in range(7):
            hx = x0 + 12 + i * 26 + (row * 8)
            d.ellipse([hx, yy, hx + 12, yy + 12], fill=(240, 200, 160))
            d.rectangle([hx - 2, yy + 12, hx + 14, yy + 18], fill=(200, 60, 50) if i % 2 else (240, 240, 235))
    d.rectangle([x0 + 20, y0 + 6, x0 + 120, y0 + 20], fill=(255, 255, 255))
    text(x0 + 70, y0 + 8, "SCIOPERO", font(SANS_B, 10), fill=RED, anchor="ma")

def mini_japan(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(245, 240, 225))
    bars = [0.35, 0.5, 0.45, 0.62, 0.78, 0.95]
    bw = (w - 24) / len(bars)
    for i, v in enumerate(bars):
        bx = x0 + 12 + i * bw
        bh = v * (h - 18)
        d.rectangle([bx, y0 + h - 8 - bh, bx + bw - 4, y0 + h - 8],
                    fill=RED if i == len(bars) - 1 else (40, 60, 90))
    d.line([(x0 + 10, y0 + 10), (x0 + w - 10, y0 + h - 22)], fill=(220, 60, 50), width=2)
    text(x0 + w - 8, y0 + 4, "2.2%", font(SANS_B, 11), fill=RED, anchor="ra")

def mini_seoul(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(200, 210, 225))
    # parliament building
    d.rectangle([x0 + 30, y0 + 22, x0 + w - 30, y0 + h - 10], fill=(240, 240, 235))
    d.polygon([(x0 + 24, y0 + 22), (x0 + w - 24, y0 + 22), (x0 + w // 2, y0 + 6)],
              fill=(120, 40, 40))
    for i in range(6):
        cx = x0 + 42 + i * 20
        d.rectangle([cx, y0 + 30, cx + 8, y0 + h - 14], fill=(60, 80, 110))
    text(x0 + w - 8, y0 + 6, "VOTE", font(SANS_B, 10), fill=(120, 40, 40), anchor="ra")

def mini_kenya(x0, y0, w, h):
    vgrad(x0, y0, x0 + w, y0 + h, (250, 190, 90), (220, 130, 50))
    # oil derrick silhouette
    dx = x0 + w // 2
    d.polygon([(dx - 26, y0 + h - 8), (dx - 8, y0 + 10), (dx + 8, y0 + 10), (dx + 26, y0 + h - 8)],
              fill=(60, 40, 20))
    d.line([(dx - 18, y0 + h - 20), (dx + 18, y0 + h - 20)], fill=(60, 40, 20), width=2)
    d.line([(dx - 12, y0 + h - 34), (dx + 12, y0 + h - 34)], fill=(60, 40, 20), width=2)
    d.ellipse([x0 + 12, y0 + 8, x0 + 30, y0 + 26], fill=(255, 240, 180))

def mini_bukele(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(20, 80, 120))
    # ballot box + ballot
    d.rectangle([x0 + 60, y0 + 24, x0 + w - 60, y0 + h - 10], fill=(240, 240, 235))
    d.rectangle([x0 + 60, y0 + 24, x0 + w - 60, y0 + 34], fill=(180, 40, 40))
    d.rectangle([x0 + w // 2 - 16, y0 + 8, x0 + w // 2 + 16, y0 + 26], fill=(255, 255, 255),
                outline=(40, 40, 40))
    d.line([(x0 + w // 2 - 10, y0 + 17), (x0 + w // 2 - 2, y0 + 23), (x0 + w // 2 + 10, y0 + 10)],
           fill=RED, width=2)
    text(x0 + 10, y0 + 8, "3RD", font(SANS_B, 13), fill=(255, 255, 255))

def mini_phillips(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(30, 110, 60))
    # cricket bat + ball
    d.polygon([(x0 + 60, y0 + 8), (x0 + 78, y0 + 8), (x0 + 66, y0 + h - 12), (x0 + 48, y0 + h - 12)],
              fill=(230, 200, 140))
    d.rectangle([x0 + 62, y0 + h - 22, x0 + 72, y0 + h - 6], fill=(120, 80, 40))
    d.ellipse([x0 + w - 34, y0 + 12, x0 + w - 18, y0 + 28], fill=(200, 40, 40),
              outline=(255, 255, 255))
    text(x0 + 10, y0 + 6, "118", font(SANS_B, 15), fill=(255, 255, 255))

CARDS = [
    ("4  BRUSSELS  ·  DIPLOMACY", "UK and EU seal a \"reset\" deal",
     "Youth mobility, food trade and carbon link agreed at Friday's summit. (Reuters)",
     "OFFICIAL", mini_flags_uk_eu),
    ("5  ANTALYA  ·  CLIMATE", "COP31 reaches its last day with no deal",
     "Draft drops fossil fuels and the $120bn finance target; 21 issues open. (UN News)",
     "REPORTED", mini_cop31),
    ("6  EASTERN POLAND  ·  SECURITY", "Russian cruise missile lands in Poland",
     "KH-101 found in a field; two airports paused. (Reuters)", "OFFICIAL", mini_poland),
    ("7  CENTRAL IRAQ  ·  SECURITY", "Iraqi army enters a militia stronghold",
     "Troops deploy to Jurf al-Sakhar; deadline was Friday. (Reuters)", "REPORTED", mini_iraq),
    ("8  ROME  ·  LABOUR", "General strike over Italy's budget",
     "CGIL 24-hour stoppage; workers and students march. (ANSA)", "REPORTED", mini_italy),
    ("9  TOKYO  ·  ECONOMY", "Japan's inflation picks up to 2.2%",
     "Core CPI highest this year; BoJ December hike in view. (Reuters)", "OFFICIAL", mini_japan),
    ("10  SEOUL  ·  POLITICS", "Korea's ruling party to impeach top judge",
     "Move follows an overturned conviction. (Korea Herald)", "REPORTED", mini_seoul),
    ("11  TURKANA, KENYA  ·  ENERGY", "Kenya starts drilling its first oil well",
     "First crude due 1 December. (allAfrica)", "OFFICIAL", mini_kenya),
    ("12  SAN SALVADOR  ·  POLITICS", "Bukele files to run for a third term",
     "Vote is 28 February 2027. (AP)", "FILED", mini_bukele),
    ("13  WELLINGTON  ·  CRICKET", "Phillips hits 118 against India",
     "Hundreds in all three formats. (ICC)", "SCORE", mini_phillips),
]
CARD_ART_H = 58
CARD_H = 132
card_w = (CW - 24) // 5
for row in range(2):
    for col in range(5):
        kicker, head, deck, tag, art = CARDS[row * 5 + col]
        x0 = M + col * (card_w + 6)
        y0 = y + row * (CARD_H + 6)
        art(x0, y0, card_w, CARD_ART_H)
        ty = y0 + CARD_ART_H + 4
        text(x0, ty, kicker, font(SANS_B, 9), fill=RED)
        ty += 12
        for ln in wrap(head, font(SERIF_B, 12.5), card_w):
            text(x0, ty, ln, font(SERIF_B, 12.5))
            ty += 15
        for ln in wrap(deck, font(SANS, 10), card_w):
            text(x0, ty, ln, font(SANS, 10), fill=(60, 60, 60))
            ty += 12
        # status chip bottom-right of art
        tw = int(d.textlength(tag, font=font(SANS_B, 8))) + 8
        d.rectangle([x0 + card_w - tw, y0 + CARD_ART_H - 13, x0 + card_w, y0 + CARD_ART_H],
                    fill=(30, 90, 60))
        text(x0 + card_w - 4, y0 + CARD_ART_H - 12, tag, font(SANS_B, 8),
             fill=(255, 255, 255), anchor="ra")
y += 2 * CARD_H + 6
hline(y, width=1)
y += 6

# ---------- map + briefs ----------
MAP_W, MAP_H = 320, 146
CONTINENTS = {
    "NA": [(0.01, 0.30), (0.07, 0.12), (0.17, 0.07), (0.27, 0.14), (0.25, 0.26),
           (0.19, 0.34), (0.11, 0.42), (0.03, 0.34)],
    "SA": [(0.24, 0.50), (0.30, 0.47), (0.34, 0.56), (0.31, 0.72), (0.26, 0.70),
           (0.22, 0.56)],
    "EU": [(0.43, 0.15), (0.49, 0.09), (0.56, 0.13), (0.55, 0.23), (0.48, 0.26),
           (0.42, 0.21)],
    "AF": [(0.44, 0.36), (0.52, 0.34), (0.57, 0.42), (0.55, 0.56), (0.49, 0.61),
           (0.44, 0.48)],
    "AS": [(0.57, 0.09), (0.74, 0.05), (0.93, 0.11), (0.96, 0.23), (0.87, 0.32),
           (0.71, 0.30), (0.58, 0.23)],
    "OC": [(0.81, 0.64), (0.90, 0.61), (0.95, 0.67), (0.90, 0.74), (0.82, 0.71)],
}
# story -> map position (spread so Europe / East Asia pins do not collide)
PINS = {1: (0.52, 0.19), 2: (0.72, 0.29), 3: (0.49, 0.27), 4: (0.85, 0.25),
        5: (0.44, 0.16), 6: (0.54, 0.14), 7: (0.56, 0.31), 8: (0.45, 0.34),
        9: (0.91, 0.17), 10: (0.83, 0.19), 11: (0.51, 0.48), 12: (0.09, 0.38),
        13: (0.90, 0.68)}
map_x, map_y = M, y
text(map_x, map_y, "WHERE IT HAPPENED", font(SANS_B, 11), fill=RED)
text(map_x + MAP_W, map_y, "RED NUMBERS MARK STORIES 01–13", font(SANS, 8),
     fill=GREY, anchor="ra")
my = map_y + 16
d.rectangle([map_x, my, map_x + MAP_W, my + MAP_H], fill=NAVY)
for pts in CONTINENTS.values():
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    big = [(cx + (px - cx) * 1.35, cy + (py - cy) * 1.35) for px, py in pts]
    poly = [(map_x + px * MAP_W, my + py * MAP_H) for px, py in big]
    d.polygon(poly, fill=(58, 96, 130))
    d.line(poly + [poly[0]], fill=(120, 160, 190), width=1)
for n, (px, py) in PINS.items():
    cx, cy = map_x + px * MAP_W, my + py * MAP_H
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED_BR, outline=(255, 255, 255), width=1)
    d.text((cx, cy - 1), str(n), font=font(SANS_B, 7.5), fill=(255, 255, 255), anchor="mm")
text(map_x + 6, my + MAP_H - 12, "1 Kyiv  ·  2 Gopalpur  ·  3 Antalya  ·  4 Seoul  ·  5 Brussels",
     font(SANS, 8), fill=(200, 210, 220))

BRIEFS = [
    (14, "Lviv", "strike on a railway station kills two", "BBC"),
    (15, "Moscow", "Russia to shut its Estonia border crossing", "Reuters"),
    (16, "Berlin", "school pupils strike against military service", "Al Jazeera"),
    (17, "London", "UK runs cyber attacks abroad, general says", "Sky News"),
    (18, "Beijing", "China holds loan rates for an 18th month", "Xinhua"),
    (19, "Tokyo", "SoftBank shares fall more than 14% in a day", "Al Jazeera"),
    (20, "Seoul", "Kospi index ends the week 7.9% lower", "Anadolu"),
    (21, "Ganjam", "209 mm of rain falls as Akvan crosses Odisha", "PTI"),
    (22, "Lebanon", "Israeli air strikes hit the south and east", "Anadolu"),
    (23, "Yemen", "gunmen fire on a cargo ship off the coast", "UKMTO"),
    (24, "Abuja", "court bars new evidence against Tinubu", "Channels TV"),
    (25, "Kampala", "police told to enforce Ebola ban on rallies", "allAfrica"),
    (26, "Malawi", "fuel crisis brings night-long petrol queues", "Al Jazeera"),
    (27, "Africa", "AfDB says 22 countries in debt distress", "allAfrica"),
    (28, "Dakar", "four bodies found after migrant boat capsized", "AP"),
    (29, "New York", "Nasdaq futures fall 1.6% before the bell", "24/7 Wall St"),
    (30, "Washington", "Democrats query law firm's free work", "Al Jazeera"),
    (31, "Wellington", "Nicholls makes 175 in a 216-run stand", "ICC"),
    (32, "Sydney", "Australian shares fall 1.8% in the sell-off", "Reuters"),
    (33, "Antalya", "Panama asks COP31 to cap world oil output", "Anadolu"),
    (34, "Turin", "ATP backs a plan to lift player pay past $350m", "Anadolu"),
    (35, "Gaza", "Israeli troops cross the Yellow Line", "AP"),
    (36, "Sudan", "drone strike kills 10 at a gold mine", "Reuters"),
    (37, "Fiji", "drought emergency declared as El Niño bites", "RNZ"),
    (38, "Las Vegas", "Russell takes pole for Saturday's race", "AP"),
]
bx = map_x + MAP_W + 14
bw_col = (W - M - bx - 8) // 2
text(bx, map_y, "ALSO ON FRIDAY 20 NOVEMBER — 25 MORE STORIES", font(SANS_B, 11), fill=RED)
by = my
bf = font(SANS, 10)
for col in range(2):
    cx = bx + col * (bw_col + 8)
    yy = by
    for n, place, s, src in BRIEFS[col * 13:(col + 1) * 13]:
        d.text((cx, yy), str(n), font=font(SANS_B, 10), fill=RED)
        d.text((cx + 18, yy), f"{place}: {s} ", font=bf, fill=INK)
        tw = d.textlength(f"{place}: {s} ", font=bf)
        d.text((cx + 18 + tw, yy), f"({src})", font=bf, fill=GREY)
        yy += 11.5
y = my + MAP_H + 8
hline(y, width=1)
y += 5

# ---------- DATE CHECK + footer ----------
d.rectangle([M, y, W - M, y + 38], outline=RED, width=2)
text(M + 8, y + 4, "DATE CHECK", font(SANS_B, 10), fill=RED)
dc = ("Left out as Thursday 19 November news: the Trump–Xi–Putin summit itself · ICJ Myanmar "
      "Rohingya verdict · Anthropic's $83 IPO pricing & Nasdaq debut · GTA VI midnight launch · "
      "$190.4m Van Gogh sale · Senate 48–51 Iran war-powers vote · Houthi strike on Riyadh's PIF "
      "tower. Not yet known at press time: any COP31 outcome, Asia's closing prices.")
for i, ln in enumerate(wrap(dc, font(SANS, 9.5), CW - 110)):
    text(M + 92, y + 4 + i * 12, ln, font(SANS, 9.5))
y += 44
text(M, y, "Every story here happened, or was first reported, on Friday 20 November 2026. "
     "Claims are attributed, not stated as fact.",
     font(SANS_I, 9), fill=GREY)
text(W - M, y, "Sources named beside each story  ·  Original drawings",
     font(SANS, 9), fill=GREY, anchor="ra")

print("final y =", y, "canvas H =", H)
img.save("entry.png", optimize=True)
import os
print("entry.png bytes:", os.path.getsize("entry.png"))
