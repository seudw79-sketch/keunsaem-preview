#!/usr/bin/env python3
"""[초안] T-HOME-PHOTO v2 비교 페이지 — selected_v2.json → r4/drafts/photo_후보.html
라이선스 우선순위(master 검수 2026-09-30): CC0·PD > Pexels > CC BY > CC BY-SA(이번 판 0장)."""
import json, html, re
from pathlib import Path

V = Path(__file__).resolve().parent
sel = json.load(open(V / "selected_v2.json", encoding="utf-8"))
by = {i["sheet_key"]: i for i in sel}
THEMES = [
    ("wilderness", "광야와 길"), ("dawnfield", "새벽·해질녘 빛 드는 들판"), ("harvest", "밀밭·포도원·올리브나무"),
    ("water", "물가·바다·배"), ("bible", "펼친 성경과 빛"), ("stone", "돌벽·돌길·고대 유적"), ("sheep", "양떼·목자"),
]
# 이번 주 말씀 값: ksmc31/latest.json(2026-09-27) = r4/index.html 설교 카드와 같은 값
SERMON = {"date": "2026. 9. 27.", "title": "광야에서도 신실하신 하나님", "ref": "민수기 14장 8–9절", "url": "https://www.youtube.com/watch?v=4Uw236eEFuk"}
HEROES = [
    ("commons:free:7", "img/hero_1.jpg", "center 55%", "광야 — 사해 바닷가", "이번 주 설교 「광야에서도 신실하신 하나님」과 그대로 이어집니다. 실제 유대 광야·사해 쪽 풍경."),
    ("pexels:region:8", "img/hero_2.jpg", "center 88%", "갈릴리 호수와 밀밭", "아르벨 언덕에서 내려다본 갈릴리 호수와 들판 — 성경 무대 실제 지역, 가장 밝고 넓은 느낌."),
    ("commons:free:34", "img/hero_3.jpg", "center 50%", "고요한 호숫가의 배", "안개 낀 물가에 매인 작은 배들 — 색이 적고 조용해 ‘전시 사진’에 가장 가깝습니다."),
]

def esc(s): return html.escape(str(s or ""), quote=True)
def who(it):
    a = re.sub(r"\s+", " ", it.get("photographer") or it.get("author") or "").strip()
    return a if len(a) <= 60 else a[:58] + "…"
def lic(it):
    if it["src"] == "pexels":
        return '<a href="https://www.pexels.com/license/" target="_blank" rel="noopener">Pexels 라이선스</a> — 상업 이용 자유 · 출처 표기 의무 없음'
    l = it["license"]
    link = f'<a href="{esc(it["license_url"])}" target="_blank" rel="noopener">{esc(l)}</a>' if it.get("license_url") else esc(l)
    return f"{link} — 상업 이용 자유 · 출처 표기 의무 없음"
def place(it):
    if it["src"] == "pexels": return it.get("location") or ""
    r = it.get("region") or ""
    return "" if r.lower().startswith("other") else r
def size(it): return f'{it.get("orig_w") or it.get("w")}×{it.get("orig_h") or it.get("h")}'
def src_name(it): return "Pexels" if it["src"] == "pexels" else "Wikimedia Commons"
def credit(it):
    p = place(it)
    return (f'<p class="who">{esc(who(it))}{" · " + esc(p) if p else ""}</p>'
            f'<p>{lic(it)}</p>'
            f'<p>원본 {size(it)} · {src_name(it)} · <a href="{esc(it["page_url"])}" target="_blank" rel="noopener">출처 페이지 ↗</a></p>')

heroes = []
for n, (k, img, pos, name, why) in enumerate(HEROES, 1):
    it = by[k]
    heroes.append(f'''
<section class="hv" aria-labelledby="hv{n}">
  <p class="hv__no">미리보기 {n} · {esc(name)}</p>
  <figure class="hv__fig"><img src="photo/v2/{img}" alt="" width="2400" height="1350" style="object-position:{pos}" {'fetchpriority="high"' if n == 1 else 'loading="lazy"'}></figure>
  <div class="hv__cap">
    <div><p class="lbl">이번 주일 · {SERMON["date"]}</p><h2 id="hv{n}">{SERMON["title"]}</h2><p class="ref">{SERMON["ref"]}</p>
      <a class="pill" href="{SERMON["url"]}" target="_blank" rel="noopener">설교 영상 보기 ↗</a></div>
    <p class="hv__credit">사진 · {esc(who(it))} / {"Pexels" if it["src"] == "pexels" else esc(it["license"])}</p>
  </div>
  <div class="hv__why"><p><b>{esc(name)}</b> — {esc(why)}</p>{credit(it)}</div>
</section>''')

