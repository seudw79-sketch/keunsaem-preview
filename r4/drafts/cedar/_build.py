#!/usr/bin/env python3
"""T-HOME-CEDAR — cedarcrestchurch.com 의 틀(수치·배치)만 따르고 내용은 큰샘교회 것으로 채운 홈 1장 생성.
입력: ../c/_src/site.json(메뉴 8·예배 시간·주소 — c/ 와 같은 정본) · 미리보기 루트 latest.json(이번 주 설교 · c/ 빌드가 라이브와 동기화)
출력: ./index.html · 규격은 master 실측 computed style(2026-09-30) 그대로 — 남의 로고·사진·영상·문구·SVG 파일은 쓰지 않는다(물결은 우리가 그림).
"""
import json, html, re
from pathlib import Path
D = Path(__file__).resolve().parent
PREVIEW = D.parent.parent.parent
SITE = json.load(open(D.parent / "c" / "_src" / "site.json", encoding="utf-8"))
LATEST = json.load(open(PREVIEW / "latest.json", encoding="utf-8"))
esc = lambda s: html.escape(str(s), quote=True)

date, _, verse = LATEST["설교_날짜"].partition("·")
y, m, d = date.strip().split("-")
label = f"이번 주일 · {int(m)}월 {int(d)}일"
vid = LATEST["설교_링크"].split("v=")[1].split("&")[0]
nav = "".join(f'<a href="../c/{esc(n["file"])}">{esc(n["label"])}</a>' for n in SITE["nav"])   # 하위 8페이지는 아직 c/ 것을 가리킨다(cedar 하위는 오너 확인 뒤)
times = " · ".join(f'{esc(w["dt"])} {esc(w["dd"])}' for w in SITE["worship"])

# 물결 곡선 — 우리가 그린 것(외부 SVG 파일 사용 0)
WAVE = '<svg class="wave" viewBox="0 0 1000 100" preserveAspectRatio="none" aria-hidden="true"><path d="M0,100 L0,58 C250,30 500,30 750,58 C830,68 920,84 1000,92 L1000,100 Z"/></svg>'  # 우리가 그린 곡선 · viewBox 만 원판과 같음

