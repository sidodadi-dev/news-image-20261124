#!/usr/bin/env python3
"""Draw the front-page poster for Tuesday 24 November 2026.

One image, 1024x1024, built only with Pillow and the fonts on this
machine. Every picture element (chart, mountains, seismograph trace)
is drawn in code; all text is wrapped to fit its box.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 242, 228)
INK = (28, 43, 69)
RUST = (179, 64, 42)
TEAL = (15, 118, 110)
GREEN = (29, 122, 61)
OCHRE = (169, 122, 20)
MUTED = (96, 104, 116)
PANEL = (255, 252, 244)
LINE = (28, 43, 69)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    """Draw a wrapped paragraph; return the y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text, color):
    f = font(SANS_B, 19)
    draw.text((x, y), text, font=f, fill=color)
    return y + 26


def rising_chart(draw, x0, y0, x1, y1):
    """A small rising market chart: grid, area fill, line, dots."""
    draw.rectangle([x0, y0, x1, y1], fill=(235, 240, 232), outline=LINE, width=2)
    for i in range(1, 4):
        gy = y0 + (y1 - y0) * i // 4
        draw.line([(x0 + 6, gy), (x1 - 6, gy)], fill=(200, 208, 196), width=1)
    pts = [
        (x0 + 14, y1 - 34),
        (x0 + 58, y1 - 52),
        (x0 + 102, y1 - 44),
        (x0 + 146, y1 - 74),
        (x0 + 190, y1 - 66),
        (x0 + 234, y1 - 104),
        (x0 + 278, y1 - 96),
        (x0 + 318, y1 - 138),
    ]
    area = pts + [(x0 + 318, y1 - 8), (x0 + 14, y1 - 8)]
    draw.polygon(area, fill=(168, 205, 178))
    draw.line(pts, fill=GREEN, width=5, joint="curve")
    for px, py in pts[::2]:
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GREEN,
                     outline=PAPER, width=2)
    lab = font(SANS_B, 17)
    draw.text((x0 + 10, y0 + 8), "NIKKEI  +2.7%", font=lab, fill=GREEN)
    draw.text((x1 - 118, y1 - 26), "TUESDAY", font=lab, fill=MUTED)


