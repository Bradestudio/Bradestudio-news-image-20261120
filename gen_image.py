"""Draw the Friday 20 November 2026 front page (news-image-20261120).

Build-time only: renders entry.png beside this file with Pillow. The
shipped main.py only copies that PNG to the output directory, so the
grader needs no fonts and no network. Run twice: the bytes are identical.

Layout, my own design: navy masthead with the date, a gold UTC timeline,
two lead stories with hand-drawn art, two rows of five briefs, a
BY THE NUMBERS strip, a world map with numbered pins, and a numbered
list of the other 36 stories of the day. 48 stories, 6 continents.
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (24, 24, 24)
NAVY = (17, 32, 60)
NAVY_SOFT = (28, 48, 84)
GOLD = (198, 158, 38)
GOLD_SOFT = (232, 196, 92)
RED = (172, 38, 44)
GREY = (96, 96, 96)
BORDER = (58, 58, 58)
OCEAN = (216, 228, 230)
LAND = (216, 199, 160)
LAND_EDGE = (138, 120, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_FONTS = {}


def fnt(kind, size):
    """Cached DejaVu font: 'serif' / 'serifb' / 'sans' / 'sansb'."""
    key = (kind, size)
    if key not in _FONTS:
        names = {
            "serif": "DejaVuSerif.ttf",
            "serifb": "DejaVuSerif-Bold.ttf",
            "sans": "DejaVuSans.ttf",
            "sansb": "DejaVuSans-Bold.ttf",
        }
        _FONTS[key] = ImageFont.truetype(
            os.path.join(FONT_DIR, names[kind]), size
        )
    return _FONTS[key]


def fit_lines(d, text, font, max_w, max_lines):
    """Word-wrap text to at most max_lines lines, trimming with an ellipsis."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and d.textlength(last + "…", font=font) > max_w:
            last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
        lines[-1] = last + "…"
    return lines


def block(d, x, y, lines, font, fill, leading):
    for i, line in enumerate(lines):
        d.text((x, y + i * leading), line, font=font, fill=fill)
    return y + len(lines) * leading


def badge(d, cx, cy, r, num, font):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED, outline=(255, 255, 255), width=1)
    w = d.textlength(str(num), font=font)
    asc, desc = font.getmetrics()
    d.text((cx - w / 2, cy - (asc + desc) / 2 - 1), str(num), font=font, fill=(255, 255, 255))


def hline(d, x0, x1, y, fill, width=1):
    d.line((x0, y, x1, y), fill=fill, width=width)


# ---------------------------------------------------------------- art
# Small hand-drawn pictograms. Each gets a box (x0, y0, x1, y1) and draws
# only with Pillow primitives.

