#!/usr/bin/env python3
"""[초안] T-HOME-PHOTO 비교 페이지 생성 — selected.json(Commons 원본 메타데이터) → r4/drafts/photo_후보.html"""
import json, html, re
from pathlib import Path

D = Path(__file__).resolve().parent
sel = json.load(open(D / "selected.json", encoding="utf-8"))
by = {i["sheet_key"]: i for i in sel}
THEMES = [
    ("wilderness", "광야와 길", "사막의 능선·마른 들길 — 광야를 지나는 백성의 길"),
    ("dawnfield", "새벽·해질녘 빛 드는 들판", "안개 낀 새벽 들판과 나무 사이로 드는 빛"),
    ("harvest", "밀밭·포도원·올리브나무", "익은 밀밭, 오래된 올리브 숲, 포도원 언덕"),
    ("water", "물가·바다·배", "고요한 호수의 작은 배, 갈릴리 바닷가"),
    ("bible", "펼친 성경과 빛", "펼친 성경과 촛불·창빛"),
    ("stone", "돌벽·돌길·고대 유적", "돌담이 이어지는 골짜기, 옛 돌기둥"),
    ("sheep", "양떼·목자", "안개 속 양떼, 먼지 길을 걷는 양떼와 목자"),
]
HEROES = [
    ("dawnfield:2", "img/hero_1.jpg", "light hp--strong", "center 62%", "새벽 안개 들판", "하늘이 넓게 비어 있어 표어가 가장 편하게 읽힙니다. 안개·새떼·홀로 선 나무 — 조용한 전시 사진 같은 느낌."),
    ("water:35", "img/hero_2.jpg", "light hp--low", "center 55%", "안개 낀 호숫가", "옅은 회청색 물과 금빛 갈대. 색이 적고 여백이 많아 가장 ‘깔끔’합니다. 풍경을 가리지 않도록 글자를 아래쪽 잔잔한 물 위에 두었습니다."),
    ("dawnfield:9", "img/hero_3.jpg", "dark", "center 45%", "빛이 드는 길", "나무 사이로 빛이 쏟아지는 길 — ‘말씀의 빛’이 가장 직접적으로 느껴집니다. 어두운 사진이라 글자를 밝게 바꿨습니다."),
]

def esc(s): return html.escape(s or "", quote=True)
def artist(it):
    a = re.sub(r"\s+", " ", it["artist"]).strip()
    return a if len(a) <= 70 else a[:68] + "…"
def lic_note(l):
    if l.startswith("CC BY-SA"): return "상업 이용 가능 · 작가·라이선스 표기 필요 · 사진을 고쳐 쓰면 같은 라이선스로 공개"
    if l.startswith("CC BY"): return "상업 이용 가능 · 작가·라이선스 표기 필요"
    if l.startswith("CC0") or l.lower().startswith("public domain") or l.startswith("PD"): return "상업 이용 가능 · 표기 의무 없음(퍼블릭 도메인)"
    return "라이선스 확인 필요"
def tier(it): return {"featured": "Commons 추천 사진(Featured)", "quality": "Commons 우수 사진(Quality)"}.get(it["tier"], "일반 등록 사진")
def credit(it):
    lu = f' <a href="{esc(it["license_url"])}" target="_blank" rel="noopener">{esc(it["license"])}</a>' if it["license_url"] else f' {esc(it["license"])}'
    return (f'<p class="c-who">{esc(artist(it))}</p>'
            f'<p class="c-lic">{lu} — {esc(lic_note(it["license"]))}</p>'
            f'<p class="c-src">원본 {it["w"]}×{it["h"]} · {esc(tier(it))} · <a href="{esc(it["page"])}" target="_blank" rel="noopener">출처 페이지 ↗</a></p>')

heroes = []
for n, (k, img, tone, pos, name, why) in enumerate(HEROES, 1):
    it = by[k]
    heroes.append(f'''
<section class="hp hp--{tone}" aria-labelledby="hp{n}">
  <img class="hp__img" src="photo/{img}" alt="" style="object-position:{pos}" {'fetchpriority="high"' if n == 1 else 'loading="lazy"'}>
  <div class="hp__lockup"><h1 id="hp{n}">말씀을 읽고<br>배우고 가르치자</h1>
    <p class="hp__sub">말씀과 기도로 세워지는 공동체입니다.</p>
    <div class="hp__links"><a class="btn" href="../index.html#worship">예배안내 ↓</a><a class="btn" href="../index.html#location">오시는 길 ↓</a><a class="btn btn--primary" href="../새가족.html">새가족 안내 →</a></div></div>
  <span class="hp__tag">미리보기 {n} · {esc(name)}</span>
</section>
<div class="hp-note"><div class="wrap-n"><p><b>미리보기 {n} · {esc(name)}</b> — {esc(why)}</p>{credit(it)}</div></div>''')