grids = []
for key, label in THEMES:
    items = [i for i in sel if i["show_theme"] == key]
    cards = "\n".join(f'''    <figure class="pc"><a href="photo/v2/{esc(i["local"])}" target="_blank" rel="noopener"><img src="photo/v2/{esc(i["local"])}" alt="" loading="lazy"></a><figcaption>{credit(i)}</figcaption></figure>''' for i in items)
    grids.append(f'<section class="th"><h3>{esc(label)} <span>{len(items)}</span></h3><div class="pg">\n{cards}\n</div></section>')

from collections import Counter
cnt = Counter("Pexels" if i["src"] == "pexels" else i["license"] for i in sel)
cnt_line = " · ".join(f"{k} {v}장" for k, v in cnt.most_common())
n_region = sum(1 for i in sel if place(i))

page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>[초안] 사진 후보 v2 — 성경적 풍경</title>
<meta name="robots" content="noindex">
<!-- [초안] T-HOME-PHOTO v2 2026-09-30 · 생성=photo/v2/_page_v2.py · 메타데이터=photo/v2/selected_v2.json(Pexels 사진 페이지·Commons API 원본) · AI 생성 0 · 본편 무수정 -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
  :root{{--bg:#FFFFFF;--ink:#000000;--mute:#6B6B6B;--line:#E4E4E4;--sans:Pretendard,"Apple SD Gothic Neo",system-ui,sans-serif;--serif:"Noto Serif KR",serif;--edge:20px}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.7 var(--sans);word-break:keep-all}}
  a{{color:inherit}}
  .top{{display:flex;justify-content:space-between;align-items:baseline;padding:18px var(--edge);border-bottom:1px solid var(--line)}}
  .logo{{font-weight:500;font-size:16px}}
  .top small{{font-size:13px;color:var(--mute)}}
  .intro{{max-width:760px;margin:0 auto;padding:56px var(--edge) 24px}}
  .intro h1{{font:400 clamp(1.8rem,3.4vw,2.6rem)/1.3 var(--serif);letter-spacing:-.02em;margin:0 0 20px;text-wrap:balance}}
  .intro p,.intro li{{font-size:15px}}
  .intro ul{{padding-left:18px}}
  .sec{{font:400 13px/1 var(--sans);color:var(--mute);letter-spacing:.06em;padding:56px var(--edge) 14px;border-top:1px solid var(--line);margin:40px 0 0}}
  .hv{{padding-bottom:56px}}
  .hv__no{{margin:0;padding:0 var(--edge) 10px;font-size:13px;color:var(--mute)}}
  .hv__fig{{margin:0 var(--edge)}}
  .hv__fig img{{display:block;width:100%;height:min(78svh,62vw);object-fit:cover;border-radius:0}}
  .hv__cap{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;padding:22px var(--edge) 0}}
  .lbl{{margin:0 0 6px;font-size:14px;color:var(--mute)}}
  .hv h2{{margin:0;font:400 clamp(1.9rem,4.2vw,3.4rem)/1.2 var(--serif);letter-spacing:-.02em;text-wrap:balance}}
  .ref{{margin:8px 0 18px;font-size:15px}}
  .pill{{display:inline-block;padding:10px 20px;border:1px solid var(--ink);border-radius:9999px;font-size:14px;text-decoration:none}}
  .pill:hover{{background:var(--ink);color:var(--bg)}}
  .hv__credit{{margin:0;font-size:12px;color:var(--mute);text-align:right}}
  .hv__why{{max-width:760px;margin:28px auto 0;padding:16px var(--edge);border-top:1px solid var(--line)}}
  .hv__why p,.pc p{{margin:2px 0;font-size:13px;color:var(--mute)}}
  .hv__why p:first-child{{font-size:14px;color:var(--ink)}}
  .who{{color:var(--ink)!important;font-weight:500}}
  .th{{padding:40px var(--edge) 8px;border-top:1px solid var(--line)}}
  .th h3{{font:400 1.5rem/1.3 var(--serif);margin:0 0 20px}}
  .th h3 span{{font:400 13px var(--sans);color:var(--mute);margin-left:6px}}
  .pg{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:36px 20px}}
  .pc{{margin:0}} .pc img{{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;background:var(--line)}}
  .pc figcaption{{padding-top:10px}}
  .foot{{padding:48px var(--edge) 80px;font-size:13px;color:var(--mute);border-top:1px solid var(--line)}}
  @media (max-width:640px){{.pg{{grid-template-columns:1fr}} .hv__cap{{flex-direction:column;align-items:flex-start}} .hv__credit{{text-align:left}} .hv__fig img{{height:62svh}}}}