def mountains(draw, x0, y0, x1, y1):
    """Layered Himalayan ridges with snow caps and a shaking line."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 232, 238), outline=LINE, width=2)
    # far ridge
    draw.polygon([(x0, y1), (x0 + 60, y0 + 62), (x0 + 130, y1)],
                 fill=(158, 172, 190))
    draw.polygon([(x0 + 110, y1), (x0 + 190, y0 + 40), (x0 + 280, y1)],
                 fill=(138, 154, 176))
    # near ridge with snow caps
    draw.polygon([(x0, y1), (x0 + 90, y0 + 84), (x0 + 190, y1)],
                 fill=(84, 102, 128))
    draw.polygon([(x0 + 170, y1), (x0 + 250, y0 + 66), (x0 + 330, y1)],
                 fill=(70, 88, 114))
    draw.polygon([(x0 + 78, y0 + 92), (x0 + 90, y0 + 84), (x0 + 102, y0 + 92),
                  (x0 + 96, y0 + 100), (x0 + 84, y0 + 100)], fill=PAPER)
    draw.polygon([(x0 + 238, y0 + 74), (x0 + 250, y0 + 66), (x0 + 262, y0 + 74),
                  (x0 + 256, y0 + 82), (x0 + 244, y0 + 82)], fill=PAPER)
    # seismograph trace across the bottom
    trace = []
    import math
    for i in range(0, 321, 4):
        amp = 2 if i < 120 or i > 210 else 8
        ty = y1 - 22 + int(amp * math.sin(i * 0.55))
        trace.append((x0 + i, ty))
    draw.line(trace, fill=RUST, width=3)
    lab = font(SANS_B, 17)
    draw.text((x0 + 10, y0 + 8), "ILAM, EASTERN NEPAL  ·  M5.0", font=lab, fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # margin

    # ---- masthead ----
    d.text((m, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 57), fill=INK)
    d.text((m, 96), "TUESDAY  24  NOVEMBER  2026",
           font=font(SANS_B, 30), fill=RUST)
    d.line([(m, 142), (W - m, 142)], fill=INK, width=3)
    d.line([(m, 148), (W - m, 148)], fill=INK, width=1)

    # ---- lead story: markets (dynamic y so nothing overlaps) ----
    y = kicker(d, m, 164, "MARKETS  ·  ASIA AND WALL STREET", TEAL)
    d.text((m, y), "THE AI RALLY ROLLS", font=font(SERIF_B, 44), fill=INK)
    d.text((m, y + 48), "INTO TUESDAY", font=font(SERIF_B, 44), fill=INK)
    rising_chart(d, 636, 190, 988, 382)
    body = ("Wall Street's Monday surge carried into Asia on "
            "Tuesday. Japan's Nikkei rose 2.7% in early trade, "
            "led by chip and metals stocks, after the S&P 500 "
            "jumped 4.7% and the Nasdaq 6.5% on Monday — Nvidia "
            "up 31% as Jensen Huang returned as chief executive.")
    y = para(d, m, y + 104, body, font(SANS, 21), INK, 580, 28)
    body2 = ("The dollar hovered near a 20-month high, and "
             "traders now fully price a quarter-point US rate "
             "rise next month.")
    y = para(d, m, y + 4, body2, font(SANS, 21), INK, 580, 28)

    # number chips under the lead text
    chips = [("NIKKEI", "+2.7%"), ("NASDAQ", "+6.5%"),
             ("S&P 500", "+4.7%"), ("NVIDIA", "+31%")]
    cy = y + 12
    cx = m
    for label, val in chips:
        d.rounded_rectangle([cx, cy, cx + 138, cy + 54], radius=8,
                            fill=PANEL, outline=GREEN, width=2)
        d.text((cx + 12, cy + 6), label, font=font(SANS_B, 14), fill=MUTED)
        d.text((cx + 12, cy + 24), val, font=font(SANS_B, 24), fill=GREEN)
        cx += 150
    d.line([(m, cy + 70), (W - m, cy + 70)], fill=INK, width=2)

    # ---- second story: Nepal quake ----
    y = kicker(d, m, cy + 86, "ASIA  ·  EARTHQUAKE", RUST)
    d.text((m, y), "QUAKE SHAKES", font=font(SERIF_B, 40), fill=INK)
    d.text((m, y + 46), "EASTERN NEPAL", font=font(SERIF_B, 40), fill=INK)
    mountains(d, 636, y - 6, 988, y + 168)
    body3 = ("A magnitude 5.0 earthquake struck Ilam in eastern "
             "Nepal early on Tuesday, at a depth of 10 km. "
             "Tremors were felt across the border in Gangtok "
             "and Siliguri, India. No casualties were reported.")
    y = para(d, m, y + 100, body3, font(SANS, 21), INK, 580, 28)
    d.line([(m, y + 12), (W - m, y + 12)], fill=INK, width=2)

    # ---- numbers strip ----
    y = y + 28
    d.text((m, y), "THE DAY IN NUMBERS", font=font(SANS_B, 19), fill=TEAL)
    nums = [("Dollar index", "104.32"),
            ("Gold", "$3,649  +3.8%"),
            ("Brent crude", "$86.60  -6.4%"),
            ("Bitcoin", "$61,137")]
    nx = m
    for label, val in nums:
        d.text((nx, y + 26), label, font=font(SANS_B, 16), fill=MUTED)
        d.text((nx, y + 48), val, font=font(SANS_B, 24), fill=INK)
        nx += 238
    d.line([(m, y + 82), (W - m, y + 82)], fill=INK, width=2)

    # ---- footer ----
    foot = ("Also today: a magnitude 4.4 quake in the Maluku Sea, "
            "Indonesia.")
    d.text((m, y + 94), foot, font=font(SANS, 17), fill=MUTED)
    d.text((m, y + 118), "Sources: Reuters · Dow Jones · The Hindu "
           "BusinessLine · GEOFON · plainmoney — 24 Nov 2026",
           font=font(SANS, 14), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