CSS = r'''<style>
/* 규격 = master 실측(§1) + CSS 선언값(§7 · 선택자 근거) — 근사치 금지 · 값 그대로. html 16px 기준 em→px.
   제목 글꼴: Poynter(상용) 대체 → 한글 Noto Serif KR 700 · 영문 Playfair Display 700 · lowercase 는 한글 무효.
   ★색 두 토큰(master 판정): 읽는 글자 --teal-text #2A7D71(흰 위 4.92:1) · 장식 면 --teal-surface #47AB9D(원판). 오너가 원판 색 그대로를 원하면 --teal-text 만 #47AB9D 로 되돌린다. */
:root{--bg:#FFFFFF;--ink:#000;--teal-text:#2A7D71;--teal-surface:#47AB9D;--dark:#404140;--light:#B2AEAA;
  --sans:"Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif;--serif:"Noto Serif KR","Playfair Display",serif}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px}
/* 배경 옅은 질감 — CSS 만(이미지 0 · master 7 · 거의 안 보일 정도): 원판은 wood-texture.png + 흰 85% */
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.6;word-break:keep-all;overflow-wrap:break-word;
  background-image:repeating-linear-gradient(0deg,rgba(0,0,0,.018) 0 1px,transparent 1px 3px),repeating-linear-gradient(90deg,rgba(0,0,0,.012) 0 1px,transparent 1px 5px)}
a{color:inherit}img{display:block;max-width:100%;height:auto}
.wrap{width:min(1200px,calc(100% - 40px));margin:0 auto}
/* 맨 위 배너 — 왼쪽 정렬(master 1) · §7: .mo-9 12.8px 500 자간 .075em 흰 · 띠 .mo-4 padding 7px(바탕은 §1 검정 vs 선언 #404140 — master 답 전 §1) */
.banner{width:min(1200px,calc(100% - 40px));margin:14px auto 0;display:flex;justify-content:flex-start}
.banner span{display:inline-block;background:#000;color:#fff;font-size:12.8px;font-weight:500;letter-spacing:.075em;line-height:1.2;padding:7px 16px;border-radius:1600px;white-space:nowrap;overflow-x:auto;max-width:100%}
/* 떠 있는 흰 카드 헤더 — §1: #FFF · radius 16px · shadow rgba(0,0,0,.2) 0 0 16px · padding 20px (§7 .mo-5 일치) */
.hd{position:sticky;top:12px;z-index:10;margin:16px auto 0;width:min(1200px,calc(100% - 40px));background:#FFF;border-radius:16px;box-shadow:rgba(0,0,0,.2) 0 0 16px;padding:20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.logo{font-family:var(--serif);font-weight:700;font-size:22px;text-decoration:none;letter-spacing:-.01em;margin-right:auto}
/* 메뉴 — §7 ①②: 12.8px · 400 · lh 1 · 자간 .1em · 안쪽 여백 .75em(12px) · 대문자화 없음(한글) · hover 청록 */
.nav{display:flex;gap:0;align-items:center}
.nav a{font-size:12.8px;font-weight:400;line-height:1;letter-spacing:.1em;padding:12px;text-decoration:none}
.nav a:hover{color:var(--teal-text)}
/* VISIT 자리 알약 = 「새가족 안내」 — §7: .9em(14.4px) · 600 · 자간 .075em · padding .575em 1.15em · 1px solid 청록 · radius 100em */
.pill{font-size:14.4px;font-weight:600;letter-spacing:.075em;padding:.575em 1.15em;border:1px solid var(--teal-surface);border-radius:100em;color:var(--teal-text);text-decoration:none;white-space:nowrap;margin-left:8px}
.pill:hover{background:var(--teal-surface);color:#fff}
/* 네모 테두리 햄버거 — 상시 표시(master 2) · 드로어(전체 메뉴) */
.tg{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);border:0}
.burger{display:block;width:44px;height:44px;position:relative;cursor:pointer;border:1px solid #000;border-radius:8px;margin-left:8px}
.burger span,.burger::before,.burger::after{content:"";position:absolute;left:12px;width:18px;height:2px;background:#000}
.burger::before{top:14px}.burger span{top:20px}.burger::after{top:26px}
.tg:focus-visible ~ .burger{outline:2px solid var(--teal-text);outline-offset:2px}
.drawer{display:none;flex-basis:100%;flex-direction:column;padding-top:12px;border-top:1px solid #eee}
.tg:checked ~ .drawer{display:flex}
.drawer a{padding:12px 0;border-bottom:1px solid #eee;text-decoration:none;font-size:15px}.drawer a:last-child{border:0}
/* 첫 화면 — §7 .mu-1: 위 calc(8rem+80px) 아래 calc(8rem+40px) · 왼쪽 영상 16:9 모서리 2em · 오른쪽 라벨→제목→버튼 둘(성구 줄 없음 · master 4) */
.hero{position:relative;padding:calc(8rem + 80px - 96px) 0 calc(8rem + 40px);overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:7fr 5fr;gap:48px;align-items:center}
.media{position:relative;display:block;width:100%;padding-top:56.25%;height:0;overflow:hidden;border-radius:2em;background:#000}
.media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.media::after{content:"";position:absolute;left:50%;top:50%;width:84px;height:84px;margin:-42px 0 0 -42px;border-radius:50%;background:rgba(255,255,255,.92)}
.media::before{content:"";position:absolute;left:50%;top:50%;z-index:1;margin:-13px 0 0 -9px;border-style:solid;border-width:13px 0 13px 24px;border-color:transparent transparent transparent #000}
.label{font-size:16px;font-weight:400;color:var(--teal-text)}
h1.title{font-family:var(--serif);font-weight:700;font-size:56px;line-height:61.6px;text-transform:lowercase;color:#000;margin-top:12px;letter-spacing:-.01em}
/* 버튼 — §1: 16px · radius 1600px · 투명 · 1px solid #000 · 글자 청록(§7 선언은 #000 — master 답 전 §1) · 자간 §7 .075em · 굵기 600 */
.btn{display:inline-block;margin-top:24px;padding:.575em 1.15em;font-size:16px;font-weight:600;letter-spacing:.075em;border-radius:1600px;background:transparent;border:1px solid #000;color:var(--teal-text);text-decoration:none}
.btn:hover{background:#000;color:#fff}
.more{display:inline-block;margin-left:18px;margin-top:24px;font-size:16px;font-weight:600;letter-spacing:.075em;color:var(--teal-text);text-decoration:none;border:0}
/* 물결 — §7 ⑥: 150px · 첫 구역 하단 · 연회색 · 곡선은 우리가 그림 */
.wave{position:absolute;left:0;right:0;bottom:-1px;width:100%;height:150px;display:block;fill:var(--light)}
/* 연회색 구역(master 6 · §7 ⑤: #b2aeaa + linear-gradient(to bottom,#b2aeaa 0% 2%,#b2aeaa8c) · padding 6rem) — 성구 줄이 여기로 옮겨짐(내용 손실 0) */
.light{background-color:var(--light);background-image:linear-gradient(to bottom,#b2aeaa 0% 2%,#b2aeaa8c);padding:6rem 0;color:#000}
.light .wrap{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.light h2{font-family:var(--serif);font-weight:700;font-size:36px;line-height:1.25;text-transform:lowercase}
.light .verse{font-size:18px;line-height:1.7;margin-top:8px}
.light .muted{font-size:14px;margin-top:12px;color:#000}
/* 진회색 구역 — 다음 구역으로 내림(master 6) */
.dark{background:var(--dark);color:#fff;padding:6rem 0}
.dark .wrap{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
.dark h2{font-family:var(--serif);font-weight:700;font-size:36px;line-height:1.25;text-transform:lowercase}
.dark p{font-size:18px;line-height:1.7}
.dark .btn{border-color:#fff;color:#fff}.dark .btn:hover{background:#fff;color:var(--dark)}
.ft{padding:28px 0 40px;font-size:13px;color:var(--dark);text-align:center}
.ft a{text-decoration:none}
@media(max-width:960px){.nav{display:none}.hero .wrap{grid-template-columns:1fr;gap:28px}h1.title{font-size:40px;line-height:1.15}.light .wrap,.dark .wrap{grid-template-columns:1fr}.hero{padding-top:56px}}
@media(max-width:640px){.pill{display:none}.hd{top:8px;padding:16px}.banner span{font-size:11px}}
</style>'''