</style>
</head><body>
<header class="top"><span class="logo">큰샘교회</span><small>[초안] 사진 후보 v2 · 오너 검토용</small></header>
<div class="intro">
  <h1>첫 화면 사진 후보 v2 — 성경 무대의 실제 풍경 우선</h1>
  <p>1차 후보를 다시 골랐습니다. <b>조건 없이 쓸 수 있는 사진만</b> 남겼고, <b>이스라엘·요단·갈릴리·유대 광야</b> 같은 성경 무대의 실제 풍경을 먼저 넣었습니다. 인공지능으로 만든 사진은 한 장도 없습니다.</p>
  <ul>
    <li><b>라이선스</b> — {esc(cnt_line)}. 28장 모두 교회 홈페이지에 조건 없이 쓸 수 있고 출처 표기 의무도 없습니다(1차 때 문제였던 ‘CC BY-SA’ 는 0장). 그래도 갤러리식으로 사진 아래 작은 글씨로 사진가 이름을 달면 격이 올라갑니다.</li>
    <li><b>성경 무대 실제 지역</b> — 28장 중 {n_region}장은 촬영지가 사진 페이지에 적혀 있고(이스라엘·요단 등), 나머지는 밀밭·올리브·양떼·물가·펼친 성경처럼 성경 장면과 바로 이어지는 사진입니다.</li>
    <li><b>뺀 것</b> — 나스카 라인·링컨 성경·르네상스 책·화산동굴·태국 호수(1차), 그리고 제목에 「요단 느보산」이라 적혔지만 실제로는 미국 아칸소주 느보산인 사진 2장, 작가가 확인되지 않는 사진 1장.</li>
    <li><b>Unsplash</b> 는 자동 접속 차단(사람 확인 화면)으로 이번에도 확인할 수 없었습니다. <b>Pexels</b> 는 사진 페이지에서 사진가 이름을 직접 확인했습니다.</li>
    <li><b>미리보기 3장</b>은 새 첫 화면 규격대로 만들었습니다 — 사진이 화면 폭을 거의 채우고(좌우 여백 20px·모서리 직각), 표어 없이 사진 <b>아래</b>에 「이번 주일」 → 이번 주 설교 제목 → 본문 → 영상 버튼.</li>
  </ul>
</div>
<p class="sec">1 · 새 첫 화면 규격으로 얹어 본 세 장</p>
{"".join(heroes)}
<p class="sec">2 · 주제별 후보 (7주제 × 4장)</p>
{"".join(grids)}
<p class="foot">[초안] 2026-09-30 · 수집: Pexels 287장 → 216장 통과 · Commons(CC0·PD·CC BY 만) 120장 → 눈으로 고름 → 제목·촬영지·작가 대조 → 28장. 원본 정보: <code>r4/drafts/photo/v2/selected_v2.json</code>. 이번 주 설교 값 = latest.json(2026-09-27).</p>
</body></html>
'''
(V.parent.parent / "photo_후보.html").write_text(page, encoding="utf-8")
print("ok", len(sel), cnt_line, "region", n_region)
