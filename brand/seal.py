#!/usr/bin/env python3
"""Compose a circular seal around the generated centre device.

Layout follows the classic pattern: Latin motto on the top arc, the same
thing in English on the bottom arc, and the handle small on an inner curve.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

SRC   = '/Users/skyler/Desktop/55ADEB61-4EF0-422C-A9BC-6FFCC2D22DCE.png'
FONT  = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
OUT   = '/Users/skyler/Mr-Pythoneer.github.io/brand'

S     = 2048          # master canvas
C     = S / 2
GOLD  = (255, 191, 0)
BG    = (0, 0, 0)

# measured from the source artwork
CCX, CCY  = 1017.5, 995.0     # centre of the visible device
CONTENT_R = 691.0             # its max radius from that centre

# ring geometry
R_OUT1, W_OUT1 = 990, 13
R_OUT2, W_OUT2 = 950, 5
R_TEXT         = 866          # motto band, top and bottom
R_IN1,  W_IN1  = 776, 7
R_IN2,  W_IN2  = 754, 3
R_NAME         = 690          # handle, on the inner curve
R_CLIP         = 736


def arc_text(im, text, radius, font, top=True, spacing=0.0):
    """Set text along a circular arc, glyphs upright and tangent to the curve."""
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
        g   = Image.new('RGBA', (int(w) + pad * 2, int(font.size * 2) + pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((g.width / 2, g.height / 2), ch, font=font,
                               fill=GOLD + (255,), anchor='mm')

        deg = math.degrees(a)
        g   = g.rotate((-deg - 90) if top else (-deg + 90),
                       resample=Image.BICUBIC, expand=True)

        px = C + radius * math.cos(a)
        py = C + radius * math.sin(a)
        im.paste(g, (int(px - g.width / 2), int(py - g.height / 2)), g)

        ang += step_dir * (adv + spacing / radius)


def star(d, angle_deg, radius, size):
    """Four-pointed sparkle, used to separate the two motto arcs."""
    a  = math.radians(angle_deg)
    cx, cy = C + radius * math.cos(a), C + radius * math.sin(a)
    waist = size * 0.30
    pts = []
    for i in range(4):
        t  = math.radians(i * 90)
        t2 = math.radians(i * 90 + 45)
        pts.append((cx + size * math.cos(t),  cy + size * math.sin(t)))
        pts.append((cx + waist * math.cos(t2), cy + waist * math.sin(t2)))
    d.polygon(pts, fill=GOLD)


def build(out_name, top_text, bottom_text, name_text=None,
          dilate=0, boost=1.0, target_r=636, sizes=(1024, 460, 128, 40)):
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
    for r, w in ((R_OUT1, W_OUT1), (R_OUT2, W_OUT2), (R_IN1, W_IN1), (R_IN2, W_IN2)):
        d.ellipse([C - r, C - r, C + r, C + r], outline=GOLD, width=w)

    arc_text(im, top_text, R_TEXT, ImageFont.truetype(FONT, 116), top=True,  spacing=40)
    arc_text(im, bottom_text, R_TEXT, ImageFont.truetype(FONT, 104), top=False, spacing=46)

    # sparkles sit due east and west, dividing the two motto arcs
    star(d,   0, R_TEXT, 30)
    star(d, 180, R_TEXT, 30)

    if name_text:
        arc_text(im, name_text, R_NAME, ImageFont.truetype(FONT, 48), top=False, spacing=24)

    im.save(f'{OUT}/{out_name}-2048.png')
    for px in sizes:
        im.resize((px, px), Image.LANCZOS).save(f'{OUT}/{out_name}-{px}.png')
    print('wrote', out_name)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    build('seal', 'NIL NISI OPTIMUM', 'ONLY THE BEST', 'MR-PYTHONEER',
          dilate=7, boost=1.18, target_r=612)