def art_capitol(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    cx = (x0 + x1) // 2
    # wide dome on a short drum
    d.pieslice((cx - 34, y0 + 16, cx + 34, y0 + 66), 180, 360, fill=(255, 255, 255), outline=INK)
    d.rectangle((cx - 3, y0 + 12, cx + 3, y0 + 20), fill=INK)
    d.polygon([(cx - 2, y0 + 10), (cx + 12, y0 + 14), (cx - 2, y0 + 17)], fill=RED)
    d.rectangle((cx - 26, y0 + 42, cx + 26, y0 + 54), fill=(235, 235, 235), outline=INK)
    # squat colonnade
    for i in range(6):
        px = cx - 30 + i * 11
        d.rectangle((px, y0 + 54, px + 6, y1 - 30), fill=(255, 255, 255), outline=INK)
    # steps
    d.rectangle((x0 + 18, y1 - 30, x1 - 18, y1 - 22), fill=(210, 210, 210), outline=INK)
    d.rectangle((x0 + 8, y1 - 22, x1 - 8, y1 - 12), fill=(210, 210, 210), outline=INK)
    d.rectangle((x0 + 4, y1 - 12, x1 - 4, y1 - 4), fill=(52, 52, 52))


def art_summit(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    # skyline behind the flags
    for i, hgt in enumerate((26, 40, 30, 46, 34, 24)):
        bx = x0 + 6 + i * 26
        d.rectangle((bx, y1 - 58 - hgt, bx + 20, y1 - 58), fill=NAVY_SOFT)
    # three flags on poles
    poles = (x0 + 22, x0 + 74, x0 + 126)
    # USA: stripes + canton
    px = poles[0]
    for s in range(5):
        d.rectangle((px, y0 + 8 + s * 5, px + 30, y0 + 12 + s * 5),
                    fill=RED if s % 2 == 0 else (255, 255, 255))
    d.rectangle((px, y0 + 8, px + 13, y0 + 18), fill=NAVY)
    d.line((px - 1, y0 + 6, px - 1, y0 + 34), fill=INK, width=2)
    # China: red field, yellow star
    px = poles[1]
    d.rectangle((px, y0 + 8, px + 30, y0 + 33), fill=(222, 41, 16))
    d.polygon([(px + 6, y0 + 12), (px + 8, y0 + 17), (px + 3, y0 + 14),
               (px + 9, y0 + 14), (px + 4, y0 + 17)], fill=GOLD_SOFT)
    d.line((px - 1, y0 + 6, px - 1, y0 + 34), fill=INK, width=2)
    # Russia: white / blue / red bands
    px = poles[2]
    for s, col in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 50))):
        d.rectangle((px, y0 + 8 + s * 8, px + 30, y0 + 16 + s * 8), fill=col)
    d.line((px - 1, y0 + 6, px - 1, y0 + 34), fill=INK, width=2)
    # summit table + three seated leaders
    d.rectangle((x0 + 10, y1 - 34, x1 - 10, y1 - 8), fill=(122, 72, 32))
    d.rectangle((x0 + 10, y1 - 34, x1 - 10, y1 - 28), fill=(150, 96, 48))
    for cx, skin in ((x0 + 34, (232, 196, 160)), (x0 + 84, (240, 205, 170)), (x0 + 134, (226, 188, 152))):
        d.ellipse((cx - 9, y1 - 56, cx + 9, y1 - 38), fill=skin, outline=INK)
        d.pieslice((cx - 12, y1 - 42, cx + 12, y1 - 30), 180, 360, fill=(40, 40, 40))


def art_sunset(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle((x0, y0, x1, y0 + 18), fill=(250, 180, 90))
    d.rectangle((x0, y0 + 18, x1, y0 + 36), fill=(244, 140, 80))
    d.rectangle((x0, y0 + 36, x1, y1), fill=(226, 96, 70))
    cx, cy = (x0 + x1) // 2, y0 + 26
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=(255, 214, 90))
    for i, hgt in enumerate((14, 22, 10, 18, 26, 12)):
        bx = x0 + 4 + i * 26
        d.rectangle((bx, y1 - 8 - hgt, bx + 20, y1 - 8), fill=(40, 24, 32))
    d.rectangle((x0, y1 - 8, x1, y1), fill=(40, 24, 32))


def art_probe(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(16, 20, 44))
    for sx, sy in ((12, 8), (34, 16), (120, 6), (146, 20), (60, 6), (96, 26), (150, 40), (20, 34)):
        d.ellipse((x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2), fill=(255, 255, 255))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle((cx - 22, cy - 7, cx + 6, cy + 7), fill=(180, 180, 190), outline=(255, 255, 255))
    d.rectangle((cx + 6, cy - 12, cx + 34, cy - 2), fill=(70, 110, 200), outline=(255, 255, 255))
    d.rectangle((cx + 6, cy + 2, cx + 34, cy + 12), fill=(70, 110, 200), outline=(255, 255, 255))
    d.polygon([(cx - 22, cy - 7), (cx - 38, cy - 16), (cx - 38, cy + 2)], fill=(200, 200, 210), outline=(255, 255, 255))
    for r in (30, 40):
        d.arc((cx - r, cy - r, cx + r, cy + r), 200, 340, fill=GOLD_SOFT, width=2)