grids = []
for key, label, blurb in THEMES:
    items = [i for i in sel if i["show_theme"] == key]
    cards = "\n".join(f'''    <figure class="pc"><a href="photo/{esc(i["local"])}" target="_blank" rel="noopener"><img src="photo/{esc(i["local"])}" alt="" loading="lazy"></a>
      <figcaption>{credit(i)}</figcaption></figure>''' for i in items)
    grids.append(f'''<section class="theme"><div class="wrap-w">
  <h2>{esc(label)} <span>{len(items)}장</span></h2><p class="blurb">{esc(blurb)}</p>
  <div class="pg">
{cards}
  </div></div></section>''')

n_total = len(sel)
lic_count = {}
for i in sel: lic_count[i["license"]] = lic_count.get(i["license"], 0) + 1
lic_line = " · ".join(f"{k} {v}장" for k, v in sorted(lic_count.items(), key=lambda x: -x[1]))

page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>[초안] 첫 화면 사진 후보 — 성경적 풍경</title>
<meta name="robots" content="noindex">
<!-- [초안] T-HOME-PHOTO 2026-09-30 · 생성=photo/_page.py · 사진 메타데이터=photo/selected.json(Wikimedia Commons API 원본) · AI 생성 이미지 0 · 본편 무수정 -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="../assets/tokens.css"><link rel="stylesheet" href="../assets/r4.css">
<style>
  :root{{
    --p-veil-light-top: rgba(246,245,241,.10);
    --p-veil-light-mid: rgba(246,245,241,.46);
    --p-veil-light-strong: rgba(246,245,241,.66);
    --p-veil-dark-top: rgba(18,20,18,.18);
    --p-veil-dark-mid: rgba(18,20,18,.50);
  }}
  body{{word-break:keep-all}}
  .intro,.wrap-n{{max-width:var(--wrap-narrow);margin:0 auto;padding-inline:var(--gutter)}}
  .intro{{padding-block:var(--s-8) var(--s-5)}}
  .intro .tag{{font-size:var(--text-caption);letter-spacing:var(--tracking-wide);font-weight:600;color:var(--accent)}}
  .intro h1{{font:500 var(--text-h1)/var(--lh-heading) var(--font-serif);color:var(--heading);margin:var(--s-1) 0 var(--s-3)}}
  .intro p,.intro li{{font-size:var(--text-body-sm)}}
  .box{{background:var(--surface);border:1px solid var(--line-light);padding:var(--s-2) var(--s-3);margin-top:var(--s-3)}}
  .sec-h{{max-width:var(--wrap);margin:var(--s-8) auto var(--s-3);padding-inline:var(--gutter);font:500 var(--text-h2)/1.3 var(--font-serif);color:var(--heading)}}
  .hp{{position:relative;min-height:clamp(560px,86svh,860px);display:grid;place-items:center;text-align:center;overflow:hidden;isolation:isolate}}
  .hp__img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2}}
  .hp::after{{content:"";position:absolute;inset:0;z-index:-1}}
  .hp--light::after{{background:linear-gradient(180deg,var(--p-veil-light-top),var(--p-veil-light-mid) 45%,var(--p-veil-light-top))}}
  .hp--strong::after{{background:linear-gradient(180deg,var(--p-veil-light-top),var(--p-veil-light-strong) 42%,var(--p-veil-light-strong) 62%,var(--p-veil-light-top))}}
  .hp--low{{place-items:end center}}
  .hp--low .hp__lockup{{padding-bottom:clamp(20px,3vh,40px)}}
  .hp--low::after{{background:linear-gradient(180deg,var(--p-veil-light-top) 0%,var(--p-veil-light-top) 45%,var(--p-veil-light-strong) 100%)}}
  .hp--dark::after{{background:linear-gradient(180deg,var(--p-veil-dark-top),var(--p-veil-dark-mid) 45%,var(--p-veil-dark-top))}}
  .hp__lockup{{padding:var(--s-12) var(--gutter);max-width:900px}}
  .hp h1{{font-family:var(--font-serif);font-weight:500;font-size:clamp(2.4rem,6vw,4.6rem);line-height:var(--lh-tight);letter-spacing:var(--tracking-tight);color:var(--ink)}}
  .hp__sub{{margin:var(--s-3) auto 0;font-family:var(--font-serif);font-size:var(--fs-1);color:var(--body)}}
  .hp__links{{display:flex;justify-content:center;gap:var(--s-2);flex-wrap:wrap;margin-top:var(--s-5)}}
  .hp--light .btn:not(.btn--primary){{background:var(--nav-glass)}}
  .hp--dark h1,.hp--dark .hp__sub{{color:var(--surface)}}
  .hp--dark .btn:not(.btn--primary){{color:var(--surface);border-color:color-mix(in srgb,var(--surface) 55%,transparent)}}
  .hp__tag{{position:absolute;left:var(--s-2);top:var(--s-2);padding:4px 10px;border-radius:var(--radius-pill);background:var(--button);color:var(--on-button);font:600 12px/1.5 var(--font-sans)}}
  .hp-note{{background:var(--surface);border-bottom:1px solid var(--line-light);padding-block:var(--s-2) var(--s-3)}}
  .hp-note p,.pc figcaption p{{margin:2px 0;font-size:13px;color:var(--muted)}}
  .hp-note p:first-child{{color:var(--body);font-size:var(--text-body-sm)}}
  .c-who{{color:var(--ink)!important;font-weight:600}}
  .theme{{padding-block:var(--s-6);border-top:1px solid var(--line)}}
  .wrap-w{{max-width:var(--wrap);margin:0 auto;padding-inline:var(--gutter)}}
  .theme h2{{font:500 var(--text-h2)/1.3 var(--font-serif);color:var(--heading);margin:0}}
  .theme h2 span{{font:600 var(--text-caption)/1 var(--font-sans);color:var(--gold);letter-spacing:var(--tracking-wide);margin-left:8px}}
  .blurb{{margin:4px 0 var(--s-3);font-size:var(--text-body-sm);color:var(--muted)}}
  .pg{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--s-4) var(--s-3)}}
  .pc{{margin:0}}
  .pc img{{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;background:var(--surface-tint)}}
  .pc figcaption{{padding-top:10px}}
  .pc a{{color:var(--accent)}}
  @media (max-width:640px){{.pg{{grid-template-columns:1fr}} .hp h1{{font-size:2.3rem}} .hp__sub{{font-size:16px}}}}
