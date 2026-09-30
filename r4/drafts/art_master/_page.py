#!/usr/bin/env python3
"""[초안] 명화 후보 페이지 — master 확보분(art_master/*.jpg · candidates.json · Met Open Access) → r4/drafts/명화_후보.html
번호 = master 파일 번호(오너 콘택트 시트 번호). 같은 작품의 중복 파일은 한 칸에 번호를 모두 표기. Met API 로 isPublicDomain=True 재확인(2026-09-30)."""
import json, html
from pathlib import Path

D = Path(__file__).resolve().parent
cand = json.load(open(D / "candidates.json", encoding="utf-8"))
SERMON = {"date": "2026. 9. 27.", "title": "광야에서도 신실하신 하나님", "ref": "민수기 14장 8–9절", "url": "https://www.youtube.com/watch?v=4Uw236eEFuk"}
# (대표번호, 같은 작품 번호들, 한국어 제목, 한 줄 설명, 비고)
WORKS = [
    ("22", ["22"], "추수하는 사람들", "황금빛 밀밭과 넓은 하늘 — 가장 힘 있는 그림, 추수의 계절감.", ""),
    ("27", ["27"], "산수(병풍)", "여백이 주인공인 일본 병풍 — ‘전시회 느낌’에 가장 가깝습니다.", ""),
    ("10", ["05", "10", "16"], "여울을 건너는 소 떼", "하늘이 화면 절반 이상 — 글자를 얹기에 가장 좋은 구도.", "05·10·16 은 같은 그림"),
    ("19", ["19"], "밀밭", "극적인 구름과 들판 — 네덜란드 풍경화의 대표작.", ""),
    ("15", ["15"], "퐁투아즈의 잘레 언덕", "초록 언덕과 마을길 — 밝고 차분한 인상파 풍경.", ""),
    ("21", ["21"], "레이스베이크의 네덜란드 운하", "수채 — 옅은 물빛, 색이 적어 가장 조용합니다.", ""),
    ("20", ["20"], "해 질 녘 폭포 앞의 두 사람", "노을빛 폭포 — 세로 그림이라 첫 화면보다 섹션용.", "세로 그림"),
    ("33", ["33"], "무지개가 있는 영웅적 풍경", "무지개와 산 — 세로 그림.", "세로 그림 · 시트 분류 ‘동양-한국’은 오기(독일 화가)"),
    ("30", ["30"], "산수", "메이지 시대 일본 산수 — 세로 그림.", "세로 그림"),
    ("31", ["31"], "연사모종 · 동정추월(소상팔경 중)", "조선 초 안견 전칭 — 한국 그림, 안개 낀 산과 물. 세로 그림.", "세로 그림"),
    ("37", ["37"], "꽃과 과일이 있는 정물", "정물 — 세로 그림, 섹션 배경·소재용.", "세로 그림"),
    ("24", ["24", "32"], "시가 있는 산수", "수묵 산수 화첩 — 원본 파일이 1000px 로 작아 전폭에는 부족(참고용).", "24·32 는 같은 그림 · 해상도 부족"),
]
EXCLUDED = [("00·18", "Camille Corot 「광야의 하갈」(1835)", "성경 장면(하갈과 천사)을 그린 종교화 — ‘교회 티 빼기’ 기준에 따라 제외. 00·18 은 같은 그림")]
HEROES = [("22", "center 45%"), ("27", "center 50%"), ("10", "center 40%")]

def esc(s): return html.escape(str(s or ""), quote=True)
def meta(n): return cand[int(n)]
def cap(n, ko, note):
    m = meta(n)
    return (f'<p class="who">{esc(m["artist"])} · 「{esc(ko)}」</p>'
            f'<p>{esc(m["title"])} · {esc(m["date"])} · {esc(m.get("medium",""))}</p>'
            f'<p>메트로폴리탄 미술관 소장 · Public Domain(저작권 만료 — 조건 없이 사용) · <a href="{esc(m["page"])}" target="_blank" rel="noopener">소장처 페이지 ↗</a></p>'
            + (f'<p class="note">{esc(note)}</p>' if note else ""))

by = {w[0]: w for w in WORKS}
heroes = []
for i, (n, pos) in enumerate(HEROES, 1):
    _, nums, ko, why, note = by[n]; m = meta(n)
    heroes.append(f'''
<section class="hv" aria-labelledby="hv{i}">
  <p class="hv__no">미리보기 {i} · {"·".join(nums)}번 「{esc(ko)}」</p>
  <figure class="hv__fig"><img src="art_master/web/{n}_2400.jpg" alt="" style="object-position:{pos}" {'fetchpriority="high"' if i == 1 else 'loading="lazy"'}></figure>
  <div class="hv__cap">
    <div><p class="lbl">이번 주일 · {SERMON["date"]}</p><h2 id="hv{i}">{SERMON["title"]}</h2><p class="ref">{SERMON["ref"]}</p>
      <a class="pill" href="{SERMON["url"]}" target="_blank" rel="noopener">설교 영상 보기 ↗</a></div>
    <p class="hv__credit">{esc(m["artist"])}, 「{esc(ko)}」({esc(m["date"])}) 부분 · 메트로폴리탄 미술관</p>
  </div>
  <div class="hv__why"><p><b>{"·".join(nums)}번</b> — {esc(why)}</p></div>
</section>''')

