#!/usr/bin/env python3
"""[초안] 홈 히어로 갤러리 3안 생성기 — 본편 r4/index.html 을 복사해 히어로 프레임만 바꾼다(문안 불변).
사용: python3 r4/_drafts/_build.py   → r4/_drafts/hero_gallery_{A,B,C}.html
검사: 생성 후 각 초안의 보이는 글자 = 본편 index 의 보이는 글자 + 초안 표지(제목·하단 알약) 뿐인지 대조(다르면 exit 1).
"""
import re, sys, html
from pathlib import Path

D = Path(__file__).resolve().parent
SRC = (D.parent / "index.html").read_text(encoding="utf-8")

OLD = re.search(r'<div class="hero__frame">\n  <img class="hero__img"[^\n]*\n.*?</div></div>\n</div></section>', SRC, re.S)
if not OLD:
    sys.exit("히어로 프레임 블록을 찾지 못함 — index.html 구조가 바뀌었다")

H1 = '<h1>말씀을 읽고<br>배우고 가르치자</h1>'
SUB = '<p class="hero__sub">기독교대한감리회 큰샘교회는<br>말씀과 기도로 세워지는 공동체입니다.</p>'
LINKS = '<div class="hero__links"><a class="btn" href="#worship">예배안내 ↓</a><a class="btn" href="#location">오시는 길 ↓</a><a class="btn btn--primary" href="../새가족.html">새가족 안내 →</a></div>'
LABEL = f'<div class="hg-label"><span class="hg-rule" aria-hidden="true"></span>{SUB}\n  {LINKS}</div>'

VARIANTS = {
    "A": ("화이트 큐브", "hg hg-a",
          f'<div class="hero__frame">\n  <span class="hg-floor" aria-hidden="true"></span>\n  <div class="hero__lockup">{H1}</div>\n  {LABEL}\n</div></section>'),
    "B": ("액자 전시", "hg hg-b",
          f'<div class="hero__frame">\n  <figure class="hg-art"><img src="img/art_cross.jpg" alt="" width="1000" height="1000" fetchpriority="high"></figure>\n  <div class="hero__lockup">{H1}\n  {LABEL}</div>\n</div></section>'),
    "C": ("야간 전시관", "hg hg-c",
          f'<div class="hero__frame">\n  <div class="hero__lockup">{H1}</div>\n  {LABEL}\n</div></section>'),
}

def rel(s):
    return re.sub(r'\b(href|src)="(?!https?:|#|mailto:|tel:|data:|/|\.\./)([^"]+)"', r'\1="../\2"', s)

def visible(s):
    s = re.sub(r"<(script|style|title)\b.*?</\1>", " ", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r'<div class="hg-badge".*?</div>', " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

base_text = visible(SRC)
fail = 0
for k, (name, cls, frame) in VARIANTS.items():
    out = rel(SRC[:OLD.start()]) + frame + rel(SRC[OLD.end():])
    out = out.replace('<section id="home" class="hero"', f'<section id="home" class="hero {cls.split()[1]}"', 1)
    out = out.replace("<body>", f'<body class="{cls.split()[0]}">', 1)
    out = out.replace("<title>큰샘교회</title>", f"<title>[초안] 히어로 {k} · {name} — 큰샘교회</title>", 1)
    out = out.replace('<link rel="canonical" href="https://ksmc31.kr/">', '<meta name="robots" content="noindex"><link rel="canonical" href="https://ksmc31.kr/">', 1)
    out = out.replace('<link rel="stylesheet" href="../assets/r4.css">',
                      '<link rel="stylesheet" href="../assets/r4.css">\n<!-- [초안] 오너 수정 #1-(2) 2026-09-30 · 문안=본편 index 그대로 · 벽/빛/배치만 다름 · 스타일=hero_gallery.css -->\n<link rel="stylesheet" href="hero_gallery.css">', 1)
    nav = " · ".join(f'<a href="hero_gallery_{x}.html"{" aria-current=\"page\"" if x == k else ""}>{x} {VARIANTS[x][0]}</a>' for x in VARIANTS)
    badge = f'<div class="hg-badge" role="note">[초안] 홈 히어로 {k}안 — {nav} · <a href="hero_gallery_모음.html">비교 모음</a> · <a href="../index.html">현재 본편</a></div>'
    out = out.replace("</body>", badge + "\n</body>", 1)
    (D / f"hero_gallery_{k}.html").write_text(out, encoding="utf-8")
    t = visible(out)
    ok = t == base_text
    fail += not ok
    print(f"hero_gallery_{k}.html  문안 동일={ok}  bytes={len(out.encode())}")
    if not ok:
        import difflib
        for l in difflib.unified_diff(base_text.split(" "), t.split(" "), lineterm="", n=2):
            print("   ", l)
sys.exit(1 if fail else 0)