</style>
</head><body>
<header class="intro">
  <span class="tag">[초안] 오너 검토용 · 본편 아님</span>
  <h1>첫 화면 사진 후보 — 성경적 풍경 실사 {n_total}장</h1>
  <p>「성경적인 풍경사진도 좋아, 꼭 우리교회 사진 아니어도 돼」·「만들지는 마」 말씀에 따라, <b>실제 사진만</b>(인공지능으로 만든 그림 0장) 모았습니다. 맨 위 세 장은 지금 표어를 그대로 얹어 첫 화면처럼 보여 드리고, 그 아래에 주제별 후보를 크게 놓았습니다. 사진을 누르면 크게 열립니다.</p>
  <div class="box">
    <p><b>사진을 어디서 가져왔나</b> — 전부 <b>위키미디어 공용(Wikimedia Commons)</b>에서, 그중에서도 사진가들의 심사를 통과한 「추천·우수 사진」 모음에서 골랐습니다(일부 성경 사진만 일반 등록 사진). 작가·라이선스·원본 크기는 각 사진의 원본 페이지 정보를 그대로 받아 적었고, 사진마다 출처 페이지 링크를 달았습니다.</p>
    <p><b>라이선스</b> — {esc(lic_line)}. 모두 <b>상업적 이용이 허락된</b> 라이선스만 남겼습니다. 다만 CC BY / CC BY-SA 사진을 쓰면 홈페이지 어딘가(예: 맨 아래)에 「사진: 작가 이름 / 라이선스」를 한 줄 적어야 합니다.</p>
    <p><b>고른 기준</b> — 가로 2400픽셀 이상 · 가로로 긴 사진 · 얼굴이 크게 나온 사진 제외 · 유명 관광지로 바로 알아보이는 곳 제외 · 색이 과하게 진한 사진 제외(색 진하기를 기계로 재서 상위 25%를 뺌).</p>
    <p class="note"><b>Unsplash·Pexels 는 이번에 빠졌습니다</b> — 두 곳 모두 자동 접속을 막는 확인 화면·열쇠(API 키)가 있어 작가·라이선스를 직접 확인할 수 없었습니다(무료 개발자 키를 발급받으면 같은 방식으로 추가할 수 있습니다).</p>
  </div>
</header>
<h2 class="sec-h">1. 첫 화면에 얹어 본 세 장</h2>
{"".join(heroes)}
<h2 class="sec-h">2. 주제별 후보 (주제마다 4장)</h2>
{"".join(grids)}
<footer class="intro" style="padding-bottom:var(--s-12)"><p class="note">[초안] 2026-09-30 · 사진 원본 정보: <code>r4/drafts/photo/selected.json</code> · 수집 기록: <code>photo/_harvest.py</code>(후보 484장(추천·우수 모음 442 + 성경 일반 검색 42) → 색 진하기 필터 → 눈으로 고름 → 제목·설명 확인으로 랜드마크·성경 아닌 책 제외)</p></footer>
</body></html>
'''
(D.parent / "photo_후보.html").write_text(page, encoding="utf-8")
print("ok", n_total, lic_line)
