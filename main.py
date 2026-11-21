#!/usr/bin/env python3
"""news-image-20261120.

One image that sums up the world's news of Friday, 20 November 2026.
Python 3 standard library only. No network. Deterministic: every run writes
the same bytes. Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png),
a 1024x1024 PNG under 1 MiB.
"""
import os
import zlib
import struct
import random

W = H = 1024
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
SEED = 20261120
# Built by Hermes Agent in a recorded session for make.fun news-image-20261120.

NAVY_TOP = (11, 16, 38)
NAVY_MID = (24, 32, 64)
GROUND = (7, 9, 18)
SKY_LOW = (16, 14, 22)
GOLD = (232, 184, 109)
WHITE = (245, 246, 250)
GREY = (208, 214, 238)
DIM = (168, 175, 208)

FONT = {
    " ": ["....."] * 5,
    ".": [".....", ".....", ".....", ".....", "..#.."],
    ",": [".....", ".....", ".....", "..#..", ".#..."],
    ":": [".....", "..#..", ".....", "..#..", "....."],
    "-": [".....", ".....", "..#..", ".....", "....."],
    "'": [".....", ".#...", ".....", ".....", "....."],
    "&": [".###.", "#...#", ".##.#", "#.#.#", ".###."],
    "/": ["#....", "...#.", "..#..", ".#...", "#..."],
    "(": [".#...", "#....", "#....", "#....", ".#..."],
    ")": [".#...", "...#.", "...#.", "...#.", ".#..."],
    "·": [".....", ".....", "..#..", ".....", "....."],
    "0": [".###.", "#...#", "#.#.#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "#####"],
    "2": [".###.", "....#", ".###.", "#....", "#####"],
    "3": [".###.", "....#", ".###.", "....#", ".###."],
    "4": ["#...#", "#...#", "#####", "....#", "....#"],
    "5": ["#####", "#....", "####.", "....#", ".###."],
    "6": [".###.", "#....", "####.", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#..."],
    "8": [".###.", "#...#", ".###.", "#...#", ".###."],
    "9": [".###.", "#...#", "####.", "....#", ".###."],
    "A": [".###.", "#...#", "#####", "#...#", "#...#"],
    "B": ["####.", "#...#", "####.", "#...#", "####."],
    "C": [".###.", "#....", "#....", "#....", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "###..", "#....", "#####"],
    "F": ["#####", "#....", "###..", "#....", "#...."],
    "G": [".###.", "#....", "#.##.", "#...#", ".###."],
    "H": ["#...#", "#...#", "#####", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "#####"],
    "J": ["#...#", "#...#", "#...#", "#...#", ".###."],
    "K": ["#...#", "#..#.", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "####.", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#.#.#", ".##.#"],
    "R": ["####.", "#...#", "####.", "#..#.", "#...#"],
    "S": [".###.", "#....", ".###.", "....#", "###.."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#.#.#", "#.#.#", ".#.#."],
    "W": ["#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
    "X": ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", "#.#.#", "..#..", "..#..", "..#.."],
    "Z": ["#####", "...#.", "..#..", ".#...", "#####"],
    "?": ["#####", "#...#", "#####", "#...#", "#####"],
}

def glyph(ch):
    return FONT.get(ch.upper(), FONT["?"])

buf = bytearray(W * H * 3)


def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = c[0]
        buf[i + 1] = c[1]
        buf[i + 2] = c[2]


def blend(x, y, c, a):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = int(buf[i] * (1 - a) + c[0] * a)
        buf[i + 1] = int(buf[i + 1] * (1 - a) + c[1] * a)
        buf[i + 2] = int(buf[i + 2] * (1 - a) + c[2] * a)


def rect(x0, y0, x1, y1, c):
    for y in range(max(0, y0), min(H, y1)):
        row = y * W * 3
        for x in range(max(0, x0), min(W, x1)):
            i = row + x * 3
            buf[i] = c[0]
            buf[i + 1] = c[1]
            buf[i + 2] = c[2]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_char(x, y, ch, scale, color):
    g = glyph(ch)
    for gy, row in enumerate(g):
        for gx, cell in enumerate(row):
            if cell == "#":
                rect(x + gx * scale, y + gy * scale,
                     x + (gx + 1) * scale, y + (gy + 1) * scale, color)


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, color):
    cx = x
    for ch in s:
        draw_char(cx, y, ch, scale, color)
        cx += 6 * scale


def draw_text_centered(y, s, scale, color):
    draw_text((W - text_w(s, scale)) // 2, y, s, scale, color)


def wrap(s, scale, max_w):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def panel(x0, y0, x1, y1, fill, edge):
    rect(x0, y0, x1, y1, fill)
    rect(x0, y0, x1, y0 + 2, edge)


# Sky: dusk gradient down to the ground.
for y in range(H):
    if y < 640:
        t = y / 640.0
        c = lerp(NAVY_TOP, NAVY_MID, t)
    elif y < 700:
        t = (y - 640) / 60.0
        c = lerp(NAVY_MID, (60, 44, 32), t)
    else:
        t = (y - 700) / (H - 700)
        c = lerp(SKY_LOW, GROUND, t)
    rect(0, y, W, y + 1, c)

# Deterministic stars.
rng = random.Random(SEED)
for _ in range(520):
    x = rng.randrange(W)
    y = rng.randrange(0, 600)
    r = rng.random()
    if r < 0.04:
        continue
    a = 0.3 + 0.7 * r
    size = 2 if r > 0.94 else 1
    for dy in range(size):
        for dx in range(size):
            blend(x + dx, y + dy, WHITE, a)

# Moon with glow and craters.
MX, MY, MR = 910, 116, 40
for rr in range(MR + 40, MR, -2):
    a = max(0.0, 0.25 * (1 - (rr - MR) / 40.0))
    for yy in range(MY - rr, MY + rr + 1):
        dx2 = rr * rr - (yy - MY) ** 2
        if dx2 < 0:
            continue
        dx = int(dx2 ** 0.5)
        for xx in range(MX - dx, MX + dx + 1):
            blend(xx, yy, (245, 235, 210), a * 0.3)
for yy in range(MY - MR, MY + MR + 1):
    dx2 = MR * MR - (yy - MY) ** 2
    if dx2 < 0:
        continue
    dx = int(dx2 ** 0.5)
    for xx in range(MX - dx, MX + dx + 1):
        if 0 <= xx < W:
            d = ((xx - MX) ** 2 + (yy - MY) ** 2) / (MR * MR)
            c = lerp((248, 240, 214), (200, 192, 168), d)
            set_px(xx, yy, c)
for cx, cy, cr in ((844, 116, 7), (876, 140, 5), (856, 100, 4), (900, 128, 6)):
    for yy in range(cy - cr, cy + cr + 1):
        dx2 = cr * cr - (yy - cy) ** 2
        if dx2 < 0:
            continue
        dx = int(dx2 ** 0.5)
        for xx in range(cx - dx, cx + dx + 1):
            blend(xx, yy, (150, 144, 124), 0.55)

# Skyline silhouette above the horizon.
sky = random.Random(SEED ^ 0x5EED)
bx = 0
while bx < W:
    bw = sky.randrange(26, 80)
    bh = sky.randrange(44, 160)
    rect(bx, 650 - bh, min(W, bx + bw), 650, (5, 6, 13))
    for wy in range(650 - bh + 8, 646, 14):
        for wx in range(bx + 6, min(W, bx + bw) - 6, 12):
            if sky.random() < 0.14:
                set_px(wx, wy, GOLD)
    bx += bw + sky.randrange(4, 16)

rect(40, 650, W - 40, 652, (70, 60, 44))
rect(40, 648, 300, 654, GOLD)

# Masthead.
rect(0, 0, W, 7, GOLD)
draw_text(40, 24, "THE WORLD IN ONE IMAGE", 2, GOLD)
dw = text_w("20 NOVEMBER 2026 · FRIDAY", 2)
draw_text(W - dw - 40, 24, "20 NOVEMBER 2026 · FRIDAY", 2, GREY)
draw_text_centered(56, "20 NOVEMBER 2026 · FRIDAY", 3, WHITE)
rect(40, 98, W - 40, 100, (64, 56, 44))
rect(40, 96, 220, 102, GOLD)

# Hero.
draw_text(40, 116, "APEC SUMMIT · SHENZHEN", 2, GOLD)
hy = 144
for line in wrap("TRUMP, XI AND PUTIN MEET IN SHENZHEN", 4, W - 160):
    draw_text(40, hy, line, 4, WHITE)
    hy += 7 * 4 + 5
hy += 8
for line in wrap("First-ever US-China-Russia trilateral talks pledge a dialogue on nuclear risks; Trump presses Iran for a real deal and rules out an Iranian nuclear weapon", 2, W - 80):
    draw_text(40, hy, line, 2, GREY)
    hy += 7 * 2 + 4

# Story tiles (2 columns x 4 rows).
stories = [
    ("UKRAINE · WAR", "RUSSIA FIRES OVER 100 MISSILES AT UKRAINE; 8 KILLED, TWO MISSILES HIT POLAND", "CBS · DW · KYIV"),
    ("IRAN · SENATE", "US SENATE REJECTS WAR-POWER CURB ON TRUMP'S IRAN ATTACKS, 51-48", "DEMOCRACY NOW · AP"),
    ("THE HAGUE", "ICJ RULES MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA, A FIRST", "ICJ · ANADOLU"),
    ("COP31 · ANTALYA", "CLIMATE DRAFT DROPS FOSSIL-FUEL REFERENCES AS TURKIYE HOSTS", "DEMOCRACY NOW · REUTERS"),
    ("TECH · MARKETS", "ANTHROPIC IPO OPENS NEAR $100; TRUMP BARS US DATA CENTRES ABROAD", "NPR · AP · CNN"),
    ("CULTURE", "GRAND THEFT AUTO VI RELEASED GLOBALLY TO WIDESPREAD ACCLAIM", "ANADOLU · PLAYERS"),
    ("BERLIN · TOKYO", "STUDENTS PROTEST GERMAN REARMAMENT; JAPANESE RALLY AGAINST CHARTER REVISION", "EURONEWS · XINHUA"),
    ("HORN OF AFRICA", "SOMALIA ORDERS UAE AMBASSADOR OUT IN 72 HOURS", "WORLD WATCH · REUTERS"),
]
col_w = (W - 40 - 32) // 2
tile_h = 76
gap = 6
start_y = 660
for idx, (kicker, headline, source) in enumerate(stories):
    col = idx % 2
    row = idx // 2
    x0 = 40 + col * (col_w + 32)
    y0 = start_y + row * (tile_h + gap)
    fill = (24, 29, 56) if row % 2 == 0 else (27, 32, 61)
    panel(x0, y0, x0 + col_w, y0 + tile_h, fill, GOLD)
    draw_text(x0 + 16, y0 + 10, kicker, 1, GOLD)
    ty = y0 + 22
    for line in wrap(headline, 2, col_w - 34):
        draw_text(x0 + 16, ty, line, 2, WHITE)
        ty += 18
    draw_text(x0 + 16, y0 + tile_h - 14, source, 1, GREY)

# Footer.
rect(0, H - 26, W, H, (5, 6, 12))
draw_text_centered(H - 18, "SOURCES: REUTERS · AP · ICJ · XINHUA · DEMOCRACY NOW · EURONEWS · DW · ANADOLU · NPR · MAKE.FUN", 1, GREY)

# PNG encode.
raw = b"".join(b"\x00" + bytes(buf[y * W * 3:(y + 1) * W * 3]) for y in range(H))
comp = zlib.compress(raw, 9)


def chunk(tag, data):
    c = struct.pack(">I", len(data)) + tag + data
    return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
       + chunk(b"IDAT", comp)
       + chunk(b"IEND", b""))
try:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
except OSError:
    pass
with open(OUT, "wb") as f:
    f.write(png)
print("wrote", OUT, len(png), "bytes")
