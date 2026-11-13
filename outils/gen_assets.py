"""Visuels de la présentation « Document sécurisé » (guillochés, rosace, puce).
Usage : python outils/gen_assets.py  -> presentation/assets/*.png
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "presentation", "assets")
os.makedirs(OUT, exist_ok=True)

W, H = 1920, 1080
SS = 2  # supersampling
NAVY = (11, 31, 58)
NAVY2 = (19, 42, 79)
GOLD = (201, 162, 39)
GREEN = (46, 139, 110)
LIGHT = (247, 248, 250)


def guilloche_band(draw, cx, cy, rx, ry, n_curves, color, width, a=7, b=3, phase=0.0, k=0.22):
    """Famille de courbes (hypotrochoïdes aplaties) autour de (cx, cy)."""
    for i in range(n_curves):
        ph = phase + i * 2 * math.pi / n_curves
        pts = []
        for s in range(0, 1441):
            t = s * 2 * math.pi / 1440
            r = 1 + k * math.cos(a * t + ph)
            x = cx + rx * r * math.cos(t + ph * 0.1)
            y = cy + ry * r * math.sin(b * t / b + ph * 0.1)
            pts.append((x, y))
        draw.line(pts, fill=color, width=width)


def rosette(size=900, color=GOLD, bg=None, n=48):
    img = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = size * SS / 2
    for ring, (rx, ry, k, a, alpha) in enumerate([(0.46, 0.46, 0.12, 12, 150), (0.36, 0.36, 0.18, 8, 170), (0.24, 0.24, 0.25, 6, 190), (0.12, 0.12, 0.35, 5, 210)]):
        for i in range(n):
            ph = i * 2 * math.pi / n
            pts = []
            for s in range(0, 721):
                t = s * 2 * math.pi / 720
                r = 1 + k * math.cos(a * t)
                ang = t + ph
                pts.append((c + c * rx * r * math.cos(ang) * (1 + 0.08 * math.cos(3 * t)),
                            c + c * ry * r * math.sin(ang)))
            d.line(pts, fill=color + (alpha,), width=SS)
    d.ellipse([c - c * 0.5, c - c * 0.5, c + c * 0.5, c + c * 0.5], outline=color + (200,), width=SS * 2)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(os.path.join(OUT, "rosette.png"))


def bg_dark():
    img = Image.new("RGB", (W * SS, H * SS), NAVY)
    # dégradé radial léger (vignette inversée au centre gauche)
    yy, xx = np.mgrid[0:H * SS, 0:W * SS]
    dist = np.sqrt(((xx - W * SS * 0.35) / (W * SS)) ** 2 + ((yy - H * SS * 0.45) / (H * SS)) ** 2)
    g = np.clip(1 - dist * 1.1, 0, 1)[..., None]
    arr = np.array(img).astype(np.float32)
    arr = arr * (1 - 0.35 * g) + np.array(NAVY2, dtype=np.float32) * (0.35 * g)
    img = Image.fromarray(arr.astype(np.uint8))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # bandes guillochées en bas à droite et en haut à gauche
    guilloche_band(d, W * SS * 1.05, H * SS * 1.1, W * SS * 0.55, H * SS * 0.75, 34, GOLD + (46,), SS, a=9, k=0.16)
    guilloche_band(d, -W * SS * 0.1, -H * SS * 0.25, W * SS * 0.5, H * SS * 0.6, 28, GREEN + (40,), SS, a=7, k=0.2, phase=0.7)
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    img = img.resize((W, H), Image.LANCZOS)
    img.save(os.path.join(OUT, "bg_dark.png"), optimize=True)


def bg_light():
    img = Image.new("RGB", (W * SS, H * SS), LIGHT)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    guilloche_band(d, W * SS * 1.08, -H * SS * 0.15, W * SS * 0.42, H * SS * 0.7, 26, NAVY + (22,), SS, a=8, k=0.18)
    guilloche_band(d, -W * SS * 0.12, H * SS * 1.12, W * SS * 0.35, H * SS * 0.5, 20, GOLD + (34,), SS, a=6, k=0.22, phase=1.3)
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    img = img.resize((W, H), Image.LANCZOS)
    img.save(os.path.join(OUT, "bg_light.png"), optimize=True)


def chip(size=(320, 240), color=GOLD, name="chip.png"):
    w, h = size[0] * SS, size[1] * SS
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = 36 * SS
    d.rounded_rectangle([4, 4, w - 4, h - 4], radius=r, fill=color + (255,), outline=(120, 95, 20, 255), width=3 * SS)
    line = (120, 95, 20, 255)
    lw = 4 * SS
    # motif de contacts de puce
    d.rounded_rectangle([w * 0.3, h * 0.28, w * 0.7, h * 0.72], radius=r // 2, outline=line, width=lw)
    for x in (w * 0.3, w * 0.7):
        d.line([(x, h * 0.5), (0 if x < w / 2 else w, h * 0.5)], fill=line, width=lw)
    for y in (h * 0.28, h * 0.72):
        d.line([(0, y), (w * 0.3, y)], fill=line, width=lw)
        d.line([(w * 0.7, y), (w, y)], fill=line, width=lw)
    d.line([(w * 0.5, 0), (w * 0.5, h * 0.28)], fill=line, width=lw)
    d.line([(w * 0.5, h * 0.72), (w * 0.5, h)], fill=line, width=lw)
    img = img.resize(size, Image.LANCZOS)
    img.save(os.path.join(OUT, name))


def card_frame():
    """Cadre façon carte d'identité (pour la slide de titre)."""
    w, h = 1012 * SS, 638 * SS
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=48 * SS, fill=(19, 42, 79, 235), outline=GOLD + (255,), width=3 * SS)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    guilloche_band(dl, w * 0.78, h * 0.55, w * 0.33, h * 0.42, 30, GOLD + (60,), SS, a=10, k=0.15)
    guilloche_band(dl, w * 0.2, h * 0.9, w * 0.3, h * 0.3, 22, GREEN + (55,), SS, a=7, k=0.2, phase=0.5)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=48 * SS, fill=255)
    layer.putalpha(Image.fromarray(np.minimum(np.array(layer.split()[3]), np.array(mask))))
    img = Image.alpha_composite(img, layer)
    img = img.resize((1012, 638), Image.LANCZOS)
    img.save(os.path.join(OUT, "card_frame.png"))


if __name__ == "__main__":
    bg_dark()
    bg_light()
    rosette()
    chip()
    chip(color=(232, 238, 246), name="chip_light.png")
    card_frame()
    print("assets OK ->", OUT)
