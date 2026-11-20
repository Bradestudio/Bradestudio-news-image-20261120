#!/usr/bin/env python3
"""Friday 20 November 2026 -- the day in world news, one image.

Draws entry.png (1024x1024): a navy masthead, a gold UTC ticker, two
lead stories, ten illustrated briefs, a BY THE NUMBERS strip, a world
map with numbered pins for stories 1-12, and a numbered list of 36 more
stories. 48 verified stories in total.

Pillow only, no network, no clock: two runs write byte-identical files.
Run:  python3 gen_image.py [output-path]
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = (13, 30, 58)
GOLD = (217, 164, 65)
PAPER = (253, 252, 247)
INK = (24, 24, 24)
GREY = (96, 96, 96)
RED = (179, 32, 44)
LINE = (28, 28, 28)
SEA = (211, 231, 238)
LAND = (232, 213, 176)
LAND_LINE = (176, 152, 108)
STEEL = (70, 110, 160)
BLUE = (38, 84, 160)
ORANGE = (214, 110, 30)
CRIMSON = (179, 32, 44)
TEAL = (15, 118, 110)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(text, fnt, width, d):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=fnt, fill=fill)


# ---------------------------------------------------------------- data

LEADS = [
    {
        "num": 1,
        "kicker": "1  —  USA · IRAN",
        "headline": "Trump pushes Iran decision into 2027",
        "body": ("The president says there is no hurry and he will decide "
                 "after the new year. Allies welcome the pause; rivals read "
                 "it as hesitation."),
        "art": "dome",
        "source": "Source: Reuters.",
    },
    {
        "num": 2,
        "kicker": "2  —  CHINA · SUMMIT",
        "headline": "First three-way summit ends in peace deal",
        "body": ("Just over an hour of talks in Shenzhen yields a three-way "
                 "peace declaration, cuts to nuclear risk, and Hormuz kept "
                 "open. Putin is invited to the G20 in Miami."),
        "art": "summit",
        "source": "Sources: Center Times, Reuters.",
    },
]

BRIEFS = [
    {"num": 3, "kicker": "ASIA · WEATHER", "headline": "Akvan landfall due at noon",
     "body": "300,000 evacuated and 423 rescue teams ready as 90–100 km/h winds near Gopalpur.",
     "art": "spiral", "tint": (219, 234, 254)},
    {"num": 4, "kicker": "JUSTICE · THE HAGUE", "headline": "Court: Myanmar committed genocide",
     "body": "The ICJ rules the 2017 crackdown on the Rohingya was genocide.",
     "art": "scales", "tint": (236, 231, 221)},
    {"num": 5, "kicker": "MIDDLE EAST · WAR", "headline": "Missile fire hits Riyadh tower",
     "body": "A Houthi attack damages the Saudi wealth fund tower in the capital.",
     "art": "tower", "tint": (243, 226, 199)},
    {"num": 6, "kicker": "TECH · MARKETS", "headline": "Anthropic jumps 17% on debut",
     "body": "Priced at $83, opens $111.50, closes $97.17 — near $1.76tn. The Dow falls 1,084.",
     "art": "chart", "tint": (220, 240, 221)},
    {"num": 7, "kicker": "SPACE · NASA", "headline": "Voyager 1 a light-day away",
     "body": "NASA confirms the milestone: 16.1bn miles out, its signal now takes a full day to reach us.",
     "art": "satellite", "tint": (16, 28, 51)},
    {"num": 8, "kicker": "SPACE · JAPAN", "headline": "Hayabusa2 abandons landing",
     "body": "Engine trouble ends the asteroid landing plan; the probe changes course instead.",
     "art": "rocket", "tint": (16, 28, 51)},
    {"num": 9, "kicker": "CULTURE · GAMING", "headline": "GTA VI tops The Odyssey",
     "body": "Sales pass the film's $1.80bn global run — a day after launch, already a record.",
     "art": "skyline", "tint": (245, 183, 92)},
    {"num": 10, "kicker": "EUROPE · DIPLOMACY", "headline": "Europe ready to talk to Russia",
     "body": "Leaders in Berlin say they are ready for talks to end the war in Ukraine.",
     "art": "people", "tint": (221, 230, 238)},
    {"num": 11, "kicker": "ASIA · JUSTICE", "headline": "Seoul court clears Han Duck-soo",
     "body": "South Korea's top court overturns the ex-PM's conviction over the 2024 martial-law case.",
     "art": "columns", "tint": (236, 231, 221)},
    {"num": 12, "kicker": "PACIFIC · CLIMATE", "headline": "Fiji declares drought disaster",
     "body": "El Niño leaves the islands short of water; a national state of disaster is declared.",
     "art": "sun", "tint": (245, 233, 200)},
]

NUMBERS = [
    ("3-way", "Trump–Xi–Putin summit"),
    ("$97.17", "Anthropic close, +17%"),
    ("300,000", "Akvan evacuations"),
    ("90–100 km/h", "Akvan landfall winds"),
    ("1 light-day", "Voyager 1 from Earth"),
]

MORE = [
    "India: Modi meets William and Kate",
    "India: Modi opens FICCI centenary",
    "Markets: Sensex and Nifty climb",
    "USA: Jobless claims hit 203,000",
    "War: Crimea bridge rail traffic halted",
    "Asia: N. Korea expands Yongbyon site",
    "Americas: US–Venezuela military pact",
    "Sport: Nicholls 113* rescues NZ",
    "Sport: Satwik–Chirag into HK quarters",
    "Sport: Women's Hockey Trophy begins",
    "Bangladesh: Fire at Yunus family home",
    "Mideast: Australia sanctions settlers",
    "Europe: LPG tanker sunk off Bulgaria",
    "Asia: Takaichi seeks China dialogue",
    "Trade: APEC leaders meet in Shenzhen",
    "Trade: US–China tariff truce ends 10 Jan",
    "Tech: Nvidia denies Beijing spy claim",
    "Asia: Pakistan minister heads to Delhi",
    "India: New PUC renewal rules",
    "India: Punjab PCS exam stayed",
    "India: Rahul Gandhi rejects poll boycott",
    "USA: Court orders Doval summons",
    "World: Children's Day marked today",
    "India: PSU banks top Rs 1 lakh cr",
    "India: Justice Varma resigns",
    "Canada: Goldy Brar tops wanted list",
    "Asia: Korea left out of the summit",
    "Asia: Taiwan fears a 'Yalta 2.0'",
    "Markets: S&P -2.0%, Nasdaq -2.2%",
    "Tech: Anthropic IPO raised $81.3bn",
    "Diplomacy: Trump invites Putin to G20",
    "Diplomacy: Xi — nuclear war 'unwinnable'",
    "Asia: Takaichi–Xi exchange greetings",
    "Asia: Seoul split over the summit",
    "Europe: Berlin hosts 'willing' summit",
    "Energy: Hormuz kept open in the deal",
]

TICKER = ("00:00 Summit opens  •  06:00 Trump defers Iran  •  10:00 ICJ rules  "
          "•  12:00 Akvan due  •  14:00 Anthropic +17%  •  21:30 Markets close")

# Rough stylised continents, as (lon, lat) vertices.
AMERICAS = [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-135, 58), (-130, 54),
            (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
            (-97, 16), (-92, 15), (-87, 13), (-83, 9), (-79, 9), (-80, 7), (-77, 4),
            (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23), (-70, -30),
            (-73, -37), (-73, -44), (-71, -52), (-66, -55), (-65, -47), (-62, -40),
            (-57, -34), (-52, -32), (-48, -28), (-41, -23), (-38, -15), (-35, -8),
            (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-59, 8), (-65, 10),
            (-72, 12), (-76, 10), (-79, 9), (-83, 10), (-86, 12), (-90, 14), (-95, 16),
            (-97, 16), (-97, 21), (-97, 26), (-93, 30), (-89, 30), (-84, 30),
            (-81, 26), (-80, 32), (-76, 35), (-74, 39), (-70, 42), (-68, 44),
            (-65, 44), (-60, 46), (-55, 52), (-60, 55), (-65, 58), (-68, 58),
            (-72, 62), (-78, 62), (-80, 66), (-85, 66), (-90, 69), (-95, 69),
            (-100, 68), (-110, 68), (-120, 69), (-130, 70), (-140, 70), (-150, 70),
            (-158, 71), (-165, 68), (-168, 66)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-25, 70),
             (-20, 74), (-25, 78), (-35, 80), (-50, 80), (-58, 76), (-60, 72), (-58, 64)]
AFRICA = [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-6, 34), (-2, 35), (3, 37),
          (10, 37), (11, 34), (15, 32), (20, 32), (25, 32), (30, 31), (32, 31),
          (34, 28), (35, 22), (37, 18), (39, 15), (43, 11), (48, 11), (51, 10),
          (46, 5), (41, 1), (40, -4), (40, -10), (37, -15), (35, -20), (32, -26),
          (28, -33), (20, -35), (17, -32), (15, -27), (13, -18), (12, -10),
          (13, -6), (9, -1), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12), (-17, 15)]
EURASIA = [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (-1, 51), (3, 53), (7, 54),
           (8, 57), (10, 59), (6, 60), (5, 62), (10, 64), (15, 68), (20, 70),
           (25, 71), (30, 70), (35, 68), (40, 68), (45, 68), (50, 69), (55, 69),
           (60, 69), (65, 70), (70, 72), (75, 73), (80, 73), (85, 74), (90, 75),
           (95, 76), (100, 77), (105, 77), (110, 76), (115, 74), (120, 73),
           (125, 72), (130, 72), (135, 72), (140, 72), (145, 72), (150, 70),
           (155, 69), (160, 69), (165, 67), (170, 66), (175, 65), (178, 65),
           (178, 62), (170, 60), (162, 56), (158, 52), (156, 51), (150, 59),
           (142, 59), (141, 53), (140, 48), (138, 44), (135, 43), (132, 43),
           (130, 42), (127, 40), (126, 38), (122, 38), (121, 35), (120, 32),
           (122, 28), (119, 25), (114, 22), (110, 21), (108, 18), (106, 10),
           (104, 9), (103, 7), (100, 8), (98, 10), (97, 15), (94, 17), (92, 21),
           (89, 22), (87, 21), (86, 20), (83, 18), (80, 15), (78, 8), (76, 10),
           (74, 14), (72, 20), (70, 22), (67, 24), (66, 25), (62, 25), (58, 26),
           (54, 26), (52, 26), (50, 29), (48, 30), (45, 29), (42, 30), (39, 31),
           (36, 36), (33, 36), (30, 36), (27, 37), (23, 36), (20, 40), (18, 40),
           (15, 44), (12, 44), (8, 44), (4, 43), (0, 43), (-2, 44), (-2, 47),
           (-4, 48), (-6, 49), (-10, 48), (-10, 43), (-10, 36)]
AUSTRALIA = [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32),
             (132, -32), (135, -35), (137, -35), (140, -38), (145, -38), (150, -37),
             (153, -32), (153, -27), (151, -24), (149, -20), (146, -19), (143, -15),
             (142, -11), (140, -17), (137, -12), (135, -15), (132, -12), (130, -13),
             (126, -14), (122, -17), (118, -20), (114, -22), (113, -22)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
         (141, 38), (141, 41), (143, 42), (144, 44), (142, 44), (140, 41),
         (139, 38), (137, 36), (135, 34), (132, 33), (130, 31)]
NEW_ZEALAND = [(167, -45), (169, -43), (172, -41), (174, -39), (176, -38),
               (178, -38), (176, -40), (174, -42), (171, -44), (168, -46), (167, -45)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25),
              (44, -22), (43, -19), (44, -16)]
BORNEO = [(109, 1), (111, 3), (114, 4), (117, 6), (118, 2), (117, -2),
          (114, -3), (110, -3), (109, 1)]
SUMATRA = [(95, 5), (98, 3), (100, 0), (103, -3), (105, -5), (104, -6),
           (101, -4), (99, -1), (97, 2), (95, 5)]
CONTINENTS = [AMERICAS, GREENLAND, AFRICA, EURASIA, AUSTRALIA, UK, JAPAN,
              NEW_ZEALAND, MADAGASCAR, BORNEO, SUMATRA]

# (number, lon, lat, colour, nudge-x, nudge-y) -- nudges keep the crowded
# European and US-east pins from sitting on top of each other.
PINS = [
    (1, -77, 39, STEEL, -14, 10),
    (2, 114, 22.5, CRIMSON, 0, -12),
    (3, 86, 19.5, CRIMSON, 10, 8),
    (4, 4.5, 52.1, BLUE, -16, -8),
    (5, 46.7, 24.6, ORANGE, 12, -6),
    (6, -74, 40.7, STEEL, 14, -10),
    (7, -118, 34.2, STEEL, -12, 8),
    (8, 139.7, 35.7, CRIMSON, -10, -10),
    (9, -80.2, 25.8, STEEL, 12, 10),
    (10, 13.4, 52.5, BLUE, 16, -12),
    (11, 127, 37.5, CRIMSON, 12, 10),
    (12, 178, -17.5, TEAL, -8, 10),
]


# ---------------------------------------------------------------- pictograms

def pic_dome(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(227, 233, 240))
    cx = (x0 + x1) // 2
    d.rectangle([x0 + 8, y1 - 10, x1 - 8, y1 - 4], fill=(90, 96, 108))
    d.rectangle([x0 + 14, y1 - 18, x1 - 14, y1 - 10], fill=(120, 126, 138))
    for i in range(4):
        px = x0 + 22 + i * 24
        d.rectangle([px, y1 - 78, px + 10, y1 - 18], fill=(245, 245, 240))
    d.rectangle([x0 + 14, y1 - 86, x1 - 14, y1 - 78], fill=(200, 204, 210))
    d.pieslice([cx - 34, y1 - 128, cx + 34, y1 - 78], 180, 360, fill=(245, 245, 240))
    d.rectangle([cx - 34, y1 - 104, cx + 34, y1 - 86], fill=(245, 245, 240))
    d.line([cx, y1 - 128, cx, y1 - 142], fill=(60, 60, 60), width=2)
    d.polygon([(cx, y1 - 142), (cx + 12, y1 - 138), (cx, y1 - 134)], fill=RED)


def pic_summit(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(239, 232, 220))
    poles = [x0 + 22, x0 + 62, x0 + 102]
    for px, kind in zip(poles, ("us", "cn", "ru")):
        d.line([px, y0 + 34, px, y0 + 78], fill=(80, 70, 60), width=2)
        fx, fy = px + 1, y0 + 10
        if kind == "us":
            for i in range(5):
                d.rectangle([fx, fy + i * 5, fx + 26, fy + i * 5 + 2],
                            fill=RED if i % 2 == 0 else (245, 245, 245))
            d.rectangle([fx, fy, fx + 11, fy + 11], fill=BLUE)
        elif kind == "cn":
            d.rectangle([fx, fy, fx + 26, fy + 24], fill=RED)
            d.ellipse([fx + 4, fy + 5, fx + 11, fy + 12], fill=GOLD)
        else:
            d.rectangle([fx, fy, fx + 26, fy + 8], fill=(245, 245, 245))
            d.rectangle([fx, fy + 8, fx + 26, fy + 16], fill=BLUE)
            d.rectangle([fx, fy + 16, fx + 26, fy + 24], fill=RED)
    d.rectangle([x0 + 8, y1 - 34, x1 - 8, y1 - 12], fill=(122, 82, 52))
    d.rectangle([x0 + 8, y1 - 12, x1 - 8, y1 - 8], fill=(90, 58, 36))
    for cx, skin, suit in ((x0 + 28, (232, 196, 160), NAVY),
                           ((x0 + x1) // 2, (240, 205, 170), (90, 30, 30)),
                           (x1 - 28, (232, 196, 160), (40, 60, 40))):
        d.ellipse([cx - 9, y1 - 62, cx + 9, y1 - 44], fill=skin)
        d.pieslice([cx - 14, y1 - 46, cx + 14, y1 - 30], 180, 360, fill=suit)


def pic_spiral(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r, start in ((17, 0), (13, 70), (9, 150), (5, 230)):
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 270,
              fill=BLUE, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)


def pic_scales(d, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    d.line([cx, y0 + 4, cx, y1 - 8], fill=(60, 50, 30), width=3)
    d.line([x0 + 6, y0 + 10, x1 - 6, y0 + 10], fill=(60, 50, 30), width=3)
    d.rectangle([x0 + 12, y1 - 6, x1 - 12, y1 - 2], fill=(60, 50, 30))
    for px in (x0 + 10, x1 - 10):
        d.line([px, y0 + 10, px - 7, y0 + 24], fill=(60, 50, 30), width=2)
        d.line([px, y0 + 10, px + 7, y0 + 24], fill=(60, 50, 30), width=2)
        d.pieslice([px - 8, y0 + 22, px + 8, y0 + 32], 0, 180, fill=GOLD)
    d.ellipse([cx - 3, y0 + 2, cx + 3, y0 + 8], fill=GOLD)


def pic_tower(d, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    d.rectangle([cx - 16, y0 + 12, cx + 16, y1 - 8], fill=(196, 164, 110))
    d.rectangle([cx - 20, y0 + 8, cx + 20, y0 + 12], fill=(150, 120, 76))
    for row in range(4):
        for col in range(3):
            wx = cx - 12 + col * 9
            wy = y0 + 18 + row * 6
            d.rectangle([wx, wy, wx + 5, wy + 4], fill=(70, 60, 44))
    for sx, sy, r in ((cx + 22, y0 + 6, 5), (cx + 28, y0 + 1, 4), (cx + 14, y0 + 2, 4)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))
    d.polygon([(cx + 8, y0 + 16), (cx + 14, y0 + 10), (cx + 20, y0 + 16)],
              fill=ORANGE)
    d.rectangle([cx - 20, y1 - 8, cx + 20, y1 - 5], fill=(120, 96, 64))


def pic_chart(d, x0, y0, x1, y1):
    d.line([x0 + 6, y1 - 6, x1 - 4, y1 - 6], fill=(60, 60, 60), width=2)
    d.line([x0 + 6, y1 - 6, x0 + 6, y0 + 4], fill=(60, 60, 60), width=2)
    bars = [10, 16, 22, 30]
    for i, h in enumerate(bars):
        bx = x0 + 12 + i * 12
        d.rectangle([bx, y1 - 6 - h, bx + 8, y1 - 6], fill=(34, 139, 84))
    d.line([x0 + 10, y1 - 16, x0 + 24, y1 - 24, x0 + 38, y1 - 30, x1 - 6, y1 - 38],
           fill=RED, width=2)
    d.polygon([(x1 - 6, y1 - 38), (x1 - 12, y1 - 38), (x1 - 6, y1 - 32)], fill=RED)


def pic_satellite(d, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for sx, sy in ((x0 + 6, y0 + 5), (x1 - 8, y0 + 9), (x0 + 12, y1 - 8),
                   (x1 - 12, y1 - 6), (x0 + 30, y0 + 4)):
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    d.rectangle([x0 + 6, cy - 8, cx - 8, cy + 8], fill=(70, 110, 180))
    d.rectangle([cx + 8, cy - 8, x1 - 6, cy + 8], fill=(70, 110, 180))
    d.rectangle([cx - 8, cy - 6, cx + 8, cy + 6], fill=(200, 200, 200))
    d.arc([cx - 14, cy - 14, cx + 2, cy + 2], 90, 270, fill=GOLD, width=2)
    d.arc([cx + 14, cy - 20, cx + 30, cy - 4], 200, 340, fill=GOLD, width=2)


def pic_rocket(d, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    for sx, sy in ((x0 + 6, y0 + 6), (x1 - 8, y0 + 8), (x0 + 10, y1 - 10),
                   (x1 - 10, y1 - 8)):
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    d.polygon([(cx, y0 + 2), (cx - 7, y0 + 14), (cx + 7, y0 + 14)], fill=RED)
    d.rectangle([cx - 7, y0 + 14, cx + 7, y1 - 14], fill=(240, 240, 240))
    d.ellipse([cx - 4, y0 + 18, cx + 4, y0 + 26], fill=(70, 140, 220))
    d.polygon([(cx - 7, y1 - 18), (cx - 14, y1 - 8), (cx - 7, y1 - 10)], fill=RED)
    d.polygon([(cx + 7, y1 - 18), (cx + 14, y1 - 8), (cx + 7, y1 - 10)], fill=RED)
    d.polygon([(cx - 4, y1 - 14), (cx + 4, y1 - 14), (cx, y1 - 2)], fill=ORANGE)
    d.polygon([(cx - 2, y1 - 14), (cx + 2, y1 - 14), (cx, y1 - 6)], fill=GOLD)


def pic_skyline(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y0 + 14], fill=(245, 183, 92))
    d.rectangle([x0, y0 + 14, x1, y0 + 26], fill=(238, 140, 80))
    d.rectangle([x0, y0 + 26, x1, y1], fill=(226, 110, 70))
    cx = (x0 + x1) // 2
    d.ellipse([cx - 8, y0 + 6, cx + 8, y0 + 22], fill=(250, 220, 120))
    base = y1
    heights = [16, 26, 20, 30, 22]
    bw = (x1 - x0) // 5
    for i, h in enumerate(heights):
        bx = x0 + i * bw + 1
        d.rectangle([bx, base - h, bx + bw - 2, base], fill=(40, 30, 44))


def pic_people(d, x0, y0, x1, y1):
    for cx, skin, suit in ((x0 + 14, (232, 196, 160), (60, 90, 140)),
                           ((x0 + x1) // 2, (240, 205, 170), (150, 40, 40)),
                           (x1 - 14, (220, 185, 150), (90, 90, 90))):
        d.ellipse([cx - 7, y0 + 6, cx + 7, y0 + 20], fill=skin)
        d.pieslice([cx - 11, y0 + 20, cx + 11, y0 + 36], 180, 360, fill=suit)


def pic_columns(d, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    d.polygon([(x0 + 6, y0 + 12), (x1 - 6, y0 + 12), (cx, y0 + 2)], fill=(150, 140, 120))
    d.rectangle([x0 + 6, y0 + 12, x1 - 6, y0 + 16], fill=(120, 112, 96))
    for i in range(3):
        px = x0 + 12 + i * 18
        d.rectangle([px, y0 + 16, px + 8, y1 - 8], fill=(245, 245, 240))
    d.rectangle([x0 + 6, y1 - 8, x1 - 6, y1 - 4], fill=(120, 112, 96))
    d.rectangle([x0 + 2, y1 - 4, x1 - 2, y1 - 1], fill=(90, 84, 70))


def pic_sun(d, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    cy = y0 + 13
    for ang in range(0, 360, 45):
        r1, r2 = 11, 16
        a = math.radians(ang)
        d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
                cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
               fill=ORANGE, width=2)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=GOLD)
    d.rectangle([x0, y1 - 10, x1, y1], fill=(196, 164, 110))
    d.line([x0 + 6, y1 - 10, x0 + 16, y1 - 4, x0 + 26, y1 - 8], fill=(120, 96, 64), width=2)
    d.line([x1 - 8, y1 - 10, x1 - 18, y1 - 3, x1 - 28, y1 - 7], fill=(120, 96, 64), width=2)


PICS = {"dome": pic_dome, "summit": pic_summit, "spiral": pic_spiral,
        "scales": pic_scales, "tower": pic_tower, "chart": pic_chart,
        "satellite": pic_satellite, "rocket": pic_rocket, "skyline": pic_skyline,
        "people": pic_people, "columns": pic_columns, "sun": pic_sun}


# ---------------------------------------------------------------- sections

def masthead(d):
    d.rectangle([10, 8, 1014, 98], fill=NAVY)
    d.rectangle([10, 96, 1014, 98], fill=GOLD)
    d.text((16, 16), "THE DAY IN WORLD NEWS", font=SANS_B(13), fill=GOLD)
    right = "48 STORIES · 6 CONTINENTS"
    d.text((1014 - 6 - d.textlength(right, font=SANS_B(13)), 16), right,
           font=SANS_B(13), fill=GOLD)
    d.text((16, 34), "Friday 20 November 2026", font=SERIF_B(52), fill=(255, 255, 255))


def ticker(d):
    d.rectangle([10, 98, 1014, 120], fill=GOLD)
    fnt = SANS_B(12)
    w = d.textlength(TICKER, font=fnt)
    d.text(((W - w) / 2, 102), TICKER, font=fnt, fill=NAVY)


def lead_panel(d, x, y, w, h, lead):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1, fill=PAPER)
    ax0, ay0, ax1, ay1 = x + 8, y + 8, x + 140, y + h - 8
    PICS[lead["art"]](d, ax0, ay0, ax1, ay1)
    tx = x + 150
    tw = x + w - 10 - tx
    d.text((tx, y + 10), lead["kicker"], font=SANS_B(11), fill=RED)
    head = wrap(lead["headline"], SERIF_B(22), tw, d)
    assert len(head) <= 2, f"lead headline too long: {lead['headline']}"
    text_block(d, tx, y + 30, head, SERIF_B(22), INK, 26)
    by = y + 30 + len(head) * 26 + 6
    body = wrap(lead["body"], SANS(11), tw, d)
    assert len(body) <= 4, f"lead body too long: {lead['body']}"
    text_block(d, tx, by, body, SANS(11), (40, 40, 40), 15)
    d.text((tx, y + h - 18), lead["source"], font=SANS(9), fill=GREY)


def brief_card(d, x, y, w, h, b):
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1, fill=PAPER)
    d.rectangle([x + 4, y + 4, x + w - 4, y + 44], fill=b["tint"])
    PICS[b["art"]](d, x + 4, y + 4, x + w - 4, y + 44)
    d.text((x + 6, y + 48), b["kicker"], font=SANS_B(9), fill=RED)
    head = wrap(b["headline"], SERIF_B(13), w - 12, d)
    assert len(head) <= 2, f"brief headline too long: {b['headline']}"
    text_block(d, x + 6, y + 59, head, SERIF_B(13), INK, 14)
    body = wrap(b["body"], SANS(10), w - 12, d)
    assert len(body) <= 3, f"brief body too long: {b['body']}"
    text_block(d, x + 6, y + 90, body, SANS(10), (40, 40, 40), 11)


def numbers_strip(d, y):
    d.rectangle([10, y, 1014, y + 50], fill=NAVY)
    cell = 1004 / 5
    for i, (num, cap) in enumerate(NUMBERS):
        cx = 10 + cell * i + cell / 2
        nw = d.textlength(num, font=SERIF_B(23))
        d.text((cx - nw / 2, y + 5), num, font=SERIF_B(23), fill=GOLD)
        cw = d.textlength(cap, font=SANS(9))
        d.text((cx - cw / 2, y + 34), cap, font=SANS(9), fill=(255, 255, 255))
        if i:
            d.line([10 + cell * i, y + 8, 10 + cell * i, y + 42], fill=GOLD, width=1)


def world_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=SEA)

    def proj(lon, lat):
        px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
        py = y0 + (84.0 - lat) / 142.0 * (y1 - y0)
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    fnt = SANS_B(10)
    for num, lon, lat, colour, dx, dy in PINS:
        px, py = proj(lon, lat)
        lx, ly = px + dx, py + dy
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
        if dx or dy:
            d.line([px, py, lx, ly], fill=INK, width=1)
        d.ellipse([lx - 9, ly - 9, lx + 9, ly + 9], fill=colour,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        tw = d.textlength(label, font=fnt)
        d.text((lx - tw / 2, ly - 7), label, font=fnt, fill=(255, 255, 255))


def bottom(d):
    # map panel
    d.rectangle([10, 610, 478, 986], outline=LINE, width=1, fill=PAPER)
    d.text((18, 618), "WHERE IT HAPPENED", font=SANS_B(13), fill=INK)
    world_map(d, (18, 640, 470, 928))
    legend = [(STEEL, "Americas"), (BLUE, "Europe"), (ORANGE, "Middle East"),
              (CRIMSON, "Asia"), (TEAL, "Oceania")]
    lx = 18
    for colour, name in legend:
        d.ellipse([lx, 940, lx + 10, 950], fill=colour)
        d.text((lx + 13, 939), name, font=SANS(10), fill=INK)
        lx += 13 + d.textlength(name, font=SANS(10)) + 14
    d.text((18, 960), "Numbered dots mark stories 1–12.",
           font=SANS(10), fill=GREY)
    # more-stories panel
    d.rectangle([482, 610, 1014, 986], outline=LINE, width=1, fill=PAPER)
    d.text((492, 618), "ALSO ON FRIDAY 20 NOVEMBER — 36 MORE STORIES",
           font=SANS_B(12), fill=INK)
    d.line([492, 638, 1004, 638], fill=LINE, width=1)
    assert len(MORE) == 36, f"expected 36 more stories, got {len(MORE)}"
    for i, item in enumerate(MORE):
        col = i // 18
        row = i % 18
        x = 492 + col * 262
        y = 650 + row * 18
        num = str(13 + i)
        d.text((x, y), num, font=SANS_B(10), fill=RED)
        tx = x + 20
        assert d.textlength(item, font=SANS(10)) <= 230, \
            f"more item too long: {item}"
        d.text((tx, y), item, font=SANS(10), fill=INK)


def footer(d):
    d.text((10, 992),
           "Morning update to 07:45 WIB — the trilateral summit, Trump on Iran, "
           "the ICJ ruling and Cyclone Akvan lead the day.",
           font=SANS(9), fill=GREY)
    d.text((10, 1005),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, NASA, IMD, ICJ, The Hindu, "
           "Times of India and others. Original drawings.",
           font=SANS(9), fill=GREY)


def build():
    assert len(LEADS) == 2 and len(BRIEFS) == 10
    assert 2 + 10 + len(MORE) == 48, "story count must be 48"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    ticker(d)
    lead_panel(d, 10, 124, 497, 168, LEADS[0])
    lead_panel(d, 517, 124, 497, 168, LEADS[1])
    cols_x = [10, 212, 414, 616, 818]
    for row in range(2):
        for col in range(5):
            brief_card(d, cols_x[col], 296 + row * 130, 196, 126,
                       BRIEFS[row * 5 + col])
    numbers_strip(d, 556)
    bottom(d)
    footer(d)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, format="PNG")
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