cards = "\n".join(f'''  <figure class="pc"><p class="num">{"·".join(nums)}</p><a href="art_master/web/{n}_1200.jpg" target="_blank" rel="noopener"><img src="art_master/web/{n}_1200.jpg" alt="" loading="lazy"></a><figcaption>{cap(n, ko, note)}<p class="why">{esc(why)}</p></figcaption></figure>''' for n, nums, ko, why, note in WORKS)
excl = "".join(f'<li><b>{esc(a)}</b> {esc(b)} — {esc(c)}</li>' for a, b, c in EXCLUDED)

page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>[초안] 명화 후보 — 첫 화면</title>
<meta name="robots" content="noindex">
<!-- [초안] 2026-09-30 · 생성=art_master/_page.py · 원본=art_master/NN.jpg(master 확보·Met Open Access) · 화면용=art_master/web/ · Met API isPublicDomain 재확인 -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
  :root{{--bg:#FFFFFF;--ink:#000000;--mute:#6B6B6B;--line:#E4E4E4;--sans:Pretendard,"Apple SD Gothic Neo",system-ui,sans-serif;--serif:"Noto Serif KR",serif;--edge:20px}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.7 var(--sans);word-break:keep-all}}
  a{{color:inherit}}
  .top{{display:flex;justify-content:space-between;align-items:baseline;padding:18px var(--edge);border-bottom:1px solid var(--line)}}
  .logo{{font-weight:500;font-size:16px}} .top small{{font-size:13px;color:var(--mute)}}
  .intro{{max-width:760px;margin:0 auto;padding:56px var(--edge) 24px}}
  .intro h1{{font:400 clamp(1.8rem,3.4vw,2.6rem)/1.3 var(--serif);letter-spacing:-.02em;margin:0 0 20px;text-wrap:balance}}
  .intro p,.intro li{{font-size:15px}} .intro ul{{padding-left:18px}}
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
  .hv__credit{{margin:0;font-size:12px;color:var(--mute);text-align:right;max-width:40ch}}
  .hv__why{{max-width:760px;margin:24px auto 0;padding:14px var(--edge);border-top:1px solid var(--line)}}
  .hv__why p{{margin:0;font-size:14px}}
  .pg{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:44px 20px;padding:24px var(--edge) 0}}
  .pc{{margin:0}} .num{{margin:0 0 8px;font:400 13px/1 var(--sans);color:var(--mute);letter-spacing:.06em}}
  .pc img{{display:block;width:100%;height:auto;background:var(--line)}}
  .pc figcaption{{padding-top:10px}} .pc p{{margin:2px 0;font-size:13px;color:var(--mute)}}
  .who{{color:var(--ink)!important;font-weight:500;font-size:14px!important}} .why{{color:var(--ink)!important}} .note{{color:var(--ink)!important}}
  .excl{{max-width:760px;margin:0 auto;padding:8px var(--edge) 0;font-size:14px}}
  .foot{{padding:48px var(--edge) 80px;font-size:13px;color:var(--mute);border-top:1px solid var(--line);margin-top:48px}}
  @media (max-width:640px){{.pg{{grid-template-columns:1fr}} .hv__cap{{flex-direction:column;align-items:flex-start}} .hv__credit{{text-align:left}} .hv__fig img{{height:62svh}}}}
</style>
</head><body>
<header class="top"><span class="logo">큰샘교회</span><small>[초안] 명화 후보 · 오너 검토용</small></header>
<div class="intro">
  <h1>첫 화면 명화 후보 — 미술관에 들어온 듯한 첫인상</h1>
  <p>「꼭 성경적이지 않아도 돼, 명화나 좋은 풍경」·「여기가 교회 홈페이지 맞나 하는 생각이 들도록」 말씀에 따라, <b>종교화가 아닌</b> 풍경화·산수화·정물만 모았습니다. 모두 뉴욕 <b>메트로폴리탄 미술관</b>이 저작권 만료(Public Domain)로 공개한 원본 고해상도 파일이라 조건 없이 쓸 수 있습니다.</p>
  <ul>
    <li><b>번호</b>는 앞서 받으신 콘택트 시트 번호 그대로입니다 — 번호로 골라 주시면 됩니다.</li>
    <li>맨 위 세 점은 새 첫 화면 규격으로 얹어 보았습니다 — 그림이 화면을 거의 채우고(좌우 여백 20px), 표어 없이 그림 <b>아래</b>에 「이번 주일」 → 이번 주 설교 제목 → 본문 → 영상 버튼. 첫 화면에서는 그림 일부가 잘려 보여서 캡션에 「부분」이라고 적었습니다.</li>
    <li>세로 그림(20·30·31·33·37)은 첫 화면보다 아래 구간·페이지 배경에 어울립니다.</li>
  </ul>
</div>
<p class="sec">1 · 새 첫 화면 규격으로 얹어 본 세 점</p>
{"".join(heroes)}
<p class="sec">2 · 후보 {len(WORKS)}점 (번호 = 콘택트 시트 번호)</p>
<div class="pg">
{cards}
</div>
<p class="sec">3 · 뺀 것</p>
<ul class="excl">{excl}</ul>
<p class="foot">[초안] 2026-09-30 · 원본 파일: r4/drafts/art_master/NN.jpg(master 확보) · 화면용 축소본: art_master/web/ · 각 작품 Public Domain 여부는 메트로폴리탄 미술관 공개 API(isPublicDomain)로 다시 확인했습니다.</p>
</body></html>
'''
(D.parent / "명화_후보.html").write_text(page, encoding="utf-8")
print("ok", len(WORKS))