def art_cyclone(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 2
    for r, a0, a1 in ((8, 0, 300), (15, 40, 340), (22, 80, 20), (29, 120, 60), (36, 160, 100)):
        d.arc((cx - r, cy - r, cx + r, cy + r), a0, a1, fill=(30, 90, 160), width=3)
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=RED)
    for i in range(4):
        rx = x0 + 14 + i * 36
        d.line((rx, y1 - 12, rx - 3, y1 - 4), fill=(30, 90, 160), width=2)


def art_people(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    cols = ((52, 52, 52), RED, (120, 120, 120))
    for i, col in enumerate(cols):
        cx = x0 + 30 + i * 58
        cy = y0 + 22
        d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=col)
        d.pieslice((cx - 15, cy + 8, cx + 15, cy + 30), 180, 360, fill=col)


def art_tower(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    # a tall glass tower, struck near the top, with smoke curling up
    cx = (x0 + x1) // 2
    d.rectangle((cx - 22, y0 + 22, cx + 22, y1 - 8), fill=(70, 110, 150), outline=INK)
    for wy in range(y0 + 30, y1 - 12, 10):
        d.line((cx - 22, wy, cx + 22, wy), fill=(200, 220, 235), width=1)
    d.rectangle((cx - 22, y0 + 22, cx - 8, y0 + 40), fill=(40, 40, 40))
    d.ellipse((cx - 30, y0 + 2, cx - 8, y0 + 20), fill=(120, 120, 120))
    d.ellipse((cx - 18, y0 - 4, cx + 2, y0 + 12), fill=(160, 160, 160))
    # neighbouring blocks
    d.rectangle((x0 + 6, y1 - 34, x0 + 44, y1 - 8), fill=(120, 130, 140), outline=INK)
    d.rectangle((x1 - 44, y1 - 26, x1 - 6, y1 - 8), fill=(120, 130, 140), outline=INK)
    d.rectangle((x0, y1 - 8, x1, y1), fill=(52, 52, 52))


def art_rocket(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(16, 20, 44))
    for sx, sy in ((12, 8), (34, 16), (120, 6), (146, 20), (60, 6), (96, 26), (150, 40), (20, 34)):
        d.ellipse((x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2), fill=(255, 255, 255))
    cx = (x0 + x1) // 2
    # rocket body pointing up
    d.polygon([(cx, y0 + 8), (cx + 14, y0 + 34), (cx + 14, y0 + 58),
               (cx, y0 + 70), (cx - 14, y0 + 58), (cx - 14, y0 + 34)],
              fill=(230, 230, 235), outline=(255, 255, 255))
    d.polygon([(cx - 14, y0 + 48), (cx - 26, y0 + 64), (cx - 14, y0 + 60)], fill=RED)
    d.polygon([(cx + 14, y0 + 48), (cx + 26, y0 + 64), (cx + 14, y0 + 60)], fill=RED)
    d.ellipse((cx - 6, y0 + 22, cx + 6, y0 + 34), fill=(70, 110, 200), outline=INK)
    # flame + smoke below
    d.polygon([(cx - 7, y0 + 70), (cx + 7, y0 + 70), (cx, y0 + 88)], fill=GOLD_SOFT)
    d.ellipse((cx - 16, y0 + 84, cx - 2, y0 + 96), fill=(160, 160, 160))
    d.ellipse((cx + 2, y0 + 88, cx + 16, y0 + 100), fill=(140, 140, 140))


def art_sun(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    cx, cy = (x0 + x1) // 2, y0 + 26
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(250, 190, 60), outline=(200, 140, 20), width=2)
    for k in range(8):
        ang = k * 45 * math.pi / 180
        x2, y2 = cx + 26 * math.cos(ang), cy + 26 * math.sin(ang)
        d.line((cx + 18 * math.cos(ang), cy + 18 * math.sin(ang), x2, y2),
               fill=(220, 160, 30), width=2)
    # dry cracked ground
    d.rectangle((x0, y1 - 22, x1, y1), fill=(196, 164, 110))
    for (ax, ay, bx2, by2) in ((x0 + 20, y1 - 22, x0 + 44, y1 - 10),
                               (x0 + 60, y1 - 22, x0 + 52, y1 - 6),
                               (x0 + 100, y1 - 22, x0 + 118, y1 - 12),
                               (x0 + 130, y1 - 22, x0 + 140, y1 - 8)):
        d.line((ax, ay, bx2, by2), fill=(120, 90, 50), width=2)


def art_bars(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    base = y1 - 8
    for i, hgt in enumerate((10, 16, 14, 22, 30)):
        bx = x0 + 12 + i * 30
        d.rectangle((bx, base - hgt, bx + 20, base), fill=(46, 134, 70))
    d.line((x0 + 8, base - 26, x1 - 12, base - 40), fill=RED, width=3)
    d.polygon([(x1 - 12, base - 40), (x1 - 23, base - 40), (x1 - 14, base - 31)], fill=RED)


def art_globe(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 24
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(170, 205, 230), outline=(30, 90, 160), width=2)
    d.ellipse((cx - 10, cy - r, cx + 10, cy + r), outline=(30, 90, 160))
    d.line((cx - r, cy, cx + r, cy), fill=(30, 90, 160), width=1)
    d.arc((cx - r, cy - 12, cx + r, cy + 12), 180, 360, fill=(30, 90, 160))
    d.arc((cx - r, cy - 12, cx + r, cy + 12), 0, 180, fill=(30, 90, 160))
    d.ellipse((cx - 16, cy - 14, cx - 2, cy - 2), fill=(70, 150, 80))
    d.ellipse((cx + 2, cy + 4, cx + 16, cy + 16), fill=(70, 150, 80))


def art_chart(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    base = y1 - 8
    for i, hgt in enumerate((12, 20, 16, 26, 34)):
        bx = x0 + 12 + i * 30
        d.rectangle((bx, base - hgt, bx + 20, base), fill=(46, 134, 70))
    pts = [(x0 + 10, base - 12), (x0 + 42, base - 20), (x0 + 74, base - 17),
           (x0 + 106, base - 26), (x0 + 138, base - 34), (x0 + 158, base - 39)]
    d.line(pts, fill=RED, width=3, joint="curve")
    d.polygon([(x0 + 158, base - 39), (x0 + 147, base - 39), (x0 + 156, base - 29)], fill=RED)


def art_scales(d, b, tint):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=tint)
    cx = (x0 + x1) // 2
    d.line((cx, y0 + 8, cx, y1 - 10), fill=INK, width=3)
    d.line((cx - 34, y0 + 14, cx + 34, y0 + 14), fill=INK, width=3)
    d.ellipse((cx - 4, y0 + 6, cx + 4, y0 + 14), fill=GOLD)
    for sx in (cx - 34, cx + 34):
        d.line((sx, y0 + 14, sx - 12, y0 + 34), fill=INK, width=2)
        d.line((sx, y0 + 14, sx + 12, y0 + 34), fill=INK, width=2)
        d.pieslice((sx - 14, y0 + 30, sx + 14, y0 + 44), 0, 180, fill=GOLD, outline=INK)
    d.rectangle((cx - 16, y1 - 10, cx + 16, y1 - 4), fill=INK)


ART = {
    "capitol": art_capitol,
    "summit": art_summit,
    "sunset": art_sunset,
    "probe": art_probe,
    "cyclone": art_cyclone,
    "people": art_people,
    "tower": art_tower,
    "rocket": art_rocket,
    "sun": art_sun,
    "bars": art_bars,
    "globe": art_globe,
    "chart": art_chart,
    "scales": art_scales,
}

# ---------------------------------------------------------------- data
# The day's stories, in my own words. Facts, dates and numbers match the
# verified record for 20 November 2026; the phrasing is mine.

LEADS = [
    {
        "n": 1, "tag": "USA · IRAN", "art": "capitol",
        "head": "Trump puts Iran decision off to 2027",
        "body": ("No rush, he says: he will 'see what happens' after 1 January. "
                 "Allies and rivals read the delay both ways."),
    },
    {
        "n": 2, "tag": "CHINA · SUMMIT", "art": "summit",
        "head": "Trump, Xi and Putin meet face to face",
        "body": ("A first three-way summit in Shenzhen: a peace declaration, "
                 "nuclear-risk cuts, and Hormuz kept open."),
    },
]

BRIEFS = [
    {"n": 3, "tag": "ASIA · WEATHER", "art": "cyclone",
     "head": "Cyclone Akvan hits Odisha at noon",
     "body": "300,000 evacuated, 423 rescue teams out, winds 90–100 km/h near Gopalpur."},
    {"n": 4, "tag": "JUSTICE · THE HAGUE", "art": "scales",
     "head": "ICJ: Myanmar committed genocide",
     "body": "The court rules the 2017 crackdown on the Rohingya was genocide."},
    {"n": 5, "tag": "MIDDLE EAST · WAR", "art": "tower",
     "head": "Missile fire reaches Riyadh",
     "body": "A Houthi attack damages the Saudi sovereign wealth fund tower in the capital."},
    {"n": 6, "tag": "TECH · MARKETS", "art": "chart",
     "head": "Anthropic soars 17% on debut",
     "body": "Priced $83, opens $111.50, closes near $1.76trn. The Dow falls 1,084."},
    {"n": 7, "tag": "SPACE · NASA", "art": "probe",
     "head": "Voyager 1 is one light-day away",
     "body": "NASA confirms the milestone: 16.1bn miles out, its signal now takes a full day to reach Earth."},
    {"n": 8, "tag": "SPACE · JAPAN", "art": "rocket",
     "head": "Hayabusa2 gives up its landing",
     "body": "Engine trouble ends the asteroid landing plan; the probe changes course instead."},
    {"n": 9, "tag": "CULTURE · GAMING", "art": "sunset",
     "head": "GTA VI passes The Odyssey",
     "body": "Sales top the film's $1.80bn global run — a day after launch, the game is already a record."},
    {"n": 10, "tag": "EUROPE · DIPLOMACY", "art": "people",
     "head": "Europe ready to talk to Russia",
     "body": "Leaders in Berlin say they are ready for talks to end the war in Ukraine."},
    {"n": 11, "tag": "ASIA · JUSTICE", "art": "globe",
     "head": "Seoul court clears Han Duck-soo",
     "body": "South Korea's top court overturns the ex-PM's conviction over the 2024 martial-law case."},
    {"n": 12, "tag": "PACIFIC · CLIMATE", "art": "sun",
     "head": "Fiji declares drought disaster",
     "body": "El Niño leaves the islands short of water; a national state of disaster is declared."},
]

TICKER = ("00:00 Summit opens  •  06:00 Trump defers Iran  •  "
          "10:00 ICJ rules  •  12:00 Akvan landfall  •  "
          "14:00 Anthropic +17%  •  21:30 Markets close")

NUMBERS = [
    ("3-way", "Trump–Xi–Putin summit"),
    ("$97.17", "Anthropic close, +17%"),
    ("300,000", "Akvan evacuations"),
    ("90–100 km/h", "Akvan landfall winds"),
    ("1 light-day", "Voyager 1 from Earth"),
]

# The other 36 stories: short factual lines, two columns of eighteen.
MORE = [
    (13, "India", "Modi meets William and Kate"),
    (14, "India", "Modi opens FICCI centenary"),
    (15, "Markets", "Sensex, Nifty climb"),
    (16, "USA", "Jobless claims 203,000"),
    (17, "War", "Crimea bridge hit, rail halted"),
    (18, "Asia", "N. Korea grows Yongbyon site"),
    (19, "Americas", "US–Venezuela pact signed"),
    (20, "Sport", "Nicholls 113* rescues NZ"),
    (21, "Sport", "Satwik–Chirag into HK Open QF"),
    (22, "Sport", "Women's Asian Hockey Trophy opens"),
    (23, "Bangladesh", "Fire at Yunus family home"),
    (24, "Mideast", "Australia sanctions settlers"),
    (25, "Europe", "LPG tanker sunk off Bulgaria"),
    (26, "Asia", "Takaichi seeks China dialogue"),
    (27, "Trade", "APEC leaders meet in Shenzhen"),
    (28, "Trade", "US–China truce ends 10 Jan"),
    (29, "Tech", "Nvidia denies Beijing spy claim"),
    (30, "Asia", "Pakistan minister heads to Delhi"),
    (31, "India", "New PUC renewal rules"),
    (32, "India", "Punjab PCS exam stayed"),
    (33, "India", "Rahul Gandhi rejects boycott"),
    (34, "USA", "Court orders Doval summons"),
    (35, "World", "Children's Day marked"),
    (36, "India", "State banks top ₹1 lakh cr profit"),
    (37, "India", "Justice Varma resigns"),
    (38, "Canada", "Goldy Brar tops wanted list"),
    (39, "Asia", "Korea left out of summit"),
    (40, "Asia", "Taiwan fears a 'Yalta 2.0'"),
    (41, "Markets", "S&P −2.0%, Nasdaq −2.2%"),
    (42, "Tech", "Anthropic raises $81.3bn"),
    (43, "Diplomacy", "Trump invites Putin to G20"),
    (44, "Diplomacy", "Xi: nuclear war unwinnable"),
    (45, "Asia", "Takaichi–Xi trade greetings"),
    (46, "Asia", "Seoul split over summit"),
    (47, "Europe", "Berlin hosts 'willing' summit"),
    (48, "Energy", "Hormuz kept open in deal"),
]

# Rough continent outlines in (lon, lat), drawn from memory of the map.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-85, 66), (-75, 62),
     (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35), (-80, 25),
     (-85, 20), (-90, 15), (-95, 16), (-105, 20), (-110, 23), (-120, 34),
     (-125, 48), (-150, 60), (-165, 60)],
    [(-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-58, 70)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50), (-73, -40),
     (-75, -30), (-80, -20), (-81, -10), (-80, 0)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
     (40, 15), (48, 11), (51, 10), (48, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (10, -5), (8, 4), (-8, 4), (-13, 12)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 70), (40, 68),
     (45, 66), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37)],
    [(30, 62), (40, 68), (60, 70), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (150, 45),
     (142, 40), (135, 35), (130, 30), (122, 28), (120, 20), (110, 10),
     (105, 5), (100, 8), (98, 15), (95, 20), (90, 22), (85, 20), (80, 10),
     (75, 8), (70, 20), (65, 25), (60, 25), (55, 26), (50, 28), (48, 30),
     (43, 35), (38, 36), (35, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -15), (140, -17), (136, -15), (135, -12), (132, -11), (130, -13),
     (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-1, 57), (-4, 58), (-6, 55)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44), (141, 45)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10)],
    [(120, 18), (122, 16), (124, 11), (126, 7)],
    [(167, -45), (170, -42), (174, -39), (177, -38), (174, -41), (170, -44)],
    [(44, -16), (47, -15), (50, -17), (49, -22), (45, -25), (43, -20)],
    [(-22, 64), (-18, 63), (-14, 64), (-18, 66), (-22, 65)],
    [(-84, 23), (-80, 23), (-77, 21), (-74, 20), (-80, 22)],
    [(80, 6), (81, 8), (80, 9)],
    [(120, 22), (121, 25), (120, 25)],
]

