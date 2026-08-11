#!/usr/bin/env python3
"""Compose a circular seal around the generated centre device."""
import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

SRC   = '/Users/skyler/Desktop/55ADEB61-4EF0-422C-A9BC-6FFCC2D22DCE.png'
FONT  = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
OUT   = '/Users/skyler/Mr-Pythoneer.github.io/brand'

S     = 2048          # master canvas
C     = S / 2
GOLD  = (255, 191, 0)
BG    = (0, 0, 0)

# measured from the source artwork
CCX, CCY   = 1017.5, 995.0    # centre of the visible device
CONTENT_R  = 691.0            # its max radius from that centre
TARGET_R   = 636.0            # how big we want it inside the seal
SCALE      = TARGET_R / CONTENT_R

# ring geometry
R_OUT1, W_OUT1 = 990, 13
R_OUT2, W_OUT2 = 950, 5
R_TEXT         = 866
R_IN1,  W_IN1  = 776, 7
R_IN2,  W_IN2  = 754, 3
R_CLIP         = 736          # device is masked to this


def arc_text(im, text, radius, font, top=True, spacing=0.0):
    """Set text along a circular arc, glyphs upright and tangent."""
    widths = [font.getlength(ch) for ch in text]
    total  = sum(widths) + spacing * (len(text) - 1)
    span   = total / radius

    if top:
        ang, step_dir = -math.pi / 2 - span / 2, 1
    else:
        ang, step_dir = math.pi / 2 + span / 2, -1

    for ch, w in zip(text, widths):
        adv = w / radius
        a   = ang + step_dir * adv / 2

        pad = 60
        gw  = int(w) + pad * 2
        gh  = int(font.size * 2) + pad * 2
        g   = Image.new('RGBA', (gw, gh), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((gw / 2, gh / 2), ch, font=font,
                               fill=GOLD + (255,), anchor='mm')

        deg = math.degrees(a)
        rot = (-deg - 90) if top else (-deg + 90)
        g   = g.rotate(rot, resample=Image.BICUBIC, expand=True)

        px = C + radius * math.cos(a)
        py = C + radius * math.sin(a)
        im.paste(g, (int(px - g.width / 2), int(py - g.height / 2)), g)

        ang += step_dir * (adv + spacing / radius)


def star(d, angle_deg, radius, size):
    """Four-pointed sparkle centred on the text ring."""
    a  = math.radians(angle_deg)
    cx = C + radius * math.cos(a)
    cy = C + radius * math.sin(a)
    waist = size * 0.30
    pts = []
    for i in range(4):
        t = math.radians(i * 90)
        pts.append((cx + size * math.cos(t), cy + size * math.sin(t)))
        t2 = math.radians(i * 90 + 45)
        pts.append((cx + waist * math.cos(t2), cy + waist * math.sin(t2)))
    d.polygon(pts, fill=GOLD)


def build(bottom_text, out_name, dilate=0, boost=1.0, target_r=TARGET_R, sizes=(460, 128, 40)):
    im  = Image.new('RGB', (S, S), BG)
    src = Image.open(SRC).convert('RGB')

    # Hairline rays disappear when the seal is shrunk to avatar size. Dilating the
    # bright linework first means it survives the downsample instead of turning to mush.
    if dilate:
        src = src.filter(ImageFilter.MaxFilter(dilate))
    if boost != 1.0:
        src = ImageEnhance.Brightness(src).enhance(boost)

    scale = target_r / CONTENT_R

    # --- centre device, scaled and masked into the inner circle ---
    dev   = src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS)
    layer = Image.new('RGB', (S, S), BG)
    layer.paste(dev, (int(round(C - CCX * scale)), int(round(C - CCY * scale))))
    mask = Image.new('L', (S, S), 0)
    ImageDraw.Draw(mask).ellipse([C - R_CLIP, C - R_CLIP, C + R_CLIP, C + R_CLIP], fill=255)
    im.paste(layer, (0, 0), mask)

    d = ImageDraw.Draw(im)

    def ring(r, w):
        d.ellipse([C - r, C - r, C + r, C + r], outline=GOLD, width=w)

    ring(R_OUT1, W_OUT1)
    ring(R_OUT2, W_OUT2)
    ring(R_IN1,  W_IN1)
    ring(R_IN2,  W_IN2)

    font = ImageFont.truetype(FONT, 116)
    arc_text(im, 'NIL NISI OPTIMUM', R_TEXT, font, top=True, spacing=40)

    if bottom_text:
        fb = ImageFont.truetype(FONT, 92)
        arc_text(im, bottom_text, R_TEXT, fb, top=False, spacing=34)
        star(d, 180, R_TEXT, 30)   # west
        star(d,   0, R_TEXT, 30)   # east
    else:
        # 90deg is south in screen coords, so the bottom cluster sits either side of it
        for deg in (68, 90, 112):
            star(d, deg, R_TEXT, 34)

    im.save(f'{OUT}/{out_name}-2048.png')
    for px in sizes:
        im.resize((px, px), Image.LANCZOS).save(f'{OUT}/{out_name}-{px}.png')
    print('wrote', out_name)


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    build(None,           'seal-a')
    build('MR-PYTHONEER', 'seal-b')
    # avatar master: bolder linework so it holds together when GitHub shrinks it
    build('MR-PYTHONEER', 'seal-avatar', dilate=7, boost=1.18, target_r=660)
