#!/usr/bin/env python3
# news-image-20261120: satu gambar yang merangkum berita dunia Jumat, 20 November 2026.
# Python 3 standar saja, tanpa jaringan, deterministik (tiap run tulis byte yang sama).
# Tulis $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png): PNG 1024x1024, < 1 MiB.
import os
import zlib
import struct
import random

W, H = 1024, 1024
# Dibangun oleh Hermes Agent (sesi direkam) untuk make.fun news-image-20261120.
DEST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

NAVY = (11, 16, 38)
MID = (24, 32, 64)
GLOW = (60, 44, 32)
GROUND = (7, 9, 18)
GOLD = (232, 184, 109)
WHITE = (245, 246, 250)
GREY = (208, 214, 238)

F = {
    " ": [0, 0, 0, 0, 0],
    ".": [0, 0, 0, 0, 4],
    ",": [0, 0, 0, 4, 2],
    ":": [0, 4, 0, 4, 0],
    "-": [0, 0, 4, 0, 0],
    "'": [0, 8, 0, 0, 0],
    "&": [14, 17, 13, 21, 14],
    "/": [16, 1, 4, 8, 17],
    "(": [8, 16, 16, 16, 8],
    ")": [8, 1, 1, 1, 8],
    "·": [0, 0, 4, 0, 0],
    "0": [14, 17, 21, 17, 14],
    "1": [4, 12, 4, 4, 31],
    "2": [14, 1, 14, 16, 31],
    "3": [14, 1, 14, 1, 14],
    "4": [17, 17, 31, 1, 1],
    "5": [31, 16, 30, 1, 14],
    "6": [14, 16, 30, 17, 14],
    "7": [31, 1, 2, 4, 8],
    "8": [14, 17, 14, 17, 14],
    "9": [14, 17, 30, 1, 14],
    "A": [14, 17, 31, 17, 17],
    "B": [30, 17, 30, 17, 30],
    "C": [14, 16, 16, 16, 14],
    "D": [30, 17, 17, 17, 30],
    "E": [31, 16, 28, 16, 31],
    "F": [31, 16, 28, 16, 16],
    "G": [14, 16, 22, 17, 14],
    "H": [17, 17, 31, 17, 17],
    "I": [31, 4, 4, 4, 31],
    "J": [17, 17, 17, 17, 14],
    "K": [17, 18, 20, 18, 17],
    "L": [16, 16, 16, 16, 31],
    "M": [17, 27, 21, 17, 17],
    "N": [17, 25, 21, 19, 17],
    "O": [14, 17, 17, 17, 14],
    "P": [30, 17, 30, 16, 16],
    "Q": [14, 17, 17, 21, 13],
    "R": [30, 17, 30, 20, 17],
    "S": [14, 16, 14, 1, 28],
    "T": [31, 4, 4, 4, 4],
    "U": [17, 17, 17, 17, 14],
    "V": [17, 17, 21, 21, 10],
    "W": [17, 17, 21, 21, 21],
    "X": [17, 10, 4, 10, 17],
    "Y": [17, 21, 4, 4, 4],
    "Z": [31, 1, 2, 4, 31],
    "?": [31, 17, 31, 17, 17],
}

buf = bytearray(W * H * 3)


def p(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = c[0]
        buf[i + 1] = c[1]
        buf[i + 2] = c[2]


def m(x, y, c, a):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = int(buf[i] * (1 - a) + c[0] * a)
        buf[i + 1] = int(buf[i + 1] * (1 - a) + c[1] * a)
        buf[i + 2] = int(buf[i + 2] * (1 - a) + c[2] * a)


def r(x0, y0, x1, y1, c):
    for y in range(max(0, y0), min(H, y1)):
        row = y * W * 3
        for x in range(max(0, x0), min(W, x1)):
            i = row + x * 3
            buf[i] = c[0]
            buf[i + 1] = c[1]
            buf[i + 2] = c[2]


def mix(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))


def ch(x, y, s, scale, color):
    rows = F.get(s.upper(), F["?"])
    bit = 16
    for gy in range(5):
        for gx in range(5):
            if rows[gy] & bit:
                r(x + gx * scale, y + gy * scale, x + (gx + 1) * scale,
                  y + (gy + 1) * scale, color)
            bit >>= 1


def tw(s, scale):
    return len(s) * 6 * scale - scale


def tx(x, y, s, scale, color):
    cx = x
    for s_ in s:
        ch(cx, y, s_, scale, color)
        cx += 6 * scale