# Numbered pins for the twelve lead stories: (lon, lat).
PINS = {
    1: (-77, 39), 2: (114, 22.5), 3: (85, 19), 4: (4.3, 52),
    5: (46.7, 24.7), 6: (-74, 40.7), 7: (-118, 34), 8: (139, 35.7),
    9: (-80, 26), 10: (13.4, 52.5), 11: (127, 37.5), 12: (178, -18),
}

LEGEND = [
    ("Europe", (43, 94, 167)),
    ("Middle East", (208, 127, 31)),
    ("Asia", (176, 42, 48)),
    ("Africa", (46, 125, 70)),
    ("Americas", (122, 74, 158)),
    ("Oceania", (31, 138, 138)),
]

# ---------------------------------------------------------------- panels

def lead_panel(d, x, y, w, h, story):
    d.rectangle((x, y, x + w, y + h), fill=(255, 255, 255), outline=BORDER, width=2)
    ART[story["art"]](d, (x + 6, y + 6, x + 174, y + h - 6), (233, 236, 238))
    tx = x + 184
    tw = x + w - tx - 10
    badge(d, tx + 11, y + 21, 11, story["n"], fnt("sansb", 12))
    d.text((tx + 28, y + 12), story["tag"], font=fnt("sansb", 12), fill=RED)
    head_lines = fit_lines(d, story["head"], fnt("serifb", 21), tw, 3)
    yy = block(d, tx, y + 38, head_lines, fnt("serifb", 21), INK, 24)
    body_lines = fit_lines(d, story["body"], fnt("sans", 13), tw, 4)
    block(d, tx, yy + 6, body_lines, fnt("sans", 13), (52, 52, 52), 17)