page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(SITE["church"])}</title>
<!-- T-HOME-CEDAR · 생성: r4/drafts/cedar/_build.py — 손으로 고치지 말 것. 규격=master 실측(cedarcrestchurch.com computed style 2026-09-30) · 내용=site.json·latest.json -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;500;600&family=Noto+Serif+KR:wght@700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
__CSS__
</head>
<body>
<div class="banner"><span>{times}</span></div>
<header class="hd">
  <a class="logo" href="index.html">{esc(SITE["church"])}</a>
  <input type="checkbox" id="tg" class="tg" aria-label="메뉴" aria-controls="drawer">
  <nav id="site-nav" class="nav" aria-label="주 메뉴">{nav}</nav>
  <a class="pill" href="../c/새가족.html">새가족 안내</a>
  <label for="tg" class="burger" aria-hidden="true"><span></span></label>
  <nav id="drawer" class="drawer" aria-label="전체 메뉴">{nav}</nav>
</header>
<main>
<section class="hero"><div class="wrap">
  <a class="media" id="sm-thumb" href="{esc(LATEST["설교_링크"])}" target="_blank" rel="noopener" aria-label="설교 영상 보기"><img id="sm-thumb-img" src="https://i.ytimg.com/vi/{esc(vid)}/hqdefault.jpg" alt="" loading="eager"></a>
  <div>
    <p class="label" id="sm-label">{esc(label)}</p>
    <h1 class="title" id="sm-title">{esc(LATEST["설교_제목"])}</h1>
    <a class="btn" id="sm-link" href="{esc(LATEST["설교_링크"])}" target="_blank" rel="noopener">설교 영상 보기</a><a class="more" href="../c/온라인예배.html">지난 설교</a>
  </div>
</div>
{WAVE}</section>
<section class="light"><div class="wrap">
  <div><h2 id="sm-title2">{esc(LATEST["설교_제목"])}</h2><p class="verse" id="sm-verse">{esc(verse.strip())}</p></div>
  <div><p class="muted" id="sm-label2">{esc(label)}</p></div>
</div></section>
<section class="dark"><div class="wrap">
  <div><h2>오시는 길</h2><p class="muted">{esc(SITE["church_full"])}</p></div>
  <div><p>{esc(SITE["address"])}<br><a href="tel:{esc(SITE["phone"])}">{esc(SITE["phone"])}</a></p>
    <a class="btn" href="https://map.kakao.com/link/search/경기%20광명시%20기아로%2023" target="_blank" rel="noopener">오시는 길 ↗</a></div>
</div></section>
</main>
<footer class="ft"><span>{esc(SITE["copyright"])}</span> · <span>T-HOME-CEDAR 비교 초안 · 내부 검토용</span></footer>
<script>
var LATEST_URL={json.dumps(SITE["latest_url"])};
if(location.protocol!=='file:')fetch(LATEST_URL,{{cache:'no-store'}}).then(function(r){{if(!r.ok)throw Error();return r.json()}}).then(function(d){{
  if(d.설교_제목&&d.설교_날짜&&/^https:\\/\\/www.youtube.com\\/watch\\?v=/.test(d.설교_링크)){{
    var p=d.설교_날짜.split('·'),ymd=p[0].trim().split('-');
    document.getElementById('sm-title').textContent=d.설교_제목;
    document.getElementById('sm-label').textContent='이번 주일 · '+parseInt(ymd[1],10)+'월 '+parseInt(ymd[2],10)+'일';
    document.getElementById('sm-verse').textContent=(p[1]||'').trim();document.getElementById('sm-title2').textContent=d.설교_제목;document.getElementById('sm-label2').textContent=document.getElementById('sm-label').textContent;
    ['sm-link','sm-thumb'].forEach(function(id){{document.getElementById(id).href=d.설교_링크}});
    var v=d.설교_링크.split('v=')[1].split('&')[0];document.getElementById('sm-thumb-img').src='https://i.ytimg.com/vi/'+v+'/hqdefault.jpg';
  }}
}}).catch(function(){{}});
</script>
</body>
</html>
'''
page = page.replace('__CSS__', CSS)
(D / "index.html").write_text(page, encoding="utf-8")
print("cedar/index.html", len(page), "B")
