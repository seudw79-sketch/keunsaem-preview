#!/usr/bin/env python3
"""[초안] 히어로 갤러리 B안 액자 작품 — ksmc31/사진/web/pastor_full.jpg 의 십자가를 사람 없이 정사각으로 잘라 인화지 톤으로."""
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import os
SRC = "/Users/sdw79/SDWjavis/_레포/ksmc31/사진/web/pastor_full.jpg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "art_cross.jpg")
im = Image.open(SRC).convert("RGB")                      # 1400×1050
box = (640, 50, 1140, 550)                               # 500×500 정사각 · 위 천장 몰딩(y<45)·아래 어깨(y>550) 제외
art = im.crop(box)
# 사람(머리) 영역 x640–800,y340–550 → 같은 벽돌 줄(y 동일)의 깨끗한 벽 x1140–1300 에서 복사, 오른쪽 경계 40px 페더
patch = im.crop((1140, 340, 1300, 550))
mask = Image.new("L", patch.size, 255)
for x in range(120, 160):
    for y in range(patch.size[1]):
        mask.putpixel((x, y), int(255 * (160 - x) / 40))
art.paste(patch, (0, 290), mask)
art = art.resize((1000, 1000), Image.LANCZOS)
g = ImageOps.grayscale(art)
g = ImageOps.autocontrast(g, cutoff=1)
toned = ImageOps.colorize(g, black=(34, 32, 28), white=(247, 244, 236), mid=(150, 138, 120))
toned = Image.blend(toned, art, 0.18)
toned = ImageEnhance.Contrast(toned).enhance(1.04)
toned.save(OUT, "JPEG", quality=84, optimize=True, progressive=True)
print(OUT, toned.size, os.path.getsize(OUT))
