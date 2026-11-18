#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news infographic (1024x1024 PNG).

Run:  python3 generate_entry.py
Writes entry.png next to this script. Deterministic: no timestamps,
no randomness, fixed font sizes and layout.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
BG = (247, 244, 236)      # off-white paper
INK = (27, 27, 27)        # near-black text
MUTED = (90, 86, 76)      # grey-brown secondary text
NAVY = (20, 33, 61)       # header
RED = (179, 38, 30)       # lead accent
BLUE = (29, 78, 216)
TEAL = (14, 124, 107)
AMBER = (180, 83, 9)
GREEN = (21, 128, 61)
PURPLE = (109, 40, 217)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)
LEAD_BG = (253, 236, 234)

LIB = "/usr/share/fonts/truetype/liberation"
DEJ = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Liberation Sans first, DejaVu Sans as fallback."""
    for base, fname in (
        (LIB, name),
        (DEJ, name.replace("LiberationSans", "DejaVuSans")),
    ):
        path = os.path.join(base, fname)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def bold(size):
    return font("LiberationSans-Bold.ttf", size)


def regular(size):
    return font("LiberationSans-Regular.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines, min_size=14):
    """Wrap text, shrinking the font until it fits max_lines."""
    size = fnt.size
    while size > min_size:
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return lines, fnt
        size -= 1
        fnt = bold(size) if "Bold" in fnt.getname()[0] or True else fnt
        # rebuild with the same family the caller used
        fnt = ImageFont.truetype(fnt.path, size)
    return wrap(draw, text, fnt, max_w), fnt


def draw_chip(draw, x, y, text, color):
    """Small coloured tag chip; returns its width."""
    fnt = bold(17)
    tw = draw.textlength(text, font=fnt)
    pad_x, pad_y = 10, 5
    draw.rounded_rectangle(
        [x, y, x + tw + 2 * pad_x, y + 27], radius=13, fill=color
    )
    draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=(255, 255, 255))
    return tw + 2 * pad_x


# ---------------------------------------------------------------- icons
def icon_tanker(draw, x, y, s, color):
    """Oil tanker on waves, drawn inside a s x s box at (x, y)."""
    u = s / 100.0
    # containers
    draw.rectangle([x + 18 * u, y + 22 * u, x + 34 * u, y + 42 * u], fill=color)
    draw.rectangle([x + 37 * u, y + 18 * u, x + 53 * u, y + 42 * u], fill=color)
    draw.rectangle([x + 56 * u, y + 26 * u, x + 70 * u, y + 42 * u], fill=color)
    # funnel
    draw.rectangle([x + 74 * u, y + 20 * u, x + 84 * u, y + 42 * u], fill=RED)
    # hull
    draw.polygon(
        [(x + 8 * u, y + 42 * u), (x + 92 * u, y + 42 * u),
         (x + 84 * u, y + 62 * u), (x + 16 * u, y + 62 * u)],
        fill=color,
    )
    # waves
    for i, wx in enumerate((6, 34, 62)):
        draw.arc([x + wx * u, y + 68 * u, x + (wx + 28) * u, y + 84 * u],
                 start=0, end=180, fill=color, width=4)
    # smoke
    draw.ellipse([x + 76 * u, y + 6 * u, x + 84 * u, y + 14 * u], fill=MUTED)


def icon_bridge(draw, x, y, s, color):
    """Suspension bridge inside a s x s box at (x, y)."""
    u = s / 100.0
    draw.rectangle([x + 6 * u, y + 58 * u, x + 94 * u, y + 64 * u], fill=color)
    draw.rectangle([x + 20 * u, y + 18 * u, x + 26 * u, y + 62 * u], fill=color)
    draw.rectangle([x + 74 * u, y + 18 * u, x + 80 * u, y + 62 * u], fill=color)
    # sagging main cable between the tower tops
    draw.arc([x + 20 * u, y + 6 * u, x + 80 * u, y + 62 * u],
             start=0, end=180, fill=color, width=3)
    # vertical suspenders from cable to deck
    for sx in (34, 50, 66):
        draw.line([x + sx * u, y + 44 * u, x + sx * u, y + 58 * u],
                  fill=color, width=3)
    # water
    for i, wx in enumerate((8, 40, 68)):
        draw.arc([x + wx * u, y + 72 * u, x + (wx + 24) * u, y + 86 * u],
                 start=0, end=180, fill=color, width=4)


def icon_tent_snow(draw, x, y, s, color):
    """Shelter tent with a snowflake, inside a s x s box at (x, y)."""
    u = s / 100.0
    draw.polygon([(x + 50 * u, y + 22 * u), (x + 88 * u, y + 70 * u),
                  (x + 12 * u, y + 70 * u)], fill=color)
    draw.polygon([(x + 50 * u, y + 48 * u), (x + 62 * u, y + 70 * u),
                  (x + 38 * u, y + 70 * u)], fill=BG)
    # snowflake
    cx, cy, r = x + 78 * u, y + 20 * u, 11 * u
    for ang in (0, 60, 120):
        import math
        a = math.radians(ang)
        draw.line([cx - r * math.cos(a), cy - r * math.sin(a),
                   cx + r * math.cos(a), cy + r * math.sin(a)],
                  fill=TEAL, width=4)
    draw.ellipse([cx - 3 * u, cy - 3 * u, cx + 3 * u, cy + 3 * u], fill=TEAL)


def icon_missile(draw, x, y, s, color):
    """Missile flying up-right, drawn on a rotated layer."""
    layer = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    u = s / 100.0
    # body
    d.polygon([(50 * u, 8 * u), (62 * u, 30 * u), (62 * u, 68 * u),
               (50 * u, 78 * u), (38 * u, 68 * u), (38 * u, 30 * u)],
              fill=color)
    # fins
    d.polygon([(38 * u, 60 * u), (24 * u, 76 * u), (38 * u, 72 * u)], fill=color)
    d.polygon([(62 * u, 60 * u), (76 * u, 76 * u), (62 * u, 72 * u)], fill=color)
    # flame
    d.polygon([(44 * u, 78 * u), (56 * u, 78 * u), (50 * u, 94 * u)], fill=AMBER)
    layer = layer.rotate(45, resample=Image.BICUBIC, center=(s / 2, s / 2))
    draw._image.paste(layer, (x, y), layer)


def icon_globe(draw, x, y, s, color):
    """Globe with a leaf, inside a s x s box at (x, y)."""
    u = s / 100.0
    cx, cy, r = x + 46 * u, y + 50 * u, 34 * u
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             start=0, end=360, fill=color, width=3)
    # leaf
    draw.pieslice([x + 68 * u, y + 8 * u, x + 96 * u, y + 36 * u],
                  start=270, end=360, fill=GREEN)
    draw.line([x + 70 * u, y + 34 * u, x + 94 * u, y + 10 * u],
              fill=GREEN, width=4)


def icon_plane(draw, x, y, s, color):
    """Airliner in side view, drawn inside a s x s box at (x, y)."""
    u = s / 100.0
    # main wing (down) and rear wing
    draw.polygon([(x + 38 * u, y + 52 * u), (x + 62 * u, y + 52 * u),
                  (x + 54 * u, y + 82 * u), (x + 46 * u, y + 82 * u)],
                 fill=color)
    draw.polygon([(x + 20 * u, y + 52 * u), (x + 30 * u, y + 52 * u),
                  (x + 26 * u, y + 68 * u), (x + 20 * u, y + 68 * u)],
                 fill=color)
    # tail fin
    draw.polygon([(x + 14 * u, y + 46 * u), (x + 22 * u, y + 26 * u),
                  (x + 30 * u, y + 46 * u)], fill=color)
    # fuselage and nose
    draw.ellipse([x + 12 * u, y + 42 * u, x + 86 * u, y + 58 * u], fill=color)
    draw.polygon([(x + 80 * u, y + 44 * u), (x + 97 * u, y + 50 * u),
                  (x + 80 * u, y + 56 * u)], fill=color)
    # windows
    draw.rectangle([x + 56 * u, y + 46 * u, x + 72 * u, y + 50 * u],
                   fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
def card(draw, x, y, w, h, accent, tag, headline, body, icon_fn, icon_color):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD, outline=BORDER, width=2)
    draw.rounded_rectangle([x, y, x + w, y + 7], radius=3, fill=accent)
    pad = 18
    draw_chip(draw, x + pad, y + 16, tag, accent)
    if icon_fn is not None:
        icon_fn(draw, x + w - 78, y + 8, 64, icon_color)
    hx = x + pad
    hw = w - 2 * pad
    lines, fnt = fit_lines(draw, headline, bold(26), hw, 3)
    ty = y + 78
    for line in lines:
        draw.text((hx, ty), line, font=fnt, fill=INK)
        ty += fnt.size + 4
    blines = wrap(draw, body, regular(19), w - 2 * pad)
    by = ty + 6
    for line in blines[:3]:
        draw.text((hx, by), line, font=regular(19), fill=MUTED)
        by += 24


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ---- header ------------------------------------------------------
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    draw.text((36, 14), "WEDNESDAY, 18 NOVEMBER 2026", font=bold(46),
              fill=(255, 255, 255))
    draw.text((36, 70), "T H E   W O R L D   I N   O N E   D A Y",
              font=bold(22), fill=(168, 196, 232))
    draw.text((W - 36, 22), "WORLD NEWS", font=bold(24),
              fill=(168, 196, 232), anchor="ra")
    draw.text((W - 36, 56), "6 STORIES + BRIEFS", font=regular(20),
              fill=(168, 196, 232), anchor="ra")

    # ---- lead story --------------------------------------------------
    lx, ly, lw, lh = 36, 128, W - 72, 258
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                           fill=LEAD_BG, outline=(232, 180, 176), width=2)
    draw.rounded_rectangle([lx, ly, lx + lw, ly + 7], radius=3, fill=RED)
    draw_chip(draw, lx + 18, ly + 20, "MIDDLE EAST  ·  LEAD", RED)
    icon_tanker(draw, lx + 20, ly + 62, 170, NAVY)
    tx = lx + 214
    tw = lx + lw - 18 - tx
    lines, fnt = fit_lines(
        draw, "U.S. sinks five Iranian tankers as Iran hits back",
        bold(40), tw, 2)
    ty = ly + 58
    for line in lines:
        draw.text((tx, ty), line, font=fnt, fill=INK)
        ty += fnt.size + 4
    body = ("Washington says it sank five Iranian tankers in the Gulf of "
            "Oman after Iran's Guards twice targeted a U.S. warship. Tehran "
            "says it hit 10 ships near Hormuz and fired missiles at a U.S. "
            "base in Jordan.")
    blines = wrap(draw, body, regular(21), tw)
    by = ty + 8
    for line in blines[:3]:
        draw.text((tx, by), line, font=regular(21), fill=(74, 68, 60))
        by += 28

    # ---- story grid, row 1 -------------------------------------------
    gy1 = 402
    gw = (W - 72 - 2 * 16) // 3
    gh = 250
    card(draw, 36, gy1, gw, gh, BLUE, "EUROPE",
         "Ukraine hits Kerch Bridge for a second night",
         "Kyiv strikes the Crimea bridge again; Russia hits Ukrainian "
         "bridges in reply.",
         icon_bridge, BLUE)
    card(draw, 36 + gw + 16, gy1, gw, gh, TEAL, "GAZA",
         "U.N. warns of more cold deaths in Gaza",
         "Winter sets in for 1.7m displaced people; four nations urge "
         "Israel to open aid.",
         icon_tent_snow, TEAL)
    card(draw, 36 + 2 * (gw + 16), gy1, gw, gh, AMBER, "ASIA-PACIFIC",
         "North Korea fires missile into the sea",
         "Pyongyang launches a ballistic missile towards the Sea of Japan "
         "after allied drills.",
         icon_missile, AMBER)

    # ---- story grid, row 2 -------------------------------------------
    gy2 = 668
    card(draw, 36, gy2, gw, gh, GREEN, "CLIMATE",
         "COP31 climate talks enter final stretch",
         "Negotiators in Antalya work through a draft deal with 144 "
         "disputed items.",
         icon_globe, GREEN)
    card(draw, 36 + gw + 16, gy2, gw, gh, PURPLE, "RUSSIA",
         "19 dead as Russian military plane crashes",
         "An An-12 transport goes down in western Siberia, killing all 19 "
         "aboard.",
         icon_plane, PURPLE)

    # ---- also today ---------------------------------------------------
    ax = 36 + 2 * (gw + 16)
    draw.rounded_rectangle([ax, gy2, ax + gw, gy2 + gh], radius=10,
                           fill=NAVY, outline=NAVY, width=2)
    draw.text((ax + 18, gy2 + 16), "ALSO TODAY", font=bold(22),
              fill=(255, 255, 255))
    briefs = [
        ("Israel: ", "Herzog asks Eisenkot to form a government."),
        ("Romania: ", "A 5.3-magnitude quake strikes near Buzau; no "
         "casualties reported."),
        ("Europe: ", "A cyber-attack hits supermarket freezers in seven "
         "countries."),
    ]
    by = gy2 + 56
    for lead, rest in briefs:
        text = lead + rest
        lines = wrap(draw, text, regular(19), gw - 36)
        # bold lead-in on the first line
        draw.text((ax + 18, by), "•  " + lead, font=bold(19),
                  fill=(255, 214, 130))
        lx0 = ax + 18 + draw.textlength("•  " + lead, font=bold(19))
        first = lines[0][len(lead):]
        draw.text((lx0, by), first, font=regular(19), fill=(235, 235, 235))
        by += 25
        for line in lines[1:2]:
            draw.text((ax + 18, by), line, font=regular(19),
                      fill=(235, 235, 235))
            by += 25
        by += 10

    # ---- footer --------------------------------------------------------
    fy = 934
    draw.line([36, fy, W - 36, fy], fill=BORDER, width=2)
    src = ("Sources: News Trend Today morning roundup; Nexus Europa (BBC, "
           "France 24, The Guardian); The Paris Eye; The Munich Eye; "
           "Daily Baku; Jagran Josh.")
    sy = fy + 10
    for line in wrap(draw, src, regular(17), W - 72):
        draw.text((36, sy), line, font=regular(17), fill=MUTED)
        sy += 23
    draw.text(
        (36, sy + 6),
        "Every event above happened, or was first reported, on Wednesday "
        "18 November 2026. Compiled from same-day reporting.",
        font=regular(17), fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