def mini_panel(d, x, y, w, h, story):
    d.rectangle((x, y, x + w, y + h), fill=(255, 255, 255), outline=BORDER, width=2)
    ART[story["art"]](d, (x + 5, y + 5, x + w - 5, y + 57), (233, 236, 238))
    badge(d, x + 13, y + 70, 8, story["n"], fnt("sansb", 9))
    d.text((x + 26, y + 62), story["tag"], font=fnt("sansb", 10), fill=RED)
    head_lines = fit_lines(d, story["head"], fnt("sansb", 14), w - 12, 3)
    yy = block(d, x + 6, y + 78, head_lines, fnt("sansb", 14), INK, 16)
    body_lines = fit_lines(d, story["body"], fnt("sans", 11), w - 12, 3)
    block(d, x + 6, yy + 3, body_lines, fnt("sans", 11), (52, 52, 52), 13)


def draw_map(d, x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), fill=OCEAN)
    lon0, lon1, lat0, lat1 = -168, 192, 80, -60

    def proj(lon, lat):
        px = x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0)
        py = y0 + (lat0 - lat) / (lat0 - lat1) * (y1 - y0)
        return (px, py)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for num, (lon, lat) in sorted(PINS.items()):
        cx, cy = proj(lon, lat)
        badge(d, cx, cy, 8, num, fnt("sansb", 9))


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle((8, 8, 1016, 112), fill=NAVY)
    d.text((24, 16), "THE DAY IN WORLD NEWS", font=fnt("sansb", 14), fill=GOLD_SOFT)
    right = "48 STORIES · 6 CONTINENTS · FULL DAY"
    d.text((1016 - 24 - d.textlength(right, font=fnt("sansb", 14)), 16),
           right, font=fnt("sansb", 14), fill=GOLD_SOFT)
    d.text((24, 40), "Friday 20 November 2026", font=fnt("serifb", 54), fill=(255, 255, 255))
    hline(d, 8, 1016, 112, GOLD, 2)

    # ---- UTC timeline ticker
    d.rectangle((8, 116, 1016, 138), fill=GOLD)
    size = 13
    while size > 10 and d.textlength(TICKER, font=fnt("sansb", size)) > 992:
        size -= 1
    d.text((16, 116 + (22 - fnt("sansb", size).getmetrics()[0]) // 2 - 2),
           TICKER, font=fnt("sansb", size), fill=NAVY)

    # ---- lead stories
    lead_panel(d, 8, 144, 499, 174, LEADS[0])
    lead_panel(d, 513, 144, 503, 174, LEADS[1])

    # ---- brief rows: five columns
    xs = [8, 211, 414, 617, 820]
    ws = [197, 197, 197, 197, 196]
    for i, story in enumerate(BRIEFS[:5]):
        mini_panel(d, xs[i], 324, ws[i], 168, story)
    for i, story in enumerate(BRIEFS[5:]):
        mini_panel(d, xs[i], 498, ws[i], 168, story)

    # ---- by the numbers
    d.rectangle((8, 672, 1016, 724), fill=NAVY)
    cell_w = 1008 / 5
    for i, (val, cap) in enumerate(NUMBERS):
        cx = 8 + cell_w * i + cell_w / 2
        if i:
            d.line((8 + cell_w * i, 678, 8 + cell_w * i, 718), fill=GOLD, width=1)
        vf = fnt("sansb", 24)
        d.text((cx - d.textlength(val, font=vf) / 2, 678), val, font=vf, fill=GOLD_SOFT)
        cf = fnt("sans", 10)
        d.text((cx - d.textlength(cap, font=cf) / 2, 706), cap, font=cf, fill=(255, 255, 255))

    # ---- map (left) + the other 36 stories (right)
    d.rectangle((8, 730, 468, 992), fill=(255, 255, 255), outline=BORDER, width=2)
    d.text((16, 738), "WHERE IT HAPPENED", font=fnt("sansb", 13), fill=INK)
    draw_map(d, 16, 758, 460, 952)
    lx = 16
    for name, col in LEGEND:
        d.ellipse((lx, 968, lx + 9, 977), fill=col)
        lf = fnt("sans", 10)
        d.text((lx + 12, 966), name, font=lf, fill=INK)
        lx += 12 + d.textlength(name, font=lf) + 10
    d.text((16, 980), "Numbered dots mark stories 1–12.",
           font=fnt("sans", 9), fill=GREY)

    d.rectangle((474, 730, 1016, 992), fill=(255, 255, 255), outline=BORDER, width=2)
    d.text((484, 738), "ALSO ON FRIDAY 20 NOVEMBER — 36 MORE STORIES",
           font=fnt("sansb", 12), fill=INK)
    cols = [(484, 256), (748, 260)]
    for ci, (cx0, cw) in enumerate(cols):
        for ri in range(18):
            n, cat, line = MORE[ci * 18 + ri]
            yy = 758 + ri * 13
            d.text((cx0, yy), str(n), font=fnt("sansb", 10), fill=RED)
            text = "%s: %s" % (cat, line)
            size = 10
            while size > 8 and d.textlength(text, font=fnt("sans", size)) > cw - 22:
                size -= 0.5
            f = fnt("sans", int(size))
            d.text((cx0 + 20, yy), text, font=f, fill=INK)

    # ---- footer
    d.text((8, 996),
           "Morning update to 07:20 WIB — the trilateral summit, Trump on Iran, "
           "the ICJ ruling and Cyclone Akvan lead the day.",
           font=fnt("sans", 10), fill=GREY)
    d.text((8, 1009),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, NASA, IMD, ICJ, The Hindu, "
           "Times of India and others. Original drawings.",
           font=fnt("sans", 10), fill=GREY)
    return img


def main():
    img = draw_page()
    img.save(OUT, format="PNG")
    raw = open(OUT, "rb").read()
    print("entry.png %d bytes sha256 %s" % (len(raw), hashlib.sha256(raw).hexdigest()))
    print("size %dx%d" % img.size)


if __name__ == "__main__":
    main()