def txc(y, s, scale, color):
    tx((W - tw(s, scale)) // 2, y, s, scale, color)


def wrap(s, scale, max_w):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def pan(x0, y0, x1, y1, fill, edge):
    r(x0, y0, x1, y1, fill)
    r(x0, y0, x1, y0 + 2, edge)

# Langit: gradien senja dari atas ke tanah.
for y in range(H):
    if y < 500:
        t = y / 500.0
        c = mix(NAVY, MID, t)
    elif y < 560:
        t = (y - 500) / 60.0
        c = mix(MID, GLOW, t)
    else:
        t = (y - 560) / (H - 560)
        c = mix((16, 14, 22), GROUND, t)
    r(0, y, W, y + 1, c)

# Bintang (deterministik).
rn = random.Random(20261120)
for _ in range(600):
    x = rn.randrange(W)
    y = rn.randrange(0, 570)
    a = rn.random()
    if a < 0.05:
        continue
    m(x, y, WHITE, 0.35 + 0.65 * a)

# Garis summit dan kota di atas horizonte.
sky = random.Random(20261120 ^ 0x5EED)
gx = 0
while gx < W:
    gw = sky.randrange(28, 84)
    gh = sky.randrange(40, 150)
    r(gx, 560 - gh, min(W, gx + gw), 560, (4, 5, 11))
    for wy in range(560 - gh + 6, 556, 12):
        for wx in range(gx + 6, min(W, gx + gw) - 6, 12):
            if sky.random() < 0.12:
                p(wx, wy, GOLD)
    gx += gw + sky.randrange(4, 16)

r(42, 560, W - 42, 562, (70, 60, 44))
r(42, 558, 300, 564, GOLD)

# Kopak.
r(0, 0, W, 8, GOLD)
tx(42, 26, "THE WORLD IN ONE IMAGE", 2, GOLD)
dw = tw("20 NOVEMBER 2026 · JUMAT", 2)
tx(W - dw - 42, 26, "20 NOVEMBER 2026 · JUMAT", 2, GREY)
txc(60, "20 NOVEMBER 2026 · JUMAT", 3, WHITE)
r(42, 104, W - 42, 106, (64, 56, 44))
r(42, 102, 240, 108, GOLD)

# Berita utama.
tx(42, 124, "SUMMIT DI SHENZHEN · APEC", 2, GOLD)
hy = 150
for line in wrap("TRUMP, XI DAN PUTIN BERTEMU DI SHENZHEN", 4, W - 160):
    tx(42, hy, line, 4, WHITE)
    hy += 7 * 4 + 5
hy += 8
for line in wrap("Pertemuan trilateral AS-China-Rusia pertama janjikan dialog risiko nuklir; Trump mendorong Iran untuk deal nyata dan menolak senjata nuklir Iran", 2, W - 80):
    tx(42, hy, line, 2, GREY)
    hy += 7 * 2 + 4

# Berita lain: 2 kolom x 3 baris.
stories = [
    ("PERANG UKRAINA", "RUSIA SERANG LEBIH DARI 100 ROKET; 8 TEWAS, DUA ROKET JATUH DI POLANDIA", "CBS · DW · KYIV"),
    ("SENAT AS", "SENAT AS TOLAK BATASAN KUASA PERANG IRAN 51-48", "DEMOCRACY NOW · AP"),
    ("THE HAGUE", "ICJ RULES MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA, A FIRST", "ICJ · ANADOLU"),
    ("COP31 ANTALYA", "DRAFT IKLIM HILANGKAN REFERENSI BAHAN BAKAR FOSIL", "DEMOCRACY NOW · REUTERS"),
    ("TEKNOLOGI", "ANTHROPIC IPO DI SEKITAR $100; TRUMP LARANG DATA CENTER AS DI LUAR NEGERI", "NPR · AP · CNN"),
    ("GAME", "GRAND THEFT AUTO VI DIRILIS GLOBAL, PUIJAN LUAS", "ANADOLU · PLAYERS"),
]
cw = (W - 42 - 32) // 2
th = 92
gap = 10
sy = 560
for i, (kicker, headline, source) in enumerate(stories):
    col = i % 2
    row = i // 2
    x0 = 42 + col * (cw + 32)
    y0 = sy + row * (th + gap)
    fill = (24, 29, 56) if row % 2 == 0 else (27, 32, 61)
    pan(x0, y0, x0 + cw, y0 + th, fill, GOLD)
    tx(x0 + 16, y0 + 10, kicker, 1, GOLD)
    ty = y0 + 24
    for line in wrap(headline, 2, cw - 34):
        tx(x0 + 16, ty, line, 2, WHITE)
        ty += 18
    tx(x0 + 16, y0 + th - 14, source, 1, GREY)

# Kaki halaman.
r(0, 990, W, H, (5, 6, 12))
# 20 November 2026: deterministik, tanpa jaringan, standar library saja.
txc(1002, "SUMBER: REUTERS · AP · ICJ · XINHUA · DEMOCRACY NOW · EURONEWS · DW · ANADOLU · NPR · MAKE.FUN", 1, GREY)

# Encode PNG.
rows = []
for y in range(H):
    rows.append(bytes([0]) + bytes(buf[y * W * 3:(y + 1) * W * 3]))
dat = zlib.compress(b"".join(rows), 9)


def chk(tag, data):
    head = struct.pack(">I", len(data))
    body = head + tag + data
    return body + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


hdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
png = b"\x89PNG\r\n\x1a\n" + chk(b"IHDR", hdr) + chk(b"IDAT", dat) + chk(b"IEND", b"")
if not os.path.exists(os.path.dirname(DEST)):
    os.makedirs(os.path.dirname(DEST))
with open(DEST, "wb") as f:
    f.write(png)
print("wrote", DEST, len(png), "bytes")
