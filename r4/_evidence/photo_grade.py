#!/usr/bin/env python3
"""R4 2차 사진 보정 스크립트 (PIL) — 산출 r4/사진/web/*.jpg 만 페이지가 참조한다.
근거: master R4 2차 방침(2026-09-29) — 히어로=사람 사진 금지·십자가/벽 질감 블러+저채도, 교회소개 1장 저채도 따뜻한 톤,
      갤러리 6장 4:3 동일 크롭+약한 세피아 duotone. 원본 무수정.
"""
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import os, json

SRC = "/Users/sdw79/SDWjavis/_레포/ksmc31/사진/web"
OUT = "/Users/sdw79/SDWjavis/_레포/keunsaem-preview/r4/사진/web"
PAPER = (246, 245, 241)   # tokens.css --p-paper-050 와 동일
INK = (30, 33, 30)
os.makedirs(OUT, exist_ok=True)
rep = {}

def save(im, name, q=82):
    p = os.path.join(OUT, name)
    im.convert("RGB").save(p, "JPEG", quality=q, optimize=True, progressive=True)
    rep[name] = {"size": im.size, "bytes": os.path.getsize(p)}
    return p

# 1) 히어로 질감: pastor_full.jpg 의 십자가·흰 벽돌 벽 영역만 크롭(사람 영역은 같은 벽 패치로 덮음) → 1920×1080 · 블러 · 저채도 · 종이톤
im = Image.open(os.path.join(SRC, "pastor_full.jpg")).convert("RGB")           # 1400×1050
crop = im.crop((600, 0, 1400, 450))                                          # 800×450 (16:9) 십자가 중앙-우측
patch = crop.crop((500, 330, 700, 450))                                      # 오른쪽 아래 평평한 벽
crop.paste(patch, (0, 330))                                                  # 왼쪽 아래(머리 윗부분) 덮기
hero = crop.resize((1920, 1080), Image.LANCZOS)
hero = hero.filter(ImageFilter.GaussianBlur(radius=6))
hero = ImageEnhance.Color(hero).enhance(0.35)
hero = ImageEnhance.Brightness(hero).enhance(1.04)
hero = ImageEnhance.Contrast(hero).enhance(0.92)
hero = Image.blend(hero, Image.new("RGB", hero.size, PAPER), 0.18)          # 종이톤 15~20% 섞기
p = save(hero, "hero_texture.jpg", q=78)
assert os.path.getsize(p) <= 300 * 1024, "히어로 300KB 초과"

# 2) 교회소개 1장: about2 — 채도 낮추고 따뜻한 톤
ab = Image.open(os.path.join(SRC, "about2.jpg")).convert("RGB")             # 1000×750
ab = ImageEnhance.Color(ab).enhance(0.62)
ab = ImageEnhance.Contrast(ab).enhance(1.04)
warm = Image.new("RGB", ab.size, (232, 214, 186))
ab = Image.blend(ab, warm, 0.08)
save(ab, "about.jpg", q=82)

# 3) 갤러리 6장: 4:3 동일 크롭 → 720×540 → 약한 세피아 duotone(저채도)
GALLERY = ["c2a", "c2b", "c4c", "g7", "c4a", "g8"]                           # alt 원문이 있는 사진만(시안E_교회소개·시안E_홈)
for n in GALLERY:
    g = Image.open(os.path.join(SRC, f"{n}.jpg")).convert("RGB")
    w, h = g.size
    tw, th = (w, round(w * 3 / 4)) if w / h >= 4 / 3 else (round(h * 4 / 3), h)
    tw, th = min(tw, w), min(th, h)
    g = g.crop(((w - tw) // 2, (h - th) // 2, (w - tw) // 2 + tw, (h - th) // 2 + th)).resize((720, 540), Image.LANCZOS)
    gray = ImageOps.autocontrast(g.convert("L"), cutoff=1)
    duo = ImageOps.colorize(gray, black=INK, white=PAPER, mid=(150, 138, 118))
    g = Image.blend(duo, g, 0.22)                                            # 원색 22% 만 남김
    save(g, f"tile_{n}.jpg", q=80)

json.dump(rep, open(os.path.join(OUT, "_grade.json"), "w"), ensure_ascii=False, indent=1)
for k, v in rep.items():
    print(f"{k:22s} {v['size']}  {v['bytes']//1024}KB")
