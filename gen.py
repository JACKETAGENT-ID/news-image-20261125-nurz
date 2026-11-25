#!/usr/bin/env python3
"""Draw the front page for Wednesday 25 November 2026.

Original broadsheet design drawn with PIL: masthead, dateline, one lead
story with a drawn refinery illustration, story cards, briefs and a
markets ticker. Every story was verified against live reporting of
25 November 2026 before drawing.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (20, 20, 20)
RED = (163, 18, 18)
GREY = (90, 86, 78)
BLUE = (28, 63, 110)
GOLD = (201, 148, 28)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, width, fill=INK, leading=None):
    lh = leading or int(font.size * 1.28)
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def rule(d, x0, x1, y, wdt=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def kicker(d, x, y, text, size=16):
    d.text((x, y), text, font=F(SANS_B, size), fill=RED)
    return y + size + 6


# ---------------------------------------------------------------- icons
def icon_refinery(d, x, y, w, h):
    # dusk sky gradient
    top = (246, 217, 160)
    bot = (232, 155, 77)
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    # pale sun
    d.ellipse([x + w - 92, y + 14, x + w - 32, y + 74], fill=(250, 238, 200))
    # smoke puffs
    for cx, cy, r in [(x + 150, y + 18, 16), (x + 178, y + 8, 20),
                      (x + 210, y + 18, 14), (x + 430, y + 14, 18),
                      (x + 458, y + 6, 15)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 116, 110))
    gy = y + h - 26
    # storage tanks
    for tx in (x + 40, x + 300):
        d.rounded_rectangle([tx, gy - 58, tx + 86, gy], radius=8,
                            fill=(52, 52, 52))
        d.ellipse([tx, gy - 66, tx + 86, gy - 50], fill=(70, 70, 70))
    # distillation towers
    for tx, th in [(x + 150, 96), (x + 205, 118), (x + 420, 104)]:
        d.rectangle([tx, gy - th, tx + 26, gy], fill=(34, 34, 34))
        d.polygon([(tx - 3, gy - th), (tx + 13, gy - th - 18),
                   (tx + 29, gy - th)], fill=(34, 34, 34))
        for wy in range(gy - th + 12, gy - 8, 16):
            d.line([(tx + 4, wy), (tx + 22, wy)], fill=(120, 118, 110),
                   width=2)
    # flare stack with flame
    fx = x + 500
    d.rectangle([fx, gy - 128, fx + 12, gy], fill=(34, 34, 34))
    d.polygon([(fx - 16, gy - 128), (fx + 6, gy - 168), (fx + 28, gy - 128)],
              fill=(230, 120, 20))
    d.polygon([(fx - 7, gy - 128), (fx + 6, gy - 152), (fx + 19, gy - 128)],
              fill=(245, 200, 60))
    # pipes along the ground
    d.line([(x, gy - 6), (x + w, gy - 6)], fill=(34, 34, 34), width=4)
    d.rectangle([x, gy, x + w, y + h], fill=(38, 36, 32))
    d.line([(x, gy), (x + w, gy)], fill=(230, 120, 20), width=3)


def icon_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 231, 240))
    sea = y + h - 26
    d.rectangle([x, sea, x + w, y + h], fill=(43, 108, 176))
    for wx in range(x + 6, x + w, 26):
        d.arc([wx, sea + 6, wx + 22, sea + 20], 180, 360,
              fill=(255, 255, 255), width=3)
    # tanker silhouette
    d.rectangle([x + 18, sea - 18, x + 190, sea], fill=(30, 30, 30))
    for cx, cc in [(x + 30, (163, 18, 18)), (x + 72, (28, 63, 110)),
                   (x + 114, (120, 120, 116)), (x + 150, (201, 148, 28))]:
        d.rectangle([cx, sea - 34, cx + 34, sea - 18], fill=cc)
    d.rectangle([x + 196, sea - 30, x + 214, sea], fill=(30, 30, 30))
    # spiky mine, top right
    mx, my = x + w - 42, y + 18
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 9, 16
        a = math.radians(ang)
        d.line([(mx + r1 * math.cos(a), my + r1 * math.sin(a)),
                (mx + r2 * math.cos(a), my + r2 * math.sin(a))],
               fill=(163, 18, 18), width=3)
    d.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=(163, 18, 18))
    d.text((mx - 3, my - 8), "!", font=F(SANS_B, 14), fill=(255, 255, 255))


def icon_yemen(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    sea = y + h - 16
    d.rectangle([x, sea, x + w, y + h], fill=(43, 108, 176))
    # port cranes
    for cx in (x + 40, x + 150):
        d.rectangle([cx, y + 8, cx + 8, sea], fill=(40, 40, 40))
        d.rectangle([cx, y + 8, cx + 86, y + 16], fill=(40, 40, 40))
        d.line([(cx + 86, y + 16), (cx + 86, y + 32)], fill=(40, 40, 40),
               width=3)
        d.rectangle([cx + 76, y + 32, cx + 96, y + 42], fill=(163, 18, 18))
    # smoke plume over a flare stack
    for cx, cy, r in [(x + 258, y + 12, 10), (x + 276, y + 6, 12),
                      (x + 292, y + 13, 9)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 116, 110))
    d.rectangle([x + 262, y + 24, x + 270, sea], fill=(40, 40, 40))
    d.polygon([(x + 254, y + 24), (x + 266, y + 8), (x + 278, y + 24)],
              fill=(230, 120, 20))


def icon_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    bars = [(20, 46), (62, 58), (104, 38), (146, 66)]
    for bx, bh in bars:
        d.rectangle([x + bx, y + h - 14 - bh, x + bx + 30, y + h - 14],
                    fill=(163, 18, 18))
    d.line([(x + 14, y + 16), (x + 78, y + 44), (x + 132, y + 30),
            (x + 196, y + 62)], fill=(28, 63, 110), width=4)
    d.polygon([(x + 196, y + 62), (x + 182, y + 58), (x + 192, y + 76)],
              fill=(28, 63, 110))
    d.line([(x + 8, y + h - 14), (x + w - 8, y + h - 14)], fill=INK, width=2)


def icon_colombia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    # striped awning
    for i in range(8):
        c = (163, 18, 18) if i % 2 == 0 else (248, 244, 232)
        d.rectangle([x + 12 + i * 26, y + 8, x + 12 + (i + 1) * 26, y + 30],
                    fill=c)
    d.rectangle([x + 12, y + 30, x + w - 12, y + 34], fill=INK)
    d.rectangle([x + 30, y + 34, x + w - 30, y + h - 8],
                outline=INK, width=2, fill=(232, 240, 248))
    d.rectangle([x + 76, y + 44, x + w - 76, y + h - 8], fill=(28, 63, 110))
    ot = "OPEN"
    of = F(SANS_B, 12)
    d.text((x + (w - d.textlength(ot, font=of)) / 2, y + 50), ot, font=of,
           fill=(255, 255, 255))


def icon_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for sx, sy in [(20, 14), (60, 30), (120, 12), (170, 26), (200, 48),
                   (40, 52), (150, 56)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                  fill=(255, 255, 255))
    # rocket, tilted
    d.polygon([(x + 128, y + 8), (x + 148, y + 34), (x + 128, y + 30),
               (x + 108, y + 34)], fill=(230, 120, 20))
    d.polygon([(x + 108, y + 34), (x + 128, y + 8), (x + 148, y + 34),
               (x + 138, y + 58), (x + 118, y + 58)], fill=(240, 240, 240))
    d.ellipse([x + 122, y + 30, x + 134, y + 42], fill=(28, 63, 110))
    d.polygon([(x + 118, y + 58), (x + 128, y + 74), (x + 138, y + 58)],
              fill=(245, 200, 60))
    d.polygon([(x + 108, y + 52), (x + 96, y + 62), (x + 110, y + 60)],
              fill=(163, 18, 18))
    d.polygon([(x + 148, y + 52), (x + 160, y + 62), (x + 146, y + 60)],
              fill=(163, 18, 18))
    d.arc([x + 8, y + h - 26, x + 90, y + h + 22], 270, 360,
          fill=(43, 108, 176), width=6)


def icon_sport(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    cx = x + w // 2
    # trophy
    d.polygon([(cx - 34, y + 10), (cx + 34, y + 10), (cx + 26, y + 40),
               (cx - 26, y + 40)], fill=GOLD)
    d.arc([cx - 52, y + 8, cx - 22, y + 34], 90, 270, fill=GOLD, width=5)
    d.arc([cx + 22, y + 8, cx + 52, y + 34], 270, 90, fill=GOLD, width=5)
    d.rectangle([cx - 6, y + 40, cx + 6, y + 56], fill=GOLD)
    d.rectangle([cx - 24, y + 56, cx + 24, y + 64], fill=GOLD)
    for px, py, pc in [(30, 14, (163, 18, 18)), (190, 18, (28, 63, 110)),
                       (60, 60, (201, 148, 28)), (170, 62, (163, 18, 18))]:
        d.ellipse([x + px, y + py, x + px + 6, y + py + 6], fill=pc)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    R = W - M  # 996

    # masthead
    title = "THE WORLD TODAY"
    tf = F(SERIF_B, 74)
    d.text(((W - d.textlength(title, font=tf)) / 2, 14), title, font=tf,
           fill=INK)
    rule(d, M, R, 106, 3)
    rule(d, M, R, 112, 1)
    # dateline bar
    d.text((M, 120), "WEDNESDAY 25 NOVEMBER 2026", font=F(SANS_B, 23),
           fill=INK)
    rt = "ONE DAY'S WORLD NEWS"
    d.text((R - d.textlength(rt, font=F(SANS, 16)), 126), rt,
           font=F(SANS, 16), fill=GREY)
    rule(d, M, R, 154, 2)

    # ---- lead story (left) ----
    lx, lw = M, 620
    y = kicker(d, lx, 168, "WAR IN UKRAINE  ·  LEAD STORY", 17)
    y = para(d, lx, y + 2, "Putin vows retaliation over refinery strikes",
             F(SERIF_B, 38), lw, leading=46)
    y = para(d, lx, y + 8,
             "Moscow calls its response \u201cinevitable\u201d despite a US call "
             "to stop. Refinery crude runs are down 45% since late October.",
             F(SERIF, 19), lw, leading=25)
    icon_refinery(d, lx, 352, lw, 162)
    para(d, lx, 522,
         "A refinery burns after a drone strike. A Russian strike on "
         "Zaporizhzhia the same day killed two people and wounded over 40.",
         F(SERIF_I, 15), lw, leading=19)

    # divider between lead and right column
    d.line([(660, 162), (660, 556)], fill=GREY, width=1)

    # ---- right column: two cards ----
    def right_card(y0, hgt, icon, kick, title, body):
        d.rectangle([672, y0, R, y0 + hgt], outline=INK, width=2)
        icon(d, 680, y0 + 8, R - 688, 60)
        yy = kicker(d, 684, y0 + 76, kick, 15)
        yy = para(d, 684, yy, title, F(SERIF_B, 21), R - 696, leading=25)
        para(d, 684, yy + 4, body, F(SANS, 14), R - 696, leading=18)

    right_card(162, 190, icon_hormuz, "STRAIT OF HORMUZ",
               "Tankers \u201chit mines\u201d in the strait, Iran says",
               "Iran says tankers under US escort hit naval mines; the claim "
               "is unconfirmed.")
    right_card(366, 190, icon_yemen, "YEMEN  ·  RED SEA",
               "Coalition strikes Hodeidah port",
               "Coalition strikes followed an evacuation order; the Houthis "
               "threaten Saudi ports.")

    rule(d, M, R, 566, 2)

    # ---- row B: four cards ----
    cards = [
        ("MARKETS", "Nvidia slides 7% as AI doubts hit stocks",
         "Nikkei -2.76%, S&P 500 -0.5% as AI doubts hit stocks.",
         icon_markets),
        ("COLOMBIA", "Hostages freed in Cartagena siege",
         "Armed men held about 20 people; all were freed unharmed.",
         icon_colombia),
        ("SPACE", "Pakistan's first astronaut reaches China's station",
         "Zeeshan Ali flew aboard Shenzhou-24 to the station.",
         icon_space),
        ("SPORT", "Senegal regain Africa Cup title",
         "CAS returned the CAN-2025 crown, ten months after the final.",
         icon_sport),
    ]
    cw, gap = 232, 12
    for i, (kick, title, body, icon) in enumerate(cards):
        cx = M + i * (cw + gap)
        d.rectangle([cx, 576, cx + cw, 786], outline=INK, width=2)
        icon(d, cx + 8, 584, cw - 16, 60)
        yy = kicker(d, cx + 10, 650, kick, 14)
        yy = para(d, cx + 10, yy, title, F(SERIF_B, 19), cw - 20, leading=22)
        para(d, cx + 10, yy + 3, body, F(SANS, 14), cw - 20, leading=17)

    rule(d, M, R, 796, 2)

    # ---- row C: three briefs ----
    briefs = [
        ("UNITED STATES", "Huawei convicted in US trade-secret case",
         "A jury found the firm guilty in a sanctions and trade-secret trial."),
        ("BANGLADESH", "Textile wage up 36% after protests",
         "Workers win a 36% minimum-wage rise after weeks of protests over "
         "living costs."),
        ("INDONESIA", "Dozens trapped in Indonesian mine",
         "Rescuers search for miners trapped 100 metres down after heavy "
         "rains."),
    ]
    bw = 316
    for i, (kick, title, body) in enumerate(briefs):
        bx = M + i * (bw + 12)
        d.rectangle([bx, 806, bx + bw, 918], outline=INK, width=2)
        yy = kicker(d, bx + 10, 814, kick, 14)
        yy = para(d, bx + 10, yy, title, F(SERIF_B, 19), bw - 20, leading=23)
        para(d, bx + 10, yy + 3, body, F(SANS, 14), bw - 20, leading=18)

    # ---- markets ticker ----
    d.rectangle([M, 932, R, 970], fill=INK)
    tick = ("MARKETS   Nikkei -2.76%    S&P 500 -0.50%    FTSE 100 -0.13%    "
            "Brent $87.49    Sensex +1.8%")
    d.text((M + 12, 941), tick, font=F(SANS_B, 17), fill=(248, 244, 232))

    # ---- footer ----
    foot = ("All stories as reported on Wednesday 25 November 2026  ·  "
            "Reuters · Xinhua · Al Jazeera · CNBC · Kyiv Independent")
    ff = F(SANS, 13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 982), foot, font=ff,
           fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("saved", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
